"""SKILL-025 — Tests fuer frameworks.py (Copy-Framework-Katalog + Hooks + Validatoren).

1 EARS = mind. 1 Test. Projektneutral, pytest.
"""
from __future__ import annotations
import string

import pytest

from creative_studio import frameworks as fw


# --- EARS-1: CopyFramework-Katalog vollstaendig + wohlgeformt ----------------
def test_ears1_catalog_has_required_frameworks():
    # mind. AIDA, PAS, BAB, FAB, PASTOR, 4P, Hook-Story-Offer
    required = {"aida", "pas", "bab", "fab", "pastor", "4p", "hso"}
    assert required.issubset(set(fw.FRAMEWORKS)), (
        f"Fehlende Frameworks: {required - set(fw.FRAMEWORKS)}"
    )


def test_ears1_frameworks_wellformed():
    for key, f in fw.FRAMEWORKS.items():
        assert f.key == key, f"Key-Mismatch bei {key}"
        assert f.name, f"{key}: name fehlt"
        assert f.slots, f"{key}: slots fehlen"
        assert f.awareness, f"{key}: awareness-Tags fehlen"
        assert f.best_for, f"{key}: best_for fehlt"
        assert f.template, f"{key}: template fehlt"
        # awareness-Tags muessen bekannte Levels sein
        for tag in f.awareness:
            assert tag in fw.AWARENESS_LEVELS, f"{key}: unbekanntes awareness-Tag '{tag}'"


def test_ears1_template_placeholders_match_slots():
    # Jedes template muss genau die slots als {slot}-Platzhalter enthalten.
    fmt = string.Formatter()
    for key, f in fw.FRAMEWORKS.items():
        placeholders = {
            name for _, name, _, _ in fmt.parse(f.template) if name is not None
        }
        assert placeholders == set(f.slots), (
            f"{key}: Platzhalter {placeholders} != slots {set(f.slots)}"
        )


def test_ears1_pas_slots_exact():
    # Stichprobe: PAS = problem/agitate/solution/cta in Reihenfolge.
    # SKILL-081-Delta (Baulig #1): expliziter CTA-Slot additiv ergaenzt.
    assert fw.FRAMEWORKS["pas"].slots == ("problem", "agitate", "solution", "cta")


def test_ears5_no_hardcoded_project_values():
    # Multi-Projekt: keine projekt-spezifischen Claims/Tonalitaet hartkodiert.
    blob = " ".join(
        f.name + " " + f.best_for + " " + f.template + " " + f.note
        for f in fw.FRAMEWORKS.values()
    ).lower()
    for forbidden in ("jakob", "immobilien", "agentisches arbeiten", "mentoring", "3.000"):
        assert forbidden not in blob, f"Projektwert '{forbidden}' im Katalog hartkodiert"


# --- EARS-2: Hook-Bibliothek >= 6 + Wortgrenze ------------------------------
def test_ears2_at_least_six_hooks():
    assert len(fw.HOOKS) >= 6, f"Nur {len(fw.HOOKS)} Hooks, erwartet >= 6"


def test_ears2_hooks_wellformed_and_max_words():
    assert fw.MAX_WORDS_ONSCREEN == 7
    for key, h in fw.HOOKS.items():
        assert h.key == key
        assert h.template, f"{key}: template fehlt"
        assert h.max_words_onscreen <= fw.MAX_WORDS_ONSCREEN


def test_ears2_word_limit_helper():
    # <= 7 Woerter -> passt, > 7 -> passt nicht.
    assert fw.hook_fits_onscreen("Eins zwei drei vier fuenf sechs sieben")
    assert not fw.hook_fits_onscreen("Eins zwei drei vier fuenf sechs sieben acht")
    assert fw.count_onscreen_words("Gib mir 30 Sekunden") == 4


# --- EARS-3: Awareness-gesteuerte Auswahl -----------------------------------
@pytest.mark.parametrize(
    "awareness,placement,expected",
    [
        ("unaware", "", "aida"),
        ("cold", "", "aida"),            # Synonym
        ("problem_aware", "", "pas"),
        ("solution_aware", "", "fab"),   # vergleichend, statisch
        ("solution_aware", "reel", "bab"),  # vergleichend, bildstark/Video
        ("product_aware", "video", "hso"),
        ("most_aware", "", "hso"),
        ("warm", "", "hso"),             # Synonym
        ("problem_aware", "vsl", "pastor"),  # Langform ueberschreibt
    ],
)
def test_ears3_recommend_framework(awareness, placement, expected):
    rec = fw.recommend_framework(awareness, placement)
    assert rec.key == expected, f"{awareness}/{placement} -> {rec.key}, erwartet {expected}"


def test_ears3_unknown_awareness_raises():
    with pytest.raises(ValueError):
        fw.recommend_framework("banana")


# --- EARS-4: 4U-Validator (Warn-Funktion) -----------------------------------
def test_ears4_weak_headline_yields_hints():
    hints = fw.validate_4u("Unser Angebot")
    assert hints, "Schwache Headline sollte Hinweise liefern"
    assert any("4U" in h for h in hints)


def test_ears4_strong_headline_few_or_no_hints():
    # nuetzlich (ohne/abgeben), spezifisch (Zahl), dringlich (Warteliste)
    strong = "In 6 Monaten Routine abgeben — jetzt auf die Warteliste"
    score = fw.score_4u(strong)
    erfuellt = sum(1 for ok in score.values() if ok)
    assert erfuellt >= 3, f"Starke Headline erfuellt nur {erfuellt}/4: {score}"


def test_ears4_is_warning_not_hard_block():
    # validate_4u gibt eine Liste zurueck (Hinweise), wirft NICHT.
    assert isinstance(fw.validate_4u("irgendwas"), list)
    assert fw.validate_4u("") == ["4U: leere Headline — keine Bewertung moeglich."]
