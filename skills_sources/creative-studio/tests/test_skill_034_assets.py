"""Tests fuer SKILL-034 (assets.py) — Konvention, meta.json Round-Trip, Release-Warnung."""
from __future__ import annotations

from creative_studio.assets import (
    Asset,
    AssetRegistry,
    asset_warnings,
    asset_root,
    ensure_source_layout,
    load_registry,
    save_registry,
    register_asset,
    meta_path,
    ORIGINALS_DIRNAME,
    WEB_DIRNAME,
)


def test_ears1_konvention_pfad_relativ_zum_projekt(tmp_path):
    """EARS-1/EARS-4: Asset-Root liegt unter <projekt>/marketing/brand-assets (kein Hartcode)."""
    root = asset_root(tmp_path)
    assert root == tmp_path / "marketing" / "brand-assets"


def test_ears1_layout_originals_und_web(tmp_path):
    """EARS-1: Konventions-Layout (originals/, web/) wird angelegt."""
    base = ensure_source_layout(tmp_path, "picdrop-jaQGXDaJAS")
    assert (base / ORIGINALS_DIRNAME).is_dir()
    assert (base / WEB_DIRNAME).is_dir()
    assert base.name == "picdrop-jaQGXDaJAS"


def test_ears2_meta_json_round_trip(tmp_path):
    """EARS-2: meta.json fuehrt je Datei quelle/lizenz/model_release/nutzung/aufnahmedatum."""
    quelle = "evisible"
    asset = Asset(
        dateiname="00_header.jpg",
        quelle="evisible | PHOTOGRAPHY",
        lizenz="Ad-Nutzung lt. Vertrag 2025",
        model_release="yes",
        nutzung="beides",
        aufnahmedatum="2025-04-24",
    )
    register_asset(tmp_path, quelle, asset)

    # meta.json existiert am Konventions-Pfad
    assert meta_path(tmp_path, quelle).is_file()

    # Round-Trip: erneut laden -> identische Felder
    reg = load_registry(tmp_path, quelle)
    loaded = reg.get("00_header.jpg")
    assert loaded is not None
    assert loaded.quelle == "evisible | PHOTOGRAPHY"
    assert loaded.lizenz == "Ad-Nutzung lt. Vertrag 2025"
    assert loaded.model_release == "yes"
    assert loaded.nutzung == "beides"
    assert loaded.aufnahmedatum == "2025-04-24"


def test_ears2_normalisierung_unbekannter_werte(tmp_path):
    """EARS-2: unbekanntes model_release/nutzung faellt auf sichere Defaults zurueck."""
    reg = AssetRegistry(quelle="q")
    reg.add(Asset(dateiname="x.jpg", model_release="vielleicht", nutzung="werbung"))
    save_registry(tmp_path, reg)

    loaded = load_registry(tmp_path, "q").get("x.jpg")
    assert loaded.model_release == "unklar"
    assert loaded.nutzung == "organic"


def test_ears3_release_warnung_bei_paid():
    """EARS-3: model_release != yes bei paid -> Warnung (keine harte Sperre)."""
    asset = Asset(dateiname="00_header.jpg", lizenz="x", model_release="unklar", nutzung="paid")
    warn = asset_warnings(asset, use="paid")
    assert any("Model-Release" in w for w in warn)


def test_ears3_keine_release_warnung_bei_yes_paid():
    """EARS-3: model_release == yes bei paid -> keine Release-Warnung."""
    asset = Asset(dateiname="00_header.jpg", lizenz="Vertrag", model_release="yes", nutzung="paid")
    warn = asset_warnings(asset, use="paid")
    assert not any("Model-Release" in w for w in warn)


def test_ears3_registry_warnings_sammelt_je_asset(tmp_path):
    """EARS-3: AssetRegistry.warnings liefert Warnungen je betroffenem Asset."""
    reg = AssetRegistry(quelle="q")
    reg.add(Asset(dateiname="ok.jpg", lizenz="v", model_release="yes", nutzung="paid"))
    reg.add(Asset(dateiname="risk.jpg", lizenz="v", model_release="no", nutzung="paid"))
    warns = reg.warnings(use="paid")
    assert "risk.jpg" in warns
    assert "ok.jpg" not in warns
