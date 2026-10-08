# Report: Unyi et al. (2025), Explainable GNN-Based Fault Forecasting

Key `unyi2025explainable`. Note: `litdb/papers/unyi2025explainable.md`. Coverage: full text read (18 pages); figures not inspected; Table III values did not extract.

## (a) Bibliographic block
Dániel Unyi, Ernő Rigó, Bálint Gyires-Tóth, Róbert Lovas. IEEE TNSM 22(6), pp.5640-5657, Dec 2025; DOI 10.1109/TNSM.2025.3602223; ISSN 1932-4537 / 2373-7379; CC BY 4.0; received 21 Nov 2024, accepted 20 Jul 2025; Crossref: 45 references, 2 citations. Scopus: unverified. SJR unknown.

## (b) Plain-language summary
Generates random 25-node service graphs, computes each system's failure probability with a model checker, trains a GNN to reproduce it from leaf failure rates and retry counts, then trains a second network to point at the nodes that matter.

## (c) Problem and motivation
Debugging is reactive and partially observable (pp.1-2); argued by citation.

## (d) Method
PRISM MDP generator; GNN regression (4 blocks, hidden 32, 200 epochs); explainer GNN with REINFORCE and a node budget (pp.7-9).

## (e) Datasets, protocol
Synthetic: 50 tree topologies x 50 subcases and 10 DAGs x 10 subcases, 25 nodes; median fault probability 1.2e-5; 80/10/10 random split; three runs (pp.10-11).

## (f) Results (copied)
Tree: MAE 0.009 +/- 0.001, R2 0.992 +/- 0.005 (pp.11-12). DAG: MAE 0.009 +/- 0.002, R2 0.996 +/- 0.003 (p.12). DAG-to-tree transfer MAE 0.038, R2 0.938. Explainer top 30% nodes R2 0.974 (tree) and 0.861 (DAG), complement 0.104 and 0.072 (pp.13-15). Baseline MAE (Table III p.13) not extracted.

## (g) Limitations and stern critique
The task regresses a model-checker value from the parameters that define it; no telemetry; synthetic only (authors say so, p.16); three runs; mesh-level random splits with topologies shared across subcases; most targets near zero; explainer sometimes misses sparse critical nodes (p.15); LLM text drafting disclosed (p.15).

## (h) Reproducibility
Dataset and code stated at github.com/BME-SmartLab/GNN-Fault-Forecasting (not checked).

## (i) Head-to-head with our work
Different regime: theirs is simulation and supervised; ours real telemetry and label-free. Their explainer concept (necessary and sufficient node subset) is reusable for our explanations.

## (j) Does it change our problem? Could a reviewer say it exists?
No. "GNN fault probability prediction" exists only in simulation here.

## (k) Sentences
Safe: "A GNN has been trained to predict model-checker fault probabilities on synthetic service meshes; evaluation on real traces is left to future work [unyi2025explainable]." Must NOT write: that it forecasts real failures or that its R2 values show practical forecasting accuracy.

## (l) Things to verify
Table III values; repository; Scopus status of ISSN 1932-4537.
