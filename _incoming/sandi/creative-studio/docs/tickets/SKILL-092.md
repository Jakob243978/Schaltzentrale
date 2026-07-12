# SKILL-092: creative-studio — Brand-Voice-Leitplanken (Tool-Namen/Preis/FOMO/Wortwahl) als Warn-Checks

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (Warn-Funktion + Kataloge + Wiring + Tests)
**surface:** backend
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** brand_voice_warnungen_im_copy_flow + keine_tool_namen + kein_preis +
motivation_statt_angst + individueller_statt_kompliziert + projektneutral + tests_gruen

## Kontext / Root-Cause
Das Playbook (§2) definiert verbindliche Marken-Leitplanken jenseits der legalen DACH-
Compliance (SKILL-026): keine Tool-Namen (Claude/n8n/Coder ...), kein Preis, Motivation
statt Angst (kein FOMO/„sonst haengst du ab"), nie „Geschaeftsfuehrer", „individueller"
statt „komplizierter". Der Copy-Vorpruef-Flow kannte diese Regeln bisher nicht.

## Was soll erreicht werden?
Eine `brand_voice_warnings()`-Funktion (Companion zu `compliance_warnings`, KEIN Ersatz)
prueft Copy auf diese Marken-Leitplanken und wird in den Bild- + Reel-Copy-Flow eingehaengt.
Projektneutral: die generische Tool-Marken-Liste enthaelt allgemein bekannte Dritt-Produkte;
projekt-eigene Tool-Namen kommen als Parameter (`forbidden_tools`), nicht hartkodiert.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Tool-Namen]:** `brand_voice_warnings()` warnt bei generischen Tool-Marken
      (chatgpt/n8n ...) und bei per `forbidden_tools`-Parameter uebergebenen Projekt-Tools.
      *(Tests `test_flags_generic_tool_name`, `test_flags_project_tool_via_parameter`.)*
- [x] **EARS-2 [Must, Preis/Wortwahl/FOMO]:** warnt bei Preis/Waehrungsbetrag, „Geschaeftsfuehrer",
      „kompliziert(er)" und FOMO-/Angst-Formulierungen (Motivation statt Angst).
      *(Tests `test_flags_price`, `test_flags_geschaeftsfuehrer`, `test_flags_kompliziert`, `test_flags_fomo`.)*
- [x] **EARS-3 [Must, Flow + nicht-brechend]:** eingehaengt in `AdContent.warnings()` +
      `content_structure_warnings()`; saubere Copy erzeugt keine Warnung; kein Projektwert hartkodiert.
      *(Tests `test_clean_copy_no_brand_voice_warning`, `test_generic_tool_list_projektneutral`,
      SKILL-090 `test_clean_copy_unchanged`.)*

## Loesungs-Skizze
- `creative_studio/specs.py`: `GENERIC_AI_TOOL_NAMES`, `FEAR_FOMO_TRIGGERS`, `_PRICE_RE`,
  `brand_voice_warnings()`; Wiring in `AdContent.warnings()` (+ Felder `forbidden_tools`).
- `creative_studio/content.py`: Wiring in `content_structure_warnings()`.
- `tests/test_skill_092_brand_voice.py`.

## Test-Ergebnis / Beleg
- `python -m pytest tests/ -q` -> **426 passed, 3 skipped**.

## Code-Referenzen
- `creative_studio/specs.py`, `creative_studio/content.py`
- `tests/test_skill_092_brand_voice.py` (neu)
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§2)
