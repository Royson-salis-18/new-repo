# Report: Zhao, Wang et al. (2024/2025), CHASE

Key `zimingzhao...chase`. Note: `litdb/papers/zimingzhao...chase.md`. Page numbers are PDF pages.
Coverage: full text read to the last reference ([36]). Not inspected: Figs 1-4. Not opened: the Google Drive code link.

## (a) Bibliographic block
Ziming Zhao, Zhenwei Wang (equal contribution), Tiehua Zhang (corresponding), Zhishu Shen, Hai Dong, Zhen Lei, Xingjun Ma, Gaowei Xu, Zhijun Ding, Yun Yang. arXiv:2406.19711v2 [cs.LG], 22 April 2025; the manuscript is in an IEEE journal LaTeX template ("JOURNAL OF LATEX CLASS FILES, April 2024") with no venue named. The arXiv record shows no journal reference or DOI (checked 2026-10-07). Preprint: not peer reviewed (publication status unknown), not Scopus-indexed. SJR n/a.

## (b) Plain-language summary
A neural model that reads the call structure of each request together with the logs and metrics of each service involved and decides which service is the root cause. A "hypergraph" step lets information flow along whole call paths at once instead of one hop at a time. It beats seven baselines on a small 10-service dataset and shows a modest gain on a bigger competition dataset.

## (c) Problem and motivation
Joint modelling of multimodal data, topology and multi-hop propagation (pp.1-2). No incident data, outage costs or labelling cost are given. Evidence type: assumed.

## (d) Method
Per trace, build a graph of instance, metric and log nodes. Encode logs with FastText on templates, metrics with a time-series transformer (last timestep), instances with one-hot plus sinusoidal position. Attention over each instance's log and metric neighbours with learnable per-modality priors (Eq.3-9; gamma = 0.5). Hyperedges: for each node and each of its parents, a hyperedge containing the node, the parent and all ancestors of the parent, plus one hyperedge of the node's descendants (Algorithm 1, p.6); equal weights; one hypergraph convolution (Eq.14); cross-entropy classification of each instance as root cause (Eq.15). 3 attention layers, 8 heads, hidden 128. Requires labelled traces.

## (e) Datasets, protocol, leakage
GAIA (MicroSS): 10 instances, anomalies injected into logs (four types), 1099 static traces, 160 for training; AIOps 2020: hundreds of instances, 68 failures of about five minutes over three months, dynamic topology (p.7). Metrics: A@1, A@3, Avg@5 on GAIA; Percentage@n (share of traces flagged anomalous within n minutes after the failure start) on AIOps 2020. The split unit (trace vs failure) is not specified; traces from one failure are correlated, so leakage is possible. No repeats.

## (f) Results (copied)
GAIA (Table II, p.8), A@1 / A@3 / Avg@5: CHASE 0.6135 / 0.8823 / 0.8276; TrinityRCL 0.4503 / 0.8244 / 0.7651; DiagFusion 0.4121 / 0.8157 / 0.7484; CausalRCA 0.3652 / 0.4973 / 0.5966; MicroRCA 0.3421 / 0.5528 / 0.5712; CloudRanger 0.3290 / 0.4771 / 0.4883; GES 0.3003 / 0.5399 / 0.5154; PC 0.2960 / 0.6368 / 0.5953. AIOps 2020 Percentage@5 / @3 / @1: CHASE 0.15 / 0.16 / 0.22; TrinityRCL 0.12 / 0.14 / 0.15; DiagFusion 0.12 / 0.14 / 0.14; MicroRCA 0.08 / 0.13 / 0.17; GES 0.11 / 0.08 / 0.14. Ablation (Table III, p.10): without instance embedding 0.5927 / 0.8554 / 0.7852; without heterogeneous message passing 0.3845 / 0.5403 / 0.6581; without causal hyperedge 0.4679 / 0.8106 / 0.7598. "36.2%" is a relative gain. No statistical tests or variance.

## (g) Limitations and stern critique
Authors: none stated beyond future work. Mine: supervised without saying so; GAIA has 10 instances with log-injected faults (chance A@1 about 0.10), so it is easy; the AIOps 2020 metric is trace-flagging, not localization, and absolute values 0.15 to 0.22 are low; the "causal" hypergraph is call-graph ancestry with equal weights, not inferred causality; baselines mis-described (MicroRCA text copies CausalRCA's description; CloudRanger described as an ML log model; PC and GES with out-degree weights); no variance or tests; baselines inapplicable on the harder dataset; code only on Google Drive; unknown venue.

## (h) Reproducibility
Code link is a Google Drive file (unopened). GAIA and AIOps 2020 repositories exist (HTTP 200, not downloaded). Not reproduced.

## (i) Head-to-head with our work
No overlap in setting: CHASE is supervised, offline and per-trace. It does show the supervised-GNN family reaches high top-1 on small easy data, but its evidence is weak. Nothing here supports or threatens our forecasting or label-free claims.

## (j) Does it change our problem? Could a reviewer say it exists?
No. It is one of many supervised GNN localizers. We should cite it among them if space allows and not as a baseline.

## (k) Sentences
Safe: "CHASE (Zhao et al. 2024) is a supervised heterogeneous-graph and hypergraph localizer that reports A@1 of 0.6135 on the GAIA dataset (10 service instances)." Must NOT write: that CHASE infers causal relations (its hyperedges follow the call graph); that it is label-free; that it is peer reviewed or published in a named venue; that it was validated on real production incidents; that its AIOps 2020 percentages measure root cause accuracy.

## (l) Things to verify
Code link and whether it runs; publication venue; trace-versus-failure split; Figs 1-4.
