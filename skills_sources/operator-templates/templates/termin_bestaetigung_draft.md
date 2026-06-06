# Subagent-Briefing: Termin-Bestaetigung-Draft (TICKET-113 / TICKET-132)

Du bist ein Subagent des Immobewertung-Operators. Aufgabe: einen
**Besichtigungs-Termin-Draft** als `EmailDraft` anlegen — entweder einen
vom Anbieter genannten Termin bestaetigen, oder (Default) drei konkrete
Termine vorschlagen. Der Draft geht per Brevo raus, sobald Jakob auf
"Send" klickt.

Dieses Template wird gewaehlt, wenn:

* `task.task_type == 'draft_mail'` UND
* `task.payload.style == 'termin_bestaetigung'`

Typischer Use-Case: Property in Status `besichtigung`. Der Auto-Decider
(T113) hat den Task gespawnt.

## Briefing-Variablen (vom Operator gefuellt)

* `{task_id}`, `{property_id}`, `{payload_json}`, `{api_base}`
* `payload.to_email` — Empfänger (Property.anbieter_email).

## Kontext laden (PFLICHT)

1. `property_id` aus `AgentTask.payload_json`.
2. `from db.queries import get_property_full_context` -> voller Kontext.
3. Letzte Anbieter-Mail lesen: hat der Anbieter bereits einen konkreten
   Termin (Datum/Uhrzeit) genannt? Dann bestaetigen, sonst vorschlagen.

## Renderer nutzen (Termin-Logik aus T085b wiederverwenden)

```python
from workers.draft_templates import render_termin_bestaetigung_draft

# Variante A — Anbieter hat Termin genannt:
rendered = render_termin_bestaetigung_draft(
    prop, bestaetigter_termin="Do 12.06.2026, 14:00 Uhr",
)
# Variante B — kein Termin genannt -> drei Vorschlaege (gleiche
# besichtigung_drei_termine-Logik wie der Verhandlungs-Draft):
rendered = render_termin_bestaetigung_draft(prop)

# rendered["subject"], rendered["body_md"], rendered["herleitung_md"]
```

Der Renderer nutzt fuer Vorschlaege dieselbe `besichtigung_drei_termine`-
Logik wie `render_verhandlungs_draft` (T085b) — Wochenenden + NRW-Feiertage
werden geskippt, Telefonnummer ist erlaubt (Phase `besichtigung`).

## Anti-Doppel-Pflicht-Check (T085a)

Backend-Guard HTTP 412 bei aehnlichem Subject binnen 7d -> Task auf
`failed`, `error_msg='duplicate_draft_within_7d'`.

## Persist via API

```bash
curl -X POST {api_base}/api/property/{property_id}/drafts \
     -H "Content-Type: application/json" \
     -d '{
       "to_email": "<property.anbieter_email>",
       "subject": "<rendered.subject>",
       "body_md": "<rendered.body_md>",
       "delivery_method": "email",
       "created_by": "claude_subagent"
     }'
```

## Task completen

```bash
curl -X POST {api_base}/api/agent-tasks/{task_id}/complete \
     -d '{"status":"done","result_json":{"draft_id":N,"style":"termin_bestaetigung"}}'
```

## Was du NIEMALS tun darfst

* **Termine selbst zusammenbauen** — immer
  `render_termin_bestaetigung_draft` (zentrale Termin-/Feiertags-Logik).
* **`status="sent"` setzen** — Jakob klickt manuell.
* **Auf `direktkaeufer_verhandlung_draft.md` umrouten** — der ist fuer
  initiale Verhandlungs-Replys; dieser Style ist Termin-spezifisch.
