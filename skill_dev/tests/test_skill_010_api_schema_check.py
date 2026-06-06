"""Smoke-Tests fuer SKILL-010 (API-Schema-Pflicht in agile-sdd-skill).

EARS-Abdeckung (SKILL-010, Teil F):
1. `templates/TICKET.md` enthaelt die Pflicht-Sektion `### API-Schema-Kontrakt`
   mit den vier Checkboxen.
2. `verifier/VERIFIER.md` enthaelt den Pflicht-Block "API-Schema-Coverage"
   (Coverage-Check ueber /openapi.json + `partial`-Regel + Folge-Ticket-Notiz).
3. `templates/IMPLEMENTER_BRIEFING_STANDARDS.md` enthaelt den Standard-Block
   "API-Schema-Mitdenken" (zur Wiederverwendung im Subagent-Briefing).

Bonus:
- `SKILL.md` referenziert IMPLEMENTER_BRIEFING_STANDARDS.md (sonst findet
  niemand die Pflicht-Bloecke).
- `operator-templates/SKILL.md` hat MCP/API-Schema-Hinweis-Block.
- Memory-File `feedback_api_schema_pflicht.md` existiert (best-effort,
  Memory-Pfad ist nutzer-spezifisch — Test wird ge-skipped wenn nicht
  vorhanden).

Ausfuehrung (PowerShell):
    cd C:\\Users\\Jakob\\claude_projects\\Schaltzentrale
    python -m pytest skill_dev\\tests\\test_skill_010_api_schema_check.py -v
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

# Repo-Root = skill_dev/  (zwei Ebenen ueber dieser Datei)
REPO_ROOT = Path(__file__).resolve().parent.parent
SCHALT_ROOT = REPO_ROOT.parent  # <Schaltzentrale>/
SKILLS_SOURCES = SCHALT_ROOT / "skills_sources"

AGILE_SDD = SKILLS_SOURCES / "agile-sdd-skill"
OPERATOR_TEMPLATES = SKILLS_SOURCES / "operator-templates"


# ---------------------------------------------------------------------------
# EARS-1: Ticket-Template enthaelt API-Schema-Kontrakt-Sektion
# ---------------------------------------------------------------------------
# SKILL-010, Teil A + Teil F Case 1
def test_ears_1_ticket_template_has_api_schema_kontrakt_section():
    """`templates/TICKET.md` MUSS eine Pflicht-Sektion
    `### API-Schema-Kontrakt` mit allen vier Checkboxen enthalten."""
    ticket_md = AGILE_SDD / "templates" / "TICKET.md"
    assert ticket_md.exists(), f"TICKET.md fehlt unter {ticket_md}"

    text = ticket_md.read_text(encoding="utf-8")

    # Akzeptiere H2 oder H3 — Ticket-Template-Konvention nutzt H2 fuer
    # Top-Level-Sektionen wie "Akzeptanzkriterien".
    assert ("## API-Schema-Kontrakt" in text) or (
        "### API-Schema-Kontrakt" in text
    ), (
        "TICKET.md fehlt die Pflicht-Sektion 'API-Schema-Kontrakt' "
        "(SKILL-010 Teil A)"
    )

    # Die vier Checkbox-Stichworte aus dem Ticket-Auftrag
    expected_keywords = [
        "Datenmodell",        # Checkbox 1
        "API-Endpoints",      # Checkbox 2
        "additiv erweitert",  # Checkbox 3 (Backwards-Kompat)
        "openapi.json",       # Checkbox 4 (OpenAPI-Schema-Check)
    ]
    for keyword in expected_keywords:
        assert keyword in text, (
            f"TICKET.md API-Schema-Kontrakt-Sektion vermisst Stichwort "
            f"'{keyword}'"
        )

    # Mindestens vier Checkboxen `- [ ]` innerhalb der Sektion
    section_start = text.find("## API-Schema-Kontrakt")
    if section_start == -1:
        section_start = text.index("### API-Schema-Kontrakt")
    # naechste H2-Sektion finden, sonst bis Ende
    rest = text[section_start:]
    next_section = rest.find("\n## ", 1)
    section = rest[: next_section if next_section != -1 else None]
    checkbox_count = section.count("- [ ]")
    assert checkbox_count >= 4, (
        f"API-Schema-Kontrakt-Sektion sollte mind. 4 Checkboxen haben, "
        f"gefunden: {checkbox_count}"
    )


# ---------------------------------------------------------------------------
# EARS-2: Verifier enthaelt "API-Schema-Coverage"-Block
# ---------------------------------------------------------------------------
# SKILL-010, Teil B + Teil F Case 2
def test_ears_2_verifier_has_api_schema_coverage_block():
    """`verifier/VERIFIER.md` MUSS einen Pflicht-Check-Block 'API-Schema-
    Coverage' enthalten (Diff-Pruefung neue Modell-Spalten, OpenAPI-
    Sichtbarkeit, `partial`-Regel + Folge-Ticket-Vorschlag)."""
    verifier_md = AGILE_SDD / "verifier" / "VERIFIER.md"
    assert verifier_md.exists(), f"VERIFIER.md fehlt unter {verifier_md}"

    text = verifier_md.read_text(encoding="utf-8")

    assert "API-Schema-Coverage" in text, (
        "VERIFIER.md fehlt der Pflicht-Block 'API-Schema-Coverage' "
        "(SKILL-010 Teil B)"
    )

    # Pflicht-Elemente im Coverage-Check
    must_contain = [
        "openapi.json",          # Coverage-Pruefung
        "additiv",               # Backwards-Kompat
        "partial",               # Status-Setzen
        "Folge-Ticket",          # Notiz-Empfehlung
        "api_endpoints_extended",  # Frontmatter-Flag
    ]
    for needle in must_contain:
        assert needle in text, (
            f"VERIFIER.md API-Schema-Coverage-Block vermisst '{needle}'"
        )


# ---------------------------------------------------------------------------
# EARS-3: Implementer-Briefing-Standards enthaelt "API-Schema-Mitdenken"
# ---------------------------------------------------------------------------
# SKILL-010, Teil C + Teil F Case 3
def test_ears_3_implementer_briefing_has_api_schema_mitdenken_block():
    """`templates/IMPLEMENTER_BRIEFING_STANDARDS.md` MUSS einen Standard-
    Block 'API-Schema-Mitdenken' enthalten, der von Operator/Lead-Claude
    an Subagent-Briefings angehaengt wird."""
    briefing_md = AGILE_SDD / "templates" / "IMPLEMENTER_BRIEFING_STANDARDS.md"
    assert briefing_md.exists(), (
        f"IMPLEMENTER_BRIEFING_STANDARDS.md fehlt unter {briefing_md} "
        "(SKILL-010 Teil C)"
    )

    text = briefing_md.read_text(encoding="utf-8")
    assert "API-Schema-Mitdenken" in text, (
        "IMPLEMENTER_BRIEFING_STANDARDS.md fehlt der Standard-Block "
        "'API-Schema-Mitdenken'"
    )

    must_contain = [
        "Backwards-Kompat",          # additive Erweiterung
        "openapi.json",              # Test-Vorgabe
        "api_endpoints_extended",    # Frontmatter-Flag
    ]
    for needle in must_contain:
        assert needle in text, (
            f"API-Schema-Mitdenken-Block vermisst '{needle}'"
        )


# ---------------------------------------------------------------------------
# Bonus: SKILL.md referenziert IMPLEMENTER_BRIEFING_STANDARDS.md
# ---------------------------------------------------------------------------
def test_bonus_skill_md_references_briefing_standards():
    """Damit der Standard-Block ueberhaupt gefunden wird, MUSS `SKILL.md`
    auf `IMPLEMENTER_BRIEFING_STANDARDS.md` verweisen."""
    skill_md = AGILE_SDD / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    assert "IMPLEMENTER_BRIEFING_STANDARDS.md" in text, (
        "SKILL.md erwaehnt das neue Briefing-Standards-File nicht — "
        "Subagent-Aufrufer finden die Pflicht-Bloecke sonst nicht."
    )


# ---------------------------------------------------------------------------
# Bonus: operator-templates SKILL.md hat MCP/API-Schema-Hinweis
# ---------------------------------------------------------------------------
def test_bonus_operator_templates_has_api_schema_hinweis():
    """`operator-templates/SKILL.md` MUSS einen 'MCP/API-Schema-Hinweis'-
    Block haben (SKILL-010 Teil D), damit Operator beim Routing auf
    Persist-Endpoints die GET-Symmetrie prueft."""
    skill_md = OPERATOR_TEMPLATES / "SKILL.md"
    if not skill_md.exists():
        pytest.skip(f"operator-templates SKILL.md nicht vorhanden: {skill_md}")

    text = skill_md.read_text(encoding="utf-8")
    assert "API-Schema-Hinweis" in text or "API-Schema" in text, (
        "operator-templates/SKILL.md fehlt der MCP/API-Schema-Hinweis-Block "
        "(SKILL-010 Teil D)"
    )


# ---------------------------------------------------------------------------
# Bonus: Memory-Eintrag feedback_api_schema_pflicht.md (best-effort)
# ---------------------------------------------------------------------------
def test_bonus_memory_feedback_exists():
    """Memory-Eintrag `feedback_api_schema_pflicht.md` sollte unter dem
    Default-Memory-Pfad liegen. Da der Pfad nutzer-spezifisch ist,
    wird der Test ge-skipped wenn das Memory-Verzeichnis nicht existiert."""
    # Default-Pfad fuer Jakobs Setup. Kann via ENV ueberschrieben werden.
    default_memory = Path(
        os.environ.get(
            "CLAUDE_MEMORY_DIR",
            os.path.expanduser(
                "~/.claude/projects/C--Users-Jakob-claude-projects/memory"
            ),
        )
    )
    if not default_memory.exists():
        pytest.skip(
            f"Memory-Verzeichnis nicht vorhanden ({default_memory}) — "
            "Test nur auf Jakobs Setup relevant."
        )

    feedback = default_memory / "feedback_api_schema_pflicht.md"
    assert feedback.exists(), (
        f"Memory-Eintrag fehlt unter {feedback} (SKILL-010 Teil E)"
    )

    text = feedback.read_text(encoding="utf-8")
    assert "api_endpoints_extended" in text, (
        "Memory-Eintrag erwaehnt das Frontmatter-Flag nicht"
    )
    assert "T103a" in text, (
        "Memory-Eintrag verweist nicht auf das Live-Beispiel T103a"
    )
