---
name: agile-sdd
description: Agile Spec-Driven Development mit KI-Agenten. Aktivieren wenn ein Agent eigenstaendig Software-Features implementieren soll — Ticket-Erstellung, Spec-First-Entwicklung, ADRs, Living Documentation, Governance-Log. Verwende diesen Skill wenn der User Features implementieren, Tickets bearbeiten, Architektur-Entscheidungen treffen oder den Projekt-Status aktualisieren will.
---

# Agile Spec-Driven Development Skill

Dieser Skill steuert wie ein KI-Agent selbstaendig Software-Projekte entwickelt. Der Business-Owner (Jakob) schreibt keine Zeile Code — er beschreibt Anforderungen, der Agent erledigt alles andere und dokumentiert alle Entscheidungen nachvollziehbar.

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

Wenn eine Datei nicht existiert: weiter zur naechsten. Nicht stoppen, nicht nachfragen.

Wenn `docs/PROJECT_SPEC.md` fehlt: als allererste Aktion vor jeder anderen Arbeit anlegen (Vorlage: `templates/PROJECT_SPEC.md`).

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

## Was soll erreicht werden? (Business-Ziel)
<!-- In einem Satz: Wer profitiert wie davon? -->

## Akzeptanzkriterien (EARS-Format)
<!-- "When [Bedingung], the system shall [Aktion]." -->
- [ ] When ..., the system shall ...
- [ ] When ..., the system shall ...

## Technische Hinweise
<!-- Nur wenn relevant: Pfade, APIs, Abhaengigkeiten, Risiken -->

## Code-Referenzen
<!-- Dateien/Funktionen die betroffen sind -->

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
- **review**: Implementierung fertig, Tests gruen, wartet auf Jakob-Abnahme (optional)
- **done**: Abgenommen, CHANGELOG aktualisiert, Code-Kommentare gesetzt

Tickets wechseln niemals zurueck von `done` zu einem anderen Status. Korrekturen erzeugen ein neues Ticket.

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

---

## C) Spec-First-Workflow

Vor dem Schreiben von neuem Code:

1. Pruefen ob `docs/PROJECT_SPEC.md` existiert und aktuell ist.
2. Wenn neue Architektur-Entscheidung noetig: ADR anlegen (Abschnitt D).
3. Ticket auf Status `spec` setzen und alle Akzeptanzkriterien vollstaendig formulieren.
4. Erst dann mit Implementierung beginnen.

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

Die Spec wird **waehrend** der Implementierung aktualisiert, nie nachtraeglich in einer separaten Session.

---

## D) Architecture Decision Records (ADR)

Format: MADR (Markdown Any Decision Records) — schlankes Format, listet Alternativen explizit.

Ablage: `docs/adr/ADR-NNN-kurztitel.md` (dreistellig, Kebab-Case-Titel).

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
- [TICKET-NNN] ...

### User-Facing
- Was der Nutzer jetzt tun kann / was sich verbessert hat
- Keine technischen Details, keine Dateinamen
```

Wird nach jedem abgeschlossenen Ticket (Status `done`) aktualisiert. Nicht gesammelt am Ende.

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

### docs/developer_notes/

Freies Format. Technische Notizen die nicht in CHANGELOG passen: Debugging-Erkenntnisse, Temporaere Workarounds, Tooling-Eigenheiten. Dateiname: `YYYY-MM-DD-thema.md`.

---

## F) Test- und Qualitaetsstrategie

### Was immer getestet wird

- **Happy Path**: Der Normalfall laut Akzeptanzkriterium
- **Kritischer Edge Case**: Der gefaehrlichste Sonderfall (leere Eingabe, ungueltige ID, fehlende Daten)

### Was nicht getestet wird

- UI-Details (Farben, Abstands-Pixel, Icon-Auswahl)
- Cosmetic Changes (Umbenennung von Labels die keine Logik aendern)
- Dokumentations-Aenderungen

### Test-Protokoll

Der Agent schreibt Tests gleichzeitig mit dem Code (nicht nachtraeglich). Nach Fertigstellung:

1. Tests ausfuehren
2. Ergebnis ins Ticket-Feld "Ergebnis / Notizen" eintragen: `Tests: N passed, M failed`
3. Bei Failures: Ursache diagnostizieren und beheben bevor Status auf `done` gesetzt wird

Akzeptanzkriterien im Ticket sind die direkte Testbasis: EARS-Satz → Test-Fall.

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

Templates liegen im Skill-Verzeichnis: `~\.claude\skills\agile-sdd-skill\templates\`

---

## Aktivierung in Projekt-CLAUDE.md

Folgende Zeilen in die CLAUDE.md des Projekts einfuegen um den Skill zu aktivieren:

```markdown
## Skill: Agile SDD
Aktiv. Bootstrap-Sequenz: CLAUDE.md → docs/PROJECT_SPEC.md → docs/adr/ → docs/tickets/ → ROADMAP.md → CHANGELOG.md → docs/governance_log.md
Tickets: docs/tickets/TICKET-NNN.md | ADRs: docs/adr/ADR-NNN-titel.md | Governance: docs/governance_log.md
KI-Autonomie: voll — alle Entscheidungen ins Governance-Log, Jakob reviewed asynchron.
```

---

## Checkliste: Neues Projekt aufsetzen

1. `docs/` Verzeichnisstruktur anlegen (tickets/, adr/, runbooks/, sprints/, releases/, developer_notes/)
2. `docs/PROJECT_SPEC.md` aus Template anlegen und befuellen
3. `CHANGELOG.md` aus Template anlegen
4. `ROADMAP.md` aus Template anlegen
5. `docs/governance_log.md` anlegen (leer)
6. `CLAUDE.md` mit Skill-Aktivierungs-Block aktualisieren
7. Erste Tickets aus bekannten Anforderungen anlegen
