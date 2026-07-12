"""SKILL-091 — Tests: Ad-Daten-Muster (konkret-menschlich gewinnt) im Code.

Ad-Performance-Lehre (Playbook §5): konkret-menschliche Angles gewinnen bei kalter
Zielgruppe, abstrakt/Statistik verliert. Encodiert als (a) Statistik-Opener-Warnung
und (b) Cold-Ranking, das szenen-/ergebnis-basierte Formeln vor die uebrigen
cold-Frameworks zieht.
"""
from __future__ import annotations

from creative_studio import frameworks as fw
from creative_studio.specs import human_rule_warnings


def test_statistics_opener_is_flagged():
    assert any("Statistik" in w for w in human_rule_warnings("0,42 Prozent CTR ueberzeugt keinen."))


def test_scene_opener_not_flagged():
    assert human_rule_warnings("Die Buchungsanfrage kam um 23:14 Uhr rein.") == []


def test_cold_ranking_puts_scene_formulas_before_generic():
    keys = [f.key for f in fw.match_frameworks(traffic="cold")]
    assert keys[0] in fw.COLD_AUDIENCE_FORMULAS
    # aida/pas (generische cold-Frameworks) stehen nach den Formeln.
    if "aida" in keys:
        assert keys.index("scene") < keys.index("aida")


def test_scene_formula_is_first_choice_for_cold_unaware():
    keys = [f.key for f in fw.match_frameworks(awareness="unaware", traffic="cold")]
    assert keys[0] == "scene"
