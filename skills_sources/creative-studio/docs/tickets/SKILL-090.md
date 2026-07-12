# SKILL-090: creative-studio — Projekt-Voice-of-Customer als Copy-Datenquelle + Human-Rule-Check im Copy-Flow

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (Parameter + Prompt-Einhaengung + Warn-Check + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** copy_flow_nutzt_projekt_voc + human_rule_warnungen_im_vorpruef_flow +
voc_als_parameter_kein_hartkodierter_projektwert + tests_gruen

## Kontext / Root-Cause
SKILL-088 (Doku) + SKILL-089 (Framework-Templates) liefern Regeln und Kundensprache, aber
der eigentliche Copy-Generierungs-Pfad (`content.build_analysis_prompt`) zieht die
**projekt-spezifische Kundensprache** (Vokabular, O-Toene, verbotene Abstrakta) noch nicht
ein und warnt nicht, wenn Copy gegen die Human-Rules verstoesst. Damit menschliche,
VoC-geerdete Copy nicht Handarbeit bleibt, muss der Flow die Projekt-VoC als Datenquelle
akzeptieren — projektneutral, per Parameter (nicht hartkodiert).

## Was soll erreicht werden?
Der Copy-Flow kann optional eine **Projekt-Messaging-/VoC-Datei** (Pfad-Parameter, analog
`--brand-env`) einlesen und ihre Kundensprache in den Analyse-Prompt einspeisen; zusaetzlich
laeuft der Human-Rule-Warn-Check (aus SKILL-089) im Copy-Vorpruef-Flow (Bild + Reel) als
Mensch-im-Loop-Warnung. Ohne Datei: unveraendertes Bestandsverhalten.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, VoC-Parameter]:** `content.load_messaging_doc(pfad)` liest die Datei ein;
      `build_analysis_prompt(..., messaging_doc=...)` speist die Kundensprache ein (Prompt fordert
      Kundensprache, verbietet Consultant-Abstrakta). *(Tests `test_messaging_doc_flows_into_prompt`,
      `test_load_messaging_doc_reads_file`.)*
- [x] **EARS-2 [Must, Rule-Check im Flow]:** `AdContent.warnings()` + `content_structure_warnings()`
      haengen die Human-Rule- + Brand-Voice- + Hype-Warnungen ein (Statistik-Opener, Begriff-zuerst,
      Consultant-Nomen, Tool-Namen). *(Tests `test_human_rule_warnings_in_image_flow_*`,
      `test_human_rule_warnings_in_reel_flow`, `test_reel_forbidden_tools_from_spec`.)*
- [x] **EARS-3 [Must, nicht-brechend/projektneutral]:** Ohne `messaging_doc` bleibt alles
      unveraendert; kein Projektwert hartkodiert (category_term/forbidden_tools als Parameter);
      fehlende Datei → Fallback ohne Fehler. *(Tests `test_clean_copy_unchanged`,
      `test_clean_reel_spec_unchanged`, `test_load_messaging_doc_missing_file_graceful`.)*
- [x] **EARS-4 [Should, SKILL.md]:** SKILL.md dokumentiert den `messaging_doc`-Parameter +
      verweist auf das Playbook als Copy-Grundlage fuer Cold-Audience-Projekte.

## Loesungs-Skizze
- `creative_studio/content.py`: Parameter + Prompt-Einhaengung + Warn-Checks.
- `creative_studio/render_image.py`/CLI: `--messaging-doc` durchreichen.
- `SKILL.md`: Abschnitt Copy/Standards ergaenzen.
- `tests/test_skill_090_project_voc_flow.py`.

## Test-Ergebnis / Beleg
- `python -m pytest tests/ -q` -> **426 passed, 3 skipped**. Neue Datei
  `tests/test_skill_090_project_voc_flow.py` gruen.

## Code-Referenzen
- `creative_studio/content.py` (`load_messaging_doc`, `build_analysis_prompt(messaging_doc=...)`,
  Human-/Brand-Voice-/Hype-Checks in `content_structure_warnings`)
- `creative_studio/specs.py` (`AdContent.category_term`/`forbidden_tools`, Wiring in `warnings()`)
- `tests/test_skill_090_project_voc_flow.py` (neu)
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md`
