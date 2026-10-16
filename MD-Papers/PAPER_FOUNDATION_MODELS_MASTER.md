<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: Generative & Multimodal Foundation Models

**Author**: Lem Treursic
**Version**: 16.7.3
**Category**: Category 10 FOUNDATION
**Target Hardware**: NVIDIA / Apple Silicon / Intel ARC / CPU

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Foundation Scaling Laws & Compute Budgets](#2-foundation-scaling-laws--compute-budgets)
* [3. Latent Diffusion Models (LDM)](#3-latent-diffusion-models-ldm)
* [4. Image-to-Text Vision-Language Models](#4-image-to-text-vision-language-models)
* [5. Causal Decoder Transformers & MoE](#5-causal-decoder-transformers--moe)
* [6. Distributed Training Dynamics](#6-distributed-training-dynamics)
* [7. Conclusion](#7-conclusion)

---

## 1. Abstract

The **Generative & Multimodal Foundation Models Suite (Category 10)** establishes the scientific and systems engineering blueprint for three emerging generative architectures within the LemGendary AI Ecosystem: **Latent Diffusion Models**, **Image-to-Text Vision-Language Models**, and **Large Language Models** (Causal Decoder-only & MoE).

---

## 2. Scaling Laws & Mathematical Foundations

### 2.1 The Compute-Optimal Scaling Law (Chinchilla Derivation)

Compute budget scaling for dense autoregressive transformer architectures follows the empirical and theoretical Chinchilla formulation:

$$C \approx 6 N D$$

where:

* $C$ represents total training compute budget in floating point operations ($\text{FLOPs}$).
* $N$ denotes the non-embedding active parameter count of the neural network.
* $D$ denotes the total volume of consumed training tokens or samples.

#### Derivation & First-Principles Accounting

For a dense transformer layer, each forward pass through feedforward and multi-head attention projection weights performs approximately:

$$\text{FLOPs}_{\text{forward}} \approx 2 N \text{ operations per token}$$

Because the backward pass requires computing gradients with respect to both activations (for propagation) and parameters (for weight updates), the backward pass requires approximately twice the floating point operations of the forward pass:

$$\text{FLOPs}_{\text{backward}} \approx 4 N \text{ operations per token}$$

Summing both phases yields:

$$\text{FLOPs}_{\text{step}} = \text{FLOPs}_{\text{forward}} + \text{FLOPs}_{\text{backward}} \approx 6 N \text{ operations per token}$$

Multiplying across the token manifold $D$ gives $C \approx 6ND$.

#### Crucial Assumptions & Architectural Boundaries

1. **Dense Transformer Dominance**: Assumes parameter-dominated matrix multiplications ($\text{GEMM}$) where feedforward and attention projection layers constitute $\ge 95\%$ of computation.
2. **Exclusion of Attention Softmax**: The quadratic attention computation $\mathcal{O}(S^2 \cdot d)$ is assumed negligible relative to $6ND$ for typical sequence lengths ($S \le 4096$). For long-context models ($S \ge 32\text{k}$), quadratic attention FLOPs must be modeled explicitly.
3. **Exclusion of Embedding Projections**: Vocabulary embedding and final un-embedding layers are excluded from $N$ to avoid distortion in small models with large vocabularies.
4. **Mixture-of-Experts (MoE) Adjustment**: For sparse MoE architectures (e.g. 8-expert routing with top-2 active), $N$ must be replaced with $N_{\text{active}}$, representing only the parameters actively executed per token:
   $$C_{\text{MoE}} \approx 6 N_{\text{active}} D$$

---

### 2.2 First-Principles VRAM Allocation & Hardware Governors

Memory containment during large-scale foundation model training requires exact accounting across static allocations, dynamic activations, and framework overhead:

$$M_{\text{total}} = M_{\text{params}} + M_{\text{grads}} + M_{\text{opt}} + M_{\text{activations}} + M_{\text{workspace}}$$

#### 1. Parameter Memory ($M_{\text{params}}$)

Stores the model weights. For a model with $N$ parameters:

* **FP32 Precision**: $M_{\text{params}} = 4N \text{ bytes}$
* **FP16 / BF16 Mixed Precision**: $M_{\text{params}} = 2N \text{ bytes}$
* **8-Bit Quantized Baseline**: $M_{\text{params}} = 1N \text{ bytes}$

#### 2. Gradient Memory ($M_{\text{grads}}$)

Stores backpropagated gradients for all trainable parameters:

* **FP32 Gradients**: $M_{\text{grads}} = 4N \text{ bytes}$
* **FP16 / BF16 Gradients**: $M_{\text{grads}} = 2N \text{ bytes}$

#### 3. Optimizer State Memory ($M_{\text{opt}}$)

The optimizer maintains running historical moments for adaptive updates. For standard AdamW:

* **Standard FP32 AdamW** (First moment $m_t$ + Second moment $v_t$ + Master FP32 weights):
  $$M_{\text{opt}} = 4N (m_t) + 4N (v_t) + 4N (\text{master copy}) = 12N \text{ bytes}$$
* **8-Bit AdamW (bitsandbytes)**:
  $$M_{\text{opt}} = 1N (m_t) + 1N (v_t) + 2N (\text{master copy}) = 4N \text{ bytes}$$
* **Adafactor / SGD with Momentum**:
  $$M_{\text{opt}} \approx 4N \text{ to } 8N \text{ bytes}$$

#### 4. Activation Memory ($M_{\text{activations}}$)

Stores intermediate forward tensors required during backpropagation:

* **Without Activation Checkpointing**:
  $$M_{\text{activations}} = B \cdot S \cdot L \cdot \left( 34 \cdot d_{\text{model}} + 5 \cdot a \cdot S \right) \text{ bytes}$$
  where $B$ is batch size, $S$ is sequence length, $L$ is layer count, and $a$ is number of attention heads.
* **With Selective FlashAttention-2 & Activation Checkpointing**:
  Recomputes intermediate activations on the backward pass, reducing activation memory to:
  $$M_{\text{activations}} \approx \mathcal{O}(B \cdot S \cdot d_{\text{model}} \cdot \sqrt{L})$$

#### 5. Framework Workspace & CUDA Context ($M_{\text{workspace}}$)

CUDA driver contexts, PyTorch caching allocators, and temporary GEMM scratch buffers allocate between $1.0\text{GB}$ and $2.5\text{GB}$ baseline memory.

---

## 3. Dedicated Whitepapers

* [Latent Diffusion Models Specification](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/PAPER_LEMGENDARY_DIFFUSION.md)
* [Image-to-Text Vision-Language Specification](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/PAPER_LEMGENDARY_IMAGE_TO_TEXT.md)
* [Large Language Models Specification](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/PAPER_LEMGENDARY_LLM.md)
