# SKILL-087: creative-studio — Gedankenstriche (Em-/En-Dash) in Copy verbieten

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (Validator + Flow-Einhaengung + SKILL.md + Template-Fixes + Tests)
**surface:** backend
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** copy_ohne_em_en_dash (jede generierte/verwendete Copy) +
validator_meldet_position + hyphen_minus_bleibt_erlaubt + kein_bestandsbruch

## Kontext / Root-Cause
Em-Dash (—, U+2014) und En-Dash (–, U+2013) wirken in Ad-/Reel-Copy nach
KI/unnatuerlich und sollen in authentischer Copy (Hook, Body, Subline, Eyebrow,
CTA, Captions) nicht vorkommen. Bisher gab es dafuer weder eine dokumentierte
Anti-Liste-Regel noch einen Validator. Zudem trugen drei Hook-Templates in
`frameworks.py` selbst einen Em-Dash (`give_me_x`, `specific_number`,
`friction_statement`) und ein illustratives Copy-Beispiel im `mindset_shift`-
`best_for`. Live-Lesson: KI-Copy verraet sich am haeufigsten ueber Gedankenstriche.

## Was soll erreicht werden?
Jede generierte/verwendete Copy ist gedankenstrichfrei. Ein Validator findet — und –
(mit Position) und wird — als Warnung (Mensch-im-Loop, konsistent mit den anderen
Copy-Checks) — in den Copy-Vorpruef-Flow von Bild UND Reel eingehaengt. Der normale
Bindestrich/Hyphen-Minus (-, U+002D) in Komposita ("Kurzzeit-Vermieter") bleibt
erlaubt. Bestandsverhalten bricht nicht.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Validator]:** `specs.check_no_emdash(text)` liefert je Em-/En-Dash
      (und optisch gleichen Varianten ‒/―/−) eine `DashViolation` mit Zeichen, Name und
      0-basierter Position. *(Tests `test_check_no_emdash_*`.)*
- [x] **EARS-2 [Must, Gegenprobe]:** Normaler Bindestrich (-, U+002D) in Komposita loest
      KEINE Meldung aus; leerer/None-Text -> leere Liste.
      *(Tests `test_check_no_emdash_erlaubt_normalen_bindestrich`, `..._leer_und_none`.)*
- [x] **EARS-3 [Must, Warn-Wrapper]:** `specs.dash_warnings(text)` liefert eine Warnung je
      Fund mit Ersatz-/Erlaubt-Hinweis — reine Warnung, keine Sperre (analog
      `compliance_warnings`). *(Tests `test_dash_warnings_*`.)*
- [x] **EARS-4 [Must, Bild-Flow]:** `AdContent.warnings()` haengt `dash_warnings` ueber
      Eyebrow/Headline/Subline/CTA ein; saubere Copy erzeugt keine Dash-Warnung.
      *(Tests `test_adcontent_warnings_*`.)*
- [x] **EARS-5 [Must, Reel-Flow]:** `content.content_structure_warnings()` prueft Reel-Copy
      (hook/hook_accent/eyebrow/subline/cta + Captions) auf lange Striche.
      *(Tests `test_content_structure_warnings_*`.)*
- [x] **EARS-6 [Must, Bestand dashfrei]:** Alle Hook- und Framework-Templates sind
      gedankenstrichfrei; ein Beispiel-Copy-Durchlauf (gefuellte Templates -> AdContent)
      loest keine Dash-Warnung aus; ganze Suite gruen.
      *(Tests `test_alle_*_templates_sind_dashfrei`, `test_beispiel_copy_durchlauf_ist_dashfrei`.)*

## Loesungs-Skizze
- `specs.py`: `FORBIDDEN_DASHES`, `DashViolation`, `check_no_emdash()`, `dash_warnings()`;
  Einhaengung in `AdContent.warnings()`.
- `content.py`: `dash_warnings` in `content_structure_warnings()`; Prompt-Regel in
  `build_analysis_prompt()` (Claude soll in hook/subline/cta keine Gedankenstriche setzen).
- `frameworks.py`: 3 Hook-Templates + 1 `best_for`-Beispiel gedankenstrichfrei
  (Em-Dash -> Komma / Punkt / Doppelpunkt).
- `SKILL.md`: Copy-Anti-Liste-Callout (Gedankenstriche TABU, Hyphen-Minus erlaubt) +
  Bullet in Abschnitt 5 (Standards); illustratives Matrix-Beispiel entschaerft.
- `tests/test_skill_087_no_emdash.py`.

## Test-Ergebnis / Beleg
- **Suite gruen:** `python -m pytest tests/ -q` -> siehe Verify-Pass.
- Validator meldet z.B. `Gedankenstrich-Verstoss: Em-Dash (—) an Position 20 — ...`.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` (`check_no_emdash`, `dash_warnings`, `AdContent.warnings`)
- `skills_sources/creative-studio/creative_studio/content.py` (`content_structure_warnings`, `build_analysis_prompt`)
- `skills_sources/creative-studio/creative_studio/frameworks.py` (Hook-/Framework-Templates)
- `skills_sources/creative-studio/SKILL.md` (Copy-Anti-Liste, Abschnitt 4d/5)
- `skills_sources/creative-studio/tests/test_skill_087_no_emdash.py`
