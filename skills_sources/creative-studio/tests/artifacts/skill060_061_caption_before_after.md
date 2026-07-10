# Captions: VORHER (hartkodiert) vs. NACHHER (aus echtem Transkript)

Beleg fuer SKILL-060/061 (Critique 2026-06-25: „kein Bezug zum Transkript").
Quelle: Bronze `Video 07.03.26, 15 46 40.mov` (Talking-Head, O-Ton).

## VORHER — `examples/reel_talkinghead.json` (hand-autoriert)
Caption-Text = vorab geschriebener Werbe-Slogan, Timings runde Handwerte:

| startMs | endMs | Wort |
|---|---|---|
| 600 | 850 | Die |
| 850 | 1300 | meisten |
| 1300 | 1750 | kaufen |
| 1750 | 2100 | neue |
| 2100 | 2700 | Tools. |
| … | … | „Du brauchst ein System. Agentisch arbeiten spart 3 Stunden pro Woche…" |

→ Das ist NICHT, was im Clip gesagt wird. Glatte Timings (600/850/1300…) = erfunden.

## NACHHER — `skill060_transcript_real.json` (faster-whisper, word-level)
Caption-Text = tatsaechlich gesprochenes Wort, Timings audio-gebunden (krumm):

| startMs | endMs | p | Wort |
|---|---|---|---|
| 1800 | 2180 | 0.63 | Die |
| 2180 | 2560 | 1.00 | meisten |
| 2560 | 3100 | 0.87 | Gastgeber |
| 3100 | 3480 | — | wissen gar nicht, |
| 3860 | 4180 | 1.00 | Nachrichten |
| 4340 | 8020 | 0.99 | … sie bekommen. |
| 10680 | 10860 | 0.88 | 16 |
| 10860 | 11940 | 0.79 | Ferienwohnungen |
| 12420 | 12760 | 0.47 | 150 |
| 12760 | 13220 | 0.99 | Nachrichten. |

Volltext: „Die meisten Gastgeber wissen gar nicht, wie viele Nachrichten sie bekommen.
Ich habe das mal bei uns gemessen, wir haben 16 Ferienwohnungen … 150 Nachrichten."

## Render-Beleg
- Gold: `…/Content Lake/Gold/reel_talkinghead_v2_transcript.mp4` (1080×1920, 11,5 s, Video+O-Ton).
- Frames: `skill061_transcript_2.3s_NACHRICHTEN.png` (Caption „VIELE NACHRICHTEN", Keyword-Highlight),
  `skill061_transcript_9.2s_FERIENWOHNUNGEN.png` (Caption „16 FERIENWOHNUNGEN", Highlight).
- Decision (Redaktions-Pass): `skill061_editorial_decision.json`.

## Keyword-Betonung — SKILL-066 (erledigt 2026-06-25)
Frueher hat `reel_spec.py.CaptionTokenSpec` das explizite `keyword:true` aus dem Redaktions-Pass
GEDROPPT → Highlights stammten aus der SKILL-055-Heuristik. **Behoben (SKILL-066):** das Feld wird
jetzt bis in die Remotion-Props durchgereicht; `Captions.tsx` highlightet das **inhaltlich** gewaehlte
Wort. Frame-Beleg in `skill066_editorial_SYSTEM_highlighted.png` (Flag → „SYSTEM") vs
`skill066_heuristic_GEWINNT_highlighted.png` (kein Flag → „GEWINNT" = laengstes Token).
