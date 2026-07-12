# SKILL-024: creative-studio — Variant-ID- & UTM-Systematik in specs.py (Single Source fuer Naming)

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Must
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** variant_id_im_insights_pull_wiederauffindbar (utm_content matcht `ads_insights_*`) + naming_single_source (keine divergierenden Namensschemata zwischen Batch/DCO/Reporting)
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_creative-studio-flow-improvements.md` (§2.5 Naming/UTM-Taxonomie, §3.3 A/B-Namens-+UTM-Systematik; MoSCoW-Liste #2 = Must)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> Ohne deterministische, eindeutige Namensgebung ist kein Rueckkanal moeglich: dieselbe Variant-/
> Ad-Konvention, die der Skill vergibt, **muss** im Meta-Insights-Pull (`ads_insights_*`) wiederauffindbar
> sein — sonst kein Performance-Loop. UTM-Best-Practice: positional, lowercase, keine Sonderzeichen/Leerzeichen;
> fuer Creative-Varianten ist `utm_content` der A/B-Hebel (z. B. `hook01-bab__feed4x5`).

## Was soll erreicht werden? (Business-Ziel)
Eine **zentrale, deterministische** Variant-ID- und `utm_content`-Systematik in `specs.py`, die jede
gerenderte Variante eindeutig benennt und die im spaeteren Insights-Pull (`ads_insights_*`) 1:1
wiedergefunden werden kann. Single Source fuer alle Naming-Entscheidungen — Batch-Engine (SKILL-023),
DCO-Export (SKILL-031) und Reporting (SKILL-033) erben sie, definieren sie nicht selbst.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When eine Variante aus (ad_id, hook, framework, format) gebildet wird, the system shall
      eine **deterministische, eindeutige** `variant_id` erzeugen (gleiche Eingabe → gleiche ID,
      kollisionsfrei bei unterschiedlicher Eingabe).
      → `make_variant_id`; Tests `test_variant_id_deterministic`, `test_variant_id_unique_per_input`.
- [x] **EARS-2:** When eine `variant_id` erzeugt wird, the system shall daraus ein `utm_content` nach
      festem Schema ableiten (positional, **lowercase**, keine Sonderzeichen/Leerzeichen, z. B.
      `hook01-bab__feed4x5`).
      → `make_utm_content` (Schema `<ad_id>-<format>-<framework>-h<NN>`); Tests `test_utm_content_schema`,
      `test_utm_content_deterministic`.
- [x] **EARS-3:** When ein Eingabe-String unzulaessige Zeichen enthaelt, the system shall ihn deterministisch
      normalisieren (slugify: lowercase, `_`/`-` statt Leerzeichen/Sonderzeichen) — keine stille Verkettung
      kollidierender IDs.
      → `slugify` (Umlaut-Translit, leerer Token → `x`); Test `test_slugify_normalizes_special_chars`.
- [x] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall das
      Naming-Schema projektneutral halten (Projekt-Praefix kommt als Parameter `ad_id`, kein hartkodierter
      Projektwert in `specs.py`).
      → Test `test_project_prefix_comes_from_ad_id`.
- [x] **EARS-5:** When Batch-Engine/DCO-Export/Reporting eine ID brauchen, the system shall **dieselben**
      `specs.py`-Funktionen aufrufen (eine Definition, kein Parallel-Schema in anderen Modulen).
      → `batch.py` importiert `make_variant_id`/`make_utm_content` aus `specs`; Test
      `test_single_source_functions_importable_from_specs`.

## Technische Hinweise
- In `specs.py` ergaenzen: `def make_variant_id(ad_id, hook, framework, fmt_key) -> str` +
  `def make_utm_content(variant_id) -> str` + ein internes `slugify(...)`-Helfer. Frozen/rein-funktional.
- Schema-Konvention dokumentieren (Docstring + kurzer Kommentar): positional `hook-framework__format`,
  lowercase, `__`-Trenner zwischen Inhalts- und Format-Teil.
- Keine Runtime-Insights-Abfrage hier — nur die **Namens-Erzeugung**. Der Abgleich gegen `ads_insights_*`
  liegt in SKILL-033.
- Reihenfolge: dieses Ticket ist Voraussetzung fuer SKILL-023 (Manifest braucht die IDs).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — neue Funktionen `make_variant_id`,
  `make_utm_content`, `slugify` (Naming-Single-Source, Block `# === SKILL-024 ===`).
- `skills_sources/creative-studio/creative_studio/batch.py` — Konsument (SKILL-023), importiert die Funktionen.
- `skills_sources/creative-studio/tests/test_skill_024_variant_id.py` — Tests (1 EARS = mind. 1 Test).
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_creative-studio-flow-improvements.md` (§2.5, §3.3).

## Ergebnis / Notizen
**Implementiert 2026-06-24.** In `specs.py` (rein-funktional, frozen):
- `slugify(value)` — lowercase, Umlaut-Translit (ae/oe/ue/ss), alle uebrigen Sonderzeichen/Leerzeichen → `-`,
  Trim, leerer Token → `x` (nie kollidierende Leer-Verkettung).
- `make_variant_id(ad_id, hook, framework, fmt_key, hook_index=None)` — Schema
  `<ad_id>__<framework>-h<NN>__<format>`. Eindeutigkeit ueber 2-stelligen nullbasierten `hook_index`
  (Position im Job); Fallback ohne Index = slugifizierter Hook-Text.
- `make_utm_content(variant_id)` — leitet positional `<ad_id>-<format>-<framework>-h<NN>` ab,
  lowercase, nur `[a-z0-9-]`; im Meta-Insights-Pull (`ads_insights_*`) wiederauffindbar.

**Single Source** bestaetigt: `batch.py` definiert kein eigenes Schema, sondern importiert die drei
Funktionen aus `specs`. Keine bestehende Signatur gebrochen (`AdFormat`, `FORMATS`, `AdContent`,
`get_format`, Constants unveraendert).

**Test-Ergebnis:** `pytest tests/ -q` → **35 passed** (gesamt; davon `test_skill_024_variant_id.py` grün).

**Real-Test-Beleg (echte Werte aus Batch-Lauf, h1-immo, brand-env JAKSE-Automations):**
6 eindeutige `variant_id` / `utm_content`:
| variant_id | utm_content |
|---|---|
| h1-immo__bab-h00__feed-4x5 | h1-immo-feed-4x5-bab-h00 |
| h1-immo__bab-h00__story-9x16 | h1-immo-story-9x16-bab-h00 |
| h1-immo__pas-h01__feed-4x5 | h1-immo-feed-4x5-pas-h01 |
| h1-immo__pas-h01__story-9x16 | h1-immo-story-9x16-pas-h01 |
| h1-immo__aida-h02__feed-4x5 | h1-immo-feed-4x5-aida-h02 |
| h1-immo__aida-h02__story-9x16 | h1-immo-story-9x16-aida-h02 |
