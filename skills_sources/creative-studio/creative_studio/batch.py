"""creative-studio — Batch-/Varianten-Engine (SKILL-023).

Aus EINER Job-Definition (job.yaml) erzeugt der Skill in einem Lauf alle
Kombinationen aus N Hooks/Varianten x M Formate x Medientyp und schreibt ein
`manifest.json` als universelle Schnittstelle zu DCO-Export (SKILL-031) und
Reporting-Rueckkanal (SKILL-033).

Naming (variant_id + utm_content) kommt AUSSCHLIESSLICH aus specs.py
(SKILL-024) — diese Engine definiert kein eigenes Namensschema.

Multi-Projekt (EARS-4): Brand + Content + Formate kommen nur aus Job-Datei/CLI;
kein hartkodierter Projektwert/Pfad hier.

Job-Schema (job.yaml):
    ad_id: h1-immo
    brand_env: /pfad/zu/branding.env        # optional, per --brand-env ueberschreibbar
    brand_json: {BRAND_BG: "#000", ...}      # optional, inline-Override (gewinnt ueber brand_env)
    formats: [square_1x1, feed_4x5, story_9x16]  # optional; fehlt es -> DEFAULT_FORMATS (alle 3)
    media: [image]                           # image (video = spaetere Ausbaustufe, s. TODO)
    variants:
      - {framework: bab, eyebrow: "...", headline: "...", subline: "...", cta: "..."}
      - ...

CLI:
    python -m creative_studio.batch --job job.yaml --out <dir> [--brand-env <pfad>]
"""
from __future__ import annotations
import argparse
import json
import pathlib
import sys

import yaml

from .specs import (
    AdContent,
    DEFAULT_FORMATS,
    FORMATS,
    make_utm_content,
    make_variant_id,
)
from .render_image import load_branding, render


# SKILL-023: Job-Datei laden + projektneutral validieren.
def load_job(job_path: str) -> dict:
    """Liest job.yaml (oder JSON, da YAML ein JSON-Superset ist) und gibt das Dict zurueck."""
    data = yaml.safe_load(pathlib.Path(job_path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Job-Datei {job_path} muss ein Mapping (ad_id/formats/variants/...) sein.")
    if not data.get("variants"):
        raise ValueError("Job-Datei enthaelt kein nicht-leeres 'variants'-Feld.")
    return data


def _content_from_variant(ad_id: str, brand_name: str, variant: dict) -> AdContent:
    """Baut ein AdContent aus einem Job-Varianten-Dict (knuepft an bestehende AdContent-Felder an)."""
    return AdContent(
        headline=str(variant.get("headline", "")),
        subline=str(variant.get("subline", "")),
        cta=str(variant.get("cta", "")),
        eyebrow=str(variant.get("eyebrow", "")),
        brand_name=str(variant.get("brand_name", "") or brand_name),
        bg_image=str(variant.get("bg_image", "")),
        ad_id=ad_id,
    )


def run_batch(job: dict, out_dir: str, brand_env_override: str | None = None,
              debug_safe: bool = False) -> dict:
    """Rendert alle Kombinationen Variante x Format x Medium und schreibt manifest.json.

    SKILL-023 EARS-1: ein Lauf -> alle Kombinationen.
    SKILL-023 EARS-2: manifest.json mit variant_id/framework/hook/format/medium/file/utm_content.
    SKILL-023 EARS-5: einzelner Render-Fehler bricht den Lauf NICHT ab; er wird je Variante markiert.

    Gibt das Manifest-Dict zurueck (wird auch nach <out_dir>/manifest.json geschrieben).
    """
    ad_id = str(job.get("ad_id", "creative"))
    formats = list(job.get("formats") or DEFAULT_FORMATS)
    media = [str(m).lower() for m in (job.get("media") or ["image"])]
    variants = job["variants"]

    # Brand laden: --brand-env (CLI) gewinnt ueber job.brand_env; brand_json (inline) gewinnt ueber beides.
    brand_env = brand_env_override or job.get("brand_env")
    brand = load_branding(brand_env or None)
    if isinstance(job.get("brand_json"), dict):
        for k, v in job["brand_json"].items():
            if v:
                brand[k] = v
    brand_name = brand.get("BRAND_NAME", "")

    out_root = pathlib.Path(out_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    image_formats = [k for k in formats if k in FORMATS]
    unknown_formats = [k for k in formats if k not in FORMATS]
    for k in unknown_formats:
        print(f"[WARN] Unbekanntes Format '{k}' wird uebersprungen (bekannt: {', '.join(FORMATS)}).")

    entries: list[dict] = []

    for hook_index, variant in enumerate(variants):
        framework = str(variant.get("framework", "default"))
        content = _content_from_variant(ad_id, brand_name, variant)
        hook = content.headline or content.eyebrow  # Hook = Headline, sonst Eyebrow

        # SKILL-023: AdContent.warnings() je Variante ins Log (+ optional ins Manifest).
        var_warnings = content.warnings()
        for w in var_warnings:
            print(f"[WARN] Variante {hook_index} ({framework}): {w}")

        # --- IMAGE ----------------------------------------------------------
        if "image" in media and image_formats:
            for fmt_key in image_formats:
                # SKILL-024: variant_id + utm_content aus der zentralen Systematik.
                vid = make_variant_id(ad_id, hook, framework, fmt_key, hook_index=hook_index)
                utm = make_utm_content(vid)
                entry = {
                    "variant_id": vid,
                    "ad_id": ad_id,
                    "framework": framework,
                    "hook": hook,
                    "format": fmt_key,
                    "media": "image",
                    "file": None,
                    "utm_content": utm,
                }
                if var_warnings:
                    entry["warnings"] = list(var_warnings)
                try:
                    # render() schreibt mit Stem <ad_id>__<fmt>; wir benennen danach auf variant_id um,
                    # damit Dateiname == variant_id (eindeutig je Hook).
                    paths = render(content, [fmt_key], brand, str(out_root), debug_safe=debug_safe)
                    src = pathlib.Path(paths[0])
                    final = out_root / f"{vid}.png"
                    if src.resolve() != final.resolve():
                        if final.exists():
                            final.unlink()
                        src.rename(final)
                    entry["file"] = final.name
                    print(f"[OK] {final.name}  (utm_content={utm})")
                except Exception as exc:  # EARS-5: weiter, Fehler je Variante markieren
                    entry["error"] = f"{type(exc).__name__}: {exc}"
                    print(f"[WARN] Render fehlgeschlagen ({vid}): {exc}", file=sys.stderr)
                entries.append(entry)

        # --- VIDEO ----------------------------------------------------------
        # TODO(SKILL-023/EARS-3): Video-Medium ueber video/-Modul (Remotion) anbinden.
        # Bewusst NICHT gefaked — wird als geplanter Eintrag markiert, kein Datei-Output.
        if "video" in media:
            for fmt_key in image_formats or formats:
                vid = make_variant_id(ad_id, hook, framework, fmt_key, hook_index=hook_index)
                entries.append({
                    "variant_id": vid,
                    "ad_id": ad_id,
                    "framework": framework,
                    "hook": hook,
                    "format": fmt_key,
                    "media": "video",
                    "file": None,
                    "utm_content": make_utm_content(vid),
                    "status": "not_implemented",
                    "note": "Video-Renderer (video/-Modul) noch nicht angebunden — TODO SKILL-023.",
                })
                print(f"[WARN] Video-Variante {vid} geplant aber nicht gerendert (TODO video/-Modul).")

    manifest = {
        "ad_id": ad_id,
        "formats": formats,
        "media": media,
        "count": len(entries),
        "variants": entries,
    }
    manifest_path = out_root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] manifest.json geschrieben ({len(entries)} Eintraege) -> {manifest_path}")
    return manifest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="creative-studio Batch-/Varianten-Engine (SKILL-023)")
    ap.add_argument("--job", required=True, help="Pfad zur job.yaml (ad_id/formats/media/variants)")
    ap.add_argument("--out", default="out", help="Output-Verzeichnis (Manifest landet dort)")
    ap.add_argument("--brand-env", default="", help="Pfad zu branding.env (ueberschreibt job.brand_env)")
    ap.add_argument("--debug-safe", action="store_true", help="Safe-Zonen rot einblenden")
    args = ap.parse_args(argv)

    job = load_job(args.job)
    run_batch(job, args.out, brand_env_override=(args.brand_env or None), debug_safe=args.debug_safe)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
