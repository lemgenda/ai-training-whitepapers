# LemGendary AI Studio: AI Helper Troubleshooting Knowledge Base

> Structured diagnostics, historical failure modes, root-cause analyses, and mitigation playbooks for the LemGendary AI ecosystem.

---

## 1. Diagnostic Schema Specification

Every troubleshooting scenario in this knowledge base conforms strictly to the following 6-attribute diagnostic schema:

* **`symptom`**: The observable failure state, error message, or telemetry anomaly.
* **`context`**: Operational environment, active model architecture, dataset container, hardware footprint, and active resolution rung.
* **`observations`**: Specific metric signals, log traces, hardware utilization patterns, and gradient telemetry.
* **`likely_causes`**: Mechanistic root-cause hypotheses ranked by likelihood.
* **`diagnostic_steps`**: Sequential procedural verification actions to isolate the root cause.
* **`recommended_action`**: Concrete, deterministic mitigation steps spanning configuration adjustments, CLI flags, or GUI controls.

---

## 2. Core Diagnostic Scenarios

### Scenario 01: Low GPU Utilization and Dataloader Starvation

* **`symptom`**: GPU compute utilization fluctuates wildly between 10% and 35% with periodic zero-utilization troughs during restoration training.
* **`context`**:
  * **Model**: NAFNet Deblurring / MPRNet Restoration
  * **Dataset**: Sharded WebDataset (`.tar` archives containing WebP tiles)
  * **Hardware**: NVIDIA GeForce GTX 1650 (4GB VRAM), SATA SSD / HDD storage
  * **Active Resolution**: 384px or 512px
* **`observations`**:
  * GPU temperature remains low (<55°C) and GPU memory is under-allocated.
  * System CPU utilization spikes on single core while training loop blocks on `get_batch()`.
  * Dataloader worker process wait times exceed 250ms per iteration.
* **`likely_causes`**:
  1. Compressed WebP image decoding overhead in Python PIL workers.
  2. Insufficient worker thread count or absence of pinned memory.
  3. Disk I/O bottleneck caused by reading from high-latency rotational drives.
* **`diagnostic_steps`**:
  1. Inspect dataloader latency in telemetry logs: `metrics.csv` dataloader wait column.
  2. Check host RAM cache and disk queue depth in Task Manager.
  3. Verify `num_workers` setting in `unified_models_v2.yaml`.
* **`recommended_action`**:
  1. Set `num_workers: 4` and enable `pin_memory: true` in dataloader initialization.
  2. If using WebDataset on HDD, pre-compile the manifold with `--storage uncompressed-tar` or migrate shards to NVMe SSD.
  3. Increase prefetch factor to `prefetch_factor: 2` in the PyTorch DataLoader.

---

### Scenario 02: NaN Instability in Mixed Precision (AMP FP16)

* **`symptom`**: Training loss suddenly spikes to `NaN` or `Inf` within the first 50 iterations; gradients zero out.
* **`context`**:
  * **Model**: NIMA Mobile (Aesthetic) / NIMA Technical
  * **Loss Function**: Earth Mover's Distance (EMD) Loss with CDF integration
  * **Hardware**: NVIDIA Turing Architecture (GTX 1650)
  * **Precision**: Automatic Mixed Precision (AMP) enabled (`amp=True`)
* **`observations`**:
  * Loss transitions from ~0.08 directly to `NaN`.
  * `GradScaler` scale factor drops exponentially: 65536 -> 32768 -> ... -> 1e-4.
  * Cumulative distribution function (CDF) calculation produces negative differences or unconstrained logits.
* **`likely_causes`**:
  1. Turing GTX 1650 lacks Tensor Cores and experiences numerical underflow in FP16 cumulative sums.
  2. Unclamped logits in softmax before Earth Mover's Distance computation.
  3. Division by zero in normalizer epsilon.
* **`diagnostic_steps`**:
  1. Inspect `loss_fn` implementation in `lemgendary-training-suite/losses/emd.py`.
  2. Check whether `amp=False` restores numerical stability.
  3. Verify logit clamping bounds in `unified_models_v2.yaml` under `stabilizers.logit_clamp`.
* **`recommended_action`**:
  1. Set `amp: false` (force FP32 mode) for all Turing GTX 1650 configurations.
  2. Apply numerical sentinel clamp: `torch.clamp(logits, min=-15.0, max=15.0)` before computing softmax.
  3. Ensure `emd_epsilon: 1e-4` is added inside the square root of the distance metric.

---

### Scenario 03: Scheduler Double-Stepping & Premature LR Decay

* **`symptom`**: Learning rate drops to minimum floor (`eta_min`) within 5 epochs despite a 100-epoch schedule.
* **`context`**:
  * **Model**: UltraZoom Super-Resolution / Hybrid UPN v2
  * **Training Suite**: Multi-stage curriculum with intra-fraction progression
  * **Scheduler**: `CosineAnnealingLR` combined with custom `SawtoothGovernor`
* **`observations`**:
  * LR decay occurs after every minibatch step instead of every epoch.
  * Telemetry displays learning rate stepping at $N \times B$ frequency rather than $N$.
  * Validation loss plateaus prematurely at high values.
* **`likely_causes`**:
  1. Scheduler `step()` called inside both the inner batch loop and outer epoch loop.
  2. Fractional ladder progression triggering premature epoch counter increments.
* **`diagnostic_steps`**:
  1. Search codebase for `scheduler.step()` calls in `trainer.py`.
  2. Check whether batch-level warmups are improperly wrapping epoch-level cosine decoders.
* **`recommended_action`**:
  1. Restrict `scheduler.step()` invocation strictly to epoch boundary: `if not is_batch_level: scheduler.step()`.
  2. When using `OneCycleLR`, step per batch; when using `CosineAnnealingLR`, step once per epoch after validation.
  3. Ensure `SawtoothGovernor` modifies learning rate multiplier directly without advancing the internal scheduler epoch counter.

---

### Scenario 04: Sentinel and Scheduler Desynchronization

* **`symptom`**: The Sawtooth Memory Sentinel reduces batch size during an OOM warning, but the learning rate remains scaled for the higher batch size, destabilizing gradients.
* **`context`**:
  * **Model**: YOLOv8n Object Detection / Forex Predictor
  * **Feature**: Dynamic Sawtooth Governor VRAM auto-scaling
  * **Hardware**: GTX 1650 (4GB VRAM) approaching 95% memory allocation
* **`observations`**:
  * Batch size dynamically cut from 16 to 8.
  * Gradient norm doubles immediately after batch size halving.
  * Loss diverges or oscillates uncontrollably.
* **`likely_causes`**:
  1. Absence of linear learning rate scaling rule (`lr_effective = lr_base * (batch_size / batch_base)`).
  2. Failure to synchronize gradient accumulation steps when batch size shrinks.
* **`diagnostic_steps`**:
  1. Inspect `telemetry.csv` for `effective_batch_size` vs `learning_rate` ratio.
  2. Verify whether `gradient_accumulation_steps` adjusted dynamically.
* **`recommended_action`**:
  1. Implement automatic gradient accumulation doubling: when batch size is cut in half ($16 \to 8$), double gradient accumulation steps ($1 \to 2$).
  2. Maintain constant effective batch size: $B_{\text{effective}} = B_{\text{physical}} \times S_{\text{accum}} = \text{constant}$.
  3. Flush CUDA cache immediately following down-scaling: `torch.cuda.empty_cache()`.

---

### Scenario 05: Infinite Plateau Loop in Validation Governor

* **`symptom`**: Training enters an infinite loop where the learning rate decays to zero, early stopping triggers, but the governor endlessly restarts the epoch without checkpoint saving.
* **`context`**:
  * **Model**: NIMA Aesthetic Scorer (Mobile / EfficientNet)
  * **Metric**: Spearman Rank Correlation Coefficient (SRCC)
  * **Feature**: SOTA Adaptation Governor with Plateau Patience
* **`observations`**:
  * Validation SRCC metric stagnates at ~0.612 for 15 consecutive evaluations.
  * `plateau_patience` counter hits threshold, triggers learning rate jolt, and resets counter without restoring `best.pth`.
* **`likely_causes`**:
  1. Lack of an absolute patience breaker (`absolute_patience`).
  2. Metric delta threshold (`min_delta: 0.001`) too small relative to statistical metric noise.
* **`diagnostic_steps`**:
  1. Check `optimization.plateau_patience` and `optimization.absolute_patience` in `unified_models_v2.yaml`.
  2. Inspect SRCC calculation on small validation batches where sample size $N < 100$ produces high variance.
* **`recommended_action`**:
  1. Enforce hard `absolute_patience: 15` in `unified_models_v2.yaml`. When exceeded, force-terminate training and restore `best.pth`.
  2. Ensure validation set size for SRCC is $\ge 500$ samples to ensure statistical significance.
  3. Implement learning rate jolt multiplier: $LR \leftarrow LR \times 1.5$ up to 2 times, followed by mandatory termination.

---

### Scenario 06: Pearson & Spearman Matrix Singularities

* **`symptom`**: Correlation metric returns `NaN` during validation or loss backpropagation, halting the training process.
* **`context`**:
  * **Model**: NIMA Quality Assessment Suite
  * **Loss / Metric**: Differentiable Soft Spearman Rank or Pearson Linear Correlation (PLCC)
* **`observations`**:
  * Model outputs collapse to identical uniform predictions across an entire batch (zero variance).
  * Standard deviation $\sigma(y) = 0$.
  * Pearson denominator $\sigma(y_{\text{pred}}) \times \sigma(y_{\text{true}}) = 0$.
* **`likely_causes`**:
  1. Mode collapse during early training iterations.
  2. Inverted rank sorting ties resulting in singular covariance matrices.
* **`diagnostic_steps`**:
  1. Calculate standard deviation of model output batch: `torch.std(predictions)`.
  2. Verify whether output variance is zero or below machine epsilon.
* **`recommended_action`**:
  1. Add numerical safety epsilon to standard deviation: $\sigma_{\text{safe}} = \sqrt{\text{Var}(x) + 10^{-8}}$.
  2. In Soft Spearman loss, add tie-breaking noise during rank matrix inversion: `predictions = predictions + 1e-6 * torch.randn_like(predictions)`.
  3. Pre-train with pure Earth Mover's Distance (EMD) loss for 5 epochs before introducing rank correlation objectives.

---

### Scenario 07: Power-Loss Resilience and Corrupted Checkpoint Recovery

* **`symptom`**: System crashes or loses power during training; subsequent run crashes on launch with `EOFError: Ran out of input` or `RuntimeError: PytorchStreamReader failed reading zip archive`.
* **`context`**:
  * **Model**: Any of the 22 LemGendary architectures
  * **File**: `best.pth` or `latest.pth`
* **`observations`**:
  * `latest.pth` file size is 0 KB or incomplete.
  * Direct load `torch.load('latest.pth')` fails.
* **`likely_causes`**:
  1. Non-atomic file write interrupted by power disruption or OS crash.
  2. Overwriting checkpoint file directly in place without writing to temporary buffer first.
* **`diagnostic_steps`**:
  1. Inspect file sizes of `progress.pth`, `latest.pth`, and `best.pth` in `checkpoints/`.
  2. Test checkpoint load in isolated python shell: `torch.load(path, map_location='cpu')`.
* **`recommended_action`**:
  1. Enforce atomic write protocol: write to `checkpoint.tmp.pth`, perform file flush and sync, then rename atomically to `latest.pth`.
  2. Check for `progress.pth` fallback: if `latest.pth` is corrupted, automatically restore from the 15-minute `progress.pth` buffer.
  3. Maintain permanent immutable `best.pth` separate from rolling `latest.pth`.

---

### Scenario 08: Runway Bloat During Spatial Resolution Escalation

* **`symptom`**: GPU runs out of memory (CUDA OOM) immediately when escalating from 320px to 480px or 640px along the resolution ladder.
* **`context`**:
  * **Model**: YOLOv8n / NAFNet / UltraZoom
  * **Feature**: Autonomous Spatial Resolution Ladder progression
* **`observations`**:
  * Peak memory footprint scales quadratically ($O(H \times W)$) or cubically with resolution.
  * Memory cached from 320px phase is not freed before allocating 640px tensors.
* **`likely_causes`**:
  1. PyTorch CUDA caching allocator fragmentation retaining unreleased activation buffers.
  2. Failure to down-scale minibatch size upon spatial ladder rung escalation.
* **`diagnostic_steps`**:
  1. Measure peak memory before and after resolution rung change: `torch.cuda.max_memory_allocated()`.
  2. Check whether batch size was reduced according to first-principles formula: $B_{r} = \lfloor B_0 \times (R_0 / R)^2 \rfloor$.
* **`recommended_action`**:
  1. Explicitly reduce batch size: $640\text{px} \implies B=8$ (from $B=16$ at $320\text{px}$).
  2. Execute explicit garbage collection and cache emptying at the rung transition:

     ```python
     del optimizer_states, activation_cache
     gc.collect()
     torch.cuda.empty_cache()
     ```

  3. Re-initialize gradient scaler and data loader with new resolution tensors.

---

### Scenario 09: Hardlink vs. Perceptual Deduplication Conflicts

* **`symptom`**: Dataset compilation claims 0 duplicate images removed, but visual inspection shows hundreds of duplicate photos with minor JPEG re-compression.
* **`context`**:
  * **Tool**: LemGendary Dataset Compiler
  * **Module**: Deduplication Engine
* **`observations`**:
  * Hardlink inode deduplication finds zero matches because byte hashes (SHA-256) differ due to distinct JPEG metadata/quantization tables.
* **`likely_causes`**:
  1. User selected `Hardlink Deduplication` instead of `Perceptual Deduplication (pHash)`.
  2. Hardlink deduplication only identifies byte-for-byte identical files on the same filesystem.
* **`diagnostic_steps`**:
  1. Inspect compile command options: check whether `--dedup hardlink` or `--dedup phash` was passed.
  2. Compute perceptual hash distance between suspected image duplicates.
* **`recommended_action`**:
  1. For visual datasets sourced from web crawls or multiple archives, select **Perceptual Deduplication** (`--dedup phash --phash-threshold 4`).
  2. Reserve **Hardlink Deduplication** exclusively for local repository multi-directory caching where identical files reside on the same NTFS/ext4 volume.

---

### Scenario 10: Raw Dataset vs. Compiled Manifold Path Confusion

* **`symptom`**: Training script aborts with `FileNotFoundError: Manifest 'manifest.json' not found in path`.
* **`context`**:
  * **Tool**: Training Suite CLI / GUI
  * **Input**: User specified raw download directory (e.g. `raw_images/`) as `--dataset-path`.
* **`observations`**:
  * Directory contains loose `.jpg` and `.png` files without shard archives (`.tar`) or index manifest (`manifest.json`).
* **`likely_causes`**:
  1. User provided a raw source dataset directory directly to the training suite instead of a compiled manifold.
  2. Training suite requires standardized manifold architecture with pre-split shards, validation subsets, and schema declarations.
* **`diagnostic_steps`**:
  1. Check contents of `--dataset-path`: look for `manifest.json`, `shards/`, or `splits.json`.
  2. Verify if Dataset Compiler was executed on the raw folder.
* **`recommended_action`**:
  1. Execute Dataset Compiler first:

     ```bash
     lem-env datasets compile --input ./raw_images --output ./LemGendaryDatasets/MyCompiledManifold --preset webdataset
     ```

  2. Point the training suite directly to the compiled manifold output directory.
