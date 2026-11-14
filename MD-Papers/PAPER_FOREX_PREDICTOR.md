# Multi-Scale CNN-Transformer Forex & Commodity Predictor

## Category 11 FINANCIAL | Architecture of LemGendary AI

**Author**: Lem Treursic · **Version**: `v16.9.214-STABLE` · **Paper Revision**:
2.9.0 - Quantitative Manifold Matrix (2026 Specialization - v17.7 Engine) ·
**Target `[TARGET]` Hardware**: NVIDIA GeForce GTX 1650 (4GB) / Apple Silicon
(MPS) / Intel ARC (XPU) / High-Frequency Low-Latency MT5 Engine

---

## Table of Contents

- [1. Abstract](#1-abstract)
  - [1.1 What ForexPredictor Does (In Plain
    English)](#11-what-forexpredictor-does-in-plain-english)
- [2. Visual Taxonomy: Multi-Asset & Temporal
  Manifolds](#2-visual-taxonomy-multi-asset--temporal-manifolds)
  - [2.1 The Titan Four Asset Universe](#21-the-titan-four-asset-universe)
  - [2.2 The 16-Symbol Financial Foundation
    Model](#22-the-16-symbol-financial-foundation-model)
  - [2.3 Future Expansion Strategy (Crosses &
    Exotics)](#23-future-expansion-strategy-crosses--exotics)
  - [2.4 Multi-Timeframe Confluence
    Ladder](#24-multi-timeframe-confluence-ladder)
- [3. Shared Foundations](#3-shared-foundations)
  - [3.1 Causal Convolution & Temporal
    Invariance](#31-causal-convolution--temporal-invariance)
  - [3.2 Cross-Timeframe Multi-Head Attention
    Fusion](#32-cross-timeframe-multi-head-attention-fusion)
  - [3.3 6-Fold Anchored Walk-Forward Cross-Validation
    Matrix](#33-6-fold-anchored-walk-forward-cross-validation-matrix)
  - [3.4 Quantitative Evaluation Formulations &
    Scoring](#34-quantitative-evaluation-formulations--scoring)
  - [3.5 Memory Complexity Scaling Bounds](#35-memory-complexity-scaling-bounds)
- [4. Model Deep-Dive: LemGendary
  ForexPredictor](#4-model-deep-dive-lemgendary-forexpredictor)
  - [4.1 Model Description, Purpose and
    Usage](#41-model-description-purpose-and-usage)
  - [4.2 Model Info](#42-model-info)
  - [4.3 Manifold Info](#43-manifold-info)
  - [4.4 Performance Metrics](#44-performance-metrics)
  - [4.5 Training Curve](#45-training-curve)
  - [4.6 Model Specific Issues and
    Optimizations](#46-model-specific-issues-and-optimizations)
  - [4.7 Consolidated SOTA Benchmarks](#47-consolidated-sota-benchmarks)
  - [4.8 Training Process Analysis](#48-training-process-analysis)
- [5. Challenges & Resilience
  Architecture](#5-challenges--resilience-architecture)
  - [5.1 Lookahead Leakage Elimination (Strict Embargo
    Gaps)](#51-lookahead-leakage-elimination-strict-embargo-gaps)
  - [5.2 Anti-Hold Manifold Collapse (Entropy
    Regularization)](#52-anti-hold-manifold-collapse-entropy-regularization)
  - [5.3 Spread Friction & Dynamic Slippage
    Simulation](#53-spread-friction--dynamic-slippage-simulation)
  - [5.4 Risk-Adjusted Position Sizing via Fractional
    Kelly](#54-risk-adjusted-position-sizing-via-fractional-kelly)
  - [5.5 Sub-5ms Real-Time Inference
    Deployment](#55-sub-5ms-real-time-inference-deployment)
- [6. Deployment Strategy: MetaTrader 5 Expert Advisor
  Bridge](#6-deployment-strategy-metatrader-5-expert-advisor-bridge)
  - [6.1 Stateless ONNX Model Export
    `[THEORETICAL]`](#61-stateless-onnx-model-export-theoretical)
  - [6.2 Automated Real-Time Tick
    Ingestion](#62-automated-real-time-tick-ingestion)
  - [6.3 Generated MQL5 Expert Advisor & MT5 Artefact (v16.9.185,
    v16.9.192)](#63-generated-mql5-expert-advisor--mt5-artefact-v169185-v169192)
- [7. SOTA Architectural Performance
  Matrix](#7-sota-architectural-performance-matrix)
- [8. Conclusion](#8-conclusion)

---

## 1. Abstract

This paper presents the theoretical design, mathematical formulation, and
production verification of the **LemGendary ForexPredictor**, a deep multi-scale
quantitative architecture designed for multi-currency algorithmic trading across
MetaTrader 5 environments. Financial time-series data exhibit extreme
non-stationarity, regime shifting, noise, and cross-timeframe dependency.
Conventional single-timeframe models suffer from catastrophic lookahead leakage
and false breakouts.

The LemGendary ForexPredictor integrates per-timeframe **Causal Dilated
Convolutional Networks (TCN)** with a **Cross-Timeframe Multi-Head Attention
(CT-MHA)** fusion layer and dynamic pair embeddings. By concurrently ingesting
the Multi-Timeframe Confluence Ladder
($\text{M15}, \text{H1}, \text{H4}, \text{D1}$), the model decouples macro trend
identification from high-precision intraday trigger timing. Training runs
over an **Anchored 6-Fold Walk-Forward Matrix (2019–2026)** with a 14-day
anti-leakage embargo gap. No validation epoch has produced a valid
measurement yet: the two recorded `metrics.csv` rows are a copy of the
registry targets and an epoch without trades (Section 4.4). Every result
figure in this paper is therefore **not yet measured**; the figures shown in
earlier revisions (for example Directional Accuracy 49.69%) are removed. Live
capital deployment stays gated until measured results reach the registry
targets. Sub-5 ms ONNX inference is a target; its latency is not yet
measured.

---

## 1.1 What ForexPredictor Does (In Plain English)

Imagine an algorithmic market analyst watching currency charts across 4
different timeframes simultaneously before making an investment call:

- **Multi-Timeframe Vision:** Instead of staring only at 15-minute price blips
  (which are noisy and cause whipsaws), the model checks the 15-Minute, 1-Hour,
  4-Hour, and Daily charts together. It identifies macro trends on the Daily
  chart and uses the 15-minute chart purely to pinpoint entry triggers.
- **Leakage-Free Temporal Guardrails:** Standard machine learning models often
  accidentally cheat during backtesting by peeking into future price data.
  ForexPredictor enforces strict causal convolutions and a mandatory 14-day
  embargo gap between training and testing periods.
- **Sub-5ms Execution Latency (Target):** Once trained, the model exports to
  compact ONNX format and is designed to calculate buy, sell, or neutral
  predictions within 5 milliseconds directly inside MetaTrader 5 Expert
  Advisors. The latency is not yet measured.

### Multi-Timeframe Confluence & Risk Matrix

- **M15 (15 Minutes)**: Temporal Resolution: Micro-Structure; Core Role in
  Predictive Synthesis: High-frequency trigger timing & spread friction
  evaluation
- **H1 (1 Hour)**: Temporal Resolution: Intraday Momentum; Core Role in
  Predictive Synthesis: Session volume dynamics & swing level confirmation
- **H4 (4 Hours)**: Temporal Resolution: Interday Structure; Core Role in
  Predictive Synthesis: Structural trend boundaries & support/resistance zones
- **D1 (Daily)**: Temporal Resolution: Macro Regime; Core Role in Predictive
  Synthesis: Major monetary policy trends & carry-trade direction

---

## 2. Visual Taxonomy: Multi-Asset & Temporal Manifolds

### 2.1 The Titan Four Asset Universe

The primary production deployment focuses on the **Titan Four** core
instruments (`TITAN_PAIRS` in `data/forex_spec.py`), three of the most liquid
currency pairs and spot gold, while maintaining an extensible embedding table
supporting up to 16 multi-asset classes:

1. **EURUSD (Euro / US Dollar)**: Global reserve liquidity benchmark; highly
   responsive to ECB/Fed interest rate differentials and macro momentum.
2. **GBPUSD (British Pound / US Dollar)**: High-beta currency pair characterized
   by expansive London session volatility and intraday trend continuation.
3. **USDJPY (US Dollar / Japanese Yen)**: Macro carry-trade barometer sensitive
   to sovereign yield curve divergence and Bank of Japan monetary interventions.
4. **XAUUSD (Spot Gold / US Dollar)**: Leading physical commodity asset serving
   as an inflation hedge and geopolitical safe-haven with non-linear volatility
   clustering.

$$
\mathcal{U}_{\text{core}} = \{ \text{EURUSD}, \text{GBPUSD}, \text{USDJPY},
\text{XAUUSD} \}
$$

### 2.2 The 16-Symbol Financial Foundation Model

The overarching strategy of the LemGendary ForexPredictor is to construct a
**Financial Foundation Model**. Financial markets are not isolated bubbles; they
are a deeply interconnected ecosystem. For instance, when global equities (e.g.,
US500, GER40) experience severe drawdowns, capital typically flows into
safe-haven assets (XAUUSD spikes, USDJPY drops). By exposing the neural network
to 16 diverse assets simultaneously during training, the model is forced to
learn these hidden macro-economic correlations. This Cross-Asset Regularization
prevents the model from overfitting to the micro-structure of a single currency
pair, yielding a vastly more intelligent and resilient core brain that
understands universal market dynamics.

The 16-symbol physical manifold (`LemGendizedForexUniverseLarge`, 2019–2026)
holds 26,818,700 rows (the training registry count of
`LemGendizedForexUniverse`) across G7 currency pairs, precious metals, crude
energy, and major equity indices:

$$
\mathcal{U}_{\text{universe}} = \mathcal{U}_{\text{core}} \cup \{ \text{USDCAD},
\text{USDCHF}, \text{AUDUSD}, \text{NZDUSD}, \text{EURJPY}, \text{GBPJPY},
\text{EURGBP}, \text{XAGUSD}, \text{USOIL}, \text{US500}, \text{NAS100},
\text{DE40} \}
$$

To resolve heterogeneous brokerage ticker nomenclatures across live MetaTrader 5
terminals, the ingestion engine implements bidirectional **Symbol Aliasing**
($\text{NAS100} \leftrightarrow \text{USTEC}$,
$\text{DE40} \leftrightarrow \text{GER40}$). Alternate symbols are dynamically
mapped to canonical embedding indices and pip scale configurations, preventing
missing tensor key errors during multi-broker deployment.

### 2.3 Future Expansion Strategy (Crosses & Exotics)

While the 16-symbol Foundation Model covers the most liquid majors, metals,
energy and indices, extending the network into illiquid markets requires a
specialized deployment strategy:

1. **Crosses Extension Model**: A dedicated model trained on secondary crosses
   (e.g., AUDCAD, NZDCHF) that are less liquid than the G7 Majors but still
   maintain stable micro-structure.
2. **Exotics Extension Model**: An entirely isolated model for exotic pairs
   (e.g., USDTRY, USDMXN). Exotics suffer from massive spreads, severe noise,
   and unpredictable central bank manipulations. Injecting them into the primary
   16-symbol Foundation Model risks poisoning the core weights. Isolating them
   ensures the primary model remains uncorrupted while providing a bespoke
   solution for high-volatility, low-liquidity environments.

### 2.4 Multi-Timeframe Confluence Ladder

Professional quant traders evaluate confluence across multiple temporal
resolutions. The Smart Governor executes a progressive curriculum ladder across
6 canonical rungs:

$$
\text{TIMEFRAME\_RUNGS} = [1, 5, 15, 60, 240, 1440]
$$

- **D1 (1440m)**: Lookback Window ($L_m$): 252 bars; Temporal Horizon: ~1
  Trading Year; Strategic Purpose: Macro Trend, Regime Classification,
  Structural Support/Resistance
- **H4 (240m)**: Lookback Window ($L_m$): 90 bars; Temporal Horizon: ~2.5 Weeks;
  Strategic Purpose: Intermediate Trend Momentum, Swings & Volatility Regimes
- **H1 (60m)**: Lookback Window ($L_m$): 168 bars; Temporal Horizon: ~1 Week;
  Strategic Purpose: Intraday Trend Direction & Volume Delta Confirmation
- **M15 (15m)**: Lookback Window ($L_m$): 192 bars; Temporal Horizon: ~2 Days;
  Strategic Purpose: High-Precision Trigger Timing & Tight Stop-Loss Placement
- **M5 (5m)**: Lookback Window ($L_m$): 288 bars; Temporal Horizon: ~1 Day;
  Strategic Purpose: Microstructure Order-Flow Refinement
- **M1 (1m)**: Lookback Window ($L_m$): 512 bars; Temporal Horizon: ~8.5 Hours;
  Strategic Purpose: Execution Scalping & Slippage Minimization

---

## 3. Shared Foundations

### 3.1 Causal Convolution & Temporal Invariance

To strictly prevent future lookahead leakage, all convolutional operations
employ left-sided zero padding. The dilated causal Conv1D operator at time $t$
for dilation rate $d$ and kernel size $K$ is defined as:

$$
\mathbf{h}_t = \text{GELU}\left( \sum_{k=0}^{K-1} \mathbf{W}_k \cdot
\mathbf{x}_{t - d \cdot k} + \mathbf{b} \right)
$$

By cascading $M$ layers with exponentially increasing dilation $d = 2^m$ for
$m \in \{0, 1, \dots, M-1\}$, the receptive field expands exponentially without
downsampling:

$$
\text{RF} = 1 + \sum_{m=0}^{M-1} (K - 1) \cdot 2^m = 1 + (K - 1)(2^M - 1)
$$

```text
Input Sequence:   x[t-3]   x[t-2]   x[t-1]   x[t]
                    \        \        \       /
Layer 1 (d=1):     h1[t-2]  h1[t-1]  h1[t]
                      \        \      /
Layer 2 (d=2):        h2[t-1]  h2[t]
                         \     /
Output Embedding:         z[t] (Zero Future Information Flow)
```

The CausalConv1D blocks implement **Stochastic Depth** (drop-path
regularization), which randomly drops entire layers during training, forcing the
network to learn robust, noise-invariant temporal features and preventing
overfitting to market idiosyncrasies.

### 3.2 Cross-Timeframe Multi-Head Attention Fusion

Given $T$ active timeframes, each timeframe encoder yields a summary
representation $\mathbf{z}_m \in \mathbb{R}^{d_{\text{model}}}$. The timeframe
embeddings are stacked into matrix
$\mathbf{Z} \in \mathbb{R}^{T \times d_{\text{model}}}$. Cross-timeframe
multi-head attention computes dynamic relational weights between all temporal
horizons:

$$
\mathbf{Q} = \mathbf{Z} \mathbf{W}_Q, \quad \mathbf{K} = \mathbf{Z}
\mathbf{W}_K, \quad \mathbf{V} = \mathbf{Z} \mathbf{W}_V
$$

$$
\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(
\frac{\mathbf{Q} \mathbf{K}^T}{\sqrt{d_k}} \right) \mathbf{V}
$$

$$
\mathbf{e}_{\text{fused}} = \text{Concat}\left(\text{head}_1, \dots,
\text{head}_h\right) \mathbf{W}_O + \mathbf{E}_{\text{pair}}(p)
$$

where $\mathbf{E}_{\text{pair}}(p) \in \mathbb{R}^{d_{\text{model}}}$ is the
learned pair embedding representing currency-specific volatility dynamics.

#### Timeframe Dropout Regularizer ($p=0.15$)

To prevent the attention mechanism from over-relying on high-frequency noise
from any single temporal rung or suffering from co-adaptation across adjacent
horizons, the fusion block incorporates **Timeframe Dropout Regularization**.
During training when $T > 1$ timeframes are active, a stochastic masking vector
$\mathbf{m} \in \{0, 1\}^T$ is sampled with drop probability
$p_{\text{tf}} = 0.15$:

$$
m_j \sim \text{Bernoulli}(1 - p_{\text{tf}}), \quad j \in \{1, \dots, T\}
$$

To eliminate catastrophic information blackout where all timeframes are dropped
simultaneously, an unconditional fallback gate ensures at least one timeframe
remains active:

$$
\mathbf{m}^* = \begin{cases} \mathbf{m}, & \text{if } \sum_{j=1}^T m_j > 0 \\
\mathbf{e}_{j^*}, \quad j^* \sim \mathcal{U}(1, T), & \text{if } \sum_{j=1}^T
m_j = 0 \end{cases}
$$

The masked timeframe embedding matrix
$\tilde{\mathbf{Z}} = \mathbf{Z} \odot (\mathbf{m}^*
\mathbf{1}_{d_{\text{model}}}^T)$ is then supplied to the cross-timeframe
projection matrices
($\mathbf{Q} = \tilde{\mathbf{Z}} \mathbf{W}_Q, \mathbf{K} = \tilde{\mathbf{Z}}
\mathbf{W}_K, \mathbf{V} = \tilde{\mathbf{Z}} \mathbf{W}_V$). This forces each
temporal encoder to maintain standalone predictive utility while compelling the
attention fusion layer to learn robust inter-temporal representations.

### 3.3 6-Fold Anchored Walk-Forward Cross-Validation Matrix

Time-series cross-validation must strictly preserve chronological order.
Standard random $K$-fold cross-validation suffers from lookahead leakage. The
LemGendary dataset compiler implements a strictly isolated, **6-Fold
Expanding-Window Walk-Forward Matrix** (2019–2026) with a 14-day anti-leakage
embargo gap between training partitions and evaluation windows:

```text
Fold 1: Train [2019-2020] -> Validation [2021] (Baseline & Recovery Stress)
Fold 2: Train [2019-2021] -> Validation [2022] (Global Rate Hikes & Dollar Surge)
Fold 3: Train [2019-2022] -> Validation [2023] (Inflation Peaks & Regime Shifts)
Fold 4: Train [2019-2023] -> Validation [2024] (Central Bank Pivot)
Fold 5: Train [2019-2024] -> Validation [2025] (Modern High-Fidelity Consolidations)
Fold 6: Train [2019-2025] -> Validation [2026] (Current Live Market Out-of-Sample)
```

### 3.4 Quantitative Evaluation Formulations & Scoring

Model predictions are evaluated using both classification accuracy and rigorous
quantitative trading metrics:

#### 1. Directional Accuracy & Win Rate

$$
\text{DirAcc} = \frac{1}{N} \sum_{i=1}^N
\mathbb{I}\left(\hat{y}_{\text{dir}}^{(i)} = y_{\text{dir}}^{(i)}\right) \times
100\%
$$

$$
\text{WinRate} = \frac{\sum_{i \in \text{Trades}} \mathbb{I}\left(R_i >
0\right)}{N_{\text{trades}}} \times 100\%
$$

#### 2. Profit Factor & Return Metrics

$$
\text{Profit Factor} = \frac{\sum_{i: R_i > 0} R_i}{\sum_{j: R_j < 0} |R_j|}
$$

#### 3. Annualized Sharpe & Sortino Ratios

$$
\text{Sharpe} = \frac{\mathbb{E}[R] - R_f}{\sigma(R)} \times \sqrt{252 \times
24}, \quad \text{Sortino} = \frac{\mathbb{E}[R] -
R_f}{\sigma_{\text{downside}}(R)} \times \sqrt{252 \times 24}
$$

$$
\sigma_{\text{downside}} = \sqrt{\frac{1}{N} \sum_{i: R_i < 0} R_i^2}
$$

#### 4. Maximum Drawdown (Equity Model)

$$
\text{MaxDD} = \max_{k} \left( \frac{\max_{j \le k} E_j - E_k}{\max_{j \le k}
E_j} \right) \times 100\%
$$

Since Training Suite v16.9.164 and v16.9.184 the validation MaxDD is a real
percentage of an explicit equity model (the older cumulative-pip measure over
a fixed pip base is withdrawn): every trade risks the
fraction $r$ = `evaluation.risk_per_trade` of the equity (registry, default
0.01, valid $0 < r \le 0.05$), a win returns $TP/SL$ R and a loss $-1$ R,
and equity compounds from 1.0, $E_{k+1} = E_k (1 + r R_k)$. MaxDD is the
largest peak-to-trough fall of $E$ in percent of the peak. An epoch without
a directional prediction reports no win rate, profit factor, Sharpe,
Sortino or drawdown.

#### 5. Scalar Quantitative Quality Score

Before Training Suite v16.9.164 the score was (historical, no longer used):

$$
\text{Quality Score} = (\text{DirAcc} \times 1.0) + (\text{WinRate} \times 1.0)
+ (\text{ProfitFactor} \times 10.0) + (\text{Sharpe} \times 10.0) -
(\text{MaxDD} \times 1.0)
$$

Since Training Suite v16.9.164 Forex epochs use the shared weighted score
(scheme `forex_weighted_targets_v2_risk0.01`, the risk is part of the id)
over the SOTA targets measured that epoch:

$$
Q = 5 \cdot \text{DirAcc} + 5 \cdot \text{WinRate} +
10 \cdot \text{PF}^{[0, 10]} + 10 \cdot \text{Sharpe}^{[-5, 10]} +
10 \cdot \text{Sortino}^{[-5, 10]} + \max(0, 100 - \text{MaxDD}) +
\max(0, 50 - \text{TPMAE}) + \max(0, 50 - \text{SLMAE})
$$

A superscript range is a clip applied inside the score only; TPMAE and SLMAE
are the take-profit and stop-loss mean absolute errors in pips. Reported
metrics keep their measured values. An unmeasured or degenerate epoch (no
target measured, a non-finite score, or no trade) never becomes `best.pth`.

### 3.5 Memory Complexity Scaling Bounds

The memory footprint during multi-timeframe ingestion scales linearly with the
number of active timeframes and batch size:

$$
\text{Mem}_{\text{total}} = \mathcal{O}\left( B \cdot \sum_{m=1}^T L_m \cdot
C_{\text{feat}} + B \cdot T \cdot d_{\text{model}} \right)
$$

$$
\text{Mem}_{\text{peak}} = \mathcal{O}\left( B \cdot \max_{m} (L_m) \cdot
d_{\text{model}} \right)
$$

For $B = 32$, $\max_m L_m = 512$ (M1) and $d_{\text{model}} = 192$, one FP32
activation tensor of that shape is $32 \cdot 512 \cdot 192 \cdot 4$ bytes
$\approx 12.6$ MB. This is arithmetic for one tensor, not a measured peak; the
measured peak memory is not yet recorded.

### 3.6 Apache Parquet Columnar Sharding & Zstandard Compression (v16.8.0)

The v16.8.0 storage modernization introduces native Apache Parquet columnar
sharding with Zstandard level 3 block compression for the 26.8M-row Forex
universe:

- **Footprint Reduction**: Consolidates 16 currency pairs across 6 timeframe
  tiers into contiguous annual Parquet partitions
  (`ForexUniverse{year}.parquet`). The footprint figures are owned by the
  [Dataset Compiler paper](./PAPER_DATASET_COMPILER.md) (Section 2.1) and are
  not repeated or re-measured here.
- **Cluster Slack Elimination**: Eliminates thousands of loose `.npy` sliding
  window files, eradicating NTFS 4KB cluster slack allocation waste.
- **Zero-Copy Columnar Ingestion**: Employs `pyarrow.parquet` with LRU row-group
  caching for batch tensor recovery directly into contiguous memory buffers
  (recovery latency not yet measured).

This minimal memory complexity allows real-time evaluation on consumer hardware
and low-latency edge deployment.

---

## 4. Model Deep-Dive: LemGendary ForexPredictor

### 4.1 Model Description, Purpose and Usage

The **ForexPredictor** outputs dual synchronous heads:

1. **Direction Head ($\hat{\mathbf{y}}_{\text{dir}}$)**: 3-class probability
   distribution
   ($\text{Class } 0 = \text{SELL}, \text{Class } 1 = \text{HOLD}, \text{Class }
   2 = \text{BUY}$).
2. **Magnitude Head ($\hat{\mathbf{y}}_{\text{mag}}$)**: Continuous
   2-dimensional regression predicting optimal Take-Profit ($\text{TP}$) and
   Stop-Loss ($\text{SL}$) boundaries in Normalized Pip Units (NPUs,
   $[0, 100]$), normalized across varied asset classes via dynamic pair scaling
   factors ($\text{NPU} = \text{Raw Pips} / \text{PAIR\_PIP\_SCALE}$).

$$
\mathcal{L}_{\text{total}} = 0.5 \cdot
\mathcal{L}_{\text{Focal}}(\hat{\mathbf{y}}_{\text{dir}},
\mathbf{y}_{\text{dir}}) + 0.02 \cdot
\mathcal{L}_{\text{Huber}}(\hat{\mathbf{y}}_{\text{mag}},
\mathbf{y}_{\text{mag}}) - \lambda_{\mathcal{H}} \cdot
\mathcal{H}(\sigma(\hat{\mathbf{y}}_{\text{dir}}))
$$

### 4.2 Model Info

- **Model Key**: `forex_predictor`
- **Architecture**: Multi-Scale Causal TCN + Cross-Timeframe Attention (with
  Stochastic Depth)
- **Embedding Dimension ($d_{\text{model}}$)**: 192
- **Attention Heads**: 6
- **Parameters**: 3.5358M FP32 Parameters (~14 MB; registry `parameters_m`,
  measured from the code since Training Suite v16.9.221)
- **Primary Checkpoint**: `[CURRENT]` `ForexPredictorWeights_FP32.pth`
- **ONNX Export**: `ForexPredictor.onnx` (opset 18, FP16 graph with FP32
  inputs and outputs, IR 9, embedded weights for MetaTrader 5)

### 4.3 Manifold Info

- **Dataset Identifier**: `LemGendizedForexUniverseLarge` (Unified 16-Symbol
  Financial Foundation Manifold)
- **Total Physical Samples**: 26,818,700 rows (2019–2026) across 16 symbols
  and 6 timeframe rungs (training registry
  `_registry_metadata.datasets.LemGendizedForexUniverse.count`)
- **Broker Symbol Aliases**: `NAS100` $\leftrightarrow$ `USTEC`, `DE40`
  $\leftrightarrow$ `GER40`
- **Normalized Features (14)**: Open, High, Low, Close, Tick Volume, RSI (14),
  MACD (12,26,9), MACD Signal, ATR (14), Bollinger Band Width (20,2), Session
  Sine, Session Cosine, ATR Percentile, Bar Range Ratio.

### 4.4 Performance Metrics

**Status: not yet measured.** The owner's Forex `metrics.csv` holds two rows,
and neither is a valid measurement:

- **Row 1 (fold 1, epoch 1)** equals the registry `sota_targets` digit for
  digit (58.5 / 56 / 1.65 / 1.85 / 2.1 / 12 / 12.5 / 12.5) with
  `Quality_Score` = 100 − `Val_Loss` (99.7291). No committed version of the
  validation code writes such a row; since Training Suite v16.9.164 a row
  whose target columns equal the targets is skipped.
- **Row 2 (fold 1, epoch 2)** opened no trade: `WinRate` equals `DirAcc`,
  Sharpe and Sortino are pinned at −5 and MaxDD at 100 by clips that
  v16.9.164 removed. Since v16.9.164 such an epoch reports no trade metrics
  and never becomes `best.pth`.

The result figures of earlier revisions (Direction Accuracy and Win Rate
49.69%, Profit Factor 0.99, Sharpe −0.16, Sortino −0.18, TP MAE 615.42, SL MAE
617.95, Quality Score 105.87, the withdrawn 665.80% drawdown) and the LSTM and
vanilla Transformer comparison columns have no backing measurement or source
and are removed. The targets below are the registry `sota_targets` of
`forex_predictor` (`unified_models_v2.yaml`):

- **Direction Accuracy**: Measured: not yet measured; Target: 58.5%
  (higher is better)
- **Trade Win Rate**: Measured: not yet measured; Target: 56.0% (higher is
  better)
- **Profit Factor**: Measured: not yet measured; Target: 1.65 (higher is
  better)
- **Sharpe Ratio**: Measured: not yet measured; Target: 1.85 (higher is
  better)
- **Sortino Ratio**: Measured: not yet measured; Target: 2.1 (higher is
  better)
- **Max Drawdown (equity model, 1% risk)**: Measured: not yet measured;
  Target: 12.0% (lower is better)
- **TP MAE (pips)**: Measured: not yet measured; Target: 12.5 (lower is
  better)
- **SL MAE (pips)**: Measured: not yet measured; Target: 12.5 (lower is
  better)
- **Quality Score**: Measured: not yet measured; Target: the weighted score
  of the targets above (Section 3.4), not a separate fixed number

#### 4.4.1 What a Valid Measured Run Must Produce

A Forex result may be reported here only when it comes from a run that:

1. Writes `metrics.csv` with Training Suite v16.9.184 or later (equity-model
   MaxDD at `evaluation.risk_per_trade`, score scheme
   `forex_weighted_targets_v2_risk0.01`), from a completed validation epoch
   on the walk-forward validation window of a named fold.
2. Has target columns that are measured values, not a copy of the registry
   targets (such rows are skipped by the engine).
3. Opened at least one trade, so win rate, profit factor, Sharpe, Sortino and
   MaxDD are present; an empty cell means not measured and is reported as
   such, never as 0 or as the target.
4. Has a finite `Quality_Score` and a matching checkpoint (`best.pth` or a
   vault checkpoint) whose governor state records the score scheme id.
5. Names the fold, the epoch, the active timeframes and pairs, and the code
   version, so that the row can be traced.

Latency figures additionally need a committed benchmark (device, runtime,
batch size, number of runs, mean and P95).

### 4.5 Training Curve

No training curve is shown: no measured epoch exists yet. The earlier chart
was not drawn from a valid measurement and is withdrawn. A new chart will plot
every completed epoch of a valid run's `metrics.csv`.

### 4.6 Model Specific Issues and Optimizations

1. **Focal Loss Regularization**: We replace standard Cross-Entropy with a focal
   loss ($\gamma = 2.0$) heavily penalizing false convictions and asymmetric
   class weights ([1.3, 0.7, 1.3]) to avert class collapse into the
   Sideways/Hold category.
2. **Directional Entropy (DirEntropy)**: The framework dynamically tracks
   Shannon Entropy across class predictions. High entropy lowers the
   contribution of magnitude gradients via the confidence gate, preventing the
   model from fitting arbitrary pip magnitudes on uncertain direction bars.
3. **High-Entropy Governor Resilience (v17.2)**: Financial time-series contain
   massive natural variance (turbulence). The `SmartTrainingGovernor` bypasses
   the standard Turbulence Shield specifically for Forex, doubling the Intense
   Cyclical Learning Rate (Jolt Protocol) intensity ($2.0\times$ multiplier over
   5-epoch windows) while extending absolute plateau patience to prevent
   false-positive retreats.
4. **Multi-Asset Pip Scale Normalization (`PAIR_PIP_SCALE`) (v17.4)**: Commodity
   assets (Gold, Oil) and equity indices (US500, USTEC, GER40) exhibit
   multi-thousand pip volatility swings that overpower standard currency majors.
   The framework standardizes all target and predicted magnitudes into
   Normalized Pip Units ($\text{NPU} = \text{Pips} / \text{PAIR\_PIP\_SCALE}$),
   applying a scale factor of $1.0\times$ for FX Majors, $5.0\times$ for
   Oil/Silver, $10.0\times$ for Gold, and $20.0\text{--}40.0\times$ for Indices.
   This eliminates magnitude head saturation and stabilizes validation losses.
5. **Governor Financial Hardening & Thermal Anchoring (v17.4)**: In
   high-entropy, low signal-to-noise financial regimes, standard temperature
   sharpening causes severe gradient instability. The `SmartTrainingGovernor`
   enforces a strict temperature floor ($\min T = 0.75$), constrains the Stress
   Protocol ($\le 2.0$), limits differential learning rate jolts to
   $\le 1.15\times$, and categorizes training as `CURRICULUM_FOLD` to prevent
   erroneous spatial ladder transitions.
6. **Timeframe Dropout Regularization (v17.6)**: Injects stochastic temporal
   masking ($p=0.15$) during training forward passes to prevent single-timeframe
   co-adaptation and high-frequency noise fitting across the multi-scale
   attention heads.
7. **Clean Training Execution & Checkpoint Isolation (v17.5)**: The CLI
   (`train.py`) and curriculum orchestrator (`train_forex_curriculum.py`)
   support `--clean` / `--fresh` flags to initiate runs from epoch 1 without
   phantom checkpoint resurrection. When active, Hub Sync bypasses
   `git lfs pull`, purges local residual checkpoints, resets
   `curriculum_state.json`, and wipes `metrics.csv`. All checkpoints (`_latest`,
   `_best`, `_progress`, and `_vault_`) are strictly saved to and loaded from
   isolated model directories (`LemGendaryModels/<model>/checkpoints/`).
8. **Vectorized Alignment Caching, Fractional Striding & Zero-Worker Windows
   Execution (v17.7)**: Resolves GPU data starvation (0% utilization) and
   Windows multiprocessing pagefile thrashing. The data pipeline precomputes
   cross-timeframe temporal alignment matrices in vector space ($O(1)$ integer
   index lookup replacing one $O(\log N)$ binary search per sample and
   timeframe). Physical batch sizes follow the Forex VRAM tiers of
   `training/hardware/probe.py` (256 from 20 GB, 128 from 12 GB, 64 from
   6 GB, 32 from 3.2 GB of total VRAM, so a 4GB GTX 1650 runs batch 32).
   Uniform chronological striding represents all 16 symbols proportionally at
   reduced fractions, and Windows multiprocessing is strictly gated to
   in-process execution (`num_workers=0`), eliminating child process memory
   duplication. The RAM, throughput and iteration savings are not yet
   measured; the figures of earlier revisions are removed. Checkpoint
   resumption enforces curriculum fraction overrides to prevent legacy $100\%$
   fraction resurrected states from diluting early-epoch convergence.

### 4.7 Consolidated SOTA Benchmarks

Not yet measured, for every pair and for the universe mean. The per-pair
figures of earlier revisions (EURUSD, GBPUSD, USDJPY and XAUUSD direction
accuracy 77.75% to 79.15%, win rate 66.60% to 69.40%, profit factor 2.04 to
2.26, Sharpe 2.29 to 2.62, drawdown 9.20% to 9.85%) and the universe mean
(49.69%) have no backing measurement and are removed. Per-pair results will be
listed once a valid run (Section 4.4.1) reports them.

### 4.8 Training Process Analysis

The Smart Governor keeps the sample fraction at 1.0 (registry
`initial_fraction: 1.0`, `fraction_increment: 0.0`) across the Walk-Forward
matrix while advancing through the Timeframe Confluence Ladder
($\text{H1}+\text{H4} \rightarrow \text{M15}+\text{H1}+\text{H4}+\text{D1}$).
The learning rate starts at $10^{-4}$ (registry `learning_rate`) and is cooled
by the governor (`cooling_factor: 0.85`); stochastic weight averaging starts
at 70% of progress (`swa_start_pct: 0.7`). Whether the weights converge is not
yet measured.

#### 4.8.1 Walk-Forward Curriculum Expansion

To robustly learn complex non-stationary regimes, the architecture is supervised
through a `train_forex_curriculum.py` orchestration loop executing across the
6-Fold Walk-Forward matrix (`active_folds: [1, 2, 3, 4, 5, 6]`):

1. **Stage 1 (Macro Confluence)**: Initial training on macro horizons
   ($\text{H1}, \text{H4}, \text{D1}$) across all 16 symbols to establish stable
   trend and regime representations.
2. **Stage 2 (Swing Confluence)**: Expanded to incorporate intermediate swing
   horizons ($\text{M15}, \text{H1}, \text{H4}, \text{D1}$).
3. **Stage 3 (Intraday Confluence)**: Expanded to incorporate high-frequency
   intraday momentum ($\text{M5}, \text{M15}, \text{H1}, \text{H4}, \text{D1}$).
4. **Stage 4 (Full Multi-Scale Universe)**: Complete multi-scale confluence
   training across all 6 timeframes
   ($\text{M1}, \text{M5}, \text{M15}, \text{H1}, \text{H4}, \text{D1}$).

The Patience-Based Early Stopping mechanism evaluates convergence over an
objective $K$-fold temporal validation matrix $\mathcal{M}_{\text{WF}}$:

$$
\mathcal{M}_{\text{WF}} = \sum_{k=1}^K \sum_{t \in \mathcal{V}_k}
\mathcal{L}_{\text{CE}}\left(f_\theta(\mathbf{X}_{t-W:t}), y_{t+1}\right)
$$

The dynamic fold advancement gate triggers if the validation loss fails to
improve for $P$ consecutive epochs:

$$
t_{\text{stop}} = \min \left\{ t \mid \min_{t' \in [t-P, t]}
\mathcal{L}_{\text{val}}(t') > \min_{\tau \le t-P}
\mathcal{L}_{\text{val}}(\tau) \right\}
$$

This progressive staging prevents gradient collapse when exposing the network to
highly decoupled esoteric currency dynamics, systematically cascading
checkpoints through the 6-Fold Walk-Forward matrix using dynamic rather than
fixed limits.

**Dynamic Orchestrator Target Scaling**: The orchestrator is designed to safely
interact with the `train.py` Resiliency Guardrail. If a fold dynamically extends
past its base epochs to force SOTA convergence, the curriculum orchestrator will
automatically read the actual model epoch from `metrics.csv` upon the next
fold's launch. It then dynamically scales the next fold's target (e.g.,
`current_epoch + epochs_per_fold`), ensuring no future folds are starved of
their intended training cycles due to previous resiliency extensions.

To optimize storage and training throughput, the 26.8M-row physical manifold
is packaged into a unified dataset:

- `LemGendizedForexUniverseLarge`

The `ForexDataset` utilizes dynamic timeframe filtering and multi-root
discovery. It scans local directory trees or attached archives and mounts the
complete 16-symbol universe with zero redundant downloads, scaling timeframe
rungs dynamically according to the curriculum stage.

**Configurable Curriculum Reductions & Timeframe Auto-Detection**
The `train_forex_curriculum.py` orchestrator supports explicit YAML-based
reduction of the curriculum matrix. By defining an `active_folds` block under
`forex_predictor.curriculum` in `unified_models_v2.yaml`, the orchestrator
filters the execution loop to only process the requested folds. Furthermore, the
`ForexDataset` dynamically computes the strict intersection of all available
timeframes across attached manifolds on disk, automatically dropping any missing
timeframes to prevent topology mismatches during training. When Folds are
reduced (e.g. from 6 to $N$), the dataset compiler automatically slides the
chronological window to the most recent $N+1$ folds, merging the earliest two
into a unified pre-training base fold while preserving the validation sequence.

**Walk-Forward Temporal Completeness (100% Data Fraction per Fold)**: Unlike
vision models that iterate through fractional resolution downsampling
(`15% -> 100%`), financial time-series models must preserve complete historical
continuity without downsampling or fractional stride gaps. The
`SmartTrainingGovernor` locks `sample_fraction = 1.0` across all Forex training
passes. The model trains on 100% of historical candles in each fold's expanding
chronological training window, advancing through the 6-Fold Walk-Forward matrix
(Fold 1: 2019–2020 $\rightarrow$ 2021 through Fold 6: 2019–2025
$\rightarrow$ 2026) while expanding across the Multi-Timeframe Confluence
Ladder.

#### 4.8.2 MetaTrader 5 (MT5) Auto-Acquisition Bridge

To eliminate the latency of packaging and distributing multi-gigabyte forex
tarballs across development environments, the dataset compilation pipeline
integrates directly with MetaTrader 5. When compiling financial time-series
manifolds, the compiler intelligence bypasses raw tarball downloads entirely. It
scans the local `data\forex` cache against the required phase configuration
(e.g., the Titan 4 Core `pairs_list`). If any currency pair shards are missing,
the compiler seamlessly bridges into the `mt5_pipeline`, instantiating a live
IPC connection to a local MetaTrader 5 terminal. It extracts, resamples, and
compiles the missing historical OHLCV data on-the-fly, bridging the gap between
quantitative finance platforms and AI training suites.

---

## 5. Challenges & Resilience Architecture

### 5.1 Lookahead Leakage Elimination (Strict Embargo Gaps)

Financial indicators that compute rolling windows across train/val boundaries
create subtle data leakage. The 14-day embargo gap physically purges overlapping
candles, guaranteeing that validation metrics reflect true out-of-sample
execution.

### 5.2 Anti-Hold Manifold Collapse (Entropy Regularization)

$$
\mathcal{H}(\mathbf{p}) = -\sum_{c=0}^2 p_c \ln(p_c + \epsilon)
$$

By maximizing entropy over uniform distributions while supervising directional
ground truth, the network avoids predicting zero-conviction trades during
consolidation periods.

### 5.3 Spread Friction & Dynamic Slippage Simulation

To simulate real broker execution friction, targets undergo spread stress:

$$
\tilde{y}_{\text{tp}} = \max(0, y_{\text{tp}} - \delta_{\text{spread}}), \quad
\tilde{y}_{\text{sl}} = y_{\text{sl}} + \delta_{\text{spread}}
$$

where $\delta_{\text{spread}}$ is the governor's stress value in pips (the
`Stress` column of `metrics.csv`, default 0) divided by the pair's
`PAIR_PIP_SCALE` (`data/forex_dataset.py`). The code has no fixed per-asset
spread value.

### 5.4 Risk-Adjusted Position Sizing via Fractional Kelly

Proposed, not implemented: the generated Expert Advisor sizes lots from
`RiskPct` (Section 6.3), not from a Kelly rule. A Fractional Kelly Criterion
($f^* = 0.25 \cdot K$) would use:

$$
K = \frac{p \cdot b - (1 - p)}{b}
$$

where $p = \text{Win Rate}$,
$b = \frac{\mathbb{E}[\text{TP}]}{\mathbb{E}[\text{SL}]}$. It needs a measured
win rate and payoff ratio, which do not exist yet (Section 4.4).

### 5.5 Sub-5ms Real-Time Inference Deployment

The $<5.0 \text{ ms}$ inference latency is a target. It is not yet measured:
the 1.42 ms average and 2.18 ms P95 of earlier revisions have no committed
benchmark behind them and are removed. A valid figure names the device, the
runtime (PyTorch or ONNX Runtime), the batch size, the number of runs, and the
mean and P95.

---

## 6. Deployment Strategy: MetaTrader 5 Expert Advisor Bridge

### 6.1 Stateless ONNX Model Export `[THEORETICAL]`

The trained model is exported to ONNX format with one static input matrix per
active timeframe $m$, $L_m$ bars (Section 2.4) by 14 features, plus the pair
index:

$$
\mathbf{X}_{m} \in \mathbb{R}^{1 \times L_m \times 14}, \quad \text{e.g.}
\quad \mathbf{X}_{15} \in \mathbb{R}^{1 \times 192 \times 14}, \quad
\mathbf{X}_{1440} \in \mathbb{R}^{1 \times 252 \times 14}
$$

### 6.2 Automated Real-Time Tick Ingestion

The generated MetaTrader 5 Expert Advisor (`LemGendaryForexEA.mq5`, Section
6.3) queries the ONNX model upon every bar close. If directional probability
$P(\text{BUY})$ or $P(\text{SELL})$ reaches `MinConfidence` (default 0.65),
orders are submitted with the predicted TP/SL boundaries.

### 6.3 Generated MQL5 Expert Advisor & MT5 Artefact (v16.9.185, v16.9.192)

The Training Suite renders the Expert Advisor from the registry
(`python -m export.mt5_signal --mode mql5_ea`, golden file
`LemGendaryForexEA.mq5`): `CTrade` orders, `OnnxCreate` with the single-file
model in `MQL5\Files`, one `[1, lookback, features]` float matrix per
timeframe plus the int64 pair index, softmax and the `MinConfidence` gate
(default 0.65), and a lot size from `RiskPct`, whose default is
`evaluation.risk_per_trade`. Its `BuildFeatures` is rendered from
`data/mt5_feature_spec.py`, the one specification of the 14 input columns,
the indicator windows and the 300 warm-up bars that the training shards and
the live signal also use.

MetaTrader 5 bundles ONNX Runtime 1.17, which reads IR versions up to 9, so
the MT5 graph (opset 18) is written as one file with embedded weights and
stamped IR 9 after a check for IR 10 features. The EA has not yet been
compiled in MetaEditor or run in the Strategy Tester (owner check).

---

## 7. SOTA Architectural Performance Matrix

- **ForexPredictor**: Task: FX & Gold Prediction; Dir Acc (%): not yet
  measured (target 58.5); Win Rate (%): not yet measured (target 56.0);
  Profit Factor: not yet measured (target 1.65); Sharpe: not yet measured
  (target 1.85); MaxDD (%): not yet measured (target 12.0); Quality Score: not
  yet measured

The figures of earlier revisions (Dir Acc 49.69% marked `[MEASURED]`, Quality
Score 105.87) are removed, as are the restoration and aesthetic rows (NAFNet
deblurring 32.85 dB, NAFNet denoising 38.40 dB, MPRNet deraining 33.12 dB,
NIMA SRCC 0.724), which had no backing measurement here. Each of those models
reports its own metrics in its own paper.

---

## 8. Conclusion

The **LemGendary ForexPredictor** combines multi-timeframe causal dilated
convolutions with cross-temporal attention fusion and 6-fold walk-forward
validation, and is built to avoid future lookahead bias. Whether it reaches
the registry targets for risk-adjusted returns is not yet measured: no valid
validation epoch exists (Section 4.4). The lightweight stateless architecture
targets sub-5ms inference for live MetaTrader 5 algorithmic execution; the
latency is not yet measured.

### Quantitative Financial Foundation Innovations (v17.1–v17.6)

- **Walk-Forward Curriculum Orchestration (v17.1)**: Automated 6-fold temporal
  expansion matrix with staged timeframe confluence progression featuring
  dynamic patience-based early stopping to sever unpromising folds and cascade
  checkpoints forward without fixed epoch starvation.
- **Forex High-Entropy Resilience (v17.2)**: `SmartTrainingGovernor` bypasses
  standard Turbulence Shields for financial manifolds, doubling the Intense
  Cyclical Learning Rate (Jolt Protocol) intensity ($2.0\times$ multiplier over
  5-epoch windows) while extending absolute plateau patience to prevent
  false-positive retreats.
- **Walk-Forward Fold Parity Verification (v17.3)**: Proactively verifies fold
  count integrity across active curriculum runs before execution, preventing
  mismatched Walk-Forward Cross-Validation splits when using reduced fold
  configurations.
- **Normalized Pip Scaling & Financial Governance Hardening (v17.4)**: Solves
  commodity and equity index pip scale divergence via `PAIR_PIP_SCALE` mapping
  (FX Majors 1.0, Commodities 5.0–10.0, Indices 20.0–40.0) standardizing
  regression targets to 0–100 NPUs, enforcing a 0.75 temperature floor, and
  gating differential LR jolts to $\le 1.15\times$.
- **Clean Training Execution & Checkpoint Isolation (v17.5)**: Clean execution
  CLI flags (`--clean` / `--fresh`) reset `curriculum_state.json`, wipe
  `metrics.csv`, and strictly isolate all checkpoints into
  `LemGendaryModels/<model>/checkpoints/`.
- **16-Symbol Forex Universe & Timeframe Dropout Regularizer (v17.6)**:
  Ingestion of `LemGendizedForexUniverseLarge` (26.8M rows across 2019–2026)
  with expanding-window 6-fold WFCV, broker symbol aliasing (`NAS100`
  $\leftrightarrow$ `USTEC`, `DE40` $\leftrightarrow$ `GER40`), and stochastic
  timeframe masking ($p=0.15$) to prevent high-frequency noise co-adaptation.

### Related Ecosystem Documentation

- [Dataset Compiler Suite](./PAPER_DATASET_COMPILER.md) (Manifold:
  `LemGendizedForexUniverse`)
- [Training Suite Architecture](./PAPER_TRAINING_SUITE.md) (Tri-Format ONNX / PT
  Checkpoint Lifecycle)
- [AI Studio GUI Manual](./MANUAL_AI_STUDIO_GUI.md) (Interactive Training
  Panel Controls)
- [Master Ecosystem Architecture](./ECOSYSTEM_ARCHITECTURE.md) (System
  Governance & Specifications)


### MT5 Strategy Tester `PERIOD_D1` Leading-Bar Padding

In MetaTrader 5 Strategy Tester backtests, `CopyRates(_Symbol, PERIOD_D1, 1,
552, rates)` can return fewer than 552 daily bars near the start of a test
window (~1 year of pre-loaded `D1` history). `BuildFeatures()` in
`training/export/mql5_features.py` now left-pads leading bars with `rates[0]`
when `0 < copied < count`, eliminating `error 4753` journal spam.
