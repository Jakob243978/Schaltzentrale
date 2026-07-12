"""SKILL-092 — Tests: Brand-Voice-Leitplanken (Playbook §2).

Companion zu compliance_warnings (legal): keine Tool-Namen, kein Preis, kein FOMO/
Angst, kein "Geschaeftsfuehrer", "individueller" statt "komplizierter". Reine
Warnungen. Projektneutral (generische Tool-Marken + Parameter fuer projekt-eigene).
"""
from __future__ import annotations

from creative_studio.specs import brand_voice_warnings, GENERIC_AI_TOOL_NAMES


def test_flags_generic_tool_name():
    assert any("Tool-Namen" in w for w in brand_voice_warnings("Gebaut mit ChatGPT und n8n"))


def test_flags_project_tool_via_parameter():
    w = brand_voice_warnings("Wir nutzen Coder dafuer", forbidden_tools=("Coder",))
    assert any("Tool-Namen" in x for x in w)


def test_flags_price():
    assert any("kein Preis" in w for w in brand_voice_warnings("Nur 990 EUR im Monat"))
    assert any("kein Preis" in w for w in brand_voice_warnings("Ab 49€ pro Nutzer"))


def test_price_can_be_disabled():
    assert not any("kein Preis" in w
                   for w in brand_voice_warnings("990 EUR", forbid_price=False))


def test_flags_geschaeftsfuehrer():
    assert any("Ansprache" in w for w in brand_voice_warnings("Als Geschaeftsfuehrer weisst du"))


def test_flags_kompliziert():
    assert any("individueller" in w for w in brand_voice_warnings("Das ist zu kompliziert"))


def test_flags_fomo():
    assert any("Motivation statt Angst" in w
               for w in brand_voice_warnings("Wer jetzt nicht handelt, wird abgehaengt"))


def test_clean_copy_no_brand_voice_warning():
    assert brand_voice_warnings("Routine an Agenten abgeben, mehr Zeit fuer dich") == []


def test_generic_tool_list_projektneutral():
    # allgemein bekannte Dritt-Produkte, kein Projekt-/Brand-eigener Wert.
    assert "chatgpt" in GENERIC_AI_TOOL_NAMES
    assert "jakob" not in GENERIC_AI_TOOL_NAMES
