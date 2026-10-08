# Comparison with our work (reviewed papers only)

| Key | Supervision | Online | Telemetry | Propagation | Forecasts failures | LLM | Datasets (open?) | Result | Overlap | Threat |
|---|---|---|---|---|---|---|---|---|---|---|
| barata2026anomaly | n/a (survey) | n/a | logs, traces, monitori | n/a (surveys graph-based | no (no | no | Table 9 lists datasets ( (n/a) | 117 studies per abstract (143 per Sec. 4.1.4); 86% | partial  | low |
| li2026service | supervised (cr | claimed  | service logs, API-call | GNN (GAT + GRU/Transform | yes (h | no | proprietary, anonymized; (no (p) | P 0.94, R 0.92, accuracy 0.93, detection time 3.2  | high (ta | medium ( |
| theysayitsre | n/a | n/a | logs, traces, metrics, | none (cites dependency-g | no | mentions | none (n/a () | none of its own; relays MicroRCA 89% precision and | low (LLM | low |
| aoyangfangsonghanzhang | mixed (11 eval | no | metrics, logs, traces  | none proposed; benchmark | no | no | new: 1,430 validated fai (promi) | mean Top@1 of 11 methods 0.21, best MicroRCA 0.37  | high for | low (ben |
| bridgingtheg | mixed: causal  | claimed  | metrics (Prometheus),  | causal discovery (hierar | no (li | yes (Lan | about 500 failure scenar (no) | Sock-Shop top-5 recall 94.3% vs RUN 91.0%, RCD 89. | low (LLM | low |
| erakovic2025hybrid | rule-based wit | no (offl | trace logs only (laten | call-graph and architect | no | no | rca_2020_04_22.csv (desi (yes () | claims correct localization of the injected fault  | partial  | low |
| fu2025intelligent | n/a (survey) | n/a | metrics, logs, traces  | n/a (surveys causal and  | no (no | no (futu | Table 7 lists five publi (n/a) | survey of work published 2013 to 2024; classifies  | partial  | low |
| graphneurala | unclear (score | no | traces (OpenTracing/Ja | GNN (GCN) + GRU | no | no | DeathStarBench (Social N (not s) | AUC 0.951, ACC 0.904, Recall 0.889, F1 0.896 vs GA | low | low |
| pantangshixiangtanghua | label-free pre | no (offl | logs, traces, metrics  | none explicit (LLM reaso | no | yes (sum | challenge phase-one (tra (partl) | final score 50.71 for log+trace+metric; 51.27 for  | partial  | low (for |
| podduturi2025microserv | n/a | n/a | metrics, logs, traces, | none | generi | no | none (n/a) | none (no numbers); qualitative claims of reduced d | none | low |
| realtimeobse | n/a | n/a | logs, metrics, traces  | n/a | no (no | no | none (n/a) | taxonomy of observability (purpose, parameters, sc | low (too | low |
| shuaiyuxiehanbinhejian | supervised (cr | no (per- | metrics, traces, logs  | heterogeneous hypergraph | no | no | A public (GAIA-DataSet r (A yes) | HR@1 0.875 / 0.923 / 0.918 and Avg@3 0.920 / 0.938 | partial  | low |
| sun2025interpretable | label-free at  | partly:  | traces, logs (Drain te | GNN (GraphSAGE-style GAE | no | no | D1 (210 failures, 3,714  (partl) | 30% labels: D1 A@1 0.803, A@5 0.966, Avg@5 0.898;  | high (la | high for |
| unyi2025explainable | supervised on  | no | none (no traces, metri | GNN (4 message-passing b | no in  | no (LLM  | generated with PRISM; ov (state) | tree meshes test MAE 0.009 +/- 0.001, R2 0.992 +/- | low (pro | low |
| costsensitiv | supervised (la | no (offl | metrics only (CPU, mem | none | no | no | RS-Anomic: 100,464 norma (yes () | precision 0.93, recall 0.89, F1 0.91, AUROC 0.98,  | none (su | low |
| pham2024root | mixed: causal- | no (offl | metrics only (Promethe | causal discovery (PC, FC | no | no | synthetic (CIRCA, RCD, C (yes () | no method best everywhere (abstract p.1); PC/FCI/G | partial  | low (it  |
| tingtingwangguilinqi20 | n/a (survey) | n/a | metrics, traces, logs, | n/a (surveys dependency, | no (no | no (surv | benchmarks named: TrainT (n/a) | classifies RCA into metric-, trace-, log-, multimo | partial  | low |
| wang2024rcagent | zero-shot LLM  | deployed | logs (platform, runtim | none | no | yes (Vic | 161 jobs (offline, class (no) | root cause METEOR 15.15 vs ReAct 6.44; G-Correctne | low (LLM | low |
| yao2024chain | supervised (tr | no (inci | events derived from me | learned weighted event-c | no | no (BERT | Service dataset (170 inc (no) | Service: top-1 79.3%, top-3 98.8%; Business: top-1 | partial  | low (for |
| yifeixujingguogehainat | self-supervise | no (offl | metrics collected with | dynamic adjacency from T | no (fo | no | own dataset: about 14,00 (not s) | abstract: 8.6% MAE and 2.2% MSE reduction vs next  | low-medi | low |
| yuqingwangmikavmntylse | supervised few | no | traces (spans) and log | none | no | no (BERT | DeepTraLog (TrainTicket, (yes () | E1 TrainTicket->TrainTicket 5-shot 92.91, 10-shot  | low (sup | low |
| zimingzhaozhenweiwangt | supervised (cr | no (offl | traces (topology), log | GNN (HGT) + hypergraph c | no | no (LLM  | GAIA: 1099 static traces (yes () | GAIA A@1 0.6135, A@3 0.8823, Avg@5 0.8276 vs best  | partial | low |
| causalrca | label-free (tr | no live  | metrics (service laten | learned weighted DAG (DA | no | no | own injected faults: CPU (yes () | service task average Avg@5 0.5815 vs LiNGAM 0.5143 | partial  | low-medi |
| sheriffadepoju2023casc | n/a | n/a | none (conceptual) | none (taxonomy of cascad | no (ca | no (mach | none (n/a) | none (taxonomy of five cascade types and resilienc | none (co | low |
| li2022actionable | supervised (tr | no (offl | metrics only (traces a | failure dependency graph | no | no | 601 failures; A, B, D in (state) | MAR 1.66 to 5.03; A@1 61.84% to 77.18%, A@5 79.24% | medium ( | low-medi |
| li2022causal | label-free (un | no live  | metrics (1-minute samp | causal Bayesian network  | no | no | D_O: 99 cases, 197 metri (no (r) | D_O: CIRCA AC@1 0.404, AC@5 0.763, Avg@5 0.603 vs  | high for | medium |
| deweiliuchuanhexinpeng | label-light/su | deployed | service-call metrics ( | dynamic service call gra | no | no | proprietary; not release (no) | HR@1 0.48, HR@3 0.67, HR@5 0.72, MRR 0.58 vs Monit | partial  | low |
| tianyiyangjiachengshen | label-free (un | claimed  | traces (spans aggregat | edge weight = normalised | no (it | no | TT (simulated users) and (state) | Industry: AID CE 0.3270, MAE 0.1751, RMSE 0.3044 v | partial  | medium |
| realtimecont | n/a (ARIMA tim | yes (str | IoT sensor measurement | none | no (fo | no | 118,370 air-quality reco (yes () | average processing time under 0.06 s per message a | none | low |
| yuganmeghnapancholidai | supervised (de | yes (str | RPC-level traces with  | none explicit: one input | yes (Q | no | own traces; not released (no (p) | abstract: anticipates QoS violations 91% of the ti | partial  | medium |
