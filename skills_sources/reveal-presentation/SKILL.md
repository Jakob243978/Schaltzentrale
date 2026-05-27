---
name: reveal-presentation
description: Build a single-file reveal.js presentation from research content. Use whenever the user asks to create a "Präsi", slide deck, presentation, or convert existing material into slides. Stores detailed researched content in `speakernotes.md` and breaks it into bite-sized notes embedded directly in `aside class="notes"` blocks on each slide. Two style modes — Default (clean white, business-tauglich, für Stakeholder-Decks) and Sandi-Style (Pastell-Sticky-Notes, warm/coaching, für Workshops/Branding/Übungen, abgeleitet aus Sandi - The Branding Fangirl PDF in assets/). Always include white space (margin 0.10), Headline-First with Fragment-Reveal pattern, and Eine-Message-pro-Slide. Defaults until user-specific CI for Jakob Sebov is supplied.
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

## Optional: Sandi-Style — Workshop / Branding / Coaching Vibe

> **Wann?** Wenn die Präsi *warmer, persönlicher, einladender* sein soll als der Default-Business-Look. Typische Fälle: Coaching-Sessions, Branding-Workshops, Personal-Brand-Decks, Hausaufgaben-Slides, „Date with your Superfan"-Übungen, kreative Strategiearbeit, alles wo der Zuhörer *aktiv mitmachen* soll.
> **Quelle:** Best Practices aus Sandi – The Branding Fangirl x AndersberaterInnen (`assets/Sandi - All Tools & Visualisierungen.pdf`).
> **Wechselbar:** Beim Anlegen einer neuen Präsi entscheiden. Default-Style (clean white, business-tauglich) bleibt erste Wahl für faktendichte / Stakeholder-Decks. Sandi-Style ist das Workshop-Schwester-Theme.

### Charakter-Merkmale auf einen Blick
- **Sticky-Note-Ästhetik** als visuelles Grundmotiv — Inhalte sitzen in farbigen, leicht abgerundeten Boxen mit Schatten, wie Post-Its auf einem Whiteboard
- **Pastellfarben mit Bedeutung**: Lila = Hauptfarbe / Standard · Mint = Alternative / „Spielbein" · Rosa = Herz / Passion / „Herzenbein" · Gelb = Akzent / Tip · Grün = DO/Booster · Rot = DON'T/Downer
- **Frage als Lead** — vor jeder Übung steht *eine* fette, große Frage; sie ist der Anker, alles andere ist Ausfüll-Material
- **Wiederkehrender Footer**: kleines Herz-Icon + „Sandi – The Branding Fangirl x AndersberaterInnen" (bei eigenen Decks ersetzen)
- **Charakter-Foto** auf Title- und Section-Slides — der Coach/Mentor visuell präsent (lockerer Pose, freundlich, mit Brand-Element)
- **Nummerierte Tools**: jede Übung trägt eine Sektion-Nummer („03 Produkttreppe", „05 Big Why für Kund:innen?")
- **Sublabel-Kategorien**: kleines Wort unter dem Titel — `Übung` · `Storytelling` · `Education` · `Sammlung` · `Recap`
- **Pill-shaped Header** statt eckiger Boxen für Kategorien/Spalten — runde Enden, farbiger Fill
- **Sehr große Headlines in schwarzer Bold-Sans-Serif** — dominiert das obere Drittel
- **Du-Form, warm, ermutigend**: „Wie willst du arbeiten?", „Wo & was steht für deine Vermarktung an?", „Hej liebe Alena!"

### Farbpalette Sandi (CSS-Variablen)

```css
:root {
  --sandi-purple-deep: #5B4FE9;     /* Title-Slides, Section-Divider, Hauptfarbe */
  --sandi-purple-pill: #6B5BFF;     /* Pill-shaped Kategorie-Header */
  --sandi-purple-sticky: #c8c4ff;   /* Lila Sticky-Notes (Standard) */
  --sandi-purple-light: #e8e5ff;    /* sehr helles Lila — Hintergründe */
  --sandi-mint: #7eebd1;            /* Mint Sticky-Notes — "Spielbein"/Alternative */
  --sandi-mint-pill: #34d399;       /* Mint Pill-Header */
  --sandi-pink: #fbcfe8;            /* Rosa Sticky-Notes — "Herzenbein"/Passion */
  --sandi-pink-pill: #ec4899;       /* Rosa Pill-Header */
  --sandi-yellow: #fef08a;          /* Gelb — Akzent/Tip */
  --sandi-green-do: #4ade80;        /* DO/Booster */
  --sandi-red-dont: #f87171;        /* DON'T/Downer */
  --sandi-text-dark: #0f172a;       /* Schwarz für Headlines */
  --sandi-heart: #22d3ee;           /* Cyan-Herz im Footer */
  --sandi-bg-white: #ffffff;        /* Content-Hintergrund */
}
```

### CSS-Klassen für Sandi-Style

```css
/* Title- und Section-Slides — tiefes Lila als Hintergrund */
.reveal section.sandi-section {
  background: var(--sandi-purple-deep);
  color: #fff;
  text-align: center;
}
.reveal section.sandi-section h1,
.reveal section.sandi-section h2,
.reveal section.sandi-section h3 { color: #fff; border-bottom: none; }

/* Sticky-Note — abgerundet, leichter Schatten */
.reveal .sticky {
  display: inline-block;
  padding: 0.7em 0.9em;
  border-radius: 6px;
  background: var(--sandi-purple-sticky);
  color: var(--sandi-text-dark);
  box-shadow: 2px 3px 8px rgba(0,0,0,0.08);
  font-size: 0.65em;
  line-height: 1.35;
  vertical-align: top;
  margin: 0.3em;
  min-width: 7em;
  max-width: 12em;
}
.reveal .sticky.mint { background: var(--sandi-mint); }
.reveal .sticky.pink { background: var(--sandi-pink); }
.reveal .sticky.yellow { background: var(--sandi-yellow); }
.reveal .sticky.empty { color: var(--sandi-text-dark); opacity: 0.5; }  /* für „..."-Platzhalter */

/* Pill-shaped Kategorie-Header */
.reveal .pill {
  display: inline-block;
  padding: 0.4em 1.2em;
  border-radius: 999px;
  background: var(--sandi-purple-pill);
  color: #fff;
  font-weight: 600;
  font-size: 0.85em;
}
.reveal .pill.mint { background: var(--sandi-mint-pill); }
.reveal .pill.pink { background: var(--sandi-pink-pill); }
.reveal .pill.outline { background: transparent; border: 2px solid var(--sandi-purple-pill); color: var(--sandi-purple-pill); }

/* Sublabel — kleines Wort unter dem Headline */
.reveal .sandi-sublabel {
  font-size: 0.55em;
  color: var(--sandi-text-dark);
  margin-top: -0.6em;
  margin-bottom: 0.6em;
  font-weight: 400;
}

/* Frage als Lead — fett, große Schrift, eigene Zeile */
.reveal .sandi-question {
  font-size: 0.95em;
  font-weight: 700;
  color: var(--sandi-text-dark);
  margin-bottom: 1.2em;
  line-height: 1.35;
}

/* Sandi-Footer mit Herz */
.reveal .sandi-footer {
  position: absolute;
  top: 0.6em;
  left: 1em;
  font-size: 0.45em;
  color: var(--sandi-text-dark);
}
.reveal .sandi-footer::before {
  content: "♥ ";
  color: var(--sandi-heart);
  font-size: 1.1em;
}

/* Sticky-Note-Row als horizontale Reihe */
.reveal .sticky-row { display: flex; flex-wrap: wrap; gap: 0.4em; margin: 0.5em 0; align-items: flex-start; }
.reveal .sticky-col { display: flex; flex-direction: column; gap: 0.4em; align-items: flex-start; }

/* Zeitachsen-Linie für Day-in-the-Life / Energietagebuch */
.reveal .timeline {
  display: flex;
  align-items: center;
  gap: 0.5em;
  margin: 1em 0;
  border-top: 2px solid var(--sandi-text-dark);
  padding-top: 1em;
  position: relative;
}
.reveal .timeline .stage { flex: 1; text-align: center; }
.reveal .timeline .stage .pill { font-size: 0.7em; }
```

### Übungs-Templates (Sandi-Pattern-Bibliothek)

Folgende wiederkehrende Layouts decken ~90 % der Workshop-Übungen ab — pro Slide einen auswählen:

**1. Standard-Übungs-Slide** (Frage + Sticky-Note-Grid zum Ausfüllen)
```html
<section>
  <div class="sandi-footer">Sandi – The Branding Fangirl x AndersberaterInnen</div>
  <h2 style="font-size: 2.4em; font-weight: 800;">03 Produkttreppe</h2>
  <div class="sandi-sublabel">Übung</div>
  <p class="sandi-question">Ein starkes Signature Offer ist die Basis für alle weiteren Formate</p>
  <div class="sticky-row" style="justify-content: center;">
    <div class="sticky">Formatableitung A</div>
    <div class="sticky">Formatableitung B</div>
    <div class="sticky">Formatableitung C</div>
  </div>
  <div style="text-align: center; margin-top: 1em;">
    <div class="pill">Dein Signature Offer</div>
  </div>
  <aside class="notes">Frage lesen lassen. Sticky-Notes als Vorlage zeigen — Team füllt sie im Workshop selbst.</aside>
</section>
```

**2. Drei-Spalter-Vergleich** (Standbein / Spielbein / Herzenbein-Pattern)
```html
<section>
  <h2 style="font-weight: 800;">03 3 Säulen Modell</h2>
  <p class="sandi-question">Welche Leistungen gehören zu welchem Bein?</p>
  <div class="sticky-row" style="justify-content: space-between;">
    <div class="sticky-col">
      <div class="pill">Standbein</div>
      <div class="sticky">…</div>
      <div class="sticky">…</div>
    </div>
    <div class="sticky-col">
      <div class="pill mint">Spielbein</div>
      <div class="sticky mint">…</div>
      <div class="sticky mint">…</div>
    </div>
    <div class="sticky-col">
      <div class="pill pink">Herzenbein</div>
      <div class="sticky pink">…</div>
      <div class="sticky pink">…</div>
    </div>
  </div>
</section>
```

**3. Problem → Lösung → Ergebnis Flow** (Big „Why" / Angebots-Cluster)
```html
<section>
  <h2 style="font-weight: 800;">05 Big "Why" für Kund:innen</h2>
  <p class="sandi-question">Warum profitieren Kund:innen von dir und wie zeigt sich das?</p>
  <div class="sticky-row" style="justify-content: space-around; align-items: center;">
    <div class="sticky-col"><div class="pill">Problem</div><div class="sticky">…</div><div class="sticky">…</div></div>
    <div style="font-size: 1.5em;">→</div>
    <div class="sticky-col"><div class="pill mint">Lösung</div><div class="sticky mint">…</div><div class="sticky mint">…</div></div>
    <div style="font-size: 1.5em;">→</div>
    <div class="sticky-col"><div class="pill pink">Ergebnis</div><div class="sticky pink">…</div><div class="sticky pink">…</div></div>
  </div>
</section>
```

**4. Zeitachse mit Post-Its oben/unten** (Energietagebuch / Day in your enVisioned life)
```html
<section>
  <h2 style="font-weight: 800;">Day in your enVisioned life</h2>
  <p class="sandi-question">Wie sieht dein Traum-Tag aus? Wo Hoch- und wo Low-Phasen?</p>
  <div class="sticky-row" style="justify-content: space-around;">
    <div class="sticky">Morgens: …</div>
    <div class="sticky">Mittags: …</div>
    <div class="sticky">Abends: …</div>
  </div>
  <div class="timeline">
    <div class="stage"><div class="pill">Morning</div></div>
    <div class="stage"><div class="pill">Flow & Focus</div></div>
    <div class="stage"><div class="pill">Lunch</div></div>
    <div class="stage"><div class="pill">Vermarktung</div></div>
    <div class="stage"><div class="pill">Night</div></div>
  </div>
</section>
```

**5. Title-/Section-Slide** (tiefes Lila, weißer Text, Charakter-Foto rechts)
```html
<section class="sandi-section">
  <p style="font-size: 0.7em; opacity: 0.9;">▶ AndersberaterInnen: Personal Brand & Business Sessions</p>
  <h1 style="font-size: 2.2em;">Hej liebe <em>Alena</em>!</h1>
  <h1 style="font-size: 2.2em;">Let's start your Personal &amp; Business Brand!</h1>
  <!-- Charakter-Foto optional rechts unten als <img> oder Hintergrund -->
</section>
```

**6. Recap-Slide** (3-Kategorien: Stärken / Ziele / Hürden)
```html
<section>
  <h2 style="font-weight: 800;">Recap: Stärken, Potenziale, Challenges</h2>
  <p class="sandi-question">Worauf kannst du zurückgreifen, wo schlummern Potenziale, was hält dich auf?</p>
  <div class="sticky-row" style="justify-content: space-between;">
    <div class="sticky-col"><p style="font-size: 0.7em;">Meine Stärken</p><div class="sticky">…</div></div>
    <div class="sticky-col"><p style="font-size: 0.7em;">Dort will ich noch hin</p><div class="sticky">…</div></div>
    <div class="sticky-col"><p style="font-size: 0.7em;">Das hält mich auf</p><div class="sticky">…</div></div>
  </div>
</section>
```

**7. Skala / Check-In** (1–10-Skala mit Emoji-Markern)
```html
<section>
  <h2 style="font-weight: 800;">01 Check-In</h2>
  <div class="sandi-sublabel">Storytelling</div>
  <p class="sandi-question">Wie fühlst du dich heute auf einer Skala von 1 bis 10?</p>
  <div style="display: flex; justify-content: space-between; border-top: 2px solid var(--sandi-text-dark); padding-top: 1em;">
    <div>1 😢</div><div>2</div><div>3</div><div>4</div><div>5</div>
    <div>6</div><div>7 👑</div><div>8</div><div>9</div><div>10</div>
  </div>
  <div class="sticky-row" style="margin-top: 1.5em;">
    <div class="sticky">…</div><div class="sticky">…</div>
  </div>
</section>
```

### Workflow-Erweiterung: Sandi-Style-Decision in Phase 1

Bei Phase 1 (Slide-Inventur, siehe Workflow oben) **zusätzlich entscheiden**:
- Ist das eine **Workshop-/Coaching-/Branding-Präsi**? → Sandi-Style empfehlen, mit User abstimmen
- Ist das ein **Business-/Stakeholder-/Status-Deck**? → Default white-clean Style bleibt
- **Mixed:** kann auch beides — Default-Slides für Daten/Argumentation + einzelne Sandi-Slides für Übungen/Aktivierung

### Disziplin-Hinweise für Sandi-Style
- **Pro Slide maximal 12 Sticky-Notes** (mehr wird optisch unruhig)
- **Sticky-Notes mit „…"** sind die Vorlage zum Ausfüllen — nicht final, der Workshop füllt sie. Bei *fertigen* Inhalts-Slides die Boxen ausfüllen
- **Maximal 3 Farben pro Slide** (z.B. Lila + Mint + Rosa) — mehr verwirrt
- **Eine Frage pro Slide** — wenn zwei Fragen, dann zwei Slides
- **Headline groß, alles andere darunter klein** — der Größenkontrast macht den Stil
- **Charakter-Foto und Footer NICHT auf jeder Slide** — Title/Section: Foto. Content-Slides: nur Footer. Schluss-Slide: Foto zurück
- **Sandi-Footer auf eigenen Decks ersetzen** durch eigenen Brand-String (z.B. „Jakob Sebov – DQM @ dm" — bis Jakobs CI da ist)

## Optional: Editorial-Mode — Jakob Sebov Personal Brand

> **Wann?** Für Jakobs eigene Personal-Brand-Decks: Vorträge, Workshop-Präsis, Tutorial-Slides, alles unter `jakse-automations.com`. Der Stil ist warm, redaktionell, mit klarer Hierarchie (großer Number-Marker links, Sublabel-Tag, Trennstrich, dann Headline mit Italic-Akzenten).
> **Quelle / Single Source of Truth:** `assets/editorial.css` (mitgeliefert im Skill) — identisch mit `personal_branding/deploy/shared/editorial.css`.
> **Wechselbar:** Phase 1 (Slide-Inventur) explizit entscheiden — Editorial bei Personal-Brand-Inhalten, Default für Stakeholder/Status, Sandi für Workshop-Übungen.

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
- **Mixed:** Editorial-Mode für die Inhalts-Slides + einzelne Sandi-Slides nur für Workshop-Übungen, wenn beide Modes benötigt werden

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
- [ ] **Bei Sandi-Style:** max 12 Sticky-Notes pro Slide, max 3 Farben, eine Frage als Lead, Sublabel (Übung/Storytelling/Education) gesetzt, Footer mit Herz-Symbol, Charakter-Foto nur auf Title/Section/Closing

## Verifikation

User sollte am Ende:
1. Die HTML-Datei im Browser öffnen können
2. Mit `S` in den Speaker-View springen → Notes sichtbar
3. Mit `?print-pdf` ein PDF-Ausdruck erzeugen können
4. `speakernotes.md` als Vorbereitungs-/Backup-Dokument neben dem Deck haben
