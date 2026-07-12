# Content-Type `landingpage` — Bau-Anleitung

Wiederverwendbares Geruest fuer eine **brand-konforme, konvertierende Landingpage**
(Warteliste / Angebot). Abstrahiert aus der Referenz-LP
`AgentischesArbeiten/landing/warteliste-02/index.html` (Vorbild) + Bau-Briefing
`landing/warteliste-02/_briefing.md`. Volldoku: **SKILL.md §16**.

Kern-Prinzip: **"Auf Mobile ist eine Spalte die Loesung, auf Desktop das Problem."**
Mobile-first, aber ab Desktop-Breakpoint eine eigene, **editoriale** Buehne
(zweispaltiger Founder-Hero, warmer Cream/Navy-Rhythmus, Serif-Display) — nicht die
hochskalierte zentrierte Handy-Spalte.

## Dateien
- `index.template.html` — kommentiertes Skelett mit `{{PLATZHALTER}}` je Sektion,
  Brand-Token-Aliasen, fluider Typo-Skala, Editorial-Responsive-CSS, Szenen-Match-JS,
  Consent-Banner + Formular-Skelett.

## Schritt fuer Schritt

1. **Kopieren.** `index.template.html` → `landing/<site>/index.html` im Projekt-Repo.

2. **Brand-Tokens binden (Pflicht, ADR-010 — kein hartkodierter Hex).**
   - `tokens.css` aus `branding.env` rendern lassen (`gen-tokens.ps1`, laeuft im
     `deploy-landing.ps1`) und neben die `index.html` legen. Der `<link rel="stylesheet"
     href="tokens.css">` ist schon drin.
   - Die `:root`-Aliase (`--navy`/`--cream`/`--coral` …) mappen auf `--brand-*` mit
     Live-Default-Fallback → funktioniert auch beim `file://`-Test ohne `tokens.css`.
   - Marke aendern spaeter = **nur `branding.env`**, sonst nichts.

3. **Fonts self-hosted einbetten (kein CDN).** Serif-Display (H1/H2) + Body-Sans als
   `woff2` unter `fonts/` ablegen (oder base64 in die `@font-face`-`src` einbetten wie
   in der Referenz-LP). Grund: Deploy per scp auf VPS, `file://`-Test hat keinen Netz,
   CWV/Datenschutz. Die `@font-face`-Bloecke oben anpassen (`{{SERIF_FONT_FILE}}`/`{{BODY_FONT_FILE}}`).

4. **Sektions-Copy fuellen** (alle `{{PLATZHALTER}}`), Reihenfolge S0–S10:
   Sticky-Header · zweispaltiger Founder-Hero · Ad-Erkennungswert/Message-Bridge ·
   Engpass · Mechanismus · Dimensionen (entwaessert) · Format · Beweis-Layer ·
   Testimonial (optional) · Formular · Footer. Zweck je Sektion: SKILL.md §16a.
   **Voice-Regeln (§16e):** du-Form, nie "Geschaeftsfuehrer"; **Szene statt These**
   (Uhrzeit/Ort/Handgriff, keine abstrakte Behauptung); Motivation statt Angst;
   keine Tool-/Produktnamen; **KEINE Gedankenstriche** (—/– tabu, Komposita-Bindestrich ok);
   **kein Preis**; Verknappung nur ehrlich.

5. **Beweis-Zahlen (§16f).** Nur **freigegebene** Zahlen einsetzen. Referenz: `16 → 30`
   ist frei; alle anderen Zahlen erst nach Einzel-Freigabe des Auftraggebers. Nichts erfinden.

6. **Szenen-Match an Ad-Slugs binden (§16d).** Im `HERO_SCENES`-Array je live geschaltetem
   Top-Ad-Slug einen Eintrag `{ m: ["<slug-fragment>"], h1: '<Szene> <em>…</em>' }` setzen.
   Fragment-Match (greift bei utm-Praefix/-Suffix), robust in try/catch, kein Treffer →
   Default-Hero bleibt. `deriveZielgruppe()` an das eigene utm_content-Namensschema anpassen.

7. **Formular anbinden.** Endpoint im `submit`-Handler (`TODO: fetch(POST)`) setzen;
   Erfolgs-View + Next-Step fuellen. Consent-Banner-Wortlaut mit Recht abstimmen;
   Marketing-Pixel erst nach Zustimmung laden (`loadPixel()`-Hook).

8. **Vision-QA (§16g) — Pflicht vor "fertig".** Die gerenderte Seite selbst anschauen:
   **Desktop 1440 UND Mobile 390**, jeweils **Default-Hero UND mindestens eine utm-Szene**
   (`?utm_content=<slug>`), plus Formular-Erfolgs-View. Pruefen: kein Horizontal-Scroll,
   Founder-Gesicht frei, Umlaute korrekt (kein Tofu/Mojibake), Kontrast WCAG-AA,
   Tap-Targets ≥44px, Editorial-Desktop greift wirklich (nicht die Handy-Spalte),
   Szenen-Match tauscht die H1. Fuer web-Surfaces gilt zusaetzlich die Projekt-Regel
   **surface: web ⇒ Playwright/UI-Verifier-Pflicht**; den `web-mobile-design`-Skill als
   Bau-Checkliste laden, **bevor** HTML/CSS geschrieben wird.

## Konventionen (kurz)
- **Deploy** ueber `scripts/deploy-landing.ps1` bzw. gegated `deploy-web.ps1` — nie am Gate vorbei.
- **noindex,nofollow** bleibt bei Wartelisten.
- **UTF-8 / Umlaute:** Content ueber Write/Edit schreiben, kein PowerShell-Roundtrip ohne `-Encoding UTF8`.
- **Customer Journey** (`docs/customer-journey.html`) beim Live-Gang nachziehen.
