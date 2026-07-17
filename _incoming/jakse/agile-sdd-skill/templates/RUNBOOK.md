# Runbook: [Service-Name]

**Projekt:** [Projektname]
**Letzte Aktualisierung:** YYYY-MM-DD

---

## Was macht dieser Service?

<!-- Ein Satz: Zweck und Rolle im Gesamtsystem. -->

---

## Starten / Stoppen

```bash
# Starten
[Befehl]

# Stoppen
[Befehl]

# Status pruefen
[Befehl]
```

---

## Gesundheits-Check

<!-- Wie erkenne ich ob der Service laeuft und korrekt funktioniert? -->

```bash
[Check-Befehl oder URL]
```

Erwartetes Ergebnis: `...`

---

## Bekannte Fehlermuster und Recovery

### Fehler: [Fehlermuster / Log-Zeile]

**Ursache:** ...

**Loesung:**
```bash
[Recovery-Befehl]
```

**Wenn das nicht hilft:** [Jakob informieren / eskalieren]

---

### Fehler: [Zweites Fehlermuster]

**Ursache:** ...

**Loesung:** ...

---

## Logs

```
# Wo liegen die Logs?
[Pfad oder Befehl]
```

Relevante Log-Level: `ERROR:` und `WARN:` immer beachten.

---

## Abhaengigkeiten

<!-- Was muss laufen damit dieser Service funktioniert? -->

- [Service/API] — [Rolle]
