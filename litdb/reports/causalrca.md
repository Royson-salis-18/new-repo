# Report: Xin, Chen, Zhao (2023), CausalRCA

Key `causalrca`. Note: `litdb/papers/causalrca.md`. Coverage: pages 1-12 read as rendered images (scanned PDF); page 13 (references) not read; Figs 6, 9-11 seen only as plots.

## (a) Bibliographic block
Ruyue Xin, Peng Chen, Zhiming Zhao. J. Syst. Softw. 203 (2023) 111724, DOI 10.1016/j.jss.2023.111724, ISSN 0164-1212 (Crossref), Elsevier, CC BY 4.0, received 15 Jul 2022, accepted 19 Apr 2023. Crossref: 101 citations, 65 references. Scopus: unverified. SJR unknown (no list).

## (b) Plain-language summary
Learns which metrics influence which (a causal graph from a neural model), then ranks metrics by PageRank to find the root cause. Tested on a demo shop with three kinds of injected faults.

## (c) Problem and motivation
Naming the faulty metric helps operators act more precisely than naming a service (pp.1-3). Argued by citation only.

## (d) Method
DAG-GNN VAE with augmented-Lagrangian acyclicity constraint (Eqs 1-7); PageRank with restart 0.85 on the reversed weighted graph (Eqs 8-9); 1000 epochs, lr 1e-3, 10 runs averaged (pp.4-7).

## (e) Datasets, protocol
Sock-Shop, 13 services on Kubernetes; Prometheus every 5 s; CPU hog, memory leak, network delay injected for 5 minutes with a 10-minute cool-down; injection counts not stated; baselines PC, GES, LiNGAM plus PageRank at default settings; ANOVA and t-tests on Avg@5 (pp.6-7).

## (f) Results (copied)
Service level: average Avg@5 0.5815 vs LiNGAM 0.5143 (+6.72%), Table 3 p.8; PC beats it on network-delay AC@3 (0.5714 vs 0.3857). Metric level in the faulty service: average Avg@5 0.6681 vs LiNGAM 0.5738 (+9.43%), average AC@3 0.719, Table 4 p.9; PC wins CPU-hog AC@1 (0.4286 vs 0.2286), LiNGAM wins memory-leak AC@1 (0.4286 vs 0.2714). All-metrics task: average rank about 13, discussion says "out of ten" (pp.10-11). ANOVA p 0.0003 and 0.0013; LiNGAM vs CausalRCA p 0.0335 in the all-metrics task.

## (g) Limitations and stern critique
One testbed, three synthetic stress faults, undeclared injection count, p-values over 10 runs of the same data; own hyperparameters tuned on test data, baselines at defaults; AC@1 not best in several cells; abstract vs intro metric naming differs (Avg@5 vs AC@5); all-metrics rank text inconsistent; offline analysis described as real-time; no simple baselines such as BARO/NSigma; no failure-time sensitivity.

## (h) Reproducibility
Code and data at github.com/AXinx/CausalRCA_code (no license, last push 2023-05-02, notebooks, scripts, data_collected). Not run.

## (i) Head-to-head with our work
Label-free like ours; richer learned graph; metrics-only; no forecasting; modest, single-system evidence.

## (j) Does it change our problem? Could a reviewer say it exists?
No change. A reviewer can say label-free causal-graph metric RCA exists; our difference is trace-based propagation plus risk scoring, which this paper does not address.

## (k) Sentences
Safe: "Gradient-based causal structure learning with PageRank has been applied to fine-grained metric RCA on Sock-Shop [causalrca]." Must NOT write: that it outperforms baselines in general, or that it is real-time.

## (l) Things to verify
Page 13; injection counts; Scopus status of 0164-1212; whether CausalRCA is in RCAEval.
