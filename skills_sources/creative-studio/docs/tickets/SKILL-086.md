# SKILL-086: creative-studio — Methoden-Tagging im Output (Bild UND Video)

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (framework-Feld + Dateiname + Sidecar/props + Tests)
**surface:** backend
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** framework_ablesbar_aus_jedem_artefakt (variant_id + Dateiname + Metadaten) +
bild_und_video_abgedeckt + default_beibehalten_fuer_bestand + kein_bestandsbruch

## Kontext / Root-Cause
Um Ads spaeter nach Copy-Methode tracken zu koennen, muss das verwendete Framework
**durchgaengig im Output** vermerkt sein. Der Reel-Pfad trug `framework` bereits im
`variant_id` (SKILL-045). Der **Bild-Einzelpfad** (`render_image.main`) dagegen fuehrte
gar kein Framework: Dateiname war `<ad_id>__<format>.png`, keine Sidecar-Metadaten. Auch
in den Reel-`props` fehlte ein **explizites** `framework`-Feld (nur positional im variant_id).

## Was soll erreicht werden?
Das Framework ist aus jedem Artefakt eindeutig ablesbar — fuer Bild UND Video —
im variant_id/utm_content, im Dateinamen und als explizites Metadaten-Feld. Bestehendes
Verhalten ohne Framework bleibt unveraendert (Default beibehalten).

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Bild-Datenmodell]:** `AdContent` hat ein `framework`-Feld (Default
      `"default"`) — additiv, Bestands-Aufrufer brechen nicht. *(Test `test_adcontent_has_framework_field_default`.)*
- [x] **EARS-2 [Must, Bild-Dateiname]:** `render_image.image_output_stem` traegt den
      (slugifizierten) Framework-Key im PNG-Namen, sobald ein nicht-Default-Framework gesetzt
      ist (`<ad_id>__<framework>__<format>`); bei Default bleibt `<ad_id>__<format>` unveraendert.
      *(Tests `test_image_filename_carries_framework_when_set`, `test_image_filename_unchanged_for_default_framework`.)*
- [x] **EARS-3 [Must, Bild-Metadaten]:** `render()` schreibt je PNG ein Sidecar `<name>.json`
      mit explizitem `framework`-Feld + variant_id/utm_content (SKILL-024); `build_image_meta`
      ist die reine Datenfunktion. `write_meta=False` unterdrueckt den Sidecar (batch fuehrt
      manifest.json). *(Tests `test_image_meta_*`.)*
- [x] **EARS-4 [Must, Video-Metadaten]:** `reel_spec_to_props` liefert ein explizites
      `framework`-Feld (zusaetzlich zu variant_id/utm_content). *(Tests `test_reel_props_*`.)*
- [x] **EARS-5 [Must, Batch-Konsistenz]:** batch reicht `framework` ins `AdContent` und
      fuehrt es weiterhin in variant_id (Dateiname) + manifest.json; Suite gruen (SKILL-023).
- [x] **EARS-6 [Must, nicht-brechend]:** Default-Renders (ohne Framework) erzeugen denselben
      Dateinamen wie bisher; ganze Suite gruen.

## Loesungs-Skizze
- `specs.py`: `AdContent.framework` (Default `"default"`).
- `render_image.py`: `DEFAULT_FRAMEWORK`, `image_output_stem`, `build_image_meta`,
  `render(..., write_meta=True)` (Sidecar), CLI `--framework`.
- `batch.py`: `framework` ins `_content_from_variant`, `render(..., write_meta=False)`.
- `reel_spec.py`: `props["framework"] = spec.framework`.
- `tests/test_skill_086_framework_tagging.py`; SKILL.md Tagging-Konvention.

## Test-Ergebnis / Beleg
- **Suite gruen:** `python -m pytest -q` -> **349 passed**.
- Beispiel Bild: `acme__mindset-shift__feed_4x5.png` + `.json` (`"framework": "mindset_shift"`).
- Beispiel Reel: `props["framework"] = "heros_journey"`, variantId `acme__heros-journey-h00__story-9x16`.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` (`AdContent`)
- `skills_sources/creative-studio/creative_studio/render_image.py`
- `skills_sources/creative-studio/creative_studio/batch.py`
- `skills_sources/creative-studio/creative_studio/reel_spec.py`
- `skills_sources/creative-studio/tests/test_skill_086_framework_tagging.py`
