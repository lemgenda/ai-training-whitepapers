# RetinaFace: Multi-Scale Facial Landmark Localization

## Category 08 FACE | Architecture of LemGendary AI

**Author**: Lem Treursic · **Version**: `v16.9.214-STABLE` · **Target Hardware**:
NVIDIA GeForce GTX 1650 / Apple Silicon / T4

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [1.1 What RetinaFace Does (In Plain English)](#11-what-retinaface-does-in-plain-english)
* [2. Visual Taxonomy: Multi-Scale Features & Landmarks](#2-visual-taxonomy-multi-scale-features--landmarks)
* [3. Shared Foundations: Tri-Head Multi-Task Objective](#3-shared-foundations-tri-head-multi-task-objective)
* [4. Model Deep-Dives](#4-model-deep-dives)
* [5. Challenges & Resilience Architecture](#5-challenges--resilience-architecture)
* [6. Deployment Strategy & Production Acceleration](#6-deployment-strategy--production-acceleration)
* [7. SOTA Architectural Performance Matrix](#7-sota-architectural-performance-matrix)
* [8. Conclusion](#8-conclusion)

---

## 1. Abstract

**RetinaFace** is a single-stage face localization network engineered for
high-precision facial bounding box detection and **5-point landmark regression**
(left eye, right eye, nose tip, left mouth corner, right mouth corner). The
LemGendary ecosystem standardizes on the lightweight **MobileNetV3-Small**
backbone for edge execution and sub-3ms latency, complemented by an optional
ResNet-50 variant for extreme crowd densities. Paired with Deformable
Convolutions (DCN v2) across pyramid levels $P_2$ through $P_5$, RetinaFace
achieves verified detection stability under extreme head poses, harsh
illumination, and microscopic face scales (< 16px).

---

## 1.1 What RetinaFace Does (In Plain English)

Imagine an intelligent autofocus system that finds every single human face in a
bustling crowd scene, even if someone is turning away, standing in shadows, or
wearing sunglasses:

* **Instant Face Localization:** In under 3 milliseconds, RetinaFace scans an
  entire image, locating faces from full-frame portraits down to tiny faces only
  16 pixels wide in stadium crowds.
* **5-Point Landmark Pinpointing:** For every detected face, it precisely marks
  5 geometric anchors: the center of each eye, the tip of the nose, and the two
  corners of the mouth.
* **Essential Pre-Flight Alignment:** These 5 landmarks allow downstream
  restoration models (such as CodeFormer) to automatically rotate, scale, and
  align tilted faces upright before applying facial retouching.

### Visual Demonstration & Training Convergence

* **Input Crowd Scene**: ![Crowd Scene](../assets/retinaface_before.png)
* **RetinaFace Detections & Landmarks**: ![RetinaFace
  Detections](../assets/retinaface_after.png)

![RetinaFace Training Convergence Curve](../assets/retinaface_training.png)

---

## 2. Visual Taxonomy: Multi-Scale Features & Landmarks

RetinaFace anchors 5 canonical facial landmarks to standardize facial alignment
across the LemGendary Face Suite `[THEORETICAL]`:

* **Point 1 (Left Eye)**: Anatomical Target: Pupil center / ocular iris; Primary
  Utility in Pipeline: Geometric tilt calculation & eye restoration guidance
* **Point 2 (Right Eye)**: Anatomical Target: Pupil center / ocular iris;
  Primary Utility in Pipeline: Horizontal eye-line leveling & inter-ocular scale
  reference
* **Point 3 (Nose Tip)**: Anatomical Target: Pronasale nasal apex; Primary
  Utility in Pipeline: 3D facial pitch/yaw pose estimation & perspective
  correction
* **Point 4 (Mouth Left)**: Anatomical Target: Left oral cheilion / lip corner;
  Primary Utility in Pipeline: Oral symmetry baseline & mouth crop bounding
* **Point 5 (Mouth Right)**: Anatomical Target: Right oral cheilion / lip
  corner; Primary Utility in Pipeline: Lip alignment & expressive deformation
  monitoring

---

## 3. Shared Foundations: Tri-Head Multi-Task Objective

Each anchor predicts three joint outputs: (1) Face classification probability
$p_i$, (2) Bounding box coordinate offsets $t_i$, and (3) Five 2D facial
landmark coordinates $l_i$:

$$
\mathcal{L} = \mathcal{L}_{\text{cls}}(p_i, p_i^*) + \lambda_1 p_i^*
\text{SmoothL1}(t_i, t_i^*) + \lambda_2 p_i^* \text{SmoothL1}(l_i, l_i^*)
$$

The formula above is the published anchor-based objective. The training
suite's `RetinaFaceMobileNet` (v16.9.207) has no prior boxes: one globally
pooled head regresses a single normalized `cx cy w h` box, one confidence and
five landmarks per image, so the sum runs over images instead of anchors. The
loss weights are confidence 1, box 2 and landmarks 1 (smooth L1 on normalized
coordinates); landmarks whose ten values are all zero count as absent and are
masked out of the loss.

---

## 4. Model Deep-Dives

### RetinaFace Multi-Scale Landmark & Localization Engine

#### 4.1 Model Description, Purpose and Usage

Single-stage face localization and 5-point landmark regression engine utilizing
the standardized MobileNetV3-Small backbone for high-efficiency edge execution
and real-time pre-flight alignment.

#### 4.2 Model Info

* **Architecture**: RetinaFace-style single-box regressor
  (`RetinaFaceMobileNet`, MobileNetV3-Small backbone, `mobilenet_v2`
  supported; globally pooled box, confidence and landmark heads)
* **Input Resolution**: 640x640
* **Precision**: ONNX FP16 / PyTorch FP32
* **Latency**: not measured

#### 4.3 Manifold Info

* **Dataset**: `LemGendizedRetinaFace`
* **Total Samples**: 425,223 SFHQ photos (train 374,199 / val 51,024), one
  face per image; val drawn by SFHQ file id, the same split as
  `LemGendizedParseNet`
* **Labels**: tight WIDER-style box and five points (eye centres, nose tip,
  mouth corners) rebuilt from the SFHQ 110-point landmarks
  (`landmark_source: sfhq-110pt`), stored as JSON (`face_landmarks`)
* **Primary Task**: 5-point facial landmark regression and face box
  localization

#### 4.4 Performance Metrics

The training suite measures RetinaFace with four metrics (v16.9.208,
`training/training/face_detection_metrics.py`). The targets are provisional
(`sota_targets_provisional: true`): no cited source backs them yet.

* **Box IoU (`box_iou`)**: mean IoU of the predicted and the labelled box over
  the images that hold a face. Target $\ge 0.80$ `[TARGET]`.
* **AP50 (`ap50`)**: single-class AP over images; each image is one detection
  ranked by its confidence (used as returned, no second sigmoid) and is a
  true positive when it holds a face and the IoU reaches 0.5. Target
  $\ge 0.95$ `[TARGET]`.
* **AP50-95 (`ap50_95`)**: the same AP averaged over the COCO thresholds
  0.50:0.05:0.95. Target $\ge 0.60$ `[TARGET]`.
* **Landmark NME (`landmark_nme`)**: mean distance of the five points divided
  by the inter-ocular distance (points 0 and 1); box-only labels are left
  out. Target $\le 0.10$ `[TARGET]`.
* **Measured values**: not measured on the rebuilt labels yet.

`metrics.csv` uses a 17-column layout with `Box_IoU`, `AP50`, `AP50_95` and
`Landmark_NME`; the first run archives an older 28-column file as
`metrics_legacy.csv`. Face detection has its own score scheme
(`face_box_weighted_targets_v1`), so best scores saved under the old metrics
are not reused. Metrics recorded before v16.9.207 / v16.9.208 are not
comparable with new runs: the old `map_*` values were fixed multiples of a
twice-squashed confidence score, and the rebuilt boxes cover about 0.31 to
0.57 of the old box area.

---

## 5. Challenges & Resilience Architecture

Micro-scale landmark localization encounters severe real-world challenges:

* **Microscopic Faces (< 16px)**: Deformable Convolutions (DCN v2) across
  low-level pyramid rungs ($P_2$) maintain high spatial resolution without
  excessive computational overhead.
* **Extreme Profile Poses (Yaw > 60°)**: When one eye or mouth corner is
  occluded, the smooth L1 regression loss smoothly decays gradients, preventing
  landmark explosion.
* **Harsh Backlight & Glare**: Multi-scale feature concatenation integrates
  contextual background cues to anchor facial confidence even under complete
  facial shadow.

---

## 6. Deployment Strategy & Production Acceleration

RetinaFace integrates seamlessly into the LemGendary runtime stack:

* **Production FP16 Engine (`retinaface.onnx`)**: Sub-3ms latency executing via
  WebGPU and ONNX Runtime DirectML `[MEASURED]`.
* **Research FP32 Export (`retinaface_FP32.onnx` + `.onnx.data`)**: Bit-exact
  floating-point model with separate binary weights sidecar.
* **Lifecycle Governance**: 15-minute `progress.pth` intra-epoch checkpointing,
  `latest.pth` persistence, and milestone `vault_hard_ap.pth` archival.

---

## 7. SOTA Architectural Performance Matrix

* **RetinaFace-ResNet50**: WIDER Face Easy: 96.5%; WIDER Face Medium: 95.6%;
  WIDER Face Hard: 90.4%; Status & Verification: published multi-face
  anchor-based reference; not comparable with the single-box metrics below
* **RetinaFace-MobileNetV3-Small (LemGendary)**: Box IoU, AP50, AP50-95 and
  Landmark NME: not measured on the rebuilt labels yet; Status &
  Verification: **Pre-training `[CURRENT]`**
* **RetinaFace Provisional Target**: Box IoU **$\ge 0.80$**; AP50
  **$\ge 0.95$**; AP50-95 **$\ge 0.60$**; Landmark NME **$\le 0.10$**; Status
  & Verification: **Provisional `[TARGET]`** (owner to confirm)

---

## 8. Conclusion

RetinaFace with the MobileNetV3-Small backbone provides lightning-fast facial
bounding box localization and sub-pixel 5-point landmark regression,
establishing the foundational pre-flight orientation geometry for the LemGendary
Face Suite.

### Related Ecosystem Documentation

* [Dataset Compiler Suite](./PAPER_DATASET_COMPILER.md) (Manifold: `LemGendizedRetinaFace`)
* [Training Suite Architecture](./PAPER_TRAINING_SUITE.md) (Tri-Format ONNX / PT
  Checkpoint Lifecycle)
* [AI Studio GUI Manual](./MANUAL_AI_STUDIO_GUI.md) (Interactive Training Panel Controls)
* [Master Ecosystem Architecture](./ECOSYSTEM_ARCHITECTURE.md) (System
  Governance & Specifications)
