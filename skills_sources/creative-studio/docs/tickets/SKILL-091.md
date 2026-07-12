# SKILL-091: creative-studio — Ad-Daten-Muster (konkret-menschlich gewinnt) im Code encodieren

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (Warn-Check + Cold-Ranking + Tests)
**surface:** backend
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** statistik_opener_wird_gewarnt + cold_ranking_szene_vor_generisch +
projektneutral_kein_hartkodierter_projektwert + tests_gruen

## Kontext / Root-Cause
Der Meta-Ad-Report (Playbook §5) zeigt ein eindeutiges Muster: konkret-menschliche
Angles gewinnen bei kalter Zielgruppe (`hook-kopf-erinnert` 4,62 % CTR, `hook-2x-durchsatz`
bester CPL), abstrakt/Statistik verliert (`hook-93-stat` 0,42 %, `hook-ki-agenten` CPL 69 €,
`hook-datenschutz` 0 Leads). Ergebnis-/Alltags-Angles bringen Leads, Verstaendnis-/Technik-/
Statistik-Angles nur Klicks. Der Generator kannte diese Lehre bisher nicht.

## Was soll erreicht werden?
Die Ad-Daten-Lehre ist testbar encodiert: (a) ein Statistik-Opener (Prozent-Claim in Zeile 1)
loest eine Warnung aus, (b) `match_frameworks(traffic="cold")` zieht die szenen-/ergebnis-
basierten Formeln (SKILL-089) vor die uebrigen cold-Frameworks. Projektneutral (keine
konkreten Projekt-Kampagnennamen im Code — die stehen als Doku im Playbook §5).

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Warn]:** `specs.human_rule_warnings()` markiert einen Prozent-Statistik-
      Opener in Zeile 1; eine krumme, konkrete Zahl OHNE Prozent loest keine Warnung aus.
      *(Tests `test_statistics_opener_is_flagged`, `test_scene_opener_not_flagged`.)*
- [x] **EARS-2 [Must, Ranking]:** `match_frameworks(traffic="cold")` liefert die
      szenen-/ergebnis-basierten Formeln (`COLD_AUDIENCE_FORMULAS`) vor den generischen
      cold-Frameworks (aida/pas). *(Tests `test_cold_ranking_puts_scene_formulas_before_generic`,
      `test_scene_formula_is_first_choice_for_cold_unaware`.)*
- [x] **EARS-3 [Should, projektneutral]:** Kein hartkodierter Projekt-Kampagnenname/-wert im
      Code; die konkreten Winner/Kill-Beispiele bleiben Playbook-Doku (§5).

## Loesungs-Skizze
- `creative_studio/specs.py`: `_STAT_OPENER_RE` + Statistik-Opener-Warnung in `human_rule_warnings`.
- `creative_studio/frameworks.py`: `COLD_AUDIENCE_FORMULAS` + Cold-Sortierung in `match_frameworks`.
- `tests/test_skill_091_ad_data_pattern.py`.

## Test-Ergebnis / Beleg
- `python -m pytest tests/ -q` -> **426 passed, 3 skipped**.

## Code-Referenzen
- `creative_studio/specs.py`, `creative_studio/frameworks.py`
- `tests/test_skill_091_ad_data_pattern.py` (neu)
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§5)
