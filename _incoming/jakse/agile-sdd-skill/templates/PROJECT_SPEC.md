# PROJECT_SPEC.md — [Projektname]

**Letzte Aktualisierung:** YYYY-MM-DD
**Anlass der letzten Aenderung:** ...

---

## Systemzweck

<!-- Ein Absatz: Was loest dieses System? Fuer wen? Was waere ohne es schlechter? -->

## Architektur-Ueberblick

<!-- Hauptkomponenten und wie sie zusammenhaengen. ASCII-Diagramm oder Stichpunkte. -->

```
[Komponente A] --> [Komponente B] --> [Datenbank]
       |
       v
[Externer Dienst]
```

## Tech-Stack

| Schicht | Technologie | Begruendung |
|---|---|---|
| Frontend | ... | ... |
| Backend/API | ... | ... |
| Datenbank | ... | ... |
| Hosting | ... | ... |
| Externe Dienste | ... | ... |

## Datenmodell (Kern-Entities)

<!-- Nur die wichtigsten Entities. Kein vollstaendiges Schema — das liegt im Code. -->

### [Entity A]
- `id`: ...
- `feld_1`: ...

### [Entity B]
- `id`: ...
- `feld_1`: ...

## Externe Abhaengigkeiten

| Dienst | Zweck | Credentials-Ort |
|---|---|---|
| ... | ... | .env |

## Bekannte Constraints

<!-- Was ist gesetzt und darf nicht geaendert werden? Deployment-Einschraenkungen, Compliance, etc. -->

- ...

## Start / Betrieb

```
# Entwicklung starten
[Befehl]

# Tests ausfuehren
[Befehl]
```
