# Governance Log — Skill-Entwicklungs-Repo

Alle autonomen KI-Entscheidungen rund um Skill-Tickets werden hier
eingetragen. Jakob reviewt dieses Log asynchron.

---

## 2026-06-18 — SKILL-014 + SKILL-015 umgesetzt: Default-Entscheidung + Empfehlungs-First

**Tickets:** SKILL-014 (agile-sdd-skill) + SKILL-015 (po-skill)
**Status:** beide `spec` -> Skill-Code gepatcht -> Deploy via setup.ps1 ->
`review` (Verifier-Pass + Jakob-Review fehlen vor `done`).

**Trigger:** Jakob 2026-06-18, *"Mein meistgenutzter Move ist 'rueckfragen,
was er empfehlen wuerde'. Ich fuehl mich entscheidungshemmt."* Vorschlag
1 (Default-Entscheidung) + Vorschlag 2 (Empfehlungs-First) aus
`skill_dev/proposals/2026-06-18_sdd_default_decision_plus_voice_mode.md`
durch Jakob freigegeben. Vorschlaege 3 + 4 (Voice-Mode +
Vision-Drift-Counter) warten ca. 2 Wochen — explizit als 2-Wochen-Plan
in beiden SKILL.md-Dateien dokumentiert.

**Autonome Entscheidungen:**

- **Naechste freie SKILL-Nummern: 014 (agile-sdd) + 015 (po-skill).**
  Globale Weiterzaehlung (siehe `docs/tickets/README.md`), nicht
  pro-Skill. Bisher hoechste Nummer war SKILL-013.
- **Zwei getrennte Tickets statt eines Cross-Cutting-Tickets.** Die
  Patches treffen zwei verschiedene Skill-Sources mit getrenntem Lifecycle
  (Versionierung), Quer-Verweis im Frontmatter (`related_tickets`) reicht.
  Ein Cross-Cutting-Ticket waere unnoetig zentralisierend.
- **Skill-Versions-Bump beide:** agile-sdd `0.5` -> `0.6`, po-skill `0.1`
  -> `0.2` (Pflicht-Konvention bei jedem SKILL.md-Patch).
- **Vorschlaege 3 + 4 NICHT als SKILL-Ticket angelegt.** Sind als
  2-Wochen-Plan in den Out-of-Scope-Sektionen der Tickets + in beiden
  SKILL.md-Dateien (Sektionen L.5, M.5, C.5.6) explizit dokumentiert.
  Kein eigenes Ticket in `idea`-Status angelegt, um keinen aktiven
  "Folge-Task-Push" zu erzeugen (siehe `feedback_skeleton_first`).
- **Empfehlungs-First-Beispiel im DB-Migration-Kontext** als
  Default-Beispiel in Sektion M.1 gewaehlt — generischer als ein
  Projekt-spezifisches Trello-/n8n-Beispiel.

**Artefakte modifiziert/neu (`skills_sources/agile-sdd-skill/`):**
- `SKILL.md` — v0.5 -> v0.6; **NEU Sektion L** (Default-Entscheidungs-
  Regel mit MUST-Bedingungen + STOPP-Liste + Doku-Pflicht + Anti-Pattern);
  **NEU Sektion M** (Empfehlungs-First-Format + Beispiel/Anti-Beispiel +
  Selbst-Check + Verhaeltnis zu L). Eingefuegt nach Sektion K, vor
  "Templates-Referenz".
- `SKILL.md.bak_2026-06-18` — Backup vor Patch.

**Artefakte modifiziert/neu (`skills_sources/po-skill/`):**
- `SKILL.md` — v0.1 -> v0.2; **NEU Sektion C.5** ("Empfehlungs-First in
  /po-challenge") direkt nach der Akut-Liste in Sektion C, vor Sektion D.
  Pflicht-Format + 4 zulaessige Empfehlungen (annehmen/parken/ablehnen/
  Vision schaerfen) + Spiegelung Sektion M + Akut-Listen-Verhaeltnis.
- `SKILL.md.bak_2026-06-18` — Backup vor Patch.

**Artefakte modifiziert (`skill_dev/`):**
- `docs/tickets/agile-sdd-skill/SKILL-014.md` — neu, Status `spec`.
- `docs/tickets/po-skill/SKILL-015.md` — neu, Status `spec`.
- `CHANGELOG.md` — Eintrag oben.
- `docs/governance_log.md` — dieser Eintrag.

**Artefakte neu (`vault/Memory/`):**
- `feedback_default_decision_empfehlung_first.md` — Kern-Regel + STOPP-
  Liste + Konsequenz + Verweise auf SKILL-014/015 + Sourcedoku.
- `MEMORY.md` — Index-Eintrag.

**ADR:** keins (Repo-Konvention, kein `docs/adr/` in skill_dev — selbe
Linie wie SKILL-009).

**Review:** ausstehend (Jakob reviewt Sprache, Wording, Wirkung in 1-2
Sessions; Commit erfolgt durch Jakob).

---

## 2026-05-31 — SKILL-009 umgesetzt: inbox/-Konvention in agile-sdd-skill (v0.4 → v0.5)

**Ticket:** SKILL-009 (inbox/-Konvention fuer agile-sdd)
**Implementer-Modell:** claude-opus-4-8 (1M context) — echte Skill-Code-Aenderung
in `skills_sources/agile-sdd-skill/` (NICHT nur Meta).
**Status:** SKILL-009 `idea` → `spec` → `review`. Skill-Quelle real geaendert;
vor `done` fehlen Verifier-Pass + `setup.ps1`-Deploy.

**Trigger:** Jakob-Auftrag (Schaltzentrale-Session). Live-Vorbild aus
2026-05-28 (Bewerbung-Bot v0.6-Spec: Janina schickte WhatsApp-Material, das
Jakob unter `workflows/prod/bewerbung-bot/inbox/` ablegte). Konvention soll
nativ im Skill leben.

**Autonome Entscheidungen — die 3 offenen Klaerungen des Tickets entschieden:**
- **Klaerung 1 — Bootstrap-Hinweis PASSIV** (nicht aktiv nachfragen): Agent
  macht Inbox-Material beim Bootstrap nur sichtbar ("X Files in inbox/ warten
  auf Spec"), unterbricht nicht und blockiert nicht. Aktives Nachfragen wuerde
  jeden Bootstrap stoeren — Vision `skill-schlanker-als-was-er-ersetzt`.
- **Klaerung 2 — KEINE Auto-Transkription von Audio**: Agent liest nur nativ
  Lesbares (PNG/JPG/PDF/Text/Markdown). OGG/MP3-Whisper-Transkription
  ausgeklammert → bleibt ggf. separater Skill. Haelt SKILL-009 bei Aufwand S.
  Bei Audio im inbox/: passiver Hinweis + Bitte um Text-Zusammenfassung.
- **Klaerung 3 — Konvention gilt fuer ALLE agile-sdd-Projekte**, inkl.
  `skill_dev` selbst (`skill_dev/inbox/`). Kein Sonderfall-Handling.

**Architektur-Entscheidung — .gitignore-Default = ignorieren:**
Inbox-Material kann sensibel sein (Screenshots mit Kundendaten, private
Sprachnachrichten). Default beim Projekt-Setup: `inbox/*` ignorieren ausser
`.gitkeep` (analog fuer `inbox/archive/`). Nur die Ordner-Struktur wird
getrackt, nicht der Inhalt. Projekte koennen die Regel bewusst lockern, wenn
unkritisches Material versioniert werden soll — der **Default ist ignorieren**.
Kein eigenes ADR angelegt: dieses Repo nutzt **kein** `docs/adr/` (existiert
nicht; etablierter Mechanismus ist dieser Governance-Log — siehe SKILL-006/008).
Daher Architektur-Entscheidung hier dokumentiert. **ADR:** keins (Repo-Konvention).

**Weitere Entscheidung — kein INBOX_README.md-Template:** Die technischen
Hinweise des Tickets nannten optional `templates/INBOX_README.md`. Bewusst
weggelassen: die Konvention lebt vollstaendig in SKILL.md Sektion K; ein
Parallel-Template waere Redundanz + Pflege-Last bei Aufwand S (Anti-Pattern
gegen `skill-schlanker-als-was-er-ersetzt`).

**Artefakte modifiziert/neu (`skills_sources/agile-sdd-skill/`):**
- `SKILL.md` — v0.4→v0.5; Sektion A Bootstrap-Punkt 10 (passiver inbox-Check);
  Sektion B `inbox_source:` im Ticket-Format; Checkliste "Neues Projekt"
  Punkt 10 (inbox/ + .gitkeep + .gitignore-Default), alt-10→11; **NEU
  Sektion K** (vollstaendige inbox-Konvention).
- `templates/TICKET.md` — optionaler `inbox_source:`-Hinweis im Frontmatter.

**Artefakte modifiziert (`skill_dev/`):**
- `docs/tickets/agile-sdd-skill/SKILL-009.md` — Status, Vision-Prinzip +
  Skill-Version im Frontmatter, AC abgehakt + auf Default-Entscheidungen
  gemappt, Klaerungen als Callouts, Ergebnis-Block.
- `docs/governance_log.md` — dieser Eintrag.

**NICHT angefasst (bewusst):**
- `setup.ps1` NICHT ausgefuehrt — Deploy nach `~/.claude/skills/` macht
  Haupt-Agent/Jakob. Bis dahin wirkt v0.5 NICHT im laufenden Skill.
- Kein git commit/push.
- Keine anderen Repos (AgentischesArbeiten, ~/.claude/skills/ unberuehrt).
- Keine Loeschung bestehender Inhalte.

**Offen / PO-Abnahme noetig:**
- Verifier-Pass `/sdd-verify SKILL-009` (frische Session) → dann `review` → `done`.
- `setup.ps1` einmalig ausfuehren (Deploy v0.5).
- PO: Klaerungen 1–3 + .gitignore-Default + INBOX_README-Verzicht absegnen.

## 2026-06-05 — Governance-Prinzip „Kein Fix ohne Ticket und Code" im agile-sdd-Skill verankert

**Ticket:** SKILL-013
**Entscheidung:** Neuer Abschnitt „0) Governance-Grundregel: Kein Fix ohne
Ticket und Code" in `skills_sources/agile-sdd-skill/SKILL.md` — platziert
direkt nach der Einleitung und VOR Abschnitt A (Bootstrap-Sequenz), damit das
Prinzip die prominenteste Stelle im Skill einnimmt und jeder Agent es zuerst
liest. Prinzip: jede Mutation an Code/Daten/Konfiguration braucht Ticket +
Code/Commit, bevor sie angewandt wird; ausdruecklich inkl. Hotfixes, Daten-
Bereinigungen/Backfills/manuelle DB-Eingriffe und Konfig/Infra; einzige
Ausnahme read-only.
**Begruendung:** Lehre aus einer Session, in der direkte DB-Bereinigungen ohne
dediziertes Ticket zu Verwirrung fuehrten (nicht reproduzierbar, kein Audit-
Trail). Alternative „nur im CLAUDE.md des Projekts verankern" verworfen — die
Regel ist multi-projekt-relevant (Vision-Prinzip `lessons-aus-live-use-
zurueckfuehren`) und gehoert daher in den Skill selbst, nicht in ein Projekt-
Repo. Platzierung als eigener Abschnitt „0)" statt Erweiterung von Abschnitt I
(Governance-Log), weil es ein Handlungs-Prinzip ist, kein Logging-Format.
**Betroffene Dateien:**
- `skills_sources/agile-sdd-skill/SKILL.md` (neuer Abschnitt 0)
- `skill_dev/docs/tickets/agile-sdd-skill/SKILL-013.md` (NEU)
- `skill_dev/CHANGELOG.md` (Eintrag)
- `skill_dev/docs/governance_log.md` (dieser Eintrag)
**ADR:** keins
**Deploy:** `setup.ps1` ausgefuehrt — Skill live unter `~/.claude/skills/agile-sdd-skill/`.
**Review:** ausstehend

---

## 2026-06-01 — operator-templates: 11 fehlende Templates ergaenzt (kein SKILL-Ticket — operative Patch-Aktion)

**Trigger:** Live-Befund aus Immobewertung — zwei Subagents (3-Drafts-Operator, P235-Sequenz) haben gemeldet, dass `templates/draft_mail.md` und `templates/generic.md` lokal fehlen, obwohl `SKILL.md` sie referenziert. Tatsaechlicher Befund war breiter: nur 2 von 13 in der SKILL.md gelisteten Templates existierten (`platform_message_draft.md`, `pdf_vision_ocr.md`).

**Implementer-Modell:** claude-opus-4-7 (1M context). Token-Budget eingehalten (< 60k).

**Autonome Entscheidungen:**
- **Kein neues SKILL-Ticket angelegt.** Ist eine reine Pattern-Luecke (Files fehlten, SKILL.md war bereits korrekt) — kein methodisches Skill-Problem, das ein Ticket rechtfertigt. Eintrag im CHANGELOG + governance_log reicht. Bei wiederkehrendem Pattern (Templates verlieren sich) sollte ein SKILL-Ticket "operator-templates Coverage-Test" angelegt werden, das via Smoke-Test verhindert, dass SKILL.md mehr Templates referenziert als existieren.
- **Pattern-Treue zu `platform_message_draft.md` + `pdf_vision_ocr.md`** — alle neuen Templates folgen Briefing-Variablen + 3-Phasen-Aufbau (Skill-Call / Persist-API / Task-Complete) + "Was du NIEMALS tun darfst"-Block.
- **`extract_kpis.md` explizit OHNE Skill-Call** — Worker ist pure Python (`workers/extract_kpis.py`), Skill-Call waere Token-Verschwendung. Template fordert direkten Worker-Call + Diff-Pruefung.
- **SKILL-010-Hinweis** ("API-Schema-Mitdenken") in allen 5 `_run`-Templates eingebaut — operative Konsequenz aus SKILL-010-Ticket.
- **T088-Hard-Check** in `draft_mail.md` eingebaut: bei `intent=='kaufangebot'` Pflicht-Check auf `cascade-state.unterlagen_analyse_status=='fresh'`. Ergaenzt den Cascade-Selector-Server-Side-Check um Subagent-Side-Defense.

**Betroffene Dateien:**
- `skills_sources/operator-templates/templates/draft_mail.md` (NEU)
- `skills_sources/operator-templates/templates/generic.md` (NEU)
- `skills_sources/operator-templates/templates/unterlagen_analyse.md` (NEU)
- `skills_sources/operator-templates/templates/extract_kpis.md` (NEU)
- `skills_sources/operator-templates/templates/research.md` (NEU)
- `skills_sources/operator-templates/templates/triage_reopen.md` (NEU)
- `skills_sources/operator-templates/templates/expose_parser_run.md` (NEU, T098 Retrofit)
- `skills_sources/operator-templates/templates/mietlisten_parser_run.md` (NEU, T093 Retrofit)
- `skills_sources/operator-templates/templates/unterlagen_analyst_run.md` (NEU, T099 Retrofit)
- `skills_sources/operator-templates/templates/dokument_klassifizierer_run.md` (NEU, T100 Retrofit)
- `skills_sources/operator-templates/templates/marktanalyse_run.md` (NEU, T095)
- `skills_sources/operator-templates/templates/risiko_scanner_run.md` (NEU, T096, 2-Call-Stabilitaet)
- `skill_dev/CHANGELOG.md` (Eintrag)
- `skill_dev/docs/governance_log.md` (dieser Eintrag)

**Deploy:** `setup.ps1` ausgefuehrt — Skill-Deploy erfolgreich, alle 13 Templates jetzt unter `~/.claude/skills/operator-templates/templates/` deployt.

**Smoke-Test:** Grep `templates/draft_mail.md|templates/generic.md|templates/unterlagen_analyse.md|templates/extract_kpis.md|templates/research.md|templates/triage_reopen.md` in `~/.claude/skills/operator-templates/` zeigt SKILL.md-Referenzen — Files existieren alle.

**Folge-Ticket-Vorschlag (offen, NICHT angelegt):** `SKILL-NNN` "operator-templates Coverage-Smoke-Test" — `skill_dev/tests/`-Case, der pro Skill mit `templates/`-Subdir verifiziert, dass jede in `SKILL.md`-Tabellen-Zeile referenzierte Datei existiert. Verhindert Pattern-Luecken in Zukunft.

---

## 2026-06-01 — SKILL-010 implementiert: API-Schema-Pflicht im SDD-Skill

**Trigger:** Jakob (2026-06-01, nach Live-PO-Klick T097+T101 in Immobewertung) — T103a musste spontan nachgeschoben werden, weil `GET /api/property/{id}` die neuen Region-/JSON-Felder aus T092/T101 nie ausgeliefert hat. Pattern: Modell + Worker + Tests sind gruen, API-Schema wird vergessen.

**Implementer-Modell:** claude-opus-4-7 (1M context). Token-Budget eingehalten (< 60k).

**Autonome Entscheidungen:**
- **Neue Sektion `## API-Schema-Kontrakt` in TICKET.md auf H2-Ebene** (nicht H3 wie im Ticket-Auftrag formuliert), damit sie zur bestehenden H2-Struktur ("## Akzeptanzkriterien", "## Technische Hinweise") passt. Test entsprechend angepasst (akzeptiert beide Ebenen).
- **Eigenes File `IMPLEMENTER_BRIEFING_STANDARDS.md`** angelegt (Teil-C-Option B) statt SKILL.md aufzublaeen — Standard-Bloecke sind nun zentral wiederverwendbar fuer Operator-Templates + Lead-Claude + Slash-Commands. SKILL.md verweist auf das File.
- **VERIFIER-Token-Aggregation auf Schritt 7 verschoben** (war Schritt 6) — API-Schema-Coverage-Check ist jetzt Schritt 6. Reihenfolge logisch: zuerst inhaltliche Pruefung, dann Cost-Tracking.
- **`partial`-Cap statt Hard-Fail** im Verifier: Wenn API-Schema-Coverage fehlt, wird Status auf `partial` gesetzt + Folge-Ticket-Notiz empfohlen — nicht hart `fail`, damit das Implementer-Ticket nicht blockiert wird (Lueke ist Schema-Symmetrie, nicht Feature-Defekt).

**Betroffene Dateien:**
- `skills_sources/agile-sdd-skill/templates/TICKET.md`
- `skills_sources/agile-sdd-skill/verifier/VERIFIER.md`
- `skills_sources/agile-sdd-skill/templates/IMPLEMENTER_BRIEFING_STANDARDS.md` (NEU)
- `skills_sources/agile-sdd-skill/SKILL.md`
- `skills_sources/operator-templates/SKILL.md`
- `~/.claude/projects/.../memory/feedback_api_schema_pflicht.md` (NEU)
- `~/.claude/projects/.../memory/MEMORY.md` (Index-Zeile)
- `skill_dev/tests/test_skill_010_api_schema_check.py` (NEU, 6/6 gruen)

**ADR:** keins (keine Architektur-Entscheidung — reine Skill-Pattern-Erweiterung).

**Verify-Report:** ausstehend — Ticket steht auf `review`. `/sdd-verify SKILL-010` empfohlen.

**Review:** ausstehend (PO-Klick).

**Vorbestehender Pre-Existing-Fund:** `test_skill_dev_smoke.py::test_ears_g2_skill_tickets_listed` ist rot wegen Duplicate `SKILL-010.md` in `n8n-human-readable/`-Sub-Verzeichnis (vom Sub-Agent 2 angelegt, vor dieser Session). Nicht behoben — out of scope SKILL-010. Folge-Ticket fuer Umnummerierung empfohlen.

---

## 2026-05-29 — Tickets-Sub-Struktur eingefuehrt (Vorbereitung paralleler Skill-Arbeit)

**Trigger:** Jakob-Auftrag (Schaltzentrale-Session) — bei 9 SKILL-Tickets in
flacher Liste + Start eines vierten Skills (`n8n-human-readable`, Sub-Agent 2)
wurde die Substruktur faellig. Sub-Agents sollen pro Skill-Kontext lesen
koennen, ohne fremde Tickets zu screenen.
**Implementer-Modell:** claude-opus-4-7 (1M context), reine Meta-/
Struktur-Aenderung im Skill-Dev-Repo — kein Skill-Code-Touch in
`skills_sources/`.
**Status:** Migration durchgefuehrt, Smoke-Tests angepasst.

**Autonome Entscheidungen:**
- **Globale Ticket-Nummerierung beibehalten** (nicht pro Skill von 1):
  SKILL-001 … SKILL-009 bleiben einzigartig. Begruendung: Memory-Eintraege,
  governance_log und Commit-Referenzen nennen `SKILL-NNN` ohne Skill-Pfad
  — Pro-Skill-Nummerierung wuerde Konflikte (zwei `SKILL-001.md`) und
  Mehrdeutigkeit in Logs verursachen. Konvention in
  `docs/tickets/README.md` fixiert.
- **Skill-Zuordnung pro Ticket** (Mapping):
  - SKILL-001 (PO-Skill bauen) → `po-skill/`
  - SKILL-002 (Vision↔Features-Bridge) → `po-skill/`
  - SKILL-003 (Implementer-Hygiene) → `agile-sdd-skill/`
  - SKILL-004 (EARS-Pre-Conditions) → `agile-sdd-skill/`
  - SKILL-005 (Skill-Versions-Anker) → `cross-cutting/` (betrifft agile-sdd + po-skill)
  - SKILL-006 (KNOWN_FAILURES.md) → `agile-sdd-skill/`
  - SKILL-007 (Reveal-Visual-Review) → `reveal-presentation/`
  - SKILL-008 (Reveal-Wrapper-Fixes) → `reveal-presentation/`
  - SKILL-009 (inbox/-Konvention) → `agile-sdd-skill/`
- **Reserved-Verzeichnisse fuer Skills ohne Ticket**: `obsidian-skills/`,
  `operator-templates/`, `n8n-human-readable/` — leer mit `.gitkeep`, damit
  das erste Ticket direkt am richtigen Platz landet. Sub-Agent 2 legt sein
  Ticket fuer `n8n-human-readable` dort ab.
- **Verifier-Reports pro Skill** (`<skill>/verify/`): nicht ein zentrales
  verify/, sondern pro Skill-Unterverzeichnis. Vorteil: Verifier-Subagent
  liest nur den eigenen Skill-Kontext.
- **Prinzip 7 in SKILLS_VISION.md ergaenzt**
  (`skill-tickets-leben-im-skill-unterverzeichnis`) + Aktualisiert-Log-
  Eintrag. Sub-Struktur ist damit als Vision-Konvention fixiert, nicht
  nur als ad-hoc-Layout.
- **Smoke-Tests angepasst**: `test_ears_g2_skill_tickets_listed` greppt
  jetzt rekursiv (`TICKETS.rglob("SKILL-*.md")`) statt flach, damit die
  Migration nicht den Test zerschiesst. Erwartungs-Set (SKILL-001/002/003)
  bleibt erhalten — sie liegen jetzt nur eine Ebene tiefer.

**Artefakte modifiziert/angelegt:**
- `skill_dev/docs/tickets/README.md` (NEU — Sub-Struktur-Konvention)
- `skill_dev/docs/tickets/<skill>/` (9 Tickets verschoben in 4 Skill-Unterverzeichnisse)
- `skill_dev/docs/tickets/{obsidian-skills,operator-templates,n8n-human-readable}/` (NEU, leer)
- `skill_dev/docs/tickets/{<skill>}/verify/.gitkeep` (pro Skill ein verify/)
- `skill_dev/CLAUDE.md` (Bootstrap-Sequenz + Verzeichnisstruktur + Konventions-Block updated)
- `skill_dev/docs/SKILLS_VISION.md` (Prinzip 7 + Aktualisiert-Log)
- `skill_dev/tests/test_skill_dev_smoke.py` (rglob statt glob, Skill-Pfad-Mapping in Erwartung)

**NICHT angefasst (bewusst):**
- `skills_sources/` — keine Skill-Code-Aenderung, kein `setup.ps1`-Re-Run noetig.
- Ticket-Inhalte selbst (Status, Frontmatter, Body) — reine Verschiebung,
  kein Inhalts-Touch.
- Ticket-Nummern — Memory + Logs bleiben kompatibel.

**PO-Abnahme noetig:**
- Vision-Prinzip 7 absegnen (oder schaerfen). Sollte das Mapping fuer
  ein Ticket abweichen (z.B. SKILL-005 nicht cross-cutting sondern
  agile-sdd?) — Verschiebung ist trivial.
- Naming-Check: passt `n8n-human-readable` als Skill-Verzeichnis (vs.
  `n8n-readable`, `n8n-workflow-readable`)? Sub-Agent 2 sollte das in
  seinem Ticket konsistent uebernehmen.

---

## 2026-05-28 — SKILL-008 angelegt — Wrapper-Bugs aus SKILL-007 Live-Anwendung

**Trigger:** Erst-Anwendung von SKILL-007 auf BeyerImmo-Onboarding-
Praesi (16 Slides) am 2026-05-28. Beide Visual-Review-Wrapper scheiterten
Windows-spezifisch: `screenshot_slides.sh` produzierte 16 Chromium-404-
PNGs wegen MSYS-`/tmp/`-Pfad in der URL, `screenshot_slides.ps1` brach
nach Slide 00 mit NativeCommandError ab (chrome.exe-stderr-Zeile triggert
PS-5.1-Quirk trotz erfolgreichem Screenshot). Recovery in der Session
via bash-Inline-Call mit Windows-Pfad — Phase-4-Mechanik selbst hat sich
bewiesen (Slide-11-Overflow gefangen), nur die Liefer-Vehikel sind kaputt.
**Implementer-Modell:** claude-opus-4-7 (1M context), reine Ticket-/
Governance-Aenderung im Meta-Layer, kein Skill-Code-Touch.
**Status:** Ticket angelegt (spec), SKILL-007 bleibt `review`
(Phase-4-Logik unveraendert valid).

**Autonome Entscheidungen:**
- **SKILL-008 Status `spec` direkt** (nicht `idea`): Live-Material
  liegt vor (BeyerImmo-Beleg + konkrete Reproduktions-Pfade beider
  Bugs), Fix-Empfehlungen pro Bug bereits formuliert, 48h-Cooldown
  nicht sinnvoll bei akut blockierender Erfahrung. Vision-Match
  eindeutig (`lessons-aus-live-use-zurueckfuehren` +
  `dogfood-zwingt-qualitaet`) — analog SKILL-007.
- **MoSCoW = Must** (nicht Should): ohne Fix ist SKILL-007 auf Windows
  praktisch unbenutzbar (Phase 4 laeuft nur via Inline-Workaround).
  Abweichung von SKILL-007/SKILL-003-Should-Pattern bewusst — die
  Wrapper sind die einzige automatisierte Schnittstelle zum Phase-4-
  Verfahren.
- **Aufwand = S** (klein): zwei kleine Wrapper-Diffs (Empfehlung
  Variante b je Bug — kleinstes Diff bei robustestem Fix), plus
  Smoke-Test-Erweiterung mit Mindest-PNG-Groessen-Check. Kein Refactor
  der Phase-4-Logik selbst.
- **SKILL-007 NICHT zurueckgestuft** (bleibt `review`): Die Phase-4-
  Logik hat im Live-Test heute gezeigt, dass sie funktioniert (sobald
  die Screenshots da waren, hat das Read-Tool den Slide-11-Overflow
  gefangen). SKILL-008 repariert nur die Liefer-Vehikel, nicht den
  Mechanismus. Verifier-Report fuer SKILL-007 ist davon unabhaengig.
- **KNOWN_FIXES-Block** statt KNOWN_FAILURES-Block in Teil D: weil das
  Ticket die Bugs aktiv behebt — der Block dient als Anker fuer den
  naechsten Implementer, der einen aehnlichen Quirk sieht, nicht als
  Symptom-Recovery-Doku.

**Artefakte angelegt:**
- `skill_dev/docs/tickets/SKILL-008.md` (Wrapper-Fixes, spec, Must)
- `skill_dev/docs/governance_log.md` (dieser Eintrag)

**NICHT angefasst (bewusst):**
- `skills_sources/reveal-presentation/tools/screenshot_slides.sh` —
  Fix-Aktion gehoert in den Implementer-Pass.
- `skills_sources/reveal-presentation/tools/screenshot_slides.ps1` — dto.
- `skills_sources/reveal-presentation/SKILL.md` — KNOWN_FIXES-Block
  ist Implementer-Aufgabe (Teil D), nicht Ticket-Anlage.
- `skill_dev/docs/tickets/SKILL-007.md` Status — bleibt `review`.
- `setup.ps1` — kein Skill-Code geaendert, kein Deploy noetig.

**PO-Abnahme noetig:**
- Vision-Prinzip-Match gegenpruefen (Annahme: `lessons-aus-live-use-zurueckfuehren`
  + `dogfood-zwingt-qualitaet` — identisch zu SKILL-007, weil beide
  Tickets aus derselben BeyerImmo-Live-Erfahrung-Ader stammen).
- MoSCoW = Must bestaetigen (oder ggf. auf Should runterstufen, falls
  Jakob die manuelle Inline-Recovery-Methode als akzeptablen
  Dauerzustand ansieht).
- Reihenfolge im Sprint: SKILL-008 sollte vor dem naechsten echten
  reveal-presentation-Build laufen, sonst wiederholt sich die heutige
  Recovery-Schleife.

---

## 2026-05-27 — SKILL-007 angelegt (Reveal-Visual-Review aus BeyerImmo-Live-Schmerz)

**Trigger:** Jakob-Auftrag aus Schaltzentrale-Session abends 2026-05-27 —
direkt nach 1h Feedback-Loops auf BeyerImmo-Onboarding-Praesi
(`KundenAB/BeyerImmo/onboarding/onboarding_office_team.html`). Drei
visuelle Bugs (CSS-Grid auf `.reveal .items > li`, Slide-Hoehe-Overflow,
Sub-Text-Pattern) waren aus HTML-Quellcode allein nicht erkennbar.
Ad-hoc-Loesung mit Chromium-headless-Screenshots hat funktioniert →
Pattern soll in Skill wandern.
**Implementer-Modell:** claude-opus-4-7 (1M context), reine Doku-/
Ticket-Aenderung im Meta-Layer
**Status:** Ticket angelegt, Skill-Code unveraendert (folgt im
Implementer-Pass)

**Autonome Entscheidungen:**
- **SKILL-007 Status `spec` direkt** (nicht `idea`): Live-Material
  liegt vor (BeyerImmo-Beispiel, validierte Methode), 48h-Cooldown
  nicht sinnvoll bei akuter Schmerz-Erfahrung mit direktem Auftrag.
  Vision-Match eindeutig (`lessons-aus-live-use-zurueckfuehren` +
  `dogfood-zwingt-qualitaet`).
- **MoSCoW = Should** (nicht Must): Skill funktioniert ohne Phase 4
  weiter; Erweiterung ist Reibungs-Reduktion, nicht Existenz-
  notwendig. Konsistent mit SKILL-003/SKILL-006-Einordnung.
- **Pre-Conditions-Format verwendet** (analog SKILL-004/SKILL-006):
  Dogfood auch fuer dieses Ticket — auch wenn SKILL-004 noch nicht
  done ist, ist das neue Format als optionale Best-Practice schon
  zulaessig (Warning-only-Design erlaubt das).
- **Skill-Source unveraendert**: Implementer-Pass folgt; dieses
  Ticket ist Spec-Layer.
- **Inhaltliche Review explizit Out-of-Scope**: Jakob hat das
  ausdruecklich gesagt — Faktentreue/Story-Bogen/Tonalitaet bleiben
  manuell, kein Skill-Scope.
- **PowerShell-Variante des Wrapper-Scripts mit aufgenommen** (Teil
  B): globaler CLAUDE.md gibt PowerShell als Default-Shell auf
  Windows, Bash-only-Script waere unvollstaendig.

**Artefakte angelegt:**
- `skill_dev/docs/tickets/SKILL-007.md` (Reveal-Presentation Visual-
  Review-Pass, spec, Should)
- `skill_dev/ROADMAP.md` (Eintrag in Should-Sektion)
- `skill_dev/docs/governance_log.md` (dieser Eintrag)

**PO-Abnahme noetig:**
- SKILL-007 Vision-Prinzip-Match gegen SKILLS_VISION.md
  gegenpruefen (Annahme: `lessons-aus-live-use` + `dogfood` passen,
  ggf. Schaerfung wenn Jakob abweicht)
- Reihenfolge im Sprint: parallel zu SKILL-004/SKILL-006 bearbeitbar,
  Skill-Code (`reveal-presentation/`) ist unabhaengig vom agile-sdd-
  Skill — kein Blocker
- Optional: reveal-presentation v0.1-Anker in `skill-versions.md`
  als Vorgriff (SKILL-005 deckt das nicht explizit ab)

---

## 2026-05-26 — Jakob-Entscheidung: SKILL-006 hochgestuft + SKILL-004 ohne Strict-Mode

**Trigger:** Jakobs Review der drei Tickets aus der Knowledge-
Persistence-Recherche (siehe vorheriger Eintrag).
**Implementer-Modell:** claude-opus-4-7 (1M context), reine Doku-Aenderung
**Status:** Tickets + Roadmap aktualisiert, kein Skill-Code-Touch

**Jakob-Entscheidungen (NICHT autonom — explizit angeordnet):**
- **SKILL-006 `idea` → `spec`**: Alle 3 Tickets sollen parallel
  bearbeitbar sein, nicht erst auf SKILL-004-Outcome warten.
  KNOWN_FAILURES.md liefert eigenstaendig Wert; Wirkung ist unabhaengig
  von Pre-Conditions. Pre-Condition „SKILL-004 done + 14d" aus
  SKILL-006 entfernt; bleibt nur „SKILL-005 done" als Voraussetzung.
- **SKILL-004 ohne Strict-Mode-Option**: Pre-Conditions bleiben
  **dauerhaft Warning-only**, kein Hard-Block via
  `SDD_STRICT_PRE_CONDITIONS=1` geplant. Begruendung Jakob: „Denke
  nicht, dass es immer passen wird" — Pre-Conditions passen nicht in
  jedes Ticket, Regel ist „pruefe + dokumentiere wenn relevant", nicht
  „blockiere ohne". Kein Future-Promise auf Strict-Mode, explizit als
  Design-Entscheidung dokumentiert.

**Artefakte modifiziert:**
- `skill_dev/docs/tickets/SKILL-006.md` (Status spec, Begruendungsblock
  ersetzt, Pre-Conditions + Voraussetzung + Verknuepfte-Tickets neu)
- `skill_dev/docs/tickets/SKILL-004.md` (Warning-Only-Block ergaenzt im
  Business-Ziel, Out-of-Scope-Eintrag „Hard-Block / Strict-Mode" auf
  Design-Entscheidung umgestellt, Technische-Hinweise glaettend
  „erzwingt" → „warnt")
- `skill_dev/ROADMAP.md` (SKILL-006 von Should-„wartet auf SKILL-004"
  in Now-Bereich, parallel zu SKILL-004)

---

## 2026-05-26 — Knowledge-Persistence-Recherche → SKILL-004/005/006 + DEFERRED

**Trigger:** Subagent-Auftrag aus Schaltzentrale-Session — Recherche
`Researcher/jakob/spec-driven-development/recherche/2026-05-26_Knowledge_Persistence_Flaky_Processes.md`
hat 3 Empfehlungen identifiziert (KNOWN_FAILURES.md, EARS-Pre-Conditions,
Auto-Memory). Subagent sollte Tickets anlegen statt Skill-Code direkt zu
aendern.
**Implementer-Modell:** claude-opus-4-7 (1M context), strukturelle Aufgabe
**Status:** Tickets angelegt, Skill-Code unveraendert

**Autonome Entscheidungen:**
- **SKILL-004 (Pre-Conditions) Status `spec` direkt** (nicht `idea`):
  Recherche markiert das eindeutig als "DIE eine Massnahme, die das
  Problem am meisten loest". Vision-Match (`lessons-aus-live-use` +
  `dogfood-zwingt-qualitaet`) eindeutig. 48h-Cooldown wurde NICHT
  angewandt — Material liegt vor, Empfehlung gehoert zur fundierten
  Recherche, kein "im-Flow-aufgekommener" Wunsch.
- **SKILL-005 (Versions-Anker) Status `spec`**: Voraussetzung fuer
  SKILL-004/006 (Rollback-Punkt). Trivial im Aufwand (XS), aber
  Reihenfolge wichtig. Datei `docs/skill-versions.md` bereits initial
  befuellt (Vorgriff auf Ticket-Inhalt), weil Phase 4 des Auftrags den
  Anker explizit verlangt — Ticket dokumentiert dann die formale
  Verankerung + Smoke-Test.
- **SKILL-006 (KNOWN_FAILURES.md) Status `idea`**: Recherche nennt das
  ebenfalls als wichtiges Pattern, aber komplementaer zu SKILL-004.
  Begruendung fuer `idea` statt `spec`: Vision-Prinzip
  `skill-schlanker-als-was-er-ersetzt` verlangt zu pruefen ob
  SKILL-004 das Problem schon allein loest, bevor wir eine zweite
  Mechanik draufpacken. Outcome-Review-Hook (14d nach SKILL-004 done)
  ist Pre-Condition.
- **DEF-001 (Auto-Memory) → DEFERRED**: Recherche markiert selbst
  als sekundaer + offene Frage zu Empirie. Vision-Match unklar
  (Ueberlapp mit SKILL-006). Klassischer 48h-Cooldown-Case.
- **Git-Tag NICHT autonom gesetzt**: Konvention im Repo + globale
  CLAUDE.md "Never update git config / no autonomous tags". Jakob
  bekommt den fertigen Tag-Befehl in `docs/skill-versions.md` zum
  Selber-Setzen.
- **Skill-Source unveraendert**: explizite Auftragsregel Phase 5.
  Keine Aenderung an `skills_sources/agile-sdd-skill/` oder
  `skills_sources/po-skill/`. Nur Meta (`skill_dev/`).

**Artefakte angelegt:**
- `skill_dev/docs/tickets/SKILL-004.md` (Pre-Conditions, spec, Must)
- `skill_dev/docs/tickets/SKILL-005.md` (Versions-Anker, spec, Must)
- `skill_dev/docs/tickets/SKILL-006.md` (KNOWN_FAILURES.md, idea, Should)
- `skill_dev/docs/skill-versions.md` (NEU — v0.4-Anker fuer agile-sdd
  + po-skill, mit Rollback-Befehlen und Tag-Vorschlag)
- `skill_dev/docs/DEFERRED.md` (DEF-001 Auto-Memory eingetragen)
- `skill_dev/ROADMAP.md` (3 neue Eintraege, Sprint-Vorschlag erweitert)

**PO-Abnahme noetig:**
- SKILLS_VISION.md gegen neue Tickets gegenchecken — passen 6 Prinzipien?
- Tag `agile-sdd-skill-v0.4-pre-pre-conditions` auf `fe9337a` setzen
  (PowerShell-Befehl in `skill-versions.md` bereit zum Copy-Paste).
- Reihenfolge bestaetigen: SKILL-005 (XS) → SKILL-004 (M, +14d Live) →
  SKILL-006 nach Outcome-Review.

---

## 2026-05-25 — Initial-Setup des Skill-Dev-Repos (TICKET-083)

**Ticket:** TICKET-083 (Immobewertung) — "Skill-Entwicklungs-Repo aufsetzen (Eat Your Own Dogfood)"
**Implementer-Modell:** claude-opus-4-7 (1M context)
**Status:** done

**Autonome Entscheidungen:**
- `/po-init`-Sequenz manuell + inline ausgefuehrt (nicht als Slash-
  Command-Aufruf), weil der PO-Skill-Subagent in einem frischen Repo
  ohne CLAUDE.md sonst nicht sauber laeuft. Material aus TICKET-083
  Teil B 1:1 in `SKILLS_VISION.md` uebertragen + Prinzip 6
  (`skill-code-getrennt-von-skill-meta`) ergaenzt, weil das in der
  Dogfood-Analyse als wiederkehrendes Missverstaendnis aufgetaucht
  ist (Code in `skills_sources/` vs Meta in `skill_dev/`).
- Original-Tickets in Immobewertung (T080/T081/T082) NICHT geloescht —
  Status auf `done` mit Migrations-Note (T080 war eh schon `review`,
  T081/T082 wandern auf `done` mit "siehe SKILL-NNN" Referenz).
- `skill_dev/` als Sub-Tree in Schaltzentrale, kein separater Git-Remote
  (war so in TICKET-083 Designentscheidung festgehalten).

**Migration:**
- TICKET-080 → SKILL-001 (PO-Skill bauen) — Status review (Implementierung
  in T080 erfolgt, Verifier-Pass + Outcome offen)
- TICKET-081 → SKILL-002 (Lift-and-Shift T078/T079) — Status spec
- TICKET-082 → SKILL-003 (Implementer-Hygiene) — Status spec

**Artefakte angelegt:**
- `skill_dev/CLAUDE.md`, `skill_dev/CHANGELOG.md`, `skill_dev/ROADMAP.md`
- `skill_dev/docs/SKILLS_VISION.md`, `docs/po-config.yaml`,
  `docs/DEFERRED.md`, `docs/po-outcomes.md`, `docs/governance_log.md`
- `skill_dev/docs/tickets/SKILL-001.md`, `SKILL-002.md`, `SKILL-003.md`
- `skill_dev/tests/test_skill_dev_smoke.py`

**Memory-Eintrag:** `feedback_skill_tickets_verortung.md` war von Jakob
vor-angelegt; Inhalt geprueft, auf Skill-Repo-Pfad konsistent — keine
Aenderung noetig.

**PO-Abnahme:** Jakob review `SKILLS_VISION.md` + bei Bedarf schaerfen
(Append-only ins Log am Ende der Datei). Danach `setup.ps1` einmalig
ausfuehren, damit die schon vorhandenen Skills (po-skill,
agile-sdd-skill) nach `~/.claude/skills/` deployed werden — am Skill-
**Code** hat dieses Ticket nichts geaendert, aber Folgetickets
(SKILL-002, SKILL-003) tun das dann.

## 2026-06-13 — SKILL-014 angelegt (spec): surface-Klassifikator + Web⇒UI-Verifier-Pflicht

**Ticket:** SKILL-014 (`agile-sdd-skill/`)
**Entscheidung:** Neues Skill-Dev-Ticket (Status `spec`) fuer eine generische
agile-sdd-Regel: Ticket-Frontmatter `surface: web|backend|n8n|infra` +
Done-Gate-Pflicht „`surface: web` ⇒ UI-Verifier-Pass (Playwright/headless),
`surface: n8n` ⇒ Execution-Check statt Browser". Enthaelt konkreten Patch-Vorschlag
(welche SKILL.md-Zeilen + Templates). **Noch NICHT** in `skills_sources/` appliziert
und NICHT deployed — wartet auf Jakobs Review + setup.ps1.
**Begruendung:** Live-Lesson aus AgentischesArbeiten (RBAC-Dashboard TICKET-051
ohne erzwungenen Browser-Check gebaut; Luecke nur durch Jakobs Nachfrage entdeckt).
Komplementaer zu SKILL-012 (liefert die Visual-Check-*Capability*, aber best-effort/
optional) — SKILL-014 ist die *Enforcement-Policy + Klassifikation*, die den Check
bei Web-Surfaces verpflichtend macht. Verortung im skill_dev statt Projekt-Repo
gemaess `feedback_skill_tickets_verortung`.
**Betroffene Dateien:** `docs/tickets/agile-sdd-skill/SKILL-014.md` (neu),
`docs/governance_log.md`. (Projekt-lokale Sofort-Umsetzung liegt in
AgentischesArbeiten TICKET-056.)
**ADR:** keins
**Review:** ausstehend ([J] Patch in skills_sources/agile-sdd-skill applien + setup.ps1)

## 2026-06-23 — Neuer Skill creative-studio initialisiert (SKILL-020/021)

**Ticket:** SKILL-020 (spec), SKILL-021 (idea)
**Entscheidung:** Neuen Skill `creative-studio` aufgesetzt — wiederverwendbare, agentische
Erzeugung von Social-Ad-Creatives (Bild + Video). Scope (Jakob 2026-06-23): EIN Skill für beide
Medien (gemeinsamer Web-Tech-Kern HTML/CSS), Bild zuerst (SKILL-020), Video als Ausbaustufe
(SKILL-021); Erst-Einsatz AgentischesArbeiten (Warteliste-Ads), dann SocialMediaBuilder.
**Begründung:** Bedarf entstand aus der Meta-Ads-Arbeit; statt pro Projekt neu zu bauen → Skill
(Vision-Prinzip `skill-muss-multi-projekt-tauglich-sein`). Wissensgrundlage: 3 Recherche-Docs vom
2026-06-23 (Formate/Safe-Zones, Bild-Generierung Playwright, Video-Automation Remotion) in
AgentischesArbeiten/docs/.
**Stack-Empfehlung (aus Recherche):** Bild = Playwright + HTML/CSS-Template + smartcrop;
Video = Remotion (bzw. ffmpeg/MoviePy als Einstieg). Kein hartkodierter Projekt-Code (Config-getrieben).
**Betroffene Dateien:** docs/tickets/creative-studio/SKILL-020.md, SKILL-021.md (neu);
docs/governance_log.md; ROADMAP.md. Skill-Code (skills_sources/creative-studio/) folgt mit SKILL-020.
**ADR:** keins (folgt ggf. bei Stack-Festlegung in SKILL-020-Umsetzung).
**Review:** ausstehend

## 2026-06-23 — creative-studio implementiert + deployed (SKILL-020/021)

**Ticket:** SKILL-020 (Bild, in_progress), SKILL-021 (Video, in_progress)
**Entscheidung:** Skill `creative-studio` gebaut + via setup.ps1 deployed (live im Harness).
- Bild: specs.py (Standards-als-Code: Formate/Safe-Zones/Constraints/AdContent) + render_image.py
  (Playwright + Jinja2-Template) → erste Bild-Ad (h1-immo) in 3 Formaten generiert + visuell validiert.
- Video: Remotion-Composition (9:16, animiert, Safe-Zone-Padding, Brand-Props) → erste Video-Ad
  (MP4, 180f) gerendert + via remotion-still-Frame validiert.
- SKILL.md + README (Subagent). Brand/Content via Parameter (multi-projekt, Vision-Prinzip 1).
**Begründung:** Jakob wollte beide Erst-Ads heute + Skill „einwandfrei". Beide Ads erzeugt, Standards
als Code (Jakobs Vorgabe), reproduzierbarer Render (package.json-Flags --concurrency=1 --port=3333,
Fix fuer „localhost:3000 got no response").
**Nebenfix:** setup.ps1 um `robocopy /XD node_modules __pycache__ .git .pytest_cache /XF *.pyc`
gehaertet — sonst blaehen Node/Python-Skills das Deploy-Target auf. Gilt fuer ALLE Skills.
**Betroffene Dateien:** skills_sources/creative-studio/** (neu), setup.ps1, SKILL-020/021, ROADMAP, governance.
**ADR:** keins (Stack-Wahl folgt der Recherche; ggf. ADR bei Video-Stack-Festlegung SKILL-021).
**Review:** ausstehend (Verify-Pass + EARS-6 smartcrop offen)

## 2026-06-23 — creative-studio Feature-Backlog aus Recherche A/B/C angelegt (SKILL-023..033)

**Tickets:** SKILL-023..033 (11 Stueck, alle `creative-studio`, Erstellt 2026-06-23) — **nur Tickets +
ROADMAP + dieser Eintrag, KEIN Skill-Code geaendert.**
- **Must (spec):** SKILL-023 (Batch-/Varianten-Engine N Hooks × M Formate × Bild/Video + manifest.json),
  SKILL-024 (Variant-ID-/UTM-Systematik in specs.py — Naming-Single-Source).
- **Should (spec):** SKILL-025 (frameworks.py: Copy-Framework-Katalog + Hook-Bibliothek + 4U-Validator),
  SKILL-026 (DACH-Compliance-Guard ausbauen: UWG/HWG-Heuristik + Ad↔LP-Message-Match), SKILL-027
  (Voiceover-Layer ElevenLabs-Voice-Clone + Untertitel ueber Remotion), SKILL-028 (KI-Disclosure-Gate:
  „KI"-Label + C2PA/Metadaten), SKILL-029 (Brand-Kit als brand.json + Logo-Handling), SKILL-030
  (Vorschau-Galerie gallery.html als QA-Gate).
- **Could (idea):** SKILL-031 (DCO-/Asset-Feed-Export-Modus dco_bundle.json), SKILL-032 (content-aware
  smartcrop fuer --bg-image, loest EARS-6 aus SKILL-020), SKILL-033 (Reporting-Rueckkanal: Insights →
  Winner-Flag via manifest-IDs).
**Implementer-Modell:** claude-opus-4-8 (1M context), Subagent-Auftrag von Jakob („Skill ausbauen, Tickets
anlegen").

**Begruendung:** Wissensgrundlage sind die drei Recherche-Docs vom 2026-06-23 unter
`AgentischesArbeiten/docs/marketing/research/` — (A) `2026-06-23_creative-studio-flow-improvements.md`
(Flow/Features + MoSCoW-Liste), (B) `2026-06-23_ad-copywriting-frameworks.md` (Copy/Frameworks),
(C) `2026-06-23_ki-avatare-voiceover.md` (Voiceover/Disclosure). Der heutige Skill ist ein
Single-Creative-Renderer ohne Varianten-/Pipeline-Schicht und ohne Performance-Rueckkanal; die Tickets
schliessen genau diese Luecken. MoSCoW + Abhaengigkeiten 1:1 aus der Recherche uebernommen
(SKILL-024 → SKILL-023 → SKILL-030/031/033). Verortung im skill_dev gemaess
`feedback_skill_tickets_verortung` (multi-projekt-relevant: AgentischesArbeiten + SocialMediaBuilder).

**Globale Nummerierung:** hoechste bisherige Nummer war SKILL-022 (per Verzeichnis-Scan
`docs/tickets/*/SKILL-*.md` verifiziert) → 023..033 vergeben.

**Betroffene Dateien:** `docs/tickets/creative-studio/SKILL-023.md` … `SKILL-033.md` (11 neu);
`ROADMAP.md` (SKILL-023/024 in Must, 025–030 in Should, 031–033 in neue Could-Tabelle);
`docs/governance_log.md` (dieser Eintrag).
**Skill-Code unveraendert:** `skills_sources/creative-studio/` NICHT angefasst (reine Spec-/Backlog-Arbeit).
**ADR:** keins (reine Ticket-Anlage).
**Review:** ausstehend ([J] MoSCoW + Abhaengigkeiten gegenpruefen; ggf. `/po-prioritize` auf die idea-Tickets).

## 2026-06-24 — creative-studio Feature-Welle implementiert (SKILL-023..035)

**Kontext:** Autonomer 48h-Block (Jakob abwesend). Nach Recherche A-E (5 Docs) den Feature-Backlog
implementiert — orchestriert über parallele Subagenten, Hauptsession als Orchestrator clean gehalten.
**Implementiert + getestet (Status review):**
- SKILL-023 Batch-/Varianten-Engine (`batch.py`) + manifest.json — Must
- SKILL-024 Variant-ID-/UTM-Systematik (`specs.py`) — Must
- SKILL-025 `frameworks.py` (Copy-Frameworks + Hooks + recommend + 4U) — Should
- SKILL-026 DACH-Compliance-Guard (`specs.py`, UWG/HWG-Trigger + Message-Match) — Should
- SKILL-028 KI-Disclosure-Gate (`specs.py`+Template, EU-AI-Act 2026-08-02) — Should
- SKILL-029 Brand-Kit `brand.json` + Logo (`render_image.py`+Template) — Should
- SKILL-030 Vorschau-Galerie (`gallery.py`) — Should
- SKILL-031 DCO-/Asset-Feed-Export (`dco.py`) — Could
- SKILL-032 content-aware smartcrop (`cropping.py`, Face>Saliency) — löst SKILL-020 EARS-6 — Could
- SKILL-034 Brand-Asset-Konvention (`assets.py`) — Should
- SKILL-035 Bild-Komprimierer (`prep_bg.py`) — Should
**Verifikation:** Gesamtsuite **127 passed**, 10 Module integrieren, via setup.ps1 deployed, requirements.txt
ergänzt (smartcrop/opencv/pyyaml). Jeder Subagent: nur eigene Datei + eigene Testdatei (Race-Vermeidung).
**Bewusst offen (spec, brauchen externe Keys/Live — nicht ehrlich autonom testbar):**
SKILL-027 (Voiceover/ElevenLabs-Key), SKILL-033 (Reporting/Live-Insights), SKILL-022 (Auto-Marketing-Ordner).
**Folge-Befund:** manifest.json führt nur `hook` (keine getrennten primary_text/cta) → DCO/Reporting
profitieren von angereichertem Manifest (SKILL-023-Erweiterung, im Backlog vermerken).
**Verify-Pass (/sdd-verify) je Ticket steht noch aus** — bewusst Jakob/Folge-Session überlassen.

## 2026-06-24 — creative-studio: Foto-Hintergrund-Pipeline gehärtet (Live-Einsatz)

**Kontext:** Erste echte Kampagne (Warteliste 2026Q3) mit Jakobs picdrop-Portraits als Ad-Hintergrund.
Drei Fixes beim Live-Einsatz entdeckt + behoben (alle additiv, 127 Tests weiter grün, deployed):
1. **bg_image-Bug:** wurde als `file://` ins Template gesetzt → lädt unter Playwright `set_content` NICHT
   (Foto blieb leer). Fix: `_as_data_uri()` (wie Logo, SKILL-029). render_image.py.
2. **Foto-Scrim verstärkt:** unterer Gradient dunkler (0.96 @100%, 0.80 @64%) für Text-Lesbarkeit auf Foto.
3. **text-shadow** auf eyebrow/headline/subline NUR bei bg_image (Lesbarkeit über hellen Bildpartien).
**Auflösungs-Lehre:** Web-Varianten (1621px) sind für 9:16 (1920px) zu klein → für Foto-Ads die
ORIGINALE (30MP) nutzen, sonst smartcrop-Upscaling-Warnung. In Kampagnen-job.yaml so gesetzt.
**Offen/Politur:** Eyebrow über Gesicht bleibt grenzwertig (text-shadow lindert) — Layout-Feinschliff
bei Bedarf (z.B. Eyebrow-Chip oder bild-abhängige Text-Position). Kein Blocker für den Test.

## 2026-06-24 — creative-studio Welle 2: Ad-Library-Scan + Remotion-Reel-Engine

**Tickets:** SKILL-052 (→ review), SKILL-043/044/045 (→ review). Vorarbeit zu SKILL-046.
Konsolidierter Eintrag von der Hauptsession (Subagenten liessen das Log bewusst in Ruhe).
**SKILL-052 Ad-Library-Scan:** `creative_studio/ad_library.py` (parse / `longevity_score` / aggregate /
hook-patterns / report) + Runbook `templates/ad_library_scan.md` + SKILL.md §9. Echter read-only
MCP-Test (`ads_library_search`, DE) bestätigte die Feld-Shape: **KEIN Spend/Reach abrufbar** →
Longevity-Score `active_days × log(1 + page_variant_count)` + Proxy-Signale, Pflicht-Disclaimer. 22 Tests.
**SKILL-043/044/045 Remotion-Reel-Engine:** `video/src/Captions.tsx` (word-level/Hormozi),
`video/src/AdReel.tsx` (B-Roll via OffthreadVideo + Voiceover + Musik mit Per-Frame-Ducking),
`Root.tsx` `calculateMetadata` (dyn. Dauer), `creative_studio/reel_spec.py` (ReelSpec + Loader/Props/CLI,
Naming aus SKILL-024). **Echter End-to-End-Render verifiziert:** 2 Bronze-HEVC-Clips → Silber
(gebündeltes Remotion-ffmpeg, kein Windows-Codec) → B-Roll + Musik + 8 Captions → **Gold-mp4 2,68 MB,
1080x1920, h264+aac, Exit 0**. Repo nur Proof-Artefakte (<2 MB) + `video/.gitignore`.
**Autonome Entscheidung:** `broll`-Feld additiv über den SKILL-043/044/045-Scope hinaus aufgenommen
(echter Render mit Footage erforderte es) — gehört zu **SKILL-046** (Should), dort als Vorarbeit vermerkt.
**Offen/ehrlich:** Ducking-unter-Voiceover nicht hörbar gegengetestet (kein freies VO-Asset);
B-Roll-Transitions (`TransitionSeries`) = SKILL-046. Remotion-Lizenz ab 4 Personen (solo = frei) als
Risiko in Tickets vermerkt.
**pytest gesamt: 180 passed** (Baseline 174 + 6 SKILL-045, 0 Regressionen). Kein git commit/push.
`setup.ps1`-Deploy nach `~/.claude/skills/` + `/sdd-verify` je Ticket offen.

## 2026-06-25 — creative-studio: Reel-Design-Overhaul SKILL-055/056/057 (Render-belegt)

**Tickets:** SKILL-055, SKILL-056, SKILL-057 (alle → review). Anlass: Jakob-Kritik am ersten Gold-Reel
(„nicht schön, nicht gut lesbar"). Quelle: `AgentischesArbeiten/docs/marketing/research/2026-06-25_reel-design-critique-content-types.md`.
**Umgesetzt:**
- **SKILL-055** Caption-Overhaul: `Captions.tsx` neu — Pill-Kontrast-Layer (Default) + Stroke-Alternative,
  genau 1 Keyword/Phrase (`pickKeywordIndex`), max 2 aktive Tokens + Wort-für-Wort-Reveal, Montserrat Bold
  (`fonts.ts`, lokale TTFs offline-robust), Position 54%.
- **SKILL-056** `TalkingHead.tsx`: Speaker-Layer (O-Ton) + Pill-Captions + Lower-Third + Hook<3s + CTA-Outro.
- **SKILL-057** Reel-Theme-Tokens: Highlight = Brand-Akzent (`#f25d3e`) statt hartem `#ffd400`; neue Keys
  `BRAND_HIGHLIGHT`/`BRAND_CAPTION_FONT`/`BRAND_CAPTION_BG_ALPHA` in `terraform/base-dev/.../branding.env`.
**Render-Beleg (Gold, extern):** VORHER `reel_h1-immo_broll.mp4` · NACHHER `reel_h1-immo_designv2.mp4` (651 KB)
· Talking-Head `reel_talkinghead_proof.mp4` (14,7s, Video+O-Ton, Jakobs echter Sprech-Clip). Frame-Vergleiche
in `tests/artifacts/`. pytest 180→**200 passed**.
**Offen/Refinement:** Talking-Head-Caption-Timing hartkodiert (Whisper = SKILL-043/056-Spec); Captions mittig
überlappen bei tightem Crop das Gesicht → optionaler Caption-Höhen-Prop als Folge-Refinement.
**Kein** git commit/push; `setup.ps1`-Deploy + `/sdd-verify` offen.
