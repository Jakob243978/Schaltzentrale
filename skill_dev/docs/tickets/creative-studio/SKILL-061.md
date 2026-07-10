# SKILL-061: creative-studio — LLM-Content-Analyse (Transkript → Segment + Hook + Script + Captions)

**Status:** review
**Erstellt:** 2026-06-25
**MoSCoW:** Must
**Geschaetzter Aufwand:** M
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_content-aware-reel-pipeline.md` (§3.2 redaktionelle Intelligenz, §4 Soll-Pipeline) + `2026-06-24_reels-video-editing-strategy.md` (§1.1 Hook, §2.3 Hook→Value→CTA)

> [!info] Herkunft (Jakob-Kritik 2026-06-25)
> Zweiter Teil der Kritik: „**Gar kein Verstaendnis, was wir dort machen.** So sind keine guten Reels
> aufgebaut." Es fehlte jede redaktionelle Intelligenz: keine Auswahl der staerksten Aussage, kein
> Hook-Extrakt, kein Narrativ Hook→Insight→CTA, keine inhaltliche Keyword-Betonung. Vorbild
> OpusClip/Vizard (Virality-Score aus Hook/Flow/Value/Trend, Top-N statt 20 scrubben).

> [!note] Architektur — Claude IST die Intelligenz (wie ad_library.py)
> Das Modul macht **keinen** LLM-Call. Der Skill wird von Claude ausgefuehrt → Claude ist der
> Redaktions-Pass. Das Modul liefert Prompt-Template + Schema-Validierung + Mapping Transkript→Spec
> und ist gegen gespeicherte Fixtures unit-testbar (kein Live-LLM). Identisches Muster wie der
> Meta-MCP-Call bei `ad_library.py`.

## Was soll erreicht werden? (Business-Ziel)
Aus dem **echten Transkript** (SKILL-060) entsteht eine **maschinell erzeugte Reel-Spec** statt einer
handgeschriebenen: Claude waehlt das staerkste 20–45-s-Segment, extrahiert einen DISC-rot-Hook,
strukturiert Hook→Insight→CTA und markiert pro Phrase **ein** Betonungs-Keyword. Captions stammen
aus dem gewaehlten Segment des echten Transkripts. Loest „kein Verstaendnis".

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When ein Transkript vorliegt, the system shall via `build_analysis_prompt()` ein
      Briefing mit Wort-Index + Aufgaben (Segment/Hook/Narrativ/Keywords) erzeugen, das Claude als JSON
      beantwortet. → Test `test_prompt_lists_real_words_with_index`.
- [x] **EARS-2:** When Claudes Antwort geparst wird, the system shall sie robust validieren (auch
      ```json-Fence/umrahmt); fehlt `segment` oder `hook`, wirft es `ContentAnalysisError` (kein
      Silent-Fake). → Tests `test_parse_decision_from_fenced_json_string`, `test_parse_decision_requires_hook_and_segment`.
- [x] **EARS-3:** When eine Decision in eine Spec gebaut wird, the system shall die Captions AUS dem
      gewaehlten Segment des echten Transkripts schneiden (auf 0 ms genullt) und `keyword:true` auf die
      betonten Woerter setzen; ausser-Range-Indizes werden geklemmt. → Tests
      `test_decision_to_spec_captions_are_real_and_nulled`, `test_decision_clamps_out_of_range_segment`.
- [x] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall
      Brand als Parameter beziehen; die Spec ist von `reel_spec.py` (SKILL-045) ladbar — kein
      Parallel-Schema, kein Projektwert. → Test `test_spec_is_reel_spec_loadable`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `creative_studio/content.py` — `build_analysis_prompt()`,
  `EditorialDecision`-Dataclass, `parse_editorial_decision()` (robustes JSON-Extrahieren),
  `decision_to_spec()` (Segment-Cut + Null-auf-0 + keyword-Mapping → reel_spec.py-kompatible Spec).
- **Verworfene Alternative:** eigener API-Key/LLM-Call im Modul — verworfen (Key-Streuung, nicht
  testbar); der Agent/Claude macht den Call (ad_library-Muster).
- **Betroffene Module:** `creative_studio/content.py` (neu), `SKILL.md` §11b. → ADR n/a.

## Technische Hinweise
- `surface: backend`. `keyword:true` dockt an das bereits in `Captions.tsx`/SKILL-055 vorhandene
  `keyword`-Feld an (explizit markiertes Token schlaegt die Heuristik) → SKILL-066 verdrahtet das
  durchgaengig.
- Validierung gegen `content_type_warnings()` (specs.py) bleibt der Laengen-/Hook-Validator
  (SKILL-065 baut den Hook→Insight→CTA-Struktur-Validator darueber).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/content.py` (neu).
- `skills_sources/creative-studio/tests/test_skill_061_content.py` (neu).
- `skills_sources/creative-studio/SKILL.md` §11b.

## Ergebnis / Notizen
**Umgesetzt 2026-06-25** (Implementer-Pass, End-to-End-Beleg).

- `content.py` neu: Prompt-Bau, robuste Decision-Validierung, `decision_to_spec()`.
- **Live-Beleg (echter Redaktions-Pass):** ueber dem SKILL-060-Transkript wurde eine Decision
  erzeugt (Segment Wort 0–24, Hook „150 Nachrichten. 16 Wohnungen.", Keywords auf
  „Nachrichten/Ferienwohnungen/150/Nachrichten") → maschinelle Spec `th-transcript-v2` mit Captions
  **aus dem echten Wort** (auf 0 genullt, keyword:true auf den Datenpunkten). `reel_spec.py`
  validierte sie (`variant_id=th-transcript-v2__hook-h00__story-9x16`).
- **Render-Beleg:** Gold `reel_talkinghead_v2_transcript.mp4` (1080×1920, 11,5 s, Video+O-Ton).
  Proof-Frames (2,3 s „VIELE **NACHRICHTEN**", 9,2 s „16 **FERIENWOHNUNGEN**") zeigen: Captions =
  tatsaechlich Gesprochenes, Keyword-Highlight (SKILL-055-Pill) auf den Kern-Aussagen.
- **Tests:** `tests/test_skill_061_content.py` (6, EARS-1..4 + Clamp + reel_spec-Loadbarkeit).
  Suite 211 passed.

**Bewusst offen:** B-Roll-Cues aus dem Redaktions-Pass = SKILL-063; durchgaengige keyword:true-
Verdrahtung in den Renderer = SKILL-066; End-to-End-Sub-Command = SKILL-064.
