# Wiki index by topic

86 pages from 2 repositories, generated 2026-10-07 16:05. Use `TIMELINE.md` for time order and `TAGS.md` for what the pages talk about.

**Start here:** [`pages/lab/docs/REVIEW_REPORT.md`](pages/lab/docs/REVIEW_REPORT.md) (honest review) · [`pages/lab/docs/FIXES_AND_TESTS.md`](pages/lab/docs/FIXES_AND_TESTS.md) (latest tests) · [`pages/lab/RESEARCH.md`](pages/lab/RESEARCH.md) (protocol) · [`pages/mapper/WIKI.md`](pages/mapper/WIKI.md) (the product's own wiki)


## Microservice Mapper: overview

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [Microservice Mapper](pages/mapper/README.md) | Real-time observability for Docker-based microservices — zero code changes required. | 2026-09-12 | 2026-09-18 | 1526 | SSH / EC2 / Docker, dashboard / UI, configuration / API |
| [Microservice Mapper — Complete System Wiki & Operational Reference](pages/mapper/WIKI.md) | This wiki is the authoritative deep-dive documentation for every design decision, subsystem, data model, and operational procedure | 2026-09-15 | 2026-09-18 | 6813 | SSH / EC2 / Docker, configuration / API, dashboard / UI |

## Microservice Mapper: wiki (architecture, data, operations)

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [Overview — What Microservice Mapper Is](pages/mapper/wiki/01-overview.md) | Microservice Mapper is a zero-instrumentation observability platform for Docker-based microservice stacks. It discovers your topol | 2026-09-18 | 2026-09-18 | 429 | SSH / EC2 / Docker, metrics / Prometheus, traces / Jaeger / OpenTelemetry |
| [Architecture — System Layers & Data Flow](pages/mapper/wiki/02-architecture.md) | Tech: React 19, Vite 8, TypeScript 6, @xyflow/react v12, Three.js v0.186, Recharts v3, Framer Motion v13, Lucide React | 2026-09-18 | 2026-09-18 | 817 | SSH / EC2 / Docker, dashboard / UI, architecture / data flow |
| [GraphStore — The Central Nervous System](pages/mapper/wiki/03-graphstore.md) | GraphStore is the most important file in the project. Every node, edge, target, and metric flows through it. No other module keeps | 2026-09-18 | 2026-09-18 | 1137 | anomaly detection, configuration / API, machine learning / GNN |
| [ID System — Canonical Node & Edge IDs](pages/mapper/wiki/04-id-system.md) | The same service is described with different string formats by different subsystems: | 2026-09-18 | 2026-09-18 | 580 | SSH / EC2 / Docker |
| [Telemetry Ingestion — `ingestRemote()` Deep Dive](pages/mapper/wiki/05-telemetry-ingestion.md) | File: server/graph/GraphStore.ts, method ingestRemote(payload, clientIp?) | 2026-09-18 | 2026-09-18 | 1233 | metrics / Prometheus, troubleshooting, traces / Jaeger / OpenTelemetry |
| [Node & Edge Lifecycle — Pruning, Status, Staleness](pages/mapper/wiki/06-node-edge-lifecycle.md) | Targets move through states based on lastSeen — the ISO timestamp updated by any successful telemetry ingestion or HTTP ping. | 2026-09-18 | 2026-09-18 | 864 | troubleshooting, configuration / API, SSH / EC2 / Docker |
| [Remote Collector — Telemetry Sources & Design](pages/mapper/wiki/07-remote-collector.md) | The remote collector is a standalone Node.js process deployed on each EC2 instance. It runs alongside the target application and r | 2026-09-18 | 2026-09-18 | 1139 | SSH / EC2 / Docker, logs |
| [RCA Engine — Root Cause Analysis](pages/mapper/wiki/08-rca-engine.md) | Files: server/rca/RCAEngine.ts, IncidentManager.ts, TemporalAnalyzer.ts, ExplanationEngine.ts, AnomalyDetector.ts | 2026-09-18 | 2026-09-18 | 897 | anomaly detection, cascading failure / propagation, root cause analysis (RCA) |
| [Frontend — Architecture, Hooks & Design Decisions](pages/mapper/wiki/09-frontend.md) | App.tsx owns all UI state and consumes the useGraphData hook. It does not fetch data directly — all data flows through the hook. | 2026-09-18 | 2026-09-18 | 1257 | dashboard / UI, architecture / data flow, traces / Jaeger / OpenTelemetry |
| [WebSocket — Broadcast Hub & Terminal Multiplexer](pages/mapper/wiki/10-websocket.md) | Both the REST API and WebSocket live on the same HTTP server on port 3001. The WebSocketServer is attached with { server } — it in | 2026-09-18 | 2026-09-18 | 803 | dashboard / UI, configuration / API, SSH / EC2 / Docker |
| [ML Anomaly Detection Pipeline](pages/mapper/wiki/11-ml-pipeline.md) | A standalone Python sidecar that trains a per-service IsolationForest on historical metrics collected from the mapper's API, then  | 2026-09-18 | 2026-09-18 | 1383 | anomaly detection, machine learning / GNN, configuration / API |
| [Data Models — TypeScript Interfaces Reference](pages/mapper/wiki/12-data-models.md) | - Server canonical: server/models/ (individual files per type) | 2026-09-18 | 2026-09-18 | 935 | SSH / EC2 / Docker, metrics / Prometheus, configuration / API |
| [API Reference](pages/mapper/wiki/13-api-reference.md) | Every route below is verified against server/api/routes.ts and | 2026-09-18 | 2026-09-18 | 1213 | configuration / API, machine learning / GNN, traces / Jaeger / OpenTelemetry |
| [Configuration Reference](pages/mapper/wiki/14-configuration.md) | Override any value with an environment variable: | 2026-09-18 | 2026-09-18 | 964 | configuration / API, machine learning / GNN, SSH / EC2 / Docker |
| [Troubleshooting & Known Issues](pages/mapper/wiki/15-troubleshooting.md) | Symptom: Target card shows NO DATA status immediately after being added. | 2026-09-18 | 2026-09-18 | 1179 | SSH / EC2 / Docker, troubleshooting, logs |
| [Change Log and Rationale](pages/mapper/wiki/16-change-log-and-rationale.md) | A record of what was changed, why it was changed, and where it lives. | 2026-09-18 | 2026-09-18 | 3697 | configuration / API, troubleshooting, SSH / EC2 / Docker |
| [17 — Findings vs Incidents: two detectors, deliberately separate](pages/mapper/wiki/17-findings-vs-incidents.md) | This page explains why the app has two places that both say "something is | 2026-09-18 | 2026-09-18 | 1218 | anomaly detection, architecture / data flow, configuration / API |
| [18 — Telemetry tiers: the plan](pages/mapper/wiki/18-telemetry-tiers-plan.md) | Status: in progress. Each phase lists what "done" means so progress is | 2026-09-19 | 2026-09-19 | 1341 | metrics / Prometheus, SSH / EC2 / Docker, traces / Jaeger / OpenTelemetry |
| [19 — How it all works](pages/mapper/wiki/19-how-it-all-works.md) | Two passes over the same system. Part 1 is the plain-language version — | 2026-09-24 | 2026-09-24 | 2036 | SSH / EC2 / Docker, configuration / API, metrics / Prometheus |
| [Microservice Mapper — Wiki](pages/mapper/wiki/README.md) | This wiki is the complete technical reference for the Microservice Mapper project. Every document reflects the actual codebase — n | 2026-09-18 | 2026-09-24 | 550 | architecture / data flow, configuration / API, dashboard / UI |

## Microservice Mapper: other components

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [Microservice Mapper | Comprehensive Technical Specification](pages/mapper/PROJECT_REFERENCE.html) | Microservice Mapper / Comprehensive Technical Specification MAPPER OS Foundation Project Vision & Scope Architecture Overview Core | 2026-09-17 | 2026-09-17 | 5809 | configuration / API, traces / Jaeger / OpenTelemetry, SSH / EC2 / Docker |
| [Anomaly detection pipeline](pages/mapper/ml/README.md) | Separate Python pipeline that trains a per-service Isolation Forest on the | 2026-09-17 | 2026-09-17 | 388 | anomaly detection, architecture / data flow |
| [Telemetry Platform — Phase 1 + Phase 2](pages/mapper/telemetry-platform%20%282%29/telemetry-platform/README.md) | Standalone data collection / cleaning / feature-engineering / analytics | 2026-09-15 | 2026-09-15 | 1435 | SSH / EC2 / Docker, architecture / data flow, dashboard / UI |
| [traces-section-prompt](pages/mapper/traces-section-prompt.md) | Build a separate TRACES section for the Microservice Mapper, plus the | 2026-09-17 | 2026-09-17 | 878 | traces / Jaeger / OpenTelemetry, SSH / EC2 / Docker, architecture / data flow |
| [Traffic Generator](pages/mapper/traffic-gen/README.md) | Organic HTTP traffic generator for Sock Shop with a live control UI, headless CLI, SSH-based target discovery, per-user sessions,  | 2026-09-17 | 2026-09-17 | 861 | configuration / API, dashboard / UI, SSH / EC2 / Docker |

## rca-lab: overview and research protocol

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [rca-lab](pages/lab/README.md) | Lean research harness for: unlabeled, live-telemetry root cause analysis with probabilistic cascade-risk prediction. | 2026-10-06 | 2026-10-07 | 718 | SSH / EC2 / Docker, configuration / API, metrics / Prometheus |
| [Research protocol](pages/lab/RESEARCH.md) | Working title: Probabilistic Cascading Failure and Agent Assisted Root Cause Analysis for Microservice Systems | 2026-10-06 | 2026-10-06 | 733 | evaluation / statistics, cascading failure / propagation, traces / Jaeger / OpenTelemetry |

## Reports and findings

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [Fixes attempted and tests on larger apps (2026-10-07)](pages/lab/docs/FIXES_AND_TESTS.md) | Scope: the problems found in REVIEWREPORT.md, what we fixed, what we tested on larger applications, and what is still not solved. | 2026-10-07 | 2026-10-07 | 1723 | cascading failure / propagation, traces / Jaeger / OpenTelemetry, evaluation / statistics |
| [Honest review of the project: RCA + cascading-failure risk for microse](pages/lab/docs/REVIEW_REPORT.md) | Prepared 2026-10-07 for Royson Salis and team (Bharath, Dhanush, Anish). | 2026-10-07 | 2026-10-07 | 5975 | cascading failure / propagation, benchmark / dataset, literature / papers |

## Experiments

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [Experiments behind docs/REVIEW_REPORT.md](pages/lab/experiments/README.md) | Run with the project venv from the project root. Scripts have absolute paths for this machine; edit ROOT if you move the folder. | 2026-10-07 | 2026-10-07 | 145 |  |

## Literature: database, survey table, evidence ledger

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [Comparison with our work (reviewed papers only)](pages/lab/litdb/COMPARISON_MATRIX.md) |  | 2026-10-07 | 2026-10-07 | 605 | traces / Jaeger / OpenTelemetry, logs, metrics / Prometheus |
| [Is the problem real? Evidence ledger](pages/lab/litdb/PROBLEM_EVIDENCE.md) | Purpose: keep an honest record of what the literature actually shows about the problem we claim to solve, so the paper's motivatio | 2026-10-07 | 2026-10-07 | 1632 | cascading failure / propagation, root cause analysis (RCA), benchmark / dataset |
| [Reading queue (3 not yet reviewed, 18 reviewed)](pages/lab/litdb/QUEUE.md) |  | 2026-10-07 | 2026-10-07 | 17 |  |
| [litdb: the reading database](pages/lab/litdb/README.md) | One note per paper, read from the full text, with a structured header that builds the survey table, the comparison matrix and the  | 2026-10-07 | 2026-10-07 | 590 | literature / papers, root cause analysis (RCA), limitations / threats |
| [Literature survey table (21 papers)](pages/lab/litdb/SURVEY_TABLE.md) | Generated from litdb/papers/.md. readstatus: extracted < read-in-full < reviewed. Scopus status is only as good as the list in lit | 2026-10-07 | 2026-10-07 | 813 | literature / papers, root cause analysis (RCA), cascading failure / propagation |
| [{{TITLE}}](pages/lab/litdb/tools/note_template.md) | - Why they say it matters (evidence offered? incident data? industrial numbers?): | 2026-10-07 | 2026-10-07 | 394 | literature / papers |

## Literature: batch comparisons

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [Batch NN: <date>](pages/lab/litdb/batches/_batch_template.md) | Papers: 1) key, 2) key, 3) key. All read in full: yes/no (state any exception). | 2026-10-07 | 2026-10-07 | 116 | literature / papers |
| [Batch 01: 2026-10-07](pages/lab/litdb/batches/batch-01.md) | Papers: 1) li2026service, 2) yao2024chain, 3) sun2025interpretable. All read in full: yes, with exceptions: Li p.12 Algorithm 1 bo | 2026-10-07 | 2026-10-07 | 1447 | cascading failure / propagation, root cause analysis (RCA), benchmark / dataset |
| [Batch 02: 2026-10-07](pages/lab/litdb/batches/batch-02.md) | Papers: 1) pham2024root, 2) pantang...microrca (MicroRCA-Agent), 3) zimingzhao...chase (CHASE). All read in full: yes, with except | 2026-10-07 | 2026-10-07 | 1117 | LLM / agents, benchmark / dataset, root cause analysis (RCA) |
| [Batch 03: 2026-10-07](pages/lab/litdb/batches/batch-03.md) | Papers (all surveys): 1) fu2025intelligent, 2) tingtingwangguilinqi2024comprehensive (Wang and Qi), 3) barata2026anomaly. All read | 2026-10-07 | 2026-10-07 | 962 | literature / papers, benchmark / dataset, root cause analysis (RCA) |
| [Batch 04: 2026-10-07](pages/lab/litdb/batches/batch-04.md) | Papers: 1) yuqingwang...cross (Few-shot cross-system trace classification; arXiv v2 read, published as PACMSE 2025), 2) graphneura | 2026-10-07 | 2026-10-07 | 881 | traces / Jaeger / OpenTelemetry, benchmark / dataset, machine learning / GNN |
| [Batch 05: 2026-10-07](pages/lab/litdb/batches/batch-05.md) | Papers: 1) shuaiyuxie...root (CCLH, arXiv 2511.17566), 2) realtimecont (Ortiz et al., IEEE Access 2019), 3) podduturi2025microserv | 2026-10-07 | 2026-10-07 | 912 | literature / papers, root cause analysis (RCA), cascading failure / propagation |
| [Batch 06: 2026-10-07](pages/lab/litdb/batches/batch-06.md) | Papers: 1) realtimeobse (Faseeha et al., IEEE Access 2025, an observability survey), 2) costsensitiv (Liu et al., Cost-Sensitive M | 2026-10-07 | 2026-10-07 | 842 | literature / papers, cascading failure / propagation, anomaly detection |

## Literature: per-paper reports

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [Report: Barata et al. (2026), Anomaly detection and root-cause identif](pages/lab/litdb/reports/barata2026anomaly.md) | Key barata2026anomaly. Note: litdb/papers/barata2026anomaly.md. Page numbers are PDF pages (42 pages). | 2026-10-07 | 2026-10-07 | 871 | benchmark / dataset, literature / papers, anomaly detection |
| [Report: Liu et al. (2024), Cost-Sensitive Mamba Sequence Modeling for ](pages/lab/litdb/reports/costsensitiv.md) | Key costsensitiv. Note: litdb/papers/costsensitiv.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 601 | anomaly detection, benchmark / dataset, literature / papers |
| [Report: Erakovic and Pahl (2025), Hybrid Root Cause Analysis for Parti](pages/lab/litdb/reports/erakovic2025hybrid.md) | Key erakovic2025hybrid. Note: litdb/papers/erakovic2025hybrid.md. Page numbers are PDF pages (CLOSER pp.255-263). | 2026-10-07 | 2026-10-07 | 811 | traces / Jaeger / OpenTelemetry, architecture / data flow, literature / papers |
| [Report: Fu et al. (2025), Intelligent Root Cause Localization in Micro](pages/lab/litdb/reports/fu2025intelligent.md) | Key fu2025intelligent. Note: litdb/papers/fu2025intelligent.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 782 | benchmark / dataset, literature / papers, root cause analysis (RCA) |
| [Report: Zhang et al. (2025), Graph Neural AI with Temporal Dynamics fo](pages/lab/litdb/reports/graphneurala.md) | Key graphneurala. Note: litdb/papers/graphneurala.md. Page numbers are PDF pages (5 pages). | 2026-10-07 | 2026-10-07 | 636 | anomaly detection, root cause analysis (RCA), benchmark / dataset |
| [Report: Li (2026), GNN service dependency modeling and failure propaga](pages/lab/litdb/reports/li2026service.md) | Key li2026service. Structured note: litdb/papers/li2026service.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 1626 | cascading failure / propagation, literature / papers, troubleshooting |
| [Report: Tang et al. (2025), MicroRCA-Agent](pages/lab/litdb/reports/pantangshixiangtanghuanqipuzhiqingmiaozhixingwang2025microrca.md) | Key pantangshixiangtanghuanqipuzhiqingmiaozhixingwang2025microrca. Note: litdb/papers/pantang...microrca.md. Page numbers are PDF  | 2026-10-07 | 2026-10-07 | 771 | LLM / agents, logs, traces / Jaeger / OpenTelemetry |
| [Report: Pham, Ha, Zhang (2024), RCA for microservices based on causal ](pages/lab/litdb/reports/pham2024root.md) | Key pham2024root. Note: litdb/papers/pham2024root.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 1189 | benchmark / dataset, root cause analysis (RCA), metrics / Prometheus |
| [Report: Podduturi (2025), AI for Microservice Monitoring and Anomaly D](pages/lab/litdb/reports/podduturi2025microservice.md) | Key podduturi2025microservice. Note: litdb/papers/podduturi2025microservice.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 474 | literature / papers, anomaly detection |
| [Report: Ortiz et al. (2019), Real-Time Context-Aware Microservice Arch](pages/lab/litdb/reports/realtimecont.md) | Key realtimecont. Note: litdb/papers/realtimecont.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 555 | architecture / data flow, root cause analysis (RCA) |
| [Report: Faseeha et al. (2025), Observability in Microservices (IEEE Ac](pages/lab/litdb/reports/realtimeobse.md) | Key realtimeobse. Note: litdb/papers/realtimeobse.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 642 | literature / papers, traces / Jaeger / OpenTelemetry |
| [Report: Adepoju (2023), Cascading Failure Modes in Model-as-a-Service ](pages/lab/litdb/reports/sheriffadepoju2023cascading.md) | Key sheriffadepoju2023cascading. Note: litdb/papers/sheriffadepoju2023cascading.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 543 | cascading failure / propagation, literature / papers, architecture / data flow |
| [Report: Xie, He, Wang, Li (2025), CCLH hypergraph RCA](pages/lab/litdb/reports/shuaiyuxiehanbinhejianwangbingli2025root.md) | Key shuaiyuxie...root. Note: litdb/papers/shuaiyuxie...root.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 775 | benchmark / dataset, root cause analysis (RCA) |
| [Report: Sun et al. (2025), DeepHunt: interpretable failure localizatio](pages/lab/litdb/reports/sun2025interpretable.md) | Key sun2025interpretable. Structured note: litdb/papers/sun2025interpretable.md. Page numbers are PDF pages (article 52:1-28). | 2026-10-07 | 2026-10-07 | 1558 | cascading failure / propagation, root cause analysis (RCA), troubleshooting |
| [Report: Vangapelli (2026), AI-Driven Root Cause Analysis In Real-Time ](pages/lab/litdb/reports/theysayitsre.md) | Key theysayitsre. Note: litdb/papers/theysayitsre.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 525 | literature / papers, root cause analysis (RCA) |
| [Report: Wang and Qi (2024), A Comprehensive Survey on Root Cause Analy](pages/lab/litdb/reports/tingtingwangguilinqi2024comprehensive.md) | Key tingtingwangguilinqi2024comprehensive. Note: litdb/papers/tingtingwangguilinqi2024comprehensive.md. Page numbers are PDF pages | 2026-10-07 | 2026-10-07 | 574 | root cause analysis (RCA), literature / papers, cascading failure / propagation |
| [Report: Yao et al. (2024), Chain-of-Event (CoE)](pages/lab/litdb/reports/yao2024chain.md) | Key yao2024chain. Structured note: litdb/papers/yao2024chain.md. Page numbers are PDF pages (ACM cover = p.1). | 2026-10-07 | 2026-10-07 | 1375 | benchmark / dataset, root cause analysis (RCA), literature / papers |
| [Report: Wang et al. (2024), Few-Shot Cross-System Anomaly Trace Classi](pages/lab/litdb/reports/yuqingwangmikavmntylsergedemeyermutlubeyazitjoannakisaakyejessenyyssl2024cross.md) | Key yuqingwang...cross. Note: litdb/papers/yuqingwang...cross.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 1016 | traces / Jaeger / OpenTelemetry, benchmark / dataset, literature / papers |
| [Report: Zhao, Wang et al. (2024/2025), CHASE](pages/lab/litdb/reports/zimingzhaozhenweiwangtiehuazhangzhishushenhaidongzhenleixingjunmagaoweixuzhijundingyunyang2024chase.md) | Key zimingzhao...chase. Note: litdb/papers/zimingzhao...chase.md. Page numbers are PDF pages. | 2026-10-07 | 2026-10-07 | 889 | traces / Jaeger / OpenTelemetry, logs, metrics / Prometheus |

## Literature: per-paper structured notes

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [Anomaly detection and root-cause identification in microservices: a su](pages/lab/litdb/papers/barata2026anomaly.md) | A PRISMA-style survey of anomaly detection and root-cause identification in microservice systems. It describes data collection (lo | 2026-10-07 | 2026-10-07 | 1533 | benchmark / dataset, literature / papers, metrics / Prometheus |
| [> Reading notes written from the **full text** (`litdb/texts/bridgingt](pages/lab/litdb/papers/bridgingtheg.md) | - Why they say it matters (evidence offered? incident data? industrial numbers?): | 2026-10-07 | 2026-10-07 | 393 | literature / papers |
| [> Reading notes written from the **full text** (`litdb/texts/causalrca](pages/lab/litdb/papers/causalrca.md) | - Why they say it matters (evidence offered? incident data? industrial numbers?): | 2026-10-07 | 2026-10-07 | 393 | literature / papers |
| [Cost-Sensitive Mamba Sequence Modeling for Fault Detection in Cloud-Na](pages/lab/litdb/papers/costsensitiv.md) | A short paper proposes a Mamba (state-space) sequence model that classifies sliding windows of multivariate metrics as anomalous o | 2026-10-07 | 2026-10-07 | 1124 | anomaly detection, metrics / Prometheus, literature / papers |
| [Hybrid Root Cause Analysis for Partially Observable Microservices Base](pages/lab/litdb/papers/erakovic2025hybrid.md) | A short conference paper proposes a rule-based RCA for trace-only (partially observable) microservice systems. It mines the archit | 2026-10-07 | 2026-10-07 | 1274 | traces / Jaeger / OpenTelemetry, architecture / data flow, benchmark / dataset |
| [Intelligent Root Cause Localization in MicroService Systems: A Survey ](pages/lab/litdb/papers/fu2025intelligent.md) | A survey of root cause localization in microservice systems covering data collection (observability tools, benchmark systems, faul | 2026-10-07 | 2026-10-07 | 1225 | literature / papers, benchmark / dataset, root cause analysis (RCA) |
| [Graph Neural AI with Temporal Dynamics for Comprehensive Anomaly Detec](pages/lab/litdb/papers/graphneurala.md) | A five-page paper proposes a GCN plus GRU model over a microservice call-chain graph, with a node anomaly score (squared distance  | 2026-10-07 | 2026-10-07 | 879 | anomaly detection, benchmark / dataset, traces / Jaeger / OpenTelemetry |
| [Service dependency modeling and failure propagation prediction in dist](pages/lab/litdb/papers/li2026service.md) | A single-author paper proposes a graph neural network that ingests per-service metrics and a dependency graph, updates edge weight | 2026-10-07 | 2026-10-07 | 2197 | cascading failure / propagation, literature / papers, troubleshooting |
| [MicroRCA-Agent: Microservice Root Cause Analysis Method Based on Large](pages/lab/litdb/papers/pantangshixiangtanghuanqipuzhiqingmiaozhixingwang2025microrca.md) | A competition solution report. For each fault window (start and end time are given in the input), it (a) compresses error logs int | 2026-10-07 | 2026-10-07 | 1383 | LLM / agents, logs, traces / Jaeger / OpenTelemetry |
| [Root Cause Analysis for Microservices based on Causal Inference: How F](pages/lab/litdb/papers/pham2024root.md) | An empirical study that runs nine causal-discovery methods and twenty-one metric-based RCA methods on six synthetic datasets and f | 2026-10-07 | 2026-10-07 | 1742 | benchmark / dataset, root cause analysis (RCA), metrics / Prometheus |
| [AI for Microservice Monitoring & Anomaly Detection](pages/lab/litdb/papers/podduturi2025microservice.md) | A 21-page narrative overview of why microservice monitoring is hard and how supervised, unsupervised, deep and reinforcement learn | 2026-10-07 | 2026-10-07 | 684 | literature / papers, anomaly detection |
| [Real-Time Context-Aware Microservice Architecture for Predictive Analy](pages/lab/litdb/papers/realtimecont.md) | This is not an RCA or failure-prediction paper. It re-engineers an earlier IoT architecture (CARED-SOA) as microservices and adds  | 2026-10-07 | 2026-10-07 | 844 | root cause analysis (RCA), architecture / data flow, literature / papers |
| [Observability in Microservices: An In-Depth Exploration of Frameworks,](pages/lab/litdb/papers/realtimeobse.md) | A survey of observability for containerized microservices. It proposes a thematic taxonomy (purpose of monitoring, parameters, sco | 2026-10-07 | 2026-10-07 | 1083 | literature / papers, traces / Jaeger / OpenTelemetry, metrics / Prometheus |
| [Cascading Failure Modes in Model-as-a-Service Architectures: When Your](pages/lab/litdb/papers/sheriffadepoju2023cascading.md) | A conceptual article argues that when machine-learning models are runtime service dependencies (Model-as-a-Service), failures can  | 2026-10-07 | 2026-10-07 | 769 | cascading failure / propagation, literature / papers, machine learning / GNN |
| [Root Cause Analysis for Microservice Systems via Cascaded Conditional ](pages/lab/litdb/papers/shuaiyuxiehanbinhejianwangbingli2025root.md) | CCLH is a supervised multimodal RCA model. It extracts GRU features from metrics, traces and Drain log templates per instance, fus | 2026-10-07 | 2026-10-07 | 1522 | benchmark / dataset, cascading failure / propagation, root cause analysis (RCA) |
| [Interpretable Failure Localization for Microservice Systems Based on G](pages/lab/litdb/papers/sun2025interpretable.md) | DeepHunt builds a graph per minute (nodes = microservice instances and hosts, edges from calls and deployment, node features = sta | 2026-10-07 | 2026-10-07 | 2084 | cascading failure / propagation, root cause analysis (RCA), benchmark / dataset |
| [AI-Driven Root Cause Analysis In Real-Time Distributed Systems](pages/lab/litdb/papers/theysayitsre.md) | An 8-page position article argues that AI-driven RCA is reliable only with four platform foundations (trustworthy service-state co | 2026-10-07 | 2026-10-07 | 866 | root cause analysis (RCA), literature / papers, metrics / Prometheus |
| [A Comprehensive Survey on Root Cause Analysis in (Micro) Services: Met](pages/lab/litdb/papers/tingtingwangguilinqi2024comprehensive.md) | A descriptive survey that organizes RCA techniques for microservices by data type (metrics, traces, logs, multimodal) plus a short | 2026-10-07 | 2026-10-07 | 1022 | root cause analysis (RCA), literature / papers, metrics / Prometheus |
| [Chain-of-Event: Interpretable Root Cause Analysis for Microservices th](pages/lab/litdb/papers/yao2024chain.md) | CoE turns metrics, logs, traces and operator actions into discrete events (what, when, where) and ranks the events of an incident  | 2026-10-07 | 2026-10-07 | 1998 | root cause analysis (RCA), literature / papers, benchmark / dataset |
| [Few-Shot Cross-System Anomaly Trace Classification for Microservice-ba](pages/lab/litdb/papers/yuqingwangmikavmntylsergedemeyermutlubeyazitjoannakisaakyejessenyyssl2024cross.md) | The paper classifies abnormal traces into fault categories with few labelled examples. A multi-head attention autoencoder fuses sp | 2026-10-07 | 2026-10-07 | 1655 | traces / Jaeger / OpenTelemetry, benchmark / dataset, logs |
| [CHASE: A Causal Hypergraph based Framework for Root Cause Analysis in ](pages/lab/litdb/papers/zimingzhaozhenweiwangtiehuazhangzhishushenhaidongzhenleixingjunmagaoweixuzhijundingyunyang2024chase.md) | CHASE builds, for each trace, a heterogeneous graph of instance, log and metric nodes. Logs go through FastText on templates, metr | 2026-10-07 | 2026-10-07 | 1428 | traces / Jaeger / OpenTelemetry, logs, evaluation / statistics |

## Literature: venue / Scopus checks

| Page | What it says | Created | Updated | Words | Tags |
|---|---|---|---|---|---|
| [Scopus venue checks (manual, via the public Scopus "Sources" preview, ](pages/lab/litdb/reference/scopus_checks.md) | Checked 2026-10-07 by ISSN search in the built-in browser (no sign-in). This is a venue-level check of the current source list (Ci | 2026-10-07 | 2026-10-07 | 590 | literature / papers, limitations / threats |

## Data and results files (not copied; open at the original path)

| File | Size | Modified | What it is |
|---|---|---|---|
| `docs/experiments/candidate_threshold.json` | 5 KB | 2026-10-07 | experiment results |
| `docs/experiments/cascade_risk_auroc.json` | 1 KB | 2026-10-07 | experiment results |
| `docs/experiments/detector_fix_live.json` | 1 KB | 2026-10-07 | experiment results |
| `docs/experiments/edge_prior_fraction.json` | 0 KB | 2026-10-07 | experiment results |
| `docs/experiments/fixes_results.json` | 17 KB | 2026-10-07 | experiment results |
| `docs/experiments/live_false_alarm.json` | 6 KB | 2026-10-07 | experiment results |
| `docs/experiments/synthetic_sweep.json` | 22 KB | 2026-10-07 | experiment results |
| `docs/experiments/otel_healthy_live.npz` | 12 KB | 2026-10-07 | real telemetry captured from your EC2 hosts |
| `docs/experiments/otel_healthy_long.npz` | 44 KB | 2026-10-07 | real telemetry captured from your EC2 hosts |
| `docs/literature/literature_matrix.csv` | 14 KB | 2026-10-07 | literature tables |
| `docs/literature/team_sheet.csv` | 2 KB | 2026-10-07 | literature tables |
| `docs/literature/references.bib` | 24 KB | 2026-10-07 | bibliography (metadata verified via Crossref/OpenAlex) |
| `litdb/papers.csv` | 29 KB | 2026-10-07 | survey table as CSV |
| `results/synthetic_sanity_hard/summary.json` | 5 KB | 2026-10-07 | method-comparison runs |
