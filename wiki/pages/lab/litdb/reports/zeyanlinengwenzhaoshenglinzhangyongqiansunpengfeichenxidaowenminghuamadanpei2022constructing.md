# Report: Li et al. (2022), Constructing Large-Scale Real-World Benchmark Datasets for AIOps

Key `zeyanlin...2022constructing`. Note: `litdb/papers/` same key. Coverage: text read to the conclusion; references not read; figures not inspected.

## (a) Bibliographic block
Zeyan Li, Nengwen Zhao, Shenglin Zhang, Yongqian Sun, Pengfei Chen, Xidao Wen, Minghua Ma, Dan Pei. arXiv 2208.03938v1, 8 Aug 2022; header says ESEC/FSE 2022 (track unstated, unverified). Preprint; not Scopus-indexed. SJR unknown.

## (b) Plain-language summary
The authors release three real-company datasets with yearly competitions: labelled KPI anomalies, injected failures on order data, and injected failures in a production-style system with traces, KPIs and metrics.

## (c) Problem and motivation
Most AIOps work is evaluated on private data, so generality is unknown (pp.1-2).

## (d) Method
Dataset A (27 KPIs, Table 1), B (400 synthetic failures via ripple-effect modification), C (169 injected failures, 7 types, spans/KPIs/metrics) (pp.2-5).

## (e) Datasets, protocol
Competition protocols; dataset C: at most two root-cause metrics per failure, precision at least 0.5 to be valid, rank-based points (p.5).

## (f) Results (copied)
Best F1 0.8216 (KPI detection, 2018) and 0.9593 (dataset B, 2019); best score 755 for 129 failures (dataset C, 2020); participation 125 / 141 / 141 teams (pp.2-5).

## (g) Limitations and stern critique
Injected faults on one system with seven types; dataset B is synthetic; no baseline results; published version and track unverified; references not read.

## (h) Reproducibility
Datasets via the competition links (stated, not checked).

## (i) Head-to-head with our work
Dataset provider: trace-based test data with call and deployment dependencies.

## (j) Does it change our problem? Could a reviewer say it exists?
No.

## (k) Sentences
Safe: "The AIOps 2020 challenge dataset provides traces, KPIs and metrics for 169 injected failures in a distributed system [AIOps datasets]." Must NOT write: that the injected faults are real production failures.

## (l) Things to verify
Published version; dataset licence; relation to the dataset called AIOps-2021 elsewhere.
