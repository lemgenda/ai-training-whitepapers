"""Tests for the documentation audit module (scripts/docs_audit).

Each test builds a small synthetic docs repository with one clean MD/HTML
pair, applies one kind of drift, and checks that the audit reports it. The
sibling sources (ecosystem.json, training registry) come from the fixture
workspace in tests/fixtures/workspace, selected with LEMGENDARY_WORKSPACE_ROOT.
"""

import contextlib
import importlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

docs_audit = importlib.import_module("docs_audit")
audit_docs = importlib.import_module("audit_docs")

FIXTURE_WORKSPACE = Path(__file__).resolve().parent / "fixtures" / "workspace"
FIXTURE = docs_audit.Workspace(FIXTURE_WORKSPACE)
GUI_PORT_SERVICES = importlib.import_module("docs_audit.checks").GUI_PORT_SERVICES

HUB_VERSION = "v1.2.3"
DOC_VERSION = "v1.0.0-STABLE"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>{title}</title></head>
<body>
<header><h1>{title}</h1><p class="subtitle">Category 01 TEST</p>
<span>Version: {version}</span></header>
<nav class="toc-sidebar" aria-label="Table of Contents"><h4>Table of Contents</h4>
<a href="#1-abstract">1. Abstract</a> <a href="#2-method">2. Method</a></nav>
<section id="1-abstract"><h2>1. Abstract</h2>
<p>The {name} engine restores old photographs with a gated network.</p></section>
<section id="2-method"><h2>2. Method</h2>
<p>Training uses a progressive ladder and the LemGendary Model Training Suite.</p></section>
<footer><p>LemGendary AI Documentation Hub</p></footer>
</body>
</html>
"""

MARKDOWN = """# {title}

## Category 01 TEST

**Version**: `{version}`

## Table of Contents

- [1. Abstract](#1-abstract)
- [2. Method](#2-method)

## 1. Abstract

The {name} engine restores old photographs with a gated network.

## 2. Method

Training uses a progressive ladder and the LemGendary Model Training Suite.
"""

INDEX = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Hub</title></head>
<body><header><h1>Hub</h1><span>Version {hub}-STABLE</span></header>
<nav class="toc-sidebar"><a href="papers/alpha.html">Alpha</a>
<a href="papers/beta.html#2-method">Beta</a></nav>
<section><h2>Catalog</h2></section><footer><p>Hub</p></footer></body></html>
"""


class SyntheticDocsRepo:
    """A minimal docs repository with two clean MD/HTML pairs."""

    DOCS = ("alpha", "beta")

    def __init__(self, root: Path):
        self.root = root
        documents = []
        for name in self.DOCS:
            title = f"{name.title()} Restoration Whitepaper"
            self.write(
                f"MD-Papers/{name.upper()}.md",
                MARKDOWN.format(title=title, version=DOC_VERSION, name=name),
            )
            self.write(
                f"papers/{name}.html", TEMPLATE.format(title=title, version=DOC_VERSION, name=name)
            )
            documents.append(
                {
                    "id": name,
                    "title": title,
                    "md_path": f"MD-Papers/{name.upper()}.md",
                    "html_path": f"papers/{name}.html",
                    "baseline_version": DOC_VERSION,
                }
            )
        baseline = f"{HUB_VERSION}-STABLE"
        manifest = {
            "document_baseline": baseline,
            "total_publications": len(documents),
            "documents": documents,
        }
        self.write("manifest/documents.json", json.dumps(manifest, indent=2))
        self.write_registry(self.registry(baseline))
        self.write(
            "README.md",
            f"# Hub\n\n**Version**: `{HUB_VERSION}`\n\n### {HUB_VERSION} - Notes\n\nOld text.\n",
        )
        self.write("index.html", INDEX.format(hub=HUB_VERSION))

    @staticmethod
    def registry(baseline: str) -> dict:
        """A capability registry consistent with the fixture workspace."""
        training_port = FIXTURE.service("training-suite").port
        return {
            "document_baseline": baseline,
            "control_planes": {
                "gui": {
                    "ports": {
                        key: FIXTURE.service(service_id).port
                        for key, service_id in GUI_PORT_SERVICES.items()
                    }
                }
            },
            "models": [
                {
                    "id": model_id,
                    "control_planes": {"api": {"available": True, "port": training_port}},
                }
                for model_id in FIXTURE.training_model_ids
            ],
        }

    def write_registry(self, data: dict, yaml_data: dict | None = None) -> None:
        self.write("canonical_capabilities.json", json.dumps(data, indent=2))
        self.write(
            "canonical_capabilities.yaml",
            yaml.safe_dump(data if yaml_data is None else yaml_data, sort_keys=False),
        )

    def path(self, relative: str) -> Path:
        return self.root / relative

    def write(self, relative: str, text: str) -> None:
        target = self.path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def replace(self, relative: str, old: str, new: str) -> None:
        text = self.path(relative).read_text(encoding="utf-8")
        if old not in text:
            raise AssertionError(f"{old!r} not found in {relative}")
        self.write(relative, text.replace(old, new, 1))

    def backlog(self, mapping: dict) -> None:
        self.write(
            "scripts/parity_backlog.json", json.dumps({"description": "test", "backlog": mapping})
        )


class TestDocsAudit(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        env = mock.patch.dict(os.environ, {docs_audit.WORKSPACE_ENV: str(FIXTURE_WORKSPACE)})
        env.start()
        self.addCleanup(env.stop)
        self.repo = SyntheticDocsRepo(Path(self._tmp.name))

    def audit(self):
        return docs_audit.run_audit(self.repo.root)

    def assertFinding(self, result, check, subject):
        keys = {f.key for f in result.new}
        self.assertIn((check, subject), keys, docs_audit.render(result))
        self.assertFalse(result.passed)

    def test_clean_pair_passes(self):
        result = self.audit()
        self.assertTrue(result.passed, docs_audit.render(result))
        self.assertEqual(result.new, [])
        self.assertEqual(result.known, [])

    def test_heading_text_drift_detected(self):
        self.repo.replace("papers/beta.html", "<h2>2. Method</h2>", "<h2>2. Methods</h2>")
        self.assertFinding(self.audit(), "heading-parity", "beta")

    def test_heading_order_drift_detected(self):
        self.repo.replace("MD-Papers/ALPHA.md", "## 2. Method", "### 2. Method")
        self.assertFinding(self.audit(), "heading-parity", "alpha")

    def test_text_drift_detected(self):
        self.repo.replace(
            "papers/alpha.html",
            "The alpha engine restores old photographs with a gated network.",
            "A completely different paragraph about forex prediction and market regimes.",
        )
        self.assertFinding(self.audit(), "text-similarity", "alpha")

    def test_display_math_is_not_prose(self):
        formula = " ".join(f"x_{i} + y_{i}" for i in range(40))
        self.repo.replace(
            "MD-Papers/ALPHA.md",
            "gated network.\n",
            f"gated network.\n\n$$\n{formula}\n$$\n",
        )
        self.repo.replace(
            "papers/alpha.html",
            "gated network.</p>",
            f'gated network.</p><div class="math-block">$${formula}$$</div>',
        )
        result = self.audit()
        self.assertTrue(result.passed, docs_audit.render(result))

    def test_code_block_is_not_prose(self):
        code = "\n".join(f'"key_{i}": "value number {i}",' for i in range(40))
        self.repo.replace(
            "MD-Papers/ALPHA.md",
            "gated network.\n",
            f"gated network.\n\n```json\n{code}\n```\n",
        )
        self.repo.replace(
            "papers/alpha.html",
            "gated network.</p>",
            f"gated network.</p><pre><code>{code}</code></pre>",
        )
        result = self.audit()
        self.assertTrue(result.passed, docs_audit.render(result))

    def test_version_line_drift_detected(self):
        self.repo.replace("papers/alpha.html", f"Version: {DOC_VERSION}", "Version: v0.9.0-STABLE")
        self.assertFinding(self.audit(), "version-line", "alpha")

    def test_hub_version_drift_detected(self):
        self.repo.replace("index.html", f"Version {HUB_VERSION}-STABLE", "Version v0.0.1-STABLE")
        self.assertFinding(self.audit(), "hub-version", "index.html")

    def test_broken_anchor_detected(self):
        self.repo.replace("MD-Papers/BETA.md", "](#2-method)", "](#2-methods)")
        self.assertFinding(self.audit(), "links", "MD-Papers/BETA.md")

    def test_missing_link_target_detected(self):
        self.repo.replace("index.html", "papers/beta.html#2-method", "papers/gamma.html")
        self.assertFinding(self.audit(), "links", "index.html")

    def test_template_element_missing_detected(self):
        self.repo.replace(
            "papers/beta.html", "<footer><p>LemGendary AI Documentation Hub</p></footer>", ""
        )
        self.assertFinding(self.audit(), "template", "papers/beta.html")

    def test_absolute_path_detected(self):
        drive_path = "C" + ":" + "\\" + "Tools"
        self.repo.replace("MD-Papers/ALPHA.md", "gated network.", f"gated network in {drive_path}.")
        self.assertFinding(self.audit(), "absolute-paths", "MD-Papers/ALPHA.md")

    def test_non_canonical_name_detected(self):
        self.repo.replace(
            "papers/alpha.html", "LemGendary Model Training Suite", "LemGendary Training Suite"
        )
        self.assertFinding(self.audit(), "canonical-names", "papers/alpha.html")

    def test_readme_changelog_history_is_not_a_name_finding(self):
        self.repo.replace("README.md", "Old text.", "Renamed the LemGendary Training Suite.")
        self.assertTrue(self.audit().passed)

    def test_unlisted_publication_detected(self):
        self.repo.write(
            "papers/gamma.html", TEMPLATE.format(title="Gamma", version=DOC_VERSION, name="gamma")
        )
        self.assertFinding(self.audit(), "manifest", "manifest/documents.json")

    def test_backlog_entry_is_tolerated(self):
        self.repo.replace("papers/beta.html", "<h2>2. Method</h2>", "<h2>2. Methods</h2>")
        self.repo.backlog({"heading-parity": ["beta"]})
        result = self.audit()
        self.assertTrue(result.passed, docs_audit.render(result))
        self.assertEqual([f.key for f in result.known], [("heading-parity", "beta")])
        self.assertIn("Known backlog (Later Phase): 1 entries", docs_audit.render(result))

    def test_new_drift_fails_despite_backlog(self):
        self.repo.replace("papers/beta.html", "<h2>2. Method</h2>", "<h2>2. Methods</h2>")
        self.repo.replace("papers/alpha.html", "<h2>2. Method</h2>", "<h2>2. Approach</h2>")
        self.repo.backlog({"heading-parity": ["beta"]})
        result = self.audit()
        self.assertEqual([f.key for f in result.new], [("heading-parity", "alpha")])
        self.assertFalse(result.passed)

    def test_stale_backlog_entry_fails(self):
        self.repo.backlog({"heading-parity": ["beta"]})
        result = self.audit()
        self.assertEqual(result.stale, [("heading-parity", "beta")])
        self.assertFalse(result.passed)

    def test_unknown_backlog_check_fails(self):
        self.repo.backlog({"no-such-check": ["beta"]})
        result = self.audit()
        self.assertEqual(result.unknown_checks, [("no-such-check", "beta")])
        self.assertFalse(result.passed)

    def _registry(self) -> dict:
        return json.loads(self.repo.path("canonical_capabilities.json").read_text(encoding="utf-8"))

    def test_registry_yaml_drift_detected(self):
        data = self._registry()
        yaml_data = json.loads(json.dumps(data))
        yaml_data["document_baseline"] = "v0.0.0-STABLE"
        self.repo.write_registry(data, yaml_data)
        result = self.audit()
        self.assertFinding(result, "registry-parity", "canonical_capabilities.yaml")
        self.assertIn("document_baseline", docs_audit.render(result))

    def test_registry_model_drift_detected(self):
        data = self._registry()
        removed = data["models"][0]["id"]
        data["models"][0]["id"] = "gamma_model"
        self.repo.write_registry(data)
        result = self.audit()
        self.assertFinding(result, "registry-models", "canonical_capabilities.json")
        report = docs_audit.render(result)
        source = FIXTURE.training_registry_path.as_posix()
        self.assertIn(f"models not in {source}: gamma_model", report)
        self.assertIn(f"missing models of {source}: {removed}", report)

    def test_registry_metadata_key_is_not_a_model(self):
        self.assertNotIn("_registry_metadata", FIXTURE.training_model_ids)
        self.assertTrue(self.audit().passed)

    def test_api_port_drift_detected(self):
        data = self._registry()
        data["models"][0]["control_planes"]["api"]["port"] += 1
        self.repo.write_registry(data)
        self.assertFinding(self.audit(), "service-ports", "canonical_capabilities.json")

    def test_gui_port_drift_detected(self):
        data = self._registry()
        key = next(iter(GUI_PORT_SERVICES))
        data["control_planes"]["gui"]["ports"][key] += 1
        self.repo.write_registry(data)
        result = self.audit()
        self.assertFinding(result, "service-ports", "canonical_capabilities.json")
        self.assertIn(key, docs_audit.render(result))

    def test_missing_workspace_is_a_clear_finding(self):
        with mock.patch.dict(os.environ, {docs_audit.WORKSPACE_ENV: str(self.repo.root)}):
            result = self.audit()
        self.assertFinding(result, "registry-models", "canonical_capabilities.json")
        self.assertIn(docs_audit.WORKSPACE_ENV, docs_audit.render(result))
        self.assertIn("ecosystem.json not found", docs_audit.render(result))

    def test_workspace_root_defaults_to_docs_parent(self):
        with mock.patch.dict(os.environ):
            os.environ.pop(docs_audit.WORKSPACE_ENV, None)
            self.assertEqual(
                docs_audit.workspace_root(self.repo.root), self.repo.root.resolve().parent
            )
        self.assertEqual(docs_audit.workspace_root(self.repo.root), FIXTURE_WORKSPACE.resolve())

    def test_cli_exit_codes_from_another_directory(self):
        cwd = os.getcwd()
        self.addCleanup(os.chdir, cwd)
        os.chdir(tempfile.gettempdir())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(audit_docs.main(["--root", str(self.repo.root)]), 0)
            self.repo.replace("papers/beta.html", "<h2>2. Method</h2>", "<h2>2. Methods</h2>")
            self.assertEqual(audit_docs.main(["--root", str(self.repo.root)]), 1)


class TestRepositoryAudit(unittest.TestCase):
    """The real repository passes: no new drift, no stale backlog entries."""

    def test_repository_passes_audit(self):
        result = docs_audit.run_audit()
        self.assertTrue(result.passed, docs_audit.render(result))

    def test_default_root_is_resolved_from_module_location(self):
        self.assertEqual(docs_audit.DOCS_ROOT, Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    unittest.main()
