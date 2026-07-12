# SKILL-065: creative-studio — Editorial-/Struktur-Regeln (Hook→Insight→CTA-Validator, DISC-rot)

**Status:** review
**Erstellt:** 2026-06-25
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_content-aware-reel-pipeline.md` (§3.2 Narrativ, §3.4 Struktur) + `2026-06-24_reels-video-editing-strategy.md` (§1.1/§2.3 Hook→Value→CTA)

> [!info] Herkunft
> Damit der Redaktions-Pass (SKILL-061) nicht nur „irgendein" Reel baut, braucht es pruefbare
> Struktur-Regeln: Laenge im Sweet Spot, Hook-Promise < 3 s, **ein** Keyword pro Phrase, CTA vorhanden,
> DISC-rot-Hook (Ergebnis/Zahl zuerst, keine Frage-Floskel).

> [!note] Abgrenzung
> `content_type_warnings()` (specs.py, SKILL-040) prueft Laenge/Hook-Fenster. Dieses Ticket ergaenzt
> die **redaktionellen** Regeln (Narrativ-Vollstaendigkeit, Keyword-Sparsamkeit, Hook-Tonalitaet) —
> kein Doppel, baut darauf auf.

## Was soll erreicht werden? (Business-Ziel)
Ein `content_structure_warnings(spec)`-Validator, der eine maschinelle Reel-Spec gegen Editorial-Best-
Practice prueft und sachliche Warnungen liefert (keine Exceptions) — als Qualitaets-Netz vor dem Render.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When eine Spec geprueft wird, the system shall warnen, wenn (a) Segment-Laenge
      ausserhalb 12–45 s, (b) kein CTA, (c) >1 Keyword pro Sinn-Phrase, (d) Hook ohne Zahl/Ergebnis
      bzw. als Frage-Floskel. → Tests pro Regel.
- [ ] **EARS-2:** When alle Regeln eingehalten sind, the system shall eine leere Warnungs-Liste
      liefern (kein Fehlalarm).
- [ ] **EARS-3:** Reine Warnungen, keine Exceptions — der Render bleibt moeglich (Mensch/Claude
      entscheidet). Delegiert Laengen/Hook-Fenster an `content_type_warnings()` (kein Doppel).
- [ ] **EARS-4 [multi-projekt]:** Regeln/Schwellen als Konstanten, kein Projektwert.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `content.py` (oder `editorial.py`) `content_structure_warnings(spec, *, ct=None)`;
  nutzt `specs.content_type_warnings` fuer Laenge/Hook-Fenster, ergaenzt CTA-/Keyword-/Hook-Tonalitaets-
  Checks (Zahl-Regex, Frage-Heuristik).
- **Verworfene Alternative:** harte Blocker — verworfen (Editorial ist Geschmack; Warnung reicht,
  `feedback_workflow_hard_failure` gilt fuer technische Stufen, nicht fuer Stil).
  **Betroffene Module:** `content.py`/`editorial.py`, `SKILL.md` §11. → ADR n/a.

## Technische Hinweise
- `surface: backend`. Abhaengig von SKILL-061. Klein (S).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/content.py` (additiv `content_structure_warnings`
  + Editorial-Konstanten; bestehende Funktionen unveraendert).
- `skills_sources/creative-studio/tests/test_skill_065_editorial_validator.py` (neu, 9 Tests).

## Ergebnis / Notizen
**Umgesetzt 2026-06-25 — additiv in `content.py` (kein neues Modul, naeher an decision_to_spec).**

- **`content_structure_warnings(spec, *, ct=None)`** prueft eine maschinelle Reel-Spec
  (decision_to_spec-Dict) und liefert reine WARNUNGEN (Liste, keine Exception/kein Blocker —
  EARS-3; Editorial ist Geschmack, `feedback_workflow_hard_failure` gilt fuer technische Stufen).
  Regeln (EARS-1):
  - **Laenge:** aus den (auf 0 genullten) Caption-Timings abgeleitet; mit uebergebenem
    `ContentType` an `specs.content_type_warnings()` delegiert (EARS-3, kein Doppel), sonst
    Fallback gegen `STRUCTURE_MIN/MAX_SECONDS` (12–45 s).
  - **CTA vorhanden** (Narrativ Hook→Insight→CTA endet sonst ohne naechste Handlung).
  - **Insight/Value-Teil** vorhanden (subline).
  - **Hook-Tonalitaet (DISC-rot):** Frage-Floskel -> Warnung; sonst Hook ohne Zahl/Ergebnis ->
    Substanz-Warnung.
  - **Caption-/Keyword-Last:** > ~1 Keyword je 4 Tokens -> Dauer-Highlight-Warnung.
- **EARS-2:** saubere Spec -> leere Liste (Test `test_perfect_structure_yields_no_warnings`).
- **EARS-4:** alle Schwellen als Modul-Konstanten (`HOOK_WINDOW_SECONDS`,
  `STRUCTURE_MIN/MAX_SECONDS`, `KEYWORD_TOKENS_PER_KEYWORD`, `_HOOK_QUESTION_OPENERS`) — kein
  Projektwert.
- **Tests:** 9 (perfekte Struktur, je Regel: CTA/Value/Hook-Frage/Hook-ohne-Zahl/Keyword-Last/
  Laenge-Fallback/Laenge-Delegation, plus „wirft nie"). Volle Suite gruen: **234**.

> [!note] Hook-Fenster (<3 s) im Fixture: das Akzeptanzkriterium „Hook im ersten Fenster" wird
> ueber `specs.content_type_warnings()` (hook_window_seconds des ContentType) mitgetragen — der
> Validator dupliziert die Fenster-Pruefung nicht, sondern delegiert sie (kein Doppel).
