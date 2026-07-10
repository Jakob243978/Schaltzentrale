"""creative-studio — Meta-Ad-Spezifikationen + Content-Klasse (SKILL-020).

Kodiert die Recherche-Ergebnisse vom 2026-06-23 als verwendbaren Code (statt nur Doku):
  - docs/marketing/ad-creative-specs.md  -> Formate, Safe-Zones, technische Specs, Text-Regel, Fallstricke
Single Source of Truth fuer die Format-/Safe-Zone-Anforderungen — genutzt von render_image.py
(Bild) und spaeter vom Video-Modul (SKILL-021), damit Bild + Video dieselben Specs teilen.

Multi-Projekt: enthaelt KEINE projekt-spezifischen Werte (kein Brand-Hex, kein Pfad) — nur die
plattform-Anforderungen von Meta. Brand-Tokens + Content kommen zur Laufzeit rein.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class AdFormat:
    """Ein Meta-Ad-Ausgabeformat inkl. Safe-Zones (Anteile der Canvas).

    Safe-Zone-Anteile aus ad-creative-specs.md (Stand 2026): Bereiche, die von der
    Meta-UI verdeckt werden und frei von Text/Logo/CTA bleiben muessen.
    """
    key: str
    ratio: str
    width: int
    height: int
    safe_top_pct: float
    safe_bottom_pct: float
    safe_x_pct: float
    placements: tuple[str, ...]
    note: str = ""

    @property
    def safe_top(self) -> int:
        return round(self.height * self.safe_top_pct)

    @property
    def safe_bottom(self) -> int:
        return round(self.height * self.safe_bottom_pct)

    @property
    def safe_x(self) -> int:
        return round(self.width * self.safe_x_pct)


# --- Format-Katalog (aus der Recherche) -------------------------------------
# 4:5 = Metas Feed-Default 2026; 9:16 = Stories/Reels (untere 35 % frei);
# 1:1 = Karussell/Alternative.
FORMATS: dict[str, AdFormat] = {
    "feed_4x5": AdFormat(
        key="feed_4x5", ratio="4:5", width=1080, height=1350,
        safe_top_pct=0.14, safe_bottom_pct=0.20, safe_x_pct=0.055,
        placements=("facebook_feed", "instagram_feed"),
        note="Meta-Default fuers Feed 2026 (~25 % mehr Mobile-Screen als 1:1).",
    ),
    "story_9x16": AdFormat(
        key="story_9x16", ratio="9:16", width=1080, height=1920,
        safe_top_pct=0.14, safe_bottom_pct=0.35, safe_x_pct=0.06,
        placements=("facebook_stories", "instagram_stories", "facebook_reels", "instagram_reels"),
        note="Stories/Reels. Konservativ untere 35 % frei (Reels-Wert) -> passt ueberall.",
    ),
    "square_1x1": AdFormat(
        key="square_1x1", ratio="1:1", width=1080, height=1080,
        safe_top_pct=0.10, safe_bottom_pct=0.16, safe_x_pct=0.055,
        placements=("feed_alt", "carousel"),
        note="Karussell-Karte / Feed-Alternative.",
    ),
}

# SKILL-076: Standard-Set = ALLE DREI Meta-Standard-Formate. Ein Creative wird per
# Default IMMER in 1:1 (Feed square), 4:5 (Feed portrait) UND 9:16 (Story/Reels)
# gerendert — 4:5 ist Metas Feed-Default 2026 und darf nie stillschweigend fehlen.
# (Vor SKILL-076 nur ("feed_4x5", "story_9x16") -> 1:1 bzw. 4:5 fielen weg, je nachdem
#  was der Aufrufer explizit anforderte; die Workshop-Ads kamen so ohne 4:5 raus.)
# Reihenfolge = Meta-Standard 1:1 -> 4:5 -> 9:16. Abweichung nur, wenn der Aufrufer
# bewusst eine kleinere Format-Liste uebergibt.
DEFAULT_FORMATS: tuple[str, ...] = ("square_1x1", "feed_4x5", "story_9x16")

# --- Technische Constraints + Best-Practice-Regeln (aus der Recherche) ------
MIN_EDGE_PX = 1080          # praktischer Mindest-Kantenwert; hoeher = Auktions-Vorteil (Andromeda)
RECOMMENDED_EDGE_PX = 1080  # bis 1440 ideal
MAX_FILE_MB = 30
COLOR_SPACE = "sRGB"        # nie CMYK
HEADLINE_MAX_CHARS = 27     # Headline (Feld ausserhalb des Bildes)
PRIMARY_TEXT_RANGE = (50, 150)
# Text-im-Bild: 20-%-Regel ist tot (abgeschafft 2020) -> keine Ablehnung, aber Empfehlung < 20 %.
TEXT_IN_IMAGE_HARD_LIMIT = False

# DACH-/Coaching-Fallstrick: persoenliche "Du + Vorher-Nachher"-Claims werden von Meta schnell
# abgelehnt. Heuristik-Trigger fuer eine Warnung (keine harte Sperre).
COACHING_CLAIM_TRIGGERS = (
    "du verdoppelst", "wir haben bemerkt", "dein leben", "verändere dich",
    "aus dir wird", "du schaffst", "endlich erfolgreich",
)

# === SKILL-026: DACH-Compliance-Guard (UWG/HWG-Heuristik) =====================
# Ausbau des Coaching-Guards zu dokumentierten Trigger-Sets nach Rechtsgrundlage.
# Wissensgrundlage: AgentischesArbeiten/docs/marketing/research/
#   2026-06-23_ad-copywriting-frameworks.md (§2.4 DACH-Fallstricke, §3.6 Message-Match).
# WICHTIG: Heuristik, KEINE Rechtsberatung und KEINE harte Sperre — alles bleibt
# Warnung an den Menschen (Mensch-im-Loop). Wortlaut bewusst sachlich:
# "abmahngefaehrdet/pruefen", nie "verboten".
#
# SKILL-026: Jede Kategorie ist ein Tupel kleingeschriebener Substring-Trigger +
# ein Risiko-Klartext (Rechtsgrundlage + Abmahn-Hinweis), der in jeden Warntext
# einfliesst (EARS-2).

# SKILL-026: Garantie-/Sicherheits-Claims ohne Beleg -> UWG §5 (irrefuehrend).
GUARANTEE_TRIGGERS = (
    "garantiert", "garantie", "100 % erfolg", "100% erfolg", "100 %ig", "100%ig",
    "sicherer erfolg", "erfolg sicher", "risikofrei", "kein risiko",
)

# SKILL-026: Unbelegte Spitzenstellung/Superlative -> UWG §5 (irrefuehrende Spitzenstellung).
SUPERLATIVE_UNPROVEN = (
    "beste", "bester", "bestes", "nr. 1", "nr.1", "nummer 1", "nummer eins",
    "marktführer", "weltbeste", "einzigartig am markt", "konkurrenzlos",
)

# SKILL-026: Erfolgs-/Ergebnis-Versprechen (person-/transformationsbezogen) -> UWG §5.
SUCCESS_PROMISE_TRIGGERS = (
    "verdopple deinen umsatz", "verdoppeln sie ihren umsatz", "verdreifache",
    "umsatz verdoppeln", "in 30 tagen zu", "in 7 tagen zu", "in x tagen zu",
    "in 6 monaten zu", "schnell reich", "passives einkommen garantiert",
)

# SKILL-026: Gesundheits-/Heilbezug -> HWG (Heilmittelwerbegesetz).
HEALTH_TRIGGERS = (
    "heilt", "heilung", "heilen", "burnout heilen", "stress weg",
    "macht gesund", "gesundheitsfördernd", "schmerzfrei", "therapiert",
    "depression weg", "angst weg",
)

# SKILL-026: Fake-Verknappung / Druck -> UWG Schwarze Liste (Anhang zu §3).
SCARCITY_FAKE = (
    "nur heute", "nur noch heute", "letzte plätze", "letzter platz",
    "nur noch wenige plätze", "nur für kurze zeit", "läuft heute ab",
    "angebot endet heute", "jetzt oder nie",
)

# SKILL-026: Vorher-Nachher-Transformations-Claims -> UWG §5 + Coaching-Fallstrick.
BEFORE_AFTER_TRIGGERS = (
    "vorher nachher", "vorher-nachher", "aus arm wird reich",
    "vom anfänger zum profi", "vom nichts zum",
)

# SKILL-026: Mapping Trigger-Set -> Risiko-Klartext (Rechtsgrundlage + Abmahn-Hinweis).
# Reihenfolge bestimmt die Pruef-Reihenfolge in compliance_warnings().
COMPLIANCE_TRIGGER_SETS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("Garantie-/Erfolgsgarantie-Claim", GUARANTEE_TRIGGERS,
     "UWG §5 (irrefuehrende Werbung) — unbelegte Garantie/Erfolgssicherheit ist "
     "abmahngefaehrdet. Beleg ergaenzen oder produkt-/prozessbezogen formulieren."),
    ("Unbelegte Spitzenstellung/Superlativ", SUPERLATIVE_UNPROVEN,
     "UWG §5 (irrefuehrende Spitzenstellung) — 'beste'/'Nr. 1' ohne nachweisbare "
     "Grundlage ist abmahngefaehrdet. Belegen oder relativieren."),
    ("Erfolgs-/Ergebnis-Versprechen", SUCCESS_PROMISE_TRIGGERS,
     "UWG §5 (irrefuehrende Werbung) — person-/transformationsbezogenes "
     "Ergebnisversprechen ist abmahngefaehrdet. Outcome produkt-/prozessbezogen "
     "und belegbar formulieren."),
    ("Gesundheits-/Heilbezug", HEALTH_TRIGGERS,
     "HWG (Heilmittelwerbegesetz) — gesundheits-/heilbezogene Aussage ist "
     "abmahngefaehrdet. Heilversprechen vermeiden (HWG pruefen)."),
    ("Fake-Verknappung/Druck", SCARCITY_FAKE,
     "UWG Schwarze Liste (Anhang zu §3) — kuenstliche/falsche Verknappung ist "
     "per se unzulaessig und abmahngefaehrdet. Nur echte Limitierung nennen."),
    ("Vorher-Nachher-Transformation", BEFORE_AFTER_TRIGGERS,
     "UWG §5 + Coaching-Fallstrick — uebertriebene Vorher-Nachher-Claims sind "
     "abmahngefaehrdet und werden von Meta oft abgelehnt. Sachlich formulieren."),
    ("Coaching-Claim", COACHING_CLAIM_TRIGGERS,
     "Coaching-Fallstrick (UWG §5 / Meta-Policy) — persoenliche 'Du'-/Vorher-"
     "Nachher-Versprechen werden von Meta oft abgelehnt. Neutral/produktbezogen "
     "formulieren."),
)

# SKILL-026: Stoppwoerter fuer die Message-Match-Heuristik (Ad-Headline <-> LP-Promise).
# Bewusst projektneutral (DE-Funktionswoerter), kein Brand-/Projektbegriff.
_MATCH_STOPWORDS = frozenset({
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer",
    "und", "oder", "aber", "mit", "ohne", "für", "fuer", "auf", "aus", "von", "vom",
    "zu", "zur", "zum", "im", "in", "an", "am", "ist", "sind", "war", "wird", "werden",
    "du", "dein", "deine", "deinen", "sie", "ihr", "ihre", "ihren", "wir", "uns", "unser",
    "so", "wie", "was", "wer", "auch", "noch", "nur", "schon", "jetzt", "mehr", "sehr",
    "the", "and", "for", "with", "your", "you",
})

_WORD_RE = re.compile(r"[a-zäöüß0-9]+", re.IGNORECASE)


def _core_terms(text: str) -> set[str]:
    """SKILL-026: Kern-Begriffe eines Textes fuer die Message-Match-Heuristik.

    lowercase, Tokens >= 4 Zeichen ohne Stoppwoerter. >= 4 vermeidet, dass kurze
    Funktionswoerter als 'Kern' zaehlen — projektneutral, keine Brand-Begriffe.
    """
    terms = set()
    for tok in _WORD_RE.findall(text.lower()):
        if len(tok) >= 4 and tok not in _MATCH_STOPWORDS:
            terms.add(tok)
    return terms


def compliance_warnings(text: str) -> list[str]:
    """SKILL-026: DACH-Compliance-Heuristik (UWG/HWG) als reine Warn-Funktion.

    Prueft `text` gegen alle COMPLIANCE_TRIGGER_SETS und liefert pro Treffer eine
    Warnung mit Rechtsgrundlage + Abmahn-Hinweis (EARS-1/EARS-2). KEINE harte
    Sperre, KEINE Rechtsberatung — Mensch entscheidet final.

    Projektneutral (EARS-5): nur DACH-Rechtsmuster, keine projekt-spezifischen
    Claims hartkodiert. Wiederverwendbar ausserhalb von AdContent.
    """
    blob = (text or "").lower()
    out: list[str] = []
    for label, triggers, risk in COMPLIANCE_TRIGGER_SETS:
        for trig in triggers:
            if trig in blob:
                out.append(f"{label}-Risiko: '{trig}' — {risk}")
    return out


def message_match_warning(headline: str, landing_promise: str) -> str | None:
    """SKILL-026: Ad<->LP-Message-Match-Heuristik (§3.6).

    Gibt eine Warnung zurueck, wenn `landing_promise` gesetzt ist und KEINE
    Kern-Begriffe der Headline in der LP-Promise auftauchen (oder umgekehrt) —
    Mismatch kostet CVR + Relevanz-Score (EARS-3). Ist `landing_promise` leer,
    gibt es keine Warnung (EARS-4). Reine Heuristik, keine Sperre.
    """
    if not (landing_promise or "").strip():
        return None  # EARS-4: Feld optional -> keine Warnung
    head_terms = _core_terms(headline)
    lp_terms = _core_terms(landing_promise)
    if not head_terms or not lp_terms:
        return None  # zu wenig Substanz fuer eine sinnvolle Aussage
    if head_terms & lp_terms:
        return None  # mind. ein gemeinsamer Kern-Begriff -> Match ok
    return (
        "Message-Match-Risiko: Ad-Headline und Landingpage-Promise teilen keinen "
        "Kern-Begriff — Mismatch senkt CVR + Relevanz-Score (§3.6). Hook/Outcome "
        "der Ad oben auf der LP woertlich/visuell wieder aufnehmen."
    )


# === SKILL-028: KI-Disclosure-Gate (Pflicht-Label + Metadaten) ================
# Sobald KI ein Creative generiert/substanziell veraendert/composited hat —
# explizit inkl. synthetischer Stimme/Voice-Clone (SKILL-027) — ist eine
# sichtbare KI-Kennzeichnung Pflicht: Meta-Policy (2026) + EU-AI-Act ab
# 02.08.2026 (sichtbares Label + maschinenlesbare Metadaten; Strafrahmen bis
# 3 % Jahresumsatz / 15 Mio. EUR). "Undisclosed AI Content" ist 2026 der
# drittgroesste Meta-Ablehnungsgrund (~14 %).
# Wissensgrundlage: AgentischesArbeiten/docs/marketing/research/
#   2026-06-23_ki-avatare-voiceover.md (§3 Pflicht-Disclosure).
#
# Multi-Projekt (EARS-5): KEIN projekt-spezifischer Label-Text/Pfad hartkodiert.
# Label-Text ist eine Konstante mit Default; die Marke kann ihn ueberschreiben.
# Der Interim-Default in DE laut Recherche ist "KI"; wir nutzen den sachlich
# eindeutigen Wortlaut "KI-generiert" als projektneutralen Default.

# SKILL-028: Pflicht-Stichtag EU-AI-Act (sichtbare Offenlegung + Metadaten).
AI_ACT_ENFORCEMENT_DATE = "2026-08-02"

# SKILL-028: projektneutraler Default-Wortlaut des sichtbaren KI-Labels.
AI_LABEL_TEXT = "KI-generiert"


def requires_ai_disclosure(content: "AdContent") -> bool:
    """SKILL-028 EARS-1/EARS-3/EARS-4: Braucht dieses Creative ein KI-Disclosure?

    True, sobald ein KI-generiertes Bild ODER eine synthetische Stimme/Voice-Clone
    im Creative steckt (`ai_image` oder `ai_voice`). False fuer rein echtes
    Eigen-Material (kein KI-Bild, keine synthetische Stimme) — nur echte
    KI-Anteile triggern das Gate (EARS-4). Projektneutral, keine Brand-Werte.
    """
    return bool(content.ai_image or content.ai_voice)


@dataclass
class AdContent:
    """Der medien-unabhaengige Inhalt eines Creatives (Bild + spaeter Video teilen ihn).

    Headline/CTA etc. sind der TEXT IM BILD. Validierung liefert nur WARNUNGEN
    (keine harten Sperren) gemaess Recherche-Regeln.
    """
    headline: str
    subline: str = ""
    cta: str = ""
    eyebrow: str = ""
    brand_name: str = ""
    bg_image: str = ""              # optionaler Pfad/URL zum Hintergrundmotiv
    ad_id: str = ""                 # z.B. "h1-immo" (fuer UTM/Dateinamen)
    landing_promise: str = ""       # SKILL-026: optionale LP-Promise fuer Ad<->LP-Message-Match
    # SKILL-028: KI-Anteil-Flags. ai_image = KI-generiertes/compositetes Bild,
    # ai_voice = synthetische Stimme / Voice-Clone (SKILL-027). Default False ->
    # bestehende Aufrufer (rein echtes Material) brechen nicht (EARS-4).
    ai_image: bool = False
    ai_voice: bool = False
    # SKILL-028: hat der Renderer das sichtbare Disclosure-Label tatsaechlich
    # gesetzt? Default False; sobald requires_ai_disclosure() True ist, aber
    # disclosure_applied False bleibt, warnt warnings() (EARS-3 Pflichtfeld).
    disclosure_applied: bool = False

    def warnings(self) -> list[str]:
        out: list[str] = []
        blob = " ".join([self.eyebrow, self.headline, self.subline, self.cta])
        # SKILL-026: DACH-Compliance-Heuristik (UWG/HWG) — deckt Coaching-Trigger
        # mit ab (COMPLIANCE_TRIGGER_SETS enthaelt COACHING_CLAIM_TRIGGERS). Reine
        # Warnungen, keine harte Sperre.
        out.extend(compliance_warnings(blob))
        # SKILL-026: Ad<->LP-Message-Match (nur wenn landing_promise gesetzt ist).
        mm = message_match_warning(self.headline, self.landing_promise)
        if mm:
            out.append(mm)
        # SKILL-028: KI-Disclosure-Gate. Wenn ein KI-Element gesetzt ist, aber das
        # sichtbare Label noch nicht aktiviert wurde, sachlicher Pflicht-Hinweis
        # (EARS-1/EARS-3). Reine Warnung, keine harte Sperre — Mensch-im-Loop.
        if requires_ai_disclosure(self) and not self.disclosure_applied:
            kind = []
            if self.ai_image:
                kind.append("KI-Bild")
            if self.ai_voice:
                kind.append("synthetische Stimme")
            out.append(
                f"KI-Disclosure-Pflicht: {' + '.join(kind)} erkannt, aber kein "
                f"sichtbares '{AI_LABEL_TEXT}'-Label gesetzt. Meta-Policy + "
                f"EU-AI-Act (ab {AI_ACT_ENFORCEMENT_DATE}) verlangen sichtbares "
                "Label + maschinenlesbare Metadaten. Disclosure aktivieren "
                "(ai_disclosure-Flag im Renderer)."
            )
        if len(self.headline) > 90:
            out.append("Headline sehr lang fuers Bild — kuerzen (Lesbarkeit auf Mobile).")
        return out


def get_format(key: str) -> AdFormat:
    if key not in FORMATS:
        raise KeyError(f"Unbekanntes Format '{key}'. Bekannt: {', '.join(FORMATS)}")
    return FORMATS[key]


# === SKILL-024: Variant-ID- & UTM-Systematik (Single Source fuer Naming) =====
# Single Source of Truth fuer die Benennung jeder gerenderten Variante. Batch-Engine
# (SKILL-023), DCO-Export (SKILL-031) und Reporting (SKILL-033) MUESSEN diese
# Funktionen aufrufen — kein paralleles Namensschema in anderen Modulen.
#
# Schema (positional, lowercase, kollisionsfrei):
#   variant_id  = "<ad_id>__<framework>-h<NN>__<format>"     (interne, dateiname-taugliche ID)
#   utm_content = "<ad_id>-<format>-<framework>-h<NN>"        (im Meta-Insights-Pull wiederauffindbar)
#
# Trenner-Konvention:
#   "__"  trennt die logischen Bloecke (ad_id / inhalt / format) der variant_id.
#   "-"   trennt Tokens innerhalb eines Blocks bzw. im utm_content (UTM-Best-Practice).
#   "h<NN>" = Hook-Index, nullbasiert, 2-stellig genullt (h00, h01, ...) -> stabile Sortierung.
#
# Multi-Projekt (EARS-4): KEIN hartkodierter Projektwert hier — der Projekt-Praefix
# kommt ausschliesslich ueber den Parameter `ad_id` rein.

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """Deterministische Normalisierung auf [a-z0-9-] (SKILL-024 EARS-3).

    lowercase, deutsche Umlaute/ss werden transliteriert, alle uebrigen
    Sonderzeichen/Leerzeichen werden zu einem einzelnen '-' zusammengefasst,
    fuehrende/abschliessende '-' entfernt. Leere/zeichenlose Eingabe -> "x"
    (nie ein leerer Token, der zu kollidierenden IDs verkettet).
    """
    if value is None:
        value = ""
    s = str(value).strip().lower()
    # deutsche Sonderzeichen transliterieren, bevor sie verschluckt werden
    for src, dst in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(src, dst)
    s = _SLUG_RE.sub("-", s).strip("-")
    return s or "x"


def make_variant_id(ad_id: str, hook: str, framework: str, fmt_key: str,
                    hook_index: int | None = None) -> str:
    """Deterministische, eindeutige variant_id fuer (ad_id, hook, framework, format).

    SKILL-024 EARS-1: gleiche Eingabe -> gleiche ID; unterschiedliche Eingabe ->
    unterschiedliche ID (kollisionsfrei). Die Eindeutigkeit kommt aus dem
    Hook-Index `hook_index` (Position der Variante im Job): zwei Varianten mit
    identischem Framework/Format aber verschiedenem Index erhalten verschiedene IDs.
    Ist kein Index gegeben, wird der Hook-Text selbst slugifiziert (Fallback).

    Format: "<ad_id>__<framework>-h<NN>__<format>" bzw.
            "<ad_id>__<framework>-<hookslug>__<format>" (ohne Index).
    """
    ad = slugify(ad_id)
    fw = slugify(framework)
    fmt = slugify(fmt_key)
    if hook_index is not None:
        hook_token = f"h{int(hook_index):02d}"
    else:
        hook_token = slugify(hook)
    return f"{ad}__{fw}-{hook_token}__{fmt}"


def make_utm_content(variant_id: str) -> str:
    """Leitet aus einer variant_id das positionale `utm_content` ab (SKILL-024 EARS-2).

    Wandelt die Block-Struktur "<ad_id>__<framework>-h<NN>__<format>" in das
    flache, UTM-taugliche Schema "<ad_id>-<format>-<framework>-h<NN>" um:
    positional, lowercase, nur [a-z0-9-]. Dieses utm_content ist im
    Meta-Insights-Pull (`ads_insights_*`) 1:1 wiederauffindbar (Performance-Loop).

    Robust gegen abweichend geformte IDs: alle Bloecke werden re-slugifiziert.
    """
    parts = variant_id.split("__")
    if len(parts) == 3:
        ad, content_block, fmt = parts
        return slugify(f"{ad}-{fmt}-{content_block}")
    # Fallback: Gesamt-ID slugifizieren (kein stiller Crash)
    return slugify(variant_id)


# === SKILL-038: UTM-Naming-Standard als dokumentierte Konstanten =============
# Single Source fuer die UTM-/Makro-Defaults, damit das Schema nicht driftet
# (case-sensitive GA4/DB, gemischte Trenner, falsche Makro-Syntax). make_url_tags
# / make_link_url (SKILL-036) referenzieren DIESE Konstanten statt Literale.
# Wissensgrundlage: AgentischesArbeiten/docs/marketing/research/
#   2026-06-24_utm-tracking-skill.md (§1 Meta-Makros, §4 UTM-Naming-Standard).
#
# Multi-Projekt (EARS-6): KEIN projekt-/brand-spezifischer Wert hier. utm_source
# bleibt stabil "meta" (NICHT fb/ig — sonst Doppel-Pflege), utm_medium ist der
# GA4-konforme Kanal-Typ "paid-social"; utm_campaign kommt immer als Arg rein.

# SKILL-038: statische UTM-Defaults (projektneutral, lowercase, nur "-"-Trenner).
UTM_SOURCE_DEFAULT = "meta"          # Netzwerk/Anbieter — stabil, nicht fb/ig
UTM_MEDIUM_DEFAULT = "paid-social"   # GA4-konformer Kanal-Typ fuer bezahlte Ads

# SKILL-038: die ACHT offiziell von Meta unterstuetzten dynamischen URL-Makros
# (doppelte geschweifte Klammern; Meta fuellt sie zur LAUFZEIT beim Klick).
# Frei erfundene Makros werden NICHT ersetzt und landen literal in der URL.
# .name-Makros sind "eingefroren" auf den Veroeffentlichungs-Zeitpunkt + bruechig
# bei Umbenennung -> fuer stabile Joins immer die .id-Makros bevorzugen (§1).
META_MACROS: dict[str, str] = {
    "ad.id": "{{ad.id}}",                       # numerische Ad-ID (stabil) — harter Join-Key
    "ad.name": "{{ad.name}}",                   # Ad-Name (eingefroren, bruechig)
    "adset.id": "{{adset.id}}",                 # numerische Ad-Set-ID (stabil)
    "adset.name": "{{adset.name}}",             # Ad-Set-Name (eingefroren, bruechig)
    "campaign.id": "{{campaign.id}}",           # numerische Kampagnen-ID (stabil)
    "campaign.name": "{{campaign.name}}",       # Kampagnen-Name (eingefroren, bruechig)
    "placement": "{{placement}}",               # Placement-Klartext (Leerzeichen!) -> utm_term
    "site_source_name": "{{site_source_name}}", # Plattform fb/ig/msg/an (kurz, stabil)
}


# === SKILL-036: make_url_tags() + make_link_url() (UTM + Meta-Makros) =========
# Single Source fuer alle UTM-/Makro-Entscheidungen. make_url_tags baut den
# fertigen url_tags-Query-String (statische UTM + dynamische Meta-Makros);
# make_link_url ist der Fallback, der alles in eine nackte LP-URL haengt.
# utm_content kommt 1:1 aus make_utm_content(vid) (SKILL-024) -> stabiler Join-Key
# zwischen Lead-Capture (LP/CRM) und Meta-Insights (ads_insights_*).
# Wissensgrundlage: 2026-06-24_utm-tracking-skill.md (§1, §2, §4, §6 Vorschlag 1).
#
# Multi-Projekt (EARS-4): utm_source/utm_medium/utm_campaign kommen als Parameter
# rein (Defaults aus SKILL-038-Konstanten, utm_campaign Pflicht-Arg) — kein
# hartkodierter Projekt-/Brand-Wert. fbclid/fbc/_fbp sind NICHT Aufgabe dieser
# Funktion (Scope B / LP, §3) — hier ausschliesslich UTM + Makros.


def make_url_tags(
    variant_id: str,
    *,
    utm_campaign: str,
    utm_source: str = UTM_SOURCE_DEFAULT,
    utm_medium: str = UTM_MEDIUM_DEFAULT,
) -> str:
    """SKILL-036: fertiger `url_tags`-Query-String (ohne fuehrendes `?`).

    Kombiniert die STATISCHEN UTM (EARS-1) mit den DYNAMISCHEN Meta-Makros
    (EARS-2). Schema (§4.1 der Recherche):

        utm_source   = <utm_source>            (statisch; Default "meta")
        utm_medium   = <utm_medium>            (statisch; Default "paid-social")
        utm_campaign = <utm_campaign>          (statisch; Pflicht-Arg, versioniert)
        utm_content  = make_utm_content(vid)   (statisch; Join-Key, SKILL-024)
        utm_term     = {{placement}}           (dynamisch; Placement-Klartext)
        utm_platform = {{site_source_name}}    (dynamisch; Plattform fb/ig/msg/an)
        ad_id        = {{ad.id}}               (dynamisch; harter Join-Key)
        cmp_id       = {{campaign.id}}         (dynamisch; stabiler Kampagnen-Key)

    Statische Werte werden slugifiziert (lowercase, nur [a-z0-9-], EARS-6); die
    Makro-Werte bleiben ROH in `{{...}}` (Meta encodet sie zur Laufzeit selbst).
    `utm_content` ist 1:1 `make_utm_content(variant_id)` (EARS-3, kein
    Parallel-Naming). `utm_campaign` ist Pflicht (EARS-4).
    """
    if not (utm_campaign or "").strip():
        raise ValueError("make_url_tags: utm_campaign ist ein Pflicht-Argument (nicht leer).")
    # Statische UTM — slugify haelt sie lowercase + nur "-" (EARS-6).
    static_params: list[tuple[str, str]] = [
        ("utm_source", slugify(utm_source)),
        ("utm_medium", slugify(utm_medium)),
        ("utm_campaign", slugify(utm_campaign)),
        ("utm_content", make_utm_content(variant_id)),
    ]
    # Dynamische Meta-Makros — roh, NICHT url-encoden (EARS-2).
    macro_params: list[tuple[str, str]] = [
        ("utm_term", META_MACROS["placement"]),
        ("utm_platform", META_MACROS["site_source_name"]),
        ("ad_id", META_MACROS["ad.id"]),
        ("cmp_id", META_MACROS["campaign.id"]),
    ]
    return "&".join(f"{k}={v}" for k, v in static_params + macro_params)


def make_link_url(
    base_url: str,
    variant_id: str,
    *,
    utm_campaign: str,
    utm_source: str = UTM_SOURCE_DEFAULT,
    utm_medium: str = UTM_MEDIUM_DEFAULT,
) -> str:
    """SKILL-036 EARS-5: Fallback — dasselbe Param-Set direkt in die `link_url`.

    Verbindet die nackte LP-URL `base_url` mit dem `make_url_tags`-String und
    waehlt korrekt `?` bzw. `&` je nachdem, ob `base_url` bereits einen
    Query-Teil hat. Genutzt, wenn `url_tags` am Ad-Objekt nicht setzbar ist
    (SKILL-037). Ein vorhandenes Fragment (`#...`) bleibt am Ende erhalten.
    """
    tags = make_url_tags(
        variant_id,
        utm_campaign=utm_campaign,
        utm_source=utm_source,
        utm_medium=utm_medium,
    )
    base = base_url or ""
    # Fragment abtrennen, damit Params VOR dem #-Anker landen.
    frag = ""
    if "#" in base:
        base, frag = base.split("#", 1)
        frag = "#" + frag
    sep = "&" if "?" in base else "?"
    return f"{base}{sep}{tags}{frag}"


# === SKILL-039: ContentType-Ebene + CONTENT_TYPES-Katalog =====================
# Neue semantische Ebene UEBER den technischen AdFormat-Formaten. AdFormat bleibt
# das Ausgabe-Format (Ratio/Pixel/Safe-Zone); ContentType beschreibt die
# inhaltliche BAUART (Medium, Funnel-Stufe, erlaubte Formate, Video-Laenge bzw.
# Slide-Anzahl, Hook-Fenster, On-Screen-Wortlimit, empfohlenes Framework).
# Lose Kopplung: ContentType referenziert FORMATS-Keys und frameworks.FRAMEWORKS-
# Keys per String — kein Import von frameworks (vermeidet Import-Zyklus); die
# Keys werden im Test gegen frameworks.FRAMEWORKS validiert.
# Wissensgrundlage: AgentischesArbeiten/docs/marketing/research/
#   2026-06-24_social-content-types.md (§0 Luecke, §3.1 Datenstruktur, §3.2 Katalog).
#
# Multi-Projekt (EARS-5): KEIN hartkodierter Brand-/Projektwert — nur generische
# Content-Typ-Definitionen.

# SKILL-039: On-Screen-Wortlimit-Default. Spiegelt frameworks.MAX_WORDS_ONSCREEN (7)
# OHNE Import (Zyklus-Vermeidung) — der Wert ist hier dokumentiert dupliziert, und
# ein Test sichert die Aequivalenz gegen frameworks.MAX_WORDS_ONSCREEN ab.
ONSCREEN_WORD_LIMIT_DEFAULT = 7


@dataclass(frozen=True)
class ContentType:
    """Eine inhaltliche Content-Bauart (semantische Ebene ueber AdFormat).

    Beschreibt, WIE ein Creative gebaut ist (mehrseitig? Video? Slide-Anzahl?
    On-Screen-Text-Limit? Funnel-Stufe? empfohlenes Framework?) und auf welche
    technischen `FORMATS`-Keys es abgebildet werden darf. Projektneutral.

    Attributes:
        key: stabiler Bezeichner ("carousel", "talking_head", ...).
        name: ausgeschriebener Name fuer UI/Doku.
        medium: "image" | "video" | "multi_image".
        funnel: Funnel-Stufen-Tags, z.B. ("awareness",) oder ("consideration","conversion").
        formats: erlaubte AdFormat-Keys aus FORMATS.
        min_seconds/max_seconds: Video-Laengen-Sweetspot (None fuer Bild-Typen).
        hook_window_seconds: Key-Promise muss bis hierher stehen (None fuer Bild-Typen).
        min_slides/max_slides: Slide-Anzahl-Range (None fuer Single-Image/Video).
        onscreen_word_limit: On-Screen-Wortgrenze (None, wo irrelevant; Video-Default 7).
        recommended_framework: Key aus frameworks.FRAMEWORKS (oder None).
        requires_compliance_check: SKILL-042 — Typ koppelt automatisch compliance_warnings().
        requires_proof: SKILL-042 — Typ braucht einen Beleg-/Echtheits-Hinweis (Testimonial).
        note: optionaler Hinweis (DACH-Vorsicht, B2B-Caveat etc.).
    """
    key: str
    name: str
    medium: str
    funnel: tuple[str, ...]
    formats: tuple[str, ...]
    min_seconds: int | None = None
    max_seconds: int | None = None
    hook_window_seconds: float | None = None
    min_slides: int | None = None
    max_slides: int | None = None
    onscreen_word_limit: int | None = None
    recommended_framework: str | None = None
    requires_compliance_check: bool = False   # SKILL-042
    requires_proof: bool = False              # SKILL-042
    note: str = ""


# SKILL-039 + SKILL-042: Content-Typ-Katalog (Werte aus §3.2 der Recherche).
# SKILL-039 liefert die Basis-Sechs (static_statement, carousel,
# educational_carousel, short_video_text_hook, talking_head, listicle).
# SKILL-042 ergaenzt die beweis-/personenbezogenen Typen (voiceover_broll,
# ugc_style, story_ad, testimonial, testimonial_video, before_after) mit
# Compliance-/Beleg-Kopplung. Alle Werte projektneutral.
CONTENT_TYPES: dict[str, ContentType] = {
    # --- SKILL-039 Basis-Sechs ---------------------------------------------
    "static_statement": ContentType(
        key="static_statement",
        name="Static Statement / Pattern-Naming Hook (Single Image)",
        medium="image",
        funnel=("awareness", "conversion"),
        formats=("feed_4x5", "square_1x1"),
        recommended_framework="pas",
        note="Pattern-naming Hook-Static = B2B-ToF-Gewinner; eine scharfe Aussage, "
             "die das Problem benennt. Billigster/schnellster Test-Slot.",
    ),
    "carousel": ContentType(
        key="carousel",
        name="Carousel-Ad (mehrseitiges Set)",
        medium="multi_image",
        funnel=("consideration", "conversion"),
        formats=("square_1x1", "feed_4x5"),
        min_slides=3,
        max_slides=10,
        recommended_framework="fab",
        note="Karte 1 = Hook, letzte Karte = CTA. Jeder Swipe = Engagement-Signal. "
             "IG-Carousel ~6,90 % ER.",
    ),
    "educational_carousel": ContentType(
        key="educational_carousel",
        name="Educational Carousel / Doc-Post (organisch)",
        medium="multi_image",
        funnel=("awareness", "consideration"),
        formats=("feed_4x5", "square_1x1"),
        min_slides=3,
        max_slides=10,
        recommended_framework="aida",
        note="Autoritaets-/Save-Treiber. Eine Idee/Slide, 'Save this'-CTA. "
             "LI-Doc-Post ~7,00 % / Carousel ~21,77 % ER.",
    ),
    "short_video_text_hook": ContentType(
        key="short_video_text_hook",
        name="Text-on-screen-Hook-Video (faceless)",
        medium="video",
        funnel=("awareness",),
        formats=("story_9x16",),
        min_seconds=8,
        max_seconds=20,
        hook_window_seconds=3.0,
        onscreen_word_limit=ONSCREEN_WORD_LIMIT_DEFAULT,
        recommended_framework="hso",
        note="Faceless, sound-off; entspricht der heutigen Remotion-Composition. "
             "Skalierbares Hook-Testing ohne Gesicht.",
    ),
    "talking_head": ContentType(
        key="talking_head",
        name="Talking-Head (Founder-led)",
        medium="video",
        funnel=("awareness", "consideration"),
        formats=("story_9x16", "square_1x1"),
        min_seconds=20,
        max_seconds=45,
        hook_window_seconds=3.0,
        onscreen_word_limit=ONSCREEN_WORD_LIMIT_DEFAULT,
        recommended_framework="pas",
        note="Founder-led B2B-ToF-Gewinner; Caption Pflicht (sound-off). KI-Avatar/"
             "Voice-Clone -> KI-Disclosure-Pflicht (SKILL-028).",
    ),
    "listicle": ContentType(
        key="listicle",
        name="Listicle (Static/Carousel)",
        medium="multi_image",
        funnel=("awareness", "consideration"),
        formats=("square_1x1", "feed_4x5"),
        min_slides=3,
        max_slides=10,
        recommended_framework="fab",
        note="1 Punkt/Slide; Nummerierung als visueller Anker. Hohe Save-Rate.",
    ),
    # --- SKILL-042 Erweiterung (beweis-/personenbezogen) -------------------
    "voiceover_broll": ContentType(
        key="voiceover_broll",
        name="Voiceover / B-Roll-Video",
        medium="video",
        funnel=("awareness", "consideration"),
        formats=("story_9x16",),
        min_seconds=15,
        max_seconds=30,
        hook_window_seconds=3.0,
        onscreen_word_limit=ONSCREEN_WORD_LIMIT_DEFAULT,
        recommended_framework="bab",
        note="Demo-Format (VO + B-Roll/Screen-Recording). KI-Voice -> KI-Disclosure-"
             "Pflicht (SKILL-028).",
    ),
    "ugc_style": ContentType(
        key="ugc_style",
        name="UGC-Style Video",
        medium="video",
        funnel=("consideration",),
        formats=("story_9x16",),
        min_seconds=15,
        max_seconds=30,
        hook_window_seconds=3.0,
        onscreen_word_limit=ONSCREEN_WORD_LIMIT_DEFAULT,
        recommended_framework="hso",
        note="B2B-Premium-Caveat: nur DOSIERT (echtes Kunden-Statement), nie Marken-"
             "Default — fuer Premium/Trust-Produkte schlaegt professionelles Material UGC.",
    ),
    "story_ad": ContentType(
        key="story_ad",
        name="Story-Ad / organische Story",
        medium="video",
        funnel=("awareness",),
        formats=("story_9x16",),
        min_seconds=5,
        max_seconds=15,
        hook_window_seconds=2.0,
        onscreen_word_limit=ONSCREEN_WORD_LIMIT_DEFAULT,
        recommended_framework="hso",
        note="Retargeting-Slot; untere 35 % UI-frei. Ephemer, kein Save/Long-tail.",
    ),
    "testimonial": ContentType(
        key="testimonial",
        name="Testimonial / Case-Study (Static)",
        medium="image",
        funnel=("consideration", "conversion"),
        formats=("feed_4x5", "square_1x1"),
        recommended_framework="4p",
        requires_compliance_check=True,
        requires_proof=True,
        note="Staerkster Beweis (+bis 34 % CVR). Braucht ECHTE Referenz (kein Fake). "
             "Ergebnis-Zahlen/Claims -> DACH-Compliance-Check (Beleg!).",
    ),
    "testimonial_video": ContentType(
        key="testimonial_video",
        name="Testimonial / Case-Study (Video)",
        medium="video",
        funnel=("consideration", "conversion"),
        formats=("story_9x16",),
        min_seconds=15,
        max_seconds=45,
        hook_window_seconds=3.0,
        onscreen_word_limit=ONSCREEN_WORD_LIMIT_DEFAULT,
        recommended_framework="4p",
        requires_compliance_check=True,
        requires_proof=True,
        note="Echtes O-Ton-Statement, Caption Pflicht. Braucht echte Referenz "
             "(kein Fake). KI-Voice -> KI-Disclosure-Pflicht (SKILL-028).",
    ),
    "before_after": ContentType(
        key="before_after",
        name="Before/After (Static)",
        medium="image",
        funnel=("consideration", "conversion"),
        formats=("feed_4x5", "square_1x1"),
        recommended_framework="bab",
        requires_compliance_check=True,
        note="'Zahl jetzt -> Zahl Ziel'. DACH-Falle: uebertriebene Vorher-Nachher-"
             "Transformations-Claims sind abmahngefaehrdet (UWG §5, BEFORE_AFTER_TRIGGERS). "
             "Nur prozess-/produktbezogen, nie Personen-Transformation.",
    ),
}


def get_content_type(key: str) -> ContentType:
    """Liefert einen ContentType per Key oder wirft KeyError (analog get_format)."""
    if key not in CONTENT_TYPES:
        raise KeyError(
            f"Unbekannter Content-Typ '{key}'. Bekannt: {', '.join(CONTENT_TYPES)}"
        )
    return CONTENT_TYPES[key]


# === SKILL-040: content_type_warnings()-Validator =============================
# Warn-Validator (analog AdContent.warnings()/compliance_warnings()): prueft eine
# geplante Content-Instanz gegen ihren ContentType (Slide-Anzahl, Video-Laenge,
# On-Screen-Wortzahl). Liefert WARNUNGEN, KEINE harte Sperre (Mensch-im-Loop).
# Die On-Screen-Pruefung delegiert an frameworks.hook_fits_onscreen() — kein
# Doppel; der Import erfolgt lokal in der Funktion (Zyklus-Vermeidung).
# Wissensgrundlage: 2026-06-24_social-content-types.md (§3.2 Validatoren-Block).


def content_type_warnings(
    ct: ContentType,
    *,
    slides: int | None = None,
    seconds: float | None = None,
    onscreen_texts: list[str] | None = None,
) -> list[str]:
    """SKILL-040: prueft eine Content-Instanz gegen ihre ContentType-Constraints.

    Pro Constraint-Verstoss genau EINE sachliche Warnung:
      - Slide-Anzahl ausserhalb min_slides..max_slides (EARS-1).
      - Video-Laenge `seconds` ausserhalb min_seconds..max_seconds (EARS-2).
      - On-Screen-Text ueber dem Wortlimit, geprueft via
        frameworks.hook_fits_onscreen() — kein Doppel (EARS-3).
    Felder, die fuer den jeweiligen `medium` `None` sind, werden uebersprungen
    statt zu crashen (EARS-5). Haelt die Instanz alle Constraints ein, ist die
    Liste leer (EARS-4). Reine Warnungen, keine Exceptions bei Constraint-Verstoss.
    """
    # Lokaler Import: haelt specs.py frei von einem Modul-Level-Import auf
    # frameworks (frameworks importiert specs nicht -> kein echter Zyklus, aber
    # der lokale Import dokumentiert die lose Kopplung).
    from .frameworks import hook_fits_onscreen

    out: list[str] = []

    # --- Slide-Anzahl (nur wenn der Typ Slide-Grenzen kennt) ---------------
    if slides is not None and (ct.min_slides is not None or ct.max_slides is not None):
        lo = ct.min_slides
        hi = ct.max_slides
        if (lo is not None and slides < lo) or (hi is not None and slides > hi):
            out.append(
                f"Slide-Anzahl-Warnung ({ct.key}): {slides} Slides ausserhalb der "
                f"Soll-Range {lo}-{hi}. Karte 1 = Hook, letzte Karte = CTA."
            )

    # --- Video-Laenge (nur wenn der Typ Laengen-Grenzen kennt) -------------
    if seconds is not None and (ct.min_seconds is not None or ct.max_seconds is not None):
        lo_s = ct.min_seconds
        hi_s = ct.max_seconds
        if (lo_s is not None and seconds < lo_s) or (hi_s is not None and seconds > hi_s):
            out.append(
                f"Video-Laengen-Warnung ({ct.key}): {seconds}s ausserhalb des "
                f"Sweetspots {lo_s}-{hi_s}s. Hook-Promise bis "
                f"{ct.hook_window_seconds}s setzen."
            )

    # --- On-Screen-Wortlimit (Delegation an frameworks.hook_fits_onscreen) -
    if onscreen_texts:
        limit = ct.onscreen_word_limit or ONSCREEN_WORD_LIMIT_DEFAULT
        for text in onscreen_texts:
            if not hook_fits_onscreen(text, limit):
                out.append(
                    f"On-Screen-Wortlimit-Warnung ({ct.key}): '{text}' hat "
                    f"{len(text.split())} Woerter (max. {limit}). Overlay kuerzen "
                    "(sound-off-Lesbarkeit)."
                )

    return out


# === SKILL-042: Compliance-/Beleg-Kopplung der beweisbezogenen Typen ==========
# Verdrahtet die in CONTENT_TYPES deklarierten Flags (requires_compliance_check,
# requires_proof) mit den BESTEHENDEN Guards — KEINE neue Compliance-Logik:
#   - requires_compliance_check -> compliance_warnings() (SKILL-026, inkl.
#     BEFORE_AFTER_TRIGGERS) auf den Content-Text.
#   - requires_proof -> Beleg-Pflicht-Hinweis (echte Referenz, kein Fake).
#   - ai_voice bei einem Video-Typ -> KI-Disclosure-Pflicht (SKILL-028)
#     weiterreichen (requires_ai_disclosure-Logik gespiegelt ohne AdContent).
# Wissensgrundlage: 2026-06-24_social-content-types.md (§2.10/§2.11, §3.2 Kopplung).


def content_type_compliance_warnings(
    ct: ContentType,
    text: str = "",
    *,
    ai_voice: bool = False,
) -> list[str]:
    """SKILL-042: loest fuer beweis-/personenbezogene Typen die passenden Guards aus.

    - `before_after`/`testimonial`/`testimonial_video` (requires_compliance_check):
      ruft compliance_warnings() auf `text` (UWG/HWG, inkl. BEFORE_AFTER_TRIGGERS)
      und liefert pro Treffer eine Warnung mit Rechtsgrundlage (EARS-2).
    - `testimonial`/`testimonial_video` (requires_proof): ein Beleg-Pflicht-Hinweis
      (echte Referenz noetig, kein Fake) als Warnung (EARS-3).
    - Video-Typ mit `ai_voice=True`: KI-Disclosure-Pflicht (SKILL-028) als Warnung
      weiterreichen (EARS-4).
    Reine Warnungen, keine Sperre. Verdrahtet nur vorhandene Guards (kein Doppel).
    """
    out: list[str] = []

    # EARS-2: Compliance-Heuristik (SKILL-026) fuer die gekoppelten Typen.
    if ct.requires_compliance_check:
        out.extend(compliance_warnings(text))

    # EARS-3: Beleg-Pflicht-Hinweis (echte Referenz, kein Fake).
    if ct.requires_proof:
        out.append(
            f"Beleg-Pflicht ({ct.key}): Testimonial/Case-Study braucht eine ECHTE, "
            "nachweisbare Referenz (echter Kunde/O-Ton, keine erfundene/gefakte "
            "Aussage). Beleg sichern, bevor das Creative live geht."
        )

    # EARS-4: KI-Disclosure-Pflicht (SKILL-028) bei synthetischer Stimme im Video.
    if ai_voice and ct.medium == "video":
        out.append(
            f"KI-Disclosure-Pflicht ({ct.key}): synthetische Stimme (ai_voice) "
            f"erkannt. Meta-Policy + EU-AI-Act (ab {AI_ACT_ENFORCEMENT_DATE}) "
            f"verlangen sichtbares '{AI_LABEL_TEXT}'-Label + maschinenlesbare "
            "Metadaten. Disclosure aktivieren."
        )

    return out


# === SKILL-072: Layout-Archetypen + Themes + Stil-Parameter ===================
# Projektneutraler Katalog (analog FORMATS/CONTENT_TYPES) fuer Scroll-Stop-Layouts
# oberhalb des Bestands-Skeletts. Der Default-Archetyp "template" ist das bisherige
# Layout — Bestandsrenders bleiben damit unveraendert (nicht-brechend). Die uebrigen
# Archetypen kommen OBENDRAUF und laufen durch dieselben FORMATS-Safe-Zones +
# Brand-Tokens. Themes ueberschreiben nur die Flaechen-/Ink-Tokens (Akzent bleibt
# markeneigen). Alle Werte projektneutral (Prinzip skill-muss-multi-projekt-tauglich).
# Wissensgrundlage: AgentischesArbeiten/marketing/2026-07-08_creative-studio_stil-gap-analyse.md
#   (7 Stil-Hebel: Scale-Kontrast, Font-Schnitt, Layout-Varietaet, Farbe als Flaeche,
#    Motiv=Konzept, Editorial-Negativraum, weniger Ad-Chrome).


@dataclass(frozen=True)
class Layout:
    """Ein Layout-Archetyp (Komposition ueber dem technischen AdFormat).

    AdFormat = Ausgabemass/Ratio/Safe-Zone; Layout = wie der Inhalt darin
    komponiert wird. Alle Layouts respektieren die Safe-Zonen des jeweiligen
    AdFormat. Projektneutral — kein Brand-/Projektwert.

    Attributes:
        key: stabiler Bezeichner ("template", "stat-hero", ...).
        name: ausgeschriebener Name fuer UI/Doku.
        description: was der Archetyp macht / wann er passt.
        hero_driven: nutzt `hero_token` als Riesen-Element (Scale-Kontrast-Hebel).
        needs_bg_image: Foto-/Objekt-getrieben — braucht ein Hintergrund-/Motiv-Bild
            (wird von SKILL-073 aus der Bildquelle gefuellt; ohne Bild Warnung + Gradient-Fallback).
        note: optionaler Hinweis.
    """
    key: str
    name: str
    description: str
    hero_driven: bool = False
    needs_bg_image: bool = False
    note: str = ""


# SKILL-072: Layout-Katalog. "template" = Bestands-Skelett (Default, nicht-brechend).
LAYOUTS: dict[str, Layout] = {
    "template": Layout(
        key="template", name="Template-Skelett (Default)",
        description="Bestands-Layout: eyebrow -> headline -> subline -> CTA-Pill, "
                    "unten ausgerichtet. Sicher, markenkonform, multi-format. Default.",
        note="Default-Archetyp — Verhalten exakt wie vor SKILL-072.",
    ),
    "stat-hero": Layout(
        key="stat-hero", name="Stat-Hero (Riesenzahl/-wort als Held)",
        description="EIN Hero-Token (Zahl/Kurzwort) riesig als Blickfang (Scale-Kontrast "
                    "5-8:1), Eyebrow oben, Subline + CTA klein darunter, viel Negativraum. "
                    "Groesster Scroll-Stop-Hebel, keine externe Bildquelle noetig.",
        hero_driven=True,
        note="Ohne --hero-token wird die Headline als Hero genutzt.",
    ),
    "photo-poster": Layout(
        key="photo-poster", name="Photo-Poster (fullbleed Foto + fette Typo)",
        description="Fullbleed-Foto, fette Headline direkt darueber; gerichteter Scrim "
                    "nur hinter dem Text statt Vollflaechen-Dimmen. Motiv traegt die Stimmung.",
        needs_bg_image=True,
        note="Bild via --bg-source/--bg-image (SKILL-073). Ohne Bild: Gradient-Fallback + Warnung.",
    ),
    "object-hero": Layout(
        key="object-hero", name="Object-Hero (freigestelltes Motiv als Held)",
        description="Freigestelltes Motiv/Objekt als Held (Motiv=Konzept), Typo daneben/darunter. "
                    "Editorial-Komposition mit bewusstem Negativraum.",
        needs_bg_image=True,
        note="Objekt-/Motiv-Bild via SKILL-073. Ohne Bild: Gradient-Fallback + Warnung.",
    ),
    "split-compare": Layout(
        key="split-compare", name="Split-Compare (Vorher/Nachher, hell/dunkel)",
        description="Zwei Haelften (z.B. 1995 vs 2026 / alt vs neu), Kontrast hell/dunkel. "
                    "Traegt Vergleichs-Botschaften.",
        note="DACH-Vorsicht bei Personen-Transformation (BEFORE_AFTER_TRIGGERS, compliance_warnings).",
    ),
}


@dataclass(frozen=True)
class Theme:
    """Ein Farb-Theme, das nur die Flaechen-/Ink-Tokens ueberschreibt.

    `overrides` mappt interne BRAND_*-Keys auf Theme-Werte; ein leeres dict laesst
    die Marke unveraendert (Theme "dark" = Brand-Default). Der Akzent (BRAND_ACCENT)
    bleibt IMMER markeneigen — ein Theme faerbt nie die Marke um, es tauscht nur
    Hintergrund/Text-Kontrast (Hebel "Farbe als Flaeche": helle Cream-Variante als
    Kontrast zur Navy-Default). Projektneutral.
    """
    key: str
    name: str
    overrides: dict
    note: str = ""


# SKILL-072: Theme-Katalog. "dark" = Brand-Default (kein Override). "light-cream" =
# helle Cream-Flaeche mit dunklem Ink — Akzent bleibt markeneigen.
THEMES: dict[str, Theme] = {
    "dark": Theme(
        key="dark", name="Dark (Brand-Default)", overrides={},
        note="Default — nutzt die Brand-Tokens unveraendert.",
    ),
    "light-cream": Theme(
        key="light-cream", name="Light Cream",
        overrides={
            "BRAND_BG": "#efe7d6",       # warme Cream-Flaeche
            "BRAND_BG_SOFT": "#faf5ec",  # heller Verlauf oben
            "BRAND_INK": "#1a1d2e",      # dunkler Ink fuer Kontrast
            "BRAND_INK_MUTED": "#6c6f80",
        },
        note="Akzent bleibt markeneigen (BRAND_ACCENT wird NICHT ueberschrieben).",
    ),
}

# SKILL-072: Hero-Scale-Sweetspot (Anteil der Canvas-Hoehe). Ausserhalb -> Warnung,
# KEINE Sperre (konsistent mit dem Warn-statt-Block-Muster von compliance_warnings()).
HERO_SCALE_SWEETSPOT: tuple[float, float] = (0.25, 0.40)
HERO_SCALE_DEFAULT: float = 0.32


def get_layout(key: str) -> Layout:
    """Liefert einen Layout-Archetyp per Key oder wirft KeyError (analog get_format)."""
    if key not in LAYOUTS:
        raise KeyError(f"Unbekanntes Layout '{key}'. Bekannt: {', '.join(LAYOUTS)}")
    return LAYOUTS[key]


def get_theme(key: str) -> Theme:
    """Liefert ein Theme per Key oder wirft KeyError (analog get_format)."""
    if key not in THEMES:
        raise KeyError(f"Unbekanntes Theme '{key}'. Bekannt: {', '.join(THEMES)}")
    return THEMES[key]


def apply_theme(brand: dict, theme_key: str) -> dict:
    """SKILL-072: Legt ein Theme ueber ein Brand-dict und gibt ein NEUES dict zurueck.

    Nur die im Theme deklarierten BRAND_*-Keys werden ueberschrieben (Flaeche/Ink);
    der Akzent + alle uebrigen Keys bleiben. Theme "dark" (leere overrides) gibt das
    Brand-dict inhaltlich unveraendert zurueck -> nicht-brechend. Unbekanntes Theme
    -> unveraendertes Brand-dict (kein Crash; der Renderer warnt separat).
    """
    out = dict(brand)
    theme = THEMES.get(theme_key)
    if theme:
        for k, v in theme.overrides.items():
            out[k] = v
    return out


def layout_warnings(
    layout_key: str,
    *,
    hero_scale: float | None = None,
    has_bg_image: bool = False,
) -> list[str]:
    """SKILL-072: Warn-Validator fuer Layout-Wahl + Stil-Parameter (keine Sperre).

    - Unbekanntes Layout -> Hinweis + Fallback-Empfehlung "template" (EARS-nah,
      konsistent mit dem Warn-statt-Block-Muster).
    - Hero-Scale ausserhalb HERO_SCALE_SWEETSPOT bei einem hero-getriebenen Layout
      -> Warnung (zu klein = kein Scale-Kontrast, zu gross = sprengt Safe-Zone).
    - Foto-/Objekt-getriebenes Layout OHNE Bild -> Warnung (Gradient-Fallback greift,
      Motiv=Konzept-Hebel fehlt). Wird mit SKILL-073 (--bg-source) aufloesbar.
    Reine Warnungen, Mensch-im-Loop. Projektneutral.
    """
    out: list[str] = []
    layout = LAYOUTS.get(layout_key)
    if layout is None:
        out.append(
            f"Layout-Warnung: unbekanntes Layout '{layout_key}'. Bekannt: "
            f"{', '.join(LAYOUTS)}. Fallback-Empfehlung: 'template'."
        )
        return out

    if layout.hero_driven and hero_scale is not None:
        lo, hi = HERO_SCALE_SWEETSPOT
        if hero_scale < lo or hero_scale > hi:
            out.append(
                f"Hero-Scale-Warnung ({layout.key}): hero_scale={hero_scale:.2f} "
                f"ausserhalb des Sweetspots {lo:.2f}-{hi:.2f} der Canvas-Hoehe. "
                "Zu klein = kein Scale-Kontrast (Blickfang schwach), zu gross = "
                "Hero sprengt die Safe-Zone/den Textblock."
            )

    if layout.needs_bg_image and not has_bg_image:
        out.append(
            f"Bild-Warnung ({layout.key}): dieses Layout ist foto-/motiv-getrieben, "
            "aber es liegt kein Hintergrund-/Motiv-Bild vor. Es greift der "
            "Gradient-Fallback (der Motiv=Konzept-Hebel fehlt). Bild via "
            "--bg-source/--bg-image liefern (SKILL-073)."
        )

    return out
