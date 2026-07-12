"""creative-studio — Bild-Renderer (SKILL-020).

HTML/CSS-Template (Jinja2) -> Playwright (headless Chromium) -> PNG, ein Aufruf pro Format.
Safe-Zones + Format-Specs kommen aus specs.py (kodierte Recherche). Brand-Tokens aus branding.env
(Parameter -> multi-projekt-tauglich, kein hartkodierter Brand-Wert hier).

CLI:
  python -m creative_studio.render_image --headline "..." --cta "..." \
      --brand-env <pfad/branding.env> --formats feed_4x5,story_9x16 --out <dir>
"""
from __future__ import annotations
import argparse
import json
import os
import pathlib
import sys
from dataclasses import replace  # SKILL-032: pro-Format bg_image-Swap ohne Mutation

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .specs import (
    AdContent, AdFormat, FORMATS, DEFAULT_FORMATS, get_format,
    # SKILL-072: Layout-Archetypen + Themes + Stil-Parameter
    LAYOUTS, THEMES, apply_theme, layout_warnings, HERO_SCALE_DEFAULT,
    # SKILL-073: KI-Disclosure-Gate im echten Render-Pfad verdrahten
    requires_ai_disclosure, AI_LABEL_TEXT,
    # SKILL-086: Methoden-Tagging (variant_id/utm_content aus der zentralen Systematik, SKILL-024)
    make_variant_id, make_utm_content, slugify,
)

# SKILL-086: Default-Framework-Marker. Ist der Wert das (oder leer), bleibt der
# Bestands-Dateiname unveraendert (kein Framework-Token im PNG-Namen).
DEFAULT_FRAMEWORK = "default"


def _framework_of(content: AdContent) -> str:
    """SKILL-086: liefert den Framework-Key des Creatives (Default-Marker als Fallback)."""
    return (getattr(content, "framework", "") or DEFAULT_FRAMEWORK)


def image_output_stem(content: AdContent, fmt: AdFormat) -> str:
    """SKILL-086: Dateiname-Stamm (ohne Endung) fuer ein gerendertes Bild.

    Traegt den Framework-Key im Namen, SOBALD ein nicht-Default-Framework gesetzt ist
    (`<ad_id>__<framework>__<format>`). Ohne/mit Default-Framework bleibt der
    Bestands-Name `<ad_id>__<format>` unveraendert (nicht-brechend, "Default beibehalten").
    """
    ad = content.ad_id or "creative"
    fw = _framework_of(content)
    if fw and fw != DEFAULT_FRAMEWORK:
        return f"{ad}__{slugify(fw)}__{fmt.key}"
    return f"{ad}__{fmt.key}"


def build_image_meta(content: AdContent, fmt: AdFormat) -> dict:
    """SKILL-086: Sidecar-Metadaten eines Bild-Creatives (mit explizitem `framework`).

    Enthaelt das durchgaengige Methoden-Tag (`framework`) sowie variant_id/utm_content
    aus der zentralen SKILL-024-Systematik (Hook = Headline; hook_index=None -> Hook-Slug),
    sodass aus jedem Artefakt eindeutig ablesbar ist, mit welcher Methode es gebaut wurde.
    Reine Datenfunktion (kein Playwright) -> unit-testbar ohne Chromium.
    """
    fw = _framework_of(content)
    hook = content.headline or content.eyebrow
    vid = make_variant_id(content.ad_id or "creative", hook, fw, fmt.key)
    return {
        "framework": fw,
        "ad_id": content.ad_id or "creative",
        "format": fmt.key,
        "variant_id": vid,
        "utm_content": make_utm_content(vid),
        "headline": content.headline,
        "cta": content.cta,
        "media": "image",
    }

_TEMPLATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "templates"

# Live-Default-Brandwerte (NUR Fallback, wenn branding.env fehlt/Key fehlt — ADR-010-Geist).
_BRAND_DEFAULTS = {
    "BRAND_NAME": "",
    "BRAND_BG": "#0a0e27",
    "BRAND_BG_SOFT": "#11163a",
    "BRAND_ACCENT": "#f25d3e",
    "BRAND_INK": "#faf7f2",
    "BRAND_INK_MUTED": "#9a9ec0",
    "BRAND_FONT": "-apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
}

# SKILL-029: Logo-Default-Rollen (NUR Fallback). Ohne Logo bleibt das Verhalten unveraendert
# (brand_name-Text wie bisher). Position-Whitelist + Default-Hoehe in Prozent der Canvas-Hoehe.
_LOGO_DEFAULTS = {
    "LOGO_PATH": "",
    "LOGO_POSITION": "top-left",
    "LOGO_HEIGHT_PCT": "6.0",
}

# SKILL-029: Erlaubte Logo-Positionen in der oberen Safe-Zone. Unbekannte Werte -> Default + Warnung.
_LOGO_POSITIONS = ("top-left", "top-right", "top-center")

# SKILL-029: Mapping JSON-Token-Rolle -> interner branding.env-Key. Das brand.json benutzt
# kurze Rollen-Namen (bg/accent/ink/font ...), intern bleibt alles auf den BRAND_*-Keys, damit
# build_html()/Template + der branding.env-Weg unveraendert weiterfunktionieren.
_JSON_ROLE_TO_KEY = {
    "brand_name": "BRAND_NAME",
    "bg": "BRAND_BG",
    "bg_soft": "BRAND_BG_SOFT",
    "accent": "BRAND_ACCENT",
    "ink": "BRAND_INK",
    "ink_muted": "BRAND_INK_MUTED",
    "font": "BRAND_FONT",
}

# SKILL-029: Mapping JSON-Logo-Rolle -> interner Logo-Key.
_JSON_LOGO_TO_KEY = {
    "logo_path": "LOGO_PATH",
    "logo_position": "LOGO_POSITION",
    "logo_height_pct": "LOGO_HEIGHT_PCT",
}


def load_branding(path: str | None) -> dict:
    """Liest KEY=\"value\"-Zeilen aus branding.env; Fallback = _BRAND_DEFAULTS."""
    vals = dict(_BRAND_DEFAULTS)
    if path and os.path.isfile(path):
        for raw in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k = k.strip()
            if k in _BRAND_DEFAULTS:
                v = v.strip().strip('"').strip("'")
                if v:
                    vals[k] = v
    return vals


def load_brand_json(path: str | None, warn=None) -> dict:
    """SKILL-029: Liest ein brand.json als Token-Rollen + Logo-Asset.

    Erwartetes Schema (alle Felder optional, verschachtelt nach Rolle):
        {
          "brand_name": "...",
          "colors": {"bg": "#..", "bg_soft": "#..", "accent": "#..",
                     "ink": "#..", "ink_muted": "#.."},
          "font": "...",
          "logo": {"path": "...", "position": "top-left", "height_pct": 6.0}
        }
    Flache Top-Level-Keys (bg/accent/... statt unter "colors") werden ebenfalls
    akzeptiert (Backward-/Convenience). Rueckgabe ist ein flaches dict auf den
    internen BRAND_*/LOGO_*-Keys — nur die im JSON tatsaechlich gesetzten Keys.
    Validierung (EARS-4): fehlende Logo-Datei oder unbekannte Position -> Warnung
    via `warn`-Callback (kein stiller Fallback). `warn` default = stderr-Print.
    """
    def _warn(msg: str) -> None:
        if warn is not None:
            warn(msg)
        else:
            print(f"[WARN] {msg}", file=sys.stderr)

    out: dict = {}
    if not path:
        return out
    if not os.path.isfile(path):
        _warn(f"brand.json nicht gefunden: {path} — branding.env/Defaults werden genutzt.")
        return out
    try:
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        _warn(f"brand.json nicht lesbar ({path}): {exc} — branding.env/Defaults werden genutzt.")
        return out
    if not isinstance(data, dict):
        _warn(f"brand.json hat kein Objekt als Wurzel ({path}) — wird ignoriert.")
        return out

    # Farben: bevorzugt unter "colors", sonst flach am Top-Level.
    colors = data.get("colors") if isinstance(data.get("colors"), dict) else {}
    for role, key in _JSON_ROLE_TO_KEY.items():
        val = None
        if role == "brand_name" or role == "font":
            val = data.get(role)
        else:
            val = colors.get(role, data.get(role))
        if val is not None and str(val).strip() != "":
            out[key] = str(val).strip()

    # Logo: bevorzugt unter "logo", sonst flach (logo_path/logo_position/logo_height_pct).
    logo = data.get("logo") if isinstance(data.get("logo"), dict) else {}
    logo_path = logo.get("path", data.get("logo_path"))
    logo_pos = logo.get("position", data.get("logo_position"))
    logo_h = logo.get("height_pct", data.get("logo_height_pct"))

    if logo_path is not None and str(logo_path).strip() != "":
        lp = str(logo_path).strip()
        out["LOGO_PATH"] = lp
        # EARS-4: referenzierte Logo-Datei fehlt -> klare Warnung statt stiller Fallback.
        if not lp.startswith(("http://", "https://", "file://", "data:")) and not os.path.isfile(lp):
            _warn(f"Logo-Datei nicht gefunden: {lp} — Logo wird nicht eingebettet.")
    if logo_pos is not None and str(logo_pos).strip() != "":
        pos = str(logo_pos).strip().lower()
        if pos not in _LOGO_POSITIONS:
            _warn(f"Unbekannte logo_position '{pos}' — Fallback auf '{_LOGO_DEFAULTS['LOGO_POSITION']}'. "
                  f"Erlaubt: {', '.join(_LOGO_POSITIONS)}.")
            pos = _LOGO_DEFAULTS["LOGO_POSITION"]
        out["LOGO_POSITION"] = pos
    if logo_h is not None and str(logo_h).strip() != "":
        out["LOGO_HEIGHT_PCT"] = str(logo_h).strip()

    return out


def resolve_brand(brand_env=None, brand_json=None, overrides=None, warn=None) -> dict:
    """SKILL-029: Vereint alle Brand-Quellen zu EINEM flachen Brand-dict.

    Praezedenz (hoechste zuerst, EARS-3 — kein stiller Misch-Zustand):
        1. explizite `overrides` (z.B. CLI --brand Name)
        2. `brand_json`  (Token-Rollen + Logo aus brand.json)
        3. `brand_env`   (klassischer branding.env-Weg — bleibt voll erhalten)
        4. _BRAND_DEFAULTS / _LOGO_DEFAULTS

    `brand_env`/`brand_json` koennen ein Pfad (str) ODER ein bereits geladenes dict
    sein. Das Ergebnis enthaelt immer alle BRAND_*-Keys + alle LOGO_*-Keys, sodass
    build_html() es unveraendert konsumieren kann.
    """
    # Schicht 4: Defaults (inkl. Logo-Defaults).
    vals = dict(_BRAND_DEFAULTS)
    vals.update(_LOGO_DEFAULTS)

    # Schicht 3: branding.env (Pfad oder dict). Voll backward-kompatibel.
    if isinstance(brand_env, dict):
        env_vals = brand_env
    else:
        env_vals = load_branding(brand_env)
    for k in _BRAND_DEFAULTS:
        if env_vals.get(k):
            vals[k] = env_vals[k]

    # Schicht 2: brand.json (ueberschreibt branding.env/Defaults).
    if isinstance(brand_json, dict):
        json_vals = brand_json
    else:
        json_vals = load_brand_json(brand_json, warn=warn)
    for k, v in json_vals.items():
        if v not in (None, ""):
            vals[k] = v

    # Schicht 1: explizite Overrides (hoechste Prioritaet).
    if overrides:
        for k, v in overrides.items():
            if v not in (None, ""):
                vals[k] = v

    return vals


def _font_sizes(fmt: AdFormat) -> dict:
    """Schriftgroessen relativ zur (konstanten) Breite 1080 -> konsistent ueber Formate."""
    w = fmt.width
    return {
        "fs_brand": round(w * 0.030),
        "fs_eyebrow": round(w * 0.026),
        "fs_headline": round(w * 0.072),
        "fs_subline": round(w * 0.036),
        "fs_cta": round(w * 0.034),
    }


# SKILL-072: Default-Stil = Bestandsverhalten. Wird build_html() KEIN style-dict
# uebergeben (Bestands-Aufrufer, Tests), gilt exakt dieser Default -> das gerenderte
# Creative ist identisch zu vor SKILL-072 (nicht-brechend).
DEFAULT_STYLE: dict = {
    "layout": "template",
    "theme": "dark",
    "hero_token": "",
    "hero_scale": HERO_SCALE_DEFAULT,
    "headline_weight": "bold",   # bold=800 | black=900
    "headline_case": "mixed",    # mixed=none | upper=uppercase
    "tracking": "normal",        # normal=-0.01em | tight=-0.03em
    "kicker_font": "sans",       # sans (Default) | serif-italic
    "accent_as_block": False,    # Headline/Hero in Akzentfarbe (Farbe als Flaeche)
    "chrome": "full",            # full (Default) | minimal
}

# SKILL-072: Uebersetzung der Stil-Parameter in Template-Werte.
_HEADLINE_WEIGHT = {"bold": 800, "black": 900}
_HEADLINE_CASE = {"mixed": "none", "upper": "uppercase"}
_TRACKING = {"normal": "-0.01em", "tight": "-0.03em"}


def _style_ctx(style: dict | None, fmt: AdFormat) -> dict:
    """SKILL-072: baut den Template-Kontext fuer Layout + Stil-Parameter.

    Fehlt `style` (oder ein Key), greift DEFAULT_STYLE -> Bestandsverhalten. Chrome
    "minimal" schaltet Brand-Name, Top-Balken und CTA-Pill (als Text-Link) einzeln
    ab (Hebel "weniger Ad-Chrome"). Die numerischen Font-/Tracking-Werte werden hier
    aufgeloest, damit das Template rein deklarativ bleibt.
    """
    s = dict(DEFAULT_STYLE)
    if style:
        s.update({k: v for k, v in style.items() if v is not None})

    chrome_full = str(s.get("chrome", "full")) != "minimal"
    weight = _HEADLINE_WEIGHT.get(str(s.get("headline_weight")), 800)
    case = _HEADLINE_CASE.get(str(s.get("headline_case")), "none")
    tracking = _TRACKING.get(str(s.get("tracking")), "-0.01em")
    kicker_serif = str(s.get("kicker_font")) == "serif-italic"
    try:
        hero_scale = float(s.get("hero_scale", HERO_SCALE_DEFAULT))
    except (TypeError, ValueError):
        hero_scale = HERO_SCALE_DEFAULT

    return {
        "layout": str(s.get("layout", "template")),
        "hero_token": s.get("hero_token") or "",
        "fs_hero": round(fmt.height * hero_scale),
        "headline_weight_val": weight,
        "headline_case_val": case,
        "headline_tracking": tracking,
        "kicker_serif": kicker_serif,
        "accent_as_block": bool(s.get("accent_as_block", False)),
        # Chrome-Schalter (full -> alles an wie bisher; minimal -> aus)
        "chrome_bar": chrome_full,
        "chrome_brand": chrome_full,
        "chrome_pill": chrome_full,
    }


def build_html(content: AdContent, fmt: AdFormat, brand: dict, debug_safe: bool = False,
               style: dict | None = None) -> str:
    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATE_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    tpl = env.get_template("ad_image.html.j2")
    ctx = {
        "w": fmt.width, "h": fmt.height,
        "safe_top": fmt.safe_top, "safe_bottom": fmt.safe_bottom, "safe_x": fmt.safe_x,
        "bg": brand["BRAND_BG"], "bg_soft": brand["BRAND_BG_SOFT"],
        "accent": brand["BRAND_ACCENT"], "ink": brand["BRAND_INK"],
        "ink_muted": brand["BRAND_INK_MUTED"], "font": brand["BRAND_FONT"],
        "brand_name": content.brand_name or brand.get("BRAND_NAME", ""),
        "eyebrow": content.eyebrow, "headline": content.headline,
        "subline": content.subline, "cta": content.cta,
        # SKILL-032-Fix: bg_image als data-URI einbetten (wie Logo) — file:// laedt
        # unter Playwrights set_content/about:blank-Basis NICHT (Foto-bg blieb sonst leer).
        "bg_image": _as_data_uri(content.bg_image) if content.bg_image else "",
        "debug_safe": debug_safe,
        # SKILL-073: KI-Disclosure-Gate verdrahten. Sobald content.ai_image/ai_voice
        # gesetzt ist (z.B. KI-generierter Hintergrund, source=magnific-gen), rendert
        # das Template das sichtbare Pflicht-Label (SKILL-028). Ohne KI-Anteil bleibt
        # das Flag False -> Template unveraendert (nicht-brechend).
        "ai_disclosure": requires_ai_disclosure(content),
        "ai_label_text": AI_LABEL_TEXT,
    }
    ctx.update(_font_sizes(fmt))
    ctx.update(_logo_ctx(brand))  # SKILL-029: Logo-Slot (additiv; leer = unveraendertes Verhalten)
    ctx.update(_style_ctx(style, fmt))  # SKILL-072: Layout-Archetyp + Stil-Parameter
    return tpl.render(**ctx)


def _logo_ctx(brand: dict) -> dict:
    """SKILL-029: Logo-Kontext fuers Template.

    Ist ein Logo gesetzt UND die Datei aufloesbar, wird es als file://-/data-URI
    eingebettet (wie bg_image) und an der konfigurierten Position in der oberen
    Safe-Zone platziert. Ohne (gueltiges) Logo -> leerer Kontext, Template faellt
    auf den bisherigen brand_name-Text zurueck (Verhalten unveraendert).
    """
    raw = (brand.get("LOGO_PATH") or "").strip()
    if not raw:
        return {"logo_url": ""}
    # Datei muss aufloesbar sein, sonst wird nichts eingebettet (EARS-4: keine Halb-Referenz).
    if not raw.startswith(("http://", "https://", "file://", "data:")) and not os.path.isfile(raw):
        return {"logo_url": ""}
    pos = (brand.get("LOGO_POSITION") or _LOGO_DEFAULTS["LOGO_POSITION"]).strip().lower()
    if pos not in _LOGO_POSITIONS:
        pos = _LOGO_DEFAULTS["LOGO_POSITION"]
    try:
        height_pct = float(brand.get("LOGO_HEIGHT_PCT") or _LOGO_DEFAULTS["LOGO_HEIGHT_PCT"])
    except (TypeError, ValueError):
        height_pct = float(_LOGO_DEFAULTS["LOGO_HEIGHT_PCT"])
    return {
        # SKILL-029: data-URI -> Logo laedt zuverlaessig unter Playwrights about:blank-Basis.
        "logo_url": _as_data_uri(raw),
        "logo_position": pos,
        "logo_height_pct": height_pct,
    }


def _bg_query_from_content(content: AdContent) -> str:
    """SKILL-073: Fallback-Suchbegriff fuers Hintergrundbild aus Eyebrow+Headline.

    Strippt Inline-HTML (z.B. <span class='hl'>) aus der Headline, sodass ein
    sauberer Text-Query an die Bildquelle geht.
    """
    import re
    raw = " ".join(x for x in [content.eyebrow, content.headline] if x)
    return re.sub(r"<[^>]+>", " ", raw).strip()


def _as_url(path: str) -> str:
    if path.startswith(("http://", "https://", "file://", "data:")):
        return path
    return pathlib.Path(path).resolve().as_uri()


# SKILL-029: Bilddatei als data-URI einbetten. Playwrights set_content() laeuft auf einer
# about:blank-Basis -> file://-Ressourcen werden vom Browser blockiert (naturalWidth=0).
# data-URIs laden unabhaengig vom Origin -> Logo erscheint zuverlaessig im PNG.
_IMG_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
             ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml"}


def _as_data_uri(path: str) -> str:
    """Lokale Bilddatei -> data:-URI. Remote/bereits-URI-Pfade bleiben unveraendert."""
    import base64
    import urllib.parse
    import urllib.request

    if path.startswith(("http://", "https://", "data:")):
        return path
    raw = path
    if raw.startswith("file://"):
        raw = urllib.request.url2pathname(urllib.parse.urlparse(raw).path)
    p = pathlib.Path(raw)
    if not p.is_file():
        return _as_url(path)
    mime = _IMG_MIME.get(p.suffix.lower(), "application/octet-stream")
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


# SKILL-032: Cache-Verzeichnis fuer pro-Format content-aware Crops von bg_image.
_CROP_CACHE_DIRNAME = "_bg_crops"


def _bg_image_for_format(content: AdContent, fmt: AdFormat, out_dir: pathlib.Path,
                         use_smartcrop: bool):
    """SKILL-032: Liefert den fuer dieses Format zu verwendenden bg_image-Pfad.

    Ist ein lokales ``content.bg_image`` gesetzt und ``use_smartcrop`` aktiv,
    wird das Foto **content-aware** auf das Ziel-Ratio des Formats gecroppt
    (Saliency via smartcrop, Fallback = zentriert-oberer Crop) und der Crop-Pfad
    zurueckgegeben — schliesst SKILL-020 EARS-6 (kein blindes ``cover`` mehr).

    Bricht das Crop fehl (z.B. Remote-URL, fehlende Datei, Lib-Fehler), bleibt das
    Verhalten unveraendert: das Original-bg_image wird zurueckgegeben (nicht-brechend).
    Ohne bg_image -> "" (Verhalten exakt wie bisher).
    """
    raw = (content.bg_image or "").strip()
    if not raw:
        return ""
    if not use_smartcrop:
        return raw
    # Remote/Data-URIs koennen lokal nicht gecroppt werden -> unveraendert lassen.
    if raw.startswith(("http://", "https://", "data:")):
        return raw
    local = raw
    if local.startswith("file://"):
        import urllib.parse
        import urllib.request
        local = urllib.request.url2pathname(urllib.parse.urlparse(local).path)
    if not os.path.isfile(local):
        return raw  # nicht-brechend: Template faellt auf cover zurueck
    try:
        from .cropping import crop_to_format
        cache = out_dir / _CROP_CACHE_DIRNAME
        crop_out = cache / f"{(content.ad_id or 'creative')}__{fmt.key}__bg.jpg"
        res = crop_to_format(local, fmt, crop_out, use_smartcrop=True)
        if res.upscaled:
            print(f"[WARN] SKILL-032: bg_image fuer {fmt.key} musste hochskaliert "
                  f"werden (Quelle kleiner als {fmt.width}x{fmt.height}) — "
                  f"hoeher aufgeloestes Foto liefern (vgl. Meta-Mindestkante).",
                  file=sys.stderr)
        return str(res.out)
    except Exception as exc:  # nicht-brechend: bei jedem Crop-Fehler Original nutzen
        print(f"[WARN] SKILL-032: content-aware Crop fehlgeschlagen ({exc}) — "
              f"Original-bg_image wird per cover genutzt.", file=sys.stderr)
        return raw


def render(content: AdContent, format_keys, brand: dict, out_dir: str,
           debug_safe: bool = False, smartcrop_bg: bool = True,
           style: dict | None = None, write_meta: bool = True) -> list[str]:
    """Rendert das Creative in allen angegebenen Formaten. Gibt die PNG-Pfade zurueck.

    SKILL-032: Ist ``content.bg_image`` ein lokales Foto und ``smartcrop_bg`` True
    (Default), wird es vor dem Template-Build pro Format content-aware auf das
    Ziel-Ratio gecroppt (statt blindem CSS-``cover``). Ohne bg_image bzw. mit
    ``smartcrop_bg=False`` ist das Verhalten exakt wie vorher (nicht-brechend).

    SKILL-072: ``style`` (optional) waehlt Layout-Archetyp + Stil-Parameter. Ohne
    ``style`` (Bestands-Aufrufer wie batch.py) gilt DEFAULT_STYLE -> Bestandsverhalten.

    SKILL-086 (Methoden-Tagging): Der Dateiname traegt den Framework-Key, sobald ein
    nicht-Default-Framework gesetzt ist (`image_output_stem`), und je PNG wird ein
    Sidecar `<name>.json` mit explizitem `framework`-Feld + variant_id/utm_content
    geschrieben (``write_meta`` True, Default). So ist aus jedem Artefakt die Methode
    ablesbar. ``write_meta=False`` unterdrueckt den Sidecar (z.B. batch.py, das ein
    eigenes manifest.json fuehrt).
    """
    from playwright.sync_api import sync_playwright

    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for key in format_keys:
                fmt = get_format(key)
                # SKILL-032: pro Format ein ratio-korrektes Crop des Hintergrundfotos.
                bg_for_fmt = _bg_image_for_format(content, fmt, out, smartcrop_bg)
                fmt_content = content
                if bg_for_fmt != (content.bg_image or ""):
                    fmt_content = replace(content, bg_image=bg_for_fmt)
                html = build_html(fmt_content, fmt, brand, debug_safe, style=style)
                page = browser.new_page(
                    viewport={"width": fmt.width, "height": fmt.height},
                    device_scale_factor=1,
                )
                page.set_content(html, wait_until="load")
                page.wait_for_timeout(150)  # Layout/Fonts settlen
                # SKILL-086: Framework-taggender Dateiname (Default -> Bestands-Name).
                stem = image_output_stem(content, fmt)
                path = out / f"{stem}.png"
                page.screenshot(path=str(path),
                                clip={"x": 0, "y": 0, "width": fmt.width, "height": fmt.height})
                page.close()
                written.append(str(path))
                # SKILL-086: Sidecar-Metadaten mit explizitem framework-Feld.
                if write_meta:
                    meta = build_image_meta(content, fmt)
                    (out / f"{stem}.json").write_text(
                        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
                    )
        finally:
            browser.close()
    return written


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="creative-studio Bild-Renderer (SKILL-020)")
    ap.add_argument("--headline", required=True)
    ap.add_argument("--subline", default="")
    ap.add_argument("--cta", default="")
    ap.add_argument("--eyebrow", default="")
    ap.add_argument("--brand", default="", help="Brand-Name-Override (sonst aus branding.env)")
    ap.add_argument("--bg-image", default="")
    ap.add_argument("--ad-id", default="creative")
    ap.add_argument("--framework", default=DEFAULT_FRAMEWORK,
                    help="SKILL-086: Copy-Framework-Key (Methoden-Tagging) — wandert in "
                         "Dateiname + Sidecar-Metadaten. Keys aus frameworks.FRAMEWORKS "
                         "(pas/aida/mindset_shift/opportunity/avatar_story/heros_journey ...).")
    ap.add_argument("--brand-env", default="", help="Pfad zu branding.env (Brand-Tokens)")
    ap.add_argument("--brand-json", default="",
                    help="SKILL-029: Pfad zu brand.json (Token-Rollen + Logo; ueberschreibt branding.env)")
    ap.add_argument("--formats", default=",".join(DEFAULT_FORMATS),
                    help=f"Komma-Liste aus: {', '.join(FORMATS)}")
    ap.add_argument("--out", default="out")
    ap.add_argument("--debug-safe", action="store_true", help="Safe-Zonen rot einblenden")
    ap.add_argument("--no-smartcrop", action="store_true",
                    help="SKILL-032: content-aware Crop des bg_image deaktivieren "
                         "(blindes CSS-cover wie vor SKILL-032).")
    # --- SKILL-072: Layout-Archetyp + Stil-Parameter (Default = Bestandsverhalten) ---
    ap.add_argument("--layout", default="template", choices=list(LAYOUTS),
                    help="SKILL-072: Layout-Archetyp (Default 'template' = Bestands-Skelett).")
    ap.add_argument("--hero-token", default="",
                    help="SKILL-072: Riesen-Held (Zahl/Kurzwort) fuer --layout stat-hero "
                         "(ohne -> Headline wird Hero).")
    ap.add_argument("--hero-scale", type=float, default=HERO_SCALE_DEFAULT,
                    help=f"SKILL-072: Hoehenanteil des Hero (Sweetspot 0.25-0.40, "
                         f"Default {HERO_SCALE_DEFAULT}).")
    ap.add_argument("--headline-weight", default="bold", choices=["bold", "black"],
                    help="SKILL-072: Schriftschnitt der Headline/Hero.")
    ap.add_argument("--headline-case", default="mixed", choices=["mixed", "upper"],
                    help="SKILL-072: Gross/Klein der Headline (upper = ALL-CAPS Impact).")
    ap.add_argument("--tracking", default="normal", choices=["normal", "tight"],
                    help="SKILL-072: Laufweite der Headline.")
    ap.add_argument("--kicker-font", default="sans", choices=["sans", "serif-italic"],
                    help="SKILL-072: Eyebrow/Kicker-Font (serif-italic = Editorial-Kicker).")
    ap.add_argument("--theme", default="dark", choices=list(THEMES),
                    help="SKILL-072: Farb-Theme (dark = Brand-Default | light-cream). "
                         "Akzent bleibt markeneigen.")
    ap.add_argument("--accent-as-block", action="store_true",
                    help="SKILL-072: Headline/Hero in Akzentfarbe (Farbe als Flaeche).")
    ap.add_argument("--chrome", default="full", choices=["full", "minimal"],
                    help="SKILL-072: 'minimal' schaltet Brand-Name, Top-Balken und "
                         "CTA-Pill ab (organischer Look).")
    # --- SKILL-073: Bildquelle (search-first). Default 'none' = Bestandsverhalten ---
    ap.add_argument("--bg-source", default="none",
                    choices=["none", "library", "stock", "generate"],
                    help="SKILL-073: Hintergrund-/Motiv-Bild ziehen. 'library'/'stock' "
                         "guenstig (Default-tauglich), 'generate' kostet Geld (explizit). "
                         "Der Resolver prueft ZUERST die lokale Bibliothek (search-first).")
    ap.add_argument("--bg-query", default="",
                    help="SKILL-073: Suchbegriff/Prompt fuers Bild (sonst aus Eyebrow+Headline).")
    ap.add_argument("--image-lib", default="",
                    help="SKILL-073: Bibliothekspfad (sonst $CREATIVE_STUDIO_IMAGE_LIB / ./image-library).")
    ap.add_argument("--no-people", dest="no_people", action="store_true", default=True,
                    help="SKILL-073: personenfreie Bilder bevorzugen (Default; gut fuer Paid-Ads).")
    ap.add_argument("--allow-people", dest="no_people", action="store_false",
                    help="SKILL-073: Personen in Bildern zulassen.")
    # --- SKILL-074: Lesbarkeits-/Kontrast-Check (Default aus = nicht-brechend) ---
    ap.add_argument("--check-contrast", action="store_true",
                    help="SKILL-074: Nach dem Render die WCAG-Kontrast-Ratio der "
                         "Text-Regionen gegen den tatsaechlichen Pixel-Hintergrund "
                         "pruefen und warnen (keine Sperre). Sinnvoll v.a. bei Foto-BG.")
    args = ap.parse_args(argv)

    # SKILL-029: brand.json ergaenzt/ueberschreibt branding.env; --brand bleibt hoechste Prioritaet.
    brand = resolve_brand(
        brand_env=args.brand_env or None,
        brand_json=args.brand_json or None,
        overrides={"BRAND_NAME": args.brand} if args.brand else None,
    )
    # SKILL-072: Theme ueber die Brand-Tokens legen (Akzent bleibt markeneigen).
    brand = apply_theme(brand, args.theme)

    content = AdContent(
        headline=args.headline, subline=args.subline, cta=args.cta, eyebrow=args.eyebrow,
        brand_name=args.brand, bg_image=args.bg_image, ad_id=args.ad_id,
        framework=args.framework,  # SKILL-086: Methoden-Tag ins Creative
    )

    # SKILL-073: Bildquelle aufloesen (search-first). Nur wenn gewaehlt UND kein
    # explizites --bg-image gesetzt ist. Ergebnis -> content.bg_image (laeuft durch
    # den bestehenden Smartcrop, SKILL-032). KI-Herkunft -> content.ai_image=True
    # (triggert das Disclosure-Gate, SKILL-028/073).
    if args.bg_source != "none" and not args.bg_image:
        from .image_source import resolve_bg, ImageSourceError
        query = args.bg_query or _bg_query_from_content(content)
        try:
            res = resolve_bg(query, args.bg_source, lib_dir=args.image_lib or None,
                             no_people=args.no_people)
        except ImageSourceError as exc:
            res = None
            print(f"[WARN] SKILL-073: Bildquelle fehlgeschlagen ({exc}) — Gradient-Fallback.",
                  file=sys.stderr)
        if res is not None:
            content.bg_image = res.local_path
            if res.ai_generated:
                content.ai_image = True  # KI-Disclosure-Pflicht (SKILL-028)
                # build_html() rendert das sichtbare Label aus requires_ai_disclosure()
                # -> disclosure gilt als angewendet (kein redundanter Warn-Hinweis).
                content.disclosure_applied = True
            src_note = "lokale Bibliothek" if res.from_cache else f"neu geladen ({res.source})"
            print(f"[OK] SKILL-073: Bild = {res.local_path} ({src_note}; "
                  f"Lizenz {res.license_type} -> {res.license_url}"
                  f"{'; KI-generiert -> Disclosure aktiv' if res.ai_generated else ''})")
        else:
            print(f"[WARN] SKILL-073: kein Bild fuer bg-source='{args.bg_source}' "
                  f"(Query '{query}') — Gradient-Fallback.", file=sys.stderr)

    for w in content.warnings():
        print(f"[WARN] {w}", file=sys.stderr)

    # SKILL-072: Stil-dict fuer den Renderer + Layout-Warnungen (keine Sperre).
    style = {
        "layout": args.layout, "theme": args.theme,
        "hero_token": args.hero_token, "hero_scale": args.hero_scale,
        "headline_weight": args.headline_weight, "headline_case": args.headline_case,
        "tracking": args.tracking, "kicker_font": args.kicker_font,
        "accent_as_block": args.accent_as_block, "chrome": args.chrome,
    }
    for w in layout_warnings(args.layout, hero_scale=args.hero_scale,
                             has_bg_image=bool(content.bg_image)):
        print(f"[WARN] {w}", file=sys.stderr)

    keys = [k.strip() for k in args.formats.split(",") if k.strip()]
    paths = render(content, keys, brand, args.out, debug_safe=args.debug_safe,
                   smartcrop_bg=not args.no_smartcrop, style=style)
    for pth in paths:
        print(f"[OK] {pth}")

    # SKILL-074: optionaler Lesbarkeits-/Kontrast-Check nach dem Render. Additiv,
    # Default aus -> parallele/Bestands-Renders unveraendert. Misst die WCAG-
    # Kontrast-Ratio der Text-Regionen gegen den tatsaechlichen Pixel-Hintergrund
    # und WARNT (keine Sperre); bei Foto-BG zusaetzlich eine Fix-Empfehlung.
    if args.check_contrast:
        from .readability import (check_contrast as _check_contrast,
                                  contrast_warnings as _contrast_warnings,
                                  recommend_contrast_fix as _recommend_fix)
        has_bg = bool(content.bg_image)
        for key, pth in zip(keys, paths):
            fmt = get_format(key)
            for w in _contrast_warnings(pth, fmt, brand, layout=args.layout,
                                        style=style, content=content):
                print(f"[WARN] SKILL-074 [{key}] {w}", file=sys.stderr)
            findings = _check_contrast(pth, fmt, brand, layout=args.layout,
                                       style=style, content=content)
            for rec in _recommend_fix(findings, has_bg_image=has_bg, layout=args.layout):
                print(f"[TIPP] SKILL-074 [{key}] {rec}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
