# SKILL-055: creative-studio — Caption-Design-Overhaul (Pill/Stroke, Kontrast, 1-Highlight, Word-Reveal)

**Status:** review
**Erstellt:** 2026-06-25
**MoSCoW:** Must
**Geschaetzter Aufwand:** M
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_reel-design-critique-content-types.md` (§1 Frame-Befund, §2 Caption-Soll) + `2026-06-24_reels-video-editing-strategy.md` (§1.2 Retention, §1.4 Captions)

> [!info] Herkunft (Frame-Critique 2026-06-25)
> Jakob zum Gold-Reel `reel_h1-immo_broll.mp4`: „nicht gut zu lesen, nicht nach Best Practice". Vier
> extrahierte Frames belegen: Captions tragen nur per `textShadow` (kein Hintergrund/Stroke) → gelbe
> Schrift auf heller Holzwand (Frame 0,5 s) und auf Laptop-Deckel (Frame 2,5 s) ist grenzwertig lesbar;
> drei gestapelte Großbuchstaben-Zeilen wirken als Textblock; `isKeyword()` färbt fast jedes Wort gelb;
> Highlight-Gelb `#ffd400` ist in `Root.tsx` hartkodiert. Best Practice 2026: **Hintergrund-Pill ODER
> harter Outline-Stroke** statt nur Shadow, **ein** Wort-Highlight pro Phrase, **1–2** aktive Wörter,
> Word-Reveal-Animation, Bold-Font (Weight 800+).

> [!note] Abgrenzung zu SKILL-043
> SKILL-043 hat den word-level Caption-Renderer **gebaut** (`Captions.tsx`, Timestamp-Mapping, Presets
> `clean/karaoke/hormozi`). Dieses Ticket **dupliziert das nicht**, sondern **verschärft die Lesbarkeit**:
> Hintergrund-Pill/Stroke-Layer, Kontrast, 1-Keyword-Logik, Word-Reveal, größere/fettere Typo — am
> bestehenden `Captions.tsx`. Es ändert keine Timestamp-/Token-Logik.

## Was soll erreicht werden? (Business-Ziel)
Captions, die auf **jedem** Footage (hell/dunkel/strukturiert) zuverlässig lesbar sind und Best-Practice
2026 entsprechen: Hintergrund-Pill **oder** Outline-Stroke, kontrastsicher, ein gezieltes Wort-Highlight,
1–2 aktive Wörter, Word-Reveal-Animation, Bold-Typo. Alle Stil-Werte bleiben Brand-Prop-getrieben
(multi-projekt). Sichtbar besser lesbar als das Ist-Gold-Reel — per Render belegt.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When eine Caption gerendert wird, the system shall hinter der aktiven Caption-Zeile einen
      **kontrastsichernden Hintergrund** legen — entweder eine halbtransparente **Pill** (Default) oder einen
      harten **Outline-Stroke** (`-webkit-text-stroke`), per Stil-Prop wählbar — **nicht** nur `textShadow`.
      → Test `test_caption_has_contrast_layer` (Frame/DOM-Snapshot: Pill-Element bzw. Stroke-Style vorhanden).
- [ ] **EARS-2:** When der Hormozi-/Highlight-Stil aktiv ist, the system shall **maximal ein** Token pro
      aktiver Phrase in der Highlight-Farbe setzen (kuratierte/positions-basierte Keyword-Wahl), nicht jedes
      Token ≥ 6 Zeichen. → Test `test_single_keyword_highlight`.
- [ ] **EARS-3:** When Captions aktiv sind, the system shall **1–2** Tokens gleichzeitig zeigen
      (`MAX_ACTIVE_TOKENS` ≤ 2, `MAX_LINE_CHARS` ≤ 18) und pro Wort eine **Reveal-Animation** (Fade+Pop via
      spring) abspielen. → Test `test_active_token_count_and_reveal`.
- [ ] **EARS-4:** When die Typo gesetzt wird, the system shall **Weight ≥ 800** und eine an Caption-
      Lesbarkeit orientierte Größe (aktiv ~9 %/Rest ~7,5 % Breite, klar über dem 48-px-Mindestmaß bei 1080)
      verwenden. → Test `test_caption_typo_weight_and_size`.
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten läuft, the system shall alle
      neuen Stil-Werte (Pill-Farbe/-Alpha, Stroke, Highlight, Caption-Font) aus **Brand-Props** beziehen —
      kein hartkodierter Brand-/Projektwert (insb. kein `#ffd400`-Literal mehr in der Komponente).
      → Test `test_caption_style_project_neutral`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `video/src/Captions.tsx` erweitern: (1) neuer Caption-Container mit
  `background`-Pill (`rgba` aus Brand-BG + Alpha-Prop, `borderRadius` aus Brand-Radius) **oder**
  `WebkitTextStroke` je `captionStyle`; (2) `isKeyword()` ersetzen durch eine **1-Keyword-pro-Phrase**-Logik
  (längstes/zahlhaltiges Token im aktiven Fenster ODER explizit markiertes Token aus der Spec); (3)
  `MAX_ACTIVE_TOKENS` auf 2, `MAX_LINE_CHARS` auf 18; (4) Word-Reveal: pro Token `spring`-Fade+translate;
  (5) `baseFontSize`/`baseWeight` anheben; (6) neue Style-Props (`captionBgAlpha`, `captionStroke`,
  `captionFont`) durch `AdReel.tsx` → `Captions` reichen, Defaults aus Brand-Props.
- **Verworfene Alternative:** Captions per ffmpeg-`drawbox` nachträglich hinterlegen — verworfen, weil
  Remotion das deterministisch als React-Layer kann (SKILL-043-Linie), batchbar + brand-getrieben.
- **Betroffene Module:** `video/src/Captions.tsx` (Hauptänderung), `video/src/AdReel.tsx` (neue Style-Props
  durchreichen), `video/src/Root.tsx` (Default-Props, `#ffd400` durch Brand-Token-Default ersetzen).
  → Architektur-Weiche: keine (ADR n/a). Token-Quelle-Andockung = SKILL-057 (additiv, nicht-blockierend).

## Technische Hinweise
- `surface: backend` — Remotion-Render headless. Verifikation: `remotion still`/Frame-Extraktion bei
  problematischem Footage (hell/Laptop) + DOM/Style-Asserts; Vergleich gegen Ist-Frames aus der Critique.
- **Kein** neuer hartkodierter Hex in `Captions.tsx` (EARS-5). `#ffd400` aus `Root.tsx`-Default zieht
  später aus `BRAND_HIGHLIGHT` (SKILL-057) — bis dahin als benannte Default-Konstante, nicht inline.
- **Lizenz-Risiko Remotion** (ab 4 Personen, SKILL.md §7) im Blick behalten (kein Blocker).

## Code-Referenzen
- `skills_sources/creative-studio/video/src/Captions.tsx` — Pill/Stroke-Layer, 1-Keyword, Word-Reveal, Typo.
- `skills_sources/creative-studio/video/src/AdReel.tsx` — neue Caption-Style-Props durchreichen.
- `skills_sources/creative-studio/video/src/Root.tsx` — Default-Props (Highlight-Default als Konstante).
- `skills_sources/creative-studio/tests/test_skill_055_caption_design.py` (neu).
- Wissensgrundlage: `2026-06-25_reel-design-critique-content-types.md` (§1, §2), `2026-06-24_reels-video-editing-strategy.md` (§1.4).

## Ergebnis / Notizen
**Umgesetzt 2026-06-25** (Implementer-Pass, Render-belegt).

- `video/src/Captions.tsx` neu: (1) Pill-Kontrast-Layer (Default) aus Brand-BG +
  `captionBgAlpha` via `hexToRgba`, Alternative harter `WebkitTextStroke` (`captionBg:"stroke"`);
  (2) `isKeyword`-Heuristik (>=6 Zeichen) ersetzt durch `pickKeywordIndex()` — GENAU EIN
  Keyword je Phrase (explizit `keyword:true` vorrangig, sonst laengstes/zahlhaltiges Token,
  Fuellwoerter <4 Zeichen ausgeschlossen); (3) `MAX_ACTIVE_TOKENS` 3→2, `MAX_LINE_CHARS` 20→18;
  (4) Wort-fuer-Wort-Reveal via `spring` pro Token-Startframe (Fade+translateY+Pop);
  (5) Typo: Aktiv-Wort `width*0.092`, Rest `width*0.078`, Weight 900; (6) Caption-Box auf 54 %
  Hoehe (eigener Pill-Hintergrund → footage-unabhaengig lesbar).
- Montserrat-Bold via `video/src/fonts.ts` (FontFace-API, lokale TTFs in `public/fonts/`,
  delayRender — offline-robust, kein Google-Fonts-Netzabruf).
- `AdReel.tsx` reicht `bg`/`captionBg`/`captionBgAlpha` an `Captions` durch; `Root.tsx`-Default
  ohne `#ffd400`-Literal (Highlight = Brand-Akzent, Font = Montserrat — SKILL-057-Kopplung).
- **Defaults (Jakob-Vorgabe):** Pill-Look, Highlight = Brand-Akzent `#f25d3e` statt Gelb,
  `BRAND_CAPTION_FONT` = Montserrat Bold — alle konfigurierbar via Spec/branding.env.

**Render-Beleg (echt):**
- AFTER: `…/Content Lake/Gold/reel_h1-immo_designv2.mp4` (Exit 0) — gleiches Reel, neuer Stil.
  VORHER bleibt `…/Gold/reel_h1-immo_broll.mp4` (Gelb, kein Pill, jedes Wort gelb).
- Vergleichs-Frames: `tests/artifacts/reel_compare_{0.5,1.5,2.5}s.png`,
  `reel_before_*.png` / `reel_after_*.png`; Klein-Proof `reel_designv2_proof.mp4` (60 KB).

**Tests:** `tests/test_skill_055_caption_design.py` (7 Tests, EARS-1..5 + Plumbing). Suite 200 passed
(Baseline 180 + 20 neu). `test_skill_045` angepasst (Highlight-Default jetzt Brand-Akzent).

**Bewusst offen/manuell:** Caption-Timing der Beleg-Reels stammt aus den Spec-`captions`
(kein Whisper-Live-Lauf — Spec von SKILL-043/056). Pill ueber Title-Card (Reel ohne B-Roll)
ueberlappt die Subline leicht — Artefakt des captions-ueber-Titlecard-Pfads, nicht des Designs.
