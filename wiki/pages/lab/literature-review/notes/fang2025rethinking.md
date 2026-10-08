---
key: fang2025rethinking
title: "Rethinking the Evaluation of Microservice RCA with a Fault Propagation-Aware Benchmark"
authors: "Aoyang Fang; Songhan Zhang; Yifan Yang; Haotong Wu; Junjielong Xu; Xuyang Wang; Rui Wang; Manyi Wang; Qisheng Lu; Pinjia He"
year: 2025
venue: "arXiv 2510.04711v2 (cs.SE, 23 Dec 2025); ACM template with placeholder DOI and 'Conference acronym XX'; literature matrix lists DOI 10.1145/3797100 (not verified here)"
publisher: "arXiv (ACM version listed in matrix)"
doc_type: preprint
doi: "10.48550/arxiv.2510.04711"
issn: ""
scopus_indexing: "arXiv preprint: not Scopus-indexed; the ACM journal version (if it exists) not checked"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "preprint (peer-review status of the ACM version unverified)"
cited_by_crossref: ""
n_references: "about 52"
license: ""
batch: "10"
read_status: reviewed                  # full text read to references (page 20); Figs 6-11 seen as plot text only
pages: 20
text_chars: 99980
metadata_source: arxiv
task: "benchmark and re-evaluation of RCA methods (service-level localization)"
supervision: "mixed (11 evaluated methods: label-free and supervised)"
online_or_streaming: "no"
telemetry: "metrics, logs, traces (OpenTelemetry), L4/L7 network telemetry"
propagation_modeling: "none proposed; benchmark claims longer call chains (max depth 7) and symptom drift"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "Train-Ticket (50 services) on Kubernetes; plus re-analysis of 11 existing datasets (Nezha, Eadro, RCAEval RE2/RE3, AIOps-2021, GAIA)"
datasets: "new: 1,430 validated failure cases from 9,152 injections, 31 fault types tried, 25 retained; 188.1 h; 154.7M log lines; 11.2M traces; average 16.47 QPS"
dataset_open: "promised ('we promise that we will release', p.19); release not verified"
code_open: "promised, not verified"
baselines_compared: "11 SOTA: MicroRank, MicroRCA, MicroHECL, MicroDig, DiagFusion, Eadro, Art, Shapleyiq, Nezha, CausalRCA, Baro; plus SimpleRCA (rule-based alert counter)"
metrics: "Top@K, Avg@K, MRR, time"
headline_result: "mean Top@1 of 11 methods 0.21, best MicroRCA 0.37 (Table 5 p.14); SimpleRCA Top@1 0.28 but Top@5 0.80, higher than every method; on 10 existing benchmarks SimpleRCA matches or beats SOTA (Table 2 p.6)"
evidence_quality: "3"
relevance_to_us: "5"
overlap_with_us: "high for evaluation methodology (datasets, baselines, failure patterns)"
threat_level_for_novelty: "low (benchmark paper); high for our evaluation design"
---

# Rethinking the Evaluation of Microservice RCA (Fang et al., 2025)

> Notes from the **full text** (`litdb/texts/aoyang...rethinking.txt`). Page numbers are PDF pages. Many numbers come from tables in the text; bar/radar plots (Figs 6-9) were not inspected.

## 1. Summary
Shows that a rule-based "alert counter" (SimpleRCA) matches or beats state-of-the-art RCA models on public benchmarks, diagnoses why (faults are overly localized, shallow call chains, incomplete telemetry), builds a new Train-Ticket benchmark of 1,430 validated failures with deeper chains and hierarchical labels, and re-evaluates 11 methods on it. Methods average Top@1 0.21; the best reaches 0.37. Failures are grouped into scalability, observability blind spots and modelling bottlenecks.

## 2. Problem and motivation
- Reported RCA progress may be an artifact of simple benchmarks (pp.1-2). Evidence is the paper's own SimpleRCA study (Table 2) and dataset statistics (Tables 1, 3).

## 3. Method (benchmark pipeline, pp.8-11)
- Train-Ticket with enhanced observability, dynamic state-machine workload, ChaosMesh faults from a 31-type space (resource, network, HTTP, JVM code, DNS, time), stratified random sampling, impact-driven validation (Z-test on success rate and latency thresholds), hierarchical labels (service, pod, container, function). 4 minutes normal + 4 minutes fault, redeploy after each injection (p.12).

## 4. Data and experimental setup
- 9,152 injections; 84.4% produced no user-perceivable anomaly and were discarded (p.13); 25 of 31 fault types survive; 1,430 cases; 262 hardest cases (at least 10 of 12 methods fail) manually coded (p.16).
- Trained methods (Art, DiagFusion, Eadro) split 80/20 by fault type (p.12) and are evaluated on the test set; the others on the full dataset (Table 5).
- Baseline hyperparameters tuned "best effort" on the new data (pp.11-12).

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Existing benchmarks, e.g. RE3-SS Top@1 | SimpleRCA 0.83 | BARO 0.00 | BARO | Table 2 p.6 |
| Nezha-TT Top@1 | SimpleRCA 0.93 | Nezha 0.87 | Nezha | Table 2 |
| Eadro-TT Top@1 | SimpleRCA 0.81 | Eadro 0.99 | Eadro (train/test overlap) | Table 2 |
| 11 existing datasets: incomplete observability | 733 of 737 cases (0.99) | n/a | n/a | Table 3 p.7 |
| Type I (only injected service symptomatic) | 0.68 of all cases | n/a | n/a | Table 3 |
| New benchmark, Top@1 / Top@3 / Top@5 | MicroRCA 0.37 / 0.50 / 0.64 | Baro 0.36 / 0.50 / 0.58 | n/a | Table 5 p.14 |
| New benchmark, SimpleRCA | 0.28 / 0.60 / 0.80 | MicroDig Top@3 0.61 | MicroDig | Table 5 |
| Nezha Top@1 on new data | 0.04 | 0.87-0.93 on its original data | n/a | Table 5 vs Table 2 |
| CausalRCA time per case | 927.11 s | Baro 0.99 s | Baro | Table 5 |
| Failure-mode shares among 262 hard cases | scalability 39.8%, modelling 47.4%, observability sub-types 5.8%, 4.2%, 2.9% | n/a | n/a | Fig 10 p.17 |

## 6. Limitations
- Stated: single system (Train-Ticket), user-facing SLI oracle excludes gray failures, proxy complexity metrics (pp.17-18).
- **My critique:**
  1. On the new benchmark SimpleRCA has the highest Top@5 (0.80) of all 12 methods and Top@3 0.60 (MicroDig 0.61); the text frames its Top@1 0.28 as evidence that simple rules fail, but a Top@5 comparison shows the simple rule still matches or beats every SOTA method. The conclusion "demand more sophisticated approaches" (p.14) is not supported by that table.
  2. Several methods are strongly affected by tuning and re-implementation: Nezha Top@1 0.04 vs 0.87-0.93 on its own datasets; MicroHECL has identical Top@1, Top@3, Top@5 (0.34), which suggests a single-answer output; re-engineered implementations are the authors'.
  3. Two evaluation sets (full dataset vs 20% test set for trained methods) are put in one table, so trained and untrained methods are not on the same cases.
  4. Fault types: abstract says "25 fault types across 6 categories"; the text builds a space of 31 types across seven categories and keeps 25 (pp.9, 13); the category count after filtering is not given.
  5. 84.4% of injections were silent and filtered by an automatic SLI check; this selects failures with user-visible impact, which favours symptom-based methods (and excludes gray failures, as noted).
  6. Release of the benchmark and code is promised, not shown (p.19); I did not verify availability.
  7. The paper is a preprint with template placeholders (DOI, conference, 2018 dates).
- Not discussed: confidence intervals or repeated runs for the Top@K numbers; label noise in hierarchical labels.

## 7. Reproducibility
- Promised release of benchmark, generator and implementations; not verified. I did not download anything.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | n/a (benchmark) | none | n/a |
| Live / streaming | no | incremental | ours |
| Telemetry used | all three | traces (+ metrics) | theirs broader |
| Propagation modelling | studies it (symptom drift, depth) | edge probabilities | motivates ours |
| Forecasts future failures | no | claimed | n/a |
| Explanation | none | templates | ours |
| Evaluation rigor | large, but one system | synthetic | theirs |
| Open / reproducible | promised | yes | unverified |

- **What they have that we do not:** a large, impact-validated, deeper-chain benchmark; a SimpleRCA sanity baseline; failure-mode taxonomy.
- **What we have that they do not:** an actual propagation-aware scoring method and a risk output.
- **Could a reviewer say "this already exists"?** Not our method; but a reviewer will expect us to include a SimpleRCA-style baseline and to avoid easy benchmarks.
- **Position:** the key methodological reference for our evaluation; use it to justify baselines (SimpleRCA, BARO, MicroRCA) and a deeper-chain benchmark.
- **Must we run it as a baseline?** Not as a baseline; its SimpleRCA idea (count of alerts per service) must be implemented as one.

## 9. Does this paper change what problem we should solve?
- Yes, for evaluation: "propagation-aware" claims are only meaningful on benchmarks where the root cause is not the loudest service; on current public data a rule matching Top@1 requires no propagation modelling. This is the strongest external support for our "negative control" evaluation.

## 10. Citation-ready facts (each with page)
- "On existing public benchmarks a rule-based alert counter matched or beat state-of-the-art RCA methods (Table 2 p.6); 99% of the cases lack at least one needed telemetry type and 68% have symptoms only in the injected service (Table 3 p.7)."
- "On the authors' new benchmark the 11 evaluated methods average Top@1 0.21; the best is 0.37 (Table 5 p.14)."

## 11. Open questions / things to verify
- Availability and licence of the released benchmark; ACM published version and DOI; whether Top@K tables are reproducible.
