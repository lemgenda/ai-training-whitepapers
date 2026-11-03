# LemGendary AI Studio GUI: Architectural Whitepaper

## Category 01.4 | Subpage of Master Ecosystem Architecture

**Parent Hub**: [Master Ecosystem Architecture](./ECOSYSTEM_ARCHITECTURE.md)

**Version**: `v2.10.36` (LemGendary AI Studio GUI) · **Last audited**:
2026-11-03

---

## Table of Contents

- [1. Abstract](#1-abstract)
- [2. High-Velocity Optimizations](#2-high-velocity-optimizations)
- [3. Hybrid Cloud & Registry
  Integration](#3-hybrid-cloud--registry-integration)
- [4. Multi-Modal & Format Resilience](#4-multi-modal--format-resilience)
- [5. Comparative Analysis / Benchmarks](#5-comparative-analysis--benchmarks)
- [6. Synthesis Flow & Topology](#6-synthesis-flow--topology)
  - [6.1 Dynamic Mesh Configuration & Protocol-Agnostic Origin
    Routing](#61-dynamic-mesh-configuration--protocol-agnostic-origin-routing)
  - [6.2 Universal Dynamic Configuration & Registry
    Editor](#62-universal-dynamic-configuration--registry-editor)
  - [6.3 Contextual UX Help & Micro-Documentation
    Layer](#63-contextual-ux-help--micro-documentation-layer)
  - [6.4 Dataset Compiler & Kaggle Cloud Synchronization
    Hub](#64-dataset-compiler--kaggle-cloud-synchronization-hub)
  - [6.5 Headless Windowless Service Lifecycle & Auto-Start on
    Launch](#65-headless-windowless-service-lifecycle--auto-start-on-launch)
  - [6.6 Test & Diagnostic Orchestrator
    Integration](#66-test--diagnostic-orchestrator-integration)
  - [6.7 Comprehensive Testing & Ecosystem Verification
    Battery](#67-comprehensive-testing--ecosystem-verification-battery)
  - [6.8 Ecosystem Maintenance & Governance
    Controls](#68-ecosystem-maintenance--governance-controls)
  - [6.9 Centralized State (Zustand) & S.O.L.I.D. Component
    Hierarchy](#69-centralized-state-zustand--solid-component-hierarchy)
  - [6.10 Multi-Variation Kaggle Model Hub Staging & Strict Isolation
    Contract](#610-multi-variation-kaggle-model-hub-staging--strict-isolation-contract)
  - [6.11 Three-Tab Real-Time Telemetry Stream & Responsive
    Cancellation](#611-three-tab-real-time-telemetry-stream--responsive-cancellation)
  - [6.12 Security Model](#612-security-model)
  - [6.13 Bug Reporting Subsystem](#613-bug-reporting-subsystem)
- [7. Unified Models Registry](#7-unified-models-registry)
- [8. Conclusion](#8-conclusion)

---

## 1. Abstract

The LemGendary AI Studio GUI (client version `v2.10.36`) is a hardware-aware
desktop orchestration system that gives machine learning workflows a
low-latency, deterministic control plane. It addresses developer friction,
process fragmentation and the high memory footprint of traditional web wrappers
by separating native operating system integration from presentation logic: a
Rust host (Tauri v2), a reactive React 18 frontend and local WebSocket telemetry
channels to three Python sidecars. Every sidecar request carries a client header
that the sidecars' origin guard checks, the window runs under a strict Content
Security Policy, and secrets are write-only from the GUI. A built-in bug
reporter packages a description, annotated screenshots, an optional screen
recording of the app window and recent telemetry into a local ZIP archive and
hands it to the operator's own mail client.

> [!NOTE]
> **Dual Versioning Architecture**: The desktop application and its backends use
> separate version tracks:
>
> 1. **LemGendary AI Studio GUI (`v2.10.36`)**: Governs the Tauri v2 desktop
>    application, the React 18 frontend and the Operator Manual
>    ([`MANUAL_AI_STUDIO_GUI.md`](./MANUAL_AI_STUDIO_GUI.md)). `package.json`
>    holds this version and `tauri.conf.json` reads it from there.
> 2. **Sidecar services (`v16.x`)**: The LemGendary Environment Manager (port
>    8000), LemGendary Dataset Compiler Suite (port 8100) and LemGendary Model
>    Training Suite (port 8200) each keep their own `v16.x` release line in their
>    README. Each sidecar publishes its contract as `openapi.json`, and the GUI
>    tests check request field names against those files. See the [Document
>    Authority Hierarchy & Versioning Policy](./VERSIONING_POLICY.md) for track
>    governance.

## 2. High-Velocity Optimizations

High-velocity desktop execution demands bounded event latency, minimal frame
rendering drops, and efficient non-blocking inter-process communication (IPC).
Traditional runtime environments such as Electron introduce severe memory bloat
and multi-second initialization delays. The LemGendary AI Studio GUI architecture
eliminates this overhead by leveraging native operating system webviews
(WebView2 on Windows, WebKitGTK on Linux) coordinated through a compiled Rust
runtime.

Let $\mathcal{E} = \{e_1, e_2, \dots, e_M\}$ denote the continuous stream of
telemetry events emitted by the backend Python orchestrator, and let $B$
represent the ring buffer size. The event ingestion latency across the local
WebSocket boundary is bounded by:

$$
T_{\text{ingest}} = \mathcal{O}\left(\frac{|\mathcal{E}|}{B} + \log B\right)
$$

The store keeps only the latest $B = 200$ events, so the log panel renders a
bounded number of DOM rows regardless of stream length:

$$
T_{\text{render}} = \mathcal{O}\left(V_{\text{DOM}} \cdot \Delta t\right), \quad
\text{where } V_{\text{DOM}} \le B \ll |\mathcal{E}|
$$

Memory scaling satisfies strict upper bounds:

$$
M_{\text{peak}} = M_{\text{core}} + \mathcal{O}(B \cdot S_{\text{event}})
$$

where $M_{\text{core}}$ represents the baseline resident set size of the webview
process, leaving room for memory-intensive PyTorch GPU kernels.

## 3. Hybrid Cloud & Registry Integration

The LemGendary AI Studio GUI operates as a unified operational bridge between
local edge compute hardware and distributed cloud execution clusters. The
interface connects directly to local Python execution runtimes, background
headless sidecars, and remote training harnesses.

The IPC communication architecture enforces a local isolation policy (section
6.12 describes the implementation):

$$
\text{AllowRPC}(origin, method) = \begin{cases} \text{True}, & \text{if } origin
\in \mathcal{A}_{\text{allow}} \land (method = \text{GET} \lor
\text{ClientHeader}) \\ \text{False}, & \text{otherwise} \end{cases}
$$

Hardware accelerator probing routes execution commands based on real-time
hardware telemetry:

$$
\mathcal{H}_{\text{target}} = \begin{cases} \text{CUDA}, & \text{if }
N_{\text{NVIDIA}} \ge 1 \land \text{DriverVersion} \ge 535.0 \\ \text{ROCm}, &
\text{if } N_{\text{AMD}} \ge 1 \land \text{HIP\_VISIBLE} = 1 \\
\text{DirectML}, & \text{if } \text{OS} = \text{Win32} \land N_{\text{DX12}} \ge
1 \\ \text{CPU}, & \text{fallback} \end{cases}
$$

Through registry synchronization, local model checkpoint directories are
verified against remote Kaggle manifolds and Hugging Face Hub registries.

## 4. Multi-Modal & Format Resilience

The desktop framework guarantees presentation and format resilience across
heterogeneous display topologies, high-DPI scaling factors, and multi-monitor
configurations. The design system is constructed entirely on native CSS custom
properties, eliminating runtime style evaluation overhead.

Format parsing resilience is governed by strict schema validation:

$$
\text{ValidatePayload}(P) = \begin{cases} \text{Accept}, & \text{if }
\text{Schema}(P) \equiv \mathcal{S}_{\text{Telemetry}} \\
\text{SanitizeFallback}, & \text{otherwise} \end{cases}
$$

Malformed JSON packets or corrupted log lines emitted by external compilers are
intercepted by the telemetry boundary, converted into structured error entries,
and rendered in monospace panels without destabilizing the React reconciliation
tree.

## 5. Comparative Analysis / Benchmarks

The following comparison of the Tauri v2 and React desktop stack against legacy
GUI solutions comes from internal measurements. No benchmark artifact is
published with this release, so treat the figures as indicative:

| Metric | Electron | PySide6 / Qt | AI Studio (Tauri v2) | Factor |
| :--- | :--- | :--- | :--- | :--- |
| Cold start launch time | 2,850 ms | 1,420 ms | 280 ms | $10.2\times$ |
| Idle RAM footprint (RSS) | 194 MB | 92 MB | 38 MB | $5.1\times$ |
| Telemetry events per second | 1,200 | 4,500 | 24,000 | $20.0\times$ |
| Executable size | 128 MB | 165 MB | 8.4 MB | $15.2\times$ |
| Leak in 24 h soak test | >400 MB | <25 MB | None observed | n/a |

## 6. Synthesis Flow & Topology

The LemGendary AI Studio GUI coordinates three headless sidecars:

1. **Native Host Layer (Rust & Tauri v2)**: Manages the window lifecycle, the
   Content Security Policy, the shell capability and background process launch.
2. **Tripartite Sidecar Mesh Boundary**:
   - **LemGendary Environment Manager (Port 8000)**: Probes host hardware,
     virtual environments, pip packages and npm workspaces; runs the clean
     install pipeline; stores secrets; receives bug reports.
   - **LemGendary Dataset Compiler Suite (Port 8100)**: Serves the dataset
     manifold catalog, format statistics, compiler presets, and compilation and
     modernization jobs.
   - **LemGendary Model Training Suite (Port 8200)**: Streams training runs, GPU
     utilization, loss convergence and export jobs.
3. **Reactive Presentation Layer (React 18 & Vanilla CSS)**: Subscribes to the
   sidecars over WebSockets and REST, with one store for telemetry, compilation
   jobs, training cards and log streams.

Since v2.10.32 the sidecar ports and the project folders come from the
committed snapshot `src/generated/ecosystem.json`, a copy of
`lemgendary-env-manager/ecosystem/ecosystem.json` that
`npm run sync:ecosystem` refreshes before `dev` and `build`;
`npm run check:ecosystem` fails when the snapshot differs from the source.

State updates follow unidirectional dispatch flows:

$$
\text{State}_{t+1} = \Phi(\text{State}_t, \text{TelemetryEvent})
$$

preventing UI race conditions and ensuring deterministic views during
high-throughput training epochs.

### 6.1 Dynamic Mesh Configuration & Protocol-Agnostic Origin Routing

The desktop frontend keeps all sidecar addresses in one configuration module
(`src/api/config.ts`, `MESH_SERVICES`):

- **Environment Overrides & Protocol Translation**: `VITE_ENV_MANAGER_URL`,
  `VITE_DATASET_COMPILER_URL` and `VITE_TRAINING_SUITE_URL` override the
  defaults; `toWebSocketUrl()` maps HTTP or HTTPS to WS or WSS.
- **Liveness Probes**: Each service entry has a `livenessPath`. The Environment
  Manager is probed on the constant-time `GET /api/ping`; the Dataset Compiler
  Suite and Model Training Suite on `GET /api/health`. The full health audit
  loads only in the Health view.
- **Semantic Origin Routing**: Telemetry frames carry an `origin` identifier
  (`"env-manager"`, `"dataset-compiler"`, `"training-suite"`), so stream
  filtering does not depend on port numbers or host names.
- **In-Place Telemetry Roll-Up**: `rollupTelemetryEvents()` coalesces
  carriage-return ticks (`\r`) and requirement installation ticks
  (`INSTALLING:`, `DOWNLOADING:`, `RESOLVING:`, `Collecting`,
  `Requirement already satisfied:`) in place, while batch metrics, loss values,
  learning rates and milestones stay as separate records.
- **Accessible Pipeline Telemetry Progress Engine**: `TelemetryProgressTracker`
  above the log stream shows live operations. For the package installation step
  an amber theme (`var(--accent-amber, #ffd166)`) shows requirement index,
  package name, download rate, ETA and an indeterminate bar while pip resolves.
- **TQDM & Ultralytics Telemetry Stream Parsing**: `progressParser.ts`
  recognizes tqdm and Ultralytics progress (`elapsed<remaining`, for example
  `<01:29:22`) and extracts the remaining time. It strips log timestamp prefixes
  (for example `11:11:36 PM`) and rejects purely numeric candidates, so YOLO and
  vision training streams resolve to the operation `TRAINING`.

### 6.2 Universal Dynamic Configuration & Registry Editor

The desktop interface embeds a non-blocking configuration and registry modal.
Operators can inspect and edit the core ecosystem configuration files:

- `unified_data.yaml`: Source definitions, upstream repositories (Kaggle,
  Hugging Face, GitHub, Google Drive), and annotation schemas.
- `unified_models_v2.yaml`: Model definitions, spatial ladder progressions, loss
  weightings, and manifold references.
- `config.yaml` / `presets.yaml`: Compiler presets, degradation configurations,
  and training defaults.
- `runtime_env.yaml`: Multi-environment overrides for local, Kaggle, Saturn
  Cloud, and Google Colab runtimes.
- `requirements.txt` / `package.json`: Dependency manifests, validated before
  saving.

The editor is a plain text area. Before writing, it sends the content to
`POST /api/manifests/validate` on the Environment Manager and shows the YAML or
JSON validation result.

### 6.3 Contextual UX Help & Micro-Documentation Layer

Interactive controls carry an inline contextual help tooltip badge
(`HelpTooltip`):

- **Visual Affordance**: A small circular help glyph next to form controls,
  buttons, toggles and status badges.
- **Hover Micro-Documentation**: A high-contrast tooltip explains in plain
  language what the action does, its CLI equivalent where one exists, and its
  consequences.
- **Accessibility & Zero-Distraction**: Tooltips follow WCAG 2.2
  non-interference guidelines and disappear when the pointer leaves, without
  covering the dashboard.

### 6.4 Dataset Compiler & Kaggle Cloud Synchronization Hub

The desktop interface integrates a visual control plane for the LemGendary
Dataset Compiler Suite (`Port 8100`):

- **Compilation Mode Switcher**:
  - **Standard Manifold Compilation**: Compiles a registered manifold
    (`POST /api/gui/quick-compile` with `model` and `preset`). The preset list
    comes only from the sidecar's `presets.yaml` (`GET /api/gui/presets`);
    "Server default" lets the sidecar apply its default preset, and an unknown
    preset shows the server's 422 detail with the valid names.
  - **Custom Multi-Source Compilation**: Aggregates Kaggle, Hugging Face, Google
    Drive and GitHub sources into a new manifold
    (`POST /api/gui/custom-compile`).
- **Card-Level Kaggle Cloud Synchronization**:
  - **Direct Manifold Actions**: Every manifold card offers `Update Metadata`
    (pushes the metadata without re-uploading data), `Download` (fetches the
    remote shards) and `Upload` (packages and publishes the local shards).
  - **Global Metadata & Index Synchronization**: The toolbar pushes metadata for
    all registered Kaggle datasets in one call
    (`POST /api/kaggle/update-metadata` with `all_datasets: true`) and
    regenerates the on-disk index (`POST /api/modernize/regenerate-manifolds`).
- **Production Manifolds Catalog, Modernization Queue & Scale Reduction**:
  - The catalog grid shows the production manifolds with shard counts, total
    samples, disk footprint, format breakdown (WebP, JPG, PNG), upstream source
    popovers and `COMPILED` badges.
  - The Modernization Queue sub-tab lists the server queue
    (`GET /api/modernize/queue`, a bare list) and dispatches parallel WebP
    transcoding (`POST /api/modernize/run`).
  - The Scale Reduction sub-tab derives downsampled dataset variants (10%, 25%,
    50%, 75%) for fast training iterations (`POST /api/modernize/reduce`).
- **Job Tracking**: Every job route returns a `DatasetJobResponse` whose `id`
  the panel shows; progress arrives over `WS /api/ws/events` and appears in the
  shared log panel.

### 6.5 Headless Windowless Service Lifecycle & Auto-Start on Launch

The desktop runtime starts sidecars without visible console windows on Windows,
Linux and macOS:

- **Zero-Window Background Execution**: On Windows the native `spawn_service`
  command uses `.venv/Scripts/pythonw.exe` with `CREATE_NO_WINDOW`
  (`0x08000000`). Standard input, output and error are discarded
  (`Stdio::null`), so sidecar output is read from the sidecars' own log files
  and WebSocket streams.
- **Service Control Routing**: Start, stop and start-all go to the Environment
  Manager (`POST /api/services/{id}/start`, `POST /api/services/{id}/stop`,
  `POST /api/services/start-all`) when its `/api/ping` answers. When it is
  offline, the desktop app falls back to the native Tauri commands
  `spawn_service` and `spawn_all_services`; a plain browser session shows a
  clear error instead.
- **Automated Mesh Bootstrapping**: On launch the GUI probes the three sidecars
  and starts the offline ones in the background, then keeps polling until they
  answer.
- **Rapid Decoupled Probing**: Liveness probes are cheap (section 6.1) and
  repeat every 4 seconds, independent of the full dependency audit.

### 6.6 Test & Diagnostic Orchestrator Integration

The Test & Diagnostic Orchestrator modal (`src/components/TestModal.tsx`) opens
from the "Tests & Diagnostics" header button (`#header-btn-test-modal`) and
offers:

1. **Fleet 1-Epoch Smoke Test**: Queues a 1-epoch pass across all 23 registered
   architectures (`POST /api/training/unit-test-all`); the console shows
   `QUEUED` with the job id.
2. **Training Suite Unit Battery**: Runs the Model Training Suite unit tests
   in-process (`POST /api/training/unit-test-run`).
3. **Dataset Compiler Unit Battery**: Runs the Dataset Compiler Suite tests
   in-process (`POST /api/llm/test-suite`).

Both unit test routes are resolved through `MESH_SERVICES`, so the modal
contains no hard-coded ports. Missing `failures` or `errors` arrays in a
response are normalized instead of crashing the modal, and Escape closes it.

### 6.7 Comprehensive Testing & Ecosystem Verification Battery

The GUI codebase is verified by an automated test battery:

- **Component & Integration Testing**: 183 Vitest tests and 21 Rust tests
  (release `v2.10.34`) cover sidecar routing, request field names against the sidecars'
  `openapi.json` files, the compiler and training panels, the config and secrets
  editors, the clean install dialog, the Report Issue modal and annotator, and a
  scan that fails when a `className` has no CSS rule.
- **Ecosystem Compliance**:
  `lem-env validate --project lemgendary-ai-studio-gui` checks zero-emoji
  compliance, ESLint, TypeScript typing (including `vite.config.ts`) and the
  accessibility contracts.

### 6.8 Ecosystem Maintenance & Governance Controls

The Health view embeds operational controls backed by the LemGendary Environment
Manager, together with a dependency audit across the Python virtual environments
and the GUI's npm packages:

- **Cross-Project Python Drift Matrix**: Compares `unified_requirements.yaml`
  with the installed wheels in `lemgendary-env-manager`, `lemgendary-datasets`
  and `lemgendary-training-suite`.
- **Desktop GUI Project Packages (NPM) Audit**: Reads `package.json` and
  `node_modules` of `lemgendary-ai-studio-gui`, including `@tauri-apps/api`,
  `@tauri-apps/plugin-shell`, `@radix-ui/react-progress`, `modern-screenshot`,
  `react`, `react-dom` and `zustand`.
- **Safe Package Upgrades & Dry Runs**: `POST /api/update` starts a background
  job and returns its `job_id` at once; progress arrives in the logs, and `409`
  means an update or the pipeline is already running.
- **Deep Cache Purges**: Cleans `__pycache__`, build remnants and staging
  residues and reports the recovered bytes (`POST /api/clean`).
- **Standardized Git Hooks**: Installs the pre-commit hooks with the zero-emoji
  and compilation gates (`POST /api/hooks/install`).
- **Multi-Gate Ecosystem Validation**: Runs the validation gates for all
  repositories (`POST /api/validate`).

### 6.9 Centralized State (Zustand) & S.O.L.I.D. Component Hierarchy

A central Zustand store (`src/store/useStudioStore.ts`) gives deterministic
state transitions without prop drilling:

- **Unified Global State Store**: Sidecar online status (ports 8000, 8100,
  8200), hardware telemetry, local and cloud training jobs, model and dataset
  caches, the log ring buffer (200 events) and the open modal (`activeModal`:
  `config`, `tests` or `bug-report`).
- **Single Responsibility Deconstruction**:
  - `TrainingPanel.tsx`: A coordinator for `ModelManifoldCard.tsx`,
    `TelemetryConsole.tsx` and `TrainingToolbar.tsx` (search, filters, notebook
    generation and "Push All Models to Kaggle").
  - `CompilerPanel.tsx`: A coordinator for `DatasetManifoldCard.tsx`,
    `DatasetCompilationForm.tsx`, `ModernizationQueueTable.tsx`,
    `ScaleReductionView.tsx` and `CompilerToolbar.tsx`.
  - `ConfigEditorModal.tsx`: Split into `ManifestEditorTab.tsx` (text editor
    with server-side YAML and JSON validation) and `SecretsEditorTab.tsx`
    (write-only credential editor, section 6.12).
  - `CloudTrainModal.tsx`: Uses `VariationIsolationChecker.tsx` for
    multi-variation validation.
  - `src/navigation/workspaceTabs.ts`: The tab ids, labels and help texts used
    by the sidebar, the `?tab=` parser and the bug report module select.
- **No Fake Catalogs (v2.10.34)**: The model and manifold catalogs come only
  from the sidecars. The hand-written fallback lists (`fallbackModels.ts`,
  `fallbackDatasets.ts`) and the `offline_placeholder` flag are removed. With a
  sidecar offline or returning an empty list, the training and compiler panels
  show an empty or offline state (the training panel with Retry) and reload
  when the sidecar answers.
- **Training Status Contract (v2.10.34)**: `training_status`
  (`TrainingStatus`: `fully_trained`, `partially_trained`, `weights_ready`,
  `initializing`, `unknown`) and `is_fully_trained` are required fields of the
  model catalog, as in the LemGendary Model Training Suite `ModelWithStats`
  schema; `stats_error` is passed through. The GUI no longer derives the status
  from pillars, epochs or checkpoints. The badge and the status filter use the
  sidecar verdict only; `unknown` shows an `UNKNOWN` badge with the reason and
  hides the metrics.
- **Control ID Registry**: Interactive controls carry stable DOM IDs listed in
  [`GUI_CONTROL_REGISTRY.md`](./GUI_CONTROL_REGISTRY.md); the registry is
  rebuilt from the `id` attributes in the source.
- **Shared Micro-Components & Utilities**:
  - `Modal.tsx`: Shared dialog with `role="dialog"`, `aria-modal`, a labelled
    title, a Tab focus trap, Escape closing only the innermost modal and focus
    returning to the opener.
  - `ValidationBanner.tsx`: Banner with message type detection (`info`,
    `success`, `warning`, `error`), dismiss buttons and WAI-ARIA alert and
    status semantics.
  - `HoverPinPopover.tsx`: CSS hover and semantic `<button>` pin popover that
    follows the `jsx-a11y` rules.
  - `src/utils/clipboard.ts`: Clipboard export with
    `navigator.clipboard.writeText` and a fallback for sandboxed webviews.

### 6.10 Multi-Variation Kaggle Model Hub Staging & Strict Isolation Contract

The desktop application orchestrates the LemGendary multi-variation distribution
contract on the Kaggle Models Hub:

- **Strict 4-Variation Isolation**: Enforces clean partition across isolated
  model directories:
  - Variation 1 (`pytorch/default`): Canonical PyTorch checkpoints
    (`checkpoints/` containing `best.pth`, `latest.pth`) alongside model cards
    and training metrics (`metrics.csv`).
  - Variation 2 (`pytorch/fp32`): Native full-precision PyTorch weights
    (`[Model].pt`).
  - Variation 3 (`onnx/fp16`): Edge-optimized half-precision ONNX computational
    graph (`[Model].onnx`).
  - Variation 4 (`onnx/fp32`): High-precision standard ONNX exports
    (`[Model]_FP32.onnx` and `.data` sidecar).
- **Single Source of Truth Metadata (`model_metadata.yaml`)**: Model
  documentation, licensing, fine-tunability, tags, and variation usage examples
  are managed in `model_metadata.yaml` and applied through the Kaggle REST API.
- **Fleet-Wide Kaggle Models Hub Push**: The "Push All Models to Kaggle" toolbar
  action (`POST /api/training/kaggle/push-all`) stages, validates and publishes
  all 23 registered architectures and their variations.
- **Pre-Upload Isolation Gate**:
  `GET /api/models/{model_key}/variations/validate` reports per variation
  whether the files are isolated before anything is uploaded.
- **Dry-Run Staging**: Operators can simulate staging and packaging locally
  before live Kaggle API uploads.

### 6.11 Three-Tab Real-Time Telemetry Stream & Responsive Cancellation

The Model Training Suite view has a three-tab telemetry console; the Dataset
Compiler Suite and Health views use the shared log panel:

- **Local Training Stream**: Worker execution logs, loss curves, gradient norms
  and spatial ladder transitions of local jobs.
- **Remote Cloud Stream**: Events of the attached remote job and of the job
  types `kaggle_train`, `kaggle_monitor` and `cloud_push`
  (`isRemoteTrainingEvent`); local events exclude them.
- **Ecosystem Mesh Stream**: Health probes, audit logs and service events across
  ports 8000, 8100 and 8200.
- **Accessible Radix UI Progress Architecture**: `@radix-ui/react-progress`
  shows a metrics header (operation, percentage, sizes, throughput and ETA)
  above the progress indicator.
- **In-Place Stream De-duplication**: Consecutive progress ticks are rolled up
  in place; step start, verification and completion records stay.
- **Confirmed Cancellation**: Stop sends `POST /api/jobs/{job_id}/cancel`. The
  job is cleared only when the sidecar answers `cancelled: true`; otherwise an
  error banner shows the sidecar's detail and the job stays. While a local job
  is attached, the panel polls `GET /api/jobs/{job_id}` every 3 seconds and
  clears the job on `completed`, `failed` or `cancelled`.

### 6.12 Security Model

The GUI and the three sidecars share one security contract:

- **Loopback Binding**: Each sidecar listens on `127.0.0.1` by default.
- **Origin Guard**: Each sidecar keeps an allow-list of origins in one module
  (`tauri://localhost`, `http://tauri.localhost`, `https://tauri.localhost`,
  `http://localhost:1420`, `http://127.0.0.1:1420`). A request whose `Origin` is
  not on the list gets `403`, and WebSocket handshakes from a foreign `Origin`
  are rejected.
- **Client Header**: Browser requests with an `Origin` that use `POST`, `PUT`,
  `PATCH` or `DELETE` must send `X-LemGendary-Client: ai-studio-gui`, else they
  get `403`. The GUI adds the header to every sidecar request through one helper
  (`sidecarFetch` in `src/api/http.ts`). Requests without an `Origin` (CLI,
  curl, tests) pass this check. Together, the allow-list and the header stop
  other web pages from calling the sidecars.
- **Content Security Policy**: `tauri.conf.json` sets a strict policy:
  `default-src 'self'`, `script-src 'self'`, `object-src 'none'` and
  `frame-src 'none'`; styles and fonts only from the app and Google Fonts;
  images from the app plus `data:` and `blob:` (for screenshots); `connect-src`
  limited to Tauri IPC, the three sidecars on ports 8000, 8100 and 8200 of
  `127.0.0.1` and `localhost`, and `https://fonts.gstatic.com` for font
  embedding in screenshots. A separate `devCsp` adds what the Vite dev server
  needs.
- **Masked Secrets**: `GET /api/secrets` returns for each credential only
  whether it is set (`has_value`) and its last 4 characters (`value_hint`). The
  Secrets editor shows `set (••••1234)`, `set` or `not set`. A password field
  replaces a value and a blank field keeps it, so the GUI never reads a stored
  secret back; after saving, the masked list is reloaded so typed values leave
  memory.
- **Shell Capability**: The capability file grants the main window
  `core:default` and `shell:allow-open` with the shell plugin's default scope
  (`http`, `https`, `mailto` and `tel` links); the Documentation Hub button
  uses it to open the hub in the system browser.
- **No Side Effects on GET**: Read requests do not change state; for example,
  `GET /api/secrets` no longer writes the secrets file.

### 6.13 Bug Reporting Subsystem

The "Report Issue" header button (`header-btn-report-issue`) opens
`BugReportModal`, built on the shared `Modal` component. The design keeps every
secret out of the app: there is no SMTP account, and the report never leaves the
machine except through the operator's own mail client.

- **Form**: Email, module (a select built from the sidebar tabs and preselected
  from the current tab), a description of 50 to 10,000 characters with a live
  counter, an "Attach telemetry" checkbox (on by default) and a strip of up to 5
  screenshots.
- **Screenshot Annotator**: `ScreenshotAnnotator` captures the app's root
  element with `modern-screenshot` 4.7.0 (pinned; elements marked
  `data-capture-exclude`, such as the modal itself, are left out). The operator
  draws one highlight rectangle and saves the image as WebP (quality 0.92), or
  PNG where the webview cannot export WebP, halved in size until it fits 5 MB.
- **Telemetry**: The recent log events are written as an RFC 4180 CSV file with
  the header `timestamp,status,source,message`.
- **Limits**: One module (`src/bugReport/limits.ts`) mirrors the server limits:
  5 screenshots of at most 5 MB each (PNG or WebP), telemetry at most 2 MB and
  80 MB per report.
- **Submission**: `submitBugReport()` posts the multipart form to the LemGendary
  Environment Manager (`POST /api/bug-report`) with `app_version` and
  `current_tab`. The server checks file types by their leading bytes, writes
  `report.csv`, saves `bug_report_<timestamp>.zip` to the `bug-reports` folder
  at the workspace root, opens the mail client (`mailto:`) with recipient and
  subject filled in, and opens the folder through a typed platform adapter.
  Recipient and subject live in the Environment Manager's configuration.
- **Results and Errors**: The success view shows the archive name and relative
  path, the recipient and subject with copy buttons, and a note when the mail
  client or folder did not open. Errors map to `offline` ("Environment Manager
  is not running"), `validation` (422 entries shown under the matching field by
  `loc`), `too_large` (413) and `server`.
- **Screen Recording (v2.10.20)**: A native recorder in
  `src-tauri/src/recording/` captures only the app's own window with Windows
  Graphics Capture (Windows only), scales frames into an even-sized 854x480 box,
  encodes H.264 with openh264 at 24 fps and muxes an MP4 in memory. A pure state
  machine handles start, pause, continue and stop with a 60-second limit on
  unpaused time. The commands are `recording_start`, `recording_pause`,
  `recording_resume`, `recording_stop` and `recording_status`; other platforms
  return "not supported on this platform yet". In the form, `RecordingSlot`
  offers "Start recording"; while recording, the dialog hides and
  `RecordingControlBar` shows the timer, Pause/Continue and "Stop and attach".
  `RecordingController` polls the native status every 250 ms and stops at the
  limit or on a capture failure. The clip is sent as `recording.mp4` (the
  Environment Manager accepts `video/mp4` up to 50 MB).

## 7. Unified Models Registry

The desktop application integrates directly with the LemGendary Unified Models
Registry. Through the GUI, researchers inspect active model weights, monitor
dynamic spatial ladder progression, track training metrics (PSNR, SSIM, LPIPS,
Quality Score), and trigger ONNX exports across all registered vision and
financial models. One request (`GET /api/gui/models/with-stats`) returns every
model together with its latest resolution, data fraction and epochs from
`metrics.csv`.

The registry binding invariant verifies:

$$
\forall m \in \mathcal{M}_{\text{registry}}, \quad
\text{Exists}(m.\text{checkpoint}) \implies \text{ValidCheckpointHeader}(m) =
\text{True}
$$

This gives operators a visual check of checkpoint integrity before cloud
deployments or edge quantization.

## 8. Conclusion

The LemGendary AI Studio GUI delivers a modern, lightweight, and robust control
center for machine learning engineering. By replacing bulky web runtimes with a
Tauri v2 shell, a reactive React 18 interface, a tripartite sidecar mesh guarded
by an origin allow-list and client header, a universal configuration editor with
write-only secrets, a local-first bug reporter and contextual hover
micro-documentation, the system sets a high bar for developer ergonomics,
resource efficiency and ecosystem stability.
