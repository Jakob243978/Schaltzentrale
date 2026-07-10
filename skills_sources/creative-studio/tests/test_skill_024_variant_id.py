"""SKILL-024 — Tests fuer die Variant-ID- & UTM-Systematik in specs.py.

1 EARS = mind. 1 Test.
"""
import re

import pytest

from creative_studio.specs import make_variant_id, make_utm_content, slugify


# EARS-1: deterministisch (gleiche Eingabe -> gleiche ID).
def test_variant_id_deterministic():
    a = make_variant_id("h1-immo", "Headline X", "bab", "feed_4x5", hook_index=0)
    b = make_variant_id("h1-immo", "Headline X", "bab", "feed_4x5", hook_index=0)
    assert a == b


# EARS-1: eindeutig (unterschiedliche Eingabe -> unterschiedliche ID, kollisionsfrei).
def test_variant_id_unique_per_input():
    ids = {
        make_variant_id("h1-immo", "H", "bab", "feed_4x5", hook_index=0),
        make_variant_id("h1-immo", "H", "bab", "feed_4x5", hook_index=1),   # anderer Hook-Index
        make_variant_id("h1-immo", "H", "pas", "feed_4x5", hook_index=0),   # anderes Framework
        make_variant_id("h1-immo", "H", "bab", "story_9x16", hook_index=0), # anderes Format
        make_variant_id("h2-immo", "H", "bab", "feed_4x5", hook_index=0),   # andere ad_id
    }
    assert len(ids) == 5  # alle verschieden


# EARS-2: utm_content nach festem Schema — positional, lowercase, nur [a-z0-9-].
def test_utm_content_schema():
    vid = make_variant_id("h1-immo", "H", "bab", "feed_4x5", hook_index=1)
    utm = make_utm_content(vid)
    assert utm == "h1-immo-feed-4x5-bab-h01"
    assert utm == utm.lower()
    assert re.fullmatch(r"[a-z0-9-]+", utm)
    # positional: ad_id zuerst, format vor framework, hook-index am Ende
    assert utm.startswith("h1-immo-")
    assert utm.endswith("-h01")


# EARS-2: gleiche variant_id -> gleiches utm_content (deterministische Ableitung).
def test_utm_content_deterministic():
    vid = make_variant_id("acme", "Hook", "aida", "square_1x1", hook_index=3)
    assert make_utm_content(vid) == make_utm_content(vid)


# EARS-3: unzulaessige Zeichen werden deterministisch normalisiert (slugify).
def test_slugify_normalizes_special_chars():
    assert slugify("Hallo Welt!") == "hallo-welt"
    assert slugify("  Über/Größe  ") == "ueber-groesse"
    assert slugify("a___b   c") == "a-b-c"
    assert slugify("") == "x"          # nie leerer Token
    assert slugify("***") == "x"
    # In der variant_id duerfen keine Leerzeichen/Sonderzeichen ueberleben:
    vid = make_variant_id("H1 Immo!", "Lange Headline mit Satz.", "B.A.B", "feed_4x5", hook_index=0)
    assert re.fullmatch(r"[a-z0-9_-]+", vid)


# EARS-4 [multi-projekt]: kein hartkodierter Projektwert — ad_id bestimmt das Praefix.
def test_project_prefix_comes_from_ad_id():
    a = make_variant_id("projektA", "H", "bab", "feed_4x5", hook_index=0)
    b = make_variant_id("projektB", "H", "bab", "feed_4x5", hook_index=0)
    assert a.startswith("projekta__")
    assert b.startswith("projektb__")
    assert a != b


# EARS-5: Batch/DCO/Reporting nutzen dieselben Funktionen — hier abgesichert,
# dass die einzige Quelle in specs.py liegt (Import-Identitaet).
def test_single_source_functions_importable_from_specs():
    from creative_studio import specs
    assert callable(specs.make_variant_id)
    assert callable(specs.make_utm_content)
    assert callable(specs.slugify)
