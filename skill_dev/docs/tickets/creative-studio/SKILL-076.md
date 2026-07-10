# SKILL-076: creative-studio — alle drei Standard-Formate (1:1, 4:5, 9:16) als Default rendern

**Status:** review
**Erstellt:** 2026-07-09
**MoSCoW:** Must
**Geschaetzter Aufwand:** S (Default-Set + Doku; kein neuer Render-Pfad)
**surface:** backend
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`
**outcome_metric:** kein_standardformat_faellt_mehr_still_weg (jeder Default-Lauf erzeugt 1:1 UND
4:5 UND 9:16; 4:5 = Meta-Feed-Portrait-Default darf nie fehlen) + kein_bestandsbruch (additive
Erweiterung des Default-Sets, bestehende explizite Format-Listen unveraendert)
**outcome_review_at:** null
**Wissensgrundlage:** Live-Use-Feedback Jakob (2026-07-09): Die letzten Workshop-Ads kamen nur als
**1:1 (Feed square) + 9:16 (Story)** raus — das **4:5 (Feed portrait, 1080×1350)** fehlte komplett.
Jakob erwartet: standardmaessig werden IMMER alle drei Meta-Standard-Formate (1:1, 4:5, 9:16)
generiert.

## Root-Cause (wo genau 4:5 verloren ging)
Das Format **existiert** in `specs.py` als vollwertiges `feed_4x5` (4:5, **1080×1350**, Safe-Zones
oben ~14 % / unten ~20 % / seitlich ~5,5 %) — es fehlt also **nicht** im Katalog.

Der Fehler lag **allein im Default-Set**:
```python
# vorher (specs.py)
DEFAULT_FORMATS: tuple[str, ...] = ("feed_4x5", "story_9x16")
```
Das Default-Set enthielt nur **zwei** Formate ("Universal-Set, deckt 90 %+ der Placements ab") —
und **nicht** alle drei. Es gab **kein** dokumentiertes "immer alle drei rendern"-Soll. Die
Ad-Agenten, die die Workshop-Ads bauten, haben die Formate **explizit** angefragt und dabei 1:1 +
9:16 gewaehlt und 4:5 schlicht weggelassen. Weil weder der Code-Default noch die `SKILL.md` "alle
drei" erzwang, fiel das 4:5 lautlos weg und niemandem fiel es auf.

Also: **nicht** ein fehlendes Format in `specs.py`, sondern (a) ein zu kleines Default-Set und
(b) eine fehlende SKILL.md-Pflicht "immer alle 3". Beides wird hier behoben.

## Was soll erreicht werden? (Business-Ziel)
Ein Creative wird per Default **immer** in allen drei Meta-Standard-Formaten erzeugt: **1:1**
(1080×1080, Feed square), **4:5** (1080×1350, Feed portrait) **und** **9:16** (1080×1920,
Story/Reels). Eine kleinere Format-Liste nur, wenn der User ausdruecklich weniger will. Der
Vision-QA-Pass (Abschnitt 15) gilt danach **pro Format einzeln** — also auch das 4:5 wird separat
angesehen.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1 [Must]:** the system (`specs.py`) shall `DEFAULT_FORMATS` = **alle drei** Standard-
      Formate `("square_1x1", "feed_4x5", "story_9x16")` fuehren (Reihenfolge 1:1 → 4:5 → 9:16).
- [x] **EARS-2 [Must]:** When kein Format explizit angefragt wird, the system shall **1:1 UND 4:5
      UND 9:16** rendern — sowohl im Einzel-Renderer (`render_image` `--formats`-Default) als auch
      in der Batch-Engine (`batch.run_batch`, `job.formats` fehlt → `DEFAULT_FORMATS`).
- [x] **EARS-3 [Must]:** the system shall sicherstellen, dass **4:5 (`feed_4x5`, 1080×1350)** ein
      vollwertiges Format mit korrekten Meta-Feed-Portrait-Safe-Zones ist (bereits vorhanden —
      im Default-Set verankert, damit es nicht mehr weggelassen wird).
- [x] **EARS-4 [Must]:** the system (`SKILL.md`) shall die Regel **"standardmaessig immer alle drei
      Formate (1:1, 4:5, 9:16) rendern; Abweichung nur, wenn der User ausdruecklich weniger will"**
      explizit verankern.
- [x] **EARS-5 [Should]:** the system shall den Vision-QA-Pass (Abschnitt 15) so schaerfen, dass er
      **pro Format einzeln** gilt (1:1, 4:5 UND 9:16 getrennt angesehen) — 4:5 ausdruecklich
      mitgeprueft.
- [x] **EARS-6 [nicht-brechend]:** the system shall rueckwaerts-kompatibel bleiben — ein Aufrufer,
      der eine explizite Format-Liste uebergibt (`--formats ...` bzw. `job.formats`), bekommt
      exakt diese Liste; nur der **Default** waechst von 2 auf 3 Formate. Kein Format entfernt,
      keine Signatur geaendert.

## Loesungs-Skizze (Approach)
- **`specs.py`:** `DEFAULT_FORMATS` von `("feed_4x5", "story_9x16")` auf
  `("square_1x1", "feed_4x5", "story_9x16")` erweitert; Kommentar erklaert Anlass + Reihenfolge.
  `render_image.py` (`--formats`-Default) und `batch.py` (`job.formats or DEFAULT_FORMATS`) lesen
  diese Konstante bereits → beide Einstiegspunkte profitieren ohne weitere Code-Aenderung.
- **`SKILL.md`:** (1) Format-Katalog-Zeile auf das neue Default-Set aktualisiert; (2) neuer
  `[!important]`-Kasten bei `--formats`: "Standard = IMMER alle drei Formate (1:1, 4:5, 9:16),
  Abweichung nur auf ausdruecklichen Wunsch"; (3) Primaer-Beispiel: `--formats` weggelassen →
  demonstriert den Default; (4) Abschnitt 15 (Vision-QA) Schritt 2 auf **1:1 UND 4:5 UND 9:16
  getrennt** geschaerft.
- **`batch.py` Docstring:** Job-Schema-Beispiel auf alle drei Formate + Hinweis "fehlt → alle 3".
- **Verworfen:** eine harte Sperre, die explizite 2-Format-Listen verbietet. Widerspraeche dem
  Warn-statt-Block-Muster des Skills und der Nutzer-Freiheit (EARS-6). Der Default + die klare
  SKILL.md-Pflicht loesen den Live-Fall vollstaendig, ohne den Renderer zu verengen.

## Test-Ergebnis / Beleg
- **Bestehende Suite gruen:** `python -m pytest -q` → **277 passed** (kein Test pinnt den exakten
  `DEFAULT_FORMATS`-Inhalt; die Erweiterung ist nicht-brechend).
- **Render-Beleg (TEMP, nicht v2-personal):** Ein Default-Lauf ohne `--formats` erzeugt jetzt
  **drei** PNGs — `*__square_1x1.png`, `*__feed_4x5.png`, `*__story_9x16.png` — statt zwei. 4:5
  ist mit 1080×1350 dabei.
- **Deploy:** `skills_sources/creative-studio/` → `~/.claude/skills/creative-studio/` (robocopy
  /MIR); `DEFAULT_FORMATS`-Zeile in der deployten Kopie enthaelt `feed_4x5`.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — `DEFAULT_FORMATS` (alle 3).
- `skills_sources/creative-studio/creative_studio/render_image.py` — `--formats`-Default liest
  `DEFAULT_FORMATS` (unveraendert; profitiert automatisch).
- `skills_sources/creative-studio/creative_studio/batch.py` — `job.formats or DEFAULT_FORMATS`
  (unveraendert; Docstring-Beispiel aktualisiert).
- `skills_sources/creative-studio/SKILL.md` — Format-Katalog, `--formats`-Default + Pflicht-Kasten,
  Primaer-Beispiel, Abschnitt 15 (Vision-QA pro Format).

## Ergebnis / Notizen
**Status review (2026-07-09).** Root-Cause = zu kleines Default-Set (2 statt 3 Formate) + fehlende
SKILL.md-Pflicht, nicht ein fehlendes Format. `DEFAULT_FORMATS` auf alle drei erweitert, SKILL.md-
Pflicht "immer alle 3 (1:1, 4:5, 9:16)" verankert, Vision-QA pro Format geschaerft. Additiv/
rueckwaerts-kompatibel (explizite Format-Listen unveraendert). 277 Tests gruen. Deploy nach
`~/.claude/skills/creative-studio/` erfolgt.

**Offen / [J]:** Verify-Pass (frische Session) + Outcome-Review (>=14 Tage).
