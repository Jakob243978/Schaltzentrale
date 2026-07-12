"""SKILL-085 — Tests fuer die Auslieferungs-Empfehlung (Empfehlungs-Metadaten + Auswahl).

Jedes Framework traegt awareness/funnel/traffic/best_for; match_frameworks filtert den
Katalog ueber die generischen Achsen; framework_matrix liefert die "wann + fuer wen"-
Uebersicht. Projektneutral, pytest.
"""
from __future__ import annotations

import pytest

from creative_studio import frameworks as fw


# --- Empfehlungs-Metadaten vorhanden + valide -------------------------------
def test_every_framework_has_recommendation_metadata():
    for key, f in fw.FRAMEWORKS.items():
        assert f.awareness, f"{key}: awareness fehlt"
        assert f.funnel, f"{key}: funnel fehlt"
        assert f.traffic, f"{key}: traffic fehlt"
        assert f.best_for, f"{key}: best_for fehlt"


def test_funnel_traffic_values_are_known():
    for key, f in fw.FRAMEWORKS.items():
        for stage in f.funnel:
            assert stage in fw.FUNNEL_STAGES, f"{key}: unbekannte funnel-Stufe {stage}"
        for temp in f.traffic:
            assert temp in fw.TRAFFIC_TEMPERATURES, f"{key}: unbekannte traffic-Temperatur {temp}"


# --- match_frameworks (Mehrfach-Auswahl) ------------------------------------
def test_match_by_awareness_and_funnel():
    # awareness="cold" -> Tag "unaware", funnel="tofu": AIDA + die szenen-basierten
    # Cold-Audience-Formeln (SKILL-089), die ebenfalls unaware/tofu getaggt sind.
    keys = [f.key for f in fw.match_frameworks(awareness="cold", funnel="tofu")]
    assert "aida" in keys
    assert "scene" in keys  # SKILL-089: szenen-basierte Cold-Audience-Formel
    assert "mindset_shift" not in keys  # problem/solution_aware, nicht unaware


def test_match_by_traffic_and_funnel_cold_tofu():
    # kalt/TOFU ueber die Traffic-Achse: AIDA + PAS + mindset_shift; bab (warm) nicht.
    keys = [f.key for f in fw.match_frameworks(traffic="cold", funnel="tofu")]
    assert "aida" in keys
    assert "pas" in keys
    assert "mindset_shift" in keys
    assert "bab" not in keys


def test_match_by_traffic_only():
    keys = [f.key for f in fw.match_frameworks(traffic="retargeting")]
    assert "hso" in keys  # hso ist warm/retargeting


def test_match_goal_narrows_to_single():
    res = fw.match_frameworks(goal="testimonial")
    assert [f.key for f in res] == ["avatar_story"]


def test_match_no_filter_returns_full_catalog():
    assert len(fw.match_frameworks()) == len(fw.FRAMEWORKS)


def test_match_unknown_axis_raises():
    with pytest.raises(ValueError):
        fw.match_frameworks(funnel="banana")
    with pytest.raises(ValueError):
        fw.match_frameworks(awareness="banana")
    with pytest.raises(ValueError):
        fw.match_frameworks(goal="banana")


# --- framework_matrix / Tabellen-Ausgabe ------------------------------------
def test_framework_matrix_complete():
    matrix = fw.framework_matrix()
    assert len(matrix) == len(fw.FRAMEWORKS)
    for row in matrix:
        assert set(row) >= {"key", "awareness", "funnel", "traffic", "best_for", "slots"}


def test_matrix_table_lists_all_keys():
    table = fw.format_matrix_table()
    for key in fw.FRAMEWORKS:
        assert key in table


# --- recommend_framework mit funnel/traffic bleibt nicht-brechend -----------
def test_recommend_with_extra_hints_still_default():
    # funnel/traffic-Hints allein aendern die Awareness-Default-Wahl nicht.
    assert fw.recommend_framework("problem_aware", funnel="tofu", traffic="cold").key == "pas"
