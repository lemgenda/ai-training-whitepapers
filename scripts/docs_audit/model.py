"""Core types shared by every audit check."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any

from .parsing import ParsedDocument, parse_html, parse_markdown

MANIFEST_PATH = Path("manifest") / "documents.json"


@dataclass(frozen=True, order=True)
class Finding:
    """One audit finding.

    ``check`` and ``subject`` form the key the parity backlog records; the
    message carries the detail for the reader.
    """

    check: str
    subject: str
    message: str

    @property
    def key(self) -> tuple[str, str]:
        return (self.check, self.subject)


@dataclass(frozen=True)
class DocumentPair:
    """One manifest entry: a Markdown source and its HTML publication."""

    doc_id: str
    md_path: str
    html_path: str
    baseline_version: str


class AuditContext:
    """Read-only view of one docs repository, with parsed files cached."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self._parsed: dict[str, ParsedDocument] = {}

    @cached_property
    def manifest(self) -> dict[str, Any]:
        return json.loads(self.read_text(MANIFEST_PATH.as_posix()))

    @cached_property
    def pairs(self) -> list[DocumentPair]:
        return [
            DocumentPair(
                doc_id=entry["id"],
                md_path=entry["md_path"],
                html_path=entry["html_path"],
                baseline_version=entry["baseline_version"],
            )
            for entry in self.manifest["documents"]
        ]

    def path(self, relative: str) -> Path:
        return self.root / relative

    def exists(self, relative: str) -> bool:
        return self.path(relative).is_file()

    def read_text(self, relative: str) -> str:
        return self.path(relative).read_text(encoding="utf-8")

    def relative(self, path: Path) -> str:
        return path.resolve().relative_to(self.root).as_posix()

    def glob(self, pattern: str) -> list[str]:
        return sorted(self.relative(p) for p in self.root.glob(pattern) if p.is_file())

    def parsed(self, relative: str) -> ParsedDocument:
        """Parse a Markdown or HTML file once per audit run."""
        if relative not in self._parsed:
            source = self.read_text(relative)
            if relative.endswith(".md"):
                self._parsed[relative] = parse_markdown(source)
            else:
                self._parsed[relative] = parse_html(source)
        return self._parsed[relative]
