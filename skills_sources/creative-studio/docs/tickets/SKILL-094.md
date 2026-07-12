# SKILL-094: creative-studio — CTA-Bibliothek (Button · hart · weich) als abrufbarer Katalog

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** XS (Katalog + get/reverse-lookup + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** cta_katalog_nach_verbindlichkeit + abrufbar_per_kategorie +
reverse_lookup + projektneutral + tests_gruen

## Kontext / Root-Cause
Das Playbook (§7) sammelt CTAs nach Verbindlichkeit: Button (Registrieren/Anmelden/Mehr dazu),
hart (Trag dich ein/Sichere dir deinen Platz), weich (Ich zeig dir wie/Willst du wissen wie).
Sie lagen als Fliesstext, nicht als abrufbarer Katalog.

## Was soll erreicht werden?
Ein projektneutraler `CTA_LIBRARY`-Katalog (button/hart/weich) mit `get_ctas(category)` +
`cta_category(text)`-Reverse-Lookup. Generische deutsche CTAs, kein Projektwert.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Katalog]:** `CTA_LIBRARY` hat die drei Kategorien button/hart/weich;
      `get_ctas()` liefert die Varianten, unbekannte Kategorie -> KeyError.
      *(Tests `test_three_categories`, `test_get_ctas_returns_variants`, `test_get_ctas_unknown_raises`.)*
- [x] **EARS-2 [Must, Reverse-Lookup]:** `cta_category(text)` ordnet einen CTA-Text seiner
      Kategorie zu (oder None). *(Tests `test_cta_category_reverse_lookup`, `test_cta_category_unknown_is_none`.)*
- [x] **EARS-3 [Must, dashfrei/projektneutral]:** alle CTAs gedankenstrichfrei + ohne Projektwert.
      *(Test `test_ctas_dashfrei_and_projektneutral`.)*

## Loesungs-Skizze
- `creative_studio/frameworks.py`: `CTA_LIBRARY`, `CTA_CATEGORIES`, `get_ctas`, `cta_category`.
- `tests/test_skill_094_cta_library.py`.

## Test-Ergebnis / Beleg
- `python -m pytest tests/ -q` -> **426 passed, 3 skipped**.

## Code-Referenzen
- `creative_studio/frameworks.py`
- `tests/test_skill_094_cta_library.py` (neu)
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§7)
