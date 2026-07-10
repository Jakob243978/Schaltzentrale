"""creative-studio — Lesbarkeits-/Kontrast-Check der Text-Regionen (SKILL-074).

Motiv (Live-Use, Jakob 2026-07-08): Bei Foto-Hintergruenden (Layout
``photo-poster``/``object-hero``, SKILL-072/073) ist der Text manchmal schlecht
lesbar — der Untergrund unter dem Text variiert (heller Himmel unter heller
Headline). Die Theme-Farbe allein sagt nichts ueber den TATSAECHLICHEN Pixel-
Hintergrund. Dieser Check misst nach dem Rendern die WCAG-Kontrast-Ratio zwischen
Textfarbe und dem tatsaechlich gerenderten Hintergrund UNTER jeder Text-Region und
**warnt** (kein Blocken — konsistent mit ``layout_warnings()``/``compliance_warnings()``,
Warn-statt-Block-Muster, Mensch-im-Loop).

Rein PIL-basiert (Pillow ist bereits Dependency — keine neue Abhaengigkeit).

Multi-Projekt (Prinzip skill-muss-multi-projekt-tauglich): kein hartkodierter
Brand-/Projektwert. Textfarben kommen aus den Brand-Tokens + Stil, die Geometrie
aus ``specs.AdFormat`` (Safe-Zones) + Layout — alles als Parameter.

Standalone-CLI:
    python -m creative_studio.readability <bild.png> --format feed_4x5 \
        --layout photo-poster --ink "#faf7f2" --accent "#f25d3e" --ink-muted "#9a9ec0"
"""
from __future__ import annotations

import argparse
import pathlib
from dataclasses import dataclass

from PIL import Image

from .specs import AdFormat, get_format

# === WCAG-2.1-Schwellwerte (AA) ==============================================
# Kleiner Text (Subline/CTA/Kicker): 4.5:1. Grosser Text (Headline/Hero,
# >= ~24px bzw. >= ~18.66px fett): 3:1. Werte aus WCAG 2.1 SC 1.4.3.
WCAG_AA_NORMAL = 4.5
WCAG_AA_LARGE = 3.0

# Analyse-Raster pro Region: die Region wird in cols x rows Kacheln zerlegt, je
# Kachel der Mittelwert (Hintergrund-Schaetzer). Der WORST-CASE ueber alle
# Kacheln ist die Region-Kontrast-Ratio (ein heller Fleck unter dem Text reicht,
# um die Lesbarkeit zu kippen). Duenne Text-Striche verschieben den Kachel-
# Mittelwert leicht Richtung Textfarbe -> konservativ (eher warnen).
DEFAULT_GRID: tuple[int, int] = (6, 3)


# === WCAG-Kontrast-Kern (reine Funktionen) ===================================
def _channel_to_linear(c8: float) -> float:
    """8-bit-Kanal (0-255) -> linearer sRGB-Wert (WCAG 2.1 Definition)."""
    cs = c8 / 255.0
    if cs <= 0.03928:
        return cs / 12.92
    return ((cs + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: tuple[float, float, float]) -> float:
    """WCAG-Relativ-Luminanz L eines RGB-Tripels (0-255 je Kanal), 0.0-1.0."""
    r, g, b = rgb[0], rgb[1], rgb[2]
    return (
        0.2126 * _channel_to_linear(r)
        + 0.7152 * _channel_to_linear(g)
        + 0.0722 * _channel_to_linear(b)
    )


def contrast_ratio(rgb1, rgb2) -> float:
    """WCAG-Kontrast-Ratio zwischen zwei Farben (1.0-21.0). Reihenfolge egal."""
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter, darker = (l1, l2) if l1 >= l2 else (l2, l1)
    return (lighter + 0.05) / (darker + 0.05)


# === Farb-Parsing (Hex / rgb() / benannte Basisfarben) =======================
_NAMED = {
    "white": (255, 255, 255), "black": (0, 0, 0),
    "red": (255, 0, 0), "green": (0, 128, 0), "blue": (0, 0, 255),
}


def parse_color(value: str) -> tuple[int, int, int]:
    """Parst '#rgb' / '#rrggbb' / 'rgb(r,g,b)' / Basis-Namen -> (r,g,b).

    Unparsbare/leere Eingabe -> Schwarz (0,0,0) als sicherer Default (kein Crash).
    """
    if value is None:
        return (0, 0, 0)
    s = str(value).strip().lower()
    if not s:
        return (0, 0, 0)
    if s in _NAMED:
        return _NAMED[s]
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        if len(h) >= 6:
            try:
                return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            except ValueError:
                return (0, 0, 0)
    if s.startswith("rgb"):
        inside = s[s.find("(") + 1: s.find(")")] if "(" in s else ""
        parts = [p.strip() for p in inside.split(",")[:3]]
        try:
            vals = [max(0, min(255, int(round(float(p))))) for p in parts]
            if len(vals) == 3:
                return (vals[0], vals[1], vals[2])
        except ValueError:
            return (0, 0, 0)
    return (0, 0, 0)


# === Region-Modell ===========================================================
@dataclass(frozen=True)
class TextRegion:
    """Eine Text-Region: name, fraktionale Box (x0,y0,x1,y1 in 0..1), Textfarbe, Schwelle."""
    name: str
    box: tuple[float, float, float, float]
    fg: tuple[int, int, int]
    min_ratio: float


@dataclass(frozen=True)
class ContrastFinding:
    """Messung einer Region: worst-/mean-Kontrast, Schwelle, ok-Flag, schlechteste BG-Farbe."""
    name: str
    fg: tuple[int, int, int]
    worst_ratio: float
    mean_ratio: float
    min_ratio: float
    worst_bg: tuple[int, int, int]

    @property
    def ok(self) -> bool:
        return self.worst_ratio >= self.min_ratio


def _clamp01(v: float) -> float:
    return 0.0 if v < 0.0 else (1.0 if v > 1.0 else v)


def _bottom_stack_regions(fmt: AdFormat, style: dict, content) -> list[tuple[str, tuple, str, float]]:
    """Bodenausgerichtete Layouts (template/photo-poster/object-hero/split-compare).

    Der Content-Block sitzt unten (justify flex-end) zwischen safe_top und
    safe_bottom, horizontal in den seitlichen Safe-Zonen. Stack von unten:
    CTA -> Subline -> Headline -> Eyebrow. Rueckgabe: (name, box, farb_rolle, schwelle).
    """
    x0 = fmt.safe_x_pct
    x1 = 1.0 - fmt.safe_x_pct
    by = 1.0 - fmt.safe_bottom_pct  # Unterkante des Content-Blocks
    top_guard = fmt.safe_top_pct
    accent_headline = bool(style.get("accent_as_block"))
    cta_minimal = str(style.get("chrome", "full")) == "minimal"
    return [
        ("eyebrow", (x0, _clamp01(by - 0.38), x1, _clamp01(by - 0.33)),
         "accent", WCAG_AA_NORMAL),
        ("headline", (x0, max(top_guard, by - 0.32), x1, _clamp01(by - 0.15)),
         "accent" if accent_headline else "ink", WCAG_AA_LARGE),
        ("subline", (x0, _clamp01(by - 0.14), x1, _clamp01(by - 0.065)),
         "ink_muted", WCAG_AA_NORMAL),
        ("cta", (x0, _clamp01(by - 0.055), x1, _clamp01(by)),
         "accent" if cta_minimal else "cta_on_pill", WCAG_AA_NORMAL),
    ]


def _stat_hero_regions(fmt: AdFormat, style: dict, content) -> list[tuple[str, tuple, str, float]]:
    """Stat-Hero: oben ausgerichtet (justify flex-start + padding-top)."""
    x0 = fmt.safe_x_pct
    x1 = 1.0 - fmt.safe_x_pct
    ty = fmt.safe_top_pct + 0.05
    try:
        hero_scale = float(style.get("hero_scale", 0.32))
    except (TypeError, ValueError):
        hero_scale = 0.32
    bottom_guard = 1.0 - fmt.safe_bottom_pct
    return [
        ("eyebrow", (x0, ty, x1, _clamp01(ty + 0.04)), "accent", WCAG_AA_NORMAL),
        ("hero", (x0, _clamp01(ty + 0.05), x1, _clamp01(ty + 0.05 + hero_scale)),
         "accent", WCAG_AA_LARGE),
        ("subline", (x0, _clamp01(ty + 0.06 + hero_scale), x1,
                     _clamp01(min(bottom_guard, ty + 0.12 + hero_scale))),
         "ink_muted", WCAG_AA_NORMAL),
        ("cta", (x0, _clamp01(ty + 0.13 + hero_scale), x1,
                 _clamp01(min(bottom_guard, ty + 0.19 + hero_scale))),
         "cta_on_pill", WCAG_AA_NORMAL),
    ]


def text_regions(fmt: AdFormat, brand: dict, *, layout: str = "template",
                 style: dict | None = None, content=None) -> list[TextRegion]:
    """Baut die zu pruefenden Text-Regionen aus Format + Layout + Brand-Tokens.

    Nur Regionen mit nicht-leerem Inhalt werden zurueckgegeben (fehlt z.B. die
    Subline, gibt es keine Subline-Region). Projektneutral — Farben aus brand.
    """
    style = style or {}
    ink = parse_color(brand.get("BRAND_INK", "#faf7f2"))
    ink_muted = parse_color(brand.get("BRAND_INK_MUTED", "#9a9ec0"))
    accent = parse_color(brand.get("BRAND_ACCENT", "#f25d3e"))
    # CTA-Pill: weisser Text auf Akzent-Pille (Template `.cta { color:#fff }`).
    role_color = {"ink": ink, "ink_muted": ink_muted, "accent": accent,
                  "cta_on_pill": (255, 255, 255)}

    if layout == "stat-hero":
        raw = _stat_hero_regions(fmt, style, content)
    else:
        # template / photo-poster / object-hero / split-compare -> Bodenstack.
        raw = _bottom_stack_regions(fmt, style, content)

    # Content-Vorhandensein pro Region pruefen (leere Felder -> keine Region).
    def _has(name: str) -> bool:
        if content is None:
            return True
        field = {"eyebrow": "eyebrow", "headline": "headline",
                 "subline": "subline", "cta": "cta"}.get(name)
        if name == "hero":
            # Hero nutzt hero_token, sonst Headline.
            return bool((style.get("hero_token") or getattr(content, "headline", "")))
        val = getattr(content, field, "") if field else ""
        return bool(str(val).strip())

    regions: list[TextRegion] = []
    for name, box, role, thr in raw:
        if not _has(name):
            continue
        # Degenerierte Box (nach Clamp) ueberspringen.
        if box[2] - box[0] < 0.02 or box[3] - box[1] < 0.01:
            continue
        regions.append(TextRegion(name=name, box=box, fg=role_color[role], min_ratio=thr))
    return regions


# === Pixel-Sampling ==========================================================
def _tile_means(img: Image.Image, box_px: tuple[int, int, int, int],
                grid: tuple[int, int]) -> list[tuple[int, int, int]]:
    """Mittelwert-Farbe je Raster-Kachel der Region (Image.BOX = flaechen-Mittel)."""
    x0, y0, x1, y1 = box_px
    if x1 <= x0 or y1 <= y0:
        return []
    cols = max(1, min(grid[0], x1 - x0))
    rows = max(1, min(grid[1], y1 - y0))
    crop = img.crop((x0, y0, x1, y1)).resize((cols, rows), resample=Image.BOX)
    return [crop.getpixel((cx, cy)) for cy in range(rows) for cx in range(cols)]


def measure_region(img: Image.Image, region: TextRegion,
                   grid: tuple[int, int] = DEFAULT_GRID) -> ContrastFinding:
    """Misst worst-/mean-Kontrast der Textfarbe gegen die BG-Kacheln der Region."""
    w, h = img.size
    x0, y0, x1, y1 = region.box
    box_px = (int(round(x0 * w)), int(round(y0 * h)),
              int(round(x1 * w)), int(round(y1 * h)))
    means = _tile_means(img, box_px, grid)
    if not means:
        # Keine Pixel -> neutral (kein Warn), max. Ratio.
        return ContrastFinding(region.name, region.fg, 21.0, 21.0,
                               region.min_ratio, region.fg)
    ratios = [(contrast_ratio(region.fg, m), m) for m in means]
    worst_ratio, worst_bg = min(ratios, key=lambda t: t[0])
    mean_ratio = sum(r for r, _ in ratios) / len(ratios)
    return ContrastFinding(region.name, region.fg, worst_ratio, mean_ratio,
                           region.min_ratio, worst_bg)


def _load_image(img_or_path) -> Image.Image:
    if isinstance(img_or_path, Image.Image):
        return img_or_path.convert("RGB")
    return Image.open(str(img_or_path)).convert("RGB")


def check_contrast(img_or_path, fmt: AdFormat, brand: dict, *,
                   layout: str = "template", style: dict | None = None,
                   content=None, grid: tuple[int, int] = DEFAULT_GRID) -> list[ContrastFinding]:
    """Misst alle Text-Regionen eines gerenderten Creatives. Rein informativ.

    `img_or_path` = PIL.Image ODER Pfad zum gerenderten PNG. `fmt` bestimmt die
    Safe-Zone-Geometrie, `layout`/`style`/`content` die Region-Positionen +
    Textfarben. Gibt ein ContrastFinding je Region zurueck (ok-Flag inklusive).
    """
    img = _load_image(img_or_path)
    regions = text_regions(fmt, brand, layout=layout, style=style, content=content)
    return [measure_region(img, r, grid) for r in regions]


def contrast_warnings(img_or_path, fmt: AdFormat, brand: dict, *,
                      layout: str = "template", style: dict | None = None,
                      content=None, grid: tuple[int, int] = DEFAULT_GRID) -> list[str]:
    """Warn-Validator (analog layout_warnings): eine Warnung je unterschrittener Region.

    KEINE Sperre — Mensch-im-Loop. Haelt jede Region ihre WCAG-AA-Schwelle ein,
    ist die Liste leer. Reine Warnungen mit Region + gemessenem Wert + Schwelle.
    """
    out: list[str] = []
    for f in check_contrast(img_or_path, fmt, brand, layout=layout, style=style,
                            content=content, grid=grid):
        if not f.ok:
            hexbg = "#%02x%02x%02x" % f.worst_bg
            hexfg = "#%02x%02x%02x" % f.fg
            out.append(
                f"Kontrast-Warnung ({f.name}): Textfarbe {hexfg} erreicht nur "
                f"{f.worst_ratio:.2f}:1 gegen den schlechtesten lokalen Hintergrund "
                f"{hexbg} (WCAG-AA-Ziel {f.min_ratio:.1f}:1). Text schlecht lesbar — "
                "Scrim/Text-Panel verstaerken oder Textfarbe/Position anpassen."
            )
    return out


def recommend_contrast_fix(findings: list[ContrastFinding], *, has_bg_image: bool,
                           layout: str = "template") -> list[str]:
    """Should (SKILL-074): konkrete Fix-Empfehlung bei Foto-BG + geringem Kontrast.

    Nur wenn tatsaechlich Regionen unterschreiten. Bei Foto-Hintergrund ist der
    gerichtete Scrim (photo-poster) bzw. ein Text-Panel der wirksamste Hebel;
    ohne Foto ist Textfarbe/Theme der Hebel. Reine Empfehlung, keine Aktion.
    """
    failing = [f for f in findings if not f.ok]
    if not failing:
        return []
    names = ", ".join(f.name for f in failing)
    if has_bg_image:
        base = (
            f"Empfehlung (Foto-BG): {names} liegt unter WCAG-AA. Den gerichteten "
            "Scrim hinter dem Text verstaerken (dunkleres/hoeheres Overlay) oder ein "
            "Text-Panel/abgesetzten Balken hinter der Headline setzen."
        )
        if layout != "photo-poster":
            base += " '--layout photo-poster' nutzt bereits einen gerichteten Scrim."
        return [base]
    return [
        f"Empfehlung: {names} liegt unter WCAG-AA (kein Foto-BG). Textfarbe/Theme "
        "kontrastreicher waehlen (z.B. --theme light-cream bei dunklem Text) oder "
        "Akzent nur fuer grosse Elemente nutzen."
    ]


# === CLI =====================================================================
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="creative-studio Lesbarkeits-/Kontrast-Check (SKILL-074)")
    ap.add_argument("image", help="Pfad zum gerenderten PNG")
    ap.add_argument("--format", default="feed_4x5", help="AdFormat-Key (Safe-Zone-Geometrie)")
    ap.add_argument("--layout", default="template",
                    help="Layout-Archetyp (template/photo-poster/object-hero/stat-hero/split-compare)")
    ap.add_argument("--ink", default="#faf7f2", help="Textfarbe Headline (BRAND_INK)")
    ap.add_argument("--ink-muted", default="#9a9ec0", help="Textfarbe Subline (BRAND_INK_MUTED)")
    ap.add_argument("--accent", default="#f25d3e", help="Akzentfarbe (Eyebrow/CTA-Link)")
    ap.add_argument("--accent-as-block", action="store_true", help="Headline in Akzentfarbe")
    ap.add_argument("--chrome", default="full", choices=["full", "minimal"])
    ap.add_argument("--has-bg-image", action="store_true", help="Foto-BG (fuer Fix-Empfehlung)")
    args = ap.parse_args(argv)

    fmt = get_format(args.format)
    brand = {"BRAND_INK": args.ink, "BRAND_INK_MUTED": args.ink_muted,
             "BRAND_ACCENT": args.accent}
    style = {"accent_as_block": args.accent_as_block, "chrome": args.chrome}
    findings = check_contrast(args.image, fmt, brand, layout=args.layout, style=style)
    for f in findings:
        flag = "OK " if f.ok else "LOW"
        print(f"[{flag}] {f.name}: worst {f.worst_ratio:.2f}:1 "
              f"(mean {f.mean_ratio:.2f}:1, Ziel {f.min_ratio:.1f}:1)")
    warns = contrast_warnings(args.image, fmt, brand, layout=args.layout, style=style)
    for w in warns:
        print(f"[WARN] {w}")
    for rec in recommend_contrast_fix(findings, has_bg_image=args.has_bg_image, layout=args.layout):
        print(f"[TIPP] {rec}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
