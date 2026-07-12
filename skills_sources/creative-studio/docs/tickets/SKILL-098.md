# SKILL-098: creative-studio — Visual-Anti-KI-Klischee-Check (Image-Prompt-Leitplanke)

**Status:** review
**Erstellt:** 2026-07-12
**MoSCoW:** Should
**Geschaetzter Aufwand:** XS (Klischee-Katalog + Warn-Funktion + Tests)
**surface:** backend
**vision_principle:** skill-muss-multi-projekt-tauglich
**outcome_metric:** ki_klischee_im_motiv_prompt_wird_gewarnt + projektneutral +
warme_palette_bleibt_projekt_doku + tests_gruen

## Kontext / Root-Cause
Die Visual-Leitplanken (Playbook §10) fordern Anti-KI-Klischee: kein Glow/Neuronen/Roboter/
Violett-Gradient/Sparkle; stattdessen warme Palette, humanist Typo, Founder-Face/Handy-Look,
Delegation/Ordnung statt Roboter. Der creative-studio-Bildpfad kannte diese Leitplanke nicht.
Die warme Marken-Palette (Coral/Navy/Cream ...) ist projekt-spezifisch und bleibt Doku/Parameter;
der Anti-Klischee-Check ist projektneutral.

## Was soll erreicht werden?
Eine projektneutrale `visual_cliche_warnings(prompt)`-Funktion warnt, wenn ein Bild-/Motiv-Prompt
KI-Klischee-Begriffe enthaelt, und empfiehlt den menschlichen Founder-/Delegation-Look.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Warn]:** `visual_cliche_warnings()` warnt bei Klischee-Begriffen
      (Glow/Neuronen/Roboter/Sparkle/Hologramm ...). *(Tests `test_flags_ai_cliche_terms`, `test_flags_sparkle`.)*
- [x] **EARS-2 [Must, sauber/leer]:** ein menschlicher Founder-Prompt und leerer/None-Prompt
      erzeugen keine Warnung. *(Tests `test_clean_prompt_no_warning`, `test_empty_prompt_no_warning`.)*
- [x] **EARS-3 [Must, projektneutral]:** `AI_CLICHE_TERMS` generisch; die warme Marken-Palette
      bleibt Projekt-Doku (nicht hartkodiert im Check). *(Test `test_cliche_terms_projektneutral`.)*

## Loesungs-Skizze
- `creative_studio/specs.py`: `AI_CLICHE_TERMS`, `visual_cliche_warnings()`.
- `tests/test_skill_098_visual_cliche.py`.
- Offen als Folge (optional): Einhaengung in den `--bg-source generate`-Prompt-Pfad (render_image).

## Test-Ergebnis / Beleg
- `python -m pytest tests/ -q` -> **426 passed, 3 skipped**.

## Code-Referenzen
- `creative_studio/specs.py`
- `tests/test_skill_098_visual_cliche.py` (neu)
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§10)
