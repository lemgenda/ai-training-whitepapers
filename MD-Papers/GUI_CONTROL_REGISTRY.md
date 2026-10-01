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
| `dash-btn-refresh-audit` | "Refresh Audit" | `<button>` | `POST /api/audit/system` (8000) | Triggers asynchronous system probe and updates all status cards. |
| `dash-badge-sidecar-status` | Connection Status Indicator | `<span>` | `WS /ws/telemetry` (8000) | Displays emerald glow for online or rose alert for offline. |
| `dash-card-hardware` | System & Hardware Architecture | `<div>` | `GET /api/hardware` (8000) | Renders CPU core counts, total RAM, and detected GPU adapters. |
| `dash-btn-clean-install` | "Execute Full Clean Install Pipeline" | `<button>` | `POST /api/pipeline/clean-install` | Initiates the 7-stage deterministic provisioning sequence. |
| `pipe-stage-1-hardware` | Stage 1: Hardware Discovery | `<li>` | `GET /api/probe/gpu` (8000) | Queries DXGI and NVML interfaces for compute acceleration. |
| `pipe-stage-4-reqs` | Stage 4: Requirements Sync | `<li>` | `POST /api/env/sync` (8000) | Copies requirements manifests and executes pip install. |
| `pipe-stage-6-verify` | Stage 6: Codebase Verification | `<li>` | `POST /api/validate/bytecode` (8000) | Compiles scripts via `py_compile` and audits zero-emoji rules. |
| `proj-card-training` | `lemgendary-training-suite` Card | `<div>` | `GET /api/env/training-suite` | Details virtual environment path, packages, and health status. |
| `proj-btn-reconcile-datasets` | "Reconcile lemgendary-datasets" | `<button>` | `POST /api/env/reconcile` (8000) | Reconciles dataset compiler dependencies against manifest. |
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
| `train-select-model` | Model Architecture Dropdown | `<select>` | `GET /api/models` | Selects target backbone (NAFNet, MIRNet, MPRNet, NIMA, etc.). |
| `train-btn-launch` | "Launch Master Training" | `<button>` | `POST /api/training/launch` | Dispatches training worker with spatial resolution ladder. |

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
