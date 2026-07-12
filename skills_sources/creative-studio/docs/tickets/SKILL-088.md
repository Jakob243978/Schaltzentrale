# SKILL-088: creative-studio — Ad-Messaging-Playbook (Human-Rules + Hook-Formeln + Voice of Customer) als ad-framework

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Must
**Geschaetzter Aufwand:** M (Analyse 2 Kunden + Ad-Report + Konsolidierung in eine Doku)
**surface:** backend
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** eine_konsolidierte_messaging_ressource + 8_human_regeln_dokumentiert +
hook_formeln_F1_F6_anwendbar + voc_bibliothek_zwei_kunden_belegt + kundenuebergreifende_muster_extrahiert +
projektneutrale_regeln_getrennt_von_projekt_voc

## Kontext / Root-Cause
Die ersten Ad-Runs fuer das Projekt AgentischesArbeiten (Jakob Sebov) wirkten
KI-generisch/unmenschlich: die Copy **erklaerte eine Kategorie, statt eine Alltagsszene
zu zeigen**, und setzte den Fachbegriff „agentisches Arbeiten" bei einer KALTEN Zielgruppe
voraus, die ihn nicht kennt. Zwei Analyse-Subagenten (Ad-Critique gegen den echten
Meta-Ad-Report; Voice of Customer aus echten Kundengespraechen Beyer + Weist) lieferten
belegte Erkenntnisse. Diese lagen verstreut (Booklet-Post-its, Proposals) — es fehlte
**eine konkrete, nutzbare, nachvollziehbare Ressource** zum Hook-Bauen (User-Feedback:
„Flickenteppich, keine easy-to-use Option").

## Was soll erreicht werden?
Eine einzige, im Skill wiederverwendbare ad-framework-Doku, die alle Ad-Messaging-
Erkenntnisse konsolidiert und direkt anwendbar macht: Regeln + Hook-Bauplan + Formeln +
VoC-Bibliothek + Ad-Daten-Muster + Baukasten-Verweise + Modell-Ads. Reusable Regeln
(projektneutral) klar getrennt von der projekt-spezifischen VoC-Bibliothek.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Regeln]:** Doku enthaelt die **8 Human-Messaging-Regeln** fuer kalte
      Zielgruppen (Szene statt These … krumme echte Zahl) als Checkliste. *(§1)*
- [x] **EARS-2 [Must, Bauplan+Formeln]:** Ein 5-Schritte-Hook-Bauplan („Insight → Ad in 5 Min")
      plus mindestens 6 anwendbare Hook-Formeln (F1 Szene, F2 O-Ton, F3 Vorher/Nachher,
      F4 Einwand-als-O-Ton, F5 Anti-Hype, F6 Umbruch/Einladung). *(§3, §4)*
- [x] **EARS-3 [Must, VoC belegt]:** Voice-of-Customer-Bibliothek mit echtem Vokabular,
      Painpoints (O-Ton) und Testimonial-Zitaten fuer **zwei** reale Kunden (Beyer + Weist)
      und eine Sektion **bestaetigter kundenuebergreifender Muster**. *(§6a–6c)*
- [x] **EARS-4 [Must, Daten]:** Ad-Daten-Muster dokumentiert (konkret-menschlich gewinnt,
      abstrakt/Statistik verliert; Winner/Kill benannt, mit Signifikanz-Vorbehalt). *(§5)*
- [x] **EARS-5 [Must, Leitplanken]:** Brand-Leitplanken (du, keine Tool-Namen, kein Preis,
      Beweis nur „verdoppelt", keine Gedankenstriche) als verbindlicher Block. *(§2)*
- [x] **EARS-6 [Should, Projektneutralitaet]:** Reusable Regeln/Formeln sind projektneutral
      formuliert; projekt-spezifische Inhalte (VoC, Jakobs Beweis, Farbwelt) sind als
      AgentischesArbeiten-Instanz gekennzeichnet und erweiterbar. *(Kopf + §6/§9)*

## Loesungs-Skizze
- Neue Datei `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (Companion zu
  `baulig-methoden.md`).
- Quellen: Meta-Ad-Report `AgentischesArbeiten/marketing/ad-creatives/ad-report-rohdaten_2026-07-12.md`;
  VoC-Transkripte `AgentischesArbeiten/brand/Jakobs Files/Kundenworkshops - Sprache/{Beyer,Weist}/`;
  Baukasten `AgentischesArbeiten/brand/proposals/2026-07-12_ad-messaging-baukasten.md`.

## Test-Ergebnis / Beleg
- Doku-Artefakt (kein Code) → Verifikation = Vollstaendigkeits-Review gegen EARS-1..6
  (Doku-Surface; keine pytest-Abnahme noetig, `manual_verify_required: false`).
- Folge-Ticket **SKILL-089** encodiert die Formeln/Regeln testbar in `frameworks.py`.

## Code-Referenzen
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (neu)
- `docs/ad-frameworks/baulig-methoden.md` (Companion)
