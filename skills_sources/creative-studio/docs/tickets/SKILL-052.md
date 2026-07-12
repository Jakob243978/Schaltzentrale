# SKILL-052: creative-studio — Ad-Library-Scan-Modul + Longevity-Score (Proxy, kein Spend)

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Must
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_meta-ad-library-zugriff-budget.md` (§1 Felder, §2 Proxy-Signale/Longevity-Score, §3 Scan-Ablauf, §4 Andockung, §6 MoSCoW Must)

> [!info] Herkunft (Recherche 2026-06-24, empirischer MCP-Test)
> `mcp__claude_ai_Meta__ads_library_search` funktioniert read-only und liefert echte aktuelle DE-Ads. Das
> Modul macht aus Einzelabfragen einen **reproduzierbaren Wettbewerbs-Scan**: Themen-Sweep → Top-Advertiser →
> Page-Drilldown → **Longevity-Score** → Tabelle + Hook-Muster. Output = Winning-Hooks/Angles als
> Briefing-Parameter fuer die Creative-Generierung.

> [!important] Ehrlichkeit (kein Silent-Fake) — Pflicht im Modul vermerken
> **Kommerzieller Spend/Impressions/Reach ist NICHT abrufbar** (weder MCP-Payload noch offizielle Public API;
> Spend-Ranges nur fuer politische/Issue-Ads). Es gibt **nur Proxy-Signale** (Longevity, Creative-
> Multiplikation, Re-Serving). Der Longevity-Score ist eine **Priorisierung fuer manuelle Sichtung**, keine
> Budget-Wahrheit — Grenzen-Disclaimer ist Pflicht-Output.

## Was soll erreicht werden? (Business-Ziel)
Ein reproduzierbares Ad-Library-Scan-Modul: aus Thema/Page-ID(s) eine Tabelle aktiver Ads
(Advertiser | Hook | aktiv seit | #Varianten | Longevity-Score | Snapshot-Link) + eine Hook-/Angle-Muster-
Liste als Inspirationspool fuer die Creative-Generierung — auf Basis der real zurueckkommenden MCP-Felder.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein Themen-Sweep (`search_terms`, `countries`, `ad_active_status="ACTIVE"`) laeuft,
      the system shall `estimated_total_count` + die mehrfach auftauchenden Top-Advertiser-Pages extrahieren.
- [ ] **EARS-2:** When ein Page-Drilldown (`page_ids`, `ad_active_status="ALL"`) laeuft, the system shall pro
      Ad die real verfuegbaren Felder erfassen (`id`, `page_name`, `ad_creative_link_title` als Hook,
      `ad_creation_time`, `ad_delivery_start_time`, `ad_snapshot_url`) — **kein** erfundenes Spend-Feld.
- [ ] **EARS-3:** When der Longevity-Score berechnet wird, the system shall die fixierte Heuristik
      `score = aktive_Tage(creation→heute) × log(1 + Anzahl_aktiver_Varianten_der_Page)` anwenden und absteigend
      sortieren. → Test `test_longevity_score_formula`.
- [ ] **EARS-4:** When ein Scan-Ergebnis ausgegeben wird, the system shall eine **Tabelle aktiver Ads** + eine
      **Hook-/Angle-Muster-Liste** liefern UND den **Grenzen-Disclaimer** (kein Spend abrufbar, nur Proxy)
      sichtbar mit ausgeben. → Tests `test_scan_table_and_hooks`, `test_disclaimer_present`.
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall Thema/
      Page-IDs/Land als Eingabe nehmen (Default Land DE) — kein hartkodierter Projekt-/Wettbewerber-Wert.
      → Test `test_scan_project_neutral`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `creative_studio/ad_library_scan.py` — Funktionen `theme_sweep()`,
  `page_drilldown()`, `longevity_score()`, `extract_hook_patterns()`, `scan_report()`. Die MCP-Aufrufe
  selbst laufen ueber den Agenten (`ads_library_search`); das Modul stellt die **Parsing-/Score-/Report-
  Logik** bereit + dokumentiert den Ablauf (testbar gegen gespeicherte MCP-Beispiel-Payloads).
- **Verworfene Alternative:** Spend/EU-Reach als Score-Eingang nutzen — verworfen, weil empirisch **nicht im
  Payload** (§1). Nur Proxy-Signale. Kein Bulk-Scraping (Tool-Policy, §3 Legal).
- **Betroffene Module:** `creative_studio/ad_library_scan.py` (neu), SKILL.md (Scan-Runbook-Abschnitt),
  neue Testdatei mit gespeicherten Beispiel-Payloads. → Architektur-Weiche: keine (ADR n/a).

## Technische Hinweise
- `surface: backend`. `longevity_score`/`extract_hook_patterns`/Parsing sind **reine Funktionen** → gegen
  fixe Beispiel-Payloads (aus der Recherche §1) unit-testbar, ohne Live-MCP.
- Longevity nur ueber `creation_time` + aktuellem `delivery_start` + ACTIVE-Status annaehern (kein
  `delivery_stop_time` im Payload, §1).
- Legal: nur **Inspiration** (Hook-/Angle-Muster), kein 1:1-Kopieren von Creatives/Claims, kein Bulk-Scraping.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/ad_library_scan.py` (neu) — Sweep/Drilldown/Score/Report.
- `skills_sources/creative-studio/SKILL.md` — Ad-Library-Scan-Abschnitt (Ablauf + Disclaimer).
- `skills_sources/creative-studio/tests/test_skill_052_ad_library_scan.py` (neu) — Beispiel-Payloads.
- Wissensgrundlage: `2026-06-24_meta-ad-library-zugriff-budget.md` (§1, §2, §3, §4, §6 Must).

## Ergebnis / Notizen

**Implementiert 2026-06-24 (Status spec -> review).**

### Gebaute Files
- `skills_sources/creative-studio/creative_studio/ad_library.py` (neu) — Parsing/Score/
  Aggregation/Report. Funktionen: `parse_ad`/`parse_ads`, `theme_sweep` (EARS-1),
  `longevity_score` (EARS-3), `aggregate_by_page`, `extract_hook_patterns`,
  `scan_report` + `render_report_markdown` (EARS-2/4), `display_hook` (Multi-Card-Dedup).
  `PROXY_DISCLAIMER` als Pflicht-Output, `DEFAULT_COUNTRY="DE"` (EARS-5).
- `skills_sources/creative-studio/templates/ad_library_scan.md` (neu) — Runbook
  (Seed-Thema -> MCP-Call(e) -> Modul -> Output) inkl. Proxy-Disclaimer + Legal.
- `skills_sources/creative-studio/SKILL.md` — neuer Abschnitt 9 "Ad-Library-Scan".
- `skills_sources/creative-studio/tests/test_skill_052_ad_library.py` (neu) — 22 Tests
  mit Fixture-Payloads aus Research §1 (JinTo/PIOLA/KI-Weiterbildungszentrum).

### Longevity-Score-Formel (fixiert, Research §2)
`score = aktive_Tage(creation -> heute) * log(1 + Anzahl_aktiver_Varianten_der_Page)`
- `active_days`: Tage seit `ad_creation_time` (kein stop_time im Payload), >= 0, Zukunft -> 0.
- `page_variant_count`: Ads derselben Page im Scan; log(1+n) -> Einzel-Ad-Boden log(2).

### Done-Kriterien (EARS -> Test)
- EARS-1 (Sweep: total_count + Top-Advertiser) -> `test_ears1_theme_sweep_*` ✅
- EARS-2 (nur reale Felder, kein Spend) -> `test_ears2_parse_only_real_fields`,
  `test_ears2_re_serving_detection` ✅
- EARS-3 (Formel + absteigende Sortierung) -> `test_longevity_score_formula`,
  `test_ears3_rows_sorted_descending`, `test_ears3_active_days_uses_creation` ✅
- EARS-4 (Tabelle + Hooks + Disclaimer) -> `test_scan_table_and_hooks`,
  `test_disclaimer_present`, `test_page_aggregation` ✅
- EARS-5 (projektneutral, Default DE) -> `test_scan_project_neutral` ✅
- Edge-Cases (fehlende Felder, ISO-Daten, Zukunfts-Datum, Multi-Card-Dedup) abgedeckt.

### Verifikation
- `pytest tests/ -q` -> **180 passed** (Baseline 158 + 22 neue).
- **Echter MCP-Test gemacht** (read-only, 1 Abfrage `ads_library_search`,
  "KI Automatisierung Unternehmen", DE, ACTIVE): Feldshape bestaetigt (`ads`-Key,
  `page_id` als int, Multi-Card-`" | "`-Titel). Modul lief sauber gegen den echten
  Payload (`theme_sweep` -> JinTo als Top-Advertiser; `render_report_markdown` -> Tabelle
  + Hooks + Disclaimer). Real-Daten-Befund "page_id als int / `ads`-Key / `" | "`-Karten"
  ist im Modul defensiv abgedeckt (`str(...)`, `data`/`ads`-Fallback, `display_hook`).

### Offen / Should (nicht in diesem Ticket)
- Snapshot-Anreicherung (Top-N `ad_snapshot_url` oeffnen, Volltext/Visual/EU-Reach-Band)
  = Research §6 Should, eigenes Ticket.
- Persistente Hook-/Angle-Bibliothek im Vault (Should).
- Verify-Report (`/sdd-verify SKILL-052`) noch ausstehend vor `done`.
