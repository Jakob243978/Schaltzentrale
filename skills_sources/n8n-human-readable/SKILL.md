---
name: n8n-human-readable
version: 0.0-geplant
description: (GEPLANT — noch nicht implementiert) Prettify-/Readability-Skill fuer n8n-Workflows. Auditiert und layoutet grosse Workflows (Sticky-Note-Sektionen, [STATUS]/[VERB]-Naming, Lane-Layout, readability_score), damit sie ohne Doku verstaendlich bleiben. Aktivieren, wenn der User einen n8n-Workflow lesbarer machen, auditieren oder "prettifien" will.
---

# n8n-human-readable — GEPLANTER SKILL (Platzhalter)

> [!warning] Status: geplant, noch nicht implementiert
> Dieser Skill hat noch **keinen** ausführbaren Code. Er existiert als
> self-contained SDD+PO-Projekt-Platzhalter, damit Spec-Arbeit (SKILL-010) und
> Research an einem Ort leben. Der Skill-Code (`commands/`, `patterns/`,
> `tools/`) wird beim Umsetzen von `docs/tickets/SKILL-010.md` hier angelegt.

## Zweck (geplant)

Verwandelt das Vision-Prinzip „visuelle Nachvollziehbarkeit" von einer Mahnung
in ein automatisch herstellbares Werkzeug — vergleichbar mit `black`/`prettier`
für Code, aber für n8n-Workflows. Auditiert Workflows
(`/n8n-readability-audit`) und generiert Prettify-Vorschläge (`/n8n-prettify`)
ohne je ungefragt in die Live-Instanz zu schreiben.

## Nächster Schritt

`docs/tickets/SKILL-010.md` (Status `idea`) durch `/po-challenge` schärfen,
offene Klärungen auflösen, dann auf `spec` heben und implementieren. Details +
Recherche: `docs/research/2026-05-29_n8n-readability-analyse.md`.
