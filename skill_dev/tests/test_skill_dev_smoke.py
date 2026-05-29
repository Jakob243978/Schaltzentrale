"""Smoke-Tests fuer das Skill-Entwicklungs-Repo (TICKET-083, Teil G).

Diese Tests pruefen NUR die Existenz und Parsebarkeit der Meta-Artefakte
im Skill-Dev-Repo — nicht die Skill-Logik selbst (Skills leben unter
`<Schaltzentrale>/skills_sources/<skill>/` bzw. nach setup.ps1 unter
`~/.claude/skills/`, und werden vom Claude-Code-Harness geladen, nicht
von pytest).

EARS-Abdeckung (TICKET-083, Teil G):
1. `SKILLS_VISION.md` existiert + parsebar (alle Pflicht-Sektionen +
   >=3 principle_id-Slugs)
2. `docs/tickets/SKILL-*.md` Liste ist nicht leer (nach Migration)
3. `po-config.yaml` valid (yaml.safe_load + Pflicht-Defaults)

Ausfuehrung (PowerShell):
    cd C:\\Users\\Jakob\\claude_projects\\Immobewertung
    .venv\\Scripts\\python.exe -m pytest \\
        C:\\Users\\Jakob\\claude_projects\\Schaltzentrale\\skill_dev\\tests\\test_skill_dev_smoke.py -v
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

# Repo-Root = skill_dev/  (zwei Ebenen ueber dieser Datei)
REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
TICKETS = DOCS / "tickets"


# ---------------------------------------------------------------------------
# EARS-G-1: SKILLS_VISION.md existiert + parsebar
# ---------------------------------------------------------------------------
# TICKET-083, Teil G, Case 1
def test_ears_g1_skills_vision_md_exists_and_parsable():
    """`docs/SKILLS_VISION.md` muss existieren und alle Pflicht-Sektionen
    enthalten (Vision-Statement, Kern-Prinzipien, Outcome-Metriken,
    Was NICHT im Scope, Aktualisiert). Mind. 3 principle_id-Slugs."""
    vision = DOCS / "SKILLS_VISION.md"
    assert vision.exists(), f"SKILLS_VISION.md fehlt unter {vision}"

    text = vision.read_text(encoding="utf-8")

    required_sections = [
        "## Vision-Statement",
        "## Kern-Prinzipien",
        "## Outcome-Metriken",
        "## Was NICHT im Scope ist",
        "## Aktualisiert",
    ]
    for section in required_sections:
        assert section in text, f"Sektion '{section}' fehlt in SKILLS_VISION.md"

    # Mind. 3 principle_id (Slug-Bullet) muss vorhanden sein.
    principle_pattern = re.compile(r"`([a-z0-9-]{3,})`", re.MULTILINE)
    principles = principle_pattern.findall(text)
    assert len(principles) >= 3, (
        f"SKILLS_VISION.md sollte mind. 3 principle_id-Slugs in Backticks "
        f"haben (gefunden: {principles})"
    )


# ---------------------------------------------------------------------------
# EARS-G-2: docs/tickets/SKILL-*.md Liste ist nicht leer
# ---------------------------------------------------------------------------
# TICKET-083, Teil G, Case 2 (angepasst 2026-05-29: Sub-Struktur pro Skill)
def test_ears_g2_skill_tickets_listed():
    """Nach der Migration aus T080/T081/T082 muss `docs/tickets/` mindestens
    3 SKILL-NNN.md-Files enthalten.

    Seit 2026-05-29 liegen Tickets pro Skill in Sub-Verzeichnissen
    (`docs/tickets/<skill>/SKILL-NNN.md`), daher rekursive Suche.
    """
    assert TICKETS.exists(), f"Tickets-Ordner fehlt: {TICKETS}"

    skill_tickets = sorted(TICKETS.rglob("SKILL-*.md"))
    assert len(skill_tickets) >= 3, (
        f"Erwartet >=3 SKILL-NNN.md-Files (rekursiv) in {TICKETS}, gefunden: "
        f"{[str(p.relative_to(TICKETS)) for p in skill_tickets]}"
    )

    # Erwartete Migrations-Tickets (irgendwo im Tickets-Baum)
    expected = {"SKILL-001.md", "SKILL-002.md", "SKILL-003.md"}
    actual_names = {p.name for p in skill_tickets}
    missing = expected - actual_names
    assert not missing, f"Erwartete Tickets fehlen: {missing}"

    # Eindeutigkeit: Jede SKILL-NNN.md darf nur einmal existieren —
    # globale Nummerierung ueber alle Skill-Unterverzeichnisse hinweg
    # (Konvention aus docs/tickets/README.md).
    name_counts: dict[str, int] = {}
    for p in skill_tickets:
        name_counts[p.name] = name_counts.get(p.name, 0) + 1
    duplicates = {n: c for n, c in name_counts.items() if c > 1}
    assert not duplicates, (
        f"Doppelte SKILL-Nummern gefunden: {duplicates}. "
        f"Nummern muessen global eindeutig sein."
    )

    # Status-Zeile ist Pflicht in JEDEM SKILL-Ticket.
    # 'Migriert'-Marker nur fuer die urspruenglichen Migrations-Tickets
    # SKILL-001/002/003 (aus T080/T081/T082). Neuere SKILL-Tickets sind
    # nativ angelegt und brauchen den Marker nicht.
    for ticket in skill_tickets:
        text = ticket.read_text(encoding="utf-8")
        assert re.search(r"\*\*Status:\*\*\s+\w+", text), (
            f"{ticket.name}: Status-Zeile (**Status:** xxx) fehlt"
        )
        if ticket.name in expected:
            assert "Migriert" in text, f"{ticket.name}: 'Migriert'-Marker fehlt"


# ---------------------------------------------------------------------------
# EARS-G-2b: docs/tickets/README.md erklaert die Sub-Struktur
# ---------------------------------------------------------------------------
# Eingefuehrt 2026-05-29 mit der Tickets-Sub-Struktur-Migration.
def test_ears_g2b_tickets_readme_explains_substructure():
    """`docs/tickets/README.md` muss die Sub-Struktur-Konvention dokumentieren
    (Nummerierungs-Regel, Cross-Cutting-Pfad, Mapping)."""
    readme = TICKETS / "README.md"
    assert readme.exists(), f"docs/tickets/README.md fehlt unter {readme}"

    text = readme.read_text(encoding="utf-8").lower()
    # Pflicht-Begriffe der Konvention (case-insensitive)
    for needle in ["cross-cutting", "global", "verify/", "skill-nnn"]:
        assert needle in text, f"README.md erwaehnt '{needle}' nicht"


# ---------------------------------------------------------------------------
# EARS-G-3: po-config.yaml valid
# ---------------------------------------------------------------------------
# TICKET-083, Teil G, Case 3
def test_ears_g3_po_config_yaml_valid():
    """`docs/po-config.yaml` muss existieren + parsebar sein + die zwei
    Pflicht-Defaults `outcome_review_days` und `cooldown_default_hours`
    enthalten."""
    pytest.importorskip("yaml")
    import yaml

    cfg = DOCS / "po-config.yaml"
    assert cfg.exists(), f"po-config.yaml fehlt unter {cfg}"

    data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    assert "po_skill" in data, "Top-Level-Key `po_skill` fehlt"
    po = data["po_skill"]
    assert "outcome_review_days" in po, "outcome_review_days fehlt"
    assert "cooldown_default_hours" in po, "cooldown_default_hours fehlt"
    assert isinstance(po["outcome_review_days"], int)
    assert isinstance(po["cooldown_default_hours"], int)


# ---------------------------------------------------------------------------
# Bonus: weitere Meta-Files (DEFERRED.md, po-outcomes.md, CLAUDE.md, ROADMAP.md)
# ---------------------------------------------------------------------------
def test_bonus_meta_files_exist():
    """CLAUDE.md, CHANGELOG.md, ROADMAP.md, DEFERRED.md, po-outcomes.md,
    governance_log.md muessen alle vorhanden sein."""
    expected_files = [
        REPO_ROOT / "CLAUDE.md",
        REPO_ROOT / "CHANGELOG.md",
        REPO_ROOT / "ROADMAP.md",
        DOCS / "DEFERRED.md",
        DOCS / "po-outcomes.md",
        DOCS / "governance_log.md",
    ]
    missing = [p for p in expected_files if not p.exists()]
    assert not missing, f"Fehlende Meta-Files: {[str(p) for p in missing]}"


def test_bonus_claude_md_mentions_skill_blocks():
    """CLAUDE.md muss `## Skill: Agile SDD` + `## Skill: PO`-Bloecke + den
    Hinweis auf `skills_sources/` (Single Source of Truth) enthalten."""
    claude_md = REPO_ROOT / "CLAUDE.md"
    text = claude_md.read_text(encoding="utf-8")
    assert "## Skill: Agile SDD" in text
    assert "## Skill: PO" in text
    assert "skills_sources" in text, (
        "CLAUDE.md sollte auf skills_sources/ als Code-Pfad hinweisen"
    )
    assert "setup.ps1" in text, "CLAUDE.md sollte setup.ps1-Hinweis enthalten"


# ---------------------------------------------------------------------------
# SKILL-007: Visual-Review-Step fuer reveal-presentation
# ---------------------------------------------------------------------------
# Stellt sicher, dass nach Implementierung von SKILL-007 die 4 Artefakte
# physisch im reveal-presentation-Skill-Source liegen.
def test_skill_007_visual_review_artifacts_exist():
    """SKILL-007 Akzeptanzkriterium: Phase-4-Doku in SKILL.md, beide
    Wrapper-Scripts (.sh + .ps1) in tools/, Pattern-Doku in patterns/."""
    reveal = REPO_ROOT.parent / "skills_sources" / "reveal-presentation"
    assert reveal.exists(), f"reveal-presentation Skill-Source fehlt: {reveal}"

    expected = [
        reveal / "tools" / "screenshot_slides.sh",
        reveal / "tools" / "screenshot_slides.ps1",
        reveal / "patterns" / "visual-review.md",
    ]
    missing = [p for p in expected if not p.exists()]
    assert not missing, f"SKILL-007 Artefakte fehlen: {[str(p) for p in missing]}"

    # Phase 4 Sektion muss in SKILL.md angekommen sein
    skill_md = reveal / "SKILL.md"
    assert skill_md.exists(), f"SKILL.md fehlt: {skill_md}"
    text = skill_md.read_text(encoding="utf-8")
    assert "Phase 4" in text and "Visual-Review-Pass" in text, (
        "SKILL.md ohne Phase-4-Sektion (Visual-Review-Pass)"
    )
    assert "patterns/visual-review.md" in text, (
        "SKILL.md verlinkt nicht patterns/visual-review.md"
    )
