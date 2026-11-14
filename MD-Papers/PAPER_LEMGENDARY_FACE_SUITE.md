# High-Fidelity Facial Restoration, Parsing & Detection Suite

## Category 08 FACE | Architecture of LemGendary AI

**Author**: Lem Treursic · **Version**: `v16.9.214-STABLE` · **Paper Revision**:
1.1.0 - Pre-Training & Deployment Specification (2026 Specialization) · **Target
Hardware**: NVIDIA GeForce GTX 1650 (4GB) / Apple Silicon (MPS) / Dual T4 Cloud
Nodes

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Visual Taxonomy: Facial Manifolds](#2-visual-taxonomy-facial-manifolds)
* [3. Shared Foundations & Universal
  Acceleration](#3-shared-foundations--universal-acceleration)
* [4. Model Deep-Dives](#4-model-deep-dives)
  * [4.1 LemGendary CodeFormer (Face
    Restoration)](#41-lemgendary-codeformer-face-restoration)
  * [4.2 LemGendary ParseNet (Face Parsing &
    Segmentation)](#42-lemgendary-parsenet-face-parsing--segmentation)
  * [4.3 LemGendary RetinaFace (Multi-Scale Face
    Detection)](#43-lemgendary-retinaface-multi-scale-face-detection)
* [5. Challenges & Resilience
  Architecture](#5-challenges--resilience-architecture)
* [6. Deployment Strategy & WebAssembly/ONNX
  Bridge](#6-deployment-strategy--webassemblyonnx-bridge)
* [7. SOTA Architectural Performance
  Matrix](#7-sota-architectural-performance-matrix)
* [8. Conclusion](#8-conclusion)

---

## 1. Abstract

This technical whitepaper details the architectural design, manifold
engineering, loss formulations, and deployment specifications for the LemGendary
Facial Vision Suite. As part of Category 08 within the LemGendary AI
Documentation Hub, this suite coordinates three specialized networks targeting
facial perception:

1. **LemGendary CodeFormer**: A transformer-based blind face restoration model
   employing a discrete vector-quantized (VQ) codebook prior to reconstruct
   high-fidelity facial features from heavily degraded, blurred, and
   low-resolution inputs.
2. **LemGendary ParseNet**: A bilateral face parsing semantic segmentation
   network segmenting 19 anatomical regions to provide dense spatial boundary
   guidance.
3. **LemGendary RetinaFace**: A single-box face localization and 5-point
   landmark regression model on a lightweight MobileNetV3-Small backbone (one
   box, one confidence and five landmarks per image; no anchors).

This specification documents the mathematical operators, target SOTA metrics,
memory-sentinel bounds, and training telemetry hooks for active and in-progress
training cycles across the compiled manifolds `LemGendizedCodeFormerLarge`,
`LemGendizedParseNet`, and `LemGendizedRetinaFace`.

---

## 2. Visual Taxonomy: Facial Manifolds

Facial restoration and analysis require processing distinct spatial degradation
distributions across human facial geometry:

* **Blind Degradation Manifold (`LemGendizedCodeFormerLarge`)**: High-entropy
  combinations of atmospheric blur, synthetic sensor noise, downsampling, and
  JPEG compression artifacts spanning diverse demographic identities and poses.
* **Anatomical Segmentation Manifold (`LemGendizedParseNetLarge`)**: Dense
  pixel-level annotations across 19 discrete facial classes (skin, eyebrows,
  eyes, nose, lips, mouth interior, teeth, hair, ears, accessories).
* **Face Localization Manifold (`LemGendizedRetinaFace`)**: 425,223 SFHQ
  photos (train 374,199 / val 51,024), one face per image with a tight
  WIDER-style box and 5-point keypoint coordinates (left eye, right eye, nose
  tip, left mouth corner, right mouth corner), rebuilt from the SFHQ 110-point
  landmarks (`landmark_source: sfhq-110pt`).

---

## 3. Shared Foundations & Universal Acceleration

All models in the Facial Suite adhere to the unified LemGendary hardware-aware
training loop.

### 3.1 VRAM Memory Bounds & Sentinel Protection

To execute training stably across constrained 4GB VRAM local devices and dual T4
cloud instances, memory scaling is strictly bounded:

$$
\text{Mem}_{\text{total}} = \mathcal{O}(N \cdot H \cdot W \cdot C) \quad
\text{vs} \quad \text{Mem}_{\text{peak}} = \mathcal{O}(b_{\text{chunk}} \cdot H
\cdot W \cdot C)
$$

The Headroom-Aware Memory-Sentinel dynamically throttles chunk size
$b_{\text{chunk}}$ when available device headroom falls below 512 MB, executing
emergency garbage collection before out-of-memory faults trigger.

### 3.2 Scalar Restoration Quality Score

Perceptual reconstruction quality across restoration phases is monitored via the
heuristic scalar quality function:

$$
\text{Quality Score} = \text{PSNR} + (\text{SSIM} \times 20) - (\text{LPIPS}
\times 20)
$$

*Metric Calibration Rationale:* PSNR (higher is better) typically spans
$20\text{--}35\text{ dB}$ in restoration tasks. SSIM (higher is better) and
LPIPS (lower is better, measuring deep perceptual distance) are normalized
indices bounded in $[0, 1]$. To prevent unit-scale distortion where a $0.05$
perceptual shift would be dwarfed by a $1.0\text{ dB}$ PSNR variation, a scaling
factor of $20\times$ maps both SSIM and LPIPS to equivalent dynamic magnitudes
($\Delta = 1.0\text{ unit}$ per $0.05$ metric change), while the negative sign
for LPIPS enforces consistent positive directionality for automated checkpoint
selection.

---

## 4. Model Deep-Dives

### 4.1 LemGendary CodeFormer (Face Restoration)

#### 4.1.1 Model Description & Usage

LemGendary CodeFormer reconstructs blind degraded facial images by mapping
degraded visual features into the discrete space of a learned facial codebook
prior $\mathcal{C} = \{\mathbf{c}_k\}_{k=1}^K \subset \mathbb{R}^d$.

#### 4.1.2 Model Info

* **Model Key**: `codeformer`
* **Architecture**: CodeFormer (Transformer-Based VQ Codebook Lookup)
* **Status**: Checkpoint Trained (`LemGendaryCodeFormer-FaceRestoration.pt`)
* **Input Resolution**: 512x512
* **Target Accelerator**: Dual T4 / Local CUDA

#### 4.1.3 Manifold Info

* **Target Manifold**: `LemGendizedCodeFormerLarge`
* **Sample Count**: 40,000 high-resolution facial pairs
* **Storage Format**: Chunked WebP Container

#### 4.1.4 Performance Metrics & SOTA Targets

* **Target PSNR**: $\ge 30.50\text{ dB}$
* **Target SSIM**: $\ge 0.930$
* **Target LPIPS**: $\le 0.080$
* **Target FID**: $\le 5.20$

#### 4.1.5 Mathematical Loss Formulation

$$
\mathcal{L}_{\text{CodeFormer}} = \mathcal{L}_{\text{rec}} +
\lambda_{\text{adv}} \mathcal{L}_{\text{adv}} + \lambda_{\text{feat}}
\mathcal{L}_{\text{feat}} + \lambda_{\text{code}} \|\text{sg}[E(\mathbf{x})] -
\mathbf{z}_q\|_2^2
$$

#### 4.1.6 Training Process Analysis

The model utilizes fixed 512px spatial dimension training with full transformer
cross-attention between degraded encoder tokens and discrete codebook
representations.

---

### 4.2 LemGendary ParseNet (Face Parsing & Segmentation)

#### 4.2.1 Model Description & Usage

ParseNet provides dense 19-class anatomical face segmentation, serving as an
upstream geometric prior for conditional editing and localized facial
restoration.

#### 4.2.2 Model Info

* **Model Key**: `parsenet`
* **Architecture**: ParseNet Bilateral Segmentation Network
* **Status**: Training In-Progress / Pre-Training Architectural Specification
* **Loss Function**: Weighted Categorical Cross-Entropy with Lovasz-Softmax
* **Learning Rate**: $5 \times 10^{-5}$
* **Input Resolution**: 512x512

#### 4.2.3 Manifold Info

* **Target Manifold**: `LemGendizedParseNetLarge`
* **Class Count**: 19 semantic anatomical classes
* **Storage Format**: Multi-Modal WebDataset Shards

#### 4.2.4 Performance Metrics & SOTA Targets

* **Target mIoU**: $\ge 0.860$
* **Target Pixel Accuracy**: $\ge 0.965$
* **Target Boundary F1**: $\ge 0.820$

#### 4.2.5 Mathematical Loss Formulation

$$
\mathcal{L}_{\text{ParseNet}} = \mathcal{L}_{\text{CE}}(\mathbf{p}, \mathbf{y})
+ \lambda_{\text{lovasz}} \mathcal{L}_{\text{Lovasz}}(\mathbf{p}, \mathbf{y}) +
\lambda_{\text{edge}} \mathcal{L}_{\text{Boundary}}(\nabla \mathbf{p}, \nabla
\mathbf{y})
$$

#### 4.2.6 Training Process Analysis & Spatial Ladder

Training follows a staged resolution schedule
($256\text{px} \to 384\text{px} \to 512\text{px}$) to stabilize semantic
boundary convergence. Checkpoint telemetry updates dynamically into
`metrics.csv`.

---

### 4.3 LemGendary RetinaFace (Multi-Scale Face Detection)

#### 4.3.1 Model Description & Usage

RetinaFace provides real-time facial bounding box localization and 5-point
landmark regression, serving as the automated face cropping and alignment
frontend across the ecosystem. The suite's model (`RetinaFaceMobileNet`) has
no prior boxes: one globally pooled head regresses a single normalized
`cx cy w h` box, one confidence and five landmarks per image.

#### 4.3.2 Model Info

* **Model Key**: `retinaface`
* **Architecture**: MobileNetV3-Small Backbone
* **Status**: Pre-Training Architectural Specification
* **Loss Function**: Multi-Task Bounding Box, Keypoint & Classification Loss
* **Learning Rate**: $5 \times 10^{-4}$
* **Input Resolution**: 640x640

#### 4.3.3 Manifold Info

* **Target Manifold**: `LemGendizedRetinaFace` (425,223 samples: train
  374,199 / val 51,024; val drawn by SFHQ file id, the same split as
  `LemGendizedParseNet`)
* **Annotation Modality**: JSON label (`face_landmarks`) with one object per
  face: normalized box $[c_x, c_y, w, h]$ + 5 keypoints
  $[(x_i, y_i)]_{i=1}^5$

#### 4.3.4 Performance Metrics & SOTA Targets

The training suite (v16.9.208) measures the single-box output per image; all
four targets are provisional (`sota_targets_provisional: true`): no cited
source backs them yet, and WIDER FACE easy / medium / hard AP does not apply
to a one-box-per-image model.

* **Box IoU (`box_iou`)**: mean IoU of the predicted and the labelled box over
  the images that hold a face. Target $\ge 0.80$.
* **AP50 (`ap50`)**: single-class AP over images (each image is one
  detection ranked by its confidence; a true positive holds a face and
  reaches IoU 0.5), all-point interpolated. Target $\ge 0.95$.
* **AP50-95 (`ap50_95`)**: the same AP averaged over the COCO thresholds
  0.50:0.05:0.95. Target $\ge 0.60$.
* **Landmark NME (`landmark_nme`)**: mean distance of the five points divided
  by the inter-ocular distance (points 0 and 1); lower is better. Target
  $\le 0.10$.

RetinaFace metrics recorded before v16.9.207 / v16.9.208 are not comparable
with new runs: the old `map_*` values were fixed multiples of a
twice-squashed confidence score, and the label rebuild made the boxes tight
(about 0.31 to 0.57 of the old box area).

#### 4.3.5 Mathematical Loss Formulation

$$
\mathcal{L}_{\text{RetinaFace}} = \mathcal{L}_{\text{cls}}(p_i, p_i^*) +
\lambda_1 p_i^* \mathcal{L}_{\text{box}}(t_i, t_i^*) + \lambda_2 p_i^*
\mathcal{L}_{\text{pts}}(l_i, l_i^*)
$$

where $\mathcal{L}_{\text{box}}$ denotes Smooth-L1 regression and
$\mathcal{L}_{\text{pts}}$ enforces keypoint localization.

---

## 5. Challenges & Resilience Architecture

1. **Extreme Pose & Occlusion Resilience**: Enforces random face erasing and
   horizontal flipping to prevent orientation overfitting.
2. **Quantization Stability**: Codebook commitment losses use straight-through
   gradient estimators to eliminate numerical gradient stagnation.
3. **Multi-Scale Anchor Density**: Anchor grids scale down to $4 \times 4$
   pixels to detect micro-faces under dense crowd scenes.

---

## 6. Deployment Strategy & WebAssembly/ONNX Bridge

The Facial Vision Suite compiles into quantized ONNX (Opset 18) and WebGPU/WASM
artifacts for real-time edge processing in the LemGendary AI Studio GUI. Memory
allocations are locked at $< 350\text{ MB}$ total runtime footprint.

---

## 7. SOTA Architectural Performance Matrix

* **`codeformer`**: Architecture: Transformer VQ-Codebook; Target Manifold:
  `LemGendizedCodeFormerLarge`; Input Res: 512x512; Primary Metric Target: PSNR
  30.5 dB, FID 5.2; Current Status: Checkpoint Trained
* **`parsenet`**: Architecture: Bilateral Segmentation; Target Manifold:
  `LemGendizedParseNetLarge`; Input Res: 512x512; Primary Metric Target: mIoU
  0.860; Current Status: In-Progress / Pre-Training
* **`retinaface`**: Architecture: MobileNetV3-Small Backbone (single-box
  head); Target Manifold: `LemGendizedRetinaFace`; Input Res: 640x640;
  Primary Metric Target: AP50 0.95 (provisional; also Box IoU 0.80, AP50-95
  0.60, Landmark NME 0.10); Current Status: Pre-Training Spec

---

## 8. Conclusion

The LemGendary Facial Vision Suite establishes a unified perception pipeline
spanning face detection, landmark alignment, anatomical semantic parsing, and
high-fidelity codebook restoration. Prepared structures ensure that as active
training iterations converge, metrics and physical weights synchronize
seamlessly into the documentation hub.
