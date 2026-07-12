# SKILL-102: creative-studio — Ad-Visual-Regeln: CTA immer als Button + Foto-Text nie ueber Gesicht

**Status:** in_progress
**Erstellt:** 2026-07-12
**MoSCoW:** Must
**Geschaetzter Aufwand:** S (CTA-Button-Flag umgesetzt; Face-Safe-Placement als Regel + Smartcrop-Ausbau)
**surface:** code + docs
**vision_principle:** creatives-muessen-plattform-konform-und-lesbar-sein
**outcome_metric:** cta_immer_als_button + text_nie_ueber_gesicht

## Kontext / Root-Cause
Jakob-Feedback (2026-07-12) am Agentic-Messaging-Test:
1. **CTA immer als Button** abbilden (nicht als schlichter Text-Link). Bisher koppelte
   `--chrome minimal` den CTA-Pill an den vollen Chrome (Balken + Brand-Name) — Button gab es
   nur mit `--chrome full`, was aber Top-Balken/Brand-Name mitbringt (unerwuenscht).
2. **Foto-Text nie ueber dem Gesicht:** Bei Creatives mit Personen-/Founder-Fotos darf der Text
   nicht direkt ueber dem Gesicht liegen.

## Was soll erreicht werden?
- Ein CTA laesst sich als **Pill-Button** rendern, **ohne** den restlichen Chrome (kein
  Top-Balken, kein Brand-Name) — organischer Look **mit** Button.
- Foto-Layouts (`photo-poster`) platzieren den Text **face-safe**: Gesicht bleibt frei, Text in
  der gesichtsfreien Zone (i.d.R. unten). Der Vision-QA-Pass prueft das je Format.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, CTA-Button-Flag]:** `render_image` bietet `--cta-button`, das den CTA-Pill
      auch bei `--chrome minimal` erzwingt (Button ohne Top-Balken/Brand-Name).
      Umgesetzt: `DEFAULT_STYLE["cta_button"]`, `chrome_pill = chrome_full or cta_button`,
      CLI-Flag + Style-Weitergabe (`creative_studio/render_image.py`).
- [ ] **EARS-2 [Should, Button = Default fuer Ads]:** Der Standard-Ad-Satz rendert den CTA als
      Button (Text-Link nur auf ausdruecklichen Wunsch). In SKILL.md Abschnitt 2/12 vermerken.
- [ ] **EARS-3 [Must, Face-Safe-Text]:** Bei `photo-poster` mit erkanntem Gesicht liegt kein
      Text ueber dem Gesicht. Regel: Smartcrop/Placement haelt das Gesicht in der
      text-freien Zone (Text ist bottom-anchored → Gesicht gehoert in die obere Bildhaelfte);
      der Vision-QA-Pass (Abschnitt 15) verifiziert je Format (1:1/4:5/9:16) einzeln.
- [ ] **EARS-4 [Should, Smartcrop face-aware ausbauen]:** Smartcrop (SKILL-032) bevorzugt Crops,
      die das Gesicht aus der unteren Textzone halten; wo unmoeglich, Warnung (keine Sperre) +
      Fallback (anderes Motiv/Format-spezifischer Crop).

## Loesungs-Skizze
- CTA-Button: umgesetzt (siehe EARS-1).
- Face-Safe: Kurzfristig ueber Vision-QA-Pflicht (Text-ueber-Gesicht = QA-Fail → anderes Motiv/
  Crop). Mittelfristig Smartcrop-Salienz um eine „Textzone-frei-halten"-Randbedingung erweitern.
- SKILL.md Abschnitt 2 (Standard-Ad-Satz) + 12 (Layouts) um beide Regeln ergaenzen.

## Test-Ergebnis / Beleg
- CTA-Button: verifiziert an der Referenz-Instanz `messaging-test-2026-07` (alle Ads mit Button).
- Face-Safe: Vision-QA je Foto-Ad (Founder-Fotos evisible) in allen 3 Formaten.

## Code-Referenzen
- `creative_studio/render_image.py` (`DEFAULT_STYLE`, `_style_ctx`, `--cta-button`)
- `templates/ad_image.html.j2` (`.cta` Pill vs. `.cta-link`, `chrome_pill`)
- Smartcrop: SKILL-032 (`creative_studio/*` Bild-Pipeline)
