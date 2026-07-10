import { continueRender, delayRender, staticFile } from "remotion";

// creative-studio Video-Modul (SKILL-055): Caption-Font-Bootstrap.
//
// Best Practice 2026 (Critique §2): dedizierter Caption-Font mit hoher x-Höhe
// und Weight 700+ (Montserrat Bold als Referenz). Wir betten die TTFs lokal aus
// `public/fonts/` ein (offline-robust, kein Google-Fonts-Netzabruf beim Render).
//
// Multi-Projekt: das Font-*Token* (BRAND_CAPTION_FONT) kommt weiter aus Brand-
// Props/Spec. Dieses Modul registriert nur die Montserrat-Familie, falls sie im
// Font-Stack genutzt wird — projektneutral (kein Brand-/Projektwert hier).

let registered = false;

const FACES: { weight: number; file: string }[] = [
  { weight: 700, file: "fonts/Montserrat-Bold.ttf" },
  { weight: 800, file: "fonts/Montserrat-ExtraBold.ttf" },
  { weight: 900, file: "fonts/Montserrat-Black.ttf" },
];

/**
 * Registriert die lokal gebündelte Montserrat-Familie via FontFace-API.
 * Idempotent; nur einmal pro Render-Prozess aktiv. Blockiert das Rendern bis
 * die Faces geladen sind (delayRender/continueRender), damit der erste Frame
 * bereits im richtigen Font erscheint.
 */
export const ensureCaptionFont = (): void => {
  if (registered) return;
  registered = true;
  // FontFace gibt es im Remotion-Render (Chromium) UND im Studio.
  if (typeof window === "undefined" || typeof (window as unknown as { FontFace?: unknown }).FontFace === "undefined") {
    return;
  }
  const handle = delayRender("Lade Montserrat-Caption-Font");
  Promise.all(
    FACES.map(async ({ weight, file }) => {
      const face = new FontFace(
        "Montserrat",
        `url(${staticFile(file)})`,
        { weight: String(weight), style: "normal" },
      );
      await face.load();
      (document.fonts as unknown as { add: (f: FontFace) => void }).add(face);
    }),
  )
    .then(() => continueRender(handle))
    .catch(() => continueRender(handle)); // Font fehlt -> Fallback-Stack, kein Render-Stop.
};
