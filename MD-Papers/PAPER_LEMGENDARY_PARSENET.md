<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: ParseNet: 19-Class Face Parsing

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 08 FACE  
**Target Hardware**: NVIDIA GeForce GTX 1650 / Apple Silicon / T4

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. The 19 Anatomical Classes](#2-the-19-anatomical-classes)
* [3. Bilateral Boundary Architecture](#3-bilateral-boundary-architecture)
* [4. Boundary-Aware Cross-Entropy Loss](#4-boundary-aware-cross-entropy-loss)
* [5. Mean IoU Targets & Benchmarks](#5-mean-iou-targets--benchmarks)
* [6. Conclusion](#6-conclusion)

---

## 1. Abstract

**ParseNet** is a specialized semantic segmentation network engineered to partition facial imagery into **19 distinct anatomical and accessory classes** with pixel-level precision. Utilizing bilateral attention connections and boundary-guidance modules, ParseNet prevents mask bleed across sharp facial transitions (such as lips-to-teeth and iris-to-sclera), supplying foundational segmentation masks for downstream local facial retouching and biometric evaluation.

---

## 2. The 19 Anatomical Classes

ParseNet segments: Background, Skin, Left Eyebrow, Right Eyebrow, Left Eye, Right Eye, Nose, Upper Lip, Inner Mouth / Teeth, Lower Lip, Hair, Left Ear, Right Ear, Eyeglasses, Earring, Necklace, Neck, Clothing, and Hat.

---

## 3. Bilateral Boundary Architecture

The network splits high-level semantic feature extraction from fine edge localization using a two-stream backbone. A boundary attention branch computes edge probability maps $E_{\text{edge}}$, which directly gate semantic decoding stages.

---

## 4. Boundary-Aware Cross-Entropy Loss

$$\mathcal{L} = \mathcal{L}_{\text{CE}}(Y, \hat{Y}) + \lambda_{\text{Dice}} \mathcal{L}_{\text{Dice}}(Y, \hat{Y}) + \lambda_{\text{edge}} \|E_{\text{gt}} - E_{\text{pred}}\|_2$$

---

## 5. Mean IoU Targets & Benchmarks

| Tissue Region | CelebAMask-HQ mIoU | Edge Boundary F1 |
| :--- | :--- | :--- |
| Eyes & Eyebrows | 0.894 | 0.921 |
| Lips & Mouth | 0.912 | 0.938 |
| Global Face Skin | 0.958 | 0.965 |

---

## 6. Conclusion

ParseNet delivers the surgical spatial boundaries required for component-aware facial processing in the LemGendary AI Ecosystem.
