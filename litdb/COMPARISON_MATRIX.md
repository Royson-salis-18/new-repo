# Comparison with our work (reviewed papers only)

| Key | Supervision | Online | Telemetry | Propagation | Forecasts failures | LLM | Datasets (open?) | Result | Overlap | Threat |
|---|---|---|---|---|---|---|---|---|---|---|
| barata2026anomaly | n/a (survey) | n/a | logs, traces, monitori | n/a (surveys graph-based | no (no | no | Table 9 lists datasets ( (n/a) | 117 studies per abstract (143 per Sec. 4.1.4); 86% | partial  | low |
| li2026service | supervised (cr | claimed  | service logs, API-call | GNN (GAT + GRU/Transform | yes (h | no | proprietary, anonymized; (no (p) | P 0.94, R 0.92, accuracy 0.93, detection time 3.2  | high (ta | medium ( |
| theysayitsre | n/a | n/a | logs, traces, metrics, | none (cites dependency-g | no | mentions | none (n/a () | none of its own; relays MicroRCA 89% precision and | low (LLM | low |
| bridgingtheg | mixed: causal  | claimed  | metrics (Prometheus),  | causal discovery (hierar | no (li | yes (Lan | about 500 failure scenar (no) | Sock-Shop top-5 recall 94.3% vs RUN 91.0%, RCD 89. | low (LLM | low |
| erakovic2025hybrid | rule-based wit | no (offl | trace logs only (laten | call-graph and architect | no | no | rca_2020_04_22.csv (desi (yes () | claims correct localization of the injected fault  | partial  | low |
| fu2025intelligent | n/a (survey) | n/a | metrics, logs, traces  | n/a (surveys causal and  | no (no | no (futu | Table 7 lists five publi (n/a) | survey of work published 2013 to 2024; classifies  | partial  | low |
| graphneurala | unclear (score | no | traces (OpenTracing/Ja | GNN (GCN) + GRU | no | no | DeathStarBench (Social N (not s) | AUC 0.951, ACC 0.904, Recall 0.889, F1 0.896 vs GA | low | low |
| pantangshixiangtanghua | label-free pre | no (offl | logs, traces, metrics  | none explicit (LLM reaso | no | yes (sum | challenge phase-one (tra (partl) | final score 50.71 for log+trace+metric; 51.27 for  | partial  | low (for |
| podduturi2025microserv | n/a | n/a | metrics, logs, traces, | none | generi | no | none (n/a) | none (no numbers); qualitative claims of reduced d | none | low |
| realtimeobse | n/a | n/a | logs, metrics, traces  | n/a | no (no | no | none (n/a) | taxonomy of observability (purpose, parameters, sc | low (too | low |
| shuaiyuxiehanbinhejian | supervised (cr | no (per- | metrics, traces, logs  | heterogeneous hypergraph | no | no | A public (GAIA-DataSet r (A yes) | HR@1 0.875 / 0.923 / 0.918 and Avg@3 0.920 / 0.938 | partial  | low |
| sun2025interpretable | label-free at  | partly:  | traces, logs (Drain te | GNN (GraphSAGE-style GAE | no | no | D1 (210 failures, 3,714  (partl) | 30% labels: D1 A@1 0.803, A@5 0.966, Avg@5 0.898;  | high (la | high for |
| costsensitiv | supervised (la | no (offl | metrics only (CPU, mem | none | no | no | RS-Anomic: 100,464 norma (yes () | precision 0.93, recall 0.89, F1 0.91, AUROC 0.98,  | none (su | low |
| pham2024root | mixed: causal- | no (offl | metrics only (Promethe | causal discovery (PC, FC | no | no | synthetic (CIRCA, RCD, C (yes () | no method best everywhere (abstract p.1); PC/FCI/G | partial  | low (it  |
| tingtingwangguilinqi20 | n/a (survey) | n/a | metrics, traces, logs, | n/a (surveys dependency, | no (no | no (surv | benchmarks named: TrainT (n/a) | classifies RCA into metric-, trace-, log-, multimo | partial  | low |
| yao2024chain | supervised (tr | no (inci | events derived from me | learned weighted event-c | no | no (BERT | Service dataset (170 inc (no) | Service: top-1 79.3%, top-3 98.8%; Business: top-1 | partial  | low (for |
| yuqingwangmikavmntylse | supervised few | no | traces (spans) and log | none | no | no (BERT | DeepTraLog (TrainTicket, (yes () | E1 TrainTicket->TrainTicket 5-shot 92.91, 10-shot  | low (sup | low |
| zimingzhaozhenweiwangt | supervised (cr | no (offl | traces (topology), log | GNN (HGT) + hypergraph c | no | no (LLM  | GAIA: 1099 static traces (yes () | GAIA A@1 0.6135, A@3 0.8823, Avg@5 0.8276 vs best  | partial | low |
| sheriffadepoju2023casc | n/a | n/a | none (conceptual) | none (taxonomy of cascad | no (ca | no (mach | none (n/a) | none (taxonomy of five cascade types and resilienc | none (co | low |
| realtimecont | n/a (ARIMA tim | yes (str | IoT sensor measurement | none | no (fo | no | 118,370 air-quality reco (yes () | average processing time under 0.06 s per message a | none | low |
