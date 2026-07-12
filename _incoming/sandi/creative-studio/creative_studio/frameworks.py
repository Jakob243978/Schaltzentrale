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
import json
import re
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
        slots: die Struktur-Bausteine in Reihenfolge, z.B. PAS = (problem, agitate, solution, cta).
        awareness: Awareness-Tags fuer die Auto-Auswahl (unaware/problem/solution/product/most_aware).
        best_for: Kurzbeschreibung + Placement-Eignung (projektneutral).
        template: Platzhalter-String mit genau den `slots` als {slot}-Marker.
        note: optionaler Hinweis (DACH-Vorsicht etc.).
        funnel: Funnel-Stufen-Tags (tofu/mofu/bofu) — SKILL-085 Auslieferungs-Empfehlung.
        traffic: Traffic-Temperatur-Tags (cold/warm/retargeting) — SKILL-085.

    SKILL-085 (Auslieferungs-Empfehlung): `awareness` + `funnel` + `traffic` + `best_for`
    bilden zusammen die **Empfehlungs-Matrix** ("wann + fuer wen"). Alle vier Achsen sind
    generisch/projektneutral — KEIN hartkodierter Projektwert. Damit muss man Zielgruppe/
    Timing beim Erzeugen nicht mehr manuell mitgeben; `recommend_framework` /
    `match_frameworks` / `framework_matrix` lesen sie aus.
    """
    key: str
    name: str
    slots: tuple[str, ...]
    awareness: tuple[str, ...]
    best_for: str
    template: str
    note: str = ""
    funnel: tuple[str, ...] = ()
    traffic: tuple[str, ...] = ()


# Awareness-Tags (Eugene Schwartz, vereinheitlicht) — als Konstanten dokumentiert,
# damit Katalog + recommend_framework dieselbe Sprache sprechen.
AWARENESS_LEVELS: tuple[str, ...] = (
    "unaware",        # kennt das Problem noch nicht
    "problem_aware",  # kennt das Problem, sieht keinen Weg
    "solution_aware", # kennt Loesungswege, vergleicht
    "product_aware",  # kennt den Anbieter, waegt ab
    "most_aware",     # warm, braucht nur noch die Einladung
)

# SKILL-085: Funnel-Stufen + Traffic-Temperatur als generische Achsen der
# Auslieferungs-Empfehlung. Projektneutral — beschreiben nur, WANN/an WEN ein
# Framework typischerweise ausgespielt wird, nicht welches Projekt es nutzt.
FUNNEL_STAGES: tuple[str, ...] = (
    "tofu",  # Top of Funnel — Reichweite/Edukation, kalte Zielgruppe
    "mofu",  # Middle of Funnel — Erwaegung/Vergleich, angewaermt
    "bofu",  # Bottom of Funnel — Conversion/Einladung, warm/retargeting
)
TRAFFIC_TEMPERATURES: tuple[str, ...] = (
    "cold",         # Prospecting — kennt Absender noch nicht
    "warm",         # hatte schon Kontakt (Engager, Video-Viewer, Website)
    "retargeting",  # heisse Custom Audience — braucht nur noch die Einladung
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
        funnel=("tofu",),
        traffic=("cold",),
    ),
    "pas": CopyFramework(
        key="pas",
        name="PAS — Problem · Agitate · Solution · CTA",
        # SKILL-081-Delta / Baulig #1: expliziter CTA-Slot ergaenzt (war zuvor 3 Slots
        # ohne CTA). Additiv — der Argumentations-Arc endet jetzt mit klarer Handlung,
        # konsistent mit allen neuen Baulig-Frameworks (jedes hat einen cta-Slot).
        slots=("problem", "agitate", "solution", "cta"),
        awareness=("problem_aware",),
        best_for="Problem-aware: Zielgruppe kennt das Problem, sieht aber keinen Weg. "
                 "Staerkstes Kurzformat fuer Ads/E-Mail — Default fuer Cold-Meta-Ads.",
        template="{problem}\n{agitate}\n{solution}\n{cta}",
        note="'Agitate' im DACH-B2B massvoll dosieren — kein Drama-/Angst-Marketing. "
             "CTA = echte Verknappung/klarer Klick-Befehl, keine Fake-Timer (UWG).",
        funnel=("tofu", "mofu"),
        traffic=("cold",),
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
        funnel=("mofu",),
        traffic=("warm",),
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
        funnel=("mofu",),
        traffic=("warm",),
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
        funnel=("mofu", "bofu"),
        traffic=("warm",),
    ),
    "4p": CopyFramework(
        key="4p",
        name="4P — Picture · Promise · Proof · Push",
        slots=("picture", "promise", "proof", "push"),
        awareness=("solution_aware", "product_aware"),
        best_for="Mid-Funnel/Landingpage, wenn Social Proof verfuegbar ist. "
                 "Beweis-lastiger Verwandter von AIDA.",
        template="{picture}\n{promise}\n{proof}\n{push}",
        funnel=("mofu",),
        traffic=("warm",),
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
        funnel=("mofu", "bofu"),
        traffic=("warm", "retargeting"),
    ),
    # --- Baulig-Methoden (Founder Summit 2025) ------------------------------
    # docs/ad-frameworks/baulig-methoden.md — 4 zusaetzliche Copy-/Argumentations-
    # Gerueste. Jedes hat einen expliziten cta-Slot. Projektneutral (Slots + Template
    # generisch, kein Brand-/Claim-Text).
    "mindset_shift": CopyFramework(  # Baulig #2 — SKILL-081
        key="mindset_shift",
        name="Mindset-Shift — Situation · False Belief · Truth · Future Projection · CTA",
        slots=("situation", "false_belief", "truth", "future_projection", "cta"),
        awareness=("problem_aware", "solution_aware"),
        best_for="Belief-Reframe: ein falscher Glaubenssatz steht zwischen Zielgruppe "
                 "und Angebot. 'Du denkst X: die Wahrheit ist Y.' Stark fuer kaltes "
                 "TOFU-Prospecting, wenn eine Ueberzeugung der Blocker ist.",
        template="{situation}\n{false_belief}\n{truth}\n{future_projection}\n{cta}",
        note="Belief-Shift: erst den aktuellen Glauben spiegeln, dann den noetigen "
             "aufbauen, DANN der Ask (Roy Furr). Die 'Wahrheit'-Aussage muss BELEGBAR "
             "bleiben — kein manipulativer Fake-Reframe (Geist von compliance_warnings/SKILL-026).",
        funnel=("tofu",),
        traffic=("cold",),
    ),
    "opportunity": CopyFramework(  # Baulig #3 — SKILL-082
        key="opportunity",
        name="Opportunity — New Opportunity · Old Way (Downsides) · New Way (Upsides) · CTA",
        slots=("new_opportunity", "old_way_downsides", "new_way_upsides", "cta"),
        awareness=("solution_aware", "product_aware"),
        best_for="Neuer Mechanismus / 'Shiny Object': das Angebot als grundsaetzlich "
                 "NEUEN Weg rahmen (nicht als inkrementelle Verbesserung). Fuer "
                 "solution_aware/product_aware, die bekannte Wege bereits kennen.",
        template="{new_opportunity}\n{old_way_downsides}\n{new_way_upsides}\n{cta}",
        note="Abgrenzung zu BAB: BAB kontrastiert Ist-/Wunsch-ZUSTAND, Opportunity "
             "kontrastiert LOESUNGSWEGE/Mechanismen. Nur nutzen, wenn der Mechanismus "
             "WIRKLICH neu/anders ist (Todd Brown 'marketplace of one'); unbelegte "
             "'einzigartig am Markt'-Claims meiden (siehe specs.SUPERLATIVE_UNPROVEN). "
             "Visuell stark als split-compare-Layout (alter Weg | neuer Weg).",
        funnel=("mofu",),
        traffic=("warm",),
    ),
    "avatar_story": CopyFramework(  # Baulig #4 — SKILL-083
        key="avatar_story",
        name="Avatar-Story — Self-Select · Problems · Mirrored Customer · "
             "Discovered Solution · New Results · CTA",
        slots=("self_select", "current_problems", "mirrored_customer",
               "discovered_solution", "new_results", "cta"),
        awareness=("problem_aware", "solution_aware"),
        best_for="Kunden-Story/Testimonial-Inszenierung mit Selbst-Selektions-Hook "
                 "('Bist du ein XYZ?'). Testimonials funktionieren immer — 10+ Ads "
                 "dieser Art moeglich. Fuer problem_aware/warm (Identifikation mit dem Kunden).",
        template="{self_select}\n{current_problems}\n{mirrored_customer}\n"
                 "{discovered_solution}\n{new_results}\n{cta}",
        note="Beleg-PFLICHT: braucht eine ECHTE, nachweisbare Referenz — kein erfundenes "
             "Testimonial (konsistent mit dem requires_proof-Guard der testimonial*-ContentTypes, "
             "content_type_compliance_warnings/specs.py). Ebenen-Trennung: dieses Framework ist "
             "die COPY (Argumentations-Arc); die Medien-Bauart bleibt der ContentType 'testimonial'. "
             "Selbst-Selektions-Opener = HOOKS['self_select'] (tauschbarer Hook-Layer).",
        funnel=("mofu",),
        traffic=("warm",),
    ),
    "heros_journey": CopyFramework(  # Baulig #5 — SKILL-084
        key="heros_journey",
        name="Hero's Journey — Past Self · Problems · Nothing Worked · Near Giving Up · "
             "Discovery · New World · Pay It Forward · CTA",
        slots=("past_self", "problems", "nothing_worked", "near_giving_up",
               "discovery", "new_world", "pay_it_forward", "cta"),
        awareness=("product_aware", "most_aware"),
        best_for="Persoenliche Gruender-/Transformations-Story ueber 8 Stufen mit dem "
                 "'near-giving-up -> discovery'-Wendepunkt. Nur sinnvoll, wenn der Absender "
                 "SELBST mal Teil der Zielgruppe war. Primaer als Video/Reel (langer Arc).",
        template="{past_self}\n{problems}\n{nothing_worked}\n{near_giving_up}\n"
                 "{discovery}\n{new_world}\n{pay_it_forward}\n{cta}",
        note="Abgrenzung: voller Monomyth-Arc mit Wendepunkt — NICHT das kompakte "
             "Hook·Story·Offer (hso) und nicht das Langform-PASTOR. Der Gruender ist der "
             "Mentor, der die Zielgruppe durch dieselbe Transformation fuehrt (pay_it_forward). "
             "Medien-Eignung: primaer talking_head/broll_message-Reel (Hook in den ersten 3 s, "
             "Captions Pflicht). Transformation muss belegbar/ehrlich bleiben "
             "(BEFORE_AFTER_TRIGGERS/compliance_warnings — keine ueberzogene Vorher-Nachher-Story).",
        funnel=("mofu", "bofu"),
        traffic=("warm",),
    ),
    # --- SKILL-089: Cold-Audience-Hook-Formeln (F1-F6) ----------------------
    # Menschliche Hook-Formeln fuer eine KALTE Zielgruppe, die den Produkt-/
    # Kategoriebegriff noch NICHT kennt: eine Alltagsszene ZEIGEN statt eine
    # Kategorie zu ERKLAEREN, Fachbegriff nie im Opener. Projektneutral (Slots +
    # Template generisch, KEIN Brand-/Projektwert; konkrete Beispiele stehen nur
    # im begleitenden Playbook, nicht im Code).
    # Quelle: docs/ad-frameworks/agentisches-arbeiten-messaging-playbook.md (§4).
    "scene": CopyFramework(  # F1 — SKILL-089
        key="scene",
        name="Szene-Formel (F1) — Alltagsszene · was von selbst laeuft · Ergebnis · CTA",
        slots=("szene", "was_laeuft", "ergebnis", "cta"),
        awareness=("unaware", "problem_aware"),
        best_for="Staerkste Formel fuer eine KALTE, den-Begriff-nicht-kennende Zielgruppe: "
                 "Zeile 1 ist eine konkrete Alltagsszene (Uhrzeit, Zahl, Handgriff), kein "
                 "Statistik-Claim. Zeigt, was ohne Zutun laeuft, statt die Kategorie zu erklaeren.",
        template="{szene}\n{was_laeuft}\n{ergebnis}\n{cta}",
        note="Human-Rule 1+2: Szene statt These, zeigen statt erklaeren. Fachbegriff nie "
             "im Opener (Human-Rule 3), kein Prozent-Statistik-Opener (Human-Rule 8).",
        funnel=("tofu",),
        traffic=("cold",),
    ),
    "kunden_oton": CopyFramework(  # F2 — SKILL-089
        key="kunden_oton",
        name="O-Ton-Formel (F2) — Kundenzitat · kurze Uebersetzung/Beweis · CTA",
        slots=("zitat", "uebersetzung", "cta"),
        awareness=("unaware", "problem_aware"),
        best_for="Ein ECHTES Kundenzitat (Voice of Customer) als Hook. Wirkt menschlich, "
                 "weil es die Sprache der Zielgruppe 1:1 spiegelt.",
        template="{zitat}\n{uebersetzung}\n{cta}",
        note="Zitat muss echt sein (kein erfundenes Testimonial, Geist des requires_proof-"
             "Guards). Human-Rule 6: die Nomen der Zielgruppe nutzen.",
        funnel=("tofu",),
        traffic=("cold",),
    ),
    "vorher_nachher": CopyFramework(  # F3 — SKILL-089
        key="vorher_nachher",
        name="Vorher/Nachher-Formel (F3) — Frueher (nervig) · Heute (geloest) · CTA",
        slots=("frueher", "heute", "cta"),
        awareness=("unaware", "problem_aware"),
        best_for="Derselbe Alltags-Moment einmal nervig, einmal geloest. Bildstark, "
                 "leicht verstaendlich fuer kalte Zielgruppen. Abgrenzung zu BAB: konkrete "
                 "Alltagsszene statt abstrakter Ist-/Wunsch-Zustand.",
        template="{frueher}\n{heute}\n{cta}",
        note="Transformation belegbar/alltagsnah halten (kein ueberzogener BEFORE_AFTER-Claim, "
             "compliance_warnings/SKILL-026).",
        funnel=("tofu",),
        traffic=("cold",),
    ),
    "einwand_oton": CopyFramework(  # F4 — SKILL-089
        key="einwand_oton",
        name="Einwand-als-O-Ton-Formel (F4) — Einwand (gesprochen) · Haeufigkeit · Aufloesung · CTA",
        slots=("einwand", "haeufigkeit", "aufloesung", "cta"),
        awareness=("problem_aware", "solution_aware"),
        best_for="Zerschlaegt einen Blocker menschlich: der Einwand als gesprochener Satz, "
                 "dann die sachliche Aufloesung. Fuer bekannte Vorbehalte der Zielgruppe.",
        template="{einwand}\n{haeufigkeit}\n{aufloesung}\n{cta}",
        note="Aufloesung muss belegbar sein (kein manipulativer Fake-Reframe). Verwandt mit "
             "mindset_shift, aber im O-Ton der Zielgruppe statt als Belehrung.",
        funnel=("tofu",),
        traffic=("cold",),
    ),
    "anti_hype": CopyFramework(  # F5 — SKILL-089
        key="anti_hype",
        name="Anti-Hype-Formel (F5) — ehrliche unbequeme Wahrheit · warum es trotzdem lohnt · CTA",
        slots=("ehrliche_wahrheit", "warum_lohnt", "cta"),
        awareness=("problem_aware", "solution_aware"),
        best_for="Vertrauen statt Versprechen: eine unbequeme Wahrheit ehrlich vorweg, dann "
                 "der echte Grund, warum es sich trotzdem lohnt. Schlaegt Hype bei skeptischen "
                 "Zielgruppen (SKILL-096: Ehrlichkeit = Vertrauensanker).",
        template="{ehrliche_wahrheit}\n{warum_lohnt}\n{cta}",
        note="Bewusst KEIN Hype/Superlativ (siehe specs.hype_warnings/SKILL-096). Die "
             "unbequeme Wahrheit muss echt sein, nicht kokettierend.",
        funnel=("tofu",),
        traffic=("cold",),
    ),
    "umbruch": CopyFramework(  # F6 — SKILL-089
        key="umbruch",
        name="Umbruch/Einladung-Formel (F6) — Analogie · die Wenigen statt aller · Einladung · CTA",
        slots=("analogie", "wenige_statt_alle", "einladung", "cta"),
        awareness=("unaware", "problem_aware"),
        best_for="Rahmt einen technologischen Umbruch als Einladung (nie als Drohung): eine "
                 "Analogie, die frueh dabei waren, und die Einladung dazuzugehoeren.",
        template="{analogie}\n{wenige_statt_alle}\n{einladung}\n{cta}",
        note="Motivation statt Angst (kein FOMO/'sonst haengst du ab', siehe "
             "specs.brand_voice_warnings/SKILL-092). Einladung, keine Drohung.",
        funnel=("tofu",),
        traffic=("cold",),
    ),
}

# SKILL-089/091: die szenen-/ergebnis-basierten Cold-Audience-Formeln (F1-F6).
# Ad-Daten-Muster (Playbook §5): konkret-menschliche Angles gewinnen bei kalter
# Zielgruppe, abstrakt/Statistik verliert. Deshalb rankt match_frameworks() diese
# Formeln bei traffic="cold" VOR die uebrigen (generische Reihenfolge, kein Projektwert).
COLD_AUDIENCE_FORMULAS: tuple[str, ...] = (
    "scene", "kunden_oton", "vorher_nachher", "einwand_oton", "anti_hype", "umbruch",
)


def get_framework(key: str) -> CopyFramework:
    """Liefert ein Framework per Key oder wirft KeyError (analog specs.get_format)."""
    if key not in FRAMEWORKS:
        raise KeyError(f"Unbekanntes Framework '{key}'. Bekannt: {', '.join(FRAMEWORKS)}")
    return FRAMEWORKS[key]


# === SKILL-089: 8 Human-Messaging-Regeln (kalte Zielgruppe) ==================
# Die 8 Regeln aus dem Playbook (§1) als abrufbare, strukturierte Pruefliste.
# Reine Wissens-/Checklisten-Ebene (das Pendant zu den Warn-Funktionen in
# specs.py). Projektneutral formuliert — die konkreten Beispiele stehen im
# Playbook, nicht hier. `check` verweist auf die automatisierbare Warn-Funktion
# (soweit vorhanden); "" = reine Mensch-im-Loop-Beurteilung.
@dataclass(frozen=True)
class MessagingRule:
    """Eine Human-Messaging-Regel fuer kalte Zielgruppen (Playbook §1)."""
    key: str
    title: str
    rule: str
    check: str = ""  # Name des automatisierten Checks in specs.py (oder "" = nur Urteil)


HUMAN_MESSAGING_RULES: tuple[MessagingRule, ...] = (
    MessagingRule(
        "szene_statt_these", "Szene statt These",
        "Zeile 1 ist ein Bild oder eine echte Frage aus dem Alltag, kein Statistik-Claim.",
        check="specs.human_rule_warnings (Statistik-Opener)"),
    MessagingRule(
        "zeig_erklaer_nicht", "Zeig, erklaer nicht",
        "Beschreibe konkret, was passiert (Anfrage, Termin, Nachfassen); die Kategorie "
        "denkt der Leser selbst.",
        check="specs.human_rule_warnings (Consultant-Abstrakta)"),
    MessagingRule(
        "begriff_zuletzt", "Begriff zuletzt",
        "Der Fachbegriff nie im Opener, hoechstens am Ende als Name fuer das eben Beschriebene.",
        check="specs.human_rule_warnings (category_term)"),
    MessagingRule(
        "ich_zu_du", "Ich zu Du",
        "Aus dem eigenen Betrieb erzaehlt und direkt an das Du gerichtet, keine "
        "'die meisten Unternehmer'-Distanz."),
    MessagingRule(
        "ein_gedanke", "Ein Gedanke pro Ad",
        "Eine Szene, ein Schmerz, ein Ergebnis. Nicht mehrere Botschaften in eine Ad."),
    MessagingRule(
        "ihre_nomen", "Ihre Nomen",
        "Die konkreten Objekte der Zielgruppe nutzen, nicht Consultant-Abstrakta "
        "(Durchsatz, Overhead, Marge).",
        check="specs.human_rule_warnings (Consultant-Abstrakta)"),
    MessagingRule(
        "ergebnis_fuehlbar", "Ergebnis fuehlbar",
        "Das Ergebnis als fuehlbaren Moment zeigen (Feierabend um drei) statt als "
        "abstrakte Kennzahl (15+ Stunden pro Woche)."),
    MessagingRule(
        "krumme_echte_zahl", "Krumme echte Zahl schlaegt runde Statistik",
        "Eine konkrete, krumme Zahl (z. B. 17 statt 20) wirkt echter als eine runde "
        "Prozent-Statistik (93 Prozent). Rhythmus brechen, keine Dauer-Dreier-Listen.",
        check="specs.human_rule_warnings (Statistik-Opener)"),
)


def human_messaging_rules() -> tuple[MessagingRule, ...]:
    """SKILL-089: die 8 Human-Messaging-Regeln als strukturierte Pruefliste (Playbook §1)."""
    return HUMAN_MESSAGING_RULES


# === SKILL-094: CTA-Bibliothek (Button · hart · weich) =======================
# Projektneutrale, wiederverwendbare CTA-Formulierungen nach Verbindlichkeit.
# "button" = Meta-Button-Label (kurz), "hart" = klare Aufforderung, "weich" =
# einladend/niedrigschwellig. Generische deutsche CTAs, kein Projekt-/Brand-Wert.
CTA_LIBRARY: dict[str, tuple[str, ...]] = {
    "button": ("Registrieren", "Anmelden", "Mehr dazu"),
    "hart": ("Trag dich ein", "Sichere dir deinen Platz"),
    "weich": ("Ich zeig dir wie", "Willst du wissen wie"),
}
CTA_CATEGORIES: tuple[str, ...] = ("button", "hart", "weich")


def get_ctas(category: str) -> tuple[str, ...]:
    """SKILL-094: liefert die CTA-Varianten einer Kategorie (button/hart/weich)."""
    key = (category or "").strip().lower()
    if key not in CTA_LIBRARY:
        raise KeyError(f"Unbekannte CTA-Kategorie '{category}'. Bekannt: {', '.join(CTA_LIBRARY)}")
    return CTA_LIBRARY[key]


def cta_category(text: str) -> str | None:
    """SKILL-094: ordnet einen CTA-Text seiner Kategorie zu (oder None, wenn unbekannt)."""
    t = (text or "").strip().lower()
    for cat, variants in CTA_LIBRARY.items():
        if any(t == v.lower() for v in variants):
            return cat
    return None


# === SKILL-095: Ton-Profile / Ansprache (Buyer vs Champion) ==================
# Zwei generische Ansprache-Profile fuer High-Ticket-Kaltkontakt. Projektneutral
# (Struktur, keine Projekt-Texte): Buyer = Entscheider (Ergebnis zuerst, Status,
# im Kaltkontakt eher "Sie"/verdientes Du), Champion = interner Fuersprecher/
# Mitarbeiter (verbuendetes "du", schnelle Wins, Geheimwaffe).
@dataclass(frozen=True)
class ToneProfile:
    """Ein Ansprache-/Ton-Profil (Playbook §7). Projektneutral."""
    key: str
    name: str
    audience: str
    pronoun: str
    lead_with: str
    register: str
    note: str = ""


TONE_PROFILES: dict[str, ToneProfile] = {
    "buyer": ToneProfile(
        key="buyer",
        name="Buyer / Entscheider (DISC D/I)",
        audience="Inhaber/Entscheider mit Budget-Hoheit",
        pronoun="Sie im Kaltkontakt, verdientes Du erst nach Naehe",
        lead_with="Ergebnis zuerst (Zahl/Status), kurz nur fuer den Einstieg",
        register="knapp, status-orientiert, Beweis so lang wie noetig",
        note="du/Sie-Risiko-Asymmetrie: 'Sie' beleidigt nie, ein zu fruehes 'du' kann "
             "anbiedern. High-Ticket: Hook kurz, Beweis so lang wie noetig.",
    ),
    "champion": ToneProfile(
        key="champion",
        name="Champion / interner Fuersprecher (Team/Mitarbeiter)",
        audience="Mitarbeiter/Team, die die Loesung intern tragen",
        pronoun="du, verbuendet auf Augenhoehe",
        lead_with="schnelle Wins / spuerbare Entlastung",
        register="verbuendet, 'Geheimwaffe', begleitet statt belehrt",
        note="Verbuendeter Ton: 'du' als Team, gemeinsame Entlastung, schnelle Erfolge "
             "zuerst. Kein Status-Gehabe.",
    ),
}


def get_tone_profile(key: str) -> ToneProfile:
    """SKILL-095: liefert ein Ton-Profil per Key (buyer/champion) oder wirft KeyError."""
    k = (key or "").strip().lower()
    if k not in TONE_PROFILES:
        raise KeyError(f"Unbekanntes Ton-Profil '{key}'. Bekannt: {', '.join(TONE_PROFILES)}")
    return TONE_PROFILES[k]


# === SKILL-093: Value-Translations (Feature -> gefuehltes Leben) =============
# Projektneutrale Muster-Funktion: uebersetzt Feature-/Technik-Sprache in ein
# fuehlbares Ergebnis. Die konkreten Paare sind PROJEKT-Daten (kommen als
# `translations`-dict rein) — hier nur der generische Mechanismus + der Katalog
# der Feature-Level-Signalverben, an denen untranslatierte Technik-Copy erkennbar ist.
# Feature-Level-Signalverben (generische Consultant-/Technik-Verben, kein Projektwert).
FEATURE_LEVEL_VERBS: tuple[str, ...] = (
    "fuehrt aus", "führt aus", "automatisiert", "orchestriert", "synchronisiert",
    "integriert", "prozessiert", "exekutiert", "verwaltet", "konfiguriert",
    "implementiert", "deployt", "skaliert",
)


def apply_value_translations(text: str, translations: dict[str, str]) -> str:
    """SKILL-093: ersetzt Feature-Formulierungen durch ihre gefuehlte Nutzen-Fassung.

    `translations` mappt Feature-Phrase -> Nutzen-Phrase (projekt-spezifisch, kommt
    als Parameter rein). Ersetzung ist case-insensitiv auf Substring-Ebene; laengere
    Schluessel zuerst (verhindert Teil-Ueberschreibungen). Leeres Mapping -> Text
    unveraendert (nicht-brechend). KEIN Projektwert hartkodiert.
    """
    if not text or not translations:
        return text or ""
    out = text
    for feature in sorted(translations, key=len, reverse=True):
        benefit = translations[feature]
        out = re.sub(re.escape(feature), benefit, out, flags=re.IGNORECASE)
    return out


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
        template="Gib mir {seconds} Sekunden, dann {payoff}.",
        note="Niedrigschwellige Mikro-Zusage. Payoff konkret + ehrlich halten.",
    ),
    "specific_number": HookPattern(
        key="specific_number",
        name="Konkrete Zahl / Reibung",
        template="{anteil} Prozent {zielgruppe} {schmerz}. Jede Woche.",
        note="Spezifische Zahlen schlagen runde (Recherche §3.3). Nur belegbare Zahlen.",
    ),
    "niche_question": HookPattern(
        key="niche_question",
        name="Spezifische Frage an die Nische",
        template="{zielgruppe} mit {merkmal}?",
        note="Selbst-Selektion der relevanten Zielgruppe in Zeile 1.",
    ),
    "self_select": HookPattern(
        key="self_select",
        name="Selbst-Selektions-Opener (Bist du ein XYZ?)",
        template="Bist du ein {zielgruppe}?",
        note="SKILL-083: der tauschbare Opener des avatar_story-Frameworks — filtert in "
             "Zeile 1 genau die kaufkraeftige Zielgruppe. Body (Story) + CTA konstant "
             "halten, nur den Hook variieren (modulares Testimonial-Testing).",
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
        template="{reibung}, und es liegt nicht an {falsche_ursache}.",
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
# SKILL-081/082/083/084: Angle-/Goal-Hints, die gezielt eines der Baulig-Frameworks
# waehlen — additiv und optional. Ohne `goal` bleibt die Awareness-Default-Regel
# unveraendert (nicht-brechend). Ein Goal ueberschreibt die Awareness-Wahl.
GOAL_ALIASES: dict[str, str] = {
    # Belief-Reframe -> mindset_shift (SKILL-081)
    "belief": "mindset_shift", "mindset": "mindset_shift", "glaubenssatz": "mindset_shift",
    "einwand": "mindset_shift", "objection": "mindset_shift", "reframe": "mindset_shift",
    # Neuer Mechanismus -> opportunity (SKILL-082)
    "opportunity": "opportunity", "new_mechanism": "opportunity",
    "neuer_mechanismus": "opportunity", "new_way": "opportunity", "mechanism": "opportunity",
    # Kunden-Story / Testimonial -> avatar_story (SKILL-083)
    "avatar": "avatar_story", "testimonial": "avatar_story", "customer_story": "avatar_story",
    "kundenstory": "avatar_story", "avatar_story": "avatar_story",
    # Gruender-Story -> heros_journey (SKILL-084)
    "founder_story": "heros_journey", "hero": "heros_journey", "heros_journey": "heros_journey",
    "gruenderstory": "heros_journey", "story": "heros_journey",
}


def recommend_framework(awareness: str, placement: str = "", *,
                        funnel: str | None = None, traffic: str | None = None,
                        goal: str | None = None) -> CopyFramework:
    """Empfiehlt das passende Framework nach Awareness-Level (+ optionalen Hints).

    Kurzregel (Recherche §1, "Framework-Wahl nach Awareness"):
      - unaware / cold                -> AIDA (edukieren)
      - problem_aware                 -> PAS (Default fuer Cold-Meta-Ads)
      - solution_aware (vergleichend) -> FAB; bei Video/bildstark -> BAB
      - product_aware                 -> BAB (Anbieter-/Kategorievergleich)
      - most_aware / warm / Video      -> Hook-Story-Offer
    Langform-Placements (vsl, sales_page, email) -> PASTOR (ueberschreibt die Awareness-Regel).

    SKILL-085 (Auslieferungs-Empfehlung): `goal` (Angle-Hint) waehlt gezielt eines der
    Baulig-Frameworks (belief -> mindset_shift, new_mechanism -> opportunity,
    testimonial -> avatar_story, founder_story -> heros_journey) und ueberschreibt die
    Awareness-Default-Regel. `funnel`/`traffic` sind hier optionale Konsistenz-Hints
    (die breitere Auswahl liefert `match_frameworks`); ohne alle drei bleibt das
    Bestandsverhalten exakt erhalten (nicht-brechend).

    Args:
        awareness: ein Wert aus AWARENESS_LEVELS. Synonyme: "cold"->unaware, "warm"->most_aware.
        placement: optionaler Hinweis (z.B. "reel", "video", "story", "vsl", "sales_page",
                   "email") — verfeinert die Auswahl.
        funnel: optionaler Funnel-Hint (tofu/mofu/bofu).
        traffic: optionaler Traffic-Hint (cold/warm/retargeting).
        goal: optionaler Angle-/Ziel-Hint (siehe GOAL_ALIASES) — ueberschreibt die Awareness-Wahl.

    Returns:
        Das empfohlene CopyFramework.

    Raises:
        ValueError: bei unbekanntem Awareness-Wert.
    """
    # SKILL-085: expliziter Angle-/Goal-Hint gewinnt (additiv, nicht-brechend).
    if goal:
        g = goal.strip().lower()
        if g in GOAL_ALIASES:
            return FRAMEWORKS[GOAL_ALIASES[g]]

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


# --- SKILL-085: Auslieferungs-Empfehlung (Matrix + Mehrfach-Auswahl) --------
# Die Empfehlungs-Metadaten (awareness/funnel/traffic/best_for) machen "wann + fuer
# wen" maschinell abfragbar. `match_frameworks` filtert den Katalog ueber die drei
# generischen Achsen; `framework_matrix` liefert die vollstaendige Uebersicht.
def _norm_awareness(value: str) -> str:
    """Mappt Awareness-Synonyme (cold/warm/vergleichend) auf die kanonischen Tags."""
    aw = (value or "").strip().lower()
    return {
        "cold": "unaware", "warm": "most_aware", "retargeting": "most_aware",
        "comparing": "solution_aware", "vergleichend": "solution_aware",
    }.get(aw, aw)


def match_frameworks(awareness: str | None = None, funnel: str | None = None,
                     traffic: str | None = None, goal: str | None = None) -> list[CopyFramework]:
    """SKILL-085: liefert ALLE Frameworks, die zu den gegebenen Achsen passen.

    Jede Achse ist ein optionaler Filter (AND-verknuepft): ist sie None, filtert sie
    nicht. `goal` (Angle-Hint aus GOAL_ALIASES) engt zusaetzlich auf genau ein
    Baulig-Framework ein. Ergebnis ist stabil nach Katalog-Reihenfolge sortiert.

    Beispiel: `match_frameworks(awareness="cold", funnel="tofu")` -> [aida, pas, mindset_shift].

    Raises:
        ValueError: bei unbekanntem awareness/funnel/traffic-Wert (klare Fehlermeldung
        statt stiller Leerliste).
    """
    goal_key = None
    if goal:
        g = goal.strip().lower()
        goal_key = GOAL_ALIASES.get(g)
        if goal_key is None:
            raise ValueError(
                f"Unbekanntes goal '{goal}'. Bekannt: {', '.join(sorted(set(GOAL_ALIASES)))}."
            )

    aw = _norm_awareness(awareness) if awareness else None
    if aw is not None and aw not in AWARENESS_LEVELS:
        raise ValueError(f"Unbekanntes awareness '{awareness}'. Bekannt: {', '.join(AWARENESS_LEVELS)}.")
    fn = funnel.strip().lower() if funnel else None
    if fn is not None and fn not in FUNNEL_STAGES:
        raise ValueError(f"Unbekanntes funnel '{funnel}'. Bekannt: {', '.join(FUNNEL_STAGES)}.")
    tr = traffic.strip().lower() if traffic else None
    if tr is not None and tr not in TRAFFIC_TEMPERATURES:
        raise ValueError(f"Unbekanntes traffic '{traffic}'. Bekannt: {', '.join(TRAFFIC_TEMPERATURES)}.")

    out: list[CopyFramework] = []
    for f in FRAMEWORKS.values():
        if goal_key is not None and f.key != goal_key:
            continue
        if aw is not None and aw not in f.awareness:
            continue
        if fn is not None and fn not in f.funnel:
            continue
        if tr is not None and tr not in f.traffic:
            continue
        out.append(f)
    # SKILL-089/091: bei kalter Zielgruppe die szenen-basierten Formeln zuerst
    # (Ad-Daten-Muster: konkret-menschlich gewinnt, abstrakt/Statistik verliert).
    # Stabile Sortierung -> innerhalb der Gruppen bleibt die Katalog-Reihenfolge.
    if tr == "cold":
        out.sort(key=lambda f: 0 if f.key in COLD_AUDIENCE_FORMULAS else 1)
    return out


def framework_matrix() -> list[dict[str, object]]:
    """SKILL-085: die Empfehlungs-Matrix (Framework -> awareness/funnel/traffic/best_for).

    Eine Zeile je Framework in Katalog-Reihenfolge — die maschinen- und menschenlesbare
    "wann + fuer wen"-Uebersicht. Genutzt von der CLI-Listenausgabe und von Tests.
    """
    return [
        {
            "key": f.key,
            "name": f.name,
            "awareness": list(f.awareness),
            "funnel": list(f.funnel),
            "traffic": list(f.traffic),
            "slots": list(f.slots),
            "best_for": f.best_for,
        }
        for f in FRAMEWORKS.values()
    ]


def format_matrix_table() -> str:
    """SKILL-085: rendert die Empfehlungs-Matrix als ausgerichtete Text-Tabelle (CLI)."""
    rows = framework_matrix()
    header = ("framework", "awareness", "funnel", "traffic", "best_for")
    lines = [
        f"{'framework':<15} {'awareness':<28} {'funnel':<12} {'traffic':<18} best_for",
        f"{'-'*15} {'-'*28} {'-'*12} {'-'*18} {'-'*40}",
    ]
    for r in rows:
        lines.append(
            f"{r['key']:<15} "
            f"{'/'.join(r['awareness']):<28} "
            f"{'/'.join(r['funnel']):<12} "
            f"{'/'.join(r['traffic']):<18} "
            f"{r['best_for']}"
        )
    return "\n".join(lines)


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


# --- CLI: Katalog listen + Framework empfehlen (SKILL-085) ------------------
def main(argv: list[str] | None = None) -> int:
    """CLI-Auswahlhilfe: `list` zeigt die Empfehlungs-Matrix, `recommend` schlaegt vor.

    Beispiele:
      python -m creative_studio.frameworks list
      python -m creative_studio.frameworks recommend --awareness cold --funnel tofu
      python -m creative_studio.frameworks recommend --goal testimonial
    """
    import argparse

    ap = argparse.ArgumentParser(
        description="creative-studio Copy-Framework-Katalog + Auslieferungs-Empfehlung (SKILL-025/085)."
    )
    sub = ap.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="Empfehlungs-Matrix (Framework -> awareness/funnel/traffic/best_for).")
    p_list.add_argument("--json", action="store_true", help="Ausgabe als JSON statt Tabelle.")

    p_rec = sub.add_parser("recommend", help="Passende Framework(s) fuer Achsen vorschlagen.")
    p_rec.add_argument("--awareness", default=None, help=f"eine aus: {', '.join(AWARENESS_LEVELS)} (+ cold/warm).")
    p_rec.add_argument("--funnel", default=None, help=f"eine aus: {', '.join(FUNNEL_STAGES)}.")
    p_rec.add_argument("--traffic", default=None, help=f"eine aus: {', '.join(TRAFFIC_TEMPERATURES)}.")
    p_rec.add_argument("--goal", default=None, help="Angle-Hint (belief/opportunity/testimonial/founder_story ...).")
    p_rec.add_argument("--placement", default="", help="reel/video/story/vsl/sales_page/email (fuer die Einzel-Empfehlung).")

    args = ap.parse_args(argv)

    if args.cmd == "list":
        if getattr(args, "json", False):
            print(json.dumps(framework_matrix(), ensure_ascii=False, indent=2))
        else:
            print(format_matrix_table())
        return 0

    if args.cmd == "recommend":
        try:
            matches = match_frameworks(
                awareness=args.awareness, funnel=args.funnel,
                traffic=args.traffic, goal=args.goal,
            )
        except ValueError as exc:
            print(f"[FEHLER] {exc}")
            return 2
        # Einzel-Empfehlung (Awareness-Default-Regel) nur, wenn ein Awareness gegeben ist.
        if args.awareness or args.goal:
            best = recommend_framework(
                args.awareness or "problem_aware", args.placement,
                funnel=args.funnel, traffic=args.traffic, goal=args.goal,
            )
            print(f"Beste Empfehlung: {best.key} — {best.name}")
        if matches:
            print("Passende Frameworks:")
            for f in matches:
                print(f"  - {f.key:<15} awareness={'/'.join(f.awareness)} "
                      f"funnel={'/'.join(f.funnel)} traffic={'/'.join(f.traffic)}")
        else:
            print("Keine Frameworks passen zu diesen Achsen.")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
