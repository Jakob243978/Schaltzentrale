---
ticket: TICKET-NNN
verify_date: YYYY-MM-DD
verify_status: pass | fail | partial
ears_total: 0
ears_passed: 0
ears_failed: 0
ears_partial: 0
ears_ui_count: 0          # Anzahl EARS-Saetze klassifiziert als UI (PO-Test noetig)
ears_backend_count: 0     # Anzahl EARS-Saetze klassifiziert als Backend (Verifier reicht)
tests_passed: 0
tests_failed: 0
implementer_session_ref: optional/commit-sha
# --- Cost-Tracking (Pflicht ab v0.4, siehe SKILL.md F.6) ---
# Trend-Analysen sind NUR innerhalb desselben verifier_model gueltig.
# Bei Modellwechsel: Tickets getrennt gruppieren, nicht direkt vergleichen.
tokens_in_total: 0           # input + cache_creation + cache_read summiert
tokens_out_total: 0          # output
cache_hit_rate: 0.0          # cache_read / (cache_read + cache_creation + input_raw)
cost_usd: 0.0                # USD via Modell-Preise zur Run-Zeit
verifier_model: claude-sonnet-4 | claude-opus-4-7
# Standard (nicht Pflicht): implementer_iterations, implementer_tokens_in, implementer_tokens_out
# implementer_iterations: 1
# implementer_tokens_in: 0
# implementer_tokens_out: 0
# implementer_model: claude-sonnet-4  # nur falls vom verifier_model verschieden
# po_acceptance:
#   pending      = wartet auf Jakobs Klick-Test (mind. 1 UI-EARS vorhanden)
#   confirmed    = Jakob hat geklickt, alles ok
#   rejected     = Jakob hat geklickt, etwas stimmt nicht (siehe PO-Notiz)
#   not_required = ausschliesslich Backend-EARS — Verifier-Output reicht
po_acceptance: pending | not_required
po_acceptance_steps: |
  - Schritt 1
  - Schritt 2
po_acceptance_date: ""
po_acceptance_note: ""
---

# Verify-Report TICKET-NNN

## Zusammenfassung

[2-3 Saetze: Hauptaussage des Verifier-Passes. pass/partial/fail. Was funktioniert,
was fehlt. Empfehlung: Status `done` setzen / Ticket nachschaerfen / Tests erweitern.]

## EARS-Kriterien Pruefung

### EARS-1: When ..., the system shall ...

- **Typ:** ui | backend  (UI = PO-Klick-Test noetig, Backend = Verifier reicht)
- **Status:** pass | fail | partial  (UI-EARS max. `partial` bis `po_acceptance: confirmed`)
- **Implementierung gefunden:** `path/to/file.py:42-58`
- **Test gefunden:** `tests/test_xy.py::test_ears_1` (oder "nicht gefunden")
- **Test-Ergebnis:** passed | failed | not_run | not_found
- **Edge-Cases gepruft:** [Liste konkret, oder "keine zusaetzlichen Cases noetig"]
- **Anmerkung:** [optional, nur bei partial/fail — was fehlt konkret]

### EARS-2: ...

(weitere EARS-Saetze im gleichen Schema)

## Test-Output (Auszug)

```
$ <test_command aus sdd-config.yaml>
[relevante Auszuege, KEINE 200-Zeilen-Dumps — Fokus auf passed/failed-Summary
und relevante Failures]
```

## Health-Check (Auszug, falls definiert)

```
$ <health_check aus sdd-config.yaml>
[Output]
```

## Manuelle PO-Abnahme

**Erforderlich:** ja (mind. 1 UI-EARS) | nein (nur Backend-EARS)

> Wenn ausschliesslich Backend-EARS: nur diesen Block stehen lassen, kein
> Klick-Pfad noetig.
>
> ```
> Keine UI-EARS in diesem Ticket — automatische Abnahme via Verifier-Output.
> Frontmatter: po_acceptance: not_required.
> ```

### Was Jakob konkret tun soll (nur fuer UI-EARS)

1. **URL/Klick-Pfad:**
   ```
   http://localhost:3000/property/2 — Inline-Status-Dropdown klicken,
   Tooltip auf Quelle-Icon hovern, Spalte XY pruefen
   ```
2. **Erwartetes sichtbares Verhalten (pro UI-EARS-Satz):**
   - EARS-1 [ui] → ["Dropdown reagiert + Status wird gespeichert"]
   - EARS-3 [ui] → ["Tooltip zeigt 'Quelle: ImmoScout' beim Hover"]
3. **Backend-EARS (zur Info, schon vom Verifier abgenommen):**
   - EARS-2 [backend] → siehe Test-Output (`tests/test_xy.py::test_ears_2 passed`)
4. **Pass/Fail-Markierung:** Frontmatter-Feld `po_acceptance` von `pending` auf
   `confirmed` (alle UI-EARS passen) oder `rejected` (etwas stimmt nicht) setzen.
   `po_acceptance_date` auf heute setzen. `po_acceptance_note` mit kurzer Notiz
   befuellen (z.B. "Alles wie erwartet" oder "EARS-3 Tooltip erscheint nicht").

### PO-Notiz (Jakob fuellt nach Pruefung)

[leer lassen — wird von Jakob nach der manuellen Abnahme befuellt]

## Empfehlungen / Offene Punkte

- [ ] [konkrete Empfehlung 1 — z.B. "Edge-Case fuer leere Property-ID nicht abgedeckt, Test ergaenzen"]
- [ ] [konkrete Empfehlung 2 — z.B. "EARS-3 ist zu unscharf formuliert, Ticket nachschaerfen"]

## Verifier-Metadaten

- **Verifier-Modell:** [aus Frontmatter `verifier_model`]
- **Tokens in/out:** [aus Frontmatter `tokens_in_total` / `tokens_out_total`]
- **Cache-Hit-Rate:** [aus Frontmatter `cache_hit_rate`]
- **Kosten (USD):** [aus Frontmatter `cost_usd`]
- **Lauf-Datum:** [aus Frontmatter `verify_date`]
- **Implementer-Iterationen (optional):** [aus Frontmatter `implementer_iterations`, falls befuellt]

> Cost-Tracking ist NUR innerhalb desselben `verifier_model` vergleichbar.
> Siehe SKILL.md F.6 (Modell-Gruppierung als Pflicht-Regel).
