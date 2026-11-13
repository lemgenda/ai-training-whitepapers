"""Parse Markdown and HTML publications into comparable structures.

Only the facts the audit compares are extracted: headings (level and plain
text), anchor targets, link targets, visible prose, the version line, the
table of contents (Markdown) or sidebar (HTML ``nav.toc-sidebar``) entries, the
level-2 sections of an HTML page and the bold labels that open top-level list
items (the rows of a master table written as a list).
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
# One ``[text](#fragment)`` entry; the text may hold one level of brackets.
_TOC_ENTRY = re.compile(r"\[((?:[^\[\]]|\[[^\]]*\])+)\]\(#([^)\s]+)\)")
TOC_SIDEBAR_CLASS = "toc-sidebar"
# A top-level (unindented) list item that opens with bold text.
_MD_LABEL_ITEM = re.compile(r"^(?:[-*+]|\d+[.)])\s+\*\*")


@dataclass(frozen=True)
class Heading:
    """One heading: level 1-6 and normalized plain text."""

    level: int
    text: str


@dataclass(frozen=True)
class TocEntry:
    """One table of contents or sidebar link: normalized text and fragment."""

    text: str
    target: str


@dataclass(frozen=True)
class SectionHeading:
    """A level-2 heading of an HTML page and the ids that can link to it.

    ``anchors`` holds the heading's own id and the id of the enclosing
    ``section``. ``has_body`` is False for a section that holds nothing but
    its heading (an end marker), which needs no sidebar link.
    """

    text: str
    anchors: frozenset[str]
    has_body: bool


@dataclass
class ParsedDocument:
    """Comparable facts extracted from one publication."""

    headings: list[Heading] = field(default_factory=list)
    anchors: set[str] = field(default_factory=set)
    links: list[tuple[int, str]] = field(default_factory=list)
    words: list[str] = field(default_factory=list)
    version: str | None = None
    elements: set[str] = field(default_factory=set)
    toc: list[TocEntry] = field(default_factory=list)
    sections: list[SectionHeading] = field(default_factory=list)
    list_labels: list[str] = field(default_factory=list)


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
    toc_lines: list[str] = []
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
        elif not heading:
            toc_lines.append(line.strip())
    doc.anchors.update(re.findall(r'<a\s+(?:id|name)="([^"]+)"', source))
    doc.toc = [
        TocEntry(normalize_text(strip_inline_markdown(m.group(1))), m.group(2))
        for m in _TOC_ENTRY.finditer(" ".join(toc_lines))
    ]
    doc.words = _words(" ".join(prose))
    doc.list_labels = markdown_list_labels(source)
    return doc


def markdown_list_labels(source: str) -> list[str]:
    """Bold labels opening top-level list items, in order.

    A label may wrap over several lines; it ends at the closing ``**``.
    Indented (nested) items, code and display math are not counted.
    """
    labels: list[str] = []
    label: str | None = None
    for _, line in markdown_content_lines(source.replace("\r\n", "\n")):
        if label is not None:
            label = f"{label} {line.strip()}"
        else:
            item = _MD_LABEL_ITEM.match(line)
            if not item:
                continue
            label = line[item.end() :]
        if "**" in label:
            labels.append(normalize_text(strip_inline_markdown(label.split("**", 1)[0])))
            label = None
    return labels


class _ListLabelCollector(HTMLParser):
    """Collect the ``strong`` text that opens each top-level ``li``.

    Lists inside navigation, code, block quotes and tables are skipped; a
    top-level Markdown list item never renders there.
    """

    _SKIPPED = frozenset({"head", "script", "style", "nav", "pre", "blockquote", "table"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.labels: list[str] = []
        self._list_depth = 0
        self._skipped_depth = 0
        self._awaiting_label = False
        self._strong_depth = 0
        self._label: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self._SKIPPED:
            self._skipped_depth += 1
        if tag in ("ul", "ol"):
            self._list_depth += 1
        elif tag == "li":
            self._awaiting_label = self._list_depth == 1 and not self._skipped_depth
        elif tag == "strong" and self._label is not None:
            self._strong_depth += 1
        elif tag == "strong" and self._awaiting_label:
            self._awaiting_label = False
            self._label = []
            self._strong_depth = 1

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIPPED and self._skipped_depth:
            self._skipped_depth -= 1
        if tag in ("ul", "ol") and self._list_depth:
            self._list_depth -= 1
        if tag == "strong" and self._label is not None:
            self._strong_depth -= 1
            if not self._strong_depth:
                self.labels.append(normalize_text("".join(self._label)))
                self._label = None

    def handle_data(self, data: str) -> None:
        if self._label is not None:
            self._label.append(data)
        elif self._awaiting_label and data.strip():
            self._awaiting_label = False


def html_list_labels(source: str) -> list[str]:
    """Bold labels opening top-level list items of a page, in order."""
    collector = _ListLabelCollector()
    collector.feed(source)
    collector.close()
    return collector.labels


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
        self._toc_depth = 0
        self._toc_link: tuple[str, list[str]] | None = None
        self._sections: list[dict[str, object]] = []

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
        self._start_toc(tag, values)
        self._start_section(tag, values)
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
        self._end_toc(tag)
        self._end_section(tag)
        if tag == "div" and self._div_hidden:
            was_math = self._div_hidden.pop()
            if was_math and self._hidden_depth:
                self._hidden_depth -= 1
        if self._heading_level is not None and tag == f"h{self._heading_level}":
            text = normalize_text("".join(self._heading_text))
            self.doc.headings.append(Heading(self._heading_level, text))
            if self._heading_level == 2 and self._sections:
                self._sections[-1].setdefault("heading", text)
            self._heading_level = None

    def handle_data(self, data: str) -> None:
        if self._heading_level is not None:
            self._heading_text.append(data)
        elif self._sections and data.strip():
            self._sections[-1]["body"] = True
        if self._toc_link is not None:
            self._toc_link[1].append(data)
        if not self._hidden_depth:
            self._text.append(data)

    def _start_toc(self, tag: str, values: dict[str, str]) -> None:
        if tag == "nav" and (
            self._toc_depth or TOC_SIDEBAR_CLASS in values.get("class", "").split()
        ):
            self._toc_depth += 1
        elif self._toc_depth and tag == "a" and values.get("href", "").startswith("#"):
            self._toc_link = (html.unescape(values["href"][1:]), [])

    def _end_toc(self, tag: str) -> None:
        if tag == "nav" and self._toc_depth:
            self._toc_depth -= 1
        elif tag == "a" and self._toc_link is not None:
            target, text = self._toc_link
            self.doc.toc.append(TocEntry(normalize_text("".join(text)), target))
            self._toc_link = None

    def _start_section(self, tag: str, values: dict[str, str]) -> None:
        if tag == "section":
            self._sections.append({"ids": {values["id"]} if values.get("id") else set()})
        elif tag == "h2" and self._sections and values.get("id"):
            ids = self._sections[-1]["ids"]
            if isinstance(ids, set):
                ids.add(values["id"])

    def _end_section(self, tag: str) -> None:
        if tag != "section" or not self._sections:
            return
        section = self._sections.pop()
        heading = section.get("heading")
        ids = section["ids"]
        if isinstance(heading, str) and isinstance(ids, set):
            self.doc.sections.append(
                SectionHeading(heading, frozenset(ids), bool(section.get("body")))
            )

    def result(self) -> ParsedDocument:
        """The collected document, with its visible words."""
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
    doc.list_labels = html_list_labels(source)
    return doc


def content_headings(doc: ParsedDocument) -> list[Heading]:
    """Headings without the TOC title and category banners."""
    return [h for h in doc.headings if not is_structural_heading(h.text)]


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:[.'][a-z0-9]+)*", html.unescape(text).lower())
