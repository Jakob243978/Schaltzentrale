# SKILL-103: creative-studio — Ad-Report (HTML) mit Review-Workflow (Status + Feedback, persistent)

**Status:** in_progress
**Erstellt:** 2026-07-12
**MoSCoW:** Must
**Geschaetzter Aufwand:** M (Report-Generator um Review-State + Persistenz + Export erweitern)
**surface:** code + docs
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** review_status_je_ad + feedback_feld + persistenz_im_html + ruecklesbar_durch_claude

## Kontext / Root-Cause
Der `ad-report.html` (SKILL-100) war reine Ansicht. Jakob arbeitet die Ads aber **durch** und will
je Ad **entscheiden und kommentieren** koennen, damit Claude gezielt nachbessert. Jakob (2026-07-12):
„wir brauchen Status pro Ad, ein Feedback-Feld, das im HTML gespeichert wird, sodass man diese dann
nochmal ueberarbeiten lassen koennte."

## Was soll erreicht werden?
Der Ad-Report ist ein **Review-Werkzeug**: pro Ad ein Status + Freitext-Feedback, beides
**persistent** und in einer Form, die **Claude zurueckgelesen** und zur gezielten Ueberarbeitung
genutzt werden kann.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Status je Ad]:** Jede Ad hat einen Status aus **`draft` (Default) · `pending` ·
      `passed` · `declined`**, sichtbar als farbiger Badge auf der Karte, setzbar im Detail-Modal.
- [x] **EARS-2 [Must, Feedback-Feld]:** Pro Ad ein Freitext-Feedback-Feld (Textarea) im Modal;
      Eingabe wird gespeichert; Karten mit Feedback tragen eine sichtbare Markierung.
- [x] **EARS-3 [Must, Persistenz]:** Status + Feedback speichern automatisch (localStorage) und
      ueberstehen Reload. Zusaetzlich **„Als HTML sichern"**: baecke den Review-State in ein
      `<script id="reviewState">` und lade die Datei herunter; beim Wiederoeffnen ist der State da.
- [x] **EARS-4 [Must, rueck-lesbar durch Claude]:** Der eingebettete `reviewState` ist valides JSON
      `{{<ad-id>: {{status, feedback}}}}` und wird beim Zurueckgeben (gespeichertes HTML oder
      Review-JSON-Export) von Claude geparst, um `declined`/kommentierte Ads gezielt zu ueberarbeiten.
- [x] **EARS-5 [Should, Durcharbeiten]:** Filter-Leiste nach Status mit Live-Zaehlern (Alle/Entwurf/
      In Pruefung/Top/Abgelehnt); Klick filtert das Karten-Grid.
- [ ] **EARS-6 [Should, projektneutral in den Generator]:** Der Report-Generator ist Teil des Skills
      (`creative_studio/ad_report.py`, SKILL-100-Folge); das Review-System ist Default jedes Reports,
      Farben/Labels aus Brand-Tokens, kein Projektwert hartkodiert.
- [ ] **EARS-7 [Must, Governance: nur „Top" geht live]:** Nur Ads mit Status **`passed` ("Top")** duerfen
      veroeffentlicht/an den Ausspiel-Agenten (z. B. **MetaAds-Agent**) uebergeben werden. **`declined`**
      -> **Archiv** (`_archiv/`, nicht veroeffentlichen), **`pending`** -> ueberarbeiten und **wieder als
      `draft`** bereitstellen (Re-Review), **`draft`** -> noch nicht reviewt, nicht veroeffentlichen. Die
      Freigabe-Quelle ist der `reviewState`/`ad-review.json`. (Anlass Jakob 2026-07-12; als Ticket
      hinterlegt, damit die Regel ueber Git in weitere Workspaces synct, nicht nur im lokalen Memory.)

## Loesungs-Skizze
- Umgesetzt (Referenz-Instanz `messaging-test-2026-07/ad-report.html`, generiert via gen-Skript):
  Review-State (localStorage + eingebettetes `reviewState`-JSON), Status-Buttons + Feedback-Textarea
  im Modal, Status-Badge + Feedback-Flag auf der Karte, Filter-Leiste mit Zaehlern, „Als HTML
  sichern" (Self-Download mit eingebettetem State, `<` -> `\\u003c` entschaerft) + „Review-JSON".
- Folge (SKILL-100/EARS-3): in den projektneutralen `ad_report.py`-Generator heben.
- Ruecklese-Konvention dokumentieren: Claude liest `reviewState` (oder `ad-review.json`), nimmt
  `declined` + `feedback` als Arbeitsauftrag, aendert **nur** die betroffenen Ads.

## Test-Ergebnis / Beleg
- Playwright-verifiziert (2026-07-12): Status setzen + Feedback -> localStorage; Reload haelt Status;
  „Als HTML sichern" -> Download mit `reviewState`-JSON; Wiederoeffnen stellt Badges wieder her;
  Filter „Top" zeigt nur passende Karten. Keine Console-Errors.

## Code-Referenzen
- Referenz-Report: `AgentischesArbeiten/marketing/ad-creatives/messaging-test-2026-07/ad-report.html`
- Generator-Prototyp: projekt-lokales gen-Skript (→ nach `creative_studio/ad_report.py`)
- Verwandt: SKILL-100 (Report als Pflicht-Deliverable)
