---
key: unyi2025explainable
title: "Explainable GNN-Based Approach to Fault Forecasting in Cloud Service Debugging"
authors: "Dániel Unyi; Ernő Rigó; Bálint Gyires-Tóth; Róbert Lovas"
year: 2025
venue: "IEEE Transactions on Network and Service Management, vol. 22, no. 6, pp. 5640-5657 (Dec 2025)"
publisher: "IEEE"
doc_type: journal-article
doi: "10.1109/tnsm.2025.3602223"
issn: "1932-4537; 2373-7379"
scopus_indexing: "unverified: Scopus preview check for 1932-4537 not yet done (IEEE TNSM; I expect it to be indexed but did not verify)"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (journal; received 21 Nov 2024, accepted 20 Jul 2025, as printed)"
cited_by_crossref: "2 (Crossref)"
n_references: "45"
license: "CC BY 4.0"
batch: "8"
read_status: reviewed                  # full text read; figures and Table I/III cell values not inspected (Table III values did not extract)
pages: 18
text_chars: 86189
metadata_source: crossref
task: "system-level fault-probability regression on service-mesh graphs plus explainer that selects critical nodes; simulation only"
supervision: "supervised on simulator-generated labels (PRISM model-checker output)"
online_or_streaming: "no"
telemetry: "none (no traces, metrics or logs; node features are leaf failure probability and retry counts)"
propagation_modeling: "GNN (4 message-passing blocks) over DAGs; failure propagation defined by a retry/MDP model"
forecasts_future_failures: "no in the sense of time-ahead prediction of real failures; predicts an aggregate system fault probability from known node parameters"
llm_used: "no (LLM used by authors for text drafting, disclosed p.15)"
systems_evaluated: "synthetic random trees (50 cases x 50 subcases) and DAGs (10 cases x 10 subcases), 25 nodes each (p.11)"
datasets: "generated with PRISM; over 2.1 GB; fault probability median 1.2e-5 (p.11)"
dataset_open: "stated: https://github.com/BME-SmartLab/GNN-Fault-Forecasting (not checked)"
code_open: "stated at the same URL (not checked)"
baselines_compared: "linear regression, linear regression with spectral embeddings, MLP, MLP with spectral embeddings (Table III; values not extracted)"
metrics: "MAE, R2 (3 repeated runs)"
headline_result: "tree meshes test MAE 0.009 +/- 0.001, R2 0.992 +/- 0.005 (p.11-12); DAGs MAE 0.009 +/- 0.002, R2 0.996 +/- 0.003 (p.12); top-30% nodes chosen by explainer R2 0.974 (tree) and 0.861 (DAG) (pp.13-15)"
evidence_quality: "1"
relevance_to_us: "2"
overlap_with_us: "low (probabilistic propagation on graphs, but simulated, supervised, no telemetry)"
threat_level_for_novelty: "low"
---

# Explainable GNN-Based Approach to Fault Forecasting (Unyi et al., TNSM 2025)

> Notes from the **full text** (`litdb/texts/unyi2025explainable.txt`). Page numbers are PDF pages (journal pp.5640-5657). Figures not inspected; Table III cell values did not extract.

## 1. Summary
A GNN is trained to predict the system-level failure probability of a synthetic service mesh (random 25-node trees and DAGs) from two node features: leaf failure probability and intermediary retry count. Labels come from the PRISM probabilistic model checker. An explainer GNN trained with REINFORCE picks a subset of nodes (10-50% budget) that preserves prediction accuracy. No real telemetry is used.

## 2. Problem and motivation
- Debugging distributed services is reactive and partially observable (pp.1-2). Argued from citations; no incident data.

## 3. Method (pp.3-9)
- PRISM generates MDPs from random DAGs; the label is a model-checked probability of root failure (Pmax) (p.7).
- Predictor: four message-passing blocks (hidden 32), mean pool, 200 epochs, Adam 2e-4, MSE, 80/10/10 random split over meshes (p.8).
- Explainer: Bernoulli node mask, reward = MSE(complement) - MSE(selected) + sparsity term (p.9).

## 4. Data and setup (p.10-11)
- 50 tree topologies x 50 parameter subcases, 10 DAG topologies x 10 subcases, 25 nodes each; fault probabilities range 0.0 to 1.0, median 1.2e-5 (p.11).
- Random split is at the mesh level; subcases of the same topology share a topology, so mesh-level random splits put near-identical graph structures in train and test (my inference from the case/subcase structure).

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Tree meshes test MAE / R2 | 0.009 +/- 0.001 / 0.992 +/- 0.005 | not extracted | LinReg, MLP variants | pp.11-13 |
| DAG meshes test MAE / R2 | 0.009 +/- 0.002 / 0.996 +/- 0.003 | not extracted | same | p.12 |
| DAG-trained model tested on trees | MAE 0.038 +/- 0.006, R2 0.938 +/- 0.014 | n/a | n/a | p.12 |
| Explainer 30% nodes, tree / DAG | R2 0.974 +/- 0.018 / 0.861 +/- 0.054 | complement 0.104 / 0.072 | n/a | pp.13-15 |
- Baseline MAE values are in Table III (p.13) as an image; text says MLP with spectral embeddings is better than linear regression but below the GNN.

## 6. Limitations
- Stated: synthetic data only; real traces left to future work; explainer sometimes masks critical sparse nodes (pp.15-16).
- **My critique:**
  1. "Fault forecasting" here is regression of a model-checker output from the very parameters that define the label (leaf failure probabilities and retries). The GNN approximates a known reliability computation, so R2 near 0.99 shows it learned a formula, not that it forecasts real failures.
  2. No real traces, metrics or logs; transfer to real systems is untested (the paper says so, p.16).
  3. Only three runs per setting; no significance tests; random mesh-level splits with shared topologies across subcases.
  4. The explainer finds nodes that matter for a synthetic formula (leaf near the root, few retries), which is largely implied by the generator.
  5. Median fault probability 1.2e-5 means most targets are near zero, so high R2 and low MAE are dominated by easy cases; MAE 0.009 is not scale-free (no relative error reported).
  6. Authors disclose use of ChatGPT and Grammarly for text (p.15).
- Not discussed: calibration, class-imbalanced evaluation of high-risk meshes, comparison with a closed-form or Monte Carlo estimator.

## 7. Reproducibility
- Dataset and code stated at github.com/BME-SmartLab/GNN-Fault-Forecasting (not checked or run).

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | simulator labels | none | ours |
| Live / streaming | no | incremental windows | ours |
| Telemetry used | none | traces (+ metrics) | ours |
| Propagation modelling | GNN on a retry/MDP model | edge probabilities | theirs richer; synthetic |
| Forecasts future failures | system fault probability from node parameters | claimed, untested | neither on real data |
| Explanation | critical node subgraph | templates | theirs (on synthetic) |
| Evaluation rigor | synthetic, 3 runs | synthetic | neither |
| Open / reproducible | stated | yes | tie |

- **What they have that we do not:** an explainer that selects a necessary and sufficient node subset.
- **What we have that they do not:** real telemetry and RCA scoring; negative controls.
- **Could a reviewer say "this already exists"?** Not for real-telemetry cascade risk; yes for "GNN predicts failure probability from a service graph" in simulation.
- **Position:** cite as simulation-based related work on graph-level fault probability prediction. It is not evidence of real forecasting performance.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- It does not change the problem. It shows that "GNN fault forecasting" papers exist that never touch real telemetry; our paper can state that real-trace cascade forecasting remains untested in this line.
- It also corrects my earlier note: the TNSM 2025 "fault forecasting" paper is simulation-only.

## 10. Citation-ready facts (each with page)
- "A GNN reached R2 0.992 (tree) and 0.996 (DAG) predicting model-checker fault probabilities on synthetic 25-node service meshes" (pp.11-12).
- "The authors state real-world evaluation is future work" (p.16).

## 11. Open questions / things to verify
- Table III values; repository contents; Scopus status of ISSN 1932-4537.
