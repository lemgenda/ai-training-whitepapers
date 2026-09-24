<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: RetinaFace: Multi-Scale Facial Landmark Localization

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 08 FACE  
**Target Hardware**: NVIDIA GeForce GTX 1650 / Apple Silicon / T4

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Feature Pyramid & Deformable Convolutions](#2-feature-pyramid--deformable-convolutions)
* [3. Tri-Head Multi-Task Detection](#3-tri-head-multi-task-detection)
* [4. Multi-Task Objective & OHEM](#4-multi-task-objective--ohem)
* [5. WIDER Face & Landmark Benchmarks](#5-wider-face--landmark-benchmarks)
* [6. Conclusion](#6-conclusion)

---

## 1. Abstract

**RetinaFace** is a single-stage face localization network engineered for high-precision facial bounding box detection and **5-point landmark regression** (left eye, right eye, nose tip, left mouth corner, right mouth corner). Utilizing a lightweight MobileNet-0.25 backbone paired with Deformable Convolutions and a Feature Pyramid Network (FPN), RetinaFace achieves robust detection under extreme angles, harsh lighting, and microscopic face scales (&lt; 16px).

---

## 2. Feature Pyramid & Deformable Convolutions

Standard convolutions apply rigid sampling grids. RetinaFace applies Deformable Convolutions (DCN v2) across FPN levels $P_2, P_3, P_4, P_5$ to adaptively deform receptive fields to match natural facial contours regardless of pitch, yaw, or roll.

---

## 3. Tri-Head Multi-Task Detection

Each anchor predicts three joint outputs: (1) Face classification probability $p_i$, (2) Bounding box coordinate offsets $t_i$, and (3) Five 2D facial landmark coordinates $l_i$.

---

## 4. Multi-Task Objective & OHEM

$$\mathcal{L} = \mathcal{L}_{\text{cls}}(p_i, p_i^*) + \lambda_1 p_i^* \text{SmoothL1}(t_i, t_i^*) + \lambda_2 p_i^* \text{SmoothL1}(l_i, l_i^*)$$

Online Hard Example Mining (OHEM) balances gradients during anchor classification.

---

## 5. WIDER Face & Landmark Benchmarks

| Backbone Variant | WIDER Hard AP | NME (5-Point) | Inference (CPU / GTX 1650) |
| :--- | :--- | :--- | :--- |
| MobileNet-0.25 (Edge) | 82.4% | 0.061 | 14 ms / 3 ms |
| ResNet-50 (Accuracy) | 91.8% | 0.048 | 45 ms / 9 ms |

---

## 6. Conclusion

RetinaFace anchors the spatial alignment pipeline for all downstream face analysis and restoration tasks.
