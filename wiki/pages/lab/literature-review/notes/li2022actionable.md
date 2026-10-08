---
key: li2022actionable
title: "Actionable and Interpretable Fault Localization for Recurring Failures in Online Service Systems (DéjàVu)"
authors: "Zeyan Li; Nengwen Zhao; Mingjie Li; Xianglin Lu; Lixin Wang; Dongdong Chang; Xiaohui Nie; Li Cao; Wenchi Zhang; Kaixin Sui; Yanhua Wang; Xu Du; Guoqiang Duan; Dan Pei"
year: 2022
venue: "ESEC/FSE '22, Singapore (ACM); arXiv 2207.09021v3 read"
publisher: "ACM"
doc_type: proceedings-article
doi: "10.1145/3540250.3549092"
issn: ""
scopus_indexing: "unverified: FSE proceedings not checked in the Scopus preview"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (ESEC/FSE '22 proceedings; arXiv author copy read)"
cited_by_crossref: ""
n_references: "about 61"
license: ""
batch: "10"
read_status: reviewed                  # text read through Sec 6.2; discussion tail and references not read; Figs 7-21 not inspected
pages: 13
text_chars: 0
metadata_source: crossref+arxiv
task: "localize faulty failure units (component + metric group) for recurring failures"
supervision: "supervised (trained offline on historical failures with ground-truth failure units)"
online_or_streaming: "no (offline training, sub-second localization per failure)"
telemetry: "metrics only (traces and CMDB used to build the failure dependency graph)"
propagation_modeling: "failure dependency graph over failure units (call and deployment relations) + 8 stacked GAT layers"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "A: production microservice system of an ISP (188 failures); B: production bank system (158); C: Oracle database system, 99 real failures; D: Train-Ticket (156 injected)"
datasets: "601 failures; A, B, D injected failures; C real; replication package stated"
dataset_open: "stated: replication package (not checked)"
code_open: "stated: replication package (not checked)"
baselines_compared: "JSS'20, iSQUAD (similar-failure matching), DT, GB, RF, SVM, RandomWalk@Metric, RandomWalk@FI"
metrics: "A@k, mean average rank (MAR), time"
headline_result: "MAR 1.66 to 5.03; A@1 61.84% to 77.18%, A@5 79.24% to 96.32% (Table 3 p.8); Random Forest reaches higher A@1 on B and D (84.46%, 85.66%)"
evidence_quality: "3"
relevance_to_us: "4"
overlap_with_us: "medium (graph-attention propagation; supervised)"
threat_level_for_novelty: "low-medium"
---

# DéjàVu (Li et al., FSE 2022)

> Notes from the **full text** of the arXiv version (13 pages), read to Section 6.2. Page numbers are PDF pages. Figures not inspected.

## 1. Summary
DéjàVu learns, from historical failures of a given system, which "failure unit" (component plus group of metrics) is faulty. Each unit's metrics are encoded with GRU and CNN layers, then aggregated over a failure dependency graph (FDG) of call and deployment relations with eight stacked graph-attention layers; a classifier scores units. Interpretation uses decision-tree surrogates and similar historical failures.

## 2. Problem and motivation
- Localization to a metric or component alone is not actionable; engineers need component plus failure kind (p.1).
- Motivation evidence: at one large bank 576 failure tickets over 12 months, 74.38% recurring (Fig 1, p.2); over 20,000 tickets in two years with average diagnosis time 28.98 minutes (median 9.65) and failure-unit localization about 9.2 minutes (p.3). Single-company measurements.

## 3. Method (pp.3-6)
- FDG: undirected graph over failure units; edges from call relations (tracing) and deployment relations (CMDB: service on container on server); engineers may edit (pp.3-4).
- Feature extractor (GRU, 1-D CNN, FC), 8 GAT layers with 4 heads and residuals, classifier with class-weighted BCE and class-balanced sampling (pp.4-5).

## 4. Data and experimental setup (pp.6-7)
- Four datasets, 601 failures; each split 40% train, 20% validation, 40% test; 10 repeated runs (p.7). Injected failures in A, B, D (10 types in A and B; 8 in D), real failures in C (99).
- Random split by failure; failures of the same injected type and system appear in train and test (this is the "recurring failure" setting by design).

## 5. Results (copied)
| Dataset | Metric | DéjàVu | Best baseline | Baseline name | Page |
|---|---|---|---|---|---|
| A | MAR / A@1 / A@5 | 1.66 / 77.18% / 96.28% | 1.88 / 73.37% / 95.71% | Random Forest | Table 3 p.8 |
| B | MAR / A@1 / A@5 | 5.03 / 66.21% / 79.24% | 8.75 / 84.46% / 88.92% | Random Forest | Table 3 |
| C (99 real failures) | MAR / A@1 / A@5 | 1.70 / 61.84% / 96.32% | 2.26 / 61.05% / 87.10% | Random Forest | Table 3 |
| D (Train-Ticket) | MAR / A@1 / A@5 | 2.63 / 75.62% / 94.27% | 12.35 / 85.66% / 91.88% | Random Forest | Table 3 |
| Ablation without graph aggregation (MAR) | A 2.32, B 5.77, C 1.75, D 3.81 | n/a | n/a | n/a | Table 3 |
- Statistical tests: t-test and Cohen's d on MAR across 10 runs (p.7). Effect sizes reported as "huge" use the 10 repeated trainings, not independent failures.

## 6. Limitations
- Stated: recurring failures only; non-recurring failures yield low scores and are warned; failure units are manually defined; unseen failure units handled by sharing weights (pp.9-11).
- **My critique:**
  1. Supervised and tied to a given system's history; not applicable in the label-free cold-start setting.
  2. A plain Random Forest on time-series features has higher A@1 than DéjàVu on B and D (84.46% vs 66.21%, 85.66% vs 75.62%); DéjàVu wins on MAR (fewer bad cases), which the paper notes (p.7), but the A@1 gap is large.
  3. Effect sizes are computed over repeated runs of the same split, not over independent failures; no significance across data splits.
  4. Ground truth on injected failures (A, B, D) is the injection; random 40/20/40 split with repeated injection types allows pattern reuse; the real-failure set C has no graph (single virtual vertex), so the propagation part is not tested there, as the paper admits (p.8).
  5. The FDG includes deployment relations (service-on-container-on-server). The ablation without graph aggregation raises MAR by 3% to 31%, so modelling co-location/call structure helps on B and D.
- Not discussed: failure-time sensitivity; how much of the gain comes from the hand-defined metric groups.

## 7. Reproducibility
- Datasets and code stated in a replication package (not checked). Production data A, B, C may be proprietary.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | supervised | none | ours |
| Live / streaming | offline | incremental | ours (claimed) |
| Telemetry used | metrics; graph from traces + CMDB | traces (+ metrics) | theirs (deployment edges) |
| Propagation modelling | GAT on FDG with call and deployment edges | call-edge probabilities | theirs richer |
| Forecasts future failures | no | claimed | n/a |
| Explanation | decision-tree surrogate + similar failures | templates | theirs |
| Evaluation rigor | 601 failures, 10 runs, RF baseline | synthetic | theirs |
| Open / reproducible | stated | yes | tie |

- **What they have that we do not:** deployment (co-location) edges in the propagation graph; interpretability methods.
- **What we have that they do not:** label-free operation.
- **Could a reviewer say "this already exists"?** For "graph attention over call and deployment edges for RCA": yes (supervised). A baseline or related-work citation is needed.
- **Position:** cite as the supervised, interpretable GNN RCA; evidence that deployment edges matter (ablation).
- **Must we run it as a baseline?** Optional (needs labels).

## 9. Does this paper change what problem we should solve?
- It strengthens the limitation: call-edge-only propagation omits deployment edges that a strong supervised model uses. It also shows the supervised ceiling (A@1 about 75%) that a label-free method should be compared with fairly.

## 10. Citation-ready facts (each with page)
- "At one commercial bank, 74.38% of 576 failure tickets over 12 months were recurring (Fig 1 p.2)".
- "DéjàVu's FDG joins failure units by call and deployment relations; removing graph aggregation worsened mean average rank by 3.19% to 30.92% across datasets (p.8)".

## 11. Open questions / things to verify
- Discussion tail and references; replication package contents; Scopus status.
