# SKILL-097: creative-studio — Voice-of-Customer als versioniert erweiterbares Datenformat

**Status:** spec
**Erstellt:** 2026-07-12
**MoSCoW:** Could
**Geschaetzter Aufwand:** M (Schema-Definition + Loader + Merge mehrerer Kunden + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** voc_als_versioniertes_datenformat + weitere_kunden_anfuegbar +
kundenuebergreifende_muster_maschinell_lesbar + projekt_voc_bleibt_daten_nicht_code

## Kontext / Root-Cause
Die Voice-of-Customer-Bibliothek (Playbook §6, Beyer + Weist) ist heute Fliesstext. SKILL-090
liest sie als opaken Text in den Prompt. Fuer echte Wiederverwendung (weitere Kunden anfuegen,
kundenuebergreifende Muster maschinell extrahieren, Vokabular gezielt in Copy-Slots ziehen)
braucht es ein **versioniertes, strukturiertes Datenformat** (Vokabular / Painpoints-O-Ton /
Testimonials / verbotene Abstrakta pro Kunde + aggregierte Muster).

## Was soll erreicht werden?
Ein projektneutrales VoC-Schema (z. B. YAML/JSON) mit Loader + Merge ueber mehrere Kunden,
das die Projekt-VoC als DATEN (nicht Code) versioniert und erweiterbar haelt. Das konkrete
Projekt-VoC (AgentischesArbeiten) bleibt Projekt-Daten/Doku; der Skill liefert nur Schema +
Loader.

## Akzeptanzkriterien (EARS)
- [ ] **EARS-1 [Must, Schema]:** ein dokumentiertes VoC-Schema (Kunde -> vocabulary/painpoints/
      testimonials/forbidden_abstracta + version) als projektneutrale Datenstruktur.
- [ ] **EARS-2 [Must, Loader/Merge]:** Loader liest 1..n Kunden-VoC-Dateien und aggregiert die
      kundenuebergreifenden Muster (Schnittmenge Vokabular/Painpoints).
- [ ] **EARS-3 [Must, projektneutral]:** kein Projekt-VoC im Code; Projekt-Daten kommen als Datei.
- [ ] **EARS-4 [Should, Anschluss]:** der Loader speist SKILL-090 (`build_analysis_prompt`) mit
      strukturierter Kundensprache statt opakem Text.

## Loesungs-Skizze (offen)
- Neues Modul `creative_studio/voc.py` (Schema-Dataclasses + Loader + Merge).
- Erweiterung von `content.load_messaging_doc` um strukturiertes Format.
- `tests/test_skill_097_voc_format.py`.

## Test-Ergebnis / Beleg
- Offen (Status spec). Done-Gate: `python -m pytest tests/ -q` gruen + Verify-Report.

## Code-Referenzen
- `creative_studio/voc.py` (neu, offen), `creative_studio/content.py`
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§6)
