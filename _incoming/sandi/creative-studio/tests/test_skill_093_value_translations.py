"""SKILL-093 — Tests: Value-Translations (Feature -> gefuehltes Leben).

Projektneutrale Muster-Funktion: uebersetzt Feature-Sprache in ein fuehlbares
Ergebnis. Die konkreten Paare sind Projekt-Daten (Parameter), der Mechanismus +
der Katalog der Feature-Level-Signalverben sind projektneutral.
"""
from __future__ import annotations

from creative_studio.frameworks import apply_value_translations, FEATURE_LEVEL_VERBS


def test_applies_translation_pair():
    translations = {"Agent fuehrt Prozesse aus": "Dein Betrieb laeuft, waehrend du weg bist"}
    out = apply_value_translations("Der Agent fuehrt Prozesse aus.", translations)
    assert "Dein Betrieb laeuft" in out
    assert "fuehrt Prozesse aus" not in out


def test_case_insensitive():
    out = apply_value_translations("RAHMEN abstecken", {"rahmen abstecken": "das Daran-Denken liegt im Prozess"})
    assert "Daran-Denken" in out


def test_longer_key_wins():
    translations = {"Prozesse": "Ablaeufe", "Prozesse ausfuehren": "alles laeuft von selbst"}
    out = apply_value_translations("Prozesse ausfuehren", translations)
    assert out == "alles laeuft von selbst"


def test_empty_mapping_is_noop():
    assert apply_value_translations("unveraendert", {}) == "unveraendert"
    assert apply_value_translations("", {"x": "y"}) == ""


def test_feature_verbs_catalog_projektneutral():
    assert "automatisiert" in FEATURE_LEVEL_VERBS
    for verb in FEATURE_LEVEL_VERBS:
        assert "jakob" not in verb.lower()
