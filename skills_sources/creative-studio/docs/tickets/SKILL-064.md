# SKILL-064: creative-studio — End-to-End-Orchestrierung (`footage → fertiges Reel`, ein Sub-Command)

**Status:** spec
**Erstellt:** 2026-06-25
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_content-aware-reel-pipeline.md` (§4 Soll-Pipeline A–F)

> [!info] Herkunft
> SKILL-060/061 liefern die Stufen einzeln (Transkript, Content-Analyse, Spec). Fuer den Alltag soll
> es **einen** Lauf geben: Footage rein → fertiges Reel raus. Der Redaktions-Pass (Claude) bleibt der
> eine interaktive Schritt; alles andere ist Glue.

> [!note] Abgrenzung
> Kein neuer Render-Pfad, keine neue Intelligenz. Reine Orchestrierung ueber transcribe.py (060),
> content.py (061), reel_spec.py (045), Remotion (043/044/055/056).

## Was soll erreicht werden? (Business-Ziel)
Ein Sub-Command/Runbook, das A→F bindet: Footage → Audio → Transkript → (Claude-Decision) → Spec →
props → Render → Gold-MP4 + Naming. Hard-Failure bei leerem Transkript/ungueltiger Decision.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein Footage-Pfad + Brand + (Claude-)Decision uebergeben werden, the system
      shall A–F deterministisch durchlaufen und ein Gold-MP4 + props.json erzeugen. → E2E-Test
      (kurzer Clip).
- [ ] **EARS-2:** When eine Stufe scheitert (leeres Transkript, ungueltige Decision, Render-Exit≠0),
      the system shall **stoppen** und den Fehler melden — nicht trotzdem weiterrendern
      (`feedback_workflow_hard_failure`).
- [ ] **EARS-3:** When der Redaktions-Pass interaktiv ist, the system shall den Prompt ausgeben und
      die Decision als Eingabe annehmen (Claude-im-Loop), ohne LLM-Key im Skill.
- [ ] **EARS-4 [multi-projekt]:** Footage/Brand/Modell/Sprache als Parameter — kein Projektwert.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `creative_studio/reel_pipeline.py` (oder Runbook `templates/reel_pipeline.md`
  + duenner CLI-Wrapper): ruft transcribe_video → gibt build_analysis_prompt aus → nimmt Decision-JSON →
  decision_to_spec → reel_spec → `npx remotion render`. Naming via SKILL-024.
- **Verworfene Alternative:** vollautonom ohne Claude-im-Loop — verworfen (die Redaktion IST der Wert;
  Auto-Heuristik waere wieder „kein Verstaendnis"). **Betroffene Module:** neu `reel_pipeline.py`/
  Runbook, `SKILL.md` §11. → ADR n/a.

## Technische Hinweise
- `surface: backend`. Abhaengig von SKILL-060 + 061. Render-Exit-Code als Gate.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/reel_pipeline.py` (neu) bzw. `templates/reel_pipeline.md`.
- `skills_sources/creative-studio/tests/test_skill_064_pipeline.py` (neu).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
