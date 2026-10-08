---
key: zeyanlinengwenzhaoshenglinzhangyongqiansunpengfeichenxidaowenminghuamadanpei2022constructing
title: "Constructing Large-Scale Real-World Benchmark Datasets for AIOps"
authors: "Zeyan Li; Nengwen Zhao; Shenglin Zhang; Yongqian Sun; Pengfei Chen; Xidao Wen; Minghua Ma; Dan Pei"
year: 2022
venue: "arXiv 2208.03938v1 (cs.SE, 8 Aug 2022); page header reads ESEC/FSE 2022, Singapore (track not stated; published version unverified)"
publisher: "arXiv"
doc_type: preprint
doi: "10.48550/arxiv.2208.03938"
issn: ""
scopus_indexing: "arXiv preprint: not Scopus-indexed; published FSE version not checked"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "preprint (header suggests FSE 2022; unverified)"
cited_by_crossref: ""
n_references: "about 51"
license: ""
batch: "12"
read_status: reviewed                  # full text read to the conclusion; references not read; figures not inspected
pages: 7
text_chars: 42062
metadata_source: arxiv
task: "dataset description: KPI anomaly detection, multi-dimensional root cause localization, failure discovery and diagnosis (microservice-like system with traces, KPIs, metrics)"
supervision: "n/a (datasets and competitions)"
online_or_streaming: "competition required online detection and diagnosis"
telemetry: "KPIs, traces and 100+ metrics (dataset C); structured logs aggregates (dataset B)"
propagation_modeling: "none; dataset C system has call and deployment dependencies (OSB, Service, DB, Docker, OS)"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "dataset C: one production-derived distributed system (sysA at China Mobile Zhejiang); 169 injected failures over one month, 7 failure types"
datasets: "A: 27 labelled KPIs; B: 400 synthetic failures on Suning order data; C: 169 injected failures with traces, KPIs and metrics"
dataset_open: "yes (links in the paper to the AIOps challenge datasets; not checked)"
code_open: "evaluation scripts mentioned (iopsai/iops); not checked"
baselines_compared: "none (competition leaderboards only)"
metrics: "competition scores (F1 0.8216 for KPI detection, F1 0.9593 for dataset B, score 755 of a maximum for dataset C)"
headline_result: "dataset C: 169 injected failures, 7 injection types (Table 6 p.5); competition best score 755 given 129 failures"
evidence_quality: "2"
relevance_to_us: "3"
overlap_with_us: "dataset provider for trace-based RCA (dataset C)"
threat_level_for_novelty: "low"
---

# Constructing Large-Scale Real-World Benchmark Datasets for AIOps (Li et al., 2022)

> Notes from the **full text** (7 pages, to the conclusion). Page numbers are PDF pages. Figures not inspected.

## 1. Summary
Describes three public AIOps datasets released with yearly competitions (2018-2020): 27 labelled KPIs, 400 synthetic multi-dimensional failures on e-commerce order data, and 169 injected failures in a production-derived distributed system with traces, KPIs and metrics for failure discovery and diagnosis.

## 2. Problem and motivation
- AIOps methods are mostly evaluated on private data, so generality is unknown (pp.1-2). Argued by citation.

## 3. Method (dataset construction)
- Dataset A: 27 KPIs from five companies, engineer labels, 2 to 7 months, anomaly ratios 0.01% to 4.37% (Table 1 p.2).
- Dataset B: 400 failures synthesized by modifying measure values with the generalized ripple effect and noise; 1-4 root cause attribute combinations (p.3-4).
- Dataset C: spans, KPIs, 4 categories of metrics (Docker, Linux, Oracle, Redis) from sysA; 7 injection types (database close, session limit, container CPU stress, container/node network delay and loss) with stress-ng and tc (Table 6 p.5).

## 4. Data and experimental setup
- Competition setting for C: participants detect and diagnose failures online, at most two root-cause metrics per failure, valid if precision at least 0.5; points by rank; best score 755 for 129 failures (p.5).

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| KPI detection best F1 (2018 competition) | 0.8216 | n/a | n/a | p.3 |
| Multi-dimensional root cause best F1 (2019) | 0.9593 | n/a | n/a | p.4 |
| Dataset C size | 169 injected failures, one month, 7 types | n/a | n/a | p.5 |
| Participation | 125 / 141 / 141 teams in 2018 / 2019 / 2020 | n/a | n/a | p.2 |

## 6. Limitations
- Stated: failures are injected because real failures with ground truth are hard to collect (pp.4-5). No other limitation section.
- **My critique:**
  1. Dataset C is injected failures from seven types on one system, so it shares the weaknesses Fang et al. found in public benchmarks (few types, limited depth); its architecture (OSB, services, databases, containers, servers with call and deployment edges) matches the system shown in DéjàVu's dataset A.
  2. Dataset B is synthetic (modified measure values), not real failures; the title's "real-world" applies to the underlying data, not the faults.
  3. No baselines or per-method results; competition scores only.
  4. Final published version unverified; the arXiv text has references not read.
- Not discussed: label quality, failure-time definitions, and potential overlap between competition training and test failures.

## 7. Reproducibility
- Datasets available through the AIOps challenge links (not checked); real data cannot be re-collected.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | n/a | none | n/a |
| Live / streaming | competition online | incremental | tie |
| Telemetry used | traces, KPIs, metrics | traces (+ metrics) | theirs (dataset) |
| Propagation modelling | none | edge probabilities | ours |
| Forecasting | no | claimed | n/a |
| Explanation | none | templates | ours |
| Evaluation rigor | competition | synthetic | theirs |
| Open / reproducible | yes (stated) | yes | tie |

- **What they have that we do not:** a public dataset with traces and metrics and ground-truth failure times and root causes.
- **What we have that they do not:** propagation scoring and risk output.
- **Could a reviewer say "this already exists"?** Not applicable (datasets).
- **Position:** cite as the source of the 2020 AIOps challenge dataset (sysA with call and deployment dependencies); candidate dataset for trace-based tests.
- **Must we run it as a baseline?** No; consider as a test set (download needs permission; not done).

## 9. Does this paper change what problem we should solve?
- No; it documents data availability.

## 10. Citation-ready facts (each with page)
- "The 2020 AIOps challenge dataset contains 169 injected failures with traces, KPIs and metrics from a distributed system with call and deployment dependencies (pp.4-5)."

## 11. Open questions / things to verify
- Published version and track; dataset licence; mapping to the datasets used in other papers (e.g. 'AIOps-2021' in Fang et al.).
