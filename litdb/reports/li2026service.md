# Report: Li (2026), GNN service dependency modeling and failure propagation prediction

Key `li2026service`. Structured note: `litdb/papers/li2026service.md`. Page numbers are PDF pages.
Reading coverage: full text read to the end (references included). Not read: Algorithm 1 pseudo-code body (p.12, did not extract), Figs 1-4 and 8 (not inspected). Figs 5-7 inspected from extracted images.

## (a) Bibliographic block
- Linling Li (sole author, Yibin Vocational and Technical College, China). "Service dependency modeling and failure propagation prediction in distributed systems based on graph neural networks". *Discover Artificial Intelligence* 6:512 (2026). Publisher: Springer Nature. Open access, CC BY-NC-ND 4.0.
- DOI 10.1007/s44163-026-01213-3 (Crossref-verified). ISSN 2731-0809. Received 21 Oct 2025, accepted 26 Mar 2026 (p.27). 24 references. Crossref cited-by: 0.
- Scopus: venue indexed (manual check on the public Scopus Sources preview, 2026-10-07; CiteScore 2025 = 6.2, 75th percentile, category Computer Vision and Pattern Recognition; SJR 2025 shown as 1.184). SJR quartile: unknown (no list supplied). Indexing is a property of the venue, not of this paper's quality. This is a broad-scope open-access journal with a short review time (about five months).
- Peer-review status: peer-reviewed journal article.

## (b) Plain-language summary
The paper builds a graph neural network that takes service metrics and a dependency graph, tracks how dependency strengths change, and outputs which services are likely to fail next and along which paths. A cascade formula converts predictions into probabilities and an alert score. It reports about 93% F1 on proprietary enterprise data, big gains over simpler methods, and a pilot with large downtime reductions. The argument rests on data and code that are only promised.

## (c) Problem and motivation
The problem (p.3) is predicting P(f_i -> f_j | t) on a weighted graph under topology drift and real-time limits. The motivation (pp.2-3) is generic: microservices are complex, traditional monitoring is reactive. No incident statistics or outage cost data are given, so the motivation is asserted (evidence type: assumed). The claim that no scalable framework for quantified cascade prediction exists is contradicted by earlier work we verified (AID, TNSM 2025, Seer, Sage, MicroHECL), none of which the paper cites.

## (d) Method (enough to re-implement, with gaps marked)
1. Collect metrics (sampling 1/dt) and discover dependencies from logs and API traces (p.4-5).
2. Edge strength w_ij = alpha*f_ij + beta*l_ij + gamma*e_ij (frequency, latency, error rate), alpha 0.4, beta 0.3, gamma 0.3 from grid search on 1000 historical scenarios; non-linear variant with tanh, 1-exp(-l), sigmoid (p.5). Edge update by exponential smoothing (Eq.4, lambda unspecified); Eq.7 and Eq.8 give two other definitions.
3. Node features [cpu, mem, load, resp, err], edge features [lat, thr, freq], sliding-window means, z-score normalisation (pp.7-8).
4. Network: linear embedding (d=128), 3 layers, 8-head GAT aggregation (Eq.14-15), GRU temporal update (Eq.16). Text elsewhere says Transformer encoder plus LSTM with an O(T log T) claim that is not justified for self-attention (p.9).
5. Loss = cross-entropy + beta * pairwise hinge ranking on path importance scores + L2 (Eq.17-20). The labels for path importance are not defined. beta, lambda not given.
6. Cascade layer: noisy-OR P = 1 - prod(1 - p_ki w_ki) (Eq.21); path probability = product of edge propagation and node vulnerability probabilities (Eq.22); impact = weighted criticality, dependency count, load (Eq.23); risk = sum of parent probabilities x impact x time weight (Eq.25); alert when risk above theta (Eq.26). Source of p_ki and vulnerability: not stated. Monte Carlo simulation and dynamic programming are mentioned (Table 4).
7. Complexity O(|V|^2 T + |E| log|V|) (p.12).
Assumptions: labelled failures with propagation sequences, discoverable graph, propagation along dependency edges. Training: Adam, dropout 0.3, patience 15, Bayesian search 50 iterations (pp.14, 17).

## (e) Datasets, faults, protocol, leakage
Three named proprietary sets: EC-2022 (450 services), FS-2023 (280), TC-2023 (650), 6 months to 2 years (pp.12-13), plus synthetic data with injected correlated failures, gradual degradation and cascading timeouts. Number of systems conflicts across the paper (3 named; 8 in Fig 5a; 93 in Fig 5d; 4 scenarios incl. manufacturing on p.21; 5 deployments in Table 9). Labels: failures detected by thresholds (above 95th percentile latency or above 5% error rate), propagation paths annotated by two administrators, kappa 0.84 (p.14). Temporal split 70/15/15 (p.18). Leakage risk: the labelling rule uses latency and error rate, which are also model inputs (Eq.9). The author lists leakage countermeasures (p.24) but they do not address this.

## (f) Results (copied)
Table 7 (p.20): accuracy 0.93 +/- 0.02 vs 0.86 +/- 0.02 (graph-based methods as a group); precision 0.94 vs 0.87; recall 0.92 vs 0.86; detection time 3.2 +/- 0.8 min vs 5.2 +/- 0.9; processing time 45.3 +/- 6.2 ms vs 62.4 +/- 8.7; memory 234.7 vs 267.5 MB. Named strong baselines on p.23: TGN 0.87, GraphMixer 0.86, DySAT 0.85 F1. Graph fault localization F1 0.78 +/- 0.04, compatibility orchestration 0.71 +/- 0.05 (p.21). Ablation (Table 8, p.22): full 0.93; without attention 0.87, temporal 0.84, message passing 0.79, feature engineering 0.71, graph structure 0.76. Incident analysis (Table 10, p.25): 127 incidents, 107 predicted, 76 prevented; average lead time stated as 4.7 minutes. Pilot (Table 9, p.24): downtime reductions 34% to 52%, availability gains +0.06 to +0.22 points. Statistics (p.21): 15 runs per dataset, t-tests, Wilcoxon, a correction labelled Holm-Bonferroni with alpha 0.0025, Cohen's d 1.4 to 2.8.
Figures: Fig 6c accuracy falls from about 0.94 to about 0.81 as horizon grows (text calls it consistently high); Fig 6d path accuracy about 0.94 at 2 hops, 0.89 at 3, 0.68 at 8; Fig 7c processing time axis is in seconds, up to about 9 s at 1500 services; Fig 7e compares with Prometheus, Datadog, New Relic and Dynatrace (detection rate about 0.72 to 0.85 vs 0.93) with no stated protocol.

## (g) Limitations and stern critique
Authors: pilots are observational, configuration errors are hard (pp.23-26). My critique, in order of severity: (1) unverifiable (proprietary data, code only promised); (2) numbers disagree with each other (table in the note: 63.2% vs 38.5% detection-time reduction, 3 vs 8 vs 93 systems, 84% vs 89% correct predictions, 100 ms vs 9 s, deployment scale 450 vs 1,247 services); (3) label circularity (labels from the same signals as features); (4) baselines weak or mismatched, and the strongest ones are reported in prose without a table or protocol; the "graph-based fault localization" baseline is the DeepHunt reference but is described as expert-rule-based, which misstates that method; (5) prediction unit and class balance undefined, no AUROC, AP, calibration; (6) repeated seeds treated as independent samples, Bonferroni labelled Holm; (7) deployment claims lack a control and the "independent audit" is unspecified; (8) related work is thin (24 references, none on propagation prediction in microservices); (9) the text has editorial defects that suggest late patching.

## (h) Reproducibility
No code or data. Article text: code and synthetic generators "will be released on GitHub following publication" (p.26) and anonymised data via institutional agreements (p.13). No URL is given. I did not look for a repository, so release is unverified. Not reproducible as published.

## (i) Head-to-head with our work (rca-lab)
Same target (cascade forecasting) but opposite regimes. They are supervised, GPU-trained, proprietary and claim large wins; we are label-free, open, small and unvalidated on real faults. Their Eq.21 is the same noisy-OR we use, so that component is not ours to claim as novel. Their evaluation looks stronger on paper but is not checkable; ours is checkable but weak (synthetic only, risk equals the prior, 82% of edge probabilities at the prior). Where they are stronger: explicit forecast horizons, a path-ranking objective, scale claims. Where we are stronger: label-free operation, openness, negative controls reported honestly.

## (j) Does it change the problem? Could a reviewer say it exists?
It does not change the problem; it removes the novelty claim "cascade prediction is under-explored", and removes "learned propagation probabilities" as a novelty. A reviewer can legitimately say "cascade-risk forecasting with propagation probabilities exists (Li 2026)". Our defensible differences are label-free, open, and honestly evaluated against structural baselines, and only if our Task B evaluation is done.

## (k) Sentences
Safe: "Prior work has proposed supervised graph neural networks for failure propagation prediction (Li 2026), evaluated on proprietary data that was not publicly released at publication." / "Li (2026) models cascade probability with a noisy-OR style formula over weighted dependencies." / "To our knowledge no open implementation of these methods was available when we wrote this paper." (re-check before submission)
Must NOT write: "Li (2026) achieves 93% F1" without the caveat that it is unverifiable; "no work predicts cascading failures"; "outperforms Li 2026"; any of the conflicting percentages as fact; that Li's method is label-free or self-supervised (only an add-on, p.14); that Li's baseline set includes DeepHunt properly reimplemented.

## (l) Things to verify
GitHub release; Algorithm 1; Figs 1-4, 8; whether ref 22 is the DeepHunt paper (it is cited as Sun et al., ACM TOSEM 2025, "Interpretable failure localization ... graph autoencoder", which is our batch-1 paper 3, `sun2025interpretable`); author contact for the inconsistencies.
