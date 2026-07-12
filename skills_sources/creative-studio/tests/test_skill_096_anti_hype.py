"""SKILL-096 — Tests: Anti-Hype-Framework + Hype-Warnung (Ehrlichkeit = Vertrauen).

Anti-Hype-Formel (F5) liegt als CopyFramework vor; hype_warnings markiert Hype-/
Wunder-Vokabular und verweist auf die ehrliche Formel. Reine Warnung.
"""
from __future__ import annotations

from creative_studio.frameworks import FRAMEWORKS
from creative_studio.specs import hype_warnings, HYPE_TRIGGERS


def test_anti_hype_framework_present():
    f = FRAMEWORKS["anti_hype"]
    assert "cold" in f.traffic
    assert "ehrliche_wahrheit" in f.slots


def test_hype_warning_flags_wonder_promise():
    assert any("Hype" in w for w in hype_warnings("Muehelos auf Autopilot ueber Nacht"))


def test_hype_warning_points_to_anti_hype_formula():
    w = hype_warnings("Die revolutionaere Zauberformel")
    assert any("anti_hype" in x for x in w)


def test_honest_copy_no_hype_warning():
    assert hype_warnings("Ehrlich vorweg: die ersten Wochen sind mehr Arbeit.") == []


def test_hype_triggers_projektneutral():
    for t in HYPE_TRIGGERS:
        assert "jakob" not in t.lower()
