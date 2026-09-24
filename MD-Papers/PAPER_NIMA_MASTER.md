<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: Image Quality Assessment & Authenticity Suite

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 07 QUALITY  
**Target Hardware**: NVIDIA GeForce GTX 1650 (4GB) / Apple Silicon (MPS) / Intel ARC (XPU)

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Four-Quadrant Quality Taxonomy](#2-four-quadrant-quality-taxonomy)
* [3. Resonance Loss & Rank Optimization](#3-resonance-loss--rank-optimization)
* [4. Model Family Architecture](#4-model-family-architecture)
* [5. SOTA Architectural Performance Matrix](#5-sota-architectural-performance-matrix)
* [6. Conclusion](#6-conclusion)

---

## 1. Abstract

The **LemGendary NIMA Suite (Category 07)** provides a multi-dimensional perceptual assessment system spanning three fundamental axes of vision evaluation: **Aesthetic Appeal**, **Technical Quality**, and **Generative Media Authenticity (Real vs. AI)**. Leveraging Earth Mover's Distance (EMD) and Soft-Spearman rank correlation loss, the suite maps continuous visual manifolds to human perceptual ratings without score saturation.

---

## 2. Four-Quadrant Quality Taxonomy

1. Quadrant 1: High Aesthetic / High Technical
2. Quadrant 2: High Aesthetic / Low Technical
3. Quadrant 3: Low Aesthetic / Low Technical
4. Quadrant 4: Low Aesthetic / High Technical

---

## 3. Resonance Loss & Rank Optimization

$$\mathcal{L}_{\text{EMD}}(p, \hat{p}) = \left( \frac{1}{N} \sum_{k=1}^N |\text{CDF}_p(k) - \text{CDF}_{\hat{p}}(k)|^r \right)^{1/r}$$

$$\mathcal{L}_{\text{Resonance}} = \mathcal{L}_{\text{EMD}} + \lambda_{\text{rank}} \mathcal{L}_{\text{SoftSpearman}}$$

---

## 4. Model Family Architecture

* `nima_aesthetic_mobile`: MobileNetV3-Small backbone (224px, SRCC &ge; 0.650)
* `nima_aesthetic_efficientnet`: EfficientNetV2-S backbone (384px, SRCC &ge; 0.700)
* `nima_aesthetic_pro`: Swin-v2-T Transformer backbone (384px, SRCC &ge; 0.720)
* `nima_technical`: EfficientNetV2-S artifact detection (384px, SRCC &ge; 0.750)
* `nima_authenticity`: Generative AI vs Real classification (384px, Accuracy &ge; 0.940)

For full mathematical proofs, refer to [PAPER_LEMGENDARY_NIMA.md](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/PAPER_LEMGENDARY_NIMA.md).
