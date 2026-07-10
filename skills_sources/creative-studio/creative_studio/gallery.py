"""creative-studio — Vorschau-Galerie gallery.html (SKILL-030, QA-Gate vor Launch).

Liest ein `manifest.json` (Output der Batch-Engine SKILL-023) und erzeugt eine
standalone `gallery.html`: ein Grid aller Varianten x Formate fuer die schnelle
menschliche Sichtfreigabe ("Claude generiert, Mensch gibt visuell frei"), BEVOR
Ads live gehen.

Designprinzipien:
  - Reines statisches HTML, file://-tauglich (per Doppelklick im Browser oeffenbar,
    kein Server). Bilder werden ueber RELATIVE Pfade aus dem Manifest-Feld `file`
    referenziert -> die gallery.html liegt im selben Ordner wie manifest.json + Bilder.
  - Markenkonform-schlichter Look in Anlehnung an templates/ad_image.html.j2
    (dunkler Grund, dezenter Akzent, System-Font-Stack -> zuverlaessige Umlaute).
  - Robust: fehlende Bilddatei -> Platzhalter statt Crash; Warnungen (gelb) und
    Fehler/`not_implemented` (rot) werden sichtbar markiert statt still weggelassen.

Manifest-Schema (aus batch.py / SKILL-023), je Eintrag:
    {variant_id, ad_id, framework, hook, format, media, file, utm_content}
  optional: warnings (list[str]), error (str), status (z.B. "not_implemented"), note (str)

CLI:
    python -m creative_studio.gallery --manifest <pfad/manifest.json> [--out gallery.html]
"""
from __future__ import annotations
import argparse
import html
import json
import pathlib
from collections import OrderedDict


# SKILL-030: Markenkonform-schlichter, in sich geschlossener Look (analog ad_image.html.j2).
# Bewusst inline -> die gallery.html ist eine einzige, transportable Datei.
_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --bg: #0a0e27; --bg-soft: #141a3a; --card: #161c40; --accent: #4f7cff;
  --ink: #f4f6ff; --ink-muted: #aab2d5; --warn: #f5b50a; --error: #ff5470;
  --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
body {
  font-family: var(--font); color: var(--ink); min-height: 100vh;
  background: radial-gradient(120% 60% at 50% 0%, var(--bg-soft) 0%, var(--bg) 60%);
  padding: 32px 28px 64px;
}
header { max-width: 1400px; margin: 0 auto 28px; }
header .accent-bar { height: 4px; width: 64px; background: var(--accent); border-radius: 999px; margin-bottom: 14px; }
header h1 { font-size: 26px; font-weight: 800; letter-spacing: -0.01em; }
header .meta { color: var(--ink-muted); font-size: 14px; margin-top: 6px; }
.group { max-width: 1400px; margin: 0 auto 36px; }
.group > h2 { font-size: 16px; font-weight: 700; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.06em; margin: 24px 0 14px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 18px; }
.card { background: var(--card); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px; overflow: hidden; display: flex; flex-direction: column; }
.card.has-error { border-color: var(--error); }
.card.has-warn { border-color: var(--warn); }
.thumb { aspect-ratio: 4 / 5; background: #0b0f25; display: flex; align-items: center;
  justify-content: center; overflow: hidden; }
.thumb img { width: 100%; height: 100%; object-fit: contain; display: block; }
.placeholder { color: var(--ink-muted); font-size: 13px; text-align: center; padding: 18px; line-height: 1.4; }
.body { padding: 12px 14px 14px; display: flex; flex-direction: column; gap: 6px; }
.vid { font-size: 13px; font-weight: 700; word-break: break-all; }
.row { font-size: 12px; color: var(--ink-muted); }
.row b { color: var(--ink); font-weight: 600; }
.badge { display: inline-block; font-size: 11px; font-weight: 700; padding: 2px 8px;
  border-radius: 999px; letter-spacing: 0.02em; }
.badge.media { background: rgba(79,124,255,0.18); color: var(--accent); }
.utm { font-size: 11px; color: var(--ink-muted); word-break: break-all;
  background: rgba(0,0,0,0.25); padding: 5px 7px; border-radius: 7px; }
.flag { font-size: 12px; border-radius: 8px; padding: 7px 9px; line-height: 1.35; }
.flag.warn { background: rgba(245,181,10,0.14); color: var(--warn); border: 1px solid rgba(245,181,10,0.4); }
.flag.error { background: rgba(255,84,112,0.14); color: var(--error); border: 1px solid rgba(255,84,112,0.45); }
.flag .lbl { font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em; margin-right: 4px; }
""".strip()


def _esc(value) -> str:
    """HTML-escape; None -> leerer String."""
    return html.escape("" if value is None else str(value))


# SKILL-030: eine Kachel pro Variante. Bild ueber RELATIVEN Pfad (file://-tauglich).
def _render_card(entry: dict) -> str:
    vid = entry.get("variant_id") or "(ohne variant_id)"
    framework = entry.get("framework") or "-"
    fmt = entry.get("format") or "-"
    media = entry.get("media") or "image"
    utm = entry.get("utm_content") or ""
    hook = entry.get("hook") or ""
    file_rel = entry.get("file")
    warnings = entry.get("warnings") or []
    error = entry.get("error")
    status = entry.get("status")
    note = entry.get("note")

    classes = ["card"]
    if error or status == "not_implemented":
        classes.append("has-error")
    elif warnings:
        classes.append("has-warn")

    # --- Thumbnail / Platzhalter -------------------------------------------
    if file_rel and media != "video":
        # onerror -> robuste Anzeige eines Platzhalters falls die Datei am
        # Galerie-Standort fehlt (EARS: kein Crash bei fehlendem Bild).
        ph = _esc(file_rel)
        thumb = (
            f'<img src="{_esc(file_rel)}" alt="{_esc(vid)}" '
            f"onerror=\"this.style.display='none';"
            f"this.parentNode.innerHTML='<div class=&quot;placeholder&quot;>"
            f"Bild nicht gefunden:<br>{ph}</div>';\">"
        )
    elif media == "video":
        label = note or status or "Video (kein Vorschaubild)"
        thumb = f'<div class="placeholder">VIDEO<br>{_esc(label)}</div>'
    else:
        thumb = '<div class="placeholder">Kein Bild gerendert</div>'

    # --- Flags (Fehler rot, Warnungen gelb) --------------------------------
    flags = []
    if error:
        flags.append(f'<div class="flag error"><span class="lbl">Fehler</span>{_esc(error)}</div>')
    if status == "not_implemented":
        msg = note or "Noch nicht implementiert."
        flags.append(
            f'<div class="flag error"><span class="lbl">not_implemented</span>{_esc(msg)}</div>'
        )
    for w in warnings:
        flags.append(f'<div class="flag warn"><span class="lbl">Warnung</span>{_esc(w)}</div>')

    parts = [
        f'<div class="{" ".join(classes)}">',
        f'  <div class="thumb">{thumb}</div>',
        '  <div class="body">',
        f'    <div class="vid">{_esc(vid)}</div>',
        f'    <div class="row"><b>Framework:</b> {_esc(framework)} '
        f'&nbsp;&middot;&nbsp; <b>Format:</b> {_esc(fmt)} '
        f'&nbsp;&middot;&nbsp; <span class="badge media">{_esc(media)}</span></div>',
    ]
    if hook:
        parts.append(f'    <div class="row"><b>Hook:</b> {_esc(hook)}</div>')
    if utm:
        parts.append(f'    <div class="utm">utm_content={_esc(utm)}</div>')
    parts.extend(f"    {f}" for f in flags)
    parts.append("  </div>")
    parts.append("</div>")
    return "\n".join(parts)


# SKILL-030: Gruppierung nach Format (Plus laut Spec) -> Varianten je Format auf einen Blick.
def _group_entries(entries: list[dict], group_by: str) -> "OrderedDict[str, list[dict]]":
    groups: "OrderedDict[str, list[dict]]" = OrderedDict()
    for e in entries:
        key = str(e.get(group_by) or "(ohne)")
        groups.setdefault(key, []).append(e)
    return groups


def build_html(manifest: dict, group_by: str = "format") -> str:
    """Baut die komplette standalone gallery.html als String (SKILL-030 EARS-1/2/3/5)."""
    entries = list(manifest.get("variants") or [])
    ad_id = manifest.get("ad_id", "")
    formats = manifest.get("formats") or []
    count = manifest.get("count", len(entries))

    n_warn = sum(1 for e in entries if e.get("warnings"))
    n_err = sum(1 for e in entries if e.get("error") or e.get("status") == "not_implemented")

    meta_line = (
        f"{_esc(count)} Varianten &nbsp;&middot;&nbsp; "
        f"Formate: {_esc(', '.join(map(str, formats)) or '-')} &nbsp;&middot;&nbsp; "
        f'<span style="color:var(--warn)">{n_warn} Warnung(en)</span> &nbsp;&middot;&nbsp; '
        f'<span style="color:var(--error)">{n_err} Fehler</span>'
    )

    sections = []
    if group_by and entries:
        for key, items in _group_entries(entries, group_by).items():
            cards = "\n".join(_render_card(e) for e in items)
            sections.append(
                f'<section class="group"><h2>{_esc(group_by)}: {_esc(key)} '
                f"({len(items)})</h2>\n<div class=\"grid\">\n{cards}\n</div></section>"
            )
    else:
        cards = "\n".join(_render_card(e) for e in entries) or (
            '<div class="placeholder">Keine Varianten im Manifest.</div>'
        )
        sections.append(f'<section class="group"><div class="grid">\n{cards}\n</div></section>')

    title = f"creative-studio — Vorschau-Galerie{(' · ' + _esc(ad_id)) if ad_id else ''}"
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{_CSS}
</style>
</head>
<body>
<header>
  <div class="accent-bar"></div>
  <h1>{title}</h1>
  <div class="meta">{meta_line}</div>
</header>
{chr(10).join(sections)}
</body>
</html>
"""


def build_gallery(manifest_path: str, out_path: str | None = None,
                  group_by: str = "format") -> pathlib.Path:
    """Liest manifest.json, schreibt gallery.html in DENSELBEN Ordner (EARS-3/4).

    Gibt den Pfad der geschriebenen Datei zurueck. out_path ist optional; ohne ihn
    landet die Galerie als 'gallery.html' neben dem Manifest (relative Bild-Pfade
    bleiben gueltig).
    """
    mpath = pathlib.Path(manifest_path)
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    out = pathlib.Path(out_path) if out_path else (mpath.parent / "gallery.html")
    if not out.is_absolute() and out.parent == pathlib.Path("."):
        # blosser Dateiname -> neben das Manifest schreiben, damit relative Bildpfade stimmen
        out = mpath.parent / out.name
    html_str = build_html(manifest, group_by=group_by)
    out.write_text(html_str, encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="creative-studio Vorschau-Galerie (SKILL-030, QA-Gate vor Launch)"
    )
    ap.add_argument("--manifest", required=True, help="Pfad zur manifest.json (SKILL-023)")
    ap.add_argument("--out", default="", help="Ziel-HTML (Default: gallery.html neben dem Manifest)")
    ap.add_argument("--group-by", default="format",
                    help="Gruppieren nach Manifest-Feld (format|framework|media), '' = keine Gruppen")
    args = ap.parse_args(argv)

    out = build_gallery(args.manifest, args.out or None, group_by=args.group_by or "")
    print(f"[OK] gallery.html geschrieben -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
