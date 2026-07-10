# SKILL-077: creative-studio — 4-Typen-Ad-Satz als Default + KEYLESS Stock-Quelle (Openverse)

**Status:** review
**Erstellt:** 2026-07-09
**MoSCoW:** Must
**Geschaetzter Aufwand:** M (neue keyless Bildquelle + Resolver-Rewire + zwei SKILL.md-Konventionen)
**surface:** backend
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`
**outcome_metric:** vier_bildtypen_pro_adsatz_default (jedes Ad-Set erzeugt per Default Text-only +
eigene Fotos + Stock + KI, jeweils in allen 3 Formaten) + stock_typ_keyless_verfuegbar (Bild-Typ 3
laeuft ohne API-Key/User-Setup) + kein_bestandsbruch (additive Erweiterung; `library`/`generate`
unveraendert)
**outcome_review_at:** null
**Wissensgrundlage:** Live-Use-Feedback Jakob (2026-07-09): Fuer JEDE Ad-Kampagne sollen
standardmaessig **vier Bild-Typen parallel** zum A/B-Testen entstehen — (1) nur Text, (2) eigene
Fotos/Brand-Assets, (3) **Stock-Fotos**, (4) KI-generiert (Magnific). **Typ 3 (Stock) fehlte in der
Praxis komplett**, weil keine benutzbare Stock-Quelle angebunden war: der `stock`-Pfad haengte am
Magnific-Key (`stock_search`/`stock_download` → `load_key()`), war also **kein** setup-freier Default.

## Root-Cause (warum der Stock-Typ nie entstand)
Der `--bg-source stock`-Zweig in `resolve_bg()` rief `k = key or load_key()` **vor** der Fallunter-
scheidung und dann `stock_search(query, k, …)` (Magnific) — d.h. **jeder** Stock-Zug brauchte einen
Magnific-Key. Ohne gesetzten Key warf `load_key()` und der ganze Stock-Typ fiel weg. Fuer einen
Ad-Satz, in dem Stock einer von vier **Default**-Typen sein soll, ist ein Key-Zwang ein De-facto-
Blocker (kein „keyless, kein Setup"). Zweitens gab es in der `SKILL.md` **keine** verankerte Regel
„immer alle vier Bild-Typen" — analog zur `SKILL-076`-Regel „immer alle drei Formate" fehlte das
Typ-Pendant, also blieb der 4-Typen-Satz Auslegungssache und Typ 3/4 wurden weggelassen.

## Was soll erreicht werden? (Business-Ziel)
1. **Keyless Stock:** `--bg-source stock` liefert ein echtes, kommerziell nutzbares Stock-Foto
   **ohne** API-Key/User-Setup — ueber **Openverse** (`api.openverse.org`, CC, Filter
   `license_type=commercial`). Optionaler Qualitaets-Upgrade via kostenlosem `PEXELS_API_KEY`.
2. **4-Typen-Konvention:** die `SKILL.md` verankert als Soll/Default: pro Ad-Set **alle vier**
   Bild-Typen (Text-only / eigene Fotos / Stock / KI), jeder in allen drei Formaten; Abweichung nur
   auf ausdruecklichen Wunsch.

## Recherche: welche keyless Stock-API?
- **Openverse** (gewaehlt, Default): **keyless** (anonyme Requests, nur `page_size ≤ 20`),
  aggregiert 800M+ CC-Werke (Flickr/StockSnap/Wikimedia u.a.), Filter `license_type=commercial`
  liefert nur kommerziell verwendbare Lizenzen (CC0/CC-BY/CC-BY-SA/PDM). Response traegt
  `url`, `license`, `license_version`, `license_url`, `creator`, `attribution`, `foreign_landing_url`,
  `tags`, `width/height` → reicht fuer ehrliche Herkunft im Index. **Nachteil:** Qualitaet/Kuration
  schwanken (viele Fotos nur ~960px breit, Motiv-Treffer variabel).
- **Pexels / Unsplash:** kuratierter/hochaufloesender, aber **brauchen einen (kostenlosen) API-Key**
  → widerspricht „kein User-Setup". Daher: **Openverse = keyless Default**, **Pexels = optionaler
  Premium-Upgrade** ueber `PEXELS_API_KEY` (wenn gesetzt, bevorzugt; sonst Openverse).
- **Empfehlung an [J]:** Fuer bessere Stock-Qualitaet einen **kostenlosen `PEXELS_API_KEY`**
  (pexels.com/api, Gratis-Tier ~200 Req/h) in die Projekt-`.env` legen — dann greift automatisch
  der Pexels-Pfad, ohne dass am Skill etwas geaendert werden muss. Unsplash waere die Alternative
  (Demo-Tier 50 Req/h), aber ein Key genuegt.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1 [Must, keyless]:** When `--bg-source stock` **ohne** Magnific-Key aufgerufen wird,
      the system shall trotzdem ein Stock-Foto ueber Openverse liefern (`load_key()` wird fuer den
      Stock-Pfad **nicht** aufgerufen). *(Test `test_resolve_bg_stock_is_keyless`.)*
- [x] **EARS-2 [Must, ehrliche Lizenz]:** the system shall jeden Stock-Eintrag mit
      `source=openverse|pexels`, `license_type`, `license_url`, `attribution`, `creator`,
      `foreign_landing_url` **und** `is_ai_generated=False` im `index.json` fuehren — nie als KI
      getarnt, **kein** Disclosure-Label (echtes Foto). *(Test `test_openverse_download_persists_honest_license`.)*
- [x] **EARS-3 [Should, Pexels optional]:** If `PEXELS_API_KEY` gesetzt ist, the system shall Pexels
      bevorzugen und bei Pexels-Fehler/kein-Treffer ehrlich auf Openverse zurueckfallen; ohne Key
      direkt Openverse. *(Test `test_resolve_stock_free_prefers_pexels_when_key`.)*
- [x] **EARS-4 [Should, People-Heuristik]:** When `no_people` aktiv ist, the system shall
      personen-getaggte Openverse-Treffer nach hinten sortieren (Openverse hat keinen harten
      People-Filter — best effort). *(Test `test_openverse_search_deprioritizes_people`.)*
- [x] **EARS-5 [Must, Lizenz-Gate bleibt]:** the system shall das bestehende
      `license_type`/`license_url`-Pflicht-Gate (SKILL-073) auch fuer Stock-Eintraege erzwingen.
      *(Test `test_stock_entries_pass_license_gate`.)*
- [x] **EARS-6 [Must, 4-Typen-Konvention]:** the system (`SKILL.md`) shall die Regel „pro Ad-Set
      **immer alle vier** Bild-Typen (Text-only / eigene Fotos / Stock / KI), jeder in allen drei
      Formaten; Abweichung nur auf ausdruecklichen Wunsch" explizit verankern.
- [x] **EARS-7 [Must, nicht-brechend]:** the system shall rueckwaerts-kompatibel bleiben —
      `--bg-source none/library/generate` unveraendert, keine Signatur geaendert, der Magnific-
      Stock-Pfad (`stock_search`/`stock_download`) bleibt als optionale Premium-Quelle im Modul.
      *(Bestehende SKILL-073-Suite gruen.)*

## Loesungs-Skizze (Approach)
- **`image_source.py`:** neue keyless Sektion — `openverse_search()` (keyless GET,
  `license_type=commercial`, `category=photograph`, `page_size ≤ 20`, aspect-first-dann-ohne,
  People-Deprioritisierung), `openverse_download()` (Download + Index mit CC-Lizenz/Attribution/
  Quelle), `pexels_search()`/`pexels_download()` (optional, key-gated), `resolve_stock_free()`
  (Pexels-bevorzugt-sonst-Openverse). `resolve_bg()` `stock`-Zweig ruft jetzt `resolve_stock_free()`
  **ohne** `load_key()`; `load_key()` bleibt nur im `generate`-Zweig. Lizenz-Helper `_cc_license_type`/
  `_cc_license_url`, People-Heuristik `_openverse_has_people`. Neuer CLI-Subcommand `stock-free`.
- **`SKILL.md`:** (1) neuer `[!important]`-Kasten in Abschnitt 2 „Standard-Ad-Satz = alle VIER
  Bild-Typen" (Mapping Typ→Aufruf, jeder in allen 3 Formaten); (2) Abschnitt 13 auf „Keyless Stock +
  KI-Gen" umgeschrieben — `stock` = Openverse keyless, Pexels optional, ehrliche Lizenz im Index,
  CC-BY-Attribution-Etikette-Hinweis, `stock-free`-CLI.
- **Tests:** `tests/test_skill_077_stock_openverse.py` — 8 Offline-Tests (HTTP gemockt), decken
  EARS-1..5 ab.
- **Verworfen:** Pexels/Unsplash als Default (Key-Zwang widerspricht „kein User-Setup"); den
  Magnific-Stock-Pfad ersatzlos loeschen (bleibt als Premium-Option erhalten → additiv/nicht-brechend).

## Test-Ergebnis / Beleg
- **Suite gruen:** `python -m pytest -q` → **284 passed** (277 vorher + 8 neue − … ; alle inkl.
  bestehender SKILL-073-Suite gruen). `test_skill_077_stock_openverse.py` = 8 passed.
- **Live keyless (echt, 2026-07-09):** `image_source stock-free "team working laptop office"` →
  Openverse-Treffer (Flickr/StockSnap), Download eines **CC0**-Fotos nach `stock/openverse_*.jpg`,
  Index-Eintrag `source=openverse`, `license_type="CC0 1.0 (Public Domain)"`,
  `license_url=creativecommons.org/publicdomain/zero/1.0/`, `is_ai_generated=false`. Kein Key gesetzt.
- **Deploy:** `skills_sources/creative-studio/` → `~/.claude/skills/creative-studio/` (robocopy /MIR);
  `resolve_stock_free` + Openverse-Code in der deployten Kopie vorhanden.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/image_source.py` — Openverse/Pexels-Sektion,
  `resolve_stock_free`, `resolve_bg`-stock-Rewire (keyless), CLI `stock-free`.
- `skills_sources/creative-studio/SKILL.md` — Abschnitt 2 (4-Typen-Kasten), Abschnitt 13 (Keyless
  Stock).
- `skills_sources/creative-studio/tests/test_skill_077_stock_openverse.py` — Offline-Tests.

## Ergebnis / Notizen
**Status review (2026-07-09).** Root-Cause = Stock-Pfad key-gebunden (kein keyless Default) + fehlende
4-Typen-Pflicht in SKILL.md. Openverse als keyless Default angebunden (CC, kommerziell), Pexels als
optionaler `PEXELS_API_KEY`-Upgrade, ehrliche Herkunft/Lizenz im Index, `resolve_bg`-stock ohne
`load_key()`. 4-Typen-Konvention in SKILL.md verankert. Additiv/nicht-brechend. 284 Tests gruen.
Deploy nach `~/.claude/skills/creative-studio/` erfolgt.

**Offen / [J]:** optional kostenlosen `PEXELS_API_KEY` in die Projekt-`.env` legen (bessere
Stock-Qualitaet, kein Skill-Change noetig); Verify-Pass (frische Session) + Outcome-Review (>=14 Tage).
