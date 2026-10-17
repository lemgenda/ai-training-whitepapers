<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: Image Quality Assessment & Authenticity Suite

**Author**: Lem Treursic  
**Version**: `v16.9.27-STABLE`  
**Last Reviewed**: 2026-10-17  
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

Quality assessment decouples visual aesthetics from technical integrity across a 2x2 four-quadrant matrix, with Generative Media Authenticity evaluated as an orthogonal classification axis:

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

| Model Key | Focus Domain | Architectural Backbone | Input Resolution | Target Performance |
| :--- | :--- | :--- | :--- | :--- |
| `nima_aesthetic_mobile` | Edge & Mobile Scoring | MobileNetV3-Small | 224x224 | SRCC &ge; 0.650 |
| `nima_aesthetic_efficientnet` | Global Composition Scorer | EfficientNetV2-S | 384x384 | SRCC &ge; 0.700 |
| `nima_aesthetic_pro` | Professional Artistic Scorer | Swin-v2-T Transformer | 384x384 | SRCC &ge; 0.720 |
| `nima_technical` | Optical Artifact Detection | EfficientNetV2-S | 384x384 | SRCC &ge; 0.750 |
| `nima_authenticity` | AI vs. Real Classification | EfficientNetV2-S | 384x384 | Accuracy &ge; 0.940 |

For full mathematical proofs, refer to [PAPER_LEMGENDARY_NIMA.md](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/PAPER_LEMGENDARY_NIMA.md).

---

## 5. SOTA Architectural Performance Matrix

Comprehensive training curves, ablation studies, and architectural deep-dives are documented in the [Unified NIMA Technical Whitepaper](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/PAPER_LEMGENDARY_NIMA.md).

---

## 6. Conclusion

Category 07 provides complete visual quality perception, delivering quantitative scoring for automated quality gates and dataset synthesis pipelines.
