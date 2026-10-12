# LemGendary AI Studio Desktop GUI: Control ID Registry & Operational Boundaries

## Category 04 CONTROLS | LemGendary AI Documentation Hub

---

## 1. Abstract & Scope

This authoritative specification establishes the formal machine-readable Control ID Registry and operational boundary matrix for the LemGendary AI Studio Desktop GUI (`lemgendary-ai-studio-gui`). To enable automated end-to-end testing, accessibility compliance (WCAG 2.1 AA), and strict contract binding between the Tauri/TypeScript frontend and backend FastAPI sidecars (`port 8000` & `port 8100`), every interactive widget, input control, action button, telemetry stream, and visual card is assigned a unique, immutable control identifier.

---

## 2. Control ID Taxonomy & Schema

All GUI elements follow a structured hyphenated taxonomy:

$$\mathbf{[view]\text{-}[component]\text{-}[element]\text{-}[action]}$$

* **`[view]`**: Top-level route context (`dash`, `pipe`, `proj`, `health`, `telem`, `comp`, `train`).
* **`[component]`**: Sub-container or card (`header`, `sidebar`, `card`, `table`, `modal`).
* **`[element]`**: Structural HTML element type (`btn`, `input`, `select`, `toggle`, `badge`, `log`).
* **`[action]`**: Operational intent (`refresh`, `execute`, `reconcile`, `compile`, `filter`).

---

## 3. Master Interactive Controls Dictionary

| Control ID | UI Component / Label | Element Type | Bound Sidecar Endpoint | Expected Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `dash-nav-sidebar` | Sidebar Navigation Container | `<nav>` | — | Houses top-level route switches. |
| `dash-btn-refresh-audit` | "Refresh Audit" | `<button>` | `GET /api/health` (8000) | Triggers asynchronous system probe and updates all status cards. |
| `dash-badge-sidecar-status` | Connection Status Indicator | `<span>` | `WS /ws/telemetry` (8000) | Displays emerald glow for online or rose alert for offline. |
| `dash-card-hardware` | System & Hardware Architecture | `<div>` | `GET /api/hardware` (8000) | Renders CPU core counts, total RAM, and detected GPU adapters. |
| `dash-btn-clean-install` | "Execute Full Clean Install Pipeline" | `<button>` | `POST /api/pipeline/run` (8000) | Initiates the 7-stage deterministic provisioning sequence. |
| `pipe-stage-1-hardware` | Stage 1: Hardware Discovery | `<li>` | `GET /api/hardware` (8000) | Queries DXGI and NVML interfaces for compute acceleration. |
| `pipe-stage-4-reqs` | Stage 4: Requirements Sync | `<li>` | `POST /api/pipeline/run` (8000) | Copies requirements manifests and executes pip install. |
| `pipe-stage-6-verify` | Stage 6: Codebase Verification | `<li>` | `POST /api/pipeline/run` (8000) | Compiles scripts via `py_compile` and audits zero-emoji rules. |
| `proj-card-training` | `lemgendary-training-suite` Card | `<div>` | `GET /api/projects` (8000) | Details virtual environment path, packages, and health status. |
| `proj-btn-reconcile-datasets` | "Reconcile lemgendary-datasets" | `<button>` | `POST /api/services/start-all` (8000) | Reconciles dataset compiler dependencies against manifest. |
| `health-table-drift` | Cross-Project Version Drift Table | `<table>` | `GET /api/health/drift` (8000) | Renders comparative grid of shared dependencies. |
| `drift-badge-sync` | "[SYNC]" Status Badge | `<span>` | — | Indicates identical package versions across all active repositories. |
| `drift-badge-alert` | "[DRIFT]" Alert Badge | `<span>` | — | Highlights version discrepancies across projects. |
| `telem-log-stream` | Monospace Telemetry Terminal | `<pre>` | `WS /ws/log` (8000) | Renders high-velocity log stream from active sub-processes. |
| `comp-select-manifold` | Manifold Target Selector | `<select>` | `GET /api/gui/datasets/with-stats` (8100) | Populates list of 22 canonical training manifolds. |
| `comp-toggle-transcode` | "Enable WebP Transcoding" | `<input type=checkbox>` | `POST /api/gui/quick-compile` (8100) | Activates $q=92$ WebP image and lossless mask encoding. |
| `comp-btn-compile` | "Compile Manifold" | `<button>` | `POST /api/gui/quick-compile` (8100) | Dispatches dataset compilation job to the dataset sidecar. |
| `comp-mode-standard` | "Standard Manifold Compilation" | `<button>` | — | Switches compilation interface to standard preset mode. |
| `comp-mode-custom` | "Custom Multi-Source Compilation" | `<button>` | — | Switches compilation interface to custom multi-source mode. |
| `comp-input-custom-name` | "Custom Manifold Name" | `<input type=text>` | — | Specifies unique identifier for custom dataset synthesis. |
| `comp-select-custom-task` | "Domain Task" | `<select>` | — | Selects target ML domain (restoration, detection, segmentation). |
| `comp-select-custom-format` | "Container Architecture" | `<select>` | — | Selects target format (WebDataset, Parquet, MDS, LitData). |
| `comp-textarea-sources` | "Source Repositories & Dataset URLs" | `<textarea>` | — | Multi-line input for Kaggle, HF, GD, GH repositories. |
| `comp-btn-custom-compile` | "Compile Custom Dataset" | `<button>` | `POST /api/gui/custom-compile` (8100) | Dispatches multi-source aggregation and sharding job. |
| `comp-tab-kaggle-download` | "Download from Kaggle" Subtab | `<button>` | — | Activates Kaggle cloud download controls. |
| `comp-tab-kaggle-upload` | "Upload to Kaggle" Subtab | `<button>` | — | Activates Kaggle manifold upload controls. |
| `comp-select-kaggle-registry` | "Select Registry Dataset" | `<select>` | `GET /api/kaggle/registry-datasets` (8100) | Lists 20 canonical Kaggle-bound production manifolds. |
| `comp-input-kaggle-custom-ref` | "Kaggle Dataset Link or Slug" | `<input type=text>` | — | Input for direct Kaggle URLs or owner/dataset references. |
| `comp-btn-kaggle-download` | "Download from Kaggle" | `<button>` | `POST /api/kaggle/download` (8100) | Queues download and extraction of Kaggle datasets. |
| `comp-select-kaggle-upload` | "Local Compiled Manifold" | `<select>` | — | Selects compiled local manifold for packaging. |
| `comp-btn-kaggle-upload` | "Upload to Kaggle" | `<button>` | `POST /api/kaggle/upload` (8100) | Packages and streams local manifold to Kaggle. |
| `comp-btn-update-all-kaggle` | "Update All Kaggle Metadata" | `<button>` | `POST /api/kaggle/update-metadata` (8100) | Bulk pushes metadata to Kaggle for all 20 canonical manifolds. |
| `comp-btn-regen-manifolds` | "Regenerate Manifolds Index" | `<button>` | `POST /api/modernize/regenerate-manifolds` (8100) | Regenerates master manifolds.json and dataset-metadata.json files. |
| `comp-subtab-catalog` | "Manifolds Catalog" Subtab | `<button>` | — | Shows the 21 production manifold cards with WebP/PNG breakdown. |
| `comp-subtab-modernize` | "Modernization Queue & Transcode" Subtab | `<button>` | — | Activates legacy format scan and batch WebP transcode queue. |
| `comp-subtab-reduce` | "Scale Reduction (Downsample)" Subtab | `<button>` | — | Activates spatial downsample and dataset scaling derivation view. |
| `comp-btn-scan-modernize-queue` | "Scan Queue" | `<button>` | `GET /api/modernize/queue` (8100) | Scans local datasets and builds transcode modernization queue. |
| `comp-btn-batch-modernize-all` | "Batch Modernize All" | `<button>` | `POST /api/modernize/run` (8100) | Dispatches batch modernization job across queued manifolds. |
| `comp-slider-modernize-workers` | "Parallel Workers Slider" | `<input type=range>` | — | Configures worker thread count for parallel WebP transcoding. |
| `comp-select-reduce-manifold` | "Target Manifold Selector" | `<select>` | — | Chooses dataset manifold for scale reduction / downsampling. |
| `comp-btn-dispatch-reduce` | "Dispatch Reduction" | `<button>` | `POST /api/modernize/reduce` (8100) | Initiates downsampling derivation job for selected manifold. |
| `train-select-model` | Model Architecture Dropdown | `<select>` | `GET /api/gui/models/with-stats` (8200) | Selects target backbone (NAFNet, MIRNet, MPRNet, NIMA, etc.). |
| `train-btn-launch` | "Launch Master Training" | `<button>` | `POST /api/gui/quick-train` (8200) | Dispatches training worker with spatial resolution ladder. |
| `train-btn-unit-test-all` | "Run 1-Epoch Diagnostic (All 22 Models)" | `<button>` | `POST /api/training/unit-test-all` (8200) | Dispatches 1-epoch diagnostic smoke test across all models. |
| `train-btn-generate-all-notebooks` | "Generate All Notebooks" | `<button>` | `POST /api/notebooks/generate-all` (8200) | Batch generates notebooks across all 22 registered architectures. |
| `train-card-btn-eval` | "Evaluate Model" | `<button>` | `POST /api/training/evaluate` (8200) | Evaluates checkpoint against validation benchmark criteria. |
| `train-card-btn-export` | "Export Binaries" | `<button>` | `POST /api/training/export` (8200) | Compiles model to ONNX, PyTorch, and WebGPU binary formats. |
| `train-modal-tab-upload` | "Upload Checkpoints" Tab | `<button>` | — | Stages and uploads local model checkpoints directly to Kaggle Models. |
| `health-btn-safe-upgrade` | "Safe Package Upgrade" | `<button>` | `POST /api/update` (8000) | Safely upgrades outdated packages with rollback validation. |
| `health-btn-upgrade-dry-run` | "Upgrade Dry Run" | `<button>` | `POST /api/update` (8000) | Previews dependency upgrade plan without altering disk state. |
| `health-btn-deep-clean` | "Deep Cache Purge" | `<button>` | `POST /api/clean` (8000) | Purges build caches, **pycache**, and staging residues. |
| `health-btn-install-hooks` | "Install Git Hooks" | `<button>` | `POST /api/hooks/install` (8000) | Installs or repairs standardized pre-commit validation hooks. |
| `health-btn-validate-ecosystem` | "Run Ecosystem Validation" | `<button>` | `POST /api/validate` (8000) | Runs full multi-gate ecosystem code validation suite. |

---

## 4. End-to-End Operational Workflows

### 4.1 Workflow 1: Environment Provisioning & Health Audit

1. Operator launches LemGendary AI Studio Desktop GUI.
2. Operator observes `dash-badge-sidecar-status` confirming emerald connection state.
3. Operator clicks `dash-btn-clean-install`.
4. The GUI displays progressive completion across badges `pipe-stage-1-hardware` through `pipe-stage-7-health`.
5. Upon completion, `health-table-drift` updates, confirming 100% synchronized `[SYNC]` badges.

### 4.2 Workflow 2: Manifold Compilation with WebP Transcoding

1. Operator navigates to Dataset Compiler View (`comp-nav-tab`).
2. Operator selects `comp-select-manifold` (e.g. `nima_aesthetic`).
3. Operator verifies `comp-toggle-transcode` is enabled (WebP $q=92$).
4. Operator clicks `comp-btn-compile`.
5. The GUI establishes a live WebSocket connection to `ws://127.0.0.1:8100/api/ws/jobs/{id}/logs`, rendering real-time image conversion velocity (img/sec) and ETA countdowns directly in `telem-log-stream`.

---

## 5. Operational Boundaries & Platform Availability

The Desktop GUI enforces strict hardware and platform execution boundaries:

| Capability | Windows 10/11 (CUDA 12+) | Linux (CUDA 12+) | Windows (DirectML) | macOS / CPU Fallback |
| :--- | :---: | :---: | :---: | :---: |
| **Sidecar REST Daemon** | Supported | Supported | Supported | Supported |
| **Clean Install Pipeline** | Full Support | Full Support | Restricted (DirectX) | Restricted |
| **WebP Transcoding** | $\mathcal{O}(1)$ Multi-Threaded | $\mathcal{O}(1)$ Multi-Threaded | Multi-Threaded | Single-Threaded |
| **Hardlink Deduplication** | Supported (NTFS `os.link`) | Supported (POSIX `os.link`) | Supported (NTFS) | Unsupported (FAT/ExFAT) |
| **Model Training (FP16/BF16)** | Full GPU Acceleration | Full GPU Acceleration | Unsupported | Unsupported (CPU Only) |
| **Spatial Ladder Scaling** | Full GPU Tensor Core | Full GPU Tensor Core | Degraded Throughput | Blocked (Excessive Latency) |

> [!CAUTION]
> Training operations on CPU or uncalibrated DirectML backends will automatically be blocked by the GUI validation gate to prevent thermal runaway and severe memory stalls.
