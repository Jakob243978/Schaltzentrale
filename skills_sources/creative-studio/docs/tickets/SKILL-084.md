# SKILL-084: creative-studio — Copy-Framework `heros_journey` (Baulig #5, Gruender-Story)

**Status:** review
**Erstellt:** 2026-07-11
**MoSCoW:** Should
**Geschaetzter Aufwand:** M (CopyFramework mit langem Arc + Reel-Mapping-Hinweis + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** heros_journey_als_framework_verfuegbar + 8_stufen_arc_vollstaendig +
klar_abgegrenzt_von_hso_pastor + kein_bestandsbruch

## Kontext / Root-Cause
Baulig-Methode #5 (`docs/ad-frameworks/baulig-methoden.md`) ist das **Hero's-Journey-Template**:
persoenliche Gruender-/Transformations-Story ueber 8 Stufen (frueher → Probleme → nichts
funktionierte → kurz vor Aufgeben → zufaellige Entdeckung → neue Welt → heute gebe ich es weiter →
CTA). *"Sinnvoll, wenn du selbst mal Teil deiner Zielgruppe warst."*
**Teilweise abgedeckt:** `hso` (Hook·Story·Offer) und `pastor` (mit `story`-Slot) sind story-nah,
aber **keiner** kodiert den vollstaendigen, wiederholbaren Hero's-Journey-Arc mit dem
"near-giving-up → discovery"-Wendepunkt. Dieser lange narrative Arc fehlt als eigenes Geruest.

## Was soll erreicht werden?
Ein `CopyFramework` `heros_journey`, das den 8-Stufen-Gruender-Story-Arc als projektneutrales
Geruest kodiert — abgegrenzt von `hso`/`pastor`, mit Video/Reel-Eignungshinweis.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Katalog]:** `frameworks.FRAMEWORKS["heros_journey"]` mit
      `slots=("past_self","problems","nothing_worked","near_giving_up","discovery","new_world","pay_it_forward","cta")`,
      Template nutzt genau diese Slots, `awareness` enthaelt `product_aware`/`most_aware`.
- [x] **EARS-2 [Must, Abgrenzung]:** `note` grenzt gegen `hso`/`pastor` ab (voller Monomyth-Arc mit
      Wendepunkt vs. kompaktes Hook·Story·Offer) und nennt die Anwendungs-Bedingung
      ("nur, wenn der Absender selbst Teil der Zielgruppe war").
- [x] **EARS-3 [Should, Medien-Eignung]:** dokumentierter Hinweis, dass `heros_journey` primaer als
      **Video/Reel** taugt (`talking_head`/`broll_message`), da langer narrativer Arc — Cross-Ref zu
      `CONTENT_TYPES["talking_head"]` und dem `broll_message`-Reel-Format (SKILL-078).
- [x] **EARS-4 [Must, DACH]:** `note` warnt, dass die Transformation belegbar/ehrlich bleiben muss
      (`BEFORE_AFTER_TRIGGERS`/`compliance_warnings` — keine ueberzogene Vorher-Nachher-Story).
- [x] **EARS-5 [Must, multi-projekt + nicht-brechend]:** kein Projektwert; bestehende Tests gruen.

## Umsetzungshinweise (Recherche 2026-07-11)
- Hero's Journey (Campbell/Monomyth) in Ads: **der Kunde ist der Held, die Marke der Mentor** — bei
  der Gruender-Story ist der Gruender der Mentor, der die Zielgruppe durch dieselbe Transformation
  fuehrt, die er selbst durchlebt hat. `pay_it_forward`-Slot ("Heute gebe ich meine Erfahrung
  weiter") macht genau diesen Mentor-Uebergang.
- Auch ein 15-30-s-Reel kann einen **komprimierten** Hero-Arc tragen (Challenge → Marke/Loesung →
  Transformation). Meta-Video-Regeln: Hook in den ersten 3 s, Captions Pflicht (85 % sound-off),
  klarer Anfang/Mitte/Ende — passt in den Bestand (`hook_window_seconds=3.0`, Caption-Pipeline).
- Template-Bausteine aus der Folie: *"Als Selbststaendiger ging es mir frueher so: …" / "– Probleme,
  – Probleme, – Probleme …" / "Ich habe A, B und C probiert, aber nichts hat funktioniert …" / "Ich
  wollte schon aufgeben und wieder …" / "Doch dann stiess ich eines Tages auf …" / "Dadurch war es
  mir ploetzlich moeglich, dass …" / "Heute helfe ich anderen dabei, auch …" / "Wenn du herausfinden
  willst, ob … dann …"*.

## Loesungs-Skizze
- `creative_studio/frameworks.py`: `FRAMEWORKS["heros_journey"]` additiv (langer Slot-Satz).
- `tests/`: Existenz + Slots==Template-Marker + Abgrenzungs-Note vorhanden.
- Doku: SKILL.md + Cross-Ref auf `talking_head`/`broll_message` als bevorzugtes Rendering.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/frameworks.py`
- `skills_sources/creative-studio/creative_studio/specs.py` (`CONTENT_TYPES["talking_head"]`, `BEFORE_AFTER_TRIGGERS`)
- `skills_sources/creative-studio/video/src/BrollMessage.tsx` (SKILL-078, Reel-Rendering)
- `skills_sources/creative-studio/docs/ad-frameworks/baulig-methoden.md` (Methode #5)
