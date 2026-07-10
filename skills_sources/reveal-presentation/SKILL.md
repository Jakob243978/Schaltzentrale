---
name: reveal-presentation
description: Build a single-file reveal.js presentation from research content. Use whenever the user asks to create a "Präsi", slide deck, presentation, or convert existing material into slides. Stores detailed researched content in `speakernotes.md` and breaks it into bite-sized notes embedded directly in `aside class="notes"` blocks on each slide. Two style modes — Default (clean white, business-tauglich, für Stakeholder-Decks) and Editorial (warm/redaktionell, Jakob Sebovs Personal Brand — Beige/Navy/Coral, Fraunces+Inter). Always include white space (margin 0.10), Headline-First with Fragment-Reveal pattern, and Eine-Message-pro-Slide. Defaults until user-specific CI for Jakob Sebov is supplied.
---

# Reveal.js Presentation Builder

Build clean, professional slide decks with reveal.js. The artefact is one HTML file plus one Markdown file:

- `<topic>_presi.html` — the actual slide deck, single-file, runs in any browser, uses reveal.js via CDN
- `<topic>_speakernotes.md` — the full researched content per slide, longform; the slide's `aside class="notes"` shows only a condensed bite-sized version that fits the speaker's mental loop

## When to use this skill

Triggered by user intents like:
- "mach mir eine Präsi aus …"
- "erstelle eine Präsentation zu …"
- "wir brauchen Folien für …"
- "bau X als reveal.js auf"
- "verproben wir das direkt mit Y" (in context of building slides)

Skip if the user only wants a static HTML document (not slide-based) or a Markdown deck without browser-rendering.

## Workflow

Build the deck in three phases — don't shortcut.

### Phase 1 — Slide-Inventur aus Quellmaterial
Read the source material (HTML doc, MD file, notes). Identify slide boundaries:
- One slide per atomic idea
- Section breaks become section-title slides (with `data-state="section-title"` or a clear visual marker)
- Long tables/code blocks get their own slide
- Comparisons → side-by-side slide
- Question lists → one slide per question or one summary slide

Produce a short outline (slide number → title → 1-sentence content) before writing anything else. Confirm with the user if there are > 15 slides — long decks need user input on cut/keep.

### Phase 2 — speakernotes.md schreiben (detailliert, vollständig)
For each slide a Markdown section like:

```markdown
## Slide N — <Title>

**Was im Bild zu sehen ist:**
…

**Vollständiger Speaker-Text (was ich sage):**
…

**Anekdoten / Beispiele / Daten:**
- …

**Mögliche Rückfragen + Antworten:**
- Q: …
  A: …

**Übergangs-Satz zur nächsten Folie:**
…
```

This is the *full* content — what the speaker prepares with, what backs up the slide if someone reads the file standalone. Detailed, complete, fact-checked.

### Phase 3 — reveal.js HTML mit Häppchen-Notes bauen
For each slide:
- Visible content: condensed, scannable, max ~6 bullets / ~50 words
- `<aside class="notes">` block: the **bite-sized version** of the Phase-2 speaker text — 2–4 short sentences, key numbers/quotes, transition. *Not* the full speakernotes.md content. The speaker has the MD file open on a second screen for the deep version; the inline notes are the speaker's memory anchor.

Use `S` to open the speaker view (notes + next-slide preview).

### Phase 4 — Visual-Review-Pass (Chromium-Screenshots) — PFLICHT

> [!danger] Niemals "fertig" melden ohne Visual-Review-Pass durchgelaufen
> HTML-Code-Read reicht nicht. Layout-Bugs (CSS-Grid-Auto-Flow, Flex-Overflow, Wort-pro-Zeile-Wraps) sind im Quellcode **nicht** sichtbar — nur im gerenderten Screenshot. Wenn der Screenshot ein Problem zeigt → erst fixen, dann erneut screenshotten. Erst dann an User übergeben.

**Reihenfolge ist fix: Phase 1 → 2 → 3 → 4 → (Loop falls nötig).** Phase 4 ist nicht optional.

**Verfahren:**

1. **Wrapper-Script aufrufen** (legt Temp-HTML mit Fragments-sichtbar-Override an, macht Screenshots pro Slide):
   ```bash
   # Git-Bash / Linux / macOS
   tools/screenshot_slides.sh <presi.html> <n_slides> <output_dir>

   # Windows PowerShell
   .\tools\screenshot_slides.ps1 -Presi <presi.html> -NSlides <n> -OutputDir <dir>
   ```
   Output: `slide_00.png` bis `slide_NN.png`.

2. **Pro Slide mit Read-Tool inspizieren** — Claude kann PNGs lesen. Check-Liste durchgehen (siehe `patterns/visual-review.md`):
   1. Headline vollständig sichtbar (nicht abgeschnitten)?
   2. Items/Bullets brechen sinnvoll (kein Wort-pro-Zeile)?
   3. Slide-Höhe-Overflow (letzte Bullet noch da)?
   4. Umlaute korrekt gerendert?
   5. Fragment-Override greift (alle Inhalte sichtbar)?
   6. Farben/Akzente erkennbar (kein weiß-auf-weiß)?

3. **Auto-Iterations-Loop:**
   - Bei sichtbarem Problem → CSS/HTML-Fix → einzelne Slide neu screenshotten → erneut lesen
   - Max **3 Auto-Iterationen pro Slide**
   - Wenn nach 3 Iterationen noch nicht clean → an User übergeben mit Hypothese (z.B. "Slide hat zuviel Inhalt für 1080p — Aufteilung nötig?")

4. **Wenn alle Slides clean:** kurze Sammel-Bestätigung an User mit Output-Pfad (z.B. "16/16 Slides visuell ok — Screenshots in `/tmp/shots/`. Bereit für inhaltlichen Review?").

**Detail-Doku + Live-Beispiele (BeyerImmo 2026-05-27):** `patterns/visual-review.md`. Drei prototypische Failure-Modes mit Screenshot-Symptom + Recovery dokumentiert.

**Token-Trade-Off:** ~1.5k Tokens pro Screenshot-Read × 16 Slides = ~24k extra pro Build. Spart aber die User-Feedback-Schleifen + Re-Reads (50-100k pro Iteration).

## Slide-Choreografie: Eine Message pro Slide + Fragment-Reveal

**Leitprinzip:** *Headline-First, Evidence Follows.* Jede Slide trägt **eine prägnante Kernaussage** (Headline / Assertion). Belege, Beispiele und Details folgen visuell darunter — und werden bevorzugt **als Fragments per Klick eingeblendet**, nicht alle auf einmal gezeigt.

### Warum
- Publikum konzentriert sich auf den einen Punkt, statt 8 Bullets parallel zu scannen
- Sprecher führt durch die Geschichte (Klick = nächster Beleg), statt eine Liste vorzulesen
- Folie funktioniert auch standalone (Headline = Take-away, lesbar in 3 Sekunden)
- Anschluss an Assertion-Evidence-Pattern (Michael Alley, NASA/SPS), das in technischen Präsentationen messbar besser als Bullet-Listen funktioniert

### Drei typische Slide-Layouts

**1. Statement + Fragment-Belege** (Standard für Argument-Slides)
```html
<section>
  <h2>Kernaussage in einem ganzen Satz.</h2>
  <p class="fragment fade-in">Erster Beleg / Beispiel / Datenpunkt.</p>
  <p class="fragment fade-in">Zweiter Beleg.</p>
  <p class="fragment fade-in">Dritter Beleg.</p>
  <aside class="notes">Sprich die Kernaussage. Dann klicke und kommentiere jeden Beleg einzeln.</aside>
</section>
```

**2. Statement + Fragment-Vergleich** (für Vorher/Nachher, Optionen-Diskussion)
```html
<section>
  <h2>Wir wollen X — die zwei Wege haben Konsequenzen.</h2>
  <div class="twocol">
    <div class="col fragment fade-in"><h3>Weg A</h3>…</div>
    <div class="col fragment fade-in"><h3>Weg B</h3>…</div>
  </div>
</section>
```

**3. Statement + Visualisierung** (Diagramm/Bild ist der Hauptinhalt)
```html
<section>
  <h2>Die Datenpipeline hat zwei Stufen.</h2>
  <div class="mermaid fragment fade-in">flowchart LR; A --> B --> C</div>
  <p class="fragment fade-in footnote">Stufe 1 erkennt Änderungen, Stufe 2 prüft sie.</p>
</section>
```

### Fragment-Stile (was nehmen)
- `class="fragment"` — Default: erscheint bei Klick (fade-in semi-transparent → opaque)
- `class="fragment fade-in"` — sauberes Einblenden, **Standard für die meisten Fälle**
- `class="fragment highlight-current-blue"` — wird beim Erreichen blau, danach normal (gut für Wort-für-Wort-Lesen)
- `class="fragment grow"` — wird beim Erreichen größer (für *einen* Punkt zur Betonung)
- `data-fragment-index="N"` — explizite Reihenfolge, falls anders als Code-Order gewünscht

### Wann Fragments NICHT nutzen
- Titel-Slide (alles auf einmal sichtbar, das ist der Anker)
- Tabelle mit < 5 Zeilen (würde nervös wirken)
- Q&A-Slide
- Closing-Slide
- Bei Print/PDF-Export müssen alle Fragments sichtbar werden — reveal.js macht das automatisch bei `?print-pdf`, kein extra Aufwand

### Headline-Disziplin
- **Vollständige Aussage**, kein Stichwort: ❌ „Die Vorteile" → ✅ „Die Erweiterung spart pro Story 5 Minuten Refinement-Zeit."
- **Konkret + überprüfbar**: Zahlen, Namen, Zeit nennen wenn möglich
- **Max 80 Zeichen** — passt in zwei Zeilen bei der definierten Schriftgröße
- Wenn die Aussage länger wird → die Aussage ist nicht klar genug; nochmal schärfen

### Spaltenbreite zuerst prüfen (vor Text-Splitting)

Wenn ein Bullet/Statement unschön bricht: **erst max-width der Liste prüfen**, dann erst den Text splitten. Häufiger Fehler: Inline `style="max-width: 28em"` ist zu eng für den Inhalt — der Text wird gesplittet obwohl er bei 40em-50em problemlos in eine Zeile passt.

**Faustregel:** Wenn ein 80-Zeichen-Bullet unschön bricht und auf der Slide noch Platz wäre, erst `max-width` auf 40-50em hoch. Erst wenn das nicht reicht (oder die Slide visuell unausgeglichen wird), den Text aufsplitten (siehe nächste Sektion).

**Slide-Höhe respektieren:** Reveal-Default 1920×1080 oder 1280×720. Bei vielen Bullets + Steve-Card + Statement zählen — passt das alles ins Viewport, oder wird die letzte Zeile abgeschnitten? Im Zweifel: Statement weglassen oder als zusätzliches Item integrieren.

### Satz-an-Sinneinheit-umbrechen (gegen unschöne Auto-Wraps)

Lange Bullet-Texte / Aussagen bei breiten Spalten brechen sonst mitten im Satz oder zwischen sinngemäß zusammengehörenden Worten — wirkt schlampig. Disziplin:

- **Bullet-Items mit längerer Erklärung:** Hauptbegriff fett + `<br>` + Erklärung als gedämpfter Sub-Text in eigenem `<span>`:
  ```html
  <li data-num="1">
    <strong>Rechnungen zu prüfen</strong><br>
    <span style="font-size: 0.9em; color: var(--ink-soft);">Paulinas Bereich — Steve hat hier nicht durchgewunken.</span>
  </li>
  ```
- **Lange Statement-Sätze:** an natürlicher Satz-/Gedanken-Grenze brechen — nach Doppelpunkt, vor Konjunktion, nach Hauptaussage. Mit `<br>` + Sub-Text-Klasse:
  ```html
  <p><strong>Parallel im Hintergrund:</strong> Jede PDF landet zusätzlich im Lake.<br>
  <span style="color: var(--ink-soft);">Compliance-Backup — unabhängig vom DATEV-Pfad.</span></p>
  ```
- **Compare-Tabellen-Items mit Erklärung:** Aktion oben, Begründung im Sub-Text — nie ein langer Satz in einer Zelle, sondern Action + Why getrennt:
  ```html
  <li data-num="1">Original in „Verarbeitet" suchen.<br>
    <span style="color: var(--ink-muted);">Irene informieren falls schon bezahlt.</span></li>
  ```
- **Faustregel:** wenn ein Bullet/Statement länger als ~80-100 Zeichen wird **und** in einer schmalen Spalte sitzt → splitten in Haupt-Aussage + Sub-Text.
- **NICHT:** ein einzelner langer `<p>` mit mehreren Sätzen — das bricht garantiert unschön. Lieber zwei Absätze oder einer mit `<br>`.

### Umlaute richtig schreiben (deutsche Stakeholder-Texte)

Für **stakeholder-sichtbare Texte** (Slides, Visible-HTML, Speaker-Notes wenn gezeigt) **echte deutsche Umlaute** verwenden — nicht `oe/ae/ue/ss` als ASCII-Notlösung:

| ❌ ASCII-Notation | ✅ Umlaut |
|---|---|
| `ueber`, `Ueber` | `über`, `Über` |
| `pruefen`, `Pruefung` | `prüfen`, `Prüfung` |
| `moegli`, `Moegli` | `mögli`, `Mögli` |
| `aend`, `Aend` | `änd`, `Änd` |
| `Schluess`, `schluess` | `Schlüss`, `schlüss` |
| `loes`, `Loes` | `lös`, `Lös` |
| `koen`, `Koen` | `kön`, `Kön` |
| `muess`, `Muess` | `müss`, `Müss` |
| `fuer`, `Fuer` | `für`, `Für` |
| `naech`, `Naech` | `näch`, `Näch` |
| `spaeter`, `Spaeter` | `später`, `Später` |
| `Geschaefts` | `Geschäfts` |
| `woechentlich` | `wöchentlich` |
| `Saetze` | `Sätze` |
| `Faelle` | `Fälle` |
| `zurueck` | `zurück` |

**Wo erlaubt bleibt:**
- **Quellcode** (Variablennamen, Slugs, Vision-Principle-IDs wie `eingangskanaele-zentralisieren`) — ASCII-only ist Konvention
- **Frontmatter-Slugs** in Tickets/ADRs (`vision_principle: bus-faktor-zaehlt`)
- **CSS-/HTML-Attributnamen, Klassen, IDs**
- **Speakernotes-MD-Datei** wenn Standalone — pragmatisch, kein Stakeholder schaut da rein

**Charset-Sanity:** HTML braucht `<meta charset="UTF-8">` im `<head>`. Beim Schreiben in PowerShell/Python: `Set-Content -Encoding utf8` bzw. `open(..., encoding='utf-8')`. Bei Editor-Diffs prüfen ob nicht durch Encoding-Drift Umlaute verloren gehen (z.B. Windows-1252-Saves).

### Sicherheits-Check vor PDF-Export/Print

- `?print-pdf` öffnen + scrollen: bricht ein Bullet unschön? Splitten.
- Über `&` in HTML-Attributen kein Problem (Browser rendert HTML-Entities), aber im sichtbaren Text mit `&amp;` schreiben falls direkt im HTML steht.

## Optional: Editorial-Mode — Jakob Sebov Personal Brand

> **Wann?** Für Jakobs eigene Personal-Brand-Decks: Vorträge, Workshop-Präsis, Tutorial-Slides, alles unter `jakse-automations.com`. Der Stil ist warm, redaktionell, mit klarer Hierarchie (großer Number-Marker links, Sublabel-Tag, Trennstrich, dann Headline mit Italic-Akzenten).
> **Quelle / Single Source of Truth:** `assets/editorial.css` (mitgeliefert im Skill) — identisch mit `personal_branding/deploy/shared/editorial.css`.
> **Wechselbar:** Phase 1 (Slide-Inventur) explizit entscheiden — Editorial bei Personal-Brand-Inhalten, Default für Stakeholder/Status.

### Charakter-Merkmale auf einen Blick
- **Cremig-warmes Beige** als Hintergrund (`#faf7f2`), tiefes Navy (`#0a0e27`) als Text, **Coral** (`#f25d3e`) als einziger Akzent
- **Inter** (sans-serif) für Body, **Fraunces** (Italic-Serif, variable Font) für Akzente in Headlines (`<span class="serif">…</span>`)
- **Number-Marker** links oben (groß, Fraunces, Coral) — strukturiert das Deck wie ein Magazin-Artikel
- **Sublabel "Tag"** unter dem Number-Marker — kleines, uppercase, Coral-farbenes Label, das die Slide-Funktion bezeichnet
- **Editorial Rule** (3em breiter Coral-Strich) zwischen Tag und Headline
- **Headline mit Italic-Serif-Akzent** für *ein* Schlüsselwort: „Smoobu kriegt einen *Webhook*."
- **Großzügiges Whitespace links** (padding-left: 5em für num-Marker)
- **Slide-Ratio: 1920×1080**, margin 0.05 (anders als Default 1280×720)
- **Drei Section-Modes:** Standard (Beige), `.dark` (Navy voll-flächig, weiße Schrift), `.accent` (Coral voll-flächig, Navy-Schrift) — für Title-, Section-Divider-, Statement-Slides

### Farbpalette Editorial (CSS-Variablen aus `editorial.css`)

```css
:root {
  --bg: #faf7f2;          /* cremiges Beige — Standard-Hintergrund */
  --ink: #0a0e27;         /* tiefes Navy — Standard-Text */
  --ink-soft: #3a3f5c;    /* abgeschwächtes Navy — Lead/Subtext */
  --ink-muted: #6b6f87;   /* grauer Ink — sehr leise Texte */
  --accent: #f25d3e;      /* Coral — der einzige Farb-Akzent */
  --accent-deep: #d4422a; /* dunkleres Coral — für strong/em */
  --accent-soft: #fde6df; /* fast-weiß Coral — Hintergründe */
  --rule: #e8e2d8;        /* sehr helles Beige — Trennlinien */
  --warm-white: #ffffff;  /* reines Weiß — Karten-Hintergründe */
}
```

### Setup im HTML-File

```html
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..900,0..100;1,9..144,300..900,0..100&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/reveal.min.css">
  <link rel="stylesheet" href="PFAD/zu/editorial.css">  <!-- Kopie aus skill-assets oder Shared-CSS-Pfad -->
</head>
```

Reveal-Initialisierung:
```js
Reveal.initialize({
  hash: true,
  transition: 'fade',
  backgroundTransition: 'fade',
  width: 1920,
  height: 1080,
  margin: 0.05,         // Personal-Brand-Default (nicht 0.10)
  minScale: 0.2,
  maxScale: 2.0,
  center: false,
  controls: true,
  progress: true,
  plugins: [ RevealNotes ],
});
```

### CSS-Klassen-Bibliothek (was wann verwenden)

| Klasse | Zweck | Beispiel |
|---|---|---|
| `<span class="num">` | Slide-Nummer links oben (Fraunces, Coral, groß) | `<span class="num">07</span>` |
| `<p class="tag">` | Sublabel unter num (uppercase, Coral, klein) | `<p class="tag">Block 1 · Gästekommunikation</p>` |
| `<hr class="rule">` | 3em Coral-Trennstrich zwischen Tag und Headline | direkt nach dem Tag |
| `<span class="serif">` | Italic-Serif-Akzent in Headline (Fraunces) | `<h2>Smoobu kriegt einen <span class="serif">Webhook</span>.</h2>` |
| `<p class="lead">` | Untertitel unter h2 (1.2em, ink-soft) | `<p class="lead">Hier kommt die Erklärung.</p>` |
| `<p class="lead large">` | Größerer Lead (1.4em) | für Statements unter Titel |
| `<ul class="items">` mit `<li data-num="A">` | Liste mit Fraunces-Markern (A, B, 1, ·) | `<li data-num="1"><strong>Name</strong> — Beschreibung</li>` |
| `<p class="statement">` | Pull-Quote (Fraunces italic, Coral-Border links) | für Kernsätze, Mantras |
| `<div class="compare">` mit `<div class="col">` / `<div class="col alt">` | Zwei-Spalter-Vergleich | API ↔ Webhook, Vorher ↔ Nachher |
| `<div class="chain">` mit `<div class="step">` / `<span class="arrow">` | Verkettete Prozess-Schritte mit Pfeilen | Event → Daten → Entscheidung → Aktion |
| `<div class="stat-block">` mit `<div class="stat-num">` + `<p class="stat-label">` | Große Statistik (Fraunces, 5em) | "< 1 %" mit Erklärung darunter |
| `<div class="formula">` mit `<span class="op">` | Formel-Layout (Fraunces, zentriert) | „**Wenn** X passiert, **und** Y gilt, **dann** Z" |
| `<p class="mindset-line">` | Großes Editorial-Quote-Statement | für emotionale Closing-Sätze |
| `<span class="mindset">` | Kleines Inline-Label (Inter Bold, dunkler Background) | inline-Tags wie Buttons |

### Section-Modes

| Section-Class | Wann | Visual |
|---|---|---|
| `<section>` (kein class) | Standard Content-Slide | Cremiger Hintergrund, Navy-Schrift |
| `<section class="dark">` | Title-Slide, Section-Divider, Mindset-Closing | Navy voll-flächig, weiße Schrift, Coral-Akzente |
| `<section class="accent">` | Coral-Statement-Slide, dramatische Pointe | Coral voll-flächig, Navy-Schrift |
| `<section class="center">` | text-align: center + vertikal zentriert | Mit `.dark` oder `.accent` für Title-Slides |

### Editorial-Pattern-Templates (5 Layouts decken ~95 % ab)

**1. Title-Slide (Dark + Center)**
```html
<section class="dark center" data-background-color="#0a0e27">
  <p class="tag" style="font-size: 0.5em; opacity: 0.7;">EVENT-KONTEXT · DATUM</p>
  <h1 style="font-size: 3.4em; line-height: 1.05; max-width: 18em; margin-top: 1em;">
    Hauptaussage mit <span class="serif" style="color: var(--accent);">Italic-Akzent.</span>
  </h1>
  <p class="lead" style="margin-top: 1em; max-width: 32em; opacity: 0.85;">Untertitel-Satz, der die Hauptaussage erweitert.</p>
  <p style="margin-top: 2.5em; font-size: 0.55em; letter-spacing: 0.15em; text-transform: uppercase; opacity: 0.6;">Sprecher · Datum · Ort</p>
</section>
```

**2. Standard Content-Slide (mit num + tag + rule + items)**
```html
<section>
  <span class="num">07</span>
  <p class="tag">Block-Kontext · Slot-Beschreibung</p>
  <hr class="rule">
  <h2>Vollständige Headline mit <span class="serif">Akzent</span>.</h2>
  <p class="lead" style="margin-top: 0.6em;">Optionaler Untertitel-Satz für Kontext.</p>
  <ul class="items" style="margin-top: 0.8em;">
    <li class="fragment fade-in" data-num="1"><strong>Punkt 1</strong> — Erklärung dazu</li>
    <li class="fragment fade-in" data-num="2"><strong>Punkt 2</strong> — Erklärung dazu</li>
    <li class="fragment fade-in" data-num="3"><strong>Punkt 3</strong> — Erklärung dazu</li>
  </ul>
  <p class="fragment fade-in statement" style="margin-top: 0.8em;">Kernsatz als Pull-Quote — Klammer für die Punkte oben.</p>
  <aside class="notes">Speaker-Häppchen.</aside>
</section>
```

**3. Section-Divider / Statement-Slide (Coral voll-flächig)**
```html
<section class="accent" data-background-color="#f25d3e">
  <span class="num" style="color: rgba(10,14,39,0.35);">04</span>
  <p class="tag" style="color: var(--ink);">SLOT-LABEL</p>
  <hr class="rule" style="background: var(--ink);">
  <h1 style="font-size: 3.6em; max-width: 18em; line-height: 1.05;">
    Dramatischer Statement-Satz mit <span class="serif">Italic-Akzent.</span>
  </h1>
  <p class="lead" style="color: var(--ink); margin-top: 0.8em;">Optionale Erklärung.</p>
</section>
```

**4. Stat-Heavy-Slide (Big Number)**
```html
<section class="accent center" data-background-color="#f25d3e">
  <p class="tag" style="color: var(--ink);">SLOT-LABEL</p>
  <h1 style="font-size: 3.6em; max-width: 18em; line-height: 1.05; color: var(--ink);">Setup für die Zahl.</h1>
  <div class="stat-block fragment fade-in" style="margin-top: 1em;">
    <div class="stat-num" style="color: var(--ink);">800</div>
    <p class="stat-label" style="color: var(--ink);">Bewerbungen pro Saison.</p>
  </div>
  <p class="fragment fade-in statement" style="margin-top: 1em; color: var(--ink); border-left-color: var(--ink);">Pointe nach der Zahl.</p>
</section>
```

**5. Two-Column Compare-Slide (API ↔ Webhook, Vorher ↔ Nachher)**
```html
<section>
  <span class="num">05</span>
  <p class="tag">Vergleichs-Kontext</p>
  <hr class="rule">
  <h2>Headline, die den Vergleich rahmt.</h2>
  <div class="compare" style="margin-top: 0.8em;">
    <div class="col">
      <p class="headline" style="font-size: 1.3em;">Spalte A</p>
      <p class="lead">Beschreibung A — was hier passiert.</p>
    </div>
    <div class="col alt">
      <p class="headline" style="font-size: 1.3em;">Spalte B</p>
      <p class="lead">Beschreibung B — was hier passiert.</p>
    </div>
  </div>
  <p class="fragment fade-in statement" style="margin-top: 1em;">Kernsatz, der den Vergleich auflöst.</p>
</section>
```

### Workflow-Erweiterung: Editorial-Decision in Phase 1

Bei Phase 1 (Slide-Inventur) zusätzlich entscheiden:
- Ist das ein **Vortrag / Workshop / Tutorial für Jakobs Personal Brand**? → Editorial-Mode
- Liegen URLs unter `jakse-automations.com` oder Sub-Pfaden davon? → Editorial-Mode
- **Mixed:** Editorial-Mode für die Inhalts-Slides + Default-Slides für faktendichte Daten/Tabellen, wenn beide Modes benötigt werden

### Disziplin-Hinweise für Editorial-Mode
- **Eine Italic-Serif-Hervorhebung pro Headline** — `<span class="serif">…</span>` für *ein* Schlüsselwort, nicht für drei
- **Statement-Klasse sparsam** — wenn jede Slide einen Statement hat, verliert er Wirkung. 1 pro 3–4 Slides ist der Default
- **Coral als einziger Akzent** — keine anderen Akzentfarben dazu mischen
- **Num-Marker konsekutiv durch das Deck** — bei Sub-Slides Pattern `14·1`, `14·2` oder Symbole wie `↻` für Reflexions-Slides
- **Tag pro Slide** — auch wenn nur Slot-Label oder Zeit-Info. Macht die Navigation klar
- **Speakernotes immer** — auch wenn nur ein Satz. Erzwingt didaktische Disziplin



### Setup — Single-file HTML, CDN, reveal.js v4
- Use `reveal.js 4.6.1` (LTS, stable) from cdnjs
- Theme: **white** (clean, business-tauglich, gut druckbar). Alternatives if user requests: `simple`, `serif`, `solarized`
- Highlight.js for code: `highlight.js 11.x` with `monokai-sublime.min.css` (or `github` for light theme)
- Markdown plugin: not needed by default — write HTML slides directly; cleaner control
- Notes plugin: enabled
- Slide ratio: 16:9 (`width: 1280, height: 720`), **Margin 0.10** (großzügiger Whitespace zum Rand — siehe „Whitespace-Standards" unten)

### Slide-Struktur
- Each slide is a `<section>`
- Vertical slides (nested `<section>`) only for sub-topics of the same idea — avoid by default, they get lost in linear print/PDF
- Title slide first with project context (title, subtitle, author, date)
- Agenda-Slide at position 2 if deck > 6 slides
- Section-divider slides between major chapters: full-bleed colored background with section title centered

### Whitespace-Standards

Folien sollen **Atemraum** haben — nicht randvoll bis zum Bildschirmrand. Defaults:

- **Reveal-Margin: 0.10** (= 10 % der Höhe oben + unten, 10 % der Breite links + rechts als „Sicherheits-Rand"). Bewirkt: Inhalt nie an Beamer-Rand verschnitten, immer komfortabel lesbar.
- **Section-Padding zusätzlich: 1.5em** innerhalb der Slide (Container-Padding über CSS-Block setzen)
- **Vertikales Zentrieren:** Slides mit wenig Inhalt mittig im Viewport, nicht oben-links-klebend (CSS: `display: flex; flex-direction: column; justify-content: center`)
- **Headline-Höhe begrenzen:** maximal 2 Zeilen, dann darunter eine Atempause (margin-bottom: 1em zur ersten Evidence)
- **Zwischen Fragment-Items: 0.6em** vertikaler Abstand (statt 0.25em wie bei dichten Listen) — damit jedes Häppchen visuell „landet"

### Content-Disziplin
- **Eine Idee pro Slide** — formuliert als vollständige Headline (siehe „Slide-Choreografie" oben)
- **Bullets durch Fragments ersetzen**, wenn die Bullets eine Argumentations-Sequenz sind (Punkt 1 → 2 → 3)
- **Bullets behalten**, wenn die Punkte parallel sind und gleichzeitig gelesen werden sollen (z.B. ein Glossar, eine Skizze von Optionen)
- **Max 4 Fragments** pro Slide, je < 80 Zeichen — mehr ist eine zweite Slide
- **Tabellen:** max 5 Spalten × 6 Zeilen; mehr → eigene Slide oder zwei. Tabellen NICHT als Fragments — sie sollen scanbar sein
- **Code-Snippets:** max ~10 Zeilen sichtbar; mehr → Auszug + Verweis auf Vollversion. Code NICHT als Fragments (zu nervös)
- **Bilder/Diagramme:** wenn Mermaid/SVG inline geht: bevorzugen statt externer Datei. Optional als Fragment einblenden, wenn Headline allein erst die Frage aufwerfen soll

### Speaker-Notes-Konvention (Häppchen-Stil)
Inside each `<section>`:
```html
<aside class="notes">
  Kernaussage in einem Satz. Plus konkrete Zahl/Beispiel. Übergang: „Damit kommen wir zu …".
</aside>
```
2–4 kurze Sätze. *Keine* Aufzählung im Notes-Block — der Speaker liest das im Live-Modus, da hilft Fließtext. Detaillierte Sub-Punkte stehen in `speakernotes.md`.

### Bis Jakob-CI da ist (Best Practice Defaults)
- Primary color: `#1f5fa6` (dezent business-blau, gut sichtbar auf weiß)
- Accent color: `#c2410c` (gedecktes Orange für Hervorhebungen)
- Body-Font: System-Sans-Serif (-apple-system, "Segoe UI", Roboto, …)
- Heading-Font: gleich (kein Font-Mix bis CI vorgibt)
- Code-Font: `"SF Mono", Consolas, Menlo, monospace`
- Tabellen: hellblauer Header (`#e8f0fa`), schmale Border, leichte Zebra-Streifen
- Callouts:
  - Standard: blauer Links-Border, blass-blauer Hintergrund
  - Warnung: roter Links-Border, blass-roter Hintergrund
  - Erfolg: grüner Links-Border, blass-grüner Hintergrund

**Wenn Jakob später CI liefert:** Farben/Fonts/Logo werden in einem CSS-Block oben in der Datei zentral angepasst. Bis dahin: das obige Default-Set.

### Druck/PDF-Tauglich
- Stylesheet `print/pdf.min.css` immer mitladen
- Aufruf `?print-pdf` am Ende der URL → Browser-Druck-Dialog liefert sauberes PDF
- Notes drucken: `?showNotes=true` zusätzlich
- Slide-Header/Footer optional dezent (Datum, Slide-Nummer)

## Template — reveal.js HTML

Use this as starting point. Replace `{{TITEL}}`, `{{SUBTITLE}}`, `{{AUTHOR}}`, `{{DATUM}}` and the slide sections.

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>{{TITEL}}</title>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/reveal.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/theme/white.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/highlight/monokai-sublime.min.css">

<style>
  :root {
    --primary: #1f5fa6;
    --accent: #c2410c;
    --good: #15803d;
    --warn: #b91c1c;
    --muted: #6b7280;
    --rule: #d1d5db;
    --soft-blue: #e8f0fa;
    --soft-orange: #fff7ed;
    --soft-red: #fef2f2;
    --soft-green: #ecfdf5;
  }
  .reveal { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }

  /* Whitespace-Pattern: jede Slide bekommt Atemraum und vertikale Mitte */
  .reveal .slides > section,
  .reveal .slides > section > section {
    padding: 1.5em 2em;
    box-sizing: border-box;
    display: flex !important;
    flex-direction: column;
    justify-content: center;
  }

  .reveal h1, .reveal h2, .reveal h3 { color: var(--primary); text-transform: none; letter-spacing: 0; }
  .reveal h1 { font-size: 2.0em; line-height: 1.2; }
  .reveal h2 { font-size: 1.5em; line-height: 1.25; border-bottom: 2px solid var(--primary); padding-bottom: 0.2em; margin-bottom: 0.9em; }
  .reveal h3 { font-size: 1.1em; color: var(--accent); margin-top: 0.5em; }

  /* Headline-First: prominenter Hauptaussage-Style */
  .reveal .headline { font-size: 1.6em; line-height: 1.3; color: var(--primary); margin-bottom: 1em; font-weight: 600; border-bottom: none; }

  .reveal section { text-align: left; }
  .reveal section.title-slide, .reveal section.section-title { text-align: center; }
  .reveal section.section-title { background: var(--primary); color: #fff; }
  .reveal section.section-title h1, .reveal section.section-title h2 { color: #fff; border-bottom: none; }

  .reveal ul, .reveal ol { margin-left: 1em; }
  .reveal li { margin: 0.3em 0; line-height: 1.4; }

  /* Fragments: mehr Luft zwischen den Items, damit sie visuell "landen" */
  .reveal .fragment { margin-bottom: 0.6em; }

  .reveal table { border-collapse: collapse; font-size: 0.7em; margin: 0.5em 0; }
  .reveal th, .reveal td { border: 1px solid var(--rule); padding: 0.3em 0.5em; text-align: left; vertical-align: top; }
  .reveal th { background: var(--soft-blue); color: var(--primary); }
  .reveal tr:nth-child(even) td { background: #f8fafc; }
  .reveal code { background: #eef2f7; padding: 0.1em 0.35em; border-radius: 3px; font-family: "SF Mono", Consolas, Menlo, monospace; font-size: 0.85em; }
  .reveal pre { width: 100%; box-shadow: none; }
  .reveal pre code { padding: 0.6em 0.9em; font-size: 0.50em; line-height: 1.4; }
  .reveal .callout { border-left: 4px solid var(--primary); background: var(--soft-blue); padding: 0.5em 0.9em; margin: 0.4em 0; border-radius: 0 6px 6px 0; }
  .reveal .callout.warning { border-color: var(--warn); background: var(--soft-red); }
  .reveal .callout.success { border-color: var(--good); background: var(--soft-green); }
  .reveal .twocol { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2em; }
  .reveal .footer { position: absolute; bottom: 0.6em; right: 1em; font-size: 0.5em; color: var(--muted); }
  .reveal .lead { color: var(--muted); }
  .reveal .footnote { font-size: 0.65em; color: var(--muted); margin-top: 0.6em; }
</style>
</head>
<body>

<div class="reveal">
  <div class="slides">

    <!-- Title slide -->
    <section class="title-slide">
      <h1>{{TITEL}}</h1>
      <p style="font-size: 1.1em; color: var(--muted);">{{SUBTITLE}}</p>
      <p style="margin-top: 2em; font-size: 0.7em;">{{AUTHOR}} · {{DATUM}}</p>
      <aside class="notes">
        Eröffnungs-Satz. Wer ich bin, worum es geht, wie lang das dauert.
      </aside>
    </section>

    <!-- Content slide: Headline-First + Fragment-Reveal -->
    <section>
      <h2 class="headline">Die Erweiterung spart pro Story 5 Minuten Refinement-Zeit.</h2>
      <p class="fragment fade-in">Erstes Beispiel: DoD-Items müssen nicht mehr aus den Akzeptanzkriterien herausgepuzzelt werden.</p>
      <p class="fragment fade-in">Zweites Beispiel: Implementation Notes sind sofort vom fachlichen Scope getrennt.</p>
      <p class="fragment fade-in">Drittes Beispiel: Reviewer hat die Checkliste auf einen Blick.</p>
      <aside class="notes">
        Headline lesen lassen (2 Sek Pause). Dann klicke jedes Beispiel einzeln ein, kommentiere ergänzend. Übergang: „Damit zur Frage, ob ihr das so seht.".
      </aside>
    </section>

  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/reveal.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/notes/notes.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/highlight/highlight.min.js"></script>
<script>
  Reveal.initialize({
    hash: true,
    slideNumber: 'c/t',
    transition: 'slide',
    width: 1280,
    height: 720,
    margin: 0.10,         // großzügiger Rand zum Bildschirm
    minScale: 0.2,
    maxScale: 1.5,
    plugins: [ RevealNotes, RevealHighlight ],
  });
</script>
</body>
</html>
```

## Template — speakernotes.md

```markdown
# Sprechernotizen — {{TITEL}}

> Begleit-Dokument zur Präsentation `{{TITEL}}_presi.html`. Pro Slide ein Detail-Abschnitt; die `<aside class="notes">`-Blöcke im HTML enthalten nur die Häppchen-Version.

## Vor der Präsentation
- Setup: Beamer testen, `S` für Speaker-View, `F` für Fullscreen
- Notes-Modus auf zweitem Screen offen halten (zeigt nächste Folie + Notes)
- PDF-Backup: `?print-pdf` im URL, dann Browser-Druck → PDF

---

## Slide 1 — <Titel / Headline>

**Headline (= die Kernaussage):**
…

**Was beim Aufrufen zu sehen ist:**
… (nur die Headline + ggf. ein erstes Bild — Fragments noch verborgen)

**Fragments und Klick-Reihenfolge:**
1. Klick 1 → Beispiel A erscheint. Was Du dazu sagst: …
2. Klick 2 → Beispiel B erscheint. Was Du dazu sagst: …
3. Klick 3 → Beleg C erscheint. Was Du dazu sagst: …

**Vollständiger Speaker-Text (Fließversion, falls Du den Faden verlierst):**
…

**Anekdoten / Beispiele / Daten:**
- …

**Mögliche Rückfragen + Antworten:**
- Q: …
  A: …

**Übergangs-Satz:**
…

---

## Slide 2 — …
…
```

## Nach dem Bauen — Checkliste

- [ ] HTML im Chrome/Edge öffnet → Folien navigieren mit Pfeiltasten
- [ ] `S` drücken → Speaker-View öffnet sich, Notes erscheinen
- [ ] `?print-pdf` im URL → Browser-Druck zeigt PDF-taugliche Folien (Fragments sind dann alle sichtbar)
- [ ] `?showNotes=true` → Notes werden auf jeder Slide eingeblendet (für Print-Notes-Version)
- [ ] Notes sind Häppchen (2–4 Sätze), nicht Volltext — Volltext ist in `speakernotes.md`
- [ ] **Whitespace:** Reveal-Margin = 0.10, Slides sitzen mit Rand zum Bildschirm, nichts klebt am Beamer-Rand
- [ ] **Headline-First:** jede Slide hat eine vollständige Aussage als Headline (max 80 Zeichen, 2 Zeilen)
- [ ] **Fragments:** wo Argumentations-Sequenz, dort eingesetzt (max 4 Fragments pro Slide)
- [ ] Tabellen und Code-Snippets NICHT als Fragments
- [ ] Title-Slide hat Autor + Datum
- [ ] Slide-Nummer wird gezeigt (`slideNumber: 'c/t'`)
- [ ] **Phase 4 Visual-Review-Pass durchgelaufen** — alle Slides per Chromium-Screenshot inspiziert, keine offenen visuellen Bugs (Headline abgeschnitten, Wort-pro-Zeile, Slide-Overflow, Umlaute kaputt)
- [ ] **Screenshots liegen in `<output_dir>/`** zur User-Review (Pfad in End-Bestätigung an User mitgeben)

## Verifikation

User sollte am Ende:
1. Die HTML-Datei im Browser öffnen können
2. Mit `S` in den Speaker-View springen → Notes sichtbar
3. Mit `?print-pdf` ein PDF-Ausdruck erzeugen können
4. `speakernotes.md` als Vorbereitungs-/Backup-Dokument neben dem Deck haben
