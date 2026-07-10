# creative-studio

Erzeugt markenkonforme **Social-Ad-Creatives (Bild + Video)** fuer Meta (Facebook/Instagram)
aus **Content + Brand-Tokens** — Safe-Zone-korrekt, Multi-Format, projektuebergreifend.

## Was der Skill ist

- **Bild** (`creative_studio/render_image.py`): HTML/CSS-Template (Jinja2) wird live ueber
  **Playwright** (headless Chromium) zu PNG gerendert — ein Aufruf pro Format.
- **Video** (`video/`): animierte 9:16-Ad-Composition mit **Remotion** (React -> MP4).
- **Standards als Code** (`creative_studio/specs.py`): Formate, Safe-Zones und technische
  Constraints von Meta liegen zentral als Code vor — **Single Source of Truth**, von Bild-
  und Video-Modul gemeinsam genutzt.

## Multi-Projekt

Der Skill enthaelt **keine** projekt-spezifischen Werte (kein Brand-Hex, kein Pfad, kein
Copy-Text). Brand-Tokens kommen zur Laufzeit ueber `--brand-env` (Bild) bzw. Props (Video),
Content ueber CLI-Args bzw. JSON. So ist derselbe Skill in mehreren Projekten nutzbar
(z. B. AgentischesArbeiten, SocialMediaBuilder).

## Abgrenzung

Der Skill **erzeugt Creatives** — er bucht oder schaltet **keine** Ads. Das Ausspielen
(Kampagne/Ad-Set/Creative-Upload) uebernimmt z. B. der MetaAdsAgent ueber das Meta-MCP.

## Aktivierung

Siehe `SKILL.md` (Trigger, CLI-Beispiele, Standards, Multi-Projekt-Nutzung, Grenzen).

## Methodik / Herkunft

Skill-Tickets: `skill_dev/docs/tickets/creative-studio/SKILL-020.md` (Bild) +
`SKILL-021.md` (Video). Vision-Grundlage: `skill_dev/docs/SKILLS_VISION.md`
(Prinzip: Skill muss multi-projekt-tauglich sein).
