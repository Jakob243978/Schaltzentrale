---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: living_docs_synchron_nach_reconcile
outcome_review_at: null
api_endpoints_extended: n/a
surface: backend
---

# SKILL-067: `/po-reconcile` pflegt Living-Docs automatisch mit

**Status:** spec
**Erstellt:** 2026-06-26
**MoSCoW:** Should
**Geschaetzter Aufwand:** S–M (reine Skill-Doku-Aenderung: neuer `reconcile.living_docs`-
Block-Konzept + Erweiterung der `/po-reconcile`-Schritte um Living-Doc-Pflege +
SKILL.md-Sektion-K-Ergaenzung + po-config-Block + Command-Doc; KEINE neue
Runtime-Logik, KEINE autonome Vision-Aenderung)
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren` (Live-erkannte Drift fuehrt
nicht nur zu einem Vorschlags-Doc, sondern haelt zusaetzlich die abgeleiteten
Living-Docs synchron, statt sie veralten zu lassen)
**Baut auf:** SKILL-015 (`/po-reconcile` Vision-Drift-Check — dort als „Vision-Living-Doc"-
Praevention bereits als separater Strang empfohlen, hier umgesetzt)

## Trigger-Live-Erfahrung

AgentischesArbeiten 2026-06-26: Es existieren mehrere **abgeleitete Living-Docs**
neben der Vision-Verfassung — `docs/projekt-cockpit.html` (Vision/Roadmap/KPIs/
ADRs/Reconcile-Status in einer Drift-Sicht) und `docs/customer-journey.html`
(Journey-SSOT). Genau die strukturelle Wurzel, die SKILL-015 als Drift-Beleg
nannte (veraltete Vision-HTML neben aktueller `PROJECT_VISION.md`), reproduziert
sich, sobald solche Docs **nicht aktiv mit dem Reconcile-Lauf mitgezogen werden**.
SKILL-015 hat die Detektion gebaut und die **Praevention** („Living-Doc wird AUS
der Vision gepflegt/generiert") explizit als separaten Strang offen gelassen
(SKILL-015 Sektion „Empfehlung — Vision-Living-Doc-Prinzip"). Dieses Ticket setzt
diesen Strang um.

## Was soll erreicht werden? (Business-Ziel)

Beim `/po-reconcile`-Lauf pflegt der Skill — **zusaetzlich** zum Vision-Schaerfungs-
VORSCHLAG (Vision selbst NIE schreiben) — die in `po-config.yaml` gelisteten
**Living-Docs** synchron mit der gelebten Realitaet:

- `docs/projekt-cockpit.html` — Vision-Kern, Prinzipien, Outcome-KPIs (Live-Werte
  aus DB/instances), Roadmap, ADR-Liste (Titel + Status), Reconcile-Status/Drift-Karte.
- `docs/customer-journey.html` — Journey-relevante Drift (neue Branche/Vertikale,
  neuer Rollen-Touchpoint, Status-Wechsel 🟡→✅), konsistent zur Journey-SSOT-
  Konvention (keine Dopplungen).

**Generisches Muster:** eine konfigurierbare Liste `reconcile.living_docs` (Pfade)
im `po-config.yaml`. Der Reconcile-Lauf haelt jeden gelisteten Pfad synchron — das
Muster ist projekt-unabhaengig (jedes Projekt traegt seine eigenen Living-Doc-Pfade
ein). Fehlt die Liste, ist die Living-Doc-Pflege ein No-Op (abwaertskompatibel).

> [!warning] Klare Abgrenzung (Anti-Pattern bleibt strikt)
> - **Vision (`docs/PROJECT_VISION.md`)** = append-only-Hoheit Jakob. `/po-reconcile`
>   schreibt NIE in die Vision, legt KEINE Tickets an — nur ein Vorschlags-Doc
>   (`docs/po-reconcile-YYYY-MM-DD.md`).
> - **Living-Docs** (Cockpit, Journey, …) = **generiert/gepflegt**, abgeleitet aus
>   Vision/Roadmap/ADRs/DB. Sie tragen einen sichtbaren Header-Hinweis „Lebendes
>   Doc — von `/po-reconcile` gepflegt; Vision-Hoheit bleibt PROJECT_VISION.md".
> - Living-Docs sind NIE die Quelle der Vision — Drift wird zur Vision hin
>   aufgeloest, nicht umgekehrt.

## Mechanismus-Entwurf

### Config — neuer `reconcile.living_docs`-Block (`po-config.yaml`)

```yaml
po_skill:
  reconcile:
    # Living-Docs, die /po-reconcile beim Lauf synchron haelt (abgeleitet,
    # NIE die Vision selbst). Fehlt der Block -> Living-Doc-Pflege ist No-Op.
    living_docs:
      - docs/projekt-cockpit.html
      - docs/customer-journey.html
```

(Liegt neben dem bestehenden `reconcile_trigger`-Block; beide unter `po_skill`.)

### Ablauf-Erweiterung `/po-reconcile`

Nach Schritt „Vorschlags-Doc schreiben" ein zusaetzlicher Schritt:

> **Schritt — Living-Docs synchronisieren.** Fuer jeden Pfad in
> `reconcile.living_docs`: das Doc gegen die seit dem Anker-Datum erkannten
> vision-relevanten Verschiebungen + den aktuellen Stand (Roadmap, ADR-Liste,
> Outcome-KPI-Live-Werte, Reconcile-Datum/Drift) aktualisieren. NUR abgeleitete
> Inhalte — die Vision selbst bleibt unberuehrt. Existiert der Pfad nicht oder
> ist die Liste leer: ueberspringen (No-Op, kein Fehler). Brand-Tokens der Surface
> respektieren (tokens.css/`--brand-*`, kein hartkodierter Hex).

### Abgrenzung „generiert vs. gepflegt"

- Wo ein Generator existiert (z.B. KPI-Werte aus DB), wird neu gerendert.
- Wo es Redaktions-Inhalt ist (Journey-Touchpoint-Status), wird gepflegt/
  nachgezogen — konsistent zur jeweiligen SSOT-Konvention des Docs (z.B.
  Journey-SSOT: keine Dopplungen, Status ✅/🟡/❌).

## Akzeptanzkriterien (EARS-Format)

- [ ] **EARS-1 (SKILL.md dokumentiert Living-Doc-Pflege):** When `SKILL.md`
  gelesen wird, the system shall in der `/po-reconcile`-Sektion (K) einen
  Unterabschnitt „Living-Doc-Pflege" beschreiben (Config-Block
  `reconcile.living_docs`, Ablauf-Schritt, Abgrenzung Vision=Hoheit /
  Living-Doc=gepflegt).
- [ ] **EARS-2 (Anti-Pattern erhalten):** When die Living-Doc-Pflege spezifiziert
  ist, the system shall explizit festhalten, dass `/po-reconcile` die Vision NIE
  schreibt und KEINE Tickets anlegt — Living-Docs sind abgeleitet, nicht Quelle.
- [ ] **EARS-3 (Config-gesteuert + No-Op-sicher):** When `po-config.yaml` einen
  `reconcile.living_docs`-Block traegt, the system shall die gelisteten Pfade beim
  Reconcile synchron halten; fehlt der Block oder ist er leer, gilt die Living-Doc-
  Pflege als No-Op ohne Fehler (abwaertskompatibel).
- [ ] **EARS-4 (Command-Doc erweitert):** When `commands/po-reconcile.md` gelesen
  wird, the system shall einen Schritt „Living-Docs synchronisieren" nach dem
  Vorschlags-Doc-Schritt enthalten + den „Was du NICHT tust"-Block um
  „Living-Doc als Vision-Quelle behandeln" ergaenzen.
- [ ] **EARS-5 (Template ausgerollt):** When `/po-init` ein neues Projekt aufsetzt,
  the system shall den `reconcile.living_docs`-Block (leer, mit Kommentar) in der
  generierten `po-config.yaml` aus `templates/po-config.yaml.example` mitliefern.

## Konkreter Patch-Vorschlag (welche Dateien)

> [!important] NICHT blind applien
> `skills_sources/po-skill/SKILL.md` ist Source-of-Truth → Deploy nur via
> `Schaltzentrale/setup.ps1` (robocopy). Vor Apply gegen die aktuelle Datei
> verifizieren.

1. **`skills_sources/po-skill/SKILL.md`** — Sektion `K) Vision-Reconciliation`
   um Unterabschnitt „Living-Doc-Pflege" erweitern (Config-Block, Ablauf-Schritt,
   Abgrenzung). Anti-Pattern-Block um einen Bullet ergaenzen. *(In diesem Ticket
   bereits umgesetzt — siehe „Umsetzung" unten.)*
2. **`skills_sources/po-skill/commands/po-reconcile.md`** — falls vorhanden:
   Schritt „Living-Docs synchronisieren" + „Was du NICHT tust"-Bullet. *(Die
   Datei existierte zum Ticket-Zeitpunkt noch nicht — SKILL-015-Strang; sobald
   sie angelegt ist, diesen Schritt aufnehmen.)*
3. **`skills_sources/po-skill/templates/po-config.yaml.example`** — `reconcile.living_docs`-
   Block (leer + Kommentar) ergaenzen, damit `/po-init` ihn ausrollt.
4. **Projekt-lokal (AgentischesArbeiten, bereits umgesetzt):**
   `docs/po-config.yaml` `reconcile.living_docs`-Block + `CLAUDE.md` „Skill: PO"-
   Hinweis, dass `/po-reconcile` Cockpit + Journey mitzieht.

## Out of Scope

- **Auto-Schaerfung der Vision** — strikt verboten (Anti-Pattern, gilt unveraendert).
- **Lauffaehiger HTML-Generator/Parser** — die Living-Doc-Pflege ist Agenten-Arbeit
  (LLM liest Vision/Roadmap/ADRs/DB und aktualisiert die Surface). Ein deterministischer
  Generator (analog SKILL-002) ist ein moegliches Folge-Ticket, nicht hier.
- **Neue Living-Doc-Typen erfinden** — der Skill pflegt nur, was ein Projekt in
  `reconcile.living_docs` listet.

## Quelle

SKILL-015 Sektion „Empfehlung — Vision-Living-Doc-Prinzip (separater Strang)" +
AgentischesArbeiten 2026-06-26 (Cockpit + Journey als abgeleitete Living-Docs neben
`PROJECT_VISION.md`). Drift-Wurzel: abgeleitete Praesentations-Docs veralten, wenn
kein PO-Command sie beim Reconcile mitzieht.

## Umsetzung (Stand 2026-06-26)

Im Rahmen der AgentischesArbeiten-Cockpit-Arbeit bereits angewendet:
- `skills_sources/po-skill/SKILL.md` — Sektion K + Anti-Pattern-Bullet (Living-Doc-Pflege).
- `AgentischesArbeiten/docs/po-config.yaml` — `reconcile.living_docs`-Block.
- `AgentischesArbeiten/CLAUDE.md` — „Skill: PO"-Block-Hinweis.
- `AgentischesArbeiten/docs/projekt-cockpit.html` (neu) + `docs/customer-journey.html` (aktualisiert)
  als die ersten beiden gepflegten Living-Docs.
Offen: `commands/po-reconcile.md` (existiert noch nicht — SKILL-015-Strang),
`templates/po-config.yaml.example`-Block, setup.ps1-Deploy + `/sdd-verify SKILL-067`.
