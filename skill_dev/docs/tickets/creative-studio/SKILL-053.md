# SKILL-053: creative-studio — Snapshot-Anreicherung (EU-Reach) + persistente Hook-Bibliothek im Vault

**Status:** spec
**Erstellt:** 2026-06-24
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_meta-ad-library-zugriff-budget.md` (§1 EU-Reach via Snapshot, §2 Proxy-Signal 5, §4 Schritt 4, §6 MoSCoW Should)

> [!info] Herkunft (Recherche 2026-06-24)
> Zwei Should-Erweiterungen des Ad-Library-Scans (SKILL-052): (a) **Snapshot-Anreicherung** — fuer Top-N-Ads
> die `ad_snapshot_url` oeffnen und Volltext + Visual + **EU-Reach-Band** erfassen (die einzige offizielle,
> semi-quantitative Budget-Annaeherung fuer kommerzielle Ads, manueller Oeffnen-Schritt pro Ad), und (b) eine
> **persistente, querybare Hook-/Angle-Bibliothek** im Vault, die Scans ueber Zeit akkumuliert.

## Was soll erreicht werden? (Business-Ziel)
Den Scan um zwei Stufen erweitern: einen optionalen Anreicherungs-Schritt, der fuer die Top-N-Score-Ads die
Snapshot-Seite auswertet (Volltext/Visual/EU-Reach-Band), und eine persistente Hook-Bibliothek im Vault
(Obsidian-Note), in der wiederkehrende Hooks/Angles aus mehreren Scans gesammelt + querybar werden.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When fuer Top-N-Ads die Anreicherung aktiviert ist, the system shall pro Ad die
      `ad_snapshot_url` als Quelle nutzen und Volltext + Visual-Hinweis + **EU-Reach-Band** (falls auf der
      Seite vorhanden) erfassen — als manueller/Vision-Oeffnen-Schritt dokumentiert.
- [ ] **EARS-2:** When EU-Reach nicht verfuegbar ist, the system shall das **ehrlich** als „nicht abrufbar"
      markieren (kein geschaetzter/erfundener Wert). → Test/Doku-Beleg.
- [ ] **EARS-3:** When ein Scan abgeschlossen ist, the system shall die extrahierten Hooks/Angles in eine
      **persistente Vault-Note** (Obsidian-Konvention: Frontmatter + ggf. Base-tauglich) schreiben/ergaenzen,
      sodass mehrere Scans ueber Zeit akkumulieren (querybar). → Test `test_hook_library_append`.
- [ ] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall den
      Vault-/Output-Pfad als Parameter nehmen — kein hartkodierter Projekt-/Vault-Pfad. → Test `test_vault_path_param`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** `ad_library_scan.py` (SKILL-052) um `enrich_snapshot()` (Snapshot-Auswertung,
  Vision/manuell) + `append_hook_library(vault_path, hooks)` erweitern. Hook-Bibliothek als Obsidian-Note
  (Frontmatter + Wikilinks/Callouts; ggf. `.base` fuer Tabellen-View) — Obsidian-Markdown-Konventionen
  beachten (Skill-Bootstrap obsidian-markdown vor dem Schreiben laden).
- **Verworfene Alternative:** EU-Reach automatisch per API ziehen — verworfen, weil empirisch **nicht im
  MCP-Payload** (§1), nur ueber die Snapshot-Seite manuell/Vision erreichbar.
- **Betroffene Module:** `creative_studio/ad_library_scan.py` (Erweiterung), Vault-Note (Output), neue Tests.

## Technische Hinweise
- `surface: backend`. EU-Reach ist die einzige offizielle kommerzielle Budget-Annaeherung — aber pro Ad ein
  manueller Oeffnen-Schritt; sauber als „semi-quantitativ, manuell" kennzeichnen.
- Vault-Note folgt Obsidian-Konvention (Frontmatter/Wikilinks/Callouts, ggf. Bases) — bei `.md`/`.base` im
  Vault den `obsidian-markdown`/`obsidian-bases`-Skill vorher laden (globale Bootstrap-Regel).
- Voraussetzung: SKILL-052 (Scan-Modul).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/ad_library_scan.py` — `enrich_snapshot()`, `append_hook_library()`.
- `skills_sources/creative-studio/tests/test_skill_053_snapshot_hooklib.py` (neu).
- Wissensgrundlage: `2026-06-24_meta-ad-library-zugriff-budget.md` (§1, §2, §4, §6 Should).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
