# SKILL-060: creative-studio — Whisper-Transkriptions-Stufe (word-level → Reel-Spec-Captions)

**Status:** review
**Erstellt:** 2026-06-25
**MoSCoW:** Must
**Geschaetzter Aufwand:** M
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_content-aware-reel-pipeline.md` (§1 Ist-Beleg, §2 STT-Verfuegbarkeit, §3.1 Transkript-getriebene Captions) + `2026-06-24_reels-video-editing-strategy.md` (§5 Voiceover-Pipeline, §3.1 Captions)

> [!info] Herkunft (Jakob-Kritik 2026-06-25)
> Jakob zu den gerenderten Reels: „Absolut schlecht. **Kein Kontext zum Transkript.** Gar kein
> Verstaendnis, was wir dort machen." Belegter Ist-Zustand: die `captions` der Reel-Spec waren
> **handgeschriebene Slogans mit erfundenen Timings** (`examples/reel_*.json`: runde 0/350/800-ms-Werte,
> Slogan-Text statt O-Ton). Der in `Captions.tsx` Z.15 referenzierte `creative_studio/captions.py`
> **existierte nicht**; `grep whisper|transcribe|stt` traf nur Kommentare. Es fehlte die gesamte
> Transkriptions-Stufe. STT war lokal verfuegbar (`faster-whisper 1.2.1` + Modelle gecacht), nur nie
> verdrahtet.

> [!note] Abgrenzung
> SKILL-043 hat den Caption-**Renderer** gebaut (konsumiert Tokens). SKILL-055 hat das Caption-
> **Design** verbessert (Pill/Stroke). Dieses Ticket baut die vorgelagerte **Quelle** der Tokens:
> aus dem echten Audio statt aus der Hand. Es aendert den Renderer NICHT.

## Was soll erreicht werden? (Business-Ziel)
Eine Skill-Stufe, die aus Footage (.mov/.mp4) ein **word-level Transkript** erzeugt, dessen Tokens
1:1 das `{text,startMs,endMs}`-Caption-Schema speisen — sodass Reel-Captions ab jetzt das
**tatsaechlich Gesprochene** zeigen statt eines hartkodierten Slogans. Smallest viable, lokal/offline.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When Footage uebergeben wird, the system shall die Tonspur via gebuendeltem
      Remotion-ffmpeg als 16 kHz mono WAV extrahieren (optional `--start/--duration`-Ausschnitt),
      ohne globalen ffmpeg-Install. → Test `test_extract_audio_missing_video_raises` + Live-Beleg.
- [x] **EARS-2:** When eine WAV transkribiert wird, the system shall via faster-whisper
      (`word_timestamps=True`) eine word-level Token-Liste mit `text/startMs/endMs/p` liefern.
      → Live-Beleg (DE, 25 Woerter) + `test_faster_whisper_importable`.
- [x] **EARS-3:** When ein Transkript entsteht, the system shall es als `{text,startMs,endMs}`
      Reel-Spec-`captions[]` ausgeben (Renderer-kompatibel, kein Renderer-Umbau).
      → Tests `test_wordtoken_to_caption_schema`, `test_transcript_to_dict_and_captions`.
- [x] **EARS-4:** When kein gesprochenes Wort erkannt wird, the system shall hart abbrechen
      (`TranscribeError`) statt ein leeres/erfundenes Reel zu erzeugen (`feedback_no_silent_fakes`).
      → in `transcribe_wav` implementiert.
- [x] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall
      Sprache/Modell/Pfade als Parameter beziehen — kein hartkodierter Projektwert.
      → Test `test_resolve_ffmpeg_prefers_explicit`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `creative_studio/transcribe.py` — `extract_audio()` (ffmpeg-Resolver:
  explizit > gebuendeltes Remotion-ffmpeg > PATH), `transcribe_wav()` (lazy `faster_whisper`-Import),
  `transcribe_video()` (End-to-End mit tempdir-WAV). `Transcript`/`WordToken`-Dataclasses mit
  `to_dict()`/`to_captions()`. CLI `python -m creative_studio.transcribe`.
- **Verworfene Alternative:** `@remotion/install-whisper-cpp` (Node) — verworfen, weil faster-whisper
  bereits lokal installiert + Modelle gecacht waren (kein Setup-Overhead); Remotion-cpp bleibt als
  alternativer Weg dokumentiert.
- **Betroffene Module:** `creative_studio/transcribe.py` (neu), `requirements.txt` (faster-whisper),
  `SKILL.md` §11/§11a. → Architektur-Weiche: keine (ADR n/a).

## Technische Hinweise
- `surface: backend`. Modell-Default `small` (~480 MB, offline gecacht). Audio via gebuendeltem ffmpeg.
- Prereq dokumentiert (kein Blocker): `pip install faster-whisper`. Hinweis auch fuer Image-Tooling-
  Ticket TICKET-160 (AgentischesArbeiten) hinterlegen.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/transcribe.py` (neu).
- `skills_sources/creative-studio/tests/test_skill_060_transcribe.py` (neu).
- `skills_sources/creative-studio/requirements.txt`, `SKILL.md` §11.

## Ergebnis / Notizen
**Umgesetzt 2026-06-25** (Implementer-Pass, End-to-End-Beleg mit echtem Bronze-Clip).

- `transcribe.py` neu: Audio-Extraktion (gebuendeltes Remotion-ffmpeg, 16 kHz mono) +
  faster-whisper word-level. `TranscribeError` bei fehlendem Video / leerem Transkript.
- **Live-Beleg:** Bronze `Video 07.03.26, 15 46 40.mov` (4K HEVC, AAC) → 20-s-Audio →
  faster-whisper `small` (DE, lang_prob 1.0, **25 Woerter**, 7,4 s) → Transkript:
  „Die meisten Gastgeber wissen gar nicht, wie viele Nachrichten sie bekommen. Ich habe das
  mal bei uns gemessen, wir haben 16 Ferienwohnungen … 150 Nachrichten." Timings krumm/audio-
  gebunden (1800-2180, 2560-3100 …) — eindeutig NICHT die alten Slogan-Timings.
- **Vorher/Nachher:** alt = hartkodiert „3 / Stunden / pro / Woche / zurueck / ohne / neues / Tool"
  (0/350/800/…); neu = echtes gesprochenes Wort aus dem Clip.
- **Tests:** `tests/test_skill_060_transcribe.py` (5; Live-STT-Test skip-bar). Suite 211 passed.

**Bewusst offen:** Karaoke-genaue Wortgrenzen (wav2vec2) = SKILL-062 (faster-whisper-Timestamps sind
fuer Pill-Captions ausreichend, fuer harten Karaoke-Sync ist Alignment besser).
