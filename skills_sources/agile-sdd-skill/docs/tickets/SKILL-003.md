# SKILL-003: Anti-Pattern "Iterative Artefakt-Generierung" + Implementer-Hygiene

**Status:** spec
**Erstellt:** 2026-05-25 (Original) | **Migriert:** 2026-05-25 (aus TICKET-082, Immobewertung)
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren` + `skill-schlanker-als-was-er-ersetzt`
**outcome_metric:** anti_pattern_im_skill_patterns_ordner (Ziel: +1 patterns/-Datei mit 3 Regeln)
**outcome_review_at:** null (wird beim done-Set gesetzt)

> [!info] Migrations-Hinweis
> Dieses Ticket wurde am 2026-05-25 aus `Immobewertung/docs/tickets/TICKET-082.md`
> nach `Schaltzentrale/skill_dev/docs/tickets/SKILL-003.md` migriert (TICKET-083).
> Original-Ticket bleibt mit Status `done` + Migrations-Note in Immobewertung
> bestehen.

## Was soll erreicht werden? (Business-Ziel)

Jakob 2026-05-25 (nach T078/T079-Token-Analyse):
> "[Die HTML] hat mehrmals geöffnet und wurde mehrmals geschrieben - warum?
> Ist das nicht sehr Token spielig?"

Befund: T078/T079-Implementer-Subagent hat 232.699 Tokens verbraucht.
Davon ~75-100k allein durch **iteratives Schreiben einer 98-KB-HTML** (3+
Iterationen mit Browser-Open dazwischen). Das Briefing sagte "Live-Smoke
ist Pflicht" — der Subagent hat das als "iteriere bis schoen"
interpretiert statt "verify einmal am Ende".

Ziel: **Implementer-Briefing-Hygiene** als verbindliche Regel im
agile-sdd-skill (oder im PO-Skill — siehe Teil D). Konkrete Regeln gegen
diese Klasse von Token-Verschwendung.

## Akzeptanzkriterien (EARS-Format)

### Teil A — Regel "Generator-Pattern bei grossen Artefakten"

- [ ] When ein Implementer ein Output-Artefakt > 10 KB erzeugen soll
      (HTML, grosse Markdown-Reports, JSON-Dumps), the system shall im
      Briefing-Template eine **Pflicht-Regel** enthalten:
      ```
      Wenn Output-Artefakt > 10 KB:
      - Verwende Generator-Pattern: Code (Python) + Template-Datei
        (Jinja2/string.Template) + 1x Generator-Aufruf
      - NICHT iterativ via Write-Tool zusammensetzen
      - HTML/MD entsteht im Filesystem durch Generator, nicht durch
        Subagent-Output
      ```

### Teil B — Regel "Live-Smoke = 1x am Ende"

- [ ] When ein Briefing "Live-Smoke ist Pflicht" enthaelt, the system
      shall praezisieren:
      ```
      Live-Smoke ist EIN finaler Verifikations-Schritt am Ende.
      - Browser-Open: 1x nach erstem Generate
      - Bei Problemen: Code/Template anpassen, Generator re-run, KEIN re-open
      - Wenn nach 2 Iterationen das Ergebnis nicht passt: stoppen + im
        Bericht melden, nicht 5x weiterversuchen
      ```

### Teil C — Token-Budget-Hint im Implementer-Briefing

- [ ] When ein Implementer-Subagent gebrieft wird, the system shall ein
      empfohlenes Token-Budget mitgeben (z.B. "Erwartetes Budget: 80-120k.
      Wenn Du bei 200k bist: in Bericht melden, nicht still weiter").
- [ ] When der Subagent sein Budget ueberschreitet, the system shall im
      Endbericht eine Begruendung verlangen ("Warum 232k statt 120k?
      Was war komplexer als erwartet?").

### Teil D — Im SDD/PO-Skill als Pattern verankern

- [ ] When der SDD-Skill (oder PO-Skill je nach Architektur-Entscheidung)
      deployed wird, the system shall folgende Datei enthalten:
      `<skill>/patterns/implementer-hygiene.md` mit den drei Regeln Teil
      A-C + Erlaeuterung am T078/T079-Live-Beispiel.
- [ ] When ein Operator (Claude im Chat) ein Implementer-Briefing
      schreibt, the system shall die `implementer-hygiene.md`-Regeln als
      Pflicht-Block im Briefing zitieren oder verlinken.

### Teil E — Memory-Save

- [ ] When dieses Ticket done ist, the system shall in
      `~/.claude/projects/.../memory/` einen Memory-Eintrag haben:
      `feedback_implementer_hygiene.md` mit den 3 Regeln als
      Auto-Reminder fuer alle zukuenftigen Implementer-Briefings.

## Technische Hinweise

- Anti-Pattern erkannt am 2026-05-25 — Live-Beispiel ist T078/T079 mit
  232k Tokens vs erwartet ~120k.
- SDD-Skill hat heute schon eine Verifier-Sektion. Hygiene-Block waere
  die natuerliche Erweiterung ("Verifier-Pattern fuer Implementer").
- **Architektur-Frage:** SDD-Skill oder PO-Skill? Argument fuer SDD:
  Implementer ist SDD-Konzept. Argument fuer PO: PO definiert das
  Briefing-Format. **Empfehlung:** SDD — Hygiene ist Implementer-Disziplin,
  PO challenged Vorab-Ideen.

## Code-Referenzen

- `<Schaltzentrale>/skills_sources/agile-sdd-skill/patterns/implementer-hygiene.md` (NEU)
- `~/.claude/projects/.../memory/feedback_implementer_hygiene.md` (NEU)
- Live-Beispiel-Verweis: T078/T079 Implementer-Bericht 2026-05-25

## Out of Scope

- Automatische Token-Telemetrie (Subagent meldet eigenes Budget) —
  Anthropic-SDK koennte das, aber das ist eigenes Ticket.
- Hard-Block bei Budget-Ueberschreitung — wuerde gute Subagents in
  echten Edge-Cases canceln. Soft-Regel reicht.

## Verknuepfte Tickets

- **Original:** `Immobewertung/docs/tickets/TICKET-082.md` (Migrations-
  Note hinzugefuegt)
- **Trigger:** TICKET-083 (Skill-Dev-Repo aufsetzen)
- **Verbunden:** SKILL-002 — Generator-Pattern wird dort beim
  T078/T079-Lift-and-Shift direkt umgesetzt (Code + Template-Datei
  statt String-Concat in Python).

## Ergebnis / Notizen

_(wird vom Implementer befuellt)_
