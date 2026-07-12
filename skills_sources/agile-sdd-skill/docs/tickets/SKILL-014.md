---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: rueckfragen_pro_session_unter_3
outcome_review_at: null
ui_verify_urls: []
api_endpoints_extended: n/a
status: spec
moscow: Must
effort: S
affects: alle Projekte (Skill ist global)
related_memorys:
  - feedback_einfach_abarbeiten
  - feedback_skeleton_first
  - feedback_style
  - feedback_user_beobachtung_vorrang
  - feedback_workflow_hard_failure
---

# SKILL-014: Default-Entscheidung + Empfehlungs-First in agile-sdd-skill

**Status:** spec
**Erstellt:** 2026-06-18
**MoSCoW:** Must
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`
**Affects:** alle Projekte, die `agile-sdd-skill` aktiviert haben (Skill ist global)

## Trigger-Live-Erfahrung

Jakob 2026-06-18:

> "Mein meistgenutzter Move ist 'rueckfragen, was er empfehlen wuerde'. Ich
> fuehl mich entscheidungshemmt."

Der Skill behandelt heute fast jede Verzweigung als entscheidungspflichtig
und liefert haeufig 3-Option-Listen ohne klare Empfehlung. Das erzeugt
unnoetige Reibung, obwohl viele Entscheidungen aus Vision + Memory
ableitbar oder reversibel sind. Memory-Belege:

- `feedback_einfach_abarbeiten.md`: *"Ja warum fragst du mich das immer?
  Einfach abarbeiten!"* — Rueckfrage als Reibung, nicht als Service.
- `feedback_skeleton_first.md`: *"keine Folge-Tasks/Tickets eroeffnen und
  keinen Push zu 'lass uns das direkt im Anschluss machen'"*.
- `feedback_style.md`: *"Antworten kurz und direkt. Keine langen
  Erklaerungen, direkt zur Sache."* — etablierter Default, der praktisch
  zu selten greift.
- `feedback_user_beobachtung_vorrang.md`: *"Default fuer die Default-Wahl
  ist 'X folgen'"* — Pattern existiert, aber nur fuer User-Beobachtungen.
- `feedback_workflow_hard_failure.md`: *"Bei Verifikations-Fehler
  STOPPEN"* — harter STOPP-Anker.

Sourcedoku: `Schaltzentrale\skill_dev\proposals\2026-06-18_sdd_default_decision_plus_voice_mode.md`.
Jakob hat Vorschlaege 1+2 (Default-Entscheidung + Empfehlungs-First) zur
sofortigen Umsetzung freigegeben. Vorschlaege 3 (Voice-Mode) und 4
(Vision-Drift-Counter) werden in 2 Wochen evaluiert (Out-of-Scope dieses
Tickets, siehe unten).

## Was soll erreicht werden? (Business-Ziel)

Der `agile-sdd-skill` bekommt zwei neue Pflicht-Sektionen, die das
Antwort-Verhalten und die Entscheidungs-Schwelle des Agenten verbindlich
schaerfen:

1. **Default-Entscheidung-Regel (Sektion L):** Bei reversiblen,
   nicht-kommunikativen, vision-konformen Aenderungen entscheidet der
   Agent selbst und dokumentiert im `governance_log.md`. Eine harte
   STOPP-Liste definiert, wann er IMMER fragen MUSS.
2. **Empfehlungs-First-Pattern (Sektion M):** Bei echten Wahlsituationen
   liefert der Agent zuerst eine klare Empfehlung mit Begruendung +
   Trade-off. 3-Option-Tabellen ohne Empfehlung sind als Default-Output
   verboten.

Konsequenz fuer Jakob: weniger Rueckfragen pro Session, klare
Verantwortungs-Uebernahme durch den Agenten, transparente Doku der
autonomen Entscheidungen.

## Akzeptanzkriterien (EARS-Format)

- [ ] When `skills_sources/agile-sdd-skill/SKILL.md` gelesen wird, the
      system shall eine neue Sektion **L "Default-Entscheidungs-Regel"**
      mit klar formulierter MUST-Regel enthalten: Reversibel + kein
      externer Kosten-Trigger + keine Outbound-Kommunikation +
      vision-konform ableitbar + keine Architektur-Vermischung -> Agent
      entscheidet selbst, dokumentiert im `governance_log.md`.
- [ ] When Sektion L beschrieben wird, the system shall eine explizite
      sechs-Punkte-STOPP-Liste enthalten, in der der Agent IMMER zuerst
      fragt: (1) destruktive Ops, (2) Outbound-Kommunikation, (3) neue
      bezahlte Dependencies, (4) vision-relevante Architektur, (5)
      Verifikations-Fehler, (6) direkte DB-Mutation ohne reproduzierbares
      Skript.
- [ ] When Sektion L greift, the system shall die Dokumentations-Pflicht
      verlangen: jede autonom getroffene Entscheidung als
      `governance_log`-Eintrag mit `Review: ausstehend` (Konsistenz mit
      Sektion I).
- [ ] When `skills_sources/agile-sdd-skill/SKILL.md` gelesen wird, the
      system shall eine neue Sektion **M "Empfehlungs-First-Antwort-Pattern"**
      enthalten, die das Pflicht-Format vorschreibt: `Empfehlung: <eine
      Zeile>` + `Warum: <2-3 Saetze>` + `Trade-off: <1 Satz>` + optional
      `Alternativen` nur auf Nachfrage.
- [ ] When Sektion M Anti-Pattern beschreibt, the system shall explizit
      3-Option-Tabellen ohne Empfehlung sowie "Welche bevorzugst du?"-
      Fragen und "Soll ich X oder Y?"-Auswahl als Default-Output verbieten.
      Tabellen sind nur **nach** der Empfehlung als optionale Vertiefung
      erlaubt.
- [ ] When Sektion M Selbst-Check beschreibt, the system shall die Regel
      enthalten: wenn die geplante Antwort > 2 gleichgewichtete Optionen
      enthaelt ohne Empfehlung -> Antwort umschreiben.
- [ ] When beide Sektionen am Ende einen Verweis brauchen, the system shall
      auf Vorschlaege 3 (Voice-Mode) + 4 (Drift-Counter) als
      2-Wochen-Plan-Out-of-Scope referenzieren — Pfad zur Sourcedoku
      `skill_dev/proposals/2026-06-18_sdd_default_decision_plus_voice_mode.md`.

## Technische Hinweise

- Skill-Code-Aenderung: `skills_sources/agile-sdd-skill/SKILL.md` —
  additive neue Sektionen **L** und **M** nach Sektion K (inbox/-Konvention),
  vor "Templates-Referenz". Append-only/additiv — nichts Bestehendes
  verfaelschen.
- Sprach-Stil: knapp, Imperativ, MUST/SHOULD/MAY analog zu Sektion 0
  (Governance-Grundregel) und Sektion K.
- Skill-Version-Bump: `0.5` → `0.6` (Frontmatter `version:`).
- Backup vor Patch: `SKILL.md.bak_2026-06-18` im selben Verzeichnis (bereits
  vor Implementierung angelegt).
- Kein neues Datenmodell, keine API-Aenderung (`api_endpoints_extended: n/a`).
- Deployment via `setup.ps1` (robocopy /MIR) nach `~/.claude/skills/`.
- Idempotenz: Wenn `## L)` oder `## M)` bereits in SKILL.md existiert,
  NICHT doppeln — im Implementer-Bericht melden.

## Code-Referenzen

- `skills_sources/agile-sdd-skill/SKILL.md` (neue Sektionen L + M)
- `skills_sources/agile-sdd-skill/SKILL.md.bak_2026-06-18` (Backup)
- `skill_dev/CHANGELOG.md` (Eintrag)
- `skill_dev/docs/governance_log.md` (Eintrag)
- `vault/Memory/feedback_default_decision_empfehlung_first.md` (neue
  Feedback-Memory)
- `vault/Memory/MEMORY.md` (Index-Eintrag)
- Sourcedoku: `skill_dev/proposals/2026-06-18_sdd_default_decision_plus_voice_mode.md`

## Out of Scope (2-Wochen-Plan)

- **Vorschlag 3 (Voice-Mode-Awareness):** Wird in ca. 2 Wochen separat
  als SKILL-Ticket evaluiert. Aktuell zu experimentell, Marker-Detection
  noch unklar (`[voice]`-Hint vs `default_mode`-Eintrag).
- **Vorschlag 4 (Vision-Drift-Counter):** Wird in ca. 2 Wochen separat
  evaluiert (PO-Skill C.5, Bestaetigungsfragen zaehlen, ggf.
  `docs/sdd-session-meta.json`). Sektion C.5 wird im **po-skill** parallel
  als Begleit-Ticket SKILL-015 jetzt schon **ohne** den
  Bestaetigungs-Counter angelegt — nur die Empfehlungs-First-Schaerfung
  fuer `/po-challenge`.

## Verknuepfte Tickets

- **Begleit-Ticket:** SKILL-015 (po-skill C.5 — Empfehlungs-First in
  `/po-challenge`)
- **Sourcedoku:** `skill_dev/proposals/2026-06-18_sdd_default_decision_plus_voice_mode.md`

## Ergebnis / Notizen

_(wird vom Implementer beim Abschliessen befuellt)_
