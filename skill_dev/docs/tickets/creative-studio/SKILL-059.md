# SKILL-059: creative-studio — Caption-Stil-Preset-Bibliothek (clean/karaoke/hormozi/pill/stroke)

**Status:** spec
**Erstellt:** 2026-06-25
**MoSCoW:** Could
**Geschaetzter Aufwand:** S
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_reel-design-critique-content-types.md` (§2 Caption-Soll) + `2026-06-24_reels-video-editing-strategy.md` (§7 Could „Caption-Stil-Presets-Bibliothek")

> [!info] Herkunft (Critique 2026-06-25 + Recherche-Could)
> Die Critique zeigt, dass je nach Footage mal eine **Pill** (helle/strukturierte Hintergründe), mal ein
> **Stroke** (saubere Hintergründe, softer Look) optimal ist. Die Reels-Strategie-Recherche listet
> „Caption-Stil-Presets-Bibliothek" bereits als Could. SKILL-055 baut die Lesbarkeits-Mechanik; dieses
> Ticket macht daraus eine **wählbare Preset-Bibliothek** mit dokumentierten Looks pro Use-Case.

> [!note] Abgrenzung zu SKILL-055
> SKILL-055 implementiert Pill/Stroke/Highlight/Reveal als Fähigkeit (Must). SKILL-059 (Could) **kuratiert**
> daraus benannte, dokumentierte Presets (`clean`, `karaoke`, `hormozi`, `pill`, `stroke`) inkl. Empfehlung
> „welcher Look für welches Footage", per einzelnem `caption_style`-Token wählbar. Kein Doppel — reine
> Konfigurations-/Kuratierungs-Ebene über SKILL-055.

## Was soll erreicht werden? (Business-Ziel)
Eine dokumentierte Caption-Stil-Preset-Bibliothek, sodass pro Reel mit **einem** Token (`caption_style`)
ein erprobter, lesbarer Look gewählt wird — inkl. Guidance „welcher Look bei welchem Footage" (Pill bei
hell/strukturiert, Stroke bei sauber/soft). Beschleunigt konsistente, lesbare Reels ohne Pro-Reel-Styling.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein `caption_style`-Key (`clean`/`karaoke`/`hormozi`/`pill`/`stroke`) gesetzt ist,
      the system shall das zugehörige, dokumentierte Stil-Set (Hintergrund-Typ, Highlight, Größe, Animation)
      auf die SKILL-055-Caption-Mechanik anwenden. → Test `test_caption_preset_resolves`.
- [ ] **EARS-2:** When ein unbekannter `caption_style`-Key übergeben wird, the system shall klar warnen/auf
      einen sicheren Default (`pill`) zurückfallen — kein stilloses/leeres Rendern. → Test `test_caption_preset_unknown_fallback`.
- [ ] **EARS-3:** When die Preset-Bibliothek dokumentiert ist, the system shall pro Preset eine
      Footage-Empfehlung bereitstellen (Pill = hell/strukturiert, Stroke = sauber/soft, hormozi = max.
      Aufmerksamkeit). → Check `test_caption_preset_docs_present`.
- [ ] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten läuft, the system shall die
      Presets ausschließlich über Brand-Props parametrisieren — kein projektspezifischer Wert im Preset.
      → Test `test_caption_preset_project_neutral`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Ein Preset-Mapping (`caption_presets` in `creative_studio/` bzw. als Style-Tabelle
  in `Captions.tsx`), das je Key die SKILL-055-Stil-Props (`bg`-Typ, `highlight`, `fontScale`, `animation`)
  setzt; Doku als `templates/caption_styles.md` (Look + Footage-Empfehlung + Beispiel). Reel-Spec wählt per
  `caption_style`.
- **Verworfene Alternative:** Jeden Look als eigene Caption-Komponente — verworfen (Code-Doppel); Presets
  sind Konfiguration über die eine SKILL-055-Mechanik.
- **Betroffene Module:** `video/src/Captions.tsx` (Preset-Resolver), `creative_studio/reel_spec.py`
  (`caption_style`-Validierung), `templates/caption_styles.md` (neu). → Architektur-Weiche: keine.

## Technische Hinweise
- `surface: backend`. Abhängig von SKILL-055 (liefert die Mechanik) — erst danach umsetzen.
- Reine Kuratierung; kein neuer Render-Pfad. Klein gehalten (Could).

## Code-Referenzen
- `skills_sources/creative-studio/video/src/Captions.tsx` — Preset-Resolver über SKILL-055-Mechanik.
- `skills_sources/creative-studio/creative_studio/reel_spec.py` — `caption_style`-Validierung.
- `skills_sources/creative-studio/templates/caption_styles.md` (neu) — Preset-Doku + Footage-Empfehlung.
- `skills_sources/creative-studio/tests/test_skill_059_caption_presets.py` (neu).
- Wissensgrundlage: `2026-06-25_reel-design-critique-content-types.md` (§2), `2026-06-24_reels-video-editing-strategy.md` (§7 Could).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
