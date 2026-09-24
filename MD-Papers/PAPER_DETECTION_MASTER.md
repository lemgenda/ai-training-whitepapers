<!-- markdownlint-disable MD051 MD013 -->
# Architecture of LemGendary AI: Real-Time Detection & Moderation Suite

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 09 VISION  
**Target Hardware**: NVIDIA / Apple Silicon / Intel ARC / CPU

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Visual Manifolds](#2-visual-manifolds)
* [3. YOLOv8n Multi-Task Architecture](#3-yolov8n-multi-task-architecture)
* [4. Universal NSFW Classifier](#4-universal-nsfw-classifier)
* [5. SOTA Architectural Performance Matrix](#5-sota-architectural-performance-matrix)
* [6. Conclusion](#6-conclusion)

---

## 1. Abstract

The **Real-Time Detection & Moderation Suite (Category 09)** decouples real-time geometric scene perception from deep generative moderation. It integrates two specialized vision networks: **YOLOv8n** (an anchor-free multi-task detection, classification, and 17-point pose localization engine) and the **Universal NSFW Classifier** (an EfficientNetV2-S categorical safety filter separating clean photographic art from inappropriate media).

---

## 2. Visual Manifolds

* `LemGendizedYoloV8n`: Bounding box and pose keypoint spatial annotations.
* `LemGendizedClassificationMasterManifoldLarge`: Categorical safety and content filtering.

---

## 3. Dedicated Whitepapers

* [YOLOv8n Multi-Task Whitepaper](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/PAPER_LEMGENDARY_YOLOV8N.md)
* [Universal NSFW Classifier Whitepaper](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/PAPER_LEMGENDARY_NSFW_CLASSIFIER.md)
