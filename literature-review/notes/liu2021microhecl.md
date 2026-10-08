---
key: liu2021microhecl
title: "MicroHECL: High-Efficient Root Cause Localization in Large-Scale Microservice Systems"
authors: "Dewei Liu; Chuan He; Xin Peng; Fan Lin; Chenxi Zhang; Shengfang Gong; Ziang Li; Jiayu Ou; Zheshun Wu"
year: 2021
venue: "arXiv preprint 2103.01782v1 (cs.SE, 1 Mar 2021); cited by CIRCA as ICSE-SEIP 2021 pp.338-347 (second-hand)"
publisher: "arXiv"
doc_type: preprint
doi: "10.48550/arxiv.2103.01782"
issn: ""
scopus_indexing: "arXiv preprints are not Scopus-indexed; published ICSE-SEIP version not checked"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "preprint (published ICSE-SEIP 2021 version unverified)"
cited_by_crossref: ""
n_references: "about 25"
license: ""
batch: "9"
read_status: reviewed                  # full text read; Figs 1-5 not inspected
pages: 11
text_chars: 0
metadata_source: arxiv
task: "root cause service and anomaly type localization for availability issues"
supervision: "label-light/supervised components: OC-SVM trained on 100,000 RT cases, random forest on 1,000 labelled error cases, 3-sigma for traffic"
online_or_streaming: "deployed in Alibaba (claimed): average 76 s analysis; offline evaluation on 75 issues"
telemetry: "service-call metrics (response time, error count, QPS) from EagleEye tracing; business metric of the initial service"
propagation_modeling: "dynamic service call graph; traversal along anomalous edges in a direction per anomaly type; Pearson-correlation pruning and ranking"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "Alibaba e-commerce: 75 availability issues from 28 subsystems (265 services on average, up to 1,687)"
datasets: "proprietary; not released"
dataset_open: "no"
code_open: "no"
baselines_compared: "MonitorRank, Microscope (authors' own reimplementations)"
metrics: "HR@1/3/5, MRR, time"
headline_result: "HR@1 0.48, HR@3 0.67, HR@5 0.72, MRR 0.58 vs MonitorRank 0.32/0.40/0.43/0.37 and Microscope 0.35/0.49/0.59/0.44 (Table IV p.7); deployed HR@3 68% over more than 600 issues (p.9)"
evidence_quality: "2"
relevance_to_us: "3"
overlap_with_us: "partial (call-graph anomaly propagation)"
threat_level_for_novelty: "low"
---

# MicroHECL (Liu et al., arXiv 2021)

> Notes from the **full text**. Page numbers are PDF pages. Figs 1-5 not inspected.

## 1. Summary
Given a business-level availability issue on an initial service, MicroHECL builds a call graph from the last 30 minutes, walks it along anomalous service calls in a direction specific to the anomaly type (response time and errors: downstream to upstream; traffic: upstream to downstream), prunes edges whose metric trends do not correlate with the adjacent edge (Pearson below 0.7), and ranks candidate root causes by correlation with the business metric.

## 2. Problem and motivation
- Alibaba's e-commerce system has over 30,000 services; availability issues must be located within minutes (pp.1-2). Single-company statements.

## 3. Method (pp.3-7)
- Three anomaly detectors: OC-SVM on 12 features for response time (trained on 100,000 cases; Table II: F1 0.91 on 600 test cases with 1:1 balance), random forest for error counts (1,000 labelled cases; Table III: F1 0.95 on 400 test cases), 3-sigma with correlation check for QPS.
- Pruning by correlation threshold 0.7; ranking by absolute Pearson correlation with the business metric.

## 4. Data and experimental setup
- 75 availability issues, Feb-Jun 2020, 28 subsystems; annotated by operation engineers (p.7). Counts by type (37 + 43 + 21 = 101) exceed 75 because issues may have several anomaly types.
- Baselines are the authors' own reimplementations from paper descriptions (p.8).

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| HR@1 / HR@3 / HR@5 / MRR | 0.48 / 0.67 / 0.72 / 0.58 | 0.35 / 0.49 / 0.59 / 0.44 | Microscope | Table IV p.7 |
| Reliability HR@1 | 0.30 | 0.26 | MonitorRank/Microscope | Table V p.8 |
| Time vs baselines | 22.3% less than Microscope, 31.7% less than MonitorRank | n/a | n/a | p.8 |
| Pruning at threshold 0.7 | HR@3 stays 0.67; time 75 s to 46 s | n/a | n/a | p.8 |
| Deployment | HR@3 68%, 76 s average, typical 30 min to 5 min | n/a | n/a | p.9 |

## 6. Limitations
- Stated: baselines reimplemented; one company's data; some issues show no metric anomaly; slow accumulation beyond the one-hour window (pp.8-9).
- **My critique:**
  1. Not label-free: three anomaly detectors need training data (100,000 cases and 1,000 labelled cases), unlike CIRCA or ours.
  2. Small test set (75 issues) with no confidence intervals or significance test; results rely on private data.
  3. Baselines are the authors' reimplementations of two older methods; no simple NSigma-style baseline.
  4. The 30-to-5 minute improvement is a typical-case statement without a measurement protocol.
  5. Training and test cases for the detectors come from the same monitoring system; data volumes and split are described only loosely.
- Not discussed: failure-time sensitivity; asynchronous call effects beyond what the graph captures.

## 7. Reproducibility
- No code or data. Alibaba-specific infrastructure (EagleEye).

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | trained detectors | none | ours |
| Live / streaming | deployed (claimed) | incremental | theirs (claimed) |
| Telemetry used | call metrics RT/EC/QPS | traces (+ metrics) | similar |
| Propagation modelling | anomaly-type-specific direction + pruning | learned edge probabilities | theirs has direction logic |
| Forecasts future failures | no | claimed | n/a |
| Explanation | chain of anomalous calls | templates | theirs |
| Evaluation rigor | 75 private cases | synthetic | theirs |
| Open / reproducible | no | yes | ours |

- **What they have that we do not:** per-anomaly-type propagation direction (traffic propagates upstream to downstream) and correlation-based pruning.
- **What we have that they do not:** label-free operation, open code and data.
- **Could a reviewer say "this already exists"?** For call-graph anomaly-chain traversal: yes. It is a representative of the call-graph walk family; its direction-by-type idea is worth borrowing.
- **Position:** cite as a deployed call-graph RCA (supervised detectors) with numbers marked as proprietary.
- **Must we run it as a baseline?** No (no code).

## 9. Does this paper change what problem we should solve?
- No. It shows industrial demand and that traffic anomalies propagate in the opposite direction to latency anomalies, which our call-edge model should respect.

## 10. Citation-ready facts (each with page)
- "MicroHECL reports HR@3 0.67 on 75 Alibaba availability issues vs 0.49 for Microscope (Table IV p.7)" (proprietary data).
- "It treats traffic anomalies as propagating from upstream to downstream and latency and error anomalies in the reverse direction (Table I p.4)".

## 11. Open questions / things to verify
- Published ICSE-SEIP version; whether any code or data exist.
