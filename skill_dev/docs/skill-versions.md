# Skill-Versions — Rollback-Anker fuer Skill-Source-Code

Diese Datei haelt **funktional validierte Skill-Versionen** + zugehoerige
Commit-Hashes + Rollback-Befehle bereit. Sie ist die Quelle fuer
"zurueck zu einer funktionierenden Version" wenn ein neuer Skill-Umbau
Reibung erzeugt.

> [!info] Append-only Log
> Neue Eintraege werden unten angehaengt, alte werden nie ueberschrieben.
> Konsistent zum Append-only-Pattern in SKILLS_VISION.md und
> governance_log.md.

> [!warning] Ergaenzt CHANGELOG.md, ersetzt es NICHT
> CHANGELOG.md = feinkoernige Aenderungen pro Datum.
> skill-versions.md = grobe, validierte Snapshots mit Rollback-Befehl.

---

## Format eines Eintrags

```
## <skill-name> v<version> — <YYYY-MM-DD>

- **Commit-Hash:** <kurz> (<voll>)
- **Status:** funktional validiert | experimental | rolled-back
- **Wofuer validiert:** <konkrete Features die laufen>
- **Rollback-Befehl (PowerShell):**
  ```powershell
  cd <Schaltzentrale>
  git checkout <hash> -- skills_sources/<skill-name>/
  .\setup.ps1
  ```
- **Bekannte Live-Anwendungen:** <Projekt 1>, <Projekt 2>
- **Optional Git-Tag:** <tag-name oder "kein Tag gesetzt">
- **Naechstes geplantes Bump:** v<n+1> via <TICKET-NNN oder SKILL-NNN>
```

---

## Eintraege (neueste unten)

## agile-sdd-skill v0.4 — 2026-05-25

- **Commit-Hash:** `fe9337a` (`fe9337a SDD: Verifier-Skill v0.4
  (EARS-Verify + PO-Klick-Anleitung + Cost-Tracking) + Recherche-Notes
  + Immobewertung tests/-Bootstrap`)
  - Der nachfolgende Commit `7fb0036` (Session sync 2026-05-25) hat den
    Skill-Source nicht inhaltlich veraendert; `fe9337a` ist der saubere
    v0.4-Code-Anker.
- **Status:** funktional validiert
- **Wofuer validiert:**
  - Bootstrap-Sequenz (Sektion A, 9 Schritte)
  - EARS-Akzeptanzkriterien (Sektion B)
  - Verifier-Pass (Sektion F.4) inkl. 5-Pflicht-Felder-Frontmatter
  - Cost-Tracking (Token + USD pro Ticket via Verify-Report)
  - Parallelisierung via Git Worktrees (Sektion J)
  - PO-Hook fuer `idea`→`spec`-Uebergang (Vision-Prinzip-Check)
- **Rollback-Befehl (PowerShell):**
  ```powershell
  cd C:\Users\Jakob\claude_projects\Schaltzentrale
  git checkout fe9337a -- skills_sources/agile-sdd-skill/
  .\setup.ps1
  ```
- **Bekannte Live-Anwendungen:**
  - Immobewertung (Verifier-Pass auf T078/T079 mit Cost-Tracking)
  - Schaltzentrale skill_dev (SKILL-001 Review, SKILL-002/003 Spec)
- **Optional Git-Tag (Vorschlag — nicht gesetzt):**
  `agile-sdd-skill-v0.4-pre-pre-conditions` auf Commit `fe9337a`.
  Setzen via:
  ```powershell
  git tag -a agile-sdd-skill-v0.4-pre-pre-conditions fe9337a `
    -m "agile-sdd v0.4 Snapshot vor Pre-Condition-Einbau (SKILL-004)"
  git push origin agile-sdd-skill-v0.4-pre-pre-conditions
  ```
  Tag-Setzen bleibt Jakob vorbehalten — Konvention im Repo: keine
  autonomen Tags durch KI-Agenten.
- **Naechstes geplantes Bump:** ~~v0.5 via SKILL-004~~ → siehe Korrektur
  unten (2026-05-31). v0.5 wurde stattdessen via SKILL-009 (inbox-Konvention,
  additiv/risikoarm) erreicht; SKILL-004 landet als v0.6.

## agile-sdd-skill v0.5 — 2026-05-31 (via SKILL-009, additiv)

- **Aenderung:** inbox/-Konvention (menschliches Eingangs-Material) — neue
  SKILL.md-Sektion K + Bootstrap-Punkt 10 (passiver Hinweis) +
  `inbox_source:`-Frontmatter-Feld + `inbox/`-Setup-Schritt mit
  `.gitignore`-Default in der "Neues Projekt"-Checkliste + `templates/TICKET.md`.
- **Risiko:** niedrig — rein additiv, backward-compatible (keine bestehende
  Mechanik geaendert; alte Tickets ohne `inbox_source` bleiben gueltig).
- **Versions-Reihenfolge-Hinweis:** SKILL-009 wurde **vor** SKILL-004/006
  umgesetzt (beide noch `spec`). Da der Skill-Version ein einzelner linearer
  Zaehler ist, belegt SKILL-009 die v0.5. **SKILL-004 bumpt entsprechend auf
  v0.6** (ROADMAP-Notiz "v0.5 via SKILL-004" ist damit ueberholt).
- **Status:** Skill-Quelle geaendert; Deploy via `setup.ps1` ausstehend,
  Verifier-Pass `/sdd-verify SKILL-009` ausstehend.
- **Rollback:** v0.4-Anker `fe9337a` (siehe oben) bleibt der saubere
  Pre-inbox-Stand.

## po-skill v0.1 — 2026-05-25

- **Commit-Hash:** `fe9337a` (gleicher Commit — po-skill wurde im Rahmen
  des Verifier-v0.4-Rollouts initial befuellt).
- **Status:** funktional validiert
- **Wofuer validiert:**
  - Vision-Constitution (`templates/vision.md`)
  - Challenge-Workflow (`/po-challenge`) — 3x-Why + 48h-Cooldown +
    Vision-Prinzip-Match
  - Prioritization (`/po-prioritize`) — RICE-Score
  - Outcome-Verifier (`/po-verify-outcome`) — 14-Tage-Check
  - Init-Pattern (`/po-init`) — angewandt in Immobewertung +
    Schaltzentrale skill_dev (manuell inline beim TICKET-083)
- **Rollback-Befehl (PowerShell):**
  ```powershell
  cd C:\Users\Jakob\claude_projects\Schaltzentrale
  git checkout fe9337a -- skills_sources/po-skill/
  .\setup.ps1
  ```
- **Bekannte Live-Anwendungen:**
  - Immobewertung (SKILL-001 Init-Lauf — done)
  - Schaltzentrale skill_dev (Vision-Constitution, DEFERRED.md,
    po-config.yaml, po-outcomes.md)
- **Optional Git-Tag (Vorschlag — nicht gesetzt):** `po-skill-v0.1-init`
- **Naechstes geplantes Bump:** v0.2 via SKILL-002 (Lift-and-Shift
  T078/T079 — Vision↔Features-Bridge generalisieren).

---

## Wann ein Eintrag hier?

- Eine **funktional validierte** Skill-Version ist erreicht (mind. 1
  Live-Anwendung in einem Projekt laeuft fehlerfrei).
- Vor einem **breaking-relevanten Skill-Umbau** (z.B. SKILL-004 Pre-
  Conditions, SKILL-006 KNOWN_FAILURES.md). Eintrag = Rollback-
  Versicherung.
- Bei Skill-Version-Bump im Frontmatter (`version: x.y` aendert sich).

## Wann KEIN Eintrag hier?

- Kleine Bugfixes ohne Verhaltensaenderung — gehoeren in CHANGELOG.md.
- Doku-Korrekturen in `skills_sources/<skill>/README.md` ohne
  Verhaltensaenderung.
- Aenderungen in `skill_dev/` (Meta-Layer) — die haben kein
  Skill-Versions-Bumping.
