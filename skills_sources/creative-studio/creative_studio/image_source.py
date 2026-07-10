"""creative-studio — Bildquellen-Modul (SKILL-073).

Zieht/generiert markenneutrale Hintergrund-/Motiv-Bilder fuer die Layout-Archetypen
(SKILL-072) — statt „Bild fehlt". Schliesst die in SKILL.md §7 genannte Grenze
„Foto-Hintergruende". Basis ist der Magnific/Freepik-Client aus
AgentischesArbeiten/scripts/magnific.py, hier **projektneutral** generalisiert:

- API-Key ueber Env: ``MAGNIFIC_API_KEY`` (Fallback: legacy ``magnific_api_key``);
  optional aus einer Env-Datei ``CREATIVE_STUDIO_MAGNIFIC_ENV``. KEIN hartkodierter
  Repo-Root-``.env``, KEIN ``marketing/…``-Pfad.
- Bibliothekspfad ueber Env ``CREATIVE_STUDIO_IMAGE_LIB`` (oder Parameter). Fallback:
  ``./image-library`` relativ zum CWD.
- **search-first:** Der Resolver prueft ZUERST die lokale Bibliothek (``index.json``),
  bevor er Stock zieht oder KI generiert — kein Doppel-Download/-Spend.
- **Lizenz/Kosten-Gate:** ``license_type`` + ``license_url`` sind Pflichtfelder jedes
  Index-Eintrags. ``generate`` (kostet Geld) nur explizit — nie Silent-Spend;
  ``library``/``stock`` sind die guenstigen Defaults.
- **KEYLESS Stock (SKILL-077):** ``--bg-source stock`` laeuft ueber **Openverse**
  (``api.openverse.org``, KEIN API-Key) und liefert CC-lizenzierte, kommerziell nutzbare
  Fotos (Filter ``license_type=commercial``). Damit ist der Stock-Typ des 4-Typen-Ad-Satzes
  ohne jedes User-Setup verfuegbar. Optional bessere Qualitaet: ein KOSTENLOSER
  ``PEXELS_API_KEY`` in der Env — ist er gesetzt, wird Pexels bevorzugt, sonst Openverse.
  (Der frueher hier verdrahtete Magnific-Stock-Pfad (``stock_search``/``stock_download``)
  bleibt als optionale Premium-Quelle im Modul, ist aber nicht mehr der Default.)

API: Header ``x-magnific-api-key``, Base ``https://api.magnific.com/v1``.
Stock-Filter brauchen Array-Syntax (``filters[content_type][]=photo``,
``filters[people][]=exclude``); KI-Gen ``POST /v1/ai/mystic`` async + poll.

Standalone-CLI (search/download/generate/credits/search-lib/resolve) am Ende — der
Render-Pfad ruft ``resolve_bg()`` aus ``render_image.py`` (``--bg-source``).
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

BASE = "https://api.magnific.com/v1"

# Env-Namen (projektneutral, kein hartkodierter Pfad/Key).
ENV_API_KEY = "MAGNIFIC_API_KEY"
ENV_API_KEY_LEGACY = "magnific_api_key"
ENV_API_ENVFILE = "CREATIVE_STUDIO_MAGNIFIC_ENV"   # optionale Env-Datei mit magnific_api_key=
ENV_IMAGE_LIB = "CREATIVE_STUDIO_IMAGE_LIB"

# KI-generierte Quellen -> loesen die KI-Disclosure-Pflicht aus (SKILL-028/073).
AI_SOURCES = ("magnific-gen",)


class ImageSourceError(RuntimeError):
    """Fehler in Bildquelle/Resolver (fehlender Key, kein Treffer, Lizenz-Gate)."""


# ------------------------------------------------------------------ config
def library_dir(explicit: str | None = None) -> pathlib.Path:
    """Aufloesung des Bibliothekspfads: Parameter > Env > ./image-library (CWD)."""
    raw = explicit or os.environ.get(ENV_IMAGE_LIB) or os.path.join(os.getcwd(), "image-library")
    return pathlib.Path(raw)


def index_path(lib: pathlib.Path) -> pathlib.Path:
    return lib / "index.json"


def load_key(explicit: str | None = None) -> str:
    """Liest den Magnific-Key aus Parameter/Env/Env-Datei. Key wird NIE geloggt."""
    key = explicit or os.environ.get(ENV_API_KEY) or os.environ.get(ENV_API_KEY_LEGACY)
    if not key:
        envfile = os.environ.get(ENV_API_ENVFILE)
        if envfile and os.path.isfile(envfile):
            for line in pathlib.Path(envfile).read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith(("magnific_api_key=", f"{ENV_API_KEY}=")):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not key:
        raise ImageSourceError(
            f"Kein Magnific-Key. Setze ${ENV_API_KEY} (oder ${ENV_API_ENVFILE} auf eine "
            "Env-Datei mit magnific_api_key=…). Der Key wird nie geloggt/committet."
        )
    return key


# ------------------------------------------------------------------ http
def api(method: str, path: str, key: str, body=None, timeout=120):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("x-magnific-api-key", key)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            return resp.status, hdrs, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, e.read()


def api_json(method: str, path: str, key: str, body=None):
    st, h, raw = api(method, path, key, body)
    try:
        parsed = json.loads(raw.decode())
    except Exception:
        parsed = {"_raw": raw.decode(errors="replace")}
    return st, h, parsed


def download_bytes(url: str, timeout=180):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 creative-studio"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


# ------------------------------------------------------------------ index
def load_index(lib: pathlib.Path) -> dict:
    ip = index_path(lib)
    if ip.exists():
        return json.loads(ip.read_text(encoding="utf-8"))
    return {"schema": 1, "images": []}


def save_index(lib: pathlib.Path, idx: dict) -> None:
    lib.mkdir(parents=True, exist_ok=True)
    index_path(lib).write_text(json.dumps(idx, indent=2, ensure_ascii=False), encoding="utf-8")


def _require_license(entry: dict) -> None:
    """SKILL-073 Lizenz-Gate: license_type + license_url sind Pflicht (kein Blind-Asset)."""
    if not entry.get("license_type") or not entry.get("license_url"):
        raise ImageSourceError(
            "Lizenz-Gate: Index-Eintrag ohne license_type/license_url wird abgelehnt "
            f"(id={entry.get('id')}). Jedes Bild braucht eine dokumentierte Lizenz."
        )


def add_entry(lib: pathlib.Path, entry: dict) -> dict:
    _require_license(entry)
    idx = load_index(lib)
    idx["images"] = [e for e in idx["images"] if e.get("local_path") != entry["local_path"]]
    idx["images"].append(entry)
    save_index(lib, idx)
    return entry


def _is_ai_entry(entry: dict) -> bool:
    return bool(entry.get("is_ai_generated")) or entry.get("source") in AI_SOURCES


# ------------------------------------------------------------------ path resolve
def resolve_entry_path(entry: dict, lib: pathlib.Path) -> str | None:
    """Absoluter Pfad einer lokal abgelegten Bilddatei.

    Robust gegen zwei Index-Konventionen: NEUE Eintraege speichern ``local_path``
    relativ zur Bibliothek (portabel); LEGACY-Eintraege (z.B. die bestehende
    AgentischesArbeiten-Bibliothek) speichern ihn repo-relativ. Wir probieren daher
    mehrere Basis-Verzeichnisse und faellt zuletzt auf eine Basename-Suche zurueck.
    """
    lp = (entry.get("local_path") or "").strip()
    if not lp:
        return None
    p = pathlib.Path(lp)
    if p.is_absolute() and p.is_file():
        return str(p)
    bases = [lib, lib.parent, lib.parent.parent, pathlib.Path(os.getcwd())]
    for base in bases:
        cand = (base / lp)
        if cand.is_file():
            return str(cand.resolve())
    # Fallback: Basename irgendwo unter der Bibliothek suchen.
    name = pathlib.Path(lp).name
    for cand in lib.rglob(name):
        if cand.is_file():
            return str(cand.resolve())
    return None


# ------------------------------------------------------------------ library search (search-first)
def _entry_terms(entry: dict) -> str:
    return " ".join(str(x) for x in [
        entry.get("title"), entry.get("prompt"),
        " ".join(entry.get("keywords", []) or []), entry.get("source"),
    ]).lower()


def search_library(query: str, lib: pathlib.Path, *, no_people: bool | None = None) -> list[dict]:
    """Lokale Bibliothek durchsuchen (Token-Overlap auf Titel/Keywords/Prompt).

    Rueckgabe absteigend nach Overlap-Score. ``no_people=True`` bevorzugt (soweit im
    Index vermerkt) personenfreie Bilder — relevant fuer Paid-Ads. Nur Eintraege mit
    aufloesbarer Datei werden zurueckgegeben (kein toter Verweis).
    """
    idx = load_index(lib)
    q_tokens = {t for t in _tokenize(query) if len(t) >= 3}
    scored: list[tuple[int, dict]] = []
    for e in idx.get("images", []):
        if resolve_entry_path(e, lib) is None:
            continue
        hay = _entry_terms(e)
        e_tokens = set(_tokenize(hay))
        score = len(q_tokens & e_tokens)
        # Substring-Bonus (ganze Query im Text) fuer kurze Queries.
        if query.strip().lower() and query.strip().lower() in hay:
            score += 2
        if no_people and _entry_has_people(e):
            score -= 3
        if score > 0:
            scored.append((score, e))
    scored.sort(key=lambda t: t[0], reverse=True)
    return [e for _, e in scored]


def _tokenize(text: str) -> list[str]:
    out, cur = [], []
    for ch in (text or "").lower():
        if ch.isalnum():
            cur.append(ch)
        elif cur:
            out.append("".join(cur)); cur = []
    if cur:
        out.append("".join(cur))
    return out


def _entry_has_people(entry: dict) -> bool:
    people = entry.get("people")
    if isinstance(people, bool):
        return people
    kws = " ".join(entry.get("keywords", []) or []).lower()
    return any(w in kws for w in ("person", "people", "man ", "woman", "team member", "portrait"))


# ------------------------------------------------------------------ stock
def stock_search(term: str, key: str, *, limit=8, photo=True, no_people=True,
                 orientation: str | None = None, ai: str | None = None) -> list[dict]:
    params = [("term", term), ("limit", str(limit))]
    if photo:
        params.append(("filters[content_type][]", "photo"))
    if no_people:
        params.append(("filters[people][]", "exclude"))
    if orientation:
        params.append(("filters[orientation][]", orientation))
    if ai:
        params.append(("filters[ai-generated]", ai))
    qs = urllib.parse.urlencode(params)
    st, h, d = api_json("GET", "/resources?" + qs, key)
    if st != 200:
        raise ImageSourceError(f"Stock-Suche fehlgeschlagen ({st}): {json.dumps(d)[:300]}")
    return d.get("data", [])


def _resource_detail(rid, key: str) -> dict:
    st, _, d = api_json("GET", f"/resources/{rid}", key)
    return d.get("data", {}) if st == 200 else {}


def stock_download(resource_id, key: str, lib: pathlib.Path, *, size="large",
                   title: str | None = None) -> dict:
    """Ein Stock-Original herunterladen + im Index persistieren (mit Lizenz)."""
    detail = _resource_detail(resource_id, key)
    qp = "?" + urllib.parse.urlencode({"image_size": size}) if size else ""
    st, _, d = api_json("GET", f"/resources/{resource_id}/download{qp}", key)
    if st != 200:
        raise ImageSourceError(f"Download-Link fehlgeschlagen ({st}): {json.dumps(d)[:300]}")
    data = d.get("data", d)
    url = data.get("url") or data.get("signed_url")
    if not url:
        raise ImageSourceError(f"Kein Download-URL in Response: {json.dumps(d)[:300]}")
    filename = data.get("filename") or f"{resource_id}.jpg"
    ext = os.path.splitext(filename)[1] or ".jpg"
    blob, _ = download_bytes(url)
    local_path = lib / "stock" / f"{resource_id}{ext}"
    local_path.parent.mkdir(parents=True, exist_ok=True)
    local_path.write_bytes(blob)
    kws = [t.get("name") for t in (detail.get("related_tags") or [])][:12]
    dims = detail.get("dimensions") or {}
    entry = {
        "source": "magnific-stock",
        "id": str(resource_id),
        "prompt": None,
        "title": title or detail.get("name") or filename,
        "license_type": "premium" if detail.get("premium") else "freemium",
        "license_url": detail.get("license") or f"https://www.magnific.com/profile/license/pdf/{resource_id}",
        "keywords": [k for k in kws if k],
        "format": ext.lstrip("."),
        "size_bytes": len(blob),
        "image_size_param": size or "default",
        "original_dimensions": f"{dims.get('width')}x{dims.get('height')}" if dims else None,
        "is_ai_generated": detail.get("is_ai_generated"),
        "people": None,
        "expose_url": detail.get("url"),
        "remote_url": url,
        # NEUE Eintraege: local_path relativ zur Bibliothek (portabel).
        "local_path": str(local_path.relative_to(lib)).replace("\\", "/"),
        "downloaded_at": datetime.date.today().isoformat(),
    }
    return add_entry(lib, entry)


# ------------------------------------------------------------------ keyless stock (Openverse) + optional Pexels
# SKILL-077: Zweite Stock-Quelle, die OHNE User-Setup laeuft. Openverse
# (https://api.openverse.org) ist keyless und liefert CC-lizenzierte, kommerziell
# nutzbare Fotos (Filter license_type=commercial). Damit ist ``--bg-source stock``
# der Default-Weg fuer den 4-Typen-Ad-Satz, ohne dass ein Magnific-Key noetig ist.
# Fuer bessere Bild-Qualitaet kann optional ein KOSTENLOSER PEXELS_API_KEY nachgeruestet
# werden — ist er gesetzt, wird Pexels bevorzugt, sonst faellt der Resolver auf Openverse.
OPENVERSE_BASE = "https://api.openverse.org/v1"
# Ehrlicher, identifizierbarer UA (Openverse-Etikette; kein Bulk-Scraping, ein Bild/Aufruf).
STOCK_UA = "creative-studio/1.0 (+https://jakobsebov.de; ad-creative-tool)"
ENV_PEXELS_KEY = "PEXELS_API_KEY"

# Keyless-Stock-Quellen -> NIE KI, loesen also NIE das Disclosure-Gate aus.
STOCK_SOURCES = ("openverse", "pexels")

_PEOPLE_WORDS = {
    "person", "people", "man", "men", "woman", "women", "boy", "girl", "face",
    "portrait", "team", "child", "children", "crowd", "businessman", "businesswoman",
    "worker", "human", "hands", "selfie",
}


def _cc_license_url(code: str | None, version: str | None) -> str:
    c = (code or "").lower()
    if c in ("cc0", "pdm"):
        return "https://creativecommons.org/publicdomain/zero/1.0/"
    return f"https://creativecommons.org/licenses/{c or 'by'}/{version or '4.0'}/"


def _cc_license_type(code: str | None, version: str | None) -> str:
    c = (code or "").lower()
    if c == "cc0":
        return "CC0 1.0 (Public Domain)"
    if c == "pdm":
        return "Public Domain Mark"
    return f"CC {c.upper()} {version or ''}".strip()


def _openverse_has_people(result: dict) -> bool:
    hay = " ".join([
        result.get("title") or "",
        " ".join(t.get("name", "") for t in (result.get("tags") or [])),
    ])
    return bool(set(_tokenize(hay)) & _PEOPLE_WORDS)


def openverse_search(query: str, *, limit: int = 8, no_people: bool = True,
                     photo: bool = True, aspect_ratio: str | None = None) -> list[dict]:
    """Keyless Stock-Suche ueber Openverse (CC, kommerziell nutzbar).

    Filtert ``license_type=commercial`` (nur kommerziell verwendbare CC-Lizenzen) und
    per Default ``category=photograph``. ``no_people=True`` sortiert personen-getaggte
    Treffer nach hinten (Openverse hat keinen harten People-Filter — best effort).
    """
    def _req(extra: dict) -> dict:
        # Openverse: anonyme (keyless) Requests erlauben max. page_size 20.
        params = {"q": query, "license_type": "commercial",
                  "page_size": max(1, min(limit * 3, 20))}
        if photo:
            params["category"] = "photograph"
        params.update(extra)
        url = OPENVERSE_BASE + "/images/?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": STOCK_UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise ImageSourceError(
                f"Openverse-Suche fehlgeschlagen ({e.code}): {e.read()[:200].decode(errors='replace')}"
            )

    # aspect_ratio kann die Treffer zu stark einengen (z.B. square+photograph=0) —
    # deshalb zuerst mit, dann ohne Aspekt-Filter versuchen (kein leeres Ergebnis erzwingen).
    tries = ([{"aspect_ratio": aspect_ratio}] if aspect_ratio else []) + [{}]
    results: list[dict] = []
    for extra in tries:
        d = _req(extra)
        results = d.get("results", []) or []
        if results:
            break
    if no_people:
        results = sorted(results, key=lambda r: 1 if _openverse_has_people(r) else 0)
    return results[:limit]


def openverse_download(result: dict, lib: pathlib.Path, *, title: str | None = None) -> dict:
    """Ein Openverse-Foto herunterladen + mit ehrlicher CC-Lizenz im Index persistieren."""
    rid = str(result.get("id") or "")
    url = result.get("url")
    if not url:
        raise ImageSourceError(f"Openverse-Treffer ohne Bild-URL (id={rid}).")
    blob, ctype = download_bytes(url)
    ft = (result.get("filetype") or "").lower()
    if ft in ("jpg", "jpeg", "png", "webp"):
        ext = "." + ("jpg" if ft == "jpeg" else ft)
    else:
        ext = ".png" if "png" in ctype else (".webp" if "webp" in ctype else ".jpg")
    local_path = lib / "stock" / f"openverse_{rid}{ext}"
    local_path.parent.mkdir(parents=True, exist_ok=True)
    local_path.write_bytes(blob)
    kws = [t.get("name") for t in (result.get("tags") or []) if t.get("name")][:12]
    entry = {
        "source": "openverse",
        "id": f"openverse_{rid}",
        "prompt": None,
        "title": title or result.get("title") or f"Openverse {rid}",
        "license_type": _cc_license_type(result.get("license"), result.get("license_version")),
        "license_url": result.get("license_url") or _cc_license_url(
            result.get("license"), result.get("license_version")),
        "attribution": result.get("attribution"),
        "creator": result.get("creator"),
        "creator_url": result.get("creator_url"),
        "provider": result.get("provider") or result.get("source"),
        "foreign_landing_url": result.get("foreign_landing_url"),
        "keywords": kws,
        "format": ext.lstrip("."),
        "size_bytes": len(blob),
        "original_dimensions": (
            f"{result.get('width')}x{result.get('height')}" if result.get("width") else None),
        "is_ai_generated": False,
        "people": _openverse_has_people(result),
        "remote_url": url,
        "local_path": str(local_path.relative_to(lib)).replace("\\", "/"),
        "downloaded_at": datetime.date.today().isoformat(),
    }
    return add_entry(lib, entry)


def pexels_key(explicit: str | None = None) -> str | None:
    """Optionaler Pexels-Key (bessere Stock-Qualitaet). Fehlt er -> Openverse-Fallback."""
    return explicit or os.environ.get(ENV_PEXELS_KEY)


def pexels_search(query: str, key: str, *, limit: int = 8,
                  orientation: str | None = None) -> list[dict]:
    params = {"query": query, "per_page": max(1, min(limit, 80))}
    if orientation:
        params["orientation"] = orientation
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": key, "User-Agent": STOCK_UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            d = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise ImageSourceError(
            f"Pexels-Suche fehlgeschlagen ({e.code}): {e.read()[:200].decode(errors='replace')}")
    return d.get("photos", []) or []


def pexels_download(photo: dict, lib: pathlib.Path, *, title: str | None = None) -> dict:
    src = photo.get("src") or {}
    url = src.get("large2x") or src.get("large") or src.get("original")
    if not url:
        raise ImageSourceError(f"Pexels-Foto ohne src-URL (id={photo.get('id')}).")
    blob, ctype = download_bytes(url)
    ext = ".png" if "png" in ctype else ".jpg"
    pid = str(photo.get("id"))
    local_path = lib / "stock" / f"pexels_{pid}{ext}"
    local_path.parent.mkdir(parents=True, exist_ok=True)
    local_path.write_bytes(blob)
    entry = {
        "source": "pexels",
        "id": f"pexels_{pid}",
        "prompt": None,
        "title": title or photo.get("alt") or f"Pexels {pid}",
        "license_type": "Pexels License (frei, kommerziell nutzbar)",
        "license_url": "https://www.pexels.com/license/",
        "attribution": f"Foto: {photo.get('photographer')} / Pexels" if photo.get("photographer") else None,
        "creator": photo.get("photographer"),
        "creator_url": photo.get("photographer_url"),
        "provider": "pexels",
        "foreign_landing_url": photo.get("url"),
        "keywords": [w for w in _tokenize(photo.get("alt") or "") if len(w) >= 3][:12],
        "format": ext.lstrip("."),
        "size_bytes": len(blob),
        "original_dimensions": (
            f"{photo.get('width')}x{photo.get('height')}" if photo.get("width") else None),
        "is_ai_generated": False,
        "people": None,
        "remote_url": url,
        "local_path": str(local_path.relative_to(lib)).replace("\\", "/"),
        "downloaded_at": datetime.date.today().isoformat(),
    }
    return add_entry(lib, entry)


def resolve_stock_free(query: str, lib: pathlib.Path, *, no_people: bool = True,
                       aspect_ratio: str | None = None) -> dict:
    """Keyless-Stock-Aufloesung: Pexels wenn PEXELS_API_KEY gesetzt, sonst Openverse.

    Kein User-Setup noetig — Openverse laeuft ohne Key. Ist ein (kostenloser)
    Pexels-Key vorhanden, wird er fuer bessere Qualitaet bevorzugt; scheitert Pexels,
    faellt der Resolver ehrlich auf Openverse zurueck.
    """
    pk = pexels_key()
    if pk:
        try:
            orient = {"tall": "portrait", "wide": "landscape", "square": "square"}.get(aspect_ratio)
            photos = pexels_search(query, pk, limit=8, orientation=orient)
            if photos:
                return pexels_download(photos[0], lib, title=query)
            print(f"  (Pexels: kein Treffer fuer '{query}' -> Openverse)", file=sys.stderr)
        except ImageSourceError as e:
            print(f"  (Pexels-Fehler: {e} -> Openverse-Fallback)", file=sys.stderr)
    results = openverse_search(query, no_people=no_people, aspect_ratio=aspect_ratio)
    if not results:
        raise ImageSourceError(f"Kein keyless Stock-Treffer (Openverse) fuer '{query}'.")
    return openverse_download(results[0], lib, title=query)


# ------------------------------------------------------------------ generate (KI, explizit)
def generate(prompt: str, key: str, lib: pathlib.Path, *, model="realism", res="2k",
             ar="widescreen_16_9", keep_original=False, poll_max=40, poll_sleep=6) -> dict:
    """KI-Bild (Mystic) generieren + persistieren. Kostet Geld -> nur explizit aufrufen."""
    body = {"prompt": prompt, "model": model, "resolution": res, "aspect_ratio": ar}
    st, _, d = api_json("POST", "/ai/mystic", key, body)
    if st not in (200, 201):
        raise ImageSourceError(f"Generierung-Start fehlgeschlagen ({st}): {json.dumps(d)[:400]}")
    task = (d.get("data") or {}).get("task_id") or d.get("task_id")
    if not task:
        raise ImageSourceError(f"Keine task_id: {json.dumps(d)[:300]}")
    result = None
    for _ in range(poll_max):
        time.sleep(poll_sleep)
        st, _, d = api_json("GET", f"/ai/mystic/{task}", key)
        data = d.get("data", d)
        status = data.get("status")
        if status == "COMPLETED":
            result = data
            break
        if status in ("FAILED", "ERROR"):
            raise ImageSourceError(f"Generierung fehlgeschlagen: {json.dumps(d)[:300]}")
    if not result:
        raise ImageSourceError(f"Timeout beim Polling. Task {task} spaeter abrufen.")
    gen = result.get("generated") or []
    if not gen:
        raise ImageSourceError(f"Keine Bilder in generated[]: {json.dumps(result)[:300]}")
    url = gen[0] if isinstance(gen[0], str) else gen[0].get("url")
    blob, ctype = download_bytes(url)
    slug = "".join(c if c.isalnum() else "-" for c in prompt.lower())[:40].strip("-")
    stamp = datetime.datetime.now().strftime("%Y%m%d")
    ext = ".png" if "png" in ctype else ".jpg"
    orig_dims = None
    if len(blob) > 1_500_000 and not keep_original:
        try:
            import io
            from PIL import Image
            im = Image.open(io.BytesIO(blob)).convert("RGB")
            orig_dims = f"{im.width}x{im.height}"
            if im.width > 1920:
                im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
            out = io.BytesIO()
            im.save(out, "JPEG", quality=88, optimize=True)
            blob = out.getvalue()
            ext = ".jpg"
        except Exception as e:  # nicht-brechend: Original behalten
            print(f"  (Web-Optimierung uebersprungen: {e})", file=sys.stderr)
    local_path = lib / "generiert" / f"{stamp}_{slug}{ext}"
    local_path.parent.mkdir(parents=True, exist_ok=True)
    local_path.write_bytes(blob)
    entry = {
        "source": "magnific-gen",
        "id": task,
        "prompt": prompt,
        "title": prompt[:80],
        "license_type": "magnific-generated",
        "license_url": "https://www.magnific.com/legal/terms-of-use#api-services",
        "keywords": [w for w in slug.split("-") if w][:12],
        "format": ext.lstrip("."),
        "size_bytes": len(blob),
        "model": model, "resolution": res, "aspect_ratio": ar,
        "original_dimensions": orig_dims,
        "web_optimized": ext == ".jpg" and orig_dims is not None,
        "is_ai_generated": True,     # -> KI-Disclosure-Pflicht (SKILL-028)
        "people": None,
        "remote_url": url,
        "local_path": str(local_path.relative_to(lib)).replace("\\", "/"),
        "downloaded_at": datetime.date.today().isoformat(),
    }
    return add_entry(lib, entry)


# ------------------------------------------------------------------ resolver (search-first)
@dataclass
class BgResult:
    """Aufgeloestes Hintergrund-/Motiv-Bild fuer den Render-Pfad."""
    local_path: str            # absoluter Dateipfad (fuer content.bg_image)
    source: str                # magnific-stock | magnific-gen | ...
    license_type: str
    license_url: str
    ai_generated: bool         # -> content.ai_image (Disclosure-Gate)
    from_cache: bool           # True = aus lokaler Bibliothek (kein Download/Spend)
    entry: dict


def resolve_bg(query: str, source: str = "library", *, lib_dir: str | None = None,
               key: str | None = None, no_people: bool = True, size: str = "large",
               model: str = "realism", res: str = "2k", ar: str = "widescreen_16_9") -> BgResult | None:
    """SKILL-073: liefert einen lokalen Bildpfad fuer die gewuenschte Quelle — search-first.

    Ablauf (kein Doppel-Download/-Spend):
      1. ``source='none'``     -> None (Renderer nutzt Gradient).
      2. IMMER zuerst die lokale Bibliothek durchsuchen (``search_library``). Treffer ->
         zurueckgeben (``from_cache=True``), egal ob source library/stock/generate.
      3. ``source='library'``  -> ohne lokalen Treffer: None (Renderer warnt).
      4. ``source='stock'``    -> KEYLESS Stock (Openverse, CC-kommerziell; Pexels wenn
         ``PEXELS_API_KEY`` gesetzt) suchen + Ergebnis herunterladen. Kein User-Setup/Key.
      5. ``source='generate'`` -> KI generieren (kostet Geld; nur weil explizit gewaehlt).

    KI-Herkunft (``magnific-gen``/is_ai_generated) setzt ``ai_generated=True`` — der
    Renderer verdrahtet das auf ``content.ai_image`` -> Disclosure-Gate (SKILL-028).
    """
    if source == "none":
        return None
    if source not in ("library", "stock", "generate"):
        raise ImageSourceError(f"Unbekannte bg-source '{source}'. Erlaubt: none, library, stock, generate.")

    lib = library_dir(lib_dir)

    # (2) search-first: lokale Bibliothek
    hits = search_library(query, lib, no_people=no_people)
    if hits:
        e = hits[0]
        path = resolve_entry_path(e, lib)
        if path:
            _require_license(e)
            return BgResult(
                local_path=path, source=e.get("source", "library"),
                license_type=e.get("license_type", ""), license_url=e.get("license_url", ""),
                ai_generated=_is_ai_entry(e), from_cache=True, entry=e,
            )

    if source == "library":
        return None  # nur lokal; Renderer warnt + Gradient-Fallback

    # (4/5) ziehen bzw. generieren
    if source == "stock":
        # KEYLESS: Openverse (bzw. Pexels wenn Key gesetzt) — kein Magnific-Key noetig.
        entry = resolve_stock_free(query, lib, no_people=no_people)
    else:  # generate — KI, kostet Geld -> Key Pflicht
        k = key or load_key()
        entry = generate(query, k, lib, model=model, res=res, ar=ar)

    path = resolve_entry_path(entry, lib)
    if not path:
        raise ImageSourceError("Bild geladen, aber Pfad nicht aufloesbar (Index/FS inkonsistent).")
    return BgResult(
        local_path=path, source=entry.get("source", source),
        license_type=entry.get("license_type", ""), license_url=entry.get("license_url", ""),
        ai_generated=_is_ai_entry(entry), from_cache=False, entry=entry,
    )


# ------------------------------------------------------------------ CLI
def _cli(argv=None) -> int:
    p = argparse.ArgumentParser(description="creative-studio Bildquelle (SKILL-073)")
    p.add_argument("--lib", default=None, help=f"Bibliothekspfad (sonst ${ENV_IMAGE_LIB} / ./image-library)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="Stock-Suche Magnific (Key noetig, kein Download)")
    s.add_argument("term"); s.add_argument("--limit", type=int, default=8)
    s.add_argument("--people", action="store_true", help="Personen zulassen (Default: exclude)")

    of = sub.add_parser("stock-free", help="KEYLESS Stock (Openverse/Pexels) suchen + laden")
    of.add_argument("term"); of.add_argument("--people", action="store_true",
                    help="Personen zulassen (Default: deprioritisieren)")
    of.add_argument("--search-only", action="store_true", help="nur suchen, nicht laden")

    d = sub.add_parser("download", help="Stock-Original laden + persistieren")
    d.add_argument("resource_id"); d.add_argument("--size", default="large")
    d.add_argument("--title")

    g = sub.add_parser("generate", help="KI-Bild (Mystic) generieren (kostet Geld)")
    g.add_argument("prompt"); g.add_argument("--model", default="realism")
    g.add_argument("--res", default="2k"); g.add_argument("--ar", default="widescreen_16_9")

    sl = sub.add_parser("search-lib", help="lokale Bibliothek durchsuchen")
    sl.add_argument("term"); sl.add_argument("--people", action="store_true")

    r = sub.add_parser("resolve", help="search-first Aufloesung (Pfad ausgeben)")
    r.add_argument("query"); r.add_argument("--source", default="library",
                                            choices=["none", "library", "stock", "generate"])
    r.add_argument("--people", action="store_true")

    sub.add_parser("credits", help="Rate-Limit-Header")

    args = p.parse_args(argv)
    lib = library_dir(args.lib)

    if args.cmd == "search":
        key = load_key()
        for it in stock_search(args.term, key, limit=args.limit, no_people=not args.people):
            lic = (it.get("licenses", [{}]) or [{}])[0]
            print(f"[{it['id']}] {it.get('title','')[:70]} | lizenz={lic.get('type')}")
        return 0
    if args.cmd == "stock-free":
        results = openverse_search(args.term, no_people=not args.people)
        if args.search_only:
            for r in results:
                print(f"[{r.get('id','')[:8]}] {r.get('license')} {r.get('license_version')} | "
                      f"{(r.get('title') or '')[:60]} | {r.get('provider')}")
            return 0
        e = resolve_stock_free(args.term, lib, no_people=not args.people)
        print(f"OK {resolve_entry_path(e, lib)} | {e['source']} | {e['license_type']} -> {e['license_url']}")
        return 0
    if args.cmd == "download":
        e = stock_download(args.resource_id, load_key(), lib, size=args.size, title=args.title)
        print(f"OK {resolve_entry_path(e, lib)} | {e['license_type']} -> {e['license_url']}")
        return 0
    if args.cmd == "generate":
        e = generate(args.prompt, load_key(), lib, model=args.model, res=args.res, ar=args.ar)
        print(f"OK {resolve_entry_path(e, lib)} | KI-generiert -> Disclosure-Pflicht")
        return 0
    if args.cmd == "search-lib":
        for e in search_library(args.term, lib, no_people=not args.people):
            print(f"- {resolve_entry_path(e, lib)} | {e.get('source')} | {e.get('title','')[:60]}")
        return 0
    if args.cmd == "resolve":
        res = resolve_bg(args.query, args.source, lib_dir=args.lib, no_people=not args.people)
        if res is None:
            print("(kein Bild — Gradient-Fallback)")
            return 0
        print(f"{res.local_path}\n  source={res.source} cache={res.from_cache} "
              f"ai={res.ai_generated} lizenz={res.license_type}")
        return 0
    if args.cmd == "credits":
        _, h, _ = api_json("GET", "/resources?term=test&limit=1", load_key())
        print(f"limit={h.get('x-ratelimit-limit')} remaining={h.get('x-ratelimit-remaining')}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(_cli())
