# TICKET-NNN: [Kurztitel — max. 60 Zeichen]

**Status:** idea
**Erstellt:** YYYY-MM-DD
**MoSCoW:** [Must | Should | Could | Wont]
**Geschaetzter Aufwand:** [XS | S | M | L | XL]

## Was soll erreicht werden? (Business-Ziel)

<!-- Ein Satz: Wer profitiert wie davon? Kein technisches Detail. -->

## Akzeptanzkriterien (EARS-Format)

<!-- "When [Bedingung], the system shall [Aktion]." — eine Zeile pro Kriterium -->
- [ ] When ..., the system shall ...
- [ ] When ..., the system shall ...

## API-Schema-Kontrakt

<!--
Pflicht-Sektion seit SKILL-010 (2026-06-01). Triggered durch Live-Erfahrung
T103a (Immobewertung): Property-Modell wurde durch T092 um Region-FK +
JSON-Felder erweitert, T101 hat sie befuellt — aber `GET /api/property/{id}`
gab die neuen Felder nie zurueck. Frontend brauchte 2 Calls, Folge-Ticket
musste spontan nachgeschoben werden.

Im Frontmatter zusaetzlich markieren:
  api_endpoints_extended: yes | no | n/a
-->

- [ ] Aendert dieses Ticket ein Datenmodell (`db/models.py` oder analog)?
- [ ] Wenn ja: welche API-Endpoints geben diese neuen Felder zurueck?
- [ ] Wurden alle GET/POST/PATCH-Response-Schemas additiv erweitert (keine Feld-Umbenennung, nur neue Felder — Backwards-Kompat)?
- [ ] Wurde ein OpenAPI-Schema-Check in den Tests verankert (`curl /openapi.json | grep <feldname>` o.Ae.)?

## Technische Hinweise

<!-- Optional. Relevante Pfade, APIs, bekannte Risiken, Abhaengigkeiten zu anderen Tickets. -->

## Code-Referenzen

<!-- Dateien / Funktionen / Tabellen die betroffen sind. Wird beim Implementieren befuellt. -->

## Ergebnis / Notizen

<!-- Vom Agenten beim Abschliessen befuellt: Tests-Ergebnis, tatsaechliche Aenderungen, Abweichungen vom Plan. -->
