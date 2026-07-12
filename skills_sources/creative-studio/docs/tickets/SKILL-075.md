# SKILL-075: creative-studio — Vision-QA-Pass nach Render (agent-getriebene Checkliste + Nachrender-Pflicht)

**Status:** review
**Erstellt:** 2026-07-09
**MoSCoW:** Must
**Geschaetzter Aufwand:** S (Doku/Prozess — kein neuer Code-Pfad)
**surface:** backend
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`
**outcome_metric:** kein_abgeschnittenes_creative_geht_mehr_durch (Cut-off/Umbruch/Umlaut-Tofu/
Face-Verdeckung/Safe-Zone-Verletzung wird VOR dem Fertigmelden erkannt, weil der Agent jedes
gerenderte PNG mit dem Read-Tool ansieht und bei Treffer nachrendert) + jedes_format_einzeln_geprueft
(Feed UND Story getrennt) + kein_bestandsbruch (rein additive Doku, kein Render-Pfad geaendert)
**outcome_review_at:** null
**Wissensgrundlage:** Live-Use-Feedback Jakob (2026-07-09): Der Skill hatte **keinen** echten
Vision-Check nach dem Rendern. Dadurch ist `konzept-a-bau-partner__feed_1x1.png` (Workshop-Ads
`AgentischesArbeiten/marketing/ad-creatives/workshop/v2-personal/`) **abgeschnitten**
durchgerutscht — die CTA-Pille + Preiszeile ragten unten aus dem 1080×1080-Rahmen. Der
automatische WCAG-Kontrast-Check (SKILL-074, `--check-contrast`) misst nur eine geschaetzte
Text-Region — er faengt Cut-off, Umbrueche, Umlaut-Tofu, Face-Visibility und Safe-Zonen
**nicht** ab. Diese Fehlerklasse sieht nur ein echter Blick.

> [!info] Herkunft (Live-Use-Feedback + „Skill haerten, damit es nicht wieder passiert")
> Fuehrt die Live-Use-Lehre in den Skill zurueck (`lessons-aus-live-use-zurueckfuehren`):
> Das Muster ist bewusst **agent-getrieben** — der Agent IST das Vision-Modell, exakt wie
> beim Ad-Library-Scan (SKILL.md §9) und beim Redaktions-Pass (§11b). Kein neuer LLM-Call,
> kein externer Service, keine neue Dependency: der Agent hat das PNG ohnehin per Read-Tool
> im Kontext; der Blick kostet nur Disziplin. Deshalb Doku/Prozess statt Code.

## Was soll erreicht werden? (Business-Ziel)
Nach **jedem** Render (Bild und Video) ist ein Vision-QA-Pass **Pflicht** und Teil des
Done-Kriteriums: der Agent liest **jedes** gerenderte PNG einzeln mit dem Read-Tool
(Feed 1:1 UND Story 9:16 **getrennt**), prueft es gegen eine explizite 6-Punkt-Checkliste
und rendert bei **jedem** Treffer nach, BEVOR er „fertig" meldet. Kein Creative geht mehr
ungesehen raus.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1 [Must]:** the system (SKILL.md) shall den Vision-QA-Pass als **PFLICHT-Schritt
      nach jedem Render** vorschreiben — explizit „nicht fertig melden ohne bestandenen
      Vision-QA-Pass auf JEDEM gerenderten Format".
- [x] **EARS-2 [Must]:** the system shall den Pass **agent-getrieben** definieren (Renderer gibt
      PNG-Pfade zurueck → Agent liest JEDES PNG mit dem Read-Tool → urteilt), analog zum
      Ad-Library-/Redaktions-Muster — **kein** eigener LLM-Call/Service/Dependency.
- [x] **EARS-3 [Must]:** the system shall eine explizite Checkliste fuehren mit den sechs
      Pruefpunkten: (1) Abschneiden/Cut-off, (2) Kontrast/Lesbarkeit, (3) unschoene Umbrueche,
      (4) Umlaute/Sonderzeichen (kein Tofu/Mojibake), (5) Face-Visibility (Personal-Brand),
      (6) Safe-Zonen (Story/Reels, untere ~35 %).
- [x] **EARS-4 [Must]:** When ein Pruefpunkt an einem PNG verletzt ist, the system shall
      **Nachrender-Pflicht** vorschreiben (Layout/Parameter anpassen, betroffenes Format neu
      rendern, erneut ansehen) bis alle PNGs bestehen.
- [x] **EARS-5 [Must]:** the system shall **jedes Format einzeln** pruefen lassen (Feed UND
      Story getrennt) — ein bestandenes Feed ist kein Nachweis fuer die Story.
- [x] **EARS-6 [Should]:** the system shall die Abgrenzung zum automatischen Kontrast-Check
      (SKILL-074/§14) klarstellen: `--check-contrast` ist maschinelles Vorabsignal fuer Punkt 2,
      **ersetzt** den Vision-Pass nicht; ein gruener Kontrast-Check ist **kein** Freibrief.
- [x] **EARS-7 [nicht-brechend]:** the system shall rein additiv bleiben — kein Render-Pfad,
      keine `specs.py`, keine bestehende Skill-Funktion geaendert.

## Loesungs-Skizze (Approach)
- **`SKILL.md` Abschnitt 15 (neu):** „Vision-QA-Pass nach dem Render (PFLICHT — agent-getrieben)".
  Callout `[!important]` mit dem Pflicht-Satz + Anlass (Konzept-A-Cut-off). Verbindlicher
  5-Schritte-Ablauf (Renderer → Read je PNG, Feed+Story getrennt → Checkliste → Nachrender bei
  Treffer → Vision-QA-Beleg im Report). 6-Punkt-Checkliste mit dem Cut-off-Punkt als kritischstem.
  Abgrenzung zu §14. Begruendung „warum agent-getrieben" (Muster §9/§11b).
- **`SKILL.md` Abschnitt 13 (geschaerft):** Magnific — expliziter Kasten „Wann WIRKLICH generieren
  (nicht nur Bestand recyceln)": search-first ist Spend-Schutz, kein Zwang zum Bibliotheks-Recycling;
  bei eigenem Motiv-Bedarf ECHT generieren (`image_source generate`, `--ar square_1_1/portrait_9_16`),
  Key nie loggen, Upscale ueber denselben Client, Ehrlichkeit (`is_ai_generated` im Index).
- **Verworfen:** ein weiterer Pixel-/Heuristik-Algorithmus fuer Cut-off/Umbruch/Tofu. Diese sind
  semantische Urteile ueber die Gesamtkomposition; der Agent hat das Bild ohnehin im Kontext.
  „Intelligenz beim Agenten, Mechanik im Modul" (Linie aus §9/§11b) konsequent weitergezogen.

## Test-Ergebnis / Beleg
- **Live-Anwendung (2026-07-09):** Workshop-Creatives `v2-personal` mit dem gehaerteten Skill neu
  gebaut. Der Vision-QA-Pass hat den Konzept-A-Feed-Cut-off gefangen und den Fix erzwungen:
  Foto-Anteil im Feed 1:1 verkleinert + Textblock gestrafft → CTA-Pille + Preiszeile liegen mit
  sichtbarem Abstand ueber der Unterkante. Alle 6 PNGs (3 Konzepte × Feed/Story) einzeln per
  Read-Tool angesehen und als bestanden belegt. Konzept C mit **frisch Magnific-generiertem**
  Hintergrund (echter Gen-Call, `is_ai_generated=true` im Index).
- Kein Code-Pfad geaendert → creative-studio Test-Suite unveraendert gruen (Bestand, keine Regression).

## Code-Referenzen
- `skills_sources/creative-studio/SKILL.md` — **Abschnitt 15 neu** (Vision-QA-Pass, Pflicht,
  agent-getrieben, 6-Punkt-Checkliste, Nachrender-Pflicht, Feed/Story getrennt).
- `skills_sources/creative-studio/SKILL.md` — **Abschnitt 13 geschaerft** (Magnific „wann wirklich
  generieren" + Upscale + Ehrlichkeits-Hinweis).

## Ergebnis / Notizen
**Status review (2026-07-09).** Vision-QA-Pass als hartes Done-Gate im Skill kodifiziert
(PFLICHT, agent-getrieben, 6-Punkt-Checkliste, Nachrender-Pflicht, Feed+Story getrennt),
Magnific-Generierung geschaerft. Rein additive Doku — kein Bestandsbruch. `setup.ps1` gelaufen
(Deploy nach `~/.claude/skills/creative-studio/`).

**Offen / [J]:** Verify-Pass (frische Session) + Outcome-Review (>=14 Tage). Optionaler Folge-
Gedanke: ein leichtes maschinelles Cut-off-Vorabsignal (unterste nicht-BG-Pixelzeile vs.
Rahmen-/Safe-Kante) als Ergaenzung — bewusst zurueckgestellt, der agent-getriebene Blick ist
das primaere Gate und deckt die Fehlerklasse vollstaendig ab.
