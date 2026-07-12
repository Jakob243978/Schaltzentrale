# CHANGELOG — Skill-Entwicklungs-Repo

Aenderungen an Skills (Code unter `<Schaltzentrale>/skills_sources/`) und
am Meta-Layer (`skill_dev/`). Neueste oben. Format orientiert sich an
Keep-a-Changelog.

---

## 2026-06-18 — agile-sdd-skill v0.6 + po-skill v0.2: Default-Entscheidung + Empfehlungs-First (SKILL-014 + SKILL-015)

**Added (`skills_sources/agile-sdd-skill/`):**
- **SKILL.md Sektion L "Default-Entscheidungs-Regel"** — MUST-Regel:
  Agent entscheidet selbst und dokumentiert im `governance_log.md`, wenn
  alle Bedingungen erfuellt (reversibel + kein externer Kosten-Trigger +
  keine Outbound-Kommunikation + vision-konform + keine Architektur).
  Harte STOPP-Liste mit 6 Faellen (destruktive Ops, Outbound, neue
  bezahlte Deps, Architektur, Verifikations-Fehler, DB-Mutation).
  Dokumentations-Pflicht + Anti-Pattern + Verweis auf 2-Wochen-Plan.
- **SKILL.md Sektion M "Antwort-Pattern Empfehlungs-First"** — Pflicht-
  Format `Empfehlung: <Zeile>` + `Warum: <2-3 Saetze>` + `Trade-off: <1>`
  + optional `Alternativen` nur auf Nachfrage. 3-Option-Tabellen ohne
  Empfehlung verboten als Default. Selbst-Check + Beispiel/Anti-Beispiel.

**Added (`skills_sources/po-skill/`):**
- **SKILL.md Sektion C.5 "Empfehlungs-First in /po-challenge"** — am Ende
  jedes Challenge-Durchlaufs Pflicht-Empfehlung
  (annehmen | parken bis YYYY-MM-DD | ablehnen | Vision schaerfen) +
  Warum + Trade-off. Spiegelt agile-sdd-skill Sektion M. Verhaeltnis zur
  Akut-Liste (Sektion C) + STOPP-Liste (agile-sdd L.2) geklaert. Verweis
  auf Vision-Drift-Counter (2-Wochen-Plan).

**Changed:**
- SKILL.md `agile-sdd` Skill-Version `0.5` -> `0.6`.
- SKILL.md `po-skill` Skill-Version `0.1` -> `0.2`.

**Added (Memory):**
- `vault/Memory/feedback_default_decision_empfehlung_first.md` — neue
  Feedback-Memory mit Kern-Regel + STOPP-Liste + Konsequenz fuer Jakob.
- `vault/Memory/MEMORY.md` — Index-Eintrag.

**Backups:**
- `skills_sources/agile-sdd-skill/SKILL.md.bak_2026-06-18`
- `skills_sources/po-skill/SKILL.md.bak_2026-06-18`

**Trigger:** Jakob 2026-06-18, *"Mein meistgenutzter Move ist
'rueckfragen, was er empfehlen wuerde'. Ich fuehl mich entscheidungshemmt."*
Sourcedoku: `skill_dev/proposals/2026-06-18_sdd_default_decision_plus_voice_mode.md`,
Vorschlaege 1+2. Vorschlaege 3 (Voice-Mode) + 4 (Vision-Drift-Counter)
warten ~2 Wochen.

**Offen:** Verifier-Pass `/sdd-verify SKILL-014` + `/sdd-verify SKILL-015`
sowie Jakob-Review der Sprache/Wording vor Status `done`. Commit-Akt
durch Jakob.

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
## 2026-06-05 — [SKILL-013] Governance-Prinzip „Kein Fix ohne Ticket und Code"

**Added:**
- `skill_dev/docs/tickets/agile-sdd-skill/SKILL-013.md` — neues Ticket
  (Status `spec`, MoSCoW Must), 4-teiliges EARS-Set. Vision-Prinzip
  `lessons-aus-live-use-zurueckfuehren`.
- `skills_sources/agile-sdd-skill/SKILL.md` — neuer Abschnitt
  **„0) Governance-Grundregel: Kein Fix ohne Ticket und Code"** direkt nach
  der Einleitung, vor Abschnitt A (prominenteste Stelle). Verbindliches
  Prinzip: jede Mutation an Code/Daten/Konfiguration braucht Ticket + Code/
  Commit, bevor sie angewandt wird. Explizit eingeschlossen: Hotfixes,
  Daten-Bereinigungen/Backfills/manuelle DB-Eingriffe (`UPDATE`/`cancel`/
  Status), Konfig/Infra. Einzige Ausnahme: read-only Lese-/Diagnose-Ops.

**Begruendung:** Lehre aus einer Session, in der direkte DB-Bereinigungen ohne
dediziertes Ticket zu Verwirrung fuehrten (nicht reproduzierbar, nicht im
Audit-Trail).

**Deploy:** `setup.ps1` ausgefuehrt — Aenderung live unter
`~/.claude/skills/agile-sdd-skill/SKILL.md`.

---

## 2026-06-02 — [SKILL-012] Verifier um Visual-UI-Check (Playwright) — Phase 1: Spec + Skeleton

**Added:**
- `skill_dev/docs/tickets/agile-sdd-skill/SKILL-012.md` — neues Ticket
  (Status `spec`), 7-teiliges EARS-Set (A-G), Phasen-Plan
  (Phase 1 Skeleton, Phase 2 Full-Impl, Phase 3 Visual-Regression).
- `skills_sources/agile-sdd-skill/verifier/visual_check.py` — NEU.
  Phase-1-Skeleton mit Dataclasses `VisualCheckResult`/`UrlCheck`, Funktionen
  `run_visual_check()` + `render_report_section()`. Kein lauffaehiger Code —
  Playwright-Integration und Markdown-Rendering sind TODO-Stubs fuer Phase 2.
  Architektur fixed: Verifier installiert NIEMALS Playwright selbst
  (`skipped_tool_missing`-Fallback analog ccusage-Pattern).

**Diff-Vorschlaege (nicht-applied — Phase 2 wendet sie an):**
- `templates/verify-report.md` — neue Sektion `## Visual UI Verification`
  zwischen "Health-Check" und "Manuelle PO-Abnahme" (Block im Ticket
  dokumentiert).
- `templates/TICKET.md` — Frontmatter-Feld `ui_verify_urls:` (Liste mit
  `path` + optional `expect`) im Body-Hinweisblock dokumentieren.
- `verifier/VERIFIER.md` — neuer Schritt 6.5 "Visual-UI-Check" zwischen
  Schritt 6 (API-Schema-Coverage) und Schritt 7 (Token-Aggregation).

**Trigger:** Jakob 2026-06-02 — UI-EARS-Wellen in Immobewertung
(T097/T101/T103) wurden vom Verifier nur als `partial` markiert, Jakob
musste jedes Mal manuell klicken. Zitat: "So bin ich ja nur ein Tester
statt PO." Komplementaer zu SKILL-007 (Reveal-Visual-Review).

**Phase-Plan:** Phase 1 (heute) = Spec + Skeleton + Diff-Vorschlaege +
ROADMAP/CHANGELOG-Eintraege. **KEIN `setup.ps1`** — Jakob entscheidet
manuell wann deployed wird. Phase 2 = Full Implementation, lauffaehiger
Playwright-Pass, Smoke-Run gegen Immobewertung T097/T103. Phase 3 (optional)
= Visual-Regression mit Baseline-Comparison (Tool-Entscheidung offen).

**Offene PO-Entscheidungen fuer Phase 2/3:**
- Visual-Regression-Tool: pixelmatch (Python) vs. Percy (SaaS) vs.
  Chromatic (SaaS) vs. pure-Python-pixel-diff
- Default-Viewport (1280x800 desktop vs. zusaetzlich Mobile 375x812?)
- Authentication-Flow-Handling (Phase 3+: Cookie-Injection, Test-User-Login)

---

## 2026-06-01 — [operator-templates] 11 fehlende Templates ergaenzt (Pattern-Luecke geschlossen)

**Added (in `skills_sources/operator-templates/templates/`):**
- `draft_mail.md` — Email-Pfad (`delivery_method="email"`) mit `/akquise-agent`-Skill, T088-Check (kein Kaufangebot ohne `done` unterlagen_analyse) + Pflicht-Signatur ankauf@jakse-apartments.de.
- `generic.md` — Fallback-Briefing fuer unbekannte `task_type` (kontrolliert `failed` statt kreativ raten).
- `unterlagen_analyse.md` — `/unterlagen-analyst`-Skill + ClaudeNote + Risk-Verdict (Property-Header-Latest-Read T025).
- `extract_kpis.md` — direkter Worker-Call `workers.extract_kpis.process_property()` (kein LLM, pure Python).
- `research.md` — `/akquise-netzwerk`-Skill oder WebSearch, ClaudeNote-Pflicht-Format + Token-Budget 25k.
- `triage_reopen.md` — Mail aus stumm zurueckholen via Backend-`/reopen`-Endpoint.
- `expose_parser_run.md` (T098 Retrofit) — `/expose-parser`-Skill -> `POST /api/property/{id}/expose-parse-result`.
- `mietlisten_parser_run.md` (T093 Retrofit) — `/mietlisten-parser`-Skill -> `PUT /api/property/{id}/rental-units`.
- `unterlagen_analyst_run.md` (T099 Retrofit) — `/unterlagen-analyst`-Skill -> `POST /api/property/{id}/due-diligence-report`.
- `dokument_klassifizierer_run.md` (T100 Retrofit) — `/dokument-klassifizierer`-Skill -> `POST /api/document/{id}/classification-result`.
- `marktanalyse_run.md` (T095) — `/marktanalyse`-Skill -> Region- oder Property-Level-Persist.
- `risiko_scanner_run.md` (T096) — `/risiko-scanner`-Skill mit **2-Call-Stabilitaets-Pattern** -> `POST /api/property/{id}/risk-scan-result`.

**Trigger:** Live-Pattern-Luecke aus Immobewertung — 3-Drafts-Operator + P235-Sequenz haben gemeldet, dass `templates/draft_mail.md` + `templates/generic.md` lokal fehlen (SKILL.md referenzierte sie, aber nur `platform_message_draft.md` + `pdf_vision_ocr.md` waren vorhanden). Subagents mussten Pattern manuell rekonstruieren -> Verdoppelte Arbeit + inkonsistente Outputs.

**Pattern-Konsistenz:** Alle neuen Templates folgen dem etablierten Pattern (Briefing-Variablen, Phase-1-Skill-Call, Phase-2-Persist-API, Phase-3-Task-Complete, "Was du NIEMALS tun darfst"-Block). SKILL-010 API-Schema-Mitdenken-Hinweis ist in den 5 `_run`-Templates verlinkt.

**Deploy:** `setup.ps1` ausgefuehrt — alle 13 Templates (11 neu + 2 vorhandene) jetzt unter `~/.claude/skills/operator-templates/templates/` verfuegbar.

**Smoke:** Grep `templates/draft_mail.md|templates/generic.md` zeigt Referenzen aus SKILL.md PLUS existierende Files.

---

## 2026-06-01 — [SKILL-010] API-Schema-Pflicht in TICKET.md + VERIFIER.md + Implementer-Briefing-Standards

**Added:**
- `skills_sources/agile-sdd-skill/templates/TICKET.md` — Pflicht-Sektion `## API-Schema-Kontrakt` mit 4 Checkboxen + Frontmatter-Hinweis `api_endpoints_extended: yes|no|n/a`.
- `skills_sources/agile-sdd-skill/verifier/VERIFIER.md` — Neuer Pflicht-Check-Schritt 6 "API-Schema-Coverage-Check" (Diff → openapi.json → partial-Regel + Folge-Ticket-Empfehlung). Token-Aggregation wandert auf Schritt 7.
- `skills_sources/agile-sdd-skill/templates/IMPLEMENTER_BRIEFING_STANDARDS.md` — NEU. Wiederverwendbare Standard-Bloecke "API-Schema-Mitdenken", "Implementer-Hygiene", "Skill-Code-Pfad" fuer jeden Implementer-Subagent-Prompt.
- `skills_sources/agile-sdd-skill/SKILL.md` — Sektion "Implementer-Briefing-Standards" in B + Templates-Tabelle erweitert.
- `skills_sources/operator-templates/SKILL.md` — Block "MCP/API-Schema-Hinweis" der bei Persist-Endpoints die GET-Symmetrie prueft.
- Memory: `feedback_api_schema_pflicht.md` + 1-Zeile-Index in `MEMORY.md`.
- `skill_dev/tests/test_skill_010_api_schema_check.py` — 6 Tests (3 EARS + 3 Bonus), alle gruen.

**Deploy:** `setup.ps1` ausgefuehrt — Skills-Deploy-Schritt erfolgreich, alle neuen Files unter `~/.claude/skills/` sichtbar.

**Trigger:** Live-Anti-Pattern T103a (Immobewertung) — neue Property-Felder aus T092/T101 wurden nie via `GET /api/property/{id}` ausgeliefert. Strukturell verhindern statt im Nachgang Folge-Tickets schieben.

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
