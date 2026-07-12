---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: tickets_mit_regressionsrisiko_die_einen_wiederholbaren_test_tragen
outcome_review_at: null
ui_verify_urls: []
api_endpoints_extended: n/a
surface: backend
---

# SKILL-069: Regressionstest pro Ticket mitdenken (`regression_test`-Feld + Regression-Gate)

**Status:** spec
**Erstellt:** 2026-07-02
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (Skill-Doku-Aenderung: ein Frontmatter-Feld +
Heuristik + eine Verify-Gate-Bedingung + Config-Schalter; keine neue
Runtime-Logik)
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`

## Trigger-Live-Erfahrung

Jakob 2026-07-02 (AgentischesArbeiten, Affiliate-Feature **TICKET-225**):

> Beim Affiliate-Feature wurden **manuell** sehr wertvolle Regressionstests
> gefahren — Provision-Rechenlogik, Satz-Historie, plus die Grenzfaelle
> 0-€ / unbekannt / Duplikat. Der SDD-Prozess soll kuenftig **pro Ticket
> pruefen, ob ein Regressionstest sinnvoll ist**, und ihn dann einfordern.

Pattern: Die bestehende Test-Pflicht (F.3, „1 EARS = mind. 1 Test") sichert,
**dass das Neue funktioniert**. Sie sagt aber nichts darueber, ob eine Aenderung
**bestehendes, etabliertes Verhalten stillschweigend bricht** — genau das, was
bei berechnender/zustandsbehafteter Logik (Geldbetraege, Historien, Grenzfaelle)
teuer wird. Bei TICKET-225 fiel das nur auf, weil Jakob die Regressionstests
**von Hand** anstiess; das System hat sie nicht eingefordert.

Nebenbeleg, dass das Bewusstsein informell schon existiert: creative-studio-
Sessions notieren im CHANGELOG bereits „180→200 passed, **0 Regressionen**" —
aber als Ad-hoc-Gewohnheit, nicht als erzwungene Ticket-Dimension.

## Die Luecke (Diagnose)

Der Skill kennt zwei Test-Achsen: **F.1/F.3** (Happy Path + kritischer Edge-Case
pro EARS) und **F.5** (Property-Based, opt-in). Beide sind *vorwaerts* gerichtet
(„tut das neue Feature, was der EARS-Satz sagt?"). Es fehlt die *rueckwaerts*
gerichtete Achse — die **Feedback-Control** im Sinne von ThoughtWorks Radar v34
(„Mutation/Regression-Testing zur Selbstkorrektur *vor* dem menschlichen
Review", Research `2026-06-19_sdd-doku-sota-vergleich.md`, Abschnitt 1). Ohne
eine bewusste Ja/Nein-Entscheidung pro Ticket bleibt „Regressionstest sinnvoll?"
dem Zufall / manuellem Nachhaken ueberlassen.

## Recherche-Fazit (knapp)

- **DoD-Erweiterung statt neuer Test-Kategorie.** Reife Agile-Praxis trennt
  **Acceptance Criteria** (ticket-lokal, „richtiges Produkt") von der **Definition
  of Done** (projektweit, „Produkt richtig gebaut") — Research a.a.O. Abschnitt 2.
  „Bestehendes Verhalten bleibt intakt" gehoert klassisch in die **DoD**, nicht in
  die AC. Genau da setzt das Feld an: es ergaenzt das Done-Gate um eine
  Regressions-Bedingung, statt eine parallele Test-Buerokratie zu erfinden.
- **Test-Impact-Analyse light.** Grosse SDD-Stacks (spec-kit „production incidents
  feed back into specifications", ThoughtWorks Feedback-Controls) verankern
  Regression bewusst am *geaenderten* Pfad. Wir brauchen dafuer KEINE
  Coverage-/Mutation-Tooling-Pipeline — eine **Heuristik pro Ticket** (beruehrt die
  Aenderung berechnende/zustandsbehaftete/geteilte Logik?) reicht fuer ein
  1-Personen-KI-Setup und vermeidet Over-Engineering.
- **Analoges Vorbild im eigenen Skill:** die `surface`-Klassifikation (SKILL-014,
  „web ⇒ UI-Verifier-Pflicht") und das harte Verify-Gate (SKILL-016). Beide sind
  **ein Frontmatter-Feld + eine Gate-Bedingung**. `regression_test` ist die exakt
  gleiche Bauform auf einer neuen Achse — kein neues Konstrukt-Muster.

## Was soll erreicht werden? (Business-Ziel)

Der agile-sdd-Skill zwingt bei **jedem** Ticket eine bewusste Entscheidung
„braucht das einen Regressionstest?" ueber ein Frontmatter-Feld
`regression_test: yes|no|n/a` (gesetzt beim `spec → in_progress`-Uebergang,
analog `surface`). Bei `yes` verlangt das Done-Gate mindestens **einen
wiederholbaren** Test, der das etablierte Verhalten (inkl. der genannten
Grenzfaelle) festnagelt und nach der Aenderung gruen bleibt — sonst kein `done`.
So wird die TICKET-225-Erfahrung strukturell statt manuell.

## Heuristik — wann gilt `regression_test: yes`?

`yes`, sobald **mindestens eine** zutrifft (Aenderung beruehrt bestehendes,
still-brechbares Verhalten):

1. **Berechnungs-/Geldlogik** — Betraege, Provisionen/Saetze, Steuer, Rundung,
   Aggregation, Scoring, KPI-Extraktion. *(TICKET-225: Provision-Rechenlogik.)*
2. **Zustandsbehaftete / historisierte Daten** — Satz-/Status-Historie,
   Versionierung, Migrationen/Backfills, Felder mit zeitlichem Verlauf.
   *(TICKET-225: Satz-Historie.)*
3. **Integration / geteilter Kontrakt** — geaendertes API-Response-Schema,
   gemeinsame Worker/Module (`db/models.py`, `api/main.py`), Daten mit mehreren
   Consumern (koppelt an SKILL-010 „API-Schema-Mitdenken").
4. **Grenzfaelle mit Geld-/Datenfolge** — 0-€ / leer / unbekannt / Duplikat /
   negativ; Faelle, deren Fehlverhalten teuer ist. *(TICKET-225: 0-€, unbekannt,
   Duplikat.)*
5. **Bug-Fix an bestehender Logik** — der Regressionstest ist der Reproduzierer,
   der ab jetzt gruen bleiben muss.

`no` — reine **neue, isolierte** Logik ohne Beruehrung bestehender Pfade: der
EARS-Test (F.3) ist bereits die volle Abdeckung, kein Altverhalten in Gefahr.

`n/a` — reines Copy/Text/Doc/Style/Config-Label **ohne Verhaltensaenderung**
(deckt sich mit F.2 „Was nicht getestet wird").

> [!info] Abgrenzung F.3 vs. Regressionstest
> **F.3** sichert: *tut das Neue, was der EARS-Satz sagt.*
> **Regressionstest** sichert: *bricht das Alte dabei nicht.*
> Oft ist ein sorgfaeltig gewaehlter Edge-Case-Test beides — dann genuegt EIN
> Test, er muss nur den etablierten Wert/Verlauf festnageln (nicht nur den neuen
> Pfad). Das Feld erzwingt die *Entscheidung*, keine Test-Verdopplung.

## Akzeptanzkriterien (EARS-Format)

- [ ] **EARS-1 (Feld dokumentiert + Pflicht-Entscheidung):** When
  `templates/TICKET.md` und die „Ticket-Format (Pflichtfelder)"-Sektion in
  `SKILL.md` (B) gelesen werden, the system shall ein Frontmatter-Feld
  `regression_test: yes|no|n/a` beschreiben, das beim Uebergang `spec →
  in_progress` bewusst gesetzt wird (analog `surface`, SKILL-014).
- [ ] **EARS-2 (Heuristik hinterlegt):** When der Agent `regression_test` setzt,
  the system shall die 5-Punkt-Heuristik (oben) als Entscheidungsgrundlage in
  `SKILL.md` F fuehren — `yes` bei berechnender/zustandsbehafteter/geteilter
  Logik oder Grenzfaellen mit Geld-/Datenfolge oder Bug-Fix; `no` bei rein neuer
  isolierter Logik; `n/a` bei reinem Copy/Doc/Style.
- [ ] **EARS-3 (Regression-Gate bei `yes`):** When ein Ticket
  `regression_test: yes` traegt, the system shall im Done-Gate (`SKILL.md` B
  Status-Flow + F) verlangen, dass mindestens **ein wiederholbarer**
  Regressionstest existiert und referenziert ist (Test-Datei/-Name im Ticket,
  im Verify-Report bestaetigt gruen) — fehlt er, bleibt das Ticket `review`,
  kein `done`. STOPP-Klausel, nicht Empfehlung (analog Verify-Gate SKILL-016).
- [ ] **EARS-4 (`no`/`n/a` unveraendert):** When ein Ticket `regression_test:
  no` oder `n/a` traegt, the system shall das heutige Gate (F.3 EARS-Tests +
  Verifier-Output) unveraendert anwenden — kein zusaetzlicher Zwang.
- [ ] **EARS-5 (Verify-Report + Traceability):** When der Verifier einen Report
  schreibt, the system shall bei `regression_test: yes` eine Zeile
  „Regression-Gate: <pass|fail — Test(s): …>" fuehren; die Traceability-Matrix
  (SKILL-017) darf die Zuordnung mitfuehren (rein additiv, best-effort).
- [ ] **EARS-6 (konfigurierbar, abwaertskompatibel):** When ein Projekt
  `docs/sdd-config.yaml` mit `regression_gate: { require_test_when_yes: true }`
  traegt, the system shall das harte Gate anwenden; fehlt der Block, gilt
  `require_test_when_yes: true` als sicherer Default. While bestehende Tickets
  kein `regression_test`-Feld tragen, the system shall sie als `n/a`/nicht-
  gesetzt behandeln (kein nachtraeglicher Zwang, kein Bruch).

## Konkreter Patch-Vorschlag (welche SKILL.md-Stellen)

> [!important] NICHT blind applien — Source-of-Truth = `skills_sources/agile-sdd-skill/`
> Deploy NUR via `setup.ps1`. Additiv/verschaerfend, nichts Bestehendes
> loeschen. Zeilennummern Stand v0.6 (2026-07-02) — vor Apply gegen die aktuelle
> Datei verifizieren.

1. **`SKILL.md` B) „Ticket-Format (Pflichtfelder)":** im Pflichtfeld-Block
   `regression_test: [yes | no | n/a]` ergaenzen, mit Einzeiler „bewusst gesetzt
   beim `spec → in_progress`-Uebergang; Heuristik siehe F".
2. **`SKILL.md` B) Status-Flow, Block `review → done`:** die Bedingung um einen
   benannten **Regression-Gate**-Satz erweitern: „Bei `regression_test: yes` ist
   `done` nur erlaubt, wenn mind. ein wiederholbarer Regressionstest existiert
   und im Verify-Report gruen ist — sonst STOPP, Ticket bleibt `review`.
   Konfigurierbar via `sdd-config.yaml: regression_gate.require_test_when_yes`
   (Default `true`)."
3. **`SKILL.md` F) Test-/Qualitaetsstrategie:** neuer Unterabschnitt **F.8
   Regressionstest-Mitdenken (SKILL-069)** — Heuristik (5 Punkte), Abgrenzung zu
   F.3, Gate-Regel. Kurz und leichtgewichtig, im Stil von F.5.
4. **`SKILL.md` „Status-Transition `review → done` — Auto-Doku-Hook":** eine
   Zeile, dass „auf `done` setzen" bei `regression_test: yes` das Regression-Gate
   einschliesst (auch bei Subagenten/Wellen — analog SKILL-016 EARS-4).
5. **`SKILL.md` „Aktivierung in Projekt-CLAUDE.md":** SDD-Config-Zeile um
   `regression_gate.require_test_when_yes` ergaenzen; Ticket-Bloecke-Zeile um
   `regression_test`-Frontmatter erweitern.
6. **`templates/TICKET.md`:** Frontmatter um `regression_test: yes|no|n/a` +
   Kurz-Hinweis auf die Heuristik.
7. **`templates/sdd-config.yaml.example`:** Block ergaenzen:
   ```yaml
   regression_gate:
     require_test_when_yes: true   # regression_test: yes ⇒ done nur mit gruenem, wiederholbarem Regressionstest
   ```
8. **`verifier/VERIFIER.md`:** Pflicht-Check ergaenzen — „Traegt das Ticket
   `regression_test: yes`? Wenn ja: existiert ein wiederholbarer Regressionstest
   und ist er gruen? Wenn nein: Verify-Status `partial`, Gate NICHT bestanden."
9. **`templates/verify-report.md`:** Status-Zeile „Regression-Gate:
   yes|no|n/a → <pass|fail|n/a>".
10. **Versions-Header `SKILL.md`:** naechster Minor-Bump — **gebuendelt mit den
    noch offenen Gate-Tickets SKILL-014/SKILL-016** in einem Deploy (siehe
    „Reihenfolge/Verhaeltnis").

## Reihenfolge / Verhaeltnis zu SKILL-014 & SKILL-016 (wichtig)

- **SKILL-014** (surface-Gate) und **SKILL-016** (Verify-Gate „Report Pflicht vor
  `done`") sind aktuell **`spec` und noch NICHT in die SKILL.md-Source appliziert**
  (verifiziert 2026-07-02: kein `surface`/`verify_gate` im Source-`SKILL.md`).
  SKILL-069 ist deren **direktes Geschwister** — dieselbe Bauform (Frontmatter-
  Feld + STOPP-Gate).
- **Empfehlung:** SKILL-014, SKILL-016 und SKILL-069 in **einem** koordinierten
  `setup.ps1`-Deploy mit **einem** gemeinsamen Versions-Bump applien — sonst
  entstehen drei Teil-Bumps und ein Regression-Gate, das auf ein noch nicht
  existierendes verify_gate-Konstrukt verweist.
- **Deshalb hier bewusst SPEC-only** (SKILL.md-Source NICHT angefasst): Die
  additiven Doc-Bloecke SKILL-017/018/019 wurden zwar direkt in die Source
  gezogen, aber **Enforcement-Gates** (SKILL-014/016) werden in diesem Repo
  gestaffelt und gemeinsam von Jakob deployed. SKILL-069 folgt exakt diesem
  Muster. (Merke: Ein Source-Edit ist ohnehin erst nach `setup.ps1` live — der
  koordinierte Deploy ist der richtige Moment.)

## Abgrenzung / Anti-Pattern wahren

- **Keine zweite Test-Bibliothek.** Ein Regressionstest ist ein normaler pytest-
  Case (ggf. genau der F.3-Edge-Case), nur mit dem Blick „nagelt Altverhalten
  fest". Kein neues Framework, kein Coverage-Gate, kein Mutation-Tooling-Zwang.
- **Kein Zwang bei `no`/`n/a`.** Reine Copy-/Doc-Tickets bleiben unberuehrt.
- **Verifier fixt nicht.** Er prueft nur, ob der Regressionstest existiert +
  gruen ist, und flaggt sonst `partial` — er schreibt keinen Test, setzt kein
  `done` (wie SKILL-014/016).
- **Kein `regression`-Status im Flow.** Das Feld lebt im bestehenden
  `idea→spec→in_progress→review→done`, kein neuer Status.

## Code-Referenzen (skills_sources/agile-sdd-skill/)

- `SKILL.md` (B Ticket-Format + Status-Flow, neuer Abschnitt F.8, Auto-Doku-Hook,
  Aktivierungs-Block, Versions-Header)
- `templates/TICKET.md` (`regression_test:` Frontmatter)
- `templates/sdd-config.yaml.example` (`regression_gate`-Block)
- `verifier/VERIFIER.md` (Regression-Gate-Check)
- `templates/verify-report.md` (Regression-Gate-Status-Zeile)
- Verweis: SKILL-014 (surface-Gate) + SKILL-016 (verify_gate) als komplementaere
  Gates, SKILL-010 (API-Schema) und SKILL-017 (Traceability) als Andock-Punkte

## Out of Scope

- Maschinelle Erzwingung via Hook/CI — Skill-Doku-/Verhaltens-Regel, kein
  Pre-Commit-Hook (eigenes Folge-Ticket, falls je gewuenscht).
- Coverage-/Mutation-Testing-Pipeline — bewusst nicht (Over-Engineering fuer
  1-Personen-Setup; ThoughtWorks-Feedback-Control-Geist reicht als Heuristik).
- Auto-Generierung von Regressionstests — Test bleibt Implementer-Arbeit.

## Live-Beispiel

AgentischesArbeiten **TICKET-225** (Affiliate-Feature): Provision-Rechenlogik +
Satz-Historie + Grenzfaelle 0-€/unbekannt/Duplikat — genau ein
`regression_test: yes`-Fall. Dort wurden die Tests manuell gefahren; SKILL-069
macht daraus die erzwungene Ticket-Dimension fuer ALLE Projekte.

## [J] — was Jakob noch tun muss

1. SKILL-069 reviewen (`/po-challenge` optional).
2. Entscheiden, ob `require_test_when_yes` global **Hard-Block** (Default-
   Empfehlung, analog SKILL-016) oder zunaechst **Warning** ist.
3. Patch (Punkte 1–10) applien — **gebuendelt mit SKILL-014 + SKILL-016** in
   `Schaltzentrale/skills_sources/agile-sdd-skill/` (SKILL.md, templates/,
   verifier/), gemeinsamer Versions-Bump.
4. `Schaltzentrale/setup.ps1` ausfuehren (Deploy nach `~/.claude/skills/`).

## Ergebnis / Notizen

(offen — spec. Bewusst SPEC-only: SKILL.md-Source NICHT angefasst, weil
Enforcement-Gate-Geschwister SKILL-014/016 auf koordinierten Deploy warten —
Begruendung in Sektion „Reihenfolge/Verhaeltnis".)

## Quelle

Jakob 2026-07-02 (TICKET-225-Regressionstest-Erfahrung). Research-Basis:
`skill_dev/docs/research/2026-06-19_sdd-doku-sota-vergleich.md` (Feedback-Controls
/ DoD vs. AC). Komplementaer zu SKILL-014 (surface-Gate) + SKILL-016 (verify_gate).
