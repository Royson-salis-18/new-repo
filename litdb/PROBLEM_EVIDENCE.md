# Is the problem real? Evidence ledger

Purpose: keep an honest record of what the literature actually shows about the problem we claim to solve, so the paper's motivation rests on cited evidence
and not on assumptions. Add a row for every claim a **reviewed** paper makes. Quote nothing; paraphrase and give the page.

## Our claimed problem (draft wording)
Root-cause localization on live, unlabeled, architecture-varying telemetry is hard; early identification of cascading-failure risk is under-addressed;
this lengthens debugging time for operators.

## A. Evidence the problem is real (pro)
| # | Claim (paraphrased) | Source (key, page) | Evidence type (measured / anecdotal / assumed) | Strength |
|---|---|---|---|---|
| A1 | Microservice dependency complexity makes traditional (reactive) monitoring and fault tolerance inadequate for forecasting propagation | li2026service, pp.2-3 | assumed (no data cited) | weak |
| A2 | Pilot deployments of a GNN predictor cut unplanned downtime 34-52% and raised availability by 0.06-0.22 points | li2026service, Table 9 p.24 | measured but uncontrolled, proprietary, internally inconsistent (author calls it observational, p.26) | very weak |
| A3 | 127 documented incidents over 18 months; categories: network 23, resource 34, configuration 18, cascading 31, external 21 | li2026service, Table 10 p.25 | measured (proprietary, unverifiable); gives a mix suggesting cascading failures are about 24% of incidents in that set | weak |
| A4 | Incidents in microservice systems can seriously disrupt business; RCA is the stage that most often challenges SREs; the detection and remediation stages follow defined procedures | yao2024chain, p.2 | assumed (general citations, no incident data) | weak |
| A5 | A production e-commerce system with over 5,000 services produces over 10 TB of daily monitoring data, so raw-data RCA is impractical without event abstraction | yao2024chain, p.5 | anecdotal (single company statement) | weak |
| A6 | Without labelled or rule-defined causal graphs a standard event-graph RCA (Groot) falls to 17.1% / 48.8% (Service) top-1 / top-3 vs 74% / 92% with a manual graph; learned weights reach 79.3% / 98.8% | yao2024chain, Table 2 p.10 | measured, proprietary, single split | medium-weak (shows weights matter, supervised) |
| A7 | Labelling root causes is expensive: four experienced operators needed nearly a month for 1,000 cases (cited from RCLIR [6]) | sun2025interpretable, p.2 | cited measurement (second-hand) | medium |
| A8 | AWS December 2021 outage took more than 4 hours to pinpoint the root cause | sun2025interpretable, p.2 (ref [4]) | anecdotal (vendor post-incident summary) | weak |
| A9 | Reconstruction error alone puts the true root cause first in about 70% of 63 failure cases and in the top five in most; propagation-aware scoring is therefore needed | sun2025interpretable, p.7 | measured, small, authors' own | weak-medium |
| A10 | Without labels the localizer reaches A@5 of 0.959 (D1) and 0.903 (D2) but A@1 of only 0.445 on D2; labels lift D2 A@1 to 0.783 at 25% | sun2025interpretable, Table 3 p.17 | measured, small datasets, no stats | medium (labels matter for top-1 on the harder system) |
| A11 | Without automated tools, engineers may need at least several hours to find a failure's root cause; one hour of downtime could cost Amazon.com up to 100 million USD | pham2024root, p.1 (citing [28,57] and [19,22]) | cited, second-hand | weak |
| A12 | Existing causal-graph RCA methods are mostly no better than random on 4 benchmark datasets; simple methods work better | pham2024root, p.6 | measured (open data, 10 repeats, no stats) | medium-strong for "RCA is not solved" |
| A13 | Methods are sensitive to the failure-time estimate: NSigma on Train Ticket Avg@5 about 0.81 at exact time vs about 0.03-0.12 when 60 s late (inferred table mapping) | pham2024root, Table 5 p.7 | measured | medium |
| A14 | A competition LLM-agent RCA system reached a score of 50.71, with the metric modality contributing most (42.78 alone), but no baselines and an undefined score | pantang...microrca (MicroRCA-Agent), Table 1 p.16 | measured, uncomparable | very weak |
| A15 | LLM reasoning chains can hallucinate trace evidence that was never provided | MicroRCA-Agent, p.16 (bad case) | anecdotal (single case) | weak but relevant to faithfulness checks |
| A16 | A supervised multimodal GNN (CHASE) reaches A@1 0.6135 on a 10-instance, log-injected dataset | zimingzhao...chase, Table II p.8 | measured, tiny and easy dataset | very weak |
| A17 | Supervised RCA methods need engineer-prepared labels, which are costly; labeled data are scarce and imbalanced | fu2025intelligent, pp.22-23 | assumed/analytical (survey remark, based on inspecting the AIOps 2022 dataset attributes) | medium-weak |
| A18 | Benchmark fault types (CPU/memory exhaustion, packet loss, delay) do not capture production faults; most fault injection targets microservice level only | fu2025intelligent, pp.10, 13, 27 | analytical (survey remark) | medium-weak |
| A19 | About 74.38% of failures in investigated applications are recurring (cited from DejaVu) | tingtingwang...comprehensive, p.3 | cited measurement, second-hand; implies historical labels are valuable (con for pure label-free) | medium-weak |
| A20 | 14 public outage events 2021-2024 with durations from 87 minutes to months (Table 1) | tingtingwang...comprehensive, p.2 | anecdotal, rows unverified (some look wrong) | very weak |
| A21 | Cross-paper comparison is unreliable because datasets and metrics differ; the survey's own averaged performance cannot be trusted | barata2026anomaly, pp.28, 31 | authors' admission | medium (supports need for common benchmarks) |
| A22 | Unsupervised learning is the most used anomaly detection class and graph-based methods dominate root-cause identification in 143 reviewed studies | barata2026anomaly, pp.23-26 | measured by survey counting, with flawed search terms | weak-medium |
| A23 | Abnormal-trace classes are imbalanced and systems heterogeneous, motivating few-shot and cross-system methods | yuqingwang...cross (arXiv v2), pp.1-2 | assumed | weak |
| A24 | Accuracy 93.26% / 85.2% within system and 92.19% / 84.77% cross-system on benchmark fault categories (10-shot, best of 5 runs per task) | yuqingwang...cross, Tables II-III p.9; best-of-5 p.8 | measured, inflated protocol, labels noisy | weak |
| A25 | Partial observability (no CPU, network or storage metrics) is a realistic constraint in some cloud environments | erakovic2025hybrid, p.1 | assumed | weak |
| A26 | A rule system on trace latency localized one injected container network fault per day in two worked cases (no metrics) | erakovic2025hybrid, pp.5-8 | illustrative only | very weak |
| A27 | A GCN+GRU scores AUC 0.951 on DeathStarBench trace data with undescribed anomalies | graphneurala, Table 1 p.3 | measured but undocumented | very weak |
| A28 | GitHub took about one and a half hours to resolve a codespace failure affecting millions of developers | shuaiyuxie...root, p.1 (cites GitHub availability report Oct 2021) | cited incident report (second-hand) | weak-medium |
| A29 | Failures in microservices propagate through group relations (co-location on a host, load-balancing siblings), not only call edges | shuaiyuxie...root, Fig 1 p.3 and Sec. III | single-run demonstrations on Online Boutique | weak-medium (con for call-edge-only propagation) |
| A30 | Removing the hypergraph (group relations) lowers Avg@3 by 0.08 to 0.14 and F1 by 0.08 to 0.32 across three datasets | shuaiyuxie...root, Table II p.8 | measured, single run, possible leakage | weak-medium |

## B. Evidence our specific gap is already addressed (con)
| # | What exists | Source (key, page) | How close to our contribution | Consequence for us |
|---|---|---|---|---|
| 1 | Verified by abstract (not yet in full): AID (2021) predicts cascading impact via dependency intensity | see docs/REVIEW_REPORT.md section 3.2 | high | must be cited and compared |
| 2 | Verified by abstract: IEEE TNSM 2025 GNN fault forecasting with probabilistic propagation | same | high | must be cited and compared |
| 5 | DeepHunt (read in full): label-free at cold start via GAE trained on normal data; A@5 0.959 / 0.903 with zero labels; open code and dataset D1 | sun2025interpretable, pp.13, 17 | very high for "label-free multimodal RCA"; none for forecasting | do not claim label-free RCA as novel; propagation weights in DeepHunt are small (Table 7 p.22), no ablation isolates them: our open question |
| 4 | Chain-of-Event (read in full): learns event-level propagation weights, but supervised (labels from tickets p.6), no forecasting | yao2024chain, pp.6-10 | medium for "learned propagation weights"; none for label-free or forecasting | cite as supervised reference; our label-free claim stands; event-level variant is not new |
| 3 | Li 2026 (read in full): supervised GNN predicting propagation probability P(f_i->f_j|t), path ranking, risk score; noisy-OR cascade formula (Eq.21 p.10) identical in form to ours | li2026service, pp.3, 10-11 | high on task, low on credibility (proprietary, inconsistent numbers) | cannot claim cascade-risk prediction or noisy-OR as novel; can claim label-free + open + honest evaluation |

## C. Open questions about the problem
- Do operators actually lack early warning, or do they lack *trust in* and *actionability of* alerts? (look for incident studies)
- What fraction of incidents propagate along call edges vs shared infrastructure? (our model assumes call edges)
- What debugging-time numbers exist from real incidents, and who measured them?
