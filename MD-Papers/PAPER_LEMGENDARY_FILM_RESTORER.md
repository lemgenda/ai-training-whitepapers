<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: Universal Film Restorer

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 05 HYBRID  
**Target Hardware**: NVIDIA GeForce GTX 1650 / Apple Silicon / T4

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Analog Emulsion Physics](#2-analog-emulsion-physics)
* [3. Tri-Stream Architecture](#3-tri-stream-architecture)
* [4. Partial Convolution Inpainting](#4-partial-convolution-inpainting)
* [5. Chemical Dye Inversion](#5-chemical-dye-inversion)
* [6. Archival Preservation Targets](#6-archival-preservation-targets)
* [7. Conclusion](#7-conclusion)

---

## 1. Abstract

The **Universal Film Restorer** is a specialized deep neural network designed to preserve historical, cinematic, and analog photographic media. Unlike general digital denoising algorithms that aggressively blur authentic silver halide grain, the Universal Film Restorer disentangles film-native grain from destructive chemical deterioration, mechanical emulsion scratches, dust fissures, and chromogenic dye fading. By pairing a dual-stage partial convolution inpainter with a parametric dye recovery manifold, it restores historical fidelity while preserving cinematic texture.

---

## 2. Analog Emulsion Physics

Analog film degrades through optical, mechanical, and chemical mechanisms. The degradation model is formulated as:

$$I_{\text{archival}} = \mathcal{C}_{\text{dye}}\left( I_{\text{scene}} \odot e^{-\kappa d} \right) + \mathcal{G}_{\text{grain}}(\sigma_{\text{ISO}}) + \mathcal{M}_{\text{defect}} \odot I_{\text{scratch}}$$

where $\mathcal{C}_{\text{dye}}$ models cyan, magenta, and yellow dye fading over decades, $\mathcal{G}_{\text{grain}}$ is non-Gaussian photographic grain, and $\mathcal{M}_{\text{defect}}$ is a binary mask of physical scratches.

---

## 3. Tri-Stream Architecture

The architecture processes archival frames through three dedicated pathways: (1) **Defect Detection & Inpainting**, (2) **Dye Correction & Exposure Equalization**, and (3) **Texture & Grain Synthesizer**. The grain synthesizer retains high-frequency film character without retaining dust or mold spores.

---

## 4. Partial Convolution Inpainting

Mechanical scratches produce missing pixel information. Partial convolutions conditioned on defect masks ensure valid feature propagation without bleed:

$$W' = \begin{cases} W \cdot \frac{\mathbf{1}^T \mathbf{1}}{\mathbf{1}^T M} & \text{if } \mathbf{1}^T M > 0 \\ 0 & \text{otherwise} \end{cases}$$

---

## 5. Chemical Dye Inversion

Kodachrome and Ektachrome dyes decay at asymmetric exponential rates. A 3D Color Transform Lattice trained on synthetic chemical decay curves predicts channel-wise restoration matrices $\mathbf{T}_{\text{RGB}}$, reviving lost spectral richness.

---

## 6. Archival Preservation Targets

| Test Corpus | Scratch IoU | Color Delta-E (CIE76) | PSNR (dB) | Grain Fidelity (FID) |
| :--- | :--- | :--- | :--- | :--- |
| Historical 35mm (1950-1970) | 0.892 | 2.14 | 31.40 | 8.4 |
| 16mm Archival Newsreel | 0.875 | 2.86 | 30.12 | 11.2 |

---

## 7. Conclusion

The Universal Film Restorer guarantees historical preservation by treating analog media as a distinct physical medium, ensuring authentic aesthetic preservation without modern digital smoothing.
