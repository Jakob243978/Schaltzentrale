# Runbook: Content-Marktrecherche (Tier 0, WebSearch-getrieben)

> **Zweck:** Aus einem Seed-Thema eine **priorisierte Themen-/Hook-/Format-Liste
> mit Quellen** erzeugen, deren Felder 1:1 die `creative-studio`-Inputs
> (`--headline`/`--subline`/`--cta`/`--eyebrow` bzw. Video-`--props`) speisen.
> **Tier 0 = gratis, kein API-Key**, rein WebSearch/WebFetch-getrieben.

Dieses Runbook ist eine **Agenten-Anleitung** (kein Code). Es ist die
vorgelagerte Ideen-/Recherche-Stufe vor der Creative-Produktion. Der Skill bleibt
projektneutral: Seed-Thema + optionaler Brand-Kontext kommen als Eingabe — **kein
hartkodierter Projektwert** im Runbook.

---

## Eingabe

| Feld | Pflicht | Beschreibung |
|---|---|---|
| `seed_thema` | ja | Das Kern-Thema (z. B. "agentisches Arbeiten", "KI-Agenten Unternehmen"). |
| `anzahl_seeds` | nein | Wie viele verwandte Seed-Begriffe ableiten (Default 3-5). |
| `tier` | nein | `0` (Default, gratis/WebSearch) \| `1` (PAA/SERP-API) \| `2` (GSC/Trends-Alpha). Dieses Runbook deckt **Tier 0** ab. |
| `brand_kontext` | nein | Optionaler Marken-/Zielgruppen-Kontext (z. B. DISC-rot, B2B, Preis-Niveau), um Hooks zu schaerfen. |

> Tier 1/2 (PAA/SERP-API, GSC, Trends-Alpha) sind separate Tickets (SKILL-050/051)
> und brauchen Keys/Property — **nicht** Teil dieses Tier-0-Runbooks.

---

## Ablauf (sechs Schritte, deterministisch in dieser Reihenfolge)

### Schritt 1 — Sammeln (pro Seed-Thema)
Seed-Begriffe definieren (Seed + `anzahl_seeds` verwandte Begriffe). Pro Seed je
gratis Quelle abfragen — jeder Roh-Eintrag bekommt **Quelle + Datum**:

- **Google Trends** (UI/WebFetch): "Rising/Breakout"-Queries, verwandte Themen,
  DACH-Regionalfilter. Stark fuer **Timing** (stabile vs. aufkommende Nachfrage).
- **YouTube-Autocomplete** (Suggest-Endpoint): reale Such-Eingaben =
  Format-/Hook-Signale ("wie ...", "... erklaert", "... vs ...").
- **People Also Ask (PAA)**: die echten Fragen rund um den Seed (Was/Wie/Warum/vs.)
  — via WebSearch der SERP. Gold fuer Hooks + AEO.
- **3-5 Reddit/LinkedIn/Foren-O-Toene** (WebSearch + Lesen): ungefilterte Sprache
  der Zielgruppe, Pain Points, Einwaende, Vokabular.

> Ergebnis Schritt 1: **Roh-Signal-Liste** (Query/Frage/O-Ton | Quelle | Datum).

### Schritt 2 — Clustern zu Themen
Verwandte Queries/Fragen **semantisch** (nicht nur Wortmatch) zu **Themen-Clustern**
gruppieren. Jedes Cluster = ein **Hub** (breite Kernfrage) + **narrow Sub-Fragen**
(Hub-and-Spoke). Kombiniertes Cluster-Volumen ueberspringt Privacy-Schwellen.

### Schritt 3 — Funnel-Mapping
Jedes Cluster einer Funnel-Stufe zuordnen (deckt sich mit `ContentType.funnel`):

- **TOFU (awareness):** "Was ist X?", Trend-/Begriffs-Fragen -> breite Reichweiten-Hooks.
- **MOFU (consideration):** Vergleiche, "Wie/Worauf achten", Risiken/Einwaende -> Trust-/Erklaer-Content.
- **BOFU (conversion):** Anbieter-/Kosten-/Ergebnis-Fragen, konkrete Use-Cases -> Angebots-nahe Hooks.

### Schritt 4 — Priorisieren
Score je Cluster = **Volumen x Relevanz x (1/Wettbewerb) + Social-Resonanz**.
Praktikabel als **1-3-Skala** pro Faktor (Social-Resonanz fuer enge B2B-Nischen
hoeher gewichten als reines Volumen). Cluster nach Gesamt-Score ranken.
Prioritaet im Output = **1 (hoch) / 2 (mittel) / 3 (niedrig)**.

### Schritt 5 — Idee -> Hook -> Format
Pro Top-Cluster:

- **Content-Idee** = der konkrete Winkel (genau 1 Message).
- **Hook** = aus der echten PAA-Frage oder dem Reddit-O-Ton formuliert
  (Frage-, Kontrast- oder Zahl-Hook). **DACH-Coaching-Claim-Check anwenden**
  (siehe `creative_studio.specs.compliance_warnings` / SKILL-026): KEINE
  "Du wirst ..."-/Vorher-Nachher-Transformations-Versprechen, keine unbelegten
  Garantien/Superlative. Hook sachlich + belegbar halten.
- **Format** = aus dem Signal ableiten und auf einen `CONTENT_TYPES`-Key mappen:
  - Autocomplete-Video-Suchen -> `short_video_text_hook` / `talking_head` (Reel/Short).
  - Vergleichs-/Schritt-Fragen -> `carousel` / `educational_carousel` / `listicle`.
  - Scharfe Einzel-Aussage / Pattern-Naming -> `static_statement`.
  - Beweis/Referenz vorhanden -> `testimonial` / `before_after` (Compliance-Kopplung beachten).

### Schritt 6 — Output-Liste
Die priorisierte Liste als **Markdown-Tabelle** ausgeben (Pflicht). Jeder Eintrag
hat **>= 1 zitierte Quelle**. Optional zusaetzlich als JSON, dessen Felder direkt
die Creative-Generierung speisen.

---

## Output-Vertrag (Uebergabe an creative-studio)

### Markdown-Tabelle (Pflicht)

| Thema | Funnel | Idee | Hook | Format | Prioritaet | Quellen |
|---|---|---|---|---|---|---|
| <Cluster/Hub> | awareness\|consideration\|conversion | <1 Message> | <Hook-Text, claim-gecheckt> | <CONTENT_TYPES-Key> | 1\|2\|3 | <Quelle + Datum> |

### JSON (optional) — speist `render_image`-Args / Video-`--props`

```json
{
  "items": [
    {
      "thema": "<Cluster/Hub>",
      "funnel": "awareness",
      "format": "short_video_text_hook",
      "prioritaet": 1,
      "quellen": ["<Quelle + Datum>"],
      "creative_inputs": {
        "headline": "<Hook -> --headline>",
        "subline": "<Idee/Beleg -> --subline>",
        "eyebrow": "<Kategorie/Kontext -> --eyebrow>",
        "cta": "<Call-to-Action -> --cta>"
      }
    }
  ]
}
```

Feld-Mapping (1:1 in die Creative-Inputs):

- `creative_inputs.headline` -> `render_image --headline` / Video `headline`
- `creative_inputs.subline`  -> `--subline` / `subline`
- `creative_inputs.eyebrow`  -> `--eyebrow` / `eyebrow`
- `creative_inputs.cta`      -> `--cta` / `cta`
- `format` -> waehlt den `CONTENT_TYPES`-Typ (-> erlaubte `FORMATS`, Slide-/Laengen-Constraints)

---

## Guardrails (verbindlich)

- **Tier 0 braucht keinen API-Key** — nur WebSearch/WebFetch. Kommt ein Schritt
  ohne Quelle aus, ist der Eintrag unvollstaendig (>= 1 Quelle pro Zeile Pflicht).
- **DACH-Coaching-Claim-Check auf jeden Hook** (SKILL-026): keine
  "Du wirst ..."-Versprechen, keine unbelegten Garantien/Superlative/Heilbezuege.
- **Projektneutral:** Seed-Thema + Brand-Kontext kommen als Eingabe — kein
  hartkodierter Projekt-/Brand-Wert in diesem Runbook.
- **Reihenfolge ist deterministisch:** Schritte 1 -> 6 strikt in dieser Folge.

---

## Quellen-Tiers (Referenz)

- **Tier 0 (dieses Runbook, gratis):** Google Trends (UI/Fetch), YouTube-Autocomplete,
  PAA (SERP via WebSearch), Reddit/LinkedIn/Foren manuell, optional TikTok Creative
  Center UI. Deckt ~80 % des Erkenntniswerts ab.
- **Tier 1 (kleines Budget, SKILL-050):** Serper (Free-Tier) / DataForSEO fuer
  strukturierte PAA/SERP-Features + YouTube-Autocomplete-Fetcher.
- **Tier 2 (Domain live, SKILL-051):** GSC Search Analytics API/MCP (eigene
  realisierte Nachfrage + Content-Gaps), Google-Trends-Alpha-API.
