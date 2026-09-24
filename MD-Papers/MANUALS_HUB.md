<!-- markdownlint-disable MD051 MD013 -->
# LemGendary Ecosystem: Master Operations Manuals Hub

**Author**: Lem Treursic  
**Version**: 16.7.3  
**Category**: Category 03 MANUALS  
**Target Hardware**: NVIDIA / Apple Silicon / Intel ARC / CPU

---

## Table of Contents

* [1. Abstract](#1-abstract)
* [2. Interface Control Boundaries](#2-interface-control-boundaries)
* [3. Desktop GUI Operational Protocol](#3-desktop-gui-operational-protocol)
* [4. Unified CLI Dispatch Matrix](#4-unified-cli-dispatch-matrix)
* [5. Sidecar Telemetry & IPC Protocols](#5-sidecar-telemetry--ipc-protocols)
* [6. Cross-Project Automation (CPA)](#6-cross-project-automation-cpa)
* [7. Conclusion](#7-conclusion)

---

## 1. Abstract

The LemGendary AI Ecosystem is governed by three interoperable control planes: the **AI Studio Desktop GUI** (presentation tier), the **Master CLI Suite** (scripted pipeline dispatch), and the **Master Sidecar API** (asynchronous REST, WebSocket, and IPC services). This manual hub establishes the authoritative operating procedures, communication contracts, and error remediation pathways for operators running data synthesis, hyperparameter tuning, model training, and checkpoint validation across universal hardware.

---

## 2. Interface Control Boundaries

| Interface Plane | Primary Role | Target Protocol | Authoritative Manual |
| :--- | :--- | :--- | :--- |
| **Desktop GUI** | Visual orchestration, reactive monitoring | Tauri v2 IPC / WebSocket | [AI Studio GUI Operator Manual](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/MANUAL_AI_STUDIO_GUI.md) |
| **Master CLI** | Automated environment probing, headless training | Direct Python execution | [Master CLI Operations Manual](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/MANUAL_CLI.md) |
| **Master API** | Multi-sidecar background daemons, telemetry streaming | HTTP REST / WebSocket | [Master API Manual](file:///c:/Development/python/model-training/lemgendary-docs/MD-Papers/MANUAL_API.md) |

---

## 3. Desktop GUI Operational Protocol

The AI Studio Desktop GUI serves as the primary visual cockpit for machine learning engineers. Built on Tauri v2 and React 18, it offers millisecond-latency UI updates without the memory penalty of traditional web containers. Key capabilities include hardware discovery, synthesis control, and training management.

---

## 4. Unified CLI Dispatch Matrix

Headless, cloud, and batch scripting operations use deterministic command-line utilities including `lem-env`, `lemtrain`, and `compiler.py`.

---

## 5. Sidecar Telemetry & IPC Protocols

Asynchronous daemons operate across ports 8000 (Env Manager), 8100 (Compiler), and 8200 (Training Engine), backed by ACID SQLite persistent job databases.

---

## 6. Cross-Project Automation (CPA)

Cross-Project Automation guarantees that actions triggered in one repository cleanly propagate throughout the entire ecosystem without manual re-linking.

---

## 7. Conclusion

The Master Operations Manuals Hub establishes clear operational guidelines across all user-facing and programmatic entrypoints.
