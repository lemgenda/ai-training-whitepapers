# Master Operations Manuals Hub

## Category 03 MANUALS | LemGendary Ecosystem

**Author**: Lem Treursic · **Version**: `v16.9.27-STABLE` · **Runtime
Baseline**: `v16.9.16-STABLE` · **Last Reviewed / Verified**: 2026-10-17 ·
**Status**: Canonical

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

The LemGendary AI Ecosystem is governed by three interoperable control planes:
the **LemGendary AI Studio GUI** (presentation tier), the **Master CLI Suite**
(scripted pipeline dispatch), and the **Master Sidecar API** (asynchronous REST,
WebSocket, and IPC services). This manual hub establishes the authoritative
operating procedures, communication contracts, and error remediation pathways
for operators running data synthesis, hyperparameter tuning, model training, and
checkpoint validation across universal hardware.

---

## 2. Interface Control Boundaries

* **Desktop GUI**: Primary Role: Visual orchestration, reactive monitoring;
  Target Protocol: Tauri v2 IPC / WebSocket; Authoritative Manual: [AI Studio
  GUI Operator Manual](./MANUAL_AI_STUDIO_GUI.md)
* **Master CLI**: Primary Role: Automated environment probing, headless
  training; Target Protocol: Direct Python execution; Authoritative Manual:
  [Master CLI Operations Manual](./MANUAL_CLI.md)
* **Master API**: Primary Role: Multi-sidecar background daemons, telemetry
  streaming; Target Protocol: HTTP REST / WebSocket; Authoritative Manual:
  [Master API Manual](./MANUAL_API.md)

---

## 3. Desktop GUI Operational Protocol

The LemGendary AI Studio GUI serves as the primary visual cockpit for machine
learning engineers. Built on Tauri v2 and React 18, it offers
millisecond-latency UI updates without the memory penalty of traditional web
containers. Key capabilities include hardware discovery, synthesis control, and
training management.

---

## 4. Unified CLI Dispatch Matrix

Headless, cloud, and batch scripting operations use deterministic command-line
utilities including `lem-env`, `lemtrain`, and `compiler.py`.

---

## 5. Sidecar Telemetry & IPC Protocols

Asynchronous daemons operate across ports 8000 (Env Manager), 8100 (Compiler),
and 8200 (Training Engine), backed by ACID SQLite persistent job databases.

---

## 6. Cross-Project Automation (CPA)

Cross-Project Automation guarantees that actions triggered in one repository
cleanly propagate throughout the entire ecosystem without manual re-linking.

---

## 7. Conclusion

The Master Operations Manuals Hub establishes clear operational guidelines
across all user-facing and programmatic entrypoints.
