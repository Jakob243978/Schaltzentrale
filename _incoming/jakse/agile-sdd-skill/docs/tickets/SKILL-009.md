---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: workflows_with_active_inbox
---

# SKILL-009: inbox/-Konvention für agile-sdd (externe Materialien)

**Status:** review
**Erstellt:** 2026-05-28
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`
**Skill-Version:** agile-sdd-skill v0.5 (von v0.4 hochgebumpt mit diesem Ticket)

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

- [x] When der agile-sdd-Skill in einem neuen Projekt initialisiert wird,
  the system shall einen `inbox/`-Ordner auf der Workflow-/
  Projekt-Ebene vorsehen (mit `.gitkeep`) und in `.gitignore` empfehlen,
  `inbox/*` ausser `.gitkeep` zu ignorieren.
  → SKILL.md Checkliste Punkt 10 + Sektion K.
- [x] When der Implementer-Bootstrap laeuft, the system shall pruefen ob
  `inbox/` Inhalt hat und **passiv** darauf hinweisen ("X Files in inbox/
  warten auf Spec-Verarbeitung") — **nicht aktiv nachfragen**, nicht
  blockieren (Klaerung 1 entschieden, siehe unten).
  → SKILL.md Sektion A Punkt 10 + Sektion K.
- [x] When ein Ticket aus einer Inbox-Quelle entsteht, the system shall
  im Ticket-Frontmatter `inbox_source:` mit Datei-Pfad referenzieren
  (Audit-Trail "wo kam die Anforderung her").
  → SKILL.md Sektion B Ticket-Format + `templates/TICKET.md`.
- [x] When die Anforderung gespec't ist UND das Ticket auf `done` geht,
  the system shall das verarbeitete Material nach `inbox/archive/`
  verschieben (Default: archivieren, nicht loeschen).
  → SKILL.md Sektion K "Nach `done`: archivieren".

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

## Geklaerte Entscheidungen (2026-05-31, vor `spec` → umgesetzt)

> [!check] Klaerung 1 — Hinweis ist PASSIV
> Der Bootstrap-Hinweis auf `inbox/`-Files ist **passiv** ("X Files in inbox/
> warten auf Spec"), **nicht aktiv** ("willst du jetzt specen?"). Begruendung:
> Der Agent macht Material nur sichtbar; die Spec-Entscheidung bleibt beim User.
> Aktives Nachfragen wuerde jeden Bootstrap unterbrechen. Vision-konform mit
> `skill-schlanker-als-was-er-ersetzt`.

> [!check] Klaerung 2 — KEINE Auto-Transkription von Audio
> Der Agent liest nur, was er **nativ** kann: PNG/JPG/PDF/Text/Markdown.
> OGG/MP3-Transkription (Whisper) ist **ausgeklammert** — bei Audio gibt der
> Agent einen passiven Hinweis und bittet um eine Text-Zusammenfassung. Eine
> Whisper-Integration ist ggf. ein **separater Skill**, nicht Teil von
> agile-sdd. Haelt den Aufwand bei S.

> [!check] Klaerung 3 — Konvention gilt fuer ALLE agile-sdd-Projekte
> Inklusive `skill_dev` selbst (`skill_dev/inbox/`). Kein Sonderfall-Handling.

## Code-Referenzen

- Live-Vorbild: `C:/Users/Jakob/claude_projects/Workflow Builder/workflows/prod/bewerbung-bot/inbox/`
- Skill-Code: `skills_sources/agile-sdd-skill/SKILL.md` Abschnitt "Checkliste:
  Neues Projekt aufsetzen" (Zeilen ~705-720) + Abschnitt "Agent Bootstrap-Sequenz"
  (Zeilen 13-37)

## Ergebnis / Notizen

**Umgesetzt 2026-05-31** (Implementer: claude-opus-4-8 [1M context]).
Status `idea` → `spec` → `review` (Skill-Quelle real geaendert; vor `done`
fehlen Verifier-Pass `/sdd-verify SKILL-009` + Deploy via `setup.ps1`).

Geaenderte/neue Dateien (alle in `skills_sources/agile-sdd-skill/`):

- `SKILL.md`
  - Version `0.4` → `0.5`.
  - Sektion A (Bootstrap): neuer Punkt 10 — passiver inbox-Check.
  - Sektion B (Ticket-Format): optionales Frontmatter-Feld `inbox_source:`.
  - Checkliste "Neues Projekt aufsetzen": neuer Punkt 10 — `inbox/` +
    `.gitkeep` + `.gitignore`-Default; alter Punkt 10 → 11.
  - **NEU Sektion K** — vollstaendige inbox/-Konvention (Ablageort,
    Struktur, .gitignore-Default, passiver Bootstrap-Hinweis,
    Format-Scope ohne Audio-Transkription, `inbox_source:`-Verknuepfung,
    Archivierung nach `done`).
- `templates/TICKET.md`
  - optionaler `inbox_source:`-Hinweis im Frontmatter-Block.

Skill-Dev-Meta (in `skill_dev/`):
- `docs/governance_log.md` — Entscheidungs-Eintrag (3 Klaerungen + .gitignore-Default).
- dieses Ticket (Status, Klaerungen, AC-Haken, Ergebnis).

**Offen vor `done`:**
1. `/sdd-verify SKILL-009` (Verifier-Pass, frische Session).
2. `setup.ps1` der Schaltzentrale ausfuehren → Deploy nach
   `~/.claude/skills/agile-sdd-skill/`. Erst danach wirkt die Konvention
   im laufenden Skill.

**Bewusst NICHT gemacht:**
- Kein `setup.ps1`-Run (Deploy macht Haupt-Agent/Jakob).
- Kein git commit/push.
- Keine Whisper-/Audio-Transkription (separater Skill, siehe Klaerung 2).
- Kein `templates/INBOX_README.md` — Konvention lebt vollstaendig in
  SKILL.md Sektion K; ein zusaetzliches Template waere Redundanz und
  Over-Engineering bei Aufwand S.
