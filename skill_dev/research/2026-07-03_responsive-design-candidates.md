# Responsive/Mobile Web-Design — Kandidaten-Recherche + uebernehmbare Rezepte

Recherche 2026-07-03 (Subagent) fuer SKILL-070 (`web-mobile-design`).
Zweck: fertige Ansaetze fuer mobil-taugliches Web-Design pruefen, beste
Rezepte RAW sichern, damit SKILL-070 damit erweitert werden kann.
**KEIN bestehender Skill wurde ueberschrieben.** Dies ist nur Quellmaterial.

Quellen sind Techniken/Formeln aus Public Docs (Every Layout Free-Tier,
Utopia.fyi Blog, Open Props Docs, Vercel Web Interface Guidelines,
Anthropic frontend-design). GitHub raw war netz-geblockt; Techniken sind
Standard-CSS und unten selbst ausformuliert.

---

## Empfehlung in einem Satz

**SKILL-070 behalten und erweitern** (nicht ersetzen). Kein fertiger Skill
deckt Layout-Rezepte (Stapeln / fluide Typo mit hohen Mobile-Minima /
zentrierte CTAs) konkret ab — genau die Luecke, die Jakobs Symptome
verursacht. Die besten uebernehmbaren Bausteine sind **Methodiken**
(Every-Layout-Primitives + Utopia-clamp-Formel + auto-fit-Grid), nicht ein
Konkurrenz-Skill.

---

## Rezept 1 — Auto-Stack-Grid (gegen "Spalten nebeneinander statt gestapelt")

Standard-CSS, kein Media-Query noetig. Spalten stapeln automatisch, sobald
kein `minmax`-Minimum mehr nebeneinander passt:

```css
.grid {
  display: grid;
  gap: 16px;
  /* min() verhindert Overflow, wenn Container < 280px (kleine Phones) */
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
}
```

- `auto-fit` + `minmax(280px, 1fr)` = bei < ~580px automatisch 1 Spalte.
- `min(100%, 280px)` statt nur `280px` = kein horizontaler Overflow auf
  360-px-Screens.
- Ersetzt fragile `@media (min-width: 760px){ grid-template-columns: 1fr 1fr }`
  Muster (fixe Breakpoints, die auf grossen Phones/kleinen Tablets kippen).

## Rezept 2 — Switcher (Every Layout, Free-Tier) — 2 Spalten -> gestapelt ohne Media-Query

Fuer genau-2-Spalten-Faelle (z.B. Preis-Karten), container-basiert:

```css
.switcher {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  --threshold: 30rem; /* ab hier stapeln */
}
.switcher > * {
  flex-grow: 1;
  flex-basis: calc((var(--threshold) - 100%) * 999);
}
```

Mechanik: Container breiter als `--threshold` -> `flex-basis` negativ ->
ignoriert -> nebeneinander. Schmaler -> grosse positive Zahl -> jedes Kind
100% -> gestapelt. Quantum-Switch, kein Zwischenzustand.
Quelle: https://every-layout.dev/layouts/switcher/

## Rezept 3 — Fluide Typo mit HOHEN Mobile-Minima (gegen "Text/Headlines zu klein")

Utopia-Formel (Pedro-Rodriguez), erzeugt clamp() ohne Media-Query:

```
Slope        = (MaxSize - MinSize) / (MaxVw - MinVw)   [Vw in rem, /100]
yIntersection= (-1 * MinVw) * Slope + MinSize
font-size    = clamp(MinSize, yIntersection + Slope*100vw, MaxSize)
```

Konkrete, mobil-sichere Werte (Min @ 320px, Max @ 1440px):

```css
:root {
  /* Body: NIE unter 1rem/16px auf Mobile (iOS-Zoom + Lesbarkeit) */
  --step-0:  clamp(1rem,    0.93rem + 0.36vw, 1.25rem);  /* 16 -> 20px */
  --step-1:  clamp(1.2rem,  1.09rem + 0.54vw, 1.56rem);
  --step-2:  clamp(1.44rem, 1.27rem + 0.84vw, 1.95rem);
  --step-3:  clamp(1.73rem, 1.47rem + 1.29vw, 2.44rem);  /* H2 */
  --step-4:  clamp(2.07rem, 1.69rem + 1.91vw, 3.05rem);  /* H1: min 33px */
}
h1 { font-size: var(--step-4); }
h2 { font-size: var(--step-3); }
p, li, .cell { font-size: var(--step-0); }
```

Kernregel gegen Jakobs Symptom: **Mobile-Minimum hochsetzen** — H1 >= ~2rem
(32px), H2 >= ~1.6rem, Body >= 1rem (16px). Kleintext wie `.cell{font-size:.94rem}`
(=15px) oder `.head{font-size:.8rem}` (=13px) sind der direkte Grund fuer
"zu klein" — durch `--step-0` bzw. ein eigenes `--step--1: clamp(0.9rem, ..., 1rem)`
ersetzen, nie unter 0.875rem fuer Fliesstext.
Quelle: https://utopia.fyi/blog/clamp/ , Rechner: https://utopia.fyi/clamp/calculator/

## Rezept 4 — Voll-breite, zentrierte CTAs auf Mobile (gegen "Buttons nicht zentriert / zu klein")

```css
.btn {
  min-height: 48px;          /* Touch-Target (Material 48dp) */
  padding: 14px 24px;
  font-size: 1.0625rem;      /* 17px, nie unter 16 */
  border-radius: var(--brand-radius, 12px);
  display: inline-flex; align-items: center; justify-content: center;
  text-align: center;
}
/* Auf Phones: voll-breit + zentriert im Fluss */
@media (max-width: 560px) {
  .btn { display: flex; width: 100%; box-sizing: border-box; }
}
/* CTA-Wrapper zentriert den Button-Block selbst */
.cta { display: flex; flex-direction: column; align-items: center; gap: 12px; }
```

- `justify-content:center` im Button = Label mittig (haeufig vergessen ->
  linksbuendiger Text).
- `.cta{align-items:center}` = der Button-Block ist zentriert, auch wenn er
  nicht voll-breit ist.
- Sticky-Variante fuer Daumen-Zone: `position:sticky; bottom:0;
  padding-bottom:max(1rem, env(safe-area-inset-bottom))`.

## Rezept 5 — Center-Primitive (Every Layout) fuer zentrierten Content-Flow

```css
.center {
  box-sizing: content-box;
  margin-inline: auto;
  max-width: 60ch;          /* Lesezeilenlaenge */
  padding-inline: 20px;     /* Gutter, damit Text nie am Rand klebt */
}
.center--intrinsic { display: flex; flex-direction: column; align-items: center; }
```

---

## Kandidaten-Bewertung (fertige Skills/Systeme)

| Kandidat | Deckt Mobile-LAYOUT konkret ab? | Lizenz | Gewicht | Passt zu Token-LPs (ADR-010)? |
|---|---|---|---|---|
| **Anthropic `frontend-design`** (anthropics/skills) | Nein — Aesthetik/Persoenlichkeit; "responsive down to mobile" nur als Qualitaets-Floor, keine Zahlen/Stapel-Rezepte | MIT | mittel (Tailwind-lastig) | teils (CSS-Vars-Theming), aber Tailwind-Bias |
| **Vercel Web Interface Guidelines / web-design-guidelines** (vercel-labs) | Teilweise — starke CHECKLISTE (44px, 16px-Input, safe-area, touch-action, tap-highlight); KEINE Layout-Rezepte (Stapeln/fluid type) | MIT | mittel (100+ Regeln) | ja (framework-agnostisch), aber ueberlappt ~90% mit SKILL-070 |
| **lotfb86/web-design-skills** (7-Skill-Paket, inkl. responsive) | Ja fuer Breakpoints/fluid/container-queries; aber schwergewichtig (7 vernetzte Skills, Rebuild-Pipeline) | siehe Repo | schwer | teilweise; widerspricht "schlanker als was er ersetzt" |
| **Every Layout** (Stack/Center/Cluster/Switcher) | Ja — beste Layout-PRIMITIVES (auto-stack ohne Media-Query) | Buch/paid (Grid hinter Paywall; Switcher/Stack/Center/Sidebar frei einsehbar) | ultraleicht (reines CSS) | ja — pures CSS auf `--brand-*`-Tokens |
| **Utopia.fyi** (fluid type/space) | Ja — beste FLUID-TYPO-Methodik (clamp-Formel, Rechner) | Rechner frei, Formel offen | ultraleicht | ja — erzeugt Tokens, passt in tokens.css |
| **Open Props** | Teilweise — fertige fluid-`clamp`-Tokens (`--font-size-fluid-*`, `--size-fluid-*`) | MIT | 4 kB, incrementally adoptable | ja — CSS-Vars, neben tokens.css nutzbar |
| **Pico.css** | Ja (auto-skaliert Font/Spacing responsive, classless) | MIT (Docs CC BY-SA) | leicht, 130+ Vars | maessig — will HTML-Elemente selbst stylen; Kollision mit handgeschriebenen LPs |

---

## Root-Cause in unseren LPs (bestaetigt am Code)

- **Gemischte Muster:** `landing/vision/index.html` nutzt bereits das robuste
  `repeat(auto-fit, minmax(280px,1fr))` (stapelt automatisch) — GUT. Aber
  `landing/verkauf-immo/index.html:114` nutzt fixes
  `@media(min-width:760px){.price-grid{1fr 1fr}}` und `vision .dim:44` ein
  fixes `grid-template-columns:200px 1fr 1fr`. Fixe Breakpoints/Spalten sind
  fragil auf grossen Phones/kleinen Tablets.
- **Zu-klein-Text:** Standalone-LPs (vision, verkauf-immo) rollen FIXE
  rem-Groessen (`.cell{font-size:.94rem}`=15px, `.head{.8rem}`=13px, kein
  clamp). Das Funnel-Template (`_templates/funnel-page.template.html`) nutzt
  zwar clamp fuer H1/H2, aber die Sonder-LPs nicht. -> fluide Typo-Skala
  (Rezept 3) fehlt genau dort.
- **CTA:** Funnel-Template hat `.btn-block{width:100%;text-align:center}` +
  `@media(max-width:560px){.btn{display:block;width:100%}}` — gut. Sonder-LPs
  ohne dieses Muster brauchen Rezept 4.

## Quellen

- Anthropic frontend-design: https://github.com/anthropics/skills (skills/frontend-design)
- Vercel Web Interface Guidelines: https://github.com/vercel-labs/web-interface-guidelines , https://vercel.com/design/guidelines
- lotfb86 web-design-skills: https://github.com/lotfb86/web-design-skills
- Every Layout (Switcher/Stack/Center): https://every-layout.dev/layouts/
- Utopia clamp-Formel: https://utopia.fyi/blog/clamp/
- Open Props: https://open-props.style/
- Pico.css: https://picocss.com/
