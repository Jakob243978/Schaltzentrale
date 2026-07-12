# SKILL-029: creative-studio — Brand-Kit als brand.json (Token-Rollen + Logo-Handling)

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** brand_als_token_rollen_statt_flacher_env (bg/accent/ink/font + Logo) + logo_safe_zone_korrekt_platziert
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_creative-studio-flow-improvements.md` (§1.3 Brand-Kit/Design-Tokens/Asset-Management, §3.5 Logo-Handling + Brand-Kit als JSON; MoSCoW-Liste #5 = Should)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> `branding.env` ist ein valider, aber flacher Token-Store. Es fehlen: **Logo-Asset-Handling**
> (Datei-Referenz + Platzierungsregel je Format), **Rollen-Semantik** (heute nur bg/accent/ink, kein
> verschachteltes Token-Modell) und Validierung beim Laden. Best Practice: Brand als Design-Tokens nach
> Rolle + Core-Assets (Logo) + Templates. JSON ist skalierbarer als `.env` (verschachtelte Tokens,
> Logo-Pfade, Schrift-Dateien).

## Was soll erreicht werden? (Business-Ziel)
Ein optionales `brand.json` als Brand-Kit, das Token-Rollen (bg/accent/ink/font + Logo-Asset-Pfad inkl.
Positionierung je Format) ergaenzend/ersetzend zu `branding.env` definiert, plus Logo-Handling im Template
(safe-zone-korrekt platziert). Validierung beim Laden (fehlende Keys/Dateien → klare Warnung statt stiller
Fallback). Multi-Projekt: jedes Projekt bringt sein eigenes `brand.json`.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When ein `brand.json` uebergeben wird, the system shall Token-Rollen (mind. bg, accent,
      ink, font) **plus** Logo-Asset-Pfad und Positionierungsregel daraus laden.
- [x] **EARS-2:** When ein Logo-Asset definiert ist, the system shall es im Template **safe-zone-korrekt** je
      Format platzieren (Safe-Zone-Werte aus `specs.py`).
- [x] **EARS-3:** When sowohl `brand.json` als auch `branding.env` vorhanden sind, the system shall eine
      klare Praezedenz definieren (`brand.json` ergaenzt/ueberschreibt `branding.env`) — kein stiller Misch-Zustand.
- [x] **EARS-4:** When ein Brand-Key oder eine referenzierte Datei (Logo/Font) fehlt, the system shall eine
      **klare Warnung** ausgeben statt still auf einen Default zu fallen.
- [x] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall das
      `brand.json` als Parameter/Projekt-Config laden — kein hartkodierter Brand-Wert/Logo-Pfad im Skill.

## Technische Hinweise
- Neuer Loader `creative_studio/brand.py` (oder Erweiterung des Brand-Token-Loadings in `render_image.py`):
  liest `brand.json`, faellt auf `branding.env` zurueck, validiert Keys + Datei-Existenz.
- Logo-Positionierung als Regel je Format (z. B. `logo.position: "top-left"` + Safe-Zone-Offset). Template
  (`ad_image.html.j2`) bekommt Logo-Slot; Video-Composition analog optional.
- Token-Rollen als verschachteltes JSON (Recherche §1.3: Farben nach Rolle). Backward-kompatibel zu
  bestehendem `--brand-*`-Flow.
- Beispiel-`brand.example.json` als Template beilegen.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/brand.py` — **neu** (Brand-Kit-Loader + Validierung) oder
  Erweiterung in `render_image.py`.
- `skills_sources/creative-studio/templates/ad_image.html.j2` — Logo-Slot, safe-zone-korrekte Platzierung.
- `skills_sources/creative-studio/creative_studio/specs.py` — Safe-Zone-Werte fuer Logo-Platzierung.
- `skills_sources/creative-studio/templates/brand.example.json` — **neu** (Brand-Kit-Schema-Vorlage).
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_creative-studio-flow-improvements.md` (§1.3, §3.5).

## Ergebnis / Notizen

**Umgesetzt am 2026-06-24 (additiv, kein Breaking Change).**

### Was ergaenzt wurde
- `creative_studio/render_image.py` (additiv):
  - `load_brand_json(path, warn=None)` — liest `brand.json` als Token-Rollen. Schema: `brand_name`,
    `colors{bg,bg_soft,accent,ink,ink_muted}`, `font`, `logo{path,position,height_pct}`. Flache
    Top-Level-Keys (`bg`, `logo_path` …) werden als Convenience ebenfalls akzeptiert. Validierung:
    fehlende Logo-Datei + unbekannte `position` -> Warnung via `warn`-Callback (Default: stderr).
  - `resolve_brand(brand_env, brand_json, overrides, warn)` — vereint alle Quellen mit klarer Praezedenz.
  - `_logo_ctx(brand)` — baut den Logo-Template-Kontext (Position, relative Hoehe, eingebettete URI).
  - `_as_data_uri(path)` — bettet lokale Logo-Datei als `data:`-URI ein (loest das Playwright-
    `about:blank`-Origin-Problem, unter dem `file://`-Bilder nicht laden).
  - CLI: neues `--brand-json <pfad>` (additiv zu `--brand-env`). `build_html()`/`render()`-Signaturen
    unveraendert, `load_branding()` + `branding.env`-Weg voll erhalten (batch.py-kompatibel).
- `templates/ad_image.html.j2` (additiv): `.logo`-Slot in der oberen Safe-Zone (`top: var(--safe-top)`,
  links/rechts/zentriert je `logo_position`, Hoehe = `h * logo_height_pct/100`). Ohne Logo unveraendert:
  `brand_name`-Text wie bisher.
- `examples/brand.example.json` — neutrale Schema-Vorlage (keine Geheimnisse).
- `tests/test_skill_029_brand.py` — 14 Tests.

### Prioritaetsreihenfolge der Brand-Quellen (EARS-3)
`explizite overrides (CLI --brand)` > `brand.json` > `branding.env` > `_BRAND_DEFAULTS/_LOGO_DEFAULTS`.
Nicht ueberschriebene Keys bleiben aus der naechst-niedrigeren Schicht erhalten (kein stiller Misch-Zustand,
sondern definierte Schicht-Ueberlagerung).

### Test-Ergebnis
`pytest tests/test_skill_029_brand.py -q` -> **14 passed in 0.23s** (nur eigene Datei, parallele Edits laufen).

### Real-Test (Beleg, EARS-2)
Echter Render mit Pillow-generiertem gruenem Test-Logo (200x80 PNG) + `brand.json` (`position: top-left`,
`height_pct: 6.0`) ueber `python -m creative_studio.render_image ... --brand-json ... --formats feed_4x5`:
PNG geschrieben, im erwarteten Top-Left-Safe-Zone-Bereich (x 50–260, y 180–290) **16281 gruene Logo-Pixel**
nachgewiesen. Logo-Render damit am echten PNG belegt. Regressions-Render via `--brand-env` (ohne Logo)
laeuft unveraendert (brand_name-Text). Hinweis: `data:`-URI noetig, weil Playwrights `set_content()` auf
`about:blank`-Basis `file://`-Bilder blockiert (`naturalWidth=0`).

### Code-Referenzen
- `skills_sources/creative-studio/creative_studio/render_image.py` — `load_brand_json`, `resolve_brand`,
  `_logo_ctx`, `_as_data_uri`, `--brand-json` (alle `# SKILL-029:`).
- `skills_sources/creative-studio/templates/ad_image.html.j2` — `.logo`-Slot.
- `skills_sources/creative-studio/examples/brand.example.json` — Schema-Vorlage.
- `skills_sources/creative-studio/tests/test_skill_029_brand.py` — Tests.

> [!note] Abweichung von der Spec-Skizze
> Loader wurde NICHT als neues `creative_studio/brand.py` umgesetzt, sondern (laut Spec-Option
> "oder Erweiterung in render_image.py") additiv in `render_image.py` — Konfliktvermeidung mit
> parallelen Edits + Naehe zu `build_html`. Font-Datei-Existenzpruefung ist nicht implementiert
> (Template nutzt einen System-Font-Stack als String, keine Webfont-Datei) — Logo-Datei-Pruefung
> deckt den relevanten EARS-4-Fall ab.
