# SKILL-062: creative-studio — WhisperX-Alignment-Pfad (Karaoke-genaue Wortgrenzen, optional)

**Status:** spec
**Erstellt:** 2026-06-25
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_content-aware-reel-pipeline.md` (§3.1 Word-level/WhisperX, §5 Tooling lokal/API)

> [!info] Herkunft
> faster-whisper (SKILL-060) liefert word-level Timestamps, die fuer Pill-Captions ausreichen.
> Fuer **harten Karaoke-Sync** (Wort sitzt aufs Audio-Boundary) ist Whispers Timing zu grob; WhisperX
> fuegt eine **wav2vec2-Forced-Alignment**-Stufe hinzu (sub-100ms). Reines Praezisions-Upgrade.

> [!note] Abgrenzung zu SKILL-060
> SKILL-060 ist der Default (faster-whisper). Dieses Ticket ist ein **optionaler** zweiter Pfad
> ueber demselben Output-Schema — kein Ersatz, kein Renderer-Umbau.

## Was soll erreicht werden? (Business-Ziel)
Optionaler Praezisions-Transkriptions-Pfad: Karaoke-genaue Wortgrenzen fuer Reels, bei denen das
Caption-Timing exakt aufs gesprochene Wort sitzen muss. Gleiches `{text,startMs,endMs}`-Output.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When der Alignment-Pfad gewaehlt wird (`--align`), the system shall nach der
      faster-whisper-Transkription eine wav2vec2-Forced-Alignment-Stufe (WhisperX) anwenden und
      sub-100ms-Wortgrenzen liefern. → Test gegen Fixture/echten Clip-Ausschnitt.
- [ ] **EARS-2:** When WhisperX/torch nicht installiert ist, the system shall klar darauf hinweisen
      und auf den SKILL-060-Default zurueckfallen — kein Hard-Crash (Prereq, kein Blocker).
- [ ] **EARS-3:** When der Alignment-Pfad laeuft, the system shall dasselbe Transkript-/Caption-Schema
      wie SKILL-060 ausgeben (kein Parallel-Format, kein Renderer-Umbau).
- [ ] **EARS-4 [multi-projekt]:** Sprache/Modell/Device als Parameter — kein Projektwert.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `transcribe.py` additiv `align=True`/`--align`; lazy `whisperx`-Import;
  faster-whisper-Segmente → `whisperx.align()` → Wort-Tokens. Fallback auf SKILL-060 bei fehlendem torch.
- **Verworfene Alternative:** WhisperX als Default — verworfen (torch-Gewicht; faster-whisper reicht
  fuer Pill-Captions). **Betroffene Module:** `creative_studio/transcribe.py` (additiv),
  `requirements.txt` (whisperx optional-kommentiert), `SKILL.md` §11c. → ADR n/a.

## Technische Hinweise
- Abhaengig von SKILL-060. `pip install whisperx` (torch) — schwer; nur Praezisions-Pfad.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/transcribe.py` (additiv `align`).
- `skills_sources/creative-studio/tests/test_skill_062_align.py` (neu).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
