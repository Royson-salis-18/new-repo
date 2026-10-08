---
key: hardt2023petshop
title: "The PetShop Dataset: Finding Causes of Performance Issues across Microservices"
authors: "Michaela Hardt; William R. Orchard; Patrick Blöbaum; Elke Kirschbaum; Shiva Prasad Kasiviswanathan"
year: 2023
venue: "Proceedings of Machine Learning Research vol. 236, 3rd Conference on Causal Learning and Reasoning (CLeaR 2024), pp.1-21; arXiv 2311.04806 version read"
publisher: "PMLR / arXiv"
doc_type: proceedings-article
doi: "10.48550/arxiv.2311.04806"
issn: ""
scopus_indexing: "unverified: PMLR volume not checked; the arXiv copy is a preprint"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (CLeaR 2024, printed header)"
cited_by_crossref: ""
n_references: "about 45"
license: ""
batch: "11"
read_status: reviewed                  # full text read; Figs 5-6 and Appendix A not inspected
pages: 22
text_chars: 62128
metadata_source: arxiv
task: "dataset for RCA benchmarking (service-level, with causal graph supplied)"
supervision: "n/a (benchmark); evaluated methods are unsupervised"
online_or_streaming: "no"
telemetry: "latency, requests and availability metrics in 5-minute intervals; service map from AWS X-Ray"
propagation_modeling: "service map given; methods use it (traversal, CIRCA, counterfactual attribution)"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "AWS PetAdoptions demo application on AWS (microservices + managed services)"
datasets: "68 injected issues at 5 nodes across three traffic scenarios (low, high, temporal); normal period plus issues; each issue repeated twice; train/test split by originating microservice"
dataset_open: "yes: https://github.com/amazon-science/petshop-root-cause-analysis (stated; not checked)"
code_open: "yes (evaluation harness and some methods; stated)"
baselines_compared: "traversal, CIRCA, counterfactual attribution, epsilon-diagnosis, RCD, ranked correlation"
metrics: "top-1 and top-3 recall (target node PetSite)"
headline_result: "ranked-correlation baseline top-3 0.57-0.92 and the best top-1 recall without graph; methods that learn the graph or SCM do poorly on small samples (Table 3 p.12, Table 8 p.22)"
evidence_quality: "3"
relevance_to_us: "4"
overlap_with_us: "medium (public benchmark with a given service graph; strong correlation baseline)"
threat_level_for_novelty: "low"
---

# PetShop dataset (Hardt et al., CLeaR 2024)

> Notes from the **full text** (22 pages). Page numbers are PDF pages. Figures and Appendix A not inspected.

## 1. Summary
A benchmark of 68 performance issues injected into five nodes of the AWS PetAdoptions microservice demo, with metrics at 5-minute resolution, a service map from X-Ray, and one unique ground-truth root cause per issue. Six RCA methods spanning correlation, causal-hypothesis testing and counterfactual attribution are evaluated by top-1 and top-3 recall at the PetSite node.

## 2. Problem and motivation
- No standard dataset exists, so groups build their own (p.1). Argued by citation.

## 3. Method (dataset construction, pp.5-9)
- Injected issues: latency delays, request overloads, memory leaks, CPU hogs, misconfigurations, availability drops; effect strength tuned to be pronounced (p.12). Traffic generator provides low, high and temporal scenarios.

## 4. Data and experimental setup
- 68 issues; per Table 2: latency 14 + 14 + 8 = 36, availability 12 + 12 + 8 = 32 (p.10). Issues repeated twice (Appendix Table 4). Train/test split "evenly at random by the originating microservice" (p.5).
- Each cell in the results tables aggregates only 8 to 14 issues.

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Top-3 recall, low-traffic latency | traversal 0.57, CIRCA 0.86, counterfactual 0.71 | correlation 0.57 | graph-free | Table 3 p.12 |
| Top-3, high-traffic availability | CIRCA 0.00, counterfactual 0.00, traversal 1.00 | correlation 0.92 | graph-free | Table 3 |
| Top-1, high-traffic availability | traversal 0.33, CIRCA 0.00 | correlation 0.83 | graph-free | Table 8 p.22 |
| Epsilon-Diagnosis top-3 | 0.00 to 0.33 | n/a | n/a | Table 3 |
| Specificity on normal data | all methods fabricate root causes | n/a | n/a | p.12 |

## 6. Limitations
- Stated: artificial traffic, no feedback loops, single root cause, injected faults not representative, tuned for strong effects, methods not tuned, not all RCA methods included (pp.12-13).
- **My critique:**
  1. Very small samples (68 issues, cells of 8-14); recalls such as 0.00 or 1.00 are coarse and have wide intervals; no intervals reported.
  2. The target node (PetSite) is a leaf in the causal graph, so common-cause confounding does not arise; the authors admit the correlation baseline benefits from this (p.12).
  3. Methods "not tuned or massaged" (p.13) and run with default Salesforce implementations; the conclusion "causal methods fail without a graph" is therefore about untuned defaults on 5-minute data.
  4. Availability issues had low variability in normal data; CIRCA and counterfactual attribution scored 0.00 on high-traffic availability, which may reflect model fitting issues rather than a method property (the paper offers that explanation).
- Not discussed: statistical significance; multiple roots; code-level faults.

## 7. Reproducibility
- Dataset and evaluation code stated at github.com/amazon-science/petshop-root-cause-analysis (not checked, not downloaded).

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | n/a (benchmark) | none | n/a |
| Live / streaming | no | incremental | ours |
| Telemetry used | metrics at 5 min, service map | traces (+ metrics) | different |
| Propagation modelling | provided graph | learned weights | different |
| Forecasting | no | claimed | n/a |
| Explanation | none | templates | ours |
| Evaluation rigor | 68 issues, no CIs | synthetic | theirs |
| Open / reproducible | yes | yes | tie |

- **What they have that we do not:** a public, labelled benchmark with a given service graph and a ready evaluation harness.
- **What we have that they do not:** trace-based edge learning and risk output.
- **Could a reviewer say "this already exists"?** Not applicable (dataset).
- **Position:** candidate public benchmark for the propagation question (graph given); its main message supports using a correlation/NSigma baseline.
- **Must we run it as a baseline?** Not as a method; use its data and ranked-correlation baseline (download needs permission; not done).

## 9. Does this paper change what problem we should solve?
- It supports the evaluation lesson from Pham et al. and Fang et al.: a simple correlation or anomaly-score ranking is a strong baseline on small, leaf-targeted benchmarks.

## 10. Citation-ready facts (each with page)
- "On the 68-issue PetShop benchmark none of the graph-free methods outperformed ranked correlation (pp.11-12)".
- "All evaluated methods produced root causes on normal data (p.12)".

## 11. Open questions / things to verify
- Dataset licence and repo contents; whether metrics at 5 minutes suit our trace windows.
