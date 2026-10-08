---
key: causalrca
title: "CausalRCA: Causal inference based precise fine-grained root cause localization for microservice applications"
authors: "Ruyue Xin, Peng Chen, Zhiming Zhao"
year: 2023
venue: "The Journal of Systems & Software, vol. 203, article 111724"
publisher: "Elsevier"
doc_type: journal-article
doi: "10.1016/j.jss.2023.111724"
issn: "0164-1212 (Crossref confirms)"
scopus_indexing: "unverified: Scopus preview check for 0164-1212 not yet done"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (journal; received 15 July 2022, accepted 19 April 2023, as printed)"
cited_by_crossref: "101 (Crossref, 2026-10-08)"
n_references: "65 (Crossref)"
license: "CC BY 4.0 (printed)"
batch: "7"
read_status: reviewed                  # pages 1-12 read as rendered images (pypdfium2); page 13 (references) not read
pages: 13
text_chars: 0
metadata_source: pdf-visual+crossref
task: "fine-grained root cause metric localization (service plus metric)"
supervision: "label-free (trained per run on collected metrics; ground truth only for scoring)"
online_or_streaming: "no live evaluation; data collected for 5 minutes after each injection and processed offline (p.11)"
telemetry: "metrics (service latency; CPU, memory, disk, network)"
propagation_modeling: "learned weighted DAG (DAG-GNN VAE) plus PageRank"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "Sock-Shop only: 13 services on Kubernetes, 1 master and 3 workers (p.6)"
datasets: "own injected faults: CPU hog, memory leak, network delay, 5 minutes each, 10-minute cool-down; Prometheus every 5 s (pp.6-7); number of injections per type not stated"
dataset_open: "yes (data_collected folder in the repo)"
code_open: "https://github.com/AXinx/CausalRCA_code (no license; last push 2023-05-02; 41 stars; notebooks, train scripts, data_collected; checked 2026-10-08)"
baselines_compared: "PC, GES, LiNGAM, each with PageRank (default causal-learn settings, p.7)"
metrics: "AC@1, AC@3, Avg@5; ANOVA and t-tests on Avg@5"
headline_result: "service task average Avg@5 0.5815 vs LiNGAM 0.5143 (Table 3 p.8); metric task in faulty service average Avg@5 0.6681 vs 0.5738 (+9.43%), average AC@3 0.719 (Table 4 p.9); all-metrics task average rank about 13 (Fig 10 p.10)"
evidence_quality: "2"
relevance_to_us: "3"
overlap_with_us: "partial (label-free causal-graph metric RCA)"
threat_level_for_novelty: "low-medium"
---

# CausalRCA (Xin, Chen, Zhao, JSS 2023)

> Notes from pages 1-12 read as rendered images (scanned PDF, no text layer). Page numbers are PDF pages. Page 13 (references) not read; Figs 6, 9, 10, 11 seen only as plots.

## 1. Summary
Learns a weighted causal graph over monitoring metrics with a DAG-GNN variational autoencoder (Eqs 1-7), then runs PageRank on the reversed graph (restart 0.85, Eqs 8-9) to rank metrics. Tested on a Sock-Shop deployment with three injected fault types in three experiments: service localization, metric localization in the faulty service, and metric localization across all metrics.

## 2. Problem and motivation (pp.1-3)
Fine-grained (service plus metric) localization is more actionable than naming a service. Argued by citation; Table 1 (p.4) is a literature classification. No incident data.

## 3. Method (pp.4-6)
DAG-GNN with MLP encoder and decoder, augmented Lagrangian; eta 10, gamma 0.25, 1000 epochs, lr 1e-3, Adam; 10 runs averaged (p.7). Root cause by PageRank. No forecasting.

## 4. Data and setup (pp.6-7)
Sock-Shop with 13 services, Prometheus every 5 s; service latency plus CPU, memory, disk read/write, network receive/transmit (Table 2). Faults injected with stress tools for 5 minutes with a 10-minute cool-down. Number of injections per fault not stated. One system, one injection style.

## 5. Results (copied)
| Task | Metric | CausalRCA | Best baseline | Page |
|---|---|---|---|---|
| Faulty service, all anomalies | average Avg@5 | 0.5815 | LiNGAM 0.5143 (+6.72%) | Table 3 p.8 |
| Service, CPU hog | AC@1 / AC@3 / Avg@5 | 0.1873 / 0.7175 / 0.6244 | LiNGAM 0.1429 / 0.7143 / 0.5714 | Table 3 |
| Service, network delay | AC@3 | 0.3857 | PC 0.5714 (PC wins) | Table 3 |
| Metric in faulty service | average Avg@5 | 0.6681 | LiNGAM 0.5738 (+9.43%) | Table 4 p.9 |
| Metric, CPU hog | AC@1 | 0.2286 | PC 0.4286 (PC wins) | Table 4 |
| Metric, memory leak | AC@1 | 0.2714 | LiNGAM 0.4286 (LiNGAM wins) | Table 4 |
| All metrics, service unknown | average rank | about 13 | LiNGAM worse | Fig 10 p.10 |
- Statistics: ANOVA p 0.0003 (service) and 0.0013 (metric); t-tests in heatmaps (Figs 4, 7); LiNGAM vs CausalRCA p 0.0335 in the all-metrics task (p.10). The unit of replication is not stated (10 runs, not independent injections).

## 6. Limitations
- Stated: single testbed, fixed-length anomalies, time lag ignored, efficiency untested, all-metrics task hard (pp.10-11).
- **My critique:**
  1. The headline AC@3 0.719 is an average over three faults; CausalRCA is not best on AC@1 in several cells (PC on CPU hog metrics, LiNGAM on memory leak metrics).
  2. Abstract says "Avg@5 improved by 9.43%" and the intro says AC@5; Table 4 shows it is the relative increase in average Avg@5.
  3. CausalRCA's hyperparameters were tuned on the same data (Figs 5, 8); baselines used defaults.
  4. One Sock-Shop deployment and three stress faults; the injection count is not given, so the p-values rest on 10 repeated runs.
  5. In the all-metrics task the average rank is about 13 (Fig 10) while the discussion says "out of ten" (p.11).
  6. No simple strong baselines (BARO/NSigma-style) that Pham et al. later showed to be competitive.
  7. "Real-time" is claimed; analysis is offline on 5 minutes of collected data (p.11).
- Not discussed: failure-time misspecification, shared-infrastructure propagation.

## 7. Reproducibility
Code and data at https://github.com/AXinx/CausalRCA_code (no license; notebooks, train scripts, data_collected; checked via the GitHub API 2026-10-08). Not run.

## 8. Comparison with OUR work
| Dimension | This paper | Ours | Stronger |
|---|---|---|---|
| Labels | none | none | tie |
| Streaming | offline | incremental windows | ours (claimed) |
| Telemetry | metrics | traces (+ metrics) | different |
| Propagation | learned weighted DAG | edge probabilities | theirs richer, evidence modest |
| Forecasting | no | claimed | n/a |
| Rigor | one system, 10 runs | synthetic only | neither strong |
| Open | code + data | yes | tie |

- Could a reviewer say "this exists"? For "label-free causal-graph metric RCA": yes. Not for traces plus risk scoring.
- Must we run it as a baseline? Optional.

## 9. Does it change our problem?
No. It confirms that causal-graph metric RCA exists and that its gain over simple structure learners is modest (6.72% and 9.43% relative on Avg@5).

## 10. Citation-ready facts
- "CausalRCA learns a weighted causal graph over metrics with a DAG-GNN VAE and ranks metrics with PageRank" (pp.4-6).
- "On a 13-service Sock-Shop with three injected faults, average Avg@5 for metric localization in the faulty service was 0.6681 vs 0.5738 for LiNGAM plus PageRank" (Table 4 p.9; authors' own tuning).

## 11. Open questions
Number of injections; the all-metrics rank scale; page 13; Scopus status of 0164-1212.
