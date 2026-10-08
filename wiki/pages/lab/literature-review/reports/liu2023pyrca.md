# Report: Liu et al. (2023), PyRCA

Key `liu2023pyrca`. Note: `litdb/papers/` same key. Coverage: full text read (12 pages); dashboard figures not inspected.

## (a) Bibliographic block
Chenghao Liu, Wenzhuo Yang, Himanshu Mittal, Manpreet Singh, Doyen Sahoo, Steven C. H. Hoi (Salesforce AI). arXiv 2306.11417v1, cs.AI, 20 Jun 2023. Technical report; not peer reviewed; not Scopus-indexed. SJR unknown.

## (b) Plain-language summary
A toolbox that bundles common metric-based RCA methods behind one interface, with a dashboard for editing the causal graph.

## (c) Problem and motivation
Thousands of KPIs per incident make manual RCA slow; no one-stop open library existed (pp.1-3).

## (d) Method
Input layer (pandas, YAML expert knowledge), model layer (anomaly detection, PC/GES, random walk, hypothesis testing, RCD, epsilon-diagnosis, Bayesian inference), output layer (visualization, evaluation) (pp.4-9).

## (e) Datasets, protocol
Synthetic: 500 graphs, 20 nodes, 30 edges, 5000 samples each (p.9).

## (f) Results (copied)
Recall@1/3/5: HT with true graph 1.00/1.00/1.00; HT-pc 0.95/1.00/1.00; HT-adj-pc 0.77/0.92/0.92; Local-RCD 0.44/0.70/0.70; RCD 0.28/0.29/0.30; random walk 0.07/0.20/0.24 (Table 1 p.10). PC graph F1 0.78, SHD 11.45; GES F1 0.45, SHD 32.53 (Table 2).

## (g) Limitations and stern critique
Synthetic data follow the hypothesis-testing model's own assumptions; no real or microservice data; no trivial baseline; not peer reviewed.

## (h) Reproducibility
Open source library (stated; not checked or installed).

## (i) Head-to-head with our work
Tooling: baseline implementations for CIRCA/RCD/epsilon-diagnosis.

## (j) Does it change our problem? Could a reviewer say it exists?
No.

## (k) Sentences
Safe: "PyRCA is an open-source library of metric-based RCA methods [PyRCA]." Must NOT write: that HT's perfect synthetic recall indicates real-world accuracy.

## (l) Things to verify
Repository status; dependency compatibility with our environment (needs a check before any install).
