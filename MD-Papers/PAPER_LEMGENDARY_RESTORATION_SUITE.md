<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: Advanced Film Restoration & Super-Resolution Master Suite

**Author**: Lem Treursic  
**Version**: 1.0.0 - Pre-Training & Deployment Specification (2026 Specialization)  
**Target Hardware**: NVIDIA GeForce GTX 1650 (4GB) / Apple Silicon (MPS) / Dual T4 Cloud Nodes

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Visual Taxonomy: Restoration Manifolds](#2-visual-taxonomy-restoration-manifolds)
* [3. Shared Foundations & Universal Acceleration](#3-shared-foundations--universal-acceleration)
* [4. Model Deep-Dives](#4-model-deep-dives)
  * [4.1 LemGendary Universal Film Restorer](#41-lemgendary-universal-film-restorer)
  * [4.2 LemGendary UltraZoom Master Model](#42-lemgendary-ultrazoom-master-model)
  * [4.3 LemGendary UPN v2 Parameter Predictor](#43-lemgendary-upn-v2-parameter-predictor)
  * [4.4 LemGendary Professional Multi-Task Restoration MoE](#44-lemgendary-professional-multi-task-restoration-moe)
* [5. Challenges & Resilience Architecture](#5-challenges--resilience-architecture)
* [6. Deployment Strategy](#6-deployment-strategy)
* [7. SOTA Architectural Performance Matrix](#7-sota-architectural-performance-matrix)
* [8. Conclusion](#8-conclusion)

---

## 1. Abstract

This specification establishes the architectural, mathematical, and algorithmic documentation for the LemGendary Advanced Restoration and Super-Resolution Master Suite (Category 14). Designed to address complex, non-linear physical degradations, this suite unites four complementary restoration architectures:

1. **Universal Film Restorer**: A residual dense autoencoder engineered to eliminate archival film damage, chemical dye fading, dust, and continuous scratches.
2. **UltraZoom Master Model**: A sub-pixel efficient super-resolution network (ESPCN backbone) restoring high-frequency edge gradients and micro-textures.
3. **UPN v2 Parameter Predictor**: A mobile-optimized parameter regressor predicting optimal physical degradation restoration parameters directly from degraded imagery.
4. **Professional Multi-Task Restoration MoE**: A shared-encoder mixture-of-experts (MoE) network executing joint deblurring, denoising, and color correction dynamically.

This document serves as the pre-training and operational framework across manifolds `LemGendizedFilmRestorerLarge`, `LemGendizedUltraZoomLarge`, `LemGendizedUpnV2Large`, and `LemGendizedProfessionalMultitaskRestorationLarge`.

---

## 2. Visual Taxonomy: Restoration Manifolds

Restoration tasks process specialized degradation domains:

* **Film Archive Degradation (`LemGendizedFilmRestorerLarge`)**: Synthetic and archival grain, dye fading, longitudinal scratches, and mold artifacts.
* **Super-Resolution Manifold (`LemGendizedUltraZoomLarge`)**: Low-resolution downsampled pairs ($4\times$ zoom) requiring sub-pixel frequency reconstruction.
* **Parameter Prediction Manifold (`LemGendizedUpnV2Large`)**: Multi-label continuous parameter targets $[\sigma_{\text{noise}}, \theta_{\text{blur}}, \gamma_{\text{color}}]$.
* **Unified Multi-Task Manifold (`LemGendizedProfessionalMultitaskRestorationLarge`)**: Compound degradations requiring selective expert routing.

---

## 3. Shared Foundations & Universal Acceleration

### 3.1 Mathematical Loss Supervision

Restoration fidelity optimizes a combined Charbonnier reconstruction and deep perceptual loss:

$$\mathcal{L}_{\text{total}} = \sqrt{\|I_{\text{restored}} - I_{\text{gt}}\|^2 + \epsilon^2} + \lambda_{\text{perceptual}} \|\phi(I_{\text{restored}}) - \phi(I_{\text{gt}})\|_2^2$$

### 3.2 Restoration Quality Score Formulation

$$\text{Quality Score} = \text{PSNR} + (\text{SSIM} \times 20) - (\text{LPIPS} \times 20)$$

---

## 4. Model Deep-Dives

### 4.1 LemGendary Universal Film Restorer

#### 4.1.1 Model Description & Usage

Deep Residual Dense Autoencoder designed for digital preservation of historical film stock, removing physical emulsion scratches and chemical decay.

#### 4.1.2 Model Info

* **Model Key**: `film_restorer`
* **Architecture**: UniversalFilmRestorer (Residual Dense Autoencoder)
* **Status**: Checkpoint Trained (`LemGendaryUniversalFilmRestorer.pt`)
* **Resolution Ladder**: `[256, 384, 512]`
* **Loss Function**: `l1_lpips`
* **Target PSNR**: $\ge 24.0\text{ dB}$, **SSIM**: $\ge 0.800$, **LPIPS**: $\le 0.250$

---

### 4.2 LemGendary UltraZoom Master Model

#### 4.2.1 Model Description & Usage

Sub-pixel convolutional super-resolution network restoring fine optical details across high-zoom crops.

#### 4.2.2 Model Info

* **Model Key**: `ultrazoom`
* **Architecture**: UltraZoomMaster (Sub-Pixel ESPCN Super-Resolution)
* **Status**: Checkpoint Trained (`LemGendaryUltraZoom(Master).pt`)
* **Resolution Ladder**: `[256, 384, 512]`
* **Target PSNR**: $\ge 34.0\text{ dB}$, **SSIM**: $\ge 0.950$, **LPIPS**: $\le 0.040$

---

### 4.3 LemGendary UPN v2 Parameter Predictor

#### 4.3.1 Model Description & Usage

Mobile-lite continuous parameter regressor inferring noise variance, blur angle, and exposure correction factors to guide adaptive filtering pipelines.

#### 4.3.2 Model Info

* **Model Key**: `upn_v2`
* **Architecture**: UPN_v2 (MobileNet-Lite Parameter Regressor)
* **Status**: Checkpoint Trained (`LemGendaryUPN(v2)Modular.pt`)
* **Resolution Ladder**: `[128, 192, 256]`
* **Loss Function**: `smooth_l1`
* **Target MAE**: $\le 0.050$

---

### 4.4 LemGendary Professional Multi-Task Restoration MoE

#### 4.4.1 Model Description & Usage

Shared-encoder multi-task model routing features to task-specific expert sub-networks (denoising, deblurring, dehazing, enhancement) based on input degradation signatures.

#### 4.4.2 Model Info

* **Model Key**: `professional_multitask_restoration`
* **Architecture**: MultiTaskRestorer (Shared Encoder Multi-Task MoE)
* **Status**: Training In-Progress / Pre-Training Architectural Specification
* **Target Manifold**: `LemGendizedProfessionalMultitaskRestorationLarge`
* **Resolution Ladder**: `[256, 384, 512]`
* **Loss Function**: `hybrid_restoration`
* **Target PSNR**: $\ge 32.0\text{ dB}$, **SSIM**: $\ge 0.930$, **LPIPS**: $\le 0.070$

#### 4.4.3 Spatial Ladder & Training Progression

The multi-task model progresses through dynamic spatial ladders:

$$\text{Phase 1: } 256\text{px} \longrightarrow \text{Phase 2: } 384\text{px} \longrightarrow \text{Phase 3: } 512\text{px}$$

As active training runs conclude on dual T4 nodes, checkpoint metrics will record into `metrics.csv`.

---

## 5. Challenges & Resilience Architecture

* **Multi-Task Task Interference**: Balanced gradient normalization prevents gradients from one degradation mode from dominating shared encoder parameters.
* **Sub-Pixel Artifact Prevention**: Periodic shuffle layers utilize blurred kernel initializations to eliminate checkerboard artifacts.

---

## 6. Deployment Strategy

Compiled via ONNX Runtime and TensorRT with dynamic batching. Export scripts target FP16 precision with verified numerical stability against gradient overflow.

---

## 7. SOTA Architectural Performance Matrix

| Model Key | Architecture | Target Manifold | Resolution Ladder | Target Metric | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `film_restorer` | Residual Dense Autoencoder | `LemGendizedFilmRestorerLarge` | [256, 384, 512] | PSNR 24.0 dB, SSIM 0.80 | Checkpoint Trained |
| `ultrazoom` | Sub-Pixel ESPCN | `LemGendizedUltraZoomLarge` | [256, 384, 512] | PSNR 34.0 dB, SSIM 0.95 | Checkpoint Trained |
| `upn_v2` | MobileNet-Lite Regressor | `LemGendizedUpnV2Large` | [128, 192, 256] | MAE 0.050 | Checkpoint Trained |
| `professional_multitask_restoration` | Shared Encoder MoE | `LemGendizedProfessionalMultitaskRestorationLarge` | [256, 384, 512] | PSNR 32.0 dB, SSIM 0.93 | In-Progress / Pre-Training |

---

## 8. Conclusion

The Advanced Restoration Suite delivers an industrial-grade framework for multi-modal image reconstruction. By pre-specifying architectural interfaces and target manifolds, ongoing training jobs integrate seamlessly into the production registry.
