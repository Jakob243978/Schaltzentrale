# PROJECT_VISION.md — po-skill

> [!info] Verfassung dieses Skills
> Wird in jedem Implementer-Bootstrap mit-gelesen und in jedem `/po-challenge`
> referenziert. Änderungen append-only im **Aktualisiert**-Log.

> [!warning] Dezentralisiert aus skill_dev/ (2026-07-12)
> Seit dem Architektur-Umbau ist dieser Skill ein **self-contained SDD+PO-Projekt**.
> Meta lebt hier, nicht mehr zentral in `skill_dev/`. Jakob ist finaler PO.
> (Meta-zirkulär: der PO-Skill managt sich selbst nach seiner eigenen Methodik.)

---

## Vision-Statement

`po-skill` ist der **Product-Owner-Counterpart** zum `agile-sdd-skill`. Er schützt
die Vision als Verfassung, hält den Backlog ehrlich priorisiert und prüft, ob
gelieferte Tickets ihren versprochenen Outcome tatsächlich erreicht haben. Der
Skill verhindert, dass ein hoch-autonomer KI-Agent zwar viel baut, aber am Ziel
vorbei — er ist die Brems- und Fokus-Instanz, nicht der Generator. Ein
1-Personen-Setup bekommt damit die Disziplin eines PO, ohne eine Person dafür zu
binden.

---

## Kern-Prinzipien

1. `vision-ist-verfassung` — `PROJECT_VISION.md` ist append-only und wird
   ausschließlich vom Menschen geschärft. Nie überschreiben, nur ergänzen.
2. `po-generiert-keine-tickets` — Der Skill challenged, priorisiert, verifiziert
   und schlägt Vision-Schärfungen VOR. Er legt keine Tickets an (das ist SDD).
3. `3x-why-gegen-scope-creep` — Jede neue Idee durchläuft eine 3-fache
   Why-Challenge + Vision-Prinzip-Match, bevor sie Ticket werden darf.
4. `48h-cooldown-gegen-hype` — Nicht-akute Ideen ruhen zwei Schlafphasen, damit
   "war-da-eine-Sprachnachricht-Hype" nicht direkt zu Arbeit wird.
5. `outcome-nach-14-tagen-messen` — `done` heißt nicht "wirkt". 14 Tage später
   prüft `/po-verify-outcome`, ob die versprochene Metrik sich bewegt hat.
6. `lessons-aus-live-use-zurueckfuehren` — Erkenntnisse aus realen
   Priorisierungs-/Outcome-Fehlern werden als Regel im Skill verstetigt.

> [!info] Portfolio-Constitution (geerbte Prinzipien)
> Die uebergreifende Skill-Bau-Constitution (multi-projekt-tauglich, dogfood-
> zwingt-qualitaet, keine-skill-fuer-skills-sake u.a.) lebt in
> `skills_sources/SKILLS_VISION.md`. Ticket-`vision_principle:`-Slugs duerfen sowohl
> auf hiesige als auch auf geerbte Portfolio-Prinzipien verweisen.

---

## Outcome-Metriken

- **ideen_im_cooldown_verworfen** — Anteil Ideen, die nach 48h-Cooldown NICHT
  weiterverfolgt wurden. Quelle: `docs/DEFERRED.md`. Ziel: > 0 (der Filter wirkt).
- **done_tickets_mit_outcome_review** — Anteil `done`-Tickets mit
  Outcome-Review >= 14 Tage danach. Quelle: `docs/po-outcomes.md`. Ziel: hoch.
- **tickets_mit_vision_principle** — Anteil Tickets mit gültigem
  `vision_principle:` im Frontmatter. Quelle: Grep. Ziel: 100%.
- **projekte_die_diesen_skill_nutzen** — Projekte mit `## Skill: PO`. Ziel: >= 2.

---

## Was NICHT im Scope ist

- Ticket-Generierung (das macht `agile-sdd-skill`).
- Autonome Vision-Änderung durch die KI (Vision-Hoheit bleibt beim Menschen).
- Multi-Stakeholder-Voting / Community-Input (Jakob ist alleiniger PO).
- Harte Blockade der eigentlichen Arbeit (Vision-Prinzip-Check ist Warning per Default).

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
**Änderung:** Vision erstmals skill-lokal niedergeschrieben. 4 Tickets aus
`skill_dev/docs/tickets/po-skill/` hierher migriert.
