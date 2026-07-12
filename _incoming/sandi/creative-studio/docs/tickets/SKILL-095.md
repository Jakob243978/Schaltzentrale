# SKILL-095: creative-studio — Ton-Profile / Ansprache (Buyer vs Champion) als Katalog

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** XS (Katalog + getter + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** zwei_ton_profile + buyer_ergebnis_zuerst + champion_du_verbuendet +
du_sie_asymmetrie_dokumentiert + projektneutral + tests_gruen

## Kontext / Root-Cause
Das Playbook (§7) unterscheidet zwei Ansprachen: Buyer/Entscheider (DISC D/I, Ergebnis zuerst,
„Sie" im Kaltkontakt / verdientes Du, Status) vs. Champion/Mitarbeiter (verbuendetes „du",
Geheimwaffe, schnelle Wins). Wichtig: du/Sie-Risiko-Asymmetrie (ein „Sie" beleidigt nie),
und „kurz nur fuer den Einstieg, Beweis so lang wie noetig" (High-Ticket).

## Was soll erreicht werden?
Ein projektneutraler `TONE_PROFILES`-Katalog (buyer/champion) mit `get_tone_profile(key)`.
Struktur (audience/pronoun/lead_with/register/note), keine Projekt-Texte.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Katalog]:** `TONE_PROFILES` hat buyer + champion; `get_tone_profile()`
      liefert das Profil, unbekannt -> KeyError. *(Tests `test_two_profiles_present`, `test_get_tone_profile_unknown_raises`.)*
- [x] **EARS-2 [Must, Inhalt]:** Buyer fuehrt mit Ergebnis + dokumentiert die du/Sie-Asymmetrie;
      Champion ist „du"/verbuendet mit schnellen Wins. *(Tests `test_buyer_leads_with_result_and_sie_asymmetry`, `test_champion_is_du_verbuendet`.)*
- [x] **EARS-3 [Must, projektneutral]:** kein „Jakob"/Immo-Nomen in den Profilen.
      *(Test `test_profiles_projektneutral`.)*

## Loesungs-Skizze
- `creative_studio/frameworks.py`: `ToneProfile`, `TONE_PROFILES`, `get_tone_profile`.
- `tests/test_skill_095_tone_profiles.py`.

## Test-Ergebnis / Beleg
- `python -m pytest tests/ -q` -> **426 passed, 3 skipped**.

## Code-Referenzen
- `creative_studio/frameworks.py`
- `tests/test_skill_095_tone_profiles.py` (neu)
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§6/§7)
