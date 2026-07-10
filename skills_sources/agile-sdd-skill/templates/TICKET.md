# TICKET-NNN: [Kurztitel — max. 60 Zeichen]

**Status:** idea
**Erstellt:** YYYY-MM-DD
**MoSCoW:** [Must | Should | Could | Wont]
**Geschaetzter Aufwand:** [XS | S | M | L | XL]
<!-- inbox_source: optional — Pfad zum inbox/-Material, aus dem dieses Ticket entstand (Audit-Trail). Zeile weglassen wenn kein Inbox-Ursprung. -->

## Was soll erreicht werden? (Business-Ziel)

<!-- Ein Satz: Wer profitiert wie davon? Kein technisches Detail. -->

## Akzeptanzkriterien (EARS-Format)

<!-- "When [Bedingung], the system shall [Aktion]." — eine Zeile pro Kriterium -->
- [ ] When ..., the system shall ...
- [ ] When ..., the system shall ...

## Loesungs-Skizze (Approach)

<!--
SKILL-019 (2026-06-19): Design-Phase light gegen Cognitive Debt.
PFLICHT ab Aufwand M/L/XL, OPTIONAL bei XS/S — bei XS/S diesen Block weglassen.
3-6 Zeilen genuegen. Wird vor Status-Uebergang nach `in_progress` ausgefuellt.

- **Gewaehlter Ansatz:** <wie wird es geloest?>
- **Verworfene Alternative(n):** <was wurde NICHT gewaehlt und warum?>
- **Betroffene Module:** <Dateien/Komponenten — kuendigt die Code-Referenzen an>

Beruehrt der Ansatz eine projektweite Architektur-Weiche → stattdessen ADR-NNN
anlegen und hier nur darauf verweisen (kein Doppel-Dokument).
-->

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

## Spec-Delta

<!--
SKILL-018 (2026-06-19): Brownfield-Nachvollziehbarkeit.
NUR ausfuellen, wenn dieses Ticket PROJECT_SPEC.md (oder eine andere Spec-Datei)
veraendert — sonst diesen Block ganz weglassen (kein leerer Pflicht-Block).

- **Vorher:** <was die Spec bisher aussagte>
- **Nachher:** <was sie jetzt aussagt>
- **Anlass:** <warum die Aenderung noetig war>

Beim Uebergang nach `done` im CHANGELOG ### Technical referenzieren:
`[TICKET-NNN] Spec-Delta: <Kurzfassung>`. Governance-Log-Pflicht
"Aenderung an PROJECT_SPEC.md" bleibt zusaetzlich bestehen.
-->

## Ergebnis / Notizen

<!-- Vom Agenten beim Abschliessen befuellt: Tests-Ergebnis, tatsaechliche Aenderungen, Abweichungen vom Plan. -->
