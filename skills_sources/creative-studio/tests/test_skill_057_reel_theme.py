"""SKILL-057 — Tests fuer das Reel-Theme-/Design-Token-System.

Prueft, dass der Reel-Look (Caption-Highlight, Caption-Font, Caption-BG-Alpha)
aus EINER Brand-Quelle zieht — kein #ffd400-/Stil-Literal mehr in Root.tsx/
Captions.tsx; Defaults aus benannten Konstanten; Spec-Brand-Block ueberschreibt;
Skill bleibt projektneutral. branding.env-Andockung (AgentischesArbeiten-Instanz).

1 EARS = mind. 1 Test.
"""
import pathlib

from creative_studio.reel_spec import parse_reel_spec, reel_spec_to_props

_VIDEO_SRC = pathlib.Path(__file__).resolve().parent.parent / "video" / "src"
_ROOT = (_VIDEO_SRC / "Root.tsx").read_text(encoding="utf-8")
_CAPTIONS = (_VIDEO_SRC / "Captions.tsx").read_text(encoding="utf-8")

# branding.env liegt im AgentischesArbeiten-Repo (Schwester-Pfad). Best-effort:
# nur pruefen, wenn vorhanden (Skill bleibt projektneutral lauffaehig).
_BRANDING_ENV = pathlib.Path(
    "C:/claude_projekte/AgentischesArbeiten/terraform/base-dev/build/customization/branding.env"
)


def _spec(**brand) -> dict:
    b = {"name": "JAKSE-Automations", "accent": "#f25d3e"}
    b.update(brand)
    return {"ad_id": "h1-immo", "hook": "3 Stunden zurueck", "brand": b}


# EARS-1: kein #ffd400-/Stil-Literal mehr in Root.tsx / Captions.tsx.
def test_reel_theme_tokens_no_hardcode():
    assert "#ffd400" not in _ROOT
    assert "#ffd400" not in _CAPTIONS
    # Default-Highlight kommt aus benannter Konstante (= Brand-Akzent), kein Inline-Gelb.
    assert "CAPTION_HIGHLIGHT_DEFAULT = BRAND_ACCENT_DEFAULT" in _ROOT
    assert "CAPTION_FONT_DEFAULT" in _ROOT


# EARS-2: branding.env enthaelt die neuen Reel-Tokens (additiv).
def test_branding_env_has_reel_tokens():
    if not _BRANDING_ENV.exists():
        # Skill projektneutral: ohne das Projekt-Repo ist dieser Check n/a.
        import pytest

        pytest.skip("branding.env (AgentischesArbeiten) nicht vorhanden")
    txt = _BRANDING_ENV.read_text(encoding="utf-8")
    assert "BRAND_HIGHLIGHT=" in txt
    assert "BRAND_CAPTION_FONT=" in txt
    assert "BRAND_CAPTION_BG_ALPHA=" in txt
    # bestehende Variablen unveraendert vorhanden (additiv, nichts ueberschrieben).
    assert 'BRAND_ACCENT="#f25d3e"' in txt
    assert 'BRAND_WARN="#ffc857"' in txt


# EARS-3: Spec-Brand-Block ueberschreibt die Defaults (Override).
def test_reel_theme_spec_override():
    spec = parse_reel_spec(
        _spec(highlight="#00ff99", captionFont="Inter, sans-serif", captionBgAlpha=0.5, captionBg="stroke")
    )
    props = reel_spec_to_props(spec)
    assert props["captionHighlight"] == "#00ff99"
    assert props["font"] == "Inter, sans-serif"
    assert abs(props["captionBgAlpha"] - 0.5) < 1e-9
    assert props["captionBg"] == "stroke"


# EARS-3b: ohne Override faellt Highlight auf den Brand-Akzent (NICHT festes Gelb).
def test_reel_theme_highlight_defaults_to_accent():
    spec = parse_reel_spec(_spec(accent="#123456"))
    props = reel_spec_to_props(spec)
    assert props["captionHighlight"] == "#123456"


# EARS-4 [multi-projekt]: keine AgentischesArbeiten-spezifischen Hex/Fonts im Skill-Code.
def test_reel_theme_project_neutral():
    # Caption-Font-Default ist generisch (Montserrat + System-Fallback), kein Projektwert.
    assert "Montserrat" in _ROOT
    # Default-Highlight ist an den (ueberschreibbaren) Brand-Akzent gekoppelt,
    # nicht an einen projektspezifischen Sonderwert.
    spec = parse_reel_spec(_spec(name="Anderes Projekt", accent="#abcdef"))
    props = reel_spec_to_props(spec)
    assert props["captionHighlight"] == "#abcdef"
