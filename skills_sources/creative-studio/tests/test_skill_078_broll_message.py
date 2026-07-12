"""SKILL-078 — Tests fuer das broll_message-Format + zentrale Reel-Brand.

1 EARS = mind. 1 Test. Deckt:
  A) broll_message-Validierung (hook/message Pflicht) + Props-Mapping (contentType,
     textBox, message, messageScenes) + Composition-Auswahl.
  B) zentrale Brand-Aufloesung (resolve_central_reel_brand) + Override-Praezedenz
     (Spec-brand > zentrale brand.json/branding.env > Defaults).
"""
from __future__ import annotations

import json
import pathlib

import pytest

from creative_studio.reel_spec import (
    BROLL_MESSAGE,
    ReelSpecError,
    load_reel_spec,
    parse_reel_spec,
    reel_spec_to_props,
    resolve_central_reel_brand,
)

_EXAMPLE = (
    pathlib.Path(__file__).resolve().parent.parent
    / "examples"
    / "reel_broll_message.json"
)


def _broll_message_dict() -> dict:
    return {
        "ad_id": "bm-1",
        "content_type": "broll_message",
        "hook": "Die meisten arbeiten noch von Hand.",
        "message": "Ein Agent erledigt den Rest.",
        "broll": [{"src": "clip1.mp4", "seconds": 6.0}],
        "brand": {"name": "JAKSE-Automations", "accent": "#f25d3e"},
    }


# === Aufgabe A: Format broll_message =========================================

# EARS-A1: gueltige broll_message-Spec -> Props inkl. contentType + message + textBox.
def test_broll_message_props_mapping():
    spec = parse_reel_spec(_broll_message_dict())
    props = reel_spec_to_props(spec)
    assert props["contentType"] == BROLL_MESSAGE
    assert props["hookText"] == "Die meisten arbeiten noch von Hand."
    assert props["message"] == "Ein Agent erledigt den Rest."
    # text_box default "auto" -> konservativ Box-AN (bool im Props-Objekt).
    assert props["textBox"] is True
    # B-Roll wird als Hintergrund-Layer durchgereicht.
    assert props["broll"] == [{"src": "clip1.mp4", "seconds": 6.0}]
    # Composition-Auswahl ueber content_type.
    assert spec.composition_id == "BrollMessage"


# EARS-A1b: broll_message `font`-Prop = brand.font (editorial Serif), NICHT der
# Caption-Font — auch wenn zentral ein captionFont gesetzt ist (kein Captions-Fall).
def test_broll_message_font_is_brand_font_not_caption():
    data = _broll_message_dict()
    data["brand"]["font"] = "Georgia, serif"
    data["brand"]["captionFont"] = "Montserrat, sans-serif"
    props = reel_spec_to_props(parse_reel_spec(data))
    assert props["font"] == "Georgia, serif"


# EARS-A2: fehlende message -> ReelSpecError (kein stilles textloses Reel).
def test_broll_message_missing_message_errors():
    data = _broll_message_dict()
    del data["message"]
    with pytest.raises(ReelSpecError):
        parse_reel_spec(data)


# EARS-A2b: fehlender hook -> ReelSpecError (hook bleibt Pflicht wie bisher).
def test_broll_message_missing_hook_errors():
    data = _broll_message_dict()
    del data["hook"]
    with pytest.raises(ReelSpecError):
        parse_reel_spec(data)


# EARS-A3: text_box-Flag wird durchgereicht (true/false/auto -> bool).
def test_broll_message_text_box_flag():
    for raw, expected in [(True, True), (False, False), ("auto", True), ("false", False)]:
        data = _broll_message_dict()
        data["text_box"] = raw
        props = reel_spec_to_props(parse_reel_spec(data))
        assert props["textBox"] is expected, f"text_box={raw!r}"


# EARS-A4: scenes -> zeitlich abgestufte Sub-Messages (messageScenes) im Props.
def test_broll_message_scenes_become_message_scenes():
    data = _broll_message_dict()
    data["scenes"] = [
        {"text": "Erst von Hand.", "seconds": 3.0},
        {"text": "Jetzt agentisch.", "seconds": 3.0},
    ]
    props = reel_spec_to_props(parse_reel_spec(data))
    assert props["messageScenes"] == [
        {"text": "Erst von Hand.", "seconds": 3.0},
        {"text": "Jetzt agentisch.", "seconds": 3.0},
    ]


# EARS-A5: talking_head/AdReel bleiben unberuehrt (nur broll_message erzwingt message).
def test_talking_head_does_not_require_message():
    data = {
        "ad_id": "th-1",
        "content_type": "talking_head",
        "hook": "Hook",
        "brand": {"name": "Marke"},
        "speaker": {"src": "s.mp4"},
    }
    spec = parse_reel_spec(data)  # kein message -> darf NICHT werfen
    assert spec.composition_id == "TalkingHead"
    # Default-Reel ohne content_type -> AdReel.
    plain = parse_reel_spec({"ad_id": "a", "hook": "h", "brand": {"name": "M"}})
    assert plain.composition_id == "AdReel"


# Beispiel-Spec laedt sauber.
def test_example_broll_message_loads():
    data = json.loads(_EXAMPLE.read_text(encoding="utf-8"))
    spec = parse_reel_spec(data)
    assert spec.content_type == BROLL_MESSAGE
    assert spec.message
    assert spec.composition_id == "BrollMessage"


# === Aufgabe B: zentrale Reel-Brand ==========================================

def _write_env(tmp_path, text) -> str:
    p = tmp_path / "branding.env"
    p.write_text(text, encoding="utf-8")
    return str(p)


# EARS-B1: zentrale branding.env liefert Reel-Tokens (name/accent/... + SKILL-057).
def test_central_brand_from_branding_env(tmp_path):
    env = _write_env(
        tmp_path,
        'BRAND_NAME="Zentrale Marke"\nBRAND_ACCENT="#123456"\nBRAND_BG="#000010"\n'
        'BRAND_HIGHLIGHT="#abcdef"\nBRAND_CAPTION_FONT="Montserrat, sans-serif"\n'
        'BRAND_CAPTION_BG_ALPHA="0.5"\n',
    )
    tokens = resolve_central_reel_brand(brand_env=env)
    assert tokens["name"] == "Zentrale Marke"
    assert tokens["accent"] == "#123456"
    assert tokens["bg"] == "#000010"
    # SKILL-057 Caption-Tokens aus derselben Datei.
    assert tokens["highlight"] == "#abcdef"
    assert tokens["captionFont"] == "Montserrat, sans-serif"
    assert tokens["captionBgAlpha"] == "0.5"


# EARS-B2: eine Brand-Datei aendern -> Reel folgt (kein Spec-brand-Block noetig).
def test_reel_follows_central_brand_without_spec_brand(tmp_path):
    env = _write_env(tmp_path, 'BRAND_NAME="Central"\nBRAND_ACCENT="#00ff00"\n')
    spec_file = tmp_path / "reel.json"
    spec_file.write_text(
        json.dumps({
            "ad_id": "bm",
            "content_type": "broll_message",
            "hook": "Hook oben",
            "message": "Message unten",
        }),
        encoding="utf-8",
    )
    spec = load_reel_spec(str(spec_file), brand_env=env)
    props = reel_spec_to_props(spec)
    assert props["brandName"] == "Central"
    assert props["accent"] == "#00ff00"


# EARS-B3: Praezedenz Spec-brand > zentrale Brand > Defaults.
def test_spec_brand_overrides_central(tmp_path):
    env = _write_env(tmp_path, 'BRAND_NAME="Central"\nBRAND_ACCENT="#00ff00"\nBRAND_BG="#010101"\n')
    central = resolve_central_reel_brand(brand_env=env)
    data = {
        "ad_id": "bm",
        "content_type": "broll_message",
        "hook": "H",
        "message": "M",
        "brand": {"accent": "#ff0000"},  # override NUR accent
    }
    spec = parse_reel_spec(data, central_brand=central)
    props = reel_spec_to_props(spec)
    # Spec gewinnt fuer accent ...
    assert props["accent"] == "#ff0000"
    # ... zentrale Brand bleibt fuer nicht-ueberschriebene Tokens (name/bg).
    assert props["brandName"] == "Central"
    assert props["bg"] == "#010101"


# EARS-B4: ohne Name (weder Spec noch zentral) -> ReelSpecError.
def test_missing_name_everywhere_errors():
    with pytest.raises(ReelSpecError):
        parse_reel_spec({"ad_id": "x", "hook": "h", "message": "m",
                         "content_type": "broll_message"}, central_brand={"accent": "#111"})
