# SKILL-085: creative-studio — Auslieferungs-Empfehlung je Framework (Empfehlungs-Matrix)

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (Metadaten-Felder + Auswahl-Funktion + CLI + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** jedes_framework_traegt_awareness_funnel_traffic_bestfor +
recommend/match_liefert_passende_frameworks + empfehlungsmatrix_abrufbar (CLI list) +
kein_projektwert_hartkodiert

## Kontext / Root-Cause
Der Framework-Katalog (`frameworks.FRAMEWORKS`) beschrieb bisher nur Struktur (Slots) +
`awareness` + `best_for`. Zielgruppe/Timing (Funnel-Stufe, Traffic-Temperatur) musste man
beim Erzeugen manuell mitdenken. Fuer einen einheitlichen Katalog — inkl. der 4 neuen
Baulig-Frameworks (SKILL-081..084) — fehlten generische Auslieferungs-Metadaten und eine
Auswahl-Hilfe ("welches Framework, wann, fuer wen?").

## Was soll erreicht werden?
Jedes Framework (Bestand **und** neu) traegt Empfehlungs-Metadaten auf generischen Achsen:
`awareness` (Schwartz), `funnel` (tofu/mofu/bofu), `traffic` (cold/warm/retargeting),
`best_for`. Dazu eine Auswahl-Hilfe (Funktion + CLI) und eine Matrix-Ausgabe. Projektneutral.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Metadaten]:** `CopyFramework` hat `funnel` + `traffic` (zusaetzlich zu
      `awareness`/`best_for`); ALLE Eintraege (11) sind befuellt und nur mit Werten aus
      `FUNNEL_STAGES`/`TRAFFIC_TEMPERATURES`/`AWARENESS_LEVELS`.
      *(Tests `test_every_framework_has_recommendation_metadata`, `test_funnel_traffic_values_are_known`.)*
- [x] **EARS-2 [Must, Mehrfach-Auswahl]:** `match_frameworks(awareness=, funnel=, traffic=, goal=)`
      filtert den Katalog AND-verknuepft; unbekannte Achsen -> `ValueError` (keine stille Leerliste).
      *(Tests `test_match_*`.)*
- [x] **EARS-3 [Must, Matrix]:** `framework_matrix()` liefert je Framework eine Zeile mit
      awareness/funnel/traffic/best_for/slots; CLI `python -m creative_studio.frameworks list`
      gibt die Matrix (Tabelle oder `--json`) aus. *(Tests `test_framework_matrix_complete`, `test_matrix_table_lists_all_keys`.)*
- [x] **EARS-4 [Must, nicht-brechend]:** `recommend_framework(awareness, placement)` bleibt
      abwaertskompatibel; optionale `funnel`/`traffic`/`goal`-Hints aendern die
      Awareness-Default-Wahl nicht. `goal` (Angle-Hint) waehlt gezielt ein Baulig-Framework.
      *(Test `test_recommend_with_extra_hints_still_default` + SKILL-081..084-Goal-Tests.)*
- [x] **EARS-5 [Must, multi-projekt]:** awareness/funnel/traffic sind generische Achsen —
      KEIN hartkodierter Projektwert (AgentischesArbeiten o.Ae.) in frameworks.py.

## Loesungs-Skizze
- `frameworks.py`: `FUNNEL_STAGES`/`TRAFFIC_TEMPERATURES`-Konstanten, `funnel`/`traffic`-Felder
  am `CopyFramework`, alle Eintraege befuellt; `match_frameworks`, `framework_matrix`,
  `format_matrix_table`, CLI `main()` (`list`/`recommend`).
- `tests/test_skill_085_recommend_metadata.py`.
- SKILL.md: Framework-Katalog + Empfehlungs-Matrix.

## Test-Ergebnis / Beleg
- **Suite gruen:** `python -m pytest -q` -> **349 passed**.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/frameworks.py`
- `skills_sources/creative-studio/tests/test_skill_085_recommend_metadata.py`
- `skills_sources/creative-studio/docs/ad-frameworks/baulig-methoden.md`
- `skills_sources/creative-studio/SKILL.md`
