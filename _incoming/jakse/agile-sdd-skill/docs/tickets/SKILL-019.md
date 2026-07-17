---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: m_l_xl_tickets_mit_loesungs_skizze
outcome_review_at: null
ui_verify_urls: []
api_endpoints_extended: n/a
surface: backend
---

# SKILL-019: Loesungs-Skizze-Block (Design-Phase light) fuer M/L/XL-Tickets

**Status:** spec
**Erstellt:** 2026-06-19
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (Skill-Doku-Aenderung: aufwand-abhaengiger Pflicht-
Block + Status-Gate-Regel + Ticket-Template-Erweiterung + ADR-Abgrenzung; keine
neue Runtime-Logik)
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`

## Trigger / Quelle

Research-Datei `skill_dev/docs/research/2026-06-19_sdd-doku-sota-vergleich.md`,
Vorschlag **SHOULD — SKILL-T-C**. Kiro und spec-kit haben bewusst eine
**Design-Phase** zwischen Requirements und Tasks (`Requirements → Design →
Tasks`). Unser Setup springt von Akzeptanzkriterium direkt zu Code — das
funktioniert bei XS/S, erzeugt aber bei M/L/XL die **Cognitive Debt**, vor der
ThoughtWorks v34 warnt (KI baut, Mensch versteht das "wie" nicht mehr).

## Die Luecke (Diagnose)

Zwischen `## Akzeptanzkriterien` und Code gibt es heute keinen festgehaltenen
Design-Schritt. ADRs decken nur projektweite Architektur-Weichen ab, nicht das
**ticket-lokale "wie genau"**. Folge: bei groesseren Tickets entsteht Code, ohne
dass irgendwo steht, *welcher Ansatz gewaehlt und welcher verworfen* wurde — eine
KI in einer neuen Session (und auch der Mensch) kann den gewaehlten Weg nicht
nachvollziehen, ohne den ganzen Code zu interpretieren.

## Was soll erreicht werden? (Business-Ziel)

Ein knapper, **nur fuer M/L/XL verpflichtender** `## Loesungs-Skizze (Approach)`-
Block (3–6 Zeilen: gewaehlter Weg, mind. eine verworfene Alternative, betroffene
Module) haelt das "wie" fest, **bevor** Code entsteht — gegen Cognitive Debt,
ohne Kiro-Schwergewicht. Bei trivialen Tickets (XS/S) bleibt er optional — kein
Overhead.

## Warum das Jakobs Ziel trifft (Doku-Nachvollziehbarkeit)

- **(a) Was wo geaendert wurde:** "betroffene Module" benennt vorab die
  Eingriffsstellen im Code — die KI weiss, wo zu arbeiten ist.
- **(b) Doku entsteht von selbst:** Der Block entsteht als natuerlicher
  Design-Schritt im Ticket, nicht nachtraeglich.
- **(c) KI in neuer Session:** Sie liest "gewaehlter Ansatz + verworfene
  Alternative" und weiss damit, **was schon versucht/entschieden wurde** — und
  wiederholt keine bereits verworfene Idee (gleicher Geist wie ADRs, nur
  ticket-lokal).

## Akzeptanzkriterien (EARS-Format)

- [ ] **EARS-1 (Pflicht-Block bei M/L/XL):** When ein Ticket den Aufwand `M`,
  `L` oder `XL` hat, the system shall vor Status-Uebergang nach `in_progress`
  einen `## Loesungs-Skizze (Approach)`-Block mit (1) gewaehltem Ansatz, (2)
  mind. einer verworfenen Alternative und (3) betroffenen Modulen verlangen.
- [ ] **EARS-2 (optional bei XS/S):** When der Aufwand `XS` oder `S` ist, the
  system shall den Block als optional behandeln (kein Zwang, kein leerer
  Pflicht-Block).
- [ ] **EARS-3 (ADR-Abgrenzung, kein Doppel-Dokument):** When der gewaehlte
  Ansatz eine projektweite Architektur-Weiche beruehrt (ADR-Kriterium aus
  SKILL.md D), the system shall im Block auf das ADR verweisen statt die
  Entscheidung doppelt auszuformulieren — Approach-Block = ticket-lokales,
  vergaengliches "wie"; ADR = projektweite, immutable Weiche.
- [ ] **EARS-4 (Status-Gate, weich):** When ein M/L/XL-Ticket nach `in_progress`
  wechselt ohne `## Loesungs-Skizze`-Block, the system shall einen Hinweis
  ausgeben ("Loesungs-Skizze fehlt — bei M/L/XL erwartet"); Default ist Warning,
  Hard-Block nur bei `sdd-config.yaml: approach_block_required_for_ML: true`.
- [ ] **EARS-5 (Bestandteil der Traceability/Doku):** When der Block existiert,
  the system shall seine "betroffene Module"-Angabe konsistent zu den
  spaeteren `## Code-Referenzen` halten (der Approach kuendigt an, die
  Code-Referenzen belegen).
- [ ] **EARS-6 (additiv/abwaertskompatibel):** While bestehende Tickets keinen
  `## Loesungs-Skizze`-Block tragen, the system shall sie unveraendert
  akzeptieren (kein nachtraeglicher Pflicht-Block fuer alte Tickets).

## Konkreter Patch-Vorschlag (welche SKILL.md-Stellen)

> [!important] NICHT blind applien — Source-of-Truth = `skills_sources/agile-sdd-skill/`
> Deploy NUR via `setup.ps1`. Additiv, nichts loeschen.

1. **`SKILL.md` B) "Ticket-Format (Pflichtfelder)":** im Ticket-Geruest zwischen
   `## Akzeptanzkriterien` und `## Technische Hinweise` einen
   `## Loesungs-Skizze (Approach)`-Block dokumentieren (3–6 Zeilen, Pflicht ab
   M/L/XL, optional bei XS/S, mit ADR-Abgrenzung).
2. **`SKILL.md` B) Status-Flow / C) Spec-First-Workflow:** Regel ergaenzen, dass
   bei M/L/XL der Approach-Block vor `in_progress` erwartet wird (Warning-Default,
   Hard-Block per Config).
3. **`SKILL.md` D) ADR:** kurzer Abgrenzungs-Satz "Approach-Block (ticket-lokal,
   vergaenglich) vs. ADR (projektweit, immutable)".
4. **`templates/TICKET.md`:** `## Loesungs-Skizze (Approach)`-Block mit
   Anleitung + Aufwand-Hinweis ergaenzen.
5. **`templates/sdd-config.yaml.example`:** optionalen Schalter
   `approach_block_required_for_ML: false` (Default Warning) dokumentieren.
6. **Versions-Header `SKILL.md` (gemeinsam mit SKILL-017/018 auf v0.6).**

## Abgrenzung

- **Kein Kiro-Schwergewicht** (kein separates `design.md` mit
  Sequenzdiagrammen) — bewusst 3–6 Zeilen im Ticket.
- **Kein Block fuer XS/S** — verhindert Overhead bei Trivial-Tickets.

## Code-Referenzen (skills_sources/agile-sdd-skill/)

- `SKILL.md` (B Ticket-Format + Status-Flow, C Spec-First, D ADR-Abgrenzung,
  Versions-Header)
- `templates/TICKET.md` (`## Loesungs-Skizze (Approach)`-Block)
- `templates/sdd-config.yaml.example` (`approach_block_required_for_ML`-Schalter)

## Out of Scope

- Eigene Design-Phase als Status (`design` zwischen `spec` und `in_progress`)
  — bewusst nicht, der Block lebt im bestehenden Status-Flow.
- Verifier prueft den Approach-Block inhaltlich — bleibt Implementer-/PO-Arbeit
  (Verifier prueft EARS, nicht Design-Qualitaet).

## Verhaeltnis zu SKILL-017 / SKILL-018 / ADRs

- **SKILL-017** spurt Test/Code-Abdeckung, **SKILL-018** spurt Spec-Aenderung,
  **SKILL-019** haelt den Design-Ansatz fest — drei unterschiedliche Doku-Achsen.
- **ADR (Sektion D)** bleibt fuer projektweite Weichen; der Approach-Block ist
  die leichtgewichtige, ticket-lokale Ergaenzung darunter.

## [J] — was Jakob noch tun muss

1. SKILL-019 reviewen (`/po-challenge` optional).
2. `Schaltzentrale/setup.ps1` ausfuehren (Deploy nach `~/.claude/skills/`).
3. Entscheiden, ob `approach_block_required_for_ML` global auf Hard-Block geht
   oder Warning bleibt (Default-Empfehlung: Warning, wie bei vision_principle).
