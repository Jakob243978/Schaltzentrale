# SKILL-040: creative-studio — content_type_warnings()-Validator in specs.py

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Must
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_social-content-types.md` (§3.2 Validatoren-Block, §5 MoSCoW Must)

> [!info] Herkunft (Recherche 2026-06-24)
> Mit der `ContentType`-Ebene (SKILL-039) braucht es einen **Warn-Validator** analog `AdContent.warnings()`:
> er prueft eine konkrete Content-Instanz (Slide-Anzahl, Video-Laenge, On-Screen-Wortzahl) gegen die
> `ContentType`-Constraints und liefert **Warnungen, keine harte Sperre** (Mensch-im-Loop, wie der gesamte
> Skill). Nutzt die bestehende `frameworks.hook_fits_onscreen()` — **keine** Doppel-Implementierung.

## Was soll erreicht werden? (Business-Ziel)
Eine Funktion `content_type_warnings(content_type, *, slides=None, seconds=None, onscreen_texts=None)` in
`specs.py`, die pro Constraint-Verstoss **genau eine sachliche Warnung** liefert: Slide-Anzahl ausserhalb
`min_slides`/`max_slides`, Video-Laenge ausserhalb `min_seconds`/`max_seconds`, On-Screen-Text ueber dem
Wortlimit. So sieht ein Generator/Agent vor dem Rendern, ob die geplante Variante zum Content-Typ passt.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein Carousel-/Multi-Image-`ContentType` mit Slide-Anzahl ausserhalb
      `min_slides..max_slides` geprueft wird, the system shall genau eine Warnung mit Soll-Range + Ist-Wert
      liefern. → Tests `test_warn_slides_below_min`, `test_warn_slides_above_max`.
- [ ] **EARS-2:** When ein Video-`ContentType` mit `seconds` ausserhalb `min_seconds..max_seconds` geprueft
      wird, the system shall genau eine Warnung mit Sweetspot-Range + Ist-Wert liefern.
      → Test `test_warn_video_length_out_of_range`.
- [ ] **EARS-3:** When ein On-Screen-Text die `onscreen_word_limit`-Grenze ueberschreitet, the system shall
      ueber `frameworks.hook_fits_onscreen()` (kein Doppel) genau eine Warnung pro verletzendem Text liefern.
      → Test `test_warn_onscreen_word_limit`.
- [ ] **EARS-4:** When eine Content-Instanz **alle** Constraints einhaelt, the system shall eine **leere**
      Warn-Liste liefern (kein Fehlalarm). → Test `test_no_warnings_when_within_constraints`.
- [ ] **EARS-5:** When ein Feld fuer den jeweiligen `medium` `None` ist (z.B. Slide-Felder bei einem
      Video-Typ), the system shall diese Pruefung ueberspringen statt zu crashen. → Test `test_irrelevant_fields_skipped`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Reine Warn-Funktion (Liste von Strings) analog `compliance_warnings()` /
  `AdContent.warnings()`. Delegiert die On-Screen-Pruefung an `frameworks.hook_fits_onscreen()`. Keine
  Sperre, keine Exceptions bei Constraint-Verstoss (nur bei echtem Programmierfehler).
- **Verworfene Alternative:** Harte Validierung mit Raise — verworfen, weil der Skill konsequent
  Mensch-im-Loop arbeitet (alle Guards sind Warnungen).
- **Betroffene Module:** `specs.py` (neue Funktion), `frameworks.py` (read-only Nutzung), neue Testdatei.

## Technische Hinweise
- Signatur-Vorschlag: `content_type_warnings(ct: ContentType, *, slides: int | None = None,
  seconds: float | None = None, onscreen_texts: list[str] | None = None) -> list[str]`.
- Voraussetzung: SKILL-039 (liefert `ContentType`/`CONTENT_TYPES`).
- Import von `frameworks` in `specs` vermeiden, falls Zyklus-Gefahr — stattdessen `onscreen_word_limit`
  lokal gegen `len(text.split())` pruefen UND in einem Test gegen `frameworks.hook_fits_onscreen()`
  Aequivalenz zeigen. (Implementer entscheidet die zyklenfreie Variante; Verhalten bleibt identisch.)

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — `content_type_warnings()` (Block `# === SKILL-040 ===`).
- `skills_sources/creative-studio/creative_studio/frameworks.py` — `hook_fits_onscreen()` (read-only).
- `skills_sources/creative-studio/tests/test_skill_040_content_type_warnings.py` (neu).
- Wissensgrundlage: `2026-06-24_social-content-types.md` (§3.2 Validatoren, §5 Must).

## Ergebnis / Notizen

**Umgesetzt 2026-06-24 (Status -> review, Verify-Gate offen).**

In `creative_studio/specs.py` (Block `# === SKILL-040 ===`) ergaenzt:
- `content_type_warnings(ct, *, slides=None, seconds=None, onscreen_texts=None) -> list[str]`
  (genau die vorgeschlagene Signatur). Pro Constraint-Verstoss genau eine Warnung.
- On-Screen-Pruefung delegiert an `frameworks.hook_fits_onscreen()` (lokaler Import
  in der Funktion -> kein Modul-Level-Zyklus, kein Doppel).

Tests: `tests/test_skill_039_content_types.py` (Abschnitt SKILL-040).

Done-Kriterien (EARS):
- [x] EARS-1: Slide-Anzahl out-of-range -> `test_warn_slides_below_min`, `test_warn_slides_above_max`.
- [x] EARS-2: Video-Laenge out-of-range -> `test_warn_video_length_out_of_range`.
- [x] EARS-3: On-Screen-Wortlimit via `hook_fits_onscreen()` -> `test_warn_onscreen_word_limit`
      (inkl. Aequivalenz-Assert gegen die Helper-Funktion).
- [x] EARS-4: alles konform -> leere Liste -> `test_no_warnings_when_within_constraints`.
- [x] EARS-5: irrelevante None-Felder uebersprungen statt Crash -> `test_irrelevant_fields_skipped`.

pytest gesamt: **158 passed**.
