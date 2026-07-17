---
id: SKILL-072
title: "Grundregel: Specen impliziert Umsetzen; Mensch-Interface = Anforderungen + Tests"
status: done
created: 2026-07-14
origin: jakob
related: [SKILL-018, SKILL-019]
---

# SKILL-072: Specen impliziert Umsetzen; Mensch reviewt ueber Anforderungen + Tests

## Was soll erreicht werden? (Business-Ziel)

Jakob (2026-07-14): Der Agent ist zu oft in „Ticket schreiben / specen und auf
Freigabe warten" verfallen, statt umzusetzen. Das kostet den (nicht-technischen)
PO viel Zeit („dir sagen, dass du es umsetzen sollst") und zwingt ihn, technische
Details mental zu rekonstruieren, die er gar nicht fassen kann. Ziel: Der Agent
setzt gespecte Tickets um und sichert sie ueber Tests ab; der Mensch wird nur
ueber Anforderungen (EARS) und Akzeptanz (Tests) eingebunden, nie ueber technische
Implementierungs-Details.

## Akzeptanzkriterien (EARS-Format)

- EARS-1: Wenn ein Ticket gespect ist, DANN setzt der Agent es um und bringt den
  Verifier/die Tests auf gruen, statt bei `spec` zu stoppen und auf Freigabe zu
  warten.
- EARS-2: Der Agent stellt dem Menschen KEINE technischen Detail-Rueckfragen;
  technische Wie-Entscheidungen trifft er autonom und macht sie ueber Tests
  ueberpruefbar.
- EARS-3: Wenn eine Entscheidung wirklich beim Menschen liegt, DANN formuliert der
  Agent sie als Anforderung/Outcome (Was + Akzeptanz), nicht als technisches Wie.
- EARS-4: Der Agent haelt NUR inne bei explizitem Stopp, schwer-reversiblem
  Aussen-Risiko (Prod-Deploy/Geld/Kunden-Daten nach aussen) oder echter
  Menschen-Entscheidung (Prioritaet/Produkt/Budget).

## Loesungs-Skizze (Approach)

Grundregel-Erweiterung in `SKILL.md` Abschnitt 0 (Governance-Grundregel), direkt
neben „Kein Fix ohne Ticket und Code": ein Callout „Specen impliziert Umsetzen".
Kein neuer Workflow, nur eine verbindliche Haltung, die die bestehenden
Bausteine (EARS-Akzeptanz, Verifier-Pass vor `done`) zum Mensch-Interface macht.

## Spec-Delta

Neu: Section 0 traegt jetzt die Regel „Specen impliziert Umsetzen; Mensch-Interface
= Anforderungen + Tests, keine technischen Detail-Rueckfragen". Bestehende
Ticket-/Verifier-Mechanik unveraendert (sie ist das Absicherungs-Mittel).

## Ergebnis / Notizen

Umgesetzt: `SKILL.md` Abschnitt 0 um den Callout erweitert. Deployment via
`setup.ps1` (robocopy /MIR) nach `~/.claude/skills/`. Als Nutzer-Feedback zusaetzlich
in Memory `feedback_umsetzen_statt_specen` gesichert. Verifikation (Doc-Skill,
manual_verify_required:false): Dogfood — der Agent wendet die Regel ab sofort an.
