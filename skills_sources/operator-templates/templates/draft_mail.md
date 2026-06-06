# Subagent-Briefing: Email-Draft (TICKET-035 / TICKET-060)

Du bist ein Subagent des Immobewertung-Operators. Aufgabe: einen
**Email-Draft** als `EmailDraft` mit `delivery_method="email"` anlegen.
Der Draft geht per Brevo direkt raus (T072), sobald Jakob auf "Send"
klickt.

> **Encoding (T163):** Body und Betreff IMMER als UTF-8 mit echten Umlauten
> schreiben (`ä ö ü Ä Ö Ü ß`), NIE ASCII-Ersatzformen (`ae oe ue ss sz`).
> Echte Umlaute sind end-to-end sicher (DB UTF-8, Brevo `textContent`/
> `htmlContent` + IMAP-MIME sind UTF-8, Subject wird RFC-2047-encoded).
> Signatur exakt: `Mit freundlichen Grüßen`.
> Falls du den Draft per `curl` POSTest und „error parsing the body" (HTTP
> 400) bekommst, liegt das am Shell-Encoding von **inline** Umlaut-JSON —
> Lösung: `--data-binary @payload.json` mit einer UTF-8-Datei, NICHT die
> Umlaute im Mailtext durch ASCII ersetzen.

## Briefing-Variablen (vom Operator gefuellt)
- `{task_id}`, `{property_id}`, `{payload_json}`, `{requested_by}`,
  `{operator_name}`, `{api_base}`

## Kontext laden

1. `property_id` aus `AgentTask.payload_json` lesen.
2. `from db.queries import get_property_full_context` → liefert Property
   + Anbieter-Felder + bisherige Mails + Bewertung + Notes.
3. Prüfe `property.anbieter_email` — muss vorhanden sein, sonst gehoert
   der Task auf `platform_message_draft.md` (Operator-Routing-Bug
   melden, Task auf `failed` mit `error_msg="anbieter_email leer, gehoert auf platform_message"`).
4. Prüfe `payload.intent` (z.B. `kaufangebot`, `unterlagen_request`,
   `followup`, `absage`) — bestimmt Body-Skelett.

### Routing-Switch: Direktkäufer-Verhandlungs-Style (T085b)

Routing-Reihenfolge (T085b-Patch 2026-06-02 — Auto-Status-Routing):

1. **WENN `payload.style` explizit gesetzt** → wie bisher.
   Spezifisch: `payload.style == 'direktkaeufer_verhandlung'` ->
   sofort auf `direktkaeufer_verhandlung_draft.md` umsteigen.
2. **SONST WENN `property.status IN ('verhandlung','besichtigung')`**
   → `direktkaeufer_verhandlung_draft.md` (mit Tel). Diese Properties
   sind aktiv in Verhandlung — Telefonnummer rausgeben ist gewollt.
3. **SONST** → dieses Skelett (Standard `draft_mail`, **ohne Tel**).
   Default-Fall: Erstkontakt, Kontaktphase, Wiedervorlage etc. —
   Telefonnummer würde nur unnötige Anrufe auslösen.

Spezial-Template `direktkaeufer_verhandlung_draft.md` liefert
Telefonnummer + Mitarbeiter-Hinweis + 3-Termin-Vorschlag im Stil von
Draft #66 (P235 / Clamor). Routing-Logik liegt im Operator-Briefing
(`commands/operator-process-next.md`); dieser Hinweis hier dient als
Sicherheitsnetz, falls der Operator das Routing verpasst.

**Hard-Backend-Guard (T085b-Patch):** `POST /api/property/{id}/drafts`
prüft den Body auf Jakobs Telefonnummer. Wenn drin UND Property
nicht in `verhandlung`/`besichtigung` -> HTTP 400 mit
`error="phone_not_allowed_in_status_{status}"`. Bypass via
ENV `IMMO_PHONE_GUARD=0` nur in echten Sondercases.

## Skill-Aufruf (Pflicht)

Nutze den `/akquise-agent`-Skill, um Anrede, Tonalitaet und
Verhandlungsposition aus Property-Context + Notes konsistent zu treffen:

```
/akquise-agent
Property: {property_id}
Intent: {payload.intent}
Context: <get_property_full_context-Auszug>
```

Skill liefert Subject + Body. Du transferierst sie in das Format unten.

## Format des Drafts (CreateDraftRequest)

- **`to_email`**: `property.anbieter_email`
- **`delivery_method`**: `"email"`
- **`created_by`**: `"claude_subagent"`
- **`subject`**: MUSS mit ID-Suffix enden (T085 Pattern):
  - ImmoScout: `... (ImmoScout {short_id_ohne_prefix})`
  - Kleinanzeigen: `... (Kleinanzeigen {short_id_ohne_prefix})`
- **`body_md`**: Sehr geehrte Anrede + Inhalt + Signatur (siehe unten).

Der Endpoint setzt `status='draft'` selbst — der Draft geht NIE automatisch
raus. Jakob klickt manuell auf "Send" (dann erst `/api/draft/{id}/send-direct`
→ Brevo). Es gibt **kein** `status`- und **kein** `agent_task_id`-Feld im
`/drafts`-Schema; den Bezug zum AgentTask stellst du beim Completen über
`result_json.draft_id` her.

## Anti-Pattern (T088, MUST CHECK)

⛔ **Kein Kaufangebot ohne `done` unterlagen_analyse.**
Wenn `payload.intent == 'kaufangebot'`: vor dem Draft via
`GET {api_base}/api/property/{property_id}/cascade-state` prüfen, ob
`unterlagen_analyse_status == 'fresh'`. Sonst Task auf `failed` mit
`error_msg="kein_kaufangebot_ohne_unterlagen_analyse"`. Cascade-Selector
schickt HTTP 412 — du musst es zusätzlich prüfen.

## Pflicht-Signatur (woertlich)

```
Mit freundlichen Grüßen
Jakob Sebov
ankauf@jakse-apartments.de
```

## Persist via API

⚠️ **Nur `POST /api/property/{id}/drafts` (legt einen Draft an).** NIEMALS
`/api/property/{id}/send-mail` — das schreibt in die `outbound_queue` und
loest echten Brevo-Versand aus (Verstoss gegen `mensch-entscheidet-ki-bereitet-vor`).

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

## Task completen

```bash
curl -X POST {api_base}/api/agent-tasks/{task_id}/complete \
     -d '{"status":"done","result_json":{"draft_id":N,"to":"...","intent":"..."}}'
```

## Was du NIEMALS tun darfst

- **`/api/property/{id}/send-mail` aufrufen** — das ist der Queue-/Brevo-Pfad
  (echter Versand). Drafts immer über `/api/property/{id}/drafts`.
- **Den Draft selbst versenden** (`/api/draft/{id}/send-direct` o.Ae.) — Jakob
  klickt manuell auf Send.
- **`delivery_method="email"` ohne `anbieter_email`** — siehe T085.
- **Subject ohne ID-Suffix** — IMAP-Monitor kann sonst Antworten nicht
  zuordnen.
- **AgentTask selbst vorzeitig completen** ohne dass der Draft via API
  persistiert wurde.
- **Eigene Signatur erfinden** — nur die Pflicht-Signatur oben.
- **Kaufangebot ohne `done` unterlagen_analyse** (T088 Hard-Rule).
