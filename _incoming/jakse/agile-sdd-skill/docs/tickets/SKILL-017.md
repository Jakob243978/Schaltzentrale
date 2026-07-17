---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: done_tickets_mit_traceability_zeile
outcome_review_at: null
ui_verify_urls: []
api_endpoints_extended: n/a
surface: backend
---

# SKILL-017: Traceability-Matrix-Generator (`docs/TRACEABILITY.md`)

**Status:** spec
**Erstellt:** 2026-06-19
**MoSCoW:** Must
**Geschaetzter Aufwand:** M (Skill-Doku-Aenderung: done-Hook-Erweiterung + neue
F-Sektion + Generator-Beschreibung + Template; reine Aggregation vorhandener
Artefakte, KEINE neue Datenquelle)
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`

## Trigger / Quelle

Research-Datei `skill_dev/docs/research/2026-06-19_sdd-doku-sota-vergleich.md`
(SOTA-Abgleich agile-sdd v0.6 / po-skill v0.2), Vorschlag **MUST — SKILL-T-A**.
Die Requirements-Traceability-Matrix (RTM) ist laut Recherche der industrielle
Kern-Hebel fuer *messbare* Doku-Qualitaet (Six Sigma, Ketryx, Medizintechnik-
Compliance) und schliesst den ThoughtWorks-v34-"Mensch-im-Loop"-Anspruch ab.

## Was soll erreicht werden? (Business-Ziel)

Eine generierte, abfragbare Matrix `docs/TRACEABILITY.md` fuehrt pro
EARS-Akzeptanzkriterium **Requirement → Test → Code → Verify-Status** in einer
Zeile zusammen. Damit sieht eine **KI in einer neuen Session** auf einen Blick:
welcher EARS-Satz hat keinen Test, welcher Test ist nicht gruen, welcher
Code-Pfad ist verwaist, welches Ticket steht ohne Verify-Report. Der Mensch
(Jakob) erkennt Doku-/Test-Luecken ohne den gesamten Code interpretieren zu
muessen. Maximaler Nutzen bei minimalem Neubau — alle Bestandteile existieren
bereits verstreut (EARS-IDs im Ticket, `test_ears_N`-Tests, `# TICKET-NNN`-Code-
Kommentare, Verify-Report mit `pass/partial/fail`), werden nur nie aggregiert.

## Warum das Jakobs Ziel trifft (Doku-Nachvollziehbarkeit)

- **(a) Was wo geaendert wurde:** Die Code-Referenz-Spalte zeigt pro EARS-Satz
  die Datei(en) — der Einstiegspunkt fuer "wo im Code eingreifen".
- **(b) Doku entsteht von selbst:** Die Matrix wird beim done-Hook automatisch
  regeneriert (analog FEATURE_MAP, SKILL-002/TICKET-078) — keine Hand-Pflege.
- **(c) KI in neuer Session:** Eine einzige Datei beantwortet "was ist abgedeckt,
  was fehlt, wo ist der Code" — ohne dass die KI alle Tickets + den ganzen Code
  lesen muss.

## Akzeptanzkriterien (EARS-Format)

- [ ] **EARS-1 (done-Hook regeneriert):** When ein Ticket auf `done` gesetzt
  wird, the system shall (analog FEATURE_MAP-Hook, SKILL.md B "Auto-Doku-Hook")
  `docs/TRACEABILITY.md` regenerieren, sofern das Projekt den Generator hat
  (Opt-in, best-effort, blockt `done` NICHT).
- [ ] **EARS-2 (Matrix-Zeilen-Schema):** When `docs/TRACEABILITY.md` generiert
  wird, the system shall pro EARS-Satz eine Zeile mit den Spalten
  `EARS-ID | Ticket | Test-Name | Code-Referenz | Verify-Status` fuehren.
- [ ] **EARS-3 (fehlender Test markiert):** When ein EARS-Satz keinen
  zugeordneten `test_ears_N`-Test (bzw. `test_ticket_NNN_*`) hat, the system
  shall die Zeile als `⚠ kein Test` markieren.
- [ ] **EARS-4 (Verify-Status gespiegelt):** When ein Verify-Report fuer das
  Ticket `fail` oder `partial` enthaelt, the system shall diesen Status in der
  Matrix-Zeile spiegeln (statt `pass`); fehlt ein Report ganz, shall die Zeile
  `⚠ kein Verify-Report` tragen.
- [ ] **EARS-5 (Bootstrap-Frische-Hinweis):** When beim Bootstrap done-Tickets
  existieren, aber `docs/TRACEABILITY.md` fehlt oder aelter als das juengste
  done-Ticket ist, the system shall dem User passiv vorschlagen, den Generator
  zu laufen (kein Hard-Block, analog A.8 FEATURE_MAP-Frischecheck).
- [ ] **EARS-6 (additiv/abwaertskompatibel):** While ein Projekt den Generator
  nicht hat (kein `workers/traceability_generator.py` o.Ae.), the system shall
  den Hook still ueberspringen — kein Bruch bestehender Projekte, kein erzwungenes
  Tooling.

## Konkreter Patch-Vorschlag (welche SKILL.md-Stellen)

> [!important] NICHT blind applien — Source-of-Truth = `skills_sources/agile-sdd-skill/`
> Deploy NUR via `setup.ps1`. Aenderungen additiv, nichts Bestehendes loeschen.

1. **`SKILL.md` B) "Status-Transition `review` → `done` — Auto-Doku-Hook":**
   Den Generator-3er-Block um einen dritten Generator
   `python -m workers.traceability_generator` ergaenzen (re-generiert
   `docs/TRACEABILITY.md`). Best-effort wie die anderen, WARN statt Block.
2. **`SKILL.md` A) Bootstrap Schritt 8 / Frische-Check:** TRACEABILITY.md in die
   Frische-Pruefung aufnehmen (analog FEATURE_MAP / PROJECT_OVERVIEW).
3. **`SKILL.md` neue Sektion `F.7 Traceability-Matrix`:** beschreibt Datenquellen
   (Ticket-EARS, Test-Namen, Code-Referenzen, Verify-Reports), Zeilen-Schema,
   Markierungs-Regeln (`⚠ kein Test` / `⚠ kein Verify-Report`), Generator-Aufruf,
   Best-effort-Charakter.
4. **`SKILL.md` Templates-Referenz + E) Living Documentation:** TRACEABILITY.md
   als lebendes Artefakt listen.
5. **NEU `templates/TRACEABILITY.md`:** Tabellen-Geruest + Legende + Generator-
   Hinweis.
6. **Versions-Header `SKILL.md` v0.5 → v0.6.**

## Abgrenzung

- **Kein lauffaehiger Generator-Code** in diesem Ticket-Scope erzwungen — die
  Aggregations-Logik ist Agenten-/Projekt-Arbeit (LLM liest Tickets + Tests +
  Verify-Reports), analog `/po-reconcile` (SKILL-015): wo ein Projekt einen
  deterministischen `traceability_generator.py` will, ist das ein Projekt-lokaler
  Worker (Lift-and-Shift-Muster wie SKILL-002). Hier nur Hook + Format + Regel.
- **Kein Done-Block:** Die Matrix-Pflege darf nie ein Ticket blockieren
  (best-effort, gleicher Geist wie FEATURE_MAP-Hook).

## Code-Referenzen (skills_sources/agile-sdd-skill/)

- `SKILL.md` (A Bootstrap-Frische-Check, B Auto-Doku-Hook, neue F.7, E Living
  Documentation, Templates-Referenz, Versions-Header)
- `templates/TRACEABILITY.md` (NEU)

## Out of Scope

- Deterministischer Parser/Generator als Pflicht — projekt-lokaler Worker, kein
  Skill-Kern.
- Aenderung der Verifier-Pruef-Logik (bleibt wie VERIFIER.md).

## Verhaeltnis zu SKILL-016 / SKILL-018

- **SKILL-016** erzwingt *dass* ein Verify-Report existiert (Gate). SKILL-017
  *aggregiert* den Report-Status in die Matrix — beide greifen sauber ineinander
  (`⚠ kein Verify-Report` in der Matrix ist der Lese-Indikator des SKILL-016-Gates).
- **SKILL-018** (Spec-Delta) liefert die Spec-Aenderungs-Spur; TRACEABILITY ist
  die Test-/Code-Abdeckungs-Spur. Komplementaer, keine Ueberlappung.

## [J] — was Jakob noch tun muss

1. SKILL-017 reviewen (`/po-challenge` optional).
2. `Schaltzentrale/setup.ps1` ausfuehren (Deploy nach `~/.claude/skills/`).
3. Entscheiden, ob ein deterministischer `traceability_generator.py` pro
   Projekt gebaut wird (Folge-Ticket, analog SKILL-002 feature_map_generator).
