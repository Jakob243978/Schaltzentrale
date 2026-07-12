# SKILLS_VISION.md — Portfolio-Constitution aller Skills (skills_sources-Root)

> [!info] Neuer Standort seit 2026-07-12 (skill_dev aufgeloest)
> Diese Datei wurde von `skill_dev/docs/SKILLS_VISION.md` nach
> `skills_sources/SKILLS_VISION.md` verschoben (`git mv`, History erhalten). Sie ist
> die **uebergreifende Skill-Bau-Constitution** fuer ALLE Skills — weder reine
> SDD- noch reine PO-Methodik (die leben in den jeweiligen `PROJECT_VISION.md`),
> sondern Portfolio-Governance: was wird ueberhaupt ein Skill, wie bleibt er schlank,
> wie werden Lessons zurueckgefuehrt. Jeder Skill referenziert sie als geerbte
> Prinzipien-Quelle. Append-only-Hoheit bleibt bei Jakob (Prinzipien nur ergaenzen,
> nie ueberschreiben). Prinzip 7 (`skill-tickets-leben-im-skill-unterverzeichnis`)
> ist durch die Dezentralisierung ueberholt — bewusst stehen gelassen (Historie),
> Neu-Formulierung entscheidet Jakob.

> [!warning] Initial-Befuellung (TICKET-083, 2026-05-25)
> Diese Vision ist die erste Niederschrift fuer das Skill-Entwicklungs-Repo
> (Eat-Your-Own-Dogfood). Sie wurde aus dem Material in TICKET-083 Teil B
> abgeleitet. Jakob: bitte review und schaerf wo noetig — du bist der
> finale PO. Aenderungen werden im **Aktualisiert**-Log unten append-only
> festgehalten, Vision wird *geschaerft*, nicht ueberschrieben.

> [!info] Hinweis
> Diese Datei ist die **Verfassung** fuer ALLE aktiv genutzten
> Claude-Code-Skills (agile-sdd-skill, po-skill, operator-templates,
> obsidian-skills, …). Sie wird in jedem Skill-Implementer-Bootstrap
> mit-gelesen und in jedem `/po-challenge` auf Skill-Tickets referenziert.
> **Eine** Vision fuer alle Skills — Skill-Identitaet (was er macht) lebt
> pro Skill in `skills_sources/<skill>/README.md`. Skill-**Methodik** (wie
> wir Skills bauen + warum) ist zentral hier.

---

## Vision-Statement

Skills muessen das Coding-Erlebnis fuer Jakob + KI **vereinfachen, nicht
verkomplizieren**. Sie sind wiederverwendbar ueber Projekte hinweg, lernen
aus Live-Use und bleiben so schlank wie moeglich. Wenn ein Skill mehr
Reibung erzeugt als er einspart, gehoert er weg — nicht aufgeblaeht.
Skills sind das Werkzeug, mit dem Jakob 1-Personen-mit-KI-Setup das Tempo
gegenueber 10-Personen-Teams haelt: Methodik wird einmal scharf gemacht
und in jedem Projekt automatisch verfuegbar, statt sie in jeder neuen
Codebase neu zu lernen.

---

## Kern-Prinzipien

1. `skill-muss-multi-projekt-tauglich-sein` — Kein hartkodierter
   Projekt-Code im Skill (kein "Immobewertung"-Pfad im SKILL.md, kein
   `data/immo.db`-Reference). Alles projekt-spezifische geht via Konfig
   (`po-config.yaml`, `sdd-config.yaml`) oder Plug-in-Hooks. Wenn ein
   Skill nur fuer ein Projekt sinnvoll ist, ist es kein Skill — es ist
   Projekt-Code.

2. `skill-schlanker-als-was-er-ersetzt` — Wenn der Skill mehr Aufwand
   verursacht als er spart, geht er weg. Konkreter Test: Kann der gleiche
   Workflow ohne Skill in <= der gleichen Zeit + mit gleicher Qualitaet
   gemacht werden? Wenn ja: Skill loeschen oder einfacher machen.

3. `dogfood-zwingt-qualitaet` — Skills entwickeln Skills nach ihrer
   eigenen Methodik. SDD + PO-Skill werden auf SKILL-Tickets in diesem
   Repo angewandt (Spec, Verifier, Vision-Prinzip-Match). Wenn die eigene
   Methodik fuer Skill-Tickets unbrauchbar ist, ist sie fuer Projekt-
   Tickets vermutlich auch unbrauchbar — meta-zirkulaer, aber genau das
   ist der Punkt.

4. `lessons-aus-live-use-zurueckfuehren` — Anti-Pattern, die in Projekten
   entdeckt werden, landen als Pattern im Skill. Beispiel: T082
   (Implementer-Hygiene) entstand aus T078/T079-Token-Overrun in
   Immobewertung — die Regel wandert ins Skill, statt im Projekt-Repo zu
   verstauben. Live-Use ist die einzige Wahrheit; theoretische Skills
   ohne 2+ reale Anwendungen sind verdaechtig.

5. `keine-skill-fuer-skills-sake` — Jeder neue Skill muss klaren
   Mehrfach-Use-Case haben (mindestens 2 Projekte ODER 1 wiederkehrendes
   Pattern, das mit Sicherheit nochmal kommt). Cool-zu-haben ist kein
   Skill-Grund. Im Zweifel: 30 Tage warten, dann nochmal pruefen.

6. `skill-code-getrennt-von-skill-meta` — Code lebt in
   `<Schaltzentrale>/skills_sources/<skill>/`, Meta (Tickets, Vision,
   ADRs, Outcomes) lebt in `<Schaltzentrale>/skill_dev/`. Verwirrung
   zwischen den beiden Schichten ist eine haeufige Fehlerquelle —
   strikte Trennung erzwingen.

7. `skill-tickets-leben-im-skill-unterverzeichnis` — Skill-Tickets in
   `skill_dev/docs/tickets/` werden pro Skill in ein Sub-Verzeichnis
   einsortiert (`docs/tickets/<skill-name>/SKILL-NNN.md`,
   Skill-Verzeichnisname = exakt der Name aus `skills_sources/`).
   Cross-Cutting-Tickets (mehrere Skills betroffen) landen in
   `docs/tickets/cross-cutting/`. Ticket-Nummern bleiben **global**
   weiterzaehlend (nicht pro Skill von vorn), damit Memory-Eintraege,
   governance_log und Commit-Referenzen eindeutig bleiben. Verifier-
   Reports liegen pro Skill in `docs/tickets/<skill>/verify/`. Begruendung:
   bei 3+ parallel entwickelten Skills wird eine flache Ticket-Liste
   unuebersichtlich, und Sub-Agents koennen sich auf den Skill-Kontext
   fokussieren ohne durch fremde Tickets zu lesen. Eingefuehrt 2026-05-29
   bei 9 aktiven SKILL-Tickets + neuem n8n-human-readable-Skill.

---

## Outcome-Metriken

- **skills_aktiv_pro_projekt** — Anzahl Skills, die in einem Projekt
  tatsaechlich genutzt werden (CLAUDE.md hat `## Skill: X`-Block).
  Quelle: Grep ueber alle `claude_projects/*/CLAUDE.md`. Ziel: Coverage
  steigt, ohne dass Skills aufgeblaeht werden.

- **token_saving_pro_skill_nutzung** — Token-Verbrauch eines Skill-
  gestuetzten Workflows vs. baseline (kein Skill, gleicher Workflow).
  Quelle: Subjektive Schaetzung aus Implementer-Berichten + langfristig
  Token-Logs der Subagent-Calls. Ziel: positives Delta (Skill spart),
  nicht negatives (Skill kostet mehr als er bringt).

- **anti_pattern_im_skill_patterns_ordner** — Anzahl dokumentierter
  Anti-Pattern in `skills_sources/<skill>/patterns/` (z.B.
  `implementer-hygiene.md`). Quelle: `ls`. Ziel: waechst monoton —
  jede Live-Erfahrung wird verstetigt.

- **projekte_die_einen_skill_nutzen** — Anzahl Projekte mit
  `## Skill: <name>`-Block in CLAUDE.md, pro Skill. Quelle: Grep ueber
  alle Projekt-CLAUDE.md. Ziel: jeder produktive Skill hat >= 2 Projekte
  (sonst Verdacht auf "skill-fuer-skills-sake").

- **time_to_new_skill_in_neues_projekt** — Median-Zeit, einen
  existierenden Skill in einem neuen Projekt scharf zu schalten
  (`/po-init`, `/sdd-init`, Hooks aktivieren). Quelle: manuelle
  Stoppuhr beim naechsten Setup. Ziel: < 10 Min — sonst ist die
  Init-Sequenz zu schwergewichtig.

---

## Was NICHT im Scope ist

- **Allgemeines Tooling** (eigene IDE-Plugins, MCP-Server,
  CLI-Wrappers) — nur Claude-Code-Skills im
  `~/.claude/skills/`-Format. MCP-Server sind eine andere Welt
  (Composio, Anthropic-SDK) und gehoeren NICHT hierher.

- **Skill-Marketplace / Public Skills** — wir teilen aktuell nichts
  oeffentlich. Skills sind intern, kein README-pflichtiges Open-Source-
  Bundle. Wenn ein Skill spaeter public-relevant wird:
  `git subtree split` macht das in einem Schritt.

- **Multi-Stakeholder-Vision** — kein Voting, kein Community-Input,
  kein PR-Gatekeeper. Jakob ist alleiniger Skill-PO. Alle anderen
  Konstrukte erzeugen Overhead ohne Mehrwert in einem 1-Personen-Setup.

- **Skills, die nur einen einzigen Projekt-Workflow abbilden** —
  siehe `keine-skill-fuer-skills-sake`. Solche Workflows bleiben
  projekt-spezifisches Tooling (Workers, Slash-Commands im
  Projekt-CLAUDE.md).

- **Automatische Skill-Discovery / Auto-Trigger via LLM-Klassifizierung**
  — Skills werden deterministisch aktiviert (CLAUDE.md-Block,
  Slash-Command, expliziter Bootstrap). Auto-Discovery hat bei
  Immobewertung wiederholt nicht zuverlaessig getriggert (siehe Globale
  CLAUDE.md "Skill-Bootstrap-Regel").

---

## Aktualisiert (Append-only Log)

## 2026-07-12 — Dezentralisierung: jeder Skill wird self-contained SDD+PO-Projekt
**Wer:** Architektur-Umbau-Subagent (im Auftrag Jakob).
**Grund:** Skills sollen eigenstaendig an Kunden ausrollbar sein und von diesen
mit eigenem SDD/PO weiterentwickelt werden koennen (Upstream-Review-Flow: Kunde
legt eigene SKILL-Tickets an, Jakob reviewt + entscheidet ueber Upstream-Merge).
Zentrale Entwicklung in `skill_dev/` skaliert dafuer nicht.
**Aenderung:** Per-Skill-Tickets aus `skill_dev/docs/tickets/<skill>/` per `git mv`
in `skills_sources/<skill>/docs/tickets/` migriert (agile-sdd-skill 14, creative-studio
62, po-skill 4, reveal-presentation 2, web-mobile-design 1). Jeder dieser 5 Skills
erhielt eine eigene SDD+PO-Initialisierung (PROJECT_VISION, sdd-config, po-config,
DEFERRED, po-outcomes, governance_log, adr/, CHANGELOG, ROADMAP, CLAUDE.md).
**Hinweis zu Prinzip 6/7:** Diese Prinzipien (`skill-code-getrennt-von-skill-meta`,
`skill-tickets-leben-im-skill-unterverzeichnis`) beschreiben den bisherigen
zentralen Zustand. Sie bleiben append-only stehen; die operative Realitaet ist
seit heute dezentral (Meta lebt PRO Skill). Jakob schaerft die Prinzip-Formulierung
bei Gelegenheit — bewusst nicht durch den Subagent ueberschrieben (Vision-Hoheit).
**Verbleibend zentral:** `docs/tickets/cross-cutting/` (SKILL-005, SKILL-011),
`docs/tickets/n8n-human-readable/` (noch kein Skill-Source), diese SKILLS_VISION
(Skill-Bau-Methodik als gemeinsame Klammer) + governance_log-Historie.

## 2026-05-29 — Prinzip 7 ergaenzt (`skill-tickets-leben-im-skill-unterverzeichnis`)
**Wer:** Reorganisations-Subagent (Opus 4.7 1M context) im Rahmen
der Tickets-Sub-Struktur-Migration (Vorbereitung paralleler Skill-
Entwicklung, neuer Skill `n8n-human-readable` startet jetzt).
**Grund:** Bei 9 SKILL-Tickets + 4. Skill in Arbeit wurde die flache
Ticket-Liste in `docs/tickets/` unuebersichtlich. Sub-Agents lesen
fremde Tickets ohne Mehrwert; Skill-Fokus ging verloren.
**Aenderung:** Prinzip 7 ergaenzt — Tickets liegen pro Skill in einem
Sub-Verzeichnis, Verifier-Reports in `<skill>/verify/`,
Ticket-Nummern bleiben global weiterzaehlend, Cross-Cutting in
eigenem `cross-cutting/`-Verzeichnis. Verzeichnis-Konvention in
`docs/tickets/README.md` festgeschrieben.

## 2026-05-25 — Initial-Befuellung (TICKET-083)
**Wer:** Implementer-Subagent (Opus 4.7 1M) im Rahmen von TICKET-083,
abgeleitet aus dem Material in Teil B des Tickets.
**Grund:** Skill-Entwicklungs-Repo erstmalig aufgesetzt — Eigene
Vision-Constitution fuer Skills, sodass Skill-Tickets nicht mehr in
Projekt-Repos (Immobewertung etc.) verwaessern.
**Aenderung:** Komplette Datei neu — alle Sektionen
(Vision-Statement, 6 Kern-Prinzipien, 5 Outcome-Metriken, 5
Out-of-Scope-Negationen) initial befuellt aus TICKET-083 Teil B
+ Erweiterungen aus Dogfood-Beobachtung (Prinzip 6
`skill-code-getrennt-von-skill-meta`).
