# SKILL-047: creative-studio — Hook-Template-Compositions (DISC-rot) + Brand-Lower-Thirds + Intro/Outro

**Status:** spec
**Erstellt:** 2026-06-24
**MoSCoW:** Should
**Geschaetzter Aufwand:** L
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_reels-video-editing-strategy.md` (§1.1 Hook, §2.3 Hook-Bibliothek, §3.4 Lower-Thirds/Intro-Outro, §7 MoSCoW Should)

> [!info] Herkunft (Recherche 2026-06-24)
> Buendelt drei verwandte Remotion-Preset-Bausteine, die alle die bestehende `AdVideo`-Mechanik (spring/
> interpolate, Brand-Tokens, Safe-Zone-Padding) wiederverwenden: (a) **Hook-Template-Compositions**
> (Big-Stat-First, Authority-Statement, Contrarian, Before/After-Zahl) als wiederverwendbare Layout-Presets
> + zugehoerige **DISC-rot-Hook-Text-Bibliothek** (MD/JSON im Repo, Ergebnis-zuerst, kein „kompliziert"),
> und (b) **Brand-Lower-Thirds + Intro/Outro-Bumper**. Ein Ticket, weil es derselbe Preset-Composition-Layer ist.

> [!note] Abgrenzung
> Die `frameworks.py`-Hook-Bibliothek (SKILL-025, `HOOKS`) liefert **generische, projektneutrale**
> Hook-Muster fuer Copy. Diese hier ergaenzte Hook-Text-Bibliothek ist **DISC-rot-tonalisiert** als
> wiederverwendbare Snippets fuer die Reel-Hook-Layouts — sie ergaenzt SKILL-025, dupliziert es nicht
> (Reel-spezifische Anwendung der generischen Muster).

## Was soll erreicht werden? (Business-Ziel)
Wiederverwendbare 9:16-Preset-Compositions: 3–5 Hook-Layouts (DISC-rot), animierte Brand-Lower-Thirds
(Name/Claim) und 1–2 s Intro/Outro-Brand-Bumper — alle Brand-Token-getrieben. Plus eine DISC-rot-Hook-
Text-Bibliothek (MD/JSON), damit Hook-Frames schnell befuellbar sind. So entstehen markenkonsistente Reels
ohne manuellen Schnitt.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein Hook-Preset-Key (`big_stat_first`/`authority_statement`/`contrarian`/
      `before_after_number`) + Text uebergeben wird, the system shall das passende 9:16-Hook-Layout rendern,
      Key-Promise im Frame **< 3 s** (Hook-Fenster), On-Screen-Text ≤ `MAX_WORDS_ONSCREEN` (7).
- [ ] **EARS-2:** When ein Brand-Lower-Third (Name/Claim) gesetzt ist, the system shall es Safe-Zone-konform
      animiert einblenden (Brand-Tokens, oberes/mittleres Drittel ueber der unteren 35 %-Zone).
- [ ] **EARS-3:** When Intro/Outro aktiviert ist, the system shall einen 1–2 s Brand-Bumper am Anfang/Ende
      einsetzen (bestehende `AdVideo`-Animations-Mechanik wiederverwendet).
- [ ] **EARS-4:** When die DISC-rot-Hook-Bibliothek geladen wird, the system shall ≥ 5 wiederverwendbare
      Hook-Snippets als MD/JSON bereitstellen (Ergebnis-zuerst, keine „kompliziert"-/Druck-Formulierung).
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall alle
      Farben/Fonts/Claims aus Brand-Props/Bibliothek-Parametern beziehen — kein hartkodierter Projektwert in
      der Composition (Hook-Bibliothek-Snippets sind als Default-Beispiele markiert, ueberschreibbar).

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Preset-Compositions in `video/src/` (z.B. `HookTemplates.tsx`, `LowerThird.tsx`,
  `Bumper.tsx`), die `AdVideo`s spring/interpolate + Safe-Zone-Padding wiederverwenden. Hook-Bibliothek als
  `templates/reel_hooks.md`/`.json` (DISC-rot-Snippets, projektneutral als Default markiert).
- **Verworfene Alternative:** Jedes Hook-Layout als komplett eigenstaendige Composition ohne geteilte
  Mechanik — verworfen (Code-Doppel, Brand-Drift). Wiederverwendung der `AdVideo`-Bausteine.
- **Betroffene Module:** `video/src/HookTemplates.tsx`/`LowerThird.tsx`/`Bumper.tsx` (neu),
  `video/src/Root.tsx`, `templates/reel_hooks.md` (+ ggf. JSON). → Architektur-Weiche: keine (ADR n/a).

## Technische Hinweise
- `surface: backend`. On-Screen-Wortgrenze gegen `frameworks.MAX_WORDS_ONSCREEN` pruefen (kein Doppelwert).
- **Lizenz-Risiko Remotion** (ab 4 Personen, SKILL.md §7) im Blick behalten.
- Voraussetzung/Nutzung: konsumiert von SKILL-045 (Reel-Spec waehlt Hook-Preset + Lower-Third-Text).

## Code-Referenzen
- `skills_sources/creative-studio/video/src/HookTemplates.tsx`, `LowerThird.tsx`, `Bumper.tsx` (neu).
- `skills_sources/creative-studio/video/src/Root.tsx` — Registrierung.
- `skills_sources/creative-studio/templates/reel_hooks.md` (+ `.json`) — DISC-rot-Hook-Bibliothek.
- `skills_sources/creative-studio/creative_studio/frameworks.py` — `MAX_WORDS_ONSCREEN` (read-only).
- Wissensgrundlage: `2026-06-24_reels-video-editing-strategy.md` (§1.1, §2.3, §3.4, §7 Should).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
