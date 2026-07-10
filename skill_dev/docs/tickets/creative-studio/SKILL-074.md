# SKILL-074: creative-studio — Automatischer Lesbarkeits-/Kontrast-Check der Text-Regionen (WCAG, warnen-statt-blocken)

**Status:** review
**Erstellt:** 2026-07-08
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**surface:** backend
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`
**outcome_metric:** schlecht_lesbarer_text_auf_foto_bg_wird_automatisch_erkannt (WCAG-AA gemessen gegen den tatsaechlichen Pixel-Hintergrund, nicht nur die Theme-Farbe) + warnung_statt_block (Mensch-im-Loop) + kein_bestandsbruch (Default aus)
**outcome_review_at:** null
**Wissensgrundlage:** Live-Use-Feedback Jakob (2026-07-08): Foto-Hintergruende (z.B.
`hook-skalieren-2026__photo-poster`, SKILL-072/073 `photo-poster`/`object-hero`) machen
Text stellenweise schlecht lesbar — der Untergrund UNTER dem Text variiert (helle Headline
auf hellem Bildbereich), was die Theme-Farbe nicht abbildet. WCAG 2.1 SC 1.4.3 (AA):
4.5:1 kleiner Text, 3:1 grosser Text. Warn-statt-Block-Muster aus SKILL-072
(`layout_warnings()`) / SKILL-026 (`compliance_warnings()`). Pillow ist bereits Dependency.

> [!info] Herkunft (Live-Use-Feedback + Jakob-Auftrag „Skill ausbauen")
> Die foto-getriebenen Layouts aus SKILL-072/073 loesen ein neues Lesbarkeits-Problem aus:
> fette Typo direkt ueber einem Foto. Statt das im Auge des Betrachters zu lassen, MISST der
> Skill den Kontrast jetzt selbst — gegen den echten gerenderten Pixel-Hintergrund — und warnt.
> Fuehrt Live-Use-Lehre in den Skill zurueck (`lessons-aus-live-use-zurueckfuehren`).

## Was soll erreicht werden? (Business-Ziel)
Nach dem Rendern wird pro Text-Region (Kicker/Headline/Subline/CTA bzw. Hero) die
WCAG-Kontrast-Ratio zwischen Textfarbe und dem TATSAECHLICHEN lokalen Pixel-Hintergrund
gemessen. Unterschreitet eine Region die AA-Schwelle, warnt der Skill (keine Sperre) mit
Region + gemessenem Wert und schlaegt bei Foto-BG eine Scrim-/Panel-Verstaerkung vor —
bei unveraendertem Default-Verhalten (Check ist opt-in via `--check-contrast`).

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** the system shall die WCAG-2.1-Kontrast-Ratio korrekt berechnen
      (Relativ-Luminanz je Kanal, `(L_hell+0.05)/(L_dunkel+0.05)`; weiss/schwarz=21:1,
      gleiche Farbe=1:1) und die AA-Schwellen 4.5:1 (klein) / 3:1 (gross) fuehren.
- [x] **EARS-2:** When ein Creative gerendert ist, the system shall je Text-Region den
      Kontrast gegen den GEMITTELTEN/SCHLECHTESTEN lokalen BG-Pixelbereich messen (Region
      in ein Raster von Kacheln zerlegt, Worst-Case-Kachel = Region-Ratio) — gegen den
      tatsaechlichen Pixel-Hintergrund, nicht nur die Theme-Farbe.
- [x] **EARS-3:** When eine Region ihre AA-Schwelle unterschreitet, the system shall
      **warnen (keine Sperre)** mit Region + gemessenem Wert + Ziel-Schwelle
      (Muster `layout_warnings()`; Mensch-im-Loop).
- [x] **EARS-4 [Should]:** When Foto-BG + geringer Kontrast vorliegt, the system shall eine
      konkrete Fix-Empfehlung liefern (Scrim/Text-Panel verstaerken); ohne Foto-BG stattdessen
      Textfarbe/Theme-Empfehlung.
- [x] **EARS-5 [nicht-brechend]:** the system shall den Check nur bei `--check-contrast`
      ausfuehren (Default aus) — Bestands-/Parallel-Renders bleiben exakt gleich; keine neue
      Abhaengigkeit (rein Pillow).
- [x] **EARS-6 [multi-projekt]:** the system shall Textfarben aus den Brand-Tokens und die
      Region-Geometrie aus `AdFormat`-Safe-Zones + Layout ableiten — kein hartkodierter
      Brand-/Projektwert.

## Loesungs-Skizze (Approach)
- **`creative_studio/readability.py`** (neu, rein PIL): WCAG-Kern
  (`relative_luminance`, `contrast_ratio`, `parse_color` fuer Hex/rgb()/Namen),
  `TextRegion`/`ContrastFinding`-Dataclasses, `text_regions()` (Region-Boxen aus
  Format-Safe-Zones + Layout; Bodenstack fuer template/photo-poster/object-hero/
  split-compare, Top-Stack fuer stat-hero; nur Regionen mit nicht-leerem Inhalt),
  `_tile_means()` (Region -> Raster-Mittel via `Image.BOX`-Resize), `measure_region()`
  (Worst-/Mean-Kachel-Kontrast), `check_contrast()`, `contrast_warnings()` (Warn-
  Validator), `recommend_contrast_fix()` (Should). Standalone-CLI.
- **`render_image.py`:** additives CLI-Flag `--check-contrast`; nach dem Render je Format
  `contrast_warnings()` + `recommend_contrast_fix()` auf das gerenderte PNG (Textfarben aus
  dem bereits themed Brand-dict, Layout/Style aus den bestehenden Args). Default aus ->
  nicht-brechend. `build_html()`/`render()` unveraendert.
- **Textfarben pro Region:** Headline=Ink (Akzent bei `--accent-as-block`), Hero/Eyebrow=Akzent,
  Subline=Ink-Muted, CTA-Pill=Weiss (das Sampling trifft die Akzent-Pille automatisch),
  CTA-Link (`--chrome minimal`)=Akzent.
- **Verworfen:** exakte DOM-Bounding-Boxes via Playwright waehrend des Renders (koppelt den
  Check an den Render-Pfad, bricht Parallel-Renders-Neutralitaet) — stattdessen geometrische
  Region-Schaetzung aus Safe-Zones + Layout, standalone auf jedem PNG lauffaehig. Text-Strich-
  Kontamination der Kachel-Mittel ist bewusst konservativ (verschiebt Richtung Textfarbe ->
  eher warnen).

## Test-Ergebnis
- `tests/test_skill_074_contrast.py` — **13 passed** (rein PIL, offline, kein Playwright):
  WCAG-Kern (21:1 / 1:1 / Monotonie / AA-Schwellen / Farb-Parsing), guter Kontrast (heller
  Text auf dunklem BG) -> keine Warnung, schlechter Kontrast (heller Text auf Cream) -> Warnung
  mit Region+Wert, Findings-`ok`-Flag, Foto-BG-Fix-Empfehlung, Projektneutralitaet
  (Parameter-Farben), leere Subline -> keine Subline-Region, PNG-Pfad-Eingang.
- Gesamt-Suite **277 passed** (264 Bestand + 13 SKILL-074), keine Regression.
- **CLI-Beleg:** `python -m creative_studio.readability <cream-poster.png> --layout photo-poster
  --has-bg-image` meldet headline 1.15:1 (Ziel 3.0), subline 2.13:1 / cta 1.23:1 / eyebrow 2.66:1
  (Ziel 4.5) + Scrim-/Panel-Empfehlung; ein rein-navy Untergrund erzeugt keine Warnung.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/readability.py` — **neu** (WCAG-Kern,
  Region-Modell, Sampling, `check_contrast`/`contrast_warnings`/`recommend_contrast_fix`, CLI).
- `skills_sources/creative-studio/creative_studio/render_image.py` — `--check-contrast`-Flag +
  Post-Render-Check (additiv, Default aus).
- `skills_sources/creative-studio/tests/test_skill_074_contrast.py` — 13 Tests.
- `skills_sources/creative-studio/SKILL.md` — Abschnitt 14 + §7-Grenze aktualisiert.

## Ergebnis / Notizen
**Status review (2026-07-08).** WCAG-AA-Kontrast-Check gegen den tatsaechlichen Pixel-
Hintergrund unter dem Text, warnen-statt-blocken, opt-in (`--check-contrast`), Foto-BG-
Fix-Empfehlung (Should) mitgebaut. Kein Bestandsbruch, keine neue Dependency. `setup.ps1` gelaufen.

**Offen / [J]:** Verify-Pass (frische Session) + Outcome-Review. Region-Geometrie ist eine
Safe-Zone-/Layout-Schaetzung (keine DOM-Boxes) — bei stark abweichenden Custom-Stacks ggf.
nachjustieren. Auto-**Anwenden** eines verstaerkten Scrims (statt nur Empfehlen) ist bewusst
zurueckgestellt (Empfehlung reicht fuer Mensch-im-Loop; automatischer Scrim-Boost = Folge-Ticket).
