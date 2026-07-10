# SKILL-032: Content-aware Smartcrop fuer Foto-Hintergruende (--bg-image).
"""creative-studio — Content-aware Crop von Foto-Hintergruenden (SKILL-032).

Schliesst die offene EARS-6 aus SKILL-020: ein Hintergrundfoto, das nicht das
Ziel-Ratio eines Ad-Formats hat, wird **content-aware** auf das Ziel-Ratio
gecroppt — statt es per CSS ``background: cover`` blind zu beschneiden oder zu
verzerren. So bleibt der wichtige Bildinhalt (Saliency + Kanten, optional
Gesichter) im sichtbaren Bereich.

Strategie (zwei Stufen, transparent markiert):
  1. ``smartcrop`` (smartcrop-py): Saliency-/Kanten-/Hautton-Gewichtung findet den
     Focal Point und liefert das beste Crop-Rechteck im Ziel-Ratio (EARS-1/EARS-2).
  2. Fallback (``method="fallback-center"``), wenn ``smartcrop`` fehlt oder fehlschlaegt:
     ein ratio-korrekter, leicht nach oben gewichteter Crop (Gesichter sitzen
     meist im oberen Drittel). Klar als Fallback gekennzeichnet — kein stiller Fake
     (EARS-4 aus SKILL-032, deckt SKILL-020 EARS-6 ab).

Multi-Projekt (EARS-5): kein hartkodierter Bildpfad/Brand-Wert — Quelle + Ziel-Format
kommen als Parameter rein. Das Ziel-Ratio + die Zielmaße stammen aus ``specs.AdFormat``.

CLI:
  python -m creative_studio.cropping <input> --format feed_4x5 --out <pfad.jpg>
"""
from __future__ import annotations

import argparse
import math
import pathlib
import sys
from dataclasses import dataclass

from PIL import Image

from .specs import AdFormat, get_format, FORMATS

# SKILL-032: smartcrop ist optional. Fehlt es, faellt crop_to_format auf den
# zentriert-oberen Crop zurueck (EARS-4) und markiert das im Ergebnis.
try:  # pragma: no cover - reiner Import-Guard
    import smartcrop as _smartcrop_mod
    _HAS_SMARTCROP = True
except Exception:  # pragma: no cover
    _smartcrop_mod = None
    _HAS_SMARTCROP = False

# SKILL-032 / EARS-2: optionale Gesichts-Erkennung (OpenCV Haar-Cascade). Ist sie
# verfuegbar und findet ein Gesicht, wird DESSEN Mittelpunkt als Focal-Point genutzt
# (statt der reinen Saliency) — so wird das Gesicht nicht aus dem Crop geschoben.
# Fehlt OpenCV, faellt der Pfad still auf smartcrop/Fallback zurueck (kein Hard-Fail).
try:  # pragma: no cover - reiner Import-Guard
    import cv2 as _cv2
    import numpy as _np
    _HAS_FACE = True
except Exception:  # pragma: no cover
    _cv2 = None
    _np = None
    _HAS_FACE = False

# SKILL-032: Wo der Focal-Point beim Fallback-Crop vertikal sitzt (0 = oben, 0.5 = Mitte).
# 0.38 = leicht oberhalb der Mitte -> Gesichter/Koepfe bleiben tendenziell drin.
_FALLBACK_VERTICAL_BIAS = 0.38


@dataclass(frozen=True)
class CropResult:
    """Ergebnis eines crop_to_format-Laufs (fuer CLI-Ausgabe + Tests)."""
    src: pathlib.Path
    out: pathlib.Path
    src_size: tuple[int, int]       # (w, h) des Originals
    crop_box: tuple[int, int, int, int]  # (left, upper, right, lower) im Original
    out_size: tuple[int, int]       # (w, h) des fertigen Crops == Zielmaße des Formats
    method: str                     # "face" | "smartcrop" | "fallback-center"
    upscaled: bool                  # True = Crop-Region war kleiner als Zielmaße (Upscaling)
    faces: int = 0                  # Anzahl erkannter Gesichter (EARS-2)


def _maximal_ratio_box(
    src_w: int, src_h: int, target_w: int, target_h: int,
    focal_x: float, focal_y: float,
) -> tuple[int, int, int, int]:
    """SKILL-032: GROESSTES Rechteck im Ziel-Ratio innerhalb (src_w x src_h),
    um den Focal-Point ``(focal_x, focal_y)`` (Pixelkoordinaten) zentriert.

    Nutzt immer die volle moegliche Aufloesung (eine Kante == Originalkante) und
    schiebt das Rechteck so, dass der Focal-Point moeglichst zentral bleibt — ohne
    ueber den Bildrand zu laufen. Das verhindert unnoetiges Upscaling (SKILL-035-Lehre)
    und haelt den Focal-Bereich (Saliency/Gesicht) im sichtbaren Crop.
    """
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        # Quelle breiter -> volle Hoehe, Breite beschneiden, horizontal am Focal ausrichten.
        new_h = src_h
        new_w = int(round(new_h * target_ratio))
        left = int(round(focal_x - new_w / 2))
        left = max(0, min(left, src_w - new_w))
        upper = 0
    else:
        # Quelle schmaler/hoeher -> volle Breite, Hoehe beschneiden, vertikal am Focal ausrichten.
        new_w = src_w
        new_h = int(round(new_w / target_ratio))
        upper = int(round(focal_y - new_h / 2))
        upper = max(0, min(upper, src_h - new_h))
        left = 0
    return (left, upper, left + new_w, upper + new_h)


def _ratio_box_from_focal(
    src_w: int, src_h: int, target_w: int, target_h: int, focal_v: float
) -> tuple[int, int, int, int]:
    """SKILL-032: Fallback-Box im Ziel-Ratio (kein Saliency).

    Horizontal zentriert, vertikal nach ``focal_v`` gewichtet (0=oben .. 0.5=Mitte),
    damit Gesichter/Koepfe (meist oberes Drittel) im Crop bleiben. Liefert immer die
    maximale Aufloesung (eine Kante == Originalkante).
    """
    focal_x = src_w * 0.5  # horizontal zentriert (kein Saliency)
    target_ratio = target_w / target_h
    if (src_w / src_h) > target_ratio:
        # Quelle breiter -> volle Hoehe, vertikal mittig.
        return _maximal_ratio_box(src_w, src_h, target_w, target_h, focal_x, src_h * 0.5)
    # Quelle schmaler/hoeher -> oben-gewichtet: upper ~ (src_h-new_h)*focal_v.
    new_h = int(round(src_w / target_ratio))
    focal_y = (src_h - new_h) * focal_v + new_h / 2
    return _maximal_ratio_box(src_w, src_h, target_w, target_h, focal_x, focal_y)


def _smartcrop_box(
    img: Image.Image, target_w: int, target_h: int
) -> tuple[int, int, int, int]:
    """SKILL-032: content-aware Box im Ziel-Ratio via smartcrop.

    smartcrop (Saliency + Kanten + Hautton) liefert das beste Crop-Rechteck fuer
    das reduzierte Ziel-Ratio. Wir nehmen dessen **Focal-Mittelpunkt** und bauen
    daraus die MAXIMALE ratio-korrekte Box (volle Aufloesung) — smartcrops eigene
    Box ist durch ``min_scale`` oft kleiner als noetig und wuerde unnoetig upscalen.
    """
    g = math.gcd(target_w, target_h)
    rw, rh = target_w // g, target_h // g
    sc = _smartcrop_mod.SmartCrop()
    result = sc.crop(img, rw, rh)
    tc = result["top_crop"]
    focal_x = tc["x"] + tc["width"] / 2.0
    focal_y = tc["y"] + tc["height"] / 2.0
    box = _maximal_ratio_box(img.width, img.height, target_w, target_h, focal_x, focal_y)
    return _clamp_box(box, img.size)


def _detect_faces(img: Image.Image):
    """SKILL-032 / EARS-2: Gesichter im Bild (Liste von (x, y, w, h)) oder [].

    Nutzt OpenCVs frontale Haar-Cascade. Fehlt OpenCV / kein Treffer -> []. Reine
    Heuristik (kein DNN), bewusst leichtgewichtig — soll nur den Focal-Point
    in Richtung Gesicht ziehen, nicht perfekt segmentieren.
    """
    if not _HAS_FACE:
        return []
    try:  # pragma: no cover - lib-internal robustness
        arr = _np.asarray(img)
        gray = _cv2.cvtColor(arr, _cv2.COLOR_RGB2GRAY)
        casc_path = _cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        cascade = _cv2.CascadeClassifier(casc_path)
        if cascade.empty():
            return []
        # minSize relativ zur Bildkante -> robust ueber Aufloesungen.
        min_edge = max(40, int(min(img.size) * 0.04))
        faces = cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(min_edge, min_edge)
        )
        return [tuple(int(v) for v in f) for f in faces]
    except Exception:  # pragma: no cover
        return []


def _face_focal(faces) -> tuple[float, float]:
    """SKILL-032: Focal-Point aus erkannten Gesichtern = Mittelpunkt des groessten Gesichts."""
    fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])
    return (fx + fw / 2.0, fy + fh / 2.0)


def _clamp_box(
    box: tuple[int, int, int, int], size: tuple[int, int]
) -> tuple[int, int, int, int]:
    """SKILL-032: Box defensiv in die Bildgrenzen klemmen (smartcrop kann ueber Rand laufen)."""
    w, h = size
    left, upper, right, lower = box
    left = max(0, min(left, w - 1))
    upper = max(0, min(upper, h - 1))
    right = max(left + 1, min(right, w))
    lower = max(upper + 1, min(lower, h))
    return (left, upper, right, lower)


def crop_to_format(
    image_path,
    fmt: AdFormat | str,
    out_path,
    *,
    use_smartcrop: bool = True,
    quality: int = 88,
) -> CropResult:
    """SKILL-032: Croppt ``image_path`` content-aware auf das Ziel-Ratio von ``fmt``.

    - Croppt auf das exakte Ziel-Ratio (AdFormat.width/height), ohne zu verzerren.
    - Skaliert die Crop-Region auf die Zielmaße des Formats (Aspect bleibt exakt).
    - smartcrop (Saliency/Kanten/Hautton) findet den Focal Point (EARS-1/EARS-2);
      bei fehlender Lib / Fehler -> ratio-korrekter, oben-gewichteter Crop (EARS-4).

    Deterministisch: gleiche Eingabe -> gleiches Crop-Rechteck/Ergebnis.
    ``upscaled`` zeigt an, ob die Crop-Region kleiner als die Zielmaße war
    (Hinweis fuer Mindestkanten-Pruefung, vgl. SKILL-035-Lehre).
    """
    if isinstance(fmt, str):
        fmt = get_format(fmt)
    src = pathlib.Path(image_path)
    if not src.is_file():
        raise FileNotFoundError(f"Hintergrundbild nicht gefunden: {src}")
    out = pathlib.Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(src) as raw:
        img = raw.convert("RGB")
        src_w, src_h = img.size
        target_w, target_h = fmt.width, fmt.height

        method = "fallback-center"
        box: tuple[int, int, int, int] | None = None
        faces: list = []

        if use_smartcrop:
            # EARS-2: Gesicht hat Vorrang vor reiner Saliency -> Gesichts-Mittelpunkt
            # wird Focal-Point, damit das Gesicht im Crop bleibt.
            faces = _detect_faces(img)
            if faces:
                fx, fy = _face_focal(faces)
                box = _clamp_box(
                    _maximal_ratio_box(src_w, src_h, target_w, target_h, fx, fy),
                    img.size,
                )
                method = "face"
            elif _HAS_SMARTCROP:
                try:
                    box = _smartcrop_box(img, target_w, target_h)
                    method = "smartcrop"
                except Exception as exc:  # pragma: no cover - lib-internal robustness
                    print(f"[WARN] SKILL-032: smartcrop fehlgeschlagen ({exc}) — "
                          f"Fallback auf zentriert-oberen Crop.", file=sys.stderr)
                    box = None
            else:
                print("[WARN] SKILL-032: 'smartcrop' nicht installiert — Fallback auf "
                      "zentriert-oberen Crop (kein Saliency). `pip install smartcrop` "
                      "fuer content-aware Crop.", file=sys.stderr)

        if box is None:
            box = _ratio_box_from_focal(
                src_w, src_h, target_w, target_h, _FALLBACK_VERTICAL_BIAS
            )

        cropped = img.crop(box)
        crop_w, crop_h = cropped.size
        upscaled = crop_w < target_w or crop_h < target_h
        # SKILL-032: auf exakte Zielmaße bringen -> exaktes Ratio, keine Verzerrung
        # (Crop-Box ist bereits ratio-korrekt, das ist nur ein sauberes Resample).
        final = cropped.resize((target_w, target_h), Image.LANCZOS)

        save_kwargs = {}
        suffix = out.suffix.lower()
        if suffix in (".jpg", ".jpeg"):
            save_kwargs = {"quality": quality, "optimize": True, "progressive": True}
            icc = img.info.get("icc_profile")
            if icc:
                save_kwargs["icc_profile"] = icc
        final.save(out, **save_kwargs)

    return CropResult(
        src=src,
        out=out,
        src_size=(src_w, src_h),
        crop_box=box,
        out_size=(target_w, target_h),
        method=method,
        upscaled=upscaled,
        faces=len(faces),
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="creative-studio content-aware Smartcrop (SKILL-032)")
    ap.add_argument("input", help="Pfad zum Hintergrundfoto")
    ap.add_argument("--format", required=True,
                    help=f"Ziel-Format, eines aus: {', '.join(FORMATS)}")
    ap.add_argument("--out", required=True, help="Ziel-Pfad fuers Crop (PNG/JPG)")
    ap.add_argument("--no-smartcrop", action="store_true",
                    help="smartcrop deaktivieren -> Fallback-Crop erzwingen")
    args = ap.parse_args(argv)

    res = crop_to_format(args.input, args.format, args.out,
                         use_smartcrop=not args.no_smartcrop)
    print(f"[OK] {res.out}  {res.out_size[0]}x{res.out_size[1]}  "
          f"method={res.method}  upscaled={res.upscaled}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
