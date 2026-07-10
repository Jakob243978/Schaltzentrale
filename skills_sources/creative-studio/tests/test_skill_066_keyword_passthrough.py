"""Tests fuer die keyword:true-Verdrahtung (SKILL-066).

content.py (SKILL-061) waehlt INHALTLICH ein Betonungs-Keyword pro Phrase und
setzt `keyword:true` auf dem Caption-Token. Bis SKILL-066 hat
`reel_spec.CaptionTokenSpec` dieses Feld GEDROPPT (nur text/startMs/endMs) — die
Highlights stammten dann aus der SKILL-055-Heuristik (laengstes/zahlhaltiges
Token), die nur zufaellig dieselben Woerter trifft. Diese Tests belegen: das
explizit gesetzte Keyword ueberlebt jetzt bis in die Remotion-Props; fehlt es,
faellt der Renderer auf die Heuristik zurueck (EARS-2, Bestand).
"""
from creative_studio import content as C
from creative_studio import reel_spec as RS


BRAND = {"name": "JAKSE-Automations", "accent": "#f25d3e", "bg": "#0a0e27"}


def _spec_with_keyword():
    """Spec mit einem editoriell gewaehlten Keyword auf einem KURZEN Wort, das
    die Heuristik NICHT waehlen wuerde (Laenge < 4, keine Zahl) — so trennt der
    Test die echte Betonung sauber von der Heuristik."""
    return {
        "ad_id": "kw-test",
        "hook": "Beleg",
        "captions": [
            {"text": "Wir", "startMs": 0, "endMs": 300, "keyword": True},  # kurz, editoriell
            {"text": "skalieren", "startMs": 300, "endMs": 900},           # laenger (Heuristik-Favorit)
        ],
        "brand": BRAND,
    }


def test_caption_token_spec_carries_keyword():
    """EARS-1/EARS-3: parse_reel_spec liest `keyword` und to_dict() reicht es durch."""
    spec = RS.parse_reel_spec(_spec_with_keyword())
    assert spec.captions[0].keyword is True
    assert spec.captions[1].keyword is False
    d0 = spec.captions[0].to_dict()
    d1 = spec.captions[1].to_dict()
    assert d0.get("keyword") is True            # markiertes Token traegt das Flag
    assert "keyword" not in d1                   # unmarkiertes Token bleibt schlank


def test_keyword_survives_into_props():
    """EARS-3: das editoriell gewaehlte Keyword landet in den Remotion-Props
    (vorher von CaptionTokenSpec gedroppt)."""
    spec = RS.parse_reel_spec(_spec_with_keyword())
    props = RS.reel_spec_to_props(spec)
    caps = props["captions"]
    flagged = [c["text"] for c in caps if c.get("keyword")]
    assert flagged == ["Wir"]   # die EDITORIELLE Wahl, NICHT das laengste "skalieren"


def test_no_keyword_falls_back_to_heuristic_shape():
    """EARS-2: ohne markiertes Keyword tragen die Props-Captions KEIN keyword-Feld
    -> Captions.tsx nutzt die Heuristik (Bestand, kein Zwang)."""
    spec = RS.parse_reel_spec(
        {
            "ad_id": "no-kw",
            "hook": "x",
            "captions": [
                {"text": "Drei", "startMs": 0, "endMs": 300},
                {"text": "Stunden", "startMs": 300, "endMs": 800},
            ],
            "brand": BRAND,
        }
    )
    props = RS.reel_spec_to_props(spec)
    assert all("keyword" not in c for c in props["captions"])


def test_content_pipeline_keyword_reaches_props_end_to_end():
    """End-to-End: content.decision_to_spec setzt keyword:true -> reel_spec reicht
    es bis in die Props durch (die ganze Kette SKILL-061 -> 066)."""
    transcript = {
        "language": "de",
        "full_text": "wir haben 16 Ferienwohnungen 150 Nachrichten",
        "words": [
            {"text": "wir", "startMs": 0, "endMs": 100, "p": 1.0},
            {"text": "haben", "startMs": 100, "endMs": 250, "p": 1.0},
            {"text": "16", "startMs": 250, "endMs": 400, "p": 0.9},
            {"text": "Ferienwohnungen", "startMs": 400, "endMs": 1400, "p": 0.8},
            {"text": "150", "startMs": 1600, "endMs": 1900, "p": 0.5},
            {"text": "Nachrichten", "startMs": 1900, "endMs": 2400, "p": 1.0},
        ],
    }
    dec = C.EditorialDecision(
        start_word=0, end_word=5, hook="150 Nachrichten", keyword_words=[3, 5]
    )
    spec_dict = C.decision_to_spec(transcript, dec, ad_id="e2e", brand=BRAND)
    spec = RS.parse_reel_spec(spec_dict)
    props = RS.reel_spec_to_props(spec)
    flagged = [c["text"] for c in props["captions"] if c.get("keyword")]
    assert flagged == ["Ferienwohnungen", "Nachrichten"]  # editoriell gewaehlt
