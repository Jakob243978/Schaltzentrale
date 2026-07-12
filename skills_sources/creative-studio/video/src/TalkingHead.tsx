import React from "react";
import {
  AbsoluteFill,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { AdVideoProps } from "./AdVideo";
import { Captions, CaptionToken, CaptionStyle, CaptionBg } from "./Captions";

// creative-studio Video-Modul (SKILL-056): Talking-Head-Composition („Founder spricht").
//
// Baut aus EINEM On-Camera-Sprech-Clip ein markenkonsistentes 9:16-Founder-Reel:
//   - durchgaengiger Vordergrund-Speaker-Layer (objectFit:cover, O-Ton),
//   - SKILL-055-Pill-Captions ueber dem Sprecher (optional — fehlt der Track,
//     rendert das Reel ohne Captions weiter),
//   - Brand-Lower-Third (Name/Claim), Safe-Zone-konform,
//   - Hook-Promise-Fenster < 3 s,
//   - kurzes CTA-Outro (Brand-Bumper) am Ende.
//
// Multi-Projekt (EARS-5): Footage-Pfad, Brand-Tokens, Hook-/CTA-Text und
// Lower-Third kommen ausschliesslich aus Props/Spec — kein hartkodierter Wert.

const resolveSrc = (src: string): string => {
  if (/^(https?:|data:)/i.test(src)) return src;
  return staticFile(src.replace(/^\/+/, ""));
};

const SAFE_TOP_PCT = 0.14;
const SAFE_BOTTOM_PCT = 0.35;
const SAFE_X_PCT = 0.06;

export type TalkingHeadProps = AdVideoProps & {
  // SKILL-056 EARS-1: On-Camera-Sprech-Clip (Pflicht fuer diesen Render-Pfad).
  speakerSrc: string;
  speakerObjectPosition?: string; // Reframe-Crop, z.B. "50% 30%"
  // SKILL-056 EARS-2: optionaler word-level Caption-Track (SKILL-043/055).
  captions?: CaptionToken[] | null;
  captionStyle?: CaptionStyle;
  captionHighlight?: string;
  captionBg?: CaptionBg;
  captionBgAlpha?: number;
  // SKILL-056 EARS-3: Lower-Third (Name/Claim) + Hook-Promise.
  lowerThirdName?: string;
  lowerThirdClaim?: string;
  hookText?: string;
  hookWindowSeconds?: number; // Default 3 s (talking_head-CONTENT_TYPE)
  // SKILL-056 EARS-4: CTA-Outro (Brand-Bumper) am Ende.
  ctaOutro?: boolean;
  ctaOutroSeconds?: number; // Default 1.5 s
};

const HOOK_WINDOW_DEFAULT = 3.0;
const CTA_OUTRO_SECONDS_DEFAULT = 1.5;

export const TalkingHead: React.FC<TalkingHeadProps> = ({
  speakerSrc,
  speakerObjectPosition = "50% 50%",
  captions,
  captionStyle = "hormozi",
  captionHighlight,
  captionBg = "pill",
  captionBgAlpha,
  lowerThirdName,
  lowerThirdClaim,
  hookText,
  hookWindowSeconds = HOOK_WINDOW_DEFAULT,
  ctaOutro = true,
  ctaOutroSeconds = CTA_OUTRO_SECONDS_DEFAULT,
  // Brand/Content (AdVideoProps)
  accent,
  bg,
  bgSoft,
  ink,
  inkMuted,
  font,
  cta,
  brandName,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();

  const padX = width * SAFE_X_PCT;
  const padTop = height * SAFE_TOP_PCT;
  const padBottom = height * SAFE_BOTTOM_PCT;

  const hookEndFrame = Math.round(hookWindowSeconds * fps);
  const outroFrames = Math.max(1, Math.round(ctaOutroSeconds * fps));
  const outroStart = Math.max(0, durationInFrames - outroFrames);

  // Lower-Third spring-in (Safe-Zone-konform, ueber der unteren 35 %-Zone).
  const ltIn = spring({ frame: frame - 14, fps, config: { damping: 18 } });
  const ltOpacity = interpolate(ltIn, [0, 1], [0, 1]);
  const ltY = interpolate(ltIn, [0, 1], [24, 0]);

  // Hook-Promise: nur im Fenster < hookWindowSeconds sichtbar (EARS-3).
  const hookOpacity = interpolate(
    frame,
    [0, 6, hookEndFrame - 8, hookEndFrame],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <AbsoluteFill style={{ fontFamily: font, backgroundColor: bg }}>
      {/* SKILL-056 EARS-1: durchgaengiger Speaker-Layer, O-Ton (NICHT gemutet). */}
      <AbsoluteFill>
        <OffthreadVideo
          src={resolveSrc(speakerSrc)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: speakerObjectPosition,
          }}
        />
        {/* Lesbarkeits-Scrim oben/unten, damit Captions/Lower-Third tragen. */}
        <AbsoluteFill
          style={{
            background:
              "linear-gradient(180deg, rgba(0,0,0,0.30) 0%, rgba(0,0,0,0.0) 22%, rgba(0,0,0,0.0) 58%, rgba(0,0,0,0.60) 100%)",
          }}
        />
      </AbsoluteFill>

      {/* SKILL-056 EARS-3: Hook-Promise im Frame < hookWindowSeconds. */}
      {hookText ? (
        <div
          style={{
            position: "absolute",
            top: padTop,
            left: padX,
            right: padX,
            opacity: hookOpacity,
            fontSize: width * 0.066,
            fontWeight: 900,
            lineHeight: 1.05,
            letterSpacing: "-0.01em",
            color: ink,
            textShadow: "0 2px 10px rgba(0,0,0,0.55)",
          }}
        >
          {hookText}
        </div>
      ) : null}

      {/* SKILL-056 EARS-2: Pill-Captions ueber dem Sprecher (optional). */}
      <Captions
        tokens={captions}
        style={captionStyle}
        ink={ink}
        accent={accent}
        highlight={captionHighlight || accent}
        font={font}
        bg={bg}
        captionBg={captionBg}
        captionBgAlpha={captionBgAlpha}
      />

      {/* SKILL-056 EARS-3: Brand-Lower-Third (Name/Claim) ueber der unteren Safe-Zone. */}
      {lowerThirdName || lowerThirdClaim ? (
        <div
          style={{
            position: "absolute",
            left: padX,
            right: padX,
            bottom: padBottom + height * 0.01,
            opacity: ltOpacity,
            transform: `translateY(${ltY}px)`,
            display: "flex",
            flexDirection: "column",
            gap: height * 0.006,
          }}
        >
          {lowerThirdName ? (
            <div
              style={{
                alignSelf: "flex-start",
                background: accent,
                color: "#fff",
                fontSize: width * 0.042,
                fontWeight: 800,
                padding: `${height * 0.008}px ${width * 0.035}px`,
                borderRadius: 999,
              }}
            >
              {lowerThirdName}
            </div>
          ) : null}
          {lowerThirdClaim ? (
            <div
              style={{
                fontSize: width * 0.03,
                fontWeight: 600,
                color: ink,
                textShadow: "0 2px 8px rgba(0,0,0,0.6)",
              }}
            >
              {lowerThirdClaim}
            </div>
          ) : null}
        </div>
      ) : null}

      {/* SKILL-056 EARS-4: CTA-Outro-Bumper am Ende (Brand-BG + CTA-Text). */}
      {ctaOutro ? (
        <Sequence from={outroStart} durationInFrames={outroFrames}>
          <AbsoluteFill
            style={{
              background: `radial-gradient(120% 80% at 50% 35%, ${bgSoft} 0%, ${bg} 70%)`,
              alignItems: "center",
              justifyContent: "center",
              padding: padX,
            }}
          >
            <div style={{ textAlign: "center" }}>
              <div
                style={{
                  fontSize: width * 0.03,
                  fontWeight: 700,
                  letterSpacing: "0.08em",
                  textTransform: "uppercase",
                  color: inkMuted,
                  marginBottom: height * 0.018,
                }}
              >
                {brandName}
              </div>
              <div
                style={{
                  display: "inline-block",
                  background: accent,
                  color: "#fff",
                  fontSize: width * 0.05,
                  fontWeight: 800,
                  padding: `${height * 0.018}px ${width * 0.06}px`,
                  borderRadius: 999,
                }}
              >
                {cta}
              </div>
            </div>
          </AbsoluteFill>
        </Sequence>
      ) : null}
    </AbsoluteFill>
  );
};
