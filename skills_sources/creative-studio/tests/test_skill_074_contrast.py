"""SKILL-074 — Tests fuer den Lesbarkeits-/Kontrast-Check (readability.py).

1 EARS = mind. 1 Test:
  - EARS-1: WCAG-Kontrast-Ratio korrekt (weiss/schwarz=21, gleich=1) + AA-Schwellen.
  - EARS-2: Guter Kontrast (heller Text auf dunklem BG unter dem Text) -> KEINE Warnung.
  - EARS-3: Schlechter Kontrast (heller Text auf hellem BG unter dem Text) -> Warnung
            mit Region + gemessenem Wert (warnen, NICHT blocken).
  - EARS-4: Foto-BG + geringer Kontrast -> Fix-Empfehlung (Scrim/Text-Panel).
  - EARS-5 [multi-projekt]: Textfarben/Geometrie kommen als Parameter — kein Brand-Hardcode.

Rein PIL, kein Playwright (schnell, offline). Synthetische Bilder: der untere
Bereich (wo Headline/Subline/CTA sitzen) wird flaechig eingefaerbt, damit die
gesampelten Kacheln deterministisch die Testfarbe treffen — unabhaengig von der
exakten Region-Fraktion.
"""
from PIL import Image

from creative_studio.readability import (
    contrast_ratio, relative_luminance, parse_color,
    check_contrast, contrast_warnings, recommend_contrast_fix,
    text_regions, WCAG_AA_NORMAL, WCAG_AA_LARGE,
)
from creative_studio.specs import AdContent, get_format

_FMT = get_format("feed_4x5")

# Dunkle Marke (Bestand): heller Ink/Muted, oranger Akzent.
_BRAND_DARK = {
    "BRAND_INK": "#faf7f2", "BRAND_INK_MUTED": "#9a9ec0", "BRAND_ACCENT": "#f25d3e",
}
_CONTENT = AdContent(headline="Verdoppeln", subline="Ohne doppeltes Team.",
                     cta="Auf die Warteliste", eyebrow="MENTORING")


def _img_lower_filled(fill, size=(1080, 1350), top=(20, 30, 60)):
    """Bild: obere Haelfte `top`, untere ~65 % `fill` (deckt alle Text-Regionen)."""
    img = Image.new("RGB", size, top)
    y = int(size[1] * 0.35)
    lower = Image.new("RGB", (size[0], size[1] - y), fill)
    img.paste(lower, (0, y))
    return img


# === EARS-1: WCAG-Kern ========================================================
def test_contrast_ratio_white_black_is_21():
    assert round(contrast_ratio((255, 255, 255), (0, 0, 0)), 1) == 21.0


def test_contrast_ratio_identical_is_1():
    assert round(contrast_ratio((120, 120, 120), (120, 120, 120)), 3) == 1.0


def test_relative_luminance_monotonic():
    assert relative_luminance((0, 0, 0)) < relative_luminance((128, 128, 128)) \
        < relative_luminance((255, 255, 255))


def test_thresholds_are_wcag_aa():
    assert WCAG_AA_NORMAL == 4.5
    assert WCAG_AA_LARGE == 3.0


def test_parse_color_forms():
    assert parse_color("#fff") == (255, 255, 255)
    assert parse_color("#f25d3e") == (242, 93, 62)
    assert parse_color("rgb(10, 14, 39)") == (10, 14, 39)
    assert parse_color("white") == (255, 255, 255)
    assert parse_color("") == (0, 0, 0)   # sicherer Default, kein Crash


# === EARS-2: guter Kontrast -> keine Warnung ==================================
def test_good_contrast_no_warning():
    # Heller Ink/Muted/Akzent auf dunklem Navy-Untergrund -> lesbar.
    img = _img_lower_filled((10, 14, 39))  # #0a0e27 navy
    warns = contrast_warnings(img, _FMT, _BRAND_DARK, layout="photo-poster",
                              content=_CONTENT)
    assert warns == []


# === EARS-3: schlechter Kontrast -> Warnung (Region + Wert) ===================
def test_bad_contrast_warns_with_region_and_value():
    # Heller Ink (#faf7f2) auf hellem Cream-Untergrund -> schlecht lesbar.
    img = _img_lower_filled((239, 231, 214))  # #efe7d6 cream
    warns = contrast_warnings(img, _FMT, _BRAND_DARK, layout="photo-poster",
                              content=_CONTENT)
    assert warns, "heller Text auf hellem BG muss eine Kontrast-Warnung ausloesen"
    blob = " ".join(warns).lower()
    assert "kontrast-warnung" in blob
    assert "headline" in blob            # Region benannt
    assert ":1" in blob                  # gemessener Ratio-Wert
    # Warnung, NICHT Blockade: reine Strings, keine Exception (impliziert durch Rueckkehr).


def test_bad_contrast_findings_flag_not_ok():
    img = _img_lower_filled((239, 231, 214))
    findings = check_contrast(img, _FMT, _BRAND_DARK, layout="photo-poster",
                              content=_CONTENT)
    headline = next(f for f in findings if f.name == "headline")
    assert not headline.ok
    assert headline.worst_ratio < WCAG_AA_LARGE
    assert headline.min_ratio == WCAG_AA_LARGE   # Headline = grosser Text


# === EARS-4: Foto-BG -> Fix-Empfehlung ========================================
def test_recommend_fix_photo_bg_suggests_scrim():
    img = _img_lower_filled((239, 231, 214))
    findings = check_contrast(img, _FMT, _BRAND_DARK, layout="object-hero",
                              content=_CONTENT)
    recs = recommend_contrast_fix(findings, has_bg_image=True, layout="object-hero")
    assert recs
    blob = " ".join(recs).lower()
    assert "scrim" in blob or "panel" in blob


def test_recommend_fix_empty_when_all_ok():
    img = _img_lower_filled((10, 14, 39))
    findings = check_contrast(img, _FMT, _BRAND_DARK, layout="photo-poster",
                              content=_CONTENT)
    assert recommend_contrast_fix(findings, has_bg_image=True) == []


# === EARS-5: projektneutral + Content-Filter ==================================
def test_regions_use_param_colors_no_hardcode():
    brand = {"BRAND_INK": "#123456", "BRAND_INK_MUTED": "#222222",
             "BRAND_ACCENT": "#abcdef"}
    regs = text_regions(_FMT, brand, layout="template", content=_CONTENT)
    headline = next(r for r in regs if r.name == "headline")
    assert headline.fg == (0x12, 0x34, 0x56)   # kommt aus dem Parameter, nicht hardcodiert


def test_empty_subline_yields_no_subline_region():
    content = AdContent(headline="Nur Headline")   # keine Subline/CTA/Eyebrow
    names = {r.name for r in text_regions(_FMT, _BRAND_DARK, content=content)}
    assert "headline" in names
    assert "subline" not in names
    assert "cta" not in names


def test_check_contrast_accepts_png_path(tmp_path):
    img = _img_lower_filled((239, 231, 214))
    p = tmp_path / "creative__feed_4x5.png"
    img.save(p)
    warns = contrast_warnings(str(p), _FMT, _BRAND_DARK, layout="photo-poster",
                              content=_CONTENT)
    assert warns  # gleiche Warnung auch ueber den Dateipfad
