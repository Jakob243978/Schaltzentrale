# SKILL-104: creative-studio — Konkretheits-Gate + Top-Ad-Rubrik (Top-Quote je Lauf steigern)

**Status:** spec
**Erstellt:** 2026-07-12
**MoSCoW:** Must
**Geschaetzter Aufwand:** M (Copy-Vorpruef-Warnungen + Rubrik-Doku; optional Self-Score-Schritt)
**surface:** code + docs
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** hoehere_passed_quote_je_review + weniger_abstrakte_ads_durchgerutscht

## Kontext / Root-Cause
Review-Runde 1 des Agentic-Messaging-Tests (26 Ads): **11 Top, 8 abgelehnt**. Gap-Analyse
(`AgentischesArbeiten/marketing/ad-creatives/messaging-test-2026-07/GAP-ANALYSE.md`):
**Top-Ads ZEIGEN eine konkrete Alltags-/Wunsch-Szene** (Uhrzeit/Ort/Gegenstand/Handgriff), **abgelehnte
Ads BEHAUPTEN einen abstrakten Nutzen** oder sind unklar/generisch. Verstaerker: text-forward Ads
(ohne Foto) fallen bei Abstraktheit besonders haeufig; reine Zahlen-Heroes ohne Szene sind unklar.
Das Playbook (§1) sagt „Szene statt These" bereits, aber es wird **nicht erzwungen/geprueft** — deshalb
rutschen abstrakte Entwuerfe durch.

## Was soll erreicht werden?
Der Skill draengt Copy aktiv zur **Konkretheit** und macht Abstraktheit vor dem Rendern sichtbar,
sodass die **Top-Quote je Lauf steigt**. Alles projektneutral (die konkreten Beispiele/VoC bleiben Doku).

## Akzeptanzkriterien (EARS)
- [ ] **EARS-1 [Must, Konkretheits-Gate]:** Copy-Vorpruefung (`content.content_structure_warnings()`
      bzw. `AdContent.warnings()`) warnt, wenn Headline/Hook **kein konkretes Anker-Element** enthaelt
      (Uhrzeit · Ort · Gegenstand · Handgriff · Person-in-Situation) — Heuristik/Regex + Signalwortliste.
      Warnung, keine Sperre (Mensch-im-Loop).
- [ ] **EARS-2 [Must, Abstraktions-/Floskel-Ban-Liste]:** Warnung bei generischen Fuellern
      („grosse Sachen", „Dinge", „stumpfer Kram", „es arbeitet fuer dich", „mehr Business/Abschluesse"
      ohne konkretes Bild) und Buzz („Branchen-Magie"). Liste projektneutral erweiterbar.
- [ ] **EARS-3 [Should, Top-Ad-Rubrik]:** Eine dokumentierte 5-Punkte-Rubrik (Szene sichtbar? ·
      spezifische Nomen? · in 2 Sek verstaendlich? · Wunsch/Emotion greifbar? · klarer Nutzen-/
      Einwand-Bezug?) als Self-Score-Schritt vor „ready to test" (nur >= 4).
- [ ] **EARS-4 [Should, Text-forward-Regel]:** Fuer text-forward Layouts (template/stat-hero ohne Foto)
      gilt die Szene-Pflicht verschaerft; reine Zahlen-Heroes nur mit sofort klarer Bedeutung.
- [ ] **EARS-5 [Should, Feedback-Loop]:** Die `reviewState`-JSONs (passed/declined) werden als
      Referenz-Beispiele in eine Skill-Doc gefuehrt (gut/floppt), die der Copy-Schritt liest.
- [ ] **EARS-6 [Must, projektneutral]:** Kein Projektwert in `creative_studio/*` hartkodiert; Signalwort-
      /Ban-Listen als Daten/Doku, Rubrik generisch.

## Loesungs-Skizze
- Playbook §1 um den **Konkretheits-Check + Rubrik** ergaenzen; SKILL.md Abschnitt 9 verweist darauf.
- Code: `content`-Warnungen um Konkretheits-Heuristik + Ban-Liste erweitern (analog `dash_warnings()`).
- Referenz-Beispiele (passed vs declined) aus der Gap-Analyse als Doku unter `docs/ad-frameworks/`.

## Test-Ergebnis / Beleg
- Offen (spec). Abnahme: an einem neuen Lauf sinkt die Abstrakt-Durchrutsch-Quote; hoehere passed-Rate.
- Beleg-Fall: Gap-Analyse Runde 1 (`messaging-test-2026-07/GAP-ANALYSE.md`).

## Code-Referenzen
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§1)
- `creative_studio/content.py` (`content_structure_warnings`), `creative_studio/specs.py` (Warn-Funktionen)
- Gap-Analyse: `AgentischesArbeiten/marketing/ad-creatives/messaging-test-2026-07/GAP-ANALYSE.md`
