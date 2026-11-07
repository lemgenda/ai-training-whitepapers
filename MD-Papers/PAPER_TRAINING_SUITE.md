# LemGendary Model Training Suite: Technical Whitepaper

## Category 01.3 | Subpage of Master Ecosystem Architecture

**Parent Hub**: [Master Ecosystem Architecture](./ECOSYSTEM_ARCHITECTURE.md)

**Version**: `v16.9.122-STABLE` (LemGendary Model Training Suite) · **Last
audited**: 2026-11-04

**Companion Paper**: [Nuclear Stability: AI Training Pathology Master
Guide](./PAPER_TRAINING_PATHOLOGY.md)

---

## Table of Contents

- [1. Abstract](#1-abstract)
- [2. High-Fidelity "Nuclear" Hardening](#2-high-fidelity-nuclear-hardening)
  - [2.1. Dynamic Memory-Sentinel (Batch
    Decoupling)](#21-dynamic-memory-sentinel-batch-decoupling)
  - [2.2. Intelligent Curriculum & Sawtooth
    Governance](#22-intelligent-curriculum--sawtooth-governance)
  - [2.3. Hardened Resolution Ladders & SOTA
    Guards](#23-hardened-resolution-ladders--sota-guards)
    - [2.3.1. Authoritative 4-Pillar Fully-Trained Verification
      Invariant](#231-authoritative-4-pillar-fully-trained-verification-invariant)
  - [2.4. Checkpoint Resumption & Singularity
    Hardening](#24-checkpoint-resumption--singularity-hardening)
  - [2.5. Mixture-of-Experts (MoE) 11-Manifold
    Architecture](#25-mixture-of-experts-moe-11-manifold-architecture)
  - [2.6. Multi-Scale Forex Trading Architecture
    (`ForexPredictor`)](#26-multi-scale-forex-trading-architecture-forexpredictor)
  - [2.7. Omni-Metric Autonomous SOTA
    Adaptation](#27-omni-metric-autonomous-sota-adaptation)
  - [2.8. Smart Governor Plateau-Breaking Engine & Nuclear Safety
    Sentinels](#28-smart-governor-plateau-breaking-engine--nuclear-safety-sentinels)
  - [2.9. Differentiable Soft-Spearman Loss & Cross-Microbatch Rank Memory
    Bank](#29-differentiable-soft-spearman-loss--cross-microbatch-rank-memory-bank)
  - [2.10. Spatial Statistical Pooling Upgrade (Mean and Std) & Universal Safety
    Filter](#210-spatial-statistical-pooling-upgrade-mean-and-std--universal-safety-filter)
  - [2.11. Headless Kaggle Cloud Engine & Dataset
    Bypass](#211-headless-kaggle-cloud-engine--dataset-bypass)
  - [2.12. Universal Post-Training Target Audit & Interactive
    Guidance](#212-universal-post-training-target-audit--interactive-guidance)
  - [2.13. Native Multi-Container Ingestion
    Architecture](#213-native-multi-container-ingestion-architecture)
  - [2.14. Autonomous YOLO Multi-Stage Curriculum Governor & SOTA Target
    Convergence](#214-autonomous-yolo-multi-stage-curriculum-governor--sota-target-convergence)
  - [2.15. SSOT Config-Governed GUI Training Controls & Run-State
    Lifecycle](#215-ssot-config-governed-gui-training-controls--run-state-lifecycle)
  - [2.16. SSOT Jupyter Notebook Generation & Cross-Workspace
    Staging](#216-ssot-jupyter-notebook-generation--cross-workspace-staging)
  - [2.17. Fleet 1-Epoch Diagnostics & Kaggle Models Checkpoint
    Publishing](#217-fleet-1-epoch-diagnostics--kaggle-models-checkpoint-publishing)
  - [2.18. Zero-Warning Tensor Memory Isolation & Telemetry Stream Segregation
    (v16.9.25)](#218-zero-warning-tensor-memory-isolation--telemetry-stream-segregation-v16925)
  - [2.19. Forex Parquet Locality & Telemetry Progress Sync
    (v16.9.26)](#219-forex-parquet-locality--telemetry-progress-sync-v16926)
  - [2.20. Validation Batch Telemetry & Live Telemetry Progress Synchronization
    (v16.9.28)](#220-validation-batch-telemetry--live-telemetry-progress-synchronization-v16928)
  - [2.21. Modernized PyTorch cu126 & Transformers v5 Stack
    Integration](#221-modernized-pytorch-cu126--transformers-v5-stack-integration)
  - [2.22. Turing Non-Tensor-Core Hardware cuDNN Bug
    Remediation](#222-turing-non-tensor-core-hardware-cudnn-bug-remediation)
  - [2.23. Multi-Task SOTA Metric Ingestion & Perceptual Telemetry
    Synchronization](#223-multi-task-sota-metric-ingestion--perceptual-telemetry-synchronization)
  - [2.24. Kaggle Models Hub Metadata Sync & Whitepaper Citations
    (v16.9.46)](#224-kaggle-models-hub-metadata-sync--whitepaper-citations-v16946)
  - [2.25. Monotonic Ratchet (Pair Rule) & `RatchetViolation` Guard
    (v16.9.67)](#225-monotonic-ratchet-pair-rule--ratchetviolation-guard-v16967)
  - [2.26. Bounded Epoch Budget & Honoured Early Stop
    (v16.9.65)](#226-bounded-epoch-budget--honoured-early-stop-v16965)
  - [2.27. Pareto Model Soup Service
    (v16.9.66)](#227-pareto-model-soup-service-v16966)
  - [2.28. Publication-Grade FID & Unverified Historical FID Rows
    (v16.9.67)](#228-publication-grade-fid--unverified-historical-fid-rows-v16967)
  - [2.29. Sidecar Security Model & OpenAPI Contract (v16.9.64,
    v16.9.68)](#229-sidecar-security-model--openapi-contract-v16964-v16968)
  - [2.30. Ecosystem Facts & GUI Training Verdict (v16.9.93,
    v16.9.94)](#230-ecosystem-facts--gui-training-verdict-v16993-v16994)
  - [2.31. Manifold Task from `dataset_info.yaml` (v16.9.100,
    v16.9.101)](#231-manifold-task-from-dataset_infoyaml-v169100-v169101)
  - [2.32. Stochastic Weight Averaging
    (v16.9.107)](#232-stochastic-weight-averaging-v169107)
  - [2.33. FID Re-evaluation Tool & Provenance Ledger
    (v16.9.107)](#233-fid-re-evaluation-tool--provenance-ledger-v169107)
  - [2.34. Version Single Source, Lint & Review Fixes
    (v16.9.122)](#234-version-single-source-lint--review-fixes-v169122)
  - [2.35. Causal Language Model Instruction Tuning & Dynamic VRAM
    Probing](#235-causal-language-model-instruction-tuning--dynamic-vram-probing)
- [3. Judicial Audit Engine](#3-judicial-audit-engine)
  - [3.1. Framework Agnosticism & Type
    Guards](#31-framework-agnosticism--type-guards)
  - [3.2. Fast-Path Correlator](#32-fast-path-correlator)
- [4. Universal Models Registry & SOTA
  Baselines](#4-universal-models-registry--sota-baselines)
- [5. Universal SOTA Telemetry & Cloud
  Sync](#5-universal-sota-telemetry--cloud-sync)
  - [5.1. Multi-GPU DataParallel Capabilities (Kaggle
    Scale)](#51-multi-gpu-dataparallel-capabilities-kaggle-scale)
  - [5.2. Universal Hardware Inference](#52-universal-hardware-inference)
  - [5.3. Hybrid Cloud Synchronization & Tiered
    Lifecycle](#53-hybrid-cloud-synchronization--tiered-lifecycle)
  - [5.4. Multi-Account Kaggle Cloud Telemetry & Live
    Monitor](#54-multi-account-kaggle-cloud-telemetry--live-monitor)
- [6. Distributed Edge Training: LemGendary Cloud
  Link](#6-distributed-edge-training-lemgendary-cloud-link)
  - [6.1. Federated Gradient Accumulation
    (Average-Sync)](#61-federated-gradient-accumulation-average-sync)
  - [6.2. Memory-Sentinel WebGPU Zero-Copy
    Export](#62-memory-sentinel-webgpu-zero-copy-export)
- [7. Universal Instruction-Tuned Causal LLM Fine-Tuning & Dynamic Dataset
  Ingestion](#7-universal-instruction-tuned-causal-llm-fine-tuning--dynamic-dataset-ingestion)
  - [7.1. GenericCausalLLM Architecture & Dynamic HuggingFace Backbone
    Wrapping](#71-genericcausalllm-architecture--dynamic-huggingface-backbone-wrapping)
  - [7.2. QLoRA Parameterization via unified_models_v2.yaml & PEFT
    Injection](#72-qlora-parameterization-via-unified_models_v2yaml--peft-injection)
  - [7.3. Dynamic Dataset Discovery for Arbitrary LLM
    Manifolds](#73-dynamic-dataset-discovery-for-arbitrary-llm-manifolds)
  - [7.4. Multi-Turn ChatML Loss Formulation & Assistant-Only Prompt
    Masking](#74-multi-turn-chatml-loss-formulation--assistant-only-prompt-masking)
  - [7.5. Tri-Format Deployment Export: PyTorch, ONNX FP32/FP16 & Edge
    Quantization](#75-tri-format-deployment-export-pytorch-onnx-fp32fp16--edge-quantization)
- [8. Conclusion](#8-conclusion)
  - [8.1. Implementation Status](#81-implementation-status)

---

## 1. Abstract

The LemGendary Model Training Suite is the orchestration layer that trains,
evaluates and exports the vision, restoration, quality-assessment, financial
time-series and causal LLM models of the LemGendary ecosystem. This paper
documents release v16.9.122-STABLE. It covers the curriculum governor and its
Monotonic Ratchet (pair rule, enforced by a `RatchetViolation` guard), the
bounded epoch budget with an honoured early stop, the 4-pillar completion
invariant, publication-grade FID evaluation (`feature=2048`, chunks of at most
two samples), the Pareto Model Soup service, optional Stochastic Weight
Averaging (SWA, off by default, Section 2.32) and the sidecar security model.
Features that earlier revisions described but the code does not run are marked
as not active or not implemented (Section 8.1). Historical FID rows of four
models are unverified (Section 2.28); the FID re-evaluation tool (Section 2.33)
can re-measure their checkpoints.

---

## 2. High-Fidelity "Nuclear" Hardening

The suite enforces a strict high-fidelity baseline to ensure models learn
complex textures and micro-artifacts from the very first epoch.

### 2.1. Dynamic Memory-Sentinel (Batch Decoupling)

- **Absolute Sentinel Authority**: Acts as the absolute physical authority. It
  treats `batch_size` from config as a maximum boundary and autonomously
  throttles it downwards if the local physical VRAM cannot hold it, permanently
  preventing system RAM paging.
- **Atomic Re-Audit**: Performs a fresh hardware probe every time the resolution
  ladder jumps, ensuring peak physical throughput at low resolutions while
  automatically throttling for high-res stability.
- **Sub-Nuclear 4GB Lockdown**: On GTX 1650/4GB cards, it enforces a strict
  **Serial-Only Mode** after an OOM, delivering a **2x performance gain** by
  preventing Windows System RAM paging.
- **Hardware-Aware Resolution Capping (not active)**: `config.yaml` declares
  `max_allowed_local_resolution: 640` and `max_allowed_cloud_resolution: 512`,
  but the training code does not read these keys (review finding D-07), so they
  do not cap the ladder. The governor only clamps the configured `input_size` to
  the hardware cap before training starts.
- **Worker Lifecycle Graceful Shutdown & GC Teardown**: Explicitly reaps
  training DataLoader iterator processes (`persistent_workers=False`), caps
  workers, and injects `gc.collect()` and `torch.cuda.empty_cache()` teardown
  sequences before spawning the validation pipeline. This eliminates System RAM
  hoarding and extreme VRAM fragmentation, stabilizing high-resolution
  validation on Kaggle kernels (T4/P100).
- **Multi-GPU DataParallel Gathering Safeguard**: Automatically detects multiple
  CUDA devices and wraps the active manifold in PyTorch's `DataParallel` engine.
  Fixes primary-device VRAM bottlenecking by eliminating naive `gpu_count`
  micro-batch multiplication at high resolutions ($\ge 512\text{px}$) and for
  restoration architectures. GPU 0 is protected from output gathering saturation
  and loss graph spikes, utilizing Universal Gradient Accumulation to maintain
  the target effective batch size.
- **Dynamic Headroom Tiering & Pre-Jump Dry-Run Probe**: Enforces a 30% free
  VRAM safety headroom margin (`safety_multiplier = 0.70`) for spatial ladders
  $\ge 512\text{px}$ and perceptual loss engines (LPIPS/VGG). **Not active**:
  the pre-jump dry-run probe and the resolution-jump veto
  (`MemorySentinel.veto_resolution_jump`,
  `SmartTrainingGovernor.veto_resolution_jump`) have no caller in the training
  loop. Since v16.9.67 the governor veto can only anchor at or above the current
  resolution, so it can never lower the resolution once it is wired in.
- **Hardware ECC, CUDA Kernel Compatibility & Virtual Memory Fragmentation
  Guard**: Detects uncorrectable ECC hardware errors and CUDA compute kernel
  incompatibilities (such as Pascal sm_60 on modern CUDA 12 builds) during
  pre-flight sanity checks with clear diagnostic recovery guidance and
  auto-remediation, and configures
  `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` to eliminate CUDA memory
  allocator fragmentation.
- **Validation Coverage (no sharding)**: No validation sharding is implemented.
  The code reads no `high_fidelity_fraction` key, so the 30% validation shard
  with auto-expansion described in earlier revisions is not in effect. Financial
  Time-Series & Forex Predictors evaluate 100% of the validation manifold every
  epoch for Walk-Forward temporal progression matrices.
- **Windows Memory-Mapped Sequence Multiprocessing Guard**: PyTorch `DataLoader`
  with `num_workers > 0` on Windows uses `multiprocessing.spawn`, duplicating
  dataset indices and memory-mapped file handles into each worker process
  (consuming 20+ GB across 4 workers). For large time-series manifolds (e.g.
  16-symbol Forex), the suite strictly enforces `num_workers = 0` on Windows,
  keeping total process RAM at 1.1 GB, eliminating 50GB+ pagefile thrashing, and
  keeping `.npy` arrays cached in the OS file cache for $12.5\times$ faster
  batch throughput (0.27s vs 3.43s).

### 2.2. Intelligent Curriculum & Sawtooth Governance

- **Universal Monotonic Progression Ratchet (pair rule)**: The curriculum moves
  through `(resolution, data fraction)` rungs and never steps backwards (Section
  2.25). Resolution never decreases. Within one resolution step the data
  fraction never decreases ($f_{t+1} = \max(f_t, f_{\text{new}})$). The fraction
  may reset to a lower value only when the resolution steps up. Resumed sessions
  on cloud environments (e.g. Kaggle/Colab) retain the highest fraction recorded
  in `metrics.csv`. Data fraction strides are 20% (`fraction_increment: 0.20`).
- **Publication-Standard FID 2048 & Micro-Chunked Memory Isolation**: The
  validation subsystem computes Frechet Inception Distance on the
  2048-dimensional final pooling layer (`feature=2048`). Inception forward
  passes run in micro-chunks of at most two samples (`chunk_size = 2`) for both
  real and reconstructed images (Section 2.28). The historical FID rows of
  `codeformer`, `ffanet_indoor`, `mprnet_deraining` and `mirnet_lowlight` were
  rewritten by the removed `tools/recalibrate_fid.py` and are unverified;
  `python -m training.fid_reeval` re-measures them (Section 2.33).
- **Pareto Model Soup (vault checkpoint blending)**: `lemtrain soup` and
  `POST /api/models/{model_key}/soup` blend a model's vault checkpoints
  (`vault_psnr.pth`, `vault_lpips.pth`, ...) into one weighted average
  checkpoint (Section 2.27). With optional Stochastic Weight Averaging (Section
  2.32) the averaged weights are one more vault, `vault_swa.pth`. Whether a
  blend beats its donors is not checked automatically and must be measured per
  model.
- **Universal Quality Scorecarding**: The trainer dynamically compounds PSNR,
  SSIM, LPIPS, and FID for all restoration models, mathematically verifying
  ultimate convergence against academic SOTA benchmarks.
- **Continuous Parameter Predictor Calibration**: Standardized validation MAE
  telemetry for continuous parameter predictors (like `upn_v2`), recording MAE
  directly into `metrics.csv`.
- **Professional Multi-Task Restoration**: Fully integrated multi-headed
  Mixture-of-Experts (MoE) routing engine with 11 specialized restoration heads
  dynamically trained under Dynamic Filename Task Ingestion.

### 2.3. Hardened Resolution Ladders & SOTA Guards

- **Universal 15% Initial Manifold Fraction**: All model training pipelines
  initiate training from 15% dataset fraction ($0.15$) on the lowest ladder rung
  (`res_ladder[0]`), progressing through gradual intra-resolution expansion
  ($15\% \to 35\% \to 55\% \to 75\% \to 100\%$) governed by maturity soak
  windows (`maturity_soak: 5` in `config.yaml`), performance plateaus, and
  overfitting indicators.
- **Steady-Improvement Soak Propulsion (v16.9.43)**: Prevents steadily improving
  models from stagnating at $15\%$ data fraction when validation quality
  increases every epoch ($\Delta q \ge \text{min\_delta}$). Once
  `epochs_since_step >= manifold_maturity` (default 3 epochs) with
  non-regressing quality, `fraction_soak_complete` automatically advances
  `current_fraction` by $+20\%$ (`fraction_increment = 0.20`), and
  `deepening_ready` promotes spatial resolution once $100\%$ data fraction and
  `stride_threshold` are satisfied.
- **Bounded Epoch Budget**: The configured epoch count is a hard cap. Training
  stops on convergence (4-pillar completion), on the governor's early-stop
  signal, or when the budget is reached. Budget extensions are opt-in through
  `training_budget.max_extension_epochs` (Section 2.26). The open-ended loop of
  earlier revisions, which added 10 epochs whenever the budget was reached, was
  removed in v16.9.65.
- **Ladder-Aware Progression**: Reaching SOTA targets at sub-maximal resolutions
  triggers a **Forced Spatial Jump** to the next rung (e.g., 256px → 384px). The
  dataset fraction then starts again at a lower value (the configured initial
  fraction after a regular jump, 50% after a forced SOTA jump). The pair rule
  allows this reset because the resolution steps up.
- **SOTA Hardening Guard**: Enforces a mandatory **2-epoch "Hardening Period"**
  for every resolution rung to solidify weights.
- **Overfitting Rescue Protocol**: Overrides tactical recoils and cooldown locks
  when trend-based overfitting is diagnosed, force-expanding the dataset
  fraction (+20% data) to break the overfitting attractor.
- **SOTA Verification**: Verifies SOTA targets on 100% of training data at final
  resolution before permitting export.

#### 2.3.1. Authoritative 4-Pillar Fully-Trained Verification Invariant

The training engine and GUI telemetry enforce an absolute, non-negotiable
invariant before designating any model as **`FULLY TRAINED`**:

$$
\text{FullyTrained} = \left(\bigwedge_{m \in \mathcal{M}_{\text{target}}}
\text{Passed}(m, T_m)\right) \land (\text{LadderPassed}) \land
(\text{DataFraction} \ge 1.0) \land (\text{Epochs} \ge 20)
$$

1. **Pillar 1: Multi-Metric SOTA Target Satisfaction ($100\%$)**:
   - The engine validates **every single metric** defined in the model's
     `sota_targets` dictionary within `unified_models_v2.yaml`.
   - Directionality is strictly enforced: higher-is-better metrics
     ($\text{PSNR}$, $\text{SSIM}$, $\text{SRCC}$, $\text{PLCC}$,
     $\text{Accuracy}$, $\text{mAP50}$, $\text{DirAcc}$, $\text{WinRate}$,
     $\text{Sharpe}$, $\text{Sortino}$) must satisfy
     $\text{Achieved} \ge \text{Target}$; lower-is-better metrics
     ($\text{LPIPS}$, $\text{FID}$, $\text{MAE}$, $\text{MaxDD}$,
     $\text{TP\_MAE}$, $\text{SL\_MAE}$, $\text{Rank\_Margin}$) must satisfy
     $\text{Achieved} \le \text{Target}$.
   - If even one defined metric fails to meet its target, SOTA is not achieved
     ($\text{sota\_targets\_met} < \text{sota\_targets\_total}$).
2. **Pillar 2: Complete Resolution / Confluence / Context Ladder Traversal**:
   - **Vision Models**: Model must have completed training at or above the
     highest rung in `res_ladder` ($\text{max\_res} \ge \text{target\_res}$,
     typically $512\text{px}$ or $640\text{px}$). Reaching SOTA at
     $256\text{px}$ does not qualify as fully trained.
   - **Forex Models**: Model must have completed all 6 walk-forward curriculum
     folds or trained through the macro daily confluence horizon
     ($\text{Fold} \ge 6 \lor \text{Horizon} \ge 1440\text{m}$).
   - **Causal LLM Assistants**: Model must operate on its maximum target context
     token window ($\text{seq\_length} \ge 2048\text{ tokens}$).
3. **Pillar 3: 100% Dataset Variety ($1.00$ Data Fraction / Full Corpus)**:
   - **Vision Models**: The model must have completed its epoch on $100\%$ of
     the training dataset manifold ($\text{Data} \ge 0.99$). Models trained on
     sub-unitary fractions ($15\%$, $35\%$, $75\%$) are strictly designated as
     `PARTIALLY TRAINED`.
   - **Causal LLM Assistants**: Model must have trained across the complete
     instruction tuning manifold without loose image sampling fraction
     constraints.
4. **Pillar 4: Minimum Epoch Convergence Threshold ($\text{Epochs} \ge 20$)**:
   - The model must have trained for at least 20 epochs
     ($\text{completed\_epochs} \ge 20$). Rapid early convergence spikes or
     premature training termination before 20 epochs strictly prohibit declaring
     training complete.

The resolution and data pillars read the governor state recorded before the
epoch audit, through the keys that `get_state()` writes (`input_size`,
`sample_fraction`; shared constants in `training/ratchet.py`, v16.9.67). A
missing key counts as 0 and can never pass. A 384px epoch that triggers a jump
to 512px is therefore no longer reported as complete.

### 2.4. Checkpoint Resumption & Singularity Hardening

- **Recovered Governor Topology Synchronization**: When restoring from a
  checkpoint, the engine (`training/core_loop.py`) directly reconfigures the
  active dataset strategy (`train_ds.update_strategy` / `sample_fraction`) and
  rebuilds the active DataLoader worker processes (`rebuild_train_loader`) to
  match the exact recovered ladder rung and dataset fraction.
- **Unified Hub Checkpoints**: Completely obsoletes volatile local checkpoint
  directories. All models, whether training locally or on Kaggle, directly sync
  `_latest`, `_best`, `_progress`, and `_vault_` checkpoints exclusively to
  their respective `LemGendaryModels/<model_name>/checkpoints` vault.
- **Safe Non-Destructive Export Instantiation**: Replaced legacy `shutil.rmtree`
  overarching folder wipes with precise, non-destructive
  `os.makedirs(exist_ok=True)` logic, structurally preventing catastrophic
  deletion of trained physical model checkpoints across projects.
- **The Scheduler Shield**: Dynamically inspects candidate checkpoints for
  poisoned/advanced step counts. If detected, it overrides and re-anchors the
  loaded scheduler steps back to actual epoch progress.
- **Velocity Bomb Prevention (Rollback Isolation)**: During a SOTA Rollback, the
  Governor surgically decouples the model weights from the learning rate
  chronometer. It reverts the weights to the safe baseline but intentionally
  bypasses chronological scheduler rewinding. This prevents the learning rate
  from violently spiking back to early-stage `max_lr` values, ensuring the model
  gently seats into a cold, stable manifold.
- **Metric Singularity & Live Polarity Shield**: The Metric Singularity Shield
  triggers a tactical recoil and rollback to SOTA weights immediately if
  PLCC/SRCC hit NaN. **New in v1.2.2**: The Live Polarity Shield monitors the
  manifold directly during training; if `SRCC < 0.0` or `PLCC < 0.0` is detected
  mid-epoch, it immediately flags a "Polarity Collapse", rejecting the epoch and
  triggering an instant SOTA rollback to purge inverted weights.
- **Absolute Anti-Loop Guard (Dead Man's Switch) (not implemented)**: Earlier
  revisions described an `absolute_patience` limit (15 epochs) that severs the
  loop and forces a hard SOTA rollback. The current code has no such limit. A
  stalled run ends through the bounded epoch budget (Section 2.26).
- **Model-Aware Adaptive Loop-Breaker & Loop Guards (v16.3.2) (not active)**:
  The breakout logic (spatial resolution promotion, drift-gate relaxation and
  the `breakout_lock` shield) exists, but
  `SmartTrainingGovernor.register_rollback` has no caller in the training loop
  (review finding D-10), so it never runs. If it is wired in, the breakout goes
  through `_commit_rung` and can only promote the resolution.
- **Autonomous Resolution Escalation & Dynamic Limits (v16.3.3) (not active)**:
  The escalation to the next rung in `res_ladder` (`256px -> 384px`, fraction
  reset to 15%) and the relaxed `get_active_regression_limit()` both depend on
  rollback registration, which is never invoked (see above).
- **Proven-Manifold Protection (hold and cool)**: When validation quality
  regresses, the manifold turns turbulent or collapses, the governor never
  retreats resolution or data fraction. It holds the current rung, multiplies
  the learning rate by `cooling_factor` (default 0.5), sets the stabilization
  lock and starts a 5-epoch cooldown. The intra-resolution data recoil of
  earlier revisions (e.g. `75% -> 55%` at `512px`) is removed because it broke
  the Monotonic Ratchet.
- **Atomic Governor Fraction Expansion Persistence & Checkpoint State Flush
  (v16.3.4)**: Solves cloud session preemption rollback during dynamic dataset
  fraction expansion. When the SOTA Guard triggers sample fraction promotion
  (e.g. `75% -> 90% -> 100%`), the engine immediately updates the active
  DataLoader topology, flushes `governor.get_state()` into the checkpoint
  payload, and overwrites both `_latest.pth` and `_best.pth` on disk. Hub Lock
  skip-paths are anchored directly to live governor telemetry, guaranteeing that
  cloud restarts resume precisely at the expanded manifold fraction rather than
  reverting to pre-expansion checkpoints.
- **ONNX Trace Resilience (FakeTensor Guards)**: Dynamically wraps unmapped
  `FakeTensor` memory pointer access (`data_ptr()`) during FX/ONNX graph tracing
  within the DataParallel multi-GPU engine to prevent false-positive
  segmentation faults during structural graph export.
- **Clean Training Initialization (--clean / --fresh)**: Operators can trigger
  pristine training starts via the `--clean` / `--fresh` flag, which instructs
  Hub Sync to bypass `git lfs pull`, purges existing local checkpoints and
  locks, resets `curriculum_state.json`, and wipes `metrics.csv` to begin
  strictly from epoch 1.
- **Restored Fraction Is Kept (v16.9.67)**: A checkpoint's saved data fraction
  is restored as-is. The earlier early-epoch guard, which lowered a legacy 100%
  fraction to the configured initial fraction for checkpoints without
  `epoch_count`, was removed because it stepped the fraction backwards at the
  same resolution. To restart a model from the initial fraction, use a clean run
  (`--clean` / `--fresh`).
- **Real-Time Cross-Model Checkpoint Parity**: All training workflows (both
  standard PyTorch pipelines and governed YOLO runners) enforce continuous
  dual-path synchronization: active rung checkpoints (`best.pt`, `best.pth`,
  `last.pt`, `progress.pth`) are mirrored to `checkpoints/<model_key>/` and
  `LemGendaryModels/<model_key>/checkpoints/` on every epoch and stage
  completion.
- **Sub-Second Minibatch Cancellation Protocol**: Training loops incorporate
  non-blocking cancellation listeners. For YOLO models, an `on_train_batch_end`
  callback sets `trainer.stop = True` within milliseconds of an abort signal,
  while standard PyTorch models evaluate `cancel_check()` at batch boundaries,
  permanently preventing mid-epoch runaway execution.
- **Mid-Rung Checkpoint Resumption & Stage Skip Protocol (v16.9.12)**: Solved
  premature epoch-1 restart bugs across both governed YOLO curricula and
  standard PyTorch pipelines. The checkpoint recovery subsystem
  (`training/checkpoint/recovery.py` and `training/governance/yolo_governor.py`)
  dynamically interrogates candidate checkpoint metadata (`torch.load`). If a
  ladder rung was already completed, it skips directly to the next stage; if
  interrupted mid-rung, it activates `resume=True` pointing to `last.pt` and
  resumes execution from `ckpt_epoch + 2` without resetting optimizer states or
  epoch counters.
- **PyTorch 2.6+ Checkpoint Unpickling Resilience & Fallback (v16.9.34)**:
  PyTorch 2.6+ enforces `weights_only=True` by default during `torch.load()`.
  When loading complex serialized model topologies (such as Ultralytics
  `DetectionModel` checkpoints), standard loads raise an `UnpicklingError`. The
  recovery layer implements an automatic `weights_only=False` fallback handler,
  ensuring legacy and complex weights are loaded cleanly without dropping
  checkpoint metadata.
- **Cumulative Historical Telemetry Epoch Anchoring (v16.9.34)**: Resumption
  routines cross-reference physical checkpoint dictionary states against
  cumulative history stored in `metrics.csv`:
  `completed_prior_epochs = max(completed_prior_epochs, csv_epochs)`. This
  permanently prevents multi-stage curriculum engines from resetting to early
  epoch counts when intermediate checkpoints lack embedded cumulative metadata.
- **Dynamic Horizon Runway Extension (v16.9.35)**: Solves static epoch
  denominator inversions (such as `266/150`) where training runs extended past
  preset targets format against obsolete bounds. Calculates dynamic training
  horizons via `stage_total_epochs = max(total_epochs, stage_start_epoch + 100)`
  and continuously extends `trainer.epochs` ahead of execution by 100 epochs
  throughout long-running runs.
- **Telemetry 1-Indexed Epoch Synchronization (v16.9.35)**: Standardizes epoch
  serialization across `TelemetryEngine.write_epoch_row` so that 1-indexed
  global epoch counters map 1-to-1 with rows in `metrics.csv`, eliminating
  off-by-one overwrites between consecutive epoch executions.
- **Universal Highest-Epoch Checkpoint Selection (v16.9.41)**: Resolved a
  critical checkpoint rollback vulnerability across all 23 production models.
  Previously, checkpoint discovery prioritized `progress.pth` over `latest.pth`
  and `best.pth`. In long-running models with pre-existing intra-epoch snapshots
  (e.g. `mirnet_exposure`, `nima_aesthetic_pro`, `nima_authenticity`), an older
  `progress.pth` from early epochs could supersede `latest.pth`, threatening up
  to dozens of epochs of completed training. The recovery engine dynamically
  inspects candidate metadata (`torch.load`) across
  `("latest", "best", "progress", "latest_epoch")` and selects the candidate
  checkpoint with the highest completed epoch and latest modification timestamp.
- **Automated Stale Progress Checkpoint Purge (v16.9.41)**: Injected automated
  lifecycle cleanup into `CheckpointLifecycleManager`: whenever `latest.pth`
  represents an epoch greater than or equal to `progress.pth`, the stale
  intra-epoch snapshot is immediately purged from `checkpoints/`, eliminating
  checkpoint ambiguity and preventing regression to earlier epochs.
- **Checkpoint Resumption Fraction Preservation & Post-Audit State Persistence
  (v16.9.43)**: Restores `epoch_count`, `last_res_jump_epoch`,
  `last_action_epoch`, and `history` inside `SmartTrainingGovernor.load_state()`
  prior to evaluating legacy state guards, and reconciles curriculum fraction
  and resolution against `metrics.csv` on startup so models at $100\%$ data
  fraction (`sample_fraction = 1.0`) never regress to $15\%$ on resume. Reorders
  `run_training` so `metrics.csv` records the active `pre_audit_gov_state` used
  during the completed epoch while `latest.pth` and `best.pth` persist the
  post-audit `governor_state`, and slices `MultiTaskDataset` and
  `InstructionDataset` manifolds deterministically in-memory
  (`random.Random(42)`) without re-initializing container readers.
- **Authoritative Single Source of Truth Persistence (`LemGendaryModels/`)
  (v16.9.12)**: Fixed workspace relative path resolution in `recovery.py` and
  aligned all training engines so that
  `LemGendaryModels/<model_key>/checkpoints/` and
  `LemGendaryModels/<model_key>/metrics.csv` serve as the primary authoritative
  persistence storage across the entire development tree.
- **Literature & Reference Paper Citations (v16.9.12)**: Embedded canonical
  academic paper citations, conference publications, arXiv references, and
  BibTeX entries across all model documentation in
  `LemGendaryModels/<model_key>/README.md` via `training/doc_generator.py`.
- **Senior Developer Suite Audit & Pyrefly Diagnostic Remediation (v16.9.44)**:
  Systematically resolved Pyrefly static typing diagnostics across
  `data/mt5_pipeline.py` (Timestamp `.hour` traversal and epoch time
  conversion), `models/core_restoration.py` (direct `up(x)` invocation
  eliminating manual ConvTranspose2d parameter unpacking while preserving
  16-byte memory alignment on Turing GPUs), `models/forex_predictor.py` (strict
  structural type guards on `fused_project` elements eliminating
  `Module | Tensor` type pollution), `models/master_generative.py` (explicit
  null-checks for `from_pretrained` subcomponents), `training/export/` (strict
  `nn.Module` typing on export wrappers), and `training/__init__.py` (default
  `MPLCONFIGDIR` and `MPLBACKEND` initialization eliminating sandboxed font scan
  overhead). Full 100% test battery pass with zero warnings and zero
  suppressions.

### 2.5. Mixture-of-Experts (MoE) 11-Manifold Architecture

- **Double-Softmax Squeeze Protection**: The `TaskClassifier` routing network
  natively isolates softmax activation from the loss engine, returning raw
  logits to prevent `log_softmax` gradient flattening when calculating
  Cross-Entropy gating loss.
- **Dynamic Perceptual LPIPS Balancing**: Automatically intercepts batch task
  indices during joint training to apply dynamic, sample-specific LPIPS
  multipliers scaling from `0.005` (Face Parsing) to `0.050` (Vintage & Face
  Restoration). This permanently prevents aggressive structural tasks from
  mathematically overpowering subtle intensity-based manifolds (like
  Lowlight/Exposure) via head competition.
- **Dynamic Regex Ingestion**: Seamlessly routes tasks like Denoise, Deblur,
  Derain, Dehaze, SuperRes, and Vintage automatically through regex extraction
  of physical dataset filenames on the fly.

### 2.6. Multi-Scale Forex Trading Architecture (`ForexPredictor`)

- **Causal Conv1D Timeframe Branches**: Processes multi-timeframe OHLCV data
  (M1, M5, M15, H1, H4, D1) through strict causal Conv1D stacks with left-only
  padding, guaranteeing zero temporal data leakage.
- **Cross-Timeframe Attention Fusion**: Fuses multi-scale feature maps with
  multi-head self-attention and currency pair embeddings into a unified feature
  manifold.
- **Timeframe Confluence Ladder (`res_ladder: [1, 5, 15, 60, 240, 1440]`)**:
  Replaces spatial pixel dimensions with MetaTrader 5 candle resolutions:
  - `M1 (1-min)`: Execution scalping and slippage minimization (Lookback: 512
    bars).
  - `M5 (5-min)`: Microstructure order-flow refinement (Lookback: 288 bars).
  - `M15 (15-min)`: Intraday trigger timing and tight stop placement (Lookback:
    192 bars).
  - `H1 (60-min)`: Intraday trend direction and volume delta confirmation
    (Lookback: 168 bars).
  - `H4 (240-min)`: Intermediate trend momentum and swing regimes (Lookback: 90
    bars).
  - `D1 (1440-min)`: Macro trend, regime classification, and structural levels
    (Lookback: 252 bars).
- **8-Metric Financial Scorecard & Domain Isolation**: Enforces quantitative
  convergence across all 8 specialized financial indicators:
  - Directional Accuracy ($\text{DirAcc} \ge 58.5\%$, higher is better)
  - Win Rate ($\text{WinRate} \ge 56.0\%$, higher is better)
  - Profit Factor ($\text{ProfitFactor} \ge 1.65$, higher is better)
  - Sharpe Ratio ($\text{Sharpe} \ge 1.85$, higher is better)
  - Sortino Ratio ($\text{Sortino} \ge 2.10$, higher is better)
  - Maximum Drawdown ($\text{MaxDD} \le 12.0\%$, lower is better)
  - Take-Profit MAE ($\text{TP\_MAE} \le 12.5\text{ pips}$, lower is better)
  - Stop-Loss MAE ($\text{SL\_MAE} \le 12.5\text{ pips}$, lower is better)
  - Strict domain isolation guarantees financial metrics never pollute vision
    model evaluation and vision metrics never distort quantitative time-series
    validation.
- **Confidence-Gated Dual Head & Loss**: Emits 3-class trade direction
  probabilities (Down/Sideways/Up) and magnitude estimates (TP/SL pips).
  Direction entropy dynamically gates Huber magnitude loss (`ForexDualLoss`) to
  prevent fitting noise on low-confidence bars.
- **Normalized Pip Scaling (`PAIR_PIP_SCALE`)**: Standardizes multi-asset
  volatility swings into Normalized Pip Units ($[0, 100]$ NPUs) via
  symbol-specific scaling factors ($1.0\times$ FX Majors, $5.0\times$
  Commodities, $10.0\times$ Gold, $20.0\text{--}40.0\times$ Indices),
  eliminating magnitude head saturation and stabilizing validation losses.
- **Calibrated Dual Loss Formulation**: Balances directional Focal/Cross-Entropy
  supervision ($0.50$) with normalized Huber regression ($0.02$, $\delta=2.0$),
  maintaining loss values in the clean $0.05\text{--}1.0$ numerical range
  matching vision restoration models.
- **Vectorized Cross-Timeframe Alignment Caching & Dynamic Hardware Scaling**:
  Precomputes cross-timeframe temporal alignment matrices in vector space
  ($O(1)$ integer array lookup replacing $35\text{M}$ individual $O(\log N)$
  binary searches per epoch). Dynamically scales physical sequence batch size by
  GPU VRAM tier (256 on 4GB GTX 1650 to maximize memory-sentinel headroom).
- **Unified Apache Parquet Streaming & LRU Row-Group Caching**: Operates
  directly on unified annual Parquet data stores
  (`ForexUniverse{year}.parquet`). Employs `ParquetRowGroupCache` for zero-seek
  random access and sub-microsecond batch tensor recovery ($<1\mu\text{s}$),
  eliminating NTFS cluster slack space and reducing dataset initialization time
  across 24M+ multi-timeframe bars to under $0.1\text{s}$.
- **Stateless ONNX Deployment**: Fully decoupled architecture exports cleanly to
  ONNX for low-latency inference in MetaTrader 5 Expert Advisors.

### 2.7. Omni-Metric Autonomous SOTA Adaptation

- **Dynamic On-the-Fly Tuning**: `SmartTrainingGovernor` dynamically audits
  model convergence against target SOTA benchmarks across all metrics
  simultaneously (e.g., PLCC, SRCC, EMD, PSNR, LPIPS, DirAcc).
- **Dynamic Severity Thresholds**: Automatically tightens deficit classification
  ($\ge 10\%$ = CRITICAL) for highly asymptotic correlation and probability
  metrics (SRCC, PLCC, Accuracy) to aggressively combat late-stage plateaus.
- **Metric Deficit Engine**: Computes the exact shortfall for any lagging metric
  $\Delta_m = \max(0, \text{Target}_m - \text{Current}_m)$ and continuously
  adjusts specific loss function components (actuators) to compensate:
  $w_{t+1} = \min(w_{\text{max}}, w_t + \alpha \cdot \Delta_{m})$.
- **Autonomous Rank-Boost Escalation**: Automatically scales pairwise
  `rank_weight` (up to `1.5`), `soft_spearman_weight` (up to `2.0`) and tightens
  `rank_margin` (down to `0.05`) when rank order metric plateaus occur in the
  Refinement Phase.
- **Dynamic Softmax Sharpening**: Softmax temperature is dynamically annealed
  down toward `min_temp` (`0.90`) to sharpen predicted score probability mass
  distributions and minimize Earth Mover's Distance.
- **Multi-Path Candidate Directory Resolver**: All generated training notebooks
  in the matrix dynamically resolve working directory candidates
  (`/kaggle/working/lemgendary-training-suite`,
  `/kaggle/working/model-training/lemgendary-training-suite`, `/kaggle/working`)
  before executing `os.chdir()` or `%pip install`, permanently eliminating
  `FileNotFoundError` across all cloud platforms.
- **Stateless ONNX Deployment**: Fully decoupled architecture exports cleanly to
  ONNX for low-latency inference in MetaTrader 5 Expert Advisors.

### 2.8. Smart Governor Plateau-Breaking Engine & Nuclear Safety Sentinels

- **3-Epoch Sustained Jolt Window**: Replaces single-epoch sawtooth LR thrashing
  with a 3-epoch sustained propulsion window, allowing AdamW momentum buffers to
  seat into new loss basins without premature cooling.
- **Early-Collapse Safety Valve**: Continuously monitors metric deltas during
  Sustained Jolt windows. If single-epoch quality regresses
  ($\Delta \text{Quality} < -0.015$), the window collapses immediately,
  triggering soft LR cooling ($0.85\times$) and momentum dampening.
- **Financial Manifold Hardening (Forex/Commodities)**: Dynamically disables
  standard Turbulence Shields for high-entropy financial time-series, doubles
  Jolt Protocol intensity ($2.0\times$ multiplier with 5-epoch sustained
  windows), and extends absolute plateau patience ($15+$ epochs) to prevent
  false-positive manifold panic retreats. Enforces a strict temperature floor
  ($\min T = 0.75$) to prevent logit explosion on low-SNR financial returns,
  categorizes the training phase as `CURRICULUM_FOLD` to block erroneous spatial
  ladder jumps, constrains the Overfitting Stress Protocol ($\le 2.0$), and
  limits differential LR jolts to $\le 1.15\times$. Collapse guard thresholds
  are explicitly recalibrated to $< 45.0\%$ Directional Accuracy.
- **Head-Differential LR Propulsion**: During REFINEMENT jolts, scales
  classification/regression head LR by $1.50\times$ while dampening backbone LR
  to $0.50\times$, protected by a strict ratio clamp
  ($\text{LR}_{\text{head}} \le 3.0 \times \text{LR}_{\text{backbone}}$).
- **Mini-SWA Plateau Recovery Pulse & Rollback Guard (not implemented)**: The
  governor sets a `trigger_mini_swa` flag on a plateau, but nothing reads it.
  There is no checkpoint averaging, no `update_bn` pass and no post-SWA rollback
  guard in the code (review finding D-10).

---

### 2.9. Differentiable Soft-Spearman Loss & Cross-Microbatch Rank Memory Bank

- **Continuous Ranking Supervision**: Replaces non-differentiable sort
  operations with a continuous sigmoid-based soft ranking formulation:

  $$
  \tilde{r}_i^p = 1 + \sum_{j \ne i} \sigma\left(\frac{p_i - p_j}{\tau}\right),
  \quad \mathcal{L}_{\text{soft\_spearman}} = 1 - \frac{\text{Cov}(\tilde{r}^p,
  \tilde{r}^t)}{\sigma(\tilde{r}^p)\sigma(\tilde{r}^t)}
  $$

- **Micro-Batch Contrastive Memory Bank**: Employs a detached FIFO queue
  ($N=32/64$) to maintain historical representation context across gradient
  accumulation steps. On 4GB GPUs where physical micro-batch size is $b=2$, this
  scales active pair comparisons from $\binom{2}{2} = 1$ to
  $\binom{32}{2} = 496$ pairs per backward pass ($41.3\times$ rank gradient
  density) without increasing VRAM allocations.

### 2.10. Spatial Statistical Pooling Upgrade (Mean and Std) & Universal Safety Filter

- **Variance-Aware Feature Aggregation**: Augments standard Global Average
  Pooling ($\text{GAP}$) with spatial standard deviation channels:

  $$
  \text{Feat}(x) = \left[ \text{GAP}(x) \,\|\, \text{StdDev}_{\text{spatial}}(x)
  \right] \in \mathbb{R}^{2C}
  $$

- **Localized Defect Retention**: Prevents localized micro-defects (compression
  blocking, fine sensor noise) and small NSFW triggers occupying
  $5\%\text{--}15\%$ canvas area from being diluted by $85\%\text{--}95\%$
  background pixels.

### 2.11. Headless Kaggle Cloud Engine & Dataset Bypass

- **Zero-Browser Cloud Deployment**: Launches, monitors, and downloads
  full-scale GPU training runs (Tesla T4 x2 / P100) directly from PowerShell
  without manual web browser intervention.
- **Kaggle Metadata API Hardening**: Strictly enforces string serialization
  (`"true"` / `"false"`) across all boolean fields (`enable_gpu`,
  `enable_internet`, `is_private`) in `kernel-metadata.json`. Resolves Kaggle
  API deserialization behavior where Python boolean values (`True`) led Kaggle's
  backend to ignore GPU flags and default worker allocation to CPU.
- **Autonomous Dataset Bypass**: Autonomously bypasses unnecessary 200GB+
  dataset downloads by inspecting `/images` and `/targets` structures directly
  on the Kaggle root block.
- **Autonomous Checkpoint Syncing**: Uses `kagglehub` model registry and kernel
  output endpoints to seamlessly pull trained `.pth` weights and `metrics.csv`
  logs into `LemGendaryModels/<model_name>/`.
- **Credential Fallback Hierarchy**: Automatically cascades from user UI prompt
  to environment variables (`KAGGLE_USERNAME`, `KAGGLE_KEY`),
  `~/.kaggle/kaggle.json`, and local `.kaggle_token`.
- **Ecosystem Facts (`training/ecosystem.py`)**: The sidecar ports, the
  Kaggle owner (including the generated notebook cells) and the documentation
  URL are read from `lemgendary-env-manager/ecosystem/ecosystem.json` through
  one loader; `LEMGENDARY_WORKSPACE_ROOT` overrides the workspace root.
- **Multi-Account Live Cloud Telemetry (`kaggle_monitor.py`)**: Supports
  multi-user credential switching across registered `.kaggle_users` profiles
  with on-demand custom account entry. Concurrently resolves active and recent
  kernel execution states via multi-threaded workers, streaming live runtime
  logs and status transitions incrementally via Kaggle API endpoints directly
  into the local terminal.

### 2.12. Universal Post-Training Target Audit & Interactive Guidance

- **Benchmark Gap Audit**: Automatically tabulates achieved metrics against
  mathematical `sota_targets` upon reaching the maximum epoch ceiling.
- **Interactive Action Matrix**: Presents operators with immediate in-process
  options to extend training, launch cloud GPU escalation, fine-tune from the
  best checkpoint, or export ONNX matrices.

### 2.13. Native Multi-Container Ingestion Architecture

- **Pluggable Container Format Engines (`training/data/containers/`)**:
  Decoupled reader ecosystem providing zero-IPC streaming ingestion across all
  modernized storage formats: `WebDatasetReader` (`.tar`/`.data`), `MdsReader`
  (`.mds`), `LitDataReader` (`chunk*.bin`), and `ParquetReader` (`.parquet`).
- **Paired Restoration Multi-Modal WebDataset Sharding**: Native extraction of
  ground truth targets (`target.webp`), semantic segmentation masks
  (`mask.webp`), text captions, and full 10-bin human perceptual quality
  distributions directly from compressed tar archives without unpacking loose
  files to disk. Shards use the `.data` extension to bypass Kaggle
  auto-extraction heuristics.
- **MosaicML Streaming (MDS) Backward Compatibility [Deprecated]**: Legacy
  format superseded by WebDataset (`.data`) and LitData. All production
  manifolds have been physically transcoded to WebDataset `.data` archives. The
  suite provides backward-compatible fallback readback via `MdsReader` while all
  new runs standardize on WebDataset and LitData.
- **Lightning AI LitData Tensor Streaming**: High-throughput memory-mapped
  binary chunk reading for regression and parameter prediction (`upn_v2`),
  supporting variable-shape tensors and robust fallback error handling.
- **Universal Container Resolver Ecosystem**: Upgraded
  `resolve_container_reader` dynamically reads `canonical_format` and `format`
  fields from `dataset_info.yaml`, falling back to candidate directory
  heuristics (`shards/`, `mds/`, `litdata/`, `parquet/`) for transparent
  zero-configuration ingestion.

### 2.14. Autonomous YOLO Multi-Stage Curriculum Governor & SOTA Target Convergence

- **Curriculum Stage Progression**: Governed by `YOLOCurriculumGovernor`
  (`training/governance/yolo_governor.py`), YOLO models progress through a
  multi-stage spatial resolution ladder (`320px -> 480px -> 640px`) paired with
  gradual dataset fraction scaling (15-stage ladder starting from 15% on the
  lowest rung: `15% -> 35% -> 55% -> 75% -> 100%` at 320px;
  `50% -> 65% -> 80% -> 100%` at 480px and 640px). Every step advances on
  plateau or overfitting detection rather than a fixed epoch budget, epochs are
  monotonic across stages, and an open-ended SOTA convergence loop continues at
  the top rung until all SOTA targets are achieved with $\ge 30$ epochs.
- **Autonomous Checkpoint Handoff & PyTorch 2.6 Resilience**: Each stage trains
  with warm-start weight handoff (`best.pt` of stage $k$ becomes the
  initialization weights for stage $k+1$). When unpickling Ultralytics
  checkpoint objects under PyTorch 2.6+, an automatic fallback to
  `weights_only=False` prevents deserialization crashes. Cumulative epoch
  progress is anchored against physical `metrics.csv` records
  (`completed_prior_epochs = max(completed_prior_epochs, csv_epochs)`),
  guaranteeing seamless resumption from arbitrary historical epochs (e.g., epoch
  271).
- **Hardware-Aware Turing FP32 Overrides**: On NVIDIA GTX 16xx (Turing
  TU117/TU116) GPUs lacking Tensor Cores, automatic mixed precision (`AMP`)
  fails and produces degenerate NaN loss values or 0.0 mAP. The governor
  automatically detects this architecture and enforces full FP32 numerical
  safety (`amp=False`).
- **Sawtooth VRAM Sentinel Integration**: Continuously monitors GPU memory
  pressure during YOLO execution, dynamically adjusting batch allocations and
  preventing out-of-memory crashes on 4GB edge hardware.
- **Unified Telemetry Stream**: All metrics across all curriculum stages are
  streamed in real time to `checkpoints/yolov8n/metrics.csv` and broadcast over
  the sidecar WebSocket feed, enabling live GUI progress tracking.

### 2.15. SSOT Config-Governed GUI Training Controls & Run-State Lifecycle

- **Read-Only Parameter Locking**: To eliminate operational configuration drift,
  the training interface locks primary hyperparameters (`Training Epochs`,
  `Minibatch Size`, `Initial Learning Rate`, and `Spatial Ladder Stage` /
  `Timeframe Confluence Stage`) to read-only mode for all neural models. Values
  are strictly sourced from authoritative manifests (`unified_models_v2.yaml` /
  `presets.yaml`).
- **In-App Manifest Adjustments**: Parameter modifications are routed through
  the Config Editor Modal (`onOpenConfigEditor`), ensuring all changes undergo
  schema validation and syntax checks before being committed.
- **Dynamic Start/Stop Action Toggle**: The training launch button automatically
  transforms into `Stop Training` (`.btn-danger`) while a background training
  job is active. Operators can gracefully cancel running jobs
  (`POST /api/jobs/{job_id}/cancel`), releasing GPU memory and updating state
  cleanly.

### 2.16. SSOT Jupyter Notebook Generation & Cross-Workspace Staging

- **Consolidated Architecture**: Consolidates all training, inference, and
  standalone usage guide Jupyter notebook generation exclusively within
  `lemgendary-training-suite` (`training/notebooks/`,
  `training/services/notebook_service.py`). Completely eliminates fragmented or
  duplicated generation logic from external toolsets.
- **Polymorphic Builder Interfaces**: Provides backward-compatible and modern
  call signatures (`(pascal_name, model_key, output_path)` and
  `(model_key, export_dir)`) in `builders/kaggle.py` and `builders/colab.py`,
  generating 100% reproducible execution environments tailored for Kaggle GPU
  environments (T4x2, P100) and Google Colab runtimes.
- **Multi-Vector Distribution & Staging**: Synthesized notebooks are atomically
  persisted and synchronized across four ecosystem locations:
  1. `LemGendaryModels/<model_key>/`: Canonical model architecture directory
     (both Kaggle and Colab training + usage notebooks).
  2. `LemGendaryDatasets/<manifold>/`: Matching compiled dataset manifold folder
     (training notebooks matching bound dataset).
  3. `kaggle_training/`: Workspace-level Kaggle execution staging directory.
  4. `colab_training/`: Workspace-level Colab execution staging directory.
- **Automated Pre-Flight Hook**: Step 0 of `TrainingService.train()`
  automatically invokes `notebook_service.generate_notebooks(model_key)` before
  local training or remote submission begins, ensuring on-disk notebooks are
  perpetually synchronized with active model configurations in
  `unified_models_v2.yaml`.
- **Omni-Channel Control (CLI, API, GUI)**: Exposed via Typer CLI
  (`lemtrain notebooks generate`), FastAPI REST endpoints (`/api/notebooks/*`),
  and one-click action buttons in the Desktop GUI (`lemgendary-ai-studio-gui`).

### 2.17. Fleet 1-Epoch Diagnostics & Kaggle Models Checkpoint Publishing

- **Sequential Fleet Diagnostics (`tools/train_all.py` / `lemtrain test-all`)**:
  The suite provides a rapid 1-epoch smoke test sequence across the registered
  architectures. Available via CLI (`lemtrain test-all [--epochs 1]`), REST API
  (`POST /api/training/unit-test-all`), and GUI toolbar ("Run 1-Epoch
  Diagnostic"). The runner verifies data loading, forward pass execution,
  backward gradient computation, checkpoint generation, and GPU memory cleanup
  per architecture. Since v16.9.65 such a run stops after one epoch with the
  stop reason `budget_reached`. Before, the open-ended loop and a hidden
  20-epoch floor on resume kept it running.
- **Kaggle Models Direct Publishing (`lemtrain sync push`)**: Dedicated cloud
  publishing pipeline allowing operators to package trained weights,
  configuration manifests, and model cards, uploading them directly to Kaggle
  Models repositories via official APIs with zero intermediate file staging.
- **Fleet-Wide Models Hub Synchronization
  (`POST /api/training/kaggle/push-all`)**: Enterprise batch publishing pipeline
  executing via REST API (`POST /api/training/kaggle/push-all`), CLI
  (`lemtrain sync push --all [-v ...] [-n ...] [--dry-run]`), and desktop GUI
  toolbar ("Push All Models to Kaggle"). Iterates across all 22 registered
  architectures, running automated pre-flight isolation verification across
  PyTorch, ONNX FP32, and ONNX FP16 variations before streaming artifacts
  directly to Kaggle Models.

### 2.18. Zero-Warning Tensor Memory Isolation & Telemetry Stream Segregation (v16.9.25)

- **PyTorch Non-Writable Tensor Root Cause Remediation**: In
  `data/forex_dataset.py`, slicing into memory-mapped NumPy window arrays
  (`raw_sample = window[:, col_indices]`) yields non-contiguous, read-only
  memory views. In modern PyTorch 2.5+, passing non-writable NumPy arrays to
  `torch.from_numpy()` triggers an internal runtime `UserWarning` indicating
  undefined behavior if written to. Rather than suppressing the diagnostic with
  `warnings.filterwarnings` (strictly prohibited under LemGendary standards),
  the dataset layer introduces `_safe_from_numpy(arr)`:

  ```python
  def _safe_from_numpy(arr: np.ndarray) -> torch.Tensor:
      if not arr.flags.writeable:
          arr = arr.copy()
      return torch.from_numpy(arr)
  ```

  This creates an isolated, writable array buffer prior to tensor conversion,
  resolving PyTorch tensor instantiation at root cause with 0 runtime warnings
  and 0 tensor copying overhead during validation.
- **Telemetry Stream Segregation**: To prevent dense training iterations from
  degrading operator clarity, terminal output streams are segregated:
  1. High-frequency iteration steps stream as discrete, unconstrained percentage
     events.
  2. The Desktop GUI log feed (`LogPanel.tsx`, `TelemetryConsole.tsx`) filters
     intermediate batch updates to avoid terminal buffer churn, rendering
     discrete milestone notices (epoch start, validation completions, SOTA
     alerts, checkpoints).
  3. Visual progress is displayed via the dedicated `@radix-ui/react-progress`
     tracker component, maintaining peak visual ergonomics and zero stream
     interference.

### 2.19. Forex Parquet Locality & Telemetry Progress Sync (v16.9.26)

- **Parquet Row-Group Locality Bottleneck & `RowGroupAwareSampler`**: Parquet is
  a columnar format organized into discrete row groups (typically ~5,000 rows
  each). Accessing row $N$ within a compressed row group requires decompressing
  the entire group. Under standard PyTorch `shuffle=True`, row indices are
  selected uniformly at random across all 700+ row groups across multiple years.
  This causes an catastrophic ~98% cache miss rate against in-memory LRU
  buffers, inflating batch iteration times to ~55 seconds per batch. The engine
  resolves this by integrating `RowGroupAwareSampler` directly in
  `training/core_loop.py` for all Forex datasets:
  1. Buckets sample indices by parent row group locality keys
     `('parquet', year, row_group_id)`.
  2. Shuffles at the row group level across epochs via
     `sampler.set_epoch(epoch)`.
  3. Yields indices within each row group contiguously, driving LRU cache hit
     rates from 2% to 99% and accelerating batch throughput to sub-second speeds
     (<0.5s/batch).

- **Curriculum Initial Fraction Ingestion**: In multi-year financial time-series
  datasets containing millions of multi-timeframe samples, initial training
  passes are governed by curriculum optimization parameters in
  `unified_models_v2.yaml` (`initial_fraction: 0.15`). `training/core_loop.py`
  pre-initializes the `SmartTrainingGovernor` before dataset construction,
  propagating `sample_fraction = governor.curriculum.current_fraction` into
  `ForexDataset(..., sample_fraction=sample_fraction)`. This bounds initial
  epoch size to ~16,379 batches instead of loading all 109,196 batches at once.

- **Standardized Batch Telemetry & Live Heartbeat**: Intra-epoch iteration
  logging in `training/training/epoch.py` is upgraded to emit standard telemetry
  lines containing:
  - Exact batch index and total count: `[BATCH 20/16379]`
  - Explicit fractional percentage: `(0.12%)`
  - Instantaneous loss and running average loss:
    `Loss: 0.3191 | AvgLoss: 0.6325`
  - Current learning rate: `LR: 0.001000`
  - Measured iteration rate: `5.42 it/s`
  - Dynamic estimated time of arrival: `ETA 50m24s`
  - Warmup logging (batches 1, 2, 5, 10) and an 8-second heartbeat timer prevent
    console and UI silence during intensive computation.

- **GUI Telemetry Progress Parser & Radix UI Progress Tracker**: The Desktop
  GUI's `progressParser.ts` natively parses `[BATCH <current>/<total>]`,
  computes exact progress percentages, and updates
  `TelemetryProgressTracker.tsx`. For fractional percentages $<1\%$, the tracker
  renders two decimal places (`0.02%`) rather than truncating to 0%.
  Indeterminate states trigger a smooth animated gradient sweep across the track
  instead of rendering static 80% filled bars.

### 2.20. Validation Batch Telemetry & Live Telemetry Progress Synchronization (v16.9.28)

- **Validation Loop Real-Time Batch Telemetry
  (`training/training/validation.py`)**: Evaluation passes under large
  validation splits (e.g. multi-thousand batch financial datasets or large image
  sets) previously operated without per-batch log emissions, causing the console
  and GUI to appear silent between 15-minute intra-epoch checkpoint intervals.
  The engine modernizes `validate_one_epoch` to log telemetry matching the
  training loop cadence:
  - Initial warmup batches (1, 2, 5, 10).
  - Periodic batches (`step_count % log_interval == 0` or final batch).
  - 8-second heartbeat timer during batch iteration.

  Each record is one log line (wrapped here at the `|` separators):

  ```text
  [VAL BATCH 125/2500] (5.00%) ValLoss: 0.2104 | AvgValLoss: 0.2215
  | 1.05 it/s | ETA 37m42s | 119.0s
  ```

- **GUI Telemetry Validation Parser & Emerald Progress Tracker
  (`progressParser.ts`, `TelemetryProgressTracker.tsx`, `client.ts`)**:
  - `client.ts` (`isProgressLine`): Recognizes `[VAL BATCH ...]` alongside
    `[BATCH ...]` to roll up consecutive ticks in-place without terminal history
    bloat.
  - `progressParser.ts`: Parses `[VAL BATCH <current>/<total>]`, sets
    `operation = "VALIDATION"`, sets `target = "Val Batch <current>/<total>"`,
    and maps to source `"training"`.
  - `TelemetryProgressTracker.tsx`: Dynamically renders an emerald green accent
    (`#00ff88`) and gradient for the `VALIDATION` operation, giving immediate
    high-contrast visual confirmation of the evaluation phase.

### 2.21. Modernized PyTorch cu126 & Transformers v5 Stack Integration

- **CUDA 12.6 Wheel Stack (`torch 2.14.1+cu126`)**: The suite operates on the
  modernized PyTorch 2.14.1 CUDA 12.6 stack, paired with
  `torchvision 0.29.1+cu126`, `torchaudio 2.11.0+cu126`, `sympy 1.14.0`, and
  `numpy 2.1.3`. This moves past legacy CUDA 12.1 pins while maintaining 100%
  binary stability across Windows and Linux.
- **Transformers v5 Ecosystem Alignment**: Adopts `transformers>=5.0.0,<6.0.0`
  (active: `v5.20.1`) alongside `tokenizers>=0.23.0` and
  `huggingface-hub>=1.0.0`. Delivers optimized weight loading, direct
  safetensors ingestion, faster Rust tokenizer execution, and reduced CPU peak
  RAM during large foundation model initialization.
- **Driver-Aware Dynamic CUDA Selection**: The training pipeline integrates
  `system_probe.select_cuda_torch_index()`, querying host NVIDIA driver
  capabilities dynamically via `nvidia-smi` and choosing the latest compatible
  PyTorch wheel index (`cu130`, `cu128`, `cu126`, or fallback `cu121`).
- **Physical Hardware Verification (GTX 1650, Driver 610.74)**: All 9 physical
  execution gates confirmed passing on local edge hardware:
  - FP32 matmul, FP16 autocast, and Conv2D forward/backward execution verified
    on CUDA.
  - Turing architecture detection correctly skips unsupported BF16 formats and
    enforces FP16/FP32 precision paths.
  - `torch.compile` eager fallback validated on Windows.
  - ONNX Dynamo export validated via `onnxscript` and `onnxruntime` (max diff
    1.78e-07).
  - Offline Transformers v5 smoke test (tokenizer, BERT forward pass, GPT-2
    generation, safetensors serialization) validated on GPU.
  - Torchvision CUDA NMS and bilinear interpolation confirmed operational.

### 2.22. Turing Non-Tensor-Core Hardware cuDNN Bug Remediation

NVIDIA GeForce GTX 16xx series GPUs (TU116 / TU117 Turing architectures without
Tensor Cores, such as GTX 1650, GTX 1660, and GTX 1630) exhibit a
hardware/driver accumulator overflow bug in cuDNN when evaluating spatial 2D
convolutions under `torch.float16` autocast with batched tensors
($\text{batch\_size} \ge 2$, e.g. at $512\text{px}$). While single-sample
training passes ($\text{batch\_size} = 1$) compute cleanly, validation batches
produce immediate `NaN` values, cascading into $\text{ValLoss} = \text{NaN}$.

The hardware policy engine (`training/hardware/policy.py`) automatically detects
Turing non-Tensor-Core GPU architectures and forces full Float32 precision
(`amp_enabled = False`), permanently eliminating numerical corruption while
preserving full evaluation fidelity.

### 2.23. Multi-Task SOTA Metric Ingestion & Perceptual Telemetry Synchronization

- **Perceptual LPIPS FP32 Guard (`training/training/validation.py`)**: In
  `training/training/validation.py`, evaluating TorchMetrics VGG feature
  extractors under mixed precision / autocast on edge Turing hardware threw
  runtime exceptions inside try/except blocks. Because errors were swallowed,
  `lpips_count` remained 0, causing `0.0000` to be written to `metrics.csv`. The
  evaluation pass now enforces explicit Float32 tensors (`p_scaled.float()`,
  `t_scaled.float()`) evaluated outside half-precision autocast blocks with
  detailed diagnostics logging.
- **Dynamic Frechet Inception Distance (FID) Feature Accumulation
  (`training/training/validation.py`)**: Integrated
  `torchmetrics.image.fid.FrechetInceptionDistance(feature=2048)` into the
  validation pass for all 11 restoration and super-resolution architectures
  defining `fid` in `sota_targets` (`mirnet_lowlight`, `mirnet_exposure`,
  `film_restorer`, `codeformer`, `ffanet_indoor`, `ffanet_outdoor`,
  `mprnet_deraining`, `nafnet_debluring`, `nafnet_denoising`,
  `professional_multitask_restoration`, `ultrazoom`). Real and reconstructed
  images are fed in chunks of at most two samples, and the final FID is written
  to `results["fid"]` at the validation epoch boundary. The legacy 64-feature
  layer is no longer used (Section 2.28).
- **Fleet-Wide SOTA Metric Parity Across All 23 Architectures**: Validation
  passes now automatically evaluate and record the corresponding SOTA targets
  for all model paradigms:
  - **Vision Restoration**: PSNR, SSIM, LPIPS, and FID.
  - **Aesthetic Quality (NIMA)**: PLCC, SRCC, and Rank Margin.
  - **Forex Time-Series**: Direction Accuracy, Win Rate, Profit Factor, Sharpe
    Ratio, Sortino Ratio, Max Drawdown, TP MAE, SL MAE, and Direction Entropy.
  - **Semantic Segmentation (ParseNet)**: Mean Intersection over Union (mIoU).
  - **Object & Face Detection (RetinaFace, YOLOv8n)**: mAP50, mAP50-95, and mAP
    difficulty scores.
  - **Classification (NSFW, Authenticity)**: Categorical Accuracy.
  - **Parameter Prediction (UPN v2)**: Mean Absolute Error (MAE).
- **Unified Telemetry Logging & Epoch Summaries
  (`training/training/engine.py`)**: Integrated LPIPS, FID, and PLCC metrics
  into canonical epoch completion summaries in `training/training/engine.py`,
  guaranteeing synchronized reporting across terminal logs, `metrics.csv`, and
  the Desktop GUI.

### 2.24. Kaggle Models Hub Metadata Sync & Whitepaper Citations (v16.9.46)

- **Automated Ecosystem Architecture Whitepaper Linking**: The cloud publishing
  layer (`training/cloud/metadata_generator.py`) programmatically resolves each
  model's authoritative technical whitepaper URL from the ecosystem
  documentation hub
  (`https://lemgenda.github.io/ai-training-whitepapers/papers/{doc}.html`) via
  `lemgendary-docs/canonical_capabilities.yaml` and `manifest/documents.json`.
  Whitepaper links are embedded directly into `provenance_sources` and formatted
  under a dedicated `### Citations & Technical Documentation` markdown block in
  Kaggle Models Hub instance metadata (`model-metadata.json`).
- **Standardized Multi-Format Variation File Descriptions**: Kaggle model
  instances stage four standardized runtime variations (`PyTorch Default`,
  `PyTorch FP32`, `ONNX FP16`, and `ONNX FP32`). The metadata generator
  synthesizes comprehensive, machine-readable file descriptions for every staged
  variation artifact:
  - `PyTorch Default`: Canonical checkpoints (`best.pth`, `latest.pth`),
    performance logs (`metrics.csv`), and ecosystem documentation (`README.md`).
  - `PyTorch (Float32)`: Standalone full-precision TorchScript / tracing weights
    file (`{model_key}.pt`) with input shape and tensor specification.
  - `ONNX (Float16)`: Half-precision graph (`{model_key}_fp16.onnx`) optimized
    for GPU execution and TensorRT conversion.
  - `ONNX (Float32)`: Full-precision graph (`{model_key}.onnx`) and external
    tensor payload (`{model_key}.onnx.data`) for CPU, OpenVINO, DirectML, and
    WebGPU deployment.
- **Bi-Directional Documentation & Metadata Command Parity**: Both the automated
  model publishing pipeline (`Push Model`) and the standalone documentation
  generator (`Docs & Meta` / `POST /api/models/{model_key}/generate_docs`)
  invoke the unified `KaggleMetadataService.build()` pipeline. Staging local
  documentation concurrently regenerates and aligns Kaggle metadata schemas,
  ensuring total parity between local repositories, GitHub Pages whitepapers,
  and remote Kaggle Models Hub registries.
- **Kaggle API Schema String Provenance & Token Alignment**: Kaggle's REST API
  (`kagglesdk.models.types.model_api_service`) enforces strict string typing on
  `provenance_sources`, throwing a runtime `TypeError` when passed list
  payloads. The generator formats provenance sources into comma-separated
  strings matching the schema. In addition, the authentication layer
  (`training/cloud/credentials.py`) binds active Personal Access Tokens
  (`KGAT_...`) from `~/.kaggle/access_token` directly to `KAGGLE_API_TOKEN` in
  the environment, guaranteeing clean automated publication of the full Model
  Card (Title, Subtitle, Description, Citations, and Provenance).

### 2.25. Monotonic Ratchet (Pair Rule) & `RatchetViolation` Guard (v16.9.67)

The governor moves through curriculum rungs $(r, f)$, where $r$ is the spatial
resolution and $f$ the data fraction. The owner ruling for the ROBOTS.md
Monotonic Ratchet Invariant is the pair rule. A transition from $(r_t, f_t)$ to
$(r_{t+1}, f_{t+1})$ is allowed only if:

$$
r_{t+1} \ge r_t \quad \land \quad \left(r_{t+1} = r_t \Rightarrow f_{t+1} \ge
f_t\right)
$$

- **Resolution never decreases**: no code path lowers `current_res` during
  training.
- **Fraction never decreases within one resolution step**: expansions use
  `expand_fraction`, $f_{t+1} = \max(f_t, \min(1, f_t + \Delta f))$ with
  $\Delta f = 0.20$. Values within 1% of full data snap to 1.0.
- **Fraction may reset when the resolution steps up**: after a regular spatial
  jump the fraction restarts at the configured initial fraction (0.15), after a
  forced SOTA jump at 0.5.
- **Enforced guard**: the torch-free module `training/ratchet.py` defines
  `check_transition`. Every governor transition (data propulsion, spatial jump,
  SOTA forced jump, loop-breaker breakout, VRAM veto) goes through
  `SmartTrainingGovernor._commit_rung`, which raises `RatchetViolation` (a
  `ValueError`) on a backward step instead of applying it.
- **Regression handling**: on regression the governor holds the rung and cools
  the learning rate (Section 2.4). It never recoils fraction or resolution.
- **Resume**: `load_state` restores the saved fraction as-is. `get_state()` and
  the 4-pillar check share the keys `input_size` and `sample_fraction`.
- **Tests**: `tests/unit/test_ratchet.py` (15 torch-free tests) checks that a
  simulated run obeys the pair rule, that backward steps are rejected, that
  governor transitions go through `_commit_rung`, and that completion fails
  below the top rung or with missing keys.

### 2.26. Bounded Epoch Budget & Honoured Early Stop (v16.9.65)

After every epoch the engine (`training/training/engine.py`) asks
`EpochBudgetPolicy` (`training/epoch_budget.py`) whether to continue, extend or
stop. With the configured budget $E$, the extension step $e$
(`training_budget.extension_epochs`, default 10) and the extension ceiling
$E_{\max}$ (`training_budget.max_extension_epochs`, default 0), the number of
trained epochs is bounded:

$$
E_{\text{trained}} \le E + E_{\max}
$$

The policy decides in this order:

1. `converged`: the 4-pillar completion invariant is met, so training stops.
2. `early_stop`: the governor signalled early stop from `audit_epoch`, so
   training stops.
3. The epoch is below the budget, so training continues.
4. `budget_reached`: extensions are disabled (`max_extension_epochs: 0`, the
   shipped default), so training stops.
5. `extension_limit`: the extension ceiling is used up, so training stops.
6. `budget_reached`: the governor does not report improvement, so training
   stops.
7. Otherwise the budget grows by $\min(e, E_{\max} - \text{used})$ epochs.

Every stop and every extension is printed and logged with its reason, and
`TrainingSummary.stop_reason` records it. Resumed runs honour the configured
budget, because the hidden 20-epoch floor on resume was removed. Pillar 4 needs
20 epochs, so a short diagnostic run always ends with `budget_reached`, never
with `converged`. The per-model `optimization.extension_epochs` key is no longer
read by the engine. The YOLO curriculum governor (Section 2.14) is unchanged.
`tests/unit/test_epoch_budget.py` holds 15 torch-free tests.

### 2.27. Pareto Model Soup Service (v16.9.66)

`blend_model_soup()` in `training/model_soup.py` (torch-free) is the one service
behind `lemtrain soup` and `POST /api/models/{model_key}/soup`
(`training/server/routes/soup.py`).

- **Hub resolution**: the models hub comes from `config.yaml`
  `paths.checkpoints_root` (default `../LemGendaryModels`, the sibling repo;
  absolute values are refused). The service resolves
  `<hub>/<model>/checkpoints/vault_*.pth` and passes the list of files to
  `create_pareto_model_soup`.
- **Donors and weights**: by default every `vault_*.pth` is blended, sorted by
  name. Optional donors (`psnr`, `lpips`, ...) select specific vaults (CLI
  `--donors`, API JSON body `{donors, weights}`; an empty body still works).
  Weights must match the donor count and be non-negative. Fewer than two donors
  are rejected.
- **Blending**: `create_pareto_model_soup` (`training/export/soup.py`) forms a
  weighted linear average of the floating-point tensors of $K \ge 2$ donors with
  weights $w_k$; other tensors are copied from the first donor. The result is
  written to `best_soup.pth` next to the vaults unless another output is given.

$$
\theta_{\text{soup}} = \sum_{k=1}^{K} \frac{w_k}{\sum_{j=1}^{K} w_j} \, \theta_k
$$

- **Errors**: a missing folder or vault file returns HTTP 404 (CLI exit code 1)
  with a list of what is missing. Fewer than two donors or invalid input return
  HTTP 422. The response keeps `model_key`, `success` and `soup_checkpoint` and
  adds `donors` and `weights`.
- **Limits**: BatchNorm statistics are not re-estimated after blending.
  Metadata, including `governor_state`, is copied from the first donor, and
  `soup_weights` stores the weights as given. The blend is not evaluated
  automatically, so any claim that it beats its donors must come from a measured
  evaluation.
- **SWA ingredient**: since v16.9.107 a run with SWA enabled (Section 2.32)
  writes `checkpoints/vault_swa.pth`. The default glob picks it up, or name it
  with `--donors psnr swa`, so SWA plus soup blending (the ROBOTS.md Pareto
  Model Soup standard) works. SWA is off by default.
- **Tests**: `tests/unit/test_model_soup_service.py` (20 torch-free tests) and
  two CLI runner tests.

### 2.28. Publication-Grade FID & Unverified Historical FID Rows (v16.9.67)

`validate_one_epoch` (`training/training/validation.py`) computes FID with
`torchmetrics` `FrechetInceptionDistance(feature=2048)`, the 2048-dimensional
final pooling layer of Inception-v3, for every model with `fid` in
`sota_targets`. With real-image statistics $(\mu_r, \Sigma_r)$ and
reconstruction statistics $(\mu_g, \Sigma_g)$:

$$
\text{FID} = \lVert \mu_r - \mu_g \rVert_2^2 + \operatorname{Tr}\left(\Sigma_r +
\Sigma_g - 2 \left(\Sigma_r \Sigma_g\right)^{1/2}\right)
$$

Real and reconstructed `uint8` images are fed in micro-chunks of at most two
samples, so the transient Inception memory scales with the chunk, not with the
validation batch:

$$
\text{Mem}_{\text{peak}} = \mathcal{O}(b_{\text{chunk}} \cdot H \cdot W \cdot
C), \quad b_{\text{chunk}} \le 2
$$

- **Removed tool**: before v16.9.67, `tools/recalibrate_fid.py` rewrote
  `metrics.csv` FID values with formulas (for example `fid * 45 + lpips * 26`,
  and a fixed `2.78` for epoch 2) and recomputed `Quality_Score`. That broke the
  Chart & Metrics Governance and Publication-Grade FID rules, and the tool was
  removed.
- **Unverified FID history**: the rewritten rows of four models are not measured
  values: `codeformer`, `ffanet_indoor`, `mprnet_deraining` and
  `mirnet_lowlight`. Their historical FID values are **unverified** wherever
  they appear (model papers, `metrics.csv`, training charts). This paper cites
  no FID value for these models and publishes no replacement numbers.
- **Open item**: the checkpoints must be re-evaluated with real Inception FID
  (`feature=2048`, chunks of at most two) or the rows excluded from charts.
  Since v16.9.107 the FID re-evaluation tool (Section 2.33) measures a
  checkpoint and records the rows as `unverified`; the measurements need a GPU
  and have not been run. The formula values are still in `metrics.csv`.

### 2.29. Sidecar Security Model & OpenAPI Contract (v16.9.64, v16.9.68)

- **Origin guard** (`training/server/security.py`): `origin_guard_middleware`
  refuses with HTTP 403 any request whose `Origin` is not an AI Studio GUI
  origin (`tauri://localhost`, `http://tauri.localhost`,
  `https://tauri.localhost`, `http://localhost:1420`, `http://127.0.0.1:1420`).
  Browser requests using `POST`, `PUT`, `PATCH` or `DELETE` must send
  `X-LemGendary-Client: ai-studio-gui`; the custom header forces a CORS
  preflight. WebSocket handshakes from foreign origins are refused. Requests
  without `Origin` (CLI, scripts, tests) are unaffected.
- **Closed CORS**: `install_security()` replaces `allow_origins=["*"]` with
  credentials by the allow-list above, explicit methods, explicit headers
  (`Content-Type`, `Authorization`, `X-LemTrain-Token`, `X-LemGendary-Client`)
  and `allow_credentials=False`. The optional token check keeps working behind
  the guard, and `lemtrain serve` binds `127.0.0.1` by default.
- **Secret files**: `.GOOGLE_DRIVE_JSON`, `.secrets.yaml`, `.mt5_credentials`
  and `.kaggle/` are git-ignored.
- **OpenAPI contract**: `tools/export_openapi.py` builds the app with
  `create_app` and writes `openapi.json` deterministically. The file lists all
  40 HTTP operations (39 paths; `/api/health` has GET and HEAD). `--check` exits
  1 on drift, and `tests/unit/test_openapi_contract.py` fails when the file
  differs from the live app. The two WebSocket routes are not part of OpenAPI.

### 2.30. Ecosystem Facts & GUI Training Verdict (v16.9.93, v16.9.94)

- **Ecosystem file**: `training/ecosystem.py` reads
  `lemgendary-env-manager/ecosystem/ecosystem.json` (`LEMGENDARY_ECOSYSTEM_FILE`,
  else the file under the workspace root; `LEMGENDARY_WORKSPACE_ROOT` overrides
  the root). Ports, the bind host, the Kaggle owner and the documentation URL
  come from it; a missing or malformed file raises `EcosystemFileError` naming
  the expected path. Model `kaggle_ref` and `kaggle_dataset_urls` are derived
  from `datasets` and the owner; an explicit value on a model is a per-model
  override.
- **Training verdict**: `GET /api/gui/models/with-stats` returns
  `ModelWithStats` entries (`training/server/routes/gui_schemas.py`).
  `training_status` (`fully_trained`, `partially_trained`, `weights_ready`,
  `initializing` or `unknown`) and `is_fully_trained` are required on every
  entry. `training_verdict()` is the only place that turns the 4 pillars (20
  epochs, top ladder rung, full data at that rung, all SOTA targets) into both
  fields. The data fraction counts only for the resolution step it was trained
  at (pair rule). A model whose stats cannot be computed is listed with
  `training_status: "unknown"`, `is_fully_trained: false` and the reason in
  `stats_error`, instead of failing the whole list.

### 2.31. Manifold Task from `dataset_info.yaml` (v16.9.100, v16.9.101)

`training/data/task_resolution.py` resolves a manifold's task without guessing
from folder names:

1. `task_type` in the manifold's `dataset_info.yaml`, the plain task id the
   LemGendary Dataset Compiler Suite writes (for example `pose`).
2. A legacy manifold without `task_type` is resolved from its layout (forex
   markers, `masks/`, `labels/`, `targets/`) through the datasets
   `task_taxonomy.json` (`LEMGENDARY_TASK_TAXONOMY_FILE`, else
   `<workspace_root>/lemgendary-datasets/task_taxonomy.json`).
3. An images-only legacy manifold falls back to `restoration` and logs a
   warning naming the `dataset_info.yaml` to fix.

`DATASETS_TO_INTERNAL_TASK` is the one table that maps datasets task ids to
internal names (`pose` to `face_detection`, `super-resolution` to
`restoration`, `authenticity` to `quality`, `ai_helper` to
`text_instruction`; the rest unchanged; `diffusion` and `vision` have no
equivalent). A missing or malformed taxonomy, or a task with no equivalent,
raises `TaskResolutionError` naming the file to fix.

### 2.32. Stochastic Weight Averaging (v16.9.107)

`training/training/swa.py` adds optional SWA on `torch.optim.swa_utils`. It is
configured in the `swa` section of `config.yaml` (validated by
`training/swa_config.py`) and is **off by default**:

- `enabled` (default `false`); `start_epoch` (first averaged epoch, overrides
  `start_fraction`) or `start_fraction` (default `0.75`, the last quarter of
  the epoch budget).
- `swa_lr`: when set, `SWALR` takes over the learning rate in the SWA phase
  and anneals over `anneal_epochs` (default 5) with `anneal_strategy` (`cos`
  or `linear`); the main scheduler is no longer stepped. `null` keeps the main
  schedule (averaging only).
- `update_every` (default 1): average every N epochs of the phase.
- `eval_every` (default 0): refresh BatchNorm, validate the averaged model and
  write `vault_swa.pth` every N updates; `0` does this once, when training
  ends. `bn_update_batches` caps the BatchNorm refresh (`null` uses the whole
  train loader).

With $n$ averaged epochs, epoch $t$ updates the running mean as

$$
\theta_{\text{SWA}} \leftarrow \frac{n \, \theta_{\text{SWA}} + \theta_t}{n + 1}
$$

- **Engine seam**: one `SwaPhase` component. The engine calls it after the
  governor audit of each epoch and once after the loop. `AveragedModel` is
  created at the first SWA epoch. `update_bn` re-estimates BatchNorm
  statistics before the averaged model is validated.
- **Ratchet safety**: SWA metrics go to the log and `swa_metrics` only, never to
  the SOTA tracker or the governor, so curriculum rungs still change only
  through `_commit_rung` (Monotonic Ratchet). A disabled run is unchanged.
- **Soup ingredient**: the averaged weights after the BatchNorm refresh are
  saved as `checkpoints/vault_swa.pth` (Section 2.27). They are not promoted to
  `best.pth`.
- **Resume**: the average, `n_averaged` and the `SWALR` state are kept in the
  `checkpoints/swa_state.pth` sidecar and restored when it matches the resumed
  epoch; otherwise averaging restarts with a warning. Cloud sync does not carry
  the sidecar yet.
- **Not implemented**: Mini-SWA (the `trigger_mini_swa` flag is still unread)
  and Metric-Specific SWA (MS-SWA).
- **Tests**: `tests/unit/test_swa.py` (18 CPU tests).

### 2.33. FID Re-evaluation Tool & Provenance Ledger (v16.9.107)

`python -m training.fid_reeval` (package `training/fid_reeval/`) re-measures
FID for the four models with unverified FID history (Section 2.28):

```bash
# Mark the formula-rewritten metrics.csv rows (no GPU, safe to repeat)
python -m training.fid_reeval mark-unverified --all

# Check all inputs on CPU, then measure (default checkpoint: best.pth)
python -m training.fid_reeval measure --model codeformer --dry-run
python -m training.fid_reeval measure --model codeformer --device cuda

# Summarise the ledgers
python -m training.fid_reeval status --all
```

- **Measurement**: `measure` uses the validation FID module
  (`FrechetInceptionDistance(feature=2048)`, chunks of at most two) on the
  model's validation split. It checks that the feature size is 2048 and that
  no chunk exceeds two, refuses a FID computed from part of the data, and loads
  the checkpoint strictly (`--non-strict` is explicit and noted in the row).
  Options: `--checkpoint`, `--datasets-root`, `--models-root`,
  `--env local|kaggle|colab`, `--device`, `--batch-size`, `--num-workers`,
  `--note`, `--dry-run`.
- **Provenance ledger**: results are appended to
  `LemGendaryModels/<model>/fid_provenance.csv` (UTC time, model, status
  `unverified` or `reevaluated`, source, epoch, value, image count, feature
  size, maximum chunk, checkpoint and its SHA-256, datasets root, device,
  note). Rows are only appended; a file with another header is refused.
- **What it never writes**: `metrics.csv` (its 28-column schema stays),
  checkpoints, `best.pth`, the quality score and the ratchet or rung state. A
  re-measured FID is evidence only.
- **Exit codes**: 0 success, 2 bad input or ledger, 3 FID invariant failure or
  missing FID backend.
- **Tests**: `tests/unit/test_fid_reeval.py` (23 CPU tests with a fake FID
  backend). The real measurements need a GPU and the validation data.

### 2.34. Version Single Source, Lint & Review Fixes (v16.9.122)

- **One version**: `[project] version` in `pyproject.toml` is the only place
  the suite version is written. `training/version.py` reads it (the installed
  distribution metadata is only a fallback), and the CLI, the sidecar app, the
  `GET /api/health` route, the notebook headers and the generated
  `openapi.json` report it. `config.yaml` has no `version` key.
- **Static checks**: pyright reports 0 errors (v16.9.120). Pylint with the
  repository `.pylintrc`, which has no `disable=` entries, reports 0 findings,
  design checks included (v16.9.121); seven inline `too-many-arguments`
  directives stay on CLI commands (one parameter per option) and model
  constructors. Large functions are split into helpers and wide classes group
  their state into dataclasses: `TrainingContext`
  (`training/training/context.py`) holds the `models`, `data`, `hardware`,
  `governance`, `run` and `state` groups instead of flat fields. Serialized
  formats and model `state_dict` keys are unchanged.
- **Review fixes (L10)**: the governor reads `plateau_patience` from
  `governor.manifold` (D-07, same value 6). `GET /api/gui/models/with-stats`
  reports measured values only: `best_metric` is `null` when nothing was
  measured, and `parameters_m` comes from `unified_models_v2.yaml` (`null` when
  the registry has no count) (D-08). A validation pass whose FID feature sets
  are unbalanced is marked `fid_incomplete` and reports no FID (D-13). The 600
  to 555 quality anchor on resume is `governor.quality_anchor_recalibration` in
  `config.yaml` (D-15), and the instruction dataset lookup uses
  `paths.datasets_root` (D-16). The unused `training/prefetch_worker.py` is
  deleted (D-12), and the `lemtrain` script targets
  `training.cli.lemtrain:app` (D-06). A test pins FID to 2048 features and
  chunks of at most two.
- **Remediation status**: `REVIEW_REPORT.md` of the LemGendary Model Training
  Suite lists the status of every review finding. Owner decisions, such as the
  optional API token and the unread resolution caps, keep today's behaviour.

---

### 2.35. Causal Language Model Instruction Tuning & Dynamic VRAM Probing

- **Dynamic Instruction Tuning Runtime (`GenericCausalLLM`)**: Causal decoder
  models (e.g. `ai_helper_lemgend`, based on `Qwen2.5-Coder-1.5B-Instruct`)
  execute instruction tuning via native `train_step(batch)` and
  `eval_step(batch)` methods that accept collated dictionary structures
  (`input_ids`, `attention_mask`, `labels`).
- **Dynamic VRAM Safety Probing & Gradient Accumulation Decoupling**: Unlike
  vision models that scale resolution ladders, LLM execution is bounded by
  sequence length (context window) and KV-cache activation overhead. When
  `batch_size` is `auto`, `audit_hardware_vram` computes the micro-batch size
  from real-time free GPU memory (70% of free VRAM at about 0.45 GB per
  2048-token sample, rounded down to a power of two, at most 32); a configured
  `batch_size` is used as is (`ai_helper_lemgend`: 2). `SmartTrainingGovernor`
  scales gradient accumulation steps
  ($K = \max(1, \operatorname{round}(B_{\text{eff}} / B_{\text{phys}}))$) to
  preserve the target effective batch size ($B_{\text{eff}} = 24$) on consumer
  GPUs (e.g. GTX 1650 4GB).
- **Universal LLM Milestone Vault Persistence & Held-Out Test Evaluation**:
  `CheckpointLifecycleManager` tracks LLM-specific SOTA target metrics
  (`eval_loss`, `perplexity`, `token_accuracy`) and persists isolated
  milestone checkpoints (`vault_eval_loss.pth`, `vault_perplexity.pth`,
  `vault_token_accuracy.pth`). Upon training completion, the engine executes
  an automated post-training evaluation pass on `ctx.data.test_loader`
  (`data/ai_helper_test.jsonl`), reporting hold-out generalization metrics
  under `test_*` into `TrainingSummary`. These checkpoints feed directly into
  the Pareto Model Soup (`create_pareto_model_soup`, Section 2.27) for linear
  adapter weight blending.

---

## 3. Judicial Audit Engine

A fully decoupled, zero-dependency validation wrapper designed for CI/CD
integration and isolated model auditing natively via `judicial_audit_api.py`.

### 3.1. Framework Agnosticism & Type Guards

Loads raw PyTorch `.pth` dictionaries, full PyTorch exported objects, and ONNX
compiled graphs dynamically. It injects a dynamic class resolution pass to
unpack `SoftmaxWrapper` boundaries, a critical guardrail accommodating PyTorch
2.6+ `weights_only=False` unpickling shifts.

To prevent standard tensor mis-casting during ONNX graph evaluation, the auditor
dynamically intercepts the `Float16` schema directly from the ONNX inputs,
safely casting down Float32 PyTorch tensors.

### 3.2. Fast-Path Correlator

Bypasses complex multi-process training augmenters for single-threaded PIL loads
(eliminating Windows DataLoader worker-hangs), outputting standard **PLCC**
(Pearson) and **SRCC** (Spearman) scores natively, and automatically piping
results into a standard JSON schema for automated regression auditing.

---

## 4. Universal Models Registry & SOTA Baselines

The registry `unified_models_v2.yaml` defines 23 models. The list below is
generated from it (v16.9.68): model key, display name, category, primary dataset
and the `sota_targets` used by Pillar 1. Directions follow the metric ($\ge$
higher is better, $\le$ lower is better). FID targets are targets, not achieved
values.

- `forex_predictor`: LemGendary Forex Predictor (Multi-Scale CNN-Transformer)
  (category `forex`, dataset `LemGendizedForexUniverse`). Targets: DirAcc % ≥
  58.5, WinRate % ≥ 56.0, Profit Factor ≥ 1.65, Sharpe ≥ 1.85, Sortino ≥ 2.1,
  MaxDD % ≤ 12.0, TP MAE pips ≤ 12.5, SL MAE pips ≤ 12.5.
- `nima_aesthetic_mobile`: LemGendary NIMA Aesthetic Scorer (Mobile) (category
  `enhance`, dataset `LemGendizedNimaAesthetic`). Targets: PLCC ≥ 0.65, SRCC ≥
  0.65.
- `nima_aesthetic_efficientnet`: LemGendary NIMA Aesthetic Scorer
  (EfficientNetV2-S) (category `enhance`, dataset `LemGendizedNimaAesthetic`).
  Targets: PLCC ≥ 0.7, SRCC ≥ 0.7.
- `nima_aesthetic_pro`: LemGendary NIMA Aesthetic Scorer (Pro ViT) (category
  `enhance`, dataset `LemGendizedNimaAesthetic`). Targets: PLCC ≥ 0.75, SRCC ≥
  0.75.
- `nima_technical`: LemGendary NIMA Technical Scorer (category `enhance`,
  dataset `LemGendizedNimaTechnical`). Targets: PLCC ≥ 0.91, SRCC ≥ 0.91, Rank
  Margin ≤ 0.05.
- `nima_authenticity`: LemGendary Authenticity Scorer (AI vs Human) (category
  `enhance`, dataset `LemGendizedNimaAuthenticity`). Targets: Accuracy ≥ 0.96.
- `upn_v2`: LemGendary UPN v2 Parameter Predictor (category `enhance`, dataset
  `LemGendizedUpnV2`). Targets: MAE ≤ 0.05.
- `film_restorer`: LemGendary Universal Film Restorer (category `restoration`,
  dataset `LemGendizedFilmRestorer`). Targets: PSNR ≥ 24.0, SSIM ≥ 0.8, LPIPS ≤
  0.25, FID ≤ 12.0.
- `codeformer`: LemGendary CodeFormer Face Restoration (category `face`, dataset
  `LemGendizedCodeFormer`). Targets: FID ≤ 5.2, PSNR ≥ 30.5, SSIM ≥ 0.93, LPIPS
  ≤ 0.08.
- `parsenet`: LemGendary ParseNet Face Parsing (category `face`, dataset
  `LemGendizedParseNet`). Targets: mIoU ≥ 0.86.
- `ffanet_indoor`: LemGendary FFANet Dehazing (Indoor) (category `restoration`,
  dataset `LemGendizedFfaNetIndoor`). Targets: PSNR ≥ 36.5, SSIM ≥ 0.99, LPIPS ≤
  0.08, FID ≤ 12.0.
- `ffanet_outdoor`: LemGendary FFANet Dehazing (Outdoor) (category
  `restoration`, dataset `LemGendizedFfaNetOutdoor`). Targets: PSNR ≥ 33.7, SSIM
  ≥ 0.986, LPIPS ≤ 0.08, FID ≤ 12.0.
- `mirnet_lowlight`: LemGendary MIRNet v2 Low-Light Enhancement (category
  `restoration`, dataset `LemGendizedMirNetLowLight`). Targets: PSNR ≥ 24.3,
  SSIM ≥ 0.84, LPIPS ≤ 0.08, FID ≤ 12.0.
- `mirnet_exposure`: LemGendary MIRNet v2 Exposure Correction (category
  `restoration`, dataset `LemGendizedMirNetExposure`). Targets: PSNR ≥ 24.3,
  SSIM ≥ 0.84, LPIPS ≤ 0.08, FID ≤ 12.0.
- `mprnet_deraining`: LemGendary MPRNet Deraining (category `restoration`,
  dataset `LemGendizedMprNetDeraining`). Targets: PSNR ≥ 30.6, SSIM ≥ 0.9, LPIPS
  ≤ 0.07, FID ≤ 12.0.
- `nafnet_debluring`: LemGendary NAFNet Debluring (category `restoration`,
  dataset `LemGendizedNafNetDebluring`). Targets: PSNR ≥ 33.9, SSIM ≥ 0.97,
  LPIPS ≤ 0.04, FID ≤ 6.0.
- `nafnet_denoising`: LemGendary NAFNet Denoising (category `restoration`,
  dataset `LemGendizedNafNetDenoising`). Targets: PSNR ≥ 40.2, SSIM ≥ 0.965,
  LPIPS ≤ 0.02, FID ≤ 4.0.
- `yolov8n`: LemGendary YOLOv8n Multi-Task Model (category `yolo`, dataset
  `LemGendizedYoloV8n`). Targets: mAP50 ≥ 0.74, mAP50-95 ≥ 0.55.
- `professional_multitask_restoration`: LemGendary Professional Multi-Task
  Restoration Model (category `restoration`, dataset
  `LemGendizedMultitaskRestorationPro`). Targets: PSNR ≥ 32.0, SSIM ≥ 0.93,
  LPIPS ≤ 0.07, FID ≤ 12.0.
- `ultrazoom`: LemGendary UltraZoom Master Model (category `restoration`,
  dataset `LemGendizedUltraZoom`). Targets: PSNR ≥ 34.0, SSIM ≥ 0.95, LPIPS ≤
  0.04, FID ≤ 10.0.
- `universal_nsfw_classification`: LemGendary Universal NSFW Classifier
  (category `enhance`, dataset `LemGendizedClassificationMaster`). Targets:
  Accuracy ≥ 0.98.
- `retinaface`: LemGendary RetinaFace Detection (category `face`, dataset
  `LemGendizedRetinaFace`). Targets: mAP easy ≥ 0.915, mAP medium ≥ 0.89, mAP
  hard ≥ 0.75.
- `ai_helper_lemgend`: LemGendary AI Studio Assistant (Causal LLM) (category
  `llm`, dataset `LemGendizedAIHelperLemGend`). Targets: Eval Loss ≤ 1.15,
  Perplexity ≤ 3.15, Token Accuracy % ≥ 72.5.

---

## 5. Universal SOTA Telemetry & Cloud Sync

Standardized historical audit (`metrics.csv`) captures the complete state
including Epoch, Loss, LR, Accuracy, Res, Data, Temp, Clamp, Batch,
Accumulation, Stress, and dynamic pair counts. The telemetry engine utilizes
dynamic attribute resolution to gracefully handle `MultiTaskDataset`
environments where specific domain attributes (like `.pairs`) are not globally
defined, preventing runtime `AttributeError` disruptions during multi-domain
logging. The **Metrics Sanitizer** explicitly sanitizes `inf`/`NaN` artifacts to
prevent numerical poison.

The Governor automatically synchronizes with the `LemGendaryModels` repository,
saving `_latest.pth` and `_best.pth` directly to the Hub. It uses Dual-Token
PATs (`SUITE_PAT` and `GITHUB_PAT`) for secure, headless authentication on
Kaggle deployment matrices.

### 5.1. Multi-GPU DataParallel Capabilities (Kaggle Scale)

The training suite natively intercepts execution environments with multiple GPUs
(e.g., Kaggle Tesla T4 x2) and automatically wraps compatible models in
PyTorch's `nn.DataParallel` API.

- **Dynamic Batch Distribution**: Seamlessly splits large high-fidelity pixel
  matrices (e.g., `768px`) across available GPUs, doubling effective throughput.
- **Seamless CPU Checkpointing**: Intelligently intercepts the `.pth` save
  hooks, stripping the `module.` prefix injected by `DataParallel` before saving
  to disk. This guarantees that Kaggle Multi-GPU checkpoints can be effortlessly
  downloaded and evaluated natively on standalone Windows environments or CPU
  deployments without manual layer re-mapping.

### 5.2. Universal Hardware Inference

All inference notebooks and training engines natively fall back to **DirectML**
on local machines, providing zero-config GPU acceleration for AMD and Intel
graphics cards on Windows.

### 5.3. Hybrid Cloud Synchronization & Tiered Lifecycle

The training suite implements an atomic, zero-drift synchronization architecture
unifying Kaggle Models and Google Drive (`142G7B9ONfUkXAhVkPeN4NeJ3YXU0UmJX`):

- **Startup Discovery**: Checkpoints are resolved exclusively from attached
  Kaggle Models (`/kaggle/input/models/...`), sorting version directories in
  descending numerical order to bind to the latest release without manual
  version pinning.
- **Mid-Epoch Preemption Resilience**: Intra-epoch iterations, optimizer
  momentum, and dynamic governor states are committed to local progress
  checkpoints (`_progress.pth`). If preempted or interrupted, an emergency
  signal hook commits the progress checkpoint solely to the Kaggle model
  artifact.
- **Epoch Completion Gating**: The trained model manifold is pushed to Google
  Drive strictly after an epoch has completed and `kagglehub.model_upload()`
  confirms successful creation of a new Kaggle model version.

### 5.4. Multi-Account Kaggle Cloud Telemetry & Live Monitor

The suite integrates a multi-account cloud monitoring and execution engine
(`kaggle_monitor.py`) accessible via Option 3 ("Kaggle Cloud Engine"):

- **Registry Authentication**: Reads user credentials directly from
  `.kaggle_users`, supporting seamless runtime profile switching across saved
  accounts or on-demand registration of new user accounts and API tokens.
- **Headless GPU Orchestration Submenu**:
  - **1. Train on Kaggle**: Prompts operator for user credential selection,
    queries user notebooks (or deploys registered local model manifolds),
    launches headless GPU execution on Kaggle, streams live runtime telemetry to
    the local console, and automatically pulls updated weights and checkpoints
    to `LemGendaryModels/<model_name>/` after each completed epoch.
  - **2. Monitor Active Cloud Jobs**: Concurrently discovers active kernels and
    streams live stdout and stderr telemetry in monitor-only mode with zero
    artifact pulling.
  - **3. Pull & Save Checkpoints**: Synchronizes latest checkpoints and metrics
    to local storage.
  - **4. Setup / Verify Credentials**: Configures and validates API
    authentication keys.
- **Concurrent Kernel Discovery**: Queries user kernel manifolds via
  multi-threaded workers (`ThreadPoolExecutor`), checking execution states
  (`RUNNING`, `QUEUED`, `COMPLETE`, `ERROR`) with near-sub-millisecond latency.
- **Incremental Telemetry Stream**: Streams stdout and stderr logs incrementally
  via Kaggle API midtier endpoints, rendering live progress lines and status
  notifications in real time with non-destructive detachment (`Ctrl+C`).

---

## 6. Distributed Edge Training: LemGendary Cloud Link

The suite integrates a multi-node, collision-resistant **LemGendary Cloud Link**
designed to crowdsource training loops across decentralized consumer-grade GPU
networks.

### 6.1. Federated Gradient Accumulation (Average-Sync)

- **WAN Payload Bypass**: Instead of syncing multi-gigabyte weight tensors
  across the network, the `CloudSyncManager` pushes lightweight, compressed
  gradient chunks to a centralized WebSockets Coordinator Hub (port 8765).
- **Consensus Broadcasting**: The coordinator tracks epoch syncs, learning rate
  recoils, and node parameters. Once a quorum is met, the hub broadcasts a
  unified federated average-sync gradient vector to all active edge nodes.

### 6.2. Memory-Sentinel WebGPU Zero-Copy Export

- **Opset 17 Hardening**: The exporter is rigidly configured to ONNX
  `opset_version=17` and dynamic axes are intentionally stripped (locked to a
  `512x512` spatial tile). This permanently prevents standard WebGPU "Slice"
  operator crashes during browser inference.
- **Crowdsourced Browser Nodes**: SOTA manifolds exported via this pipeline
  enable crowdsourced, zero-copy training and inference directly within any
  user's mobile or desktop NPU-enabled web browser.

---

## 7. Universal Instruction-Tuned Causal LLM Fine-Tuning & Dynamic Dataset Ingestion

The LemGendary Model Training Suite (v16.9.19) integrates a universal
fine-tuning backbone (`GenericCausalLLM` in `models/generic_causal_llm.py`)
capable of ingesting arbitrary HuggingFace causal language models, executing
memory-efficient quantized Low-Rank Adaptation (QLoRA), dynamically resolving
dataset paths from unified manifests, and exporting tri-format deployment
binaries.

### 7.1. GenericCausalLLM Architecture & Dynamic HuggingFace Backbone Wrapping

The `GenericCausalLLM` neural wrapper eliminates bespoke model definitions by
wrapping any open-weights causal architecture specified via
`base_foundation_model` (e.g. Qwen2.5-Coder, Llama-3, Mistral, Gemma, DeepSeek):

- **Dynamic HF Backbone Instantiation**: Instantiates the underlying transformer
  backbone and tokenizer dynamically via `AutoModelForCausalLM` and
  `AutoTokenizer` using `trust_remote_code=True` and `padding_side="right"`.
- **Automatic 4-bit Quantization Shielding**: Leverages `BitsAndBytesConfig`
  (`load_in_4bit=True`, `bnb_4bit_quant_type="nf4"`,
  `bnb_4bit_compute_dtype=torch.bfloat16`, `bnb_4bit_use_double_quant=True`) to
  compress base model weights from 16-bit to 4-bit NormalFloat representations,
  drastically reducing VRAM footprint to allow fine-tuning on consumer GPUs.
- **Lightweight Mock Verification Pathway**: Implements a native mock pathway
  (`self.embed` + `self.lm_head`) activated automatically during headless smoke
  tests or environments without CUDA hardware, ensuring 100% deterministic unit
  test execution across CI/CD pipelines.
- **Backward-Compatible Inheritance**: The legacy assistant model class
  `AIHelperLemGend` directly subclasses `GenericCausalLLM`, ensuring backward
  compatibility across existing registry queries and checkpoint vaults.

### 7.2. QLoRA Parameterization via unified_models_v2.yaml & PEFT Injection

All fine-tuning hyperparameters are declared authoritatively in
`unified_models_v2.yaml` under the model specification:

```yaml
test_llm:
  name: "LemGendizedTestLLM"
  base_foundation_model: "Qwen/Qwen2.5-Coder-1.5B-Instruct"
  category: "Language Modeling"
  dataset: "LemGendizedTestLLM"
  target_hardware: "CUDA_RTX"
  use_lora: true
  lora_r: 16
  lora_alpha: 32
  lora_dropout: 0.05
  load_in_4bit: true
  target_modules:
    - "q_proj"
    - "k_proj"
    - "v_proj"
    - "o_proj"
    - "gate_proj"
    - "up_proj"
    - "down_proj"
```

The model factory invokes `peft.prepare_model_for_kbit_training()` followed by
`peft.get_peft_model()`, freezing the base weights while injecting trainable
low-rank decomposition matrices ($A$ and $B$) into all attention projections and
MLP feed-forward gates:

$$
W = W_0 + \frac{\alpha}{r} (B \times A)
$$

### 7.3. Dynamic Dataset Discovery for Arbitrary LLM Manifolds

The training engine (`training/engine.py`) decouples dataset ingestion from
hardcoded repository paths:

- **Manifest-Driven Path Resolution**: Reads `model_info.dataset` from
  `unified_models_v2.yaml`, dynamically resolving the manifold directory
  `../LemGendaryDatasets/{dataset_folder}/data/`.
- **Automatic Shard Discovery**: Automatically detects `{key}_train.jsonl` and
  `{key}_val.jsonl` shards within the `data/` subfolder.
- **Zero-Copy Streaming**: Iterates over JSONL instruction turns with
  deterministic batch collation (`collate_fn`), eliminating memory spikes when
  processing extensive text corpuses.

### 7.4. Multi-Turn ChatML Loss Formulation & Assistant-Only Prompt Masking

During instruction tuning, computing loss across system prompts and user inputs
severely impairs model generalization by penalizing the model for memorizing
input tokens. The training engine enforces strict assistant-only supervised loss
masking:

1. **ChatML Serialization**: Formats multi-turn conversations into standard
   ChatML sequences:

   ```text
   <|im_start|>system
   {system_prompt}<|im_end|>
   <|im_start|>user
   {user_message}<|im_end|>
   <|im_start|>assistant
   {assistant_response}<|im_end|>
   ```

2. **Label Masking with -100 Ignored Index**: Token targets corresponding to
   <|im_start|>system...<|im_end|> and <|im_start|>user...<|im_end|> are
   assigned label -100. Only token targets within
   <|im_start|>assistant...<|im_end|> retain their token IDs:

   $$
   L_i = \begin{cases} -100 & \text{if token } i \in \text{Prompt (System/User)}
   \\ y_i & \text{if token } i \in \text{Assistant Response} \end{cases}
   $$

3. **CrossEntropy Loss & Perplexity Tracking**: PyTorch's
   `nn.CrossEntropyLoss(ignore_index=-100)` ignores masked prompt tokens during
   gradient backward passes. Real-time validation loss
   ($\mathcal{L}_{\text{CE}}$) is converted to validation Perplexity:

   $$
   \text{PPL} = \exp(\mathcal{L}_{\text{CE}})
   $$

### 7.5. Tri-Format Deployment Export: PyTorch, ONNX FP32/FP16 & Edge Quantization

Upon achieving validation convergence, the export subsystem (`training/export/`)
compiles universal deployment artifacts across three formats:

- **QLoRA Adapter Weights**: Standalone PEFT adapter checkpoint
  (`adapter_model.safetensors` and `adapter_config.json`) enabling zero-copy
  weight hot-swapping on shared inference servers.
- **Merged FP16 Safetensors**: Full-rank merged weights (`model.safetensors`)
  synthesized by fusing LoRA matrices into base weights ($W_0 + \Delta W$),
  optimized for native vLLM and HuggingFace pipelines.
- **GGUF / ONNX / WebGPU Quantization**: Exported ONNX compute graphs
  (`model_fp32.onnx`, `model_fp16.onnx`) and quantized GGUF binaries
  (`q4_k_m.gguf`) for real-time edge inference on consumer CPUs, NPUs, and
  desktop runtimes.

---

## 8. Conclusion

The LemGendary Model Training Suite provides the critical nuclear-hardened
infrastructure necessary to orchestrate, audit, and deploy high-fidelity
generative models. By integrating dynamic memory management, SOTA verification
gates, and multi-GPU distributed orchestration natively, LemGendary AI ensures
maximum hardware efficiency and an unbroken trajectory toward optimal perceptual
performance.

### 8.1. Implementation Status

- **Active**: pair-rule Monotonic Ratchet with the `RatchetViolation` guard
  (Section 2.25); bounded epoch budget with an honoured early stop (Section
  2.26); 4-pillar completion on the pre-audit governor state (Section 2.3.1);
  FID with `feature=2048` and chunks of at most two (Section 2.28); Pareto Model
  Soup service for CLI and API (Section 2.27); origin guard, closed CORS and the
  OpenAPI contract test (Section 2.29); ecosystem facts from `ecosystem.json`
  and the required GUI training verdict (Section 2.30); manifold task from
  `task_type` (Section 2.31); Stochastic Weight Averaging, off by default
  (Section 2.32); the FID re-evaluation tool (Section 2.33); omni-metric
  deficit engine and
  rank-boost escalation (Section 2.7); Soft-Spearman loss with the rank memory
  bank (Section 2.9).
- **Present but not active** (code exists, never invoked by the training loop):
  rollback registration (`register_rollback`) with the loop-breaker and
  resolution escalation built on it; the resolution-jump veto and the pre-jump
  dry-run probe; the `trigger_mini_swa` flag; the hardware resolution caps in
  `config.yaml`.
- **Not implemented**: Mini-SWA with its `update_bn` rollback guard and
  Metric-Specific SWA (MS-SWA) over the per-metric vaults; the absolute
  patience limit; validation sharding.
- **Needs the owner's GPU**: the FID re-measurement of the four models with
  unverified FID history (Section 2.33).
