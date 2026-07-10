# ROADMAP — Skill-Entwicklung

Geplante SKILL-Tickets, sortiert nach MoSCoW + Vision-Prinzip-Match.
Diese Datei ist **nicht** Ground-Truth — die `docs/tickets/SKILL-NNN.md`
sind es. Hier nur Uebersicht fuer Sprint-Planung + Status-Check.

---

## Must

| Ticket | Titel | Status | Vision-Prinzip |
|---|---|---|---|
| SKILL-001 | PO-Skill bauen (Schaltzentrale) + Init in Immobewertung | review (Implementierung in T080 erfolgt, Verifier-Pass + Outcome offen) | `skill-muss-multi-projekt-tauglich-sein` + `dogfood-zwingt-qualitaet` |
| SKILL-005 | Skill-Versions-Anker (rollbar-zu-v0.4 vor Pre-Condition-Einbau) | spec — Voraussetzung fuer SKILL-004/006 | `dogfood-zwingt-qualitaet` + `skill-schlanker-als-was-er-ersetzt` |
| SKILL-004 | EARS-Pre-Conditions als Pflicht im SDD-Ticket-Template + Verifier-Check | spec — wartet auf SKILL-005 done | `lessons-aus-live-use-zurueckfuehren` + `dogfood-zwingt-qualitaet` |
| SKILL-023 | **creative-studio**: Batch-/Varianten-Engine (N Hooks × M Formate × Bild/Video) + manifest.json | spec — Kern-Klammer fuer DCO + Reporting | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-024 | **creative-studio**: Variant-ID- & UTM-Systematik in specs.py (Naming-Single-Source) | spec — Voraussetzung fuer SKILL-023/031/033 | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-036 | **creative-studio**: make_url_tags() (+make_link_url-Fallback) in specs.py — UTM + Meta-Makros als Single Source | spec — Voraussetzung fuer SKILL-037 | `skill-muss-multi-projekt-tauglich-sein` |

## Should

| Ticket | Titel | Status | Vision-Prinzip |
|---|---|---|---|
| SKILL-002 | Refactor T078/T079 in PO-Skill (Vision↔Features-Bridge generalisieren) | spec — wartet auf T078+T079 done in Immobewertung | `skill-muss-multi-projekt-tauglich-sein` + `lessons-aus-live-use-zurueckfuehren` |
| SKILL-003 | Anti-Pattern "Iterative Artefakt-Generierung" + Implementer-Hygiene | spec | `lessons-aus-live-use-zurueckfuehren` + `skill-schlanker-als-was-er-ersetzt` |
| SKILL-006 | KNOWN_FAILURES.md als Pflicht-Datei + Bootstrap-Eintrag (Living Runbook) | spec — parallel zu SKILL-004 bearbeitbar (Jakob-Entscheidung 2026-05-26) | `lessons-aus-live-use-zurueckfuehren` + `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-007 | Reveal-Presentation Skill: Visual-Review-Step nach Build (Chromium-Screenshot-Pass) | spec — unabhaengig bearbeitbar (anderer Skill als agile-sdd) | `lessons-aus-live-use-zurueckfuehren` + `dogfood-zwingt-qualitaet` |
| SKILL-009 | inbox/-Konvention fuer agile-sdd (menschliches Eingangs-Material) | review (umgesetzt 2026-05-31, bumpt agile-sdd v0.4 → v0.5; Verifier-Pass + setup.ps1-Deploy offen) | `lessons-aus-live-use-zurueckfuehren` |
| SKILL-020 | **creative-studio**: Grundgeruest + Bild-Modul (Playwright/HTML-CSS, Safe-Zones, Multi-Format) | spec — Erst-Einsatz AgentischesArbeiten (Warteliste-Ads) | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-021 | **creative-studio**: Video-Modul (Remotion, 9:16 + Multi-Format) | idea — Ausbaustufe nach SKILL-020 | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-012 | agile-sdd-skill Verifier: Visual-UI-Check (Playwright, Screenshots + Console-Errors) | spec — Phase 1 (Spec + Skeleton) done am 2026-06-02; Phase 2 (Full-Impl + Smoke-Run) offen; Phase 3 (Visual-Regression) optional | `lessons-aus-live-use-zurueckfuehren` + `dogfood-zwingt-qualitaet` |
| SKILL-025 | **creative-studio**: frameworks.py (Copy-Framework-Katalog + Hook-Bibliothek + 4U-Validator) | spec — Copy-Pendant zu specs.py, projektneutral | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-026 | **creative-studio**: DACH-Compliance-Guard ausbauen (UWG/HWG-Heuristik + Ad↔LP-Message-Match) | spec — nur Warnungen, keine harte Sperre | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-027 | **creative-studio**: Voiceover-Layer (ElevenLabs-Voice-Clone + Untertitel ueber Remotion) | spec — Key via Env, ohne Re-Architektur | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-028 | **creative-studio**: KI-Disclosure-Gate („KI"-Label + C2PA/Metadaten auf KI-Creatives) | spec — EU-AI-Act + Meta-Policy ab 02.08.2026 | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-029 | **creative-studio**: Brand-Kit als brand.json (Token-Rollen + Logo-Handling) | spec — ergaenzend/ersetzend zu branding.env | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-030 | **creative-studio**: Vorschau-Galerie gallery.html (QA-Gate vor Launch) | spec — liest manifest.json, file://-tauglich | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-037 | **creative-studio**: url_tags am Ad-Objekt setzen + ins manifest.json (batch.py, Live-Verifikation + link_url-Fallback) | spec — wartet auf SKILL-036 done | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-038 | **creative-studio**: UTM-Naming-Standard als Konstanten (UTM_*/META_MACROS) + pytest | spec — sichert SKILL-036/037 gegen Naming-Drift | `skill-muss-multi-projekt-tauglich-sein` |

## Could

| Ticket | Titel | Status | Vision-Prinzip |
|---|---|---|---|
| SKILL-031 | **creative-studio**: DCO-/Asset-Feed-Export-Modus (dco_bundle.json fuer Advantage+) | idea — abhaengig von SKILL-023/024 | `skill-muss-multi-projekt-tauglich-sein` |
| SKILL-032 | **creative-studio**: content-aware smartcrop fuer --bg-image (loest EARS-6 aus SKILL-020) | idea — relevant sobald Foto-Hintergruende | `lessons-aus-live-use-zurueckfuehren` |
| SKILL-033 | **creative-studio**: Reporting-Rueckkanal (Insights → Winner-Flag via manifest-IDs) | idea — abhaengig von SKILL-023/024 | `skill-muss-multi-projekt-tauglich-sein` |

### Could (offene Ideen, noch keine SKILL-Tickets)

- **operator-templates-Skill formal aufsetzen** — heute teils unter
  `~/.claude/skills/operator-templates/` aktiv, aber kein eigenes
  `skills_sources/operator-templates/`-Repo. Nach Bedarf SKILL-Ticket
  anlegen sobald mehrere Templates dort landen.
- **SDD-Skill: Verifier-Subagent-Caching** — wenn Verifier in jeder
  Session frisch SKILLS_VISION + Ticket-Spec liest, kommt redundanter
  Read-Overhead. Nur sinnvoll wenn Subagent-Calls > 5 Min werden.
- **PO-Skill: Outcome-Auto-Tracking** — heute manuell via
  `/po-verify-outcome`. Anti-Pattern: Auto-Tracking kann den User
  abstumpfen lassen. Bleibt bewusst manuell.

## Wont (explizit nicht)

- **Eigener Skill-Marketplace / Public-Sharing** — siehe SKILLS_VISION.md
  "Was NICHT im Scope ist".
- **Auto-Discovery via LLM-Klassifizierung** — Skills bleiben
  deterministisch aktiviert. Siehe globale CLAUDE.md
  "Skill-Bootstrap-Regel".

---

## Naechster Sprint-Vorschlag

1. Jakob: SKILLS_VISION.md review + schaerfen wo noetig.
2. Jakob: setup.ps1 ausfuehren (deployt nach `~/.claude/skills/`)
   — falls noch nicht passiert.
3. SKILL-001 Verifier-Pass ausstehend (falls Status `review`):
   `/sdd-verify SKILL-001`.
4. **NEU 2026-05-26 (Knowledge-Persistence-Recherche + Jakob-Update):**
   - SKILL-005 (Versions-Anker) zuerst — XS, blockt nichts ausser SKILL-004/006.
     `docs/skill-versions.md` ist bereits initial befuellt (v0.4-Anker
     `fe9337a`); offen: Smoke-Test-Erweiterung + optional Git-Tag durch Jakob.
   - **SKILL-004 (Pre-Conditions als Sektion, Warning-only)** — M,
     strukturell wichtige Aenderung. Bumpt agile-sdd v0.4 → v0.5.
     **Kein Strict-Mode geplant** (Jakob-Entscheidung 2026-05-26):
     Pre-Conditions bleiben dauerhaft Warning, kein Hard-Block.
   - **SKILL-006 (KNOWN_FAILURES.md)** — jetzt `spec`, **parallel zu
     SKILL-004 bearbeitbar** (Jakob-Entscheidung 2026-05-26). Wirkt
     unabhaengig, kein Warten auf SKILL-004-Outcome noetig.
5. SKILL-002 abwarten, bis T078/T079 in Immobewertung done sind.
6. SKILL-003 (Implementer-Hygiene) kann sofort angegangen werden —
   Pattern-Datei + Memory-Save sind kleine Stueck-Arbeit.
7. **NEU 2026-05-27 (BeyerImmo-Onboarding-Live-Schmerz):**
   - SKILL-007 (Reveal Visual-Review-Pass) — Should, M-Aufwand.
     Unabhaengig vom agile-sdd-Skill bearbeitbar (anderer Skill-
     Source), kein Blocker. Optional: reveal-presentation v0.1-
     Anker in `docs/skill-versions.md` als Vorgriff anlegen.
