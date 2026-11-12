# LemGendary Ecosystem: Current State & Architectural Manifest

## Category 01.0 STATUS | Authoritative Workspace State Manifest

**Parent Authority**: [Master Ecosystem
Architecture](./ECOSYSTEM_ARCHITECTURE.md)

**Versioning Policy**: [Document Authority Hierarchy & Versioning
Policy](./VERSIONING_POLICY.md)

**Version**: `v16.9.68-STABLE` · **Status**: Canonical ·
**Last audited**: 2026-11-12

---

## Table of Contents

- [1. Abstract](#1-abstract)
- [2. Multi-Track Versioning Matrix](#2-multi-track-versioning-matrix)
- [3. Document Authority Hierarchy](#3-document-authority-hierarchy)
- [4. Tripartite Microservice Topology & Port
  Bindings](#4-tripartite-microservice-topology--port-bindings)
- [5. Registered Model Architectures & Convergence
  Status](#5-registered-model-architectures--convergence-status)
- [6. Manifold Ingestion & Container
  Modernization](#6-manifold-ingestion--container-modernization)
- [7. Cloud Training & Remote Synchronization
  Pipeline](#7-cloud-training--remote-synchronization-pipeline)
- [8. Hardware Sentinels & Physical Execution
  Constraints](#8-hardware-sentinels--physical-execution-constraints)
- [9. Zero-Suppression Policy Compliance](#9-zero-suppression-policy-compliance)
- [10. Background Process Lifecycle Governance & Zombie
  Elimination](#10-background-process-lifecycle-governance--zombie-elimination)

---

## 1. Abstract

The **LemGendary AI Ecosystem** is an end-to-end, hardware-aware deep learning
platform for vision restoration, perceptual quality assessment, object
detection, a causal LLM assistant and multi-timeframe quantitative finance.
This manifest records the operational state verified on 2026-11-03 against the
code and the README changelogs of the five project repositories.

Current capabilities:

- **Tripartite Services**: Three decoupled FastAPI sidecars with HTTP REST and
  live WebSocket channels (ports 8000, 8100, 8200), each bound to `127.0.0.1`
  and described by its own OpenAPI 3.1.0 `openapi.json` (33, 37 and 40
  operations).
- **Shared Security Contract**: Every sidecar runs the same Origin Guard.
  Browser requests from origins other than the LemGendary AI Studio GUI
  (`tauri://localhost`, `http://tauri.localhost`, `https://tauri.localhost`,
  `http://localhost:1420`, `http://127.0.0.1:1420`) get HTTP 403, and
  state-changing browser requests must send the Client Header
  `X-LemGendary-Client: ai-studio-gui`. `GET /api/secrets` returns only whether
  each secret is set and its last 4 characters.
- **Presentation Layer**: The LemGendary AI Studio GUI (`v2.10.57`), a
  cross-platform desktop cockpit built with Tauri v2, React 18 and Vite, with a
  real Content Security Policy and one shared fetch wrapper for all sidecar
  calls.
- **Bug Report Tool**: The header button "Report Issue" opens a form (email,
  module, description of at least 50 characters, up to 5 annotated
  screenshots, optional Telemetry CSV). `POST /api/bug-report` on the
  LemGendary Environment Manager saves a Bug Report Archive (ZIP) in the
  workspace and opens the user's own mail client; no SMTP password ships with
  the application. In the desktop app on Windows the form can also attach a
  screen recording of the app window (MP4, up to 60 s); other platforms report
  that recording is not supported yet.
- **Monotonic Ratchet (pair rule)**: Resolution never decreases, and the data
  fraction never decreases within one resolution step; it may reset when the
  resolution steps up. A backward step raises `RatchetViolation`.
- **Bounded Epoch Budget**: Training stops on convergence (4-pillar
  completion), on the governor's early stop or when the configured budget is
  spent; extensions are opt-in and capped.
- **Pareto Model Soup**: `lemtrain soup` and `POST /api/models/{model_key}/soup`
  blend vault checkpoints. Optional Stochastic Weight Averaging (SWA, the
  `swa` section of `config.yaml`, off by default) adds `vault_swa.pth` as one
  more ingredient.
- **Publication-Grade FID**: FID uses the 2048-dimensional Inception pooling
  layer in micro-chunks of at most two samples. Historical FID values of
  `codeformer`, `ffanet_indoor`, `mprnet_deraining` and `mirnet_lowlight` are
  **FID unverified** (rewritten by a removed tool) until the checkpoints are
  re-evaluated with `python -m training.fid_reeval`, which records its results
  in `fid_provenance.csv` (needs a GPU; not run yet).
- **Non-Destructive Pipelines**: The Run Pipeline action is non-destructive by
  default; a clean run needs an explicit option and a confirmation dialog.
- **Zero-Hang Pipeline Lifecycle**: GUI pipeline completion recovers from all
  terminal statuses (`success`, `warning`, `error`). A 1,500 ms reconciliation
  poll against `/api/pipeline/status` and an `isLatestCompleted` guard in
  `PipelineStepCards.tsx` keep step cards from staying in `RUNNING`.
- **OpenCV Variant Equivalence**: `health_checker.py` treats the four OpenCV
  distributions (`opencv-python`, `opencv-contrib-python` and their
  `-headless` counterparts) as mutually satisfying.
- **Toolchain Modernization**: `mosaicml-streaming` is removed; **Lightning AI
  LitData** and **WebDataset** are the canonical streaming primitives.
  **Ruff** (`>=0.9.0`) is the formatter and fast linter; Pylint runs as a
  validation gate with each project's own `.pylintrc`.
- **Physical MDS Transcoding**: 110.9 GB of legacy `.mds.zstd` shards were
  transcoded to WebDataset `.data` archives: `LemGendizedClassificationMaster`
  (68.7 GB, 789 shards; 693,040 train + 94,965 val samples) and
  `LemGendizedMultitaskRestorationPro` (42.2 GB, 54 shards; 232,464 train +
  31,742 val samples).
- **PyTorch Stack**: the central `lemgendary-env-manager/requirements/*.txt`
  files pin `torch==2.15.0`, `torchvision==0.29.2`, `transformers==5.22.1` and
  `numpy==2.5.4` for `lemgendary-training-suite` and `lemgendary-datasets`, plus
  `torchaudio==2.11.1` for the training suite. No wheel index is pinned:
  `select_cuda_torch_index()` in `system_probe.py` picks it from the hardware
  probe (`cu134`, `cu126`, `cu121` or `cu118` by NVIDIA driver version, ROCm,
  PyPI for Apple MPS, CPU otherwise).

---

## 2. Multi-Track Versioning Matrix

Each project keeps its own version line; the README changelog of each
repository is the source of the release version.

- **LemGendary Model Training Suite** (`v16.9.122-STABLE`): PyTorch training
  loops, Sawtooth Governor, pair-rule ratchet, epoch budget, model soup,
  optional SWA, FID re-evaluation tool.
  Entrypoint: `lemtrain` (for example `lemtrain train MODEL_KEY`).
- **LemGendary Dataset Compiler Suite** (`v16.9.84-STABLE`): shard synthesis,
  WebP transcoding, Kaggle and HF ingestion, 21 manifolds, task taxonomy.
  Entrypoints:
  `python cli.py` and `lemgendary_datasets_hub.ps1`.
- **LemGendary Environment Manager** (`v16.9.79-STABLE`): hardware probe,
  virtual environments, compliance audits, bug report endpoint, ecosystem
  registry (`ecosystem.json`). Entrypoints: `lem-env` and
  `lemgendary_env_manager.ps1`.
- **LemGendary AI Studio GUI** (`v2.10.57`): Tauri v2 desktop application and
  operator cockpit. Entrypoint: the `lemgendary-ai-studio-gui` executable.
- **LemGendary AI Documentation Hub** (`v16.9.95-STABLE`): whitepapers,
  manuals and HTML papers. Entrypoint: `lemgendary-docs/index.html`.
- **LemGendary Trained Models Repo** (`v16.9.16-STABLE`): model weights, ONNX
  exports and metrics in `LemGendaryModels/<model_key>/`.
- **Training Pathology Guide** (`1.9.0`, baseline `v16.9.138-STABLE`):
  `PAPER_TRAINING_PATHOLOGY.md`.
- **Forex Predictor Specification** (`v2.7.1`): `PAPER_FOREX_PREDICTOR.md`.

The package metadata matches the README releases: the LemGendary Model
Training Suite writes its version only in `pyproject.toml` (`16.9.122`);
`training/version.py` reads it for the CLI, the sidecar, the health route and
`openapi.json`, and `config.yaml` has no version key (since v16.9.128). The
LemGendary Dataset Compiler Suite `core/cli_args.py` reports `16.9.84` (one
version string since v16.9.52).

---

## 3. Document Authority Hierarchy

To keep documentation and code consistent, all documentation follows the
four-tier authority hierarchy:

$$
\text{Code Manifests (SSOT)} \succ \text{Master Manuals} \succ
\text{Architectural Whitepapers} \succ \text{Educational Guides}
$$

1. **Level 1: Single Source of Truth Configuration Manifests**:
   - `unified_models_v2.yaml`, `unified_data.yaml`, `presets.yaml`,
     `openapi.json`.
   - Highest physical authority for parameters, architecture baselines and
     data bindings.
2. **Level 2: Master Operational & Technical Manuals**:
   - `MANUAL_AI_STUDIO_GUI.md`, `MANUAL_CLI.md`, `MANUAL_API.md`,
     `GUI_CONTROL_REGISTRY.md`.
   - Authoritative for operational workflows, control IDs, CLI flags and API
     payloads.
3. **Level 3: Architectural & Technical Whitepapers**:
   - `ECOSYSTEM_ARCHITECTURE.md`, `PAPER_TRAINING_SUITE.md`,
     `PAPER_DATASET_COMPILER.md`, `PAPER_AI_STUDIO_GUI.md`,
     `PAPER_ENV_MANAGER.md`, `PAPER_DEGRADATION_ENGINE.md`,
     `PAPER_TRAINING_PATHOLOGY.md` and the model deep-dive whitepapers.
   - Authoritative for optical formulations, asymptotic runtime complexity,
     memory sentinels and scientific citations.
4. **Level 4: Educational & Ecosystem Guides**:
   - `GENERAL_AI_TRAINING_KNOWLEDGE.md`, `GLOSSARY.md`,
     `LEMGENDARY_CURRENT_STATE.md`.
   - Reference material for engineering principles and deep learning theory.

The machine-readable registries `canonical_capabilities.json`,
`canonical_capabilities.yaml` and `manifest/documents.json` are updated
together and share the document baseline `v16.9.95-STABLE`.

---

## 4. Tripartite Microservice Topology & Port Bindings

The local orchestration layer runs three background sidecar services, each
bound to `127.0.0.1` and protected by the Origin Guard:

- **LemGendary Environment Manager**, port `8000` (HTTP / WebSocket): hardware
  sensing, venv provisioning, package drift analytics, compliance gating,
  masked secrets and the bug report endpoint (`POST /api/bug-report`).
- **LemGendary Dataset Compiler Suite**, port `8100` (HTTP / WebSocket):
  manifold sharding, WebP conversion, Kaggle sync hub and custom compilation.
- **LemGendary Model Training Suite**, port `8200` (HTTP / WebSocket):
  training job submission (`POST /api/training/train`), live loss streaming,
  GPU device allocation, model soup and SOTA audits.

The ports, the project list, the pipeline step names and the Kaggle owner
are defined once, in `lemgendary-env-manager/ecosystem/ecosystem.json`
(served by `GET /api/ecosystem`). The LemGendary Dataset Compiler Suite and
the LemGendary Model Training Suite read it through their `ecosystem`
loaders, the LemGendary AI Studio GUI through its snapshot
`src/generated/ecosystem.json`, and the `ecosystem_ssot` validation gate
(error severity since Environment Manager v16.9.52) fails validation when a
value is written anywhere else.

---

## 5. Registered Model Architectures & Convergence Status

The LemGendary Model Training Suite governs **23 registered models** tracked in
`unified_models_v2.yaml` and documented in `LemGendaryModels/<model_key>/`.
Registry categories are `forex`, `enhance`, `restoration`, `face`, `yolo` and
`llm`.

1. **Blind Face Restoration**: `codeformer` (Vector-Quantized Codebook Lookup)
2. **Atmospheric Dehazing**: `ffanet_indoor`, `ffanet_outdoor` (Feature Fusion
   Attention)
3. **Film Restoration**: `film_restorer` (Feature-Interpolated Motion
   Restorer)
4. **Quantitative Finance**: `forex_predictor` (Multi-Timeframe Causal
   CNN-Transformer)
5. **Exposure & Lighting Correction**: `mirnet_exposure`, `mirnet_lowlight`
   (Multi-Scale Residual Network)
6. **Precipitation Restoration**: `mprnet_deraining` (Cross-Stage Feature
   Fusion)
7. **High-Fidelity Restoration**: `nafnet_debluring`, `nafnet_denoising`
   (SimpleGate Nonlinearity-Free)
8. **Perceptual Quality Scoring**:
   - `nima_aesthetic_mobile` (MobileNetV3-Small EMD Scorer)
   - `nima_aesthetic_efficientnet` (EfficientNetV2-S Scorer)
   - `nima_aesthetic_pro` (Swin-v2-T Multiscale Scorer)
   - `nima_authenticity` (EfficientNetV2-S AI vs Human Generative Classifier)
   - `nima_technical` (EfficientNetV2-S Micro-Defect ISO Scorer)
9. **Face Parsing & Landmarks**: `parsenet`, `retinaface`
10. **Universal Restoration Engine**: `professional_multitask_restoration`
    (11-Head MoE Router)
11. **Super-Resolution**: `ultrazoom` (Sub-Pixel ESPCN / Residual SR)
12. **Content Moderation**: `universal_nsfw_classification` (GeM Pooling
    Safety Filter)
13. **Parameter Steering**: `upn_v2` (Continuous Parameter Predictor)
14. **Object Detection**: `yolov8n` (Anchor-Free CSPDarknet + PANet Curriculum
    Governor)
15. **Causal LLM Assistant**: `ai_helper_lemgend` (trained with
    `lemtrain llm train`)

Every model enforces the authoritative **4-Pillar Fully-Trained Verification
Invariant** (all SOTA targets met, top ladder rung reached, full data fraction,
at least 20 epochs):

$$
\text{FullyTrained} = \left(\bigwedge_{m} \text{Passed}(m, T_m)\right) \land
\text{LadderPassed} \land (\text{DataFraction} \ge 1.0) \land (\text{Epochs}
\ge 20)
$$

**FID unverified**: the historical FID values of `codeformer`,
`ffanet_indoor`, `mprnet_deraining` and `mirnet_lowlight` were rewritten by
the removed `tools/recalibrate_fid.py` and are not measured values. Any FID
value or chart from these four histories is unverified until the checkpoints
are re-evaluated with `feature=2048`. The tool for that is
`python -m training.fid_reeval` (training v16.9.107): it appends to
`LemGendaryModels/<model>/fid_provenance.csv` and never rewrites
`metrics.csv`. The re-measurement needs a GPU and has not been run.

**Training status in the GUI**: `GET /api/gui/models/with-stats` always
returns `training_status` (`fully_trained`, `partially_trained`,
`weights_ready`, `initializing` or `unknown`) and `is_fully_trained`. The
LemGendary AI Studio GUI shows that verdict and no longer derives it. A model
whose stats cannot be read is shown as `unknown` with the reason
(`stats_error`).

---

## 6. Manifold Ingestion & Container Modernization

- **Storage Location**: LemGendary Compiled Manifolds Repo
  (`LemGendaryDatasets/`, suffix-free directory topology).
- **Container Formats**: WebDataset (`.data`/`.tar`), Lightning AI LitData
  (`.bin`), Apache Parquet (`.parquet`), Directory (`.webp`). The registry
  canonical formats are `webdataset` for vision models, `parquet` for
  `forex_predictor` and `directory` for `yolov8n`.
  - **Deprecated**: MosaicML MDS (`.mds`). All legacy `.mds.zstd` shards were
    transcoded to WebDataset `.data` archives. The `.data` extension is
    canonical across the ecosystem, bypassing Kaggle backend archive-sniffing
    heuristics that would otherwise expand multi-gigabyte containers into
    loose files.
- **Transcoding Standard**: In-flight 12-thread WebP zero-intermediate
  compression:
  - Input/Degraded: WebP Lossy ($q=92$).
  - Ground Truth Target: WebP High-Fidelity ($q=95$).
  - Alpha / Segmentation Masks: WebP Lossless.
- **Task Taxonomy**: `lemgendary-datasets/task_taxonomy.json` defines the task
  ids. Every registry entry in `unified_data.yaml` names its `task`; four are
  marked `task_confirmed: false` until the owner confirms them
  (`retinaface_mobilenet`, `nima_authenticity`, `forex_universe`,
  `ai_helper_lemgend`). The compiler writes `task_type` into each manifold's
  `dataset_info.yaml`, and the LemGendary Model Training Suite reads it (older
  manifolds without it are resolved through the taxonomy).

---

## 7. Cloud Training & Remote Synchronization Pipeline

- **Kaggle Pipelines (`kaggle_training/`)**: 23 standalone notebooks consuming
  attached input datasets directly from `/kaggle/input/` with zero redundant
  cloud downloads.
- **Google Colab Pipelines (`colab_training/`)**: 23 automated training
  pipelines synchronized idempotently to Google Drive via `push_to_drive.py`.
- **Kaggle Models Hub 4-Variation Publishing (`lemtrain sync push`)**:
  - Publishes 4 strictly isolated variations per model: `pytorch/default`
    (checkpoints and metrics), `pytorch/fp32` (native `.pt`), `onnx/fp16`
    (half-precision graph) and `onnx/fp32` (full-precision graph with `.data`
    sidecar).
  - Metadata comes from `LemGendaryModels/<key>/model_metadata.yaml` and is
    synchronized to the Kaggle REST API with resolved owner credentials.
  - Full fleet synchronization (`lemtrain sync push --all`) sequences all 23
    registered models with per-model progress telemetry routed to the Local
    Telemetry tab; Kaggle job events go to the Remote Cloud telemetry tab.
- **Bidirectional Metadata Sync**:
  - `push_kaggle_dataset_metadata` verifies that the remote repository exists
    via `ensure_kaggle_dataset_exists`.
  - If a target dataset slug does not exist on Kaggle, the synchronizer
    creates a minimal public placeholder dataset containing `README.md` first,
    which prevents `403 Forbidden` errors during metadata updates.
  - PowerShell (`lemgendary_datasets_hub.ps1` options `3` and `A`) and the
    LemGendary AI Studio GUI (`CompilerPanel.tsx` "Update Metadata Only" tab)
    update metadata without re-uploading multi-gigabyte data archives.

---

## 8. Hardware Sentinels & Physical Execution Constraints

- **GTX 1650 (4GB VRAM) Edge Baseline**: Sub-nuclear 4GB lockdown enforces
  Serial-Only Mode upon memory saturation, eliminating Windows System RAM
  pagefile thrashing (empirically measured $12.5\times$ batch retrieval
  acceleration from 3.43s down to 0.27s per batch when memory-mapped sequence
  manifolds on Windows enforce `num_workers=0`).
- **CUDA 12.6 Verified (cu126)**: NVIDIA GeForce GTX 1650 (Turing, `sm_75`,
  Driver 610.74) verified with `torch 2.14.1+cu126`. Hardware gates
  confirmed: FP32 matmul, FP16 autocast, Conv2D forward/backward,
  `torch.compile` eager fallback, ONNX Dynamo export (max diff 1.78e-07),
  Transformers 5.20.1 BERT/GPT2 CUDA inference and Torchvision CUDA NMS. BF16
  is unsupported on Turing as expected and is not selected.
- **Continuous Memory Formula**: Dynamic batch calculation scales continuously
  with available VRAM:

$$
B_{\text{safe}} = \left\lfloor \frac{\text{VRAM}_{\text{total}} \cdot
\text{safety} - \text{static\_overhead}}{\text{mem\_per\_sample}(\text{resolution})}
\right\rfloor
$$

- **Sawtooth VRAM Governor**: Halves batch sizes when memory pressure exceeds
  90% and scales up when headroom exceeds 40%.
- **Sub-Second Minibatch Cancellation**: Evaluates non-blocking cancellation
  listeners at batch boundaries, terminating execution within one batch cycle
  upon operator abort signals. Stop Training in the GUI shows an error when
  the cancel request fails.

---

## 9. Zero-Suppression Policy Compliance

The codebase follows the zero-suppression rules of `ROBOTS.md` across all
languages:

- **Python**: no `# type: ignore` or `# noqa` directives and no programmatic
  `warnings.filterwarnings` suppressions. The only `# pylint: disable`
  directives are seven inline `too-many-arguments` in the LemGendary Model
  Training Suite (CLI commands with one parameter per option and model
  constructors); its `.pylintrc` has no disables.
- **TypeScript & JavaScript**: no `@ts-ignore`, `@ts-expect-error` or
  `/* eslint-disable */` directives and no configuration diagnostic
  suppressions (`warnOnUnsupportedTypeScriptVersion: false` is banned).
- **Markdown**: no inline `markdownlint-disable` directives in the documents
  synchronized during the 2026-11 remediation.
- **Zero Silent Crashes**: Bare `except: pass` and empty `catch {}` blocks are
  forbidden. All errors must be explicitly typed, logged or surfaced to
  operators.
- **Root-Cause Resolution**: Warnings, type checks and dependency
  vulnerabilities are resolved through static type annotations, Pydantic
  schema validation, safe package upgrades and defensive programming.

---

## 10. Background Process Lifecycle Governance & Zombie Elimination

The ecosystem enforces deterministic process lifecycle management to prevent
orphaned child processes and CPU/VRAM resource leaks:

- **Recursive Process Tree Elimination**: Sidecar shutdown
  (`service_manager.stop_service`) and job cancellation (`jobs.py`) execute
  recursive tree termination (`taskkill /F /T /PID` on Windows, recursive
  signal propagation on POSIX), terminating both parent orchestrators and all
  spawned worker subprocesses. PID files (`server.pid`) are immediately
  written upon detached process creation, and listening process discovery
  features full netstat multi-format parsing for wildcard listening sockets.
- **Guaranteed Cleanup Handlers**: `atexit` child process sentinels prevent
  detached PyTorch training loops, Uvicorn workers or compilation scripts from
  persisting after cancellation or abnormal exit.
- **Telemetry & Unzip Progress Synchronization**: Kaggle dataset decompression
  streaming (`kaggle_importer.py`) and multi-stream telemetry tracking
  (`TelemetryProgressTracker.tsx`) keep operator progress bars in line with
  the physical disk and training state.
