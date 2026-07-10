"""Tests fuer SKILL-029 (brand.json als Token-Rollen + Logo-Handling).

Deckt die EARS-Kriterien ab:
  EARS-1: brand.json laedt Token-Rollen (bg/accent/ink/font) + Logo-Pfad/Position/Hoehe.
  EARS-2: gesetztes Logo erscheint safe-zone-korrekt im gerenderten HTML (build_html-Output).
  EARS-3: brand.json ergaenzt/ueberschreibt branding.env -> klare Praezedenz, kein Misch-Zustand.
  EARS-4: fehlende Logo-Datei / unbekannte Position -> Warnung (kein stiller Fallback ohne Hinweis).
  EARS-5: alles aus Parametern (tmp_path) -> kein hartkodierter Brand-/Logo-Wert.

HTML-String-Assertions reichen — kein Playwright-Render noetig (testet build_html).
Regression: branding.env-Weg + render()-Signatur bleiben intakt.
"""
from __future__ import annotations

import json

from creative_studio.render_image import (
    load_branding,
    load_brand_json,
    resolve_brand,
    build_html,
    _BRAND_DEFAULTS,
    _LOGO_DEFAULTS,
)
from creative_studio.specs import AdContent, get_format


# --- Helfer ------------------------------------------------------------------

def _write_json(tmp_path, data) -> str:
    p = tmp_path / "brand.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return str(p)


def _write_env(tmp_path, text) -> str:
    p = tmp_path / "branding.env"
    p.write_text(text, encoding="utf-8")
    return str(p)


def _content():
    return AdContent(headline="Hallo Welt", cta="Mehr erfahren", ad_id="t029")


# --- EARS-1: brand.json laedt Token-Rollen + Logo ----------------------------

def test_ears1_brand_json_laedt_token_rollen(tmp_path):
    path = _write_json(tmp_path, {
        "brand_name": "Marke X",
        "colors": {"bg": "#111111", "accent": "#22ff22", "ink": "#ffffff"},
        "font": "Georgia, serif",
    })
    vals = load_brand_json(path)
    assert vals["BRAND_NAME"] == "Marke X"
    assert vals["BRAND_BG"] == "#111111"
    assert vals["BRAND_ACCENT"] == "#22ff22"
    assert vals["BRAND_INK"] == "#ffffff"
    assert vals["BRAND_FONT"] == "Georgia, serif"


def test_ears1_brand_json_laedt_logo_rolle(tmp_path):
    logo = tmp_path / "logo.png"
    logo.write_bytes(b"\x89PNG\r\n")  # Datei muss existieren (sonst Warnung)
    path = _write_json(tmp_path, {
        "logo": {"path": str(logo), "position": "top-right", "height_pct": 8.5}
    })
    vals = load_brand_json(path)
    assert vals["LOGO_PATH"] == str(logo)
    assert vals["LOGO_POSITION"] == "top-right"
    assert vals["LOGO_HEIGHT_PCT"] == "8.5"


def test_ears1_flache_top_level_keys_akzeptiert(tmp_path):
    """Convenience: bg/accent flach am Top-Level (ohne 'colors')."""
    path = _write_json(tmp_path, {"bg": "#abcdef", "logo_path": "x", "logo_position": "top-center"})
    vals = load_brand_json(path)
    assert vals["BRAND_BG"] == "#abcdef"
    assert vals["LOGO_POSITION"] == "top-center"


# --- EARS-3: Praezedenz brand.json > branding.env > Defaults ------------------

def test_ears3_brand_json_ueberschreibt_branding_env(tmp_path):
    env = _write_env(tmp_path, 'BRAND_BG="#000000"\nBRAND_ACCENT="#ff0000"\nBRAND_INK="#eeeeee"\n')
    j = _write_json(tmp_path, {"colors": {"accent": "#00ff00"}})
    brand = resolve_brand(brand_env=env, brand_json=j)
    # brand.json gewinnt fuer accent ...
    assert brand["BRAND_ACCENT"] == "#00ff00"
    # ... branding.env bleibt fuer nicht ueberschriebene Keys erhalten ...
    assert brand["BRAND_BG"] == "#000000"
    assert brand["BRAND_INK"] == "#eeeeee"


def test_ears3_overrides_haben_hoechste_prioritaet(tmp_path):
    j = _write_json(tmp_path, {"brand_name": "Aus JSON"})
    brand = resolve_brand(brand_json=j, overrides={"BRAND_NAME": "CLI Override"})
    assert brand["BRAND_NAME"] == "CLI Override"


def test_ears3_defaults_wenn_nichts_gesetzt():
    brand = resolve_brand()
    assert brand["BRAND_BG"] == _BRAND_DEFAULTS["BRAND_BG"]
    assert brand["LOGO_POSITION"] == _LOGO_DEFAULTS["LOGO_POSITION"]
    assert brand["LOGO_PATH"] == ""


# --- EARS-4: Validierung / Warnungen -----------------------------------------

def test_ears4_fehlende_logo_datei_warnt(tmp_path):
    warns = []
    path = _write_json(tmp_path, {"logo": {"path": "C:/gibt/es/nicht/logo.png"}})
    load_brand_json(path, warn=warns.append)
    assert any("nicht gefunden" in w.lower() for w in warns)


def test_ears4_unbekannte_position_warnt_und_faellt_zurueck(tmp_path):
    warns = []
    path = _write_json(tmp_path, {"logo": {"path": "x", "position": "mitte-unten"}})
    vals = load_brand_json(path, warn=warns.append)
    assert any("position" in w.lower() for w in warns)
    assert vals["LOGO_POSITION"] == _LOGO_DEFAULTS["LOGO_POSITION"]


def test_ears4_fehlende_brand_json_warnt(tmp_path):
    warns = []
    load_brand_json(str(tmp_path / "fehlt.json"), warn=warns.append)
    assert any("nicht gefunden" in w.lower() for w in warns)


# --- EARS-2: Logo-Markup im gerenderten HTML ---------------------------------

def test_ears2_logo_markup_erscheint_wenn_gesetzt(tmp_path):
    logo = tmp_path / "logo.png"
    logo.write_bytes(b"\x89PNG\r\n")
    brand = resolve_brand(brand_json={"LOGO_PATH": str(logo), "LOGO_POSITION": "top-right",
                                      "LOGO_HEIGHT_PCT": "7.0", "BRAND_NAME": "Marke"})
    html = build_html(_content(), get_format("feed_4x5"), brand)
    assert 'class="logo"' in html
    # SKILL-029: lokales Logo wird als data-URI eingebettet (laedt unter about:blank-Basis)
    assert "data:image/png;base64," in html
    # safe-zone-korrekt: Logo nutzt --safe-top + safe-x-Anker
    assert "top: var(--safe-top)" in html
    assert "right: var(--safe-x)" in html  # top-right -> rechte Safe-Zone


def test_ears2_kein_logo_markup_ohne_logo():
    brand = resolve_brand(overrides={"BRAND_NAME": "Nur Text"})
    html = build_html(_content(), get_format("feed_4x5"), brand)
    assert 'class="logo"' not in html
    # Fallback auf brand_name-Text bleibt
    assert "Nur Text" in html
    assert 'class="brand"' in html


def test_ears2_fehlende_logo_datei_kein_markup(tmp_path):
    """Logo gesetzt, Datei fehlt -> kein <img> (keine kaputte Referenz), brand_name-Text greift."""
    brand = resolve_brand(brand_json={"LOGO_PATH": "C:/fehlt/logo.png"},
                          overrides={"BRAND_NAME": "Fallback"})
    html = build_html(_content(), get_format("feed_4x5"), brand)
    assert 'class="logo"' not in html
    assert "Fallback" in html


# --- Regression: branding.env-Weg + render()-Signatur intakt -----------------

def test_regression_branding_env_weg_intakt(tmp_path):
    """load_branding() liefert weiterhin alle BRAND_*-Keys aus branding.env."""
    env = _write_env(tmp_path, 'BRAND_NAME="Alt"\nBRAND_BG="#123456"\n')
    vals = load_branding(env)
    assert vals["BRAND_NAME"] == "Alt"
    assert vals["BRAND_BG"] == "#123456"
    # nicht gesetzte Keys bleiben Default
    assert vals["BRAND_ACCENT"] == _BRAND_DEFAULTS["BRAND_ACCENT"]


def test_regression_build_html_mit_load_branding_dict(tmp_path):
    """Alter Weg: load_branding() -> build_html() funktioniert unveraendert (kein Logo)."""
    env = _write_env(tmp_path, 'BRAND_NAME="Klassisch"\nBRAND_ACCENT="#abc123"\n')
    brand = load_branding(env)  # KEINE LOGO_*-Keys drin
    html = build_html(_content(), get_format("story_9x16"), brand)
    assert "Klassisch" in html
    assert "#abc123" in html
    assert 'class="logo"' not in html  # ohne Logo-Keys -> kein Logo-Markup
