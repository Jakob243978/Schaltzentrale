---
description: Pruefe 14 Tage nach done-Ticket ob das Outcome-Metric tatsaechlich beruehrt wurde
arg-hint: TICKET-NNN | --all-due
---

Du fuehrst eine Outcome-Verifikation auf einem oder mehreren `done`-Tickets aus.

## Argumente

- `/po-verify-outcome TICKET-NNN` — explizit ein Ticket
- `/po-verify-outcome --all-due` — alle Tickets mit `outcome_review_at <=
  heute` und kein vorhandener Outcome-Eintrag

## Ablauf

### Schritt 1: Ticket(s) auswaehlen

- Bei `TICKET-NNN`: lade direkt.
- Bei `--all-due`: scanne `docs/tickets/*.md` nach Status `done` +
  Frontmatter `outcome_review_at`, das <= heute ist UND kein Eintrag in
  `docs/po-outcomes.md` mit `TICKET-NNN` existiert.

### Schritt 2: Outcome-Metric extrahieren

Aus Ticket-Frontmatter `outcome_metric: <metric_id>` lesen. Wenn das Feld
fehlt:
- Den User fragen: *"Ticket hat kein `outcome_metric`. Welche Metrik aus
  `PROJECT_VISION.md` `Outcome-Metriken` sollte ich pruefen?"*
- Wenn keine Antwort: in `docs/po-outcomes.md` markieren als
  `not_measurable` und naechstes Ticket.

### Schritt 3: Metrik gegen Quelle pruefen

Je nach Metrik-Typ:

| Metrik-Typ | Vorgehen |
|---|---|
| **DB-Counter** (z.B. `banking_match_per_month`) | SQL gegen `data/immo.db` (oder Projekt-spezifische DB), Wert "heute - 30 Tage" vs. "Baseline vor Ticket-Done" |
| **Log-Auswertung** (z.B. `time_to_decision_median`) | Workers-Skript / SQL, Median ueber Zeitraum berechnen |
| **Manuell** (z.B. "User-Zufriedenheit", "Wettbewerbs-Position") | Den User direkt fragen, Antwort notieren |

Wenn die Quelle (DB, Log, Worker) **nicht existiert oder nicht abrufbar
ist**: notiere `not_measurable` mit konkretem Grund (z.B. "SQL-Tabelle
`bank_matches` existiert nicht — Folge-Ticket noetig fuers Tracking"),
NICHT raten.

### Schritt 4: Eintrag in `docs/po-outcomes.md`

Anhaengen:

```markdown
## TICKET-NNN — verify YYYY-MM-DD

**Ticket-Done-Datum:** YYYY-MM-DD
**Metrik:** <metric_id> (aus PROJECT_VISION.md)
**Wert davor (Baseline):** <wert oder "unbekannt — Ticket setzte keinen Baseline-Marker">
**Wert jetzt:** <wert oder "nicht messbar — Grund: ...">
**Beurteilung:** erreicht | nicht erreicht | nicht messbar
**Hypothese-Status:** bestaetigt | widerlegt | offen
**Folge-Aktion:** <z.B. "kein Handlungsbedarf" / "Folge-Ticket T0XX" / "Vision-Prinzip ueberpruefen">
```

### Schritt 5: Eskalation flaggen

Wenn ein `MoSCoW: Must`-Ticket >= 90 Tage nach `done` und Outcome ist
`nicht erreicht`:

→ Gib dem User einen Hinweis:
*"TICKET-NNN war Must-Have, 90 Tage spaeter keine Outcome-Bewegung. In
naechster Retro flaggen? Mogliche Hypothese: ... ist widerlegt — bedarf
Vision-Schaerfung."*

### Schritt 6: Bericht

Zusammenfassung in 5 Zeilen:
- Wie viele Tickets gecheckt
- Wie viele `erreicht` / `nicht erreicht` / `nicht messbar`
- Welche Tickets brauchen Folge-Aktion
- Pfad zu `docs/po-outcomes.md`
- Naechster /po-verify-outcome Run sinnvoll wann?

## Was du NICHT tust

- Neue Tickets fuer Folge-Aktionen anlegen — nur Empfehlung
- Vision aendern
- Metrik-Werte raten wenn Quelle fehlt
