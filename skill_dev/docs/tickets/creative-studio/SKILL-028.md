# SKILL-028: creative-studio — KI-Disclosure-Gate („KI"-Label + C2PA/Metadaten auf KI-Creatives)

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** jedes_ki_creative_traegt_disclosure (Label + Metadaten bei KI-Bild ODER synthetischer Stimme) + rechtskonform_ab_02_08_2026 (EU-AI-Act + Meta-Policy)
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_ki-avatare-voiceover.md` (§3 Pflicht-Disclosure: Meta 2026 „AI-generated" inkl. synthetischer Voiceovers; EU-AI-Act ab 02.08.2026: sichtbares Label „KI" + maschinenlesbare Metadaten; Strafrahmen bis 3 % Jahresumsatz/15 Mio. €)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> Sobald KI ein Creative **generiert/substanziell veraendert/composited** hat — explizit inkl.
> synthetischer Voiceovers — ist eine sichtbare KI-Kennzeichnung Pflicht (Meta-Policy + EU-AI-Act ab
> 02.08.2026). „Undisclosed AI Content" ist 2026 der drittgroesste Meta-Ablehnungsgrund (~14 %). Die Marke
> haftet fuer die sichtbare Offenlegung, der Tool-Anbieter fuer die Metadaten. Das gehoert als
> **Pflicht-Constraint** in den Skill, nicht in jede Projekt-Pipeline einzeln.

## Was soll erreicht werden? (Business-Ziel)
Ein Disclosure-Gate, das auf **jedem** Creative mit KI-generiertem Bild ODER synthetischer Stimme
automatisch ein sichtbares „KI"-Label setzt und C2PA-/Metadaten schreibt — als Constraint/Pflichtfeld im
`specs.py`-Set und als Render-Overlay. Projektneutral, EU-AI-Act- und Meta-Policy-konform.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1 (Bild):** When ein Creative ein KI-generiertes Bild ODER eine synthetische Stimme (SKILL-027) enthaelt,
      the system shall ein sichtbares **„KI"-Label** als Render-Overlay setzen (Bild + Video).
      → **Bild erledigt:** `ad_image.html.j2` rendert bei `ai_disclosure=True` ein dezentes `.ai-label`
      (untere Ecke, innerhalb seitlicher + oberhalb unterer Safe-Zone, halbtransparent). **Video-Overlay
      (`AdVideo.tsx`) bleibt offen** — paralleler Subagent / Folgeschritt (video/ war hier out-of-scope).
- [ ] **EARS-2:** When ein KI-Creative exportiert wird, the system shall **C2PA-/Metadaten** (maschinenlesbare
      Herkunfts-Kennzeichnung) in die Ausgabedatei schreiben.
      → **Folgeschritt — NICHT in diesem Ticket implementiert.** Das Metadaten-Schreiben gehoert in den
      Renderer (`render_image.py`), der hier bewusst NICHT angefasst wurde. Konzept siehe „Metadaten-Teil"
      unten. Hier nur Flag + sichtbares Label + Pflicht-Warnung. **Nicht gefaket.**
- [x] **EARS-3:** When der KI-Anteil als Flag/Constraint im `AdContent`/Spec-Set gesetzt ist, the system shall
      das Disclosure-Gate als **Pflichtfeld** behandeln (kein KI-Creative ohne Disclosure-Entscheidung) —
      Default „KI-Anteil = ja" wenn ein KI-Asset (Bild/Stimme) im Lauf war.
      → `requires_ai_disclosure(content)` + Pflicht-Warnung in `AdContent.warnings()`, wenn KI-Element
      gesetzt aber `disclosure_applied=False`. Reine Warnung (Mensch-im-Loop), keine harte Sperre.
- [x] **EARS-4:** When ein Creative **rein** aus echtem Eigen-Material besteht (kein KI-Bild, keine
      synthetische Stimme), the system shall **kein** Label/Metadaten erzwingen (nur echte KI-Anteile triggern).
      → `ai_image`/`ai_voice` default `False`; saubere `AdContent` erzeugt keine Disclosure-Warnung,
      Template rendert kein Label.
- [x] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall die
      Disclosure-Regel projektneutral als Constraint im `specs.py`-Set halten (kein projekt-spezifischer
      Label-Text/Pfad hartkodiert; Label-Text als Parameter mit Default „KI").
      → `AI_LABEL_TEXT = "KI-generiert"` als projektneutraler Default; Template-Variable `ai_label_text`
      ueberschreibbar (z. B. „KI"). Kein Brand-/Projektwert hartkodiert.

## Technische Hinweise
- `specs.py`: neues Constraint/Flag (z. B. `ai_generated: bool` im Content-/Job-Set + Label-Default „KI").
- Render-Overlay: Bild-Template (`ad_image.html.j2`) + Video-Composition (`AdVideo.tsx`) bekommen ein
  Disclosure-Element (Safe-Zone-konform platziert).
- C2PA-Metadaten: beim Export schreiben (Bild via Pillow/exif/c2pa-Tooling; Video via Metadaten-Step nach
  Remotion-Render). Genaue Tool-Wahl im Implementer-Pass.
- Kopplung: SKILL-027 (synthetische Stimme) und ein kuenftiges Avatar/KI-Bild-Feature setzen das Flag.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — Disclosure-Constraint/Flag + Label-Default.
- `skills_sources/creative-studio/templates/ad_image.html.j2` — „KI"-Overlay (Bild).
- `skills_sources/creative-studio/video/src/AdVideo.tsx` — „KI"-Overlay (Video).
- `skills_sources/creative-studio/creative_studio/render_image.py` / `video/`-Render — C2PA-/Metadaten-Step.
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_ki-avatare-voiceover.md` (§3).

## Metadaten-Teil (C2PA / PNG-tEXt) — Konzept, Folgeschritt

> [!note] Metadaten-Schreiben = Folgeschritt in `render_image.py` (hier bewusst NICHT implementiert)
> Sichtbares Label deckt die Marken-Haftung ab; die **maschinenlesbaren Metadaten** sind der zweite,
> separat haftende Teil (Tool-Anbieter-Seite des EU-AI-Act). Geplant, aber NICHT Teil dieses Tickets,
> weil es `render_image.py` anfasst (ausgeschlossen — paralleler Subagent):
>
> - **PNG (Bild-Export):** beim Schreiben der PNG einen `tEXt`/`iTXt`-Chunk setzen, z. B.
>   `ai_generated=true` (+ optional `ai_elements=image,voice`, `disclosure=KI-generiert`). Pillow:
>   `PngImagePlugin.PngInfo().add_text("ai_generated", "true")` → `img.save(..., pnginfo=info)`.
> - **C2PA / Content Credentials:** vollwertige, signierte Herkunfts-Manifeste via `c2pa`-Tooling
>   (Content Authenticity Initiative). Schwergewichtiger; PNG-`tEXt` ist der pragmatische Interim-Schritt.
> - **Video:** Metadaten-Step nach dem Remotion-Render (z. B. ffmpeg-Metadaten-Tags) — eigener Folgeschritt.
>
> Hook für den Renderer: `render_image.py` speist die Template-Variable `ai_disclosure` aus
> `specs.requires_ai_disclosure(content)` und schreibt im gleichen Schritt den PNG-Metadaten-Chunk.

## Ergebnis / Notizen

**Abgeschlossen 2026-06-24 (Status: review).** Additiv, keine bestehende Funktion gebrochen.

**Was ergänzt (nur additiv):**
- `creative_studio/specs.py`:
  - `AdContent`-Felder `ai_image: bool = False`, `ai_voice: bool = False`, `disclosure_applied: bool = False`.
  - Helper `requires_ai_disclosure(content) -> bool` (True bei `ai_image` oder `ai_voice`).
  - Konstanten `AI_LABEL_TEXT = "KI-generiert"`, `AI_ACT_ENFORCEMENT_DATE = "2026-08-02"`.
  - `AdContent.warnings()` additiv: Pflicht-Hinweis (sachlich, mit EU-AI-Act-Stichtag) wenn KI-Element
    gesetzt aber `disclosure_applied=False`.
- `templates/ad_image.html.j2`:
  - Bei `ai_disclosure=True`: kleines, dezentes, halbtransparentes `.ai-label` in der **unteren rechten Ecke**,
    `bottom: var(--safe-bottom)` + `right: var(--safe-x)` → innerhalb der seitlichen und oberhalb der unteren
    Safe-Zone, von der Meta-UI nicht verdeckt. Wortlaut via `ai_label_text` (Default „KI-generiert", auf „KI"
    überschreibbar). Ohne Flag: Template unverändert.
- `tests/test_skill_028_disclosure.py`: 13 Tests (EARS-1/3/4/5 + Template-Render mit/ohne Flag + Regression).

**Test-Ergebnis:** `pytest tests/test_skill_028_disclosure.py -q` → **13 passed in 0.11s** (grün).

**Wie das Label aussieht / positioniert ist:** kleine abgerundete Pille, dunkel-halbtransparenter Hintergrund
(`rgba(10,14,39,0.55)`, opacity 0.85), weißer fetter Text ~1.6 % der Canvas-Höhe, untere rechte Ecke innerhalb
der Safe-Zonen. Dezent sichtbar, ohne das Creative-Layout zu stören.

**Offen / Folgeschritt:** (a) **C2PA-/PNG-tEXt-Metadaten-Schreiben** (EARS-2) im Renderer `render_image.py`
(Konzept oben). (b) **Video-Overlay** `AdVideo.tsx` (EARS-1 Video-Teil). Beide bewusst out-of-scope hier
(render_image.py + video/ nicht angefasst — Konfliktvermeidung mit Parallel-Subagent).

**Code-Referenzen:**
- `skills_sources/creative-studio/creative_studio/specs.py` (Marker `# SKILL-028:`)
- `skills_sources/creative-studio/templates/ad_image.html.j2` (Marker `SKILL-028`)
- `skills_sources/creative-studio/tests/test_skill_028_disclosure.py`
