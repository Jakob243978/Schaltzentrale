# SKILL-063: creative-studio — B-Roll-zu-Transkript-Matching (Keyword/Embedding)

**Status:** review
**Erstellt:** 2026-06-25
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_content-aware-reel-pipeline.md` (§3.3 B-Roll-Matching) + `2026-06-24_reels-video-editing-strategy.md` (§1.6 B-Roll ueber Voiceover)

> [!info] Herkunft
> Teil von Jakobs Kritik („kein Matching von B-Roll zum Gesagten"): heute fuellt nichts das
> `broll[]`-Feld inhaltlich — Clips waeren beliebig. Best Practice 2026: B-Roll-Position an
> Keyword/Phrase im Transkript binden (Descript 92 % Trefferquote; B-Script/USPTO-Verfahren).

> [!note] Abgrenzung
> SKILL-046 hat das `broll[]`-Render-Feld + B-Roll-Series gebaut (RENDER). Dieses Ticket fuellt es
> **inhaltlich** aus dem Redaktions-Pass (CONTENT). Renderer unveraendert.

## Was soll erreicht werden? (Business-Ziel)
Pro Aussage im gewaehlten Segment einen **passenden** B-Roll-Clip zuordnen (statt zufaellig), sodass
das Visual den gesprochenen Inhalt belegt. Tier-0 = Keyword-Match gegen Asset-Tags (kein Modell);
Should-Ausbau = Embedding-Aehnlichkeit.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When der Redaktions-Pass B-Roll-Cues liefert (Tag/Phrase + Timestamp), the system
      shall sie gegen einen Asset-Index (Tags/Beschreibung, ggf. ueber `assets.py`) matchen und das
      `broll[]`-Feld der Spec mit `{src,seconds}` fuellen. → Test gegen Asset-Index-Fixture.
- [ ] **EARS-2:** When kein passendes Asset existiert, the system shall die Position leer lassen
      (Talking-Head/Title-Card-Fallback) statt einen unpassenden Clip zu erzwingen — kein Silent-Fake.
- [ ] **EARS-3 [Should-Ausbau]:** When Embeddings verfuegbar sind, the system shall semantische
      Aehnlichkeit (Phrase ⇄ Asset-Beschreibung) statt reinem Keyword-Match nutzen.
- [ ] **EARS-4 [multi-projekt]:** Asset-Index + Tags kommen als Parameter — kein Projektwert.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `content.py` additiv `broll_cues` in der `EditorialDecision`;
  `match_broll(cues, asset_index)` (Keyword-Tier-0) → fuellt `decision_to_spec()` das `broll[]`.
  Embedding-Match als optionaler zweiter Resolver.
- **Verworfene Alternative:** eigener multimodaler Highlight-Detektor — Won't (Research §6).
  **Betroffene Module:** `content.py`, evtl. `assets.py` (Tag-Index), `SKILL.md` §11c. → ADR n/a.

## Technische Hinweise
- Abhaengig von SKILL-061. Embedding-Variante kann lokal (sentence-transformers) oder API sein —
  Tier-0 Keyword braucht kein Modell.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/broll_match.py` (neu — eigenes Modul statt in
  content.py, damit das Matching eigenstaendig/wiederverwendbar bleibt; content.py unveraendert
  als Cue-Quelle ueber `EditorialDecision`).
- `skills_sources/creative-studio/tests/test_skill_063_broll_match.py` (neu, 10 Tests).

## Ergebnis / Notizen
**Umgesetzt 2026-06-25 (v1, Tier-0 Keyword/Token-Overlap — kein Modell/keine API).**

- **Neues Modul `broll_match.py`** (bewusst eigenstaendig statt in content.py — so ist das
  Matching auch ohne den Redaktions-Pass nutzbar; content.py liefert die Cues ueber die
  bestehende `EditorialDecision`):
  - `load_library(manifest)` / `library_from_dir(dir)` — Bibliothek aus Manifest-Dicts ODER aus
    einem Verzeichnis (Dateinamen als implizite Tags).
  - `build_broll_cues(transcript, decision)` — eine Cue je `keyword_words`-Phrase (Wort +/-1
    Kontext-Fenster); Fallback = Hook-Cue, wenn keine Keywords gesetzt (EARS-1).
  - `match_cue` / `match_broll` — Token-Overlap-Score (lowercase, Stoppwort-bereinigt, leichtes
    DE-Stemming gleicht Singular/Plural-Drift aus, z.B. „Ferienwohnungen" ⇄ Tag „ferienwohnung").
    Score 0 -> Position bleibt LEER (EARS-2, kein erzwungener Fehl-Clip).
  - `match_broll_for_decision(...)` — Convenience: Transkript+Decision+Bibliothek -> `broll[]`.
  - Output `[{src, seconds}]` ist 1:1 reel_spec-`broll`-kompatibel (in Test gegen
    `reel_spec.parse_reel_spec` verifiziert). `allow_repeat=False` verbraucht jeden Clip nur einmal.
- **Tag-/Manifest-Konvention** in der Modul-Docstring dokumentiert (zusaetzlich in SKILL.md §11c):
  Clip = `{src, tags?, description?, seconds?}`; ohne `tags` dienen Dateiname + Beschreibung als
  implizite Tag-Quelle. Bibliothek kommt als Parameter (EARS-4, kein Projektwert).
- **EARS-3 (Embedding)** bleibt offen/Should-Ausbau — bewusst NICHT gebaut (v1 = Keyword Tier-0
  laut Ticket; Embedding waere eine Design-/Dependency-Entscheidung). Im Modul-Docstring als
  Ausbaupfad markiert.
- **Tests:** 10 (kein Match, leere Bibliothek, Reel-Spec-Schema/Ladbarkeit, no-repeat,
  Dateiname-als-Tag, Cue-Ableitung aus Keywords, Hook-Fallback, End-to-End, library_from_dir).
  Volle Suite gruen: **234** (Baseline 215 + 19 aus SKILL-063/065).
