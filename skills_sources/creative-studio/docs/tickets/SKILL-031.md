# SKILL-031: creative-studio — DCO-/Asset-Feed-Export-Modus (dco_bundle.json fuer Advantage+)

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Could
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** asset_feed_statt_fertiger_komposition (getrennte Bausteine fuer Advantage+) + dco_bundle_von_ads_agent_konsumierbar
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_creative-studio-flow-improvements.md` (§1.2 DCO/Advantage+ Creative, §3.4 Asset-Feed-/DCO-Export-Modus; MoSCoW-Liste #4)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> Meta hat DCO Ende 2024 in **Advantage+ Creative** ueberfuehrt: man laedt einzelne Asset-Komponenten hoch,
> Metas ML assembliert pro Impression. Asset-Budgets: bis 10 Medien, je 5 Headlines/Primary-Texte/
> Descriptions/CTAs. Studien zeigen 15–25 % niedrigere CPA vs. Single-Ad-Testing. Neben dem heutigen
> Komposition-Modus braucht der Skill einen **Asset-Feed-Modus**: getrennte Bausteine statt fertig
> komponierter Creatives.

## Was soll erreicht werden? (Business-Ziel)
Ein zweiter Output-Modus, der **getrennte Bausteine** (Medien / Headlines / Texte / CTAs) als
`dco_bundle.json` liefert — strukturiert nach Metas Asset-Budgets — sodass ein Ads-Agent das Bundle direkt
in ein Advantage+/DCO-Ad-Set kippt, statt fertig komponierte Creatives zu erhalten. Projektneutral.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When der Asset-Feed-Modus aktiviert wird, the system shall die Creative-Bausteine
      **getrennt** ausgeben (Medien, Headlines, Primary-Texte, CTAs) statt fertig komponierter Creatives.
- [x] **EARS-2:** When ein Bundle erzeugt wird, the system shall ein `dco_bundle.json` schreiben, das die
      Bausteine nach Metas Asset-Budgets gruppiert (≤ 10 Medien, je ≤ 5 Headlines/Texte/Descriptions/CTAs).
- [x] **EARS-3:** When mehr Bausteine vorliegen als ein Budget zulaesst, the system shall warnen/kappen
      (kein stilles Ueberschreiten der Meta-Limits).
- [x] **EARS-4:** When ein Bundle erzeugt wird, the system shall die `variant_id`/`utm_content`-Systematik
      (SKILL-024) und das Manifest (SKILL-023) als Quelle nutzen — derselbe Naming-Vertrag.
- [x] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall das
      Bundle-Format projektneutral halten (Ads-Agenten beider Projekte lesen dasselbe Schema).

## Technische Hinweise
- Baut auf SKILL-023 (Manifest) + SKILL-024 (Naming) auf — abhaengiges Folge-Ticket, daher `idea`/Could.
- `creative_studio/dco_export.py`: Manifest/Job → `dco_bundle.json` (Bausteine gruppiert nach Asset-Typ).
- Komposition-Modus (heute) bleibt erhalten — Advantage+ Creative-Enhancement im Ad-Set muss dann
  deaktiviert sein (siehe SKILL.md §7). Asset-Feed-Modus ist der gegenteilige, skalierende Pfad.
- Das tatsaechliche Hochladen ins Ad-Set liegt beim Ads-Agent (Meta-MCP), nicht in diesem Skill.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/dco_export.py` — **neu** (Manifest → dco_bundle.json).
- `skills_sources/creative-studio/creative_studio/batch.py` — Manifest-Quelle (SKILL-023).
- `skills_sources/creative-studio/creative_studio/specs.py` — Naming (SKILL-024) + Asset-Budget-Konstanten.
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_creative-studio-flow-improvements.md` (§1.2, §3.4).

## Ergebnis / Notizen

**Implementiert (2026-06-24):** `creative_studio/dco.py` — zweiter Output-Modus
(Asset-Feed/DCO). Liest ein `manifest.json` (SKILL-023) und schreibt ein
`dco_bundle.json` mit den **getrennten Bausteinen** statt fertig komponierter
Creatives. Komposition-Modus (heute) bleibt unberuehrt.

- **Bausteine getrennt (EARS-1):** `medias`, `headlines`, `primary_texts`,
  `descriptions`, `ctas` — jeweils dedupliziert (Reihenfolge-erhaltend).
  `medias` dedupliziert ueber `(file, format)`; Varianten ohne Datei-Output
  (`file=None`: Video-TODO / Render-Fehler aus SKILL-023) liefern **kein**
  Fake-Asset, werden aber geloggt.
- **Meta-Asset-Budgets (EARS-2):** Konstanten in `dco.py`
  (`MAX_MEDIAS=10`, `MAX_HEADLINES/PRIMARY_TEXTS/DESCRIPTIONS/CTAS=5`),
  im Bundle unter `asset_budgets` mitgeschrieben.
- **Kappen statt stilles Truncaten (EARS-3):** `_cap()` + Media-Kappung loggen
  via `log()` Anzahl **und** die konkret verworfenen Bausteine. Verifiziert in
  `test_capping_warns_and_truncates` (8 Headlines -> 5, "Hook 7" im Log) und
  `test_media_capping_warns` (13 -> 10).
- **Attribution erhalten (EARS-4):** `utm_mapping` behaelt **alle**
  `variant_id`/`utm_content`-Paare (auch geplante/gekappte Varianten) — wird
  bewusst NICHT gekappt, sonst geht Attribution verloren. Naming kommt 1:1 aus
  `specs.make_variant_id`/`make_utm_content` (SKILL-024).
- **Projektneutral (EARS-5):** kein Brand-/Projektwert in `dco.py`; `ad_id`
  kommt aus dem Manifest. `mode: "asset_feed"` grenzt gegen Komposition ab.
- **Abgrenzung dokumentiert:** Bundle ist nur die **Vorbereitung**; das
  tatsaechliche Anlegen des Advantage+/DCO-Asset-Feed-Creatives bei Meta ist ein
  separater Schritt (Meta-MCP/SDK beim Ads-Agent), nicht Teil dieses Skills
  (Docstring + `note`-Feld im Bundle).
- **CLI:** `python -m creative_studio.dco --manifest <pfad> [--out dco_bundle.json]`.

**ANNAHME zu den Rohtexten (zentral, ehrlich dokumentiert):** Das heutige
SKILL-023-`manifest.json` fuehrt pro Variante nur `hook` (= Headline oder
Eyebrow) + variant_id/framework/format/media/file/utm_content — **keine**
getrennten Felder fuer `primary_text`, `description`, `cta`. Daraus folgt:
- `headlines` werden aus den `hook`-Werten abgeleitet (Feld-Aliasse
  `headline` -> `hook`).
- `primary_texts` / `descriptions` / `ctas` werden **nur** uebernommen, wenn das
  Manifest die Felder tatsaechlich fuehrt (Alias-Sets, z.B. `cta`/`subline`/`body`).
  Fehlen sie, bleibt die Liste **leer** und es wird geloggt — **keine erfundenen
  Texte** (kein Fake). Wer ein vollstaendiges Text-Set will, reichert das Manifest
  beim Batch-Lauf an; `dco.py` ist dafuer ueber die Feld-Aliasse vorbereitet.

**Test-Ergebnis:** `pytest tests/test_skill_031_dco.py -q` -> **7 passed in 0.13s**.
Tests: getrennte Bloecke (EARS-1), Bundle geschrieben + medias dedup (EARS-2,
6 Varianten/geteilte Datei -> 5 medias), Headline-Kappung + Log (EARS-3),
Media-Kappung + Log (EARS-3), utm_mapping vollstaendig (EARS-4), kein Fake-Text
bei fehlenden Feldern, file=None wird uebersprungen (kein Fake-Medium).

**Beispiel-Auszug `dco_bundle.json`** (aus Mini-Manifest, gekuerzt):
```json
{
  "mode": "asset_feed",
  "ad_id": "h1-immo",
  "source": "manifest.json (SKILL-023)",
  "asset_budgets": {"medias": 10, "headlines": 5, "primary_texts": 5, "descriptions": 5, "ctas": 5},
  "medias": [
    {"file": "h1-immo__bab-h00__feed_4x5.png", "format": "feed_4x5", "media": "image"},
    {"file": "h1-immo__bab-h00__story_9x16.png", "format": "story_9x16", "media": "image"}
  ],
  "headlines": ["Mehr Rendite", "Schluss mit Leerstand", "Jetzt investieren"],
  "primary_texts": [],
  "descriptions": [],
  "ctas": ["Mehr erfahren"],
  "utm_mapping": [
    {"variant_id": "h1-immo__bab-h00__feed_4x5", "utm_content": "h1-immo-feed-4x5-bab-h00", "format": "feed_4x5", "media": "image"}
  ],
  "note": "Bundle = Vorbereitung fuer Meta Advantage+/DCO ... Anlegen erfolgt separat (Meta-MCP/SDK)."
}
```

**Code-Referenzen:**
- `skills_sources/creative-studio/creative_studio/dco.py` — **neu** (Manifest -> dco_bundle.json).
  Hinweis: Ticket-Code-Referenz nannte `dco_export.py`; Datei heisst `dco.py`
  (CLI `python -m creative_studio.dco`) — abgestimmt mit Auftrags-Vorgabe.
- `skills_sources/creative-studio/tests/test_skill_031_dco.py` — **neu** (7 Tests).
- Liest (unveraendert): `creative_studio/batch.py` (Manifest-Quelle),
  `creative_studio/specs.py` (Naming SKILL-024).

**Nicht beruehrt** (parallele Subagenten): specs.py, render_image.py, templates/,
batch.py, frameworks.py, assets.py, prep_bg.py, gallery.py, video/.
