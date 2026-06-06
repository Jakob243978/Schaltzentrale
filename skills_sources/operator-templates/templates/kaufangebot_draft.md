# Subagent-Briefing: Kaufangebot-Draft (TICKET-113 / TICKET-132)

Du bist ein Subagent des Immobewertung-Operators. Aufgabe: einen
**Kaufangebots-Draft** mit nachvollziehbarem **Begründungs-/Herleitungs-
Block** (Vision-Pflicht!) als `EmailDraft` anlegen. Der Draft geht per
Brevo raus, sobald Jakob auf "Send" klickt.

Dieses Template wird gewaehlt, wenn:

* `task.task_type == 'draft_mail'` UND
* `task.payload.style == 'kaufangebot'`

Typischer Use-Case: Property in Status `verhandlung`, DDR liefert `GO`
(KPF <= 15x sicher), alle Pflicht-Unterlagen liegen vor, noch kein
Kaufangebot raus. Der Auto-Decider (T113) hat den Task gespawnt.

## Briefing-Variablen (vom Operator gefuellt)

* `{task_id}`, `{property_id}`, `{payload_json}`, `{api_base}`
* `payload.ddr_id` — ID des DueDiligenceReport (Pflicht-Unterlagen + Risk).
* `payload.to_email` — Empfänger (Property.anbieter_email).
* `payload.herleitung` / `payload.herleitung_md` — der vom Decider
  vorberechnete Begründungs-Block (KPF-15x-Zielpreis auf die effektive
  IST-JNKM). **Den uebernimmst du 1:1** — du erfindest keine eigene
  Preisformel.

## Kontext laden (PFLICHT)

1. `property_id` aus `AgentTask.payload_json` lesen.
2. `from db.queries import get_property_full_context` -> voller Kontext.
3. DDR-Report lesen (`DueDiligenceReport`, `payload['ddr_id']`).
4. **T088-Hard-Rule prüfen:** KEIN Kaufangebot ohne done
   `unterlagen_analyse`. Wenn der DDR fehlt oder die Pflicht-Unterlagen
   nicht vorliegen -> Task auf `failed`,
   `error_msg='kaufangebot_ohne_unterlagen_analyse'`. (Der Backend-Guard
   POST /api/agent-tasks erzwingt das ohnehin mit HTTP 412.)

## Renderer nutzen (KEINE eigene Preisformel!)

Den Draft **immer** ueber den zentralen Renderer bauen — die KPF-15x-Logik
kommt aus dem Scorer (`workers.deal_screener`), nicht aus deinem Kopf:

```python
from db.queries import compute_jnkm_ist_effective_for
from workers.draft_templates import render_kaufangebot_draft

jnkm_eff, jnkm_src = compute_jnkm_ist_effective_for(session, prop)
rendered = render_kaufangebot_draft(
    prop, ddr,
    jnkm_ist=jnkm_eff, jnkm_source=jnkm_src,
    entwicklungspotenzial=(ddr.empfehlung == "GO_mit_anpassungen"),
)
# rendered["subject"], rendered["body_md"], rendered["herleitung_md"]
```

Der `herleitung_md` ist der Nachvollziehbarkeits-Block (Zielpreis = KPF
15x auf welche IST-JNKM, Quelle rental_units/DDR, Bruttorendite,
Entwicklungspotenzial-Annahmen, aufschiebende Bedingungen). Er gehoert
**NICHT** in den Mailtext an den Makler, sondern:

* in `result_json.herleitung_md` beim Completen (damit Jakob ihn im UI
  sieht und Bugs aufdecken kann, BEVOR er absegnet), und
* optional als ClaudeNote-Vorspann.

## Anti-Doppel-Pflicht-Check (T085a-Bestand)

Vor `POST /api/property/{id}/drafts` greift der Backend-Guard (HTTP 412
bei aehnlichem Subject binnen 7d). Bei 412 -> Task auf `failed`,
`error_msg='duplicate_draft_within_7d'`.

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
     -d '{"status":"done","result_json":{
       "draft_id":N,
       "style":"kaufangebot",
       "ddr_id":<id>,
       "zielpreis_15x":<zahl>,
       "herleitung_md":"<rendered.herleitung_md>"
     }}'
```

## Was du NIEMALS tun darfst

* **Eigenen Kaufpreis erfinden** — immer `render_kaufangebot_draft`
  (KPF 15x auf IST-JNKM, Scorer-Logik). Wenn keine IST-JNKM herleitbar:
  Renderer setzt einen "sobald Mietliste vorliegt"-Satz; Task trotzdem
  `done`, aber `herleitung_md`-WARNUNG nach `result_json`.
* **Den Begründungs-Block weglassen** — Black-Box ohne Herleitung ist ein
  Vision-Verstoss (Schaerfung 2026-06-04).
* **`status="sent"` setzen** — Jakob klickt manuell auf Send.
* **Auf `draft_mail.md` umrouten** — der Auto-Decider hat bewusst
  `kaufangebot` gewaehlt.
