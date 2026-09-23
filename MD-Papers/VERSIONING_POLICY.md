# LemGendary Ecosystem: Canonical Versioning Policy & Contract Freezing

## Category 00 POLICY | LemGendary AI Documentation Hub

---

## 1. Abstract & Rationale

Prior to the 2026 unification, repositories across the LemGendary AI ecosystem operated under fragmented versioning conventions: some components utilized calendar versioning (e.g. `v2026.11.1`), while others utilized uncalibrated Semantic Versioning (`v2.3.0` vs `v16.7.3`). This created cognitive friction, complicated cross-project dependency tracking, and triggered false-positive drift warnings in automated CI/CD audits.

This policy establishes the authoritative **Canonical `v16.x.x` Ecosystem Versioning Scheme**, defining how builds, APIs, contracts, and documentation are versioned, frozen, and verified.

---

## 2. The Canonical `v16.x.x` Architectural Framework

All primary repositories in the LemGendary AI Ecosystem adhere to the unified `v16.<minor>.<patch>` iteration standard:

$$\text{Version} = \mathbf{v16}.\langle\text{Minor}\rangle.\langle\text{Patch}\rangle$$

* **Major Version `16` (Epoch Baseline)**: Signifies the complete, post-modernization S.O.L.I.D. architectural era. All packages sharing `v16` guarantee:
  * Strict zero-suppression error telemetry (`0` `# type: ignore`, `0` `# noqa`, `0` `# pylint: disable`).
  * In-process single-responsibility service layers (`services/`).
  * Dual-interface sidecar API daemon readiness (FastAPI + WebSocket).
  * Direct root streaming with bidirectional resumption protocol.
* **Minor Version (`<minor>`)**: Represents major functional phase completions (e.g., Phase 0 Modernization, Phase 3 Transcoding, Phase 7 Sidecar API, Phase 8 CPA Integration).
* **Patch Version (`<patch>`)**: Represents incremental optimizations, bug fixes, benchmark enhancements, and documentation synchronizations.

---

## 3. Component Version Registry

The active canonical versions across all workspace components are synchronized as follows:

| Repository / Component | Runtime Version | Config Manifests | Primary Interface |
| :--- | :--- | :--- | :--- |
| **`lemgendary-datasets`** | `v16.7.3` | `unified_data.yaml` | `python cli.py` / `lemgendary_datasets_hub.ps1` |
| **`lemgendary-training-suite`** | `v16.2.9` | `pyproject.toml` | `python -m training.cli.lemtrain` |
| **`lemgendary-env-manager`** | `v16.2.0` | `pyproject.toml`, `package.json` | `lem-env` / `lemgendary_env_manager.ps1` |
| **`lemgendary-docs`** | `v16.7.3` | `MD-Papers/`, `papers/` | Documentation Hub (`index.html`) |

---

## 4. Standalone Diagnostic Specifications

Specialized clinical or analytical diagnostic frameworks maintain independent specification versions to reflect domain-specific diagnostic taxonomies:

* **Training Pathology Specification (`PAPER_TRAINING_PATHOLOGY.md`)**: Maintained at **`v1.4.0` (Clinical Diagnostic Standard)**. While the training suite that executes these diagnostics operates at `v16.2.9`, the diagnostic taxonomy itself evolves according to independent diagnostic taxonomies.

---

## 5. Frozen Contract Guarantees (OpenAPI 3.1 & Zero Drift)

To ensure zero breaking changes for desktop operators, Tauri Rust backends, and TypeScript frontend clients (`lemgendary-ai-studio-gui`), all sidecar API endpoints adhere to **Frozen Contract Governance**:

1. **Explicit Schema Export**: All REST endpoints are serialized to frozen `openapi.json` files residing in repository roots.
2. **Schema Drift Prohibition**: Modifying route parameters, payload schemas, or response shapes without a minor version increment and regenerated TypeScript client bindings is strictly prohibited.
3. **Automated Assertion Testing**: Unit tests (`tests/unit/test_phase13_gui_presets.py`) actively assert that running FastAPI server route definitions match the frozen `openapi.json` version string.

---

## 6. Ecosystem Enforcement & Audit Gating

Version compliance is enforced at git commit time via the pre-commit compliance validator:

```powershell
lem-env validate --project lemgendary-training-suite,lemgendary-datasets,lemgendary-env-manager,lemgendary-docs
```

Any attempt to introduce calendar versioning (`2026.*`), uncoordinated major version tags (`2.x`), or mismatched package manifest strings is rejected by the pre-commit gate before touching version control.
