"""SKILL-045 — Tests fuer den Reel-Spec-Loader (creative_studio/reel_spec.py).

1 EARS = mind. 1 Test.
"""
import json
import pathlib

import pytest

from creative_studio.reel_spec import (
    ReelSpecError,
    load_reel_spec,
    parse_reel_spec,
    reel_spec_to_props,
)
from creative_studio.specs import make_utm_content, make_variant_id

_EXAMPLE = (
    pathlib.Path(__file__).resolve().parent.parent / "examples" / "reel_h1-immo.json"
)


def _minimal_spec_dict() -> dict:
    return {
        "ad_id": "h1-immo",
        "hook": "3 Stunden zurück",
        "brand": {"name": "JAKSE-Automations", "accent": "#f25d3e"},
    }


# EARS-1: gueltige Spec -> --props-Objekt (Hook, Brand, CTA, Captions-Ref, Musik-Ref).
def test_reel_spec_to_props():
    spec = load_reel_spec(str(_EXAMPLE))
    props = reel_spec_to_props(spec)
    assert props["headline"] == "3 Stunden pro Woche zurück"
    assert props["headlineAccent"] == "ohne neues Tool"
    assert props["cta"] == "Auf die Warteliste"
    assert props["brandName"] == "JAKSE-Automations"
    assert props["accent"] == "#f25d3e"
    # Caption-Ref vorhanden + word-level Struktur korrekt durchgereicht
    assert props["captions"] and props["captions"][0] == {
        "text": "3",
        "startMs": 0,
        "endMs": 350,
    }
    assert props["captionStyle"] == "hormozi"
    # SKILL-057: Highlight ohne expliziten Brand-Wert faellt auf den Brand-Akzent
    # zurueck (NICHT mehr festes Gelb #ffd400) — Jakob-Vorgabe 2026-06-25.
    assert props["captionHighlight"] == "#f25d3e"
    # dynamische Dauer aus Szenen (1.5 + 1.5 = 3 s -> 90 Frames @ 30 fps)
    assert props["durationInFrames"] == 90


# EARS-2: Pflichtfeld fehlt -> klare Fehlermeldung statt stilles leeres Reel.
def test_reel_spec_missing_required():
    for missing in ("ad_id", "hook", "brand"):
        data = _minimal_spec_dict()
        del data[missing]
        with pytest.raises(ReelSpecError):
            parse_reel_spec(data)
    # brand ohne name -> ebenfalls Fehler
    bad = _minimal_spec_dict()
    bad["brand"] = {"accent": "#000"}
    with pytest.raises(ReelSpecError):
        parse_reel_spec(bad)


# EARS-3: optionale Layer (captions/broll/voiceover/music) -> Reel rendert trotzdem.
def test_reel_spec_optional_layers():
    spec = parse_reel_spec(_minimal_spec_dict())
    props = reel_spec_to_props(spec)
    assert props["captions"] is None
    assert props["voiceoverSrc"] is None
    assert props["musicSrc"] is None
    # ohne Szenen/Captions keine fixe Dauer -> Composition leitet sie selbst ab
    assert "durationInFrames" not in props
    # Pflicht-Inhalt ist trotzdem da
    assert props["headline"] == "3 Stunden zurück"
    assert props["brandName"] == "JAKSE-Automations"


# EARS-4 [multi-projekt]: Brand + Inhalt kommen NUR aus der Spec, kein Projektwert.
def test_reel_spec_project_neutral():
    data_a = _minimal_spec_dict()
    data_a["ad_id"] = "projektA"
    data_a["brand"] = {"name": "Marke A", "accent": "#111111", "bg": "#222222"}
    data_b = _minimal_spec_dict()
    data_b["ad_id"] = "projektB"
    data_b["brand"] = {"name": "Marke B", "accent": "#aaaaaa", "bg": "#bbbbbb"}

    props_a = reel_spec_to_props(parse_reel_spec(data_a))
    props_b = reel_spec_to_props(parse_reel_spec(data_b))

    assert props_a["brandName"] == "Marke A"
    assert props_a["accent"] == "#111111"
    assert props_b["brandName"] == "Marke B"
    assert props_b["accent"] == "#aaaaaa"
    assert props_a["variantId"] != props_b["variantId"]


# EARS-5: Naming nutzt SKILL-024 (variant_id/utm_content) — kein Parallel-Schema.
def test_reel_spec_naming_single_source():
    spec = parse_reel_spec(_minimal_spec_dict())
    expected_vid = make_variant_id(
        "h1-immo", "3 Stunden zurück", "hook", "story_9x16", hook_index=0
    )
    assert spec.variant_id == expected_vid
    assert spec.utm_content == make_utm_content(expected_vid)
    props = reel_spec_to_props(spec)
    assert props["variantId"] == expected_vid
    assert props["utmContent"] == make_utm_content(expected_vid)


# Zusatz: Loader liest die ausgelieferte Beispiel-Spec sauber ein.
def test_example_spec_is_valid_json_and_loads():
    data = json.loads(_EXAMPLE.read_text(encoding="utf-8"))
    spec = parse_reel_spec(data)
    assert spec.ad_id == "h1-immo"
    assert len(spec.captions) == 8
