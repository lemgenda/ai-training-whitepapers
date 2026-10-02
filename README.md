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

## Changelog

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
