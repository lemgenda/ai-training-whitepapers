"""Known parity backlog: recorded findings that do not fail the audit.

The backlog file lists, per check, the subjects (document ids or file paths)
whose drift is already known and scheduled for the Later Phase. A finding for
a listed subject is reported as backlog; any other finding fails the audit.
A listed subject with no finding left is stale and also fails the audit, so
the backlog only ever shrinks.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from .model import Finding

BACKLOG_KEY = "backlog"


@dataclass(frozen=True)
class Backlog:
    """Recorded (check, subject) keys tolerated by the audit."""

    entries: frozenset[tuple[str, str]] = field(default_factory=frozenset)

    @classmethod
    def load(cls, path: Path) -> Backlog:
        """Read the backlog file; a missing file means an empty backlog."""
        if not path.is_file():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_mapping(data[BACKLOG_KEY])

    @classmethod
    def from_mapping(cls, mapping: dict[str, list[str]]) -> Backlog:
        """Build a backlog from ``{check: [subject, ...]}``."""
        return cls(
            frozenset(
                (check, subject) for check, subjects in mapping.items() for subject in subjects
            )
        )

    def __len__(self) -> int:
        return len(self.entries)


@dataclass(frozen=True)
class Triage:
    """Findings split into new drift, recorded backlog and stale entries."""

    new: list[Finding]
    known: list[Finding]
    stale: list[tuple[str, str]]
    unknown_checks: list[tuple[str, str]]

    @property
    def passed(self) -> bool:
        """True when there is no new finding, stale entry or unknown check."""
        return not (self.new or self.stale or self.unknown_checks)


def triage(findings: Iterable[Finding], backlog: Backlog, check_names: Iterable[str]) -> Triage:
    """Split findings against the backlog."""
    names = set(check_names)
    new: list[Finding] = []
    known: list[Finding] = []
    seen: set[tuple[str, str]] = set()
    for finding in sorted(findings):
        seen.add(finding.key)
        (known if finding.key in backlog.entries else new).append(finding)
    unknown = sorted(key for key in backlog.entries if key[0] not in names)
    stale = sorted(key for key in backlog.entries if key[0] in names and key not in seen)
    return Triage(new=new, known=known, stale=stale, unknown_checks=unknown)
