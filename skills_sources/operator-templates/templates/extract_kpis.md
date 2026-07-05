# Subagent-Briefing: Extract KPIs (TICKET-035)

Du bist ein Subagent des Immobewertung-Operators. Aufgabe: KPF, JNKM,
Brutto-Rendite, Wohnflaeche, Kaufpreis aus `scraper_data_json` +
Trello-Description in echte Property-Felder schreiben.

## Briefing-Variablen (vom Operator gefuellt)
- `{task_id}`, `{property_id}`, `{payload_json}`, `{api_base}`

## Vorgehen — DIREKTER WORKER-CALL (kein LLM, kein Skill)

Das ist reine Python-Regex-Logik, **kein** Claude-Call. Du fuehrst den
bestehenden Worker aus — **CLI ist die Primaer-Empfehlung** (TICKET-276):

```bash
cd C:/Users/Jakob/claude_projects/Immobewertung
python -m workers.extract_kpis --property-id {property_id}
```

Programmatischer Fallback (TICKET-276): Die echte Worker-Signatur ist
`process_property(p: Property)` — sie nimmt ein **geladenes Property-Objekt**,
KEINEN `property_id=`-Keyword-Parameter. Empfohlen ist `main(property_id=N)`
(kapselt Session, Commit + T203-Re-Screen und liefert ein Summary-Dict):

```python
from workers.extract_kpis import main
summary = main(property_id={property_id})
# summary = {"processed": 1, "asking_price": 1, "jnkm_ist": 1,
#            "kpf_ist": 1, "wfl_m2": 0, "rescreened": 1, ...}
```

Wer wirklich nur die pure Extraktion braucht, laedt das Objekt selbst:

```python
from db.engine import SessionLocal
from db.models import Property
from workers.extract_kpis import process_property

with SessionLocal() as s:
    p = s.get(Property, {property_id})
    process_property(p)   # mutiert p in-place, fuellt nur leere Felder
    s.commit()
```

## Erwartetes Ergebnis

Worker setzt die Property-Felder per UPDATE. Du:

1. Hole das Property-Snapshot **vor** dem Run via
   `GET {api_base}/api/property/{property_id}`.
2. Fuehre Worker aus.
3. Hole das Snapshot **nach** dem Run.
4. Diff bilden — Set von neu gesetzten / geaenderten Feldern.

## Task completen

```bash
curl -X POST {api_base}/api/agent-tasks/{task_id}/complete \
     -d '{
       "status": "done",
       "result_json": {
         "fields_set": {"kp": 549000, "jnkm": 32400, ...},
         "skipped": ["wfl_already_set"],
         "summary": "Property #{property_id}: 4 KPIs gesetzt (kp, jnkm, kpf, brutto_rendite)"
       }
     }'
```

## Fehlerfaelle

- Worker raised Exception → `failed` mit
  `error_msg="extract_kpis_failed: <ex>"`.
- Worker setzt 0 Felder (alles schon da, kein Regex-Match) → `done`
  mit `fields_set={}`, `summary="bereits alle KPIs gesetzt"`.

## Was du NIEMALS tun darfst

- **Eigene Regex erfinden** — der Worker hat die abgestimmten Patterns
  (`_extract_jnkm_from_desc`, `_parse_money`, ...). Wenn die nicht
  reichen: Folge-Ticket vorschlagen, nicht ad-hoc patchen.
- **Property-Felder direkt per API patchen** — der Worker macht das via
  SessionLocal-Commit konsistent.
- **LLM/Skill aufrufen** — das ist pure Python, kein Token-Verbrauch
  fuer KPI-Extraktion noetig. Skill-Call ist hier Geldverschwendung
  und macht den Output instabil.
- **Bei Skip-Faellen `failed` setzen** — "bereits gesetzt" ist `done`
  mit leerem `fields_set`.
