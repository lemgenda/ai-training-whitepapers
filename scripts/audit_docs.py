"""Single entry point for the documentation audit (used by pre-commit).

Usage: python scripts/audit_docs.py [--root DOCS_ROOT] [--verbose]

Paths resolve from this file, so the command works from any directory.
Exit code 0 means no new findings and no stale backlog entries.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from docs_audit import CHECKS, DOCS_ROOT, render, run_audit

DESCRIPTION = "Single entry point for the documentation audit (used by pre-commit)."


def main(argv: list[str] | None = None) -> int:
    """Run the audit, print the report and return the process exit code."""
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--root", type=Path, default=DOCS_ROOT, help="docs repository root (default: this repo)"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="also list every known backlog finding"
    )
    args = parser.parse_args(argv)

    print("Checks: " + ", ".join(check.name for check in CHECKS))
    result = run_audit(args.root)
    if args.verbose:
        for finding in result.known:
            print(f"  backlog [{finding.check}] {finding.subject}: {finding.message}")
    print(render(result))
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
