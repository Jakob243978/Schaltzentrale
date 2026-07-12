# SKILL-083: creative-studio — Copy-Framework `avatar_story` (Baulig #4, Kunden-Story)

**Status:** review
**Erstellt:** 2026-07-11
**MoSCoW:** Should
**Geschaetzter Aufwand:** M (CopyFramework + Selbst-Selektions-Hook + Proof-Kopplung + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** avatar_story_als_framework_verfuegbar + self_selection_opener_erzwungen +
proof_pflicht_verdrahtet (requires_proof greift) + kein_bestandsbruch

## Kontext / Root-Cause
Baulig-Methode #4 (`docs/ad-frameworks/baulig-methoden.md`) ist das **Avatar-Ansprache-Template**:
Selbst-Selektions-Hook ("Bist du ein XYZ?") → aktuelle Probleme → gespiegelte Kunden-Erfahrung →
entdeckte Loesung → neue Resultate → CTA. *"So laesst sich JEDER erfolgreiche Kunde als
Werbeanzeige inszenieren. 10+ Ads. Testimonials funktionieren immer."*
**Teilweise abgedeckt:** Es gibt den **ContentType** `testimonial`/`testimonial_video`
(`specs.py`, mit `requires_proof`) — das ist die *Medien-Bauart*. Es fehlt das zugehoerige
**Copy-Framework** (der Argumentations-Arc) und der **Selbst-Selektions-Hook** als wiederverwendbares
Muster. ContentType (Bauart) und CopyFramework (Copy-Arc) sind zwei getrennte Ebenen — hier fehlt die
Copy-Ebene.

## Was soll erreicht werden?
Ein `CopyFramework` `avatar_story` (Kunden-Story-Arc) + ein `HookPattern` fuer den
Selbst-Selektions-Opener, plus Verdrahtung der **Beleg-Pflicht** (echte Referenz, kein Fake) ueber
den bestehenden `requires_proof`-Guard.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Katalog]:** `frameworks.FRAMEWORKS["avatar_story"]` mit
      `slots=("self_select","current_problems","mirrored_customer","discovered_solution","new_results","cta")`,
      Template nutzt genau diese Slots, `awareness` enthaelt `problem_aware`/`solution_aware`.
- [x] **EARS-2 [Should, Hook]:** ein `HookPattern` fuer den Selbst-Selektions-Opener
      ("Bist du ein {zielgruppe}?") — entweder neuer Key `self_select` oder dokumentierte
      Wiederverwendung von `HOOKS["niche_question"]` (Entscheidung im Ticket begruenden).
- [x] **EARS-3 [Must, Proof-Kopplung]:** `note` verweist auf die **Beleg-Pflicht** (echte,
      nachweisbare Referenz — kein erfundenes Testimonial), konsistent mit
      `content_type_compliance_warnings()` (`requires_proof`) fuer `testimonial*`. Der Renderer/Agent
      soll bei `avatar_story` denselben Proof-Hinweis erhalten wie beim `testimonial`-ContentType.
- [x] **EARS-4 [Must, Trennung der Ebenen]:** dokumentierte Abgrenzung Framework (Copy) vs.
      ContentType (`testimonial`, Medien-Bauart) — kein Duplizieren der ContentType-Logik.
- [x] **EARS-5 [Must, multi-projekt + nicht-brechend]:** kein Projektwert; bestehende Tests gruen.

## Umsetzungshinweise (Recherche 2026-07-11)
- Testimonial-Ads = staerkster Social Proof (bis +34 % CVR laut Bestand `testimonial`-Note).
  Best Practice 2026: modular testen — **Hook tauschen, Body (Story) + CTA konstant halten**;
  lange Testimonials in 6-Sekunden-Reels mit verschiedenen Openern schneiden. Der
  Selbst-Selektions-Hook ("Bist du ein X?") ist genau dieser tauschbare Hook-Layer.
- O-Ton-Opener ("Ich war skeptisch — dann …") laesst den Zuschauer sich mit dem Kunden
  identifizieren → passt in `mirrored_customer`.
- Template-Bausteine aus der Folie: *"Bist du ein …?" / "Dann kennst du bestimmt folgende
  Situationen: …" / "Genau so ging es unserem Kunden …" / "Wir konnten seine Probleme loesen,
  indem wir …" / "Seitdem hat er …, … und … erreicht!" / "Wenn du herausfinden willst, ob …, dann
  klicke jetzt hier, um …"*.
- Rendert als `testimonial`/`testimonial_video`-ContentType bzw. `broll_message`-Reel (Hook =
  Selbst-Selektion, Message = gespiegelte Kunden-Story).

## Loesungs-Skizze
- `creative_studio/frameworks.py`: `FRAMEWORKS["avatar_story"]` + ggf. `HOOKS["self_select"]`.
- Kopplung: bei Verwendung von `avatar_story` denselben `requires_proof`-Hinweis ausgeben wie
  `content_type_compliance_warnings()` (kein Doppel — vorhandenen Guard referenzieren).
- `tests/`: Existenz + Slots/Template + Proof-Hinweis-Verdrahtung.
- Doku: SKILL.md + `docs/ad-frameworks/baulig-methoden.md` (Methode #4).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/frameworks.py`
- `skills_sources/creative-studio/creative_studio/specs.py` (`CONTENT_TYPES["testimonial"]`, `content_type_compliance_warnings`)
- `skills_sources/creative-studio/docs/ad-frameworks/baulig-methoden.md` (Methode #4)
