# SKILL-093: creative-studio — Value-Translations (Feature -> gefuehltes Leben) als projektneutrale Muster-Funktion

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (Substitutions-Funktion + Verb-Katalog + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** feature_zu_nutzen_uebersetzung_als_funktion + paare_als_parameter +
feature_level_verben_als_katalog + projektneutral + tests_gruen

## Kontext / Root-Cause
Das Playbook (§7) zeigt Value-Translations: „Agent fuehrt Prozesse aus" -> „Dein Betrieb
laeuft, waehrend du weg bist"; „Rahmen abstecken" -> „das Daran-Denken liegt im Prozess".
Diese Feature-zu-Leben-Uebersetzung war reine Handarbeit. Die konkreten Paare sind
projekt-spezifisch, der Mechanismus ist projektneutral.

## Was soll erreicht werden?
Eine projektneutrale `apply_value_translations(text, translations)`-Funktion setzt
projekt-gelieferte Feature->Nutzen-Paare ein (case-insensitiv, laengere Schluessel zuerst);
zusaetzlich ein projektneutraler Katalog `FEATURE_LEVEL_VERBS` (Signalverben, an denen
untranslatierte Technik-Copy erkennbar ist). Keine Projektwerte im Code.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Substitution]:** `apply_value_translations()` ersetzt Feature-Phrasen durch
      ihre Nutzen-Fassung; laengere Schluessel gewinnen; case-insensitiv.
      *(Tests `test_applies_translation_pair`, `test_longer_key_wins`, `test_case_insensitive`.)*
- [x] **EARS-2 [Must, nicht-brechend]:** leeres Mapping/leerer Text -> unveraenderte Ausgabe.
      *(Test `test_empty_mapping_is_noop`.)*
- [x] **EARS-3 [Must, projektneutral]:** die konkreten Paare kommen als Parameter; der
      `FEATURE_LEVEL_VERBS`-Katalog ist generisch (kein „Jakob"/Immo-Nomen).
      *(Test `test_feature_verbs_catalog_projektneutral`.)*

## Loesungs-Skizze
- `creative_studio/frameworks.py`: `FEATURE_LEVEL_VERBS`, `apply_value_translations()`.
- `tests/test_skill_093_value_translations.py`.

## Test-Ergebnis / Beleg
- `python -m pytest tests/ -q` -> **426 passed, 3 skipped**.

## Code-Referenzen
- `creative_studio/frameworks.py`
- `tests/test_skill_093_value_translations.py` (neu)
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§7)
