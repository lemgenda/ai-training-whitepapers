# LemGendary AI Documentation Hub - Lead Documentation Review Report

- **Project:** LemGendary AI Documentation Hub (`./lemgendary-docs/`)
- **Review type:** Read-only lead documentation review (no repository files
  modified other than this report)
- **Review date:** 2026-11-02
- **Governance baseline:** `../ROBOTS.md` (supreme), `../Instructions.md`
- **Scope:** 48 Markdown sources in `MD-Papers/`, 48 HTML publications in
  `papers/`, `index.html`, `manifest/documents.json`,
  `canonical_capabilities.json` / `.yaml`, `scripts/`, `tests/`, `assets/`,
  `README.md`, `INVESTOR_STRATEGY_LEMGENDARY_2026.md`

## Executive Findings

### Headline Numbers

| Metric | Result |
| --- | --- |
| MD / HTML / manifest entries | 48 / 48 / 48 (1:1, zero orphans) |
| Pairs fully in sync (headings and text) | 5 of 48 |
| Pairs with heading drift greater than 1 | 33 of 48 (236 headings) |
| Pairs with text similarity below 0.85 | 18 of 48 |
| H1 title mismatches MD vs HTML | 41 of 48 |
| Version consistent (manifest = MD = HTML) | 4 of 48 |
| markdownlint (inline suppressions honoured) | 2025 errors, 16 files |
| markdownlint (suppressions ignored) | 3647 errors, 50 files |
| Files with inline `markdownlint-disable` | 34 of 48 MD sources |
| W3C Nu validator (vnu) | 5 errors (4 files), 16 warnings |
| HTML template compliance | 0 of 49 HTML files |
| Broken MD TOC fragments (MD051) | 49 in 15 files |
| Broken HTML in-page anchors | 4 (`ultrazoom.html`) |
| Broken relative links (MD) | 4 (`MANUAL_API.md`, `MANUAL_CLI.md`) |
| Absolute paths | 8 occurrences in 7 files |
| JSON vs YAML capability registry | Semantically identical |
| Test suite (`tests/test_documentation.py`) | 37 passed, 1 failed |
| Repository audit scripts | 0 discrepancies (false negative) |

### Strengths

- Inventory is complete and bijective: every Markdown source has exactly one
  HTML counterpart and one manifest entry; manifest `id` equals the HTML
  file stem for all 48 entries; every publication is reachable from
  `index.html` (14 hub cards plus hub sub-navigation).
- `canonical_capabilities.json` and `canonical_capabilities.yaml` are
  semantically identical (0 differences after parsing both).
- The capability registry matches the LemGendary Model Training Suite
  registry (`unified_models_v2.yaml`): 23 of 23 model identifiers.
- Sidecar ports (LemGendary Environment Manager 8000, LemGendary Dataset
  Compiler Suite 8100, LemGendary Model Training Suite 8200) agree across
  the registry, whitepapers and code in all four sibling repositories.
- No duplicate HTML `id` attributes, no broken HTML relative links or
  asset references, no emoji, no broken LaTeX stems (test suite).

### Weaknesses

- MD/HTML word-for-word synchronization is not achieved: only 5 pairs are
  green; 18 pairs differ materially in text (similarity below 0.85).
- The approved HTML template (`header`, `nav.toc-sidebar`, `section`,
  `footer`) is used by none of the publications; papers use
  `div#tabs-top`, `nav#toc.toc-fixed-bar` and `main` without `header` or
  `footer`.
- 34 Markdown files contain inline `markdownlint-disable` directives and
  `.markdownlint.json` is gitignored. Both are diagnostic suppressions
  forbidden by `ROBOTS.md`.
- Version metadata is fragmented: manifest, Markdown and HTML agree on the
  version for only 4 of 48 documents.
- The repository's own parity scripts report 0 discrepancies because they
  compare only H2 counts, image sets, table counts and length ratios.

### Risks

- Readers of the HTML hub and readers of the Markdown sources receive
  different content (for example, the MD of `degradation-engine` has 1408
  words and the HTML has 452).
- The test suite pins stale values (for example `Version v16.9.27-STABLE`
  in `index.html`), so the version cannot be corrected without editing
  the test.
- The pre-commit configuration calls `verify_docs.py`, which does not
  exist in the repository.

### Opportunities

- Generate HTML from Markdown (single source of truth) instead of
  maintaining two hand-edited copies; this removes the whole drift class.
- Promote `manifest/documents.json` to the single version authority and
  render version badges from it.
- Replace the shallow parity scripts with a heading-sequence and
  text-similarity gate (the method used in this review).

## Documentation Inventory

All 48 manifest entries resolve to existing files. The HTML path is always
`papers/<ID>.html`. "Card" marks the 14 publications linked directly from
`index.html` hub cards; the other 34 are reachable through hub pages
(crawl from `index.html`: 0 unreachable pages).

| # | ID (`papers/<ID>.html`) | Card | MD hd | HTML hd | Hd drift | Words |
| -: | --- | :-: | -: | -: | -: | -: |
| 1 | `ai-helper-troubleshooting-knowledge` | Y | 23 | 23 | 1 | 0.81 |
| 2 | `ai-studio-manual` | - | 72 | 71 | 1 | 0.82 |
| 3 | `ai-studio-whitepaper` | - | 21 | 20 | 1 | 0.59 |
| 4 | `api-manual` | - | 76 | 67 | 10 | 0.86 |
| 5 | `classification-nsfw` | - | 17 | 17 | 2 | 0.94 |
| 6 | `cli-manual` | - | 55 | 54 | 2 | 0.96 |
| 7 | `current-state` | - | 12 | 11 | 1 | 0.97 |
| 8 | `dataset-compiler` | - | 74 | 73 | 10 | 0.87 |
| 9 | `degradation-engine` | - | 24 | 10 | 17 | 0.33 |
| 10 | `detection-classification` | - | 18 | 12 | 9 | 0.52 |
| 11 | `detection-master` | Y | 7 | 7 | 1 | 0.92 |
| 12 | `detection-yolov8n` | - | 26 | 24 | 11 | 0.67 |
| 13 | `ecosystem-architecture` | Y | 10 | 6 | 5 | 0.88 |
| 14 | `env_manager` | - | 16 | 15 | 2 | 0.97 |
| 15 | `face-codeformer` | - | 17 | 19 | 8 | 0.94 |
| 16 | `face-parsenet` | - | 17 | 19 | 8 | 0.92 |
| 17 | `face-retinaface` | - | 17 | 19 | 8 | 0.48 |
| 18 | `face-suite` | Y | 31 | 13 | 21 | 0.50 |
| 19 | `ffanet` | - | 34 | 34 | 1 | 0.93 |
| 20 | `forex_predictor` | Y | 46 | 45 | 5 | 0.85 |
| 21 | `foundation-diffusion` | - | 8 | 8 | 1 | 0.96 |
| 22 | `foundation-image-to-text` | - | 8 | 8 | 1 | 0.94 |
| 23 | `foundation-llm` | - | 8 | 8 | 1 | 0.96 |
| 24 | `foundation-models-master` | Y | 17 | 8 | 10 | 0.59 |
| 25 | `general-ai-training-knowledge` | Y | 289 | 289 | 0 | 0.96 |
| 26 | `glossary` | Y | 28 | 10 | 19 | 0.95 |
| 27 | `gui-control-registry` | - | 10 | 9 | 2 | 0.95 |
| 28 | `hybrid-film-restorer` | - | 17 | 16 | 3 | 0.96 |
| 29 | `hybrid-multitask` | - | 16 | 16 | 2 | 0.97 |
| 30 | `hybrid-upn-v2` | - | 17 | 17 | 2 | 0.97 |
| 31 | `manuals-hub` | Y | 8 | 8 | 1 | 0.63 |
| 32 | `mirnet` | - | 36 | 38 | 3 | 0.97 |
| 33 | `mprnet` | - | 64 | 64 | 1 | 0.98 |
| 34 | `nafnet` | - | 74 | 74 | 3 | 0.95 |
| 35 | `nima-authenticity` | - | 17 | 16 | 5 | 0.92 |
| 36 | `nima-efficientnet` | - | 17 | 16 | 5 | 0.92 |
| 37 | `nima-master` | Y | 7 | 7 | 1 | 0.80 |
| 38 | `nima-mobile` | - | 17 | 16 | 5 | 0.92 |
| 39 | `nima-pro` | - | 17 | 16 | 5 | 0.92 |
| 40 | `nima-quality` | - | 125 | 121 | 5 | 0.78 |
| 41 | `nima-technical` | - | 17 | 16 | 5 | 0.92 |
| 42 | `restoration-master` | Y | 8 | 8 | 1 | 0.66 |
| 43 | `restoration-suite` | - | 26 | 15 | 13 | 0.54 |
| 44 | `training-pathology` | Y | 52 | 52 | 1 | 0.83 |
| 45 | `training-suite-master` | - | 49 | 47 | 7 | 0.85 |
| 46 | `ultrazoom` | Y | 17 | 17 | 4 | 0.66 |
| 47 | `universal-hybrid` | Y | 12 | 13 | 2 | 0.93 |
| 48 | `versioning-policy` | - | 13 | 12 | 4 | 0.94 |

Column legend: "MD hd" and "HTML hd" are H1 to H4 heading counts
(Table of Contents headings excluded); "Hd drift" is the number of
headings that do not align in sequence; "Words" is the word-sequence
similarity ratio (1.00 means identical prose).

Markdown source for each row (same numbering):

| # | Markdown source (`MD-Papers/`) |
| -: | --- |
| 1 | `AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md` |
| 2 | `MANUAL_AI_STUDIO_GUI.md` |
| 3 | `PAPER_AI_STUDIO_GUI.md` |
| 4 | `MANUAL_API.md` |
| 5 | `PAPER_LEMGENDARY_NSFW_CLASSIFIER.md` |
| 6 | `MANUAL_CLI.md` |
| 7 | `LEMGENDARY_CURRENT_STATE.md` |
| 8 | `PAPER_DATASET_COMPILER.md` |
| 9 | `PAPER_DEGRADATION_ENGINE.md` |
| 10 | `PAPER_LEMGENDARY_DETECTION_CLASSIFICATION.md` |
| 11 | `PAPER_DETECTION_MASTER.md` |
| 12 | `PAPER_LEMGENDARY_YOLOV8N.md` |
| 13 | `ECOSYSTEM_ARCHITECTURE.md` |
| 14 | `PAPER_ENV_MANAGER.md` |
| 15 | `PAPER_LEMGENDARY_CODEFORMER.md` |
| 16 | `PAPER_LEMGENDARY_PARSENET.md` |
| 17 | `PAPER_LEMGENDARY_RETINAFACE.md` |
| 18 | `PAPER_LEMGENDARY_FACE_SUITE.md` |
| 19 | `PAPER_LEMGENDARY_FFANET.md` |
| 20 | `PAPER_FOREX_PREDICTOR.md` |
| 21 | `PAPER_LEMGENDARY_DIFFUSION.md` |
| 22 | `PAPER_LEMGENDARY_IMAGE_TO_TEXT.md` |
| 23 | `PAPER_LEMGENDARY_LLM.md` |
| 24 | `PAPER_FOUNDATION_MODELS_MASTER.md` |
| 25 | `GENERAL_AI_TRAINING_KNOWLEDGE.md` |
| 26 | `GLOSSARY.md` |
| 27 | `GUI_CONTROL_REGISTRY.md` |
| 28 | `PAPER_LEMGENDARY_FILM_RESTORER.md` |
| 29 | `PAPER_LEMGENDARY_MULTITASK.md` |
| 30 | `PAPER_LEMGENDARY_UPN_V2.md` |
| 31 | `MANUALS_HUB.md` |
| 32 | `PAPER_LEMGENDARY_MIRNET.md` |
| 33 | `PAPER_LEMGENDARY_MPRNET.md` |
| 34 | `PAPER_LEMGENDARY_NAFNET.md` |
| 35 | `PAPER_NIMA_AUTHENTICITY.md` |
| 36 | `PAPER_NIMA_EFFICIENTNET.md` |
| 37 | `PAPER_NIMA_MASTER.md` |
| 38 | `PAPER_NIMA_MOBILE.md` |
| 39 | `PAPER_NIMA_PRO.md` |
| 40 | `PAPER_LEMGENDARY_NIMA.md` |
| 41 | `PAPER_NIMA_TECHNICAL.md` |
| 42 | `PAPER_RESTORATION_MASTER.md` |
| 43 | `PAPER_LEMGENDARY_RESTORATION_SUITE.md` |
| 44 | `PAPER_TRAINING_PATHOLOGY.md` |
| 45 | `PAPER_TRAINING_SUITE.md` |
| 46 | `PAPER_LEMGENDARY_ULTRAZOOM.md` |
| 47 | `PAPER_LEMGENDARY_HYBRID.md` |
| 48 | `VERSIONING_POLICY.md` |

### Orphans and Unregistered Files

- Markdown without manifest entry: none.
- HTML without manifest entry: none.
- Manifest entries pointing to missing files: none.
- `index.html` links to missing files: none.
- `INVESTOR_STRATEGY_LEMGENDARY_2026.md` (repository root) has no HTML
  counterpart and no manifest entry. Decide whether it is a publication
  (then register and pair it) or internal material (then move it out of
  the published hub).
- Unreferenced assets (24): `assets/gui/test_*.png` (8 debug screenshots),
  10 GUI screenshots (`gui_cloud_modal_*.png`, `gui_cloud_train_modal.png`,
  `gui_custom_compilation.png`, `gui_dataset_compiler_custom.png`,
  `gui_kaggle_*_hub.png`, `gui_log_panel.png`), `multitask_before.png`,
  `multitask_after.png`, `multitask_training.png`,
  `nsfw_classifier_training.png`, `yolov8n_confusion_matrix.png` and
  `sticky-tabs.js`.

## Synchronization Status

Method: Markdown and HTML heading sequences (H1 to H4) were normalized and
aligned with a sequence matcher; prose was compared as word sequences
(HTML navigation, scripts and tab bars excluded; Markdown TOC, images and
link targets excluded).

| Tier | Criteria | Pairs |
| --- | --- | -: |
| Green | Heading drift at most 1 and words at least 0.95 | 5 |
| Amber | Words 0.85 to 0.95, or heading drift above 1 | 25 |
| Red | Words below 0.85 | 18 |

Green pairs: `current-state`, `foundation-diffusion`, `foundation-llm`,
`general-ai-training-knowledge`, `mprnet`.

### Most Severe Drift

| ID | Words | Hd drift | Observation |
| --- | -: | -: | --- |
| `degradation-engine` | 0.33 | 17 | MD 1408 words vs HTML 452 |
| `face-retinaface` | 0.48 | 8 | HTML has 2.6x the MD prose |
| `face-suite` | 0.50 | 21 | MD sections 3.1, 3.2, 4.x absent |
| `detection-classification` | 0.52 | 9 | MD 3.1, 4.1.x absent in HTML |
| `restoration-suite` | 0.54 | 13 | MD 3.1, 4.1.x absent in HTML |
| `foundation-models-master` | 0.59 | 10 | Chinchilla 2.1 is MD only |
| `ai-studio-whitepaper` | 0.59 | 1 | HTML has 2.1x the MD prose |
| `ultrazoom` | 0.66 | 4 | Section 2 and 6 titles differ |
| `detection-yolov8n` | 0.67 | 11 | 4.1 vs 4.1.1 numbering |
| `nima-quality` | 0.78 | 5 | MD 5.47 to 5.49 not in HTML |
| `training-suite-master` | 0.85 | 7 | HTML 2.18 to 2.20 not in MD |
| `api-manual` | 0.86 | 10 | `POST /api/hooks/install` MD only |
| `dataset-compiler` | 0.87 | 10 | HTML has extra 5.x, renumbered |
| `glossary` | 0.95 | 19 | MD headings vs HTML list items |

### Systematic Drift Patterns

1. **H1 titles (41 pairs):** Markdown H1 carries a prefix such as
   "Architecture of LemGendary AI:" or "LemGendary Ecosystem:" that the
   HTML H1 drops (HTML moves the remainder to `p.subtitle`, or drops it).
2. **Category banner H2 (13 pairs):** Markdown has a
   `## Category ... | Subpage of ...` heading with no HTML counterpart.
3. **Model-card numbering (NIMA, face and YOLO papers):** Markdown uses
   `4.1`, `4.2` while HTML uses `4.1.1`, `4.1.2`.
4. **NIMA 1.1 titles:** Markdown "What NIMA Aesthetic Mobile Architecture
   Does" vs HTML "What This Model Does" (5 pairs).
5. **Late additions applied to one side only:** `training-suite-master`
   (HTML only), `nima-quality` (MD only), `dataset-compiler` (HTML only).

## Validation Results

### Tools Run

| Tool | Scope | Result |
| --- | --- | --- |
| `pytest` on `tests/test_documentation.py` | 38 tests | 37 pass, 1 fail |
| `scripts/audit_parity.py` | 48 pairs | 0 of 48 flagged |
| `scripts/audit_deep_parity.py` | 48 pairs | 0 of 48 flagged |
| `markdownlint-cli2` 0.18.1 (default) | 50 MD files | 2025 errors |
| Same, `noInlineConfig: true` | 50 MD files | 3647 errors |
| vnu.jar (html5validator, Java 21) | 49 HTML files | 5 errors |
| Structural parser (python `html.parser`) | 49 HTML files | See below |
| Link and anchor crawler | MD and HTML | See below |

The single test failure is `test_ai_helper_corpus_integrity`: it requires
`../LemGendaryDatasets/LemGendizedAIHelperLemGend/` (LemGendary Compiled
Manifolds Repo), which is not present in this workspace. The test should
skip with an explicit reason instead of failing, or the dependency should
be documented.

The two audit scripts resolve paths relative to the current working
directory (`lemgendary-docs/...`), so they only work from the workspace
root, and their checks are too coarse to detect the drift reported above.

### markdownlint

With inline directives honoured, all 2025 findings are `MD013`
(line length) in 16 files. With inline directives ignored (the real state
once the forbidden suppressions are removed):

| Rule | Count | Files |
| --- | -: | --- |
| MD013 line-length | 3495 | 50 files |
| MD051 link-fragments | 49 | 15 files |
| MD025 single-h1 | 44 | `GENERAL_AI_TRAINING_KNOWLEDGE.md` |
| MD024 duplicate heading | 44 | `GENERAL_AI_TRAINING_KNOWLEDGE.md` |
| MD035 hr-style | 7 | `GENERAL_AI_TRAINING_KNOWLEDGE.md` |
| MD003 heading-style | 4 | `GENERAL_AI_TRAINING_KNOWLEDGE.md` |
| MD001 heading-increment | 4 | `GENERAL_AI_TRAINING_KNOWLEDGE.md` |

Largest MD013 contributors (suppressions honoured):
`MANUAL_AI_STUDIO_GUI.md` (425), `PAPER_DATASET_COMPILER.md` (243),
`MANUAL_API.md` (199), `PAPER_TRAINING_PATHOLOGY.md` (175),
`README.md` (168), `MANUAL_CLI.md` (150).

Inline suppressions found: `MD051 MD013` (32 files),
`MD033 MD024` (1 file) and `MD025 MD024 MD035 MD003 MD001 MD013`
(`GENERAL_AI_TRAINING_KNOWLEDGE.md`).

MD051 examples: `PAPER_LEMGENDARY_FILM_RESTORER.md` and
`PAPER_LEMGENDARY_UPN_V2.md` (TOC links to sections 3 to 8 whose headings
are titled differently), `PAPER_LEMGENDARY_NIMA.md` (14 entries),
`PAPER_TRAINING_SUITE.md` (TOC lists 2.18 to 2.20, which exist only in
the HTML), `#conclusion` in MIRNet and MPRNet, and the five NIMA model
papers (1.1 anchors no longer match their headings).

### HTML (W3C Nu Validator)

| File | Line | Finding |
| --- | -: | --- |
| `ai-helper-troubleshooting-knowledge.html` | 689 | Unescaped `<` |
| `forex_predictor.html` | 401 | Unescaped `<` |
| `mirnet.html` | 135 | Duplicate `class` attribute |
| `mirnet.html` | 142 | Duplicate `class` attribute |
| `training-pathology.html` | 323 | Duplicate `class` attribute |

Warnings (16): redundant `type="text/javascript"` on the MathJax script
in 10 files; table rows narrower or wider than the header row in
`mirnet.html` (3) and `mprnet.html` (3). `index.html` and the other 44
papers validate with no errors.

### HTML Template Compliance

| Element | Required | Papers with it | `index.html` |
| --- | --- | -: | --- |
| `<!DOCTYPE html>` | Yes | 48 of 48 | Yes |
| `header` | Yes | 0 of 48 | Yes |
| `nav.toc-sidebar` | Yes | 0 of 48 | No |
| `section` | Yes | 47 of 48 | No |
| `footer` | Yes | 0 of 48 | Yes |

Papers use `nav#toc.toc-fixed-bar`; `general-ai-training-knowledge.html`
has no `section` element. The test suite does not check this template, so
the gap is invisible to CI.

### Links and Anchors

- HTML in-page anchors: 4 broken in `ultrazoom.html`
  (`#variant-x2`, `#variant-x3`, `#variant-x4`, `#variant-x8`).
- HTML relative links and assets: 0 broken; 0 duplicate `id` values.
- Markdown relative links: 4 broken. `MANUAL_API.md` links to
  `cli-manual.html` and `env_manager.html`; `MANUAL_CLI.md` links to
  `api-manual.html` and `env_manager.html`. These resolve only from
  `papers/`; from `MD-Papers/` they should target the Markdown files.
- Markdown fragments: 49 broken (MD051), plus
  `#31-quantitative-parameter-supervision-labelssplitnamejson` in
  `PAPER_DEGRADATION_ENGINE.md` found by the crawler.

## Manifest & Capability Registry Findings

### Registry Equivalence

- JSON vs YAML: identical after parsing (0 differing keys or values).
- `document_baseline` is `v16.9.60-STABLE` in both the registry and the
  manifest, but `README.md` already records releases up to `v16.9.63`, and
  `index.html` still shows `Version v16.9.27-STABLE` with
  `Last Reviewed: 2026-10-17` (manifest `last_audited` is `2026-11-02`).
- `total_publications` (48) equals the number of manifest entries.

### Per-Document Version Consistency

Only 4 documents agree across manifest, Markdown and HTML
(`ai-helper-troubleshooting-knowledge`, `current-state`,
`ecosystem-architecture`, `manuals-hub`). The `-STABLE` suffix is omitted
below; `-` means no version metadata was found.

| # | ID | Manifest | MD | HTML |
| -: | --- | --- | --- | --- |
| 1 | `ai-helper-troubleshooting-knowledge` | 16.9.27 | 16.9.27 | 16.9.27 |
| 2 | `ai-studio-manual` | 2.10.2 | - | 2.0.0 |
| 3 | `ai-studio-whitepaper` | 2.10.2 | 2.0.0 | 16.9.16 |
| 4 | `api-manual` | 16.9.44 | - | 16.9.44 |
| 5 | `classification-nsfw` | 16.9.27 | 16.9.16 | 16.9.16 |
| 6 | `cli-manual` | 16.9.44 | - | 16.9.16 |
| 7 | `current-state` | 16.9.27 | 16.9.27 | 16.9.27 |
| 8 | `dataset-compiler` | 16.9.19 | - | 16.9.13 |
| 9 | `degradation-engine` | 16.9.27 | - | 16.9.16 |
| 10 | `detection-classification` | 16.9.27 | 1.0.0 | 16.9.16 |
| 11 | `detection-master` | 16.9.27 | 16.9.27 | 16.9.16 |
| 12 | `detection-yolov8n` | 16.9.27 | 16.9.10 | 16.9.16 |
| 13 | `ecosystem-architecture` | 16.9.27 | 16.9.27 | 16.9.27 |
| 14 | `env_manager` | 16.9.27 | - | 16.9.3 |
| 15 | `face-codeformer` | 16.9.27 | 16.9.16 | 16.9.16 |
| 16 | `face-parsenet` | 16.9.27 | 16.9.16 | 16.9.16 |
| 17 | `face-retinaface` | 16.9.27 | 16.9.16 | 16.9.16 |
| 18 | `face-suite` | 16.9.27 | 1.0.0 | 16.9.16 |
| 19 | `ffanet` | 16.9.27 | 2.6.0 | 16.9.16 |
| 20 | `forex_predictor` | 16.9.27 | 2.7.1 | 2.7.1 |
| 21 | `foundation-diffusion` | 16.9.27 | 16.7.3 | 16.9.16 |
| 22 | `foundation-image-to-text` | 16.9.27 | 16.7.3 | 16.9.16 |
| 23 | `foundation-llm` | 16.9.27 | 16.7.3 | 16.9.16 |
| 24 | `foundation-models-master` | 16.9.27 | 16.9.27 | 16.9.16 |
| 25 | `general-ai-training-knowledge` | 16.9.27 | - | - |
| 26 | `glossary` | 16.9.27 | - | 16.9.16 |
| 27 | `gui-control-registry` | 16.9.27 | - | 16.9.16 |
| 28 | `hybrid-film-restorer` | 16.9.27 | 16.9.16 | 16.9.16 |
| 29 | `hybrid-multitask` | 16.9.27 | 16.9.16 | 16.9.16 |
| 30 | `hybrid-upn-v2` | 16.9.27 | 16.9.16 | 16.9.16 |
| 31 | `manuals-hub` | 16.9.27 | 16.9.27 | 16.9.27 |
| 32 | `mirnet` | 16.9.27 | 2.6.0 | 16.9.16 |
| 33 | `mprnet` | 16.9.27 | 2.6.0 | 16.9.16 |
| 34 | `nafnet` | 16.9.27 | 2.6.0 | 16.9.16 |
| 35 | `nima-authenticity` | 16.9.27 | 16.9.16 | 16.9.16 |
| 36 | `nima-efficientnet` | 16.9.27 | 16.9.16 | 16.9.16 |
| 37 | `nima-master` | 16.9.27 | 16.9.27 | 16.9.16 |
| 38 | `nima-mobile` | 16.9.27 | 16.9.16 | 16.9.16 |
| 39 | `nima-pro` | 16.9.27 | 16.9.16 | 16.9.16 |
| 40 | `nima-quality` | 16.9.27 | 3.2.0 | 3.2.0 |
| 41 | `nima-technical` | 16.9.27 | 16.9.16 | 16.9.16 |
| 42 | `restoration-master` | 16.9.27 | 16.7.3 | 16.9.16 |
| 43 | `restoration-suite` | 16.9.27 | 1.0.0 | 16.9.16 |
| 44 | `training-pathology` | 16.9.27 | 1.4.0 | 1.4.0 |
| 45 | `training-suite-master` | 16.9.44 | - | 16.9.27 |
| 46 | `ultrazoom` | 16.9.27 | 16.7.3 | 16.9.16 |
| 47 | `universal-hybrid` | 16.9.27 | 1.0.0 | 16.9.16 |
| 48 | `versioning-policy` | 16.9.27 | - | 16.9.16 |

Additional version notes:

- Several MD sources use a paper-local version line (for example
  `2.6.0 - Dynamic VRAM Sync`), while the HTML shows the ecosystem release
  (`16.9.16-STABLE`). `VERSIONING_POLICY.md` should define which one is
  authoritative.
- `PAPER_ENV_MANAGER.md` H1 embeds `(v16.8.0-stable)`, which differs from
  the manifest, the HTML and the code.

### Category Taxonomy Drift

| ID | Manifest | Markdown | HTML |
| --- | --- | --- | --- |
| `ai-studio-whitepaper` | 01 ARCH | 01.4 | 01.4 GUI |
| `dataset-compiler` | 01.1 COMPILER | 01.2 | 01.2 DATASET |
| `degradation-engine` | 01.2 ENGINE | 01.2 | none |
| `env_manager` | 01.4 ENV | 01.1 | 01.1 ENV |
| `gui-control-registry` | 03.4 CONTROLS | 04 CONTROLS | 03.4 CONTROLS |
| `api-manual` | 03 MANUALS | 00 | 03 MANUALS |
| `cli-manual` | 03 MANUALS | 00 | 03 MANUALS |
| `restoration-suite` | 04 RESTORATION | 14 | 14 RESTORATION |
| `forex_predictor` | 11 FOREX | 11 FINANCIAL | none |
| `face-suite` | 08 FACE VISION | 08 FACE | 08 FACE |
| Model specification papers | 04.1 to 10.3 SPECIFICATION | parent | parent |

- Category 01.2 is used by two documents in Markdown, and 01.4 is used by
  both the GUI whitepaper (MD/HTML) and the Environment Manager
  (manifest).
- Category 14 is outside the canonical 00 to 13 taxonomy described by
  `test_no_category_taxonomy_drift` (that test only rejects "15").
- Category 00 is reserved for General AI Training Knowledge, yet the API
  and CLI manual sources declare Category 00.

## Whitepaper Structure Compliance

### Section 1 Title Rule

- Compliant (`1. Abstract`): all 23 vision papers, Forex Predictor,
  Dataset Compiler, Degradation Engine, Environment Manager, AI Studio
  GUI, Training Suite, Training Pathology, foundation papers and masters.
- Explicit violation: `LEMGENDARY_CURRENT_STATE.md` uses
  `1. Executive Summary & Current Operational State`.
- Non-strict variants: `1. Abstract & ...` in `ECOSYSTEM_ARCHITECTURE.md`,
  `GLOSSARY.md`, `GUI_CONTROL_REGISTRY.md`, `MANUAL_AI_STUDIO_GUI.md`,
  `VERSIONING_POLICY.md`; `1. Executive Overview` in `MANUAL_API.md` and
  `MANUAL_CLI.md`. Confirm whether manuals are in scope of the rule.

### Vision and Restoration Models (23 papers)

| Check | Compliant | Notes |
| --- | -: | --- |
| 8-section ordering | 21 of 23 | Fails: HYBRID, NIMA |
| Section 4.1.8 present | 2 of 23 | NAFNet, MPRNet only |
| Ladder 256, 384, 512, 640 px in 4.1.8 | 1 of 23 | NAFNet |
| Quality Score LaTeX formula | 4 of 23 | See below |
| Mem total vs peak LaTeX bound | 3 of 23 | NAFNet, MPRNet, Face Suite |
| PSNR, SSIM, LPIPS and FID all named | 8 of 23 | Classifiers omit |

- `PAPER_LEMGENDARY_HYBRID.md` has only 5 top-level sections
  (Unified Architectures, Optimizations, Deployment, Conclusion).
- `PAPER_LEMGENDARY_NIMA.md` section 7 is "Universal Hardware Protocols"
  instead of "SOTA Architectural Performance Matrix".
- MPRNet 4.1.8 documents `256px -> 384px -> 512px` only.
- Quality Score formula present in NAFNet, MPRNet, Face Suite and
  Restoration Suite.
- Operator formulas: CSFF and SAM appear only in MPRNet; SimpleGate
  appears in NAFNet and MPRNet; Charbonnier is absent from NAFNet.
- The NIMA, NSFW, YOLO, RetinaFace and ParseNet papers are classifiers or
  detectors; the restoration metrics and the spatial ladder do not map
  cleanly to them. `ROBOTS.md` should state whether these papers belong to
  the vision domain rule or need their own rule.

### Financial Time-Series (Forex Predictor)

- 8-section ordering: compliant.
- Section 4.1.8 (Walk-Forward validation): missing. The deep-dive has
  only `4.1 Model Description, Purpose and Usage`; walk-forward is
  discussed elsewhere (13 mentions).
- LaTeX: 26 display blocks; temporal convolution and attention present;
  an explicit directional cross-entropy formula was not detected and
  needs manual confirmation.

### Dataset Compilers (`PAPER_DATASET_COMPILER.md`)

- Ordering: non-compliant. A section `5. 2026 Modernization Architecture &
  Innovations` is inserted, so Comparative Analysis becomes 6, Synthesis
  Flow 7, Unified Models Registry 8, an extra `9. Generic LLM Dataset
  Compiler Architecture` follows, and Conclusion is 10.
- LaTeX: 13 display blocks and 15 complexity terms using `mathcal{O}`;
  compliant.

### Chart Governance

- Versioned chart filenames exist for `forex_training_curve_v2.png` and
  `mprnet_deraining_training_v2.png` only.
- `multitask_training.png` and `nsfw_classifier_training.png` exist but
  are not embedded in their papers.
- Exact metric parity with `metrics.csv` and checkpoints could not be
  verified: the LemGendary Trained Models Repo (`../LemGendaryModels/`) is
  not present in this workspace.

## Naming & Path Governance Findings

### Absolute Paths

Drive-rooted Windows paths (literal values not repeated here):

| File | Occurrence |
| --- | --- |
| `MD-Papers/MANUAL_API.md` | MetaTrader 5 install path in JSON example |
| `papers/api-manual.html` | Same JSON example |
| `MD-Papers/MANUAL_CLI.md` | MetaTrader 5 `terminal64.exe` path |
| `papers/cli-manual.html` | Same |
| `MD-Papers/PAPER_DATASET_COMPILER.md` | 7-Zip and Windows `tar.exe` paths |
| `papers/dataset-compiler.html` | Same two paths |
| `README.md` | Quotes a `file:` URL in the v16.9.62 note |

These describe third-party install locations probed at runtime, but the
`ROBOTS.md` invariant has no exception. Use placeholders such as
`%ProgramFiles%/MetaTrader 5` or `<ProgramFiles>/7-Zip/7z.exe`. The
README note for v16.9.62 states that all absolute paths were removed.

### Canonical Project Names

| Canonical name | Uses |
| --- | -: |
| LemGendary Environment Manager | 24 |
| LemGendary Dataset Compiler Suite | 22 |
| LemGendary AI Documentation Hub | 15 |
| LemGendary Model Training Suite | 14 |
| LemGendary AI Studio GUI | 11 |
| LemGendary Compiled Manifolds Repo | 0 |
| LemGendary Trained Models Repo | 0 |

| Non-canonical variant | Uses | Main locations |
| --- | -: | --- |
| AI Studio Desktop GUI | 42 | AI Studio manual and whitepaper |
| LemGendary AI Studio (no "GUI") | 34 | AI Studio papers, registry |
| LemGendary Training Suite | 22 | NIMA, Pathology, investor doc |
| LemGendary Dataset Compiler (no "Suite") | 11 | Helper KB, compiler |
| ai-training-whitepapers / AI Training Whitepapers | 8 | `index.html` |
| LemGendary Docs Hub / AI Hub | 5 | tests, `index.html`, README |
| lemgendary-dataset-generator | 2 | `PAPER_DEGRADATION_ENGINE.md` |
| Lemgendary (case variant) | 1 | Investor strategy document |

Governance-file observations for the human owner (not edited):
`../ROBOTS.md` lists `./LemGendaryDatasets\` with mixed separators, and
`../Instructions.md` names the LemGendary Dataset Compiler Suite
repository `lemgendary-dataset-generator`, which conflicts with the
canonical folder `lemgendary-datasets`.

## Cross-Project Drift (docs vs code)

| Item | Documentation | Code |
| --- | --- | --- |
| Ports 8000, 8100, 8200 | Env, Compiler, Training | Same |
| Model identifiers | 23 in registry | 23 in `unified_models_v2.yaml` |
| CLI entry points | `lem-env`, `lemtrain`, `cli.py` | All exist |
| AI Studio GUI version | Registry v2.10.5; manifest v2.10.2 | README v2.10.7 |
| AI Studio GUI package | Manual HTML 2.0.0 | `package.json` 2.0.0 |
| Model Training Suite | Registry v16.9.60 | README v16.9.61 |
| Training Suite package | n/a | `pyproject.toml` 16.2.9 |
| Dataset Compiler Suite | Registry v16.9.21; paper v16.9.19 | README v16.9.22 |
| Dataset Compiler HTML | 16.9.13 | OpenAPI 16.5.0 |
| Environment Manager | Manifest v16.9.27; HTML 16.9.3 | README v16.9.10 |
| Environment Manager pkg | MD H1 v16.8.0 | `pyproject.toml` 16.2.0 |

Test-suite drift:

- `test_cross_repo_manifest_and_runtime_consistency` labels port 8000 as
  Training Suite, 8100 as Env Manager and 8200 as Dataset Compiler. The
  code and documents use 8000 Environment Manager, 8100 Dataset Compiler
  Suite and 8200 Model Training Suite. The assertion passes but its
  messages are wrong.
- `test_header_version_authority_metadata` hard-codes
  `Version v16.9.27-STABLE`, locking `index.html` to a stale version.
- `test_ai_helper_dataset_integrity` returns silently when the dataset is
  missing (a silent pass, contrary to `ROBOTS.md`), while the sibling
  corpus test fails hard on the same condition.
- `setUpClass` falls back to a path relative to the current working
  directory (`os.path.abspath('lemgendary-training-suite/...')`).
- `.pre-commit-config.yaml` runs `python verify_docs.py --staged`; the
  script does not exist.

## Proposed Changelog Entries

Proposed for the human owner to add to `README.md` once the fixes land
(not applied by this review):

```markdown
### v16.9.64 - Lead Documentation Review Remediation

* **Template Compliance** - Migrated all 48 publications and `index.html`
  to the approved template (`header`, `nav.toc-sidebar`, `section`,
  `footer`); fixed 5 W3C errors and 16 warnings.
* **Lint Without Suppressions** - Removed inline `markdownlint-disable`
  directives from 34 sources, committed `.markdownlint.json` with default
  rules, and resolved MD013, MD051, MD025, MD024, MD035, MD003, MD001.
* **MD/HTML Parity** - Resynchronized 43 drifting pairs (H1 titles,
  category banners, model-card numbering, one-sided section additions).
* **Versioning SSOT** - Aligned manifest, Markdown and HTML versions for
  all 48 publications; updated `index.html` version and review date;
  `document_baseline` raised to v16.9.64-STABLE in the manifest and both
  capability registries.
* **Taxonomy** - Resolved category collisions (01.2, 01.4), replaced
  Category 14 and Category 00 misuse.
* **Relative Paths** - Replaced 8 absolute install-path examples with
  portable placeholders.
* **Whitepaper Rigor** - Added Section 4.1.8 to vision and forex papers,
  reordered the Dataset Compiler paper to the 8-section topology, renamed
  `1. Executive Summary` to `1. Abstract` in the current-state manifest.
* **Validation Tooling** - Replaced shallow parity scripts with a
  heading-sequence and text-similarity gate; corrected port labels and
  stale version pins in the test suite; fixed the pre-commit entry point.
```

Proposed registry update (manifest and both capability registries, in the
same change): bump `document_baseline` and `last_audited`, and align
`desktop_client_baseline`, `runtime_engine_baseline` and
`dataset_compiler_baseline` with the latest code releases (v2.10.7,
v16.9.61, v16.9.22) once those releases are confirmed.

## Remaining Recommendations

Ranked by priority (1 = highest).

1. **Make Markdown the single source and generate HTML.** Hand-maintained
   pairs have drifted in 43 of 48 cases; a generator using the approved
   template removes drift, template non-compliance and H1 divergence
   together.
2. **Remove all lint suppressions and commit the lint configuration.**
   Delete the 34 inline directives, stop ignoring `.markdownlint.json`,
   then fix the 3647 findings at source (mostly line wrapping).
3. **Resynchronize the 18 red pairs first**, starting with
   `degradation-engine`, `face-suite`, `restoration-suite`,
   `detection-classification`, `face-retinaface` and
   `foundation-models-master`.
4. **Adopt one version authority.** Drive the HTML badge, the Markdown
   header and `index.html` from `manifest/documents.json`; define paper
   version vs ecosystem release in `VERSIONING_POLICY.md`.
5. **Fix the 5 W3C errors, 4 broken HTML anchors, 49 MD051 fragments and
   4 broken Markdown relative links.**
6. **Bring whitepapers to the ROBOTS.md structure:** Section 4.1.8 for 21
   vision papers and Forex Predictor, Dataset Compiler ordering, HYBRID
   and NIMA ordering, Quality Score and memory-bound formulas.
7. **Resolve category taxonomy collisions** and record the canonical
   category map in the manifest only.
8. **Replace absolute install paths** with portable placeholders.
9. **Standardize project names** to the seven canonical names, especially
   "AI Studio Desktop GUI" and "LemGendary Training Suite".
10. **Harden validation tooling:** parity gate based on heading sequence
    and text similarity, template checks for `header`, `nav.toc-sidebar`
    and `footer`, paths resolved from `Path(__file__)`, explicit skips with
    reasons, a correct pre-commit entry point, and no hard-coded versions.
11. **Prune or register unreferenced assets** (24 files, including 8 debug
    screenshots) and decide the status of
    `INVESTOR_STRATEGY_LEMGENDARY_2026.md`.
12. **Clarify domain scope in `ROBOTS.md`** for classifier and detector
    papers and for manuals (human decision; governance not edited here).
