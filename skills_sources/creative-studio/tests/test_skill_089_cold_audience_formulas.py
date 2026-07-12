"""SKILL-089 — Tests: Cold-Audience-Hook-Formeln (F1-F6) + Human-Rules encodiert.

Die 6 menschlichen Hook-Formeln liegen als projektneutrale CopyFrameworks im
Katalog (awareness/funnel/traffic aus SKILL-085), die 8 Human-Regeln sind als
abrufbare Pruefliste verfuegbar, match_frameworks bevorzugt bei kalter Zielgruppe
die szenen-basierten Formeln, und alle neuen Templates sind gedankenstrichfrei +
projektneutral.
"""
from __future__ import annotations

from creative_studio import frameworks as fw
from creative_studio.specs import check_no_emdash, human_rule_warnings


# --- EARS-1: die 6 Formeln existieren als FRAMEWORKS-Eintraege ----------------
def test_cold_audience_formulas_present():
    for key in ("scene", "kunden_oton", "vorher_nachher", "einwand_oton",
                "anti_hype", "umbruch"):
        assert key in fw.FRAMEWORKS, f"Formel {key} fehlt im Katalog"


def test_cold_audience_formulas_metadata():
    for key in fw.COLD_AUDIENCE_FORMULAS:
        f = fw.FRAMEWORKS[key]
        assert "cold" in f.traffic, f"{key}: traffic sollte cold enthalten"
        assert "tofu" in f.funnel, f"{key}: funnel sollte tofu enthalten"
        assert f.slots, f"{key}: slots fehlen"
        assert f.best_for, f"{key}: best_for fehlt"
        # Template nutzt genau die Slots als {slot}-Marker.
        for slot in f.slots:
            assert "{" + slot + "}" in f.template, f"{key}: Slot {slot} fehlt im Template"


# --- EARS-2: Human-Rules als Pruefliste + Warn-Checks -------------------------
def test_human_messaging_rules_are_eight():
    rules = fw.human_messaging_rules()
    assert len(rules) == 8
    keys = {r.key for r in rules}
    assert "szene_statt_these" in keys
    assert "begriff_zuletzt" in keys
    assert "krumme_echte_zahl" in keys


def test_human_rule_warns_on_statistics_opener():
    w = human_rule_warnings("93 Prozent der Unternehmer verlieren Zeit.")
    assert any("Statistik" in x for x in w)


def test_human_rule_no_warn_on_concrete_crumb_number():
    # Krumme, konkrete Zahl ohne Prozent ist erwuenscht -> keine Statistik-Warnung.
    w = human_rule_warnings("16 Wohnungen, morgens auf einer Liste.")
    assert not any("Statistik" in x for x in w)


def test_human_rule_warns_on_consultant_abstracta():
    w = human_rule_warnings("Mehr Durchsatz und weniger Overhead.")
    assert any("Consultant-Abstrakta" in x or "ihre Nomen" in x for x in w)


def test_human_rule_warns_on_term_in_opener():
    w = human_rule_warnings("Agentisches Arbeiten spart dir Zeit.",
                            category_term="agentisches Arbeiten")
    assert any("Begriff zuletzt" in x for x in w)


def test_human_rule_term_check_off_by_default():
    # Ohne category_term wird der Begriff-Check nicht ausgeloest.
    assert not any("Begriff zuletzt" in x
                   for x in human_rule_warnings("Agentisches Arbeiten spart Zeit."))


# --- EARS-3: match_frameworks bevorzugt szenen-basierte Formeln bei cold ------
def test_match_cold_prefers_scene_formulas_first():
    res = fw.match_frameworks(traffic="cold")
    keys = [f.key for f in res]
    # Die szenen-basierten Formeln stehen vor den uebrigen cold-Frameworks.
    scene_positions = [keys.index(k) for k in fw.COLD_AUDIENCE_FORMULAS if k in keys]
    other_cold = [i for i, k in enumerate(keys) if k not in fw.COLD_AUDIENCE_FORMULAS]
    assert max(scene_positions) < min(other_cold), keys


def test_recommend_framework_backwards_compatible():
    # SKILL-085-Bestand: unaware -> aida, problem_aware -> pas (nicht-brechend).
    assert fw.recommend_framework("unaware").key == "aida"
    assert fw.recommend_framework("problem_aware").key == "pas"


# --- EARS-4: neue Templates dashfrei + projektneutral ------------------------
def test_new_templates_dashfrei():
    for key in fw.COLD_AUDIENCE_FORMULAS:
        assert check_no_emdash(fw.FRAMEWORKS[key].template) == [], f"{key} Template hat langen Strich"


def test_no_project_values_in_new_templates():
    # Kein hartkodierter Projektwert (kein "Jakob", keine Immo-Nomen) in Slots/Template.
    forbidden = ("jakob", "immobilien", "mieter", "wohnung", "vermieter")
    for key in fw.COLD_AUDIENCE_FORMULAS:
        f = fw.FRAMEWORKS[key]
        blob = (f.template + " " + " ".join(f.slots)).lower()
        for bad in forbidden:
            assert bad not in blob, f"{key}: Projektwert '{bad}' im Template/Slots"


# --- EARS-5: framework_matrix zeigt die neuen Formeln mit --------------------
def test_matrix_includes_new_formulas():
    table = fw.format_matrix_table()
    for key in fw.COLD_AUDIENCE_FORMULAS:
        assert key in table
