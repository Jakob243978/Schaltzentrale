# Governance-Log — Skill "creative-studio"

Alle autonomen Entscheidungen + Verifier-Pass-Log fuer diesen self-contained Skill.
Neueste Eintraege oben.

## 2026-07-13 — Upstream-Merge: Sandis Ad-Messaging-Ebene uebernommen (SKILL-088..104)
**Herkunft:** `customer/sandi` (Sandis self-contained Weiterentwicklung des zu ihr per
Datei-Spiegel ausgerollten Skills; Review-Ablage `Schaltzentrale/_incoming/sandi/creative-studio/`).
**Entscheidung:** Sandis Upstream-Beitrag (Ad-Messaging-Ebene, 17 Tickets SKILL-088..104,
9 neue Test-Dateien, 2 neue Doks: `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md`
+ `docs/templates/ad-copy-sheet.md`) additiv in die Source gemergt. Merge folgt dem
Upstream-Review-Flow aus PROJECT_VISION/CLAUDE.md (Kunde legt eigene SKILL-Tickets an,
Original-Maintainer reviewt + uebernimmt).
**Merge-Analyse:** Sandis Basis == aktueller Source-Stand (inkl. SKILL-087). Alle 8 geaenderten
Kern-Dateien (SKILL.md, content.py, frameworks.py, render_image.py, specs.py, governance_log.md,
CHANGELOG.md, test_skill_085) sind rein additive Erweiterungen — 0 zerstoererische Removals
(SKILL.md 0 entfernt/51 ergaenzt; SKILL-087-Gedankenstrich-Validator `check_no_emdash`/`dash_warnings`
in specs.py + der `dash_warnings`-Aufruf in content.py **erhalten**). Ticket-Nummern 088..104 waren
in der Source frei (Bestand 020..087). Einzige Nicht-rein-additive Stelle: `test_skill_085`
(eine bestehende Assertion `keys == ["aida"]` -> `"aida" in keys` + `"scene" in keys`), bewusst
angepasst, weil `match_frameworks` durch die neuen Cold-Audience-Formeln (SKILL-089) mehr Treffer
liefert — legitim, kein Regressions-Verlust.
**Test:** `python -m pytest -q` in der Source -> **429 passed, 0 failed** (inkl. Sandis 9 neuer Tests).
**ADR:** keins (additive Encodierung im bestehenden Framework-/Validator-Muster).
**Review:** Jakob (finaler PO) — Merge ausgefuehrt durch Subagent, Jakob prueft/committet.
**Offen:** inhaltliche Ueberlappung Sandis Ad-Messaging (089..104) mit den Baulig-Frameworks
(SKILL-081..086) noch nicht konsolidiert; SKILL-097/099 bleiben `spec` (offen).

## 2026-07-12 — Ad-Messaging testbar encodiert (SKILL-089..099)
**Ticket:** SKILL-089 (review), SKILL-090 (review), SKILL-091 (review), SKILL-092 (review),
SKILL-093 (review), SKILL-094 (review), SKILL-095 (review), SKILL-096 (review),
SKILL-098 (review); SKILL-097 (spec), SKILL-099 (spec).
**Entscheidung:** Den vollstaendigen Ad-Messaging-Insight-Satz aus dem Playbook (SKILL-088)
als SDD-Ticket-Cluster erfasst (je Insight-Cluster >= 1 Ticket, SKILL-091..099) und die
implementierbaren Teile projektneutral + testbar encodiert:
- **089/091:** 6 Cold-Audience-Hook-Formeln (F1-F6) als CopyFrameworks + `COLD_AUDIENCE_FORMULAS`;
  `match_frameworks(traffic="cold")` rankt Szenen-Formeln zuerst; 8 Human-Rules als
  `human_messaging_rules()` + `human_rule_warnings()` (Statistik-Opener/Consultant-Abstrakta/
  Begriff-zuerst).
- **090:** `load_messaging_doc()` + `build_analysis_prompt(messaging_doc=...)` (Projekt-VoC als
  Parameter); Human-/Brand-Voice-/Hype-Warnungen in Bild- (`AdContent.warnings`) + Reel-Flow
  (`content_structure_warnings`) eingehaengt; neue `AdContent`-Felder `category_term`/`forbidden_tools`.
- **092:** `brand_voice_warnings()` (keine Tool-Namen, kein Preis, kein FOMO, „individueller"
  statt „kompliziert", nie „Geschaeftsfuehrer").
- **093:** `apply_value_translations()` + `FEATURE_LEVEL_VERBS`.
- **094:** `CTA_LIBRARY` (button/hart/weich) + `get_ctas`/`cta_category`.
- **095:** `TONE_PROFILES` (buyer/champion) + `get_tone_profile`.
- **096:** `anti_hype`-Formel + `hype_warnings()`.
- **098:** `visual_cliche_warnings()` (Anti-KI-Klischee im Motiv-Prompt).
- **097 (spec):** VoC als versioniert erweiterbares Datenformat (offen). **099 (spec):**
  Modell-Ads/Vorher-Nachher als projekt-spezifisches Referenzmaterial (offen).
**Begruendung:** Erkenntnisse sollen der Skill beim Ad-Bauen automatisch anwenden (nicht nur
dokumentiert). Prinzip `skill-muss-multi-projekt-tauglich` gewahrt: KEIN Projektwert im Code —
Fachbegriff/Tool-Namen/VoC/Palette kommen als Parameter/Datei; projekt-spezifisches bleibt Doku.
**Betroffene Dateien:** creative_studio/frameworks.py, creative_studio/specs.py,
creative_studio/content.py, SKILL.md, docs/tickets/SKILL-089..099.md,
tests/test_skill_089..098_*.py (7 neue Test-Dateien).
**Test:** `python -m pytest tests/ -q` -> **426 passed, 3 skipped** (Bestand 363 -> +63 Tests).
**ADR:** keins (additive Encodierung im bestehenden Framework-/Validator-Muster, kein Architektur-Wechsel).
**Review:** ausstehend (Jakob)

## 2026-07-12 — Ad-Messaging-Erkenntnisse konsolidiert (SKILL-088..090)
**Ticket:** SKILL-088 (review), SKILL-089 (spec), SKILL-090 (spec)
**Entscheidung:** Alle Ad-Messaging-Erkenntnisse aus dem AgentischesArbeiten-Brand-Workshop
(zwei Analyse-Subagenten: Ad-Critique gegen den echten Meta-Ad-Report + Voice of Customer aus
echten Kundengespraechen Beyer + Weist) in EINE ad-framework-Doku konsolidiert
(`docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md`): 8 Human-Messaging-Regeln
(kalte Zielgruppe), 5-Schritte-Hook-Bauplan + 6 Hook-Formeln, VoC-Bibliothek (2 Kunden +
bestaetigte kundenuebergreifende Muster), Ad-Daten-Muster, Baukasten, Modell-Ads.
Follow-ups: Formeln/Regeln testbar in `frameworks.py` encodieren (089), Projekt-VoC +
Human-Rule-Check in den Copy-Flow einhaengen (090).
**Begruendung:** User-Feedback „Flickenteppich, keine easy-to-use Hook-Ressource" → eine
konsolidierte, nachvollziehbare, wiederverwendbare Ressource im Skill statt verstreuter
Post-its im Booklet. Reusable Regeln projektneutral, Projekt-VoC als Instanz gekennzeichnet.
**Betroffene Dateien:** docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md (neu),
docs/tickets/SKILL-088.md, SKILL-089.md, SKILL-090.md.
**ADR:** keins (Doku + Backlog-Tickets; testbare Encodierung folgt in 089/090).
**Review:** ausstehend (Jakob)

## 2026-07-12 — Dezentralisierung: Skill wird self-contained SDD+PO-Projekt
**Ticket:** kein Ticket (Struktur-Migration, Architektur-Umbau durch Subagent)
**Entscheidung:** Der Skill "creative-studio" bekommt eine eigene SDD+PO-Initialisierung
(PROJECT_VISION, sdd-config, po-config, tickets/, adr/, governance_log, CHANGELOG,
ROADMAP, CLAUDE.md). Die bisher zentral in `skill_dev/docs/tickets/creative-studio/` liegenden
SKILL-Tickets wurden per `git mv` hierher (`docs/tickets/`) migriert; Ticket-IDs
(SKILL-NNN, global eindeutig) unveraendert.
**Begruendung:** Jeder Skill soll eigenstaendig an Kunden ausrollbar sein und von
diesen mit eigenem SDD/PO weiterentwickelt werden koennen (Upstream-Review-Flow).
Zentrale Entwicklung in `skill_dev/` skaliert nicht auf Kunden-Rollout.
**Betroffene Dateien:** docs/PROJECT_VISION.md, docs/sdd-config.yaml,
docs/po-config.yaml, docs/DEFERRED.md, docs/po-outcomes.md, docs/governance_log.md,
docs/adr/, docs/tickets/ (migriert), CHANGELOG.md, ROADMAP.md, CLAUDE.md.
**ADR:** keins (reine Struktur-Migration; inhaltliche Skill-ADRs kommen ins docs/adr/)
**Review:** ausstehend (Jakob)
