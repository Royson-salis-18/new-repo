# Report: Sun et al. (2025), DeepHunt: interpretable failure localization with a graph autoencoder

Key `sun2025interpretable`. Structured note: `litdb/papers/sun2025interpretable.md`. Page numbers are PDF pages (article 52:1-28).
Reading coverage: full text read to the last reference. Tables 1-8 read as text. Figures 1-11 were not inspected visually; I rely on text and captions.

## (a) Bibliographic block
- Yongqian Sun, Zihan Lin, Binpeng Shi, Shenglin Zhang, Shiyu Ma (Nankai), Pengxiang Jin (Alibaba), Zhenyu Zhong (Nankai), Lemeng Pan, Yicheng Guo (Huawei), Dan Pei (Tsinghua). "Interpretable Failure Localization for Microservice Systems Based on Graph Autoencoder". *ACM Transactions on Software Engineering and Methodology* 34(2), Article 52, January 2025. DOI 10.1145/3695999. ISSN 1049-331X / 1557-7392. Received 23 Feb 2024, revised 19 Jun 2024, accepted 12 Aug 2024 (p.28).
- Scopus: venue indexed (manual Scopus Sources preview check by ISSN, 2026-10-07; CiteScore 2025 = 11.6, 89th percentile, 53/503 in Software; SJR 2025 shown as 1.59). SJR quartile unknown (no list supplied).
- Peer reviewed: yes, journal with revision round. This is the strongest venue in batch 1.

## (b) Plain-language summary
The method learns what "normal" looks like for each service and host, using a graph neural autoencoder trained on normal operating data only. When a failure happens, services whose measurements are hardest to reconstruct (and, optionally, whose neighbours are also anomalous) rank highest as the culprit. A tiny scorer with about 13 weights combines these signals. It starts working with no labels, and gets better if operators confirm or correct a few cases. On two datasets it finds the true culprit in the top five over 90% of the time.

## (c) Problem and motivation
Problem (p.6): given a detected failure with its time window, return the root-cause instance(s) from trace, log, metric and deployment data. Motivations: label cost (the cited RCLIR work: four experienced operators nearly a month for 1,000 root-cause cases, p.2), distribution shift in changing systems (p.2), lack of interpretability and continual learning (p.3). The AWS December 2021 outage (more than 4 hours to pinpoint cause, p.2) is cited as an example, which is anecdotal. The authors' own 63-case study (p.7) shows reconstruction error alone ranks the root cause first in only about 70% of cases. Motivation is partly measured by others (cited) and partly anecdotal.

## (d) Method (re-implementable)
1. Per minute, build an SBG: nodes = microservice instances plus hosts; edges = observed invocations (traces) and deployment relations.
2. Node features: trace latency, request count and status-code frequencies per callee instance; log template-group counts (Drain parsing, rare templates merged, one series for unseen templates); metric series resampled to 1 minute; all z-scored using a sliding historical window and concatenated (pp.9-10).
3. GAE: GraphSAGE-style layers with neighbor aggregation (Eq.1), one hidden layer, MSE reconstruction on normal data, feature masking for augmentation (pp.10-11, 20).
4. Scoring (Eq.2, pp.11-12): per instance, reconstruction errors over a 10-minute window are mixed by W1 (10 weights, initialized 0.1); self error, max downstream error and max upstream error form a 3-vector; W2 = (alpha, beta, gamma), initial (1, 0, 0), gives the root cause score; rank instances.
5. Feedback (Eq.3): hinge-style ranking loss over fine-tuning cases; fine-tune W1, beta, gamma (alpha frozen) with Adam, initial learning rate 0.01.
Assumptions: failure detected elsewhere; topology from traces and deployment; clean normal data; instance-level (not code-level) root causes.

## (e) Datasets, protocol, leakage
D1: simulated e-commerce system deployed in a real cloud, 46 instances, failures derived from real ones and replayed in May 2022; 210 failures and 3,714 normal samples; five failure types (container hardware, container network, node CPU, disk, memory). D2: commercial bank management system, 18 instances, 133 failures from Jan to Jun 2021, 12,297 normal samples; six types (JVM memory/CPU, container memory/CPU/network/disk); NDA, not public (pp.14-15). The abstract's "two open source datasets" conflicts with the NDA statement. Protocol: GAE trained on normal-period data; failure cases split chronologically 30% (feedback or training) / 70% (test); five repeats averaged (p.16). Not stated: where the normal training data sit in time relative to the test failures. Leakage across failures looks controlled; timing of normal data is unclear.

## (f) Results (copied)
Table 3 (p.17), A@1 / A@3 / A@5 / Avg@5: D1 DeepHunt 0% labels 0.780 / 0.898 / 0.959 / 0.889; 1% 0.795 / 0.905 / 0.966 / 0.894; 25% 0.797 / 0.902 / 0.966 / 0.895; 30% 0.803 / 0.912 / 0.966 / 0.898. D2 0% 0.445 / 0.772 / 0.903 / 0.716; 1% 0.498 / 0.781 / 0.910 / 0.741; 25% 0.783 / 0.935 / 0.944 / 0.900; 30% 0.785 / 0.936 / 0.946 / 0.901. Baselines at 30% labels, D1: DejaVu 0.473 / 0.701 / 0.793 / 0.670; Eadro 0.310 / 0.446 / 0.484 / 0.413; DiagFusion 0.333 / 0.500 / 0.648 / 0.493. D2: DejaVu 0.583 / 0.733 / 0.817 / 0.714; Eadro 0.214 / 0.386 / 0.454 / 0.361; DiagFusion 0.398 / 0.552 / 0.750 / 0.532. Label-free baselines D1 / D2 (A@1 / A@5): MicroHECL 0.091 / 0.386 and 0.068 / 0.414; MicroRank 0.144 / 0.259 and 0.208 / 0.541; AutoMAP 0.279 / 0.729 and 0.128 / 0.421; TraceRCA 0.243 / 0.338 and 0.241 / 0.459; Microscope 0.074 / 0.227 and 0.030 / 0.241; RCD 0.095 / 0.174 and 0.106 / 0.220. Ablations (Table 4, p.18) and Table 7 (fine-tuned W2: D1 beta 0.020, gamma 0.009; D2 beta 0.133, gamma -0.002) in the note. Online time 0.169 s (D1) and 0.262 s (D2); offline training 629.892 s and 1,961.616 s (Table 6, p.20). No significance tests or confidence intervals; stability shown only by box plots over five unseeded repeats.

## (g) Limitations and stern critique
Authors: failure type not determined; small datasets; two datasets cannot represent all systems (pp.22-23). Mine, in order: (1) the label-free version equals averaged reconstruction-error ranking, because the initial scorer disables propagation (p.13); (2) no ablation removes the propagation term, and the learned propagation weights are tiny (Table 7), so "propagation-aware" is not supported as a contributor; (3) D1 is a testbed and D2 is small and proprietary; (4) zero-label performance is strong at A@5 but weak at A@1 on D2 (0.445 at 0% vs 0.783 at 25%); (5) detection and failure time are given; end-to-end detection delay and false alarms are not evaluated; (6) baselines receive 30% labels and original settings, which suits label-hungry deep baselines poorly; (7) test sets are small (my estimate about 93 to 147 failures), no statistics; (8) abstract overstates openness; (9) first-order propagation only.

## (h) Reproducibility
Code: github.com/bbyldebb/DeepHunt exists (checked 2026-10-07 via the GitHub API, last push 2024-02-23, no license file); I did not run it. Data: github.com/bbyldebb/Aiops-Dataset exists, README describes D1 and points to a MEGA file; I did not download it, so its availability is unverified. D2 is not available.

## (i) Head-to-head with our work
DeepHunt is the closest published match to our label-free localization story and it is stronger in method, evaluation and reproducibility. Both train a normal-behaviour model on a clean window and rank by deviation; ours is a lightweight robust-z detector with a call-graph ranking, theirs a GAE. Neither shows propagation modelling adds value. They do not forecast; our cascade-risk claim has no evidence yet. A reviewer will compare us to this paper first.

## (j) Does it change our problem? Could a reviewer say it exists?
It changes our claims: "unlabeled RCA" and "learned propagation without labels" must not be presented as new. A reviewer can say "label-free multimodal graph RCA exists (DeepHunt)". Remaining space: (1) whether propagation structure helps beyond reconstruction-error ranking, tested with a proper ablation on public data; (2) forecasting and early warning; (3) a lightweight, non-deep, trace-only method that works on live systems.

## (k) Sentences
Safe: "DeepHunt (Sun et al. 2025) is a self-supervised, graph-autoencoder-based localizer that needs no labels at cold start and reports A@5 of 0.959 and 0.903 on two datasets without labels." / "Its learned propagation weights after fine-tuning are small." / "Operator labelling of 1,000 root-cause cases was reported to take four experienced operators nearly a month (cited in DeepHunt)." Must NOT write: "no label-free RCA exists"; that DeepHunt requires labels (it does not at cold start); that DeepHunt is not online or "static" (it has an online stage); that DeepHunt models multi-hop propagation or forecasts; that D2 is open; that propagation modelling is proven to help.

## (l) Things to verify
Run the code on D1 and on RCAEval; add a reconstruction-error-only control; check where the normal training window lies; confirm the MEGA link; Figs 1-11; AID's relation to cascading failure (cited here as [51], title about intensity of dependency).
