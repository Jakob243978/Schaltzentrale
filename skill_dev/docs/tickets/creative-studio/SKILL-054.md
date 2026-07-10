# SKILL-054: creative-studio — Wettbewerber-Watchlist + Trend-Tracking (estimated_total_count)

**Status:** spec
**Erstellt:** 2026-06-24
**MoSCoW:** Could
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_meta-ad-library-zugriff-budget.md` (§3 Scan-Ablauf, §6 MoSCoW Could)

> [!info] Herkunft (Recherche 2026-06-24)
> Two-Could-Erweiterungen des Ad-Library-Scans (SKILL-052/053): eine **Watchlist** relevanter DACH-
> Wettbewerber-Page-IDs (Coaching/Consulting/KI-Automation) fuer wiederkehrende Scans, und ein
> **Trend-Tracking**, das denselben Themen-Scan periodisch wiederholt und steigende `estimated_total_count`
> / neue Hooks erkennt (Markttiefe ueber Zeit). Bewusst Could — Komfort/Skalierung, kein Kern.

## Was soll erreicht werden? (Business-Ziel)
Wiederkehrende Wettbewerbs-Beobachtung: eine pflegbare Watchlist von Page-IDs + ein periodischer
Themen-Scan, der Veraenderungen (steigende Markttiefe via `estimated_total_count`, neu aufgetauchte Hooks)
sichtbar macht — als laufendes Signal fuer die Content-Strategie.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When eine Watchlist (Liste von Page-IDs + Labels) konfiguriert ist, the system shall sie als
      Eingabe fuer wiederkehrende Page-Drilldowns (SKILL-052) nutzen. → Test `test_watchlist_drives_drilldowns`.
- [ ] **EARS-2:** When ein Themen-Scan wiederholt laeuft, the system shall den aktuellen `estimated_total_count`
      gegen den vorigen Lauf vergleichen und **Delta** (steigend/fallend) + neue Hooks markieren.
      → Test `test_trend_delta_and_new_hooks`.
- [ ] **EARS-3 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall Watchlist
      + Themen + Verlaufs-Speicherpfad als Parameter nehmen — kein hartkodierter Wettbewerber-/Projektwert.
      → Test `test_watchlist_project_neutral`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Kleine Erweiterung auf SKILL-052: Watchlist als Config-Datei (Page-IDs + Labels),
  Verlaufs-Snapshots (`estimated_total_count` + Hook-Set je Lauf) als JSON; Delta-Vergleich beim naechsten
  Lauf. Kein Scheduler im Skill — der Lauf wird extern getriggert (Agent/Routine).
- **Verworfene Alternative:** Eigener Cron/Scheduler im Skill — verworfen (Plattform-/Orchestrierungs-Sache,
  nicht Skill-Aufgabe). Skill liefert nur Watchlist-Eingang + Delta-Logik.
- **Betroffene Module:** `creative_studio/ad_library_scan.py` (Watchlist + Verlaufs-Delta), Config/Verlaufs-
  JSON, neue Tests.

## Technische Hinweise
- `surface: backend`. Verlaufs-Speicher als einfache JSON-Snapshots (kein DB). Delta = Mengen-/Zahlen-Vergleich.
- Voraussetzung: SKILL-052 (Scan-Modul); profitiert von SKILL-053 (Hook-Bibliothek als Hook-Set-Quelle).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/ad_library_scan.py` — Watchlist + Verlaufs-Delta (Block `# SKILL-054`).
- `skills_sources/creative-studio/tests/test_skill_054_watchlist_trend.py` (neu).
- Wissensgrundlage: `2026-06-24_meta-ad-library-zugriff-budget.md` (§3, §6 Could).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
