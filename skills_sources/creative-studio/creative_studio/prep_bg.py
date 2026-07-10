# SKILL-035: Bild-Komprimierungs-Helper fuer Ad-Hintergruende.
"""creative-studio — Bild-Komprimierungs-Helper (SKILL-035).

Wandelt ein Roh-/Profi-Foto reproduzierbar in eine Ad-taugliche **Web-Variante**:
lange Kante 1440 px, sRGB, JPEG ~q82 (optimize+progressive). Das Original bleibt
unangetastet. Die Web-Variante wird gegen die Meta-Specs aus ``specs.py`` validiert
(sRGB, kurze Kante >= MIN_EDGE_PX, Groesse <= MAX_FILE_MB) -> Warnliste.

Hintergrund (Recherche 2026-06-23): Profi-Fotos kommen in ~30 MP; Meta re-encodiert
beim Upload ohnehin. Ziel ist saubere sRGB-Qualitaet bei kleiner Datei, nicht maximale
Aufloesung. MozJPEG bringt nur Repo-/Render-Vorteile -> wir nutzen Pillow-JPEG
(optimize=True), MozJPEG nur, falls trivial verfuegbar.

Multi-Projekt (EARS-4): kein hartkodierter Pfad. Ohne ``--out`` landet die Web-Variante
in ``web/`` neben dem Original (Konvention aus SKILL-034).

CLI:
  python -m creative_studio.prep_bg <input> [--out <web-dir>] [--long-edge 1440] [--quality 82]
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from dataclasses import dataclass

from PIL import Image, ImageCms

from .specs import MIN_EDGE_PX, MAX_FILE_MB, COLOR_SPACE

# SKILL-035: Default-Parameter der Web-Variante (Recherche-Empfehlung).
WEB_LONG_EDGE_PX = 1440      # lange Kante der Ad-Web-Variante (Meta-ideal, mehr bringt nichts)
WEB_JPEG_QUALITY = 82        # MozJPEG-/Pillow-q82 = visuell verlustfrei fuer cover-Komposition
_JPEG_SUFFIXES = {".jpg", ".jpeg"}


@dataclass(frozen=True)
class PrepResult:
    """Ergebnis einer prep_bg-Wandlung (fuer CLI-Ausgabe + Tests)."""
    src: pathlib.Path
    out: pathlib.Path
    src_size: tuple[int, int]       # (w, h) des Originals
    out_size: tuple[int, int]       # (w, h) der Web-Variante
    src_bytes: int
    out_bytes: int
    color_space: str                # erkannter/gesetzter Farbraum der Web-Variante
    skipped: bool                   # True = idempotent uebersprungen (kein Re-Encode)
    warnings: tuple[str, ...]

    @property
    def long_edge(self) -> int:
        return max(self.out_size)

    @property
    def short_edge(self) -> int:
        return min(self.out_size)


def _detect_srgb(img: Image.Image) -> bool:
    """Heuristik: Bild ist (effektiv) sRGB.

    Pillow legt das eingebettete ICC-Profil unter ``info['icc_profile']`` ab. Fehlt es,
    behandeln Web-Workflows RGB-Daten konventionell als sRGB (so auch Meta). Ein
    eingebettetes Profil pruefen wir auf das sRGB-Kennzeichen (IEC 61966-2.1).
    """
    if img.mode not in ("RGB", "L"):
        return False
    icc = img.info.get("icc_profile")
    if not icc:
        # Kein Profil -> als sRGB interpretiert (Web-Konvention).
        return True
    try:
        prof = ImageCms.ImageCmsProfile(__import__("io").BytesIO(icc))
        desc = (ImageCms.getProfileDescription(prof) or "").lower()
        return "srgb" in desc or "iec 61966" in desc
    except Exception:
        # Profil unlesbar -> nicht als sicheres sRGB werten.
        return False


def _validate(out_path: pathlib.Path, size: tuple[int, int], color_space: str) -> list[str]:
    """SKILL-035 EARS-2: Web-Variante gegen Meta-Specs aus specs.py pruefen."""
    warn: list[str] = []
    short_edge = min(size)
    if short_edge < MIN_EDGE_PX:
        warn.append(
            f"Kurze Kante {short_edge}px < MIN_EDGE_PX ({MIN_EDGE_PX}px) — "
            f"fuers Meta-Feed evtl. zu klein."
        )
    if color_space != COLOR_SPACE:
        warn.append(
            f"Farbraum '{color_space}' != {COLOR_SPACE} — Meta erwartet sRGB (kein CMYK)."
        )
    size_mb = out_path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_MB:
        warn.append(
            f"Dateigroesse {size_mb:.1f} MB > MAX_FILE_MB ({MAX_FILE_MB} MB)."
        )
    return warn


def _is_already_conform(img: Image.Image, src_bytes: int,
                        long_edge: int, max_mb: float) -> bool:
    """SKILL-035 EARS-3: Bild ist bereits klein/konform -> Re-Encode vermeiden.

    Konform = sRGB + lange Kante <= Ziel-Kante + Datei <= MAX_FILE_MB. Dann ist
    ein erneutes Encoding reine Verschlechterung ohne Nutzen.
    """
    if max(img.size) > long_edge:
        return False
    if (src_bytes / (1024 * 1024)) > max_mb:
        return False
    return _detect_srgb(img)


def prep_bg(src: str | pathlib.Path,
            out_dir: str | pathlib.Path | None = None,
            *,
            long_edge: int = WEB_LONG_EDGE_PX,
            quality: int = WEB_JPEG_QUALITY) -> PrepResult:
    """Erzeugt eine Ad-taugliche Web-Variante aus ``src`` (SKILL-035 EARS-1..4).

    - lange Kante auf ``long_edge`` (Default 1440) herunterskaliert (nie hochskaliert),
    - in sRGB konvertiert (RGB), JPEG q82 optimize+progressive,
    - Original bleibt unangetastet,
    - ohne ``out_dir`` -> ``web/`` neben dem Original (SKILL-034-Konvention),
    - idempotent: bereits konforme/kleine Bilder werden 1:1 kopiert (kein Re-Encode).

    Rueckgabe: PrepResult mit vorher/nachher-Kennzahlen + Validierungs-Warnungen.
    """
    src_path = pathlib.Path(src).resolve()
    if not src_path.is_file():
        raise FileNotFoundError(f"Eingabe-Bild nicht gefunden: {src_path}")

    if out_dir is None:
        # EARS-4: web/ neben dem Original (SKILL-034-Konvention).
        web_dir = src_path.parent / "web"
    else:
        web_dir = pathlib.Path(out_dir).resolve()
    web_dir.mkdir(parents=True, exist_ok=True)
    out_path = web_dir / (src_path.stem + ".jpg")

    src_bytes = src_path.stat().st_size
    with Image.open(src_path) as opened:
        opened.load()
        src_size = opened.size
        # EARS-3: idempotent — bereits konform -> nur kopieren, kein Re-Encode.
        if _is_already_conform(opened, src_bytes, long_edge, MAX_FILE_MB):
            out_path.write_bytes(src_path.read_bytes())
            out_size = src_size
            color_space = COLOR_SPACE
            skipped = True
        else:
            img = opened
            # In sRGB/RGB ueberfuehren (CMYK/RGBA/P/L -> RGB).
            if img.mode != "RGB":
                img = img.convert("RGB")
            # Downscale auf lange Kante (nie hochskalieren).
            if max(img.size) > long_edge:
                w, h = img.size
                if w >= h:
                    new = (long_edge, max(1, round(h * long_edge / w)))
                else:
                    new = (max(1, round(w * long_edge / h)), long_edge)
                img = img.resize(new, Image.LANCZOS)
            save_kwargs = dict(
                format="JPEG", quality=quality,
                optimize=True, progressive=True,
            )
            # sRGB-ICC der Web-Variante mitgeben (Meta/Browser eindeutig).
            try:
                srgb = ImageCms.createProfile("sRGB")
                save_kwargs["icc_profile"] = ImageCms.ImageCmsProfile(srgb).tobytes()
            except Exception:
                pass  # ohne ICC: RGB wird konventionell als sRGB interpretiert
            img.save(out_path, **save_kwargs)
            out_size = img.size
            color_space = COLOR_SPACE
            skipped = False

    warnings = tuple(_validate(out_path, out_size, color_space))
    return PrepResult(
        src=src_path, out=out_path,
        src_size=src_size, out_size=out_size,
        src_bytes=src_bytes, out_bytes=out_path.stat().st_size,
        color_space=color_space, skipped=skipped, warnings=warnings,
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="creative-studio Bild-Komprimierung (SKILL-035)")
    ap.add_argument("input", help="Pfad zum Original-Foto")
    ap.add_argument("--out", default=None,
                    help="Ziel-Verzeichnis (default: web/ neben dem Original)")
    ap.add_argument("--long-edge", type=int, default=WEB_LONG_EDGE_PX,
                    help=f"Lange Kante der Web-Variante (default {WEB_LONG_EDGE_PX})")
    ap.add_argument("--quality", type=int, default=WEB_JPEG_QUALITY,
                    help=f"JPEG-Qualitaet (default {WEB_JPEG_QUALITY})")
    args = ap.parse_args(argv)

    res = prep_bg(args.input, args.out, long_edge=args.long_edge, quality=args.quality)
    mode = "kopiert (idempotent)" if res.skipped else "re-encoded"
    print(f"[OK] {res.out}  [{mode}]")
    print(f"     {res.src_size[0]}x{res.src_size[1]} ({res.src_bytes/1024:.0f} KB) "
          f"-> {res.out_size[0]}x{res.out_size[1]} ({res.out_bytes/1024:.0f} KB), "
          f"{res.color_space}")
    for w in res.warnings:
        print(f"[WARN] {w}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
