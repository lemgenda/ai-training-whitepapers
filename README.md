# LemGendary AI Documentation Hub

> Authoritative technical whitepapers, architectural manuals, API references,
> CLI guides, and visual demonstrations for the LemGendary AI ecosystem.

**Version**: `v16.9.116`

---

## Hub Features

* **48 publications** - Markdown sources in `MD-Papers/` paired 1-to-1 with
  HTML pages in `papers/`, catalogued in `manifest/documents.json`.
* **Capability registry** - `canonical_capabilities.json` and its YAML twin
  (kept identical) list the 23 registered models with registry categories,
  CLI commands (`lemtrain train MODEL_KEY`), API routes
  (`POST /api/training/train`) and GUI control IDs, plus the platform
  capabilities: Bug Report Tool (`POST /api/bug-report`, screen recording in
  the desktop app on Windows), the sidecar security contract (Origin Guard and
  Client Header), Pareto Model Soup, the Ecosystem Registry, Stochastic Weight
  Averaging, the FID Re-evaluation Tool, shard-window sampling, Kaggle Cloud
  Training and Frozen Run Settings.
* **Current baselines** - LemGendary Environment Manager v16.9.85, LemGendary
  Dataset Compiler Suite v16.9.109, LemGendary Model Training Suite v16.9.223,
  LemGendary AI Studio GUI v2.10.68.
* **Glossary and current state** - canonical terms (including Bug Report
  Archive, Telemetry CSV, Origin Guard, Ratchet Violation and Epoch Budget) and
  the verified workspace state with the versioning matrix.
* **Approved HTML template** - synchronized pages use `header`,
  `nav.toc-sidebar`, `section` and `footer` and pass W3C validation.
* **Documentation audit** - `python scripts/audit_docs.py` (also the
  pre-commit hook) checks the manifest, hub and document versions, MD/HTML
  heading parity and text similarity, the HTML sidebar against the Markdown
  table of contents (no duplicate entries, every section linked), raw GitHub
  alert markers in pages, the approved template, internal links and anchors,
  absolute paths and canonical names, and the capability registry against
  the sibling repositories: JSON and YAML hold the same data, the model ids
  equal the keys of the training registry (`unified_models_v2.yaml`), every
  port equals the service port in
  `lemgendary-env-manager/ecosystem/ecosystem.json` and every component
  baseline equals the release version the component declares. The sibling
  files are found next to this repository or under
  `LEMGENDARY_WORKSPACE_ROOT`; a missing file is a finding that names the
  path. The parity backlog (`scripts/parity_backlog.json`) is empty: every
  finding fails the audit.

---

## Directory Overview

* **`papers/`** — W3C-compliant standalone HTML versions of all 48 technical
  whitepapers, manuals, and architectural specifications.
* **`MD-Papers/`** — Markdown sources synchronized 1-to-1 with the HTML
  publications, formatted to strict markdownlint compliance.
* **`assets/`** — Static imagery, training loss curves, architectural
  flowcharts, and before/after perceptual visual demonstrations.
* **`manifest/`** — Machine-readable document catalog pairing all 48
  publications 1-to-1 with Markdown companions.
* **`tests/`** — Automated documentation verification test suite enforcing
  formatting, structure, and integrity gates.
* **`scripts/`** — Documentation audit (`audit_docs.py`, `docs_audit/`) and the
  known parity backlog (`parity_backlog.json`).
* **`index.html`** — Central documentation catalog and entry portal.

### v16.9.225 - Pre-Baked WebDataset Indexing & Cloud Training Pathologies

* **Pathology 64 & 65**: Documented dual-GPU PCIe barrier overhead on lightweight
  parameter predictors and 0-byte WebDataset member fallback / shard index latency.
* **Dataset Compiler & UPN v2**: Documented pre-baked `shard_offsets.json` v2
  generation for 0.0s startup resolution and WebP-only container purity.
* **Training Suite**: Documented Single-GPU T4 affinity governance and
  SOTA-driven `ALL_VARIATIONS` auto-sync to Kaggle Model Hub.

### v16.9.116 - Sync Push Notes, Export Run Log Lines, Forex Layout

* `MANUAL_CLI.md` and its page, Section 5.10: Dataset Compiler v16.9.109
  `sync push --notes TEXT` adds what changed after the generated version
  notes (compiler release and sample counts); whitespace is collapsed and
  blank text adds nothing. The registries gain
  `control_planes.cli.syntax.dataset_sync_push`; `PAPER_DATASET_COMPILER.md`
  Section 4.12 notes it.
* `PAPER_TRAINING_SUITE.md` and its page, Section 2.47 (now v16.9.216 to
  v16.9.223, version line v16.9.223): the export prints the ONNX FP32 parity
  probe result (or "not run" for a graph without dynamic axes) and the
  release files it wrote to the run log, because the trainer has no INFO log
  handler. Run 6 of `upn_v2` confirmed the v16.9.222 CPU probe; parity
  measured locally: FP32 max abs diff 4.17e-7 at `1x3x128x128`, FP16
  4.51e-3 / 6.64e-3 (the FP16 graph has no in-run probe). The mid-run Hub
  sync uploads only `pytorch/default`; ONNX variations go up with the
  release publish after training completes.
* `PAPER_DATASET_COMPILER.md` and its page, Section 7
  `LemGendizedForexUniverse`: the 765 "chunks" are `index.json` entries (one
  per pair, timeframe and year; 573 train, 192 val), not files; storage is
  eight yearly Zstandard Parquet files with 5,368 row groups.
* Baselines: Training Suite v16.9.223, Dataset Compiler v16.9.109,
  Environment Manager v16.9.85, AI Studio GUI v2.10.68.

### v16.9.115 - ForexUniverse Sample Count

* `PAPER_DATASET_COMPILER.md` and its page, Section 7
  `LemGendizedForexUniverse`: Total Samples 26,818,700 (train 21,015,570 /
  val 5,803,130; 765 chunks), was 24,850,000. The count is the dataset's
  `dataset_info.yaml` on Kaggle, the sum of its `index.json`, and the
  training registry (Training Suite v16.9.221 checked it); the Forex paper
  already stated 26,818,700.

### v16.9.114 - Measured Model Parameter Counts

* Training Suite v16.9.221 measures `parameters_m` in
  `unified_models_v2.yaml` from the code. The papers now state those counts
  (old value, then measured, in millions):
  * `PAPER_FOREX_PREDICTOR.md` Section 4.1 and `MANUAL_AI_STUDIO_GUI.md`
    (model card example): `forex_predictor` 2.75 to 3.5358 (about 14 MB in
    FP32, was about 11 MB).
  * `PAPER_NIMA_MOBILE.md`: MobileNetV3-Small model 2.5 to 1.0773.
  * `PAPER_NIMA_EFFICIENTNET.md`: EfficientNetV2-S model 21.5 to 20.508.
  * `PAPER_NIMA_PRO.md`: Swin-v2-T model 28.3 to 27.5887.
  * `PAPER_LEMGENDARY_MIRNET.md`: MIRNet v2 31 (and "31M+" in Section 3.1)
    to 0.0387.
  * `PAPER_LEMGENDARY_MPRNET.md`: the "Ours" row 17 to 0.0046.
  * `PAPER_LEMGENDARY_NAFNET.md`: the "Ours" row 17 to 4.4921.
  * The published-baseline rows (DnCNN, U-Net, MIRNet, Restormer) and the
    SOTA target rows describe other models and are unchanged.
* `PAPER_TRAINING_SUITE.md` Section 2.47 lists every registry model's old
  and measured count (for example `retinaface` 27.2 to 0.9357, `upn_v2` 88.5
  to 0.9287, `mprnet_deraining` 20.1 to 0.0046). The RetinaFace paper
  already stated 935,663. The capability registries hold no parameter
  counts.
* Every changed page mirrors its Markdown. `manifest/documents.json`: the
  changed papers are audited 2026-11-13.

### v16.9.113 - Training Suite v16.9.216 to v16.9.222 Kaggle Run Fixes

* `PAPER_TRAINING_SUITE.md` and its page (version line v16.9.222): new
  Section 2.47 "Kaggle Run Fixes: Manifold Dedupe, Log Lines, Decode
  Warnings & Export Probe (v16.9.216 to v16.9.222)".
  * Known issue in past runs, fixed in v16.9.216: Kaggle runs before
    v16.9.216 saw every train and validation sample twice per epoch, because
    alias paths of one manifold each opened a reader (`upn_v2`: 2,699,430
    train entries for 1,349,715 samples). Discovery now compares real paths.
  * Read-only manifold folders are skipped by the notebook sync (v16.9.217).
  * Kaggle trainer output is streamed through a pipe, so each line appears
    once (v16.9.219).
  * Decode warnings name the sample key, member, size, head bytes and shard
    (v16.9.220); the run 4 cases were 0-byte DPED `.jpg` members.
  * The export probe compares outputs on the CPU (v16.9.222), not yet rerun
    on Kaggle; the run 5 result is recorded.
* Section 8.1 lists the shard offset index as active and the doubled
  samples as a known issue of past runs.
* `manifest/documents.json`: Training Suite paper at baseline v16.9.222.
  The component baselines are unchanged.

### v16.9.112 - Shard Offset Index and `repair shard-offsets`

* `PAPER_DATASET_COMPILER.md` and its page (version line v16.9.108): new
  Section 4.13 "Shard Offset Index (v16.9.108)": `shard_offsets.json` in
  every shard folder, format `version` 2 (per plain tar shard `size`,
  `mtime_ns`, `names`, `offsets`, `sizes`), the acceptance rule (size plus
  modification time, or a three-header check), the read cost, the single
  writer `utils/shard_offsets.py` and the steps that refresh it, the shard
  verifier, the upload, the measured `repair shard-offsets` runs
  (RetinaFace, ParseNet, ClassificationMaster) and the read-only case.
  Section 4.12 names `shard-offsets` among the repairs.
* `PAPER_TRAINING_SUITE.md` and its page (version line v16.9.218): new
  Section 2.46 "Shard Offset Index & Fast WebDataset Open (v16.9.215 to
  v16.9.218)": the 48-minute open of run 3, the shipped index and its
  acceptance rule, the read-only cache fallback (`.cache/shard_offsets`,
  `LEMGENDARY_SHARD_CACHE_DIR`), the build lock per shard folder (one DDP
  rank builds), the 16-thread scan picked by a probe of the largest missing
  shard, and the measurements. Section 2.37 points from the hidden
  `.shard_offsets.json` cache to it.
* `MANUAL_CLI.md` and its page, Section 5.17: the `repair shard-offsets
  [--model KEY | --manifold PATH] [--apply]` example and entry; shard
  rewriting repairs refresh the index, and `repair manifold` verifies a
  present one.
* Capability registries (JSON and YAML): new capability
  `shard_offset_index` (dataset compiler v16.9.108, Training Suite reader
  v16.9.215).
* `manifest/documents.json`: dataset compiler paper at baseline v16.9.108,
  Training Suite paper at v16.9.218. The component baselines are unchanged.

### v16.9.111 - GUI v2.10.68 Kaggle Advanced Launch Controls

* `GUI_CONTROL_REGISTRY.md` and its page (version line v2.10.68): section
  3.6 lists the Kaggle launch "Advanced" group `kaggle-fieldset-advanced` and
  its four optional fields `kaggle-input-git-ref` (`git_ref`),
  `kaggle-input-env-manager-ref` (`env_manager_ref`),
  `kaggle-input-limit-hours` (`limit_hours`, greater than 0) and
  `kaggle-input-margin-minutes` (`margin_minutes`, 0 or more and below the
  limit), each empty by default and not sent when empty; refs follow the
  Training Suite ref rules. Section 3.9 lists the four `role="alert"`
  messages `kaggle-input-{field}-error`. The count is now 202 distinct IDs
  (128 controls, 74 dialogs, regions, landmarks and headings; was 193 / 123 /
  70), and section 3.11 lists the nine IDs under `v2.10.68` (53 added since
  the `v2.10.57` registry).
* `MANUAL_AI_STUDIO_GUI.md` and its page (version line v2.10.68): Section
  7.4 (now "v2.10.58 to v2.10.68", Training Suite contract up to v16.9.210)
  describes the Advanced group instead of saying the GUI lacks the clone ref
  and session window options.
* `manifest/documents.json`: both documents at baseline v2.10.68.

### v16.9.110 - ClassificationMaster Per-Source and Per-Class Counts

* `PAPER_DATASET_COMPILER.md` and its page, Section 7
  `LemGendizedClassificationMaster`: per-source train / val counts counted
  from the manifold's `index.json` (Anime DB Rating 544,611 / 74,903,
  Food-101 89,105 / 11,894, NSFW 29,030 / 3,991; totals 662,746 / 90,788)
  and the per-class train / val counts of the `repair class-labels` run
  (drawings 300,702 / 41,355, hentai 249,105 / 34,257, neutral 92,905 /
  12,445, porn 9,392 / 1,318, sexy 10,642 / 1,413). `index.json` has no class
  field, so the paper names the label repair as the source of the per-class
  counts.

### v16.9.109 - RetinaFace Paper Describes the Single-Box Model

* `PAPER_LEMGENDARY_RETINAFACE.md` and its page: the abstract, Section 1.1
  and Sections 5, 6 and 8 now describe the model in the training suite's
  `models/detection.py`: a MobileNetV3-Small backbone (`mobilenet_v2`
  optional), adaptive average pooling and three linear heads giving one
  normalized `cx cy w h` box, one sigmoid confidence and 10 landmark values
  per image. The anchor, FPN ($P_2$ to $P_5$), DCN v2 and ResNet-50 claims
  are removed; a multi-scale anchor head is noted as an open owner decision.
* The "sub-3ms" latency marked `[MEASURED]` (Section 6) and the "under 3
  milliseconds" claim (Section 1.1) are removed: no benchmark backs them,
  latency is "not yet measured". The crowd-scene pictures and the
  convergence curve are labelled as not measurements of the current model;
  the WIDER FACE ResNet-50 row is labelled an external reference value.
* Model info: 935,663 parameters with MobileNetV3-Small (927,008 backbone,
  8,655 heads), counted from the code; the training registry
  `parameters_m: 27.2` does not match. Section 6 uses the release names
  `RetinaFace-Detection.onnx`, `RetinaFace-Detection_FP32.onnx` (+ `.data`)
  and `RetinaFace-Detection.pt` and per-metric `vault_<metric>.pth` (there
  is no `vault_hard_ap.pth`). Section 4.4 (v16.9.100 metrics) is unchanged.

### v16.9.108 - Forex Paper States Only Measured Results

* `PAPER_FOREX_PREDICTOR.md` and its page (revision 2.9.0): no result figure
  has a backing measurement. The owner's `metrics.csv` row 1 copies the
  registry targets and row 2 opened no trade (Training Suite v16.9.164), so
  every result is marked "not yet measured". Removed: Direction Accuracy and
  Win Rate 49.69%, Profit Factor 0.99, Sharpe -0.16, Sortino -0.18, TP / SL
  MAE 615.42 / 617.95, Quality Score 105.87 (abstract, Sections 4.4, 4.7 and
  7, where it was marked `[MEASURED]`), the LSTM and vanilla Transformer
  comparison columns, the per-pair benchmarks (77.75% to 79.15% direction
  accuracy), the restoration and NIMA rows of Section 7 (each model reports
  in its own paper), the 1.42 ms / 2.18 ms latency, the RAM (53 GB to
  1.1 GB), throughput (12.5x) and iteration (28x) savings, the 65% and 85%
  market-share claims, 428,940 windows per fraction and the sub-microsecond
  recovery figure. The training curve is withdrawn (no measured epoch).
* Targets are the registry `sota_targets` (58.5 / 56.0 / 1.65 / 1.85 / 2.1 /
  12.0 / 12.5 / 12.5), replacing the old unsourced targets (> 60%, > 1.85,
  < 6.50% drawdown, > 150 quality). New Section 4.4.1 lists what a valid
  measured run must produce.
* Corrected from code: 26,818,700 rows (training registry count, was
  30,810,572), sample fraction fixed at 1.0 (was 15% to 100%), Forex VRAM
  batch tiers (a 4 GB GTX 1650 runs batch 32, not 256), the equity-model
  MaxDD formula (the 10,000-pip base formula is withdrawn), the spread stress
  (governor stress value over the pair pip scale; no fixed 1.5 / 3.0 pips),
  ONNX inputs with 14 features (was 10), the EA name
  `LemGendaryForexEA.mq5`, Fractional Kelly marked as proposed (the EA sizes
  from `RiskPct`), the one-tensor memory arithmetic (12.6 MB, was an
  unexplained 14.2 MB). Disk footprint figures point to the Dataset
  Compiler paper instead of being repeated.

### v16.9.107 - Component Baselines

* Both capability registries: `runtime_engine_baseline` v16.9.214-STABLE
  (LemGendary Model Training Suite), `dataset_compiler_baseline`
  v16.9.107-STABLE (LemGendary Dataset Compiler Suite),
  `environment_manager_baseline` v16.9.85-STABLE (LemGendary Environment
  Manager), `desktop_client_baseline` and `control_planes.gui.version`
  v2.10.67 (LemGendary AI Studio GUI), every model's `runtime_baseline`
  v16.9.214-STABLE, `last_audited` 2026-11-13. The documentation audit's
  component-version check passes again.
* README "Current baselines", `LEMGENDARY_CURRENT_STATE.md`,
  `VERSIONING_POLICY.md` and `ECOSYSTEM_ARCHITECTURE.md` (and their pages)
  name the same component versions and the hub release v16.9.107.

### v16.9.106 - Environment Manager v16.9.81 to v16.9.85, Registry Sync

* `PAPER_ENV_MANAGER.md` and its page (version line v16.9.85-STABLE): new
  Section 6.8 on the one Kaggle credential loader and the `access_token`
  writer (v16.9.84), the changelog scope rule for docs, test and tooling
  commits (v16.9.83) and the dropped `mosaicml-streaming` runtime dependency
  (v16.9.81). Section 6.7 documents `identity.github_url` and the `kaggle`
  section of `ecosystem.json` (collaborators, default accelerator,
  accelerator table, retired machine shapes; v16.9.85); the install step
  reports a failed editable install as a warning (v16.9.82).
* `ECOSYSTEM_ARCHITECTURE.md` and its page: MDS is discontinued and no longer
  in `runtime_env.yaml` (the "open" note is closed); shard labels are JSON
  only.
* Both capability registries: `train` syntax with `--clean` and
  `--override-frozen`; new `kaggle_launch` syntax and the `kaggle_status`,
  `kaggle_accelerators` and `kaggle_train` routes; RetinaFace is a
  single-box model with provisional `box_iou`, `ap50`, `ap50_95` and
  `landmark_nme` targets; Model Soup opens `soup-dialog` (GUI v2.10.60); the
  Ecosystem Registry lists `github_url` and the `kaggle` section;
  shard-window sampling is on by default (v16.9.159); new platform
  capabilities `kaggle_cloud_training` and `frozen_run_settings`. README hub
  features name them.

### v16.9.105 - GUI v2.10.67 Control Registry and Kaggle Launch Options

* `GUI_CONTROL_REGISTRY.md` and its page, recounted against LemGendary AI
  Studio GUI v2.10.67: 193 distinct IDs (123 controls, 70 dialogs, status
  regions, landmarks and headings; was 150). Added in sections 3.1 to 3.9:
  `dash-btn-refresh-projects`; the compiler sub-tabs,
  `compiler-btn-validate-schema`, `comp-input-max-gb`, `comp-input-workers`,
  `comp-select-shard-ext`, `comp-select-kaggle-registry` and
  `comp-btn-kaggle-registry-reload`; the card controls
  `train-select-batch-{model_key}`, `train-input-custom-batch-{model_key}`,
  `train-input-override-frozen-{model_key}`, `train-btn-docs-{model_key}` and
  `train-btn-stage-{model_key}`; the Blend Soup dialog (`soup-*`); the
  console tabs `training-telemetry-tabs-tab-*`; the Kaggle launch options
  `kaggle-accelerator-select`, `kaggle-poll-interval-input`,
  `kaggle-auto-pull-checkbox`, `kaggle-auto-resume-checkbox`,
  `kaggle-max-resumes-input` and `kaggle-override-frozen-checkbox`; the
  kernel picker; the status regions `cloud-modal-auth-badge`,
  `cloud-modal-auth-error`, `cloud-modal-dataset-links`,
  `kaggle-accelerator-source`, `comp-badge-kaggle-auth`; and the resume
  refusal region `train-frozen-refusal` with `-message`, `-changes`, `-hint`
  and `train-btn-frozen-refusal-dismiss`. `gpu-select` is removed and the
  Config & Secrets tabs are `config-tabs-tab-*`. Section 3.10 drops the
  controls that gained an ID; Section 3.11 lists the changes by release.
* `MANUAL_AI_STUDIO_GUI.md` and its page (version line v2.10.67): new Section
  7.4 on the Kaggle launch options, kernel monitor, variation names, card
  transfers, the override toggle, the resume refusal notice and the Blend
  Soup dialog; the authentication row and the variation select of Section
  7.3 are corrected.

### v16.9.104 - Dataset Compiler v16.9.85 to v16.9.107 in the Paper

* `PAPER_DATASET_COMPILER.md` and its page (version line v16.9.107-STABLE):
  new Section 4.12 documents the JSON label schema (`face_landmarks`,
  `yolo_boxes`, `yolo_polygons`, `nima`, `segmentation_mask`, `class_label`,
  `caption`, with `objects`, `class_id` / `class_name`, `caption`,
  `landmark_source`, `label_source` / `label_confidence`), the sample
  policies and the shared val split by source file id, the `source_labels`
  registry with the `celebamask_hq_19` and `sfhq_110` schemes, the
  ClassificationMaster class labels (`nsfw_5`, pseudo labels kept at 0.8 when
  both GantMan models agree), the repairs, the Kaggle sync changes, Forex
  timestamps in seconds and the GUI-facing routes.
* Section 7: LemGendizedClassificationMaster 753,534 samples (train 662,746
  / val 90,788, 5 classes), LemGendizedParseNet 425,258 (train 374,228 / val
  51,030, 19 mask classes) and LemGendizedRetinaFace 425,223 (train 374,199 /
  val 51,024). Per-class counts are not recorded in the local
  `dataset_info.yaml` files, so none are given.
* Section 4.11: repairs no longer keep a `.repair_backup` copy. Section 4.5:
  the MDS writer needs the optional `mosaicml-streaming` package, which the
  Environment Manager no longer installs.

### v16.9.103 - Training Suite v16.9.158 to v16.9.214 in the Papers

* `PAPER_TRAINING_SUITE.md` and its page (version line v16.9.214-STABLE): six
  new sections. 2.40: the `torch.export` ONNX exporter, the three release
  variants, ONNX `metadata_props`, the MT5 artefact (one file, IR 9) and the
  MQL5 EA built from `data/mt5_feature_spec.py`. 2.41: locality sampling on
  by default, generator state per DDP rank, frozen and epoch run settings,
  `--override-frozen`, `resume_refusal.json` and head parameter prefixes.
  2.42: LPIPS loss, the NIMA soft logit cap, temperature 1, `emd_form` and
  post-hoc calibration, honest Forex metrics, `risk_per_trade` and the
  RetinaFace metrics. 2.43: one device-memory adapter, the DXGI budget and
  DirectML through `torch_directml`. 2.44: the preprocessing key, the 5-class
  NSFW head, `IGNORE_TARGET`, JSON-only shard labels and the YOLO shard
  cache. 2.45: the Kaggle cloud pipeline and the one models hub root. The
  Section 2.37 locality bullet no longer calls the sampler opt-in.
* `PAPER_LEMGENDARY_NIMA.md` and its page (revision 3.3.0): new Section 5.50
  (soft logit cap 15, temperature 1, `emd_form`, post-hoc calibration); the
  0.1 temperature anchor of Section 3.1.2 is marked superseded.
* `PAPER_FOREX_PREDICTOR.md` and its page (revision 2.8.0): the equity-model
  MaxDD at `evaluation.risk_per_trade` and the weighted Forex score
  (`forex_weighted_targets_v2_risk0.01`) are documented; the 665.80% drawdown
  is withdrawn as the old cumulative-pip measure; the ONNX export is opset 18
  with an IR 9 single-file MT5 graph; new Section 6.3 describes the
  generated MQL5 Expert Advisor.

### v16.9.102 - CLI and API Reference: Kaggle Routes, Sync Pull, Repairs

* `MANUAL_CLI.md` and its page: Section 5.10 documents `sync pull --only`
  and `--output`, the missing-root fix, the file-by-file fallback when Kaggle
  has no whole-dataset archive, the Kaggle API route after a per-file 404,
  the HTTP 429 retry, label packing on pull and private new datasets
  (LemGendary Dataset Compiler Suite v16.9.96 to v16.9.104). New Section
  5.17 "Manifold Repair (`repair`)" lists `manifold`, `all`, `labels`,
  `txt-labels`, `pack-loose`, `sample-policy`, `masks`, `face-landmarks`,
  `pseudo-labels` and `class-labels` with their options. Section 5.2 no
  longer uses MDS in its examples and says that `mds` needs the
  `mosaicml-streaming` package the Environment Manager no longer installs.
* `MANUAL_API.md` and its page (version line v16.9.214-STABLE): the training
  endpoint matrix lists the Kaggle routes (`status`, `kernels`,
  `accelerators`, `train`, `monitor`, `pull`, `push`); new sections document
  the status probe fields, the accelerator list and every
  `POST /api/training/kaggle/train` field (`accelerator`, `git_ref`,
  `env_manager_ref`, `limit_hours`, `margin_minutes`, `override_frozen`,
  `auto_pull`, `poll_interval`, `auto_resume`, `max_resumes`), the monitor
  and pull requests. `push-model` uses the `VariationKey` names and the real
  response (`variations`, `skipped`, `errors`). `quick-train` takes `clean`
  and `override_frozen`; `ModelWithStats.sota_targets_provisional` is
  documented. Dataset Compiler: `/api/config/validate` is open to the GUI
  origins, `/api/kaggle/status` lists the four credential sources, and
  `quick-compile` takes `max_gb`, `workers` and `shard_ext`.

### v16.9.101 - Kaggle Cloud Training How-To

* `MANUAL_CLI.md` and its page (checked against LemGendary Model Training
  Suite v16.9.214): new Section 6.13 "Kaggle Cloud Training How-To
  (`lemtrain kaggle`)". It covers the `KGAT_` API token (resolver order:
  vault, `KAGGLE_API_TOKEN`, `kaggle.json`, `~/.kaggle/access_token`), the
  Kaggle Secrets to attach (`KAGGLE_API_TOKEN`; `GITHUB_PAT` or `SUITE_PAT`;
  optional `GOOGLE_DRIVE`), the accelerators `cpu`, `gpu-t4x2` (default) and
  `tpu-v5e8`, `lemtrain kaggle accelerators|bundle|launch|status`, the launch
  options `--git-ref`, `--env-manager-ref`, `--limit-hours`,
  `--margin-minutes` and `--override-frozen`, the 12 h session guard, the
  deadline stop (`session_deadline.json`), auto-resume, the trainer exit gate
  before the publish cell, the `resume_refusal.json` record, the
  `VariationKey` names, the one push policy (page before upload, skip
  unchanged variations), version notes and the first live check.
* Section 6.2: `--override-frozen` and the frozen / epoch run settings of a
  resume. Section 6.9: `VariationKey` values and the epoch-based pull merge.

### v16.9.100 - RetinaFace Box IoU, AP and Landmark NME

* `PAPER_LEMGENDARY_FACE_SUITE.md` and its page (revision 1.1.0, checked
  against LemGendary Model Training Suite v16.9.214): the RetinaFace targets
  "mAP (Easy) >= 0.915" and the mAP medium / hard rows are replaced by the
  metrics the training suite measures since v16.9.208: `box_iou` >= 0.80,
  `ap50` >= 0.95, `ap50_95` >= 0.60 and `landmark_nme` <= 0.10, all
  provisional (`sota_targets_provisional: true`, no cited source yet). The
  model is described as a single-box regressor (one box, one confidence and
  five landmarks per image, no anchors), the manifold as
  `LemGendizedRetinaFace` (425,223 samples: train 374,199 / val 51,024,
  boxes and points rebuilt from the SFHQ 110-point landmarks), and the
  matrix row and abstract follow. A note says that RetinaFace metrics
  recorded before v16.9.207 / v16.9.208 are not comparable with new runs.
* `PAPER_LEMGENDARY_RETINAFACE.md` and its page: the same four metrics and
  provisional targets, the 17-column `metrics.csv` layout and the
  `face_box_weighted_targets_v1` score scheme. The WIDER FACE AP, NME and
  latency values of Sections 4 and 7 marked `[MEASURED]` are removed: no
  measurement backs them, and the manifold holds 425,223 SFHQ photos, not
  32,203 WIDER FACE samples. Section 3 notes that the suite's model has no
  prior boxes.
* `PAPER_TRAINING_SUITE.md` and its page: the `retinaface` registry row lists
  the provisional targets.

### v16.9.99 - Merged Similar Training Pathologies

* `PAPER_TRAINING_PATHOLOGY.md` and its page: revision 1.12.0. Five similar
  pairs are merged into the lower number, each combined entry keeping both
  mechanisms: NaN Divergence now covers overflow and mixed-precision
  underflow (20 into 5), the Training Plateau row names optimizer momentum
  decay and its remedies (21 into 7), Checkpoint Fraction Desynchronization
  covers preemption recoil and the ghost loader in its row and section
  (25 into 18), Memory-Sentinel Drift includes atomic hardware re-auditing
  (45 into 44), and the 4 GB paging section covers language and vision
  models (47 into 34). Numbers stay stable: each higher number keeps its
  heading or row with a short "Merged into Pathology N" pointer, so
  external references and anchors stay valid. The abstract counts 58
  distinct pathologies (it said 63) and Section 2 explains the merges.
* `LEMGENDARY_CURRENT_STATE.md` and `VERSIONING_POLICY.md` (and their
  pages): pathology guide revision 1.12.0; the current state lists 58
  distinct pathologies under 63 stable numbers.
* **Version** - hub version v16.9.99 in `README.md`, `index.html`, manifest,
  both registries and the Current State and Versioning Policy documents.

### v16.9.98 - Training Pathology Numbering

* `PAPER_TRAINING_PATHOLOGY.md` and its page: revision 1.11.0. Only
  Pathologies 24 to 39 carried a number; the guide describes 63 distinct
  pathologies, and every one now has a number in the master table, its
  section heading, the table of contents and the cross-references.
  Pathologies 24 to 39 keep their numbers. The master-table rows are
  Pathologies 1 to 19 in their order (with 24 to 27 and 36 as before), the
  first four unnumbered Section 4 headings are 20 to 23, and the remaining
  Section 4 and Section 5 headings are 40 to 61 in document order. Two
  pathologies that only Sections 9 to 11 named get short sections:
  Finished-Epoch Resume Loop (62) and Restoration Metric Weight Imbalance
  (63). A master-table row and the section that details it share one
  number (14 to 19, 24 to 27 and 36). The abstract states 63 (it said 39),
  Section 2 explains the numbering and Section 8 names the numbers.
* `LEMGENDARY_CURRENT_STATE.md` and `VERSIONING_POLICY.md` (and their
  pages): pathology guide revision 1.11.0; the current state lists the 63
  numbered pathologies.
* **Version** - hub version v16.9.98 in `README.md`, `index.html`, manifest,
  both registries and the Current State and Versioning Policy documents.

### v16.9.97 - Training Pathology Page Parity, Labelled List Item Check and Master API Python Examples

* `papers/training-pathology.html`: the Section 2 master table lacked the
  Pathology 36 row (Static OS Worker Throttling & WebDataset Tar
  Decompression Starvation) that the Markdown has; the row is added. The
  Pathology 35 and 36 sections of the page were older shortened wording;
  they now follow the Markdown word for word (the three-case task index
  resolution, the 12-thread example, the epoch-time estimate and the three
  worker formulas).
* `scripts/docs_audit/`: new `list-items` check. Every top-level list item
  that opens with a bold label (the master-table rows written as lists)
  must appear in the Markdown and the page, in the same order; a missing,
  extra or reordered row is a finding. Labels wrapped over several lines
  are joined; nested items and lists in the sidebar, code, block quotes
  and tables are not counted. `tests/test_docs_audit.py` covers matching
  rows, a missing row, reordered rows and quoted lists.
* `MANUAL_API.md` and its page: the Section 4.7 example imported modules
  and classes that do not exist (`training.core.orchestrator`,
  `TrainingOrchestrator`, `training.governance.sentinel`, `DynamicGovernor`,
  `training.models.registry`, `ModelRegistry`). It now uses
  `get_model_registry()` from `training.registry.model_specs`,
  `SentinelGuard` from `training.hardware.sentinel`,
  `SmartTrainingGovernor` from `training.governance.governor`, and
  `load_workspace_config`, `load_model_info` and `main` from
  `training.core_loop`. The Section 5.8 example named `CompilerService`
  and `ZipToContainerStreamer`, which do not exist, and wrong
  `migrate_containers` arguments; it now uses `run_compile()`,
  `ZipStreamOptions` with `stream_zip_to_webdataset()` and the static
  `MigrationService.migrate_containers(manifold_path, to_formats, ...)`.
  Both sections say to run from the project root with its `.venv`. Every
  import was checked against the LemGendary Model Training Suite and the
  LemGendary Dataset Compiler Suite sources.
* **Version** - hub version v16.9.97 in `README.md`, `index.html`, manifest,
  both registries and the Current State and Versioning Policy documents.
  `VERSIONING_POLICY.md` Section 8 wraps its 90-column line at 80 columns
  (markdownlint MD013).

### v16.9.96 - LemGendary Model Training Suite v16.9.157 and Environment Manager v16.9.80 Sync (Audit Phase 5b)

* `canonical_capabilities.json`, `canonical_capabilities.yaml`:
  `runtime_engine_baseline` and every model `runtime_baseline` set to
  v16.9.157-STABLE (they said v16.9.139 and v16.9.128),
  `environment_manager_baseline` to v16.9.80-STABLE. New platform capability
  `shard_locality_sampling` (`data.locality.window_shards` and
  `data.locality.fraction_block_size`, off by default). Its two behaviour
  strings are folded YAML scalars so every YAML line stays under the
  120-column yamllint limit.
* `scripts/parity_backlog.json`: the last backlog entry
  (`runtime_engine_baseline`) is resolved and removed; the backlog is empty.
* `PAPER_TRAINING_SUITE.md` and its page (v16.9.157-STABLE): new Sections
  2.36 (container targets for both shard layouts, 15-value face targets with
  masked absent landmarks, synthesised degradation for unpaired samples,
  UltraZoom bicubic input, prompt masking, LPIPS for `l1_lpips` models,
  governor LR as a ratio over the scheduler, deterministic mid-epoch resume
  with `ResumableBatchSampler` and GradScaler state, NCCL/Gloo selection,
  macOS worker budget, POSIX process-group cleanup, readiness flags), 2.37
  (byte-offset shard reads, `.shard_offsets.json` cache, 16-handle LRU
  pool, label 0 fix, zero-rebuild curriculum transitions, opt-in locality
  sampler), 2.38 (one quality score with scheme tagging and FID as a
  separate gate, four optimizer groups with old-checkpoint migration, the
  exact-divisor batch rule, VRAM refit on resolution jumps with the
  `256px -> 384px -> 512px -> 640px` memory analysis, rung entry fraction)
  and 2.39 (single task-type resolver, exact-divisor OOM throttle,
  `EpochOrder`, optional `paged_adamw_8bit()` adapter), with LaTeX for the
  LR ratio, quality score, batch invariant and memory bound. Section 2.21
  named stale pins (`torch 2.14.1+cu126`) and a training-side index
  selection; it now names the central pins and the env-manager probe
  (`cu134`, `cu126`, `cu121`, `cu118`) and marks the GTX 1650 gates as run
  on the earlier stack. Section 2.34 dates `REVIEW_REPORT.md` to v16.9.123.
  The abstract, the scorecarding bullet (FID no longer compounded into the
  score) and Section 8.1 follow; a raw `**` in the 2.35 page is now
  `strong`.
* `PAPER_TRAINING_PATHOLOGY.md` and its page: revision 1.10.0, baseline
  v16.9.157-STABLE; Pathology 36 describes the bounded handle pool and
  offset reads, Pathology 29 the probe-selected `cu134` index.
* `MANUAL_API.md` and its page: `ModelWithStats` example and field list
  gain `pytorch_ready`, `onnx_fp32_ready` and `onnx_fp16_ready`.
* `LEMGENDARY_CURRENT_STATE.md`, `VERSIONING_POLICY.md`,
  `ECOSYSTEM_ARCHITECTURE.md` and their pages: training suite v16.9.157,
  env manager v16.9.80, documentation hub v16.9.96, pathology guide 1.10.0.
  The GTX 1650 bullet no longer claims a current cu126 verification; it
  names the earlier `torch 2.14.1+cu126` stack and the `cu134` index the
  probe selects today.
* `PAPER_ENV_MANAGER.md`, `MANUAL_CLI.md` and their pages: env manager
  v16.9.80; every validation gate runs its tool from the project
  directory, so `validate` behaves the same from the workspace root.
* `manifest/documents.json`: training suite and pathology baselines
  v16.9.157-STABLE, env manager v16.9.80-STABLE, touched documents audited
  2026-11-12.

### v16.9.95 - Current State and Versioning Policy Version Sync (Audit DOCS-4)

* `LEMGENDARY_CURRENT_STATE.md`, `VERSIONING_POLICY.md` and their pages:
  component versions synced with the component sources: LemGendary
  Environment Manager v16.9.79, LemGendary Dataset Compiler Suite v16.9.84,
  LemGendary AI Studio GUI v2.10.57, documentation hub v16.9.95 and the
  Training Pathology Guide revision 1.9.0 (baseline v16.9.138). The
  training suite versions are left for the training-suite sync.
* `LEMGENDARY_CURRENT_STATE.md` and its page: the "cu126 PyTorch Stack"
  bullet named stale pins (`torch 2.14.1+cu126` and others) and a fixed
  index list; it now names the central requirements pins and the probe
  index order (`cu134`, `cu126`, `cu121`, `cu118`, ROCm, PyPI for Apple
  MPS, CPU).
* `MANUAL_AI_STUDIO_GUI.md` and its page: the example wheel index row named
  `cu121` next to driver 610.74; the probe selects `cu134` for that driver.
* `manifest/documents.json`: `current-state` and `versioning-policy`
  audited 2026-11-12.

### v16.9.94 - LemGendary AI Studio GUI v2.10.57 Control Registry, Manual and Whitepaper (Audit DOCS-3)

* `GUI_CONTROL_REGISTRY.md` and its page: recounted against the
  `lemgendary-ai-studio-gui` source of v2.10.57: 150 distinct IDs (91
  controls). Added `train-btn-soup-{model_key}`, `kaggle-monitor-slug` and
  `kaggle-monitor-btn`. Section 3.10 now lists every control without an ID
  by area (it missed, among others, the card "Docs & Meta" and "Stage
  Variations" actions, the batch size select, the filters and the manifest
  editor buttons). The IDs the 2026-11 audit asked to add
  (`compiler-btn-validate-schema`, `comp-input-max-gb`,
  `train-select-batch-{key}`, `config-tabs-tab-manifests` and others) do not
  exist in the source; section 3.11 records this.
* `MANUAL_AI_STUDIO_GUI.md` and its page: the Reconcile button exists
  ("Reconcile Environment" on each project card), but it calls
  `POST /api/pipeline/run` with `target_project` and `clean: false`, not the
  nonexistent `POST /api/pipeline/reconcile`, and keeps valid `.venv`
  folders. `unified_requirements.yaml` replaced with
  `lemgendary-env-manager/requirements/*.txt`. Documents the v2.10.47 to
  v2.10.57 features: manifest editor guards and central manifests, the red
  error banner for failed actions, per-step pipeline pills, remote job
  restore and polling, per-format variation badges, card actions disabled
  while the training sidecar is offline, telemetry auto-scroll, sidecar
  stop with SIGTERM before SIGKILL, Blend Soup, Attach Monitor and the
  portable verify script.
* `PAPER_AI_STUDIO_GUI.md` and its page: v2.10.57; the drift matrix reads
  the central requirements files; the v2.10.47 to v2.10.55 architecture
  changes are listed in Section 6.9.
* `canonical_capabilities.json` and `.yaml`: `model_soup` is available in
  the GUI since v2.10.57 (`train-btn-soup-{model_key}`).
* `manifest/documents.json`: the three GUI documents at baseline v2.10.57.

### v16.9.93 - LemGendary Dataset Compiler Suite v16.9.84 (Audit DOCS-2)

* `PAPER_DATASET_COMPILER.md` and `papers/dataset-compiler.html`: baseline
  v16.9.84-STABLE (was v16.9.65; the audit named v16.9.75, but the suite
  declares 16.9.84 in `core/cli_args.py`). The abstract summarizes
  v16.9.66 to v16.9.84, and the new Section 4.11 "Sample Integrity, Shard
  Verification & Manifold Repair" documents the v16.9.75 to v16.9.84
  changes: no identity pairs, lossless masks and corrupt-image rejection,
  contiguous sample groups, label geometry fixes, the audit gates and
  `reject_log`, post-write shard verification with pair completeness, the
  lossless MDS transcode, safe worker init and interrupt, full dedup on
  warm-up and resume, download and Temp sweep safety, the `repair` command
  and logged instead of swallowed errors.
* `manifest/documents.json`: `dataset-compiler` baseline v16.9.84-STABLE.

### v16.9.92 - LemGendary Environment Manager v16.9.79 and PyTorch Index Claims (Audit DOCS-2)

* `PAPER_ENV_MANAGER.md` and `papers/env_manager.html`: baseline
  v16.9.79-STABLE (the page abstract still said v16.9.60). Documents the
  v16.9.69 to v16.9.79 changes: the `cu134` index for drivers 610 and newer,
  the PyPI index for Apple MPS and the probe order; no fixed
  `--extra-index-url` in the central requirements; the 64-bit DirectML and
  CSV `rocm-smi` probes; the `bitsandbytes` macOS marker; the write-back of
  upgraded pins only after validation (`finalize_upgrade()`) and the npm
  write-back; the manifest editor that opens the central manifests;
  `pip3` detection; `sys.prefix` venv detection; the editable project
  install; one upgrade engine with CUDA family vetting; the in-memory
  compile check and the new and corrected validation gates.
* PyTorch claims checked against `lemgendary-env-manager/requirements/`
  (`torch==2.15.0`, `torchvision==0.29.2`, `torchaudio==2.11.1`,
  `transformers==5.22.1`; the wheel index comes from the hardware probe):
  `ECOSYSTEM_ARCHITECTURE.md` no longer names a fixed `cu126` index and lists
  `cu134`; `GLOSSARY.md` lists `cu134`; the `MANUAL_API.md` manifest example
  shows the pins instead of the removed `--extra-index-url` line;
  `MANUAL_CLI.md` no longer names a fixed `cu121` index. The training suite
  paper keeps its claims until that suite's documentation sync.
* `ECOSYSTEM_ARCHITECTURE.md`: component versions Environment Manager
  v16.9.79, Dataset Compiler Suite v16.9.84, AI Studio GUI v2.10.57.
* `manifest/documents.json`: `env_manager` baseline v16.9.79-STABLE; audit
  dates of the edited documents.

### v16.9.91 - Audit Checks for Sidebars, Alert Markers and Component Versions (Audit DOCS-4)

* `scripts/docs_audit/`: three new checks.
  * `toc-sidebar`: the `nav.toc-sidebar` links of a page list the same
    entries in the same order as the Markdown table of contents, neither
    lists a target twice, and every level-2 section with content has a
    sidebar link.
  * `alert-markers`: raw GitHub alert markers (`[!NOTE]`, `[!IMPORTANT]`,
    `[!WARNING]`, `[!TIP]`, `[!CAUTION]`) in a page are a finding.
  * `component-versions`: the component baselines of
    `canonical_capabilities.json` equal the versions in
    `env_manager/__init__.py`, `core/cli_args.py`, the training suite
    `pyproject.toml` and the GUI `package.json`, and
    `control_planes.gui.version` equals `desktop_client_baseline`. The
    project folders come from `ecosystem.json`. `manifest/documents.json`
    holds no component baselines, only per-document baselines.
* `canonical_capabilities.json` and `.yaml`: LemGendary Environment Manager
  v16.9.79, LemGendary Dataset Compiler Suite v16.9.84, LemGendary AI Studio
  GUI v2.10.57. The LemGendary Model Training Suite baseline stays at
  v16.9.139 and is the one backlog entry until that suite's documentation
  sync.
* `MANUAL_API.md`, `MANUAL_CLI.md` and `PAPER_LEMGENDARY_ULTRAZOOM.md` (and
  their pages): the table of contents and sidebar now link the "Companion
  Documentation" and "1.1 What UltraZoom Does" sections the new check found.
* `REVIEW_REPORT.md` removed: the 2026-11-02 review it records was closed
  in v16.9.77 and git keeps the history.
* `scripts/audit_docs.py` and `tests/test_documentation_content.py`: no
  optional-member access on `None` (pyright clean).
* Tests: 9 new audit tests; the fixture workspace gains the four version
  files and the `projects` list.

### v16.9.90 - Training Pathology Table of Contents Repair (Audit DOCS-1)

* `MD-Papers/PAPER_TRAINING_PATHOLOGY.md`: removed the orphan fragment and
  the duplicated Pathology 26 to 34 entries from the table of contents and
  added the missing entries for Pathologies 37 to 39.
* `papers/training-pathology.html`: the sidebar lists Pathologies 36 to 39,
  which were missing.
* Both files: Paper Revision 1.9.0 (2026-11-12). The Abstract counts 39
  pathologies (it said 27) and cites the header release v16.9.138-STABLE
  instead of revision 1.6.0 and v16.9.107-STABLE. The Section 5 note cites
  v16.9.138-STABLE instead of v16.9.68-STABLE.
* The raw `[!NOTE]` text in `papers/training-pathology.html` and
  `papers/foundation-llm.html` is now a styled `Note:` blockquote, the
  markup the other pages use. In both Markdown sources the `[!NOTE]` marker
  stands on its own line, which GitHub needs to render the alert.
* `manifest/documents.json`: `training-pathology` audited 2026-11-12.

### v16.9.89 - WCAG 2.2 AA Contrast Fixes (Audit WCAG)

* `style.css`: new colour token `--accent-fill` (`#006ee6`, 4.8:1 against
  white text) for the active tab pill. The accent colour `#007aff` gave white
  text only 4.0:1: 48 of the 61 pa11y findings, one per paper page.
* `papers/ecosystem-architecture.html`: edge labels of the Mermaid dark theme
  had 4.43:1 contrast (11 findings); the diagram now sets
  `edgeLabelBackground` to the code background colour.
* `MD-Papers/PAPER_LEMGENDARY_CODEFORMER.md` and `papers/face-codeformer.html`:
  restored two damaged formulas ($b_{\text{chunk}} \le 2$ and $20\%$
  strides). MathJax rendered the broken input as red error text, which also
  failed the contrast check (2 findings); the HTML list item that had
  swallowed the next bullet is split again.
* `requirements.txt`: regenerated from the central
  `requirements-documentation.txt` of the LemGendary Environment Manager. It
  now pins `pylint`, which the validator runs in this venv.
* All 49 pages pass pa11y (WCAG2AA) with no findings.

### v16.9.88 - Dynamic Worker Topology & Boundary Tooltip Positioning

* `manifest/documents.json`, `canonical_capabilities.json`, `canonical_capabilities.yaml`:
  Synchronized Model Training Suite baseline to `v16.9.138-STABLE` and AI Studio
  GUI baseline to `v2.10.45` with audit timestamp `2026-11-10`.
* `MD-Papers/PAPER_TRAINING_PATHOLOGY.md` and `papers/training-pathology.html`:
  Documented Pathology 36 (Static OS Worker Throttling & WebDataset Starvation)
  covering dynamic worker sizing, memory headroom equations, and fork-safe tar
  handle isolation.

### v16.9.87 - Sidecar Process Lifecycle Hardening & Multitask Loss Alignment

* `MD-Papers/LEMGENDARY_CURRENT_STATE.md` and `papers/current-state.html`:
  Documented persistent `server.pid` recording upon detached sidecar launch and
  multi-format `netstat` listening port resolution across modern Windows
  environments.
* `MD-Papers/PAPER_LEMGENDARY_HYBRID.md` and `papers/universal-hybrid.html`:
  Updated Section 3.2 mathematical formulation and task ingestion details for
  multitask loss normalization ($int64$ tensor resolution across DataLoader
  collation string tuples).

### v16.9.86 - PyTorch 2.15.0+cu134 Toolchain Upgrade & Component Baseline Refresh

* Updated ecosystem baselines to LemGendary Environment Manager v16.9.63,
  LemGendary Dataset Compiler Suite v16.9.72, LemGendary Model Training Suite
  v16.9.133, and LemGendary AI Studio GUI v2.10.42.
* Synchronized documentation regarding PyTorch 2.15.0+cu134, TorchVision
  0.29.2+cu134, and TorchAudio 2.11.1+cu134 runtime acceleration under CUDA
  13.4.

### v16.9.85 - Edge GPU 4GB VRAM Containment & Causal LLM Quantization Hardening

* `MD-Papers/PAPER_LEMGENDARY_LLM.md`: documented 4-bit NF4 QLoRA quantization,
  SDPA execution, gradient checkpointing, and Paged 8-bit AdamW containment profile.
* `MD-Papers/PAPER_TRAINING_PATHOLOGY.md`: catalogued Pathology 33 (Unquantized
  Checkpoint Resume Shape Mismatch on 4-bit Backbones) and Pathology 34 (PCIe
  Paging Thrashing & Host VRAM Starvation on 4GB Accelerators).
* `MD-Papers/PAPER_TRAINING_SUITE.md`: detailed Section 7.6 Edge Hardware
  Optimization Profile for sub-4GB consumer accelerators.

### v16.9.84 - Three-Way Split (Train/Val/Test) & Held-Out Test Evaluation

* `MD-Papers/PAPER_DATASET_COMPILER.md` and `papers/dataset-compiler.html`:
  documented Three-Way Partitioning (`val_split` and `test_split`) with
  deterministic stratification across all 7 corpus categories and held-out test
  shard generation (`ai_helper_test.jsonl`).
* `MD-Papers/PAPER_TRAINING_SUITE.md` and `papers/training-suite-master.html`:
  documented held-out test set ingestion, tokenization, and automated post-training
  evaluation metrics (`test_loss`, `test_perplexity`, `test_accuracy`).
* `canonical_capabilities.yaml`, `canonical_capabilities.json`, and
  `manifest/documents.json`: bumped runtime engine baseline to `v16.9.128-STABLE`
  and dataset compiler baseline to `v16.9.71-STABLE`.

### v16.9.83 - Master API Manual .secrets.yaml SSOT Alignment

* `MD-Papers/MANUAL_API.md` and `papers/api-manual.html`: updated `GET
  /api/secrets` and `POST /api/secrets` specifications to establish
  `.secrets.yaml` as the authoritative Single Source of Truth across the
  ecosystem, removing references to legacy token dotfiles. Aligned
  `/api/kaggle/status` credential reporting with `.secrets.yaml`.

### v16.9.82 - Merge of `main`: LLM Whitepapers from the Owner

* **Merge** - `origin/main` commit `8645505` (owner's LLM pathology, QLoRA
  and vault milestone additions, released on `main` as v16.9.64) is merged
  into this branch. All of its text is kept; it is placed in the
  restructured papers, wrapped to 80 columns and mirrored in the HTML pages.
* **Renumbering** - the owner's Training Suite Section 2.25 is now Section
  2.35 (2.25 to 2.34 already exist), and the owner's Pathologies 26 to 30
  are now Pathologies 28 to 32 (26 and 27 already exist). Table of contents
  entries are added in Markdown and HTML.
* **Facts checked against the LemGendary Model Training Suite (`main`)** -
  the gradient accumulation formula uses `round`, not floor
  (`update_batch_and_accumulation`); NF4 loading is opt-in
  (`load_in_4bit=True`, default `False`); the soup entry point is
  `create_pareto_model_soup` (there is no `ParetoModelSoup` class);
  `audit_hardware_vram` uses a fixed heuristic (70% of free VRAM, about
  0.45 GB per 2048-token sample) when `batch_size` is `auto`; the 2.8 GB
  activation bound is a sizing target the code does not measure; the trainer
  has no automatic CPU-only-wheel pre-flight check (only the Kaggle
  notebooks probe the GPU); the LLM ONNX export uses `dynamo=True` with
  `torch.export.Dim` and `use_cache = False` (the Markdown text had the
  older dynamic-axes remedy; the HTML text was already right).
* **Version** - hub version v16.9.82 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML).

### v16.9.81 - Final Refresh to the Current Component Releases

* **Training Suite** (`PAPER_TRAINING_SUITE.md`, v16.9.122): new Section 2.34
  Version Single Source, Lint & Review Fixes: the version lives only in
  `pyproject.toml` (`training/version.py`; CLI, sidecar, health route,
  notebooks and `openapi.json` derive it; `config.yaml` has no `version`
  key), pyright 0, pylint 0 with no `.pylintrc` disables (seven inline
  `too-many-arguments` directives stay), grouped `TrainingContext`, and the L10
  review fixes (D-06, D-07 part, D-08, D-12, D-13, D-15, D-16).
* **Master API Manual**: `parameters_m`, `best_metric` and `sota_target` of
  `GET /api/gui/models/with-stats` are documented as nullable (measured or
  registered values only); the example uses the registry count (17.1) and the
  `GET /api/gui/state` example the real service version.
* **AI Studio GUI** (v2.10.38): nullable model stats and the `N/A` Parameters
  row (whitepaper, manual); no sidecar port written out in the source since
  v2.10.37. The control registry is recounted from the v2.10.38 source (147
  distinct IDs: 88 in sections 3.1 to 3.8, 59 in section 3.9, was 119 from
  v2.10.19); the existing `cloud-modal-tab-*`, `train-modal-tab-upload`,
  `config-editor-tab-*`, `*-panel`, `test-modal` and
  `comp-input-kaggle-custom-ref` IDs are added and no longer listed as
  missing.
* **Environment Manager** (`PAPER_ENV_MANAGER.md`, v16.9.60): the
  `ecosystem_ssot` port rule flags every standalone port token (v16.9.59);
  `check_npm_manifest` and the pipeline step check are listed; the
  `package.json` `version` is not compared or synced (v16.9.60).
* **Dataset Compiler** (`PAPER_DATASET_COMPILER.md`): version line v16.9.65.
* **Current State, Versioning Policy, Architecture**: component versions
  (Environment Manager v16.9.60, Dataset Compiler Suite v16.9.65, Model
  Training Suite v16.9.122, AI Studio GUI v2.10.38); OpenAPI operation counts
  33, 37 and 40; Ruff and Pylint both described as in use; the
  zero-suppression statements name the seven inline pylint directives.
* **Registries and manifest** - baselines and runtime baselines updated;
  document baselines of the six papers above. **Version** - hub version
  v16.9.81 in `README.md`, `index.html`, manifest, both capability
  registries, `VERSIONING_POLICY.md` and `LEMGENDARY_CURRENT_STATE.md`
  (+ HTML). HTML pages carry the same changes as their Markdown sources.
* **Workspace validator** - `python -m env_manager.cli validate -p
  lemgendary-docs` passes. HTML: heading ids start with a letter (`sec-`
  prefix, internal links updated); the redundant `style="text-align:left"`
  on table cells is removed (`style.css` already aligns them left); the hub
  portal buttons have `type="button"` and the footer link colour moved to
  `style.css`; four page titles are at most 70 characters. Pylint: docstrings
  in `scripts/docs_audit`; `tests/test_documentation.py` is split into the
  shared `tests/docs_test_base.py`, `test_documentation.py`,
  `test_documentation_content.py` and `test_ai_helper_corpus.py`, and
  `test_docs_audit.py` into parity, backlog and registry classes (same 65
  passing tests, 2 skips).

### v16.9.80 - Later Phase Documentation Sync (DOCS-3)

* **Training Suite** (`PAPER_TRAINING_SUITE.md`, v16.9.107): new Sections
  2.30 Ecosystem Facts & GUI Training Verdict (required `training_status` and
  `is_fully_trained`, `unknown` with `stats_error`, derived `kaggle_ref`), 2.31
  Manifold Task from `dataset_info.yaml` (`task_type`, taxonomy fallback,
  legacy `restoration` default), 2.32 Stochastic Weight Averaging (`swa.*`
  keys, off by default, `vault_swa.pth`, `swa_state.pth`) and 2.33 FID
  Re-evaluation Tool & Provenance Ledger (`python -m training.fid_reeval
  measure|mark-unverified|status`, `fid_provenance.csv`). The "SWA is not
  implemented" and "no re-evaluation tool exists yet" statements in the
  abstract, Sections 2, 2.27, 2.28 and 8.1 are corrected; Mini-SWA and MS-SWA
  stay not implemented. Training Pathology guide revision 1.6.0 (v16.9.107).
* **Dataset Compiler** (`PAPER_DATASET_COMPILER.md`, v16.9.64): new Section
  3.7 Task Taxonomy & Manifold Task Type (`task_taxonomy.json`, registry
  `task`, the four `task_confirmed: false` entries, `task_type` in
  `dataset_info.yaml`); API jobs run `python -m services.<module>` through
  `ServiceInvocation`; `POST /api/jobs/generic` removed (37 operations);
  `.pylintrc` has no disables.
* **Environment Manager** (`PAPER_ENV_MANAGER.md`, v16.9.58): `ecosystem_ssot`
  is an error-severity gate; the validation gates match the gate registry
  (Pylint, forbidden suppressions, absolute paths, fail-closed tools);
  `requires-python >=3.12`; upgrades install exactly the vetted versions with
  a `pip freeze` rollback. The Master CLI Manual gate list is rebuilt from the
  registry (the `stylelint` gate it listed does not exist) and has a new
  Section 6.12 for the FID re-evaluation tool.
* **AI Studio GUI** (v2.10.36): screen recording for bug reports (Windows,
  app window only, MP4 up to 60 s) replaces "planned" in the manual (Section
  13.6), whitepaper, control registry (recording controls, confirmation
  dialogs, `comp-mode-*` IDs), glossary, architecture and current state; the
  fallback model and dataset catalogs are documented as removed; the training
  status badge shows the sidecar verdict including `UNKNOWN`; Python 3.12+
  baseline.
* **Master API Manual**: `max_seq_length` removed from
  `POST /api/training/llm/train`; `training_status` lists `unknown` and the
  required `is_fully_trained`.
* **Current State, Glossary, Versioning Policy, Architecture**: component
  versions (Environment Manager v16.9.58, Dataset Compiler Suite v16.9.64,
  Model Training Suite v16.9.107, AI Studio GUI v2.10.36); the stale
  package-version drift note is replaced; new glossary terms 3.9 Task
  Taxonomy, 4.7 Stochastic Weight Averaging and 4.8 FID Provenance Ledger.
* **Registries** - both capability registries: new platform capabilities
  `stochastic_weight_averaging` and `fid_reevaluation`; screen recording
  implemented; model soup limitations updated; `ecosystem_ssot` error
  severity; operation counts (Environment Manager 33, Dataset Compiler 37);
  baselines updated. Manifest baselines for the seven papers above.
* **Version** - hub version v16.9.80 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML). HTML pages updated with the same
  changes as their Markdown sources.

### v16.9.79 - Strict YAML Lint (DOCS-2)

* **YAML** - every tracked YAML file passes `yamllint -s` with the new
  `.yamllint.yaml` (defaults, line length 120 as error, same as
  `lemgendary-env-manager`). `canonical_capabilities.yaml` was reindented
  (indented sequences, long BibTeX strings folded); its data equals
  `canonical_capabilities.json` (`registry-parity` passes).
* **Tooling** - `.gitattributes` forces LF for YAML; the pre-commit config
  has a new `yamllint` hook.
* **Version** - hub version v16.9.79 in `README.md`, `index.html`, manifest,
  both registries and the Current State and Versioning Policy documents
  (Markdown and HTML).

### v16.9.78 - Ecosystem Registry Checks and Documentation (DOCS-1)

* **Audit** - three new checks in `scripts/docs_audit/`:
  `registry-parity` (`canonical_capabilities.json` and `.yaml` hold the same
  data), `registry-models` (model ids equal the keys of the training registry
  `unified_models_v2.yaml`, without `_registry_metadata`) and `service-ports`
  (every model `api.port` equals the `training-suite` port and
  `control_planes.gui.ports` equal the service ports of
  `lemgendary-env-manager/ecosystem/ecosystem.json`). New module
  `docs_audit/workspace.py` resolves the sibling files from the workspace root
  (the parent of this repository, or `LEMGENDARY_WORKSPACE_ROOT`); the training
  folder is taken from `ecosystem.json`. A missing file is a finding that
  names the expected path and the variable.
* **Tests** - `test_cross_repo_manifest_and_runtime_consistency` reads the
  ports from `ecosystem.json` instead of literals (the 3 `ecosystem_ssot`
  findings in this repository are gone; the gate reports 0).
  `tests/test_docs_audit.py` uses a fixture workspace
  (`tests/fixtures/workspace/`) and has 7 new tests (registry drift, model
  drift, metadata key, API and GUI port drift, missing workspace, root
  resolution). 65 passed, 2 skipped.
* **Papers and Manuals** - the Environment Manager whitepaper has a new
  Section 6.7 Ecosystem Registry (file contents, `GET /api/ecosystem`, the
  Dataset Compiler and Training Suite `ecosystem` loaders, the GUI snapshot
  `src/generated/ecosystem.json`, the `ecosystem_ssot` gate) and notes that
  pipeline step names come from the file. The Master API Manual documents
  `GET /api/ecosystem` and where the server defaults and step names come
  from; Current State, Ecosystem Architecture, the AI Studio GUI whitepaper,
  the Dataset Compiler and the Training Suite papers say where ports, project
  lists, step names and the Kaggle owner live. HTML updated to match.
* **Registries** - new platform capability `ecosystem_registry` in both
  capability registries; `api-manual` audited 2026-11-03 in the manifest.
* **Version** - hub version v16.9.78 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML).

### v16.9.77 - Parity Backlog Cleared: Hub Index and Lint

* **Hub Index** - `index.html` now has the template's `nav.toc-sidebar`
  (a centered category bar linking to the 14 catalog cards, which carry
  `cat-NN` ids) and wraps the catalog in a `section`; `style.css` styles the
  hub bar (`.hub-page .hub-toc`). W3C (vnu) reports no errors or warnings on
  `index.html` and all 48 pages.
* **Markdown** - `INVESTOR_STRATEGY_LEMGENDARY_2026.md` rewrapped at 80
  columns and its wide tables rewritten as lists. markdownlint reports 0
  findings repository-wide with inline directives ignored (1957 at v16.9.70),
  and no `markdownlint-disable` directive remains.
* **Parity Backlog** - last entry removed (1 to 0); the backlog file stays,
  empty, and `README.md` no longer lists open drift.
* **Version** - hub version v16.9.77 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML).

### v16.9.76 - Parity Backlog Batch 6: Knowledge Bases

* **Approved Template** - `ai-helper-troubleshooting-knowledge` and
  `general-ai-training-knowledge` regenerated from their Markdown sources on
  the approved template (training tab bar; the AI Helper sidebar is built from
  its H2/H3 headings because the Markdown has no table of contents); W3C
  (vnu) clean.
* **Markdown** - `GENERAL_AI_TRAINING_KNOWLEDGE.md`: the inline directive
  disabling MD001, MD003, MD013, MD024, MD025 and MD035 is removed and the
  causes fixed: one H1 (section headings one level down, skipped levels
  closed), the five repeated sub-headings (Strengths, Weaknesses, Best use,
  ...) name their format, the four pandoc text tables (which rendered as
  setext headings) are lists, horizontal rules are `---`, prose is wrapped at
  80 columns. `AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md`: header on the approved
  layout, prose wrapped at 80 columns. markdownlint 0 on both files without
  inline directives. No technical claims changed.
* **Parity Backlog** - 3 entries removed (4 to 1: template 1, `index.html`).
* **Version** - hub version v16.9.76 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML).

### v16.9.75 - Parity Backlog Batch 5: Master API and CLI Manuals

* **Approved Template** - `api-manual` and `cli-manual` regenerated from
  `MANUAL_API.md` and `MANUAL_CLI.md` on the approved template (manuals tab
  bar); W3C (vnu) clean. The Markdown is a superset of the old HTML (it also
  documents `POST /api/hooks/install`, the notebook synthesis, Kaggle metadata
  and modernize endpoints), so no HTML content had to be ported back.
* **Markdown** - inline `markdownlint-disable` directives removed; prose
  rewrapped at 80 columns, wide tables rewritten as lists, long JSON example
  lines expanded over several lines, long shell commands split with `\`
  continuations and long comments over two lines. markdownlint 0 on both
  files without inline directives. No technical claims changed.
* **Audit** - the HTML parser now also leaves code blocks (`pre`) out of the
  compared prose, as the Markdown parser already skips fenced code; code
  inside `pre` keeps literal `"` so JSON examples read as in the Markdown.
  New test `test_code_block_is_not_prose` (58 passed, 2 skipped).
* **Parity Backlog** - 6 entries removed (10 to 4: heading parity 1,
  template 3, text similarity 0).
* **Version** - hub version v16.9.75 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML).

### v16.9.74 - Parity Backlog Batch 4: Suite Masters, Manuals Hub and Policy

* **Approved Template** - `nima-master`, `restoration-master`, `ultrazoom`,
  `versioning-policy` and `manuals-hub` regenerated from their Markdown
  sources on the approved template with family tab bars; W3C (vnu) clean.
  The Markdown stays the source of truth: HTML-only material in these pages
  (older benchmark and latency figures in `ultrazoom.html`, longer prose in
  the suite masters and the manuals hub) was not newer than the Markdown and
  is replaced by the Markdown content.
* **Markdown** - inline `markdownlint-disable` directives removed; prose
  rewrapped at 80 columns, display math split into `$$` blocks, wide tables
  rewritten as lists, headers on the approved layout. markdownlint 0 on the
  five files without inline directives. No technical claims changed.
* **Audit** - the HTML parser now leaves display math (`div.math-block`) out
  of the compared prose, as the Markdown parser already skips `$$` blocks;
  math-heavy pages such as `degradation-engine` no longer read as text drift.
  New test `test_display_math_is_not_prose` (57 passed, 2 skipped).
* **Parity Backlog** - 15 entries removed (25 to 10: heading parity 3,
  template 5, text similarity 2).
* **Version** - hub version v16.9.74 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML).

### v16.9.73 - Parity Backlog Batch 3: Model Specifications and Engine Paper

* **Approved Template** - `degradation-engine`, `detection-classification`,
  `detection-yolov8n`, `foundation-models-master`, `restoration-suite`,
  `mprnet`, `nafnet`, `nima-quality` and `forex_predictor` regenerated from
  their Markdown sources on the approved template with family tab bars.
  Headings and prose match the Markdown (the shorter HTML pages for the
  degradation engine, detection, YOLOv8n, foundation and restoration suite
  now carry the full Markdown content); W3C (vnu) clean.
* **Markdown** - inline `markdownlint-disable` directives removed from the
  nine sources; prose rewrapped at 80 columns, display math split into `$$`
  blocks, wide tables rewritten as lists, headers on the approved layout.
  markdownlint 0 on all nine files without inline directives. No technical
  claims changed.
* **Parity Backlog** - 22 entries removed (47 to 25: heading parity 8,
  template 10, text similarity 7).
* **Version** - hub version v16.9.73 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML).

### v16.9.72 - Parity Backlog Batch 2: Face, Hybrid and Restoration Papers

* **Approved Template** - `face-codeformer`, `face-parsenet`,
  `face-retinaface`, `face-suite`, `hybrid-upn-v2`, `hybrid-film-restorer`,
  `hybrid-multitask`, `universal-hybrid`, `ffanet` and `mirnet` regenerated
  from their Markdown sources on the approved template with family tab bars.
  Headings and prose match the Markdown; W3C (vnu) clean. The Markdown is the
  source of truth: HTML-only presentation (comparison cards, duplicated
  training-curve sub-sections) is replaced by the Markdown content.
* **Markdown** - inline `markdownlint-disable` directives removed from the ten
  sources; prose rewrapped at 80 columns, display math split into `$$`
  blocks, wide tables rewritten as lists, headers on the approved layout.
  markdownlint 0 on all ten files without inline directives. No technical
  claims changed.
* **Parity Backlog** - 21 entries removed (68 to 47: heading parity 17,
  template 19, text similarity 11).
* **Version** - hub version v16.9.72 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML).

### v16.9.71 - Parity Backlog Batch 1: Quality, Foundation and Vision Papers

* **Approved Template** - `nima-mobile`, `nima-efficientnet`, `nima-pro`,
  `nima-technical`, `nima-authenticity`, `foundation-diffusion`,
  `foundation-image-to-text`, `foundation-llm`, `detection-master` and
  `classification-nsfw` regenerated from their Markdown sources on the
  approved template (`header`, `nav.toc-sidebar`, `section`, `footer`, family
  tab bar). Headings and prose now match the Markdown exactly; W3C (vnu) clean.
* **Markdown** - inline `markdownlint-disable` directives removed from the ten
  sources; prose rewrapped at 80 columns, one-line display math split into
  `$$` blocks, tables wider than 80 columns rewritten as lists. Headers use the
  `# Title` / `## Category ... | Series` / meta-line layout (the
  "Architecture of LemGendary AI" prefix moved to the subtitle). markdownlint
  0 on all ten files without inline directives. No technical claims changed.
* **Parity Backlog** - 20 entries removed (88 to 68: heading parity 27,
  template 29, text similarity 12).
* **Version** - hub version v16.9.71 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML).

### v16.9.70 - Strict Documentation Audit, Test Fixes and Lint Config

* **One Audit Module** - `scripts/audit_parity.py` and
  `scripts/audit_deep_parity.py` (H2 counts, image sets and length ratios
  only; 0 of 48 flagged; worked only from the workspace root) replaced by the
  `scripts/docs_audit/` package and one entry point, `scripts/audit_docs.py`.
  Paths resolve from `Path(__file__)`, so it runs from any directory. Checks:
  manifest paths and unlisted pages, hub version (README, `index.html`,
  manifest, both registries), document version lines, MD/HTML heading list
  (level, text and order), MD/HTML text similarity (at least 0.85), approved
  template elements, internal links and anchors, absolute paths, canonical
  project names. Exit code 1 on any finding.
* **Parity Backlog** - existing drift is recorded in
  `scripts/parity_backlog.json` (88 entries: heading parity 37, template 39,
  text similarity 12) and reported as known backlog for the Later Phase. New
  drift fails, and an entry whose drift is fixed fails as stale until it is
  removed, so the list only shrinks.
* **Pre-Commit Hook** - `.pre-commit-config.yaml` called the nonexistent
  `verify_docs.py`; it now runs `python scripts/audit_docs.py`. The
  `.githooks/pre-commit` hook runs the audit after the test suite.
* **Tests** - port messages corrected (8000 LemGendary Environment Manager,
  8100 LemGendary Dataset Compiler Suite, 8200 LemGendary Model Training
  Suite); the working-directory fallback in `setUpClass` removed; the two AI
  Helper corpus tests skip with an explicit reason when the LemGendary
  Compiled Manifolds Repo (`../LemGendaryDatasets`) is not checked out
  (one used to pass silently, the other failed); the companion test reads the
  manifest instead of a copied map. New `tests/test_docs_audit.py` (20 tests)
  covers each check on synthetic MD/HTML pairs, the backlog and the CLI. Result:
  56 passed, 2 skipped.
* **Lint Config** - `.markdownlint.json` is tracked (no longer gitignored):
  default rules, `MD013` at 80 columns, nothing disabled. This README is
  rewrapped to 80 columns and 30 long changelog headings are shortened;
  markdownlint 0 on README. Repository-wide: 639 findings (all `MD013`, in 7
  files) with inline directives honoured, 1957 without them (Later Phase).
* **Version** - hub version v16.9.70 in `README.md`, `index.html`, manifest,
  both capability registries, `VERSIONING_POLICY.md` and
  `LEMGENDARY_CURRENT_STATE.md` (+ HTML).

### v16.9.69 - Hub Versions, Links, Paths and Canonical Names

* **Version Split** - Hub version is v16.9.69 in `README.md`, `index.html`
  (Last Reviewed 2026-11-03), `manifest/documents.json`, both capability
  registries, `VERSIONING_POLICY.md` and `LEMGENDARY_CURRENT_STATE.md` (+ HTML).
  Every Markdown and HTML version line now equals its manifest
  `baseline_version` (37 documents fixed, version lines added to 5 Markdown and
  1 HTML file). Paper-local releases moved to a separate **Paper Revision**
  line; `VERSIONING_POLICY.md` states this rule and lists current component
  versions. The header test reads the version from this README.
* **Links and Anchors** - 0 broken links: 34 Markdown TOC fragments, 4
  Markdown companion links (now `../papers/*.html`), 4 HTML anchors in
  `ultrazoom.html` and the corrupted UltraZoom TOC entry. Three display-math
  blocks in the Film Restorer and UPN v2 papers that hid later headings now
  use `$$` fence lines. `MD051` removed from 31 inline `markdownlint-disable`
  comments.
* **Absolute Paths** - MetaTrader 5 install paths in the API and CLI manuals
  (+ HTML) now use `%ProgramFiles%`; the v16.9.62 note no longer quotes a
  drive-rooted `file:` URI. 0 absolute paths remain.
* **Canonical Names** - 46 aliases replaced ("AI Studio Desktop GUI",
  "LemGendary Training Suite", "LemGendary AI Studio", "LemGendary Dataset
  Compiler") in Markdown and HTML; index copyright reads "LemGendary AI
  Documentation Hub"; LemGendary Compiled Manifolds Repo named in the
  architecture, glossary and current-state documents.
* **W3C** - fixed 4 errors (unescaped `<` in the AI helper and Forex pages,
  duplicate `class` in `mirnet.html`).

### v16.9.68 - Capability Registries, Manifest, Glossary and Current State Sync

* **Capability Registries** - `canonical_capabilities.json` and `.yaml`
  (identical after parsing): baselines updated (documents v16.9.68, Model
  Training Suite v16.9.68, AI Studio GUI v2.10.19, Dataset Compiler Suite
  v16.9.27, new Environment Manager v16.9.18), audited 2026-11-03. Removed the
  nonexistent `POST /v16/train/start` (now `POST /api/training/train`; LLM:
  `POST /api/training/llm/train`); CLI syntax fixed to `lemtrain train
  MODEL_KEY` and `lemtrain llm train`; CLI engine is Typer; 14 model categories
  aligned with `unified_models_v2.yaml` and a `registry_status` field added;
  manifold formats follow the registry (`parquet` for `forex_predictor`,
  `directory` for `yolov8n`); GUI IDs point to `train-btn-start-{model_key}`.
  New `platform_capabilities`: `bug_reporting` (env manager
  `POST /api/bug-report`, local ZIP plus mail client, at most 5 screenshots,
  Telemetry CSV, recording planned), `security_contract` (Origin Guard, Client
  Header, masked secrets) and `model_soup` (SWA not implemented).
* **Document Manifest** - `manifest/documents.json` baseline v16.9.68, audited
  2026-11-03. Titles, versions and audit dates for the GUI documents (v2.10.19),
  Environment Manager (v16.9.18), Ecosystem Architecture (v16.9.65), Dataset
  Compiler Suite (v16.9.27), Model Training Suite and pathology guide
  (v16.9.68), glossary and current state. Category collisions fixed: Environment
  Manager 01.1 ENV, Dataset Compiler Suite 01.2 DATASET, Degradation Engine
  01.6 ENGINE (Markdown and HTML updated), AI Studio GUI whitepaper 01.4 GUI,
  GUI Control Registry 03.4 CONTROLS. All 48 entries point to existing files.
* **Glossary** - `GLOSSARY.md` and `papers/glossary.html` rebuilt on the
  approved template ("1. Abstract", TOC, wrapped lines, matrix as a list); new
  terms Ratchet Violation, Epoch Budget, Origin Guard, Client Header, Bug Report
  Tool, Bug Report Archive, Screenshot Annotator and Telemetry CSV.
* **Current State** - `LEMGENDARY_CURRENT_STATE.md` and
  `papers/current-state.html` on the approved template; Section 1 is now
  "1. Abstract"; versioning matrix and feature list updated (security
  contract, bug reporting, pair-rule ratchet, epoch budget, model soup, 23
  models, 4-pillar invariant, known package-version drift); FID unverified note
  for `codeformer`, `ffanet_indoor`, `mprnet_deraining` and `mirnet_lowlight`.
* **Environment Manager paper** - category banner reads "Category 01.1 ENV",
  which fixes `test_category_taxonomy_uniqueness`.

### v16.9.67 - Model Training Suite v16.9.68 Paper Sync (Pair-Rule Ratchet)

* **Training Suite Whitepaper** - `PAPER_TRAINING_SUITE.md` and
  `papers/training-suite-master.html` retitled "LemGendary Model Training
  Suite: Technical Whitepaper" and synced with training suite v16.9.68. New
  sections 2.25 to 2.29: pair-rule Monotonic Ratchet with the enforced
  `RatchetViolation` guard (`_commit_rung`), bounded epoch budget with honoured
  early stop (`training_budget`, stop reasons), Pareto Model Soup service (CLI
  and API, what the blend does and does not do; SWA is not implemented),
  publication-grade FID (`feature=2048`, chunks of at most two) and the sidecar
  security model with the 40-operation `openapi.json`. Section 4 regenerated
  from `unified_models_v2.yaml` (23 models); new 8.1 Implementation Status.
* **Pathology Guide** - `PAPER_TRAINING_PATHOLOGY.md` and
  `papers/training-pathology.html` revision 1.5.0: header and TOC on the
  standard layout, wide tables turned into lists, Pathology 26 (unbounded epoch
  horizon) and 27 (fabricated FID history) added, registry-accurate model
  groups (diffusion and VLM groups marked as planned).
* **Corrected Claims** - removed the intra-resolution fraction recoil and the
  early-epoch fraction override (both broke the ratchet); 4-pillar epochs 20
  (not 30); `maturity_soak` 5; FID `feature=2048` (not 64); rollback
  registration, loop-breaker, resolution-jump veto, dry-run probe and Mini-SWA
  marked as not active, absolute patience, validation sharding, SWA and MS-SWA
  as not implemented. Historical FID rows of `codeformer`, `ffanet_indoor`,
  `mprnet_deraining` and `mirnet_lowlight` are marked unverified; no
  replacement numbers.
* **Lint & HTML** - inline `markdownlint-disable` comments removed and the
  hidden issues fixed (TOC anchors, line length, duplicate headings); both
  HTML files rebuilt on the approved template with MathJax. markdownlint 0,
  W3C 0, anchors resolve, MD/HTML headings identical (52 and 53).

### v16.9.66 - Dataset Compiler Suite v16.9.27 Whitepaper Sync

* **Dataset Compiler Whitepaper** - `PAPER_DATASET_COMPILER.md` and
  `papers/dataset-compiler.html` describe release v16.9.27 in exactly the eight
  framework sections. The former section 5 (modernization) is folded into
  sections 2, 3, 4 and 6; the former section 9 (LLM compiler) into 4.10 and
  6.3; the Conclusion is section 8.
* **New Behaviour** - default preset from `presets.yaml`, atomic registry
  writes with HTTP 409/422/500, purge only after a successful compile, async
  LLM jobs with a bounded CLI wait, modernize and reduce scope and dry-run
  guarantees, origin guard and closed CORS, dataset-root confinement for
  `llm validate`, and the regenerated `openapi.json` (38 operations).
* **Corrected Claims** - 21 registry manifolds (not 22), all vision containers
  except YoloV8n on WebDataset (no `mds`), canonical folder names
  (`LemGendizedRetinaFace`, `LemGendizedMultitaskRestorationPro`),
  `KnowledgeIngestor`, chunk `sha256`, 1200/200 chunking, stratified 80/20
  split, validator rules as coded, resolution floors from
  `audit/vision_audit.py`,
  WebP quality on streaming download, removed modules and the nonexistent
  `compile_all` and `_read_stream`. Added the `rain`, `lowlight`, `downsample`
  and `film` filters and the `modernize`, `llm`, `forex`, `test` and
  `sync metadata` CLI groups. Benchmark figures marked as historical.
* **HTML Template** - Regenerated from the Markdown with the approved template
  and MathJax. W3C valid, markdownlint clean, MD and HTML heading lists
  identical.

### v16.9.65 - Environment Manager v16.9.18 and Ecosystem Architecture Sync

* **Environment Manager Whitepaper** - `PAPER_ENV_MANAGER.md` and
  `papers/env_manager.html` describe release v16.9.18: driver-aware PyTorch
  index (`cu126`, `cu121`, `cu118`) instead of a fixed `cu121`, one-way manifest
  sync with the downgrade guard instead of "bidirectional" mirroring (all six
  central manifests listed), fail-closed pip parsing, non-destructive pipeline
  with opt-in `--clean`, Step 5 routing by project metadata, Python 3.12 as the
  effective minimum, validator and sidecar probe descriptions matching the code.
  Sections renumbered to the framework ordering (8 sections); new 6.4
  Background Update Jobs, 6.5 Security Model and 6.6 Bug Report Endpoint before
  the Conclusion. Benchmark latencies marked as historical `v16.8.0` values.
* **Ecosystem Architecture** - Section 1 is "1. Abstract"; table of contents,
  component versions, sidecar responsibilities (`/api/ping`, update jobs,
  masked secrets, bug report, optional training token), corrected invariants
  (Python contract, `.pylintrc`, MosaicML status, `torch==2.15.0` on `cu126`,
  pair-rule ratchet), new sections 6 Cross-Repository Security Contract, 7 Bug
  Reporting Flow and 8 Conclusion.
* **HTML Template** - Both pages regenerated from the Markdown with the approved
  template; mermaid pinned to 10.9.1. W3C valid, markdownlint clean, MD and HTML
  heading lists identical.

### v16.9.64 - LemGendary AI Studio GUI v2.10.19 Documentation Sync

* **GUI Control Registry Rebuilt from Code** - `GUI_CONTROL_REGISTRY.md` and
  `papers/gui-control-registry.html` now list the 119 `id` attributes of GUI
  release v2.10.19 (75 controls, 44 dialogs, status regions and headings). 54
  stale IDs removed, 98 added; endpoints corrected (`GET /api/ping` liveness,
  `POST /api/pipeline/run` with `clean`, `POST /api/bug-report`, masked `GET
  /api/secrets`).
* **Operator Manual** - New chapter 13 "Reporting an Issue" (annotated
  screenshots, telemetry CSV, local ZIP report and mail client; screen recording
  marked as planned). Tests & Diagnostics header button, Clean Install
  confirmation dialog, write-only secrets, offline placeholders, Documentation
  Hub button served by the Environment Manager. Removed the "Unit Test All
  Models" toolbar button and the `lem-env validate --all` flag, which do not
  exist.
* **Architectural Whitepaper** - Version v2.10.19; new sections 6.12 Security
  Model (origin guard, client header, Content Security Policy, masked secrets)
  and 6.13 Bug Reporting Subsystem, placed before the Conclusion; references to
  nonexistent files and dependencies removed.
* **HTML Template** - The three HTML pages are generated from the Markdown with
  the approved template (`header`, `nav.toc-sidebar`, `section`, `footer`) and
  validate with the W3C Nu validator; Markdown passes markdownlint.

### v16.9.64 - LLM Training Pathology, Hardware Probing & Vault Whitepapers

* **Training Pathology Master Guide (`PAPER_TRAINING_PATHOLOGY.md`)** -
  Documented Pathologies 26 through 30 (numbered 28 to 32 since v16.9.82)
  covering variable-length validation collation collapse, CPU-bound
  accelerator starvation, vision-curriculum cross-contamination, symbolic
  tracing artifacts on dynamic causal masks, and disconnected LLM milestone
  vault tracking.
* **Causal LLM Whitepaper Expansion (`PAPER_LEMGENDARY_LLM.md`)** - Added
  mathematical formulations for QLoRA dynamic quantization, hardware-aware
  gradient accumulation decoupling, autoregressive non-masked token accuracy,
  and Pareto milestone vault ensembling.
* **Training Suite Master Guide (`PAPER_TRAINING_SUITE.md`)** - Added Section
  2.25 (Section 2.35 since v16.9.82) formalizing causal language model
  instruction tuning, empirical VRAM safety boundaries, and vault milestone
  persistence.

### v16.9.63 - Tripartite Sidecar Termination & UI Control Alignment

* **Tripartite Sidecar Lifecycle Documentation** - Updated system operations
  documentation to reflect bidirectional daemon control over all three sidecar
  ports (8000, 8100, 8200) directly from desktop GUI action tiles.
* **UI Test Control Streamlining** - Synchronized documentation specifications
  to reflect the removal of redundant header and toolbar test buttons in favor
  of dedicated panel workflows.

### v16.9.62 - Absolute Paths Elimination & Relative Link Governance

* **Universal Relative Path Normalization** - Converted all legacy drive-rooted
  `file:` URI links across 34 Markdown whitepapers and `MANUAL_API.md` payload
  specifications into clean, portable relative paths (`./`, `../`).

### v16.9.61 - Pipeline Step 5 Safe Dependency Upgrade Execution Specification

* **Pipeline Step 5 Active Safe Upgrade Specification** - Synchronized
  MANUAL_AI_STUDIO_GUI.md, ai-studio-manual.html, and GUI control documentation
  to reflect active bottom-up safe package upgrade execution in Pipeline Step 5.

### v16.9.60 - Generic LLM, In-Process Test Orchestrator & Publication Sync

* **Generic LLM Compiler & Instruction Tuning Documentation Synchronization** -
  Synchronized PAPER_DATASET_COMPILER.md and dataset-compiler.html with Section
  9 "Generic LLM Dataset Compiler Architecture & Multi-Source Knowledge
  Ingestion", and PAPER_TRAINING_SUITE.md and training-suite-master.html with
  Section 7 "Universal Instruction-Tuned Causal LLM Fine-Tuning & Dynamic
  Dataset Ingestion".
* **Test & Diagnostic Orchestration Parity Across Entire Documentation Suite** -
  Updated MANUAL_CLI.md, cli-manual.html, MANUAL_API.md, api-manual.html,
  MANUAL_AI_STUDIO_GUI.md, ai-studio-manual.html, PAPER_AI_STUDIO_GUI.md,
  ai-studio-whitepaper.html, GUI_CONTROL_REGISTRY.md, and
  gui-control-registry.html with full specifications for in-process test
  discovery sweeps, fleet smoke tests, and the GUI TestModal.
* **Bijective Document Manifest Baseline Audit** - Synchronized
  manifest/documents.json to document_baseline v16.9.60-STABLE, last_audited
  2026-11-02 across all 48 authoritative publications with 100% heading and
  table parity.

---

### v16.9.59 - Training Hardening, Pareto Model Soup & Manual Parity

* **Pareto Model Soup Documentation Parity** - Updated MANUAL_CLI.md,
  cli-manual.html, MANUAL_API.md, api-manual.html, MANUAL_AI_STUDIO_GUI.md, and
  ai-studio-manual.html with complete specifications for CLI soup, REST endpoint
  POST /api/models/{model_key}/soup, and GUI client method
  blendModelSoup(modelKey).
* **Training Suite Whitepaper Master Synchronization** - Updated
  PAPER_TRAINING_SUITE.md and companion publication training-suite-master.html
  reflecting realistic FID Inception-2048 calibration, OOM safeguard ratchets,
  Pareto Model Soup blending, dual Kaggle secret retrieval (GOOGLE_DRIVE +
  GOOGLE_DRIVE_JSON), and modular notebook architecture.
* **Canonical Capabilities & Documents Registry Sync** - Synchronized
  canonical_capabilities.json, canonical_capabilities.yaml, and
  manifest/documents.json with updated audit dates and canonical version
  baselines.

---

### v16.9.44 — GUI Screenshot Suite, Sidecar Port Realignment & 6-Pair Sync

* **Authoritative GUI Figures Integrity Verification (`assets/gui/`)** —
  Verified all 19 official figures against the live desktop application
  topology, guaranteeing full card bounding, online hardware telemetry,
  cross-project drift matrix data, and numbered circular callout badges (1–11)
  matching `MANUAL_AI_STUDIO_GUI.md` and `ai-studio-manual.html` references.
* **Bijective Markdown & HTML Manual/Whitepaper 6-Pair Synchronization** —
  Synchronized all 6 primary manual and whitepaper pairs 1-to-1:
  * `MANUAL_AI_STUDIO_GUI.md` <-> `ai-studio-manual.html`
  * `MANUAL_API.md` <-> `api-manual.html` (Added Section 5.7 Ingestion Pipelines
    and Section 5.8 Python Services)
  * `MANUAL_CLI.md` <-> `cli-manual.html` (Standardized canonical
    `LemGendizedMirNetExposure` and `LemGendizedUpnV2` paths)
  * `PAPER_AI_STUDIO_GUI.md` <-> `ai-studio-whitepaper.html`
  * `PAPER_DATASET_COMPILER.md` <-> `dataset-compiler.html`
  * `PAPER_TRAINING_SUITE.md` <-> `training-suite-master.html`
* **Canonical Capabilities & Manifest Alignment (`canonical_capabilities.json`,
  `canonical_capabilities.yaml`, `manifest/documents.json`)** — Updated
  `last_audited` to `2026-10-28`, set `document_baseline` and
  `runtime_engine_baseline` to `v16.9.44-STABLE`, set `desktop_client_baseline`
  to `v2.10.2`, and aligned tripartite sidecar ports: Environment Manager
  (`8000`), Dataset Compiler (`8100`), and Training Suite (`8200`).
* **Automated Documentation Integrity Verification** — All 48 document pairs
  verified on disk with 0 broken links, 100% W3C HTML compliance, zero
  suppressions, and zero emojis.

---

### v16.9.43 — Data Fraction Progression & Checkpoint Resumption Fidelity

* **Master Training Suite Whitepaper & HTML Synchronization
  (`PAPER_TRAINING_SUITE.md`, `training-suite-master.html`)** — Synchronized
  Section 2.3 (Hardened Resolution Ladders & SOTA Guards) and Section 2.4
  (Checkpoint Resumption & Singularity Hardening) to document steady-improvement
  soak propulsion (`fraction_soak_complete` and `deepening_ready` across 3-epoch
  `manifold_maturity` windows), pre-guard `epoch_count` restoration in
  `SmartTrainingGovernor.load_state()`, `metrics.csv` curriculum reconciliation
  on resume, post-audit checkpoint persistence in `run_training`, and in-memory
  manifold slicing (`random.Random(42)`) across `MultiTaskDataset` and
  `InstructionDataset`.
* **Automated Documentation Integrity Verification** — All 38 documentation
  validation gates passing in `tests/test_documentation.py` with 100% W3C HTML
  compliance, zero markdownlint errors, zero broken links, and zero emojis.

---

### v16.9.36 — 20-Epoch Convergence Floor & LLM Context Window

* **Master Training Suite Whitepaper & HTML Synchronization
  (`PAPER_TRAINING_SUITE.md`, `training-suite-master.html`)** — Calibrated the
  authoritative Pillar 4 convergence floor from 30 epochs down to 20 epochs
  across Section 2.3.1 and Section 2.14. Specialized Pillar 2 (Complete
  Resolution / Confluence / Context Ladder Traversal) to mandate full target
  sequence length ($\text{seq\_length} \ge 2048\text{ tokens}$) for Causal LLM
  assistants, and Pillar 3 to mandate full instruction tuning manifold traversal
  without spatial cropping constraints.
* **AI Studio GUI Operator Manual & HTML Synchronization
  (`MANUAL_AI_STUDIO_GUI.md`, `ai-studio-manual.html`)** — Documented the
  domain-specific telemetry row specialization in Section 6.2 (Architecture
  Telemetry Card): updated Row 9 to document `Context Window: 2048 tokens
  (Full)` for causal LLMs alongside spatial and timeframe confluence ladders,
  and Row 10 to document `Training Dataset: LemGendizedAIHelperLemGend`
  alongside fractional vision samplers and walk-forward forex folds.
* **Automated Documentation Integrity Verification** — All 38 documentation
  validation gates passing in `tests/test_documentation.py` with 100% W3C HTML
  compliance, zero markdownlint errors, zero broken links, and zero emojis.

---

### v16.9.35 — Horizon Runway Extension & 1-Indexed Epoch Telemetry

* **Master Training Suite Whitepaper & HTML Synchronization
  (`PAPER_TRAINING_SUITE.md`, `training-suite-master.html`)** — Documented
  dynamic horizon runway extension (`stage_total_epochs = max(total_epochs,
  stage_start_epoch + 100)`), strict historical checkpoint-to-telemetry anchor
  parity (`max(stage_start_epoch, csv_epochs)`), and telemetry 1-indexed epoch
  serialization in Section 2.4 (Checkpoint Resumption & Singularity Hardening).
* **Automated Documentation Integrity Verification** — All 38 documentation
  validation gates passing in `tests/test_documentation.py` with 100% W3C HTML
  compliance, zero markdownlint errors, zero broken links, and zero emojis.

---

### v16.9.34 — YOLO PyTorch 2.6 Deserialization & Telemetry Epoch Anchoring

* **Master Training Suite Whitepaper & HTML Synchronization
  (`PAPER_TRAINING_SUITE.md`, `training-suite-master.html`)** — Synchronized
  Section 2.4 (Checkpoint Resumption & Singularity Hardening) and Section 2.14
  (Autonomous YOLO Multi-Stage Curriculum Governor & SOTA Target Convergence).
  Documented the PyTorch 2.6+ `weights_only=False` fallback unpickling guard for
  Ultralytics `DetectionModel` checkpoints and cumulative historical epoch
  recovery (`completed_prior_epochs = max(completed_prior_epochs, csv_epochs)`).
* **AI Studio GUI Documentation Synchronization (`MANUAL_AI_STUDIO_GUI.md`,
  `PAPER_AI_STUDIO_GUI.md`)** — Documented tqdm/Ultralytics `<remaining` ETA
  parsing and log timestamp prefix sanitization in `progressParser.ts`.
* **Automated Documentation Integrity Verification** — All 38 documentation
  validation gates passing in `tests/test_documentation.py` with 100% W3C HTML
  compliance, zero markdownlint errors, zero broken links, and zero emojis.

---

### v16.9.32 — 4-Pillar Fully-Trained Invariant & SOTA Matrix Sync

* **Master Training Suite Whitepaper & HTML Synchronization
  (`PAPER_TRAINING_SUITE.md`, `training-suite-master.html`)** — Expanded formal
  model graduation criteria from 3 to 4 pillars in Section 2.3.1. Documented the
  strict mathematical formulation requiring multi-metric SOTA target
  satisfaction, full resolution ladder traversal, 100% dataset variety
  ($D_{\text{fraction}} \ge 1.0$), and minimum epoch convergence threshold
  ($\text{Epochs} \ge 30$).
* **Authoritative Hub Readme Generator (`LemGendaryModels/README.md`)** —
  Synchronized model cards and status matrix. Models with fewer than 30
  completed epochs are strictly classified as In Progress until full
  mathematical convergence is achieved.
* **Automated Integrity Verification** — All 38 documentation validation gates
  passing in `tests/test_documentation.py` with 100% W3C HTML compliance, zero
  markdownlint errors, zero broken links, and zero emojis.

---

### v16.9.29 — Hub Inventory Alignment (48 Publications) & Directory Overview

* **Publication Inventory Reconciliation (`README.md`)** — Updated directory
  overview count from 46 to 48 W3C-compliant standalone HTML/Markdown
  publications, exactly matching `manifest/documents.json`.
* **Directory Structure Alignment (`README.md`)** — Replaced non-existent
  roadmap directory reference with active `manifest/` (machine-readable 1-to-1
  document pairing catalog) and `tests/` (automated 38-rule documentation
  verification suite).
* **Automated Integrity Verification** — All 38 automated test gates in
  `tests/test_documentation.py` passing with zero warnings and strict zero-emoji
  compliance.

---

### v16.9.28 — Requirements Progress Bar & Subprocess Telemetry Paper Sync

* **Environment Manager Whitepaper (`PAPER_ENV_MANAGER.md`,
  `env_manager.html`)** — Documented unbuffered real-time stdout streaming via
  `stream_pip_with_recovery`, `stream_npm_install`, and
  `stream_install_requirements` using `PYTHONUNBUFFERED="1"` and `--progress-bar
  on`. Documented real-time regex parsing of wheel download metrics, requirement
  progress ratios (`[k/N requirements]`), and typed progress event emissions
  (`is_progress=True`) in Section 7.1.
* **AI Studio GUI Whitepaper (`PAPER_AI_STUDIO_GUI.md`,
  `ai-studio-whitepaper.html`)** — Documented in-place terminal event roll-up
  (`rollupTelemetryEvents`, `isProgressLine`) extended to package installation
  lines and the accessible `TelemetryProgressTracker` with amber pipeline theme
  in Section 6.1.
* **AI Studio GUI Operator Manual (`MANUAL_AI_STUDIO_GUI.md`,
  `ai-studio-manual.html`)** — Added dedicated Section 4.1 subsection
  documenting the real-time requirements progress bar, package download speeds,
  ETA countdowns, and card-level animated progress bars on executing pipeline
  steps.
* **Automated Integrity Verification** — Re-validated all documentation
  integrity gates in `tests/test_documentation.py` passing with zero warnings
  and strict zero-emoji compliance.

---

### v16.9.27 — AI Studio Manual Formatting, Badging & Screenshot Audit

* **Section 4.2 Individual Pipeline Step Cards Audit** — Captured complete
  7-stage cards grid (`gui_pipeline_step_cards.png`) badging all 7 stages with
  14 distinct callouts (card titles and isolated run buttons). Documented Step 5
  (Dependency Audit & Upgrades), Step 6 (Codebase Verification), and Step 7
  (Health Matrix) in both HTML and Markdown manuals.
* **Section 4.3 Hardware Sentinel Scaling** — Scaled Hardware Acceleration
  Sentinel card image down by 50% (`.img-paper-50`, `max-width: 525px;`).
* **Section 5.2 Production Manifolds Header & Margins** — Recaptured Production
  Manifolds catalog screenshot (`gui_production_manifolds.png`) with scroll
  offset and 20px padding margins, eliminating header and badge clipping.
  Harmonized reference list and table to 7 unified badges.
* **Section 6.1 Training Orchestration Toolbar Controls & Fleet Push Action** —
  Recaptured Training Orchestration Toolbar screenshot
  (`gui_training_orchestrator.png`) badged with 8 distinct callouts for all 4
  inputs/dropdowns (Search, Status, Category, Architecture) and all 4 fleet
  action buttons (Unit Test All Models, Generate All Notebooks, Push All Models
  to Kaggle, Refresh Models) with zero text occlusion. Fully documented in HTML
  and Markdown manuals.
* **Section 6.2 Architecture Telemetry All Rows & Buttons Numbering & Scaling**
  — Recaptured neural architecture card screenshot
  (`gui_architecture_telemetry.png`) including full card header, model title,
  and pin button. Scaled image down by 50% (`.img-paper-50`). Numbered every
  single row (1–10) and action button (11–21) with 21 distinct badges, fully
  referenced and documented in HTML and Markdown tables.
* **Section 6.4 Training Dashboard Filter Section Callout** — Recaptured
  Training Dashboard topology screenshot (`gui_training_panel_overview.png`)
  badging all 5 key dashboard sections (Toolbar, Filter/Search, Card Grid, SOTA
  Target Popover, Execution Triggers) with zero text clipping. Documented in
  HTML and Markdown manuals.
* **Section 7.3 Fleet Push to Kaggle Integration & Publishing Modal Numbering**
  — Recaptured Cloud & Registry Dispatch modal (`gui_model_export_publish.png`)
  tightly cropped, scaled down by 30% (`.img-paper-70`), and numbered with 17
  distinct badges covering all buttons, dropdowns, and pre-flight verification
  rows. Documented fleet-wide Kaggle Models synchronization (`POST
  /api/training/kaggle/push-all`, `lemtrain sync push --all`).
* **Section 8.2 Ecosystem Maintenance Controls Screenshot** — Captured and
  integrated dedicated numbered screenshot (`gui_ecosystem_maintenance.png`)
  with 5 action button badges into Section 8.2 across HTML and Markdown manuals.
* **Section 9 Contextual Help Popover Scaling** — Scaled contextual help popover
  screenshot (`gui_contextual_help_popover.png`) down by 50% (`.img-paper-50`,
  `max-width: 525px;`).
* **API, CLI & Control Registry Synchronization** — Documented `POST
  /api/training/kaggle/push-all` across `MANUAL_API.md` and `api-manual.html`;
  documented `lemtrain sync push --all` across `MANUAL_CLI.md` and
  `cli-manual.html`; registered `training-toolbar-push-all-models-btn` in
  `GUI_CONTROL_REGISTRY.md` and `gui-control-registry.html`.
* **Automated Integrity Verification & Documentation Hub Audit Remediation** —
  All 38 automated documentation test gates in `tests/test_documentation.py`
  passing with zero warnings and 100% zero-emoji compliance. Established
  machine-readable `manifest/documents.json` pairing all 48 HTML publications
  1-to-1 with Markdown companions; purged third-party external CDN fallback
  references; synchronized hub header, baseline manifests, and manuals to
  `v16.9.27-STABLE` reviewed 2026-10-17.

---

### v16.9.26 — Hub Audit Remediation & 32-Rule Test Suite Expansion

* **Mathematical Delimiter & LaTeX Corruption Purge** — Eradicated corrupted
  `\|^2\right]` regex escape artifacts and malformed delimiters across scaling
  laws, VRAM capacity equations, and diffusion transition dynamics in
  `foundation-models-master.html`. Standardized MathJax configuration
  delimiters.
* **VLM Cross-Entropy Equation Integrity** — Replaced unescaped `<t` and `<i`
  operators with `\lt t` and `\lt i` in `foundation-image-to-text.html`,
  `foundation-models-master.html`, and companion markdown, preventing browser
  HTML tag truncation and rendering complete autoregressive loss
  $\mathcal{L}_{\text{VLM}} = -\sum_{t=1}^T \log P_\theta(w_t \mid w_{\lt t},
  Z)$.
* **Gated SwiGLU Formulation Correction** — Replaced single-matrix placeholder
  with the dual-projection gated formulation $\text{SwiGLU}(x) = (\text{Swish}(x
  W_1) \odot (x W_2)) W_3$ in `foundation-llm.html` and companion markdown,
  qualifying PagedAttention non-contiguous memory claims.
* **Diffusion Sampler & Spatial Resolution Qualification** — Disambiguated
  second-order Euler Ancestral claims in `foundation-diffusion.html` to fast
  stochastic Euler Ancestral (Euler-A) and deterministic DDIM; clarified latent
  spatial area downsampling ($8 \times 8 = 64\times$) versus channel expansion.
* **Taxonomy Alignment & Elimination of Category 15** — Re-indexed legacy
  Category 15 references in `detection-classification.html` and companion
  markdown to `Category 09 VISION` (sub-designation `Category 09.1
  SPECIFICATION`).
* **YOLOv8n & UPN v2 Latency Disambiguation** — Reconciled YOLOv8n task-specific
  benchmarks (7.2 ms detection, 3.1 ms classification, 8.4 ms pose) and UPN v2
  benchmarks (18.0 ms preview on RTX 3060 vs. 31.0 ms full-resolution on GTX
  1650 FP16 ONNX). Qualified 4GB VRAM execution guarantees to dynamic
  micro-batch scaling.
* **NIMA Taxonomy Matrix Clarification** — Formally clarified the 2x2
  four-quadrant aesthetic and technical matrix alongside the orthogonal
  generative media authenticity axis in `nima-master.html` and companion
  markdown.
* **Forex Predictor Backtest & Drawdown Boundary** — Clarified baseline
  volatility in abstract and documented the 665.80% maximum drawdown convention
  as cumulative leveraged loss on unconstrained Walk-Forward validation without
  margin stop-out.
* **Facial Restoration Metric Calibration Rationale** — Added mathematical
  justification for the $20\times$ multiplier in composite visual quality
  scoring ($\text{PSNR} + (\text{SSIM} \times 20) - (\text{LPIPS} \times 20)$)
  bringing normalized $[0, 1]$ indices into parity with decibel scales.
* **Hub Index Branding Consistency & Canonical Author Standardization** —
  Standardized logo alt text and copyright notice to `LemGendary AI Hub` in
  `index.html`; standardized all author attributions to canonical ASCII `Lem
  Treursic` across 17 files; aligned dataset compiler version to `v16.9.6`
  across HTML and Markdown.
* **32-Rule Automated Test Suite Expansion** — Expanded
  `tests/test_documentation.py` from 24 to 32 automated tests with new
  regression checks for regex escape math corruptions, category taxonomy drift,
  author standardization, SwiGLU equation integrity, VLM cross-entropy syntax,
  index branding consistency, universal LaTeX delimiter balance, and strict
  HTMLParser tag hierarchy validation. All 32 tests passing with 0 warnings.

---

### v16.9.25 — Ecosystem Sync & Fleet Testing API/CLI/GUI Manuals Alignment

* **Master API Reference Manual (`MANUAL_API.md`)** — Documented new endpoints
  across all 3 sidecars: Environment Manager (`POST /api/hooks/install`, `POST
  /api/clean`), Dataset Compiler (`GET /api/modernize/queue`, `POST
  /api/modernize/run`, `POST /api/modernize/reduce`, `POST
  /api/modernize/regenerate-manifolds`, `POST /api/kaggle/update-metadata` with
  `all_datasets: true`), and Training Suite (`POST /api/training/unit-test-all`,
  `POST /api/notebooks/generate-all`).
* **Master CLI Operations Manual (`MANUAL_CLI.md`)** — Documented new CLI
  commands and aliases: `lem-env hooks`, `python cli.py modernize
  queue|run|reduce|regen`, `python cli.py sync metadata [--all]`, `lemtrain
  test-all [--epochs 1]`, and `lemtrain sync push <model>`.
* **AI Studio GUI Operator Manual (`MANUAL_AI_STUDIO_GUI.md`)** — Documented
  CompilerPanel Section 2 sub-tabs (Catalog, Modernization Queue, Scale
  Reduction) and top toolbar actions, TrainingPanel fleet diagnostic test
  button, notebook generator button, per-card eval/export actions,
  CloudTrainModal checkpoint upload tab, and HealthPanel Ecosystem Maintenance &
  Governance card.
* **GUI Control Registry (`GUI_CONTROL_REGISTRY.md`)** — Registered all newly
  added control IDs across Compiler, Training, and Health panels with bound
  sidecar endpoints.
* **Architectural Whitepapers (`PAPER_DATASET_COMPILER.md`,
  `PAPER_TRAINING_SUITE.md`, `PAPER_ENV_MANAGER.md`, `PAPER_AI_STUDIO_GUI.md`)**
  — Synchronized architectural sections with the new modernization, fleet
  testing, git hook installation, and governance capabilities.
* **Test Battery Pass** — Verified 24/24 automated integrity tests passing in
  `tests/test_documentation.py`.

---

### v16.9.24 — SSOT Notebook Generation, Manuals & Whitepaper Sync

* **Single Source of Truth (SSOT) Notebook Generation Architecture** —
  Synchronized whitepapers and operational manuals with the consolidation of
  Jupyter notebook synthesis into `lemgendary-training-suite`
  (`training/notebooks/`, `training/services/notebook_service.py`) and removal
  of redundant generators from `lemgendary-datasets`.
* **Master CLI Operations Manual (`MANUAL_CLI.md`)** — Documented Section 6.5
  (`lemtrain notebooks list`, `lemtrain notebooks generate --model`, `lemtrain
  notebooks generate --all`) detailing multi-target staging across
  `LemGendaryModels/`, `LemGendaryDatasets/`, `kaggle_training/`, and
  `colab_training/`.
* **Master API Reference Manual (`MANUAL_API.md`)** — Documented Section 4.3
  REST endpoints (`GET /api/notebooks/models`, `POST /api/notebooks/generate`,
  `POST /api/notebooks/refresh-all`) on port 8200.
* **AI Studio GUI Manual (`MANUAL_AI_STUDIO_GUI.md`)** — Documented Section 6.1
  Callouts 9 & 10 detailing the dedicated "Training Notebook" and "Usage
  Notebook" one-click action buttons on model cards.
* **Master Training Suite Whitepaper (`PAPER_TRAINING_SUITE.md`)** — Added
  Section 2.16 covering unified notebook synthesis, polymorphic Kaggle/Colab
  builders, and Step 0 training pre-flight synchronization hooks.
* **Dataset Compiler Whitepaper (`PAPER_DATASET_COMPILER.md`)** — Added Section
  5.15 covering dynamic SSOT notebook delegation, compiler deduplication, and
  stale artifact purging.

---

### v16.9.23 — Hub Live Search, Task Portals, AI-Helper Contract & 24 Tests

* **Client-Side Live Search & Keyboard Navigation** — Integrated real-time
  client-side search bar (`#hub-search-input`) with glassmorphism styling and
  keyboard shortcut (`/`) filtering across category titles, summaries, and
  keyword tags.
* **Task-Oriented Entry Portals** — Added dynamic task filters on `index.html`
  allowing instant filtering by developer intent: `Getting Started` (Cat 01,
  03), `Dataset Engineering` (Cat 00, 12), `Training & Debugging` (Cat 02, 13),
  and `Model Reference` (Cat 04–11).
* **Document Authority & Metadata Standard** — Exposed visible header metadata
  pills (`v16.9.23-STABLE`, `Last Reviewed: 2026-10-09`, `AUTHORITATIVE SSOT`)
  and tier authority badges (`Tier 1 OpenAPI`, `Tier 2 Manual`, `Tier 3
  Spec/Whitepaper`, `Tier 4 Playbook`) across category cards.
* **AI-Helper Knowledge Contract & Resolution Protocol** — Added formal 4-part
  AI Helper operational contract to `AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md` and
  `ai-helper-troubleshooting-knowledge.html` establishing strict Authority
  Hierarchy (Tiers 1–4), Mandatory Citation Policy, Diagnostic Intake Protocol,
  and Explicit Admission Bounds (`"UNVERIFIED IN PUBLISHED HUB"`).
* **24-Rule Test Battery** — Expanded `test_documentation.py` from 20 to 24
  automated tests covering live search integration, task portals, authority
  metadata badges, knowledge contract assertions, and real-world failure
  scenario resolution.

---

### v16.9.22 — GUI Control Registry, Troubleshooting CLI & Claims Qualification

* **GUI Control Registry Contract Alignment** — Reconciled bound sidecar
  endpoints in `GUI_CONTROL_REGISTRY.md` and `gui-control-registry.html` with
  canonical API manual specifications (`GET /api/health`, `POST
  /api/pipeline/run`, `GET /api/gui/models/with-stats`, `POST
  /api/gui/quick-train`).
* **Troubleshooting CLI Command Standardization** — Verified dataset compilation
  command syntax strictly uses `python cli.py compile` with valid `cli.py`
  options across troubleshooting knowledge documentation.
* **Mathematical Delimiter & LaTeX Audit** — Audited LaTeX equations and
  validated delimiter integrity (`\left` / `\right`) across all NIMA
  publications.
* **API Manual Version Metadata Alignment** — Updated sidecar health endpoint
  example version metadata in `MANUAL_API.md` and `api-manual.html` to align
  with `v16.9.16-STABLE`.
* **Technical Claims Qualification & Benchmark Linking** — Qualified absolute
  claims for Zero-IPC ThreadPool and Parquet Zstd cluster slack recovery in
  `GLOSSARY.md` and `glossary.html` with explicit benchmark conditions.

---

### v16.9.21 — 20-Rule Test Suite, Category Taxonomy & Pre-Commit Hardening

* **20-Rule Comprehensive Documentation Test Battery** — Expanded
  `tests/test_documentation.py` from 13 to 20 automated tests, enforcing zero
  emojis, LaTeX deep integrity, stray HTML fragment detection, category taxonomy
  uniqueness, ungrounded CLI command rejection, compiler API parity, model
  registry specification alignment, and benchmark evidence qualification.
* **Global Category Taxonomy Unification** — Reconciled category collisions: GUI
  Control Registry reassigned to `Category 03.4 CONTROLS`, reserving `Category
  04` exclusively for Dedicated Image Restoration. Centralized governance and
  operational specs under `Category 01.x` (`01.0 STATUS`, `01.1 ENV`, `01.5
  POLICY`), preserving `Category 00` strictly for General AI Training Knowledge.
* **Deep Mathematical & LaTeX Notation Repairs** — Corrected escape-truncated
  primitives (`\alpha`, `\bar{\alpha}_t`, `\tau`, `\right`, `\begin{cases}`,
  `\rho(`, `\beta(`) across all 48 HTML whitepapers and Markdown companion
  sources.
* **SSOT Model Registry & Compiler API Synchronization** — Aligned NIMA Mobile
  backbone specification to `MobileNetV3-Small`, technical and authenticity
  backbones to `EfficientNetV2-S`, and documented compiler endpoints (`POST
  /api/gui/custom-compile`, `/api/kaggle/...`) across both HTML and Markdown API
  manuals.
* **Git Pre-Commit Hook Hardening** — Hardened pre-commit hook path resolution
  across `.githooks/pre-commit` and `.git/hooks/pre-commit` with dynamic
  directory inspection (`HOOK_DIR`) and direct `test_documentation.py`
  execution, ensuring commits from any CWD trigger the full 20-rule battery.

---

### v16.9.20 — Stage 8: Documentation, Manuals & GUI Training Panel Sync

* **Universal Automated Documentation Test Suite Validation** — Expanded
  automated test suite in `lemgendary-docs/tests/test_documentation.py` (12/12
  passing) covering zero emojis, LaTeX syntax integrity, HTML tag balancing,
  internal link existence across all 48 publications, and CSS brace balance.
* **Full Compliance Passing Status** — Validated `lem-env validate --project
  lemgendary-docs` achieving 100% compliance across Python compilation,
  markdownlint, YAML, JSON, W3C/WCAG, and domain document sync similarity.
* **Category 13: AI Helper Troubleshooting Integration** — Added Category 13
  card to `index.html` and cross-linked
  `ai-helper-troubleshooting-knowledge.html` into `manuals-hub.html` and
  `training-pathology.html`.
* **GUI Manual & Training Panel Revamp Documentation** — Documented the
  redesigned 1/4 - 3/4 dashboard topology, full-width model card header with
  integrated progress bars, interactive pinned/persisted SOTA tooltip metric
  inspector, dual Local/Cloud triggers with auto-scroll and telemetry focus, and
  the interactive Cloud Training modal in `MANUAL_AI_STUDIO_GUI.md` and
  `ai-studio-manual.html`.

---

### v16.9.19 — Stage 7: P2 AI Helper Training Corpus & Documentation Tests

* **Tasks 11-13 & 17: Tri-Level Task Trajectories (GUI, CLI, REST API)** —
  Synthesized multi-tiered procedural training pairs answering identical
  developer objectives across GUI click paths, CLI terminal automation
  (`lem-env`), and headless backend REST API requests.
* **Tasks 14 & 16: Structured Troubleshooting Knowledge Base** — Published
  `AI_HELPER_TROUBLESHOOTING_KNOWLEDGE.md` and
  `ai-helper-troubleshooting-knowledge.html` formalizing real-world failure
  modes (scheduler double-stepping, AMP NaN instability, sentinel/scheduler
  desynchronization, infinite plateau loops, Pearson matrix singularities,
  dataloader starvation) into a 6-attribute diagnostic schema (`symptom`,
  `context`, `observations`, `likely_causes`, `diagnostic_steps`,
  `recommended_action`).
* **Task 15: Cross-Document Architectural Pipelines** — Synthesized end-to-end
  provenance trajectories spanning Raw Datasets $\to$ Dataset Compiler Presets
  $\to$ Sharded Manifolds $\to$ Model Architectures $\to$ Resolution Ladders
  $\to$ Checkpoint Lifecycles $\to$ ONNX/WebGPU Production Targets.
* **Task 18: Canonical 32-Field Model Schema Registry** — Standardized all 22
  active and specification models in `tools/model_schema_registry.json`
  conforming to a uniform 32-field schema covering inputs, outputs, loss
  functions, SOTA targets, failure modes, and hardware bounds.
* **Task 19: Terminology Disambiguation & Hardened Negative Pairs** —
  Synthesized contrastive pairs training the AI Helper on foundational
  distinctions: Raw Dataset vs. Compiled Manifold, Container Format vs.
  Directory Layout, Hardlink vs. Perceptual Deduplication, and Native Studio
  Compatibility vs. General AI Formats.
* **Corpus Sharding & Validation** — Generated
  `lemgendary-docs/corpus/ai_helper_train.jsonl` and `ai_helper_val.jsonl`
  validated for strict ChatML schema compliance, token length bounds, and zero
  emojis.
* **Automated Documentation Test Suite** — Implemented unit test suite in
  `lemgendary-docs/tests/test_documentation.py` running automated regression
  audits on emojis, control characters, LaTeX integrity, SSOT manifest parity,
  canonical topologies, and epistemic tags.

### v16.9.18 — Stage 6: P1 Knowledge Normalization, Topology & Schema

* **Item 6: Studio-Supported-Format Matrix** — Added comprehensive comparative
  matrix in `dataset-compiler.html` and `PAPER_DATASET_COMPILER.md` explicitly
  distinguishing General Knowledge formats from Studio-Supported native
  compilation manifolds.
* **Item 7: Canonical 8-Section Topology Normalization** — Enforced uniform
  structural topology across all 19 model whitepapers in both HTML (`papers/`)
  and Markdown (`MD-Papers/`): `1. Abstract`, `1.1 Plain English`, `2. Visual
  Taxonomy`, `3. Shared Foundations`, `4. Model Deep-Dives`, `5. Challenges &
  Resilience Architecture`, `6. Deployment Strategy & Production Acceleration`,
  `7. SOTA Architectural Performance Matrix`, and `8. Conclusion`.
* **Item 8: Universal Epistemic Claim Tagging** — Annotated empirical
  measurements, mathematical theorems, aspirational targets, and operational
  checkpoints with normalized tags (`[THEORETICAL]`, `[MEASURED]`, `[TARGET]`,
  `[CURRENT]`, and `[DESIGN_GOAL]`) across all model documentation.
* **Item 9: Technical Guarantee Qualification** — Qualified ungrounded absolute
  terminology ("impossible", "100%", "sub-millisecond latency", "guaranteed",
  "never") to mathematically bounded engineering guarantees across the corpus.
* **Item 10: Bidirectional Cross-Document Knowledge Graph** — Embedded
  comprehensive cross-reference hubs linking Model Whitepapers $\leftrightarrow$
  Dataset Compiler Specifications $\leftrightarrow$ Training Suite Architecture
  $\leftrightarrow$ GUI Manuals.

### v16.9.17 — Hub Quality Audit, LaTeX Standardization & Section 4 Deep-Dives

* **Universal W3C & Structural Integrity Audit** — Audited and remediated all 48
  HTML whitepapers in `lemgendary-docs/papers/`. Resolved tag balance mismatches
  in `forex_predictor.html`, `dataset-compiler.html`, `ffanet.html`, and
  `universal-hybrid.html`. Standardized MathJax 3 configurations with SVG global
  font caching across all technical documents.
* **Corrupted LaTeX & Mathematical Delimiter Repair** — Fixed tab-corrupted and
  carriage-return-corrupted LaTeX primitives (`\text`, `\times`, `\right`,
  `\bmod`) across `forex_predictor.html`, `foundation-models-master.html`,
  `nima-master.html`, `restoration-master.html`, and `ultrazoom.html`. Escaped
  raw pricing currency signs in `dataset-compiler.html` to prevent math syntax
  conflicts.
* **Section 1.1 (Plain English) & Section 4 (Model Deep-Dives) Standardization**
  — Uniformly implemented Section `1.1 What [ModelName] Does (In Plain English)`
  with visual before/after comparison demonstrations and Section `4. Model
  Deep-Dives` with model metadata, dataset specs, verified metric benchmarks,
  and high-resolution dark-themed training curves across all 19 model
  whitepapers.
* **P0 Metadata Synchronization** — Unified the NIMA Mobile backbone
  specification strictly to `MobileNetV3-Small (Global Composition)` and
  documented edge backbones (`MobileNetV3-Small`) for RetinaFace across both
  markdown sources and HTML publications. Standardized model status tokens
  across the entire corpus.

### v16.9.16 — Batch/Epoch Progress Telemetry & First-Principles VRAM Sizing

* **`PAPER_LEMGENDARY_YOLOV8N.md` Synchronization** — Documented Section 5.1
  first-principles dynamic Sawtooth VRAM sizing formula, configuration
  externalization in `unified_models_v2.yaml`, and real-time validation plot
  mirroring (`confusion_matrix.png`, `confusion_matrix_normalized.png`, PR/F1
  curves) directly to `LemGendaryModels/yolov8n/`.
* **`PAPER_TRAINING_SUITE.md` Synchronization** — Documented real-time batch and
  epoch progress logging in terminal execution, non-blocking remote checkpoint
  probing with 5-second timeouts, and strict code-only training suite filesystem
  isolation.
* **`LemGendaryModels/` Dashboard Synchronization** — Synchronized live metrics
  matrix dashboard and per-model READMEs across all 22 active architectures via
  `doc_generator.py`.

### v16.9.13 — Intra-Resolution Fraction Progression & Overfitting Rescue

* **`PAPER_LEMGENDARY_YOLOV8N.md` & `detection-yolov8n.html` Synchronization** —
  Documented Section 5.1 Intra-Resolution Fraction Progression on the lowest
  resolution rung ($320\text{px} @ 30\% \to 70\% \to 100\%$) prior to spatial
  resolution escalation, Governor Overfitting Rescue Protocol monitoring loss
  divergence and mAP stagnation during partial fraction stages to force
  immediate dataset expansion, and Section 5.2 Multi-Fraction Checkpoint
  Discovery and Resumption.
* **`lemgendary-training-suite/` Protocol Synchronization** — Documented
  deterministic fraction progression on base rungs, adaptive epoch allocations
  across 5 stages, and checkpoint state encoding (`stage{idx}_{res}px_f{pct}`).

### v16.9.12 — Checkpoint Resumption, Persistence & Literature Citations

* **`PAPER_LEMGENDARY_YOLOV8N.md` & `detection-yolov8n.html` Synchronization** —
  Documented Section 5.2 deep checkpoint metadata interrogation, completed stage
  skipping, and mid-rung resumption (`resume=True`) from `last.pt`, Section 5.3
  Authoritative Persistence in `LemGendaryModels/`, and Section 7 Scientific
  Literature & Reference Citations.
* **`PAPER_TRAINING_SUITE.md` & `training-suite-master.html` Synchronization** —
  Documented Section 2.4 Mid-Rung Checkpoint Resumption & Stage Skip Protocol
  across all models, Authoritative Single Source of Truth Persistence in
  `LemGendaryModels/<model_key>/`, and literature references integration.
* **`LemGendaryModels/` Model Documentation Matrix Synchronization** — Embedded
  landmark academic citations (authors, venue, year, canonical link, and BibTeX)
  across all 22 model READMEs in `LemGendaryModels/<model_key>/README.md` and
  refreshed the master hub dashboard.

### v16.9.11 — Checkpoint Parity, Sub-Second Cancellation & Telemetry Stream

* **`PAPER_LEMGENDARY_YOLOV8N.md` Synchronization** — Documented Section 5.1
  dual-path intermediate checkpoint synchronization (`best.pt`, `best.pth`,
  `last.pt`, `progress.pth`) to `checkpoints/` and `LemGendaryModels/`, and
  inner-loop minibatch cancellation via `on_train_batch_end` setting
  `trainer.stop = True`.
* **`PAPER_TRAINING_SUITE.md` Synchronization** — Documented Section 2.4
  Real-Time Cross-Model Checkpoint Parity and Sub-Second Minibatch Cancellation
  Protocol across all 20 architectures.
* **`MANUAL_AI_STUDIO_GUI.md` Synchronization** — Documented Section 6.2
  Top-of-Fold Real-Time Telemetry Stream placement directly above the Registered
  Architectures catalog and the sub-second cancellation response handshake.

### v16.9.10 — SSOT Readonly Parameters, Job Control & YOLO Curriculum Governor

* **`MANUAL_AI_STUDIO_GUI.md` & `ai-studio-manual.html` Synchronization** —
  Documented Section 6.1 Single Source of Truth (SSOT) parameter locking across
  all neural models (`Training Epochs`, `Minibatch Size`, `Initial Learning
  Rate`, and `Spatial Ladder Stage` / `Timeframe Confluence Stage`) to read-only
  mode (`.editor-input-readonly`) tied directly to `unified_models_v2.yaml` /
  `presets.yaml`. Documented the `.config-governed-banner`, inline `Adjust via
  Config Editor` workflow, and the dynamic run-state action button transforming
  from `Start Training` (`.btn-primary`) to `Stop Training` (`.btn-danger`) with
  job cancellation signal dispatch (`POST /api/jobs/{job_id}/cancel`).
* **`PAPER_TRAINING_SUITE.md` & `training-suite-master.html` Synchronization** —
  Documented Section 2.14 Autonomous YOLO Multi-Stage Curriculum Governor
  (`YOLOCurriculumGovernor`, `320px -> 480px -> 640px` resolution ladder, `0.3
  -> 0.6 -> 1.0` dataset fraction scaling, Turing FP32 numerical stability
  overrides, Sawtooth VRAM sentinel, and telemetry writeback to
  `checkpoints/yolov8n/metrics.csv`), as well as Section 2.15 SSOT
  Config-Governed GUI Training Controls and dynamic run-state lifecycle.
* **`PAPER_LEMGENDARY_YOLOV8N.md` & `detection-yolov8n.html` Synchronization** —
  Documented Section 5.1 detailing the autonomous curriculum governor,
  progressive spatial ladder handoff (`best.pt` warm-starts), dataset scaling,
  Sawtooth memory sentinel, Turing non-Tensor core AMP overrides (`amp=False`),
  and live telemetry streaming.

### v16.9.9 — Training Form Stabilization & Dynamic Model Defaults Sync

* **`MANUAL_AI_STUDIO_GUI.md` & `ai-studio-manual.html` Synchronization** —
  Documented Section 6.2 dynamic model hyperparameter synchronization upon
  architecture selection (YOLOv8n default 300 epochs, 0.01 learning rate, 640px
  stage; Forex Predictor default 0.0001 learning rate, D1 macro horizon),
  dedicated architecture selector row with architectural metadata badges, and
  glassmorphic Sawtooth Governor card.
* **`MANUAL_API.md` & `api-manual.html` Synchronization** — Documented `POST
  /api/gui/quick-train` payload support for `ladder_stage` and `enable_sawtooth`
  with in-process Ultralytics native trainer delegation for YOLOv8n, and
  enriched `GET /api/gui/models/with-stats` returning `learning_rate`,
  `batch_size`, and `default_epochs`.

### v16.9.8 — 3-Pillar SOTA Convergence & Forex Multi-Timeframe Confluence

* **`PAPER_TRAINING_SUITE.md` Synchronization** — Documented the mathematical
  3-Pillar Fully-Trained Verification Invariant ($\bigwedge_{m} \text{Passed}(m,
  T_m) \land \text{LadderPassed} \land \text{DataFraction} \ge 1.0$),
  multi-metric evaluation across all defined `sota_targets`, Timeframe
  Confluence Ladder (`res_ladder: [1, 5, 15, 60, 240, 1440]`), and the 8-metric
  financial scorecard (`DirAcc`, `WinRate`, `ProfitFactor`, `Sharpe`, `Sortino`,
  `MaxDD`, `TP_MAE`, `SL_MAE`).
* **`MANUAL_AI_STUDIO_GUI.md` & `MANUAL_API.md` Specification Updates** —
  Documented Section 6.4 Model Architecture Cards and Status Badges (`FULLY
  TRAINED`, `PARTIALLY TRAINED`, `WEIGHTS READY`, `INITIALIZING`), card
  telemetry rows (`SOTA Targets`, `Confluence Ladder / Resolution Ladder`, `Data
  Fraction`), adaptive timeframe controls, and the enriched `GET
  /api/gui/models/with-stats` schema.

### v16.9.7 — Headless Service Execution & Automated GUI Mesh Bootstrapping

* **`PAPER_AI_STUDIO_GUI.md` & `MANUAL_AI_STUDIO_GUI.md` Synchronization** —
  Documented the cross-platform windowless background daemon execution
  architecture (`pythonw.exe`, `CREATE_NO_WINDOW`, `stdin=DEVNULL` on Windows;
  `start_new_session=True` on POSIX), eliminating intrusive console and Windows
  Terminal popups. Documented the GUI's automated startup effect on launch
  (`autoStartOffline`) and decoupled sub-100ms mesh heartbeats.
* **`MANUAL_API.md` Specification Updates** — Documented extended 20-second
  startup verification windows and `is_port_in_use()` collision guards for `POST
  /api/services/{service_id}/start`, plus dual `GET` and `HEAD` handler
  compliance across all sidecar `/api/health` endpoints.

### v16.9.6 — GUI Kaggle Cloud Sync Hub & Multi-Source Custom Compilation

* **`PAPER_DATASET_COMPILER.md` & `PAPER_AI_STUDIO_GUI.md` Synchronization** —
  Documented the Kaggle Cloud Synchronization & Storage Hub (bidirectional
  dataset downloads from `unified_data.yaml` registry, custom Kaggle link/slug
  downloads, and local manifold uploads), multi-source custom dataset synthesis
  pipeline (`kaggle://`, `hf://`, `gd://`, `gh://`), and fast split-shard
  discovery caching across 22 compiled manifolds.
* **`MANUAL_AI_STUDIO_GUI.md` & `MANUAL_API.md` Expansion** — Updated Section 5
  of the GUI manual with detailed walkthroughs for Standard and Custom
  Multi-Source compilation modes, documented new REST endpoints (`GET
  /api/kaggle/registry-datasets`, `POST /api/kaggle/download`, `POST
  /api/kaggle/upload`, `POST /api/gui/custom-compile`), and synchronized the
  interactive control dictionary in `GUI_CONTROL_REGISTRY.md`.

### v16.9.1 — Visual Demonstration Remediation (Track B Execution)

* **`assets/` Asset Generation & Conversion** — Generated and optimized 10
  high-fidelity perceptual demonstration assets into `assets/`:
  * `codeformer_before.png` & `codeformer_after.png` — Vector-quantized codebook
    face restoration before/after pair.
  * `film_restorer_before.png` & `film_restorer_after.png` — Analog 35mm
    celluloid scratch, dust, and dye recovery pair.
  * `upn_v2_before.png` & `upn_v2_after.png` — Multi-degradation composite
    restoration pair (motion blur, noise, compression).
  * `ultrazoom_before.png` & `ultrazoom_after.png` — Sub-pixel 4x
    super-resolution architectural crop pair.
  * `yolov8n_before.png` & `yolov8n_after.png` — Real-time spatial object
    detection and bounding box matrix pair.
* **HTML Whitepaper Remediation (`papers/`)** — Completely eliminated all
  dashed-border `<div>` placeholders across 9 papers, replacing them with
  semantic `<img>` elements and descriptive accessibility attributes:
  * `nima-authenticity.html` — Replaced placeholder blocks with
    `nima_authenticity_fake.png` and `nima_authenticity_real.png`. Synchronized
    training curve to `nima_authenticity_training.png`.
  * `nima-pro.html`, `nima-mobile.html`, `nima-efficientnet.html` — Replaced
    placeholder blocks with `technical_compression.png` and
    `aesthetic_masterpiece.png`.
  * `face-codeformer.html` — Embedded `codeformer_before.png` and
    `codeformer_after.png`.
  * `hybrid-film-restorer.html` — Embedded `film_restorer_before.png` and
    `film_restorer_after.png`.
  * `hybrid-upn-v2.html` — Embedded `upn_v2_before.png`, `upn_v2_after.png`, and
    `upn_v2_training.png`.
  * `ultrazoom.html` — Embedded `ultrazoom_before.png`, `ultrazoom_after.png`,
    and `ultrazoom_training.png`.
  * `detection-yolov8n.html` — Embedded `yolov8n_before.png` and
    `yolov8n_after.png`.
* **Markdown Whitepaper Synchronization (`MD-Papers/`)** — Updated all 9
  markdown companions (`PAPER_NIMA_*.md`, `PAPER_LEMGENDARY_*.md`) with
  synchronized visual assessment tables and training curve references.
