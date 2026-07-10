"""SKILL-031 — Tests fuer den DCO-/Asset-Feed-Export-Modus (dco_bundle.json).

1 EARS = mind. 1 Test. Aus einem Mini-Manifest (mehrere Varianten, geteilte
Medien) entsteht ein dco_bundle.json mit deduplizierten medias + Text-Bausteinen
+ utm_mapping; die Kappungs-Warnung greift bei Ueberschreitung der Meta-Budgets.
"""
import json

import pytest

from creative_studio import dco
from creative_studio.specs import make_utm_content, make_variant_id


def _variant(ad_id, framework, hook, fmt, hook_index, *, file=None, **extra):
    """Baut einen Manifest-Eintrag im SKILL-023-Schema (variant_id/utm_content aus SKILL-024)."""
    vid = make_variant_id(ad_id, hook, framework, fmt, hook_index=hook_index)
    entry = {
        "variant_id": vid,
        "ad_id": ad_id,
        "framework": framework,
        "hook": hook,
        "format": fmt,
        "media": "image",
        "file": file,
        "utm_content": make_utm_content(vid),
    }
    entry.update(extra)
    return entry


def _mini_manifest():
    """3 Hooks x 2 Formate; geteilte Bild-Dateien zwischen Formaten -> Dedup-Faelle."""
    ad = "h1-immo"
    hooks = [("bab", "Mehr Rendite"), ("pas", "Schluss mit Leerstand"), ("aida", "Jetzt investieren")]
    variants = []
    for i, (fw, hook) in enumerate(hooks):
        # gleiche Bilddatei je Hook in beiden Formaten? Nein — file ist je (variant,format)
        # eindeutig. Aber: zwei Varianten teilen denselben file-Namen, um Dedup zu testen.
        for fmt in ("feed_4x5", "story_9x16"):
            vid = make_variant_id(ad, hook, fw, fmt, hook_index=i)
            variants.append(_variant(ad, fw, hook, fmt, i, file=f"{vid}.png", cta="Mehr erfahren"))
    # Zwei Varianten kuenstlich auf dieselbe Datei zeigen lassen (Dedup-Probe).
    variants[1]["file"] = variants[0]["file"]
    variants[1]["format"] = variants[0]["format"]
    return {"ad_id": ad, "formats": ["feed_4x5", "story_9x16"], "media": ["image"], "variants": variants}


# EARS-1: Bausteine getrennt ausgegeben (medias / headlines / primary_texts / ctas).
def test_bundle_has_separated_blocks(tmp_path):
    mp = tmp_path / "manifest.json"
    mp.write_text(json.dumps(_mini_manifest(), ensure_ascii=False), encoding="utf-8")
    bundle = dco.export_bundle(str(mp), str(tmp_path / "dco_bundle.json"))
    for key in ("medias", "headlines", "primary_texts", "descriptions", "ctas"):
        assert key in bundle
    assert bundle["mode"] == "asset_feed"
    # headlines aus den hooks dedupliziert -> 3 verschiedene Hooks
    assert sorted(bundle["headlines"]) == sorted(["Mehr Rendite", "Schluss mit Leerstand", "Jetzt investieren"])
    # cta wurde gefuehrt -> wird uebernommen + dedupliziert
    assert bundle["ctas"] == ["Mehr erfahren"]


# EARS-2: dco_bundle.json geschrieben + nach Meta-Budgets gruppiert; medias dedupliziert.
def test_bundle_written_and_medias_deduped(tmp_path):
    mp = tmp_path / "manifest.json"
    mp.write_text(json.dumps(_mini_manifest(), ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "dco_bundle.json"
    dco.export_bundle(str(mp), str(out))
    assert out.is_file()
    data = json.loads(out.read_text(encoding="utf-8"))
    # asset_budgets vorhanden mit Meta-Limits
    assert data["asset_budgets"]["medias"] == dco.MAX_MEDIAS
    assert data["asset_budgets"]["headlines"] == dco.MAX_HEADLINES
    # 6 Varianten, aber zwei teilen (file,format) -> 5 deduplizierte medias
    files = [(m["file"], m["format"]) for m in data["medias"]]
    assert len(files) == len(set(files))  # keine Duplikate
    assert len(data["medias"]) == 5


# EARS-3: bei Ueberschreitung eines Budgets wird gekappt UND geloggt (kein stiller Cut).
def test_capping_warns_and_truncates(tmp_path, capsys):
    ad = "big"
    variants = []
    for i in range(8):  # 8 verschiedene Headlines > MAX_HEADLINES (5)
        vid = make_variant_id(ad, f"Hook {i}", "bab", "feed_4x5", hook_index=i)
        variants.append({
            "variant_id": vid, "ad_id": ad, "framework": "bab", "hook": f"Hook {i}",
            "format": "feed_4x5", "media": "image", "file": f"{vid}.png",
            "utm_content": make_utm_content(vid), "cta": "Los",
        })
    manifest = {"ad_id": ad, "variants": variants}
    mp = tmp_path / "manifest.json"
    mp.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    bundle = dco.export_bundle(str(mp), str(tmp_path / "dco_bundle.json"))
    assert len(bundle["headlines"]) == dco.MAX_HEADLINES  # gekappt auf 5
    err = capsys.readouterr().err
    assert "Kappung headlines" in err          # Kappung wurde geloggt (nicht still)
    assert "Hook 7" in err                     # konkret verworfene Bausteine genannt


# EARS-3 (media-Kappung): >10 Medien werden gekappt + geloggt.
def test_media_capping_warns(tmp_path, capsys):
    ad = "manymedia"
    variants = []
    for i in range(13):  # 13 Medien > MAX_MEDIAS (10)
        vid = make_variant_id(ad, f"H{i}", "bab", "feed_4x5", hook_index=i)
        variants.append({
            "variant_id": vid, "ad_id": ad, "framework": "bab", "hook": f"H{i}",
            "format": "feed_4x5", "media": "image", "file": f"img_{i}.png",
            "utm_content": make_utm_content(vid),
        })
    mp = tmp_path / "manifest.json"
    mp.write_text(json.dumps({"ad_id": ad, "variants": variants}, ensure_ascii=False), encoding="utf-8")
    bundle = dco.export_bundle(str(mp), str(tmp_path / "dco_bundle.json"))
    assert len(bundle["medias"]) == dco.MAX_MEDIAS
    assert "Kappung medias" in capsys.readouterr().err


# EARS-4: variant_id/utm_content-Systematik (SKILL-024) bleibt im utm_mapping erhalten.
def test_utm_mapping_preserves_attribution(tmp_path):
    mp = tmp_path / "manifest.json"
    manifest = _mini_manifest()
    mp.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    bundle = dco.export_bundle(str(mp), str(tmp_path / "dco_bundle.json"))
    # jede Variante mit variant_id ist im Mapping (auch wenn Bausteine gekappt wuerden)
    src_ids = {v["variant_id"] for v in manifest["variants"]}
    map_ids = {m["variant_id"] for m in bundle["utm_mapping"]}
    assert src_ids == map_ids
    for m in bundle["utm_mapping"]:
        assert m["utm_content"] == make_utm_content(m["variant_id"])


# EARS-1/Annahme: ohne Rohtexte werden primary_texts/ctas NICHT erfunden (kein Fake).
def test_no_fake_texts_when_absent(tmp_path, capsys):
    ad = "lean"
    # Manifest im schlanken SKILL-023-Schema OHNE cta/subline/description
    variants = []
    for i in range(2):
        vid = make_variant_id(ad, f"H{i}", "bab", "feed_4x5", hook_index=i)
        variants.append({
            "variant_id": vid, "ad_id": ad, "framework": "bab", "hook": f"H{i}",
            "format": "feed_4x5", "media": "image", "file": f"{vid}.png",
            "utm_content": make_utm_content(vid),
        })
    mp = tmp_path / "manifest.json"
    mp.write_text(json.dumps({"ad_id": ad, "variants": variants}, ensure_ascii=False), encoding="utf-8")
    bundle = dco.export_bundle(str(mp), str(tmp_path / "dco_bundle.json"))
    assert bundle["headlines"] == ["H0", "H1"]   # Hooks werden zu Headlines
    assert bundle["primary_texts"] == []          # nichts erfunden
    assert bundle["ctas"] == []                   # nichts erfunden
    err = capsys.readouterr().err
    assert "primary_texts leer" in err            # Annahme transparent geloggt


# EARS-1: geplante/fehlgeschlagene Varianten (file=None) liefern KEIN Fake-Medium.
def test_skips_entries_without_file(tmp_path, capsys):
    ad = "mixed"
    ok = make_variant_id(ad, "H0", "bab", "feed_4x5", hook_index=0)
    todo = make_variant_id(ad, "H1", "bab", "story_9x16", hook_index=1)
    variants = [
        {"variant_id": ok, "ad_id": ad, "framework": "bab", "hook": "H0", "format": "feed_4x5",
         "media": "image", "file": f"{ok}.png", "utm_content": make_utm_content(ok)},
        {"variant_id": todo, "ad_id": ad, "framework": "bab", "hook": "H1", "format": "story_9x16",
         "media": "video", "file": None, "utm_content": make_utm_content(todo),
         "status": "not_implemented"},
    ]
    mp = tmp_path / "manifest.json"
    mp.write_text(json.dumps({"ad_id": ad, "variants": variants}, ensure_ascii=False), encoding="utf-8")
    bundle = dco.export_bundle(str(mp), str(tmp_path / "dco_bundle.json"))
    assert len(bundle["medias"]) == 1             # nur das real gerenderte Bild
    # aber utm_mapping behaelt BEIDE (Attribution auch fuer geplante Varianten)
    assert len(bundle["utm_mapping"]) == 2
    assert "ohne Datei-Output uebersprungen" in capsys.readouterr().err
