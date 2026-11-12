"""The audit checks. Each check is one function registered in ``CHECKS``.

Add a check by writing a function that takes an ``AuditContext`` and yields
``Finding`` objects, then appending it to ``CHECKS``; the runner and the
backlog need no change.
"""

from __future__ import annotations

import difflib
import json
import posixpath
import re
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from typing import Any
from urllib.parse import unquote

import yaml

from .model import MANIFEST_PATH, AuditContext, Finding
from .parsing import TocEntry, content_headings
from .workspace import COMPONENT_SOURCES, ECOSYSTEM_PATH, TRAINING_SERVICE_ID, WorkspaceError

SIMILARITY_THRESHOLD = 0.85
TEMPLATE_ELEMENTS = (
    "!doctype",
    "html",
    "head",
    "body",
    "header",
    "nav.toc-sidebar",
    "section",
    "footer",
)
REGISTRY_FILES = ("canonical_capabilities.json", "canonical_capabilities.yaml")
# Keys of control_planes.gui.ports in the capability registry, by service id
# of ecosystem.json.
GUI_PORT_SERVICES = {
    "environment_manager_sidecar": "env-manager",
    "dataset_compiler_sidecar": "dataset-compiler",
    "training_sidecar": TRAINING_SERVICE_ID,
}
TEXT_SUFFIXES = frozenset(
    {
        ".md",
        ".html",
        ".css",
        ".js",
        ".json",
        ".yaml",
        ".yml",
        ".py",
        ".txt",
        ".toml",
        ".cfg",
        ".ini",
        ".sh",
        ".ps1",
    }
)
SKIPPED_DIRS = frozenset(
    {".git", ".pytest_cache", "__pycache__", "node_modules", ".venv", "scratch"}
)

# Drive roots, file URIs and Unix home directories. The pattern is written so
# that its own source text does not match it.
_ABSOLUTE_PATH = re.compile(
    r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]+|file:/{2}|/(?:home|Users)/", re.IGNORECASE
)
_README_VERSION = re.compile(r"^\*\*Version\*\*: `(v[0-9][^`]*)`", re.MULTILINE)
_YAML_BASELINE = re.compile(r"^document_baseline:\s*['\"]?([^'\"\s]+)", re.MULTILINE)
_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
# GitHub alert markers render only on GitHub; in a page they show as raw text.
_ALERT_MARKER = re.compile(r"\[!(?:NOTE|IMPORTANT|WARNING|TIP|CAUTION)\]")
_RELEASE_SUFFIX = "-STABLE"
_GAP = r"(\s+)"
_NAME_RULES = (
    (
        re.compile(r"\bAI" + _GAP + r"Studio" + _GAP + r"Desktop" + _GAP + r"GUI"),
        "LemGendary AI Studio GUI",
    ),
    (
        re.compile(r"LemGendary" + _GAP + r"Training" + _GAP + r"Suite"),
        "LemGendary Model Training Suite",
    ),
    (
        re.compile(r"LemGendary" + _GAP + r"AI" + _GAP + r"Studio\b(?!\s+(?:GUI|Assistant))"),
        "LemGendary AI Studio GUI",
    ),
    (
        re.compile(r"LemGendary" + _GAP + r"Dataset" + _GAP + r"Compiler\b(?!\s+(?:Suite|API\"))"),
        "LemGendary Dataset Compiler Suite",
    ),
)


@dataclass(frozen=True)
class Check:
    """A named audit check."""

    name: str
    description: str
    run: Callable[[AuditContext], Iterable[Finding]]


def _strip_v(version: str) -> str:
    return version.removeprefix("v")


def _publications(ctx: AuditContext) -> list[str]:
    return ctx.glob("papers/*.html") + ["index.html"]


def _markdown_sources(ctx: AuditContext) -> list[str]:
    return ctx.glob("*.md") + ctx.glob("MD-Papers/*.md")


def check_manifest(ctx: AuditContext) -> Iterator[Finding]:
    """Every manifest path exists and every publication is in the manifest."""
    subject = MANIFEST_PATH.as_posix()
    ids = [pair.doc_id for pair in ctx.pairs]
    for doc_id in sorted({i for i in ids if ids.count(i) > 1}):
        yield Finding("manifest", subject, f"duplicate document id {doc_id}")
    declared = ctx.manifest.get("total_publications")
    if declared != len(ctx.pairs):
        yield Finding(
            "manifest",
            subject,
            f"total_publications is {declared}, documents lists {len(ctx.pairs)}",
        )
    listed: set[str] = set()
    for pair in ctx.pairs:
        for path in (pair.md_path, pair.html_path):
            listed.add(path)
            if not ctx.exists(path):
                yield Finding("manifest", subject, f"{pair.doc_id}: {path} does not exist")
    for path in ctx.glob("papers/*.html") + ctx.glob("MD-Papers/*.md"):
        if path not in listed:
            yield Finding("manifest", subject, f"{path} is not listed in the manifest")


def check_hub_version(ctx: AuditContext) -> Iterator[Finding]:
    """README, index.html, manifest and both registries carry one hub version."""
    match = _README_VERSION.search(ctx.read_text("README.md"))
    if not match:
        yield Finding("hub-version", "README.md", "no **Version**: `vX.Y.Z` line")
        return
    expected = f"{match.group(1)}-STABLE"
    if f"Version {expected}" not in ctx.read_text("index.html"):
        yield Finding("hub-version", "index.html", f"header does not show Version {expected}")
    actual = {
        MANIFEST_PATH.as_posix(): ctx.manifest.get("document_baseline"),
        REGISTRY_FILES[0]: json.loads(ctx.read_text(REGISTRY_FILES[0])).get("document_baseline"),
    }
    yaml_match = _YAML_BASELINE.search(ctx.read_text(REGISTRY_FILES[1]))
    actual[REGISTRY_FILES[1]] = yaml_match.group(1) if yaml_match else None
    for path, value in actual.items():
        if value != expected:
            yield Finding(
                "hub-version", path, f"document_baseline is {value}, README says {expected}"
            )


def check_version_lines(ctx: AuditContext) -> Iterator[Finding]:
    """Markdown and HTML version lines equal the manifest baseline_version."""
    for pair in ctx.pairs:
        want = _strip_v(pair.baseline_version)
        for path in (pair.md_path, pair.html_path):
            if not ctx.exists(path):
                continue
            found = ctx.parsed(path).version
            if found is None:
                yield Finding("version-line", pair.doc_id, f"{path} has no version line")
            elif _strip_v(found) != want:
                yield Finding(
                    "version-line",
                    pair.doc_id,
                    f"{path} says {found}, manifest says {pair.baseline_version}",
                )


def _existing_pairs(ctx: AuditContext) -> Iterator[tuple[str, str, str]]:
    for pair in ctx.pairs:
        if ctx.exists(pair.md_path) and ctx.exists(pair.html_path):
            yield pair.doc_id, pair.md_path, pair.html_path


def check_heading_parity(ctx: AuditContext) -> Iterator[Finding]:
    """Markdown and HTML have the same headings (level and text) in the same order."""
    for doc_id, md_path, html_path in _existing_pairs(ctx):
        md = content_headings(ctx.parsed(md_path))
        page = content_headings(ctx.parsed(html_path))
        if md == page:
            continue
        index = next(
            (i for i, (a, b) in enumerate(zip(md, page, strict=False)) if a != b),
            min(len(md), len(page)),
        )
        md_at = f"h{md[index].level} '{md[index].text}'" if index < len(md) else "end"
        page_at = f"h{page[index].level} '{page[index].text}'" if index < len(page) else "end"
        yield Finding(
            "heading-parity",
            doc_id,
            f"MD {len(md)} vs HTML {len(page)} headings; first difference at #{index + 1}: "
            f"MD {md_at} vs HTML {page_at}",
        )


def check_text_similarity(ctx: AuditContext) -> Iterator[Finding]:
    """Markdown and HTML prose match (word-sequence similarity at least 0.85)."""
    for doc_id, md_path, html_path in _existing_pairs(ctx):
        md_words = ctx.parsed(md_path).words
        page_words = ctx.parsed(html_path).words
        ratio = difflib.SequenceMatcher(None, md_words, page_words, autojunk=False).ratio()
        if ratio < SIMILARITY_THRESHOLD:
            yield Finding(
                "text-similarity",
                doc_id,
                f"similarity {ratio:.3f} < {SIMILARITY_THRESHOLD} "
                f"(MD {len(md_words)} words, HTML {len(page_words)})",
            )


def check_list_items(ctx: AuditContext) -> Iterator[Finding]:
    """Top-level list items with a bold label match between Markdown and HTML.

    These are the rows of the master tables written as lists; a row present
    in one file and missing in the other is a finding.
    """
    for doc_id, md_path, html_path in _existing_pairs(ctx):
        md = ctx.parsed(md_path).list_labels
        page = ctx.parsed(html_path).list_labels
        if md == page:
            continue
        missing = [label for label in md if label not in page]
        extra = [label for label in page if label not in md]
        detail = []
        if missing:
            detail.append("missing from HTML: " + "; ".join(missing))
        if extra:
            detail.append("missing from MD: " + "; ".join(extra))
        if not detail:
            detail.append("same labels in a different order")
        yield Finding(
            "list-items",
            doc_id,
            f"MD {len(md)} vs HTML {len(page)} labelled list items; " + "; ".join(detail),
        )


def _duplicates(entries: list[TocEntry]) -> list[str]:
    targets = [entry.target for entry in entries]
    return sorted({target for target in targets if targets.count(target) > 1})


def _toc_mismatch(md: list[TocEntry], page: list[TocEntry]) -> str | None:
    """Describe how the sidebar differs from the Markdown ToC, or None."""
    md_texts = [entry.text for entry in md]
    page_texts = [entry.text for entry in page]
    if md_texts == page_texts:
        return None
    missing = [text for text in md_texts if text not in page_texts]
    extra = [text for text in page_texts if text not in md_texts]
    if not (missing or extra):
        return "sidebar lists the Markdown ToC entries in a different order"
    parts = []
    if missing:
        parts.append(f"missing from the sidebar: {'; '.join(missing)}")
    if extra:
        parts.append(f"not in the Markdown ToC: {'; '.join(extra)}")
    return ", ".join(parts)


def check_toc_sidebar(ctx: AuditContext) -> Iterator[Finding]:
    """The HTML sidebar matches the Markdown ToC and links every section."""
    for doc_id, md_path, html_path in _existing_pairs(ctx):
        md = ctx.parsed(md_path)
        page = ctx.parsed(html_path)
        for path, entries in ((md_path, md.toc), (html_path, page.toc)):
            for target in _duplicates(entries):
                yield Finding("toc-sidebar", doc_id, f"{path} lists #{target} more than once")
        if md.toc:
            mismatch = _toc_mismatch(md.toc, page.toc)
            if mismatch:
                yield Finding("toc-sidebar", doc_id, f"{html_path}: {mismatch}")
        targets = {entry.target for entry in page.toc}
        for section in page.sections:
            if section.has_body and not section.anchors & targets:
                yield Finding(
                    "toc-sidebar",
                    doc_id,
                    f"{html_path}: no sidebar link to section '{section.text}'",
                )


def check_alert_markers(ctx: AuditContext) -> Iterator[Finding]:
    """No raw GitHub alert markers ([!NOTE] and the like) in HTML pages."""
    for path in _publications(ctx):
        for number, line in enumerate(ctx.read_text(path).splitlines(), start=1):
            match = _ALERT_MARKER.search(line)
            if match:
                yield Finding(
                    "alert-markers",
                    path,
                    f"line {number}: raw {match.group(0)}; use a styled blockquote",
                )


def check_template(ctx: AuditContext) -> Iterator[Finding]:
    """HTML pages use the approved structural template."""
    for path in _publications(ctx):
        elements = ctx.parsed(path).elements
        missing = [name for name in TEMPLATE_ELEMENTS if name not in elements]
        if missing:
            yield Finding("template", path, f"missing {', '.join(missing)}")


def _link_target(source: str, url: str) -> tuple[str, str] | None:
    """Resolve an internal link to (target path, fragment); None for external links."""
    if not url or url.startswith("//") or _SCHEME.match(url):
        return None
    path, _, fragment = url.partition("#")
    path = unquote(path.split("?")[0])
    target = posixpath.normpath(posixpath.join(posixpath.dirname(source), path)) if path else source
    return target, unquote(fragment)


def check_links(ctx: AuditContext) -> Iterator[Finding]:
    """Internal links point at existing files and existing anchors."""
    for source in _markdown_sources(ctx) + _publications(ctx):
        for line, url in ctx.parsed(source).links:
            resolved = _link_target(source, url)
            if resolved is None:
                continue
            target, fragment = resolved
            if not ctx.path(target).exists():
                yield Finding("links", source, f"line {line}: {url} -> missing {target}")
            elif (
                fragment
                and target.endswith((".md", ".html"))
                and not target.startswith("../")
                and fragment not in ctx.parsed(target).anchors
            ):
                yield Finding(
                    "links", source, f"line {line}: {url} -> no anchor #{fragment} in {target}"
                )


def _text_files(ctx: AuditContext) -> Iterator[str]:
    for path in sorted(ctx.root.rglob("*")):
        relative = path.relative_to(ctx.root)
        if any(part in SKIPPED_DIRS or part.startswith(".venv") for part in relative.parts):
            continue
        if path.is_file() and (
            path.suffix.lower() in TEXT_SUFFIXES or relative.parts[0] == ".githooks"
        ):
            yield relative.as_posix()


def check_absolute_paths(ctx: AuditContext) -> Iterator[Finding]:
    """No hard-coded absolute paths in any text file."""
    for path in _text_files(ctx):
        for number, line in enumerate(ctx.read_text(path).splitlines(), start=1):
            match = _ABSOLUTE_PATH.search(line)
            if match:
                excerpt = line[max(0, match.start() - 20) : match.end() + 20].strip()
                yield Finding("absolute-paths", path, f"line {number}: {excerpt}")


def _name_scope(ctx: AuditContext, path: str) -> str:
    text = ctx.read_text(path)
    if path == "README.md":
        changelog = re.search(r"^### v", text, re.MULTILINE)
        return text[: changelog.start()] if changelog else text
    return text


def check_canonical_names(ctx: AuditContext) -> Iterator[Finding]:
    """Project names use the seven canonical names (README changelog is history)."""
    for path in _markdown_sources(ctx) + _publications(ctx):
        text = _name_scope(ctx, path)
        for pattern, canonical in _NAME_RULES:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                alias = re.sub(r"\s+", " ", match.group(0))
                yield Finding(
                    "canonical-names", path, f"line {line}: '{alias}' should be '{canonical}'"
                )


def _registry(ctx: AuditContext) -> dict[str, Any]:
    data = json.loads(ctx.read_text(REGISTRY_FILES[0]))
    return data if isinstance(data, dict) else {}


def check_registry_parity(ctx: AuditContext) -> Iterator[Finding]:
    """The YAML capability registry holds the same data as the JSON registry."""
    json_data = _registry(ctx)
    yaml_data = yaml.safe_load(ctx.read_text(REGISTRY_FILES[1]))
    if json_data == yaml_data:
        return
    if not isinstance(yaml_data, dict):
        yield Finding("registry-parity", REGISTRY_FILES[1], "is not a mapping")
        return
    keys = sorted(
        key
        for key in set(json_data) | set(yaml_data)
        if json_data.get(key) != yaml_data.get(key)
    )
    yield Finding(
        "registry-parity",
        REGISTRY_FILES[1],
        f"differs from {REGISTRY_FILES[0]} in: {', '.join(keys)}",
    )


def _models(ctx: AuditContext) -> list[dict[str, Any]]:
    models = _registry(ctx).get("models")
    return [m for m in models if isinstance(m, dict)] if isinstance(models, list) else []


def check_registry_models(ctx: AuditContext) -> Iterator[Finding]:
    """Registry model ids equal the training registry keys (without metadata)."""
    subject = REGISTRY_FILES[0]
    try:
        expected = ctx.workspace.training_model_ids
        source = ctx.workspace.training_registry_path.as_posix()
    except WorkspaceError as error:
        yield Finding("registry-models", subject, str(error))
        return
    ids = [str(model.get("id")) for model in _models(ctx)]
    for model_id in sorted({i for i in ids if ids.count(i) > 1}):
        yield Finding("registry-models", subject, f"duplicate model id {model_id}")
    missing = sorted(set(expected) - set(ids))
    extra = sorted(set(ids) - set(expected))
    if missing:
        yield Finding(
            "registry-models", subject, f"missing models of {source}: {', '.join(missing)}"
        )
    if extra:
        yield Finding("registry-models", subject, f"models not in {source}: {', '.join(extra)}")


def _release(version: object) -> str:
    return _strip_v(str(version)).removesuffix(_RELEASE_SUFFIX)


def check_component_versions(ctx: AuditContext) -> Iterator[Finding]:
    """Registry component baselines equal the versions the components declare."""
    subject = REGISTRY_FILES[0]
    registry = _registry(ctx)
    for source in COMPONENT_SOURCES:
        try:
            declared = ctx.workspace.component_version(source)
            origin = ctx.workspace.component_version_path(source).as_posix()
        except WorkspaceError as error:
            yield Finding("component-versions", subject, str(error))
            continue
        recorded = registry.get(source.registry_key)
        if _release(recorded) != _release(declared):
            yield Finding(
                "component-versions",
                f"{subject}#{source.registry_key}",
                f"{source.registry_key} is {recorded}, {origin} declares {declared}",
            )
    gui = registry.get("control_planes", {}).get("gui", {})
    client = registry.get("desktop_client_baseline")
    if "version" in gui and gui["version"] != client:
        yield Finding(
            "component-versions",
            f"{subject}#control_planes.gui.version",
            f"control_planes.gui.version is {gui['version']}, "
            f"desktop_client_baseline is {client}",
        )


def check_service_ports(ctx: AuditContext) -> Iterator[Finding]:
    """Registry ports equal the service ports of ecosystem.json."""
    subject = REGISTRY_FILES[0]
    source = ECOSYSTEM_PATH.as_posix()
    try:
        services = ctx.workspace.services
        training = ctx.workspace.service(TRAINING_SERVICE_ID)
    except WorkspaceError as error:
        yield Finding("service-ports", subject, str(error))
        return
    for model in _models(ctx):
        api = model.get("control_planes", {}).get("api", {})
        port = api.get("port")
        if port is None and not api.get("available"):
            continue
        if port != training.port:
            yield Finding(
                "service-ports",
                subject,
                f"model {model.get('id')}: api.port is {port}, "
                f"{source} gives {TRAINING_SERVICE_ID} port {training.port}",
            )
    gui_ports = _registry(ctx).get("control_planes", {}).get("gui", {}).get("ports", {})
    for key in sorted(set(gui_ports) | set(GUI_PORT_SERVICES)):
        service_id = GUI_PORT_SERVICES.get(key)
        if service_id is None:
            yield Finding("service-ports", subject, f"control_planes.gui.ports.{key} is unknown")
            continue
        service = services.get(service_id)
        want = service.port if service else None
        if gui_ports.get(key) != want:
            yield Finding(
                "service-ports",
                subject,
                f"control_planes.gui.ports.{key} is {gui_ports.get(key)}, "
                f"{source} gives {service_id} port {want}",
            )


CHECKS: tuple[Check, ...] = (
    Check("manifest", "manifest paths exist; no unlisted publications", check_manifest),
    Check("hub-version", "README, index.html, manifest and registries agree", check_hub_version),
    Check("version-line", "MD and HTML version lines equal the manifest", check_version_lines),
    Check(
        "heading-parity",
        "MD and HTML headings match in level, text and order",
        check_heading_parity,
    ),
    Check(
        "text-similarity",
        f"MD and HTML prose similarity >= {SIMILARITY_THRESHOLD}",
        check_text_similarity,
    ),
    Check(
        "list-items",
        "MD and HTML top-level labelled list items (master-table rows) match",
        check_list_items,
    ),
    Check(
        "toc-sidebar",
        "HTML sidebar matches the Markdown ToC, no duplicates, every section linked",
        check_toc_sidebar,
    ),
    Check("alert-markers", "no raw GitHub alert markers in HTML", check_alert_markers),
    Check("template", "HTML uses the approved structural template", check_template),
    Check("links", "internal links and anchors resolve", check_links),
    Check("absolute-paths", "no hard-coded absolute paths", check_absolute_paths),
    Check("canonical-names", "canonical project names only", check_canonical_names),
    Check("registry-parity", "JSON and YAML capability registries agree", check_registry_parity),
    Check(
        "registry-models",
        "registry model ids equal the training registry keys",
        check_registry_models,
    ),
    Check("service-ports", "registry ports equal the ecosystem.json ports", check_service_ports),
    Check(
        "component-versions",
        "registry component baselines equal the sibling release versions",
        check_component_versions,
    ),
)
