# SKILL-070: Neuer Skill `web-mobile-design` — ladbare Bau-/Review-Checkliste fuer mobil-taugliche Web-Surfaces

**Status:** review
**Erstellt:** 2026-07-03
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein` + `skill-schlanker-als-was-er-ersetzt`
**outcome_metric:** projekte_die_einen_skill_nutzen (Ziel: >= 2 Projekte mit `## Skill: web-mobile-design`-Block — Kandidaten: Immo CRM App, GuestAI, Warteliste-LP, Projekt-Cockpit/Customer-Journey-HTML) + token_saving_pro_skill_nutzung (weniger Mobil-Bug-Feedback-Schleifen)
**outcome_review_at:** null (wird beim done-Set gesetzt)

## Kontext / Trigger

Recherche- und Entscheidungs-Auftrag (Jakob, 2026-07-03): Best-Practices
mobiles/responsives Web-Design sammeln, pruefen ob es dafuer schon einen
Skill gibt (lokal + oeffentlich), abgleichen, selbst entscheiden ob ein
eigener Skill sinnvoll ist.

Jakob baut wiederkehrend Web-Surfaces ueber mehrere Projekte hinweg:
Immo CRM App (Next.js), GuestAI-Kunden-Portale, Warteliste-LP auf dem
VPS, generierte `projekt-cockpit.html` / `customer-journey.html`
(po-reconcile Living-Docs). Diese werden auf dem Smartphone benutzt, aber
kein Skill prueft heute die technische Mobil-Tauglichkeit.

## Ergebnis der Skill-Suche

**Lokal** (`~/.claude/skills/` + `skills_sources/`): kein Web-/UI-/
Frontend-/Mobile-Skill. Vorhandene beruehren das Thema nur tangential:
- `creative-studio` = Social-Ad-Creatives (Bild/Video fuer Meta), kein Web-UI.
- `reveal-presentation` = Slide-Decks fuer Beamer/Laptop (explizit KEIN Mobile-Viewport, siehe SKILL-007 Out-of-Scope).
- `dataviz` (built-in) = Chart-Farbsystem, kein Layout/Touch/Viewport.

**Oeffentlich:**
- **Anthropic `frontend-design`** (github.com/anthropics/claude-code, plugins/frontend-design) — deckt **aesthetische Richtung** ab (Palette, Typo, Layout-Idee, gegen generische Defaults). Enthaelt **keine** konkreten Mobil-/Responsive-Zahlen (keine Touch-Target-Groessen, keine WCAG-Target-Size-Werte, kein 16px-Input, kein safe-area, keine Core-Web-Vitals). Komplementaer, nicht ueberlappend.
- Community-Sammlungen (lotfb86/web-design-skills = 7-Skill-Paket, ceorkm/mobile-app-ui-design, jezweb/claude-skills u.a.) — teils gut, aber schwergewichtig (Multi-Skill-Plugins, App-UI-fokussiert) und widersprechen `skill-schlanker-als-was-er-ersetzt`. Nicht 1:1 uebernommen.

## Entscheidung (autonom, mit Begruendung)

**Ja — schlanken eigenen Skill `web-mobile-design` anlegen.** Begruendung:
1. **Luecke real:** Kein lokaler Skill deckt technische Mobil-Tauglichkeit ab; `frontend-design` (Aesthetik) laesst genau die harten Zahlen aus, die auf Mobile brechen.
2. **Multi-Projekt-tauglich** (`skill-muss-multi-projekt-tauglich-sein`): >= 4 Kandidaten-Surfaces ueber mehrere Projekte, null hartkodierter Projekt-Code.
3. **Schlank** (`skill-schlanker-als-was-er-ersetzt`): eine ladbare Checkliste + 12-Regel-Tabelle + Copy-paste-Baseline; keine Tools, keine Generatoren, kein Multi-Skill-Plugin. Kosten ~ ein Load, Nutzen = vermiedene Mobil-Bug-Feedback-Schleifen (Zoom-Falle, Horizontal-Scroll, unsichtbarer Fokus).
4. **Kein Over-Engineering:** bewusst KEIN Screenshot-Automations-Tooling in v0.1 (anders als reveal SKILL-007). Erst wenn Live-Use zeigt, dass ein Viewport-Screenshot-Pass sich lohnt, als Folge-Ticket.

## Was angelegt wurde

- `skills_sources/web-mobile-design/SKILL.md` (NEU) — Frontmatter + 7 Sektionen: Aktivierung/Abgrenzung, Heuristik, 12-Regel-Tabelle mit Quellen, Fertig-Checkliste, Anti-Pattern-Block, Copy-paste-Baseline, Quellenliste, CLAUDE.md-Aktivierungsblock.
- `docs/tickets/web-mobile-design/` + `verify/.gitkeep` (NEU) — Ticket-Verzeichnis nach Substruktur-Konvention.
- Dieses Ticket.

## Akzeptanzkriterien (EARS)

- [x] When der Skill angelegt ist, the system shall `skills_sources/web-mobile-design/SKILL.md` mit gueltigem Frontmatter (`name`, `version`, `description`) enthalten.
- [x] When ein Agent die Mobil-Tauglichkeit prueft, the system shall eine abhakbare Fertig-Checkliste bereitstellen, die mindestens Touch-Targets, 16px-Input, Viewport-Meta, Horizontal-Scroll, Kontrast und sichtbaren Fokus abdeckt.
- [x] When eine Regel genannt wird, the system shall eine autoritative Quelle (Apple HIG / Material 3 / WCAG 2.2 / web.dev / MDN / NN/g) verlinken.
- [x] When der Skill aktiviert wird, the system shall sich von `frontend-design` (Aesthetik) und `creative-studio` (Ad-Creatives) explizit abgrenzen (kein Scope-Overlap).
- [x] When der Skill kein Projekt-spezifisches Detail braucht, the system shall keinen hartkodierten Projekt-Pfad/-Wert enthalten (`skill-muss-multi-projekt-tauglich-sein`).
- [ ] When ein Deploy noetig ist, the system shall via `setup.ps1` nach `~/.claude/skills/web-mobile-design/` gespiegelt werden. **[J] — setup.ps1 noch nicht ausgefuehrt (Deploy-Hinweis unten).**

## Deploy-Hinweis [J]

Skill-Source liegt in `skills_sources/`, ist aber noch **nicht deployed**.
Damit er im laufenden Harness aktiv wird, einmalig ausfuehren:

```powershell
cd C:\claude_projekte\Schaltzentrale; .\setup.ps1
```

(Bewusst nicht vom Subagent ausgefuehrt — nur Schaltzentrale-Repo-Files
angelegt, kein Deploy getriggert.)

## Out of Scope (v0.1)

- **Screenshot-/Viewport-Automation** (headless-Chromium-Mobil-Pass wie reveal SKILL-007) — erst bei belegtem Live-Bedarf als Folge-Ticket.
- **Framework-spezifische Rezepte** (React/Tailwind/Next-Patterns) — bleibt generisch HTML/CSS, damit projekt-agnostisch.
- **Automatisierte A11y-Audits** (axe/Lighthouse-Runner) — Checkliste ist manuell/heuristisch; Runner waere separates Tooling (Out-of-Scope der Vision: "Allgemeines Tooling").
- **Aesthetische Richtung** — bleibt `frontend-design`.

## Verknuepfte Tickets / Skills

- Komplementaer: `frontend-design` (extern, Aesthetik), `creative-studio` (Ad-Creatives), `dataviz` (Chart-Farben).
- Muster-Vorbild fuer Ticket-Aufbau: SKILL-007 (reveal Visual-Review), bewusst OHNE dessen Tooling-Schwere uebernommen.

## Nachtrag 2026-07-03 — Encoding-Sicherheit (additiv)

Anlass: heute ist beim skriptbasierten CSS-Fix ueber die Landing-Pages der
Umlaut-Content **live kaputtgegangen** (echter Datei-Schaden, doppeltes
Mojibake `ae` → `Ã¤` → `ÃƒÂ¤`) — PowerShell 5.1 liest UTF-8 ohne
`-Encoding UTF8` als Windows-1252 und schreibt Mojibake zurueck.

Additiv in `skills_sources/web-mobile-design/SKILL.md` ergaenzt:
- Neuer **Abschnitt 5 „Encoding-Sicherheit (UTF-8 / Umlaute — harte Regel)"**
  mit Anti-Pattern-Callout: kein PowerShell-`Get-Content -Raw`-Roundtrip ohne
  `-Encoding UTF8`; Lesen via `[IO.File]::ReadAllText(..UTF8)`, Schreiben via
  `WriteAllText(..UTF8Encoding($false))` (ohne BOM); Bash-Heredoc/echo/cat fuer
  Umlaut-Content meiden; `<meta charset="UTF-8">` Pflicht;
  Doppel-Mojibake-Reparatur (2x 1252-Decode); bevorzugt Edit/Write-Tool statt
  Shell-Roundtrip.
- Neuer **Fertig-Checklisten-Punkt:** „Umlaute intakt nach jedem
  skriptbasierten Edit (`fuer`/`Gaeste`/`persoenlich` korrekt, kein `Ã` im
  File) — VOR dem Deploy."
- Folge-Abschnitte umnummeriert (Copy-paste-Baseline → 6, Quellen → 7,
  Aktivierung → 8); Frontmatter-`description` um UTF-8-Klausel ergaenzt.

Skill bleibt schlank (kein Tooling, nur Regel + Check). Deploy via setup.ps1
bleibt [J].

## Nachtrag 2026-07-03 — Layout-Rezepte (additiv)

Anlass: Jakobs Landing-Pages sahen **mobil schlecht aus**. Zwei konkrete
Root-Causes im Code bestaetigt: (1) feste `@media(min-width:760px){1fr 1fr}`-
Spalten — auf grossen Phones/kleinen Tablets stehen Karten nebeneinander statt
gestapelt, teils Horizontal-Overflow auf 360 px; (2) feste kleine rem-Schriften
ohne `clamp` (`.cell{.94rem}`=15px, `.head{.8rem}`=13px) → Text/Headlines zu
klein. Der Skill hatte die technischen Checks (Touch-Target, 16px-Input,
Viewport, CWV), aber **keine Layout-Rezepte** gegen genau diese Symptome.

Quelle der Rezepte: `skill_dev/research/2026-07-03_responsive-design-candidates.md`
(Subagent-Recherche; Empfehlung „SKILL-070 behalten und erweitern, kein
Fremd-Skill" bestaetigt).

Additiv in `skills_sources/web-mobile-design/SKILL.md` ergaenzt:
- Neuer **Abschnitt 4 „Layout-Rezepte (Stapeln / fluide Skala / CTA)"** mit drei
  kompakten, token-kompatiblen (`var(--brand-*)`, kein Framework) Snippets:
  1. **Auto-Stack-Grid** statt fester Breakpoints:
     `grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr))`
     (stapelt automatisch, kein Media-Query, kein Overflow auf 360 px).
  2. **Fluide Typo mit hohen Mobile-Minima** (Utopia-clamp): Body nie < 1.125rem
     (~18px), H1-Minimum >= ~2.25rem (~36px), z.B.
     `h1: clamp(2.25rem,1.7rem+2.6vw,3rem)`, `p: clamp(1.125rem,1.05rem+0.5vw,1.35rem)`.
     Kernregel: feste rem-Schriften ohne `clamp` = Fail; Fliesstext nie < 18px.
  3. **Voll-breite + zentrierte CTAs**: `.btn{justify-content:center;text-align:center}`
     + `@media(max-width:560px){.btn{display:block;width:100%}}` + Button-Block
     zentriert via `.cta-wrap{display:flex;flex-direction:column;align-items:center}`.
- **Methodik-Quellen** als `[!note]`-Callout: Every Layout (Switcher/Stack) +
  Utopia.fyi — **bewusst als Muster adaptiert, NICHT als abhaengiger Fremd-Skill
  eingebunden** (schlank halten, keine externe Skill-Abhaengigkeit).
- **Fertig-Checkliste** um drei Punkte erweitert: „keine festen Spalten-
  Breakpoints (auto-fit nutzen)", „Fliesstext-clamp-Minimum >= 18px",
  „Primaer-CTA voll-breit + zentriert auf Mobile".
- Folge-Abschnitte umnummeriert (Fertig-Checkliste → 5, Encoding → 6,
  Copy-paste-Baseline → 7, Quellen → 8, Aktivierung → 9); interne Verweise
  („Abschnitt 5/6") und Frontmatter-`description` (Layout-Rezepte-Klausel)
  angepasst.

Skill bleibt schlank (3 Snippets + 3 Checklisten-Punkte, kein Tooling).
**Status bleibt `review`.** Deploy via `setup.ps1` bleibt [J].

## Ergebnis / Notizen

Skill in einem Pass gebaut (Recherche via Subagent aus autoritativen
Primaerquellen 2025/2026). Verify-Pass durch frischen Verifier-Subagent
empfohlen vor `done` (liest SKILLS_VISION.md + dieses Ticket + die
tatsaechliche SKILL.md).
