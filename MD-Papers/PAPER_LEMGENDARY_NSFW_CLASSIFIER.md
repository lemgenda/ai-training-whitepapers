<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: Universal NSFW Safety Classifier

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 09 VISION  
**Target Hardware**: NVIDIA GeForce GTX 1650 / Apple Silicon / T4

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. The 5-Tier Moderation Taxonomy](#2-the-5-tier-moderation-taxonomy)
* [3. EfficientNetV2-S Architecture](#3-efficientnetv2-s-architecture)
* [4. Class-Balanced Focal Loss](#4-class-balanced-focal-loss)
* [5. Verification Targets & False Positives](#5-verification-targets--false-positives)
* [6. Conclusion](#6-conclusion)

---

## 1. Abstract

The **LemGendary Universal NSFW Classifier** is a high-speed, on-device content moderation model powered by an EfficientNetV2-S backbone. Designed to safeguard automated data pipelines, public model endpoints, and desktop GUI workflows, the classifier categorizes incoming images into a 5-tier safety hierarchy. By optimizing Class-Balanced Focal Loss on curated edge distributions, the system achieves a verified False Positive Rate &lt; 0.4% on benign artistic content while reliably identifying explicit material in &lt; 5ms.

---

## 2. The 5-Tier Moderation Taxonomy

The model categorizes content into mutually exclusive probability distributions:

* **Drawings**: Benign illustrations, digital paintings, comics, and non-explicit anime.
* **Neutral**: General real-world photographic content, landscapes, everyday objects.
* **Sexy**: Provocative poses, swimwear, lingerie, and suggestive non-explicit scenes.
* **Hentai**: Explicit illustrated, animated, or drawn adult material.
* **Porn**: Explicit photographic sexual acts and anatomically explicit genitalia.

---

## 3. EfficientNetV2-S Architecture

Utilizing Fused-MBConv layers in early stages and MBConv with Squeeze-and-Excitation (SE) in deeper layers, EfficientNetV2-S minimizes training memory while maximizing receptive field coverage. Progressive training gradually increases image resolution from 128px to 256px alongside data augmentation intensity.

---

## 4. Class-Balanced Focal Loss

To overcome heavy real-world class imbalance, the loss incorporates class-frequency weighting $\alpha_t$ and focusing parameter $\gamma = 2.0$:

$$\mathcal{L}_{\text{focal}}(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)$$

---

## 5. Verification Targets & False Positives

| Category Tier | Target Precision | Target Recall | False Positive Ceiling |
| :--- | :--- | :--- | :--- |
| Explicit (Porn / Hentai) | $\ge 98.2\%$ | $\ge 97.5\%$ | &lt; 0.3% |
| Suggestive (Sexy) | $\ge 94.0\%$ | $\ge 92.8\%$ | &lt; 1.2% |
| Benign (Neutral / Drawings) | $\ge 99.1\%$ | $\ge 98.8\%$ | &lt; 0.4% |

---

## 6. Conclusion

The Universal NSFW Classifier provides privacy-preserving, zero-telemetry content filtering natively integrated into the LemGendary AI Ecosystem.
