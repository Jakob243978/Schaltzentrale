# PROJECT_VISION.md — agile-sdd-skill

> [!info] Verfassung dieses Skills
> Wird in jedem Implementer-Bootstrap mit-gelesen und in jedem `/po-challenge`
> referenziert. Änderungen append-only im **Aktualisiert**-Log — die Vision wird
> *geschärft*, nicht neu geschrieben.

> [!warning] Dezentralisiert aus skill_dev/ (2026-07-12)
> Seit dem Architektur-Umbau ist dieser Skill ein **self-contained SDD+PO-Projekt**.
> Meta lebt hier, nicht mehr zentral in `skill_dev/`. Jakob ist finaler PO.

---

## Vision-Statement

`agile-sdd-skill` ist die **Methodik-Verfassung**, mit der ein KI-Agent
eigenständig Software entwickelt, ohne dass der Business-Owner eine Zeile Code
schreibt — und ohne dass Nachvollziehbarkeit verloren geht. Spec zuerst, jede
Mutation über ein Ticket, jede Architektur-Weiche als ADR, jede Anforderung mit
Test und Verifier-Pass belegt. Der Skill ist der Grund, warum ein
1-Personen-mit-KI-Setup die Kontrolle behält, wo ein reines "Vibe-Coding" in
Cognitive Debt versinkt.

---

## Kern-Prinzipien

1. `kein-fix-ohne-ticket-und-code` — Jede Änderung an Code/Daten/Config braucht
   Ticket UND Commit, bevor sie angewandt wird. Dringlichkeit ist kein Freibrief.
   Einzige Ausnahme: reine Lese-/Diagnose-Operationen.
2. `spec-first-vor-code` — Akzeptanzkriterien (EARS) stehen vollständig, bevor
   Code entsteht. Bei M/L/XL zusätzlich eine Lösungs-Skizze (Design-Phase light).
3. `ein-ears-mindestens-ein-test` — Pro EARS-Satz mindestens ein Test, grün vor
   dem Verify-Pass. Traceability-Matrix macht Lücken sichtbar.
4. `verifier-in-frischer-session` — Der Verifier-Subagent prüft ohne
   Implementer-Bias in eigener Session. `review` → `done` nie ohne Report.
5. `living-doc-statt-nachtrag` — PROJECT_SPEC, CHANGELOG, ROADMAP,
   Governance-Log werden *während* der Arbeit gepflegt, nicht gesammelt am Ende.
6. `skill-schlanker-als-was-er-ersetzt` — Erzeugt der Skill mehr Bürokratie als
   Nutzen, wird er verschlankt. Skill-angemessen, kein Overhead um seiner selbst willen.
7. `lessons-aus-live-use-zurueckfuehren` — Anti-Pattern aus realer Anwendung
   (z.B. Implementer-Hygiene aus Token-Overruns) werden als Regel im Skill verstetigt.
8. `dogfood-zwingt-qualitaet` — SDD entwickelt sich nach seiner eigenen Methodik
   (Spec, Verifier, Vision-Prinzip-Match). Ist die eigene Methodik fuer Skill-Tickets
   unbrauchbar, ist sie es fuer Projekt-Tickets vermutlich auch.

> [!info] Portfolio-Constitution (geerbte Prinzipien)
> Die uebergreifende Skill-Bau-Constitution (multi-projekt-tauglich, keine-skill-
> fuer-skills-sake, code-getrennt-von-meta u.a.) lebt in
> `skills_sources/SKILLS_VISION.md`. Ticket-`vision_principle:`-Slugs duerfen sowohl
> auf hiesige als auch auf geerbte Portfolio-Prinzipien verweisen.

---

## Outcome-Metriken

- **implementer_iterations_pro_ticket** — Sessions bis `done`. 1 = perfekte Spec,
  >= 3 = Spec war unscharf. Quelle: Verify-Report-Felder. Ziel: sinkend.
- **tickets_mit_verify_report** — Anteil `done`-Tickets mit Verify-Report.
  Quelle: `docs/tickets/verify/`. Ziel: 100%.
- **ears_ohne_test** — Anzahl EARS-Sätze ohne zugeordneten Test.
  Quelle: TRACEABILITY-Matrix. Ziel: 0.
- **projekte_die_diesen_skill_nutzen** — Projekte mit `## Skill: Agile SDD` in
  CLAUDE.md. Ziel: >= 2.

---

## Was NICHT im Scope ist

- Ad-hoc-Mutation ohne Ticket ("mal eben direkt in der DB").
- Multi-Stakeholder-Voting / PR-Gatekeeper (1-Personen-Setup, Jakob ist PO).
- Auto-Discovery via LLM-Klassifizierung (Skills werden deterministisch aktiviert).
- Schwergewichtige Prozess-Bürokratie, die die eigentliche Ticket-Arbeit blockiert.

---

## Kunden-Weiterentwicklung (Upstream-Review-Flow)

Der Skill ist eigenständig an Kunden ausrollbar. Kunden legen **eigene
SKILL-Tickets** in `docs/tickets/` an und entwickeln mit eigenem SDD/PO weiter.
Der Original-Maintainer **Jakob** reviewt und entscheidet über Upstream-Übernahme.
Kunden-Tickets tragen `origin: customer/<name>` im Frontmatter.

---

## Aktualisiert (Append-only Log)

## 2026-07-12 — Dezentralisierung zu self-contained SDD+PO-Projekt
**Wer:** Architektur-Umbau-Subagent
**Grund:** Skill soll eigenständig ausrollbar + kundenseitig weiterentwickelbar sein.
**Änderung:** Vision erstmals skill-lokal niedergeschrieben (abgeleitet aus SKILL.md
+ geerbter Skill-Constitution). 14 Tickets aus `skill_dev/docs/tickets/agile-sdd-skill/`
hierher migriert.
