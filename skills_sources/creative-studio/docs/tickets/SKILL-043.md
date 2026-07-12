# SKILL-043: creative-studio — Caption-Renderer-Composition (word-level, Whisper, burned-in)

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Must
**Geschaetzter Aufwand:** L
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_reels-video-editing-strategy.md` (§1.4 Captions, §3.1 Remotion-Captions word-level, §5 Pipeline-Schritt 4, §7 MoSCoW Must)

> [!info] Herkunft (Recherche 2026-06-24)
> ~85 % schauen Reels **ohne Ton** → Captions sind „der ganze Hook", nicht Beiwerk; Viewer mit Captions
> schauen ~80 % haeufiger bis zum Ende. Remotion hat **native Caption-Unterstuetzung** (ab v4.0.216,
> `@remotion/install-whisper-cpp` / `@remotion/openai-whisper`, Caption-Struktur `text/startMs/endMs/
> timestampMs/confidence`). Das heutige `AdVideo.tsx` ist nur eine statische Title-Card — **kein**
> Caption-Renderer. Dieses Ticket baut die word-level Caption-Composition (Hormozi-Stil ueber Props).

> [!note] Abgrenzung zu SKILL-027
> SKILL-027 (Voiceover-Layer) leitet Untertitel **aus dem Skript-Text** ab. Dieses Ticket liefert die
> **word-level, an Whisper-Timestamps ausgerichtete** Caption-Composition (Karaoke-/Word-Reveal). Beide
> ergaenzen sich: SKILL-027 erzeugt den Audio-Track, SKILL-043 rendert die zeitgenauen Captions dazu.

## Was soll erreicht werden? (Business-Ziel)
Eine Remotion-Caption-Komponente, gespeist aus Whisper-Output, die burned-in Word-by-Word-Captions
(Hormozi-Preset: fett, gelbe Keyword-Hervorhebung) ueber der unteren 35 %-Safe-Zone (oberes/mittleres
Drittel) rendert. Stil/Position/Farbe ueber Brand-Props — projektneutral, batchbar.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When eine Caption-Liste (`text/startMs/endMs`-Struktur aus Whisper) uebergeben wird, the
      system shall die Captions **frame-genau an den Timestamps** als Overlay einblenden (1–3 Woerter aktiv).
- [x] **EARS-2:** When Captions gerendert werden, the system shall sie **ueber** der unteren 35 %-Safe-Zone
      (oberes/mittleres Drittel, `SAFE_BOTTOM_PCT` aus der geteilten Safe-Zone-Logik) positionieren — nie im
      unteren Drittel (Reels-UI). Zeilenlaenge ~15–20 Zeichen.
- [x] **EARS-3:** When ein Caption-Stil-Preset (`clean`/`karaoke`/`hormozi`) per Prop gewaehlt wird, the
      system shall Font/Farbe/Keyword-Highlight/Animation entsprechend setzen (Word-by-Word-Highlight im
      Hormozi-Preset).
- [x] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall
      Caption-Farben/Font aus Brand-Props beziehen — kein hartkodierter Brand-/Projektwert in der Komponente.
- [x] **EARS-5:** When keine Caption-Liste uebergeben wird, the system shall das Video weiterhin ohne
      Captions rendern (Layer optional, bestehender Pfad bricht nicht).

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Neue React-Caption-Komponente in `video/src/` (z.B. `Captions.tsx`), die eine
  Caption-Liste als Prop nimmt und per `useCurrentFrame()` + Timestamp-Mapping das aktive Wort hervorhebt.
  Whisper-Transkription (cpp/openai) erzeugt die Caption-JSON **vorgelagert** (CLI-/Helper-Schritt); die
  Composition konsumiert sie nur. Presets als Prop-gesteuerte Style-Objekte. Safe-Zone-Werte aus der
  geteilten `specs.py`-Konvention (gleiche Prozentwerte wie `AdVideo.tsx`).
- **Verworfene Alternative:** Post-burn der Captions per ffmpeg nach dem Render — verworfen, weil Remotion
  Captions als React-Komponenten erlaubt (Stil/Animation per Props, deterministisch, batchbar).
- **Betroffene Module:** `video/src/Captions.tsx` (neu), `video/src/AdVideo.tsx` (Caption-Slot einhaengen),
  `video/src/Root.tsx` (Props), optional `creative_studio/captions.py` (Whisper → Caption-JSON-Helper).

## Technische Hinweise
- `surface: backend` — Remotion-Render headless (kein Web-UI-Verifier noetig; Verifikation via
  `remotion still`/Frame-Vergleich + Caption-JSON-Unit-Test fuer das Timestamp-Mapping).
- **Lizenz-Risiko:** Remotion ist ab 4 Team-Personen kostenpflichtig (SKILL.md §7) — vor Skalierung des
  Video-Moduls klaeren. Hier vermerkt, kein Blocker fuers Bauen.
- Whisper-Helper installiert **nichts** automatisch — Voraussetzung (npm/cpp) dokumentieren.

## Code-Referenzen
- `skills_sources/creative-studio/video/src/Captions.tsx` (neu) — word-level Caption-Komponente.
- `skills_sources/creative-studio/video/src/AdVideo.tsx` — Caption-Slot (additiv).
- `skills_sources/creative-studio/creative_studio/captions.py` (optional, neu) — Whisper → Caption-JSON.
- Wissensgrundlage: `2026-06-24_reels-video-editing-strategy.md` (§1.4, §3.1, §5, §7 Must).

## Ergebnis / Notizen

**Umgesetzt (2026-06-24):**
- Neue Komponente `video/src/Captions.tsx` — word-level Caption-Renderer. Input =
  `CaptionToken[]` (`text/startMs/endMs`, Whisper-kompatibel). `useCurrentFrame()` ->
  ms-Mapping waehlt 1–3 aktive Tokens (`MAX_ACTIVE_TOKENS=3`), highlightet das aktive
  Wort (EARS-1). Position via `captionCenterY = 0.58*height`: klar **ueber** der
  unteren 35 %-Safe-Zone (beginnt bei 65 %), unter der Top-Safe-Zone (14 %); Container
  auf `MAX_LINE_CHARS=20`ch begrenzt (EARS-2). Presets `clean`/`karaoke`/`hormozi` als
  prop-gesteuerte Style-Logik (EARS-3). Farben/Font/Highlight aus Brand-Props, kein
  Projektwert (EARS-4). `tokens` leer/null -> `return null` (EARS-5).
- Eingehaengt in `video/src/AdReel.tsx` (neuer Caption-Slot ueber der Title-Card).
  `AdVideo.tsx` selbst bleibt unveraendert (Title-Card intakt).
- Whisper-Transkription bleibt **vorgelagert** (Input = Transkript-JSON); kein
  Auto-Install im Skill.

**Render-Verify (echt, kein Fake):**
- *Captions-only:* `AdReel`-Render der Beispiel-Spec (8 word-level Tokens) ->
  **Exit 0**, 90 Frames, MP4 539 kB (`tests/artifacts/reel_h1-immo.mp4`).
- *Captions + echtem B-Roll + Musik (Gold):* Render mit 2 Silber-Clips + Musik +
  denselben 8 Tokens -> **Exit 0**, 120 Frames, Gold-MP4 2,7 MB; Captions liegen real
  ueber dem Footage (Scrim sichert Lesbarkeit). Proof-Artefakt:
  `tests/artifacts/reel_h1-immo_broll_proof.mp4` (222 kB).
Voller Skill-Test-Lauf: **180 passed** (vorher 174, +6 SKILL-045).

**Done-Kriterien:** EARS-1..5 erfuellt; echter MP4-Render mit Caption-Tokens gruen
(Exit 0). -> `review`.

**Lizenz-Risiko (Vermerk, kein Blocker):** Remotion ab 4 Team-Personen
kostenpflichtig (SKILL.md §7) — vor Skalierung des Video-Moduls klaeren.
