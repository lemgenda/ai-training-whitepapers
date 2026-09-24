<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: Large Language Models & Mixture-of-Experts (MoE)

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 10 FOUNDATION  
**Target Hardware**: NVIDIA GeForce GTX 1650 / Apple Silicon / T4

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Causal Decoder Architecture](#2-causal-decoder-architecture)
* [3. RoPE & SwiGLU Formulations](#3-rope--swiglu-formulations)
* [4. Sparse Mixture-of-Experts Routing](#4-sparse-mixture-of-experts-routing)
* [5. KV Cache & Inference Throughput](#5-kv-cache--inference-throughput)
* [6. Parameter Specifications & Scaling](#6-parameter-specifications--scaling)
* [7. Conclusion](#7-conclusion)

---

## 1. Abstract

The **LemGendary Large Language Model (LLM) Suite** implements next-generation causal autoregressive Transformers incorporating **Rotary Position Embeddings (RoPE)**, **SwiGLU activation functions**, RMSNorm pre-normalization, and **Top-2 Sparse Mixture-of-Experts (MoE)** routing. Engineered to drive system-level automation, natural language dataset queries, and mathematical reasoning across the ecosystem, these models decouple active parameter compute from total parameter capacity, executing high-throughput token generation on consumer and enterprise hardware alike.

---

## 2. Causal Decoder Architecture

The network employs a decoder-only architecture where each token attends strictly to preceding tokens via causal attention masking, preventing future information leakage during training.

---

## 3. RoPE & SwiGLU Formulations

Positional encoding uses Rotary Position Embeddings (RoPE), rotating query and key vectors in complex 2D planes to naturally capture relative distance:

$$R_{\Theta, m}^d = \text{diag}(R_{\theta_1, m}, R_{\theta_2, m}, \dots, R_{\theta_{d/2}, m})$$

Feed-Forward networks replace standard GELU with SwiGLU (Swish Gated Linear Units):

$$\text{SwiGLU}(x) = (x W_1 \odot \sigma(x W_1)) W_2$$

---

## 4. Sparse Mixture-of-Experts Routing

In MoE layers, token representations are routed to the top 2 out of 8 expert FFNs via softmax gating with auxiliary load-balancing loss:

$$y = \sum_{i \in \text{Top2}} G(x)_i \cdot \text{Expert}_i(x)$$

$$\mathcal{L}_{\text{balance}} = \alpha \cdot N \sum_{i=1}^E f_i \cdot P_i$$

---

## 5. KV Cache & Inference Throughput

Grouped-Query Attention (GQA) combined with PagedAttention KV-caching maximizes continuous batching throughput, eliminating VRAM fragmentation.

---

## 6. Parameter Specifications & Scaling

| Model Configuration | Total Parameters | Active Parameters | Context Window |
| :--- | :--- | :--- | :--- |
| LemGendary-LLM-1B (Dense) | 1.1 Billion | 1.1 Billion | 8,192 tokens |
| LemGendary-MoE-8x1B | 7.2 Billion | 1.8 Billion | 32,768 tokens |

---

## 7. Conclusion

Sparse MoE decoders deliver unprecedented reasoning and language generation capabilities while adhering strictly to hardware memory bounds.
