# SKILL-099: creative-studio — Modell-Ads + humanisierte Vorher/Nachher-Beispiele als Referenzmaterial

**Status:** spec
**Erstellt:** 2026-07-12
**MoSCoW:** Could
**Geschaetzter Aufwand:** S (Referenz-Doku + Verlinkung; projekt-spezifisch, kein Code)
**surface:** docs
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** vier_modell_ads_als_referenz + humanisierte_vorher_nachher_beispiele +
projekt_spezifisch_als_beispiel_gekennzeichnet + nicht_hartkodiert_im_code

## Kontext / Root-Cause
Das Playbook (§8) benennt vier fertige menschliche Modell-Ads („Arbeit wegnehmen",
„23:14-Szene", „Ich bin kein IT-Mensch", „Kein zehntes Tool") plus humanisierte Vorher/Nachher-
Beispiele. Sie sind wertvolles Referenz-/Trainingsmaterial, aber projekt-spezifisch (Immo-VoC,
Jakobs Beweis) — sie duerfen NICHT in den projektneutralen Skill-Code wandern.

## Was soll erreicht werden?
Die Modell-Ads + Vorher/Nachher-Beispiele liegen als klar als AgentischesArbeiten-Instanz
gekennzeichnetes Referenzmaterial vor (Doku), verlinkt aus dem Playbook, nutzbar als Vorlage
beim Ad-Bauen — ohne Projektwerte in den Code zu ziehen (Prinzip skill-muss-multi-projekt-tauglich).

## Akzeptanzkriterien (EARS)
- [ ] **EARS-1 [Must, Modell-Ads]:** die 4 Modell-Ads voll ausgeschrieben (Langform + Kurzvarianten)
      als Referenz-Doku, den Hook-Formeln (F1-F6, SKILL-089) zugeordnet.
- [ ] **EARS-2 [Must, Vorher/Nachher]:** humanisierte Vorher/Nachher-Beispiele (KI-generisch ->
      menschlich) als Lern-Gegenueberstellung.
- [ ] **EARS-3 [Must, projektneutral getrennt]:** klar als Projekt-Instanz gekennzeichnet; kein
      Wert wandert in `frameworks.py`/`specs.py` (dort nur `best_for`/generische Muster).

## Loesungs-Skizze (offen)
- Referenz-Doku unter `docs/ad-frameworks/` bzw. Verweis auf
  `AgentischesArbeiten/brand/proposals/2026-07-12_human-test-ads.md`.
- Verlinkung aus dem Playbook (§8) + den Formel-`best_for`-Feldern.

## Test-Ergebnis / Beleg
- Offen (Status spec). Doku-Surface (keine pytest-Abnahme; `manual_verify_required: false`).

## Code-Referenzen
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§8)
- `frameworks.FRAMEWORKS["scene"|...]` (`best_for`-Verweise, projektneutral)
