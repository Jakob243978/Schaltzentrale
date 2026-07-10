"""Tests fuer SKILL-032 (cropping.py) — content-aware Crop von Foto-Hintergruenden.

Deckt die EARS-Kriterien aus SKILL-032 (und damit SKILL-020 EARS-6) ab:
  - EARS-1: falsches Ratio -> content-aware Crop aufs Ziel-Ratio (kein Verzerren).
  - EARS-3: je Format (4:5, 9:16, 1:1) ein eigener, exakt-massgenauer Crop aus EINER Quelle.
  - EARS-4: ohne smartcrop-Lib -> Fallback-Crop, klar markiert (kein harter Abbruch).
  - Determinismus: gleiche Eingabe -> identisches Crop-Rechteck/Bytes.
"""
from __future__ import annotations

import pathlib

import pytest
from PIL import Image

from creative_studio.cropping import (
    crop_to_format,
    _ratio_box_from_focal,
    _maximal_ratio_box,
    _HAS_SMARTCROP,
    _HAS_FACE,
)
from creative_studio import specs


def _make_salient_image(path: pathlib.Path, size=(2000, 1000)) -> None:
    """Querformat-Testbild (2:1) mit einem markanten hellen Block rechts der Mitte.

    Saliency soll diesen Bereich erkennen; das Ergebnis-Crop muss das Ziel-Ratio
    exakt treffen — egal ob smartcrop oder Fallback.
    """
    w, h = size
    img = Image.new("RGB", size, (60, 60, 70))
    # leichte Struktur ueberall (sonst trivialer Crop)
    for x in range(0, w, 25):
        for y in range(0, h, 25):
            img.putpixel((x, y), (90, 90, 100))
    # markanter Focal-Block (hell/warm) bei ~70 % Breite, vertikal Mitte
    for x in range(int(w * 0.62), int(w * 0.82)):
        for y in range(int(h * 0.30), int(h * 0.62)):
            img.putpixel((x, y), (255, 70, 40))
    img.save(path, format="JPEG", quality=95)


@pytest.mark.parametrize("fmt_key", ["story_9x16", "feed_4x5", "square_1x1"])
def test_ears3_crop_trifft_zielmasse_und_ratio_exakt(tmp_path, fmt_key):
    """EARS-1/EARS-3: Crop auf 9:16 / 4:5 / 1:1 -> exakte Zielmaße + exaktes Ratio."""
    src = tmp_path / "shot.jpg"
    _make_salient_image(src)
    fmt = specs.get_format(fmt_key)
    out = tmp_path / f"crop_{fmt_key}.jpg"

    res = crop_to_format(src, fmt, out)

    assert out.is_file()
    with Image.open(out) as im:
        assert im.size == (fmt.width, fmt.height)  # exakte Zielmaße
    # exaktes Ziel-Ratio (kein Verzerren) — Toleranz nur fuer Float-Rundung
    assert res.out_size == (fmt.width, fmt.height)
    assert abs((fmt.width / fmt.height) - (res.out_size[0] / res.out_size[1])) < 1e-9


def test_ears1_querformat_quelle_nicht_verzerrt(tmp_path):
    """EARS-1: 2:1-Quelle in 9:16 wird gecroppt (Breite beschnitten), nicht gestaucht.

    Der gewaehlte Crop-Bereich muss schmaler als das Original sein (echtes Crop),
    und das Ergebnis trifft das Hochformat exakt.
    """
    src = tmp_path / "wide.jpg"
    _make_salient_image(src, size=(2000, 1000))
    fmt = specs.get_format("story_9x16")
    out = tmp_path / "wide_9x16.jpg"

    res = crop_to_format(src, fmt, out)

    left, upper, right, lower = res.crop_box
    crop_w = right - left
    crop_h = lower - upper
    # Hochformat aus Querformat -> Crop-Box ist schmaler als das Original (Breite beschnitten)
    assert crop_w < res.src_size[0]
    assert crop_h == res.src_size[1]  # volle Hoehe genutzt
    # Crop-Box selbst hat (bis auf Rundung) das Ziel-Ratio
    box_ratio = crop_w / crop_h
    target_ratio = fmt.width / fmt.height
    assert abs(box_ratio - target_ratio) < 0.01


def test_kein_upscaling_bei_grosser_quelle(tmp_path):
    """Kein Upscaling-Artefakt: Quelle >> Zielmaße -> upscaled=False."""
    src = tmp_path / "big.jpg"
    _make_salient_image(src, size=(4000, 2000))
    out = tmp_path / "big_9x16.jpg"

    res = crop_to_format(src, "story_9x16", out)

    assert res.upscaled is False


def test_determinismus_identische_bytes(tmp_path):
    """Determinismus: gleiche Eingabe -> identisches Crop-Rechteck UND identische Bytes."""
    src = tmp_path / "shot.jpg"
    _make_salient_image(src)
    out_a = tmp_path / "a.jpg"
    out_b = tmp_path / "b.jpg"

    res_a = crop_to_format(src, "feed_4x5", out_a)
    res_b = crop_to_format(src, "feed_4x5", out_b)

    assert res_a.crop_box == res_b.crop_box
    assert out_a.read_bytes() == out_b.read_bytes()


def test_ears4_fallback_crop_erzwungen_ist_markiert(tmp_path):
    """EARS-4: use_smartcrop=False erzwingt Fallback -> method markiert, Maße korrekt."""
    src = tmp_path / "shot.jpg"
    _make_salient_image(src)
    out = tmp_path / "fallback.jpg"

    res = crop_to_format(src, "square_1x1", out, use_smartcrop=False)

    assert res.method == "fallback-center"
    with Image.open(out) as im:
        assert im.size == (1080, 1080)


def test_ears4_fallback_box_ratio_korrekt():
    """EARS-4: der reine Fallback-Box-Helfer liefert ein ratio-korrektes Rechteck."""
    # 2000x1000 (2:1) -> 9:16 (1080x1920)
    box = _ratio_box_from_focal(2000, 1000, 1080, 1920, 0.38)
    left, upper, right, lower = box
    w = right - left
    h = lower - upper
    assert h == 1000  # volle Hoehe
    assert abs((w / h) - (1080 / 1920)) < 0.01
    assert left >= 0 and right <= 2000


def test_ears1_smartcrop_pfad_volle_aufloesung(tmp_path):
    """EARS-1: ist smartcrop verfuegbar, nutzt der Crop die volle Quell-Aufloesung.

    Der smartcrop-Pfad baut um den Saliency-Focal-Point die MAXIMALE ratio-korrekte
    Box (eine Kante == Originalkante) -> kein unnoetiges Upscaling, ratio-korrekt.
    (Welche Saliency smartcrop auf einem synthetischen Bild findet, ist lib-intern;
    EARS-1 = content-aware + verlustarm, nicht ein fixer Pixel.)
    Skip, wenn die Lib fehlt (Fallback-Pfad ist via EARS-4-Test abgedeckt).
    """
    if not _HAS_SMARTCROP:
        pytest.skip("smartcrop nicht installiert — Fallback-Pfad via EARS-4-Test geprueft")
    src = tmp_path / "shot.jpg"
    _make_salient_image(src, size=(2000, 1000))
    out = tmp_path / "sc.jpg"

    res = crop_to_format(src, "story_9x16", out)

    assert res.method == "smartcrop"
    left, upper, right, lower = res.crop_box
    crop_w, crop_h = right - left, lower - upper
    # Querformat -> 9:16: volle Hoehe genutzt (maximale verfuegbare Aufloesung).
    assert crop_h == res.src_size[1]
    # Crop-Box ratio-korrekt (kein Verzerren).
    assert abs((crop_w / crop_h) - (9 / 16)) < 0.01
    # SKILL-035-Lehre: ein 2:1-Foto deckt 9:16 nicht ohne Upscaling -> ehrlich markiert.
    assert res.upscaled is True


def _make_face_image(path: pathlib.Path, size=(2000, 1200)) -> tuple[int, int]:
    """Querformat-Bild mit einem groben 'Gesicht' (Hautton-Oval + Augen) rechts.

    Reicht fuer die Haar-Cascade i.d.R. NICHT (die braucht echte Foto-Features),
    daher wird der Face-Test bei 0 Treffern uebersprungen — der ECHTE Face-Beleg
    kommt aus dem dokumentierten Real-Test (Header-Foto, 1 Gesicht erkannt).
    """
    from PIL import ImageDraw
    w, h = size
    img = Image.new("RGB", size, (40, 40, 50))
    d = ImageDraw.Draw(img)
    cx, cy = int(w * 0.72), int(h * 0.45)
    d.ellipse([cx - 130, cy - 170, cx + 130, cy + 170], fill=(228, 190, 165))
    d.ellipse([cx - 70, cy - 40, cx - 30, cy], fill=(30, 30, 30))
    d.ellipse([cx + 30, cy - 40, cx + 70, cy], fill=(30, 30, 30))
    img.save(path, format="JPEG", quality=95)
    return (cx, cy)


def test_ears2_face_bleibt_im_crop_wenn_erkannt(tmp_path):
    """EARS-2: wird ein Gesicht erkannt, liegt sein Mittelpunkt im Crop (method='face').

    Skip, wenn OpenCV fehlt ODER die Cascade auf dem synthetischen Bild nichts findet
    (EARS-2 ist am echten Foto im Real-Test belegt — 1 Gesicht erkannt, Kopf zentriert).
    """
    if not _HAS_FACE:
        pytest.skip("OpenCV nicht installiert — Face-Pfad faellt auf smartcrop zurueck")
    src = tmp_path / "face.jpg"
    cx, cy = _make_face_image(src)
    out = tmp_path / "face_9x16.jpg"

    res = crop_to_format(src, "story_9x16", out)

    if res.faces == 0:
        pytest.skip("Haar-Cascade fand kein Gesicht im synthetischen Bild — "
                    "EARS-2 ist im Real-Test belegt")
    assert res.method == "face"
    left, upper, right, lower = res.crop_box
    assert left <= cx <= right
    assert upper <= cy <= lower


def test_maximal_box_zentriert_focal_und_bleibt_im_bild():
    """SKILL-032: maximal-Box zentriert den Focal-Point und laeuft nie ueber den Rand."""
    # Querformat 4000x2667, Ziel 9:16, Focal weit rechts -> Box am rechten Rand geklemmt.
    box = _maximal_ratio_box(4000, 2667, 1080, 1920, focal_x=3900, focal_y=1300)
    left, upper, right, lower = box
    assert left >= 0 and right <= 4000
    assert lower - upper == 2667  # volle Hoehe
    assert abs(((right - left) / (lower - upper)) - (1080 / 1920)) < 0.01


def test_input_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        crop_to_format(tmp_path / "nope.jpg", "feed_4x5", tmp_path / "o.jpg")
