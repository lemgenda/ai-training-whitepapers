# Large Language Models & Mixture-of-Experts (MoE)

## Category 10 FOUNDATION | Architecture of LemGendary AI

**Author**: Lem Treursic · **Version**: `v16.9.27-STABLE` · **Target Hardware**:
NVIDIA GeForce GTX 1650 / Apple Silicon / T4

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

The **LemGendary Large Language Model (LLM) Suite** implements next-generation
causal autoregressive Transformers incorporating **Rotary Position Embeddings
(RoPE)**, **SwiGLU activation functions**, RMSNorm pre-normalization,
and **Top-2 Sparse Mixture-of-Experts (MoE)** routing. Engineered to drive
system-level automation, natural language dataset queries, and mathematical
reasoning across the ecosystem, these models decouple active parameter compute
from total parameter capacity, executing high-throughput token generation on
consumer and enterprise hardware alike.

---

## 2. Causal Decoder Architecture

The network employs a decoder-only architecture where each token attends
strictly to preceding tokens via causal attention masking, preventing future
information leakage during training.

---

## 3. RoPE & SwiGLU Formulations

Positional encoding uses Rotary Position Embeddings (RoPE), rotating query and
key vectors in complex 2D planes to naturally capture relative distance:

$$
R_{\Theta, m}^d = \text{diag}(R_{\theta_1, m}, R_{\theta_2, m}, \dots,
R_{\theta_{d/2}, m})
$$

Feed-Forward networks replace standard GELU with SwiGLU (Swish Gated Linear
Units, Shazeer 2020), projecting inputs through independent gate ($W_1$) and
value ($W_2$) matrices before down-projection ($W_3$):

$$
\text{SwiGLU}(x) = \left( \text{Swish}(x W_1) \odot (x W_2) \right) W_3 = \left(
(x W_1 \cdot \sigma(x W_1)) \odot (x W_2) \right) W_3
$$

---

## 4. Sparse Mixture-of-Experts Routing

In MoE layers, token representations are routed to the top 2 out of 8 expert
FFNs via softmax gating with auxiliary load-balancing loss:

$$
y = \sum_{i \in \text{Top2}} G(x)_i \cdot \text{Expert}_i(x)
$$

$$
\mathcal{L}_{\text{balance}} = \alpha \cdot N \sum_{i=1}^E f_i \cdot P_i
$$

---

## 5. KV Cache & Inference Throughput

Grouped-Query Attention (GQA) combined with PagedAttention non-contiguous block
allocation maximizes continuous batching throughput, significantly mitigating
virtual memory fragmentation during extended context inference.

---

## 6. Parameter Specifications & Scaling

| Model Configuration | Total Parameters | Active Parameters | Context Window |
| :--- | :--- | :--- | :--- |
| LemGendary-LLM-1B (Dense) | 1.1 Billion | 1.1 Billion | 8,192 tokens |
| LemGendary-MoE-8x1B | 7.2 Billion | 1.8 Billion | 32,768 tokens |

### 6.1 QLoRA Parameter-Efficient Fine-Tuning & Dynamic Quantization

For consumer hardware deployment (e.g. NVIDIA GeForce GTX 1650 with 4GB VRAM),
full parameter fine-tuning of 1.5B dense transformers is intractable. The suite
deploys **QLoRA (Quantized Low-Rank Adaptation)** utilizing NF4 (NormalFloat4)
weight quantization with double quantization and 16-bit LoRA adapter matrices
injected across projection layers (`q_proj`, `k_proj`, `v_proj`, `o_proj`,
`gate_proj`, `up_proj`, `down_proj`):

$$
W_{\text{eff}} = W_{\text{NF4}} + \frac{\alpha}{r} (B \cdot A)
$$

where rank $r=16$, $\alpha=32$, and LoRA dropout is $0.05$. NF4 loading is
opt-in: `GenericCausalLLM` quantizes only when `load_in_4bit=True` is passed
(default `False`); otherwise the LoRA adapters sit on a bfloat16 base on CUDA.

### 6.2 Hardware-Aware Dynamic Micro-Batch & Gradient Accumulation Scaling

Memory sentinels probe free VRAM at runtime. To prevent Out-Of-Memory (OOM)
faults while maintaining a stable target effective batch size
($B_{\text{eff}} = 24$), physical micro-batch size ($B_{\text{phys}}$) and
gradient accumulation steps ($K_{\text{accum}}$) are resolved dynamically:

$$
K_{\text{accum}} = \max\left(1, \operatorname{round}\left(
\frac{B_{\text{eff}}}{B_{\text{phys}}} \right)\right)
$$

On 4GB hardware, $B_{\text{phys}} = 2$ and $K_{\text{accum}} = 12$, yielding an
effective batch of 24 with peak activation memory constrained below 2.8 GB
(a sizing target; `ai_helper_lemgend` pins `batch_size: 2` and
`accumulation_steps: 12` in `unified_models_v2.yaml`, and the code does not
measure the 2.8 GB bound).

### 6.3 Token Accuracy & Autoregressive Validation Formulations

Validation loss ($\mathcal{L}_{\text{val}}$) is complemented by two primary
evaluation metrics:

1. **Perplexity ($\text{PPL}$)**: Evaluates confidence on validation tokens:

   $$
   \text{PPL} = \exp\left( \frac{1}{N} \sum_{i=1}^N \mathcal{L}_i \right)
   $$

2. **Non-Masked Token Accuracy ($\text{Acc}_{\text{token}}$)**: Evaluates
   next-token prediction correctness exclusively over assistant target turns,
   ignoring prompt tokens masked with $-100$:

   $$
   \text{Acc}_{\text{token}} = \frac{\sum_{i=1}^{M} \mathbb{I}\left(
   \hat{y}_i = y_i \right) \cdot \mathbb{I}\left( y_i \ne -100 \right)}
   {\sum_{i=1}^{M} \mathbb{I}\left( y_i \ne -100 \right)} \times 100\%
   $$

### 6.4 Pareto Milestone Vault Checkpointing & Adapter Souping

The `CheckpointLifecycleManager` records isolated milestone weights whenever an
evaluation run sets a new historical best in any SOTA target metric:

* `vault_eval_loss.pth`: Optimized for minimum cross-entropy loss.
* `vault_perplexity.pth`: Optimized for minimum perplexity.
* `vault_token_accuracy.pth`: Optimized for maximum token prediction accuracy.

These adapter checkpoints form a Pareto frontier in parameter space and can be
linearly blended via the Pareto Model Soup (`create_pareto_model_soup` in
`training/export/soup.py`) without retraining to generate an ensembled final
adapter weights binary.

### 6.5 Three-Way Partitioning & Held-Out Test Evaluation

To guarantee generalization without data contamination, instruction manifolds
adhere to Three-Way Partitioning (Train / Val / Test):

* **Deterministic Stratification**: Splits records according to declared ratios
  (`val_split` and `test_split`) across all seven corpus taxonomies, preventing
  epistemic bias and domain skew.
* **Held-Out Test Shard**: Sharded into `ai_helper_test.jsonl` with zero prompt
  or ID leakage into training or validation splits.
* **Post-Training Evaluation**: Evaluates the best milestone checkpoints across
  unseen test splits, recording `test_loss`, `test_perplexity`, and
  `test_token_accuracy` in the final `TrainingSummary`.

### 6.6 Edge Hardware Optimization: 4-Bit NF4 QLoRA, SDPA & Paged AdamW

To execute fine-tuning of 1.5B+ parameter causal language models on consumer
workstations constrained to 4 GB VRAM (e.g. NVIDIA GeForce GTX 1650), the
training suite deploys a multi-tier memory containment profile:

1. **NormalFloat-4 (NF4) Quantization**: Employs `bitsandbytes` 4-bit normal
   quantization with double quantization (`bnb_4bit_use_double_quant=True`),
   compressing FP32/BF16 base foundation weights from 3.1 GB to ~900 MB while
   retaining near-lossless numerical fidelity.
2. **Low-Rank Adaptation (QLoRA)**: Injects rank $r=16$, $\alpha=32$ adapters
   across all projection matrices ($q$, $k$, $v$, $o$, $\text{gate}$,
   $\text{up}$, $\text{down}$), training $<1\%$ of total network weights.
3. **Gradient Checkpointing & SDPA**: Recomputes activations during backward
   passes via `model.gradient_checkpointing_enable(use_reentrant=False)` and
   substitutes manual attention matrices with PyTorch Scaled Dot-Product
   Attention (`attn_implementation="sdpa"`).
4. **Paged 8-bit AdamW**: Leverages `bitsandbytes.optim.PagedAdamW8bit` to
   compress optimizer states to 8 bits and dynamically page optimizer states
   across CUDA unified memory when VRAM boundaries approach saturation.
5. **Sequence Clamping**: Constrains micro-batch to 1 and sequence length to 512
   tokens with 16 gradient accumulation steps, eliminating $O(N^2)$ memory spikes
   and preserving stable throughput on edge accelerators.

---

## 7. Conclusion

Sparse MoE decoders deliver unprecedented reasoning and language generation
capabilities while adhering strictly to hardware memory bounds.
