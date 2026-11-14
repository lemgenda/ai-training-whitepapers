# LemGendary Environment Manager: Technical Whitepaper

## Category 01.1 ENV | Subpage of Master Ecosystem Architecture

**Parent Hub**: [Master Ecosystem Architecture](./ECOSYSTEM_ARCHITECTURE.md)

**Version**: `v16.9.85-STABLE` (LemGendary Environment Manager) · **Last
audited**: 2026-11-13

---

## Table of Contents

- [1. Abstract](#1-abstract)
- [2. High-Velocity Optimizations](#2-high-velocity-optimizations)
- [3. Hybrid Cloud & Registry
  Integration](#3-hybrid-cloud--registry-integration)
  - [3.1 Sibling Surgery & Architectural
    Decoupling](#31-sibling-surgery--architectural-decoupling)
  - [3.2 PEP 508 Cross-Platform
    Invariants](#32-pep-508-cross-platform-invariants)
- [4. Multi-Modal & Format Resilience](#4-multi-modal--format-resilience)
- [5. Comparative Analysis / Benchmarks](#5-comparative-analysis--benchmarks)
- [6. Synthesis Flow & Topology](#6-synthesis-flow--topology)
  - [6.1 Entrypoints & Operator
    Interfaces](#61-entrypoints--operator-interfaces)
  - [6.2 Dual-Interface Telemetry
    Topology](#62-dual-interface-telemetry-topology)
  - [6.3 Desktop GUI State Aggregation & Multi-Sidecar Ecosystem
Observability](#63-desktop-gui-state-aggregation--multi-sidecar-ecosystem-observability)
  - [6.4 Background Update Jobs](#64-background-update-jobs)
  - [6.5 Security Model](#65-security-model)
  - [6.6 Bug Report Endpoint](#66-bug-report-endpoint)
  - [6.7 Ecosystem Registry
    (ecosystem.json)](#67-ecosystem-registry-ecosystemjson)
  - [6.8 Kaggle Credentials, Changelog Scope & Runtime Contract (v16.9.81 to
v16.9.85)](#68-kaggle-credentials-changelog-scope--runtime-contract-v16981-to-v16985)
- [7. Unified Models Registry](#7-unified-models-registry)
- [8. Conclusion](#8-conclusion)
- [Companion Documentation](#companion-documentation)

---

## 1. Abstract

The LemGendary Environment Manager (release `v16.9.85-STABLE`) is the
infrastructure layer of the LemGendary ecosystem: it probes hardware, provisions
and audits virtual environments, keeps dependency manifests aligned, validates
the workspace and serves this functionality to the LemGendary AI Studio GUI as a
local sidecar on port 8000. It addresses environmental drift, non-deterministic
wheel resolution and accelerator fragmentation through a seven-step pipeline
that couples device probing, one-way manifest synchronization with a downgrade
guard, reverse-dependency upgrade classification with a constraint-preserving
pip dry-run that fails closed, and real-time WebSocket telemetry. The pipeline
is non-destructive by default; a clean reinstall needs an explicit option. The
sidecar accepts browser requests only from AI Studio GUI origins, never returns
stored secrets, runs package updates as background jobs and packages bug reports
into a local ZIP archive for the operator's own mail client. Its
`ecosystem/ecosystem.json` is the single source of the ports, project list,
pipeline steps and identity that every project reads (Section 6.7).

---

## 2. High-Velocity Optimizations

High-velocity execution across high-performance computing pipelines mandates
deterministic sub-second environment inspection and rapid package
reconciliation. The LemGendary Environment Manager achieves high throughput via
an optimized dependency resolution graph and lazy evaluation of system probes.

Let $\mathcal{P} = \{p_1, p_2, \dots, p_N\}$ denote the set of managed projects,
and $\mathcal{R}_i = \{r_{i,1}, r_{i,2}, \dots, r_{i,M}\}$ represent the
requirement constraints for project $p_i$. The dependency verification
complexity is bounded by:

$$
T_{\text{verify}} = \mathcal{O}\left(\sum_{i=1}^{N} |\mathcal{R}_i| \cdot \log
|\mathcal{I}_i|\right)
$$

where $\mathcal{I}_i$ represents the set of installed site-packages within the
virtual environment of project $p_i$. By querying pre-indexed JSON manifest
metadata rather than re-invoking package inspection iteratively, package state
lookup resolves in amortized $\mathcal{O}(1)$ time.

Liveness and auditing are separated. `GET /api/ping` answers in constant time
without any I/O and is the probe the GUI uses to decide whether the sidecar is
online; `GET /api/health` remains the full audit (prerequisites, hardware and
`pip list` per project) for the Health panel.

Disk space recovery and cached package deduplication follow a deterministic
reclamation model:

$$
S_{\text{recovered}} = \sum_{c \in \mathcal{C}_{\text{stale}}} \text{Size}(c) +
\sum_{w \in \mathcal{W}_{\text{orphan}}} \text{Size}(w)
$$

where $\mathcal{C}_{\text{stale}}$ represents expired pip cache wheels and
$\mathcal{W}_{\text{orphan}}$ represents unreferenced bytecode caches across
isolated project virtual directories.

---

## 3. Hybrid Cloud & Registry Integration

Seamless execution between local development stations (Windows 11 with
DirectX/DirectML, CUDA, or ROCm) and cloud execution clusters (Kaggle Linux
environments, headless HPC nodes) demands resilient registry binding.

The system implements dynamic index routing based on probed hardware attributes.
The probe checks the backends in the order CUDA, ROCm, Apple MPS, DirectML and
CPU. On CUDA hosts the index depends on the NVIDIA driver major version $d$
(`select_cuda_torch_index()`); an unknown or unparseable driver version selects
`cu126`:

$$
\text{IndexURL}(H) = \begin{cases} \text{.../whl/cu134}, & \text{if }
H.\text{backend} = \text{CUDA} \land d \ge 610 \\ \text{.../whl/cu126}, &
\text{if } H.\text{backend} = \text{CUDA} \land 560 \le d < 610 \\
\text{.../whl/cu121}, & \text{if } H.\text{backend} = \text{CUDA} \land 535
\le d < 560 \\ \text{.../whl/cu118}, & \text{if } H.\text{backend} =
\text{CUDA} \land d < 535 \\ \text{.../whl/rocm6.0}, & \text{if }
H.\text{backend} = \text{ROCm} \\ \text{PyPI}, & \text{if } H.\text{backend} =
\text{MPS} \\ \text{.../whl/cpu}, & \text{otherwise (DirectML or CPU)}
\end{cases}
$$

where `.../whl/` stands for `https://download.pytorch.org/whl/` and PyPI for
`https://pypi.org/simple`.

Since v16.9.70 the central requirements files carry no fixed `--extra-index-url`
line: the installer passes the probed index, so CPU hosts and older drivers no
longer receive `cu134` wheels. Since v16.9.71 macOS on arm64 reports one `mps`
device (unified memory as VRAM), the DirectML probe reads the 64-bit adapter
memory size from the registry (adapters above 4 GB no longer report 4095 MB) and
skips basic, Hyper-V, remote and virtual display adapters, and `rocm-smi` output
is read as CSV. The pinned versions (`torch==2.15.0`, `torchvision==0.29.2`,
`torchaudio==2.11.1`) are the same on every backend; only the wheel build
differs.

### 3.1 Sibling Surgery & Architectural Decoupling

Prior architecture relied on redundant, monolithic PowerShell scripts
(`lemgendary_env_manager.ps1`) duplicated across sibling project trees
(`lemgendary-training-suite` and `lemgendary-datasets`). This structural
fragmentation resulted in divergent dependency specifications, uncoordinated pip
cache mutations, and failure modes when deploying to headless POSIX runtimes.

The Sibling Surgery protocol extracts environment management into an
autonomous, decoupled microservice. Sibling entrypoints
(`lemgendary_models_hub.ps1` and `lemgendary_datasets_hub.ps1`) delegate
bootstrap and reconciliation workflows via a standardized Inter-Process
Communication (IPC) delegation pattern:

$$
\mathcal{D}(P, c) = \text{SubprocessExecute}\left(\text{lem-env}, c,
\text{Target} = P\right)
$$

If the centralized `lem-env` binary is absent, the launcher executes a
self-healing bootstrap sequence that clones and installs
`lemgendary-env-manager` in editable mode before delegating execution.

### 3.2 PEP 508 Cross-Platform Invariants

To eliminate wheel collision across heterogeneous runtime operating systems,
requirements manifests enforce strict PEP 508 platform markers:

$$
\mathcal{M}(w, P) = \begin{cases} \text{Install}(w), & \text{if }
\text{Eval}(\text{Marker}(w), P) = \text{True} \\ \text{Omit}(w), &
\text{otherwise} \end{cases}
$$

This formalization guarantees that Windows-specific binary extensions (e.g.
`MetaTrader5` dynamic link libraries and DirectML backends) are conditionally
excluded in Linux cloud instances (`sys_platform == 'win32'`), eliminating
silent import failures in Kaggle and Colab container runs.

Since v16.9.70 `bitsandbytes` carries `; sys_platform != 'darwin'` in
`requirements-training.txt`, so macOS installs skip it.

---

## 4. Multi-Modal & Format Resilience

The framework guarantees format resilience across Python packages and Node.js
tooling. The central files in `lemgendary-env-manager/requirements/` are the
single source of truth; each sibling manifest is a generated copy. Sync is
one-way, from central to sibling (`lem-env sync`, `POST /api/manifests/sync` and
pipeline steps 4 and 6):

- `requirements-training.txt` → `lemgendary-training-suite/requirements.txt`
- `requirements-datasets.txt` → `lemgendary-datasets/requirements.txt`
- `requirements-env-manager.txt` → `lemgendary-env-manager/requirements.txt`
- `requirements-documentation.txt` → `lemgendary-docs/requirements.txt`
- `lemgendary-ai-studio-gui.package.json` →
  `lemgendary-ai-studio-gui/package.json`
- `lemgendary-env-manager.package.json` → `lemgendary-env-manager/package.json`

Sync never takes anything away from a sibling. Let $C$ and $S$ be the central
and sibling requirement sets, compared per package and environment marker, and
$\text{floor}(r)$ the lowest version a requirement admits. The copy is written
only when the drift set is empty:

$$
\text{Drift}(C, S) = \{ s \in S : s \notin C \} \cup \{ s \in S :
\text{pinned}(s) \land \lnot \text{pinned}(C_s) \} \cup \{ s \in S :
\text{floor}(C_s) < \text{floor}(s) \}
$$

A non-empty drift set leaves both files unchanged and is reported as a
`DRIFT:` warning (`find_requirement_drift`, `find_package_json_drift`); the fix
is to raise the central pin and sync again. The `package.json` `version` is a
release field, not dependency data (`NPM_RELEASE_KEYS`, since v16.9.60): the
central npm manifests do not hold it, drift ignores it and sync keeps the
sibling's own value.

Upgrades flow back the other way only after validation. Since v16.9.72
`finalize_upgrade()` validates the upgraded projects and, only when all pass,
re-pins the central requirements from the venvs: only exact `==` pins are
re-pinned, local build tags such as `+cu134` or `+cpu` are stripped, and extras,
`>=` floors, ranges and markers are kept. Upgraded npm dependency sections flow
from a project `package.json` back to its central manifest, which keeps no
`version`. `lem-env update`, the GUI update job and pipeline step 6 follow this
order. Since v16.9.79 the GUI manifest editor (`/api/manifests/registry`) opens
the central manifests instead of the generated copies, and `POST
/api/manifests/save` on a central manifest runs the sync to every sibling and
returns its results as `sync`.

The environment manager enforces strict schema parsing resilience:

$$
\text{Valid}(\text{line}) = (\text{line} \in \mathcal{M}_{\text{index}}) \lor
\text{Match}(\text{line}, \text{PEP508\_REGEX})
$$

pip output is parsed fail-closed. pip stdout and stderr are captured on separate
pipes, so warnings never corrupt `--format=json` or `--report -` output. A
failed or unparseable `pip list` or `pip inspect` raises `PipJsonError`, and the
upgrade classifier then blocks every candidate instead of guessing.

---

## 5. Comparative Analysis / Benchmarks

To quantify the operational efficiency gains delivered by the unified
architecture, benchmark evaluations were conducted comparing the legacy
PowerShell scripts against the Python-native `lem-env` engine. The latency
figures were measured at release `v16.8.0`; the repository does not contain the
benchmark harness, so they are historical values that cannot be reproduced from
the current code.

Latency measured at `v16.8.0` (legacy engine versus `lem-env`):

| Operational Metric | Legacy PowerShell | `lem-env` | Factor |
| :--- | :--- | :--- | :--- |
| System Hardware Probe Latency | 4,250 ms | 310 ms | $13.7\times$ |
| Cross-Project Dependency Audit | 18,900 ms | 1,420 ms | $13.3\times$ |
| Manifest Consistency Sync | Manual | 45 ms | $400\times$ |
| MetaTrader 5 Detection | None | ~5 ms | Sub-second |

Capabilities at `16.9.60`:

| Capability | Legacy PowerShell | `lem-env` `v16.9.60` |
| :--- | :--- | :--- |
| Manifest sync | Manual copy | One-way, downgrade guard |
| MetaTrader 5 detection | None | Registry-first + file version |
| Upgrade safety | None | Reverse-dep check + dry-run, fail-closed |
| Cache corruption recovery | Hard failure | Detect, purge, retry |
| Platforms | Windows | Engine: Linux, Windows, macOS (1) |
| Remote observability | Console only | REST + WebSocket telemetry |
| Sibling decoupling | Duplicated scripts | Autonomous microservice |
| Node.js / npm | None | Audit, install, `npm outdated` upgrades |
| Compliance validation | `py_compile` | Multi-linter suite (2) |
| Local toolchain | Global npm | Isolated `node_modules/.bin` |
| Domain verification | Separate scripts | `validator.py` domain gates |
| Destructive reinstall | Always | Only with `--clean` / `"clean": true` |

(1) The PowerShell launcher and the git hook template are Windows-only.
(2) Python compile check, ESLint, TypeScript, jsonlint, PSScriptAnalyzer,
Pylint,
forbidden suppressions, absolute paths, markdownlint, yamllint, W3C HTML, WCAG
2.2 AA and the `ecosystem_ssot` gate.

---

## 6. Synthesis Flow & Topology

The Smart Install Pipeline operates as a directed acyclic synthesis flow
comprising seven deterministic stages:

$$
\mathcal{G} = (\mathcal{V}, \mathcal{E}), \quad \mathcal{V} = \{v_1, v_2, \dots,
v_7\}
$$

Since v16.9.49 the step numbers, ids and names come from `pipeline_steps` in
`ecosystem/ecosystem.json` (Section 6.7), and the step events of the pipeline
carry those names: Hardware Discovery, Toolchain Audit, Virtual Environments,
Requirements Sync & Install, Dependency Audit & Upgrades, Codebase Verification
and Health Matrix. The list below describes what each step does.

1. **Hardware Discovery ($v_1$)**: Evaluates OS architecture, CPU topology,
   system RAM, GPU accelerators, and MetaTrader 5 installation. Resolves the
   PyTorch index URL (Section 3). MT5 detection uses a registry-first strategy
   with `terminal64.exe` file-version extraction for authoritative version
   reporting even when winget has no record of the installation.
2. **Toolchain Audit ($v_2$)**: Verifies the host Python runtime, Git binaries,
   Node.js / npm, PowerShell modules, and MetaTrader 5 package managers.
   Resolves local linters from `lemgendary-env-manager/node_modules/.bin`.
   `pyproject.toml` declares `requires-python >=3.12`, the bootstrap
   (`MIN_PYTHON`) and the launcher ask for Python 3.12+, and a test keeps the
   values equal; the code uses Python 3.12 APIs (`Path.walk`,
   `shutil.rmtree(onexc=...)`, `datetime.UTC`). pip counts as installed when
   `pip` or `pip3` is on PATH or `python -m pip --version` succeeds (since
   v16.9.73).
3. **Virtual Environments Provisioning ($v_3$)**: Identifies missing or invalid
   virtual environments across Python projects and creates isolated `.venv`
   trees. A default run keeps valid venvs and `node_modules` and stops no
   processes. Only a clean run (`lem-env install --clean` or `"clean": true` on
   `POST /api/pipeline/run`) deletes every `.venv` and `node_modules`, stops
   processes running from those venvs and reinstalls; the environment executing
   the pipeline is preserved. A failed `node_modules` purge is reported as a
   step error. The running environment is recognized from `sys.prefix` (since
   v16.9.69), which also holds on Linux and macOS, where the venv interpreter is
   a symlink to the base Python.
4. **Requirements Synchronization & Installation ($v_4$)**: Writes the central
   manifests to the siblings under the downgrade guard (Section 4) and installs
   wheel distributions under PEP 508 filters. Runs `npm install` for
   `lemgendary-ai-studio-gui` and `lemgendary-env-manager`. Applies OpenCV
   variant normalization after install to guarantee a single `cv2` provider per
   project. A project with `pyproject.toml` or `setup.py` is then installed in
   editable mode (`pip install --no-deps --no-build-isolation -e`), so console
   scripts such as `lem-env` exist in the venv. Since v16.9.82 a failed
   editable install is a structured warning, not an install failure (the
   project's dependencies are already installed): step 4 reports `warning`
   with `data.install_warning`, step 7 summarises the install warnings, and a
   full run ends with `last_status: warning`.
5. **Dependency Audit & Safe Upgrades ($v_5$)**: Routes by discovery metadata:
   every Python project gets the pip path and every project with a
   `package.json` (`has_npm_manifest`) gets the npm path (`npm outdated`), so a
   dual-stack project gets both. Every pip candidate is classified as safe or
   blocked by a reverse-dependency check (via `pip inspect --local`) followed by
   a constraint-preserving pip dry-run. Only safe candidates are upgraded;
   blocked candidates carry a reason describing the violated requirement.
   The apply phase installs exactly the vetted versions (`name==version`), and
   a failed install restores the `pip freeze` snapshot taken before it.
   Since v16.9.72 step 5 uses the same planning and apply engine as `lem-env
   update`. Torch-family packages on CUDA hosts are resolved against the PyTorch
   CUDA index, filtered to the installed subset and vetted as one family:
   reverse dependencies outside the family, then one dry-run against the CUDA
   index.
6. **Codebase Verification ($v_6$)**: Compiles every Python file in memory
   (built-in `compile`, so no `__pycache__` is written) and runs the
   registered validation gates
   (`env_manager/validation/registry.py`): yamllint, RFC 8259 JSON validation,
   markdownlint, ESLint, TypeScript check, W3C HTML validation, WCAG 2.2 AA
   accessibility audit, PowerShell analysis (`PSScriptAnalyzer`), Pylint,
   forbidden suppressions (Python directives and `warnings` filters, TS/JS
   `@ts-*` and `eslint-disable` comments, Rust `allow` attributes, silent
   `except` and empty `catch` blocks, PowerShell `SilentlyContinue`, rule
   disables in linter configs), hardcoded
   absolute paths, ecosystem domain verifications (README changelog, docs hub,
   dataset manifests, training suite, models hub, git hooks) and
   `ecosystem_ssot` (Section 6.7). Gates fail closed: a missing or crashing
   tool is a `tool_error` finding, and the npx fallback never downloads
   packages. A new gate is one more `Gate` in the registry. The documentation
   check compares each Markdown and HTML pair by H2 count, table count and
   length ratio; it is not a word-for-word comparison. Changes in v16.9.74 to
   v16.9.78: a project without its own Pylint config is linted with the
   env-manager `.pylintrc`; ESLint warnings fail like errors and flat configs
   get no `--ext`; `tsc` also checks `tsconfig.node.json`; html-validate and
   pa11y run on every HTML page and name the file; the emoji scan covers every
   text type and the `.githooks`, `.github` and `.agents` folders; the
   documentation test suite runs as a subprocess with the docs `.venv`; and step
   6 validates every validated project, not only those with a venv. Since
   v16.9.80 `run_tool` requires a working directory and every gate runs its
   tool from the project directory, so `validate` launched from the
   workspace root (which is not a git repository) no longer crashes the
   yamllint gate, whose `ignore-from-file: .gitignore` resolves against the
   working directory.
7. **Health Matrix Generation ($v_7$)**: Compiles global telemetry into an
   aggregated health status matrix for desktop and CLI display, including
   manifest coverage, single-manifest package inventory, and npm workspace
   drift.

### 6.1 Entrypoints & Operator Interfaces

The LemGendary Environment Manager provides a unified command line interface
(`lem-env`) and a background API server for multi-repository Python and Node.js
environments. Its commands are `probe`, `audit`, `install`, `update`, `sync`,
`validate`, `clean`, `serve`, `setup-hooks` and `hooks`. All operations can be
invoked directly from the terminal, through the interactive PowerShell menu, or
via sibling launcher scripts. `lem-env update --project X` plans and applies
upgrades for project X only; an unknown project exits with code 1.

Detailed command recipes, operational procedures, and complete CLI syntax are
documented in the [Master CLI Operations Manual](./MANUAL_CLI.md). Complete API
route specifications and WebSocket schemas are available in the [Master REST &
WebSocket API Specification](./MANUAL_API.md).

```bash
# Install Environment Manager in editable mode
pip install -e ./lemgendary-env-manager

# Verify installation
lem-env --help
```

The PowerShell menu (`.\lemgendary_env_manager.ps1`) provides an interactive
loop that returns to the menu after each command. It also manages the API server
as a background PowerShell job, allowing it to remain running while the menu
stays accessible.

### 6.2 Dual-Interface Telemetry Topology

The control topology couples a headless CLI engine (`lem-env`) and a reactive
desktop GUI shell (`lemgendary-ai-studio-gui`) via an asynchronous non-blocking
event stream:

$$
T_{\text{telemetry}} = \mathcal{O}(1) \quad \text{amortized broadcast}
$$

Pipeline and update worker threads dispatch typed `PipelineEvent` messages to
connected WebSocket clients through `asyncio.run_coroutine_threadsafe()`, which
bridges the worker threads to the server event loop without blocking the UI
during prolonged package compilation and bytecode verification. The FastAPI
`@asynccontextmanager` lifespan handler starts the ecosystem sidecars in the
thread pool on startup.

To eliminate unobservable blocking stalls during dependency installation, the
execution subsystem deploys unbuffered real-time streaming generators
(`stream_pip_with_recovery`, `stream_npm_install`,
`stream_install_requirements`) that yield subprocess output line-by-line using
`PYTHONUNBUFFERED="1"` and `--progress-bar on`. Streaming lines are parsed in
real time to extract wheel download metrics (transfer bandwidth, byte ratios,
and ETA countdowns), requirement progress ratios (`[k/N requirements]`), and
discrete stage milestones, broadcasting typed progress events
(`is_progress=True`) over the `/ws/log` WebSocket channel without terminal
stream saturation.

### 6.3 Desktop GUI State Aggregation & Multi-Sidecar Ecosystem Observability

To minimize HTTP handshake overhead in desktop graphical clients, the
Environment Manager daemon exposes high-density aggregated endpoints:

- **Liveness (`/api/ping`)**: Constant-time `GET` and `HEAD` probe returning
  `status`, `service` and `version`.
- **State Aggregation (`/api/gui/state`)**: Packages system identity, hardware
  sensors, discovered repository trees, and active pipeline statuses into a
  single non-blocking payload, eliminating waterfall polling.
- **Ecosystem Sidecar Interoperability (`/api/gui/ecosystem`)**: Probes the
  `lemgendary-datasets` sidecar (port 8100) and the `lemgendary-training-suite`
  sidecar (port 8200) one after the other in the thread pool, each with a 1.5 s
  timeout, and reports their health next to the env manager itself (port 8000)
  for the `lemgendary-ai-studio-gui` status bar.
- **Service Control (`/api/services/{service_id}/start` and `/stop`)**: Starts
  and stops the sidecar daemons. In v16.9.67, process termination is hardened
  via a two-tier strategy: recording the background process PID to
  `server.pid` upon launch, and executing Windows netstat parsing that
  recognizes both explicit IP bindings (`127.0.0.1`, `0.0.0.0`, `[::]`) and
  listening wildcard tokens (`*:*`, `:0`) to terminate stubborn lingering
  processes reliably. Furthermore, test environments enforce isolation
  via `LEM_DISABLE_SIDECAR_AUTORUN=1`.
- **Governance & Maintenance Endpoints (`/api/hooks/install`, `/api/clean`)**:
  Provides programmatic endpoints for ecosystem-wide Git hook installation and
  recursive temporary cache/staging artifact purges with space recovery
  telemetry.
- **API Contract**: `openapi.json` is regenerated from the running app and
  includes `run-step`, `hooks/install`, `ping`, `update/status`, `shutdown` and
  `bug-report`, so Tauri Rust and TypeScript clients can be generated from it.

### 6.4 Background Update Jobs

`POST /api/update` no longer runs the upgrade inside the request handler. A dry
run returns the plan. A real run starts a background job
(`env_manager/update_jobs.py`, `UpdateJobManager`) and returns at once with
`status: "accepted"` and a `job_id`; progress is streamed over `/ws/log` and
`GET /api/update/status` returns the current or last job. The `project` field
limits the plan to one project, and an unknown project returns `404`.

Updates are mutually exclusive with each other and with the pipeline. With $U$
the running update job and $\Pi$ the running pipeline:

$$
\text{Admit}(\text{req}) = \lnot U \land \lnot \Pi, \qquad \text{otherwise HTTP
} 409
$$

A runner failure is logged and recorded as `status: "failed"` with an `error`,
and the lock is released.

### 6.5 Security Model

The sidecar binds to `127.0.0.1` by default and shares one security contract
with the other two sidecars and the GUI:

- **Origin Guard** (`env_manager/security.py`): a request whose `Origin` header
  is not an AI Studio GUI origin (`tauri://localhost`, `http://tauri.localhost`,
  `https://tauri.localhost`, `http://localhost:1420`, `http://127.0.0.1:1420`)
  gets `403`, and WebSocket handshakes from a foreign origin are refused.
- **Client Header**: browser requests that use `POST`, `PUT`, `PATCH` or
  `DELETE` must send `X-LemGendary-Client: ai-studio-gui`. The custom header
  forces a CORS preflight, which blocks cross-site form posts. Requests without
  an `Origin` (CLI, scripts, tests) are not affected.
- **Closed CORS**: the CORS policy lists the same origins, explicit methods and
  headers, and `allow_credentials=False` instead of `allow_origins=["*"]`.
- **Masked Secrets** (`env_manager/secrets_vault.py`): `GET /api/secrets`
  returns only `has_value` and a `value_hint` (last 4 characters, empty for
  values shorter than 8) and has no side effects. `POST /api/secrets` is
  write-only: an empty value keeps the stored one, a non-empty value replaces
  it. The vault file `.secrets.yaml` is written atomically with a backup. Kaggle
  credentials are propagated only to repositories that read them, without
  invented usernames, and the result is reported in `propagation` (`written`,
  `skipped`, `failed`). All secret files are ignored by git.

### 6.6 Bug Report Endpoint

`POST /api/bug-report` receives the report built by the AI Studio GUI. The
server sends no email and stores no SMTP credentials:

- **Validation**: a Pydantic model checks the multipart fields (`email`,
  `module`, a description of 50 to 10,000 characters, `app_version`,
  `current_tab`). Uploads are checked by count, size, declared type and leading
  bytes: up to 5 screenshots (PNG or WebP, 5 MB each), an optional telemetry CSV
  (2 MB) and an optional recording (WebM or MP4, 50 MB), at most 80 MB in total.
  Errors return `422` or `413` with the field in `loc`.
- **Archive**: `bug_report_<UTC timestamp>_<id>.zip` holds `report.csv` (written
  with the `csv` module; cells that look like formulas are prefixed with `'`),
  the telemetry file and the uploads. It is saved to `bug-reports/` at the
  workspace root, outside every repository.
- **Hand-off**: a `PlatformAdapter` protocol opens the mail client (`mailto:`
  with recipient and subject) and reveals the archive in the file manager. The
  response returns the archive's path relative to the workspace root and
  whether each step worked; the request succeeds even when the mail client
  cannot be opened, because the archive is saved.
- **Configuration**: recipient, subject, reports folder and limits are defined
  in one place, `env_manager/bug_report/config.py` (`BugReportSettings`).

### 6.7 Ecosystem Registry (ecosystem.json)

Since v16.9.49 the facts that every project shares are defined in one file,
`lemgendary-env-manager/ecosystem/ecosystem.json`, described by
`ecosystem/ecosystem.schema.json` (JSON Schema draft 2020-12). Edit the file,
not the code:

- **Services** (`services[]`): id, aliases, project folder, port, health,
  liveness and WebSocket paths, app import and log folder of each sidecar. The
  sidecar ports, URLs and the `lem-env serve` defaults are read from here.
- **Projects** (`projects[]`): folder, display name, kind (`python`, `node`,
  `asset`), whether the project is managed, validated or git-hooked, its
  upgrade order and manifests. Project discovery, the validation targets, the
  upgrade order and the manifest sync targets are derived from this list.
- **Pipeline steps** (`pipeline_steps[]`): number, id, name and descriptions of
  the seven pipeline steps (Section 6).
- **Identity** (`identity`): documentation URL, Kaggle owner, bind host and,
  since v16.9.85, `github_url` (the clone URL base,
  `github_repo_url(folder)`).
- **Kaggle** (`kaggle`, v16.9.85): `collaborators` (merged into every model's
  editor binding), `default_accelerator` (`gpu-t4x2`), `accelerators[]` (`id`,
  `label`, `kind`, `machine_shape`: `cpu` without a shape, `gpu-t4x2` on
  `NvidiaTeslaT4`, `tpu-v5e8` on `TpuV5E8`) and `retired_machine_shapes`
  (P100 and the older TPU shapes, never offered). `KaggleSettings` checks
  unique ids, a listed default, no retired shape and a null shape exactly for
  CPU.

Python code in this repository reads the file through
`env_manager.ecosystem.ecosystem()` (parsed once and cached;
`LEMGENDARY_ECOSYSTEM_FILE` overrides the location). `GET /api/ecosystem`
returns it as a typed `Ecosystem` response. The other projects read the same
file:

- The LemGendary Dataset Compiler Suite and the LemGendary Model Training Suite
  each have one loader, `core/ecosystem.py` and `training/ecosystem.py`, that
  locates the file in the workspace (`LEMGENDARY_WORKSPACE_ROOT` or the parent
  folder) and provides ports, project folders and the Kaggle owner.
- The LemGendary AI Studio GUI copies it to the committed snapshot
  `src/generated/ecosystem.json` before `dev` and `build`
  (`npm run sync:ecosystem`; `npm run check:ecosystem` fails when the snapshot
  differs) and derives its sidecar ports and project folders from the snapshot.
- The LemGendary AI Documentation Hub audit checks that the model ids of
  `canonical_capabilities.json` equal the training registry keys and that its
  ports equal the service ports in the file.

The validation gate `ecosystem_ssot` (error severity since v16.9.52; findings
fail validation) reports drift: in code,
configuration and tests a literal service port, the Kaggle owner, the
documentation URL or a list of three or more project folders is a finding (test
fixtures are allowed); in Markdown, HTML and the registries the values may be
written out but must equal the file. Since v16.9.59 a service port is a finding
wherever it stands as its own number token (template literals, calls,
assignments, list items); longer numbers, hex values, colours, versions,
decimals, negative numbers and units pass. It also checks that the GUI snapshot
equals the source, that the GUI Content Security Policy ports equal the service
ports, that the GUI pipeline steps match the file, that the GUI `ProjectHealth`
type matches the OpenAPI schema and that the GUI `package.json` equals its
central manifest (`check_npm_manifest`, finding `ssot_npm_manifest`; the
`version` field is not compared since v16.9.60).

### 6.8 Kaggle Credentials, Changelog Scope & Runtime Contract (v16.9.81 to v16.9.85)

- **One Kaggle credential loader** (`env_manager/kaggle_auth/credentials.py`,
  v16.9.84): `load_kaggle_credential(vault_records, environ, config_dir)`
  resolves the vault default first, then `KAGGLE_API_TOKEN` (or
  `KAGGLE_USERNAME` / `KAGGLE_KEY`), then `~/.kaggle/access_token`; a
  `KaggleCredential` never shows its token in `repr`, and nothing mutates
  `os.environ`. `KaggleCliConfigWriter` writes a `KGAT_` API token to
  `~/.kaggle/access_token` (0600) and removes a `kaggle.json` that holds such
  a token as its legacy `key` (the Kaggle CLI answers 401); a legacy key still
  goes to `kaggle.json` with its username. The unused `.kaggle_token`
  repository list is gone; `.kaggle_users` is read only to seed a new vault.
- **Changelog scope** (`env_manager/validation/domain/changelog_scope.py`,
  v16.9.83): the single definition of which changed paths need a README
  changelog entry. Docs (Markdown other than `README.md`, a top-level
  `docs/`), tests (`tests` / `test` / `__tests__` folders, `test_*.py`,
  `*_test.py`, `conftest.py`, `*.test.*`, `*.spec.*`) and tooling (`.github`,
  `.githooks`, `.husky`, `.vscode`, lint, format and git config files) are
  exempt; everything else, including `pyproject.toml`, `package.json`,
  requirements and runtime config, needs an entry. A docs-only or tooling-only
  last commit no longer fails the domain gate.
- **MDS dropped** (v16.9.81): `requirements/runtime_env.yaml` (contract 1.2)
  no longer lists `mosaicml-streaming`; MDS dataset compilation is
  discontinued.

---

## 7. Unified Models Registry

The environment framework interfaces directly with the LemGendary Unified Models
Registry and Dataset Compilers. By maintaining environment alignment across all
sibling repositories, models trained within `lemgendary-training-suite` can be
exported directly into target deployment runtimes without runtime DLL mismatches
or missing operator kernels.

$$
\forall p \in \mathcal{P}, \quad \text{Compat}(\text{PythonVersion}(p),
\text{ONNXRuntime}(p)) = \text{True}
$$

This structural invariant ensures that inference runtimes, MetaTrader bridges,
and dataset compilers operate in total environmental equilibrium.

---

## 8. Conclusion

The LemGendary Environment Manager reduces environmental divergence across the
machine learning development lifecycle. A standalone Python engine with a CLI
and a local sidecar provides driver-aware PyTorch index selection, one-way
manifest synchronization that refuses downgrades, fail-closed upgrade
classification, a non-destructive install pipeline, background update jobs and
real-time telemetry. The sidecar accepts browser requests only from the AI
Studio GUI, keeps secrets write-only and turns bug reports into local archives
for the operator's mail client, giving model training, dataset compilation and
the desktop GUI one reproducible foundation.

---

## Companion Documentation

Operational procedures, command-line reference, API specifications, and
troubleshooting guides are maintained in separate documents to keep this
whitepaper focused on architectural design and comparative analysis:

- [Master CLI Operations Manual (Markdown)](./MANUAL_CLI.md)
- [Master CLI Operations Manual (HTML)](../papers/cli-manual.html)
- [Master REST & WebSocket API Specification (Markdown)](./MANUAL_API.md)
- [Master REST & WebSocket API Specification (HTML)](../papers/api-manual.html)
