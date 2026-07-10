"""Tests fuer SKILL-035 (prep_bg.py) — Web-Variante, Validierung, Idempotenz."""
from __future__ import annotations

import pathlib

import pytest
from PIL import Image, ImageCms

from creative_studio.prep_bg import prep_bg, WEB_LONG_EDGE_PX
from creative_studio import specs


def _make_image(path: pathlib.Path, size: tuple[int, int], color=(180, 90, 40)) -> bytes:
    """Erzeugt ein einfaches RGB-Testbild und gibt seine Bytes zurueck (fuer Unveraendert-Check)."""
    img = Image.new("RGB", size, color)
    # leichte Struktur, damit JPEG nicht trivial 1px-komprimiert
    for x in range(0, size[0], 40):
        for y in range(0, size[1], 40):
            img.putpixel((x, y), (10, 10, 10))
    img.save(path, format="JPEG", quality=95)
    return path.read_bytes()


def test_ears1_web_variante_lange_kante_1440_und_srgb(tmp_path):
    """EARS-1: Web-Variante hat lange Kante 1440 px und sRGB, Original unveraendert."""
    src = tmp_path / "shot.jpg"
    original_bytes = _make_image(src, (4000, 2667))

    res = prep_bg(src, out_dir=tmp_path / "web")

    assert res.long_edge == WEB_LONG_EDGE_PX == 1440
    assert res.out.is_file()
    with Image.open(res.out) as out_img:
        assert max(out_img.size) == 1440
        assert out_img.mode == "RGB"
        # sRGB-ICC sollte eingebettet sein
        icc = out_img.info.get("icc_profile")
        if icc:
            import io
            prof = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            desc = (ImageCms.getProfileDescription(prof) or "").lower()
            assert "srgb" in desc or "iec 61966" in desc
    assert res.color_space == specs.COLOR_SPACE == "sRGB"
    # Original unangetastet
    assert src.read_bytes() == original_bytes


def test_ears1_original_in_anderem_ordner_unveraendert(tmp_path):
    """EARS-1: Schreiben in separaten web-Dir laesst Original-Datei byte-identisch."""
    src = tmp_path / "orig" / "shot.jpg"
    src.parent.mkdir()
    original_bytes = _make_image(src, (2000, 1500))
    before_mtime = src.stat().st_mtime

    res = prep_bg(src)  # ohne out -> web/ neben dem Original (EARS-4)

    assert res.out.parent == src.parent / "web"
    assert src.read_bytes() == original_bytes
    assert src.stat().st_mtime == before_mtime


def test_ears2_validierung_warnt_bei_zu_kleiner_kante(tmp_path):
    """EARS-2: kurze Kante < MIN_EDGE_PX erzeugt eine Warnung."""
    src = tmp_path / "tiny.jpg"
    _make_image(src, (1440, 600))  # kurze Kante 600 < 1080

    res = prep_bg(src, out_dir=tmp_path / "web")

    assert res.short_edge < specs.MIN_EDGE_PX
    assert any("MIN_EDGE_PX" in w for w in res.warnings)


def test_ears2_keine_warnung_bei_konformem_bild(tmp_path):
    """EARS-2: konforme Web-Variante (1440x1080) erzeugt keine Spec-Warnung."""
    src = tmp_path / "ok.jpg"
    _make_image(src, (2880, 2160))  # -> wird auf 1440x1080 skaliert

    res = prep_bg(src, out_dir=tmp_path / "web")

    assert res.short_edge >= specs.MIN_EDGE_PX
    assert res.warnings == ()


def test_ears3_idempotenz_kleines_konformes_bild_nicht_reencoded(tmp_path):
    """EARS-3: bereits konformes/kleines sRGB-Bild wird nur kopiert (skipped=True)."""
    src = tmp_path / "small.jpg"
    # lange Kante 1200 <= 1440, kleine Datei -> konform
    _make_image(src, (1200, 1200))

    res = prep_bg(src, out_dir=tmp_path / "web")

    assert res.skipped is True
    # Bytes der Web-Variante == Original (1:1 kopiert, kein Re-Encode)
    assert res.out.read_bytes() == src.read_bytes()


def test_ears3_grosses_bild_wird_reencoded(tmp_path):
    """EARS-3 (Gegenprobe): grosses Bild wird re-encoded (skipped=False, kleiner)."""
    src = tmp_path / "big.jpg"
    _make_image(src, (4000, 2667))

    res = prep_bg(src, out_dir=tmp_path / "web")

    assert res.skipped is False
    assert res.out_bytes < res.src_bytes


def test_input_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        prep_bg(tmp_path / "does_not_exist.jpg")
