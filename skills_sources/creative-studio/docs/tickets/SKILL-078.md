# SKILL-078: creative-studio — eigenstaendiges Reel-Format `broll_message`

**Status:** review
**Erstellt:** 2026-07-11
**MoSCoW:** Must
**Geschaetzter Aufwand:** M (neue Remotion-Composition + Spec-Feld + Validierung + Tests)
**surface:** backend
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`
**outcome_metric:** broll_message_ist_eigenes_format (kein zweckentfremdeter talking_head mehr) +
hook_message_pflicht_erzwungen (Spec ohne message/hook -> ReelSpecError) + kein_bestandsbruch

## Kontext / Root-Cause
Der letzte Reel-Build (AgentischesArbeiten, `reel_recruiting_*`/`reel_zahlungslauf_*`) hat die
`talking_head`-Composition zweckentfremdet: B-Roll ueber `speakerSrc`, die eine Message ueber
`hookText` mit `hookWindowSeconds:999` (persistent) + `ctaOutro:false`. Das funktioniert, ist aber
semantisch falsch (kein Sprecher, kein Hook-Fenster, kein CTA-Outro) und fragil. B-Roll + eine
editorial-Serif-Message ist ein **eigenes** Content-Format und soll sauber existieren.

## Was soll erreicht werden?
Ein eigenstaendiges Format `broll_message`: B-Roll-Vollbild-Hintergrund + **Hook oben** + **abholende
Message unten** (editorial Serif, Saskia/Gold-Stil), optional dunkle Box, optional zeitlich abgestufte
Sub-Messages. Kein Talking-Head, kein Akzent-Balken, keine Wort-fuer-Wort-Captions.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Composition]:** Neue Composition `video/src/BrollMessage.tsx` (in `Root.tsx`
      registriert) montiert `broll[]` als Vollbild-9:16-BG (objectFit cover, O-Ton stumm), legt Hook
      (obere Safe-Zone) + Message (unteres Mittel-Drittel ueber der 35 %-UI) editorial-Serif darueber.
      Brand-Tokens via Props, nichts hartkodiert.
- [x] **EARS-2 [Must, Pflicht-Copy]:** `content_type == "broll_message"` ohne `hook` **oder** ohne
      `message` -> `ReelSpecError` (kein stilles textloses Reel). `hook` bleibt Pflicht wie bisher.
      *(Tests `test_broll_message_missing_message_errors` / `_missing_hook_errors`.)*
- [x] **EARS-3 [Must, text_box]:** Spec-Flag `text_box` (`true`/`false`/`"auto"`, Default auto) wird
      zu einem bool `textBox`-Prop aufgeloest (auto = konservativ Box-AN; Vision-QA setzt false auf
      dunkler B-Roll). *(Test `test_broll_message_text_box_flag`.)*
- [x] **EARS-4 [Should, Sub-Messages]:** ist `scenes[]` gesetzt, erscheinen zeitlich abgestufte
      Sub-Messages je Segment (`messageScenes`-Prop). *(Test `test_broll_message_scenes_become_message_scenes`.)*
- [x] **EARS-5 [Must, Composition-Auswahl]:** `reel_spec_to_props` setzt `contentType`; die
      Composition-Id waehlt sich ueber `ReelSpec.composition_id` (`broll_message -> BrollMessage`).
      *(Test `test_broll_message_props_mapping` / `test_talking_head_does_not_require_message`.)*
- [x] **EARS-6 [Must, nicht-brechend]:** `talking_head`/`AdReel` unveraendert; bestehende
      SKILL-045-Suite gruen. TalkingHead wird nicht angefasst (Akzent-Balken bleibt entfernt).

## Loesungs-Skizze
- `video/src/BrollMessage.tsx` (neu), Registrierung + `calculateBrollMessageMetadata` in `Root.tsx`.
- `creative_studio/reel_spec.py`: Felder `message` + `text_box`, `BROLL_MESSAGE`-Konstante,
  `composition_id`-Property, Validierung + Props-Mapping (`hookText`/`message`/`messageScenes`/`textBox`).
- `examples/reel_broll_message.json`, `tests/test_skill_078_broll_message.py` (Aufgabe-A-Teil).
- SKILL.md Abschnitt 4b + Abschnitt-10-Tabelle + Redaktions-Copy-Pflicht-Kasten.

## Test-Ergebnis / Beleg
- **Suite gruen:** `python -m pytest -q` -> **295 passed** (284 + 11 neue SKILL-078-Tests).
- **Live-Render:** zwei echte `broll_message`-Reels fuer AgentischesArbeiten neu gebaut
  (Recruiting/400-Bewerbungen + Zahlungslauf), 1080x1920, Vision-QA bestanden (siehe Ergebnis).

## Code-Referenzen
- `skills_sources/creative-studio/video/src/BrollMessage.tsx`, `video/src/Root.tsx`
- `skills_sources/creative-studio/creative_studio/reel_spec.py`
- `skills_sources/creative-studio/examples/reel_broll_message.json`
- `skills_sources/creative-studio/tests/test_skill_078_broll_message.py`
- `skills_sources/creative-studio/SKILL.md` (Abschnitt 4b/10)
