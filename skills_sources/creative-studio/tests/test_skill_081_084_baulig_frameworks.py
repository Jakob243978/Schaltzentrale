"""SKILL-081..084 — Tests fuer die 4 Baulig-Copy-Frameworks.

mindset_shift (081), opportunity (082), avatar_story (083), heros_journey (084).
1 EARS = mind. 1 Test. Projektneutral, pytest. Prueft Slots (inkl. CTA-Slot),
Template==Slots, awareness-Tags, Abgrenzungs-/Proof-/DACH-Notes, Goal-Hints und
Nicht-Bruch der Bestands-Frameworks.
"""
from __future__ import annotations
import string

import pytest

from creative_studio import frameworks as fw


NEW_FRAMEWORKS = {
    "mindset_shift": ("situation", "false_belief", "truth", "future_projection", "cta"),
    "opportunity": ("new_opportunity", "old_way_downsides", "new_way_upsides", "cta"),
    "avatar_story": ("self_select", "current_problems", "mirrored_customer",
                     "discovered_solution", "new_results", "cta"),
    "heros_journey": ("past_self", "problems", "nothing_worked", "near_giving_up",
                      "discovery", "new_world", "pay_it_forward", "cta"),
}


# --- Existenz + exakte Slots (EARS-1 je Ticket) -----------------------------
@pytest.mark.parametrize("key,slots", NEW_FRAMEWORKS.items())
def test_new_framework_exists_with_exact_slots(key, slots):
    f = fw.get_framework(key)
    assert f.key == key
    assert f.slots == slots, f"{key}: {f.slots} != {slots}"


@pytest.mark.parametrize("key", NEW_FRAMEWORKS)
def test_new_framework_has_explicit_cta_slot(key):
    # Jedes neue Baulig-Framework braucht einen expliziten CTA-Slot.
    assert "cta" in fw.get_framework(key).slots, f"{key}: cta-Slot fehlt"


@pytest.mark.parametrize("key", NEW_FRAMEWORKS)
def test_new_framework_template_matches_slots(key):
    f = fw.get_framework(key)
    fmt = string.Formatter()
    placeholders = {name for _, name, _, _ in fmt.parse(f.template) if name is not None}
    assert placeholders == set(f.slots), f"{key}: {placeholders} != {set(f.slots)}"


@pytest.mark.parametrize("key", NEW_FRAMEWORKS)
def test_new_framework_awareness_valid(key):
    f = fw.get_framework(key)
    assert f.awareness, f"{key}: awareness fehlt"
    for tag in f.awareness:
        assert tag in fw.AWARENESS_LEVELS, f"{key}: unbekanntes awareness-Tag {tag}"


def test_awareness_assignments_match_tickets():
    # EARS-1 der Tickets: konkrete awareness-Zuordnung.
    assert set(fw.get_framework("mindset_shift").awareness) >= {"problem_aware", "solution_aware"}
    assert set(fw.get_framework("opportunity").awareness) >= {"solution_aware", "product_aware"}
    assert set(fw.get_framework("avatar_story").awareness) >= {"problem_aware", "solution_aware"}
    assert set(fw.get_framework("heros_journey").awareness) >= {"product_aware", "most_aware"}


# --- Notes: DACH / Abgrenzung / Proof (EARS-2/3 je Ticket) ------------------
def test_mindset_shift_note_belegbar():
    # SKILL-081 EARS-3: 'Wahrheit' muss belegbar bleiben (kein Fake-Reframe).
    note = fw.get_framework("mindset_shift").note.lower()
    assert "belegbar" in note or "fake" in note


def test_opportunity_note_grenzt_gegen_bab_ab():
    # SKILL-082 EARS-2: Abgrenzung Mechanismus vs. Zustand + Superlativ-Warnung.
    note = fw.get_framework("opportunity").note.lower()
    assert "bab" in note
    assert "mechanism" in note or "weg" in note
    assert "superlative" in note or "einzigartig" in note


def test_avatar_story_note_proof_pflicht():
    # SKILL-083 EARS-3/4: Beleg-Pflicht + Ebenen-Trennung (ContentType testimonial).
    note = fw.get_framework("avatar_story").note.lower()
    assert "requires_proof" in note or "beleg" in note
    assert "testimonial" in note


def test_heros_journey_note_grenzt_ab_und_dach():
    # SKILL-084 EARS-2/4: Abgrenzung hso/pastor + Ehrlichkeits-Warnung.
    note = fw.get_framework("heros_journey").note.lower()
    assert "hso" in note and "pastor" in note
    assert "belegbar" in note or "ehrlich" in note or "before_after" in note


# --- Goal-Hints (Auswahl, nicht-brechend) -----------------------------------
@pytest.mark.parametrize("goal,expected", [
    ("belief", "mindset_shift"),
    ("mindset", "mindset_shift"),
    ("new_mechanism", "opportunity"),
    ("opportunity", "opportunity"),
    ("testimonial", "avatar_story"),
    ("avatar", "avatar_story"),
    ("founder_story", "heros_journey"),
    ("hero", "heros_journey"),
])
def test_goal_hint_selects_new_framework(goal, expected):
    # Angle-Hint ueberschreibt die Awareness-Default-Regel (additiv).
    assert fw.recommend_framework("problem_aware", goal=goal).key == expected


def test_goal_none_keeps_default_behavior():
    # Ohne goal bleibt die Bestands-Zuordnung problem_aware -> pas erhalten.
    assert fw.recommend_framework("problem_aware").key == "pas"
    assert fw.recommend_framework("unaware").key == "aida"


# --- Selbst-Selektions-Hook (SKILL-083 EARS-2) ------------------------------
def test_self_select_hook_exists():
    h = fw.get_hook("self_select")
    assert "{zielgruppe}" in h.template


# --- Nicht-brechend + projektneutral ----------------------------------------
def test_existing_frameworks_still_present():
    for key in ("aida", "pas", "bab", "fab", "pastor", "4p", "hso"):
        assert key in fw.FRAMEWORKS


def test_new_frameworks_projektneutral():
    blob = " ".join(
        fw.get_framework(k).name + " " + fw.get_framework(k).best_for + " "
        + fw.get_framework(k).template + " " + fw.get_framework(k).note
        for k in NEW_FRAMEWORKS
    ).lower()
    for forbidden in ("jakob", "immobilien", "agentisches arbeiten", "mentoring", "3.000"):
        assert forbidden not in blob, f"Projektwert '{forbidden}' hartkodiert"
