#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lp_layout_lint.py: Playwright-Layout-Linter fuer Landingpages (creative-studio).

Faengt die Klasse „gequetscht / tote Leere"-Layoutfehler, die an der Referenz-LP
warteliste-02 real aufgetreten sind (siehe SKILL.md §16i, Ticket SKILL-107):

  1. overflow            Seite scrollt horizontal (scrollWidth > clientWidth) -> FAIL
  2. tote-spalte         2-Spalten-Layout, kurze Spalte oben geklebt (align-items:start),
                         Hoehendifferenz der Spalten > 30 % -> FAIL (tote Leere unter der
                         kurzen Spalte).
  3. kacheln-ungleich    Karten-Grid, Kacheln in einer Zeile unterschiedlich hoch -> FAIL.
                         Kacheln MUESSEN gleich gross sein (equal-height); Loesung bei
                         ungleichem Inhalt = Text angleichen, NICHT ungleich stehen lassen.
  4. karten-leere        Gleich hohe Kacheln, aber eine hat unten tote Flaeche > 22 %
                         der Kartenhoehe -> WARN (Text der Kacheln angleichen).
  5. mobil-bottom-space  Auf schmaler Breite (<= 480) klebt das letzte Element einer
                         `.band` mit < 24 px an der Sektions-Unterkante -> WARN.
  6. testimonial-slider  > 3 Testimonials in statischem Layout (kein Slider-Markup) -> WARN
                         (ab 4 Testimonials Slider/Carousel: scroll-snap + Pfeile/Dots).
  7. enge-abstaende      Aufeinanderfolgende Bloecke in einer grosszuegig gepolsterten
                         `.band`, deren fester margin-top winzig (< 20 px) ist -> WARN
                         (Skala vermutlich nicht genutzt; heuristisch, non-gating).

Das Skript rendert die LP auf mehreren Breiten (Default 1900 / 1440 / 390) und
prueft heuristisch im Browser (getComputedStyle + Geometrie). Es ist robust: fehlende
Elemente fuehren nie zum Crash, jede Heuristik ist in try/catch gekapselt.

Exit-Code = Gate:
  0  keine FAIL-Findings (WARN erlaubt, ausser mit --strict)
  1  mindestens ein FAIL (bzw. mit --strict: mindestens ein WARN)
  2  Ausfuehrungsfehler (z.B. Seite nicht ladbar)

Alle Schwellen stehen als Konstanten oben im File und lassen sich anpassen.

--------------------------------------------------------------------------------
Aufruf (Windows: `python`, nicht `python3`):

    # Live-LP pruefen
    python tests/lp_layout_lint.py --url https://warteliste-02.jakobsebov.de/

    # Lokale Datei (file://) pruefen: Pfad ODER file://-URL beides ok
    python tests/lp_layout_lint.py --url landing/warteliste-02/index.html

    # Eigene Breiten, WARN ebenfalls als Gate werten, sichtbarer Browser
    python tests/lp_layout_lint.py --url <url> --widths 1440 390 --strict --headed

Rueckgabe: Klartext-Findings je Breite + Zusammenfassung, Exit-Code als Gate.
--------------------------------------------------------------------------------
"""
from __future__ import annotations

import argparse
import pathlib
import sys

# ============================================================================
# SCHWELLEN / KONSTANTEN  (hier zentral justieren)
# ============================================================================
DEFAULT_WIDTHS = [1900, 1440, 390]   # Desktop-gross / Desktop / Mobile
VIEWPORT_HEIGHT = 1200               # Renderhoehe (nur Startwert; Seite scrollt)

OVERFLOW_TOLERANCE_PX = 1            # scrollWidth darf clientWidth um max. 1px ueberschreiten
COL_HEIGHT_DIFF_RATIO = 0.30         # tote-spalte: Hoehendiff > 30 % der groesseren Spalte
COL_MIN_HEIGHT_PX = 140              # tote-spalte: groessere Spalte muss substanziell sein
COL_MIN_ABS_DIFF_PX = 120            # ... UND die absolute tote Leere muss spuerbar sein
                                     #     (filtert Icon+Text-Reihen wie Checkbox/Listen-Bullet raus)

# Karten-Grid: Kacheln MUESSEN gleich gross sein (equal-height). Zwei Findings:
#  (a) Kacheln in derselben Grid-Zeile unterschiedlich hoch -> FAIL ("nicht gleich gross")
#  (b) Kacheln gleich hoch, aber eine hat unten tote Flaeche -> WARN ("Text angleichen")
CARD_GRID_MIN_CARDS = 3              # ab so vielen gleichartigen Kacheln = Karten-Grid
CARD_ROW_DIFF_RATIO = 0.12          # Hoehendiff in einer Zeile > 12 % -> nicht gleich gross
CARD_ROW_DIFF_MIN_PX = 16           # ... und absolut spuerbar
CARD_DEAD_SPACE_RATIO = 0.22        # tote Flaeche unten > 22 % der Kartenhoehe -> Text angleichen
CARD_MIN_HEIGHT_PX = 80             # Karten unter dieser Hoehe ignorieren (Rauschen)
ROW_TOP_TOLERANCE_PX = 6            # Kacheln mit ~gleicher Oberkante gelten als eine Zeile

# enge-abstaende (heuristisch, non-gating)
TIGHT_MARGIN_PX = 20                 # fester margin-top < 20px gilt als „winzig"
SECTION_PADDING_PX = 60              # ... waehrend die Sektion mehr als 60px Polsterung hat

# mobil-bottom-space: letztes Element einer .band klebt unten an der Sektionskante
MOBILE_WIDTH_MAX = 480               # Check nur auf schmaler Breite
MOBILE_BOTTOM_MIN_PX = 24            # Mindestabstand letztes Element -> Sektions-Unterkante

# testimonial-slider: ab > 3 Testimonials gehoert ein Slider her (nicht statisches Grid)
TESTIMONIAL_SLIDER_MIN = 3           # ab 4 Testimonials (> 3) Slider-Pflicht

# align-items-Werte, die eine kurze Spalte NICHT oben ankleben (kein Finding):
SAFE_ALIGN_ITEMS = {"center", "stretch", "normal", "baseline"}

# Severity-Konstanten
FAIL = "FAIL"
WARN = "WARN"

# ============================================================================
# In-Browser-Heuristik: eine Arrow-Function (cfg) => [...findings].
# Laeuft via page.evaluate im Seitenkontext, gibt Liste {check,severity,msg}.
# Nie werfend: jede Heuristik in try/catch, fehlende Elemente sind kein Crash.
# ============================================================================
_LINT_JS = r"""
(cfg) => {
  const findings = [];
  const add = (check, severity, msg) => findings.push({ check, severity, msg });
  const label = (el) => {
    try {
      let s = el.tagName ? el.tagName.toLowerCase() : "?";
      if (el.id) s += "#" + el.id;
      if (el.classList && el.classList.length) s += "." + Array.from(el.classList).join(".");
      return s;
    } catch (e) { return "?"; }
  };
  const isVisible = (el) => {
    try {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && cs.display !== "none" && cs.visibility !== "hidden";
    } catch (e) { return false; }
  };
  const elementChildren = (el) => {
    try { return Array.from(el.children).filter((c) => c.nodeType === 1 && isVisible(c)); }
    catch (e) { return []; }
  };

  // ---- 1) OVERFLOW: horizontaler Scroll ----
  try {
    const de = document.documentElement;
    const over = de.scrollWidth - de.clientWidth;
    if (over > cfg.OVERFLOW_TOLERANCE_PX) {
      add("overflow", "FAIL",
        "Horizontaler Scroll: scrollWidth " + de.scrollWidth + " > clientWidth " + de.clientWidth +
        " (Ueberhang " + over + "px). Ein Element ist breiter als der Viewport.");
    }
  } catch (e) {}

  const all = Array.from(document.querySelectorAll("*"));

  // ---- 2) TOTE-SPALTE: 2-spaltiges Grid / Flex-Row mit ungleicher Spaltenhoehe ----
  for (const el of all) {
    try {
      if (!isVisible(el)) continue;
      const cs = getComputedStyle(el);
      const kids = elementChildren(el);
      if (kids.length !== 2) continue;               // nur echte Zweispalter

      let isTwoCol = false;
      const r0 = kids[0].getBoundingClientRect(), r1 = kids[1].getBoundingClientRect();
      const sideBySide = Math.abs(r0.left - r1.left) > 8;      // nebeneinander, nicht gestapelt
      if (cs.display === "grid") {
        const tracks = (cs.gridTemplateColumns || "").trim().split(/\s+/).filter(Boolean);
        if (tracks.length === 2 && sideBySide) isTwoCol = true;
      } else if (cs.display === "flex" && cs.flexDirection.startsWith("row")) {
        if (sideBySide) isTwoCol = true;
      }
      if (!isTwoCol) continue;

      const big = Math.max(r0.height, r1.height), small = Math.min(r0.height, r1.height);
      if (big < cfg.COL_MIN_HEIGHT_PX) continue;          // Spalten zu klein -> kein Layout-Zweispalter
      if ((big - small) < cfg.COL_MIN_ABS_DIFF_PX) continue;  // tote Leere absolut vernachlaessigbar
      const diff = (big - small) / big;
      const align = (cs.alignItems || "normal").trim();
      if (diff > cfg.COL_HEIGHT_DIFF_RATIO && !cfg.SAFE_ALIGN_ITEMS.includes(align)) {
        add("tote-spalte", "FAIL",
          label(el) + ": Zweispalter mit Hoehendiff " + Math.round(diff * 100) +
          "% (Spalten " + Math.round(small) + "px vs " + Math.round(big) + "px), align-items:" +
          align + ". Kurze Spalte klebt oben -> tote Leere darunter. -> align-items:center " +
          "(oder Inhalte auf aehnliche Hoehe bringen).");
      }
    } catch (e) {}
  }

  // ---- 3) KARTEN-GRID: Kacheln muessen gleich gross sein (equal-height) ----
  // (a) Kacheln in derselben Zeile unterschiedlich hoch -> FAIL ("nicht gleich gross")
  // (b) Kacheln gleich hoch, aber eine hat unten tote Flaeche -> WARN ("Text angleichen")
  const cardSig = (k) => {
    try {
      const cls = (k.classList && k.classList.length) ? k.classList[0] : "";
      return (k.tagName || "?").toLowerCase() + "." + cls;
    } catch (e) { return "?"; }
  };
  for (const el of all) {
    try {
      if (!isVisible(el)) continue;
      const cs = getComputedStyle(el);
      if (cs.display !== "grid") continue;
      const kids = elementChildren(el);
      if (kids.length < cfg.CARD_GRID_MIN_CARDS) continue;   // erst ab N gleichartigen Kacheln
      // Dominante Signatur bestimmen -> nur uniforme Karten-Grids, keine Layout-Grids:
      const counts = {};
      for (const k of kids) { const s = cardSig(k); counts[s] = (counts[s] || 0) + 1; }
      let domSig = null, domN = 0;
      for (const s in counts) { if (counts[s] > domN) { domN = counts[s]; domSig = s; } }
      if (domN < cfg.CARD_GRID_MIN_CARDS) continue;          // keine >=N gleichartigen Kacheln
      const cards = kids.filter((k) => cardSig(k) === domSig);

      // In Zeilen gruppieren (gleiche Oberkante = eine Zeile):
      const rows = [];
      for (const card of cards) {
        const top = card.getBoundingClientRect().top;
        let row = rows.find((r) => Math.abs(r.top - top) <= cfg.ROW_TOP_TOLERANCE_PX);
        if (!row) { row = { top: top, items: [] }; rows.push(row); }
        row.items.push(card);
      }

      for (const row of rows) {
        if (row.items.length < 2) continue;
        const hs = row.items.map((c) => c.getBoundingClientRect().height);
        const maxH = Math.max.apply(null, hs), minH = Math.min.apply(null, hs);
        if (maxH < cfg.CARD_MIN_HEIGHT_PX) continue;
        const rowUneven = (maxH - minH) / maxH > cfg.CARD_ROW_DIFF_RATIO
                          && (maxH - minH) > cfg.CARD_ROW_DIFF_MIN_PX;
        if (rowUneven) {
          add("kacheln-ungleich", "FAIL",
            label(el) + ": Kacheln in einer Zeile unterschiedlich hoch (" + Math.round(minH) +
            "px vs " + Math.round(maxH) + "px). Karten-Grid muss equal-height sein (align-items:stretch) " +
            "-> Kacheln gleich gross machen (Content/Text angleichen), nicht ungleich stehen lassen.");
          continue;   // ungleiche Zeile: WARN-Deadspace waere doppeltes Rauschen
        }
        // Zeile ist equal-height: pro Karte tote Flaeche unten pruefen (Text angleichen):
        for (const card of row.items) {
          const cr = card.getBoundingClientRect();
          const padBottom = parseFloat(getComputedStyle(card).paddingBottom) || 0;
          const inner = elementChildren(card);
          if (!inner.length) continue;
          let contentBottom = cr.top;
          for (const c of inner) {
            const rb = c.getBoundingClientRect().bottom;
            if (rb > contentBottom) contentBottom = rb;
          }
          const dead = (cr.bottom - padBottom) - contentBottom;
          if (cr.height >= cfg.CARD_MIN_HEIGHT_PX && dead / cr.height > cfg.CARD_DEAD_SPACE_RATIO) {
            add("karten-leere", "WARN",
              label(card) + " (in " + label(el) + "): " + Math.round(dead) + "px tote Flaeche unten (" +
              Math.round((dead / cr.height) * 100) + "% der Kartenhoehe " + Math.round(cr.height) +
              "px). Equal-Height-Karte mit zu wenig Text -> Text der Kacheln aneinander angleichen.");
          }
        }
      }
    } catch (e) {}
  }

  // ---- 3b) MOBIL-BOTTOM-SPACE: letztes Element einer .band klebt unten (nur schmal) ----
  if (cfg.WIDTH <= cfg.MOBILE_WIDTH_MAX) {
    for (const el of all) {
      try {
        if (!isVisible(el)) continue;
        if (!(el.classList && el.classList.contains("band"))) continue;
        const br = el.getBoundingClientRect();
        // letztes sichtbares, im Fluss liegendes Nachkommen-Element:
        let lastBottom = null, lastEl = null;
        for (const d of el.querySelectorAll("*")) {
          if (!isVisible(d)) continue;
          const dcs = getComputedStyle(d);
          if (dcs.position === "absolute" || dcs.position === "fixed") continue;  // Deko ignorieren
          const rb = d.getBoundingClientRect().bottom;
          if (rb <= br.bottom + 1 && (lastBottom === null || rb > lastBottom)) {
            lastBottom = rb; lastEl = d;
          }
        }
        if (lastBottom === null) continue;
        const gap = br.bottom - lastBottom;   // Abstand letztes Element -> Sektions-Unterkante
        if (gap < cfg.MOBILE_BOTTOM_MIN_PX) {
          add("mobil-bottom-space", "WARN",
            label(el) + ": auf " + cfg.WIDTH + "px klebt das letzte Element (" + label(lastEl) +
            ") mit nur " + Math.round(gap) + "px an der Sektions-Unterkante (< " +
            cfg.MOBILE_BOTTOM_MIN_PX + "px). Untere Sektions-Polsterung (--space-section) fehlt/zu klein.");
        }
      } catch (e) {}
    }
  }

  // ---- 3c) TESTIMONIAL-SLIDER: > 3 Testimonials gehoeren in einen Slider ----
  try {
    const containers = Array.from(document.querySelectorAll(
      "[data-testimonials], .testimonials, #stimmen, #testimonials"));
    for (const c of containers) {
      if (!isVisible(c)) continue;
      // Testimonial-Items zaehlen: markierte bevorzugt, sonst Karten-Kinder:
      let items = Array.from(c.querySelectorAll("[data-testimonial], .testimonial, .t-card"))
                    .filter(isVisible);
      if (!items.length) items = elementChildren(c);
      if (items.length <= cfg.TESTIMONIAL_SLIDER_MIN) continue;

      // Slider-Markup? scroll-snap-Container / role=region mit overflow-x auto|scroll.
      const isSlider = (node) => {
        try {
          if (!node) return false;
          const ncs = getComputedStyle(node);
          const snap = (ncs.scrollSnapType || "none") !== "none";
          const ox = ncs.overflowX;
          const scrollable = ox === "auto" || ox === "scroll";
          const marked = (node.matches && (node.matches("[data-slider], .slider, .t-slider, .t-track")))
                         || node.getAttribute && node.getAttribute("role") === "region";
          return (snap && scrollable) || (marked && scrollable) || (marked && snap);
        } catch (e) { return false; }
      };
      let slider = isSlider(c);
      if (!slider) {
        for (const d of c.querySelectorAll("*")) { if (isSlider(d)) { slider = true; break; } }
      }
      if (!slider) {
        add("testimonial-slider", "WARN",
          label(c) + ": " + items.length + " Testimonials in statischem Layout. Ab 4 Testimonials " +
          "(> 3) einen Slider/Carousel nutzen (scroll-snap horizontal + Pfeile/Dots, mobil 1, " +
          "Desktop 2-3 pro View).");
      }
    }
  } catch (e) {}

  // ---- 4) ENGE-ABSTAENDE: winzige feste Bloeckabstaende in grosszuegiger .band (heuristisch) ----
  for (const el of all) {
    try {
      if (!isVisible(el)) continue;
      if (!(el.classList && el.classList.contains("band"))) continue;
      const bcs = getComputedStyle(el);
      const pad = Math.max(parseFloat(bcs.paddingTop) || 0, parseFloat(bcs.paddingBottom) || 0);
      if (pad <= cfg.SECTION_PADDING_PX) continue;
      // Direkte Inhalts-Bloecke: .band > .wrap > * (falls .wrap vorhanden), sonst .band > *
      const host = el.querySelector(":scope > .wrap") || el;
      const blocks = elementChildren(host);
      for (let i = 1; i < blocks.length; i++) {
        const prev = blocks[i - 1], cur = blocks[i];
        // eyebrow -> Heading darf eng bleiben (gehoert zusammen): ausnehmen
        const prevIsEyebrow = prev.classList && prev.classList.contains("eyebrow");
        const curIsHeading = /^H[1-3]$/.test(cur.tagName || "");
        if (prevIsEyebrow && curIsHeading) continue;
        const mt = parseFloat(getComputedStyle(cur).marginTop) || 0;
        if (mt > 0 && mt < cfg.TIGHT_MARGIN_PX) {
          add("enge-abstaende", "WARN",
            label(cur) + " in " + label(el) + ": margin-top " + Math.round(mt) +
            "px winzig, waehrend die Sektion " + Math.round(pad) + "px Polsterung hat. " +
            "Vermutlich fester px-Abstand statt --space-*-Skala.");
        }
      }
    } catch (e) {}
  }

  return findings;
}
"""


def _path_to_uri(target: str) -> str:
    """Akzeptiert http(s)-/file://-URL oder lokalen Pfad und liefert eine ladbare URL."""
    if target.startswith(("http://", "https://", "file://")):
        return target
    return pathlib.Path(target).expanduser().resolve().as_uri()


def run_lint(url: str, widths, headed: bool = False, verbose: bool = True) -> dict:
    """Rendert die LP auf allen Breiten, sammelt Findings, aggregiert FAIL/WARN.

    Returns: {'FAIL': int, 'WARN': int} aggregiert ueber alle Breiten.
    """
    from playwright.sync_api import sync_playwright

    base_cfg = {
        "OVERFLOW_TOLERANCE_PX": OVERFLOW_TOLERANCE_PX,
        "COL_HEIGHT_DIFF_RATIO": COL_HEIGHT_DIFF_RATIO,
        "COL_MIN_HEIGHT_PX": COL_MIN_HEIGHT_PX,
        "COL_MIN_ABS_DIFF_PX": COL_MIN_ABS_DIFF_PX,
        "CARD_GRID_MIN_CARDS": CARD_GRID_MIN_CARDS,
        "CARD_ROW_DIFF_RATIO": CARD_ROW_DIFF_RATIO,
        "CARD_ROW_DIFF_MIN_PX": CARD_ROW_DIFF_MIN_PX,
        "CARD_DEAD_SPACE_RATIO": CARD_DEAD_SPACE_RATIO,
        "CARD_MIN_HEIGHT_PX": CARD_MIN_HEIGHT_PX,
        "ROW_TOP_TOLERANCE_PX": ROW_TOP_TOLERANCE_PX,
        "TIGHT_MARGIN_PX": TIGHT_MARGIN_PX,
        "SECTION_PADDING_PX": SECTION_PADDING_PX,
        "MOBILE_WIDTH_MAX": MOBILE_WIDTH_MAX,
        "MOBILE_BOTTOM_MIN_PX": MOBILE_BOTTOM_MIN_PX,
        "TESTIMONIAL_SLIDER_MIN": TESTIMONIAL_SLIDER_MIN,
        "SAFE_ALIGN_ITEMS": sorted(SAFE_ALIGN_ITEMS),
    }
    totals = {FAIL: 0, WARN: 0}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        try:
            for w in widths:
                page = browser.new_page(viewport={"width": int(w), "height": VIEWPORT_HEIGHT},
                                        device_scale_factor=1)
                try:
                    page.goto(url, wait_until="networkidle", timeout=30000)
                except Exception:
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(400)  # Fonts/Layout settlen lassen
                cfg = dict(base_cfg, WIDTH=int(w))  # aktuelle Breite fuer breitenabhaengige Checks
                try:
                    findings = page.evaluate(_LINT_JS, cfg) or []
                except Exception as exc:  # Heuristik darf nie den Lauf killen
                    findings = []
                    print(f"  [warn] Heuristik-Evaluate fehlgeschlagen @ {w}px: {exc}")

                fails = [f for f in findings if f.get("severity") == FAIL]
                warns = [f for f in findings if f.get("severity") == WARN]
                totals[FAIL] += len(fails)
                totals[WARN] += len(warns)

                if verbose:
                    tag = "OK  " if not findings else ("FAIL" if fails else "WARN")
                    print(f"\n[{tag}] Breite {w}px  ({len(fails)} FAIL, {len(warns)} WARN)")
                    for f in fails + warns:
                        print(f"    {f['severity']:4} {f['check']:14} {f['msg']}")
                page.close()
        finally:
            browser.close()
    return totals


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Playwright-Layout-Linter fuer Landingpages (creative-studio).")
    ap.add_argument("--url", required=True,
                    help="LP-URL: http(s)://, file:// oder lokaler Pfad zur index.html")
    ap.add_argument("--widths", type=int, nargs="+", default=DEFAULT_WIDTHS,
                    help=f"Render-Breiten in px (Default: {DEFAULT_WIDTHS})")
    ap.add_argument("--strict", action="store_true",
                    help="WARN ebenfalls als Gate werten (Exit 1 auch bei WARN).")
    ap.add_argument("--headed", action="store_true",
                    help="Browser sichtbar starten (Debug).")
    args = ap.parse_args(argv)

    url = _path_to_uri(args.url)
    print(f"LP-Layout-Linter -> {url}")
    print(f"Breiten: {args.widths}  |  Gate: {'FAIL+WARN' if args.strict else 'nur FAIL'}")

    try:
        totals = run_lint(url, args.widths, headed=args.headed)
    except Exception as exc:
        print(f"\nAUSFUEHRUNGSFEHLER: {exc}")
        return 2

    print("\n" + "=" * 70)
    print(f"Summe: {totals[FAIL]} FAIL, {totals[WARN]} WARN (ueber {len(args.widths)} Breiten)")
    gate_hit = totals[FAIL] > 0 or (args.strict and totals[WARN] > 0)
    if gate_hit:
        print("GATE: ROT (1): Layout-Fehler gefunden.")
        return 1
    print("GATE: GRUEN (0): keine blockierenden Layout-Fehler.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
