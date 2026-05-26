# Governance Log — Skill-Entwicklungs-Repo

Alle autonomen KI-Entscheidungen rund um Skill-Tickets werden hier
eingetragen. Jakob reviewt dieses Log asynchron.

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
