# LemGendary Dataset Compiler — 2026 Modernization Roadmap (v3)

> Supersedes `compiler_implementation_plan.md` (retained as reference).
> Expands `dataset_compiler_revamp.md` to the 2026 scope.
> Aligns with LemGendary Environment Manager v2.3 (API/CLI patterns).
>
> Written against the codebase, whitepapers, and env-manager stack
> as of 2026-09.

---

## 1. Executive Summary

The 2026 modernization has **eight concurrent goals**, listed in execution order:

1. Retire legacy `Large` suffix (cosmetic — visible win, ships first).
2. Consolidate config, registry, and module layout (foundation).
3. Add full audit, dedup, and reject-logging pipeline (data correctness).
4. Introduce WebP image transcoding (storage + bandwidth reduction).
5. Add a container-format plugin layer (MDS / LitData / WebDataset / Parquet).
6. Add smart label, prompt, and mask generation (source-quality).
7. Add a compiler-time degradation engine (derived-manifold synthesis).
8. Expose everything via `lemgendary` CLI and FastAPI HTTP/WebSocket server
   for CPA GUI integration, mirroring the Environment Manager's patterns.

Total estimated effort: **~12 weeks** across 9 phases. Each phase ships
independently.

---

## 2. Vision & Guiding Principles

### 2.1 Primary Objectives

- **Emit modern formats** for every manifold, chosen per-manifold based on
  actual training characteristics (not uniformity).
- **Preserve hardlink dedup** as a first-class physical property. Any format
  that forces byte duplication of hardlinked targets is disqualified for that
  manifold above the hardlink threshold (§7.3).
- **Faster, more reliable training** is co-equal with smaller storage. A
  format that saves 30% space but adds 3× decode cost is a loss.
- **Zero-drift resumption** at every stage: fetch, compile, transcode,
  format-write, sync.
- **Full auditability** — every accept/reject decision logged, queryable,
  reproducible.
- **Automation-first** — every CLI action has an API equivalent; every API
  action has CLI parity; the CPA GUI speaks only HTTP.

### 2.2 Branding Consistency (Mandatory)

All naming must use the **LemGendary** brand. No abbreviated internal names
in user-facing surfaces. The seven-project ecosystem:

| # | Project | Folder | Binary / Entry |
| --- | --- | --- | --- |
| 1 | LemGendary Environment Manager | `.\lemgendary-env-manager\` | `lem-env` |
| 2 | LemGendary Dataset Compiler Suite | `.\lemgendary-datasets\` | `lemgendary` |
| 3 | LemGendary Model Training Suite | `.\lemgendary-training-suite\` | (Python entry points) |
| 4 | LemGendary AI Studio GUI | `.\lemgendary-ai-studio-gui\` | Tauri IPC |
| 5 | LemGendary AI Documentation Hub | `.\lemgendary-docs\` | — |
| 6 | LemGendary Compiled Manifolds Repo | `./LemGendaryDatasets\` | — |
| 7 | LemGendary Trained Models Repo | `.\LemGendaryModels\` | — |

**Rule**: every reference in documentation, CLI help text, API responses, error
messages, and code comments uses the project's full branded name. Never
"the compiler", "the training suite", "the GUI" as bare nouns in user-facing
output.

### 2.3 Non-Goals

- Not distributed / multi-node. Single-node multi-threaded + GPU is the target.
- Not a training framework. The compiler emits artifacts; the training suite
  consumes them.
- Not an environment manager. That is `lem-env`'s exclusive domain.
- Not a model-hosting service. Weights stay in Kaggle Models / HF Hub.

### 2.4 Design Tenets

- **Canonical directory layout survives.** `images/`, `labels/`, `targets/`,
  `masks/` remain on disk for every vision manifold, always. Modern container
  formats are written *in addition*.
- **Opt-in everything.** Transcoding, container formats, smart generation,
  degradation — all opt-in. Defaults reproduce pre-modernization behavior.
- **Reversibility.** Every phase has a documented rollback. No destructive
  operations without explicit user confirmation.
- **Mirror the Environment Manager.** CLI structure, API shape, error format,
  exit codes, and validation gates are all inherited from `lem-env`. Do not
  reinvent.

---

## 3. Scope Boundaries

### 3.1 In Scope

Everything in `.\lemgendary-datasets\`:

- Python modules at root (`compiler_core.py`, `manifold_*.py`, `doc_generator.py`)
- Fetcher modules (`hf_manager.py`, `gh_manager.py`, `gd_manager.py`, `kaggle_manager.py`)
- Sync modules (`common_sync.py`, `manifold_sync.py`, `archive_manager.py`)
- Hub (`lemgendary_datasets_hub.ps1`)
- Config (`unified_data.yaml`, `models_metadata.yaml`)
- New packages: `sources/`, `audit/`, `converters/`, `formats/`, `generators/`, `degrade/`, `api/`
- New tools: `modernize_manifold.py`, `migrate_manifold_format.py`, `lemgendary.py`

### 3.2 Explicitly Out of Scope

| Component | Owner | Rationale |
| --- | --- | --- |
| Venv creation / package install | `lem-env` | Environment Manager exclusive |
| Dependency manifest sync | `lem-env` | Centralized manifests |
| Code validation (`py_compile`, lint, YAML/JSON) | `lem-env validate` | Multi-gate validation engine |
| Git hooks | `lem-env setup-hooks` | Standardized across all 7 projects |
| Training-suite loaders | Training suite | Separate roadmap in that repo |
| On-the-fly training augmentation | Training suite | Compiler emits artifacts; training applies distortion |
| Model weights / training | Training suite | Different concern |
| CPA GUI | `lemgendary-ai-studio-gui` | Consumes our API; we ship the contract |
| Documentation Hub content | `lemgendary-docs` | We contribute whitepaper updates |

### 3.3 Boundary Rule

**If it relates to Python packages, virtual environments, or code quality,
it belongs in `lem-env`.** The dataset compiler never calls `pip install`,
never creates `.venv`, never runs `pylint`. It shells out to `lem-env` for
those concerns and treats its return codes as authoritative.

---

## 4. Current State Assessment

### 4.1 What's Already Modern

- **`archive_manager.py`** — Resumable smart extraction, common-root detection, byte-metered progress.
- **`common_sync.py`** — Direct-root streaming, bidirectional resumption, server-side extraction tracking.
- **Forex pipeline** — Parquet + Zstd, 99.3% space reduction, 100% bit-exact.
- **DPED mirroring** — Pre-cached canonical paths.
- **O(1) physical skip index** — `PHYSICAL_INDEX` in `manifold_compile.py`.
- **NTFS hardlink dedup** — `os.link()` for restoration targets; 1.06 TB recovered on UPNv2.

### 4.2 What's Fused and Needs Extraction

| Concern | Location today | Target module |
| --- | --- | --- |
| Config validation | Ad-hoc dict access in `compiler_core.py` | `config_schema.py` (pydantic) |
| Image / annotation audit | Inline in `process_image()` | `audit/vision_audit.py` |
| Format parsing | `parse_coco`, `parse_parquet`, etc. | `converters/*.py` |
| Output serialization | `ShardWriter` + inline directory writes | `formats/*.py` |
| Reject logging | `print("[WARNING] ...")` | `audit/reject_log.py` |
| Fetcher entry points | Four root-level `*_manager.py` files | `sources/*.py` package |
| Documentation | `doc_generator.py` (monolithic) | Extend with datasheet + regen |

### 4.3 Sample-Count Source of Truth

**Kaggle is authoritative.** `manifolds.md` and `PAPER_DATASET_COMPILER.md`
both have stale counts (differ by 10–100× for at least five manifolds).

Resolution: Phase 0 adds `lemgendary sources verify-counts` which queries the
Kaggle `dataset_files_summary` API per manifold and writes authoritative
counts to `manifolds.md` and each `dataset_info.yaml`. All format decisions
in Phase 4 depend on these authoritative counts.

---

## 5. Integration with LemGendary Environment Manager

### 5.1 Delegation Model

The dataset compiler delegates infrastructure to `lem-env` via subprocess.
This mirrors the Sibling Surgery protocol already documented in the
Environment Manager whitepaper §4.1.

```python
# Example delegation pattern (used throughout)
def ensure_environment(project_dir: Path) -> bool:
    result = subprocess.run(
        ["lem-env", "install", "--project", "lemgendary-datasets"],
        cwd=project_dir, capture_output=True, text=True
    )
    return result.returncode == 0
```

### 5.2 Shared Patterns (Mirror Env Manager)

| Concern | Env Manager Pattern | Dataset Compiler Adopts |
| --- | --- | --- |
| CLI framework | Typer + Rich | Typer + Rich |
| CLI exit codes | POSIX (0/1/2/3/4) | Same |
| API framework | FastAPI + uvicorn | FastAPI + uvicorn |
| API prefix | `/api/` | `/api/` |
| API port | 8000 | **8100** (avoid collision) |
| Error format | `{detail, error_code, timestamp}` | Same |
| WebSocket path | `/ws/log` + `/ws/logs` (aliases) | Same |
| Connection manager | `active_connections` list + broadcast | Same |
| Event queue | `asyncio.Queue(maxsize=500)` | Same |
| Event drain | `lifespan` contextmanager | Same |
| Thread→async bridge | `asyncio.run_coroutine_threadsafe` | Same |
| Blocking ops | `loop.run_in_executor` | Same |

### 5.3 Validation Boundary

`lem-env validate --project lemgendary-datasets` is authoritative for
**code quality** (py_compile, zero-emoji, YAML, JSON, markdownlint).

The dataset compiler owns **data quality** validation, exposed under
`lemgendary audit *`:

| Command | Scope | Authority |
| --- | --- | --- |
| `lem-env validate` | Python syntax, lints, YAML/JSON, emoji | Env Manager |
| `lemgendary audit run` | Image headers, resolution, black frames | Dataset Compiler |
| `lemgendary audit dedup` | Exact + perceptual hash dedup | Dataset Compiler |
| `lemgendary audit hardlinks` | Hardlink fraction per manifold | Dataset Compiler |

### 5.4 Cross-Project Sync

Requirements manifest for this project lives in the env-manager as
`requirements-datasets.txt` and is mirrored to `lemgendary-datasets/requirements.txt`
by `lem-env sync`. The dataset compiler never edits its own `requirements.txt`.

### 5.5 Git Hooks

`lem-env setup-hooks` installs the pre-commit hook that calls
`lem-env validate --project lemgendary-datasets`. The dataset compiler does
not manage its own hooks.

---

## 6. Target Architecture

```text
                     ┌─────────────────────────────┐
                     │   lemgendary CLI (thin)     │
                     │   Typer + Rich              │
                     └──────────┬──────────────────┘
                                │  (HTTP if server running, in-process if not)
                     ┌──────────▼──────────────────┐
                     │     api/ (FastAPI)          │
                     │     port 8100               │
                     │     /api/ prefix            │
                     │     ConnectionManager       │
                     │     asyncio.Queue           │
                     └──────────┬──────────────────┘
                                │
                     ┌──────────▼──────────────────┐
                     │     Core Library            │
                     │     (all modules below)     │
                     └──────────┬──────────────────┘
                                │
   ┌────────────────┬───────────┼───────────┬────────────────┐
   │                │           │           │                │
┌──▼───┐      ┌─────▼────┐ ┌────▼─────┐ ┌───▼────┐     ┌─────▼─────┐
│sources│     │converters│ │  audit   │ │formats │     │generators │
│       │     │          │ │          │ │        │     │           │
│hf.py  │     │coco.py   │ │vision.py │ │direct. │     │labels.py  │
│gh.py  │     │parquet.py│ │dedup.py  │ │mds.py  │     │prompts.py │
│gd.py  │     │xml.py    │ │verify.py │ │litdata │     │masks.py   │
│kaggle │     │yolo.py   │ │reject.py │ │wds.py  │     │           │
│       │     │matlab.py │ │          │ │pq.py   │     │           │
│       │     │safetens. │ │          │ │        │     │           │
│       │     │npz.py    │ │          │ │        │     │           │
└───────┘     └──────────┘ └──────────┘ └────────┘     └───────────┘
                                │
                     ┌──────────▼──────────────────┐
                     │     degrade/                │
                     │     blur.py, noise.py,      │
                     │     haze.py, jpeg.py, ...   │
                     └──────────┬──────────────────┘
                                │
                     ┌──────────▼──────────────────┐
                     │     config_schema.py        │
                     │     manifold_registry.db    │
                     └─────────────────────────────┘

                     ┌─────────────────────────────┐
                     │ lem-env (external)          │
                     │ - venv, packages, manifests │
                     │ - code validation gates     │
                     │ - git hooks                 │
                     └─────────────────────────────┘
```

---

## 7. Format Strategy

### 7.1 Container Format Decision Matrix

Every vision manifold gets **one canonical container** plus the always-present
directory layout. Container choice is per-manifold based on:

1. **Hardlink preservation** — tiered gate (§7.3).
2. **Sample count** — >100K strongly prefers a container; <10K stays directory.
3. **Shuffle requirement** — quality / classification / multi-task manifolds
   benefit from MDS's true global shuffle.
4. **Shape variance** — detection/pose (variable bbox/landmark counts) prefers
   LitData.
5. **Fixed-shape throughput** — FFCV only if resolution ladder is abandoned
   (currently not the case for any model).

### 7.2 Full Decision Matrix

Counts below are **provisional** — Phase 0 verifies via Kaggle before Phase 4.

| Manifold | Samples (K) | Container | Image fmt | Hardlink % | Rationale |
| --- | ---: | --- | --- | ---: | --- |
| `ForexUniverse` | 26,818 | Parquet+Zstd | n/a | n/a | Already optimal; frozen |
| `NimaAesthetic` | 321 | **MDS** | WebP 92 | 0% | Large, single-image, shuffle benefits |
| `NimaTechnical` | 26 | Directory | WebP 92 | 0% | Small; container overhead not amortized |
| `NimaAuthenticity` | 209 | **MDS** | WebP 92 | 0% | Larger than manifolds.md claimed |
| `UpnV2` | 1,378 | Directory + hardlinks | WebP 92 | high | Hardlinks recover 1.06 TB |
| `FilmRestorer` | 68 | Directory + hardlinks | WebP 92 | high | Same |
| `CodeFormer` | 22 | Directory + hardlinks | WebP 92 | medium | Small; hardlinks preserve parity |
| `ParseNet` | 854 | **MDS** | WebP 92 + mask WebP-lossless | low | Fixed 512px; masks compress well losslessly |
| `RetinaFaceMobileNet` | 854 | **LitData** | WebP 92 | 0% | Variable landmark counts |
| `FfaNetIndoor` | 196 | Directory + hardlinks | WebP 92 | high | Hardlinks |
| `FfaNetOutdoor` | 217 | Directory + hardlinks | WebP 92 | high | Hardlinks |
| `MirNetLowLight` | 15 | Directory | WebP 92 | low | Small |
| `MirNetExposure` | 1,416 | Directory + hardlinks | WebP 92 | high | Now 100× larger than manifolds.md; hardlinks decisive |
| `MprNetDeraining` | 248 | Directory + hardlinks | WebP 92 | high | Hardlinks |
| `NafNetDebluring` | 26 | Directory + hardlinks | WebP 92 | medium | Hardlinks |
| `NafNetDenoising` | 8 | Directory | WebP 92 | low | Very small |
| `UltraZoom` | 18 | Directory | WebP 92 | low | Small; HR targets are bottleneck |
| `YoloV8n` | 154 | **LitData** | WebP 92 | 0% | Variable resolution + mosaic aug |
| `ProfessionalMultitaskRestoration` | 344 | **MDS** (pending hardlink audit) | WebP 92 | TBD | Unified shuffle across 11 sub-tasks |
| `ClassificationMasterManifold` | 788 | **MDS** | WebP 92 | 0% | Largest single-image set |

Legend:

- **MDS** — MosaicML Streaming: Zstd, true shuffle, mid-epoch resume.
- **LitData** — PyTorch-native, variable-shape friendly.
- **FFCV** — Deferred; incompatible with res-ladder training.
- **Directory + hardlinks** — Canonical, preserves dedup.
- **Parquet+Zstd** — Tabular only.

### 7.3 Hardlink Gate (Tiered)

Before any non-directory container is written, `lemgendary audit hardlinks`
runs automatically and classifies:

| Hardlink fraction | Verdict | Action |
| ---: | --- | --- |
| **< 5%** | PROCEED | Negligible duplication cost; container compression wins. |
| **5–25%** | WARN | Display estimated space delta (duplication cost vs. compression win). Require `--force-duplicate` to proceed. |
| **> 25%** | BLOCK | Catastrophic duplication. Container write refused without explicit `--force-duplicate --accept-space-loss`. |

Rationale for the 5%/25% thresholds:

- WebP q=92 images are already near-incompressible; Zstd gains on top are
  ~3–5%. Below 5% hardlinks, container compression win dominates.
- Above 5%, the duplication cost eats into compression savings. Functional
  wins (shuffle, resumption) may still justify container — hence WARN not BLOCK.
- Above 25%, the container is unambiguously a space loss regardless of
  functional wins. Hard block.

The audit output includes an estimated space delta:

```text
[FORMAT-AUDIT] upn_v2
  Total targets: 1,378,070
  Hardlinked targets: 1,198,830 (87.0%)
  Estimated space delta if container written:
    - Container compression win: ~42 GB (3% of 1.4 TB)
    - Hardlink duplication cost: ~1.06 TB
    - NET: -1.02 TB (container is 1.02 TB WORSE)
  Verdict: BLOCK
```

### 7.4 Diffusion / VLM (Future Manifolds)

Not currently in production. When added:

| Manifold type | Container | Image fmt inside |
| --- | --- | --- |
| Diffusion | WebDataset (.tar) | WebP 92 |
| Diffusion (bulk) | Parquet (Zstd) | WebP 92 in `image_bytes` |
| VLM | Parquet (Zstd) | WebP 92 + structured conversation JSON |

### 7.5 Forex

Frozen. Parquet + Zstd. `ParquetRowGroupCache` already in training suite.
No changes in this roadmap.

---

## 8. Image Transcoding Strategy

### 8.1 Format Choices

| Format | Lossy ratio vs JPEG | Decode cost vs JPEG | Alpha | Recommendation |
| --- | ---: | ---: | --- | --- |
| **WebP 92** | 0.65–0.75× | 2.0× | Yes | **Default** for all vision manifolds |
| WebP lossless | 0.55–0.65× vs PNG | 2.5× | Yes | **Mandatory** for masks |
| JPEG 95 | 1.00× (baseline) | 1.0× | No | Opt-in `--image-format keep` for local 4GB-GPU training |
| PNG | n/a | n/a | Yes | Only kept when source has alpha and user opts out |

**AVIF is not offered.** Research as of 2026 confirms 5–10× slower decode than
WebP and 5–8× slower encode. For a training-bound pipeline, the decode cost
outweighs the ~20–30% additional file-size savings. Moved to §24 Deferred.

### 8.2 Default Policy

- **Images** → WebP quality 92.
- **Targets** (restoration ground truth) → WebP quality 95.
- **Masks** → WebP lossless.
- **JPEG with alpha** → composited on white then WebP (lossy).
- **PNG with alpha** → WebP lossless (preserve transparency).

### 8.3 Per-Compile Override

```bash
lemgendary compile --model nima_aesthetic --image-format webp --image-quality 92
lemgendary compile --model nafnet_denoising --image-format keep    # preserve JPEG
```

### 8.4 Backwards Compatibility

Transcoding is **opt-in via CLI flag or `--from-config`**. Manifolds compiled
without the flag retain JPEG/PNG. `migrate_manifold_image_format.py` (Phase 3)
transcodes an existing manifold in place with metadata preserved
(registry hash chain maintained).

---

## 9. Registry Promotion (`manifold_registry.db`)

### 9.1 Current State

`manifold_compile.py` writes registry to `.cache/registry_<name>.db` — a
helper for resumption.

### 9.2 Target State

Registry becomes **first-class**, stored **inside the manifold folder**:

```text
LemGendizedNimaAesthetic/
├── images/
├── labels/
├── mds/
├── manifold_registry.db       ← NEW LOCATION
├── dataset_info.yaml
├── index.json
└── README.md
```

### 9.3 Schema Expansion

```sql
CREATE TABLE samples (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    task TEXT NOT NULL,
    split TEXT NOT NULL,
    hash TEXT,                          -- BLAKE3 content hash
    perceptual_hash TEXT,               -- pHash for near-dup detection
    nima_score REAL,
    quality_dist BLOB,
    caption TEXT,
    style_tag TEXT,
    clip_latent BLOB,
    img_format TEXT,                    -- 'webp', 'jpeg', 'png'
    img_size_bytes INTEGER,
    target_size_bytes INTEGER,
    mask_size_bytes INTEGER,
    is_hardlinked INTEGER DEFAULT 0,    -- 1 if target is hardlink to image
    reject_code TEXT,                   -- NULL if accepted
    audit_trail TEXT,                   -- JSON: list of audit results
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cluster_id INTEGER DEFAULT -1
);

CREATE INDEX idx_samples_hash ON samples(hash);
CREATE INDEX idx_samples_phash ON samples(perceptual_hash);
CREATE INDEX idx_samples_source ON samples(source);
CREATE INDEX idx_samples_task ON samples(task);
CREATE INDEX idx_samples_reject ON samples(reject_code);

CREATE TABLE audit_events (
    id INTEGER PRIMARY KEY,
    sample_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,           -- 'audit', 'transcode', 'dedup', 'label'
    event_data TEXT,                    -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sample_id) REFERENCES samples(id)
);

CREATE TABLE reject_log (
    id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    sample_name TEXT NOT NULL,
    reject_code TEXT NOT NULL,
    reason TEXT,
    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 9.4 Registry-Backed Operations

- **Dedup** — Phase 2
- **Resumption** — Already implemented; keep
- **Doc generation** — Phase 5 reads registry for accurate counts
- **Re-sharding** — Phase 4 reads registry to know sample→shard mapping
- **Compliance** — Phase 5 exports reject log into README
- **Re-manifold derivation** — Phase 6 (degradation) reads source registry

### 9.5 Backwards Compatibility

Existing manifolds without registry DB are detected and one is built by
scanning `images/`, `labels/`, `targets/`, `masks/` during Phase 0's
`lemgendary sources verify-counts` pass.

---

## 10. API Surface (FastAPI)

### 10.1 Server Configuration

```bash
# Default binding: http://127.0.0.1:8100
lemgendary server start --host 127.0.0.1 --port 8100
```

Port 8100 avoids collision with env-manager (port 8000). Both can run
concurrently.

### 10.2 Endpoints

#### **Health / Config**

```text
GET    /api/health
GET    /api/config
PUT    /api/config
POST   /api/config/validate
```

**Jobs** (long-running tasks)

```text
POST   /api/jobs/{type}              # type: compile|reduce|sync|fetch|transcode|audit|dedup|label|mask|degrade|modernize|format-write
GET    /api/jobs/{id}
GET    /api/jobs                    # list, filterable by status/type
DELETE /api/jobs/{id}
POST   /api/jobs/{id}/cancel
WS     /api/jobs/{id}/stream         # live log streaming
```

**Datasets** (local manifolds)

```text
GET    /api/datasets                 # list local
GET    /api/datasets/{name}
GET    /api/datasets/{name}/info     # dataset_info.yaml
GET    /api/datasets/{name}/count    # from registry
GET    /api/datasets/{name}/rejects  # reject log summary
POST   /api/datasets/{name}/validate
POST   /api/datasets/{name}/transcode
POST   /api/datasets/{name}/regenerate-docs
POST   /api/datasets/{name}/reshard  # format rewrite
DELETE /api/datasets/{name}/samples  # with body: list of names to purge
```

**Sources** (raw sets)

```text
GET    /api/sources                  # list all raw sources
GET    /api/sources/{ref}
POST   /api/sources/{ref}/fetch
POST   /api/sources/{ref}/verify
POST   /api/sources/{ref}/purge      # delete raw after confirm
```

**Kaggle** (raw sets)

```text
GET    /api/kaggle/{slug}/status
GET    /api/kaggle/{slug}/versions
POST   /api/kaggle/{slug}/sync       # push local → Kaggle
POST   /api/kaggle/{slug}/get        # pull Kaggle → local
GET    /api/kaggle/{slug}/count      # authoritative count from API
```

**Gates** (verification)

```text
POST   /api/gates/hardlink-audit     # body: {model}
POST   /api/gates/parity-compile     # body: {model, ref_hash}
POST   /api/gates/roundtrip          # body: {model, format}
```

**Environment Manager Integration** (example)

```text
GET    /api/env/status               # passthrough to lem-env audit
GET    /api/env/validate             # passthrough to lem-env validate
POST   /api/env/install              # passthrough to lem-env install
```

### 10.3 WebSocket Telemetry

Following the env-manager pattern exactly:

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)
```

WebSocket paths (aliases, mirroring env-manager):

```text
ws://127.0.0.1:8100/ws/log
ws://127.0.0.1:8100/ws/logs
```

On connect, the client receives the last 20 buffered events, then continues
to receive new events as they are emitted.

### 10.4 Event Schema

```json
{
  "timestamp": "2026-09-16T14:22:02.123456Z",
  "job_id": "compile-nima_aesthetic-001",
  "job_type": "compile",
  "step_number": 3,
  "total_steps": 7,
  "step_name": "Audit & Transcode",
  "status": "info",
  "message": "Transcoding 12,450 images to WebP q=92...",
  "data": {
    "model": "nima_aesthetic",
    "progress_pct": 42.3,
    "eta_seconds": 287
  }
}
```

Event status values (matching env-manager):

- `info` — Informational milestone
- `success` — Step completed cleanly
- `warning` — Step completed with advisory notice
- `error` — Fatal error in step execution

### 10.5 Error Format

Matching env-manager's format exactly:

```json
{
  "detail": "Manifold 'upn_v2' blocked: 87% hardlinked targets",
  "error_code": "FORMAT_BLOCKED_HARDLINK",
  "timestamp": "2026-09-16T14:22:02Z"
}
```

| HTTP Status | Code String | Description |
| --- | --- | --- |
| 200 OK | `SUCCESS` | Request processed successfully |
| 400 Bad Request | `VALIDATION_ERROR` | Request body or query params failed schema validation |
| 404 Not Found | `MANIFOLD_NOT_FOUND` | Specified manifold does not exist |
| 409 Conflict | `JOB_ACTIVE` | Conflicting job currently executing |
| 500 Server Error | `INTERNAL_FAILURE` | Unhandled exception |

### 10.6 Authentication

Local-only by default: `127.0.0.1:8100`. Optional token auth via
`.lgd_api_token` for CPA GUI to reach it over network. Token stored alongside
`.kaggle_token`.

### 10.7 Lifespan Handler

Matching env-manager's pattern:

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    drain_task = asyncio.create_task(_drain_event_queue())
    try:
        yield
    finally:
        drain_task.cancel()
        try:
            await drain_task
        except asyncio.CancelledError:
            pass
```

---

## 11. CLI Surface (`lemgendary`)

### 11.1 Command Tree

```text
lemgendary
├── compile          Compile a manifold from raw sources
├── reduce           Create a reduced variant
├── modernize        Retire 'Large' suffix, rename folders
├── sync
│   ├── push         Push local manifold → Kaggle
│   └── pull         Pull Kaggle manifold → local
├── fetch            Fetch a raw source (hf/gh/gd/kaggle)
├── transcode        Convert images in existing manifold
├── audit
│   ├── run          Full audit pass
│   ├── hardlinks    Hardlink fraction report
│   ├── dedup        Exact + perceptual
│   └── verify       Header + decode + truncation
├── format
│   ├── write        Write additional container format
│   └── migrate      Convert existing manifold between formats
├── label            Smart label generation
├── prompt           Smart prompt generation
├── mask             Smart mask generation
├── degrade          Synthesis of derived manifolds
├── docs
│   ├── regen        Regenerate README/yaml/index
│   └── manifolds    Rebuild manifolds.md from registry
├── env              Passthrough to lem-env
│   ├── status       → lem-env audit --fast
│   ├── validate     → lem-env validate --project lemgendary-datasets
│   └── install      → lem-env install --project lemgendary-datasets
├── server
│   ├── start
│   ├── stop
│   └── status
├── config
│   ├── show
│   └── validate
└── version
```

### 11.2 Server-Optional Behavior

`lemgendary` checks for a running server at `http://127.0.0.1:8100`. If found,
all commands route through the API. If not found, commands run in-process.

Deterministic: `LEMGENDARY_FORCE_LOCAL=1` skips server detection;
`LEMGENDARY_FORCE_REMOTE=http://host:port` forces remote.

### 11.3 Example Invocations

```bash
# Modernize (suffix removal)
lemgendary modernize --all --dry-run
lemgendary modernize --datasets nima_technical,nima_aesthetic
lemgendary modernize --all --yes

# Compile with transcoding + modern format
lemgendary compile --model nima_aesthetic \
                   --image-format webp --image-quality 92 \
                   --also-format mds

# Audit and dedup
lemgendary audit run --model classification_master --level perceptual
lemgendary audit hardlinks --model upn_v2

# Transcode existing manifold
lemgendary transcode --model nima_technical --to webp --quality 92

# Format migration (in place, non-destructive)
lemgendary format migrate --model nima_technical --to mds --keep-directory

# Smart generation
lemgendary label --model parsenet --strategy sam
lemgendary mask  --model parsenet --strategy sam --max-samples 5000
lemgendary prompt --model diffusion_master

# Degradation synthesis
lemgendary degrade --source div2k --profile motion-blur+gauss-noise --intensity medium \
                   --output LemGendizedNafNetDebluringSynthetic

# Environment Manager passthrough
lemgendary env validate

# Server
lemgendary server start --host 127.0.0.1 --port 8100
lemgendary server status
```

### 11.4 Exit Codes

Matching env-manager's POSIX convention:

| Exit Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | General failure |
| 2 | Validation error |
| 3 | Missing prerequisites |
| 4 | Network / IO error |

---

## 12. Phase 0 — Modernize (Suffix Removal)

**Effort**: 1–2 days. **Risk**: Low. **Blocks**: Phase 1.

### Deliverables

1. **New** `modernize_manifold.py`
2. **Modify** `doc_generator.py` — add modern-name entries to `MANIFOLD_TASK_MAP`; emit relative `path:` in `dataset_info.yaml`
3. **Modify** `manifold_reduce.py` — replace `.endswith("Large")` filter with `_has_manifold_data()`
4. **Modify** `lemgendary_datasets_hub.ps1` — bump to v5.3; add menu `4. [MODERNIZE]`
5. **Modify** `unified_data.yaml` — programmatically only
6. **Modify** `README.md` — version bump + section
7. **New** `regenerate_manifolds_md.py` — rebuilds `manifolds.md` from Kaggle-authoritative counts
8. **Modify** `manifolds.md` — regenerated by #7

### Rename Eligibility

Only datasets with actual data (verified via Kaggle):

| Current | Target |
| --- | --- |
| `LemGendizedForexUniverseLarge` | `LemGendizedForexUniverse` |
| `LemGendizedNimaAestheticLarge` | `LemGendizedNimaAesthetic` |
| `LemGendizedNimaTechnicalLarge` | `LemGendizedNimaTechnical` |
| `LemGendizedYoloV8nLarge` | `LemGendizedYoloV8n` |
| `LemGendizedProfessionalMultitaskRestorationLarge` | `LemGendizedProfessionalMultitaskRestoration` |

Any others found with data during the Kaggle verification are added
automatically.

### Kaggle Count Verification

`regenerate_manifolds_md.py` calls Kaggle `dataset_files_summary` per public
slug, writes actual counts to `manifolds.md` and each `dataset_info.yaml`.
**Phase 4 depends on these counts.**

### Gate 0

- [ ] `py_compile` passes for all modified files
- [ ] Hub menu shows `4. [MODERNIZE]`
- [ ] Test rename of `LemGendizedNimaTechnicalLarge` → `LemGendizedNimaTechnical` (folder + metadata + Kaggle)
- [ ] Partial run: `name_suffix` stays `Large` if not all confirmed
- [ ] Full run: `name_suffix` becomes `""`
- [ ] Post-migration compile produces suffix-free name
- [ ] `manifolds.md` regenerated with Kaggle-authoritative counts

---

## 13. Phase 1 — Foundation

**Effort**: ~1 week. **Risk**: Low. **Blocks**: 2, 3, 4, 5, 6, 7, 8.

### 13.1 Pydantic Config Schema

**New** `config_schema.py`:

```python
class SourceRef(BaseModel):
    ref: str
    tag: Literal["sfw", "nsfw", "anime_nsfw", "general_nsfw", "sfw_baseline"] = "sfw"

class ImageFormatPolicy(BaseModel):
    format: Literal["webp", "jpeg", "png", "keep"] = "webp"
    quality: int = 92
    mask_format: Literal["webp-lossless", "png"] = "webp-lossless"
    target_quality: int = 95

class ContainerPolicy(BaseModel):
    primary: Literal["directory", "mds", "litdata", "webdataset", "parquet"] = "directory"
    extra: list[str] = []
    preserve_hardlinks: bool = True

class DatasetEntry(BaseModel):
    name: str
    kaggle_ref: str | None
    val_split: float = 0.12
    labeling: bool = True
    vetting: bool = True
    task_override: str | None
    dataset_type: Literal["vision", "forex", "diffusion", "vlm"] = "vision"
    acquisition_mode: Literal["hf", "kaggle", "gh", "gdrive", "mt5_terminal", "local"] = "kaggle"
    nsfw_ratio: float = 0.0
    refs: list[SourceRef] = []
    image_format: ImageFormatPolicy = ImageFormatPolicy()
    container: ContainerPolicy = ContainerPolicy()
    pairs: list[str] | None
    timeframe_rungs: list[int] | None
    start_date: str | None
    lookback_bars: int | None

class UnifiedData(BaseModel):
    _registry_metadata: RegistryMetadata
    datasets: dict[str, DatasetEntry]
```

### 13.2 Registry Promotion

- Move `.cache/registry_<name>.db` → `<manifold>/manifold_registry.db`
- Expand schema per §9.3
- Migration tool for existing manifolds: `lemgendary registry migrate --model <name>`
- Backwards-compat shim during transition (read from both locations for one release)

### 13.3 Module Extraction

Full extraction of the concerns listed in §4.2:

- `audit/` — package skeleton (implementation in Phase 2)
- `converters/` — extract `parse_*` functions
- `formats/` — package skeleton (implementation in Phase 4)
- `generators/` — package skeleton (implementation in Phase 5)
- `degrade/` — package skeleton (implementation in Phase 6)

At the end of Phase 1, `compiler_core.py` imports from these packages but
the packages' internals are thin wrappers around existing code. **Byte-parity
with pre-Phase-1 output is mandatory** (see Gate 1).

### 13.4 Fetcher Packaging

```text
sources/
├── __init__.py
├── base.py       # shared arg parsing / auth helpers
├── hf.py         ← hf_manager.py
├── gh.py         ← gh_manager.py
├── gd.py         ← gd_manager.py
└── kaggle.py     ← kaggle_manager.py
```

Hub PS1 changes four path lines. ScriptBlocks unchanged (unified dispatcher
deferred to Phase 7).

### 13.5 CLI Skeleton

New `lemgendary.py` with all subcommands stubbed (returning `NotImplementedError`
except for existing ops which pass through to current modules). Uses Typer +
Rich, matching `lem-env`'s structure.

### 13.6 Env-Manager Passthrough

Add `lemgendary env` subcommands that shell out to `lem-env`:

```python
@app.command()
def env_validate():
    """Delegate code validation to lem-env."""
    result = subprocess.run(
        ["lem-env", "validate", "--project", "lemgendary-datasets"],
        check=False
    )
    raise typer.Exit(code=result.returncode)
```

### Gate 1

- [ ] `lemgendary config validate` passes on current `unified_data.yaml`
- [ ] Malformed YAML produces clear error and aborts
- [ ] **Byte-parity compile**: compile `nima_technical` before and after Phase 1; `index.json` MD5 + directory tree hash match
- [ ] Registry DB created in new location for a test compile; `lemgendary registry migrate` succeeds for an existing manifold
- [ ] `python -c "import sources.hf, sources.gh, sources.gd, sources.kaggle"` passes
- [ ] `lemgendary env validate` correctly delegates to `lem-env`
- [ ] Hub menu 3 (Kaggle sync) still works after fetcher packaging
- [ ] `lemgendary version`, `lemgendary --help`, `lemgendary config show` produce sane output

---

## 14. Phase 2 — Audit & Dedup

**Effort**: ~2 weeks. **Risk**: Low (byte-parity gate). **Blocks**: 4, 5.

### 14.1 Vision Auditor

**New** `audit/vision_audit.py`. Methods:

- `verify_header(bytes) -> bool` — magic-number sniff (PNG/JPEG/WebP/TIFF)
- `audit_image(img) -> AuditResult` — resolution floor, mode, black-frame, aspect ratio
- `audit_bbox(bbox, w, h) -> list[str]` — out-of-bounds, negative, degenerate
- `audit_pairs(img, tgt) -> list[str]` — dimension match, mode match
- `audit_mask(mask) -> list[str]` — value range, palette validity

Every method returns structured `AuditResult` with `.valid`, `.reason`, `.code`.

Reject codes (canonical):

```text
ERR_RES_UNDERFLOW
ERR_RES_OVERFLOW
ERR_BLACK_FRAME
ERR_WHITE_FRAME
ERR_ASPECT_EXTREME
ERR_PAIR_MISMATCH
ERR_PAIR_MODE_MISMATCH
ERR_MASK_INVALID
ERR_BBOX_OUT_OF_BOUNDS
ERR_BBOX_DEGENERATE
ERR_KEYPOINT_OUT_OF_BOUNDS
ERR_TRUNCATED
ERR_HEADER_INVALID
ERR_ZERO_BYTES
ERR_DECODE_FAILED
ERR_EXACT_DUP
ERR_NEAR_DUP
ERR_LABEL_MISSING
ERR_LABEL_MALFORMED
```

### 14.2 Dedup Engine

**New** `audit/dedup.py`. Two levels:

- **Exact**: BLAKE3 hash of raw file bytes. Cost: ~1 GB/s/core.
- **Perceptual**: pHash + dHash + wHash, Hamming-distance threshold. Cost: ~200 img/s/core.

Policy:

- Exact-dup in same source → drop (reject code `ERR_EXACT_DUP`)
- Near-dup (Hamming ≤ 5) in same source → drop, log both
- Cross-source near-dup → log warning, keep both

Opt-in via `--dedup {none,exact,perceptual,both}`; default `exact`.

### 14.3 Verification Engine

**New** `audit/verify.py`. Decode-and-re-encode round-trip for every image.
Runs in full-audit mode; in normal compiles only header + `verify()` runs.

### 14.4 Reject Log

**New** `audit/reject_log.py`. Writes to `manifold_registry.db.reject_log`
table. Exports summary to `dataset_info.yaml`, `README.md`, `rejects.jsonl`.

### 14.5 Hardlink Auditor

**New** `audit/hardlinks.py`. Reports per-manifold hardlink fraction and
estimated space delta. Used as pre-flight gate for Phase 4.

### 14.6 Subcommands

```bash
lemgendary audit run --model nima_aesthetic --level full
lemgendary audit run --model nima_aesthetic --level fast
lemgendary audit hardlinks --model upn_v2
lemgendary audit dedup --model classification_master --level perceptual
lemgendary audit verify --model nafnet_denoising --roundtrip
lemgendary audit purge --model nima_aesthetic --confirm
```

### Gate 2

- [ ] **Byte-parity compile**: `nima_technical` produces identical output to Phase 1
- [ ] Dedup catches known duplicates in `classification_master` test subset
- [ ] Reject log populated for a deliberate-corruption test source
- [ ] `dataset_info.yaml` gains `rejected` + `reject_breakdown`
- [ ] Hardlink audit correctly identifies `upn_v2` as >25% hardlinked

---

## 15. Phase 3 — Image Transcoding

**Effort**: ~1 week. **Risk**: Medium (lossy → quality floor). **Blocks**: 4.

### 15.1 Transcoding Engine

**New** `formats/transcode.py`:

```python
class ImageTranscoder:
    def __init__(self, policy: ImageFormatPolicy): ...
    def transcode(self, img: Image.Image, kind: Literal["image","target","mask"]) -> tuple[bytes, str]:
        """Returns (encoded_bytes, format_name)."""
```

- **Images** → WebP q=92 (default)
- **Targets** → WebP q=95
- **Masks** → WebP lossless
- **JPEG-with-alpha** → composite on white → WebP lossy
- **PNG-with-alpha** → WebP lossless

### 15.2 In-Flight Transcoding

`process_image()` writes transcoded bytes directly. No intermediate JPEG.

### 15.3 Retroactive Migration

**New** `migrate_manifold_image_format.py`:

- Reads existing `images/`, `targets/`, `masks/`
- Transcodes each in place (writes temp, atomic rename)
- Updates registry with new `img_format` and `img_size_bytes`
- Preserves hardlinks (transcode the link target, all links see the new bytes)
- Reports per-manifold: original size, new size, savings

### Gate 3

- [ ] WebP round-trip on `nima_technical` produces visually-identical output (SSIM ≥ 0.995)
- [ ] Size reduction: WebP q=92 saves ≥ 25% vs JPEG q=95 on the test manifold
- [ ] Masks: WebP lossless preserves exact pixel values (byte-compare mask arrays)
- [ ] Hardlinks preserved through transcode (test on `upn_v2` subset)
- [ ] `migrate_manifold_image_format.py` on `nima_technical` produces updated registry

---

## 16. Phase 4 — Format Layer

**Effort**: ~2 weeks. **Risk**: Medium. **Blocks**: 5, 8.

### 16.1 Plugin Interface

**New** `formats/base.py`:

```python
class Sample(NamedTuple):
    name: str
    image_bytes: bytes
    image_format: str
    target_bytes: bytes | None
    mask_bytes: bytes | None
    label: dict
    metadata: dict

class Writer(Protocol):
    def open(self, output_root: Path, config: ContainerPolicy) -> None: ...
    def write(self, sample: Sample) -> None: ...
    def close(self) -> None: ...
```

Implementations:

- `formats/directory.py` — canonical; preserves hardlinks
- `formats/mds.py` — MosaicML Streaming
- `formats/litdata.py` — PyTorch LitData
- `formats/webdataset.py` — existing diffusion shard writer
- `formats/parquet.py` — forex only

### 16.2 Multi-Format Write

`manifold_compile.py` accepts `--also-format mds,litdata` and writes each in
addition to canonical directory output. Canonical is always written first.

### 16.3 Migration Tool

**New** `migrate_manifold_format.py`:

- Reads existing directory manifold
- Writes new container into `<manifold>/mds/` or `<manifold>/litdata/`
- Verifies round-trip (sample count + per-sample hash)
- Never deletes source directory without `--purge-source` + confirmation

### 16.4 Hardlink Pre-Flight

Before any `--also-format` write, `lemgendary audit hardlinks` runs
automatically. Tiered gate per §7.3 applies.

### 16.5 Training Suite Coordination

This phase ships **writer only**. Training suite reader is a separate
release in `lemgendary-training-suite`.

### Gate 4

- [ ] MDS writer on `nima_technical` produces valid MDS
- [ ] Round-trip: read MDS, compare sample count + hash per sample against directory
- [ ] LitData writer on `retinaface_mobilenet` subset produces valid LitData
- [ ] Hardlink block: `upn_v2` refuses container write without `--force-duplicate`
- [ ] `migrate_manifold_format.py` works on a frozen directory manifold
- [ ] Zstd compression ratios documented for each migrated manifold

---

## 17. Phase 5 — Smart Generation

**Effort**: ~2 weeks. **Risk**: Medium (GPU-bound). **Blocks**: 6.

### 17.1 Label Generation

**New** `generators/labels.py`:

- **Diffusion** → BLIP caption (reuse `CaptionSentry`)
- **Detection** → YOLO auto-label (reuse `AutoLabeler`)
- **Segmentation** → ParseNet inference
- **Classification** → CLIP zero-shot
- **Quality** → NIMA (reuse `QualitySentry`)
- **Style** → CLIP style tag (reuse `CLIPManifold`)

### 17.2 Prompt Generation

**New** `generators/prompts.py`:

- Input: image + caption + style tag + CLIP features
- Output: structured prompt for diffusion training
- Format: `{subject}, {style}, {lighting}, {camera}, {quality_tokens}`

### 17.3 Mask Generation

**New** `generators/masks.py`:

- **Face parsing** → ParseNet
- **Generic object** → SAM v2
- **Portrait** → MODNet / RobustVideoMatting

### 17.4 CLI

```bash
lemgendary label  --model <name> --strategy blip
lemgendary prompt --model <name> --template diffusers-v1
lemgendary mask   --model <name> --strategy sam --confidence 0.85
```

### Gate 5

- [ ] Label generation on a 1000-sample test subset produces valid labels
- [ ] Prompt generation produces non-empty, non-repetitive prompts
- [ ] Mask generation produces valid single-channel masks
- [ ] All generated content is registered in `manifold_registry.db`

---

## 18. Phase 6 — Degradation Engine

**Effort**: ~2 weeks. **Risk**: Medium. **Blocks**: none (independent).

### 18.1 Scope Clarification

**Compiler-time degradation** (this phase) = synthesize derived manifolds
from clean sources. Example: take DIV2K, apply motion blur, output
`LemGendizedNafNetDebluringSynthetic` with degraded images + clean targets.

**Training-time augmentation** (not this phase) = on-the-fly distortion
during training. Lives in `lemgendary-training-suite`.

### 18.2 Degradation Profiles

**New** `degrade/`:

- `blur.py` — Gaussian, motion-linear, defocus, box
- `noise.py` — Gaussian, Poisson, salt-pepper, ISO-calibrated
- `haze.py` — atmospheric scatter
- `rain.py` — rain streaks + droplets
- `jpeg.py` — JPEG quantization artifacts
- `lowlight.py` — gamma + Poisson + readout noise
- `downsample.py` — bicubic / bilinear / Lanczos
- `film.py` — scratches, dust, grain, color fade

Composable: `--profile blur.gauss(σ=2)+noise.gauss(σ=0.05)+jpeg(q=40)`

### 18.3 CLI

```bash
lemgendary degrade --source div2k --profile motion-blur+iso-noise \
                   --intensity medium \
                   --output LemGendizedNafNetDebluringSynthetic \
                   --pairs 50000
```

### Gate 6

- [x] Degradation pipeline on 1000 DIV2K images produces expected visual results
- [x] Deterministic with fixed seed
- [x] Registry records provenance
- [x] Derived manifold is a valid compile target

---

## 19. Phase 7 — API + CLI Unification

**Effort**: ~2 weeks. **Risk**: Medium (new service). **Blocks**: 8.

### 19.1 FastAPI Server

**New** `api/`:

```text
api/
├── __init__.py
├── server.py          # FastAPI app + uvicorn entry
├── jobs.py            # Job queue, status tracking
├── auth.py            # Token auth
├── events.py          # ConnectionManager, event queue
├── routes/
│   ├── health.py
│   ├── config.py
│   ├── jobs.py
│   ├── datasets.py
│   ├── sources.py
│   ├── kaggle.py
│   ├── gates.py
│   └── env.py         # Env-manager passthrough
└── models.py          # Pydantic request/response models
```

### 19.2 Server Startup

```python
# api/server.py
app = FastAPI(
    title="LemGendary Dataset Compiler API",
    version="1.0.0",
    description="REST and WebSocket sidecar service for LemGendary AI Studio.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 19.3 Job Queue

In-process queue (asyncio + ThreadPoolExecutor). Long-running compiles run
in background threads, jobs report status + log via WebSocket.

Persistent across restarts: job state stored in `.lgd_server/jobs.db`
(SQLite). On restart, running jobs are marked `interrupted` with resume
instructions.

### 19.4 CLI Shell

`lemgendary.py` becomes a thin wrapper:

1. Detect server at `127.0.0.1:8100`
2. If running → POST to API, stream log via WebSocket
3. If not running → import core library, run in-process
4. Same code path via shared core

### 19.5 Log Streaming

Server writes all job logs to `.lgd_server/logs/<job_id>.log`. WebSocket
streams tail. CLI attaches and renders with Rich.

### 19.6 Env-Manager Integration Endpoints

```python
@app.get("/api/env/status")
async def get_env_status():
    """Passthrough to lem-env audit --fast."""
    result = await loop.run_in_executor(
        None,
        lambda: subprocess.run(
            ["lem-env", "audit", "--fast"],
            capture_output=True, text=True
        )
    )
    return {"status": "success", "output": result.stdout}

@app.get("/api/env/validate")
async def validate_codebase():
    """Passthrough to lem-env validate --project lemgendary-datasets."""
    result = await loop.run_in_executor(
        None,
        lambda: subprocess.run(
            ["lem-env", "validate", "--project", "lemgendary-datasets"],
            capture_output=True, text=True
        )
    )
    return {"status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout}
```

### Gate 7

- [x] `lemgendary server start` launches on 8100
- [x] `lemgendary compile` while server running routes through API
- [x] `lemgendary compile` with server stopped runs in-process
- [x] WebSocket log stream shows real-time progress
- [x] Job state survives server restart
- [x] OpenAPI docs at `/docs` render correctly
- [x] Token auth blocks unauthorized requests
- [x] `lemgendary env validate` correctly delegates to `lem-env`

---

## 20. Phase 8 — CPA Integration Prep

**Effort**: ~1 week. **Risk**: Low. **Blocks**: none.

### 20.1 API Contract

Freeze `/api/` schema. Publish `openapi.json` as release artifact.
Semantic versioning on the API surface.

### 20.2 GUI-Friendly Endpoints

```text
GET    /api/gui/state                # single call returning all dashboard data
GET    /api/gui/datasets/with-stats  # datasets + sizes + counts + last modified
GET    /api/gui/jobs/active          # currently running jobs summary
POST   /api/gui/quick-compile        # simplified compile with presets
```

### 20.3 Presets

Named presets shipped in `presets.yaml`:

- `quality-vision` — WebP 92 + MDS + full audit
- `restoration-hardlinked` — Directory + hardlinks + WebP 95
- `detection-variable` — WebP 92 + LitData
- `cloud-archival` — WebP 92 + MDS, no local training

GUI calls `POST /api/jobs/compile {"preset": "quality-vision", "model": "..."}`.

### Gate 8

- [x] `openapi.json` published and validated
- [x] All presets work via API
- [x] GUI team confirms endpoints match CPA needs

---

## 21. Verification Gates Summary

| Gate | Phase | Type | Blocking |
| --- | --- | --- | --- |
| 0 | Modernize | Functional | 1 |
| 1 | Foundation | **Byte-parity** | 2, 3, 4, 5, 6, 7, 8 |
| 2 | Audit & Dedup | **Byte-parity** + functional | 4 |
| 3 | Transcoding | Quality + functional | 4 |
| 4 | Format Layer | Round-trip | 5, 8 |
| 5 | Smart Generation | Functional | 6 |
| 6 | Degradation | Functional | — |
| 7 | API/CLI | Functional | 8 |
| 8 | CPA Prep | Contract | — |

**Byte-parity gates** (1, 2) run a fixed-input compile of `nima_technical`
and compare `index.json` MD5 + full directory tree hash against the
pre-phase baseline. Divergence blocks progression.

---

## 22. Risk Register

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Phase 0 rename breaks training suite hardcoded paths | Medium | High | Grep training suite for `Large` before Gate 0 |
| Phase 0 Kaggle re-upload hits rate limit | Low | Medium | Stagger uploads over 24h |
| Phase 1 registry promotion breaks in-flight compiles | Low | Medium | Read-both-locations shim for one release |
| Phase 2 dedup rejects legitimate cross-source duplicates | Medium | Low | Configurable threshold; log-only default for cross-source |
| Phase 3 WebP decode cost penalizes local 4GB-GPU training | Medium | Low | `--image-format keep` opt-out; warned in docs |
| Phase 4 container write duplicates >1 TB of hardlinked targets | Medium | High | Tiered hardlink gate blocks automatically |
| Phase 4 MDS incompatible with training suite at rollout | High | Medium | Parallel-write; training suite continues on directory |
| Phase 5 SAM mask generation is GPU-heavy on 4GB cards | High | Low | Batch size 1; CPU fallback |
| Phase 6 degradation non-determinism causes drift | Medium | Medium | Seed every RNG; log seed in registry |
| Phase 7 server port conflicts with env-manager | Low | Low | Port 8100 chosen; both can coexist |
| Phase 8 API contract freezes too early | Low | Medium | Preview period before freeze |

---

## 23. Success Metrics

| Metric | Baseline | Phase 5 Target | Phase 8 Target |
| --- | ---: | ---: | ---: |
| Manifolds with modern names | 0/20 | 20/20 | 20/20 |
| Config errors caught pre-filesystem | ~0% | 100% | 100% |
| Manifolds with reject logs | 0 | all | all |
| Manifolds transcoded to WebP | 0 | all vision | all vision |
| Manifolds with MDS/LitData containers | 0 | 5+ | 5+ |
| Manifolds with hardlink preservation verified | 0 | all | all |
| Reduction in average vision manifold size | 1.0× | ≤0.70× | ≤0.70× |
| `lemgendary` CLI subcommands | ~5 | ~25 | ~30 |
| API endpoints | 0 | ~25 | ~35 |
| Env-manager passthrough endpoints | 0 | 3 | 3 |
| CPA GUI integration | manual | — | API contract |

---

## 24. Deferred / Out of Scope

Explicitly not in this roadmap:

- **AVIF** — Deferred. Research as of 2026 confirms 5–10× slower decode
  than WebP. The additional ~20–30% file-size savings do not justify the
  decode-cost penalty for training-bound pipelines. Revisit only if a
  future hardware decoder (AV1 hardware block) becomes universally available.
- **FFCV (.beton)** — Incompatible with resolution-ladder training.
  Interface stub only.
- **Distributed multi-node compilation** — Single-node only.
- **Celery / Redis job queue** — asyncio + ThreadPoolExecutor is sufficient.
- **Streaming IR (MDS as intermediate)** — Current two-pass pipeline works.
- **Training-time augmentation** — Belongs in training suite.
- **Model training** — Belongs in training suite.
- **Auto-migration of existing manifolds** — Always user-invoked.
- **Venv / package management** — Belongs in `lem-env`.
- **Code validation (py_compile, lint, YAML/JSON)** — Belongs in `lem-env`.
- **Git hooks** — Belongs in `lem-env`.

---

## 25. Implementation Order

```text
Phase 0 ──► Modernize (suffix removal)
             │   Visible win; regenerates manifolds.md from Kaggle
             ▼
Phase 1 ──► Foundation (schema, registry, extraction, fetchers, CLI skeleton,
             │           env-manager passthrough)
             │   Byte-parity gate; blocks everything
             ▼
Phase 2 ──► Audit & Dedup
             │   Byte-parity gate; blocks 4, 5
             ▼
Phase 3 ──► Transcoding
             │   Blocks 4
             ▼
Phase 4 ──► Format Layer
             │   Blocks 5, 8
             ▼
Phase 5 ──► Smart Generation
             │   Blocks 6
             ▼
Phase 6 ──► Degradation Engine
             ▼
Phase 7 ──► API + CLI Unification
             │   Blocks 8
             ▼
Phase 8 ──► CPA Integration Prep
```

Phases 0–8 are strictly sequential. Phase 0 can run in parallel with
planning Phase 1.

---

## 26. File Inventory After Full Migration

```text
lemgendary-datasets/
├── lemgendary.py                       [NEW — Phase 1 skeleton, Phase 7 complete]
├── config_schema.py                    [NEW — Phase 1]
├── modernize_manifold.py               [NEW — Phase 0]
├── regenerate_manifolds_md.py          [NEW — Phase 0]
├── migrate_manifold_format.py          [NEW — Phase 4]
├── migrate_manifold_image_format.py    [NEW — Phase 3]
├── presets.yaml                        [NEW — Phase 8]
├── sources/
│   ├── __init__.py                     [NEW — Phase 1]
│   ├── base.py                         [NEW — Phase 1]
│   ├── hf.py                           [MOVED — from hf_manager.py]
│   ├── gh.py                           [MOVED — from gh_manager.py]
│   ├── gd.py                           [MOVED — from gd_manager.py]
│   └── kaggle.py                       [MOVED — from kaggle_manager.py]
├── audit/
│   ├── __init__.py                     [NEW — Phase 1]
│   ├── vision_audit.py                 [NEW — Phase 2]
│   ├── dedup.py                        [NEW — Phase 2]
│   ├── verify.py                       [NEW — Phase 2]
│   ├── hardlinks.py                    [NEW — Phase 2]
│   └── reject_log.py                   [NEW — Phase 2]
├── converters/
│   ├── __init__.py                     [NEW — Phase 1]
│   ├── base.py                         [NEW — Phase 1]
│   ├── coco.py                         [NEW — Phase 1]
│   ├── parquet.py                      [NEW — Phase 1]
│   ├── xml.py                          [NEW — Phase 1]
│   ├── yolo.py                         [NEW — Phase 1]
│   ├── matlab.py                       [NEW — Phase 1]
│   ├── safetensors.py                  [NEW — Phase 1]
│   └── npz.py                          [NEW — Phase 1]
├── formats/
│   ├── __init__.py                     [NEW — Phase 1]
│   ├── base.py                         [NEW — Phase 1]
│   ├── directory.py                    [NEW — Phase 4]
│   ├── mds.py                          [NEW — Phase 4]
│   ├── litdata.py                      [NEW — Phase 4]
│   ├── webdataset.py                   [NEW — Phase 4]
│   ├── parquet.py                      [NEW — Phase 4]
│   └── transcode.py                    [NEW — Phase 3]
├── generators/
│   ├── __init__.py                     [NEW — Phase 1]
│   ├── labels.py                       [NEW — Phase 5]
│   ├── prompts.py                      [NEW — Phase 5]
│   └── masks.py                        [NEW — Phase 5]
├── degrade/
│   ├── __init__.py                     [NEW — Phase 1]
│   ├── blur.py                         [NEW — Phase 6]
│   ├── noise.py                        [NEW — Phase 6]
│   ├── haze.py                         [NEW — Phase 6]
│   ├── rain.py                         [NEW — Phase 6]
│   ├── jpeg.py                         [NEW — Phase 6]
│   ├── lowlight.py                     [NEW — Phase 6]
│   ├── downsample.py                   [NEW — Phase 6]
│   └── film.py                         [NEW — Phase 6]
├── api/
│   ├── __init__.py                     [NEW — Phase 7]
│   ├── server.py                       [NEW — Phase 7]
│   ├── jobs.py                         [NEW — Phase 7]
│   ├── auth.py                         [NEW — Phase 7]
│   ├── events.py                       [NEW — Phase 7]
│   ├── models.py                       [NEW — Phase 7]
│   └── routes/                         [NEW — Phase 7]
├── compiler_core.py                    [MODIFIED — Phases 1–6]
├── manifold_compile.py                 [MODIFIED — Phases 1, 4]
├── manifold_reduce.py                  [MODIFIED — Phase 0, 1]
├── manifold_sync.py                    [MODIFIED — Phase 0, 1]
├── doc_generator.py                    [MODIFIED — Phases 0, 5]
├── archive_manager.py                  [FROZEN]
├── common_sync.py                      [FROZEN]
├── mt5_pipeline.py                     [FROZEN]
├── convert_forex_manifest.py           [FROZEN]
├── forex_schema.py                     [FROZEN]
├── notebook_generator.py               [FROZEN]
├── models_metadata.yaml                [FROZEN]
├── unified_data.yaml                   [MUTATED by Phase 0]
├── README.md                           [MODIFIED — Phases 0, 5]
├── manifolds.md                        [REGENERATED — Phase 0]
├── models.md                           [FROZEN]
├── lemgendary_datasets_hub.ps1         [MODIFIED — Phases 0, 7]
└── requirements.txt                    [FROZEN — managed by lem-env]
```

---

## 27. Open Questions

Resolve before starting the indicated phase.

**Before Phase 3:**

- Is the training environment consistently compute-bound at the target
  resolutions? If any model is ever data-bound, WebP must be replaced by JPEG
  for that manifold.

**Before Phase 4:**

- Does the training suite need one canonical container per manifold, or can
  it read multiple? Affects whether migration deletes sources.
- Is Kaggle FUSE fast enough to stream MDS directly, or is MDS only useful
  from local NVMe?
- For `ProfessionalMultitaskRestoration`, what is the hardlink fraction
  post-aggregation?

**Before Phase 5:**

- Does the training suite's task classifier route based on filename prefix
  or content? Affects how synthesized labels are emitted.

**Before Phase 7:**

- Does CPA GUI need synchronous job execution (blocking HTTP call) or
  async (job ID + WS stream)? The latter is strongly preferred.
- Is API access localhost-only or must it work over LAN/VPN?

**Before Phase 8:**

- Is the CPA GUI a separate process (uses API) or embedded (imports
  Python directly)?
- What is the CPA tech stack? Affects whether we ship an OpenAPI spec or a
  Python SDK.

---

*End of roadmap v3. Execute Phase 0 on approval.*
