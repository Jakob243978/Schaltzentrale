"""SKILL-028 — Tests fuer das KI-Disclosure-Gate (Pflicht-Label + Warnung).

1 EARS = mind. 1 Test:
  - EARS-1: KI-Element -> sichtbares Label im gerenderten Template.
  - EARS-3: KI-Element ohne aktivierte Disclosure -> Pflicht-Warnung (Gate).
  - EARS-4: rein echtes Material -> kein Label/keine Warnung erzwungen.
  - EARS-5: Label-Text projektneutral (Default-Konstante, kein Brand-Wert).

Das Template wird mit Jinja2 real gerendert (mit/ohne `ai_disclosure`), damit der
Label-Markup-Pfad echt geprueft ist — nicht nur ein String-Assert.

Metadaten-Schreiben (C2PA / PNG-tEXt `ai_generated=true`, EARS-2) ist bewusst
NICHT hier getestet: das ist ein Folgeschritt im Renderer (render_image.py),
nicht in specs.py/Template. Siehe Ticket-Notizen.
"""
import pathlib

import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape

from creative_studio.specs import (
    AdContent,
    requires_ai_disclosure,
    AI_LABEL_TEXT,
    AI_ACT_ENFORCEMENT_DATE,
)

_TEMPLATES_DIR = pathlib.Path(__file__).resolve().parent.parent / "templates"


def _render(ai_disclosure: bool, ai_label_text: str = AI_LABEL_TEXT) -> str:
    """Rendert ad_image.html.j2 mit Minimal-Kontext + dem Disclosure-Flag."""
    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "j2"]),
    )
    tpl = env.get_template("ad_image.html.j2")
    ctx = dict(
        bg="#0a0e27", bg_soft="#1a1f3a", accent="#ff6b35", ink="#fff",
        ink_muted="#cbd5e1", font="sans-serif",
        safe_top=189, safe_bottom=270, safe_x=59,
        w=1080, h=1350,
        fs_brand=28, fs_eyebrow=24, fs_headline=64, fs_subline=32, fs_cta=30,
        headline="Routine an Agenten abgeben",
        subline="", cta="", eyebrow="", brand_name="Beispiel",
        bg_image="", logo_url="", debug_safe=False,
        ai_disclosure=ai_disclosure, ai_label_text=ai_label_text,
    )
    return tpl.render(**ctx)


# --- EARS-1 / EARS-3: requires_ai_disclosure korrekt --------------------------

def test_requires_disclosure_true_for_ai_image():
    assert requires_ai_disclosure(AdContent(headline="x", ai_image=True)) is True


def test_requires_disclosure_true_for_ai_voice():
    assert requires_ai_disclosure(AdContent(headline="x", ai_voice=True)) is True


def test_requires_disclosure_false_for_real_material():
    # EARS-4: kein KI-Bild, keine synthetische Stimme -> kein Gate.
    assert requires_ai_disclosure(AdContent(headline="x")) is False


# --- EARS-3: Warnung bei KI-Element ohne aktivierte Disclosure ----------------

def test_warning_when_ai_image_without_disclosure():
    warns = AdContent(headline="Echtes Foto? Nein, KI", ai_image=True).warnings()
    j = " || ".join(warns).lower()
    assert "ki-disclosure-pflicht" in j
    assert "ki-bild" in j
    assert AI_ACT_ENFORCEMENT_DATE in " || ".join(warns)


def test_warning_when_ai_voice_without_disclosure():
    warns = AdContent(headline="Voice-Clone Spot", ai_voice=True).warnings()
    j = " || ".join(warns).lower()
    assert "ki-disclosure-pflicht" in j
    assert "synthetische stimme" in j


def test_no_warning_when_disclosure_applied():
    # Label gesetzt -> Gate erfuellt, keine Disclosure-Warnung mehr.
    warns = AdContent(
        headline="Routine an Agenten abgeben",
        ai_image=True, disclosure_applied=True,
    ).warnings()
    assert not any("ki-disclosure" in w.lower() for w in warns)


# --- EARS-4: sauberes (echtes) Creative -> keine Disclosure-Warnung -----------

def test_clean_content_no_disclosure_warning():
    warns = AdContent(headline="Routine an Agenten abgeben").warnings()
    assert warns == []
    assert not any("ki-disclosure" in w.lower() for w in warns)


# --- EARS-1: Template rendert das Label nur mit Flag --------------------------

def test_template_renders_label_when_flag_set():
    html = _render(ai_disclosure=True)
    assert 'class="ai-label"' in html
    assert AI_LABEL_TEXT in html  # "KI-generiert"


def test_template_omits_label_without_flag():
    html = _render(ai_disclosure=False)
    assert 'class="ai-label"' not in html
    assert "KI-generiert" not in html


# --- EARS-5: Label-Text projektneutral + ueberschreibbar ----------------------

def test_label_default_is_project_neutral():
    # Default-Konstante traegt keinen Brand-/Projektwert.
    blob = AI_LABEL_TEXT.lower()
    for forbidden in ("immo", "jakob", "creative-studio", "mentoring"):
        assert forbidden not in blob


def test_template_label_text_override():
    html = _render(ai_disclosure=True, ai_label_text="KI")
    assert 'class="ai-label"' in html
    assert ">KI</div>" in html


# --- Regression: bestehende AdContent-Felder/Defaults unveraendert ------------

def test_adcontent_ai_flags_default_false():
    ad = AdContent(headline="Test")
    assert ad.ai_image is False
    assert ad.ai_voice is False
    assert ad.disclosure_applied is False


def test_warnings_never_raise_with_ai_flags():
    ad = AdContent(headline="garantiert", ai_image=True)
    assert isinstance(ad.warnings(), list)
