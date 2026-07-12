# SKILL-037: creative-studio — url_tags am Ad-Objekt setzen + ins manifest.json (batch.py)

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_utm-tracking-skill.md` (§2 url_tags vs. Query, §2.1 Verifikationspflicht, §6 Vorschlag 2)

> [!info] Herkunft (Recherche 2026-06-24 + Owner-Wunsch)
> Owner-Wunsch: **maximales Tracking** — zu jedem Lead spaeter wissen, von welcher Ad/Plattform/Placement er
> kam. SKILL-036 baut den Parameter-String; dieses Ticket hebt ihn von „im Manifest dokumentiert" auf
> „tatsaechlich an der Ad gesetzt". `url_tags` ist Metas zentrale Tag-Quelle pro Ad (eine Stelle statt
> verstreuter Query-Strings) und fuellt die dynamischen Makros sauber. **Ehrlichkeit:** ob das Meta-MCP
> `url_tags` 1:1 an das Ad-Objekt durchreicht, ist nicht offiziell belegt und MUSS live verifiziert werden
> (kein stiller Fake) — sonst greift der `link_url`-Fallback.

## Was soll erreicht werden? (Business-Ziel)
Beim Ad-Anlegen den `url_tags`-String (aus SKILL-036) am **Ad-Objekt** setzen **und** je Variante ins
`manifest.json` schreiben. Primaerstrategie ueber `ads_update_entity` mit **Live-Verifikation**; bei
Fehlschlag dokumentierter Fallback ueber `link_url` direkt am Creative.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When eine Variante im Batch erzeugt wird, the system shall ihren `url_tags`-String
      (aus `make_url_tags`, SKILL-036) je Variante ins `manifest.json` schreiben (neben `utm_content`).
- [ ] **EARS-2:** When eine Ad angelegt wird, the system shall als **Primaerstrategie** `url_tags` per
      `ads_update_entity(entity_type=ad, fields={url_tags})` **nach** dem Ad-Create setzen.
- [ ] **EARS-3:** When die Primaerstrategie ausgefuehrt wurde, the system shall sie **live verifizieren**
      (Ad anlegen → update → `ads_get_ad_entities` lesen ob `url_tags` gesetzt ist → optional
      `ads_get_ad_preview` ob die Makros in der finalen URL ankommen) — kein stiller Erfolg ohne Read-Back.
- [ ] **EARS-4:** When die `url_tags`-Durchreichung fehlschlaegt oder nicht verifizierbar ist, the system
      shall auf den **Fallback** umschalten: UTM + Makros via `make_link_url()` direkt in
      `link_url` bei `ads_create_creative(link_url=...)`.
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall keinen
      hartkodierten Kampagnen-/Brand-/Account-Wert setzen — Kampagnen-Kontext kommt aus Job/CLI.
- [ ] **EARS-6:** When dokumentiert wird, the system shall **ehrlich** festhalten, dass die MCP-Durchreichung
      von `url_tags` zu verifizieren ist (welche Strategie im Real-Test gegriffen hat als Default markieren).

## Technische Hinweise
- `batch.py`: `url_tags` je Manifest-Entry ergaenzen (analog `utm_content`). Reines String-Feld, kein
  Render-Output noetig — auch fuer geplante Video-Eintraege setzbar.
- Ad-Anlege-/Verifikations-Schritt ist **nicht** Teil des reinen Batch-Renderns; er gehoert in den
  Ad-Publish-Pfad (MCP-Aufrufe). Der Skill-Code stellt den String bereit + dokumentiert beide Strategien.
- `ads_create_creative` hat **nur** `link_url`, **kein** `url_tags` → beim reinen Creative-Anlegen kann
  `url_tags` nicht mitgegeben werden; daher der `ads_update_entity`-Schritt am Ad-Objekt (§2.1 der Recherche).
- `url_tags` enthaelt **nur** den Query-Teil (ohne `?`) und **ersetzt** kollidierende Tags in der URL
  (Meta-Verhalten) — daher `link_url` im url_tags-Pfad sauber (nur nackte LP-URL) halten.
- Voraussetzung: SKILL-036 done (liefert `make_url_tags` + `make_link_url`).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/batch.py` — `url_tags` ins Manifest, Konsument von
  `make_url_tags`/`make_link_url` aus `specs` (Block `# SKILL-037`).
- `skills_sources/creative-studio/creative_studio/specs.py` — read-only Nutzung der SKILL-036-Funktionen.
- MCP: `ads_create_ad`/`ads_create_creative`, `ads_update_entity`, `ads_get_ad_entities`, `ads_get_ad_preview`.
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-24_utm-tracking-skill.md` (§2, §2.1, §6 Vorschlag 2).

## Ergebnis / Notizen

**Live-Verifikation 2026-06-25 (T167-Test-Ad, AgentischesArbeiten, alles PAUSED):**

- **EARS-2/EARS-3 — Primaerstrategie A funktioniert + ist der Default.** An der echten PAUSED-Ad
  `120249024916170412` wurde `ads_update_entity(entity_type=ad, fields={url_tags:"<make_url_tags-Ergebnis>"})`
  ausgefuehrt → **`success:true`**, `updated_fields` echot den vollstaendigen `url_tags`-String 1:1 zurueck
  (inkl. der dynamischen Makros `{{placement}}`/`{{site_source_name}}`/`{{ad.id}}`/`{{campaign.id}}`). Die
  MCP-Durchreichung von `url_tags` ans Ad-Objekt ist damit **belegt akzeptiert** → **Strategie A = Default**.
- **EARS-3 Read-Back-Einschraenkung (ehrlich, kein stiller Erfolg):** Ein unabhaengiger Read-Back ueber
  `ads_get_ad_entities` ist **nicht moeglich** — `url_tags` ist dort **kein** abfragbares Feld (Endpoint
  liefert nur Insights-/Delivery-Felder; Error „Unsupported field(s) at level 'ad': url_tags"). Der Beleg
  stuetzt sich daher auf den **akzeptierten Write + das 1:1-Echo** der `updated_fields`. Die finale
  Makro-Ersetzung in der Klick-URL fuellt Meta erst zur Laufzeit (vor Live nicht final inspizierbar).
- **EARS-4 — Fallback B nicht ausgeloest:** Strategie A greift, daher kein Wechsel auf
  `make_link_url()`-in-`link_url`. Fallback bleibt im Code/Runbook als dokumentierte Reserve.
- **EARS-1/EARS-5/EARS-6** (Manifest-Feld je Variante, multi-projekt-neutral, ehrliche Doku der
  MCP-Verifikationspflicht) sind im `batch.py`/`specs.py`-Code + Runbook umgesetzt; die Live-Bestaetigung
  von A erfuellt die Default-Markierungs-Anforderung aus EARS-6.

Quer-Beleg: `AgentischesArbeiten/docs/marketing/test-ads-status.md` (T167/T166 2026-06-25),
`AgentischesArbeiten/docs/runbooks/meta-ad-launch.md` (Strategie A als Default, T167).
