# LemGendary Ecosystem: Master CLI Operations Manual

## Category 00 | LemGendary AI Documentation Hub

---

## Table of Contents

- [1. Executive Overview](#1-executive-overview)
- [2. Environment Manager CLI (`lem-env`)](#2-environment-manager-cli-lem-env)
  - [2.1 Global Options & Invocation](#21-global-options--invocation)
  - [2.2 Hardware Probing (`probe`)](#22-hardware-probing-probe)
  - [2.3 Ecosystem Health Audit (`audit`)](#23-ecosystem-health-audit-audit)
  - [2.4 Smart Clean Install Pipeline (`install`)](#24-smart-clean-install-pipeline-install)
  - [2.5 Safe Bottom-Up Package Upgrades (`update`)](#25-safe-bottom-up-package-upgrades-update)
  - [2.6 Manifest Synchronization (`sync`)](#26-manifest-synchronization-sync)
  - [2.7 Multi-Gate Validation Engine (`validate`)](#27-multi-gate-validation-engine-validate)
  - [2.8 Workspace Cache & Residue Purge (`clean`)](#28-workspace-cache--residue-purge-clean)
  - [2.9 Telemetry Daemon & Background Server (`serve`)](#29-telemetry-daemon--background-server-serve)
  - [2.10 Git Hook Installation (`setup-hooks`)](#210-git-hook-installation-setup-hooks)
- [3. Interactive PowerShell Host (`lemgendary_env_manager.ps1`)](#3-interactive-powershell-host-lemgendary_env_managerps1)
- [4. AI Studio Desktop GUI CLI & Toolchain](#4-ai-studio-desktop-gui-cli--toolchain)
- [5. Datasets Compilation Suite CLI](#5-datasets-compilation-suite-cli)
  - [5.1 Invocation Syntax](#51-invocation-syntax)
  - [5.2 Manifold Compilation (`compile`)](#52-manifold-compilation-compile)
  - [5.3 Degradation Engine Synthesis (`degrade`)](#53-degradation-engine-synthesis-degrade)
  - [5.4 Audit, Deduplication & Hardlinks (`audit`)](#54-audit-deduplication--hardlinks-audit)
  - [5.5 Retroactive Transcoding (`transcode`)](#55-retroactive-transcoding-transcode)
  - [5.6 Smart Multi-Modal Generation (`label`, `prompt`, `mask`)](#56-smart-multi-modal-generation-label-prompt-mask)
  - [5.7 Variant Reduction & Modernization (`reduce`, `modernize`)](#57-variant-reduction--modernization-reduce-modernize)
  - [5.8 Sidecar API Server (`server`)](#58-sidecar-api-server-server)
  - [5.9 Ecosystem Delegation (`env`)](#59-ecosystem-delegation-env)
  - [5.10 Cloud & Metadata Sync (`sync`, `docs`, `config`)](#510-cloud--metadata-sync-sync-docs-config)
  - [5.11 Canonical Compiler Presets (`presets`)](#511-canonical-compiler-presets-presets)
  - [5.12 Forex Universe & Parquet Operations (`forex`)](#512-forex-universe--parquet-operations-forex)
- [6. Training Suite CLI (`lemtrain` / `python cli.py`)](#6-training-suite-cli-lemtrain--python-clipy)
  - [6.1 Invocation Syntax & Global Help](#61-invocation-syntax--global-help)
  - [6.2 Model Training (`train`)](#62-model-training-train)
  - [6.3 Checkpoint Evaluation (`eval`)](#63-checkpoint-evaluation-eval)
  - [6.4 Model Compilation & Export (`export`)](#64-model-compilation--export-export)
  - [6.5 Notebook Generation (`notebooks`)](#65-notebook-generation-notebooks)
  - [6.6 Checkpoint Management (`checkpoints`)](#66-checkpoint-management-checkpoints)
  - [6.7 Canonical Presets (`presets`)](#67-canonical-presets-presets)
  - [6.8 Hardware & Architecture Audit (`audit`)](#68-hardware--architecture-audit-audit)
  - [6.9 Cloud Synchronization (`sync`)](#69-cloud-synchronization-sync)
  - [6.10 Sidecar Daemon Operations (`server`)](#610-sidecar-daemon-operations-server)
- [7. Models Hub & Verification Toolchain](#7-models-hub--verification-toolchain)
- [8. Documentation Hub & Static Validation](#8-documentation-hub--static-validation)
- [9. Exit Codes, Automation & CI/CD Integration](#9-exit-codes-automation--cicd-integration)

---

## 1. Executive Overview

The LemGendary Ecosystem comprises seven specialized repositories orchestrated under a unified architectural contract.
All command-line operations are standardized, deterministic, and free of external visual noise or emojis.
The single authoritative command-line tool for ecosystem health, virtual environment lifecycles, and verification is `lem-env`,
located in `lemgendary-env-manager`.

Every toolchain command adheres strictly to semantic exit codes, making them directly suited for automated continuous integration,
local terminal workflows, and cross-project orchestration.

---

## 2. Environment Manager CLI (`lem-env`)

`lem-env` is packaged as a standard Python console application using Typer and Rich. It provides the central management interface
for inspecting hardware capabilities, provisioning isolated virtual environments, upgrading packages in dependency order,
and enforcing strict linting and compilation gates across all seven workspaces.

### 2.1 Global Options & Invocation

```bash
# General invocation syntax
lem-env [COMMAND] [OPTIONS]

# Help and discovery
lem-env --help
```

| Global Option | Type | Description |
| :--- | :--- | :--- |
| `--help` | Flag | Display comprehensive command usage, available subcommands, and flags |

---

### 2.2 Hardware Probing (`probe`)

The `probe` command discovers system hardware, compute accelerators, operating system architecture, MetaTrader 5 availability,
and checks for software update releases against upstream registries.

```bash
lem-env probe
```

Key features:

- Detects GPU acceleration backends including NVIDIA CUDA, AMD ROCm, Windows DirectML, and CPU fallback.
- Detects MetaTrader 5 terminal installations, install directories, and software versions.
- Queries `winget list` (installed version) and `winget show` (available version) to report both current and latest software versions with a status of `UP TO DATE`, `UPDATE AVAILABLE`, `NOT INSTALLED`, or `INSTALLED (not in winget)`.

MetaTrader 5 detection priority:

1. Windows registry keys under `HKCU`/`HKLM\SOFTWARE\MetaQuotes\Terminal` (fast, ~5 ms)
2. Well-known install paths (`C:\Program Files\MetaTrader 5\terminal64.exe`)
3. PowerShell `Get-Package -Name '*MetaTrader*'` (slow fallback)

When an install path is available, the version is read directly from `terminal64.exe`'s `FileVersion` metadata via PowerShell's `VersionInfo` property. This gives an authoritative version number even when winget has no record of the installation (typical for MT5, which is often installed outside winget's package database).

---

### 2.3 Ecosystem Health Audit (`audit`)

The `audit` command executes an exhaustive diagnostic audit of all seven repositories in the ecosystem.

```bash
# Full audit with per-project safety classification (~30-90s)
lem-env audit

# Fast audit — skips pip dry-runs
lem-env audit --fast
```

| Option | Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--fast` | None | Bool | `False` | Skip per-project pip safety dry-runs. Audit completes in seconds but the Safe-↑ column in the drift matrix is left empty. |

Diagnostic checks performed:

- Toolchain prerequisites verification for Python, Git, NPM, and MetaTrader 5.
- Virtual environment presence, Python executable health, and missing package count for each repository.
- Node.js workspace health, inspecting `package.json`, `node_modules`, and declared dependencies.
- Manifest Coverage: declared vs installed vs missing vs extra vs platform-skipped counts per project.
- Python Package Drift & Upgrade Status matrix. Every package declared in two or more manifests appears with:
  - **Pin type glyph**: `=` (exact `==`), `~` (range), `*` (floating), `·` (transitive install), empty (declared but not installed)
  - **Upgrade marker**: `↑` (safe update available), `⊘` (blocked by reverse dependency), none (at latest version)
- Packages Declared in Only One Manifest: full inventory of drift-invisible packages.
- NPM Package Dependency Matrix inspecting declared versus installed package versions.
- NPM Package Drift Across Workspaces.

Blocked upgrades include a reason string naming the requiring package and constraint, e.g. `pylint requires astroid<=4.1.dev0,>=4.0.2`.

---

### 2.4 Smart Clean Install Pipeline (`install`)

The `install` command runs the automated seven-step environment creation and package installation pipeline.

```bash
# Execute clean install across all ecosystem projects
lem-env install

# Target a specific repository
lem-env install --project lemgendary-training-suite

# Install without purging existing virtual environments
lem-env install --no-clean
```

| Option | Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--project` | `-p` | Text | `None` | Restrict installation to a single target repository |
| `--clean / --no-clean` | None | Bool | `True` | Completely purge existing `.venv` and `node_modules` before fresh recreation. The venv currently executing the pipeline is preserved automatically. |

The pipeline executes in sequential order:

1. Hardware discovery and backend acceleration detection.
2. Global toolchain verification (Python, Git, NPM).
3. Virtual environment provisioning and purge (skips the running venv).
4. Python package installation using locked manifests, followed by OpenCV variant normalization.
5. Node.js package installation via NPM.
6. Post-install validation (py_compile, lint, YAML, JSON, HTML/WCAG, domain gates).
7. Final ecosystem health audit generation.

---

### 2.5 Safe Bottom-Up Package Upgrades (`update`)

The `update` command safely resolves outdated dependencies and upgrades them bottom-up across the dependency hierarchy:
`lemgendary-env-manager` -> `lemgendary-datasets` -> `lemgendary-training-suite` -> `lemgendary-ai-studio-gui`.

```bash
# Inspect potential upgrades without modifying files
lem-env update --dry-run

# Apply upgrades and auto-sync requirement manifests
lem-env update
```

| Option | Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--project` | `-p` | Text | `None` | Target package upgrades for a specific repository |
| `--dry-run` | None | Bool | `False` | Display proposed version changes without executing installations |

Every candidate upgrade passes through a multi-layer safety pipeline before being applied:

1. **Reverse-dependency check**: `pip inspect --local` is used to build a reverse-dependency graph of every installed package. Any candidate whose target version would violate an installed package's requirement is marked `BLOCKED` with an explanation.
2. **Constraint-preserving dry-run**: Every non-target installed package is written into a temporary pip constraints file. If pip cannot resolve the target batch without downgrading or removing anything, the batch is split into per-package checks so a single bad candidate does not poison the whole set.
3. **CUDA-aware torch handling**: On CUDA hosts, `torch`, `torchvision`, and `torchaudio` are resolved against the PyTorch CUDA index (`download.pytorch.org/whl/cu121`). Only packages already installed in the project are considered; packages already at the newest CUDA build produce a `VERIFIED` event instead of a spurious `UPGRADED` event.
4. **Snapshot + rollback**: Each batch is snapshotted via `pip freeze`, applied, and verified with `pip check`. If the check fails, the batch is rolled back from the snapshot.

After all pip/npm upgrades complete, centralized manifests in `lemgendary-env-manager/requirements/` are automatically re-written to reflect actual installed versions. Packages in `PROTECTED_FROM_SYNC` (`astroid`, `pylint`, `pydantic`, `pydantic-core`) are passed through untouched to prevent a transient upgrade-time drift from being permanently encoded into the manifest.

---

### 2.6 Manifest Synchronization (`sync`)

The `sync` command captures currently installed packages from active virtual environments and synchronizes pinned requirement manifests
under `lemgendary-env-manager/requirements/`.

```bash
lem-env sync
```

Manifests maintained:

- `requirements-env-manager.txt`
- `requirements-datasets.txt`
- `requirements-training.txt`
- `lemgendary-ai-studio-gui.package.json`

This is called automatically by `install` and `update` — use directly only when you need to reset a project's requirements without running the full pipeline.

---

### 2.7 Multi-Gate Validation Engine (`validate`)

The `validate` command enforces strict quality, formatting, compilation, and domain integrity gates across all seven workspaces.

```bash
# Validate entire ecosystem
lem-env validate

# Validate specific project
lem-env validate --project lemgendary-docs
```

Validation gates enforced:

| Check | Tool | Projects |
| :--- | :--- | :--- |
| Python bytecode | `py_compile` | Python projects |
| Zero-emoji | Regex scan | All projects |
| JS/TS linting | ESLint (`--format json`) | `lemgendary-ai-studio-gui` |
| TypeScript types | `tsc --noEmit` | `lemgendary-ai-studio-gui` |
| JSON RFC 8259 | Python `json` (in-process) | All 7 repos |
| PowerShell syntax | `PSScriptAnalyzer` (`pwsh` preferred) | Repositories with `.ps1` |
| Markdown lint | `markdownlint-cli` | All 7 repos |
| YAML lint | `yamllint` (env-manager .venv) | All 7 repos |
| W3C HTML | `html-validate` | `lemgendary-docs` |
| CSS lint | `stylelint` | `lemgendary-docs` |
| WCAG 2.2 AA | `pa11y` | `lemgendary-docs` (static HTML) |
| Domain Verifications | `validator.py` ecosystem gates | All 7 repos (doc sync, parquet schemas, weights, Tauri) |

All Node.js validation tools are resolved locally from `lemgendary-env-manager/node_modules/.bin` via `_resolve_tool_cmd()`, eliminating global toolchain pollution.

> **Note on WCAG for the React app (`lemgendary-ai-studio-gui`)**: The Vite/React build produces a minimal `index.html` shell with a single `<div id="root">`. WCAG accessibility validation of the fully rendered UI requires a running dev server. The `validate` command runs ESLint and TypeScript checks for the GUI instead; WCAG should be run manually via `npx pa11y http://localhost:5173` against a live dev server.

---

### 2.8 Workspace Cache & Residue Purge (`clean`)

The `clean` command removes volatile temporary files, caches, and build artifacts to maintain absolute workspace hygiene.

```bash
# Clean entire workspace
lem-env clean

# Clean specific repository
lem-env clean --project lemgendary-training-suite
```

Purged items include:

- `__pycache__` directories and `.pyc` bytecode files.
- `.pytest_cache`, `.mypy_cache`, and `.ruff_cache`.
- Temporary build residues (`dist/`, `build/`, `*.egg-info`).
- Staging artifacts (`.staging_*`, `staging_*`, `.kaggle-partial`, `.tmp`, `.log`).

---

### 2.9 Telemetry Daemon & Background Server (`serve`)

The `serve` command launches the FastAPI REST API and WebSocket real-time telemetry server.

```bash
# Start server on default address
lem-env serve

# Start on custom interface and port
lem-env serve --host 0.0.0.0 --port 8000
```

| Option | Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--host` | `-h` | Text | `127.0.0.1` | Network interface address to bind the HTTP listener |
| `--port` | `-p` | Int | `8000` | TCP port for incoming REST and WebSocket connections |

Server lifecycle is managed via FastAPI's `@asynccontextmanager` lifespan handler, ensuring the background event-drain task is cancelled cleanly on shutdown.

---

### 2.10 Git Hook Installation (`setup-hooks`)

The `setup-hooks` command installs or repairs standardized pre-commit hooks across all ecosystem projects.

```bash
# Install hooks across all projects
lem-env setup-hooks

# Install for a single project
lem-env setup-hooks --project lemgendary-datasets
```

The installed hook delegates validation to `lem-env validate --project <name>` and blocks the commit if any gate fails. This ensures every repository runs the same validation pipeline regardless of local toolchain state.

---

## 3. Interactive PowerShell Host (`lemgendary_env_manager.ps1`)

For Windows terminal operators, `lemgendary_env_manager.ps1` provides an interactive, keyboard-driven management console.

Execution syntax:

```powershell
powershell -ExecutionPolicy Bypass -File .\lemgendary_env_manager.ps1
```

Interactive Menu Matrix:

- `[1] Probe System & Hardware Accelerators`: Executes hardware discovery and checks for updates.
- `[2] Run Full Ecosystem Health Audit`: Displays toolchain, virtual environment, manifest coverage, drift matrix, single-manifest inventory, and NPM dependency matrix.
- `[3] Execute Smart Clean Install Pipeline`: Purges environments and installs clean dependencies.
- `[4] Run Safe Package Updates`: Executes bottom-up dependency upgrades and syncs manifests.
- `[5] Validate Projects`: Enforces py_compile, ESLint, YAML, JSON, W3C, WCAG 2.2 AA, and domain gates.
- `[6] Start/Stop Background API Server`: Launches or stops the FastAPI server as a background PowerShell job with live WebSocket streaming.
- `[Q] Quit`: Gracefully terminates the management console.

---

## 4. AI Studio Desktop GUI CLI & Toolchain

The desktop application `lemgendary-ai-studio-gui` utilizes Node.js, React 18, Vite, and Tauri v2.

CLI Operations:

```bash
# Navigate to GUI directory
cd lemgendary-ai-studio-gui

# Start development frontend server
npm run dev

# Run TypeScript static type check
npm run typecheck

# Run ESLint with strict JSX accessibility rules
npm run lint

# Build production bundle
npm run build

# Run Tauri desktop development application
cargo tauri dev

# Build native desktop installer
cargo tauri build
```

---

## 5. Datasets Compilation Suite CLI

The `lemgendary-datasets` repository provides the unified `lemgendary` CLI (`cli.py`), exposing a full suite of compiler, synthesis, audit, transcoding, and server operations. All commands feature transparent hybrid routing: when the sidecar API daemon is active on `127.0.0.1:8100`, commands submit tasks to the API and render live WebSocket logs to Rich Console; when stopped or when `--no-server` is passed, commands fall back cleanly to direct in-process execution.

### 5.1 Invocation Syntax

```bash
# Navigate to datasets workspace
cd lemgendary-datasets

# General syntax
python cli.py [COMMAND] [OPTIONS]

# Help and discovery
python cli.py --help
python cli.py [COMMAND] --help
```

### 5.2 Manifold Compilation (`compile`)

Compiles raw image and market data into production-ready dataset manifolds with optional multi-container emission and quality gates:

```bash
# Standard compilation with default WebP q=92
python cli.py compile --model nima_aesthetic --max-gb 50

# Compile using canonical compiler preset (Phase 8)
python cli.py compile --model nima_aesthetic --preset quality-vision

# Concurrently emit WebP directory and MosaicML Streaming (MDS) container
python cli.py compile --model nima_aesthetic --image-format webp --image-quality 92 --also-format mds

# High-throughput compile bypassing aesthetic vetting and labeling
python cli.py compile --model nafnet_deblurring --workers 16 --no-vetting --no-labeling

# Force container byte duplication across hardlink gates
python cli.py compile --model upn_v2 --also-format mds --force-duplicate

# Force in-process compilation bypassing active API server
python cli.py compile --model nima_technical --no-server
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--model`, `-m` | String | `None` | Dataset registry key in `unified_data.yaml` |
| `--preset`, `-p` | String | `None` | Predefined compiler preset profile (`quality-vision`, `restoration-hardlinked`, `detection-variable`, `cloud-archival`) |
| `--max-gb` | Float | Config | Maximum size allocation threshold in gigabytes |
| `--workers` | Integer | Auto | Number of parallel worker threads/processes |
| `--image-format` | String | `webp` | Target format: `webp`, `jpeg`, `png`, `keep` |
| `--image-quality` | Integer | `92` | Target image compression quality (1-100) |
| `--target-quality` | Integer | `95` | Restoration target ground-truth quality |
| `--mask-format` | String | `webp-lossless` | Segmentation mask format |
| `--also-format` | String | `None` | Comma-separated containers: `mds`, `litdata`, `wds`, `parquet` |
| `--no-vetting` | Flag | `False` | Bypass NIMA aesthetic score gate |
| `--no-labeling` | Flag | `False` | Bypass YOLO detection auto-labeling |
| `--no-hash` | Flag | `False` | Bypass pHash/dHash perceptual deduplication |
| `--no-server` | Flag | `False` | Force local in-process execution |

### 5.3 Degradation Engine Synthesis (`degrade`)

Derives paired synthetic restoration manifolds from clean ground-truth sources using mathematical physical kernels:

```bash
# Motion blur and heteroscedastic sensor noise synthesis
python cli.py degrade --source raw-sets/div2k --output LemGendizedNafNetDebluringSynthetic --profile motion-blur+iso-noise

# Atmospheric haze synthesis on custom manifold directory
python cli.py degrade --source ../LemGendaryDatasets/LemGendizedNimaAesthetic --output LemGendizedHazySynthetic --profile rainy-haze --intensity high

# Dry-run validation
python cli.py degrade --source raw-sets/div2k --output LemGendizedTest --profile vintage-film --dry-run
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--source`, `-s` | String | Required | Source dataset folder or registered manifold name |
| `--output`, `-o` | String | Required | Destination synthetic manifold folder name |
| `--profile`, `-p` | String | `motion-blur+iso-noise` | Profile token or composite expression |
| `--intensity` | String | `medium` | Intensity preset: `low`, `medium`, `high` |
| `--pairs` | Integer | `None` | Maximum sample pair count cap |
| `--val-split` | Float | `0.12` | Validation set split ratio |
| `--seed` | Integer | `42` | Deterministic random number seed |
| `--image-format` | String | `webp` | Target output format for degraded images |
| `--dry-run` | Flag | `False` | Simulate derivation plan without writing files |

### 5.4 Audit, Deduplication & Hardlinks (`audit`)

Performs image integrity auditing, magic byte sniffing, aspect ratio filtering, perceptual hashing, and NTFS hardlink fraction accounting:

```bash
# Audit registered manifold
python cli.py audit --model nima_aesthetic

# Audit arbitrary filesystem directory with sample cap
python cli.py audit --manifold ../LemGendaryDatasets/LemGendizedUpnV2 --sample 1000
```

### 5.5 Retroactive Transcoding (`transcode`)

In-place atomic transcoding of existing manifold image sets to WebP with zero intermediate files:

```bash
python cli.py transcode --model nima_technical --image-format webp --image-quality 92
```

### 5.6 Smart Multi-Modal Generation (`label`, `prompt`, `mask`)

Runs GPU/CPU inference backends over compiled manifolds to generate labels, diffusion prompts, or segmentation masks:

```bash
# Multi-strategy label generation
python cli.py label --model parsenet --strategy parsenet_segmentation
python cli.py label --model nima_aesthetic --strategy blip_caption --device cuda

# Structured diffusion prompt generation
python cli.py prompt --model diffusion_master --template diffusers-v1

# Mask generation
python cli.py mask --model parsenet --strategy sam --device cuda
```

### 5.7 Variant Reduction & Modernization (`reduce`, `modernize`)

```bash
# Create downsampled reduced manifold variant
python cli.py reduce --max-gb 10

# Retire legacy `Large` suffix locally and in registry
python cli.py modernize --dry-run
python cli.py modernize --all --yes
python cli.py modernize --datasets nima_technical,nima_aesthetic --skip-kaggle

# Full modernization: suffix retirement, WebP transcoding, and modern container conversion
python cli.py modernize --datasets nima_aesthetic --image-format webp --also-format webdataset
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--all` | Flag | `False` | Select all eligible manifolds for modernization |
| `--yes`, `-y` | Flag | `False` | Skip interactive confirmation gate |
| `--dry-run` | Flag | `False` | Simulate modernization plan without file modification |
| `--datasets` | String | `None` | Comma-separated list of folder names, base names, or keys |
| `--skip-kaggle` | Flag | `False` | Skip Kaggle re-upload (local creation and metadata preserved) |
| `--image-format` | String | `webp` | Target format for image transcoding (`webp`, `jpeg`, `png`, `keep`) |
| `--image-quality` | Integer | `92` | Compression quality for image transcoding (1-100) |
| `--target-quality` | Integer | `95` | Quality floor for ground-truth restoration target transcoding |
| `--mask-format` | String | `webp-lossless` | Format for mask transcoding (`webp-lossless`, `png`) |
| `--also-format` | String | `webdataset` | Target container format (`webdataset`, `mds`, `litdata`, `parquet`) |
| `--skip-transcode` | Flag | `False` | Skip WebP image transcoding phase |
| `--skip-container` | Flag | `False` | Skip container format conversion phase |

### 5.8 Sidecar API Server (`server`)

Controls the local FastAPI and WebSocket daemon on `127.0.0.1:8100`:

```bash
# Launch background server daemon
python cli.py server start --background

# Inspect server status, uptime, and hardware sensors
python cli.py server status

# Gracefully terminate server daemon
python cli.py server stop
```

### 5.9 Ecosystem Delegation (`env`)

Delegates environment lifecycle and code validation directly to `lem-env`:

```bash
# Execute full multi-gate validation suite
python cli.py env validate

# Probe ecosystem health (fast mode)
python cli.py env status

# Provision clean virtual environment
python cli.py env install
```

### 5.10 Cloud & Metadata Sync (`sync`, `docs`, `config`)

```bash
# Kaggle dataset push and pull
python cli.py sync push --model nima_aesthetic
python cli.py sync pull --url lemgenda/lemgendizednimaaesthetic

# Documentation regeneration
python cli.py docs regen

# Schema validation
python cli.py config validate
```

### 5.11 Canonical Compiler Presets (`presets`)

Inspects canonical compilation profiles defined in `presets.yaml`:

```bash
# Display formatted table of available compiler presets
python cli.py presets list
```

The output provides a matrix of target formats, image quality percentages, aesthetic vetting gates, and auto-labeling toggles for each profile.

### 5.12 Forex Universe & Parquet Operations (`forex`)

Converts historical multi-symbol tick and M1/M15/H1/H4/D1 time-series arrays from legacy `.npy` containers into compressed, partitioned PyArrow Parquet manifolds with embedded schema metadata:

```bash
# Convert NPY market array files into Parquet
python cli.py forex convert --source ../raw-market-data/forex_manifold.npy --output ../LemGendaryDatasets/LemGendizedForex

# Embed column descriptions and metadata into Parquet tables
python cli.py forex embed --target ../LemGendaryDatasets/LemGendizedForex/forex_universe.parquet
```

---

## 6. Training Suite CLI (`lemtrain` / `python cli.py`)

The `lemgendary-training-suite` repository provides the canonical `lemtrain` Typer CLI (accessible via `python cli.py` or console entrypoint `lemtrain`). It coordinates in-process model training, deterministic evaluations, multi-target model compilation, notebook generation, checkpoint management, system audits, cloud synchronization, and the background sidecar daemon.

### 6.1 Invocation Syntax & Global Help

```bash
# Display global help and command groups
python cli.py --help

# Display suite version
python cli.py version
```

| Command | Description |
| :--- | :--- |
| `train` | Train a neural architecture in-process using presets or custom hyperparameters |
| `eval` | Evaluate a trained model checkpoint under torch.no_grad() |
| `export` | Compile models to FP32 ONNX, FP16 ONNX, PyTorch standalone, WebGPU, or MT5 |
| `notebooks` | Generate reproducible Kaggle and Google Colab training notebooks |
| `checkpoints` | List, inspect metadata, and prune model checkpoints |
| `presets` | Enumerate and inspect canonical training presets (`presets.yaml`) |
| `audit` | Audit host resources, model topologies, and judicial PLCC/SRCC rank correlations |
| `sync` | Synchronize model checkpoints and artifacts to remote targets (GDrive, Kaggle, GitHub) |
| `server` | Control FastAPI sidecar daemon (`start`, `stop`, `status`, `openapi`) |

### 6.2 Model Training (`train`)

Executes in-process model training with automatic hardware discovery, SentinelGuard VRAM protection, and SOTA governance:

```bash
# In-process training run using a canonical preset
python cli.py train mirnet_exposure --preset quick-sota --epochs 50

# Custom hyperparameter overrides
python cli.py train mirnet_exposure --batch-size 32 --lr 0.0005 --epochs 100 --clean
```

### 6.3 Checkpoint Evaluation (`eval`)

Runs deterministic validation under `torch.no_grad()` computing task-specific quality metrics:

```bash
# Deterministic evaluation of a checkpoint
python cli.py eval mirnet_exposure --checkpoint checkpoints/mirnet_exposure/best.pth --batch-size 16
```

### 6.4 Model Compilation & Export (`export`)

Compiles trained PyTorch checkpoints into optimized runtime deployment artifacts:

```bash
# Multi-target export: FP32 ONNX, FP16 ONNX, PyTorch standalone, and WebGPU
python cli.py export mirnet_exposure --format all

# Single-target export
python cli.py export mirnet_exposure --format webgpu
```

### 6.5 Notebook Generation (`notebooks`)

Generates reproducible standalone Jupyter notebooks for Kaggle and Google Colab environments:

```bash
# Generate Kaggle and Google Colab notebooks for a model
python cli.py notebooks mirnet_exposure --platform all --output-dir notebooks/
```

### 6.6 Checkpoint Management (`checkpoints`)

Manages checkpoint storage, inspections, and disk pruning:

```bash
# List discovered checkpoints with size and epoch metadata
python cli.py checkpoints list mirnet_exposure

# Inspect specific checkpoint tensor state dict
python cli.py checkpoints inspect checkpoints/mirnet_exposure/best.pth

# Prune older checkpoints keeping the top N
python cli.py checkpoints prune mirnet_exposure --keep 3
```

### 6.7 Canonical Presets (`presets`)

Inspects canonical training profiles defined in `presets.yaml`:

```bash
# List all canonical profiles defined in presets.yaml
python cli.py presets list

# Inspect specific preset parameters
python cli.py presets show quick-sota
```

### 6.8 Hardware & Architecture Audit (`audit`)

Audits system resources, model topologies, and judicial rank correlations:

```bash
# Host hardware and VRAM headroom audit
python cli.py audit system

# Model parameter, layer topology, and memory audit
python cli.py audit model mirnet_exposure

# Judicial rank correlation audit (PLCC and SRCC)
python cli.py audit judicial --model export/mirnet_exposure_fp32.onnx --dataset test_data/
```

### 6.9 Cloud Synchronization (`sync`)

Transfers checkpoints and artifacts between local storage and remote cloud providers:

```bash
# Sync checkpoint artifacts to Google Drive
python cli.py sync run mirnet_exposure --target gdrive --epoch 10

# Probe remote cloud storage connection
python cli.py sync probe --target kaggle
```

### 6.10 Sidecar Daemon Operations (`server`)

Controls the background FastAPI sidecar service running on `127.0.0.1:8200`:

```bash
# Launch background sidecar daemon on port 8200
python cli.py server start --daemon

# Check daemon health, port, and PID
python cli.py server status

# Export OpenAPI 3.1 specification schema
python cli.py server openapi --output openapi.json

# Terminate running daemon process
python cli.py server stop
```

---

## 7. Models Hub & Verification Toolchain

The `LemGendaryModels` repository hosts trained neural checkpoints and model cards.

Validation and inspection:

```bash
# Model validation is executed centrally via Environment Manager:
lem-env validate --project LemGendaryModels

# Check model checkpoint integrity directly
python -c "import torch; print(torch.load('NAFNet/checkpoints/nafnet_weights.pth', map_location='cpu').keys())"
```

---

## 8. Documentation Hub & Static Validation

The `lemgendary-docs` repository contains technical research whitepapers, HTML documentation, and operational manuals.

Operations:

```bash
# Documentation validation is executed centrally via Environment Manager:
lem-env validate --project lemgendary-docs

# Serve documentation hub locally using Python HTTP server
python -m http.server 8080 --directory lemgendary-docs
```

---

## 9. Exit Codes, Automation & CI/CD Integration

All ecosystem CLI tools follow standard POSIX and Windows process exit code conventions:

| Exit Code | Meaning | Operator Action |
| :--- | :--- | :--- |
| `0` | Success | Operation completed successfully with zero violations or errors |
| `1` | General Failure | Unhandled exception or syntax failure during execution |
| `2` | Validation Error | One or more quality, linting, or domain gates failed verification |
| `3` | Missing Prerequisites | Required toolchain component (Python, Git, NPM) is not installed |
| `4` | Network / IO Error | Failed to reach remote registry or download necessary assets |

Continuous Integration Workflow Example:

```bash
# Standard CI/CD verification pipeline
lem-env audit --fast || exit 1
lem-env validate || exit 2
```

---

## Companion Documentation

- [Technical Whitepaper (Markdown)](PAPER_ENV_MANAGER.md)
- [Technical Whitepaper (HTML)](env_manager.html)
- [Master REST & WebSocket API Specification (Markdown)](MANUAL_API.md)
- [Master REST & WebSocket API Specification (HTML)](api-manual.html)
