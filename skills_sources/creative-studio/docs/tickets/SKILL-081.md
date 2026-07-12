# SKILL-081: creative-studio — Copy-Framework `mindset_shift` (Baulig #2)

**Status:** review
**Erstellt:** 2026-07-11
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (neuer CopyFramework-Eintrag + Template + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** mindset_shift_als_framework_verfuegbar (recommend/get_framework liefert es) +
belief_reframe_arc_vollstaendig (5 Slots) + kein_bestandsbruch (bestehende FRAMEWORKS-Suite gruen)

## Kontext / Root-Cause
Aus dem Baulig-Vortrag (Founder Summit 2025, `docs/ad-frameworks/baulig-methoden.md`, Methode #2)
stammt ein **Belief-Reframe-Framework**: einen falschen Glaubenssatz der Zielgruppe
identifizieren, drehen und in eine Zukunftsprojektion + CTA ueberfuehren. Der Skill kennt heute
`aida/pas/bab/fab/pastor/4p/hso` — **kein** Framework fuer das gezielte Zerpfluecken einer
falschen Ueberzeugung. Diese Ad-Sorte ("Du denkst X — die Wahrheit ist Y") ist ein eigenes,
haeufig skalierendes Angle und fehlt.

## Was soll erreicht werden?
Ein neues `CopyFramework` `mindset_shift` in `creative_studio/frameworks.py`, das den Baulig-Arc
als projektneutrales Geruest kodiert (Slots + Platzhalter-Template), plus Einordnung in die
awareness-gesteuerte Auswahl.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Katalog]:** `frameworks.FRAMEWORKS["mindset_shift"]` existiert mit
      `slots=("situation","false_belief","truth","future_projection","cta")`, `template` nutzt
      **genau** diese Slots als `{slot}`-Marker, `awareness` enthaelt `problem_aware`/`solution_aware`.
      *(Test: `get_framework("mindset_shift")`, Slot-/Template-Konsistenz wie die Bestands-Frameworks.)*
- [x] **EARS-2 [Should, Auswahl]:** `recommend_framework(...)` kann `mindset_shift` als Alternative
      fuer einen Einwand-/Belief-Blocker liefern (z.B. neuer optionaler Hint `angle="belief"`), ohne
      die bestehende Default-Zuordnung (`problem_aware -> pas`) zu veraendern (nicht-brechend).
- [x] **EARS-3 [Must, Note/DACH]:** `note` warnt sachlich, dass die "Wahrheit"-Aussage belegbar
      bleiben muss (kein manipulativer Fake-Reframe) — konsistent mit dem `compliance_warnings`-Geist.
- [x] **EARS-4 [Must, multi-projekt]:** kein Brand-/Projektwert im Eintrag (nur generische Slots).
- [x] **EARS-5 [Must, nicht-brechend]:** bestehende `frameworks`-Tests gruen; kein Eintrag geaendert,
      nur additiv ergaenzt.

## Umsetzungshinweise (Recherche 2026-07-11)
- Belief-Shift-Copy (Roy Furr "6-Step Belief-Shifting", "Belief Shift Method"): zuerst den
  **aktuellen** Glaubenssatz spiegeln, dann den **noetigen** Glaubenssatz aufbauen, BEVOR der Ask
  kommt ("changes minds before asking for the sale"). Reihenfolge Situation → falscher Glaube →
  Wahrheit deckt sich mit Baulig.
- Template-Bausteine 1:1 aus der Folie: *"Du denkst, dass …" / "Der Grund dafuer ist, dass du
  annimmst, dass …" / "Die Wahrheit ist aber, dass …" / "Sobald du …, wirst du …" / "Klicke jetzt
  hier, um …"*.
- Rendert als **static_statement** (Headline = gespiegelter Glaubenssatz) ODER als
  `talking_head`/`broll_message`-Reel (Hook = "Du denkst X", Message = "Die Wahrheit ist Y").

## Loesungs-Skizze
- `creative_studio/frameworks.py`: neuer `FRAMEWORKS["mindset_shift"]`-Eintrag; optional ein
  awareness-`angle`-Hint in `recommend_framework`.
- `tests/`: neuer Test analog der Bestands-Framework-Tests (Existenz, Slots==Template-Marker,
  projektneutral).
- Doku: SKILL.md (Framework-Katalog-Erwaehnung) + Verweis auf `docs/ad-frameworks/baulig-methoden.md`.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/frameworks.py`
- `skills_sources/creative-studio/docs/ad-frameworks/baulig-methoden.md` (Methode #2)
