# DEFERRED — geparkte Ideen (PO-Skill)

Ideen, die per `/po-challenge` geparkt wurden (48h-Cooldown oder bewusst spaeter).
Format pro Eintrag:

## YYYY-MM-DD — <Kurztitel>
**Warum geparkt:** <Cooldown | Scope | wartet auf X>
**Frueheste Wiedervorlage:** YYYY-MM-DD
**Kern-Idee:** <1-2 Saetze>

---

## DEF-001 — Auto-Memory-Pattern fuer In-Session-Erkenntnisse (MindStudio/Anthropic-Style)
**Warum geparkt:** Cooldown + Vision-Prinzip-Match unklar (Ueberlapp mit
KNOWN_FAILURES.md/SKILL-006) + Empirie-Bedarf. Aus skill_dev/DEFERRED.md migriert 2026-07-12.
**Frueheste Wiedervorlage:** nach 14+ Tagen Live-Erfahrung mit SKILL-004 (Pre-Conditions)
+ SKILL-006 (KNOWN_FAILURES), inkl. konkreter Beobachtung ob Claude-Code-Auto-Memory
selbsttaetig in CLAUDE.md schreibt.
**Vision-Prinzip-Kandidat:** `lessons-aus-live-use-zurueckfuehren` (mit Ueberlapp-Warnung).
**Kern-Idee:** Hook im agile-sdd-skill, der analog zu Anthropics Auto-Memory
In-Session-Erkenntnisse (geloeste Fehler, ENV-Abhaengigkeiten, Code-Quirks) automatisch
in CLAUDE.md/KNOWN_FAILURES.md persistiert — ohne expliziten User-Befehl.
**Risiko:** Zwei Mechanismen fuer denselben Effekt (`skill-schlanker-als-was-er-ersetzt`-
Verletzung); Black-Box-Verhalten (Auto-Memory entscheidet selbst). Erst nach Erfahrung
mit den manuellen Varianten (SKILL-006) entscheiden — sonst archivieren.
**Release-Trigger:** `/po-challenge --release DEF-001` nach SKILL-004+006 Outcome-Review.
