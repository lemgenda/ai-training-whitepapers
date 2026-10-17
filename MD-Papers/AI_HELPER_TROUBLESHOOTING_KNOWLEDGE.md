# LemGendary AI Studio: AI Helper Troubleshooting Knowledge Base

> Structured diagnostics, historical failure modes, root-cause analyses, and mitigation playbooks for the LemGendary AI ecosystem.

**Hub Version**: `v16.9.27-STABLE`  
**Runtime Baseline**: `v16.9.16-STABLE`  
**Last Reviewed / Verified**: 2026-10-17  
**Status**: Canonical  

---

## 1. Diagnostic Schema & Epistemic Standards

Every troubleshooting scenario in this knowledge base conforms strictly to the canonical 3-stage diagnostic structure and 6-attribute diagnostic schema:

* **`symptom`**: The observable failure state, error message, or telemetry anomaly.
* **`context`**: Operational environment, active model architecture, dataset container, hardware footprint, and active resolution rung.
* **`Stage 1: Initial Triage (Safe Checks)`**: Safe, non-destructive checks based strictly on observable symptoms without modifying runtime configuration.
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**: Mechanistic hypotheses ranked by likelihood, accompanied by explicit requests for the missing telemetry needed to discriminate between candidate root causes.
* **`Stage 3: Bounded Remediation (Prerequisite-Checked Fixes)`**: Concrete, deterministic mitigations recommended only when telemetry evidence and prerequisite validation checks confirm the root cause.
* **`epistemic_status`**: Standardized certainty qualification: `[CONFIRMED]` (deterministic proof), `[PROBABLE]` (strongly supported by telemetry), or `[ILLUSTRATIVE]` (hypothesis requiring further empirical evidence).

---

## 2. AI-Helper Knowledge Contract & Conflict Resolution Protocol

To guarantee reliable assistant behavior, source attribution, and deterministic failure resolution, the AI Helper operates under four strict operational contracts:

### 2.1 Authority Hierarchy & Resolution Protocol

When resolving ambiguous or conflicting instructions, the AI Helper evaluates sources strictly in descending order of precedence:

1. **Tier 1 (Supreme Ground Truth)**: Active in-process code manifests (`unified_models_v2.yaml`, `unified_data.yaml`) and sidecar OpenAPI specifications (`http://127.0.0.1:8000/openapi.json`, `http://127.0.0.1:8100/openapi.json`, `http://127.0.0.1:8200/openapi.json`).
2. **Tier 2 (Operational Manuals)**: Master API Reference ([`MANUAL_API.md`](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/MANUAL_API.md)), Master CLI Manual ([`MANUAL_CLI.md`](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/MANUAL_CLI.md)), Desktop GUI Operator Manual ([`MANUAL_AI_STUDIO_GUI.md`](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/MANUAL_AI_STUDIO_GUI.md)), and Ecosystem Architecture ([`ECOSYSTEM_ARCHITECTURE.md`](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/ECOSYSTEM_ARCHITECTURE.md)).
3. **Tier 3 (Architectural Whitepapers)**: Model whitepapers (`PAPER_LEMGENDARY_*.md`, `PAPER_NIMA_*.md`).
4. **Tier 4 (Diagnostic Playbooks)**: Troubleshooting knowledge base (`AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md`).

### 2.2 Mandatory Citation Policy

The AI Helper must explicitly cite the authoritative document, section title, and specific file path for every technical recommendation or procedural claim.

### 2.3 3-Stage Diagnostic Intake Protocol

Before formulating targeted diagnostic hypotheses, the AI Helper must enforce the 3-stage protocol and request or verify the four mandatory telemetry points from the operator:

1. **Stage 1: Initial Triage**: Offer immediate, non-destructive safety checks (inspecting log files, reviewing process status, verifying filesystem paths) without modifying training configurations.
2. **Stage 2: Targeted Diagnosis**: Verify or request the missing telemetry points necessary to discriminate between candidate root causes:
   * **Model & Pipeline Context**: Active model key, spatial ladder stage, and dataset container format.
   * **Telemetry Logs**: Traces from `metrics.csv` or `telemetry.csv` (loss curves, gradient norms, dataloader wait times).
   * **VRAM Allocation**: Physical VRAM allocation metrics from `torch.cuda.mem_get_info()` or GUI telemetry stream.
   * **Invocation Parameters**: Exact CLI command line arguments or active GUI configuration toggles.
3. **Stage 3: Bounded Remediation**: Recommend concrete parameter, flag, or structural modifications only after evidence and prerequisites justify the change. All diagnoses must carry an epistemic tag: `[CONFIRMED]`, `[PROBABLE]`, or `[ILLUSTRATIVE]`.

### 2.4 Explicit Admission Bound

If a requested behavior, obscure failure state, or ungrounded option is not established by Tier 1-4 documentation, the AI Helper must explicitly respond: `"UNVERIFIED IN PUBLISHED HUB: The current documentation does not establish a single authoritative resolution for this state."` and prescribe running `lem-env audit` or querying active REST sidecars.

---

## 3. Core Diagnostic Scenarios

### Scenario 01: Low GPU Utilization and Dataloader Starvation `[PROBABLE]`

* **`symptom`**: GPU compute utilization fluctuates wildly between 10% and 35% with periodic zero-utilization troughs during restoration training.
* **`context`**:
  * Model: NAFNet Deblurring / MPRNet Restoration
  * Dataset: Sharded WebDataset (.tar archives containing WebP tiles)
  * Hardware: NVIDIA GeForce GTX 1650 (4GB VRAM), SATA SSD / HDD storage
  * Active Resolution: 384px or 512px
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Verify GPU temperature and clock throttling via nvidia-smi (confirm GPU is not thermal throttling below 55°C).
  2. Check whether the training process is currently active or stalled on background file operations.
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Check metrics.csv dataloader wait column and Host Task Manager Disk Queue depth.
  * **Ranked Candidate Causes**:
    1. Compressed WebP image decoding overhead in Python PIL workers (dataloader wait time > 250ms).
    2. Insufficient worker count (num_workers: 0 on disk-backed datasets).
    3. Disk I/O latency bottleneck caused by reading archives from rotational media.
* **`Stage 3: Bounded Remediation [PROBABLE]`**:
  * *Prerequisite*: Dataloader wait time confirmed > 200ms per iteration in metrics.csv.
  1. Set num_workers: 4 and enable pin_memory: true in dataloader configuration.
  2. Increase prefetch buffer factor to prefetch_factor: 2 in PyTorch DataLoader.
  3. If reading WebDataset from HDD, pre-compile shards onto NVMe SSD (--also-format webdataset).

---

### Scenario 02: NaN Instability in Mixed Precision (AMP FP16) `[CONFIRMED]`

* **`symptom`**: Training loss suddenly spikes to NaN or Inf within the first 50 iterations; GradScaler scale collapses to zero.
* **`context`**:
  * Model: NIMA Mobile (Aesthetic) / NIMA Technical
  * Loss Function: Earth Mover's Distance (EMD) Loss with CDF integration
  * Hardware: NVIDIA Turing Architecture (GTX 1650)
  * Precision: Automatic Mixed Precision (AMP) enabled (amp=True)
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Inspect last 5 lines of metrics.csv to confirm exact step where loss transitioned to NaN.
  2. Confirm whether weights in the last saved checkpoint remain valid or have been overwritten with NaNs.
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Check GradScaler scale factor history and confirm accelerator architecture (GTX 1650 TU117 lacks Tensor Cores).
  * **Ranked Candidate Causes**:
    1. Turing GTX 1650 FP16 half-precision underflows during Earth Mover's Distance cumulative distribution function (CDF) sums, causing square root of zero gradients to yield NaN.
* **`Stage 3: Bounded Remediation [CONFIRMED]`**:
  * *Prerequisite*: GTX 1650 hardware confirmed with EMD loss active.
  1. Set amp: false (force FP32 mode) for all Turing GTX 1650 configurations in unified_models_v2.yaml.
  2. Apply logit numerical clamping: torch.clamp(logits, min=-15.0, max=15.0) before computing softmax.
  3. Ensure emd_epsilon: 1e-4 is added inside the square root of the distance metric in losses/emd.py.

---

### Scenario 03: Scheduler Double-Stepping & Premature LR Decay `[PROBABLE]`

* **`symptom`**: Learning rate drops to minimum floor (eta_min) within 5 epochs despite a 100-epoch schedule.
* **`context`**:
  * Model: UltraZoom Super-Resolution / Hybrid UPN v2
  * Training Suite: Multi-stage curriculum with intra-fraction progression
  * Scheduler: CosineAnnealingLR combined with custom SawtoothGovernor
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Plot learning rate column in metrics.csv against epoch index.
  2. Inspect trainer logs to identify if scheduler.step() logs appear per batch or per epoch.
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Codebase inspection of trainer.py for invocation frequency of scheduler.step().
  * **Ranked Candidate Causes**:
    1. scheduler.step() called inside the inner batch loop instead of the outer epoch boundary.
    2. SawtoothGovernor advancing scheduler epoch counter prematurely during intra-fraction adjustments.
* **`Stage 3: Bounded Remediation [PROBABLE]`**:
  * *Prerequisite*: Confirm whether scheduler is epoch-based (CosineAnnealingLR) or step-based (OneCycleLR).
  1. Restrict scheduler.step() invocation strictly to epoch boundary for CosineAnnealingLR.
  2. Ensure SawtoothGovernor modifies learning rate multiplier directly without advancing the internal scheduler epoch counter.

---

### Scenario 04: Sentinel and Scheduler Desynchronization `[PROBABLE]`

* **`symptom`**: The Sawtooth Memory Sentinel reduces batch size during an OOM warning, but the learning rate remains scaled for the higher batch size, destabilizing gradients.
* **`context`**:
  * Model: YOLOv8n Object Detection / Forex Predictor
  * Feature: Dynamic Sawtooth Governor VRAM auto-scaling
  * Hardware: GTX 1650 (4GB VRAM) approaching 95% memory allocation
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Check telemetry.csv for sudden batch size cut events (e.g. 16 -> 8).
  2. Verify gradient norm behavior immediately following the batch size change.
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Inspect telemetry.csv for effective_batch_size vs learning_rate ratio and gradient accumulation steps.
  * **Ranked Candidate Causes**:
    1. Absence of linear learning rate scaling rule or failure to double gradient accumulation steps when physical batch size is halved.
* **`Stage 3: Bounded Remediation [PROBABLE]`**:
  * *Prerequisite*: Dynamic batch reduction event observed in telemetry.
  1. Implement automatic gradient accumulation doubling: when batch size is cut in half (16 -> 8), double gradient accumulation steps (1 -> 2).
  2. Maintain constant effective batch size: B_effective = B_physical * S_accum = constant.
  3. Flush CUDA cache immediately following down-scaling: torch.cuda.empty_cache().

---

### Scenario 05: Infinite Plateau Loop in Validation Governor `[PROBABLE]`

* **`symptom`**: Training enters an infinite loop where the learning rate decays to zero, early stopping triggers, but the governor endlessly restarts the epoch without checkpoint saving.
* **`context`**:
  * Model: NIMA Aesthetic Scorer (Mobile / EfficientNet)
  * Metric: Spearman Rank Correlation Coefficient (SRCC)
  * Feature: SOTA Adaptation Governor with Plateau Patience
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Check metrics.csv to verify if validation SRCC metric stagnates while epochs continue cycling.
  2. Confirm whether training is deadlocked or endlessly triggering jolt multipliers.
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Check optimization.plateau_patience and optimization.absolute_patience in unified_models_v2.yaml.
  * **Ranked Candidate Causes**:
    1. Lack of an absolute patience breaker (`absolute_patience`) or plateau patience configured without a hard epoch termination bound.
    2. Metric delta threshold (`min_delta: 0.001`) too small relative to statistical metric noise on small validation sets.
* **`Stage 3: Bounded Remediation [PROBABLE]`**:
  * *Prerequisite*: Verify `plateau_patience` is configured without an active `absolute_patience` guard in `unified_models_v2.yaml`.
  1. Enforce hard dead-man switch `absolute_patience: 15` in `unified_models_v2.yaml`. The Training Governor automatically halts execution and preserves the authoritative `best.pth` checkpoint if global SOTA is not surpassed within 15 consecutive epochs.
  2. Maintain validation set size for rank correlation metrics (SRCC/PLCC) at >= 500 samples as an empirical heuristic to prevent stochastic validation jitter from resetting patience counters.
  3. Implement learning rate jolt multiplier: `LR <- LR * 1.5` up to 2 times, followed by mandatory governor loop termination.

---

### Scenario 06: Pearson & Spearman Matrix Singularities `[CONFIRMED]`

* **`symptom`**: Correlation metric returns NaN during validation or loss backpropagation, halting the training process.
* **`context`**:
  * Model: NIMA Quality Assessment Suite
  * Loss / Metric: Differentiable Soft Spearman Rank or Pearson Linear Correlation (PLCC)
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Calculate standard deviation of model output batch: torch.std(predictions).
  2. Check if predictions collapsed to a uniform constant across the batch.
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Inspect prediction variance across samples in batch.
  * **Ranked Candidate Causes**:
    1. Mode collapse during early training iterations causing standard deviation sigma(y) = 0 and Pearson denominator sigma(y_pred) * sigma(y_true) = 0.
* **`Stage 3: Bounded Remediation [CONFIRMED]`**:
  * *Prerequisite*: Output batch variance confirmed near zero.
  1. Add numerical safety epsilon to standard deviation: sigma_safe = sqrt(Var(x) + 1e-8).
  2. In Soft Spearman loss, add tie-breaking noise during rank matrix inversion: predictions = predictions + 1e-6 * torch.randn_like(predictions).
  3. Pre-train with pure Earth Mover's Distance (EMD) loss for 5 epochs before introducing rank correlation objectives.

---

### Scenario 07: Power-Loss Resilience and Corrupted Checkpoint Recovery `[CONFIRMED]`

* **`symptom`**: System crashes or loses power during training; subsequent run crashes on launch with EOFError: Ran out of input or RuntimeError: PytorchStreamReader failed reading zip archive.
* **`context`**:
  * Model: Any of the 22 LemGendary architectures
  * File: best.pth or latest.pth
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Inspect file sizes of progress.pth, latest.pth, and best.pth in checkpoints/.
  2. Test checkpoint load in an isolated python shell: torch.load(path, map_location='cpu').
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Verify file integrity of primary and fallback checkpoints.
  * **Ranked Candidate Causes**:
    1. Non-atomic file write interrupted by power disruption, leaving a 0 KB or incomplete archive.
* **`Stage 3: Bounded Remediation [CONFIRMED]`**:
  * *Prerequisite*: latest.pth confirmed corrupted while progress.pth or best.pth is intact.
  1. Restore training from uncorrupted progress.pth (intra-epoch rolling checkpoint) or immutable best.pth.
  2. Enforce atomic write protocol: write to checkpoint.tmp.pth, flush and sync, then rename atomically to latest.pth (using resilient replacement with exponential backoff retry to prevent transient Windows OS Defender / Search Indexer file locks).

---

### Scenario 08: Runway Bloat During Spatial Resolution Escalation `[PROBABLE]`

* **`symptom`**: GPU runs out of memory (CUDA OOM) immediately when escalating from 320px to 480px or 640px along the resolution ladder.
* **`context`**:
  * Model: YOLOv8n / NAFNet / UltraZoom
  * Feature: Autonomous Spatial Resolution Ladder progression
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Confirm the exact rung boundary where OOM occurred (e.g. 320px -> 640px).
  2. Check torch.cuda.max_memory_allocated() before and after the ladder jump.
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Measure peak activation memory vs available VRAM at the new resolution.
  * **Ranked Candidate Causes**:
    1. PyTorch CUDA caching allocator fragmentation retaining unreleased activation buffers from the lower resolution rung, coupled with unscaled batch size.
* **`Stage 3: Bounded Remediation [PROBABLE]`**:
  * *Prerequisite*: Transition to higher spatial ladder rung confirmed.
  1. Explicitly downscale batch size according to first principles: B_r = floor(B_0 * (R_0 / R)^2).
  2. Execute explicit garbage collection and cache emptying at the rung transition: del optimizer_states, activation_cache; gc.collect(); torch.cuda.empty_cache().
  3. Re-initialize gradient scaler and data loader with new resolution tensors.

---

### Scenario 09: Hardlink vs. Perceptual Deduplication Conflicts `[PROBABLE]`

* **`symptom`**: Dataset compilation claims 0 duplicate images removed, but visual inspection shows hundreds of duplicate photos with minor JPEG re-compression.
* **`context`**:
  * Tool: LemGendary Dataset Compiler
  * Module: Deduplication Engine
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Review Dataset Compiler execution command flags used during compilation in compiler.log.
  2. Inspect raw source images to check if metadata or byte headers differ across visually identical images.
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Verify if --no-hash flag was passed or if hardlink deduplication was selected instead of perceptual hashing.
  * **Ranked Candidate Causes**:
    1. Hardlink deduplication checks byte-for-byte SHA-256 hashes on the same volume; re-compressed images possess different quantization tables and fail byte-level deduplication.
* **`Stage 3: Bounded Remediation [PROBABLE]`**:
  * *Prerequisite*: Dataset sourced from web crawl or multiple compressed archives.
  1. Re-compile manifold with default perceptual deduplication enabled (do NOT pass --no-hash).
  2. Reserve Hardlink Deduplication exclusively for local repository multi-directory caching where identical files reside on the same NTFS/ext4 volume.

---

### Scenario 10: Raw Dataset vs. Compiled Manifold Path Confusion `[CONFIRMED]`

* **`symptom`**: Training script aborts with FileNotFoundError: Manifest 'manifest.json' not found in path.
* **`context`**:
  * Tool: Training Suite CLI / GUI
  * Input: User specified raw download directory (e.g. raw_images/) as --dataset-path.
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Run ls or dir on the path provided to --dataset-path.
  2. Confirm whether manifest.json, shards/, or splits.json exist in that directory.
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Verify directory layout against LemGendary Manifold Specification.
  * **Ranked Candidate Causes**:
    1. User provided an uncompiled raw image directory directly to the training suite. The training suite strictly requires a compiled manifold containing manifest.json and pre-split shards.
* **`Stage 3: Bounded Remediation [CONFIRMED]`**:
  * *Prerequisite*: Directory lacks manifest.json.
  1. Execute Dataset Compiler first: python cli.py compile --model <model_key> --preset webdataset in lemgendary-datasets.
  2. Pass the compiled manifold directory path containing manifest.json to the training suite.

---

### Scenario 11: Ambiguous Loss Plateau & Validation Stagnation `[ILLUSTRATIVE]`

* **`symptom`**: Validation loss plateaus for 8 consecutive epochs without triggering early stopping or achieving target SOTA threshold.
* **`context`**:
  * Model: Hybrid MultiTask Restoration / NIMA Aesthetic
  * Epoch: Epoch 42 of 100
  * Observed Metric: Loss fluctuates within +/- 0.002 range
* **`Stage 1: Initial Triage (Safe Checks)`**:
  1. Review metrics.csv without modifying parameters or stopping the run.
  2. Confirm whether training loss is also plateauing or continuing to decrease (check for overfitting divergence).
* **`Stage 2: Targeted Diagnosis (Telemetry Verification)`**:
  * **Required Telemetry**: Do NOT prematurely alter learning rate or change optimizer settings. Request gradient L2 norms from the last 50 iterations, current spatial ladder rung, and validation sample size.
  * **Ranked Candidate Causes**:
    1. Evidence gathering is mandatory before selecting a remediation path: vanishing gradients vs overfitting vs validation subset noise.
* **`Stage 3: Bounded Remediation [ILLUSTRATIVE]`**:
  * *Prerequisite*: Action is conditioned on telemetry gathered in Stage 2.
  1. If gradient norm < 1e-4: Gradient vanishing diagnosed; adjust residual scaling or learning rate multiplier.
  2. If training loss is dropping while validation loss creeps up: Overfitting diagnosed; trigger Overfitting Rescue Protocol (force-expand dataset fraction by +15%).
  3. If validation subset is noisy: Auto-expand validation shard to 100% full dataset evaluation before declaring a false plateau.

---
