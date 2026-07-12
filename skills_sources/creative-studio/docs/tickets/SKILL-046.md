# SKILL-046: creative-studio — B-Roll-Timeline-Composition (Series/TransitionSeries)

**Status:** spec
**Erstellt:** 2026-06-24
**MoSCoW:** Should
**Geschaetzter Aufwand:** L
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_reels-video-editing-strategy.md` (§1.6 B-Roll, §3.2 Series/TransitionSeries/OffthreadVideo, §5 Pipeline-Schritt 5, §7 MoSCoW Should)

> [!info] Herkunft (Recherche 2026-06-24)
> B-Roll-Wechsel pro gesprochener Aussage = visueller Beleg + Retention. Remotion bietet dafuer
> `Series`/`TransitionSeries` + `OffthreadVideo` (Clip-Liste mit Frame-Dauern, Crossfades/Slides,
> `premountFor` fuer sauberes Laden). Das heutige Video-Modul hat **keine** B-Roll-Timeline. Dieses Ticket
> baut die Composition, die eine B-Roll-Liste aus der Reel-Spec (SKILL-045) als Timeline rendert.

## Was soll erreicht werden? (Business-Ziel)
Eine B-Roll-Timeline-Composition: aus einer Clip-Liste (Clip, Dauer, Transition) ein durchgehendes 9:16-Video
mit Uebergaengen rendern, unter den Captions (SKILL-043) und dem Audio (SKILL-044). So entstehen
B-Roll-getriebene Reels statt einer statischen Title-Card.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When eine B-Roll-Clip-Liste (Pfad + Frame-Dauer je Clip) uebergeben wird, the system shall
      die Clips als `Series`/`TransitionSeries` nacheinander mit den angegebenen Dauern rendern.
- [ ] **EARS-2:** When zwischen Clips eine Transition (Crossfade/Slide) definiert ist, the system shall sie
      anwenden; ohne Transition shall ein harter Schnitt erfolgen.
- [ ] **EARS-3:** When Clips geladen werden, the system shall `OffthreadVideo` + `premountFor` nutzen, sodass
      kein leerer/schwarzer Frame an den Clip-Grenzen entsteht.
- [ ] **EARS-4:** When ein Clip-Pfad fehlt/nicht ladbar ist, the system shall den Fehler sichtbar melden
      (kein still schwarzer Abschnitt) — Hard-Failure-Hinweis statt Silent-Fake.
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall die
      Clip-Liste ausschliesslich aus der Reel-Spec/Props beziehen — kein hartkodierter Projektwert.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Neue Composition/Komponente `video/src/BRollTimeline.tsx` mit
  `TransitionSeries` + `OffthreadVideo`; die Clip-Liste kommt aus der Reel-Spec (SKILL-045). Captions/Audio
  liegen als Layer darueber (gleiche Composition). Safe-Zone-Padding wie `AdVideo.tsx`.
- **Verworfene Alternative:** Pre-Concat der Clips per ffmpeg vor dem Remotion-Render — verworfen, weil
  Transitions/Layering/Brand dann nicht mehr deterministisch in der Composition steuerbar sind.
- **Betroffene Module:** `video/src/BRollTimeline.tsx` (neu), `video/src/Root.tsx` (Composition-Registrierung),
  konsumiert SKILL-045-Spec. → Architektur-Weiche: keine (ADR n/a).

## Technische Hinweise
- `surface: backend`. **Lizenz-Risiko Remotion** (ab 4 Personen kostenpflichtig, SKILL.md §7) — vor
  Skalierung klaeren. Remotion ist der Finishing-/Compositing-Layer; das **Finden** der besten Momente
  bleibt einem vorgelagerten AI-Clipper (OpusClip/Descript) ueberlassen (§7 Won't), nicht Teil dieses Tickets.
- Voraussetzung: SKILL-045 (Reel-Spec liefert die B-Roll-Liste).

## Code-Referenzen
- `skills_sources/creative-studio/video/src/BRollTimeline.tsx` (neu) — Timeline-Composition.
- `skills_sources/creative-studio/video/src/Root.tsx` — Registrierung.
- Wissensgrundlage: `2026-06-24_reels-video-editing-strategy.md` (§1.6, §3.2, §5, §7 Should).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
