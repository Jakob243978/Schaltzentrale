"""SKILL-073 — Tests fuer das Bildquellen-Modul (Magnific Stock + KI-Gen, search-first).

Offline: KEIN Netzwerk-Call. Getestet werden Config-Aufloesung, search-first-Resolver,
Lizenz-/Kosten-Gate, KI-Disclosure-Verdrahtung und die Legacy-Pfad-Kompatibilitaet.

1 EARS = mind. 1 Test:
  - EARS-1 [multi-projekt]: Key + Bibliothekspfad kommen aus Env/Param (kein Repo-.env,
    kein marketing/-Pfad hartkodiert).
  - EARS-2: search-first — der Resolver liefert einen lokalen Treffer, bevor er zieht.
  - EARS-3: source='library' ohne Treffer -> None (Renderer-Fallback), source='none' -> None.
  - EARS-4: Lizenz-Gate — Eintrag ohne license_type/url wird abgelehnt.
  - EARS-5: KI-Herkunft (magnific-gen/is_ai_generated) -> ai_generated=True (Disclosure).
"""
import json

import pytest

from creative_studio import image_source as m


def _write_lib(tmp_path, entries, *, files=True, local_path_style="lib-relative"):
    """Baut eine Test-Bibliothek mit index.json + (optional) echten Dateien."""
    lib = tmp_path / "image-library"
    (lib / "stock").mkdir(parents=True, exist_ok=True)
    (lib / "generiert").mkdir(parents=True, exist_ok=True)
    for e in entries:
        if files and e.get("local_path"):
            fp = lib / e["local_path"]
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_bytes(b"\x89PNG\r\n\x1a\n fake")
    (lib / "index.json").write_text(
        json.dumps({"schema": 1, "images": entries}, ensure_ascii=False), encoding="utf-8"
    )
    return lib


_STOCK = {
    "source": "magnific-stock", "id": "111", "title": "Modern office desk workspace",
    "license_type": "premium", "license_url": "https://example.com/lic/111",
    "keywords": ["office", "desk", "workspace", "laptop"],
    "local_path": "stock/111.jpg", "is_ai_generated": False,
}
_GEN = {
    "source": "magnific-gen", "id": "gen-1", "title": "clean minimal studio background",
    "license_type": "magnific-generated", "license_url": "https://example.com/terms",
    "keywords": ["clean", "minimal", "studio", "background"],
    "local_path": "generiert/gen1.jpg", "is_ai_generated": True,
}


# --- EARS-1: Config projektneutral (Env/Param) --------------------------------

def test_library_dir_from_env(tmp_path, monkeypatch):
    monkeypatch.setenv(m.ENV_IMAGE_LIB, str(tmp_path / "lib"))
    assert str(m.library_dir()) == str(tmp_path / "lib")


def test_library_dir_param_wins(tmp_path, monkeypatch):
    monkeypatch.setenv(m.ENV_IMAGE_LIB, str(tmp_path / "env"))
    assert str(m.library_dir(str(tmp_path / "param"))) == str(tmp_path / "param")


def test_load_key_from_env(monkeypatch):
    monkeypatch.setenv(m.ENV_API_KEY, "secret-xyz")
    assert m.load_key() == "secret-xyz"


def test_load_key_missing_raises(monkeypatch):
    monkeypatch.delenv(m.ENV_API_KEY, raising=False)
    monkeypatch.delenv(m.ENV_API_KEY_LEGACY, raising=False)
    monkeypatch.delenv(m.ENV_API_ENVFILE, raising=False)
    with pytest.raises(m.ImageSourceError):
        m.load_key()


def test_no_hardcoded_project_lib_path(tmp_path, monkeypatch):
    # Funktional darf kein Projekt-/marketing-Pfad hartkodiert sein: der Default
    # (ohne Env/Param) faellt auf ./image-library relativ zum CWD, nicht auf einen
    # Repo-/marketing-Pfad. (Die Provenienz im Docstring ist blosse Attribution.)
    monkeypatch.delenv(m.ENV_IMAGE_LIB, raising=False)
    monkeypatch.chdir(tmp_path)
    default = str(m.library_dir())
    assert default.endswith("image-library")
    assert "marketing" not in default
    # Code (ohne Docstring) enthaelt keinen konkreten Projekt-Bibliothekspfad.
    import inspect
    code = "".join(l for l in inspect.getsource(m).splitlines(keepends=True))
    assert "marketing/bild-bibliothek" not in code


# --- EARS-2: search-first ------------------------------------------------------

def test_resolve_library_returns_cached_hit(tmp_path):
    lib = _write_lib(tmp_path, [_STOCK])
    res = m.resolve_bg("modern office desk", "library", lib_dir=str(lib))
    assert res is not None
    assert res.from_cache is True
    assert res.local_path.endswith("111.jpg")
    assert res.license_type == "premium"


def test_search_library_ranks_by_overlap(tmp_path):
    lib = _write_lib(tmp_path, [_STOCK, _GEN])
    hits = m.search_library("clean minimal studio", lib)
    assert hits and hits[0]["id"] == "gen-1"


# --- EARS-3: kein Treffer / none ----------------------------------------------

def test_resolve_library_no_match_returns_none(tmp_path):
    lib = _write_lib(tmp_path, [_STOCK])
    assert m.resolve_bg("underwater volcano", "library", lib_dir=str(lib)) is None


def test_resolve_none_source_returns_none(tmp_path):
    lib = _write_lib(tmp_path, [_STOCK])
    assert m.resolve_bg("office", "none", lib_dir=str(lib)) is None


# --- EARS-4: Lizenz-Gate -------------------------------------------------------

def test_license_gate_rejects_entry_without_license(tmp_path):
    lib = m.library_dir(str(tmp_path / "lib"))
    with pytest.raises(m.ImageSourceError):
        m.add_entry(lib, {"source": "x", "id": "1", "local_path": "a.jpg"})


def test_license_gate_accepts_full_entry(tmp_path):
    lib = m.library_dir(str(tmp_path / "lib"))
    e = m.add_entry(lib, dict(_STOCK))
    assert e["license_type"] == "premium"


# --- EARS-5: KI-Herkunft -> Disclosure ----------------------------------------

def test_resolve_ai_generated_sets_flag(tmp_path):
    lib = _write_lib(tmp_path, [_GEN])
    res = m.resolve_bg("clean minimal studio background", "library", lib_dir=str(lib))
    assert res is not None
    assert res.ai_generated is True
    assert res.source == "magnific-gen"


# --- Legacy-Pfad-Kompatibilitaet (repo-relative local_path) -------------------

def test_resolve_entry_path_handles_legacy_repo_relative(tmp_path):
    # Legacy: local_path repo-relativ ("marketing/bild-bibliothek/stock/x.jpg"),
    # lib zeigt auf .../marketing/bild-bibliothek -> muss trotzdem aufloesen.
    repo = tmp_path
    lib = repo / "marketing" / "bild-bibliothek"
    (lib / "stock").mkdir(parents=True, exist_ok=True)
    (lib / "stock" / "x.jpg").write_bytes(b"fake")
    entry = {"local_path": "marketing/bild-bibliothek/stock/x.jpg"}
    path = m.resolve_entry_path(entry, lib)
    assert path is not None and path.endswith("x.jpg")


def test_dead_reference_not_returned(tmp_path):
    # Eintrag ohne existierende Datei darf NICHT als Treffer zurueckkommen.
    lib = _write_lib(tmp_path, [_STOCK], files=False)
    assert m.search_library("office desk", lib) == []
