# SKILL-105: creative-studio — Content-Type `landingpage` (reproduzierbares LP-Bau-System)

**Status:** spec
**Erstellt:** 2026-07-13
**MoSCoW:** Must
**Geschaetzter Aufwand:** M (Doku-Sektion in SKILL.md + wiederverwendbares Template/Skelett + README; kein neuer Render-Pfad)
**surface:** docs + web
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** neue_LP_reproduzierbar_aus_template (statt Copy-Paste alter LP) + brand_konform_ab_start (Brand-Tokens + Editorial-Desktop + Szenen-Match ohne Neu-Erfindung)

## Kontext / Root-Cause
Der Skill deckte bisher nur **Bild** (Playwright/HTML-CSS) und **Video** (Remotion) als Content-Types
ab. Landingpages entstanden ausserhalb des Skills, ad-hoc, und erbten wiederholt ein
nicht-brandkonformes Desktop-Geruest (680-px-Handy-Spalte, durchgehend Navy, System-Sans).

Anlass: der Neubau `AgentischesArbeiten/landing/warteliste-02/index.html` (Bau-Briefing
`landing/warteliste-02/_briefing.md`) loest genau dieses Problem — **editoriales Desktop-Layout**
(zweispaltiger Founder-Hero, warmer Cream/Navy-Rhythmus, Serif-Display), **Brand-Token-Anbindung**
(`--brand-*`, kein hartkodierter Hex), **self-hosted Fonts** (kein CDN, file://- und Deploy-tauglich),
**dynamischer Szenen-Match** (utm_content → Hero-Headline, Message-Match Ad↔LP) und eine
**Conversion-Checkliste**. Diese Referenz-Implementierung soll als **Content-Type `landingpage`** in
den Skill abstrahiert werden, damit die naechste LP reproduzierbar aus einem Template + Doku entsteht
statt aus dem Kopieren einer projektspezifischen Datei.

Kernerkenntnis, die der Content-Type traegt: **"Auf Mobile ist eine Spalte die Loesung, auf Desktop
das Problem."** Mobile-first, aber ab dem Desktop-Breakpoint eine eigene, editoriale Buehne
(mehrspaltiger Hero/Proof/Fuer-wen), nicht die hochskalierte zentrierte Handy-Spalte.

## Was soll erreicht werden?
Ein dokumentierter, wiederverwendbarer Content-Type `landingpage`: Sektions-Schema + Brand-Token-Anbindung
+ Editorial-Desktop/Mobile-Prinzipien + Szenen-Match-Hook + Conversion-Checkliste + Voice-/Beweis-Governance.
**Projektneutral** — die warteliste-Copy bleibt Beispiel/Referenz, im Template stehen Platzhalter.

## Akzeptanzkriterien (EARS)
- [ ] **EARS-1 [Must, Sektions-Schema]:** SKILL.md dokumentiert die verbindliche LP-Sektionsabfolge
      (Sticky-CTA-Header → zweispaltiger Founder-Hero → Ad-Erkennungswert/Message-Bridge → Engpass →
      Mechanismus → Dimensionen entwaessert → Format → Beweis-Layer → Testimonial → Formular → Footer)
      mit **Zweck je Sektion**. Das Template `templates/landingpage/index.template.html` enthaelt jede
      Sektion als kommentierten Platzhalter-Block in derselben Reihenfolge.
- [ ] **EARS-2 [Must, Brand-Tokens]:** Alle Farben/Fonts der LP beziehen sich auf `--brand-*` aus
      `tokens.css`/`branding.env` (ADR-010) über lokale Aliase mit Live-Fallback — **kein hartkodierter
      Brand-Hex**. Serif-Display + Body-Font sind **self-hosted** (`@font-face`, kein externer CDN,
      wegen Deploy + file://). Template und Doku belegen das Muster.
- [ ] **EARS-3 [Must, Editorial-Desktop + Mobile-Responsive]:** Das Template ist mobile-first (eine
      Spalte, voll-breite CTAs, 16px-Inputs, Sticky-Mobile-CTA) und schaltet ab Desktop-Breakpoint auf
      **editoriales mehrspaltiges Layout** (asymmetrischer Hero-Grid, zweispaltige Quotes/Proof, breiter
      strukturierter Container ~1180px mit Lesespalte ~680px). Das Kern-Learning
      ("Mobile eine Spalte = Loesung, Desktop = Problem") steht als Prinzip in SKILL.md.
- [ ] **EARS-4 [Must, Szenen-Match-Hook]:** Das Template enthaelt den `HERO_SCENES`/`swapHeroForUtm()`-
      JS-Block (utm_content → Hero-Headline, robust in try/catch, kein Treffer → starker Default) als
      Conversion-Feature (Message-Match Ad↔LP), projektneutral mit Platzhalter-Szenen + Anleitung, wie
      die Matcher an die live geschalteten Ad-Slugs gebunden werden.
- [ ] **EARS-5 [Should, Conversion-/QA-Governance]:** SKILL.md nennt die LP-Conversion-Checkliste,
      die **Voice-Regeln** (du-Form, keine Tool-Namen, Motivation statt Angst, KEINE Gedankenstriche,
      Szene statt These — wiederverwendet aus den Copy-Anti-Listen §4c/SKILL-087), die
      **Beweis-Zahlen-Governance** (nur freigegebene Zahlen; 16→30 ok, andere erst nach Einzel-Freigabe)
      und die **Vision-QA-Pflicht** (Desktop 1440 + Mobile 390, Default + utm-Szenen) — analog zum
      Bild-Vision-QA (§15).
- [ ] **EARS-6 [Must, projektneutral + nicht-brechend]:** Kein Projektwert (warteliste-Copy, Founder-Name,
      konkrete Ad-Slugs) hartkodiert im Template — Platzhalter + README. Bestehende Content-Types
      (Bild/Video, `specs.py`, Frameworks) bleiben unveraendert; `python -m pytest tests/ -q` bleibt gruen.

## Loesungs-Skizze
- **SKILL.md** neue Sektion "16. Landingpage (Content-Type)": Sektions-Struktur (Zweck je Sektion),
  Editorial-Desktop-Prinzip, Brand-Tokens, Szenen-Match, Voice-Regeln, Beweis-Zahlen-Governance,
  Vision-QA-Pflicht. Verweis auf die Referenz-LP + Briefing als Vorbild.
- **Template** `templates/landingpage/index.template.html` — abstrahiert aus warteliste-02:
  `@font-face` (self-hosted, Kommentar-Hinweis), `:root`-Token-Aliase (`--brand-*`-Fallback),
  fluide clamp-Skala, `.band--cream/--cream-alt/--navy`-Rhythmus, asymmetrischer Hero-Grid,
  Sticky-Header + Mobile-CTA, Consent-Banner-Platzhalter, `HERO_SCENES`/`swapHeroForUtm()`-Block.
  Copy = `{{PLATZHALTER}}`, keine projektspezifische warteliste-Copy.
- **README** `templates/landingpage/README.md` — Schritt-fuer-Schritt: Template kopieren → Brand-Tokens
  binden → Sektions-Copy fuellen (Voice-Regeln) → Szenen-Matcher an Ad-Slugs binden → Fonts einbetten →
  Vision-QA (Desktop+Mobile). Verweis auf `web-mobile-design`-Skill als Bau-Checkliste.

## Test-Ergebnis / Beleg
- Offen (spec). Abnahme: aus dem Template entsteht eine neue LP ohne Copy-Paste einer alten LP; sie ist
  brand-konform (Tokens), editorial auf Desktop, responsiv auf Mobile, mit funktionierendem Szenen-Match.
- Referenz-Beleg (Vorbild): `AgentischesArbeiten/landing/warteliste-02/index.html` +
  `landing/warteliste-02/_briefing.md`.
- `python -m pytest tests/ -q` bleibt gruen (reine Doku+Template, kein Code-Pfad angefasst).

## Code-Referenzen
- `SKILL.md` (neue Sektion 16 "Landingpage (Content-Type)")
- `templates/landingpage/index.template.html`, `templates/landingpage/README.md`
- Vorbild: `AgentischesArbeiten/landing/warteliste-02/index.html` + `_briefing.md`
- Brand-Token-Konvention: ADR-010 / AgentischesArbeiten TICKET-123 (`branding.env` → `tokens.css`)
- Wiederverwendete Copy-Governance: SKILL.md §4c / SKILL-087 (Gedankenstrich-Verbot), §15 (Vision-QA)
