# DEFERRED.md — Geparkte Skill-Ideen (skill_dev)

Ideen, die `/po-challenge` durchlaufen haben aber im 48h-Cooldown sind
oder zu vage formuliert waren, um direkt in den SDD-Flow uebergeben zu
werden.

**Workflow:**
- Cooldown ablauf abwarten -> mit `/po-challenge --release <ID>` wieder ziehen.
- Nach 30 Tagen ohne Release: Eintrag als `status: archived` markieren
  (Anti-Pattern: stille Loeschung — Ideen-Archiv ist Lern-Material).

---

## Format eines Eintrags

```
## <ID> — <Kurztitel>

**Erstellt:** YYYY-MM-DD HH:MM
**Release-bar ab:** YYYY-MM-DD HH:MM
**Vision-Prinzip-Kandidat:** <principle_id oder "unklar">
**Status:** parked | released | archived

**Idee:**
<2-3 Saetze Originalformulierung>

**3x Why (Antwort):**
- Warum wirklich? <Antwort>
- Warum jetzt? <Antwort>
- Warum so? <Antwort>

**Cooldown-Begruendung:** <warum 48h sinnvoll waren>
```

---

## Geparkte Ideen

<!-- Neueste oben. Eintraege werden von `/po-challenge` angehaengt. -->

## DEF-001 — Auto-Memory-Pattern fuer In-Session-Erkenntnisse (MindStudio/Anthropic-Style)

**Erstellt:** 2026-05-26 10:00
**Release-bar ab:** 2026-05-28 10:00 (= +48h)
**Vision-Prinzip-Kandidat:** `lessons-aus-live-use-zurueckfuehren` (mit Ueberlapp-Warnung)
**Status:** parked

**Idee:**
Im agile-sdd-skill einen Hook bauen, der analog zu Anthropics
Claude-Code-Auto-Memory automatisch In-Session-Erkenntnisse (geloeste
Fehler, neu entdeckte ENV-Abhaengigkeiten, Code-Quirks) in CLAUDE.md
oder KNOWN_FAILURES.md persistiert — ohne expliziten User-Befehl.
Quelle: Recherche 2026-05-26 Empfehlung 3 + MindStudio-Artikel zu
Claude-Code-Auto-Memory + Anthropic "Dreaming"-System + Cognition-
Devin-Erkenntnisse zu explizitem Memory-Management.

**3x Why (Antwort):**
- Warum wirklich? Wenn ein Subagent waehrend einer Session was lernt
  (z.B. "Lightroom UI hat seit Update einen Update-Dialog im Vordergrund"),
  geht das Wissen heute mit Session-Ende verloren. Anthropic-Beta-Daten
  zeigen 97% weniger First-Pass-Errors bei expliziter Memory-Persistierung.
- Warum jetzt? Recherche bringt das Pattern als "dominante Optimierung
  2026". ABER: Recherche markiert selbst als sekundaer und stellt offene
  Frage "wann triggert Claude-Code-Auto-Memory wirklich? Empirie sammeln."
- Warum so? Anthropic hat den Mechanismus schon — wir muessten nur den
  Hook im Skill aufschnueren. Risiko: Black-Box-Verhalten (Auto-Memory
  entscheidet selbst was persistiert wird).

**Cooldown-Begruendung:**
Drei Gruende fuer 48h-Defer (statt sofort Ticket):
1. **Vision-Prinzip-Match ist unklar.** Naechste-Kandidat ist
   `lessons-aus-live-use-zurueckfuehren` — das deckt aber bereits
   SKILL-006 (KNOWN_FAILURES.md) ab. Risiko: zwei Mechanismen fuer den
   gleichen Effekt = `skill-schlanker-als-was-er-ersetzt`-Verletzung.
2. **Recherche selbst markiert als "sekundaer".** Empfehlung 2
   (Pre-Conditions, → SKILL-004) ist "DIE eine Massnahme". Empfehlung 1
   (KNOWN_FAILURES, → SKILL-006) ist die strukturierte Ablage. Auto-
   Memory ist die automatische Befuellung — sinnvoll, aber erst nach
   Erfahrung mit den manuellen Varianten.
3. **Empirie-Bedarf:** Recherche-Offene-Frage 2 lautet "wann triggert
   Claude-Code-Auto-Memory wirklich?". Ohne Empirie wuerden wir ein
   Skill-Feature fuer einen Mechanismus bauen, dessen Verhalten wir
   nicht zuverlaessig kennen.

**Was muesste vor Release passieren:**
- 14+ Tage Live-Erfahrung mit SKILL-004 (Pre-Conditions) und SKILL-006
  (KNOWN_FAILURES) gesammelt
- Konkrete Beobachtung: hat Claude-Code-Auto-Memory in einer
  Schaltzentrale/Immobewertung/DropboxCheck-Session etwas selbsttaetig
  in CLAUDE.md geschrieben? (= Empirie-Datenpunkt)
- Falls SKILL-006-Live-Use zeigt: "Subagent dokumentiert die neuen
  FAILURE-Eintraege schon manuell zuverlaessig" → Auto-Memory ist
  ueberfluessig → archive.
- Falls SKILL-006-Live-Use zeigt: "Subagent vergisst, FAILURE-Eintraege
  zu schreiben — Verifier muss nachhaken" → Auto-Memory wird relevant
  als Auto-Vorschlag-Mechanismus.

**Release-Trigger:** `/po-challenge --release DEF-001` nach
SKILL-004 + SKILL-006 Outcome-Review (frueh: 2026-06-XX).
