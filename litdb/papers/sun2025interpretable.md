---
key: sun2025interpretable
title: "Interpretable Failure Localization for Microservice Systems Based on Graph Autoencoder (DeepHunt)"
authors: "Sun, Yongqian; Lin, Zihan; Shi, Binpeng; Zhang, Shenglin; Ma, Shiyu; Jin, Pengxiang; Zhong, Zhenyu; Pan, Lemeng; Guo, Yicheng; Pei, Dan"
year: 2025
venue: "ACM Transactions on Software Engineering and Methodology, Vol. 34, No. 2, Article 52"
publisher: "ACM"
doc_type: journal-article
doi: "10.1145/3695999"
issn: "1049-331X, 1557-7392"
scopus_indexing: "indexed (manual check of Scopus Sources preview by ISSN, 2026-10-07; CiteScore 2025 = 11.6, 89th percentile, rank 53/503 Software)"
scopus_match: "ISSN 1049-331X, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied (Scopus preview shows SJR 2025 = 1.59, quartile not displayed)"
peer_reviewed: "yes (received 23 Feb 2024, revised 19 Jun 2024, accepted 12 Aug 2024, p.28)"
cited_by_crossref: ""
n_references: "60"
license: "ACM publication rights licensed; see PDF"
batch: "1"
read_status: reviewed                  # Figs 1-11 not inspected visually (text and all tables read)
pages: 28
text_chars: 101304
metadata_source: crossref
task: "localization (instance-level, given a detected failure)"
supervision: "label-free at cold start (GAE trained on normal data; fixed initial scorer); label-light after operator feedback (ranking loss on labelled failures)"
online_or_streaming: "partly: per-failure online diagnosis in about 0.17-0.26 s (Table 6, p.20); failure detection is out of scope (p.6); minute-level SBGs"
telemetry: "traces, logs (Drain templates, counts), metrics, deployment topology"
propagation_modeling: "GNN (GraphSAGE-style GAE) + first-order upstream/downstream aggregation (max) in the root cause score; no forecasting"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "D1: simulated e-commerce testbed, 46 instances (40 services + 6 VMs); D2: bank management system, 18 instances (proprietary)"
datasets: "D1 (210 failures, 3,714 normal samples; public via GitHub/MEGA), D2 (133 failures, 12,297 normal samples; NDA)"
dataset_open: "partly: D1 yes (https://github.com/bbyldebb/Aiops-Dataset, README links a MEGA file; file not downloaded or verified); D2 no"
code_open: "yes: https://github.com/bbyldebb/DeepHunt (verified exists, last push 2024-02-23, no license file)"
baselines_compared: "MicroHECL, MicroRank, AutoMAP, TraceRCA, Microscope, RCD (non-deep); DejaVu, Eadro, DiagFusion (supervised deep, 30% labels)"
metrics: "A@1, A@3, A@5, Avg@5"
headline_result: "30% labels: D1 A@1 0.803, A@5 0.966, Avg@5 0.898; D2 A@1 0.785, A@5 0.946, Avg@5 0.901 (Table 3, p.17); 0% labels: D1 A@5 0.959, D2 A@5 0.903 (p.17)"
evidence_quality: "3"
relevance_to_us: "5"
overlap_with_us: "high (label-free baseline-window calibration; multimodal; graph; online) except forecasting"
threat_level_for_novelty: "high for 'label-free RCA is new'; low for 'cascade forecasting'"
---

# Interpretable Failure Localization for Microservice Systems Based on Graph Autoencoder (DeepHunt)

> Reading notes written from the **full text** (`litdb/texts/sun2025interpretable.txt`). Page numbers are PDF pages (article pages 52:1-52:28).
> Tables 1-8 were readable as text. Figures 1-11 are images and were not inspected visually; I rely on the surrounding text for them.

## 1. One-paragraph summary
DeepHunt builds a graph per minute (nodes = microservice instances and hosts, edges from calls and deployment, node features = standardized trace, log-template and metric series). A graph autoencoder is trained on normal data only. After a failure is detected, instances are ranked by a small learned "root cause score" built from the reconstruction errors of an instance over a 10-minute window and those of its first-order upstream and downstream neighbors (max-aggregated). The scorer starts from fixed weights (no labels needed) and can be fine-tuned from operator feedback with a ranking loss. On two datasets it reports A@5 above 0.9 even with 0% to 1% labels and beats nine baselines.

## 2. Problem and motivation
- Problem: localize root-cause instances in microservice systems from multimodal data with few labels, with interpretable scores and continual improvement (pp.1-4).
- Evidence offered: AWS December 2021 incident took more than 4 hours to pinpoint the root cause (p.2, citing the AWS summary [4]); the cited RCLIR work reports that labelling 1,000 root-cause cases takes four experienced operators nearly a month (p.2, [6]); frequent system change causes distribution shift (p.2). A small empirical study of 63 failure cases from an e-commerce system shows reconstruction error alone puts the root cause in the top five in most cases but not first in about 30% (p.7, Fig 3). Evidence type: anecdotal / cited, not measured by the authors except the 63-case study.
- Real? The label-cost motivation is directly relevant to our label-free framing; the propagation motivation is partly supported by the authors' own observation (p.7-8).

## 3. Method
- Data model: System Behavior Graph (SBG) per minute; nodes = instances; edges = invocation (traces) plus deployment; features = z-scored (sliding historical window) trace series (latency, request count, status codes), log template-group counts via Drain (rare templates merged, a new-template series), metric series interpolated to 1 min (pp.9-10).
- GAE (pp.10-11): encoder and decoder of GraphSAGE-like layers (Eq.1, mean aggregator, concatenate, normalize, LeakyReLU); trained with MSE on SBGs from normal uptime; data augmentation by random feature masking (Noise_Rate, Fig 10); 1 hidden layer (p.20).
- Root cause scorer (pp.11-13): reconstruction errors over a window (Window_Size = 10) are combined by a fully connected layer W1 (initialized to 0.1 each); a graph layer takes [self error, max over downstream neighbours, max over upstream neighbours] (Eq.2); a second layer W2 = (alpha, beta, gamma) gives the score; initial W2 = (1, 0, 0) so the cold-start score ignores propagation (p.13, Table 1).
- Feedback (pp.13-14): operators confirm or correct root causes; fine-tune W1, beta, gamma (alpha frozen, p.21) with a ranking loss L_s = - (1/N) sum_j sum_i max{RS_j^(i) - RS_j . Y_j, 0} (Eq.3), Adam, initial learning rate 0.01, early stopping.
- Assumptions: failure already detected and its time window known; topology from traces and deployment; clean normal data available for GAE training.
- Hyper-parameters: Window_Size 10, layers 1, learning rate 0.01 for fine-tuning, others in Fig 10 (p.20-21).

## 4. Data and setup
- D1: simulated e-commerce system deployed in a real cloud; 46 instances (40 microservice, 6 VM); user traffic patterned on real business; failure cases derived from real failures and replayed in batches; Table 2: 3,714 normal, 210 failure, 44.9 M trace, 66.6 M log, 20.9 M metric records; failure types: container hardware, container network, node CPU, node disk, node memory (pp.14-15). Public via GitHub README (MEGA link).
- D2: management system of a commercial bank, 18 instances (web, application servers, databases, dockers); failures Jan to Jun 2021 labelled by two operators with cross-check; Table 2: 12,297 normal, 133 failure, 214.3 M trace; types JVM memory, JVM CPU, container memory, CPU, network, disk; used in the International AIOps Challenge 2022; **not public (NDA)** (p.15).
- Note a contradiction: the abstract says two open-source datasets (p.1), but D2 is not available (p.15).
- Protocol: normal-period data trains the GAE; failure cases split chronologically, first 30% as feedback/training and last 70% as test (p.16). Each experiment repeated five times, averaged (p.16). Baselines configured with original settings (p.15) and given 30% labels (p.17).
- Leakage: failure split is chronological (good). Not stated: whether the GAE's normal training data precede all test failures; timing of normal-data windows.
- Hardware: 12x Xeon E5-2650 v4, 128 GB, no GPU (p.16).

## 5. Results (copied; Table 3, p.17)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| D1 A@1 / A@5 / Avg@5 at 30% labels | 0.803 / 0.966 / 0.898 | 0.473 / 0.793 / 0.670 | DejaVu (30%); best non-deep AutoMAP 0.279 / 0.729 / 0.531 | Table 3 |
| D2 A@1 / A@5 / Avg@5 at 30% labels | 0.785 / 0.946 / 0.901 | 0.583 / 0.817 / 0.714 | DejaVu (30%) | Table 3 |
| D1 at 0% labels (A@1, A@3, A@5, Avg@5) | 0.780, 0.898, 0.959, 0.889 | n/a | n/a | Table 3 |
| D2 at 0% labels | 0.445, 0.772, 0.903, 0.716 | n/a | n/a | Table 3 |
| D1 / D2 at 1% labels A@5 | 0.966 / 0.910 | n/a | n/a | Table 3 |
| Improvement claim at 30% | A@5 gain between 16% and 455% | n/a | n/a | p.16 |
| Online / offline time | 0.169 s / 629.892 s (D1); 0.262 s / 1,961.616 s (D2) | DejaVu online 0.318 s (D1), 0.192 s (D2) | n/a | Table 6, p.20 |

- Statistics: five repeats averaged, box plots of stability (Fig 9); no significance tests, no confidence intervals. Test set sizes about 147 failures (D1) and about 93 (D2) if 70% of 210 and 133 (my arithmetic, not stated).
- Ablations (Table 4, p.18; D1 / D2, A@1): full 0.795 / 0.498; C1 no augmentation 0.759 / 0.426; C2 non-GNN AE 0.488 / 0.447; C3 no feedback 0.780 / 0.445; C4 random forest scorer 0.544 / 0.138; C5 DejaVu loss 0.776 / 0.432.
- Dynamic instances (Table 5, p.19): removing 20% of training instances changes D1 A@1 from 0.795 to 0.788 and D2 0.498 to 0.473.
- Fine-tuned propagation weights (Table 7, p.22): D1 beta = 0.020, gamma = 0.009; D2 beta = 0.133, gamma = -0.002 (alpha fixed at 1.000).
- Efficiency: online under 1 s (p.19).

## 6. Limitations
- Stated (pp.22-23): cannot determine failure type; datasets small; two datasets cannot represent all systems.
- **My critique:**
  1. The label-free variant is essentially "rank instances by mean GAE reconstruction error over the window": initial W2 = (1, 0, 0) turns propagation off (p.13). The propagation term is learned only from feedback, and its learned weights are tiny (Table 7). No ablation isolates the propagation term (C1-C5 do not remove it); so the paper does not show that propagation awareness helps.
  2. D1 is a simulated testbed with replayed failures; D2 is small (18 instances) and proprietary; fault types are resource and container faults, not logic bugs.
  3. A zero-label gap exists at A@1: on D2 A@1 is 0.445 at 0% labels but 0.783 at 25% (Table 3); the "zero-label" success is mostly A@5.
  4. Localization is given the failure and its time window; detection is out of scope (p.6), so end-to-end diagnosis latency and false alarms are not evaluated.
  5. Baselines are run at 30% labels from "original settings"; supervised baselines such as Eadro and DiagFusion are designed for much more data, which flatters DeepHunt. No tests.
  6. Test-set sizes are small (my estimate about 93 to 147), so differences of a few points are within noise; five repeats vary only the initialization.
  7. The abstract's claim of "two open source datasets" is contradicted on p.15.
  8. Only first-order propagation is modelled; no multi-hop or forecasting.
- Not discussed: how the GAE's normal-training period relates to the test failures (leakage), threshold-free evaluation on failures with several simultaneous root causes, shared-infrastructure faults.

## 7. Reproducibility
- Code: https://github.com/bbyldebb/DeepHunt exists (API check 2026-10-07; last push 2024-02-23; main.py, models/, utils/, config/, data/, res/; no license file). Not run.
- Data: https://github.com/bbyldebb/Aiops-Dataset README describes D1 and links a MEGA file (not downloaded; availability unverified). D2 unavailable.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | zero-label cold start; GAE on normal data; optional feedback | label-free calibration on a baseline window | Essentially the same idea; theirs is deep-learned and evaluated on two datasets |
| Live / streaming | per-failure online localization after detection (0.2 s); minute graphs | incremental windows | Comparable; theirs has measured latency |
| Telemetry used | traces, logs, metrics, deployment | traces (+ optional metrics, SSH docker) | Theirs |
| Propagation modelling | first-order upstream/downstream max aggregation, weights mostly near zero | edge probabilities, mostly prior | Neither shows propagation helps; theirs is honest about tiny weights |
| Forecasts future failures | no | risk score, untested | Neither evaluated; we claim it, they do not |
| Explanation | W1/W2 weights, heatmaps (Fig 11) | template text | Theirs |
| Evaluation rigor | two datasets, nine baselines, 5 repeats, no tests | synthetic only | Theirs |
| Open / reproducible | code and one dataset | yes | Comparable |

- **What they have that we do not:** a published, peer-reviewed, label-free-capable multimodal localizer with baselines and open code and data (D1).
- **What we have that they do not:** cascade-risk forecasting intent, lightweight non-deep calibration, live Jaeger and SSH adapters.
- **Could a reviewer say "this already exists"?** Yes for "label-free RCA on live telemetry by training on normal data" (zero-label cold start) and for "interpretable scorer with learned propagation weights". No for forecasting.
- **Position:** "DeepHunt (Sun et al. 2025) already ranks root-cause instances without labels using GAE reconstruction errors; we study whether propagation structure adds value beyond that, and whether it supports early warning."
- **Must we run it as a baseline?** Yes, strongly (code and D1 open); a reconstruction-error-only variant is also a necessary control. Needs deep-learning environment (DGL, PyTorch); not on this PC given App Control limits noted in the review.

## 9. Does this paper change what problem we should solve?
- It shows that label-free (zero-label) RCA with multimodal data already exists and works at A@5 above 0.9 on two datasets. Our novelty cannot be "unlabeled RCA".
- It shows (Table 7, Table 4) that the propagation term contributes little in the learned model, matching our synthetic finding that cascade terms add nothing. This supports reframing as a study of whether propagation modelling helps.
- It provides evidence that labelling cost is a real barrier (cited numbers, p.2).

## 10. Citation-ready facts (each with page)
- DeepHunt trains a graph autoencoder on normal data and ranks instances by a learned root cause score combining reconstruction error with first-order upstream/downstream errors (pp.11-12).
- With no labels it reports A@5 of 0.959 (D1) and 0.903 (D2); with 30% labelled failures A@5 0.966 and 0.946 (Table 3, p.17).
- Its fine-tuned propagation weights are small (D1 0.020 and 0.009; D2 0.133 and -0.002) (Table 7, p.22).
- Labelling 1,000 root-cause cases was reported (via RCLIR [6]) to take four experienced operators nearly a month (p.2).
- Code and one dataset (D1) are public; the second (bank) dataset is not (p.15).

## 11. Open questions / things to verify
- Whether the MEGA file for D1 is still available; whether the repo reproduces Table 3.
- Whether D2 (AIOps Challenge 2022 data) can be obtained.
- AID [51] is cited here as a trace-based dependency-intensity prediction work (title: prediction of aggregated intensity of dependency); verify against its full text whether it concerns cascading failures at all before using it as "cascade prediction" prior art.
- Figs 1-11 not viewed.
