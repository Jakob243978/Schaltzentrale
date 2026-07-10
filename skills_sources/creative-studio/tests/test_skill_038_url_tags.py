"""SKILL-036/SKILL-038 — Tests fuer make_url_tags/make_link_url + UTM-Konstanten.

Sichert das UTM-/Makro-Schema gegen Naming-Drift (case-sensitive GA4/DB,
gemischte Trenner, falsche Makro-Syntax). 1 EARS = mind. 1 Test.

Wissensgrundlage: AgentischesArbeiten/docs/marketing/research/
  2026-06-24_utm-tracking-skill.md (§1 Meta-Makros, §4 UTM-Naming, §6 V1/V3).
"""
import re

import pytest

from creative_studio.specs import (
    META_MACROS,
    UTM_MEDIUM_DEFAULT,
    UTM_SOURCE_DEFAULT,
    make_link_url,
    make_url_tags,
    make_utm_content,
    make_variant_id,
)


def _params(query: str) -> list[tuple[str, str]]:
    """Zerlegt einen `&`-getrennten Query-Teil in (key, value)-Paare (ohne `?`)."""
    out = []
    for chunk in query.split("&"):
        if not chunk:
            continue
        k, _, v = chunk.partition("=")
        out.append((k, v))
    return out


# --- SKILL-038 EARS-1: Konstanten vorhanden + korrekte Defaults --------------
def test_utm_default_constants():
    assert UTM_SOURCE_DEFAULT == "meta"
    assert UTM_MEDIUM_DEFAULT == "paid-social"


# --- SKILL-038 EARS-4: META_MACROS = exakt die acht Makros in {{...}}-Syntax --
def test_meta_macros_table():
    expected = {
        "ad.id", "ad.name", "adset.id", "adset.name",
        "campaign.id", "campaign.name", "placement", "site_source_name",
    }
    assert set(META_MACROS) == expected  # nur die acht offiziell unterstuetzten
    for name, macro in META_MACROS.items():
        assert macro == "{{" + name + "}}"            # exakte {{...}}-Syntax
        assert re.fullmatch(r"\{\{[a-z._]+\}\}", macro)


# --- SKILL-036 EARS-1: statische UTM im Query-String -------------------------
def test_url_tags_static_utms():
    vid = make_variant_id("h1-immo", "H", "bab", "feed_4x5", hook_index=0)
    tags = make_url_tags(vid, utm_campaign="warteliste-2026q3")
    params = dict(_params(tags))
    assert params["utm_source"] == "meta"
    assert params["utm_medium"] == "paid-social"
    assert params["utm_campaign"] == "warteliste-2026q3"
    assert tags[0] != "?"  # ohne fuehrendes "?"


# --- SKILL-036 EARS-2: dynamische Meta-Makros roh in {{...}} ------------------
def test_url_tags_dynamic_macros():
    vid = make_variant_id("acme", "H", "pas", "story_9x16", hook_index=2)
    tags = make_url_tags(vid, utm_campaign="launch-2026q3")
    params = dict(_params(tags))
    assert params["utm_term"] == "{{placement}}"
    assert params["utm_platform"] == "{{site_source_name}}"
    assert params["ad_id"] == "{{ad.id}}"
    assert params["cmp_id"] == "{{campaign.id}}"


# --- SKILL-036 EARS-3 / SKILL-038 EARS-5: utm_content == make_utm_content(vid)
def test_url_tags_utm_content_is_join_key():
    vid = make_variant_id("h1-immo", "H", "aida", "square_1x1", hook_index=1)
    tags = make_url_tags(vid, utm_campaign="warteliste-2026q3")
    params = dict(_params(tags))
    assert params["utm_content"] == make_utm_content(vid)


# --- SKILL-038 EARS-5: keine doppelten Param-Keys ----------------------------
def test_url_tags_no_duplicate_keys():
    vid = make_variant_id("h1-immo", "H", "bab", "feed_4x5", hook_index=0)
    tags = make_url_tags(vid, utm_campaign="warteliste-2026q3")
    keys = [k for k, _ in _params(tags)]
    assert len(keys) == len(set(keys))  # jeder Key genau einmal


# --- SKILL-038 EARS-3: statische Werte lowercase + nur "-"-Trenner -----------
def test_url_tags_static_values_hygienic():
    vid = make_variant_id("H1 Immo", "H", "BAB", "feed_4x5", hook_index=0)
    # gemischte Schreibweise + Sonderzeichen in source/medium/campaign:
    tags = make_url_tags(
        vid, utm_campaign="Warteliste 2026/Q3",
        utm_source="Meta", utm_medium="Paid_Social",
    )
    static_keys = {"utm_source", "utm_medium", "utm_campaign", "utm_content"}
    for k, v in _params(tags):
        if k in static_keys:
            assert v == v.lower(), f"{k} nicht lowercase: {v}"
            assert "_" not in v, f"{k} enthaelt '_': {v}"
            assert re.fullmatch(r"[a-z0-9-]+", v), f"{k} unhygienisch: {v}"


# --- SKILL-036 EARS-4: utm_campaign Pflicht-Arg ------------------------------
def test_url_tags_campaign_required():
    vid = make_variant_id("h1-immo", "H", "bab", "feed_4x5", hook_index=0)
    with pytest.raises(ValueError):
        make_url_tags(vid, utm_campaign="")
    with pytest.raises(ValueError):
        make_url_tags(vid, utm_campaign="   ")


# --- SKILL-038 EARS-6 [multi-projekt]: kein hartkodierter Projektwert --------
def test_url_tags_project_neutral():
    vid = make_variant_id("projektA", "H", "bab", "feed_4x5", hook_index=0)
    a = make_url_tags(vid, utm_campaign="camp-a")
    b = make_url_tags(
        make_variant_id("projektB", "H", "bab", "feed_4x5", hook_index=0),
        utm_campaign="camp-b",
    )
    # source/medium sind projektneutrale Defaults, campaign/content tragen das Projekt:
    assert "utm_source=meta" in a and "utm_source=meta" in b
    assert "utm_campaign=camp-a" in a
    assert "utm_campaign=camp-b" in b
    assert a != b


# --- SKILL-036 EARS-5: make_link_url verbindet LP-URL korrekt ----------------
def test_link_url_query_separator():
    vid = make_variant_id("h1-immo", "H", "bab", "feed_4x5", hook_index=0)
    tags = make_url_tags(vid, utm_campaign="warteliste-2026q3")
    # ohne vorhandenen Query -> "?"
    u1 = make_link_url("https://x.de/warteliste", vid, utm_campaign="warteliste-2026q3")
    assert u1 == f"https://x.de/warteliste?{tags}"
    # mit vorhandenem Query -> "&"
    u2 = make_link_url("https://x.de/lp?ref=a", vid, utm_campaign="warteliste-2026q3")
    assert u2 == f"https://x.de/lp?ref=a&{tags}"


# --- SKILL-036 EARS-5: Fragment-Anker bleibt am Ende -------------------------
def test_link_url_preserves_fragment():
    vid = make_variant_id("h1-immo", "H", "bab", "feed_4x5", hook_index=0)
    u = make_link_url("https://x.de/lp#cta", vid, utm_campaign="warteliste-2026q3")
    assert u.endswith("#cta")
    assert "?utm_source=meta" in u
    # Makros UEBERLEBEN unencoded vor dem Fragment:
    assert "utm_term={{placement}}" in u
