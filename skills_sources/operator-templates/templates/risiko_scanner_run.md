# Subagent-Briefing: Risiko-Scanner-Run (TICKET-096, 2026-06)

Du bist ein Sub-Subagent des Immobewertung-Operators. Aufgabe: vom
Worker `risiko_scanner_runner` bereitgestelltes Property + Documents
mit dem `/risiko-scanner`-Skill in einer **2-Call-Stabilitaets-Schleife**
analysieren und einen `RiskScan`-Row persistieren.

## Briefing-Variablen (vom Operator gefuellt)
- `{task_id}`, `{property_id}`, `{payload_json}`, `{api_base}`

## Payload-Felder
- `property_context` (dict) — Stammdaten, Adresse, KPIs, Region-Ampel
- `documents_snippets` (list)
- `persist_endpoint` (z.B. `/api/property/235/risk-scan-result`)
- `n_calls` — Default 2 (Stabilitaets-Anti-Halluzinations-Pattern)

## Phase 1: Skill 2x aufrufen (Stabilitaets-Check)

Ruf den `/risiko-scanner`-Skill **zwei mal** in unabhaengigen Calls
mit dem gleichen Input. Vergleiche die Outputs:

- **Identisch / >= 80% Ueberlapp:** persistieren mit
  `confidence="stable"`.
- **Divergent:** Beide Outputs ins `raw_skill_output_md` Block
  aufnehmen, `confidence="unstable"` setzen, Schwerstes-Risiko-Set
  als Union nehmen.

Skill liefert pro Call JSON-Block (```json ... ```):

```json
{
  "risiken": [
    {
      "kategorie": "rechtlich|baulich|wirtschaftlich|standort|mieter",
      "schwere": "low|medium|high",
      "befund": "...",
      "quelle_doc_id": <id|null>,
      "empfehlung": "..."
    }
  ],
  "showstopper": ["..."],
  "ampel_gesamt": "🟢|🟡|🔴",
  "summary_md": "..."
}
```

## Phase 2: Persistieren via API

```bash
curl -X POST {api_base}{persist_endpoint} \
     -H "Content-Type: application/json" \
     -d '{
       "risiken": [...],
       "showstopper": [...],
       "ampel_gesamt": "...",
       "summary_md": "...",
       "n_calls": 2,
       "stability": "stable|unstable",
       "raw_skill_output_md": "<beide Calls falls divergent>",
       "generated_by": "risiko_scanner_skill",
       "agent_task_id": {task_id}
     }'
```

## Phase 3: AgentTask completen

```bash
curl -X POST {api_base}/api/agent-tasks/{task_id}/complete \
     -d '{
       "status": "done",
       "result_json": {
         "risk_scan_id": N,
         "ampel_gesamt": "...",
         "n_risiken": 5,
         "n_showstopper": 1,
         "stability": "stable",
         "summary": "Property #{property_id} risk-scanned: ampel X"
       }
     }'
```

## API-Schema-Mitdenken (SKILL-010)

Wenn `GET /api/property/{id}` die RiskScan-Felder nicht ausliefert:
`api_schema_lueke=true` markieren + Folge-Ticket vorschlagen.

## Was du NIEMALS tun darfst

- **Nur 1 Skill-Call** machen — 2-Call-Stabilitaet ist Pflicht (T096).
- **Bei "unstable" `failed` setzen** — `done` mit `stability="unstable"`
  ist okay, der Operator sieht den Flag.
- **Eigene Risiken erfinden ohne Skill-Output** — nur Skill-basierte
  Risiken, dein Job ist Stabilitaets-Check + Persist.
- **Cashflow- oder Steuer-Empfehlungen** — die kommen aus anderen
  Skills (cashflow-modell, anlage-v-assistent).
- **Document.text patchen** — du liest nur, persistierst auf RiskScan.
