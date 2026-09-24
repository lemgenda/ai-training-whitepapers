<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: CodeFormer: VQ-Codebook Face Restoration

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 08 FACE  
**Target Hardware**: NVIDIA GeForce GTX 1650 / Apple Silicon / T4

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Discrete Codebook Prior](#2-discrete-codebook-prior)
* [3. Transformer Feature Matching](#3-transformer-feature-matching)
* [4. Controllable Fidelity Scalar (Alpha)](#4-controllable-fidelity-scalar-alpha)
* [5. Loss Formulations & Multi-Objective](#5-loss-formulations--multi-objective)
* [6. Benchmark Comparisons](#6-benchmark-comparisons)
* [7. Conclusion](#7-conclusion)

---

## 1. Abstract

**CodeFormer** is a robust blind face restoration algorithm that models high-quality facial representations through a discrete **Vector-Quantized (VQ) codebook** prior and a Transformer-based prediction network. Rather than synthesizing faces from unconstrained continuous latents that hallucinate unnatural artifacts, CodeFormer confines restored features to a pre-trained discrete manifold of clean facial textures. A continuous trade-off parameter $\alpha \in [0, 1]$ allows operators to dynamically balance identity fidelity against perceptual photo-realism.

---

## 2. Discrete Codebook Prior

The codebook $\mathcal{C} = \{c_k\}_{k=1}^K \subset \mathbb{R}^d$ consists of $K = 1024$ learned discrete code vectors capturing high-frequency eye, skin, and facial geometry primitives. Features $z$ from severely degraded inputs are mapped to their nearest codebook entries:

$$z_q = \arg\min_{c_k \in \mathcal{C}} \|z - c_k\|_2$$

---

## 3. Transformer Feature Matching

To overcome severe degradation where nearest-neighbor Euclidean lookup fails, a 9-layer Transformer predicts global contextual codebook indices, ensuring anatomically consistent restoration even under severe occlusion or heavy sensor blur.

---

## 4. Controllable Fidelity Scalar (Alpha)

CodeFormer introduces an adjustable modulation scalar $\alpha$ governing intermediate feature fusion:

$$\tilde{F} = \alpha \cdot F_{\text{input}} + (1 - \alpha) \cdot F_{\text{codebook}}$$

When $\alpha = 1.0$, maximum identity preservation is enforced (ideal for biometric matching); when $\alpha = 0.0$, maximum perceptual enhancement and de-noising are applied.

---

## 5. Loss Formulations & Multi-Objective

$$\mathcal{L} = \|I - \hat{I}\|_1 + \lambda_{\text{perc}} \mathcal{L}_{\text{VGG}} + \lambda_{\text{code}} \|\text{sg}[z] - z_q\|_2^2 + \lambda_{\text{adv}} \mathcal{L}_{\text{WGAN}}$$

---

## 6. Benchmark Comparisons

| Model Benchmark | LPIPS (Lower is better) | Degradation Resistance | Identity Sim (CSIM) |
| :--- | :--- | :--- | :--- |
| GFPGAN v1.4 | 0.362 | Medium | 0.742 |
| **CodeFormer ($\alpha=0.5$)** | **0.315** | **Extreme** | **0.785** |

---

## 7. Conclusion

CodeFormer provides unparalleled face restoration by grounding hallucination in discrete geometric priors.
