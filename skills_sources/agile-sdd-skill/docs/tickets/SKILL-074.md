---
id: SKILL-074
title: "EARS-Saetze auf Deutsch (Bug: englisch/deutscher Mischmasch)"
status: done
created: 2026-07-15
origin: jakob
related: [SKILL-072]
---

# SKILL-074: EARS-Saetze auf Deutsch

## Was soll erreicht werden? (Business-Ziel)

SKILL.md und die Templates definieren EARS englisch ("When [Bedingung], the
system shall [Aktion]"), die realen Tickets sind aber laengst deutsch und
mischen shall/SOLL/When/Wenn. Der nicht-technische PO (Jakob) soll
Akzeptanzkriterien in EINEM konsistenten deutschen Schema lesen und schreiben
koennen; der Verifier muss trotzdem Bestands-Tickets mit englischen Saetzen
weiter matchen (append-only-Historie, kein Massen-Rewrite).

## Akzeptanzkriterien (EARS-Format)

- [x] EARS-1: WENN ein neues Ticket angelegt wird, SOLL das Template und die
  SKILL.md-Definition das deutsche EARS-Schema vorgeben:
  "WENN <Ausloeser/Bedingung>, SOLL <System> <Verhalten>."
- [x] EARS-2: Das System SOLL die fuenf EARS-Varianten deutsch dokumentieren
  (Ubiquitous "Das System SOLL...", Event "WENN..., SOLL...", State
  "SOLANGE..., SOLL...", Unwanted "FALLS..., SOLL...", Optional "WO...").
- [x] EARS-3: WENN der Verifier EARS-Saetze in einem Ticket matcht, SOLL er
  beide Formen akzeptieren (deutsches Schema UND englisches
  Bestands-Schema "When ..., the system shall ...").
- [x] EARS-4: Das System SOLL bestehende Projekt-Tickets NICHT umschreiben
  (append-only-Historie); nur neue Tickets folgen dem deutschen Schema.

## Loesungs-Skizze (Approach)

- **Gewaehlter Ansatz:** Deutsches EARS-Schema als Definition + Beispiele in
  SKILL.md (Ticket-Format in Sektion B, plus neue Untersektion mit den fuenf
  Varianten und Bestandsschutz-Regel), templates/TICKET.md und
  templates/verify-report.md angepasst; Verifier-Doku (VERIFIER.md +
  verifier-prompt.md) um Matching-Hinweis "beide Formen akzeptieren" ergaenzt.
- **Verworfene Alternative(n):** Massen-Rewrite aller Bestands-Tickets auf das
  deutsche Schema; verworfen wegen append-only-Historie und weil der Verifier
  beide Formen problemlos matchen kann.
- **Betroffene Module:** `SKILL.md`, `templates/TICKET.md`,
  `templates/verify-report.md`, `verifier/VERIFIER.md`,
  `verifier/verifier-prompt.md`.

## Technische Hinweise

RESEARCH.md dokumentiert weiterhin die englische EARS-Original-Notation als
Recherche-Quelle; Recherche-Dokumente sind Historie und werden nicht angefasst.

## Code-Referenzen

- `SKILL.md` Sektion B: Ticket-Format-Block (Akzeptanzkriterien) + neue
  Untersektion "EARS-Schema auf Deutsch (SKILL-074)"
- `templates/TICKET.md`: Akzeptanzkriterien-Block
- `templates/verify-report.md`: EARS-Beispielzeile
- `verifier/VERIFIER.md`: Pruefungs-Algorithmus, Matching-Satz
- `verifier/verifier-prompt.md`: Schritt "Pruefen", Matching-Hinweis

## Spec-Delta

- **Vorher:** EARS-Definition + alle Beispiele englisch ("When [Bedingung],
  the system shall [Aktion]."), reale Tickets deutsch: Mischmasch.
- **Nachher:** Verbindliches deutsches Schema "WENN <Ausloeser/Bedingung>,
  SOLL <System> <Verhalten>." inkl. der fuenf EARS-Varianten; Verifier
  akzeptiert Bestands-Tickets mit englischen Saetzen weiterhin.
- **Anlass:** Konsistenz fuer den nicht-technischen PO, Bug-Report Jakob
  2026-07-15.

## Ergebnis / Notizen

Umgesetzt 2026-07-15: SKILL.md (Ticket-Format-Beispiele deutsch + Untersektion
"EARS-Schema auf Deutsch" mit den fuenf Varianten und Bestandsschutz),
templates/TICKET.md und templates/verify-report.md auf das deutsche Schema
umgestellt, verifier/VERIFIER.md + verifier/verifier-prompt.md um den
Matching-Hinweis (beide Formen akzeptieren, kein Massen-Rewrite) ergaenzt.
Bestehende Projekt-Tickets unveraendert. Deployment via `setup.ps1`
(robocopy /MIR) nach `~/.claude/skills/`. Verifikation: Doc-/Methodik-Skill
(`manual_verify_required: false`, keine pytest-Suite): kein Verifier-Setup
fuer Doku-Tickets, Abnahme via Review + Dogfood in konsumierenden Projekten.
