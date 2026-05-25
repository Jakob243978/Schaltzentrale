---
description: Backlog priorisieren — alle idea-Tickets nach RICE-Score sortieren
arg-hint: (optional) --top N | --include-spec
---

Du priorisierst den Backlog des aktuellen Projekts nach RICE-Score.

## Argumente

- Default: alle Tickets mit `Status: idea`
- `--top N` — nur die Top-N anzeigen
- `--include-spec` — auch Tickets mit `Status: spec` mit aufnehmen
  (noch nicht in `in_progress`)

## Ablauf

### Schritt 1: Kontext laden

- `docs/PROJECT_VISION.md` (fuer Prinzip-Lookups)
- `docs/po-config.yaml` (fuer `rice_effort_mapping`, `moscow_default`)
- Alle Ticket-Files in `docs/tickets/` mit passendem Status

### Schritt 2: Pro Ticket extrahieren

Aus Frontmatter:
- `Status`
- `MoSCoW` (Must|Should|Could|Wont)
- `Geschaetzter Aufwand` (XS|S|M|L|XL)
- `vision_principle` (falls gesetzt)
- `outcome_metric` (falls gesetzt)
- `Reach`, `Impact`, `Confidence` (optional)

### Schritt 3: RICE-Score berechnen

```
score = (Reach * Impact * Confidence) / Effort
```

- `Effort` aus `rice_effort_mapping` (XS=1, S=2, M=3, L=5, XL=8).
- Wenn `Reach/Impact/Confidence` fehlen:
  - **Wenn `moscow_default` definiert ist:** Fallback-Werte verwenden, im
    Output mit `(default)` markieren.
  - **Wenn auch das fehlt:** Score = `?`, im Output mit `?` markieren,
    den User fragen ob er ergaenzen will. **Niemals raten.**

### Schritt 4: Vision-Prinzip-Check

Fuer jedes Ticket:
- Hat es `vision_principle:` im Frontmatter? Existiert das Prinzip in
  `PROJECT_VISION.md`?
- Wenn nein: Output-Marker `[no-vision]` — Empfehlung im Bericht:
  *"Vor Implementation `/po-challenge` empfohlen."*

### Schritt 5: Ranking + Tabelle

Markdown-Tabelle, absteigend nach `score`:

```
| # | Ticket | Titel | Score | Reach | Impact | Conf | Effort | Vision-Prinzip | Notiz |
|---|--------|-------|-------|-------|--------|------|--------|----------------|-------|
| 1 | T078 | XYZ | 12.4 | 8 | 8 | 0.7 | 3 | banking-realitaet-vor-wunsch | — |
| 2 | T080 | ABC | 5.6 (default) | 5? | 6? | 0.6? | 5 | [no-vision] | /po-challenge empfohlen |
```

### Schritt 6: Pro Top-3 eine 1-Satz-Begruendung

```
**#1 T078** — Hoher Score weil Vision-Prinzip
`banking-realitaet-vor-wunsch` direkt adressiert + Effort gering (M=3).
**#2 T080** — Mittlerer Score, aber `[no-vision]` — challenge vorher.
**#3 T075** — ...
```

### Schritt 7: Empfehlungen

- Welche Tickets sollten als naechstes in `in_progress`?
- Gibt es Tickets mit `[no-vision]`, die zuerst challenged werden sollten?
- Sind WIP-Limits beachtet? (Max 2-3 parallel laut SDD-Skill J.)

## Was du NICHT tust

- Tickets selbst auf `in_progress` setzen — nur Empfehlung
- Reach/Impact/Confidence raten ohne den User zu fragen
- Vision-Prinzip vorschlagen (das ist `/po-challenge`-Job)
