---
name: po-skill
version: 0.2
description: Product-Owner-Skill als Counterpart zum agile-sdd-skill. Aktivieren wenn ein Agent Vision-Hygiene, Backlog-Priorisierung oder Outcome-Verifikation fuer ein Projekt uebernehmen soll — Vision-Constitution, 3x-Why-Challenge, 48h-Cooldown, RICE-Priorisierung, 14-Tage-Outcome-Check. Verwende diesen Skill wenn der User Ideen challengen will (`/po-challenge`), Backlog priorisieren will (`/po-prioritize`), Outcomes von done-Tickets pruefen will (`/po-verify-outcome`) oder das Projekt initial mit Vision aufsetzen will (`/po-init`).
---

# Product-Owner-Skill

Gegenstueck zum `agile-sdd-skill`. Waehrend SDD die **Wie**-Frage stellt
(Spec, Tests, Verifier, ADRs), stellt dieser Skill die **Warum**-Frage:
- Warum bauen wir dieses Feature ueberhaupt?
- Passt es zur Vision?
- Haelt der erwartete Outcome 14 Tage spaeter Stand?

**Anti-Pattern bewusst vermieden:**
- Der PO-Skill **generiert keine Tickets selbst**. Er challenged, priorisiert
  und verifiziert. Sonst halluziniert er Features (BMad-Erfahrung 2026).
- `/po-reconcile` schlaegt Vision-Schaerfungen nur **VOR** (Vorschlags-Doc) und
  **pflegt abgeleitete Living-Docs** — es schreibt nie in `PROJECT_VISION.md`
  und legt keine Tickets an. Living-Docs sind abgeleitet, NIE die Quelle der Vision.
- Kein PR-Gatekeeper-Workflow — Jakob ist 1-Personen-Setup, kein
  Multi-Stakeholder-Approval.
- Kein Crowd-Sourcing / Constitutional-Voting — alleiniger Stakeholder
  (Jakob) entscheidet, der Skill macht die Disziplin sichtbar.

---

## A) Wann den Skill aktivieren

| Trigger | Aktion |
|---|---|
| User sagt "lass uns Feature X bauen" / "Ticket fuer X" | `/po-challenge` BEVOR der SDD-Skill `idea`→`spec` ausfuehrt |
| User fragt "was ist als naechstes dran?" | `/po-prioritize` ueber die `idea`-Tickets |
| Ein `done`-Ticket ist >= 14 Tage alt | `/po-verify-outcome TICKET-NNN` |
| Neues Projekt-Setup ohne `docs/PROJECT_VISION.md` | `/po-init` (einmalig pro Projekt) |
| User redet ueber Scope / Strategie / "lohnt sich das?" | Vision-Datei oeffnen + relevante Prinzipien zitieren |
| Letzte Vision-Schaerfung > N Tage / neue ADR seit Schaerfung | `/po-reconcile` (Drift-Vorschlag + Living-Docs synchron) |

---

## B) Vision-Constitution (`docs/PROJECT_VISION.md`)

Pflicht-Datei pro Projekt mit folgenden Sektionen (Template: `templates/vision.md`):

1. **Vision-Statement** — 1 Absatz, was-fuer-wen-warum, ohne Tech-Begriffe
2. **Kern-Prinzipien** — 5-10 Bullets, jeder mit `principle_id` (Kebab-Slug),
   Kurzbegruendung. **Tickets referenzieren mind. 1 `principle_id`.**
3. **Outcome-Metriken** — messbare Groessen (z.B. "Banking-Match-Properties/
   Monat"), nicht "mehr Effizienz". Tickets duerfen `outcome_metric:`-Feld setzen.
4. **Was NICHT im Scope ist** — explizite Negationen. Schuetzt vor
   Scope-Creep.
5. **Aktualisiert** — Append-only Log mit Datum + Grund. Vision wird
   geschaerft, nicht ueberschrieben.

Vision wird in Implementer-Sessions als **Pflicht-Lese-Datei** mit-geladen
(Bootstrap-Sequenz im SDD-Skill bekommt einen Hook — siehe Sektion F).

---

## C) Challenge-Workflow (`/po-challenge`)

Aufruf: `/po-challenge "<Kurzbeschreibung der Idee>"` ODER auf bestehender
`idea`-Ticket-Datei.

Algorithmus:

1. **Vision-Prinzip-Match.** Welche `principle_id` aus `PROJECT_VISION.md`
   wird adressiert? Wenn keines passt: STOP — Frage an User:
   *"Diese Idee passt zu keinem aktuellen Prinzip. Soll die Vision erweitert
   werden oder ist die Idee out-of-scope?"*
2. **3x Why.**
   - *Warum wirklich?* — was passiert wenn wir das NICHT bauen?
   - *Warum jetzt?* — welche Realitaet macht das jetzt akut (nicht in 2 Monaten)?
   - *Warum so?* — was waere die billigste Variante mit 80% Wert?
3. **48h-Cooldown-Empfehlung.** Wenn die Idee nicht akut ist (kein Bug,
   kein Live-Blocker, kein Audit-Termin):
   - In `docs/DEFERRED.md` mit `created: YYYY-MM-DD HH:MM` + `release_at:
     YYYY-MM-DD HH:MM (= +48h)` eintragen.
   - User-Antwort: *"Idee geparkt bis YYYY-MM-DD HH:MM. Wenn du sie dann
     immer noch wichtig findest: `/po-challenge --release ID` und wir gehen
     in den SDD-Flow."*
   - Cooldown wird per `--force` ueberschrieben — die Vision-Prinzip-Frage
     bleibt aber Pflicht.
4. **Uebergabe an SDD.** Erst wenn Cooldown abgelaufen UND Prinzip
   referenziert: der Skill empfiehlt dem User
   `/sdd-init TICKET-NNN` (bzw. Ticket aus `idea` → `spec` zu setzen).
   Das Ticket-Frontmatter MUSS dabei `vision_principle: <principle_id>`
   enthalten.

> [!warning] Akut-Liste (kein Cooldown)
> - Bug-Fix der Production-Daten betrifft
> - Verifikations-Fehler eines aktiven Tickets
> - Audit/Compliance-Termin in < 7 Tagen
> - Vom User explizit als "akut" markiert

### C.5 Empfehlungs-First in `/po-challenge` (Schaerfung 2026-06-18)

> [!important] `/po-challenge` empfiehlt — der User entscheidet
>
> Heute endet `/po-challenge` haeufig in 3x-Why-Antworten plus offener
> Frage ("Was meinst du?"). Das verstaerkt genau das Rueckfrage-Pattern,
> das `feedback_einfach_abarbeiten` und `feedback_style` vermeiden wollen.
> Ab sofort liefert jeder Challenge-Durchlauf eine **klare Empfehlung**.

#### C.5.1 Pflicht-Format am Ende eines Challenge-Durchlaufs

Nach 3x-Why + Vision-Prinzip-Match + Akut-/Cooldown-Pruefung gibt
`/po-challenge` IMMER aus:

```
Empfehlung: <annehmen | parken bis YYYY-MM-DD HH:MM | ablehnen | Vision schaerfen>
Warum: <2-3 Saetze, expliziter Bezug zum Vision-Prinzip / Memory / Live-Beleg>
Trade-off: <1 Satz: was die Empfehlung kostet>
```

Die vier zulaessigen Empfehlungen:

- **annehmen** — Idee passt zur Vision, ist akut (Akut-Liste greift) oder
  Cooldown bereits geleistet → Uebergabe an SDD (`idea` → `spec`).
- **parken bis YYYY-MM-DD HH:MM** — Default bei nicht-akuten Ideen.
  Eintrag in `docs/DEFERRED.md`, 48h-Cooldown.
- **ablehnen** — Idee laeuft Vision aktiv zuwider oder ist
  out-of-scope laut "Was NICHT im Scope ist" der Vision.
- **Vision schaerfen** — kein Prinzip passt, aber die Idee wirkt
  strategisch relevant → Empfehlung an User, die Vision append-only zu
  erweitern, bevor das Ticket entsteht.

#### C.5.2 Anti-Pattern (verboten als Default-Output)

- **3x-Why-Antworten ohne abschliessende Empfehlung** — der Challenge ist
  ein Werkzeug zum Empfehlen, kein Frage-Werkzeug.
- **"Soll ich das Ticket auf spec setzen?"** — die Empfehlung MUSS kommen;
  der User entscheidet danach mit Ja/Nein, nicht aus einer offenen Liste.
- **Neutrale Aufzaehlung von Vor- und Nachteilen** ohne Wertung.

#### C.5.3 Beziehung zu `agile-sdd-skill` Sektion M

Dieses Pattern spiegelt **agile-sdd-skill Sektion M
("Antwort-Pattern Empfehlungs-First")** direkt fuer den
Challenge-Workflow. Konsistenz ist Pflicht — wenn der Implementer-Agent
Empfehlungs-First sprechen muss, darf der PO-Skill nicht der einzige Ort
sein, der wieder offen fragt.

#### C.5.4 STOPP-Faelle aus `agile-sdd-skill` Sektion L

Wenn die Idee einen Fall aus `agile-sdd-skill` Sektion L.2 (STOPP-Liste)
beruehrt — destruktive Op, Outbound-Kommunikation, neue bezahlte
Dependency, vision-relevante Architektur, Verifikations-Fehler,
DB-Mutation ohne Skript — dann gilt: `/po-challenge` darf die Empfehlung
aussprechen ("annehmen, weil…"), aber **setzt sie nicht autonom um**.
Jakob entscheidet. Die STOPP-Liste ueberstimmt jede autonome Setzung,
**nicht** die Empfehlung selbst.

#### C.5.5 Verhaeltnis zur Akut-Liste (Sektion C, Schritt 3)

Die Akut-Liste (Bug-Fix Production-Daten, Verifikations-Fehler, Audit/
Compliance-Termin < 7 Tagen, explizit "akut") verschiebt die
Default-Empfehlung von **"parken bis +48h"** auf **"annehmen sofort"** —
sie **ueberspringt den Cooldown-Schritt nicht** (der Eintrag in
`DEFERRED.md` entfaellt nur dann, wenn die Akut-Liste greift). Die
Empfehlung sagt das explizit, z.B.:

```
Empfehlung: annehmen sofort (Akut-Liste: Verifikations-Fehler aktives Ticket)
Warum: TICKET-NNN haengt; Cooldown wuerde Live-Workflow blockieren.
Trade-off: Kein 48h-Reifezeit-Puffer fuer alternative Loesungs-Ideen.
```

#### C.5.6 Verweis auf 2-Wochen-Plan (Vision-Drift-Counter)

Der **Vision-Drift-Counter** (Bestaetigungsfragen pro Session zaehlen,
nach der 3. automatisch `/po-reconcile` empfehlen, ggf.
`docs/sdd-session-meta.json`) ist Vorschlag 4 der Sourcedoku und
aktuell **OUT-OF-SCOPE**. Wird in ca. 2 Wochen separat als SKILL-Ticket
evaluiert. Sourcedoku:
`skill_dev/proposals/2026-06-18_sdd_default_decision_plus_voice_mode.md`.

---

## D) Priorisierung (`/po-prioritize`)

Aufruf: `/po-prioritize` (oder mit `--top N` fuer Kurzliste).

Algorithmus:

1. Alle Ticket-Files mit `Status: idea` aus `docs/tickets/` lesen.
2. Pro Ticket aus Frontmatter / Body extrahieren:
   - `Reach` (1-10) — wie viele Nutzer/Events betroffen
   - `Impact` (1-10) — wie stark die Wirkung pro Nutzer
   - `Confidence` (0.0-1.0) — wie sicher die Schaetzung
   - `Effort` — aus `Geschaetzter Aufwand: XS|S|M|L|XL` mapped auf
     `1|2|3|5|8`
3. **RICE-Score** = `(Reach * Impact * Confidence) / Effort`. Ranking absteigend.
4. Output: Markdown-Tabelle + 1-Satz-Begruendung pro Position
   (welches Vision-Prinzip, was haebt Score).
5. Fehlen Felder (Reach/Impact/Confidence)? → in Output mit `?` markieren
   und User fragen ob er ergaenzen will. **Niemals raten.**

Default-Mapping fuer MoSCoW falls Felder fehlen (Fallback, nicht Pflicht):
- `Must` → Reach=8, Impact=8, Confidence=0.7
- `Should` → Reach=5, Impact=6, Confidence=0.6
- `Could` → Reach=3, Impact=4, Confidence=0.5
- `Wont` → wird nicht priorisiert

---

## E) Outcome-Verifikation (`/po-verify-outcome TICKET-NNN`)

Aufruf nach >= 14 Tagen seit `done`, oder via Cron.

Algorithmus:

1. Ticket lesen — `outcome_metric:` aus Frontmatter holen.
2. Metrik gegen Quelle pruefen (SQL-Query, Log-Auswertung, manuelle Frage).
   - Wenn Metrik unmessbar (z.B. "User-Zufriedenheit"): User direkt fragen.
3. Eintrag in `docs/po-outcomes.md` anhaengen:
   ```
   ## TICKET-NNN — verify YYYY-MM-DD
   Metrik: <id>
   Wert davor: <baseline>
   Wert jetzt: <actual>
   Beurteilung: erreicht | nicht erreicht | nicht messbar
   Hypothese-Status: bestaetigt | widerlegt | offen
   ```
4. **Eskalation:** Wenn ein Ticket mit `MoSCoW: Must` 90 Tage nach `done`
   keine Outcome-Bewegung zeigt → User-Hinweis:
   *"TICKET-NNN war Must-Have, Outcome stagniert. In naechster Retro flaggen?"*

---

## F) SDD-Integration

Der `agile-sdd-skill` hat einen Hook auf den Status-Uebergang `idea` →
`spec`. Konkret (in `agile-sdd-skill/SKILL.md` Sektion B nach diesem Skill
eingefuegt):

> Bevor ein Ticket auf Status `spec` gesetzt wird, pruefe:
> - Existiert `docs/PROJECT_VISION.md`?
> - Enthaelt das Ticket-Frontmatter `vision_principle: <principle_id>`,
>   die in der Vision tatsaechlich existiert?
> - **Default (Warning):** Wenn nein → User-Hinweis: *"Kein
>   `vision_principle` referenziert — `/po-challenge` empfohlen, bevor
>   Implementierung startet."* Status-Uebergang trotzdem moeglich.
> - **Strict-Mode (ENV `PO_SKILL_STRICT=1`):** Hard-Block. Status-Uebergang
>   verweigern bis Prinzip referenziert ist.

Zusaetzlich: Beim Status-Uebergang `in_progress` → `done` wird im
Ticket-Frontmatter automatisch gesetzt:

```yaml
outcome_review_at: <heute + outcome_review_days aus docs/po-config.yaml>
```

(Default `outcome_review_days: 14`.)

---

## G) Ticket-Frontmatter-Erweiterung

Tickets, die nach PO-Skill-Aktivierung im Projekt entstehen, bekommen drei
optionale Felder (Pflicht erst nach `po-init`):

```yaml
vision_principle: mensch-entscheidet-ki-bereitet-vor   # Pflicht nach po-init
outcome_metric: time_to_decision_median                # optional
outcome_review_at: null                                # wird beim done-Set gesetzt
```

Das Template `templates/TICKET.md` im `agile-sdd-skill` bleibt unveraendert
— der PO-Skill ergaenzt diese Felder additiv in projekt-eigenen Templates,
falls noetig.

---

## H) Init-Workflow (`/po-init`)

Einmalig pro Projekt aufrufen. Schritte:

1. Pruefen ob `docs/PROJECT_VISION.md` existiert. Wenn ja: STOP mit
   Hinweis *"Bereits initialisiert — nutze `/po-challenge` fuer neue Ideen."*
2. `docs/PROJECT_VISION.md` aus `~/.claude/skills/po-skill/templates/vision.md`
   ableiten. Mit projekt-spezifischem Material befuellen (entweder vom
   User abfragen, oder — wenn im Briefing schon mitgegeben — direkt
   einsetzen).
3. `docs/DEFERRED.md` leer anlegen aus Template.
4. `docs/po-config.yaml` aus Template ableiten (siehe Defaults unten).
5. `CLAUDE.md` um einen `## Skill: PO`-Block ergaenzen, der die Datei
   `docs/PROJECT_VISION.md` referenziert + die Slash-Commands listet.
6. Hinweis ausgeben: *"Vision-Initial-Befuellung erfolgte aus Briefing-
   Material. Bitte review die Datei und schaerf sie wo noetig — du bist
   der finale PO. Aenderungen ins Aktualisiert-Log eintragen."*

**Default `po-config.yaml`:**

```yaml
outcome_review_days: 14
cooldown_default_hours: 48
strict_vision_principle: false   # set true → ENV PO_SKILL_STRICT=1
rice_effort_mapping:
  XS: 1
  S: 2
  M: 3
  L: 5
  XL: 8
```

---

## I) Verifier-Subagent (`po-verifier/`)

Analog zum `agile-sdd-skill`-Verifier, aber **vor** der Implementierung
(nicht nach). Aufruf: `/po-challenge` triggert den Subagent in einer
frischen Session, um Bias-Vermeidung sicherzustellen.

**Was er prueft (siehe `po-verifier/PO_VERIFIER.md`):**
1. Vision-Prinzip-Match (Pflicht).
2. 3x-Why-Antworten plausibel oder zirkulaer?
3. Cooldown-Empfehlung sinnvoll? (Akut-Liste anwenden.)
4. Gibt es bereits aehnliche Ideen in `DEFERRED.md` oder offene Tickets?

**Was er NICHT tut:**
- Tickets selbst anlegen (Anti-Pattern).
- Code lesen oder modifizieren.
- Vision-Datei aendern (nur User darf Vision schaerfen).

---

## J) Lebende Outputs

| Datei | Wer schreibt | Wer liest |
|---|---|---|
| `docs/PROJECT_VISION.md` | User (po-init befuellt initial) | Alle Implementer + Verifier |
| `docs/DEFERRED.md` | `/po-challenge` (Append) | `/po-prioritize`, User |
| `docs/po-config.yaml` | `/po-init` (User editiert) | Alle PO-Commands |
| `docs/po-outcomes.md` | `/po-verify-outcome` (Append) | User, Retros |

---

## K) Vision-Reconciliation (`/po-reconcile`)

Periodischer **Rueckblick**, der die gelebte Weiterentwicklung gegen die
Vision-Verfassung abgleicht und Jakob einen **Schaerfungs-VORSCHLAG** liefert —
nie eine autonome Vision-Aenderung (SKILL-015). `/po-challenge` und
`/po-verify-outcome` sind ticket-lokal + vorwaerts; `/po-reconcile` schliesst die
Luecke „Ist die Verfassung angesichts der seither gebauten ADRs/done-Tickets/
Meetings noch aktuell?".

### Input-Quellen (aus `po-config.yaml: reconcile_trigger.sources`)

Gescannt wird alles seit dem juengsten Datum im „Aktualisiert"-Log von
`PROJECT_VISION.md` (Anker): `adr` (`docs/adr/ADR-*.md`), `tickets_done`
(Status `done`, v.a. `Must`), `meetings` (`meetings/**`, `docs/meetings/**`),
`governance` (`docs/governance_log.md`), optional `changelog`.

### Heuristik — vision-relevant vs. reine Implementierung

Vision-relevant, wenn mind. eines zutrifft: (1) Scope-Verschiebung, (2) Prinzip
ohne Heimat, (3) Realitaets-Widerspruch, (4) Architektur-Entscheidung, (5)
Outcome-Metrik veraltet. Bugfix/Refactor/Test/Doku-Tippfehler ist KEIN Signal —
nur zaehlen, nicht vorschlagen.

### Output — `docs/po-reconcile-YYYY-MM-DD.md` (Vorschlags-Doc, KEIN Vision-Write)

Pro Verschiebung: Beleg-Datei, Drift, Schaerfungs-VORSCHLAG (nicht angewendet),
`[J]`-Frage. Reine Implementierung nur als Zaehlung. Schaerfung erfolgt
ausschliesslich durch Jakob ins „Aktualisiert"-Log.

### Living-Doc-Pflege (SKILL-067)

Zusaetzlich zum Vorschlags-Doc haelt `/po-reconcile` die in `po-config.yaml`
gelisteten **abgeleiteten Living-Docs** synchron — generierte/gepflegte
Praesentationen der Vision/Roadmap/KPIs/ADRs (z.B. ein Projekt-Cockpit-HTML, eine
Customer-Journey-SSOT). So kann „veraltete Praesentation neben aktueller Vision"
strukturell nicht mehr entstehen.

```yaml
po_skill:
  reconcile:
    # Abgeleitete Docs, die /po-reconcile synchron haelt (NIE die Vision selbst).
    # Fehlt der Block / leer -> Living-Doc-Pflege ist No-Op (abwaertskompatibel).
    living_docs:
      - docs/projekt-cockpit.html
      - docs/customer-journey.html
```

**Ablauf (nach „Vorschlags-Doc schreiben"):** Fuer jeden Pfad in
`reconcile.living_docs` das Doc gegen die erkannten vision-relevanten
Verschiebungen + den aktuellen Stand (Roadmap, ADR-Liste mit Titel+Status,
Outcome-KPI-Live-Werte aus DB/Quellen, Reconcile-Datum/Drift) aktualisieren.
NUR abgeleitete Inhalte; die Vision bleibt unberuehrt. Pfad fehlt / Liste leer ->
ueberspringen (No-Op). Brand-Tokens der Surface respektieren (tokens.css /
`--brand-*`, kein hartkodierter Hex). Konsistenz zur SSOT-Konvention des Docs
wahren (z.B. Journey-SSOT: keine Dopplungen, Status ✅/🟡/❌).

> [!warning] Abgrenzung (strikt)
> **Vision = append-only-Hoheit Jakob** (nur er schaerft, ins „Aktualisiert"-Log).
> **Living-Docs = generiert/gepflegt**, abgeleitet — sie tragen einen sichtbaren
> Header-Hinweis „Lebendes Doc — von `/po-reconcile` gepflegt; Vision-Hoheit bleibt
> PROJECT_VISION.md" und sind NIE die Quelle der Vision. `/po-reconcile` schreibt
> weder die Vision noch legt es Tickets an.

### Trigger

1. **Manuell:** `/po-reconcile` (oder `--since YYYY-MM-DD`).
2. **Bootstrap-Hinweis (passiv, nie blockierend):** Beim Lesen von
   `PROJECT_VISION.md` die `reconcile_trigger`-Bedingung aus `po-config.yaml`
   pruefen (`max_days_since_sharpen`, `max_done_tickets_since_sharpen`,
   `new_adr_triggers`) und bei Faelligkeit EINEN Hinweis ausgeben. Kein Stopp,
   kein Auto-Run.

---

## Templates-Referenz

| Template | Pfad | Verwenden fuer |
|---|---|---|
| Vision | `templates/vision.md` | Initiale PROJECT_VISION.md |
| Deferred | `templates/DEFERRED.md` | Initiale DEFERRED.md |
| PO-Config | `templates/po-config.yaml.example` | Initiale po-config.yaml |

---

## Aktivierung in Projekt-CLAUDE.md

Folgende Zeilen in die `CLAUDE.md` des Projekts einfuegen:

```markdown
## Skill: PO
Aktiv. Vision-Constitution: docs/PROJECT_VISION.md (Pflicht-Lese-Datei in jedem Implementer-Bootstrap)
Backlog-Hygiene: docs/DEFERRED.md (geparkte Ideen) | docs/po-outcomes.md (Outcome-Reviews)
Commands: /po-init (einmalig) | /po-challenge (vor jedem neuen Ticket) | /po-prioritize (Backlog ranken) | /po-verify-outcome TICKET-NNN (>= 14 Tage nach done) | /po-reconcile (Vision-Drift-Vorschlag + Living-Docs synchron, schreibt NIE die Vision)
SDD-Hook: Ticket-Frontmatter braucht `vision_principle: <principle_id>` bevor Status auf `spec` darf (Warning per Default, Hard-Block bei `PO_SKILL_STRICT=1`).
Bootstrap-Drift-Check: Beim Lesen von docs/PROJECT_VISION.md die `reconcile_trigger`-Bedingung pruefen; bei Faelligkeit EINEN passiven Hinweis ausgeben (kein Stopp, kein Auto-Run).
Config: docs/po-config.yaml (outcome_review_days, cooldown_default_hours, rice_effort_mapping, reconcile_trigger, reconcile.living_docs).
```
