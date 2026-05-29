---
name: operator-templates
version: 0.2
description: Templates fuer den Immobewertung-Operator-Subagent (TICKET-035). Beim Abarbeiten eines AgentTasks aus der Queue (`/operator-process-next` / `/operator-process-all`) waehlt der Operator anhand `task_type` + Payload-Hints das passende Sub-Template aus `templates/` und delegiert die Arbeit an einen frischen Subagent mit dem Briefing aus dem Template. Aktivieren wenn ein Subagent fuer eine Property-bezogene Aufgabe (Draft-Mail, Plattform-Nachricht, Unterlagen-Analyse, KPI-Extraction, Research, Triage-Reopen) geplant wird.
---

# Operator-Templates Skill

Dieser Skill stellt Briefing-Templates bereit, die der Operator-Subagent
in der Immobewertung-CRM-App nutzt, um neue Subagents mit klaren
Aufgaben + Output-Format-Vorgaben zu instruieren.

## Verfuegbare Templates

| Template | task_type | Output |
|---|---|---|
| `templates/draft_mail.md` | `draft_mail` (Email-Pfad) | EmailDraft mit `delivery_method='email'` |
| `templates/platform_message_draft.md` | `draft_mail` mit `payload.platform` ODER source_type=IS/KA + anbieter_email leer | EmailDraft mit `delivery_method='platform_message'` |
| `templates/unterlagen_analyse.md` | `unterlagen_analyse` | ClaudeNote + Risk-Verdict |
| `templates/extract_kpis.md` | `extract_kpis` | Property-KPF/JNKM/Brutto-Felder gefuellt |
| `templates/research.md` | `research` | ClaudeNote mit Recherche-Befund |
| `templates/triage_reopen.md` | `triage_reopen` | Mail aus Stumm zurueckholen |
| `templates/generic.md` | unknown | Fallback-Briefing |

## Routing

Routing-Logik im Operator-Briefing (siehe `commands/operator-process-next.md`):

1. `task.task_type` als Primaer-Schluessel
2. Bei `draft_mail`: Wenn `payload.platform IN ('immoscout','kleinanzeigen','sonstige')` ODER
   (`property.source_type IN ('immoscout','kleinanzeigen')` AND `property.anbieter_email IS NULL`)
   → `platform_message_draft.md` statt `draft_mail.md`
3. Sonst: `generic.md`

## Pflicht-Outputs

Jedes Template endet mit dem Block "Was du NIEMALS tun darfst" — bewahrt
den Subagent davor, AgentTasks selbst zu komplettieren (das macht der
Operator). Templates duerfen erweitert, aber nicht reduziert werden.
