# SKILL-036: creative-studio — make_url_tags() (+ make_link_url-Fallback) in specs.py (UTM + Meta-Makros als Single Source)

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Must
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** url_tags_string_join_bar (utm_content matcht make_utm_content + dynamische Makros in {{...}}-Syntax fuer Plattform/Placement/Ad-Join) + naming_single_source (kein Parallel-Schema neben SKILL-024)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_utm-tracking-skill.md` (§1 Meta-Makros, §2 url_tags vs. Query, §4 UTM-Naming, §6 Vorschlag 1)

> [!info] Herkunft (Recherche 2026-06-24 + Owner-Wunsch)
> Owner-Wunsch: **maximales Tracking** — zu jedem Lead spaeter wissen, von **welcher Ad / welcher Plattform /
> welchem Placement** er kam. Der Skill setzt heute nur statische UTM (`utm_source`/`utm_campaign`/`utm_content`)
> ohne `utm_medium`, ohne dynamische Meta-Makros und ohne `url_tags`-Pfad — damit ist die Plattform-/
> Placement-Ebene **nicht** join-bar. Genau diese Luecke schliesst das Ticket. `make_utm_content(vid)`
> (SKILL-024) bleibt 1:1 der stabile Join-Key zwischen Lead-Capture (LP/CRM) und Meta-Insights (`ads_insights_*`).

## Was soll erreicht werden? (Business-Ziel)
Eine **zentrale, deterministische** Funktion `make_url_tags()` in `specs.py`, die aus `variant_id` +
Kampagnen-Kontext den **fertigen URL-Parameter-String** baut: statische UTM **kombiniert mit** Metas
dynamischen Makros. Plus ein Helper `make_link_url(base_url, ...)` als Fallback (alles in die `link_url`).
Single Source fuer alle UTM-/Makro-Entscheidungen — Batch-Engine (SKILL-037) erbt sie, definiert sie nicht selbst.
Projektneutral: Source/Medium/Campaign kommen als Parameter mit Defaults rein, kein hartkodierter Projektwert.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When `make_url_tags(variant_id, utm_campaign, ...)` aufgerufen wird, the system shall einen
      Query-String-Teil (ohne fuehrendes `?`) erzeugen, der die **statischen** UTM
      `utm_source=meta`, `utm_medium=paid-social`, `utm_campaign=<arg>`, `utm_content=make_utm_content(variant_id)`
      enthaelt. → Test `test_url_tags_static_utms`.
- [x] **EARS-2:** When `make_url_tags(...)` aufgerufen wird, the system shall zusaetzlich die **dynamischen**
      Meta-Makros `utm_term={{placement}}`, `utm_platform={{site_source_name}}`, `ad_id={{ad.id}}`,
      `cmp_id={{campaign.id}}` in exakt der `{{...}}`-Syntax anhaengen (zur Laufzeit von Meta gefuellt).
      → Test `test_url_tags_dynamic_macros`.
- [x] **EARS-3:** When `utm_content` gesetzt wird, the system shall es **1:1** aus `make_utm_content(variant_id)`
      ableiten (kein paralleles Naming) — der Join-Key bleibt identisch zu SKILL-024.
      → Test `test_url_tags_utm_content_is_join_key`.
- [x] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall
      `utm_source`/`utm_medium`/`utm_campaign` als **Parameter** annehmen (Defaults `meta`/`paid-social`,
      `utm_campaign` Pflicht-Arg) — kein hartkodierter Projekt-/Brand-Wert in `specs.py`.
      → Tests `test_url_tags_campaign_required`, `test_url_tags_project_neutral`.
- [x] **EARS-5:** When `make_link_url(base_url, variant_id, ...)` aufgerufen wird, the system shall die nackte
      LP-URL korrekt mit demselben Parameter-Set verbinden (`?` bzw. `&` je nach vorhandenem Query) — als
      Fallback, wenn `url_tags` am Ad-Objekt nicht setzbar ist (SKILL-037).
      → Tests `test_link_url_query_separator`, `test_link_url_preserves_fragment`.
- [x] **EARS-6:** When der Parameter-String erzeugt wird, the system shall ihn hygienisch halten: statische
      Werte lowercase + nur `-` als Trenner, keine doppelten Param-Keys, keine PII.
      → Tests `test_url_tags_static_values_hygienic`, `test_url_tags_no_duplicate_keys`.

## Technische Hinweise
- In `specs.py` ergaenzen: `def make_url_tags(variant_id, *, utm_campaign, utm_source="meta",
  utm_medium="paid-social") -> str` + `def make_link_url(base_url, variant_id, *, utm_campaign, ...) -> str`.
  Rein-funktional, keine Runtime-/Netzwerk-Logik.
- Makro-Werte (`{{placement}}` etc.) **nicht** url-encoden — Meta erwartet die rohe `{{...}}`-Syntax; das
  Encoding der eingefuellten Werte macht Meta zur Laufzeit. Statische Werte hingegen sauber halten.
- `utm_source` bleibt **stabil `meta`** (nicht `fb`/`ig` — sonst Doppel-Pflege); die feine Plattform-
  Aufloesung kommt aus `utm_platform={{site_source_name}}` (§4.1 der Recherche).
- `{{placement}}` bewusst in `utm_term`, **nicht** in `utm_medium` (Klartext mit Leerzeichen wuerde das
  GA4-Channel-Grouping verschmutzen, §1 Hygiene-Falle).
- `fbclid`/`fbc`/`_fbp` sind **NICHT** Aufgabe dieser Funktion (Scope B / LP, §3 der Recherche) — der Skill
  setzt ausschliesslich UTM + Makros.
- Reihenfolge: dieses Ticket ist Voraussetzung fuer SKILL-037 (Ad-Anlegen + Manifest brauchen den String).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — neue Funktionen `make_url_tags`,
  `make_link_url` (Block `# === SKILL-036 ===`); nutzt bestehendes `make_utm_content` (SKILL-024).
- `skills_sources/creative-studio/creative_studio/batch.py` — Konsument (SKILL-037).
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-24_utm-tracking-skill.md` (§1, §2, §4, §6 Vorschlag 1).

## Ergebnis / Notizen
**Implementiert 2026-06-24.** In `specs.py` (rein-funktional, additiv, keine bestehende Signatur gebrochen):
- `make_url_tags(variant_id, *, utm_campaign, utm_source="meta", utm_medium="paid-social") -> str` — baut den
  `url_tags`-Query-String (ohne fuehrendes `?`). Statische UTM werden slugifiziert (lowercase, nur `[a-z0-9-]`),
  die vier Meta-Makros bleiben **roh** in `{{...}}` (Meta encodet zur Laufzeit). `utm_campaign` ist Pflicht
  (leer/whitespace → `ValueError`). `utm_content` = 1:1 `make_utm_content(variant_id)` (SKILL-024-Join-Key).
- `make_link_url(base_url, variant_id, *, utm_campaign, ...) -> str` — Fallback: haengt denselben Param-Satz
  an die nackte LP-URL, waehlt `?`/`&` je nach vorhandenem Query, ein `#fragment` bleibt am Ende erhalten.

Die UTM-Defaults (`UTM_SOURCE_DEFAULT`/`UTM_MEDIUM_DEFAULT`/`META_MACROS`) kommen als Konstanten aus dem
SKILL-038-Block (gemeinsam implementiert) — keine Literal-Duplikate in den Funktionen.

**Real-Test-Beleg (echte Werte, h1-immo / bab / feed_4x5 / hook_index=0):**
- `variant_id` = `h1-immo__bab-h00__feed-4x5`
- `url_tags`   = `utm_source=meta&utm_medium=paid-social&utm_campaign=warteliste-2026q3&utm_content=h1-immo-feed-4x5-bab-h00&utm_term={{placement}}&utm_platform={{site_source_name}}&ad_id={{ad.id}}&cmp_id={{campaign.id}}`
- `link_url`   = `https://jakse.de/warteliste?` + obigem String

**Test-Ergebnis:** `pytest tests/ -q` → **138 passed** (vorher 127; +11 in `tests/test_skill_038_url_tags.py`,
das SKILL-036 + SKILL-038 gemeinsam abdeckt). EARS-1..6 je >= 1 Test.

**Offen (Verify-Gate):** Verify-Report `docs/tickets/creative-studio/verify/SKILL-036-verify-*.md` fehlt noch
→ Status bleibt `review` (kein `done` ohne Report). Deploy nach `~/.claude/skills/` via `setup.ps1` noch faellig.
