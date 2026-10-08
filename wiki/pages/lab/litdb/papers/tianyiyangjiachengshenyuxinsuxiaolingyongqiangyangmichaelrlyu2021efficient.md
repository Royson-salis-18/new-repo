---
key: tianyiyangjiachengshenyuxinsuxiaolingyongqiangyangmichaelrlyu2021efficient
title: "AID: Efficient Prediction of Aggregated Intensity of Dependency in Large-scale Cloud Systems"
authors: "Tianyi Yang; Jiacheng Shen; Yuxin Su; Xiao Ling; Yongqiang Yang; Michael R. Lyu"
year: 2021
venue: "arXiv preprint 2109.04893v1 (cs.SE, 20 Aug 2021); published venue not stated in the text (unverified)"
publisher: "arXiv"
doc_type: preprint
doi: "10.48550/arxiv.2109.04893"
issn: ""
scopus_indexing: "arXiv preprints are not Scopus-indexed; the published version (if any) was not checked"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "preprint (peer-review status of any published version unverified)"
cited_by_crossref: ""
n_references: "about 38 (reference list partly read)"
license: ""
batch: "8"
read_status: reviewed                  # full text read to the references; Figs 1-6 not inspected
pages: 13
text_chars: 71515
metadata_source: arxiv
task: "estimate the strength ('intensity') of service-to-service dependencies from traces; motivated by cascading-failure impact; NOT a forecast of failure times"
supervision: "label-free (unsupervised; labels only for evaluation)"
online_or_streaming: "claimed continuous update in a production dependency system (anecdotal); batch evaluation"
telemetry: "traces (spans aggregated per service into invocation count, error rate, mean duration per 1-minute bin)"
propagation_modeling: "edge weight = normalised directed time-warping similarity of caller and callee status series; indirect dependencies by assumed transitivity (not evaluated)"
forecasts_future_failures: "no (it scores dependency strength; the abstract says 'predict' for the intensity value)"
llm_used: "no"
systems_evaluated: "Train-Ticket (25 microservices, 17,471,024 spans) and a Huawei Cloud region (192 microservices, about 1.0e10 spans, 7 days)"
datasets: "TT (simulated users) and Industry; only 19 labelled dependencies in TT and 75 in Industry (strong/weak binary)"
dataset_open: "stated: https://github.com/OpsPAI/aid (not checked)"
code_open: "stated at the same URL (not checked)"
baselines_compared: "Pearson, Spearman, Kendall correlation on the same status series; plain DTW ablation"
metrics: "cross entropy, MAE, RMSE against binary strong/weak labels"
headline_result: "Industry: AID CE 0.3270, MAE 0.1751, RMSE 0.3044 vs best baseline CE 0.6030, MAE 0.4501, RMSE 0.4537 (Table III p.8); TT: Pearson MAE 0.3305 beats AID 0.3435 (Table III)"
evidence_quality: "2"
relevance_to_us: "4"
overlap_with_us: "partial (label-free trace-based edge-strength estimation, our propagation weights)"
threat_level_for_novelty: "medium"
---

# AID: Aggregated Intensity of Dependency (Yang et al., 2021, arXiv)

> Reading notes from the **full text** (`litdb/texts/tianyiyang...txt`). Page numbers are PDF pages. Figs 1-6 not inspected.

## 1. One-paragraph summary
AID estimates how strongly a caller depends on a callee. Spans are binned per service into three KPIs (invocation count, error rate, mean duration). Directed time warping (DSW) measures similarity between caller and callee series, min-max normalised and averaged over the three KPIs. Evaluated against 19 and 75 hand-labelled dependencies (strong/weak) on Train-Ticket and a Huawei Cloud region. It outputs edge weights; it does not forecast when or whether a failure will occur.

## 2. Problem and motivation
- Binary dependency graphs cannot tell engineers which dependencies matter during an outage (pp.1-5).
- Evidence: 5 of 13 public AWS outages (2011-2020) are "related" to service dependency (38%) (Table I p.4); an analysis of over 1000 Huawei Cloud incidents in 2019 where improper dependency was reportedly the most frequent cause, with no figures given (p.3); engineer interviews at one company (p.4). Evidence type: small anecdotal survey plus one company's statement.
- Real? Plausible; the numbers are too thin to cite as a rate.

## 3. Method
- Candidate pairs (P, C) from parent/child spans; status series (invo, err, dur) per 1-minute bin; DSW: directed warping window = max callee duration + round-trip estimate, plus time-drift allowance (Algorithm 1 p.7); intensity I = mean of three min-max normalised similarities (Eq 1-2 p.7).
- Complexity O(k N^2) per pair; 155 s per pair of 1440-bin series on a laptop (p.9).
- Assumptions: direct calls only; transitive strength by chaining (p.10); asynchronous calls are a stated weakness (p.10).

## 4. Data and experimental setup
- TT: 25 services, 18 strong and 1 weak labels (Table II p.7). Industry: 192 services, 67 strong and 8 weak (Table II); only dependencies engineers knew were labelled (footnote p.7).
- Labels: two PhD students (TT) and senior engineers (Industry), consensus on disagreement.
- Parameters: bin 1 minute, round trip 0, drift 1 minute (Industry) or 0 (TT) (p.8). Bin sizes 1-10 minutes tested on Industry only.
- Leakage: none (unsupervised); but parameters are tuned on the evaluated data.

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Industry CE / MAE / RMSE | 0.3270 / 0.1751 / 0.3044 | 0.6030 / 0.4501 / 0.4537 (best per column from Spearman) | correlation baselines | Table III p.8 |
| TT CE / MAE / RMSE | 0.4562 / 0.3435 / 0.3859 | 0.6464 (Kendall) / 0.3305 (Pearson) / 0.4388 (Pearson) | Pearson, Spearman, Kendall | Table III |
| DSW vs DTW on Industry | CE 0.3270 vs 0.3584 | n/a | AID_DTW | Table IV p.9 |
| Reduction on Industry | 45.8%, 61.1%, 33.2% (as stated) | n/a | n/a | p.9 |

- The 45.8% quoted for cross entropy matches 0.3270 vs 0.6030 (as reported). No statistical tests; one run.
- Case study: more than ten unnecessary dependencies found and optimised since deployment; engineer feedback only, no measured benefit (p.10).

## 6. Limitations
- Stated: labelling accuracy, small simulator with one weak dependency, asynchronous calls, indirect dependencies (pp.10).
- **My critique:**
  1. Task is dependency strength, not failure prediction; the "cascading failure prediction" framing is only motivation (p.2).
  2. Evaluation set is tiny and skewed: TT has 18 of 19 strong, so predicting "strong" everywhere scores well; Industry 67 of 75 strong (about 89%). A constant predictor of 0.89 would also be a natural baseline, not reported.
  3. Labels are binary and chosen by engineers for dependencies they knew; the continuous score is compared to 0/1.
  4. Baselines are correlation coefficients on the same series; no other dependency-mining methods (Rippler, CloudScout etc.) are run (p.11).
  5. Training-time and test-time parameters (drift, bin size) are set on the evaluation data.
  6. Stated "first": narrow claim (intensity from traces).
- Not discussed: label noise, confidence intervals, performance during an actual failure (the claimed cascading-failure use is anecdotal).

## 7. Reproducibility
- Code and data stated at github.com/OpsPAI/aid (not checked yet). Industrial data cannot be shared in full; the released set is described as released with the paper.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | none (labels for eval) | none | tie |
| Live / streaming | batch, anecdotal live use | incremental | ours (claimed) |
| Telemetry used | traces | traces (+ metrics) | similar |
| Propagation modelling | per-edge strength from time-warped similarity | learned edge probabilities | similar idea; theirs tested on edges |
| Forecasts future failures | no | claimed | n/a |
| Explanation | none | templates | ours |
| Evaluation rigor | 94 labelled edges, no CIs | synthetic | theirs has real data |
| Open / reproducible | stated | yes | tie |

- **What they have that we do not:** an evaluation of edge weights against engineer labels on a real cloud (Industry), and directed time-warping that handles caller-callee lag.
- **What we have that they do not:** use of the weights for RCA ranking and risk scoring; negative controls.
- **Could a reviewer say "this already exists"?** For "learn the strength of call edges from traces without labels": yes, partly. We must cite AID and compare our edge-weight estimator against its DSW similarity.
- **Position:** cite as prior work on label-free edge strength; do not call it failure prediction.
- **Must we run it as a baseline?** Yes, as a propagation-weight baseline if code is available.

## 9. Does this paper change what problem we should solve?
- It corrects my earlier reading of AID in `docs/REVIEW_REPORT.md` (it was described as predicting cascading impact; it estimates dependency strength). The gap "forecast cascade risk" is therefore less covered by AID than assumed, but "learn edge strength without labels" is covered.

## 10. Citation-ready facts (each with page)
- "AID derives a continuous dependency intensity from trace-derived invocation, error and duration series with a directed time-warping similarity" (pp.5-7).
- "On a Huawei Cloud region with 75 labelled dependencies, AID reached cross entropy 0.327 vs 0.603 for the best correlation baseline" (Table III p.8; note 67 of 75 labels are strong).

## 11. Open questions / things to verify
- Published venue; repo contents; whether AID's weights improve RCA ranking (not evaluated).
