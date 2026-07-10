"""SKILL-052 — Tests fuer ad_library.py (Ad-Library-Scan + Longevity-Score, Proxy).

1 EARS = mind. 1 Test. Projektneutral, pytest. Fixture-Daten realitaetsnah aus der
Research-Doku (2026-06-24_meta-ad-library-zugriff-budget.md §1: JinTo Solutions,
PIOLA, KI-Weiterbildungszentrum etc.). Referenzdatum fix gesetzt -> deterministisch.
"""
from __future__ import annotations

import math
from datetime import date

import pytest

from creative_studio import ad_library as al


# Fixes Referenzdatum (heute), damit active_days deterministisch ist.
TODAY = date(2026, 6, 24)


def _epoch(y, m, d) -> int:
    from datetime import datetime, timezone
    return int(datetime(y, m, d, tzinfo=timezone.utc).timestamp())


# --- Fixture: realistische MCP-Ad-Eintraege (Research §1) -------------------
@pytest.fixture
def sample_entries() -> list[dict]:
    return [
        # JinTo Solutions — Re-Serving-Beispiel aus der Doku:
        # erstellt 2026-05-15, re-served 2026-06-19 (5+ Wochen Longevity).
        {
            "id": "1398586478698792",
            "page_id": "829515410244190",
            "page_name": "JinTo Solutions",
            "ad_creative_link_title": "Gratis KI Automation Guide",
            "ad_creation_time": _epoch(2026, 5, 15),
            "ad_delivery_start_time": _epoch(2026, 6, 19),
            "ad_snapshot_url": "https://www.facebook.com/ads/library/?id=1398586478698792",
        },
        # JinTo Variante 2 — selber Hook, juenger, kein Re-Serving.
        {
            "id": "1398586478698793",
            "page_id": "829515410244190",
            "page_name": "JinTo Solutions",
            "ad_creative_link_title": "Gratis KI Automation Guide",
            "ad_creation_time": _epoch(2026, 6, 10),
            "ad_delivery_start_time": _epoch(2026, 6, 10),
            "ad_snapshot_url": "https://www.facebook.com/ads/library/?id=1398586478698793",
        },
        # PIOLA Automations — Einzel-Ad, anderer Hook, mittlere Laufzeit.
        {
            "id": "555000111",
            "page_id": "111222333",
            "page_name": "PIOLA Automations",
            "ad_creative_link_title": "200 Bewerbungen in 30 Sekunden",
            "ad_creation_time": _epoch(2026, 6, 1),
            "ad_delivery_start_time": _epoch(2026, 6, 1),
            "ad_snapshot_url": "https://www.facebook.com/ads/library/?id=555000111",
        },
        # KI-Weiterbildungszentrum — sehr lange aktiv, Einzel-Ad.
        {
            "id": "777888999",
            "page_id": "444555666",
            "page_name": "KI-Weiterbildungszentrum.de",
            "ad_creative_link_title": "Werde Spezialist/in fuer KI-Transformation & Automatisierung",
            "ad_creation_time": _epoch(2026, 3, 1),
            "ad_delivery_start_time": _epoch(2026, 3, 1),
            "ad_snapshot_url": "https://www.facebook.com/ads/library/?id=777888999",
        },
    ]


# --- EARS-1: Themen-Sweep -> total_count + Top-Advertiser --------------------
def test_ears1_theme_sweep_extracts_count_and_top_advertisers(sample_entries):
    mcp_result = {"estimated_total_count": 338, "data": sample_entries}
    sweep = al.theme_sweep(mcp_result)
    assert sweep["estimated_total_count"] == 338
    assert sweep["ad_count"] == 4
    # JinTo taucht 2x auf -> Top-Advertiser zuerst.
    assert sweep["top_advertisers"][0].page_name == "JinTo Solutions"
    assert sweep["top_advertisers"][0].ad_count == 2


def test_ears1_theme_sweep_accepts_ads_key_and_empty():
    assert al.theme_sweep({"ads": []})["ad_count"] == 0
    assert al.theme_sweep({})["estimated_total_count"] is None


# --- EARS-2: Page-Drilldown erfasst real verfuegbare Felder, kein Spend -----
def test_ears2_parse_only_real_fields(sample_entries):
    ad = al.parse_ad(sample_entries[0])
    assert ad.id == "1398586478698792"
    assert ad.page_name == "JinTo Solutions"
    assert ad.hook == "Gratis KI Automation Guide"
    assert ad.creation_date == date(2026, 5, 15)
    assert ad.delivery_start_date == date(2026, 6, 19)
    assert ad.snapshot_url.endswith("=1398586478698792")
    # Kein erfundenes Spend-Feld irgendwo.
    assert not hasattr(ad, "spend")
    assert "spend" not in al.AD_FIELDS
    assert "reach" not in al.AD_FIELDS
    assert "impressions" not in al.AD_FIELDS


def test_ears2_re_serving_detection(sample_entries):
    ad = al.parse_ad(sample_entries[0])  # 2026-05-15 -> 2026-06-19
    assert ad.re_serving_gap_days() == 35
    ad2 = al.parse_ad(sample_entries[1])  # gleicher creation/delivery
    assert ad2.re_serving_gap_days() == 0


# --- EARS-3: Longevity-Score-Formel + Sortierung ----------------------------
def test_longevity_score_formula():
    # score = active_days * log(1 + variant_count)
    assert al.longevity_score(40, 1) == pytest.approx(40 * math.log(2))
    assert al.longevity_score(40, 5) == pytest.approx(40 * math.log(6))
    # active_days=0 -> 0
    assert al.longevity_score(0, 10) == 0.0
    # Mehr Varianten -> hoeherer Score bei gleichen Tagen.
    assert al.longevity_score(30, 5) > al.longevity_score(30, 1)


def test_longevity_score_rejects_negative():
    with pytest.raises(ValueError):
        al.longevity_score(-1, 2)
    with pytest.raises(ValueError):
        al.longevity_score(10, -1)


def test_ears3_rows_sorted_descending(sample_entries):
    report = al.scan_report(sample_entries, theme="KI Automatisierung", today=TODAY)
    scores = [r.longevity_score for r in report["rows"]]
    assert scores == sorted(scores, reverse=True), "Rows nicht absteigend nach Score"
    # KI-Weiterbildungszentrum (seit 2026-03-01, ~115 Tage) sollte oben stehen,
    # trotz Einzel-Ad — lange Laufzeit dominiert.
    assert report["rows"][0].page_name == "KI-Weiterbildungszentrum.de"


def test_ears3_active_days_uses_creation(sample_entries):
    report = al.scan_report(sample_entries, today=TODAY)
    jinto_old = next(r for r in report["rows"] if r.active_since == "2026-05-15")
    assert jinto_old.active_days == (TODAY - date(2026, 5, 15)).days  # 40
    assert jinto_old.variant_count == 2  # JinTo hat 2 Ads im Scan


# --- EARS-4: Tabelle + Hook-Muster + Disclaimer Pflicht ---------------------
def test_scan_table_and_hooks(sample_entries):
    report = al.scan_report(sample_entries, theme="KI", today=TODAY)
    assert report["ad_count"] == 4
    assert report["page_count"] == 3  # JinTo, PIOLA, KI-Weiterbildungszentrum
    assert len(report["rows"]) == 4
    # Hook-Cluster: "gratis ki automation guide" 2x ueber 1 Page.
    patterns = {c.hook.lower(): c for c in report["hook_patterns"]}
    assert "gratis ki automation guide" in patterns
    assert patterns["gratis ki automation guide"].occurrences == 2
    # Staerkster Hook-Cluster steht vorne (occurrences desc).
    assert report["hook_patterns"][0].occurrences == 2


def test_disclaimer_present(sample_entries):
    report = al.scan_report(sample_entries, today=TODAY)
    assert report["disclaimer"] == al.PROXY_DISCLAIMER
    assert "Spend" in report["disclaimer"]
    assert "Proxy" in report["disclaimer"] or "PROXY" in report["disclaimer"]
    # Auch im gerenderten Markdown sichtbar.
    md = al.render_report_markdown(report)
    assert "Proxy-Disclaimer" in md
    assert "Longevity-Score" in md
    assert "| Advertiser |" in md


def test_page_aggregation(sample_entries):
    aggs = al.aggregate_by_page(al.parse_ads(sample_entries), today=TODAY)
    jinto = aggs["829515410244190"]
    assert jinto.active_ad_count == 2
    assert jinto.hook_clusters["gratis ki automation guide"] == 2
    assert jinto.re_serving_count == 1
    assert jinto.max_active_days == (TODAY - date(2026, 5, 15)).days


# --- EARS-5: Projektneutral (kein hartkodierter Wettbewerber/Land) ----------
def test_scan_project_neutral():
    # Default-Land ist DE, aber ueberschreibbar; kein Projektwert hartkodiert.
    assert al.DEFAULT_COUNTRY == "DE"
    report = al.scan_report([], theme="beliebig", country="AT", today=TODAY)
    assert report["country"] == "AT"
    # Quellcode-Konstanten enthalten keinen konkreten Wettbewerber-/Projektnamen.
    blob = (al.PROXY_DISCLAIMER + " ".join(al.AD_FIELDS)).lower()
    for forbidden in ("jakob", "jinto", "piola", "immobilien", "mentoring"):
        assert forbidden not in blob


# --- Edge-Cases: fehlende Felder --------------------------------------------
def test_edge_missing_fields_do_not_crash():
    entries = [
        {},  # voellig leer
        {"id": "x"},  # nur id
        {"page_name": "Nur Name", "ad_creative_link_title": "Hook ohne Zeit"},
        {"id": "y", "ad_creation_time": "", "ad_delivery_start_time": None},
        "kein dict",  # wird uebersprungen
    ]
    report = al.scan_report(entries, today=TODAY)
    # 4 dict-Eintraege werden geparst, der String uebersprungen.
    assert report["ad_count"] == 4
    # Ad ohne creation_time -> active_days 0, Score 0.
    zero_rows = [r for r in report["rows"] if r.active_days == 0]
    assert zero_rows, "Ads ohne creation_time sollten active_days 0 haben"
    # Markdown rendert trotz fehlender Felder.
    md = al.render_report_markdown(report)
    assert "aktiv seit" in md


def test_edge_iso_date_strings_accepted():
    # Defensiv: ISO-Datums-Strings statt Epoch.
    e = {
        "id": "iso1",
        "page_name": "ISO Page",
        "ad_creative_link_title": "Hook",
        "ad_creation_time": "2026-05-15",
        "ad_delivery_start_time": "2026-06-19T10:00:00Z",
    }
    ad = al.parse_ad(e)
    assert ad.creation_date == date(2026, 5, 15)
    assert ad.delivery_start_date == date(2026, 6, 19)


def test_display_hook_dedupes_multicard_titles():
    # MCP liefert oft "A | A | A" -> Anzeige nur einmal, Clustering unveraendert.
    assert al.display_hook("Gratis KI Automation Guide | Gratis KI Automation Guide") == \
        "Gratis KI Automation Guide"
    # Echt verschiedene Karten bleiben erhalten.
    assert al.display_hook("Hook A | Hook B") == "Hook A | Hook B"
    assert al.display_hook("") == ""
    # In der Tabelle erscheint der deduplizierte Hook.
    entries = [{
        "id": "m", "page_id": "p1", "page_name": "P",
        "ad_creative_link_title": "Gratis Guide | Gratis Guide",
        "ad_creation_time": _epoch(2026, 5, 1),
    }]
    report = al.scan_report(entries, today=TODAY)
    assert report["rows"][0].hook == "Gratis Guide"


def test_edge_future_creation_clamps_to_zero():
    e = {"id": "f", "page_name": "P", "ad_creation_time": _epoch(2027, 1, 1)}
    ad = al.parse_ad(e)
    assert ad.active_days(TODAY) == 0
