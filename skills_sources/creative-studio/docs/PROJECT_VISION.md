# PROJECT_VISION.md — creative-studio

> [!info] Verfassung dieses Skills
> Diese Datei ist die **Verfassung** des Skills `creative-studio`. Sie wird in
> jedem Implementer-Bootstrap mit-gelesen und in jedem `/po-challenge`
> referenziert. Änderungen werden im **Aktualisiert**-Log am Ende append-only
> festgehalten — die Vision wird *geschärft*, nicht neu geschrieben.

> [!warning] Dezentralisiert aus skill_dev/ (2026-07-12)
> Dieser Skill ist seit dem Architektur-Umbau ein **self-contained SDD+PO-Projekt**.
> Vision + Tickets + Governance leben jetzt hier, nicht mehr zentral in
> `skill_dev/`. Jakob: bitte review + schärfen — du bist der finale PO.

---

## Vision-Statement

`creative-studio` verwandelt Content + Brand-Tokens in **markenkonforme
Social-Ad-Creatives** (Bild und Video) für Meta (FB/IG) — Safe-Zone-korrekt,
Multi-Format, projektübergreifend. Der Skill ist der Hebel, mit dem ein
1-Personen-mit-KI-Setup Ad-Creatives in der Menge und Konsistenz produziert, für
die ein Team sonst eine Design-Abteilung bräuchte. Brand + Content kommen immer
als **Parameter** — der Skill trägt nie einen hartkodierten Projektwert. So läuft
dieselbe Engine für jede Marke, jeden Kunden.

---

## Kern-Prinzipien

### Produkt-Prinzipien (dieser Skill)

1. `brand-und-content-als-parameter` — Kein Marken-/Projektwert steht im Skill-Code.
   Farben, Fonts, Logos, Copy kommen als Input. Ein hartkodierter Wert ist ein Bug.
2. `safe-zone-ist-nicht-verhandelbar` — Jedes Format respektiert die zentral in
   `specs.py` definierten Safe-Zones. Ein Creative, dessen CTA in der UI-Overlay-Zone
   verschwindet, ist Ausschuss — egal wie schön es aussieht.
3. `standards-zentral-in-specs` — Formate, Safe-Zones, Constraints leben an *einer*
   Stelle (`specs.py`). Kein Format-Wissen wird über Module verstreut dupliziert.
4. `bild-und-video-gleichwertig` — Bild-Pfad (Playwright/HTML-CSS) und Video-Pfad
   (Remotion, 9:16) sind erstklassige, konsistente Ausgaben — kein Zweitrang-Video.

### Skill-Methodik-Prinzipien (geerbt aus der Skill-Constitution)

5. `skill-muss-multi-projekt-tauglich` — Der Skill ist über Projekte hinweg
   wiederverwendbar; alles Projekt-Spezifische geht via Parameter/Config.
6. `skill-schlanker-als-was-er-ersetzt` — Erzeugt der Skill mehr Reibung als er
   spart, wird er einfacher gemacht, nicht aufgebläht.
7. `lessons-aus-live-use-zurueckfuehren` — Anti-Pattern aus echten Ad-Runs landen
   als Pattern/Test im Skill, statt im Projekt-Repo zu verstauben.

---

## Outcome-Metriken

- **creatives_pro_run** — Anzahl valider Creatives (Bild+Video) pro Batch-Lauf.
  Quelle: `manifest.json` je Batch. Ziel: hoher Durchsatz ohne Safe-Zone-Verstöße.
- **safe_zone_verstoesse** — Anteil Renders, die die Safe-Zone verletzen.
  Quelle: Visual-Check / Tests. Ziel: 0.
- **framework_ablesbar_aus_jedem_artefakt** — Anteil Artefakte, deren Copy-Framework
  aus variant_id + Dateiname + Metadaten eindeutig hervorgeht (SKILL-086). Ziel: 100%.
- **projekte_die_diesen_skill_nutzen** — Anzahl Projekte mit `## Skill: creative-studio`
  in CLAUDE.md. Ziel: >= 2 (sonst Verdacht auf "skill-fuer-skills-sake").

---

## Was NICHT im Scope ist

- Hartkodierte Marken-/Projektwerte im Skill-Code.
- Ästhetische Richtungs-Entscheidungen (dafür Brand-Tokens / eine Design-Instanz).
- Nicht-Meta-Plattformen als Erstbürger (Fokus FB/IG-Formate).
- Ein Asset-Management-/DAM-System — der Skill rendert, verwaltet keine Mediathek.

---

## Kunden-Weiterentwicklung (Upstream-Review-Flow)

Dieser Skill ist eigenständig an Kunden ausrollbar. Kunden dürfen im ausgerollten
Skill **eigene SKILL-Tickets** anlegen (`docs/tickets/`) und den Skill mit
eigenem SDD/PO weiterentwickeln. Der Original-Maintainer (**Jakob**) reviewt diese
Erweiterungen und entscheidet, ob ein Kunden-Ticket ins Upstream-Original
übernommen wird. Kunden-Tickets bekommen dabei einen erkennbaren Marker (z.B.
`origin: customer/<name>` im Frontmatter), damit Upstream-Review + Merge
nachvollziehbar bleiben.

---

## Aktualisiert (Append-only Log)

## 2026-07-12 — Dezentralisierung zu self-contained SDD+PO-Projekt
**Wer:** Architektur-Umbau-Subagent
**Grund:** Skill soll eigenständig an Kunden ausrollbar + von diesen
weiterentwickelbar sein (Upstream-Review-Flow).
**Änderung:** Vision erstmals skill-lokal niedergeschrieben (abgeleitet aus
SKILL.md + geerbten Skill-Constitution-Prinzipien). Tickets aus
`skill_dev/docs/tickets/creative-studio/` hierher migriert.
