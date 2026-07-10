"""SKILL-030 — Tests fuer die Vorschau-Galerie gallery.html (QA-Gate vor Launch).

1 EARS = mind. 1 Test. Geprueft wird der erzeugte HTML-String (kein Browser noetig):
alle variant_ids + utm_content + die Warn-/Fehler-Markierung muessen sichtbar sein.
"""
import json
import pathlib

from creative_studio import gallery


def _manifest():
    """Mini-Manifest: ein OK-Eintrag, einer mit warning, einer mit error,
    plus ein nicht-implementiertes Video (status)."""
    return {
        "ad_id": "h1-immo",
        "formats": ["feed_4x5", "story_9x16"],
        "media": ["image", "video"],
        "count": 4,
        "variants": [
            {
                "variant_id": "h1-immo__bab-h00__feed_4x5", "ad_id": "h1-immo",
                "framework": "bab", "hook": "Sicher anlegen", "format": "feed_4x5",
                "media": "image", "file": "h1-immo__bab-h00__feed_4x5.png",
                "utm_content": "h1-immo-feed_4x5-bab-h00",
            },
            {
                "variant_id": "h1-immo__pas-h01__feed_4x5", "ad_id": "h1-immo",
                "framework": "pas", "hook": "Du verdoppelst", "format": "feed_4x5",
                "media": "image", "file": "h1-immo__pas-h01__feed_4x5.png",
                "utm_content": "h1-immo-feed_4x5-pas-h01",
                "warnings": ["Coaching-Claim-Risiko: 'du verdoppelst' — neutraler formulieren."],
            },
            {
                "variant_id": "h1-immo__aida-h02__story_9x16", "ad_id": "h1-immo",
                "framework": "aida", "hook": "Jetzt starten", "format": "story_9x16",
                "media": "image", "file": "h1-immo__aida-h02__story_9x16.png",
                "utm_content": "h1-immo-story_9x16-aida-h02",
                "error": "RuntimeError: Chromium-Boom",
            },
            {
                "variant_id": "h1-immo__bab-h00__story_9x16", "ad_id": "h1-immo",
                "framework": "bab", "hook": "Sicher anlegen", "format": "story_9x16",
                "media": "video", "file": None,
                "utm_content": "h1-immo-story_9x16-bab-h00",
                "status": "not_implemented",
                "note": "Video-Renderer noch nicht angebunden.",
            },
        ],
    }


def _write_manifest(tmp_path) -> pathlib.Path:
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps(_manifest(), ensure_ascii=False), encoding="utf-8")
    return p


# EARS-1/2: alle Varianten + ihre Metadaten (variant_id, utm_content) im HTML.
def test_gallery_contains_all_variants_and_utm(tmp_path):
    mp = _write_manifest(tmp_path)
    out = gallery.build_gallery(str(mp))
    assert out.is_file()
    doc = out.read_text(encoding="utf-8")
    for e in _manifest()["variants"]:
        assert e["variant_id"] in doc
        assert f"utm_content={e['utm_content']}" in doc


# EARS-5: fehlgeschlagene Variante sichtbar als Fehler (rot) markiert, nicht still weggelassen.
def test_gallery_marks_error(tmp_path):
    mp = _write_manifest(tmp_path)
    doc = gallery.build_gallery(str(mp)).read_text(encoding="utf-8")
    assert "Chromium-Boom" in doc
    assert "flag error" in doc
    assert "has-error" in doc


# Warnung gelb markiert (warnings-Feld aus dem Manifest).
def test_gallery_marks_warning(tmp_path):
    mp = _write_manifest(tmp_path)
    doc = gallery.build_gallery(str(mp)).read_text(encoding="utf-8")
    assert "flag warn" in doc
    assert "Coaching-Claim-Risiko" in doc
    assert "has-warn" in doc


# not_implemented (Video) wird ebenfalls als Fehler/rot ausgewiesen statt verschwiegen.
def test_gallery_marks_not_implemented(tmp_path):
    mp = _write_manifest(tmp_path)
    doc = gallery.build_gallery(str(mp)).read_text(encoding="utf-8")
    assert "not_implemented" in doc


# EARS-3: standalone HTML neben dem Manifest, per file:// oeffenbar (relative Bildpfade).
def test_gallery_is_standalone_next_to_manifest(tmp_path):
    mp = _write_manifest(tmp_path)
    out = gallery.build_gallery(str(mp))
    assert out.parent == mp.parent
    assert out.name == "gallery.html"
    doc = out.read_text(encoding="utf-8")
    assert doc.lstrip().startswith("<!DOCTYPE html>")
    # relativer Bildpfad (kein absoluter Pfad) im src
    assert 'src="h1-immo__bab-h00__feed_4x5.png"' in doc
    # kein Server-/CDN-Asset noetig -> alles inline (CSS im <style>)
    assert "<style>" in doc


# Robust: fehlende Bilddatei -> Platzhalter-Mechanik vorhanden (onerror), kein Crash.
def test_gallery_has_image_fallback(tmp_path):
    mp = _write_manifest(tmp_path)
    doc = gallery.build_gallery(str(mp)).read_text(encoding="utf-8")
    assert "onerror=" in doc
    assert "Bild nicht gefunden" in doc


# Gruppierung nach Format (Plus laut Spec): jede Format-Sektion vorhanden.
def test_gallery_grouping_by_format(tmp_path):
    mp = _write_manifest(tmp_path)
    doc = gallery.build_gallery(str(mp), group_by="format").read_text(encoding="utf-8")
    assert "format: feed_4x5" in doc
    assert "format: story_9x16" in doc


# CLI-Pfad: main() schreibt die Galerie und gibt 0 zurueck.
def test_cli_main(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    rc = gallery.main(["--manifest", str(mp)])
    assert rc == 0
    assert (tmp_path / "gallery.html").is_file()
