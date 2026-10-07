---
key: costsensitiv
title: "Cost-Sensitive Mamba Sequence Modeling for Fault Detection in Cloud-Native Microservice Systems"
authors: "Liu, Zhaocheng; Meng, Ru; Huang, Shao-yu; Huang, Zeyu (corresponding)"
year: 2024
venue: "Transactions on Computational and Scientific Methods, Vol. 4, No. 12 (2024), Pinnacle Science Press (the volume number is printed as 'Vo. 4')"
publisher: "Pinnacle Science Press"
doc_type: journal-article
doi: ""
issn: "2998-8780"
scopus_indexing: "not found (ISSN 2998-8780 returned 0 results in the Scopus Sources preview, 2026-10-07)"
scopus_match: "ISSN 2998-8780, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied; venue not found in Scopus preview"
peer_reviewed: "unclear (journal article; no review dates in the PDF)"
cited_by_crossref: ""
n_references: "14"
license: "unknown"
batch: "6"
read_status: reviewed                  # Figs 1-4 not inspected; Tables 1-2 read
pages: 11
text_chars: 33144
metadata_source: pdf-header
task: "detection (binary window-level anomaly classification), not RCA"
supervision: "supervised (labelled anomalous windows; class-weighted cross-entropy)"
online_or_streaming: "no (offline windows); claims suitability for online monitoring"
telemetry: "metrics only (CPU, memory, disk, network of 12 services plus inter-service response times)"
propagation_modeling: "none"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "RS-Anomic dataset built on the open-source RobotShop e-commerce microservices (12 services)"
datasets: "RS-Anomic: 100,464 normal and 14,112 anomaly instances, ten anomaly types (from the dataset README); the paper does not state the numbers or which test ratio it used"
dataset_open: "yes (github.com/ms-anomaly/rs-anomic exists, no license file; not downloaded)"
code_open: "not linked (the paper says dataset and loading scripts are in 'a public code repository', no URL)"
baselines_compared: "seven cited methods (Liu 2020, Xie 2023, Chen 2023, Cinque 2022, GAL-MAD 2025, Wang 2025, CAPAD 2025) with no implementation details"
metrics: "precision, recall, F1, AUROC, AUPRC, ECE, Brier, alarm rate"
headline_result: "precision 0.93, recall 0.89, F1 0.91, AUROC 0.98, AUPRC 0.96, ECE 0.021, Brier 0.062, alarm rate 0.20 vs best baseline (Cheng et al.) 0.90, 0.86, 0.88, 0.96, 0.93, 0.029, 0.076, 0.23 (Table 2, p.7)"
evidence_quality: "1"
relevance_to_us: "1"
overlap_with_us: "none (supervised detection on metrics)"
threat_level_for_novelty: "low"
---

# Cost-Sensitive Mamba Sequence Modeling for Fault Detection in Cloud-Native Microservice Systems

> Reading notes written from the **full text** (`litdb/texts/costsensitiv.txt`). Page numbers are PDF pages (11 pages).
> Figs 1-4 (preprocessing example, architecture, two sensitivity bar charts) not inspected.

## 1. One-paragraph summary
A short paper proposes a Mamba (state-space) sequence model that classifies sliding windows of multivariate metrics as anomalous or normal, trained with a class-weighted cross-entropy (weights 5.0 for anomalies and 1.0 for normal) labelled "cost-sensitive". On the RS-Anomic metrics dataset it reports higher precision, recall, F1, AUROC, AUPRC and calibration than seven cited methods.

## 2. Problem and motivation
- Problem: detect rare, costly faults under class imbalance and asymmetric error costs (pp.1-3).
- Motivation: generic statements about rare faults and cascading effects; no incident data or cost figures. Evidence type: assumed.
- Real? The idea that false negatives cost more than false positives is plausible but the paper uses no real cost numbers.

## 3. Method
- Preprocessing: time alignment, forward-fill and local linear interpolation, removal of constant and duplicate columns, quantile truncation and moving-median filtering, train-set standardization (p.3).
- Windows: L = 128, stride s = 16; window label = OR of point labels (Eq. on p.5).
- Model: linear projection of the window, Mamba-style recurrence h_t = A h_{t-1} + B(g_t ⊙ x_t) with a gating coefficient (p.5), final representation to a sigmoid anomaly probability; 4 layers, hidden size 256, dropout 0.10 (Table 1, p.6).
- Loss: weighted binary cross-entropy with weights 5.0 and 1.0; alarm threshold 0.5 (Table 1, p.7). The "cost" is only this class weight; no business cost is quantified.
- Optimization: AdamW, learning rate 1e-3, weight decay 1e-4, batch 64, 100 epochs, cosine annealing with 5% warm-up, seed 42 (Table 1).
- Assumptions: labelled anomaly windows for training; metrics only.

## 4. Data and setup
- Dataset RS-Anomic (p.3): 12 services of the RobotShop application with cAdvisor-type resource metrics and response times, ten anomaly types. The dataset README (github.com/ms-anomaly/rs-anomic, checked 2026-10-07) states 100,464 normal and 14,112 anomaly instances, i.e., about 12% anomalies, and provides test scenarios with normal:anomalous ratios of 95:5, 90:10 and 60:40; the paper says the dataset has a "clear dominance of normal samples" and "extreme class imbalance" but does not state counts, ratio used, or split.
- Protocol: "fixed data partitioning strategy" (p.6), no description of train, validation, test or time ordering; random seed 42 fixed; no repeats.
- Leakage: windows with stride 16 and length 128 overlap heavily, so a random split would leak; the split is not described.
- Hardware: RTX 4090 (Table 1).

## 5. Results (copied; Table 2, p.7)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Precision | 0.93 | 0.90 | Cheng et al. [14] (CAPAD) | Table 2 |
| Recall | 0.89 | 0.86 | Cheng et al. [14] | Table 2 |
| F1 | 0.91 | 0.88 | Cheng et al. [14] | Table 2 |
| AUROC / AUPRC | 0.98 / 0.96 | 0.96 / 0.93 | Cheng et al. [14] | Table 2 |
| ECE / Brier | 0.021 / 0.062 | 0.029 / 0.076 | Cheng et al. [14] | Table 2 |
| Alarm rate | 0.20 | 0.23 (Cheng), 0.17 (Cinque lowest) | n/a | Table 2 |

- The seven baselines rank in nearly strictly ascending order of publication date and score (Liu 2020 lowest F1 0.81; Cheng 2025 F1 0.88); no details of how each was re-implemented.
- Statistical testing: none; single run; no confidence intervals.
- Sensitivity (Figs 3-4, p.8-9): AUROC versus cost weight and training set size (bar charts, not inspected); text says performance rises, falls and rises again with cost weight.
- Efficiency: not reported.

## 6. Limitations
- Stated: none; future work on topology integration, drift adaptation and linking scores to mitigation (p.10).
- **My critique:**
  1. The baselines are published trace, log or graph models (e.g., DeepTraLog-type, GAL-MAD, CAPAD) listed with precision/recall for the same metrics-only dataset; the paper gives no implementation, hyper-parameters or code for any of them, and the results look implausibly smooth; unverifiable.
  2. "Cost-sensitive" is a class weight of 5:1, not a measured cost; no cost metric is reported; the 0.5 threshold is untuned; the central claim is untested.
  3. The dataset is described as extremely imbalanced; its README shows about 12% anomalies and test ratios as low as 5% to 40% anomalous; the used ratio is not stated.
  4. Overlapping windows (L = 128, s = 16) and an undescribed split raise leakage risk; no repeats or variance.
  5. Detection of known injected anomaly types only; not RCA, and not evidence about rare faults.
  6. Dataset license unknown; code not linked.
  7. The introduction claims microservice anomalies are "low frequency, long tails" and "cascading" without evidence.
- Not discussed: label cost, drift, false-alarm rate on healthy production data.

## 7. Reproducibility
- Dataset repository github.com/ms-anomaly/rs-anomic exists (last push 2023-06-22, no license; contains normal_data.zip, anomaly_data.zip, train.zip, test.zip per the README; not downloaded). Code for this paper: not provided.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | supervised | label-free | Ours lighter |
| Live / streaming | offline windows | incremental windows | Ours |
| Telemetry used | metrics | traces (+ metrics) | n/a |
| Propagation modelling | none | edge probabilities | Ours |
| Forecasts future failures | no | claimed | n/a |
| Explanation | none | templates | Ours |
| Evaluation rigor | one dataset, no repeats, unverifiable baselines | synthetic only | Neither convincing |
| Open / reproducible | dataset only | yes | Ours |

- **What they have that we do not:** a supervised metrics detector with calibration metrics (ECE, Brier) reported.
- **What we have that they do not:** localization, propagation, label-free calibration.
- **Could a reviewer say "this already exists"?** No.
- **Position:** do not cite as RCA literature; calibration metrics (ECE, Brier) are a useful reporting idea for our risk score.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- No. It is a detection paper with unverifiable comparisons. One transferable point: report calibration (ECE, Brier) and alarm rate for any risk score, as we plan for Task B.

## 10. Citation-ready facts (each with page)
- A Mamba-based window classifier with a 5:1 class-weighted loss reports F1 0.91 on the RS-Anomic dataset (Table 1 p.6-7, Table 2 p.7).
- It reports ECE and Brier score alongside detection metrics (Table 2, p.7).
- (Prefer not to cite; unverifiable baselines.)

## 11. Open questions / things to verify
- Which test ratio and split were used; whether any baseline was actually run; Figs 1-4.
- Venue status (ISSN 2998-8780 not found in Scopus preview).
