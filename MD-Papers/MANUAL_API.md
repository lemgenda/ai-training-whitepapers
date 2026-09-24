# LemGendary Ecosystem: Master API Reference Manual

## Category 00 | LemGendary AI Documentation Hub

---

## Table of Contents

- [1. Executive Overview](#1-executive-overview)
- [2. Environment Manager REST API](#2-environment-manager-rest-api)
  - [2.1 Server Configuration & Startup](#21-server-configuration--startup)
  - [2.2 Interactive OpenAPI Documentation](#22-interactive-openapi-documentation)
  - [2.3 Health & System Discovery Endpoints](#23-health--system-discovery-endpoints)
  - [2.4 Projects & Ecosystem Audit Endpoints](#24-projects--ecosystem-audit-endpoints)
  - [2.5 Orchestration & Lifecycle Action Endpoints](#25-orchestration--lifecycle-action-endpoints)
  - [2.6 WebSocket Real-Time Telemetry](#26-websocket-real-time-telemetry)
  - [2.7 Desktop GUI Aggregation & Multi-Sidecar Ecosystem Endpoints](#27-desktop-gui-aggregation--multi-sidecar-ecosystem-endpoints)
- [3. Desktop GUI Tauri IPC API Contracts](#3-desktop-gui-tauri-ipc-api-contracts)
- [4. Training Suite Sidecar Daemon & Python Engine](#4-training-suite-sidecar-daemon--python-engine)
  - [4.1 Server Architecture & Startup](#41-server-architecture--startup)
  - [4.2 Security & Authentication](#42-security--authentication)
  - [4.3 Endpoint Reference Matrix](#43-endpoint-reference-matrix)
  - [4.4 WebSocket Real-Time Telemetry & Log Streaming](#44-websocket-real-time-telemetry--log-streaming)
  - [4.5 SQLite WAL Job Persistence & Crash Recovery](#45-sqlite-wal-job-persistence--crash-recovery)
  - [4.6 Desktop GUI Dashboard Aggregation Endpoints](#46-desktop-gui-dashboard-aggregation-endpoints)
  - [4.7 Python In-Process Engine & Governance API](#47-python-in-process-engine--governance-api)
- [5. Datasets Compilation & Stream Pipeline API](#5-datasets-compilation--stream-pipeline-api)
  - [5.1 Server Architecture & Discovery](#51-server-architecture--discovery)
  - [5.2 Security & Authentication](#52-security--authentication)
  - [5.3 Endpoint Reference Matrix](#53-endpoint-reference-matrix)
  - [5.4 WebSocket Real-Time Log Streaming](#54-websocket-real-time-log-streaming)
  - [5.5 SQLite Job Persistence & Restart Recovery](#55-sqlite-job-persistence--restart-recovery)
  - [5.6 Desktop GUI Aggregated Endpoints & Presets (Phase 8)](#56-desktop-gui-aggregated-endpoints--presets-phase-8)
- [6. Error Handling, Status Codes & Resilience](#6-error-handling-status-codes--resilience)

---

## 1. Executive Overview

The LemGendary Ecosystem exposes clean, typed, deterministic API surfaces for machine-to-machine integration,
desktop UI orchestration, and automated pipeline execution.
Central to the ecosystem is the authoritative FastAPI daemon running in `lemgendary-env-manager`, providing both
high-throughput HTTP REST endpoints and bidirectional WebSocket streams.

All REST endpoints follow standard HTTP semantics, return strict JSON payloads conforming to Pydantic models,
and maintain zero extraneous metadata.

---

## 2. Environment Manager REST API

The Environment Manager server runs locally or inside CI environments to expose hardware discovery, ecosystem audits,
package synchronization, and multi-gate validations over HTTP.

### 2.1 Server Configuration & Startup

The server is launched via the `lem-env` command or PowerShell management console:

```bash
# Default binding: http://127.0.0.1:8000
lem-env serve --host 127.0.0.1 --port 8000
```

| Configuration Parameter | Default Value | CLI Flag | Description |
| :--- | :--- | :--- | :--- |
| Host Interface | `127.0.0.1` | `--host` | Network IP address to bind HTTP and WebSocket listener |
| TCP Port | `8000` | `--port` | Local listening port for incoming requests |

The server's lifecycle is managed via FastAPI's `@asynccontextmanager` lifespan handler. A background asyncio task drains the WebSocket event queue for the lifetime of the server and is cancelled cleanly on shutdown.

---

### 2.2 Interactive OpenAPI Documentation

When the server is active, auto-generated interactive OpenAPI specifications are served at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc UI: `http://127.0.0.1:8000/redoc`
- Raw OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

---

### 2.3 Health & System Discovery Endpoints

#### `GET /api/health`

Returns the complete ecosystem health audit. This is the largest response body in the API, containing bootstrap status, hardware profile, project environments, version drift entries, manifest coverage, single-manifest inventory, and npm status.

Query parameters:

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `include_safety` | Boolean | `false` | When true, runs per-project pip safety dry-runs to classify each outdated package as safe-↑ or blocked-⊘. Adds 15–40 seconds of latency per Python project. |

Response structure (top-level keys):

```json
{
  "bootstrap": { "python_valid": true, "python_version": "3.12.10" },
  "hardware": { "os_name": "Windows", "primary_backend": "cuda" },
  "projects": [
    {
      "name": "lemgendary-datasets",
      "venv_exists": true,
      "total_required": 36,
      "total_installed": 105,
      "missing_packages": [],
      "is_healthy": true
    }
  ],
  "version_drift": [
    {
      "package_name": "numpy",
      "versions": { "lemgendary-datasets": "2.5.3", "lemgendary-training-suite": "2.5.3" },
      "pins": { "lemgendary-datasets": { "pin_type": "range", "specifier": ">=2.2.6,<2.6" } },
      "upgrades": { "lemgendary-datasets": { "current": "2.5.3", "latest": null, "safe": false } },
      "has_drift": false,
      "has_pin_mismatch": false,
      "projects_declared": 2
    }
  ],
  "manifest_coverage": [
    {
      "project_name": "lemgendary-datasets",
      "declared_count": 36,
      "installed_count": 105,
      "missing": [],
      "extra": ["setuptools"],
      "platform_skipped": []
    }
  ],
  "single_manifest_packages": [
    {
      "package_name": "mediapipe",
      "project": "lemgendary-datasets",
      "installed_version": "1.0.1",
      "pin_type": "exact",
      "specifier": "==1.0.1"
    }
  ],
  "npm_packages": [],
  "npm_drift": [],
  "overall_healthy": true
}
```

#### `GET /api/drift`

Compact alternative to `/api/health` that returns only the drift-related data. Useful for GUI dashboards that only need the matrix view.

Query parameters:

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `include_safety` | Boolean | `false` | Same semantics as `/api/health?include_safety`. |

Response structure:

```json
{
  "python": [],
  "coverage": [],
  "single_manifest": [],
  "npm": [],
  "include_safety": false
}
```

`python` entries are drift rows (packages declared in two or more manifests). `coverage` entries reconcile each manifest's declared set against its installed set. `single_manifest` lists packages declared in exactly one manifest. `npm` entries track version drift across npm workspaces.

#### `GET /api/hardware`

Returns the parsed hardware and accelerator profile: OS, CPU topology, RAM, GPU devices, primary backend, recommended PyTorch index, and MetaTrader 5 info.

Example response:

```json
{
  "os_name": "Windows",
  "os_release": "11",
  "architecture": "AMD64",
  "cpu_count_logical": 16,
  "cpu_count_physical": 8,
  "total_ram_mb": 32768,
  "primary_backend": "cuda",
  "recommended_torch_index": "https://download.pytorch.org/whl/cu121",
  "accelerators": [
    {
      "name": "NVIDIA GeForce GTX 1650",
      "backend": "cuda",
      "total_memory_mb": 4096,
      "index": 0,
      "driver_version": "552.22"
    }
  ],
  "metatrader5": {
    "installed": true,
    "version": "5.0.0.6182",
    "install_path": "C:\\Program Files\\MetaTrader 5"
  }
}
```

The `metatrader5.version` field is populated from `terminal64.exe`'s `FileVersion` metadata via PowerShell's `VersionInfo` property. This is authoritative even when winget has no record of the MT5 installation.

#### `GET /api/projects`

Enumerates all discovered ecosystem repositories with their virtual environment status, installed package count, and health indicators.

```json
[
  {
    "name": "lemgendary-env-manager",
    "project_dir": "C:\\Development\\python\\model-training\\lemgendary-env-manager",
    "venv_dir": "C:\\Development\\python\\model-training\\lemgendary-env-manager\\.venv",
    "python_path": "C:\\Development\\python\\model-training\\lemgendary-env-manager\\.venv\\Scripts\\python.exe",
    "is_valid": true,
    "python_version": "Python 3.12.10",
    "installed_packages_count": 45,
    "is_node_project": false,
    "node_modules_present": false
  }
]
```

#### `GET /api/npm`

Returns Node.js workspace status and the npm package dependency matrix for every workspace containing `package.json`.

---

### 2.4 Projects & Ecosystem Audit Endpoints

#### `GET /api/pipeline/status`

Returns the execution state of the background pipeline orchestrator together with the last 50 telemetry events.

```json
{
  "is_running": false,
  "last_status": "success",
  "last_run_timestamp": "2026-09-15T00:15:00Z",
  "recent_events": []
}
```

#### `GET /api/manifests`

Lists every centralized requirements manifest with its raw contents.

```json
{
  "manifests": {
    "requirements-datasets.txt": "--extra-index-url https://download.pytorch.org/whl/cu121",
    "requirements-training.txt": "--extra-index-url https://download.pytorch.org/whl/cu121",
    "requirements-env-manager.txt": "typer==0.27.2\nrich==15.0.0"
  }
}
```

---

### 2.5 Orchestration & Lifecycle Action Endpoints

#### `POST /api/pipeline/run`

Triggers the Smart Clean Install Pipeline asynchronously. Telemetry events stream across WebSocket connections.

Request body:

```json
{
  "target_project": null
}
```

Response:

```json
{
  "status": "accepted",
  "message": "Pipeline initiated."
}
```

If a pipeline is already running, returns:

```json
{
  "status": "error",
  "message": "Pipeline is already running."
}
```

#### `POST /api/update`

Triggers safe bottom-up package upgrades across all projects and auto-syncs manifests.

Request body:

```json
{
  "project": null,
  "dry_run": false
}
```

When `dry_run=true`, returns the plan without applying:

```json
{
  "status": "dry_run",
  "plan": {
    "total_outdated": 34,
    "total_safe": 24,
    "total_blocked": 10,
    "cuda_detected": true,
    "cuda_index_url": "https://download.pytorch.org/whl/cu121",
    "projects": []
  }
}
```

When `dry_run=false`, applies the plan and returns the collected events:

```json
{
  "status": "success",
  "events": [
    {
      "project": "lemgendary-datasets",
      "package": "pandas-ta-classic",
      "old_version": "0.6.52",
      "new_version": "0.8.32",
      "status": "upgraded",
      "message": "Upgraded 0.6.52 -> 0.8.32."
    }
  ]
}
```

Event status values:

- `upgraded`: package was successfully upgraded.
- `blocked`: upgrade blocked by reverse dependency; `message` contains the reason.
- `verified`: environment verified as healthy without a version change (`pip check`, `torch-cuda-verify`, or torch-family no-op).
- `failed`: batch or rollback failure.
- `skipped`: nothing to do.

#### `POST /api/validate`

Executes the multi-gate validation suite across all projects or a single project.

Request body:

```json
{
  "project": null
}
```

Response:

```json
{
  "status": "success",
  "all_passed": true,
  "projects": {
    "lemgendary-datasets": {
      "project_name": "lemgendary-datasets",
      "compiled_files_count": 24,
      "compile_errors": [],
      "emoji_violations": [],
      "yaml_errors": [],
      "json_errors": [],
      "lint_errors": [],
      "html_errors": [],
      "wcag_violations": [],
      "domain_errors": [],
      "passed": true
    }
  }
}
```

#### `POST /api/manifests/sync`

One-way copy of centralized manifests to project directories. Returns per-project sync status.

```json
{
  "status": "success",
  "results": {
    "lemgendary-training-suite": {
      "success": true,
      "message": "Synchronized sanitized requirements-training.txt to C:\\Development\\python\\model-training\\lemgendary-training-suite\\requirements.txt."
    },
    "lemgendary-datasets": {
      "success": true,
      "message": "Synchronized sanitized requirements-datasets.txt to C:\\Development\\python\\model-training\\lemgendary-datasets\\requirements.txt."
    }
  }
}
```

#### `POST /api/clean`

Purges orphaned bytecode caches and temporary build artifacts.

Request body:

```json
{
  "project": null
}
```

Response:

```json
{
  "status": "success",
  "cleaned_count": 42,
  "reclaimed_bytes": 1258291,
  "reclaimed_mb": 1.2
}
```

---

### 2.6 WebSocket Real-Time Telemetry

Real-time logging, telemetry, and pipeline progression are streamed to connected clients over a persistent WebSocket connection:

```bash
ws://127.0.0.1:8000/ws/log
ws://127.0.0.1:8000/ws/logs
```

Both paths are aliases for the same handler. On connect, the client receives the last 20 buffered events, then continues to receive new events as they are emitted by the pipeline.

Telemetry Event Schema (`PipelineEvent`):

```json
{
  "timestamp": "2026-09-15T00:15:02.123456Z",
  "step_number": 3,
  "total_steps": 7,
  "step_name": "Virtual Environments",
  "status": "info",
  "message": "Creating fresh virtual environment for lemgendary-datasets...",
  "data": {
    "project": "lemgendary-datasets",
    "venv_path": "C:\\Development\\python\\model-training\\lemgendary-datasets\\.venv"
  }
}
```

Event Status Values:

- `info`: Informational milestone during pipeline processing.
- `success`: Step completed cleanly without warnings.
- `warning`: Step completed with non-fatal advisory notice.
- `error`: Fatal error encountered in step execution.

Thread-safe dispatch is guaranteed via `asyncio.run_coroutine_threadsafe()`, which allows the background pipeline thread to broadcast events on the server's running event loop without blocking.

---

### 2.7 Desktop GUI Aggregation & Multi-Sidecar Ecosystem Endpoints

The Environment Manager provides specialized endpoints for high-velocity hydration in `lemgendary-ai-studio-gui`:

#### `GET /api/gui/state`

Returns a consolidated snapshot containing service identity, hardware profile (`probe_hardware()`), discovered projects summary (`discover_projects()`), and pipeline execution status (`orchestrator.is_running`) in a single non-blocking payload.

Example response:

```json
{
  "service": {
    "name": "lemgendary-env-manager",
    "version": "2.0.0",
    "port": 8000,
    "status": "online"
  },
  "hardware": {
    "os_name": "Windows",
    "primary_backend": "cuda"
  },
  "projects": [],
  "pipeline": {
    "is_running": false,
    "last_status": "success",
    "last_run_timestamp": "2026-09-17T20:00:00Z"
  }
}
```

#### `GET /api/gui/ecosystem`

Monitors health and connectivity across local ecosystem sidecars by actively probing `http://127.0.0.1:8100/api/health` with a non-blocking timeout. Powers the desktop GUI top-bar status indicator:

```json
{
  "env_manager": {
    "service": "lemgendary-env-manager",
    "port": 8000,
    "status": "online",
    "reachable": true
  },
  "dataset_compiler": {
    "service": "lemgendary-datasets",
    "port": 8100,
    "status": "online",
    "reachable": true,
    "data": {
      "status": "ok",
      "service": "LemGendary Dataset Compiler API"
    }
  }
}
```

---

## 3. Desktop GUI Tauri IPC API Contracts

The desktop frontend `lemgendary-ai-studio-gui` communicates with the native Rust backend via Tauri v2 IPC invocations.

| IPC Command | Arguments | Return Type | Purpose |
| :--- | :--- | :--- | :--- |
| `run_system_probe` | None | `SystemProbeResult` | Triggers hardware discovery from native desktop thread |
| `get_ecosystem_status` | None | `EcosystemReport` | Queries active environment manager daemon for health metrics |
| `trigger_clean_install` | `project: Option<String>` | `PipelineLaunchResult` | Starts environment provisioning pipeline |
| `execute_validation` | `project: Option<String>` | `ValidationResult` | Runs multi-gate verification suite |
| `connect_telemetry_stream` | None | `WebSocketHandle` | Subscribes frontend to `/ws/log` channel |

---

## 4. Training Suite Sidecar Daemon & Python Engine

The `lemgendary-training-suite` repository provides both a background FastAPI sidecar service on `127.0.0.1:8200` and high-performance Python engine classes for in-process training, SOTA validation, and WebGPU optimization.

### 4.1 Server Architecture & Startup

The sidecar service daemon coordinates background training pipelines, asynchronous job execution, real-time log streaming, and model compilation. It is launched via the `lemtrain` CLI:

```bash
# Launch server daemon as a background service on port 8200
python cli.py server start --daemon --host 127.0.0.1 --port 8200

# Inspect server status, port, and PID
python cli.py server status

# Export OpenAPI 3.1 schema specification
python cli.py server openapi --output openapi.json

# Gracefully terminate daemon
python cli.py server stop
```

| Parameter | Default | Description |
| :--- | :--- | :--- |
| Bind Host | `127.0.0.1` | Local loopback interface |
| Bind Port | `8200` | Dedicated training suite sidecar port |
| Interactive Docs | `/docs` | OpenAPI Swagger UI |
| Schema Spec | `/openapi.json` | OpenAPI 3.1.0 JSON specification |

### 4.2 Security & Authentication

Operational endpoints under `/api` requiring modification or system access enforce token authentication:

- Provide the token via HTTP header `X-LemTrain-Token: <token>` or `Authorization: Bearer <token>`.
- Token resolution: checked from the `LEMTRAIN_API_TOKEN` environment variable, or read from `.lemtrain_server/token`.
- Unauthenticated requests to protected endpoints return `401 Unauthorized`. Diagnostic endpoints (`/api/health`, `/docs`, `/openapi.json`, `/redoc`) and WebSocket streams (`/api/ws/*`) are open for non-blocking monitoring.

### 4.3 Endpoint Reference Matrix

| Method | Endpoint | Auth | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | None | Basic liveness, uptime, accelerator device, and version 16.2.9 |
| `GET` | `/api/config` | Required | Active configuration parameters and loaded training configurations |
| `GET` | `/api/presets` | Required | Canonical training presets list and hyperparameter definitions |
| `GET` | `/api/presets/{name}` | Required | Detailed hyperparameter parameters for a specific preset |
| `GET` | `/api/jobs` | Required | List background jobs with pagination and status filtering |
| `POST` | `/api/jobs` | Required | Submit asynchronous background job (train, eval, export, audit, sync) |
| `GET` | `/api/jobs/{id}` | Required | Query job state, progress metrics, exit code, and timestamps |
| `GET` | `/api/jobs/{id}/logs` | Required | Retrieve execution log text slice or tail lines for a job |
| `POST` | `/api/jobs/{id}/cancel` | Required | Gracefully cancel a running background job |
| `GET` | `/api/models` | Required | Enumerate registered neural architectures and target domains |
| `GET` | `/api/models/{name}` | Required | Retrieve model specifications and default hyperparameters |
| `GET` | `/api/models/{name}/audit` | Required | Detailed model audit: parameter counts, layer topology, memory |
| `POST` | `/api/training/train` | Required | In-process training initiation with hardware discovery |
| `POST` | `/api/training/evaluate` | Required | In-process checkpoint evaluation under torch.no_grad() |
| `POST` | `/api/training/export` | Required | In-process multi-format model compilation and export |
| `GET` | `/api/datasets` | Required | Discover available compiled datasets and dataset manifolds |
| `GET` | `/api/env/telemetry` | Required | System hardware telemetry: CPU, RAM, GPU, VRAM headroom, disk |
| `GET` | `/api/gui/state` | Required | Consolidated GUI snapshot: daemon, hardware, active jobs, models |
| `GET` | `/api/gui/models/with-stats` | Required | Model cards hydrated with checkpoint and export disk stats |
| `POST` | `/api/gui/quick-train` | Required | High-velocity one-click preset training dispatch |

### 4.4 WebSocket Real-Time Telemetry & Log Streaming

Persistent WebSocket streams provide low-latency log and telemetry feeds for connected user interfaces:

- `ws://127.0.0.1:8200/api/ws/jobs/{id}/logs` — Streams real-time line-buffered log output for an active background job.
- `ws://127.0.0.1:8200/api/ws/logs` — Global server execution and orchestration log stream.

### 4.5 SQLite WAL Job Persistence & Crash Recovery

All asynchronous jobs are persisted in `.lemtrain_server/jobs.db` using SQLite Write-Ahead Logging (WAL) mode:

- Immediate ACID recording of job metadata, parameters, start time, and state transitions (`queued`, `running`, `completed`, `failed`, `cancelled`).
- Crash recovery: when the sidecar daemon restarts, any jobs found in `running` or `queued` state from an ungraceful host shutdown are automatically transitioned to `failed` with diagnostic recovery logs.

### 4.6 Desktop GUI Dashboard Aggregation Endpoints

To eliminate waterfall roundtrips from `lemgendary-ai-studio-gui`, specialized aggregation endpoints hydrate desktop views in a single HTTP transaction:

- `GET /api/gui/state`: Returns system health, GPU hardware metrics, active job count, recent jobs, and model catalog in one payload.
- `GET /api/gui/models/with-stats`: Enriches each registered model with discovered `.pth` checkpoints, file sizes, timestamps, and compiled ONNX export artifacts.
- `POST /api/gui/quick-train`: Accepts `{ "model_name": "mirnet_exposure", "preset": "quick-sota" }` and queues a training pipeline instantly with validated defaults.

### 4.7 Python In-Process Engine & Governance API

The training suite provides foundational Python engine classes for standalone execution and notebook integration:

```python
from training.core.orchestrator import TrainingOrchestrator
from training.governance.sentinel import SentinelGuard
from training.governance.governor import DynamicGovernor
from training.models.registry import ModelRegistry

# Discover registered architectures
registry = ModelRegistry()
model_meta = registry.get_model("mirnet_exposure")

# Initialize safety sentinel guard
sentinel = SentinelGuard(target_device="cuda:0", min_headroom_mb=1024)

# Create training orchestrator with dynamic loss governor
orchestrator = TrainingOrchestrator(
    model_name="mirnet_exposure",
    sentinel=sentinel,
    governor=DynamicGovernor(initial_lr=1e-4, min_lr=1e-6),
)
```

---

## 5. Datasets Compilation & Stream Pipeline API

The `lemgendary-datasets` repository provides a high-throughput sidecar API service running on `127.0.0.1:8100` (`api/`). It provides REST endpoints for hardware inspection, configuration validation, dataset and raw-source querying, and background execution of compilation and degradation tasks, with bidirectional WebSocket streaming for live logs and global telemetry.

### 5.1 Server Architecture & Discovery

```bash
# Launch server daemon
python cli.py server start --background --host 127.0.0.1 --port 8100

# Probe status and hardware sensors
python cli.py server status

# Terminate server daemon
python cli.py server stop
```

| Parameter | Default | Description |
| :--- | :--- | :--- |
| Bind Host | `127.0.0.1` | Local loopback interface |
| Bind Port | `8100` | Dedicated compiler service port (distinct from `lem-env` on 8000) |
| Interactive Docs | `/docs` | OpenAPI Swagger UI |
| Schema Spec | `/openapi.json` | OpenAPI 3.1.0 JSON specification |

### 5.2 Security & Authentication

All operational endpoints under `/api` requiring modification privileges enforce token authentication:

- Provide the token via HTTP header `X-API-Key: <token>` or `Authorization: Bearer <token>`.
- Master token resolution: checked from `LEMGENDARY_API_TOKEN` environment variable, or automatically loaded/generated in `.lgd_server/token`.
- Unauthenticated requests to protected endpoints return `401 Unauthorized`; invalid tokens return `403 Forbidden`. Diagnostic endpoints (`/api/health`, `/api/datasets`, `/api/sources`, `/api/gates`) and WebSocket streams are open.

### 5.3 Endpoint Reference Matrix

| Method | Endpoint | Auth | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | None | Basic liveness check, uptime, version, and active job count |
| `GET` | `/api/health/full` | None | Detailed telemetry: CPU cores, RAM, PyTorch CUDA detection, GPU model |
| `GET` | `/api/config` | Required | Retrieves parsed `unified_data.yaml` structure |
| `POST` | `/api/config/validate` | Required | Validates configuration against Pydantic schema |
| `GET` | `/api/jobs` | Required | List historical and active jobs with pagination (`limit`, `offset`, `state`, `job_type`) |
| `GET` | `/api/jobs/{id}` | Required | Fetch state, timestamps, exit code, and error details for a single job |
| `GET` | `/api/jobs/{id}/logs` | Required | Retrieve buffered execution log text or tail lines |
| `POST` | `/api/jobs/compile` | Required | Queue a manifold compilation task |
| `POST` | `/api/jobs/degrade` | Required | Queue a synthetic degradation derivation task |
| `POST` | `/api/jobs/{id}/cancel` | Required | Terminate an active job subprocess |
| `GET` | `/api/datasets` | None | Catalog compiled manifolds with size, sample counts, and container formats |
| `GET` | `/api/datasets/{name}` | None | Retrieve `dataset_info.yaml` and class lists for a specific manifold |
| `GET` | `/api/sources` | None | Catalog local `raw-sets` and configured upstream datasets |
| `GET` | `/api/kaggle/status` | None | Check Kaggle credentials (`.kaggle_token`, `~/.kaggle/kaggle.json`, env) |
| `POST` | `/api/kaggle/sync` | Required | Queue a Kaggle push/pull metadata synchronization job |
| `GET` | `/api/gates/hardlinks` | None | Audit NTFS/POSIX hardlink fractions and evaluate container safety |
| `GET` | `/api/gui/state` | None | Unified snapshot: uptime, active jobs, storage capacity, hardware profile, presets |
| `GET` | `/api/gui/datasets/with-stats` | None | Detailed manifold catalog: file distribution by format (WebP/JPEG/PNG/Parquet), storage bytes, hardlink metrics |
| `GET` | `/api/gui/jobs/active` | None | Real-time execution telemetry for active compiler background tasks |
| `GET` | `/api/gui/presets` | None | Canonical compiler preset parameter definitions and descriptions |
| `POST` | `/api/gui/quick-compile` | Required | Fast-dispatch compilation using a predefined compiler preset profile |
| `GET` | `/api/env/status` | Required | Passthrough delegating to `lem-env audit --fast` |
| `POST` | `/api/env/validate` | Required | Passthrough delegating to `lem-env validate --project lemgendary-datasets` |

### 5.4 WebSocket Real-Time Log Streaming

Clients connect to real-time log channels to monitor long-running compiler and degradation tasks without polling:

```text
ws://127.0.0.1:8100/api/ws/jobs/{job_id}/logs
```

On connection, the server automatically replays any existing backlog text buffered on disk, then streams incremental stdout/stderr chunks in real time as emitted by the subprocess.

Message Payload Format:

```json
{
  "job_id": "735bfe51-007d-4405-adf0-53ff34985668",
  "type": "log",
  "chunk": "[DEGRADE] Processing sample 1500/50000 (3.0%)...\n"
}
```

When execution concludes, a terminal chunk `[PROCESS_TERMINATED] Job <id> COMPLETED (Exit Code: 0)` is emitted before socket closing.

### 5.5 SQLite Job Persistence & Restart Recovery

All job states, parameters, created/started/completed timestamps, exit codes, and log paths are recorded in `.lgd_server/jobs.db` via SQLite.
If the API server or host reboots while jobs are in `running` or `pending` state, an automated recovery pass on boot transitions orphaned jobs to `interrupted`, preventing zombie job tracking and providing clean diagnostic records.

### 5.6 Desktop GUI Aggregated Endpoints & Presets (Phase 8)

The Dataset Compiler API exposes specialized endpoints tailored for `lemgendary-ai-studio-gui` desktop integration and Cross-Project Automation (CPA):

#### `GET /api/gui/state`

Aggregates system uptime, active jobs count, discovered manifold count, storage metrics, hardware sensors, and available compiler presets into a single rapid hydration payload.

#### `GET /api/gui/datasets/with-stats`

Returns comprehensive manifold storage and format statistics, including file distribution counts across formats (`webp`, `jpg`, `png`, `parquet`), total byte footprint, and physical NTFS hardlink deduplication ratios.

#### `GET /api/gui/jobs/active`

Streams execution progress telemetry for currently running compilation and degradation tasks, including percentage complete, current sample index, elapsed duration, and processing frames-per-second (`fps`).

#### `GET /api/gui/presets`

Catalogs canonical compiler preset profiles (`quality-vision`, `restoration-hardlinked`, `detection-variable`, `cloud-archival`) loaded from `presets.yaml`. Each entry documents target image formats, quality floors, NIMA vetting thresholds, YOLO auto-labeling flags, and container targets.

#### `POST /api/gui/quick-compile`

Fast-dispatch compilation endpoint accepting a preset profile name, target model key, and optional worker/storage overrides. Requires authentication token.

---

## 6. Error Handling, Status Codes & Resilience

All ecosystem APIs implement strict error resilience:

| HTTP Status | Code String | Description |
| :--- | :--- | :--- |
| `200 OK` | `SUCCESS` | Request processed successfully |
| `400 Bad Request` | `VALIDATION_ERROR` | Request body or query parameters failed schema validation |
| `404 Not Found` | `PROJECT_NOT_FOUND` | Specified target repository does not exist in workspace |
| `409 Conflict` | `PIPELINE_ACTIVE` | An install or update pipeline is currently executing |
| `500 Server Error` | `INTERNAL_FAILURE` | Unhandled internal exception occurred during toolchain execution |

Error Response Format:

```json
{
  "detail": "Project 'unknown-suite' was not found in ecosystem registry",
  "error_code": "PROJECT_NOT_FOUND",
  "timestamp": "2026-09-15T00:00:00Z"
}
```

Additional resilience features:

- **Automatic cache recovery**: `run_pip_with_recovery` detects corruption signatures in pip's output (`access violation`, hash mismatch, truncated download) and purges the HTTP cache before retrying once with `--no-cache-dir`.
- **Reverse-dependency safety**: No upgrade is applied if it would violate an installed package's requirement. The blocked reason is returned in the event stream.
- **Snapshot rollback**: Every package batch is snapshotted via `pip freeze` before apply. If `pip check` fails afterward, the batch is rolled back automatically.
- **Graceful WebSocket shutdown**: The event drain task is cancelled cleanly by the FastAPI lifespan handler on server shutdown, so no `Task was destroyed but it is pending!` warnings appear in the log.

---

## Companion Documentation

- [Technical Whitepaper (Markdown)](PAPER_ENV_MANAGER.md)
- [Technical Whitepaper (HTML)](env_manager.html)
- [Master CLI Operations Manual (Markdown)](MANUAL_CLI.md)
- [Master CLI Operations Manual (HTML)](cli-manual.html)
