"""SKILL-090 — Tests: Projekt-VoC als Copy-Datenquelle + Human-Rule-Check im Flow.

Der Copy-Flow kann optional eine Projekt-Messaging-/VoC-Datei einlesen und ihre
Kundensprache in den Analyse-Prompt einspeisen; zusaetzlich laufen die Human-Rule-/
Brand-Voice-Warnungen im Copy-Vorpruef-Flow (Bild + Reel). Ohne Datei bleibt alles
unveraendert; fehlende Datei -> Fallback ohne Fehler; kein Projektwert hartkodiert.
"""
from __future__ import annotations

from creative_studio import content as C
from creative_studio.specs import AdContent


_TRANSCRIPT = {
    "full_text": "Das ueberschwemmt mich, ich koordiniere alles selbst.",
    "words": [
        {"startMs": 0, "endMs": 400, "text": "Das"},
        {"startMs": 400, "endMs": 900, "text": "ueberschwemmt"},
        {"startMs": 900, "endMs": 1200, "text": "mich"},
    ],
}


# --- EARS-1: VoC-Doc fliesst in build_analysis_prompt ------------------------
def test_messaging_doc_flows_into_prompt():
    doc = "Vokabular: en bloc, glattziehen, Zahllauf. O-Ton: 'das ueberschwemmt mich'."
    p = C.build_analysis_prompt(_TRANSCRIPT, messaging_doc=doc)
    assert "en bloc" in p
    assert "Kundensprache" in p or "VOICE OF CUSTOMER" in p
    assert "Consultant-Abstrakta" in p


def test_prompt_without_messaging_doc_unchanged():
    base = C.build_analysis_prompt(_TRANSCRIPT)
    assert "VOICE OF CUSTOMER" not in base


# --- EARS-1: load_messaging_doc liest Datei / graceful bei fehlen -------------
def test_load_messaging_doc_reads_file(tmp_path):
    f = tmp_path / "voc.md"
    f.write_text("Kundensprache: Zahllauf, Belegfreigabe.", encoding="utf-8")
    assert "Zahllauf" in C.load_messaging_doc(str(f))


def test_load_messaging_doc_missing_file_graceful():
    assert C.load_messaging_doc("/nonexistent/path/voc.md") == ""
    assert C.load_messaging_doc("") == ""
    assert C.load_messaging_doc(None) == ""


# --- EARS-2: Human-Rule-/Brand-Voice-Warnungen im Copy-Flow (Bild) -----------
def test_human_rule_warnings_in_image_flow_statistics():
    ad = AdContent(headline="93 Prozent der Betriebe verlieren Zeit")
    assert any("Statistik" in w for w in ad.warnings())


def test_brand_voice_warning_tool_name_in_image_flow():
    ad = AdContent(headline="Wir bauen dir das mit n8n und ChatGPT")
    assert any("Tool-Namen" in w for w in ad.warnings())


def test_category_term_in_image_flow():
    ad = AdContent(headline="Agentisches Arbeiten fuer dich",
                   category_term="agentisches Arbeiten")
    assert any("Begriff zuletzt" in w for w in ad.warnings())


# --- EARS-2: Human-Rule-Warnungen im Reel-Flow -------------------------------
def test_human_rule_warnings_in_reel_flow():
    spec = {
        "hook": "42 Prozent der Betriebe verlieren Zeit",
        "subline": "Ein System buendelt alles.",
        "cta": "Auf die Warteliste",
        "captions": [{"text": "Hallo", "startMs": 0, "endMs": 500}],
    }
    warns = C.content_structure_warnings(spec)
    assert any("Statistik" in w for w in warns)


def test_reel_forbidden_tools_from_spec():
    spec = {
        "hook": "150 Nachrichten pro Woche mit Coder gebaut",
        "subline": "Ein System buendelt alles.",
        "cta": "Auf die Warteliste",
        "forbidden_tools": ("Coder",),
        "captions": [{"text": "Hallo", "startMs": 0, "endMs": 500}],
    }
    assert any("Tool-Namen" in w for w in C.content_structure_warnings(spec))


# --- EARS-3: nicht-brechend / projektneutral ---------------------------------
def test_clean_copy_unchanged():
    ad = AdContent(headline="Routine an Agenten abgeben")
    assert ad.warnings() == []


def test_clean_reel_spec_unchanged():
    spec = {
        "hook": "150 Nachrichten pro Woche. So kommen wir hinterher.",
        "subline": "Ein System buendelt alle Gast-Nachrichten an einem Ort.",
        "cta": "Auf die Warteliste",
        "captions": [{"text": "w", "startMs": 0, "endMs": 20000}],
    }
    assert C.content_structure_warnings(spec) == []
