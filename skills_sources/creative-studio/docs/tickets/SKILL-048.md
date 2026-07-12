# SKILL-048: creative-studio — Batch-Render-Runner fuer Reel-Specs (n Reels in einem Lauf)

**Status:** spec
**Erstellt:** 2026-06-24
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_reels-video-editing-strategy.md` (§2.4 Batch/Templatisierung, §3.5 Batch/Data-driven, §7 MoSCoW Should)

> [!info] Herkunft (Recherche 2026-06-24)
> Skalierung = **Distribution-Engine, nicht Markenfilm**: ein Verzeichnis von Reel-Specs nacheinander
> rendern, n Reels in einem Lauf, mit konsistentem Naming. Das ist das Video-Pendant zur Bild-Batch-Engine
> (SKILL-023): die Reel-Spec (SKILL-045) ist die Einheit, der Runner orchestriert viele davon.

## Was soll erreicht werden? (Business-Ziel)
Ein Runner, der ein Verzeichnis (oder eine Liste) von Reel-Specs einliest und jede Spec als Reel-MP4 rendert
— mit Datei-Naming-Konvention (analog `--ad-id`/`variant_id`) und einem Manifest-Eintrag pro Reel. So
entsteht Batch-Reel-Produktion ohne manuellen Schnitt.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein Verzeichnis mit N Reel-Specs uebergeben wird, the system shall N Reels nacheinander
      rendern (ein MP4 pro Spec). → Test (Mock-Render) `test_runner_iterates_all_specs`.
- [ ] **EARS-2:** When ein einzelner Reel-Render fehlschlaegt, the system shall den Lauf **nicht** abbrechen,
      sondern den Fehler je Spec markieren und mit der naechsten weitermachen (analog SKILL-023 EARS-5).
      → Test `test_runner_isolates_render_error`.
- [ ] **EARS-3:** When Reels gerendert werden, the system shall Dateinamen + Manifest ueber die Naming-
      Systematik (SKILL-024, `variant_id`/`utm_content`) vergeben — **kein** Parallel-Schema.
      → Test `test_runner_naming_single_source`.
- [ ] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall Brand +
      Inhalt ausschliesslich aus den Specs/CLI beziehen — kein hartkodierter Projektwert. → Test `test_runner_project_neutral`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `creative_studio/batch_video.py` (oder Erweiterung von `batch.py`) — laedt Specs
  via `load_reel_spec()` (SKILL-045), ruft je Spec den Remotion-Render (`npx remotion render … --props`)
  ueber einen Subprocess-Wrapper auf, sammelt Ergebnisse in einem Manifest. Fehler je Spec isoliert.
- **Verworfene Alternative:** Video-Batch in die bestehende Bild-`batch.py` zwingen — moeglich, aber der
  Remotion-Subprocess-Pfad ist genug eigenstaendig, dass ein klar getrennter Runner sauberer ist (gleiche
  Naming-Single-Source). Implementer darf zusammenlegen, wenn die Manifest-Struktur identisch bleibt.
- **Betroffene Module:** `creative_studio/batch_video.py` (neu) ODER `batch.py` (Video-Zweig ausbauen —
  heute nur `not_implemented`-Stub, SKILL-023 EARS-3), `reel_spec.py` (read-only), `specs.py` (Naming, read-only).

## Technische Hinweise
- `surface: backend`. Der heutige `batch.py`-Video-Zweig ist ein bewusster `status: not_implemented`-Stub
  (SKILL-023 EARS-3) — dieser Runner loest ihn ein.
- **Lizenz-Risiko Remotion** (ab 4 Personen kostenpflichtig, SKILL.md §7) — Batch verstaerkt die Nutzung,
  vor Skalierung klaeren.
- Tests rendern nicht real (zu teuer/Tooling) — Render via Mock/Subprocess-Stub testen, Naming + Fehler-
  Isolation echt pruefen.
- Voraussetzung: SKILL-045 (Reel-Spec). Nutzt optional SKILL-043/044/046/047.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/batch_video.py` (neu) ODER `batch.py` (Video-Zweig).
- `skills_sources/creative-studio/creative_studio/reel_spec.py`, `specs.py` (read-only).
- `skills_sources/creative-studio/tests/test_skill_048_batch_video.py` (neu).
- Wissensgrundlage: `2026-06-24_reels-video-editing-strategy.md` (§2.4, §3.5, §7 Should).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
