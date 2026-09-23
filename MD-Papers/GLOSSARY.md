# LemGendary Ecosystem: Canonical Glossary & Terminology Specification

## Category 00 | LemGendary AI Documentation Hub

---

## 1. Abstract & Scope

This authoritative specification establishes the single source of truth (SSOT) for all terminology, mathematical primitives, architectural definitions, and system invariants utilized across the LemGendary AI Ecosystem. Designed to eliminate semantic ambiguity across machine learning pipelines, desktop operators, agentic reasoning models, and technical documentation, every entry in this glossary carries strict operational definitions and cross-reference boundaries.

---

## 2. Core Taxonomy: Dataset vs. Manifold

The distinction between a raw dataset and a compiled manifold is an inviolable architectural invariant across the ecosystem:

### 2.1 Dataset (Raw Set)

* **Definition**: A collection of uncurated, heterogeneous source data originating from external repositories (e.g. HuggingFace, Kaggle, GitHub, Google Drive, or local filesystem drops).
* **Location**: Stored strictly under `raw-sets/<source-name>/` or fetched ephemeral caches.
* **Characteristics**:
  * Unstandardized file formats (loose JPEGs, PNGs, BMPs, TARs, ZIPs).
  * Arbitrary spatial resolutions, varying aspect ratios, and uncalibrated colour spaces.
  * Incomplete, missing, or malformed label structures.
  * Mutable: raw files may be updated, pruned, or re-downloaded from upstream remotes.
* **Usage**: Raw datasets are **never** ingested directly by the Master Training Suite.

### 2.2 Manifold (Compiled Training Manifold)

* **Definition**: A deterministic, mathematically vetted, hardware-aligned topological data representation compiled specifically for machine learning ingestion.
* **Location**: Stored in `../LemGendaryDatasets/LemGendized<Name>/`.
* **Characteristics**:
  * **Unified Invariants**: Strict resolution floors ($\ge 224\text{px}$ restoration, $\ge 512\text{px}$ diffusion), standardized WebP encoding ($q=92$ images, $q=95$ targets, lossless masks), and deterministic split assignments (`train`, `val`, `test`).
  * **Immutable Provenance**: Every manifold contains terminal self-documenting manifests: `dataset_info.yaml`, `index.json`, `classes.txt`, and `manifold_registry.db`.
  * **Zero Redundancy**: Identity image targets leverage physical NTFS/POSIX hardlink deduplication (`os.link`), guaranteeing zero cluster waste.
  * **High-Throughput Alignment**: Built for $\mathcal{O}(1)$ flat directory indexation and optional concurrent multi-container sharding (MDS, LitData, WebDataset, Parquet).

---

## 3. Compiler & Storage Primitives

### 3.1 $\mathcal{O}(1)$ Physical Skip-Indexing

A high-velocity filesystem technique where a single flat `os.scandir` traversal during pipeline initialization populates an in-memory string hash set ($\mathcal{S}_{\text{disk}}$) of existing files. Verifying whether a sample has already been compiled executes in $\mathcal{O}(1)$ average-case dictionary lookup time, bypassing recursive $\mathcal{O}(N \cdot d)$ disk seek overhead.

### 3.2 Zero-IPC ThreadPool

An execution model utilizing Python's `ThreadPoolExecutor` within a single virtual memory space for pure I/O operations (image decoding, transcoding, and disk writing). By avoiding multiprocessing serialization (IPC pipes/pickling), it eliminates Windows IPC latency completely ($0.0\text{ seconds}$ serialization overhead).

### 3.3 NTFS Cluster Slack Space Recovery

Standard NTFS filesystems allocate physical disk space in $4,096\text{-byte}$ clusters. Loose sliding-window arrays waste up to $4\text{ KB}$ per file in cluster slack. The compiler's columnar Parquet + Zstandard architecture aggregates temporal records into contiguous row groups, reclaiming physical disk space with up to $99.3\%$ compression ratios.

### 3.4 Hardlink Deduplication (Identity Mapping)

An optimization for image restoration where the clean ground-truth target matches the degraded input. Instead of duplicating multi-megabyte image bytes across directories, the compiler issues NTFS hardlinks referencing identical physical disk clusters, saving hundreds of gigabytes per manifold.

### 3.5 Lossless Mask Transcoding

A format constraint requiring all segmentation masks (`masks/`) to be encoded strictly via WebP lossless compression. Lossy compression introduces subtle edge-quantization artifacts that corrupt discrete integer class labels.

### 3.6 Two-Tier Modernization Resumption

An architectural design in `tools/modernize_manifold.py` combining high-level manifest validation (`dataset_info.yaml` + `index.json`) with file-level delta verification. Interrupted modernization runs bypass already-transcoded `.webp` images and metadata in seconds, resuming only uncompleted files.

---

## 4. Master Training Suite & Optimization

### 4.1 Spatial Resolution Ladder

A multi-stage curriculum learning schedule where image resolution progressively scales during training (e.g. $128\text{px} \to 256\text{px} \to 512\text{px}$). It allows early epochs to capture global structural features at high batch velocities before fine-tuning high-frequency details.

### 4.2 Nuclear-Hardened Architecture

A resilience design pattern in `lemgendary-training-suite` enforcing comprehensive validation across hardware backends, dynamic gradient scaling, automated checkpoint verification, and zero-suppression error telemetry.

### 4.3 Directional Accuracy (DA)

The primary evaluation metric for financial time-series forecasting, defined as the percentage of temporal steps where the predicted sign of price delta matches the actual market trajectory:

$$\text{DA} = \frac{1}{N} \sum_{t=1}^{N} \mathbb{I}\left( \text{sgn}(\hat{y}_t - y_{t-1}) = \text{sgn}(y_t - y_{t-1}) \right) \times 100\%$$

### 4.4 Earth Mover's Distance (EMD) Loss

The objective function utilized for probabilistic aesthetic quality distributions (NIMA), penalizing misclassifications proportionally to the distance between ordinal rating bins ($1\text{ to }10$):

$$\text{EMD}(p, \hat{p}) = \left( \frac{1}{K} \sum_{k=1}^{K} |\text{CDF}_p(k) - \text{CDF}_{\hat{p}}(k)|^r \right)^{1/r}$$

---

## 5. Training Pathology & Diagnostics

### 5.1 Pathology Reasoning Trace

A structured, synthetic diagnostic narrative generated from empirical training failure modes. It models the causal chain: Observational Symptom $\to$ Diagnostic Telemetry $\to$ Root Cause Analysis $\to$ Automated Mitigation Strategy.

### 5.2 Latent Disconnect

A training pathology where the restoration backbone converges to a trivial spatial average (e.g., solid grey or blur) while loss curves report apparent convergence, indicating loss-term imbalance or improper normalizations.

### 5.3 Catastrophic Gradient Collapse

An unrecoverable parameter destabilization typically caused by exploding gradient spikes ($\|\mathbf{g}\| > 10^4$) or unhandled NaN inputs, requiring automated checkpoint rewind and learning rate penalization.

---

## 6. Environment & Infrastructure

### 6.1 Deterministic Environment Reconciliation

The automated synchronization of local `.venv` packages against central manifests (`requirements-*.txt`), identifying version drifts and resolving transitive dependencies without global Python pollution.

### 6.2 Sidecar REST Daemon

An asynchronous FastAPI service operating on dedicated local ports (`8000` for Environment Manager, `8100` for Dataset Compiler, and `8200` for Master Training Suite) that provides headless API access, hardware health telemetry, and WebSocket log broadcasting.

---

## 7. Authoritative "Do Not Confuse With" Matrix

| Term A | Term B | Key Architectural Difference |
| :--- | :--- | :--- |
| **Dataset** | **Manifold** | Datasets are raw, mutable, heterogeneous source drops; Manifolds are compiled, deterministic, immutable, hardware-aligned training topologies. |
| **Reconciliation** | **Clean Install** | Reconciliation inspects and patches delta package drifts in-place; Clean Install nukes `.venv` and rebuilds the toolchain from stage 1 hardware probing. |
| **Container Format** | **Directory Layout** | Container formats (MDS, LitData, WebDataset) pack data into contiguous shards for cloud streaming; Directory layout preserves raw filesystem hierarchy and hardlink deduplication. |
| **Hardlink Deduplication** | **Perceptual Deduplication** | Hardlink dedup maps identical target files to the exact same physical NTFS cluster; Perceptual dedup flags visually similar images via pHash/dHash hamming distances. |
| **Image Transcoding** | **Synthetic Degradation** | Transcoding converts image file encodings (e.g. PNG $\to$ WebP $q=92$) preserving visual fidelity; Degradation mathematically corrupts images with blur/noise/haze kernels to generate paired training pairs. |
| **Sidecar API** | **CLI Tool** | Sidecar is an active background daemon streaming WebSocket events to GUI/remote clients; CLI is a direct local command executing in-process or delegating to the sidecar. |
