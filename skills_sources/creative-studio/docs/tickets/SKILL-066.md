# SKILL-066: creative-studio — `keyword:true`-Verdrahtung aus LLM-Pass in den Caption-Renderer

**Status:** review
**Erstellt:** 2026-06-25
**MoSCoW:** Could
**Geschaetzter Aufwand:** S
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_content-aware-reel-pipeline.md` (§3.2 Keyword-Betonung) + SKILL-055 (`keyword`-Feld in Captions.tsx)

> [!info] Herkunft
> SKILL-055 hat in `Captions.tsx` bereits ein optionales `keyword:true`-Feld pro Token (explizit
> markiertes Keyword schlaegt die Heuristik „laengstes/zahlhaltiges Token"). SKILL-061 setzt dieses
> Feld bereits aus dem Redaktions-Pass. Dieses Ticket stellt sicher, dass die **inhaltliche** Betonung
> durchgaengig bis ins Bild ankommt — und ersetzt die Heuristik, wo eine Decision vorliegt.

> [!note] Abgrenzung
> SKILL-055 = Mechanik (`pickKeywordIndex` mit explizit-Vorrang). SKILL-061 = Quelle (`keyword:true`
> in der Spec). Dieses Ticket = **durchgaengiger Beleg** im Render + Doku, dass die LLM-Betonung
> gewinnt; kleines Verifikations-/Verdrahtungs-Ticket.

## Was soll erreicht werden? (Business-Ziel)
Die vom Redaktions-Pass gesetzte Betonung (genau ein Keyword pro Phrase, inhaltlich) erscheint
zuverlaessig im gerenderten Reel — statt der reinen Laengen-/Zahl-Heuristik.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When ein Caption-Token `keyword:true` traegt, the system shall genau dieses Token
      highlighten (Vorrang vor der Heuristik) — pro aktiver Phrase hoechstens eins. → Frame-Beleg
      (SYSTEM vs GEWINNT) + `Captions.tsx.pickKeywordIndex` (explicit-Vorrang, Bestand SKILL-055).
- [x] **EARS-2:** When kein Token einer Phrase markiert ist, the system shall auf die SKILL-055-
      Heuristik zurueckfallen (Bestand unveraendert). → Test `test_no_keyword_falls_back_to_heuristic_shape`.
- [x] **EARS-3:** When `reel_spec.py` eine Spec mit `keyword`-Captions laedt, the system shall das
      Feld bis in die Remotion-Props durchreichen (kein Drop im Adapter). → Tests
      `test_caption_token_spec_carries_keyword`, `test_keyword_survives_into_props`.
- [x] **EARS-4 [multi-projekt]:** Highlight-Farbe aus Brand-Props (Bestand), kein Projektwert.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** pruefen/sicherstellen, dass `reel_spec.py` das optionale `keyword`-Feld in
  `CaptionTokenSpec` aufnimmt und in `to_dict()` durchreicht (heute nur `text/startMs/endMs`); Render-
  Frame-Test, dass markiertes Token gewinnt. Minimaler Adapter-Fix + Test.
- **Verworfene Alternative:** Heuristik ganz entfernen — verworfen (Fallback fuer Specs ohne Decision).
  **Betroffene Module:** `creative_studio/reel_spec.py` (`keyword` durchreichen), `video/src/Captions.tsx`
  (bereits vorhanden), `SKILL.md` §11b. → ADR n/a.

## Technische Hinweise
- `surface: backend`. Abhaengig von SKILL-055 + 061. Klein (S). **Hinweis:** `CaptionTokenSpec` in
  `reel_spec.py` droppt das `keyword`-Feld aktuell — genau das schliesst dieses Ticket.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/reel_spec.py` (`CaptionTokenSpec.keyword` durchreichen).
- `skills_sources/creative-studio/video/src/Captions.tsx` (Bestand, `keyword`-Vorrang).
- `skills_sources/creative-studio/tests/test_skill_066_keyword_passthrough.py` (neu).

## Ergebnis / Notizen
**Umgesetzt 2026-06-25** (Implementer-Pass, Frame-belegt).

- `reel_spec.py`: `CaptionTokenSpec` um `keyword: bool = False` erweitert; `to_dict()` reicht
  `keyword:true` nur fuer markierte Tokens durch (schlanker Default sonst); `parse_reel_spec`
  liest `c.get("keyword")`. Damit ueberlebt die von `content.py` (SKILL-061) gesetzte
  inhaltliche Betonung bis in die Remotion-Props — vorher hat der Adapter sie gedroppt.
- `Captions.tsx` war bereits vorbereitet (`pickKeywordIndex`: expliziter `keyword:true`-Vorrang
  vor der Heuristik, SKILL-055) — kein TSX-Aenderung noetig, nur der gebrochene Daten-Pfad.
- **Frame-Beleg (Divergenz heuristik vs editoriell):** identisches Caption-Fenster
  `["SYSTEM","GEWINNT"]`, nur der `keyword:true`-Flag unterschiedlich:
  - `skill066_editorial_SYSTEM_highlighted.png` — „**SYSTEM**" orange (editorielle Wahl).
  - `skill066_heuristic_GEWINNT_highlighted.png` — „**GEWINNT**" orange (Heuristik = laengstes Token).
  Das Highlight wandert allein durch das durchgereichte Keyword.
- Re-Render des transkript-basierten Reels: `…/Gold/reel_talkinghead_v3_kw.mp4` (Exit 0) mit
  jetzt durchgereichten Keywords (Nachrichten/Ferienwohnungen/150/Nachrichten).
- **Tests:** `tests/test_skill_066_keyword_passthrough.py` (4, EARS-1..3 + E2E content→props).
  Suite 215 passed (Baseline 211 + 4).

