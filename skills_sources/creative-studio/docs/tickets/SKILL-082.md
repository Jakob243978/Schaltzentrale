# SKILL-082: creative-studio — Copy-Framework `opportunity` / neuer Mechanismus (Baulig #3)

**Status:** review
**Erstellt:** 2026-07-11
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (neuer CopyFramework-Eintrag + Template + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** opportunity_als_framework_verfuegbar + alt_weg_neu_weg_arc_vollstaendig (4 Slots) +
klar_abgegrenzt_von_bab (eigener Eintrag, nicht BAB-Alias) + kein_bestandsbruch

## Kontext / Root-Cause
Baulig-Methode #3 (`docs/ad-frameworks/baulig-methoden.md`) ist das **Opportunity-Template**: eine
**neue Gelegenheit / neuer Mechanismus** ("Shiny Object"), der alte Weg mit Nachteilen, der neue Weg
mit Vorteilen, CTA. Das ist **nicht** dasselbe wie `bab` (Before/After/Bridge): BAB kontrastiert
Ist-/Wunsch-**Zustand**, Opportunity kontrastiert **Loesungswege/Mechanismen** und rahmt das Angebot
als grundsaetzlich Neues. Dieses Angle fehlt im Katalog.

## Was soll erreicht werden?
Ein `CopyFramework` `opportunity`, das den "neuer-Mechanismus-statt-Verbesserung"-Arc kodiert —
klar abgegrenzt von `bab`, mit awareness-Einordnung fuer solution_aware/product_aware.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Katalog]:** `frameworks.FRAMEWORKS["opportunity"]` mit
      `slots=("new_opportunity","old_way_downsides","new_way_upsides","cta")`, Template nutzt genau
      diese Slots, `awareness` enthaelt `solution_aware`/`product_aware`.
- [x] **EARS-2 [Must, Abgrenzung]:** `note` grenzt explizit gegen `bab` ab (Mechanismus/Weg vs.
      Zustand) und gegen unbelegte "einzigartig am Markt"-Claims (Verweis `SUPERLATIVE_UNPROVEN`).
- [x] **EARS-3 [Should, Auswahl]:** `recommend_framework` kann `opportunity` fuer einen
      "neuer Ansatz"-Hint anbieten, ohne die bestehende `solution_aware -> fab/bab`-Default-Regel
      zu brechen (nicht-brechend; additiver optionaler Parameter).
- [x] **EARS-4 [Must, multi-projekt + nicht-brechend]:** kein Projektwert; bestehende
      `frameworks`-Tests gruen.

## Umsetzungshinweise (Recherche 2026-07-11)
- Todd Brown / Rich Schefren: ein Angebot **nie als inkrementelle Verbesserung** positionieren,
  sondern als **etwas grundsaetzlich Neues** ("marketplace of one"). Schwache = "more of the same" →
  **mental opt-out**. Genau das leistet der `new_opportunity`-Slot. `note` sollte das aufgreifen:
  Opportunity nur nutzen, wenn der Mechanismus **wirklich** neu/anders ist (Folie: *"Sollte jeder
  hier haben, weil ihr sonst nicht relevant waert"*).
- Template-Bausteine aus der Folie: *"Wusstest du, dass es einen vollkommen neuen Weg gibt, um …" /
  "Du kennst bestimmt den alten Weg: …" / "Wir setzen mittlerweile auf …" / "Wenn du herausfinden
  willst, ob diese Methode auch fuer dich funktionieren kann, dann …"*.
- Visuell stark als `split-compare`-Layout (alter Weg | neuer Weg) — Cross-Referenz zu
  `specs.LAYOUTS["split-compare"]`.

## Loesungs-Skizze
- `creative_studio/frameworks.py`: `FRAMEWORKS["opportunity"]` additiv; optional `angle`-Hint in
  `recommend_framework`.
- `tests/`: Existenz + Slot/Template-Konsistenz + Abgrenzungs-Note vorhanden.
- Doku: SKILL.md + Verweis Layout `split-compare` als bevorzugtes Bild-Rendering.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/frameworks.py`
- `skills_sources/creative-studio/creative_studio/specs.py` (`LAYOUTS["split-compare"]`, `SUPERLATIVE_UNPROVEN`)
- `skills_sources/creative-studio/docs/ad-frameworks/baulig-methoden.md` (Methode #3)
