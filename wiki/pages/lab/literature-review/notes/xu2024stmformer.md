---
key: xu2024stmformer
title: "System States Forecasting of Microservices with Dynamic Spatio-Temporal Data (STMformer)"
authors: "Yifei Xu; Jingguo Ge; Haina Tang; Shuai Ding; Tong Li; Hui Li"
year: 2024
venue: "arXiv preprint 2408.07894v1 (cs.NI, 15 Aug 2024); ACM-format template 'Conference'24' with placeholder DOI; published venue unverified"
publisher: "arXiv"
doc_type: preprint
doi: "10.48550/arxiv.2408.07894"
issn: ""
scopus_indexing: "arXiv preprints are not Scopus-indexed; any published version not checked"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "preprint (no review evidence)"
cited_by_crossref: ""
n_references: "42"
license: ""
batch: "8"
read_status: reviewed                  # full text read; Figs 1-4 not inspected
pages: 11
text_chars: 56283
metadata_source: arxiv
task: "multivariate metric forecasting for pods (system state), short and long horizons; not failure prediction"
supervision: "self-supervised on metric windows (forecasting loss); no fault labels used in training"
online_or_streaming: "no (offline windows)"
telemetry: "metrics collected with eBPF/cgroups (80+ metrics per pod, host metrics, TCP connection events used for dynamic adjacency)"
propagation_modeling: "dynamic adjacency from TCP connections + GAT + global patch cross-attention ('cascading effects'); no explicit propagation target"
forecasts_future_failures: "no (forecasts metric values; faults are only present in the data)"
llm_used: "no"
systems_evaluated: "Train-Ticket (41 services, 7 VMs), one deployment"
datasets: "own dataset: about 14,000 samples (64 steps x 56 pods x 80 features), 5 s sampling, 1-2 hours per condition, six Chaos Mesh faults plus normal (p.6)"
dataset_open: "not stated for the dataset; code stated at https://github.com/xuyifeiiie/STMformer (not checked)"
code_open: "stated (not checked)"
baselines_compared: "Informer, Autoformer, FEDformer, PatchTST, TimesNet, DLinear, STSGCN, STSGT"
metrics: "MAE, MSE, RMSE on normalised data"
headline_result: "abstract: 8.6% MAE and 2.2% MSE reduction vs next best; Table 1 short-term step 16: STMformer MAE 0.01663 vs FEDformer 0.01709, MSE 0.002102 vs PatchTST 0.002126 (p.7)"
evidence_quality: "2"
relevance_to_us: "3"
overlap_with_us: "low-medium (co-location and call-edge propagation inputs for forecasting metrics)"
threat_level_for_novelty: "low"
---

# STMformer (Xu et al., arXiv 2024)

> Notes from the **full text** (`litdb/texts/yifeixu...txt`). Page numbers are PDF pages. Figs 1-4 not inspected.

## 1. Summary
A transformer model that forecasts metric time series of microservice pods using three message modules: same-host interactions (IMM), a graph attention network over per-step TCP-connection adjacency matrices (SMM), and a temporal module combining TimesNet blocks with a global patch cross-attention that is meant to capture cascading effects. Evaluated on one Train-Ticket deployment with six injected fault types, against six time-series and two spatio-temporal baselines.

## 2. Problem and motivation
- Forecasting system states helps AIOps tasks; microservice states depend on host co-location, call connections and delayed cascading effects (pp.1-2). Fig 1(b) shows one example of delayed CPU fluctuation in a neighbour after a fault. Evidence: one demonstration, not a rate.

## 3. Method (pp.4-6)
Series decomposition, embedding, one-stride patching; encoder with IMM, SMM, TMM (TimesBlock plus PatchCrossAttention mixed by a random matrix alpha, Eq 6); global spatio-temporal adjacency from STSGT; ProbSparse attention. Time-varying adjacency from eBPF-observed TCP connection latency and frequency.

## 4. Data and setup (pp.6-8)
- Own collector (coroot-node-agent based), 80+ metrics, 5-second sampling, 1-2 hours per condition, 41-service Train-Ticket on seven VMs, Locust load, six Chaos Mesh faults (p.6).
- Split 8:1:1, horizon equals prediction length, 16 and 32 (short) and 64 and 128 (long) steps (p.8).
- Whether windows are split by time or at random is not stated; overlapping windows from one run with a random split would leak.

## 5. Results (copied)
| Task | Metric | Theirs | Best baseline | Page |
|---|---|---|---|---|
| Short, step 16 | MAE / MSE | 0.01663 / 0.002102 | FEDformer 0.01709 MAE; PatchTST 0.002126 MSE | Table 1 p.7 |
| Short, step 32 | MAE / MSE | 0.01623 / 0.002084 | TimesNet 0.01684 MAE; PatchTST 0.002135 MSE | Table 1 |
| Long, step 64 | MAE / MSE | 0.01644 / 0.002040 | PatchTST 0.01899 MAE; 0.002053 MSE | Table 2 p.8 |
| Long, step 128 | MAE / MSE | 0.01728 / 0.002126 | TimesNet 0.01818 MAE; PatchTST 0.002081 MSE (PatchTST better) | Table 2 |
| Ablation (step 64) | MAE | 0.01644 | w/o PCA 0.04434; w/o IMM 0.5768 | Table 3 p.8 |

## 6. Limitations
- Stated: computational cost, kernel selection, single modality (p.10).
- **My critique:**
  1. Task is metric forecasting; no evaluation of whether it predicts faults, anomalies or cascades earlier than a threshold on the raw series. The word "cascading effects" refers to a modelling module, not a measured outcome.
  2. The abstract's 8.6% MAE and 2.2% MSE gains do not match the tables I can compute: step 16 MAE gain over FEDformer is about 2.7% and MSE gain over PatchTST about 1.1%; at step 128 PatchTST has lower MSE (0.002081 vs 0.002126). The abstract numbers may be averages of specific cells; the paper does not show the calculation.
  3. Table 3's "w/o IMM" has MAE 0.5768 but RMSE 0.1300; MAE cannot exceed RMSE, so at least one number is wrong (as printed in the PDF text).
  4. No persistence baseline (predict last value) or seasonal naive baseline, which are strong when errors are around 0.017 on min-max scaled data.
  5. Random matrix alpha in Eq 6 is described as a "uniform random matrix"; the role is not justified.
  6. One deployment, one split, no repeated seeds or intervals; the STSGT baseline does not converge in some settings (p.8), so the spatio-temporal baselines are weak.
  7. Dataset release is not stated; the PDF carries a placeholder ACM DOI and conference name.
- Not discussed: leakage from overlapping windows, performance specifically around fault periods.

## 7. Reproducibility
- Code stated at github.com/xuyifeiiie/STMformer (not checked). Dataset not stated as released.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | none for training | none | tie |
| Live / streaming | offline windows | incremental windows | ours (claimed) |
| Telemetry used | eBPF metrics, TCP connections | traces (+ metrics) | theirs richer |
| Propagation modelling | dynamic adjacency + host co-location + attention | call-edge probabilities | theirs includes co-location |
| Forecasts future failures | no (forecasts metrics) | claimed | n/a |
| Explanation | none | templates | ours |
| Evaluation rigor | one run, no naive baseline | synthetic | neither |
| Open / reproducible | code stated | yes | tie |

- **What they have that we do not:** host co-location and connection-level dynamic adjacency as inputs.
- **What we have that they do not:** RCA output and a risk score tied to edges.
- **Could a reviewer say "this already exists"?** For "forecast pod metrics using call and co-location structure": yes. Not for cascade-risk scoring.
- **Position:** supports our limitation that call edges alone miss co-location effects; cite as forecasting prior art that uses host co-location.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- Slightly: it shows co-location (same host) is treated as a propagation channel in forecasting, which our call-edge model omits.

## 10. Citation-ready facts (each with page)
- "STMformer combines same-host attention, TCP-connection-based dynamic graphs and cross-time attention for pod metric forecasting on Train-Ticket" (pp.3-6).
- "Ablating the host-interaction module (IMM) or the connection module (SMM) increased error in the authors' ablation (Table 3 p.8), but Table 3 contains an inconsistent MAE/RMSE pair."

## 11. Open questions / things to verify
- Split protocol; whether the dataset is public; published version (if any).
