# SKILL-023: creative-studio — Batch-/Varianten-Engine (N Hooks × M Formate × Medientyp) + manifest.json

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Must
**Geschaetzter Aufwand:** L
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** varianten_pro_lauf (≥ N Hooks × M Formate in einem Aufruf statt 1 Creative) + manifest_als_bruecke_zu_dco_und_reporting_genutzt (SKILL-031/033)
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_creative-studio-flow-improvements.md` (§1.1 Template-API-Systeme, §2.2 Hook-Varianten, §3.1 Batch-/Varianten-Engine — Kern-Luecke; MoSCoW-Liste #1 = Must)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> Die zentrale Luecke des heutigen Skills: er ist ein **Single-Creative-Renderer** (1 Variante × N Formate),
> kein **Pipeline-/Varianten-System**. Der Industrie-Standard (Bannerbear/Placid/Creatomate) ist
> „Template einmal designen → per Datenzeile dynamisch befuellen"; Creative-Testing braucht
> **viele Varianten aus einer Quelle** (1 Core-Body × 5–10 Hooks). Dieses Ticket ist die **Kern-Klammer**
> fuer DCO-Export (SKILL-031) und Reporting-Rueckkanal (SKILL-033).

## Was soll erreicht werden? (Business-Ziel)
Aus **einer** Job-Definition (`job.yaml`/Input) erzeugt der Skill in **einem Lauf** alle Kombinationen aus
**N Hooks × M Formate × Medientyp (Bild/Video)** und schreibt ein **`manifest.json`**, das je Variante
`variant_id`, `framework`, `hook`, `format`, Dateipfad und `utm_content` festhaelt. Das Manifest ist die
universelle Schnittstelle zu DCO-Upload und Performance-Rueckkanal — ohne projekt-spezifischen Code.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When eine Job-Datei (`job.yaml`/JSON) mit einer Liste von Content-Varianten
      (headline/subline/cta/hook/framework) × Formaten × Medientyp uebergeben wird, the system shall in
      **einem Lauf** alle Kombinationen rendern (kein manueller Aufruf je Variante).
      → `run_batch` iteriert Varianten × Formate; Test `test_batch_renders_n_times_m` (6 = 3×2).
- [x] **EARS-2:** When der Batch-Lauf abgeschlossen ist, the system shall ein **`manifest.json`** schreiben,
      das je erzeugter Datei `variant_id`, `framework`, `hook`, `format`, `medium` (image|video),
      relativen Dateipfad und `utm_content` enthaelt.
      → Feld heisst `media` (image|video); Tests `test_manifest_written_with_fields`,
      `test_manifest_variant_ids_unique`.
- [x] **EARS-3:** When im Job Bild- UND Video-Varianten gemischt sind, the system shall beide Medientypen
      ueber dieselbe Job-/Manifest-Struktur erzeugen (Bild via `render_image.py`, Video via `video/`-Modul).
      → Image voll implementiert; Video-Eintraege werden in derselben Struktur als
      `status: not_implemented` (TODO `video/`-Modul) markiert — **nicht gefaked**. Test
      `test_mixed_media_video_marked`.
- [x] **EARS-4 [multi-projekt]:** When der Skill in unterschiedlichen Projekten laeuft, the system shall
      Brand + Content + Formate **ausschliesslich** aus Job-Datei/Config beziehen — kein hartkodierter
      Projektwert/Pfad in der Batch-Engine (Vision-Prinzip 1).
      → Brand via `--brand-env`/`brand_env`/`brand_json`, ad_id aus Job; Test `test_no_hardcoded_project_value`.
- [x] **EARS-5:** When eine einzelne Variante beim Rendern fehlschlaegt, the system shall die uebrigen
      Varianten weiter erzeugen und den Fehler je Variante im Manifest/Log markieren (kein Abbruch des
      ganzen Laufs).
      → try/except je Render mit `entry["error"]`; Test `test_single_failure_does_not_abort`.
- [x] **EARS-6:** When kein expliziter Output-Pfad angegeben ist, the system shall den projekt-lokalen
      Marketing-Ordner (SKILL-022-Konvention) als Job-Wurzel verwenden und das Manifest dort ablegen.
      → Manifest landet immer im uebergebenen `--out` (Default `out`); Test `test_manifest_lands_in_out_dir`.
      Hinweis: die SKILL-022-Marketing-Ordner-Auflösung als Default-Wurzel ist als Folge-Ausbaustufe offen
      (heute expliziter `--out` bzw. Default `out/`).

## Technische Hinweise
- **Neuer Einstiegspunkt** `creative_studio/batch.py` (oder `render_batch.py`): liest `job.yaml`, iteriert
  Varianten × Formate × Medium, ruft den jeweiligen Renderer auf, sammelt das Manifest.
- **`variant_id`/`utm_content`** kommen aus der zentralen Systematik von **SKILL-024** (`specs.py`) — dieses
  Ticket konsumiert sie, definiert sie nicht selbst.
- **Job-Schema** projektneutral halten (Liste von `AdContent`-aehnlichen Dicts + Format-Keys aus `specs.py`
  + `medium`). Beispiel-`job.yaml` als Template beilegen.
- **Manifest** ist Vertrag fuer SKILL-030 (Galerie liest es), SKILL-031 (DCO-Bundle) und SKILL-033
  (Insights-Rueckkanal). Felder additiv erweiterbar halten.
- Abhaengigkeit: SKILL-024 (Naming) sollte parallel/zuerst stehen.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/batch.py` — **neu** (Batch-/Varianten-Engine + Manifest-Writer,
  CLI `python -m creative_studio.batch --job <yaml> --out <dir> [--brand-env <pfad>]`).
- `skills_sources/creative-studio/creative_studio/specs.py` — `make_variant_id`/`make_utm_content` (aus SKILL-024).
- `skills_sources/creative-studio/creative_studio/render_image.py` — Bild-Renderer (`render()` je Variante; unveraendert).
- `skills_sources/creative-studio/video/` — Video-Renderer (TODO im batch.py markiert, noch nicht angebunden).
- `skills_sources/creative-studio/examples/job_h1-immo.yaml` — **neu** (Job-Schema-Vorlage + Real-Test-Input).
- `skills_sources/creative-studio/tests/test_skill_023_batch.py` — Tests (1 EARS = mind. 1 Test).
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_creative-studio-flow-improvements.md` (§3.1).

## Ergebnis / Notizen
**Implementiert 2026-06-24.** Neue `batch.py`:
- `load_job(path)` liest `job.yaml` (PyYAML; YAML ist JSON-Superset → JSON-Jobs ebenso).
- `run_batch(job, out_dir, brand_env_override, debug_safe)` rendert alle Kombinationen Variante×Format
  über `render_image.render(...)`, vergibt `variant_id`+`utm_content` aus `specs.py` (SKILL-024), benennt
  jede Datei auf `<variant_id>.png` (eindeutig je Hook) und schreibt `manifest.json`.
- Brand-Auflösung: `--brand-env` (CLI) > `job.brand_env`; `job.brand_json` (inline) überschreibt einzelne Tokens.
- `AdContent.warnings()` je Variante → Log (`[WARN]`) und, falls vorhanden, additiv ins Manifest (`warnings`).
- Robustheit: einzelner Render-Fehler bricht den Lauf nicht ab (`entry["error"]`), unbekannte Formate werden
  mit `[WARN]` übersprungen.
- Video: bewusst **nicht gefaked** — Mixed-Media-Jobs erzeugen Video-Einträge mit `status: not_implemented`
  + `note` (TODO `video/`-Remotion-Modul), `file=None`.

Bestehende Signaturen unverändert (`render`, `load_branding`, `AdContent`, `specs`-API).

**Test-Ergebnis:** `pytest tests/ -q` → **35 passed** (gesamt; `test_skill_023_batch.py` 8 Tests grün).

**Real-Test-Beleg (echter Playwright-Lauf, in Temp-Out, nicht committet):**
Input `examples/job_h1-immo.yaml` (3 Hooks bab/pas/aida × 2 Formate feed_4x5/story_9x16),
brand-env = `AgentischesArbeiten/.../branding.env` (BRAND_NAME=JAKSE-Automations).
→ **6 PNGs** (208–289 KB, echt gerendert) + `manifest.json` mit `count: 6`, 6 eindeutigen `variant_id`:
```
h1-immo__bab-h00__feed-4x5     utm=h1-immo-feed-4x5-bab-h00
h1-immo__bab-h00__story-9x16   utm=h1-immo-story-9x16-bab-h00
h1-immo__pas-h01__feed-4x5     utm=h1-immo-feed-4x5-pas-h01
h1-immo__pas-h01__story-9x16   utm=h1-immo-story-9x16-pas-h01
h1-immo__aida-h02__feed-4x5    utm=h1-immo-feed-4x5-aida-h02
h1-immo__aida-h02__story-9x16  utm=h1-immo-story-9x16-aida-h02
```
