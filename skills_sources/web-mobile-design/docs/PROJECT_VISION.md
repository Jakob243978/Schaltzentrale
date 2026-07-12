# PROJECT_VISION.md — web-mobile-design

> [!info] Verfassung dieses Skills
> Wird in jedem Implementer-Bootstrap mit-gelesen und in jedem `/po-challenge`
> referenziert. Änderungen append-only im **Aktualisiert**-Log.

> [!warning] Dezentralisiert aus skill_dev/ (2026-07-12)
> Seit dem Architektur-Umbau ein **self-contained SDD+PO-Projekt**. Jakob ist finaler PO.

---

## Vision-Statement

`web-mobile-design` ist eine **ladbare Checkliste + Heuristik**, die jede
Web-Surface (Landing-Page, App-UI, Dashboard, Formular, Kunden-Portal) mobil
tauglich macht — kurz bevor HTML/CSS geschrieben wird und bevor "fertig" gemeldet
wird. Der Skill verhindert die immer gleichen Mobile-Fehler (zu kleine
Touch-Targets, iOS-Zoom durch <16px-Inputs, Horizontal-Scroll, fehlende
safe-area-insets) systematisch, statt sie im Nachhinein einzeln zu entdecken. Er
ist der Qualitäts-Anker für responsives Bauen in einem Setup, das keine separate
QA-Instanz hat.

---

## Kern-Prinzipien

1. `mobile-first-vor-desktop` — Layout wird ab dem kleinen Viewport gedacht
   (Auto-Stack-Grid, fluide Typo mit hohen Mobile-Minima), nicht herunterskaliert.
2. `check-vor-dem-fertig-melden` — Die Checkliste wird zweimal aktiv: vor dem
   Schreiben und vor dem "fertig". Ein übersprungener Check ist ein Bug.
3. `touch-targets-und-16px-inputs-sind-pflicht` — 44px/48dp Targets,
   16px-Input-Minimum (iOS-Zoom), sichtbarer Fokus, Kontrast >= 4.5:1. Nicht verhandelbar.
4. `kein-horizontal-scroll` — Der Body scrollt nie horizontal; breite Inhalte
   scrollen in ihrem eigenen Container.
5. `heuristik-nicht-aesthetik` — Der Skill entscheidet Tauglichkeit/Regeln, NICHT
   die ästhetische Richtung (dafür frontend-design) oder Ad-Creatives (creative-studio).
6. `lessons-aus-live-use-zurueckfuehren` — Real gefundene Mobile-Bugs werden als
   Checklisten-Punkt/Heuristik im Skill verstetigt.

---

## Outcome-Metriken

- **mobile_regelverstoesse_pre_fertig** — Anzahl Verstöße, die der Pre-"fertig"-Check
  noch findet. Quelle: Review-Notiz. Ziel: sinkend (Prävention greift früher).
- **surfaces_mit_check_belegt** — Anteil gebauter Surfaces, bei denen der Check
  dokumentiert lief. Quelle: Implementer-Berichte. Ziel: 100%.
- **projekte_die_diesen_skill_nutzen** — Projekte mit Nutzung. Ziel: >= 2.

---

## Was NICHT im Scope ist

- Ästhetische Richtungs-Entscheidungen (dafür frontend-design).
- Ad-/Social-Creatives (dafür creative-studio).
- Backend-/Performance-Tuning jenseits der Core-Web-Vitals-Heuristik.

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
**Änderung:** Vision erstmals skill-lokal niedergeschrieben. 1 Ticket aus
`skill_dev/docs/tickets/web-mobile-design/` hierher migriert.
