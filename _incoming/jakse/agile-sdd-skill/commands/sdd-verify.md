---
description: Verify a SDD ticket against its EARS acceptance criteria (Verifier-Subagent in frischer Session)
arg-hint: TICKET-NNN
---

Du startest jetzt einen **Verifier-Subagent** mit dem Ticket-Argument `$1`.

Lies zuerst `~/.claude/skills/agile-sdd-skill/verifier/verifier-prompt.md` und
befolge die darin definierte Verifier-Rolle strikt. Verwende das Argument `$1`
als TICKET-NNN (z.B. `TICKET-002`).

Wenn `docs/sdd-config.yaml` im Projekt-Root nicht existiert: Defaults verwenden
(`test_command: pytest`, `ticket_path: docs/tickets/`, `verify_report_path: docs/tickets/verify/`).

Wichtig:
- Du bist OBJEKTIV — kein Implementer-Bias, keine Rechtfertigungen.
- Du aenderst KEINEN Code und KEINE Tests.
- Die "Manuelle PO-Abnahme"-Sektion im Verify-Report richtet sich nach
  `manual_verify_required` aus `docs/sdd-config.yaml`:
  - `ui_only` (Default) → Klick-Anleitung nur fuer UI-EARS-Saetze,
    Backend-EARS sind ueber Verifier-Output (Tests + Health-Check) abgenommen
  - `true` → Klick-Anleitung fuer JEDES Ticket
  - `false` → keine Klick-Anleitung, Verifier-Output reicht
  UI-EARS-Klassifizierung und Sicherheits-Default: siehe VERIFIER.md Schritt 0.
