---
id: SKILL-075
title: "CLAUDE.md als Living-Documentation-Pflege-Ziel (nicht nur Lese-Datei)"
status: done
created: 2026-07-15
origin: jakob
related: [SKILL-017, SKILL-018, SKILL-073]
---

# SKILL-075: CLAUDE.md ist Pflege-Ziel, nicht nur Lese-Datei

## Was soll erreicht werden? (Business-Ziel)

Jakob (2026-07-15): Der SDD-Skill fasst die Projekt-`CLAUDE.md` oft nicht an bzw.
"traut sich nicht" / ist sich nicht bewusst, dass er sie pflegen MUSS, wenn ein
Ticket eine dauerhafte Konvention/Regel etabliert. Folge: Kontext geht zwischen
Sessions verloren, der User muss sich wiederholen, Sachen werden schlechter
umgesetzt.

**Root-Cause (belegt in SKILL.md):** Sektion **A)** listet `CLAUDE.md` nur als
Bootstrap-**Lese**-Datei ("PFLICHT"). Sektion **E) Living Documentation** pflegt
CHANGELOG / ROADMAP / TRACEABILITY / developer_notes — **`CLAUDE.md` fehlt dort
komplett**. Zusaetzlich rahmt die Parallelitaets-Konfliktregel (Sektion B) sie als
"geteilte Datei, vorsichtig", was das proaktive Pflegen eher bremst. Es gibt also
NIRGENDS die Anweisung, dass eine ticket-etablierte Dauer-Regel in die CLAUDE.md
gehoert. Genau diese Luecke fuellt dieses Ticket.

## Akzeptanzkriterien (EARS-Format)

- [x] EARS-1: WENN ein Ticket eine dauerhafte, sessionuebergreifend geltende Regel
  etabliert (neue verbindliche Konvention, verbindlicher Pfad/Command/Gate,
  Gotcha/Known-Failure-Kurzform, Architektur-Weichen-Pointer), SOLL der Skill
  vorgeben, dass ein praegnanter Block **im selben Ticket** in die Projekt-CLAUDE.md
  geschrieben wird (Teil der Definition of Done, wie die CHANGELOG-Zeile).
- [x] EARS-2: Das System SOLL `CLAUDE.md` explizit als Living-Documentation-Ziel in
  Sektion E fuehren (mit Was-gehoert-rein / Was-nicht / Wann-Regel).
- [x] EARS-3: Das System SOLL die Abgrenzung zu DEF-001 (autonomes Auto-Memory,
  geparkt) dokumentieren: ticket-gekoppelt + deterministisch, KEIN Black-Box-
  Selbstschreiben.
- [x] EARS-4: Die Bootstrap-Sektion A SOLL `CLAUDE.md` als Lese- **und** Pflege-Ziel
  kennzeichnen (Verweis auf Sektion E), ohne die restliche Bootstrap-Reihenfolge zu
  aendern.

## Loesungs-Skizze (Approach)

- **Gewaehlter Ansatz:** Neuer Unterabschnitt "### CLAUDE.md (Projekt-Kontext,
  lebend)" als ERSTER Punkt in Sektion E) Living Documentation (Prominenz, da
  Kontext-tragend); Bootstrap-Zeile A.1 um "(Lesen und pflegen -> Sektion E)"
  ergaenzt; Kompakt-Referenz (Doku-Artefakte lebend) um CLAUDE.md erweitert.
- **Verworfene Alternative:** DEF-001 (autonomes Auto-Memory) freigeben — verworfen,
  weil Black-Box-Risiko + Doppel-Mechanismus (bleibt geparkt). Dieses Ticket loest
  das Problem deterministisch/ticket-gekoppelt statt autonom.
- **Betroffene Module:** `SKILL.md` (Sektion A, Sektion E, Kompakt-Referenz).

## Spec-Delta

- **Vorher:** `CLAUDE.md` war reine Bootstrap-Lese-Datei; Sektion E kannte sie nicht;
  keine Regel, wann eine ticket-etablierte Konvention in CLAUDE.md gehoert.
- **Nachher:** `CLAUDE.md` ist explizites Living-Doc-Pflege-Ziel mit Definition-of-
  Done-Kopplung, Was-rein/Was-nicht-Regel und DEF-001-Abgrenzung.
- **Anlass:** Jakob-Beobachtung 2026-07-15 (Kontextverlust, Wiederholungen).

## Ergebnis / Notizen

Umgesetzt 2026-07-15: SKILL.md Sektion E um "### CLAUDE.md (Projekt-Kontext, lebend)"
erweitert (Pflege-Pflicht, Was-rein/Was-nicht, Wann=Definition of Done, DEF-001-
Abgrenzung); Bootstrap A.1 + Kompakt-Referenz ergaenzt. Deployment via `setup.ps1`
(robocopy /MIR) nach `~/.claude/skills/`. Doc-/Methodik-Skill
(`manual_verify_required: false`): Abnahme via Review + Dogfood.
