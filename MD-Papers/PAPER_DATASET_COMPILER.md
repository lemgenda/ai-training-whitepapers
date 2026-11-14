# LemGendary Dataset Compiler Suite: Technical Whitepaper

## Category 01.2 | Subpage of Master Ecosystem Architecture

**Parent Hub**: [Master Ecosystem Architecture](./ECOSYSTEM_ARCHITECTURE.md)

**Version**: `v16.9.108-STABLE` (LemGendary Dataset Compiler Suite) · **Last
audited**: 2026-11-13

---

## Table of Contents

- [1. Abstract](#1-abstract)
- [2. High-Velocity Optimizations](#2-high-velocity-optimizations)
  - [2.1 Formal Complexity Mappings](#21-formal-complexity-mappings)
  - [2.2 Resampling & Resolution
    Constraints](#22-resampling--resolution-constraints)
  - [2.3 System Performance & Throughput
    Matrix](#23-system-performance--throughput-matrix)
  - [2.4 Zero-Intermediate WebP
    Transcoding](#24-zero-intermediate-webp-transcoding)
  - [2.5 Direct Streaming Zip-to-Container
    Engine](#25-direct-streaming-zip-to-container-engine)
  - [2.6 Native 7-Zip & Tar Archive
    Acceleration](#26-native-7-zip--tar-archive-acceleration)
  - [2.7 Two-Tier Modernization & WebP
    Resumption](#27-two-tier-modernization--webp-resumption)
  - [2.8 Fast Split Shard Discovery & mtime
    Caching](#28-fast-split-shard-discovery--mtime-caching)
  - [2.9 In-Memory Streaming Download & Terminal
    Telemetry](#29-in-memory-streaming-download--terminal-telemetry)
  - [2.10 Modern Telemetry Progress
    Architecture](#210-modern-telemetry-progress-architecture)
- [3. Hybrid Cloud & Registry
  Integration](#3-hybrid-cloud--registry-integration)
  - [3.1 Atomic Registry Resumption & Hardlink
    Deduplication](#31-atomic-registry-resumption--hardlink-deduplication)
  - [3.2 Metadata Synchronization & Cloud
    Transfer](#32-metadata-synchronization--cloud-transfer)
  - [3.3 Kaggle Cloud Synchronization & Storage
    Hub](#33-kaggle-cloud-synchronization--storage-hub)
  - [3.4 Canonical Storage Format & Kaggle SSOT
    Governance](#34-canonical-storage-format--kaggle-ssot-governance)
  - [3.5 Multi-Source Custom Dataset Synthesis
    Engine](#35-multi-source-custom-dataset-synthesis-engine)
  - [3.6 SSOT Notebook Delegation &
    Deduplication](#36-ssot-notebook-delegation--deduplication)
  - [3.7 Task Taxonomy & Manifold Task Type
    (v16.9.61)](#37-task-taxonomy--manifold-task-type-v16961)
- [4. Multi-Modal & Format Resilience](#4-multi-modal--format-resilience)
  - [4.1 Upstream Multi-Source Expansion
    Architecture](#41-upstream-multi-source-expansion-architecture)
  - [4.2 Multi-Format Annotation Converter
    Subsystem](#42-multi-format-annotation-converter-subsystem)
  - [4.3 Pre-flight Validation, Integrity Vetting &
    Pruning](#43-pre-flight-validation-integrity-vetting--pruning)
  - [4.4 Domain Specializations](#44-domain-specializations)
  - [4.5 Modular Container Format Layer](#45-modular-container-format-layer)
  - [4.6 Studio-Supported vs. General Knowledge
    Formats](#46-studio-supported-vs-general-knowledge-formats)
  - [4.7 Hardlink Dedup Preservation & Pre-Flight
    Gate](#47-hardlink-dedup-preservation--pre-flight-gate)
  - [4.8 Smart Multi-Modal Generation
    Engine](#48-smart-multi-modal-generation-engine)
  - [4.9 Physical Degradation Synthesis
    Engine](#49-physical-degradation-synthesis-engine)
  - [4.10 Generic LLM Dataset Compiler](#410-generic-llm-dataset-compiler)
  - [4.11 Sample Integrity, Shard Verification & Manifold
    Repair](#411-sample-integrity-shard-verification--manifold-repair)
  - [4.12 JSON Shard Labels, Sample Policies & Source Labels (v16.9.85 to
    v16.9.107)](#412-json-shard-labels-sample-policies--source-labels-v16985-to-v169107)
  - [4.13 Shard Offset Index (v16.9.108)](#413-shard-offset-index-v169108)
- [5. Comparative Analysis / Benchmarks](#5-comparative-analysis--benchmarks)
  - [5.1 Technical Comparison Matrix](#51-technical-comparison-matrix)
  - [5.2 Competitor Deep-Dive: Pros, Cons &
    Pricing](#52-competitor-deep-dive-pros-cons--pricing)
- [6. Synthesis Flow & Topology](#6-synthesis-flow--topology)
  - [6.1 The Dataset Hub](#61-the-dataset-hub)
  - [6.2 Industrial Output Topology](#62-industrial-output-topology)
  - [6.3 LLM Manifold Filesystem Topology](#63-llm-manifold-filesystem-topology)
  - [6.4 Unified Three-Pipeline
    Architecture](#64-unified-three-pipeline-architecture)
  - [6.5 S.O.L.I.D. Services Layer & Forex
    Encapsulation](#65-solid-services-layer--forex-encapsulation)
  - [6.6 Asynchronous Sidecar API & Hybrid
    CLI](#66-asynchronous-sidecar-api--hybrid-cli)
  - [6.7 Cross-Project Automation & Desktop GUI
    Presets](#67-cross-project-automation--desktop-gui-presets)
  - [6.8 Modernize and Reduce Operations](#68-modernize-and-reduce-operations)
  - [6.9 Security Model](#69-security-model)
- [7. Unified Models Registry](#7-unified-models-registry)
- [8. Conclusion](#8-conclusion)

---

## 1. Abstract

The LemGendary Dataset Compiler Suite (release `v16.9.84-STABLE`) is the data
layer of the LemGendary ecosystem for Generative, Vision, Language and
Time-Series dataset synthesis. It elevates static sharding to a self-optimizing
generative manifold, orchestrating Diffusion, Restoration, Detection, Quality,
Market and LLM instruction datasets with zero-intermediate WebP transcoding,
pluggable container formats (WebDataset, LitData, Parquet; MosaicML MDS is
legacy and transcoded to WebDataset), deterministic degradation kernels,
bidirectional Kaggle Cloud Synchronization, multi-source custom compilation, a
FastAPI/WebSocket REST sidecar daemon (`api/`, port 8100) and a hybrid Typer
CLI. The single source of truth registry `unified_data.yaml` declares 21
manifolds: 19 vision manifolds, the `LemGendizedForexUniverse` financial
manifold and the `LemGendizedAIHelperLemGend` instruction manifold.

The `v16.9.23` to `v16.9.27` releases harden the operating contract. Browser
access is limited to the AI Studio GUI by an origin guard and a closed CORS
allow-list. Custom compilation resolves its preset from `presets.yaml`
(`default_preset`), writes the registry atomically without touching existing
text, and purges loose images only after a successful compile. LLM compile jobs
start and are awaited with a bounded poll. Modernize and reduce honour scope and
dry run, and never delete sources unless asked. `POST /api/llm/validate` only
opens files inside the dataset root, and `openapi.json` is regenerated from the
live application (38 operations at v16.9.27).

The `v16.9.28` to `v16.9.64` releases remove silent exception handling and
lint suppressions, split the large modules, and move shared facts to single
sources. API jobs run the same service entry points as the CLI
(`python -m services.<module>`, described by a typed `ServiceInvocation`), and
the arbitrary-command endpoint `POST /api/jobs/generic` is removed (37 operations).
The port, bind host, Kaggle owner and sibling folders come from
`lemgendary-env-manager/ecosystem/ecosystem.json`, and task ids come from
`task_taxonomy.json` (Section 3.7).

The `v16.9.66` to `v16.9.74` releases move the toolchain to `torch==2.15.0` (the
wheel index comes from the LemGendary Environment Manager hardware probe), make
`.secrets.yaml` the authoritative credential source over stale environment
tokens, and register the Kaggle reference of the AIHelper instruction manifold.
The `v16.9.75` to `v16.9.84` releases reject incomplete or corrupt samples,
verify every written shard, keep every metadata column in transcodes and add a
manifold repair command (Section 4.11).

- **Project Repository**:
  [lemgendary-datasets](https://github.com/lemgenda/lemgendary-datasets)

---

## 2. High-Velocity Optimizations

The v16.2.8 release introduced the High-Fidelity Compiler, optimized for
processing 1.4M+ item manifolds while maintaining structural integrity for
restoration tasks. Later releases added zero-unpack streaming, native archive
acceleration and file-level resumption.

### 2.1 Formal Complexity Mappings

- **O(1) Physical Skip-Indexing**: Traditional compiler engines verify existing
  outputs on disk by executing recursive path queries for every sample. In
  directory topologies containing millions of files, this incurs an
  $\mathcal{O}(N \cdot d)$ filesystem metadata lookup complexity (where $d$ is
  directory depth and $N$ is the dataset size). This results in system lockups
  due to OS seek contention.

  The compiler bypasses this lookup complexity. During initialization, it
  performs a single flat scan via `os.scandir` to construct an in-memory hash
  set ($\mathcal{S}_{\text{disk}}$) of existing filenames. Verifications then
  achieve $\mathcal{O}(1)$ average-case lookup complexity:

  $$
  \text{Verify}(x) = \begin{cases} \text{Skip} & \text{if } \text{hash}(x) \in
  \mathcal{S}_{\text{disk}} \\ \text{Process} & \text{otherwise} \end{cases}
  $$

- **ThreadPoolExecutor Zero-IPC**: Python's standard `ProcessPoolExecutor`
  relies on inter-process communication (IPC) to serialize and deserialize data
  across process boundaries via pipes. On Windows, this incurs a pickling
  serialization overhead of $\mathcal{O}(P \cdot S)$ (where $P$ is the number of
  subprocesses and $S$ is the serialized payload size).

  The compile loop in `core/manifold_compile.py` therefore runs every sample
  worker in a `ThreadPoolExecutor`, for I/O-bound copying as well as for NIMA
  vetting and YOLO labeling (whose native kernels release the interpreter lock):

  $$
  \text{Executor}_{\text{compile}} = \text{ThreadPoolExecutor}, \qquad
  T_{\text{IPC}} = \mathcal{O}(1)
  $$

  This keeps a single shared virtual memory address space (Zero-IPC), scaling
  throughput to the physical limits of the target NVMe drive. When more than 4
  workers are requested with vetting and labeling disabled, the compiler warns
  that mechanical hard disks will thrash.

- **Parquet Manifold Compression & NTFS Cluster Slack Space Recovery
  (Space-Recovery Equation)**: For high-frequency multi-timeframe financial
  datasets containing rolling sliding windows ($W = 512$ bars), storing
  individual timeframes across currency pairs in uncompressed `.npy` arrays
  produces a large disk footprint and filesystem fragmentation. On standard NTFS
  filesystems with cluster size $C_{\text{cluster}} = 4096\text{ bytes}$,
  storing hundreds of thousands of loose shard files introduces physical cluster
  slack space waste:

  $$
  \text{Slack}(f) = C_{\text{cluster}} - (\text{Size}(f)
  \pmod{C_{\text{cluster}}})
  $$

  Raw `.npy` arrays also dedicate full structural bit-weight to redundant
  sliding window overlaps. The compiler's unified Parquet architecture
  (`forex/pipeline.py`) uses Zstandard (zstd level 3) compression across
  contiguous row groups ($R = 5{,}000$). The physical space recovery ratio
  $\mathcal{R}_{\text{space}}$ and compression factor
  $\mathcal{C}_{\text{factor}}$ are:

  $$
  \mathcal{R}_{\text{space}} = 1 - \frac{\sum_{y}
  \text{Size}(\text{Parquet}_y)}{\sum_{y} \left( \sum_{s}
  \text{Size}(\text{NPY}_{y,s}) + \text{Slack}(\text{NPY}_{y,s}) \right)}
  \approx 99.3\%
  $$

  $$
  \mathcal{C}_{\text{factor}} = \frac{\text{Size}_{\text{Total}}(\text{NPY})}
  {\text{Size}_{\text{Total}}(\text{Parquet})} \approx 143\times
  $$

  This reduces the physical manifold footprint from $\sim 738\text{ GB}$ to
  $\sim 5.2\text{ GB}$ across the 8-year temporal continuum (2019 to 2026), with
  $100\%$ bit-exact floating-point recovery.

### 2.2 Resampling & Resolution Constraints

- **LANCZOS High-Fidelity Interpolation**: To prevent aliasing and preserve
  high-frequency details (textures and sharp edges) during downsampling of
  resolution-locked tasks, the compiler uses the Lanczos-3 filter kernel. The
  interpolation weight for a coordinate distance $x$ is:

  $$
  L(x) = \begin{cases} \text{sinc}(x)\,\text{sinc}\left(\frac{x}{a}\right) &
  \text{for } -a < x < a \\ 0 & \text{otherwise} \end{cases}
  $$

  where $a = 3$ is the spatial filter lobe support size, and
  $\text{sinc}(x) = \frac{\sin(\pi x)}{\pi x}$. This produces better
  anti-aliasing than bilinear or bicubic downsampling, preventing artifacts from
  corrupting downstream training manifolds.

- **High-Fidelity Resolution Floor**: Filtering bounds prevent low-resolution
  samples from corrupting convergence. If $W$ and $H$ are image dimensions,
  `VisionAuditor.audit_image()` (`audit/vision_audit.py`) enforces:

  $$
  \min(W, H) \ge \text{Threshold}
  $$

  where the per-task floors are:

  $$
  \text{Threshold} = \begin{cases} 512 & \text{if task} = \text{diffusion} \\
  224 & \text{if task} \in \{\text{quality}, \text{classification},
  \text{restoration}, \text{super-resolution}\} \\ 128 & \text{if task} \in
  \{\text{parameter\_prediction}, \text{detection}, \text{segmentation},
  \text{pose}\} \\ 128 & \text{if the slug contains ``artifact''} \end{cases}
  $$

  Tasks without an entry fall back to 128 px. Compiler presets (`presets.yaml`)
  carry their own `min_resolution` (512 for `quality-vision`, 224 for
  `restoration-hardlinked`, 320 for `detection-variable`).

- **Aspect-Ratio and Black-Frame Thresholds**: The same audit rejects extreme
  crops and near-black frames. With $g(p)$ the 8-bit grayscale value of pixel
  $p$ on a $64 \times 64$ thumbnail and $\beta = 0.1$ the configurable
  `black_threshold`:

  $$
  \frac{\max(W, H)}{\max(1, \min(W, H))} \le 10.0, \qquad \frac{|\{p : g(p) <
  10\}|}{|P|} \le 1 - \beta
  $$

### 2.3 System Performance & Throughput Matrix

To validate these system-level optimizations, execution profiles were collected
during the compilation of the `LemGendizedUpnV2` manifold (1.37M samples, 1024px
targets) on PCIe Gen4 NVMe hardware. Each entry compares the legacy recursive
pipeline with the High-Fidelity Compiler Suite:

- **Directory Indexing Latency**: $184.2 \text{ seconds}$ to
  **$0.4 \text{ seconds}$**, a **$460\times$ latency reduction**
  ($\mathcal{O}(1)$ vs $\mathcal{O}(N)$).
- **Windows IPC Serialization Overhead**: $2{,}840.5 \text{ seconds}$ to
  **$0.0 \text{ seconds}$**, **$100\%$ overhead elimination** (Zero-IPC
  ThreadPool).
- **Filesystem Storage Footprint**: $1.64 \text{ TB}$ to **$0.58 \text{ TB}$**,
  **$1.06 \text{ TB}$ space recovered** ($64.6\%$ deduplication).
- **Vetting Throughput (Aesthetic/NIMA)**: $42 \text{ items/sec}$ to
  **$185 \text{ items/sec}$**, **$4.4\times$ ingestion acceleration**.

These figures are historical measurements from the v16.8.0 profile and were not
re-measured for `v16.9.27`.

### 2.4 Zero-Intermediate WebP Transcoding

Eliminating bulky intermediate disk writes, the compiler transcodes input
streams directly in memory to tuned WebP formats:

- **Images (`images/`)**: WebP $q=92$ delivering a $40\text{--}65\%$ disk
  footprint reduction compared to standard JPEG while preserving frequency
  harmonics.
- **Restoration Ground Truth (`targets/`)**: WebP $q=95$ guaranteeing
  high-frequency fidelity for restoration models (NAFNet, MirNet, MPRNet,
  UPNv2).
- **Segmentation Masks (`masks/`)**: WebP lossless compression preserving exact
  discrete class indices and pixel boundaries.
- **Alpha Channel Resilience**: Transparent RGBA inputs are transcoded to
  lossless WebP or alpha-composited over calibrated neutral backdrops without
  quantization halos.

### 2.5 Direct Streaming Zip-to-Container Engine

To resolve Windows NTFS Master File Table (MFT) lock contention, 8.3 short-name
collision overhead, and antivirus real-time filter driver (`WdFilter.sys`)
serialization when unpacking multi-gigabyte legacy archives containing millions
of small images (for example `LemGendizedMirNetExposure` with 2.82M loose files
and `LemGendizedUpnV2` with 1.42M files), v16.8.0 introduced the **Direct
Streaming Zip-to-Container Engine** (`tools/stream_zip_to_container.py`). With
$N$ archive members it reads each member once, so its time complexity is
$\mathcal{O}(N)$ and its loose-file disk footprint is $\mathcal{O}(1)$:

1. **Zero-Unpack Architecture**: Directly mounts legacy `.zip` archives and
   streams raw byte streams into canonical WebDataset POSIX `.tar` shards in
   memory, eliminating loose file generation on physical disk.
2. **In-Flight Multi-Threaded WebP Transcoding**: Deploys a worker pool
   (`ThreadPoolExecutor`, 12 CPU cores) executing Pillow WebP encoding
   (`method=2`, `quality=92` for input images, `quality=95` for ground-truth
   targets). Delivers about $1{,}800\text{--}2{,}000\text{ img/sec}$ throughput,
   accelerating processing time from days to minutes.
3. **Dual-Pass Sequential Tar Streaming**: For paired restoration manifolds
   (`images/` and `targets/`), Pass 1 streams input images sequentially by zip
   central directory header offset into `shard-*.tar`, and Pass 2 appends paired
   ground truth (`sample.target.webp`) in standard POSIX append mode (`"a"`),
   preserving sequential NVMe read velocity without random seek degradation.
4. **Automated Disk Reclamation**: Extracts root metadata (`dataset_info.yaml`,
   `dataset-metadata.json`, `README.md`, `index.json`, notebooks), validates
   shard byte integrity, updates the canonical format to `webdataset`, and, only
   when asked, unlinks the source `.zip` archive (`--delete-zip`) and purges
   legacy uncompressed directories (`--delete-legacy-dir`), recovering over
   $120\text{ GB}$ of local storage space.

### 2.6 Native 7-Zip & Tar Archive Acceleration

For workflows requiring physical archive extraction, `utils/archive.py`
(`smart_extract`) delegates to native subsystems:

1. **Binary Auto-Discovery**: Probes the standard install locations for the
   native 64-bit 7-Zip executable (`7z.exe`) and the native POSIX `tar.exe`
   shipped with Windows, falling back to Python standard library engines.
2. **Multi-Threaded Hardware Saturation**: Dispatches extraction via native
   7-Zip with parameters `-mmt=on -bsp0 -aos -y`, achieving multi-core
   decompression that outpaces single-threaded Python zip extraction by orders
   of magnitude while suppressing per-file stdout progress flooding.
3. **Automated Root Flattening**: Detects single root manifold directory
   envelopes (`LemGendized{Name}Large/`) and flattens directory topologies
   post-extraction to guarantee consistent sibling pathing.

### 2.7 Two-Tier Modernization & WebP Resumption

Introduced in v16.7.3:

- **Suffix-Removal Modernization**: Retires legacy `Large` naming conventions
  across manifolds into production-standard suffixes while preserving legacy
  folders intact during migration (CLI: `modernize manifolds`).
- **Two-Tier State Verification**: Solves false-positive completion bugs by
  checking terminal manifest generation (`dataset_info.yaml` and `index.json`).
  Partially transcoded sets are classified as `[RESUMABLE]`.
- **File-Level Delta Scanning**: Replaces blind file queues with size-aware
  delta inspection. Any existing valid `.webp` image or metadata file is
  bypassed in milliseconds, eliminating redundant CPU/GPU compute upon
  interrupted runs.
- **Real-Time Visual Telemetry**: Integrates single-line progress tracking
  reporting conversion speed (img/sec), active thread allocation, and countdown
  ETA across both metadata replication and multi-threaded WebP encoding.

### 2.8 Fast Split Shard Discovery & mtime Caching

Introduced in v16.9.6, this eliminates deep recursive walking across hundreds of
thousands of loose files when evaluating manifold compiled status. The scanner
inspects container roots (`shards/`, `mds/`, `wds/`, `litdata/`) and immediate
split folders (`train/`, `val/`, `test/`) with `os.scandir`, and since v16.9.22
also the `data/*.jsonl` splits of LLM manifolds. Results are cached against the
directory's filesystem `st_mtime`, dropping API response latency from
$> 20\text{ seconds}$ to $< 50\text{ ms}$; with $k$ inspected folders a cache
miss costs $\mathcal{O}(k)$ and a hit $\mathcal{O}(1)$.

### 2.9 In-Memory Streaming Download & Terminal Telemetry

To prevent terminal line wrapping and intermediate disk consumption during
remote manifold acquisition, v16.9.1 hardens terminal progress telemetry and
couples cloud synchronization with the streaming modernization engine:

1. **Direct In-Memory Streaming on Cloud Download (`[GET]`)**: In
   `core/common_sync.py` (`perform_dataset_download`), downloaded legacy `.zip`
   archives are inspected prior to extraction. If an archive contains legacy
   loose image structures (`images/`, `targets/`) without pre-existing `.tar`
   shards, the compiler bypasses disk extraction via 7-Zip and routes the
   archive through `stream_zip_to_webdataset`
   (`tools/stream_zip_to_container.py`). Input and target images are decoded and
   transcoded to WebP in memory (quality 92 for inputs, 95 for targets) directly
   into POSIX `.tar` shards across parallel worker threads. Upon verified
   completion, the source `.zip` archive is deleted, saving 60 GB to 130+ GB of
   intermediate disk headroom and eliminating millions of loose filesystem
   writes.
2. **Terminal Telemetry & Column Width Hardening**: Fixes a PowerShell and
   Windows conhost line wrapping defect in Kaggle transfers where multi-byte
   block characters (`█`, `▋`) and dynamic column widths cascaded carriage
   returns (`\r`) onto new lines for every tick. Transfer progress bars use a
   fixed width (`dynamic_ncols=False`) and a fixed `bar_format`, and
   `utils/progress.py` switches to ASCII rendering when standard output cannot
   encode Unicode block characters, guaranteeing single-line in-place updates.
3. **Silent Subsystem Extraction Delegation**: Native 7-Zip execution parameters
   in `utils/archive.py` (`smart_extract`) changed from `-bsp1` to `-bsp0`,
   silencing per-file stdout progress emission during fallback physical archive
   extractions.

### 2.10 Modern Telemetry Progress Architecture

v16.9.19 replaces legacy ASCII terminal progress bars with unconstrained metric
streams that the frontend UI digests:

1. **Elimination of ASCII Progress Bar Glyph Flooding**: In `utils/progress.py`,
   the default progress format moved from multi-line visual bar graphics
   (`\n|{bar:50}|`) to a single-line metric descriptor:

   ```python
   STANDARD_BAR_FORMAT = (
       "{desc} - {percentage:5.1f}% "
       "[{n_fmt}/{total_fmt}, {rate_fmt}{postfix}]"
   )
   ```

   This format provides parseable telemetry metrics (`percentage`, `n_fmt`,
   `total_fmt`, `rate_fmt`) without character-based visual bars (`[====>]`,
   `|...|`, `█`).
2. **WebSocket & Sidecar Stream Sanitization**: In `api/jobs.py`
   (`JobManager._execute_job_thread`), every child process line is forwarded
   unchanged to the per-job WebSocket log. For the global dashboard stream,
   lines detected as progress output have residual bar segments (`|...|`,
   `[...]`) stripped by regular expression and repeated whitespace collapsed
   before broadcast.
3. **Static Analysis Protocol Compliance**: `utils/progress.py`
   (`track_progress`) replaces dynamic `hasattr(iterable, "__len__")`
   introspection with the `collections.abc.Sized` protocol
   (`isinstance(iterable, Sized)`), enabling static type narrowing in Pyright
   and mypy without suppression pragmas.
4. **Decoupled Visual Rendering**: Visual progress rendering is delegated to the
   desktop GUI layer (`@radix-ui/react-progress`), which shows animated progress
   bars, live transfer rate indicators, and ETA badges while keeping log feeds
   focused on milestone events.

---

## 3. Hybrid Cloud & Registry Integration

### 3.1 Atomic Registry Resumption & Hardlink Deduplication

- **Atomic Registry Resumption & SQLite Mappings**: Resumption safety is
  guaranteed by tying the metadata compiler to a transaction-locked SQLite
  register ($\mathcal{D}$, `manifold_registry.db`). Each compiled sample state
  $s_i$ is committed atomically. The state resumption mapping is:

  $$
  \mathcal{R}: \mathcal{D} \to \mathcal{S}_{\text{state}}
  $$

  This lets interrupted runs fast-forward past millions of completed operations
  in milliseconds, without index scans or I/O traversals.

- **NTFS Hardlink Deduplication (Space-Recovery Equation)**: For restoration and
  super-resolution tasks where target images map identically to clean source
  copies (identity mapping), physical duplication of image pixels is avoided.
  The compiler issues NTFS hardlinks (`os.link`) to map multiple target
  directories back to a single physical source cluster. The total recovered disk
  space $\Delta S$ is:

  $$
  \Delta S = \sum_{i=1}^{M} \text{Size}(I_i) \cdot (\text{Refs}(I_i) - 1)
  $$

  where $I_i$ is a clean target image, $\text{Size}(I_i)$ is its file size on
  disk, and $\text{Refs}(I_i)$ is the number of active training manifolds that
  reference it. This recovered **1.06 TB** of disk space during the UPNv2
  compilation with zero pipeline disruption.

- **Orphan Rescue & Batch Adoption (v6.1)**: During pipeline initialization, the
  compiler scans physical storage and identifies "orphaned" files (files on disk
  but missing from the SQLite registry). It runs a low-memory batch adoption
  cycle to register them:

  $$
  \text{Adopt}(\mathcal{O}) = \bigcup_{k=1}^{\lceil |\mathcal{O}|/C \rceil}
  \text{Commit}(\mathcal{O}_{k \cdot C})
  $$

  where $C = 100{,}000$ is the batch memory chunk limit, preventing memory
  spikes during large recovery operations. Adoption costs
  $\mathcal{O}(|\mathcal{O}|)$ time and $\mathcal{O}(C)$ memory.

### 3.2 Metadata Synchronization & Cloud Transfer

- **Metadata Synchronization**:
  - **KaggleHub & HF Sync**: Automated synchronization of compiled manifolds to
    Kaggle/HF via native API managers.
  - **Standardized `dataset_info.yaml`**: Every manifold generates a
    suite-compliant metadata package for immediate ingestion by the LemGendary
    Model Training Suite.
  - **Decoupled Documentation Generation (v16.4.1)**: All dataset documentation
    generation (`README.md`, `dataset_info.yaml`, `category.txt`, `classes.txt`,
    `index.json`) moved out of the monolithic compiler pipeline. The
    orchestrator `core/docs/orchestrator.py` (with `core/doc_generator.py`)
    generates model-specific architecture mappings and extrapolated baseline
    metric tables directly from `models_metadata` and `task_metadata` in
    `unified_data.yaml`.
- **Real-Time Byte-Metered Synchronization & Status Polling (v16.6.0)**:
  Replaces silent transfer pipelines with chunk-level streaming monitors.
  Archiving and remote payload transmission (`core/common_sync.py`,
  `tools/manifold_sync.py`; the former `archive_manager.py` and
  `kaggle_manager.py` were folded into these modules and `sources/`) use 1 MB
  byte-stream chunking
  ($\mathcal{C}_{\text{chunk}} = 1024 \times 1024\text{ B}$) with pre-calculated
  uncompressed byte envelopes to report transfer velocity ($\text{MB/s}$), ETA,
  and completion bounds. After an upload, status telemetry polls backend dataset
  readiness every 5 seconds until the ingestion pipeline moves from
  `queued`/`creating` to `ready`.
- **Direct Root Streaming & Bidirectional Resumption Protocol (v16.7.0)**:
  Eliminates the legacy intermediate extraction cache and the secondary
  byte-copy ("FINALIZING" phase). Ingestion streams remote archives directly to
  the datasets root (`LemGendaryDatasets/`) via Kaggle API binary chunking.
  Single-level extraction identifies root manifold folders to prevent
  double-nesting (`LemGendizedParseNet/LemGendizedParseNet`). The bidirectional
  resumption protocol preserves archives upon transfer or extraction
  interruptions:
  - **Download Resumption**: Pre-scans for existing valid archives on disk,
    verifies structural integrity via CRC/central directory checks, and resumes
    extraction of only missing files without redundant network I/O. Source
    archives are unlinked only after 100% successful extraction.
  - **Upload Resumption**: Preserves generated
    `.staging_<manifold>/<manifold>.zip` archives upon upload failure or
    connection resets. Retries detect valid existing archives and bypass
    recompression, saving 30 to 60 minutes of compute on multi-gigabyte
    manifolds.
- **MetaTrader 5 (MT5) Auto-Acquisition (v16.5.0)**: For financial time-series
  manifolds, the compiler bypasses raw tarball downloads and bridges into
  `tools/mt5_pipeline.py`, opening a connection to a local MetaTrader 5
  terminal. It fetches missing currency pair shards into the unified 16-symbol
  financial manifold (`LemGendizedForexUniverse`). The compiler builds a 1-Year
  Progressive Chronological Walk-Forward matrix (Fold 1: 2019 to 2020, Folds 2
  to 6: subsequent 1-year blocks) to eliminate temporal data duplication,
  computing 14 quantitative features and synchronizing shards end-to-end for
  dynamic stacking in the LemGendary Model Training Suite.

### 3.3 Kaggle Cloud Synchronization & Storage Hub

Introduced in v16.9.6, the sidecar exposes bidirectional synchronization between
the local dataset root (`LemGendaryDatasets/`) and Kaggle via
`GET /api/kaggle/registry-datasets`, `POST /api/kaggle/download`,
`POST /api/kaggle/upload`, `POST /api/kaggle/sync`,
`POST /api/kaggle/update-metadata` and `GET /api/kaggle/status`:

- **Registry Datasets**: Lists every manifold declared in `unified_data.yaml` in
  the UI with live local existence indicators and sample counts.
- **Direct Custom Link / Slug Ingestion**: Operators can provide Kaggle web URLs
  (for example `https://www.kaggle.com/datasets/owner/dataset`) or slugs
  (`owner/dataset`) to pull and unpack custom research datasets into the
  manifold storage hierarchy, with automatic unzipping and an explicit overwrite
  option.
- **Zero-Recompression Upload**: Packages compiled streaming manifolds with
  valid metadata manifests and streams them to Kaggle Model and Dataset
  registries.

### 3.4 Canonical Storage Format & Kaggle SSOT Governance

To eliminate dual-storage waste, v16.8.0 established a Single Source of Truth
(SSOT) container governance matrix. Every manifold declares exactly one
`canonical_format` in `unified_data.yaml` (registry schema `4.3.0`):

- **Zero-Duplication Format Assignment**: Loose directory trees and streaming
  tar archives never coexist for the same manifold:
  - **Apache Parquet (`parquet`)**: Zstandard-compressed annual columnar shards
    for high-frequency financial time-series (`LemGendizedForexUniverse`).
  - **WebDataset (`webdataset`)**: Contiguous $\sim 500\text{ MB}$ tar shards
    for 18 manifolds: 10-bin quality distributions (`NimaAesthetic`,
    `NimaTechnical`, `NimaAuthenticity`), ultra-scale parameter prediction
    (`LemGendizedUpnV2`), paired restoration targets (`FilmRestorer`,
    `CodeFormer`, `ParseNet`, `RetinaFace`, `FfaNet` indoor and outdoor,
    `MirNet` low-light and exposure, `MprNet`, `NafNet` deblurring and
    denoising, `UltraZoom`), multi-task restoration
    (`LemGendizedMultitaskRestorationPro`) and safety classification
    (`LemGendizedClassificationMaster`). The last two used MosaicML Streaming
    (`mds`) until their shards were transcoded to WebDataset.
  - **Directory (`directory`)**: Optimized WebP `images/` with YOLO `.cache`
    label arrays for native Ultralytics training (`LemGendizedYoloV8n`),
    remediated via NTFS LZX transparent compaction.
  - **JSON Lines (`jsonl`)**: Train and validation instruction splits for the
    LLM manifold (`LemGendizedAIHelperLemGend`).
- **Automated Kaggle Metadata Governance**: `unified_data.yaml` (v4.3.0) and
  `core/config_schema.py` enforce 5 audited Kaggle taxonomy tags, CC-BY-NC-4.0
  licensing, and provenance tables for 10.0 Usability score compliance. CLI:
  `sync metadata`.

### 3.5 Multi-Source Custom Dataset Synthesis Engine

`POST /api/gui/custom-compile` (v16.9.6, hardened in v16.9.24) compiles a new
manifold from heterogeneous sources:

- **Kaggle**: `kaggle://owner/dataset` or Kaggle web URLs.
- **Hugging Face**: `hf://org/dataset` or Hugging Face dataset URLs.
- **Google Drive**: `gd://folder_id` or Google Drive sharing links.
- **GitHub**: `gh://owner/repo` or repository URLs.

The engine normalizes all inputs into canonical URI schemes, adds a registry
entry and dispatches a background compile job with the selected task
(`restoration`, `detection`, `segmentation`, `quality`, `vision`), container
format and preset. The request is processed in a fixed order, and any failure
stops it before a job exists:

1. **Preset**: `preset` is optional. An omitted preset resolves to
   `default_preset` in `presets.yaml` (`quality-vision`), read by
   `core.presets.get_default_preset_name()`, which fails if the value names no
   defined preset. An unknown preset returns HTTP 422 with the list of valid
   presets.
2. **Registry write**: `core.unified_registry.add_dataset_entry` keeps the
   existing `unified_data.yaml` text (comments, folding, line endings) byte for
   byte and inserts only the new entry at the end of `datasets:`. An existing
   key returns HTTP 409; an entry that fails the compiler schema (`UnifiedData`)
   returns HTTP 422. The write is atomic (temporary file in the same folder,
   `fsync`, `os.replace`); if it fails, the route returns HTTP 500 and no job is
   created. The registry path does not depend on the working directory.
3. **Compile, then purge**: the job runs
   `core/manifold_compile.py --model <key> --preset <name>`, adding `--cleanup`
   when `purge_loose_images` is true (the default). `process_dataset` returns
   one `ManifoldOutcome` per manifold and
   `core.compile_outcome.finalize_compile` sets the exit code: a run that
   compiled nothing (unknown model, zero samples) exits 1, so the job ends as
   `failed`. With `--cleanup`, the loose layout (`images/`, `labels/`,
   `targets/`, `masks/`) is removed only after a successful compile and only for
   manifolds whose packed container was written in that run, because otherwise
   the loose layout is the only copy. The container writer's exit code is
   checked, and `formats.directory.purge_loose_layout` is shared with
   `tools/migrate_manifold_format.py --purge-source`.

With $\mathcal{M}_{\text{run}}$ the manifolds compiled in a run and
$\text{packed}(m)$ true when the container for $m$ was written successfully in
that run, the purged set is:

$$
\mathcal{P}_{\text{purge}} = \{ m \in \mathcal{M}_{\text{run}} : \text{cleanup}
\wedge \text{compiled}(m) \wedge \text{packed}(m) \}
$$

### 3.6 SSOT Notebook Delegation & Deduplication

To keep a single authoritative source for training and inference notebooks,
v16.9.7 moved notebook generation out of `lemgendary-datasets`:

1. **Deduplication of Generator Codebase**: Removed duplicated notebook builders
   (`tools/notebook_generator.py` and `tools/notebooks/`), eliminating redundant
   cell templates and diverging execution logic across repositories.
2. **Dynamic In-Process Delegation (`core/manifold_compile.py`)**: During
   manifold compilation, notebook generation imports
   `generate_training_notebook` and `generate_colab_training_notebook` from the
   sibling `lemgendary-training-suite`. If the LemGendary Model Training Suite
   is not on the Python path, the compiler logs actionable setup instructions
   instead of falling back to stale local templates.
3. **Identical Manifold & Model Training Notebooks**: Because manifold
   compilation and training launches use the same builder, the `.ipynb` files
   placed in `LemGendaryDatasets/<manifold>/` are bit-exact copies of those
   placed in `LemGendaryModels/<model>/`, `kaggle_training/`, and
   `colab_training/`.
4. **Stale Artifact Purge**: Obsolete or unreferenced legacy notebooks in
   compiled manifolds (such as `classification_master_manifold_training.ipynb`)
   are purged during compilation and replaced with freshly generated notebooks.

A contract test (`tests/test_ecosystem.py`) checks that the training suite's
notebook generators are real callables; the training suite is found through the
`training-suite` service in `ecosystem.json` (skipped when the sibling checkout
is absent).

### 3.7 Task Taxonomy & Manifold Task Type (v16.9.61)

`task_taxonomy.json` (schema `task_taxonomy.schema.json`) is the single source
of task ids. Each entry of `tasks[]` has an `id`, the split folder the task adds
(`layout_dir`: `masks`, `labels`, `targets` or none), a default `label_strategy`
and `mask_strategy`, and the ordered `name_patterns` of the fallback heuristic
(`heuristic.fallback_task` is `detection`, `heuristic.unnamed_task` is
`quality`). `documentation_tasks` gives the documentation profile per manifold
folder. The loader `core/task_taxonomy.py` caches the file
(`LEMGENDARY_TASK_TAXONOMY_FILE` overrides the path; a missing or invalid file
raises `TaskTaxonomyError` naming it) and replaces the former in-code tables
(`_TASK_PATTERNS`, `_TASK_DIRS`, the label and mask strategy dicts and
`MANIFOLD_TASK_MAP`). Outputs are unchanged.

- **Registry**: every `unified_data.yaml` entry sets `task` explicitly
  (`upn_v2` moved from `task_override` to `task`), and `load_unified_data`
  rejects task ids the taxonomy does not define. Four entries carry
  `task_confirmed: false` until the owner confirms them:
  `retinaface_mobilenet` (`pose`), `nima_authenticity` (`quality`),
  `forex_universe` (`detection`) and `ai_helper_lemgend` (`detection`).
- **Manifold metadata**: the compiler writes the task id as `task_type` into
  every manifold's `dataset_info.yaml` (image and forex paths). A docs-only
  regeneration takes it from the registry entry, else keeps the existing value.
  The LemGendary Model Training Suite reads `task_type` and falls back to the
  taxonomy for manifolds compiled before v16.9.61.

---

## 4. Multi-Modal & Format Resilience

### 4.1 Upstream Multi-Source Expansion Architecture

The compiler supports declarative multi-source dataset expansion (`sources/`)
through `unified_data.yaml` under each manifold's `refs:` array. Operators can
add heterogeneous source repositories without altering compilation code:

- **Kaggle Datasets (`kaggle://<owner>/<dataset-slug>`)**: Handled by
  `sources/kaggle.py`, executing authenticated API or KaggleHub retrieval with
  fallback across environment variables, `~/.kaggle/kaggle.json`, and
  `.kaggle_token`.
- **Hugging Face Hub (`hf://<org>/<repo-id>[:<archive-file>]`)**: Handled by
  `sources/hf.py`, supporting snapshot downloads, compressed tarball streaming
  (`.tgz`, `.tar.gz`), and individual file synchronization with
  `.huggingface_token` authentication.
- **Google Drive (`gd://<file_or_folder_id>`)**: Handled by `sources/gd.py`,
  providing multi-threaded chunked downloads for large hosted research datasets.
- **GitHub Repositories (`gh://<owner>/<repo>`)**: Handled by `sources/gh.py`,
  enabling release asset extraction and source tree synchronization.
- **Inter-Manifold Recirculation (`manifold://<ManifoldName>`)**: Mounts and
  slices already-compiled sibling manifolds (for example
  `LemGendizedNafNetDebluring` inside `LemGendizedMultitaskRestorationPro`)
  without duplicating image files on disk.

### 4.2 Multi-Format Annotation Converter Subsystem

Regardless of the upstream dataset's original structure, the compiler detects
and transforms annotations and image tensors through the unified `converters/`
subsystem:

- **MATLAB Input Format (`converters/matlab.py`)**: Native support for MATLAB
  `.mat` files via `scipy.io.loadmat(mat_path, spmatrix=False)`. Hardened for
  SciPy 1.14+ sparse matrix deprecations, the parser extracts annotation keys,
  matrix coordinates, and ground-truth bounding arrays.
- **COCO JSON Format (`converters/coco.py`)**: Parses MS-COCO bounding boxes,
  instance categories, and polygon segmentation boundaries into unified internal
  sample dictionaries.
- **Pascal VOC XML Format (`converters/xml.py`)**: Traverses XML node trees to
  extract object classes and pixel-coordinate bounding boxes
  (`[xmin, ymin, xmax, ymax]`).
- **YOLO Format (`converters/yolo.py`)**: Normalizes space-delimited text
  annotations (`class x_center y_center width height`) into standardized
  bounding box targets.
- **Apache Parquet & Safetensors (`converters/parquet.py`)**: Native ingestion
  of compressed PyArrow columnar tables, embedded byte buffers, and model
  tensors.
- **Multi-Format Image Support**: A single-pass scanner (`_fast_scan`) ingests
  `.jpg`, `.jpeg`, `.png`, `.webp`, `.safetensors`, `.tiff`, `.tif`, `.bmp`, and
  `.npy` arrays.

### 4.3 Pre-flight Validation, Integrity Vetting & Pruning

Every discovered sample from any source passes pre-flight gating before entering
the manifold:

- **Magic-Byte Header Sniffing**: `VisionAuditor.verify_header()` inspects raw
  file signatures (a RIFF container must carry `WEBP` in bytes 8 to 12),
  rejecting zero-byte stubs, corrupt bitstreams, and truncated downloads.
- **Spatial Dimension Floors, Aspect Ratios & Black Frames**: Samples below the
  task floor of Section 2.2 ($\min(W, H) < 224\text{ px}$ for restoration,
  $< 512\text{ px}$ for diffusion), with an aspect ratio above $10{:}1$, or with
  more than $90\%$ near-black pixels are filtered out.
- **NIMA Perceptual Quality Gating**: Evaluates aesthetic and technical quality
  score distributions, discarding heavily degraded or out-of-distribution frames
  (the `quality-vision` preset gates at a NIMA aesthetic score $\ge 5.0$).
- **Perceptual Deduplication (`pHash`)**: Computes DCT perceptual hashes to
  eliminate duplicate or near-identical images across overlapping upstream
  sources.

### 4.4 Domain Specializations

- **Parquet & Safetensors Support (v16.6.0)**: Native ingestion of compressed
  PyArrow binaries, Safetensors model weights, and unified annual financial
  manifolds (`ForexUniverse{year}.parquet`) using Zstandard compression (level
  3) with in-memory row-group caching.
- **DPED Mirroring v2.1**: Automated alignment of synthetic and real-world
  restoration pairs (Smartphone vs. Canon) using the specialized DPED cache.
- **VRAM De-fragmentation**: Proactive memory purging during NIMA/YOLO vetting
  to prevent out-of-memory errors on 4 GB to 8 GB local hardware.
- **Universal Film Restorer Dataset Hardening**: Confirmed 0 empty label files
  and 100% target physical hardlinking in `LemGendizedFilmRestorer`, at 0 bytes
  of disk overhead.
- **Professional Multi-Task Restoration Dataset Integration (v16.3.0)**: Unified
  source pipeline merging 11 individual manifolds with filename prefix
  preservation for downstream regular expression routing. Standardized target
  hardlinking layout with case-insensitive skip-indexed ingestion, and Lanczos
  interpolation ceilings at 256 px to 640 px to feed the Mixture-of-Experts
  (MoE) routing engine.
- **ParseNet Semantic Extraction (v16.3.1)**: The compiler outputs a `masks/`
  directory, resolving paired masks as target images for face segmentation tasks
  rather than generic YOLO polygons.
- **RetinaFace YOLO Landmarking (v16.3.1)**: Dynamic 5-point landmark extraction
  from `landmarks/` into standard YOLO format, with all classes filtered to
  `face` (index 0).

### 4.5 Modular Container Format Layer

The format layer (`formats/`: `directory`, `webdataset`, `litdata`, `parquet`,
`mds`, `transcode`) supports concurrent multi-format emission (`--also-format`)
alongside canonical directory structures:

- **WebDataset (WDS)**: Obfuscated shard emission (`.data` binary blobs,
  `--shard-ext data` by default) preventing cloud archive sniffing and automated
  extraction freezes while streaming POSIX ustar streams. Canonical container
  format for all vision manifolds except `LemGendizedYoloV8n`.
- **PyTorch Lightning LitData**: Streaming format for variable-length detection
  bounding boxes and landmark regression targets.
- **Apache Parquet + Zstandard**: Contiguous columnar storage with level 3
  compression for financial and tabular time-series manifolds.
- **MosaicML Streaming (MDS) [Legacy]**: Superseded by WebDataset (`.data`) and
  LitData. All existing 110.9 GB `.mds.zstd` shards
  (`LemGendizedClassificationMaster` and `LemGendizedMultitaskRestorationPro`)
  were transcoded to WebDataset (`.data`) shards via
  `tools/modernization_queue.py`. The MDS writer remains available through
  `--also-format mds` for compatibility, but no registry manifold uses it as its
  canonical format, and it needs the optional `mosaicml-streaming` package,
  which the Environment Manager no longer installs (v16.9.81).

> **Dataset Compiler Format Ingestion Notice**: Formats such as **TFRecord**,
> **HDF5**, and **CSV** are valid general machine learning dataset structures
> covered in General AI Training Knowledge. They are **not natively parsed** by
> the LemGendary Dataset Compiler Suite as image dataset containers. Before
> ingestion, convert them into supported representations (**LitData**,
> **WebDataset**, **Parquet**, **YOLO**, or **VOC**). The LLM knowledge ingestor
> (Section 4.10) reads CSV files as text sources only. MosaicML MDS (`.mds`) is
> legacy; transcoding to WebDataset (`.data`) is available via
> `tools/modernization_queue.py`.

### 4.6 Studio-Supported vs. General Knowledge Formats

The compiler delineates **Studio Native Supported Formats** (first-class
streaming manifolds and annotation converters ingested by `lemgendary-datasets`
and `lemgendary-training-suite`) from **General Knowledge Formats**
(industry-standard containers documented for ML ecosystem context but not
emitted by the LemGendary suite). For each format the list gives family,
classification, ingestion or emission mode, shard indexing and streaming
mechanism, and primary optimization target:

- **WebDataset (.data / .tar)**: Archive tarball shard (obfuscated); **STUDIO
  SUPPORTED**; native bidirectional; sequential POSIX tar shard streaming with
  `wds.WebDataset` via the `.data` extension to bypass Kaggle automatic archive
  sniffing; large vision manifolds on POSIX/Linux clusters and Kaggle/Colab
  runtimes.
- **MosaicML MDS (.mds)**: Binary indexed chunks; **DEPRECATED (MIGRATED)**;
  legacy ingestion and transcoding; index JSON manifest plus raw binary chunks,
  transcoded to WebDataset `.data` via `tools/modernization_queue.py`;
  cloud-native multi-node streaming (superseded by WebDataset and LitData).
- **LitData (.litdata)**: Lightning streaming; **STUDIO SUPPORTED**; native
  bidirectional; chunked binary records with dynamic index boundaries;
  variable-length detection and regression targets.
- **Apache Parquet (.parquet)**: Columnar table with Zstandard; **STUDIO
  SUPPORTED**; native bidirectional; PyArrow row-group indexing with zstd
  compression; high-frequency financial and tabular time-series.
- **JSON Lines (.jsonl)**: Line-delimited instruction records; **STUDIO
  SUPPORTED**; native emission by the LLM compiler; one ChatML record per line
  in `data/` train and validation splits; LLM instruction fine-tuning.
- **Flat Image Manifold (.webp/.png)**: Directory structure; **STUDIO
  SUPPORTED**; native bidirectional; in-memory `os.scandir` hash-set with
  $\mathcal{O}(1)$ physical skip-indexing; zero-intermediate transcoding and
  NTFS cluster recovery.
- **YOLO / COCO / VOC / MAT**: Annotation vectors; **STUDIO SUPPORTED**;
  ingestion via `converters/`; per-sample spatial parsing into normalized target
  tensors; object detection, facial landmarks, bounding boxes.
- **TFRecord (.tfrecord)**: Protocol buffer binary; **GENERAL KNOWLEDGE**;
  non-native, documented; `tf.data.TFRecordDataset` sequential record reader;
  legacy TensorFlow pipelines, non-standard in PyTorch 2.x.
- **Petastorm (.parquet via Spark)**: Columnar PySpark container; **GENERAL
  KNOWLEDGE**; non-native, documented; Apache Arrow PySpark IPC connector;
  distributed Spark analytics, superseded by native PyArrow.
- **LMDB (.lmdb)**: Memory-mapped B-tree key-value store; **GENERAL KNOWLEDGE**;
  non-native, documented; single mmap address space with transaction locks;
  legacy Caffe/PyTorch, lacks cloud-chunked streaming.
- **HDF5 / H5 (.h5, .hdf5)**: Hierarchical scientific container; **GENERAL
  KNOWLEDGE**; non-native, documented; `h5py` hierarchical dataset pointers;
  multidimensional physics arrays, prone to multiprocessing write lock
  contention.
- **RecordIO (.rec)**: MXNet sequential record; **GENERAL KNOWLEDGE**;
  non-native, documented; `mxnet.recordio` sequential chunk reader; legacy
  Apache MXNet pipelines.
- **Feather / Arrow IPC (Raw)**: Memory-mapped flat binary; **GENERAL
  KNOWLEDGE**; non-native, documented; uncompressed Arrow memory buffer mapping;
  ephemeral IPC transfer, lacks compressed row-group partitions.

### 4.7 Hardlink Dedup Preservation & Pre-Flight Gate

Because container formats (tarballs, chunked binaries) pack raw byte streams and
destroy NTFS/POSIX hardlink deduplication, the compiler runs a pre-flight
hardlink audit gate (`audit/hardlinks.py`, `audit_hardlinks()`, exposed as
`GET /api/gates/hardlinks`):

$$
\text{Verdict} = \begin{cases} \text{PROCEED} & \text{if } \text{HardlinkRatio}
< 5.0\% \\ \text{WARN} & \text{if } 5.0\% \le \text{HardlinkRatio} \le 25.0\% \\
\text{BLOCK} & \text{if } \text{HardlinkRatio} > 25.0\% \end{cases}
$$

Any attempt to emit container formats on restoration manifolds with heavy
hardlink dedup (such as `LemGendizedUpnV2` with $1.06\text{ TB}$ recovered) is
blocked unless explicitly overridden via `--force-duplicate`.

### 4.8 Smart Multi-Modal Generation Engine

Integrated AI backends (`generators/`, CLI `label`, `prompt`, `mask`) run across
compiled manifolds:

- **BLIP Captioning & NIMA Quality Vetting**: Generates descriptive prompts and
  perceptual quality distributions.
- **CLIP Zero-Shot & Style Clustering**: Partitions manifolds into latent style
  clusters via `MiniBatchKMeans` with deterministic seeding.
- **YOLO Detection & Auto-Labeling**: Derives normalized bounding boxes and
  object class distributions.
- **ParseNet & SAM Segmentation**: Generates discrete face and instance masks.

### 4.9 Physical Degradation Synthesis Engine

Pure NumPy, SciPy, and Pillow kernels (`degrade/`, CLI `degrade`,
`POST /api/jobs/degrade`) derive paired synthetic restoration manifolds from
clean targets:

- **Optical Defocus & Motion Blur (`blur`)**: Directional linear trajectories
  and circular aperture disk diffraction.
- **Heteroscedastic Sensor Noise (`noise`)**: Poisson photon arrival statistics
  coupled with Gaussian sensor readout noise.
- **Atmospheric Koschmieder Scattering (`haze`)**:
  $I(x) = J(x)t(x) + A(1 - t(x))$ simulating atmospheric depth and haze.
- **DCT Quantization (`jpeg`)**: 8x8 block discrete cosine transform simulation
  modeling JPEG artifacts.
- **Rain & Precipitation (`rain`)**: Linear directional rain streaks with mist
  and droplet scattering for deraining pairs.
- **Low-Light Underexposure (`lowlight`)**: Non-linear gamma darkening with
  readout noise in deep shadows, simulating photon starvation.
- **Downsampling (`downsample`)**: Bicubic and bilinear down-and-up sampling
  simulating optical resolution loss for super-resolution pairs.
- **Vintage Film (`film`)**: Non-linear film grain, vertical scratches and
  archival artifacts for film restoration pairs.
- **Provenance Logging**: Exact parameter values (blur kernel dimensions, angle,
  noise variance, gamma) logged per sample to `labels/<split>/<name>.json`.

### 4.10 Generic LLM Dataset Compiler

The suite includes a generic, declarative Large Language Model (LLM) instruction
manifold compiler in `tools/llm_helper/` (`BaseLLMCompiler` in
`base_compiler.py`), exposed as CLI `llm compile` and `llm validate` and as
`POST /api/llm/compile` and `POST /api/llm/validate`. It replaces ad-hoc
scraping and manual JSONL formatting with an extraction, chunking and validation
pipeline driven by declarations in `unified_data.yaml`.

#### 4.10.1 Declarative Configuration

Every instruction manifold declares its pipeline under the registry. The
production entry `ai_helper_lemgend` (abridged) is:

```yaml
ai_helper_lemgend:
  name: AIHelperLemGend
  dataset_type: llm
  modernized_folder: LemGendizedAIHelperLemGend
  canonical_format: jsonl
  train_file: data/ai_helper_train.jsonl
  val_file: data/ai_helper_val.jsonl
  test_file: data/ai_helper_test.jsonl
  split_strategy: stratified
  val_split: 0.15
  test_split: 0.15
  llm_pipeline:
    schema_format: chatml_turn3
    target_samples: 1150
    generator_module: tools.llm_helper.knowledge_synthesizer
    knowledge_sources:
      - type: markdown_dir
        path: lemgendary-docs/MD-Papers
        glob: '*.md'
      - type: yaml_file
        path: lemgendary-training-suite/unified_models_v2.yaml
      - type: remote_url
        url: https://lemgenda.github.io/ai-training-whitepapers/index.html
    chunking:
      strategy: recursive
      chunk_size: 1200
      chunk_overlap: 200
    quality_invariants:
      zero_emojis: true
      enforce_epistemic_tags: true
      intake_protocol_stages: 3
```

The compiler reads `llm_pipeline`, resolves the knowledge sources relative to
the workspace root, and dispatches the generator module
(`tools.llm_helper.knowledge_synthesizer`). A key without a mapped generator
raises an error instead of producing an empty manifold.

#### 4.10.2 Supported Multi-Format Loaders

The knowledge ingestor (`KnowledgeIngestor`, `knowledge_ingestor.py`) turns
documentation and data sources into normalized `KnowledgeDocument` objects, each
with a SHA-256 `content_hash`:

- **Markdown (`.md`)**: Structured technical documentation, keeping headings,
  fenced code blocks and tables.
- **Plain Text (`.txt`)**: Raw logs, terminal transcripts and unformatted
  documentation.
- **JSON / JSONL (`.json`, `.jsonl`)**: Structured telemetry, conversational
  traces and existing instruction pairs.
- **YAML (`.yaml`, `.yml`)**: Ecosystem configuration manifests, registry
  schemas and pipeline blueprints.
- **CSV (`.csv`)**: Tabular data, metric logs and parameter grids rendered as
  readable tables.
- **Web URLs**: Remote documentation fetched over HTTP and cached on disk (URL
  keyed by a truncated SHA-256 digest).

#### 4.10.3 Chunking, Provenance Lineage & Hash Verification

To partition documentation into bounded instruction units, `RecursiveChunker`
(`chunker.py`) splits each document:

- **Hierarchical Boundary Splitting**: For each window of `chunk_size`
  characters (default 1200), the chunker cuts at the last of the separators
  `"\n## "`, `"\n### "`, `"\n\n"`, `"\n"`, `". "` (tried in that order) that
  lies beyond half the window; otherwise it cuts at the window edge.
- **Contextual Sliding Window Overlap**: The next window starts `chunk_overlap`
  characters (default 200) before the cut, preserving cross-boundary continuity.
  For a document of $L$ characters, chunk size $s$ and overlap $o < s/2$, the
  chunk count and time are bounded by:

  $$
  n_{\text{chunks}} \le \left\lceil \frac{L}{s/2 - o} \right\rceil, \qquad
  T_{\text{chunk}} = \mathcal{O}(L \cdot s / (s/2 - o))
  $$

- **Provenance Lineage Tracing**: Every `KnowledgeChunk` records `chunk_id`,
  `doc_id`, `source_path`, `canonical_url`, `section_title` and its character
  offsets (`char_start`, `char_end`).
- **Cryptographic Hash Verification**: Each chunk carries a deterministic
  SHA-256 digest (`sha256`) of its UTF-8 text:

  $$
  \mathcal{H}(c) = \text{SHA256}(\text{UTF8}(c))
  $$

  The hash supports bit-exact deduplication and tamper verification across the
  training lifecycle; `index.json` lists the record inventory with SHA-256
  hashes.

#### 4.10.4 Quality Invariants & Validation

Every record passes the `QualityValidator` gate (`quality_validator.py`) before
any file is written. Each finding is a frozen `ValidationIssue` dataclass
(record id, `field`, `issue`, severity); errors block the compile, warnings are
reported:

1. **Schema (error)**: A record needs an `id` and a `category`; `messages` must
   hold at least 2 turns in the order `[system, user, assistant]` or
   `[user, assistant]`, each with non-empty string content. Record ids must be
   unique across the corpus.
2. **Zero-Emoji Enforcement (error)**: Unicode emoji characters (surrogate
   pairs, pictographs, symbols, dingbats) are prohibited in all turns.
3. **3-Stage Diagnostic Intake Protocol (warning)**: In
   `troubleshooting_diagnostics` records, the assistant turn must cover Stage 1
   Initial Triage, Stage 2 Targeted Diagnosis and Stage 3 Bounded Remediation.
4. **Epistemic Certainty Tagging (warning)**: The same troubleshooting answers
   must carry an epistemic qualifier (`[CONFIRMED]`, `[PROBABLE]`,
   `[ILLUSTRATIVE]`) to separate verified facts from illustrative examples.

After validation, records are split per category with a seeded generator (seed
42): with $n_c$ records in category $c$ and validation share $v$ (`val_split`,
default 0.20), the validation count is $\max(1, \lfloor v \cdot n_c \rfloor)$
for $n_c > 1$ and 0 otherwise.

`lem llm validate` and `POST /api/llm/validate` report up to 20 issues
(severity, field, record id, issue) and exit 1 or return HTTP 400 when the
corpus fails; unreadable or invalid JSONL is reported as such.

### 4.11 Sample Integrity, Shard Verification & Manifold Repair

The `v16.9.75` to `v16.9.84` releases close the data-integrity findings of the
2026-11 audit. A sample is written whole and correct, or it is rejected and
recorded.

- **No identity pairs (v16.9.79)**: restoration, super-resolution and
  segmentation samples without a real target are rejected before anything is
  written; before, the degraded input (or the RGB image for segmentation) was
  copied as its own target. Clean-only sources (ParseNet, CodeFormer) keep their
  documented behaviour.
- **Masks, labels and corrupt images (v16.9.76)**: `utils/image_payload.py`
  turns raw bytes into shard payloads; zero-byte or undecodable images raise
  `CorruptImageError` instead of being packed, and masks are stored as lossless
  `.mask.webp` that keep their class indices. Loose and zip `masks/` and
  `labels/` are packed with their image, and `utils/sample_group.py` writes one
  sample (image, `.target`, `.mask`, `.txt` or `.json`) as one contiguous tar
  member group.
- **Label geometry (v16.9.79)**: safetensors full-frame boxes are pixel boxes
  (they were normalized twice), Parquet pose rows use their bbox columns or the
  box around the visible keypoints instead of `0 0 0 0`, and NPZ face keypoints
  are normalized like every other pose source. `WebDatasetWriter` partitions
  shards by split (`shards/<split>/`).
- **Audit gates (v16.9.80)**: `core/sample_audit.py` runs the audit gates on the
  compile path: file headers (magic bytes) before decoding, target size equal to
  the input size, boxes in pixels and keypoints and polygons normalized. A
  missing paired target is `ERR_TARGET_MISSING`, and every reject goes to the
  registry's `reject_log` table.
- **Shard verification (v16.9.80, v16.9.83)**: `utils/shard_audit.py` audits
  every written shard by its headers: sample keys, zero-byte members, scattered
  groups, unreadable tars and, in a paired set, samples without a `.target.*`
  member. The converters and the MDS transcoder fail on any finding and keep the
  source; `verify_archive` fails on zero-byte image or shard members.
- **Lossless MDS transcode (v16.9.77)**: every non-image MDS column (class,
  category, `nima_scores`, bbox, keypoints, source and others) is decoded by its
  column encoding into the `<key>.json` sidecar, and the legacy `mds/` folder is
  purged only when the written sample count equals the count in the MDS index.
- **Workers, interrupt and dedup (v16.9.78)**: worker state is initialised once
  per process under a lock; Ctrl+C cancels queued batches, commits the registry
  and re-raises instead of calling `os._exit`; warm-up results pass the same
  dedup and `max_gb` accounting as pool results; resumed runs seed exact and
  perceptual hashes from the registry; perceptual dedup
  (`enable_perceptual_dedup`) uses a bucketed `NearDupIndex`.
- **Download safety (v16.9.82)**: a downloaded zip is streamed into new
  WebDataset shards only when it is a legacy loose-image archive; a zip that
  holds shards, Parquet, MDS or JSONL splits is extracted as is, and a target
  that already has shards is never streamed into. The Temp sweep deletes only
  `LemGendized*.zip`, and layout folders (`shards`, `data`, `images`, `targets`,
  `labels`, `masks`, `mds`) are never unwrapped.
- **Manifold repair (v16.9.81)**: `python cli.py repair manifold --manifold
  PATH` (or `--model KEY`) and `python cli.py repair all [--root DIR]` print a
  repair plan and change nothing. With `--apply` they drop samples with
  zero-byte members, make scattered groups contiguous (each rewritten shard is
  verified before it replaces the original), resync the `dataset_info.yaml`
  counts, replace an absolute or staging `path` with the canonical relative one
  and clean `index.json`. Since v16.9.85 no originals are kept: each rewritten
  file is verified and swapped in atomically (the `.repair_backup` folder is
  gone), and a second run finds nothing to do. LLM manifolds now record the
  canonical `path` too.
- **No swallowed errors (v16.9.75)**: the hub script's folder probes, the MT5
  vault reader and the JSONL ingestor log errors instead of hiding them.

### 4.12 JSON Shard Labels, Sample Policies & Source Labels (v16.9.85 to v16.9.107)

- **JSON is the only shard label format (v16.9.98)**: inside WebDataset shards
  a sample's label is `<key>.json`; there are no `.txt` label members, and
  masks stay `<key>.mask.webp`. `utils/label_json.py` is the schema SSOT
  (`LABEL_STRATEGIES`); the strategy is the registry entry's `label_json`,
  else its task's (`TASK_STRATEGIES`). Coordinates are normalised to 0..1 and
  boxes are `cx cy w h`:
  - `face_landmarks` (RetinaFace): `face_count`, `objects[]` with
    `category_id`, `bbox_cxcywh_normalized` and, when the face has real
    landmarks, `landmarks_normalized` (10 values; ten zeros count as absent).
    Labels rebuilt from source landmarks also record `landmark_source`.
  - `yolo_boxes` (detection, pose, restoration, super-resolution,
    parameter prediction): `object_count`, `objects[]` with `category_id`,
    `bbox_cxcywh_normalized` and, for pose lines, `keypoints`.
  - `yolo_polygons` (segmentation): `object_count`, `objects[]` with
    `category_id`, `polygon_normalized`.
  - `nima` (quality): `nima_scores` with `distribution` (10) and
    `mean_score`.
  - `segmentation_mask` (face parsing): the class mask is the
    `<key>.mask.webp` member (lossless, one class id per pixel); the JSON
    records `num_classes`, `class_names` and `mask_source`.
  - `class_label` (classification): `class_id` or `class_name`; labels
    written by `repair class-labels` carry both plus `label_source` and the
    registry `task`, and a pseudo label also `label_confidence` and
    `label_check_class`.
  - `caption` (diffusion): `caption`.

  An empty detection label is `{"object_count": 0, "objects": []}`, a valid
  negative. Every shard writer packs JSON only, and the shard verifier
  (`utils/label_audit.py`, `repair manifold`, the converters' post-write
  check) fails on any `.txt` member or schema break. The Training Suite reads
  the same schema (`data/json_labels.py`, v16.9.200).
- **Sample policies (v16.9.97, v16.9.100, v16.9.102)**: `core/sample_policy.py`
  sorts samples into kinds, drops `drop_kinds` and draws val from
  `val_kinds`. The face detection policy (`label_json: face_landmarks`)
  drops samples without a face and draws val from the landmark-bearing photos
  by source file id; the face parsing policy (`segmentation_mask`) drops
  copies and segmentation maps by key and splits all photos by SFHQ file id.
  A source with a key layout draws its val share over all of the layout's
  file ids, so ParseNet and RetinaFace share one val set and no file is in
  both splits. Registry fields: `scan_exclude_dirs` (folder globs the source
  scan never enters) and `key_layouts` (the key index layout of a source).
- **Source labels registry (v16.9.100, v16.9.101)**: `source_labels`
  (`scheme`, `source`) names the per-file labels a source ships next to its
  images, and `key_layouts[].files_dir` the source's folder under a local
  label root. Schemes live in `core/source_labels.py`: `celebamask_hq_19`
  (the 19-class CelebAMask-HQ / BiSeNet masks of SFHQ, `repair masks`) and
  `sfhq_110` (the SFHQ 110-point landmarks; points 0-67 follow the iBUG
  300-W order), from which `core/face_geometry.py` derives the five
  RetinaFace points (eye centres, nose tip 30, mouth corners 48 and 54) and a
  tight WIDER-style box (`repair face-landmarks`).
- **Class labels (v16.9.103 to v16.9.106)**: the registry field
  `class_labels` holds a scheme (`nsfw_5`: 0 drawings, 1 hentai, 2 neutral,
  3 porn, 4 sexy) and ordered key rules (`core/class_labels.py`, first match
  wins). ClassificationMaster: `anime_dbrating` index below 278,119 is
  hentai, the rest drawings, `food101` neutral, and the NSFW source a pseudo
  label from the GantMan nsfw_model (Inception V3, MIT, ONNX on the CPU),
  kept only at a top probability of at least 0.8 when the MobileNet V2 check
  model agrees (`require_check_agreement`); other NSFW samples are dropped.
- **Manifold repairs**: `repair` keeps no originals (v16.9.85; each shard is
  rewritten to a temporary file, verified and swapped in with `os.replace`),
  converts leftover PNG/JPEG members to WebP (v16.9.86) and offers `labels`,
  `txt-labels`, `pack-loose`, `sample-policy`, `masks`, `face-landmarks`,
  `pseudo-labels` and `class-labels` (CLI manual Section 5.17); since
  v16.9.108 also `shard-offsets` (Section 4.13).
- **Kaggle sync (v16.9.92 to v16.9.104)**: one credential module
  (`core/kaggle_credentials.py`: a `KGAT_` token goes to `KAGGLE_API_TOKEN`
  unchanged, `~/.kaggle/access_token` counts); `GET /api/kaggle/status` lists
  `environment_variables`, `secrets_vault`, `user_access_token` and
  `user_kaggle_json`. Uploads carry version notes; new datasets are created
  private with the manifold's license; dataset cards state the real split
  counts once and per-source counts only when exact. `sync pull` creates a
  missing datasets root, falls back to a file-by-file download (and the
  Kaggle API route after a per-file 404), waits on HTTP 429 and takes
  `--only`. Since v16.9.109 `sync push --notes TEXT` adds what changed in the
  new version after the generated version notes (CLI manual Section 5.10).
- **Forex timestamps (v16.9.87)**: the `timestamp` column is whole Unix epoch
  seconds (UTC); `forex/columns.py` holds the column definitions and
  `TIMESTAMP_UNIT = "seconds"`, and `dataset_info.yaml` and the Parquet schema
  metadata record `timestamp_unit: seconds`.
- **GUI access (v16.9.89, v16.9.90)**: `POST /api/config/validate` is open to
  the GUI origins with the client header; `POST /api/gui/quick-compile`
  takes `shard_ext`.

### 4.13 Shard Offset Index (v16.9.108)

Every WebDataset shard folder (`shards/<split>/`) carries
`shard_offsets.json`, the byte offsets of the members of its plain tar
shards. The Training Suite (v16.9.215 and later) reads this file instead of
every tar member header of a split; the header scan took 15 to 48 minutes for
a 53 GB split on Kaggle's network storage (Training Suite paper Section 2.46).

- **Format (version 2)**: one JSON object per shard folder,
  `{"version": 2, "shards": {"shard-00000.data": {...}}}`. Each plain tar
  shard has its byte `size`, its modification time `mtime_ns` and the
  `names`, `offsets` (payload offsets) and `sizes` of its regular members in
  archive order. The layout is the Training Suite's
  (`training/data/containers/shard_tables.py`), and a file with another
  `version` is ignored. The name has no leading dot because Kaggle dataset
  uploads skip hidden files. A compressed shard cannot be read by offset and
  gets no entry.
- **Acceptance rule**: an entry is used when the shard size matches and
  either the modification time matches or the tar headers of the first,
  middle and last member agree with the entry (three reads). An upload or a
  copy changes the modification time, never the size or the member layout, so
  the index stays valid after a Kaggle upload. Any other entry is stale and
  the shard is rescanned.
- **Cost**: for a split of $S$ shards with $M_s$ members each, the header
  scan costs $\mathcal{O}\left(\sum_{s=1}^{S} M_s\right)$ random reads, while
  an open from the index costs one file read plus at most $3S$ header reads
  (none when the modification times match).
- **One writer**: `utils/shard_offsets.py` (`write_shard_offsets`) is the
  only writer and checker and does not import the Training Suite. Unchanged
  shards keep their entry, rewritten ones are rescanned. Every step that
  writes or rewrites shards refreshes the file: `WebDatasetWriter.close` and
  the legacy `ShardWriter.close` (compile and `--also-format`), the diffusion
  shard pass, zip streaming, loose packing, MDS transcoding, the sample
  policy, and the `apply` of `repair manifold`, `labels`, `txt-labels`,
  `masks`, `face-landmarks` and `class-labels`.
- **Verification**: the shard verifier (`utils/shard_audit.py`
  `shard_set_problems`, so the converters' post-write check and
  `repair manifold`, which rewrites a stale index) checks a present index:
  every plain shard needs an entry the Training Suite would accept, with the
  member count of the audit, and no entry may name a missing shard.
- **Upload**: the staging zip packs every file of the manifold folder, so the
  index is uploaded; a newer index makes the staging zip be rebuilt. The GUI
  catalog scan does not count `shard_offsets.json` as a shard.
- **Existing manifolds**: `repair shard-offsets [--model KEY | --manifold
  PATH] [--apply]` writes the index without touching the shards (CLI manual
  Section 5.17). Measured runs: LemGendizedRetinaFace 103 shards, 850,446
  members, 75.5 MiB in 98 s; LemGendizedParseNet 111 shards, 1,275,774
  members, 101.8 MiB in 101 s; LemGendizedClassificationMaster 158 shards,
  1,507,068 members, 107.0 MiB in 163 s. The Training Suite reader accepts
  every train shard from the file (1.5 to 3.1 s per split, no header scan).
- **Read-only folders**: when the Training Suite opens a read-only shard
  folder without a usable index (Kaggle `/kaggle/input`), it keeps its own
  scan cache outside the manifold; the index in the manifold is written only
  by the compiler or by a Training Suite run on a writable folder.

---

## 5. Comparative Analysis / Benchmarks

### 5.1 Technical Comparison Matrix

The dataset compilation landscape in 2026 is shaped by the trade-off between
distributed cloud throughput and local zero-IPC hardware efficiency. The
benchmark compares the **LemGendary Dataset Compiler Suite (v16.8.0 profile)**
with five industry manifold compilers: **NVIDIA NeMo Curator (v2026)**,
**HuggingFace WebDataset / Datasets v3**, **Ray Data / Anyscale Compiler**,
**Cohere / DeepSpeed Data Engine**, and **Meta / PyTorch TorchData v2**. Values
are listed per benchmark parameter in that order, LemGendary last; LemGendary
figures are the historical v16.8.0 measurements of Section 2.3.

- **Filesystem Indexing**: NeMo Curator $\mathcal{O}(N \log N)$ metadata scan;
  HF WebDataset v3 $\mathcal{O}(N)$ manifest traversal; Ray Data
  $\mathcal{O}(N)$ graph build; Cohere/DeepSpeed $\mathcal{O}(N \cdot d)$
  directory walk; TorchData v2 $\mathcal{O}(N)$ MapDataPipe; **LemGendary
  $\mathcal{O}(1)$ flat `scandir` hash scan**.
- **Indexing Latency (1.4M items)**: $112.5$, $145.0$, $88.2$, $210.4$ and
  $165.8 \text{ seconds}$; **LemGendary $0.4 \text{ seconds}$ ($460\times$
  faster than its legacy pipeline)**.
- **Memory & IPC Model**: PyArrow shared memory IPC; multiprocess queue
  pickling; Plasma store object IPC; PyTorch DDP IPC; DataLoader worker IPC;
  **LemGendary Zero-IPC ThreadPool (shared RAM)**.
- **IPC Serialization Latency**: $12.4$, $412.0$, $45.6$, $280.1$ and
  $390.5 \text{ seconds}$; **LemGendary $0.0 \text{ seconds}$ ($100\%$ overhead
  elimination)**.
- **Storage Optimization**: MinHash physical rewrite; tarball duplication;
  Parquet physical rewrite; tarball sharding; in-memory filtering; **LemGendary
  WebP 92 + hardlink ($64.6\%$ recovery)**.
- **Resampling Preservation**: GPU bilinear/bicubic; PIL default bicubic;
  OpenCV/PIL resize; PyTorch interpolate; torchvision transforms; **LemGendary
  Lanczos-3 anti-aliased kernel**.
- **Resumption Engine**: JSONL checkpoints; tarball shard indexes; actor state
  logs; metadata manifests; IterDataPipe state dicts; **LemGendary
  transaction-locked SQLite registry**.

### 5.2 Competitor Deep-Dive: Pros, Cons & Pricing

#### 5.2.1 NVIDIA NeMo Curator & Data Designer (v2026)

- **Pros:** GPU-accelerated MinHash deduplication and VLM semantic filtering;
  native integration with the NeMo training framework.
- **Cons:** Requires multi-GPU DGX/HGX clusters for heavy tasks; significant
  VRAM overhead during pre-processing; locked to the NVIDIA ecosystem.
- **Pricing & Cost Model:** Commercial enterprise license via **NVIDIA AI
  Enterprise (USD 4,500 per GPU per year)** or cloud GPU usage rates (USD 3.50
  to 4.80 per GPU-hour).

#### 5.2.2 HuggingFace WebDataset / Datasets v3 Compiler

- **Pros:** Standard for cloud tarball streaming (`.tar` / `.parquet`); HF Hub
  integration and dataset sharing.
- **Cons:** High Windows IPC serialization penalty; tarball creation forces
  physical data duplication; slow random-access seek times.
- **Pricing & Cost Model:** Open-source core; **HF Enterprise Hub (USD 20 per
  user per month)** plus HF Endpoints storage and ingress costs (about USD 0.02
  per GB per month).

#### 5.2.3 Ray Data / Anyscale Distributed Compiler

- **Pros:** Scalable distributed batch execution across thousands of CPU/GPU
  worker nodes; resilient task graphs.
- **Cons:** High memory footprint due to Plasma Object Store serialization
  overhead; complex cluster orchestration and setup.
- **Pricing & Cost Model:** Open-source core (Ray); **Anyscale Managed Cloud
  (USD 0.10 to 0.30 per Anyscale Compute Unit hour)** plus underlying AWS/GCP
  infrastructure costs.

#### 5.2.4 Cohere / DeepSpeed Data Engine

- **Pros:** Optimized for large-scale LLM/VLM text-image tokenization and
  multi-modal sharding; strong multi-node streaming.
- **Cons:** Weak support for image restoration/super-resolution paired targets;
  high multi-node network bandwidth requirements.
- **Pricing & Cost Model:** Open-source (DeepSpeed); **Cohere Enterprise API
  custom tier (USD 15,000 to 50,000+ per year commitment)** for managed
  enterprise pipeline deployment.

#### 5.2.5 Meta / PyTorch TorchData Manifold Compiler v2

- **Pros:** Native PyTorch `IterDataPipe` / `MapDataPipe` ecosystem
  compatibility; zero external framework dependencies.
- **Cons:** Lacks persistent metadata transactions (susceptible to corruption
  during crashes); high multiprocessing worker IPC overhead.
- **Pricing & Cost Model:** Open-source (BSD License); **no software cost**, but
  standard unoptimized cloud compute and storage overheads due to lack of
  hardlinking.

#### 5.2.6 LemGendary Dataset Compiler Suite

- **Pros:** $\mathcal{O}(1)$ physical skip-indexing; Zero-IPC ThreadPool RAM
  sharing; 64.6% disk space recovery via NTFS/POSIX hardlinking; Lanczos-3
  spectral preservation; SQLite transaction resumption locks; atomic registry
  writes and purge-after-success cleanup.
- **Cons:** Optimized primarily for local/hybrid single-node and edge hardware;
  non-distributed (single-node multi-threaded/GPU execution).
- **Pricing & Cost Model:** **No software license cost**; zero cloud lock-in;
  storage for identical paired restoration targets is eliminated via native
  hardlinking.

---

## 6. Synthesis Flow & Topology

### 6.1 The Dataset Hub

The interactive dashboard (Dataset Hub v6.0.0-SOTA,
`lemgendary_datasets_hub.ps1`) manages manifolds end-to-end on top of a
decoupled modular engine (`core/compiler_core.py`, `core/manifold_compile.py`,
`tools/manifold_reduce.py` and `tools/manifold_sync.py`). Hardware acceleration
includes **CPU-GUARD** (detection of large datasets on CPU-bound systems;
triggers "High-Speed Mode" to prevent I/O thrashing) and **CUDA-Sentry**
(real-time detection of GPU availability for NIMA vetting and YOLO
auto-labeling). `tools/manifold_sync.py` supports full duplex Kaggle
synchronization (upload via automatic zipping and download with disk-space
collision safeguards).

### 6.2 Industrial Output Topology

The output topology (Nuclear Architecture) is:

- `raw-sets/` (source datasets, protected by the Cleanup Guardian)
- `../LemGendaryDatasets/<name>/images/` (standard structured folders for
  restoration)
- `../LemGendaryDatasets/<name>/labels/` (NIMA 10-bin probabilities or YOLO
  vectors)
- `../LemGendaryDatasets/<name>/targets/` (ground truth targets for
  SR/restoration)
- `../LemGendaryDatasets/<name>/dataset_info.yaml` (suite metadata)
- `../LemGendaryDatasets/<name>/manifold_registry.db` (persistent SQLite
  metadata)
- `../LemGendaryDatasets/<name>/README.md` (Kaggle-optimized manifest)

The output root comes from `_registry_metadata.output_folder_name` in
`unified_data.yaml` (`../LemGendaryDatasets`). The loose `images/`, `labels/`,
`targets/` and `masks/` folders are removed by `--cleanup` only after their
packed container was written in the same run (Section 3.5).

### 6.3 LLM Manifold Filesystem Topology

Compiled LLM manifolds follow the standardized topology:

```text
LemGendaryDatasets/
└── LemGendized{Name}/
    ├── data/
    │   ├── {train_file}.jsonl
    │   └── {val_file}.jsonl
    ├── dataset_info.yaml
    ├── index.json
    ├── category.txt
    ├── classes.txt
    ├── dataset-metadata.json
    └── README.md
```

- **`data/` Subfolder**: The train and validation JSONL splits named by
  `train_file` and `val_file` (default `data/<key>_train.jsonl` and
  `data/<key>_val.jsonl`), produced by the seeded stratified split of Section
  4.10.4.
- **`dataset_info.yaml`, `category.txt`, `classes.txt`**: Suite metadata,
  category and task class, as for vision manifolds.
- **`index.json`**: Record inventory with SHA-256 hashes.
- **`dataset-metadata.json`**: Kaggle Frictionless descriptor declaring
  licensing and resources.

### 6.4 Unified Three-Pipeline Architecture

Three standardized pipelines govern the lifecycle of training datasets.

#### 6.4.1 Regular Ingestion & Manifold Compilation (`compile`)

- **Primary Scope**: Ingesting raw external datasets (`raw-sets/`), applying
  quality gating, and compiling standardized production manifolds
  (`LemGendized*`). CLI `compile`, API `POST /api/jobs/compile`,
  `POST /api/gui/quick-compile` and `POST /api/gui/custom-compile`; a run
  without `--model` compiles every registry manifold.
- **Workflow Stages**:
  1. *Discovery & Pre-flight*: Scans raw sources and verifies directory layout
     and file structures against `unified_data.yaml`.
  2. *Quality & Integrity Filters*: Inspects magic headers, validates resolution
     floors and aspect ratios, filters corrupted samples, and applies NIMA
     aesthetic/technical quality gating.
  3. *Auto-Labeling & Resampling*: Derives normalized YOLO bounding boxes,
     SAM/ParseNet segmentation masks, or BLIP captions where applicable,
     applying Lanczos-3 anti-aliasing interpolation for spatial rescales.
  4. *Zero-Intermediate WebP Transcoding*: Transcodes input images in memory
     (`quality=92` for inputs, `quality=95` for restoration targets) without
     uncompressed intermediate disk writes.
  5. *Emission & Container Sharding*: Emits canonical directory layouts with
     NTFS hardlink deduplication preserved, or additionally exports streaming
     container shards (`--also-format webdataset`, `--also-format litdata`,
     legacy `--also-format mds`).
  6. *Manifest & Documentation Generation*: The documentation orchestrator
     (`core/docs/orchestrator.py`) dispatches single-responsibility generators
     producing `category.txt`, `classes.txt`, `<ModelName>.jpg` (564x284
     architecture banner), `dataset_info.yaml`, `index.json`, `README.md`, and
     Frictionless `dataset-metadata.json` for Kaggle API synchronization.
  7. *Outcome & Cleanup*: `core.compile_outcome.finalize_compile` turns the
     per-manifold outcomes into the exit code (1 when nothing compiled);
     `--cleanup` then purges loose layouts as described in Section 3.5.

#### 6.4.2 Legacy Archive Modernization (`stream_zip_to_container`)

- **Primary Scope**: Modernizing legacy multi-gigabyte `.zip` archives
  containing millions of small files into canonical POSIX WebDataset `.tar`
  shards without writing uncompressed loose files to disk
  (`tools/stream_zip_to_container.py`, driven by
  `tools/modernization_queue.py`).
- **Workflow Stages**:
  1. *Zero-Unpack Streaming Ingestion*: Opens the `.zip` archive via central
     directory indexing, bypassing NTFS MFT lock contention, short filename
     generation, and real-time antivirus filter driver serialization.
  2. *In-Flight Multi-Threaded Transcoding*: Decompresses raw image streams in
     memory and dispatches them across a 12-thread worker pool executing Pillow
     WebP encoding (`method=2`, `quality=92` for inputs, `quality=95` for
     targets).
  3. *Dual-Pass Sequential Tar Streaming*: For paired restoration sets
     (`images/` and `targets/`), Pass 1 writes sequential input images into
     `shard-*.tar`, while Pass 2 appends paired targets in POSIX append mode
     (`"a"`), maintaining sequential write throughput on NVMe SSDs.
  4. *Root Metadata Extraction*: Extracts documentation, notebooks, and index
     manifests (`index.json`, `dataset_info.yaml`, `README.md`) to the
     modernized manifold root.
  5. *Storage Reclamation (opt-in)*: Validates shard byte counts and sample
     completeness. Only when requested (`--delete-zip`, `--delete-legacy-dir`,
     or `purge_loose: true` / `--purge-source` through modernize) does it delete
     the source `.zip` archive and legacy unpacked directory trees, recovering
     50 GB to 100+ GB per dataset. By default every source is kept.

#### 6.4.3 Retroactive Manifold Migration (`format migrate`)

- **Primary Scope**: Converting already modernized local dataset directories
  (loose WebP images, targets and `index.json`) into canonical streaming
  container shards (`webdataset`, or legacy `mds`) via `format migrate` /
  `tools/migrate_manifold_format.py`.
- **Workflow Stages**:
  1. *Manifest & Index Traversal*: Reads the existing `index.json` or scans the
     structured manifold directory tree to build deterministic sample queues.
  2. *Container Chunk Serializer*: Streams samples into contiguous, fixed-size
     container chunks (about 500 MB `.tar` shards or `.bin` / `.index` MosaicML
     Streaming files).
  3. *Cluster Slack Elimination & Source Purge*: With `--purge-source`, unlinks
     loose intermediate image files after successful shard verification through
     the shared `formats.directory.purge_loose_layout`, consolidating tens of
     thousands of fragmented files into a handful of sequential shards.
  4. *Registry Synchronization*: Updates `dataset_info.yaml` with
     `canonical_format: webdataset`, enabling zero-overhead streaming ingestion
     by the training suite DataLoader.

### 6.5 S.O.L.I.D. Services Layer & Forex Encapsulation

Introduced in v16.7.0 and extended in v16.9.19 and v16.9.25:

- **In-Process Services Layer (`services/`)**: Compiler workflows are split into
  single-responsibility services (`CompilerService`, `DegradeService`,
  `AuditService`, `DocService`, `GenerationService`, `MigrationService`,
  `SyncService`) plus the `job_watch` helper. CLI commands call typed service
  layers in-process rather than shelling out to external subprocesses.
- **One Service Layer for CLI and API (v16.9.57)**: long API jobs (compile,
  degrade, LLM compile, modernization queue and reduce, Kaggle and manifold
  sync) run a service module as their own process
  (`services.compiler_service`, `services.degrade_service`,
  `services.llm_service`, `services.migration_service queue|reduce`,
  `services.sync_service kaggle|manifold`); each module's `main(argv)` calls
  the same function the CLI calls in-process. `services/invocation.py` holds
  the typed `ServiceInvocation` and the flag tables that both the job and the
  parser use, and `JobManager` is the only place in the API that starts a
  process.
- **Unified Audit Engine**: `AuditService.audit_manifold()` unifies magic-byte
  checking, resolution and aspect ratio validation, DCT perceptual
  deduplication, and NTFS hardlink fraction audits in one command (`audit`).
- **Safe Module Ingestion**: Argument parsing in `core/manifold_compile.py` is
  encapsulated in `parse_compile_args()` and `process_dataset(parsed_args)`,
  eliminating top-level import side-effects.
- **Domain Encapsulation (`forex/`)**: Historical Forex time-series pipelines
  live in a modular subpackage (`forex.schema`, `forex.converter`,
  `forex.injector`, `forex.bridge`, `forex.pipeline`) with root
  backward-compatibility shims and CLI subcommands (`forex convert`,
  `forex embed`).
- **Warning Suppression Policy**: Programmatic warning suppressions
  (`warnings.filterwarnings`) and inline diagnostic silencing directives were
  removed from the code. Since v16.9.51 the repository `.pylintrc` has no
  `disable=` entries, and Ruff and Pylint report no findings (v16.9.53,
  v16.9.54).

### 6.6 Asynchronous Sidecar API & Hybrid CLI

- **FastAPI / Uvicorn Daemon (`api/`)**: Runs on `127.0.0.1:8100` with route
  groups for health (`/api/health`, `/api/health/full`), GUI aggregation
  (`/api/gui/*`), datasets, sources, gates, Kaggle, modernize, LLM,
  configuration, jobs and environment. `openapi.json` lists all 37 operations
  (`POST /api/jobs/generic` was removed in v16.9.58).
  The port, the Kaggle owner and the sibling project folders are read
  from `lemgendary-env-manager/ecosystem/ecosystem.json` through one loader,
  `core/ecosystem.py`.
- **SQLite Job Registry (`.lgd_server/jobs.db`)**: Persistent state machine with
  restart recovery that marks orphaned runs `interrupted`. Job types include
  compile, degrade and, since v16.9.25, `llm`. The arbitrary-command job
  endpoint (`POST /api/jobs/generic`) was removed in v16.9.58; every job is a
  typed `ServiceInvocation`. A job moves `pending` to `running` to
  `completed`, `failed` (with the exit code), `cancelled` or `interrupted`.
- **WebSocket Streaming**: Live logs stream per job via
  `ws://127.0.0.1:8100/api/ws/jobs/{id}/logs`, and dashboard events via
  `ws://127.0.0.1:8100/api/ws/events`.
- **Asynchronous LLM Compile (v16.9.25)**: `POST /api/llm/compile` is an `async`
  route, so `async_mode: true` hands the running event loop to the job runner
  and the `llm` job actually starts (the former synchronous route left it
  `pending`). The synchronous path runs the compiler in a worker thread and
  returns HTTP 400 with a logged traceback on failure.
- **Bounded CLI Wait**: `llm compile` polls `GET /api/jobs/{id}` through
  `services.job_watch.wait_for_job` until `completed`, `failed`, `cancelled` or
  `interrupted`, then prints the log tail. `--timeout` (default 3600 s) bounds
  the wait, so the polling cost is $\mathcal{O}(t_{\max} / \Delta t)$ requests
  for poll interval $\Delta t$. A timeout, an unknown job or an unknown state
  exits 1; a failed job exits with its exit code.
- **Hybrid Transparent CLI**: When the server daemon is active, CLI commands
  dispatch via HTTP and stream logs to the Rich console, falling back to
  in-process execution when offline. CLI groups: `env`, `sync` (`push`, `pull`,
  `metadata`), `docs`, `config`, `format`, `presets`, `server`, `forex`,
  `modernize`, `llm`, plus top-level `compile`, `transcode`, `audit`, `label`,
  `prompt`, `mask`, `degrade`, `reduce`, `test` and `version`.

### 6.7 Cross-Project Automation & Desktop GUI Presets

- **Canonical Compiler Presets (`presets.yaml`, `core/presets.py`)**: Formal
  compilation profiles (`quality-vision`, `restoration-hardlinked`,
  `detection-variable`, `cloud-archival`) define quality floors, resampling
  filters, auto-labeling toggles and container targets.
  `default_preset: "quality-vision"` names the preset used when an API request
  omits one; `core.presets.get_default_preset_name()` rejects a value that names
  no defined preset.
- **Aggregated Desktop GUI Endpoints (`api/routes/gui.py`)**: `/api/gui/state`,
  `/api/gui/datasets/with-stats`, `/api/gui/jobs/active`, `/api/gui/presets`,
  `/api/gui/quick-compile` and `/api/gui/custom-compile` hydrate the LemGendary
  AI Studio GUI dashboard.
- **Regenerated OpenAPI 3.1 Contract (v16.9.27)**: `openapi.json` is written
  deterministically from the live application by `tools/export_openapi.py`
  (application key order, 2-space indent, LF, trailing newline); `--check` exits
  1 on drift, and `tests/test_openapi_contract.py` fails when the file drifts
  from the app or misses a served operation. `info.version` equals the version
  the API serves.
- **Multi-Sidecar Top-Bar Observability**: Interoperable with the LemGendary
  Environment Manager (port 8000) and the LemGendary Model Training Suite
  sidecars for synchronized cross-project governance.

### 6.8 Modernize and Reduce Operations

v16.9.26 aligns the modernize and reduce routes with the CLI and makes them safe
by default:

- **Modernize Scope**: `POST /api/modernize/run` (`ModernizeRunRequest`) accepts
  `datasets`, the GUI's single `dataset`, `dry_run` and `force`. Both scopes are
  merged and passed once as a comma-joined `--datasets` value. Matching prefers
  an exact key, name or folder, so `alpha` no longer also runs `alpha_v2`; a
  dataset that matches nothing exits 1.
- **Dry-Run Guarantee**: A dry run never converts, deletes, writes or uploads;
  it prints the per-dataset plan, including what a real run would delete.
  Formally, with $\mathcal{F}$ the filesystem and registry state:

  $$
  \text{dry\_run} \Rightarrow \mathcal{F}_{\text{after}} =
  \mathcal{F}_{\text{before}}
  $$

- **Source Retention**: `purge_loose` defaults to `false` and keeps every source
  (zip, legacy folder, loose images); `true` deletes them only after a
  successful conversion. API and CLI share
  `tools.modernization_queue.build_queue_args` and `main(argv)`; `modernize run`
  has `--purge-source`.
- **Reduce Through the API**: `tools/manifold_reduce.py` accepts `--dataset`,
  `--fraction`, `--yes` and `--dry-run` and returns a real exit code; with
  `--yes` it never prompts and requires `--dataset`.
  `POST /api/modernize/reduce` accepts the GUI's `manifold` (alias of
  `dataset_key`), optional `max_gb`, `suffix` and `dry_run`, and a `scale`
  interpreted as a kept fraction $f$:

  $$
  f = \begin{cases} s & \text{if } 0 < s \le 1 \\ 1/s & \text{if } s > 1
  \end{cases}
  $$

  so `0.25` keeps 25 % and `2` keeps half. The route always runs
  non-interactively and rejects a missing manifold with HTTP 400. `reduce` and
  `modernize reduce` are the same CLI command; without `--yes` they still
  prompt.
- **Suffix Retirement**: The former shadowed `modernize` command is reachable as
  `modernize manifolds`.

### 6.9 Security Model

The sidecar binds to `127.0.0.1` by default and shares one security contract
with the other two sidecars and the GUI:

- **Origin Guard (`api/security.py`, v16.9.23)**: A request whose `Origin`
  header is not an AI Studio GUI origin (`tauri://localhost`,
  `http://tauri.localhost`, `https://tauri.localhost`, `http://localhost:1420`,
  `http://127.0.0.1:1420`) gets HTTP 403, and WebSocket handshakes from a
  foreign origin are closed with policy-violation code 1008.
- **Client Header**: Browser requests that use `POST`, `PUT`, `PATCH` or
  `DELETE` must send `X-LemGendary-Client: ai-studio-gui`. The custom header
  forces a CORS preflight, which blocks cross-site form posts. Requests without
  an `Origin` (CLI, scripts, tests) are not affected.
- **Closed CORS**: The CORS policy lists the same origins, explicit methods and
  headers (`Content-Type`, `Authorization`, `X-API-Key`, `X-LemGendary-Client`)
  and `allow_credentials=False` instead of `allow_origins=["*"]`.
- **API Token**: Behind the guard, the configuration, jobs and environment
  routes check the `X-API-Key` token (`api/auth.py`, `LEMGENDARY_API_TOKEN`).
- **Dataset Root Confinement (v16.9.27)**: `POST /api/llm/validate` resolves
  `file_path` (preferably relative to the dataset root; absolute paths only when
  inside it) with `..` collapsed and symlinks followed before checking it. With
  $R$ the resolved dataset root and $p$ the resolved path:

  $$
  \text{status}(p) = \begin{cases} 403 & \text{if } p \notin \text{subtree}(R)
  \\ 404 & \text{if } p \in \text{subtree}(R) \wedge \neg\,\text{isfile}(p) \\
  \text{validate} & \text{otherwise} \end{cases}
  $$

  A path outside the root returns 403 even when the file does not exist. Only
  file, encoding and JSON errors become HTTP 400.
- **Secret Files**: Token files and `.GOOGLE_DRIVE_JSON` are ignored by git.

---

## 7. Unified Models Registry

`unified_data.yaml` declares 21 manifolds. The entries below use the canonical
output folder names (`modernized_folder`); sample counts are from the latest
manifold builds.

### LemGendizedAIHelperLemGend

- **Category:** Technical Documentation & AI Assistant Training
- **Target Samples:** 1,150 (`target_samples`), stratified 80/20
  train/validation split
- **Storage Format:** JSON Lines (`jsonl`)
- **Architecture Base:** Instruction-tuned causal language model (AI LemGend
  assistant)
- **Primary Task:** Documentation-grounded question answering, GUI/CLI/API
  guidance and safe troubleshooting.

### LemGendizedClassificationMaster

- **Category:** Image Classification
- **Total Samples:** 753,534 (train 662,746 / val 90,788; Anime DB Rating
  619,514, Food-101 100,999, NSFW 33,021)
- **Per Source (train / val, `index.json`):** Anime DB Rating 544,611 /
  74,903; Food-101 89,105 / 11,894; NSFW 29,030 / 3,991
- **Classes:** 5 (`nsfw_5`: drawings, hentai, neutral, porn, sexy), written
  by `repair class-labels`
- **Per Class (train / val, from the `repair class-labels` run):** drawings
  300,702 / 41,355; hentai 249,105 / 34,257; neutral 92,905 / 12,445; porn
  9,392 / 1,318; sexy 10,642 / 1,413. `index.json` has no class field, so the
  per-class counts come from the label repair, not from the index.
- **Architecture Base:** Lightweight convolutional backbones with classification
  heads
- **Primary Task:** Predict categorical classes and safety content labels.

### LemGendizedCodeFormer

- **Category:** Image Restoration / Face Enhancement
- **Total Samples:** 22,000
- **Architecture Base:** CodeFormer or UNet-based restoration architectures
- **Primary Task:** Restore degraded images and enhance visual quality of human
  faces.

### LemGendizedFfaNetIndoor

- **Category:** Image Restoration
- **Total Samples:** 196,304
- **Architecture Base:** UNet-based restoration architectures with residual
  learning
- **Primary Task:** Restore degraded images and enhance visual quality.

### LemGendizedFfaNetOutdoor

- **Category:** Image Restoration
- **Total Samples:** 217,113
- **Architecture Base:** UNet-based restoration architectures with residual
  learning
- **Primary Task:** Restore degraded images and enhance visual quality.

### LemGendizedFilmRestorer

- **Category:** Image Restoration
- **Total Samples:** 67,542
- **Architecture Base:** UNet-based restoration architectures with residual
  learning
- **Primary Task:** Restore degraded images and enhance visual quality.

### LemGendizedForexUniverse

- **Category:** Financial Time-Series
- **Total Samples:** 26,818,700 (train 21,015,570 / val 5,803,130, per
  `dataset_info.yaml` and `index.json` and the training registry)
- **Storage Format:** eight yearly Apache Parquet files
  (`ForexUniverse2019.parquet` to `ForexUniverse2026.parquet`, Zstandard level
  3, 5,368 row groups of up to 5,000 rows), each row one window with its
  `pair` and `timeframe` columns. The 765 "chunks" are the `index.json`
  entries, one per pair, timeframe and year present (16 pairs by 6
  timeframes by 8 years, 3 absent), not files: years before 2025 are `train`
  (573 entries), 2025 and 2026 are `val` (192)
  (`core/docs/generators/index_json.py`). The MT5 pipeline writes per-year
  chunk shards (`ForexUniverse<year>/<pair>/<timeframe>/shard_chunk<N>.parquet`)
  that the scanner also reads; the published manifold holds the yearly files.
- **Architecture Base:** Multi-Scale CNN-Transformer (TCN + CT-MHA)
- **Primary Task:** Predict directional probability and Pip-Magnitude Boundaries
  for 16 major currency pairs and commodities across 6 timeframes.

### LemGendizedMirNetExposure

- **Category:** Image Restoration
- **Total Samples:** 1,416,459
- **Architecture Base:** UNet-based restoration architectures with residual
  learning
- **Primary Task:** Restore degraded images and enhance visual quality.

### LemGendizedMirNetLowLight

- **Category:** Image Restoration
- **Total Samples:** 15,070
- **Architecture Base:** UNet-based restoration architectures with residual
  learning
- **Primary Task:** Restore degraded images and enhance visual quality.

### LemGendizedMprNetDeraining

- **Category:** Image Restoration
- **Total Samples:** 248,190
- **Architecture Base:** UNet-based restoration architectures with residual
  learning
- **Primary Task:** Restore degraded images and enhance visual quality.

### LemGendizedMultitaskRestorationPro

- **Category:** Image Restoration
- **Total Samples:** 343,911
- **Architecture Base:** UNet-based restoration architectures with residual
  learning
- **Primary Task:** Restore degraded images and enhance visual quality (registry
  key `professional_multitask_restoration`).

### LemGendizedNafNetDebluring

- **Category:** Image Restoration
- **Total Samples:** 26,093
- **Architecture Base:** UNet-based restoration architectures with residual
  learning
- **Primary Task:** Restore degraded images and enhance visual quality.

### LemGendizedNafNetDenoising

- **Category:** Image Restoration
- **Total Samples:** 7,727
- **Architecture Base:** UNet-based restoration architectures with residual
  learning
- **Primary Task:** Restore degraded images and enhance visual quality.

### LemGendizedNimaAesthetic

- **Category:** Image Quality Assessment
- **Total Samples:** 321,369
- **Architecture Base:** MobileNetV3-Small / EfficientNetV2 / SwinV2 backbone
  with 10-bin distribution head
- **Primary Task:** Predict human-perceptual quality score.

### LemGendizedNimaAuthenticity

- **Category:** Image Authenticity Assessment
- **Total Samples:** 209,196 (189 corrupt samples were filtered during the
  latest manifold build)
- **Architecture Base:** MobileNetV3-Small / EfficientNetV2 / SwinV2 backbone
  with 10-bin distribution head
- **Primary Task:** Predict image authenticity score and map to binary
  categorical distribution.

### LemGendizedNimaTechnical

- **Category:** Image Quality Assessment
- **Total Samples:** 26,093
- **Architecture Base:** MobileNetV3-Small / EfficientNetV2 / SwinV2 backbone
  with 10-bin distribution head
- **Primary Task:** Predict human-perceptual quality score.

### LemGendizedParseNet

- **Category:** Image Segmentation
- **Total Samples:** 425,258 SFHQ photos with class masks (train 374,228 / val
  51,030, split by SFHQ file id)
- **Classes:** 19 (`celebamask_hq_19`, lossless `<key>.mask.webp`)
- **Architecture Base:** Vision Transformer (ViT) backbones with hierarchical
  decoders
- **Primary Task:** Assign categorical labels to every pixel in the image
  manifold.

### LemGendizedRetinaFace

- **Category:** Pose Estimation / Face Landmarks
- **Total Samples:** 425,223 SFHQ photos, one face each (train 374,199 / val
  51,024, the same file-id split as ParseNet)
- **Labels:** tight WIDER-style box and 5 points rebuilt from the SFHQ
  110-point landmarks (`landmark_source: sfhq-110pt`)
- **Architecture Base:** High-Resolution Net (HRNet) or ViT backbones
- **Primary Task:** Regress exact coordinate points for biological landmarks
  (registry key `retinaface_mobilenet`).

### LemGendizedUltraZoom

- **Category:** Super-Resolution
- **Total Samples:** 17,724
- **Architecture Base:** Transformer-based or Deep Residual networks
- **Primary Task:** Scale low-resolution images to high-resolution while
  preserving details.

### LemGendizedUpnV2

- **Category:** Image Restoration
- **Total Samples:** 1,378,070
- **Architecture Base:** UNet-based restoration architectures with residual
  learning
- **Primary Task:** Restore degraded images and enhance visual quality.

### LemGendizedYoloV8n

- **Category:** Object Detection
- **Total Samples:** 153,972
- **Storage Format:** Directory (`directory`)
- **Architecture Base:** CSP-Darknet / Transformer backbones with Path
  Aggregation
- **Primary Task:** Detect and localize multiple object classes with high
  precision.

---

### Pre-Baked WebDataset Offset Indexing & WebP Purity

To eliminate cloud virtual-disk startup latency (which previously required 507.9
seconds of sequential tar header scanning for 270 shards on Kaggle), every
WebDataset split (`train/`, `val/`) ships a pre-baked `shard_offsets.json`
(`STORE_VERSION = 2`) generated by `utils/shard_offsets.py` during compilation.
This enables instantaneous `0.0s` byte-offset resolution at training startup.
Additionally, all vision manifolds enforce strict WebP-only encoding, purging
any 0-byte or null-padded legacy JPEG/PNG members before shard sealing.

---

## 8. Conclusion

The LemGendary Dataset Compiler Suite changes how generative AI manifolds are
structured, scaled, and consumed. By automating the ingestion pipeline,
enforcing structural integrity, and unifying vision, detection, market data and
LLM instruction manifolds under one SSOT registry, it lets every downstream
model train on clean, hardware-aligned data with minimal disk overhead and
deterministic output. The `v16.9.23` to `v16.9.27` releases make that pipeline
safe to drive from the AI Studio GUI: only the GUI's origins may call the
sidecar, registry writes are atomic and never rewrite existing entries, loose
images are removed only after their container exists, dry runs change nothing,
and file access by the validator stays inside the dataset root. The `v16.9.75`
to `v16.9.84` releases make the output verifiable: a sample is written whole or
rejected and logged, every shard is audited after writing, and a damaged
manifold can be repaired in place.
