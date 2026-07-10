# SKILL-039: creative-studio — ContentType-Ebene + CONTENT_TYPES-Katalog in specs.py

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Must
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_social-content-types.md` (§0 Lücke, §3.1 Datenstruktur, §3.2 Katalog, §5 MoSCoW Must)

> [!info] Herkunft (Recherche 2026-06-24)
> Der Skill kennt heute nur **technische Ausgabe-Formate** (`AdFormat`/`FORMATS`: feed_4x5/story_9x16/
> square_1x1) — aber **keine semantischen Content-Typen** (Carousel, Talking-Head, Listicle …). Es fehlt
> eine **Content-Typ-Ebene** ueber den Formaten, die die *inhaltliche Bauart* beschreibt (mehrseitig?
> Video? Slide-Anzahl? On-Screen-Text-Limit? Funnel-Stufe? empfohlenes Framework?). Genau diese Ebene
> legt dieses Ticket additiv an — **ohne** die Formate aufzublaehen (neue Ebene neben `AdFormat`, §3 Designprinzip).

## Was soll erreicht werden? (Business-Ziel)
Eine neue `@dataclass(frozen=True) ContentType` + ein Katalog `CONTENT_TYPES` in `specs.py`, der die
inhaltlichen Content-Arten modelliert und auf **erlaubte `FORMATS`-Keys** + **`frameworks.FRAMEWORKS`-Keys**
verweist. So kann ein vorgelagerter Agent/Generator den passenden Content-Typ waehlen und kennt dessen
Constraints (Slide-Range, Video-Laenge, Hook-Fenster, On-Screen-Wortlimit, Funnel-Stufe). Projektneutral:
keine Brand-/Projektwerte — nur generische Content-Typ-Definitionen.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When `specs.py` geladen wird, the system shall eine `@dataclass(frozen=True) ContentType`
      mit den Feldern aus §3.1 bereitstellen (`key`, `name`, `medium`, `funnel`, `formats`, `min_seconds`,
      `max_seconds`, `hook_window_seconds`, `min_slides`, `max_slides`, `onscreen_word_limit`,
      `recommended_framework`, `note`). → Test `test_content_type_dataclass_fields`.
- [ ] **EARS-2:** When `CONTENT_TYPES` geladen wird, the system shall mindestens die Typen
      `static_statement`, `carousel`, `educational_carousel`, `short_video_text_hook`, `talking_head`,
      `listicle` enthalten (Werte aus §3.2). → Test `test_content_types_minimum_catalog`.
- [ ] **EARS-3:** When ein `ContentType.formats`-Eintrag geprueft wird, the system shall ausschliesslich
      gueltige `FORMATS`-Keys referenzieren; und jeder gesetzte `recommended_framework` shall ein gueltiger
      `FRAMEWORKS`-Key sein. → Tests `test_content_type_formats_are_valid`, `test_content_type_framework_keys_valid`.
- [ ] **EARS-4:** When `get_content_type(key)` mit gueltigem Key aufgerufen wird, the system shall den
      `ContentType` liefern; bei unbekanntem Key shall ein `KeyError` mit Liste der bekannten Keys geworfen
      werden (analog `get_format()`). → Tests `test_get_content_type_ok`, `test_get_content_type_keyerror`.
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall im
      `ContentType`-Katalog **keinen** hartkodierten Projekt-/Brand-Wert tragen (nur generische
      Content-Typ-Definitionen). → Test `test_content_types_project_neutral`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Additive neue Datenklasse + Katalog-Dict in `specs.py`, parallel zu `AdFormat`/
  `FORMATS`. `ContentType` referenziert `FORMATS`-Keys und `frameworks.FRAMEWORKS`-Keys per String
  (lose Kopplung, kein Import-Zyklus — `frameworks` importiert `specs` nicht umgekehrt; Keys werden im
  Test gegen `frameworks.FRAMEWORKS` validiert). `get_content_type()` analog `get_format()`.
- **Verworfene Alternative:** Content-Typ-Felder in `AdFormat` integrieren — verworfen, weil das die
  technische Format-Ebene aufblaeht und Format ≠ Content-Bauart vermischt (§3 Designprinzip).
- **Betroffene Module:** `specs.py` (neue Klasse + Katalog + Getter), neue Testdatei.

## Technische Hinweise
- `onscreen_word_limit` Default = `frameworks.MAX_WORDS_ONSCREEN` (7) — **kein** Doppel-Wert. Bild-Typen
  setzen Video-Felder (`min_seconds`/`max_seconds`/`hook_window_seconds`) auf `None`, Single-Image-Typen
  die Slide-Felder auf `None`.
- Reine Datenstruktur, keine Render-/Netzwerk-Logik. Validierungs-Logik kommt in SKILL-040.
- `before_after`/`testimonial`/`talking_head`/`voiceover_broll`/`story_ad`/`ugc_style`/`testimonial_video`
  duerfen ergaenzt werden, sind aber Teil von SKILL-042 (ContentType-Erweiterung) — dieses Ticket liefert
  die Basis-Sechs (EARS-2).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — neue `ContentType`, `CONTENT_TYPES`,
  `get_content_type()` (Block `# === SKILL-039 ===`).
- `skills_sources/creative-studio/tests/test_skill_039_content_types.py` (neu).
- Wissensgrundlage: `2026-06-24_social-content-types.md` (§0, §3.1, §3.2, §5 Must).

## Ergebnis / Notizen

**Umgesetzt 2026-06-24 (Status -> review, Verify-Gate offen).**

In `creative_studio/specs.py` (Block `# === SKILL-039 ===`) ergaenzt:
- `@dataclass(frozen=True) ContentType` mit allen Feldern aus §3.1 (`key`, `name`,
  `medium`, `funnel`, `formats`, `min_seconds`, `max_seconds`, `hook_window_seconds`,
  `min_slides`, `max_slides`, `onscreen_word_limit`, `recommended_framework`, `note`)
  + zwei SKILL-042-Flags (`requires_compliance_check`, `requires_proof`).
- Konstante `ONSCREEN_WORD_LIMIT_DEFAULT = 7` (spiegelt `frameworks.MAX_WORDS_ONSCREEN`
  ohne Import; Aequivalenz per Test gesichert).
- Katalog `CONTENT_TYPES` mit den Basis-Sechs (`static_statement`, `carousel`,
  `educational_carousel`, `short_video_text_hook`, `talking_head`, `listicle`) —
  Erweiterung via SKILL-042 im selben Dict.
- `get_content_type(key)` analog `get_format()` (KeyError mit Key-Liste).

Tests: `tests/test_skill_039_content_types.py` (Abschnitt SKILL-039).

Done-Kriterien (EARS):
- [x] EARS-1: Dataclass-Felder vorhanden -> `test_content_type_dataclass_fields`.
- [x] EARS-2: Basis-Sechs im Katalog -> `test_content_types_minimum_catalog`.
- [x] EARS-3: nur gueltige FORMATS-/FRAMEWORKS-Keys -> `test_content_type_formats_are_valid`,
      `test_content_type_framework_keys_valid`.
- [x] EARS-4: `get_content_type` ok + KeyError -> `test_get_content_type_ok`,
      `test_get_content_type_keyerror`.
- [x] EARS-5: projektneutral -> `test_content_types_project_neutral`.

pytest gesamt: **158 passed** (138 Baseline + 20 neu).
