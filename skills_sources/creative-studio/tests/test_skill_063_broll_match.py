"""Tests fuer das B-Roll-zu-Transkript-Matching (SKILL-063, v1 keyword-basiert).

Getestet wird die Tier-0-Keyword-/Token-Overlap-Logik gegen Fixtures (Manifest +
Verzeichnis), inkl. der Edge-Cases: kein Match (leere Position statt Fehl-Clip),
leere Bibliothek, Dateiname-als-Tag-Fallback und der Convenience-Pfad
Decision -> broll[]. KEINE echten Medien — nur Manifest/Fixtures.
"""
import pytest

from creative_studio import broll_match as B
from creative_studio import content as C
from creative_studio import reel_spec as RS


# --- Fixtures ---------------------------------------------------------------
TRANSCRIPT = {
    "language": "de",
    "full_text": "wir haben 16 Ferienwohnungen 150 Nachrichten pro Woche",
    "word_count": 8,
    "words": [
        {"text": "wir", "startMs": 0, "endMs": 200, "p": 1.0},
        {"text": "haben", "startMs": 200, "endMs": 500, "p": 1.0},
        {"text": "16", "startMs": 500, "endMs": 800, "p": 0.9},
        {"text": "Ferienwohnungen", "startMs": 800, "endMs": 1600, "p": 0.8},
        {"text": "150", "startMs": 1600, "endMs": 1900, "p": 0.9},
        {"text": "Nachrichten", "startMs": 1900, "endMs": 2400, "p": 1.0},
        {"text": "pro", "startMs": 2400, "endMs": 2600, "p": 1.0},
        {"text": "Woche", "startMs": 2600, "endMs": 3000, "p": 1.0},
    ],
}

# B-Roll-Manifest (Tag-/Manifest-Konvention).
LIBRARY = [
    {"src": "broll/ferienwohnung_balkon.mp4", "tags": ["ferienwohnung", "balkon"], "seconds": 2.0},
    {"src": "broll/handy_nachrichten.mp4", "tags": ["nachrichten", "handy", "chat"]},
    {"src": "broll/sonnenuntergang.mp4", "description": "ruhiger Sonnenuntergang am Meer"},
]


def test_match_cue_picks_best_token_overlap():
    """EARS-1: die Cue 'Ferienwohnungen' matcht den ferienwohnung-Clip (Overlap)."""
    clips = B.load_library(LIBRARY)
    m = B.match_cue(B.BrollCue(phrase="16 Ferienwohnungen"), clips)
    assert m.matched
    assert m.clip.src.endswith("ferienwohnung_balkon.mp4")
    assert m.score >= 1


def test_match_cue_no_overlap_leaves_empty():
    """EARS-2: kein passendes Asset -> kein erzwungener Clip (matched=False)."""
    clips = B.load_library(LIBRARY)
    m = B.match_cue(B.BrollCue(phrase="quartalsbericht steuerberater"), clips)
    assert not m.matched
    assert m.clip is None and m.score == 0


def test_empty_library_yields_no_broll():
    """EARS-2: leere Bibliothek -> leere broll-Liste (kein Crash, kein Fake)."""
    cues = [B.BrollCue(phrase="150 Nachrichten")]
    assert B.match_broll(cues, []) == []


def test_match_broll_returns_reel_spec_schema():
    """EARS-1: Output ist {src, seconds} und in eine Reel-Spec ladbar."""
    cues = [
        B.BrollCue(phrase="16 Ferienwohnungen", seconds=2.0),
        B.BrollCue(phrase="150 Nachrichten", seconds=1.5),
    ]
    broll = B.match_broll(cues, B.load_library(LIBRARY))
    assert len(broll) == 2
    assert {"src", "seconds"} <= set(broll[0])
    # In eine echte Reel-Spec einsetzbar (reel_spec.BrollClipSpec-kompatibel).
    spec = {
        "ad_id": "th-x", "hook": "150 Nachrichten",
        "brand": {"name": "JAKSE"}, "broll": broll,
    }
    parsed = RS.parse_reel_spec(spec)
    assert len(parsed.broll) == 2
    assert parsed.broll[0].src.endswith("ferienwohnung_balkon.mp4")


def test_no_repeat_consumes_clip_once():
    """Default allow_repeat=False: derselbe Clip belegt nicht zwei Aussagen."""
    cues = [B.BrollCue(phrase="Nachrichten"), B.BrollCue(phrase="Nachrichten")]
    broll = B.match_broll(cues, B.load_library(LIBRARY))
    # Zweite identische Cue findet keinen frischen passenden Clip mehr -> 1 Eintrag.
    assert len(broll) == 1
    broll_rep = B.match_broll(cues, B.load_library(LIBRARY), allow_repeat=True)
    assert len(broll_rep) == 2  # mit Repeat darf der Clip doppelt belegen


def test_filename_is_implicit_tag_source():
    """Ohne tags/description dient der Dateiname als implizite Tag-Quelle."""
    clips = B.load_library([{"src": "clips/balkon_ferienwohnung.mp4"}])
    m = B.match_cue(B.BrollCue(phrase="Ferienwohnungen mit Balkon"), clips)
    assert m.matched and m.clip.src.endswith("balkon_ferienwohnung.mp4")


def test_build_cues_from_decision_keywords():
    """build_broll_cues: eine Cue je Keyword-Phrase (mit Kontext-Fenster)."""
    dec = C.EditorialDecision(start_word=0, end_word=7, hook="150 Nachrichten",
                              keyword_words=[3, 5])
    cues = B.build_broll_cues(TRANSCRIPT, dec)
    assert len(cues) == 2
    assert "Ferienwohnungen" in cues[0].phrase
    assert "Nachrichten" in cues[1].phrase


def test_build_cues_fallback_to_hook_when_no_keywords():
    """Ohne Keywords faellt build_broll_cues auf eine Hook-Cue zurueck."""
    dec = C.EditorialDecision(start_word=0, end_word=7, hook="16 Ferienwohnungen")
    cues = B.build_broll_cues(TRANSCRIPT, dec)
    assert len(cues) == 1 and "Ferienwohnungen" in cues[0].phrase


def test_match_broll_for_decision_end_to_end():
    """EARS-1: Convenience-Pfad Transkript+Decision+Manifest -> broll[]."""
    dec = C.EditorialDecision(start_word=0, end_word=7, hook="150 Nachrichten",
                              keyword_words=[3, 5])
    broll = B.match_broll_for_decision(TRANSCRIPT, dec, LIBRARY)
    srcs = [b["src"] for b in broll]
    assert any(s.endswith("ferienwohnung_balkon.mp4") for s in srcs)
    assert any(s.endswith("handy_nachrichten.mp4") for s in srcs)


def test_library_from_dir(tmp_path):
    """library_from_dir liest Video-Dateien; nicht-Video wird ignoriert."""
    (tmp_path / "ferienwohnung_balkon.mp4").write_bytes(b"x")
    (tmp_path / "notes.txt").write_text("kein video", encoding="utf-8")
    clips = B.library_from_dir(tmp_path)
    assert len(clips) == 1 and clips[0].src.endswith("ferienwohnung_balkon.mp4")
    # nicht existierendes Verzeichnis -> leere Liste (kein Crash)
    assert B.library_from_dir(tmp_path / "fehlt") == []
