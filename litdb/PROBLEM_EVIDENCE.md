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
| A31 | Among 25 reviewed observability frameworks, root cause analysis (34.2%) and performance analysis (30.1%) are the main purposes | realtimeobse, p.20 (Fig 4) | counted from a non-reproducible selection | weak |
| A32 | Silent decision-quality failures in ML-dependent services propagate along decision paths without errors | sheriffadepoju2023cascading, pp.4-5, Table 1 | conceptual, no data | very weak |
| A33 | Metrics-only anomaly detection with class-weighted Mamba reaches F1 0.91, AUROC 0.98 on RS-Anomic (about 12% anomalous per the dataset README) | costsensitiv, Table 2 p.7 | measured, unverifiable baselines | very weak |
| A34 | An LLM-agent RCA framework reports 94.3% top-5 on Sock-Shop and a 91% MTTR cut in production, but the same paper's two timing tables disagree and the CI width does not fit 50 scenarios | bridgingtheg, pp.10-13 | measured claims, internally inconsistent, unverifiable | very weak |
| A35 | Position paper argues RCA quality is bounded by freshness of topology and change context; no data of its own | theysayitsre, pp.1-7 | assumed (copies others' numbers) | very weak |
| A36 | A gradient-based causal-graph RCA gains only 6.72% (service) and 9.43% (metric, faulty service) relative Avg@5 over structure-learner baselines on one Sock-Shop with three injected faults; on all metrics the average rank is about 13 | causalrca, Tables 3-4 pp.8-9, Fig 10 p.10 | measured, one system, own tuning | weak-medium |
| A37 | Five of 13 public AWS outages 2011-2020 were dependency-related (38%); two (2011, 2012) lasted more than 48 hours in a region | AID (tianyiyang...2021efficient), Table I and p.4 | cited public post-incident summaries, small sample | weak-medium |
| A38 | Binary dependency graphs are not discriminating enough for diagnosis; on Huawei Cloud 67 of 75 labelled dependencies are strong, 8 weak | AID, Table II p.7, pp.4-5 | measured labels on a subset engineers knew | weak |
| A39 | Simulation-only GNN fault forecasting reaches R2 0.99 on 25-node synthetic meshes; real traces untested | unyi2025explainable, pp.11-12, 16 | simulated | very weak |
| A40 | Host co-location and TCP-connection graphs improve metric forecasting error in the authors' ablation (one deployment; table has an impossible MAE/RMSE pair) | yifeixu...2024system, Table 3 p.8 | measured, single run | very weak |
| A41 | A supervised network on queue-depth traces anticipates QoS violations 91% of the time and names the culprit 89% (GCE, authors' own apps, no external baseline) | Seer (yugan...2018seer), p.2 | measured, unreproducible, supervised | weak |
| A42 | On 99 real Oracle failures at a bank, the strongest baseline for RCA is plain NSigma (AC@1 0.323); the best method reaches AC@1 0.404 | CIRCA (li2022causal), Table 3 p.7 | measured, proprietary, tuned on test | medium |
| A43 | On 75 Alibaba availability issues, a call-graph RCA reaches HR@3 0.67 vs 0.49 for Microscope; in deployment HR@3 68%, localization from 30 to 5 minutes | MicroHECL (deweiliu...2021microhecl), Table IV p.7, p.9 | measured, proprietary, supervised detectors | weak-medium |
| A44 | A rule-based alert counter matches or beats SOTA RCA on public benchmarks; 68% of cases have symptoms only in the injected service; 99% of cases lack some telemetry type | Fang et al. (aoyangfang...2025rethinking), Tables 2-3 pp.6-7 | measured across 11 public datasets | medium-strong for 'benchmarks are easy' |
| A45 | 84.4% of 9,152 injected faults produced no user-visible anomaly; on the new benchmark 11 SOTA methods average Top@1 0.21 (best 0.37) | Fang et al., p.13, Table 5 p.14 | measured, one system, re-implemented methods | medium |
| A46 | 74.38% of 576 failure tickets at a bank over 12 months were recurring; average diagnosis time 28.98 min over 20,000 tickets | DéjàVu (li2022actionable), pp.2-3 | measured, one bank | medium |
| A47 | Graph aggregation over call and deployment edges lowers mean average rank by 3% to 31% on four datasets | DéjàVu, Table 3 p.8 | measured, 10 repeated trainings, supervised | medium (supports co-location channel) |
| A48 | LLM-agent RCA for Flink jobs reaches human helpfulness 2.92 of 5 on online out-of-domain jobs | RCAgent (wang2024rcagent), Table 5 p.7 | measured, proprietary, LLM-judged | very weak |

## B. Evidence our specific gap is already addressed (con)
| # | What exists | Source (key, page) | How close to our contribution | Consequence for us |
|---|---|---|---|---|
| 1 | AID (read in full, batch 8): label-free estimate of dependency intensity (edge strength) from traces; evaluated on 94 labelled edges; does NOT forecast failures | AID (tianyiyang...2021efficient), pp.5-9 | medium for 'label-free edge strength'; low for forecasting | cite and compare our edge weights against its DSW similarity; do not call it failure prediction |
| 2 | IEEE TNSM 2025 GNN fault forecasting (read in full, batch 8): simulation-only (PRISM synthetic meshes), supervised on model-checker labels, no telemetry | unyi2025explainable, pp.11-16 | low (not real-telemetry forecasting) | cite as simulation work; real-trace cascade forecasting remains untested |
| 6 | SuanMing (Grohmann et al., ICPE 2021; seen only via the Faseeha survey, p.12): explainable prediction of microservice performance degradation 100-200 s ahead, accuracy 90%, F1 0.7 as reported second-hand; paper verified in Crossref, not read | realtimeobse, p.12; Crossref DOI 10.1145/3427921.3450248 | high for "early warning of degradation exists" | cannot claim early warning as new; must read and compare |
| 5 | DeepHunt (read in full): label-free at cold start via GAE trained on normal data; A@5 0.959 / 0.903 with zero labels; open code and dataset D1 | sun2025interpretable, pp.13, 17 | very high for "label-free multimodal RCA"; none for forecasting | do not claim label-free RCA as novel; propagation weights in DeepHunt are small (Table 7 p.22), no ablation isolates them: our open question |
| 4 | Chain-of-Event (read in full): learns event-level propagation weights, but supervised (labels from tickets p.6), no forecasting | yao2024chain, pp.6-10 | medium for "learned propagation weights"; none for label-free or forecasting | cite as supervised reference; our label-free claim stands; event-level variant is not new |
| 3 | Li 2026 (read in full): supervised GNN predicting propagation probability P(f_i->f_j|t), path ranking, risk score; noisy-OR cascade formula (Eq.21 p.10) identical in form to ours | li2026service, pp.3, 10-11 | high on task, low on credibility (proprietary, inconsistent numbers) | cannot claim cascade-risk prediction or noisy-OR as novel; can claim label-free + open + honest evaluation |
| 7 | Seer (read in full, short arXiv version): supervised early warning of QoS violations plus culprit microservice from queue-depth traces; 91% / 89% on own apps | Seer (yugan...2018seer), p.2 | high for 'early warning with culprit exists' | cannot claim early warning with culprit as new; our difference must be label-free, explicit propagation, calibration |
| 8 | CIRCA (read in full): label-free, architecture-aware causal metric RCA, in RCAEval | li2022causal, pp.3-7 | very high for 'label-free RCA' | must run as baseline; NSigma is its strongest simple baseline |
| 9 | DéjàVu (read in full): supervised graph-attention RCA with call and deployment edges; A@5 79-96% on four datasets | li2022actionable, Table 3 p.8 | medium for 'graph RCA with co-location edges' | cite; our call-edge model omits deployment edges |
| 10 | Fang et al. (read in full): rule-based SimpleRCA is a necessary baseline; benchmarks mostly Type I | aoyangfang...2025rethinking, Tables 2-5 | very high for evaluation design | must run SimpleRCA and stratify by Type I/II/III |

## C. Open questions about the problem
- Do operators actually lack early warning, or do they lack *trust in* and *actionability of* alerts? (look for incident studies)
- What fraction of incidents propagate along call edges vs shared infrastructure? (our model assumes call edges)
- What debugging-time numbers exist from real incidents, and who measured them?
