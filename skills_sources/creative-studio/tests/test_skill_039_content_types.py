"""SKILL-039/040/042 — Tests fuer die ContentType-Ebene + Validatoren.

Deckt ab:
  - SKILL-039: ContentType-Dataclass, CONTENT_TYPES-Katalog, get_content_type,
               Format-/Framework-Key-Gueltigkeit, Projektneutralitaet.
  - SKILL-040: content_type_warnings() (Slide-/Video-/On-Screen-Grenzfaelle,
               leere Liste bei Konformitaet, irrelevante Felder uebersprungen).
  - SKILL-042: erweiterte beweis-/personenbezogene Typen + Compliance-/Beleg-/
               KI-Disclosure-Kopplung.

1 EARS = mind. 1 Test. Wissensgrundlage:
  AgentischesArbeiten/docs/marketing/research/2026-06-24_social-content-types.md (§3.1/§3.2).
"""
import pytest

from creative_studio import frameworks
from creative_studio.specs import (
    AI_ACT_ENFORCEMENT_DATE,
    AI_LABEL_TEXT,
    CONTENT_TYPES,
    FORMATS,
    ONSCREEN_WORD_LIMIT_DEFAULT,
    ContentType,
    content_type_compliance_warnings,
    content_type_warnings,
    get_content_type,
)


# ============================================================================
# SKILL-039 — ContentType + Katalog
# ============================================================================

# --- EARS-1: ContentType-Dataclass traegt die Felder aus §3.1 ----------------
def test_content_type_dataclass_fields():
    expected = {
        "key", "name", "medium", "funnel", "formats",
        "min_seconds", "max_seconds", "hook_window_seconds",
        "min_slides", "max_slides", "onscreen_word_limit",
        "recommended_framework", "note",
    }
    fields = set(ContentType.__dataclass_fields__)
    assert expected <= fields, f"Fehlende Felder: {expected - fields}"


# --- EARS-2: CONTENT_TYPES enthaelt mindestens die Basis-Sechs ---------------
def test_content_types_minimum_catalog():
    must_have = {
        "static_statement", "carousel", "educational_carousel",
        "short_video_text_hook", "talking_head", "listicle",
    }
    assert must_have <= set(CONTENT_TYPES), (
        f"Fehlende Basis-Typen: {must_have - set(CONTENT_TYPES)}"
    )
    # mediums plausibel
    assert CONTENT_TYPES["static_statement"].medium == "image"
    assert CONTENT_TYPES["carousel"].medium == "multi_image"
    assert CONTENT_TYPES["short_video_text_hook"].medium == "video"


# --- EARS-3a: jeder formats-Eintrag ist ein gueltiger FORMATS-Key ------------
def test_content_type_formats_are_valid():
    for ct in CONTENT_TYPES.values():
        assert ct.formats, f"{ct.key} hat keine Formate"
        for fmt in ct.formats:
            assert fmt in FORMATS, f"{ct.key}: ungueltiger Format-Key '{fmt}'"


# --- EARS-3b: jeder recommended_framework ist ein gueltiger FRAMEWORKS-Key ---
def test_content_type_framework_keys_valid():
    for ct in CONTENT_TYPES.values():
        if ct.recommended_framework is not None:
            assert ct.recommended_framework in frameworks.FRAMEWORKS, (
                f"{ct.key}: ungueltiger Framework-Key '{ct.recommended_framework}'"
            )


# --- EARS-4: get_content_type ok + KeyError mit bekannten Keys ---------------
def test_get_content_type_ok():
    ct = get_content_type("carousel")
    assert isinstance(ct, ContentType)
    assert ct.key == "carousel"


def test_get_content_type_keyerror():
    with pytest.raises(KeyError) as exc:
        get_content_type("does_not_exist")
    # Meldung listet die bekannten Keys (analog get_format)
    assert "carousel" in str(exc.value)


# --- EARS-5 [multi-projekt]: kein hartkodierter Brand-/Projektwert -----------
def test_content_types_project_neutral():
    # Bekannte Projekt-/Brand-Begriffe duerfen im Katalog NICHT auftauchen.
    forbidden = ("jakse", "jakob", "immobewertung", "warteliste", "dm-drogerie", "beyerimmo")
    blob = " ".join(
        f"{ct.key} {ct.name} {ct.note}".lower() for ct in CONTENT_TYPES.values()
    )
    for term in forbidden:
        assert term not in blob, f"Projekt-/Brand-Begriff '{term}' im Katalog"


# --- Zusatz: onscreen_word_limit-Default spiegelt frameworks.MAX_WORDS_ONSCREEN
def test_onscreen_word_limit_default_matches_frameworks():
    assert ONSCREEN_WORD_LIMIT_DEFAULT == frameworks.MAX_WORDS_ONSCREEN


# ============================================================================
# SKILL-040 — content_type_warnings()
# ============================================================================

# --- EARS-1: Slide-Anzahl unter min -> genau eine Warnung --------------------
def test_warn_slides_below_min():
    ct = get_content_type("carousel")  # min_slides=3
    w = content_type_warnings(ct, slides=2)
    assert len(w) == 1
    assert "2" in w[0] and "3-10" in w[0]


# --- EARS-1: Slide-Anzahl ueber max -> genau eine Warnung --------------------
def test_warn_slides_above_max():
    ct = get_content_type("carousel")  # max_slides=10
    w = content_type_warnings(ct, slides=12)
    assert len(w) == 1
    assert "12" in w[0]


# --- EARS-2: Video-Laenge ausserhalb Sweetspot -> genau eine Warnung ---------
def test_warn_video_length_out_of_range():
    ct = get_content_type("short_video_text_hook")  # 8-20s
    w_long = content_type_warnings(ct, seconds=40)
    assert len(w_long) == 1
    assert "40" in w_long[0]
    w_short = content_type_warnings(ct, seconds=3)
    assert len(w_short) == 1
    assert "3" in w_short[0]


# --- EARS-3: On-Screen-Text ueber Wortlimit -> Warnung pro verletzendem Text -
def test_warn_onscreen_word_limit():
    ct = get_content_type("short_video_text_hook")  # onscreen_word_limit=7
    texts = [
        "kurz genug",                                  # 2 Woerter -> ok
        "eins zwei drei vier fuenf sechs sieben acht", # 8 Woerter -> Warnung
    ]
    w = content_type_warnings(ct, onscreen_texts=texts)
    assert len(w) == 1
    assert "8 Woerter" in w[0]
    # Aequivalenz zur bestehenden Helper-Funktion (kein Doppel):
    assert not frameworks.hook_fits_onscreen(texts[1], 7)


# --- EARS-4: alle Constraints eingehalten -> leere Liste --------------------
def test_no_warnings_when_within_constraints():
    ct = get_content_type("carousel")
    assert content_type_warnings(ct, slides=5) == []
    vid = get_content_type("short_video_text_hook")
    assert content_type_warnings(vid, seconds=12, onscreen_texts=["drei kurze worte"]) == []


# --- EARS-5: irrelevante Felder (None) werden uebersprungen statt zu crashen -
def test_irrelevant_fields_skipped():
    # Bild-Typ ohne Video-Felder: seconds-Pruefung darf nicht crashen.
    img = get_content_type("static_statement")
    assert content_type_warnings(img, seconds=99, slides=99) == []
    # Video-Typ ohne Slide-Felder: slides-Pruefung darf nicht crashen.
    vid = get_content_type("talking_head")
    assert content_type_warnings(vid, slides=99) == []


# ============================================================================
# SKILL-042 — erweiterte Typen + Compliance-/Beleg-/Disclosure-Kopplung
# ============================================================================

# --- EARS-1: erweiterte Typen sind im Katalog mit gueltigen Keys ------------
def test_extended_content_types_present():
    extended = {
        "talking_head", "testimonial", "testimonial_video", "before_after",
        "voiceover_broll", "ugc_style", "story_ad",
    }
    assert extended <= set(CONTENT_TYPES), (
        f"Fehlende erweiterte Typen: {extended - set(CONTENT_TYPES)}"
    )
    for key in extended:
        ct = CONTENT_TYPES[key]
        for fmt in ct.formats:
            assert fmt in FORMATS
        if ct.recommended_framework:
            assert ct.recommended_framework in frameworks.FRAMEWORKS


# --- EARS-2: before_after triggert compliance_warnings (BEFORE_AFTER_TRIGGERS)
def test_before_after_triggers_compliance():
    ct = get_content_type("before_after")
    assert ct.requires_compliance_check is True
    w = content_type_compliance_warnings(ct, "Vom Anfaenger zum Profi in 30 Tagen zu Erfolg")
    assert any("UWG" in x or "abmahn" in x.lower() for x in w)


# --- EARS-2: testimonial triggert compliance_warnings bei Claim-Trigger ------
def test_testimonial_triggers_compliance():
    ct = get_content_type("testimonial")
    w = content_type_compliance_warnings(ct, "Garantiert beste Ergebnisse, Nr. 1 am Markt")
    assert any("UWG" in x for x in w)


# --- EARS-3: testimonial/_video -> Beleg-Pflicht-Hinweis --------------------
def test_testimonial_beleg_hint():
    for key in ("testimonial", "testimonial_video"):
        ct = get_content_type(key)
        assert ct.requires_proof is True
        w = content_type_compliance_warnings(ct, "neutraler text ohne claim")
        assert any("Beleg-Pflicht" in x for x in w), key


# --- EARS-4: synthetische Stimme (ai_voice) -> KI-Disclosure-Pflicht ---------
def test_synthetic_voice_triggers_disclosure():
    for key in ("talking_head", "voiceover_broll", "testimonial_video"):
        ct = get_content_type(key)
        w = content_type_compliance_warnings(ct, "", ai_voice=True)
        assert any("KI-Disclosure" in x for x in w), key
        # enthaelt Label + Stichtag (SKILL-028)
        joined = " ".join(w)
        assert AI_LABEL_TEXT in joined
        assert AI_ACT_ENFORCEMENT_DATE in joined
    # Bild-Typ mit ai_voice -> KEINE Disclosure (medium != video)
    img = get_content_type("testimonial")
    w_img = content_type_compliance_warnings(img, "", ai_voice=True)
    assert not any("KI-Disclosure" in x for x in w_img)


# --- EARS-5 [multi-projekt]: erweiterte Typen projektneutral ----------------
def test_extended_types_project_neutral():
    forbidden = ("jakse", "jakob", "immobewertung", "warteliste", "beyerimmo")
    for key in ("testimonial", "before_after", "ugc_style"):
        ct = get_content_type(key)
        blob = f"{ct.key} {ct.name} {ct.note}".lower()
        for term in forbidden:
            assert term not in blob, f"{key}: Projekt-Begriff '{term}'"
