"""SKILL-094 — Tests: CTA-Bibliothek (Button · hart · weich).

Projektneutrale CTA-Formulierungen nach Verbindlichkeit, per Kategorie abrufbar +
Reverse-Lookup eines CTA-Textes auf seine Kategorie.
"""
from __future__ import annotations

import pytest

from creative_studio.frameworks import CTA_LIBRARY, CTA_CATEGORIES, get_ctas, cta_category


def test_three_categories():
    assert set(CTA_CATEGORIES) == {"button", "hart", "weich"}
    assert set(CTA_LIBRARY) == set(CTA_CATEGORIES)


def test_get_ctas_returns_variants():
    assert "Registrieren" in get_ctas("button")
    assert "Sichere dir deinen Platz" in get_ctas("hart")
    assert "Ich zeig dir wie" in get_ctas("weich")


def test_get_ctas_unknown_raises():
    with pytest.raises(KeyError):
        get_ctas("nonsense")


def test_cta_category_reverse_lookup():
    assert cta_category("Registrieren") == "button"
    assert cta_category("Trag dich ein") == "hart"
    assert cta_category("Willst du wissen wie") == "weich"


def test_cta_category_unknown_is_none():
    assert cta_category("Kauf jetzt sofort") is None


def test_ctas_dashfrei_and_projektneutral():
    from creative_studio.specs import check_no_emdash
    for variants in CTA_LIBRARY.values():
        for v in variants:
            assert check_no_emdash(v) == []
            assert "jakob" not in v.lower()
