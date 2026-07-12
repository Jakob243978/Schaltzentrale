---
ticket: SKILL-071
status: spec
created: 2026-07-03
moscow: Should
effort: L
surface: backend
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: projekte_mit_generierter_uebersicht_html_im_artifact-design-stil
outcome_review_at: null
ui_verify_urls: []
api_endpoints_extended: n/a
touches_skills: agile-sdd-skill (primaer), po-skill (Vision-/Outcome-Datenquelle, nur lesend)
---

# SKILL-071: SDD/PO generiert + pflegt eine Projekt-`uebersicht.html` im artifact-design-Stil

**Status:** spec
**Erstellt:** 2026-07-03
**MoSCoW:** Should
**Geschaetzter Aufwand:** L (neuer Skill-Template + Command + Datenschema-Konvention +
done-Hook-/Bootstrap-Erweiterung + Design-Token-Spezifikation; Generator-Code bleibt
projekt-lokaler Worker im Lift-and-Shift-Muster)
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`

## Trigger / Quelle

Live-Use-Lesson aus dem Projekt **jakseapartments/automation/nuki-code-verwaltung**:
Jakob hat dort eine **handgebaute** einseitige Projekt-Uebersicht als Referenz-Artefakt
gebaut und will sie als **Standard-Basis je Projekt** — "PO/SDD sollte sowas im aehnlichen
Stil generieren, mit vielleicht noch mehr Kontext."

- **Referenz-Artefakt (Vorbild):**
  `C:\claude_projekte\jakseapartments\automation\nuki-code-verwaltung\docs\uebersicht.html`
- Es speist sich aus `docs/PROJECT_VISION.md` (Vision + Prinzipien + Outcome-Metriken),
  den Tickets (`docs/tickets/`) und den Workflow-Staenden/Status.
- Design folgt dem `artifact-design`-Skill: Palette, **Light/Dark-Tokens** (`:root` +
  `@media (prefers-color-scheme)` + `:root[data-theme=...]`), **Status-Pills**
  (Live/Inaktiv/Build/Spec), **Timeline** (Tagesablauf), **Mail-/Benachrichtigungs-Matrix**,
  Roadmap-Pills, self-contained (kein CDN, kein externes CSS/JS).

## Was soll erreicht werden? (Business-Ziel)

SDD/PO erzeugen und pflegen **standardmaessig** pro Projekt eine einseitige, self-contained
`docs/uebersicht.html` im `artifact-design`-Stil, gespeist aus **Vision + Tickets +
Workflow-/Betriebs-Staenden**. Jakob (und jeder Stakeholder) sieht auf einen Blick "was
laeuft, was wann passiert, was ist offen, wie steht der Outcome" — ohne den Code oder die
Tickets zu lesen und ohne die Seite von Hand zu bauen. Die Seite bleibt **lebend** (analog
Living-Map-Konvention), d.h. sie regeneriert beim done-Hook / Statuswechsel, statt zu
veralten.

## Ausgangslage / Lueckenanalyse (Ist-Zustand 2026-07-03)

Heute wird **teilweise** etwas Uebersicht-artiges erzeugt, aber nicht das Gewuenschte:

1. **`agile-sdd-skill/SKILL.md` Sektion B** referenziert bereits einen done-Hook-Generator
   `python -m workers.project_overview_generator` → `docs/PROJECT_OVERVIEW.html`
   ("Vision + Prinzip-Karten + Feature-Mapping + Live-DB-Stats"). Der Hook ist Opt-in
   (greift nur wenn das Worker-Modul existiert) und wird im Bootstrap-Frische-Check (A.8)
   geprueft.
2. **Aber:** Es gibt **kein Skill-Template**, **keinen Command** und **keine Design-Spec**
   dafuer. Der Generator ist ein **projekt-lokaler** `workers/project_overview_generator.py`,
   den jedes Projekt selbst bauen muss. Real existiert er nur in `Immobewertung/` und
   `KundenAB/BeyerImmo/` — **nicht** im nuki-Projekt (dort ist `uebersicht.html` handgebaut,
   heisst anders und ist an keinen Hook gekoppelt).
3. **Stil-Divergenz:** Die vorhandenen `project_overview_generator.py` nutzen **Tailwind per
   CDN** (externer Script) und einen generischen Indigo/Purple-Gradient — **nicht** die
   `artifact-design`-Tokens (Light/Dark, Status-Pills, Timeline, Mail-Matrix). Sie sind
   **nicht self-contained** und nicht theme-aware.
4. **Content-Modell-Divergenz:** Der vorhandene Generator ist **DB-/CRM-zentriert**
   (Property-Funnel, Live-DB-Stats aus SQLAlchemy) und blendet Ticket-Nummern via
   "banned tokens" bewusst aus. Das Referenz-Artefakt ist dagegen **workflow-/ops-zentriert**
   (Tagesablauf-Timeline, Workflow-Karten mit Status-Pills + n8n-IDs + Versionen,
   Benachrichtigungs-Matrix, Roadmap-Pills). Fuer automation/-Workflow-Projekte (keine
   lokale DB) passt das vorhandene Modell nicht.
5. **Datenschema-Luecke:** Vision-Statement, Prinzipien (`principle_id`), Outcome-Metriken
   und Ticket-Frontmatter (`status/moscow/vision_principle/outcome_metric/effort`) sind
   bereits **maschinenlesbar**. Die **workflow-/betriebsspezifischen** Inhalte des
   Referenz-Artefakts (welcher Workflow, Trigger-Zeiten/Cron, welche Mails/Alerts wann,
   Live/Inaktiv-Status, n8n-ID/Version) stehen heute **nur in Prosa** (CLAUDE.md,
   PROJECT_SPEC.md, Ticket-Body) — es fehlt eine strukturierte Quelle (z.B. ein
   `docs/overview.yaml` / Frontmatter-Konvention), aus der die Timeline + Workflow-Karten +
   Mail-Matrix deterministisch gefuellt werden koennen.

**Fazit Q1:** Es wird heute nur **teilweise** eine Uebersicht generiert (DB-CRM-Variante in
2 Projekten, generischer Tailwind-Stil), **nicht** im artifact-design-Stil und **nicht** als
Skill-Standard. Die begehrte `uebersicht.html`-Form (Ops-Timeline + Workflow-Status +
Mail-Matrix, Light/Dark, self-contained) generiert heute **kein** Skill-Artefakt automatisch.

## Was fehlt (Q2) — die konkreten Luecken

- **L1 — Kein Skill-Template.** Es gibt keine `templates/uebersicht.html` (bzw.
  `templates/PROJECT_OVERVIEW.html`) im `agile-sdd-skill`. Der artifact-design-Stil ist
  nirgends reproduzierbar hinterlegt (Token-Block, Status-Pill-Klassen, Timeline-Grid,
  Mail-Matrix-Table). Damit ist "im aehnlichen Stil" nicht deterministisch erreichbar.
- **L2 — Kein Datenschema fuer Ops-Kontext.** Timeline (Cron/Trigger-Zeiten), Workflow-Karten
  (Name, Instanz, n8n-ID, Version, Status-Pill, "Laeuft/Macht/Mails"), Benachrichtigungs-Matrix
  sind nicht maschinenlesbar erfasst. Es braucht eine leichte Konvention (z.B.
  `docs/overview.yaml` **oder** ein `workflows:`-Block, aus dem Generator/Agent die Karten +
  Timeline + Mail-Matrix zieht). Vision/Prinzipien/Tickets sind bereits da und werden nur
  aggregiert.
- **L3 — Kein Command / Trigger-Klarheit.** Es fehlt ein expliziter `/sdd-overview`-Command
  zum manuellen (Re)Generieren, und die Regenerierungs-Trigger sind unscharf: der done-Hook
  existiert nur in Prosa, ein Statuswechsel `spec→in_progress→review` aktualisiert die
  Uebersicht heute nicht.
- **L4 — "mehr Kontext als jetzt".** Das Referenz-Artefakt zeigt Vision/Prinzipien/Timeline/
  Workflows/Mails/Roadmap. Wertvoller wuerde es durch: **Outcome-Metrik-Ist-Werte** (aus
  `po-outcomes.md`), **offene Tickets nach MoSCoW** (aus Ticket-Frontmatter), **Governance-
  Highlights** (letzte autonome Entscheidungen aus `governance_log.md`), **Abhaengigkeiten/
  Risiken** (aus `depends_on` + Ticket-Risiko-Hinweisen), sowie ein **Verify-/Traceability-
  Ampel** (aus den Verify-Reports / TRACEABILITY.md).
- **L5 — Living-Aspekt nicht verankert.** Analog Living-Map-Konvention muss die Uebersicht
  im **selben Pass** wie der Ticket-/Workflow-Patch aktualisiert werden (done-Hook +
  Bootstrap-Frische-Check + optional Statuswechsel), sonst driftet sie.

## Akzeptanzkriterien (EARS-Format)

- [ ] **EARS-1 (Skill-Template im artifact-design-Stil):** When ein Projekt eine
  Projekt-Uebersicht generiert, the system shall dies aus einem **skill-bereitgestellten**
  Template `templates/uebersicht.html` tun, das **self-contained** ist (kein externes
  CSS/JS/CDN), **Light/Dark-Tokens** (`:root` + `@media (prefers-color-scheme:dark)` +
  `:root[data-theme="dark"|"light"]`), **Status-Pills**, eine **Timeline** und eine
  **Benachrichtigungs-/Mail-Matrix** enthaelt (Stil-Vorbild: das Referenz-Artefakt).
- [ ] **EARS-2 (Datenquellen aggregiert):** When die Uebersicht generiert wird, the system
  shall Vision-Statement + Kern-Prinzipien + Outcome-Metriken aus `docs/PROJECT_VISION.md`,
  die Tickets (Status/MoSCoW/`vision_principle`/`outcome_metric` aus Frontmatter) und die
  Workflow-/Betriebs-Staende in **eine** Seite zusammenfuehren — reine Aggregation
  vorhandener Artefakte plus der Ops-Datenquelle aus EARS-3.
- [ ] **EARS-3 (Ops-Datenschema fuer Timeline/Workflows/Mails):** When ein Projekt
  Workflow-/Ops-Inhalte (Trigger-Zeiten, Workflow-Karten mit Status, Alerts/Mails) in der
  Uebersicht zeigen will, the system shall diese aus einer **maschinenlesbaren** Quelle
  (Konvention: `docs/overview.yaml` oder aequivalenter Frontmatter-Block) ziehen — nicht aus
  Prosa raten. Fehlt die Quelle, shall der entsprechende Abschnitt still weggelassen werden
  (kein Fehler, kein Halluzinieren).
- [ ] **EARS-4 (mehr Kontext):** When die Uebersicht generiert wird UND die jeweiligen
  Quellen vorhanden sind, the system shall zusaetzlich anzeigen: **offene Tickets nach
  MoSCoW**, **Outcome-Metrik-Ist-Werte** (aus `docs/po-outcomes.md`), **Governance-Highlights**
  (letzte Eintraege aus `docs/governance_log.md`) und **Abhaengigkeiten/Risiken** (aus
  `depends_on` + Risiko-Hinweisen der Tickets). Jede Sektion ist Opt-in: fehlt die Quelle,
  entfaellt die Sektion.
- [ ] **EARS-5 (Command):** When der User `/sdd-overview` aufruft, the system shall
  `docs/uebersicht.html` (re)generieren und den Ausgabepfad + eine Kurz-Statistik
  (Workflows, offene Tickets, Warnungen) berichten.
- [ ] **EARS-6 (Living / done-Hook):** When ein Ticket auf `done` gesetzt wird, the system
  shall — analog FEATURE_MAP/TRACEABILITY, best-effort, Opt-in — `docs/uebersicht.html`
  regenerieren, sofern das Projekt den Generator/Command hat, und das `done` **niemals**
  blocken (Fehler nur als WARN im Implementer-Bericht).
- [ ] **EARS-7 (Bootstrap-Frische-Check):** When beim Bootstrap done-Tickets existieren,
  aber `docs/uebersicht.html` fehlt oder aelter als das juengste done-Ticket / der letzte
  Workflow-Patch ist, the system shall dem User **passiv** vorschlagen, `/sdd-overview` zu
  laufen (kein Hard-Block, analog A.8 FEATURE_MAP/TRACEABILITY-Frischecheck).
- [ ] **EARS-8 (multi-projekt-tauglich):** While der Skill kein projekt-spezifisches
  Wissen hartkodiert (kein "nuki"/"Immobewertung"-Pfad, keine feste Workflow-Liste), the
  system shall Projekt-Inhalte ausschliesslich aus Projekt-Dateien (Vision/Tickets/
  `overview.yaml`/Config) beziehen — Vision-Prinzip `skill-muss-multi-projekt-tauglich-sein`.

## Loesungs-Skizze (Approach)

- **Gewaehlter Ansatz:** (a) **Skill-Template** `templates/uebersicht.html` mit dem
  artifact-design-Token-Block + Bausteinen (Vision-Card, Timeline-Grid, Workflow-Karten,
  Mail-Matrix-Table, Roadmap-Pills, Governance-/Outcome-Sektionen) als **Referenz-Struktur**.
  (b) **Ops-Datenschema** `docs/overview.yaml` (Konvention + Beispiel im Skill), das Timeline,
  Workflow-Karten und Mail-Matrix maschinenlesbar macht. (c) **Command** `commands/sdd-overview.md`
  (Agenten-getrieben: liest Vision/Tickets/overview.yaml/governance/outcomes, fuellt das
  Template). (d) **SKILL.md-Aenderungen:** done-Hook (Sektion B) + Bootstrap-Frische-Check
  (Sektion A.8) + neue Sektion "E) Living Documentation → Projekt-Uebersicht" + Templates-
  Referenz + Versions-Header-Bump. (e) Generator-Code bleibt **projekt-lokaler Worker**
  (Lift-and-Shift-Muster wie feature_map/traceability) — der Skill liefert Template + Command +
  Format + Regeln, erzwingt aber keinen deterministischen Python-Generator.
- **Verworfene Alternative(n):** (1) Den bestehenden `project_overview_generator.py`
  (Tailwind-CDN, DB-Funnel) einfach zum Skill-Standard erklaeren — verworfen: nicht
  self-contained, nicht theme-aware, DB-zentriertes Content-Modell passt nicht auf
  automation/-Workflow-Projekte ohne lokale DB, widerspricht dem Referenz-Artefakt.
  (2) Uebersicht rein aus Prosa (CLAUDE.md/SPEC) generieren lassen — verworfen: nicht
  deterministisch, Timeline/Cron/Mail-Matrix wuerden halluziniert (verletzt "keine stillen
  Fakes"). (3) Deterministischen Generator als Skill-Kern erzwingen — verworfen: widerspricht
  dem etablierten Lift-and-Shift-Muster (SKILL-002/017) und der Multi-Projekt-Tauglichkeit.
- **Betroffene Module:** `skills_sources/agile-sdd-skill/SKILL.md`,
  `skills_sources/agile-sdd-skill/templates/uebersicht.html` (NEU),
  `skills_sources/agile-sdd-skill/templates/overview.yaml.example` (NEU),
  `skills_sources/agile-sdd-skill/commands/sdd-overview.md` (NEU).

## Umsetzungsschritte (konkrete Skill-Aenderungen)

> [!important] NICHT blind applien — Source-of-Truth = `skills_sources/agile-sdd-skill/`
> Deploy NUR via `Schaltzentrale/setup.ps1`. Aenderungen additiv, nichts Bestehendes loeschen.
> Bestehenden `PROJECT_OVERVIEW.html`-Hook nicht brechen — SKILL-071 fuehrt die
> artifact-design-`uebersicht.html` als **empfohlenen Standard** ein und markiert die
> DB-CRM-Variante als Sonderfall/Legacy bzw. als "Content-Profil B".

1. **NEU `templates/uebersicht.html`** — artifact-design-Token-Block (Light/Dark),
   Bausteine: Vision-Card + Prinzipien-Grid, Timeline-Grid (Tagesablauf/Trigger),
   Workflow-Karten mit Status-Pills (`p-live/p-idle/p-build/p-spec`), Mail-/Benachrichtigungs-
   Matrix (Table, `overflow-x:auto`), Roadmap-Pills, Governance-/Outcome-/Risiko-Sektionen.
   Platzhalter-Kommentare markieren die Fuell-Stellen. (Vorbild: nuki `docs/uebersicht.html`.)
2. **NEU `templates/overview.yaml.example`** — Ops-Datenschema: `stand`, `meta` (Instanz,
   Anzahl, Alert-Empfaenger), `timeline[]` (zeit, titel, text, kind: normal|deadline|extern),
   `recurring[]` (intervall, text), `workflows[]` (name, id, instanz, version, status,
   laeuft, macht, mails[]), `notifications[]` (name, workflow, wann), `roadmap[]`
   (ticket, text, status). Alles Opt-in.
3. **NEU `commands/sdd-overview.md`** — Agenten-Command: liest Vision + Tickets +
   `overview.yaml` + `po-outcomes.md` + `governance_log.md`, fuellt `templates/uebersicht.html`
   → `docs/uebersicht.html`, berichtet Pfad + Kurz-Statistik. Explizit: fehlt eine Quelle →
   Sektion weglassen, nicht raten.
4. **`SKILL.md` B) Auto-Doku-Hook:** den Generator-Block um die Uebersicht ergaenzen
   (best-effort, Opt-in, WARN statt Block) und die Beziehung zum bestehenden
   `PROJECT_OVERVIEW.html`-Hook klarstellen (zwei Content-Profile: A=Ops/artifact-design
   `uebersicht.html`, B=DB-CRM `PROJECT_OVERVIEW.html`; Projekt waehlt via Config).
5. **`SKILL.md` A.8) Bootstrap-Frische-Check:** `docs/uebersicht.html` in den Frische-Check
   aufnehmen (fehlt/veraltet → passiver `/sdd-overview`-Vorschlag).
6. **`SKILL.md` E) Living Documentation:** neue Unter-Sektion "Projekt-Uebersicht
   (`docs/uebersicht.html`)" + Templates-Referenz-Zeile; `artifact-design`-Skill als
   Stil-Autoritaet referenzieren.
7. **`sdd-config.yaml.example`:** optionale Keys `overview_enabled`, `overview_profile:
   ops|crm`, `overview_path: docs/uebersicht.html`.
8. **Versions-Header `SKILL.md`** bumpen (v0.6 → v0.7).

## Datenquellen-Matrix (was ist schon da vs. neu)

| Sektion der Uebersicht | Quelle heute | Status |
|---|---|---|
| Vision + Prinzipien | `docs/PROJECT_VISION.md` | vorhanden (maschinenlesbar) |
| Outcome-Metriken (Ziel) | `PROJECT_VISION.md` | vorhanden |
| Outcome-Ist-Werte | `docs/po-outcomes.md` | vorhanden, heute ungenutzt |
| Offene Tickets nach MoSCoW | Ticket-Frontmatter (`status`,`moscow`) | vorhanden |
| Roadmap-Pills | Tickets + `ROADMAP.md` | vorhanden |
| Governance-Highlights | `docs/governance_log.md` | vorhanden, heute ungenutzt |
| Abhaengigkeiten/Risiken | Ticket `depends_on` + Body | teilweise (uneinheitlich) |
| Verify-/Traceability-Ampel | Verify-Reports / `TRACEABILITY.md` | vorhanden, heute ungenutzt |
| **Timeline (Cron/Trigger-Zeiten)** | nur Prosa (CLAUDE.md/SPEC) | **NEU: `overview.yaml`** |
| **Workflow-Karten (id/version/status)** | nur Prosa | **NEU: `overview.yaml`** |
| **Mail-/Benachrichtigungs-Matrix** | nur Prosa | **NEU: `overview.yaml`** |

## Abgrenzung / Out of Scope

- **Kein deterministischer Python-Generator als Pflicht** — projekt-lokaler Worker
  (Lift-and-Shift), Skill liefert Template + Command + Format + Regeln.
- **Kein Bruch des bestehenden `PROJECT_OVERVIEW.html`-Hooks** (Immobewertung/BeyerImmo) —
  additive Koexistenz als Profil B.
- **Kein Auto-Deploy/Hosting** der HTML (bleibt lokale `file://`-Datei; Jakob nutzt keine
  Online-Artifacts).

## Verhaeltnis zu bestehenden Tickets

- **SKILL-002** (Vision↔Features-Bridge, `feature_map_generator`) und **TICKET-078**
  (Immobewertung `project_overview_generator.py`) sind die Vorlaeufer/Content-Profil B.
  SKILL-071 hebt den Uebersicht-Gedanken auf einen **skill-bereitgestellten, artifact-design-
  konformen, ops-tauglichen** Standard (Profil A) und schliesst die Stil-/Content-/Trigger-Luecke.
- **SKILL-017** (TRACEABILITY) + **FEATURE_MAP** liefern Ampel-/Abdeckungs-Daten, die die
  Uebersicht als Kontext-Sektion einbinden kann.

## Referenz-Artefakt (Vorbild, Pflicht-Read bei Umsetzung)

`C:\claude_projekte\jakseapartments\automation\nuki-code-verwaltung\docs\uebersicht.html`
— Token-Block (Zeilen ~8-40), Timeline (`.tl`), Workflow-Karten (`.card` + `.pill`),
Mail-Matrix (`<table>`), Roadmap-Pills (`.road`). Genau diese Struktur ist der Ziel-Stil.

## Code-Referenzen (skills_sources/agile-sdd-skill/)

- `SKILL.md` (A.8 Bootstrap-Frische-Check, B Auto-Doku-Hook, E Living Documentation,
  Templates-Referenz, Versions-Header)
- `templates/uebersicht.html` (NEU)
- `templates/overview.yaml.example` (NEU)
- `commands/sdd-overview.md` (NEU)
- `templates/sdd-config.yaml.example` (optionale overview_*-Keys)

## [J] — was Jakob noch tun muss

1. SKILL-071 reviewen (`/po-challenge` optional — Vision-Prinzip-Match
   `lessons-aus-live-use-zurueckfuehren` ist gesetzt).
2. Entscheiden: soll `uebersicht.html` **Default-an** je Projekt sein oder Opt-in via
   `sdd-config.yaml: overview_enabled: true`?
3. Nach Umsetzung `Schaltzentrale/setup.ps1` ausfuehren (Deploy nach `~/.claude/skills/`).
4. Referenz-Content-Profil festlegen: A (Ops, wie nuki) als Default, B (DB-CRM) fuer
   App-Projekte wie Immobewertung.
