# SKILL-026: creative-studio — DACH-Compliance-Guard ausbauen (UWG/HWG-Heuristik + Ad↔LP-Message-Match)

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** abmahn_risiken_vor_launch_geflaggt (UWG/HWG-Trigger + Ad↔LP-Mismatch als Warnung) + guard_projektneutral_wiederverwendbar
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_ad-copywriting-frameworks.md` (§2.4 DACH-Fallstricke UWG §5/§7/Schwarze Liste/HWG, §3.6 Message-Match Ad↔LP, §4.2 Punkte 5+6); `2026-06-23_creative-studio-flow-improvements.md` (§2.1 DACH-Coaching-Vorsicht)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> Der bestehende `COACHING_CLAIM_TRIGGERS`-Heuristik-Block in `specs.py` warnt heute nur vor wenigen
> „Du + Vorher-Nachher"-Mustern. Die DACH-Rechtslage (UWG §5 irrefuehrende Werbung, §7 Belaestigung,
> Schwarze Liste falsche Verknappung, HWG Heilversprechen) ist breiter — und Abmahnungen sind real
> (Anwaltskosten ~800–1.500 EUR, Vertragsstrafe 5.000 EUR+). Zudem fehlt eine Ad↔Landingpage-Message-Match-
> Pruefung (Mismatch kostet CVR + Relevanz-Score). **Nur Warnungen, keine harte Sperre.**

## Was soll erreicht werden? (Business-Ziel)
Den vorhandenen Claim-Guard zu einer dokumentierten **UWG/HWG-Heuristik** ausbauen (Garantie-/Erfolgs-/
Heil-/Vorher-Nachher-Trigger inkl. Abmahn-Hinweis im Warntext) und ein optionales `landing_promise`-Feld
in `AdContent` ergaenzen, das eine Warnung ausloest, wenn Headline/Hook nicht zur LP-Promise passen.
Projektneutral, weiterhin nur Warn-Ausgabe (kein harter Block).

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When ein `AdContent`-Text Garantie-/Erfolgs-/Heil-/Vorher-Nachher-Muster enthaelt
      (erweiterte Trigger-Liste: „garantiert", „verdopple deinen umsatz", „in X tagen zu", „100 % erfolg",
      gesundheitsbezogene Begriffe …), the system shall eine **Warnung** mit Hinweis auf das konkrete Risiko
      (UWG/HWG, Abmahnung) ausgeben — keine harte Sperre.
- [x] **EARS-2:** When ein Warntext erzeugt wird, the system shall die jeweilige Rechtsgrundlage/das Risiko
      kurz benennen (z. B. „UWG §5 irrefuehrend" / „HWG Heilversprechen" / „Abmahn-Risiko") statt nur den
      Treffer zu melden.
- [x] **EARS-3:** When `AdContent` ein optionales `landing_promise`-Feld gesetzt hat, the system shall warnen,
      wenn Headline/Hook **nicht** zur LP-Promise passen (Message-Match-Heuristik, §3.6).
- [x] **EARS-4:** When `landing_promise` leer ist, the system shall keine Message-Match-Warnung ausgeben
      (Feld bleibt optional, kein Pflichtbruch).
- [x] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall die
      Trigger-Heuristik projektneutral halten (DACH-Rechtsmuster, keine projekt-spezifischen Claims hartkodiert).

## Technische Hinweise
- `specs.py`: `COACHING_CLAIM_TRIGGERS` zu kategorisierter Struktur erweitern (Garantie/Erfolg/Heil/
  Vorher-Nachher), Warntext um Risiko-Klartext ergaenzen. Optional Auslagerung der Guard-Logik nach
  `frameworks.py::compliance_warnings(...)` (SKILL-025) und Re-Use in `AdContent.warnings()`.
- `AdContent` um `landing_promise: str = ""` erweitern + Message-Match-Warnung in `warnings()`.
- Bewusst **keine** harte Sperre — Metas 20-%-Regel ist tot, und Recht ist Heuristik, kein Automatik-Block.
  Mensch entscheidet final (Recherche §2.6: DACH-Recht bleibt Mensch-im-Loop).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — erweiterte Trigger-Liste, `AdContent.landing_promise`,
  `AdContent.warnings()`.
- `skills_sources/creative-studio/creative_studio/frameworks.py` — optional `compliance_warnings(...)` (SKILL-025).
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_ad-copywriting-frameworks.md` (§2.4, §3.6, §4.2).

## Ergebnis / Notizen

**Umgesetzt (2026-06-24, additiv in `specs.py`):**
- Der bestehende `COACHING_CLAIM_TRIGGERS`-Block wurde zu **dokumentierten Trigger-Sets nach
  Rechtsgrundlage** ausgebaut (alle additiv, bestehendes Tupel unveraendert + als eine der Kategorien
  weiterverwendet):
  - `GUARANTEE_TRIGGERS` (garantiert/100 % erfolg/risikofrei …) → **UWG §5**
  - `SUPERLATIVE_UNPROVEN` (beste/Nr. 1/marktführer …) → **UWG §5 (Spitzenstellung)**
  - `SUCCESS_PROMISE_TRIGGERS` (verdopple deinen umsatz/in X tagen zu …) → **UWG §5**
  - `HEALTH_TRIGGERS` (heilt/burnout heilen/stress weg …) → **HWG**
  - `SCARCITY_FAKE` (nur noch heute/letzte plätze/jetzt oder nie …) → **UWG Schwarze Liste (Anh. §3)**
  - `BEFORE_AFTER_TRIGGERS` (vorher-nachher/vom anfänger zum profi …) → **UWG §5 + Coaching**
  - `COACHING_CLAIM_TRIGGERS` (bestehend) → **Coaching-Fallstrick / Meta-Policy**
- Mapping `COMPLIANCE_TRIGGER_SETS` (Label, Trigger, Risiko-Klartext) + neue Funktion
  `compliance_warnings(text)` — jeder Warntext nennt Rechtsgrundlage + Abmahn-Hinweis,
  Wortlaut sachlich („abmahngefaehrdet/pruefen", nie „verboten"). EARS-1/EARS-2.
- `AdContent.landing_promise: str = ""` (optional) + `message_match_warning(headline, landing_promise)`:
  warnt bei fehlendem gemeinsamen Kern-Begriff zwischen Headline und LP-Promise (§3.6, EARS-3);
  leeres Feld → keine Warnung (EARS-4). Stoppwort-Liste projektneutral (EARS-5).
- `AdContent.warnings()` ruft jetzt `compliance_warnings(...)` + `message_match_warning(...)` auf →
  bestehende Aufrufer (`render_image.py`, `batch.py`) profitieren automatisch, ohne Code-Aenderung.
  Alles bleibt **Warnung, keine harte Sperre** (Mensch-im-Loop).

**Test-Ergebnis:** `pytest tests/test_skill_026_compliance.py -q` → **24 passed** (0.04s). Je Kategorie
ein Treffer-Test + Gegenprobe, Message-Match greift/greift-nicht/leeres-Feld, bestehende Coaching-Warnung
(Regression) gruen, Projektneutralitaet (EARS-5), „nie Exception" (keine harte Sperre).

**Beispiel-Warntexte:**
- `Garantie-/Erfolgsgarantie-Claim-Risiko: 'garantiert' — UWG §5 (irrefuehrende Werbung) — unbelegte
  Garantie/Erfolgssicherheit ist abmahngefaehrdet. Beleg ergaenzen oder produkt-/prozessbezogen formulieren.`
- `Gesundheits-/Heilbezug-Risiko: 'heilt' — HWG (Heilmittelwerbegesetz) — gesundheits-/heilbezogene
  Aussage ist abmahngefaehrdet. Heilversprechen vermeiden (HWG pruefen).`
- `Fake-Verknappung/Druck-Risiko: 'nur noch heute' — UWG Schwarze Liste (Anhang zu §3) — kuenstliche/
  falsche Verknappung ist per se unzulaessig und abmahngefaehrdet. Nur echte Limitierung nennen.`
- `Message-Match-Risiko: Ad-Headline und Landingpage-Promise teilen keinen Kern-Begriff — Mismatch senkt
  CVR + Relevanz-Score (§3.6). Hook/Outcome der Ad oben auf der LP woertlich/visuell wieder aufnehmen.`

**Code-Referenz:**
- `skills_sources/creative-studio/creative_studio/specs.py` — Trigger-Sets, `COMPLIANCE_TRIGGER_SETS`,
  `compliance_warnings()`, `message_match_warning()`, `AdContent.landing_promise`, `AdContent.warnings()`
  (alle Aenderungen mit `# SKILL-026:` kommentiert, additiv).
- `skills_sources/creative-studio/tests/test_skill_026_compliance.py` — 24 Tests.

**Bewusst NICHT umgesetzt (Scope-Abgrenzung):** Auslagerung nach `frameworks.py::compliance_warnings`
(als Option im Ticket genannt) — wegen Konfliktvermeidung mit parallelen Subagenten in `frameworks.py`.
Die Guard-Logik liegt projektneutral in `specs.py` und ist von dort wiederverwendbar/importierbar.
