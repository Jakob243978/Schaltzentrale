# SKILL-034: creative-studio — Brand-Asset-Ordner-Konvention + Lizenz/Release-Tracking

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-23_picdrop-brand-assets.md`

> [!info] Herkunft (Recherche 2026-06-23, Subagent E + Jakob-Auftrag „Skill ausbauen")
> Jakobs Business-Portrait-Shooting (picdrop „Jacob_Businessshooting", evisible) ist potentielles
> Ad-Hintergrund-/Personal-Brand-Material. Dabei kam auf: Foto-Assets brauchen eine **klare Ablage +
> Lizenz-/Model-Release-Status**, sonst landen rechtlich ungeklärte Bilder in bezahlten Ads. Verbindet
> sich mit der Empfehlung aus der Avatar-Recherche (echtes Gesicht > KI-Avatar für DACH-B2B-Trust).

## Was soll erreicht werden? (Business-Ziel)
Eine projektneutrale **Konvention für Bild-Motiv-Assets**, die Original + Web-Variante + Metadaten
(inkl. Rechte/Release-Status) zusammenhält — damit nur rechtlich geklärtes Material in (bezahlte) Ads
fließt und der Skill Foto-Hintergründe sauber findet.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When Motiv-Assets in einem Projekt abgelegt werden, the system shall die Konvention
      `<projekt>/marketing/brand-assets/<quelle>/{originals/,web/,meta.json}` verwenden.
- [x] **EARS-2:** When ein Asset registriert wird, the system shall in `meta.json` je Datei
      `quelle`, `lizenz`, `model_release` (yes|no|unklar), `nutzung` (organic|paid|beides) und
      `aufnahmedatum` führen.
- [x] **EARS-3:** When ein Asset als `--bg-image` für eine **bezahlte** Ad verwendet wird und
      `model_release != yes`, the system shall eine **Warnung** ausgeben (keine harte Sperre, aber
      sichtbarer Hinweis — analog `AdContent.warnings()`).
- [x] **EARS-4 [multi-projekt]:** When der Skill in unterschiedlichen Projekten läuft, the system shall
      den Asset-Root relativ zum Projekt auflösen (kein hartkodierter Pfad).

## Technische Hinweise
- Knüpft an SKILL-029 (Brand-Kit `brand.json` = Tokens/Logo) an, ist aber das **Motiv-Pendant**
  (Foto-Assets + Rechte), nicht die Token-Schicht.
- `meta.json`-Schema klein halten; Lizenz/Release ist primär ein menschlich gepflegtes Feld.
- Offener Realfall: picdrop-Shooting — Rechte mit evisible noch zu klären (siehe Recherche-Doc).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/` (neue `assets.py` o. Ä. für Registry/Warnung).
- Konvention dokumentiert in `SKILL.md`.

## Ergebnis / Notizen

**Implementiert (2026-06-24):** `creative_studio/assets.py` — Registry-Helper für die Motiv-Asset-Konvention.

- **EARS-1:** Pfad-Auflösung `asset_root()` → `<project_root>/marketing/brand-assets`,
  `source_dir()`/`ensure_source_layout()` legen `<quelle>/{originals/,web/}` an,
  `meta_path()` → `meta.json`. Konstanten `ASSET_ROOT_REL`, `ORIGINALS_DIRNAME`, `WEB_DIRNAME`.
- **EARS-2:** `Asset`-Dataclass mit `dateiname, quelle, lizenz, model_release (yes|no|unklar),
  nutzung (organic|paid|beides), aufnahmedatum`. `load_registry()`/`save_registry()`/`register_asset()`
  schreiben/lesen `meta.json` (Round-Trip getestet). `normalized()` fängt unbekannte Enum-Werte ab
  (→ `unklar`/`organic`).
- **EARS-3:** `asset_warnings(asset, use="paid")` warnt bei `model_release != yes` (analog
  `AdContent.warnings()` — nur Hinweis, keine Sperre); zusätzlich Hinweise bei organic-Asset→paid und
  fehlender Lizenz. `AssetRegistry.warnings()` sammelt je Asset.
- **EARS-4:** Asset-Root immer relativ zum `project_root`-Parameter — kein hartkodierter Pfad
  (multi-projekt-tauglich, Vision-Prinzip erfüllt).

**Tests:** `tests/test_skill_034_assets.py` — 7 Tests, alle grün (Teil der 14 passed in 0.90s).
Abgedeckt: Konventions-Pfad relativ, Layout originals/web, meta.json Round-Trip,
Enum-Normalisierung, Release-Warnung bei paid (+ Gegenprobe yes), Registry-Sammlung.

**Real-Bezug:** Die picdrop-Quelle `picdrop-jaQGXDaJAS` (Header 4000x2667 sRGB) passt 1:1 in die
Konvention; deren Web-Variante erzeugt SKILL-035 (`prep_bg.py`). Rechte/Model-Release mit evisible
noch offen → genau das, wovor `asset_warnings(use="paid")` schützt.

**Code-Referenz:** `skills_sources/creative-studio/creative_studio/assets.py` (Kommentare `# SKILL-034:`).
Knüpft an SKILL-029 (Brand-Kit `brand.json`) als Motiv-Pendant an. `specs.py` NICHT geändert.
