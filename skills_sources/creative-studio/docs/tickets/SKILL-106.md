# SKILL-106: Whitespace-/Spacing-System fuer den landingpage-Content-Type

**Status:** spec
**Erstellt:** 2026-07-13
**MoSCoW:** Must
**Geschaetzter Aufwand:** S (Doku-Unterabschnitt in SKILL.md §16 + Spacing-Tokens/Rhythmus-Regeln im Template; kein Code-Pfad)
**surface:** docs + web
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** neue_LP_hat_richtigen_Space_ab_start (allseitig grosszuegig, nirgends eng, nirgends leer) — ohne dass pro Sektion von Hand nachjustiert werden muss

## Kontext / Root-Cause
Anlass: Jakobs Feedback zur Referenz-LP `AgentischesArbeiten/landing/warteliste-02/index.html`.
An mehreren Stellen ist zu **wenig** Space, an anderen wirkt die Flaeche **leer**. Kernaussage:
**Whitespace gilt allseitig (rechts, links, oben, unten) — Space ist Gestaltung, darf aber NICHT
„leer" wirken.** Konkrete Problemstellen:

- Abschnitt **„Du baust dir keinen Chatbot…"** (Mechanismus) — zu wenig Space.
- Nach **„Ein Format, das in deinen Arbeitsalltag passt."** — zu wenig Abstand zur naechsten Sektion.
- **„Einer von euch"** (Beweis-Layer) — zu wenig Platz zwischen Text und Bild rechts.
- **Formular** — zu eng.

### Warum ist das passiert? (Analyse an der echten LP)
Der Content-Type war typografisch/farblich schon editorial, aber das **Spacing war unsystematisch**:

1. **Ein einziger Abstands-Token macht alles.** `--gap: clamp(2.6rem,1.8rem+3vw,5rem)` wird als
   **einzige** vertikale Einheit benutzt: `.band { padding: var(--gap) 0; }`. Es gibt keine
   Trennung zwischen **Makro-Whitespace** (zwischen Sektionen, soll grosszuegig sein) und
   **Mikro-Whitespace** (innerhalb einer Sektion, soll enger/verwandt sein). Ein Token kann nicht
   beides: content-dichte Sektionen wirken gequetscht, sparsame Sektionen wirken leer.
2. **Feste px-Innenabstaende statt fluider Skala.** Zwischenraeume wie `margin-top:16px` /
   `margin-top:26px` (inline an den H2) und `gap:14px` / `gap:16px` (Contrast/Cards/Steps) sind
   **fix und klein**. Waehrend der Container auf Desktop bis 1180px aufgeht, bleiben diese Abstaende
   winzig → „Chatbot"-Block und Karten kleben zusammen (zu wenig Space), obwohl drumherum viel
   Flaeche ist (wirkt leer). Fix ≠ proportional.
3. **Text-Spalte wird vom Bild erdrueckt.** Der Beweis-Grid gibt dem **Bild** die groessere Fraktion
   (`grid-template-columns: 0.95fr 1.05fr`) und der Gap hat keine **wirksame Untergrenze**, die mit
   dem Viewport waechst. Ergebnis: die Lesespalte wird schmal, der Gutter zwischen Text und Bild
   bleibt duenn → „zu wenig Platz Text↔Bild". Zusaetzlich hat das Bild rechts keinen eigenen
   Atem — Whitespace ist eben **allseitig**, nicht nur „zwischen" den Elementen.
4. **Space ohne Anker liest als Lücke.** Wo eine `.band` volle `--gap`-Polsterung bekommt, aber nur
   eine schmale, zentrierte `.measure` drin sitzt, entsteht eine breite Band-Flaeche um ein kleines
   Text-Inselchen → das ist **passiver** Whitespace (wirkt „leer/kaputt"), nicht **aktiver** (der
   ein Fokus-Element umhalot). Genau das ist Jakobs „wirkt leer".

### Was ist die gute Umsetzung?
- **Eigene fluide `--space-*`-Skala** (clamp-basiert) als Tokens — **jeder** Abstand skaliert mit dem
  Viewport, kein festes px mehr. Eine Skala, konsistenter Rhythmus (Editorial-Aequivalent zum 8px-Grid,
  aber fluid).
- **Zwei-Ebenen-Rhythmus (Makro > Mikro):** Sektions-Polsterung ist **grosszuegig** (`--space-section`,
  eigener grosser Token), Abstaende **innerhalb** einer Sektion sind **kleiner** und gestuft. Regel:
  „innen eng/verwandt, zwischen den Sektionen grosszuegig".
- **Grid-Gap mit echter, skalierender Untergrenze** (allseitig): Text↔Bild-Gutter hat einen Boden
  (z.B. `min 1.75rem`) und waechst mit dem Viewport; die **Lesespalte** bekommt Paritaet oder mehr
  (Text-Fraktion ≥ Bild-Fraktion), damit Text nie erdrueckt wird; Sektions-Polsterung sorgt fuer den
  Atem links/rechts/oben/unten am Bild selbst.
- **Space ≠ Leere:** Makro-Whitespace muss immer **etwas umhalot** (Headline, Zahl, Bild). Sparsame
  Sektion → entweder Band-Polsterung reduzieren ODER Gewicht/Anker hinzufuegen (Eyebrow-Rule,
  Zahl, Bild), nie eine weite Band um eine winzige zentrierte Text-Insel stehen lassen.

## Akzeptanzkriterien (EARS)
- [ ] **EARS-1 [Must, fluide Spacing-Skala als Tokens]:** Das Template `templates/landingpage/index.template.html`
      definiert im `:root` eine **fluide `--space-*`-Skala** (clamp-basiert, gestuft von 3xs bis 2xl)
      plus einen dedizierten `--space-section`-Token fuer die Sektions-Polsterung. Es gibt **keine
      neuen festen px-Abstaende** fuer Section-/Block-Rhythmus; SKILL.md §16 dokumentiert die Skala.
- [ ] **EARS-2 [Must, Section-Rhythmus oben/unten]:** `.band` bezieht seine vertikale Polsterung aus
      `--space-section` (allseitig gedacht: oben UND unten). SKILL.md formuliert die Rhythmus-Regel
      **„zwischen Sektionen grosszuegiger als innerhalb einer Sektion"** (Makro > Mikro) und nennt die
      Mindest-/Rhythmus-Werte, sodass „nach ‚Ein Format…' zu wenig Abstand" strukturell nicht mehr
      auftritt.
- [ ] **EARS-3 [Must, Text↔Bild-Gap allseitig]:** Editorial-Grids mit Text neben Bild (Hero, Beweis)
      nutzen einen **Gap mit skalierender Untergrenze** (fluid, echter Boden) und geben der **Lesespalte
      mindestens Paritaet** (Text-Fraktion ≥ Bild-Fraktion). SKILL.md dokumentiert die Grid-Gap-Regel
      inkl. „Whitespace ist allseitig" (Gutter + Sektions-Polsterung am Bildrand).
- [ ] **EARS-4 [Must, Anti-Pattern „leere Flaeche" vs. „grosszuegiger Space"]:** SKILL.md §16 enthaelt
      ein **Do/Don't** zum Prinzip **„Space ≠ Leere"** (aktiver vs. passiver Whitespace; Makro-Space
      muss etwas umhalot; sparsame Band → Polsterung runter ODER Anker rein).
- [ ] **EARS-5 [Should, Vision-QA-Check fuer Spacing]:** Die Vision-QA-Pflicht (§16g) wird um einen
      expliziten **Spacing-Check** erweitert: Desktop 1440 + Mobile 390 daraufhin ansehen, dass (a)
      Sektionen sich klar absetzen, (b) Text neben Bild nicht klebt, (c) keine Band als leere Flaeche
      um eine winzige Text-Insel wirkt.
- [ ] **EARS-6 [Must, projektneutral + nicht-brechend]:** Kein Projektwert im Template. Bestehende
      Content-Types (Bild/Video, `specs.py`) bleiben unveraendert; `python -m pytest tests/ -q` bleibt
      gruen.

## Loesungs-Skizze
- **SKILL.md** neuer Unterabschnitt **§16i „Spacing-/Whitespace-System (Space ≠ Leere)"**: fluide
  `--space-*`-Skala, Section-Rhythmus-Regel (Makro > Mikro), Text↔Bild-Gap-Regel (allseitig, Boden,
  Text-Paritaet), Do/Don't „Space ≠ Leere". Querverweis aus §16b („Struktur statt Leere") und §16h
  (Ablauf-Schritt). §16g bekommt den Spacing-Check.
- **Template** `templates/landingpage/index.template.html`: `--space-*`-Skala + `--space-section` im
  `:root`; `.band` auf `--space-section`; fluide Gaps mit Boden fuer `.contrast`/`.steps`/`.cards`/
  `.proof-grid`/`.form-layout`; Lesespalte ≥ Bild-Fraktion in Hero/Proof; feste inline-margins durch
  Skala-Tokens ersetzen wo sie den Rhythmus tragen.

## Test-Ergebnis / Beleg
- Offen (spec). Abnahme: neue LP aus dem Template hat allseitig richtigen Space (nirgends eng, nirgends
  leer), ohne Hand-Nachjustierung; Vision-QA (Desktop 1440 + Mobile 390) bestaetigt Spacing-Check.
- `python -m pytest tests/ -q` bleibt gruen (reine Doku+Template, kein Code-Pfad angefasst).

## Code-Referenzen
- `SKILL.md` §16 (neuer Unterabschnitt 16i; Querverweise 16b/16g/16h)
- `templates/landingpage/index.template.html` (`:root` Spacing-Tokens, `.band`, Editorial-Grids)
- Anlass/Belegquelle: `AgentischesArbeiten/landing/warteliste-02/index.html`
- Vorgaenger-Ticket (Content-Type): SKILL-105
- Recherche-Prinzipien: Micro/Macro-Whitespace, vertical rhythm (tight-within/generous-between),
  aktiver vs. passiver Whitespace, fluid spacing (clamp), asymmetrischer Grid-Gutter + Reading-Measure
