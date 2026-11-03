"""Parse Markdown and HTML publications into comparable structures.

Only the facts the audit compares are extracted: headings (level and plain
text), anchor targets, link targets, visible prose and the version line.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser

TOC_TITLES = frozenset({"table of contents", "contents", "navigation matrix"})

_FENCE = re.compile(r"^\s{0,3}(```|~~~)")
_MATH_OPEN = re.compile(r"^\s{0,3}\$\$[^$]*$")
_MATH_CLOSE = re.compile(r"^\s{0,3}\$\$\s*$")
_ATX = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_MD_LINK = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\)")
_MD_VERSION = re.compile(r"\*\*Version(?::\*\*|\*\*:) `(v?[0-9][^`]*)`")
_VERSION_LINE_WINDOW = 30
_HTML_VERSION = re.compile(
    r"<span>Version:? (v?[0-9][^<]*)</span>"
    r"|<strong>Version:?</strong>:? <code>(v?[0-9][^<]*)</code>"
)
_SPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class Heading:
    """One heading: level 1-6 and normalized plain text."""

    level: int
    text: str


@dataclass
class ParsedDocument:
    """Comparable facts extracted from one publication."""

    headings: list[Heading] = field(default_factory=list)
    anchors: set[str] = field(default_factory=set)
    links: list[tuple[int, str]] = field(default_factory=list)
    words: list[str] = field(default_factory=list)
    version: str | None = None
    elements: set[str] = field(default_factory=set)


def normalize_text(text: str) -> str:
    """Collapse whitespace and unescape entities."""
    return _SPACE.sub(" ", html.unescape(text)).strip()


def strip_inline_markdown(text: str) -> str:
    """Remove inline Markdown and HTML markup, keeping code span content."""
    codes: list[str] = []

    def keep(match: re.Match[str]) -> str:
        codes.append(match.group(1))
        return f"\u0001{len(codes) - 1}\u0001"

    text = re.sub(r"`([^`]*)`", keep, text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\*\*|\*|~~", "", text)
    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|])", r"\1", text)
    return re.sub("\u0001(\\d+)\u0001", lambda m: codes[int(m.group(1))], text)


def github_slug(text: str) -> str:
    """Anchor id that GitHub and markdownlint MD051 derive from a heading."""
    slug = text.strip().lower()
    slug = re.sub(r"[^\w\- ]", "", slug, flags=re.UNICODE)
    return slug.replace(" ", "-")


def is_structural_heading(text: str) -> bool:
    """True for navigation headings and category banners that are not content."""
    lowered = text.lower()
    return lowered in TOC_TITLES or lowered.startswith("category ")


def markdown_content_lines(source: str) -> list[tuple[int, str]]:
    """Lines outside fenced code and display-math blocks, numbered from 1."""
    lines: list[tuple[int, str]] = []
    in_code = False
    in_math = False
    for number, line in enumerate(source.split("\n"), start=1):
        if not in_math and _FENCE.match(line):
            in_code = not in_code
            continue
        if not in_code:
            if not in_math and _MATH_OPEN.match(line):
                in_math = True
                continue
            if in_math and _MATH_CLOSE.match(line):
                in_math = False
                continue
        if in_code or in_math:
            continue
        lines.append((number, line))
    return lines


def parse_markdown(source: str) -> ParsedDocument:
    """Extract headings, anchors, links, words and the version line."""
    source = source.replace("\r\n", "\n")
    doc = ParsedDocument()
    seen: dict[str, int] = {}
    prose: list[str] = []
    in_toc = False
    for number, line in markdown_content_lines(source):
        heading = _ATX.match(line)
        if heading:
            text = normalize_text(strip_inline_markdown(heading.group(2)))
            doc.headings.append(Heading(len(heading.group(1)), text))
            in_toc = text.lower() in TOC_TITLES
            slug = github_slug(text)
            if slug in seen:
                seen[slug] += 1
                slug = f"{slug}-{seen[slug]}"
            else:
                seen[slug] = 0
            doc.anchors.add(slug)
        if doc.version is None and number <= _VERSION_LINE_WINDOW:
            version = _MD_VERSION.search(line)
            if version:
                doc.version = version.group(1)
        without_code = re.sub(r"`[^`]*`", "", line)
        doc.links.extend((number, m.group(1)) for m in _MD_LINK.finditer(without_code))
        if not in_toc:
            prose.append(strip_inline_markdown(line))
    doc.anchors.update(re.findall(r'<a\s+(?:id|name)="([^"]+)"', source))
    doc.words = _words(" ".join(prose))
    return doc


class _HtmlCollector(HTMLParser):
    """Collect headings, ids, link targets and visible text in one pass.

    Code blocks (``pre``) and display math (``div.math-block``) are left out
    of the prose, matching ``markdown_content_lines``, which skips fenced code
    and ``$$`` blocks in Markdown.
    """

    _HIDDEN = frozenset({"script", "style", "head", "nav", "pre"})
    _MATH_CLASS = "math-block"

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doc = ParsedDocument()
        self._heading_level: int | None = None
        self._heading_text: list[str] = []
        self._hidden_depth = 0
        self._div_hidden: list[bool] = []
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        self.doc.elements.add(tag)
        self.doc.elements.update(f"{tag}.{cls}" for cls in values.get("class", "").split())
        for name in ("id", "name"):
            if values.get(name) and (name == "id" or tag == "a"):
                self.doc.anchors.add(values[name])
        for name in ("href", "src"):
            if name in values:
                self.doc.links.append((self.getpos()[0], html.unescape(values[name])))
        if tag in self._HIDDEN:
            self._hidden_depth += 1
        if tag == "div":
            is_math = self._MATH_CLASS in values.get("class", "").split()
            self._div_hidden.append(is_math)
            if is_math:
                self._hidden_depth += 1
        if re.fullmatch(r"h[1-6]", tag):
            self._heading_level = int(tag[1])
            self._heading_text = []

    def handle_decl(self, decl: str) -> None:
        if decl.lower() == "doctype html":
            self.doc.elements.add("!doctype")

    def handle_endtag(self, tag: str) -> None:
        if tag in self._HIDDEN and self._hidden_depth:
            self._hidden_depth -= 1
        if tag == "div" and self._div_hidden:
            was_math = self._div_hidden.pop()
            if was_math and self._hidden_depth:
                self._hidden_depth -= 1
        if self._heading_level is not None and tag == f"h{self._heading_level}":
            text = normalize_text("".join(self._heading_text))
            self.doc.headings.append(Heading(self._heading_level, text))
            self._heading_level = None

    def handle_data(self, data: str) -> None:
        if self._heading_level is not None:
            self._heading_text.append(data)
        if not self._hidden_depth:
            self._text.append(data)

    def result(self) -> ParsedDocument:
        self.doc.words = _words(" ".join(self._text))
        return self.doc


def parse_html(source: str) -> ParsedDocument:
    """Extract headings, anchors, links, words and the version line."""
    collector = _HtmlCollector()
    collector.feed(source)
    collector.close()
    doc = collector.result()
    version = _HTML_VERSION.search(source)
    if version:
        doc.version = version.group(1) or version.group(2)
    return doc


def content_headings(doc: ParsedDocument) -> list[Heading]:
    """Headings without the TOC title and category banners."""
    return [h for h in doc.headings if not is_structural_heading(h.text)]


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:[.'][a-z0-9]+)*", html.unescape(text).lower())
