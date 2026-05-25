---
description: Einmalige Initialisierung des PO-Skills in einem neuen Projekt (Vision, Deferred, Config, CLAUDE.md-Block)
arg-hint: (optional) Pfad-Hinweis zum Projekt-Root, default = cwd
---

Du fuehrst die einmalige Initialisierung des PO-Skills im aktuellen Projekt
durch. Halte dich strikt an die folgenden Schritte.

## 1. Vorbedingungen pruefen

- Existiert `docs/PROJECT_VISION.md`?
  → Wenn ja: STOP mit Hinweis *"PO-Skill bereits initialisiert. Nutze
    `/po-challenge` fuer neue Ideen oder editiere die Vision-Datei direkt."*
- Existiert `docs/` Ordner?
  → Wenn nein: anlegen.

## 2. Vision-Datei erstellen

Kopiere `~/.claude/skills/po-skill/templates/vision.md` nach
`docs/PROJECT_VISION.md`.

**Befuellung:**
- Wenn der User im aktuellen Chat schon **Initial-Vision-Material** geliefert
  hat (Sprachnachrichten, Briefing, Spec): direkt einarbeiten — in **Jakobs
  Sprache**, nicht im Marketing-Sprech glaetten.
- Sonst: User aktiv fragen nach
  - 1 Vision-Statement
  - 5-8 Kern-Prinzipien (mit Slug-IDs)
  - 3-5 Outcome-Metriken (messbar)
  - Was explizit NICHT im Scope ist

Pflicht-Footer am Ende der Datei:

```
## Aktualisiert (Append-only Log)

## YYYY-MM-DD — Initial-Befuellung durch /po-init
**Wer:** Implementer-Subagent (po-init)
**Grund:** Erstmalige Vision-Erstellung
**Aenderung:** Komplett-Befuellung aus Briefing-Material
```

Hinweis am Anfang der Datei (oberhalb des Vision-Statements):

```
> [!warning] Initial-Befuellung
> Diese Vision ist die erste Niederschrift basierend auf User-Material.
> User: bitte review und schaerf wo noetig — du bist der finale PO.
> Aenderungen ins Aktualisiert-Log unten append-only festhalten.
```

## 3. DEFERRED.md anlegen

Kopiere `~/.claude/skills/po-skill/templates/DEFERRED.md` nach
`docs/DEFERRED.md` (leer, nur Header + Format-Beschreibung).

## 4. po-config.yaml anlegen

Kopiere `~/.claude/skills/po-skill/templates/po-config.yaml.example` nach
`docs/po-config.yaml`. Defaults uebernehmen (`outcome_review_days: 14`,
`cooldown_default_hours: 48`).

## 5. CLAUDE.md erweitern

Pruefe ob in `CLAUDE.md` bereits ein `## Skill: PO`-Block existiert.
Wenn nein: ergaenze ihn am Ende der Datei (analog zum vorhandenen
`## Skill: Agile SDD`-Block falls vorhanden):

```markdown
## Skill: PO
Aktiv. Vision-Constitution: docs/PROJECT_VISION.md (Pflicht-Lese-Datei in jedem Implementer-Bootstrap)
Backlog-Hygiene: docs/DEFERRED.md (geparkte Ideen) | docs/po-outcomes.md (Outcome-Reviews)
Commands: /po-init (einmalig) | /po-challenge (vor jedem neuen Ticket) | /po-prioritize (Backlog ranken) | /po-verify-outcome TICKET-NNN (>= 14 Tage nach done)
SDD-Hook: Ticket-Frontmatter braucht `vision_principle: <principle_id>` bevor Status auf `spec` darf (Warning per Default, Hard-Block bei `PO_SKILL_STRICT=1`).
Config: docs/po-config.yaml (outcome_review_days, cooldown_default_hours, rice_effort_mapping).
```

## 6. Optional: po-outcomes.md vorbereiten

Lege `docs/po-outcomes.md` leer mit Header an (wird spaeter von
`/po-verify-outcome` befuellt):

```markdown
# Outcome-Reviews (PO-Skill)

Eintraege werden von `/po-verify-outcome TICKET-NNN` angehaengt.
Format siehe ~/.claude/skills/po-skill/SKILL.md Sektion E.
```

## 7. Abschluss-Bericht

Gib eine knappe Zusammenfassung aus:
- Welche Dateien wurden angelegt
- Was der User als naechstes tun sollte:
  1. Vision-Datei review + schaerfen
  2. `/po-challenge` ab sofort vor neuen Ticket-Ideen aufrufen
  3. Bei naechstem SDD-Ticket: `vision_principle:` ins Frontmatter setzen

**Wichtig:** Du legst KEINE Tickets an. Der PO-Skill ist
challenger/priorisierer/verifier — nicht generator.
