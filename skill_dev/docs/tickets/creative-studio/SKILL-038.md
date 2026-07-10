# SKILL-038: creative-studio — UTM-Naming-Standard als Konstanten + pytest (specs.py)

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** naming_drift_verhindert (pytest schuetzt UTM-/Makro-Schema: lowercase, nur `-` statisch, Makros in {{...}}, utm_content==make_utm_content, keine Dup-Keys)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_utm-tracking-skill.md` (§1 Meta-Makros, §4 UTM-Naming-Standard, §6 Vorschlag 3)

> [!info] Herkunft (Recherche 2026-06-24 + Owner-Wunsch)
> Owner-Wunsch: **maximales Tracking** — zu jedem Lead spaeter wissen, von welcher Ad/Plattform/Placement er
> kam. Damit das UTM-/Makro-Schema nicht driftet (case-sensitive GA4/DB, gemischte Trenner, falsche
> Makro-Syntax), werden die Naming-Defaults als dokumentierte Konstanten in `specs.py` verankert und per
> pytest abgesichert — analog `tests/test_skill_024_variant_id.py`.

## Was soll erreicht werden? (Business-Ziel)
Den UTM-Naming-Standard als **dokumentierte Konstanten** (`UTM_*`-Defaults + `META_MACROS`-Tabelle) in
`specs.py` fixieren und mit einem pytest gegen Naming-Drift schuetzen. Sichert Konsistenz von SKILL-036/037
und verhindert, dass spaetere Aenderungen das Schema still brechen.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When `specs.py` geladen wird, the system shall die UTM-Defaults als Konstanten bereitstellen
      (`UTM_SOURCE_DEFAULT="meta"`, `UTM_MEDIUM_DEFAULT="paid-social"`) + eine `META_MACROS`-Tabelle, die die
      acht unterstuetzten Makros der `{{...}}`-Syntax dokumentiert.
      → Tests `test_utm_default_constants`, `test_meta_macros_table`.
- [x] **EARS-2:** When `make_url_tags`/`make_link_url` (SKILL-036) die Defaults brauchen, the system shall
      **diese** Konstanten nutzen (eine Definition, kein Literal-Duplikat in den Funktionen).
      → Signatur-Defaults = `UTM_SOURCE_DEFAULT`/`UTM_MEDIUM_DEFAULT`, Makros aus `META_MACROS[...]`.
- [x] **EARS-3:** When der pytest laeuft, the system shall pruefen, dass die statischen UTM-Werte **lowercase**
      sind und **nur `-`** als Trenner nutzen (kein `_`-Mix). → Test `test_url_tags_static_values_hygienic`.
- [x] **EARS-4:** When der pytest laeuft, the system shall pruefen, dass die dynamischen Makros exakt in
      `{{...}}`-Syntax stehen und nur die acht offiziell unterstuetzten Makros verwendet werden.
      → Tests `test_meta_macros_table`, `test_url_tags_dynamic_macros`.
- [x] **EARS-5:** When der pytest laeuft, the system shall pruefen, dass `utm_content == make_utm_content(vid)`
      im erzeugten Parameter-String ist und **keine doppelten Param-Keys** vorkommen.
      → Tests `test_url_tags_utm_content_is_join_key`, `test_url_tags_no_duplicate_keys`.
- [x] **EARS-6 [multi-projekt]:** When der pytest laeuft, the system shall pruefen, dass kein hartkodierter
      Projekt-/Brand-Wert in den Defaults steckt (Source/Medium projektneutral, Campaign kommt als Arg).
      → Test `test_url_tags_project_neutral`.

## Technische Hinweise
- In `specs.py` die Konstanten direkt am SKILL-036-Block verankern (eine Single-Source-Stelle), damit
  `make_url_tags` sie referenziert statt Literale.
- `META_MACROS` als dokumentierte Tabelle (Makro → kurze Bedeutung), inkl. Hinweis, dass `.name`-Makros
  bruechig sind (eingefroren auf Veroeffentlichungszeitpunkt) → `.id`-Makros bevorzugen (§1 der Recherche).
- Testdatei spiegelt das Muster von `tests/test_skill_024_variant_id.py` (1 EARS = mind. 1 Test).
- Reine Konstanten + Tests, keine Verhaltensaenderung an SKILL-036-Funktionen (additiv).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — Konstanten `UTM_SOURCE_DEFAULT`,
  `UTM_MEDIUM_DEFAULT`, `META_MACROS` (Block `# SKILL-038`); referenziert von SKILL-036-Funktionen.
- `skills_sources/creative-studio/tests/test_skill_038_url_tags.py` (neu) — analog `test_skill_024_variant_id.py`.
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-24_utm-tracking-skill.md` (§1, §4, §6 Vorschlag 3).

## Ergebnis / Notizen
**Implementiert 2026-06-24** (gemeinsam mit SKILL-036). In `specs.py` (Block `# === SKILL-038 ===`):
- `UTM_SOURCE_DEFAULT = "meta"`, `UTM_MEDIUM_DEFAULT = "paid-social"` — projektneutrale Defaults.
- `META_MACROS: dict[str, str]` — die **acht** offiziell unterstuetzten Meta-Makros (`ad.id`, `ad.name`,
  `adset.id`, `adset.name`, `campaign.id`, `campaign.name`, `placement`, `site_source_name`) in exakter
  `{{...}}`-Syntax, je mit Kommentar zur Stabilitaet (`.id` stabil, `.name` eingefroren/bruechig).
- `make_url_tags`/`make_link_url` (SKILL-036) referenzieren diese Konstanten als Signatur-Defaults bzw.
  `META_MACROS["placement"]` etc. — kein Literal-Duplikat.

**Test:** `tests/test_skill_038_url_tags.py` (11 Tests, deckt SKILL-036 + SKILL-038 gemeinsam ab, Muster aus
`test_skill_024_variant_id.py`). Prueft: Konstanten-Werte, vollstaendige Makro-Tabelle in `{{...}}`-Syntax
(nur die acht), statische Werte lowercase + nur `-` (auch bei gemischter Eingabe `Meta`/`Paid_Social`/
`Warteliste 2026/Q3`), `utm_content == make_utm_content(vid)`, keine doppelten Param-Keys,
`utm_campaign`-Pflicht, Projektneutralitaet, `make_link_url`-Separator + Fragment-Erhalt.

**Test-Ergebnis:** `pytest tests/ -q` → **138 passed** (vorher 127; +11 neu).

**Offen (Verify-Gate):** Verify-Report fehlt → Status `review` (kein `done` ohne Report). `setup.ps1`-Deploy
nach `~/.claude/skills/` noch faellig.
