# LemGendary AI Documentation Hub

> Authoritative technical whitepapers, architectural manuals, API references, CLI guides, and visual demonstrations for the LemGendary AI ecosystem.

---

## Directory Overview

* **`papers/`** — W3C-compliant standalone HTML versions of all 46 technical whitepapers, manuals, and architectural specifications.
* **`MD-Papers/`** — Markdown sources synchronized 1-to-1 with the HTML publications, formatted to strict markdownlint compliance.
* **`assets/`** — Static imagery, training loss curves, architectural flowcharts, and before/after perceptual visual demonstrations.
* **`roadmaps/`** — Strategic planning and implementation roadmap documents.
* **`index.html`** — Central documentation catalog and entry portal.

---

### v16.9.21 — 20-Rule Automated Test Suite Expansion, Category Taxonomy & Pre-Commit Hardening

* **20-Rule Comprehensive Documentation Test Battery** — Expanded `tests/test_documentation.py` from 13 to 20 automated tests, enforcing zero emojis, LaTeX deep integrity, stray HTML fragment detection, category taxonomy uniqueness, ungrounded CLI command rejection, compiler API parity, model registry specification alignment, and benchmark evidence qualification.
* **Global Category Taxonomy Unification** — Reconciled category collisions: GUI Control Registry reassigned to `Category 03.4 CONTROLS`, reserving `Category 04` exclusively for Dedicated Image Restoration. Centralized governance and operational specs under `Category 01.x` (`01.0 STATUS`, `01.1 ENV`, `01.5 POLICY`), preserving `Category 00` strictly for General AI Training Knowledge.
* **Deep Mathematical & LaTeX Notation Repairs** — Corrected escape-truncated primitives (`\alpha`, `\bar{\alpha}_t`, `\tau`, `\right`, `\begin{cases}`, `\rho(`, `\beta(`) across all 48 HTML whitepapers and Markdown companion sources.
* **SSOT Model Registry & Compiler API Synchronization** — Aligned NIMA Mobile backbone specification to `MobileNetV3-Small`, technical and authenticity backbones to `EfficientNetV2-S`, and documented compiler endpoints (`POST /api/gui/custom-compile`, `/api/kaggle/...`) across both HTML and Markdown API manuals.
* **Git Pre-Commit Hook Hardening** — Hardened pre-commit hook path resolution across `.githooks/pre-commit` and `.git/hooks/pre-commit` with dynamic directory inspection (`HOOK_DIR`) and direct `test_documentation.py` execution, ensuring commits from any CWD trigger the full 20-rule battery.

---

### v16.9.20 — Stage 8: Documentation, Manuals & GUI Training Panel Synchronization

* **Universal Automated Documentation Test Suite Validation** — Expanded automated test suite in `lemgendary-docs/tests/test_documentation.py` (12/12 passing) covering zero emojis, LaTeX syntax integrity, HTML tag balancing, internal link existence across all 48 publications, and CSS brace balance.
* **Full Compliance Passing Status** — Validated `lem-env validate --project lemgendary-docs` achieving 100% compliance across Python compilation, markdownlint, YAML, JSON, W3C/WCAG, and domain document sync similarity.
* **Category 13: AI Helper Troubleshooting Integration** — Added Category 13 card to `index.html` and cross-linked `ai-helper-troubleshooting-knowledge.html` into `manuals-hub.html` and `training-pathology.html`.
* **GUI Manual & Training Panel Revamp Documentation** — Documented the redesigned 1/4 - 3/4 dashboard topology, full-width model card header with integrated progress bars, interactive pinned/persisted SOTA tooltip metric inspector, dual Local/Cloud triggers with auto-scroll and telemetry focus, and the interactive Cloud Training modal in `MANUAL_AI_STUDIO_GUI.md` and `ai-studio-manual.html`.

---

### v16.9.19 — Stage 7: P2 AI Helper Specialized Training Corpus Preparation & Documentation Test Suite

* **Tasks 11-13 & 17: Tri-Level Task Trajectories (GUI, CLI, REST API)** — Synthesized multi-tiered procedural training pairs answering identical developer objectives across GUI click paths, CLI terminal automation (`lem-env`), and headless backend REST API requests.
* **Tasks 14 & 16: Structured Troubleshooting Knowledge Base** — Published `AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md` and `ai-helper-troubleshooting-knowledge.html` formalizing real-world failure modes (scheduler double-stepping, AMP NaN instability, sentinel/scheduler desynchronization, infinite plateau loops, Pearson matrix singularities, dataloader starvation) into a 6-attribute diagnostic schema (`symptom`, `context`, `observations`, `likely_causes`, `diagnostic_steps`, `recommended_action`).
* **Task 15: Cross-Document Architectural Pipelines** — Synthesized end-to-end provenance trajectories spanning Raw Datasets $\to$ Dataset Compiler Presets $\to$ Sharded Manifolds $\to$ Model Architectures $\to$ Resolution Ladders $\to$ Checkpoint Lifecycles $\to$ ONNX/WebGPU Production Targets.
* **Task 18: Canonical 32-Field Model Schema Registry** — Standardized all 22 active and specification models in `tools/model_schema_registry.json` conforming to a uniform 32-field schema covering inputs, outputs, loss functions, SOTA targets, failure modes, and hardware bounds.
* **Task 19: Terminology Disambiguation & Hardened Negative Pairs** — Synthesized contrastive pairs training the AI Helper on foundational distinctions: Raw Dataset vs. Compiled Manifold, Container Format vs. Directory Layout, Hardlink vs. Perceptual Deduplication, and Native Studio Compatibility vs. General AI Formats.
* **Corpus Sharding & Validation** — Generated `lemgendary-docs/corpus/ai_helper_train.jsonl` and `ai_helper_val.jsonl` validated for strict ChatML schema compliance, token length bounds, and zero emojis.
* **Automated Documentation Test Suite** — Implemented unit test suite in `lemgendary-docs/tests/test_documentation.py` running automated regression audits on emojis, control characters, LaTeX integrity, SSOT manifest parity, canonical topologies, and epistemic tags.

### v16.9.18 — Stage 6: P1 Knowledge Normalization, Canonical Topology & Schema Harmonization

* **Item 6: Studio-Supported-Format Matrix** — Added comprehensive comparative matrix in `dataset-compiler.html` and `PAPER_DATASET_COMPILER.md` explicitly distinguishing General Knowledge formats from Studio-Supported native compilation manifolds.
* **Item 7: Canonical 8-Section Topology Normalization** — Enforced uniform structural topology across all 19 model whitepapers in both HTML (`papers/`) and Markdown (`MD-Papers/`): `1. Abstract`, `1.1 Plain English`, `2. Visual Taxonomy`, `3. Shared Foundations`, `4. Model Deep-Dives`, `5. Challenges & Resilience Architecture`, `6. Deployment Strategy & Production Acceleration`, `7. SOTA Architectural Performance Matrix`, and `8. Conclusion`.
* **Item 8: Universal Epistemic Claim Tagging** — Annotated empirical measurements, mathematical theorems, aspirational targets, and operational checkpoints with normalized tags (`[THEORETICAL]`, `[MEASURED]`, `[TARGET]`, `[CURRENT]`, and `[DESIGN_GOAL]`) across all model documentation.
* **Item 9: Technical Guarantee Qualification** — Qualified ungrounded absolute terminology ("impossible", "100%", "sub-millisecond latency", "guaranteed", "never") to mathematically bounded engineering guarantees across the corpus.
* **Item 10: Bidirectional Cross-Document Knowledge Graph** — Embedded comprehensive cross-reference hubs linking Model Whitepapers $\leftrightarrow$ Dataset Compiler Specifications $\leftrightarrow$ Training Suite Architecture $\leftrightarrow$ GUI Manuals.

### v16.9.17 — Documentation Hub Quality Audit, LaTeX Standardization & Section 4 Model Deep-Dives

* **Universal W3C & Structural Integrity Audit** — Audited and remediated all 48 HTML whitepapers in `lemgendary-docs/papers/`. Resolved tag balance mismatches in `forex_predictor.html`, `dataset-compiler.html`, `ffanet.html`, and `universal-hybrid.html`. Standardized MathJax 3 configurations with SVG global font caching across all technical documents.
* **Corrupted LaTeX & Mathematical Delimiter Repair** — Fixed tab-corrupted and carriage-return-corrupted LaTeX primitives (`\text`, `\times`, `\right`, `\bmod`) across `forex_predictor.html`, `foundation-models-master.html`, `nima-master.html`, `restoration-master.html`, and `ultrazoom.html`. Escaped raw pricing currency signs in `dataset-compiler.html` to prevent math syntax conflicts.
* **Section 1.1 (Plain English) & Section 4 (Model Deep-Dives) Standardization** — Uniformly implemented Section `1.1 What [ModelName] Does (In Plain English)` with visual before/after comparison demonstrations and Section `4. Model Deep-Dives` with model metadata, dataset specs, verified metric benchmarks, and high-resolution dark-themed training curves across all 19 model whitepapers.
* **P0 Metadata Synchronization** — Unified the NIMA Mobile backbone specification strictly to `MobileNetV3-Small (Global Composition)` and documented edge backbones (`MobileNetV3-Small`) for RetinaFace across both markdown sources and HTML publications. Standardized model status tokens across the entire corpus.

### v16.9.16 — Real-Time Batch/Epoch Progress Telemetry & First-Principles VRAM Sizing

* **`PAPER_LEMGENDARY_YOLOV8N.md` Synchronization** — Documented Section 5.1 first-principles dynamic Sawtooth VRAM sizing formula, configuration externalization in `unified_models_v2.yaml`, and real-time validation plot mirroring (`confusion_matrix.png`, `confusion_matrix_normalized.png`, PR/F1 curves) directly to `LemGendaryModels/yolov8n/`.
* **`PAPER_TRAINING_SUITE.md` Synchronization** — Documented real-time batch and epoch progress logging in terminal execution, non-blocking remote checkpoint probing with 5-second timeouts, and strict code-only training suite filesystem isolation.
* **`LemGendaryModels/` Dashboard Synchronization** — Synchronized live metrics matrix dashboard and per-model READMEs across all 22 active architectures via `doc_generator.py`.

### v16.9.13 — Intra-Resolution Fraction Progression & Governor Overfitting Rescue Protocol

* **`PAPER_LEMGENDARY_YOLOV8N.md` & `detection-yolov8n.html` Synchronization** — Documented Section 5.1 Intra-Resolution Fraction Progression on the lowest resolution rung ($320\text{px} @ 30\% \to 70\% \to 100\%$) prior to spatial resolution escalation, Governor Overfitting Rescue Protocol monitoring loss divergence and mAP stagnation during partial fraction stages to force immediate dataset expansion, and Section 5.2 Multi-Fraction Checkpoint Discovery and Resumption.
* **`lemgendary-training-suite/` Protocol Synchronization** — Documented deterministic fraction progression on base rungs, adaptive epoch allocations across 5 stages, and checkpoint state encoding (`stage{idx}_{res}px_f{pct}`).

### v16.9.12 — Checkpoint Resumption Protocol, Authoritative Persistence & Literature Citations

* **`PAPER_LEMGENDARY_YOLOV8N.md` & `detection-yolov8n.html` Synchronization** — Documented Section 5.2 deep checkpoint metadata interrogation, completed stage skipping, and mid-rung resumption (`resume=True`) from `last.pt`, Section 5.3 Authoritative Persistence in `LemGendaryModels/`, and Section 7 Scientific Literature & Reference Citations.
* **`PAPER_TRAINING_SUITE.md` & `training-suite-master.html` Synchronization** — Documented Section 2.4 Mid-Rung Checkpoint Resumption & Stage Skip Protocol across all models, Authoritative Single Source of Truth Persistence in `LemGendaryModels/<model_key>/`, and literature references integration.
* **`LemGendaryModels/` Model Documentation Matrix Synchronization** — Embedded landmark academic citations (authors, venue, year, canonical link, and BibTeX) across all 22 model READMEs in `LemGendaryModels/<model_key>/README.md` and refreshed the master hub dashboard.

### v16.9.11 — Real-Time Checkpoint Parity, Sub-Second Cancellation & Telemetry Stream Repositioning

* **`PAPER_LEMGENDARY_YOLOV8N.md` Synchronization** — Documented Section 5.1 dual-path intermediate checkpoint synchronization (`best.pt`, `best.pth`, `last.pt`, `progress.pth`) to `checkpoints/` and `LemGendaryModels/`, and inner-loop minibatch cancellation via `on_train_batch_end` setting `trainer.stop = True`.
* **`PAPER_TRAINING_SUITE.md` Synchronization** — Documented Section 2.4 Real-Time Cross-Model Checkpoint Parity and Sub-Second Minibatch Cancellation Protocol across all 20 architectures.
* **`MANUAL_AI_STUDIO_GUI.md` Synchronization** — Documented Section 6.2 Top-of-Fold Real-Time Telemetry Stream placement directly above the Registered Architectures catalog and the sub-second cancellation response handshake.

### v16.9.10 — SSOT Config-Governed Readonly Parameters, Dynamic Job Control & YOLO Curriculum Governor

* **`MANUAL_AI_STUDIO_GUI.md` & `ai-studio-manual.html` Synchronization** — Documented Section 6.1 Single Source of Truth (SSOT) parameter locking across all neural models (`Training Epochs`, `Minibatch Size`, `Initial Learning Rate`, and `Spatial Ladder Stage` / `Timeframe Confluence Stage`) to read-only mode (`.editor-input-readonly`) tied directly to `unified_models_v2.yaml` / `presets.yaml`. Documented the `.config-governed-banner`, inline `Adjust via Config Editor` workflow, and the dynamic run-state action button transforming from `Start Training` (`.btn-primary`) to `Stop Training` (`.btn-danger`) with job cancellation signal dispatch (`POST /api/jobs/{job_id}/cancel`).
* **`PAPER_TRAINING_SUITE.md` & `training-suite-master.html` Synchronization** — Documented Section 2.14 Autonomous YOLO Multi-Stage Curriculum Governor (`YOLOCurriculumGovernor`, `320px -> 480px -> 640px` resolution ladder, `0.3 -> 0.6 -> 1.0` dataset fraction scaling, Turing FP32 numerical stability overrides, Sawtooth VRAM sentinel, and telemetry writeback to `checkpoints/yolov8n/metrics.csv`), as well as Section 2.15 SSOT Config-Governed GUI Training Controls and dynamic run-state lifecycle.
* **`PAPER_LEMGENDARY_YOLOV8N.md` & `detection-yolov8n.html` Synchronization** — Documented Section 5.1 detailing the autonomous curriculum governor, progressive spatial ladder handoff (`best.pt` warm-starts), dataset scaling, Sawtooth memory sentinel, Turing non-Tensor core AMP overrides (`amp=False`), and live telemetry streaming.

### v16.9.9 — Training Orchestration Form Stabilization & Dynamic Model Defaults Synchronization

* **`MANUAL_AI_STUDIO_GUI.md` & `ai-studio-manual.html` Synchronization** — Documented Section 6.2 dynamic model hyperparameter synchronization upon architecture selection (YOLOv8n default 300 epochs, 0.01 learning rate, 640px stage; Forex Predictor default 0.0001 learning rate, D1 macro horizon), dedicated architecture selector row with architectural metadata badges, and glassmorphic Sawtooth Governor card.
* **`MANUAL_API.md` & `api-manual.html` Synchronization** — Documented `POST /api/gui/quick-train` payload support for `ladder_stage` and `enable_sawtooth` with in-process Ultralytics native trainer delegation for YOLOv8n, and enriched `GET /api/gui/models/with-stats` returning `learning_rate`, `batch_size`, and `default_epochs`.

### v16.9.8 — Authoritative 3-Pillar SOTA Convergence & Forex Multi-Timeframe Confluence Synchronization

* **`PAPER_TRAINING_SUITE.md` Synchronization** — Documented the mathematical 3-Pillar Fully-Trained Verification Invariant ($\bigwedge_{m} \text{Passed}(m, T_m) \land \text{LadderPassed} \land \text{DataFraction} \ge 1.0$), multi-metric evaluation across all defined `sota_targets`, Timeframe Confluence Ladder (`res_ladder: [1, 5, 15, 60, 240, 1440]`), and the 8-metric financial scorecard (`DirAcc`, `WinRate`, `ProfitFactor`, `Sharpe`, `Sortino`, `MaxDD`, `TP_MAE`, `SL_MAE`).
* **`MANUAL_AI_STUDIO_GUI.md` & `MANUAL_API.md` Specification Updates** — Documented Section 6.4 Model Architecture Cards and Status Badges (`FULLY TRAINED`, `PARTIALLY TRAINED`, `WEIGHTS READY`, `INITIALIZING`), card telemetry rows (`SOTA Targets`, `Confluence Ladder / Resolution Ladder`, `Data Fraction`), adaptive timeframe controls, and the enriched `GET /api/gui/models/with-stats` schema.

### v16.9.7 — Headless Windowless Service Execution & Automated GUI Mesh Bootstrapping

* **`PAPER_AI_STUDIO_GUI.md` & `MANUAL_AI_STUDIO_GUI.md` Synchronization** — Documented the cross-platform windowless background daemon execution architecture (`pythonw.exe`, `CREATE_NO_WINDOW`, `stdin=DEVNULL` on Windows; `start_new_session=True` on POSIX), eliminating intrusive console and Windows Terminal popups. Documented the GUI's automated startup effect on launch (`autoStartOffline`) and decoupled sub-100ms mesh heartbeats.
* **`MANUAL_API.md` Specification Updates** — Documented extended 20-second startup verification windows and `is_port_in_use()` collision guards for `POST /api/services/{service_id}/start`, plus dual `GET` and `HEAD` handler compliance across all sidecar `/api/health` endpoints.

### v16.9.6 — Desktop GUI Kaggle Cloud Synchronization Hub & Multi-Source Custom Compilation

* **`PAPER_DATASET_COMPILER.md` & `PAPER_AI_STUDIO_GUI.md` Synchronization** — Documented the Kaggle Cloud Synchronization & Storage Hub (bidirectional dataset downloads from `unified_data.yaml` registry, custom Kaggle link/slug downloads, and local manifold uploads), multi-source custom dataset synthesis pipeline (`kaggle://`, `hf://`, `gd://`, `gh://`), and fast split-shard discovery caching across 22 compiled manifolds.
* **`MANUAL_AI_STUDIO_GUI.md` & `MANUAL_API.md` Expansion** — Updated Section 5 of the GUI manual with detailed walkthroughs for Standard and Custom Multi-Source compilation modes, documented new REST endpoints (`GET /api/kaggle/registry-datasets`, `POST /api/kaggle/download`, `POST /api/kaggle/upload`, `POST /api/gui/custom-compile`), and synchronized the interactive control dictionary in `GUI_CONTROL_REGISTRY.md`.

### v16.9.1 — Visual Demonstration Remediation (Track B Execution)

* **`assets/` Asset Generation & Conversion** — Generated and optimized 10 high-fidelity perceptual demonstration assets into `assets/`:
  * `codeformer_before.png` & `codeformer_after.png` — Vector-quantized codebook face restoration before/after pair.
  * `film_restorer_before.png` & `film_restorer_after.png` — Analog 35mm celluloid scratch, dust, and dye recovery pair.
  * `upn_v2_before.png` & `upn_v2_after.png` — Multi-degradation composite restoration pair (motion blur, noise, compression).
  * `ultrazoom_before.png` & `ultrazoom_after.png` — Sub-pixel 4x super-resolution architectural crop pair.
  * `yolov8n_before.png` & `yolov8n_after.png` — Real-time spatial object detection and bounding box matrix pair.
* **HTML Whitepaper Remediation (`papers/`)** — Completely eliminated all dashed-border `<div>` placeholders across 9 papers, replacing them with semantic `<img>` elements and descriptive accessibility attributes:
  * `nima-authenticity.html` — Replaced placeholder blocks with `nima_authenticity_fake.png` and `nima_authenticity_real.png`. Synchronized training curve to `nima_authenticity_training.png`.
  * `nima-pro.html`, `nima-mobile.html`, `nima-efficientnet.html` — Replaced placeholder blocks with `technical_compression.png` and `aesthetic_masterpiece.png`.
  * `face-codeformer.html` — Embedded `codeformer_before.png` and `codeformer_after.png`.
  * `hybrid-film-restorer.html` — Embedded `film_restorer_before.png` and `film_restorer_after.png`.
  * `hybrid-upn-v2.html` — Embedded `upn_v2_before.png`, `upn_v2_after.png`, and `upn_v2_training.png`.
  * `ultrazoom.html` — Embedded `ultrazoom_before.png`, `ultrazoom_after.png`, and `ultrazoom_training.png`.
  * `detection-yolov8n.html` — Embedded `yolov8n_before.png` and `yolov8n_after.png`.
* **Markdown Whitepaper Synchronization (`MD-Papers/`)** — Updated all 9 markdown companions (`PAPER_NIMA_*.md`, `PAPER_LEMGENDARY_*.md`) with synchronized visual assessment tables and training curve references.
