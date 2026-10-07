---
key: shuaiyuxiehanbinhejianwangbingli2025root
title: "Root Cause Analysis for Microservice Systems via Cascaded Conditional Learning with Hypergraphs (CCLH)"
authors: "Xie, Shuaiyu; He, Hanbin; Wang, Jian; Li, Bing"
year: 2025
venue: "arXiv:2511.17566v1 [cs.LG], 14 Nov 2025"
publisher: "arXiv"
doc_type: preprint
doi: ""
issn: ""
scopus_indexing: "not indexed (arXiv preprint; no journal reference in the arXiv record, checked 2026-10-07)"
scopus_match: ""
sjr_quartile: "n/a"
peer_reviewed: "no (preprint; submission status unknown)"
cited_by_crossref: ""
n_references: "41"
license: "arXiv"
batch: "5"
read_status: reviewed                  # Figs 1-6 not inspected (Figs 5 and 6 carry numbers in plots); Tables I-III read
pages: 11
text_chars: 65839
metadata_source: arxiv
task: "localization (instance-level) + failure type identification (supervised)"
supervision: "supervised (cross-entropy on culprit instance and failure type labels)"
online_or_streaming: "no (per-failure diagnosis, under 1 s per case)"
telemetry: "metrics, traces, logs (Drain templates), deployment configuration"
propagation_modeling: "heterogeneous hypergraph (call, deployment, load-balancing hyperedges) with attention; no forecasting"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "Dataset A: GAIA (10 instances, 1,099 labelled cases, 5 failure types); Dataset B: Online Boutique (489 injected cases); Dataset C: Sock Shop (700 injected cases); Chaos Mesh injections in the authors' cluster"
datasets: "A public (GAIA-DataSet repo), B and C collected by the authors (not stated as released)"
dataset_open: "A yes (github.com/CloudWise-OpenSource/GAIA-DataSet); B and C not stated"
code_open: "no (no code link in the paper)"
baselines_compared: "MicroRCA, LogCluster, DiagFusion, TVDiag, Medicine, DeepHunt (supervised variant)"
metrics: "HR@1, HR@3, Avg@3 (localization); weighted precision, recall, F1 (failure type)"
headline_result: "HR@1 0.875 / 0.923 / 0.918 and Avg@3 0.920 / 0.938 / 0.938 on datasets A / B / C (Table I, p.8)"
evidence_quality: "2"
relevance_to_us: "3"
overlap_with_us: "partial (group-level propagation modelling, but supervised, no forecasting)"
threat_level_for_novelty: "low"
---

# Root Cause Analysis for Microservice Systems via Cascaded Conditional Learning with Hypergraphs (CCLH)

> Reading notes written from the **full text** (`litdb/texts/shuaiyuxie...root.txt`). Page numbers are PDF pages (11 pages).
> Not inspected: Figs 1-6 (Figs 1 and 5 and 6 contain plotted data).

## 1. One-paragraph summary
CCLH is a supervised multimodal RCA model. It extracts GRU features from metrics, traces and Drain log templates per instance, fuses them by attention, builds a hypergraph with three kinds of hyperedges (call, deployment/co-location, load-balancing siblings), aggregates with a hyperedge-type-aware hypergraph attention network, scores each instance as culprit, and then classifies the failure type of the top instance. A "task trigger" delays training of the failure-type head until localization reaches a threshold. On one public dataset (GAIA, 10 instances) and two benchmark systems with injected faults it reports higher localization hit ratios than DiagFusion, TVDiag and a supervised DeepHunt variant.

## 2. Problem and motivation
- Problem: RCA as root cause localization (RCL) followed by failure type identification (FTI) in microservice systems (p.1).
- Motivation: GitHub took about one and a half hours to resolve a failure of its codespace service affecting millions (p.1, cites a GitHub availability report [3]); failure propagation is group-like because of co-location and load balancing (pp.1-3). The three small experiments in Sec. III (Fig 1) on Online Boutique show effects of call, deployment and load-balancing relations; these are illustrations on one demo system.
- Real? Anecdote plus demonstrations on a demo app; no incident statistics.

## 3. Method
- Preprocessing (p.4): sliding window 30 s; metrics averaged, traces by mean duration and status-code counts, logs by Drain template counts per snapshot.
- Feature extraction (Eq.1-7): GRUs per modality (3 layers, hidden 256), attention fusion over modalities.
- Hypergraph (pp.5-6): call hyperedges link an instance with its callers; deployment hyperedges link co-located instances on a host; load-balancing hyperedges link sibling instances of a microservice. UniGAT-HE (Eq.8-11): hyperedge embedding = mean of members; per-hyperedge-type attention; 2 layers, hidden 256.
- Cascaded conditional learning (Eq.12-13): scorer MLP outputs a scalar per instance; softmax cross-entropy across instances to pick the culprit; the FTI classifier is trained only after HR@1 passes a trigger theta (0.4, 0.6, 0.7 for A, B, C chosen from Fig 5); inference runs RCL then FTI on the predicted instance.
- Hyper-parameters: window 30 s, GRU 3 layers, 256 hidden; 60/40 train/test split; early stopping on training loss.
- Assumptions: labelled failure cases with culprit instance and failure type; deployment configuration known; the failure period is given (data are segmented from the failure start).

## 4. Data and setup
- Dataset A: GAIA, 1,099 labelled cases over two weeks from an online system with 10 instances and 5 failure types (p.7).
- Datasets B and C: Online Boutique and Sock Shop deployed in the authors' cluster; Chaos Mesh injection of CPU, memory, network (loss, delay, corruption) and pod/container faults; each instance injected and repeated five times: 489 and 700 failure cases (p.7).
- Split: 60% train, 40% test per dataset (p.7). The split is not stated to be by time or by instance. Because each (instance, fault type) is repeated five times, random case-level splits would place near-duplicate cases in train and test (a leakage risk the paper does not discuss).
- RQ4 (p.9): re-split so that, per failure type, 60% of culprit components are in training and 40% unseen at test time.
- Hardware: Windows laptop, RTX 2070, 16 GB RAM (p.7).

## 5. Results (copied; Tables I-III)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| HR@1 (A / B / C) | 0.875 / 0.923 / 0.918 | 0.811 / 0.834 / 0.832 | TVDiag | Table I, p.8 |
| HR@3 (A / B / C) | 0.950 / 0.954 / 0.950 | 0.939 / 0.925 / 0.904 | TVDiag | Table I |
| Avg@3 (A / B / C) | 0.920 / 0.938 / 0.938 | 0.884 / 0.884 / 0.877 | TVDiag | Table I |
| F1 for failure type (A / B / C) | 0.941 / 0.768 / 0.772 | 0.977 / 0.577 / 0.505 | TVDiag | Table I |
| DeepHunt (supervised variant) HR@1 | 0.308 / 0.436 / 0.441 | n/a | n/a | Table I |
| MicroRCA HR@1 | 0.207 / 0.061 / 0.050 | n/a | n/a | Table I |
| Ablation Avg@3 and F1 (A / B / C) | default Avg@3 0.920 / 0.938 / 0.938; F1 0.941 / 0.768 / 0.772; without hypergraph (HG) Avg@3 0.838 / 0.800 / 0.863; F1 0.860 / 0.449 / 0.555 | n/a | n/a | Table II, p.8 |
| Time (dataset A) | training 168.204 s; inference 0.434 s per case | DiagFusion 19.687 s, 0.013 s | n/a | Table III, p.9 |

- On dataset A, TVDiag's F1 (0.977) exceeds CCLH's (0.941); the text says CCLH "performs comparably" there (p.7).
- Statistical testing: none; single run per configuration; no variance.
- RQ4 results are in Fig 6 (plot), described as stable for CCLH and DeepHunt and declining for DiagFusion and TVDiag; numbers not available to me.

## 6. Limitations
- Stated: platform events not used; no joint metric for the two tasks; task trigger sensitivity and the need for manual theta (pp.9-10); datasets may not represent real systems.
- **My critique:**
  1. Supervised, and the authors say real settings "often operate under few-shot or even zero-shot scenario", yet no label-limited experiment is given; the suggestion is to collect labels via chaos engineering.
  2. Likely leakage by random case-level 60/40 splits with five repeated injections per instance; RQ4 partially addresses unseen culprit components but only as a plot.
  3. Baselines were re-run by the authors; the DeepHunt "supervised variant" gets HR@1 0.308 to 0.441, far lower than DeepHunt's own published A@1 values (0.78 to 0.80 on its datasets, batch 1); the comparison therefore reflects reimplementation and setting differences, not DeepHunt's published performance.
  4. Datasets B and C are not released (not stated), no code link, so results cannot be checked.
  5. Dataset A has only 10 instances (chance HR@1 about 0.1); the larger gains are on small simulated systems.
  6. No statistical tests or repetitions; ablation differences of about 0.01 to 0.02 are within plausible noise.
  7. The "group influence" insight is demonstrated by three single-run illustrations on Online Boutique, not by a systematic study.
  8. Preprint, venue unknown.
- Not discussed: label cost, concurrent failures, forecasting.

## 7. Reproducibility
- Code: none stated. Dataset A: github.com/CloudWise-OpenSource/GAIA-DataSet (cited p.7; not opened). Datasets B and C: self-collected; no release stated.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | supervised (culprit and failure-type labels) | label-free | Ours lighter |
| Live / streaming | per-failure, under 1 s | incremental windows | Comparable |
| Telemetry used | metrics, traces, logs, deployment | traces (+ optional metrics, SSH) | Theirs |
| Propagation modelling | hypergraph with call, co-location, load-balancing hyperedges | edge probabilities (call graph only) | Theirs is richer; co-location and sibling effects are ideas we lack |
| Forecasts future failures | no | claimed | n/a |
| Explanation | none beyond scores | templates | Ours |
| Evaluation rigor | three datasets, 6 baselines, no stats, possible leakage | synthetic only | Theirs |
| Open / reproducible | partly (dataset A) | yes | Ours (code) |

- **What they have that we do not:** group-level propagation relations (co-location and load-balancing siblings) and failure-type identification.
- **What we have that they do not:** label-free operation, open code.
- **Could a reviewer say "this already exists"?** For "propagation beyond call edges (shared host, siblings)": yes in a supervised setting. It suggests our call-graph-only propagation misses shared-infrastructure effects (a limitation already noted in REVIEW_REPORT).
- **Position:** "Hypergraph-based RCA models group relations (co-location, load balancing) with supervision (Xie et al. 2025); our edge model uses call relations only."
- **Must we run it as a baseline?** No (no code, supervised).

## 9. Does this paper change what problem we should solve?
- It supports adding non-call propagation channels (co-location, siblings) to our model as a planned extension and as a stated limitation; the evidence is demo-system experiments.
- No forecasting content.

## 10. Citation-ready facts (each with page)
- CCLH builds hyperedges for call, co-location (deployment) and sibling (load-balancing) relations among instances (pp.5-6).
- It trains the failure-type classifier only after the localization head reaches a threshold (pp.6-7).
- On three datasets it reports HR@1 of 0.875, 0.923 and 0.918 (Table I, p.8).
- Single-run demonstrations on Online Boutique show latency effects from call, co-location and sibling failure relations (Fig 1, p.3).
- The paper cites OpenRCA (ICLR 2025) as an LLM benchmark finding suboptimal performance and high latency (p.10).

## 11. Open questions / things to verify
- Whether datasets B and C or code are released; Figs 1, 5, 6.
- OpenRCA existence is corroborated by this citation (ICLR 2025); check the title before citing (REVIEW_REPORT Appendix B).
