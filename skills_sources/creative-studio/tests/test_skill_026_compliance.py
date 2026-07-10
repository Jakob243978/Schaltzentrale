"""SKILL-026 — Tests fuer den DACH-Compliance-Guard (UWG/HWG) + Ad<->LP-Message-Match.

1 EARS = mind. 1 Test. Treffer-Test + Gegenprobe je Kategorie; Message-Match
greift/greift nicht; bestehende Coaching-Warnung weiter funktionsfaehig.

Wichtig: Alles sind WARNUNGEN, keine harten Sperren (kein Exception/Block).
"""
import pytest

from creative_studio.specs import (
    AdContent,
    compliance_warnings,
    message_match_warning,
    GUARANTEE_TRIGGERS,
    SUPERLATIVE_UNPROVEN,
    SUCCESS_PROMISE_TRIGGERS,
    HEALTH_TRIGGERS,
    SCARCITY_FAKE,
    BEFORE_AFTER_TRIGGERS,
    COACHING_CLAIM_TRIGGERS,
)


def _joined(warns: list[str]) -> str:
    return " || ".join(warns).lower()


# --- EARS-1 + EARS-2: Trigger-Kategorien treffen, Warntext nennt Rechtsgrundlage ---

# EARS-1/2: Garantie-Claim -> UWG §5.
def test_guarantee_trigger_hits_with_uwg_hint():
    w = compliance_warnings("Erfolg garantiert in unserem Mentoring")
    assert w
    assert "uwg" in _joined(w) and "§5" in _joined(w)
    assert "abmahngefaehrdet" in _joined(w)


def test_guarantee_trigger_clean_no_warning():
    w = compliance_warnings("Routine an KI-Agenten abgeben, nachvollziehbar dokumentiert")
    assert w == []


# EARS-1/2: unbelegte Spitzenstellung -> UWG §5.
def test_superlative_trigger_hits_with_uwg_hint():
    w = compliance_warnings("Die beste Beratung fuer Immobilien-Unternehmer")
    assert w
    assert "spitzenstellung" in _joined(w) or "superlativ" in _joined(w)
    assert "uwg" in _joined(w)


def test_superlative_clean_no_warning():
    assert compliance_warnings("Eine fundierte Beratung fuer Immobilien-Unternehmer") == []


# EARS-1/2: Erfolgs-/Ergebnis-Versprechen -> UWG §5.
def test_success_promise_trigger_hits():
    w = compliance_warnings("Verdopple deinen Umsatz mit unserem System")
    assert w
    assert "ergebnis-versprechen" in _joined(w) or "erfolgs" in _joined(w)
    assert "uwg" in _joined(w)


def test_success_promise_clean_no_warning():
    assert compliance_warnings("Mehr Zeit fuer Entscheidungen, weniger Routine") == []


# EARS-1/2: Gesundheits-/Heilbezug -> HWG.
def test_health_trigger_hits_with_hwg_hint():
    w = compliance_warnings("Dieses Programm heilt deinen Burnout")
    assert w
    assert "hwg" in _joined(w)


def test_health_clean_no_warning():
    assert compliance_warnings("Weniger Stress im Arbeitsalltag durch klare Prozesse") == []


# EARS-1/2: Fake-Verknappung -> Schwarze Liste.
def test_scarcity_trigger_hits_with_schwarze_liste_hint():
    w = compliance_warnings("Nur noch heute: letzte Plaetze sichern!")
    assert w
    assert "schwarze liste" in _joined(w)


def test_scarcity_clean_no_warning():
    # echte Limitierung ohne Fake-Trigger -> keine Warnung
    assert compliance_warnings("Begrenzte Kohorte, Start im Herbst") == []


# EARS-1/2: Vorher-Nachher-Transformation -> UWG §5 + Coaching.
def test_before_after_trigger_hits():
    w = compliance_warnings("Unser Vorher-Nachher zeigt: vom Anfaenger zum Profi")
    assert w
    assert "vorher-nachher" in _joined(w)


def test_before_after_clean_no_warning():
    assert compliance_warnings("Schritt fuer Schritt an deinen Prozessen") == []


# EARS-1: bestehende Coaching-Warnung weiter funktionsfaehig (Regression).
def test_existing_coaching_trigger_still_warns():
    w = compliance_warnings("Endlich erfolgreich, dein Leben veraendert sich")
    assert w
    j = _joined(w)
    assert "coaching" in j


def test_coaching_clean_no_warning():
    assert compliance_warnings("Konkrete Methodik, nachvollziehbar dokumentiert") == []


# --- EARS-3 + EARS-4: Ad<->LP-Message-Match -----------------------------------

# EARS-3: Mismatch -> Warnung.
def test_message_match_mismatch_warns():
    w = message_match_warning(
        headline="Routine an KI-Agenten abgeben",
        landing_promise="Jetzt Termin beim Steuerberater vereinbaren",
    )
    assert w is not None
    assert "message-match" in w.lower()


# EARS-3: gemeinsamer Kern-Begriff -> keine Warnung.
def test_message_match_match_no_warning():
    w = message_match_warning(
        headline="Routine an KI-Agenten abgeben",
        landing_promise="Trag dich ein und gib Routine an Agenten ab",
    )
    assert w is None


# EARS-4: landing_promise leer -> keine Message-Match-Warnung.
def test_message_match_empty_promise_no_warning():
    assert message_match_warning("Beliebige Headline hier", "") is None
    assert message_match_warning("Beliebige Headline hier", "   ") is None


# --- Integration in AdContent.warnings() (Aufrufer profitieren automatisch) ----

def test_adcontent_integrates_compliance_warning():
    ad = AdContent(headline="Erfolg garantiert in 30 Tagen zu mehr Umsatz")
    warns = ad.warnings()
    j = _joined(warns)
    assert "uwg" in j
    assert "abmahngefaehrdet" in j


def test_adcontent_clean_no_compliance_warning():
    ad = AdContent(headline="Routine an Agenten abgeben")
    # darf keine Compliance-/Message-Match-Warnung haben (Headline kurz, kein Trigger)
    assert ad.warnings() == []


def test_adcontent_message_match_via_field():
    ad = AdContent(
        headline="Routine an Agenten abgeben",
        landing_promise="Termin beim Anwalt buchen",
    )
    assert any("message-match" in w.lower() for w in ad.warnings())


def test_adcontent_no_message_match_without_field():
    ad = AdContent(headline="Routine an Agenten abgeben")
    assert not any("message-match" in w.lower() for w in ad.warnings())


def test_adcontent_landing_promise_default_empty():
    # EARS-4: Feld bleibt optional -> bestehende Aufrufer brechen nicht.
    ad = AdContent(headline="Test")
    assert ad.landing_promise == ""


# --- EARS-5 (multi-projekt): Trigger projektneutral (keine Brand-/Projektwerte) ---

def test_triggers_are_project_neutral():
    all_triggers = (
        GUARANTEE_TRIGGERS + SUPERLATIVE_UNPROVEN + SUCCESS_PROMISE_TRIGGERS
        + HEALTH_TRIGGERS + SCARCITY_FAKE + BEFORE_AFTER_TRIGGERS + COACHING_CLAIM_TRIGGERS
    )
    blob = " ".join(all_triggers).lower()
    # keine projekt-/markenspezifischen Begriffe hartkodiert
    for forbidden in ("immo", "jakob", "mentoring", "agentisch", "creative-studio"):
        assert forbidden not in blob


# --- Heuristik liefert nur Warnungen, keine harte Sperre ----------------------

def test_warnings_never_raise():
    # darf nie eine Exception werfen, egal wie der Text aussieht
    for txt in ("", "garantiert beste heilung nur heute", None and ""):
        assert isinstance(compliance_warnings(txt), list)
    assert isinstance(AdContent(headline="garantiert").warnings(), list)
