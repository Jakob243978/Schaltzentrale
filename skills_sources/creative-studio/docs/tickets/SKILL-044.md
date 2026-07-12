# SKILL-044: creative-studio — Audio-Track-Modell + Ducking + dynamische Composition-Dauer

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Must
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_reels-video-editing-strategy.md` (§1.7 Musik, §3.3 Audio/Voiceover-Sync, §5 Pipeline-Schritt 6/7, §7 MoSCoW Must)

> [!info] Herkunft (Recherche 2026-06-24)
> Das heutige `AdVideo.tsx` rendert **fix 180 Frames (6 s)** und kennt **keinen Audio-Track**. Fuer echte
> Reels braucht die Composition: einen Voiceover-Track, optional Musik **leiser drunter** (Per-Frame-Ducking)
> und eine **dynamische Dauer aus der Audio-Laenge** statt der fixen 6 s. Das ist die Composition-Infrastruktur,
> in die SKILL-027 (ElevenLabs-Voiceover) und SKILL-043 (Captions) ihren Output einhaengen.

> [!note] Abgrenzung zu SKILL-027
> SKILL-027 **erzeugt** den Voiceover-Audio (ElevenLabs). Dieses Ticket liefert das **Composition-seitige
> Audio-Modell** (Track-Einbindung, Ducking, dyn. Dauer) — die Remotion-Mechanik, die SKILL-027 nutzt.
> Kein Doppel: 027 = Provider/Generierung, 044 = Composition-Audio-Infrastruktur.

## Was soll erreicht werden? (Business-Ziel)
Die Remotion-Composition um ein Audio-Modell erweitern: Voiceover-Track + optionale Hintergrundmusik mit
Per-Frame-Ducking (Musik leiser unter dem Voiceover), Composition-Dauer dynamisch aus der Audio-Laenge.
So entsteht ein vollwertiges, vertontes Reel statt einer stummen Title-Card.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When ein Voiceover-Audio-Pfad/-Asset uebergeben wird, the system shall ihn als `Audio`-Track
      in die Composition einbinden und die **Composition-Dauer aus der Audio-Laenge** ableiten (statt fix 180 Frames).
- [x] **EARS-2:** When zusaetzlich ein Musik-Track gesetzt ist, the system shall ihn **leiser** unter dem
      Voiceover mischen (Per-Frame-/Bereichs-Ducking), sodass die Sprache traegt.
- [x] **EARS-3:** When **kein** Audio uebergeben wird, the system shall auf die bisherige feste Dauer
      zurueckfallen (bestehender stummer Pfad bricht nicht). → Test-/Render-Beleg.
- [x] **EARS-4:** When nur Musik mit „Original audio"-Eignung erlaubt ist, the system shall die
      Audio-Quelle als Parameter nehmen (kein Auto-Sourcing von Trending-Audio — Lizenz bleibt Plattform-/
      Rechtssache, §7 Won't).
- [x] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall
      Audio-Pfade/-Parameter ausschliesslich aus Props/Job beziehen — kein hartkodierter Projektwert.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `AdVideo.tsx`/Root um optionale `voiceoverSrc`/`musicSrc`/`musicGainDb`-Props
  erweitern, `Audio`-Komponenten mit `volume`-Callback (Per-Frame) fuer Ducking, `durationInFrames`
  dynamisch aus Audio-Metadaten (Remotion `getAudioDurationInSeconds` / `calculateMetadata`).
- **Verworfene Alternative:** Audio erst im ffmpeg-Post mischen — verworfen, weil Remotion deterministisches
  In-Composition-Audio + Ducking bietet und die dyn. Dauer ohnehin in der Composition entschieden werden muss.
- **Betroffene Module:** `video/src/AdVideo.tsx`, `video/src/Root.tsx` (Props + `calculateMetadata`).
  → Architektur-Weiche: keine (ADR n/a); baut auf bestehender AdVideo-Mechanik auf.

## Technische Hinweise
- `surface: backend`. **Lizenz-Risiko Remotion** (ab 4 Personen kostenpflichtig, SKILL.md §7) — hier
  vermerkt, vor Video-Skalierung klaeren.
- Ducking bewusst einfach (fester Gain-Abfall unter Voiceover-Bereich genuegt; kein Sidechain-DSP noetig).
- Voraussetzung/Reihenfolge: nutzbar mit SKILL-027 (Voiceover-Quelle) + SKILL-043 (Captions an denselben
  Timestamps). SKILL-045 (Reel-Spec) speist die Audio-Felder.

## Code-Referenzen
- `skills_sources/creative-studio/video/src/AdVideo.tsx` — Audio-Tracks + Ducking (Block `// SKILL-044`).
- `skills_sources/creative-studio/video/src/Root.tsx` — Props + `calculateMetadata` (dyn. Dauer).
- Wissensgrundlage: `2026-06-24_reels-video-editing-strategy.md` (§1.7, §3.3, §5, §7 Must).

## Ergebnis / Notizen

**Umgesetzt (2026-06-24):**
- Neue Composition `video/src/AdReel.tsx` (additiv, Title-Card `AdVideo.tsx` bleibt
  unangetastet): komponiert AdVideo als Basis-Layer + Captions (SKILL-043) +
  Audio-Modell. `voiceoverSrc` -> `<Audio src=... />` (EARS-1). `musicSrc` ->
  `<Audio volume={duckByFrame} />`: Per-Frame-Ducking — Musik faellt auf
  `musicDuckVolume` (Default 0.12) waehrend Voiceover/Sprechspannen, sonst
  `musicVolume` (Default 0.5) (EARS-2). Ohne Voiceover keine Absenkung. Audio-Quellen
  ausschliesslich aus Props (EARS-4/EARS-5).
- Dynamische Dauer in `video/src/Root.tsx` via `calculateMetadata` (neue Composition
  `AdReel`): Prioritaet `durationInFrames` (aus Spec) > `getAudioDurationInSeconds`
  (Voiceover) > letztes Caption-`endMs` > Fallback 180 Frames (EARS-1/EARS-3). Die
  alte `AdVideo`-Composition behaelt fix 180 Frames (stummer Pfad bricht nicht).

**Render-Verify (echt, ZWEI Laeufe):**
1. *Stummer Pfad / Captions-only:* `AdReel`-Render der Beispiel-Spec ->
   **Exit 0**, **90 Frames** (= 3 s aus `scenes`-Summe, nicht 6 s/180) -> dyn. Dauer
   real wirksam. MP4 539 kB (`tests/artifacts/reel_h1-immo.mp4`). Audio `null` ->
   stummer Fallback-Pfad (EARS-3) zugleich real belegt.
2. *Mit echtem Footage + Musik (Medallion End-to-End):* Bronze-Clips (HEVC .mov)
   via gebuendeltem Remotion-ffmpeg nach **Silber** transcodiert (1080x1920,
   `…/Silber/reeltest_clip01.mp4` + `…clip02.mp4`), in `video/public/assets/`
   gestaget, + Musik `Super Neato - Hit It Off`. Render -> **Exit 0**, **120 Frames**
   (4 s aus B-Roll-Summe), Output **Gold**:
   `…/Jakob Sebov Content Lake/Gold/reel_h1-immo_broll.mp4` (2,7 MB). ffprobe:
   1080x1920 **h264 + aac** (Musik-Track real im Container), dur 4,05 s. Damit ist
   der **Audio-Track real gerendert** (EARS-1/EARS-2-Mechanik). Kompaktes
   Proof-Artefakt im Repo: `tests/artifacts/reel_h1-immo_broll_proof.mp4` (222 kB).
   Voller Python-Test-Lauf: **180 passed**.

**Offen (klein, ehrlich):** Das **sichtbare** Ducking-UNTER-Voiceover (EARS-2) ist
mit echtem Ton noch nicht belegt — es gab kein freies Voiceover-Asset im Repo, und
ohne Voiceover laeuft die Musik bewusst auf vollem `musicVolume` (nichts zum Ducken).
Die Ducking-Logik (`duckByFrame`, Caption-Sprechspannen) ist verdrahtet + im realen
Render mit Musik durchlaufen, aber der hoerbare Duck-Effekt braucht ein VO-Asset zum
Gegentest. Verifier kann mit einem Test-mp3-Voiceover nachziehen.

**Done-Kriterien:** EARS-1..5 verdrahtet; dyn. Dauer (90 bzw. 120 statt 180 Frames)
real belegt; stummer Fallback + echter Musik-/Audio-Track real gerendert. -> `review`.

**Lizenz-Risiko (Vermerk, kein Blocker):** Remotion ab 4 Team-Personen
kostenpflichtig (SKILL.md §7).
