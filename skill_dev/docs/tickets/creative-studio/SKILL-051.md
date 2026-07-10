# SKILL-051: creative-studio — GSC-Anbindung + Google-Trends-Alpha-API (vorgemerkt, blockiert)

**Status:** spec
**Erstellt:** 2026-06-24
**MoSCoW:** Could
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_content-market-research-methodik.md` (§2.1 Google Trends, §2.2 GSC, §3 Stufe 2, §6 MoSCoW Could)

> [!info] Herkunft (Recherche 2026-06-24)
> Tier 2 des Recherche-Ablaufs (eigene realisierte Nachfrage + frueher Trend-Zugang). **Beide Quellen sind
> heute blockiert:** GSC braucht eine Domain mit Traffic (existiert noch nicht), die Google-Trends-Alpha-API
> ist Waitlist-/Antrags-gegated. Das Ticket haelt den Anbindungs-Plan fest, damit er bei Verfuegbarkeit
> sofort umgesetzt werden kann — bewusst **Could**, nicht jetzt umsetzbar.

## Was soll erreicht werden? (Business-Ziel)
Vorgemerkter Anbindungs-Plan: Sobald eine LP/Domain mit Traffic existiert, GSC **Search Analytics API**
(`searchanalytics/query`) via OAuth-Service-Account **oder** GSC-MCP anbinden (Content-Gap + Intent-Gap aus
echter Nachfrage; Pflicht **API statt UI**, da die UI bei 1.000 Zeilen deckelt / ~75 % Impressionen filtert).
Parallel: Google-Trends-Alpha-API beantragen, bis dahin Apify-Trends-Actor als Bruecke evaluieren.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When eine GSC-Property mit Traffic verfuegbar ist, the system shall echte Queries +
      Content-Gap (Position > 20) + Intent-Gap ueber die **Search Analytics API** (unsampled, nicht UI) ziehen.
- [ ] **EARS-2:** When GSC angebunden wird, the system shall OAuth-Credentials **aus Env/Service-Account**
      beziehen — kein Key im Code, kein Projektwert (multi-projekt). Alternativ GSC-MCP, falls im Stack.
- [ ] **EARS-3:** When die Google-Trends-Alpha-API freigeschaltet ist, the system shall Rising-/Breakout-
      Queries strukturiert ziehen; bis dahin shall ein Apify-Trends-Actor als dokumentierte Bruecke gelten.
- [ ] **EARS-4:** When weder GSC-Property noch Trends-Alpha-Zugang vorhanden sind, the system shall klar als
      **blockiert** dokumentieren und auf Tier 0/1 (SKILL-049/050) verweisen — kein Crash, kein Silent-Fake.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Heute **nur Plan + Doku-Eintrag** (Could, blockiert). Bei Freischaltung: `research.py`
  (SKILL-050) um GSC-/Trends-Quellen erweitern, OAuth via Service-Account/Env. Bis dahin kein Code.
- **Verworfene Alternative:** pytrends (archiviert/read-only, 429-Limits) als Dauerlosung — verworfen
  (fragil, §2.1). Apify-Actor nur als Uebergangs-Bruecke.
- **Betroffene Module:** spaeter `creative_studio/research.py` (Quellen-Erweiterung); jetzt SKILL.md-Notiz
  (Tier 2, blockiert).

## Technische Hinweise
- `surface: backend`. **Externe Kosten/Zugang:** GSC kostenlos (aber Domain noetig), Trends-Alpha Antrag,
  Apify pay-per-query — Aktivierung erst nach Owner-Entscheidung + verfuegbarer Domain.
- Blocker: keine Live-Domain mit Traffic (Stand 2026-06-24). Re-Trigger, sobald LP/Warteliste live Traffic hat.

## Code-Referenzen
- `skills_sources/creative-studio/SKILL.md` — Tier-2-Notiz (blockiert) im Recherche-Abschnitt.
- `skills_sources/creative-studio/creative_studio/research.py` — spaetere GSC-/Trends-Quellen (bei Freischaltung).
- Wissensgrundlage: `2026-06-24_content-market-research-methodik.md` (§2.1, §2.2, §3 Stufe 2, §6 Could).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt — blockiert bis Domain live + Trends-Alpha-Zugang)_
