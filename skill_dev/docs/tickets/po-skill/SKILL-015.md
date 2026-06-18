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
  - feedback_style
  - feedback_user_beobachtung_vorrang
related_tickets:
  - SKILL-014
---

# SKILL-015: Empfehlungs-First in po-skill `/po-challenge` (Begleit zu SKILL-014)

**Status:** spec
**Erstellt:** 2026-06-18
**MoSCoW:** Must
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`
**Affects:** alle Projekte, die `po-skill` aktiviert haben (Skill ist global)

## Trigger-Live-Erfahrung

Jakob 2026-06-18 (selbe Session wie SKILL-014):

> "Mein meistgenutzter Move ist 'rueckfragen, was er empfehlen wuerde'. Ich
> fuehl mich entscheidungshemmt."

SKILL-014 schaerft das Antwort-Verhalten **generell** (agile-sdd: Default-
Entscheidung + Empfehlungs-First). Der PO-Skill braucht denselben Patch
spezifisch fuer seinen Challenge-Workflow: heute ist `/po-challenge` ein
3x-Why-Frageprozess **ohne** explizite Empfehlung am Ende. Das verstaerkt
genau das Rueckfrage-Pattern, das Jakob abstellen will — der Challenge
fragt, statt zu empfehlen.

Sourcedoku: `Schaltzentrale\skill_dev\proposals\2026-06-18_sdd_default_decision_plus_voice_mode.md`
(Sektion "Vorschlag 4" — Vision-Drift-Counter ist OUT-OF-SCOPE und wartet
2 Wochen; nur die Empfehlungs-First-Variante fuer C.5 wird jetzt umgesetzt).

## Was soll erreicht werden? (Business-Ziel)

Der `po-skill` bekommt eine neue Sektion **C.5
"Empfehlungs-First in /po-challenge"**, die das Antwort-Schema von
`/po-challenge` an SKILL-014 ausrichtet:

- Nach 3x-Why + Vision-Prinzip-Match liefert `/po-challenge` immer eine
  **klare Empfehlung** (annehmen | parken | ablehnen | Vision schaerfen)
  mit Begruendung und Trade-off — nicht nur Optionen ohne Wertung.
- Der Skill spiegelt damit explizit Sektion M des `agile-sdd-skill`.
- Kein Bestaetigungs-Counter (Vorschlag 4 vollstaendig) — der ist
  Out-of-Scope und wartet 2 Wochen.

Konsequenz fuer Jakob: `/po-challenge` wird zum Empfehlungs-Werkzeug,
nicht zum Frage-Werkzeug.

## Akzeptanzkriterien (EARS-Format)

- [ ] When `skills_sources/po-skill/SKILL.md` gelesen wird, the system
      shall eine neue Sektion **C.5 "Empfehlungs-First in /po-challenge"**
      enthalten, die das Antwort-Schema am Ende eines Challenge-Durchlaufs
      verbindlich festlegt: `Empfehlung: <annehmen | parken bis YYYY-MM-DD
      | ablehnen | Vision schaerfen>` + `Warum: <2-3 Saetze, Bezug zu
      Vision-Prinzip>` + `Trade-off: <1 Satz>`.
- [ ] When Sektion C.5 Anti-Pattern beschreibt, the system shall
      "3x-Why-Antworten ohne abschliessende Empfehlung" und "Soll ich das
      Ticket auf spec setzen?" als Default-Output verbieten — die
      Empfehlung MUSS kommen, der User entscheidet danach.
- [ ] When Sektion C.5 die Beziehung zu SKILL-014 beschreibt, the system
      shall explizit auf `agile-sdd-skill` Sektion M referenzieren
      (Empfehlungs-First-Pattern als Quelle der Konvention).
- [ ] When die STOPP-Faelle aus SKILL-014 Sektion L greifen (akute Bugs,
      Outbound-Kommunikation, vision-relevante Architektur), the system
      shall in Sektion C.5 klarstellen, dass diese im Challenge-Workflow
      die Empfehlung NICHT autonom umsetzen — sie werden empfohlen, aber
      Jakob entscheidet.
- [ ] When Sektion C.5 das Verhaeltnis zur bestehenden Akut-Liste in
      Sektion C beschreibt, the system shall klarstellen, dass die
      Akut-Liste (Bug-Fix, Verifikations-Fehler, Audit-Termin <7 Tage,
      explizit "akut") die Default-Empfehlung "parken bis +48h" auf
      "annehmen sofort" verschiebt — ohne den Cooldown-Schritt zu
      ueberspringen.

## Technische Hinweise

- Skill-Code-Aenderung: `skills_sources/po-skill/SKILL.md` — additive
  neue Sektion **C.5** zwischen Sektion C (Challenge-Workflow) und
  Sektion D (Priorisierung). Append-only/additiv.
- Sprach-Stil: knapp, Imperativ, MUST/SHOULD/MAY analog zur bestehenden
  Sektion C.
- Skill-Version-Bump: `0.1` → `0.2` (Frontmatter `version:`).
- Backup vor Patch: `SKILL.md.bak_2026-06-18` im selben Verzeichnis (bereits
  vor Implementierung angelegt).
- Kein Bestaetigungs-Counter, kein `docs/sdd-session-meta.json` — diese
  Komponenten kommen mit Vorschlag 4 in 2 Wochen als separates Ticket.
- Deployment via `setup.ps1` (robocopy /MIR) nach `~/.claude/skills/`.
- Idempotenz: Wenn `### C.5` bereits in SKILL.md existiert, NICHT
  doppeln — im Implementer-Bericht melden.

## Code-Referenzen

- `skills_sources/po-skill/SKILL.md` (neue Sektion C.5)
- `skills_sources/po-skill/SKILL.md.bak_2026-06-18` (Backup)
- `skill_dev/CHANGELOG.md` (Eintrag)
- `skill_dev/docs/governance_log.md` (Eintrag, gemeinsam mit SKILL-014)
- Quer-Verweis: SKILL-014 (agile-sdd-skill Sektionen L + M)

## Out of Scope (2-Wochen-Plan)

- **Vorschlag 4 vollstaendig (Vision-Drift-Counter):** Bestaetigungs-
  Counter pro Session, Bootstrap-Hook der nach 3 Confirm-Fragen
  `/po-reconcile` empfiehlt, optionales `docs/sdd-session-meta.json`.
  Separates SKILL-Ticket in ca. 2 Wochen.

## Verknuepfte Tickets

- **Begleit-Ticket:** SKILL-014 (agile-sdd-skill Sektionen L + M)
- **Sourcedoku:** `skill_dev/proposals/2026-06-18_sdd_default_decision_plus_voice_mode.md`

## Ergebnis / Notizen

_(wird vom Implementer beim Abschliessen befuellt)_
