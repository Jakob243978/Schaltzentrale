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

# SKILL-078: Content-Type-Key des B-Roll+Message-Formats (eigenstaendig, KEIN
# zweckentfremdeter talking_head mehr). Steuert Validierung (hook+message Pflicht)
# und die Remotion-Composition-Auswahl (BrollMessage).
BROLL_MESSAGE = "broll_message"

# SKILL-078: Mapping Composition-Auswahl ueber content_type. Der reel_spec-Loader
# liefert NUR die Props; die Composition-Id waehlt der Renderer (`npx remotion
# render … <CompositionId>`). Diese Tabelle ist die Single Source dafuer.
_CONTENT_TYPE_TO_COMPOSITION = {
    BROLL_MESSAGE: "BrollMessage",
    "talking_head": "TalkingHead",
}
DEFAULT_COMPOSITION = "AdReel"


class ReelSpecError(ValueError):
    """SKILL-045 EARS-2: klare Fehlermeldung bei ungueltiger/unvollstaendiger Spec."""


# === SKILL-078: Reel-Pfad zentral an die Brand anbinden ======================
# Bisher trug JEDE Reel-Spec ihren eigenen brand-Block; eine zentrale
# Brand-Aenderung (brand.json / branding.env) schlug NICHT auf Reels durch
# (anders als beim Bild-Pfad via render_image.resolve_brand). Das widerspricht
# Jakobs Prinzip „Config zentral entkoppeln".
#
# Loesung: dieselbe resolve-Logik wie der Bild-Pfad wiederverwenden
# (render_image.resolve_brand) — KEIN zweites Schema. Die zentral aufgeloesten
# internen BRAND_*-Keys werden auf die Reel-Token-Namen gemappt. Der brand-Block
# IN der Spec wird zum optionalen Override.
# Praezedenz: Spec-brand > zentrale brand.json/branding.env > Defaults.

# Interne render_image-BRAND_*-Keys -> Reel-Token-Namen (die AdVideo/AdReel-Props).
_CENTRAL_TO_REEL_TOKEN = {
    "BRAND_NAME": "name",
    "BRAND_ACCENT": "accent",
    "BRAND_BG": "bg",
    "BRAND_BG_SOFT": "bgSoft",
    "BRAND_INK": "ink",
    "BRAND_INK_MUTED": "inkMuted",
    "BRAND_FONT": "font",
}

# SKILL-057 Reel-/Caption-Tokens leben ebenfalls zentral in derselben
# branding.env (BRAND_HIGHLIGHT/BRAND_CAPTION_FONT/BRAND_CAPTION_BG_ALPHA) bzw.
# im brand.json (highlight/caption_font/caption_bg_alpha). Sie sind reel-spezifisch
# (der Bild-Renderer kennt sie nicht), werden also aus derselben Quelle nachgelesen.
_CAPTION_ENV_TO_REEL_TOKEN = {
    "BRAND_HIGHLIGHT": "highlight",
    "BRAND_CAPTION_FONT": "captionFont",
    "BRAND_CAPTION_BG_ALPHA": "captionBgAlpha",
}
_CAPTION_JSON_TO_REEL_TOKEN = {
    "highlight": "highlight",
    "caption_font": "captionFont",
    "caption_bg_alpha": "captionBgAlpha",
}


def _read_caption_extras(brand_env: Any, brand_json: Any) -> dict[str, Any]:
    """Liest die reel-spezifischen SKILL-057-Caption-Tokens aus derselben
    Brand-Quelle (branding.env / brand.json). branding.env verliert diese Keys
    im Bild-Resolver (nicht Teil von _BRAND_DEFAULTS), daher hier direkt gelesen —
    aus DERSELBEN Datei, kein zweites Schema fuer die Kern-Tokens.

    Praezedenz innerhalb der zentralen Quelle: brand.json > branding.env.
    """
    out: dict[str, Any] = {}

    # branding.env (Pfad -> Zeilen KEY="value").
    if isinstance(brand_env, str) and brand_env:
        try:
            for raw in pathlib.Path(brand_env).read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                tok = _CAPTION_ENV_TO_REEL_TOKEN.get(k.strip())
                if tok:
                    val = v.strip().strip('"').strip("'")
                    if val:
                        out[tok] = val
        except OSError:
            pass
    elif isinstance(brand_env, dict):
        for k, tok in _CAPTION_ENV_TO_REEL_TOKEN.items():
            if brand_env.get(k):
                out[tok] = brand_env[k]

    # brand.json (Pfad ODER dict) ueberschreibt branding.env.
    data: dict[str, Any] | None = None
    if isinstance(brand_json, dict):
        data = brand_json
    elif isinstance(brand_json, str) and brand_json:
        try:
            loaded = json.loads(pathlib.Path(brand_json).read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                data = loaded
        except (OSError, ValueError):
            data = None
    if data:
        for jkey, tok in _CAPTION_JSON_TO_REEL_TOKEN.items():
            val = data.get(jkey)
            if val not in (None, ""):
                out[tok] = val

    return out


def resolve_central_reel_brand(brand_env: Any = None, brand_json: Any = None,
                               warn=None) -> dict[str, Any]:
    """SKILL-078: zentrale Reel-Brand-Tokens aus brand.json/branding.env.

    Reused die Bild-Pfad-Logik (render_image.resolve_brand) fuer die
    Kern-Tokens (name/accent/bg/bgSoft/ink/inkMuted/font) und ergaenzt die
    reel-spezifischen SKILL-057-Caption-Tokens aus derselben Quelle. Rueckgabe
    ist ein Reel-Token-dict (name/accent/... — dieselben Keys wie ein
    Spec-brand-Block), das als Basis unter den Spec-brand-Override gelegt wird.

    Eine Brand-Datei aendern -> Bilder UND Reels folgen automatisch.
    """
    from .render_image import resolve_brand  # lokal, um Import-Zyklus zu meiden

    resolved = resolve_brand(brand_env=brand_env, brand_json=brand_json, warn=warn)
    tokens: dict[str, Any] = {}
    for internal_key, reel_token in _CENTRAL_TO_REEL_TOKEN.items():
        val = resolved.get(internal_key)
        if val not in (None, ""):
            tokens[reel_token] = val
    tokens.update(_read_caption_extras(brand_env, brand_json))
    return tokens


def _resolve_text_box(value: Any) -> bool:
    """SKILL-078: dunkle Box hinter der Message aufloesen.

    `text_box`-Flag: True | False | "auto" (Default). Der Render kann den
    tatsaechlichen B-Roll-Kontrast nicht messen (das ist der Job des Vision-QA-
    Passes, SKILL-075) — deshalb loest "auto" KONSERVATIV auf Box-AN auf: lieber
    eine lesbare Message mit dezenter Box als ein still unleserliches Reel. Der
    Agent setzt nach dem Vision-QA-Blick `text_box:false`, wenn die B-Roll dunkel
    genug ist, dass die Box unnoetig waere.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("true", "1", "yes", "on"):
            return True
        if v in ("false", "0", "no", "off"):
            return False
        # "auto" (und alles Unbekannte) -> konservativ Box-AN.
        return True
    return True


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
    # SKILL-078: broll_message-Format — abholender Haupttext + optionale dunkle Box.
    message: str = ""
    text_box: Any = "auto"  # True | False | "auto" (siehe _resolve_text_box)

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

    @property
    def composition_id(self) -> str:
        """SKILL-078: Remotion-Composition-Id fuer diese Spec (Single Source).

        broll_message -> BrollMessage, talking_head -> TalkingHead, sonst AdReel.
        Der Renderer nutzt den Wert im `npx remotion render … <CompositionId>`.
        """
        return _CONTENT_TYPE_TO_COMPOSITION.get(self.content_type or "", DEFAULT_COMPOSITION)

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


def parse_reel_spec(data: dict[str, Any],
                    central_brand: dict[str, Any] | None = None) -> ReelSpec:
    """SKILL-045: validiert ein Spec-Dict und baut eine ReelSpec.

    EARS-2: fehlt ein Pflichtfeld (ad_id/hook), wird ReelSpecError geworfen
    — kein stilles leeres Reel.
    EARS-3: captions/broll/voiceover/music/scenes sind optional.

    SKILL-078 (zentrale Brand): `central_brand` (Reel-Token-dict aus
    resolve_central_reel_brand) wird als Basis unter den Spec-brand-Block gelegt.
    Praezedenz: Spec-brand > central_brand > Defaults. Der brand-Block IN der Spec
    ist damit ein optionaler OVERRIDE — Pflicht ist nur noch, dass die EFFEKTIVE
    Brand einen Namen traegt (aus Spec ODER zentraler Quelle).

    SKILL-078 (broll_message): ist `content_type == "broll_message"`, sind `hook`
    UND `message` Pflicht (kein still leeres/textloses Reel — EARS-Geist).
    """
    if not isinstance(data, dict):
        raise ReelSpecError("Reel-Spec muss ein JSON-Objekt (Mapping) sein.")

    ad_id = str(_require(data, "ad_id"))
    hook = str(_require(data, "hook"))

    # SKILL-078: Spec-brand ist ein optionaler Override ueber der zentralen Brand.
    spec_brand = data.get("brand") or {}
    if not isinstance(spec_brand, dict):
        raise ReelSpecError("Reel-Spec: 'brand' muss ein Objekt mit Brand-Tokens sein.")
    brand: dict[str, Any] = dict(central_brand or {})
    for k, v in spec_brand.items():  # Spec gewinnt (hoechste Praezedenz)
        if v not in (None, ""):
            brand[k] = v
    if not (str(brand.get("name") or "")).strip():
        raise ReelSpecError(
            "Reel-Spec: 'brand.name' ist Pflicht — weder der Spec-brand-Block noch "
            "die zentrale Brand (brand.json/branding.env) liefern einen Namen."
        )

    content_type = (data.get("content_type") or None)
    message = str(data.get("message", ""))
    if content_type == BROLL_MESSAGE:
        # EARS: hook (bereits oben) UND message Pflicht -> kein stilles leeres Reel.
        if not message.strip():
            raise ReelSpecError(
                "Reel-Spec (broll_message): Pflichtfeld 'message' (der abholende "
                "Haupttext) fehlt oder ist leer. Ein broll_message-Reel ohne "
                "durchdachte Message waere unvollstaendig (redaktionelle Copy-Pflicht)."
            )

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
        content_type=content_type,
        speaker=speaker,
        message=message,
        text_box=data.get("text_box", "auto"),
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
        # SKILL-086: Methoden-Tagging — das verwendete Copy-Framework als explizites
        # Metadaten-Feld (zusaetzlich zu variant_id/utm_content, die es bereits
        # positional tragen). So ist aus props.json ablesbar, mit welcher Methode das
        # Reel gebaut wurde. Der Output-MP4 soll nach variant_id benannt werden.
        "framework": spec.framework,
    }
    # SKILL-056: Talking-Head-Sprecher-Layer (optional) in die Props reichen.
    if spec.speaker is not None:
        props["speakerSrc"] = spec.speaker.src
        props["speakerObjectPosition"] = spec.speaker.object_position
    if spec.content_type:
        props["contentType"] = spec.content_type
    # SKILL-078: broll_message-Props. Composition = BrollMessage (via composition_id).
    # Hook liegt oben (Serif, obere Safe-Zone), Message als abholender Haupttext
    # (Serif, unteres Mittel-Drittel). Szenen -> zeitlich abgestufte Sub-Messages.
    if spec.content_type == BROLL_MESSAGE:
        props["hookText"] = spec.hook
        props["message"] = spec.message
        props["messageScenes"] = [s.to_dict() for s in spec.scenes] or None
        props["textBox"] = _resolve_text_box(spec.text_box)
        # broll_message hat KEINE Captions -> der `font`-Prop ist die editorial
        # Serif (Hook + Message). Er kommt aus brand.font (Spec-Override > zentral),
        # NICHT aus dem Caption-Font (der Captions-Fall gilt hier nicht).
        props["font"] = str(b.get("font") or caption_font)
    dur = spec.duration_frames()
    if dur:
        props["durationInFrames"] = dur
    return props


def load_reel_spec(spec_path: str, brand_env: Any = None, brand_json: Any = None,
                   warn=None) -> ReelSpec:
    """Liest eine Reel-Spec-JSON-Datei und validiert sie zu einer ReelSpec.

    SKILL-078: sind `brand_env`/`brand_json` gesetzt, wird die zentrale Brand
    (resolve_central_reel_brand) als Basis unter den Spec-brand-Override gelegt —
    eine Brand-Datei aendern -> Bilder UND Reels folgen.
    """
    raw = pathlib.Path(spec_path).read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReelSpecError(f"Reel-Spec {spec_path} ist kein gueltiges JSON: {exc}") from exc
    central = None
    if brand_env or brand_json:
        central = resolve_central_reel_brand(brand_env=brand_env, brand_json=brand_json,
                                             warn=warn)
    return parse_reel_spec(data, central_brand=central)


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Reel-Spec (JSON) -> Remotion --props (creative-studio SKILL-045)."
    )
    ap.add_argument("--spec", required=True, help="Pfad zur Reel-Spec-JSON.")
    ap.add_argument("--out", help="Pfad fuer das --props-JSON (Default: stdout).")
    ap.add_argument("--brand-env", dest="brand_env",
                    help="SKILL-078: zentrale branding.env (Basis unter Spec-brand-Override).")
    ap.add_argument("--brand-json", dest="brand_json",
                    help="SKILL-078: zentrales brand.json (Basis unter Spec-brand-Override).")
    args = ap.parse_args(argv)

    spec = load_reel_spec(args.spec, brand_env=args.brand_env, brand_json=args.brand_json)
    props = reel_spec_to_props(spec)
    out_json = json.dumps(props, ensure_ascii=False, indent=2)
    if args.out:
        pathlib.Path(args.out).write_text(out_json, encoding="utf-8")
        print(
            f"props geschrieben: {args.out} "
            f"(variant_id={spec.variant_id}, composition={spec.composition_id})"
        )
    else:
        print(out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
