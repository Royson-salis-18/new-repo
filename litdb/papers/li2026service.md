---
key: li2026service
title: "Service dependency modeling and failure propagation prediction in distributed systems based on graph neural networks"
authors: "Li, Linling"
year: 2026
venue: "Discover Artificial Intelligence"
publisher: "Springer Science and Business Media LLC"
doc_type: journal-article
doi: "10.1007/s44163-026-01213-3"
issn: "2731-0809"
scopus_indexing: "indexed (manual check of Scopus Sources preview by ISSN, 2026-10-07; CiteScore 2025 = 6.2, 75th percentile)"
scopus_match: "ISSN 2731-0809, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied (Scopus preview shows SJR 2025 = 1.184, quartile not displayed)"
peer_reviewed: "yes (journal; received 21 Oct 2025, accepted 26 Mar 2026, p.27)"
cited_by_crossref: "0"
n_references: "24"
license: "CC BY-NC-ND 4.0"
batch: "1"
read_status: reviewed                  # Algorithm 1 pseudo-code body not extractable (p.12); Figs 1-4, 8 not inspected visually
pages: 27
text_chars: 77492
metadata_source: crossref
task: "cascade-forecast (failure propagation prediction + path ranking + impact scoring)"
supervision: "supervised (cross-entropy on failure labels, Eq.17); a self-supervised pre-training extension is mentioned in one paragraph (p.14)"
online_or_streaming: "claimed yes (Kafka streaming, incremental updates, 2.3 s prediction-to-alert, p.11); no end-to-end live evaluation shown"
telemetry: "service logs, API-call traces, resource metrics (CPU, memory, load, response time, error rate), configuration files"
propagation_modeling: "GNN (GAT + GRU/Transformer/LSTM) plus noisy-OR cascade formula (Eq.21) and path probability product (Eq.22)"
forecasts_future_failures: "yes (horizons 5 min to 24 h claimed, p.18; Fig.6c)"
llm_used: "no"
systems_evaluated: "three named proprietary datasets EC-2022 (450 services), FS-2023 (280), TC-2023 (650) (p.12-13) plus synthetic data; Fig.5 shows 8 systems; Table 9 lists 5 deployments; counts inconsistent"
datasets: "proprietary, anonymized; synthetic generator"
dataset_open: "no (promised 'through institutional data sharing agreements', p.13)"
code_open: "no (promised 'on GitHub following publication', p.26; link not given; release unverified)"
baselines_compared: "rule-based, statistical correlation, SVM, RF, LSTM, GraphSAGE, GAT, GCN, TGN, graph-based fault localization (= ref 22, which is DeepHunt/Sun 2025), compatibility orchestration (ref 21), Prometheus+Grafana, Datadog APM; DySAT/GraphMixer quoted p.23"
metrics: "precision, recall, F1, accuracy, Jaccard of propagation sequence, MAE of propagation time, latency, memory, detection time"
headline_result: "P 0.94, R 0.92, accuracy 0.93, detection time 3.2 min vs 5.2 best graph baseline (Table 7, p.20); abstract: 94.1% P, 92.3% R, 93.2% F1, detection time -63.2%"
evidence_quality: "2"
relevance_to_us: "5"
overlap_with_us: "high (task); low (method: supervised GNN, proprietary data)"
threat_level_for_novelty: "medium (high as a citation a reviewer will raise; low as evidence)"
---

# Service dependency modeling and failure propagation prediction in distributed systems based on graph neural networks

> Reading notes written from the **full text** (`litdb/texts/li2026service.txt`) and from the figure images of pp.13, 19, 20 extracted from the PDF.
> Not inspected visually: Figs 1-4 (architecture drawings), Fig 8 (ablation chart), and the body of Algorithm 1 (p.12: the pseudo-code lines did not extract, only its complexity paragraph).

## 1. One-paragraph summary
A single-author paper proposes a graph neural network that ingests per-service metrics and a dependency graph, updates edge weights over time, and predicts which services will fail next and along which propagation paths. A noisy-OR style formula and a path-probability product turn the network's output into cascade probabilities and a risk score. It reports F1 about 0.93 on proprietary enterprise datasets plus synthetic data, large margins over classical, ML and graph baselines, and a pilot deployment with large downtime reductions. Data and code are promised but not available, and many numbers conflict with each other.

## 2. Problem and motivation
- Problem statement (p.3): given a dependency graph with strengths, predict P(f_i -> f_j | t) that a failure spreads from i to j within time t, under topology change and real-time constraints.
- Motivation evidence offered: none measured. The introduction (pp.2-3) cites general microservice literature and asserts that frameworks for quantified cascade prediction "remain absent". No incident statistics, no cost-of-outage data.
- Real? Motivation is generic and asserted. The claimed gap is not true (AID, TNSM 2025 GNN forecasting, Seer, Sage, MicroHECL exist; see docs/REVIEW_REPORT.md section 3.2), and the paper cites none of them.

## 3. Method
- Pipeline: telemetry collection (sampling rate 1/dt, Eq.1) -> dependency discovery from logs/API traces -> edge strength w_ij from frequency, latency, error rate (Eq.2; alpha=0.4, beta=0.3, gamma=0.3 chosen by grid search maximizing F1 on 1000 historical failure scenarios, p.5; a sigmoid/tanh variant also given) -> exponentially smoothed temporal edge update (Eq.4; a different update in Eq.8 and a reliability-weighted definition in Eq.7) -> node features CPU, memory, load, response time, error rate (Eq.9), edge features latency, throughput, frequency (Eq.10) -> z-score normalisation (Eq.12) -> input embedding (Eq.13) -> GAT message passing (Eq.14-15) -> temporal GRU (Eq.16), also described as Transformer encoder plus LSTM -> losses: cross-entropy (Eq.17), pairwise hinge ranking on "path importance scores" (Eq.18), L2 (Eq.19), total (Eq.20).
- Cascade layer (pp.10-11): "discrete-time Markov process"; Eq.21 gives P(i fails) = 1 - product over parents k of (1 - p_ki * w_ki), which is the standard noisy-OR / independent-cascade form; Eq.22 path probability = product of edge propagation probabilities times node vulnerabilities; impact score Eq.23 = weighted criticality, dependency count, load; risk score Eq.25 sums parent-failure probability times impact times a temporal weight; alert if risk > threshold (Eq.26). How the base probabilities p_ki are obtained is not stated.
- Hyper-parameters (Table 6, p.17): embedding 128, 3 hidden layers, 8 heads, Adam with weight decay, dropout 0.3, early-stopping patience 15, PyTorch 1.12.0, PyG 2.1, A100 40 GB. Bayesian search of 50 iterations, 24 GPU-hours per method (p.14).
- Assumptions: labelled historical failures with propagation sequences; dependency graph discoverable from traces/logs; failures propagate along dependency edges.

## 4. Data and setup
- Systems: EC-2022 (450 services, 2.3 M API calls/day), FS-2023 (280 services, 890 K transactions/day), TC-2023 (650 services, 5.1 M events/day) (pp.12-13); 6 months to 2 years of data. Fig.5a (p.13) shows 8 systems from about 50 to about 1340 services; Fig.5d shows 93 systems by dependency complexity; Table 9 (p.24) has 5 deployments with different service counts (1,247; 589; 2,134; 856; 423). These do not reconcile.
- Faults: real historical failures; synthetic injection with 30% correlated failure probability, gradual degradation over 5-15 min, cascading timeouts (p.13). Claimed 89% similarity to "Netflix Simian Army patterns" without defining the measure.
- Ground truth (p.14): failure events auto-detected by threshold (above 95th percentile latency or above 5% error rate), then two administrators annotate propagation paths, kappa = 0.84.
- Split: temporal 70/15/15 (p.18); leakage-prevention list on p.24.
- Hardware: A100 training; inference 100 +/- 18 ms (p.21-22).

## 5. Results (copied from the paper)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Accuracy | 0.93 +/- 0.02 | 0.86 +/- 0.02 | "Graph-based methods" (aggregate) | Table 7, p.20 |
| Precision / Recall | 0.94 / 0.92 | 0.87 / 0.86 | same | Table 7, p.20 |
| Detection time (min) | 3.2 +/- 0.8 | 5.2 +/- 0.9 | same | Table 7, p.20 |
| Processing time (ms) | 45.3 +/- 6.2 | 62.4 +/- 8.7 | same | Table 7, p.20 |
| F1 vs named strong baselines | 0.93 | TGN 0.87, GraphMixer 0.86, DySAT 0.85 | p.23 (not in Table 5 or Fig 7a) | p.23 |
| F1 of graph fault localization / compatibility orchestration | n/a | 0.78 +/- 0.04 / 0.71 +/- 0.05 | refs 22 / 21 | p.21 |
| Path accuracy | above 94% for 2-3 hop paths (text, p.19); Fig 6d reads about 0.94 at 2 hops, about 0.89 at 3, about 0.68 at 8 | n/a | n/a | p.19, Fig 6d |
| Historical incidents | 127 incidents; correctly predicted 107 (sum of Table 10); prevention success 76 | n/a | n/a | Table 10, p.25 |
| Pilot deployment | downtime -47% (e-commerce), availability 99.91 -> 99.97% (financial) | n/a | before/after, no control | p.24, Table 9 |

- Statistics: n = 15 runs per dataset (5 seeds x 3 time periods) x 4 scenarios; paired t-tests, Wilcoxon, "Holm-Bonferroni" with adjusted alpha 0.0025 (= 0.05/20, which is plain Bonferroni), Cohen's d 1.4 to 2.8 (p.21). Seeds and time periods of the same data are not independent samples.
- Ablation (Table 8, p.22): removing attention 0.87, temporal 0.84, message passing 0.79, feature engineering 0.71, graph structure 0.76 (full 0.93).
- Efficiency: text says 64.5% processing-time and 43.1% memory reduction versus traditional methods (p.20); Table 7 gives 156.3 -> 45.3 ms (about 71%) and 387.2 -> 234.7 MB (about 39%); against the best graph baseline the improvements are 27.4% and 12.3%. Fig 7c shows processing time in seconds (about 9 s at 1500 services), while p.21 states 100 ms total latency.

## 6. Limitations
- Stated by authors: deployment results are observational, not controlled (pp.23-26); config errors and external dependencies are hardest.
- **My critique:**
  1. Nothing can be checked: proprietary data, code "will be released" (still a promise at acceptance, p.26). Release is unverified.
  2. Internal inconsistencies (see below) mean at least some reported numbers are wrong or come from different runs.
  3. Label circularity: ground-truth failure events come from latency and error-rate thresholds (p.14), and response time and error rate are input features (Eq.9). The model may be learning to reproduce the labelling rule.
  4. The "baselines" are weak or oddly constructed: compatibility orchestration, designed for version conflicts, is scored zero outside configuration failures (p.21); the "graph-based fault localization" baseline is ref 22, which is DeepHunt (Sun et al., TOSEM 2025), described in Table 5 as expert-rule-based, which does not match that paper's graph-autoencoder method. No MicroRCA, AID, Seer, or any propagation-prediction work. Strong baselines (TGN, DySAT, GraphMixer) appear only in one paragraph.
  5. Metric undefined: unit of a prediction (service-window? incident?) is not stated, no class balance, no AUROC/AP/Brier, lead time only as an average of 4.7 min.
  6. Text says performance stays "consistently high" over horizons (p.18) but Fig 6c falls to about 0.81 at the longest horizon.
  7. Pilot deployment: five environments in Table 9 versus three in the text; satisfaction scores; "independent reliability audits confirm" with no detail (p.24).
  8. The text reads as patched after review (numerous "as shown in the above analysis" captions, an ungrammatical sentence on p.16). That is an observation about editorial quality only.
- Threats not discussed: label leakage through the detection rule; model trained on incident periods; shared-infrastructure causes; repeated incidents from one root cause across splits (they claim deduplication, p.24).

### Internal inconsistencies found (so we do not copy any of these numbers)
| Item | Value A | Value B |
|---|---|---|
| Detection time reduction | abstract/conclusion: 63.2% | Table 7: 38.5% vs graph methods (about 74% vs traditional) |
| Processing latency reduction | abstract 64.5% | Table 7: 27.4% vs graph (about 71% vs traditional) |
| Latency | 45.3 ms (Table 7) | 100 +/- 18 ms (p.21); about 9 s at 1500 services (Fig 7c) |
| Number of systems | 3 named datasets (p.12) | 8 systems (Fig 5a), 93 systems (Fig 5d), 5 deployments (Table 9); 4 scenarios incl. manufacturing (p.21) |
| Deployment scale | EC 450 / FS 280 / TC 650 services (p.24 text) | 1,247 / 589 / 2,134 (Table 9) |
| Correct predictions | Table 10 sums to 107 of 127 (84%) | text: 89% successful prediction (p.25) |
| Prevention | Table 10: 76 of 127 (60%) | text: preventive interventions in 76% of cases; 73% success (pp.25-26) |
| 3-hop path accuracy | text: above 94% for 2-3 hops | Fig 6d: about 0.89 at 3 hops |

## 7. Reproducibility
- Code/data: none available. Verified only that the article states a future GitHub release (p.26) and data sharing "through institutional data sharing agreements" (p.13). I did not search for a repository; release is **unverified**.
- Missing: datasets, label definitions per metric, p_ki estimation, Algorithm 1 details, the splits, seeds.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | needs labelled failures and propagation sequences (supervised) | label-free calibration on baseline window | Ours is lighter; theirs is a different problem setting |
| Live / streaming | claims Kafka streaming, 2.3 s alert latency; no end-to-end proof | incremental windows, offline-evaluated | Neither proven; theirs claims more |
| Telemetry used | metrics + logs + API traces | traces (+ optional Prometheus/Loki, SSH docker) | Comparable |
| Propagation modelling | GAT + temporal net, plus noisy-OR with weights | edge probabilities, mostly prior | Theirs is richer on paper; same cascade formula as ours (noisy-OR) |
| Forecasts future failures | yes, with horizons | risk score, untested vs structural | They claim and evaluate (weakly); we do not evaluate at all |
| Explanation | none beyond path visualisation | template; LLM layer not built | Ours slightly ahead on intent only |
| Evaluation rigor | proprietary, inconsistent, circular labels, but reports tests and CIs | synthetic only | Theirs has more real-data claims; ours is more honest and reproducible |
| Open / reproducible | no | yes | Ours |

- **What they have that we do not:** a stated forecasting task with horizons, a path-ranking objective, claimed real-system data and a deployment story.
- **What we have that they do not:** no labels required, runnable open code, honest negative controls (ablations show cascade term adds nothing on synthetic data).
- **Could a reviewer say "this already exists"?** Yes for the claim "predicting cascade risk / propagation paths with a GNN"; and our noisy-OR cascade-risk is the same functional form as their Eq.21. Not for label-free operation.
- **How we must position:** "Li (2026) proposes a supervised GNN for cascade prediction evaluated on proprietary data that is not available; we study a label-free alternative and evaluate it openly."
- **Must we run it as a baseline?** Cannot: no code or data. Cite as unverifiable prior work; a reimplementation would have unspecified components (p_ki, labels).

## 9. Does this paper change what problem we should solve?
- It confirms that cascade prediction is an active claim, and removes any "no one does this" framing.
- It does not give credible evidence that the problem is solved: numbers cannot be checked and conflict internally. The open niche is therefore "an open, label-free, honestly evaluated cascade-risk forecaster against structural baselines".
- Evidence for the problem being real: none measured (only assertion; deployment gains are uncontrolled and unaudited as presented).

## 10. Citation-ready facts (each with page)
- Li (2026) formulates failure-propagation prediction as estimating P(f_i -> f_j | t) on a weighted dependency graph (p.3).
- It uses a GAT with temporal recurrence and a path ranking loss (pp.8-10) and a noisy-OR style cascade formula (Eq.21, p.10).
- Reports F1 about 0.93 on proprietary datasets of 280 to 650 services (Table 7 p.20; datasets pp.12-13); data and code were not available at publication (pp.13, 26).
- The study's own pilot deployments are described by the author as observational and not controlled (p.26).

## 11. Open questions / things to verify
- Whether the promised GitHub repository exists now (not checked).
- Which of the conflicting figures (e.g., 63.2% vs 38.5%) is correct; the author could be asked.
- Whether the baseline labelled "Graph-based fault localization" really is DeepHunt (ref 22 is its citation) and how it was adapted.
- Algorithm 1 pseudo-code (p.12) and Figs 1-4, 8 not read.
