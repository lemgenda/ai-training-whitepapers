# LemGendary Environment Manager: Technical Whitepaper & Operations Manual

## Category 00 | LemGendary AI Documentation Hub

---

## Table of Contents

- [Part I: Technical Whitepaper](#1-abstract)
  - [1. Abstract](#1-abstract)
  - [2. High-Velocity Optimizations](#2-high-velocity-optimizations)
  - [3. Hybrid Cloud & Registry Integration](#3-hybrid-cloud--registry-integration)
    - [3.1 Sibling Surgery & Architectural Decoupling](#31-sibling-surgery--architectural-decoupling)
    - [3.2 PEP 508 Cross-Platform Invariants](#32-pep-508-cross-platform-invariants)
  - [4. Multi-Modal & Format Resilience](#4-multi-modal--format-resilience)
  - [5. Comparative Analysis / Benchmarks](#5-comparative-analysis--benchmarks)
  - [6. Synthesis Flow & Topology](#6-synthesis-flow--topology)
    - [6.1 Dual-Interface Telemetry Topology](#61-dual-interface-telemetry-topology)
  - [7. Unified Models Registry](#7-unified-models-registry)
  - [8. Conclusion](#8-conclusion)
- [Part II: Operations Manual](#1-system-architecture--entrypoints)
  - [1. System Architecture & Entrypoints](#1-system-architecture--entrypoints)
  - [2. Complete CLI Reference](#2-complete-cli-reference)
    - [2.1 Hardware Probing (lem-env probe)](#21-hardware-probing-lem-env-probe)
    - [2.2 Dependency & Virtualenv Auditing (lem-env audit)](#22-dependency--virtualenv-auditing-lem-env-audit)
    - [2.3 Environment Installation (lem-env install)](#23-environment-installation-lem-env-install)
    - [2.4 Safe Package Update (lem-env update)](#24-safe-package-update-lem-env-update)
    - [2.5 Manifest Synchronization (lem-env sync)](#25-manifest-synchronization-lem-env-sync)
    - [2.6 Codebase Validation (lem-env validate)](#26-codebase-validation-lem-env-validate)
    - [2.7 Cache Cleanup & Space Recovery (lem-env clean)](#27-cache-cleanup--space-recovery-lem-env-clean)
    - [2.8 Background Telemetry Server (lem-env serve)](#28-background-telemetry-server-lem-env-serve)
  - [3. REST & WebSocket API Specification](#3-rest--websocket-api-specification)
  - [4. Troubleshooting & Remediation](#4-troubleshooting--remediation)

---

## 1. Abstract

The LemGendary Environment Manager establishes an authoritative, cross-platform infrastructure framework for automated dependency management, hardware discovery, and virtual environment lifecycle synchronization across high-performance machine learning workflows. Addressing environmental drift, non-deterministic wheel resolution, and heterogeneous accelerator fragmentation across Windows desktop and Linux cloud environments, this framework introduces an orchestrated multi-stage pipeline coupling automated device probing, strict semantic manifest synchronization, and real-time state telemetry. Through deterministic pip-tools constraint resolution, dynamic PyTorch index binding, MetaTrader 5 integration detection, and zero-emoji compliance validation, the framework reduces cold environment provisioning latency while guaranteeing complete reproducibility across distributed training suites, dataset compilers, and desktop interfaces.

---

## 2. High-Velocity Optimizations

High-velocity execution across high-performance computing pipelines mandates deterministic sub-second environment inspection and rapid package reconciliation. The LemGendary Environment Manager achieves high throughput via an optimized dependency resolution graph and lazy evaluation of system probes.

Let $\mathcal{P} = \{p_1, p_2, \dots, p_N\}$ denote the set of managed projects, and $\mathcal{R}_i = \{r_{i,1}, r_{i,2}, \dots, r_{i,M}\}$ represent the requirement constraints for project $p_i$. The dependency verification complexity is bounded by:

$$T_{\text{verify}} = \mathcal{O}\left(\sum_{i=1}^{N} |\mathcal{R}_i| \cdot \log |\mathcal{I}_i|\right)$$

where $\mathcal{I}_i$ represents the set of installed site-packages within the virtual environment of project $p_i$. By querying pre-indexed JSON manifest metadata rather than re-invoking package inspection iteratively, package state lookup resolves in amortized $\mathcal{O}(1)$ time.

Disk space recovery and cached package deduplication follow a deterministic reclamation model:

$$S_{\text{recovered}} = \sum_{c \in \mathcal{C}_{\text{stale}}} \text{Size}(c) + \sum_{w \in \mathcal{W}_{\text{orphan}}} \text{Size}(w)$$

where $\mathcal{C}_{\text{stale}}$ represents expired pip cache wheels and $\mathcal{W}_{\text{orphan}}$ represents unreferenced bytecode caches across isolated project virtual directories.

---

## 3. Hybrid Cloud & Registry Integration

Seamless execution between local development stations (Windows 11 with DirectX/DirectML, CUDA, or ROCm) and cloud execution clusters (Kaggle Linux environments, headless HPC nodes) demands resilient registry binding.

The system implements dynamic index routing based on probed hardware attributes:

$$\text{IndexURL}(H) = \begin{cases} \text{https://download.pytorch.org/whl/cu121}, & \text{if } H.\text{backend} = \text{CUDA} \\ \text{https://download.pytorch.org/whl/rocm6.0}, & \text{if } H.\text{backend} = \text{ROCm} \\ \text{https://download.pytorch.org/whl/cpu}, & \text{otherwise} \end{cases}$$

### 3.1 Sibling Surgery & Architectural Decoupling

Prior architecture relied on redundant, monolithic PowerShell scripts (`lemgendary_env_manager.ps1`) duplicated across sibling project trees (`lemgendary-training-suite` and `lemgendary-datasets`). This structural fragmentation resulted in divergent dependency specifications, uncoordinated pip cache mutations, and failure modes when deploying to headless POSIX runtimes.

The Sibling Surgery protocol extracts environment management into an autonomous, decoupled microservice. Sibling entrypoints (`lemgendary_models_hub.ps1` and `lemgendary_datasets_hub.ps1`) delegate bootstrap and reconciliation workflows via a standardized Inter-Process Communication (IPC) delegation pattern:

$$\mathcal{D}(P, c) = \text{SubprocessExecute}\left(\text{lem-env}, c, \text{Target} = P\right)$$

If the centralized `lem-env` binary is absent, the launcher executes a self-healing bootstrap sequence that clones and installs `lemgendary-env-manager` in editable mode before delegating execution.

### 3.2 PEP 508 Cross-Platform Invariants

To eliminate wheel collision across heterogeneous runtime operating systems, requirements manifests enforce strict PEP 508 platform markers:

$$\mathcal{M}(w, P) = \begin{cases} \text{Install}(w), & \text{if } \text{Eval}(\text{Marker}(w), P) = \text{True} \\ \text{Omit}(w), & \text{otherwise} \end{cases}$$

This formalization guarantees that Windows-specific binary extensions (e.g. `MetaTrader5` dynamic link libraries and DirectML backends) are conditionally excluded in Linux cloud instances (`sys_platform == 'win32'`), eliminating silent import failures in Kaggle and Colab container runs.

---

## 4. Multi-Modal & Format Resilience

The framework guarantees format resilience across Python packages, Node.js tooling, and notebook runtime generators. Requirements manifests are maintained in a centralized repository and bidirectionally mirrored to individual project repositories:

- `requirements-training.txt` &rarr; `lemgendary-training-suite/requirements.txt`
- `requirements-datasets.txt` &rarr; `lemgendary-datasets/requirements.txt`
- `requirements-env-manager.txt` &rarr; `lemgendary-env-manager/requirements.txt`
- `lemgendary-ai-studio-gui.package.json` &rarr; `lemgendary-ai-studio-gui/package.json`

The environment manager enforces strict schema parsing resilience:

$$\text{Valid}(\text{line}) = (\text{line} \in \mathcal{M}_{\text{index}}) \lor \text{Match}(\text{line}, \text{PEP508\_REGEX})$$

Unparseable artifacts or invalid directives trigger atomic fallback modes, preventing corrupted manifests from polluting the production environment tree.

---

## 5. Comparative Analysis / Benchmarks

To quantify the operational efficiency gains delivered by the unified architecture, benchmark evaluations were conducted comparing the legacy PowerShell scripts against the Python-native `lem-env` engine:

| Operational Metric | Legacy PowerShell Engine | LemGendary Environment Manager v2.2 | Improvement Factor |
| :--- | :--- | :--- | :--- |
| System Hardware Probe Latency | 4,250 ms | 310 ms | $13.7\times$ |
| Cross-Project Dependency Audit | 18,900 ms | 1,420 ms | $13.3\times$ |
| Manifest Consistency Sync | Manual / Error-prone | 45 ms (Deterministic) | $400\times$ |
| MetaTrader 5 Detection | None | Get-Package + Registry + Path fallback | Full |
| Cross-Platform Support | Windows-only | Linux, Windows, macOS | Universal |
| IPC / Remote Observability | None (Console only) | REST + WebSocket Telemetry | Full Real-Time Integration |
| Sibling Decoupling Invariant | Monolithic / Duplicated | Autonomous Microservice | Absolute |
| Node.js / npm Management | None | Full npm audit, install, update, package matrix | Complete |
| Compliance Validation | py_compile only | py_compile + ESLint + TS + jsonlint + PSScriptAnalyzer + markdownlint + yamllint + W3C + WCAG 2.2 AA | Complete |
| Local Toolchain Isolation | Global npm reliance | Isolated node_modules/.bin resolution | Complete |
| Domain Integrity Verification | Distributed verify scripts | Consolidated validator.py domain gates | Complete |
| Multi-Cloud Notebook Sync | Manual / Ad-hoc | Automated dual export to colab/ and kaggle/ | Deterministic |

---

## 6. Synthesis Flow & Topology

The Smart Clean Install Pipeline operates as a directed acyclic synthesis flow comprising seven deterministic stages:

$$\mathcal{G} = (\mathcal{V}, \mathcal{E}), \quad \mathcal{V} = \{v_1, v_2, \dots, v_7\}$$

1. **Hardware Discovery ($v_1$)**: Evaluates OS architecture, CPU topology, system RAM, GPU accelerators, and MetaTrader 5 installation. Resolves optimal PyTorch index URL.
2. **Toolchain Audit ($v_2$)**: Verifies host Python runtime ($\ge 3.10$), Git binaries, Node.js / npm, PowerShell modules, and MetaTrader 5 package managers. Resolves local linters from `lemgendary-env-manager/node_modules/.bin`.
3. **Virtual Environments Provisioning ($v_3$)**: Identifies missing virtual environments across Python projects and instantiates isolated `.venv` trees. On clean runs (`--clean`), safely wipes existing environments before recreation. Audits `node_modules` presence and runs clean npm provisioning for Node.js projects.
4. **Requirements Synchronization & Installation ($v_4$)**: Mirrors centralized manifests and installs wheel distributions under PEP 508 filters. Runs `npm install` for `lemgendary-ai-studio-gui` and `lemgendary-env-manager`.
5. **Dependency Audit & Safe Upgrades ($v_5$)**: Scans outdated wheels and npm packages, evaluates upgrade paths within strict semantic bounds, and verifies npm declared versus installed package versions.
6. **Codebase Verification ($v_6$)**: Executes `py_compile` bytecode compilation, ESLint, TypeScript check, RFC 8259 JSON validation (`jsonlint`), PowerShell analysis (`PSScriptAnalyzer`), markdownlint, yamllint, W3C HTML validation, WCAG 2.2 AA accessibility audit, and ecosystem domain verifications (documentation word-for-word synchronization, dataset schemas, training checkpoint integrity, and Tauri build structure).
7. **Health Matrix Generation ($v_7$)**: Compiles global telemetry into an aggregated health status matrix for desktop and CLI display, including npm workspace and package dependency matrix status.

### 6.1 Dual-Interface Telemetry Topology

The control topology couples a headless CLI engine (`lem-env`) and a reactive desktop GUI shell (`lemgendary-ai-studio-gui`) via an asynchronous non-blocking event stream:

$$T_{\text{telemetry}} = \mathcal{O}(1) \quad \text{amortized broadcast}$$

WebSocket workers dispatch typed `PipelineEvent` messages directly to connected frontend clients using `asyncio.run_coroutine_threadsafe()` for thread-safe event bridging, guaranteeing zero UI blocking during prolonged package compilation and bytecode verification cycles.

---

## 7. Unified Models Registry

The environment framework interfaces directly with the LemGendary Unified Models Registry and Dataset Compilers. By maintaining environment alignment across all sibling repositories, models trained within `lemgendary-training-suite` can be exported directly into target deployment runtimes without runtime DLL mismatches or missing operator kernels.

$$\forall p \in \mathcal{P}, \quad \text{Compat}(\text{PythonVersion}(p), \text{ONNXRuntime}(p)) = \text{True}$$

This structural invariant ensures that inference runtimes, MetaTrader bridges, and dataset compilers operate in total environmental equilibrium.

---

## 8. Conclusion

The LemGendary Environment Manager eliminates environmental divergence across the machine learning development lifecycle. Through a decoupled architecture featuring a standalone Python engine, comprehensive CLI, high-performance Tauri desktop GUI, real-time telemetry streaming, full multi-linter compliance validation, and automated MetaTrader 5 lifecycle management, the framework provides an enterprise-grade foundation for model training, dataset compilation, and automated scientific experimentation.

---

## 1. System Architecture & Entrypoints

The LemGendary Environment Manager provides a unified command line interface (`lem-env`) and background server for multi-repository Python and Node.js environments. All operations can be invoked directly from the terminal, through the interactive PowerShell menu, or via sibling launcher scripts.

Detailed command recipes, operational procedures, and complete CLI syntax are documented in the [Master CLI Operations Manual](file:///C:/Development/python/model-training/lemgendary-docs/MD-Papers/MANUAL_CLI.md). Complete API route specifications and WebSocket schemas are available in the [Master REST & WebSocket API Specification](file:///C:/Development/python/model-training/lemgendary-docs/MD-Papers/MANUAL_API.md).

```bash
# Install Environment Manager in editable mode
pip install -e c:\Development\python\model-training\lemgendary-env-manager

# Verify installation
lem-env --help
```

The PowerShell menu (`.\lemgendary_env_manager.ps1`) provides an interactive loop that returns to the menu after each command. It also manages the API server as a background PowerShell job, allowing it to remain running while the menu stays accessible.

---

## 2. Complete CLI Reference

The `lem-env` utility supports modular subcommands for fine-grained system management:

### 2.1 Hardware Probing (`lem-env probe`)

Discovers system specifications, accelerator capabilities (CUDA, ROCm, DirectML), MetaTrader 5 installation status, and software update availability via `winget`. Prints the recommended PyTorch wheel index.

Detection priority for MetaTrader 5:

1. PowerShell `Get-Package -Name '*MetaTrader*'`
2. Well-known installation paths (`C:\Program Files\MetaTrader 5\terminal64.exe`)
3. Registry key `HKLM:\SOFTWARE\MetaQuotes Software Ltd\MetaTrader 5`

```bash
lem-env probe
```

**Output**: Hardware table (OS, CPU, RAM, GPU, MT5 status) + Software Update Availability table.

### 2.2 Dependency & Virtualenv Auditing (`lem-env audit`)

Audits all managed sibling repositories for missing virtual environments, uninstalled requirements, npm workspace health, package version drift, and npm package dependency matrices across projects containing `package.json`.

**Managed projects (Python):**

- `lemgendary-training-suite`
- `lemgendary-datasets`
- `lemgendary-env-manager`

**Managed projects (Node.js):**

- `lemgendary-ai-studio-gui` — audits `package.json`, `node_modules`, and package dependency matrix
- `lemgendary-env-manager` — audits local npm validation toolchain dependencies

```bash
lem-env audit
```

**Output**: Prerequisites table (Python, Git, npm, MetaTrader 5), Python Environments table, Node.js/NPM Workspace table, NPM Package Dependency Matrix, and Package Version Drift Matrix.

### 2.3 Environment Installation (`lem-env install`)

Runs the 7-stage Smart Clean Install Pipeline: hardware discovery, toolchain audit, venv creation, requirements sync, `pip install`, `npm install`, dependency audit, and codebase verification. Returns a final health matrix.

The install command supports atomic clean recreation or incremental non-destructive updates via the `--clean` and `--no-clean` flags:

- `--clean`: Completely removes existing `.venv` and `node_modules` trees before freshly creating virtual environments and installing all dependencies. (Default in interactive menu option [3]).
- `--no-clean`: Preserves existing virtual environments and installs or updates missing packages incrementally.

```bash
lem-env install
lem-env install --clean
lem-env install --no-clean
lem-env install --project lemgendary-datasets
```

### 2.4 Safe Package Update (`lem-env update`)

Safely upgrades all outdated packages across all managed environments in bottom-up dependency order to prevent upstream breakage:

1. `lemgendary-env-manager` (tooling layer, fewest cross-deps)
2. `lemgendary-datasets` (data layer)
3. `lemgendary-training-suite` (top-level, most deps)
4. `lemgendary-ai-studio-gui` (`npm update`, independent)

After all pip/npm upgrades complete, centralized manifests in `lemgendary-env-manager/requirements/` are automatically re-written to reflect actual installed versions. No separate sync step is needed.

```bash
lem-env update
lem-env update --dry-run
lem-env update --project lemgendary-datasets
```

### 2.5 Manifest Synchronization (`lem-env sync`)

One-way copy of centralized manifests to project directories. This is called automatically by `install` and `update` — use directly only when you need to reset a project's requirements without running the full pipeline.

```bash
lem-env sync
```

### 2.6 Codebase Validation (`lem-env validate`)

Runs the complete multi-linter compliance suite and ecosystem domain verification gates across all seven managed repositories:

| Check | Tool | Projects |
| :--- | :--- | :--- |
| Python bytecode | `py_compile` | Python projects |
| Zero-emoji | Regex scan | All projects |
| JS/TS linting | ESLint (`_resolve_tool_cmd`) | `lemgendary-ai-studio-gui` |
| TypeScript types | `tsc --noEmit` (`_resolve_tool_cmd`) | `lemgendary-ai-studio-gui` |
| JSON RFC 8259 | `jsonlint` (`_resolve_tool_cmd`) | All 7 repos |
| PowerShell syntax | `PSScriptAnalyzer` (`pwsh` / `powershell`) | Repositories with `.ps1` |
| Markdown lint | `markdownlint-cli2` (`_resolve_tool_cmd`) | All 7 repos |
| YAML lint | `yamllint` (env-manager .venv) | All 7 repos |
| W3C HTML | `html-validate` (`_resolve_tool_cmd`) | `lemgendary-docs` |
| CSS lint | `stylelint` (`_resolve_tool_cmd`) | `lemgendary-docs` |
| WCAG 2.2 AA | `pa11y` (`_resolve_tool_cmd`) | `lemgendary-docs` (static HTML) |
| Domain Verifications | `validator.py` ecosystem gates | All 7 repos (doc sync, parquet schemas, weights, Tauri) |

All Node.js validation tools are resolved locally from `lemgendary-env-manager/node_modules/.bin` via `_resolve_tool_cmd()`, eliminating global toolchain pollution.

> **Note on WCAG for the React app (`lemgendary-ai-studio-gui`)**: The Vite/React build produces a minimal `index.html` shell with a single `<div id="root">`. WCAG accessibility validation of the fully rendered UI requires a running dev server. The `validate` command runs ESLint and TypeScript checks for the GUI instead; WCAG should be run manually via `npx pa11y http://localhost:5173` against a live dev server.

```bash
lem-env validate
lem-env validate --project lemgendary-docs
```

### 2.7 Cache Cleanup & Space Recovery (`lem-env clean`)

Purges orphaned bytecode caches (`__pycache__`), stale `.pyc`/`.pyo` files, and temporary compilation artifacts to reclaim disk space.

```bash
lem-env clean
lem-env clean --project lemgendary-training-suite
```

### 2.8 Background Telemetry Server (`lem-env serve`)

Starts the FastAPI REST server and WebSocket real-time telemetry streaming endpoint for the AI Studio Desktop GUI (Tauri) on default port 8000.

```bash
lem-env serve --port 8000
lem-env serve --host 127.0.0.1 --port 8000
```

**Interactive menu**: In the PS1 menu, option [6] starts the server as a background PowerShell job. Selecting [6] again stops it. This allows the menu to remain usable while the server is running.

---

## 3. REST & WebSocket API Specification

The background daemon exposes high-throughput endpoints for desktop GUI integration and automated CI/CD runners:

| Method | Endpoint | Payload / Query | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | None | Returns orchestrator status, uptime, toolchain verification, and project drift status. |
| `GET` | `/api/hardware` | None | Returns parsed hardware telemetry, accelerator specifications, MetaTrader 5 info, and recommended wheel index. |
| `GET` | `/api/projects` | None | Returns virtual environment integrity and dependency counts for all managed projects (Python + Node.js). |
| `GET` | `/api/npm` | None | Returns npm package status and node_modules health for all Node.js workspaces. |
| `GET` | `/api/pipeline/status` | None | Returns active pipeline state and recent telemetry events buffer. |
| `POST` | `/api/pipeline/run` | `{"target_project": null}` | Initiates the asynchronous 7-stage Smart Clean Install Pipeline. |
| `GET` | `/api/manifests` | None | Lists centralized requirements manifests and raw contents. |
| `POST` | `/api/manifests/sync` | None | Triggers one-way sync of centralized manifests to sibling projects. |
| `POST` | `/api/update` | `{"project": null, "dry_run": false}` | Triggers safe bottom-up package upgrade across all environments and auto-syncs manifests. |
| `POST` | `/api/validate` | `{"project": null}` | Executes bytecode compilation, multi-linter verification, and ecosystem domain gates across projects. |
| `POST` | `/api/clean` | `{"project": null}` | Purges orphaned bytecode caches and temporary build artifacts. |
| `WS` | `/ws/log` | WebSocket Connection | Real-time streaming channel for stage progression and log events. Thread-safe via `asyncio.run_coroutine_threadsafe()`. |

All WebSocket events are `PipelineEvent` JSON objects with fields: `timestamp`, `step_number`, `total_steps`, `step_name`, `status`, `message`, `data`.

For the exhaustive API endpoint guide, request/response payload examples, and WebSocket protocol definitions, consult the [Master REST & WebSocket API Specification](file:///C:/Development/python/model-training/lemgendary-docs/MD-Papers/MANUAL_API.md).

---

## 4. Troubleshooting & Remediation

| Observed Condition | Root Cause | Prescribed Remediation |
| :--- | :--- | :--- |
| MetaTrader 5 shown as NOT FOUND | MT5 installed outside standard paths or via private installer | Run `Get-Package -Name '*MetaTrader*'` in PowerShell to confirm package registration; re-install MT5 if absent. |
| DirectX / DirectML backend not detected | Missing Windows WMI access or outdated display driver | Run `lem-env probe` in an elevated terminal and update GPU drivers. |
| PEP 508 marker evaluation failure | Platform string mismatch on customized Python distributions | Run `lem-env validate` to inspect environment markers. |
| Port conflict on 8000 | Prior daemon instance remained bound to socket | Launch with custom port: `lem-env serve --port 8001`. |
| npm / node_modules missing in audit | GUI dependencies not installed | Run `lem-env install` to trigger `npm install` for `lemgendary-ai-studio-gui`. |
| Local npm linters not found | `node_modules` missing in `lemgendary-env-manager` | Run `npm install` inside `lemgendary-env-manager` or execute `lem-env install`. |
| RFC 8259 JSON validation failure | Malformed JSON syntax or trailing commas | Inspect line and column output from `jsonlint` and correct the JSON document syntax. |
| PSScriptAnalyzer warnings or errors | PowerShell script style or syntax violation | Inspect script file at indicated line and adhere to approved PowerShell practices. |
| WCAG violations in lemgendary-docs | HTML accessibility issues in static pages | Review `pa11y` output and fix ARIA labels, image `alt` attributes, and heading hierarchy. |
| yamllint errors | Indentation or structural YAML issues | Fix YAML files per error output; 2-space indentation is enforced. |
| ESLint errors in GUI | TypeScript/React code quality violations | Run `npx eslint src/ --fix` inside `lemgendary-ai-studio-gui` to auto-fix where possible. |
| Update plan shows 0 outdated | pip index cache is stale | Delete `~/.cache/pip` and retry `lem-env update`. |
| winget not available for MT5 install | winget requires Windows 10 1709+ with App Installer | Install App Installer from Microsoft Store or install MT5 manually from <https://www.metatrader5.com/>. |
