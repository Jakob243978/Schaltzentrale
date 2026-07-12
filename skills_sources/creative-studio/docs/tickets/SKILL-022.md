# SKILL-022: creative-studio — Output automatisch in projekt-lokalen Marketing-Ordner

**Status:** spec
**Erstellt:** 2026-06-23
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null

> [!info] Herkunft (Jakob 2026-06-23)
> Die ersten Test-Creatives landeten im Session-Temp/Scratchpad (fluechtig, schwer auffindbar) und
> mussten manuell ins Projekt kopiert werden (`AgentischesArbeiten/marketing/ad-creatives/h1-immo/`).
> Anforderung: **Wenn der Skill fuer ein Projekt verwendet wird, soll der Output automatisch in einem
> projekt-lokalen Marketing-Ordner landen** (auto-angelegt) — nicht in Temp.

## Was soll erreicht werden? (Business-Ziel)
Generierte Creatives (Bild + Video) sind **automatisch im richtigen Projekt** abgelegt, auffindbar +
versionierbar — ohne manuelles Kopieren. Multi-Projekt: der Zielordner ergibt sich aus dem Projekt
(Parameter/Konvention), kein hartkodierter Pfad.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When der Skill Creatives fuer ein Projekt erzeugt, the system shall den Output in
      einen **projekt-lokalen Marketing-Ordner** schreiben (Konvention: `<projekt>/marketing/ad-creatives/<ad-id>/`),
      der bei Bedarf **automatisch angelegt** wird — nicht in einen Temp-/Scratchpad-Pfad.
- [ ] **EARS-2:** When der Zielordner nicht existiert, the system shall ihn (rekursiv) anlegen.
- [ ] **EARS-3 [multi-projekt]:** When der Skill in unterschiedlichen Projekten laeuft, the system shall
      den Projekt-Root als Parameter (`--project-dir`/Config) nehmen und den Marketing-Ordner relativ
      dazu auflösen — kein hartkodierter Projektpfad im Skill.
- [ ] **EARS-4:** When `render_image.py` / das Video-Modul ohne expliziten `--out` aufgerufen wird, the
      system shall den projekt-lokalen Marketing-Ordner als **Default-Ziel** verwenden (statt `out/`/Temp).

## Technische Hinweise
- `render_image.py`: `--out` Default auf den projekt-lokalen Pfad umstellen (aus `--project-dir` +
  Konvention ableiten). Video-Modul (`video/`) analog (Render-Ziel relativ zum Projekt).
- Konvention `<projekt>/marketing/ad-creatives/<ad-id>/` — passt zu bestehendem `marketing/`-Ordner in
  AgentischesArbeiten. Bei Projekten ohne `marketing/` den Ordner anlegen.
- **Offene Zukunft (DEFERRED 2026-06-23):** ob Videos langfristig per Git oder anders gespeichert werden
  — separate Entscheidung, blockt dieses Ticket nicht.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/render_image.py` (--out-Default).
- `skills_sources/creative-studio/video/` (Render-Ziel).

## Ergebnis / Notizen
_(wird beim Abschließen befüllt)_
