"""creative-studio — DCO-/Asset-Feed-Export-Modus (SKILL-031).

Zweiter Output-Modus neben dem Komposition-Modus (heute): Statt fertig
komponierter Creatives liefert dieser Modus die **getrennten Bausteine**
(Medien / Headlines / Primary-Texte / Descriptions / CTAs) als
`dco_bundle.json`, das ein Ads-Agent direkt in ein Meta Advantage+ /
DCO-Ad-Set kippen kann (Metas ML-Engine assembliert pro Impression die beste
Kombination). Laut Recherche -15..25 % CPA vs. Single-Ad-Testing.

Quelle: das `manifest.json` aus SKILL-023 (batch.py) — derselbe Naming-Vertrag
(variant_id/utm_content aus SKILL-024). Dieser Modus ERZEUGT KEIN Ad-Set; das
tatsaechliche Anlegen eines Asset-Feed-Creatives bei Meta ist ein separater
Schritt (Meta-MCP/SDK) und gehoert NICHT in diesen Skill (Mensch-im-Loop:
Generierung automatisch, Launch/Budget bleiben menschlich).

Meta Asset-Budgets (Advantage+ Creative, Stand 2026, siehe Wissensgrundlage
§1.2): bis 10 Medien, je 5 Headlines / Primary-Texte / Descriptions / CTAs.
Bei Ueberschreitung wird gekappt — NIE still: jede Kappung wird via log()
sichtbar gemacht (kein stilles Truncaten, keine Fakes).

ANNAHME zu den Rohtexten (wichtig, weil das Manifest sie nicht vollstaendig
fuehrt):
  Das manifest.json (SKILL-023) speichert pro Variante nur `hook` (= Headline
  ODER Eyebrow) sowie variant_id/framework/format/media/file/utm_content — es
  enthaelt KEINE getrennten Felder fuer primary_text, description oder cta.
  Deshalb:
    - headlines      werden aus den Manifest-`hook`-Werten dedupliziert.
    - primary_texts  werden NUR uebernommen, wenn das Manifest sie tatsaechlich
                     fuehrt (Feld `primary_text`/`subline`/`body`) — sonst leer
                     gelassen (kein erfundener Text).
    - descriptions   analog (Feld `description`) — sonst leer.
    - ctas           analog (Feld `cta`) — sonst leer.
  Wer ein vollstaendiges Text-Set will, ergaenzt die Felder beim Batch-Lauf
  (oder uebergibt eine angereicherte Manifest-Variante). So bleibt das Bundle
  ehrlich: es enthaelt genau das, was vorhanden ist, und kein Platzhalter-Fake.

CLI:
    python -m creative_studio.dco --manifest <pfad> [--out dco_bundle.json]
"""
from __future__ import annotations
import argparse
import json
import pathlib
import sys

# SKILL-031: Meta Advantage+/DCO Asset-Budgets (Wissensgrundlage §1.2).
# Bewusst hier als modulweite Konstanten — projektneutral, kein Brand-/Projektwert.
MAX_MEDIAS = 10
MAX_HEADLINES = 5
MAX_PRIMARY_TEXTS = 5
MAX_DESCRIPTIONS = 5
MAX_CTAS = 5

# SKILL-031: Manifest-Feld-Aliasse je Baustein-Typ (erstes vorhandenes gewinnt).
# So funktioniert der Export auch mit angereicherten Manifesten, ohne das
# heutige (schlanke) SKILL-023-Schema zu brechen.
_HEADLINE_FIELDS = ("headline", "hook")
_PRIMARY_TEXT_FIELDS = ("primary_text", "subline", "body")
_DESCRIPTION_FIELDS = ("description", "desc")
_CTA_FIELDS = ("cta", "call_to_action")


def log(msg: str) -> None:
    """SKILL-031: einheitlicher Log-Kanal (stderr) — u.a. fuer Kappungs-Hinweise."""
    print(f"[SKILL-031] {msg}", file=sys.stderr)


def load_manifest(manifest_path: str) -> dict:
    """SKILL-031: Liest ein manifest.json (SKILL-023) und validiert die Grundform."""
    data = json.loads(pathlib.Path(manifest_path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("variants"), list):
        raise ValueError(
            f"Manifest {manifest_path} hat nicht die erwartete Form "
            "(dict mit 'variants'-Liste, SKILL-023)."
        )
    return data


def _first_field(variant: dict, fields: tuple[str, ...]) -> str:
    """SKILL-031: erstes nicht-leeres Feld aus einer Alias-Liste (sonst "")."""
    for f in fields:
        val = variant.get(f)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ""


def _dedup_preserve_order(values: list[str]) -> list[str]:
    """SKILL-031: dedupliziert eine Liste, behaelt die erste Auftritts-Reihenfolge."""
    seen: set[str] = set()
    out: list[str] = []
    for v in values:
        if v and v not in seen:
            seen.add(v)
            out.append(v)
    return out


def _cap(label: str, values: list[str], limit: int) -> list[str]:
    """SKILL-031 EARS-3: kappt auf das Meta-Limit und LOGGT die Kappung (kein stiller Cut)."""
    if len(values) > limit:
        dropped = values[limit:]
        log(
            f"Kappung {label}: {len(values)} Bausteine > Meta-Limit {limit} -> "
            f"{len(dropped)} gekappt. Verworfen: {dropped}"
        )
        return values[:limit]
    return values


def build_bundle(manifest: dict) -> dict:
    """SKILL-031: Manifest -> dco_bundle.json-Struktur (getrennte Bausteine).

    EARS-1: Bausteine getrennt (medias / headlines / primary_texts / descriptions / ctas).
    EARS-2: nach Metas Asset-Budgets gruppiert (≤10 Medien, je ≤5 Texte/CTAs).
    EARS-3: bei Ueberschreitung warnen/kappen (siehe _cap, via log()).
    EARS-4: variant_id/utm_content-Systematik (SKILL-024) als utm_mapping beibehalten.
    EARS-5: projektneutrale Struktur — Ads-Agenten beliebiger Projekte lesen dasselbe Schema.
    """
    variants = manifest.get("variants", [])

    # --- Medien deduplizieren (nur real existierende Datei-Outputs) ----------
    # Schluessel = (file, format) — geplante/fehlgeschlagene Eintraege (file=None,
    # z.B. Video-TODO oder Render-Fehler in SKILL-023) werden NICHT als Medium
    # ausgegeben (kein Fake-Asset).
    medias: list[dict] = []
    seen_media: set[tuple[str, str]] = set()
    skipped_no_file = 0
    for v in variants:
        file = v.get("file")
        if not file:
            skipped_no_file += 1
            continue
        fmt = str(v.get("format", ""))
        key = (file, fmt)
        if key in seen_media:
            continue
        seen_media.add(key)
        medias.append({
            "file": file,
            "format": fmt,
            "media": str(v.get("media", "image")),
        })
    if skipped_no_file:
        log(
            f"{skipped_no_file} Variante(n) ohne Datei-Output uebersprungen "
            "(geplant/fehlgeschlagen, kein Fake-Asset im Bundle)."
        )

    # --- Text-Bausteine ableiten + deduplizieren -----------------------------
    headlines = _dedup_preserve_order([_first_field(v, _HEADLINE_FIELDS) for v in variants])
    primary_texts = _dedup_preserve_order([_first_field(v, _PRIMARY_TEXT_FIELDS) for v in variants])
    descriptions = _dedup_preserve_order([_first_field(v, _DESCRIPTION_FIELDS) for v in variants])
    ctas = _dedup_preserve_order([_first_field(v, _CTA_FIELDS) for v in variants])

    if not primary_texts:
        log("Kein primary_text/subline/body im Manifest gefunden -> primary_texts leer "
            "(Annahme dokumentiert: SKILL-023-Manifest fuehrt diese Felder nicht).")
    if not ctas:
        log("Kein cta im Manifest gefunden -> ctas leer (keine erfundenen CTAs).")

    # --- Kappen auf Meta-Asset-Budgets (EARS-3, mit Log) ---------------------
    medias_capped = medias[:MAX_MEDIAS]
    if len(medias) > MAX_MEDIAS:
        dropped = [m["file"] for m in medias[MAX_MEDIAS:]]
        log(f"Kappung medias: {len(medias)} > Meta-Limit {MAX_MEDIAS} -> "
            f"{len(dropped)} gekappt. Verworfen: {dropped}")

    headlines = _cap("headlines", headlines, MAX_HEADLINES)
    primary_texts = _cap("primary_texts", primary_texts, MAX_PRIMARY_TEXTS)
    descriptions = _cap("descriptions", descriptions, MAX_DESCRIPTIONS)
    ctas = _cap("ctas", ctas, MAX_CTAS)

    # --- utm_mapping: Attribution erhalten (EARS-4) --------------------------
    # variant_id <-> utm_content bleibt vollstaendig erhalten (NICHT gekappt),
    # auch wenn die Bausteine gekappt wurden — sonst geht Attribution verloren.
    utm_mapping = [
        {
            "variant_id": v.get("variant_id"),
            "utm_content": v.get("utm_content"),
            "format": v.get("format"),
            "media": v.get("media"),
        }
        for v in variants
        if v.get("variant_id")
    ]

    return {
        "mode": "asset_feed",  # SKILL-031: Abgrenzung zum Komposition-Modus
        "ad_id": manifest.get("ad_id"),
        "source": "manifest.json (SKILL-023)",
        "asset_budgets": {
            "medias": MAX_MEDIAS,
            "headlines": MAX_HEADLINES,
            "primary_texts": MAX_PRIMARY_TEXTS,
            "descriptions": MAX_DESCRIPTIONS,
            "ctas": MAX_CTAS,
        },
        "medias": medias_capped,
        "headlines": headlines,
        "primary_texts": primary_texts,
        "descriptions": descriptions,
        "ctas": ctas,
        "utm_mapping": utm_mapping,
        "note": (
            "Bundle = Vorbereitung fuer Meta Advantage+/DCO-Asset-Feed. Das "
            "tatsaechliche Anlegen des Asset-Feed-Creatives erfolgt separat "
            "(Meta-MCP/SDK durch den Ads-Agent), nicht in diesem Skill."
        ),
    }


def export_bundle(manifest_path: str, out_path: str) -> dict:
    """SKILL-031: laedt Manifest, baut Bundle, schreibt dco_bundle.json. Gibt das Bundle zurueck."""
    manifest = load_manifest(manifest_path)
    bundle = build_bundle(manifest)
    out = pathlib.Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    log(
        f"dco_bundle.json geschrieben -> {out} "
        f"(medias={len(bundle['medias'])}, headlines={len(bundle['headlines'])}, "
        f"primary_texts={len(bundle['primary_texts'])}, ctas={len(bundle['ctas'])}, "
        f"utm_mapping={len(bundle['utm_mapping'])})"
    )
    return bundle


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="creative-studio DCO-/Asset-Feed-Export (SKILL-031): manifest.json -> dco_bundle.json"
    )
    ap.add_argument("--manifest", required=True, help="Pfad zur manifest.json (SKILL-023)")
    ap.add_argument("--out", default="dco_bundle.json", help="Ausgabepfad fuers dco_bundle.json")
    args = ap.parse_args(argv)

    export_bundle(args.manifest, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
