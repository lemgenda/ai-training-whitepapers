<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: YOLOv8n Multi-Task Perception Architecture

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 09 VISION  
**Target Hardware**: NVIDIA GeForce GTX 1650 / Apple Silicon / T4

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Anchor-Free CSPDarknet & PANet](#2-anchor-free-cspdarknet--panet)
* [3. Decoupled Head & TAL Assignment](#3-decoupled-head--tal-assignment)
* [4. CIoU & Distribution Focal Loss (DFL)](#4-ciou--distribution-focal-loss-dfl)
* [5. 17-Point Human Keypoint Estimation](#5-17-point-human-keypoint-estimation)
* [6. Performance Targets & WebGPU](#6-performance-targets--webgpu)
* [7. Conclusion](#7-conclusion)

---

## 1. Abstract

The **LemGendary YOLOv8n Multi-Task Model** provides a lightweight, anchor-free visual perception engine capable of simultaneous object detection, categorical classification, and 17-point human keypoint pose estimation. Operating on the compiled manifold `LemGendizedYoloV8n`, the network replaces heuristic anchor boxes with continuous bounding box distribution modeling. Decoupled detection heads eliminate task conflicts between classification and spatial regression, achieving high-throughput inference (&lt; 8ms on consumer GPUs) suitable for real-time edge processing.

---

## 2. Anchor-Free CSPDarknet & PANet

The backbone utilizes modified CSPDarknet53 with C2f modules that split feature channels across residual bottleneck branches, maximizing gradient flow while minimizing memory bandwidth. The neck employs a Path Aggregation Network (PANet) fusing multi-scale feature hierarchies $P_3, P_4, P_5$ via top-down and bottom-up pathways.

---

## 3. Decoupled Head & TAL Assignment

Unlike anchor-based YOLO models that share classification and localization convolutional layers, YOLOv8n features a decoupled head where classification and regression branches branch independently. Target assignment is governed by Task-Aligned Assigner (TAL):

$$t = s^\alpha \times \text{IoU}^\beta$$

where $s$ is the classification score and $\text{IoU}$ is the spatial bounding overlap.

---

## 4. CIoU & Distribution Focal Loss (DFL)

Bounding box regression optimizes Complete IoU (CIoU) and Distribution Focal Loss (DFL) to model boundary uncertainty:

$$\mathcal{L}_{\text{box}} = \text{CIoU}(b, b^{\text{gt}}) + \lambda_{\text{dfl}} \mathcal{L}_{\text{DFL}}(b, b^{\text{gt}})$$

$$\mathcal{L}_{\text{DFL}}(S_i, S_{i+1}) = -((q_{i+1} - q)\log(S_i) + (q - q_i)\log(S_{i+1}))$$

---

## 5. 17-Point Human Keypoint Estimation

The pose head predicts 17 standard COCO anatomical keypoints with visibility scores $v_i \in [0, 1]$, optimized via Object Keypoint Similarity (OKS) loss:

$$\text{OKS} = \frac{\sum_i \exp(-d_i^2 / 2s^2 k_i^2) \delta(v_i > 0)}{\sum_i \delta(v_i > 0)}$$

---

## 6. Performance Targets & WebGPU

| Target Task | Primary Metric | Target Goal | Inference Latency (GTX 1650) |
| :--- | :--- | :--- | :--- |
| Object Detection | mAP50-95 | $\ge 0.390$ | 7.2 ms |
| Classification | Top-1 Accuracy | $\ge 78.4\%$ | 3.1 ms |
| Pose Estimation | mAP50 (Pose) | $\ge 0.540$ | 8.4 ms |

---

## 7. Conclusion

YOLOv8n Multi-Task unifies spatial detection, categorization, and human pose estimation within a resilient, anchor-free framework optimized for universal hardware.
