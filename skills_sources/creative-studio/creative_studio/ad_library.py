"""creative-studio — Ad-Library-Scan-Modul + Longevity-Score (SKILL-052).

Verarbeitet die JSON-Eintraege, die der Agent ueber das Meta-MCP
`mcp__claude_ai_Meta__ads_library_search` (read-only) zurueckbekommt, zu einem
reproduzierbaren Wettbewerbs-Scan: pro Ad ein **Longevity-Score**, Aggregation
pro Page (Anzahl aktiver Creatives, Hook-Cluster), eine sortierte Tabelle
"wahrscheinlich skalierende Ads" und eine Hook-/Angle-Muster-Liste als
Inspirationspool fuer die Creative-Generierung.

Architektur (wichtig): Dieses Modul ruft das MCP NICHT selbst auf. Der MCP-Call
laeuft ueber den Agenten/Claude; das Modul ist reine **Parsing-/Score-/Report-
Logik** und damit gegen gespeicherte Beispiel-Payloads unit-testbar (ohne
Live-MCP).

Wissensgrundlage:
  AgentischesArbeiten/docs/marketing/research/2026-06-24_meta-ad-library-zugriff-budget.md
  -> §1 real verfuegbare Felder, §2 Proxy-Signale + Longevity-Score, §3 Scan-Ablauf.

> [!important] EHRLICHKEIT (kein Silent-Fake) — Pflicht-Disclaimer
> Kommerzieller **Spend / Impressions / Reach ist NICHT abrufbar** (weder im
> MCP-Payload noch ueber die offizielle Public API; Spend-Ranges nur fuer
> politische/Issue-Ads). Dieses Modul nutzt ausschliesslich **Proxy-Signale**:
> Longevity (Tage seit creation, ACTIVE), Creative-Multiplikation pro Page,
> Re-Serving (delivery_start >> creation), Hook-Wiederholung. Der Longevity-Score
> ist eine **Priorisierung fuer manuelle Sichtung**, KEINE Budget-Wahrheit.
> `PROXY_DISCLAIMER` wird in jedem Report mit ausgegeben.

Multi-Projekt: enthaelt KEINE projekt-spezifischen Werte (kein Wettbewerber, kein
Land hartkodiert) — Thema/Page-IDs/Land kommen als Parameter, Default Land DE.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, datetime, timezone


# --- Pflicht-Disclaimer (kein Silent-Fake) ----------------------------------
PROXY_DISCLAIMER = (
    "Hinweis (Grenzen der Aussage): Meta gibt fuer kommerzielle Ads KEINEN Spend / "
    "keine Impressions / keine Reichweite preis — weder im MCP-Payload noch ueber "
    "die offizielle Public API (Spend-Ranges nur fuer politische/Issue-Ads). Dieser "
    "Scan beruht ausschliesslich auf PROXY-SIGNALEN (Longevity, Creative-Multiplikation "
    "pro Page, Re-Serving, Hook-Wiederholung). Der Longevity-Score ist eine "
    "Priorisierung fuer die manuelle Sichtung, KEINE Budget-Wahrheit. Lange Laufzeit "
    "kann auch Always-on-Branding mit kleinem Budget sein; viele Varianten koennen "
    "auch eine Testphase sein. Nur fuer Inspiration (Hook-/Angle-Muster) nutzen — kein "
    "1:1-Kopieren von Creatives/Claims, kein Bulk-Scraping."
)

# Land-Default (Multi-Projekt: ISO-2, ueberschreibbar).
DEFAULT_COUNTRY = "DE"

# Die real verfuegbaren Felder pro Ad (empirisch, Research §1). KEIN Spend/Reach.
AD_FIELDS: tuple[str, ...] = (
    "id",
    "page_id",
    "page_name",
    "ad_creative_link_title",  # = Hook
    "ad_creation_time",
    "ad_delivery_start_time",
    "ad_snapshot_url",
)


# --- Zeit-Helfer ------------------------------------------------------------
def _to_epoch(value) -> int | None:
    """Normalisiert ein Zeitfeld (Unix-Epoch int/str ODER ISO-Datum) auf Epoch-Sekunden.

    Der MCP liefert Unix-Epoch (Research §1). Wir akzeptieren defensiv auch
    ISO-8601-Strings (YYYY-MM-DD oder voll), damit Fixtures lesbar bleiben.
    Gibt None zurueck, wenn das Feld fehlt/leer/unparsebar ist.
    """
    if value is None or value == "":
        return None
    # Schon numerisch (Epoch).
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip()
    if not s:
        return None
    # Reiner Integer-String = Epoch.
    if s.lstrip("-").isdigit():
        return int(s)
    # ISO-Datum/Datetime.
    try:
        s_norm = s.replace("Z", "+00:00")
        if len(s_norm) == 10:  # YYYY-MM-DD
            dt = datetime.fromisoformat(s_norm).replace(tzinfo=timezone.utc)
        else:
            dt = datetime.fromisoformat(s_norm)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())
    except ValueError:
        return None


def _epoch_to_date(epoch: int | None) -> date | None:
    if epoch is None:
        return None
    return datetime.fromtimestamp(epoch, tz=timezone.utc).date()


def _today() -> date:
    return datetime.now(tz=timezone.utc).date()


# --- Parsing: rohe MCP-Eintraege -> ParsedAd --------------------------------
@dataclass(frozen=True)
class ParsedAd:
    """Eine einzelne Ad mit genau den real verfuegbaren Feldern (Research §1).

    KEIN Spend/Impressions/Reach — die kommen nicht im Payload. `longevity_score`
    und `active_days` werden in scan_report() gefuellt (Page-Kontext noetig).
    """
    id: str
    page_id: str
    page_name: str
    hook: str  # = ad_creative_link_title
    creation_epoch: int | None
    delivery_start_epoch: int | None
    snapshot_url: str
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def creation_date(self) -> date | None:
        return _epoch_to_date(self.creation_epoch)

    @property
    def delivery_start_date(self) -> date | None:
        return _epoch_to_date(self.delivery_start_epoch)

    def active_days(self, today: date | None = None) -> int:
        """Tage seit `ad_creation_time` bis heute (Proxy fuer Laufzeit, Research §2).

        Kein `ad_delivery_stop_time` im Payload -> Longevity nur ueber creation +
        heute angenaehert. Fehlt die creation_time, sind es 0 Tage (kein Signal).
        Negative Werte (Zukunfts-Datum) werden auf 0 geklemmt.
        """
        if self.creation_epoch is None:
            return 0
        ref = today or _today()
        cdate = self.creation_date
        if cdate is None:
            return 0
        return max(0, (ref - cdate).days)

    def re_serving_gap_days(self) -> int:
        """Tage zwischen creation und (spaeterem) delivery_start = Re-Serving (Research §2).

        Grosser positiver Wert = bewaehrtes Creative wurde neu gestartet
        (klassisches Skalierungsmuster). 0, wenn Felder fehlen oder kein Re-Serving.
        """
        if self.creation_epoch is None or self.delivery_start_epoch is None:
            return 0
        gap = (self.delivery_start_date - self.creation_date).days  # type: ignore[operator]
        return max(0, gap)


def parse_ad(entry: dict) -> ParsedAd:
    """Parst einen rohen MCP-Ad-Eintrag defensiv in ein ParsedAd.

    Fehlende Felder werden zu leeren Strings / None (Edge-Case-fest). Akzeptiert
    Epoch-int/str und — defensiv — ISO-Datums-Strings.
    """
    return ParsedAd(
        id=str(entry.get("id", "") or ""),
        page_id=str(entry.get("page_id", "") or ""),
        page_name=str(entry.get("page_name", "") or "").strip(),
        hook=str(entry.get("ad_creative_link_title", "") or "").strip(),
        creation_epoch=_to_epoch(entry.get("ad_creation_time")),
        delivery_start_epoch=_to_epoch(entry.get("ad_delivery_start_time")),
        snapshot_url=str(entry.get("ad_snapshot_url", "") or "").strip(),
        raw=dict(entry),
    )


def parse_ads(entries: list[dict]) -> list[ParsedAd]:
    """Parst eine Liste roher MCP-Eintraege. Nicht-dict-/leere Eintraege werden uebersprungen."""
    out: list[ParsedAd] = []
    for e in entries or []:
        if isinstance(e, dict):
            out.append(parse_ad(e))
    return out


# --- Longevity-Score --------------------------------------------------------
# SKILL-052 / Research §2 — fixierte Heuristik:
#   score = aktive_Tage(creation->heute) * log(1 + Anzahl_aktiver_Varianten_der_Page)
# Hoch = lange aktiv UND breit ausgerollt. Bewusst grob; ersetzt keinen echten
# Spend, rankt aber "wahrscheinliche Gewinner" zuverlaessig nach oben.
def longevity_score(active_days: int, page_variant_count: int) -> float:
    """Longevity-Score (Proxy) fuer eine Ad.

    Formel (fixiert, Research §2):
        score = active_days * log(1 + page_variant_count)

    Args:
        active_days: Tage seit `ad_creation_time` bis heute (>= 0).
        page_variant_count: Anzahl der (aktiven) Ad-Varianten derselben Page im
            Scan (>= 1). Die Page selbst zaehlt mit -> log(1+1)=log(2) als Boden,
            damit eine Einzel-Ad nicht auf 0 faellt.

    Returns:
        Score als float (>= 0). 0, wenn active_days == 0.

    Raises:
        ValueError: bei negativen Eingaben.
    """
    if active_days < 0 or page_variant_count < 0:
        raise ValueError("active_days und page_variant_count muessen >= 0 sein.")
    return float(active_days) * math.log(1 + page_variant_count)


# --- Aggregation pro Page ---------------------------------------------------
@dataclass
class PageAggregate:
    """Aggregat pro Advertiser-Page (Proxy-Signale, Research §2).

    Attributes:
        page_id / page_name: Identifikation.
        active_ad_count: Anzahl der Ads dieser Page im Scan (Creative-Multiplikation).
        hook_clusters: Hook (normalisiert) -> Anzahl Ads mit diesem Hook (Hook-Wiederholung).
        max_active_days: laengste Laufzeit einer Ad der Page.
        re_serving_count: Anzahl Ads mit Re-Serving (delivery_start >> creation).
        top_score: hoechster Longevity-Score einer Ad der Page.
    """
    page_id: str
    page_name: str
    active_ad_count: int = 0
    hook_clusters: dict[str, int] = field(default_factory=dict)
    max_active_days: int = 0
    re_serving_count: int = 0
    top_score: float = 0.0


def _normalize_hook(hook: str) -> str:
    """Normalisiert einen Hook fuer das Clustering (Kleinschreibung, Whitespace, " | "-Karten)."""
    if not hook:
        return ""
    # Mehrkarten-Titel ("A | B | C") -> erste Karte als Cluster-Schluessel.
    first = hook.split(" | ")[0]
    return " ".join(first.lower().split())


def display_hook(hook: str) -> str:
    """Lesbarer Hook fuer Tabellen/Output: dedupliziert wiederholte " | "-Karten.

    Der MCP liefert Mehrkarten-Titel oft als "A | A | A" (gleiche Karte mehrfach).
    Fuer die Anzeige reicht die erste eindeutige Karte; bei echt verschiedenen Karten
    bleiben alle (mit " | " verbunden). Aendert NICHT das Clustering.
    """
    if not hook:
        return ""
    parts = [p.strip() for p in hook.split(" | ") if p.strip()]
    seen: list[str] = []
    for p in parts:
        if p not in seen:
            seen.append(p)
    return " | ".join(seen) if seen else hook.strip()


def aggregate_by_page(ads: list[ParsedAd], today: date | None = None) -> dict[str, PageAggregate]:
    """Aggregiert ParsedAds pro Page: Anzahl aktiver Creatives + Hook-Cluster + Longevity.

    page_variant_count fuer den Score = Anzahl Ads der jeweiligen Page im Scan.
    """
    ref = today or _today()
    # 1. Pass: Ads pro Page zaehlen (= page_variant_count).
    counts: dict[str, int] = {}
    for ad in ads:
        key = ad.page_id or ad.page_name
        counts[key] = counts.get(key, 0) + 1

    aggs: dict[str, PageAggregate] = {}
    for ad in ads:
        key = ad.page_id or ad.page_name
        agg = aggs.get(key)
        if agg is None:
            agg = PageAggregate(page_id=ad.page_id, page_name=ad.page_name)
            aggs[key] = agg
        agg.active_ad_count += 1
        norm = _normalize_hook(ad.hook)
        if norm:
            agg.hook_clusters[norm] = agg.hook_clusters.get(norm, 0) + 1
        adays = ad.active_days(ref)
        agg.max_active_days = max(agg.max_active_days, adays)
        if ad.re_serving_gap_days() > 0:
            agg.re_serving_count += 1
        score = longevity_score(adays, counts[key])
        agg.top_score = max(agg.top_score, score)
    return aggs


# --- Hook-/Angle-Muster -----------------------------------------------------
@dataclass(frozen=True)
class HookCluster:
    """Ein wiederkehrender Hook ueber Pages/Ads hinweg (Inspirationspool)."""
    hook: str            # repraesentativer (erst gesehener) Original-Hook
    occurrences: int     # Gesamtzahl Ads mit diesem (normalisierten) Hook
    page_count: int      # ueber wie viele verschiedene Pages er auftaucht


def extract_hook_patterns(ads: list[ParsedAd], min_occurrences: int = 1) -> list[HookCluster]:
    """Extrahiert wiederkehrende Hook-/Angle-Muster als Inspirationspool (Research §3.5).

    Clustert ueber den normalisierten `ad_creative_link_title`. Sortiert nach
    Haeufigkeit (occurrences desc), dann Page-Breite (page_count desc).

    Args:
        ads: geparste Ads.
        min_occurrences: nur Cluster mit >= so vielen Ads zurueckgeben (Default 1).

    Returns:
        Sortierte Liste von HookCluster. Leere Hooks werden ignoriert.
    """
    by_norm: dict[str, dict] = {}
    for ad in ads:
        norm = _normalize_hook(ad.hook)
        if not norm:
            continue
        bucket = by_norm.setdefault(
            norm, {"original": ad.hook, "occurrences": 0, "pages": set()}
        )
        bucket["occurrences"] += 1
        bucket["pages"].add(ad.page_id or ad.page_name)

    clusters = [
        HookCluster(
            hook=display_hook(b["original"]),
            occurrences=b["occurrences"],
            page_count=len(b["pages"]),
        )
        for b in by_norm.values()
        if b["occurrences"] >= min_occurrences
    ]
    clusters.sort(key=lambda c: (c.occurrences, c.page_count), reverse=True)
    return clusters


# --- Themen-Sweep-Auswertung ------------------------------------------------
@dataclass(frozen=True)
class TopAdvertiser:
    page_id: str
    page_name: str
    ad_count: int  # wie oft die Page im Sweep auftaucht


def theme_sweep(search_result: dict) -> dict:
    """Wertet das Roh-Ergebnis eines Themen-Sweeps aus (EARS-1, Research §3.1/§3.2).

    Erwartet das MCP-Ergebnis als dict mit `estimated_total_count` (top-level) und
    `data`/`ads` (Liste). Extrahiert die Markttiefe + die mehrfach auftauchenden
    Top-Advertiser-Pages.

    Returns:
        dict mit:
          estimated_total_count: int | None
          ad_count: Anzahl tatsaechlich gelieferter Ads
          top_advertisers: List[TopAdvertiser] (absteigend nach ad_count)
    """
    total = search_result.get("estimated_total_count")
    entries = search_result.get("data") or search_result.get("ads") or []
    ads = parse_ads(entries)

    counts: dict[str, dict] = {}
    for ad in ads:
        key = ad.page_id or ad.page_name
        if not key:
            continue
        b = counts.setdefault(key, {"page_id": ad.page_id, "page_name": ad.page_name, "n": 0})
        b["n"] += 1

    top = [
        TopAdvertiser(page_id=b["page_id"], page_name=b["page_name"], ad_count=b["n"])
        for b in counts.values()
    ]
    top.sort(key=lambda t: t.ad_count, reverse=True)
    return {
        "estimated_total_count": total,
        "ad_count": len(ads),
        "top_advertisers": top,
    }


# --- Scan-Report (Tabelle + Hooks + Disclaimer) -----------------------------
@dataclass(frozen=True)
class ScanRow:
    """Eine Zeile der Tabelle 'wahrscheinlich skalierende Ads'."""
    page_name: str
    hook: str
    active_since: str        # YYYY-MM-DD oder "?"
    active_days: int
    variant_count: int       # Ads der Page im Scan
    re_served: bool
    longevity_score: float
    snapshot_url: str


def scan_report(
    entries: list[dict],
    *,
    theme: str = "",
    country: str = DEFAULT_COUNTRY,
    today: date | None = None,
) -> dict:
    """Baut den vollstaendigen Scan-Report aus rohen MCP-Eintraegen (EARS-2/3/4).

    Args:
        entries: Liste roher Ad-Eintraege (aus einem oder mehreren MCP-Calls).
        theme: optionales Seed-Thema (nur fuer Header, projektneutral).
        country: ISO-2-Land (Default DE).
        today: Referenzdatum (testbar; sonst heute UTC).

    Returns:
        dict mit:
          theme, country, disclaimer (PROXY_DISCLAIMER, Pflicht),
          ad_count, page_count,
          rows: List[ScanRow] absteigend nach longevity_score,
          hook_patterns: List[HookCluster],
          page_aggregates: dict[str, PageAggregate].
    """
    ref = today or _today()
    ads = parse_ads(entries)
    aggs = aggregate_by_page(ads, today=ref)

    # variant_count pro Page = active_ad_count des Aggregats.
    variant_by_key = {k: agg.active_ad_count for k, agg in aggs.items()}

    rows: list[ScanRow] = []
    for ad in ads:
        key = ad.page_id or ad.page_name
        vcount = variant_by_key.get(key, 1)
        adays = ad.active_days(ref)
        score = longevity_score(adays, vcount)
        cdate = ad.creation_date
        rows.append(
            ScanRow(
                page_name=ad.page_name or "(unbekannt)",
                hook=display_hook(ad.hook) or "(kein Titel)",
                active_since=cdate.isoformat() if cdate else "?",
                active_days=adays,
                variant_count=vcount,
                re_served=ad.re_serving_gap_days() > 0,
                longevity_score=round(score, 2),
                snapshot_url=ad.snapshot_url,
            )
        )
    # Absteigend nach Score; bei Gleichstand nach active_days, dann variant_count.
    rows.sort(
        key=lambda r: (r.longevity_score, r.active_days, r.variant_count),
        reverse=True,
    )

    return {
        "theme": theme,
        "country": country,
        "disclaimer": PROXY_DISCLAIMER,
        "ad_count": len(ads),
        "page_count": len(aggs),
        "rows": rows,
        "hook_patterns": extract_hook_patterns(ads),
        "page_aggregates": aggs,
    }


def render_report_markdown(report: dict) -> str:
    """Rendert einen scan_report() als lesbares Markdown (Tabelle + Hooks + Disclaimer).

    Der Disclaimer steht IMMER mit im Output (EARS-4, kein Silent-Fake).
    """
    theme = report.get("theme") or "(kein Thema)"
    country = report.get("country", DEFAULT_COUNTRY)
    lines: list[str] = []
    lines.append(f"# Ad-Library-Scan — {theme} ({country})")
    lines.append("")
    lines.append(
        f"Ads im Scan: {report.get('ad_count', 0)} | "
        f"Pages: {report.get('page_count', 0)}"
    )
    lines.append("")
    lines.append("> [!warning] Proxy-Disclaimer (kein Spend abrufbar)")
    for chunk in report.get("disclaimer", PROXY_DISCLAIMER).split(". "):
        chunk = chunk.strip()
        if chunk:
            lines.append(f"> {chunk}.")
    lines.append("")

    lines.append("## Wahrscheinlich skalierende Ads (Longevity-Score, absteigend)")
    lines.append("")
    lines.append(
        "| Advertiser | Hook | aktiv seit | Tage | #Varianten | Re-Serving | Longevity-Score | Snapshot |"
    )
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in report.get("rows", []):
        snap = f"[Link]({r.snapshot_url})" if r.snapshot_url else "—"
        re_s = "ja" if r.re_served else "—"
        lines.append(
            f"| {r.page_name} | {r.hook} | {r.active_since} | {r.active_days} | "
            f"{r.variant_count} | {re_s} | {r.longevity_score} | {snap} |"
        )
    lines.append("")

    lines.append("## Hook-/Angle-Muster (Inspirationspool — nur Inspiration, kein 1:1-Kopieren)")
    lines.append("")
    patterns = report.get("hook_patterns", [])
    if not patterns:
        lines.append("_(keine Hooks extrahiert)_")
    else:
        lines.append("| Hook | Vorkommen | Pages |")
        lines.append("|---|---|---|")
        for c in patterns:
            lines.append(f"| {c.hook} | {c.occurrences} | {c.page_count} |")
    lines.append("")
    return "\n".join(lines)
