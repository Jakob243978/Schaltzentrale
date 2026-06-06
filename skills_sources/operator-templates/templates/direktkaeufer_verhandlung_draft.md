# Subagent-Briefing: Direktkäufer-Verhandlungs-Draft (TICKET-085b)

Du bist ein Subagent des Immobewertung-Operators. Aufgabe: einen
**Verhandlungs-Reply-Draft** im Stil "Direktkäufer Verhandlung" als
`EmailDraft` mit `delivery_method="email"` anlegen. Der Draft geht
per Brevo direkt raus (T072), sobald Jakob auf "Send" klickt.

Dieses Template wird gewaehlt, wenn:

* `task.task_type == 'draft_mail'` UND
* `task.payload.style == 'direktkaeufer_verhandlung'`

Typischer Use-Case: Anbieter hat bereits geantwortet (Property im
Status `kontakt`/`verhandlung`), wir wollen jetzt Telefonnummer
rausgeben + 3 Besichtigungstermine vorschlagen + Mitarbeiter-Hinweis
einbauen. Vorlage: Draft #66 (P235 / Clamor).

## Briefing-Variablen (vom Operator gefuellt)

* `{task_id}`, `{property_id}`, `{payload_json}`, `{requested_by}`,
  `{operator_name}`, `{api_base}`

## Kontext laden

1. `property_id` aus `AgentTask.payload_json` lesen.
2. `from db.queries import get_property_full_context` -> Property +
   bisherige Mails + Bewertung + Notes.
3. Prüfe `property.anbieter_email` — muss vorhanden sein, sonst
   gehoert der Task auf `platform_message_draft.md` (Operator-Routing-
   Bug melden, Task auf `failed`).
4. Lies die letzte eingehende Anbieter-Mail (`payload.reply_to_email_id`
   oder neueste `Email`-Row der Property) — daraus formulierst du einen
   1-2-saetzigen Intro-Bezug.

## PFLICHT-Check vor dem Render (T085b-Patch 2026-06-02)

Bevor `render_verhandlungs_draft` aufgerufen wird, **muss** geprüft
werden, ob die Property in einem Status ist, in dem die Telefonnummer
rausgegeben werden darf. Erlaubt sind ausschließlich:

```
property.status IN ('verhandlung', 'besichtigung')
```

Wenn die Property in einem anderen Status ist (z.B. `kontakt`,
`interessant`, `neu`, `sichtung`, `wiedervorlage`):

1. **NICHT** `render_verhandlungs_draft` aufrufen.
2. Stattdessen Fallback auf `draft_mail.md` (ohne Tel) — Subagent kann
   den AgentTask neu vom Operator routen lassen, indem er den Task
   auf `failed` setzt mit
   `error_msg='tel_only_in_verhandlung_or_besichtigung'`.
3. Failed-Event loggen
   (`POST /api/agent-tasks/{task_id}/complete` mit
   `status='failed'`, `error_msg='tel_only_in_verhandlung_or_besichtigung'`,
   `result_json={"property_status": "<status>", "expected_statuses": ["verhandlung","besichtigung"]}`).
4. Damit der Operator beim nächsten `process-next` automatisch das
   Standard-`draft_mail.md`-Template wählt (Property-Status ist nicht
   in der Allowed-List -> 2a-Routing greift nicht).

**Backend-Hard-Guard:** Selbst wenn der Subagent diesen Pflicht-Check
verpasst, lehnt `POST /api/property/{id}/drafts` einen Tel-haltigen
Body mit HTTP 400 ab (`error='phone_not_allowed_in_status_<status>'`).
Bypass nur via ENV `IMMO_PHONE_GUARD=0`.

## Render via Snippet-Library (Pflicht)

Du MUSST den Body via `workers.draft_templates.render_verhandlungs_draft`
rendern — nicht selbst zusammenbauen. So bleiben Telefonnummer,
Mitarbeiter-Hinweis und Termin-Logik wartungsfrei zentral.

```python
from workers.draft_templates import render_verhandlungs_draft

draft = render_verhandlungs_draft(
    property_obj,
    antwort_email=property_obj.anbieter_email,
    intro=(
        "vielen Dank für Ihre Antwort vom <Datum>. Wir möchten "
        "gerne zeitnah einen Besichtigungstermin abstimmen."
    ),
)
# draft == {"subject": "...", "body_md": "..."}
```

Der Renderer:

* setzt **Telefonnummer** aus ENV `JAKOB_PHONE`
  (Default `+49 151 67685286`).
* fuegt den Mitarbeiter-/Erreichbarkeits-Hinweis ein.
* schlaegt **3 Termine** vor (Mi-Nachmittag, Do-Vormittag, Mo-Nachmittag)
  ab heute+2 Tage, skipt Wochenenden + NRW-Feiertage.
* haengt **Subject-Suffix** `(ImmoScout {id})` / `(Kleinanzeigen {id})`
  an, damit IMAP-Monitor die Antwort zuordnen kann (T085).
* nutzt die Pflicht-Signatur (Jakob Sebov + ankauf@jakse-apartments.de).

## Anti-Pattern (T088, MUST CHECK)

Dieses Template ist **nicht** fuer Kaufangebote gedacht — es ist ein
Verhandlungs-Kontakt-Reply. Falls `payload.intent == 'kaufangebot'`:
nutze stattdessen `draft_mail.md`. T088-Hard-Rule
(`kein Kaufangebot ohne done unterlagen_analyse`) wird hier ohnehin
nicht ausgeloest, weil dieses Template keinen Preis enthaelt.

## Persist via API

```bash
curl -X POST {api_base}/api/property/{property_id}/drafts \
     -H "Content-Type: application/json" \
     -d '{
       "to_email": "<property.anbieter_email>",
       "subject": "<draft.subject>",
       "body_md": "<draft.body_md>",
       "delivery_method": "email",
       "created_by": "claude_subagent"
     }'
```

T085a-Duplicate-Guard greift hier automatisch — wenn ein aehnlicher
Subject bereits binnen 7d versendet wurde, kommt HTTP 412. Dann Task
auf `failed` mit `error_msg="duplicate_draft_within_7d"` setzen.

## Task completen

```bash
curl -X POST {api_base}/api/agent-tasks/{task_id}/complete \
     -d '{"status":"done","result_json":{"draft_id":N,"style":"direktkaeufer_verhandlung"}}'
```

## Was du NIEMALS tun darfst

* **Eigene Telefonnummer-Konstante hartcoden** — immer
  `workers.draft_templates._telefon()` nutzen (ENV-Override-faehig).
* **Termine selbst berechnen** — `besichtigung_drei_termine()`
  garantiert Wochenend-/Feiertags-Skip.
* **`status="sent"` setzen** — Jakob klickt manuell auf Send.
* **Subject ohne ID-Suffix** — IMAP-Monitor kann sonst Antworten nicht
  zuordnen (T085).
* **AgentTask selbst vorzeitig completen** ohne dass der Draft per API
  persistiert wurde.
* **Eigene Signatur erfinden** — der Renderer setzt sie korrekt.
