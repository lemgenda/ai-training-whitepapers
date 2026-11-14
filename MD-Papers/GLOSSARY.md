# LemGendary Ecosystem: Canonical Glossary & Terminology Specification

## Category 12 GLOSSARY | LemGendary AI Documentation Hub

**Parent Hub**: [Master Ecosystem Architecture](./ECOSYSTEM_ARCHITECTURE.md)

**Version**: `v16.9.68-STABLE` (LemGendary AI Documentation Hub) · **Last
audited**: 2026-11-12

---

## Table of Contents

- [1. Abstract](#1-abstract)
- [2. Core Taxonomy: Dataset vs. Manifold](#2-core-taxonomy-dataset-vs-manifold)
  - [2.1 Dataset (Raw Set)](#21-dataset-raw-set)
  - [2.2 Manifold (Compiled Training
    Manifold)](#22-manifold-compiled-training-manifold)
- [3. Compiler & Storage Primitives](#3-compiler--storage-primitives)
  - [3.9 Task Taxonomy](#39-task-taxonomy)
- [4. Model Training Suite &
  Optimization](#4-model-training-suite--optimization)
  - [4.5 Ratchet Violation](#45-ratchet-violation)
  - [4.6 Epoch Budget](#46-epoch-budget)
  - [4.7 Stochastic Weight Averaging (SWA)](#47-stochastic-weight-averaging-swa)
  - [4.8 FID Provenance Ledger](#48-fid-provenance-ledger)
- [5. Training Pathology & Diagnostics](#5-training-pathology--diagnostics)
- [6. Environment & Infrastructure](#6-environment--infrastructure)
  - [6.3 Origin Guard](#63-origin-guard)
  - [6.4 Client Header](#64-client-header)
- [7. Bug Reporting](#7-bug-reporting)
  - [7.1 Bug Report Tool](#71-bug-report-tool)
  - [7.2 Bug Report Archive](#72-bug-report-archive)
  - [7.3 Screenshot Annotator](#73-screenshot-annotator)
  - [7.4 Telemetry CSV](#74-telemetry-csv)
- [8. Authoritative "Do Not Confuse With"
  Matrix](#8-authoritative-do-not-confuse-with-matrix)

---

## 1. Abstract

This specification is the single source of truth (SSOT) for the terminology,
mathematical primitives, architectural definitions and system invariants used
across the LemGendary AI Ecosystem. It removes semantic ambiguity across
machine learning pipelines, desktop operators, agentic reasoning models and
technical documentation. Every entry carries a strict operational definition
and cross-reference boundaries.

---

## 2. Core Taxonomy: Dataset vs. Manifold

The distinction between a raw dataset and a compiled manifold is an inviolable
architectural invariant across the ecosystem:

### 2.1 Dataset (Raw Set)

- **Definition**: A collection of uncurated, heterogeneous source data from
  external repositories (for example HuggingFace, Kaggle, GitHub, Google Drive
  or local filesystem drops).
- **Location**: Stored strictly under `raw-sets/<source-name>/` or in
  ephemeral fetch caches.
- **Characteristics**:
  - Unstandardized file formats (loose JPEGs, PNGs, BMPs, TARs, ZIPs).
  - Arbitrary spatial resolutions, varying aspect ratios and uncalibrated
    colour spaces.
  - Incomplete, missing or malformed label structures.
  - Mutable: raw files may be updated, pruned or re-downloaded from upstream
    remotes.
- **Usage**: Raw datasets are **never** ingested directly by the LemGendary
  Model Training Suite.

### 2.2 Manifold (Compiled Training Manifold)

- **Definition**: A deterministic, vetted, hardware-aligned data
  representation compiled specifically for machine learning ingestion.
- **Location**: Stored in the LemGendary Compiled Manifolds Repo
  (`../LemGendaryDatasets/LemGendized<Name>/`).
- **Characteristics**:
  - **Unified Invariants**: Strict resolution floors ($\ge 224\text{px}$
    restoration, $\ge 512\text{px}$ diffusion), standardized WebP encoding
    ($q=92$ images, $q=95$ targets, lossless masks) and deterministic split
    assignments (`train`, `val`, `test`).
  - **Immutable Provenance**: Every manifold contains self-documenting
    manifests: `dataset_info.yaml`, `index.json`, `classes.txt` and
    `manifold_registry.db`.
  - **Zero Redundancy**: Identity image targets use physical NTFS/POSIX
    hardlink deduplication (`os.link`), so no cluster space is wasted.
  - **High-Throughput Alignment**: Built for $\mathcal{O}(1)$ flat directory
    indexation and optional concurrent multi-container sharding (LitData,
    WebDataset, Parquet).

---

## 3. Compiler & Storage Primitives

### 3.1 $\mathcal{O}(1)$ Physical Skip-Indexing

A high-velocity filesystem technique where a single flat `os.scandir`
traversal during pipeline initialization populates an in-memory string hash
set ($\mathcal{S}_{\text{disk}}$) of existing files. Verifying whether a sample
has already been compiled executes in $\mathcal{O}(1)$ average-case dictionary
lookup time, bypassing recursive $\mathcal{O}(N \cdot d)$ disk seek overhead.

### 3.2 Zero-IPC ThreadPool

An execution model utilizing Python's `ThreadPoolExecutor` within a single
virtual memory space for pure I/O operations (image decoding, transcoding, and
disk writing). By executing within a shared memory space, it avoids
inter-process serialization and pickling overhead (measured near-zero IPC
serialization overhead relative to multi-process queue IPC under standard
Python I/O worker benchmarks).

### 3.3 NTFS Cluster Slack Space Recovery

Standard NTFS filesystems allocate physical disk space in
$4,096\text{-byte}$ clusters. Loose sliding-window arrays waste up to
$4\text{ KB}$ per file in cluster slack. The compiler's columnar Parquet +
Zstandard architecture aggregates temporal records into contiguous row groups,
achieving compression ratios up to $99.3\%$ on highly repetitive tick-level
financial datasets (measured against raw uncompressed CSV dumps in the
MetaTrader 5 Forex benchmark suite).

### 3.4 Hardlink Deduplication (Identity Mapping)

An optimization for image restoration where the clean ground-truth target
matches the degraded input. Instead of duplicating multi-megabyte image bytes
across directories, the compiler issues NTFS hardlinks referencing identical
physical disk clusters, saving hundreds of gigabytes per manifold.

### 3.5 Lossless Mask Transcoding

A format constraint requiring all segmentation masks (`masks/`) to be encoded
strictly via WebP lossless compression. Lossy compression introduces subtle
edge-quantization artifacts that corrupt discrete integer class labels.

### 3.6 Two-Tier Modernization Resumption

An architectural design in `tools/modernize_manifold.py` combining high-level
manifest validation (`dataset_info.yaml` + `index.json`) with file-level delta
verification. Interrupted modernization runs bypass already-transcoded `.webp`
images and metadata in seconds, resuming only uncompleted files.

### 3.7 WebDataset `.data` Shard Convention

The canonical shard file extension for all WebDataset archives in the
LemGendary ecosystem. Shards are valid POSIX `ustar` tar archives internally,
but use `.data` instead of `.tar` to bypass Kaggle backend archive-sniffing
heuristics that would otherwise recursively expand multi-gigabyte containers
into millions of loose files, causing inode exhaustion and attachment latency
measured in hours. The LemGendary Model Training Suite discovers and decodes
`.data` and `.tar` shards transparently via POSIX magic byte inspection.

### 3.8 Dynamic CUDA Index Selection

A runtime algorithm implemented in
`env_manager.system_probe.select_cuda_torch_index()` that reads the NVIDIA
driver version and returns the newest compatible PyTorch wheel index (`cu134`,
then `cu126`, then `cu121`, then `cu118`). It eliminates hard-coded CUDA index
pins and ensures the correct build is installed regardless of driver version.

### 3.9 Task Taxonomy

The file `lemgendary-datasets/task_taxonomy.json` (schema
`task_taxonomy.schema.json`), the single source of task ids such as `pose`,
`segmentation`, `restoration` or `detection`. For each task it gives the split
folder the task adds (`layout_dir`), the default label and mask strategies and
the name patterns of the fallback heuristic. Every entry in `unified_data.yaml`
names its `task`; an entry with `task_confirmed: false` waits for the owner to
confirm it. The compiler writes the task id as `task_type` into each
manifold's `dataset_info.yaml`, which the LemGendary Model Training Suite reads.

---

## 4. Model Training Suite & Optimization

### 4.1 Spatial Resolution Ladder

A multi-stage curriculum learning schedule in which image resolution scales up
during training (for example $256\text{px} \to 384\text{px} \to 512\text{px}
\to 640\text{px}$). Early epochs capture global structure at high batch
velocity before later rungs fine-tune high-frequency detail.

### 4.2 Nuclear-Hardened Architecture

A resilience design pattern in `lemgendary-training-suite` that combines
validation across hardware backends, dynamic gradient scaling, automated
checkpoint verification and zero-suppression error telemetry.

### 4.3 Directional Accuracy (DA)

The primary evaluation metric for financial time-series forecasting: the
percentage of time steps where the predicted sign of the price delta matches
the actual market trajectory:

$$
\text{DA} = \frac{1}{N} \sum_{t=1}^{N} \mathbb{I}\left( \text{sgn}(\hat{y}_t -
y_{t-1}) = \text{sgn}(y_t - y_{t-1}) \right) \times 100\%
$$

### 4.4 Earth Mover's Distance (EMD) Loss

The objective function for probabilistic aesthetic quality distributions
(NIMA). It penalizes misclassifications in proportion to the distance between
ordinal rating bins ($1\text{ to }10$):

$$
\text{EMD}(p, \hat{p}) = \left( \frac{1}{K} \sum_{k=1}^{K} \left|
\text{CDF}_p(k) - \text{CDF}_{\hat{p}}(k) \right|^r \right)^{1/r}
$$

### 4.5 Ratchet Violation

The error raised when a curriculum transition would step backwards.
`RatchetViolation` (a `ValueError` in `training/ratchet.py`) enforces the
Monotonic Ratchet pair rule: resolution never decreases, and within one
resolution step the data fraction never decreases; when the resolution steps
up, the fraction may reset. Every governor transition goes through
`SmartTrainingGovernor._commit_rung`, which raises `RatchetViolation` instead
of applying a backward step. A transition from $(r_t, f_t)$ to
$(r_{t+1}, f_{t+1})$ is allowed only if:

$$
r_{t+1} \ge r_t \land \left(r_{t+1} = r_t \Rightarrow f_{t+1} \ge f_t\right)
$$

On regression the governor holds the rung and cools the learning rate; it
never recoils fraction or resolution.

### 4.6 Epoch Budget

The bounded number of epochs a training run may use. After every epoch,
`EpochBudgetPolicy` (`training/epoch_budget.py`) decides whether to continue,
extend or stop, and records the stop reason (`converged`, `early_stop`,
`budget_reached` or `extension_limit`). Extensions are opt-in through the
`training_budget` section of `config.yaml` (`extension_epochs`,
`max_extension_epochs`; the shipped ceiling is 0, which makes the configured
budget a hard cap). With budget $E$ and extension ceiling $E_{\max}$:

$$
E_{\text{trained}} \le E + E_{\max}
$$

### 4.7 Stochastic Weight Averaging (SWA)

A running mean of the model weights over the last epochs of a run, computed
with `torch.optim.swa_utils` (`AveragedModel`, optional `SWALR`, `update_bn`).
In the LemGendary Model Training Suite it is set in the `swa` section of
`config.yaml` and is **off by default**. The averaged weights are written as
`checkpoints/vault_swa.pth`, an ingredient for the Pareto Model Soup; they
never move the curriculum rungs. Not to be confused with Mini-SWA or
Metric-Specific SWA (MS-SWA), which are not implemented.

### 4.8 FID Provenance Ledger

The append-only file `LemGendaryModels/<model>/fid_provenance.csv` written by
`python -m training.fid_reeval`. Each row records where a FID value came from:
`unverified` rows mark `metrics.csv` values rewritten by the removed
`tools/recalibrate_fid.py`; `reevaluated` rows hold a FID re-measured from a
checkpoint with `feature=2048` and chunks of at most two, with the image count
and the checkpoint SHA-256. `metrics.csv` itself is never rewritten.

---

## 5. Training Pathology & Diagnostics

### 5.1 Pathology Reasoning Trace

A structured diagnostic narrative generated from empirical training failure
modes. It models the causal chain: Observational Symptom $\to$ Diagnostic
Telemetry $\to$ Root Cause Analysis $\to$ Mitigation Strategy.

### 5.2 Latent Disconnect

A training pathology where the restoration backbone converges to a trivial
spatial average (for example solid grey or blur) while the loss curves report
apparent convergence, which indicates a loss-term imbalance or improper
normalization.

### 5.3 Catastrophic Gradient Collapse

An unrecoverable parameter destabilization, typically caused by exploding
gradient spikes ($\|\mathbf{g}\| > 10^4$) or unhandled NaN inputs, that needs
an automated checkpoint rewind and a learning rate penalty.

---

## 6. Environment & Infrastructure

### 6.1 Deterministic Environment Reconciliation

The automated synchronization of local `.venv` packages against central
manifests (`requirements-*.txt`). It identifies version drift and resolves
transitive dependencies without polluting the global Python. Code compliance
validation runs through **Ruff** (`ruff>=0.9.0`), which replaced the former
Pylint and astroid toolchain.

### 6.2 Sidecar REST Daemon

An asynchronous FastAPI service on a dedicated local port (`8000` for the
LemGendary Environment Manager, `8100` for the LemGendary Dataset Compiler
Suite and `8200` for the LemGendary Model Training Suite). Each sidecar binds
to `127.0.0.1` and provides headless API access, hardware health telemetry and
WebSocket log broadcasting.

### 6.3 Origin Guard

The browser-origin middleware shared by all three sidecars
(`env_manager/security.py`, `api/security.py`,
`training/server/security.py`). Only the LemGendary AI Studio GUI may call a
sidecar from a browser. A request whose `Origin` header is not in the
allow-list (`tauri://localhost`, `http://tauri.localhost`,
`https://tauri.localhost`, `http://localhost:1420`, `http://127.0.0.1:1420`) is
refused with HTTP 403, and WebSocket handshakes follow the same rule. Requests
without an `Origin` header (CLI, scripts, tests) are allowed.

### 6.4 Client Header

The custom request header `X-LemGendary-Client: ai-studio-gui`. A browser
request (one that carries `Origin`) using `POST`, `PUT`, `PATCH` or `DELETE`
must send it, or the Origin Guard refuses it. Because a custom header forces a
CORS preflight, other web pages on the same machine cannot submit cross-site
form posts to a sidecar.

---

## 7. Bug Reporting

### 7.1 Bug Report Tool

The LemGendary AI Studio GUI feature behind the header button
`header-btn-report-issue`. The user enters an email address, the module, and a
description of at least 50 characters, and may attach up to 5 screenshots and
the Telemetry CSV. The GUI posts the form as `multipart/form-data` to
`POST /api/bug-report` on the LemGendary Environment Manager (port `8000`),
which saves a Bug Report Archive and opens the user's own mail client through
a `mailto:` link. No SMTP password ships with the application. In the desktop
app on Windows the user can also record the app window (H.264 MP4, up to 60 s,
854x480 at 24 fps) and attach it as `recording.mp4`; other platforms report
that recording is not supported yet.

### 7.2 Bug Report Archive

The ZIP file that `POST /api/bug-report` writes under `bug-reports/` in the
workspace root. It holds `report.csv` (one row: timestamp, report ID, email,
module, current tab, app version, description and attachment flags), the
screenshots (`screenshot_N.png` or `.webp`, at most 5, 5 MB each), the
optional `telemetry.csv` (at most 2 MB) and an optional recording (`.webm` or
`.mp4`, at most 50 MB). The whole report is limited to
80 MB. A `mailto:` link cannot carry files, so the user attaches the archive to
the prepared message by hand.

### 7.3 Screenshot Annotator

The GUI dialog (`ScreenshotAnnotator.tsx`) that captures the application
window and lets the user draw one highlight rectangle over the problem area
before the image is attached to a bug report.

### 7.4 Telemetry CSV

The pipeline event log that the GUI attaches to a bug report as
`telemetry.csv` unless the user clears "Attach telemetry". It is RFC 4180 CSV
with CRLF line breaks and the columns `timestamp`, `status`, `source` and
`message`; `source` is the sidecar origin of the event when known, otherwise
its step name.

---

## 8. Authoritative "Do Not Confuse With" Matrix

- **Dataset vs. Manifold**: Datasets are raw, mutable, heterogeneous source
  drops; Manifolds are compiled, deterministic, immutable, hardware-aligned
  training data.
- **Reconciliation vs. Clean Install**: Reconciliation inspects and patches
  package drift in place; Clean Install removes `.venv` and rebuilds the
  toolchain from the first hardware probing stage.
- **Container Format vs. Directory Layout**: Container formats (LitData,
  WebDataset `.data`) pack data into contiguous shards for cloud streaming; a
  directory layout preserves the raw filesystem hierarchy and hardlink
  deduplication. MosaicML MDS is deprecated; all production shards are
  WebDataset `.data` archives.
- **Hardlink Deduplication vs. Perceptual Deduplication**: Hardlink
  deduplication maps identical target files to the same physical cluster;
  perceptual deduplication flags visually similar images through pHash/dHash
  Hamming distances.
- **Image Transcoding vs. Synthetic Degradation**: Transcoding converts image
  encodings (for example PNG $\to$ WebP $q=92$) and preserves visual fidelity;
  degradation corrupts images with blur, noise or haze kernels to generate
  paired training samples.
- **Sidecar API vs. CLI Tool**: A sidecar is a background daemon that streams
  WebSocket events to the GUI; a CLI is a direct local command that runs in
  process or delegates to the sidecar.
- **Origin Guard vs. Client Header**: The Origin Guard decides which browser
  origins may call a sidecar at all; the Client Header is the extra proof a
  browser request needs for state-changing methods.
- **Bug Report Archive vs. Telemetry CSV**: The archive is the whole ZIP saved
  on disk; the Telemetry CSV is one optional file inside it.
- **Ratchet Violation vs. Epoch Budget stop**: A Ratchet Violation rejects a
  backward curriculum step and is a guard error; an Epoch Budget stop is a
  normal end of training with a recorded reason.
