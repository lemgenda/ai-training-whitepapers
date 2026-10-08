# LemGendary Ecosystem: Canonical Versioning Policy & Contract Freezing

## Category 01.5 | Subpage of Master Ecosystem Architecture

**Parent Hub**: [Master Ecosystem Architecture](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/ECOSYSTEM_ARCHITECTURE.md)

---

## Table of Contents

- [1. Abstract & Rationale](#1-abstract--rationale)
- [2. The Canonical Ecosystem Versioning Framework](#2-the-canonical-ecosystem-versioning-framework)
- [3. Multi-Track Versioning Taxonomy & Rationale](#3-multi-track-versioning-taxonomy--rationale)
- [4. Component Version Registry](#4-component-version-registry)
- [5. Document Authority Hierarchy](#5-document-authority-hierarchy)
- [6. Standalone Diagnostic & Specialized Specifications](#6-standalone-diagnostic--specialized-specifications)
- [7. Frozen Contract Guarantees (OpenAPI 3.1 & Zero Drift)](#7-frozen-contract-guarantees-openapi-31--zero-drift)
- [8. Ecosystem Enforcement & Audit Gating](#8-ecosystem-enforcement--audit-gating)

---

## 1. Abstract & Rationale

Prior to the 2026 unification, repositories across the LemGendary AI ecosystem operated under fragmented versioning conventions: some components utilized calendar versioning, while others utilized uncalibrated Semantic Versioning (`v2.3.0` vs `v16.7.3`). This created cognitive friction, complicated cross-project dependency tracking, and triggered false-positive drift warnings in automated audits.

This policy establishes the authoritative **Canonical Ecosystem Versioning Scheme** and **Document Authority Hierarchy**, explicitly standardizing multi-track versioning regimes, resolving cross-document authority ambiguities, and defining how builds, APIs, contracts, and documentation are versioned, frozen, and verified.

---

## 2. The Canonical Ecosystem Versioning Framework

All core backend execution engines and orchestrators in the LemGendary AI Ecosystem adhere to the unified `v16.<minor>.<patch>` iteration standard:

$$\text{Version} = \mathbf{v16}.\langle\text{Minor}\rangle.\langle\text{Patch}\rangle$$

- **Major Version `16` (Epoch Baseline)**: Signifies the complete, post-modernization S.O.L.I.D. architectural era. All packages sharing `v16` guarantee:
  - Strict zero-suppression error telemetry (`0` `# type: ignore`, `0` `# noqa`, `0` `# pylint: disable`).
  - In-process single-responsibility service layers (`services/`).
  - Dual-interface sidecar API daemon readiness (FastAPI + WebSocket).
  - Direct root streaming with bidirectional resumption protocol.
- **Minor Version (`<minor>`)**: Represents major functional phase completions (e.g., Phase 0 Modernization, Phase 3 Transcoding, Phase 7 Sidecar API, Phase 8 CPA Integration).
- **Patch Version (`<patch>`)**: Represents incremental optimizations, bug fixes, benchmark enhancements, and documentation synchronizations.

---

## 3. Multi-Track Versioning Taxonomy & Rationale

Different subsystems within the LemGendary AI ecosystem serve different operational domains and therefore adhere to distinct, intentional versioning tracks. Cross-document version differences between these tracks are deliberate and governed as follows:

1. **Core Backend Engines & Services (`v16.x.y`)**:
   - Covers `lemgendary-training-suite`, `lemgendary-datasets`, and `lemgendary-env-manager`.
   - Governs Python microservice sidecars (Ports 8000, 8100, 8200), training loops, skip-index compilers, and dataset containers.
   - Current active state: `v16.9.16-STABLE` (Training Suite), `v16.9.6` (Datasets), `v16.9.3` (Env Manager).
2. **Desktop Operator GUI Client (`v2.x.y` / `v2.0.0`)**:
   - Covers `lemgendary-ai-studio-gui` (Tauri v2 + React 18 + Vite desktop cockpit) and the Operator Manual (`MANUAL_AI_STUDIO_GUI.md`).
   - Version `2.0.0` represents the second-generation Tauri v2 native desktop release (superseding legacy web/Electron prototypes).
   - The GUI client acts as a consumer of the `v16.x.y` sidecar APIs via frozen OpenAPI 3.1 contracts (`openapi.json`).
3. **Master Ecosystem Whitepapers & Specification Baseline (`v16.9.16`)**:
   - Covers `lemgendary-docs`, master architectural maps, and foundational whitepapers.
   - Synchronized directly to the highest active backend engine milestone (`v16.9.16`).
4. **Specialized Diagnostic & Clinical Specifications (`v1.x.y` / `v2.x.y`)**:
   - Covers clinical/diagnostic taxonomy standards such as `PAPER_TRAINING_PATHOLOGY.md` (`v1.4.0`) and algorithmic papers (`ForexPredictor v2.7.1`).
   - These versions reflect domain-specific taxonomy releases rather than software runtime build numbers.

---

## 4. Component Version Registry

The active canonical versions across all workspace components are synchronized as follows:

| Subsystem / Track | Repository / Component | Runtime Version | Config Manifests | Primary Interface |
| :--- | :--- | :--- | :--- | :--- |
| **Training Engine** | `lemgendary-training-suite` | `v16.9.16-STABLE` | `unified_models_v2.yaml` | `python -m training.cli.lemtrain` |
| **Dataset Compiler** | `lemgendary-datasets` | `v16.9.6` | `unified_data.yaml` | `python cli.py` / `lemgendary_datasets_hub.ps1` |
| **Env Manager** | `lemgendary-env-manager` | `v16.9.3` | `pyproject.toml`, `package.json` | `lem-env` / `lemgendary_env_manager.ps1` |
| **Desktop Operator GUI** | `lemgendary-ai-studio-gui` | `v2.0.0` (Client) | `package.json`, `src-tauri/tauri.conf.json` | Tauri v2 Desktop App / Ports 8000/8100/8200 |
| **Documentation Hub** | `lemgendary-docs` | `v16.9.16-STABLE` | `MD-Papers/`, `papers/` | Documentation Hub (`index.html`) |
| **Model Registry** | `LemGendaryModels` | `v16.9.16-STABLE` | `LemGendaryModels/*/README.md` | Authoritative Model Weights & SOTA Exports |

---

## 5. Document Authority Hierarchy

To prevent conflicting statements across documentation and code, the LemGendary AI ecosystem establishes a strict **Document Authority Hierarchy**:

$$\text{Code Manifests (SSOT)} \succ \text{Master Manuals} \succ \text{Architectural Whitepapers} \succ \text{Educational Guides}$$

1. **Level 1 — Single Source of Truth Configuration Manifests**:
   - Manifests: `unified_models_v2.yaml`, `unified_data.yaml`, `presets.yaml`, `openapi.json`.
   - **Authority**: Absolute physical authority for hyperparameters, model architectures, dataset paths, and API schemas.
2. **Level 2 — Master Operational & Technical Manuals**:
   - Documents: `MANUAL_AI_STUDIO_GUI.md`, `MANUAL_CLI.md`, `MANUAL_API.md`, `GUI_CONTROL_REGISTRY.md`.
   - **Authority**: Authoritative for runtime operation, control IDs, CLI flags, REST payloads, and operational guarantees.
3. **Level 3 — Architectural & Technical Whitepapers**:
   - Documents: `ECOSYSTEM_ARCHITECTURE.md`, `PAPER_TRAINING_SUITE.md`, `PAPER_DATASET_COMPILER.md`, `PAPER_AI_STUDIO_GUI.md`, `PAPER_DEGRADATION_ENGINE.md`, `PAPER_TRAINING_PATHOLOGY.md`, and individual model whitepapers.
   - **Authority**: Authoritative for mathematical formulations, asymptotic complexity, hardware memory sentinels, and scientific citations. Must remain concise, project-specific engineering specifications rather than generic introductory AI textbooks.
4. **Level 4 — Educational & Ecosystem Guides**:
   - Documents: `GENERAL_AI_TRAINING_KNOWLEDGE.md`, `GLOSSARY.md`, `LEMGENDARY_CURRENT_STATE.md`.
   - **Authority**: Comprehensive educational and onboarding context, cross-referenced against Levels 1–3. Subservient to Levels 1–3 in the event of any conflict.

---

## 6. Standalone Diagnostic & Specialized Specifications

Specialized clinical or analytical diagnostic frameworks maintain independent specification versions to reflect domain-specific diagnostic taxonomies:

- **Training Pathology Specification (`PAPER_TRAINING_PATHOLOGY.md`)**: Maintained at **`v1.4.0` (Clinical Diagnostic Standard)**. While the training suite executing these diagnostics operates at `v16.9.16`, the diagnostic taxonomy itself evolves according to clinical diagnostic revisions.
- **Forex Predictive Architecture (`PAPER_FOREX_PREDICTOR.md`)**: Maintained at **`v2.7.1` (Quantitative Model Specification)**, executing under the `v16.9.16` engine.

---

## 7. Frozen Contract Guarantees (OpenAPI 3.1 & Zero Drift)

To ensure zero breaking changes for desktop operators, Tauri Rust backends, and TypeScript frontend clients (`lemgendary-ai-studio-gui`), all sidecar API endpoints adhere to **Frozen Contract Governance**:

1. **Explicit Schema Export**: All REST endpoints are serialized to frozen `openapi.json` files residing in repository roots.
2. **Schema Drift Prohibition**: Modifying route parameters, payload schemas, or response shapes without a minor version increment and regenerated TypeScript client bindings is strictly prohibited.
3. **Automated Assertion Testing**: Unit tests (`tests/unit/test_phase13_gui_presets.py`) actively assert that running FastAPI server route definitions match the frozen `openapi.json` version string.

---

## 8. Ecosystem Enforcement & Audit Gating

Version compliance is enforced at git commit time via the pre-commit compliance validator:

```powershell
lem-env validate --project lemgendary-training-suite,lemgendary-datasets,lemgendary-env-manager,lemgendary-docs
```

Any attempt to introduce uncalibrated calendar versioning (`2026.*`), uncoordinated major version tags outside defined tracks, or mismatched package manifest strings is rejected by the pre-commit gate before touching version control.
