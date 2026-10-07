# Report: Xie, He, Wang, Li (2025), CCLH hypergraph RCA

Key `shuaiyuxie...root`. Note: `litdb/papers/shuaiyuxie...root.md`. Page numbers are PDF pages.
Coverage: full text and Tables I-III read; Figs 1-6 not inspected (Fig 1 illustrations, Figs 5 and 6 sensitivity and generalization plots).

## (a) Bibliographic block
Shuaiyu Xie, Hanbin He (equal contribution), Jian Wang, Bing Li (Wuhan University; Zhongguancun Laboratory). arXiv:2511.17566v1 [cs.LG], 14 November 2025. No DOI or journal reference. Preprint: not peer reviewed (status unknown), not Scopus-indexed. SJR n/a.

## (b) Plain-language summary
A supervised model that finds the faulty instance and then its failure type. Its main idea is that failures spread in groups: a slow instance hurts every caller, every instance on the same host, and its siblings behind a load balancer. It encodes these three group relations as hyperedges and reports better localization than DiagFusion, TVDiag and a supervised DeepHunt variant.

## (c) Problem and motivation
Joint RCL and FTI in microservices (p.1). Motivation: GitHub needed about 1.5 hours to resolve a codespace failure affecting millions (p.1, cited report); group relations (pp.2-3, Fig 1 on Online Boutique). Evidence type: anecdotal plus single-run demonstrations.

## (d) Method
30-second snapshots; per-modality GRUs (3 layers, 256) fused by attention; hypergraph with call, deployment and load-balancing hyperedges; UniGAT-HE with hyperedge-type attention (2 layers, 256); scorer MLP per instance trained with softmax cross-entropy over instances; failure-type classifier trained only after HR@1 exceeds a trigger (theta 0.4, 0.6, 0.7); inference RCL then FTI. 60/40 split.

## (e) Datasets, protocol, leakage
Dataset A: GAIA, 10 instances, 1,099 cases, 5 failure types. Datasets B and C: Online Boutique (489 cases) and Sock Shop (700) deployed by the authors with Chaos Mesh injections of CPU, memory, network and pod faults into each instance, repeated five times (p.7). The 60/40 split is not described as temporal or by instance; with five repeats per injection, near-duplicate cases may straddle train and test. RQ4 re-splits by culprit component (60/40 per failure type).

## (f) Results (copied)
Table I (p.8), HR@1 / HR@3 / Avg@3 / F1 on A, B, C: CCLH 0.875 / 0.950 / 0.920 / 0.941; 0.923 / 0.954 / 0.938 / 0.768; 0.918 / 0.950 / 0.938 / 0.772. TVDiag 0.811 / 0.939 / 0.884 / 0.977; 0.834 / 0.925 / 0.884 / 0.577; 0.832 / 0.904 / 0.877 / 0.505. DiagFusion HR@1 0.465, 0.533, 0.398. DeepHunt (supervised variant) HR@1 0.308, 0.436, 0.441. MicroRCA HR@1 0.207, 0.061, 0.050. Ablation (Table II, p.8): without the hypergraph Avg@3 0.838 / 0.800 / 0.863 and F1 0.860 / 0.449 / 0.555. Time (Table III, p.9, dataset A): training 168.204 s, inference 0.434 s per case. No statistical tests; single runs.

## (g) Limitations and stern critique
Authors: platform events missing; no joint metric; manual theta (pp.9-10). Mine: supervised without label-limited experiments despite arguing few-shot or zero-shot realities; probable case-level leakage; baselines re-run by the authors with the DeepHunt variant far below that method's published numbers; datasets B and C and code not released; dataset A has 10 instances; no variance or tests; "group influence" shown by three single-run demonstrations; TVDiag has the higher F1 on dataset A.

## (h) Reproducibility
No code link. GAIA data repo cited (not opened). B and C not released as far as the text states.

## (i) Head-to-head with our work
Complementary. They model co-location and sibling relations, which are exactly the shared-infrastructure channel that our call-edge model cannot see; we are label-free. They do not forecast. A reviewer will likely ask us why we model only call edges.

## (j) Does it change our problem? Could a reviewer say it exists?
It adds a limitation and an extension to our plan (non-call propagation). It does not touch label-free forecasting.

## (k) Sentences
Safe: "Xie et al. (2025) model call, co-location and load-balancing relations among instances with hyperedges in a supervised RCA model [key]." / "They report HR@1 of 0.875 on the public GAIA dataset [key] (preprint)." Must NOT write: that CCLH is peer reviewed; that it outperforms DeepHunt in general (their variant of DeepHunt is not the published method); that it is label-free; that its datasets B and C are available.

## (l) Things to verify
Code or data release; Figs 1, 5, 6; the OpenRCA reference.
