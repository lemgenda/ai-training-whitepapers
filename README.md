# LemGendary AI Documentation Hub

> Authoritative technical whitepapers, architectural manuals, API references, CLI guides, and visual demonstrations for the LemGendary AI ecosystem.

---

## Directory Overview

* **`papers/`** — W3C-compliant standalone HTML versions of all 46 technical whitepapers, manuals, and architectural specifications.
* **`MD-Papers/`** — Markdown sources synchronized 1-to-1 with the HTML publications, formatted to strict markdownlint compliance.
* **`assets/`** — Static imagery, training loss curves, architectural flowcharts, and before/after perceptual visual demonstrations.
* **`roadmaps/`** — Strategic planning and implementation roadmap documents.
* **`index.html`** — Central documentation catalog and entry portal.

---

## Changelog

### v16.9.6 — Desktop GUI Kaggle Cloud Synchronization Hub & Multi-Source Custom Compilation

* **`PAPER_DATASET_COMPILER.md` & `PAPER_AI_STUDIO_GUI.md` Synchronization** — Documented the Kaggle Cloud Synchronization & Storage Hub (bidirectional dataset downloads from `unified_data.yaml` registry, custom Kaggle link/slug downloads, and local manifold uploads), multi-source custom dataset synthesis pipeline (`kaggle://`, `hf://`, `gd://`, `gh://`), and fast split-shard discovery caching across 22 compiled manifolds.
* **`MANUAL_AI_STUDIO_GUI.md` & `MANUAL_API.md` Expansion** — Updated Section 5 of the GUI manual with detailed walkthroughs for Standard and Custom Multi-Source compilation modes, documented new REST endpoints (`GET /api/kaggle/registry-datasets`, `POST /api/kaggle/download`, `POST /api/kaggle/upload`, `POST /api/gui/custom-compile`), and synchronized the interactive control dictionary in `GUI_CONTROL_REGISTRY.md`.

### v16.9.1 — Visual Demonstration Remediation (Track B Execution)

* **`assets/` Asset Generation & Conversion** — Generated and optimized 10 high-fidelity perceptual demonstration assets into `assets/`:
  * `codeformer_before.png` & `codeformer_after.png` — Vector-quantized codebook face restoration before/after pair.
  * `film_restorer_before.png` & `film_restorer_after.png` — Analog 35mm celluloid scratch, dust, and dye recovery pair.
  * `upn_v2_before.png` & `upn_v2_after.png` — Multi-degradation composite restoration pair (motion blur, noise, compression).
  * `ultrazoom_before.png` & `ultrazoom_after.png` — Sub-pixel 4x super-resolution architectural crop pair.
  * `yolov8n_before.png` & `yolov8n_after.png` — Real-time spatial object detection and bounding box matrix pair.
* **HTML Whitepaper Remediation (`papers/`)** — Completely eliminated all dashed-border `<div>` placeholders across 9 papers, replacing them with semantic `<img>` elements and descriptive accessibility attributes:
  * `nima-authenticity.html` — Replaced placeholder blocks with `nima_authenticity_fake.png` and `nima_authenticity_real.png`. Synchronized training curve to `nima_authenticity_training.png`.
  * `nima-pro.html`, `nima-mobile.html`, `nima-efficientnet.html` — Replaced placeholder blocks with `technical_compression.png` and `aesthetic_masterpiece.png`.
  * `face-codeformer.html` — Embedded `codeformer_before.png` and `codeformer_after.png`.
  * `hybrid-film-restorer.html` — Embedded `film_restorer_before.png` and `film_restorer_after.png`.
  * `hybrid-upn-v2.html` — Embedded `upn_v2_before.png`, `upn_v2_after.png`, and `upn_v2_training.png`.
  * `ultrazoom.html` — Embedded `ultrazoom_before.png`, `ultrazoom_after.png`, and `ultrazoom_training.png`.
  * `detection-yolov8n.html` — Embedded `yolov8n_before.png` and `yolov8n_after.png`.
* **Markdown Whitepaper Synchronization (`MD-Papers/`)** — Updated all 9 markdown companions (`PAPER_NIMA_*.md`, `PAPER_LEMGENDARY_*.md`) with synchronized visual assessment tables and training curve references.
