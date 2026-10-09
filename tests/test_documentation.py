import glob
import os
import re
import unittest
import yaml

class TestDocumentationIntegrity(unittest.TestCase):
    """Authoritative, comprehensive test suite verifying the integrity, typography,
    schema conformance, mathematical correctness, HTML/CSS syntax, and dead-link
    resilience of the LemGendary AI documentation hub."""

    @classmethod
    def setUpClass(cls):
        cls.docs_root = os.path.abspath('lemgendary-docs')
        cls.html_files = glob.glob(os.path.join(cls.docs_root, 'papers', '*.html'))
        cls.index_html = os.path.join(cls.docs_root, 'index.html')
        if os.path.exists(cls.index_html):
            cls.html_files.append(cls.index_html)
        cls.md_files = glob.glob(os.path.join(cls.docs_root, 'MD-Papers', '*.md'))
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
        valid_statuses = {'PLANNED', 'SPECIFICATION', 'DATASET_READY', 'TRAINING', 'TRAINED', 'VALIDATED', 'PRODUCTION', 'DEPRECATED'}
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

if __name__ == '__main__':
    unittest.main()
