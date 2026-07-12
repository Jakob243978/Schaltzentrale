import React from "react";
import {
  AbsoluteFill,
  Audio,
  interpolate,
  OffthreadVideo,
  Series,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// creative-studio Video-Modul (SKILL-078): B-Roll + Message-Composition.
//
// Eigenstaendiges, sauberes Reel-Format (loest die Zweckentfremdung von
// TalkingHead ab): montiert B-Roll-Clips als Vollbild-9:16-Hintergrund und legt
// eine redaktionell durchdachte Copy darueber — Hook oben (editorial Serif,
// obere Safe-Zone) + abholende Message (editorial Serif, unteres Mittel-Drittel
// ueber der Reels-UI). Optional eine dunkle Box hinter der Message (Saskia-Loesung
// fuer helle/kontrastarme B-Roll).
//
// KEIN Talking-Head, KEIN Akzent-Balken, KEINE Wort-fuer-Wort-Captions.
//
// Multi-Projekt (EARS-5): Footage-Pfade, Brand-Tokens (accent/ink/bg/font …),
// Hook- und Message-Text kommen ausschliesslich aus Props/Spec — kein
// hartkodierter Brand-/Projektwert.

const resolveSrc = (src: string): string => {
  if (/^(https?:|data:)/i.test(src)) return src;
  return staticFile(src.replace(/^\/+/, ""));
};

// Safe-Zonen (9:16 Reels): obere ~14 % frei, untere ~35 % = Plattform-UI (frei).
const SAFE_TOP_PCT = 0.14;
const SAFE_BOTTOM_PCT = 0.35;
const SAFE_X_PCT = 0.06;

const hexToRgba = (hex: string, alpha: number): string => {
  const h = (hex || "#000000").replace("#", "");
  const full = h.length === 3 ? h.split("").map((c) => c + c).join("") : h;
  const r = parseInt(full.slice(0, 2), 16) || 0;
  const g = parseInt(full.slice(2, 4), 16) || 0;
  const b = parseInt(full.slice(4, 6), 16) || 0;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
};

export type BrollClip = {
  src: string;
  seconds: number;
};

export type MessageScene = {
  text: string;
  seconds: number;
};

export type BrollMessageProps = {
  // SKILL-078 EARS-1: B-Roll-Clips als Vollbild-Hintergrund (objectFit cover).
  broll?: BrollClip[] | null;
  // SKILL-078 EARS-2: Pflicht-Copy — Hook (oben) + Message (Haupttext).
  hookText: string;
  message: string;
  // SKILL-078: optionale zeitlich abgestufte Sub-Messages je Segment.
  messageScenes?: MessageScene[] | null;
  // SKILL-078 EARS-3: dunkle Box hinter der Message (Kontrast-Loesung, aufgeloest).
  textBox?: boolean;
  // Brand-Tokens (multi-projekt): editorial-Serif kommt ueber `font` (kein Literal).
  accent: string;
  bg: string;
  bgSoft: string;
  ink: string;
  inkMuted: string;
  font: string;
  // Audio optional (Meta Sound-off Default -> O-Ton der B-Roll ist stumm).
  voiceoverSrc?: string | null;
  musicSrc?: string | null;
  musicVolume?: number;
};

// SKILL-078: gemeinsamer Message-Textblock (Hook oben ODER Message unten).
const TextBlock: React.FC<{
  text: string;
  fontFamily: string;
  color: string;
  fontSize: number;
  weight: number;
  box: boolean;
  boxColor: string;
  padX: number;
  width: number;
  height: number;
  opacity: number;
}> = ({ text, fontFamily, color, fontSize, weight, box, boxColor, width, height, opacity }) => {
  return (
    <div
      style={{
        display: "inline-block",
        maxWidth: "100%",
        opacity,
        fontFamily,
        fontSize,
        fontWeight: weight,
        lineHeight: 1.18,
        letterSpacing: "-0.005em",
        color,
        textAlign: "center",
        // Immer ein starker Schatten (traegt auch OHNE Box auf dunkler B-Roll).
        textShadow: box ? "0 2px 10px rgba(0,0,0,0.35)" : "0 2px 14px rgba(0,0,0,0.75)",
        // SKILL-078 EARS-3: dunkle Box (aufgeloest) hinter dem Text.
        background: box ? boxColor : "transparent",
        borderRadius: box ? width * 0.03 : 0,
        padding: box ? `${height * 0.018}px ${width * 0.05}px` : 0,
        boxShadow: box ? "0 10px 40px rgba(0,0,0,0.45)" : "none",
      }}
    >
      {text}
    </div>
  );
};

export const BrollMessage: React.FC<BrollMessageProps> = ({
  broll,
  hookText,
  message,
  messageScenes,
  textBox = false,
  bg,
  bgSoft,
  ink,
  font,
  voiceoverSrc,
  musicSrc,
  musicVolume = 0.5,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();

  const padX = width * SAFE_X_PCT;
  const padTop = height * SAFE_TOP_PCT;
  const padBottom = height * SAFE_BOTTOM_PCT;

  const hasBroll = Boolean(broll && broll.length > 0);
  const boxColor = hexToRgba(bgSoft || bg, 0.62);

  // Hook: sauberer Fade-in in der ersten ~0,5 s, danach persistent.
  const hookOpacity = interpolate(frame, [0, Math.round(fps * 0.5)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Message: kurzer Fade-in ~0,3 s nach dem Hook.
  const msgOpacity = interpolate(
    frame,
    [Math.round(fps * 0.3), Math.round(fps * 0.8)],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  const useScenes = Boolean(messageScenes && messageScenes.length > 0);

  return (
    <AbsoluteFill style={{ backgroundColor: bg }}>
      {/* SKILL-078 EARS-1: B-Roll-Layer (Vollbild 9:16, objectFit cover, O-Ton
          stumm — Meta Sound-off). OffthreadVideo wendet Rotations-Metadaten an,
          sodass hochkant gedrehtes iPhone-Footage aufrecht steht. */}
      {hasBroll ? (
        <AbsoluteFill>
          <Series>
            {broll!.map((clip, i) => (
              <Series.Sequence
                key={`${clip.src}-${i}`}
                durationInFrames={Math.max(1, Math.round(clip.seconds * fps))}
                premountFor={30}
              >
                <OffthreadVideo
                  src={resolveSrc(clip.src)}
                  muted
                  style={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
              </Series.Sequence>
            ))}
          </Series>
          {/* Lesbarkeits-Scrim oben/unten, damit Hook + Message auf jedem
              Footage tragen (unabhaengig von der Box). */}
          <AbsoluteFill
            style={{
              background:
                "linear-gradient(180deg, rgba(0,0,0,0.42) 0%, rgba(0,0,0,0.0) 24%, rgba(0,0,0,0.0) 52%, rgba(0,0,0,0.62) 100%)",
            }}
          />
        </AbsoluteFill>
      ) : (
        // Ohne B-Roll: Brand-Gradient als ruhiger Hintergrund (Reel bricht nicht).
        <AbsoluteFill
          style={{
            background: `radial-gradient(120% 80% at 50% 0%, ${bgSoft} 0%, ${bg} 60%)`,
          }}
        />
      )}

      {/* SKILL-078 EARS-2: Hook oben in der oberen Safe-Zone (editorial Serif). */}
      <div
        style={{
          position: "absolute",
          top: padTop,
          left: padX,
          right: padX,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <TextBlock
          text={hookText}
          fontFamily={font}
          color={ink}
          fontSize={width * 0.05}
          weight={600}
          box={false}
          boxColor={boxColor}
          padX={padX}
          width={width}
          height={height}
          opacity={hookOpacity}
        />
      </div>

      {/* SKILL-078 EARS-2: Message im unteren Mittel-Drittel, ueber der unteren
          35 %-Reels-UI-Zone. Bei messageScenes zeitlich abgestufte Sub-Messages. */}
      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "flex-end",
          paddingBottom: padBottom + height * 0.03,
          paddingLeft: padX,
          paddingRight: padX,
        }}
      >
        {useScenes ? (
          <Series>
            {messageScenes!.map((sc, i) => (
              <Series.Sequence
                key={`${i}-${sc.text.slice(0, 12)}`}
                durationInFrames={Math.max(1, Math.round(sc.seconds * fps))}
              >
                <AbsoluteFill
                  style={{
                    alignItems: "center",
                    justifyContent: "flex-end",
                    paddingBottom: padBottom + height * 0.03,
                    paddingLeft: padX,
                    paddingRight: padX,
                  }}
                >
                  <TextBlock
                    text={sc.text}
                    fontFamily={font}
                    color={ink}
                    fontSize={width * 0.072}
                    weight={600}
                    box={textBox}
                    boxColor={boxColor}
                    padX={padX}
                    width={width}
                    height={height}
                    opacity={1}
                  />
                </AbsoluteFill>
              </Series.Sequence>
            ))}
          </Series>
        ) : (
          <TextBlock
            text={message}
            fontFamily={font}
            color={ink}
            fontSize={width * 0.072}
            weight={600}
            box={textBox}
            boxColor={boxColor}
            padX={padX}
            width={width}
            height={height}
            opacity={msgOpacity}
          />
        )}
      </AbsoluteFill>

      {/* Audio optional (Default stumm): Voiceover + optionale Musik. */}
      {voiceoverSrc ? <Audio src={resolveSrc(voiceoverSrc)} /> : null}
      {musicSrc ? <Audio src={resolveSrc(musicSrc)} volume={musicVolume} /> : null}

      {/* durationInFrames referenzieren, damit die Signatur stabil bleibt. */}
      {durationInFrames < 0 ? <AbsoluteFill /> : null}
    </AbsoluteFill>
  );
};
