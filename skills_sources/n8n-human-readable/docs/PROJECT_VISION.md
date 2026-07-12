# PROJECT_VISION.md — n8n-human-readable (geplant)

> [!info] Verfassung dieses Skills
> Wird in jedem Implementer-Bootstrap mit-gelesen und in jedem `/po-challenge`
> referenziert. Änderungen append-only im **Aktualisiert**-Log.

> [!warning] Geplanter Skill (2026-07-12)
> Noch kein Code. Self-contained SDD+PO-Platzhalter, aus `skill_dev/` migriert.
> Jakob ist finaler PO.

---

## Vision-Statement

`n8n-human-readable` macht grosse n8n-Workflows so lesbar, dass Jakob (oder ein
Subagent) sie **6 Monate später ohne Doku** versteht. Der Skill auditiert und
layoutet Workflows automatisch (Sticky-Note-Sektionen, klares Node-Naming,
Lane-Layout, Readability-Score) und macht damit das bislang nur ermahnte Prinzip
„visuelle Nachvollziehbarkeit" operativ herstellbar — ohne je ungefragt in eine
Live-Instanz zu schreiben.

---

## Kern-Prinzipien

1. `mensch-final-im-loop` — Der Skill schlägt vor (Audit, Prettify-Diff), pusht
   aber NIE autonom in die Live-Instanz. Bestätigung ist Pflicht.
2. `deterministisch-nicht-ml` — Wir parsen Workflow-JSON, kein Pixel-/ML-Diff.
   Reproduzierbar, erklärbar.
3. `why-not-what-in-notes` — Sticky Notes erklären das WARUM, nicht das
   offensichtliche WAS. Oberflächliche Auto-Notes sind ein Bug.
4. `readability-score-gegen-goodhart` — Der Score misst Lesbarkeit, wird aber
   durch 14-Tage-Outcome-Review qualitativ gegengeprüft (nicht auf 100 optimieren).
5. `lessons-aus-live-use-zurueckfuehren` — Erkenntnisse aus realen Workflow-Audits
   werden als Pattern/Scoring-Regel im Skill verstetigt.

---

## Outcome-Metriken

- **workflow_readability_score** — 0-100 pro Workflow (Sticky-Coverage,
  Branch-Labels, Nodes/Sektion, Lane-Konsistenz, Naming). Quelle: Skill-Output.
- **verstanden_ohne_doku_nach_6_wochen** — qualitativ: hat ein Subagent den
  Workflow später ohne Doku verstanden? Quelle: Outcome-Review.

---

## Was NICHT im Scope ist

- Direktes Schreiben in Prod-Instanz ohne User-Confirm (Hard-No).
- Auto-Refactor in Sub-Workflows (nur vorschlagen).
- Visual-Linting via Screenshot-Diff (wir parsen JSON).
- Einfrieren/Überschreiben versionierter `versions/vX.Y/`-Snapshots.

---

## Kunden-Weiterentwicklung (Upstream-Review-Flow)

Sobald implementiert, eigenständig an Kunden ausrollbar. Kunden legen eigene
SKILL-Tickets in `docs/tickets/` an (`origin: customer/<name>`); Jakob reviewt
und entscheidet über Upstream-Übernahme.

---

## Aktualisiert (Append-only Log)

## 2026-07-12 — Migration aus skill_dev + Platzhalter-Init
**Wer:** Architektur-Umbau-Subagent
**Grund:** skill_dev wird aufgelöst; der geplante Skill bekommt ein eigenes
self-contained SDD+PO-Projekt, damit Spec (SKILL-010) + Research einen Ort haben.
**Änderung:** Vision erstmals skill-lokal; SKILL-010 + Recherche hierher migriert.
