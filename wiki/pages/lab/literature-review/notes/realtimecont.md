---
key: realtimecont
title: "Real-Time Context-Aware Microservice Architecture for Predictive Analytics and Smart Decision-Making"
authors: "Ortiz, Guadalupe; Caravaca, José Antonio; García-de-Prado, Alfonso; Chávez de la O, Francisco; Boubeta-Puig, Juan"
year: 2019
venue: "IEEE Access, vol. 7, pp. 183177-183194 (published 18 Dec 2019)"
publisher: "IEEE"
doc_type: journal-article
doi: "10.1109/ACCESS.2019.2960516 (the PDF header prints 10.1 109/ACCESS.2019.29605 16 with spaces; the DOI is as printed, not checked against Crossref)"
issn: "2169-3536"
scopus_indexing: "indexed (manual check of Scopus Sources preview by ISSN, 2026-10-07; IEEE Access, CiteScore 2025 = 9.3, 91st percentile, rank 31/351 General Engineering)"
scopus_match: "ISSN 2169-3536, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied (Scopus preview shows SJR 2025 = 0.884, quartile not displayed)"
peer_reviewed: "yes (received 18 Nov 2019, accepted 13 Dec 2019: a 25-day review for IEEE Access)"
cited_by_crossref: ""
n_references: "about 75"
license: "CC BY 4.0"
batch: "5"
read_status: reviewed                  # reference list read partly; Figs 1-11 and Tables 5-8 images/tables mostly not inspected
pages: 18
text_chars: 94462
metadata_source: pdf-header
task: "not RCA: IoT streaming architecture (microservices + Spark/ARIMA prediction + CEP alerts), air-quality case study"
supervision: "n/a (ARIMA time-series forecasting)"
online_or_streaming: "yes (stream processing, message queues)"
telemetry: "IoT sensor measurements (air pollutants), not microservice telemetry"
propagation_modeling: "none"
forecasts_future_failures: "no (forecasts pollutant levels, not system failures)"
llm_used: "no"
systems_evaluated: "Predictive CARED-SOA on Andalusian air-quality data and synthetic IoT messages (nITROGEN generator)"
datasets: "118,370 air-quality records 2014-01-01 to 2016-03-31; two months (June, July 2019) of Mazagon data; synthetic messages"
dataset_open: "yes (dataset footnote: http://dx.doi.org/10.17632/4y586x9bhv.1, Mendeley Data; not opened)"
code_open: "no"
baselines_compared: "none (ARIMA only; the paper says it does not compare prediction models)"
metrics: "prediction absolute error, level hit rate, processing time per message"
headline_result: "average processing time under 0.06 s per message and 0.01 s per event up to 300,000 messages (pp.12-13); alert-level hit rate 100% for CO and NO2, 48.64% to 93.81% for O3, PM2.5, SO2, PM10 (p.11)"
evidence_quality: "2"
relevance_to_us: "1"
overlap_with_us: "none"
threat_level_for_novelty: "low"
---

# Real-Time Context-Aware Microservice Architecture for Predictive Analytics and Smart Decision-Making

> Reading notes written from the **full text** (`litdb/texts/realtimecont.txt`). Page numbers are PDF pages (journal pp.183177 to 183194).
> Reference list skimmed after [41]; figures and Tables 5 to 8 (appendix) not inspected in detail.

## 1. One-paragraph summary
This is not an RCA or failure-prediction paper. It re-engineers an earlier IoT architecture (CARED-SOA) as microservices and adds a prediction module (ARIMA on Spark Streaming) whose forecasts feed a complex event processing engine that sends context-aware mobile alerts. It is evaluated on air-quality forecasting and on processing throughput with synthetic messages.

## 2. Problem and motivation
- Problem: provide real-time, context-aware, predictive decision-making for IoT data (p.1-2).
- Motivation: IoT big data and the need to act before a situation occurs (e.g., disaster prevention) (p.2). Not about microservice faults.
- Real? Not relevant to our problem.

## 3. Method
- Microservice decomposition with message broker (ActiveMQ), domain and context databases, REST services, a prediction module service (Hadoop YARN + Spark Streaming + Spark SQL + Spark-TS), an ESB (Mule), a CEP engine (Esper), a context broker, Firebase notifications and an Android app (pp.6-8).
- Prediction: ARIMA (autoregression, integration, moving average) per pollutant series; window sizes from 1 to 14 days at 144 samples per day chosen by lowest error (p.10).
- Assumptions: stationary pollutant series (Augmented Dickey-Fuller test, p<0.05) (p.9).

## 4. Data and setup
- 118,370 registers from the Andalusian air sensor network, 2014-01-01 to 2016-03-31; 10-fold cross-validation, 70/30 split (p.10); two months of predicted vs actual levels for Mazagon (June and July 2019) (pp.10-11, appendix).
- Performance tests with synthetic messages from nITROGEN (1,000 to 100,000 messages per queue, one or two queues) on several machines (Table 2) (pp.11-12).
- Leakage and rigor: random cross-validation on time series (10-fold), which is not a valid forecast evaluation; the two-month check is a separate period but reported only as level hit rates.

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Message processing time (prediction module) | under 0.06 s per message, 0.01 s per event, up to 300,000 messages | none | none | pp.12-13 |
| Message processing time (full architecture) | under 0.06 s per message, 0.01 s per event | none | none | p.13 |
| Level hit rate over two months (Mazagon) | CO and NO2 100%; O3, PM2.5, SO2, PM10 48.64% to 93.81% | none | none | p.11 |

- Statistical testing: none.
- Efficiency: stated above; hardware in Table 2 (not extracted).

## 6. Limitations
- Stated: predictions near level thresholds are classified as errors; erroneous predictions due to algorithm anomalies were discarded (appendix B, p.16); future work on other domains.
- **My critique:**
  1. Out of scope for RCA and for microservice fault prediction; the "microservices" here are the system's own components and the domain is IoT air quality.
  2. Random 10-fold cross-validation on time series; discarding "erroneous predictions due to anomalies" in the two-month evaluation biases accuracy.
  3. No baseline predictors; the authors explicitly do not compare models.
  4. Performance numbers rely on synthetic messages and unspecified machine details in an image-like table.
  5. "Predictive" here means forecasting a physical measurement, which is not evidence about forecasting software failures.
- Not discussed: failure handling, fault propagation in the microservice architecture itself.

## 7. Reproducibility
- Air-quality data cited at http://dx.doi.org/10.17632/4y586x9bhv.1 (Mendeley Data; not opened). Code not provided.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | n/a | label-free | n/a |
| Live / streaming | streaming architecture (Spark Streaming) | incremental windows | Their architecture is a throughput design; not RCA |
| Telemetry used | IoT sensor data | traces (+ metrics) | n/a |
| Propagation modelling | none | edge probabilities | Ours |
| Forecasts future failures | no | claimed | n/a |
| Explanation | no | templates | n/a |
| Evaluation rigor | processing times and forecast errors, some flawed | synthetic only | n/a |
| Open / reproducible | data DOI | yes | n/a |

- **What they have that we do not:** nothing relevant to RCA.
- **What we have that they do not:** all RCA-related content.
- **Could a reviewer say "this already exists"?** No.
- **Position:** do not cite as RCA literature; at most in a sentence on streaming architectures for prediction.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- No. It should be removed from the RCA/cascade literature list; the earlier session grouped it with microservice RCA papers.

## 10. Citation-ready facts (each with page)
- A microservice-based IoT architecture combines Spark Streaming ARIMA forecasts with complex event processing for context-aware alerts (pp.6-8).
- Average processing time per message under 0.06 s up to 300,000 messages in synthetic tests (pp.12-13).
- (Not recommended for citation in our paper.)

## 11. Open questions / things to verify
- Crossref check of the DOI spelling; dataset DOI; Tables 5 to 8 content.
