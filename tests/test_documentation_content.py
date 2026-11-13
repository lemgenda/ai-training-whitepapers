"""Content and cross-repository consistency tests of the LemGendary AI Documentation Hub."""

import glob
import json
import os
import re
import unittest
from html.parser import HTMLParser

from docs_test_base import DocsTestCase


class TestDocumentationContent(DocsTestCase):
    """Equations, taxonomy, branding, parity and cross-repository facts in the documents."""

    # ── 22. Header Authority & Version Metadata ────────────────────────────
    def test_header_version_authority_metadata(self):
        """Rule: Central index.html header must expose version, last-reviewed date, and authority
        status."""
        with open(self.index_html, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()

        readme = os.path.join(self.docs_root, "README.md")
        with open(readme, "r", encoding="utf-8") as f:
            match = re.search(r"\*\*Version\*\*: `(v[0-9.]+)`", f.read())
        if match is None:
            self.fail("README.md has no **Version** line")
        hub_version = match.group(1)
        self.assertIn(
            f"Version {hub_version}-STABLE",
            txt,
            "index.html header version must equal the README version",
        )
        self.assertIn("Last Reviewed:", txt, "index.html missing last-reviewed date metadata")
        self.assertIn("AUTHORITATIVE SSOT", txt, "index.html missing authoritative SSOT badge")

    # ── 23. AI Helper Knowledge Contract & Resolution Protocol ──────────────
    def test_ai_helper_knowledge_contract(self):
        """Rule: AI Helper Troubleshooting Knowledge Base must specify authority hierarchy,
        intake protocol, and admission bounds."""
        tb_md = os.path.join(self.docs_root, "MD-Papers", "AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md")
        tb_html = os.path.join(self.docs_root, "papers", "ai-helper-troubleshooting-knowledge.html")

        with open(tb_md, "r", encoding="utf-8", errors="ignore") as f:
            md_txt = f.read()
        with open(tb_html, "r", encoding="utf-8", errors="ignore") as f:
            html_txt = f.read()

        for content in [md_txt, html_txt]:
            self.assertIn("Authority Hierarchy", content, "Missing Authority Hierarchy section")
            self.assertIn("Mandatory Citation Policy", content, "Missing Mandatory Citation Policy")
            self.assertIn(
                "Diagnostic Intake Protocol", content, "Missing Diagnostic Intake Protocol"
            )
            self.assertIn(
                "UNVERIFIED IN PUBLISHED HUB", content, "Missing Explicit Admission Bound statement"
            )

    # ── 24. Task-Based Diagnostic Scenario Coverage ─────────────────────────
    def test_troubleshooting_task_scenarios(self):
        """Rule: AI Helper Knowledge Base must cover key real-world diagnostic failure scenarios."""
        tb_md = os.path.join(self.docs_root, "MD-Papers", "AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md")
        with open(tb_md, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()

        scenarios = [
            "Low GPU Utilization and Dataloader Starvation",
            "NaN Instability in Mixed Precision",
            "Scheduler Double-Stepping",
            "Sentinel and Scheduler Desynchronization",
            "Infinite Plateau Loop",
            "Pearson & Spearman Matrix Singularities",
            "Power-Loss Resilience",
            "Runway Bloat During Spatial Resolution Escalation",
            "Hardlink vs. Perceptual Deduplication Conflicts",
            "Raw Dataset vs. Compiled Manifold Path Confusion",
        ]
        for scenario in scenarios:
            self.assertIn(scenario, txt, f"Missing diagnostic scenario: {scenario}")

    # ── 25. Regex Escape Math Corruption Defense ─────────────────────────────
    def test_no_regex_escape_math_corruptions(self):
        r"""Rule: Documentation must never contain corrupted regex escapes such as
        '\|^2\\right]'."""
        corrupted_pat = re.compile(r"(\|\|?\^2\\right\]|\\right\]\|\|?\^2)")
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if corrupted_pat.search(content):
                failures.append(os.path.basename(path))
        self.assertEqual(len(failures), 0, f"Corrupted LaTeX escape artifacts found in: {failures}")

    # ── 26. Global Category Taxonomy Integrity ──────────────────────────────
    def test_no_category_taxonomy_drift(self):
        """Rule: Documentation must adhere to canonical Category 00 through 13 taxonomy with zero
        Category 15 drift."""
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "Category 15" in content or "CATEGORY 15" in content:
                failures.append(os.path.basename(path))
        self.assertEqual(len(failures), 0, f"Drifted Category 15 found in: {failures}")

    # ── 27. Canonical Author Standardization ─────────────────────────────────
    def test_canonical_author_standardization(self):
        """Rule: Author name must be consistently standardized as 'Lem Treursic' without diacritic
        variants."""
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "Lem Treursić" in content:
                failures.append(os.path.basename(path))
        self.assertEqual(
            len(failures), 0, f"Non-canonical author spelling 'Lem Treursić' found in: {failures}"
        )

    # ── 28. SwiGLU Architectural Formulation Integrity ──────────────────────
    def test_swiglu_equation_integrity(self):
        """Rule: SwiGLU formula must explicitly project inputs through independent gate (W_1)
        and value (W_2) matrices."""
        llm_html = os.path.join(self.docs_root, "papers", "foundation-llm.html")
        llm_md = os.path.join(self.docs_root, "MD-Papers", "PAPER_LEMGENDARY_LLM.md")
        for fpath in [llm_html, llm_md]:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            self.assertIn("W_1", txt, f"Missing W_1 gate projection in {os.path.basename(fpath)}")
            self.assertIn("W_2", txt, f"Missing W_2 value projection in {os.path.basename(fpath)}")
            self.assertNotIn(
                "(x W_1 \\odot \\sigma(x W_1)) W_2",
                txt,
                f"Degenerate non-gated SwiGLU found in {os.path.basename(fpath)}",
            )

    # ── 29. VLM Cross-Entropy Equation Integrity ────────────────────────────
    def test_vlm_cross_entropy_equation_integrity(self):
        """Rule: VLM cross-entropy loss must escape less-than operators to prevent HTML tag
        truncation."""
        vlm_html = os.path.join(self.docs_root, "papers", "foundation-image-to-text.html")
        vlm_md = os.path.join(self.docs_root, "MD-Papers", "PAPER_LEMGENDARY_IMAGE_TO_TEXT.md")
        for fpath in [vlm_html, vlm_md]:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            self.assertNotIn(
                "w_{<t}",
                txt,
                f"Unescaped w_{{<t}} causing HTML tag truncation in {os.path.basename(fpath)}",
            )
            self.assertIn("w_{\\lt t}", txt, f"Expected w_{{\\lt t}} in {os.path.basename(fpath)}")

    # ── 30. Hub Index Branding Consistency ──────────────────────────────────
    def test_hub_index_branding_consistency(self):
        """Rule: Hub index must consistently use 'LemGendary AI' for product and copyright
        branding."""
        index_html = os.path.join(self.docs_root, "index.html")
        with open(index_html, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        self.assertNotIn('alt="LemGenda"', txt, "Index logo alt text should be 'LemGendary AI'")
        self.assertNotIn(
            "&copy; 2026 LemGenda AI Hub", txt, "Index copyright should use the canonical hub name"
        )
        self.assertIn(
            "&copy; 2026 LemGendary AI Documentation Hub",
            txt,
            "Missing canonical 'LemGendary AI Documentation Hub' copyright",
        )

    # ── 31. Universal LaTeX Formula & Tag Integrity ──────────────────────────
    def test_universal_latex_formula_and_tag_integrity(self):
        """Rule: All LaTeX blocks across all publications must have balanced delimiters,
        braces, and 0 unescaped HTML tags."""
        patterns = [
            re.compile(r"\$\$([\s\S]*?)\$\$"),
            re.compile(r"\\\[([\s\S]*?)\\\]"),
            re.compile(r"\\\(([\s\S]*?)\\\)"),
        ]
        failures = []
        for fpath in self.html_files:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            for regex in patterns:
                for match in regex.finditer(content):
                    math_text = match.group(1).strip()
                    if re.search(r"<[a-zA-Z/][^>]*>", math_text):
                        failures.append(
                            f"{os.path.basename(fpath)}: HTML tag inside math block: "
                            f"{math_text[:50]}"
                        )
                    n_left = len(re.findall(r"\\left(?![a-zA-Z])", math_text))
                    n_right = len(re.findall(r"\\right(?![a-zA-Z])", math_text))
                    if n_left != n_right:
                        failures.append(
                            f"{os.path.basename(fpath)}: Unbalanced \\left/\\right ({n_left} vs "
                            f"{n_right})"
                        )
                    if math_text.count("{") != math_text.count("}"):
                        failures.append(
                            f"{os.path.basename(fpath)}: Unbalanced braces in math block"
                        )
        self.assertEqual(len(failures), 0, f"Universal LaTeX integrity violations: {failures}")

    # ── 32. HTML Parser Tag Hierarchy Integrity ─────────────────────────────
    def test_html_parser_tag_integrity(self):
        """Rule: All HTML files must parse cleanly with zero unescaped tags or unclosed major
        containers."""
        valid_tags = {
            "a",
            "abbr",
            "address",
            "area",
            "article",
            "aside",
            "audio",
            "b",
            "base",
            "bdi",
            "bdo",
            "blockquote",
            "body",
            "br",
            "button",
            "canvas",
            "caption",
            "cite",
            "code",
            "col",
            "colgroup",
            "data",
            "datalist",
            "dd",
            "del",
            "details",
            "dfn",
            "dialog",
            "div",
            "dl",
            "dt",
            "em",
            "embed",
            "fieldset",
            "figcaption",
            "figure",
            "footer",
            "form",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "head",
            "header",
            "hr",
            "html",
            "i",
            "iframe",
            "img",
            "input",
            "ins",
            "kbd",
            "label",
            "legend",
            "li",
            "link",
            "main",
            "map",
            "mark",
            "meta",
            "meter",
            "nav",
            "noscript",
            "object",
            "ol",
            "optgroup",
            "option",
            "output",
            "p",
            "param",
            "picture",
            "pre",
            "progress",
            "q",
            "rp",
            "rt",
            "ruby",
            "s",
            "samp",
            "script",
            "section",
            "select",
            "small",
            "source",
            "span",
            "strong",
            "style",
            "sub",
            "summary",
            "sup",
            "svg",
            "table",
            "tbody",
            "td",
            "template",
            "textarea",
            "tfoot",
            "th",
            "thead",
            "time",
            "title",
            "tr",
            "track",
            "u",
            "ul",
            "var",
            "video",
            "wbr",
            "circle",
            "line",
            "path",
            "rect",
            "polygon",
            "polyline",
            "text",
            "g",
            "defs",
            "clippath",
            "use",
        }

        class StrictValidator(HTMLParser):
            """Collects unknown tags, stray closing tags and unclosed major containers."""

            def __init__(self, filename):
                super().__init__()
                self.filename = filename
                self.errors = []
                self.stack = []
                self.void_tags = {
                    "meta",
                    "link",
                    "img",
                    "br",
                    "hr",
                    "input",
                    "area",
                    "base",
                    "col",
                    "embed",
                    "param",
                    "source",
                    "track",
                    "wbr",
                }

            def handle_starttag(self, tag, attrs):
                t = tag.lower()
                if t not in valid_tags:
                    self.errors.append(
                        f"Unescaped or invalid tag <{tag}> at line {self.getpos()[0]}"
                    )
                if t not in self.void_tags:
                    self.stack.append((t, self.getpos()))

            def handle_endtag(self, tag):
                t = tag.lower()
                if t in self.void_tags:
                    return
                if not self.stack:
                    self.errors.append(f"Stray closing </{tag}> at line {self.getpos()[0]}")
                    return
                while self.stack:
                    top_tag, pos = self.stack.pop()
                    if top_tag == t:
                        return
                    if top_tag in {
                        "html",
                        "head",
                        "body",
                        "main",
                        "nav",
                        "header",
                        "footer",
                        "table",
                        "thead",
                        "tbody",
                        "section",
                    }:
                        self.errors.append(
                            f"Unclosed major tag <{top_tag}> from line {pos[0]} "
                            f"when encountering </{tag}> at line {self.getpos()[0]}"
                        )
                        return

        all_errors = []
        for path in self.html_files:
            validator = StrictValidator(path)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                validator.feed(f.read())
            if validator.errors:
                all_errors.append(f"{os.path.basename(path)}: {validator.errors}")
        self.assertEqual(len(all_errors), 0, f"HTML parser tag integrity failures: {all_errors}")

    # ── 33. Cross-Repository Runtime & Manifest Consistency ─────────────────
    def test_cross_repo_manifest_and_runtime_consistency(self):
        """Rule: Model identifiers in unified_models_v2.yaml and the sidecar ports of
        ecosystem.json (LemGendary Environment Manager) must match documentation."""
        models = [k for k in self.manifest if not k.startswith("_")]
        self.assertGreater(len(models), 10, "unified_models_v2.yaml must declare model definitions")

        # Verify port bindings in authoritative documents
        current_state_path = os.path.join(self.docs_root, "papers", "current-state.html")
        with open(current_state_path, "r", encoding="utf-8", errors="ignore") as f:
            cs_txt = f.read()
        services = self.workspace.services
        self.assertTrue(services, "ecosystem.json must declare the sidecar services")
        for service in services.values():
            self.assertIn(
                str(service.port),
                cs_txt,
                f"Current state must reference port {service.port} ({service.service_id}, "
                "from ecosystem.json)",
            )

    # ── 34. 3-Stage Diagnostic Intake Protocol Integrity ────────────────────
    def test_three_stage_diagnostic_protocol_integrity(self):
        """Rule: AI Helper troubleshooting documentation must strictly implement the
        3-Stage Diagnostic Protocol with epistemic tags."""
        html_diag = os.path.join(
            self.docs_root, "papers", "ai-helper-troubleshooting-knowledge.html"
        )
        md_diag = os.path.join(
            self.docs_root, "MD-Papers", "AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md"
        )

        for fpath in [html_diag, md_diag]:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            self.assertIn(
                "Stage 1: Initial Triage", content, f"Missing Stage 1 in {os.path.basename(fpath)}"
            )
            self.assertIn(
                "Stage 2: Targeted Diagnosis",
                content,
                f"Missing Stage 2 in {os.path.basename(fpath)}",
            )
            self.assertIn(
                "Stage 3: Bounded Remediation",
                content,
                f"Missing Stage 3 in {os.path.basename(fpath)}",
            )
            self.assertIn(
                "[CONFIRMED]", content, f"Missing [CONFIRMED] tag in {os.path.basename(fpath)}"
            )
            self.assertIn(
                "[PROBABLE]", content, f"Missing [PROBABLE] tag in {os.path.basename(fpath)}"
            )
            self.assertIn(
                "[ILLUSTRATIVE]",
                content,
                f"Missing [ILLUSTRATIVE] tag in {os.path.basename(fpath)}",
            )

    # ── 35. Evidence-Bounded Quantitative Performance Claims ─────────────────
    def test_evidence_bounded_quantitative_claims(self):
        """Rule: Quantitative acceleration claims (such as 12.5x) must specify benchmark
        conditions and baseline metrics."""
        html_cs = os.path.join(self.docs_root, "papers", "current-state.html")
        md_cs = os.path.join(self.docs_root, "MD-Papers", "LEMGENDARY_CURRENT_STATE.md")

        for fpath in [html_cs, md_cs]:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            self.assertIn("12.5", content, f"Missing 12.5x reference in {os.path.basename(fpath)}")
            self.assertIn(
                "3.43s",
                content,
                f"12.5x speedup claim must cite 3.43s baseline in {os.path.basename(fpath)}",
            )
            self.assertIn(
                "0.27s",
                content,
                f"12.5x speedup claim must cite 0.27s result in {os.path.basename(fpath)}",
            )
            self.assertIn(
                "num_workers=0",
                content,
                "12.5x speedup claim must cite num_workers=0 condition in "
                f"{os.path.basename(fpath)}",
            )

    # ── 37. Hub Catalog & Asset Resilience ───────────────────────────────────
    def test_hub_catalog_and_asset_resilience(self):
        """Rule: Central index.html catalog cards must link to existing pages, expose unique
        category numbers, and contain zero unvetted external asset references."""
        with open(self.index_html, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        card_hrefs = re.findall(r'href="([^"]+)"\s+class="hub-card"', content)
        self.assertEqual(len(card_hrefs), 14, f"Expected 14 catalog cards, found {len(card_hrefs)}")
        for href in card_hrefs:
            target_path = os.path.join(self.docs_root, href.replace("/", os.sep))
            self.assertTrue(
                os.path.exists(target_path),
                f"Catalog card href {href} does not exist at {target_path}",
            )

        cat_nums = re.findall(r'<span class="category-num">(CAT\.\s*\d+[^<]*)</span>', content)
        self.assertEqual(len(cat_nums), 14, f"Expected 14 category badges, found {len(cat_nums)}")
        self.assertEqual(len(set(cat_nums)), 14, f"Duplicate category badges found: {cat_nums}")

        unvetted_cdns = ["iconscout.com", "unsplash.com", "placeholder.com"]
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            for cdn in unvetted_cdns:
                if cdn in txt:
                    failures.append((os.path.basename(path), cdn))
        self.assertEqual(len(failures), 0, f"Unvetted external CDN references found: {failures}")

    # ── 38. HTML & Markdown Companion Parity ─────────────────────────────────
    def test_html_markdown_companion_parity(self):
        """Rule: All standalone HTML publications in papers/ must maintain a 1-to-1 synchronized
        Markdown companion in MD-Papers/."""
        with open(
            os.path.join(self.docs_root, "manifest", "documents.json"), "r", encoding="utf-8"
        ) as f:
            documents = json.load(f)["documents"]
        html_files = sorted(
            os.path.basename(p) for p in glob.glob(os.path.join(self.docs_root, "papers", "*.html"))
        )
        canonical_map = {
            os.path.basename(d["html_path"]): os.path.basename(d["md_path"]) for d in documents
        }

        self.assertEqual(
            html_files,
            sorted(canonical_map),
            "Every HTML publication must be listed in the manifest",
        )
        missing_md = [
            (h_name, m_name)
            for h_name, m_name in canonical_map.items()
            if not os.path.isfile(os.path.join(self.docs_root, "MD-Papers", m_name))
        ]
        self.assertEqual(len(missing_md), 0, f"Missing Markdown companion files: {missing_md}")


if __name__ == "__main__":
    unittest.main()
