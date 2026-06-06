---
name: operator-templates
version: 0.3
description: Templates fuer den Immobewertung-Operator-Subagent (TICKET-035). Beim Abarbeiten eines AgentTasks aus der Queue (`/operator-process-next` / `/operator-process-all`) waehlt der Operator anhand `task_type` + Payload-Hints das passende Sub-Template aus `templates/` und delegiert die Arbeit an einen frischen Subagent mit dem Briefing aus dem Template. Aktivieren wenn ein Subagent fuer eine Property-bezogene Aufgabe (Draft-Mail, Plattform-Nachricht, Unterlagen-Analyse, KPI-Extraction, Research, Triage-Reopen, Expose-/Mietlisten-/Doku-Parser) geplant wird.
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
| `templates/direktkaeufer_verhandlung_draft.md` | `draft_mail` mit `payload.style='direktkaeufer_verhandlung'` *(T085b 2026-06)* | EmailDraft im Stil Draft #66 (Tel + 3-Termin-Vorschlag + Mitarbeiter-Hinweis) |
| `templates/unterlagen_anforderung_erstkontakt.md` | `draft_mail` mit `payload.style='unterlagen_anforderung_erstkontakt'` *(T113 Phase-1 2026-06)* | EmailDraft mit Suchprofil-Pitch + Pflicht-Unterlagen-Liste aus DDR |
| `templates/absage_mit_suchprofil_draft.md` | `draft_mail` mit `payload.style='absage_mit_suchprofil'` *(T113 Phase-1 2026-06)* | EmailDraft mit Standard-Absage + Suchprofil-Hinweis |
| `templates/unterlagen_nachforderung.md` | `draft_mail` mit `payload.style='unterlagen_nachforderung'` *(T113 PHASE-2-STUB)* | failt mit `error_msg='style_not_yet_implemented'` |
| `templates/kaufangebot_draft.md` | `draft_mail` mit `payload.style='kaufangebot'` *(T113 PHASE-2-STUB)* | failt mit `error_msg='style_not_yet_implemented'` |
| `templates/termin_bestaetigung_draft.md` | `draft_mail` mit `payload.style='termin_bestaetigung'` *(T113 PHASE-2-STUB)* | failt mit `error_msg='style_not_yet_implemented'` |
| `templates/unterlagen_analyse.md` | `unterlagen_analyse` | ClaudeNote + Risk-Verdict |
| `templates/extract_kpis.md` | `extract_kpis` | Property-KPF/JNKM/Brutto-Felder gefuellt |
| `templates/research.md` | `research` | ClaudeNote mit Recherche-Befund |
| `templates/triage_reopen.md` | `triage_reopen` | Mail aus Stumm zurueckholen |
| `templates/expose_parser_run.md` | `expose_parser_run` *(T098 Retrofit 2026-06)* | Property-Felder (`condition`, `heizung_typ`, ...) via `POST /api/property/{id}/expose-parse-result` |
| `templates/mietlisten_parser_run.md` | `mietlisten_parser_run` *(T093 Retrofit 2026-06)* | RentalUnits + Analyse via `PUT /api/property/{id}/rental-units` |
| `templates/unterlagen_analyst_run.md` | `unterlagen_analyst_run` *(T099 Retrofit 2026-06)* | DueDiligenceReport via `POST /api/property/{id}/due-diligence-report` |
| `templates/dokument_klassifizierer_run.md` | `dokument_klassifizierer_run` *(T100 Retrofit 2026-06)* | Document-Klassifikation via `POST /api/document/{id}/classification-result` |
| `templates/marktanalyse_run.md` | `marktanalyse_run` *(T095 2026-06)* | MarketAnalysis + Region-Mietspiegel via `POST /api/region/{id}/market-analysis-result` (oder `/api/property/{id}/...`) |
| `templates/risiko_scanner_run.md` | `risiko_scanner_run` *(T096 2026-06, 2-Call-Stabilitaet)* | RiskScan via `POST /api/property/{id}/risk-scan-result` |
| `templates/pdf_vision_ocr.md` | `pdf_vision_ocr` *(T093b 2026-06)* | Document.ocr_text via Claude-Vision-Subscription -> `POST /api/document/{id}/ocr-result` |
| `templates/email_review_trigger_run.md` | `email_review_trigger` *(T103d 2026-06)* | Mail-Review-Vorschlag via `POST /api/email/{id}/review-result` |
| `templates/generic.md` | unknown | Fallback-Briefing |

## Routing

Routing-Logik im Operator-Briefing (siehe `commands/operator-process-next.md`):

1. `task.task_type` als Primaer-Schluessel
2. Bei `draft_mail`: Wenn `payload.platform IN ('immoscout','kleinanzeigen','sonstige')` ODER
   (`property.source_type IN ('immoscout','kleinanzeigen')` AND `property.anbieter_email IS NULL`)
   → `platform_message_draft.md` statt `draft_mail.md`
2a. Bei `draft_mail`: Wenn `payload.style == 'direktkaeufer_verhandlung'`
    → `direktkaeufer_verhandlung_draft.md` (T085b — gewinnt nicht ueber Plattform-Pfad;
    Plattform-Drafts brauchen nie dieses Template, weil Tel + Termine im Plattform-Body
    keinen Sinn ergeben).
2b. **TICKET-113 (2026-06-02):** Bei `draft_mail` mit `payload.style` aus dem
    T113-Set wird vor allen anderen Regeln (ausser dem Plattform-Pfad) auf das
    Style-Template gemappt:
    - `payload.style == 'unterlagen_anforderung_erstkontakt'`
      → `unterlagen_anforderung_erstkontakt.md`
    - `payload.style == 'absage_mit_suchprofil'`
      → `absage_mit_suchprofil_draft.md`
    - `payload.style == 'unterlagen_nachforderung'` → `unterlagen_nachforderung.md` (Phase-2-Stub, failt sofort)
    - `payload.style == 'kaufangebot'` → `kaufangebot_draft.md` (Phase-2-Stub, failt sofort)
    - `payload.style == 'termin_bestaetigung'` → `termin_bestaetigung_draft.md` (Phase-2-Stub, failt sofort)
    Phase-2-Stubs failen mit `error_msg='style_not_yet_implemented'`. Wenn
    `payload.style` zwar gesetzt, aber kein Match -> `draft_mail.md` Fallback.
3. **Legacy-Task-Types (Backwards-Kompat T093/T098/T099/T100/T095/T096 Retrofit):**
   - `expose_parser` → `expose_parser_run.md`
   - `mietlisten_parser` → `mietlisten_parser_run.md`
   - `unterlagen_analyst` → `unterlagen_analyst_run.md` (zusaetzlich
     zum `unterlagen_analyse` -> `unterlagen_analyse.md`-Mapping)
   - `dokument_klassifizierer` → `dokument_klassifizierer_run.md`
   - `marktanalyse` → `marktanalyse_run.md` (T095, neu)
   - `risk_scan` → `risiko_scanner_run.md` (T096, Legacy-Alias)
4. **T103d (2026-06):** `email_review_trigger` → `email_review_trigger_run.md`
   (Generalist-Agent nach Mail-Eingang; pruft Lead-Status-Update / Frage /
   Anhaenge / no_action)
5. Sonst: `generic.md`

## Pflicht-Outputs

Jedes Template endet mit dem Block "Was du NIEMALS tun darfst" — bewahrt
den Subagent davor, AgentTasks selbst zu komplettieren (das macht der
Operator). Templates duerfen erweitert, aber nicht reduziert werden.

## MCP/API-Schema-Hinweis (SKILL-010, 2026-06-01)

Wenn ein Operator-Template einen **Persist-Endpoint** nutzt (siehe
Retrofit-Tabelle unten — `POST /api/property/{id}/...`,
`PUT /api/property/{id}/rental-units`, `POST /api/document/{id}/...`),
ist beim Routing zusaetzlich zu pruefen:

- **Liefert der zugehoerige GET-Endpoint die neuen Felder, die der
  Subagent gerade persistiert, auch wieder aus?**
  Beispiel: Subagent schreibt `condition` + `heizung_typ` per
  `POST /api/property/{id}/expose-parse-result`, aber
  `GET /api/property/{id}` gibt die Felder nicht zurueck → Frontend
  sieht nichts. Klassischer T103a-Anti-Pattern.
- Wenn ein Mismatch entdeckt wird: AgentTask-Result mit Notiz
  `api_schema_lueke=true` markieren und Operator soll ein Folge-Ticket
  vorschlagen (`SKILL-010`-Pattern). Operator persistiert das Result
  trotzdem — Lueke ist API-Seite, nicht Worker-Seite.

Diese Hygiene-Regel referenziert den Standard-Block "API-Schema-
Mitdenken" aus `agile-sdd-skill/templates/IMPLEMENTER_BRIEFING_STANDARDS.md`
und wird bei jedem neuen `*_run`-Template mitgepflegt.

## Retrofit Operator-Pattern (2026-06) — T093/T098/T099/T100

Frueher hatten die Worker `workers/expose_parser_runner.py`,
`workers/mietlisten_runner.py`, `workers/unterlagen_analyst_runner.py`
und `workers/dokument_klassifizierer.py` einen direkten
`anthropic.Anthropic().messages.create()`-Call eingebaut, mit
`skipped_no_api_key`-Fallback wenn kein `ANTHROPIC_API_KEY` gesetzt war.
Jakob nutzt **kein** eigenes API-Key — alle LLM-Calls laufen ueber
Claude Code Subscription. Deshalb wurden die Direct-Call-Pfade entfernt.

Stattdessen spawnen die Worker jetzt einen AgentTask vom Typ
`<step>_run`. Der Operator-Subagent waehlt das Template, der
Sub-Subagent fuehrt den Skill via Claude Code Subscription aus und
persistiert das Ergebnis ueber die folgenden API-Endpunkte:

| Worker | task_type | Persist-Endpoint |
|---|---|---|
| expose_parser_runner | `expose_parser_run` | `POST /api/property/{id}/expose-parse-result` |
| mietlisten_runner | `mietlisten_parser_run` | `PUT /api/property/{id}/rental-units` |
| unterlagen_analyst_runner | `unterlagen_analyst_run` | `POST /api/property/{id}/due-diligence-report` |
| dokument_klassifizierer | `dokument_klassifizierer_run` | `POST /api/document/{id}/classification-result` |
| marktanalyse_runner | `marktanalyse_run` | `POST /api/region/{id}/market-analysis-result` |
| risiko_scanner_runner | `risiko_scanner_run` | `POST /api/property/{id}/risk-scan-result` |
| **T093b PDF-OCR-Pipeline** (horizontal, von T093/T098/T099/T100 gespawnt wenn pdfplumber Bild-PDF erkennt) | `pdf_vision_ocr` | `POST /api/document/{id}/ocr-result` |
