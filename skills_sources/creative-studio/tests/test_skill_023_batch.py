"""SKILL-023 — Tests fuer die Batch-/Varianten-Engine + manifest.json.

1 EARS = mind. 1 Test. Der echte Playwright-Render wird hier gemockt (deterministisch,
kein Chromium pro Test); der reale End-to-End-Lauf ist im Ticket als Real-Test belegt.
"""
import json
import pathlib

import pytest

from creative_studio import batch
from creative_studio.specs import make_utm_content, make_variant_id


def _fake_render(monkeypatch, out_root_holder):
    """Ersetzt render_image.render durch einen Stub, der eine leere PNG-Datei anlegt."""
    def fake(content, format_keys, brand, out_dir, debug_safe=False, write_meta=True, **kwargs):
        written = []
        stem = content.ad_id or "creative"
        for key in format_keys:
            p = pathlib.Path(out_dir) / f"{stem}__{key}.png"
            p.write_bytes(b"\x89PNG\r\n")  # Minimal-Marker, kein echtes Bild noetig
            written.append(str(p))
        return written
    monkeypatch.setattr(batch, "render", fake)


def _job():
    return {
        "ad_id": "h1-immo",
        "formats": ["feed_4x5", "story_9x16"],
        "media": ["image"],
        "variants": [
            {"framework": "bab", "headline": "A", "cta": "Go"},
            {"framework": "pas", "headline": "B", "cta": "Go"},
            {"framework": "aida", "headline": "C", "cta": "Go"},
        ],
    }


# EARS-1: ein Lauf -> alle N x M Kombinationen gerendert.
def test_batch_renders_n_times_m(tmp_path, monkeypatch):
    _fake_render(monkeypatch, None)
    manifest = batch.run_batch(_job(), str(tmp_path))
    pngs = sorted(tmp_path.glob("*.png"))
    assert len(pngs) == 6           # 3 Hooks x 2 Formate
    assert manifest["count"] == 6


# EARS-2: manifest.json mit allen Pflichtfeldern je Eintrag.
def test_manifest_written_with_fields(tmp_path, monkeypatch):
    _fake_render(monkeypatch, None)
    batch.run_batch(_job(), str(tmp_path))
    manifest_path = tmp_path / "manifest.json"
    assert manifest_path.is_file()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert len(data["variants"]) == 6
    required = {"variant_id", "ad_id", "framework", "hook", "format", "media", "file", "utm_content"}
    for e in data["variants"]:
        assert required <= set(e)
        assert e["media"] == "image"
        assert e["file"] and e["file"].endswith(".png")
        # utm_content stammt aus specs.py-Systematik (SKILL-024), passend zur variant_id
        assert e["utm_content"] == make_utm_content(e["variant_id"])


# EARS-2: variant_ids sind alle eindeutig.
def test_manifest_variant_ids_unique(tmp_path, monkeypatch):
    _fake_render(monkeypatch, None)
    batch.run_batch(_job(), str(tmp_path))
    data = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    vids = [e["variant_id"] for e in data["variants"]]
    assert len(vids) == len(set(vids)) == 6


# EARS-3: gemischte Medien (image + video) ueber dieselbe Struktur; Video als TODO markiert.
def test_mixed_media_video_marked(tmp_path, monkeypatch):
    _fake_render(monkeypatch, None)
    job = _job()
    job["media"] = ["image", "video"]
    data = batch.run_batch(job, str(tmp_path))
    media_types = {e["media"] for e in data["variants"]}
    assert media_types == {"image", "video"}
    videos = [e for e in data["variants"] if e["media"] == "video"]
    assert videos and all(e.get("status") == "not_implemented" for e in videos)
    assert all(e["file"] is None for e in videos)  # kein gefakter Datei-Output


# EARS-4 [multi-projekt]: Brand/Content/Formate nur aus Job/CLI; ad_id steuert Praefix.
def test_no_hardcoded_project_value(tmp_path, monkeypatch):
    _fake_render(monkeypatch, None)
    job = _job()
    job["ad_id"] = "projektX"
    data = batch.run_batch(job, str(tmp_path))
    assert all(e["variant_id"].startswith("projektx__") for e in data["variants"])
    assert all(e["utm_content"].startswith("projektx-") for e in data["variants"])


# EARS-5: einzelner Render-Fehler bricht den Lauf nicht ab, wird je Variante markiert.
def test_single_failure_does_not_abort(tmp_path, monkeypatch):
    calls = {"n": 0}

    def flaky(content, format_keys, brand, out_dir, debug_safe=False, write_meta=True, **kwargs):
        calls["n"] += 1
        if calls["n"] == 2:                       # zweiter Render-Aufruf scheitert
            raise RuntimeError("Chromium-Boom")
        p = pathlib.Path(out_dir) / f"{content.ad_id}__{format_keys[0]}.png"
        p.write_bytes(b"\x89PNG\r\n")
        return [str(p)]

    monkeypatch.setattr(batch, "render", flaky)
    data = batch.run_batch(_job(), str(tmp_path))
    assert data["count"] == 6                     # alle Eintraege im Manifest
    errored = [e for e in data["variants"] if "error" in e]
    assert len(errored) == 1
    assert "Chromium-Boom" in errored[0]["error"]
    ok = [e for e in data["variants"] if e["file"]]
    assert len(ok) == 5                           # restliche 5 erfolgreich


# EARS-6: ohne expliziten Out wird der uebergebene out_dir verwendet (Manifest landet dort).
def test_manifest_lands_in_out_dir(tmp_path, monkeypatch):
    _fake_render(monkeypatch, None)
    sub = tmp_path / "marketing" / "creatives"
    batch.run_batch(_job(), str(sub))
    assert (sub / "manifest.json").is_file()
