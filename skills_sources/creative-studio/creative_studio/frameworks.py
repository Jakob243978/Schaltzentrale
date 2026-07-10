"""creative-studio — Copy-Framework-Katalog + Hook-Bibliothek + Validatoren (SKILL-025).

Kodiert die Recherche-Ergebnisse vom 2026-06-23 als verwendbaren Code (statt nur Doku):
  - AgentischesArbeiten/docs/marketing/research/2026-06-23_ad-copywriting-frameworks.md
    -> §1 Frameworks (AIDA/PAS/BAB/FAB/PASTOR/4P/HSO), §3 Conversion-Best-Practices,
       §4 Umsetzung als frameworks.py

Dies ist das **Copy-Pendant zu specs.py**: specs.py haelt die Format-/Safe-Zone-Standards
von Meta, frameworks.py haelt die Copy-Standards (Strukturen + Platzhalter + Validatoren).
Single Source of Truth fuer Copy-Geruest — genutzt vom Generator (oder einem vorgelagerten
Agent), damit Bild + Video dieselben Copy-Frameworks teilen.

Abgrenzung: Diese Datei liefert **Struktur + Validierung**, NICHT den finalen kreativen
Text — der bleibt LLM-/Mensch-Aufgabe. Sie erzeugt das Geruest, in das Brand + Inhalt zur
Laufzeit eingesetzt werden.

Multi-Projekt: enthaelt KEINE projekt-spezifischen Werte (kein Brand-Claim, keine Tonalitaet,
keine Jakob-Texte) — nur die generischen Frameworks/Hooks. Projektspezifisches bleibt Overlay/
Parameter.

Hinweis: Der DACH-Compliance-Guard (UWG/HWG-Trigger, `compliance_warnings`, `landing_promise`)
ist als SKILL-026 separat spezifiziert — hier nur Referenz, KEINE Doppel-Implementierung.
"""
from __future__ import annotations
from dataclasses import dataclass


# --- Copy-Framework-Katalog -------------------------------------------------
# SKILL-025: CopyFramework ist das Copy-Pendant zu AdFormat (specs.py): ein
# medien-unabhaengiges, projektneutrales Argumentations-Geruest mit Slots +
# Platzhalter-Template, aus dem der Generator Copy baut (statt Freitext).
@dataclass(frozen=True)
class CopyFramework:
    """Ein bewaehrtes Copy-Framework als Argumentations-Geruest.

    Frameworks sind keine Magie, sondern erzwingen, dass eine Anzeige Aufmerksamkeit,
    Relevanz, Beweis und Handlungsaufforderung in sinnvoller Reihenfolge enthaelt.
    Welches Framework passt, haengt vom Awareness-Level der Zielgruppe ab (Eugene Schwartz).

    Attributes:
        key: stabiler Bezeichner ("pas", "aida", ...).
        name: ausgeschriebener Name fuer UI/Doku.
        slots: die Struktur-Bausteine in Reihenfolge, z.B. PAS = (problem, agitate, solution).
        awareness: Awareness-Tags fuer die Auto-Auswahl (unaware/problem/solution/product/most_aware).
        best_for: Kurzbeschreibung + Placement-Eignung (projektneutral).
        template: Platzhalter-String mit genau den `slots` als {slot}-Marker.
        note: optionaler Hinweis (DACH-Vorsicht etc.).
    """
    key: str
    name: str
    slots: tuple[str, ...]
    awareness: tuple[str, ...]
    best_for: str
    template: str
    note: str = ""


# Awareness-Tags (Eugene Schwartz, vereinheitlicht) — als Konstanten dokumentiert,
# damit Katalog + recommend_framework dieselbe Sprache sprechen.
AWARENESS_LEVELS: tuple[str, ...] = (
    "unaware",        # kennt das Problem noch nicht
    "problem_aware",  # kennt das Problem, sieht keinen Weg
    "solution_aware", # kennt Loesungswege, vergleicht
    "product_aware",  # kennt den Anbieter, waegt ab
    "most_aware",     # warm, braucht nur noch die Einladung
)

# SKILL-025: Katalog der Frameworks. Templates nutzen NUR die jeweiligen Slots als
# {slot}-Platzhalter — projektneutral, kein Brand-/Claim-Text hartkodiert.
FRAMEWORKS: dict[str, CopyFramework] = {
    "aida": CopyFramework(
        key="aida",
        name="AIDA — Attention · Interest · Desire · Action",
        slots=("attention", "interest", "desire", "action"),
        awareness=("unaware",),
        best_for="Cold / problem-unaware: Zielgruppe muss erst edukiert werden. "
                 "Mittellange Landingpages, Cold-Audiences.",
        template="{attention}\n{interest}\n{desire}\n{action}",
        note="Aeltestes Modell (E. St. Elmo Lewis, 1898).",
    ),
    "pas": CopyFramework(
        key="pas",
        name="PAS — Problem · Agitate · Solution",
        slots=("problem", "agitate", "solution"),
        awareness=("problem_aware",),
        best_for="Problem-aware: Zielgruppe kennt das Problem, sieht aber keinen Weg. "
                 "Staerkstes Kurzformat fuer Ads/E-Mail — Default fuer Cold-Meta-Ads.",
        template="{problem}\n{agitate}\n{solution}",
        note="'Agitate' im DACH-B2B massvoll dosieren — kein Drama-/Angst-Marketing.",
    ),
    "bab": CopyFramework(
        key="bab",
        name="BAB — Before · After · Bridge",
        slots=("before", "after", "bridge"),
        awareness=("solution_aware", "product_aware"),
        best_for="Vergleichend / verbesserungsmotiviert (nicht akuter Schmerz). "
                 "Sehr bildstark — gut fuer Video.",
        template="{before}\n{after}\n{bridge}",
        note="Vorsicht: uebertriebene Vorher-Nachher-Transformations-Claims sind ein "
             "bekannter Coaching-Fallstrick (siehe specs.COACHING_CLAIM_TRIGGERS / SKILL-026).",
    ),
    "fab": CopyFramework(
        key="fab",
        name="FAB — Features · Advantages · Benefits",
        slots=("feature", "advantage", "benefit"),
        awareness=("solution_aware", "product_aware"),
        best_for="Vergleichende/abwaegende Zielgruppe; Detail-/Mid-Funnel-Copy, "
                 "FAQ, Karussell-Karten.",
        template="{feature}\n{advantage}\n{benefit}",
        note="Zwingt, von Feature zu Nutzen zu uebersetzen.",
    ),
    "pastor": CopyFramework(
        key="pastor",
        name="PASTOR — Problem · Amplify · Story/Solution · Transformation · Offer · Response",
        slots=("problem", "amplify", "story", "transformation", "offer", "response"),
        awareness=("problem_aware", "solution_aware", "product_aware"),
        best_for="Langform: VSL, lange Sales-Page, E-Mail-Sequenz. Fuer eine einzelne Ad "
                 "zu lang — ideal als Quelle fuer Hooks/PAS-Snippets.",
        template="{problem}\n{amplify}\n{story}\n{transformation}\n{offer}\n{response}",
        note="Erweitertes PAS mit Story-Beleg + expliziter Transformation.",
    ),
    "4p": CopyFramework(
        key="4p",
        name="4P — Picture · Promise · Proof · Push",
        slots=("picture", "promise", "proof", "push"),
        awareness=("solution_aware", "product_aware"),
        best_for="Mid-Funnel/Landingpage, wenn Social Proof verfuegbar ist. "
                 "Beweis-lastiger Verwandter von AIDA.",
        template="{picture}\n{promise}\n{proof}\n{push}",
    ),
    "hso": CopyFramework(
        key="hso",
        name="Hook · Story · Offer (Russell Brunson)",
        slots=("hook", "story", "offer"),
        awareness=("product_aware", "most_aware"),
        best_for="Warmes Publikum, Reels/Video, Funnel-Copy. Bewusst lockerer, "
                 "story-getrieben. Der Hook ist der wichtigste, eigenstaendig "
                 "wiederverwendbare Baustein (siehe HOOKS).",
        template="{hook}\n{story}\n{offer}",
    ),
}


def get_framework(key: str) -> CopyFramework:
    """Liefert ein Framework per Key oder wirft KeyError (analog specs.get_format)."""
    if key not in FRAMEWORKS:
        raise KeyError(f"Unbekanntes Framework '{key}'. Bekannt: {', '.join(FRAMEWORKS)}")
    return FRAMEWORKS[key]


# --- Hook-Bibliothek --------------------------------------------------------
# SKILL-025: Overlay-Lesbarkeit. 85 % der Feed-Videos laufen ohne Ton -> Text-Overlay
# noetig, max. ~7 Woerter on-screen (Recherche §3.2). MAX_WORDS_ONSCREEN ist die Regel,
# die jeder Hook beim Rendern als On-Screen-Text einhalten soll.
MAX_WORDS_ONSCREEN = 7


@dataclass(frozen=True)
class HookPattern:
    """Ein wiederverwendbares Scroll-Stopper-Muster mit Platzhaltern.

    Der Hook muss in 1,5-3 Sek. landen (Recherche §3.1). Templates sind projektneutral —
    Platzhalter ({zielgruppe}, {ergebnis}, {schmerz}, ...) kommen zur Laufzeit rein.
    `max_words_onscreen` ist die On-Screen-Wortgrenze fuer den gerenderten Text.

    Attributes:
        key: stabiler Bezeichner.
        name: Kurzname des Musters.
        template: Platzhalter-String (KEIN fertiger Text).
        max_words_onscreen: Wortgrenze fuer das On-Screen-Overlay (Default MAX_WORDS_ONSCREEN).
        note: optionaler Hinweis zur seriosen Anwendung.
    """
    key: str
    name: str
    template: str
    max_words_onscreen: int = MAX_WORDS_ONSCREEN
    note: str = ""


# SKILL-025: >= 6 seriose, projektneutrale Hook-Muster (Recherche §3.1/§3.2).
# Bewusst KEINE reisserischen "SCAM"-/Druck-Hooks — markenschaedlich fuer B2B-Premium
# und in DACH abmahngefaehrdet.
HOOKS: dict[str, HookPattern] = {
    "give_me_x": HookPattern(
        key="give_me_x",
        name="Gib mir X (kleine Selbstverpflichtung)",
        template="Gib mir {seconds} Sekunden — dann {payoff}.",
        note="Niedrigschwellige Mikro-Zusage. Payoff konkret + ehrlich halten.",
    ),
    "specific_number": HookPattern(
        key="specific_number",
        name="Konkrete Zahl / Reibung",
        template="{anteil} Prozent {zielgruppe} {schmerz} — jede Woche.",
        note="Spezifische Zahlen schlagen runde (Recherche §3.3). Nur belegbare Zahlen.",
    ),
    "niche_question": HookPattern(
        key="niche_question",
        name="Spezifische Frage an die Nische",
        template="{zielgruppe} mit {merkmal}?",
        note="Selbst-Selektion der relevanten Zielgruppe in Zeile 1.",
    ),
    "pattern_interrupt": HookPattern(
        key="pattern_interrupt",
        name="Pattern Interrupt (unerwartetes Bild/Statement)",
        template="{unerwartete_aussage}",
        note="Visueller/sprachlicher Bruch der Erwartung. Bild-Cue, kein Clickbait.",
    ),
    "before_after": HookPattern(
        key="before_after",
        name="Before/After-Bild",
        template="Heute {ist_zustand}. Bald {wunsch_zustand}.",
        note="Bildstark fuer Video. Transformations-Claims belegbar + produktbezogen halten "
             "(DACH-Vorsicht, siehe SKILL-026).",
    ),
    "friction_statement": HookPattern(
        key="friction_statement",
        name="Reibungs-Statement",
        template="{reibung} — und es liegt nicht an {falsche_ursache}.",
        note="Benennt den wunden Punkt sachlich, ohne Druck/Drama.",
    ),
    "outcome_without_pain": HookPattern(
        key="outcome_without_pain",
        name="Ergebnis ohne Schmerz",
        template="Wie {zielgruppe} {ergebnis} erreicht, ohne {schmerz}.",
        note="Klassisches How-to-Versprechen. Ergebnis konkret + belegbar.",
    ),
}


def get_hook(key: str) -> HookPattern:
    """Liefert ein Hook-Muster per Key oder wirft KeyError."""
    if key not in HOOKS:
        raise KeyError(f"Unbekanntes Hook-Muster '{key}'. Bekannt: {', '.join(HOOKS)}")
    return HOOKS[key]


def count_onscreen_words(text: str) -> int:
    """Zaehlt die Woerter eines On-Screen-Textes (whitespace-getrennt)."""
    return len(text.split())


def hook_fits_onscreen(text: str, max_words: int = MAX_WORDS_ONSCREEN) -> bool:
    """True, wenn der On-Screen-Text die Wortgrenze (Default 7) einhaelt.

    SKILL-025: prueft EARS-2 — jeder gerenderte Hook-Text muss <= MAX_WORDS_ONSCREEN
    Woerter haben (Overlay-Lesbarkeit, Recherche §3.2).
    """
    return count_onscreen_words(text) <= max_words


# --- Awareness-gesteuerte Framework-Auswahl ---------------------------------
# SKILL-025: Kurzregel aus Recherche §1 (cold->AIDA, problem_aware->PAS,
# vergleichend->FAB/BAB, warm/video->HSO, Langform->PASTOR).
def recommend_framework(awareness: str, placement: str = "") -> CopyFramework:
    """Empfiehlt das passende Framework nach Awareness-Level (+ Placement-Hint).

    Kurzregel (Recherche §1, "Framework-Wahl nach Awareness"):
      - unaware / cold                -> AIDA (edukieren)
      - problem_aware                 -> PAS (Default fuer Cold-Meta-Ads)
      - solution_aware (vergleichend) -> FAB; bei Video/bildstark -> BAB
      - product_aware                 -> BAB (Anbieter-/Kategorievergleich)
      - most_aware / warm / Video      -> Hook-Story-Offer
    Langform-Placements (vsl, sales_page, email) -> PASTOR (ueberschreibt die Awareness-Regel).

    Args:
        awareness: ein Wert aus AWARENESS_LEVELS. Synonyme: "cold"->unaware, "warm"->most_aware.
        placement: optionaler Hinweis (z.B. "reel", "video", "story", "vsl", "sales_page",
                   "email") — verfeinert die Auswahl.

    Returns:
        Das empfohlene CopyFramework.

    Raises:
        ValueError: bei unbekanntem Awareness-Wert.
    """
    aw = awareness.strip().lower()
    place = placement.strip().lower()

    # Synonyme auf die kanonischen Tags mappen.
    synonyms = {
        "cold": "unaware",
        "warm": "most_aware",
        "retargeting": "most_aware",
        "comparing": "solution_aware",
        "vergleichend": "solution_aware",
    }
    aw = synonyms.get(aw, aw)

    if aw not in AWARENESS_LEVELS:
        raise ValueError(
            f"Unbekanntes Awareness-Level '{awareness}'. "
            f"Bekannt: {', '.join(AWARENESS_LEVELS)} (oder Synonyme cold/warm/vergleichend)."
        )

    # Langform-Placements ueberschreiben die Awareness-Regel -> PASTOR.
    longform_placements = {"vsl", "sales_page", "salespage", "email", "sequence", "langform"}
    if place in longform_placements:
        return FRAMEWORKS["pastor"]

    video_placements = {"reel", "reels", "video", "story", "stories"}
    is_video = place in video_placements

    if aw == "unaware":
        return FRAMEWORKS["aida"]
    if aw == "problem_aware":
        return FRAMEWORKS["pas"]
    if aw == "solution_aware":
        # Vergleichend: bildstark/Video -> BAB, sonst FAB.
        return FRAMEWORKS["bab"] if is_video else FRAMEWORKS["fab"]
    if aw == "product_aware":
        # Warm + Video -> HSO, sonst Before/After-Vergleich.
        return FRAMEWORKS["hso"] if is_video else FRAMEWORKS["bab"]
    # most_aware
    return FRAMEWORKS["hso"]


# --- 4U-Headline-Validator (Warn-Funktion, keine harte Sperre) --------------
# SKILL-025: 4U-Checkliste (useful/urgent/unique/ultra_specific) aus Recherche §1.6.
# Liefert HINWEISE analog AdContent.warnings() — kein hartes Pass/Fail.

# Heuristik-Vokabular (projektneutral, bewusst klein gehalten — keine echte NLP).
_USEFUL_HINTS = (
    "ohne", "spar", "gewinn", "mehr", "weniger", "schneller", "einfacher",
    "abgeben", "automatis", "loesung", "lösung",
)
_URGENT_HINTS = (
    "jetzt", "heute", "noch", "letzte", "begrenzt", "limitiert", "warteliste",
    "start", "frist", "nur", "diese woche",
)
_UNIQUE_HINTS = (
    "einzig", "exklusiv", "nur wir", "als einzige", "patent", "methode", "system",
    "anders als", "ohne ", "neu",
)


def _has_number(text: str) -> bool:
    return any(ch.isdigit() for ch in text)


def score_4u(headline: str) -> dict[str, bool]:
    """4U-Heuristik: prueft useful/urgent/unique/ultra_specific (grobe Wort-Heuristik).

    Bewusst simpel: erkennt Signal-Woerter/Zahlen, ersetzt keine menschliche Bewertung.
    Gibt pro U True/False zurueck. Genutzt von validate_4u() fuer die Warntexte.
    """
    h = headline.lower()
    return {
        "useful": any(w in h for w in _USEFUL_HINTS),
        "urgent": any(w in h for w in _URGENT_HINTS),
        # ultra_specific: Zahl ODER ein konkretes Spezifik-Signal (Prozent/Zeitraum).
        "ultra_specific": _has_number(headline) or "%" in headline,
        "unique": any(w in h for w in _UNIQUE_HINTS),
    }


def validate_4u(headline: str) -> list[str]:
    """4U-Warn-Validator fuer eine Headline (analog AdContent.warnings()).

    SKILL-025 (EARS-4): liefert HINWEISE, keine harte Sperre. Eine starke Headline
    sollte moeglichst mehrere der vier Qualitaeten haben (useful/urgent/unique/
    ultra_specific, Recherche §1.6). Bei schwacher Headline -> Hinweise, was fehlt.

    Returns:
        Liste von Hinweistexten (leer = alle 4U erfuellt). Reihenfolge: U-fehlt-Hinweise,
        dann ggf. ein Gesamt-Hinweis bei sehr schwacher Headline.
    """
    out: list[str] = []
    if not headline.strip():
        out.append("4U: leere Headline — keine Bewertung moeglich.")
        return out

    score = score_4u(headline)
    labels = {
        "useful": "useful (klarer Nutzen) — z.B. konkretes Ergebnis/Ersparnis benennen.",
        "urgent": "urgent (Dringlichkeit) — z.B. echte Verknappung (Warteliste, Kohorten-Start). "
                  "Keine Fake-Timer (UWG).",
        "unique": "unique (Alleinstellung) — was macht es anders/einzigartig?",
        "ultra_specific": "ultra_specific (Spezifik) — konkrete Zahl/Zeitraum statt Floskel.",
    }
    for key, ok in score.items():
        if not ok:
            out.append(f"4U-Hinweis: fehlt {labels[key]}")

    erfuellt = sum(1 for ok in score.values() if ok)
    if erfuellt <= 1:
        out.append(
            f"4U gesamt: Headline erfuellt nur {erfuellt}/4 U — schwacher Hook. "
            f"Mind. 2-3 U anstreben (nuetzlich/dringlich/einzigartig/ultra-spezifisch)."
        )
    return out
