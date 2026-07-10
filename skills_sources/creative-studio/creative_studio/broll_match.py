"""creative-studio — B-Roll-zu-Transkript-Matching (SKILL-063, v1 keyword-basiert).

Loest den dritten Teil der Critique 2026-06-25 ("kein Matching von B-Roll zum
Gesagten"): heute fuellt nichts das `broll[]`-Feld der Reel-Spec INHALTLICH — die
Clips waeren beliebig. Diese Stufe bindet B-Roll-Positionen an die tatsaechlich
GESPROCHENEN Aussagen, indem sie pro Segment-/Keyword-Phrase den best-passenden
Clip aus einer B-Roll-Bibliothek via Token-Overlap waehlt.

> [!important] Architektur: Tier-0 = reiner Keyword-/Token-Overlap (kein Modell).
> v1 nutzt KEIN Embedding und KEINEN API-Call (Should-Ausbau SKILL-063 EARS-3:
> Embedding-Aehnlichkeit spaeter). Score = Anzahl gemeinsamer (lowercase,
> stop-word-bereinigter) Tokens zwischen Cue-Phrase und Clip-Tags/-Beschreibung.
> Bei Score 0 bleibt die Position LEER (Talking-Head-/Title-Card-Fallback) statt
> einen unpassenden Clip zu erzwingen — kein Silent-Fake (EARS-2).

Tag-/Manifest-Konvention (multi-projekt, EARS-4 — kein Projektwert hartkodiert):
    Die B-Roll-Bibliothek ist eine Liste von Clips. Jeder Clip:
        {
          "src": "broll/ferienwohnung_balkon.mp4",   # Pflicht — Datei-Ref
          "tags": ["ferienwohnung", "balkon", "aussicht"],  # optional — kuratierte Tags
          "description": "Drohnenflug ueber Ferienwohnung",  # optional — Freitext
          "seconds": 2.5                              # optional — Default-Einblenddauer
        }
    Fehlen `tags`, werden Tokens aus `src` (Dateiname ohne Endung/Pfad) +
    `description` als implizite Tags genutzt. So funktioniert das Matching auch
    gegen ein blosses Verzeichnis (Dateinamen als Tag-Quelle).

Cue-Konvention: Ein Cue ist eine gesprochene Phrase + Einblende-Sekunde:
    {"phrase": "150 Nachrichten", "seconds": 2.5}
`build_broll_cues()` leitet die Cues aus dem gewaehlten Segment + den
Redaktions-Keywords (content.EditorialDecision) ab — eine Cue pro Keyword-Phrase.

Output von `match_broll()`: B-Roll-Liste im Reel-Spec-Schema `[{src, seconds}]`,
direkt in das `broll`-Feld der Spec (reel_spec.BrollClipSpec) einsetzbar.
"""
from __future__ import annotations

import pathlib
import re
from dataclasses import dataclass, field
from typing import Any

# Default-Einblenddauer einer B-Roll-Position (Sekunden), wenn weder Cue noch
# Clip eine Dauer vorgibt. Bewusst projektneutral.
DEFAULT_BROLL_SECONDS = 2.5

# Projektneutrale DE/EN-Stoppwoerter fuer das Token-Overlap (analog
# specs._MATCH_STOPWORDS — hier lokal gehalten, da broll_match eigenstaendig
# nutzbar sein soll). Tokens < 3 Zeichen werden ohnehin verworfen.
_STOPWORDS = frozenset({
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer",
    "und", "oder", "aber", "mit", "ohne", "fuer", "auf", "aus", "von", "vom",
    "zu", "zur", "zum", "im", "in", "an", "am", "ist", "sind", "war", "wird", "werden",
    "du", "dein", "deine", "sie", "ihr", "ihre", "wir", "uns", "unser", "man",
    "wie", "was", "wer", "wo", "auch", "noch", "nur", "schon", "jetzt", "mehr", "sehr",
    "the", "and", "for", "with", "your", "you", "this", "that",
})

_TOKEN_RE = re.compile(r"[a-z0-9äöüß]+", re.IGNORECASE)

# Leichtgewichtiges DE-Stemming (kein NLP-Dependency): haeufige Flexions-/Plural-
# Endungen abschneiden, damit "Ferienwohnungen" und "Ferienwohnung" matchen
# (Tag-Singular vs. gesprochener Plural). Reihenfolge = laengste Endung zuerst.
# Nur auf Tokens >= STEM_MIN_LEN angewandt (sonst frisst es kurze Stems auf).
_DE_SUFFIXES = ("nen", "en", "er", "es", "em", "s", "n", "e")
STEM_MIN_LEN = 5


def _stem(tok: str) -> str:
    """Schneidet eine haeufige DE-Flexions-/Plural-Endung ab (rein heuristisch).

    Bewusst simpel (kein Snowball/NLTK): deckt Singular/Plural-Drift ab, der
    keyword-basiertes Matching in DE sonst bruechig macht. Numerische Tokens und
    sehr kurze Tokens bleiben unveraendert.
    """
    if tok.isdigit() or len(tok) < STEM_MIN_LEN:
        return tok
    for suf in _DE_SUFFIXES:
        if tok.endswith(suf) and len(tok) - len(suf) >= 3:
            return tok[: -len(suf)]
    return tok


def _tokens(text: str) -> set[str]:
    """Tokenisiert `text` zu lowercase-, gestemmten Tokens (>= 3 Zeichen, ohne Stoppw.).

    Zahlen bleiben erhalten (z.B. "150", "16") — sie sind oft der staerkste
    Match-Anker (DISC-rot: Zahl zuerst). Das leichte DE-Stemming (_stem) gleicht
    Singular/Plural-Drift zwischen Tag und gesprochenem Wort aus.
    """
    out: set[str] = set()
    for tok in _TOKEN_RE.findall((text or "").lower()):
        if len(tok) >= 3 and tok not in _STOPWORDS:
            out.add(_stem(tok))
    return out


@dataclass
class BrollClip:
    """Ein B-Roll-Clip aus der Bibliothek (Manifest-Eintrag oder Verzeichnis-Datei).

    `effective_tags` faellt auf Tokens aus Dateiname + Beschreibung zurueck, wenn
    keine kuratierten Tags gepflegt sind — so matcht auch ein blosses Verzeichnis.
    """
    src: str
    tags: list[str] = field(default_factory=list)
    description: str = ""
    seconds: float | None = None

    def effective_tags(self) -> set[str]:
        toks: set[str] = set()
        for t in self.tags:
            toks |= _tokens(t)
        toks |= _tokens(self.description)
        if not toks:
            # Fallback: Dateiname (ohne Pfad/Endung) als implizite Tag-Quelle.
            stem = pathlib.PurePath(self.src).stem
            toks |= _tokens(stem.replace("_", " ").replace("-", " "))
        return toks


@dataclass
class BrollCue:
    """Eine gesprochene Phrase, die mit einem B-Roll-Clip belegt werden soll."""
    phrase: str
    seconds: float = DEFAULT_BROLL_SECONDS


@dataclass
class BrollMatch:
    """Ergebnis eines Cue-Matches (None = kein passender Clip -> Position leer)."""
    cue: BrollCue
    clip: BrollClip | None
    score: int

    @property
    def matched(self) -> bool:
        return self.clip is not None and self.score > 0


def load_library(clips: list[dict[str, Any]]) -> list[BrollClip]:
    """Baut eine B-Roll-Bibliothek aus einer Manifest-Liste (Dicts -> BrollClip).

    `src` ist Pflicht je Eintrag; tags/description/seconds optional (EARS-4: alles
    kommt als Parameter, kein hartkodierter Projektwert).
    """
    out: list[BrollClip] = []
    for c in clips or []:
        src = str(c.get("src", "")).strip()
        if not src:
            continue
        secs = c.get("seconds")
        out.append(BrollClip(
            src=src,
            tags=[str(t) for t in (c.get("tags") or [])],
            description=str(c.get("description", "")),
            seconds=float(secs) if secs is not None else None,
        ))
    return out


def library_from_dir(
    directory: str | pathlib.Path,
    *,
    suffixes: tuple[str, ...] = (".mp4", ".mov", ".webm", ".m4v"),
) -> list[BrollClip]:
    """Baut eine Bibliothek aus einem Verzeichnis — Dateinamen als implizite Tags.

    Kein Manifest noetig: jeder Video-Datei wird ihr Dateiname (ohne Endung) als
    Tag-Quelle zugeordnet (effective_tags-Fallback). Existiert das Verzeichnis
    nicht, wird eine leere Liste geliefert (kein Crash).
    """
    base = pathlib.Path(directory)
    if not base.is_dir():
        return []
    clips: list[BrollClip] = []
    for p in sorted(base.iterdir()):
        if p.is_file() and p.suffix.lower() in suffixes:
            clips.append(BrollClip(src=str(p)))
    return clips


def build_broll_cues(
    transcript: dict[str, Any],
    decision: Any,
    *,
    default_seconds: float = DEFAULT_BROLL_SECONDS,
) -> list[BrollCue]:
    """Leitet B-Roll-Cues aus dem gewaehlten Segment + den Redaktions-Keywords ab.

    Eine Cue pro Keyword-Phrase (content.EditorialDecision.keyword_words): die
    Phrase ist das betonte Wort plus ein kleines Kontext-Fenster (Wort davor +
    danach), damit der Token-Overlap genug Substanz hat. Sind keine Keywords
    gesetzt, faellt es auf eine einzige Cue ueber den Hook zurueck (damit auch
    keyword-lose Decisions ein Visual bekommen koennen).

    Multi-projekt: liest nur das uebergebene Transkript/Decision — kein Projektwert.
    """
    words = transcript.get("words", [])
    n = len(words)
    cues: list[BrollCue] = []

    kw = [int(i) for i in getattr(decision, "keyword_words", []) or []]
    for idx in kw:
        if not (0 <= idx < n):
            continue
        lo = max(0, idx - 1)
        hi = min(n, idx + 2)
        phrase = " ".join(str(words[j]["text"]) for j in range(lo, hi))
        cues.append(BrollCue(phrase=phrase, seconds=default_seconds))

    if not cues:
        hook = str(getattr(decision, "hook", "")).strip()
        if hook:
            cues.append(BrollCue(phrase=hook, seconds=default_seconds))
    return cues


def match_cue(cue: BrollCue, library: list[BrollClip]) -> BrollMatch:
    """Matcht EINE Cue gegen die Bibliothek via Token-Overlap (hoechster Score gewinnt).

    Score = |cue_tokens ∩ clip_tokens|. Bei Gleichstand gewinnt der erste Clip
    (stabil/deterministisch). Score 0 -> kein Match (clip=None) -> Position bleibt
    leer (EARS-2: Talking-Head-Fallback, kein erzwungener Fehl-Clip).
    """
    cue_toks = _tokens(cue.phrase)
    best: BrollClip | None = None
    best_score = 0
    if cue_toks:
        for clip in library:
            score = len(cue_toks & clip.effective_tags())
            if score > best_score:
                best_score = score
                best = clip
    return BrollMatch(cue=cue, clip=best if best_score > 0 else None, score=best_score)


def match_broll(
    cues: list[BrollCue],
    library: list[BrollClip],
    *,
    allow_repeat: bool = False,
) -> list[dict[str, Any]]:
    """Matcht alle Cues und liefert die B-Roll-Liste im Reel-Spec-Schema.

    Output: `[{src, seconds}]` — direkt in das `broll`-Feld der Reel-Spec
    einsetzbar (reel_spec.BrollClipSpec-kompatibel). Cues ohne Match werden
    ueberSPRUNGEN (kein leerer/zufaelliger Eintrag — EARS-2). Die Einblende-Dauer
    kommt aus der Cue, sonst aus dem Clip, sonst DEFAULT_BROLL_SECONDS.

    `allow_repeat=False` (Default) verbraucht jeden Clip nur einmal (vermeidet
    denselben Clip mehrfach hintereinander); bei `True` darf ein Clip mehrere
    Aussagen belegen.
    """
    out: list[dict[str, Any]] = []
    used: set[str] = set()
    for cue in cues:
        pool = library if allow_repeat else [c for c in library if c.src not in used]
        m = match_cue(cue, pool)
        if not m.matched or m.clip is None:
            continue  # EARS-2: keine Position erzwingen
        secs = cue.seconds if cue.seconds else (m.clip.seconds or DEFAULT_BROLL_SECONDS)
        out.append({"src": m.clip.src, "seconds": float(secs)})
        used.add(m.clip.src)
    return out


def match_broll_for_decision(
    transcript: dict[str, Any],
    decision: Any,
    library: list[dict[str, Any]] | list[BrollClip],
    *,
    default_seconds: float = DEFAULT_BROLL_SECONDS,
    allow_repeat: bool = False,
) -> list[dict[str, Any]]:
    """Convenience: Transkript + Decision + Bibliothek -> fertige `broll[]`-Liste.

    Kombiniert build_broll_cues() + match_broll(). Die Bibliothek darf als
    Manifest-Dicts ODER als BrollClip-Liste kommen. Ergebnis ist direkt als
    `spec["broll"] = ...` setzbar (EARS-1: fuellt das broll-Feld inhaltlich).
    """
    clips = library if (library and isinstance(library[0], BrollClip)) else load_library(library)  # type: ignore[arg-type]
    cues = build_broll_cues(transcript, decision, default_seconds=default_seconds)
    return match_broll(cues, clips, allow_repeat=allow_repeat)  # type: ignore[arg-type]
