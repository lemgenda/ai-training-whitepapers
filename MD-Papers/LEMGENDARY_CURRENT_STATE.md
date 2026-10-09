# LemGendary Ecosystem: Current State & Architectural Manifest

## Category 00 STATUS | Authoritative Workspace State Manifest

**Timestamp**: 2026-10-08  
**Master Architectural Baseline**: `v16.9.16-STABLE`  
**Parent Authority**: [Master Ecosystem Architecture](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/ECOSYSTEM_ARCHITECTURE.md) · [Document Authority Hierarchy & Versioning Policy](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/VERSIONING_POLICY.md)

---

## Table of Contents

- [1. Executive Summary & Current Operational State](#1-executive-summary--current-operational-state)
- [2. Multi-Track Versioning Matrix](#2-multi-track-versioning-matrix)
- [3. Document Authority Hierarchy](#3-document-authority-hierarchy)
- [4. Tripartite Microservice Topology & Port Bindings](#4-tripartite-microservice-topology--port-bindings)
- [5. Registered Model Architectures & Convergence Status](#5-registered-model-architectures--convergence-status)
- [6. Manifold Ingestion & Container Modernization](#6-manifold-ingestion--container-modernization)
- [7. Cloud Training & Remote Synchronization Pipeline](#7-cloud-training--remote-synchronization-pipeline)
- [8. Hardware Sentinels & Physical Execution Constraints](#8-hardware-sentinels--physical-execution-constraints)
- [9. Zero-Suppression Policy Compliance](#9-zero-suppression-policy-compliance)

---

## 1. Executive Summary & Current Operational State

The **LemGendary AI Ecosystem** is an end-to-end, hardware-aware distributed deep learning platform designed for vision restoration, perceptual quality assessment, object detection, and high-frequency multi-timeframe quantitative finance.

The ecosystem has achieved full **Post-Modernization S.O.L.I.D. Architectural Maturity** across all subsystems:

- **Zero-Suppression**: 100% zero-suppression code hygiene (`0` `# type: ignore`, `0` `# noqa`, `0` `# pylint: disable`).
- **Tripartite Services**: Completely decoupled sidecar daemons running over HTTP REST and live WebSocket channels (Ports 8000, 8100, 8200).
- **Presentation Layer**: Native cross-platform desktop cockpit built with Tauri v2, React 18, and Vite (`v2.0.0`).
- **Nuclear Stability**: Automated Sawtooth VRAM Governor, continuous first-principles memory batch sizing, non-blocking sub-second minibatch cancellation, and multi-rung checkpoint resumption across 22 production neural architectures.
- **Bi-Directional Cloud Sync**: Real-time Kaggle and Google Drive synchronization with automatic 403 Forbidden prevention (auto-creation of repository placeholders before metadata updates).

---

## 2. Multi-Track Versioning Matrix

The ecosystem operates on intentional, well-defined versioning tracks:

| Subsystem / Track | Scope / Domain | Active Version | Primary Interface / Entrypoint |
| :--- | :--- | :--- | :--- |
| **Master Training Suite** | PyTorch training loops, Sawtooth Governor, SOTA ladders | `v16.9.16-STABLE` | `python -m training.cli.lemtrain` |
| **Dataset Compiler** | Shard synthesis, WebP transcoding, Kaggle/HF ingestion | `v16.9.6` | `python cli.py` / `lemgendary_datasets_hub.ps1` |
| **Environment Manager** | Hardware probe, virtual environments, compliance audits | `v16.9.3` | `lem-env` / `lemgendary_env_manager.ps1` |
| **AI Studio Desktop GUI** | Tauri v2 desktop application & Operator Cockpit | `v2.0.0` (Client) | `lemgendary-ai-studio-gui` executable |
| **Documentation Hub** | Master architectural whitepapers, manuals, HTML papers | `v16.9.16-STABLE` | `lemgendary-docs/papers/index.html` |
| **Production Models** | Authoritative model weights, ONNX exports, metrics | `v16.9.16-STABLE` | `LemGendaryModels/<model_key>/` |
| **Clinical Diagnostic Specs** | Training pathology & medical failure mode taxonomies | `v1.4.0` | `PAPER_TRAINING_PATHOLOGY.md` |
| **Quantitative Algorithmic Specs** | Multi-Scale CNN-Transformer Forex & Commodities | `v2.7.1` | `PAPER_FOREX_PREDICTOR.md` |

---

## 3. Document Authority Hierarchy

To guarantee consistency across documentation and codebase implementations, all documentation strictly adheres to the four-tier authority hierarchy:

$$\text{Code Manifests (SSOT)} \succ \text{Master Manuals} \succ \text{Architectural Whitepapers} \succ \text{Educational Guides}$$

1. **Level 1 — Single Source of Truth Configuration Manifests**:
   - `unified_models_v2.yaml`, `unified_data.yaml`, `presets.yaml`, `openapi.json`.
   - Highest physical authority for parameters, architecture baselines, and data bindings.
2. **Level 2 — Master Operational & Technical Manuals**:
   - `MANUAL_AI_STUDIO_GUI.md`, `MANUAL_CLI.md`, `MANUAL_API.md`, `GUI_CONTROL_REGISTRY.md`.
   - Authoritative for operational workflows, control IDs, CLI flags, and API payloads.
3. **Level 3 — Architectural & Technical Whitepapers**:
   - `ECOSYSTEM_ARCHITECTURE.md`, `PAPER_TRAINING_SUITE.md`, `PAPER_DATASET_COMPILER.md`, `PAPER_AI_STUDIO_GUI.md`, `PAPER_DEGRADATION_ENGINE.md`, `PAPER_TRAINING_PATHOLOGY.md`, and the 22 model deep-dive whitepapers.
   - Authoritative for physical optical formulations, asymptotic runtime complexity, memory sentinels, and scientific citations. Whitepapers remain project-specific technical specifications and do not duplicate generic introductory textbooks.
4. **Level 4 — Educational & Ecosystem Guides**:
   - `GENERAL_AI_TRAINING_KNOWLEDGE.md`, `GLOSSARY.md`, `LEMGENDARY_CURRENT_STATE.md`.
   - Comprehensive reference manuals for engineering principles and universal deep learning theory.

---

## 4. Tripartite Microservice Topology & Port Bindings

The local orchestration layer operates across three background sidecar services:

| Sidecar Service | Port | Protocol | Responsibilities |
| :--- | :--- | :--- | :--- |
| **Environment Manager** | `8000` | HTTP / WebSocket | Hardware sensing, venv provisioning, package drift analytics, compliance gating. |
| **Dataset Compiler** | `8100` | HTTP / WebSocket | Manifold sharding, WebP conversion, Kaggle sync hub, custom compilation. |
| **Training Suite** | `8200` | HTTP / WebSocket | Training job submission, live loss streaming, GPU device allocation, SOTA audits. |

---

## 5. Registered Model Architectures & Convergence Status

The suite governs **22 production neural network architectures** tracked in `unified_models_v2.yaml` and documented in `LemGendaryModels/<model_key>/README.md`:

1. **Blind Face Restoration**: `codeformer` (Vector-Quantized Codebook Lookup)
2. **Atmospheric Dehazing**: `ffanet_indoor`, `ffanet_outdoor` (Feature Fusion Attention)
3. **Frame Interpolation**: `film_restorer` (Feature-Interpolated Motion Restorer)
4. **Quantitative Finance**: `forex_predictor` (Multi-Timeframe Causal CNN-Transformer)
5. **Exposure & Lighting Correction**: `mirnet_exposure`, `mirnet_lowlight` (Multi-Scale Residual Network)
6. **Precipitation Restoration**: `mprnet_deraining` (Cross-Stage Feature Fusion)
7. **High-Fidelity Restoration**: `nafnet_debluring`, `nafnet_denoising` (SimpleGate Nonlinearity-Free)
8. **Perceptual Quality Scoring**:
   - `nima_aesthetic_mobile` (MobileNetV2 EMD Scorer)
   - `nima_aesthetic_efficientnet` (EfficientNetV2-S Scorer)
   - `nima_aesthetic_pro` (Swin-v2-T Multiscale Scorer)
   - `nima_authenticity` (AI vs Human Generative Classifier)
   - `nima_technical` (Micro-Defect ISO Scorer)
9. **Face Parsing & Landmarks**: `parsenet`, `retinaface`
10. **Universal Restoration Engine**: `professional_multitask_restoration` (11-Head MoE Router)
11. **Super-Resolution**: `ultrazoom` (Sub-Pixel ESPCN / Residual SR)
12. **Content Moderation**: `universal_nsfw_classification` (GeM Pooling Safety Filter)
13. **Parameter Steering**: `upn_v2` (Continuous Parameter Predictor)
14. **Object Detection**: `yolov8n` (Anchor-Free CSPDarknet + PANet Curriculum Governor)

Every model enforces the authoritative **3-Pillar Fully-Trained Verification Invariant**:
$$\text{Status} = \text{FULLY\_TRAINED} \iff \left(\bigwedge_{m} \text{Passed}(m, T_m)\right) \land \text{LadderPassed} \land (\text{DataFraction} \ge 1.0)$$

---

## 6. Manifold Ingestion & Container Modernization

- **Storage Location**: `LemGendaryDatasets/` (suffix-free directory topology).
- **Container Formats**: WebDataset (`.tar`), MosaicML (`.mds`), Lightning AI LitData (`.bin`), Apache Parquet (`.parquet`), Directory (`.webp`).
- **Transcoding Standard**: In-flight 12-thread WebP zero-intermediate compression:
  - Input/Degraded: WebP Lossy ($q=92$).
  - Ground Truth Target: WebP High-Fidelity ($q=95$).
  - Alpha / Segmentation Masks: WebP Lossless.

---

## 7. Cloud Training & Remote Synchronization Pipeline

- **Kaggle Pipelines (`kaggle_training/`)**: 22 standalone notebooks consuming attached input datasets directly from `/kaggle/input/` with zero redundant cloud downloads.
- **Google Colab Pipelines (`colab_training/`)**: 22 automated training pipelines synchronized idempotently to Google Drive via `push_to_drive.py`.
- **Bidirectional Metadata Sync**:
  - `push_kaggle_dataset_metadata` automatically verifies remote repository existence via `ensure_kaggle_dataset_exists`.
  - If a target dataset slug does not exist on Kaggle, the synchronizer auto-creates a minimal public placeholder dataset containing `README.md` first, permanently eliminating `403 Forbidden` errors during metadata updates.
  - Interactive options in PowerShell (`lemgendary_datasets_hub.ps1` options `3` and `A`) and Desktop GUI (`CompilerPanel.tsx` "Update Metadata Only" tab) enable single and batch metadata updates without re-uploading multi-gigabyte data archives.

---

## 8. Hardware Sentinels & Physical Execution Constraints

- **GTX 1650 (4GB VRAM) Edge Baseline**: Sub-nuclear 4GB lockdown enforces Serial-Only Mode upon memory saturation, eliminating Windows System RAM pagefile thrashing ($12.5\times$ batch retrieval speedup).
- **Continuous Memory Formula**: Dynamic batch calculation scales continuously with available VRAM:
  $$B_{\text{safe}} = \left\lfloor \frac{\text{VRAM}_{\text{total}} \cdot \text{safety} - \text{static\_overhead}}{\text{mem\_per\_sample}(\text{resolution})} \right\rfloor$$
- **Sawtooth VRAM Governor**: Dynamically halves batch sizes when memory pressure exceeds 90% and scales up when headroom exceeds 40%.
- **Sub-Second Minibatch Cancellation**: Evaluates non-blocking cancellation listeners at batch boundaries, instantly interrupting runaway runs.

---

## 9. Zero-Suppression Policy Compliance

The codebase strictly adheres to 100% zero-suppression error telemetry:

- `0` instances of `# type: ignore`
- `0` instances of `# noqa`
- `0` instances of `# pylint: disable`
- Zero programmatic `warnings.filterwarnings` suppressions.

All warnings and type checks are resolved through rigorous static type annotations, Pydantic schema validation, and defensive programming.
