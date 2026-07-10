import React from "react";
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  Series,
  staticFile,
  useVideoConfig,
} from "remotion";
import { AdVideo, AdVideoProps } from "./AdVideo";
import { Captions, CaptionToken, CaptionStyle, CaptionBg } from "./Captions";

// SKILL-044/046: Asset-Quellen aufloesen. Remotion-Render akzeptiert nur
// http(s)/data-URLs oder via staticFile() aus dem `public/`-Ordner servierte
// Pfade — KEINE rohen file://-URLs. Lokale Assets werden in `public/assets/`
// gestaget und hier per relativem Pfad ueber staticFile() aufgeloest. Absolute
// http(s)/data-URLs werden unveraendert durchgereicht.
const resolveSrc = (src: string): string => {
  if (/^(https?:|data:)/i.test(src)) return src;
  return staticFile(src.replace(/^\/+/, ""));
};

// SKILL-046 (Vorbereitung): ein B-Roll-Clip aus der Reel-Spec.
export type BrollClip = {
  src: string;
  seconds: number;
};

// creative-studio Video-Modul (SKILL-044): vollwertiges, vertontes Reel.
//
// Komponiert die bestehende AdVideo-Title-Card (Brand/Hook/CTA, Safe-Zones) als
// Basis-Layer und legt darueber:
//   - SKILL-043: word-level Captions (Hormozi-Stil) ueber Whisper-Tokens.
//   - SKILL-044: Voiceover-Track + optionale Hintergrundmusik mit Per-Frame-
//     Ducking (Musik leiser unter Sprache). Composition-Dauer wird in Root.tsx
//     via calculateMetadata DYNAMISCH aus der Audio-/Spec-Laenge abgeleitet.
//
// Bestehender stummer Pfad bleibt intakt: ohne Audio/Captions rendert AdReel wie
// die alte Title-Card (EARS-3 / EARS-5).

export type AdReelProps = AdVideoProps & {
  // B-Roll-Timeline (optional): Clips als Hintergrund-Layer unter Captions/CTA.
  broll?: BrollClip[] | null;
  // SKILL-043: Caption-Track (optional).
  captions?: CaptionToken[] | null;
  captionStyle?: CaptionStyle;
  captionHighlight?: string; // Keyword-Highlight-Farbe (Brand-Akzent, SKILL-057)
  // SKILL-055: Caption-Kontrast-Layer (Pill/Stroke), aus Brand-Props/Spec.
  captionBg?: CaptionBg; // "pill" (Default) | "stroke"
  captionBgAlpha?: number; // 0..1 Pill-Deckkraft (Default 0.62)
  // SKILL-044: Audio-Tracks (optional, Pfade/URLs aus Props/Spec — multi-projekt).
  voiceoverSrc?: string | null;
  musicSrc?: string | null;
  // SKILL-044: Ducking — Musik-Grundlautstaerke + abgesenkte Lautstaerke unter VO.
  musicVolume?: number; // 0..1 Grundpegel der Musik, wenn KEIN Voiceover laeuft
  musicDuckVolume?: number; // 0..1 abgesenkter Pegel, waehrend Voiceover laeuft
};

// SKILL-044: Default-Ducking-Pegel (bewusst einfach, kein Sidechain-DSP).
const DEFAULT_MUSIC_VOLUME = 0.5;
const DEFAULT_MUSIC_DUCK_VOLUME = 0.12;

export const AdReel: React.FC<AdReelProps> = (props) => {
  const {
    broll,
    captions,
    captionStyle = "hormozi",
    captionHighlight,
    captionBg = "pill",
    captionBgAlpha,
    voiceoverSrc,
    musicSrc,
    musicVolume = DEFAULT_MUSIC_VOLUME,
    musicDuckVolume = DEFAULT_MUSIC_DUCK_VOLUME,
    ...adProps
  } = props;

  const { fps } = useVideoConfig();
  const hasVoiceover = Boolean(voiceoverSrc);
  const hasBroll = Boolean(broll && broll.length > 0);

  // SKILL-044: Per-Frame-Ducking. Solange ein Voiceover existiert, faehrt die
  // Musik fuer die GANZE Komposition auf den Duck-Pegel herunter (einfacher,
  // robuster Bereichs-Duck statt token-genauem Sidechain — Recherche §3.3 erlaubt
  // bewusst die einfache Variante). Liegen Caption-Tokens vor, ducken wir nur in
  // deren Sprech-Spannen exakter.
  const duckByFrame = React.useCallback(
    (frame: number): number => {
      if (!hasVoiceover) return musicVolume;
      if (!captions || captions.length === 0) {
        // kein Token-Timing bekannt -> ganze Laufzeit ducken
        return musicDuckVolume;
      }
      const ms = (frame / fps) * 1000;
      const speaking = captions.some(
        (t) => ms >= t.startMs && ms <= t.endMs,
      );
      return speaking ? musicDuckVolume : musicVolume;
    },
    [hasVoiceover, captions, fps, musicVolume, musicDuckVolume],
  );

  return (
    <AbsoluteFill style={{ backgroundColor: adProps.bg }}>
      {/* B-Roll-Layer (optional): Clip-Folge als Hintergrund via Series +
          OffthreadVideo (SKILL-046-Vorbereitung). Liegt UNTER allem. */}
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
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                  }}
                />
              </Series.Sequence>
            ))}
          </Series>
          {/* Lesbarkeits-Scrim, damit Captions/Text auf jedem Footage tragen. */}
          <AbsoluteFill
            style={{
              background:
                "linear-gradient(180deg, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0.0) 30%, rgba(0,0,0,0.0) 60%, rgba(0,0,0,0.55) 100%)",
            }}
          />
        </AbsoluteFill>
      ) : (
        // Ohne B-Roll: bestehende Title-Card als Basis-Layer (Pfad unveraendert).
        <AdVideo {...adProps} />
      )}

      {/* SKILL-043: word-level Captions ueber der unteren 35 %-Safe-Zone. */}
      <Captions
        tokens={captions}
        style={captionStyle}
        ink={adProps.ink}
        accent={adProps.accent}
        highlight={captionHighlight || adProps.accent}
        font={adProps.font}
        bg={adProps.bg}
        captionBg={captionBg}
        captionBgAlpha={captionBgAlpha}
      />

      {/* SKILL-044: Voiceover-Track (EARS-1). */}
      {voiceoverSrc ? <Audio src={resolveSrc(voiceoverSrc)} /> : null}

      {/* SKILL-044: Hintergrundmusik mit Per-Frame-Ducking unter dem Voiceover (EARS-2). */}
      {musicSrc ? <Audio src={resolveSrc(musicSrc)} volume={duckByFrame} /> : null}
    </AbsoluteFill>
  );
};
