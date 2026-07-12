# SKILL-096: creative-studio — Anti-Hype-Framework + Hype-Warnung (Ehrlichkeit = Vertrauen)

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** XS (Formel-Framework (via 089) + Hype-Warn-Funktion + Tests)
**surface:** backend
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** anti_hype_formel_verfuegbar + hype_vokabular_wird_gewarnt +
verweis_auf_ehrliche_formel + projektneutral + tests_gruen

## Kontext / Root-Cause
Ueber zwei Kunden belegt (Playbook §8, VoC): Ehrlichkeit, wo KI (noch) nicht lohnt, schlaegt
Hype. „Die ersten Wochen sind mehr Arbeit" -> spaeter „es erleichtert die Arbeit und macht
Spass". Der staerkste Vertrauensanker ist die unbequeme Wahrheit statt das Wunderversprechen.

## Was soll erreicht werden?
Die Anti-Hype-Formel liegt als CopyFramework vor (F5, via SKILL-089), und `hype_warnings()`
markiert Hype-/Wunder-Vokabular und verweist auf die ehrliche Formel. Reine Warnung,
projektneutral.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Formel]:** `FRAMEWORKS["anti_hype"]` existiert (traffic cold, Slot
      `ehrliche_wahrheit`). *(Test `test_anti_hype_framework_present`.)*
- [x] **EARS-2 [Must, Warn]:** `hype_warnings()` markiert Hype-Vokabular (muehelos/Autopilot/
      revolutionaer ...) und verweist auf `anti_hype`; ehrliche Copy erzeugt keine Warnung.
      *(Tests `test_hype_warning_flags_wonder_promise`, `test_hype_warning_points_to_anti_hype_formula`, `test_honest_copy_no_hype_warning`.)*
- [x] **EARS-3 [Must, projektneutral]:** `HYPE_TRIGGERS` generisch (kein Projektwert).
      *(Test `test_hype_triggers_projektneutral`.)*

## Loesungs-Skizze
- `creative_studio/frameworks.py`: `anti_hype`-CopyFramework (SKILL-089).
- `creative_studio/specs.py`: `HYPE_TRIGGERS`, `hype_warnings()`; Wiring in Bild-/Reel-Flow.
- `tests/test_skill_096_anti_hype.py`.

## Test-Ergebnis / Beleg
- `python -m pytest tests/ -q` -> **426 passed, 3 skipped**.

## Code-Referenzen
- `creative_studio/frameworks.py`, `creative_studio/specs.py`
- `tests/test_skill_096_anti_hype.py` (neu)
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§8)
