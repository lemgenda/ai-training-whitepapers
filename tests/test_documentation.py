import glob
import json
import os
import re
import unittest
from html.parser import HTMLParser

import yaml


class TestDocumentationIntegrity(unittest.TestCase):
    """Authoritative, comprehensive test suite verifying the integrity, typography,
    schema conformance, mathematical correctness, HTML/CSS syntax, and dead-link
    resilience of the LemGendary AI documentation hub."""

    @classmethod
    def setUpClass(cls):
        cls.docs_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        cls.workspace_root = os.path.abspath(os.path.join(cls.docs_root, '..'))
        cls.html_files = glob.glob(os.path.join(cls.docs_root, 'papers', '*.html'))
        cls.index_html = os.path.join(cls.docs_root, 'index.html')
        if os.path.exists(cls.index_html):
            cls.html_files.append(cls.index_html)
        cls.md_files = glob.glob(os.path.join(cls.docs_root, 'MD-Papers', '*.md'))
        cls.manifest_path = os.path.join(cls.workspace_root, 'lemgendary-training-suite', 'unified_models_v2.yaml')
        if not os.path.exists(cls.manifest_path):
            cls.manifest_path = os.path.abspath('lemgendary-training-suite/unified_models_v2.yaml')
        with open(cls.manifest_path, 'r', encoding='utf-8') as f:
            cls.manifest = yaml.safe_load(f)

    # ── 1. Zero Emoji Rule ───────────────────────────────────────────────────
    def test_zero_emojis(self):
        """Rule: Strict zero emojis across all documentation files."""
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            matches = emoji_pattern.findall(content)
            if matches:
                failures.append((os.path.basename(path), set(matches)))
        self.assertEqual(len(failures), 0, f"Found emojis in documentation: {failures}")

    # ── 2. Control Characters Rule ───────────────────────────────────────────
    def test_no_control_characters(self):
        """Rule: Zero raw ASCII control characters (\\x07, \\x08, \\x0b, \\x0c)."""
        ctrl_pat = re.compile(r'[\x07\x08\x0b\x0c]')
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if ctrl_pat.search(content):
                failures.append(os.path.basename(path))
        self.assertEqual(len(failures), 0, f"Found control characters in: {failures}")

    # ── 3. Mathematical & LaTeX Integrity ───────────────────────────────────
    def test_latex_integrity(self):
        """Rule: No escape-truncated broken LaTeX primitives."""
        broken_pats = [
            (re.compile(r'(?<![a-zA-Z\\])ext\{'), r'\text{'),
            (re.compile(r'(?<![a-zA-Z\\])rac\{'), r'\frac{'),
            (re.compile(r'(?<![a-zA-Z\\])heta(?![a-zA-Z])'), r'\theta'),
            (re.compile(r'(?<![a-zA-Z\\])imes(?![a-zA-Z])'), r'\times'),
            (re.compile(r'(?<![a-zA-Z\\])abla(?![a-zA-Z])'), r'\nabla'),
            (re.compile(r'C pprox 6ND'), r'C \approx 6ND'),
        ]
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for pat, desc in broken_pats:
                if pat.search(content):
                    failures.append((os.path.basename(path), desc))
        self.assertEqual(len(failures), 0, f"Broken LaTeX expressions detected: {failures}")

    # ── 4. Technical Guarantee Qualification ────────────────────────────────
    def test_no_absolute_guarantees(self):
        """Rule: Absolute marketing claims must be replaced with bounded engineering terms."""
        forbidden = [
            'structurally impossible',
            'OOM crashes structurally impossible',
            '100% checkpoint compatibility',
            'zero-latency shader execution'
        ]
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for claim in forbidden:
                if claim.lower() in content.lower():
                    failures.append((os.path.basename(path), claim))
        self.assertEqual(len(failures), 0, f"Absolute guarantees found: {failures}")

    # ── 5. HTML Structural & W3C Standard Validation ─────────────────────────
    def test_html_structural_validation(self):
        """Rule: Every HTML file must have DOCTYPE, html, head, title, viewport, and balanced key tags."""
        failures = []
        for path in self.html_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                txt = f.read()
            fname = os.path.basename(path)

            if not txt.strip().startswith('<!DOCTYPE html>'):
                failures.append((fname, "Missing <!DOCTYPE html>"))
            if '<html' not in txt or '</html>' not in txt:
                failures.append((fname, "Missing <html> or </html>"))
            if '<head>' not in txt and '<head ' not in txt:
                failures.append((fname, "Missing <head>"))
            if '<title>' not in txt:
                failures.append((fname, "Missing <title>"))
            if 'name="viewport"' not in txt and "name='viewport'" not in txt:
                failures.append((fname, "Missing viewport meta tag"))

            # Tag balance checks for critical blocks
            for tag in ['div', 'section', 'table', 'ul', 'ol']:
                open_count = len(re.findall(rf'<{tag}\b[^>]*>', txt, re.IGNORECASE))
                close_count = len(re.findall(rf'</{tag}>', txt, re.IGNORECASE))
                if open_count != close_count:
                    failures.append((fname, f"Tag mismatch <{tag}>: {open_count} open vs {close_count} closed"))

        self.assertEqual(len(failures), 0, f"HTML structural failures: {failures}")

    # ── 6. CSS Syntax & Integrity ───────────────────────────────────────────
    def test_css_syntax_integrity(self):
        """Rule: Master style.css must exist, have balanced braces, and valid rules."""
        css_path = os.path.join(self.docs_root, 'style.css')
        self.assertTrue(os.path.exists(css_path), "style.css missing in lemgendary-docs")
        with open(css_path, 'r', encoding='utf-8', errors='ignore') as f:
            css = f.read()
        open_braces = css.count('{')
        close_braces = css.count('}')
        self.assertEqual(open_braces, close_braces, f"CSS brace mismatch: {open_braces} open vs {close_braces} closed")
        self.assertNotIn('\x00', css, "Null byte in CSS")

    # ── 7. Internal Link & Asset Integrity ──────────────────────────────────
    def test_html_internal_links_exist(self):
        """Rule: All relative href and src links in HTML files must point to existing files."""
        link_failures = []
        for path in self.html_files:
            doc_dir = os.path.dirname(path)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                txt = f.read()

            # Find href links (excluding external http/https, hashes #, and mailto)
            hrefs = re.findall(r'href=["\']([^"\']+)["\']', txt)
            for href in hrefs:
                if href.startswith(('http://', 'https://', '#', 'mailto:', 'javascript:')):
                    continue
                clean_href = href.split('#')[0].split('?')[0]
                if not clean_href:
                    continue
                target = os.path.normpath(os.path.join(doc_dir, clean_href))
                if not os.path.exists(target):
                    link_failures.append((os.path.basename(path), href, target))

            # Find src assets
            srcs = re.findall(r'src=["\']([^"\']+)["\']', txt)
            for src in srcs:
                if src.startswith(('http://', 'https://', 'data:')):
                    continue
                clean_src = src.split('?')[0]
                target = os.path.normpath(os.path.join(doc_dir, clean_src))
                if not os.path.exists(target):
                    link_failures.append((os.path.basename(path), src, target))

        self.assertEqual(len(link_failures), 0, f"Dead internal links detected: {link_failures}")

    # ── 8. Markdown Structure & Code Block Balance ───────────────────────────
    def test_markdown_structure_and_fenced_blocks(self):
        """Rule: Every markdown paper must start with an H1 (# Title) and have closed code fences."""
        failures = []
        for path in self.md_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                txt = f.read()
            fname = os.path.basename(path)

            lines = [line.strip() for line in txt.splitlines() if line.strip() and not line.strip().startswith('<!--')]
            if not lines or not lines[0].startswith('# '):
                failures.append((fname, "Does not start with H1 '# Title'"))

            # Code fence balance
            fence_count = len(re.findall(r'^```', txt, re.MULTILINE))
            if fence_count % 2 != 0:
                failures.append((fname, f"Unbalanced fenced code blocks (count: {fence_count})"))

        self.assertEqual(len(failures), 0, f"Markdown formatting issues: {failures}")

    # ── 9. Index Hub Registration ───────────────────────────────────────────
    def test_index_hub_includes_all_master_categories(self):
        """Rule: Central index.html must register all major category portals (Cat 00 through Cat 13)."""
        with open(self.index_html, 'r', encoding='utf-8', errors='ignore') as f:
            index_txt = f.read()

        required_categories = [
            'papers/general-ai-training-knowledge.html',
            'papers/ecosystem-architecture.html',
            'papers/training-pathology.html',
            'papers/manuals-hub.html',
            'papers/restoration-master.html',
            'papers/universal-hybrid.html',
            'papers/ultrazoom.html',
            'papers/nima-master.html',
            'papers/face-suite.html',
            'papers/detection-master.html',
            'papers/foundation-models-master.html',
            'papers/forex_predictor.html',
            'papers/glossary.html',
            'papers/ai-helper-troubleshooting-knowledge.html'
        ]
        missing = [cat for cat in required_categories if cat not in index_txt]
        self.assertEqual(len(missing), 0, f"Index hub missing registrations: {missing}")

    # ── 10. SSOT Manifest Parity ────────────────────────────────────────────
    def test_ssot_manifest_conformance(self):
        """Rule: Registered model keys and canonical status values conform to unified_models_v2.yaml."""
        valid_statuses = {
            'PLANNED', 'SPECIFICATION', 'DATASET_READY', 'TRAINING',
            'TRAINED', 'VALIDATED', 'PRODUCTION', 'DEPRECATED'
        }
        for k, v in self.manifest.items():
            if isinstance(v, dict) and 'status' in v:
                self.assertIn(v['status'].upper(), valid_statuses, f"Model {k} has non-canonical status {v['status']}")

    # ── 11. Model Whitepaper Canonical Topology ──────────────────────────────
    def test_model_whitepaper_canonical_topology(self):
        """Rule: All 19 model whitepapers must follow canonical 8-section topology."""
        expected_sections = ['1', '1.1', '2', '3', '4', '5', '6', '7', '8']
        model_names = [
            'nafnet', 'mprnet', 'mirnet', 'ffanet', 'face-codeformer', 'face-parsenet',
            'face-retinaface', 'detection-yolov8n', 'ultrazoom', 'hybrid-upn-v2',
            'hybrid-film-restorer', 'forex_predictor', 'nima-mobile', 'nima-efficientnet',
            'nima-pro', 'nima-technical', 'nima-authenticity', 'classification-nsfw',
            'hybrid-multitask'
        ]
        failures = []
        for name in model_names:
            h_path = os.path.join(self.docs_root, 'papers', f'{name}.html')
            if not os.path.exists(h_path):
                failures.append((name, "File missing"))
                continue
            with open(h_path, 'r', encoding='utf-8') as f:
                content = f.read()
            secs = [m.group(1).rstrip('.') for m in re.finditer(r'<h2[^>]*>\s*([0-9]+(?:\.[0-9]+)?)\.?', content)]
            if secs != expected_sections:
                failures.append((name, f"Got sections: {secs}"))
        self.assertEqual(len(failures), 0, f"Topology mismatches: {failures}")

    # ── 12. Epistemic Claim Tags ────────────────────────────────────────────
    def test_epistemic_claim_tags(self):
        """Rule: Every model whitepaper must have >= 4 epistemic tags matching between HTML and MD."""
        model_pairs = [
            ('nafnet.html', 'PAPER_LEMGENDARY_NAFNET.md'),
            ('mprnet.html', 'PAPER_LEMGENDARY_MPRNET.md'),
            ('mirnet.html', 'PAPER_LEMGENDARY_MIRNET.md'),
            ('ffanet.html', 'PAPER_LEMGENDARY_FFANET.md'),
            ('face-codeformer.html', 'PAPER_LEMGENDARY_CODEFORMER.md'),
            ('face-parsenet.html', 'PAPER_LEMGENDARY_PARSENET.md'),
            ('face-retinaface.html', 'PAPER_LEMGENDARY_RETINAFACE.md'),
            ('detection-yolov8n.html', 'PAPER_LEMGENDARY_YOLOV8N.md'),
            ('ultrazoom.html', 'PAPER_LEMGENDARY_ULTRAZOOM.md'),
            ('hybrid-upn-v2.html', 'PAPER_LEMGENDARY_UPN_V2.md'),
            ('hybrid-film-restorer.html', 'PAPER_LEMGENDARY_FILM_RESTORER.md'),
            ('forex_predictor.html', 'PAPER_FOREX_PREDICTOR.md'),
            ('nima-mobile.html', 'PAPER_NIMA_MOBILE.md'),
            ('nima-efficientnet.html', 'PAPER_NIMA_EFFICIENTNET.md'),
            ('nima-pro.html', 'PAPER_NIMA_PRO.md'),
            ('nima-technical.html', 'PAPER_NIMA_TECHNICAL.md'),
            ('nima-authenticity.html', 'PAPER_NIMA_AUTHENTICITY.md'),
            ('classification-nsfw.html', 'PAPER_LEMGENDARY_NSFW_CLASSIFIER.md'),
            ('hybrid-multitask.html', 'PAPER_LEMGENDARY_MULTITASK.md'),
        ]
        failures = []
        for h_name, m_name in model_pairs:
            hp = os.path.join(self.docs_root, 'papers', h_name)
            mp = os.path.join(self.docs_root, 'MD-Papers', m_name)
            with open(hp, 'r', encoding='utf-8') as f:
                h_content = f.read()
            with open(mp, 'r', encoding='utf-8') as f:
                m_content = f.read()
            h_tags = set(re.findall(r'\[(THEORETICAL|MEASURED|TARGET|CURRENT|DESIGN_GOAL)\]', h_content))
            m_tags = set(re.findall(r'\[(THEORETICAL|MEASURED|TARGET|CURRENT|DESIGN_GOAL)\]', m_content))
            if len(h_tags) < 4 or len(m_tags) < 4 or h_tags != m_tags:
                failures.append((h_name, f"H:{len(h_tags)} M:{len(m_tags)}"))
        self.assertEqual(len(failures), 0, f"Epistemic tag failures: {failures}")

    # ── 13. AI Helper Training Corpus Integrity ─────────────────────────────
    def test_ai_helper_corpus_integrity(self):
        """Rule: AI Helper JSONL corpus must exist, parse cleanly, obey zero-emojis,
        strictly align with unified_models_v2.yaml SSOT, and maintain balanced validation coverage."""
        corpus_dir = os.path.abspath(
            os.path.join(self.docs_root, '..', 'LemGendaryDatasets', 'LemGendizedAIHelperLemGend')
        )
        if not os.path.exists(corpus_dir):
            corpus_dir = os.path.abspath(
                os.path.join(self.docs_root, '..', 'LemGendaryDatasets', 'LemGendizedAIHelperCorpus')
            )
        train_path = os.path.join(corpus_dir, 'ai_helper_train.jsonl')
        val_path = os.path.join(corpus_dir, 'ai_helper_val.jsonl')

        self.assertTrue(os.path.exists(train_path), "ai_helper_train.jsonl missing")
        self.assertTrue(os.path.exists(val_path), "ai_helper_val.jsonl missing")

        train_records = []
        with open(train_path, 'r', encoding='utf-8') as f:
            for line_idx, line in enumerate(f, 1):
                try:
                    train_records.append(json.loads(line))
                except Exception as e:
                    self.fail(f"Malformed JSON on line {line_idx} of ai_helper_train.jsonl: {e}")

        val_records = []
        with open(val_path, 'r', encoding='utf-8') as f:
            for line_idx, line in enumerate(f, 1):
                try:
                    val_records.append(json.loads(line))
                except Exception as e:
                    self.fail(f"Malformed JSON on line {line_idx} of ai_helper_val.jsonl: {e}")

        all_records = train_records + val_records
        all_ids = [r['id'] for r in all_records]
        self.assertEqual(len(all_ids), len(set(all_ids)), "Duplicate IDs found in corpus")

        emoji_pat = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        for r in all_records:
            text = " ".join(m["content"] for m in r["messages"])
            self.assertEqual(len(emoji_pat.findall(text)), 0, f"Emoji detected in {r['id']}")

            # Verify NIMA mobile backbone SSOT
            if "nima_aesthetic_mobile" in text.lower():
                self.assertFalse(
                    bool(re.search(r'nima_aesthetic_mobile.*MobileNetV[12]', text, re.IGNORECASE)),
                    f"Corpus {r['id']} claimed legacy MobileNet for NIMA Mobile instead of MobileNetV3-Small"
                )

            # Verify no invalid endpoint routes
            self.assertNotIn("POST /api/compile\n", text)
            self.assertNotIn("/api/ws/telemetry", text)
            self.assertNotIn("lem-env training", text)
            self.assertNotIn("lem-env datasets", text)
            self.assertNotIn("default: 1000", text)

        # Check validation set coverage across all required categories
        val_categories = {r['category'] for r in val_records}
        required_categories = {
            'gui_procedure', 'cli_procedure', 'api_procedure',
            'troubleshooting_diagnostics', 'model_selection',
            'unsupported_and_negative', 'cross_document_pipeline'
        }
        missing = required_categories - val_categories
        self.assertEqual(len(missing), 0, f"Held-out validation set missing categories: {missing}")

    # ── 14. Global Category Taxonomy Uniqueness ──────────────────────────────
    def test_category_taxonomy_uniqueness(self):
        """Rule: Category identifiers must be globally unambiguous and unique across the hub."""
        # GUI Control Registry must be Category 03.4 CONTROLS (not colliding with Category 04 Restoration)
        gui_registry_html = os.path.join(self.docs_root, 'papers', 'gui-control-registry.html')
        if os.path.exists(gui_registry_html):
            with open(gui_registry_html, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            self.assertNotIn(
                "Category 04 CONTROLS", content,
                "gui-control-registry.html must not use Category 04 (reserved for Restoration)"
            )
            self.assertIn(
                "Category 03.4 CONTROLS", content,
                "gui-control-registry.html must be categorized under Category 03.4 CONTROLS"
            )

        # Category 00 must be General AI Training Knowledge, not governance/operational docs
        for fname, expected_cat, forbidden_cat in [
            ('current-state.html', 'Category 01.0 STATUS', 'Category 00 STATUS'),
            ('env_manager.html', 'Category 01.1 ENV', 'Category 00 ENV'),
            ('versioning-policy.html', 'Category 01.5 POLICY', 'Category 00 POLICY')
        ]:
            fpath = os.path.join(self.docs_root, 'papers', fname)
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    c = f.read()
                self.assertNotIn(forbidden_cat, c, f"{fname} must not use {forbidden_cat}")
                self.assertIn(expected_cat, c, f"{fname} must use {expected_cat}")

    # ── 15. Deep Mathematical & LaTeX Integrity ─────────────────────────────
    def test_latex_deep_integrity(self):
        """Rule: No malformed LaTeX stems or escape-truncated Greek symbols in any HTML/MD file."""
        deep_broken_pats = [
            (re.compile(r'(?<![a-zA-Z\\])lpha\b'), 'Malformed alpha stem: "lpha"'),
            (re.compile(r'ar\{lpha\}'), 'Malformed bar-alpha: "ar{lpha}"'),
            (re.compile(r'(?<![a-zA-Z\\])ight\b'), 'Malformed right delimiter: "ight"'),
            (re.compile(r'(?<![a-zA-Z\\])egin\{'), 'Malformed begin environment: "egin{"'),
            (re.compile(r'(?<![a-zA-Z\\])ho\('), 'Malformed rho notation: "ho("'),
            (re.compile(r'(?<![a-zA-Z\\])eta\('), 'Malformed beta notation: "eta("'),
        ]
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for pat, desc in deep_broken_pats:
                if pat.search(content):
                    failures.append((os.path.basename(path), desc))
        self.assertEqual(len(failures), 0, f"Deep LaTeX integrity issues found: {failures}")

    # ── 16. No Stray HTML Syntax Fragments ───────────────────────────────────
    def test_no_stray_html_fragments(self):
        """Rule: No visible broken HTML fragments like ' /p>' or stray tags in documentation."""
        failures = []
        stray_pat = re.compile(r'(\s/p>|> /p>|\b/p>)')
        for path in self.html_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if stray_pat.search(content):
                failures.append(os.path.basename(path))
        self.assertEqual(len(failures), 0, f"Stray HTML fragments found in: {failures}")

    # ── 17. No Unsupported Operational CLI Commands ──────────────────────────
    def test_no_unsupported_cli_commands(self):
        """Rule: Documentation must never teach ungrounded/non-existent CLI commands or flags."""
        forbidden_commands = [
            '--storage uncompressed-tar',
            '--dedup phash --phash-threshold',
            'lem-env datasets compile',
            'lem-env training'
        ]
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for cmd in forbidden_commands:
                if cmd in content:
                    failures.append((os.path.basename(path), cmd))
        self.assertEqual(len(failures), 0, f"Unsupported CLI commands found in documentation: {failures}")

    # ── 18. Compiler API Contract Parity ─────────────────────────────────────
    def test_compiler_api_parity(self):
        """Rule: All documented compiler endpoints (including custom-compile) must be present in API manual."""
        api_manual_path = os.path.join(self.docs_root, 'papers', 'api-manual.html')
        api_manual_md = os.path.join(self.docs_root, 'MD-Papers', 'MANUAL_API.md')
        self.assertTrue(os.path.exists(api_manual_path), "api-manual.html missing")
        self.assertTrue(os.path.exists(api_manual_md), "MANUAL_API.md missing")

        with open(api_manual_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_txt = f.read()
        with open(api_manual_md, 'r', encoding='utf-8', errors='ignore') as f:
            md_txt = f.read()

        for route in ['/api/gui/custom-compile', '/api/gui/quick-compile', '/api/jobs/compile']:
            self.assertIn(route, html_txt, f"api-manual.html missing route {route}")
            self.assertIn(route, md_txt, f"MANUAL_API.md missing route {route}")

    # ── 19. Model Registry Specification Parity ──────────────────────────────
    def test_model_registry_specification_parity(self):
        """Rule: Current State manifest and model whitepapers must agree with canonical backbones."""
        current_state_html = os.path.join(self.docs_root, 'papers', 'current-state.html')
        self.assertTrue(os.path.exists(current_state_html), "current-state.html missing")
        with open(current_state_html, 'r', encoding='utf-8', errors='ignore') as f:
            cs_txt = f.read()

        # NIMA Aesthetic Mobile must be MobileNetV3-Small
        self.assertIn(
            "MobileNetV3-Small", cs_txt,
            "current-state.html must specify MobileNetV3-Small for nima_aesthetic_mobile"
        )
        # NIMA Technical and Authenticity must specify EfficientNetV2-S
        self.assertIn(
            "EfficientNetV2-S", cs_txt,
            "current-state.html must specify EfficientNetV2-S for technical/authenticity backbones"
        )

    # ── 20. Benchmark Evidence Condition Qualification ───────────────────────
    def test_evidence_condition_labeling(self):
        """Rule: Performance figures with multi-stage evaluations (e.g. NAFNet) must explicitly qualify conditions."""
        nafnet_html = os.path.join(self.docs_root, 'papers', 'nafnet.html')
        self.assertTrue(os.path.exists(nafnet_html), "nafnet.html missing")
        with open(nafnet_html, 'r', encoding='utf-8', errors='ignore') as f:
            txt = f.read()

        self.assertIn("51.60 dB", txt, "nafnet.html missing peak 256px metric")
        self.assertIn("48.29 dB", txt, "nafnet.html missing 640px stage metric")
        self.assertIn("256x256 ladder stage", txt, "nafnet.html missing evaluation condition qualifier for 51.60 dB")
        self.assertIn("640x640 stage", txt, "nafnet.html missing evaluation condition qualifier for 48.29 dB")

    # ── 21. Search Bar & Task-Oriented Entry Portals ───────────────────────
    def test_index_search_and_task_portals(self):
        """Rule: Central index.html must feature a live search bar and task-oriented entry portals."""
        with open(self.index_html, 'r', encoding='utf-8', errors='ignore') as f:
            txt = f.read()

        self.assertIn('id="hub-search-input"', txt, "index.html missing search input element")
        self.assertIn('id="task-portals"', txt, "index.html missing task entry portals container")
        for portal in ['getting-started', 'dataset-engineering', 'training-debugging', 'model-reference']:
            self.assertIn(f'data-filter="{portal}"', txt, f"index.html missing task portal filter {portal}")

    # ── 22. Header Authority & Version Metadata ────────────────────────────
    def test_header_version_authority_metadata(self):
        """Rule: Central index.html header must expose version, last-reviewed date, and authority status."""
        with open(self.index_html, 'r', encoding='utf-8', errors='ignore') as f:
            txt = f.read()

        self.assertIn('Version v16.9.26-STABLE', txt, "index.html missing header version metadata")
        self.assertIn('Last Reviewed:', txt, "index.html missing last-reviewed date metadata")
        self.assertIn('AUTHORITATIVE SSOT', txt, "index.html missing authoritative SSOT badge")

    # ── 23. AI Helper Knowledge Contract & Resolution Protocol ──────────────
    def test_ai_helper_knowledge_contract(self):
        """Rule: AI Helper Troubleshooting Knowledge Base must specify authority hierarchy,
        intake protocol, and admission bounds."""
        tb_md = os.path.join(self.docs_root, 'MD-Papers', 'AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md')
        tb_html = os.path.join(self.docs_root, 'papers', 'ai-helper-troubleshooting-knowledge.html')

        with open(tb_md, 'r', encoding='utf-8', errors='ignore') as f:
            md_txt = f.read()
        with open(tb_html, 'r', encoding='utf-8', errors='ignore') as f:
            html_txt = f.read()

        for content in [md_txt, html_txt]:
            self.assertIn("Authority Hierarchy", content, "Missing Authority Hierarchy section")
            self.assertIn("Mandatory Citation Policy", content, "Missing Mandatory Citation Policy")
            self.assertIn("Diagnostic Intake Protocol", content, "Missing Diagnostic Intake Protocol")
            self.assertIn("UNVERIFIED IN PUBLISHED HUB", content, "Missing Explicit Admission Bound statement")

    # ── 24. Task-Based Diagnostic Scenario Coverage ─────────────────────────
    def test_troubleshooting_task_scenarios(self):
        """Rule: AI Helper Knowledge Base must cover key real-world diagnostic failure scenarios."""
        tb_md = os.path.join(self.docs_root, 'MD-Papers', 'AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md')
        with open(tb_md, 'r', encoding='utf-8', errors='ignore') as f:
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
            "Raw Dataset vs. Compiled Manifold Path Confusion"
        ]
        for scenario in scenarios:
            self.assertIn(scenario, txt, f"Missing diagnostic scenario: {scenario}")

    # ── 25. Regex Escape Math Corruption Defense ─────────────────────────────
    def test_no_regex_escape_math_corruptions(self):
        r"""Rule: Documentation must never contain corrupted regex escapes such as '\|^2\\right]'."""
        corrupted_pat = re.compile(r'(\|\|?\^2\\right\]|\\right\]\|\|?\^2)')
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if corrupted_pat.search(content):
                failures.append(os.path.basename(path))
        self.assertEqual(len(failures), 0, f"Corrupted LaTeX escape artifacts found in: {failures}")

    # ── 26. Global Category Taxonomy Integrity ──────────────────────────────
    def test_no_category_taxonomy_drift(self):
        """Rule: Documentation must adhere to canonical Category 00 through 13 taxonomy with zero Category 15 drift."""
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if "Category 15" in content or "CATEGORY 15" in content:
                failures.append(os.path.basename(path))
        self.assertEqual(len(failures), 0, f"Drifted Category 15 found in: {failures}")

    # ── 27. Canonical Author Standardization ─────────────────────────────────
    def test_canonical_author_standardization(self):
        """Rule: Author name must be consistently standardized as 'Lem Treursic' without diacritic variants."""
        failures = []
        for path in self.html_files + self.md_files:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if "Lem Treursić" in content:
                failures.append(os.path.basename(path))
        self.assertEqual(len(failures), 0, f"Non-canonical author spelling 'Lem Treursić' found in: {failures}")

    # ── 28. SwiGLU Architectural Formulation Integrity ──────────────────────
    def test_swiglu_equation_integrity(self):
        """Rule: SwiGLU formula must explicitly project inputs through independent gate (W_1)
        and value (W_2) matrices."""
        llm_html = os.path.join(self.docs_root, 'papers', 'foundation-llm.html')
        llm_md = os.path.join(self.docs_root, 'MD-Papers', 'PAPER_LEMGENDARY_LLM.md')
        for fpath in [llm_html, llm_md]:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                txt = f.read()
            self.assertIn("W_1", txt, f"Missing W_1 gate projection in {os.path.basename(fpath)}")
            self.assertIn("W_2", txt, f"Missing W_2 value projection in {os.path.basename(fpath)}")
            self.assertNotIn(
                "(x W_1 \\odot \\sigma(x W_1)) W_2", txt,
                f"Degenerate non-gated SwiGLU found in {os.path.basename(fpath)}"
            )

    # ── 29. VLM Cross-Entropy Equation Integrity ────────────────────────────
    def test_vlm_cross_entropy_equation_integrity(self):
        """Rule: VLM cross-entropy loss must escape less-than operators to prevent HTML tag truncation."""
        vlm_html = os.path.join(self.docs_root, 'papers', 'foundation-image-to-text.html')
        vlm_md = os.path.join(self.docs_root, 'MD-Papers', 'PAPER_LEMGENDARY_IMAGE_TO_TEXT.md')
        for fpath in [vlm_html, vlm_md]:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                txt = f.read()
            self.assertNotIn(
                "w_{<t}", txt,
                f"Unescaped w_{{<t}} causing HTML tag truncation in {os.path.basename(fpath)}"
            )
            self.assertIn("w_{\\lt t}", txt, f"Expected w_{{\\lt t}} in {os.path.basename(fpath)}")

    # ── 30. Hub Index Branding Consistency ──────────────────────────────────
    def test_hub_index_branding_consistency(self):
        """Rule: Hub index must consistently use 'LemGendary AI' for product and copyright branding."""
        index_html = os.path.join(self.docs_root, 'index.html')
        with open(index_html, 'r', encoding='utf-8', errors='ignore') as f:
            txt = f.read()
        self.assertNotIn('alt="LemGenda"', txt, "Index logo alt text should be 'LemGendary AI'")
        self.assertNotIn('&copy; 2026 LemGenda AI Hub', txt, "Index copyright should be 'LemGendary AI Hub'")
        self.assertIn('&copy; 2026 LemGendary AI Hub', txt, "Missing canonical 'LemGendary AI Hub' copyright")

    # ── 31. Universal LaTeX Formula & Tag Integrity ──────────────────────────
    def test_universal_latex_formula_and_tag_integrity(self):
        """Rule: All LaTeX blocks across all publications must have balanced delimiters,
        braces, and 0 unescaped HTML tags."""
        patterns = [
            re.compile(r'\$\$([\s\S]*?)\$\$'),
            re.compile(r'\\\[([\s\S]*?)\\\]'),
            re.compile(r'\\\(([\s\S]*?)\\\)')
        ]
        failures = []
        for fpath in self.html_files:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for regex in patterns:
                for match in regex.finditer(content):
                    math_text = match.group(1).strip()
                    if re.search(r'<[a-zA-Z/][^>]*>', math_text):
                        failures.append(f"{os.path.basename(fpath)}: HTML tag inside math block: {math_text[:50]}")
                    n_left = len(re.findall(r'\\left(?![a-zA-Z])', math_text))
                    n_right = len(re.findall(r'\\right(?![a-zA-Z])', math_text))
                    if n_left != n_right:
                        failures.append(f"{os.path.basename(fpath)}: Unbalanced \\left/\\right ({n_left} vs {n_right})")
                    if math_text.count('{') != math_text.count('}'):
                        failures.append(f"{os.path.basename(fpath)}: Unbalanced braces in math block")
        self.assertEqual(len(failures), 0, f"Universal LaTeX integrity violations: {failures}")

    # ── 32. HTML Parser Tag Hierarchy Integrity ─────────────────────────────
    def test_html_parser_tag_integrity(self):
        """Rule: All HTML files must parse cleanly with zero unescaped tags or unclosed major containers."""
        valid_tags = {
            'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdi', 'bdo',
            'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup',
            'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'embed',
            'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'head', 'header', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'legend',
            'li', 'link', 'main', 'map', 'mark', 'meta', 'meter', 'nav', 'noscript', 'object', 'ol',
            'optgroup', 'option', 'output', 'p', 'param', 'picture', 'pre', 'progress', 'q', 'rp', 'rt',
            'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strong', 'style',
            'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th',
            'thead', 'time', 'title', 'tr', 'track', 'u', 'ul', 'var', 'video', 'wbr', 'circle', 'line',
            'path', 'rect', 'polygon', 'polyline', 'text', 'g', 'defs', 'clippath', 'use'
        }

        class StrictValidator(HTMLParser):
            def __init__(self, filename):
                super().__init__()
                self.filename = filename
                self.errors = []
                self.stack = []
                self.void_tags = {
                    'meta', 'link', 'img', 'br', 'hr', 'input', 'area', 'base', 'col',
                    'embed', 'param', 'source', 'track', 'wbr'
                }

            def handle_starttag(self, tag, attrs):
                t = tag.lower()
                if t not in valid_tags:
                    self.errors.append(f'Unescaped or invalid tag <{tag}> at line {self.getpos()[0]}')
                if t not in self.void_tags:
                    self.stack.append((t, self.getpos()))

            def handle_endtag(self, tag):
                t = tag.lower()
                if t in self.void_tags:
                    return
                if not self.stack:
                    self.errors.append(f'Stray closing </{tag}> at line {self.getpos()[0]}')
                    return
                while self.stack:
                    top_tag, pos = self.stack.pop()
                    if top_tag == t:
                        return
                    if top_tag in {
                        'html', 'head', 'body', 'main', 'nav', 'header', 'footer',
                        'table', 'thead', 'tbody', 'section'
                    }:
                        self.errors.append(
                            f'Unclosed major tag <{top_tag}> from line {pos[0]} '
                            f'when encountering </{tag}> at line {self.getpos()[0]}'
                        )
                        return

        all_errors = []
        for path in self.html_files:
            validator = StrictValidator(path)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                validator.feed(f.read())
            if validator.errors:
                all_errors.append(f"{os.path.basename(path)}: {validator.errors}")
        self.assertEqual(len(all_errors), 0, f"HTML parser tag integrity failures: {all_errors}")

    # ── 33. Cross-Repository Runtime & Manifest Consistency ─────────────────
    def test_cross_repo_manifest_and_runtime_consistency(self):
        """Rule: Model identifiers in unified_models_v2.yaml and sidecar ports (8000, 8100, 8200)
        must match documentation."""
        models = [k for k in self.manifest.keys() if not k.startswith('_')]
        self.assertGreater(len(models), 10, "unified_models_v2.yaml must declare model definitions")

        # Verify port bindings in authoritative documents
        current_state_path = os.path.join(self.docs_root, 'papers', 'current-state.html')
        with open(current_state_path, 'r', encoding='utf-8', errors='ignore') as f:
            cs_txt = f.read()
        self.assertIn("8000", cs_txt, "Current state must reference Port 8000 (Training Suite)")
        self.assertIn("8100", cs_txt, "Current state must reference Port 8100 (Env Manager)")
        self.assertIn("8200", cs_txt, "Current state must reference Port 8200 (Dataset Compiler)")

    # ── 34. 3-Stage Diagnostic Intake Protocol Integrity ────────────────────
    def test_three_stage_diagnostic_protocol_integrity(self):
        """Rule: AI Helper troubleshooting documentation must strictly implement the
        3-Stage Diagnostic Protocol with epistemic tags."""
        html_diag = os.path.join(self.docs_root, 'papers', 'ai-helper-troubleshooting-knowledge.html')
        md_diag = os.path.join(self.docs_root, 'MD-Papers', 'AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md')

        for fpath in [html_diag, md_diag]:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            self.assertIn("Stage 1: Initial Triage", content, f"Missing Stage 1 in {os.path.basename(fpath)}")
            self.assertIn("Stage 2: Targeted Diagnosis", content, f"Missing Stage 2 in {os.path.basename(fpath)}")
            self.assertIn("Stage 3: Bounded Remediation", content, f"Missing Stage 3 in {os.path.basename(fpath)}")
            self.assertIn("[CONFIRMED]", content, f"Missing [CONFIRMED] tag in {os.path.basename(fpath)}")
            self.assertIn("[PROBABLE]", content, f"Missing [PROBABLE] tag in {os.path.basename(fpath)}")
            self.assertIn("[ILLUSTRATIVE]", content, f"Missing [ILLUSTRATIVE] tag in {os.path.basename(fpath)}")

    # ── 35. Evidence-Bounded Quantitative Performance Claims ─────────────────
    def test_evidence_bounded_quantitative_claims(self):
        """Rule: Quantitative acceleration claims (such as 12.5x) must specify benchmark
        conditions and baseline metrics."""
        html_cs = os.path.join(self.docs_root, 'papers', 'current-state.html')
        md_cs = os.path.join(self.docs_root, 'MD-Papers', 'LEMGENDARY_CURRENT_STATE.md')

        for fpath in [html_cs, md_cs]:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            self.assertIn("12.5", content, f"Missing 12.5x reference in {os.path.basename(fpath)}")
            self.assertIn(
                "3.43s", content,
                f"12.5x speedup claim must cite 3.43s baseline in {os.path.basename(fpath)}"
            )
            self.assertIn(
                "0.27s", content,
                f"12.5x speedup claim must cite 0.27s result in {os.path.basename(fpath)}"
            )
            self.assertIn(
                "num_workers=0", content,
                f"12.5x speedup claim must cite num_workers=0 condition in {os.path.basename(fpath)}"
            )

    # ── 36. AI Helper Dataset Schema & Split Integrity ───────────────────────
    def test_ai_helper_dataset_integrity(self):
        """Rule: ai_helper_train.jsonl and ai_helper_val.jsonl must have valid schemas, zero overlap, and 0 emojis."""
        dataset_dir = os.path.join(self.workspace_root, 'LemGendaryDatasets', 'LemGendizedAIHelperLemGend')
        train_path = os.path.join(dataset_dir, 'ai_helper_train.jsonl')
        val_path = os.path.join(dataset_dir, 'ai_helper_val.jsonl')

        if not os.path.exists(train_path) or not os.path.exists(val_path):
            return  # Skip if dataset directory is not located at expected path

        train_ids = set()
        val_ids = set()
        emoji_pat = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)

        for p, id_set in [(train_path, train_ids), (val_path, val_ids)]:
            with open(p, 'r', encoding='utf-8') as f:
                for line_idx, line in enumerate(f):
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    self.assertIn('id', rec, f"Missing 'id' at line {line_idx+1} in {os.path.basename(p)}")
                    self.assertIn('category', rec, f"Missing 'category' at line {line_idx+1} in {os.path.basename(p)}")
                    self.assertIn('messages', rec, f"Missing 'messages' at line {line_idx+1} in {os.path.basename(p)}")
                    self.assertEqual(
                        len(rec['messages']), 3,
                        f"Expected 3 messages (system, user, assistant) in {rec['id']}"
                    )
                    id_set.add(rec['id'])
                    self.assertFalse(emoji_pat.search(line), f"Found emoji in {os.path.basename(p)} record {rec['id']}")

        overlap = train_ids.intersection(val_ids)
        self.assertEqual(len(overlap), 0, f"Train and validation splits share duplicate IDs: {overlap}")
        self.assertGreaterEqual(
            len(val_ids), 25,
            "Held-out validation set must contain >= 25 records for robust evaluation"
        )

        # Verify metadata synchronization and purge of irrelevant lineage
        info_path = os.path.join(dataset_dir, 'dataset_info.yaml')
        meta_path = os.path.join(dataset_dir, 'dataset-metadata.json')
        readme_path = os.path.join(dataset_dir, 'README.md')

        for fpath in [info_path, meta_path, readme_path]:
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding='utf-8') as f:
                    txt = f.read()
                self.assertNotIn(
                    "Rain Streaks", txt,
                    f"Found irrelevant 'Rain Streaks' lineage in {os.path.basename(fpath)}"
                )
                self.assertNotIn(
                    "Parquet feature tensors", txt,
                    f"Found stale Parquet description in {os.path.basename(fpath)}"
                )

        if os.path.exists(info_path):
            with open(info_path, 'r', encoding='utf-8') as f:
                info_data = yaml.safe_load(f)
            self.assertEqual(info_data.get('train_samples'), len(train_ids), "dataset_info.yaml train count mismatch")
            self.assertEqual(info_data.get('val_samples'), len(val_ids), "dataset_info.yaml val count mismatch")
            self.assertEqual(
                info_data.get('count'), len(train_ids) + len(val_ids),
                "dataset_info.yaml total count mismatch"
            )

if __name__ == '__main__':
    unittest.main()


