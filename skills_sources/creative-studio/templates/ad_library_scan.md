# Runbook: Ad-Library-Scan (Wettbewerbs-Recherche, Proxy — kein Spend)

Reproduzierbarer Ablauf, um aus einem **Seed-Thema** oder **Wettbewerber-Page-ID(s)**
eine Tabelle **wahrscheinlich skalierender Ads** + eine **Hook-/Angle-Muster-Liste**
zu erzeugen, die als Briefing-Input in die Creative-Generierung fliesst.

> [!warning] EHRLICHKEIT — kein Spend abrufbar (Pflicht-Disclaimer)
> Meta gibt fuer kommerzielle Ads **KEINEN Spend / keine Impressions / keine
> Reichweite** preis — weder im MCP-Payload noch ueber die offizielle Public API
> (Spend-Ranges nur fuer politische/Issue-Ads). Dieser Scan beruht ausschliesslich
> auf **Proxy-Signalen**: Longevity, Creative-Multiplikation pro Page, Re-Serving,
> Hook-Wiederholung. Der Longevity-Score ist eine **Priorisierung fuer manuelle
> Sichtung**, KEINE Budget-Wahrheit. Der Disclaimer (`ad_library.PROXY_DISCLAIMER`)
> ist **Pflicht-Output** jedes Scans.

> [!important] Architektur — wer macht den MCP-Call?
> Das Python-Modul `creative_studio/ad_library.py` ruft das Meta-MCP **nicht selbst**
> auf. Den read-only Call `mcp__claude_ai_Meta__ads_library_search` macht der
> **Agent/Claude**; das Modul **verarbeitet** die zurueckgegebene JSON.

> [!warning] Legal / Compliance
> Ad Library nur fuer **Inspiration** (Hook-/Angle-Muster, Format-Trends) — **kein
> 1:1-Kopieren** von Creatives/Claims, **kein Bulk-Scraping** (Tool-Policy). Markenrechte/
> Claims der Wettbewerber nicht uebernehmen.

---

## Eingabe

- **Seed-Thema** (z.B. "KI Automatisierung Unternehmen") **ODER** Wettbewerber-`page_ids`.
- **Land** (ISO-2, Default `DE`).
- Optional: `ad_active_status` (`ALL`/`ACTIVE`/`INACTIVE`), `limit` (max. 50).

Projektneutral — kein hartkodierter Wettbewerber/Themenwert im Modul.

---

## Ablauf (deterministisch)

### Schritt 1 — Themen-Sweep (Markttiefe + Top-Advertiser)

Agent ruft das MCP auf:

```
ads_library_search(search_terms="<Seed-Thema>", countries=["DE"], ad_active_status="ACTIVE", limit=50)
```

Das Ergebnis (JSON mit `estimated_total_count` + Ad-Liste unter `data`/`ads`) ins Modul:

```python
from creative_studio import ad_library as al
sweep = al.theme_sweep(mcp_result)
# sweep["estimated_total_count"]  -> Markttiefe
# sweep["top_advertisers"]        -> mehrfach auftauchende Pages (absteigend)
```

### Schritt 2 — Page-Drilldown (pro Top-Page)

Fuer jede interessante Page aus `top_advertisers` ruft der Agent auf:

```
ads_library_search(page_ids=["<page_id>"], countries=["DE"], ad_active_status="ALL", limit=50)
```

Real verfuegbare Felder pro Ad (empirisch, **kein** Spend/Reach):
`id`, `page_id`, `page_name`, `ad_creative_link_title` (= Hook), `ad_creation_time`,
`ad_delivery_start_time`, `ad_snapshot_url`.

### Schritt 3 — Longevity-Score + Report

Alle gesammelten Ad-Eintraege (aus einem oder mehreren Calls) als Liste ins Modul:

```python
report = al.scan_report(all_entries, theme="<Seed-Thema>", country="DE")
print(al.render_report_markdown(report))   # Tabelle + Hooks + Disclaimer
```

**Longevity-Score-Formel (fixiert, Research §2):**

```
score = aktive_Tage(creation -> heute) * log(1 + Anzahl_aktiver_Varianten_der_Page)
```

Hoch = **lange aktiv UND breit ausgerollt**. Bewusst grob; rankt wahrscheinliche
Gewinner nach oben, ersetzt aber keinen echten Spend.

### Schritt 4 (optional) — Snapshot-Anreicherung

Fuer die Top-N-Ads die `ad_snapshot_url` oeffnen (manuell/Vision): Volltext, Visual,
Format, ggf. **EU-Reach-Band** (DSA, nur ueber die Snapshot-Seite — nicht im MCP-Payload).
Das ist die einzige offizielle Budget-Annaeherung fuer kommerzielle Ads.

### Schritt 5 — Uebergabe an die Creative-Generierung

Die Top-Hooks/Angles aus `report["hook_patterns"]` fliessen als Inspiration in die
bestehende `render_image`/Video-Generierung (Headline/Subline/Hook) — **nur als Muster,
nie als Copy-Paste**.

---

## Output

- **Tabelle** `Advertiser | Hook | aktiv seit | Tage | #Varianten | Re-Serving | Longevity-Score | Snapshot`
  (absteigend nach Longevity-Score).
- **Hook-/Angle-Muster-Liste** (wiederkehrende Hooks, nach Vorkommen + Page-Breite).
- **Proxy-Disclaimer** (immer mit ausgegeben).

## Proxy-Signale (staerkstes zuerst, Research §2)

1. **Longevity** — `ACTIVE` + grosser Abstand creation->heute (staerkstes Signal).
2. **Creative-Multiplikation** — viele aktive Varianten desselben Hooks pro Page.
3. **Re-Serving** — `ad_delivery_start_time` deutlich nach `ad_creation_time`.
4. **Hook-Wiederholung** — derselbe Hook ueber Wochen/mehrere Ad-IDs.
5. **EU-Reach-Baender** (manuell, nur Snapshot-Seite) — semi-quantitativ.

> [!caution] Grenzen
> Lange Laufzeit kann Always-on-Branding mit kleinem Budget sein; viele Varianten
> koennen Testphase sein; keine Plattform-Aufschluesselung (FB/IG/Reels) im MCP.
> Proxy-Score = Priorisierung fuer manuelle Sichtung, nicht Wahrheit.
