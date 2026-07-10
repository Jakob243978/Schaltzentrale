"""SKILL-072 — Tests fuer Layout-Archetypen + Themes + Stil-Parameter.

1 EARS = mind. 1 Test:
  - EARS-1: --layout stat-hero rendert den Hero; Default-Layout unveraendert (nicht-brechend).
  - EARS-2: theme light-cream ueberschreibt Flaeche/Ink, laesst den Akzent markeneigen.
  - EARS-3: chrome minimal schaltet Brand-Name/Top-Balken/CTA-Pill ab (CTA -> Text-Link).
  - EARS-4: layout_warnings warnt (keine Sperre) bei Hero-Scale ausserhalb Sweetspot,
            foto-getriebenem Layout ohne Bild und unbekanntem Layout.
  - EARS-5 [multi-projekt]: LAYOUTS/THEMES tragen keinen Projekt-/Brand-Wert.

Gerendert wird ueber build_html() (Jinja real), damit die Template-Pfade echt geprueft
sind — nicht nur String-Asserts. Kein Playwright noetig (schnell, headless-frei).
"""
from creative_studio.render_image import build_html, DEFAULT_STYLE
from creative_studio.specs import (
    AdContent, get_format,
    LAYOUTS, THEMES, apply_theme, layout_warnings,
    HERO_SCALE_SWEETSPOT, HERO_SCALE_DEFAULT,
)

_FMT = get_format("feed_4x5")

_BRAND = {
    "BRAND_BG": "#0a0e27", "BRAND_BG_SOFT": "#11163a", "BRAND_ACCENT": "#f25d3e",
    "BRAND_INK": "#faf7f2", "BRAND_INK_MUTED": "#9a9ec0",
    "BRAND_FONT": "sans-serif", "BRAND_NAME": "JAKSE-Automations",
    "LOGO_PATH": "", "LOGO_POSITION": "top-left", "LOGO_HEIGHT_PCT": "6.0",
}

_CONTENT = AdContent(
    headline="Verdoppeln", subline="Ohne doppeltes Team.",
    cta="Auf die Warteliste", eyebrow="MENTORING", brand_name="JAKSE-Automations",
)


def _html(style=None, brand=None, content=None):
    return build_html(content or _CONTENT, _FMT, brand or _BRAND, style=style)


# --- Nicht-Brechung: Default == kein style == DEFAULT_STYLE ---------------------

def test_default_render_unchanged_without_style():
    """Ohne style-Arg identisch zu explizitem DEFAULT_STYLE (Bestandsverhalten)."""
    assert _html(style=None) == _html(style=dict(DEFAULT_STYLE))


def test_default_layout_has_no_hero_element():
    html = _html(style=None)
    assert 'class="hero"' not in html          # kein Stat-Hero im Default
    assert 'class="safe"' in html              # Bestands-Safe-Block
    assert 'class="accent-bar"' in html        # Top-Balken (chrome full)
    assert 'class="brand"' in html             # Brand-Name (chrome full)
    assert 'class="cta"' in html               # CTA-Pill (chrome full)


def test_default_headline_weight_and_case_are_classic():
    html = _html(style=None)
    assert "font-weight: 800" in html          # bold-Default
    assert "text-transform: none" in html      # mixed-Default (kein ALL-CAPS)


# --- EARS-1: stat-hero rendert den Hero ----------------------------------------

def test_stat_hero_renders_hero_token():
    html = _html(style={"layout": "stat-hero", "hero_token": "93 %"})
    assert 'class="hero"' in html
    assert ">93 %<" in html
    assert 'class="safe safe-hero"' in html
    assert 'class="hero-icon"' in html         # Editorial-Pfeil-Icon


def test_stat_hero_falls_back_to_headline_without_token():
    html = _html(style={"layout": "stat-hero"})
    assert 'class="hero"' in html
    assert ">Verdoppeln<" in html              # Headline als Hero


# --- EARS-2: theme light-cream ueberschreibt Flaeche/Ink, Akzent bleibt --------

def test_apply_theme_light_cream_keeps_accent():
    themed = apply_theme(_BRAND, "light-cream")
    assert themed["BRAND_BG"] != _BRAND["BRAND_BG"]          # Flaeche geaendert
    assert themed["BRAND_INK"] != _BRAND["BRAND_INK"]        # Ink geaendert
    assert themed["BRAND_ACCENT"] == _BRAND["BRAND_ACCENT"]  # Akzent markeneigen


def test_apply_theme_dark_is_noop():
    assert apply_theme(_BRAND, "dark") == _BRAND


def test_theme_reaches_template_css():
    themed = apply_theme(_BRAND, "light-cream")
    html = _html(brand=themed)
    assert "#efe7d6" in html                   # Cream-BG im :root
    assert "#f25d3e" in html                    # Akzent unveraendert


# --- EARS-3: chrome minimal schaltet Ad-Chrome ab ------------------------------

def test_chrome_minimal_drops_brand_bar_pill():
    html = _html(style={"chrome": "minimal"})
    assert 'class="accent-bar"' not in html
    assert 'class="brand"' not in html
    assert 'class="cta"' not in html           # keine Pill ...
    assert 'class="cta-link"' in html          # ... sondern Text-Link


def test_chrome_full_is_default():
    html = _html(style={"chrome": "full"})
    assert 'class="accent-bar"' in html
    assert 'class="cta"' in html


# --- EARS-4: layout_warnings (keine Sperre) ------------------------------------

def test_warn_hero_scale_outside_sweetspot():
    lo, hi = HERO_SCALE_SWEETSPOT
    warns = layout_warnings("stat-hero", hero_scale=hi + 0.1)
    assert any("hero-scale" in w.lower() for w in warns)


def test_no_warn_hero_scale_in_sweetspot():
    warns = layout_warnings("stat-hero", hero_scale=HERO_SCALE_DEFAULT)
    assert not any("hero-scale" in w.lower() for w in warns)


def test_warn_photo_poster_without_bg_image():
    warns = layout_warnings("photo-poster", has_bg_image=False)
    assert any("bild-warnung" in w.lower() for w in warns)
    assert layout_warnings("photo-poster", has_bg_image=True) == []


def test_warn_unknown_layout():
    warns = layout_warnings("does-not-exist")
    assert any("unbekanntes layout" in w.lower() for w in warns)


# --- EARS-5: LAYOUTS/THEMES projektneutral -------------------------------------

def test_catalog_is_project_neutral():
    blob = " ".join(
        [l.key + l.name + l.description + l.note for l in LAYOUTS.values()]
        + [t.key + t.name + t.note + "".join(t.overrides.values()) for t in THEMES.values()]
    ).lower()
    for forbidden in ("immo", "jakob", "jakse", "mentoring", "warteliste"):
        assert forbidden not in blob


def test_expected_layouts_and_themes_present():
    assert set(LAYOUTS) >= {"template", "stat-hero", "photo-poster", "object-hero", "split-compare"}
    assert set(THEMES) >= {"dark", "light-cream"}
