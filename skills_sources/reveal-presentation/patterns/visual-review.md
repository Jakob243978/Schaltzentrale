# Pattern: Visual-Review-Pass (Phase 4)

> Reveal-Decks werden in Browsern gerendert, nicht in HTML-Parsern. Layout-Bugs (CSS-Grid-Auto-Flow, Flex-Overflow, Wort-pro-Zeile-Wraps) sind im Quellcode **nicht** sichtbar — nur im gerenderten Screenshot. Dieses Pattern operationalisiert die visuelle Inspektion.

## Anti-Pattern

> [!danger] Niemals "fertig" melden ohne Screenshot-Pass durchgelaufen
> Code-Read reicht nicht. Wenn der Screenshot ein Problem zeigt → erst fixen, dann erneut screenshotten. Erst dann an User übergeben.

## Verfahren

1. **Temp-HTML mit Fragments-sichtbar erzeugen** (Reveal versteckt Fragments per Default — Screenshot würde nur Slide-Initialzustand zeigen):
   ```bash
   sed 's|</style>|.reveal .fragment{opacity:1!important;visibility:visible!important;}\n</style>|' \
     presi.html > /tmp/presi_visible.html
   ```

2. **Wrapper-Script aufrufen:**
   ```bash
   tools/screenshot_slides.sh <presi.html> <n_slides> <output_dir>
   # oder unter Windows PowerShell:
   .\tools\screenshot_slides.ps1 -Presi presi.html -NSlides 16 -OutputDir C:\temp\shots
   ```
   Output: `slide_00.png` bis `slide_NN.png` in `<output_dir>`.

3. **Pro Slide mit Read-Tool inspizieren** (Claude kann PNGs lesen). Check-Liste durchgehen (unten).

4. **Bei Auffälligkeit** → CSS/HTML-Fix → einzelne Slide neu screenshotten → nochmal lesen. Max 3 Auto-Iterationen pro Slide. Bei strukturellen Problemen (Aufteilung nötig, Inhalt zu groß) → User entscheidet.

5. **Wenn alle Slides clean** → Sammel-Bestätigung an User, Screenshots-Pfad angeben, ready für inhaltliche Review.

## Visual-Check-Liste (6 Punkte pro Slide)

1. **Headline vollständig sichtbar** — nicht oben oder unten abgeschnitten? Slide-Höhe-Overflow ist häufig, weil `display:flex; justify-content:center; overflow:hidden` zentriert und Inhalt rechts/links/oben/unten verschluckt.
2. **Items/Bullets brechen sinnvoll** — kein Wort-pro-Zeile-Layout, kein einzelner Buchstabe hinter `<br>`. Häufige Ursache: `display:grid` auf Listen-Items macht inline-Children zu separaten Grid-Cells.
3. **Slide-Höhe-Overflow** — letzte Bullet noch sichtbar? Footer/Statement noch da? Wenn Inhalt > 1080p: Aufteilen oder Inhalt kürzen.
4. **Umlaute korrekt gerendert** — kein `Ã¼` statt `ü`, kein Tofu-Block für fehlende Glyphen. Falls Tofu: Font fehlt (CDN-Block?) oder Encoding falsch.
5. **Fragment-Override greift** — alle Inhalte sichtbar im Screenshot, nicht nur erstes Fragment. Wenn nur Headline sichtbar: Override-CSS wurde nicht injiziert.
6. **Farben/Akzente erkennbar** — kein versehentlich-weiß-auf-weiß durch CSS-Konflikt (z.B. `section.dark` Text auf hellem Hintergrund weil `data-background-color` fehlt).

## Live-Beispiele aus BeyerImmo-Onboarding (2026-05-27)

Drei Failure-Modes in einer Präsentation, die ohne Screenshot-Pass nicht erkannt wurden. ~1 Stunde User-Feedback-Loops gekostet.

### 1. CSS-Grid-Auto-Flow-Bug (Wort-pro-Zeile)

**Symptom (Screenshot):** Auf Slide 2 + 4 zerlegte sich `<li><strong>X</strong> · text</li>` so:
```
Lieferanten umlenken
→
direkt
an
info@.
```
Jedes Wort eine eigene Zeile.

**Ursache:** Die CSS-Regel
```css
.reveal .items > li {
  display: grid;
  grid-template-columns: 2.2em 1fr;
}
```
behandelte direkte inline-Children (`<strong>` + folgender Text) als separate Grid-Items, die in zusätzliche Grid-Rows umbrachen.

**Recovery:** `display: grid` ersetzt durch `position: relative` + `::before` absolut positioniert links statt Grid-Spalte 1:
```css
.reveal .items > li {
  position: relative;
  padding: 0.45em 0 0.45em 2.7em;
}
.reveal .items > li::before {
  content: attr(data-num);
  position: absolute;
  left: 0;
  top: 0.45em;
  width: 2.2em;
}
```
Inhalt fließt jetzt normal als Block, inline-Kinder bleiben zusammen.

### 2. Slide-Höhe-Overflow (Headline halb weg)

**Symptom:** Slide 4 (Accent-Bg) zeigte nur die untere Hälfte der Headline + Sub-Lead, Items komplett verschluckt.

**Ursache:** `display:flex; flex-direction:column; justify-content:center; overflow:hidden` zentriert vertikal — wenn Inhalt zu groß für 1080p, wird oben **und** unten gleichermaßen abgeschnitten.

**Recovery (Optionen):**
- Inhalt kürzen (am ehrlichsten — wenn nicht alles reinpasst, ist die Slide zu voll)
- Headline-Size reduzieren (`font-size: 2.9em` → `2.3em`)
- Slide in zwei aufteilen
- `justify-content: flex-start` statt `center` (Inhalt sitzt oben, Bottom-Schnitt — wenigstens Headline garantiert sichtbar)

### 3. Sub-Text-Pattern war Symptombehandlung statt Ursache

**Symptom:** Über mehrere Iterationen wurden Bullets mit `<br>` + Sub-Span aufgesplittet, max-width erhöht — Problem blieb (siehe 1).

**Lesson:** Wenn `<br>`+Sub-Pattern oder max-width-Tweaks das Problem nicht lösen, ist die **CSS-Grundstruktur** verdächtig. Screenshot inspizieren statt Code-Pattern stapeln.

## Bekannte Failure-Modes (Kandidaten für KNOWN_FAILURES.md sobald SKILL-006 live)

- CSS-Grid-Auto-Flow auf List-Items
- Slide-Höhe-Overflow durch zentriertes Flex + overflow:hidden
- Fragment-Reveal-Test ohne Override (Screenshot zeigt nur 1. Fragment)
- Umlaut-Encoding-Drift (Datei als UTF-16 statt UTF-8 gespeichert, Browser zeigt Tofu)
- Webfont-CDN-Block (Fonts laden nicht, Browser-Fallback macht Layout größer)

## Token-Trade-Off

PNG-Inspektion via Read-Tool kostet ~1.5k Tokens pro 1920×1080-Slide. Bei 16 Slides ~24k Tokens extra pro Build. Trade-Off: deutlich weniger als die User-Feedback-Schleifen + Re-Reads großer HTML-Files vorher (geschätzt 50-100k pro Iteration). Phase 4 spart Tokens, auch wenn sie pro Build welche kostet.
