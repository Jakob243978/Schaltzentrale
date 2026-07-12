# PROJECT_VISION.md — reveal-presentation

> [!info] Verfassung dieses Skills
> Wird in jedem Implementer-Bootstrap mit-gelesen und in jedem `/po-challenge`
> referenziert. Änderungen append-only im **Aktualisiert**-Log.

> [!warning] Dezentralisiert aus skill_dev/ (2026-07-12)
> Seit dem Architektur-Umbau ein **self-contained SDD+PO-Projekt**. Jakob ist finaler PO.

---

## Vision-Statement

`reveal-presentation` baut aus Research-Content **eine einzelne, in sich
geschlossene reveal.js-Datei** — inklusive detaillierter Speaker-Notes. Der Skill
nimmt Jakob (und der KI) die mechanische Slide-Bau-Arbeit ab und erzwingt gute
Präsentations-Prinzipien: eine Message pro Slide, Headline-First mit
Fragment-Reveal, viel Weißraum. Zwei Style-Modi (Default für Stakeholder-Decks,
Editorial für Jakob Sebovs Personal Brand) decken beide Anlässe ab, ohne dass
jemand von Hand CSS schreibt.

---

## Kern-Prinzipien

1. `single-file-selbstenthaltend` — Output ist EINE Datei, offline lauffähig,
   ohne externe Abhängigkeiten. Verschickbar per Doppelklick.
2. `eine-message-pro-slide` — Jede Folie trägt genau eine Aussage. Überladene
   Slides sind ein Bug, kein Stilmittel.
3. `speakernotes-tragen-die-tiefe` — Recherche-Detail lebt in
   `speakernotes.md` + `aside class="notes"`, nicht auf der Folie.
4. `zwei-modi-eine-engine` — Default und Editorial teilen sich denselben Bau-Pfad;
   der Stil ist Parameter, kein Fork.
5. `skill-schlanker-als-was-er-ersetzt` — Schneller + konsistenter als Slides von
   Hand; sonst gehört der Skill verschlankt.
6. `lessons-aus-live-use-zurueckfuehren` — Visual-Review-Erkenntnisse (Overflow,
   Kontrast, Fragment-Timing) werden als Regel/Check im Skill verstetigt.

---

## Outcome-Metriken

- **decks_ohne_manuelle_css-korrektur** — Anteil Decks, die ohne Hand-CSS
  präsentierfertig sind. Quelle: Implementer-Berichte. Ziel: hoch.
- **visual_review_findings_pro_deck** — Overflow/Kontrast/Timing-Findings pro
  Deck. Quelle: Visual-Review (SKILL-007). Ziel: sinkend.
- **projekte_die_diesen_skill_nutzen** — Projekte/Kontexte mit Nutzung. Ziel: >= 2.

---

## Was NICHT im Scope ist

- Mehrdatei-Slide-Frameworks / Build-Pipelines (bewusst single-file).
- Ästhetische Sonderwünsche jenseits der zwei definierten Modi (erst als Idee an Jakob).
- Live-Präsentations-Hosting / Remote-Control-Server.

---

## Kunden-Weiterentwicklung (Upstream-Review-Flow)

Der Skill ist eigenständig an Kunden ausrollbar. Kunden legen **eigene
SKILL-Tickets** in `docs/tickets/` an; der Original-Maintainer **Jakob** reviewt
und entscheidet über Upstream-Übernahme. Kunden-Tickets tragen
`origin: customer/<name>` im Frontmatter.

---

## Aktualisiert (Append-only Log)

## 2026-07-12 — Dezentralisierung zu self-contained SDD+PO-Projekt
**Wer:** Architektur-Umbau-Subagent
**Grund:** Skill soll eigenständig ausrollbar + kundenseitig weiterentwickelbar sein.
**Änderung:** Vision erstmals skill-lokal niedergeschrieben. 2 Tickets aus
`skill_dev/docs/tickets/reveal-presentation/` hierher migriert.
