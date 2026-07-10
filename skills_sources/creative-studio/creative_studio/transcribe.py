"""creative-studio — Whisper-Transkriptions-Stufe (SKILL-060).

Erzeugt **word-level Captions aus dem tatsaechlich gesprochenen Wort** statt sie
hartzukodieren. Das ist der Kern-Fix gegen die Critique 2026-06-25 ("kein Bezug
zum Transkript"): bisher waren `captions` in der Reel-Spec handgeschriebene
Slogans mit erfundenen Timings — diese Stufe liest die Tonspur aus dem Footage
und transkribiert sie word-level via faster-whisper.

Pipeline (vorgelagert zum Render, SKILL-043/045):

    footage (.mov/.mp4)
        -> [A] Audio-Extraktion (16 kHz mono WAV) via gebuendeltem Remotion-ffmpeg
        -> [B] faster-whisper (word_timestamps=True)
        -> Transkript-JSON: {language, full_text, words:[{text,startMs,endMs,p}]}
        -> [C] LLM-Content-Analyse (content.py, SKILL-061) waehlt Segment + Hook
        -> Reel-Spec captions[] (reel_spec.py, SKILL-045)

Voraussetzungen (Skill-Prereqs, siehe requirements.txt / SKILL.md):
  - `faster-whisper` (pip) + ein lokales Modell (Default "small", offline gecacht)
  - ffmpeg: bevorzugt das mit `video/node_modules` gebuendelte Remotion-ffmpeg
    (kein globaler Install noetig); Fallback `ffmpeg` auf PATH.

Multi-Projekt: KEIN projekt-spezifischer Wert. Sprache/Modell/Pfade sind
Parameter. Das Modul macht NUR Audio-Extraktion + STT; die redaktionelle
Auswahl/Strukturierung ist content.py (SKILL-061) bzw. Claude.

CLI:
    python -m creative_studio.transcribe --video clip.mov --out transcript.json \
        [--language de] [--model small] [--start 0 --duration 20]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from typing import Any

# --- Konstanten (benannte, ueberschreibbare Defaults) ------------------------
DEFAULT_MODEL = "small"          # smallest viable fuer DE-Sprech-Clips, offline gecacht
DEFAULT_LANGUAGE: str | None = None  # None = Whisper-Autodetect
WHISPER_SAMPLE_RATE = 16000      # Whisper-optimale Abtastrate (16 kHz mono)

# Gebuendeltes Remotion-ffmpeg (kein globaler Install noetig). Pfad relativ zum
# Skill-Root; faellt auf `ffmpeg` (PATH) zurueck, wenn nicht vorhanden.
_BUNDLED_FFMPEG = (
    pathlib.Path(__file__).resolve().parent.parent
    / "video" / "node_modules" / "@remotion" / "compositor-win32-x64-msvc" / "ffmpeg.exe"
)


class TranscribeError(RuntimeError):
    """SKILL-060: klare Fehlermeldung statt stillem Fehlschlag (kein Silent-Fake)."""


@dataclass
class WordToken:
    """Ein transkribiertes Wort mit Audio-gebundenem Timing (ms)."""

    text: str
    startMs: int
    endMs: int
    p: float = 1.0  # Whisper-Wort-Wahrscheinlichkeit (Konfidenz)

    def to_caption(self) -> dict[str, Any]:
        """Mapping auf das Reel-Spec/Captions.tsx-Schema {text,startMs,endMs}."""
        return {"text": self.text, "startMs": self.startMs, "endMs": self.endMs}


@dataclass
class Transcript:
    """Validiertes Transkript-Ergebnis."""

    language: str
    full_text: str
    words: list[WordToken] = field(default_factory=list)
    lang_prob: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "language": self.language,
            "lang_prob": round(self.lang_prob, 3),
            "full_text": self.full_text,
            "word_count": len(self.words),
            "words": [
                {"text": w.text, "startMs": w.startMs, "endMs": w.endMs, "p": round(w.p, 3)}
                for w in self.words
            ],
        }

    def to_captions(self) -> list[dict[str, Any]]:
        """Direkt als Reel-Spec `captions[]` verwendbar (SKILL-045)."""
        return [w.to_caption() for w in self.words]


def _resolve_ffmpeg(ffmpeg: str | None = None) -> str:
    """Findet ein lauffaehiges ffmpeg: explizit > gebuendelt (Remotion) > PATH."""
    if ffmpeg:
        return ffmpeg
    if _BUNDLED_FFMPEG.exists():
        return str(_BUNDLED_FFMPEG)
    found = shutil.which("ffmpeg")
    if found:
        return found
    raise TranscribeError(
        "Kein ffmpeg gefunden. Erwartet: gebuendeltes Remotion-ffmpeg unter "
        f"{_BUNDLED_FFMPEG} (nach `cd video && npm install`) oder `ffmpeg` auf PATH."
    )


def extract_audio(
    video_path: str,
    wav_out: str,
    *,
    start: float | None = None,
    duration: float | None = None,
    ffmpeg: str | None = None,
) -> str:
    """[A] Extrahiert die Tonspur als 16 kHz mono WAV (Whisper-optimal).

    `start`/`duration` (Sekunden) schneiden optional einen Ausschnitt — fuer
    20-45-s-Reel-Fenster, ohne den ganzen Clip zu transkribieren.
    """
    src = pathlib.Path(video_path)
    if not src.exists():
        raise TranscribeError(f"Video nicht gefunden: {video_path}")
    ff = _resolve_ffmpeg(ffmpeg)
    cmd = [ff, "-y"]
    if start is not None:
        cmd += ["-ss", str(start)]
    if duration is not None:
        cmd += ["-t", str(duration)]
    cmd += [
        "-i", str(src),
        "-vn",                       # kein Video
        "-ac", "1",                  # mono
        "-ar", str(WHISPER_SAMPLE_RATE),
        "-c:a", "pcm_s16le",
        wav_out,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not pathlib.Path(wav_out).exists():
        raise TranscribeError(
            f"Audio-Extraktion fehlgeschlagen (ffmpeg exit {proc.returncode}).\n"
            f"{proc.stderr[-800:]}"
        )
    return wav_out


def transcribe_wav(
    wav_path: str,
    *,
    language: str | None = DEFAULT_LANGUAGE,
    model: str = DEFAULT_MODEL,
    compute_type: str = "int8",
    device: str = "cpu",
) -> Transcript:
    """[B] Transkribiert eine WAV word-level via faster-whisper.

    `word_timestamps=True` liefert pro Wort `start/end/probability` — Audio-
    gebundene Millisekunden (krumm), NICHT die handgesetzten Slogan-Timings von
    vorher. Genau das loest "kein Bezug zum Transkript".
    """
    try:
        from faster_whisper import WhisperModel  # lazy: kein Hard-Dep beim Import
    except ImportError as exc:  # pragma: no cover
        raise TranscribeError(
            "faster-whisper ist nicht installiert. `pip install faster-whisper` "
            "(siehe requirements.txt). Modell wird beim ersten Lauf offline gecacht."
        ) from exc

    wm = WhisperModel(model, device=device, compute_type=compute_type)
    segments, info = wm.transcribe(wav_path, language=language, word_timestamps=True)

    words: list[WordToken] = []
    seg_texts: list[str] = []
    for seg in segments:
        seg_texts.append(seg.text.strip())
        for w in (seg.words or []):
            txt = w.word.strip()
            if not txt:
                continue
            words.append(
                WordToken(
                    text=txt,
                    startMs=int(round(w.start * 1000)),
                    endMs=int(round(w.end * 1000)),
                    p=float(w.probability or 0.0),
                )
            )

    if not words:
        raise TranscribeError(
            "Transkript leer — kein gesprochenes Wort erkannt (kein Silent-Fake: "
            "lieber hart fehlschlagen als ein leeres/erfundenes Caption-Reel rendern)."
        )

    return Transcript(
        language=info.language,
        lang_prob=float(info.language_probability or 0.0),
        full_text=" ".join(t for t in seg_texts if t),
        words=words,
    )


def transcribe_video(
    video_path: str,
    *,
    language: str | None = DEFAULT_LANGUAGE,
    model: str = DEFAULT_MODEL,
    start: float | None = None,
    duration: float | None = None,
    ffmpeg: str | None = None,
) -> Transcript:
    """[A]+[B]: Footage -> Audio-Extraktion -> word-level Transkript (End-to-End)."""
    with tempfile.TemporaryDirectory() as tmp:
        wav = str(pathlib.Path(tmp) / "audio_16k.wav")
        extract_audio(
            video_path, wav, start=start, duration=duration, ffmpeg=ffmpeg
        )
        return transcribe_wav(wav, language=language, model=model)


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Footage -> word-level Transkript-JSON (creative-studio SKILL-060)."
    )
    ap.add_argument("--video", required=True, help="Pfad zum Footage (.mov/.mp4).")
    ap.add_argument("--out", help="Pfad fuer Transkript-JSON (Default: stdout).")
    ap.add_argument("--language", default=None, help="Sprachcode (z.B. 'de'); leer = Autodetect.")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"Whisper-Modell (Default {DEFAULT_MODEL}).")
    ap.add_argument("--start", type=float, default=None, help="Ausschnitt-Start (Sek).")
    ap.add_argument("--duration", type=float, default=None, help="Ausschnitt-Dauer (Sek).")
    ap.add_argument("--ffmpeg", default=None, help="ffmpeg-Pfad (Default: gebuendelt/PATH).")
    args = ap.parse_args(argv)

    tr = transcribe_video(
        args.video,
        language=args.language,
        model=args.model,
        start=args.start,
        duration=args.duration,
        ffmpeg=args.ffmpeg,
    )
    out_json = json.dumps(tr.to_dict(), ensure_ascii=False, indent=2)
    if args.out:
        pathlib.Path(args.out).write_text(out_json, encoding="utf-8")
        print(
            f"Transkript geschrieben: {args.out} "
            f"(lang={tr.language}, {len(tr.words)} Woerter)",
            file=sys.stderr,
        )
    else:
        print(out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
