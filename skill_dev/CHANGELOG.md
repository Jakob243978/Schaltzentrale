# CHANGELOG — Skill-Entwicklungs-Repo

Aenderungen an Skills (Code unter `<Schaltzentrale>/skills_sources/`) und
am Meta-Layer (`skill_dev/`). Neueste oben. Format orientiert sich an
Keep-a-Changelog.

---

## 2026-05-31 — agile-sdd-skill v0.5: inbox/-Konvention (SKILL-009)

**Added (`skills_sources/agile-sdd-skill/`):**
- **SKILL.md Sektion K** — vollstaendige inbox/-Konvention: fester
  Ablageort pro Workflow/Projekt fuer menschliches Eingangs-Material
  (Screenshots, PDFs, Notizen), `.gitignore`-Default (Inhalt ignorieren
  ausser `.gitkeep`), Format-Scope (PNG/PDF/Text, **keine** Audio-Auto-
  Transkription), Archivierung nach `done`.
- SKILL.md Bootstrap (Sektion A) Punkt 10 — **passiver** Hinweis, wenn
  `inbox/` unverarbeitetes Material enthaelt (kein aktives Nachfragen).
- SKILL.md Ticket-Format (Sektion B) + `templates/TICKET.md` — optionales
  Frontmatter-Feld `inbox_source:` (Audit-Trail).
- SKILL.md Checkliste "Neues Projekt aufsetzen" — Schritt `inbox/`-Setup
  inkl. `.gitignore`-Empfehlung.

**Changed:**
- SKILL.md Skill-Version `0.4` → `0.5`.

**Decisions (governance_log 2026-05-31):** Bootstrap-Hinweis passiv; keine
Audio-Transkription (separater Skill); Konvention gilt fuer alle agile-sdd-
Projekte inkl. `skill_dev`; `.gitignore`-Default = ignorieren (sensibles
Material); kein separates `INBOX_README.md`-Template (Sektion K reicht).

**Offen:** Verifier-Pass `/sdd-verify SKILL-009` + `setup.ps1`-Deploy nach
`~/.claude/skills/`.

**Trigger:** SKILL-009 — Live-Erfahrung 2026-05-28 (Bewerbung-Bot-Spec mit
WhatsApp-Material von Janina).

---

## 2026-05-25 — Skill-Dev-Repo initial aufgesetzt (SKILL-Migration)

**Added:**
- `skill_dev/` Sub-Tree in Schaltzentrale neu angelegt — eigene Meta-Ebene
  fuer Skill-Entwicklung.
- `docs/SKILLS_VISION.md` initial befuellt aus TICKET-083 Teil B —
  Vision-Statement, 6 Kern-Prinzipien, 5 Outcome-Metriken,
  5 Out-of-Scope-Negationen.
- `docs/po-config.yaml` mit Skill-Repo-Defaults
  (outcome_review_days=14, cooldown_default_hours=48).
- `docs/DEFERRED.md` + `docs/po-outcomes.md` + `docs/governance_log.md`
  initial leer (mit Header).
- `CLAUDE.md` (Bootstrap-Sequenz fuer Skill-Dev-Arbeit, Verweis dass
  Code in `skills_sources/` lebt + `setup.ps1`-Hinweis).
- `ROADMAP.md` (initiale Liste: SKILL-001/002/003 als migrierte Tickets).
- `tests/test_skill_dev_smoke.py` (3+ Cases: Vision parsebar,
  SKILL-Tickets-Liste nicht leer, po-config.yaml valid).

**Migrated:**
- `TICKET-080` (Immobewertung) → `SKILL-001` (PO-Skill bauen) — Original
  bleibt in Immobewertung mit Status `done` + Migrations-Note.
- `TICKET-081` (Immobewertung) → `SKILL-002` (Lift-and-Shift T078/T079
  in PO-Skill) — Original bleibt mit Migrations-Note.
- `TICKET-082` (Immobewertung) → `SKILL-003` (Implementer-Hygiene-
  Pattern) — Original bleibt mit Migrations-Note.

**Memory:**
- `feedback_skill_tickets_verortung.md` war bereits angelegt (User
  hat das vorgezogen). Inhalt geprueft + auf Skill-Repo-Pfad
  konsistent.

**Trigger:** TICKET-083 — Dogfood-Erkenntnis: Skill-Tickets gehoeren
nicht in Projekt-Repos.
