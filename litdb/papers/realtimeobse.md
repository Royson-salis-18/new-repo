---
key: realtimeobse
title: "Observability in Microservices: An In-Depth Exploration of Frameworks, Challenges, and Deployment Paradigms"
authors: "Faseeha, Ummay; Syed, Hassan Jamil; Samad, Fahad; Zehra, Sehar; Ahmed, Hamza"
year: 2025
venue: "IEEE Access, Vol. 13, pp.72011-72039 (published 17 Apr 2025)"
publisher: "IEEE"
doc_type: journal-article
doi: "10.1109/ACCESS.2025.3562125 (PDF header prints 10.1 109/ACCESS.2025.3562 125 with spaces; not re-checked in Crossref)"
issn: "2169-3536"
scopus_indexing: "indexed (manual check of Scopus Sources preview by ISSN, 2026-10-07; IEEE Access, CiteScore 2025 = 9.3, 91st percentile, rank 31/351 General Engineering)"
scopus_match: "ISSN 2169-3536, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied (Scopus preview shows SJR 2025 = 0.884, quartile not displayed)"
peer_reviewed: "yes (received 17 Mar 2025, accepted 11 Apr 2025: a 25-day review for IEEE Access)"
cited_by_crossref: ""
n_references: "about 100"
license: "CC BY 4.0"
batch: "6"
read_status: reviewed                  # all prose sections read to the conclusion; Tables 1-4 and Figs 1-7 did not extract; reference list skimmed
pages: 29
text_chars: 161335
metadata_source: pdf-header
task: "survey (observability tools and frameworks for microservices)"
supervision: "n/a"
online_or_streaming: "n/a"
telemetry: "logs, metrics, traces (observability), eBPF"
propagation_modeling: "n/a"
forecasts_future_failures: "no (not a focus; mentions SuanMing predicting degradation 100 s to 200 s ahead and forecasting-based alerting in AAD)"
llm_used: "no"
systems_evaluated: "n/a"
datasets: "none"
dataset_open: "n/a"
code_open: "n/a"
baselines_compared: "none"
metrics: "numbers copied from the surveyed papers (e.g., CPU overhead percentages)"
headline_result: "taxonomy of observability (purpose, parameters, scope, implementation layer, deployment environment, tools, architecture pattern); Fig 4: root cause analysis 34.2% and performance analysis 30.1% of framework purposes"
evidence_quality: "2"
relevance_to_us: "2"
overlap_with_us: "low (tooling and taxonomy; our data-collection design relates)"
threat_level_for_novelty: "low"
---

# Observability in Microservices: An In-Depth Exploration of Frameworks, Challenges, and Deployment Paradigms

> Reading notes written from the **full text** (`litdb/texts/realtimeobse.txt`). Page numbers are PDF pages (journal pp.72011 to 72039).
> The queue file name for this PDF suggested "real-time observability and failure prediction"; the actual title is the one above, and failure prediction is not its topic.
> Not extracted: Tables 1 to 4 (contents) and Figs 1 to 7 (images). All prose sections were read to the conclusion; the reference list was skimmed.

## 1. One-paragraph summary
A survey of observability for containerized microservices. It proposes a thematic taxonomy (purpose of monitoring, parameters, scope, implementation layers, deployment environments, tools, architecture patterns), reviews 25 published frameworks (e.g., MDF, MetroFunnel, MOA, SuanMing, BBMA, Nezha, eBPF-based tools), compares them in tables, gives counts of tool use, and lists open challenges (cross-level observability, unified data analysis, scalability, adaptability, privacy and security, emerging technologies).

## 2. Problem and motivation
- Problem: observability across system, service and network levels in cloud, fog and edge microservice deployments (pp.1-4).
- Motivation: complexity and distributed failures; no incident data. Evidence type: assumed.
- Real? Not argued with measurements.

## 3. Method (of the survey)
- Searches in IEEE Xplore, ACM Digital Library and Google Scholar with four keyword phrases ("Observability in microservices", "Containerized environments", "Microservices performance monitoring in Kubernetes", "Observability in cloud-native applications"), tools such as OpenTelemetry, Prometheus and Grafana added by popularity (p.5). Inclusion: observability frameworks for containerized microservices, metrics/tracing/log tools, quantitative or comparative analyses; exclusion: monolithic, orchestration-only, before 2019 unless foundational (p.5). The number of retrieved and selected papers is not reported.
- Taxonomy (Fig 2, pp.5-9) and comparison tables (Tables 2-4).
- The "evaluation" (Sec. VI, pp.20-24) restates numbers from the surveyed papers (e.g., KUNERVA 4.53% CPU, CDoF 2.69%, eBPFM 1.4% at 10,000 packets per second, DESK 90 ms for 50 pods and 130 ms for 110 pods) and counts (RCA 34.2% and performance analysis 30.1% of framework purposes; OpenTelemetry in 5 studies, Jaeger and Zipkin in 4 each).

## 4. Data and experimental setup
- None; no experiments. Numbers are copied from other papers without a common protocol.

## 5. Results
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Purposes among reviewed frameworks | RCA 34.2%, performance analysis 30.1% | n/a | n/a | p.20 (Fig 4) |
| Tool usage counts | eBPF most mentioned; OpenTelemetry 5 studies; Jaeger and Zipkin 4 each; BPFTrace 3 | n/a | n/a | pp.23-24 |
| SuanMing (as reported) | predicts microservice performance degradation 100 s to 200 s ahead, accuracy 90%, F1 0.7 | n/a | n/a | p.12 |

- Statistical testing: none. Efficiency numbers are copied as stated in the original papers.

## 6. Limitations
- Stated: none explicit beyond future-direction gaps.
- **My critique:**
  1. Selection is not reproducible: the number of records and the screening steps are not reported.
  2. The "quantitative comparison" collects incommensurable numbers from different studies (CPU percentages, millisecond timings, accuracy) without common settings.
  3. Descriptions of several frameworks are generic (e.g., game theory or GNN described in textbook terms) and add no evaluation; some items are tools rather than research frameworks. In Sec. V.A.27 ("Other observability solutions", pp.15-17) the text uses speculative wording about the surveyed papers ("likely provides tools", "the researchers likely utilize", "specific quantitative results ... are not provided in this excerpt", "the strategies ... would include"), which indicates descriptions written without reading the full source. Claims drawn from those paragraphs are unreliable.
  3b. Nezha is summarized as reaching "97% at both top 3 and top 5 and 90% at top 1" at service level and "outperforms all baseline techniques" (p.12), copied from the Nezha paper (not verified here) and presented as "the most effective tool available" without a common benchmark.
  4. Table and figure contents were not recoverable here, so some claims could not be checked.
  5. The paper is about observability tooling; it does not review RCA or failure forecasting methods systematically, although the reviewed list includes Nezha and SuanMing.
  6. The queue file name (and the earlier REVIEW_REPORT) listed this as "Real-Time Observability and Failure Prediction in Kubernetes-Based Microservices"; it is a survey of observability.
- Not discussed: label requirements, benchmark validity.

## 7. Reproducibility
- Not applicable.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | n/a | label-free | n/a |
| Live / streaming | surveys real-time monitoring | incremental windows | n/a |
| Telemetry used | logs, metrics, traces, eBPF | traces (+ Prometheus/Loki, SSH docker) | n/a |
| Propagation modelling | n/a | edge probabilities | n/a |
| Forecasts future failures | mentions SuanMing and AAD only | claimed | see section 9 |
| Explanation | n/a | templates | n/a |
| Evaluation rigor | none (survey) | synthetic only | n/a |
| Open / reproducible | n/a | yes | n/a |

- **What they have that we do not:** a catalogue of observability tools and overhead figures reported by others.
- **What we have that they do not:** an implemented RCA pipeline.
- **Could a reviewer say "this already exists"?** No.
- **Position:** cite for observability background (logs, metrics, traces, eBPF) and tool landscape; use with the caveat about its comparisons.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- It surfaces a forecasting prior-art item worth checking: **SuanMing** (Grohmann et al., ACM/SPEC ICPE 2021, Crossref DOI 10.1145/3427921.3450248, "Explainable Prediction of Performance Degradations in Microservice Applications"), described here as predicting degradation 100 s to 200 s ahead with 90% accuracy and F1 0.7 (second-hand). Together with the AID, Seer and Sage mentions elsewhere, it is a candidate for the "early warning" related work. Not read in full.
- It also mentions AAD (Kubernetes forecasting of Prometheus metrics to alert early) (p.12).
- It does not provide evidence that the problem is real.

## 10. Citation-ready facts (each with page)
- Observability is defined by logs, metrics and traces, at system, service and network levels (pp.1-2, 5-8).
- eBPF is the most frequently mentioned tool among reviewed frameworks, followed by OpenTelemetry (5), Jaeger and Zipkin (4 each) (pp.23-24).
- A reviewed framework (SuanMing) is reported to predict performance degradation 100 s to 200 s ahead with accuracy 90% and F1 0.7 (p.12, second-hand; verify at source).

## 11. Open questions / things to verify
- Read SuanMing (ICPE 2021) in full; check AID, Seer and Sage in full as the forecasting prior art.
- Table and figure contents.
