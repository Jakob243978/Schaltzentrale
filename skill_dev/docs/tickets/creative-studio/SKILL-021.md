# SKILL-021: creative-studio — Video-Modul (Remotion, 9:16 + Multi-Format, Safe-Zone-Untertitel)

**Status:** in_progress
**Erstellt:** 2026-06-23
**MoSCoW:** Could
**Geschaetzter Aufwand:** L
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei spec gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/research/2026-06-23_ad-video-automation.md`

> [!info] Herkunft (Jakob 2026-06-23)
> Zweite Ausbaustufe des `creative-studio`-Skills (nach Bild-Modul SKILL-020): agentische
> Ad-**Video**-Erzeugung. Empfehlung der Recherche: **Remotion** (React→MP4, Claude schreibt den Code →
> versioniert/reproduzierbar) als Hauptweg; ffmpeg/MoviePy als lizenzfreier Einstieg; Cloud-API
> (Creatomate/json2video) als setup-armer Shortcut. DaVinci-MCP nur für Mensch-im-Loop-NLE-Schnitt
> (GUI-/Studio-gebunden, nicht headless → nicht für die Pipeline).

## Was soll erreicht werden? (Business-Ziel, grob)
Aus Skript/Copy + Voiceover/Avatar + Clips automatisiert ein **Reels-Video (9:16)** schneiden — mit
Safe-Zone-konformen Untertiteln, Logo/CTA, Multi-Format-Export — über denselben Web-Tech-Kern wie das
Bild-Modul (Brand-Tokens, Safe-Zones geteilt).

## Offene Punkte vor `spec` (po-challenge)
- Lizenz-Caveat Remotion (ab 4 Personen 100 USD/Mo) gegen ffmpeg/MoviePy (frei) abwägen.
- Voiceover/Avatar-Quelle: HeyGen-API (Talking-Head) vs. TTS (ElevenLabs) — separates Bausteins-Ticket?
- Pragmatischer Einstieg laut Recherche: ffmpeg/MoviePy-Prototyp (Voiceover + Untertitel + 9:16),
  später auf Remotion heben — als eigenes Sub-Ticket sinnvoll?

## Technische Hinweise
- Code-Ablage `skills_sources/creative-studio/` (Video-Submodul). Geteilte Safe-Zone-/Brand-Logik mit SKILL-020.
- Vollständiger Tool-Vergleich + Workflow-Skizze: `2026-06-23_ad-video-automation.md`.

## Code-Referenzen
- `skills_sources/creative-studio/video/` — Remotion-Projekt: `package.json` (remotion 4.0.482, React 19),
  `src/AdVideo.tsx` (animierte 9:16-Composition, Safe-Zone als Padding, Brand-Tokens als Props),
  `src/Root.tsx` (Composition-Registrierung + Default-Props = h1-immo/Brand), `src/index.ts`, `tsconfig.json`.

## Ergebnis / Notizen
**Implementiert (2026-06-23):** Remotion-Composition `AdVideo` (9:16, 1080×1920, 6 s @ 30 fps) gebaut —
Eyebrow/Headline/Subline fade-up, CTA spring-in + dezenter Puls, Akzent-Leiste, Brand oben, Content im
sicheren Bereich (untere 35 % frei), Brand-Tokens + Content als Props (multi-projekt). **Composition
visuell validiert** via `remotion still` (Frame 75): identisch sauber wie die Bild-Ad (Umlaute,
Brand-Farben, Safe-Zone). MP4-Render scheiterte zunächst an „localhost:3000 got no response"
(Port/Pool) → Fix: `--concurrency=1 --port=3333`. Geteilter Web-Tech-Kern mit Bild-Modul (gleiche
Safe-Zone-/Brand-Logik) bestätigt.
**Offen:** finaler MP4-Render-Lauf (läuft), Lizenz-Caveat-Entscheidung, Voiceover/Avatar als Folge-Ticket.
