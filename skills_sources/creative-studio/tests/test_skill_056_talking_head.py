"""SKILL-056 — Tests fuer die Talking-Head-Composition (TalkingHead.tsx + Spec).

Prueft (a) die Render-Garantien im TalkingHead.tsx-Quelltext (Speaker-Layer mit
O-Ton, optionale Captions, Lower-Third + Hook-Fenster, CTA-Outro, kein
hartkodierter Projektwert) und (b) das Spec->Props-Mapping (speaker/content_type)
sowie die content_type_warnings()-Andockung (kein Parallel-Validator).

1 EARS = mind. 1 Test.
"""
import pathlib

import pytest

from creative_studio.reel_spec import (
    ReelSpecError,
    parse_reel_spec,
    reel_spec_to_props,
)
from creative_studio.specs import CONTENT_TYPES, content_type_warnings

_VIDEO_SRC = pathlib.Path(__file__).resolve().parent.parent / "video" / "src"
_TH = (_VIDEO_SRC / "TalkingHead.tsx").read_text(encoding="utf-8")
_ROOT = (_VIDEO_SRC / "Root.tsx").read_text(encoding="utf-8")


def _spec_dict(**extra) -> dict:
    base = {
        "ad_id": "th-immo",
        "hook": "Wie ich 3 Stunden pro Woche zurueckgewinne",
        "content_type": "talking_head",
        "speaker": {"src": "speaker.mp4", "objectPosition": "50% 30%"},
        "brand": {"name": "JAKSE-Automations", "accent": "#f25d3e"},
    }
    base.update(extra)
    return base


# EARS-1: durchgaengiger Speaker-Layer (objectFit cover) + O-Ton (NICHT gemutet).
def test_talking_head_speaker_layer():
    assert "OffthreadVideo" in _TH
    assert 'objectFit: "cover"' in _TH
    # O-Ton: KEIN muted-Attribut am Speaker-OffthreadVideo.
    assert "muted" not in _TH
    assert "speakerObjectPosition" in _TH
    # Spec reicht speakerSrc/objectPosition als Props durch.
    spec = parse_reel_spec(_spec_dict())
    props = reel_spec_to_props(spec)
    assert props["speakerSrc"] == "speaker.mp4"
    assert props["speakerObjectPosition"] == "50% 30%"


# EARS-2: Captions optional — mit Track eingeblendet, ohne Track rendert es weiter.
def test_talking_head_captions():
    assert "<Captions" in _TH
    assert "captionBg" in _TH and "captionBgAlpha" in _TH


def test_talking_head_no_captions():
    # Captions-Komponente gibt bei null-Tokens null zurueck (Layer optional) ->
    # TalkingHead haengt nicht an einem Pflicht-Track.
    captions_src = (_VIDEO_SRC / "Captions.tsx").read_text(encoding="utf-8")
    assert "if (!tokens || tokens.length === 0) return null;" in captions_src
    # Spec ohne captions ist gueltig.
    spec = parse_reel_spec(_spec_dict())
    props = reel_spec_to_props(spec)
    assert props.get("captions") is None


# EARS-3: Lower-Third Safe-Zone-konform + Hook-Promise im Fenster < 3 s.
def test_talking_head_hook_window_and_lowerthird():
    assert "lowerThirdName" in _TH and "lowerThirdClaim" in _TH
    assert "hookWindowSeconds" in _TH
    assert "hookEndFrame" in _TH
    # Lower-Third sitzt ueber der unteren 35 %-Safe-Zone (padBottom-bezogen).
    assert "bottom: padBottom" in _TH
    # Default-Hook-Fenster = 3 s.
    assert "HOOK_WINDOW_DEFAULT = 3.0" in _TH


# EARS-4: CTA-Outro-Bumper am Ende (Brand-CTA).
def test_talking_head_cta_outro():
    assert "ctaOutro" in _TH
    assert "outroStart" in _TH
    assert "Sequence" in _TH


# EARS-5 [multi-projekt]: keine hartkodierten Projektwerte im TSX.
def test_talking_head_project_neutral():
    import re

    hexes = set(re.findall(r"#[0-9a-fA-F]{6}", _TH))
    assert not hexes, f"TalkingHead.tsx darf keine Brand-Hex-Literale halten: {hexes}"
    # Komposition ist in Root.tsx registriert.
    assert 'id="TalkingHead"' in _ROOT


# EARS-6: talking_head-CONTENT_TYPE-Validierung ueber content_type_warnings (kein Parallel-Validator).
def test_talking_head_content_type_validation():
    ct = CONTENT_TYPES["talking_head"]
    # In-Range (20-45 s) -> keine Laengen-Warnung.
    assert content_type_warnings(ct, seconds=30.0) == []
    # Zu kurz -> Warnung (gleicher Validator wie alle anderen Typen).
    warns = content_type_warnings(ct, seconds=8.0)
    assert any("Laengen-Warnung" in w for w in warns)


# Spec-Validierung: speaker ohne src -> klarer Fehler (kein stiller Leer-Layer).
def test_talking_head_speaker_requires_src():
    bad = _spec_dict(speaker={"objectPosition": "50% 50%"})
    with pytest.raises(ReelSpecError):
        parse_reel_spec(bad)
