# SKILL-056: creative-studio — Talking-Head-Composition („Founder spricht")

**Status:** review
**Erstellt:** 2026-06-25
**MoSCoW:** Must
**Geschaetzter Aufwand:** L
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_reel-design-critique-content-types.md` (§3 Talking-Head-Footage) + `2026-06-24_social-content-types.md` (§2 `talking_head`) + `2026-06-24_reels-video-editing-strategy.md` (§1.1 Hook, §5 Voiceover-Pipeline)

> [!info] Herkunft (Jakob-Wunsch 2026-06-25 + Footage-Befund)
> Jakob will einen weiteren Content-Typ: einen **„wo ich spreche"** (Talking-Head / Founder-Speaks).
> Footage-Sichtung der Bronze-Clips bestätigt: **vorhanden** — `Video 07.03.26, 15 46 40.mov` (2:32 min)
> zeigt Jakob frontal sitzend, **Lavalier-Mikrofon sichtbar**, sprechend. Mehrere ähnliche Sprech-Clips
> existieren. Der `talking_head`-CONTENT_TYPE ist in `specs.py` (SKILL-042) bereits **deklarativ**
> vorhanden (medium=video, 20–45 s, Hook<3s, Caption Pflicht) — es fehlt die **Composition**, die ihn
> tatsächlich rendert.

> [!note] Abgrenzung
> SKILL-042 hat den `talking_head`-CONTENT_TYPE als Daten-/Validierungs-Eintrag gebaut (kein Render).
> SKILL-044 hat `AdReel` mit B-Roll-Series + Audio. Dieses Ticket baut die **Talking-Head-Variante**:
> Sprecher-Clip als **durchgängiger Vordergrund-Layer** (statt B-Roll-Schnittfolge), 9:16-Reframe-Crop,
> Captions (SKILL-043/055), Brand-Lower-Third (SKILL-047), Hook-Fenster < 3 s, CTA-Outro. Es ersetzt
> weder AdReel noch B-Roll, sondern ergänzt einen typisierten Render-Pfad.

## Was soll erreicht werden? (Business-Ziel)
Eine Remotion-Composition `TalkingHead`, die aus **einem On-Camera-Sprech-Clip** + optionalem Transkript
ein markenkonsistentes 9:16-Founder-Reel baut: korrektes Framing/Crop der Sprecher-Footage, burned-in
word-level Captions, Brand-Lower-Third (Name/Claim), Hook-Promise im Frame < 3 s, CTA-Outro. Input-Bedarf
klar dokumentiert. Andockung an den `talking_head`-CONTENT_TYPE (Längen-/Hook-Validierung).

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein On-Camera-Sprech-Clip (`speakerSrc`) übergeben wird, the system shall ihn als
      **durchgängigen Vordergrund-Layer** 9:16-formatfüllend (`objectFit: cover`, optional `objectPosition`
      für Reframe) rendern, mit Audio des Clips als Tonspur. → Test `test_talking_head_speaker_layer`.
- [ ] **EARS-2:** When ein Caption-Track vorliegt, the system shall die word-level Captions (SKILL-043/055,
      inkl. Pill/Stroke-Lesbarkeit) über dem Sprecher einblenden; fehlt der Track, rendert das Reel **ohne**
      Captions weiter (Layer optional). → Tests `test_talking_head_captions`, `test_talking_head_no_captions`.
- [ ] **EARS-3:** When ein Brand-Lower-Third (Name/Claim) gesetzt ist, the system shall es Safe-Zone-konform
      (über der unteren 35 %-Zone) animiert einblenden; Hook-Promise-Text muss im Frame **< 3 s** stehen
      (Hook-Fenster aus `talking_head`-CONTENT_TYPE). → Test `test_talking_head_hook_window_and_lowerthird`.
- [ ] **EARS-4:** When ein CTA-Outro aktiviert ist, the system shall am Ende einen 1–2 s Brand-CTA-Bumper
      (bestehende `AdVideo`-Mechanik) anhängen. → Test `test_talking_head_cta_outro`.
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten läuft, the system shall Footage-
      Pfad, Brand-Tokens, Hook-/CTA-Text und Lower-Third ausschließlich aus Props/Spec beziehen — kein
      hartkodierter Projektwert. → Test `test_talking_head_project_neutral`.
- [ ] **EARS-6:** When eine Talking-Head-Reel-Spec gegen den `talking_head`-CONTENT_TYPE geprüft wird, the
      system shall `content_type_warnings()` (Länge 20–45 s, Hook<3s) nutzen — kein Parallel-Validator.
      → Test `test_talking_head_content_type_validation`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Neue Composition `video/src/TalkingHead.tsx` — `OffthreadVideo` (speakerSrc,
  **nicht** gemutet, da O-Ton), darüber `Captions` (SKILL-043/055), `LowerThird` (SKILL-047), optional
  Hook-Overlay (erste < 3 s) + CTA-Outro-Sequence (`AdVideo`-Bumper am Ende). Reframe via `objectPosition`-
  Prop. Registrierung in `Root.tsx` als eigene `Composition` (id `TalkingHead`), Dauer dynamisch aus
  Clip-/Audio-Länge (`calculateMetadata` analog SKILL-044). Reel-Spec (SKILL-045) bekommt additiv
  `content_type: "talking_head"` + `speaker`-Feld; Loader reicht es in die Props.
- **Verworfene Alternative:** Talking-Head als Sonderfall in `AdReel` (broll mit einem Clip) — verworfen,
  weil B-Roll gemutet/geschnitten ist und Talking-Head O-Ton + durchgängigen Speaker-Layer + eigenes
  Framing braucht; eigener typisierter Pfad ist klarer und an den CONTENT_TYPE andockbar.
- **Betroffene Module:** `video/src/TalkingHead.tsx` (neu), `video/src/Root.tsx` (Composition + Metadata),
  `creative_studio/reel_spec.py` (additiv `content_type`/`speaker`), `creative_studio/specs.py` (read-only
  `talking_head`-CONTENT_TYPE + `content_type_warnings`). → Architektur-Weiche: keine (ADR n/a).

## Technische Hinweise
- `surface: backend` — Remotion-Render headless. Verifikation: echter End-to-End-Render mit dem realen
  Bronze-Sprech-Clip (`Video 07.03.26, 15 46 40.mov`, ggf. 20–45-s-Ausschnitt) → Exit 0 + Gold-MP4.
- **Input-Bedarf (dokumentieren in SKILL.md):** (1) On-Camera-Speaking-Clip (Pflicht); (2) Transkript-JSON
  für word-level Captions (optional, **vorgelagert** via Whisper — kein Auto-Install); (3) Hook-/CTA-Text +
  Lower-Third-Name aus der Spec. Clip-Auswahl (bester 20–45-s-Ausschnitt) bleibt vorgelagert (AI-Clipper).
- **KI-Disclosure:** Bei echtem O-Ton/echter Person **keine** KI-Disclosure nötig; nur falls Voice-Clone/
  KI-Avatar → SKILL-028-Gate (im CONTENT_TYPE bereits vermerkt).
- **Lizenz-Risiko Remotion** (ab 4 Personen, SKILL.md §7).

## Code-Referenzen
- `skills_sources/creative-studio/video/src/TalkingHead.tsx` (neu) — Speaker-Layer + Captions + Lower-Third + Hook/CTA.
- `skills_sources/creative-studio/video/src/Root.tsx` — `TalkingHead`-Composition + dyn. Dauer.
- `skills_sources/creative-studio/creative_studio/reel_spec.py` — additiv `content_type`/`speaker`.
- `skills_sources/creative-studio/creative_studio/specs.py` — `talking_head`-CONTENT_TYPE (read-only, SKILL-042).
- `skills_sources/creative-studio/tests/test_skill_056_talking_head.py` (neu).
- Wissensgrundlage: `2026-06-25_reel-design-critique-content-types.md` (§3), `2026-06-24_social-content-types.md` (§2 talking_head).

## Ergebnis / Notizen
**Umgesetzt 2026-06-25** (Implementer-Pass, End-to-End-Render mit echtem Bronze-Clip).

- `video/src/TalkingHead.tsx` neu: durchgaengiger Speaker-Layer via `OffthreadVideo`
  (objectFit:cover, `objectPosition`-Reframe, **NICHT gemutet** → O-Ton); darueber die
  SKILL-055-Pill-`Captions` (optional — fehlt der Track, rendert es weiter); Brand-Lower-Third
  (Name-Pill + Claim, ueber unterer 35 %-Zone, spring-in); Hook-Promise im Fenster < 3 s
  (`hookWindowSeconds`, Default 3.0); CTA-Outro-Bumper (`Sequence` am Ende, Brand-CTA).
- `video/src/Root.tsx`: `TalkingHead`-Composition registriert, Dauer dynamisch via
  `calculateTalkingHeadMetadata` (`@remotion/media-utils getVideoMetadata` der Speaker-Clip-Laenge,
  Fallback Captions/180).
- `creative_studio/reel_spec.py`: additiv `content_type` + `speaker`(`SpeakerSpec`:
  `src`/`objectPosition`); `speaker.src` Pflicht wenn speaker-Block gesetzt; Props-Mapping
  reicht `speakerSrc`/`speakerObjectPosition`/`contentType` durch.
- `content_type_warnings()` (specs.py, SKILL-040) wird fuer die Laengen-/Hook-Validierung genutzt
  (read-only, kein Parallel-Validator).

**Footage:** Bronze `Video 07.03.26, 15 46 40.mov` (4K HEVC) → gebuendeltes ffmpeg, 18s-Ausschnitt,
9:16-Crop (956×1700 @ y635, Face in obere Bildmitte gehoben) → Silber
`…/Content Lake/Silber/talkinghead_founder_9x16.mp4` (1080×1920, 30 fps, **mit O-Ton**), gestaget
nach `video/public/assets/talkinghead_founder.mp4` (git-ignored via `video/.gitignore`).

**Render-Beleg (echt):** `…/Content Lake/Gold/reel_talkinghead_proof.mp4` (Exit 0, 14,66s,
Video+Audio). Frames `tests/artifacts/th_proof_{1.0,7.5,14.5}s.png` + `th_proof_overview.png`
belegen: Speaker full-frame, Pill-Captions, Hook<3s ("So gewinnst du 3 Stunden…"), Lower-Third
("Jakob Sebov"), CTA-Outro ("Auf die Warteliste"). Klein-Proof `th_proof.mp4` (362 KB, mit Ton).

**Tests:** `tests/test_skill_056_talking_head.py` (8 Tests, EARS-1..6 + Spec-Guard).

**Bewusst manuell/offen:** Caption-Timing der Talking-Head-Spec ist hartkodiert (Design-Proof,
volle Whisper-Integration = SKILL-043/056-Spec, nicht Voraussetzung). Captions liegen mittig
(54 %) und ueberlagern bei tightem Crop das Gesicht — fuer den Design-Proof toleriert; ein
optionaler caption-Höhen-Prop fuer Talking-Head waere ein Folge-Refinement. 404-Logzeilen fuer
die staticFile-URL im Render-Log waren nicht-fatal (Asset lud sichtbar korrekt).
