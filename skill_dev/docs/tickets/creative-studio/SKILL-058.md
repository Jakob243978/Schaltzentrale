# SKILL-058: creative-studio — Hook-Title-Card-Redesign (Daumenstopp im ersten Frame)

**Status:** spec
**Erstellt:** 2026-06-25
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_reel-design-critique-content-types.md` (§1 Hook-Wirkung, §2 Hook-Title-Card-Soll) + `2026-06-24_reels-video-editing-strategy.md` (§1.1 Hook, §1.5 Text-on-Screen)

> [!info] Herkunft (Frame-Critique 2026-06-25)
> Frame 0,5 s des Gold-Reels zeigt nur „3 / STUNDEN" klein-gelb auf heller Holzwand — **kein
> scroll-stoppendes Visual**, schwacher Kontrast, kein dedizierter Hook-Frame. Bis zu 50 % springen in
> den ersten 3 s ab (Recherche §1.1); der stärkste Daumenstopp-Hebel (großer, kontrastreicher
> Ergebnis-/Zahl-Hook im **ersten** Frame) ist verschenkt. Das Reel startet direkt mit kleinen
> word-level Captions statt mit einem Hook-Statement.

> [!note] Abgrenzung zu SKILL-047
> SKILL-047 (Should, noch `spec`) definiert die **Hook-Template-Compositions** (Big-Stat-First,
> Authority, Contrarian, Before/After) als Bausteine. Dieses Ticket **dupliziert sie nicht**, sondern
> verdrahtet ein **dediziertes Hook-Fenster (0–~1,5 s)** als ersten Layer im Reel-/Talking-Head-Pfad:
> großer Hook-Frame statt klein-gelber Erst-Caption. Wenn SKILL-047 die Layouts liefert, nutzt 058 sie;
> bis dahin baut 058 die Big-Stat-First-Variante minimal selbst (aus `AdVideo`-Mechanik).

## Was soll erreicht werden? (Business-Ziel)
Ein dediziertes **Hook-Fenster** in den ersten ~0–1,5 s jedes Reels: großer, kontrastreicher Ergebnis-/
Zahl-Hook (Big-Stat-First, DISC-rot) auf Brand-BG **oder** mit kräftiger Caption-Pill über dem Footage —
statt der heutigen kleinen 2-Wort-Caption auf hellem Hintergrund. Maximiert den 3-Sekunden-Hold
(Daumenstopp im ersten Frame). Brand-Token-getrieben, multi-projekt.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein Reel mit Hook-Text rendert, the system shall in den **ersten ~0–1,5 s** einen
      dedizierten Hook-Frame zeigen — großer Ergebnis-/Zahl-Text (deutlich größer als die laufenden
      Captions), kontrastsicher (Brand-BG-Frame ODER Caption-Pill über Footage). → Test `test_hook_window_present`.
- [ ] **EARS-2:** When der Hook-Frame rendert, the system shall On-Screen-Text ≤ `MAX_WORDS_ONSCREEN` (7)
      halten und die Key-Promise vollständig **vor** Sekunde 3 zeigen (Hook-Fenster). → Test `test_hook_word_limit_and_timing`.
- [ ] **EARS-3:** When das Hook-Fenster endet, the system shall sauber in die laufenden Captions / das
      Footage übergehen (Fade/Cut), ohne den bestehenden Pfad zu brechen (Reel ohne Hook-Text rendert
      weiter). → Tests `test_hook_handoff`, `test_no_hook_text_path`.
- [ ] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten läuft, the system shall
      Hook-Text, Farben, Font aus Props/Spec beziehen — kein hartkodierter Projektwert. → Test `test_hook_card_project_neutral`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Ein Hook-Layer (`video/src/HookTitleCard.tsx` bzw. — falls SKILL-047 vorhanden —
  dessen `big_stat_first`-Preset) wird als erste Sequence (`Series.Sequence`/`Sequence` mit `durationInFrames`
  ~45 bei 30 fps) vor dem laufenden Caption-/Footage-Layer in `AdReel`/`TalkingHead` eingehängt. Großer
  `fontSize` (~12–16 % Breite), Brand-Akzent für die Zahl, kontrastsichere Fläche (BG-Frame oder Pill aus
  SKILL-055/057-Tokens). Spec (SKILL-045) bekommt additiv `hook_card: true|false` (Default an, wenn `hook`
  gesetzt). Wortlimit gegen `frameworks.MAX_WORDS_ONSCREEN`.
- **Verworfene Alternative:** Den Hook nur als größere erste Caption ausführen — verworfen, weil ein
  dedizierter Hook-Frame (eigenes Layout, Brand-Akzent, garantierter Kontrast) den Daumenstopp zuverlässiger
  liefert als eine vergrößerte Caption auf zufälligem Footage.
- **Betroffene Module:** `video/src/HookTitleCard.tsx` (neu, oder SKILL-047-Preset nutzen),
  `video/src/AdReel.tsx` + `video/src/TalkingHead.tsx` (Hook-Sequence einhängen), `video/src/Root.tsx`,
  `creative_studio/reel_spec.py` (`hook_card`-Feld), `frameworks.py` (`MAX_WORDS_ONSCREEN`, read-only).
  → Architektur-Weiche: keine (ADR n/a).

## Technische Hinweise
- `surface: backend`. Verifikation: Frame-Extraktion bei t=0,3 s → großer Hook-Text sichtbar + Wortlimit-
  Assert. Kombiniert sich mit SKILL-055 (Pill) und SKILL-057 (Tokens).
- Abhängigkeit: nutzt SKILL-047-Hook-Layouts, wenn fertig — sonst minimale Big-Stat-First-Eigenbau-Variante.
- **Lizenz-Risiko Remotion** (ab 4 Personen, SKILL.md §7).

## Code-Referenzen
- `skills_sources/creative-studio/video/src/HookTitleCard.tsx` (neu) bzw. SKILL-047 `HookTemplates.tsx`.
- `skills_sources/creative-studio/video/src/AdReel.tsx`, `TalkingHead.tsx` — Hook-Sequence einhängen.
- `skills_sources/creative-studio/creative_studio/reel_spec.py` — `hook_card`-Feld.
- `skills_sources/creative-studio/creative_studio/frameworks.py` — `MAX_WORDS_ONSCREEN` (read-only).
- `skills_sources/creative-studio/tests/test_skill_058_hook_title_card.py` (neu).
- Wissensgrundlage: `2026-06-25_reel-design-critique-content-types.md` (§1, §2), `2026-06-24_reels-video-editing-strategy.md` (§1.1, §1.5).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
