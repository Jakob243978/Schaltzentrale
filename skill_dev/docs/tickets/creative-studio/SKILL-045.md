# SKILL-045: creative-studio — Reel-Spec (JSON) als Render-Input

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Must
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_reels-video-editing-strategy.md` (§3.5 Batch/Data-driven, §6 Soll, §7 MoSCoW Must)

> [!info] Herkunft (Recherche 2026-06-24)
> Skalierung = **eine Composition + n Props-JSONs** (`npx remotion render … --props`). Es fehlt ein
> definiertes **Reel-Spec-Schema** (Hook, Captions-JSON/SRT, B-Roll-Liste, Brand, CTA, Musik), das einen
> einzelnen Reel-Render vollstaendig beschreibt. Dieses Schema ist die **Basis fuer Batch** (SKILL-048) und
> der gemeinsame Eingang fuer Captions (SKILL-043), Audio (SKILL-044) und B-Roll (SKILL-046).

## Was soll erreicht werden? (Business-Ziel)
Ein dokumentiertes, validiertes **Reel-Spec-JSON-Schema** + Loader, der eine Spec in die `--props` der
Remotion-Composition uebersetzt. Ein Reel pro Spec → reproduzierbar, versionierbar, batchbar.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When eine gueltige Reel-Spec (JSON) geladen wird, the system shall daraus ein
      `--props`-Objekt fuer die Composition bauen (Hook, Captions-Ref, B-Roll-Liste, Brand-Tokens, CTA,
      Musik-Ref). → Test `test_reel_spec_to_props`.
- [x] **EARS-2:** When eine Reel-Spec Pflichtfelder vermisst (z.B. kein `hook`/`brand`), the system shall
      eine klare Fehler-/Warn-Meldung liefern statt still ein leeres Reel zu rendern. → Test `test_reel_spec_missing_required`.
- [x] **EARS-3:** When eine Reel-Spec Captions/B-Roll/Musik **nicht** enthaelt, the system shall die
      jeweiligen Layer als optional behandeln (Reel rendert trotzdem). → Test `test_reel_spec_optional_layers`.
- [x] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall Brand +
      Inhalt ausschliesslich aus der Spec beziehen — kein hartkodierter Projektwert im Loader.
      → Test `test_reel_spec_project_neutral`.
- [x] **EARS-5:** When eine Reel-Spec geladen wird, the system shall die Naming-Systematik (SKILL-024,
      `variant_id`/`utm_content`) fuer den Reel-Output nutzen — **kein** Parallel-Schema. → Test `test_reel_spec_naming_single_source`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `creative_studio/reel_spec.py` mit einer `ReelSpec`-Dataclass + `load_reel_spec()`
  (JSON → Dataclass → `--props`-Dict). Schema dokumentiert in SKILL.md/Template. Naming via bestehendem
  `make_variant_id`/`make_utm_content`.
- **Verworfene Alternative:** Spec direkt als rohes `--props`-JSON ohne Schema/Validierung — verworfen,
  weil ein still leer gerendertes Reel ein Hard-Failure-Risiko ist (kein Silent-Fake).
- **Betroffene Module:** `creative_studio/reel_spec.py` (neu), `specs.py` (read-only Naming), SKILL.md
  (Schema-Doku), neue Testdatei.

## Technische Hinweise
- `surface: backend`. Spec-Felder (Vorschlag): `ad_id`, `framework`, `hook`, `captions` (Pfad/JSON/SRT),
  `broll` (Clip-Liste), `voiceover`/`music` (Audio-Refs), `cta`, `brand` (Tokens). Optional-Felder klar markiert.
- Voraussetzung: SKILL-043/044/046 liefern die Composition-Layer, die die Spec adressiert; SKILL-024 das Naming.
- **Lizenz-Risiko Remotion** (ab 4 Personen) im Blick behalten (SKILL.md §7).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/reel_spec.py` (neu) — `ReelSpec` + `load_reel_spec()`.
- `skills_sources/creative-studio/creative_studio/specs.py` — `make_variant_id`/`make_utm_content` (read-only).
- `skills_sources/creative-studio/SKILL.md` — Reel-Spec-Schema-Abschnitt.
- `skills_sources/creative-studio/tests/test_skill_045_reel_spec.py` (neu).
- Wissensgrundlage: `2026-06-24_reels-video-editing-strategy.md` (§3.5, §6, §7 Must).

## Ergebnis / Notizen

**Umgesetzt (2026-06-24):**
- Neues Modul `creative_studio/reel_spec.py` mit `ReelSpec`-Dataclass (+ `SceneSpec`,
  `CaptionTokenSpec`, `BrollClipSpec`), `load_reel_spec()` (JSON-Datei),
  `parse_reel_spec()` (Dict -> validierte ReelSpec) und `reel_spec_to_props()`
  (-> `--props`-Dict fuer die `AdReel`-Composition). CLI:
  `python -m creative_studio.reel_spec --spec reel.json [--out props.json]`.
- Schema dokumentiert in `SKILL.md` §10 (Feld-Tabelle, Pflicht/Optional). Beispiel-
  Spec: `examples/reel_h1-immo.json`.
- Naming aus SKILL-024 (`make_variant_id`/`make_utm_content`) — `variant_id`/
  `utm_content` als `@property` + in die Props uebernommen, **kein** Parallel-Schema
  (EARS-5). Pflichtfeld-Validierung wirft `ReelSpecError` statt stillem Leer-Reel
  (EARS-2). Optionale Layer -> `None`/leer (EARS-3). Brand/Inhalt nur aus Spec
  (EARS-4).
- `duration_frames()` leitet die dyn. Dauer aus `scenes`-Summe bzw. letztem
  Caption-`endMs` ab und speist `props.durationInFrames` (Kopplung an SKILL-044).

**Tests:** `tests/test_skill_045_reel_spec.py` — 6 Tests (je EARS + Example-Load),
**alle gruen**. Voller Skill-Lauf: **180 passed** (vorher 174).

**Render-Verify (echt, End-to-End):**
- Repo-Beispiel `examples/reel_h1-immo.json` -> `reel_spec_to_props` -> `AdReel` ->
  **Exit 0**, MP4 539 kB (`tests/artifacts/reel_h1-immo.mp4`).
- Voll bestueckte Spec (B-Roll aus Silber + Musik + Captions) -> Props -> `AdReel` ->
  **Exit 0**, Gold-MP4 2,7 MB (`…/Gold/reel_h1-immo_broll.mp4`), 120 Frames, h264+aac.
Die Spec ist damit als realer Render-Input nachgewiesen (Hook/Brand/Captions/B-Roll/
Musik/dyn. Dauer alle durchgelaufen). Hinweis: `broll`-Feld wurde additiv in den
Loader + Props aufgenommen (SKILL-046-Vorbereitung); `duration_frames()` zieht jetzt
auch B-Roll-Summe heran.

**Reel-Spec-Schema-Felder:** Pflicht `ad_id`, `hook`, `brand` (mit `brand.name`);
optional `framework`, `hook_index`, `hook_accent`, `eyebrow`, `subline`, `cta`,
`scenes[{text,seconds}]`, `captions[{text,startMs,endMs}]`, `caption_style`,
`voiceover`, `music`, `broll[{src,seconds}]`. Brand-Tokens: `name`, `accent`, `bg`,
`bgSoft`, `ink`, `inkMuted`, `highlight`, `font`.

**Done-Kriterien:** EARS-1..5 per Test gruen; echter End-to-End-Render der
Beispiel-Spec (Exit 0). -> `review`.

**Lizenz-Risiko (Vermerk, kein Blocker):** Remotion ab 4 Team-Personen
kostenpflichtig (SKILL.md §7).
