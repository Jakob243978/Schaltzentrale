import React from "react";
import { Composition, getAudioDurationInSeconds } from "remotion";
import { getVideoMetadata } from "@remotion/media-utils";
import { AdVideo } from "./AdVideo";
import { AdReel, AdReelProps } from "./AdReel";
import { TalkingHead, TalkingHeadProps } from "./TalkingHead";

// Default-Props = Erst-Einsatz AgentischesArbeiten (h1-immo, Brand aus branding.env).
// Multi-Projekt: beim Render via --props <json> ueberschreiben.

const FPS = 30;
const WIDTH = 1080;
const HEIGHT = 1920;
const FALLBACK_DURATION_FRAMES = 180; // 6 s — stummer Fallback (bestehender Pfad).

// SKILL-057: Reel-Theme-Default-Konstanten (benannte, ueberschreibbare Defaults —
// KEINE Brand-Literale verstreut). Projektspezifische Werte leben in der Spec /
// branding.env (BRAND_HIGHLIGHT, BRAND_CAPTION_FONT, BRAND_CAPTION_BG_ALPHA) und
// werden per --props ueberschrieben. Default-Highlight = Brand-Akzent (statt Gelb,
// Jakob-Vorgabe 2026-06-25), Default-Caption-Font = Montserrat Bold.
const BRAND_ACCENT_DEFAULT = "#f25d3e";
const CAPTION_FONT_DEFAULT =
  "Montserrat, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif";
const CAPTION_HIGHLIGHT_DEFAULT = BRAND_ACCENT_DEFAULT; // SKILL-057: kein festes Highlight-Gelb-Literal mehr
const CAPTION_BG_ALPHA_DEFAULT = 0.62;

// Gemeinsame Brand/Content-Defaults (Title-Card-Werte aus dem bisherigen AdVideo).
const BRAND_DEFAULTS = {
  eyebrow: "MENTORING · WARTELISTE",
  headline: "Verdoppeln",
  headlineAccent: "ohne doppeltes Team",
  subline:
    "Agentisches Arbeiten für Immobilien-Unternehmer. Plätze sind begrenzt.",
  cta: "Auf die Warteliste",
  brandName: "JAKSE-Automations",
  accent: BRAND_ACCENT_DEFAULT,
  bg: "#0a0e27",
  bgSoft: "#11163a",
  ink: "#faf7f2",
  inkMuted: "#9a9ec0",
  // SKILL-055/057: Caption-Default-Font = Montserrat Bold (Title-Card erbt System-Stack).
  font: "-apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
};

// SKILL-044: dynamische Composition-Dauer aus der Audio-/Spec-Laenge ableiten.
// Reihenfolge der Quellen:
//   1. expliziter durationInFrames-Prop (z.B. aus der Reel-Spec berechnet),
//   2. Voiceover-Audio-Laenge (getAudioDurationInSeconds),
//   3. letztes Caption-endMs,
//   4. Fallback 180 Frames (stummer Pfad bricht nicht — EARS-3).
const calculateReelMetadata = async ({
  props,
}: {
  props: AdReelProps & { durationInFrames?: number };
}) => {
  let durationInFrames = FALLBACK_DURATION_FRAMES;

  if (props.durationInFrames && props.durationInFrames > 0) {
    durationInFrames = Math.ceil(props.durationInFrames);
  } else if (props.voiceoverSrc) {
    try {
      const seconds = await getAudioDurationInSeconds(props.voiceoverSrc);
      if (seconds && seconds > 0) {
        durationInFrames = Math.ceil(seconds * FPS);
      }
    } catch {
      // Audio nicht lesbar -> Caption-/Fallback-Pfad unten.
    }
  }

  if (
    durationInFrames === FALLBACK_DURATION_FRAMES &&
    props.captions &&
    props.captions.length > 0
  ) {
    const lastEnd = Math.max(...props.captions.map((c) => c.endMs));
    if (lastEnd > 0) {
      durationInFrames = Math.ceil((lastEnd / 1000) * FPS);
    }
  }

  return { durationInFrames, fps: FPS, width: WIDTH, height: HEIGHT };
};

// SKILL-056: Talking-Head-Dauer aus der Speaker-Clip-Laenge ableiten (O-Ton-Pfad).
// Prioritaet: expliziter durationInFrames-Prop > Video-Laenge des Speaker-Clips >
// letztes Caption-endMs > Fallback.
const calculateTalkingHeadMetadata = async ({
  props,
}: {
  props: TalkingHeadProps & { durationInFrames?: number };
}) => {
  let durationInFrames = FALLBACK_DURATION_FRAMES;

  if (props.durationInFrames && props.durationInFrames > 0) {
    durationInFrames = Math.ceil(props.durationInFrames);
  } else if (props.speakerSrc) {
    try {
      const meta = await getVideoMetadata(props.speakerSrc);
      if (meta?.durationInSeconds && meta.durationInSeconds > 0) {
        durationInFrames = Math.ceil(meta.durationInSeconds * FPS);
      }
    } catch {
      // Clip-Laenge nicht lesbar -> Caption-/Fallback-Pfad unten.
    }
  }

  if (
    durationInFrames === FALLBACK_DURATION_FRAMES &&
    props.captions &&
    props.captions.length > 0
  ) {
    const lastEnd = Math.max(...props.captions.map((c) => c.endMs));
    if (lastEnd > 0) {
      durationInFrames = Math.ceil((lastEnd / 1000) * FPS);
    }
  }

  return { durationInFrames, fps: FPS, width: WIDTH, height: HEIGHT };
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Bestehende statische Title-Card — unveraendert (Brand-Bumper/Outro). */}
      <Composition
        id="AdVideo"
        component={AdVideo}
        durationInFrames={FALLBACK_DURATION_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
        defaultProps={BRAND_DEFAULTS}
      />

      {/* SKILL-043/044/045: Reel-Composition mit Captions + Audio + dyn. Dauer. */}
      <Composition
        id="AdReel"
        component={AdReel}
        durationInFrames={FALLBACK_DURATION_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
        calculateMetadata={calculateReelMetadata}
        defaultProps={
          {
            ...BRAND_DEFAULTS,
            // SKILL-055/057: Caption-Font + Highlight aus benannten Konstanten
            // (kein hartkodiertes Highlight-Gelb). Override per Reel-Spec-Brand-Block.
            font: CAPTION_FONT_DEFAULT,
            captions: null,
            captionStyle: "hormozi",
            captionHighlight: CAPTION_HIGHLIGHT_DEFAULT,
            captionBg: "pill",
            captionBgAlpha: CAPTION_BG_ALPHA_DEFAULT,
            voiceoverSrc: null,
            musicSrc: null,
            musicVolume: 0.5,
            musicDuckVolume: 0.12,
          } as AdReelProps
        }
      />

      {/* SKILL-056: Talking-Head-Composition ("Founder spricht"). */}
      <Composition
        id="TalkingHead"
        component={TalkingHead}
        durationInFrames={FALLBACK_DURATION_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
        calculateMetadata={calculateTalkingHeadMetadata}
        defaultProps={
          {
            ...BRAND_DEFAULTS,
            font: CAPTION_FONT_DEFAULT,
            speakerSrc: "",
            speakerObjectPosition: "50% 50%",
            captions: null,
            captionStyle: "hormozi",
            captionHighlight: CAPTION_HIGHLIGHT_DEFAULT,
            captionBg: "pill",
            captionBgAlpha: CAPTION_BG_ALPHA_DEFAULT,
            lowerThirdName: "",
            lowerThirdClaim: "",
            hookText: "",
            hookWindowSeconds: 3.0,
            ctaOutro: true,
            ctaOutroSeconds: 1.5,
          } as unknown as TalkingHeadProps
        }
      />
    </>
  );
};
