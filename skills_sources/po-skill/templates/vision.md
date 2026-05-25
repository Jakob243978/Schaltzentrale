# PROJECT_VISION.md

> [!info] Hinweis
> Diese Datei ist die **Verfassung** des Projekts. Sie wird in jedem
> Implementer-Bootstrap mit-gelesen und in jedem `/po-challenge` referenziert.
> Aenderungen werden im **Aktualisiert**-Log am Ende append-only festgehalten —
> die Vision wird *geschaerft*, nicht neu geschrieben.

---

## Vision-Statement

<!--
Ein Absatz, 3-5 Saetze: Wer profitiert wie davon? Warum existiert dieses
Projekt UEBERHAUPT? Keine Tech-Begriffe, kein Framework, kein Stack — nur
Realitaet + Wirkung.

Beispiel-Stil:
"Hoechst autonomer Immobilien-Einkauf — KI hilft dem Menschen, die noetigen
Schritte auszufuehren. Mehr Deals, weniger Zeit-pro-Deal, Vorteil gegenueber
der Konkurrenz, die das nicht hat. Wir bauen einen Hebel durch
Geschwindigkeit und Daten-Akkumulation, nicht durch Kapital."
-->

---

## Kern-Prinzipien

<!--
5-10 Bullets. Jeder Bullet hat eine `principle_id` (Kebab-Slug) — Tickets
referenzieren diese ID im Frontmatter `vision_principle:`.

Format:
1. `slug-id` — Titel-Satz. Begruendung in 1-2 Saetzen.

Beispiele:
1. `mensch-entscheidet-ki-bereitet-vor` — KI macht niemals Kauf-/Verkaufs-
   Entscheidungen autonom. KI bereitet Entscheidungen vor: filtert,
   recherchiert, formuliert. Mensch klickt.
2. `geschwindigkeit-vor-perfektion` — 80%-Bewertung in 5 Min ist besser
   als 100%-Bewertung in 5 Tagen.
-->

---

## Outcome-Metriken

<!--
Messbare Groessen die zeigen, ob die Vision Realitaet wird. NICHT "mehr
Effizienz" / "bessere UX" — sondern Zahlen aus echten Quellen (DB, Logs,
Manual-Tracking).

Format:
- **<metric_id>** — Klartext-Beschreibung. Quelle: <woher kommt der Wert>.

Beispiele:
- **banking_match_per_month** — Anzahl Properties die echten 15x-Filter
  passieren / Monat. Quelle: SQL auf `properties` WHERE kpf<=15.
- **time_to_decision_median** — Median-Zeit von Inserat-Eingang bis
  PURSUE/PASS-Entscheidung. Quelle: `properties.created_at` -> erstes
  `actions.completed_at`.
-->

---

## Was NICHT im Scope ist

<!--
Explizite Negationen schuetzen vor Scope-Creep. Wenn jemand eine Idee
bringt die hier steht: keine Diskussion, Idee passt nicht.

Beispiele:
- Verkauf von Immobilien (nur Einkauf)
- Andere Asset-Klassen (nur Wohnimmobilien)
- Massenmailing im Spam-Stil
-->

---

## Aktualisiert (Append-only Log)

<!--
Jede Aenderung an dieser Datei bekommt einen Eintrag. Format:

## YYYY-MM-DD — <Was wurde geschaerft>
**Wer:** <User / Implementer>
**Grund:** <warum war die Aenderung noetig?>
**Aenderung:** <welche Sektion / welcher Bullet>

Reihenfolge: neueste oben.
-->
