"""creative-studio — Content-Analyse-Stufe (SKILL-061).

Loest den zweiten Teil der Critique 2026-06-25 ("gar kein Verstaendnis, was wir
dort machen"): aus dem **echten Transkript** (transcribe.py, SKILL-060) wird eine
**maschinell erzeugte Reel-Spec** statt einer handgeschriebenen — mit redaktioneller
Auswahl der staerksten Aussage, Hook, Narrativ (Hook -> Insight/Value -> CTA) und
Betonungs-Keywords, die zum tatsaechlich Gesprochenen passen.

> [!important] Architektur: Die "Intelligenz" ist Claude selbst.
> Wie bei `ad_library.py` (MCP-Call beim Agent) macht **dieses Modul KEINEN
> LLM-Call**. Der Skill wird von Claude ausgefuehrt — Claude IST der
> Redaktions-Pass. Dieses Modul liefert:
>   1. `build_analysis_prompt(transcript)` — das exakte Briefing, das Claude
>      ueber dem Transkript abarbeitet (Segment-Wahl, Hook, Script, Keywords).
>   2. `EditorialDecision` + `parse_editorial_decision()` — Schema + Validierung
>      von Claudes JSON-Antwort (kein stilles leeres Reel).
>   3. `decision_to_spec()` — baut aus Transkript + Decision die fertige
>      Reel-Spec (reel_spec.py-kompatibel), inkl. word-level Captions, die aus
>      dem GEWAEHLTEN Segment des echten Transkripts geschnitten + relativ auf 0
>      genullt sind, und `keyword:true` auf den vom Redaktions-Pass betonten
>      Woertern.
> So ist das Modul gegen gespeicherte Beispiel-Transkripte/-Decisions
> unit-testbar (ohne Live-LLM).

Best-Practice-Grundlage (2026): Hook -> Body/Value -> CTA, 20-45 s Sweet Spot,
EIN betontes Keyword pro Phrase, Captions = echtes Wort. Quellen:
AgentischesArbeiten/docs/marketing/research/2026-06-25_content-aware-reel-pipeline.md.

Multi-Projekt: KEIN projekt-spezifischer Wert. Brand kommt als Parameter.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

# Sweet-Spot-Fenster (Best Practice 2026); content_type_warnings(specs.py)
# bleibt der Validator fuer talking_head — hier nur als Briefing-Hinweis.
TARGET_MIN_SECONDS = 12.0
TARGET_MAX_SECONDS = 45.0

# === SKILL-065: Editorial-/Struktur-Regeln (Konstanten, EARS-4 multi-projekt) ===
# Schwellen als benannte Konstanten — kein Projektwert. Laengen-/Hook-Fenster-
# Pruefung delegiert content_structure_warnings() an specs.content_type_warnings()
# (kein Doppel, EARS-3); HIER nur die redaktionellen Zusatz-Regeln.

# Hook-Promise muss im ersten Fenster stehen (DISC-rot: Ergebnis/Zahl zuerst).
HOOK_WINDOW_SECONDS = 3.0
# Best-Practice-Sweetspot fuer das Segment (Fallback, wenn kein ContentType uebergeben).
STRUCTURE_MIN_SECONDS = TARGET_MIN_SECONDS
STRUCTURE_MAX_SECONDS = TARGET_MAX_SECONDS
# Caption-Last/Pacing: zu viele markierte Keywords -> Dauer-Highlight statt EIN
# Akzent pro Sinn-Phrase. Heuristik: max. ~1 Keyword je 4 Caption-Tokens.
KEYWORD_TOKENS_PER_KEYWORD = 4
# Frage-Floskel-Heuristik fuer den Hook (DISC-rot: keine Frage als Einstieg).
_HOOK_QUESTION_OPENERS = (
    "hast du", "kennst du", "wusstest du", "willst du", "moechtest du",
    "weisst du", "warum", "wieso", "wie oft", "was waere", "schon mal",
)


def _has_number(text: str) -> bool:
    """True, wenn `text` mindestens eine Ziffer enthaelt (Ergebnis/Zahl-Heuristik)."""
    return any(ch.isdigit() for ch in text or "")


class ContentAnalysisError(ValueError):
    """SKILL-061: ungueltige/unvollstaendige Redaktions-Decision (kein Silent-Fake)."""


# --------------------------------------------------------------------------- #
# 1) Analyse-Prompt fuer Claude (der Redaktions-Pass)                          #
# --------------------------------------------------------------------------- #
def build_analysis_prompt(transcript: dict[str, Any], *, brand_context: str = "") -> str:
    """Baut das Briefing, das Claude ueber dem Transkript abarbeitet.

    Erwartet ein Transkript-Dict (transcribe.Transcript.to_dict()). Gibt einen
    String-Prompt zurueck, dessen Antwort Claude als JSON liefern soll
    (EditorialDecision-Schema, siehe parse_editorial_decision()).
    """
    words = transcript.get("words", [])
    # Wort-Index mit Timing als Referenz fuer die Segment-Auswahl.
    indexed = "\n".join(
        f"  [{i}] {w['startMs']}-{w['endMs']}ms  {w['text']}"
        for i, w in enumerate(words)
    )
    ctx = f"\nBRAND-/PROJEKT-KONTEXT:\n{brand_context}\n" if brand_context.strip() else ""
    return f"""Du bist Redakteur fuer Short-Form-Reels (9:16, B2B, DISC-rot: Ergebnis/Zahl zuerst,
kein Geschwafel, ein klarer CTA). Unten ein WORT-GENAUES Transkript des tatsaechlich
gesprochenen Clips (Index, Start-/End-Millisekunden, Wort).
{ctx}
VOLLTEXT: {transcript.get('full_text','')}

WORT-INDEX:
{indexed}

AUFGABE — gib NUR ein JSON-Objekt zurueck (kein Prosatext) mit Feldern:
{{
  "segment": {{"start_word": <int>, "end_word": <int>}},   // staerkste {int(TARGET_MIN_SECONDS)}-{int(TARGET_MAX_SECONDS)}s, Indizes aus WORT-INDEX (inkl.)
  "hook": "<kurzer scroll-stoppender Hook, Zahl/Ergebnis zuerst, <= 60 Zeichen>",
  "hook_accent": "<Teil des Hooks fuer die Akzentfarbe, oder \\"\\">",
  "narrative": {{                                           // Hook -> Insight/Value -> CTA
    "insight": "<die eine Kern-Aussage des Segments, 1 Satz>",
    "cta": "<eine konkrete naechste Handlung>"
  }},
  "keyword_words": [<int>, ...],   // Indizes (aus WORT-INDEX) der zu BETONENDEN Woerter — GENAU EIN Keyword je Sinn-Phrase, nicht jedes Wort
  "eyebrow": "<optional kurze Kategorie, oder \\"\\">",
  "subline": "<optional 1 Zeile, oder \\"\\">"
}}

REGELN:
- segment: nur Indizes, die im WORT-INDEX existieren; start_word <= end_word.
- Captions kommen spaeter AUS DIESEM Segment (echtes Wort) — erfinde KEINE Caption-Texte.
- keyword_words: sparsam, ein Akzent pro Phrase (Zahlen/Ergebnis bevorzugt).
- Hook DISC-rot: Ergebnis/Zahl/These zuerst, keine Frage-Floskel.
"""


# --------------------------------------------------------------------------- #
# 2) Schema + Validierung von Claudes Antwort                                 #
# --------------------------------------------------------------------------- #
@dataclass
class EditorialDecision:
    start_word: int
    end_word: int
    hook: str
    hook_accent: str = ""
    insight: str = ""
    cta: str = ""
    keyword_words: list[int] = field(default_factory=list)
    eyebrow: str = ""
    subline: str = ""


def parse_editorial_decision(data: dict[str, Any] | str) -> EditorialDecision:
    """Validiert Claudes JSON-Antwort zu einer EditorialDecision.

    Akzeptiert ein Dict oder einen JSON-String (auch mit umschliessendem Text /
    ```json-Fences — robustes Extrahieren des ersten {...}-Blocks).
    """
    if isinstance(data, str):
        data = _extract_json_object(data)
    if not isinstance(data, dict):
        raise ContentAnalysisError("Redaktions-Decision muss ein JSON-Objekt sein.")

    seg = data.get("segment") or {}
    if not isinstance(seg, dict) or "start_word" not in seg or "end_word" not in seg:
        raise ContentAnalysisError(
            "Decision: 'segment.start_word'/'segment.end_word' (Wort-Indizes) sind Pflicht."
        )
    hook = str(data.get("hook", "")).strip()
    if not hook:
        raise ContentAnalysisError("Decision: 'hook' ist Pflicht (kein leerer Hook).")

    narrative = data.get("narrative") or {}
    keyword_words = [int(i) for i in (data.get("keyword_words") or [])]

    return EditorialDecision(
        start_word=int(seg["start_word"]),
        end_word=int(seg["end_word"]),
        hook=hook,
        hook_accent=str(data.get("hook_accent", "")).strip(),
        insight=str(narrative.get("insight", "")).strip(),
        cta=str(narrative.get("cta", "")).strip(),
        keyword_words=keyword_words,
        eyebrow=str(data.get("eyebrow", "")).strip(),
        subline=str(data.get("subline", "")).strip(),
    )


def _extract_json_object(text: str) -> dict[str, Any]:
    """Holt das erste balancierte {...}-JSON-Objekt aus einem (ggf. umrahmten) String."""
    # ```json ... ``` Fence zuerst entfernen, sonst ersten {..} balancieren.
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fence.group(1) if fence else None
    if candidate is None:
        start = text.find("{")
        if start < 0:
            raise ContentAnalysisError("Keine JSON-Struktur in der Antwort gefunden.")
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start : i + 1]
                    break
        if candidate is None:
            raise ContentAnalysisError("Unbalancierte JSON-Struktur in der Antwort.")
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise ContentAnalysisError(f"Antwort ist kein gueltiges JSON: {exc}") from exc


# --------------------------------------------------------------------------- #
# 3) Decision + Transkript -> fertige Reel-Spec                               #
# --------------------------------------------------------------------------- #
def decision_to_spec(
    transcript: dict[str, Any],
    decision: EditorialDecision,
    *,
    ad_id: str,
    brand: dict[str, Any],
    caption_style: str = "hormozi",
    speaker: dict[str, Any] | None = None,
    content_type: str | None = None,
) -> dict[str, Any]:
    """Baut die maschinelle Reel-Spec (reel_spec.py-kompatibel).

    - Captions werden AUS DEM GEWAEHLTEN SEGMENT des echten Transkripts
      geschnitten und relativ auf 0 ms genullt (Render startet bei 0).
    - `keyword:true` wird auf die vom Redaktions-Pass betonten Woerter gesetzt
      (Index relativ zum Segment-Start) -> der SKILL-055-Caption-Renderer
      bevorzugt explizit markierte Keywords vor seiner Heuristik.
    - Brand kommt als Parameter (multi-projekt).
    """
    words = transcript.get("words", [])
    n = len(words)
    if n == 0:
        raise ContentAnalysisError("Transkript hat keine Woerter — keine Spec moeglich.")

    s = max(0, min(decision.start_word, n - 1))
    e = max(s, min(decision.end_word, n - 1))
    seg_words = words[s : e + 1]
    if not seg_words:
        raise ContentAnalysisError("Gewaehltes Segment ist leer.")

    base_ms = int(seg_words[0]["startMs"])
    keyword_set = {k - s for k in decision.keyword_words if s <= k <= e}

    captions: list[dict[str, Any]] = []
    for local_idx, w in enumerate(seg_words):
        tok: dict[str, Any] = {
            "text": str(w["text"]),
            "startMs": int(w["startMs"]) - base_ms,
            "endMs": int(w["endMs"]) - base_ms,
        }
        if local_idx in keyword_set:
            tok["keyword"] = True
        captions.append(tok)

    spec: dict[str, Any] = {
        "ad_id": ad_id,
        "framework": "hook",
        "hook": decision.hook,
        "hook_accent": decision.hook_accent,
        "eyebrow": decision.eyebrow,
        "subline": decision.subline or decision.insight,
        "cta": decision.cta,
        "caption_style": caption_style,
        "captions": captions,
        "brand": brand,
    }
    if speaker:
        spec["speaker"] = speaker
    if content_type:
        spec["content_type"] = content_type
    return spec


# --------------------------------------------------------------------------- #
# 4) SKILL-065: Editorial-/Struktur-Validator (Hook -> Insight/Value -> CTA)   #
# --------------------------------------------------------------------------- #
def content_structure_warnings(
    spec: dict[str, Any],
    *,
    ct: Any | None = None,
) -> list[str]:
    """SKILL-065: prueft eine maschinelle Reel-Spec gegen Editorial-Best-Practice.

    Reine WARNUNGEN (keine Exceptions, kein Blocker — EARS-3): der Render bleibt
    moeglich, Mensch/Claude entscheidet. Editorial ist Geschmack -> Warnung reicht.

    Geprueft wird (EARS-1):
      (a) Segment-Laenge ausserhalb des Sweetspots — delegiert an
          specs.content_type_warnings(), wenn ein ContentType `ct` uebergeben ist
          (kein Doppel, EARS-3); sonst Fallback gegen STRUCTURE_MIN/MAX_SECONDS.
      (b) fehlender CTA (Narrativ unvollstaendig: Hook -> Insight/Value -> CTA).
      (c) fehlender Insight/Value-Teil (subline ODER insight muss Substanz haben).
      (d) Hook nicht im ersten Fenster bzw. ohne Zahl/Ergebnis / als Frage-Floskel
          (DISC-rot: Ergebnis/Zahl zuerst, keine Frage als Einstieg).
      (e) Caption-Last: zu viele markierte Keywords (Dauer-Highlight statt EIN
          Akzent pro Sinn-Phrase).

    Haelt die Spec alle Regeln ein, ist die Liste leer (EARS-2: kein Fehlalarm).

    `spec` ist das decision_to_spec()-Dict (oder ein kompatibles Reel-Spec-Dict).
    Schwellen kommen aus Modul-Konstanten (EARS-4: multi-projekt, kein Projektwert).
    """
    out: list[str] = []
    captions = spec.get("captions") or []

    # --- Segment-Laenge ----------------------------------------------------
    seconds = _spec_seconds(spec)
    if seconds is not None:
        if ct is not None:
            # EARS-3: Laengen-/Hook-Fenster an den Bestand delegieren (kein Doppel).
            from .specs import content_type_warnings
            out.extend(content_type_warnings(ct, seconds=seconds))
        else:
            if seconds < STRUCTURE_MIN_SECONDS or seconds > STRUCTURE_MAX_SECONDS:
                out.append(
                    f"Struktur-Warnung (Laenge): Segment {seconds:.1f}s ausserhalb des "
                    f"Sweetspots {STRUCTURE_MIN_SECONDS:.0f}-{STRUCTURE_MAX_SECONDS:.0f}s. "
                    "Completion-Rate ist Ranking-Faktor — straffen/erweitern."
                )

    # --- CTA vorhanden (Narrativ-Vollstaendigkeit) -------------------------
    if not str(spec.get("cta", "")).strip():
        out.append(
            "Struktur-Warnung (CTA): kein CTA gesetzt — das Narrativ Hook -> Insight "
            "-> CTA endet ohne naechste Handlung. Eine konkrete Handlung am Ende ergaenzen."
        )

    # --- Insight/Value-Teil vorhanden --------------------------------------
    if not (str(spec.get("subline", "")).strip()):
        out.append(
            "Struktur-Warnung (Value): kein Insight/Value-Teil (subline leer) — der "
            "Body soll einen such-/save-baren Mehrwert liefern, nicht nur Hook + CTA."
        )

    # --- Hook-Tonalitaet (DISC-rot) ----------------------------------------
    hook = str(spec.get("hook", "")).strip()
    if hook:
        low = hook.lower()
        is_question = hook.endswith("?") or any(low.startswith(o) for o in _HOOK_QUESTION_OPENERS)
        if is_question:
            out.append(
                "Struktur-Warnung (Hook-Tonalitaet): Hook ist eine Frage-Floskel — "
                "DISC-rot will Ergebnis/Zahl/These zuerst, keine Frage als Einstieg."
            )
        elif not _has_number(hook):
            out.append(
                "Struktur-Warnung (Hook-Substanz): Hook ohne Zahl/Ergebnis — der "
                "scroll-stoppendste Einstieg nennt eine konkrete Zahl/ein Ergebnis zuerst."
            )

    # --- Caption-Last / Keyword-Sparsamkeit --------------------------------
    if captions:
        kw_count = sum(1 for c in captions if c.get("keyword"))
        allowed = max(1, len(captions) // KEYWORD_TOKENS_PER_KEYWORD)
        if kw_count > allowed:
            out.append(
                f"Struktur-Warnung (Keyword-Last): {kw_count} betonte Keywords auf "
                f"{len(captions)} Tokens (Richtwert <= {allowed}). EIN Akzent pro "
                "Sinn-Phrase statt Dauer-Highlight — sonst verpufft die Betonung."
            )

    return out


def _spec_seconds(spec: dict[str, Any]) -> float | None:
    """Leitet die Segment-Laenge (Sekunden) aus den Caption-Timings ab.

    Captions sind auf 0 ms genullt (decision_to_spec); die Laenge ist das groesste
    endMs. Ohne Captions -> None (Laengen-Check wird uebersprungen).
    """
    captions = spec.get("captions") or []
    if not captions:
        return None
    last = max(int(c.get("endMs", 0)) for c in captions)
    return last / 1000.0 if last > 0 else None
