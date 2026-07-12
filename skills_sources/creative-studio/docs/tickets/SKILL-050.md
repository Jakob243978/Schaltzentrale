# SKILL-050: creative-studio — PAA/SERP-API-Helper (Tier 1) + YouTube-Autocomplete-Fetcher

**Status:** spec
**Erstellt:** 2026-06-24
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_content-market-research-methodik.md` (§2.4 PAA/SERP-APIs, §2.5 YouTube-Autocomplete, §3 Stufe 1, §6 MoSCoW Should)

> [!info] Herkunft (Recherche 2026-06-24)
> Tier 1 des Recherche-Ablaufs (SKILL-049) ergaenzt die WebSearch-Stufe um zwei guenstige, gut
> automatisierbare Bausteine: **strukturierte PAA/SERP-Features** via Serper (2.500 Gratis-Suchen/Mon) oder
> DataForSEO (~6 USD/10k), und **YouTube-Autocomplete** (Suggest-Endpoint, gratis, kein Key). Beide liefern
> Frage-Intent + Format-/Hook-Signale als JSON, das ins Roh-Signal des Recherche-Ablaufs merged.

## Was soll erreicht werden? (Business-Ziel)
Ein optionaler `research.py`-Helper, der bei Tier 1 PAA + verwandte Queries strukturiert (Serper/DataForSEO)
zieht und die YouTube-Autocomplete-Suggests zu einem Seed gratis abfragt — beide als JSON ins Roh-Signal des
Content-Marktrecherche-Ablaufs (SKILL-049). API-Key kommt aus Env, nie hartkodiert.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When der Helper mit `--tier 1` + Seed aufgerufen wird, the system shall PAA + verwandte
      Queries strukturiert via Serper **oder** DataForSEO ziehen und als JSON zurueckgeben. → Test (gemockte API) `test_paa_serp_json`.
- [ ] **EARS-2:** When der YouTube-Autocomplete-Fetcher mit einem Seed aufgerufen wird, the system shall die
      Suggest-Daten **ohne API-Key** strukturiert zurueckgeben. → Test (gemockt) `test_youtube_autocomplete`.
- [ ] **EARS-3:** When ein API-Key fehlt/ungueltig ist, the system shall **nicht crashen**, sondern auf Tier 0
      zurueckfallen + eine klare Warnung ausgeben (kein Silent-Fail). → Test `test_missing_key_falls_back`.
- [ ] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall den
      Provider-Key **aus Env** (`branding.env`-Pattern / Umgebungsvariable) beziehen — kein Key im Code,
      kein Projektwert. → Test `test_key_from_env_not_hardcoded`.
- [ ] **EARS-5:** When PAA-/Autocomplete-Daten zurueckkommen, the system shall sie ins Roh-Signal-JSON-Format
      des Recherche-Ablaufs (SKILL-049) mergebar liefern (gleiche Eintrag-Struktur Quelle+Datum). → Test `test_merge_into_raw_signal`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `creative_studio/research.py` mit zwei Funktionen: `fetch_paa_serp(seed, provider,
  key)` (HTTP gegen Serper/DataForSEO) und `fetch_youtube_autocomplete(seed)` (oeffentlicher Suggest-
  Endpoint, kein Key). Beide geben normalisierte JSON-Eintraege (Quelle+Datum) zurueck. Key via Env.
- **Verworfene Alternative:** Ubersuggest/SEMrush/Ahrefs-API einbinden — verworfen (teurer, fuer die Nische
  Overkill; §2.3). Tier-1-Default bleibt Serper-Free + DataForSEO-PAYG.
- **Betroffene Module:** `creative_studio/research.py` (neu), referenziert vom SKILL-049-Runbook (Tier 1).

## Technische Hinweise
- `surface: backend`. HTTP-Requests gegen externe APIs — Key aus Env, `-UserAgent` setzen (Provider lehnen
  „Browser"-lose Requests teils ab; vgl. `feedback_powershell_http_scripts`). Tests mocken die HTTP-Calls.
- **Kosten-Hinweis:** Serper Free-Tier 2.500/Mon; DataForSEO PAYG ~6 USD/10k — kein neuer Dauer-Vertrag,
  Owner entscheidet ueber Aktivierung (Tier-1-Schalter). Helper macht ohne Key/`--tier 1` nichts.
- Voraussetzung: SKILL-049 (Runbook), in das die Tier-1-Signale fliessen.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/research.py` (neu) — PAA/SERP + YouTube-Autocomplete.
- `skills_sources/creative-studio/SKILL.md` — Tier-1-Hinweis im Recherche-Abschnitt (SKILL-049).
- `skills_sources/creative-studio/tests/test_skill_050_research.py` (neu).
- Wissensgrundlage: `2026-06-24_content-market-research-methodik.md` (§2.4, §2.5, §3 Stufe 1, §6 Should).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
