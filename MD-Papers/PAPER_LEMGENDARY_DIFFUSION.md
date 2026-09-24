<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: Latent Diffusion & Score-Based Generative Architectures

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 10 FOUNDATION  
**Target Hardware**: NVIDIA GeForce GTX 1650 / Apple Silicon / T4

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Latent Space Compression](#2-latent-space-compression)
* [3. Stochastic Differential Equations & Score Matching](#3-stochastic-differential-equations--score-matching)
* [4. Classifier-Free Guidance (CFG)](#4-classifier-free-guidance-cfg)
* [5. Fast Schedulers (DDIM & Euler-A)](#5-fast-schedulers-ddim--euler-a)
* [6. Architecture & Training Parameters](#6-architecture--training-parameters)
* [7. Conclusion](#7-conclusion)

---

## 1. Abstract

The **LemGendary Latent Diffusion Engine** implements score-based generative modeling over continuous latent representations. Rather than executing stochastic reverse-diffusion in high-dimensional pixel space $\mathbb{R}^{H \times W \times 3}$, the model operates within the spatial latent manifold of a pre-trained Vector-Quantized Variational Autoencoder (VQ-VAE). Paired with cross-attention text conditioners, classifier-free guidance, and second-order Euler Ancestral sampling schedulers, the system synthesizes high-fidelity photographic content in as few as 20 sampling steps.

---

## 2. Latent Space Compression

A convolutional autoencoder encodes pixel inputs $x \in \mathbb{R}^{H \times W \times 3}$ into latent tensors $z = \mathcal{E}(x) \in \mathbb{R}^{h \times w \times c}$ with downsampling factor $f = H/h = 8$. The reverse diffusion process operates strictly in this compressed manifold, reducing memory footprint by $64\times$.

---

## 3. Stochastic Differential Equations & Score Matching

Forward noise injection follows the Ornstein-Uhlenbeck stochastic differential equation:

$$dz = -\frac{1}{2} \beta(t) z dt + \sqrt{\beta(t)} dw$$

The U-Net / DiT backbone is trained to predict the added noise via reweighted mean squared error:

$$\mathcal{L}_{\text{simple}} = \mathbb{E}_{z_0, \epsilon, t} \left[ \|\epsilon - \epsilon_\theta(z_t, t, c)\|^2 \right]$$

---

## 4. Classifier-Free Guidance (CFG)

Conditioned generation balances prompt alignment against sample diversity via Classifier-Free Guidance:

$$\tilde{\epsilon}_\theta(z_t, c) = \epsilon_\theta(z_t, \emptyset) + s \cdot \left( \epsilon_\theta(z_t, c) - \epsilon_\theta(z_t, \emptyset) \right)$$

where $s \in [5.0, 9.0]$ is the guidance scale.

---

## 5. Fast Schedulers (DDIM & Euler-A)

Deterministic DDIM and stochastic Euler Ancestral schedulers invert the probability flow ODE, reducing generation from 1000 DDPM steps to 20-30 discrete evaluation steps.

---

## 6. Architecture & Training Parameters

| Hyperparameter | Specification Value | Design Rationale |
| :--- | :--- | :--- |
| Latent Channels ($c$) | 4 | Optimal perceptual compression ratio |
| U-Net Base Channels | 320 | Channel multiplier [1, 2, 4, 4] |
| Conditioning Dimension | 768 / 1024 | Frozen CLIP ViT-L/14 or OpenCLIP text encoder |
| Precision | FP16 / BF16 mixed | Accelerated Tensor Core throughput |

---

## 7. Conclusion

Latent Diffusion serves as the generative foundation for generative synthesis and guided inpainting across the ecosystem.
