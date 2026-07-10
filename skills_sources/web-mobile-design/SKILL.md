---
name: web-mobile-design
version: 0.1
description: Ladbare Checkliste + Heuristik fuer mobil-taugliches, responsives Web-Design. Aktivieren beim Bauen ODER Reviewen einer Web-Surface (Landing-Page, App-UI, HTML-Cockpit/-Dashboard, Formular, Warteliste, Kunden-Portal) — kurz bevor du HTML/CSS schreibst und bevor du "fertig" meldest. Deckt Touch-Targets (44px/48dp, WCAG 2.5.5/2.5.8), Thumb-Zone/CTA-Platzierung, Mobile-First-Breakpoints, Layout-Rezepte (Auto-Stack-Grid statt fester Spalten-Breakpoints, fluide Typo-Skala mit hohen Mobile-Minima, voll-breite zentrierte CTAs), fluide Typografie (clamp), 16px-Input-Regel (iOS-Zoom), Viewport-Meta + safe-area-insets, kein Horizontal-Scroll, Core Web Vitals (LCP/CLS/INP), Mobile-Formulare (type/inputmode/autocomplete), A11y (Kontrast 4.5:1, sichtbarer Fokus) und UTF-8/Umlaut-sicheres Editieren (kein PowerShell-Roundtrip ohne -Encoding UTF8). NICHT fuer aesthetische Richtung (dafuer frontend-design) oder Ad-Creatives (dafuer creative-studio).
---

# web-mobile-design

Schlanke, ladbare **Bau- und Review-Checkliste** fuer jede Web-Surface, die
auf dem Smartphone benutzt wird. Ersetzt kein Design-System und keine
aesthetische Richtung — er ist die **Qualitaets-Gitter**, das verhindert,
dass eine Surface auf Mobile bricht (Zoom-Falle, unklickbare Buttons,
Horizontal-Scroll, unsichtbarer Fokus).

## 1. Wann aktivieren

- Du baust oder aenderst eine **Web-Surface** (Landing-Page, App-UI,
  HTML-Cockpit/-Dashboard, Formular, Warteliste-LP, Kunden-Portal,
  Customer-Journey-HTML).
- Du machst einen **Review** einer bestehenden Surface auf Mobil-Tauglichkeit.
- **Timing:** einmal *bevor* du das erste HTML/CSS schreibst (Heuristik unten
  im Kopf behalten) und einmal *bevor du "fertig" meldest* (Checkliste in
  Abschnitt 5 durchgehen).

**Abgrenzung (nicht hier):**
- Aesthetische Richtung (Palette, Typo-Persoenlichkeit, Layout-Idee) →
  `frontend-design`-Skill.
- Social-/Ad-Creatives (Bild/Video fuer Meta) → `creative-studio`-Skill.
- Charts/Dashboards-Farbsystem → `dataviz`-Skill.
Dieser Skill kommt **zusaetzlich** dazu und prueft die technische
Mobil-Tauglichkeit.

## 2. Heuristik (vor dem Bauen — im Kopf behalten)

1. **Mobile-First.** Entwirf zuerst fuer den kleinsten Screen (~360 px),
   dann per `min-width`-Media-Queries erweitern. Content first, Navigation
   second.
2. **Daumen regiert.** ~75 % der Interaktionen laufen ueber den Daumen,
   ~49 % bedienen einhaendig. Primaere Aktion / Haupt-Navigation gehoert in
   die **untere Bildschirm-Zone** (Bottom-Nav / Sticky-CTA unten), nicht in
   die schwer erreichbaren oberen Ecken.
3. **Fluide statt fix.** Grid/Flex + relative Einheiten + `clamp()` statt
   Pixel-Breiten und Media-Query-Typo-Stufen.
4. **Die Surface darf nie horizontal scrollen.** Breite Elemente (Tabellen,
   Code, Diagramme) bekommen einen eigenen `overflow-x:auto`-Container.

## 3. Die 12 tragenden Regeln (mit Quelle)

| # | Regel | Konkret | Quelle |
|---|---|---|---|
| 1 | **Touch-Target-Groesse** | >= 44x44 px (iOS) bzw. 48x48 dp (Android). WCAG AA-Minimum (2.5.8): 24x24 CSS-px; AAA (2.5.5): 44 px. Praxis-Ziel = 44/48. | Apple HIG; Material 3; [WCAG 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) |
| 2 | **Target-Abstand** | >= 8 dp zwischen Targets; 24-px-Kreis um den Mittelpunkt darf keinen Nachbarn schneiden (2.5.8-Ausnahme). | [WCAG 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) |
| 3 | **Viewport-Meta** | `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`. **Kein** `user-scalable=no` / `maximum-scale=1` (verletzt Zoom / WCAG 1.4.4). | [MDN viewport](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport) |
| 4 | **Safe-Area-Insets** | `padding: env(safe-area-inset-*)` fuer Notch / Home-Indicator / runde Ecken. Braucht `viewport-fit=cover`. | [MDN env()](https://developer.mozilla.org/en-US/docs/Web/CSS/env) |
| 5 | **16px-Input-Regel** | Schriftgroesse auf `input`/`select`/`textarea` >= 16 px, sonst zoomt iOS-Safari beim Fokus rein. Bevorzugt via `@media (pointer: coarse)`. | [CSS-Tricks](https://css-tricks.com/16px-or-larger-text-prevents-ios-form-zoom/) |
| 6 | **Fluide Typografie** | `font-size: clamp(min, vw-preferred, max)`. Max-Wert >= 2x Min-Wert, damit 200%-Zoom moeglich bleibt. | [web.dev clamp](https://web.dev/articles/min-max-clamp) |
| 7 | **Kein Horizontal-Scroll** | `width=device-width`, `max-width:100%` auf Medien, breite Bloecke in `overflow-x:auto`. Body scrollt nie seitlich. | [web.dev design](https://web.dev/learn/design/) |
| 8 | **CTA in Daumen-Zone** | Primaere Aktion / Navigation unten (Bottom-Nav / Sticky-CTA), nicht oben. | [Smashing Thumb-Zone](https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/) |
| 9 | **Core Web Vitals** | LCP <= 2,5 s; CLS <= 0,1; INP <= 200 ms (INP hat FID im Maerz 2024 ersetzt). Bilder mit Breite/Hoehe gegen CLS. | [web.dev Vitals](https://web.dev/articles/vitals) |
| 10 | **Mobile-Formulare** | Passende `type` (`email`/`tel`/`url`/`number`/`date`) + `inputmode` (z.B. `numeric`) + `autocomplete`-Tokens. Kein `autocomplete="off"`. | [web.dev forms](https://web.dev/learn/forms/attributes) |
| 11 | **Kontrast** | Text >= 4,5:1 (grosser Text / Non-Text-UI >= 3:1). | [WCAG 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum) |
| 12 | **Sichtbarer Fokus** | Tastatur-Fokus muss sichtbar sein: >= 2 px Rahmen, >= 3:1 Kontrast fokussiert/unfokussiert. Nie `outline:none` ohne Ersatz. | [WCAG 2.4.11](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html) |

## 4. Layout-Rezepte (Stapeln / fluide Skala / CTA)

Token-kompatibel (`var(--brand-*)`, kein Framework). Diese Rezepte schliessen
die Luecke, die feste Breakpoint-Spalten und feste kleine rem-Schriften auf
grossen Phones/Tablets reissen (Anlass: Landing-Pages sahen mobil schlecht aus).

### Auto-Stack-Grid statt fester Breakpoints

```css
.grid {
  display: grid;
  gap: 16px;
  /* stapelt automatisch, kein Media-Query; min() verhindert Overflow < 280px */
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
}
```

Ersetzt fragiles `@media (min-width:760px){ ...1fr 1fr }` — das kippt auf
grossen Phones/kleinen Tablets zu Spalten-nebeneinander statt gestapelt und
kann auf 360 px horizontal ueberlaufen.

### Fluide Typo mit HOHEN Mobile-Minima (Utopia-clamp)

```css
:root {
  --step-0: clamp(1.125rem, 1.05rem + 0.5vw, 1.35rem);  /* Body: nie < 18px */
  --step-4: clamp(2.25rem,  1.7rem  + 2.6vw, 3rem);      /* H1:  min ~36px */
}
h1     { font-size: var(--step-4); }
p, li  { font-size: var(--step-0); }
```

Kernregel: **feste rem-Schriften ohne `clamp` sind ein Fail.** Fliesstext nie
unter 1.125rem (~18px), H1-Minimum >= ~2.25rem (~36px). Kleintext wie
`.cell{font-size:.94rem}` (=15px) oder `.head{font-size:.8rem}` (=13px) ist der
direkte Grund fuer „zu klein" auf Mobile.

### Voll-breite, zentrierte CTAs auf Mobile

```css
.btn      { display: inline-flex; justify-content: center; text-align: center; }
.cta-wrap { display: flex; flex-direction: column; align-items: center; }
@media (max-width: 560px) {
  .btn { display: block; width: 100%; box-sizing: border-box; }
}
```

`justify-content:center` = Label mittig (oft vergessen → linksbuendiger Text);
`.cta-wrap{align-items:center}` zentriert den Button-Block selbst, auch wenn er
nicht voll-breit ist.

> [!note] Methodik-Quellen (bewusst NICHT als Fremd-Skill uebernommen)
> Every Layout (Switcher/Stack — auto-stack ohne Media-Query) und Utopia.fyi
> (fluide `clamp`-Formel + Rechner) sind die Methodik hinter diesen Rezepten.
> Als Muster adaptiert, nicht als abhaengiger Skill eingebunden.
> https://every-layout.dev/layouts/ · https://utopia.fyi/blog/clamp/

## 5. Fertig-Checkliste (vor Uebergabe abhaken)

Vor "fertig" jede Zeile pruefen — im Zweifel real im schmalen Viewport
(~375 px) oder per Screenshot ansehen, nicht nur im Quellcode annehmen.

- [ ] Viewport-Meta korrekt gesetzt (`width=device-width, initial-scale=1, viewport-fit=cover`), **kein** `user-scalable=no`.
- [ ] Alle Buttons/Links/Icons >= 44 px effektive Klickflaeche, >= 8px Abstand.
- [ ] Alle Text-Inputs haben >= 16px Schrift (kein iOS-Zoom beim Fokus).
- [ ] Kein horizontaler Scroll bei 360-390 px Breite; breite Tabellen/Code in `overflow-x:auto`.
- [ ] Keine festen Spalten-Breakpoints — `auto-fit`/`minmax(min(100%,280px),1fr)` nutzen (stapelt automatisch).
- [ ] Fliesstext-`clamp`-Minimum >= 18px (1.125rem); keine festen rem-Schriften ohne `clamp`.
- [ ] Primaer-CTA voll-breit + zentriert auf Mobile (`justify-content:center` + `width:100%` unter 560px).
- [ ] Typo skaliert per `clamp()`; bei 200% Zoom bleibt alles lesbar/bedienbar.
- [ ] `env(safe-area-inset-*)` beruecksichtigt, falls fixe/sticky Bottom-Elemente (iPhone-Notch/Indicator).
- [ ] Primaere CTA / Navigation in der unteren Daumen-Zone erreichbar.
- [ ] Formulare: korrekte `type` + `inputmode` + `autocomplete`-Tokens.
- [ ] Text-Kontrast >= 4,5:1, UI/grosser Text >= 3:1.
- [ ] Sichtbarer Fokus-Indikator auf allen interaktiven Elementen (nie `outline:none` ohne Ersatz).
- [ ] Bilder mit `width`/`height` (oder `aspect-ratio`) gegen Layout-Shift (CLS).
- [ ] Kurzer Blick auf LCP-Element (grosses Hero-Bild vorab laden / dimensionieren).
- [ ] Umlaute intakt nach jedem skriptbasierten Edit (`fuer`/`Gaeste`/`persoenlich` korrekt, kein `Ã` im File) — siehe Abschnitt 6.

> [!warning] Anti-Pattern: "sieht am Desktop gut aus = fertig"
> Nie "fertig" melden ohne die schmale Viewport-Ansicht (~375 px) real
> geprueft zu haben. Die drei haeufigsten Mobil-Bugs — Zoom-beim-Fokus
> (Input < 16px), Horizontal-Scroll (fixe Breite / Tabelle) und
> unsichtbarer Fokus (`outline:none`) — sind aus dem Desktop-Bild allein
> nicht erkennbar.

## 6. Encoding-Sicherheit (UTF-8 / Umlaute — harte Regel)

> [!warning] Anti-Pattern: deutschen HTML-Content ueber PowerShell roundtrippen
> Anlass 2026-07-03: ein skriptbasierter CSS-Fix ueber die Landing-Pages hat
> die Umlaute **live zerstoert** (echter Datei-Schaden, doppeltes Mojibake
> `ae` → `Ã¤` → `ÃƒÂ¤`). PS 5.1 liest UTF-8 ohne `-Encoding UTF8` als
> Windows-1252 und schreibt es als Mojibake zurueck.

- **NIE** deutschen HTML-/CSS-Content ueber PowerShell `Get-Content -Raw` **ohne**
  `-Encoding UTF8` lesen+zurueckschreiben. Ebenso Bash-Heredoc/`echo`/`cat` fuer
  Umlaut-Content meiden.
- **Lesen:** `[IO.File]::ReadAllText($f,[Text.Encoding]::UTF8)`
- **Schreiben (UTF-8 ohne BOM):** `[IO.File]::WriteAllText($f,$c,(New-Object Text.UTF8Encoding($false)))`
- **Nach jedem skriptbasierten Edit an Umlaut-Content gegenpruefen** — VOR dem
  Deploy: `fuer` / `Gaeste` / `persoenlich` korrekt gerendert, kein `Ã` im File
  (`Select-String 'Ã' $f`).
- **`<meta charset="UTF-8">`** ist Pflicht im `<head>` jeder Seite.
- **Doppel-Mojibake-Reparatur** (2x rueckwaerts durch 1252 dekodieren):
  ```powershell
  1..2 | % { [IO.File]::WriteAllBytes($f,[Text.Encoding]::GetEncoding(1252).GetBytes([IO.File]::ReadAllText($f,[Text.Encoding]::UTF8))) }
  ```
- Bevorzugt: fuer Umlaut-Content das Edit/Write-Tool statt Shell-Roundtrip nutzen.

## 7. Copy-paste-Baseline (Startpunkt, kein Dogma)

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

```css
/* Fluide Basis-Typo — Max >= 2x Min fuer 200%-Zoom */
html { font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem); }

/* Inputs nie unter 16px (iOS-Zoom-Falle) */
@media (pointer: coarse) {
  input, select, textarea { font-size: 16px; }
}

/* Touch-Targets */
button, a.btn, [role="button"] { min-height: 44px; min-width: 44px; }

/* Safe-Area fuer sticky Bottom-CTA / Bottom-Nav */
.bottom-bar {
  padding-bottom: max(1rem, env(safe-area-inset-bottom));
}

/* Sichtbarer Fokus statt outline:none */
:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; }

/* Breite Bloecke scrollen in sich, nicht die Seite */
.table-wrap { overflow-x: auto; }
img, video, canvas, svg { max-width: 100%; height: auto; }
```

## 8. Quellen (autoritativ)

- Apple HIG — Touch-Targets 44pt: https://developer.apple.com/design/human-interface-guidelines/accessibility
- Material Design 3 — 48dp: https://m3.material.io/foundations/designing/structure
- WCAG 2.2 SC 2.5.8 Target Size (Minimum, AA, 24px): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- WCAG 2.2 SC 2.5.5 Target Size (Enhanced, AAA, 44px): https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html
- WCAG 2.2 SC 1.4.3 Contrast (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum
- WCAG 2.2 SC 2.4.11 Focus Appearance: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
- Steven Hoober — Thumb-Zone (Smashing Magazine): https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/
- Luke Wroblewski — Mobile First: https://www.lukew.com/resources/mobile_first.asp
- web.dev — clamp() fluide Typo: https://web.dev/articles/min-max-clamp
- web.dev — Core Web Vitals (LCP/CLS/INP): https://web.dev/articles/vitals
- web.dev — INP ersetzt FID (03/2024): https://web.dev/blog/inp-cwv-launch
- web.dev — Forms (type/inputmode/autocomplete): https://web.dev/learn/forms/attributes
- CSS-Tricks — 16px verhindert iOS-Form-Zoom: https://css-tricks.com/16px-or-larger-text-prevents-ios-form-zoom/
- MDN — viewport meta: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport
- MDN — env() safe-area-inset: https://developer.mozilla.org/en-US/docs/Web/CSS/env
- NN/g — Touch-Target-Groesse: https://www.nngroup.com/articles/touch-target-size/

## 9. Aktivierung in Projekt-CLAUDE.md

Zeilen fuer die `CLAUDE.md` eines Projekts, das Web-Surfaces baut:

```markdown
## Skill: web-mobile-design
Aktiv. Ladbare Bau-/Review-Checkliste fuer mobil-taugliche Web-Surfaces
(Landing-Pages, HTML-Cockpits, Formulare, Portale). Laden VOR dem ersten
HTML/CSS und VOR dem "fertig"-Melden. Kern: Touch-Targets 44/48, 16px-Input,
Viewport-Meta + safe-area, kein Horizontal-Scroll, clamp-Typo, Core Web
Vitals, sichtbarer Fokus, Kontrast 4.5:1. Ergaenzt frontend-design (Aesthetik)
und creative-studio (Ad-Creatives), ersetzt sie nicht.
```
