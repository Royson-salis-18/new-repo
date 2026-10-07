# Report: Liu et al. (2024), Cost-Sensitive Mamba Sequence Modeling for Fault Detection

Key `costsensitiv`. Note: `litdb/papers/costsensitiv.md`. Page numbers are PDF pages.
Coverage: full text read (11 pages); Figs 1-4 not inspected; dataset README read via the GitHub API.

## (a) Bibliographic block
Zhaocheng Liu (Northeastern), Ru Meng (CMU), Shao-yu Huang (Duke), Zeyu Huang (UC Irvine, corresponding). Transactions on Computational and Scientific Methods, Vol. 4, No. 12, 2024, Pinnacle Science Press, ISSN 2998-8780. No DOI printed. Scopus: ISSN not found in the Sources preview on 2026-10-07 (0 results). SJR unknown. Peer review: unclear; no dates in the PDF. This is the same journal family cited by the Graph Neural AI preprint (batch 4) for several of its references.

## (b) Plain-language summary
A neural model reads windows of service metrics and says whether the window contains an anomaly; it is trained with extra weight on anomalies. It claims better precision, recall and calibration than seven earlier methods on a small public metrics dataset.

## (c) Problem and motivation
Rare faults, class imbalance and asymmetric error costs in microservice anomaly detection (pp.1-3). No incident data, no cost data. Evidence type: assumed.

## (d) Method
Windows of length 128, stride 16, OR-aggregated labels; Mamba-style gated state-space recurrence with 4 layers, hidden 256; sigmoid anomaly probability; weighted cross-entropy with weights 5.0 (anomaly) and 1.0 (normal); alarm threshold 0.5; AdamW at learning rate 1e-3, 100 epochs, seed 42 (Table 1, pp.6-7).

## (e) Datasets, protocol, leakage
RS-Anomic (RobotShop, 12 services, ten anomaly types). The dataset README reports 100,464 normal and 14,112 anomaly instances (about 12% anomalous) and test ratios of 95:5, 90:10, 60:40. The paper calls this "extreme class imbalance", gives no counts, ratio or split and uses windows that overlap strongly (128 with stride 16), so a random split would leak.

## (f) Results (copied)
Table 2 (p.7): proposed model precision 0.93, recall 0.89, F1 0.91, AUROC 0.98, AUPRC 0.96, ECE 0.021, Brier 0.062, alarm rate 0.20; best baseline (Cheng et al., CAPAD 2025) 0.90, 0.86, 0.88, 0.96, 0.93, 0.029, 0.076, 0.23; other baselines F1 from 0.81 (Liu 2020) to 0.87 (Wang 2025). No variance or tests; no implementation details for any baseline.

## (g) Limitations and stern critique
Unverifiable baselines (no details or code) with a suspiciously smooth ranking; "cost-sensitive" means a 5:1 class weight with no cost measurement; imbalance claim contradicts the dataset's 12% anomaly share; leakage risk; single run; detection only and on known injected anomaly types; metrics only; code not linked; venue not found in Scopus preview.

## (h) Reproducibility
Dataset repository exists (github.com/ms-anomaly/rs-anomic, no license, last push 2023-06-22; not downloaded). No code for this paper.

## (i) Head-to-head with our work
No overlap in task. A transferable point is reporting calibration (ECE, Brier) and alarm rate for risk outputs, which we plan to do for Task B.

## (j) Does it change our problem? Could a reviewer say it exists?
No.

## (k) Sentences
Safe (if at all): "Class-weighted sequence models have been applied to window-level microservice anomaly detection on the RS-Anomic dataset (Liu et al. 2024)." Must NOT write: its comparison numbers as evidence of state of the art; that it addresses rare faults in production; that it performs RCA.

## (l) Things to verify
Split and ratio used; whether any baseline was run; Figs 1-4; venue status.
