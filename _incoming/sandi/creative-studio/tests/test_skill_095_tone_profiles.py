"""SKILL-095 — Tests: Ton-Profile / Ansprache (Buyer vs Champion).

Zwei generische Ansprache-Profile fuer High-Ticket-Kaltkontakt. Projektneutrale
Struktur (Buyer = Ergebnis zuerst, Sie/verdientes Du; Champion = verbuendetes du).
"""
from __future__ import annotations

import pytest

from creative_studio.frameworks import TONE_PROFILES, get_tone_profile


def test_two_profiles_present():
    assert set(TONE_PROFILES) == {"buyer", "champion"}


def test_buyer_leads_with_result_and_sie_asymmetry():
    buyer = get_tone_profile("buyer")
    assert "Ergebnis" in buyer.lead_with
    # du/Sie-Risiko-Asymmetrie dokumentiert.
    assert "Sie" in buyer.pronoun
    assert "beleidigt nie" in buyer.note.lower() or "anbiedern" in buyer.note.lower()


def test_champion_is_du_verbuendet():
    champ = get_tone_profile("champion")
    assert "du" in champ.pronoun.lower()
    assert "win" in champ.lead_with.lower() or "entlast" in champ.lead_with.lower()


def test_get_tone_profile_unknown_raises():
    with pytest.raises(KeyError):
        get_tone_profile("nonsense")


def test_profiles_projektneutral():
    for p in TONE_PROFILES.values():
        blob = (p.audience + p.pronoun + p.lead_with + p.register + p.note).lower()
        assert "jakob" not in blob
        assert "immobilien" not in blob
