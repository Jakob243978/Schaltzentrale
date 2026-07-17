---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: spec_touch_tickets_mit_spec_delta_block
outcome_review_at: null
ui_verify_urls: []
api_endpoints_extended: n/a
surface: backend
---

# SKILL-018: Spec-Delta-Block pro Ticket (Brownfield-Nachvollziehbarkeit)

**Status:** spec
**Erstellt:** 2026-06-19
**MoSCoW:** Should
**Geschaetzter Aufwand:** S (Skill-Doku-Aenderung: neues optionales Ticket-Feld/
Block + Ticket-Template-Erweiterung + CHANGELOG-Kopplung; keine neue
Runtime-Logik)
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`

## Trigger / Quelle

Research-Datei `skill_dev/docs/research/2026-06-19_sdd-doku-sota-vergleich.md`,
Vorschlag **SHOULD — SKILL-T-B**. OpenSpec (ThoughtWorks Radar v34) zeigt: in
Bestandssystemen (Brownfield) ist die *Aenderung* der Spec das wertvolle
Artefakt, nicht die Voll-Spec ("spec deltas", `propose → apply → archive`).

## Die Luecke (Diagnose)

Heute wird `PROJECT_SPEC.md` laut SKILL.md C) **"waehrend der Implementierung
aktualisiert"** — die konkrete Aenderung verschwindet danach in der Git-History
und ist **nicht ticket-lokal nachvollziehbar**. Eine KI in einer neuen Session,
die wissen will "was hat sich am System-Verhalten durch TICKET-NNN geaendert",
muss `git blame`/`git log` auf PROJECT_SPEC.md fahren statt eine Antwort im
Ticket zu finden. Das widerspricht Jakobs Ziel, dass das **Ticket selbst**
erzaehlt, was getan/geaendert wurde.

## Was soll erreicht werden? (Business-Ziel)

Jedes Ticket, das `PROJECT_SPEC.md` (oder eine andere Spec-Datei) veraendert,
fuehrt einen optionalen `## Spec-Delta`-Block mit **Vorher/Nachher-Kurzfassung**.
So ist jede Spec-Mutation auffindbar und an das ausloesende Ticket gekoppelt —
passt exakt zur Governance-Grundregel "kein Fix ohne Ticket". Bewusst
leichtgewichtig: Delta-Notiz **im Ticket**, KEIN separates Delta-File pro Ticket
wie OpenSpec (das waere fuer dieses 1-Personen-Setup Over-Engineering).

## Warum das Jakobs Ziel trifft (Doku-Nachvollziehbarkeit)

- **(a) Was wo geaendert wurde:** Der Vorher/Nachher-Block sagt praezise, welche
  Spec-Aussage sich wie geaendert hat — ohne Git-Archaeologie.
- **(b) Doku entsteht von selbst:** Der Block wird beim Implementieren mitgefuehrt
  und beim done-Schritt im CHANGELOG `### Technical` referenziert.
- **(c) KI in neuer Session:** Sie liest am Ticket direkt "was wurde am
  Verhalten/Spec geaendert und warum" — Teil der "was schon gemacht wurde"-Spur.

## Akzeptanzkriterien (EARS-Format)

- [ ] **EARS-1 (Spec-Delta-Block dokumentiert):** When `templates/TICKET.md` und
  die "Ticket-Format (Pflichtfelder)"-Sektion in `SKILL.md` (B) gelesen werden,
  the system shall einen optionalen `## Spec-Delta`-Block mit Vorher/Nachher-
  Kurzfassung beschreiben (welche `PROJECT_SPEC.md`-Aussage additiv geaendert/
  ergaenzt wurde).
- [ ] **EARS-2 (Pflicht bei Spec-Touch):** When ein Ticket `PROJECT_SPEC.md`
  (oder eine andere Spec-Datei) veraendert, the system shall den `## Spec-Delta`-
  Block ausfuellen (Vorher/Nachher + Anlass) — der Block ist bei Spec-Touch
  Pflicht.
- [ ] **EARS-3 (CHANGELOG-Kopplung):** When ein Ticket mit Spec-Delta auf `done`
  geht, the system shall den Spec-Delta-Verweis im CHANGELOG `### Technical`
  referenzieren (z.B. `[TICKET-NNN] Spec-Delta: <Kurzfassung>`).
- [ ] **EARS-4 (weglassbar ohne Spec-Touch):** When kein Spec-Touch stattfand,
  the system shall den Block weglassen — optional, kein Zwang, kein leerer
  Pflicht-Block.
- [ ] **EARS-5 (Governance-Kopplung erhalten):** When eine Spec-Aenderung
  passiert, the system shall (wie heute, SKILL.md I) zusaetzlich der Governance-
  Log-Pflicht "Jede Aenderung an PROJECT_SPEC.md" genuegen — der Spec-Delta-Block
  ergaenzt diese Pflicht, ersetzt sie nicht.
- [ ] **EARS-6 (additiv/abwaertskompatibel):** While bestehende Tickets keinen
  `## Spec-Delta`-Block tragen, the system shall sie unveraendert akzeptieren
  (kein Bruch, reine Doku-Konvention).

## Konkreter Patch-Vorschlag (welche SKILL.md-Stellen)

> [!important] NICHT blind applien — Source-of-Truth = `skills_sources/agile-sdd-skill/`
> Deploy NUR via `setup.ps1`. Additiv, nichts loeschen.

1. **`SKILL.md` B) "Ticket-Format (Pflichtfelder)":** im Ticket-Geruest nach
   "Code-Referenzen" einen optionalen `## Spec-Delta`-Block dokumentieren (mit
   Vorher/Nachher-Mini-Schema + Hinweis "nur bei Spec-Touch").
2. **`SKILL.md` C) Spec-First-Workflow:** den Satz "Die Spec wird waehrend der
   Implementierung aktualisiert" um den Verweis ergaenzen: "...und die Aenderung
   wird im `## Spec-Delta`-Block des ausloesenden Tickets als Vorher/Nachher
   festgehalten (Brownfield-Nachvollziehbarkeit)."
3. **`SKILL.md` E) Living Documentation / CHANGELOG:** Regel ergaenzen, dass ein
   Spec-Delta beim done-Schritt im `### Technical`-Block referenziert wird.
4. **`templates/TICKET.md`:** optionalen `## Spec-Delta`-Block mit
   Kommentar-Anleitung ergaenzen.
5. **Versions-Header `SKILL.md` (gemeinsam mit SKILL-017/019 auf v0.6).**

## Abgrenzung

- **Kein separates Delta-File** pro Ticket (kein `docs/spec-deltas/`), kein
  `propose/apply/archive`-Workflow — bewusst leichter als OpenSpec.
- **Kein Spec-Regenerieren** (Tessl-Ansatz) — wir bleiben inkrementell.

## Code-Referenzen (skills_sources/agile-sdd-skill/)

- `SKILL.md` (B Ticket-Format, C Spec-First-Workflow, E Living Documentation,
  Versions-Header)
- `templates/TICKET.md` (`## Spec-Delta`-Block)

## Out of Scope

- Maschinelle Erzwingung (Pre-Commit-Hook, der prueft ob PROJECT_SPEC im Diff =>
  Spec-Delta vorhanden) — moeglicher Folge-Hook, hier nur Doku-Regel.

## Verhaeltnis zu SKILL-017 / SKILL-019

- **SKILL-017** (TRACEABILITY) spurt Test-/Code-Abdeckung; **SKILL-018** spurt
  Spec-/Verhaltens-Aenderung — komplementaer.
- **SKILL-019** (Loesungs-Skizze) haelt das *wie* der Implementierung fest;
  SKILL-018 haelt fest, *was sich an der Spec aenderte*. Verschiedene Achsen.

## [J] — was Jakob noch tun muss

1. SKILL-018 reviewen (`/po-challenge` optional).
2. `Schaltzentrale/setup.ps1` ausfuehren (Deploy nach `~/.claude/skills/`).
3. Entscheiden, ob ein optionaler Pre-Commit-Hook (Spec-Touch ⇒ Delta-Pflicht)
   als Folge-Ticket eroeffnet wird.
