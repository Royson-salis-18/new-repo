# Report: Li et al. (2022), DéjàVu (FSE '22)

Key `li2022actionable`. Note: `litdb/papers/li2022actionable.md`. Coverage: arXiv text read to Section 6.2; tail and references not read; figures not inspected.

## (a) Bibliographic block
Zeyan Li, Nengwen Zhao, Mingjie Li, Xianglin Lu, Lixin Wang, Dongdong Chang, Xiaohui Nie, Li Cao, Wenchi Zhang, Kaixin Sui, Yanhua Wang, Xu Du, Guoqiang Duan, Dan Pei. ESEC/FSE '22, DOI 10.1145/3540250.3549092; arXiv 2207.09021. Peer reviewed. Scopus: unverified. SJR unknown.

## (b) Plain-language summary
Learns from past failures at a given system which component and kind of problem (a group of metrics) was at fault, using a graph that links related components by calls and by what runs on what.

## (c) Problem and motivation
Metric-only or component-only localization is not actionable (p.1); 74.38% of 576 tickets at a bank were recurring (p.2); average diagnosis time 28.98 min over 20,000 tickets (p.3).

## (d) Method
GRU + CNN feature extractor, 8 stacked GAT layers on the failure dependency graph (call + deployment edges), class-weighted loss and balanced sampling, decision-tree and similar-failure interpretation (pp.3-6).

## (e) Datasets, protocol
601 failures in four sets (A, B production-injected; C 99 real Oracle failures; D Train-Ticket injected); 40/20/40 split; 10 repeats; baselines JSS'20, iSQUAD, DT, GB, RF, SVM, two random walks (pp.6-7).

## (f) Results (copied)
MAR 1.66 / 5.03 / 1.70 / 2.63 on A / B / C / D; A@1 77.18% / 66.21% / 61.84% / 75.62%; A@5 96.28% / 79.24% / 96.32% / 94.27% (Table 3 p.8). Random Forest A@1 73.37% / 84.46% / 61.05% / 85.66%. Ablation without graph aggregation MAR 2.32 / 5.77 / 1.75 / 3.81. Random walk baselines A@1 5% to 24% (p.8).

## (g) Limitations and stern critique
Supervised, recurring-failure setting; Random Forest beats it on A@1 on B and D; effect sizes over repeated runs of one split; injected-failure ground truth with random splits; C has no real graph (so propagation untested on real failures); hand-defined metric groups; production data proprietary.

## (h) Reproducibility
Replication package stated (not checked).

## (i) Head-to-head with our work
Supervised graph-attention RCA with deployment edges; ours is label-free, call-edge only. Their ablation shows graph aggregation (including deployment edges) helps.

## (j) Does it change our problem? Could a reviewer say it exists?
Strengthens our co-location limitation. A reviewer may cite DéjàVu as existing graph-based RCA; our difference is label-free cold start.

## (k) Sentences
Safe: "DéjàVu learns recurring-failure localization over a dependency graph that includes deployment relations and reports A@5 of 79% to 96% on four datasets [DéjàVu]." Must NOT write: that it is label-free; that it beats all baselines on top-1 accuracy.

## (l) Things to verify
Replication package; tail of paper; Scopus status of FSE proceedings.
