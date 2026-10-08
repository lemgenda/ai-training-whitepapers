<!-- markdownlint-disable MD025 MD024 MD035 MD003 MD001 MD013 -->

# General AI Training Knowledge & Systems Engineering Reference

## Category 00 --- General AI Knowledge Reference Specification

**Document status:** Canonical general-knowledge reference\
**Scope:** Universal AI/ML systems engineering, training dynamics, architecture taxonomy, and dataset engineering independent of specific software implementations.\
**Primary purpose:** Provide an exhaustive, mathematically rigorous, and technically authoritative reference manual for deep learning training, dataset container architectures, model selection, loss formulation, optimization, evaluation, and production deployment decisions.

> **Boundary:** This specification describes foundational AI/ML scientific principles, algorithmic formalisms, and industry-standard engineering practices. It remains completely decoupled from proprietary software implementations, vendor-specific GUI wrappers, and localized workflow paths. Implementation-specific configurations and project runtime defaults belong exclusively in dedicated application manuals.

------------------------------------------------------------------------

## Table of Contents

1. [Knowledge Architecture](#1-knowledge-architecture)
2. [Core Concepts](#2-core-concepts)
   - [2.1 Dataset](#21-dataset)
   - [2.2 Dataset Split](#22-dataset-split)
   - [2.3 Sample Independence](#23-sample-independence)
   - [2.4 Data Leakage](#24-data-leakage)
3. [General Dataset Formats](#3-general-dataset-formats)
   - [3.1 Format Decision Framework](#31-format-decision-framework)
   - [3.2 CSV / TSV](#32-csv--tsv)
   - [3.3 JSON Lines / JSONL / NDJSON](#33-json-lines--jsonl--ndjson)
   - [3.4 Apache Parquet](#34-apache-parquet)
   - [3.5 Apache Arrow / Arrow IPC / Feather](#35-apache-arrow--arrow-ipc--feather)
   - [3.6 Zarr](#36-zarr)
   - [3.7 TFRecord](#37-tfrecord)
   - [3.8 WebDataset](#38-webdataset)
   - [3.9 HDF5](#39-hdf5)
   - [3.10 NetCDF](#310-netcdf)
   - [3.11 LMDB](#311-lmdb)
   - [3.12 MosaicML MDS / Streaming Formats](#312-mosaicml-mds--streaming-formats)
   - [3.13 Format Comparison](#313-format-comparison)
4. [Dataset Structure and Engineering](#4-dataset-structure-and-engineering)
   - [4.1 Canonical Dataset Layers](#41-canonical-dataset-layers)
   - [4.2 Dataset Manifest](#42-dataset-manifest)
   - [4.3 Dataset Invariants](#43-dataset-invariants)
5. [Model Weights, Checkpoints, Serialization and Runtime Artifacts](#5-model-weights-checkpoints-serialization-and-runtime-artifacts)
   - [5.1 Safetensors](#51-safetensors)
   - [5.2 PyTorch `.pt` / `.pth`](#52-pytorch-pt--pth)
   - [5.3 ONNX](#53-onnx)
   - [5.4 GGUF](#54-gguf)
   - [5.5 GGML](#55-ggml)
   - [5.6 TensorRT Engines](#56-tensorrt-engines)
   - [5.7 OpenVINO](#57-openvino)
   - [5.8 Core ML](#58-core-ml)
   - [5.9 TFLite / LiteRT Ecosystem](#59-tflite--litert-ecosystem)
   - [5.10 JAX / Orbax Checkpoints](#510-jax--orbax-checkpoints)
   - [5.11 Weight-Format Comparison](#511-weight-format-comparison)
6. [Deep Learning Architecture Knowledge](#6-deep-learning-architecture-knowledge)
7. [Training Theory](#7-training-theory)
8. [Optimizers](#8-optimizers)
9. [Learning Rate and Schedulers](#9-learning-rate-and-schedulers)
10. [Batch Size and Gradient Accumulation](#10-batch-size-and-gradient-accumulation)
11. [Regularization](#11-regularization)
12. [Normalization](#12-normalization)
13. [Mixed Precision](#13-mixed-precision)
14. [Distributed Training](#14-distributed-training)
15. [Parameter-Efficient Fine-Tuning](#15-parameter-efficient-fine-tuning)
16. [LLM Post-Training](#16-llm-post-training)
17. [Loss Functions](#17-loss-functions)
18. [Evaluation Metrics](#18-evaluation-metrics)
19. [Dataset Engineering](#19-dataset-engineering)
20. [Class Imbalance](#20-class-imbalance)
21. [Augmentation](#21-augmentation)
22. [Sampling and Curriculum](#22-sampling-and-curriculum)
23. [Sharding and Streaming](#23-sharding-and-streaming)
24. [Data Splitting Best Practices](#24-data-splitting-best-practices)
25. [Training Pathology](#25-training-pathology)
26. [Reproducibility](#26-reproducibility)
27. [Checkpointing](#27-checkpointing)
28. [Hyperparameter Search](#28-hyperparameter-search)
29. [Model Selection](#29-model-selection)
30. [Quantization](#30-quantization)
31. [Knowledge for an AI Training Helper](#31-knowledge-for-an-ai-training-helper)
32. [AI Helper Decision Rules](#32-ai-helper-decision-rules)
33. [Common AI Training Misconceptions](#33-common-ai-training-misconceptions)
34. [Comparison Knowledge the AI Helper Should Master](#34-comparison-knowledge-the-ai-helper-should-master)
35. [General Recommendations by Scenario](#35-general-recommendations-by-scenario)
36. [General AI Knowledge Safety and Reliability Rules](#36-general-ai-knowledge-safety-and-reliability-rules)
37. [Recommended Knowledge-Base Metadata](#37-recommended-knowledge-base-metadata)
38. [Final General AI Training Continuum](#38-final-general-ai-training-continuum)
39. [Summary](#39-summary)

- [Appendix A: Training-Corpus Coverage Checklist](#appendix-a-training-corpus-coverage-checklist)
- [Appendix B: Important Terminology Distinctions](#appendix-b-important-terminology-distinctions)
- [Appendix C: Required Behavior for Derived AI-Helper Training Examples](#appendix-c-required-behavior-for-derived-ai-helper-training-examples)
- [Appendix D: Source Authority Boundary](#appendix-d-source-authority-boundary)

------------------------------------------------------------------------

# 1. Knowledge Architecture

The AI training lifecycle can be represented as:

``` text
DATA
  |
  +--> acquisition
  +--> validation
  +--> cleaning / deduplication
  +--> labeling / annotation
  +--> splitting
  +--> transformation / augmentation
  +--> serialization / sharding
  |
  v
MODEL
  |
  +--> architecture
  +--> parameters / weights
  +--> tokenizer / preprocessing
  +--> objective / loss
  |
  v
TRAINING
  |
  +--> optimizer
  +--> learning-rate schedule
  +--> regularization
  +--> precision
  +--> batching
  +--> distributed execution
  |
  v
EVALUATION
  |
  +--> task metrics
  +--> robustness
  +--> calibration
  +--> OOD testing
  +--> human evaluation where applicable
  |
  v
ARTIFACT
  |
  +--> checkpoint
  +--> weights
  +--> exported graph
  +--> optimized / quantized runtime
  |
  v
DEPLOYMENT
```

A strong AI system is not produced by choosing an architecture in
isolation. Dataset quality, task definition, objective, optimization,
evaluation methodology, hardware, and deployment constraints interact.

------------------------------------------------------------------------

# 2. Core Concepts

## 2.1 Dataset

A dataset is a collection of samples and associated metadata intended
for a defined analytical or machine-learning purpose.

A sample may contain:

- input features;
- target labels;
- annotations;
- metadata;
- provenance;
- identifiers;
- quality flags;
- timestamps;
- masks;
- bounding boxes;
- captions;
- embeddings;
- auxiliary targets.

A dataset should have an explicit **task contract**:

``` yaml
task:
  modality: image | text | audio | video | tabular | multimodal | time_series
  objective: classification | detection | segmentation | restoration | generation | regression | ...
  input_schema: ...
  target_schema: ...
  preprocessing: ...
  split_policy: ...
  evaluation_protocol: ...
```

## 2.2 Dataset split

Common splits are:

- training;
- validation;
- test.

The validation set supports model selection and hyperparameter
decisions. The test set should remain isolated until final evaluation. A
third-party benchmark may serve as an external test set.

For grouped, temporal, medical, geospatial, or otherwise correlated
data, random row-level splitting may be invalid.

## 2.3 Sample independence

Many ML assumptions concern independent and identically distributed
observations, but real datasets often contain dependencies.

Examples:

- multiple images from one patient;
- frames from one video;
- multiple measurements from one machine;
- several crops from one source image;
- documents from the same author;
- repeated financial observations from the same instrument.

When correlated samples cross train/validation boundaries, evaluation
can become optimistically biased.

## 2.4 Data leakage

Data leakage occurs when information unavailable at inference time
influences training or model selection.

Major forms include:

1. **Target leakage** --- a feature directly or indirectly contains the
    target.
2. **Temporal leakage** --- future information is used to predict the
    past.
3. **Group leakage** --- related entities occur in multiple splits.
4. **Preprocessing leakage** --- statistics are computed using
    validation/test data.
5. **Benchmark contamination** --- evaluation examples or close
    derivatives appear in training.
6. **Augmentation leakage** --- augmented variants of the same source
    cross splits.

------------------------------------------------------------------------

# 3. General Dataset Formats

Dataset formats are not interchangeable. Format selection depends on
access pattern, modality, schema, scale, storage backend, framework,
concurrency, compression, and whether training requires random access or
sequential streaming.

## 3.1 Format decision framework

Use these questions:

``` text
1. Is the data tabular, tensor-like, document-oriented, or multimodal?
2. Is access predominantly random or sequential?
3. Is the dataset local or object-storage based?
4. Does training require streaming?
5. Do samples have variable structure?
6. Are strong schema and type guarantees required?
7. Is column projection important?
8. Is chunk-level parallelism important?
9. Does the framework have native support?
10. Is the format an interchange format, training format, or both?
```

------------------------------------------------------------------------

## 3.2 CSV / TSV

CSV and TSV are simple delimited text formats.

### Strengths

- human-readable;
- ubiquitous;
- easy to inspect;
- simple interchange;
- supported by nearly every data tool.

### Weaknesses

- textual parsing overhead;
- weak schema/type enforcement;
- escaping and quoting edge cases;
- larger storage footprint than typed binary formats;
- poor random access without an index;
- expensive repeated parsing during training.

### Best use

- small to medium tabular datasets;
- interchange;
- inspection;
- source ingestion.

### Poor use

Large-scale high-throughput GPU training where the same text must be
reparsed repeatedly.

------------------------------------------------------------------------

## 3.3 JSON Lines / JSONL / NDJSON

JSON Lines stores one JSON object per line.

Example:

``` json
{"id":1,"text":"hello","label":"positive"}
{"id":2,"text":"world","label":"negative"}
```

### Strengths

- one record per line;
- easy append and streaming;
- human-readable;
- flexible nested records;
- excellent for language-model instruction/SFT source data;
- easy to process incrementally.

### Weaknesses

- parsing cost;
- larger than binary formats;
- schema is convention rather than physical enforcement;
- random access requires indexing;
- malformed records must be handled explicitly.

### Best use

- instruction tuning;
- chat/SFT corpora;
- document metadata;
- preprocessing pipelines;
- streaming ingestion.

### Important distinction

JSONL is an excellent **source/interchange format** for LLM training
examples, but it is not automatically the optimal final representation
for very large high-throughput training.

------------------------------------------------------------------------

## 3.4 Apache Parquet

Parquet is a column-oriented binary storage format.

A Parquet file contains:

``` text
File
 |
 +-- Row Groups
      |
      +-- Column Chunks
           |
           +-- Pages
```

### Important properties

- typed schema;
- columnar storage;
- compression;
- dictionary encoding;
- statistics;
- predicate pushdown;
- projection pushdown;
- efficient analytical scans.

### Strengths

- excellent tabular analytics;
- strong compression;
- efficient column selection;
- rich ecosystem;
- excellent integration with Apache Arrow and query engines.

### Weaknesses

- not inherently a tensor-training format;
- row-oriented random sample access can be less natural than key-value
    or sharded sample stores;
- decoding overhead may matter for extremely latency-sensitive
    training;
- many small files can become an operational problem.

### Best use

- tabular datasets;
- metadata;
- labels and annotations;
- embeddings;
- analytical preprocessing;
- feature stores;
- large structured datasets.

------------------------------------------------------------------------

## 3.5 Apache Arrow / Arrow IPC / Feather

Apache Arrow defines a language-independent in-memory columnar
representation and interoperability ecosystem.

### Strengths

- efficient columnar memory layout;
- zero-copy interoperability in appropriate situations;
- excellent Python/C++/Rust ecosystem;
- vectorized processing;
- efficient interchange between analytical systems.

### Weaknesses

- Arrow is primarily a memory/interchange model rather than a
    universal training-dataset format;
- large analytical tables may still require an appropriate on-disk
    layout;
- tensor-heavy workloads may be better represented by chunked array
    formats.

### Best use

- preprocessing;
- analytical pipelines;
- interchange;
- tabular data;
- integration between languages and systems.

------------------------------------------------------------------------

## 3.6 Zarr

Zarr stores N-dimensional arrays in independently addressable chunks.

Conceptually:

``` text
Array
 |
 +-- Chunk (0,0,0)
 +-- Chunk (0,0,1)
 +-- Chunk (0,1,0)
 +-- ...
```

### Strengths

- N-dimensional arrays;
- chunk-level access;
- cloud/object-storage friendly designs;
- independent chunk compression;
- parallel reads/writes;
- excellent for scientific and imaging workloads.

### Weaknesses

- poor chunk design can cause severe I/O amplification;
- many small objects can stress object stores;
- metadata and storage layout require engineering;
- not automatically optimal for every deep-learning sample format.

### Chunk design principle

Choose chunks according to the expected access pattern.

If training usually reads:

``` text
sample -> complete image
```

then chunking individual samples can be appropriate.

If analysis usually reads:

``` text
all time points -> one spatial location
```

a different chunk orientation is preferable.

------------------------------------------------------------------------

## 3.7 TFRecord

TFRecord is a sequential binary record format strongly associated with
TensorFlow.

A record contains length information, integrity fields, and serialized
payload data.

### Strengths

- efficient sequential streaming;
- mature TensorFlow integration;
- good distributed ingestion;
- suitable for large training pipelines.

### Weaknesses

- less convenient outside TensorFlow ecosystems;
- sequential access is natural;
- random access requires auxiliary indexing;
- serialized feature schemas must be managed.

### Best use

- TensorFlow pipelines;
- TPU-oriented input pipelines;
- sequential large-scale training.

------------------------------------------------------------------------

## 3.8 WebDataset

WebDataset commonly represents samples inside TAR shards.

Example:

``` text
000001.jpg
000001.json
000001.txt

000002.jpg
000002.json
000002.txt
```

Files sharing a sample key form one logical sample.

### Strengths

- sequential I/O;
- simple sharding;
- object-storage friendly;
- multimodal samples;
- distributed training;
- easy shard-level partitioning;
- efficient streaming.

### Weaknesses

- not naturally random-access oriented;
- shard management matters;
- sample-to-shard assignment affects distributed efficiency;
- TAR itself does not provide rich typed schema semantics.

### Best use

- computer vision;
- multimodal training;
- image/text pairs;
- video;
- large-scale streaming training.

------------------------------------------------------------------------

## 3.9 HDF5

HDF5 provides hierarchical groups and multidimensional datasets inside a
single container.

``` text
/
+-- images
+-- labels
+-- metadata
+-- calibration
```

### Strengths

- scientific computing;
- multidimensional arrays;
- chunking;
- compression;
- rich metadata;
- mature ecosystem.

### Weaknesses

- multiprocessing/concurrency requires care;
- single-file access can create operational bottlenecks;
- file locking and driver behavior depend on environment;
- object-storage workflows can be less natural than chunk/object
    formats.

### Best use

- scientific datasets;
- microscopy;
- physics;
- dense multidimensional arrays;
- legacy scientific pipelines.

------------------------------------------------------------------------

## 3.10 NetCDF

NetCDF is designed for scientific multidimensional data, especially
geospatial and climate data.

Typical dimensions:

``` text
time
latitude
longitude
level
```

### Strengths

- scientific metadata;
- coordinate systems;
- gridded environmental data;
- integration with xarray and scientific Python.

### Weaknesses

- specialized rather than general-purpose ML storage;
- access pattern and chunking must be designed carefully;
- may require transformation before high-throughput model training.

### Best use

- climate;
- weather;
- oceanography;
- geospatial scientific datasets.

------------------------------------------------------------------------

## 3.11 LMDB

LMDB is an embedded transactional key-value database using memory
mapping.

### Strengths

- fast key-based lookup;
- mature transactional semantics;
- efficient local random access;
- useful for datasets with sample IDs as keys.

### Weaknesses

- storage is less transparent than loose files;
- environment configuration matters;
- object-store-native workflows are not its primary strength.

### Best use

- local key-value datasets;
- image patches;
- embeddings;
- random-access sample stores.

------------------------------------------------------------------------

## 3.12 MosaicML MDS / streaming formats

Streaming dataset systems commonly divide datasets into binary shards
plus metadata/index information.

Typical goals:

- deterministic shuffling;
- streaming;
- local caching;
- worker resumption;
- distributed ingestion.

They can be excellent when the training framework and infrastructure are
designed around streaming.

------------------------------------------------------------------------

## 3.13 Format comparison

  -----------------------------------------------------------------------------------------------------
  Format       Best access        Schema                Streaming   Random      Best domain
                                                                    access
  ------------ ------------------ --------------------- ----------- ----------- -----------------------
  CSV/TSV      Row scan           Weak                  Yes         Poor        Simple tabular

  JSONL        Record stream      Flexible              Excellent   Poor        LLM/SFT/source data
                                                                    without
                                                                    index

  Parquet      Column/row-group   Strong                Good        Moderate    Tabular/analytics

  Arrow IPC    Columnar           Strong                Good        Good        Interchange/analytics

  Zarr         Chunk              Strong                Good        Excellent   N-D arrays
                                                                    by chunk

  TFRecord     Sequential         Serialized features   Excellent   Poor        TensorFlow
                                                                    without
                                                                    index

  WebDataset   Shard/sample       Convention-based      Excellent   Poor        Vision/multimodal
               stream

  HDF5         Dataset/chunk      Strong                Possible    Good        Scientific arrays

  NetCDF       Dimension/chunk    Strong                Possible    Good        Geoscience

LMDB         Key                Application-defined   Good        Excellent   Local random access
  -----------------------------------------------------------------------------------------------------

### Important rule

**There is no universally best dataset format.**

The correct choice follows the training access pattern.

------------------------------------------------------------------------

# 4. Dataset Structure and Engineering

## 4.1 Canonical dataset layers

A robust pipeline separates:

``` text
RAW
 |
 +-- immutable source data
 |
 v
NORMALIZED
 |
 +-- decoded/validated representation
 |
 v
CURATED
 |
 +-- deduplicated
 +-- labeled
 +-- filtered
 |
 v
TRAINING
 |
 +-- split
 +-- transformed
 +-- serialized
 +-- sharded
 |
 v
DEPLOYMENT / ARCHIVE
```

## 4.2 Dataset manifest

A production dataset should have a manifest containing at least:

``` yaml
dataset_id:
dataset_version:
task:
modality:
sample_count:
schema:
source:
provenance:
license:
split_policy:
train_count:
validation_count:
test_count:
format:
shard_count:
compression:
checksum:
preprocessing:
label_schema:
quality_checks:
```

## 4.3 Dataset invariants

Before training, validate:

- schema;
- missing values;
- corrupted samples;
- duplicate IDs;
- duplicate content;
- label validity;
- class distribution;
- split isolation;
- dimensions;
- channel ordering;
- dtype;
- value ranges;
- normalization;
- color space where relevant;
- annotation bounds;
- timestamp ordering where relevant;
- license/provenance;
- checksum/integrity.

------------------------------------------------------------------------

# 5. Model Weights, Checkpoints, Serialization and Runtime Artifacts

A critical distinction:

``` text
TRAINING CHECKPOINT
       |
       +-- model parameters
       +-- optimizer state
       +-- scheduler state
       +-- scaler state
       +-- epoch/step
       +-- RNG state
       +-- configuration
       |
       v
MODEL WEIGHTS
       |
       v
EXPORTED MODEL
       |
       +-- ONNX
       +-- TensorFlow SavedModel
       +-- TorchScript where applicable
       +-- Core ML
       +-- TensorRT engine
       +-- other runtime artifacts
```

A deployment artifact is not necessarily a training checkpoint.

------------------------------------------------------------------------

## 5.1 Safetensors

Safetensors is a tensor serialization format designed around a simple
header plus raw tensor storage.

### Strengths

- avoids Python pickle execution semantics;
- explicit tensor metadata;
- efficient loading;
- memory mapping can be used by compatible implementations;
- strong ecosystem support in modern model repositories.

### Limitations

- stores tensors, not arbitrary Python training state;
- optimizer state must be stored separately or as additional tensors;
- a Safetensors file does not by itself describe the entire executable
    model architecture.

### Best use

- model weights;
- safe interchange;
- Hugging Face ecosystem;
- inference and fine-tuning checkpoints.

------------------------------------------------------------------------

## 5.2 PyTorch `.pt` / `.pth`

PyTorch commonly uses `torch.save` / `torch.load` for checkpoints.

Depending on how the file was produced, it can contain:

- a state dictionary;
- optimizer state;
- scheduler state;
- arbitrary Python objects;
- complete serialized objects.

### Security rule

Do not blindly deserialize untrusted PyTorch pickle-based artifacts.

Prefer safer state-dict workflows and formats such as Safetensors where
supported.

### Best use

- native PyTorch training;
- research checkpoints;
- complete training-state snapshots when trust is established.

------------------------------------------------------------------------

## 5.3 ONNX

ONNX is an open model interchange representation.

It describes:

- computational graphs;
- operators;
- tensors;
- shapes;
- metadata.

An ONNX model is intended to be executed by an ONNX-compatible runtime
rather than directly being a PyTorch training checkpoint.

### Strengths

- cross-framework interchange;
- broad inference-runtime ecosystem;
- graph-level optimization;
- CPU/GPU/accelerator deployment.

### Limitations

- operator compatibility matters;
- dynamic shapes can complicate optimization;
- training support is not equivalent to native framework training;
- export can expose unsupported or numerically different operations.

------------------------------------------------------------------------

## 5.4 GGUF

GGUF is a model-file format strongly associated with llama.cpp and
related LLM inference ecosystems.

It supports:

- tensor storage;
- metadata;
- quantized tensors;
- memory-mapped inference;
- CPU/GPU-oriented LLM execution.

### Best use

- local LLM inference;
- quantized transformer deployment;
- llama.cpp-compatible ecosystems.

### Important limitation

GGUF should not be treated as a universal model format for arbitrary
vision or scientific models.

------------------------------------------------------------------------

## 5.5 GGML

GGML is an older ecosystem and tensor/model representation associated
with early llama.cpp implementations.

GGUF largely replaced it for modern llama.cpp model packaging.

------------------------------------------------------------------------

## 5.6 TensorRT engines

TensorRT builds optimized inference engines for NVIDIA hardware.

Optimizations can include:

- kernel selection;
- layer fusion;
- precision conversion;
- memory planning;
- hardware-specific execution.

### Critical portability rule

A serialized TensorRT engine may depend on:

- GPU architecture;
- TensorRT version;
- CUDA/runtime compatibility;
- build settings.

Therefore it is not equivalent to a portable model-weight file.

------------------------------------------------------------------------

## 5.7 OpenVINO

OpenVINO provides an intermediate representation and optimized runtime
ecosystem primarily associated with Intel hardware.

It supports optimized inference on:

- CPUs;
- integrated GPUs;
- discrete GPUs;
- supported accelerators.

------------------------------------------------------------------------

## 5.8 Core ML

Core ML is Apple's model deployment ecosystem.

It targets Apple devices and can integrate with:

- CPU;
- GPU;
- Neural Engine where supported.

Model conversion and supported operations depend on the specific model
and Core ML version.

------------------------------------------------------------------------

## 5.9 TFLite / LiteRT ecosystem

TensorFlow Lite, now evolving toward LiteRT terminology in Google's
ecosystem, targets efficient deployment on constrained and mobile
hardware.

Typical goals include:

- low memory;
- low latency;
- mobile/edge inference;
- quantization.

------------------------------------------------------------------------

## 5.10 JAX / Orbax checkpoints

JAX ecosystems often separate model state from executable architecture
and use checkpoint systems such as Orbax.

Checkpointing can preserve:

- arrays;
- optimizer state;
- training state;
- metadata.

This is conceptually closer to a training-state system than a universal
deployment format.

------------------------------------------------------------------------

## 5.11 Weight-format comparison

  --------------------------------------------------------------------------------------------------------
  Format              Training    Inference          Quantization          Portability Primary ecosystem
                         state
  --------------- ------------ ------------ --------------------- -------------------- -------------------
  Safetensors          Limited          Yes                   Yes                 High PyTorch/HF
                  unless state
                       encoded

  PyTorch            Excellent          Yes   Framework-dependent          Medium/High PyTorch
  checkpoint

  ONNX            Not a normal    Excellent                   Yes                 High Cross-runtime
                      training
                    checkpoint

  GGUF              No general    Excellent             Excellent          High within llama.cpp
                      training          for                                  ecosystem
                         state    supported
                                       LLMs

  TensorRT engine           No    Excellent             Excellent   Hardware-dependent NVIDIA

  OpenVINO IR       No general    Excellent                   Yes       Intel-oriented OpenVINO
                      training
                         state

  Core ML           No general    Excellent                   Yes       Apple-oriented Apple
                      training
                         state

TFLite/LiteRT     No general    Excellent                   Yes        Edge-oriented TensorFlow/Google
                      training
                         state
  --------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 6. Deep Learning Architecture Knowledge

Architecture determines how information is represented and transformed.
There is no universally best architecture.

Selection should consider:

``` text
task
modality
input resolution
context length
latency
memory
dataset size
inductive bias
deployment hardware
training budget
```

------------------------------------------------------------------------

## 6.1 Multilayer Perceptron / MLP

An MLP applies learned affine transformations and nonlinearities:

``` text
x -> Linear -> Activation -> Linear -> ...
```

### Strengths

- simple;
- strong baseline for tabular data;
- inexpensive;
- useful inside larger architectures.

### Weaknesses

- poor spatial inductive bias;
- parameter-heavy for high-dimensional images;
- limited sequence structure without additional mechanisms.

------------------------------------------------------------------------

## 6.2 CNN

Convolutional neural networks use local receptive fields and shared
kernels.

A 2D convolution can be expressed as:

``` text
Y[i,j] = sum_{u,v,c} W[u,v,c] X[i+u,j+v,c]
```

### Strengths

- locality;
- translation-related inductive bias;
- efficient spatial feature extraction;
- excellent for vision and restoration.

### Weaknesses

- receptive field grows through depth or architectural mechanisms;
- long-range dependencies can require additional structures.

------------------------------------------------------------------------

## 6.3 ResNet

ResNet introduces residual connections:

``` text
y = F(x) + x
```

Residual pathways improve optimization of deep networks and became
foundational to modern vision architectures.

------------------------------------------------------------------------

## 6.4 EfficientNet

EfficientNet uses compound scaling to jointly scale:

- depth;
- width;
- input resolution.

The key idea is that scaling only one dimension is often inefficient.

------------------------------------------------------------------------

## 6.5 ConvNeXt

ConvNeXt modernizes convolutional networks using design choices inspired
by transformer-era architectures while retaining convolutional inductive
bias.

Useful when:

- spatial locality is valuable;
- convolutional efficiency is desirable;
- transformer-style design patterns are attractive without full
    attention everywhere.

------------------------------------------------------------------------

## 6.6 Vision Transformer (ViT)

ViT divides an image into patches, embeds the patches, and processes
them with transformer blocks.

Typical pipeline:

``` text
image
 -> patches
 -> linear embedding
 -> positional information
 -> transformer encoder
 -> task head
```

### Strengths

- global interactions;
- scalable architecture;
- strong transfer learning;
- unified transformer ecosystem.

### Weaknesses

- computational cost;
- data requirements;
- attention memory scaling;
- less local inductive bias than CNNs unless introduced
    architecturally.

------------------------------------------------------------------------

## 6.7 Swin Transformer

Swin uses windowed self-attention and shifted windows.

This reduces the cost of full global attention while maintaining
hierarchical spatial representations.

Useful for:

- detection;
- segmentation;
- dense vision tasks;
- high-resolution imagery.

------------------------------------------------------------------------

## 6.8 Transformer

The transformer is based primarily on attention and feed-forward blocks.

Scaled dot-product attention:

``` text
Attention(Q,K,V) =
softmax(Q K^T / sqrt(d_k)) V
```

### Core strengths

- flexible sequence modeling;
- global token interactions;
- strong scaling behavior;
- multimodal adaptability.

### Core costs

Naive full attention has approximately quadratic complexity in sequence
length:

``` text
O(n² d)
```

where `n` is sequence length and `d` is feature dimension.

Modern systems reduce practical cost using:

- FlashAttention;
- grouped-query attention;
- multi-query attention;
- sparse attention;
- sliding windows;
- local/global hybrids;
- linear/state-space alternatives.

------------------------------------------------------------------------

## 6.9 U-Net

U-Net uses an encoder-decoder structure with skip connections.

``` text
Input
  |
Encoder
  |
Bottleneck
  |
Decoder
  |
Output
```

Skip connections transfer high-resolution information from encoder
layers to decoder layers.

Excellent for:

- segmentation;
- image restoration;
- denoising;
- diffusion-model components.

------------------------------------------------------------------------

## 6.10 GAN

A Generative Adversarial Network contains:

``` text
Generator
     |
     v
Synthetic sample
     |
     v
Discriminator <--- real sample
```

The generator attempts to produce realistic samples while the
discriminator distinguishes real and generated data.

### Strengths

- sharp generated outputs;
- adversarial learning;
- image synthesis and translation.

### Weaknesses

- training instability;
- mode collapse;
- sensitive objective dynamics;
- evaluation complexity.

------------------------------------------------------------------------

## 6.11 VAE

A Variational Autoencoder learns a probabilistic latent representation.

The objective typically contains:

``` text
reconstruction loss + KL divergence
```

The KL term regularizes the latent distribution toward a prior.

Useful for:

- representation learning;
- latent-variable modeling;
- generative systems;
- compression.

------------------------------------------------------------------------

## 6.12 Diffusion models

Diffusion systems learn to reverse a progressive corruption process.

A simplified forward process adds noise:

``` text
x_0 -> x_1 -> ... -> x_T
```

The learned reverse process reconstructs or generates samples.

Common components include:

- noise scheduler;
- denoising network;
- text/image conditioning;
- latent representation;
- classifier-free guidance;
- sampling solver.

Diffusion is not limited to images; related formulations exist for
audio, video, 3D, molecules, and other modalities.

------------------------------------------------------------------------

## 6.13 Mixture of Experts

MoE architectures contain multiple expert subnetworks and a router.

``` text
tokens
   |
router
 / | \
E1 E2 E3 ... EN
 \ | /
selected expert outputs
   |
combine
```

Only a subset of experts may process each token.

### Advantages

- high parameter capacity;
- lower active compute than a dense model of equivalent total
    parameter count;
- specialization.

### Problems

- routing imbalance;
- communication overhead;
- expert collapse;
- capacity overflow;
- distributed-training complexity.

------------------------------------------------------------------------

## 6.14 State Space Models / Mamba-style architectures

State-space models represent sequences through recurrent state dynamics.

A continuous-time formulation can be expressed as:

``` text
h'(t) = A h(t) + B x(t)
y(t)  = C h(t)
```

Modern selective state-space architectures make parts of the state
dynamics input-dependent and use hardware-aware scan algorithms.

### Strengths

- efficient long-sequence processing;
- alternatives to quadratic attention;
- strong sequence modeling.

### Trade-offs

- different inductive bias from attention;
- ecosystem/tooling differences;
- architecture-specific optimization requirements.

------------------------------------------------------------------------

## 6.15 Architecture selection matrix

  -----------------------------------------------------------------------
  Task                                Strong candidates
  ----------------------------------- -----------------------------------
  Tabular classification              MLP, tree models, transformer
                                      variants

  Image classification                CNN, ConvNeXt, ViT

  Object detection                    CNN detectors, DETR-family,
                                      Swin-based systems

  Segmentation                        U-Net, U-Net variants, transformer
                                      hybrids

  Restoration                         CNN/U-Net, NAFNet-like,
                                      transformer/restoration hybrids

  Language modeling                   Transformer, MoE, SSM/hybrid

  Image generation                    Diffusion, GAN, flow-based systems

  Representation learning             CNN, ViT, autoencoder, contrastive
                                      architectures

  Long sequences                      Transformer variants, SSMs, hybrid
                                      models

Multimodal                          Transformer-based fusion,
                                      modality-specific encoders + shared
                                      heads
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 7. Training Theory

Training is numerical optimization over a parameterized function.

Given parameters `theta`, training minimizes an objective:

``` text
theta* = argmin_theta E[L(f_theta(x), y)]
```

In practice the expectation is approximated using minibatches.

------------------------------------------------------------------------

## 7.1 Forward pass

The model computes:

``` text
prediction = f_theta(x)
```

------------------------------------------------------------------------

## 7.2 Loss

The loss quantifies disagreement between prediction and target.

Examples:

- cross entropy;
- binary cross entropy;
- mean squared error;
- L1;
- Huber;
- focal loss;
- contrastive loss;
- triplet loss;
- perceptual loss;
- ranking losses.

The loss being optimized is not necessarily the metric users ultimately
care about.

------------------------------------------------------------------------

## 7.3 Backpropagation

Backpropagation applies the chain rule to compute gradients:

``` text
dL/dtheta
```

Automatic differentiation systems construct or track computational
graphs and propagate derivatives backward.

------------------------------------------------------------------------

## 7.4 Gradient descent

Basic gradient descent:

``` text
theta_(t+1) = theta_t - eta * grad_theta L
```

where `eta` is the learning rate.

------------------------------------------------------------------------

# 8. Optimizers

## 8.1 SGD

``` text
theta <- theta - eta * g
```

### Strengths

- simple;
- predictable;
- strong generalization behavior in many vision settings.

### Weaknesses

- learning-rate tuning;
- potentially slower convergence.

------------------------------------------------------------------------

## 8.2 Momentum

Momentum maintains a running update direction.

``` text
v_t = beta * v_(t-1) + g_t
theta_t = theta_(t-1) - eta * v_t
```

It reduces oscillation and can accelerate movement along persistent
gradient directions.

------------------------------------------------------------------------

## 8.3 Adam

Adam maintains first and second moments of gradients.

``` text
m_t = beta1*m_(t-1) + (1-beta1)*g_t
v_t = beta2*v_(t-1) + (1-beta2)*g_t²
```

Bias correction is applied before updating parameters.

------------------------------------------------------------------------

## 8.4 AdamW

AdamW decouples weight decay from the adaptive gradient update.

This is generally preferred over treating weight decay as an ordinary
gradient term when using Adam-style optimizers.

------------------------------------------------------------------------

## 8.5 RMSProp

RMSProp adapts updates using an exponential moving average of squared
gradients.

It can be useful for some recurrent and nonstationary optimization
problems.

------------------------------------------------------------------------

## 8.6 LAMB / LARS

Layer-wise adaptive methods can be useful for very large batch training.

They scale updates using layer-wise norms and can help stabilize
large-batch optimization.

------------------------------------------------------------------------

## 8.7 Lion

Lion is a sign-based optimizer with low optimizer-state memory relative
to Adam-style methods.

Its practical suitability depends on model family and training regime;
it should not be assumed universally superior.

------------------------------------------------------------------------

## 8.8 Sophia

Sophia uses curvature information to adapt updates more efficiently than
purely first-order methods in some language-model training settings.

It is more specialized than AdamW.

------------------------------------------------------------------------

## 8.9 Muon

Muon is an optimizer family designed around structured updates to weight
matrices and has attracted interest in modern neural-network training.

It should be treated as an alternative requiring architecture- and
implementation-specific validation rather than a drop-in universal
replacement.

------------------------------------------------------------------------

# 9. Learning Rate and Schedulers

Learning rate is one of the most influential hyperparameters.

A useful conceptual decomposition is:

``` text
initial learning rate
+ warmup
+ stable phase
+ decay
```

## 9.1 Warmup

Warmup gradually increases the learning rate at the beginning of
training.

Useful when:

- optimization is unstable at initialization;
- batch sizes are large;
- transformer training is sensitive to early updates;
- mixed precision requires stabilization.

## 9.2 Cosine decay

A cosine schedule smoothly decreases the learning rate.

Conceptually:

``` text
eta(t) = eta_min + 0.5*(eta_max-eta_min)*(1 + cos(pi*t/T))
```

## 9.3 OneCycle

OneCycle increases and then decreases the learning rate, often with an
inverse momentum relationship.

It can be effective for some supervised training workloads.

## 9.4 Exponential decay

``` text
eta_t = eta_0 * gamma^t
```

Simple but can decay too aggressively if not tuned.

## 9.5 Warmup-Stable-Decay

A three-stage schedule:

``` text
warmup -> stable high/medium LR -> decay
```

is useful when a long stable optimization phase is desirable.

------------------------------------------------------------------------

# 10. Batch Size and Gradient Accumulation

## 10.1 Batch size

A batch is the set of samples used for one gradient estimate.

Larger batches:

- improve hardware utilization;
- reduce gradient-estimator variance;
- increase memory use;
- may require learning-rate changes;
- can alter optimization/generalization behavior.

## 10.2 Micro-batch

The micro-batch is the portion processed in one forward/backward pass.

## 10.3 Gradient accumulation

If gradients are accumulated for `k` micro-batches before an optimizer
step:

``` text
effective batch ≈ micro_batch * accumulation_steps * data_parallel_world_size
```

provided the implementation scales loss and gradients consistently.

Gradient accumulation reduces activation-memory pressure but does not
make each forward/backward pass cheaper.

------------------------------------------------------------------------

# 11. Regularization

Regularization reduces overfitting or constrains model behavior.

## 11.1 Weight decay

Penalizes large parameter values or, under AdamW-style decoupling,
directly shrinks parameters.

## 11.2 Dropout

Randomly removes activation elements during training.

## 11.3 DropPath / stochastic depth

Randomly skips complete residual paths or blocks during training.

## 11.4 Label smoothing

Replaces hard one-hot targets with softened distributions.

Useful for reducing overconfidence in some classification tasks.

## 11.5 Mixup

Creates interpolated training examples:

``` text
x' = lambda*x_i + (1-lambda)*x_j
y' = lambda*y_i + (1-lambda)*y_j
```

## 11.6 CutMix

Combines spatial regions from two images and adjusts labels according to
region proportions.

------------------------------------------------------------------------

# 12. Normalization

## BatchNorm

Normalizes using batch statistics.

Strengths:

- effective in many CNNs;
- well-established.

Limitations:

- sensitive to small batch sizes;
- distributed synchronization can add overhead.

## LayerNorm

Normalizes features within each sample.

Common in transformers.

## RMSNorm

Normalizes based on root-mean-square magnitude without explicit mean
subtraction.

Common in modern transformer architectures.

## GroupNorm

Normalizes channels in groups and is often useful when batch sizes are
small.

------------------------------------------------------------------------

# 13. Mixed Precision

Common numeric formats include:

``` text
FP32
FP16
BF16
FP8
INT8
INT4
```

Training commonly uses higher precision for selected operations and
lower precision for throughput.

## FP16

Advantages:

- low memory;
- high accelerator throughput.

Risk:

- narrower exponent range can cause underflow/overflow.

## BF16

Advantages:

- exponent range similar to FP32;
- generally easier numerical stability than FP16.

Cost:

- lower mantissa precision than FP32.

## FP8

FP8 formats can substantially improve throughput and memory efficiency
on compatible hardware, but training requires careful scaling and
hardware/software support.

## Loss scaling

Dynamic loss scaling can protect FP16 gradients from underflow.

------------------------------------------------------------------------

# 14. Distributed Training

## 14.1 Data Parallelism

Each worker receives different samples and maintains model replicas.

Gradients are synchronized.

## 14.2 DDP

DistributedDataParallel is a common PyTorch implementation.

The effective batch size generally scales with worker count.

## 14.3 FSDP

Fully Sharded Data Parallel shards parameters, gradients, and optimizer
state across workers.

Primary benefit:

``` text
lower per-GPU memory footprint
```

at the cost of communication and implementation complexity.

## 14.4 ZeRO

ZeRO reduces redundant optimizer/gradient/parameter memory.

Conceptually:

``` text
ZeRO-1 -> shard optimizer states
ZeRO-2 -> shard optimizer + gradients
ZeRO-3 -> shard optimizer + gradients + parameters
```

## 14.5 Tensor Parallelism

Splits individual layers/tensors across devices.

Useful for models too large for one device.

## 14.6 Pipeline Parallelism

Splits model layers into stages across devices.

Micro-batches flow through stages to improve device utilization.

## 14.7 3D parallelism

Large models can combine:

``` text
Data Parallelism
+
Tensor Parallelism
+
Pipeline Parallelism
```

The correct strategy depends on:

- model size;
- batch size;
- network bandwidth;
- latency;
- accelerator memory;
- communication topology.

------------------------------------------------------------------------

# 15. Parameter-Efficient Fine-Tuning

## 15.1 LoRA

Low-Rank Adaptation freezes the base weights and trains low-rank update
matrices.

Conceptually:

``` text
W' = W + B A
```

where `A` and `B` have much lower rank than `W`.

Advantages:

- fewer trainable parameters;
- lower optimizer memory;
- smaller adapters;
- efficient specialization.

## 15.2 QLoRA

QLoRA combines quantized base-model weights with LoRA adapters.

The base model is kept in a low-bit representation while adapters are
trained.

Important distinction:

**QLoRA is a fine-tuning strategy, not merely a file format.**

------------------------------------------------------------------------

# 16. LLM Post-Training

## Supervised Fine-Tuning (SFT)

The model learns from prompt/response or instruction/response examples.

Typical data:

``` json
{"messages":[
  {"role":"user","content":"..."},
  {"role":"assistant","content":"..."}
]}
```

High-quality SFT data should emphasize:

- factual correctness;
- useful explanations;
- consistent terminology;
- refusal/uncertainty behavior;
- task diversity;
- difficult edge cases.

## Preference optimization

Methods such as DPO learn from preferred versus rejected responses.

The purpose is to optimize behavior relative to preference data without
requiring the same reinforcement-learning pipeline as PPO.

## PPO / RLHF

PPO-based RLHF uses reward modeling and reinforcement learning.

It is powerful but substantially more complex than SFT and preference
optimization.

------------------------------------------------------------------------

# 17. Loss Functions

## Classification

- Cross Entropy;
- Binary Cross Entropy;
- Focal Loss;
- Label-smoothed Cross Entropy.

## Regression

- MSE;
- MAE;
- Huber;
- Log-Cosh.

## Vision restoration

- L1;
- L2;
- Charbonnier;
- SSIM-based losses;
- perceptual losses;
- frequency-domain losses;
- adversarial losses.

## Metric learning

- contrastive loss;
- triplet loss;
- InfoNCE.

## Ranking

- pairwise hinge;
- RankNet;
- ListNet;
- differentiable ranking objectives.

### Important principle

A training loss is an optimization objective, not necessarily the final
evaluation metric.

------------------------------------------------------------------------

# 18. Evaluation Metrics

## 18.1 Classification

### Accuracy

``` text
(TP + TN) / (TP + TN + FP + FN)
```

Useful when classes and error costs are reasonably balanced.

### Precision

``` text
TP / (TP + FP)
```

### Recall

``` text
TP / (TP + FN)
```

### F1

``` text
2 * Precision * Recall / (Precision + Recall)
```

### ROC-AUC

Measures ranking quality across classification thresholds.

### PR-AUC

Often more informative under strong class imbalance.

------------------------------------------------------------------------

## 18.2 Detection

### IoU

``` text
intersection / union
```

### GIoU / DIoU / CIoU

Extensions that incorporate geometric relationships beyond simple
overlap.

### mAP

Mean Average Precision aggregates precision-recall performance across
classes and specified IoU thresholds.

Always state the evaluation convention, e.g.:

``` text
mAP@0.5
mAP@0.5:0.95
```

These are not equivalent metrics.

------------------------------------------------------------------------

## 18.3 Segmentation

### IoU / Jaccard

``` text
TP / (TP + FP + FN)
```

### Dice

``` text
2TP / (2TP + FP + FN)
```

### Pixel accuracy

Can be misleading for heavily imbalanced backgrounds.

### Boundary metrics

Useful when boundary precision is more important than area overlap.

------------------------------------------------------------------------

## 18.4 Image restoration

### MSE

Penalizes squared reconstruction error.

### PSNR

``` text
10 log10(MAX² / MSE)
```

Higher is generally better.

### SSIM

Measures structural similarity using luminance, contrast, and structural
terms.

### MS-SSIM

Extends SSIM across scales.

### LPIPS

Uses deep feature representations to estimate perceptual distance.

Lower is generally better.

### NIMA

Predicts aesthetic/technical quality distributions rather than direct
pixel fidelity.

### NIQE / BRISQUE

No-reference image-quality metrics. They measure statistical quality
characteristics and should not be interpreted as perfect proxies for
human preference.

------------------------------------------------------------------------

## 18.5 Generative models

### FID

Compares distributions of feature embeddings from real and generated
samples.

Lower is generally better, but FID is sensitive to:

- feature extractor;
- sample count;
- preprocessing;
- implementation;
- domain mismatch.

### KID

Kernel-based distribution distance with an unbiased estimator.

### CLIP-based metrics

Can estimate image-text semantic alignment but should not be treated as
complete measures of image quality.

### Precision / Recall for generative distributions

Can separately characterize fidelity and diversity.

------------------------------------------------------------------------

## 18.6 Language models

### Perplexity

Measures average predictive uncertainty:

``` text
PPL = exp(-mean(log p(token | previous tokens)))
```

Lower is generally better on a fixed evaluation distribution.

Perplexity alone does not measure instruction following, factuality,
reasoning, safety, or user usefulness.

### Exact Match

Useful for structured answer tasks.

### BLEU / ROUGE

Useful for some text-generation comparisons but imperfect proxies for
semantic quality.

### Human evaluation

Still important for:

- helpfulness;
- correctness;
- instruction following;
- style;
- factuality;
- safety.

------------------------------------------------------------------------

## 18.7 Time-series and forecasting

### MAE

``` text
mean(|y-y_hat|)
```

### MSE

``` text
mean((y-y_hat)^2)
```

### RMSE

Square root of MSE.

### MAPE

Can behave poorly when actual values are near zero.

### sMAPE

Provides a more symmetric percentage-style error but still has
interpretation limitations.

### Directional accuracy

Measures whether predicted direction matches actual direction.

### Sharpe ratio

A portfolio-level risk-adjusted performance measure, not a generic
model-accuracy metric.

------------------------------------------------------------------------

# 19. Dataset Engineering

## 19.1 Deduplication

### Exact deduplication

Cryptographic hashes identify byte-identical files.

Examples:

- SHA-256;
- SHA-512.

### Near-duplicate text

MinHash and LSH can efficiently identify candidate similar documents.

### Perceptual image deduplication

pHash and related methods identify visually similar images.

### Semantic deduplication

Embedding similarity can identify semantically similar content.

No single threshold is universally correct. Thresholds must be validated
for the dataset and task.

------------------------------------------------------------------------

# 20. Class Imbalance

Approaches include:

- class-weighted losses;
- focal loss;
- oversampling;
- undersampling;
- balanced batch construction;
- synthetic sampling;
- threshold optimization;
- hard-negative mining.

### Important warning

Oversampling does not create genuinely new information unless the
transformation adds useful variation.

------------------------------------------------------------------------

# 21. Augmentation

Augmentation should preserve task-relevant semantics.

Examples:

### Vision

- crop;
- resize;
- flip;
- rotation;
- color perturbation;
- blur;
- noise;
- perspective;
- Mixup;
- CutMix.

### Audio

- time masking;
- frequency masking;
- noise;
- time stretch;
- pitch changes where valid.

### Text

- paraphrasing;
- back translation;
- controlled substitution.

### Critical rule

Never apply an augmentation that changes the target semantics unless the
label/target is transformed consistently.

------------------------------------------------------------------------

# 22. Sampling and Curriculum

## Temperature sampling

For multiple datasets:

``` text
p_i = n_i^(1/T) / sum_j n_j^(1/T)
```

Interpretation depends on the exact convention used by the
implementation.

Sampling can be used to:

- prevent small datasets from being ignored;
- control domain mixture;
- rebalance tasks;
- implement curriculum strategies.

## Curriculum learning

Training examples can be ordered from:

``` text
easy -> difficult
```

or from broad foundational data toward specialized examples.

Curriculum is not universally beneficial; it should be validated
experimentally.

------------------------------------------------------------------------

# 23. Sharding and Streaming

Large datasets should be designed around the training access pattern.

Consider:

- shard size;
- sample size;
- worker count;
- network bandwidth;
- storage latency;
- cache capacity;
- object-store request cost;
- deterministic resumption;
- distributed shuffling.

### GPU starvation

If the GPU spends significant time waiting for data, increasing model
compute efficiency may not improve end-to-end throughput.

Monitor:

``` text
GPU utilization
data-loader wait time
CPU utilization
storage throughput
network throughput
batch latency
prefetch depth
```

------------------------------------------------------------------------

# 24. Data Splitting Best Practices

## Random split

Appropriate only when samples are sufficiently independent.

## Stratified split

Preserves approximate class proportions.

## Group split

Keeps correlated entities in one partition.

## Temporal split

Training occurs on past data and validation/test occurs on future data.

## Spatial split

Useful when neighboring spatial regions are correlated.

## Cross-validation

Useful when data is limited, but must respect grouping and temporal
constraints.

------------------------------------------------------------------------

# 25. Training Pathology

## Overfitting

Typical pattern:

``` text
training loss ↓
validation loss ↓ then ↑
```

Possible responses:

- more data;
- stronger regularization;
- augmentation;
- smaller model;
- early stopping;
- better split;
- remove leakage.

## Underfitting

Typical pattern:

``` text
training performance poor
validation performance also poor
```

Possible responses:

- larger model;
- longer training;
- better optimization;
- improved features;
- less restrictive regularization.

## Vanishing gradients

Gradients become too small for effective learning.

Possible mitigations:

- residual connections;
- normalization;
- activation changes;
- architecture changes;
- initialization improvements.

## Exploding gradients

Gradients become excessively large.

Possible mitigations:

- lower learning rate;
- gradient clipping;
- normalization;
- architecture changes;
- numerical stabilization.

## NaN divergence

Potential causes:

- invalid inputs;
- excessive learning rate;
- overflow;
- invalid operations;
- unstable mixed precision;
- corrupted loss;
- bad labels.

Debug systematically rather than changing many parameters
simultaneously.

## CUDA OOM

Potential causes:

- batch size;
- resolution;
- sequence length;
- model size;
- optimizer state;
- activations;
- fragmentation;
- worker duplication;
- validation memory;
- distributed replication.

Possible mitigations:

- smaller micro-batch;
- gradient accumulation;
- activation checkpointing;
- mixed precision;
- sharding;
- lower resolution;
- fewer workers;
- memory-aware validation.

------------------------------------------------------------------------

# 26. Reproducibility

Record:

``` text
random seeds
dataset version
dataset manifest/checksum
model version
code revision
dependency versions
CUDA/runtime version
hardware
training configuration
optimizer
scheduler
precision
batch size
gradient accumulation
checkpoint
```

A training result without provenance is difficult to reproduce or audit.

------------------------------------------------------------------------

# 27. Checkpointing

A robust checkpoint should preserve enough state to resume training
consistently.

Possible contents:

``` text
model state
optimizer state
scheduler state
AMP scaler
epoch
step
global sample position
RNG state
configuration
dataset version
code revision
```

A deployment weight file is generally much smaller in scope than a full
resumable checkpoint.

------------------------------------------------------------------------

# 28. Hyperparameter Search

Common strategies:

- grid search;
- random search;
- Bayesian optimization;
- population-based methods;
- successive halving;
- Hyperband.

Random search can outperform grid search when only a small subset of
hyperparameters strongly affects performance.

Do not compare runs fairly unless:

- datasets are equivalent;
- evaluation protocol is equivalent;
- compute budget is understood;
- preprocessing is equivalent.

------------------------------------------------------------------------

# 29. Model Selection

Choose models based on the complete constraint set:

``` text
task
dataset
accuracy target
latency target
memory limit
training budget
deployment hardware
interpretability
maintenance requirements
```

A larger or newer model is not automatically better.

------------------------------------------------------------------------

# 30. Quantization

Quantization reduces numerical precision.

Common levels:

``` text
FP32
FP16
BF16
FP8
INT8
INT4
```

Benefits:

- smaller models;
- lower memory;
- potentially higher inference throughput.

Costs:

- accuracy degradation;
- calibration complexity;
- hardware/runtime dependence.

Quantization-aware training can train the model while simulating
quantization effects.

Post-training quantization applies quantization after training.

------------------------------------------------------------------------

# 31. Knowledge for an AI Training Helper

A high-quality AI Helper should reason across four layers:

``` text
GENERAL AI KNOWLEDGE
        +
PLATFORM / DOMAIN IMPLEMENTATION KNOWLEDGE
        +
CURRENT RUNTIME STATE
        +
USER'S CURRENT TASK
```

The LLM should not hallucinate runtime facts.

For example:

``` text
Question:
"Why is my training slow?"

Static knowledge can explain:
- I/O bottlenecks
- CPU bottlenecks
- GPU utilization
- network latency
- data-loader configuration

Runtime tools should provide:
- GPU utilization
- CPU usage
- batch latency
- storage throughput
- current model
- dataset
- workers
- memory
```

The final answer combines both.

------------------------------------------------------------------------

# 32. AI Helper Decision Rules

When answering a technical question:

1. Identify the user's task.
2. Identify modality and dataset type.
3. Identify constraints.
4. Distinguish general AI knowledge from Studio-specific behavior.
5. Check whether the answer depends on current runtime state.
6. State assumptions.
7. Recommend the smallest set of relevant changes.
8. Explain trade-offs.
9. Warn about dangerous or irreversible changes.
10. Never invent unsupported Studio functionality.
11. Distinguish documented fact from heuristic recommendation.
12. If evidence is insufficient, say so.

------------------------------------------------------------------------

# 33. Common AI Training Misconceptions

### "More data always improves the model."

False. Additional low-quality, duplicated, contaminated, or
distribution-mismatched data can reduce quality.

### "Higher training accuracy means a better model."

False. Generalization and task-specific evaluation matter.

### "Lower loss always means better output."

False. The training loss may not correlate perfectly with the desired
metric.

### "Bigger batch size is always faster."

False. Hardware utilization can improve, but communication, memory,
optimization dynamics, and scaling efficiency matter.

### "More epochs are always better."

False. More training can overfit or waste compute.

### "A newer architecture is automatically superior."

False. Architecture quality is task- and constraint-dependent.

### "FP16 and BF16 are equivalent."

False. Their exponent and mantissa properties differ.

### "ONNX is a model weight format like Safetensors."

Incomplete. ONNX represents a computational graph and associated tensors
for interoperability/execution.

### "GGUF is a universal AI model format."

False. It is strongly optimized for a particular LLM inference
ecosystem.

### "A checkpoint and a model file are the same."

False. A resumable checkpoint may contain optimizer, scheduler, scaler,
RNG, and training metadata.

------------------------------------------------------------------------

# 34. Comparison Knowledge the AI Helper Should Master

The training corpus should explicitly teach comparisons such as:

``` text
Parquet vs WebDataset
Parquet vs Zarr
Zarr vs HDF5
JSONL vs Parquet
TFRecord vs WebDataset
LMDB vs loose files

Safetensors vs PyTorch checkpoint
Safetensors vs ONNX
ONNX vs TensorRT
GGUF vs Safetensors
TensorRT vs OpenVINO

CNN vs ViT
ResNet vs ConvNeXt
ViT vs Swin
U-Net vs transformer encoder-decoder
GAN vs diffusion
Transformer vs SSM
Dense model vs MoE

SGD vs AdamW
Adam vs AdamW
FP16 vs BF16
Batch size vs gradient accumulation
DDP vs FSDP
FSDP vs ZeRO
LoRA vs full fine-tuning
LoRA vs QLoRA

PSNR vs SSIM
SSIM vs LPIPS
FID vs KID
ROC-AUC vs PR-AUC
MAE vs RMSE
```

The correct answer must always be conditional on the task and
constraints.

------------------------------------------------------------------------

# 35. General Recommendations by Scenario

## Large image restoration dataset

Consider:

``` text
WebDataset / Zarr / suitable sharded binary representation
+
streaming
+
deterministic shuffling
+
group-aware splitting
+
perceptual + pixel metrics
```

## Large tabular dataset

Consider:

``` text
Parquet
+
Arrow
+
column projection
+
predicate filtering
+
partitioning
```

## LLM instruction/SFT dataset

A practical source representation is:

``` text
JSONL
```

with explicit:

``` text
messages
system/developer instructions where applicable
user input
assistant response
metadata
source/provenance
quality flags
```

The final training framework may transform this into tokenized
binary/sharded representations.

## Scientific N-dimensional data

Consider:

``` text
Zarr
or
HDF5 / NetCDF
```

depending on ecosystem and access pattern.

## Local LLM inference

Consider:

``` text
GGUF
```

when the target runtime supports it.

## Cross-platform inference

Consider:

``` text
ONNX
```

when the model operators and target runtime are compatible.

## NVIDIA production inference

Consider:

``` text
TensorRT
```

when hardware-specific optimization justifies compilation and
portability constraints are acceptable.

------------------------------------------------------------------------

# 36. General AI Knowledge Safety and Reliability Rules

A training assistant should:

- distinguish facts from estimates;
- distinguish benchmark results from theoretical expectations;
- identify version-dependent behavior;
- avoid fabricating unsupported APIs;
- avoid claiming a metric proves overall model quality;
- warn when evaluation is invalid due to leakage;
- avoid treating a single benchmark as universal;
- identify when a recommendation requires empirical validation;
- preserve dataset provenance;
- treat untrusted serialized model files as potentially dangerous;
- never recommend executing untrusted pickle-based checkpoints
    blindly.

------------------------------------------------------------------------

# 37. Recommended Knowledge-Base Metadata

Every extracted concept should be representable using metadata such as:

``` yaml
concept_id:
title:
domain:
subdomain:
definition:
aliases:
related_concepts:
common_confusions:
best_use_cases:
poor_use_cases:
advantages:
limitations:
failure_modes:
selection_criteria:
metrics:
frameworks:
hardware:
source_type: general_ai
confidence:
```

For training examples:

``` yaml
example_id:
task_type: explanation | comparison | diagnosis | procedure | recommendation
domain:
difficulty:
question:
context:
answer:
reasoning_summary:
constraints:
common_wrong_answer:
correction:
```

------------------------------------------------------------------------

# 38. Final General AI Training Continuum

``` text
                    RAW DATA
                       |
                       v
             +-------------------+
             | DATA ENGINEERING   |
             | clean / split /   |
             | deduplicate /     |
             | validate          |
             +-------------------+
                       |
                       v
             +-------------------+
             | SERIALIZATION     |
             | Parquet / Zarr /  |
             | WebDataset / ...  |
             +-------------------+
                       |
                       v
             +-------------------+
             | MODEL             |
             | CNN / Transformer |
             | U-Net / Diffusion |
             | MoE / SSM / ...   |
             +-------------------+
                       |
                       v
             +-------------------+
             | OPTIMIZATION      |
             | loss / optimizer  |
             | LR / precision    |
             | regularization    |
             +-------------------+
                       |
                       v
             +-------------------+
             | DISTRIBUTED       |
             | DDP / FSDP / ZeRO |
             | TP / PP           |
             +-------------------+
                       |
                       v
             +-------------------+
             | EVALUATION        |
             | task metrics      |
             | robustness / OOD  |
             +-------------------+
                       |
                       v
             +-------------------+
             | CHECKPOINT /      |
             | EXPORT            |
             | Safetensors /    |
             | ONNX / GGUF / ... |
             +-------------------+
                       |
                       v
             +-------------------+
             | DEPLOYMENT        |
             | cloud / server /  |
             | desktop / edge    |
             +-------------------+
```

------------------------------------------------------------------------

# 39. Summary

The central principle of modern AI engineering is **constraint-aware
system design**.

There is no universally best:

- dataset format;
- model architecture;
- optimizer;
- precision;
- batch size;
- distributed strategy;
- metric;
- serialization format.

The correct decision depends on:

``` text
task
+
data
+
scale
+
access pattern
+
model
+
hardware
+
training budget
+
evaluation requirements
+
deployment target
```

A high-quality AI Training Helper must therefore learn not only
definitions but **relationships, trade-offs, failure modes, selection
criteria, and uncertainty**.

The General AI Knowledge layer provides the universal technical
foundation.

Domain-specific or application documentation provides the implementation
and tool-integration layer.

Runtime telemetry and APIs provide active environment state.

Together these form a reliable, context-aware AI training assistant rather than a
static chatbot.

------------------------------------------------------------------------

# Appendix A: Training-Corpus Coverage Checklist

This document is intended to provide excellent general coverage of:

- [x] CSV / TSV
- [x] JSONL / NDJSON
- [x] Parquet
- [x] Apache Arrow / IPC
- [x] Zarr
- [x] TFRecord
- [x] WebDataset
- [x] HDF5
- [x] NetCDF
- [x] LMDB
- [x] streaming/sharded dataset concepts
- [x] dataset manifests
- [x] dataset validation
- [x] leakage
- [x] deduplication
- [x] class imbalance
- [x] augmentation
- [x] sampling
- [x] sharding
- [x] train/validation/test splitting
- [x] Safetensors
- [x] PyTorch checkpoints
- [x] ONNX
- [x] GGUF
- [x] GGML
- [x] TensorRT
- [x] OpenVINO
- [x] Core ML
- [x] TFLite/LiteRT
- [x] JAX/Orbax checkpoint concepts
- [x] CNN
- [x] ResNet
- [x] EfficientNet
- [x] ConvNeXt
- [x] ViT
- [x] Swin
- [x] Transformer
- [x] U-Net
- [x] GAN
- [x] VAE
- [x] Diffusion
- [x] MoE
- [x] State Space Models
- [x] SGD
- [x] Momentum
- [x] Adam
- [x] AdamW
- [x] RMSProp
- [x] LARS / LAMB
- [x] Lion
- [x] Sophia
- [x] Muon
- [x] learning-rate schedules
- [x] warmup
- [x] cosine decay
- [x] OneCycle
- [x] WSD
- [x] regularization
- [x] normalization
- [x] mixed precision
- [x] FP16 / BF16 / FP8
- [x] gradient accumulation
- [x] DDP
- [x] FSDP
- [x] ZeRO
- [x] tensor parallelism
- [x] pipeline parallelism
- [x] LoRA
- [x] QLoRA
- [x] SFT
- [x] DPO
- [x] PPO/RLHF concepts
- [x] classification metrics
- [x] detection metrics
- [x] segmentation metrics
- [x] restoration metrics
- [x] generative metrics
- [x] language-model metrics
- [x] forecasting metrics
- [x] quantization
- [x] reproducibility
- [x] checkpointing
- [x] hyperparameter search
- [x] pathology
- [x] model selection
- [x] deployment trade-offs
- [x] AI Helper reasoning principles

------------------------------------------------------------------------

# Appendix B: Important Terminology Distinctions

The training corpus should preserve these distinctions:

  ------------------------------------------------------------------------
  Term A                  Must not be treated as  Key distinction
                          identical to
  ----------------------- ----------------------- ------------------------
  Dataset                 Dataset format          Dataset is the data;
                                                  format is its
                                                  representation

  Dataset                 Training split          Dataset may contain
                                                  multiple splits

  Checkpoint              Model weights           Checkpoint can contain
                                                  full training state

  Weights                 Architecture            Weights are parameters;
                                                  architecture defines
                                                  computation

  ONNX                    Safetensors             ONNX represents a
                                                  computational graph;
                                                  Safetensors stores
                                                  tensors

  GGUF                    Universal model format  GGUF is primarily an LLM
                                                  inference ecosystem
                                                  format

  Loss                    Metric                  Loss is optimized;
                                                  metric evaluates

  Validation              Test                    Validation influences
                                                  development; test should
                                                  remain isolated

  Batch size              Micro-batch             A micro-batch may be
                                                  accumulated before
                                                  optimizer update

  Epoch                   Optimizer step          One epoch traverses a
                                                  dataset; one optimizer
                                                  step updates parameters

  Precision               Quantization            Precision describes
                                                  numerical
                                                  representation;
                                                  quantization is a
                                                  broader
                                                  conversion/compression
                                                  process

  Data parallelism        Model parallelism       Data parallelism
                                                  replicates model
                                                  computation across data;
                                                  model parallelism
                                                  partitions the model

  LoRA                    Quantization            LoRA changes trainable
                                                  parameterization;
                                                  quantization changes
                                                  numerical representation

  SFT                     RLHF                    SFT is supervised
                                                  learning; RLHF uses
                                                  preference/reward
                                                  optimization

  PSNR                    Perceptual quality      PSNR measures pixel
                                                  error, not human
                                                  preference

FID                     Human quality           FID is a distributional
                                                  statistic, not a
                                                  complete
                                                  human-evaluation
                                                  substitute
  ------------------------------------------------------------------------

------------------------------------------------------------------------

# Appendix C: Required Behavior for Derived AI-Helper Training Examples

Derived SFT examples should teach the model to:

1. answer definitions precisely;
2. compare alternatives conditionally;
3. explain pros and cons;
4. identify hidden constraints;
5. diagnose symptoms systematically;
6. distinguish root cause from symptom;
7. recommend measurements before speculative fixes;
8. state when an answer is framework-specific;
9. state when empirical validation is required;
10. avoid absolute claims where evidence is conditional;
11. preserve the distinction between general AI knowledge and
    Studio-specific knowledge;
12. never invent a Studio feature merely because the general technology
    exists.

------------------------------------------------------------------------

# Appendix D: Source Authority Boundary

For an intelligent AI training assistant:

``` text
GENERAL_AI_TRAINING_KNOWLEDGE.md
    = general AI/ML scientific principles & training dynamics

PLATFORM / APPLICATION MANUALS
    = platform architecture, workflows, models, GUI and tool implementations

CURRENT STATE / REGISTRY
    = active framework configurations, installed packages and models

RUNTIME TOOLS & TELEMETRY
    = current hardware, active jobs, metrics, files, environment, and GPU telemetry

USER CONTEXT
    = current task, objectives, constraints and intent
```

The assistant should prefer the most authoritative and current source
available for the specific question.

------------------------------------------------------------------------

# Document End
