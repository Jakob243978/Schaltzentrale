---
id: SKILL-073
title: "Implementer-Default: Subagent im Hintergrund (Parallelisierung)"
status: done
created: 2026-07-15
origin: jakob
related: [SKILL-003, SKILL-072]
---

# SKILL-073: Implementer-Default = Subagent im Hintergrund

## Was soll erreicht werden? (Business-Ziel)

Jakob (2026-07-15): Tickets sollen GRUNDSAETZLICH zuerst als Subagent-Umsetzung
im Hintergrund versucht werden (run_in_background), weil das Parallelisierung
zulaesst und die Durchlaufzeit senkt. Der Hauptagent bleibt Koordinator statt
selbst sequenziell jedes Ticket abzuarbeiten. Heute (2026-07-15) wurde das
Muster 4x praktisch erprobt, inklusive der Konfliktregel fuer geteilte Dateien.

## Akzeptanzkriterien (EARS-Format)

- [x] EARS-1: WENN ein gespectes Ticket zur Umsetzung ansteht, SOLL der Agent
  die Umsetzung zuerst als Subagent im Hintergrund (run_in_background)
  versuchen, statt sie default-maessig selbst im Vordergrund abzuarbeiten.
- [x] EARS-2: WENN ein Ticket per Subagent umgesetzt wird, SOLL der Hauptagent
  als Koordinator agieren: Briefing nach IMPLEMENTER_BRIEFING_STANDARDS,
  Datei-Set-Disjunktheit nach Sektion J pruefen, Ergebnisse einsammeln und den
  Verify-Pass anstossen.
- [x] EARS-3: FALLS eine der definierten Ausnahmen greift (Hello-/op-/ssh-
  gegatete Schritte, Prod-Deploys, ueberlappende Datei-Sets zu laufender
  Arbeit, winzige XS-Edits, Mensch-Interaktion noetig), SOLL der Agent das
  Ticket direkt im Hauptkontext bearbeiten.
- [x] EARS-4: SOLANGE mehrere Subagents parallel laufen, SOLL kein Subagent in
  geteilte Dateien (governance_log, CLAUDE.md, PROJECT_SPEC) schreiben;
  Eintraege liefert der Subagent als Textblock, der Hauptagent appended.

## Loesungs-Skizze (Approach)

- **Gewaehlter Ansatz:** Neue Untersektion "Implementer-Default: Subagent im
  Hintergrund (SKILL-073)" in SKILL.md Sektion B, direkt nach den
  Implementer-Briefing-Standards (dort ist der Subagent-Spawn schon
  definiert). Querverweis in Sektion J (Parallelisierung), damit der
  Worktree-Default "sequenziell" und der neue Hintergrund-Default sauber
  abgegrenzt sind.
- **Verworfene Alternative(n):** Regel nur in Sektion J zu verankern; verworfen,
  weil J die schwergewichtige Worktree-Parallelisierung beschreibt, waehrend
  der Hintergrund-Subagent der leichtgewichtige Standard-Weg im selben
  Arbeitsverzeichnis ist.
- **Betroffene Module:** `SKILL.md` (Sektion B + Sektion J).

## Technische Hinweise

Praxis-Beleg: 2026-07-15 wurden 4 Tickets parallel per Hintergrund-Subagent
umgesetzt; Konflikte auf geteilten Dateien wurden ueber die Textblock-Regel
(Subagent liefert, Hauptagent appended) vermieden.

## Code-Referenzen

- `SKILL.md` Sektion B: neue Untersektion "Implementer-Default: Subagent im
  Hintergrund (SKILL-073)"
- `SKILL.md` Sektion J: Absatz "Default: sequenziell" um Abgrenzung +
  Querverweis ergaenzt

## Spec-Delta

- **Vorher:** SKILL.md kannte nur den Implementer-Subagent-Spawn (Briefing-
  Standards) und die Worktree-Parallelisierung (Sektion J, Default
  sequenziell). Kein Default, WIE ein einzelnes Ticket umgesetzt wird.
- **Nachher:** Verbindlicher Default: Ticket-Umsetzung zuerst als
  Hintergrund-Subagent; Hauptagent koordiniert. Explizite Ausnahmen-Liste +
  Konfliktregel fuer geteilte Dateien. Sektion J verweist auf den neuen
  Default.
- **Anlass:** Parallelisierung/Durchlaufzeit (Jakob 2026-07-15, 4x erprobt).

## Ergebnis / Notizen

Umgesetzt 2026-07-15: SKILL.md Sektion B um Untersektion "Implementer-Default:
Subagent im Hintergrund (SKILL-073)" erweitert (Default-Regel, Ausnahmen,
Konfliktregel geteilte Dateien), Sektion J um Abgrenzung + Querverweis.
Deployment via `setup.ps1` (robocopy /MIR) nach `~/.claude/skills/`.
Verifikation: Doc-/Methodik-Skill (`manual_verify_required: false`, keine
pytest-Suite laut CLAUDE.md/sdd-config): kein Verifier-Setup fuer
Doku-Tickets, Abnahme via Review + Dogfood in konsumierenden Projekten.
