# video/public/ — Remotion-Asset-Staging

Remotion-Render akzeptiert **keine** rohen `file://`-URLs — lokale Assets
(B-Roll-Clips, Musik, Voiceover) muessen aus `public/` ueber `staticFile()`
serviert werden. `AdReel.tsx` (`resolveSrc`) wandelt relative Spec-`src`-Werte
automatisch in `staticFile(...)` um; absolute `http(s)://`/`data:`-URLs bleiben
unveraendert.

## Konvention

- Lege Render-Assets unter `public/assets/` ab (z.B. aus dem **Silber**-Tier
  kopierte Transcodes + lizensierte Musik).
- Referenziere sie in der Reel-Spec per relativem Pfad, z.B.:
  `"broll": [{ "src": "assets/clip01.mp4", "seconds": 2.0 }]`,
  `"music": "assets/music.mp3"`.
- **`public/assets/` ist gitignored** (grosse Medien gehoeren nicht ins Repo;
  Brand-Asset-Originale-Regel). Lokal reproduzierbar via Silber-Transcode.

## Medallion-Tiers (Output-Strategie)

- **Bronze** = Rohmaterial (extern, read-only).
- **Silber** = Transcodes/Arbeits-Clips (extern).
- **Gold** = fertig geschnittenes Reel (extern).
- **Repo** = nur winzige Proof-Artefakte (`tests/artifacts/`, < 2 MB), nie das
  fertige Reel.
