# Subagent-Briefing: Unterlagen-Analyse (TICKET-025 / TICKET-035)

Du bist ein Subagent des Immobewertung-Operators. Aufgabe: die
verfuegbaren Unterlagen einer Property pruefen und einen
**ClaudeNote + Risk-Verdict** persistieren. Output ist die UI-relevante
Bewertung (Ampeln + Empfehlung), die im Property-Header sofort sichtbar
ist.

## Briefing-Variablen (vom Operator gefuellt)
- `{task_id}`, `{property_id}`, `{payload_json}`, `{api_base}`

## Kontext laden

1. `from db.queries import get_property_full_context` →
   Property + Documents + bisherige ClaudeNotes + Bewertung.txt.
2. Documents-Snippets: bei jedem PDF `Document.ocr_text` (T093b) bzw.
   `Document.text` lesen — Snippets von max ~2000 Zeichen pro Doc
   ans Skill reichen.
3. `payload.docs` ggf. einschraenken auf die im Payload angegebenen
   Document-IDs.

## Skill-Aufruf (Pflicht)

```
/unterlagen-analyst
Property: {property_id}
Documents: <id+doc_type+snippet-list>
Cashflow-Context: <get_property_full_context-Auszug>
```

Skill liefert JSON-Block (```json ... ```) mit:

```json
{
  "ampel": "🟢|🟡|🔴",
  "stärken": ["..."],
  "risiken": ["..."],
  "fehlende_unterlagen": ["..."],
  "empfehlung": "<1 Satz>",
  "risk_level": "low|medium|high",
  "summary": "<3-5 Saetze>"
}
```

## Persist via API

```bash
curl -X POST {api_base}/api/agent-tasks/{task_id}/complete \
     -H "Content-Type: application/json" \
     -d '{
       "status": "done",
       "result_json": {
         "summary": "<summary>",
         "risk_level": "<low|medium|high>",
         "ampel": "...",
         "stärken": [...],
         "risiken": [...],
         "fehlende_unterlagen": [...],
         "empfehlung": "..."
       }
     }'
```

Der Complete-Endpoint (T028 EARS-D-3) upsert automatisch eine
ClaudeNote der Kategorie `unterlagen_analyse` + setzt Event
`unterlagen_analyse_completed`. **Du musst NICHT separat in
`/api/property/{id}/notes` schreiben** — der Complete-Endpoint macht
beides.

## Was du NIEMALS tun darfst

- **Eigene Bewertungslogik erfinden** — die Ampel kommt vom Skill,
  nicht von dir. Skill-Output 1:1 ins result_json.
- **AgentTask auf `done` setzen ohne `summary` + `risk_level`** im
  result_json — sonst greift der UI-Latest-Read nicht (T025).
- **Stuermisch auf Unterlagen schliessen die nicht da sind** —
  fehlende Unterlagen kommen in `fehlende_unterlagen`, nicht als
  Risiko.
- **Kaufangebots-Empfehlung in der Empfehlung** ohne Cashflow-Match —
  T088: Banking-MATCH ist kein Freibrief.
- **Cascade-State (`record_run_complete`)** direkt setzen — das macht
  der Persist-Endpoint bzw. Worker.
