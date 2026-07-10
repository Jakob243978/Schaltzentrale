# SKILL-020: creative-studio — Skill-Grundgerüst + Bild-Modul (HTML/CSS → Playwright, Safe-Zones, Multi-Format)

**Status:** in_progress
**Erstellt:** 2026-06-23
**MoSCoW:** Should
**Geschaetzter Aufwand:** L
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** skill_in_2plus_projekten_genutzt (MetaAdsAgent + SocialMediaBuilder) + token_saving_pro_skill_nutzung (Creative-Erzeugung ohne Re-Recherche/Re-Bau pro Projekt)
**outcome_review_at:** null (wird beim done-Set gesetzt)
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/):**
`docs/marketing/ad-creative-specs.md` (Formate/Safe-Zones/Specs) + `docs/research/2026-06-23_ad-image-generation-python.md` (Bild-Stack)

> [!info] Herkunft (Jakob 2026-06-23)
> Aus der Meta-Ads-Arbeit entstand der Bedarf, Social-Ad-Creatives **automatisiert + markenkonform**
> zu erzeugen (Bild jetzt, Video als SKILL-021). Statt es pro Projekt neu zu bauen → **ein
> wiederverwendbarer Skill** `creative-studio`, erster Einsatz in **AgentischesArbeiten**
> (Warteliste-Ads), danach SocialMediaBuilder. Scope-Entscheidung: ein Skill für Bild + Video
> (gemeinsamer Web-Tech-Kern), Bild zuerst.

## Was soll erreicht werden? (Business-Ziel)
Ein Skill, der aus **Content (Copy/Headline/CTA) + Brand-Tokens + optional Motiv** markenkonforme
Social-Ad-**Bilder** in mehreren Formaten (4:5, 9:16, 1:1) erzeugt — Safe-Zone-korrekt, deutschsprachig
(Umlaute), reproduzierbar/versioniert, **ohne hartkodierten Projekt-Code** (Multi-Projekt via Config).

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When der Skill aktiviert wird, the system shall ein `SKILL.md` + `README.md` unter
      `skills_sources/creative-studio/` bereitstellen (Identität, Scope, Aktivierungs-Trigger,
      Abgrenzung Bild/Video) — Identität in README, Methodik referenziert SKILLS_VISION.
- [ ] **EARS-2:** When ein Creative erzeugt wird, the system shall ein **HTML/CSS-Template** (Jinja2)
      über **Playwright** (headless Chromium) zu PNG rendern — mit Webfont für korrekte Umlaute.
- [ ] **EARS-3:** When ein Zielformat gewählt wird, the system shall **Safe-Zones als CSS-Padding** pro
      Format setzen (Werte aus `ad-creative-specs.md`: 9:16 oben ~14 %, unten ~35 %; Feed ~14 %/20–35 %)
      und Text/Logo in einen `.safe`-Container legen.
- [ ] **EARS-4:** When mehrere Formate angefordert werden, the system shall **aus EINER Vorlage**
      4:5 (1080×1350), 9:16 (1080×1920) und 1:1 (1080×1080) per viewport-/Variablen-Swap exportieren.
- [ ] **EARS-5 [multi-projekt]:** When der Skill in einem Projekt läuft, the system shall Brand-Werte
      (Farben/Font/Logo) + Content **aus Projekt-Config** beziehen (z. B. `branding.env`/Parameter) —
      **kein** projekt-spezifischer Pfad/Wert im Skill (Vision-Prinzip 1).
- [x] **EARS-6:** When ein Hintergrundfoto im falschen Ratio vorliegt, the system shall content-aware
      croppen (`smartcrop.py`) statt zu verzerren. _(erledigt via SKILL-032 — `creative_studio/cropping.py` + Integration in `render_image.py`, 2026-06-24)_
- [x] **EARS-7 [Standards-als-Code]:** When der Skill arbeitet, the system shall die Meta-Ad-Anforderungen
      aus der Recherche (Formate, Safe-Zone-Anteile, technische Constraints, Text-im-Bild-Regel,
      DACH-Coaching-Claim-Fallstrick) als **zentrale Spec-/Content-Klasse** (`specs.py`: `AdFormat`,
      `FORMATS`, `AdContent`, Constants) kodieren — Single Source, von Bild- UND (künftig) Video-Modul
      genutzt, ohne projekt-spezifische Werte (Vision-Prinzip 1).
- [x] **EARS-8 [Content-Validierung]:** When ein `AdContent` Text-im-Bild-Risiken enthält (Coaching-
      Claim-Trigger, zu lange Headline), the system shall **Warnungen** ausgeben (keine harte Sperre,
      da Metas 20-%-Regel tot ist) — `AdContent.warnings()`.

## Technische Hinweise
- **Code-Ablage:** `skills_sources/creative-studio/` (Source-of-Truth) → Deploy via `setup.ps1`.
- **Stack:** Playwright (Python) + Jinja2-HTML/CSS-Templates + `smartcrop.py`. Pillow als Fallback
  (ohne Browser-Stack). Details + Repos/Quellen in `2026-06-23_ad-image-generation-python.md`.
- **Synergie:** Web-Tech-Kern (HTML/CSS) wird mit dem Video-Modul (SKILL-021, Remotion) geteilt —
  gleiche Brand-Tokens + Safe-Zone-Logik. Beim Bild-Modul-Design schon auf Wiederverwendung achten.
- **Meta Advantage+ Hinweis:** Creative-Enhancements ggf. im Ad-Set deaktivieren, sonst überschreibt
  Meta die Komposition (siehe Recherche).
- **Multi-Projekt:** Erst-Einsatz AgentischesArbeiten (Warteliste-Ads, Copies aus
  `ads_warteliste_meta.md` ⚠️ Meta-Coaching-Claim-Fallstrick beachten), dann SocialMediaBuilder.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — **Standards als Code** (AdFormat, FORMATS,
  Safe-Zones, Constraints, AdContent + warnings) ✅ gebaut.
- `skills_sources/creative-studio/creative_studio/render_image.py` — Playwright-Renderer, Multi-Format,
  Brand-Tokens aus `branding.env` (Parameter) ✅ gebaut.
- `skills_sources/creative-studio/templates/ad_image.html.j2` — HTML/CSS-Template, Safe-Zones als
  CSS-Padding, Brand-Token-Variablen, `--debug-safe`-Overlay ✅ gebaut.
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/ad-creative-specs.md`,
  `AgentischesArbeiten/docs/research/2026-06-23_ad-image-generation-python.md`.

## Ergebnis / Notizen

**Implementiert (2026-06-23):**
- Standards aus der Recherche als Code kodiert (`specs.py`) — EARS-7/8 ✅ (Jakob: „Code und Standards
  unbedingt als Ticket reinbringen").
- HTML/CSS-Template + Playwright-Renderer, **Multi-Format aus EINER Vorlage** (feed_4x5, story_9x16,
  square_1x1), Safe-Zones als CSS-Padding aus `specs.py`.
- **Erste Bild-Ad live generiert + visuell validiert (h1-immo, 3 Formate):** Brand-Farben aus
  `branding.env` korrekt, Umlaute korrekt (System-Font, kein Webfont nötig), 9:16 hält die untere
  35 %-Safe-Zone frei, CTA/Eyebrow/Headline-Akzent sauber. Stack: Playwright + Jinja2 (+ Pillow/Jinja2
  bereits vorhanden; Playwright+Chromium neu installiert).

**Offen:** EARS-1 (SKILL.md/README) in Arbeit; EARS-6 (smartcrop für Foto-Hintergründe) noch offen
(erste Ad nutzt Brand-Gradient statt Foto); Verify-Pass + `setup.ps1`-Deploy + Outcome.
