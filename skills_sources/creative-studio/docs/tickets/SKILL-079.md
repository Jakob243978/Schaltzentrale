# SKILL-079: creative-studio — Reel-Pfad zentral an die Brand anbinden

**Status:** review
**Erstellt:** 2026-07-11
**MoSCoW:** Must
**Geschaetzter Aufwand:** S (Loader reused resolve_brand; Merge + Praezedenz + Tests)
**surface:** backend
**Vision-Prinzip:** `config-zentral-entkoppeln`
**outcome_metric:** eine_brand_datei_bilder_und_reels (branding.env aendern -> Bild-Ads UND Reels
folgen) + kein_doppel_schema (Reuse render_image.resolve_brand) + spec_brand_bleibt_override

## Kontext / Root-Cause
Beim Bild-Pfad zieht `render_image.resolve_brand` die Brand-Tokens zentral aus `brand.json`/
`branding.env` (SKILL-029). Der **Reel-Pfad** dagegen trug die Brand ausschliesslich im `brand`-Block
**jeder** Spec — eine zentrale Brand-Aenderung schlug NICHT auf Reels durch. Das widerspricht Jakobs
Prinzip „Config zentral entkoppeln" (ADR-010 / branding.env als Single Source).

## Was soll erreicht werden?
Der Reel-Loader laedt Brand-Tokens aus derselben zentralen Quelle wie der Bild-Pfad; der `brand`-Block
in der Spec wird zum optionalen **Override**. Kein zweites Brand-Schema.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, zentrale Quelle]:** `reel_spec.resolve_central_reel_brand(brand_env=, brand_json=)`
      liefert Reel-Tokens (name/accent/bg/bgSoft/ink/inkMuted/font) via **`render_image.resolve_brand`**
      (kein Neu-Erfinden) + SKILL-057-Caption-Tokens (highlight/captionFont/captionBgAlpha) aus
      derselben Datei. *(Test `test_central_brand_from_branding_env`.)*
- [x] **EARS-2 [Must, Reel folgt zentral]:** `load_reel_spec(spec, brand_env=/brand_json=)` legt die
      zentrale Brand als Basis unter die Spec; eine Spec **ohne** brand-Block rendert mit der zentralen
      Marke. *(Test `test_reel_follows_central_brand_without_spec_brand`.)*
- [x] **EARS-3 [Must, Praezedenz]:** Spec-brand > zentrale brand.json/branding.env > Defaults —
      ueberschriebene Tokens gewinnen aus der Spec, nicht ueberschriebene bleiben zentral.
      *(Test `test_spec_brand_overrides_central`.)*
- [x] **EARS-4 [Must, Name-Pflicht bleibt]:** liefert weder Spec noch zentrale Quelle einen `name` ->
      `ReelSpecError` (kein namenloses Reel). *(Test `test_missing_name_everywhere_errors`.)*
- [x] **EARS-5 [Must, nicht-brechend]:** Specs mit eigenem brand-Block (Bestand) laufen unveraendert;
      SKILL-045-Suite gruen. CLI `reel_spec` bekommt `--brand-env`/`--brand-json` (optional).

## Loesungs-Skizze
- `creative_studio/reel_spec.py`: `resolve_central_reel_brand`, `_read_caption_extras` (SKILL-057-Keys
  aus derselben Datei), `parse_reel_spec(data, central_brand=)` mit Merge (Spec gewinnt),
  `load_reel_spec(..., brand_env=, brand_json=)`, CLI-Args `--brand-env`/`--brand-json`.
- Kern-Tokens ueber `render_image.resolve_brand` (Import lokal, Zyklus-frei).
- SKILL.md Abschnitt 4c (zentrale Reel-Brand + Praezedenz).

## Test-Ergebnis / Beleg
- **Suite gruen:** `python -m pytest -q` -> **295 passed**.
- **Live-Beleg:** die zwei neuen AgentischesArbeiten-Reels wurden mit `--brand-env
  terraform/base-dev/build/customization/branding.env` gebaut (zentrale Brand, minimaler Spec-Override
  nur fuer die editorial-Serif `font`).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/reel_spec.py`
- `skills_sources/creative-studio/tests/test_skill_078_broll_message.py` (Aufgabe-B-Teil, EARS-B1..B4)
- `skills_sources/creative-studio/SKILL.md` (Abschnitt 4c)
