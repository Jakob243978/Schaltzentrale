# SKILL-035: creative-studio — Bild-Komprimierungs-Helper (prep_bg.py)

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-23_picdrop-brand-assets.md`

> [!info] Herkunft (Recherche 2026-06-23, Subagent E)
> Profi-Fotos kommen in 30-MP-Originalauflösung. Für Ad-Hintergründe braucht es eine schlanke,
> Meta-konforme Web-Variante; das Original sollte verlustfrei archiviert bleiben. Meta re-encodiert
> beim Upload ohnehin → Ziel ist saubere sRGB-Qualität bei kleiner Datei, nicht maximale Auflösung.

## Was soll erreicht werden? (Business-Ziel)
Ein kleiner Helper, der Roh-Fotos reproduzierbar in **Ad-taugliche Hintergrund-Varianten** wandelt
(Meta-Spec-konform) und das Original unangetastet lässt.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When ein Original-Foto übergeben wird, the system shall eine Web-Variante erzeugen:
      lange Kante **1440 px**, **sRGB**, **MozJPEG ~q82**, und das Original unverändert in `originals/` lassen.
- [x] **EARS-2:** When die Web-Variante erzeugt ist, the system shall sie gegen die Meta-Specs aus
      `specs.py` validieren (sRGB, kurze Kante ≥ `MIN_EDGE_PX`, Dateigröße ≤ `MAX_FILE_MB`) und bei
      Verstoß warnen.
- [x] **EARS-3:** When ein Bild bereits sRGB/klein genug ist, the system shall unnötiges Re-Encoding
      vermeiden (idempotent).
- [x] **EARS-4 [multi-projekt]:** When ohne Zielordner aufgerufen, the system shall die Web-Variante
      neben dem Original unter `web/` ablegen (Konvention aus SKILL-034).

## Technische Hinweise
- Pillow (bereits vorhanden) reicht; optional `mozjpeg`/`cwebp` falls verfügbar. WebP/AVIF bringt für
  die Ad-Qualität wenig (Meta re-encodiert), v. a. Repo-Größen-Vorteil — als Option, nicht Default.
- Speist die `--bg-image`-Pipeline (zusammen mit smartcrop SKILL-032).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/prep_bg.py` (neu).
- Nutzt `specs.py`-Constraints (MIN_EDGE_PX, MAX_FILE_MB, COLOR_SPACE).

## Ergebnis / Notizen

**Implementiert (2026-06-24):** `creative_studio/prep_bg.py` — Funktion `prep_bg(src, out_dir=None,
*, long_edge=1440, quality=82)` + CLI `python -m creative_studio.prep_bg <input> [--out <dir>]`.

- **EARS-1:** Downscale auf lange Kante 1440 px (nie hochskaliert, LANCZOS), `convert("RGB")` → sRGB,
  JPEG `quality=82, optimize=True, progressive=True`, sRGB-ICC eingebettet (`ImageCms.createProfile("sRGB")`).
  Original wird nie geöffnet-zum-Schreiben → byte-identisch erhalten (Test prüft `read_bytes()`-Gleichheit
  + mtime). MozJPEG nicht trivial verfügbar → Pillow-JPEG `optimize=True` wie in Spec erlaubt.
- **EARS-2:** `_validate()` prüft gegen `specs.MIN_EDGE_PX` / `MAX_FILE_MB` / `COLOR_SPACE` → Warnliste
  (kurze Kante, Farbraum, Größe).
- **EARS-3:** `_is_already_conform()` (sRGB + lange Kante ≤ Ziel + Datei ≤ MAX_FILE_MB) → 1:1-Copy statt
  Re-Encode, `skipped=True`. Gegenprobe: großes Bild → `skipped=False`, kleiner.
- **EARS-4:** ohne `--out` → `web/` neben dem Original (SKILL-034-Konvention).

**Tests:** `tests/test_skill_035_prep_bg.py` — 7 Tests, alle grün
(`pytest tests/test_skill_035_prep_bg.py tests/test_skill_034_assets.py` → 14 passed in 0.90s).

**Real-Test** (Probe-Datei `AgentischesArbeiten/marketing/brand-assets/picdrop-jaQGXDaJAS/00_header_4000x2667_sRGB.jpg`,
Output in Temp, NICHT ins Repo):
| | vorher | nachher |
|---|---|---|
| px | 4000 x 2667 | **1440 x 960** |
| Größe | 836 KB | **100 KB** (≈ 88 % kleiner) |
| Farbraum | sRGB | **sRGB (ICC "sRGB built-in" eingebettet)** |

Original unverändert (856473 bytes). Sichtbare Validierungs-Warnung griff korrekt: kurze Kante 960 px
< MIN_EDGE_PX (1080) — das 3:2-Querformat unterschreitet bei 1440 px langer Kante die Meta-Mindestkante,
genau der Hinweis, den EARS-2 liefern soll (keine harte Sperre).

**Code-Referenz:** `skills_sources/creative-studio/creative_studio/prep_bg.py` (Kommentare `# SKILL-035:`).
Nutzt `specs.py`-Constants read-only (specs.py NICHT geändert).
