"""
Visual UI Check for the SDD Verifier (SKILL-012, Phase 1 Skeleton).

This module is the Phase-1 architecture stub for the Verifier's
"Visual UI Verification" sub-step (Schritt 6.5 in VERIFIER.md).

Phase plan:
  Phase 1 (this file)  — Skeleton, no runtime logic. Architecture frozen.
  Phase 2 (next ticket) — Full Playwright implementation + smoke run
                          against Immobewertung T097/T103.
  Phase 3 (optional)   — Visual-Regression with baseline comparison
                          (tool choice deferred — see Ticket SKILL-012).

Triggered by VERIFIER.md Schritt 6.5 when the ticket has a UI touch
(ui_verify_urls frontmatter, frontend/-Diff, or ui-classified EARS).

The Verifier MUST NOT install Playwright automatically. If the import
fails or the Chromium binary is missing, the function returns a
VisualCheckResult with status="skipped_tool_missing" and a setup hint.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


VisualCheckStatus = Literal[
    "not_required",        # no UI touch detected
    "pass",                # all URLs clean (0 console errors, 0 failed requests)
    "partial",             # mixed pass/fail across URLs
    "fail",                # all URLs failed
    "skipped_tool_missing",  # Playwright not available, no auto-install
]


@dataclass
class UrlCheck:
    """Result of a single URL screenshot + console/network capture."""

    path: str
    expect: str = ""
    screenshot_path: Path | None = None
    console_errors: list[str] = field(default_factory=list)
    failed_requests: list[str] = field(default_factory=list)
    notes: str = ""

    @property
    def passed(self) -> bool:
        return (
            self.screenshot_path is not None
            and self.screenshot_path.exists()
            and len(self.console_errors) == 0
            and len(self.failed_requests) == 0
        )


@dataclass
class VisualCheckResult:
    """Aggregated result of all URL checks for a single Verifier run."""

    status: VisualCheckStatus
    urls: list[UrlCheck] = field(default_factory=list)
    setup_hint: str = ""
    notes: str = ""

    @property
    def n_pass(self) -> int:
        return sum(1 for u in self.urls if u.passed)

    @property
    def n_fail(self) -> int:
        return sum(1 for u in self.urls if not u.passed)


def run_visual_check(
    ticket_urls: list[dict],
    output_dir: Path,
    viewport: tuple[int, int] = (1280, 800),
    nav_timeout_ms: int = 5000,
) -> VisualCheckResult:
    """
    Run headless Chromium against each URL in ticket_urls.

    Args:
        ticket_urls: List of dicts from ticket frontmatter `ui_verify_urls`.
            Each dict has at least `path: str`, optionally `expect: str`.
            Example:
                [
                  {"path": "/property/2", "expect": "Marktanalyse-Card sichtbar"},
                  {"path": "/property/287", "expect": "DDR-Empfehlung sichtbar"},
                ]
        output_dir: Directory to write screenshots to. Created if missing.
            Conventionally <verify_report_path>/screenshots/.
        viewport: (width, height) tuple. Default 1280x800 — desktop laptop.
        nav_timeout_ms: Network-idle wait timeout per URL.

    Returns:
        VisualCheckResult with per-URL details and aggregate status.

    Behavior:
        - On missing Playwright import: returns status="skipped_tool_missing"
          with setup_hint, no exception raised.
        - On missing Chromium binary: same as above.
        - On per-URL navigation timeout: that URL's notes are set,
          screenshot may still be saved as partial-render.
        - The function NEVER installs anything. Verifier-Guarantee.
    """

    # ------------------------------------------------------------------
    # TODO Phase 2: Implement Playwright integration. Stub below.
    # ------------------------------------------------------------------

    # TODO: Try to import Playwright, fall back gracefully.
    # try:
    #     from playwright.sync_api import sync_playwright
    # except ImportError:
    #     return VisualCheckResult(
    #         status="skipped_tool_missing",
    #         setup_hint=(
    #             "Playwright not available. Install via: "
    #             "pip install playwright && playwright install chromium"
    #         ),
    #     )

    # TODO: Ensure output_dir exists.
    # output_dir.mkdir(parents=True, exist_ok=True)

    # TODO: Launch headless Chromium once, iterate URLs.
    # with sync_playwright() as p:
    #     browser = p.chromium.launch(headless=True)
    #     for url_spec in ticket_urls:
    #         page = browser.new_page(viewport={"width": viewport[0],
    #                                            "height": viewport[1]})
    #         console_errors = []
    #         page.on("console", lambda msg: (
    #             console_errors.append(msg.text)
    #             if msg.type == "error" else None
    #         ))
    #         failed_requests = []
    #         page.on("response", lambda resp: (
    #             failed_requests.append(f"{resp.url} ({resp.status})")
    #             if resp.status >= 400 else None
    #         ))
    #         page.goto(url_spec["path"], wait_until="networkidle",
    #                   timeout=nav_timeout_ms)
    #         screenshot_path = output_dir / _slugify(url_spec["path"])
    #         page.screenshot(path=str(screenshot_path), full_page=True)
    #         ...

    # TODO: Aggregate per-URL pass/fail to overall status:
    #   - all URLs passed → "pass"
    #   - all URLs failed → "fail"
    #   - mixed → "partial"
    #   - no URLs → "not_required"

    return VisualCheckResult(
        status="skipped_tool_missing",
        setup_hint=(
            "SKILL-012 Phase 1 Skeleton — Playwright integration is "
            "scheduled for Phase 2 (SKILL-012b). This function is a "
            "non-functional stub. See verifier/visual_check.py header."
        ),
        notes="Phase 1 stub. Not callable in production.",
    )


def render_report_section(result: VisualCheckResult, ticket_id: str) -> str:
    """
    Render the Markdown block for the Verify-Report's
    "Visual UI Verification" section.

    Args:
        result: VisualCheckResult from run_visual_check().
        ticket_id: e.g. "TICKET-097" — used for screenshot link prefixes.

    Returns:
        Markdown string starting with `## Visual UI Verification`.

    Layout (matches templates/verify-report.md proposal in SKILL-012 Phase 1):
        ## Visual UI Verification
        **Status:** <status>
        ### Pro URL ...
        ### Aggregat ...
    """

    # ------------------------------------------------------------------
    # TODO Phase 2: Render real Markdown. Stub below returns placeholder.
    # ------------------------------------------------------------------

    lines = [
        "## Visual UI Verification",
        "",
        f"**Status:** {result.status}",
        "",
    ]

    if result.status == "skipped_tool_missing":
        lines.extend([
            f"> {result.setup_hint}",
            "",
            "> Verifier-Guarantee: kein automatisches `pip install`. "
            "Bitte manuell installieren und Verify-Pass erneut starten.",
        ])
        return "\n".join(lines)

    if result.status == "not_required":
        lines.append(
            "> n/a — kein UI-Touch im Diff, keine `ui_verify_urls` im "
            "Ticket-Frontmatter, keine UI-EARS-Saetze."
        )
        return "\n".join(lines)

    # TODO Phase 2: iterate result.urls and render each block.
    # for url_check in result.urls:
    #     lines.append(f"### URL: {url_check.path}")
    #     lines.append(f"- Screenshot: ![{url_check.path}]"
    #                  f"(screenshots/{ticket_id}-{slug}.png)")
    #     lines.append(f"- Console-Errors: {len(url_check.console_errors)}")
    #     lines.append(f"- Failed-Requests: {len(url_check.failed_requests)}")
    #     lines.append(f"- Erwartung: {url_check.expect or '-'}")
    #     lines.append(f"- Pass/Fail: {'pass' if url_check.passed else 'fail'}")
    #     lines.append("")

    lines.append("> Phase 1 stub — per-URL rendering noch nicht implementiert.")
    return "\n".join(lines)


def _slugify(path: str) -> str:
    """Convert a URL path into a safe filename slug.

    Example: "/property/2" → "property-2.png"
             "/api/v1/foo" → "api-v1-foo.png"
    """
    # TODO Phase 2: proper slugification + length cap + collision handling.
    slug = path.strip("/").replace("/", "-") or "root"
    return f"{slug}.png"
