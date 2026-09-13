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
- [3. Interactive PowerShell Host (`lemgendary_env_manager.ps1`)](#3-interactive-powershell-host-lemgendary_env_managerps1)
- [4. AI Studio Desktop GUI CLI & Toolchain](#4-ai-studio-desktop-gui-cli--toolchain)
- [5. Datasets Compilation Suite CLI](#5-datasets-compilation-suite-cli)
- [6. Training Suite & Neural Model Registry CLI](#6-training-suite--neural-model-registry-cli)
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

- Detects GPU acceleration backends including NVIDIA CUDA, AMD ROCm, Apple Metal Performance Shaders, and CPU fallback.
- Detects MetaTrader 5 terminal installations, install directories, and software versions.
- Queries GitHub and package registries to notify operators of available toolchain updates.

---

### 2.3 Ecosystem Health Audit (`audit`)

The `audit` command executes an exhaustive diagnostic audit of all seven repositories in the ecosystem.

```bash
lem-env audit
```

Diagnostic checks performed:

- Toolchain prerequisites verification for Python, Git, NPM, and MetaTrader 5.
- Virtual environment presence, Python executable health, and missing package count for each repository.
- Node.js workspace health, inspecting `package.json`, `node_modules`, and declared dependencies.
- Detailed NPM Package Dependency Matrix inspecting declared versus installed package versions.
- Version Drift Matrix identifying package version discrepancies across project boundaries.

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
| `--clean / --no-clean` | None | Bool | `True` | Completely purge existing `.venv` and `node_modules` before fresh recreation |

The pipeline executes in sequential order:

1. Hardware discovery and backend acceleration detection.
2. Global toolchain verification (Python, Git, NPM).
3. Virtual environment provisioning and purge.
4. Python package installation using locked manifests.
5. Node.js package installation via NPM.
6. Post-install validation and import sanity tests.
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
- `requirements-docs.txt`

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

- Python Compilation: Bytecode verification with `py_compile`.
- Zero-Emoji Compliance: Scans all scannable text files for forbidden emoji glyphs.
- YAML Linting: Syntax validation with `yamllint`.
- JSON Validation: RFC 8259 syntax validation across all `.json` files.
- Markdown Linting: Style compliance via local `markdownlint-cli` with root configuration.
- PowerShell Analysis: Script quality checks with Microsoft `PSScriptAnalyzer`.
- ESLint & TypeScript: Static type checking (`tsc --noEmit`) and strict accessibility linting.
- W3C & WCAG 2.2 AA: Static HTML standards verification and accessibility checking via `pa11y`.
- Domain Gates: Whitepaper word-for-word synchronization, manifold integrity, and model checkpoint validity.

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
lem-env serve --host 0.0.0.0 --port 8765
```

| Option | Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--host` | `-h` | Text | `127.0.0.1` | Network interface address to bind the HTTP listener |
| `--port` | `-p` | Int | `8765` | TCP port for incoming REST and WebSocket connections |
| `--reload` | None | Bool | `False` | Enable auto-reload on source file changes for local development |

---

## 3. Interactive PowerShell Host (`lemgendary_env_manager.ps1`)

For Windows terminal operators, `lemgendary_env_manager.ps1` provides an interactive, keyboard-driven management console.

Execution syntax:

```powershell
powershell -ExecutionPolicy Bypass -File .\lemgendary_env_manager.ps1
```

Interactive Menu Matrix:

- `[1] Probe System & Hardware Accelerators`: Executes hardware discovery and checks for updates.
- `[2] Run Full Ecosystem Health Audit`: Displays toolchain, virtual environment, and NPM dependency matrix.
- `[3] Execute Smart Clean Install Pipeline`: Purges environments and installs clean dependencies.
- `[4] Run Safe Package Updates`: Executes bottom-up dependency upgrades and syncs manifests.
- `[5] Validate Projects`: Enforces py_compile, ESLint, YAML, JSON, W3C, WCAG 2.2 AA, and domain gates.
- `[6] Start Background API Server`: Launches the FastAPI server with live WebSocket streaming.
- `[7] Purge Build & Cache Artifacts`: Cleans temporary residues and caches across all projects.
- `[8] Exit`: Gracefully terminates the management console.

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

The `lemgendary-datasets` repository contains data synthesis and manifold compilation pipelines.

CLI Operations:

```bash
# Navigate to datasets directory
cd lemgendary-datasets

# Compile all registered image restoration and vision datasets
python compile_all_datasets.py

# Compile specific dataset manifold
python compile_dataset.py --target LemGendizedFFANet

# Compile Forex & Commodities trading manifold
python compile_forex_dataset.py --timeframe M5 --symbols EURUSD,GBPUSD,USDJPY,XAUUSD

# Synchronize compiled manifolds with remote cloud storage
python cloud_sync.py --direction upload --provider gcs
```

---

## 6. Training Suite & Neural Model Registry CLI

The `lemgendary-training-suite` repository provides training engines, loss functions, and evaluation scripts.

CLI Operations:

```bash
# Navigate to training suite
cd lemgendary-training-suite

# Launch neural training run with Sawtooth Governor and Memory Sentinel
python train.py --config configs/nafnet_baseline.yaml --backend cuda

# Run SOTA validation ladder evaluation
python evaluate.py --model checkpoints/nafnet_best.pth --dataset LemGendizedNAFNet

# Export trained PyTorch weights to WebGPU optimized ONNX
python export_onnx.py --model checkpoints/nafnet_best.pth --opset 17 --output webgpu/nafnet.onnx

# Run hardware inference benchmark
python benchmark.py --model webgpu/nafnet.onnx --batch-size 1
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
lem-env audit || exit 1
lem-env validate || exit 2
```
