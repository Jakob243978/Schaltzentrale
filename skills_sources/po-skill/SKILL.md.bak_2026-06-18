---
name: po-skill
version: 0.1
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
Commands: /po-init (einmalig) | /po-challenge (vor jedem neuen Ticket) | /po-prioritize (Backlog ranken) | /po-verify-outcome TICKET-NNN (>= 14 Tage nach done)
SDD-Hook: Ticket-Frontmatter braucht `vision_principle: <principle_id>` bevor Status auf `spec` darf (Warning per Default, Hard-Block bei `PO_SKILL_STRICT=1`).
Config: docs/po-config.yaml (outcome_review_days, cooldown_default_hours, rice_effort_mapping).
```
