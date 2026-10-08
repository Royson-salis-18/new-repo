# Report: Li et al. (2022), CIRCA (KDD '22)

Key `li2022causal`. Note: `litdb/papers/li2022causal.md`. Coverage: full text of the arXiv version read; appendices only partly.

## (a) Bibliographic block
Mingjie Li, Zeyan Li, Kanglin Yin, Xiaohui Nie, Wenchi Zhang, Kaixin Sui, Dan Pei. KDD '22, pp. (ACM), DOI 10.1145/3534678.3539041; arXiv 2206.05871. Peer reviewed (KDD). Scopus: unverified. SJR unknown.

## (b) Plain-language summary
For each metric, predict its value from its causal parents with a regression trained before the fault; metrics whose actual value deviates are root cause candidates; scores are then adjusted using their children.

## (c) Problem and motivation
A fault produces many abnormal metrics ("anomaly storm"); a short ranked list saves mitigation time (p.1).

## (d) Method
Intervention Recognition Criterion (Theorem 3.4); structural graph from architecture with four meta metrics (traffic, errors, latency, saturation); regression-based hypothesis testing (Eqs 3-4); descendant adjustment (Algorithm 2) (pp.3-5).

## (e) Datasets, protocol
Simulation (VAR, 50/100/500 nodes) and 99 real Oracle database failures from a bank (197 metrics, 2,641-edge graph); baselines NSigma, SPOT, DFS variants, random walks, ENMF, CRD; parameters tuned for best AC@5 on the evaluation data (pp.5-6).

## (f) Results (copied)
D_O: CIRCA AC@1 0.404, AC@5 0.763, Avg@5 0.603, 0.578 s; NSigma 0.323, 0.662, 0.525, 0.472 s (Table 3 p.7). Ablation AC@1: NSigma 0.323, RHT 0.328, CIRCA 0.404 (Table 4). Simulation D50 AC@1: RHT 0.598 vs DFS 0.541; D500: RHT 0.510 vs DFS 0.540 (Table 1). Abstract's 25% = 0.404/0.323.

## (g) Limitations and stern critique
Baseline trivial NSigma is the runner-up; the gain is about 0.08 absolute on 99 cases without intervals; tuning on the evaluation set; one proprietary dataset (database, not microservices); hand-built graphs; assumptions (Markovian, DAG) partly violated by the authors' own admission (p.9); counterfactual methods dismissed, not run.

## (h) Reproducibility
Code stated (github.com/NetManAIOps/CIRCA, not checked); real data not released.

## (i) Head-to-head with our work
Direct competitor family: label-free, graph-aware metric RCA. Theirs has a causal criterion; ours learns trace-based edge weights and outputs risk.

## (j) Does it change our problem? Could a reviewer say it exists?
It confirms that label-free RCA is established. Must-cite, must-run baseline; also shows NSigma is strong.

## (k) Sentences
Safe: "CIRCA formulates RCA as intervention recognition and ranks metrics by deviation from regression on causal parents without labels [CIRCA]." Must NOT write: that its 25% gain is robust (it is 8 cases of 99 against a simple baseline).

## (l) Things to verify
KDD published version; repository; whether D_O has any public counterpart.
