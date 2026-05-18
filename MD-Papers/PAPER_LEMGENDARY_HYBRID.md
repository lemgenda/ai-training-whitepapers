# Architecture of LemGendary AI: Universal Hybrid Restoration Pipelines

**Author**: Lem Treursić  
**Version**: 1.0.0 - Unified Multi-Modal Release (2026 Specialization)  
**Target Hardware**: NVIDIA GeForce GTX 1650 (4GB) / Apple Silicon (MPS) / Intel ARC (XPU)

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Unified Hybrid Architectures](#2-unified-hybrid-architectures)
   - [2.1 UPN v2 Large: Parameterized Space-Recovery](#21-upn-v2-large-parameterized-space-recovery)
   - [2.2 Universal Film Restorer: Synthesized Degradation](#22-universal-film-restorer-synthesized-degradation)
   - [2.3 Multi-Task Restorer: Multiheaded Mixture-of-Experts Routing](#23-multi-task-restorer-multiheaded-mixture-of-experts-routing)
3. [Critical Architectural Optimizations](#3-critical-architectural-optimizations)
   - [3.1 Downsampled Global Attention (OOM Remediation)](#31-downsampled-global-attention-oom-remediation)
   - [3.2 Dynamic Filename Task Ingestion](#32-dynamic-filename-task-ingestion)
   - [3.3 Dynamic Validation Sharding & Auto-Expansion](#33-dynamic-validation-sharding--auto-expansion)
4. [Deployment Strategy & WebGPU Compatibility](#4-deployment-strategy--webgpu-compatibility)
5. [Conclusion](#5-conclusion)

---

## 1. Abstract

The **LemGendary Training Suite** achieves absolute multi-modal restoration parity through its **Universal Hybrid Architecture** release. By integrating parameterized steering networks, dynamic physical degradation modeling, and soft Mixture-of-Experts (MoE) multi-task routing, the suite expands beyond single-problem architectures. This paper presents the mathematical models, spatial complexity optimizations, and deployment pathways for three flagship models: **UPN v2 Large**, the **Universal Film Restorer**, and the **Multi-Task Restorer**. We demonstrate how memory-sentinel optimizations enable high-resolution restoration execution within highly constrained consumer hardware environments.

---

## 2. Unified Hybrid Architectures

### 2.1 UPN v2 Large: Parameterized Space-Recovery

The **UPN v2 Large** model represents our premier space-recovery and super-resolution engine. Built on top of residual channel-attention blocks, UPN v2 incorporates **Parameterized Steering Vectors** that allow real-time strength tuning during runtime execution.

- **Dynamic Kernel Steerability**: Rather than baking static restoration parameters into the weights, the steering vector dynamically scales internal residual feature maps.
- **Fixed-Shape ONNX Compliance**: Engineered specifically to prevent WebGPU slice and dynamic-shape boundary crashes in browser runtimes by enforcing strict static-tensor compilation formats during export.

### 2.2 Universal Film Restorer: Synthesized Degradation

The **Universal Film Restorer** targets the remediation of legacy analog film assets. Its primary innovation is its **Dynamic Film Degradation Synthesizer**, which eliminates the need for paired degraded/clean reference manifolds.

- **On-the-Fly Synthetic Injection**: Clean, high-fidelity source images (such as DIV2K) are dynamically degraded during batch ingestion.
- **Parametric Degradation Layers**: Randomly samples and blends spatial noise, continuous analog film grain, high-contrast dust specs, physical emulsion scratches, and localized chromatic aberration vectors.
- **Global Identity Recovery**: Forces the model to map severely corrupted visual arrays back to their mathematically clean high-resolution target anchors.

### 2.3 Multi-Task Restorer: Multiheaded Mixture-of-Experts Routing

The **LemGendized Professional Multi-Task Restoration Model** addresses heterogenous degradations through a unified architecture. It bypasses the need for running multiple isolated models sequentially.

- **Shared Encoder Backbone**: Features a deep spatial encoder that captures core texture representation.
- **Soft Routing Task Classifier**: A specialized classifier analyzes the latent features and generates a probability weight vector:
  $$\mathbf{w} \in \mathbb{R}^{11}$$
- **Mixture-of-Experts Heads**: Feeds the latent representations into 11 specialized restoration heads simultaneously:
  1. `DenoiseHead` (denoise)
  2. `DeblurHead` (deblur)
  3. `DerainHead` (derain)
  4. `DehazeHead` (dehaze_indoor)
  5. `DehazeHead` (dehaze_outdoor)
  6. `LowLightHead` (lowlight)
  7. `LowLightHead` (exposure)
  8. `SuperResHead` (superres)
  9. `GenericConvHead` (vintage)
  10. `GenericConvHead` (face_restorer)
  11. `GenericConvHead` (face_parser)
- **Linear Blending Output**: The final output is a dynamically weighted linear combination of the heads' outputs based on the routing probabilities:
  $$\hat{\mathbf{Y}} = \sum_{i=1}^{11} w_i \cdot \mathbf{H}_i(\mathbf{Z})$$

---

## 3. Critical Architectural Optimizations

### 3.1 Downsampled Global Attention (OOM Remediation)

Standard spatial self-attention possesses quadratic spatial complexity:
$$\mathcal{O}(N^2) = \mathcal{O}((H \times W)^2)$$

For high-fidelity inputs scaled up to $256 \times 256$ pixels, the sequence length is $65,536$, forcing PyTorch to attempt a massive **128 GB memory allocation** for the attention matrix on GPU/CPU forward passes.

To achieve robust consumer-grade hardware compatibility (targeting NVIDIA GTX 1650 / 4GB VRAM), we engineered the **Downsampled Global Attention (DGA)** block:

1. **Adaptive Average Pooling**: Downsamples spatial feature tensors dynamically to a stable sequence map of $32 \times 32$ pixels.
2. **Global Attention Computation**: Executes multihead spatial self-attention on the pooled $1,024$-token sequence, reducing memory consumption by over **4,000x** (limiting attention matrices to $<4\text{ MB}$ of VRAM).
3. **Bilinear Interpolation**: Interpolates the processed attention map back to the original input resolution $(H \times W)$ and injects it residually:
   $$\mathbf{X}_{\text{out}} = \mathbf{X} + \text{Interpolate}(\text{Attention}(\text{Pool}(\mathbf{X})))$$

This maintains 100% checkpoint compatibility with existing weights while rendering OOM crashes structurally impossible.

### 3.2 Dynamic Filename Task Ingestion

During dataset consolidation, multi-task models ingest millions of composite images. A critical failure mode discovered was **Task-Index Blindness**, where the loss engine received a static task label (e.g. `"restoration"` globally), locking the routing classifier into a single head and halting the optimization of secondary heads.

We implemented the **Dynamic Task-Index Extractor**:

- Instantiates a regex-driven analysis of compiled physical image filenames via `professionalmultitaskrestoration_[task]_compiled_[manifold]_[idx].jpg`.
- Maps physical compilation tags (`deblur`, `denoise`, `derain`, `dehaze_indoor`, `dehaze_outdoor`, `lowlight`, `exposure`, `superres`, `vintage`, `face_restorer`, and `face_parser`) natively back to task indices with backward-compatible substring fallbacks.
- Passes explicit `task_idx` targets to the `CombinedLoss` CrossEntropy classifier during training, forcing proper multi-head optimization.

### 3.3 Dynamic Validation Sharding & Auto-Expansion

To balance computational efficiency during optimization with rigorous quality assurance, the training suite implements a dual-mode validation regime:

- **Active Training Phases (Foundation, Expansion)**: Validation is constrained to a deterministic **30% subset** using a fixed random seed. Because evaluating high-fidelity perceptual metrics (LPIPS/FID) is highly compute-intensive, this sharding provides a **3x validation speedup**. The fixed seed ensures that the metrics baseline remains mathematically stable across epochs for the Governor's plateau-detection calculations.
- **Refinement Phase**: Once the model achieves maximum resolution and 100% training dataset fraction, the validation loader automatically auto-expands to **100% (the full validation dataset)**. This guarantees that final model checkpoints undergo a complete generalizability audit before production WebGPU deployment, protecting against local subset overfitting.

---

## 4. Deployment Strategy & WebGPU Compatibility

All Universal Hybrid models are exported utilizing **Opset 15/17** validation structures. The network architectures are stripped of all dynamic resizing logic and fully normalized to fixed visual dimensions. Weights are stored in highly efficient float16 parameters, ensuring fast transfer over PCIe lanes and zero-latency shader execution inside modern WebGPU browser kernels.

---

## 5. Conclusion

The **Universal Hybrid Restoration** paradigms set a new standard for efficient, high-fidelity AI processing. By combining dynamic physical degradation synthesis, parameterized steering, and memory-hardened global attention blocks, LemGendary AI models guarantee superior restoration performance across heterogeneous consumer hardware fleets.
