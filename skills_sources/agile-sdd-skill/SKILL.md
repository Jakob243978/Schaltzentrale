---
name: agile-sdd
version: 0.4
description: Agile Spec-Driven Development mit KI-Agenten. Aktivieren wenn ein Agent eigenstaendig Software-Features implementieren soll — Ticket-Erstellung, Spec-First-Entwicklung, ADRs, Living Documentation, Governance-Log, EARS-getriebene Verifikation (Verifier-Subagent), Cost-Tracking (Token/USD pro Ticket) und kontrollierte Parallelisierung (Git Worktrees). Verwende diesen Skill wenn der User Features implementieren, Tickets bearbeiten, Architektur-Entscheidungen treffen, einen Verify-Pass starten (`/sdd-verify TICKET-NNN`) oder den Projekt-Status aktualisieren will.
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
- **review**: Implementierung fertig, Tests gruen, Verifier-Pass + (bei UI-EARS) manuelle PO-Abnahme stehen aus
- **done**: Abgenommen, CHANGELOG aktualisiert, Code-Kommentare gesetzt

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
| SDD-Config (Beispiel) | `templates/sdd-config.yaml.example` | Vorlage fuer `docs/sdd-config.yaml` pro Projekt |

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
SDD-Config: docs/sdd-config.yaml (test_command, health_check, ticket_path, verify_report_path, manual_verify_required: ui_only|true|false)
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
10. Erste Tickets aus bekannten Anforderungen anlegen.
