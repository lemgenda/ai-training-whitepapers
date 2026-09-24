<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: Dedicated Image Restoration Suite

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 04 RESTORATION  
**Target Hardware**: NVIDIA GeForce GTX 1650 (4GB) / Apple Silicon (MPS) / Intel ARC (XPU)

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Physical Optical Degradation Taxonomy](#2-physical-optical-degradation-taxonomy)
* [3. Architectural Taxonomy](#3-architectural-taxonomy)
* [4. Mathematical Loss Formulations](#4-mathematical-loss-formulations)
* [5. SOTA Architectural Performance Matrix](#5-sota-architectural-performance-matrix)
* [6. Universal Hardware Deployment](#6-universal-hardware-deployment)
* [7. Conclusion](#7-conclusion)

---

## 1. Abstract

The **Dedicated Image Restoration Suite** establishes an authoritative, single-task deep learning framework engineered for physical image restoration across four classical degradation domains: **Deblurring and Denoising** (NAFNet), **Multi-Stage Progressive Deraining** (MPRNet), **Dual-Residual Exposure and Low-Light Enhancement** (MIRNet v2), and **Feature Fusion Atmospheric Dehazing** (FFANet). Each architecture in Category 04 operates without multi-task cross-talk, maximizing domain-specific reconstruction fidelity, peak signal-to-noise ratio (PSNR), and structural similarity (SSIM).

---

## 2. Physical Optical Degradation Taxonomy

The suite targets five distinct optical phenomena:

1. Motion and Defocus Blur (NAFNet Deblurring)
2. Heteroscedastic Sensor Noise (NAFNet Denoising)
3. Physical Rain Streaks and Transmission Occlusion (MPRNet Deraining)
4. Extreme Underexposure and Low-Light Attenuation (MIRNet v2)
5. Koschmieder Atmospheric Scattering Haze (FFANet Indoor and Outdoor)

---

## 3. Architectural Taxonomy

* **NAFNet**: Nonlinear Activation-Free network with SimpleGate and Simple Channel Attention.
* **MPRNet**: Multi-Stage Progressive Restoration with Cross-Stage Feature Fusion (CSFF).
* **MIRNet v2**: Dual-residual multi-scale architecture with Selective Kernel Feature Fusion (SKFF).
* **FFANet**: Feature Fusion Attention network with pixel and channel attention blocks.

---

## 4. Mathematical Loss Formulations

All models optimize a combination of Charbonnier loss, edge frequency supervision, and perceptual guidance:

$$\mathcal{L}_{\text{Restoration}} = \sqrt{\|\mathbf{I}_{\text{pred}} - \mathbf{I}_{\text{gt}}\|^2 + \epsilon^2} + \lambda_{\text{edge}} \sqrt{\|\nabla \mathbf{I}_{\text{pred}} - \nabla \mathbf{I}_{\text{gt}}\|^2 + \epsilon^2} + \lambda_{\text{perc}} \mathcal{L}_{\text{LPIPS}}(\mathbf{I}_{\text{pred}}, \mathbf{I}_{\text{gt}})$$

---

## 5. SOTA Architectural Performance Matrix

| Model Key | Target Dataset Manifold | Resolution Ladder | Target PSNR | Target SSIM | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `nafnet_debluring` | `LemGendizedNafNetDebluringLarge` | [256, 384, 512] | &ge; 33.90 dB | &ge; 0.970 | Trained / Active |
| `nafnet_denoising` | `LemGendizedNafNetDenoisingLarge` | [256, 384, 512] | &ge; 40.20 dB | &ge; 0.965 | Trained / Active |
| `mprnet_deraining` | `LemGendizedMprNetDerainingLarge` | [256, 384, 512] | &ge; 32.50 dB | &ge; 0.940 | Trained / Active |
| `mirnet_exposure` | `LemGendizedMirNetExposureLarge` | [256, 384, 512] | &ge; 23.50 dB | &ge; 0.880 | Trained / Active |
| `mirnet_lowlight` | `LemGendizedMirNetLowlightLarge` | [256, 384, 512] | &ge; 24.80 dB | &ge; 0.890 | Trained / Active |
| `ffanet_indoor` | `LemGendizedFfaNetIndoorLarge` | [256, 384, 512] | &ge; 36.50 dB | &ge; 0.985 | Trained / Active |
| `ffanet_outdoor` | `LemGendizedFfaNetOutdoorLarge` | [256, 384, 512] | &ge; 34.00 dB | &ge; 0.975 | Trained / Active |

---

## 6. Universal Hardware Deployment

All dedicated restoration models compile to static ONNX graphs (Opset 17) and WebGPU shader pipelines for low-latency inference on consumer hardware.

---

## 7. Conclusion

The Dedicated Image Restoration Suite provides high-fidelity, single-task image recovery across classical optical distortions.
