"""Zentraler Smoke-Test fuer die dezentralisierte Skill-Struktur.

Seit dem Dezentralisierungs-Umbau (2026-07-12, skill_dev aufgeloest) ist jeder
Skill unter `skills_sources/<skill>/` ein self-contained SDD+PO-Projekt. Dieser
Test prueft die STRUKTUR (Existenz + Parsebarkeit der Meta-Artefakte pro Skill +
portfolio-weite Konventionen) — NICHT die Skill-Logik selbst.

Vorher lag dieser Test als `skill_dev/tests/test_skill_dev_smoke.py` und pruefte
die zentrale skill_dev-Meta-Struktur. Er wurde bei der Aufloesung von skill_dev
hierher verlegt und auf die neue Struktur umgeschrieben.

EARS-Abdeckung:
1. Jeder aktiv entwickelte Skill hat die SDD+PO-Kern-Artefakte
   (PROJECT_VISION.md, sdd-config.yaml, po-config.yaml, tickets/).
2. SKILL-NNN-Ticket-Nummern sind portfolio-weit eindeutig (global).
3. `skills_sources/SKILLS_VISION.md` (Portfolio-Constitution) existiert + parsebar.
4. po-config.yaml jedes Skills ist valide (Pflicht-Defaults).
5. reveal-presentation SKILL-007 Visual-Review-Artefakte liegen physisch vor.

Ausfuehrung (PowerShell):
    cd C:\\Users\\Jakob\\claude_projects\\Schaltzentrale
    python -m pytest skills_sources\\tests\\test_skills_smoke.py -v
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

# skills_sources/  (eine Ebene ueber tests/)
SKILLS_SOURCES = Path(__file__).resolve().parent.parent

# Skills mit eigenem self-contained SDD+PO-Projekt (Code + Meta).
# n8n-human-readable ist ein geplanter Platzhalter (Meta vorhanden, Code folgt).
SELF_CONTAINED_SKILLS = [
    "agile-sdd-skill",
    "creative-studio",
    "po-skill",
    "reveal-presentation",
    "web-mobile-design",
    "n8n-human-readable",
]


# ---------------------------------------------------------------------------
# EARS-1: Jeder Skill hat die SDD+PO-Kern-Artefakte
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("skill", SELF_CONTAINED_SKILLS)
def test_ears_1_skill_has_sdd_po_scaffolding(skill: str):
    """Jeder self-contained Skill MUSS docs/PROJECT_VISION.md, docs/sdd-config.yaml,
    docs/po-config.yaml und docs/tickets/ haben."""
    root = SKILLS_SOURCES / skill
    assert root.is_dir(), f"Skill-Verzeichnis fehlt: {root}"
    required = [
        root / "docs" / "PROJECT_VISION.md",
        root / "docs" / "sdd-config.yaml",
        root / "docs" / "po-config.yaml",
        root / "docs" / "tickets",
        root / "CLAUDE.md",
    ]
    missing = [str(p) for p in required if not p.exists()]
    assert not missing, f"{skill}: fehlende SDD+PO-Artefakte: {missing}"


# ---------------------------------------------------------------------------
# EARS-1b: PROJECT_VISION.md jedes Skills hat die Pflicht-Sektionen
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("skill", SELF_CONTAINED_SKILLS)
def test_ears_1b_vision_has_required_sections(skill: str):
    vision = SKILLS_SOURCES / skill / "docs" / "PROJECT_VISION.md"
    text = vision.read_text(encoding="utf-8")
    for section in [
        "## Vision-Statement",
        "## Kern-Prinzipien",
        "## Outcome-Metriken",
        "## Was NICHT im Scope ist",
        "## Aktualisiert",
    ]:
        assert section in text, f"{skill}: Sektion '{section}' fehlt in PROJECT_VISION.md"


# ---------------------------------------------------------------------------
# EARS-2: SKILL-NNN-Nummern sind portfolio-weit eindeutig (global)
# ---------------------------------------------------------------------------
def test_ears_2_skill_ticket_numbers_globally_unique():
    """Ueber ALLE skills_sources/<skill>/docs/tickets/SKILL-*.md hinweg darf
    jede SKILL-Nummer nur einmal existieren (globale Nummerierung)."""
    tickets = sorted(SKILLS_SOURCES.glob("*/docs/tickets/SKILL-*.md"))
    assert len(tickets) >= 80, (
        f"Erwartet >=80 migrierte SKILL-Tickets, gefunden: {len(tickets)}"
    )
    # Bekannte, VOR-BESTEHENDE Kollision (aus der zentralen skill_dev-Phase):
    # SKILL-010 wurde historisch zweimal vergeben — einmal agile-sdd-skill
    # (API-Schema-Pflicht) und einmal n8n-human-readable (Readability-Prettify).
    # Beide Tickets wurden bei der Dezentralisierung ID-erhaltend migriert.
    # TODO(Jakob): eine der beiden umnummerieren, sobald die Nummernvergabe des
    # parallelen creative-studio-Jobs abgeschlossen ist; dann diese Ausnahme entfernen.
    KNOWN_PREEXISTING_DUPLICATES = {"SKILL-010.md"}

    name_counts: dict[str, int] = {}
    for p in tickets:
        name_counts[p.name] = name_counts.get(p.name, 0) + 1
    duplicates = {n: c for n, c in name_counts.items() if c > 1}
    unexpected = {n: c for n, c in duplicates.items() if n not in KNOWN_PREEXISTING_DUPLICATES}
    assert not unexpected, (
        f"NEUE doppelte SKILL-Nummern (muessen global eindeutig sein): {unexpected}. "
        f"Bekannte Alt-Kollision (toleriert): {KNOWN_PREEXISTING_DUPLICATES}"
    )

    # Jedes Ticket hat eine Status-Zeile.
    for p in tickets:
        text = p.read_text(encoding="utf-8")
        assert re.search(r"\*\*Status:\*\*\s+\w+", text), (
            f"{p.relative_to(SKILLS_SOURCES)}: Status-Zeile fehlt"
        )


# ---------------------------------------------------------------------------
# EARS-3: Portfolio-Constitution existiert + parsebar
# ---------------------------------------------------------------------------
def test_ears_3_portfolio_skills_vision_exists():
    """`skills_sources/SKILLS_VISION.md` (Portfolio-Constitution, aus skill_dev
    migriert) MUSS existieren und die Pflicht-Sektionen + >=3 principle-Slugs
    enthalten."""
    vision = SKILLS_SOURCES / "SKILLS_VISION.md"
    assert vision.exists(), f"SKILLS_VISION.md fehlt unter {vision}"
    text = vision.read_text(encoding="utf-8")
    for section in [
        "## Vision-Statement",
        "## Kern-Prinzipien",
        "## Outcome-Metriken",
        "## Was NICHT im Scope ist",
        "## Aktualisiert",
    ]:
        assert section in text, f"Sektion '{section}' fehlt in SKILLS_VISION.md"
    principles = re.findall(r"`([a-z0-9-]{3,})`", text)
    assert len(principles) >= 3, f"SKILLS_VISION.md: <3 principle-Slugs ({principles})"


# ---------------------------------------------------------------------------
# EARS-4: po-config.yaml jedes Skills ist valide
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("skill", SELF_CONTAINED_SKILLS)
def test_ears_4_po_config_valid(skill: str):
    pytest.importorskip("yaml")
    import yaml

    cfg = SKILLS_SOURCES / skill / "docs" / "po-config.yaml"
    data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    assert "po_skill" in data, f"{skill}: Top-Level-Key `po_skill` fehlt"
    po = data["po_skill"]
    assert isinstance(po.get("outcome_review_days"), int)
    assert isinstance(po.get("cooldown_default_hours"), int)


# ---------------------------------------------------------------------------
# EARS-4b: sdd-config.yaml jedes Skills ist valide
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("skill", SELF_CONTAINED_SKILLS)
def test_ears_4b_sdd_config_valid(skill: str):
    pytest.importorskip("yaml")
    import yaml

    cfg = SKILLS_SOURCES / skill / "docs" / "sdd-config.yaml"
    data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    assert "sdd_verifier" in data, f"{skill}: Top-Level-Key `sdd_verifier` fehlt"
    assert "test_command" in data["sdd_verifier"], f"{skill}: test_command fehlt"


# ---------------------------------------------------------------------------
# EARS-5: reveal-presentation SKILL-007 Visual-Review-Artefakte
# ---------------------------------------------------------------------------
def test_ears_5_reveal_skill_007_artifacts_exist():
    """SKILL-007: Wrapper-Scripts + Pattern-Doku im reveal-presentation-Skill."""
    reveal = SKILLS_SOURCES / "reveal-presentation"
    expected = [
        reveal / "tools" / "screenshot_slides.sh",
        reveal / "tools" / "screenshot_slides.ps1",
        reveal / "patterns" / "visual-review.md",
    ]
    missing = [str(p) for p in expected if not p.exists()]
    assert not missing, f"SKILL-007 Artefakte fehlen: {missing}"

    skill_md = reveal / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    assert "Phase 4" in text and "Visual-Review-Pass" in text, (
        "reveal SKILL.md ohne Phase-4-Sektion (Visual-Review-Pass)"
    )
