"""SKILL-077 — Tests fuer die KEYLESS Stock-Quelle (Openverse) + optionalen Pexels-Key.

Offline: KEIN echter Netzwerk-Call. Die HTTP-Schicht (``download_bytes`` bzw. die
Suchfunktionen) wird monkeypatched; getestet werden Lizenz-Mapping, People-Heuristik,
Persistenz mit ehrlicher Herkunft/Lizenz im Index und die Pexels-bevorzugt/Openverse-
Fallback-Logik im keyless-Resolver.

1 EARS = mind. 1 Test:
  - EARS-1 [keyless]: ``resolve_bg(source='stock')`` braucht KEINEN Magnific-Key
    (load_key wird nicht aufgerufen) und persistiert einen Openverse-Treffer.
  - EARS-2 [ehrliche Lizenz]: Openverse-Eintrag traegt CC-license_type + license_url +
    Attribution/Quelle; is_ai_generated=False -> KEIN Disclosure-Gate.
  - EARS-3 [Pexels optional]: mit PEXELS_API_KEY wird Pexels bevorzugt, ohne Key Openverse.
  - EARS-4 [People-Heuristik]: no_people sortiert personen-getaggte Treffer nach hinten.
  - EARS-5 [Lizenz-Gate bleibt]: der bestehende license_type/url-Zwang greift auch hier.
"""
import json

import pytest

from creative_studio import image_source as m


_OV_RESULT = {
    "id": "abc-123", "title": "Modern office desk with laptop",
    "url": "https://cdn.example.com/img/abc-123.jpg", "filetype": "jpg",
    "license": "cc0", "license_version": "1.0",
    "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    "creator": "Startup Stock Photos", "attribution": "\"Team meeting\" is marked CC0 1.0",
    "provider": "stocksnap", "foreign_landing_url": "https://stocksnap.io/photo/abc-123",
    "width": 5472, "height": 3648,
    "tags": [{"name": "office"}, {"name": "laptop"}, {"name": "desk"}],
}
_OV_PERSON = {
    "id": "p-1", "title": "Portrait of a businesswoman", "url": "https://x/p1.jpg",
    "filetype": "jpg", "license": "by", "license_version": "2.0",
    "tags": [{"name": "woman"}, {"name": "portrait"}],
}


# --- EARS-2: Lizenz-Mapping (rein) --------------------------------------------

def test_cc_license_type_and_url_mapping():
    assert m._cc_license_type("cc0", "1.0").startswith("CC0")
    assert m._cc_license_type("by", "4.0") == "CC BY 4.0"
    assert m._cc_license_url("by-sa", "4.0").endswith("/by-sa/4.0/")
    assert "publicdomain/zero" in m._cc_license_url("cc0", "1.0")


# --- EARS-4: People-Heuristik -------------------------------------------------

def test_people_detection():
    assert m._openverse_has_people(_OV_PERSON) is True
    assert m._openverse_has_people(_OV_RESULT) is False


def test_openverse_search_deprioritizes_people(monkeypatch):
    def fake_req(url, timeout):  # noqa: ARG001
        class R:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self): return json.dumps({"results": [_OV_PERSON, _OV_RESULT]}).encode()
        return R()
    monkeypatch.setattr(m.urllib.request, "urlopen", fake_req)
    hits = m.openverse_search("office", no_people=True)
    assert hits[0]["id"] == "abc-123"  # personenfreier Treffer zuerst


# --- EARS-2: Persistenz mit ehrlicher Lizenz/Herkunft -------------------------

def test_openverse_download_persists_honest_license(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "download_bytes", lambda url, timeout=180: (b"\xff\xd8\xff fake", "image/jpeg"))
    lib = m.library_dir(str(tmp_path / "lib"))
    e = m.openverse_download(_OV_RESULT, lib, title="team laptop office")
    assert e["source"] == "openverse"
    assert e["is_ai_generated"] is False
    assert e["license_type"].startswith("CC0")
    assert e["license_url"].startswith("https://creativecommons.org/")
    assert e["attribution"] and e["foreign_landing_url"]
    # im Index gelandet + Datei existiert
    idx = json.loads((lib / "index.json").read_text(encoding="utf-8"))
    assert any(x["id"] == "openverse_abc-123" for x in idx["images"])
    assert m.resolve_entry_path(e, lib) is not None


# --- EARS-1 + EARS-3: keyless Resolver, Pexels bevorzugt ----------------------

def test_resolve_bg_stock_is_keyless(tmp_path, monkeypatch):
    # KEIN Magnific-Key gesetzt -> stock darf trotzdem laufen (load_key NICHT aufrufen).
    monkeypatch.delenv(m.ENV_API_KEY, raising=False)
    monkeypatch.delenv(m.ENV_API_KEY_LEGACY, raising=False)
    monkeypatch.delenv(m.ENV_PEXELS_KEY, raising=False)
    def _boom(*a, **k):
        raise AssertionError("load_key darf fuer keyless-stock NICHT aufgerufen werden")
    monkeypatch.setattr(m, "load_key", _boom)
    monkeypatch.setattr(m, "openverse_search", lambda q, **k: [_OV_RESULT])
    monkeypatch.setattr(m, "download_bytes", lambda url, timeout=180: (b"\xff\xd8\xff fake", "image/jpeg"))
    res = m.resolve_bg("team office", "stock", lib_dir=str(tmp_path / "lib"))
    assert res is not None
    assert res.source == "openverse"
    assert res.ai_generated is False           # keyless-Stock -> KEIN Disclosure
    assert res.from_cache is False


def test_resolve_stock_free_prefers_pexels_when_key(tmp_path, monkeypatch):
    monkeypatch.setenv(m.ENV_PEXELS_KEY, "pex-secret")
    calls = {"pexels": 0, "openverse": 0}
    def fake_pex_search(q, key, **k):
        calls["pexels"] += 1
        return [{"id": 99, "src": {"large2x": "https://x/p.jpg"},
                 "photographer": "Jane Doe", "url": "https://pexels.com/photo/99",
                 "alt": "team laptop", "width": 4000, "height": 3000}]
    monkeypatch.setattr(m, "pexels_search", fake_pex_search)
    monkeypatch.setattr(m, "openverse_search",
                        lambda *a, **k: calls.__setitem__("openverse", calls["openverse"] + 1) or [])
    monkeypatch.setattr(m, "download_bytes", lambda url, timeout=180: (b"\xff\xd8\xff fake", "image/jpeg"))
    e = m.resolve_stock_free("team laptop", m.library_dir(str(tmp_path / "lib")))
    assert e["source"] == "pexels"
    assert e["license_type"].startswith("Pexels")
    assert calls["pexels"] == 1 and calls["openverse"] == 0


# --- EARS-5: Lizenz-Gate bleibt fuer Stock ------------------------------------

def test_stock_entries_pass_license_gate(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "download_bytes", lambda url, timeout=180: (b"x", "image/jpeg"))
    lib = m.library_dir(str(tmp_path / "lib"))
    e = m.openverse_download(_OV_RESULT, lib)
    m._require_license(e)  # darf NICHT werfen
