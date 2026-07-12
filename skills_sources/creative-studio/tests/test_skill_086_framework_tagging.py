"""SKILL-086 — Tests fuer das Methoden-Tagging im Output (Bild UND Video).

Das verwendete Copy-Framework muss durchgaengig ablesbar sein: im variant_id/
utm_content, im Dateinamen und in den Metadaten (Bild-Sidecar / Reel-props /
Batch-manifest). Reine Datenfunktionen -> kein Playwright/Remotion noetig.
"""
from __future__ import annotations

import json

import pytest

from creative_studio.specs import AdContent, get_format, make_utm_content, slugify
from creative_studio import render_image as ri
from creative_studio import reel_spec as rs


# === BILD =================================================================== #
def test_adcontent_has_framework_field_default():
    c = AdContent(headline="H")
    assert c.framework == "default"  # Bestand: Default beibehalten


def test_image_filename_carries_framework_when_set():
    # Der Framework-Key wird dateiname-tauglich slugifiziert ("_" -> "-", SKILL-024).
    fmt = get_format("feed_4x5")
    c = AdContent(headline="H", ad_id="acme", framework="mindset_shift")
    stem = ri.image_output_stem(c, fmt)
    assert slugify("mindset_shift") in stem  # -> "mindset-shift"
    assert stem == "acme__mindset-shift__feed_4x5"


def test_image_filename_unchanged_for_default_framework():
    # "Default beibehalten fuer Bestand": ohne Framework kein Token im Namen.
    fmt = get_format("feed_4x5")
    c = AdContent(headline="H", ad_id="acme")
    assert ri.image_output_stem(c, fmt) == "acme__feed_4x5"


def test_image_meta_has_explicit_framework_field():
    fmt = get_format("story_9x16")
    c = AdContent(headline="Schluss mit Leerstand", ad_id="acme",
                  framework="opportunity", cta="Jetzt")
    meta = ri.build_image_meta(c, fmt)
    assert meta["framework"] == "opportunity"  # roher Key im Metadaten-Feld
    assert meta["media"] == "image"
    assert meta["format"] == "story_9x16"
    # variant_id/utm_content tragen das (slugifizierte) Framework ebenfalls (SKILL-024).
    assert slugify("opportunity") in meta["variant_id"]
    assert slugify("opportunity") in meta["utm_content"]
    assert meta["utm_content"] == make_utm_content(meta["variant_id"])


def test_image_meta_default_framework_still_tagged():
    # Auch Bestands-Renders (Default) fuehren ein explizites framework-Feld.
    fmt = get_format("square_1x1")
    c = AdContent(headline="H", ad_id="acme")
    meta = ri.build_image_meta(c, fmt)
    assert meta["framework"] == "default"


# === VIDEO ================================================================== #
def _reel_spec_dict(framework="heros_journey"):
    return {
        "ad_id": "acme",
        "hook": "In 6 Monaten Routine abgeben",
        "framework": framework,
        "brand": {"name": "Acme"},
    }


def test_reel_props_have_explicit_framework_field():
    spec = rs.parse_reel_spec(_reel_spec_dict("heros_journey"))
    props = rs.reel_spec_to_props(spec)
    assert props["framework"] == "heros_journey"


def test_reel_variant_id_carries_framework():
    spec = rs.parse_reel_spec(_reel_spec_dict("avatar_story"))
    assert slugify("avatar_story") in spec.variant_id  # -> "avatar-story"
    assert slugify("avatar_story") in spec.utm_content


def test_reel_props_variant_matches_utm():
    spec = rs.parse_reel_spec(_reel_spec_dict("mindset_shift"))
    props = rs.reel_spec_to_props(spec)
    assert props["utmContent"] == make_utm_content(props["variantId"])
    # variantId ist die kanonische Basis fuer den Output-Dateinamen (mp4).
    assert slugify("mindset_shift") in props["variantId"]  # -> "mindset-shift"


def test_reel_default_framework_still_present():
    spec = rs.parse_reel_spec({"ad_id": "acme", "hook": "H", "brand": {"name": "Acme"}})
    props = rs.reel_spec_to_props(spec)
    assert props["framework"] == "hook"  # Reel-Default
