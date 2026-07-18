# Master Training Suite Guide: LemGendary AI

## Category 02 | LemGendary AI Documentation Hub

---

## 1. Executive Summary

The LemGendary AI Training Suite is an industrial-grade orchestration layer for training, optimizing, and deploying SOTA vision and multimodal models. Optimized for high-frequency artifact detection and structural restoration, the v16.2.9 "Nuclear-Hardened" Architecture represents the global standard for high-fidelity model training.

---

## 2. High-Fidelity "Nuclear" Hardening

The suite enforces a strict high-fidelity baseline to ensure models learn complex textures and micro-artifacts from the very first epoch.

### 2.1. Dynamic Memory-Sentinel (Batch Decoupling)

- **Absolute Sentinel Authority**: Acts as the absolute physical authority. It treats `batch_size` from config as a maximum boundary and autonomously throttles it downwards if the local physical VRAM cannot hold it, permanently preventing system RAM paging.
- **Atomic Re-Audit**: Performs a fresh hardware probe every time the resolution ladder jumps, ensuring peak physical throughput at low resolutions while automatically throttling for high-res stability.
- **Sub-Nuclear 4GB Lockdown**: On GTX 1650/4GB cards, it enforces a strict **Serial-Only Mode** after an OOM, delivering a **2x performance gain** by preventing Windows System RAM paging.
- **Hardware-Aware Resolution Capping**: Dynamically limits maximum training and validation resolution (e.g. `max_allowed_local_resolution: 640`) on local environments to prevent 4GB VRAM exhaustion, while permitting 1024px+ scaling on robust cloud infrastructures.
- **Multi-GPU DataParallel Engine**: Automatically detects multiple CUDA devices and wraps the active manifold in PyTorch's `DataParallel` engine. It dynamically scales the batch size perfectly across the available physical hardware (e.g. Kaggle T4x2) while keeping learning rates synchronized.
- **Dynamic Validation Sharding & Auto-Expansion**: Subsets the validation dataloader to 30% per epoch to accelerate perceptual metric computation. Once the model hits the Refinement Phase, or the dynamically configurable `high_fidelity_fraction` (default 70%) at maximum resolution, it dynamically auto-expands validation to **100% (full dataset)** to guarantee an absolute SOTA generalizability audit.

### 2.2. Intelligent Curriculum & Sawtooth Governance

- **Universal Quality Scorecarding**: The trainer dynamically compounds PSNR, SSIM, LPIPS, and FID for all restoration models, mathematically verifying ultimate convergence against academic SOTA benchmarks.
- **Continuous Parameter Predictor Calibration**: Standardized validation MAE telemetry for continuous parameter predictors (like `upn_v2`), recording MAE directly into `metrics.csv`.
- **Professional Multi-Task Restoration**: Fully integrated multi-headed Mixture-of-Experts (MoE) routing engine with 11 specialized restoration heads dynamically trained under Dynamic Filename Task Ingestion.

### 2.3. Hardened Resolution Ladders & SOTA Guards

- **Ladder-Aware Progression**: Reaching SOTA targets at sub-maximal resolutions triggers a **Forced Spatial Jump** to the next rung (e.g., 256px → 384px).
- **SOTA Hardening Guard**: Enforces a mandatory **2-epoch "Hardening Period"** for every resolution rung to solidify weights.
- **Overfitting Rescue Protocol**: Overrides tactical recoils and cooldown locks when trend-based overfitting is diagnosed, force-expanding the dataset fraction (+15% data) to break the overfitting attractor.
- **SOTA Verification**: Verifies SOTA targets on 100% of training data at final resolution before permitting export.

### 2.4. Checkpoint Resumption & Singularity Hardening

- **The Scheduler Shield**: Dynamically inspects candidate checkpoints for poisoned/advanced step counts. If detected, it overrides and re-anchors the loaded scheduler steps back to actual epoch progress.
- **Velocity Bomb Prevention (Rollback Isolation)**: During a SOTA Rollback, the Governor surgically decouples the model weights from the learning rate chronometer. It reverts the weights to the safe baseline but intentionally bypasses chronological scheduler rewinding. This prevents the learning rate from violently spiking back to early-stage `max_lr` values, ensuring the model gently seats into a cold, stable manifold.
- **Metric Singularity & Live Polarity Shield**: The Metric Singularity Shield triggers a tactical recoil and rollback to SOTA weights immediately if PLCC/SRCC hit NaN. **New in v1.2.2**: The Live Polarity Shield monitors the manifold directly during training; if `SRCC < 0.0` or `PLCC < 0.0` is detected mid-epoch, it immediately flags a "Polarity Collapse", rejecting the epoch and triggering an instant SOTA rollback to purge inverted weights.
- **Absolute Anti-Loop Guard (Dead Man's Switch)**: To prevent models from manipulating localized 5% drift gates via marginal "lucky" spikes, the Governor tracks an `absolute_patience` limit (default 15 epochs). If a model fails to beat the Absolute SOTA for 15 epochs, the Governor forcefully severs the training loop and executes a hard SOTA rollback.
- **ONNX Trace Resilience (FakeTensor Guards)**: Dynamically wraps unmapped `FakeTensor` memory pointer access (`data_ptr()`) during FX/ONNX graph tracing within the DataParallel multi-GPU engine to prevent false-positive segmentation faults during structural graph export.

### 2.5. Mixture-of-Experts (MoE) 11-Manifold Architecture

- **Double-Softmax Squeeze Protection**: The `TaskClassifier` routing network natively isolates softmax activation from the loss engine, returning raw logits to prevent `log_softmax` gradient flattening when calculating Cross-Entropy gating loss.
- **Dynamic Perceptual LPIPS Balancing**: Automatically intercepts batch task indices during joint training to apply dynamic, sample-specific LPIPS multipliers scaling from `0.005` (Face Parsing) to `0.050` (Vintage & Face Restoration). This permanently prevents aggressive structural tasks from mathematically overpowering subtle intensity-based manifolds (like Lowlight/Exposure) via head competition.
- **Dynamic Regex Ingestion**: Seamlessly routes tasks like Denoise, Deblur, Derain, Dehaze, SuperRes, and Vintage automatically through regex extraction of physical dataset filenames on the fly.

---

## 3. Judicial Audit Engine

A fully decoupled, zero-dependency validation wrapper designed for CI/CD integration and isolated model auditing natively via `judicial_audit_api.py`.

### 3.1. Framework Agnosticism & Type Guards

Loads raw PyTorch `.pth` dictionaries, full PyTorch exported objects, and ONNX compiled graphs dynamically. It injects a dynamic class resolution pass to unpack `SoftmaxWrapper` boundaries, a critical guardrail accommodating PyTorch 2.6+ `weights_only=False` unpickling shifts.

To prevent standard tensor mis-casting during ONNX graph evaluation, the auditor dynamically intercepts the `Float16` schema directly from the ONNX inputs, safely casting down Float32 PyTorch tensors.

### 3.2. Fast-Path Correlator

Bypasses complex multi-process training augmenters for single-threaded PIL loads (eliminating Windows DataLoader worker-hangs), outputting standard **PLCC** (Pearson) and **SRCC** (Spearman) scores natively, and automatically piping results into a standard JSON schema for automated regression auditing.

---

## 4. Universal Models Registry & SOTA Baselines

Below is the exhaustive matrix of supported architectures natively integrated within the suite, dynamically driven by the `unified_models_v2.yaml` engine.

| Model Name | Architecture / Backbone | LemGendized Dataset | SOTA Targets |
| --- | --- | --- | --- |
| LemGendary NIMA Aesthetic Scorer (Mobile) | MobileNetV2 (Global Composition) | LemGendizedNimaAesthetic | PLCC: 0.60 \| SRCC: 0.60 |
| LemGendary NIMA Aesthetic Scorer (EfficientNetV2-S) | EfficientNetV2-S (Global Composition) | LemGendizedNimaAesthetic | PLCC: 0.7 \| SRCC: 0.7 |
| LemGendary NIMA Aesthetic Scorer (Pro ViT) | Swin-v2-T (Global Multi-Scale Attention) | LemGendizedNimaAesthetic | PLCC: 0.75 \| SRCC: 0.75 |
| LemGendary NIMA Technical Scorer | EfficientNetV2-S (Spatial Integrity) | LemGendizedNimaTechnical | PLCC: 0.88 \| SRCC: 0.88 |
| LemGendary Authenticity Scorer (AI vs Human) | EfficientNetV2-S (Distribution Scorer) | LemGendizedNimaAuthenticity | N/A |
| LemGendary UPN v2 Parameter Predictor | N/A | LemGendizedUpnV2 | MAE: 0.05 |
| LemGendary Universal Film Restorer | N/A | LemGendizedFilmRestorer | PSNR: 24.0 \| SSIM: 0.8 |
| LemGendary CodeFormer Face Restoration | N/A | LemGendizedCodeFormer | PSNR: 33.0 \| SSIM: 0.92 |
| LemGendary ParseNet Face Parsing | N/A | LemGendizedParseNet | N/A |
| LemGendary RetinaFace MobileNet Detection | N/A | LemGendizedRetinaFaceMobileNet | N/A |
| LemGendary RetinaFace ResNet Detection | N/A | LemGendizedRetinaFaceResNet | N/A |
| LemGendary FFANet Dehazing (Indoor) | N/A | LemGendizedFfaNetIndoor | PSNR: 36.39 \| SSIM: 0.988 |
| LemGendary FFANet Dehazing (Outdoor) | N/A | LemGendizedFfaNetOutdoor | PSNR: 33.57 \| SSIM: 0.984 |
| LemGendary MIRNet v2 Low-Light Enhancement | N/A | LemGendizedMirNetLowLight | PSNR: 24.14 \| SSIM: 0.83 |
| LemGendary MIRNet v2 Exposure Correction | N/A | LemGendizedMirNetExposure | PSNR: 24.14 \| SSIM: 0.83 |
| LemGendary MPRNet Deraining | N/A | LemGendizedMprNetDeraining | PSNR: 36.4 \| SSIM: 0.98 |
| LemGendary NAFNet Debluring | N/A | LemGendizedNafNetDebluring | PSNR: 37.0 \| SSIM: 0.975 |
| LemGendary NAFNet Denoising | N/A | LemGendizedNafNetDenoising | PSNR: 42.0 \| SSIM: 0.992 |
| LemGendary YOLOv8n Multi-Task Model | N/A | LemGendizedYoloV8n | N/A |
| LemGendary Professional Multi-Task Restoration Model | N/A | LemGendizedProfessionalMultitaskRestoration | PSNR: 32.0 \| SSIM: 0.93 |
| LemGendary UltraZoom Master Model | N/A | LemGendizedUltraZoom | PSNR: 34.0 \| SSIM: 0.95 |
| LemGendary SDXL Master Diffusion | N/A | diffusion_master_manifold | N/A |
| LemGendary FLUX.1 Master Diffusion | N/A | diffusion_master_manifold | N/A |
| LemGendary LLaVA v1.5 Master VLM | N/A | vision_language_master_manifold | N/A |
| LemGendary BLIP-2 Master VLM | N/A | vision_language_master_manifold | N/A |
| LemGendary Universal NSFW Classifier | MobileNetV2 (Categorical Anchor) | classification_master_manifold | N/A |

---

## 5. Universal SOTA Telemetry & Cloud Sync

Standardized historical audit (`metrics.csv`) captures the complete state including Epoch, Loss, LR, Accuracy, Res, Data, Temp, Clamp, Batch, Accumulation, and Stress. The **Metrics Sanitizer** explicitly sanitizes `inf`/`NaN` artifacts to prevent numerical poison.

The Governor automatically synchronizes with the `LemGendaryModels` repository, saving `_latest.pth` and `_best.pth` directly to the Hub. It uses Dual-Token PATs (`SUITE_PAT` and `GITHUB_PAT`) for secure, headless authentication on Kaggle deployment matrices.

### 5.1. Multi-GPU DataParallel Capabilities (Kaggle Scale)

The training suite natively intercepts execution environments with multiple GPUs (e.g., Kaggle Tesla T4 x2) and automatically wraps compatible models in PyTorch's `nn.DataParallel` API.

- **Dynamic Batch Distribution**: Seamlessly splits large high-fidelity pixel matrices (e.g., `768px`) across available GPUs, doubling effective throughput.
- **Seamless CPU Checkpointing**: Intelligently intercepts the `.pth` save hooks, stripping the `module.` prefix injected by `DataParallel` before saving to disk. This guarantees that Kaggle Multi-GPU checkpoints can be effortlessly downloaded and evaluated natively on standalone Windows environments or CPU deployments without manual layer re-mapping.

### 5.2. Universal Hardware Inference

All inference notebooks and training engines natively fall back to **DirectML** on local machines, providing zero-config GPU acceleration for AMD and Intel graphics cards on Windows.

---

## 6. Distributed Edge Training: LemGendary Cloud Link

The suite integrates a multi-node, collision-resistant **LemGendary Cloud Link** designed to crowdsource training loops across decentralized consumer-grade GPU networks.

### 6.1. Federated Gradient Accumulation (Average-Sync)

- **WAN Payload Bypass**: Instead of syncing multi-gigabyte weight tensors across the network, the `CloudSyncManager` pushes lightweight, compressed gradient chunks to a centralized WebSockets Coordinator Hub (port 8765).
- **Consensus Broadcasting**: The coordinator tracks epoch syncs, learning rate recoils, and node parameters. Once a quorum is met, the hub broadcasts a unified federated average-sync gradient vector to all active edge nodes.

### 6.2. Memory-Sentinel WebGPU Zero-Copy Export

- **Opset 17 Hardening**: The exporter is rigidly configured to ONNX `opset_version=17` and dynamic axes are intentionally stripped (locked to a `512x512` spatial tile). This permanently prevents standard WebGPU "Slice" operator crashes during browser inference.
- **Crowdsourced Browser Nodes**: SOTA manifolds exported via this pipeline enable crowdsourced, zero-copy training and inference directly within any user's mobile or desktop NPU-enabled web browser.
