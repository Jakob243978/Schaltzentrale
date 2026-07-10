import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ensureCaptionFont } from "./fonts";

// creative-studio Video-Modul (SKILL-043 + SKILL-055): word-level, burned-in
// Caption-Renderer.
//
// Input = Whisper-/Transkript-Tokens (text + startMs/endMs) — die Transkription
// selbst ist VORGELAGERT (CLI/Helper, z.B. creative_studio/captions.py). Diese
// Komponente konsumiert die Tokens nur und rendert sie im oberen/mittleren
// Drittel ueber der unteren 35 %-Safe-Zone (Reels-UI-frei).
//
// SKILL-055 (Caption-Design-Overhaul, Critique 2026-06-25):
//   - Kontrast-Layer: halbtransparente PILL (Default) ODER harter Outline-STROKE
//     statt nur textShadow -> auf hellem UND dunklem Footage lesbar.
//   - EIN Keyword pro Phrase highlighten (nicht jedes Token >= 6 Zeichen).
//   - Wort-fuer-Wort-Reveal (Fade+Pop via spring), 1-2 aktive Tokens.
//   - Bold-Typo (Weight >= 800), groessere Caption-Schrift, Montserrat-Default.
//
// Multi-Projekt (EARS-5): Farben/Font/Alpha/Stroke kommen aus Brand-Props —
// KEIN hartkodierter Brand-/Projektwert in der Komponente.

// SKILL-043: ein einzelnes Caption-Token (kompatibel zur Remotion-Caption-Struktur
// text/startMs/endMs/timestampMs/confidence — wir nutzen die drei Pflichtfelder).
export type CaptionToken = {
  text: string;
  startMs: number;
  endMs: number;
  // SKILL-055 EARS-2 (optional): explizit als Phrasen-Keyword markiert. Ist es an
  // KEINEM Token einer Phrase gesetzt, waehlt die Heuristik EIN Keyword automatisch.
  keyword?: boolean;
};

export type CaptionStyle = "clean" | "karaoke" | "hormozi";

// SKILL-055: Kontrast-Layer hinter der Caption. "pill" = halbtransparente Box
// (Default, footage-robust), "stroke" = harter Outline-Stroke statt Box.
export type CaptionBg = "pill" | "stroke";

export type CaptionsProps = {
  tokens?: CaptionToken[] | null;
  style?: CaptionStyle;
  // Brand-Props (multi-projekt): Caption-Grundfarbe, Keyword-Highlight, Font.
  ink: string;
  accent: string;
  highlight: string; // Keyword-Highlight (Brand-Akzent statt Gelb); aus Props
  font: string;
  // SKILL-055: Kontrast-Layer-Werte (alle aus Brand-Props/Spec, multi-projekt).
  bg?: string; // Footage-/Brand-BG-Farbe als Pill-Grundton (Default ueber Prop)
  captionBg?: CaptionBg; // "pill" (Default) | "stroke"
  captionBgAlpha?: number; // 0..1 Deckkraft der Pill (Default 0.62)
};

// SKILL-043/055: Safe-Zone-Werte spiegeln AdReel/AdVideo + specs.py (gleiche Logik).
// Captions liegen IM Band zwischen Top-Safe und der oberen Kante der unteren
// 35 %-Safe-Zone — also oberes/mittleres Drittel, NIE im unteren Drittel.
const SAFE_TOP_PCT = 0.14;
const SAFE_BOTTOM_PCT = 0.35;
const SAFE_X_PCT = 0.06;

// SKILL-055: 1-2 Tokens gleichzeitig aktiv (Critique §2: nicht 3 gestapelte Zeilen).
const MAX_ACTIVE_TOKENS = 2;
// SKILL-055: Ziel-Zeilenlaenge <= 18 Zeichen (Critique §2) — Umbruch-Grenze.
const MAX_LINE_CHARS = 18;

// SKILL-055 Default-Konstanten (KEIN Brand-Literal — benannte, ueberschreibbare
// Defaults; projektspezifische Werte kommen aus Props/Spec/branding.env).
const DEFAULT_CAPTION_BG_ALPHA = 0.62;
const DEFAULT_PILL_BG = "#0a0e27"; // neutraler dunkler Default-Grundton (override via prop `bg`)

const groupForFrame = (
  tokens: CaptionToken[],
  ms: number,
): { active: CaptionToken[]; activeIndex: number; windowStart: number } => {
  // aktiver Index = letztes Token, dessen startMs <= ms (oder das gerade laeuft).
  let idx = -1;
  for (let i = 0; i < tokens.length; i++) {
    if (tokens[i].startMs <= ms) idx = i;
    else break;
  }
  if (idx < 0) return { active: [], activeIndex: -1, windowStart: 0 };
  // Fenster von bis zu MAX_ACTIVE_TOKENS um den aktiven Index (zentriert-links).
  const start = Math.max(0, idx - (MAX_ACTIVE_TOKENS - 1));
  const active = tokens.slice(start, idx + 1);
  return { active, activeIndex: idx - start, windowStart: start };
};

const stripPunct = (word: string): string => word.replace(/[^\p{L}\p{N}]/gu, "");

// SKILL-055 EARS-2: GENAU EIN Keyword pro aktiver Phrase.
// Prioritaet: (1) explizit `keyword:true` markiertes Token im Fenster,
// (2) sonst das laengste/zahlhaltige Token (heuristischer Akzent). Liefert den
// Index INNERHALB des aktiven Fensters (oder -1, wenn keins infrage kommt).
const pickKeywordIndex = (active: CaptionToken[]): number => {
  const explicit = active.findIndex((t) => t.keyword === true);
  if (explicit >= 0) return explicit;
  let best = -1;
  let bestScore = -1;
  active.forEach((t, i) => {
    const clean = stripPunct(t.text);
    // Zahl-Tokens schlagen reine Wort-Laenge (Zahl/Ergebnis-zuerst, DISC-rot).
    const score = (/\d/.test(clean) ? 100 : 0) + clean.length;
    // Mindest-Laenge 4, damit Fuellwoerter ("pro", "ohne") nicht highlighten.
    if (clean.length >= 4 && score > bestScore) {
      bestScore = score;
      best = i;
    }
  });
  return best;
};

export const Captions: React.FC<CaptionsProps> = ({
  tokens,
  style = "hormozi",
  ink,
  accent,
  highlight,
  font,
  bg,
  captionBg = "pill",
  captionBgAlpha = DEFAULT_CAPTION_BG_ALPHA,
}) => {
  // SKILL-055: Caption-Font (Montserrat) lokal registrieren (idempotent).
  ensureCaptionFont();

  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // EARS-5 (SKILL-043): keine Tokens -> nichts rendern (Layer optional).
  if (!tokens || tokens.length === 0) return null;

  const ms = (frame / fps) * 1000;
  const { active, activeIndex, windowStart } = groupForFrame(tokens, ms);
  if (active.length === 0) return null;

  const padX = width * SAFE_X_PCT;
  const bandTop = height * SAFE_TOP_PCT;
  const bandBottom = height * SAFE_BOTTOM_PCT;
  // SKILL-055: Caption-Box bei ~54 % Hoehe — klar ueber der unteren 35 %-Safe-Zone
  // (beginnt bei 65 %), unter der Top-Safe-Zone (14 %); eigener Pill-Hintergrund
  // macht die Lesbarkeit footage-unabhaengig (nicht auf Gesicht/Mitte angewiesen).
  const captionCenterY = height * 0.54;

  // SKILL-055 EARS-4: groessere, fettere Typo. Aktiv-Wort ~9 %, Rest ~7,5 % Breite.
  const activeFontSize = width * 0.092;
  const baseFontSize = width * 0.078;
  const baseWeight = style === "clean" ? 700 : 900;

  // SKILL-055 EARS-2: genau ein Keyword pro aktiver Phrase (nur Highlight-Stil).
  const keywordIdx = style === "hormozi" ? pickKeywordIndex(active) : -1;

  // SKILL-055 EARS-1: Pill-Hintergrundfarbe aus Brand-BG-Prop + Alpha.
  const hexToRgba = (hex: string, alpha: number): string => {
    const h = hex.replace("#", "");
    const full = h.length === 3 ? h.split("").map((c) => c + c).join("") : h;
    const r = parseInt(full.slice(0, 2), 16) || 0;
    const g = parseInt(full.slice(2, 4), 16) || 0;
    const b = parseInt(full.slice(4, 6), 16) || 0;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  };
  const pillColor = hexToRgba(bg || DEFAULT_PILL_BG, captionBgAlpha);
  const usePill = captionBg !== "stroke";
  // Stroke-Breite ~6 % der Caption-Schrift (Critique §2 caption_stroke_px).
  const strokePx = Math.max(2, Math.round(activeFontSize * 0.06));

  return (
    <AbsoluteFill
      style={{
        fontFamily: font,
        paddingTop: bandTop,
        paddingBottom: bandBottom,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: captionCenterY,
          left: padX,
          right: padX,
          transform: "translateY(-50%)",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          // SKILL-055: Pill als Container-Hintergrund hinter der aktiven Zeile.
          background: usePill ? pillColor : "transparent",
          borderRadius: usePill ? width * 0.045 : 0,
          padding: usePill
            ? `${height * 0.014}px ${width * 0.05}px`
            : 0,
          boxShadow: usePill ? "0 6px 24px rgba(0,0,0,0.35)" : "none",
          gap: width * 0.022,
          textAlign: "center",
          maxWidth: `${MAX_LINE_CHARS}ch`,
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >
        {active.map((tok, i) => {
          const isActive = i === activeIndex;
          const isKw = i === keywordIdx;
          // Stil-Logik (EARS-2/EARS-3):
          //  - clean:   einheitliche Ink-Farbe, keine Wort-Hervorhebung.
          //  - karaoke: aktives Wort accent-gefaerbt (Reveal/Karaoke).
          //  - hormozi: GENAU EIN Keyword pro Phrase highlight-gefaerbt; das
          //             aktuell gesprochene Wort traegt den Reveal-Pop.
          let color = ink;
          if (style === "karaoke") {
            color = isActive ? accent : ink;
          } else if (style === "hormozi") {
            color = isKw ? highlight : ink;
          }

          // SKILL-055 EARS-3: Wort-fuer-Wort-Reveal. Globaler Token-Index sorgt
          // dafuer, dass jedes neu auftauchende Wort einen eigenen Spring bekommt.
          const globalIdx = windowStart + i;
          const tokenStartFrame = (tok.startMs / 1000) * fps;
          const reveal = spring({
            frame: frame - tokenStartFrame,
            fps,
            config: { damping: 14, stiffness: 160, mass: 0.6 },
          });
          const revealOpacity = interpolate(reveal, [0, 1], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const revealY = interpolate(reveal, [0, 1], [height * 0.018, 0]);
          // Aktives Wort bekommt zusaetzlich einen leichten Pop ueber den Reveal.
          const pop = interpolate(reveal, [0, 1], [0.86, isActive ? 1.06 : 1.0]);

          return (
            <span
              key={`${tok.startMs}-${globalIdx}`}
              style={{
                fontSize: isActive ? activeFontSize : baseFontSize,
                fontWeight: baseWeight,
                lineHeight: 1.02,
                letterSpacing: "-0.01em",
                color,
                textTransform: style === "hormozi" ? "uppercase" : "none",
                // SKILL-055 EARS-1: Kontrast-Layer.
                //  - Pill-Stil: zarter Shadow genuegt (Box traegt den Kontrast).
                //  - Stroke-Stil: harter Outline-Stroke statt Box.
                ...(usePill
                  ? { textShadow: "0 2px 6px rgba(0,0,0,0.45)" }
                  : {
                      WebkitTextStroke: `${strokePx}px ${bg || DEFAULT_PILL_BG}`,
                      paintOrder: "stroke fill",
                      textShadow: "0 2px 8px rgba(0,0,0,0.6)",
                    }),
                transform: `translateY(${revealY}px) scale(${pop})`,
                opacity: revealOpacity,
                transformOrigin: "center bottom",
                display: "inline-block",
              }}
            >
              {tok.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
