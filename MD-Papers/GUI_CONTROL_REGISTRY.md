# LemGendary AI Studio GUI: Control ID Registry & Operational Boundaries

## Category 03.4 CONTROLS | LemGendary AI Documentation Hub

**Version**: `v2.10.57` (LemGendary AI Studio GUI) · **Last audited**:
2026-11-12 · **Companion**: [Operator Manual](./MANUAL_AI_STUDIO_GUI.md) ·
[Architectural Whitepaper](./PAPER_AI_STUDIO_GUI.md)

---

## Table of Contents

- [1. Abstract](#1-abstract)
- [2. Control ID Taxonomy & Schema](#2-control-id-taxonomy--schema)
- [3. Master Interactive Controls
  Dictionary](#3-master-interactive-controls-dictionary)
  - [3.1 Header & Sidebar](#31-header--sidebar)
  - [3.2 Report Issue Dialog & Annotator](#32-report-issue-dialog--annotator)
  - [3.3 Test & Diagnostic Orchestrator](#33-test--diagnostic-orchestrator)
  - [3.4 Run Pipeline & Clean Install](#34-run-pipeline--clean-install)
  - [3.5 Dataset Compiler Suite](#35-dataset-compiler-suite)
  - [3.6 Model Training Suite](#36-model-training-suite)
  - [3.7 Health & Version Drift](#37-health--version-drift)
  - [3.8 Config & Secrets](#38-config--secrets)
  - [3.9 Dialogs, Status Regions &
    Headings](#39-dialogs-status-regions--headings)
  - [3.10 Controls Without an ID](#310-controls-without-an-id)
  - [3.11 Changes Since the Previous
    Registry](#311-changes-since-the-previous-registry)
- [4. End-to-End Operational Workflows](#4-end-to-end-operational-workflows)
  - [4.1 Workflow 1: Environment Provisioning & Health
    Audit](#41-workflow-1-environment-provisioning--health-audit)
  - [4.1.1 WebSocket Event Lifecycle
    Recovery](#411-websocket-event-lifecycle-recovery)
  - [4.2 Workflow 2: Manifold Compilation](#42-workflow-2-manifold-compilation)
  - [4.3 Workflow 3: Reporting an Issue](#43-workflow-3-reporting-an-issue)
- [5. Operational Boundaries & Platform
  Availability](#5-operational-boundaries--platform-availability)

---

## 1. Abstract

This registry lists every element of the LemGendary AI Studio GUI
(`lemgendary-ai-studio-gui`) that carries an `id` attribute, with its label,
element type, the sidecar endpoint it calls and its behaviour. It is recounted
from the `id` attributes in `src/**/*.tsx` of GUI release `v2.10.57`, including
the IDs that the shared `Modal`, `ConfirmDialog` and `Tabs` components build
from their props, with a template such as `train-btn-start-{model_key}` counted
once: 150 distinct IDs, of which 91 belong to controls (sections 3.1 to 3.8)
and 59 to dialogs, status regions, landmarks and headings (section 3.9).
Automated tests, accessibility checks and the bug report module select use these
IDs, so an ID changes only together with this registry.

The GUI talks to three local sidecars: the LemGendary Environment Manager on
port 8000, the LemGendary Dataset Compiler Suite on port 8100 and the LemGendary
Model Training Suite on port 8200.

---

## 2. Control ID Taxonomy & Schema

New IDs follow a hyphenated pattern:

$$
\mathbf{[view]\text{-}[component]\text{-}[element]\text{-}[action]}
$$

- **`[view]` or `[component]`**: `header`, `dash`, `pipeline`, `comp`, `custom`,
  `reduce`, `train`, `health`, `test-modal`, `bug-modal`, `annotator`.
- **`[element]`**: `btn`, `select`, `input`, `dialog`, `tab`.
- **`[action]`**: what the control does, for example `run-pipeline`,
  `clean-confirm`, `submit`.

Older IDs keep their shipped names (`preset-select`, `custom-name-input`,
`training-toolbar-push-all-models-btn`) because tests depend on them. Repeated
controls are templates: `{model_key}` is a model key from
`unified_models_v2.yaml`, `{dataset_key}` a manifold key, `{tab_id}` one of
`dashboard`, `datasets`, `training`, `pipeline`, `health`, `{n}` a position
starting at 1 and `{secret_id}` the id of a stored credential.

Endpoint notation: `GET /api/hardware` (8000) means the Environment Manager
route on port 8000. Every request goes through `sidecarFetch` in
`src/api/http.ts`, which adds the header `X-LemGendary-Client: ai-studio-gui`;
the sidecars refuse browser writes without it. "None" means the control only
changes GUI state.

---

## 3. Master Interactive Controls Dictionary

Each entry reads: ID (element type): label. Endpoint. Behaviour.

### 3.1 Header & Sidebar

- `header-btn-report-issue` (`button`): "Report Issue". None. Opens the Report
  Issue dialog (section 3.2) with the module set to the current tab.
- `header-btn-test-modal` (`button`): "Tests & Diagnostics". None. Opens the
  Test & Diagnostic Orchestrator (section 3.3).
- `dash-btn-refresh-audit` (`button`): "Refresh Audit". `GET /api/hardware`,
  `GET /api/health` and `GET /api/pipeline/status` (8000) plus the liveness
  probes. Reloads hardware, health and pipeline state; shows "Refreshing..."
  while busy.
- `tab-{tab_id}` (`button`): sidebar tab ("Dashboard", "LemGendary Dataset
  Compiler Suite", "LemGendary Model Training Suite", "Clean Install Pipeline",
  "Health & Version Drift"). None. Switches the workspace view; the dot shows
  whether the sidecar behind the view is online.

### 3.2 Report Issue Dialog & Annotator

- `bug-modal-email` (`input type=email`): "Your email". None. Reply address, at
  most 254 characters, checked on submit.
- `bug-modal-module` (`select`): "Module". None. One option per sidebar tab;
  preselected from the current tab.
- `bug-modal-description` (`textarea`): "What happened?". None. 50 to 10,000
  characters; the counter below shows the length.
- `bug-modal-telemetry` (`input type=checkbox`): "Attach telemetry". None. On by
  default; attaches the recent log events as a CSV file
  (`timestamp,status,source,message`).
- `bug-modal-btn-add-screenshot` (`button`): "Capture screenshot". None. Opens
  the annotator; disabled when 5 screenshots are attached.
- `bug-modal-btn-remove-screenshot-{n}` (`button`): "Remove". None. Removes
  screenshot `{n}` from the strip.
- `bug-modal-btn-start-recording` (`button`): "Start recording". Native
  `recording_start`. Desktop app only; hides the dialog and shows the recording
  control bar.
- `bug-modal-btn-remove-recording` (`button`): "Remove recording". None. Shown
  only when a recording is attached; discards it.
- `recording-btn-pause` (`button`): "Pause". Native `recording_pause`. Shown in
  `recording-control-bar` while recording.
- `recording-btn-resume` (`button`): "Continue". Native `recording_resume`.
  Shown while paused.
- `recording-btn-stop` (`button`): "Stop and attach". Native `recording_stop`.
  Returns to the dialog with the MP4 attached as `recording.mp4`.
- `bug-modal-btn-cancel` (`button`): "Cancel". None. Closes the dialog.
- `bug-modal-btn-submit` (`button type=submit`): "Send report".
  `POST /api/bug-report` (8000), multipart. Validates the form, sends it and
  shows the success view; 422 errors appear under the matching field.
- `bug-modal-btn-done` (`button`): "Done". None. Closes the success view and
  resets the form.
- `bug-modal-btn-copy-address` (`button`): "Copy address". None. Copies the
  recipient address to the clipboard.
- `bug-modal-btn-copy-subject` (`button`): "Copy subject". None. Copies the mail
  subject to the clipboard.
- `annotator-canvas` (`canvas`): screenshot of the app. None. Drag to draw one
  highlight rectangle; a new drag replaces it.
- `annotator-btn-cancel` (`button`): "Cancel". None. Discards the capture.
- `annotator-btn-retake` (`button`): "Retake". None. Captures the app window
  again.
- `annotator-btn-save` (`button`): "Save". None. Exports the annotated image as
  WebP (PNG where WebP export is not supported), at most 5 MB, and adds it to
  the strip.

### 3.3 Test & Diagnostic Orchestrator

- `test-modal-btn-close` (`button`): "X". None. Closes the dialog; Escape does
  the same.
- `test-modal-tab-fleet` (`button`): "Fleet 1-Epoch Smoke Test". None. Selects
  the fleet tab.
- `test-modal-tab-training` (`button`): "Training Suite Unit Tests". None.
  Selects the training tab.
- `test-modal-tab-dataset` (`button`): "Dataset Compiler Tests". None. Selects
  the dataset tab.
- `test-modal-btn-run-fleet` (`button`): "Run Fleet Diagnostic (All 23 Models)".
  `POST /api/training/unit-test-all` (8200). Queues the 1-epoch smoke test; the
  console shows `QUEUED` and the job id.
- `test-modal-btn-run-training-unit` (`button`): "Run Training Unit Tests".
  `POST /api/training/unit-test-run` (8200). Runs the Training Suite unit tests
  in-process and prints the summary.
- `test-modal-btn-run-dataset-unit` (`button`): "Run Dataset Compiler Tests".
  `POST /api/llm/test-suite` (8100). Runs the Dataset Compiler test suite
  in-process and prints the summary.

### 3.4 Run Pipeline & Clean Install

- `dash-btn-run-pipeline` (`button`): "Run Pipeline". `POST /api/pipeline/run`
  (8000) with `clean: false`. Runs the 7-step pipeline without deleting
  environments; disabled while the Environment Manager is offline.
- `pipeline-btn-clean-install` (`button`): "Clean Install...". None. Opens the
  clean install confirmation dialog.
- `pipeline-btn-clean-cancel` (`button`): "Cancel". None. Closes the dialog
  without a request; it has focus when the dialog opens.
- `pipeline-btn-clean-confirm` (`button`): "Delete and reinstall".
  `POST /api/pipeline/run` (8000) with `clean: true`. Deletes the virtual
  environments and `node_modules` of all projects, then reinstalls them.

### 3.5 Dataset Compiler Suite

- `comp-mode-standard`, `comp-mode-custom` (`button`, `aria-pressed`):
  "Standard Preset" and "Custom Multi-Source" compile mode switch. None. Shows
  the standard or the custom multi-source compilation form.
- `comp-btn-update-all-kaggle` (`button`): "Update All Kaggle Metadata".
  `POST /api/kaggle/update-metadata` (8100) with `all_datasets: true`. Pushes
  metadata for every registered Kaggle dataset.
- `comp-btn-regen-manifolds` (`button`): "Regen Index".
  `POST /api/modernize/regenerate-manifolds` (8100). Rebuilds `manifolds.json`
  and the dataset metadata files.
- `comp-btn-refresh-catalog` (`button`): "Refresh Catalog".
  `GET /api/gui/datasets/with-stats` (8100). Reloads the manifold catalog.
- `comp-select-manifold` (`select`): target manifold.
  `GET /api/gui/datasets/with-stats` (8100) fills it. Chooses the manifold for a
  standard compile.
- `preset-select` (`select`): compiler preset. `GET /api/gui/presets` (8100)
  fills it. "Server default" omits `preset` so the sidecar applies its default;
  offline only that option is shown.
- `comp-btn-compile` (`button`): "Compile Manifold".
  `POST /api/gui/quick-compile` (8100) with `model` and `preset`. Starts a
  compile job; an unknown preset shows the server's 422 detail.
- `custom-name-input` (`input type=text`): custom manifold name. None. Name of
  the new manifold.
- `custom-task-select` (`select`): domain task. None. Restoration, detection or
  another task type.
- `custom-format-select` (`select`): container format. None. WebDataset,
  Parquet, MDS or LitData.
- `custom-preset-select` (`select`): compiler preset for the custom compile.
  `GET /api/gui/presets` (8100) fills it.
- `custom-shard-size` (`input type=number`): shard size. None. Samples per
  shard.
- `custom-purge-check` (`input type=checkbox`): purge loose files. None. Removes
  loose source images after sharding.
- `custom-sources-area` (`textarea`): source repositories and URLs. None. One
  Kaggle, Hugging Face, Google Drive or GitHub source per line; submitted with
  `POST /api/gui/custom-compile` (8100).
- `comp-input-kaggle-custom-ref` (`input type=text`): Kaggle dataset slug or
  URL. `POST /api/kaggle/download` (8100) on "Ingest from Kaggle". Downloads a
  public or private Kaggle dataset into `LemGendaryDatasets`.
- `comp-btn-meta-{dataset_key}` (`button`): "Update Metadata".
  `POST /api/kaggle/update-metadata` (8100). Pushes the metadata of one manifold
  without uploading data.
- `comp-btn-pull-{dataset_key}` (`button`): "Download".
  `POST /api/kaggle/download` (8100). Downloads the manifold's shards.
- `comp-btn-push-{dataset_key}` (`button`): "Upload". `POST /api/kaggle/upload`
  (8100). Packages and uploads the local shards.
- `reduce-manifold-select` (`select`): manifold to reduce. None. Chooses the
  source manifold for scale reduction.
- `reduce-scale-select` (`select`): sampling scale. None. 10, 25, 50 or 75
  percent; sent with `POST /api/modernize/reduce` (8100).

### 3.6 Model Training Suite

- `train-btn-generate-all-notebooks` (`button`): "Generate All Notebooks".
  `POST /api/notebooks/generate-all` (8200). Writes notebooks for every
  registered model.
- `training-toolbar-push-all-models-btn` (`button`): "Push All Models to
  Kaggle". `POST /api/training/kaggle/push-all` (8200). Stages and publishes all
  model variations.
- `train-btn-refresh-models` (`button`): "Refresh Models".
  `GET /api/gui/models/with-stats` (8200). Reloads models with their latest
  metrics in one request.
- `train-btn-start-{model_key}` (`button`): "Local Training".
  `POST /api/gui/quick-train` (8200) with `model_key` and `batch_size`. Starts
  local training.
- `train-btn-stop-{model_key}` (`button`): "Stop Training".
  `POST /api/jobs/{job_id}/cancel` (8200). Cancels the local job; the job is
  cleared only when the sidecar confirms `cancelled`.
- `train-btn-cloud-{model_key}` (`button`): "Cloud Training". None. Opens the
  Cloud & Registry Dispatch dialog (`POST /api/training/kaggle/train` on
  launch).
- `train-btn-pub-model-{model_key}` (`button`): "Push Model".
  `POST /api/training/kaggle/push` (8200). Publishes the model variations to
  Kaggle Models.
- `train-btn-pull-model-{model_key}` (`button`): "Pull Model".
  `POST /api/training/kaggle/pull` (8200). Downloads the published variations.
- `train-btn-gen-nb-{model_key}` (`button`): "Training Notebook".
  `POST /api/notebooks/generate` (8200) with `kinds: ["training"]`.
- `train-btn-usage-nb-{model_key}` (`button`): "Usage Notebook".
  `POST /api/notebooks/generate` (8200) with `kinds: ["usage"]`.
- `train-btn-eval-{model_key}` (`button`): "Evaluate Model".
  `POST /api/training/evaluate` (8200). Evaluates the checkpoint locally.
- `train-btn-export-{model_key}` (`button`): "Export Binaries".
  `POST /api/training/export` (8200). Exports the model binaries.
- `train-btn-soup-{model_key}` (`button`): "Blend Soup". `POST
  /api/models/{model_key}/soup` (8200). Blends the checkpoints in the model's
  vault into one Model Soup checkpoint (uniform weights) and reports it.
- `cloud-modal-tab-kaggle`, `cloud-modal-tab-colab`, `train-modal-tab-upload`
  (`button`, `role="tab"`): "Kaggle GPU Cloud", "Google Colab FUSE" and "Kaggle
  Models Hub" in the Cloud & Registry Dispatch dialog. None. Switch the panel
  `cloud-modal-panel`.
- `gpu-select` (`select`): Kaggle GPU. None. T4 x2 or P100 for the cloud launch.
- `kaggle-monitor-slug` (`input type=text`): "Monitor an already running
  kernel". None. Kernel reference `owner/kernel-slug`.
- `kaggle-monitor-btn` (`button`): "Attach Monitor". `POST
  /api/training/kaggle/monitor` (8200). Attaches the Remote Cloud console to the
  running kernel and tracks it as the remote job; disabled until the reference
  has the form `owner/kernel-slug`.
- `variation-select` (`select`): variation to check. None. Filters the isolation
  report from `GET /api/models/{model_key}/variations/validate` (8200).

### 3.7 Health & Version Drift

- `health-btn-safe-upgrade` (`button`): "Safe Package Upgrade".
  `POST /api/update` (8000). Starts a background upgrade job and returns its
  `job_id`; 409 means an update or the pipeline is already running.
- `health-btn-upgrade-dry-run` (`button`): "Upgrade Dry Run". `POST /api/update`
  (8000) with `dry_run: true`. Lists planned upgrades without changing anything.
- `health-btn-deep-clean` (`button`): "Deep Cache Purge". `POST /api/clean`
  (8000). Removes `__pycache__`, build remnants and staging residues.
- `health-btn-install-hooks` (`button`): "Install Git Hooks".
  `POST /api/hooks/install` (8000). Installs the pre-commit hooks.
- `health-btn-validate-ecosystem` (`button`): "Run Ecosystem Validation".
  `POST /api/validate` (8000). Runs the validation gates for all projects.

### 3.8 Config & Secrets

- `config-editor-tab-manifests`, `config-editor-tab-secrets` (`button`,
  `role="tab"`): "Registry Manifests" and "Secrets & Tokens Vault". None. Switch
  the panel `config-editor-panel`.
- `manifest-select` (`select`): manifest file. `GET /api/manifests/registry`
  fills it; `GET /api/manifests/read` (8000) loads the chosen file.
- `new-service-select` (`select`): "Target Service". None. Service of a new
  credential.
- `new-label-input` (`input type=text`): "Label / Description". None.
- `new-username-input` (`input type=text`): "Username / Account ID". None.
- `new-server-input` (`input type=text`): "Broker Server". None. Shown for
  MetaTrader 5 credentials.
- `new-secret-input` (`input type=password`): "Secret Token / API Key /
  Password". None. Write-only; sent with `POST /api/secrets` (8000) on save.
- `replace-secret-{secret_id}` (`input type=password`): replacement value.
  `POST /api/secrets` (8000) on save. Blank keeps the stored value; a value
  replaces it. The GUI never reads a stored value back: `GET /api/secrets`
  returns only `has_value` and the last 4 characters (`value_hint`).

### 3.9 Dialogs, Status Regions & Headings

Dialogs and forms:

- `bug-modal-dialog`, `annotator-dialog`, `pipeline-dialog-clean-install`:
  shared `Modal` dialogs (`role="dialog"`, `aria-modal`, focus trap; Escape
  closes the innermost one). Each title has the ID `{dialog_id}-title`.
- `bug-modal-form`: the Report Issue form.
- `test-modal`, `cloud-modal`, `config-editor-modal`: the Test & Diagnostic
  Orchestrator, Cloud Training and Config & Secrets dialogs (shared `Modal`).
- `test-modal-panel`, `cloud-modal-panel`, `config-editor-panel`: the tab
  panels (`role="tabpanel"`) of the shared `Tabs` component, labelled by the
  active tab.
- Confirmation dialogs (`ConfirmDialog`, focus starts on Cancel; buttons
  `{dialog_id}-cancel` and `{dialog_id}-confirm`, text `{dialog_id}-desc`):
  `dash-dialog-stop-service` (Stop Service), `health-dialog-confirm` (Safe
  Package Upgrade and Deep Cache Purge), `config-dialog-delete-secret` (delete a
  credential), `config-dialog-discard-edits` (close or leave the manifest editor
  with unsaved edits) and `config-dialog-discard-manifest` (switch manifests
  with unsaved edits).
- `pipeline-dialog-clean-install-desc`: lists what a clean install deletes.

Status and error regions:

- `bug-modal-error`, `bug-modal-email-error`, `bug-modal-module-error`,
  `bug-modal-description-error`, `bug-modal-other-error`,
  `bug-modal-screenshot-error`, `bug-modal-recording-error`, `annotator-error`:
  error messages (`role="alert"`).
- `bug-modal-description-counter`, `annotator-status`, `bug-modal-copy-status`:
  live status text.
- `bug-modal-screenshot-{n}`: thumbnail `{n}` in the screenshot strip.
- `bug-modal-recording-slot`: the recording field set; outside the desktop app
  it is disabled with the note "Screen recording is available in the desktop
  app".
- `bug-modal-recording-summary`: the attached clip (length, resolution, size);
  `bug-modal-recorder-error`: recorder failures (`role="alert"`).
- `recording-control-bar` (`role="region"`, "Screen recording"),
  `recording-control-status`, `recording-control-time`: the floating bar shown
  while recording (state and elapsed time against the 60 s limit).
- `bug-modal-success`, `bug-modal-archive-path`, `bug-modal-recipient`,
  `bug-modal-subject`, `bug-modal-note-mail`, `bug-modal-note-folder`: the
  success view (archive name and relative path, recipient, subject, and notes
  when the mail client or the reports folder did not open).
- `test-modal-output-console`: test output (`pre`).

Landmarks and headings:

- `main-content` (main view), `telemetry-panel-anchor` (training telemetry).
- `test-modal-title`, `config-editor-modal-title`, `cloud-modal-title`,
  `pipeline-panel-title`, `service-tiles-heading`,
  `service-card-title-{service_id}`, `proj-title-{project}`, `hw-card-title`,
  `hw-card-title-offline`, `health-offline-title`, `toolchain-prereq-title`,
  `drift-matrix-title`, `gui-dependencies-title`, `maintenance-actions-title`,
  `telemetry-stream-heading`, `telemetry-card-heading`.

### 3.10 Controls Without an ID

These controls work but have no `id` yet; tests find them by role and label. The
list is recounted from the `button`, `input`, `select` and `textarea` elements
without an `id` in GUI release `v2.10.57`:

- **Header and shell**: the "Config & Secrets" and "LemGendary AI Documentation
  Hub" buttons, the help tooltip (`?`) buttons, the validation banner and error
  dismiss buttons and the hover pin popovers.
- **Dashboard**: the quick action, Start Service and Stop Service buttons on the
  sidecar tiles, "Start All Services" in the mesh banner, "Start Environment
  Manager" on the hardware card and the health panel, the "Reconcile
  Environment" button on each project card, and the "Copy Stream" and "Clear
  Stream" buttons of the log panel.
- **Pipeline**: the per-step run buttons of the pipeline step cards.
- **Dataset Compiler Suite**: the Catalog, Modernization Queue and Scale
  Reduction sub-tabs; the manifold search box, its clear button, the status,
  format and task filters and "Reset Filters"; the custom compile button; the
  Kaggle ingestion target folder, force check box and "Ingest from Kaggle"; the
  modernization workers input, the push, force and dry-run check boxes, "Scan
  Queue", the run-all and per-row modernize buttons; and "Launch Scale
  Reduction".
- **Model Training Suite**: the model search box, its clear button, the status,
  category and architecture filters and "Reset Filters"; "Start Training Suite",
  Retry and the clear-filters button of the training panel; the per-card batch
  size select; the "Docs & Meta" and "Stage Variations" card actions; the Local
  Process, Remote Cloud and mesh telemetry console tabs with their "Copy
  Stream", "Clear Stream" and "Halt Local Job" buttons; the "Regen Docs & Meta",
  "Stage Variations" and dry-run controls of the variation isolation checker;
  and the close button, auto-pull check box, Cancel, "Launch Cloud Training" and
  publish buttons of the Cloud & Registry Dispatch dialog.
- **Config & Secrets**: the dialog close button; "Validate Syntax", the diff
  toggle, "Revert", "Save Manifest" and the text area of the manifest editor;
  and the add toggle, "Save Secrets to Ecosystem", the default check box,
  Cancel, "Add to Vault", the service shortcut buttons and the per-credential
  set-default and delete buttons of the secrets vault.

### 3.11 Changes Since the Previous Registry

Since the `v2.10.38` registry three IDs were added
(`train-btn-soup-{model_key}`, `kaggle-monitor-slug` and `kaggle-monitor-btn`,
release `v2.10.55`) and none removed. The IDs `compiler-btn-validate-schema`,
`comp-input-max-gb`, `comp-input-workers`, `comp-select-shard-ext`,
`compiler-subtabs-tab-{catalog,queue,reduce}`, `train-select-batch-{key}`,
`train-input-custom-batch-{key}`, `train-btn-docs-{key}`,
`train-btn-stage-{key}`, `training-telemetry-tabs-tab-{local,remote,system}` and
`config-tabs-tab-{manifests,secrets}` named by the 2026-11 audit do not exist in
the source, so they are not listed: the Config & Secrets tabs are
`config-editor-tab-manifests` and `config-editor-tab-secrets` (section 3.8), and
the other controls have no ID (section 3.10).

Before that, the previous registry listed 75 IDs, of which 21 exist in the
code. 54 were removed and 98 added.

Renamed (old ID to current ID): `comp-input-custom-name` to `custom-name-input`,
`comp-select-custom-task` to `custom-task-select`, `comp-select-custom-format`
to `custom-format-select`, `comp-textarea-sources` to `custom-sources-area`,
`comp-select-reduce-manifold` to `reduce-manifold-select`,
`dash-btn-clean-install` to `dash-btn-run-pipeline` (non-destructive; the
destructive run moved to `pipeline-btn-clean-confirm`), `train-card-btn-eval` to
`train-btn-eval-{model_key}`, `train-card-btn-export` to
`train-btn-export-{model_key}`, `train-card-btn-push` to
`train-btn-pub-model-{model_key}`, `train-card-btn-pull` to
`train-btn-pull-model-{model_key}`, `dash-nav-sidebar` to `tab-{tab_id}`.

Removed because the feature no longer exists: `train-select-model`,
`train-btn-launch` (training starts per card), `train-btn-unit-test-all` (moved
into the Test & Diagnostic Orchestrator), `comp-toggle-transcode`, the Kaggle
sub-tab controls (`comp-tab-kaggle-download`, `comp-tab-kaggle-upload`,
`comp-select-kaggle-registry`, `comp-select-kaggle-upload`,
`comp-btn-kaggle-upload`, replaced by the card actions in section 3.5),
`comp-slider-modernize-workers` and the pipeline stage list items
`pipe-stage-*`.

Removed because the control has no ID (section 3.10; `comp-mode-standard`,
`comp-mode-custom`, `comp-input-kaggle-custom-ref` and `train-modal-tab-upload`
exist again since v2.10.28, sections 3.5 and 3.6):
`comp-btn-custom-compile`, `comp-subtab-catalog`,
`comp-subtab-modernize`, `comp-subtab-reduce`, `comp-btn-scan-modernize-queue`,
`comp-btn-batch-modernize-all`, `comp-btn-dispatch-reduce`,
`comp-input-kaggle-custom-ref`, `comp-btn-kaggle-download`,
`pipe-btn-run-step-1` to `pipe-btn-run-step-7`, `pipe-step-status-badge`,
`pipe-step-progress-bar`, `health-table-drift`, `drift-badge-sync`,
`drift-badge-alert`, `telem-log-stream`, `dash-card-hardware`,
`dash-badge-sidecar-status`, `proj-card-training`, `proj-btn-reconcile-datasets`
and `train-modal-tab-upload`.

---

## 4. End-to-End Operational Workflows

### 4.1 Workflow 1: Environment Provisioning & Health Audit

1. The operator starts the LemGendary AI Studio GUI. The sidebar dots and the
   sidecar tiles show which sidecars answer their liveness probe
   (`GET /api/ping` on 8000, `GET /api/health` on 8100 and 8200).
2. The operator clicks `dash-btn-run-pipeline`. The GUI sends
   `POST /api/pipeline/run` (8000) with `clean: false`.
3. Progress arrives over the Environment Manager log socket (`WS /ws/log`,
   8000). Each step card shows its status and a progress bar while it runs.
4. On a terminal event (`success`, `warning` or `error`) the GUI reloads its
   data and, after 1,500 ms, reads `GET /api/pipeline/status` (8000) once more
   to catch late messages.
5. The Health view shows the result of `GET /api/health` (8000), including the
   cross-project version drift matrix.

For a clean reinstall the operator clicks `pipeline-btn-clean-install`, reads
the list of what will be deleted and confirms with `pipeline-btn-clean-confirm`,
which sends `clean: true`.

### 4.1.1 WebSocket Event Lifecycle Recovery

The GUI reacts to these terminal `status` values from the log stream:

- `success`: the pipeline is marked as finished and the data is reloaded; the
  step card shows `PASSED`.
- `warning`: the same, and the step card shows `WARNING`.
- `error`: the pipeline is marked as finished and the error is shown; the step
  card shows `FAILED`.

In all three cases the progress bar is removed and the 1,500 ms status read from
step 4 runs.

### 4.2 Workflow 2: Manifold Compilation

1. The operator opens the Dataset Compiler view (`tab-datasets`).
2. The operator picks a manifold in `comp-select-manifold` and a preset in
   `preset-select` (or keeps "Server default").
3. The operator clicks `comp-btn-compile`. The GUI sends
   `POST /api/gui/quick-compile` (8100) and shows the returned job `id`.
4. Job progress arrives over the Dataset Compiler event socket
   (`WS /api/ws/events`, 8100) and appears in the shared log panel.

### 4.3 Workflow 3: Reporting an Issue

1. The operator clicks `header-btn-report-issue`. The module is preselected from
   the current tab.
2. The operator enters an email and a description of at least 50 characters and
   keeps or clears `bug-modal-telemetry`.
3. Optionally the operator clicks `bug-modal-btn-add-screenshot`, draws a
   highlight in `annotator-canvas` and clicks `annotator-btn-save` (up to 5
   screenshots). In the desktop app the operator can also click
   `bug-modal-btn-start-recording`, reproduce the problem and click
   `recording-btn-stop` (at most 60 s).
4. The operator clicks `bug-modal-btn-submit`. The Environment Manager
   (`POST /api/bug-report`, 8000) saves a ZIP report in the `bug-reports` folder
   of the workspace, opens the mail client with recipient and subject filled in
   and opens the folder.
5. The success view shows the archive path; the operator attaches the ZIP to the
   mail. If the mail client did not open, `bug-modal-btn-copy-address` and
   `bug-modal-btn-copy-subject` copy the details.

---

## 5. Operational Boundaries & Platform Availability

The desktop app runs on Windows, Linux and macOS. What each platform can do
depends on the sidecars and the hardware:

- **Sidecar REST services**: all platforms.
- **Run Pipeline and Clean Install**: full support on Windows and Linux;
  restricted on Windows with DirectML only and on macOS.
- **WebP transcoding**: multi-threaded on Windows and Linux; single-threaded on
  the CPU fallback.
- **Hardlink deduplication**: NTFS and POSIX file systems (`os.link`); not on
  FAT or exFAT.
- **Model training with FP16 or BF16**: CUDA GPUs on Windows and Linux; not on
  DirectML or CPU only.
- **Spatial ladder scaling**: full speed on CUDA GPUs; slower on DirectML; not
  practical on CPU.
- **Screen recording in bug reports**: desktop app on Windows (Windows
  Graphics Capture, app window only); macOS and Linux report "not supported on
  this platform yet"; not available in the browser build.
