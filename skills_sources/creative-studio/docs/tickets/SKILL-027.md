# SKILL-027: creative-studio — Voiceover-Layer (ElevenLabs-Voice-Clone + Untertitel ueber Remotion)

**Status:** spec
**Erstellt:** 2026-06-23
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** voiceover_ohne_re_architektur (Audio-Track + Untertitel ueber bestehende Compositions) + provider_key_via_env_multi_projekt
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_ki-avatare-voiceover.md` (§2 Voiceover-Optionen, §3 Disclosure-Pflicht, §4 Remotion-Integration, Fazit: groesster Hebel bei kleinstem Pipeline-Eingriff)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> Belastbarste Aussage der Avatar-/Voiceover-Recherche: fuer DACH-B2B-Trust schlaegt eine echte Person
> KI-Avatare deutlich. Der **groesste Hebel mit kleinstem Pipeline-Eingriff** ist ein ElevenLabs-Voice-Clone
> von Jakobs eigener Stimme ueber **bestehende** Remotion-Videos — kein Avatar-Rendering, keine Re-Architektur.
> Skript → ElevenLabs-API → MP3/WAV → Audio-Track in die Composition + Untertitel aus demselben Skript.

## Was soll erreicht werden? (Business-Ziel)
Ein optionaler Voiceover-Layer fuers Video-Modul: aus einem Skript erzeugt der Skill (via ElevenLabs-
Voice-Clone) einen Audio-Track und legt ihn samt Untertiteln ueber die **bestehende** Remotion-Composition
— ohne Umbau der Video-Architektur. Provider-Key kommt aus Env, multi-projekt nutzbar.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein Voiceover-Skript uebergeben wird, the system shall daraus via ElevenLabs-API
      einen Audio-Track (MP3/WAV) erzeugen und ihn in die bestehende Remotion-Composition einbetten —
      ohne deren Struktur zu veraendern.
- [ ] **EARS-2:** When ein Audio-Track erzeugt wurde, the system shall **Untertitel** aus demselben Skript
      ableiten und Safe-Zone-konform als Overlay einblenden (geteilte Safe-Zone-Logik aus `specs.py`).
- [ ] **EARS-3 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall den
      ElevenLabs-Provider-Key **aus Env** (`.env`/Umgebungsvariable) beziehen — kein Key im Skill-Code,
      kein projekt-spezifischer Wert.
- [ ] **EARS-4:** When kein Voiceover-Skript/-Key vorhanden ist, the system shall das Video weiterhin ohne
      Voiceover rendern (Layer ist **optional**, kein Bruch des bestehenden Pfads).
- [ ] **EARS-5:** When ein Voiceover synthetisch erzeugt wurde, the system shall die KI-Disclosure-Pflicht
      (SKILL-028) als Constraint setzen/weiterreichen (synthetische Stimme = Disclosure-pflichtig).

## Technische Hinweise
- Asset-Provider-Schritt **vor** dem Remotion-Render: `creative_studio/voiceover.py` (Skript → ElevenLabs →
  Audio-Datei). In der Composition per Audio-Track + `<Sequence>` einbinden; Untertitel-Overlay drueber.
- ElevenLabs-Modell `eleven_multilingual_v2` (DE gut). Key via Env, Consent dokumentiert (Jakobs Eigen-Stimme).
- **Kein Avatar-Rendering** in diesem Ticket (Avatar = separates, niedriger-priorisiertes Thema). Recherche-
  Empfehlung: Voiceover zuerst.
- Kopplung zu SKILL-028 (Disclosure-Gate) — synthetische Stimme triggert das „KI"-Label.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/voiceover.py` — **neu** (Skript → ElevenLabs → Audio-Track).
- `skills_sources/creative-studio/video/src/AdVideo.tsx` — Audio-Track + Untertitel-Overlay (bestehende Composition).
- `skills_sources/creative-studio/creative_studio/specs.py` — geteilte Safe-Zone-Werte fuer Untertitel.
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_ki-avatare-voiceover.md` (§2, §3, §4).

## Ergebnis / Notizen
_(wird beim Abschließen befüllt)_
