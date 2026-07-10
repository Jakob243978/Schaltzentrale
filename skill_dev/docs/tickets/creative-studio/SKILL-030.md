# SKILL-030: creative-studio — Vorschau-Galerie gallery.html (QA-Gate vor Launch)

**Status:** review
**Erstellt:** 2026-06-23
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** menschliche_sichtfreigabe_vor_launch (alle Varianten × Formate auf einen Blick) + galerie_liest_manifest_json
**outcome_review_at:** null
**Wissensgrundlage (Recherche 2026-06-23, AgentischesArbeiten/docs/marketing/research/):**
`2026-06-23_creative-studio-flow-improvements.md` (§2.3 Vorschau/QA, §2.6 Mensch-im-Loop, §3.6 Vorschau-Galerie; MoSCoW-Liste #6 = Should)

> [!info] Herkunft (Recherche 2026-06-23 + Jakob-Auftrag „Skill ausbauen, Tickets anlegen")
> Vor dem Launch braucht es eine **Vorschau-Galerie** aller Varianten × Formate an einem Ort fuer schnelle
> menschliche Sichtfreigabe (Safe-Zone-/Caption-/Lesbarkeits-Check). Das bestehende `--debug-safe` ist nur
> der Baustein; es fehlt die aggregierte Galerie. Passt zu Jakobs Prinzip „Claude generiert, Mensch gibt
> visuell frei" (Recherche §2.6). Die Galerie liest das `manifest.json` aus SKILL-023.

## Was soll erreicht werden? (Business-Ziel)
Eine `gallery.html`, die **alle Varianten eines Jobs** (alle Hooks × Formate × Medien) nebeneinander
rendert — als QA-Gate fuer die visuelle Sichtfreigabe durch den Menschen, bevor Ads live gehen. Sie liest
das `manifest.json` und ist projektneutral (kein hartkodierter Pfad).

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When ein Job-Lauf ein `manifest.json` erzeugt hat, the system shall eine `gallery.html`
      rendern, die **alle** im Manifest gelisteten Varianten × Formate (Bild + Video) anzeigt.
- [x] **EARS-2:** When die Galerie eine Variante anzeigt, the system shall die Manifest-Metadaten je Kachel
      ausweisen (`variant_id`, `framework`, `hook`, `format`, `utm_content`) — fuer nachvollziehbare Freigabe.
- [x] **EARS-3:** When der Mensch die Galerie oeffnet, the system shall sie als reines lokales HTML-Artefakt
      bereitstellen (per Doppelklick/file:// oeffenbar, kein Server noetig).
- [x] **EARS-4 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall den
      Manifest-/Galerie-Pfad relativ zum Job-Ordner aufloesen (kein hartkodierter Projektpfad).
- [x] **EARS-5:** When eine Variante im Manifest als fehlgeschlagen markiert ist (SKILL-023 EARS-5), the
      system shall sie in der Galerie sichtbar als Fehler kennzeichnen (statt sie still wegzulassen).

## Technische Hinweise
- Generator `creative_studio/gallery.py` (oder Jinja2-Template `templates/gallery.html.j2`): liest
  `manifest.json`, baut ein Grid aus `<img>`/`<video>` + Metadaten-Caption.
- Reines statisches HTML (file://-tauglich, analog Jakobs LP-Test-Praxis). Keine Server-Abhaengigkeit.
- Optionaler Ausbau (separat, nicht in diesem Ticket): `ads_get_ad_preview`-Integration als echter
  Placement-Check.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/gallery.py` — **neu** (Manifest → gallery.html).
- `skills_sources/creative-studio/templates/gallery.html.j2` — **neu** (Galerie-Template).
- `skills_sources/creative-studio/creative_studio/batch.py` — liefert `manifest.json` (SKILL-023).
- Wissensgrundlage: `AgentischesArbeiten/docs/marketing/research/2026-06-23_creative-studio-flow-improvements.md` (§2.3, §2.6, §3.6).

## Ergebnis / Notizen

**Umgesetzt am 2026-06-24 (Status spec → review).**

### Implementierung
- **Neu:** `skills_sources/creative-studio/creative_studio/gallery.py` — liest `manifest.json`
  (SKILL-023-Schema) und erzeugt eine **standalone `gallery.html`** im selben Ordner
  (relative Bildpfade aus `file`, file://-tauglich, kein Server). Code-Kommentare `# SKILL-030:`.
  - CSS ist inline im `<style>` -> die Galerie ist eine einzige transportable Datei. Kein Jinja2-Template
    noetig (HTML wird in Python gebaut, da statisch + selbst-enthalten) — `templates/gallery.html.j2`
    bewusst NICHT angelegt.
  - **Markenkonform-schlicht** in Anlehnung an `templates/ad_image.html.j2` (dunkler Grund #0a0e27,
    Akzent #4f7cff, System-Font-Stack fuer zuverlaessige Umlaute).
  - Je Kachel: Bild + `variant_id`, `framework`, `format`, `hook`, `media`-Badge, `utm_content`.
  - **Warnungen** (Manifest-Feld `warnings`) gelb (`.flag.warn`, `.has-warn`), **Fehler** (`error`) und
    **`status: not_implemented`** rot (`.flag.error`, `.has-error`) sichtbar markiert (EARS-5) — nichts
    wird still weggelassen (Video-not_implemented erscheint ebenfalls als rote Kachel).
  - **Robust:** fehlende Bilddatei -> `<img onerror>`-Fallback auf Platzhalter "Bild nicht gefunden",
    kein Crash.
  - **Gruppierung umgesetzt** (das in der Spec als „Plus" genannte Feature): Default `--group-by format`
    (auch `framework`/`media` oder `''` fuer keine Gruppen). Jede Format-Sektion mit Ueberschrift + Count.
  - CLI: `python -m creative_studio.gallery --manifest <pfad/manifest.json> [--out gallery.html] [--group-by format]`.
- **Konfliktvermeidung eingehalten:** NUR neue Dateien angelegt. `specs.py`, `render_image.py`,
  `batch.py`, `frameworks.py`, `assets.py`, `prep_bg.py`, `video/` unveraendert (nur gelesen).

### Tests
- **Neu:** `tests/test_skill_030_gallery.py` — 8 Tests aus einem Mini-Manifest (OK / warning / error /
  not_implemented-Video). HTML-String-Assertions: alle `variant_id`s + `utm_content=...`, `flag error`/
  `has-error` (rot), `flag warn`/`has-warn` (gelb), `not_implemented`, standalone-DOCTYPE + relativer
  `src="...png"`, `onerror`-Fallback, Format-Gruppierung, CLI-`main()`.
- **Ergebnis:** `pytest tests/test_skill_030_gallery.py` → **8 passed**. Gesamtsuite **57 passed**.
- **Beleg:** generierte `gallery.html` aus 4-Eintrag-Manifest = **6093 bytes** (eine Datei, alle Assets inline).

### Code-Referenzen
- `skills_sources/creative-studio/creative_studio/gallery.py` (neu)
- `skills_sources/creative-studio/tests/test_skill_030_gallery.py` (neu)
- liest `manifest.json` aus `skills_sources/creative-studio/creative_studio/batch.py` (SKILL-023)

### Offen
- Kein Deploy ausgefuehrt (`setup.ps1` separat noetig, damit die Galerie im laufenden Skill landet).
- Optionaler Ausbau (separat, nicht in diesem Ticket): `ads_get_ad_preview`-Placement-Check.
