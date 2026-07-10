"""Tests fuer die Content-Analyse-Stufe (SKILL-061).

Die "Intelligenz" ist Claude (kein LLM-Call im Modul). Getestet wird die
Glue-Logik: Prompt-Bau, robuste Decision-Validierung und der Bau der
maschinellen Reel-Spec aus echtem Transkript + Decision — inkl. Caption-Nullung
und keyword:true-Markierung. Gegen Fixtures, ohne Live-LLM.
"""
import pytest

from creative_studio import content as C
from creative_studio import reel_spec as RS


# --- Fixture: ein realistisches (verkuerztes) Transkript --------------------
TRANSCRIPT = {
    "language": "de",
    "full_text": "Die meisten Gastgeber wissen gar nicht wie viele Nachrichten sie bekommen "
    "wir haben 16 Ferienwohnungen 150 Nachrichten",
    "word_count": 9,
    "words": [
        {"text": "Die", "startMs": 1800, "endMs": 2180, "p": 0.6},
        {"text": "meisten", "startMs": 2180, "endMs": 2560, "p": 1.0},
        {"text": "Gastgeber", "startMs": 2560, "endMs": 3100, "p": 0.9},
        {"text": "Nachrichten", "startMs": 3860, "endMs": 4180, "p": 1.0},
        {"text": "bekommen", "startMs": 4180, "endMs": 8020, "p": 1.0},
        {"text": "wir", "startMs": 10520, "endMs": 10580, "p": 1.0},
        {"text": "16", "startMs": 10680, "endMs": 10860, "p": 0.9},
        {"text": "Ferienwohnungen", "startMs": 10860, "endMs": 11940, "p": 0.8},
        {"text": "150", "startMs": 12420, "endMs": 12760, "p": 0.5},
    ],
}

BRAND = {"name": "JAKSE-Automations", "accent": "#f25d3e", "bg": "#0a0e27"}


def test_prompt_lists_real_words_with_index():
    """EARS-1: der Prompt enthaelt den Wort-Index aus dem echten Transkript."""
    p = C.build_analysis_prompt(TRANSCRIPT)
    assert "[0]" in p and "Gastgeber" in p and "Ferienwohnungen" in p
    assert "JSON" in p  # verlangt strukturierte Antwort


def test_parse_decision_from_fenced_json_string():
    """EARS-2: robustes Parsen von Claudes Antwort (auch ```json-Fence + Text drumherum)."""
    raw = (
        "Hier meine Wahl:\n```json\n"
        '{"segment":{"start_word":0,"end_word":8},"hook":"150 Nachrichten",'
        '"keyword_words":[3,7,8],"narrative":{"cta":"Auf die Warteliste"}}\n```\n'
    )
    dec = C.parse_editorial_decision(raw)
    assert dec.start_word == 0 and dec.end_word == 8
    assert dec.hook == "150 Nachrichten"
    assert dec.keyword_words == [3, 7, 8]
    assert dec.cta == "Auf die Warteliste"


def test_parse_decision_requires_hook_and_segment():
    """EARS-2: fehlender Hook/Segment -> ContentAnalysisError (kein Silent-Fake)."""
    with pytest.raises(C.ContentAnalysisError):
        C.parse_editorial_decision({"segment": {"start_word": 0, "end_word": 2}})  # kein hook
    with pytest.raises(C.ContentAnalysisError):
        C.parse_editorial_decision({"hook": "x"})  # kein segment


def test_decision_to_spec_captions_are_real_and_nulled():
    """EARS-3: Captions stammen AUS dem Segment des echten Transkripts und sind
    relativ auf 0 genullt; keyword:true sitzt auf den betonten Woertern."""
    dec = C.EditorialDecision(
        start_word=0, end_word=8, hook="150 Nachrichten.", keyword_words=[3, 7, 8]
    )
    spec = C.decision_to_spec(TRANSCRIPT, dec, ad_id="th-x", brand=BRAND)
    caps = spec["captions"]
    # echtes erstes Wort, auf 0 genullt
    assert caps[0]["text"] == "Die" and caps[0]["startMs"] == 0
    # Inhalt = echtes Wort, NICHT ein erfundener Slogan
    assert [c["text"] for c in caps][:3] == ["Die", "meisten", "Gastgeber"]
    # keyword:true auf den richtigen (segment-relativen) Indizes
    kw_idx = [i for i, c in enumerate(caps) if c.get("keyword")]
    assert kw_idx == [3, 7, 8]


def test_spec_is_reel_spec_loadable():
    """EARS-4: die maschinelle Spec ist von reel_spec.py (SKILL-045) ladbar +
    multi-projekt (Brand kommt als Parameter)."""
    dec = C.EditorialDecision(start_word=0, end_word=8, hook="150 Nachrichten.")
    spec = C.decision_to_spec(
        TRANSCRIPT, dec, ad_id="th-x", brand=BRAND, content_type="talking_head"
    )
    parsed = RS.parse_reel_spec(spec)
    assert parsed.ad_id == "th-x"
    assert parsed.hook == "150 Nachrichten."
    assert len(parsed.captions) == 9
    assert parsed.captions[0].text == "Die"


def test_decision_clamps_out_of_range_segment():
    """EARS-3: ausser-Range-Indizes werden geklemmt statt zu crashen."""
    dec = C.EditorialDecision(start_word=-5, end_word=999, hook="x")
    spec = C.decision_to_spec(TRANSCRIPT, dec, ad_id="t", brand=BRAND)
    assert len(spec["captions"]) == 9  # ganzer Bereich, geklemmt
