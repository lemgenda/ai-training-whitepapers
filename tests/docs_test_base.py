"""Shared fixtures of the LemGendary AI Documentation Hub test modules.

``DocsTestCase`` resolves the docs root, the workspace root (parent of the docs
root, or ``LEMGENDARY_WORKSPACE_ROOT``), the HTML and Markdown pages and the
model manifest once per test class.
"""

import glob
import importlib
import os
import sys
import unittest
from pathlib import Path

yaml = importlib.import_module("yaml")

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
docs_audit = importlib.import_module("docs_audit")


class DocsTestCase(unittest.TestCase):
    """Base class: paths, page lists and the model manifest of the documentation hub."""

    @classmethod
    def setUpClass(cls):
        cls.docs_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # Parent of the docs root, or LEMGENDARY_WORKSPACE_ROOT when set.
        cls.workspace_root = str(docs_audit.workspace_root(Path(cls.docs_root)))
        cls.workspace = docs_audit.Workspace(Path(cls.workspace_root))
        cls.html_files = glob.glob(os.path.join(cls.docs_root, "papers", "*.html"))
        cls.index_html = os.path.join(cls.docs_root, "index.html")
        if os.path.exists(cls.index_html):
            cls.html_files.append(cls.index_html)
        cls.md_files = glob.glob(os.path.join(cls.docs_root, "MD-Papers", "*.md"))
        cls.manifest_path = os.path.join(
            cls.workspace_root, "lemgendary-training-suite", "unified_models_v2.yaml"
        )
        if not os.path.exists(cls.manifest_path):
            candidate = os.path.join(cls.docs_root, "canonical_capabilities.yaml")
            if os.path.exists(candidate):
                cls.manifest_path = candidate
        if not os.path.exists(cls.manifest_path):
            raise FileNotFoundError(
                f"Model manifest not found at {cls.manifest_path}. Ensure unified_models_v2.yaml "
                "or canonical_capabilities.yaml exists."
            )
        with open(cls.manifest_path, "r", encoding="utf-8") as f:
            raw_manifest = yaml.safe_load(f)
            if (
                isinstance(raw_manifest, dict)
                and "models" in raw_manifest
                and isinstance(raw_manifest["models"], list)
            ):
                cls.manifest = {m["id"]: m for m in raw_manifest["models"] if "id" in m}
            else:
                cls.manifest = raw_manifest

    # The AI Helper corpus is data of the LemGendary Compiled Manifolds Repo
    # (../LemGendaryDatasets), a sibling checkout that is not part of this
    # repository. Tests that read it skip with this reason when it is absent.
    AI_HELPER_CORPUS_DIRS = ("LemGendizedAIHelperLemGend", "LemGendizedAIHelperCorpus")

    def _ai_helper_corpus(self):
        """Return (corpus_dir, train_path, val_path) or skip with an explicit reason."""
        manifolds_repo = os.path.join(self.workspace_root, "LemGendaryDatasets")
        for name in self.AI_HELPER_CORPUS_DIRS:
            corpus_dir = os.path.join(manifolds_repo, name)
            data_dir = os.path.join(corpus_dir, "data")
            base = data_dir if os.path.isdir(data_dir) else corpus_dir
            train_path = os.path.join(base, "ai_helper_train.jsonl")
            val_path = os.path.join(base, "ai_helper_val.jsonl")
            if os.path.isfile(train_path) and os.path.isfile(val_path):
                return corpus_dir, train_path, val_path
        raise unittest.SkipTest(
            "AI Helper corpus not found: needs the LemGendary Compiled Manifolds Repo checked "
            "out as "
            "../LemGendaryDatasets with "
            + " or ".join(self.AI_HELPER_CORPUS_DIRS)
            + " containing ai_helper_train.jsonl and ai_helper_val.jsonl"
        )
