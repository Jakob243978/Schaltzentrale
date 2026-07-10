import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// creative-studio Video-Modul (SKILL-021): animierte 9:16-Ad-Composition.
// Brand-Tokens + Content kommen als Props (multi-projekt). Safe-Zones aus der
// Recherche (untere 35 % frei) als Padding kodiert — gleiche Logik wie das Bild-Modul.

export type AdVideoProps = {
  eyebrow: string;
  headline: string;
  headlineAccent: string; // hervorgehobener Teil der Headline (accent-Farbe)
  subline: string;
  cta: string;
  brandName: string;
  accent: string;
  bg: string;
  bgSoft: string;
  ink: string;
  inkMuted: string;
  font: string;
};

const SAFE_TOP_PCT = 0.14;
const SAFE_BOTTOM_PCT = 0.35;
const SAFE_X_PCT = 0.06;

const fadeUp = (frame: number, start: number, fps: number) => {
  const s = spring({ frame: frame - start, fps, config: { damping: 200 } });
  return {
    opacity: interpolate(frame, [start, start + 12], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }),
    transform: `translateY(${interpolate(s, [0, 1], [28, 0])}px)`,
  };
};

export const AdVideo: React.FC<AdVideoProps> = ({
  eyebrow, headline, headlineAccent, subline, cta, brandName,
  accent, bg, bgSoft, ink, inkMuted, font,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const padTop = height * SAFE_TOP_PCT;
  const padBottom = height * SAFE_BOTTOM_PCT;
  const padX = width * SAFE_X_PCT;

  // CTA: spring-in + dezenter Dauer-Puls danach
  const ctaIn = spring({ frame: frame - 52, fps, config: { damping: 12, stiffness: 120 } });
  const pulse = 1 + 0.02 * Math.sin((frame / fps) * Math.PI * 2 * 1.1);

  return (
    <AbsoluteFill style={{ fontFamily: font, backgroundColor: bg }}>
      {/* Marken-Hintergrund (Gradient wie Bild-Modul) */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(120% 80% at 50% 0%, ${bgSoft} 0%, ${bg} 60%)`,
        }}
      />
      {/* Akzent-Leiste oben */}
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: height * 0.012, background: accent }} />

      {/* Brand-Zeile in der oberen Safe-Zone */}
      <div style={{
        position: "absolute", top: padTop, left: padX, right: padX,
        fontSize: width * 0.03, fontWeight: 600, color: ink, opacity: 0.92,
        ...fadeUp(frame, 0, fps),
      }}>
        {brandName}
      </div>

      {/* Content im sicheren Bereich, unten ausgerichtet (ueber der unteren 35 %-Safe-Zone) */}
      <div style={{
        position: "absolute", top: padTop, bottom: padBottom, left: padX, right: padX,
        display: "flex", flexDirection: "column", justifyContent: "flex-end", gap: height * 0.022,
      }}>
        <div style={{
          fontSize: width * 0.026, fontWeight: 700, letterSpacing: "0.08em",
          textTransform: "uppercase", color: accent, ...fadeUp(frame, 12, fps),
        }}>
          {eyebrow}
        </div>
        <div style={{
          fontSize: width * 0.072, fontWeight: 800, lineHeight: 1.08, letterSpacing: "-0.01em",
          color: ink, ...fadeUp(frame, 22, fps),
        }}>
          {headline} <span style={{ color: accent }}>{headlineAccent}</span>
        </div>
        <div style={{
          fontSize: width * 0.036, fontWeight: 400, lineHeight: 1.35, color: inkMuted, maxWidth: "92%",
          ...fadeUp(frame, 36, fps),
        }}>
          {subline}
        </div>
        <div style={{
          alignSelf: "flex-start", marginTop: height * 0.01,
          background: accent, color: "#fff", fontSize: width * 0.034, fontWeight: 700,
          padding: `${height * 0.018}px ${height * 0.032}px`, borderRadius: 999,
          opacity: interpolate(ctaIn, [0, 1], [0, 1]),
          transform: `scale(${interpolate(ctaIn, [0, 1], [0.85, 1]) * (frame > 64 ? pulse : 1)})`,
        }}>
          {cta}
        </div>
      </div>
    </AbsoluteFill>
  );
};
