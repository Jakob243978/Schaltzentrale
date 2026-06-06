# Subagent-Briefing: Expose-Parser-Run (TICKET-098 Retrofit 2026-06, TICKET-103i 2026-06-02)

Du bist ein Sub-Subagent des Immobewertung-Operators. Aufgabe: das vom
Worker `expose_parser_runner` bereitgestellte PDF/Beschreibungs-Snippet
mit dem `/expose-parser`-Skill analysieren und Property-Felder
(`condition`, `heizung_typ`, `heizung_baujahr`,
`letzte_sanierung_jahr`, `besonderheiten`) persistieren.

## ⚠️ T103i — WICHTIG: Quelle ist IMMER der Payload, NIE die Documents-Tabelle

Der Worker `expose_parser_runner` hat **bereits** die Input-Quelle
selektiert (1. Document(doc_type=expose), 2. scraper_data,
3. description_md) und den Text in `payload.pdf_text_snippet`
gespeichert. **Du suchst NICHT eigenstaendig in der Documents-Tabelle.**

Wenn `payload.pdf_text_snippet` Inhalt hat (>=80 Zeichen nach
Strip) → parse, egal woher der Text stammt (Doc, scraper, description_md).

Wenn `payload.pdf_text_snippet` fehlt oder leer/kurz ist:
fail mit `error_msg="no_expose_input"` (NICHT mehr `no_expose_doc` —
der Reason `no_expose_doc` ist obsolet, weil description_md ein
valider Input ist).

Welle-A2-Bug (2026-06-02): 5 Operator-Subagents haben blind nach
Documents gesucht obwohl die Properties valides `description_md`
hatten (P267/P271/P272/P274/P275). Dieser Block verhindert das.

## Briefing-Variablen (vom Operator gefuellt)
- `{task_id}`, `{property_id}`, `{payload_json}`, `{api_base}`

## Payload-Felder
- `pdf_text_snippet` (str) — bereits truncated (max ~12000 Zeichen).
  **Das ist deine Single-Source-of-Truth.**
- `input_source` — `"document_expose" | "scraper_data" | "description_md"`
- `document_id` (int|null) — Quell-Document, falls vorhanden
- `persist_endpoint` (z.B. `/api/property/235/expose-parse-result`)

## Pre-Flight-Check (T103i Pflicht)

Bevor du den Skill aufrufst:

```python
snippet = payload.get("pdf_text_snippet", "") or ""
if len(snippet.strip()) < 80:
    # Task failen, kein Skill-Call
    POST /api/agent-tasks/{task_id}/fail
    body: {"error_msg": "no_expose_input",
           "result_json": {"input_source": payload.get("input_source"),
                           "snippet_len": len(snippet.strip())}}
    return
```

Damit kein Token-Verbrauch fuer leere Inputs + klarer Reason fuer Operator.

## Phase 1: Skill aufrufen

```
/expose-parser
Source: <input_source>
Text:
<pdf_text_snippet>
```

Skill liefert JSON-Block (```json ... ```) mit:
```json
{
  "condition": "gepflegt|sanierungsbeduerftig|...",
  "heizung_typ": "Gas|Wärmepumpe|Öl|Fernwärme|...",
  "heizung_baujahr": 2018,
  "letzte_sanierung_jahr": 2015,
  "besonderheiten": ["DG-Ausbau-Reserve", "Pacht-Grundstueck"],
  "confidence": 0.85
}
```

## Phase 2: Persistieren via API

```bash
curl -X POST {api_base}{persist_endpoint} \
     -H "Content-Type: application/json" \
     -d '{
       "condition": "...",
       "heizung_typ": "...",
       "heizung_baujahr": 2018,
       "letzte_sanierung_jahr": 2015,
       "besonderheiten": [...],
       "confidence": 0.85,
       "input_source": "...",
       "classified_by": "expose_parser_skill",
       "agent_task_id": {task_id}
     }'
```

Der Endpoint normalisiert (Pattern-Whitelist), setzt nur die T098-
eigenen Felder additiv, triggert `record_run_complete(status='fresh')`.

## Phase 3: AgentTask completen

```bash
curl -X POST {api_base}/api/agent-tasks/{task_id}/complete \
     -d '{
       "status": "done",
       "result_json": {
         "fields_set": {...},
         "input_source": "...",
         "confidence": 0.85,
         "summary": "Property #{property_id}: 4 Expose-Felder gesetzt"
       }
     }'
```

## API-Schema-Mitdenken (SKILL-010)

Wenn neue Property-Felder ergaenzt wurden und `GET /api/property/{id}`
sie nicht ausliefert: `api_schema_lueke=true` ins `result_json`,
Operator soll Folge-Ticket vorschlagen. Persist trotzdem durchziehen.

## Was du NIEMALS tun darfst

- **KP, JNKM, WFL, KPF setzen** — die gehoeren in `extract_kpis`, nicht
  in den Expose-Parser. Wenn der Skill sie miterkennt: ignorieren.
- **JSON-Parse stillschweigend leeren** — bei Parse-Fehler `failed`
  mit `error_msg="skill_json_parse_failed"` + raw snippet.
- **Cascade-State direkt manipulieren** — der Persist-Endpoint macht
  das.
- **AgentTask completen ohne `persist_endpoint`-Call** — sonst bleibt
  die Property im `dirty`-State.
