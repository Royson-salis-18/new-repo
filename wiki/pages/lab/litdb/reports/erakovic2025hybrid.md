# Report: Erakovic and Pahl (2025), Hybrid Root Cause Analysis for Partially Observable Microservices

Key `erakovic2025hybrid`. Note: `litdb/papers/erakovic2025hybrid.md`. Page numbers are PDF pages (CLOSER pp.255-263).
Coverage: full text read to the end. Tables 1 and 2 and Figures 1-9 are images that did not extract; numeric evidence in them is unknown to me.

## (a) Bibliographic block
Isidora Erakovic and Claus Pahl (Free University of Bozen-Bolzano). CLOSER 2025 (15th International Conference on Cloud Computing and Services Science), pp.255-263. SCITEPRESS. DOI 10.5220/0013453600003950; ISBN 978-989-758-747-4; ISSN 2184-5042. CC BY-NC-ND 4.0. Scopus: the ISSN matches the Scopus source "International Conference on Cloud Computing and Services Science, CLOSER - Proceedings" (preview 2026-10-07, CiteScore 2025 = 2.2, 37th percentile, 130 documents for 2022 to 2025); coverage of the 2025 volume is unverified. SJR 2025 shown as 0.22; quartile unknown. Peer reviewed: conference paper, review details not stated.

## (b) Plain-language summary
When only request traces are available, the authors judge which service is faulty and what kind of fault it is from how latency changes over time and where the service sits in the architecture. They hand-write five rules (CPU, memory, host network, container network, database) and show two worked examples from a public ISP trace dataset.

## (c) Problem and motivation
Partial observability: no CPU, network or storage metrics, only trace latency (p.1). Motivation is generic (RCA is crucial for reliability); claim that the state of the art lacks architecture-aware interpretation of RCA results (p.1). No data. Evidence type: assumed.

## (d) Method
Mine the architecture from trace CSVs (call graph; shared hosts or resources, including load-balancer patterns); flag components whose latency exceeds their normal-period maximum (method from Forsberg 2019, a master's thesis); classify latency patterns (gradual rise, rapid rise, widespread spikes) and match with architecture to a rule: CPU exhaustion (rapid rise, shared CPU), memory exhaustion (gradual rise, affected component), host network error (widespread spikes, same host), container network error (rapid rise, affected container plus connected ones), database failure (rapid rise, all database-connected components) (Sec. 4.2.3, p.4). BIRCH clustering is used to "validate results". Gradient thresholds and the exact anomaly criteria are not specified.

## (e) Datasets, protocol, leakage
ISP trace dataset from the TraceRCA repository (p.3): the method was built on rca_2020_04_22.csv with ret_info.csv fault injection records, and tested on rca_2020_04_21.csv, where trace IDs exist for only the first 40 minutes and one fault is injected at docker_007 at 00:17 (p.7). Rules come from the literature and the authors' own analysis of the same dataset family; the evaluation is two worked cases from the same system.

## (f) Results (copied)
No metrics. For 22 April the authors conclude a container network error at docker_004 from latency plots (Figs 1 to 8, pp.5 to 7); for 21 April they conclude a container network issue at docker_007 from latency tables and plots (Tables 1 and 2, Fig 9, pp.7 to 8). No accuracy, precision, recall, MRR, detection delay, baselines, ablations, statistics or runtime.

## (g) Limitations and stern critique
Authors: variability of system behaviour and need for adaptive thresholds (p.8). Mine: two worked examples with one fault each, judged visually; handcrafted rules checked on the same system; thresholds undefined; the paper itself notes db_003 showed no effect for lack of interactions; no comparison with MicroRank, TraceRCA, MRCA or DeepHunt despite claiming to go beyond MRCA; relies on a companion paper for details; unverifiable without the figures; no false alarm analysis.

## (h) Reproducibility
The dataset is public (TraceRCA repository, cited on p.3; I did not open or download it). No code. The rules are reproducible in outline but thresholds are missing.

## (i) Head-to-head with our work
Closest in constraints: trace-only, label-free, offline. It adds architecture-aware fault-type reasoning that we lack, with almost no evidence. Our advantage is a quantified evaluation design and open code. The ISP dataset is a candidate for our first real-fault test (subject to permission to download).

## (j) Does it change our problem? Could a reviewer say it exists?
Does not change the problem. A reviewer could cite it for "trace-only, label-free, architecture-aware RCA"; we must state the difference (probabilistic propagation, calibration on a baseline window, quantitative evaluation).

## (k) Sentences
Safe: "Erakovic and Pahl propose rule-based RCA on trace latency with architecture mining and illustrate it on injected faults from a public ISP trace dataset [erakovic2025hybrid]." Must NOT write: that it achieves a stated accuracy; that it was evaluated against baselines; that it classifies fault types reliably; that it is Scopus-indexed beyond the series-level check.

## (l) Things to verify
Table and figure content; whether the TraceRCA ISP dataset contains the files named; the companion paper.
