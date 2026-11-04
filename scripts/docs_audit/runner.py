"""Run the registered checks and render the report."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from pathlib import Path

from .backlog import Backlog, Triage, triage
from .checks import CHECKS, Check
from .model import AuditContext, Finding

DOCS_ROOT = Path(__file__).resolve().parents[2]
BACKLOG_PATH = Path("scripts") / "parity_backlog.json"


def run_audit(
    root: Path = DOCS_ROOT, backlog: Backlog | None = None, checks: Sequence[Check] = CHECKS
) -> Triage:
    """Run every check against ``root`` and triage the findings."""
    ctx = AuditContext(root)
    if backlog is None:
        backlog = Backlog.load(ctx.root / BACKLOG_PATH)
    findings: list[Finding] = []
    for check in checks:
        findings.extend(check.run(ctx))
    return triage(findings, backlog, (check.name for check in checks))


def render(result: Triage) -> str:
    """Human-readable report: failures first, then the known backlog summary."""
    lines: list[str] = []
    if result.new:
        lines.append(f"NEW FINDINGS ({len(result.new)}) - fix these or the audit fails:")
        lines.extend(f"  [{f.check}] {f.subject}: {f.message}" for f in result.new)
    if result.stale:
        backlog_file = BACKLOG_PATH.as_posix()
        lines.append(
            f"STALE BACKLOG ENTRIES ({len(result.stale)}) - resolved; "
            f"remove them from {backlog_file}:"
        )
        lines.extend(f"  [{check}] {subject}" for check, subject in result.stale)
    if result.unknown_checks:
        lines.append(f"UNKNOWN CHECKS IN BACKLOG ({len(result.unknown_checks)}):")
        lines.extend(f"  [{check}] {subject}" for check, subject in result.unknown_checks)
    keys = sorted({f.key for f in result.known})
    per_check = Counter(check for check, _ in keys)
    summary = ", ".join(f"{name} {count}" for name, count in sorted(per_check.items())) or "none"
    lines.append(f"Known backlog (Later Phase): {len(keys)} entries ({summary})")
    lines.append("PASS" if result.passed else "FAIL")
    return "\n".join(lines)
