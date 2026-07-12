---
name: creative-studio
description: Erzeugt markenkonforme Social-Ad-Creatives (Bild + Video) fuer Meta (FB/IG) aus Content + Brand-Tokens — Safe-Zone-korrekt, Multi-Format, projektuebergreifend. Aktivieren, wenn der User Ad-/Social-Creatives, Werbebilder, Reels-/Story-Ads, eine "Bild-Ad" oder "Video-Ad generieren" oder Meta-Ads-Creatives will. Bild = Playwright/HTML-CSS, Video = Remotion (9:16). Standards (Formate/Safe-Zones/Constraints) zentral in specs.py. Brand + Content kommen als Parameter — kein hartkodierter Projektwert.
---

# creative-studio

## 1. Wann aktivieren

Aktiviere diesen Skill, wenn der User eines davon will:

- Social-Ad-Creatives / Werbebilder fuer Meta (Facebook, Instagram)
- "Bild-Ad generieren" / "Video-Ad generieren" / Meta-Ads-Creatives
- Reels-Ads, Story-Ads, Feed-Ads (4:5 / 9:16 / 1:1)
- markenkonforme Werbe-Visuals aus Copy/Headline/CTA + Brand-Farben

## 2. Was der Skill liefert (und was nicht)

**Liefert:** fertige Creative-Dateien — PNG-Bilder (mehrere Formate aus EINER Vorlage)
und ein 9:16-MP4-Video. Safe-Zone-korrekt, deutschsprachig (Umlaute), markenkonform
ueber Brand-Tokens.

**Abgrenzung:** Der Skill **bucht oder schaltet keine Ads**. Das Ausspielen
(Kampagne/Ad-Set/Creative-Upload) macht ein Ads-Agent (z. B. MetaAdsAgent ueber das
Meta-MCP). Hier entsteht nur das Creative-Asset.

> [!important] Standard-Ad-Satz = IMMER alle VIER Bild-Typen (zum A/B-Testen)
> Fuer **ein Ad-Set** erzeugt der Skill per **Default alle vier Bild-Typen parallel** —
> genau wie er per Default alle drei Formate rendert (Abschnitt 3/5, SKILL-076). Die vier
> Typen testen unterschiedliche visuelle Sprachen gegeneinander (welche zieht):
>
> 1. **Text-only** — reine Typo/Brand-Flaeche, kein Bild (`--bg-source none`, Default;
>    Layout `template` oder `stat-hero`, `--chrome minimal` fuer den organischen Look).
> 2. **Eigene Fotos / Brand-Assets** — echtes Projekt-/Personen-Foto als Motiv
>    (`--bg-image <brand-foto>` oder `--bg-source library` auf die Projekt-Bibliothek;
>    Layout `photo-poster`/`object-hero`).
> 3. **Stock** — echtes Stock-Foto, **keyless** ueber Openverse (CC, kommerziell nutzbar) —
>    `--bg-source stock` (Abschnitt 13). Kein API-Key/User-Setup noetig.
> 4. **KI-generiert** — ueber Magnific/Mystic (`--bg-source generate`, kostet Geld, explizit;
>    loest automatisch das sichtbare „KI-generiert"-Label aus, Abschnitt 13).
>
> **Soll/Default:** immer **alle vier** Typen, **jeder in allen drei Formaten** (also
> 4 × 3 = 12 Creatives pro Ad-Satz). Eine kleinere Auswahl **nur auf ausdruecklichen
> Wunsch** des Users. Jedes gerenderte PNG durchlaeuft danach den Vision-QA-Pass
> (Abschnitt 15) — **pro Typ und pro Format einzeln**.

> [!important] Standard-Ad-Satz = Creatives PLUS Ad-Copy-Sheet PLUS Ad-Report (SKILL-100)
> Ein Ad-Satz ist erst „fertig", wenn neben den Creatives (PNG) **zwei Text-Deliverables**
> entstehen. Ohne sie ist der Satz unvollstaendig:
> 1. **`ad-copy.md`** — veroeffentlichungsfertige Meta-Copy je Hook: Topline · Headline · Subline ·
>    **CTA-Button** · Headline-Feld · Beschreibung · `utm_content` · Ziel-URL · Primaertext
>    (A Langform, B Kurz) + Mapping-Tabelle. Vorlage: `docs/templates/ad-copy-sheet.md`.
> 2. **`ad-report.html`** — self-contained Review-/Launch-Report: Karten-Grid je Ad, Klick-Modal
>    mit allen Formaten + voller Copy, Uebersicht, Metrik-Sektion (Post-Launch-Platzhalter).
>    **Review-Workflow (SKILL-103):** Status je Ad (`draft` Default · `pending` · `passed` · `declined`)
>    + Feedback-Feld, persistent (localStorage + „Als HTML sichern" mit eingebettetem `reviewState`-JSON),
>    Filter nach Status. Der zurueckgegebene State ist Arbeitsauftrag: nur `declined`/kommentierte Ads
>    ueberarbeiten. Referenz: `AgentischesArbeiten/marketing/ad-creatives/ad-report.html`.

> [!important] Ad-Copy-Voice = Workshop-Brand „How You Sound" (SKILL-101), verbindlich
> Copy klingt **direkt, energetisch, motivierend, nahbar, mutig** — NICHT nach Angst, Buzzwords,
> belehrend, Toolnamen. **Emotionsraum statt Angst** (nach vorne: Wachstum/Freiheit/Begeisterung,
> nie Pain-/Angst-Lead). **Wachstum verkaufen, nicht Entlastung.** „du", nie „Geschaeftsfuehrer",
> „individueller" statt „komplizierter". **„KI" nur als konkrete Loesungsbenennung**, nicht als Buzz.
> Gesprochen/menschlich, keine Floskeln, keine Gedankenstriche, Komma nur wo grammatisch noetig.
> **Dramaturgie:** Topline = Auftakt (kein Zielgruppen-Label) · Headline = konkrete Wunsch-/Pain-Szene
> (kurz, vollstaendig, **face-safe**) · Subline = Mehrwert (Bislang … ab jetzt …) · **CTA = Button
> mit Handlungs-Aufforderung + Zeit/Ort** (SKILL-102, `--cta-button`). Die konkreten Voice-Adjektive/
> Leitplanken kommen aus der Brand (Parameter/Doku), nicht hartkodiert.

> [!important] Foto-Ads: Text nie ueber dem Gesicht (SKILL-102)
> Bei `photo-poster` mit Founder-/Personen-Foto darf kein Text ueber dem Gesicht liegen. Kurze
> Headlines halten den bottom-anchored Textblock unter dem Gesicht; der Vision-QA-Pass (Abschnitt 15)
> prueft es je Format. KI-generierte Motive tragen das „KI-generiert"-Overlay nur, wenn es der
> Brand/Kunde will (steuerbar; Provenienz bleibt im `index.json` ehrlich, unabhaengig vom Overlay).

## 3. Bild generieren

Voraussetzung (einmalig):

```bash
pip install playwright jinja2
python -m playwright install chromium
```

Aufruf (aus dem Skill-Verzeichnis, Modul-Form):

```bash
python -m creative_studio.render_image \
  --headline "Verdoppeln <span class='hl'>ohne doppeltes Team</span>" \
  --subline "Agentisches Arbeiten fuer Immobilien-Unternehmer." \
  --eyebrow "MENTORING · WARTELISTE" \
  --cta "Auf die Warteliste" \
  --brand "JAKSE-Automations" \
  --brand-env ../AgentischesArbeiten/branding.env \
  --ad-id h1-immo \
  --out ./out
```

`--formats` weggelassen → Default = **alle drei Standard-Formate** (1:1, 4:5, 9:16, SKILL-076).

Wichtige Optionen:

- `--formats` — Komma-Liste aus `square_1x1`, `feed_4x5`, `story_9x16`
  (Default: `square_1x1,feed_4x5,story_9x16` — **alle drei Standard-Formate**, SKILL-076).

> [!important] Standard = IMMER alle drei Formate (1:1, 4:5, 9:16)
> Wird `--formats` **nicht** gesetzt, rendert der Skill per Default **alle drei** Meta-Standard-
> Formate: **1:1** (1080×1080, Feed square), **4:5** (1080×1350, Feed portrait) **und** **9:16**
> (1080×1920, Story/Reels). Das ist das **Soll fuer jede Ad** — eine kleinere Liste nur, wenn der
> User ausdruecklich weniger will. **4:5 ist Metas Feed-Portrait-Default 2026 und darf nie
> stillschweigend fehlen** (Anlass: Workshop-Ads kamen nur als 1:1 + 9:16 raus, 4:5 fehlte
> komplett, weil die Formate explizit ohne 4:5 angefragt wurden). Der Vision-QA-Pass (Abschnitt 15)
> gilt danach **pro Format einzeln** — also auch das 4:5 wird separat angesehen.
- `--brand-env <pfad>` — Pfad zu `branding.env` mit den Brand-Tokens (siehe Abschnitt 6).
  Fehlt die Datei/ein Key, greifen interne Fallback-Defaults.
- `--bg-image <pfad|url>` — optionales Hintergrundmotiv (wird mit Lesbarkeits-Overlay
  ueberlagert). Ohne Angabe wird der Brand-Gradient verwendet.
- `--ad-id <id>` — bestimmt den Datei-Stamm (`<ad-id>__<format>.png`).
- `--debug-safe` — blendet die Safe-Zonen rot ein (Sichtpruefung, dass Text/Logo/CTA
  nicht in verdeckte Bereiche ragen).

Headline darf Inline-HTML enthalten (`<span class="hl">…</span>` faerbt den Teil in der
Akzentfarbe). Ausgabe: ein PNG pro Format unter `--out`.

Fuer **Scroll-Stop-Layouts** (Riesenzahl-Held, Cream-Theme, minimal Chrome, Foto-Poster)
siehe Abschnitt 12 (`--layout` + Stil-Parameter) und Abschnitt 13 (automatische
Bildbeschaffung `--bg-source`). Default-Aufruf bleibt unveraendert.

## 4. Video generieren

Voraussetzung (einmalig):

```bash
cd video && npm install
```

Render (9:16, MP4):

```bash
cd video
npx remotion render src/index.ts AdVideo ./out/ad.mp4
```

Brand-Tokens und Content ueberschreiben (Multi-Projekt) ueber `--props` als JSON:

```bash
npx remotion render src/index.ts AdVideo ./out/ad.mp4 \
  --props '{"headline":"Verdoppeln","headlineAccent":"ohne doppeltes Team","eyebrow":"MENTORING · WARTELISTE","subline":"Plaetze sind begrenzt.","cta":"Auf die Warteliste","brandName":"JAKSE-Automations","accent":"#f25d3e","bg":"#0a0e27","bgSoft":"#11163a","ink":"#faf7f2","inkMuted":"#9a9ec0","font":"-apple-system, sans-serif"}'
```

Ohne `--props` rendern die Default-Props der Composition (h1-immo / Brand) aus
`video/src/Root.tsx`. Format: 1080x1920, 30 fps, 180 Frames (6 s).

### 4a. Reel-Composition `AdReel` (Captions + Audio + dyn. Dauer)

Neben der statischen `AdVideo`-Title-Card gibt es die **Reel-Engine** `AdReel`
(SKILL-043/044/045): dieselbe Title-Card als Basis-Layer **plus** burned-in
word-level Captions (Hormozi-Stil), Voiceover-/Musik-Track mit Ducking und
**dynamischer Dauer** (aus Spec/Audio/Captions abgeleitet, nicht fix 180 Frames).

Eingabe ist eine **Reel-Spec (JSON)** — siehe Abschnitt 9. Sie wird per
`reel_spec`-Loader in `--props` uebersetzt und dann gerendert:

```bash
# 1) Reel-Spec -> Remotion-Props (aus dem Skill-Root)
python -m creative_studio.reel_spec --spec examples/reel_h1-immo.json \
  --out video/out/reel.props.json

# 2) Render (9:16, MP4) — Composition-Id "AdReel"
cd video
npx remotion render src/index.ts AdReel out/reel.mp4 \
  --props=./out/reel.props.json --concurrency=1
```

- **Captions** (`Captions.tsx`, SKILL-043): konsumiert word-level Tokens
  (`text/startMs/endMs`, Whisper-kompatibel). Position: oberes/mittleres Drittel
  **ueber** der unteren 35 %-Safe-Zone (Reels-UI-frei), ~15–20 Zeichen/Zeile,
  1–3 Woerter aktiv. Presets `clean` / `karaoke` / `hormozi` per Prop
  (`captionStyle`); Farben/Font/Highlight aus Brand-Props. Ohne Tokens rendert
  das Reel ohne Captions (Layer optional). Whisper-Transkription ist
  **vorgelagert** (Input = Transkript-JSON).
- **Audio** (`AdReel.tsx`, SKILL-044): `voiceoverSrc` als Track, `musicSrc` mit
  Per-Frame-**Ducking** (Musik leiser, waehrend Captions-Sprechspannen laufen
  bzw. solange ein Voiceover existiert). Ohne Audio bricht der stumme Pfad nicht.
- **Dynamische Dauer** (`Root.tsx` `calculateMetadata`, SKILL-044): Reihenfolge
  Spec-`durationInFrames` > Voiceover-Audio-Laenge > letztes Caption-`endMs` >
  Fallback 180 Frames.

### 4b. Reel-Format `broll_message` (B-Roll + Message, SKILL-078)

Eigenstaendiges, sauberes Reel-Format fuer **organische Content-Reels** (Saskia-/
Gold-Stil): B-Roll-Footage als Vollbild-Hintergrund + **eine redaktionell
durchdachte Message** — **kein** Talking-Head, **kein** Akzent-Balken, **keine**
Wort-fuer-Wort-Captions. Loest die fruehere Zweckentfremdung von `talking_head`
(B-Roll ueber `speakerSrc` + persistente `hookText`) durch ein sauberes Format ab.

Composition `BrollMessage.tsx` (in `Root.tsx` registriert). Aufbau:

- **B-Roll-Layer:** montiert `broll[]`-Clips (`{src, seconds}`) als Vollbild-9:16-
  Hintergrund (`OffthreadVideo`, `objectFit: cover`, O-Ton **stumm** = Meta
  Sound-off; `OffthreadVideo` wendet iPhone-Rotations-Metadaten an -> aufrecht).
  Musik/Voiceover optional (`music`/`voiceover`). Ohne `broll` faellt es auf den
  Brand-Gradient zurueck (Reel bricht nicht).
- **Hook oben** (`hook`, Pflicht): kurz, editorial Serif, in der oberen Safe-Zone
  (14 %), sauberer Fade-in, danach persistent.
- **Message** (`message`, Pflicht): der abholende Haupttext, editorial Serif im
  Saskia/Gold-Stil (weiss=`ink`, zentriert, unteres Mittel-Drittel **ueber** der
  unteren 35 %-Reels-UI). **EINE Kernbotschaft pro Reel** ist der Default; ist
  `scenes[]` gesetzt, erscheinen zeitlich abgestufte **Sub-Messages** je Segment.
- **Optionale dunkle Box** hinter der Message (`text_box`, Saskia-Loesung fuer
  helle/kontrastarme B-Roll). Werte `true` / `false` / `"auto"` (Default). Der
  Render kann den echten B-Roll-Kontrast nicht messen (das ist der Vision-QA-Job,
  Abschnitt 15) — deshalb loest `"auto"` **konservativ auf Box-AN** auf; nach dem
  Vision-QA-Blick setzt der Agent `text_box:false`, wenn die B-Roll dunkel genug
  ist. Ein starker Text-Schatten traegt auch **ohne** Box.

Brand-Tokens (accent/ink/bg/**font** = die editorial-Serif …) kommen ausschliesslich
ueber Props/Spec — **nichts hartkodiert** (die Serif-Wahl ist eine Brand-Entscheidung
via `brand.font`).

**Spec + Render:**

```bash
# broll_message-Spec -> Props (zentrale Brand als Basis unter dem Spec-Override):
python -m creative_studio.reel_spec --spec examples/reel_broll_message.json \
  --brand-env ../AgentischesArbeiten/terraform/base-dev/build/customization/branding.env \
  --out video/out/reel.props.json
#   -> Ausgabe nennt die Composition (composition=BrollMessage).

cd video
npx remotion render src/index.ts BrollMessage out/reel.mp4 \
  --props=./out/reel.props.json --concurrency=1
```

Die **Composition-Id** waehlt sich ueber `content_type` (Single Source
`reel_spec.ReelSpec.composition_id`): `broll_message -> BrollMessage`,
`talking_head -> TalkingHead`, sonst `AdReel`. Beispiel-Spec:
`examples/reel_broll_message.json`.

### 4c. Reel-Brand zentral (SKILL-078) — eine Brand-Datei, Bilder UND Reels folgen

Frueher trug **jede** Reel-Spec ihren eigenen `brand`-Block; eine zentrale
Brand-Aenderung schlug (anders als beim Bild-Pfad) **nicht** auf Reels durch. Ab
SKILL-078 l-aedt der Reel-Loader die Brand-Tokens aus **derselben zentralen Quelle**
wie der Bild-Pfad (`render_image.resolve_brand` ueber `brand.json` bzw.
`branding.env`) — **kein zweites Schema**. Der `brand`-Block in der Spec ist nur
noch ein optionaler **Override**.

**Praezedenz:** `Spec-brand` > zentrale `brand.json`/`branding.env` > Defaults.

- Kern-Tokens (`name`/`accent`/`bg`/`bgSoft`/`ink`/`inkMuted`/`font`) kommen aus
  `resolve_brand()` (dieselbe Logik wie das Bild-Modul).
- Reel-/Caption-Tokens (SKILL-057: `BRAND_HIGHLIGHT`/`BRAND_CAPTION_FONT`/
  `BRAND_CAPTION_BG_ALPHA` bzw. `highlight`/`caption_font`/`caption_bg_alpha` im
  brand.json) werden aus **derselben** Datei nachgelesen.
- API: `reel_spec.resolve_central_reel_brand(brand_env=, brand_json=)` liefert das
  Reel-Token-dict; `load_reel_spec(spec, brand_env=, brand_json=)` legt es als Basis
  unter den Spec-Override. Ergebnis: **eine** `branding.env` aendern -> Bild-Ads UND
  Reels ziehen automatisch nach.

> [!important] Redaktionelle Copy ist Pflicht (nicht optional) — SKILL-078
> Jedes Reel braucht **redaktionell durchdachte Copy**: **Hook** (oben, holt an —
> Ergebnis/Zahl zuerst, DISC-rot) **+ abholende Message** (der Haupttext, der die
> Kernbotschaft traegt). Das ist dieselbe Textdisziplin wie bei den Ad-Creatives —
> nutze das Hook-Framework aus `creative_studio/frameworks.py` (`get_hook()`,
> `hook_fits_onscreen()`, `recommend_framework()`) und den Editorial-Validator
> `content.content_structure_warnings()` (Hook ohne Zahl / Frage-Floskel / fehlender
> Value warnen). Ein `broll_message`-Reel **ohne** durchdachten Hook+Message-Text ist
> **unvollstaendig** — die Spec-Validierung wirft `ReelSpecError`, wenn `hook` oder
> `message` fehlt (kein stilles leeres/textloses Reel, EARS-Geist).

> [!warning] Copy-Anti-Liste: Gedankenstriche sind TABU (SKILL-087)
> In **jeder generierten/verwendeten Copy** (Hook, Body/Message, Subline, Eyebrow,
> CTA, Captions) sind **Em-Dash (—, U+2014) und En-Dash (–, U+2013) verboten** —
> sie wirken nach KI/unnatuerlich. Ersetze sie durch **Punkt, Komma, Doppelpunkt
> oder eine Umformulierung**. Der **normale Bindestrich/Hyphen-Minus (-, U+002D)
> in Komposita** ("Kurzzeit-Vermieter", "DISC-rot") **bleibt erlaubt** — nur die
> langen Striche sind gemeint (vorsorglich auch ‒/―/− als optisch nicht
> unterscheidbare Varianten). Erzwungen im Copy-Vorpruef-Flow: `AdContent.warnings()`
> (Bild) und `content.content_structure_warnings()` (Reel) rufen
> `specs.dash_warnings()` auf; die reine Fund-Funktion ist `specs.check_no_emdash(text)`
> (liefert `DashViolation` mit Position). Wie die uebrigen Copy-Checks ist es eine
> **Warnung, keine harte Sperre** (Mensch-im-Loop).
>
> Dieselbe Anti-Liste-Disziplin wie sonst: **keine Tool-/Produktnamen im Bild-Text,
> nie "Geschaeftsfuehrer" als Anrede (DISC-rot), kein Preis im Creative** — und eben
> keine Gedankenstriche.

### 4d. Copy-Framework-Katalog + Empfehlungs-Matrix + Methoden-Tagging (SKILL-025/081-086)

Der Copy-Framework-Katalog (`creative_studio/frameworks.py`) ist die Single Source fuer die
Argumentations-Gerueste — **medien-uebergreifend** (Bild + Video teilen ihn). Neben den
Klassikern (AIDA/PAS/BAB/FAB/PASTOR/4P/HSO) enthaelt er die **4 Baulig-Methoden**
(Founder Summit 2025, siehe `docs/ad-frameworks/baulig-methoden.md`). Jedes neue Framework
hat einen expliziten **CTA-Slot**; PAS wurde additiv um den CTA-Slot ergaenzt (Baulig #1).

**Empfehlungs-Matrix ("wann + fuer wen").** Jedes Framework traegt generische, projektneutrale
Auslieferungs-Metadaten — so muss man Zielgruppe/Timing beim Erzeugen nicht mehr manuell
mitgeben:

| Framework | Slots (Copy-Arc) | awareness | funnel | traffic | wofuer/wann (best_for) |
|---|---|---|---|---|---|
| `aida` | attention·interest·desire·action | unaware | tofu | cold | Cold/edukieren, mittellange LPs |
| `pas` | problem·agitate·solution·**cta** | problem_aware | tofu/mofu | cold | Default fuer Cold-Meta-Ads (Problem bekannt, kein Weg) |
| `bab` | before·after·bridge | solution/product_aware | mofu | warm | Verbesserungs-motiviert, bildstark (Video) |
| `fab` | feature·advantage·benefit | solution/product_aware | mofu | warm | Vergleichend/abwaegend, FAQ/Karussell |
| `pastor` | problem·amplify·story·transformation·offer·response | problem/solution/product_aware | mofu/bofu | warm | Langform (VSL, Sales-Page, E-Mail) |
| `4p` | picture·promise·proof·push | solution/product_aware | mofu | warm | Mid-Funnel mit Social Proof |
| `hso` | hook·story·offer | product/most_aware | mofu/bofu | warm/retargeting | Warmes Publikum, Reels/Video |
| `mindset_shift` | situation·false_belief·truth·future_projection·**cta** | problem/solution_aware | tofu | cold | Belief-Reframe ("Du denkst X: Wahrheit ist Y") |
| `opportunity` | new_opportunity·old_way_downsides·new_way_upsides·**cta** | solution/product_aware | mofu | warm | Neuer Mechanismus (nicht inkrementelle Verbesserung); Layout `split-compare` |
| `avatar_story` | self_select·current_problems·mirrored_customer·discovered_solution·new_results·**cta** | problem/solution_aware | mofu | warm | Kunden-Story/Testimonial mit Selbst-Selektions-Hook (Beleg-PFLICHT) |
| `heros_journey` | past_self·problems·nothing_worked·near_giving_up·discovery·new_world·pay_it_forward·**cta** | product/most_aware | mofu/bofu | warm | Gruender-Story (8 Stufen), primaer Video/Reel |

Achsen sind generisch (`AWARENESS_LEVELS`/`FUNNEL_STAGES`/`TRAFFIC_TEMPERATURES`) — **kein**
Projektwert hartkodiert. Auswahl-Hilfe:

- `frameworks.recommend_framework(awareness, placement="", *, funnel=, traffic=, goal=)` —
  Einzel-Empfehlung; `goal` (Angle-Hint: `belief`→mindset_shift, `new_mechanism`→opportunity,
  `testimonial`→avatar_story, `founder_story`→heros_journey) ueberschreibt die Awareness-Default-Wahl.
- `frameworks.match_frameworks(awareness=, funnel=, traffic=, goal=)` — alle passenden Frameworks.
- CLI: `python -m creative_studio.frameworks list` (Empfehlungs-Matrix, `--json` moeglich),
  `... recommend --awareness cold --funnel tofu` / `... recommend --goal testimonial`.

**Methoden-Tagging (SKILL-086) — Framework durchgaengig im Output.** Damit Ads spaeter nach
Copy-Methode getrackt werden koennen, ist das Framework aus jedem Artefakt ablesbar — fuer
Bild UND Video:

- **variant_id / utm_content:** tragen den (slugifizierten) Framework-Key positional
  (`<ad_id>__<framework>-h<NN>__<format>`, SKILL-024). Reels wie Bild-Ads.
- **Dateiname:** Bild-Ads = `<ad_id>__<framework>__<format>.png` (Framework-Token, sobald ein
  nicht-Default-Framework gesetzt ist; Default-Renders bleiben `<ad_id>__<format>.png`).
  Reels: MP4 nach `variantId` benennen. Batch: Dateiname == variant_id.
- **Metadaten:** Bild-Sidecar `<name>.json` (`build_image_meta`, Feld `framework` roh + variant_id/
  utm_content), Reel-`props.json` (`"framework": <key>`), Batch-`manifest.json` (Feld `framework`).
- **Setzen:** Bild-CLI `render_image ... --framework <key>` (Default `default`); Reel-Spec-Feld
  `framework`; Batch-Variante `{framework: ...}`. `AdContent.framework` ist der Bild-SSOT.

> [!tip] Beispiel Bild vs. Video
> `render_image ... --ad-id acme --framework mindset_shift` -> `acme__mindset-shift__feed_4x5.png`
> + `.json` mit `"framework": "mindset_shift"`. Reel-Spec `{"framework": "heros_journey"}` ->
> `props["framework"] = "heros_journey"`, `variantId = acme__heros-journey-h00__story-9x16`.

## 5. Standards (specs.py)

Alle Meta-Anforderungen liegen zentral in `creative_studio/specs.py` (Single Source,
von Bild- und Video-Modul geteilt):

- **Formate / Safe-Zones** (`AdFormat`, `FORMATS`):
  - `feed_4x5` — 4:5, **1080x1350**, Safe oben ~14 % / unten ~20 %.
  - `story_9x16` — 9:16, **1080x1920**, Safe oben ~14 % / **untere 35 % frei** (Reels-konservativ).
  - `square_1x1` — 1:1, **1080x1080**, Safe oben ~10 % / unten ~16 %.
  - `DEFAULT_FORMATS = ("square_1x1", "feed_4x5", "story_9x16")` (SKILL-076) — **alle drei
    Meta-Standard-Formate**. Ein Creative wird per Default IMMER in 1:1 **und** 4:5 **und**
    9:16 erzeugt; 4:5 ist Metas Feed-Portrait-Default 2026 und darf nie stillschweigend fehlen.
- **Technische Constraints:** Mindestkante 1080 px (1080–1440 ideal), max. 30 MB, Farbraum
  sRGB (nie CMYK), Headline-Feld max. 27 Zeichen, Primary-Text 50–150 Zeichen.
- **Text-im-Bild:** Metas 20-%-Regel ist tot — keine harte Sperre, nur Empfehlung < 20 %.
- **Coaching-Claim-Warnung** (`AdContent.warnings()`): persoenliche Vorher-Nachher-/Du-
  Versprechen (DACH-Coaching-Fallstrick) loesen eine Warnung aus — keine Sperre, aber
  Hinweis, neutraler/produktbezogen zu formulieren. Ebenso Warnung bei sehr langer Headline.
- **Gedankenstrich-Verbot** (`dash_warnings()` / `check_no_emdash()`, SKILL-087): Em-Dash
  (—) / En-Dash (–) in der Copy loesen eine Warnung aus (wirkt nach KI). Normaler
  Bindestrich (-) bleibt erlaubt. In `AdContent.warnings()` + `content_structure_warnings()`
  eingehaengt — Warnung, keine Sperre. Siehe Copy-Anti-Liste-Callout oben.
- **Cold-Audience-Messaging** (SKILL-088..098, `docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md`):
  Fuer kalte Zielgruppen, die den Produkt-/Kategoriebegriff noch nicht kennen, sind die
  Erkenntnisse testbar encodiert (alles projektneutral, Projekt-VoC bleibt Parameter/Doku):
  - **Hook-Formeln F1-F6** als CopyFrameworks (`scene`/`kunden_oton`/`vorher_nachher`/
    `einwand_oton`/`anti_hype`/`umbruch`); `match_frameworks(traffic="cold")` rankt sie vor
    die generischen cold-Frameworks (SKILL-089/091).
  - **8 Human-Messaging-Regeln** abrufbar (`frameworks.human_messaging_rules()`); Warn-Checks
    `specs.human_rule_warnings()` (Statistik-Opener, Consultant-Abstrakta, `category_term`
    fuer „Begriff zuletzt") in Bild- + Reel-Flow eingehaengt (SKILL-089).
  - **Brand-Voice-Leitplanken** `specs.brand_voice_warnings()` (keine Tool-Namen via
    `forbidden_tools`, kein Preis, kein FOMO, „individueller" statt „kompliziert"), plus
    `specs.hype_warnings()` (Anti-Hype = Vertrauen) und `specs.visual_cliche_warnings()`
    (Anti-KI-Klischee im Motiv-Prompt) (SKILL-092/096/098).
  - **CTA-Bibliothek** (`frameworks.CTA_LIBRARY`, button/hart/weich), **Ton-Profile**
    (`frameworks.TONE_PROFILES`, buyer/champion) und **Value-Translations**
    (`frameworks.apply_value_translations(text, mapping)`) (SKILL-093/094/095).
  - **Projekt-VoC** als optionaler Copy-Kontext: `content.load_messaging_doc(pfad)` +
    `content.build_analysis_prompt(..., messaging_doc=...)` speist echte Kundensprache in den
    Reel-Redaktions-Pass ein (fehlende Datei -> Fallback ohne Fehler) (SKILL-090). Die
    projekt-spezifischen Werte (VoC, Tool-Namen, Fachbegriff, warme Palette) kommen als
    Parameter/Datei rein, nicht als hartkodierter Wert im Skill-Code.

## 6. Multi-Projekt-Nutzung

Der Skill traegt **keinen** Projektwert in sich. Pro Projekt:

- **Brand-Tokens** ueber `--brand-env <pfad/branding.env>` (Bild) bzw. `--props` (Video).
  `branding.env` ist eine Key=Value-Datei mit:
  `BRAND_NAME`, `BRAND_BG`, `BRAND_BG_SOFT`, `BRAND_ACCENT`, `BRAND_INK`,
  `BRAND_INK_MUTED`, `BRAND_FONT`.
- **Content** ueber CLI-Args (`--headline`, `--subline`, `--cta`, `--eyebrow`, `--brand`,
  `--ad-id`, `--bg-image`) bzw. das `--props`-JSON beim Video.

So laeuft derselbe Skill z. B. in AgentischesArbeiten (Warteliste-Ads) und SocialMediaBuilder.

## 7. Bekannte Grenzen / offen

- **Foto-Hintergruende** — geschlossen: content-aware Crop (SKILL-032, Smartcrop) +
  automatische Bildbeschaffung (SKILL-073, `--bg-source`, Abschnitt 13). Der
  Brand-Gradient bleibt der Default, wenn kein Bild gewaehlt/gefunden wird.
  **Lesbarkeit auf Foto-BG** — geschlossen: WCAG-Kontrast-Check (SKILL-074,
  `--check-contrast`, Abschnitt 14) misst nach dem Render den echten Pixel-Kontrast
  unter dem Text und warnt (keine Sperre).
- **Meta Advantage+ Creative-Enhancements** ggf. im Ad-Set deaktivieren — sonst kann Meta
  die hier gebaute Komposition automatisch ueberschreiben.
- **Remotion-Lizenz:** ab 4 Personen im Team kostenpflichtig (Lizenzpruefung beim
  Skalieren des Video-Moduls beachten).

## 8. Content-Marktrecherche (Tier 0, vorgelagert)

Der Skill ist sonst strikt **produktionsseitig** (nimmt fertigen Content + rendert).
Davor steht eine optionale **Ideen-/Recherche-Stufe**, die aus einem **Seed-Thema**
eine **priorisierte Themen-/Hook-/Format-Liste mit Quellen** erzeugt, die 1:1 die
Creative-Inputs (`--headline`/`--subline`/`--cta`/`--eyebrow` bzw. Video-`--props`)
speist. **Tier 0 = gratis, kein API-Key**, rein WebSearch/WebFetch-getrieben.

**Runbook:** `templates/content_research.md` — der deterministische 6-Schritte-Ablauf:

1. **Sammeln** (pro Seed: Google Trends Rising-Queries, YouTube-Autocomplete,
   PAA-Fragen, 3-5 Reddit/LinkedIn-O-Toene — je mit **Quelle + Datum**).
2. **Clustern** zu Themen (Hub + narrow Sub-Fragen, Hub-and-Spoke).
3. **Funnel-Mapping** (TOFU/awareness, MOFU/consideration, BOFU/conversion —
   deckt sich mit `ContentType.funnel`).
4. **Priorisieren** (Volumen x Relevanz x 1/Wettbewerb + Social-Resonanz, 1-3-Skala).
5. **Idee -> Hook -> Format** (Hook aus echter Frage/O-Ton, **DACH-Coaching-Claim-Check**
   via `compliance_warnings()` / SKILL-026; Format auf einen `CONTENT_TYPES`-Key mappen).
6. **Output-Liste** als Markdown-Tabelle `Thema | Funnel | Idee | Hook | Format | Prioritaet | Quellen`
   (>= 1 Quelle pro Eintrag), optional zusaetzlich als JSON, dessen Felder direkt
   `render_image`-Args / Video-`--props` speisen.

**Eingabe:** Seed-Thema (Pflicht), optional `anzahl_seeds`, `tier` (Default 0),
`brand_kontext`. **Kein hartkodierter Projektwert** — projektneutral wie der Rest des
Skills. Tier 1 (PAA/SERP-API) und Tier 2 (GSC/Trends-Alpha) sind separate Stufen
(API-Key/Domain noetig), nicht Teil von Tier 0.

> **Kein Eingriff in den Render-Pfad/`specs.py`:** Diese Stufe ist reines Runbook/Doku;
> ihr Output ist der Uebergabe-Vertrag zur Creative-Generierung.

## 9. Ad-Library-Scan (Wettbewerbs-Recherche, Proxy — kein Spend)

Vorgelagerter, reproduzierbarer Wettbewerbs-Scan: aus einem **Seed-Thema** oder
**Wettbewerber-Page-ID(s)** eine Tabelle **wahrscheinlich skalierender Ads** + eine
**Hook-/Angle-Muster-Liste**, die als Briefing-Input in die Creative-Generierung
fliesst. Modul: `creative_studio/ad_library.py`. Runbook: `templates/ad_library_scan.md`.

> [!warning] EHRLICHKEIT — kein Spend abrufbar (Pflicht-Disclaimer)
> Meta gibt fuer **kommerzielle** Ads **KEINEN Spend / keine Impressions / keine
> Reichweite** preis — weder im MCP-Payload noch ueber die offizielle Public API
> (Spend-Ranges nur fuer politische/Issue-Ads). Der Scan beruht ausschliesslich auf
> **Proxy-Signalen**: Longevity, Creative-Multiplikation pro Page, Re-Serving,
> Hook-Wiederholung. Der **Longevity-Score** ist eine Priorisierung fuer die manuelle
> Sichtung, KEINE Budget-Wahrheit. `ad_library.PROXY_DISCLAIMER` ist Pflicht-Output.

**Architektur:** Das Python-Modul ruft das Meta-MCP **nicht selbst** auf. Den read-only
Call `mcp__claude_ai_Meta__ads_library_search` macht der **Agent/Claude**; das Modul
verarbeitet die zurueckgegebene JSON (`theme_sweep`, `scan_report`, `extract_hook_patterns`,
`render_report_markdown`) und ist so gegen gespeicherte Beispiel-Payloads unit-testbar.

**Ablauf (Details + Code-Snippets im Runbook):**

1. **Themen-Sweep:** `ads_library_search(search_terms=..., countries=["DE"], ad_active_status="ACTIVE", limit=50)`
   -> `al.theme_sweep(result)` -> `estimated_total_count` + Top-Advertiser-Pages.
2. **Page-Drilldown:** pro Top-Page `ads_library_search(page_ids=[...], ad_active_status="ALL")`.
   Real verfuegbare Felder: `id`, `page_id`, `page_name`, `ad_creative_link_title` (= Hook),
   `ad_creation_time`, `ad_delivery_start_time`, `ad_snapshot_url` — **kein** Spend/Reach.
3. **Score + Report:** `al.scan_report(entries, theme=..., country="DE")` -> Tabelle
   (absteigend nach Longevity-Score) + Hook-Muster + Disclaimer; `al.render_report_markdown(report)`.
4. **Snapshot-Anreicherung (optional):** Top-N `ad_snapshot_url` oeffnen (Volltext/Visual,
   ggf. EU-Reach-Band — nur ueber die Snapshot-Seite, nicht im MCP).
5. **Uebergabe:** Top-Hooks aus `report["hook_patterns"]` als Inspiration in `render_image`/Video.

**Longevity-Score-Formel (fixiert, Research §2):**
`score = aktive_Tage(creation -> heute) * log(1 + Anzahl_aktiver_Varianten_der_Page)`.
Hoch = lange aktiv UND breit ausgerollt.

> [!warning] Legal: nur **Inspiration** (Hook-/Angle-Muster), **kein** 1:1-Kopieren von
> Creatives/Claims, **kein** Bulk-Scraping (Tool-Policy).

## 10. Reel-Spec (JSON) — zentrale Eingabe der Reel-Engine (SKILL-045)

Eine **Reel-Spec** beschreibt **ein** Reel vollstaendig und treibt den `AdReel`-Render
(Abschnitt 4a). Skalierung = eine Composition + n Specs. Loader/Adapter:
`creative_studio/reel_spec.py` (`load_reel_spec` -> `ReelSpec` -> `reel_spec_to_props`).
Beispiel: `examples/reel_h1-immo.json`.

**Felder:**

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `ad_id` | **ja** | Datei-/Naming-Stamm; speist `variant_id`/`utm_content` (SKILL-024, Single Source). |
| `hook` | **ja** | Headline/Hook (Ergebnis/Zahl zuerst, DISC-rot). |
| `brand` | **ja** | Brand-Tokens-Objekt: `name` (Pflicht), `accent`, `bg`, `bgSoft`, `ink`, `inkMuted`, `highlight` (Caption-Keyword), `font`. |
| `framework` | nein | Copy-Framework-Key (Default `hook`) — Methoden-Tagging (SKILL-086): landet positional im `variant_id`/`utm_content` UND als explizites `props["framework"]`-Feld. Keys aus `frameworks.FRAMEWORKS` (pas/mindset_shift/opportunity/avatar_story/heros_journey ...). |
| `hook_index` | nein | Hook-Index fuer kollisionsfreie `variant_id` (Default 0). |
| `hook_accent` | nein | accent-gefaerbter Teil der Headline. |
| `eyebrow` / `subline` / `cta` | nein | Title-Card-Texte. |
| `scenes` | nein | Segmente `{text, seconds}` — Summe der Sekunden bestimmt die dyn. Dauer. |
| `captions` | nein | word-level Tokens `{text, startMs, endMs}` (Whisper-Output, **vorgelagert**). |
| `caption_style` | nein | `clean` / `karaoke` / `hormozi` (Default `hormozi`). |
| `voiceover` | nein | VO-Audio-Ref (Pfad/URL) -> Audio-Track + dyn. Dauer. |
| `music` | nein | Musik-Ref -> Hintergrundmusik mit Ducking unter dem Voiceover. |
| `broll` | nein | B-Roll-Clips `{src, seconds}` (Hintergrund-Layer; bei `broll_message` der Vollbild-BG). |
| `content_type` | nein | CONTENT_TYPE-Key; steuert die Composition (`broll_message` → BrollMessage, `talking_head` → TalkingHead, sonst AdReel). |
| `message` | **ja (broll_message)** | SKILL-078: abholender Haupttext (Serif, unteres Mittel-Drittel). Pflicht **nur** fuer `content_type == "broll_message"`. |
| `text_box` | nein | SKILL-078: dunkle Box hinter der Message — `true` / `false` / `"auto"` (Default, konservativ Box-AN; Vision-QA setzt `false` auf dunkler B-Roll). |

**Validierung (EARS-2):** fehlt ein Pflichtfeld (`ad_id`/`hook`, plus `brand.name`
aus Spec **oder** zentraler Brand), wirft der Loader `ReelSpecError` — **kein**
stilles leeres Reel (kein Silent-Fake). Fuer `content_type == "broll_message"` sind
zusaetzlich `hook` **und** `message` Pflicht (SKILL-078).
**Zentrale Brand (SKILL-078):** der `brand`-Block ist ein optionaler Override ueber
der zentralen `brand.json`/`branding.env` — siehe Abschnitt 4c.
**Optionale Layer (EARS-3):** ohne `captions`/`voiceover`/`music` rendert das Reel
trotzdem. **Multi-Projekt (EARS-4):** Brand + Inhalt kommen ausschliesslich aus der
Spec — kein hartkodierter Projektwert im Loader.

> **Lizenz-Risiko Remotion:** ab 4 Team-Personen kostenpflichtig (Abschnitt 7) — vor
> Skalierung des Video-Moduls klaeren.

## 11. Content-aware Reel-Pipeline (SKILL-060/061) — Captions aus dem ECHTEN Wort

> [!important] Loest die Critique 2026-06-25: „kein Bezug zum Transkript / kein Verstaendnis"
> Bis SKILL-059 waren die `captions` der Reel-Spec **handgeschriebene Slogans mit erfundenen
> Timings** — nicht das tatsaechlich Gesprochene. Diese Stufe erzeugt die Captions
> **aus der Tonspur des Footage** (Whisper, word-level) und strukturiert das Reel
> **redaktionell** (Claude = der Redaktions-Pass). Die Render-Schicht (SKILL-043/044/055/056)
> bleibt unveraendert — nur die **Quelle der Spec** wird vom Hand-Tippen auf „aus Audio + Analyse".

**Voranforderungen (Prereqs, kein Blocker — lokal/offline):**
```bash
pip install faster-whisper        # smallest viable; Modell "small" wird offline gecacht
# ffmpeg: das gebuendelte Remotion-ffmpeg reicht (nach `cd video && npm install`) — kein globaler Install
```

**Pipeline (vorgelagert zum Render):**

```
footage (.mov/.mp4)
  └─[A]──> Audio 16kHz mono WAV  (gebuendeltes Remotion-ffmpeg)
       └─[B]──> word-level Transkript-JSON  (faster-whisper, word_timestamps)
            └─[C]──> Redaktions-Pass (CLAUDE)  -> EditorialDecision (JSON)
                 └─[D]──> maschinelle Reel-Spec  (content.decision_to_spec)
                      └─[E]──> reel_spec.py --props  (BESTAND, SKILL-045)
                           └─[F]──> Remotion-Render  (BESTAND, TalkingHead/AdReel)
```

### 11a. Transkription (`creative_studio/transcribe.py`, SKILL-060)

```bash
# Footage -> word-level Transkript (optional Ausschnitt --start/--duration)
python -m creative_studio.transcribe \
  --video "Content Lake/Bronze/clip.mov" \
  --out transcript.json --language de --model small --start 0 --duration 20
```
Output: `{language, full_text, words:[{text,startMs,endMs,p}]}`. `words` ist 1:1 das
Caption-Schema von `Captions.tsx` (SKILL-043). Bei leerem Transkript bricht die Stufe hart ab
(kein erfundenes Reel — `feedback_no_silent_fakes`).

### 11b. Content-Analyse (`creative_studio/content.py`, SKILL-061) — Claude IST die Intelligenz

Wie `ad_library.py` (MCP-Call beim Agent) macht das Modul **keinen** LLM-Call. Ablauf fuer Claude:

1. `prompt = content.build_analysis_prompt(transcript_dict, brand_context=...)` — Briefing mit
   Wort-Index ueber dem echten Transkript.
2. **Claude beantwortet** das Briefing als JSON (`EditorialDecision`): staerkstes 20–45-s-`segment`
   (Wort-Indizes), `hook` (DISC-rot, Zahl/Ergebnis zuerst), `narrative` (Insight + CTA),
   `keyword_words` (zu betonende Wort-Indizes — **ein** Akzent pro Phrase).
3. `dec = content.parse_editorial_decision(antwort)` — validiert (Pflicht: segment + hook).
4. `spec = content.decision_to_spec(transcript, dec, ad_id=..., brand=..., content_type="talking_head", speaker={...})`
   — schneidet die Captions **aus dem gewaehlten Segment** des echten Transkripts (auf 0 ms genullt)
   und setzt `keyword:true` auf die betonten Woerter. Ergebnis = fertige Reel-Spec.
5. `python -m creative_studio.reel_spec --spec spec.json --out props.json` + Render (Abschnitt 4a/SKILL-056).

> **Beleg (echt, 2026-06-25):** Bronze `Video 07.03.26, 15 46 40.mov` -> 20-s-Audio -> faster-whisper
> (DE, 25 Woerter, 7,4 s) -> Transkript „Die meisten Gastgeber wissen gar nicht, wie viele Nachrichten
> sie bekommen … 16 Ferienwohnungen, 150 Nachrichten" -> Redaktions-Pass -> maschinelle Spec ->
> Gold `reel_talkinghead_v2_transcript.mp4` (11,5 s, Video+O-Ton). Die Captions zeigen das **tatsaechlich
> Gesprochene** (Keyword-Highlight auf „NACHRICHTEN", „FERIENWOHNUNGEN", „150") — nicht mehr den
> hartkodierten „3 Stunden pro Woche"-Slogan.

### 11c. Optional/Folge

- **WhisperX-Alignment** (SKILL-062, Should): Karaoke-genaue Wortgrenzen (wav2vec2, sub-100ms) —
  `pip install whisperx` (schwerer, torch). Nur fuer den Praezisions-Pfad.
- **B-Roll-Matching** (`creative_studio/broll_match.py`, SKILL-063, erledigt): bindet B-Roll an
  das tatsaechlich Gesprochene statt zufaellig. v1 = reiner Keyword-/Token-Overlap (kein Modell,
  kein API; leichtes DE-Stemming gleicht Singular/Plural-Drift aus). Ablauf:
  `cues = broll_match.build_broll_cues(transcript, decision)` (eine Cue je Keyword-Phrase) ->
  `spec["broll"] = broll_match.match_broll(cues, broll_match.load_library(manifest))` bzw. die
  Kurzform `broll_match.match_broll_for_decision(transcript, decision, manifest)`. Kein passender
  Clip -> Position bleibt LEER (Talking-Head-Fallback, kein erzwungener Fehl-Clip).
  **Tag-/Manifest-Konvention:** Bibliothek = Liste `{src, tags?, description?, seconds?}`; fehlen
  Tags, dienen Dateiname + Beschreibung als implizite Tags (so matcht auch ein blosses Verzeichnis,
  `broll_match.library_from_dir(...)`). Output `[{src, seconds}]` ist reel_spec-kompatibel.
- **Editorial-/Struktur-Validator** (`content.content_structure_warnings(spec, ct=None)`, SKILL-065,
  erledigt): Qualitaets-Netz vor dem Render — warnt (keine Exception/kein Blocker) bei Hook ohne
  Zahl/als Frage-Floskel, fehlendem Insight/Value (subline), fehlendem CTA, Caption-/Keyword-Last
  (Dauer-Highlight statt EIN Akzent/Phrase) und Segment-Laenge ausserhalb des Sweetspots. Laenge/
  Hook-Fenster delegiert er bei uebergebenem `ContentType` an `specs.content_type_warnings()`
  (kein Doppel). Schwellen sind Modul-Konstanten (multi-projekt).
- **End-to-End-Sub-Command** (SKILL-064, Should): `footage -> fertiges Reel` in einem Lauf.

> **Keyword-Betonung (SKILL-066, erledigt):** Das vom Redaktions-Pass gesetzte `keyword:true`
> wird von `reel_spec.py` bis in die Remotion-Props durchgereicht; `Captions.tsx` highlightet das
> **inhaltlich** gewaehlte Wort (Vorrang vor der SKILL-055-Heuristik „laengstes/zahlhaltiges Token";
> Heuristik nur noch Fallback, wenn kein Keyword gesetzt ist). Frame-Beleg: gleiches Fenster
> `["SYSTEM","GEWINNT"]` highlightet mit Flag „SYSTEM", ohne Flag „GEWINNT".

## 12. Layout-Archetypen + Stil-Parameter (SKILL-072)

Statt EIN Template-Skelett rendert der Bild-Renderer **Scroll-Stop-Archetypen** — die
Staerken bleiben (Multi-Format, Safe-Zones, Brand-Tokens, Compliance), die Archetypen
kommen **obendrauf**. **Nicht-brechend:** ohne `--layout` (Default `template`) ist der
Render exakt wie bisher. Katalog `LAYOUTS`/`THEMES` liegt projektneutral in `specs.py`.

**`--layout {template,stat-hero,photo-poster,object-hero,split-compare}`**

- **`template`** (Default) — Bestands-Skelett: eyebrow → headline → subline → CTA-Pill.
- **`stat-hero`** — EIN Riesen-Token (Zahl/Kurzwort) als Held (Scale-Kontrast 5–8:1),
  Editorial-Pfeil-Icon, viel Negativraum. Groesster Hebel, **keine** externe Bildquelle noetig.
- **`photo-poster`** — fullbleed Foto, fette Typo darueber, gerichteter Scrim nur hinter
  dem Text (Motiv bleibt sichtbar). Bild via `--bg-source` (Abschnitt 13).
- **`object-hero`** — freigestelltes Motiv/Objekt als Held (Motiv=Konzept). Bild via `--bg-source`.
- **`split-compare`** — zwei Haelften hell/dunkel (Vorher/Nachher, alt/neu).

**Stil-Parameter (alle optional, Default = Bestandslook):**

| Arg | Werte | Wirkung |
|---|---|---|
| `--hero-token` | Text | Riesen-Held fuer `stat-hero` (sonst Headline). |
| `--hero-scale` | 0.25–0.40 | Hoehenanteil des Hero (Default 0.32; ausserhalb → Warnung, keine Sperre). |
| `--headline-weight` | `bold`/`black` | Schriftschnitt. |
| `--headline-case` | `mixed`/`upper` | ALL-CAPS-Impact. |
| `--tracking` | `normal`/`tight` | Laufweite. |
| `--kicker-font` | `sans`/`serif-italic` | Editorial-Kicker. |
| `--theme` | `dark`/`light-cream` | Cream-Flaeche statt Navy; **Akzent bleibt markeneigen**. |
| `--accent-as-block` | flag | Headline/Hero in Akzentfarbe (Farbe als Flaeche). |
| `--chrome` | `full`/`minimal` | `minimal` schaltet Brand-Name, Top-Balken **und** CTA-Pill (→ Text-Link) ab — organischer Look. |

Beispiel (Sofia-Stil Stat-Hero):

```bash
python -m creative_studio.render_image \
  --headline "93 %" --hero-token "93 %" \
  --subline "nutzen KI nur als Chatbot. Du nicht." \
  --eyebrow "AGENTISCHES ARBEITEN" --cta "Auf die Warteliste →" \
  --brand-env ../AgentischesArbeiten/.../branding.env \
  --layout stat-hero --theme light-cream --chrome minimal \
  --headline-weight black --headline-case upper \
  --formats feed_4x5,story_9x16 --ad-id h1-stat --out ./out
```

`specs.layout_warnings(layout, hero_scale=, has_bg_image=)` warnt (keine Sperre) bei
Hero-Scale ausserhalb Sweetspot, foto-getriebenem Layout ohne Bild und unbekanntem Layout.

## 13. Bildquellen-Modul (Keyless Stock + KI-Gen) — `--bg-source` (SKILL-073/077)

Der Skill **zieht/generiert** passende Hintergrund-/Motiv-Bilder statt „Bild fehlt".
Modul: `creative_studio/image_source.py`.

**`--bg-source {none,library,stock,generate}`** (Default `none` = Bestandsverhalten).
Das aufgeloeste Bild wird in `content.bg_image` gefuettert → laeuft durch den bestehenden
**Smartcrop** (SKILL-032) und das Template — **kein** neuer Render-Pfad.

- **`library`** = zuerst die lokale Projekt-Bibliothek (`index.json`), kein Download.
- **`stock`** = **KEYLESS** echtes Stock-Foto ueber **Openverse** (`api.openverse.org`,
  CC-lizenziert, Filter `license_type=commercial` → kommerziell nutzbar). **Kein API-Key,
  kein User-Setup** — das ist der Default-Weg fuer Bild-Typ 3 des 4-Typen-Ad-Satzes
  (Abschnitt 2). Optionaler Qualitaets-Upgrade: ein **kostenloser** `PEXELS_API_KEY` in
  der Env — ist er gesetzt, bevorzugt der Resolver Pexels (bessere/kuratiertere Fotos),
  sonst Openverse. Herkunft + CC-/Pexels-Lizenz landen ehrlich im `index.json`
  (`source=openverse|pexels`, `license_type`, `license_url`, `attribution`, `creator`,
  `foreign_landing_url`) — nie als KI getarnt, `is_ai_generated=False` → **kein**
  Disclosure-Label (echtes Foto). (Der frueher hier genutzte Magnific-Stock-Pfad bleibt
  als optionale Premium-Quelle im Modul, ist aber nicht mehr der `stock`-Default.)
- **`generate`** = KI (Mystic) — **kostet Geld, nur explizit** (kein Silent-Spend).
- **search-first:** der Resolver prueft ZUERST die lokale Bibliothek (`index.json`),
  bevor er zieht/generiert — kein Doppel-Download/-Spend.
- **`--bg-query`** Suchbegriff/Prompt (sonst aus Eyebrow+Headline abgeleitet).
- **`--no-people`** (Default) bevorzugt personenfreie Bilder — gut fuer Paid-Ads;
  `--allow-people` hebt es auf.

**KI-Disclosure verdrahtet:** ein KI-generierter Hintergrund (`source=magnific-gen` /
`is_ai_generated`) setzt `content.ai_image=True` → das bestehende
`requires_ai_disclosure()`-Gate (SKILL-028) rendert das sichtbare **„KI-generiert"**-Label.

> [!important] Konvention: KI-Label ist IMMER ein Overlay, NIE Bild-Prompt-Inhalt
> Das „KI-generiert"-Label ist **ausschliesslich** ein Overlay, das der Skill NACH der
> Generierung ueber das fertige Creative legt (via `ai_image=True` → Disclosure-Gate
> SKILL-028 → Template `.ai-label`). Es gehoert **NIEMALS** in den Bild-Generierungs-Prompt
> (`--bg-source generate` / Magnific-Mystic) — sonst malt das Bildmodell den Text
> „KI-generiert" als **Bildinhalt** mit hinein (unkontrollierbare Position/Schrift, nicht
> entfernbar). Die Kennzeichnung ist **unsere** steuerbare Entscheidung — An/Aus, Position,
> Wortlaut (`AI_LABEL_TEXT`) bleiben in unserer Hand und werden als klar abgesetzte
> Overlay-Ebene gerendert, nicht als eingebrannter Pixelinhalt. `--bg-query`/Gen-Prompts
> beschreiben **nur** das Motiv, nie die Disclosure.

**Lizenz/Kosten-Gate:** `license_type` + `license_url` sind Pflichtfelder jedes
Index-Eintrags (Eintrag ohne Lizenz wird abgelehnt).

**Konfiguration (projektneutral — kein hartkodierter Pfad/Key):**

- `MAGNIFIC_API_KEY` (Fallback legacy `magnific_api_key`; optional Env-Datei via
  `CREATIVE_STUDIO_MAGNIFIC_ENV`). Key wird **nie** geloggt/committet.
- `CREATIVE_STUDIO_IMAGE_LIB` = Bibliothekspfad (oder `--image-lib`; Fallback `./image-library`).

```bash
export MAGNIFIC_API_KEY=…            # nie committen
export CREATIVE_STUDIO_IMAGE_LIB=/pfad/zur/bild-bibliothek
python -m creative_studio.render_image \
  --headline "Klar. Ruhig. Automatisiert." --cta "Mehr erfahren" \
  --brand-env …/branding.env \
  --layout photo-poster --chrome minimal \
  --bg-source library --bg-query "modern office desk workspace" \
  --formats feed_4x5 --out ./out
```

Standalone-CLI: `python -m creative_studio.image_source {search|stock-free|download|generate|search-lib|resolve|credits}`.
`stock-free <term>` zieht keyless (Openverse/Pexels) — `--search-only` listet nur, `--people`
laesst Personen zu (Default: personenfrei bevorzugen). Beispiel Bild-Typ 3:
`--bg-source stock --bg-query "team working laptop office" --allow-people`.

> [!note] Openverse-Lizenz-Etikette: CC0/Public-Domain braucht keine Namensnennung; **CC-BY/
> CC-BY-SA verlangen Attribution** (Urheber + Lizenz). Der Index speichert `attribution` +
> `creator` + `foreign_landing_url` je Bild — bei Paid-Ads mit CC-BY-Foto die Nennung im
> Ad-Text/Impressum sicherstellen (oder ein CC0-Foto waehlen, um die Pflicht zu vermeiden).

> [!important] Wann WIRKLICH generieren (nicht nur Bestand recyceln)
> `search-first` schuetzt vor Doppel-Spend — es ist **kein** Auftrag, jedes Motiv aus der
> Bibliothek zu erzwingen. Wenn ein Konzept eine **eigene, passende Szene/Textur** braucht,
> die die Bibliothek nicht in guter Qualitaet hergibt (fremdes Motiv „notduerftig
> passend gemacht" ist ein Qualitaetsverlust), dann **generiere echt** ueber Magnific
> (`magnific_api_key`) — das ist ausdruecklich erwuenscht, nicht der Ausnahmefall:
>
> ```bash
> # Key nie loggen/committen. Env-Datei-Weg (empfohlen, kein Klartext im Verlauf):
> export CREATIVE_STUDIO_MAGNIFIC_ENV=/pfad/zum/projekt/.env   # Datei enthaelt magnific_api_key=…
> export CREATIVE_STUDIO_IMAGE_LIB=/pfad/zur/bild-bibliothek
> # ECHT generieren (Mystic, kostet 1 Credit) — neue Datei landet in <lib>/generiert/ + index.json:
> python -m creative_studio.image_source generate \
>   "abstrakte ruhige Tech-Textur, teal/navy, viel Negativraum, keine Menschen, keine Schrift" \
>   --model realism --res 2k --ar square_1_1
> # Danach: --bg-source library greift den frischen Treffer (search-first findet ihn) —
> # oder den ausgegebenen Pfad direkt als --bg-image verwenden.
> ```
>
> `--ar`: `square_1_1` (Feed 1:1), `portrait_9_16`/`vertical` (Story), `widescreen_16_9`.
> Der Resolver setzt bei generierten Bildern `is_ai_generated=true` → Disclosure-Gate
> (SKILL-028) greift automatisch (Overlay, NIE im Prompt — siehe Kasten oben).
> **Upscaling** (Detail/Aufloesung eines Bestands-Assets echt anheben) laeuft ueber denselben
> Key/Client (Magnific-Upscale-Endpoint) — nutze es, wenn ein Foto/Motiv fuer 1080px+ zu weich ist.
> **Ehrlichkeit:** ein generiertes Bild als generiert im `index.json` fuehren (`is_ai_generated`,
> `license_type: magnific-generated`), nie als Stock/Foto tarnen (`feedback_no_silent_fakes`).

> **Phase-2 (dokumentiert, nicht gebaut):** Vision-Caption — der Agent IST das
> Vision-Modell (wie beim Ad-Library-/Redaktions-Pass), kein eigener LLM-Call. Bei Bedarf
> beschreibt Claude das aufgeloeste Bild und speist es als `--bg-query`/Alt-Text zurueck.

## 14. Lesbarkeits-/Kontrast-Check (WCAG) — `--check-contrast` (SKILL-074)

Bei Foto-Hintergruenden (`photo-poster`/`object-hero`) variiert der Untergrund UNTER dem
Text — helle Headline auf hellem Bildbereich wird schlecht lesbar, was die Theme-Farbe
allein nicht abbildet. Der Skill misst das nach dem Render selbst. Modul:
`creative_studio/readability.py` (rein Pillow, keine neue Dependency).

**`--check-contrast`** (Default aus = Bestandsverhalten). Nach dem Render wird je
Text-Region (Kicker/Headline/Subline/CTA bzw. Hero) die **WCAG-2.1-Kontrast-Ratio**
zwischen Textfarbe und dem **tatsaechlichen Pixel-Hintergrund** gemessen:

- **Region-Sampling:** jede Region (aus Format-Safe-Zone + Layout abgeleitet) wird in ein
  Kachel-Raster zerlegt, je Kachel der Flaechen-Mittelwert; der **Worst-Case** ueber alle
  Kacheln ist die Region-Ratio (ein heller Fleck unter dem Text reicht, um die Lesbarkeit
  zu kippen).
- **Schwellwerte (WCAG AA, SC 1.4.3):** **4.5:1** kleiner Text (Subline/CTA/Kicker),
  **3:1** grosser Text (Headline/Hero).
- **Warnen statt blocken:** unterschreitet eine Region ihre Schwelle, gibt es eine
  Warnung mit Region + gemessenem Wert + schlechtester lokaler BG-Farbe (Muster
  `layout_warnings()`; Mensch-im-Loop). Bei Foto-BG zusaetzlich eine Fix-Empfehlung
  (gerichteten Scrim verstaerken / Text-Panel setzen).

Textfarben kommen aus den Brand-Tokens (Headline=Ink bzw. Akzent bei `--accent-as-block`,
Hero/Eyebrow=Akzent, Subline=Ink-Muted, CTA-Pill=Weiss auf Akzent, CTA-Link=Akzent) —
projektneutral.

```bash
python -m creative_studio.render_image \
  --headline "Klar. Ruhig. Automatisiert." --cta "Mehr erfahren" \
  --brand-env …/branding.env --layout photo-poster --chrome minimal \
  --bg-source library --bg-query "modern office desk" \
  --formats feed_4x5 --out ./out \
  --check-contrast
```

Standalone-CLI auf jedem PNG:
`python -m creative_studio.readability <bild.png> --format feed_4x5 --layout photo-poster --has-bg-image`.

> **API (Agent-nutzbar):** `readability.check_contrast(img_or_path, fmt, brand, layout=, style=, content=)`
> liefert `ContrastFinding`-Objekte (worst/mean-Ratio, Schwelle, `ok`);
> `readability.contrast_warnings(...)` die fertigen Warn-Strings;
> `readability.recommend_contrast_fix(findings, has_bg_image=)` die Fix-Empfehlung.
> Die Region-Geometrie ist eine Safe-Zone-/Layout-Schaetzung (keine DOM-Boxes) — bewusst
> konservativ (Text-Striche verschieben den Kachel-Mittelwert Richtung Textfarbe -> eher warnen).

## 15. Vision-QA-Pass nach dem Render (PFLICHT — agent-getrieben, SKILL-075)

> [!important] PFLICHT — nicht „fertig" melden ohne bestandenen Vision-QA-Pass auf JEDEM gerenderten Format
> Der Renderer (Playwright/HTML-CSS bzw. Remotion) erzeugt Pixel — er **sieht** sie nicht.
> `--check-contrast` (Abschnitt 14) misst nur eine geschaetzte Text-Region, **nicht** ob ein
> Foto oder Element aus dem Rahmen ragt, ob ein Wort mitten durchbricht oder ein Umlaut zu Tofu
> wird. Diese Klasse Fehler faengt **nur ein echter Blick** ab. Deshalb ist nach **jedem** Render
> ein Vision-QA-Pass **Pflicht** — kein optionaler Zusatz, sondern Teil des Done-Kriteriums.
>
> **Anlass (Jakob 2026-07-09):** `konzept-a-bau-partner__feed_1x1.png` (Workshop-Ads) ging
> **abgeschnitten** durch — die CTA-Pille + Preiszeile ragten unten aus dem 1080×1080-Rahmen.
> Es gab keinen Blick-Check nach dem Render, also fiel es niemandem auf. Das darf nicht mehr passieren.

**Wer prueft: der Agent selbst ist das Vision-Modell** — exakt das Muster wie beim
Ad-Library-Scan (§9) und beim Redaktions-Pass (§11b): das Python-/Render-Modul macht **keinen**
LLM-Call, **Claude** liest die fertigen Pixel und urteilt. Kein externer Service, kein neuer
Dependency.

**Verbindlicher Ablauf (nach JEDEM Render-Lauf, bevor irgendetwas als fertig gilt):**

1. **Renderer laeuft** → gibt die Liste der PNG-Pfade zurueck (ein Pfad je Format).
2. **Der Agent liest JEDES PNG einzeln mit dem Read-Tool** (das Read-Tool zeigt Bilder visuell an).
   **Jedes** Format wird geprueft — **1:1 (Feed square) UND 4:5 (Feed portrait) UND 9:16 (Story)
   getrennt** (ein bestandenes 1:1 sagt NICHTS ueber 4:5 oder die Story aus: andere Hoehe, andere
   Safe-Zone, anderer Umbruch). Da der Default **alle drei** Formate rendert (SKILL-076), sieht der
   Agent bei einem Standard-Lauf pro Konzept **drei** PNGs an — 4:5 ausdruecklich mitgeprueft, nicht
   uebersprungen. Bei n Konzepten × m Formaten sind das n×m Blicke, nicht einer.
3. **Der Agent prueft jedes PNG gegen die Checkliste unten** und notiert je PNG ein explizites
   Urteil (bestanden / welcher Punkt verletzt).
4. **Bei JEDEM Treffer: Layout/Parameter anpassen und das betroffene Format NEU rendern** —
   danach zurueck zu Schritt 2 fuer genau dieses PNG. Erst wenn **alle** PNGs die Checkliste
   bestehen, ist der Job fertig.
5. **Im Report je PNG den Vision-QA-Beleg mitgeben** (bestanden / was gefixt) — Nachweis, dass
   der Blick stattgefunden hat, nicht nur behauptet wurde.

**Checkliste (jeder Punkt an JEDEM PNG — ein Treffer = Nachrender-Pflicht):**

1. **Abschneiden / Cut-off** — ragt **Text, Foto oder irgendein Element** aus dem Rahmen oder
   wird an einer Kante abgeschnitten? Sitzt eine CTA-Pille/Zeile flush an der Unterkante (halb
   abgeschnitten)? *(Genau der Konzept-A-Fehler — hier am kritischsten hinsehen. Vor allem die
   unterste sichtbare Zeile/das unterste Element: hat es sichtbaren Abstand zur Rahmenkante?)*
2. **Kontrast** — ist **jeder** Text gut lesbar ueber seinem tatsaechlichen Hintergrund
   (heller Text nicht auf hellem Bildbereich, dunkler nicht auf dunklem)?
3. **Umbrueche** — unschoene Zeilenumbrueche: ein einzelnes Wort/eine Silbe allein auf der
   letzten Zeile (Waise), Umbruch **mitten im Wort** ohne Trennstrich, „ein Wort pro Zeile"-
   Treppe? Fliesst die Headline natuerlich?
4. **Umlaute / Sonderzeichen** — werden **ä ö ü Ä Ö Ü ß € – „ "** korrekt dargestellt und
   **nicht** als Tofu (□), Fragezeichen (?) oder Mojibake (Ã¤, â‚¬)?
5. **Face-Visibility** (Personal-Brand) — ist das **Gesicht der Person frei** und nicht von
   Text, Pille, Scrim-Kante oder Logo verdeckt/angeschnitten? Sitzt der Kopf nicht am oberen
   Beschnitt?
6. **Safe-Zonen** (Story/Reels 9:16) — liegt **aller wichtige Inhalt oberhalb der unteren
   ~35 %-UI-Zone** (Reels-/Story-Bedienelemente) und unterhalb der oberen ~14 %? Nichts
   Wichtiges dort, wo die Plattform-UI es verdeckt?

**Abgrenzung zum automatischen Kontrast-Check (§14):** `--check-contrast` bleibt ein nuetzliches
**maschinelles** Vorabsignal fuer Punkt 2 (misst geschaetzte Regionen). Es **ersetzt den
Vision-QA-Pass nicht** — Cut-off, Umbrueche, Umlaut-Tofu, Face-Visibility und Safe-Zonen sieht
nur der Agent. Umgekehrt ist ein gruener `--check-contrast` **kein** Freibrief, den Blick zu
ueberspringen. Beides zusammen; der Vision-Pass ist das harte Gate.

**Warum agent-getrieben (und nicht ein weiterer Pixel-Algorithmus):** Cut-off/Umbruch/Tofu/
Gesicht sind semantische Urteile ueber die Gesamtkomposition. Der Agent hat das Bild ohnehin
im Kontext (Read-Tool) — der Blick kostet nur Disziplin, kein Tooling. Genau wie §9/§11b die
„Intelligenz beim Agenten, Mechanik im Modul"-Linie ziehen, zieht §15 sie fuer die Qualitaets-
Abnahme des fertigen Creatives.

## 16. Landingpage (Content-Type) — reproduzierbares LP-Bau-System (SKILL-105)

Neben **Bild** (Playwright/HTML-CSS) und **Video** (Remotion) kennt der Skill den Content-Type
**`landingpage`**: eine brand-konforme, konvertierende Warteliste-/Angebots-LP, die aus **Content
(Sektions-Texte) + Brand-Tokens** entsteht — genau wie Bild/Video nichts Projektspezifisches
hartkodiert. Anders als der Bild-/Video-Pfad gibt es keinen Renderer-Aufruf, sondern ein
**wiederverwendbares HTML/CSS/JS-Geruest**: `templates/landingpage/index.template.html`
(+ `README.md`). Vorbild/Referenz-Implementierung: die warteliste-02-LP von AgentischesArbeiten
(`landing/warteliste-02/index.html` + Bau-Briefing `_briefing.md`).

> [!important] Kern-Learning: „Auf Mobile ist eine Spalte die Loesung, auf Desktop das Problem"
> Eine LP wird **mobile-first** gedacht (eine Spalte, voll-breite CTAs). Aber ab dem
> Desktop-Breakpoint darf sie **nicht** die zentrierte Handy-Spalte nur breiter ziehen (riesige
> tote Raender, kalt-techy SaaS-Look). Desktop = **eigenstaendige, editoriale Buehne**:
> zweispaltiger Founder-Hero (Founder **erlebbar**, Magazin-Cover-Gefuehl), Serif-Display-Headlines,
> warmer Cream/Navy-Farb-Rhythmus, breiter aber strukturierter Container (~1180px) mit einer
> ruhigen Lesespalte (~680px). Das ist der Unterschied zwischen „hochskaliertes Handy" und
> „Personal-Brand-Auftritt".

### 16a. Sektions-Struktur (Zweck je Sektion)

Reihenfolge folgt der bewaehrten Waitlist-Architektur (Outcome-Hero → Qualifikation → Mechanismus
→ Beweis → Angebot → CTA-Wiederholung, „eine Aktion, oft wiederholt"). Jede Sektion ist im Template
ein kommentierter Block:

| # | Sektion | Zweck |
|---|---|---|
| S0 | **Sticky-CTA-Header** | Oben-CTA immer sichtbar; Wortmarke + ein Coral-Button auf `#warteliste`. **Keine Navigation** (distraktionsfrei). |
| S1 | **Zweispaltiger Founder-Hero** ★ | In 2 Sek Ergebnis + eine Handlung. Links Kicker+H1(Serif)+Subline+CTA+Micro-Trust, rechts grosses Founder-Foto (Coral-Versatzrahmen, Stat-Tag). Message-Match zur Ad. LCP-Element. |
| S2 | **Ad-Erkennungswert / Message-Bridge** | Der aus der Ad kommende Besucher findet „seine" Zeile wieder (Kontinuitaet senkt Bounce) + Selbst-Qualifikation. Editorial-Pull-Quotes (Serif, Coral-Rule links). |
| S3 | **Der wahre Engpass** (Problem) | Problem benennen, das der Kunde selbst fuehlt (Stress/Abhaengigkeit erlaubt), **sofort nach vorne aufloesen**. Schmale Lesespalte, grosse Serif-Zwischenzeile. Kurz, KEINE Textwand. |
| S4 | **Mechanismus** (Kategorie-Reframe) | Die eine Idee, die alles traegt (z.B. Agent ≠ Chatbot; Durchsatz entkoppelt von Kopfzahl). Kontrast-Zweispalter + optionaler 3-Schritt-Karten-Grid. |
| S5 | **Dimensionen entwaessert** | Zeigen, dass es an allen Fronten besser wird — aber **je Punkt eine szenische + eine Nutzenzeile (max ~20 Woerter)**, kein langer Absatz. Editorial-Zeilen (Name links Coral, Text rechts). |
| S6 | **Format / Angebot** | Erwartung setzen (**kein Preis**): Zeitinvest, wer mitkommt, aus der eigenen Praxis. 4 Karten (2×2 auf Desktop). |
| S7 | **Beweis-Layer** ★ | Staerkster Trust-Block: Founder lebt es selbst vor („einer von euch"). Stat-Hero-Behandlung (grosse Coral-Zahl + ruhiger Kontext), Founder-Foto, Navy-Sektion fuer Ernst. **Nur freigegebene Zahlen** (siehe 16f). |
| S8 | **Testimonial** (optional) | Named Mentors/Referenzen > anonyme Sterne. **Struktur bauen, leer/aus bis echtes Testimonial + Freigabe da** — nie erfinden (Anti-Fake). |
| S9 | **Warteliste-Formular** ★ | Conversion. Wenige Pflichtfelder + **eine bewusste Vorqualifizierungs-Frage** (z.B. Team-Groesse). Schmale zentrierte Karte, 16px-Inputs, Erfolgs-View + Next-Step. |
| S10 | **Footer** | Rechtslinks (Impressum/Datenschutz/AGB/Widerruf), Social, Wortmarke. Schlicht. + Consent-Banner (DSGVO). |

Zusatz: **Mobile-Sticky-CTA** (nur `max-width:719px`) haelt die Aktion am Daumen erreichbar.

### 16b. Editorial-Desktop-Prinzip (das Kern-Layout)

- **Mobile-first Basis:** alles eine Spalte, CTAs voll-breit + zentriert, Tap-Targets ≥44px,
  Inputs `font-size:16px` (iOS-Zoom-Regel), kein Horizontal-Scroll (`overflow-x:hidden` + `max-width:100%`).
- **Desktop-Umschaltung ueber Breakpoints** (Referenz: 720px = zweispaltige Quotes/Contrast/Dims/Cards;
  960px = asymmetrischer Hero-Grid `1.05fr 0.95fr` + Proof-Grid). Der Hero wird **nie** zentriert
  gestapelt auf Desktop, sondern links Copy / rechts Founder-Figur.
- **Warmer Farb-Rhythmus statt durchgehend Navy:** `.band--cream` / `.band--cream-alt` als Grundton
  fuer Content-/Vertrauens-Sektionen, `.band--navy` als dramatischer Kontrast fuer Hero + Beweis.
  **Coral ist der EINE Akzent** (CTA, Kicker, Zahlen), nicht Buntheit.
- **Serif-Display fuer H1/H2** (redaktionell/Personal-Brand), **Grotesk/Sans fuer Body**. Die
  Serif-Headline ist der schnellste Hebel weg vom „SaaS-Tech"-Look. Fluide `clamp()`-Skala mit
  **hohen Mobile-Minima**.
- **Struktur statt Leere:** Container ~1180px, Lesespalte (`.measure`) ~680px, gezielte Weissraeume,
  Pull-Quotes / Zahlen-Karten / Rules statt Textwaende.

### 16c. Brand-Tokens (Pflicht — ADR-010)

**Kein hartkodierter Brand-Hex/-Font.** Die LP mappt lokale Aliase auf die `--brand-*`-Tokens aus
`tokens.css` (Quelle `branding.env`), mit **Live-Default als Fallback**, falls `tokens.css` fehlt
(z.B. beim `file://`-Test):

```css
:root{
  --navy:  var(--brand-bg,     #0a0e27);
  --cream: var(--brand-ink,    #faf7f2);
  --coral: var(--brand-accent, #f25d3e);
  /* Sekundaerfarben tokenbasiert ableiten, nicht neu hardcoden: */
  --on-cream-muted: color-mix(in srgb, var(--navy) 66%, var(--cream));
  --cream-alt:      color-mix(in srgb, var(--cream) 88%, var(--navy));
}
```

Marke aendern = **nur `branding.env`** → `gen-tokens.ps1` rendert `tokens.css` (laeuft im
`deploy-landing.ps1`). **Fonts self-hosted** per `@font-face` (Serif-Display + Body als eingebettete
oder mitgelieferte woff2) — **kein externer CDN** (Deploy nutzt scp auf VPS; `file://`-Test hat keinen
Netzzugang; ausserdem CWV/Datenschutz).

### 16d. Dynamischer Szenen-Match (Conversion-Feature)

Message-Match Ad↔LP: die Hero-H1 wird per `utm_content` (= Ad-Slug) auf die **Szene der Ad** getauscht,
aus der der Besucher kommt — der aus der Ad Kommende sieht „seine" Zeile wieder (senkt Bounce). Muster
(im Template als Platzhalter-Block):

```js
var HERO_SCENES = [
  { m: ["<ad-slug-fragment>", "<synonym>"], h1: '<Szene> <em><Aufloesung.</em>' },
  // ... ein Eintrag je live geschaltetem Top-Ad-Slug ...
];
function swapHeroForUtm(){
  try {
    var c = (currentUtm().utm_content || "").toLowerCase();
    if(!c) return;
    var el = document.getElementById("hero-h1"); if(!el) return;
    for (var i=0;i<HERO_SCENES.length;i++)
      for (var j=0;j<HERO_SCENES[i].m.length;j++)
        if (c.indexOf(HERO_SCENES[i].m[j])!==-1){ el.innerHTML = HERO_SCENES[i].h1; return; }
  } catch(e){ /* starker Default-Hero bleibt stehen */ }
}
```

Regeln: **Fragment-Match** (greift auch bei utm-Praefix/-Suffix), **robust in try/catch**, **kein
Treffer → starker Default-Hero bleibt**. Jeder live geschaltete Top-Ad-Slug braucht einen Eintrag;
den Match auch mit dem abgeleiteten `zielgruppe`-Formularfeld konsistent halten (nicht brechen).

### 16e. Voice-Regeln (verbindlich)

Dieselbe Copy-Disziplin wie bei Ad-/Reel-Copy (§4c / SKILL-087 / SKILL-101/104):

- **„du", nie „Geschaeftsfuehrer"** — auf Augenhoehe, einer von euch.
- **Szene statt These** — jeder Kernsatz zeigt einen konkreten Moment (Uhrzeit/Ort/Handgriff),
  keine abstrakte Nutzen-Behauptung (das Konkretheits-Gate aus SKILL-104 gilt auch auf der LP).
- **Motivation statt Angst** — nach vorne (Wachstum/Freiheit), kein FOMO/Fake-Countdown.
- **Keine Tool-/Produktnamen, keine Buzzwords**; „KI" nur als konkrete Loesungsbenennung.
- **KEINE Gedankenstriche** (Em-/En-Dash —/– sind tabu, wirken nach KI; normaler Bindestrich in
  Komposita bleibt) — identisch zur Copy-Anti-Liste §4c.
- **Kein Preis** auf der LP; Verknappung nur **ehrlich** („Plaetze begrenzt, Warteliste = Reihenfolge").
- Marken-Voice-Adjektive/Leitplanken kommen aus der **Brand** (Doku/Parameter), nicht hartkodiert.

### 16f. Beweis-Zahlen-Governance

Auf die LP duerfen **nur freigegebene Zahlen**. Referenz-Regel aus dem warteliste-Briefing:
die **16 → 30**-Zahl ist freigegeben/live nutzbar (steht im Workbook, laeuft in allen Ads); **andere
Zahlen** (z.B. Margen, Folgejahr-Skalierung, Bewerbungs-/Standort-Zahlen) gehen **erst nach
Einzel-Freigabe** durch den Auftraggeber auf die LP. Framing-Pflicht: Zahlen immer als
**Skalierungs-Beweis**, nie als blosse Effizienz-Anekdote. Nichts erfinden (Anti-Fake).

### 16g. Vision-QA-Pflicht (nicht „fertig" ohne Blick)

Analog zum Bild-Vision-QA (§15): eine LP gilt erst als fertig, wenn der **Agent die gerenderte Seite
selbst angeschaut** hat — **Desktop 1440 UND Mobile 390**, jeweils **Default-Hero UND mindestens
eine utm-Szene** (`?utm_content=<slug>`), plus die Erfolgs-View des Formulars. Geprueft wird:
kein Horizontal-Scroll, Founder-Gesicht frei, Umlaute korrekt (kein Tofu/Mojibake), Kontrast
(WCAG-AA), Tap-Targets ≥44px, Editorial-Desktop greift wirklich (nicht die hochskalierte
Handy-Spalte), Szenen-Match tauscht die H1. Fuer web-Surfaces gilt zusaetzlich die Projekt-Regel
**surface: web ⇒ Playwright/UI-Verifier-Pflicht** (Desktop- + Mobile-Viewport), und der
`web-mobile-design`-Skill ist die Bau-Checkliste, **bevor** HTML/CSS geschrieben wird.

### 16h. Von Content + Brand-Tokens zur LP (Ablauf)

1. `templates/landingpage/index.template.html` in `landing/<site>/index.html` kopieren.
2. Brand-Tokens binden: `tokens.css` aus `branding.env` rendern lassen und einbinden; Fonts einbetten.
3. Sektions-Copy je Block fuellen (Voice-Regeln 16e), nur freigegebene Zahlen (16f).
4. `HERO_SCENES` an die live geschalteten Ad-Slugs binden (16d).
5. Vision-QA (16g): Desktop 1440 + Mobile 390, Default + utm-Szene.

Details Schritt-fuer-Schritt: `templates/landingpage/README.md`.
