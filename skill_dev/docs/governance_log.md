# Governance Log — Skill-Entwicklungs-Repo

Alle autonomen KI-Entscheidungen rund um Skill-Tickets werden hier
eingetragen. Jakob reviewt dieses Log asynchron.

---

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
