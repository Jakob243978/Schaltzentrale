# SKILL-068: creative-studio — Video-Render nutzt Image-Browser explizit (kein Render-Zeit-Download)

**Status:** idea
**Erstellt:** 2026-07-02
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** Prod-Rollout `base-dev-253a31e` am 2026-07-02 (AgentischesArbeiten) —
Diagnose des Remotion-Tooling-Blockers im base-dev-Image. Verifizierte Testläufe im
Image: globales `remotion`-bin + `--browser-executable=<pfad>` rendert ohne Download
(mp4 41 KB, ftyp); `npx --yes remotion@4.0.482` scheitert ("could not determine
executable to run", kein CLI-bin im Basis-Paket).

> [!info] Herkunft
> Beim Prod-Rollout des `base-dev`-Images wurde das Content-**Video**-Tooling (Remotion)
> repariert: Der Image-Build zieht den Chrome-Headless-Shell jetzt deterministisch nach
> `/opt/remotion-browser` (hartes Build-Gate), und der Image-Smoke (`run_smoke.sh`) rendert
> mit dem globalen `remotion`-bin **explizit** gegen diesen Browser
> (`--browser-executable=$(find /opt/remotion-browser -name chrome-headless-shell)`).
> Der **echte** creative-studio-Video-Render tut das noch NICHT.

> [!note] Abgrenzung
> Image-/Template-Seite (Browser im Image, Smoke grün) ist mit Commit `253a31e`
> (AgentischesArbeiten) erledigt und auf allen 6 Prod-Instanzen live. Dieses Ticket
> betrifft ausschliesslich den **Skill-Code** in `skills_sources/creative-studio/`, damit
> der produktive Render denselben vorinstallierten Browser nutzt.

## Was soll erreicht werden? (Business-Ziel)
Der erste Video-Render eines Kunden startet sofort und offline — ohne dass Remotion zur
Laufzeit ~92 MB Chrome-Headless-Shell nachlädt. Der im Image vorinstallierte Browser wird
deterministisch verwendet (EARS-4 „kein Render-Zeit-Download" auch im echten Pfad, nicht nur
im Image-Smoke).

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When der creative-studio-Video-Render ausgeführt wird, the system shall das
      globale `remotion`-bin (bzw. `npx @remotion/cli`) verwenden — NICHT `npx remotion@<v>`
      (Basis-Paket ohne CLI-bin → „could not determine executable to run").
- [ ] **EARS-2:** When im Image ein Browser unter `$REMOTION_BROWSER_DIR` (Default
      `/opt/remotion-browser`) vorliegt, the system shall ihn per `--browser-executable=<pfad>`
      (=Syntax! ohne `=` interpretiert die CLI den Wert als boolean `true`) referenzieren, sodass
      KEIN Laufzeit-Download passiert.
- [ ] **EARS-3:** When kein Image-Browser gefunden wird (lokale Dev-Umgebung ohne Vorinstallation),
      the system shall auf Remotions Standardverhalten zurückfallen (Download/Auto-Ensure) — kein
      Hard-Fail ausserhalb des Images.
- [ ] **EARS-4 [multi-projekt]:** Der Browser-Pfad wird über eine Env/Konfig aufgelöst
      (`REMOTION_BROWSER_DIR`), kein hartkodierter Projekt-/Instanzwert.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** In der Render-Aufruf-Stelle (`reel_spec.py` bzw. der Renderer, der
  `npx remotion render … --props` baut) den Aufruf auf das globale `remotion`-bin umstellen und
  einen optionalen `--browser-executable=<pfad>` anhängen, wenn unter `REMOTION_BROWSER_DIR` eine
  `chrome-headless-shell`-Binary existiert (per `find`, wie im Image-Smoke bewiesen). Fehlt sie →
  Flag weglassen (Dev-Fallback).
- **Verworfene Alternative:** `REMOTION_BROWSER_DIR`/`--browser-executable-dir` als impliziten Cache
  nutzen — verworfen, weil `--browser-executable-dir` in 4.0.482 ignoriert wird (verifiziert: Browser
  landet in `$CWD/.remotion`, nicht im Zielordner). Nur `--browser-executable=<binary>` wirkt.
- **Betroffene Module:** `skills_sources/creative-studio/creative_studio/reel_spec.py` (Render-Aufruf),
  ggf. `batch.py`; `SKILL.md` (Render-Runtime-Hinweis). → ADR n/a.

## Technische Hinweise
- `surface: backend`. Klein (S). Kein Template-/Image-Blocker — die Image-Seite ist bereits live.
- Verifizierte Fakten aus dem Rollout (2026-07-02, quality-Image `base-dev-253a31e`):
  - `remotion render … --browser-executable=$BR` → 15/15 Frames, mp4 41196 Byte, `ftyp`, **kein** Download.
  - `--browser-executable $BR` (Leerzeichen) → Fehler „browserExecutable was specified as 'true'".
  - `npx --yes remotion@4.0.482 …` → „npm error could not determine executable to run".
- Nach Umsetzung: `setup.ps1` der Schaltzentrale ausführen (Deploy nach `~/.claude/skills/`).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/reel_spec.py` (Doku-Zeile „`npx remotion render … --props`").
- Referenz-Implementierung (Image-Seite, bereits live): `AgentischesArbeiten/terraform/base-dev/build/
  customization/content-tooling-smoke/run_smoke.sh` (EARS-4-Block) + `base-dev.Dockerfile` (browser ensure).

## Ergebnis / Notizen
(offen — idea)
