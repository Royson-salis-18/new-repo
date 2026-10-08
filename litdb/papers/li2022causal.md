---
key: li2022causal
title: "Causal Inference-Based Root Cause Analysis for Online Service Systems with Intervention Recognition (CIRCA)"
authors: "Mingjie Li; Zeyan Li; Kanglin Yin; Xiaohui Nie; Wenchi Zhang; Kaixin Sui; Dan Pei"
year: 2022
venue: "Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '22), Washington DC; arXiv 2206.05871 version read"
publisher: "ACM"
doc_type: proceedings-article
doi: "10.1145/3534678.3539041"
issn: ""
scopus_indexing: "unverified: KDD proceedings not checked in the Scopus preview; the arXiv copy is a preprint"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (KDD '22 proceedings; the arXiv version read is the author copy)"
cited_by_crossref: ""
n_references: "32"
license: ""
batch: "9"
read_status: reviewed                  # full text read to the references; appendices A-C partly skimmed (proof start p.10 only)
pages: 11
text_chars: 0
metadata_source: crossref+arxiv
task: "root cause metric ranking (indicator level)"
supervision: "label-free (unsupervised; regression trained on pre-fault data; labels only for evaluation)"
online_or_streaming: "no live evaluation; analysis delay 5 min after detection assumed"
telemetry: "metrics (1-minute sampling) with a structural graph built from architecture/call graph"
propagation_modeling: "causal Bayesian network from architecture knowledge ('structural graph') + regression-based hypothesis testing + descendant adjustment"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "simulation (VAR graphs of 50/100/500 nodes) and 99 real Oracle database failures from a large banking system (D_O)"
datasets: "D_O: 99 cases, 197 metrics, 2,641-edge structural graph; not released (stated only code)"
dataset_open: "no (real data not released); simulation generator described"
code_open: "stated: https://github.com/NetManAIOps/CIRCA (not checked)"
baselines_compared: "NSigma, SPOT, DFS, DFS-MS, DFS-MH, RW-Par, RW-2, ENMF, CRD (graph builders PC-gauss, PC-gsq, PCTS, Structural)"
metrics: "AC@k, Avg@5, time"
headline_result: "D_O: CIRCA AC@1 0.404, AC@5 0.763, Avg@5 0.603 vs best AC@1 baseline NSigma 0.323 (Table 3 p.7); abstract: 25% top-1 recall gain (0.404/0.323 = 1.25)"
evidence_quality: "3"
relevance_to_us: "4"
overlap_with_us: "high for label-free metric RCA with explicit graph"
threat_level_for_novelty: "medium"
---

# CIRCA (Li et al., KDD 2022)

> Notes from the **full text** of the arXiv version (`litdb/texts/li2022causal.txt`). Page numbers are PDF pages. Appendices not read in full.

## 1. Summary
Formulates RCA as "intervention recognition": a metric is a root cause indicator if its distribution given its parents in a causal Bayesian network changes. Builds a structural graph from architecture knowledge (four meta metrics per service: traffic, errors, latency, saturation), tests each metric with regression residuals, and adjusts scores using descendants. Evaluated by simulation and on 99 Oracle database failures.

## 2. Problem and motivation
- A single fault can cause an "anomaly storm"; ranking a few root cause indicators saves mitigation time (p.1). No new data; cites prior studies.

## 3. Method (pp.3-5)
- Theorem 3.4 (Intervention Recognition Criterion), regression-based hypothesis testing with per-metric residual z-scores (Eqs 3-4), score s = max over time; descendant adjustment (Algorithm 2) adds the largest score among non-anomalous (score below 3) descendants to anomalous metrics.
- Structural graph: traffic causes all others, saturation to latency, errors accumulate downstream (Fig 2, Algorithm 1).
- Assumptions: DAG, Markovian, faithfulness; defaults t_delay 5 min, t_ref 120 min, t_test 10 min (p.5).

## 4. Data and experimental setup
- Simulation: VAR models with 50/100/500 nodes, 10 graphs by 100 cases each; baseline parameters tuned for best AC@5 on the first graph (p.5).
- Real: 99 Oracle database high-AAS failures at a bank; call graph from vendor documentation; 197 metrics mapped to meta metrics; graph chosen per scoring method by best AC@5 on the same data; baseline parameters also tuned for AC@5 on D_O (pp.5-6).

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| D_O AC@1 / AC@5 / Avg@5 | 0.404 / 0.763 / 0.603 | 0.323 / 0.662 / 0.525 | NSigma | Table 3 p.7 |
| D_O time per case (s) | 0.578 | 0.472 | NSigma | Table 3 |
| Ablation AC@1: NSigma / RHT / CIRCA | 0.323 / 0.328 / 0.404 | n/a | n/a | Table 4 p.7 |
| Simulation D50 AC@1 / AC@5 | RHT 0.598 / 0.880 | 0.541 / 0.761 | DFS / SPOT | Table 1 p.7 |
| Simulation D500 AC@1 | RHT 0.510 | DFS 0.540 (DFS better) | DFS | Table 1 |
- Simulation: RHT-PG beats baselines (p<0.001 t-test on AC@k, p.6); the real-data table has no statistical test.

## 6. Limitations
- Stated: assumptions may not hold; hidden meta metrics violate Markovian; descendant adjustment needs verification on more real datasets (pp.8-9).
- **My critique:**
  1. The strongest baseline on real data is the trivial NSigma; the gain over it is 8 cases at AC@1 on 99 (about 0.081 absolute), without confidence intervals.
  2. Baseline and graph choices were tuned on the evaluation set (best AC@5), which favours the baselines but also blurs the comparison; CIRCA's own settings are also fixed on D_O.
  3. Real data are one database type at one bank, not released; the structural graph is hand-built from documentation per instance type.
  4. In simulation at 500 nodes RHT AC@1 (0.510) trails DFS (0.540); gains depend on a perfect graph (RHT-PG).
  5. Corollary 3.3 dismisses counterfactual methods (Sage) without evaluating them.
- Not discussed: failure-time misspecification beyond t_delay sweep; microservice (non-database) benchmarks.

## 7. Reproducibility
- Code stated at github.com/NetManAIOps/CIRCA (not checked). Real data not released.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | none | none | tie |
| Live / streaming | offline cases | incremental | ours (claimed) |
| Telemetry used | metrics | traces (+ metrics) | different |
| Propagation modelling | explicit CBN from architecture + causal criterion | learned edge probabilities | theirs principled; ours learns weights |
| Forecasts future failures | no | claimed | n/a |
| Explanation | causal criterion + case study | templates | theirs |
| Evaluation rigor | simulation + 99 real cases, tuned on test | synthetic | theirs |
| Open / reproducible | code stated | yes | tie |

- **What they have that we do not:** a causal criterion, descendant adjustment and an evaluation on real failures.
- **What we have that they do not:** trace-based learned edge weights and cascade-risk output.
- **Could a reviewer say "this already exists"?** Yes for "label-free, architecture-aware causal RCA on metrics". CIRCA is a must-cite and must-run baseline (it is in RCAEval).
- **Position:** cite as the label-free, architecture-aware causal baseline; it also cites AID for dependency intensity (ref [26], ASE 2021).
- **Must we run it as a baseline?** Yes.

## 9. Does this paper change what problem we should solve?
- It reinforces that "unlabeled RCA" is established. Its own result that NSigma is the strongest simple baseline on real data supports adding NSigma and BARO to our comparison.

## 10. Citation-ready facts (each with page)
- "CIRCA reached top-1 recall 0.404 vs 0.323 for NSigma on 99 real Oracle failures (Table 3 p.7)".
- "CIRCA's gain on simulation requires a correct graph; with a broken graph the gap to ideal grows with node count (p.6)".

## 11. Open questions / things to verify
- Published KDD version vs arXiv version; code; Scopus status of KDD proceedings.
