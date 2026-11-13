# LemGendary Ecosystem: Master CLI Operations Manual

## Category 00 | LemGendary AI Documentation Hub

**Version**: `v16.9.214-STABLE`

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
- [4. LemGendary AI Studio GUI CLI & Toolchain](#4-lemgendary-ai-studio-gui-cli--toolchain)
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
  - [5.13 Direct Streaming Zip-to-Container Engine (`stream_zip_to_container.py`)](#513-direct-streaming-zip-to-container-engine-stream_zip_to_containerpy)
  - [5.14 Retroactive Container Migration (`format migrate` / `format write`)](#514-retroactive-container-migration-format-migrate--format-write)
  - [5.15 Upstream Dataset Expansion & Multi-Format Ingestion Reference](#515-upstream-dataset-expansion--multi-format-ingestion-reference)
  - [5.16 LLM Dataset Compilation & Quality Invariant Auditing (`llm`)](#516-llm-dataset-compilation--quality-invariant-auditing-llm)
  - [5.17 Manifold Repair (`repair`)](#517-manifold-repair-repair)
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
  - [6.11 LLM Causal Instruction Tuning & Model Export (`llm`)](#611-llm-causal-instruction-tuning--model-export-llm)
  - [6.12 FID Re-evaluation (`python -m training.fid_reeval`)](#612-fid-re-evaluation-python--m-trainingfid_reeval)
  - [6.13 Kaggle Cloud Training How-To (`lemtrain kaggle`)](#613-kaggle-cloud-training-how-to-lemtrain-kaggle)
- [7. Models Hub & Verification Toolchain](#7-models-hub--verification-toolchain)
- [8. Documentation Hub & Static Validation](#8-documentation-hub--static-validation)
- [9. Exit Codes, Automation & CI/CD Integration](#9-exit-codes-automation--cicd-integration)
- [Companion Documentation](#companion-documentation)

---

## 1. Executive Overview

The LemGendary Ecosystem comprises seven specialized repositories orchestrated
under a unified architectural contract.
All command-line operations are standardized, deterministic, and free of
external visual noise or emojis.
The single authoritative command-line tool for ecosystem health, virtual
environment lifecycles, and verification is `lem-env`,
located in `lemgendary-env-manager`.

Every toolchain command adheres strictly to semantic exit codes, making them
directly suited for automated continuous integration,
local terminal workflows, and cross-project orchestration.

---

## 2. Environment Manager CLI (`lem-env`)

`lem-env` is packaged as a standard Python console application using Typer and
Rich. It provides the central management interface
for inspecting hardware capabilities, provisioning isolated virtual
environments, upgrading packages in dependency order,
and enforcing strict linting and compilation gates across all seven workspaces.

### 2.1 Global Options & Invocation

```bash
# General invocation syntax
lem-env [COMMAND] [OPTIONS]

# Help and discovery
lem-env --help
```

- **`--help`**: Type: Flag; Description: Display comprehensive command usage,
  available subcommands, and flags

---

### 2.2 Hardware Probing (`probe`)

The `probe` command discovers system hardware, compute accelerators, operating
system architecture, MetaTrader 5 availability,
and checks for software update releases against upstream registries.

```bash
lem-env probe
```

Key features:

- Detects GPU acceleration backends including NVIDIA CUDA, AMD ROCm, Windows
  DirectML, and CPU fallback.
- Detects MetaTrader 5 terminal installations, install directories, and software
  versions.
- Queries `winget list` (installed version) and `winget show` (available
  version) to report both current and latest software versions with a status of
  `UP TO DATE`, `UPDATE AVAILABLE`, `NOT INSTALLED`, or
  `INSTALLED (not in winget)`.

MetaTrader 5 detection priority:

1. Windows registry keys under `HKCU`/`HKLM\SOFTWARE\MetaQuotes\Terminal` (fast,
   ~5 ms)
2. Well-known install paths (`%ProgramFiles%\MetaTrader 5\terminal64.exe`,
   the MetaTrader 5 installation folder under Program Files)
3. PowerShell `Get-Package -Name '*MetaTrader*'` (slow fallback)

When an install path is available, the version is read directly from
`terminal64.exe`'s `FileVersion` metadata via PowerShell's `VersionInfo`
property. This gives an authoritative version number even when winget has no
record of the installation (typical for MT5, which is often installed outside
winget's package database).

---

### 2.3 Ecosystem Health Audit (`audit`)

The `audit` command executes an exhaustive diagnostic audit of all seven
repositories in the ecosystem.

```bash
# Full audit with per-project safety classification (~30-90s)
lem-env audit

# Fast audit — skips pip dry-runs
lem-env audit --fast
```

- **`--fast`**: Flag: None; Type: Bool; Default: `False`; Description: Skip
  per-project pip safety dry-runs. Audit completes in seconds but the Safe-↑
  column in the drift matrix is left empty.

Diagnostic checks performed:

- Toolchain prerequisites verification for Python, Git, NPM, and MetaTrader 5.
- Virtual environment presence, Python executable health, and missing package
  count for each repository.
- Node.js workspace health, inspecting `package.json`, `node_modules`, and
  declared dependencies.
- Manifest Coverage: declared vs installed vs missing vs extra vs
  platform-skipped counts per project.
- Python Package Drift & Upgrade Status matrix. Every package declared in two or
  more manifests appears with:
  - **Pin type glyph**: `=` (exact `==`), `~` (range), `*` (floating), `·`
    (transitive install), empty (declared but not installed)
  - **Upgrade marker**: `↑` (safe update available), `⊘` (blocked by reverse
    dependency), none (at latest version)
- Packages Declared in Only One Manifest: full inventory of drift-invisible packages.
- NPM Package Dependency Matrix inspecting declared versus installed package versions.
- NPM Package Drift Across Workspaces.

Blocked upgrades include a reason string naming the requiring package and
constraint, e.g. `pylint requires astroid<=4.1.dev0,>=4.0.2`.

---

### 2.4 Smart Clean Install Pipeline (`install`)

The `install` command runs the automated seven-step environment creation and
package installation pipeline.

```bash
# Execute clean install across all ecosystem projects
lem-env install

# Target a specific repository
lem-env install --project lemgendary-training-suite

# Install without purging existing virtual environments
lem-env install --no-clean
```

- **`--project`**: Flag: `-p`; Type: Text; Default: `None`; Description:
  Restrict installation to a single target repository
- **`--clean / --no-clean`**: Flag: None; Type: Bool; Default: `True`;
  Description: Completely purge existing `.venv` and `node_modules` before fresh
  recreation. The venv currently executing the pipeline is preserved
  automatically.

The pipeline executes in sequential order:

1. Hardware discovery and backend acceleration detection.
2. Global toolchain verification (Python, Git, NPM).
3. Virtual environment provisioning and purge (skips the running venv).
4. Python package installation using locked manifests, followed by OpenCV
   variant normalization.
5. Node.js package installation via NPM.
6. Post-install validation (py_compile, lint, YAML, JSON, HTML/WCAG, domain gates).
7. Final ecosystem health audit generation.

---

### 2.5 Safe Bottom-Up Package Upgrades (`update`)

The `update` command safely resolves outdated dependencies and upgrades them
bottom-up across the dependency hierarchy:
`lemgendary-env-manager` -> `lemgendary-datasets` -> `lemgendary-training-suite`
-> `lemgendary-ai-studio-gui`.

```bash
# Inspect potential upgrades without modifying files
lem-env update --dry-run

# Apply upgrades and auto-sync requirement manifests
lem-env update
```

- **`--project`**: Flag: `-p`; Type: Text; Default: `None`; Description: Target
  package upgrades for a specific repository
- **`--dry-run`**: Flag: None; Type: Bool; Default: `False`; Description:
  Display proposed version changes without executing installations

Every candidate upgrade passes through a multi-layer safety pipeline before
being applied:

1. **Reverse-dependency check**: `pip inspect --local` is used to build a
   reverse-dependency graph of every installed package. Any candidate whose
   target version would violate an installed package's requirement is marked
   `BLOCKED` with an explanation.
2. **Constraint-preserving dry-run**: Every non-target installed package is
   written into a temporary pip constraints file. If pip cannot resolve the
   target batch without downgrading or removing anything, the batch is split
   into per-package checks so a single bad candidate does not poison the whole
   set.
3. **CUDA-aware torch handling**: On CUDA hosts, `torch`, `torchvision`, and
   `torchaudio` are resolved against the PyTorch CUDA index the probe picks
   from the driver version (for example `download.pytorch.org/whl/cu126`).
   Only packages already installed in the
   project are considered; packages already at the newest CUDA build produce a
   `VERIFIED` event instead of a spurious `UPGRADED` event.
4. **Snapshot + rollback**: Each batch is snapshotted via `pip freeze`, applied,
   and verified with `pip check`. If the check fails, the batch is rolled back
   from the snapshot.

After all pip/npm upgrades complete, centralized manifests in
`lemgendary-env-manager/requirements/` are automatically re-written to reflect
actual installed versions. Packages in `PROTECTED_FROM_SYNC` (`astroid`,
`pylint`, `pydantic`, `pydantic-core`) are passed through untouched to prevent a
transient upgrade-time drift from being permanently encoded into the manifest.

---

### 2.6 Manifest Synchronization (`sync`)

The `sync` command captures currently installed packages from active virtual
environments and synchronizes pinned requirement manifests
under `lemgendary-env-manager/requirements/`.

```bash
lem-env sync
```

Manifests maintained:

- `requirements-env-manager.txt`
- `requirements-datasets.txt`
- `requirements-training.txt`
- `lemgendary-ai-studio-gui.package.json`

This is called automatically by `install` and `update` — use directly only when
you need to reset a project's requirements without running the full pipeline.

---

### 2.7 Multi-Gate Validation Engine (`validate`)

The `validate` command enforces strict quality, formatting, compilation, and
domain integrity gates across all seven workspaces.

```bash
# Validate entire ecosystem
lem-env validate

# Validate specific project
lem-env validate --project lemgendary-docs
```

Validation gates enforced (in run order, from
`env_manager/validation/registry.py`):

- **Python bytecode**: Tool: `py_compile`; Projects: Python projects
- **Zero-emoji**: Tool: Regex scan; Projects: All projects
- **YAML lint**: Tool: `yamllint` (env-manager .venv); Projects: All 7 repos
- **JSON RFC 8259**: Tool: Python `json` (in-process); Projects: All 7 repos
- **Markdown lint**: Tool: `markdownlint-cli2`; Projects: All 7 repos
- **JS/TS linting**: Tool: ESLint (`--format json`); Projects: Node projects
  (`lemgendary-ai-studio-gui`)
- **TypeScript types**: Tool: `tsc --noEmit`; Projects: Node projects
- **W3C HTML**: Tool: `html-validate`; Projects: static HTML sites
  (`lemgendary-docs`)
- **WCAG 2.2 AA**: Tool: `pa11y`; Projects: static HTML sites
  (`lemgendary-docs`)
- **PowerShell analysis**: Tool: `PSScriptAnalyzer` (`pwsh` preferred);
  Projects: Repositories with `.ps1`
- **Pylint**: Tool: `pylint` from the project's `.venv` with the project's own
  config; Projects: Python projects
- **Forbidden suppressions**: Tool: in-process scan (Python directives and
  `warnings` ignore filters, TS/JS `@ts-*` and `eslint-disable` comments, Rust
  `allow` attributes); Projects: All projects
- **Absolute paths**: Tool: in-process scan for hardcoded absolute paths;
  Projects: All projects
- **Domain Verifications**: Tool: domain gates (README changelog, docs sync,
  docs manifests, docs suite, dataset manifests, training suite, models hub,
  git hooks); Projects: the matching repositories
- **Ecosystem SSOT**: Tool: `ecosystem_ssot` (error severity): literal ports,
  Kaggle owner, docs URL or project lists that do not come from
  `lemgendary-env-manager/ecosystem/ecosystem.json`; Projects: All projects

Gates fail closed: a missing or crashing tool is a `tool_error` finding, and the
npx fallback (`npx --no`) never downloads packages. Every gate runs its tool
with the project directory as working directory (since LemGendary Environment
Manager v16.9.80), so `validate` gives the same result from the workspace root
as from inside a project.

All Node.js validation tools are resolved locally from
`lemgendary-env-manager/node_modules/.bin` via `_resolve_tool_cmd()`,
eliminating global toolchain pollution.

> **Note on WCAG for the React app (`lemgendary-ai-studio-gui`)**: The
> Vite/React build produces a minimal `index.html` shell with a single
> `<div id="root">`. WCAG accessibility validation of the fully rendered UI
> requires a running dev server. The `validate` command runs ESLint and
> TypeScript checks for the GUI instead; WCAG should be run manually via
> `npx pa11y http://localhost:5173` against a live dev server.

---

### 2.8 Workspace Cache & Residue Purge (`clean`)

The `clean` command removes volatile temporary files, caches, and build
artifacts to maintain absolute workspace hygiene.

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

The `serve` command launches the FastAPI REST API and WebSocket real-time
telemetry server.

```bash
# Start server on default address
lem-env serve

# Start on custom interface and port
lem-env serve --host 0.0.0.0 --port 8000
```

- **`--host`**: Flag: `-h`; Type: Text; Default: `127.0.0.1`; Description:
  Network interface address to bind the HTTP listener
- **`--port`**: Flag: `-p`; Type: Int; Default: `8000`; Description: TCP port
  for incoming REST and WebSocket connections

Server lifecycle is managed via FastAPI's `@asynccontextmanager` lifespan
handler, ensuring the background event-drain task is cancelled cleanly on
shutdown.

---

### 2.10 Git Hook Installation (`setup-hooks`)

The `setup-hooks` command (with canonical alias `hooks`) installs or repairs
standardized pre-commit hooks across all ecosystem projects.

```bash
# Install hooks across all projects
lem-env setup-hooks
# Or using the concise alias:
lem-env hooks

# Install for a single project
lem-env setup-hooks --project lemgendary-datasets
```

The installed hook delegates validation to `lem-env validate --project <name>`
and blocks the commit if any gate fails. This ensures every repository runs the
same validation pipeline regardless of local toolchain state.

---

## 3. Interactive PowerShell Host (`lemgendary_env_manager.ps1`)

For Windows terminal operators, `lemgendary_env_manager.ps1` provides an
interactive, keyboard-driven management console.

Execution syntax:

```powershell
powershell -ExecutionPolicy Bypass -File .\lemgendary_env_manager.ps1
```

Interactive Menu Matrix:

- `[1] Probe System & Hardware Accelerators`: Executes hardware discovery and
  checks for updates.
- `[2] Run Full Ecosystem Health Audit`: Displays toolchain, virtual
  environment, manifest coverage, drift matrix, single-manifest inventory, and
  NPM dependency matrix.
- `[3] Execute Smart Clean Install Pipeline`: Purges environments and installs
  clean dependencies.
- `[4] Run Safe Package Updates`: Executes bottom-up dependency upgrades and
  syncs manifests.
- `[5] Validate Projects`: Enforces py_compile, ESLint, YAML, JSON, W3C, WCAG
  2.2 AA, and domain gates.
- `[6] Start/Stop Background API Server`: Launches or stops the FastAPI server
  as a background PowerShell job with live WebSocket streaming.
- `[Q] Quit`: Gracefully terminates the management console.

---

## 4. LemGendary AI Studio GUI CLI & Toolchain

The desktop application `lemgendary-ai-studio-gui` utilizes Node.js, React 18,
Vite, and Tauri v2.

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

The `lemgendary-datasets` repository provides the unified `lemgendary` CLI
(`cli.py`), exposing a full suite of compiler, synthesis, audit, transcoding,
and server operations. All commands feature transparent hybrid routing: when the
sidecar API daemon is active on `127.0.0.1:8100`, commands submit tasks to the
API and render live WebSocket logs to Rich Console; when stopped or when
`--no-server` is passed, commands fall back cleanly to direct in-process
execution.

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

Compiles raw image and market data into production-ready dataset manifolds with
optional multi-container emission and quality gates:

```bash
# Standard compilation with default WebP q=92
python cli.py compile --model nima_aesthetic --max-gb 50

# Compile using canonical compiler preset (Phase 8)
python cli.py compile --model nima_aesthetic --preset quality-vision

# Concurrently emit WebP directory and a LitData container
python cli.py compile --model nima_aesthetic --image-format webp \
  --image-quality 92 --also-format litdata

# High-throughput compile bypassing aesthetic vetting and labeling
python cli.py compile --model nafnet_deblurring --workers 16 --no-vetting --no-labeling

# Force container byte duplication across hardlink gates
python cli.py compile --model upn_v2 --also-format litdata --force-duplicate

# Force in-process compilation bypassing active API server
python cli.py compile --model nima_technical --no-server
```

- **`--model`, `-m`**: Type: String; Default: `None`; Description: Dataset
  registry key in `unified_data.yaml`
- **`--preset`, `-p`**: Type: String; Default: `None`; Description: Predefined
  compiler preset profile (`quality-vision`, `restoration-hardlinked`,
  `detection-variable`, `cloud-archival`)
- **`--max-gb`**: Type: Float; Default: Config; Description: Maximum size
  allocation threshold in gigabytes
- **`--workers`**: Type: Integer; Default: Auto; Description: Number of parallel
  worker threads/processes
- **`--image-format`**: Type: String; Default: `webp`; Description: Target
  format: `webp`, `jpeg`, `png`, `keep`
- **`--image-quality`**: Type: Integer; Default: `92`; Description: Target image
  compression quality (1-100)
- **`--target-quality`**: Type: Integer; Default: `95`; Description: Restoration
  target ground-truth quality
- **`--mask-format`**: Type: String; Default: `webp-lossless`; Description:
  Segmentation mask format
- **`--also-format`**: Type: String; Default: `None`; Description:
  Comma-separated containers: `litdata`, `wds`, `parquet`; `mds` needs the
  optional `mosaicml-streaming` package, which the Environment Manager no
  longer installs (MDS compilation is discontinued since Environment Manager
  v16.9.81)
- **`--no-vetting`**: Type: Flag; Default: `False`; Description: Bypass NIMA
  aesthetic score gate
- **`--no-labeling`**: Type: Flag; Default: `False`; Description: Bypass YOLO
  detection auto-labeling
- **`--no-hash`**: Type: Flag; Default: `False`; Description: Bypass pHash/dHash
  perceptual deduplication
- **`--no-server`**: Type: Flag; Default: `False`; Description: Force local
  in-process execution

### 5.3 Degradation Engine Synthesis (`degrade`)

Derives paired synthetic restoration manifolds from clean ground-truth sources
using mathematical physical kernels:

```bash
# Motion blur and heteroscedastic sensor noise synthesis
python cli.py degrade --source raw-sets/div2k \
  --output LemGendizedNafNetDebluringSynthetic --profile motion-blur+iso-noise

# Atmospheric haze synthesis on custom manifold directory
python cli.py degrade --source ../LemGendaryDatasets/LemGendizedNimaAesthetic \
  --output LemGendizedHazySynthetic --profile rainy-haze --intensity high

# Dry-run validation
python cli.py degrade --source raw-sets/div2k --output LemGendizedTest \
  --profile vintage-film --dry-run
```

- **`--source`, `-s`**: Type: String; Default: Required; Description: Source
  dataset folder or registered manifold name
- **`--output`, `-o`**: Type: String; Default: Required; Description:
  Destination synthetic manifold folder name
- **`--profile`, `-p`**: Type: String; Default: `motion-blur+iso-noise`;
  Description: Profile token or composite expression
- **`--intensity`**: Type: String; Default: `medium`; Description: Intensity
  preset: `low`, `medium`, `high`
- **`--pairs`**: Type: Integer; Default: `None`; Description: Maximum sample
  pair count cap
- **`--val-split`**: Type: Float; Default: `0.12`; Description: Validation set
  split ratio
- **`--seed`**: Type: Integer; Default: `42`; Description: Deterministic random
  number seed
- **`--image-format`**: Type: String; Default: `webp`; Description: Target
  output format for degraded images
- **`--dry-run`**: Type: Flag; Default: `False`; Description: Simulate
  derivation plan without writing files

### 5.4 Audit, Deduplication & Hardlinks (`audit`)

Performs image integrity auditing, magic byte sniffing, aspect ratio filtering,
perceptual hashing, and NTFS hardlink fraction accounting:

```bash
# Audit registered manifold
python cli.py audit --model nima_aesthetic

# Audit arbitrary filesystem directory with sample cap
python cli.py audit --manifold ../LemGendaryDatasets/LemGendizedUpnV2 --sample 1000
```

### 5.5 Retroactive Transcoding (`transcode`)

In-place atomic transcoding of existing manifold image sets to WebP with zero
intermediate files:

```bash
python cli.py transcode --model nima_technical --image-format webp \
  --image-quality 92
```

### 5.6 Smart Multi-Modal Generation (`label`, `prompt`, `mask`)

Runs GPU/CPU inference backends over compiled manifolds to generate labels,
diffusion prompts, or segmentation masks:

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
# Modernization queue inspection and management
python cli.py modernize queue

# Run batch modernization and WebP transcoding
python cli.py modernize run --workers 8 --push-kaggle

# Scale reduction (spatial downsampling) for a specific manifold
python cli.py modernize reduce --manifold LemGendizedClassificationMaster \
  --scale-factor 0.25

# Batch regenerate manifolds index and dataset-metadata.json files
python cli.py modernize regen

# Create downsampled reduced manifold variant (legacy CLI syntax)
python cli.py reduce --max-gb 10

# Retire legacy `Large` suffix locally and in registry
python cli.py modernize --dry-run
python cli.py modernize --all --yes
python cli.py modernize --datasets nima_technical,nima_aesthetic --skip-kaggle

# Full modernization: suffix retirement, WebP transcoding, and modern container conversion
python cli.py modernize --datasets nima_aesthetic --image-format webp \
  --also-format webdataset
```

- **`--all`**: Type: Flag; Default: `False`; Description: Select all eligible
  manifolds for modernization
- **`--yes`, `-y`**: Type: Flag; Default: `False`; Description: Skip interactive
  confirmation gate
- **`--dry-run`**: Type: Flag; Default: `False`; Description: Simulate
  modernization plan without file modification
- **`--datasets`**: Type: String; Default: `None`; Description: Comma-separated
  list of folder names, base names, or keys
- **`--skip-kaggle`**: Type: Flag; Default: `False`; Description: Skip Kaggle
  re-upload (local creation and metadata preserved)
- **`--image-format`**: Type: String; Default: `webp`; Description: Target
  format for image transcoding (`webp`, `jpeg`, `png`, `keep`)
- **`--image-quality`**: Type: Integer; Default: `92`; Description: Compression
  quality for image transcoding (1-100)
- **`--target-quality`**: Type: Integer; Default: `95`; Description: Quality
  floor for ground-truth restoration target transcoding
- **`--mask-format`**: Type: String; Default: `webp-lossless`; Description:
  Format for mask transcoding (`webp-lossless`, `png`)
- **`--also-format`**: Type: String; Default: `webdataset`; Description: Target
  container format (`webdataset`, `mds`, `litdata`, `parquet`)
- **`--skip-transcode`**: Type: Flag; Default: `False`; Description: Skip WebP
  image transcoding phase
- **`--skip-container`**: Type: Flag; Default: `False`; Description: Skip
  container format conversion phase

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
# Run dataset compiler unit tests
python cli.py test
python cli.py test --pattern test_llm*.py

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
# Say what changed in the new version (added to the generated version notes)
python cli.py sync push --model retinaface_mobilenet --notes "Rebuilt labels"
python cli.py sync pull --url lemgenda/lemgendizednimaaesthetic

# Fetch only some folders or files (repeatable --only), into another folder
python cli.py sync pull --url lemtreursi/lemgendizedretinafacemobilenetlarge \
  --only labels/ --only classes.txt --output RetinaFaceLabels

# Update Kaggle metadata across all manifolds or a single manifold
python cli.py sync metadata --all
python cli.py sync metadata --model nima_aesthetic

# Documentation regeneration
python cli.py docs regen

# Schema validation
python cli.py config validate
```

`sync pull` creates the datasets root (`LemGendaryDatasets/`) when it is
missing and measures free space at the nearest existing parent folder. When
Kaggle has no whole-dataset archive (HTTP 404 "No gcs url found") the pull
falls back to a file-by-file download: every page of the file listing is
read, each file is fetched through its signed URL, checked against the listed
size and skipped on a re-run, and an interrupted `.part` resumes with an HTTP
range. After the first per-file 404 the Kaggle API's `dataset_download_file`
serves every remaining file. HTTP 429 waits and retries on both routes
(Retry-After, else 30 s doubling up to 600 s). `--only` fetches a folder
(ending in `/`) or file relative to the dataset's top folder, from the zip
through HTTP byte ranges or file by file. A pulled registered manifold packs
its text labels into JSON with the entry's label strategy. A new Kaggle
dataset is created private; the metadata push applies the registry
`is_private` and license.

`sync push` labels every new Kaggle dataset version with generated version
notes: the compiler release and the sample counts the manifold's `index.json`
(else `dataset_info.yaml`) records. Since v16.9.109, `--notes TEXT` adds what
changed in this version after them, separated by `". "`; whitespace is
collapsed and blank text adds nothing. Without `--notes` the notes are the
generated part only.

### 5.11 Canonical Compiler Presets (`presets`)

Inspects canonical compilation profiles defined in `presets.yaml`:

```bash
# Display formatted table of available compiler presets
python cli.py presets list
```

The output provides a matrix of target formats, image quality percentages,
aesthetic vetting gates, and auto-labeling toggles for each profile.

### 5.12 Forex Universe & Parquet Operations (`forex`)

Converts historical multi-symbol tick and M1/M15/H1/H4/D1 time-series arrays
from legacy `.npy` containers into compressed, partitioned PyArrow Parquet
manifolds with embedded schema metadata:

```bash
# Convert NPY market array files into Parquet
python cli.py forex convert --source ../raw-market-data/forex_manifold.npy \
  --output ../LemGendaryDatasets/LemGendizedForex

# Embed column descriptions and metadata into Parquet tables
python cli.py forex embed --target ../LemGendaryDatasets/LemGendizedForex/forex_universe.parquet
```

### 5.13 Direct Streaming Zip-to-Container Engine (`stream_zip_to_container.py`)

Directly streams multi-gigabyte legacy dataset zip archives into canonical POSIX
WebDataset `.tar` shards with on-the-fly 12-thread WebP transcoding, eliminating
NTFS MFT file allocation overhead and real-time antivirus filter driver
slowdowns:

```bash
# Stream paired restoration dataset directly to WebDataset shards with WebP transcoding
python tools/stream_zip_to_container.py \
    --zip ../LemGendaryDatasets/lemgendizedmirnetexposure.zip \
    --target ../LemGendaryDatasets/LemGendizedMirNetExposure \
    --shard-size 5000 \
    --delete-zip

# Stream split target dataset (UpnV2) with automatic metadata and index.json extraction
python tools/stream_zip_to_container.py \
    --zip ../LemGendaryDatasets/lemgendizedupnv2.zip \
    --target ../LemGendaryDatasets/LemGendizedUpnV2 \
    --shard-size 5000 \
    --delete-zip
```

- **`--zip`**: Type: Path; Default: Required; Description: Path to the source
  multi-gigabyte `.zip` archive
- **`--target`**: Type: Path; Default: Required; Description: Destination
  modernized manifold directory
- **`--format`**: Type: Choice; Default: `webdataset`; Description: Target
  container format (`webdataset`)
- **`--shard-size`**: Type: Integer; Default: `5000`; Description: Number of
  samples per tar shard (~500 MB)
- **`--no-webp`**: Type: Flag; Default: `False`; Description: Disable WebP
  transcoding (preserves original bytes)
- **`--workers`**: Type: Integer; Default: `None` (auto: 12); Description:
  Number of worker threads for parallel transcoding
- **`--delete-zip`**: Type: Flag; Default: `False`; Description: Unlink source
  `.zip` archive upon verified completion
- **`--delete-legacy-dir`**: Type: Path; Default: `None`; Description: Path to
  legacy uncompressed folder to purge

### 5.14 Retroactive Container Migration (`format migrate` / `format write`)

Converts already modernized datasets with loose WebP images and `index.json`
into streaming container shards, with optional purging of loose files to
eliminate cluster slack:

```bash
# Convert existing directory to WebDataset shards and purge loose directory layout
python cli.py format migrate \
    --manifold ../LemGendaryDatasets/LemGendizedFilmRestorer \
    --to webdataset \
    --accept-space-loss \
    --purge-source

# Equivalent direct script invocation:
python tools/migrate_manifold_format.py \
    --manifold ../LemGendaryDatasets/LemGendizedFilmRestorer \
    --to webdataset \
    --accept-space-loss \
    --purge-source
```

### 5.15 Upstream Dataset Expansion & Multi-Format Ingestion Reference

The dataset compiler allows expanding any manifold simply by appending new
source references to `unified_data.yaml` under the target dataset's `refs:`
array:

```yaml
datasets:
  nima_aesthetic:
    name: NimaAesthetic
    canonical_format: webdataset
    val_split: 0.12
    refs:
      - ref: kaggle://nicolacarrassi/ava-aesthetic-visual-assessment
      - ref: hf://chaofengc/IQA-PyTorch-Datasets:spaq.tgz
      - ref: gd://1A2B3C4D5E6F7G8H9I0J
      - ref: gh://owner/research-dataset
      - ref: manifold://NafNetDebluring
```

#### Supported Upstream Source Protocols

- **`kaggle://<owner>/<slug>`**: Handler Submodule: `sources/kaggle.py`;
  Description: Authenticated KaggleHub and Kaggle API dataset download with
  auto-unpack
- **`hf://<org>/<repo>[:<file>]`**: Handler Submodule: `sources/hf.py`;
  Description: Hugging Face Hub snapshot or archive (`.tgz`, `.tar.gz`) download
- **`gd://<id>`**: Handler Submodule: `sources/gd.py`; Description: Google Drive
  multi-threaded chunked download
- **`gh://<owner>/<repo>`**: Handler Submodule: `sources/gh.py`; Description:
  GitHub repository archive or release asset synchronization
- **`manifold://<Name>`**: Handler Submodule: `core/manifold_compile.py`;
  Description: Zero-copy sibling manifold recirculation without duplicating
  files

#### Supported Input Annotation & Image Formats

- **MATLAB (`.mat`)**: Converter Submodule: `converters/matlab.py`; Parsing
  Engine & Capabilities: `scipy.io.loadmat(mat_path, spmatrix=False)` extracting
  structs, keys, and coordinate arrays
- **COCO JSON (`.json`)**: Converter Submodule: `converters/coco.py`; Parsing
  Engine & Capabilities: MS-COCO bounding boxes, categories, and polygon masks
- **Pascal VOC (`.xml`)**: Converter Submodule: `converters/xml.py`; Parsing
  Engine & Capabilities: XML node traversal extracting class names and bounding
  coordinates
- **YOLO TXT (`.txt`)**: Converter Submodule: `converters/yolo.py`; Parsing
  Engine & Capabilities: Space-delimited bounding boxes (`class xc yc w h`)
- **Apache Parquet (`.parquet`)**: Converter Submodule: `converters/parquet.py`;
  Parsing Engine & Capabilities: Columnar table schemas with embedded image
  bytes or URLs
- **Images**: Converter Submodule: `_fast_scan`; Parsing Engine & Capabilities:
  `.jpg`, `.jpeg`, `.png`, `.webp`, `.safetensors`, `.tiff`, `.tif`, `.bmp`,
  `.npy`

#### Compilation Trigger

Once sources are added, run compilation to automatically download missing sets,
prune corrupt files, vet quality, resize via Lanczos-3, and transcode directly
into modern WebP containers:

```bash
# Ingest all configured sources, vet, and emit canonical modern container shards
python cli.py compile --model nima_aesthetic --also-format webdataset --workers 12
```

---

### 5.16 LLM Dataset Compilation & Quality Invariant Auditing (`llm`)

The LLM compiler module (`tools.llm_helper`) provides high-velocity generic
compilation and validation for instruction tuning datasets:

```bash
# Compile an LLM instruction manifold declared in unified_data.yaml (in-process)
python cli.py llm compile --dataset test_llm --no-server

# Compile via local FastAPI sidecar daemon with live WebSocket log streaming
python cli.py llm compile --dataset test_llm

# Audit any JSONL dataset file against the 4 LemGendary Quality Invariants
python cli.py llm validate --file ../LemGendaryDatasets/LemGendizedTestLLM/data/test_llm_train.jsonl
```

#### Quality Invariant Checks Enforced

1. **Zero-Emoji Rule**: Verifies total absence of Unicode emojis across all
   system, user, and assistant turns.
2. **ChatML 3-Turn Schema**: Enforces strict `[system, user, assistant]` message
   structure with non-empty strings.
3. **Epistemic Certainty Tags**: Enforces presence of `[CONFIRMED]`,
   `[PROBABLE]`, or `[ILLUSTRATIVE]` tags in diagnostic and troubleshooting
   outputs.
4. **Duplicate Detection**: Identifies exact and fuzzy duplicate prompt
   collisions across the manifold.

### 5.17 Manifold Repair (`repair`)

Repairs a compiled manifold in place without a recompile. Every subcommand is a
dry run that prints its plan unless `--apply` is given, takes `--model KEY`
(registry key) or `--manifold PATH`, rewrites each changed shard to a
temporary file, verifies it and swaps it in atomically (no backup copies are
kept), and keeps `index.json` and the `dataset_info.yaml` `count` in step. A
re-run finds nothing to do. Every subcommand that rewrites shards also
refreshes the `shard_offsets.json` index of each shard folder it touched
(dataset compiler v16.9.108).

```bash
# Zero-byte samples, scattered groups, png/jpg members, counts, paths
python cli.py repair manifold --model retinaface_mobilenet
python cli.py repair all

# Labels from a loose labels/<split>/<key>.txt folder into the JSON labels
python cli.py repair labels --model retinaface_mobilenet \
  --labels ../LemGendaryDatasets/_labels/RetinaFace/labels --apply

# Legacy .txt label members merged into <key>.json, then removed
python cli.py repair txt-labels --model yolov8n --apply

# Loose images/ + labels/ folders packed into JSON-labelled WebDataset shards
python cli.py repair pack-loose --model yolov8n --apply

# Registry sample policy: drop copies, auxiliary images and no-face samples,
# re-split val by source file id
python cli.py repair sample-policy --model retinaface_mobilenet --apply

# ParseNet class masks from the SFHQ segmentations/ folders
python cli.py repair masks --model parsenet --masks-root ../sfhq --apply

# RetinaFace boxes and 5 points rebuilt from the SFHQ 110-point landmarks
python cli.py repair face-landmarks --model retinaface_mobilenet \
  --landmarks-root ../sfhq --apply

# ClassificationMaster: pseudo-label table first, then the class labels
python cli.py repair pseudo-labels --model classification_master_manifold \
  --table-root ../LemGendaryDatasets/_labels/LemGendizedClassificationMaster
python cli.py repair class-labels --model classification_master_manifold \
  --table-root ../LemGendaryDatasets/_labels/LemGendizedClassificationMaster \
  --apply

# Shard offset index (shard_offsets.json) of every shard folder; the shards
# are not changed
python cli.py repair shard-offsets --model upn_v2
python cli.py repair shard-offsets --model upn_v2 --apply
```

- **`manifold`**, **`all`**: Description: Zero-byte samples, scattered sample
  groups, leftover PNG/JPEG members (re-encoded to WebP with the compiler's
  encoders), counts and recorded paths. A present `shard_offsets.json` is
  verified, and a stale one is rewritten on `--apply`.
- **`labels`**: Options: `--labels DIR` (required), `--strategy NAME`,
  `--classes FILE`; Description: Writes each sample's label from
  `DIR/<split>/<key>.txt` into its JSON label through the registry
  `label_json` strategy. A label whose boxes differ from the recorded ones is
  a MISMATCH and refuses the apply.
- **`txt-labels`**: Options: `--strategy NAME`; Description: Merges every
  `.txt` label member into the sample's JSON (keys must agree; nothing is
  dropped) and removes the `.txt` members. MISMATCH or UNREADABLE labels
  refuse the apply.
- **`pack-loose`**: Options: `--strategy NAME`; Description: Packs
  `images/<split>` + `labels/<split>` into `shards/<split>/shard-*.data`
  with `<key>.webp` + `<key>.json`. Refuses while an image has no label file,
  a label has no image or shards already exist; removes the loose folders
  only after the packed shards verify.
- **`sample-policy`**: Description: Applies the registry sample policy
  (face detection: drop no-face samples and copies, val drawn from the
  landmark-bearing photos by source file id; face parsing: drop copies and
  segmentation maps, split all photos by source file id).
- **`masks`**: Options: `--masks-root DIR` (required), `--workers N`;
  Description: Stores each photo's source class mask as lossless
  `<key>.mask.webp` (class ids checked after a decode round trip) and records
  `num_classes`, `class_names` and `mask_source` in the JSON label.
- **`face-landmarks`**: Options: `--landmarks-root DIR` (required),
  `--workers N`; Description: Replaces each photo's `objects` with one face:
  a tight WIDER-style box and five points derived from the source landmark
  file, `landmark_source` recorded. A sample that fails the plausibility
  check is dropped; a missing landmark file refuses the apply.
- **`pseudo-labels`**: Options: `--table-root DIR` (required), `--workers N`,
  `--max-shards N`; Description: Runs the registry pseudo-label models (ONNX,
  CPU) over the pseudo-rule samples and writes one JSON Lines table per shard
  outside the manifold; the shards are not touched, and a re-run resumes.
- **`class-labels`**: Options: `--table-root DIR` (required), `--workers N`;
  Description: Writes `class_id`, `class_name`, `label_source` and the
  registry task into each sample's JSON (pseudo labels also
  `label_confidence` and `label_check_class`); a pseudo label that fails its
  rule drops the sample, and a sample without a rule or table row refuses the
  apply.
- **`shard-offsets`**: Options: `--model KEY` or `--manifold PATH`,
  `--apply`; Description: Writes the Shard Offset Index
  `shards/<split>/shard_offsets.json` (format `version` 2) without touching
  the shards. The dry run reports each shard folder's index as missing,
  stale (with the reasons) or current, checking a present index the way the
  Training Suite does: an entry is accepted when the shard size matches and
  either the modification time matches or the tar headers of the first,
  middle and last member agree. `--apply` keeps the entries of unchanged
  shards, rescans the rest, prints the file size and time, and exits 1 when a
  folder is still not current afterwards. Compressed shards get no entry. See
  Section 4.13 of the Dataset Compiler paper.

---

## 6. Training Suite CLI (`lemtrain` / `python cli.py`)

The `lemgendary-training-suite` repository provides the canonical `lemtrain`
Typer CLI (accessible via `python cli.py` or console entrypoint `lemtrain`). It
coordinates in-process model training, deterministic evaluations, multi-target
model compilation, notebook generation, checkpoint management, system audits,
cloud synchronization, and the background sidecar daemon.

### 6.1 Invocation Syntax & Global Help

```bash
# Display global help and command groups
python cli.py --help

# Display suite version
python cli.py version
```

- **`train`**: Description: Train a neural architecture in-process using presets
  or custom hyperparameters
- **`test-all`**: Description: Run a 1-epoch diagnostic smoke test across all 22
  registered neural architectures
- **`eval`**: Description: Evaluate a trained model checkpoint under
  torch.no_grad()
- **`export`**: Description: Compile models to FP32 ONNX, FP16 ONNX, PyTorch
  standalone, WebGPU, or MT5
- **`notebooks`**: Description: Generate reproducible Kaggle and Google Colab
  training notebooks
- **`checkpoints`**: Description: List, inspect metadata, and prune model
  checkpoints
- **`presets`**: Description: Enumerate and inspect canonical training presets
  (`presets.yaml`)
- **`audit`**: Description: Audit host resources, model topologies, and judicial
  PLCC/SRCC rank correlations
- **`sync`**: Description: Synchronize model checkpoints and artifacts to remote
  targets (GDrive, Kaggle, GitHub)
- **`server`**: Description: Control FastAPI sidecar daemon (`start`, `stop`,
  `status`, `openapi`)

### 6.2 Model Training (`train`)

Executes in-process model training with automatic hardware discovery,
SentinelGuard VRAM protection, and SOTA governance:

```bash
# In-process training run using a canonical preset
python cli.py train mirnet_exposure --preset quick-sota --epochs 50

# Custom hyperparameter overrides
python cli.py train mirnet_exposure --batch-size 32 --lr 0.0005 --epochs 100 --clean

# Resume although a frozen run setting changed (logged and recorded)
lemtrain train mirnet_exposure --override-frozen
```

Checkpoints record the run settings (v16.9.187). Frozen settings (model class
and `kwargs`, optimizer type, datasets and task type, quality scheme, Forex
`evaluation.risk_per_trade`, NIMA `stabilizers.emd_form`, subset seed,
precision) must not change on resume: a change raises
`FrozenSettingsChanged`, which names the change, `--clean` and
`--override-frozen`. Epoch settings (locality, batch, LR schedule, weight
decay, gradient clip, loader workers) change at the next epoch boundary: a
resumed run finishes the current epoch on the recorded settings, logs
`[SETTINGS] epoch N: ...` and appends the change to
`LemGendaryModels/<model>/settings_changes.jsonl`.

#### Fleet Diagnostic Smoke Test (`test-all`)

Executes a rapid 1-epoch diagnostic smoke test sequentially across all 22
registered neural architectures using `tools/train_all.py`:

```bash
# Run 1-epoch diagnostic test across all models
lemtrain test-all

# Override test epochs
lemtrain test-all --epochs 2
```

### 6.3 Checkpoint Evaluation (`eval`)

Runs deterministic validation under `torch.no_grad()` computing task-specific
quality metrics:

```bash
# Deterministic evaluation of a checkpoint
python cli.py eval mirnet_exposure \
  --checkpoint checkpoints/mirnet_exposure/best.pth --batch-size 16
```

### 6.4 Model Compilation & Export (`export`)

Compiles trained PyTorch checkpoints into optimized runtime deployment artifacts:

```bash
# Multi-target export: FP32 ONNX, FP16 ONNX, PyTorch standalone, and WebGPU
python cli.py export mirnet_exposure --format all

# Single-target export
python cli.py export mirnet_exposure --format webgpu

# Universal model export and automatic staging into canonical Kaggle variation subdirectories
python -m training.export.universal_exporter --model yolov8n --stage-dist

# Stage existing binaries into dist/kaggle/ without re-exporting
python -m training.export.universal_exporter --model yolov8n --stage-only
```

### 6.5 Notebook Generation (`notebooks`)

Generates reproducible standalone Jupyter training, inference, and usage
notebooks for Kaggle and Google Colab environments from the Training Suite
Single Source of Truth:

```bash
# List all registered architectures available for notebook compilation
lemtrain notebooks list

# Generate Kaggle and Google Colab training & usage notebooks for a specific model
lemtrain notebooks generate --model mirnet_exposure

# Generate only Kaggle training notebooks for a specific model
lemtrain notebooks generate --model forex_predictor --platform kaggle --kind training

# Batch generate and synchronize notebooks across all 22 registered models
lemtrain notebooks generate --all

# Specify custom output export directory
lemtrain notebooks generate --model nima_aesthetic_mobile --output-dir custom_notebooks/
```

- **`--model`, `-m`**: Type: String; Default: `None`; Description: Target neural
  architecture key (e.g., `forex_predictor`, `codeformer`)
- **`--all`, `-a`**: Type: Flag; Default: `False`; Description: Batch generate
  notebooks across all 22 registered model architectures
- **`--platform`, `-p`**: Type: Choice; Default: `all`; Description: Target
  cloud execution platform (`kaggle`, `colab`, `all`)
- **`--kind`, `-k`**: Type: List; Default: `all`; Description: Notebook kinds to
  generate (`training`, `inference`, `usage`)
- **`--output-dir`, `-o`**: Type: Path; Default: `LemGendaryModels`;
  Description: Custom directory to persist generated `.ipynb` files

All generated notebooks are automatically distributed and mirrored across:

1. `LemGendaryModels/<model_key>/` (canonical model folder)
2. `LemGendaryDatasets/<manifold>/` (matching dataset manifold)
3. `kaggle_training/` (workspace-level Kaggle staging directory)
4. `colab_training/` (workspace-level Colab staging directory)

### 6.6 Checkpoint Management (`checkpoints`)

Manages checkpoint storage, inspections, disk pruning, and Pareto Model Soup blending:

```bash
# List discovered checkpoints with size and epoch metadata
python cli.py checkpoints list mirnet_exposure

# Inspect specific checkpoint tensor state dict
python cli.py checkpoints inspect checkpoints/mirnet_exposure/best.pth

# Prune older checkpoints keeping the top N
python cli.py checkpoints prune mirnet_exposure --keep 3

# Blend specialized vault checkpoints using Pareto Model Soup
python cli.py soup codeformer --weights 0.6,0.4 --output checkpoints/codeformer/best_soup.pth
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

Transfers model artifacts, checkpoints, and variations between local storage and
remote cloud providers (Kaggle Models Hub and Google Drive) with strict payload
isolation audits and YAML-driven metadata synchronization. `--variation` takes
a `VariationKey` (`pytorch/default`, `pytorch/fp32`, `onnx/fp16`,
`onnx/fp32`) or `all`; unchanged variations are skipped and every upload
carries version notes (section 6.13):

```bash
# Push single model across all 4 canonical variations (pytorch/default,
# pytorch/fp32, onnx/fp16, onnx/fp32)
lemtrain sync push yolov8n

# Push specific isolated variation to Kaggle Models Hub
lemtrain sync push yolov8n --variation pytorch/default

# Push with custom username override and custom release version notes
lemtrain sync push yolov8n --username lemtreursi \
  --notes "Automated SOTA Release: yolov8n"

# Push all 23 registered models to Kaggle Models Hub with metadata, checkpoints,
# and isolated variations
lemtrain sync push --all

# Perform a dry-run validation of metadata and isolation across all models
# without uploading
lemtrain sync push --all --dry-run

# Pull all 4 isolated variations for a target model from Kaggle Models Hub into
# canonical directories
lemtrain sync pull yolov8n

# Pull specific variation (e.g. pytorch/default checkpoints or onnx/fp16
# deployment binary); files merge into LemGendaryModels/<model>, a checkpoint
# replaces its local copy only when its stored epoch is newer
lemtrain sync pull yolov8n --variation pytorch/default

# Force re-download even if already present locally
lemtrain sync pull yolov8n --force

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

### 6.11 LLM Causal Instruction Tuning & Model Export (`llm`)

Dispatches QLoRA instruction fine-tuning and tri-format export for causal LLM
architectures registered in `unified_models_v2.yaml`:

```bash
# Fine-tune causal LLM on instruction dataset (in-process)
python cli.py llm train ai_helper_lemgend --epochs 3 --batch-size 2 \
  --lr 0.0002 --env local

# Fine-tune generic LLM proof-of-concept manifold
python cli.py llm train test_llm --epochs 1 --batch-size 2 --env local

# Compile and export tri-format deployment binaries
python cli.py llm export ai_helper_lemgend --target qlora_adapter \
  --target merged_safetensors --target gguf_fp16
```

#### Tri-Format LLM Binary Specifications

- **QLoRA Adapter**: Standalone Low-Rank Adaptation weights
  (adapter_model.safetensors, adapter_config.json).
- **Merged Safetensors**: Full floating-point FP16 weights merged into base
  architecture for high-throughput vLLM and HuggingFace inference.
- **GGUF / ONNX Quantized**: Integer-quantized format (q4_k_m.gguf or INT8 ONNX)
  optimized for edge deployment on consumer hardware.

### 6.12 FID Re-evaluation (`python -m training.fid_reeval`)

Re-measures FID (`feature=2048`, chunks of at most two) for the four models whose
historical FID rows were rewritten by a removed tool (`codeformer`,
`ffanet_indoor`, `mprnet_deraining`, `mirnet_lowlight`). Run it from the
`lemgendary-training-suite` root:

```bash
# Record the formula-rewritten metrics.csv rows as unverified (no GPU)
python -m training.fid_reeval mark-unverified --all --dry-run
python -m training.fid_reeval mark-unverified --all

# Check all inputs on CPU, then measure (default: checkpoints/best.pth)
python -m training.fid_reeval measure --model codeformer --dry-run
python -m training.fid_reeval measure --model codeformer --device cuda \
  --batch-size 4 --note "re-evaluation of best.pth"

# Summarise the ledgers
python -m training.fid_reeval status --all
```

- **`measure`**: `--model` (any registry key), `--checkpoint`,
  `--datasets-root`, `--models-root` (default
  `<workspace>/LemGendaryModels`), `--env local|kaggle|colab`,
  `--device auto|cpu|cuda|cuda:N`, `--batch-size` (default 4),
  `--num-workers`, `--non-strict` (allow missing or extra keys; noted in the
  row), `--note`, `--dry-run`.
- **`mark-unverified`** and **`status`**: `--model` (one of the four models) or
  `--all`, `--models-root`; `mark-unverified` also takes `--dry-run`.
- **Output**: rows are appended to
  `LemGendaryModels/<model>/fid_provenance.csv`; `metrics.csv`, checkpoints and
  rung state are never written.
- **Exit codes**: `0` success, `2` bad input or ledger, `3` FID invariant
  failure or missing FID backend.

### 6.13 Kaggle Cloud Training How-To (`lemtrain kaggle`)

A Kaggle training session is a private notebook kernel that the Training Suite
builds from the same generator as the notebook files (`lemtrain kaggle
bundle`), pushes with the Kaggle API (`lemtrain kaggle launch`, the GUI or
`POST /api/training/kaggle/train`) and watches until it ends. Run the commands
from the `lemgendary-training-suite` root.

#### 1. Kaggle API Token

Kaggle API tokens start with `KGAT_`. The suite resolves one credential
(`training/cloud/credentials.py`) in this order: the `.secrets.yaml` vault of
the Environment Manager (default Kaggle record), the environment
(`KAGGLE_API_TOKEN`, then a legacy `KAGGLE_KEY` with `KAGGLE_USERNAME`),
`~/.kaggle/kaggle.json`, then `~/.kaggle/access_token` (or
`access_token.txt`). A `KGAT_` token is exported unchanged as
`KAGGLE_API_TOKEN`, the name kaggle 2.x, kagglesdk and kagglehub read first;
it never goes into `kaggle.json` as a legacy `key` (the CLI answers 401). The
Environment Manager writes a vault token to `~/.kaggle/access_token`. The
legacy `.kaggle_users` and `.kaggle_token` files are no longer read.

```bash
# Check that the resolved credential really works (one authenticated call)
curl -s http://127.0.0.1:8200/api/training/kaggle/status
```

#### 2. Kaggle Secrets of the Kernel

Attach these secrets to the kernel (Kaggle notebook editor, Add-ons,
Secrets) before the first launch. The secrets cell reads them with
`kaggle_secrets.UserSecretsClient` (Colab: `google.colab.userdata`):

- **`KAGGLE_API_TOKEN`**: Required; a `KGAT_` token. Exported for the Hub
  sync and the resume pull; a legacy key is refused. `KAGGLE_KEY` and
  `KAGGLE_USERNAME` secrets are no longer read.
- **`GITHUB_PAT` or `SUITE_PAT`**: Required while the suite or env-manager
  repository is private. The clone gets it only through `GIT_ASKPASS`, never
  in a URL or a file.
- **`GOOGLE_DRIVE`**: Optional; Google Drive mirroring.

Without `KAGGLE_API_TOKEN` the session trains but cannot read or write the
Kaggle Models Hub (`[AUTH] Secrets available: []` in the log).

#### 3. Accelerators

The accelerator table lives in the ecosystem file
(`lemgendary-env-manager/ecosystem/ecosystem.json`, section `kaggle`);
retired machine shapes (P100, the older TPU shapes) are never offered:

- **`cpu`**: CPU; no machine shape.
- **`gpu-t4x2`**: GPU T4 x2 (`NvidiaTeslaT4`); the default.
- **`tpu-v5e8`**: TPU v5e-8 (`TpuV5E8`).

```bash
lemtrain kaggle accelerators
```

#### 4. Bundle, Launch and Status

```bash
# Write the kernel bundle (notebook + kernel-metadata.json) for review
lemtrain kaggle bundle upn_v2 --out ../kaggle_bundle

# Push the kernel and start the session
lemtrain kaggle launch upn_v2 --accelerator gpu-t4x2

# Test fix-branch code for 45 minutes, stopping 5 minutes before the limit
lemtrain kaggle launch upn_v2 --git-ref fix/review-remediation \
  --limit-hours 0.75 --margin-minutes 5

# Session status (QUEUED, RUNNING, COMPLETE, ERROR, CANCEL_REQUESTED, ...)
lemtrain kaggle status upn_v2
```

The kernel id is `<user>/<registry slug>-training`; the bundle is private with
internet on and mounts the model's manifold datasets and, when the Hub has
one, the latest `pytorch/default` version (`--resume-version N` pins another).
The same options exist on `python -m training.kaggle_cloud_manager --action
launch` and, as JSON fields, on `POST /api/training/kaggle/train`:

- **`--git-ref`**: Branch, tag or full commit SHA the kernel clones the
  suite at (default `main`). Letters, digits, `.`, `_`, `/` and `-` only, a
  letter or digit first, at most 200 characters; the clone prints
  `[GIT] <url> at <ref> (<sha>)`.
- **`--env-manager-ref`**: Ref of the env-manager clone (default: the
  `--git-ref` value).
- **`--limit-hours`**: Session limit for this kernel (default
  `kaggle_session.limit_hours` of `config.yaml`, 12).
- **`--margin-minutes`**: Minutes before the limit the trainer stops (default
  `kaggle_session.margin_minutes`, 30).
- **`--override-frozen`**: Resume although a frozen run setting changed
  (logged and recorded in `settings_changes.jsonl`); also used by the
  auto-resume sessions of a GUI job.

#### 5. Session Guard, Deadline Stop and Auto-Resume

- **12 h session guard**: the first cell exports `LEMGENDARY_SESSION_START`;
  the training and validation loops check the deadline (limit minus margin)
  every step and before each epoch. Under DDP the ranks agree every 25 steps,
  so no rank stops alone.
- **Deadline stop**: at the deadline the loop saves `progress.pth`
  (generator states included), writes
  `LemGendaryModels/<model>/session_deadline.json`, runs the final Hub sync,
  prints `[DEADLINE]` and exits 0. No release export runs.
- **Auto-resume**: a GUI or API job launched with `auto_resume: true` (default
  `kaggle_session.auto_resume`, false) reads the marker from the kernel output
  and pushes a new kernel version that resumes from the Hub, at most
  `max_resumes` times (default 3). `lemtrain kaggle launch` starts one
  session and does not watch it.
- **Publish gate**: the training cell ends with
  `training.cloud.trainer_exit.check_trainer_exit`. A non-zero trainer exit
  raises `TrainerExitError`, the kernel ends with `ERROR` and no later cell
  (release publish, Google Drive mirror) runs. Exit 0 with
  `session_deadline.json` is the resumable deadline stop; the publish cell
  skips itself on the marker.
- **Resume refusal record**: a resume refused because a frozen setting
  changed writes `LemGendaryModels/<model>/resume_refusal.json` (the
  `FrozenSettingsChanged` text and the changed setting names). The Kaggle job
  then fails with that text as its `error_message`, the same text a local job
  records. Relaunch with `--override-frozen` or start fresh.

#### 6. Kaggle Models Hub Variations and Push Policy

`VariationKey` (`training/cloud/variations.py`) is the single list of Hub
variations: `pytorch/default` (checkpoints, `README.md`, `metrics.csv`),
`pytorch/fp32` (`<Stem>.pt`), `onnx/fp16` (`<Stem>.onnx`) and `onnx/fp32`
(`<Stem>_FP32.onnx` + `.onnx.data`). `--variation` and the API `variation`
take one of them or `all`; the old names (`pytorch`, `onnx_fp16`) are
refused.

One push policy (`KaggleModelSyncManager.push_model`) serves the GUI,
`lemtrain sync push`, `kaggle_cloud_manager` and the notebook release:
validate the key, stage `dist/kaggle`, create or update the model page before
the first upload (a failed page sync uploads nothing), upload each variation
with the license from the model metadata, then sync the metadata again. A
variation whose staged files have the same SHA-256 as its last upload
(recorded in `<model>/.kaggle_sync.json`) is skipped: no new Hub version,
`UNCHANGED` in the log. The per-epoch auto-sync uploads only
`pytorch/default`, every `fleet.kaggle_sync_every_epochs` epochs (default 5)
and on a new best (`fleet.kaggle_sync_on_best`).

Every upload carries version notes with the stored epoch, up to six measured
values of the last `metrics.csv` row and the suite version, for example
`Release: mirnet_exposure [ONNX FP16] | epoch 41 | val_loss=0.0123
psnr=27.1000 | suite v16.9.177`.

#### 7. First Live Check

1. Attach `KAGGLE_API_TOKEN` and `GITHUB_PAT` to the kernel.
2. `lemtrain kaggle bundle upn_v2 --out <folder>` and review
   `kernel-metadata.json`.
3. `lemtrain kaggle launch upn_v2 --accelerator gpu-t4x2 --limit-hours 0.2
   --margin-minutes 5`.
4. Expect `[AUTH] Secrets available` with both secrets, checkpoints under
   `/kaggle/working/LemGendaryModels/<model>/checkpoints/`, `[DEADLINE]` and
   `session_deadline.json` in the output, `COMPLETE` from `lemtrain kaggle
   status upn_v2` and Hub version notes with the epoch and suite version.
5. Launch again: the session resumes from the Hub. A second push of
   unchanged files reports every variation as `UNCHANGED`.

---

## 7. Models Hub & Verification Toolchain

The `LemGendaryModels` repository hosts trained neural checkpoints and model cards.

Validation and inspection:

```bash
# Model validation is executed centrally via Environment Manager:
lem-env validate --project LemGendaryModels

# Regenerate all 23 model README cards and validate/stage variations
python -m training.doc_generator --all --stage-variations

# Regenerate single model README card
python -m training.doc_generator --model yolov8n --stage-variations

# Regenerate LemGendaryModels/README.md live SOTA matrix and canonical topology
python -m training.hub_readme_generator

# Check model checkpoint integrity directly
python \
  -c "import torch; print(torch.load('NAFNet/checkpoints/nafnet_weights.pth', map_location='cpu').keys())"
```

---

## 8. Documentation Hub & Static Validation

The `lemgendary-docs` repository contains technical research whitepapers, HTML
documentation, and operational manuals.

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

- **`0`**: Meaning: Success; Operator Action: Operation completed successfully
  with zero violations or errors
- **`1`**: Meaning: General Failure; Operator Action: Unhandled exception or
  syntax failure during execution
- **`2`**: Meaning: Validation Error; Operator Action: One or more quality,
  linting, or domain gates failed verification
- **`3`**: Meaning: Missing Prerequisites; Operator Action: Required toolchain
  component (Python, Git, NPM) is not installed
- **`4`**: Meaning: Network / IO Error; Operator Action: Failed to reach remote
  registry or download necessary assets

Continuous Integration Workflow Example:

```bash
# Standard CI/CD verification pipeline
lem-env audit --fast || exit 1
lem-env validate || exit 2
```

---

## Companion Documentation

- [Technical Whitepaper (Markdown)](PAPER_ENV_MANAGER.md)
- [Technical Whitepaper (HTML)](../papers/env_manager.html)
- [Master REST & WebSocket API Specification (Markdown)](MANUAL_API.md)
- [Master REST & WebSocket API Specification (HTML)](../papers/api-manual.html)
