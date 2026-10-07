---
key: yao2024chain
title: "Chain-of-Event: Interpretable Root Cause Analysis for Microservices through Automatically Learning Weighted Event Causal Graph"
authors: "Yao, Zhenhe; Pei, Changhua; Chen, Wenxiao; Wang, Hanzhang; Su, Liangfei; Jiang, Huai; Xie, Zhe; Nie, Xiaohui; Pei, Dan"
year: 2024
venue: "FSE Companion '24: Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering (Porto de Galinhas, Brazil)"
publisher: "ACM"
doc_type: proceedings-article
doi: "10.1145/3663529.3663827"
issn: "none (ACM proceedings, ISBN 9798400706585)"
scopus_indexing: "unverified (proceedings volume has no ISSN; Scopus title search in the preview did not work reliably; see litdb/reference/scopus_checks.md)"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes, conference companion volume; track not stated in the PDF; received 2024-02-08, accepted 2024-04-18 (p.13)"
cited_by_crossref: ""
n_references: "45"
license: "CC BY 4.0"
batch: "1"
read_status: reviewed                  # Appendix A (error-bound proof) is cited in the text but is not in the PDF; Figs 1-3 are diagrams and were not inspected visually
pages: 13
text_chars: 79155
metadata_source: crossref
task: "localization (event-level root cause ranking within a known incident)"
supervision: "supervised (trained on historical incidents with root-cause event labels from SRE tickets, p.6)"
online_or_streaming: "no (incident-time inference; periodic retraining suggested, p.9)"
telemetry: "events derived from metrics, logs, traces, and operation activities (code deployment, config change)"
propagation_modeling: "learned weighted event-causal graph; random-walk-style chain scoring with absorbing 'self-cause' term"
forecasts_future_failures: "no"
llm_used: "no (BERT embeddings used only for GNN baselines)"
systems_evaluated: "one proprietary e-commerce system (eBay-affiliated authors; 'global top-5', over 5,000 services)"
datasets: "Service dataset (170 incidents) and Business dataset (782 incidents), Jan 2020 to Apr 2021; proprietary"
dataset_open: "no"
code_open: "yes: https://github.com/NetManAIOps/Chain-of-Event (verified HTTP 200, last push 2024-05-06; minimal README, no license file, no data)"
baselines_compared: "PageRank, GCN, GraphSAGE, GAT, Groot (with and without manual graph), CoE with manual graph"
metrics: "top-1 and top-3 accuracy"
headline_result: "Service: top-1 79.3%, top-3 98.8%; Business: top-1 85.3%, top-3 96.6% (Table 2, p.10)"
evidence_quality: "2"
relevance_to_us: "4"
overlap_with_us: "partial (event-level propagation weights; but supervised and not forecasting)"
threat_level_for_novelty: "low (for forecasting); medium (for 'learned causal weights between events')"
---

# Chain-of-Event: Interpretable Root Cause Analysis for Microservices through Automatically Learning Weighted Event Causal Graph

> Reading notes written from the **full text** (`litdb/texts/yao2024chain.txt`). Page numbers are PDF pages (ACM cover page is p.1; paper pp.2-13).
> Not read: Appendix A (cited at pp.8 as proof of the approximation bound; the PDF has no appendix). Figs 1-3 not inspected visually.

## 1. One-paragraph summary
CoE turns metrics, logs, traces and operator actions into discrete events (what, when, where) and ranks the events of an incident by root-cause score. It builds a naive graph linking events within the same service (bidirectional) and in adjacent services (direction follows calls), then scores events by summing contributions of event chains. The chain contribution multiplies a start-event importance, per-hop "caused-by" weights, a not-caused-by-anything term and a length bonus. The weights (per event-type pair, split into intra-service and inter-service tables, plus a per-event-type importance vector) are learned by gradient descent so that the labelled root-cause event gets the highest score. On two proprietary e-commerce datasets it reports 79.3% top-1 / 98.8% top-3 (Service) and 85.3% / 96.6% (Business).

## 2. Problem and motivation
- Problem: event-level RCA for microservices that (C1) fuses multi-modal data, (C2) is interpretable and aligned with SRE experience, (C3) needs no manual configuration (pp.3, 4).
- Evidence for the problem: general statements that incidents have large business impact (cites [2,6,26,29,30], mostly general microservice references) and that RCA is the hard step for SREs (p.2). No numbers on incident cost or diagnosis time. Evidence type: assumed.
- Real? The intro uses an industrial setting (over 5,000 services, 10 TB of daily monitoring data, p.5) as context, which is measured scale information but not evidence of the specific RCA difficulty.

## 3. Method
- Events: WHAT / WHEN / WHERE (p.5). Incident = set of events in a window. How events are created in the experiments (thresholds/detectors for the 46 signals per service) is **not specified** (p.9 only says 46 signals).
- NEG (naive event-causal graph): nodes = incident events; same-service pairs get bidirectional links; adjacent-service pairs get a link directed by call direction; no link otherwise (p.6, p.7).
- Parameters: R_s (intra-service causal weights), R_d (inter-service), indexed by event-type pair; S (event importance per event type) (p.7). T = 100, alpha = 0.2 (approximation bound below 1e-8 claimed, p.7).
- Inference (Algorithm 1, p.8): assign E[(a,b)] from R_s or R_d; sum[a] = sum of weights from a; k = alpha * mean of sums; initial score vector = normalized importance S; iterate i = 1..T: Q_i[b] += Q_{i-1}[a] * E[(a,b)] / (sum[a] + k); C[a] += Q_i[a] * k / (sum[a] + k) * length_bonus[i]. Length bonus LB(i) = min(1, 0.01 * 2^(i-1)) (p.8). Chain contribution Eq.2: normalized start importance x product of hop probabilities x out-edge bonus x length bonus.
- Training (Eq.3, Algorithm 2, p.9): loss = negative expected score of the ground-truth root-cause event; Adam with L2 penalty; minimum learning rate 4e-5 (p.10); about 45 minutes to train on a dataset (p.10).
- Human knowledge: SREs may edit learned weights (pp.8-9); not evaluated except by comparing against a fully manual graph.
- Assumptions: historical incidents with root-cause event labels; call dependency graph; incident events already extracted; the root cause is an observed event.

## 4. Data and setup
- Proprietary e-commerce platform ("global top-5", over 5,000 services, three data centers, 185 million active users, p.9). 46 signals per service from 800,000 monitoring signals.
- Service dataset: service-level incidents (e.g. connection stacking); Business dataset: customer/business-impact incidents. **The text says both contain 170 service incidents and 782 business incidents** (p.9), i.e. Service = 170, Business = 782; collected Jan 2020 to Apr 2021, split evenly into train/test "through multiple rounds of random splitting" (p.9). Conclusion (p.11) says 952 incidents total.
- Labels: root-cause events from SRE remediation tickets by keyword search (p.6).
- Faults: real production incidents (not injected).
- Protocol and leakage: random (not temporal) splits; recurring incident types can appear in both halves, and CoE's parameters are per event type, so it can memorize recurring patterns. Results "keep the same in five repeated experiments" (p.10), which suggests a fixed split and seeds rather than variance across splits. No CIs or tests.
- Inference from the numbers (mine, not stated): many Service-dataset percentages equal k/82 (e.g. 79.3% = 65/82, 51.2% = 42/82, 98.8% = 81/82), so the test set is probably about 82 incidents and one incident is about 1.2 points.
- Hardware: i9-9980HK, GTX1080Ti, 32 GB. Inference time 4.06 s / 18.73 events (Business) and 2.16 s / 14.70 events (Service), vs Groot 2.98 s and 3.16 s; model 52.06 KB (p.10).

## 5. Results (copied; Table 2, p.10)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Service top-1 / top-3 | 79.3% / 98.8% | 74% / 92% | Groot with manual graph | Table 2, p.10 |
| Business top-1 / top-3 | 85.3% / 96.6% | 81.1% / 96% (top-1 GraphSAGE, top-3 Groot) | GraphSAGE / Groot | Table 2, p.10 |
| CoE with manual graph | 78.1% / 93.9% (Service), 78.7% / 95% (Business) | n/a | n/a | Table 2 |
| Learned-only baselines | PageRank 16.1/25.3 and 1.2/1.8; GCN 29.3/57.3 and 69.2/85.3; GAT 12.2/47.6 and 60.5/79.2; GraphSAGE 62.2/78.1 and 81.1/93.7; Groot without manual graph 17.1/48.8 and 23.2/45.5 | n/a | n/a | Table 2 |

- Statistical testing: none.
- Ablations: Table 3 (bonus terms): Service top-1 79.3 -> 75.6 without out-edge bonus; Business 85.3 -> 83.4. Table 4 (adding components sequentially): naive CoE 31.7 / 64.6 (Service); +bonus 33.0 / 67.1; +learn S 51.2 / 81.7; +learn R_d 51.2 / 86.6; +learn R_s 79.3 / 98.8; Business 71.7 -> 85.3 top-1. Table 5 (remove one): without learning R_s Service top-1 51.2 / top-3 86.6; without learning S 75.6 / 96.3; without learning R_d 78.1 / 97.6; without bonus 75.6 / 93.9.
- Efficiency: see section 4.
- Notice: Business-set gain over simple GraphSAGE is 85.3 vs 81.1 top-1 and top-3 96.6 vs Groot 96 (0.6 points). Groot figures in Table 2 are written without decimals (74%, 92%, 81%, 96%), which suggests they may be copied from another source or rounded; not stated.

## 6. Limitations
- Authors (p.11): future work on unsupervised or active learning (i.e. labels are needed now).
- **My critique:**
  1. Supervised and label-hungry, yet Table 1 (p.4) marks C3 "needs no manual configuration" as satisfied; that holds only if labelling effort via tickets is free, which the paper asserts ("does not incur additional resource overhead", p.6).
  2. Single proprietary system; data not released; one random split; no variance or tests; test set likely about 82 incidents for the Service dataset.
  3. Event generation is unspecified, so a large part of the pipeline (which determines what is detectable) is invisible.
  4. The claim that the learned graph "surpasses human expertise" (p.10) rests on one manual graph built by the authors' rules and a few points of difference; Business-set CoE with manual graph is lower than Groot and GraphSAGE.
  5. Random splits plus per-event-type parameters invite memorization of recurring incidents.
  6. The edge weights are normalized transition weights with a self-cause term, not calibrated probabilities that one event triggers another; the paper's "likelihood" language (p.5, p.8) can mislead.
  7. Appendix A with the error-bound proof is missing from the PDF.
  8. Interpretability is argued by a single case (Fig 2a, Table 6), not user-tested.
- Not discussed: temporal leakage, sensitivity to event-extraction thresholds, comparisons to Nezha/Eadro/DejaVu on the same data (they are described but not run), generalization to a second system.

## 7. Reproducibility
- Code: https://github.com/NetManAIOps/Chain-of-Event, HTTP 200, last pushed 2024-05-06, 13 stars at check time; contains graph/, util/, conf/ (groot.conf), requirements (torch 2.0.1, torch_geometric 2.3.1); README only shows workflow image and requirements; no license; no data folder. Whether it reproduces the paper's numbers: not tested.
- Data: proprietary; not available.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | needs labelled root-cause events from tickets | label-free calibration | Ours is lighter; theirs gets accuracy from labels |
| Live / streaming | incident-time inference, periodic retraining | incremental windows | Neither streaming-proven |
| Telemetry used | events from metrics/logs/traces + ops activities | traces (+ optional metrics, SSH docker) | Theirs broader on paper |
| Propagation modelling | learned event-type-pair weights, chain scoring | edge probabilities, mostly prior | Theirs learns real weights from 85 to 391 training incidents; ours mostly stays at prior |
| Forecasts future failures | no | risk score, untested | Neither evaluated; theirs does not claim it |
| Explanation | weights, chain contributions, per-round scores | template text | Theirs is stronger and concrete |
| Evaluation rigor | real incidents, one proprietary system, no stats | synthetic only | Theirs is stronger on realism, weaker on openness |
| Open / reproducible | code yes, data no | yes | Ours (data), theirs (code exists) |

- **What they have that we do not:** real production incidents, learned per-event weights, chain-level explanations, integration of operator knowledge.
- **What we have that they do not:** label-free operation, open data path, a (planned) cascade-risk evaluation.
- **Could a reviewer say "this already exists"?** For "learned propagation weights between events for RCA": yes, supervised. For label-free: no, and the authors list unsupervised/active learning as future work. For forecasting: no.
- **Position:** "Chain-of-Event learns event-causal weights from labelled historical incidents; we ask whether comparable propagation weights can be estimated without incident labels."
- **Must we run it as a baseline?** Not for a label-free comparison on RCAEval unless we can supply labels; useful as a supervised upper reference. Code exists; data proprietary, so reproducing their numbers is impossible. Requires an event-extraction step we would have to define.

## 9. Does this paper change what problem we should solve?
- Real problem evidence: weak (asserted). Production incidents are real data, but the paper offers no outage-cost or time-to-diagnose numbers.
- Our gap: not undermined for label-free or forecasting. It does sharpen the point that propagation weights learned from labels beat uniform or rule-based weights on their data (Table 4: learning R_s alone moved Service top-1 from 51.2 to 79.3), so a label-free estimator must show it recovers something useful.

## 10. Citation-ready facts (each with page)
- CoE is a supervised event-graph RCA method trained on historical incidents with root-cause labels taken from SRE tickets (p.6).
- On two proprietary datasets (170 and 782 incidents, one e-commerce system) it reports 79.3% top-1 and 98.8% top-3 (Service), 85.3% and 96.6% (Business) (Table 2, p.10).
- Learned continuous event-pair weights outperformed a manually configured binary graph in their experiments (Table 2, p.10).
- Authors list unsupervised or active learning as future work (p.11).
- Code is public at github.com/NetManAIOps/Chain-of-Event (checked 2026-10-07); data is not.

## 11. Open questions / things to verify
- How events are generated in the experiments (thresholds per signal).
- Appendix A and whether the error bound holds; the proof may be in a longer version.
- Whether the repository reproduces anything on a public dataset (RCAEval/other); not tested.
- Whether FSE Companion '24 track was industry (not stated); Scopus status of the proceedings volume.
