"""SKILL-055 — Tests fuer den Caption-Design-Overhaul (Captions.tsx + Plumbing).

Backend/Render-Surface: die Caption-Logik lebt in TSX (Remotion). Diese Tests
pruefen (a) die Code-Garantien im Captions.tsx-Quelltext (Pill/Stroke-Layer,
1-Keyword-Logik, <=2 aktive Tokens, Word-Reveal-Spring, Bold-Typo, kein
hartkodierter Brand-Hex) und (b) das Props-Durchreichen ueber reel_spec.py.

1 EARS = mind. 1 Test.
"""
import pathlib
import re

from creative_studio.reel_spec import load_reel_spec, reel_spec_to_props

_VIDEO_SRC = pathlib.Path(__file__).resolve().parent.parent / "video" / "src"
_CAPTIONS = (_VIDEO_SRC / "Captions.tsx").read_text(encoding="utf-8")
_ADREEL = (_VIDEO_SRC / "AdReel.tsx").read_text(encoding="utf-8")
_EXAMPLE = (
    pathlib.Path(__file__).resolve().parent.parent / "examples" / "reel_h1-immo.json"
)


# EARS-1: Kontrast-Layer — Pill (Default) ODER Stroke, nicht nur textShadow.
def test_caption_has_contrast_layer():
    # Pill-Hintergrund hinter der aktiven Caption-Zeile vorhanden.
    assert "usePill" in _CAPTIONS
    assert "borderRadius" in _CAPTIONS
    # Pill-Farbe wird aus Brand-BG + Alpha gebaut (rgba), nicht nur Shadow.
    assert "hexToRgba" in _CAPTIONS and "captionBgAlpha" in _CAPTIONS
    # Stroke-Alternative ueber -webkit-text-stroke (WebkitTextStroke) vorhanden.
    assert "WebkitTextStroke" in _CAPTIONS
    # CaptionBg-Typ kennt beide Looks.
    assert '"pill"' in _CAPTIONS and '"stroke"' in _CAPTIONS


# EARS-2: genau EIN Keyword pro Phrase (kuratiert/positions-basiert), nicht jedes >=6.
def test_single_keyword_highlight():
    # Alte "jedes Token >= 6 Zeichen"-Heuristik (isKeyword) ist entfernt.
    assert "isKeyword" not in _CAPTIONS
    # Neue 1-Keyword-Wahl je Phrase.
    assert "pickKeywordIndex" in _CAPTIONS
    assert "keywordIdx" in _CAPTIONS
    # explizite keyword:true-Markierung wird vorrangig genutzt.
    assert "keyword === true" in _CAPTIONS


# EARS-3: 1-2 aktive Tokens + Word-Reveal (Fade+Pop via spring).
def test_active_token_count_and_reveal():
    m = re.search(r"MAX_ACTIVE_TOKENS\s*=\s*(\d+)", _CAPTIONS)
    assert m and int(m.group(1)) <= 2, "MAX_ACTIVE_TOKENS muss <= 2 sein"
    m2 = re.search(r"MAX_LINE_CHARS\s*=\s*(\d+)", _CAPTIONS)
    assert m2 and int(m2.group(1)) <= 18, "MAX_LINE_CHARS muss <= 18 sein"
    # Word-Reveal via spring + per-Token-Startframe.
    assert "spring(" in _CAPTIONS
    assert "tokenStartFrame" in _CAPTIONS
    assert "revealOpacity" in _CAPTIONS


# EARS-4: Bold-Typo (Weight >= 800) + groessere Caption-Schrift.
def test_caption_typo_weight_and_size():
    # baseWeight fuer Highlight/Karaoke = 900 (>= 800).
    assert "baseWeight = style === \"clean\" ? 700 : 900" in _CAPTIONS
    # Aktiv-Wort ~9 %, Rest ~7,5 % Breite (klar ueber 48 px bei 1080 -> >= ~81 px).
    assert "activeFontSize = width * 0.092" in _CAPTIONS
    assert "baseFontSize = width * 0.078" in _CAPTIONS


# EARS-5 [multi-projekt]: keine hartkodierten Brand-Hex in der Komponente.
def test_caption_style_project_neutral():
    # KEIN #ffd400 (oder anderes Brand-Gelb) als Literal in Captions.tsx.
    assert "#ffd400" not in _CAPTIONS
    # Highlight/ink/accent kommen aus Props (Funktions-Signatur).
    assert "highlight," in _CAPTIONS and "accent," in _CAPTIONS
    # Es darf kein 6-stelliger Brand-Hex hartkodiert sein AUSSER der neutrale
    # Default-Pill-Grundton (DEFAULT_PILL_BG) — der ist explizit override-bar.
    hexes = set(re.findall(r"#[0-9a-fA-F]{6}", _CAPTIONS))
    assert hexes <= {"#0a0e27"}, f"Unerwartete Hex-Literale in Captions.tsx: {hexes}"


# EARS-1/5: AdReel reicht die neuen Caption-Style-Props (bg/captionBg/alpha) durch.
def test_adreel_passes_caption_style_props():
    assert "captionBg" in _ADREEL and "captionBgAlpha" in _ADREEL
    assert "bg={adProps.bg}" in _ADREEL


# Plumbing: reel_spec.py mappt die Caption-Style-Props (default Pill + Brand-Akzent).
def test_reel_spec_props_caption_style():
    spec = load_reel_spec(str(_EXAMPLE))
    props = reel_spec_to_props(spec)
    assert props["captionBg"] == "pill"
    assert abs(props["captionBgAlpha"] - 0.62) < 1e-9
