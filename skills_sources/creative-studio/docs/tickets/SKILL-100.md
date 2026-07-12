# SKILL-100: creative-studio — Ad-Copy-Sheet + Ad-Report als Pflicht-Deliverable jedes Ad-Satzes

**Status:** spec
**Erstellt:** 2026-07-12
**MoSCoW:** Must
**Geschaetzter Aufwand:** M (SKILL.md-Mandat + Templates jetzt; projektneutrale Generatoren `ad_copy.py`/`ad_report.py` als Folge-Implementierung)
**surface:** docs + code
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** jeder_ad_satz_liefert_ad_copy_sheet + ad_report_html + veroeffentlichungsfertig_ohne_nacharbeit

## Kontext / Root-Cause
Der Skill erzeugt bisher **nur die Creatives** (PNGs pro Typ/Format) plus die On-Image-Copy.
Fuer die **Ad-Veroeffentlichung** fehlen aber zwei Deliverables, die das Team jedes Mal braucht
und bisher manuell/aus dem Gedaechtnis nachziehen musste:

1. **Ad-Copy-Sheet** (veroeffentlichungsfertige Meta-Copy je Hook): Headline-Feld, Beschreibung,
   CTA-Button, `utm_content`, Ziel-URL + **Primaertext** (A Langform, B Kurz <125, C Variante).
   Referenz-Instanz: `AgentischesArbeiten/marketing/ad-creatives/ki-hooks-v2/copy-vorschlag.md`.
2. **Ad-Report (HTML)**: self-contained Review-/Launch-Report — Karten-Grid je Ad, Modal mit allen
   Formaten + voller Copy, Uebersichts-Stats, Metrik-Sektion (nach Launch via Meta API/UTM).
   Referenz-Instanz: `AgentischesArbeiten/marketing/ad-creatives/ad-report.html`.

**Anlass (Jakob 2026-07-12):** Beim Agentic-Messaging-Test kamen 26 Creatives + On-Image-Copy,
aber **weder Ad-Copy-Sheet noch Ad-Report** automatisch mit. Jakob: „das brauchen wir fuer die
Ad-Veroeffentlichung … ich dachte das waere im Skill mit beruecksichtigt" und „wir brauchen auch
bei sowas immer einen Ad-Report … das muss auch in ein Skill-SDD-Ticket aufgenommen werden."

## Was soll erreicht werden?
Der **Standard-Ad-Satz** (Abschnitt 2 SKILL.md) umfasst ab jetzt **drei** Ergebnis-Klassen statt
nur der Creatives:
(a) Creatives (PNG, alle Typen/Formate — Bestand),
(b) **`ad-copy.md`** (veroeffentlichungsfertiges Copy-Sheet, Struktur unten),
(c) **`ad-report.html`** (self-contained Review-/Launch-Report).
Kein Ad-Satz gilt als „fertig", solange (b) und (c) fehlen. Copy zieht ihre Argumentations-Arcs
aus `frameworks.FRAMEWORKS` (slots → Primaertext), Brand aus `branding.env`/`brand.json`; nichts
Projekt-Spezifisches wandert in den Skill-Code (Personas/VoC/Beweis bleiben Parameter/Doku).

## Akzeptanzkriterien (EARS)
- [ ] **EARS-1 [Must, Copy-Sheet-Pflicht]:** Wenn ein Ad-Satz gebaut wird, DANN entsteht ein
      `ad-copy.md` mit je Hook: Headline-Feld, Beschreibung, CTA-Button, `utm_content`, Ziel-URL
      und Primaertext A (Langform) + B (Kurz <125) + C (Variante) — plus Mapping-Tabelle
      (Creative ↔ Persona ↔ Kategorie ↔ Layout ↔ BG ↔ utm_content). Brand-Regeln (§2) eingehalten.
- [ ] **EARS-2 [Must, Report-Pflicht]:** Wenn ein Ad-Satz gebaut wird, DANN entsteht ein
      self-contained `ad-report.html`: Karten-Grid je Ad (Thumb 4:5 + Slug + Hook + Chips),
      Klick-Modal mit allen Formaten (Tabs) + voller Copy, Uebersichts-Stats, Metrik-Sektion als
      Post-Launch-Platzhalter (spaeter Meta-API/UTM). Oeffnet ohne Console-Errors.
- [ ] **EARS-3 [Must, Templates/Generatoren im Skill]:** Der Skill stellt die Vorlage bereit —
      Interim als `docs/templates/ad-copy-sheet.md`; Ziel: projektneutrale Generatoren
      `creative_studio/ad_copy.py` (Copy-Skeleton aus Framework-Arc + Baukasten) und
      `creative_studio/ad_report.py` (HTML aus Ad-Satz-Manifest), CLI-aufrufbar.
- [ ] **EARS-4 [Must, projektneutral]:** Kein Projektwert (Persona-Namen, VoC-Zitate, Beweis-Satz,
      warteliste-URL, Farb-Hex) hartkodiert in `creative_studio/*` — alles Parameter/Template.
- [ ] **EARS-5 [Should, SKILL.md-Verankerung]:** Abschnitt 2 (Standard-Ad-Satz) nennt (b)+(c) als
      Pflicht; Abschnitt 9 (Anwenden) verweist auf die Templates/Generatoren.

## Loesungs-Skizze
- **Sofort (dieses Ticket, umgesetzt):** SKILL.md Abschnitt 2 + 9 um den Pflicht-Deliverable-
  Callout erweitert; `docs/templates/ad-copy-sheet.md` als projektneutrale Vorlage angelegt.
  Arbeits-Prototyp des Report-Generators liegt als projekt-lokales Skript vor
  (`AgentischesArbeiten/.../messaging-test-2026-07` erzeugt via gen-Skript).
- **Folge (Code):** Prototyp in `creative_studio/ad_report.py` generalisieren (CSS-Theme aus
  Brand-Tokens statt hartkodiert; Datenquelle = Batch-`manifest.json`). `ad_copy.py` scaffoldet
  A/B/C-Primaertext aus `frameworks.get_arc()` + `content`-Bausteinen; Mensch schleift final.
- Batch-Modus (`render_image` Batch/`manifest.json`) um Copy-Felder erweitern, damit Report +
  Sheet direkt aus dem Manifest generierbar sind.

## Test-Ergebnis / Beleg
- Referenz-Umsetzung (projekt-lokal, 2026-07-12): `AgentischesArbeiten/marketing/ad-creatives/
  messaging-test-2026-07/` mit `ad-copy.md` (26 Hooks) + `ad-report.html` (Playwright: 26 Karten,
  0 Console-Errors, Modal mit 3 Format-Tabs + voller Copy). Dient als Abnahme-Vorlage fuer die
  projektneutralen Generatoren.

## Code-Referenzen
- `SKILL.md` Abschnitt 2 (Standard-Ad-Satz) + Abschnitt 9 (Anwenden)
- `docs/templates/ad-copy-sheet.md` (neu)
- `creative_studio/frameworks.py` (`FRAMEWORKS`, Arc-Slots → Primaertext)
- Referenz-Instanzen: `AgentischesArbeiten/.../ki-hooks-v2/copy-vorschlag.md`,
  `AgentischesArbeiten/.../ad-report.html`
