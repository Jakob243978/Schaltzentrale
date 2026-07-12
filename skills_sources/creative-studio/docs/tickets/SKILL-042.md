# SKILL-042: creative-studio — Testimonial-/Before-After-/Talking-Head-ContentTypes mit Compliance-Kopplung

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Could
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_social-content-types.md` (§2.5/§2.10/§2.11 Talking-Head/Testimonial/Before-After, §3.2 Katalog, §3.2 Compliance-Kopplung, §5 MoSCoW Should/Could)

> [!info] Herkunft (Recherche 2026-06-24)
> Erweitert den `CONTENT_TYPES`-Katalog (SKILL-039) um die beweis-/personenbezogenen Typen:
> `talking_head`, `testimonial`, `testimonial_video`, `before_after`, plus die ergaenzenden `voiceover_broll`,
> `ugc_style`, `story_ad`. Diese Typen tragen ein **Compliance-Risiko** (UWG/HWG, Vorher-Nachher-Falle) und
> eine **Beleg-Pflicht** (Testimonial braucht echten Kunden — kein Fake). Das Ticket koppelt sie an die
> bestehenden Guards `compliance_warnings()` (SKILL-026) + `requires_ai_disclosure()` (SKILL-028).

## Was soll erreicht werden? (Business-Ziel)
Die restlichen Content-Typen aus dem Katalog ergaenzen und beim Bauen automatisch die passenden Guards
ausloesen: `before_after`/`testimonial` rufen `compliance_warnings()` (UWG/HWG, `BEFORE_AFTER_TRIGGERS`)
mit Beleg-Pflicht-Hinweis; `talking_head`/`voiceover_broll`/`testimonial_video` mit synthetischer Stimme
reichen die KI-Disclosure-Pflicht (SKILL-028) weiter. Reine Warnungen, keine Sperre.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When `CONTENT_TYPES` geladen wird, the system shall zusaetzlich `talking_head`,
      `testimonial`, `testimonial_video`, `before_after`, `voiceover_broll`, `ugc_style`, `story_ad` mit den
      Werten aus §3.2 enthalten (gueltige `FORMATS`-/`FRAMEWORKS`-Keys). → Test `test_extended_content_types_present`.
- [ ] **EARS-2:** When ein `before_after`- oder `testimonial`-Content geprueft wird, the system shall die
      `compliance_warnings()`-Heuristik (SKILL-026, inkl. `BEFORE_AFTER_TRIGGERS`) ausloesen, sobald ein
      Claim-Trigger im Text steht — mit Rechtsgrundlage im Warntext. → Tests `test_before_after_triggers_compliance`,
      `test_testimonial_triggers_compliance`.
- [ ] **EARS-3:** When ein `testimonial`/`testimonial_video` gebaut wird, the system shall einen
      **Beleg-Pflicht-Hinweis** ausgeben (echte Referenz noetig, kein Fake) — als Warnung. → Test `test_testimonial_beleg_hint`.
- [ ] **EARS-4:** When ein `talking_head`/`voiceover_broll`/`testimonial_video` mit synthetischer Stimme
      (`ai_voice`) gebaut wird, the system shall die KI-Disclosure-Pflicht (SKILL-028) weiterreichen.
      → Test `test_synthetic_voice_triggers_disclosure`.
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall die
      Typen projektneutral halten (keine Brand-/Projekt-Claims im Katalog). → Test `test_extended_types_project_neutral`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Katalog-Erweiterung in `specs.py` + eine duenne Kopplungs-Funktion, die anhand
  `ContentType.key` die passenden bestehenden Guards (`compliance_warnings`, `requires_ai_disclosure`)
  aufruft und ihre Warnungen sammelt. **Keine** neue Compliance-Logik — nur Verdrahtung der vorhandenen.
- **Verworfene Alternative:** Eigene Trigger-Sets pro Content-Typ — verworfen (Doppel zu SKILL-026).
- **Betroffene Module:** `specs.py` (Katalog + Kopplung), neue Testdatei.

## Technische Hinweise
- Beleg-Pflicht ist ein **Hinweis-String**, kein Datencheck (der Skill kennt keine echten Referenzen).
- `ugc_style` traegt den B2B-Premium-Caveat als `note` (nur dosiert, kein Marken-Default — §2.8).
- Voraussetzung: SKILL-039 (Katalog-Basis), nutzt SKILL-026 + SKILL-028 read-only.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — Katalog-Erweiterung + Guard-Kopplung (Block `# SKILL-042`).
- `skills_sources/creative-studio/tests/test_skill_042_content_types_compliance.py` (neu).
- Wissensgrundlage: `2026-06-24_social-content-types.md` (§2.5/§2.8/§2.10/§2.11, §3.2, §5).

## Ergebnis / Notizen

**Umgesetzt 2026-06-24 (Status -> review, Verify-Gate offen).**

In `creative_studio/specs.py` ergaenzt:
- Katalog-Erweiterung (im `CONTENT_TYPES`-Dict, SKILL-039-Block): `talking_head`,
  `testimonial`, `testimonial_video`, `before_after`, `voiceover_broll`, `ugc_style`,
  `story_ad` mit Werten aus §3.2. `ugc_style` traegt den B2B-Premium-Caveat als `note`.
- Deklarative Compliance-Kopplung ueber zwei `ContentType`-Flags
  (`requires_compliance_check`, `requires_proof`).
- Kopplungs-Funktion (Block `# === SKILL-042 ===`):
  `content_type_compliance_warnings(ct, text="", *, ai_voice=False) -> list[str]`.
  Verdrahtet NUR vorhandene Guards: `compliance_warnings()` (SKILL-026, inkl.
  `BEFORE_AFTER_TRIGGERS`), Beleg-Pflicht-Hinweis (kein Datencheck — Hinweis-String),
  KI-Disclosure-Pflicht (SKILL-028) bei `ai_voice` + Video-Medium. Keine neue
  Compliance-Logik.

Tests: `tests/test_skill_039_content_types.py` (Abschnitt SKILL-042).

Done-Kriterien (EARS):
- [x] EARS-1: erweiterte Typen mit gueltigen Keys -> `test_extended_content_types_present`.
- [x] EARS-2: `before_after`/`testimonial` triggern `compliance_warnings()` ->
      `test_before_after_triggers_compliance`, `test_testimonial_triggers_compliance`.
- [x] EARS-3: Beleg-Pflicht-Hinweis -> `test_testimonial_beleg_hint`.
- [x] EARS-4: synthetische Stimme -> KI-Disclosure-Pflicht -> `test_synthetic_voice_triggers_disclosure`
      (inkl. Negativ-Fall Bild-Medium).
- [x] EARS-5: projektneutral -> `test_extended_types_project_neutral`.

pytest gesamt: **158 passed**.
