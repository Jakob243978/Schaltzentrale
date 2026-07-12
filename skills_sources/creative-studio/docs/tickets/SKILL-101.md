# SKILL-101: creative-studio — Human-Messaging-Voice-Direktive (Workshop 03 How You Sound) fuer Ad-Copy

**Status:** spec
**Erstellt:** 2026-07-12
**MoSCoW:** Must
**Geschaetzter Aufwand:** M (Copy-Regeln in SKILL.md + Playbook verankern; Vorpruef-Checks als Warnungen)
**surface:** docs (+ optional code: Copy-Linter-Warnungen)
**vision_principle:** skill-muss-multi-projekt-tauglich (Voice ist Parameter/Brand, nicht hartkodiert)
**outcome_metric:** ad_copy_klingt_menschlich_zugewandt + kein_angst_frame + kein_ki_buzz + wachstums_frame

## Kontext / Root-Cause
Beim Agentic-Messaging-Test (2026-07-12) war die erste Copy-Runde **zu generisch/„KI-typisch"**
und verstiess gegen Jakobs Voice aus dem Brand-Workshop **Step 03 · How You Sound**. Jakob-Feedback
(mehrere Nachrichten, an konkreten Ads belegt):
- a08 „Die ersten Wochen sind mehr Arbeit" → **Angst-/Negativ-Lead**, verstoesst gegen 03.3/03.8.
- a03 „gleiche Mannschaft, doppelt geschafft" → **Marketing-Floskel**, nicht Kundensprache.
- a09 „Zahllauf: 3 Stunden zurueck" → **kein logischer, vollstaendiger Satz**.
- Topline benannte die Zielgruppe („FUER MAKLER") → **schraenkt Ausstrahlung ein**.
- „KI" ist **verbranntes Branchen-Wording** → nur gekonnt/sparsam einsetzen.
- Copy soll **menschlich zugewandt** klingen, wie **Jakob im echten Gespraech ZUR Zielgruppe**.

## Was soll erreicht werden?
Jede Ad-/Reel-Copy folgt **verbindlich** der Voice aus Workshop 03 (Quelle:
`brand/Agentic KI Brand/Workbook/Jakob-Brand-Workshop.html`, Slides 03.1-03.10). Der Skill
kodiert das als Copy-Direktive (projektneutral: die konkreten Voice-Adjektive/Leitplanken kommen
aus der Brand, nicht hartkodiert).

## Akzeptanzkriterien (EARS)
- [ ] **EARS-1 [Must, Emotionsraum statt Angst (03.3/03.8)]:** Keine Angst-/Pain-/Verlust-Leads.
      Jede Aussage nach vorne gedreht: Wachstum, Freiheit, Begeisterung. Verboten: „wenn du jetzt
      nicht …", „du verlierst …", Negativ-Opener.
- [ ] **EARS-2 [Must, Wachstums-Frame (03.8)]:** Verkauft wird **Verdopplung/Wachstum/Freiheit**,
      nicht Entlastung-als-Opfer. Entlastungs-Nutzen wird Richtung Wachstum/Freiheit geframt.
- [ ] **EARS-3 [Must, Klingt-nach/NICHT-nach (03.2)]:** klingt nach *direkt, energetisch,
      motivierend, klar, nahbar, mutig*; NICHT nach *Angst, Buzzwords, belehrend, Toolnamen-Dropping*.
- [ ] **EARS-4 [Must, Sprach-Leitplanken (03.8)]:** immer „du"/Unternehmer/Kunde, **nie
      „Geschaeftsfuehrer"**; **nie „komplizierter" → „individueller"**; **keine Tool-Namen**.
- [ ] **EARS-5 [Must, „KI" sparsam]:** Der verbrannte Begriff „KI" wird in On-Image-Copy weitgehend
      vermieden; stattdessen **zeigen, was passiert** (Playbook §1 Regel 2: „Zeig, erklaer nicht").
- [ ] **EARS-6 [Must, menschliche Phonetik]:** Gesprochene, zugewandte Sprache (Jakob ZUR
      Zielgruppe); Kontraktionen erlaubt; **keine KI-typischen Triaden/Floskeln** („gleiche
      Mannschaft, doppelt geschafft" u.ae. verboten); Kundensprache aus der Voice-of-Customer.
- [ ] **EARS-7 [Must, Copy-Dramaturgie]:** **Topline = Auftakt/Setup** (kein Zielgruppen-Label,
      haelt Ausstrahlung breit); **Headline = der „Boom"/die Aufloesung** als vollstaendiger,
      logischer Satz; **Subline = der Mehrwert** im Alltag. Ich-Perspektive (Jakob) als Option.
- [ ] **EARS-8 [Should, Repeatable Pitch (03.4)]:** Primaertexte folgen Hook → Tension →
      Resolution → Proof → Ask (Hormozi), Beweis = Jakobs eigener Betrieb verdoppelt.
- [ ] **EARS-9 [Should, projektneutral]:** Voice-Adjektive/Leitplanken/VoC bleiben Brand-Parameter
      /Doku; kein Projektwert in `creative_studio/*` hartkodiert.

## Loesungs-Skizze
- SKILL.md Abschnitt 9 („Anwenden") + Playbook um den verbindlichen Voice-Block (03.2/03.3/03.8)
  erweitern; Verweis auf die Workshop-Slides als Brand-Quelle.
- Optional Code: `content.content_structure_warnings()` um Warnungen ergaenzen
  (Angst-/Negativ-Opener erkannt; „KI"-Dichte hoch; unvollstaendiger Headline-Satz; Floskel-Liste).
- Referenz-Instanz: `AgentischesArbeiten/marketing/ad-creatives/messaging-test-2026-07/` (Copy v2).

## Test-Ergebnis / Beleg
- Offen (spec). Abnahme visuell an der Referenz-Instanz + Jakob-Review der Copy.

## Code-Referenzen
- `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md` (§1, §2)
- `SKILL.md` Abschnitt 9
- Brand-Quelle: `AgentischesArbeiten/brand/Agentic KI Brand/Workbook/Jakob-Brand-Workshop.html` (03.1-03.10)
