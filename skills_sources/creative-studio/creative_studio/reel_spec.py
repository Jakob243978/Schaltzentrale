"""creative-studio — Reel-Spec (JSON) als Render-Input (SKILL-045).

Zentrale Eingabe fuer einen einzelnen Reel-Render: eine Reel-Spec (JSON)
beschreibt EIN Reel vollstaendig (Hook, Szenen/Segmente, Captions, optional
Voiceover/Musik, optional B-Roll, CTA, Brand-Tokens) und wird per `load_reel_spec`
in das `--props`-Objekt der Remotion-`AdReel`-Composition uebersetzt.

Skalierung = eine Composition + n Reel-Specs (`npx remotion render … --props`).
Diese Spec ist die Basis fuer Batch (SKILL-048) und der gemeinsame Eingang fuer
Captions (SKILL-043), Audio (SKILL-044) und B-Roll (SKILL-046).

Naming (variant_id + utm_content) kommt AUSSCHLIESSLICH aus specs.py (SKILL-024) —
KEIN Parallel-Schema hier (EARS-5).

Multi-Projekt (EARS-4): Brand + Inhalt kommen NUR aus der Spec — kein
hartkodierter Projektwert im Loader.

Reel-Spec-Schema (JSON):
    {
      "ad_id": "h1-immo",                  # Pflicht — Datei-/Naming-Stamm (SKILL-024)
      "framework": "pas",                  # optional — Hook-Framework-Key (Default "hook")
      "hook_index": 0,                     # optional — Hook-Index fuer variant_id
      "hook": "3 Stunden pro Woche zurueck — ohne neues Tool.",  # Pflicht — Headline/Hook
      "hook_accent": "ohne neues Tool",    # optional — accent-gefaerbter Headline-Teil
      "eyebrow": "MENTORING · WARTELISTE", # optional
      "subline": "...",                    # optional
      "cta": "Auf die Warteliste",         # optional
      "scenes": [                          # optional — Segmente (Text + Dauer in Sekunden)
        {"text": "...", "seconds": 3.0},
        ...
      ],
      "captions": [                        # optional — word-level Tokens (Whisper-Output)
        {"text": "3", "startMs": 0, "endMs": 350},
        ...
      ],
      "caption_style": "hormozi",          # optional — clean|karaoke|hormozi
      "voiceover": "voiceover.mp3",        # optional — VO-Audio-Ref (Pfad/URL)
      "music": "beat.mp3",                 # optional — Musik-Ref (Pfad/URL)
      "broll": [                           # optional — B-Roll-Clips (Ref + Dauer)
        {"src": "clip1.mp4", "seconds": 2.5},
        ...
      ],
      "content_type": "talking_head",     # optional — CONTENT_TYPE-Key (SKILL-042/056)
      "speaker": {                         # optional — Talking-Head-Sprecher-Layer (SKILL-056)
        "src": "speaker.mp4",              #   On-Camera-Sprech-Clip (Pflicht im talking_head)
        "objectPosition": "50% 30%"        #   optional — Reframe-Crop
      },
      "brand": {                           # Pflicht — Brand-Tokens
        "name": "JAKSE-Automations",
        "accent": "#f25d3e", "bg": "#0a0e27", "bgSoft": "#11163a",
        "ink": "#faf7f2", "inkMuted": "#9a9ec0",
        "highlight": "#f25d3e",            # optional — Caption-Keyword (Default: Brand-Akzent, SKILL-057)
        "captionFont": "Montserrat, sans-serif",  # optional — Caption-Font (SKILL-055/057)
        "captionBg": "pill",               # optional — pill|stroke (SKILL-055)
        "captionBgAlpha": 0.62,            # optional — Pill-Deckkraft 0..1 (SKILL-057)
        "font": "-apple-system, sans-serif"
      }
    }

CLI:
    python -m creative_studio.reel_spec --spec reel.json [--out props.json]
"""
from __future__ import annotations

import argparse
import json
import pathlib
from dataclasses import dataclass, field
from typing import Any

from .specs import make_utm_content, make_variant_id

FPS = 30

# SKILL-057: Reel-Theme-Default-Konstanten (benannte, ueberschreibbare Defaults —
# kein verstreutes Brand-Literal). Projektwerte kommen aus dem Brand-Block der
# Spec (bzw. branding.env: BRAND_HIGHLIGHT/BRAND_CAPTION_FONT/BRAND_CAPTION_BG_ALPHA).
# Default-Highlight bewusst KEIN festes Gelb: faellt auf den Brand-Akzent zurueck
# (Jakob-Vorgabe 2026-06-25 — Brand-Akzent statt #ffd400).
DEFAULT_ACCENT = "#f25d3e"
DEFAULT_CAPTION_FONT = (
    "Montserrat, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
)
DEFAULT_CAPTION_BG = "pill"
DEFAULT_CAPTION_BG_ALPHA = 0.62


class ReelSpecError(ValueError):
    """SKILL-045 EARS-2: klare Fehlermeldung bei ungueltiger/unvollstaendiger Spec."""


@dataclass
class CaptionTokenSpec:
    text: str
    startMs: int
    endMs: int
    # SKILL-066: explizit vom Redaktions-Pass (content.py, SKILL-061) gewaehltes
    # Keyword. Wird durchgereicht, damit Captions.tsx die INHALTLICH gewaehlte
    # Betonung nutzt statt der SKILL-055-Heuristik (laengstes/zahlhaltiges Token).
    keyword: bool = False

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "text": self.text,
            "startMs": self.startMs,
            "endMs": self.endMs,
        }
        # Nur setzen, wenn markiert — fehlt es, faellt Captions.tsx auf die
        # Heuristik zurueck (Bestand, EARS-2).
        if self.keyword:
            d["keyword"] = True
        return d


@dataclass
class SceneSpec:
    text: str
    seconds: float

    def to_dict(self) -> dict[str, Any]:
        return {"text": self.text, "seconds": self.seconds}


@dataclass
class BrollClipSpec:
    src: str
    seconds: float

    def to_dict(self) -> dict[str, Any]:
        return {"src": self.src, "seconds": self.seconds}


@dataclass
class SpeakerSpec:
    """SKILL-056: On-Camera-Sprech-Clip fuer den Talking-Head-Render."""

    src: str
    object_position: str = "50% 50%"

    def to_dict(self) -> dict[str, Any]:
        return {"src": self.src, "objectPosition": self.object_position}


@dataclass
class ReelSpec:
    """Validierte, in-memory Repraesentation einer Reel-Spec.

    Pflicht: ad_id, hook, brand. Alle uebrigen Layer (scenes/captions/voiceover/
    music/broll) sind optional (EARS-3) — das Reel rendert auch ohne sie.
    """

    ad_id: str
    hook: str
    brand: dict[str, Any]
    framework: str = "hook"
    hook_index: int | None = 0
    hook_accent: str = ""
    eyebrow: str = ""
    subline: str = ""
    cta: str = ""
    caption_style: str = "hormozi"
    scenes: list[SceneSpec] = field(default_factory=list)
    captions: list[CaptionTokenSpec] = field(default_factory=list)
    voiceover: str | None = None
    music: str | None = None
    broll: list[BrollClipSpec] = field(default_factory=list)
    # SKILL-056: Talking-Head-Felder (additiv, optional).
    content_type: str | None = None
    speaker: SpeakerSpec | None = None

    # --- abgeleitete Werte (Single-Source-Naming via SKILL-024) ---------------
    @property
    def variant_id(self) -> str:
        return make_variant_id(
            self.ad_id, self.hook, self.framework, "story_9x16",
            hook_index=self.hook_index,
        )

    @property
    def utm_content(self) -> str:
        return make_utm_content(self.variant_id)

    def duration_frames(self) -> int | None:
        """Dauer in Frames, falls aus der Spec berechenbar (sonst None -> Composition
        leitet sie aus Audio/Captions/Fallback ab, SKILL-044).

        Prioritaet: Summe der Szenen-Sekunden > Summe der B-Roll-Sekunden >
        letztes Caption-endMs.
        """
        if self.scenes:
            total = sum(max(0.0, s.seconds) for s in self.scenes)
            if total > 0:
                return int(round(total * FPS))
        if self.broll:
            total_b = sum(max(0.0, b.seconds) for b in self.broll)
            if total_b > 0:
                return int(round(total_b * FPS))
        if self.captions:
            last = max(c.endMs for c in self.captions)
            if last > 0:
                return int(round((last / 1000.0) * FPS))
        return None


def _require(data: dict[str, Any], key: str) -> Any:
    if key not in data or data[key] in (None, "", [], {}):
        raise ReelSpecError(
            f"Reel-Spec: Pflichtfeld '{key}' fehlt oder ist leer. "
            "Eine Spec ohne Pflichtfeld wuerde still ein leeres Reel rendern "
            "(Hard-Failure-Risiko)."
        )
    return data[key]


def parse_reel_spec(data: dict[str, Any]) -> ReelSpec:
    """SKILL-045: validiert ein Spec-Dict und baut eine ReelSpec.

    EARS-2: fehlt ein Pflichtfeld (ad_id/hook/brand), wird ReelSpecError geworfen
    — kein stilles leeres Reel.
    EARS-3: captions/broll/voiceover/music/scenes sind optional.
    """
    if not isinstance(data, dict):
        raise ReelSpecError("Reel-Spec muss ein JSON-Objekt (Mapping) sein.")

    ad_id = str(_require(data, "ad_id"))
    hook = str(_require(data, "hook"))
    brand = _require(data, "brand")
    if not isinstance(brand, dict):
        raise ReelSpecError("Reel-Spec: 'brand' muss ein Objekt mit Brand-Tokens sein.")
    if not (brand.get("name") or "").strip():
        raise ReelSpecError("Reel-Spec: 'brand.name' ist Pflicht (Brand-Token).")

    scenes = [
        SceneSpec(text=str(s.get("text", "")), seconds=float(s.get("seconds", 0)))
        for s in (data.get("scenes") or [])
    ]
    captions = [
        CaptionTokenSpec(
            text=str(c["text"]),
            startMs=int(c["startMs"]),
            endMs=int(c["endMs"]),
            # SKILL-066: optionales, vom Redaktions-Pass gesetztes Keyword.
            keyword=bool(c.get("keyword", False)),
        )
        for c in (data.get("captions") or [])
    ]
    broll = [
        BrollClipSpec(src=str(b.get("src", "")), seconds=float(b.get("seconds", 0)))
        for b in (data.get("broll") or [])
    ]

    hook_index = data.get("hook_index", 0)
    if hook_index is not None:
        hook_index = int(hook_index)

    # SKILL-056: optionaler Talking-Head-Sprecher-Layer.
    speaker_raw = data.get("speaker") or None
    speaker = None
    if speaker_raw:
        if not isinstance(speaker_raw, dict) or not str(speaker_raw.get("src", "")).strip():
            raise ReelSpecError(
                "Reel-Spec: 'speaker.src' (On-Camera-Sprech-Clip) ist Pflicht, "
                "wenn ein speaker-Block gesetzt ist."
            )
        speaker = SpeakerSpec(
            src=str(speaker_raw["src"]),
            object_position=str(speaker_raw.get("objectPosition", "50% 50%")),
        )

    return ReelSpec(
        ad_id=ad_id,
        hook=hook,
        brand=brand,
        framework=str(data.get("framework", "hook")),
        hook_index=hook_index,
        hook_accent=str(data.get("hook_accent", "")),
        eyebrow=str(data.get("eyebrow", "")),
        subline=str(data.get("subline", "")),
        cta=str(data.get("cta", "")),
        caption_style=str(data.get("caption_style", "hormozi")),
        scenes=scenes,
        captions=captions,
        voiceover=(data.get("voiceover") or None),
        music=(data.get("music") or None),
        broll=broll,
        content_type=(data.get("content_type") or None),
        speaker=speaker,
    )


def reel_spec_to_props(spec: ReelSpec) -> dict[str, Any]:
    """SKILL-045 EARS-1: uebersetzt eine ReelSpec in das `--props`-Objekt der
    Remotion-`AdReel`-Composition.

    Brand-Tokens werden auf die AdVideo/AdReel-Prop-Namen gemappt. Optionale Layer
    (captions/voiceover/music) landen als null/leer, wenn nicht gesetzt (EARS-3).
    Naming-Felder (variant_id/utm_content) kommen aus SKILL-024 — Single Source.
    """
    b = spec.brand
    accent = str(b.get("accent", DEFAULT_ACCENT))
    # SKILL-057: Caption-Font = brand.captionFont (override) -> brand.font -> Default
    # (Montserrat Bold). Der Font-Prop speist Title-Card UND Captions in AdReel.
    caption_font = str(b.get("captionFont") or b.get("font") or DEFAULT_CAPTION_FONT)
    props: dict[str, Any] = {
        # Title-Card / Hook
        "eyebrow": spec.eyebrow,
        "headline": spec.hook,
        "headlineAccent": spec.hook_accent,
        "subline": spec.subline,
        "cta": spec.cta,
        "brandName": str(b.get("name", "")),
        # Brand-Tokens (multi-projekt, alle aus der Spec)
        "accent": accent,
        "bg": str(b.get("bg", "#0a0e27")),
        "bgSoft": str(b.get("bgSoft", "#11163a")),
        "ink": str(b.get("ink", "#faf7f2")),
        "inkMuted": str(b.get("inkMuted", "#9a9ec0")),
        "font": caption_font,
        # B-Roll-Timeline (optional) — Clips als Hintergrund-Layer (SKILL-046-Vorber.)
        "broll": [b.to_dict() for b in spec.broll] or None,
        # SKILL-043: Caption-Track (optional)
        "captions": [c.to_dict() for c in spec.captions] or None,
        "captionStyle": spec.caption_style,
        # SKILL-057: Highlight default = Brand-Akzent (NICHT festes #ffd400).
        "captionHighlight": str(b.get("highlight", accent)),
        # SKILL-055/057: Caption-Kontrast-Layer (Pill/Stroke + Alpha), aus Brand-Block.
        "captionBg": str(b.get("captionBg", DEFAULT_CAPTION_BG)),
        "captionBgAlpha": float(b.get("captionBgAlpha", DEFAULT_CAPTION_BG_ALPHA)),
        # SKILL-044: Audio (optional)
        "voiceoverSrc": spec.voiceover,
        "musicSrc": spec.music,
        # Naming (Single Source SKILL-024) — fuer Output-Dateinamen/Reporting
        "variantId": spec.variant_id,
        "utmContent": spec.utm_content,
    }
    # SKILL-056: Talking-Head-Sprecher-Layer (optional) in die Props reichen.
    if spec.speaker is not None:
        props["speakerSrc"] = spec.speaker.src
        props["speakerObjectPosition"] = spec.speaker.object_position
    if spec.content_type:
        props["contentType"] = spec.content_type
    dur = spec.duration_frames()
    if dur:
        props["durationInFrames"] = dur
    return props


def load_reel_spec(spec_path: str) -> ReelSpec:
    """Liest eine Reel-Spec-JSON-Datei und validiert sie zu einer ReelSpec."""
    raw = pathlib.Path(spec_path).read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReelSpecError(f"Reel-Spec {spec_path} ist kein gueltiges JSON: {exc}") from exc
    return parse_reel_spec(data)


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Reel-Spec (JSON) -> Remotion --props (creative-studio SKILL-045)."
    )
    ap.add_argument("--spec", required=True, help="Pfad zur Reel-Spec-JSON.")
    ap.add_argument("--out", help="Pfad fuer das --props-JSON (Default: stdout).")
    args = ap.parse_args(argv)

    spec = load_reel_spec(args.spec)
    props = reel_spec_to_props(spec)
    out_json = json.dumps(props, ensure_ascii=False, indent=2)
    if args.out:
        pathlib.Path(args.out).write_text(out_json, encoding="utf-8")
        print(f"props geschrieben: {args.out} (variant_id={spec.variant_id})")
    else:
        print(out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
