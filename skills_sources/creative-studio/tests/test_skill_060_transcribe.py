"""Tests fuer die Whisper-Transkriptions-Stufe (SKILL-060).

Die reine Schema-/Mapping-Logik (WordToken -> Caption, Transcript -> dict) ist
ohne Modell/ffmpeg testbar. Der echte End-to-End-Lauf (faster-whisper) wird nur
ausgefuehrt, wenn das Paket installiert ist (sonst skip — kein Hard-Fail in CI).
"""
import importlib.util

import pytest

from creative_studio import transcribe as T


def test_wordtoken_to_caption_schema():
    """EARS: ein WordToken mappt exakt auf das Reel-Spec/Captions.tsx-Schema."""
    w = T.WordToken(text="Nachrichten", startMs=2060, endMs=2380, p=0.97)
    cap = w.to_caption()
    assert cap == {"text": "Nachrichten", "startMs": 2060, "endMs": 2380}
    assert "p" not in cap  # Konfidenz gehoert NICHT in den Render-Track


def test_transcript_to_dict_and_captions():
    """EARS: Transcript serialisiert + liefert direkt verwendbare captions[]."""
    tr = T.Transcript(
        language="de",
        lang_prob=1.0,
        full_text="Die meisten Gastgeber",
        words=[
            T.WordToken("Die", 1800, 2180, 0.63),
            T.WordToken("meisten", 2180, 2560, 1.0),
            T.WordToken("Gastgeber", 2560, 3100, 0.87),
        ],
    )
    d = tr.to_dict()
    assert d["language"] == "de"
    assert d["word_count"] == 3
    assert d["words"][0] == {"text": "Die", "startMs": 1800, "endMs": 2180, "p": 0.63}
    caps = tr.to_captions()
    assert caps == [
        {"text": "Die", "startMs": 1800, "endMs": 2180},
        {"text": "meisten", "startMs": 2180, "endMs": 2560},
        {"text": "Gastgeber", "startMs": 2560, "endMs": 3100},
    ]


def test_extract_audio_missing_video_raises():
    """EARS: fehlendes Video -> klare TranscribeError (kein Silent-Fake)."""
    with pytest.raises(T.TranscribeError):
        T.extract_audio("does_not_exist.mov", "out.wav")


def test_resolve_ffmpeg_prefers_explicit():
    """EARS: expliziter ffmpeg-Pfad hat Vorrang (multi-projekt/CI-robust)."""
    assert T._resolve_ffmpeg("/custom/ffmpeg") == "/custom/ffmpeg"


@pytest.mark.skipif(
    importlib.util.find_spec("faster_whisper") is None,
    reason="faster-whisper nicht installiert — STT-Live-Lauf uebersprungen.",
)
def test_faster_whisper_importable():
    """EARS: wenn installiert, ist das STT-Backend importierbar (Prereq-Check)."""
    from faster_whisper import WhisperModel  # noqa: F401
