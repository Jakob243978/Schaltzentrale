---
name: agile-sdd
version: 0.6
description: Agile Spec-Driven Development mit KI-Agenten. Aktivieren wenn ein Agent eigenstaendig Software-Features implementieren soll — Ticket-Erstellung, Spec-First-Entwicklung, ADRs, Living Documentation, Governance-Log, EARS-getriebene Verifikation (Verifier-Subagent), Cost-Tracking (Token/USD pro Ticket) und kontrollierte Parallelisierung (Git Worktrees). Verwende diesen Skill wenn der User Features implementieren, Tickets bearbeiten, Architektur-Entscheidungen treffen, einen Verify-Pass starten (`/sdd-verify TICKET-NNN`) oder den Projekt-Status aktualisieren will.
---

# Agile Spec-Driven Development Skill

Dieser Skill steuert wie ein KI-Agent selbstaendig Software-Projekte entwickelt. Der Business-Owner (Jakob) schreibt keine Zeile Code — er beschreibt Anforderungen, der Agent erledigt alles andere und dokumentiert alle Entscheidungen nachvollziehbar.

---

## 0) Governance-Grundregel: Kein Fix ohne Ticket und Code

> [!important] „Wir fixen nichts ohne Ticket und Code dazu." (Jakob, 2026-06-05)
>
> **Jede Aenderung an Code, Daten oder Konfiguration MUSS ein Ticket (Spec)
> haben UND ueber zugehoerigen Code/Commit laufen — bevor sie angewandt wird.**
> Dieses Prinzip steht ueber allen anderen Workflow-Schritten: ein Ticket ist
> der Eintrittspunkt jeder Mutation, nicht eine nachtraegliche Dokumentation.

Das gilt **ausdruecklich auch** fuer:

- **Hotfixes / „schnelle" Korrekturen** — Dringlichkeit ist kein Freibrief.
  Auch der Einzeiler braucht Ticket + Commit.
- **Daten-Bereinigungen, Backfills, manuelle DB-Eingriffe** — jedes
  `UPDATE`/`cancel`/Status-Setzen, jede Korrektur „von Hand" in der Datenbank
  laeuft ueber ein Ticket und einen nachvollziehbaren, wiederholbaren
  Code-/Skript-Pfad (z.B. ein migrations-/backfill-Skript im Repo), nicht ueber
  einen Ad-hoc-Befehl in der Konsole.
- **Konfig-/Infra-Eingriffe** — Konfig-Werte, ENV, Deploy-/Infra-Aenderungen.

**Verboten:** Ad-hoc-Mutation „mal eben direkt in der DB" oder „kurz per Hand"
ohne Ticket + nachvollziehbaren Code.

**Einzige Ausnahme:** reine **Lese-/Diagnose-Operationen** (read-only `SELECT`,
Status-Checks, Health-Checks, Log-Auswertung) — die brauchen kein Ticket.
Sobald eine Operation Zustand veraendert, greift die Grundregel.

**Begruendung:** Nachvollziehbarkeit + Vertrauen. Lehre aus einer Session, in der
direkte DB-Bereinigungen ohne dediziertes Ticket zu Verwirrung fuehrten — die
Aenderung war nicht reproduzierbar und nicht im Audit-Trail. Ticket + Commit
machen jede Mutation auffindbar, begruendet und wiederholbar.

> [!info] Praktische Konsequenz
> Faellt waehrend einer Session eine noetige Korrektur auf (auch eine winzige
> Daten-Bereinigung): **zuerst ein Ticket anlegen** (Status `idea`/`spec`,
> Spec-First-Workflow Abschnitt C), dann die Aenderung als Code/Commit fahren —
> erst dann anwenden. Nicht „erst fixen, Ticket spaeter".

---

## A) Agent Bootstrap-Sequenz

Beim Start jeder neuen Session oder nach Erhalt eines neuen Tasks IMMER in dieser Reihenfolge lesen:

1. **`CLAUDE.md`** (Projekt-Root) — Projektkontext, Stack, Pfade, Claude-spezifische Regeln. PFLICHT.
2. **`docs/PROJECT_SPEC.md`** — Systemzweck, Architektur, Datenmodell, Tech-Stack. Gibt den "Was-ist-das"-Kontext.
3. **`docs/adr/`** (alle Dateien, neueste zuerst) — Warum das System so gebaut ist wie es ist. Verhindert Wiederholung schon verworfener Alternativen.
4. **`docs/tickets/`** (nur Status `in_progress` und `spec`) — Was gerade aktiv ist. Maximal 10 Tickets.
5. **`ROADMAP.md`** — Wo das Projekt hingeht. Hilft bei Priorisierungs-Entscheidungen.
6. **`CHANGELOG.md`** (letzte 20 Zeilen) — Was zuletzt geaendert wurde. Vermeidet Doppelarbeit.
7. **`docs/governance_log.md`** (letzte 10 Eintraege) — Letzte autonome Entscheidungen. Zeigt Kontext juengster Aenderungen.
8. **Verify-Status pruefen:** Fuer jedes Ticket mit Status `review` pruefen, ob ein
   Verify-Report in `<verify_report_path>/TICKET-NNN-verify-*.md` existiert. Falls
   nicht: dem User aktiv vorschlagen, **`/sdd-verify TICKET-NNN`** auszufuehren,
   bevor das Ticket auf `done` gesetzt wird. Sektion F.4 erklaert den Verifier-Pass
   im Detail.
9. **Parallelisierungs-Check:** Wenn mehrere Tickets gleichzeitig `in_progress`
   sind, pruefen ob deren `Code-Referenzen` disjunkte Datei-Sets ergeben. Bei
   Ueberlapp (insbesondere `db/models.py`, `api/main.py`, gemeinsame Worker,
   `CLAUDE.md`, `PROJECT_SPEC.md`): auf ein Ticket beschraenken oder klar
   sequenzieren. Sektion J definiert die Parallelisierungs-Regeln.
10. **inbox-Check (passiv):** Wenn `inbox/`-Ordner existieren (pro Workflow-/
    Projekt-Verzeichnis), pruefen ob darin unverarbeitetes Material liegt
    (alles ausser `.gitkeep` und dem Unterordner `archive/`). Falls ja:
    **passiver Hinweis** an den User — z.B. *"3 Files in `workflows/prod/x/inbox/`
    warten auf Spec-Verarbeitung."* **Nicht** aktiv nachfragen, ob jetzt
    gespec't werden soll, und **nicht** blockieren. Der Hinweis macht das
    Material sichtbar; die Entscheidung, daraus ein Ticket zu specen, bleibt
    beim User. Details: Sektion **K**.

Wenn eine Datei nicht existiert: weiter zur naechsten. Nicht stoppen, nicht nachfragen.

Wenn `docs/PROJECT_SPEC.md` fehlt: als allererste Aktion vor jeder anderen Arbeit anlegen (Vorlage: `templates/PROJECT_SPEC.md`).

> [!info] Cost-Tracking
> Bei Verify-Pass: Token-Aggregation passiert automatisch durch den Verifier
> (5 Pflicht-Felder im Verify-Report-Frontmatter). Siehe Sektion **F.6**.

---

## B) Ticket-Workflow

### Ticket-Format (Pflichtfelder)

Jedes Ticket lebt als eigene Datei unter `docs/tickets/TICKET-NNN.md` (dreistellige Nummerierung, NNN = naechste freie Nummer).

```
# TICKET-NNN: [Kurztitel — max. 60 Zeichen]

**Status:** [idea | spec | in_progress | review | done]
**Erstellt:** YYYY-MM-DD
**MoSCoW:** [Must | Should | Could | Wont]
**Geschaetzter Aufwand:** [XS | S | M | L | XL]
**inbox_source:** [optional — Pfad zum inbox/-Material, aus dem dieses Ticket entstand]

## Was soll erreicht werden? (Business-Ziel)
<!-- In einem Satz: Wer profitiert wie davon? -->

## Akzeptanzkriterien (EARS-Format)
<!-- "When [Bedingung], the system shall [Aktion]." -->
- [ ] When ..., the system shall ...
- [ ] When ..., the system shall ...

## Loesungs-Skizze (Approach)
<!-- SKILL-019: Pflicht ab Aufwand M/L/XL, optional bei XS/S. 3-6 Zeilen.
     - Gewaehlter Ansatz: ...
     - Verworfene Alternative(n): ...
     - Betroffene Module: ...
     Bei Architektur-Weiche stattdessen auf ADR-NNN verweisen, nicht doppeln. -->

## Technische Hinweise
<!-- Nur wenn relevant: Pfade, APIs, Abhaengigkeiten, Risiken -->

## Code-Referenzen
<!-- Dateien/Funktionen die betroffen sind -->

## Spec-Delta
<!-- SKILL-018: NUR wenn dieses Ticket PROJECT_SPEC.md (oder eine andere
     Spec-Datei) veraendert — sonst Block weglassen.
     - Vorher: <was die Spec bisher sagte>
     - Nachher: <was sie jetzt sagt>
     - Anlass: <warum>
     Beim done-Schritt im CHANGELOG ### Technical referenzieren. -->

## Ergebnis / Notizen
<!-- Wird vom Agenten beim Abschliessen befuellt -->
```

### Status-Flow

```
idea --> spec --> in_progress --> review --> done
```

- **idea**: Anforderung existiert, noch nicht ausformuliert
- **spec**: Akzeptanzkriterien und technische Hinweise vollstaendig
- **in_progress**: Agent arbeitet aktiv daran
- **review**: Implementierung fertig, Tests gruen, Verifier-Pass + (bei UI-EARS) manuelle PO-Abnahme stehen aus
- **done**: Abgenommen, CHANGELOG aktualisiert, Code-Kommentare gesetzt

### PO-Skill-Hook (Status-Uebergang `idea` -> `spec`)

Wenn der `po-skill` im Projekt aktiv ist (erkennbar an
`docs/PROJECT_VISION.md` + `## Skill: PO`-Block in `CLAUDE.md`), gilt **vor**
dem Setzen von Status `spec`:

1. Pruefe ob das Ticket-Frontmatter ein Feld
   `vision_principle: <principle_id>` enthaelt.
2. Pruefe ob `<principle_id>` in `docs/PROJECT_VISION.md` als
   `Kern-Prinzip` existiert (Slug-Match).
3. Wenn **nein**:
   - **Default (Warning):** Hinweis an User:
     *"Kein `vision_principle` referenziert — `/po-challenge` empfohlen
     bevor Implementierung startet. Status-Uebergang trotzdem moeglich,
     wenn du sicher bist."*
   - **Strict-Mode** (`docs/po-config.yaml: strict_vision_principle: true`
     oder ENV `PO_SKILL_STRICT=1`): Hard-Block. Status bleibt `idea` bis
     Prinzip ergaenzt ist.

Beim Status-Uebergang `in_progress` -> `done` setzt der Implementer
automatisch:

```yaml
outcome_review_at: <heute + outcome_review_days aus docs/po-config.yaml>
```

(Default `outcome_review_days: 14`.) Damit `/po-verify-outcome --all-due`
spaeter den Termin findet.

Wenn der `po-skill` **nicht aktiv** ist (keine `PROJECT_VISION.md`), bleibt
der Status-Flow unveraendert — kein Vision-Prinzip-Check, kein
Outcome-Review.

`review` ist **obligatorischer Zwischenschritt** vor `done`, nicht optional. In
`review` laeuft:
1. Verifier-Pass (`/sdd-verify TICKET-NNN`) — Verify-Report wird unter
   `docs/tickets/verify/TICKET-NNN-verify-YYYY-MM-DD.md` abgelegt.
2. Manuelle PO-Abnahme durch Jakob — **nur fuer UI-EARS-Saetze** (siehe F.4
   Klassifizierung). Backend-/Worker-EARS-Saetze gelten als automatisch abgenommen,
   wenn der Verifier-Pass `pass` ergibt (`health_check` + Tests + Diff-Pruefung).
3. Erst wenn `verify_status: pass` UND `po_acceptance: confirmed|not_required`
   im Frontmatter des Reports stehen, darf das Ticket auf `done`.

Tickets wechseln niemals zurueck von `done` zu einem anderen Status. Korrekturen erzeugen ein neues Ticket.

### Status-Transition `review` → `done` — Auto-Doku-Hook (TICKET-078 + TICKET-079)

Beim Setzen eines Tickets auf `done` MUSS der Implementer (oder Operator)
unmittelbar danach die folgenden zwei Generatoren laufen lassen, **wenn
das Projekt sie hat** (Opt-in: greift nur wenn die Worker-Module existieren):

1. `python -m workers.feature_map_generator` — re-generiert `docs/FEATURE_MAP.md`
   aus allen `done`-Tickets (Heuristik nach Job-Kategorie + Vision-Prinzip).
2. `python -m workers.project_overview_generator` — re-generiert
   `docs/PROJECT_OVERVIEW.html` (Vision + Prinzip-Karten + Feature-Mapping +
   Live-DB-Stats). Standalone-HTML, oeffnet auch ohne Backend im Browser.
3. `python -m workers.traceability_generator` — re-generiert
   `docs/TRACEABILITY.md`, die Requirement→Test→Code→Verify-Matrix (SKILL-017,
   Sektion **F.7**). Aggregiert NUR vorhandene Artefakte (EARS-IDs aus Tickets,
   `test_ears_N`-Tests, `# TICKET-NNN`-Code-Marker, Verify-Report-Status) — keine
   neue Datenquelle. Opt-in: greift nur wenn das Projekt den Generator hat.

Implementer-Bericht enthaelt die HTML-Update-Bestaetigung als Pflicht-Zeile
(z.B. "Feature-Map + Projekt-Uebersicht regeneriert: 47 done-Tickets,
HTML-Datei aktualisiert"). Bei Fehlern: nicht das `done` blocken, aber im
Bericht klar als WARN markieren — die Generatoren sind best-effort.

Pruefung am Bootstrap (`A.8` Verify-Status): Wenn `docs/PROJECT_VISION.md`
existiert UND es done-Tickets gibt aber `docs/FEATURE_MAP.md`,
`docs/PROJECT_OVERVIEW.html` oder `docs/TRACEABILITY.md` (SKILL-017) fehlen /
aelter als das juengste done-Ticket sind, schlaegt der Agent dem User aktiv vor,
die entsprechenden Generatoren einmal zu laufen. (Der TRACEABILITY-Frische-Check
greift auch ohne PROJECT_VISION.md, sobald done-Tickets existieren.) Strict-Mode
(Hard-Block) ist nicht vorgesehen — die Datei-Pflege darf nie die eigentliche
Ticket-Arbeit blockieren.

### Implementer-Briefing-Standards (Pflicht-Bloecke pro Subagent)

Beim Spawn eines Implementer-Subagents (per Operator, Lead-Claude oder
direkt durch den User) MUESSEN die passenden Standard-Bloecke aus
`templates/IMPLEMENTER_BRIEFING_STANDARDS.md` ans Ende des Subagent-
Briefings kopiert werden. Default-Auswahl:

- **Immer:** Block "Implementer-Hygiene" (Token-Budget, Scope-Hygiene).
- **Bei Ticket mit Datenmodell-Touch ODER neuen Endpoints:** Block
  "API-Schema-Mitdenken" (SKILL-010, 2026-06-01). Verhindert die T103a-
  Anti-Pattern-Klasse (neue Modell-Felder werden nie via API ausgeliefert).
- **Bei SKILL-NNN-Tickets:** Block "Skill-Code-Pfad" (Source-of-Truth +
  setup.ps1-Hinweis).

Operator-Templates (`operator-templates` Skill) referenzieren diese Datei
in ihren Briefing-Bloecken — siehe deren SKILL.md "MCP/API-Schema-Hinweis".

### Code-Referenz-Pattern

Jede Stelle im Code die ein Ticket implementiert bekommt einen Kommentar:

```python
# TICKET-042: Inline-Status-Aenderung via Dropdown
```

```typescript
// TICKET-042: Inline-Status-Aenderung via Dropdown
```

Beim Commit:
```
[TICKET-042] Inline-Status-Dropdown fuer Property-Ampel
```

Bei mehreren Tickets in einem Commit:
```
[TICKET-041][TICKET-042] Status-Dropdown + Ampel-Farben
```

### Loesungs-Skizze-Block (Design-Phase light) — SKILL-019

Zwischen `## Akzeptanzkriterien` und Code fehlt sonst ein festgehaltener
Design-Schritt. Kiro/spec-kit haben dafuer eine eigene **Design-Phase**
(`Requirements → Design → Tasks`); wir holen das leichtgewichtig als
ticket-lokalen Block nach — gegen die **Cognitive Debt** (ThoughtWorks v34: KI
baut, Mensch versteht das "wie" nicht mehr).

- **Pflicht ab Aufwand `M`/`L`/`XL`:** Bevor ein solches Ticket nach
  `in_progress` wechselt, wird der `## Loesungs-Skizze (Approach)`-Block mit
  (1) gewaehltem Ansatz, (2) mind. einer **verworfenen Alternative** und
  (3) **betroffenen Modulen** ausgefuellt (3–6 Zeilen genuegen).
- **Optional bei `XS`/`S`:** Trivial-Tickets brauchen den Block nicht — kein
  Overhead.
- **Status-Gate (weich):** Fehlt der Block bei einem M/L/XL-Ticket beim Wechsel
  nach `in_progress`, gibt der Agent einen Hinweis aus ("Loesungs-Skizze fehlt —
  bei M/L/XL erwartet"). Default ist **Warning**; Hard-Block nur bei
  `docs/sdd-config.yaml: approach_block_required_for_ML: true`.
- **Abgrenzung zu ADR (Sektion D):** Der Approach-Block ist das **ticket-lokale,
  vergaengliche "wie"**. Beruehrt der gewaehlte Weg eine **projektweite
  Architektur-Weiche** (ADR-Kriterium), wird im Block auf das ADR verwiesen statt
  die Entscheidung doppelt auszuformulieren — kein Doppel-Dokument.
- **Konsistenz:** Die "betroffene Module"-Angabe kuendigt an, was die spaeteren
  `## Code-Referenzen` belegen — so weiss eine KI in einer neuen Session vorab,
  **wo im Code einzugreifen ist**, und welche Alternative schon verworfen wurde.

### Spec-Delta-Block (Brownfield-Nachvollziehbarkeit) — SKILL-018

`PROJECT_SPEC.md` wird **waehrend** der Implementierung aktualisiert (Sektion C).
Damit die konkrete Aenderung nicht in der Git-History verschwindet, fuehrt jedes
Ticket mit Spec-Touch einen `## Spec-Delta`-Block:

- **Pflicht bei Spec-Touch:** Veraendert das Ticket `PROJECT_SPEC.md` (oder eine
  andere Spec-Datei), wird der Block mit **Vorher / Nachher / Anlass** ausgefuellt
  (Kurzfassung, kein Voll-Diff).
- **Weglassbar sonst:** Ohne Spec-Touch entfaellt der Block — kein leerer
  Pflicht-Block.
- **CHANGELOG-Kopplung:** Beim Uebergang nach `done` wird der Spec-Delta-Verweis
  im CHANGELOG `### Technical` referenziert
  (`[TICKET-NNN] Spec-Delta: <Kurzfassung>`).
- **Governance bleibt:** Der Block **ergaenzt** die bestehende Governance-Log-
  Pflicht "Jede Aenderung an PROJECT_SPEC.md" (Sektion I), ersetzt sie nicht.
- **Bewusst leichtgewichtig:** Delta-Notiz **im Ticket**, KEIN separates
  Delta-File pro Ticket und kein `propose/apply/archive`-Workflow wie OpenSpec —
  das waere fuer dieses Setup Over-Engineering.

---

## C) Spec-First-Workflow

Vor dem Schreiben von neuem Code:

1. Pruefen ob `docs/PROJECT_SPEC.md` existiert und aktuell ist.
2. Wenn neue Architektur-Entscheidung noetig: ADR anlegen (Abschnitt D).
3. Ticket auf Status `spec` setzen und alle Akzeptanzkriterien vollstaendig formulieren.
4. Bei Aufwand `M`/`L`/`XL`: `## Loesungs-Skizze (Approach)`-Block im Ticket
   ausfuellen, bevor der Status auf `in_progress` geht (Design-Phase light,
   SKILL-019 — Details in Sektion B "Loesungs-Skizze").
5. Erst dann mit Implementierung beginnen.

### PROJECT_SPEC.md Pflichtinhalt

```
# PROJECT_SPEC.md

## Systemzweck
<!-- Ein Absatz: Was loest das System? Fuer wen? -->

## Architektur-Ueberblick
<!-- Komponenten + Datenfluesse, max. 10 Zeilen oder ASCII-Diagramm -->

## Tech-Stack
<!-- Sprache, Framework, DB, externe Dienste — je eine Zeile mit Begruendung -->

## Datenmodell (Kerntabellen / Kern-Entities)
<!-- Nur die wichtigsten Entities mit Feldern. Kein vollstaendiges Schema. -->

## Externe Abhaengigkeiten
<!-- APIs, Webhooks, Cron-Jobs, MCP-Verbindungen die das System braucht -->

## Bekannte Constraints
<!-- Was darf nicht geaendert werden? Was ist gesetzt? -->

## Letzte Spec-Aktualisierung
<!-- YYYY-MM-DD, Anlass -->
```

Die Spec wird **waehrend** der Implementierung aktualisiert, nie nachtraeglich in
einer separaten Session. **Jede Spec-Aenderung wird zusaetzlich im
`## Spec-Delta`-Block des ausloesenden Tickets als Vorher/Nachher-Kurzfassung
festgehalten** (SKILL-018, Brownfield-Nachvollziehbarkeit) — so verschwindet die
Aenderung nicht in der Git-History, sondern bleibt ticket-lokal auffindbar.
Details: Sektion B "Spec-Delta-Block".

---

## D) Architecture Decision Records (ADR)

Format: MADR (Markdown Any Decision Records) — schlankes Format, listet Alternativen explizit.

Ablage: `docs/adr/ADR-NNN-kurztitel.md` (dreistellig, Kebab-Case-Titel).

> [!info] ADR vs. Loesungs-Skizze-Block (SKILL-019)
> Ein **ADR** haelt eine **projektweite, immutable Architektur-Weiche** fest
> (eigenes File, Status-Flow). Der **`## Loesungs-Skizze (Approach)`-Block** im
> Ticket (Sektion B) ist das **ticket-lokale, vergaengliche "wie"** eines
> einzelnen Tickets. Beruehrt eine Loesungs-Skizze eine Architektur-Weiche →
> ADR anlegen und im Block darauf verweisen, nicht beides ausformulieren.

### Wann ein ADR anlegen

- Neue Datenbank-Technologie oder Schema-Strategie
- Wechsel oder Ergaenzung im Tech-Stack
- Sicherheits-relevante Entscheidung
- Abkehr von einer bestehenden Konvention
- Externe API-Integration (Auswahl unter mehreren Optionen)
- Jede Entscheidung bei der "warum nicht X" relevant ist

### ADR-Status-Flow

```
Proposed --> Accepted --> (Deprecated | Superseded by ADR-NNN)
```

ADRs sind nach Abschluss unveraenderlich. Korrekturen = neues ADR mit `Superseded by`-Referenz.

### Agent-Autonomie bei ADRs

Da Jakob volle KI-Autonomie gewaehlt hat: Der Agent legt ADRs selbst an, setzt Status auf `Accepted` und traegt die Entscheidung ins Governance-Log ein. Jakob reviewed asynchron.

Ausnahme: Entscheidungen die externe Kosten erzeugen (neue bezahlte APIs, Cloud-Ressourcen) oder die bestehende Produktions-Daten unwiederbringlich veraendern — diese IMMER mit Jakob absprechen, bevor sie umgesetzt werden.

---

## E) Living Documentation

### CHANGELOG.md

Zwei Sektionen pro Release-Eintrag:

```markdown
## [YYYY-MM-DD] vX.Y — Kurztitel

### Technical
- [TICKET-NNN] Was wurde implementiert (Pfad/Komponente)
- [TICKET-NNN] Spec-Delta: <Kurzfassung der PROJECT_SPEC-Aenderung> (nur bei Spec-Touch, SKILL-018)
- [TICKET-NNN] ...

### User-Facing
- Was der Nutzer jetzt tun kann / was sich verbessert hat
- Keine technischen Details, keine Dateinamen
```

Wird nach jedem abgeschlossenen Ticket (Status `done`) aktualisiert. Nicht
gesammelt am Ende. Hat ein Ticket einen `## Spec-Delta`-Block (SKILL-018), wird
dessen Kurzfassung als eigene `### Technical`-Zeile referenziert.

### ROADMAP.md

Format: Now / Next / Later. Keine langen Beschreibungen.

```markdown
## Now (aktiv in Arbeit)
- [TICKET-NNN] Kurztitel — Business-Nutzen in einem Satz

## Next (naechste Prioritaet, bereit fuer Umsetzung)
- [TICKET-NNN] Kurztitel — Business-Nutzen

## Later (Ideen, noch nicht priorisiert)
- Kurztitel — Business-Idee (kein Ticket noetig bis Priorisierung)
```

Wird vom Agenten nach jedem Sprint-Abschluss oder auf Jakobs Anfrage aktualisiert.

### docs/TRACEABILITY.md (SKILL-017)

Lebende Requirement→Test→Code→Verify-Matrix, beim done-Hook regeneriert
(Sektion B + **F.7**). Aggregiert vorhandene Artefakte, keine Hand-Pflege.
Zeigt auf einen Blick ungetestete EARS-Saetze, nicht-gruene Tests, verwaiste
Code-Pfade und Tickets ohne Verify-Report. Template: `templates/TRACEABILITY.md`.

### docs/developer_notes/

Freies Format. Technische Notizen die nicht in CHANGELOG passen: Debugging-Erkenntnisse, Temporaere Workarounds, Tooling-Eigenheiten. Dateiname: `YYYY-MM-DD-thema.md`.

---

## F) Test- und Qualitaetsstrategie

### F.1 Was immer getestet wird

- **Happy Path**: Der Normalfall laut Akzeptanzkriterium
- **Kritischer Edge Case**: Der gefaehrlichste Sonderfall (leere Eingabe, ungueltige ID, fehlende Daten)

### F.2 Was nicht getestet wird

- UI-Details (Farben, Abstands-Pixel, Icon-Auswahl)
- Cosmetic Changes (Umbenennung von Labels die keine Logik aendern)
- Dokumentations-Aenderungen

### F.3 Test-Pflicht — 1 EARS = mindestens 1 Test

**Pflicht-Regel:** Pro EARS-Akzeptanzkriterium im Ticket MUSS mindestens ein
pytest-Test-Case existieren, der diesen Satz konkret abdeckt. Tests werden
**idealerweise vor** dem Implementierungscode geschrieben (TDD); zwingend ist nur,
dass sie **vor dem Verify-Pass** existieren und gruen laufen.

Empfohlene Konventionen, damit der Verifier-Subagent Tests automatisch zuordnet:

- Test-Datei pro Ticket: `tests/test_ticket_NNN_<kurzname>.py`
- Test-Name spiegelt EARS-Nummer: `def test_ears_1_<stichwort>()`
- Im Docstring oder Kommentar: `# TICKET-NNN, EARS-N: <kurze EARS-Phrase>`

### Test-Protokoll

Der Agent schreibt Tests gleichzeitig mit dem Code (nicht nachtraeglich). Nach Fertigstellung:

1. Tests ausfuehren (`test_command` aus `docs/sdd-config.yaml`).
2. Ergebnis ins Ticket-Feld "Ergebnis / Notizen" eintragen: `Tests: N passed, M failed`.
3. Bei Failures: Ursache diagnostizieren und beheben bevor Status auf `review`
   gesetzt wird.
4. Status auf `review`, dann **`/sdd-verify TICKET-NNN`** ausfuehren (siehe F.4).

### F.4 Verifier-Pass (Subagent in frischer Session)

Vor dem Uebergang `review` → `done` wird **immer** ein Verifier-Pass ausgefuehrt.
Der Verifier-Subagent laeuft in einer **frischen Session ohne Reasoning-History**
des Implementer-Agents (Bias-Vermeidung).

**Aufruf:** `/sdd-verify TICKET-NNN` (Slash-Command aus diesem Skill,
`commands/sdd-verify.md`).

**Was der Verifier macht:**
1. Liest `~/.claude/skills/agile-sdd-skill/verifier/VERIFIER.md` und
   `docs/sdd-config.yaml`.
2. Liest das Ticket, sammelt Diff + Test-Output + Health-Check.
3. Prueft pro EARS-Satz: Implementierung gefunden? Test gefunden? Test gruen?
   Edge-Cases plausibel? Status `pass | partial | fail`.
4. Schreibt Verify-Report nach `<verify_report_path>/TICKET-NNN-verify-YYYY-MM-DD.md`
   strikt nach Template `templates/verify-report.md`.
5. Schreibt 8-zeiligen Eintrag ins `docs/governance_log.md` (mit Link zum Report).
6. Haengt Kurz-Notiz ans Ende des Original-Tickets.

**Pflicht-Inhalt des Reports — differenziert nach UI- vs Backend-EARS:**

Der Verifier klassifiziert jeden EARS-Satz beim Pruefen als **ui** oder **backend**.
Die "Manuelle PO-Abnahme"-Sektion ist nur fuer UI-EARS-Saetze Pflicht. Backend-EARS
werden ueber den Verifier-Output (Tests + Health-Check + Diff) automatisch
abgenommen — Jakob soll nicht jeden Backend-Test selbst re-runnen.

**Klassifizierungs-Regeln (EARS-Satz ist UI wenn mindestens eine zutrifft):**
1. Implementierung liegt unter `frontend/` (z.B. `frontend/app/`, `frontend/components/`).
2. EARS-Satz nennt explizit Browser-Interaktion ("klickt", "hovert", "Dropdown",
   "Tooltip", "sichtbar", "Spalte zeigt", "Dialog oeffnet").
3. EARS-Satz hat explizites Tag `[ui]` oder `[manual]` am Zeilenende.
4. Im Zweifel: **ui** (Sicherheits-Default — lieber einmal mehr klicken als
   einen Bug uebersehen).

Alle anderen EARS-Saetze (Worker-CLI, API-Endpoint ohne UI-Effekt, DB-Migration,
Cron-Job, Hintergrund-Job) gelten als **backend**.

**Sektion "Manuelle PO-Abnahme" im Report:**
- **Wenn mindestens ein UI-EARS-Satz existiert:** Pflicht-Sektion mit
  Klick-Pfad / URL, erwartetem sichtbarem Verhalten pro UI-EARS-Satz,
  Pass/Fail-Markierung via Frontmatter `po_acceptance: pending|confirmed|rejected`.
  Backend-EARS-Saetze werden in der gleichen Sektion mit
  "automatisch abgenommen — siehe Test-Output / Health-Check" markiert.
- **Wenn ausschliesslich Backend-EARS:** Sektion enthaelt nur den Hinweis
  "Keine UI-EARS — automatische Abnahme via Verifier-Output". Frontmatter:
  `po_acceptance: not_required`. Jakob muss nichts klicken.

**Lesson Learned (TICKET-009, 2026-05-21):**

> [!warning] Verifier kann Hover-/Click-Bugs nicht entdecken
> Der Verifier-Subagent hat keine Browser-Capability. Er prueft Source-Code
> per Substring-Match — das deckt UI-Verhalten NICHT zuverlaessig ab. Bei
> TICKET-009 markierte der Verifier "Tooltips auf Quelle-Icons" als `pass`,
> obwohl die Tooltips real nicht funktionierten (CSS-Klasse fehlte). Erst
> Jakobs manueller Hover-Test im Browser deckte den Bug auf.
>
> **Konsequenz:** Fuer UI-EARS-Saetze ist die PO-Manuelle-Abnahme der
> **Sicherheitsanker**, nicht eine Doppelpruefung. Der Verifier darf UI-EARS
> hoechstens auf `partial` setzen, wenn er die Implementierung im Diff findet —
> `pass` setzt erst Jakobs Klick-Test nach `po_acceptance: confirmed`.

Jakob nimmt **UI-Tickets selbst ab**. Backend-Tickets nimmt der Verifier ab.

**Was der Verifier NICHT tut:** Code aendern, Tests aendern, Akzeptanzkriterien
aendern, Ticket-Status auf `done` setzen. Er produziert nur den Report — der
Status-Uebergang bleibt eine bewusste Implementer/PO-Entscheidung.

### F.5 Property-Based Testing (Add-on, optional)

Fuer Daten-Worker (Regex-Extraktion, Pattern-Matching, Heuristiken auf
ungetypten Inputs) ist Property-Based Testing (Python: Hypothesis, TS:
fast-check) ein wertvoller Add-on. Aus EARS-Saetzen werden Invarianten
extrahiert ("fuer alle gueltigen Inputs muss X gelten"), die mit zufaelligen
Inputs geprueft werden.

**Konvention pro Projekt:** Property-Based Testing ist standardmaessig **aus**.
Aktivierung erfordert ein eigenes ADR mit Begruendung + Scope. Im
`docs/sdd-config.yaml` wird `property_based_tests_enabled: true` gesetzt; ohne
ADR bleibt es bei `false`.

**Gut geeignet:** `workers/extract_kpis.py`, `workers/imap_backfill.py`-Match,
JSON-Parser, ID-Extraktoren.
**Schlecht geeignet:** UI-Komponenten, Migrations-Skripte, externe API-Wrapper.

Akzeptanzkriterien im Ticket sind die direkte Testbasis: EARS-Satz → Test-Fall.

### F.6 Cost-Tracking (Token-Verbrauch pro Ticket)

Jeder Verify-Report enthaelt seit v0.4 fuenf Pflicht-Felder im Frontmatter, die
den Token-Verbrauch und die Kosten des Tickets aggregieren. Der Verifier-Subagent
befuellt diese Felder als letzten Schritt seines Pruefungs-Algorithmus
(siehe `verifier/VERIFIER.md`, Schritt 6).

#### Warum

1. **Transparenz** — Anthropic-Industrie-Schnitt liegt bei ca. 13 USD pro
   Entwickler pro aktiven Tag. Ein einzelner `cost_usd`-Wert pro Ticket macht
   sichtbar, ob ein Setup im normalen Rahmen laeuft.
2. **Spec-Qualitaets-Proxy** ueber `implementer_iterations` (Standard-Feld):
   Anzahl Implementer-Sessions pro Ticket. 1 Iteration = perfekte Spec, ≥ 3 =
   Spec war unscharf. Das ist die **eigentlich aussagekraeftige SDD-Metrik**.
3. **Trend-Analyse** ueber Tickets hinweg — wird die Cache-Hit-Rate ueber
   Zeit besser (CLAUDE.md wird praegnanter)? Wird `cost_usd` pro Ticket-
   Komplexitaet stabiler (Spec-Praezision steigt)?

#### Die 5 Pflicht-Felder im Verify-Report

```yaml
tokens_in_total: 84230      # input + cache_creation + cache_read summiert
tokens_out_total: 12450     # output
cache_hit_rate: 0.73        # cache_read / (cache_read + cache_creation + input_raw)
cost_usd: 0.42              # via Modell-Preise zur Run-Zeit
verifier_model: claude-sonnet-4   # bereits seit v0.3 im Template
```

Optionale Standard-Felder (empfohlen ab TICKET-005):
`implementer_iterations`, `implementer_tokens_in`, `implementer_tokens_out`.

#### Modell-Gruppierung — Pflicht-Regel

> [!important] Trend-Analysen und Ticket-Vergleiche sind NUR innerhalb desselben Modells gueltig
>
> Empirie 2026 (Microsoft Research, arxiv 2604.22750): unterschiedliche
> Frontier-Modelle koennen auf identischem Task **bis zu 1,5 Mio Tokens**
> auseinanderliegen — Kimi-K2/Claude-Sonnet-4.5 vs. GPT-5. Ein
> Token-/Cost-Vergleich zwischen Tickets aus verschiedenen Modellen ist
> **bedeutungslos**.
>
> **Regel fuer Trend-Auswertungen:**
>
> 1. Tickets werden zur Vergleichbarkeit nach `verifier_model` gruppiert.
>    Tickets mit unterschiedlichem `verifier_model` werden NICHT direkt
>    verglichen — auch nicht im optionalen Trend-File.
> 2. Wenn die Standard-Felder gefuellt sind, gilt zusaetzlich:
>    `implementer_model` muss identisch sein, sonst nur innerhalb derselben
>    Gruppe vergleichen.
> 3. Bei Modellwechsel im Projekt: im optionalen `docs/ticket_metrics.md`
>    einen sichtbaren Marker-Eintrag setzen (z.B. `--- Wechsel auf
>    claude-opus-4-7 ab TICKET-NNN ---`).
> 4. Cache-Hit-Rate ist die einzige modell-uebergreifend halbwegs
>    vergleichbare Metrik (sie misst Context-Engineering-Qualitaet, nicht
>    Modell-Effizienz) — aber auch sie schwankt zwischen Modellen, weil
>    Cache-Granularitaeten unterschiedlich sind.
>
> **Das ist nicht optional.** Modell-Mixing ist der haeufigste Grund,
> warum Cost-Tracking-Initiativen unbrauchbare Zahlen produzieren.

#### Confounders (kurze Warnliste)

- **30× Stochastik** auf identischem Task (Microsoft Research 2026) —
  Einzel-Ticket-Vergleich ist sinnlos, nur Trends ueber ≥ 5 Tickets sind
  belastbar.
- **Cache-Hit-Rate verzerrt absolute Kosten** — erstes Ticket im neuen
  Projekt ist teurer, weil noch nichts gecached. Beide Felder zusammen lesen.
- **Modellwechsel killt Vergleichbarkeit** (siehe Pflicht-Regel oben).
- **Token != Wert** — triviales Ticket mit unscharfer Spec kann teurer sein
  als komplexes Ticket mit guter Spec. Cost-Tracking ist Effizienz-, nicht
  Ergebnis-Indikator.

#### Werkzeug

- **Default-Empfehlung:** [`ccusage`](https://github.com/ryoppippi/ccusage)
  (de-facto-Standard 2026, 4800+ Stars). Aufruf via `bunx ccusage` oder global
  via `npm install -g ccusage`. Hat `--project`-Filter, kennt Modell-Preise via
  LiteLLM, gibt Cache-Felder getrennt aus.
- **Fallback ohne ccusage:** JSONL-Files direkt parsen unter
  `~/.claude/projects/c--Users-Jakob-claude-projects/*.jsonl`. Pro Zeile gibt
  es einen `usage`-Block mit `input_tokens`, `output_tokens`,
  `cache_creation_input_tokens`, `cache_read_input_tokens`. Ueber
  `sessionId`/`cwd`/`gitBranch` laesst sich pro Ticket aggregieren. 20-Zeilen-
  Python-Snippet reicht.
- **Wenn weder noch:** Verifier setzt die Felder auf `null` und schreibt im
  Report-Body einen Hinweis "ccusage nicht installiert, manueller Nachtrag
  noetig". **Der Verifier installiert NIE selbst Tooling.**

#### Weiterfuehrend

Vollstaendige Begruendung, Tooling-Vergleich, Confounder-Analyse:
[[Researcher/jakob/spec-driven-development/recherche/2026-05-21_Token_Tracking_pro_Ticket]].

### F.7 Traceability-Matrix (`docs/TRACEABILITY.md`) — SKILL-017

Die Traceability-Matrix fuehrt pro EARS-Akzeptanzkriterium die Kette
**Requirement → Test → Code → Verify-Status** in **einer** abfragbaren Datei
zusammen. Sie ist der industrielle Kern-Hebel fuer messbare Doku-Qualitaet (RTM,
Six Sigma / Ketryx) und beantwortet einer KI in einer neuen Session auf einen
Blick: *Welcher EARS-Satz hat keinen Test? Welcher Test ist nicht gruen? Wo im
Code liegt die Implementierung? Welches Ticket steht ohne Verify-Report?* — ohne
dass der gesamte Code interpretiert werden muss.

> [!important] Reine Aggregation — keine neue Datenquelle
> Die Matrix baut AUSSCHLIESSLICH auf bereits vorhandenen Artefakten auf:
> EARS-Saetze aus den Tickets, `test_ears_N`-/`test_ticket_NNN_*`-Tests,
> `# TICKET-NNN`-Code-Marker (Code-Referenz-Pattern, Sektion B) und der
> `verify_status` aus den Verify-Reports. Es entsteht keine Pflege-Last neben dem
> bestehenden Workflow — nur eine Zusammenfuehrung.

#### Zeilen-Schema (eine Zeile pro EARS-Satz)

| EARS-ID | Ticket | Test-Name | Code-Referenz | Verify-Status |
|---|---|---|---|---|
| EARS-1 | TICKET-042 | `tests/test_ticket_042.py::test_ears_1_dropdown` | `frontend/app/property.tsx:88-104` | pass |
| EARS-2 | TICKET-042 | `⚠ kein Test` | `api/main.py:210-225` | partial |

#### Markierungs-Regeln

- **Kein zugeordneter Test** (`test_ears_N` / `test_ticket_NNN_*` nicht
  gefunden) → Test-Spalte traegt `⚠ kein Test`.
- **Verify-Report `fail`/`partial`** → Status-Spalte spiegelt diesen Status
  (statt `pass`).
- **Kein Verify-Report fuer das Ticket vorhanden** → Status-Spalte traegt
  `⚠ kein Verify-Report` (komplementaer zum harten Verify-Gate aus SKILL-016).
- **Keine `# TICKET-NNN`-Code-Referenz auffindbar** → Code-Spalte traegt
  `⚠ Code-Referenz fehlt` (verwaister/nicht markierter Pfad).

#### Generator + Best-effort-Charakter

- Aufruf im done-Hook (Sektion B): `python -m workers.traceability_generator`.
- **Best-effort wie FEATURE_MAP:** ein Fehler blockt NIE das `done` — er wird im
  Implementer-Bericht als WARN markiert.
- Wo ein Projekt (noch) keinen deterministischen Generator hat, ist die Matrix
  agentisch pflegbar (LLM liest Tickets + Tests + Verify-Reports und fuellt
  `docs/TRACEABILITY.md` nach `templates/TRACEABILITY.md`). Ein projekt-lokaler
  `traceability_generator.py` ist das Lift-and-Shift-Ziel (analog
  feature_map_generator) — kein Skill-Kern.

Template: `templates/TRACEABILITY.md`.

---

## G) Monitoring und Betrieb

### Log-Konventionen (in CLAUDE.md des Projekts dokumentieren)

```
ERROR: [Komponente] Beschreibung — wird immer geloggt
WARN:  [Komponente] Beschreibung — wird geloggt, kein Stopp
INFO:  [Komponente] Beschreibung — nur bei Debug-Modus
```

Strukturierte Logs (JSON) wenn der Service produktiv laeuft.

### Runbooks

Fuer jeden kritischen Service eine Datei `docs/runbooks/SERVICE.md` anlegen. Pflichtinhalt:
- Was macht der Service?
- Wie startet/stoppt man ihn?
- Was sind bekannte Fehlermuster und wie werden sie behoben?
- Wie prueft man ob er laeuft?

Runbook wird angelegt wenn ein Fehler zum ersten Mal auftritt und analysiert wurde.

### KI-Alerting-Regel

Agent behebt selbst:
- Bekannte Fehler mit dokumentiertem Runbook-Recovery
- Test-Failures bei eigenem Code
- Import-Fehler / fehlende Packages

Agent informiert Jakob:
- Unbekannte Fehler ohne Runbook-Eintrag
- Fehler die Produktions-Daten betreffen koennen
- Externe API-Probleme (Credentials, Rate Limits)
- Wenn ein Fehler nach 2 Loesungsversuchen nicht behoben ist

---

## H) Stakeholder-Kommunikation

### Sprint-Summary

Nach Abschluss eines Batches von Tickets (= Sprint) automatisch generieren.
Ablage: `docs/sprints/YYYY-MM-DD-sprint-NNN.md`

Inhalt:
- Welche Tickets wurden abgeschlossen
- Was kann der Nutzer jetzt tun (aus User-Facing CHANGELOG)
- Was ist der naechste geplante Schritt
- Offene Blocker (falls vorhanden)

### Release Notes

Werden aus `CHANGELOG.md [User-Facing]` + abgeschlossenen Ticket-Titeln generiert. Kein Entwickler-Jargon. Ablage: `docs/releases/vX.Y.md`.

### Roadmap-Update

Wird nach jedem Sprint oder auf Jakobs Anfrage automatisch aktualisiert. Der Agent verschiebt Tickets von `Next` nach `Now` wenn sie in Arbeit sind, von `Now` nach abgeschlossen wenn `done`.

---

## I) Governance-Log

`docs/governance_log.md` — alle autonomen Entscheidungen des Agenten.

### Format eines Eintrags

```markdown
## YYYY-MM-DD — [Kurzbeschreibung der Entscheidung]

**Ticket:** TICKET-NNN (oder "kein Ticket")
**Entscheidung:** Was wurde entschieden?
**Begruendung:** Warum? Welche Alternativen wurden verworfen?
**Betroffene Dateien:** Liste der geaenderten/erstellten Dateien
**ADR:** ADR-NNN (falls relevant, sonst "keins")
**Review:** ausstehend
```

Wenn Jakob eine Entscheidung bestaetigt: `**Review:** bestaetigt YYYY-MM-DD` eintragen.

### Was immer ins Governance-Log kommt

- Jede neue ADR-Erstellung
- Jede Abweichung von der bestehenden Architektur
- Jede Aenderung an `PROJECT_SPEC.md`
- Jede Entscheidung zwischen zwei technischen Alternativen (auch kleine)
- Jede Installation neuer Abhaengigkeiten (packages, libraries)
- Jeder Verifier-Pass (Kurzfassung, Link auf den vollen Report)

---

## J) Parallelisierung (Git Worktrees)

### Default: sequenziell

Tickets werden **standardmaessig sequenziell** abgearbeitet. Parallelisierung ist
ein bewusster Ausnahmefall, kein Default.

### Erlaubt: max. 2-3 Worktrees, nur bei disjunkten Datei-Sets

Praxis-Erfahrungswert (Recherche 2026-05-21): 4-8 parallele Worktrees sind die
empirische Obergrenze pro Entwickler, **darueber wird Review zum Engpass**.
Fuer Jakobs 1-Person-Setup ist die Schwelle bei **2-3 parallel** — sonst
ueberlaeuft die manuelle PO-Abnahme.

### Pflicht-Check vor Parallelisierung

Bevor zwei Tickets parallel gestartet werden, pruefen:

1. Welche Files beruehrt jedes Ticket (aus dem `Code-Referenzen`-Block)?
2. Gibt es ueberlappende Files? Besonders kritisch:
   - `db/models.py` (Schema-Aenderungen)
   - `api/main.py` (Endpoint-Aenderungen)
   - `frontend/app/`-Routen
   - `CLAUDE.md`, `docs/PROJECT_SPEC.md`, `ROADMAP.md`
3. Bei Ueberlapp → **sequenziell**, keine Parallelisierung.
4. Bei disjunkten Sets → Parallelisierung erlaubt.

### Mechanik: Git Worktrees

```bash
git worktree add ../<projekt>-feat-NNN feat/TICKET-NNN
cd ../<projekt>-feat-NNN
claude
```

Pro Worktree eine eigene Session. Merge erfolgt sequenziell am Ende.

### SQLite-spezifisch

Bei SQLite-Projekten (z.B. Immobewertung): **pro Worktree eine eigene DB-Datei**
via `DATABASE_URL`-ENV — sonst konkurrieren beide Sessions um die gleiche
`data/immo.db`.

### Konventionen bei parallelen Branches

- **Spec-Aenderungen** (`PROJECT_SPEC.md`, `CLAUDE.md`, `ROADMAP.md`) duerfen
  **nur im Hauptbranch** passieren. Parallele Tickets schreiben ausschliesslich
  ihre eigenen Files + ihr Ticket.
- **Verifier-Pass pro Branch** — der Verifier laeuft im jeweiligen Worktree, vor
  dem Merge.
- Bei Merge-Konflikten auf gemeinsamen Files: das auseinandergelaufene Ticket
  wird zurueck auf sequenziell gezogen, nicht heimlich gemergt.

### Wann ein Orchestrator-Claude lohnt

Faustregel aus der Recherche: erst ab > 5 offenen Tickets gleichzeitig.
Vorher ueberwiegt der Coordination-Overhead. Pattern: Lead-Claude (Opus) plant +
delegiert, 3-5 Worker-Claudes (Sonnet) arbeiten an disjunkten Datei-Sets, Lead
mergt am Ende.

---

## K) inbox/-Konvention (menschliches Eingangs-Material)

Material, das **nicht** ueber den Standard-Spec-Weg (Chat mit Claude) reinkommt
— Screenshots, PDFs, weitergeleitete Mails, Notizen, Sprachnachrichten — bekommt
einen festen Ablageort, **bevor** daraus ein formelles Ticket entsteht. So geht
es nicht im Chat-Backlog verloren und ist beim Spec-Prozess auffindbar.

### Ablageort: pro Workflow/Projekt

`inbox/` liegt **pro Workflow- bzw. Projekt-Verzeichnis**, nicht zentral —
sonst vermischt sich Spec-Material aus mehreren Workflows. Beispiele:

```
workflows/prod/bewerbung-bot/inbox/   ← Material fuer diesen Workflow
docs/inbox/                           ← oder auf Projekt-Root-Ebene
```

Die Konvention gilt fuer **alle** agile-sdd-Projekte — inklusive `skill_dev`
selbst (dort z.B. `skill_dev/inbox/` fuer Skill-Ideen-Material).

### Struktur

```
inbox/
├── .gitkeep                ← haelt den Ordner im Repo
├── <material>              ← eingehendes Material (NICHT committet, siehe .gitignore)
└── archive/
    └── .gitkeep            ← verarbeitetes Material nach `done`
```

### .gitignore (Default — sensibles Material nicht committen)

Inbox-Material kann sensibel sein (Screenshots mit Kundendaten, private
Sprachnachrichten). Default ist daher: **Inhalt ignorieren, nur Ordner-Struktur
tracken.** Beim Projekt-Setup in `.gitignore` ergaenzen:

```gitignore
# inbox: menschliches Eingangs-Material (nicht committen, ausser .gitkeep)
inbox/*
!inbox/.gitkeep
inbox/archive/*
!inbox/archive/.gitkeep
```

Will ein Projekt bewusst unkritisches Material mit-versionieren, kann es die
Regel pro Projekt lockern — der **Default ist ignorieren**.

### Bootstrap-Hinweis (passiv)

Beim Agent-Bootstrap (Sektion A, Punkt 10) prueft der Agent, ob `inbox/`-Ordner
unverarbeitetes Material enthalten (alles ausser `.gitkeep` und `archive/`).
Falls ja: **passiver Hinweis**, z.B. *"3 Files in `workflows/prod/x/inbox/`
warten auf Spec-Verarbeitung."* Der Agent fragt **nicht** aktiv nach, ob jetzt
gespec't werden soll, und blockiert nicht — er macht das Material nur sichtbar.

### Welche Formate der Agent liest

Der Agent verarbeitet nur, was er **nativ** lesen kann: PNG/JPG (Read-Tool als
Bild), PDF, Text/Markdown. **Keine Auto-Transkription von Audio** (OGG/MP3) —
das ist bewusst ausgeklammert (haelt den Scope schlank). Liegen Audio-Files in
`inbox/`, weist der Agent passiv darauf hin und bittet den User um eine
Text-Zusammenfassung; eine Whisper-/Transkriptions-Integration ist ggf. ein
separater Skill, nicht Teil von agile-sdd.

### Ticket-Verknuepfung: `inbox_source:`

Entsteht ein Ticket aus Inbox-Material, traegt der Implementer im Ticket-
Frontmatter das optionale Feld `inbox_source:` mit dem Datei-Pfad ein
(Audit-Trail "wo kam die Anforderung her"):

```yaml
inbox_source: workflows/prod/bewerbung-bot/inbox/anforderungen_janina.png
```

### Nach `done`: archivieren

Geht das aus dem Material entstandene Ticket auf `done`, verschiebt der
Implementer das verarbeitete Material nach `inbox/archive/` (Nachvollziehbarkeit
— gleicher Geist wie `KNOWN_FAILURES_archive.md`: Lern-Material bleibt, wird
nicht geloescht). Default ist **archivieren, nicht loeschen**.

---

## L) Default-Entscheidungs-Regel (statt Rueckfrage)

> [!important] „Mein meistgenutzter Move ist 'rueckfragen, was er empfehlen wuerde'." (Jakob, 2026-06-18)
>
> Rueckfragen sind Reibung, nicht Service. Der Agent **entscheidet selbst
> und dokumentiert**, wo immer er es verantworten kann — er fragt nur, wo
> die STOPP-Liste es verlangt. Dieses Prinzip ergaenzt Sektion 0
> (Governance-Grundregel "Kein Fix ohne Ticket und Code") — Ticket-/Code-
> Pflicht bleibt; was sich aendert ist die Entscheidungs-Schwelle, ob
> vorher zurueckgefragt wird.

### L.1 MUST-Regel: Agent entscheidet selbst, wenn ALLE Punkte zutreffen

Der Agent **entscheidet eigenstaendig und dokumentiert die Entscheidung im
`docs/governance_log.md`** (Format Sektion I, `Review: ausstehend`), wenn
alle folgenden Punkte zutreffen:

1. **Reversibel** — Code-Aenderung, additives Schema, neue Datei, neue
   Konfig-Default-Wert. Kein irreversibler Datenverlust, kein
   History-Rewrite.
2. **Kein externer Kosten-Trigger** — keine bezahlte API wird neu
   angesprochen, keine Cloud-Ressource erzeugt, keine kostenpflichtige
   Dependency installiert.
3. **Keine Outbound-Kommunikation an Dritte** — keine Mail, keine
   WhatsApp/Trello/Webhook-Schreibvorgaenge nach aussen.
4. **Vision-konform ableitbar** — entweder deckt ein Prinzip in
   `docs/PROJECT_VISION.md` die Entscheidung, oder die Frage ist operativ
   neutral (z.B. Default-Wert fuer Pagination, Format einer Log-Zeile,
   Datei-Namens-Konvention).
5. **Keine Vermischung mit Architektur** — Architektur-Entscheidungen
   (neuer Service, neue DB, Tech-Stack-Wechsel) brauchen IMMER ein ADR +
   Rueckfrage, nie eine stille autonome Setzung.

Sind alle Punkte erfuellt: **entscheiden, dokumentieren, weiterarbeiten**.
Nicht fragen.

### L.2 Hartes STOPP — Agent fragt IMMER zuerst

Diese sechs Faelle ueberstimmen L.1 immer. Bei JEDEM Treffer wird vor der
Aktion zurueckgefragt:

1. **Destruktive Operationen** — `DROP`, `DELETE`, `rm -rf`, Force-Push,
   History-Rewrite, Branch-Loeschungen, irreversibles Aufraeumen.
2. **Outbound-Kommunikation an Dritte** — Mail/WhatsApp/Trello-Schreiben/
   Webhook-Call an externe Empfaenger. (Lesen ist OK, Schreiben braucht
   Bestaetigung.)
3. **Neue bezahlte Dependencies** — API-Key-Setup, Cloud-Resourcen-Erzeugung,
   Subscription-Aktivierung.
4. **Vision-relevante Architektur** — neuer Service, neue DB, Tech-Stack-
   Wechsel, neue ADR. Architektur ist nie autonom.
5. **Verifikations-Fehler** — siehe `feedback_workflow_hard_failure`:
   wenn ein vorgelagerter Schritt nicht eindeutig erfolgreich war,
   STOPPEN. Niemals durch eine autonome Entscheidung "drueber weg".
6. **Direkte DB-Mutation ohne reproduzierbares Skript** — `UPDATE`/`cancel`/
   Status-Setzen aus der Konsole. Greift Sektion 0: zuerst Ticket + Skript,
   dann anwenden.

### L.3 Dokumentations-Pflicht

Jede autonom getroffene Entscheidung nach L.1 bekommt einen Eintrag in
`docs/governance_log.md` mit:

- Datum + Kurzbeschreibung
- Ticket-Referenz (oder "kein Ticket — operativ neutral")
- Begruendung, welcher L.1-Punkt warum erfuellt war
- Liste betroffener Dateien
- `Review: ausstehend` (Jakob reviewt asynchron, nicht synchron)

So bleibt jede Entscheidung **auffindbar**, ohne dass sie den Flow
unterbricht.

### L.4 Anti-Pattern (verboten)

- "Soll ich X oder Y machen?" wenn beide reversibel + vision-konform sind →
  Agent entscheidet selbst (L.1).
- "Magst du das so?" nach einer reversiblen Default-Setzung → ueberfluessig,
  governance_log reicht.
- Stille Mutation OHNE governance_log-Eintrag → verletzt L.3 und Sektion 0.

### L.5 Verweis auf 2-Wochen-Plan

Voice-Mode-Detection und Vision-Drift-Counter (Bestaetigungsfragen pro
Session zaehlen, `/po-reconcile` empfehlen) sind aktuell OUT-OF-SCOPE. Sie
werden in ca. 2 Wochen separat als SKILL-Tickets evaluiert. Sourcedoku:
`skill_dev/proposals/2026-06-18_sdd_default_decision_plus_voice_mode.md`
(Vorschlaege 3 + 4).

---

## M) Antwort-Pattern „Empfehlungs-First"

> [!important] Empfehlungs-First statt Optionen-Liste
>
> Bei jeder echten Wahlsituation, in der eine Rueckfrage doch noetig ist
> (Sektion L.2 greift, oder die Vision deckt die Frage wirklich nicht ab),
> **liefert der Agent zuerst eine klare Empfehlung mit Begruendung und
> Trade-off** — nicht eine neutrale 3-Option-Tabelle, die der User wieder
> bewerten soll.

### M.1 Pflicht-Format

```
Empfehlung: <eine Zeile, klare Aktion>
Warum: <2-3 Saetze Begruendung, Bezug zu Vision-Prinzip / Memory / Live-Beleg>
Trade-off: <1 Satz: was du dafuer aufgibst>
[optional, nur auf Nachfrage] Alternativen: A | B | C
```

Konkretes Beispiel (gut):

```
Empfehlung: Migrate die DB-Datei jetzt mit additivem ALTER TABLE.
Warum: TICKET-NNN braucht das Feld, ALTER ist reversibel + vision-konform
  (Prinzip "additive Schema-Aenderungen"). Memory feedback_api_schema_pflicht
  greift — Endpoints werden im selben Commit erweitert.
Trade-off: 1 zusaetzlicher Deploy-Schritt fuer Bestands-DB; akzeptabel.
```

Konkretes Anti-Beispiel (verboten als Default):

```
Es gibt drei Optionen fuer die DB-Migration:
1. ALTER TABLE additiv
2. Neue Tabelle + View
3. JSON-Spalte als Beifang
Welche bevorzugst du?
```

### M.2 Anti-Pattern (explizit verboten als Default-Output)

- **3-Option-Tabellen ohne Empfehlung.** Tabellen sind erlaubt **nach** der
  Empfehlung als optionale Vertiefung — nie als Default-Output.
- **"Welche bevorzugst du?"-Fragen** ohne dass eine Empfehlung vorausging.
- **"Soll ich X oder Y?"-Auswahl** — der Agent waehlt, der User korrigiert
  bei Bedarf.
- **Neutrale Listen** ("hier sind ein paar Ideen, was meinst du?") ohne
  klare Wertung.

### M.3 Selbst-Check (Skill-Regel)

Vor dem Senden: **Wenn die geplante Antwort > 2 gleichgewichtete Optionen
enthaelt, ohne dass eine empfohlen ist → Antwort umschreiben.** Empfehlung
zuerst, Alternativen nur auf Nachfrage.

### M.4 Verhaeltnis zu Sektion L

- Wenn L.1 greift: gar nicht erst fragen — entscheiden + governance_log.
- Wenn L.2 (STOPP) greift: fragen, aber im Format M.1 (Empfehlungs-First).
- Wenn unklar ist, ob L.1 oder L.2 greift: M.1-Format + STOPP-Reflex
  bevorzugen (Sicherheits-Default).

### M.5 Verweis auf 2-Wochen-Plan

Antwort-Profil-Differenzierung nach Voice-/Text-Mode (Vorschlag 3 der
Sourcedoku) ist aktuell OUT-OF-SCOPE und wird in ca. 2 Wochen evaluiert.

---

## Templates-Referenz

| Template | Pfad | Verwenden fuer |
|---|---|---|
| Ticket | `templates/TICKET.md` | Neues Ticket anlegen |
| ADR | `templates/ADR.md` | Neue Architektur-Entscheidung |
| PROJECT_SPEC | `templates/PROJECT_SPEC.md` | Initiales Spec-Dokument |
| ROADMAP | `templates/ROADMAP.md` | Roadmap neu anlegen |
| CHANGELOG | `templates/CHANGELOG.md` | CHANGELOG initialisieren |
| Sprint Summary | `templates/SPRINT_SUMMARY.md` | Sprint abschliessen |
| Runbook | `templates/RUNBOOK.md` | Service-Runbook anlegen |
| Verify-Report | `templates/verify-report.md` | Output-Schema des Verifier-Subagents (Pflicht-Format) |
| Traceability-Matrix | `templates/TRACEABILITY.md` | Requirement→Test→Code→Verify-Matrix (SKILL-017, F.7) |
| SDD-Config (Beispiel) | `templates/sdd-config.yaml.example` | Vorlage fuer `docs/sdd-config.yaml` pro Projekt |
| Implementer-Briefing-Standards | `templates/IMPLEMENTER_BRIEFING_STANDARDS.md` | Wiederverwendbare Pflicht-Bloecke (API-Schema-Mitdenken, Hygiene, Skill-Code-Pfad) fuer jeden Implementer-Subagent-Prompt |

Verifier-Subagent: `verifier/VERIFIER.md` (Aufgabenbeschreibung) +
`verifier/verifier-prompt.md` (System-Prompt). Slash-Command:
`commands/sdd-verify.md`.

Templates liegen im Skill-Verzeichnis: `~\.claude\skills\agile-sdd-skill\templates\`

---

## Aktivierung in Projekt-CLAUDE.md

Folgende Zeilen in die CLAUDE.md des Projekts einfuegen um den Skill zu aktivieren:

```markdown
## Skill: Agile SDD
Aktiv. Bootstrap-Sequenz: CLAUDE.md → docs/PROJECT_SPEC.md → docs/adr/ → docs/tickets/ → ROADMAP.md → CHANGELOG.md → docs/governance_log.md → Verify-Status (review-Tickets ohne Report?) → Parallelisierungs-Check
Tickets: docs/tickets/TICKET-NNN.md | ADRs: docs/adr/ADR-NNN-titel.md | Governance: docs/governance_log.md
Verifier: docs/tickets/verify/TICKET-NNN-verify-YYYY-MM-DD.md (Pflicht-Pass vor `done`, Aufruf: `/sdd-verify TICKET-NNN`)
SDD-Config: docs/sdd-config.yaml (test_command, health_check, ticket_path, verify_report_path, manual_verify_required: ui_only|true|false, approach_block_required_for_ML: false)
Doku-Artefakte (lebend): docs/TRACEABILITY.md (Req→Test→Code→Verify, done-Hook, SKILL-017) | Ticket-Bloecke: ## Loesungs-Skizze (M/L/XL, SKILL-019) + ## Spec-Delta (bei Spec-Touch, SKILL-018)
KI-Autonomie: voll — alle Entscheidungen ins Governance-Log, Jakob reviewed asynchron. PO-Abnahme: Klick-Anleitung im Verify-Report nur fuer UI-EARS (Default `ui_only`), Jakob setzt `po_acceptance: confirmed|rejected|not_required`. Backend-EARS = automatisch via Verifier-Output.
```

---

## Checkliste: Neues Projekt aufsetzen

1. `docs/` Verzeichnisstruktur anlegen (`tickets/`, `tickets/verify/`, `adr/`, `runbooks/`, `sprints/`, `releases/`, `developer_notes/`)
2. `docs/PROJECT_SPEC.md` aus Template anlegen und befuellen
3. `docs/sdd-config.yaml` aus `templates/sdd-config.yaml.example` ableiten (Pflicht-Felder anpassen: `test_command`, `health_check`, `ticket_path`, `verify_report_path`; `manual_verify_required: ui_only` als Default — `true` fuer rein UI-getriebene Projekte, `false` nur fuer headless Worker-Projekte ohne Frontend)
4. `CHANGELOG.md` aus Template anlegen
5. `ROADMAP.md` aus Template anlegen
6. `docs/governance_log.md` anlegen (leer)
7. `tests/` Ordner anlegen mit `conftest.py` + mindestens 1 Smoke-Test
   (importiert die App und assertet, dass sie laedt). Ohne `tests/` kann der
   Verifier-Pass nie laufen.
8. `pyproject.toml` (oder `requirements-dev.txt`) um `pytest` ergaenzen, falls
   noch nicht enthalten.
9. `CLAUDE.md` mit Skill-Aktivierungs-Block aktualisieren (inkl. Verifier- und
   SDD-Config-Zeile, siehe Beispiel oben).
10. **`inbox/`-Ordner anlegen** (pro Workflow-/Projekt-Verzeichnis) mit
    `inbox/.gitkeep`. In `.gitignore` ergaenzen, damit eingehendes Material
    nicht versehentlich committet wird (sensible Screenshots/Sprachnachrichten):
    ```gitignore
    # inbox: menschliches Eingangs-Material (nicht committen, ausser .gitkeep)
    inbox/*
    !inbox/.gitkeep
    inbox/archive/*
    !inbox/archive/.gitkeep
    ```
    Details + Konvention: Sektion **K**.
11. Erste Tickets aus bekannten Anforderungen anlegen.
