#!/usr/bin/env bash
# screenshot_slides.sh — Visual-Review-Pass für reveal.js Decks
#
# Macht headless-Chromium-Screenshots pro Slide, mit allen Fragments
# sichtbar (Override via Temp-HTML-Kopie). Output ist eine PNG pro Slide
# unter <output_dir>/slide_NN.png.
#
# Usage:
#   tools/screenshot_slides.sh <presi.html> <n_slides> <output_dir>
#
# Beispiel:
#   tools/screenshot_slides.sh onboarding/team.html 16 /tmp/shots
#
# Env-Override:
#   CHROME=<pfad>  Chromium-Binary (Default: Windows Chrome, Fallback chromium/google-chrome)
#
# Lessons (BeyerImmo 2026-05-27):
#   - Fragments brauchen CSS-Override sonst sieht man nur Slide-Initialzustand
#   - Pro Slide eigenes --user-data-dir, sonst lockt sich Chromium gegenseitig
#   - --virtual-time-budget=8000 reicht für reveal.js + Fonts + Mermaid

set -euo pipefail

if [ $# -lt 3 ]; then
  echo "Usage: $0 <presi.html> <n_slides> <output_dir>" >&2
  echo "  presi.html: Pfad zur Reveal-HTML (absolut oder relativ)" >&2
  echo "  n_slides:   Anzahl Top-Level-Slides (0-basiert: 0 bis n-1)" >&2
  echo "  output_dir: Wo die PNGs hinkommen (wird angelegt)" >&2
  exit 2
fi

PRESI="$1"
N_SLIDES="$2"
OUTPUT_DIR="$3"

# Chromium auflösen: $CHROME-Env zuerst, dann Windows-Pfad, dann PATH
CHROME="${CHROME:-}"
if [ -z "$CHROME" ]; then
  for candidate in \
    "/c/Program Files/Google/Chrome/Application/chrome.exe" \
    "C:/Program Files/Google/Chrome/Application/chrome.exe" \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "$(command -v chromium 2>/dev/null || true)" \
    "$(command -v google-chrome 2>/dev/null || true)" \
    "$(command -v chrome 2>/dev/null || true)"; do
    if [ -n "$candidate" ] && [ -x "$candidate" ]; then
      CHROME="$candidate"
      break
    fi
  done
fi
if [ -z "$CHROME" ] || [ ! -x "$CHROME" ]; then
  echo "ERROR: Chromium-Binary nicht gefunden. Setze \$CHROME oder installiere Chrome." >&2
  exit 3
fi

# Presi-File existiert?
if [ ! -f "$PRESI" ]; then
  echo "ERROR: $PRESI nicht gefunden." >&2
  exit 4
fi

# Absoluten Pfad ermitteln (für file:// URL)
PRESI_ABS="$(realpath "$PRESI" 2>/dev/null || readlink -f "$PRESI" 2>/dev/null || echo "$PRESI")"

# Output-Dir + Temp-HTML
mkdir -p "$OUTPUT_DIR"
TMP_HTML="$(mktemp --suffix=.html 2>/dev/null || mktemp -t visible.html)"
trap 'rm -f "$TMP_HTML"' EXIT

# CSS-Override injizieren: Fragments sofort sichtbar
sed 's|</style>|.reveal .fragment{opacity:1!important;visibility:visible!important;}\n</style>|' \
  "$PRESI_ABS" > "$TMP_HTML"

# URL für Chromium (Windows: file:///C:/..., Unix: file:///path)
case "$TMP_HTML" in
  /c/*) URL="file:///C:${TMP_HTML#/c}" ;;
  *)    URL="file://$TMP_HTML" ;;
esac

echo "Chromium: $CHROME"
echo "Source:   $PRESI_ABS"
echo "Slides:   $N_SLIDES"
echo "Output:   $OUTPUT_DIR"
echo ""

# Pro Slide Screenshot
for n in $(seq 0 $((N_SLIDES - 1))); do
  nn=$(printf "%02d" "$n")
  out="$OUTPUT_DIR/slide_${nn}.png"
  userdir="$(mktemp -d -t chrome_userdata_XXXXXX)"
  echo "  Slide $nn → $out"
  "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --user-data-dir="$userdir" \
    --window-size=1920,1080 \
    --screenshot="$out" \
    --virtual-time-budget=8000 \
    "${URL}#/${n}" > /dev/null 2>&1
  rm -rf "$userdir" 2>/dev/null || true
done

echo ""
echo "✓ $N_SLIDES Screenshots in $OUTPUT_DIR/"
echo "  Nächster Schritt: mit Read-Tool pro Datei visuell prüfen."
