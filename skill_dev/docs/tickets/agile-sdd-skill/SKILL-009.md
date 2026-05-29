---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: workflows_with_active_inbox
---

# SKILL-009: inbox/-Konvention für agile-sdd (externe Materialien)

**Status:** idea
**Erstellt:** 2026-05-28
**MoSCoW:** Should
**Geschaetzter Aufwand:** S

> [!info] Trigger-Live-Erfahrung
> 2026-05-28, Bewerbung-Bot v0.6-Spec mit Jakob: Janina hat per WhatsApp
> Anforderungen geschickt (Text + 2 OGG-Sprachnachrichten), die zum
> Spec-Material fuer 5 Tickets wurden. Jakob hat die Files unter
> `workflows/prod/bewerbung-bot/inbox/` abgelegt und vorgeschlagen,
> dass der SDD-Skill so eine Inbox-Konvention nativ vorsieht.

## Was soll erreicht werden? (Business-Ziel)

Externe Materialien (Sprachnachrichten, Screenshots, PDFs, Forward-Mails),
die NICHT ueber den Standard-Spec-Weg (Chat mit Claude) reinkommen,
sollen einen festen Ablageort pro Workflow/Projekt haben — vor dem
formellen Ticket-Spec. So gehen sie nicht im Chat-Backlog verloren und
sind beim Spec-Prozess auffindbar.

## Akzeptanzkriterien (EARS-Format)

- [ ] When der agile-sdd-Skill in einem neuen Projekt initialisiert wird,
  the system shall optional einen `inbox/`-Ordner auf der Workflow-/
  Projekt-Ebene vorsehen (mit `.gitkeep`).
- [ ] When der Implementer-Bootstrap laeuft, the system shall pruefen ob
  `inbox/` Inhalt hat und Jakob aktiv darauf hinweisen ("X Files in inbox/
  warten auf Spec-Verarbeitung").
- [ ] When ein Ticket aus einer Inbox-Quelle entsteht, the system shall
  im Ticket-Frontmatter `inbox_source:` mit Datei-Pfad referenzieren
  (Audit-Trail "wo kam die Anforderung her").
- [ ] When die Anforderung gespec't ist UND das Ticket auf `done` geht,
  the system shall Jakob fragen, ob die Inbox-Files archiviert
  (`inbox/archive/`) oder geloescht werden sollen (Default: archivieren).

## Technische Hinweise

- Skill-Code-Aenderung: `skills_sources/agile-sdd-skill/SKILL.md`
  (Abschnitt "Checkliste: Neues Projekt aufsetzen" um `inbox/` ergaenzen +
  Bootstrap-Sequenz um inbox-Check erweitern).
- Optional: `templates/INBOX_README.md` mit Konvention
  ("OGG/MP3/PDF/Screenshots hier ablegen, Sprachnachrichten am besten
  transkribieren wenn moeglich").
- Inbox sollte **pro Workflow/Projekt-Verzeichnis** existieren, nicht
  zentral — sonst wuerde Spec-Material aus mehreren Workflows vermischt.
- Inbox-File-Ablage in `.gitignore` koennte sinnvoll sein (Sprachnachrichten
  koennten sensible Daten enthalten) — pro Projekt-Konvention.

## Offene Klaerungen (vor `spec`)

- Soll der Bootstrap-Hinweis auf `inbox/`-Files **passiv** sein (nur Hinweis)
  oder **aktiv** (Jakob wird gefragt: "willst du jetzt das Material specen?")?
- Welche Formate werden unterstuetzt? (OGG-Transkription waere via
  Whisper-MCP moeglich — separater Skill?)
- Soll das Pattern auch in Skill-Tickets selbst gelten (also `skill_dev/inbox/`)?

## Code-Referenzen

- Live-Vorbild: `C:/Users/Jakob/claude_projects/Workflow Builder/workflows/prod/bewerbung-bot/inbox/`
- Skill-Code: `skills_sources/agile-sdd-skill/SKILL.md` Abschnitt "Checkliste:
  Neues Projekt aufsetzen" (Zeilen ~705-720) + Abschnitt "Agent Bootstrap-Sequenz"
  (Zeilen 13-37)

## Ergebnis / Notizen

_Wird beim Implementieren befuellt._
