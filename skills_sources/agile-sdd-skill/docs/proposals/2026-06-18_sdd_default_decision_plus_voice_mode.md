---
title: SDD-Skill-Schaerfung — Default-Entscheidung + Voice-Mode-Awareness
type: proposal
status: vorschlag
created: 2026-06-18
target_skills:
  - agile-sdd-skill (primaer)
  - po-skill (sekundaer)
  - global CLAUDE.md (Hinweis)
related_memorys:
  - feedback_einfach_abarbeiten
  - feedback_skeleton_first
  - feedback_style
  - feedback_user_beobachtung_vorrang
  - feedback_workflow_hard_failure
tags:
  - skill-dev
  - proposal
  - communication-style
---

# Vorschlag — Default-Entscheidung statt Rueckfrage, plus Voice-Mode-Awareness

## Diagnose

Jakob fuehlt sich aktuell unter **Entscheidungshemmung** wegen zu vieler Detail-Rueckfragen ("rueckfragen, was er empfehlen wuerde" ist sein meistgenutzter Move). Der Skill behandelt heute fast jede Verzweigung als entscheidungspflichtig, obwohl viele davon aus der Vision ableitbar oder reversibel sind. Wenn der Skill nicht ableiten kann, ist das in Wahrheit ein **Vision-Schaerfungs-Signal**, kein Frage-Trigger. Zusatzlast: Voice-Mode bekommt heute gleich lange Antworten wie Text-Mode — beim Sprechen entsteht so eine doppelte Reibung.

## Memory-Belege

- `vault/Memory/feedback_einfach_abarbeiten.md` Z.10/12: *"Ja warum fragst du mich das immer? Einfach abarebiten!"* — Rueckfrage als Reibung, nicht als Service.
- `vault/Memory/feedback_skeleton_first.md` Z.10: *"keine Folge-Tasks/Tickets eroeffnen und keinen Push zu 'lass uns das direkt im Anschluss machen'"* — Skill darf nicht aktiv weiterschieben.
- `vault/Memory/feedback_style.md` Z.16/22: *"Antworten kurz und direkt. Keine langen Erklaerungen, direkt zur Sache."* — bereits etablierter Default, der praktisch zu selten greift.
- `vault/Memory/feedback_user_beobachtung_vorrang.md` Z.14: *"Default fuer die Default-Wahl ist 'X folgen'"* — Pattern fuer Default-Entscheidung mit transparenter Begruendung existiert bereits, aber nur fuer User-Beobachtungen.
- `vault/Memory/feedback_workflow_hard_failure.md` Z.20: *"Bei mehrstufigen Workflows ... wenn ein Schritt nicht eindeutig erfolgreich war, darf der Workflow NICHT als erfolgreich weitergehen"* — definiert das harte STOPP-Kriterium (Verifikationsfehler), das die Default-Entscheidung niemals ueberstimmen darf.

## Vorschlag 1 — Default-Entscheidung-Pattern (in `agile-sdd-skill/SKILL.md`, neue Sektion **L**)

**Regel:** Der Skill **entscheidet selbst und dokumentiert** im `governance_log.md`, wenn ALLE folgenden Punkte zutreffen:

- Reversibel (Code-Aenderung, additives Schema, neue Datei).
- Kein externer Kosten-Trigger (keine bezahlte API, kein Cloud-Resource-Aufruf).
- Kein Kommunikations-Effekt nach aussen (keine Mail, kein WhatsApp, kein Trello-Schreibvorgang, kein Webhook an Dritte).
- Vision-konform ableitbar (entweder ein Prinzip in `PROJECT_VISION.md` deckt es, oder es ist operativ neutral).
- Keine Vermischung mit Architektur (Architektur-Entscheidungen kommen IMMER als ADR + Rueckfrage).

**Hartes STOPP — Skill fragt IMMER:**
1. Destruktive Operationen (`DROP`, `DELETE`, `rm -rf`, Force-Push, History-Rewrite).
2. Outbound-Kommunikation an Dritte (Mail/WhatsApp/Trello/Webhook).
3. Neue bezahlte Dependencies (API-Key-Setup, Cloud-Ressourcen).
4. Vision-relevante Architektur (neuer Service, neue DB, Tech-Stack-Wechsel).
5. Verifikations-Fehler (siehe `feedback_workflow_hard_failure`).
6. Direkte DB-Mutation ohne reproduzierbares Skript (siehe SKILL Sektion 0).

**Dokumentations-Pflicht:** Jede autonom getroffene Entscheidung bekommt einen `governance_log`-Eintrag mit `Review: ausstehend` — Jakob reviewt asynchron, nicht synchron.

## Vorschlag 2 — Empfehlungs-First statt Optionen-Liste (neue Sektion **M**)

**Antwort-Pattern bei jeder echten Wahlsituation:**

```
Empfehlung: <eine Zeile, klare Aktion>
Warum: <2-3 Saetze Begruendung, Bezug zu Vision-Prinzip oder Memory>
Trade-off: <1 Satz: was du dafuer aufgibst>
[optional, nur auf Nachfrage] Alternativen: A | B | C
```

**Anti-Pattern (explizit verboten als Default):** 3-Option-Tabellen ohne Empfehlung, "Welche bevorzugst du?"-Fragen, "Soll ich X oder Y?"-Auswahl. Tabellen sind erlaubt **nach** Empfehlung als optionale Vertiefung, nie als Default-Output.

**Selbst-Check (Skill-Regel):** Wenn die geplante Antwort > 2 gleichgewichtete Optionen enthaelt, ohne dass eine empfohlen wird → Antwort umschreiben.

## Vorschlag 3 — Voice-Mode-Awareness (neue Sektion **N**, ggf. global)

**Detection (welcher Marker funktioniert in Claude Code heute realistisch):**
1. Primaer: User-Prompt enthaelt expliziten Hint `[voice]` / `[stt]` / "ich diktiere gerade".
2. Sekundaer: Prompt hat STT-Charakteristik — keine Codeblocks, keine genauen Datei-Pfade, hohe Konversations-Dichte, < 50 Wort-Stoerwoerter ("aehm", "also").
3. Tertiar: User-Eintrag in `~/.claude/CLAUDE.md` setzt Default-Modus (z.B. `default_mode: voice`).

**Antwort-Profil Voice-Mode:**
- Max 3-5 Saetze, keine Listen mit > 3 Bullets.
- Kein Code, keine Datei-Pfade in voller Laenge ("die Skill-Datei" reicht).
- Eine Empfehlung, ein Why, kein Trade-off.
- Fallback bei Komplexitaet: *"Das beantworte ich dir im Text-Mode ausfuehrlicher — kurze Antwort jetzt: X."*

**Antwort-Profil Text-Mode:**
- Empfehlungs-First-Pattern aus Vorschlag 2 weiterhin Pflicht.
- Tabellen + Code OK, aber nur als Vertiefung nach der Empfehlung.

## Vorschlag 4 — Vision-Drift-Erkennung (Erweiterung `po-skill` Sektion C)

**Trigger:** Wenn der Skill in einer Session zum **3. Mal** "ich brauche deine Bestaetigung" / "wie soll ich entscheiden?" sagt, gibt er stattdessen aus:

```
Hinweis: Das ist die 3. Bestaetigungsfrage in dieser Session.
Vermutung: Die Vision deckt diesen Bereich nicht eindeutig.
Empfehlung: /po-reconcile vor weiterem Implementieren — Vision schaerfen statt weiter zurueckfragen.
```

**Bootstrap-Hook (im `agile-sdd-skill` A.4 Bootstrap):** Wenn `docs/po-config.yaml` existiert, Datum des letzten `/po-reconcile`-Eintrags in `PROJECT_VISION.md` Aktualisiert-Log lesen. Wenn > 30 Tage alt UND in der vorherigen Session > 2 Bestaetigungsfragen geloggt wurden → Hinweis im Bootstrap-Output.

(Das setzt voraus, dass der Skill Bestaetigungsfragen zaehlt — kann via einfachem Marker in `docs/sdd-session-meta.json` passieren, optionaler Add-on.)

## Implementations-Aufwand

| Bereich | Datei | Aufwand |
|---|---|---|
| Default-Entscheidung-Pattern | `Schaltzentrale/skills_sources/agile-sdd-skill/SKILL.md` (neue Sektion L) | ~30 Min |
| Empfehlungs-First-Pattern | `Schaltzentrale/skills_sources/agile-sdd-skill/SKILL.md` (neue Sektion M) | ~20 Min |
| Voice-Mode-Awareness | `Schaltzentrale/skills_sources/agile-sdd-skill/SKILL.md` (neue Sektion N) + ggf. `~/.claude/CLAUDE.md` Hinweis | ~30 Min |
| Vision-Drift-Erkennung | `Schaltzentrale/skills_sources/po-skill/SKILL.md` (C.5 + Bootstrap-Hook) | ~30 Min |
| Memory-Eintrag | Neue `feedback_default_entscheidung_plus_voice.md` als Querverweis | ~10 Min |
| Deploy | `Schaltzentrale/setup.ps1` einmal laufen lassen | trivial |

**Risiko:** Skills sind global. Vorschlag 1 (Default-Entscheidung) sollte konservativ starten — STOPP-Liste lieber zu lang als zu kurz, im Zweifel weiter fragen. Vorschlag 3 (Voice-Mode) ist die experimentellste Komponente — sollte als opt-in markiert sein, bis 1-2 Wochen Erfahrung da sind.

## Offen fuer Jakob

1. **Voice-Mode-Detection:** Bevorzugst du einen expliziten Marker (`[voice]` im Prompt) oder einen Default-Mode-Eintrag in `~/.claude/CLAUDE.md`? Marker ist deterministischer, Default ist bequemer.
2. **Default-Entscheidung-Scope:** Reicht "reversibel + kein externer Effekt + Vision-konform" als Freibrief, oder willst du eine zusaetzliche Begrenzung pro Projekt (z.B. nur in nicht-prod-Projekten)?
3. **Vision-Drift-Counter:** OK mit zusaetzlichem `docs/sdd-session-meta.json` pro Projekt, oder lieber leichter Session-Marker ueber Implementer-Bootstrap-Output (ohne neue Datei)?
4. **Rollout:** Alle 4 Vorschlaege auf einen Schlag, oder erst Vorschlag 1+2 (sicherster Wert), dann 3+4 nach 2 Wochen Praxis?
