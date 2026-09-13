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
  - [2.6 WebSocket Real-Time Telemetry (`/ws/events`)](#26-websocket-real-time-telemetry-wsevents)
- [3. Desktop GUI Tauri IPC API Contracts](#3-desktop-gui-tauri-ipc-api-contracts)
- [4. Training Suite Python API Engine](#4-training-suite-python-api-engine)
- [5. Datasets Compilation & Stream Pipeline API](#5-datasets-compilation--stream-pipeline-api)
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
# Default binding: http://127.0.0.1:8765
lem-env serve --host 127.0.0.1 --port 8765
```

| Configuration Parameter | Default Value | CLI Flag | Description |
| :--- | :--- | :--- | :--- |
| Host Interface | `127.0.0.1` | `--host` | Network IP address to bind HTTP and WebSocket listener |
| TCP Port | `8765` | `--port` | Local listening port for incoming requests |
| Hot Reload | `False` | `--reload` | Auto-reloads server when Python source files change |

---

### 2.2 Interactive OpenAPI Documentation

When the server is active, auto-generated interactive OpenAPI specifications are served at:

- Swagger UI: `http://127.0.0.1:8765/docs`
- ReDoc UI: `http://127.0.0.1:8765/redoc`
- Raw OpenAPI JSON: `http://127.0.0.1:8765/openapi.json`

---

### 2.3 Health & System Discovery Endpoints

#### `GET /`

Returns service identifier, ecosystem version, and operational status.

Response:

```json
{
  "service": "lemgendary-env-manager",
  "version": "2.1.0",
  "status": "online"
}
```

#### `GET /api/v1/health`

Lightweight liveness probe for monitoring tools and orchestrators.

Response:

```json
{
  "status": "healthy",
  "python_version": "3.11.9",
  "timestamp": "2026-09-13T00:00:00Z"
}
```

#### `GET /api/v1/probe`

Performs comprehensive hardware, OS, and GPU accelerator discovery.

Response:

```json
{
  "os_name": "Windows",
  "os_release": "11",
  "architecture": "AMD64",
  "cpu_count_logical": 32,
  "cpu_count_physical": 16,
  "total_ram_mb": 65536,
  "primary_backend": "cuda",
  "recommended_torch_index": "https://download.pytorch.org/whl/cu121",
  "accelerators": [
    {
      "name": "NVIDIA GeForce RTX 4090",
      "backend": "cuda",
      "total_memory_mb": 24576,
      "index": 0,
      "driver_version": "552.22"
    }
  ],
  "metatrader5": {
    "installed": true,
    "version": "5.0.38",
    "install_path": "C:\\Program Files\\MetaTrader 5"
  }
}
```

#### `GET /api/v1/hardware`

Returns the cached accelerator profile without re-probing external devices.

---

### 2.4 Projects & Ecosystem Audit Endpoints

#### `GET /api/v1/projects`

Enumerates all seven discovered ecosystem repositories, their paths, virtual environment status, and health indicators.

Response:

```json
[
  {
    "name": "lemgendary-env-manager",
    "path": "C:\\Development\\python\\model-training\\lemgendary-env-manager",
    "venv_exists": true,
    "is_healthy": true,
    "total_installed": 38,
    "missing_packages": []
  }
]
```

#### `GET /api/v1/projects/{project_name}`

Returns in-depth health, dependency status, and package manifest details for a single target project.

#### `GET /api/v1/audit`

Executes an exhaustive ecosystem audit, returning prerequisites, all project environments, NPM package matrices, and version drift data.

#### `GET /api/v1/npm`

Returns the complete Node.js workspace status and NPM Package Dependency Matrix inspecting declared versus installed package versions.

#### `GET /api/v1/drift`

Returns the cross-project package version drift matrix.

---

### 2.5 Orchestration & Lifecycle Action Endpoints

#### `POST /api/v1/install`

Triggers the Smart Clean Install Pipeline asynchronously. Telemetry events stream across WebSocket connections.

Request Body:

```json
{
  "target_project": null,
  "clean": true
}
```

Response:

```json
{
  "status": "started",
  "message": "Smart Clean Install Pipeline launched",
  "target_project": null,
  "clean": true
}
```

#### `GET /api/v1/pipeline/status`

Returns the execution state of the background pipeline orchestrator.

Response:

```json
{
  "is_running": false,
  "last_status": "idle",
  "current_step": 7,
  "total_steps": 7,
  "last_run_timestamp": "2026-09-13T00:15:00Z"
}
```

#### `POST /api/v1/upgrade-plan`

Analyzes outdated packages and constructs a safe bottom-up upgrade plan.

#### `POST /api/v1/apply-upgrade`

Applies proposed package upgrades and regenerates requirement manifests.

#### `POST /api/v1/sync`

Synchronizes active virtual environment package states into pinned requirements manifests.

#### `POST /api/v1/validate`

Executes the multi-gate validation engine across one or all projects.

Request Body:

```json
{
  "project_name": "lemgendary-docs"
}
```

Response:

```json
{
  "project_name": "lemgendary-docs",
  "passed": true,
  "total_violations": 0,
  "compile_errors": [],
  "emoji_violations": [],
  "yaml_errors": [],
  "json_errors": [],
  "lint_errors": [],
  "html_errors": [],
  "wcag_violations": [],
  "domain_errors": []
}
```

#### `POST /api/v1/clean`

Purges temporary build artifacts, cache directories, and volatile residue across projects.

---

### 2.6 WebSocket Real-Time Telemetry (`/ws/events`)

Real-time logging, telemetry, and pipeline progression are streamed to connected clients over a persistent WebSocket connection:
`ws://127.0.0.1:8765/ws/events`

#### Telemetry Event Schema (`PipelineEvent`)

```json
{
  "timestamp": "2026-09-13T00:15:02.123456Z",
  "step_number": 3,
  "total_steps": 7,
  "step_name": "Virtual Environment Creation",
  "status": "info",
  "message": "Provisioning virtual environment for lemgendary-training-suite...",
  "data": {
    "project": "lemgendary-training-suite",
    "venv_path": "C:\\Development\\python\\model-training\\lemgendary-training-suite\\.venv"
  }
}
```

Event Status Values:

- `info`: Informational milestone during pipeline processing.
- `success`: Step completed cleanly without warnings.
- `warning`: Step completed with non-fatal advisory notice.
- `error`: Fatal error encountered in step execution.

---

## 3. Desktop GUI Tauri IPC API Contracts

The desktop frontend `lemgendary-ai-studio-gui` communicates with the native Rust backend via Tauri v2 IPC invocations.

| IPC Command | Arguments | Return Type | Purpose |
| :--- | :--- | :--- | :--- |
| `run_system_probe` | None | `SystemProbeResult` | Triggers hardware discovery from native desktop thread |
| `get_ecosystem_status` | None | `EcosystemReport` | Queries active environment manager daemon for health metrics |
| `trigger_clean_install` | `project: Option<String>` | `PipelineLaunchResult` | Starts environment provisioning pipeline |
| `execute_validation` | `project: Option<String>` | `ValidationResult` | Runs multi-gate verification suite |
| `connect_telemetry_stream` | None | `WebSocketHandle` | Subscribes frontend to `/ws/events` channel |

---

## 4. Training Suite Python API Engine

The `lemgendary-training-suite` provides specialized Python classes for neural network training and validation.

Key API interfaces:

- `SawtoothGovernor`: Dynamic gradient scaling and learning rate scheduling preventing NaN divergence.
- `MemorySentinel`: Continuous VRAM monitoring that adjusts batch dimensions when nearing hardware limits.
- `SOTAValidationLadder`: Benchmark suite evaluating PSNR, SSIM, and LPIPS metrics against historical checkpoints.
- `ModelRegistry`: Typed metadata manager for reading and validating `unified_models_v2.yaml`.

Example Usage:

```python
from training.governor import SawtoothGovernor
from training.sentinel import MemorySentinel
from models.registry import ModelRegistry

registry = ModelRegistry.load_unified("unified_models_v2.yaml")
sentinel = MemorySentinel(target_device="cuda:0", headroom_mb=2048)
governor = SawtoothGovernor(initial_lr=1e-4, min_lr=1e-6)
```

---

## 5. Datasets Compilation & Stream Pipeline API

The `lemgendary-datasets` repository exposes Python APIs for compiling and reading structured image and market data.

Key API interfaces:

- `ManifoldCompiler`: High-throughput image pairing, bicubic downsampling, and synthetic noise generation.
- `ForexStreamCompiler`: Parquet chunking engine converting tick and candlestick data into normalized training tensors.
- `CloudSyncManager`: Authenticated transfer client interfacing with Google Cloud Storage and S3 buckets.

Example Usage:

```python
from datasets.compiler import ManifoldCompiler
from datasets.forex import ForexStreamCompiler

compiler = ManifoldCompiler(target_dir="LemGendizedNAFNet")
compiler.compile_pairs(hr_source="data/raw_hr", lr_dest="data/compiled_lr")
```

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
  "timestamp": "2026-09-13T00:00:00Z"
}
```
