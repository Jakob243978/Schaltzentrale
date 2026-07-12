# SKILL-049: creative-studio — Content-Marktrecherche-Runbook (Tier 0, WebSearch-getrieben)

**Status:** review
**Erstellt:** 2026-06-24
**MoSCoW:** Must
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_content-market-research-methodik.md` (§4 Methodik-Pipeline, §5 Andockbarkeit, §6 MoSCoW Must)

> [!info] Herkunft (Recherche 2026-06-24)
> Der Skill ist heute strikt **produktionsseitig** — er nimmt fertigen Content (`--headline`/`--subline`/
> `--cta`/`--eyebrow`) und rendert. Es fehlt eine **vorgelagerte Ideen-/Recherche-Stufe**. Dieses Ticket
> fuellt die Luecke mit einem **Runbook/Sub-Command „Content-Marktrecherche"**, dessen Output exakt die
> Input-Felder von `render_image`/`--props` speist — **Tier 0** (gratis, WebSearch/WebFetch-getrieben,
> **kein API-Key**). Sauberste Verortung: SKILL.md-Abschnitt + Markdown-Template, **kein** Eingriff in
> `specs.py`/Render-Pfad (§5).

## Was soll erreicht werden? (Business-Ziel)
Ein wiederholbarer 6-Schritte-Ablauf (Sammeln → Clustern → Funnel-Mapping → Priorisieren → Idee→Hook→Format
→ Output-Liste), der aus einem Seed-Thema eine **priorisierte Themen-/Hook-/Format-Liste mit Quellen**
erzeugt, die 1:1 in die Creative-Generierung fliesst. Tier 0 braucht keinen API-Key.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When der Skill mit Seed-Thema + Tier 0 ausgefuehrt wird, the system shall eine priorisierte
      Themen-/Hook-/Format-Liste mit **≥ 1 zitierter Quelle pro Eintrag** erzeugen — **ohne externen API-Key**.
- [ ] **EARS-2:** When der Ablauf laeuft, the system shall die sechs Schritte (Sammeln/Clustern/Funnel-Mapping/
      Priorisieren/Idee→Hook→Format/Output-Liste) deterministisch in dieser Reihenfolge abarbeiten (Runbook).
- [ ] **EARS-3:** When ein Hook formuliert wird, the system shall den DACH-Coaching-Claim-Check
      (`creative-studio` Coaching-/UWG-Warnung, SKILL-026) anwenden — keine „Du wirst…"-Versprechen.
- [ ] **EARS-4:** When die Output-Liste erzeugt wird, the system shall sie als Markdown-Tabelle
      `Thema | Funnel | Idee | Hook | Format | Prioritaet | Quellen` ausgeben (optional zusaetzlich als JSON,
      dessen Felder `render_image`-Args/Video-`--props` speisen).
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall Seed-Thema
      + optionalen Brand-Kontext als Eingabe nehmen — **kein** hartkodierter Projektwert im Runbook/Template.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** **Reine Doku-/Runbook-Arbeit** — neuer Abschnitt „8. Content-Marktrecherche" in
  `SKILL.md` + `templates/content_research.md` (Agenten-Runbook, WebSearch/WebFetch-getrieben). **Kein**
  Python-Code, **kein** Eingriff in `specs.py`/Render-Pfad (§5). Output-Tabelle ist der Uebergabe-Vertrag
  zur Creative-Generierung.
- **Verworfene Alternative:** Sofort ein `research.py` mit API-Helpern bauen — verworfen, weil Tier 0
  ohne Key 80 % des Erkenntniswerts liefert (§3) und der API-Baustein bewusst SKILL-050 (Should) ist.
- **Betroffene Module:** `SKILL.md` (neuer Abschnitt), `templates/content_research.md` (neu). Kein Code.

## Technische Hinweise
- `surface: backend` (Doku/Runbook, kein Web-UI). Quellen Tier 0: Google Trends (UI/Fetch), YouTube-
  Autocomplete, PAA-Fragen, 3–5 Reddit/LinkedIn-O-Toene — je mit Quelle+Datum.
- Priorisierung: Volumen × Relevanz × (1/Wettbewerb) + Social-Resonanz, 1–3-Skala (§4 Schritt 4).
- Bewusst **billiger MUST**: sofort umsetzbar wie SKILL-049 ist reine Markdown-/SKILL.md-Arbeit.

## Code-Referenzen
- `skills_sources/creative-studio/SKILL.md` — neuer Abschnitt „8. Content-Marktrecherche".
- `skills_sources/creative-studio/templates/content_research.md` (neu) — 6-Schritte-Agenten-Runbook.
- Wissensgrundlage: `2026-06-24_content-market-research-methodik.md` (§4, §5, §6 Must).

## Ergebnis / Notizen

**Umgesetzt 2026-06-24 (Status -> review, Verify-Gate offen). Reine Doku, KEIN Code.**

Artefakte:
- `templates/content_research.md` (neu) — der vollstaendige 6-Schritte-Tier-0-Runbook
  (Eingabe-Tabelle, Schritte Sammeln/Clustern/Funnel-Mapping/Priorisieren/Idee->Hook->Format/
  Output-Liste, Output-Vertrag mit Markdown-Tabelle + optionalem JSON-Feld-Mapping auf
  `render_image`-Args/Video-`--props`, Guardrails inkl. DACH-Coaching-Claim-Check, Quellen-Tiers).
- `SKILL.md` — neuer Abschnitt „8. Content-Marktrecherche (Tier 0, vorgelagert)".

KEIN Eingriff in `specs.py`/Render-Pfad (wie spezifiziert).

Done-Kriterien (EARS):
- [x] EARS-1: priorisierte Themen-/Hook-/Format-Liste mit >= 1 Quelle pro Eintrag, ohne API-Key
      (Output-Vertrag + Guardrail dokumentiert).
- [x] EARS-2: sechs Schritte deterministisch in fester Reihenfolge (Runbook).
- [x] EARS-3: DACH-Coaching-Claim-Check (SKILL-026 `compliance_warnings()`) bei Hook-Formulierung.
- [x] EARS-4: Output als Markdown-Tabelle `Thema | Funnel | Idee | Hook | Format | Prioritaet | Quellen`
      (+ optional JSON, das die Creative-Inputs speist).
- [x] EARS-5: Seed-Thema + optionaler Brand-Kontext als Eingabe, kein hartkodierter Projektwert.

Hinweis: Doku-Ticket ohne automatischen Test — Verify per Inhalts-Review der beiden Doku-Files.
