"""Tests fuer den Editorial-/Struktur-Validator (SKILL-065).

content_structure_warnings() prueft eine maschinelle Reel-Spec auf gute Struktur
(Hook im ersten Fenster, Insight/Value, CTA, Caption-Last/Pacing) und liefert
reine WARNUNGEN — keine Exceptions. Getestet pro Regel + perfekte Struktur
(leere Liste) + Delegation an specs.content_type_warnings().
"""
from creative_studio import content as C
from creative_studio import specs as S


def _caption_track(seconds: float, keyword_idxs=()):
    """Baut einen Caption-Track der Laenge `seconds` (auf 0 ms genullt)."""
    n = max(1, int(seconds))
    step = int((seconds * 1000) / n)
    caps = []
    for i in range(n):
        c = {"text": f"w{i}", "startMs": i * step, "endMs": (i + 1) * step}
        if i in keyword_idxs:
            c["keyword"] = True
        caps.append(c)
    return caps


def _good_spec():
    """Eine strukturell saubere Spec (DISC-rot, alle Teile vorhanden)."""
    return {
        "ad_id": "th-x",
        "hook": "150 Nachrichten pro Woche — so kommen wir hinterher.",
        "subline": "Ein System buendelt alle Gast-Nachrichten an einem Ort.",
        "cta": "Auf die Warteliste",
        "captions": _caption_track(20.0, keyword_idxs=[4, 10]),
    }


def test_perfect_structure_yields_no_warnings():
    """EARS-2: eine saubere Spec liefert eine LEERE Warnungs-Liste (kein Fehlalarm)."""
    assert C.content_structure_warnings(_good_spec()) == []


def test_missing_cta_warns():
    """EARS-1b: kein CTA -> Warnung (Narrativ endet ohne naechste Handlung)."""
    spec = _good_spec()
    spec["cta"] = ""
    w = C.content_structure_warnings(spec)
    assert any("CTA" in x for x in w)


def test_missing_value_part_warns():
    """EARS-1: kein Insight/Value-Teil (subline leer) -> Warnung."""
    spec = _good_spec()
    spec["subline"] = ""
    w = C.content_structure_warnings(spec)
    assert any("Value" in x for x in w)


def test_hook_as_question_warns():
    """EARS-1d: Frage-Floskel als Hook -> DISC-rot-Warnung."""
    spec = _good_spec()
    spec["hook"] = "Hast du auch zu viele Nachrichten?"
    w = C.content_structure_warnings(spec)
    assert any("Hook-Tonalitaet" in x for x in w)


def test_hook_without_number_warns():
    """EARS-1d: Hook ohne Zahl/Ergebnis -> Substanz-Warnung."""
    spec = _good_spec()
    spec["hook"] = "Wir buendeln alle Gast-Nachrichten."
    w = C.content_structure_warnings(spec)
    assert any("Hook-Substanz" in x for x in w)


def test_too_many_keywords_warns():
    """EARS-1c: zu viele betonte Keywords -> Caption-Last-Warnung."""
    spec = _good_spec()
    # 20 Captions, 10 Keywords -> weit ueber Richtwert (20//4 = 5).
    spec["captions"] = _caption_track(20.0, keyword_idxs=range(0, 20, 2))
    w = C.content_structure_warnings(spec)
    assert any("Keyword-Last" in x for x in w)


def test_length_out_of_sweetspot_warns_fallback():
    """EARS-1a: ohne ContentType warnt der Fallback bei zu kurzem Segment."""
    spec = _good_spec()
    spec["captions"] = _caption_track(5.0)  # < STRUCTURE_MIN_SECONDS (12)
    w = C.content_structure_warnings(spec)
    assert any("Laenge" in x for x in w)


def test_length_delegates_to_content_type_warnings():
    """EARS-3: mit ContentType wird die Laenge an specs.content_type_warnings delegiert."""
    spec = _good_spec()
    spec["captions"] = _caption_track(5.0)  # unter talking_head min (20s)
    ct = S.get_content_type("talking_head")
    w = C.content_structure_warnings(spec, ct=ct)
    # Die delegierte Warnung traegt den content_type_warnings-Wortlaut.
    assert any("Video-Laengen-Warnung" in x and "talking_head" in x for x in w)


def test_warnings_never_raise():
    """EARS-3: reine Warnungen, keine Exceptions — auch bei minimaler Spec."""
    # Leere Spec: keine Captions (Laenge uebersprungen), kein Hook -> nur CTA/Value.
    w = C.content_structure_warnings({"ad_id": "x", "brand": {"name": "y"}})
    assert isinstance(w, list)
    assert any("CTA" in x for x in w) and any("Value" in x for x in w)
