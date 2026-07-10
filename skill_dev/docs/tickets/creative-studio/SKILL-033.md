# SKILL-033: creative-studio — Reporting-Rueckkanal (Insights → Winner-Flag via manifest-IDs)

**Status:** idea
**Erstellt:** 2026-06-23
**MoSCoW:** Could
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** performance_je_variante_zurueckgeordnet (ads_insights_* ↔ manifest variant_id/utm_content) + gewinner_automatisch_geflaggt (95 % / ≥50 Conv.)
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_creative-studio-flow-improvements.md` (§2.5 Messung & Iteration, §3.7 Reporting-Rueckkanal; MoSCoW-Liste #8)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> Heute gibt es **keinen** Rueckkanal aus den Performance-Daten — der Loop ist offen. Best Practice:
> Insights-Pull (`ads_insights_*`) ordnet Performance ueber dieselbe `variant_id`/`utm_content`-Konvention
> aus dem `manifest.json` zu und flaggt Gewinner. Winner-Schwellen: ~95 % Confidence und ≥ 50 Conversions/
> Variante; Sekundaer-Metriken (Thumb-Stop-Rate, Watch-Time) statt nur CTR. Abhaengig von SKILL-023/024.

## Was soll erreicht werden? (Business-Ziel)
Ein optionales Reporting-Modul, das per Insights-Pull (`ads_insights_*`) die Performance ueber
`variant_id`/`utm_content` aus dem `manifest.json` den Varianten zuordnet, Sekundaer-Metriken je Variante
aggregiert und Gewinner nach Schwellen flaggt — schliesst den Creative-Loop. Projektneutral.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein Insights-Datensatz (`ads_insights_*`) vorliegt, the system shall ihn ueber
      `variant_id`/`utm_content` den Varianten im `manifest.json` zuordnen.
- [ ] **EARS-2:** When eine Variante ~95 % Confidence **und** ≥ 50 Conversions erreicht, the system shall sie
      als **Gewinner** flaggen.
- [ ] **EARS-3:** When Performance ausgewertet wird, the system shall **Sekundaer-Metriken** (Thumb-Stop-Rate,
      Watch-Time) je Variante mit ausweisen — nicht nur CTR.
- [ ] **EARS-4:** When eine Variant-ID aus dem Manifest in den Insights nicht auffindbar ist, the system
      shall das als Lueck-/Mismatch-Warnung melden (Naming-Bruch sichtbar machen, nicht still ignorieren).
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall den
      Rueckkanal projektneutral halten (Schwellen als Parameter, Ad-Account/Pull-Quelle als Config).

## Technische Hinweise
- Abhaengig von SKILL-023 (Manifest) + SKILL-024 (Naming) — daher `idea`/Could. Teils beim Ads-Agent
  verortbar; dieser Skill liefert die ID-Bruecke + Auswertungs-Logik.
- `creative_studio/reporting.py`: Insights-JSON + Manifest → Auswertung + Winner-Flags. Der eigentliche
  Insights-Pull kann ueber den Meta-MCP (`ads_insights_*`) laufen; das Modul konsumiert das Ergebnis.
- Schwellen (95 % Confidence / ≥ 50 Conv.) als Default-Parameter, ueberschreibbar.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/reporting.py` — **neu** (Insights ↔ Manifest → Winner-Flag).
- `skills_sources/creative-studio/creative_studio/batch.py` — `manifest.json`-Quelle (SKILL-023).
- `skills_sources/creative-studio/creative_studio/specs.py` — `variant_id`/`utm_content` (SKILL-024).
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_creative-studio-flow-improvements.md` (§2.5, §3.7).

## Ergebnis / Notizen
_(wird beim Abschließen befüllt)_
