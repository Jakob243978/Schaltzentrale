# SKILL-089: creative-studio — Cold-Audience-Hook-Formeln + Human-Rules als Framework-Templates encodieren

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** M (frameworks.py-Templates + Metadaten + Auswahl + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** hook_formeln_F1_F6_als_templates + human_rules_als_pruefliste_abrufbar +
recommend_beruecksichtigt_cold_audience + projektneutral_kein_hartkodierter_projektwert + tests_gruen

## Kontext / Root-Cause
SKILL-088 hat die Human-Messaging-Regeln + Hook-Formeln (F1 Szene, F2 O-Ton, F3 Vorher/
Nachher, F4 Einwand-als-O-Ton, F5 Anti-Hype, F6 Umbruch) als Doku konsolidiert. Der
Generator (`frameworks.py`, `content.py`) kennt sie aber noch NICHT — die Copy-Templates
dort tragen die „Szene statt Kategorie / Begriff zuletzt"-Logik nicht. Damit der Skill die
Erkenntnisse tatsaechlich anwendet (statt nur dokumentiert), muessen die Formeln testbar
in den Framework-Katalog — analog zur Encodierung der Baulig-Frameworks (SKILL-081..084).

## Was soll erreicht werden?
Die 6 Cold-Audience-Hook-Formeln liegen als projektneutrale Copy-Templates im
`FRAMEWORKS`-Katalog (mit awareness/funnel/traffic-Metadaten aus SKILL-085), und die
8 Human-Regeln sind als abrufbare Pruefliste/Funktion verfuegbar, sodass `recommend`/
`match_frameworks` fuer eine kalte, den-Begriff-nicht-kennende Zielgruppe die
szenen-basierten Formeln priorisiert. Keine projekt-spezifischen Werte im Code.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Templates]:** Die 6 Formeln (F1–F6) existieren als Eintraege im
      `FRAMEWORKS`-Katalog (scene/kunden_oton/vorher_nachher/einwand_oton/anti_hype/umbruch)
      mit Slot-Struktur, `awareness=unaware/problem-aware`, `traffic=cold`, `funnel=tofu`,
      `best_for`. *(Tests `test_cold_audience_formulas_present`, `test_cold_audience_formulas_metadata`.)*
- [x] **EARS-2 [Must, Human-Rules]:** `frameworks.human_messaging_rules()` liefert die 8 Regeln
      als strukturierte Liste; `specs.human_rule_warnings()` markiert Statistik-Opener,
      Consultant-Abstrakta und (optional per `category_term`) Begriff-zuerst als
      Mensch-im-Loop-Warnung (analog `compliance_warnings`/`dash_warnings`). *(Tests `test_human_*`.)*
- [x] **EARS-3 [Must, Auswahl]:** `match_frameworks(traffic="cold", awareness="unaware")`
      liefert die szenen-basierten Formeln zuerst (stabile Sortierung); `recommend_framework`
      bleibt abwaertskompatibel. *(Tests `test_match_cold_prefers_scene_formulas_first`,
      `test_recommend_framework_backwards_compatible`.)*
- [x] **EARS-4 [Must, dashfrei/projektneutral]:** Alle neuen Templates sind gedankenstrichfrei
      (SKILL-087) und enthalten KEINE projekt-spezifischen Werte (kein „Jakob", keine
      Immo-Nomen hartkodiert; Beispiele nur als `best_for`/Playbook). *(Tests `test_new_templates_dashfrei`, `test_no_project_values_in_new_templates`.)*
- [x] **EARS-5 [Should, Matrix]:** `framework_matrix()`/`format_matrix_table()` zeigt die neuen
      Formeln mit. *(Test `test_matrix_includes_new_formulas`.)*

## Loesungs-Skizze
- `creative_studio/frameworks.py`: 6 Formel-Templates + Metadaten; ggf. `human_messaging_rules()`.
- `creative_studio/specs.py` oder `content.py`: optionale Warn-Checks (Statistik-Opener, Begriff-zuerst).
- `tests/test_skill_089_cold_audience_formulas.py`.
- Quelle/Referenz: `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§4, §1).

## Test-Ergebnis / Beleg
- `python -m pytest tests/ -q` -> **426 passed, 3 skipped** (Bestand 363 -> +63 neue Tests
  ueber SKILL-089..098). Neue Datei `tests/test_skill_089_cold_audience_formulas.py` gruen.

## Code-Referenzen
- `creative_studio/frameworks.py` (6 Formel-CopyFrameworks, `COLD_AUDIENCE_FORMULAS`,
  `HUMAN_MESSAGING_RULES`/`human_messaging_rules()`, Cold-Sortierung in `match_frameworks`)
- `creative_studio/specs.py` (`human_rule_warnings`, `ABSTRACT_CONSULTANT_TERMS`, `_STAT_OPENER_RE`)
- `tests/test_skill_089_cold_audience_formulas.py` (neu)
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md`
