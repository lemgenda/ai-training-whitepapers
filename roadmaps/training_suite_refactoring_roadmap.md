# LemGendary Model Training Suite — 2026 Refactoring & Modernization Roadmap (v3)

> Supersedes the v1 inline draft and v2 interim roadmap.
> Interoperates with `lemgendary-docs/roadmaps/dataset_compiler_modernization_roadmap.md` (Dataset Compiler Suite v16.7.2-SOLID).
> Aligns with LemGendary Environment Manager v2.0.0 / v2.3 (API, CLI, and validation patterns).
> Written against the codebase, whitepapers, and sibling-project contracts as of 2026-09.

---

## 1. Executive Summary

The LemGendary Model Training Suite contains a legacy 2,600-line `core_loop.py` coordinator surrounded by multiple modules of overlapping concerns. While the training mathematics (losses, rollback, telemetry, network heads) and specialized time-series optimizations (`ParquetRowGroupCache` v2.3, `RowGroupAwareSampler`) are mathematically proven and high-performing, the surrounding execution scaffolding requires modernization to match the S.O.L.I.D. architectural standards established by its sibling projects: the LemGendary Dataset Compiler Suite (`v16.7.2-SOLID`) and the LemGendary Environment Manager (`v2.0.0`).

This refactoring achieves eight concurrent outcomes in execution order:

1. **Monolith Decomposition**: `core_loop.py` is reduced from 2,600 lines to a slim ~50-line pipeline coordinator, delegating to focused subpackages (`training/`, `hardware/`, `checkpoint/`, `governance/`).
2. **In-Process S.O.L.I.D. Services Layer**: Implements `training/services/` (`TrainingService`, `EvaluationService`, `CheckpointService`, `ExportService`, `CloudSyncService`, `NotebookService`, `AuditService`), decoupling the CLI and API server from training mechanics without subprocess indirection.
3. **Strategy Pattern for Parallelism**: Integrates the modular parallel strategy layer (`training/parallel/`) supporting SingleGPU, DataParallel, and DDP with seamless checkpoint portability and automatic device resolution.
4. **Unified Container Readers**: Implements a unified `ContainerReader` protocol consuming all five container formats emitted by the LemGendary Dataset Compiler Suite (Directory with in-place lossless WebP, MDS, LitData, WebDataset, Parquet), alongside dynamic on-the-fly degradation (`DynamicOnTheFlyDegrader`).
5. **Unified Cloud Protocol Layer**: Collapses five overlapping cloud synchronization scripts into structured protocols in `training/cloud/` (`manager.py`, `git_hub.py`, `kaggle_hub.py`, `gdrive.py`) with structured `CloudSyncError` handling.
6. **Sidecar API & Desktop GUI Integration**: Establishes a FastAPI HTTP/WebSocket sidecar service on port 8200 with SQLite persistent job tracking (`.lemtrain_server/jobs.db`), real-time WebSocket log streaming (`/api/ws/jobs/{id}/logs`), canonical presets (`presets.yaml`), GUI aggregation endpoints (`/api/gui/state`, `/api/gui/quick-train`), and a frozen `openapi.json` contract.
7. **Root Decluttering & Ecosystem Tooling**: Relocates auxiliary scripts into `tools/`, centralizes models registry/metadata, eliminates loose scripts (`train_all.py`, `cloud_hub.py`, `sync_to_gdrive.py`, `judicial_audit_api.py`), evicts committed binary blobs (`yolov8n.pt`, `face_landmarker.task`), leaving only canonical entrypoints (`cli.py`, `lemgendary_models_hub.ps1`), manifests, and packages.
8. **Absolute Zero-Suppression Hardening**: 100% elimination of `# type: ignore`, `# noqa`, bare `except:`, `except Exception: pass`, and `warnings.filterwarnings`, achieving full compliance under `python -m env_manager.cli validate -p lemgendary-training-suite`.

---

## 2. Naming & Branding (Mandatory, Non-Negotiable)

All documentation, CLI help text, API responses, error messages, and code comments must use the project's **full branded name** — never abbreviations in user-facing surfaces. The seven-project ecosystem taxonomy:

| # | Project | Folder | Binary / Entry |
| --- | --- | --- | --- |
| 1 | LemGendary Environment Manager | `.\lemgendary-env-manager\` | `lem-env` |
| 2 | LemGendary Dataset Compiler Suite | `.\lemgendary-datasets\` | `lemgendary` |
| 3 | **LemGendary Model Training Suite** | `.\lemgendary-training-suite\` | `lemtrain` |
| 4 | LemGendary AI Studio GUI | `.\lemgendary-ai-studio-gui\` | Tauri IPC |
| 5 | LemGendary AI Documentation Hub | `.\lemgendary-docs\` | — |
| 6 | LemGendary Compiled Manifolds Repo | `./LemGendaryDatasets\` | — |
| 7 | LemGendary Trained Models Repo | `.\LemGendaryModels\` | — |

**Rule**: No bare nouns in user-facing output. "The training suite" is never a sentence subject. Error messages must state `LemGendary Model Training Suite: <message>`.

---

## 3. Scope Boundaries

### 3.1 In Scope

Everything located under `.\lemgendary-training-suite\`:

- `training/` core subpackages:
  - `training/services/` (in-process S.O.L.I.D. service layer)
  - `training/cli/` (Typer command tree)
  - `training/server/` (FastAPI sidecar application, WebSocket handlers, routes)
  - `training/training/` (engine, epoch runner, validation, optimizer, context)
  - `training/hardware/` (device discovery, execution policy, VRAM probe, sentinel)
  - `training/data/` (loaders, worker topology, manifold resolver, containers)
  - `training/checkpoint/` (manager, recovery BFS, resume state, metric vaults)
  - `training/governance/` (metrics registry, curriculum, thermal state, SOTA tracker)
  - `training/parallel/` (parallel strategies: SingleGPU, DataParallel, DDP)
  - `training/cloud/` (cloud managers: GitHub, Kaggle Hub, Google Drive)
  - `training/export/` (format exporters: ONNX, Torch Standalone, WebGPU, MT5 Signal)
  - `training/notebooks/` (cell generators, builders, registry)
  - `training/telemetry/` (telemetry engine, CSV writers)
  - `training/utils/` (logging, paths, subprocess, interrupt, delegates)
- `models/` (neural network architectures, backbones, and head definitions)
- `tools/` (relocated operational CLI tools with repository root bootstrapping)
- Root entry points and manifests:
  - `cli.py` (canonical root entry point for `lemtrain`)
  - `lemgendary_models_hub.ps1` (orchestration hub script)
  - `config.yaml` (global configuration manifest)
  - `unified_models_v2.yaml` (neural network model registry)
  - `presets.yaml` (canonical training presets)
- Eviction of committed binary blobs (`yolov8n.pt`, `face_landmarker.task`) to model storage.

### 3.2 Explicitly Out of Scope

| Concern | Owner | Architectural Rule |
| --- | --- | --- |
| Dataset compilation, transcoding, format conversion, source auditing | LemGendary Dataset Compiler Suite | Training reads artifacts; never compiles datasets |
| Virtual environment creation, pip installation, manifest sync, code validation, git hooks | LemGendary Environment Manager | Training delegates via typed adapter or REST |
| Dataset storage, versioning, remote manifold hosting | LemGendary Compiled Manifolds Repo | Read-only local/remote mount |
| Production model weights storage, versioning | LemGendary Trained Models Repo | Read/write via `CloudManager` |
| Whitepapers, technical manuals, cross-project architecture documentation | LemGendary AI Documentation Hub | Training links to docs; never ships raw docs |
| Desktop Cross-Project Automation (CPA) GUI | LemGendary AI Studio GUI | Training exposes OpenAPI 3.1 contract; GUI consumes |

### 3.3 The Boundary Rule

**If a capability relates to Python packages, virtual environments, code quality enforcement, or dataset compilation, it does not live in this repository.** The LemGendary Model Training Suite calls `lem-env` and `lemgendary` via structured client adapters or local HTTP sidecars, treating their return codes and schemas as authoritative.

### 3.4 No Internal Datasets or Docs

This repository does **not** contain `datasets/` or `docs/` directories. Dataset content lives in the LemGendary Compiled Manifolds Repo (`./LemGendaryDatasets/`). Documentation lives in the LemGendary AI Documentation Hub. The training suite's `README.md` serves strictly as a **changelog**, not a feature guide.

---

## 4. Integration with Sibling Projects

### 4.1 Environment Manager Delegation

The suite communicates with the LemGendary Environment Manager via typed adapter `training.utils.env_delegate.EnvManagerDelegate`:

```python
# training/utils/env_delegate.py
class EnvManagerDelegate:
    def __init__(self, project_root: Path, sidecar_port: int = 8000) -> None:
        self.project_root = project_root
        self.sidecar_url = f"http://127.0.0.1:{sidecar_port}"

    def validate_codebase(self) -> bool:
        """Run full multi-gate validation via lem-env CLI with timeout."""
        cmd = [
            "python", "-m", "env_manager.cli", "validate",
            "-p", "lemgendary-training-suite"
        ]
        result = subprocess.run(
            cmd, cwd=self.project_root, capture_output=True,
            text=True, timeout=120, check=False
        )
        if result.returncode != 0:
            logger.error("Environment Manager validation failed:\n%s", result.stdout)
            return False
        return True

    def is_sidecar_online(self) -> bool:
        """Probe environment manager sidecar health."""
        try:
            with urllib.request.urlopen(f"{self.sidecar_url}/api/health", timeout=1.0) as resp:
                return resp.status == 200
        except Exception:
            return False
```

### 4.2 Dataset Compiler Integration

The LemGendary Dataset Compiler Suite (`v16.7.2-SOLID`) emits manifolds in up to five container formats. The LemGendary Model Training Suite reads all five via a unified `ContainerReader` protocol that mirrors the compiler's `Writer` protocol 1:1:

```python
# training/data/containers/base.py
class Sample(NamedTuple):
    name: str
    image_bytes: bytes
    image_format: str
    target_bytes: bytes | None
    mask_bytes: bytes | None
    label: dict[str, Any]
    metadata: dict[str, Any]

class ContainerReader(Protocol):
    format_name: ClassVar[str]
    def open(self, manifold_root: Path) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[Sample]: ...
    def get(self, idx: int) -> Sample: ...
    def close(self) -> None: ...
```

Concrete readers supported:

| Format | Reader Class | Backing Implementation | Notes |
| --- | --- | --- | --- |
| `directory` | `DirectoryReader` | stdlib + PIL / TurboJPEG | Native directory layout; decodes lossless WebP |
| `mds` | `MdsReader` | `streaming` (MosaicML) | Global streaming shuffle, Zstd compression |
| `litdata` | `LitDataReader` | `litdata` (PyTorch) | Optimized for variable-shape arrays |
| `webdataset` | `WebDatasetReader` | `webdataset` | Sharded tar format for sequential streaming |
| `parquet` | `ParquetReader` | `pyarrow` + `ParquetRowGroupCache` | Financial time-series; decode-at-fill caching |

Auto-resolution is handled by `training.data.containers.resolve(manifold_root)`, which inspects `dataset_info.yaml:container.primary`. In addition, dynamic degradation during training is powered by `training.data.degrade.DynamicOnTheFlyDegrader`, mirroring the compiler's `degrade/` package for on-the-fly image restoration augmentation.

Model metadata is resolved from `lemgendary-datasets/models/models_metadata.yaml` with seamless fallbacks.

### 4.3 Full Ecosystem Wiring

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LemGendary AI Studio Desktop GUI                         │
│                  Consumes OpenAPI 3.1 specs from all 3 services             │
└──────────────┬──────────────────────┬──────────────────────┬────────────────┘
               │ Port 8000            │ Port 8100            │ Port 8200
      ┌────────▼────────┐    ┌────────▼────────┐    ┌────────▼────────┐
      │  lemgendary-    │    │  lemgendary-    │    │  lemgendary-    │
      │  env-manager    │    │  datasets       │    │  training-suite │
      │                 │    │                 │    │                 │
      │  CLI: lem-env   │    │  CLI: lemgendary│    │  CLI: lemtrain  │
      │  FastAPI+Typer  │    │  FastAPI+Typer  │    │  FastAPI+Typer  │
      │  + Rich         │    │  + Rich         │    │  + Rich         │
      │                 │    │                 │    │  Services Layer │
      └────────┬────────┘    └────────┬────────┘    └────────┬────────┘
               │                      │                      │
               │ Subprocess / HTTP    │ Subprocess / HTTP    │
               │ (Code validation,    │ (Dataset audit,      │
               │  dependency sync)    │  transcode, fetch)   │
               └──────────────────────┴──────────────────────┘
```

---

## 5. Current State Assessment

### 5.1 What is Healthy and Retained

- **`training/losses.py`** — Mathematical implementations for Focal, EMD, Rank, and Dual-loss. Time-tested and mathematically verified.
- **`training/telemetry.py`** — Quality score computation and streaming metrics tracker.
- **`training/sota_rollback.py`** — Atomic state-saving and rollback primitives.
- **`training/model_registry.py`** — Checkpoint loading helpers and architectural introspection.
- **`models/*.py` and `models/heads/*.py`** — Complete neural network architectures and multi-task heads.
- **`training/parallel/`** — Strategy pattern implementation (`base.py`, `single.py`, `dp.py`, `ddp.py`, `__init__.py`, `__main__.py`).
- **`data/forex_dataset.py` (v2.3)** — `ParquetRowGroupCache` with decode-at-fill caching, eliminating per-row pyarrow extraction overhead.
- **`data/forex_sampler.py`** — `RowGroupAwareSampler` providing 99%+ cache hit rate under walk-forward training.
- **`data/dataset.py`** — Multi-task vision dataset with `DynamicOnTheFlyDegrader` augmentation.

### 5.2 What is Fused and Requires Extraction

| Concern | Current Location | Target Location | Architecture Role |
| --- | --- | --- | --- |
| In-process workflow coordination | Split across `cli.py` & `main()` | `training/services/*.py` | S.O.L.I.D. Services Layer |
| Device discovery & sensors | `main()` inline | `training/hardware/discovery.py` | Hardware abstraction |
| Execution & precision policy | `main()` inline | `training/hardware/policy.py` | AMP / cuDNN / channels-last |
| VRAM sentinel & OOM recovery | Loop inline | `training/hardware/sentinel.py` | Proactive memory guard |
| Worker topology calculation | `main()` inline | `training/data/workers.py` | CPU thread allocation |
| DataLoader factories | 7 duplicated sites | `training/data/loaders.py` | Unified builder functions |
| Manifold path resolution | 4 duplicated copies | `training/data/manifold.py` | Single Source of Truth |
| Resume state calculation | ~700 lines inline | `training/checkpoint/resume.py` | Typed `ResumeState` |
| Kaggle recovery BFS | ~200 lines inline | `training/checkpoint/recovery.py` | Checkpoint search engine |
| SOTA metric tracking | Mixed in `optimization_engine.py` | `training/governance/sota.py` | Dedicated SOTA tracker |
| Curriculum phase transitions | Mixed in `optimization_engine.py` | `training/governance/curriculum.py` | Resolution ladder state |
| Thermal logit clamping | Mixed in `optimization_engine.py` | `training/governance/thermal.py` | Softmax temperature state |
| Cloud synchronization | 5 overlapping files | `training/cloud/*.py` | Protocol-based cloud sync |
| Operational root scripts | 5 root scripts | `tools/*.py` | Root decluttering |

### 5.3 Silent Failures to Eradicate

All silent failures, swallowed exceptions, and compiler suppressions are strictly prohibited across the codebase:

1. **Zero Suppression Tolerance**: Absolute ban on `# type: ignore`, `# noqa`, `# pylint: disable`, and `warnings.filterwarnings('ignore')`. All type ambiguities and linter warnings must be resolved at the root cause through proper type narrowing and explicit typing.
2. **Zero Swallowed Exceptions**: Every `except: pass`, `except Exception: pass`, or `except: return (None,)*4` is replaced with structured contextual logging (`logger.warning(...)` / `logger.error(...)`) or typed domain exceptions (`GovernorStateError`, `CloudSyncError`, `ContainerReadError`).
3. **Automated Enforcement**: Pre-commit hooks installed by `lem-env setup-hooks` execute `lem-env validate`, failing any commit containing banned patterns.

---

## 6. Target Architecture

The target layout adopts a flat package structure matching sibling conventions. Root clutter is eliminated:

```text
lemgendary-training-suite/
├── cli.py                                  <-- Canonical root entrypoint for lemtrain
├── lemgendary_models_hub.ps1               <-- Root orchestration script
├── config.yaml                             <-- Global configuration manifest
├── unified_models_v2.yaml                  <-- Neural network model registry
├── presets.yaml                            <-- Canonical training presets
├── pyproject.toml                          <-- Build system & tool configurations
├── pyrightconfig.json                      <-- Pyright type-checking configuration
├── .pylintrc                               <-- Pylint linting configuration
├── .gitignore                              <-- Cleaned gitignore
├── README.md                               <-- Changelog strictly (links to Docs Hub)
├── tools/                                  <-- Relocated auxiliary operational tools
│   ├── train_all.py
│   ├── cloud_hub.py
│   ├── sync_to_gdrive.py
│   ├── generate_notebooks.py
│   ├── judicial_audit.py
│   └── export_model.py
├── models/                                 <-- Neural network architectures
│   ├── __init__.py
│   ├── heads/
│   └── *.py
├── data/                                   <-- Datasets & data ingestion
│   ├── __init__.py
│   ├── dataset.py
│   ├── forex_dataset.py
│   ├── forex_sampler.py
│   ├── mt5_pipeline.py
│   └── yolo_config_gen.py
├── export/                                 <-- Model export implementations
│   ├── __init__.py
│   ├── onnx_export.py
│   ├── webgpu_export.py
│   └── mt5_signal_export.py
├── cloud_jobs/                             <-- Cloud kernel configurations
├── tests/                                  <-- Comprehensive test suites
│   ├── unit/
│   ├── integration/
│   ├── smoke/
│   └── fixtures/
└── training/                               <-- Core framework package
    ├── __init__.py
    ├── services/                           <-- In-Process S.O.L.I.D. Services Layer
    │   ├── __init__.py
    │   ├── training_service.py             <-- Training execution lifecycle orchestrator
    │   ├── eval_service.py                 <-- Evaluation, metrics, and judicial auditing
    │   ├── checkpoint_service.py           <-- Checkpoint recovery, resume, and SOTA rollback
    │   ├── export_service.py               <-- Model export orchestration (ONNX, WebGPU, etc.)
    │   ├── sync_service.py                 <-- Cloud synchronization orchestrator
    │   ├── notebook_service.py             <-- Notebook generation from cell modules
    │   └── audit_service.py                <-- VRAM, model parameter, and compliance audit
    ├── cli/                                <-- Typer CLI tree
    │   ├── __init__.py
    │   ├── lemtrain.py                     <-- Main Typer CLI app
    │   ├── lemtrain_curriculum.py
    │   ├── lemtrain_export.py
    │   ├── lemtrain_notebooks.py
    │   └── lemtrain_server.py
    ├── server/                             <-- FastAPI Sidecar Service (Port 8200)
    │   ├── __init__.py
    │   ├── app.py                         <-- FastAPI application & lifespan management
    │   ├── auth.py                        <-- Token auth & local master key (.lemtrain_server/token)
    │   ├── events.py                      <-- WebSocket ConnectionManager
    │   ├── jobs.py                        <-- SQLite persistent job queue (.lemtrain_server/jobs.db)
    │   └── routes/                        <-- Modular API route handlers
    │       ├── __init__.py
    │       ├── health.py                  <-- Sensors, VRAM, and process health
    │       ├── config.py                  <-- Configuration inspection & validation
    │       ├── jobs.py                    <-- Job submission, cancellation, status, logs
    │       ├── models.py                  <-- Model architectures, weights, parameters
    │       ├── training.py                <-- Training launch, pause, and live metrics
    │       ├── datasets.py                <-- Manifold inspection & dataset passthrough
    │       ├── env.py                     <-- Env-manager sidecar passthrough (Port 8000)
    │       └── gui.py                     <-- Desktop GUI aggregated state & quick-train
    ├── training/                           <-- Execution Engine
    │   ├── __init__.py
    │   ├── context.py                     <-- Immutable TrainingContext dataclass
    │   ├── engine.py                      <-- run_training(ctx) coordinator
    │   ├── epoch.py                       <-- train_one_epoch(ctx, epoch)
    │   ├── validation.py                  <-- validate_one_epoch(ctx)
    │   ├── optimizer.py                   <-- Optimizer & scheduler builders
    │   ├── amp.py                         <-- Mixed precision & GradScaler management
    │   └── losses.py                      <-- Focal, EMD, Rank, and Dual losses
    ├── hardware/                           <-- Hardware Subsystem
    │   ├── __init__.py
    │   ├── discovery.py                   <-- CUDA / ROCm / MPS / CPU discovery
    │   ├── probe.py                       <-- Deep VRAM audit & hardware capability probe
    │   ├── policy.py                      <-- Execution policy (AMP, cuDNN, memory formats)
    │   └── sentinel.py                    <-- VRAM SentinelGuard & proactive OOM prevention
    ├── data/                               <-- Data Ingestion & Containers
    │   ├── __init__.py
    │   ├── manifold.py                    <-- Canonical ManifoldResolver
    │   ├── workers.py                     <-- Worker topology calculation & disposal
    │   ├── loaders.py                     <-- Unified DataLoader factory functions
    │   ├── degrade.py                     <-- DynamicOnTheFlyDegrader augmentation
    │   └── containers/                    <-- Container Reader Plugins
    │       ├── __init__.py                <-- resolve(manifold_root) factory
    │       ├── base.py                    <-- ContainerReader Protocol & Sample NamedTuple
    │       ├── directory.py               <-- DirectoryReader (WebP lossless decoder)
    │       ├── mds.py                     <-- MdsReader (Streaming Zstd)
    │       ├── litdata.py                 <-- LitDataReader (Variable-shape)
    │       ├── webdataset.py              <-- WebDatasetReader (Tar-sharded)
    │       └── parquet.py                 <-- ParquetReader (ParquetRowGroupCache v2.3)
    ├── checkpoint/                         <-- Checkpoint Management
    │   ├── __init__.py
    │   ├── manager.py                     <-- CheckpointManager save/load
    │   ├── recovery.py                    <-- Kaggle BFS recovery engine
    │   ├── resume.py                      <-- ResumeState dataclass & scaler logic
    │   └── vault.py                       <-- MetricVault history tracker
    ├── governance/                         <-- Training Governance
    │   ├── __init__.py
    │   ├── metrics.py                     <-- MetricRegistry, directions, and weights
    │   ├── curriculum.py                  <-- Dynamic curriculum & resolution ladder
    │   ├── thermal.py                     <-- Softmax temperature & logit clamping
    │   ├── sota.py                        <-- SotaTracker & rollback decisions
    │   └── governor.py                    <-- SmartTrainingGovernor orchestrator
    ├── parallel/                           <-- Parallel Strategy Layer (Strategy Pattern)
    │   ├── __init__.py                    <-- Strategy factory & auto-resolution policy
    │   ├── base.py                        <-- ParallelStrategy ABC
    │   ├── single.py                      <-- SingleGPUStrategy
    │   ├── dp.py                          <-- DataParallelStrategy
    │   ├── ddp.py                         <-- DistributedDataParallelStrategy
    │   └── __main__.py                    <-- Diagnostic strategy CLI
    ├── cloud/                              <-- Cloud Synchronization
    │   ├── __init__.py
    │   ├── manager.py                     <-- CloudManager protocol & error definitions
    │   ├── credentials.py                 <-- Credential manager for secrets
    │   ├── git_hub.py                     <-- Git synchronization
    │   ├── kaggle_hub.py                  <-- Kaggle dataset & model push/pull
    │   └── gdrive.py                      <-- Google Drive synchronization
    ├── export/                             <-- Export Subsystem
    │   ├── __init__.py
    │   ├── common.py                      <-- Base export utilities
    │   ├── onnx.py                        <-- ONNX export with dynamic/fixed axes
    │   ├── torch_standalone.py            <-- Standalone torchscript/weights export
    │   ├── webgpu.py                      <-- WebGPU-optimized ONNX export
    │   └── mt5_signal.py                  <-- Financial signal export
    ├── notebooks/                          <-- Notebook Generation Subsystem
    │   ├── __init__.py
    │   ├── cells/                         <-- Individual cell generator modules
    │   ├── builders/                      <-- Platform builders (Kaggle, Colab)
    │   └── registry.py                    <-- Template registry
    ├── telemetry/                          <-- Telemetry Subsystem
    │   ├── __init__.py
    │   ├── engine.py                      <-- Live telemetry computation
    │   └── csv_writer.py                  <-- Streaming CSV logger
    └── utils/                              <-- Shared Utilities
        ├── __init__.py
        ├── logging.py                     <-- ForceTTY logger & Rich formatting
        ├── paths.py                       <-- Repository root discovery & path utilities
        ├── subprocess.py                  <-- Subprocess runner with timeout & exit codes
        ├── interrupt.py                   <-- Graceful signal handling
        ├── env_delegate.py                <-- EnvManagerDelegate adapter
        └── dataset_delegate.py            <-- DatasetCompilerDelegate adapter
```

---

## 7. README as Changelog

`README.md` in this repository serves exclusively as a **changelog**. Feature guides and architecture whitepapers live in the LemGendary AI Documentation Hub.

Format standard:

```markdown
# LemGendary Model Training Suite — Changelog

Manual: https://lemgenda.github.io/ai-training-whitepapers/index.html

## [Unreleased]
### Added
- In-Process S.O.L.I.D. Services Layer (`training/services/`)
- Sidecar API server on port 8200 with SQLite persistent jobs and WebSocket logs
- Container reader adapters for MDS, LitData, WebDataset, and lossless WebP Directory
- Canonical training presets in `presets.yaml`

### Changed
- Monolithic `core_loop.py` decomposed into modular coordinator and engine subpackages
- Root directory decluttered, moving auxiliary scripts to `tools/` and adding `cli.py`

### Fixed
- Completely purged all bare except clauses, except pass blocks, and warning suppressions
- Replaced unhandled numpy load exceptions in `data/forex_dataset.py` with structured errors
```

---

## 8. Phases

### Phase 0 — Baseline Freeze & Binary Blobs Eviction (0.5 day)

- Tag repository at `git tag pre-refactor-v2` on `main`.
- Evict committed binary weights (`yolov8n.pt`, `face_landmarker.task`) from git tracking, relocating them to external model storage / cache.
- Establish `tests/smoke/test_entrypoints.py` to freeze legacy CLI entry points.
- Create `tests/fixtures/tiny_dataset/` (8 synthetic samples per task) and `tests/fixtures/tiny_checkpoint.pth`.
- Create clean `pyproject.toml` and configure `pyrightconfig.json` without suppressions.

**Gate 0:** Baseline smoke tests pass and binary blobs are fully untracked.

### Phase 1 — Core Utilities, Structured Secrets & Delegation Adapters (1 day)

- Implement `training/utils/logging.py` with `ForceTTY` and Rich console streaming.
- Implement `training/utils/paths.py` with project root auto-discovery.
- Implement `training/utils/subprocess.py` and `training/utils/interrupt.py`.
- Implement `training/utils/env_delegate.py` and `training/utils/dataset_delegate.py`.
- Implement `training/config/secrets.py` unifying dotfile credentials (`.GITHUB_PAT`, `.SUITE_PAT`, `.SATURN_PAT`, `.GOOGLE_DRIVE`, `.kaggle_token`, `.kaggle_users`).

**Gate 1:** `core_loop.py` shrinks by ~200 lines. Zero bare `except:` blocks in moved utilities.

### Phase 2 — Hardware Discovery, Policy & Sentinel (2 days)

- Implement `training/hardware/discovery.py` returning structured `DeviceInfo`.
- Implement `training/hardware/probe.py` auditing deep VRAM capability.
- Implement `training/hardware/policy.py` applying AMP, cuDNN benchmarks, and memory format policies.
- Implement `training/hardware/sentinel.py` with proactive `SentinelGuard` and OOM recovery.

**Gate 2:** `core_loop.py` shrinks by ~400 lines. VRAM sentinel unit-tested under synthetic memory spikes.

### Phase 3 — Data Loaders, Worker Topologies & Manifold Resolver (2 days)

- Implement `training/data/manifold.py` with canonical `ManifoldResolver`, eliminating 4 duplicate implementations across the repository.
- Implement `training/data/workers.py` with `compute_worker_topology` and `dispose_loader`.
- Implement `training/data/loaders.py` exposing unified `build_train_loader` and `build_val_loader`.
- Integrate `training/data/degrade.py` (`DynamicOnTheFlyDegrader`) for dynamic augmentation.

**Gate 3:** All DataLoader construction routes through `loaders.py`. Zero `except: pass` in worker cleanup.

### Phase 4 — Modern Container Readers & Lossless WebP Decoders (3 days)

- Implement `training/data/containers/base.py` with `ContainerReader` protocol and `Sample` namedtuple.
- Implement `training/data/containers/directory.py` decoding lossless WebP and traditional images while respecting NTFS hardlinks.
- Implement `training/data/containers/mds.py` (`streaming`), `litdata.py` (`litdata`), and `webdataset.py` (`webdataset`).
- Implement `training/data/containers/parquet.py` wrapping PyArrow and `ParquetRowGroupCache` (v2.3).
- Implement `training/data/containers/__init__.py:resolve(manifold_root)` auto-inspecting `dataset_info.yaml`.

**Gate 4:** All 5 readers pass round-trip verification against fixture manifolds emitted by Dataset Compiler v16.7.2.

### Phase 5 — Checkpoint Management, Recovery & SOTA Rollback (3 days)

- Implement `training/checkpoint/manager.py` for atomic save/replace.
- Implement `training/checkpoint/recovery.py` with BFS Kaggle recovery search.
- Implement `training/checkpoint/resume.py` with typed `ResumeState` and iteration scaling.
- Implement `training/checkpoint/vault.py` tracking multi-metric progression.

**Gate 5:** `core_loop.py` shrinks by ~700 lines. Checkpoint resume tests pass under iteration scaling.

### Phase 6 — Governance, Curriculum, Thermal & Metric Registry (3 days)

Decompose `optimization_engine.py` (900 lines) into focused, testable state objects:

- `training/governance/metrics.py` — `MetricRegistry`, directions, and weights.
- `training/governance/curriculum.py` — `CurriculumState` and resolution ladder.
- `training/governance/thermal.py` — `ThermalState`, temperature decay, and logit clamping.
- `training/governance/sota.py` — `SotaTracker` and drift-gated rollback logic.
- `training/governance/governor.py` — Thin coordinator maintaining public `SmartTrainingGovernor` API.

**Gate 6:** `governor.audit_epoch()` behavior is byte-identical on recorded epoch-transition fixtures.

### Phase 7 — Unified Cloud Management (2 days)

- Implement `training/cloud/manager.py` with `CloudManager` protocol and structured `CloudSyncError`.
- Implement `training/cloud/credentials.py`.
- Implement `training/cloud/git_hub.py`, `training/cloud/kaggle_hub.py`, and `training/cloud/gdrive.py`.
- Purge all 12 bare `except:` blocks in legacy git synchronization.

**Gate 7:** Fixture model checkpoint pushed and pulled from Kaggle/GDrive test target with bit-exact hash verification.

### Phase 8 — Model Export Subsystem (1 day)

- Implement `training/export/common.py` and `training/export/__init__.py:export_all()`.
- Implement `training/export/onnx.py` supporting dynamic axes.
- Implement `training/export/torch_standalone.py`.
- Implement `training/export/webgpu.py` (Opset 17, fixed-shape, slice-error free).
- Implement `training/export/mt5_signal.py`.

**Gate 8:** `export_all` produces byte-identical exported artifacts compared to pre-refactor pipelines.

### Phase 9 — Modular Notebook Cell Architecture (3 days)

- Implement `training/notebooks/cells/*.py` exporting `build_cell(model_key, config) -> dict`.
- Implement `training/notebooks/builders/*.py` for Kaggle and Colab runtime targets.
- Implement `training/notebooks/registry.py`.
- Ensure Dataset Compiler generators can consume `training.notebooks.cells` directly.

**Gate 9:** Regenerated notebooks are structurally identical to baseline for `mirnet_exposure` and `forex_predictor`.

### Phase 10 — Training Engine Core Coordinator (3 days)

- Implement `training/training/context.py` with immutable `TrainingContext` dataclass.
- Implement `training/training/engine.py:run_training(ctx)`.
- Implement `training/training/epoch.py:train_one_epoch(ctx, epoch)`.
- Implement `training/training/validation.py:validate_one_epoch(ctx)`.
- Implement `training/training/optimizer.py` and `training/training/amp.py`.
- Shrink `training/core_loop.py` to a ~50-line backwards-compatible facade.

**Gate 10:** 3-epoch training run on `nima_technical` fixture matches pre-refactor metric trajectories within floating-point tolerance.

### Phase 10.5 — DistributedDataParallel (DDP) Multi-GPU Wiring (2 days, deferred post-Phase 12)

- Wire `training/parallel/ddp.py` into `run_training(ctx)`.
- Integrate `DistributedSampler` composed with `RowGroupAwareSampler` for Parquet workloads.
- Establish NCCL watchdog timeout (5 minutes) and automatic rank-0 file write gating.
- Update auto-resolution policy to select `ddp` for non-forex CUDA environments with >1 GPU.

**Gate 10.5:** 2-process `torchrun` on Kaggle T4x2 produces identical epoch-end metrics as single-GPU execution.

### Phase 11 — In-Process S.O.L.I.D. Services Layer & Canonical CLI (2 days)

- Implement in-process services under `training/services/`:
  - `TrainingService`: Job lifecycle, execution loop, device policy.
  - `EvaluationService`: Epoch validation, judicial audit, metric vaults.
  - `CheckpointService`: Checkpoint save, recovery BFS, SOTA rollback.
  - `ExportService`: Model exports (ONNX, WebGPU, standalone).
  - `CloudSyncService`: Cloud transfers (GitHub, Kaggle, GDrive).
  - `NotebookService`: Notebook compilation.
  - `AuditService`: Model parameter, VRAM, and zero-suppression audits.
- Implement Typer CLI under `training/cli/lemtrain.py` and root `cli.py` entrypoint.
- Relocate root operational scripts (`train_all.py`, `cloud_hub.py`, `sync_to_gdrive.py`, `judicial_audit_api.py`) to `tools/` with backwards-compatible shims.
- Implement hybrid CLI dispatch: CLI checks if sidecar is running on `127.0.0.1:8200`; if present, routes via HTTP; otherwise executes directly in-process via `services/`.

**Gate 11:** `lemtrain --help`, `lemtrain version`, and `lemtrain presets list` pass. In-process services execute cleanly without subprocess self-invocation.

### Phase 12 — FastAPI Sidecar Service & Persistent Job Queue (3 days)

- Implement FastAPI application under `training/server/app.py` binding to `127.0.0.1:8200`.
- Implement `.lemtrain_server/` state directory management:
  - SQLite persistent job queue in `.lemtrain_server/jobs.db` with WAL mode.
  - Local authentication token in `.lemtrain_server/token`.
  - Process PID file in `.lemtrain_server/server.pid`.
  - Job logs buffered to `.lemtrain_server/logs/<job_id>.log`.
- Implement real-time WebSocket log streaming at `/api/ws/jobs/{job_id}/logs` and `/api/ws/logs`.
- Implement REST route handlers under `training/server/routes/` (`health.py`, `config.py`, `jobs.py`, `models.py`, `training.py`, `datasets.py`, `env.py`, `gui.py`).
- Implement lifespan management with graceful shutdown and orphaned job recovery.

**Gate 12:** `lemtrain server start` starts sidecar on port 8200. Jobs survive server restart. WebSocket streams real-time training progress. Interactive OpenAPI docs accessible at `/docs`.

### Phase 13 — Canonical Presets & Desktop GUI Integration (1 day)

- Define canonical training presets in `presets.yaml` (`quick-sota`, `debug-tiny`, `walk-forward`, `restoration-ultra`, `detection-yolo`).
- Implement GUI aggregation endpoints in `training/server/routes/gui.py`:
  - `GET /api/gui/state`: Unified snapshot (host metrics, active jobs, model status, presets).
  - `GET /api/gui/models/with-stats`: Deep breakdown of model architectures, weights, SOTA metrics.
  - `POST /api/gui/quick-train`: Fast one-click training job dispatch via preset name and model key.
- Export frozen `openapi.json` contract for TypeScript client generation in `lemgendary-ai-studio-gui`.

**Gate 13:** OpenAPI contract validates without errors. All canonical presets execute cleanly via API.

### Phase 14 — Root Decluttering, Zero-Suppression Hardening & Final Validation (1 day)

- Remove residual `scratch/`, `__pycache__/`, and orphaned files.
- Verify `tools/` contains all auxiliary scripts with project root auto-discovery.
- Verify root contains exclusively canonical entrypoints (`cli.py`, `lemgendary_models_hub.ps1`), config manifests (`config.yaml`, `unified_models_v2.yaml`, `presets.yaml`), and subpackages.
- Update `README.md` to changelog format.
- Run complete compliance validation: `python -m env_manager.cli validate -p lemgendary-training-suite`.

**Gate 14:** `lem-env validate` passes with 0 errors and 0 warnings. 100% clean on Python compilation, zero-emoji check, zero-suppression check, YAML formatting, and JSON validation.

---

## 9. Verification Gates Summary

| Gate | Phase | Verification Scope | Gate Type | Blocking Prerequisite |
| --- | --- | --- | --- | --- |
| 0 | Baseline Freeze | Entrypoint smoke tests pass; binary blobs evicted | Smoke | Blocks Phase 1 |
| 1 | Utils & Secrets | `ForceTTY`, paths, secrets, delegates functional | Smoke | Blocks Phase 2 |
| 2 | Hardware | Discovery, VRAM probe, execution policy, sentinel | Functional | Blocks Phase 3 |
| 3 | Data | Manifold resolver unified; workers & loaders tested | Integration | Blocks Phase 4 |
| 4 | Container Readers | All 5 container readers pass round-trip fixtures | Round-Trip | Blocks Phase 5 |
| 5 | Checkpoint | Resume state & Kaggle BFS recovery tested | Parity | Blocks Phase 6 |
| 6 | Governance | `audit_epoch()` byte-identical on synthetic fixtures | **Behavioral Parity** | Blocks Phase 7 |
| 7 | Cloud | Bit-exact round-trip weights sync to Kaggle/GDrive | Round-Trip | Blocks Phase 8 |
| 8 | Export | Byte-identical ONNX/WebGPU/MT5 export artifacts | **Byte Parity** | Blocks Phase 9 |
| 9 | Notebook Cells | Cell generators structurally identical | Cross-Repo | Blocks Phase 10 |
| 10 | Engine | 3-epoch training trajectory matches baseline | **Metric Parity** | Blocks Phase 11 |
| 10.5 | DDP | Multi-process `torchrun` metric parity on T4x2 | **Metric Parity** | Non-blocking (Deferred) |
| 11 | Services & CLI | In-process services functional; `lemtrain` CLI passes | Functional | Blocks Phase 12 |
| 12 | Sidecar Server | Port 8200 active; SQLite jobs & WS logs verified | Integration | Blocks Phase 13 |
| 13 | Presets & GUI | OpenAPI contract exported; GUI endpoints validated | Contract | Blocks Phase 14 |
| 14 | Hardening | Zero-suppression & zero-emoji full validation | Zero-Diagnostic | Ready for Ecosystem |

---

## 10. Canonical Presets Specification

The suite introduces `presets.yaml`, defining canonical profiles for automated execution across CLI, API, and Desktop GUI:

```yaml
---
# LemGendary Model Training Suite Presets
# Canonical preset profiles for CLI, API, and Desktop GUI consumption.

version: "1.0"

presets:
  quick-sota:
    name: "quick-sota"
    title: "Quick SOTA (Aggressive Convergence Baseline)"
    description: "Mixed-precision training with cosine annealing, warm restarts, full curriculum progression, and active SOTA rollback gating."
    precision: "amp_fp16"
    batch_size: 64
    learning_rate: 0.001
    optimizer: "adamw"
    scheduler: "cosine_annealing_warm_restarts"
    epochs: 50
    curriculum_enabled: true
    sota_tracking: true
    vram_sentinel: true

  debug-tiny:
    name: "debug-tiny"
    title: "Debug Tiny (Instant Verification Run)"
    description: "Rapid 2-epoch run over a tiny 8-sample fixture batch for quick regression testing and pipeline debugging on CPU or single GPU."
    precision: "fp32"
    batch_size: 4
    learning_rate: 0.0001
    optimizer: "adam"
    scheduler: "constant"
    epochs: 2
    curriculum_enabled: false
    sota_tracking: false
    vram_sentinel: false

  walk-forward:
    name: "walk-forward"
    title: "Walk-Forward Financial (Forex Time-Series)"
    description: "Curriculum-driven walk-forward time-series training using ParquetRowGroupCache, RowGroupAwareSampler, and combined EMD + Rank losses."
    precision: "amp_fp16"
    batch_size: 512
    learning_rate: 0.0005
    optimizer: "adamw"
    scheduler: "plateau"
    epochs: 100
    curriculum_enabled: true
    sota_tracking: true
    vram_sentinel: true

  restoration-ultra:
    name: "restoration-ultra"
    title: "Restoration Ultra (High-Fidelity Vision Restoration)"
    description: "High-resolution tile curriculum for MIRNet, DeblurGAN, and super-resolution models with combined L1 + Perceptual loss and VRAM sentinel protection."
    precision: "amp_fp16"
    batch_size: 16
    learning_rate: 0.0002
    optimizer: "adamw"
    scheduler: "cosine"
    epochs: 80
    curriculum_enabled: true
    sota_tracking: true
    vram_sentinel: true

  detection-yolo:
    name: "detection-yolo"
    title: "Object Detection (YOLO Multi-Task Vision)"
    description: "Detection tuning with CIoU + DFL loss, dynamic letterboxing, and mosaic/mixup augmentations."
    precision: "amp_fp16"
    batch_size: 32
    learning_rate: 0.001
    optimizer: "sgd"
    scheduler: "linear"
    epochs: 100
    curriculum_enabled: false
    sota_tracking: true
    vram_sentinel: true
```

---

## 11. Risk Register

| Risk | Likelihood | Impact | Mitigation Strategy |
| --- | --- | --- | --- |
| Checkpoint resume logic diverges | Medium | High | Capture 10 pre-refactor resume fixtures; test exact parity against refactored `ResumeState`. |
| Governor transition behavior shifts | Medium | High | Snapshot 100 synthetic transitions from legacy `optimization_engine.py`; assert byte-parity. |
| Container readers degrade on Kaggle FUSE | Medium | Medium | Benchmark MDS and Parquet reads against FUSE mount; optimize chunk and buffer sizing. |
| DDP multi-process hangs on Kaggle T4x2 | Medium | Medium | Implement strict 5-minute NCCL watchdog; provide instant fallback to SingleGPU / DP. |
| Port collision on 8200 | Low | Low | Enforce ecosystem port taxonomy: Env Manager (8000), Datasets (8100), Training (8200). |
| Accidental reintroduction of silent exceptions | Medium | High | Enforce pre-commit validation hook via `lem-env validate`, failing on any bare `except:`. |

---

## 12. Success Metrics

| Metric | Baseline | Target (Phase 10) | Final Target (Phase 14) |
| --- | ---: | ---: | ---: |
| `core_loop.py` lines of code | 2,600 | ~50 | ~50 |
| `optimization_engine.py` lines | 900 | ~200 | ~200 |
| In-process typed services (`training/services/`) | 0 | 0 | 7 |
| Bare `except:` clauses | 34 | 0 | 0 |
| `warnings.filterwarnings('ignore')` suppressions | 5 | 0 | 0 |
| Swallowed `except Exception: pass` sites | 21 | 0 | 0 |
| Manifold resolver duplicate copies | 4 | 1 | 1 |
| Cloud synchronization modules | 5 (spaghetti) | 3 | 3 (protocol-unified) |
| Container formats readable | 2 (dir, parquet) | 5 | 5 |
| Presets available (`presets.yaml`) | 0 | 0 | 5 |
| API endpoints (FastAPI port 8200) | 0 | 0 | ~28 |
| Committed binary blobs in repository | 2 (`.pt`, `.task`) | 0 | 0 |
| Multi-gate compliance validation pass rate | Failing | Passing | 100% [PASS] |

---

## 13. Implementation Order

```text
Phase 0     ──┐  Freeze baseline & evict binary blobs
             │
Phase 1     ──┤  Core utilities, structured secrets & delegates
             │
Phase 2     ──┤  Hardware discovery, policy & VRAM sentinel
             │
Phase 3     ──┤  Data loaders, workers & manifold resolver
             │
Phase 4     ──┤  Modern container readers (MDS, LitData, WebDataset, Parquet, WebP)
             │
Phase 5     ──┤  Checkpoint management, recovery BFS & SOTA rollback
             │
Phase 6     ──┤  Governance, dynamic curriculum, thermal & metrics registry
             │
Phase 7     ──┤  Unified cloud management (GitHub, Kaggle Hub, Google Drive)
             │
Phase 8     ──┤  Model export subsystem (ONNX, Torch Standalone, WebGPU, MT5)
             │
Phase 9     ──┤  Modular notebook cell architecture
             │
Phase 10    ──┤  Training engine core coordinator (run_training)
             │
Phase 11    ──┤  In-process S.O.L.I.D. services layer & canonical CLI
             │
Phase 12    ──┤  FastAPI sidecar service & persistent job queue (Port 8200)
             │
Phase 13    ──┤  Canonical presets & Desktop GUI integration
             │
Phase 14    ──┤  Root decluttering, zero-suppression hardening & ecosystem validation
             │
Phase 10.5  ──┘  DistributedDataParallel (DDP) integration (deferred post-Phase 12)
```

Phases 0 through 14 execute sequentially. Phase 10.5 is scheduled following Phase 12 to safely validate distributed process orchestration on top of a fully tested sidecar and services foundation.

---

## 14. Completed Work (Already Landed)

The following architectural components are already completed and verified in the codebase:

1. **Strategy Pattern for Parallelism (`training/parallel/`)**: Full implementation across `base.py`, `single.py`, `dp.py`, `ddp.py`, `__init__.py`, and `__main__.py`. Model wrapping, state-dict prefix stripping (`.module.`), and rank-0 gating are fully realized.
2. **`ParquetRowGroupCache` (v2.3 in `data/forex_dataset.py`)**: Decode-at-fill caching converts raw row groups into per-row numpy records at cache-fill time, dropping per-row feature access from ~5 ms to ~3 µs.
3. **`RowGroupAwareSampler` (`data/forex_sampler.py`)**: Shuffles dataset batches at the row group level, increasing cache hit rate from ~2% to ~99% under random access.
4. **`DynamicOnTheFlyDegrader` (`data/dataset.py`)**: Real-time image degradation engine for on-the-fly vision model training augmentation.

---

## 15. Architectural Decisions & Resolved Questions

1. **Container Auto-Resolution**: The training suite dynamically resolves the active container format via `dataset_info.yaml:container.primary`. If a modern container (`mds`, `litdata`, `webdataset`, `parquet`) is present, it is selected; otherwise it seamlessly falls back to `directory`.
2. **Lossless WebP Image Decoding**: The `DirectoryReader` supports both legacy image formats (JPEG, PNG) and in-place transcoded lossless WebP images produced by the Dataset Compiler Suite v16.7.2, preserving all NTFS hardlinks.
3. **In-Process Services vs Subprocess Execution**: In alignment with S.O.L.I.D. principles, CLI commands and API endpoints invoke typed Python services (`training/services/`) directly in-process. Subprocess execution is reserved strictly for long-running asynchronous jobs managed by `training/server/jobs.py`.
4. **Notebook Generation Single Source of Truth**: Cell generator functions reside in `training/notebooks/cells/`, serving as the single source of truth for both training suite CLI commands and Dataset Compiler notebook generators.
5. **CPA Desktop GUI Topology**: The LemGendary AI Studio Desktop GUI connects as an external client over HTTP and WebSocket to the three independent sidecar services: `lemgendary-env-manager` (port 8000), `lemgendary-datasets` (port 8100), and `lemgendary-training-suite` (port 8200).

---

## 16. Parallel Strategy Layer Detail

The `training/parallel/` package provides a robust Strategy pattern for execution topologies:

- `SingleGPUStrategy`: Standard execution with zero wrapper overhead.
- `DataParallelStrategy`: Multi-GPU single-process execution with automated `.module.` prefix normalization.
- `DistributedDataParallelStrategy`: Multi-process distributed execution with synchronized state dictionaries.

### Checkpoint Portability

To guarantee that models trained under DataParallel or DDP can be seamlessly reloaded on single-GPU or CPU workstations without weight key errors, `state_dict_for_save()` strips the `.module.` prefix before saving, while `load_state_dict()` automatically inspects and normalizes checkpoints upon loading.

---

## 17. Container Reader Phase Detail (Phase 4)

### 17.1 Protocol Specification

The `ContainerReader` protocol guarantees uniform random access and iteration across diverse storage backends:

```python
class ContainerReader(Protocol):
    format_name: ClassVar[str]

    def open(self, manifold_root: Path) -> None:
        """Initialize backing readers, memory maps, or shard indices."""
        ...

    def __len__(self) -> int:
        """Return total accessible samples in the manifold."""
        ...

    def __iter__(self) -> Iterator[Sample]:
        """Iterate through samples in sequential order."""
        ...

    def get(self, idx: int) -> Sample:
        """Retrieve a specific sample by global index."""
        ...

    def close(self) -> None:
        """Release open file handles, memory maps, or network streams."""
        ...
```

### 17.2 Sample Unpacking

Each sample returned by `ContainerReader` unpacks raw image bytes, paired targets, masks, and metadata:

- `image_bytes`: Encoded bytes (JPEG, PNG, or WebP). Decoded via PIL or TurboJPEG to RGB tensor.
- `target_bytes`: Paired ground-truth image for restoration/super-resolution tasks.
- `mask_bytes`: Segmentation or inpainting mask bytes.
- `label`: Dictionary containing classification indices, bounding boxes, or financial features.
- `metadata`: Provenance dictionary parsed from compiler manifests.

---

## 18. Governance Phase Detail (Phase 6)

The legacy `optimization_engine.py` (900 lines) mixes metric parsing, curriculum transitions, thermal logit scaling, and SOTA model saves. Phase 6 partitions these into isolated state objects:

| Module | Class | Responsibility |
| --- | --- | --- |
| `metrics.py` | `MetricRegistry` | Metric directionality (`min` / `max`), weightings, and composite score calculation. |
| `curriculum.py` | `CurriculumState` | Resolution ladders, sample fraction scaling, phase transitions, and jolt triggers. |
| `thermal.py` | `ThermalState` | Softmax temperature scheduling, logit clamping floors, and entropy monitoring. |
| `sota.py` | `SotaTracker` | Historical SOTA score tracking, patience windows, drift detection, and rollback decisions. |
| `governor.py` | `SmartTrainingGovernor` | Thin coordinator uniting the state objects while preserving legacy public methods. |

All swallowed errors are replaced with typed `GovernorStateError(code, message)`.

---

## 19. Cloud Phase Detail (Phase 7)

Phase 7 consolidates five disparate cloud modules (`cloud_sync.py`, `checkpoint_sync.py`, `kaggle_cloud_manager.py`, `kaggle_monitor.py`, `sync_to_gdrive.py`) into a structured `training/cloud/` package:

- `manager.py`: Base `CloudManager` protocol and structured `CloudSyncError(code, message, retryable)`.
- `credentials.py`: Safe credential discovery and decryption.
- `git_hub.py`: Robust git synchronization replacing bare `except:` clauses with typed git error handlers.
- `kaggle_hub.py`: Unified Kaggle dataset, model, and kernel API interactions.
- `gdrive.py`: Google Drive backup and recovery synchronization.

---

## 20. Cross-Project Synchronization Matrix

| Sibling Capability | LemGendary Dataset Compiler Suite (v16.7.2-SOLID) | LemGendary Environment Manager (v2.0.0) | LemGendary Model Training Suite Target |
| --- | --- | --- | --- |
| **CLI Framework** | Typer + Rich (`lemgendary`) | Typer + Rich (`lem-env`) | Typer + Rich (`lemtrain`) via `cli.py` |
| **Sidecar Server** | FastAPI Port 8100 (`api/`) | FastAPI Port 8000 (`env_manager/`) | FastAPI Port 8200 (`training/server/`) |
| **Services Layer** | `services/*.py` (7 in-process services) | `env_manager/*.py` | `training/services/*.py` (7 in-process services) |
| **Job Persistence** | SQLite WAL (`.lgd_server/jobs.db`) | In-memory + process queue | SQLite WAL (`.lemtrain_server/jobs.db`) |
| **Log Streaming** | WebSocket `/ws/jobs/{id}/logs` | WebSocket `/ws/logs` | WebSocket `/api/ws/jobs/{id}/logs` & `/api/ws/logs` |
| **Presets Manifest** | `presets.yaml` (4 canonical presets) | Manifests in `requirements/` | `presets.yaml` (5 canonical presets) |
| **GUI Endpoints** | `/api/gui/state`, `/api/gui/quick-compile` | `/api/gui/state`, `/api/gui/ecosystem` | `/api/gui/state`, `/api/gui/quick-train` |
| **Code Validation** | Multi-gate clean, zero-suppression | Authoritative validation engine | Multi-gate clean, zero-suppression |
| **Taxonomy Standard** | Full branded names, zero abbreviations | Full branded names, zero abbreviations | Full branded names, zero abbreviations |
| **Zero Emojis** | 100% enforced | 100% enforced | 100% enforced |

---

## 21. Test Plan

### 21.1 Unit Tests

- `tests/unit/hardware/test_discovery.py`: Verify GPU/MPS/CPU detection logic.
- `tests/unit/hardware/test_sentinel.py`: Verify proactive VRAM OOM prevention and recovery.
- `tests/unit/governance/test_curriculum.py`: Verify resolution ladder and sample scaling.
- `tests/unit/governance/test_sota.py`: Verify SOTA rollback gating and patience counters.
- `tests/unit/parallel/test_strategy_resolution.py`: Verify automatic strategy selection.
- `tests/unit/parallel/test_checkpoint_normalization.py`: Verify state-dict key prefix stripping.
- `tests/unit/checkpoint/test_resume_scaling.py`: Verify iteration and epoch resume calculations.
- `tests/unit/data/test_parquet_cache.py`: Verify `ParquetRowGroupCache` v2.3 hit rates and feature decoding.
- `tests/unit/data/test_containers.py`: Verify `ContainerReader` implementations across all 5 formats.
- `tests/unit/services/test_training_service.py`: Verify in-process training service orchestration.

### 21.2 Integration Tests

- `tests/integration/test_one_epoch.py`: Run one full training epoch on synthetic fixtures.
- `tests/integration/test_strategy_swap.py`: Save checkpoint under DataParallel, resume under SingleGPU.
- `tests/integration/test_server_jobs.py`: Submit training job via FastAPI test client, stream WebSocket logs.
- `tests/integration/test_presets_dispatch.py`: Dispatch training run using canonical presets.

### 21.3 Behavioral Parity Tests

- `tests/parity/test_governor_parity.py`: Replay recorded epoch transitions through `SmartTrainingGovernor`.
- `tests/parity/test_export_parity.py`: Compare ONNX export outputs against baseline exports.

---

## 22. End of Roadmap

Execution begins with Phase 0 upon approval. The parallel strategy layer (`training/parallel/`) and Parquet cache v2.3 optimizations are already completed and will be integrated into the refactored engine during Phase 10.

All implementation tasks must strictly maintain zero emojis, zero warning/error suppressions, and 100% compliance with `python -m env_manager.cli validate -p lemgendary-training-suite`.
