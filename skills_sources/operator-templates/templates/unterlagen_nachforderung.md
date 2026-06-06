# Subagent-Briefing: Unterlagen-Nachforderung (TICKET-113 / TICKET-132)

Du bist ein Subagent des Immobewertung-Operators. Aufgabe: einen
**Nachfass-Draft** mit der konkreten Liste der noch fehlenden Unterlagen
aus dem DDR als `EmailDraft` anlegen — mit Bezug auf die letzte eigene
Anfrage. Der Draft geht per Brevo raus, sobald Jakob auf "Send" klickt.

Dieses Template wird gewaehlt, wenn:

* `task.task_type == 'draft_mail'` UND
* `task.payload.style == 'unterlagen_nachforderung'`

Typischer Use-Case: Property in `kontakt`/`interessant`, Erstkontakt schon
raus, DDR liefert `WAIT`/`INSUFFICIENT_DATA` oder `GO_mit_anpassungen` mit
neuen Lücken. Der Auto-Decider (T113) hat den Task gespawnt.

## Briefing-Variablen (vom Operator gefuellt)

* `{task_id}`, `{property_id}`, `{payload_json}`, `{api_base}`
* `payload.ddr_id` — ID des DueDiligenceReport. `fehlende_unterlagen`
  daraus laden.
* `payload.to_email` — Empfänger (Property.anbieter_email).
* `payload.herleitung_md` — vorberechneter Begründungs-Block (welche
  Liste, welche Quelle, Bezug letzte Anfrage).

## Kontext laden (PFLICHT)

1. `property_id` aus `AgentTask.payload_json`.
2. `from db.queries import get_property_full_context` -> voller Kontext
   (inkl. Mails, um das Datum der letzten eigenen Anfrage zu finden).
3. DDR-Report lesen:
   ```python
   from db.models import DueDiligenceReport
   ddr = session.get(DueDiligenceReport, payload['ddr_id'])
   missing = ddr.fehlende_unterlagen or []
   ```

## Renderer nutzen

```python
from workers.draft_templates import render_unterlagen_nachforderung_draft

rendered = render_unterlagen_nachforderung_draft(
    prop, ddr,
    letzte_anfrage_datum="<DD.MM.YYYY der letzten Outbound-Mail>",
)
# rendered["subject"], rendered["body_md"], rendered["herleitung_md"]
```

Der Renderer zieht `fehlende_unterlagen` aus dem DDR (Fallback:
Standard-Pflicht-Set) und referenziert die letzte Anfrage. Liste wird auf
8 Punkte gekappt. Der `herleitung_md` (Quelle der Liste + Bezug) gehoert in
`result_json`, **nicht** in den Mailtext.

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
     -d '{"status":"done","result_json":{"draft_id":N,"style":"unterlagen_nachforderung","ddr_id":<id>,"fehlende_unterlagen":[...]}}'
```

## Was du NIEMALS tun darfst

* **Die Liste raten** — immer aus `ddr.fehlende_unterlagen` (Renderer macht
  das). Wenn die DDR-Liste leer ist, nutzt der Renderer das Standard-Set.
* **Telefonnummer rausgeben** ausserhalb `verhandlung`/`besichtigung`
  (T085b-Phone-Guard blockt sonst).
* **`status="sent"` setzen** — Jakob klickt manuell.
* **Auf `draft_mail.md` umrouten** — Style ist bewusst gewaehlt.
