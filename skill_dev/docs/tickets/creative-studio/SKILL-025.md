# SKILL-025: creative-studio — frameworks.py (Copy-Framework-Katalog + Hook-Bibliothek + Validatoren)

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** strukturierte_copy_varianten_statt_freitext (Generator zieht Frameworks/Hooks aus Katalog) + frameworks_py_als_copy_pendant_zu_specs_py (Single Source, projektneutral)
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_ad-copywriting-frameworks.md` (§1 Frameworks AIDA/PAS/BAB/FAB/PASTOR/4P/4U/HSO, §3 Conversion-Best-Practices, §4 Umsetzung als `frameworks.py`); `2026-06-23_creative-studio-flow-improvements.md` (§2.1/§3.2; MoSCoW-Liste #3 = Should)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> Analog zu `specs.py` (Single Source fuer Meta-Format-Standards) braucht der Skill eine
> **medien-unabhaengige, projektneutrale Standards-Klasse fuer Copy**: Strukturen + Platzhalter +
> Validatoren, aus denen der Generator (oder ein vorgelagerter Agent) Copy baut — statt Freitext.
> Sie liefert KEINEN fertigen kreativen Text (bleibt LLM-/Mensch-Aufgabe), sondern das Geruest.

## Was soll erreicht werden? (Business-Ziel)
Eine neue `frameworks.py` als **Copy-Pendant zu `specs.py`**: ein Katalog bewaehrter Copy-Frameworks mit
Slots/Awareness-Tags/`best_for`/Platzhaltern, eine Hook-Bibliothek mit Scroll-Stopper-Mustern, eine
Awareness-gesteuerte Framework-Auswahl und ein 4U-Headline-Validator (Warn-Funktion). Projektneutral —
Brand/Inhalt kommen zur Laufzeit rein.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When der Skill Copy-Struktur braucht, the system shall einen `CopyFramework`-Katalog
      (mind. AIDA, PAS, BAB, FAB, PASTOR, 4P, Hook-Story-Offer) mit `key`, `slots`, `awareness`, `best_for`
      und Platzhalter-`template` bereitstellen — projektneutral, ohne Brand-/Projektwerte.
- [x] **EARS-2:** When Hooks generiert werden, the system shall eine **Hook-Bibliothek** mit **≥ 6** belegten
      Mustern (z. B. give-me-X, spezifische Zahl, Nischen-Frage, Pattern-Interrupt, Before/After-Bild,
      Reibungs-Statement) liefern, jedes mit der Regel **`max_words_onscreen ≤ 7`**.
- [x] **EARS-3:** When ein Awareness-Level + Placement gegeben sind, the system shall via
      `recommend_framework(awareness, placement)` das passende Framework nach der Kurzregel empfehlen
      (cold→AIDA, problem_aware→PAS, vergleichend→FAB/BAB, warm/video→HSO).
- [x] **EARS-4:** When eine Headline geprueft wird, the system shall einen **4U-Validator**
      (useful/urgent/unique/ultra_specific) liefern, der **Warnungen/Hinweise** ausgibt — keine harte Sperre
      (analog `AdContent.warnings()`).
- [x] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall
      `frameworks.py` als Single Source fuer Copy-Standards halten (keine projekt-spezifische Tonalitaet/Claim
      hartkodiert — projektspezifisches bleibt Overlay/Parameter).

## Technische Hinweise
- Neue Datei `creative_studio/frameworks.py`. Skizze in der Recherche §4.1 (CopyFramework, HookPattern,
  `score_4u`, `recommend_framework`). Frozen dataclasses, rein-funktional.
- DACH-Compliance-Guard (UWG/HWG-Trigger, `landing_promise`) ist **SKILL-026** — hier nur Referenz, nicht
  Doppel-Implementierung. `frameworks.py` darf `compliance_warnings(...)` aus dem Guard re-exportieren.
- Abgrenzung: `frameworks.py` erzeugt **Struktur + Validierung**, nicht den finalen Text.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/frameworks.py` — **neu** (CopyFramework-Katalog,
  HookPattern-Bibliothek, `recommend_framework`, `score_4u`).
- `skills_sources/creative-studio/creative_studio/specs.py` — Vorbild-Pattern (Standards-als-Code).
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_ad-copywriting-frameworks.md` (§1/§3/§4),
  `…/2026-06-23_creative-studio-flow-improvements.md` (§2.1, §3.2).

## Ergebnis / Notizen

**Implementiert (2026-06-24):** Neue Datei `creative_studio/frameworks.py` als Copy-Pendant zu
`specs.py` — frozen dataclasses, rein-funktional, projektneutral. Inhalt:

- **`CopyFramework`-Datenklasse** (`key`, `name`, `slots`, `awareness`, `best_for`, `template`, `note`)
  + Katalog **`FRAMEWORKS`** mit 7 Frameworks: **AIDA, PAS, BAB, FAB, PASTOR, 4P, HSO** (Hook-Story-Offer).
  Jedes `template` nutzt **genau** seine `slots` als `{slot}`-Platzhalter (per Test verifiziert).
  `AWARENESS_LEVELS`-Konstante (unaware/problem_aware/solution_aware/product_aware/most_aware) +
  `get_framework(key)`.
- **`HookPattern`-Datenklasse** + Katalog **`HOOKS`** mit **7** seriösen, projektneutralen Mustern
  (give_me_x, specific_number, niche_question, pattern_interrupt, before_after, friction_statement,
  outcome_without_pain). Konstante **`MAX_WORDS_ONSCREEN = 7`** + Helper `count_onscreen_words()` /
  `hook_fits_onscreen()` (prüft On-Screen-Wortgrenze ≤ 7, Recherche §3.2). Bewusst KEINE
  reißerischen Druck-/„SCAM"-Hooks.
- **`recommend_framework(awareness, placement)`** — Awareness-Kurzregel (Recherche §1):
  cold/unaware→AIDA, problem_aware→PAS, solution_aware vergleichend→FAB (statisch) / BAB (Video),
  product_aware→BAB bzw. HSO (Video), warm/most_aware→HSO; Langform-Placements (vsl/sales_page/email)
  überschreiben → PASTOR. Synonyme cold/warm/vergleichend gemappt; unbekanntes Level → `ValueError`.
- **`validate_4u(headline)`** — 4U-Warn-Funktion (useful/urgent/unique/ultra_specific), analog
  `AdContent.warnings()`: liefert Hinweise als Liste, **keine harte Sperre**. Stützt sich auf
  `score_4u()` (grobe Wort-/Zahlen-Heuristik). Gesamt-Hinweis bei ≤ 1/4 erfüllten U.

**Abgrenzung eingehalten:** DACH-Compliance-Guard (`compliance_warnings`, UWG/HWG-Trigger,
`landing_promise`) bewusst NICHT implementiert — ist SKILL-026; in Docstrings/Notes nur referenziert.
`specs.py`, `render_image.py`, `batch.py`, `video/` **nicht** angefasst.

**Test-Ergebnis:** `tests/test_skill_025_frameworks.py` — **21 passed in 0.04s** (pytest).
Abdeckung: 1 EARS ≥ 1 Test (EARS-1 Katalog vollständig/wohlgeformt + Template↔Slots-Match;
EARS-2 ≥ 6 Hooks + Wortgrenze; EARS-3 parametrisiert über alle Awareness-Fälle inkl. Synonyme +
Langform-Override + ValueError; EARS-4 schwache vs. starke Headline + Nicht-Sperre; EARS-5
kein hartkodierter Projektwert im Katalog).

**Beispiel-Output `recommend_framework`:**

| awareness | placement | → Framework |
|---|---|---|
| `cold` | — | **AIDA** |
| `problem_aware` | — | **PAS** |
| `solution_aware` | `reel` | **BAB** |
| `warm` | `video` | **HSO** |
| `problem_aware` | `vsl` | **PASTOR** (Langform-Override) |

**Code-Referenz:** `skills_sources/creative-studio/creative_studio/frameworks.py` (neu),
`skills_sources/creative-studio/tests/test_skill_025_frameworks.py` (neu).
Kernstellen mit `# SKILL-025:`-Kommentaren markiert.

> [!note] Offen (kein Teil dieses Tickets)
> Generator-Anbindung (frameworks.py → render_image/video Copy-Set-Output, §4.2 Punkt 7) und
> SKILL-026 (Compliance-Guard + `landing_promise`-Message-Match) bleiben separate Tickets.
> `setup.ps1`-Deploy noch ausstehend (kein Deploy in diesem Ticket-Scope).
