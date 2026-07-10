# SKILL-034: Brand-Asset-Ordner-Konvention + Lizenz/Release-Tracking.
"""creative-studio — Brand-Asset-Registry (SKILL-034).

Projektneutrale Konvention fuer Bild-Motiv-Assets (Fotos), die Original + Web-Variante
+ Metadaten (inkl. Rechte/Release-Status) zusammenhaelt. Verhindert, dass rechtlich
ungeklaertes Material in (bezahlte) Ads fliesst, und macht Foto-Hintergruende auffindbar.

Konvention (EARS-1):
    <projekt>/marketing/brand-assets/<quelle>/
        originals/   <- verlustfrei archivierte Roh-Fotos
        web/         <- Ad-taugliche Web-Varianten (siehe SKILL-035 prep_bg.py)
        meta.json    <- Registry: je Datei Quelle/Lizenz/Release/Nutzung/Aufnahmedatum

Dies ist das **Motiv-Pendant** zu SKILL-029 (Brand-Kit ``brand.json`` = Tokens/Logo) —
hier geht es um Foto-Assets + Rechte, nicht um die Token-Schicht.

Multi-Projekt (EARS-4): der Asset-Root wird relativ zu einem ``project_root``-Parameter
aufgeloest — kein hartkodierter Pfad. Lizenz/Release sind menschlich gepflegte Felder;
das ``meta.json``-Schema bleibt bewusst klein.
"""
from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field, asdict

# SKILL-034: Erlaubte Werte (klein gehalten, menschlich pflegbar).
MODEL_RELEASE_VALUES = ("yes", "no", "unklar")
NUTZUNG_VALUES = ("organic", "paid", "beides")

# SKILL-034: Konventions-Pfade relativ zum Projekt-Root.
ASSET_ROOT_REL = ("marketing", "brand-assets")
ORIGINALS_DIRNAME = "originals"
WEB_DIRNAME = "web"
META_FILENAME = "meta.json"


@dataclass
class Asset:
    """Ein registriertes Motiv-Asset (eine Datei) mit Rechte-Status (EARS-2).

    ``dateiname`` ist der Schluessel innerhalb einer Quelle (z.B. ``00_header.jpg``).
    Lizenz/Release sind menschlich gepflegte Freitext-/Enum-Felder.
    """
    dateiname: str
    quelle: str = ""                    # z.B. "evisible | PHOTOGRAPHY"
    lizenz: str = ""                    # Freitext, z.B. "Ad-Nutzung lt. Vertrag 2025"
    model_release: str = "unklar"       # yes | no | unklar
    nutzung: str = "organic"            # organic | paid | beides
    aufnahmedatum: str = ""             # ISO-Datum, z.B. "2025-04-24"

    def normalized(self) -> "Asset":
        """Werte auf erlaubte Enums normalisieren (unbekannt -> sicherer Default)."""
        mr = self.model_release.strip().lower()
        nu = self.nutzung.strip().lower()
        return Asset(
            dateiname=self.dateiname,
            quelle=self.quelle,
            lizenz=self.lizenz,
            model_release=mr if mr in MODEL_RELEASE_VALUES else "unklar",
            nutzung=nu if nu in NUTZUNG_VALUES else "organic",
            aufnahmedatum=self.aufnahmedatum,
        )


def asset_warnings(asset: Asset, use: str = "paid") -> list[str]:
    """SKILL-034 EARS-3: Warnungen fuer eine geplante Nutzung (keine harte Sperre).

    Analog ``AdContent.warnings()``: liefert nur sichtbare Hinweise. Bei einer
    **bezahlten** Nutzung (``use='paid'``) und ``model_release != 'yes'`` wird gewarnt —
    rechtlich ungeklaertes Material darf nicht ungeprueft in Paid-Ads.
    """
    out: list[str] = []
    a = asset.normalized()
    if use == "paid" and a.model_release != "yes":
        out.append(
            f"Model-Release '{a.model_release}' fuer paid-Nutzung von '{a.dateiname}' — "
            f"Rechte/Model-Release vor bezahlter Ad schriftlich absichern."
        )
    if use == "paid" and a.nutzung == "organic":
        out.append(
            f"Asset '{a.dateiname}' ist als nutzung='organic' markiert, soll aber paid "
            f"verwendet werden — Nutzungsumfang pruefen."
        )
    if not a.lizenz.strip():
        out.append(f"Keine Lizenz-Angabe fuer '{a.dateiname}' — Herkunft/Recht dokumentieren.")
    return out


@dataclass
class AssetRegistry:
    """In-Memory-Sicht einer ``meta.json`` einer Quelle (EARS-2 Round-Trip)."""
    quelle: str
    assets: dict[str, Asset] = field(default_factory=dict)

    def add(self, asset: Asset) -> None:
        self.assets[asset.dateiname] = asset.normalized()

    def get(self, dateiname: str) -> Asset | None:
        return self.assets.get(dateiname)

    def warnings(self, use: str = "paid") -> dict[str, list[str]]:
        """Warnungen je Asset (nur Assets mit mindestens einer Warnung)."""
        out: dict[str, list[str]] = {}
        for name, asset in self.assets.items():
            w = asset_warnings(asset, use=use)
            if w:
                out[name] = w
        return out


# === Pfad-Aufloesung (EARS-1, EARS-4) ========================================

def asset_root(project_root: str | pathlib.Path) -> pathlib.Path:
    """Asset-Root ``<project_root>/marketing/brand-assets`` (EARS-4, kein Hartcode)."""
    return pathlib.Path(project_root).resolve().joinpath(*ASSET_ROOT_REL)


def source_dir(project_root: str | pathlib.Path, quelle: str) -> pathlib.Path:
    """Verzeichnis einer Quelle (``.../brand-assets/<quelle>/``)."""
    return asset_root(project_root) / quelle


def ensure_source_layout(project_root: str | pathlib.Path, quelle: str) -> pathlib.Path:
    """SKILL-034 EARS-1: Konventions-Layout anlegen (originals/, web/) + Pfad zurueck."""
    base = source_dir(project_root, quelle)
    (base / ORIGINALS_DIRNAME).mkdir(parents=True, exist_ok=True)
    (base / WEB_DIRNAME).mkdir(parents=True, exist_ok=True)
    return base


def meta_path(project_root: str | pathlib.Path, quelle: str) -> pathlib.Path:
    """Pfad der ``meta.json`` einer Quelle."""
    return source_dir(project_root, quelle) / META_FILENAME


# === meta.json lesen/schreiben (EARS-2) ======================================

def load_registry(project_root: str | pathlib.Path, quelle: str) -> AssetRegistry:
    """Liest ``meta.json`` einer Quelle in eine AssetRegistry (leere Registry, wenn fehlt)."""
    path = meta_path(project_root, quelle)
    reg = AssetRegistry(quelle=quelle)
    if not path.is_file():
        return reg
    data = json.loads(path.read_text(encoding="utf-8"))
    reg.quelle = data.get("quelle", quelle)
    for entry in data.get("assets", []):
        reg.add(Asset(
            dateiname=entry.get("dateiname", ""),
            quelle=entry.get("quelle", reg.quelle),
            lizenz=entry.get("lizenz", ""),
            model_release=entry.get("model_release", "unklar"),
            nutzung=entry.get("nutzung", "organic"),
            aufnahmedatum=entry.get("aufnahmedatum", ""),
        ))
    return reg


def save_registry(project_root: str | pathlib.Path, registry: AssetRegistry) -> pathlib.Path:
    """Schreibt eine AssetRegistry als ``meta.json`` (legt Layout an). Gibt den Pfad zurueck."""
    ensure_source_layout(project_root, registry.quelle)
    path = meta_path(project_root, registry.quelle)
    payload = {
        "quelle": registry.quelle,
        "assets": [asdict(a.normalized()) for a in registry.assets.values()],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def register_asset(project_root: str | pathlib.Path, quelle: str, asset: Asset) -> AssetRegistry:
    """Convenience: meta.json lesen, ein Asset hinzufuegen/updaten, zurueckschreiben."""
    reg = load_registry(project_root, quelle)
    reg.quelle = quelle
    reg.add(asset)
    save_registry(project_root, reg)
    return reg
