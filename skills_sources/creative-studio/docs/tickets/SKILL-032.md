# SKILL-032: creative-studio — content-aware smartcrop fuer --bg-image (loest EARS-6 aus SKILL-020)

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Could
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`
**outcome_metric:** foto_hintergruende_verlustarm_in_alle_formate (Saliency + Face-Detection statt blind cover) + ears6_aus_skill_020_geschlossen
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_creative-studio-flow-improvements.md` (§1.4 Content-aware Crop / Saliency, §3.8 smartcrop; MoSCoW-Liste #7)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> Bekannte offene Luecke: SKILL-020 EARS-6 (content-aware Crop) ist heute nur CSS `cover` — bei Ratio-Wechsel
> (4:5 ↔ 9:16 ↔ 1:1) wird blind skaliert, der Bildinhalt kann beschnitten werden. Auto-Crop-Stand-der-Technik
> nutzt **Saliency Detection** (Attention-Map) und/oder **Face/Object-Detection**, um den Focal Point zu
> finden. Open-Source: `smartcrop-py`. Dies ist die direkte Rueckfuehrung der EARS-6-Live-Luecke.

## Was soll erreicht werden? (Business-Ziel)
Foto-Hintergruende (`--bg-image`) verlustarm in alle Zielformate croppen: ein `smartcrop`-Schritt
(Saliency + optionale Face-Detection) **vor** dem CSS-Compositing, der je Ziel-Ratio so croppt, dass das
Wichtige im Bild bleibt — statt zu verzerren oder blind `cover`-zu-skalieren. Schliesst die offene EARS-6
aus SKILL-020.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When ein `--bg-image` im falschen Ratio vorliegt, the system shall es content-aware croppen
      (`smartcrop-py`/Saliency) statt zu verzerren oder blind `cover`-zu-skalieren.
- [x] **EARS-2:** When das Hintergrundbild ein Gesicht enthaelt, the system shall (optionale) Face-Detection
      nutzen, um das Gesicht im sichtbaren Bereich zu halten.
- [x] **EARS-3:** When fuer mehrere Formate gecroppt wird, the system shall je Format einen eigenen,
      Focal-Point-treuen Crop erzeugen (4:5, 9:16, 1:1 aus einer Quelle).
- [x] **EARS-4:** When `smartcrop`/Detection-Abhaengigkeiten fehlen, the system shall auf den bisherigen
      `cover`-Pfad zurueckfallen und das per Warnung kenntlich machen (kein harter Abbruch).
- [x] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall den
      Crop-Schritt parameter-/config-getrieben halten (kein projekt-spezifischer Bildpfad im Skill).

## Technische Hinweise
- `creative_studio/smartcrop_step.py`: `smartcrop-py` (Saliency) + optional Face-Detection; Crop **vor** dem
  HTML/CSS-Compositing in `render_image.py`. Recherche §1.4/§3.8 nennt Tooling (smartcrop-py; YOLO/DETR fuer
  Faces optional).
- Greift SKILL-020 EARS-6 direkt auf — beim Abschluss dort EARS-6 abhaken/verlinken.
- Bewusst Could/idea: Erst-Ads nutzen Brand-Gradient statt Foto; relevant sobald Foto-Hintergruende kommen.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/smartcrop_step.py` — **neu** (Saliency-/Face-Crop vor Compositing).
- `skills_sources/creative-studio/creative_studio/render_image.py` — Crop-Schritt vor dem Playwright-Render.
- `skills_sources/creative-studio/creative_studio/specs.py` — Ziel-Format-Maße fuer den Crop.
- Bezug: SKILL-020 EARS-6 (offene Luecke).
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_creative-studio-flow-improvements.md` (§1.4, §3.8).

## Ergebnis / Notizen

**Status review (2026-06-24).** Content-aware Smartcrop additiv implementiert; SKILL-020 EARS-6 geschlossen.

**Was implementiert:**
- **Neu `creative_studio/cropping.py`** — `crop_to_format(image_path, fmt, out_path, *, use_smartcrop=True, quality=88) -> CropResult`.
  Croppt ein Foto content-aware auf das Ziel-Ratio von `AdFormat` (width/height) und skaliert exakt auf die
  Zielmaße — ohne Verzerrung. Dreistufige Focal-Point-Wahl mit klarer `method`-Markierung:
  1. `method="face"` (EARS-2): OpenCV-Haar-Cascade erkennt Gesicht(er) -> Mittelpunkt des groessten Gesichts
     wird Focal-Point. Hat Vorrang vor reiner Saliency (verhinderte im Real-Test das Abschneiden des Kopfes).
  2. `method="smartcrop"` (EARS-1): `smartcrop`-Lib (Saliency + Kanten + Hautton) liefert den Focal-Point.
  3. `method="fallback-center"` (EARS-4): ohne smartcrop/OpenCV -> ratio-korrekter, oben-gewichteter Crop,
     per stderr-Warnung markiert (kein Hard-Fail, kein stiller Fake).
  Schluessel-Detail: Aus dem Focal-Point wird stets die **maximale** ratio-korrekte Box gebaut
  (`_maximal_ratio_box`, eine Kante == Originalkante) -> volle Aufloesung, kein unnoetiges Upscaling
  (SKILL-035-Mindestkanten-Lehre). `CropResult.upscaled` markiert ehrlich, wenn die Quelle das Zielformat
  nicht ohne Hochskalieren deckt.
- **`creative_studio/render_image.py` (additiv, nicht-brechend):** neuer Helper `_bg_image_for_format(...)` +
  Param `render(..., smartcrop_bg: bool = True)` + CLI-Flag `--no-smartcrop`. Bei lokalem `bg_image` wird pro
  Format ein ratio-korrektes Crop in `<out>/_bg_crops/` erzeugt und statt des Originals ins Template gegeben
  (per `dataclasses.replace`, keine Mutation des content). Remote/data-URIs, fehlende Dateien und jeder
  Crop-Fehler -> Original-`bg_image` (Template faellt auf `cover` zurueck). Ohne `bg_image` bzw. mit
  `smartcrop_bg=False` exakt das alte Verhalten. `render()`-Signatur backward-kompatibel (neuer Kwarg mit
  Default) — `batch.py` haengt unveraendert dran.
- Libs installiert: `smartcrop` 0.5.0 + `opencv-python-headless` 4.13 (Pillow 12.2 war da). Beide optional
  via Import-Guard — fehlen sie, greift sauber der Fallback (EARS-4).

**Test-Ergebnis:** `pytest tests/test_skill_032_smartcrop.py -q` -> **12 passed** (1 EARS = >=1 Test):
EARS-1 (Ratio/keine Verzerrung + smartcrop-Pfad volle Aufloesung), EARS-2 (Face bleibt im Crop, `method="face"`),
EARS-3 (9:16+4:5+1:1 je exakte Zielmaße/Ratio aus einer Quelle), EARS-4 (erzwungener Fallback markiert + Box
ratio-korrekt), plus Determinismus (identische Crop-Box + Bytes), kein-Upscaling-bei-grosser-Quelle, maximal-Box-Klemmung.

**Real-Test** (Header `00_header_4000x2667_sRGB.jpg`, Crops nur in Temp, nicht im Repo):
| Format | Zielmaße | Crop-Box (Original) | method | faces | upscaled | Datei |
|---|---|---|---|---|---|---|
| story_9x16 | 1080x1920 | (1578,0,3078,2667) | face | 1 | False | ~248 KB |
| feed_4x5   | 1080x1350 | (1262,0,3396,2667) | face | 1 | False | ~161 KB |
| square_1x1 | 1080x1080 | (995,0,3662,2667)  | face | 1 | False | ~124 KB |
Visuell geprueft: in allen drei Formaten ist die sitzende Person mit vollstaendigem, zentriertem Kopf im Bild —
kein Gesicht abgeschnitten. (Reiner smartcrop-Pfad hatte den Kopf im 9:16 noch abgeschnitten, weil er die
texturierte Wand hoeher als die Person scorte — die Face-Priority loest genau das.)

**Code-Referenzen:**
- `skills_sources/creative-studio/creative_studio/cropping.py` — `crop_to_format`, `_maximal_ratio_box`,
  `_smartcrop_box`, `_detect_faces`/`_face_focal`, `_ratio_box_from_focal`, `CropResult` (Kommentare `# SKILL-032:`).
- `skills_sources/creative-studio/creative_studio/render_image.py` — `_bg_image_for_format`, `render(... smartcrop_bg=)`,
  CLI `--no-smartcrop` (`# SKILL-032:`).
- `skills_sources/creative-studio/tests/test_skill_032_smartcrop.py` — 12 Tests.

**Offen:** Verify-Pass (frische Session) + `setup.ps1`-Deploy + `requirements.txt` um `smartcrop` /
`opencv-python-headless` ergaenzen + Outcome-Review. Hinweis: lib-internes `RuntimeWarning: divide by zero` von
smartcrop auf flachen synthetischen Test-Bildern ist harmlos (echte Fotos betroffen nicht).
