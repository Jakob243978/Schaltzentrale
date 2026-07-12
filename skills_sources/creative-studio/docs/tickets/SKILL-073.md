# SKILL-073: creative-studio — Bildquellen-Modul (Magnific Stock + KI-Gen) mit search-first + Disclosure

**Status:** review
**Erstellt:** 2026-07-08
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** bild_beschaffung_im_skill_projektneutral (kein „Bild fehlt") + kein_doppel_spend_durch_search_first + ki_disclosure_automatisch_verdrahtet
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/scripts/magnific.py` (bestehender Magnific/Freepik-Client
+ Bild-Bibliothek `marketing/bild-bibliothek/index.json`); SKILL.md §7-Grenze „Foto-Hintergruende";
SKILL-028 (KI-Disclosure-Gate). Magnific-API: Header `x-magnific-api-key`, Base
`https://api.magnific.com/v1`, Stock-Filter Array-Syntax (`filters[content_type][]=photo`,
`filters[people][]=exclude`), KI-Gen `POST /v1/ai/mystic` async + poll.

> [!info] Herkunft (Jakob-Auftrag „Skill ausbauen" + SKILL-072-Bedarf)
> Die foto-getriebenen Layout-Archetypen aus SKILL-072 (photo-poster/object-hero) brauchen
> **Bilder**. Statt „Bild fehlt" soll der Skill selbst passende Hintergruende ziehen/generieren.
> Der bestehende Projekt-Client `magnific.py` (AgentischesArbeiten) wird ins Skill-Source
> gehoben und **projektneutral** gemacht (Lift-and-Shift, Prinzip skill-muss-multi-projekt-tauglich).

## Was soll erreicht werden? (Business-Ziel)
Der Skill zieht/generiert automatisch passende Hintergruende (Stock gratis, KI nur explizit)
und speist sie in den bestehenden Render-Pfad — projektneutral, ohne Doppel-Spend, mit
automatischer KI-Kennzeichnung.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1 [multi-projekt]:** the system shall API-Key + Bibliothekspfad ueber Env/Config
      aufloesen (`MAGNIFIC_API_KEY`, `CREATIVE_STUDIO_IMAGE_LIB`) — **kein** hartkodierter
      `marketing/…`-Pfad, **kein** Repo-Root-`.env`. Key wird nie geloggt.
- [x] **EARS-2:** When ein Bild aufgeloest wird, the system shall ZUERST die lokale Bibliothek
      (`index.json`) durchsuchen (search-first), bevor es zieht/generiert — kein Doppel-Download/-Spend.
- [x] **EARS-3:** When `--bg-source {none,library,stock,generate}` gesetzt ist, the system shall
      das Ergebnis in `content.bg_image` fuettern → durch den bestehenden Smartcrop (SKILL-032) +
      Template — **kein** neuer Render-Pfad.
- [x] **EARS-4:** When ein KI-generierter Hintergrund (`source=magnific-gen`/`is_ai_generated`)
      verwendet wird, the system shall `content.ai_image=True` setzen → das bestehende
      `requires_ai_disclosure()`-Gate (SKILL-028) rendert das sichtbare „KI-generiert"-Label.
- [x] **EARS-5:** the system shall `license_type` + `license_url` als Pflichtfelder jedes
      Index-Eintrags erzwingen (Eintrag ohne Lizenz wird abgelehnt); `--no-people` (Default)
      bevorzugt personenfreie Bilder (Paid-Ads).
- [x] **EARS-6:** When `generate` gewaehlt ist, the system shall NUR dann KI generieren (kostet
      Geld) — `library`/`stock` sind die guenstigen Defaults (kein Silent-Spend).

## Loesungs-Skizze (Approach)
- **`creative_studio/image_source.py`** (Lift + generalisiert): `library_dir()`/`load_key()`
  (Env/Config, kein Hardcode), `load_index`/`add_entry` (+`_require_license` Gate),
  `resolve_entry_path` (robust ggü. lib-relativen **und** legacy repo-relativen `local_path`),
  `search_library` (Token-Overlap, personenfrei-Bevorzugung, keine toten Verweise),
  `stock_search`/`stock_download`, `generate` (Mystic async poll), **`resolve_bg()`** (search-first)
  + `BgResult`. Standalone-CLI.
- **`render_image.py`:** CLI `--bg-source/--bg-query/--image-lib/--no-people/--allow-people`;
  `resolve_bg()`-Aufruf VOR dem Render, Ergebnis → `content.bg_image`; KI-Herkunft →
  `content.ai_image=True` + `disclosure_applied=True`. Ausserdem: `build_html()` verdrahtet jetzt
  `ai_disclosure`/`ai_label_text` in den ECHTEN Render-Pfad (bisher nur im Test).
- **Verworfen:** Modul ruft das Meta-/LLM-Vision selbst — nein (Muster wie ad_library.py: der
  Agent IST das Modell; Vision-Caption ist dokumentierte Phase-2, nicht gebaut).

## Test-Ergebnis
- `tests/test_skill_073_image_source.py` — **14 passed** (offline, kein Netzwerk): Env/Param-Config,
  search-first Cache-Hit, source=none/library-ohne-Treffer → None, Lizenz-Gate, KI-Flag,
  Legacy-repo-relativer Pfad, kein toter Verweis, Projektneutralitaet.
- Gesamt-Suite **264 passed**, keine Regression.
- **Live-Beleg (sparsam, 1 Stock-Download, KEINE KI-Gen):** `resolve source=stock` lud 1 Bild
  (`58595353.jpg`, Lizenz premium, `cache=False`) in eine Wegwerf-Bibliothek; zweiter Aufruf
  **ohne** Key → `cache=True`, **kein** zweiter Download (search-first belegt).
- **Render-Beleg:** `--bg-source library` gegen die bestehende AgentischesArbeiten-Bibliothek
  (legacy Pfade): photo-poster mit Stock-Desk-Foto; template mit dem **KI-generierten** Office-BG
  → sichtbares „KI-generiert"-Label im PNG (Disclosure-Gate end-to-end).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/image_source.py` — **neu** (Lift von
  `AgentischesArbeiten/scripts/magnific.py`, projektneutral).
- `skills_sources/creative-studio/creative_studio/render_image.py` — `--bg-source`-Verdrahtung,
  `resolve_bg`-Aufruf, `ai_disclosure`/`ai_label_text` im Render-Pfad, `_bg_query_from_content`.
- `skills_sources/creative-studio/tests/test_skill_073_image_source.py` — 14 Tests.
- `skills_sources/creative-studio/SKILL.md` — Abschnitt 13 + §7-Grenze aktualisiert.

## Ergebnis / Notizen
**Status review (2026-07-08).** search-first + Lizenz-/Kosten-Gate + KI-Disclosure end-to-end
verdrahtet; kein hartkodierter Projektpfad. `setup.ps1` gelaufen.

**Offen / [J]:** Verify-Pass (frische Session) + Outcome-Review. **Magnific-Pricing/Lizenz [J]:**
Stock-Freikontingent (~100/Tag) + Premium-Lizenz-Bedingungen (`license_url` je Bild) und die
KI-Gen-Kosten pro Bild sind noch nicht offiziell dokumentiert/geprueft — vor Serien-Nutzung
klaeren (Stock-Nutzungsrechte fuer Paid-Ads, KI-Gen-Credits/Budget-Cap). Kein Auto-`generate`
im Produktivlauf ohne explizite Freigabe.
