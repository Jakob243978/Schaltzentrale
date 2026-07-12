"""SKILL-098 — Tests: Visual-Anti-KI-Klischee-Check (Image-Prompt-Ebene).

Creative-Leitplanke (Playbook §10): keine KI-Klischees (Glow, Neuronen, Roboter,
Violett-Gradient, Sparkle). Prueft einen Bild-/Motiv-Prompt. Projektneutral (die
warme Marken-Palette bleibt Projekt-Doku/Parameter).
"""
from __future__ import annotations

from creative_studio.specs import visual_cliche_warnings, AI_CLICHE_TERMS


def test_flags_ai_cliche_terms():
    assert any("Klischee" in w for w in visual_cliche_warnings("Glow und Neuronen mit Roboter"))


def test_flags_sparkle():
    assert visual_cliche_warnings("ein Sparkle-Effekt am Hologramm")


def test_clean_prompt_no_warning():
    assert visual_cliche_warnings("Founder am Kuechentisch, warmes Licht, Handy-Look") == []


def test_empty_prompt_no_warning():
    assert visual_cliche_warnings("") == []
    assert visual_cliche_warnings(None) == []


def test_cliche_terms_projektneutral():
    assert "roboter" in AI_CLICHE_TERMS
    for t in AI_CLICHE_TERMS:
        assert "jakob" not in t.lower()
