---
key: tingtingwangguilinqi2024comprehensive
title: "A Comprehensive Survey on Root Cause Analysis in (Micro) Services: Methodologies, Challenges, and Trends"
authors: "Wang, Tingting; Qi, Guilin"
year: 2024
venue: "arXiv:2408.00803v1 [cs.SE], 23 Jul 2024 (ACM template; manuscript submitted to ACM; DOI placeholder 'XXXXXXX.XXXXXXX')"
publisher: "arXiv"
doc_type: preprint
doi: ""
issn: ""
scopus_indexing: "not indexed (arXiv preprint; no journal reference or DOI in the arXiv record, checked 2026-10-07)"
scopus_match: ""
sjr_quartile: "n/a"
peer_reviewed: "no (preprint; dates in the file read 'Received 2 July 2024; revised xxx; accepted xxx')"
cited_by_crossref: ""
n_references: "about 134"
license: "arXiv"
batch: "3"
read_status: reviewed                  # Figs 1-6 not inspected; reference list skimmed
pages: 31
text_chars: 119739
metadata_source: arxiv
task: "survey"
supervision: "n/a (survey)"
online_or_streaming: "n/a"
telemetry: "metrics, traces, logs, multimodal"
propagation_modeling: "n/a (surveys dependency, topology, causal and knowledge graphs)"
forecasts_future_failures: "no (not a focus)"
llm_used: "no (surveys LLM-based RCA in Sec. 3.5)"
systems_evaluated: "n/a"
datasets: "benchmarks named: TrainTicket, SockShop, OnlineBoutique, SocialNetwork"
dataset_open: "n/a"
code_open: "n/a"
baselines_compared: "none"
metrics: "defines A@K, MAR, precision, recall, F1, training time, localization time (Table 7)"
headline_result: "classifies RCA into metric-, trace-, log-, multimodal- and LLM-based (Sec. 3); Tables 3 to 6 list methods; no quantitative comparison"
evidence_quality: "2"
relevance_to_us: "3"
overlap_with_us: "partial (taxonomy; outage motivation table)"
threat_level_for_novelty: "low"
---

# A Comprehensive Survey on Root Cause Analysis in (Micro) Services: Methodologies, Challenges, and Trends

> Reading notes written from the **full text** (`litdb/texts/tingtingwangguilinqi2024comprehensive.txt`). Page numbers are PDF pages.
> Figures 1-6 (diagrams) not inspected; references (pp.26-31) skimmed, not read entry by entry.

## 1. One-paragraph summary
A descriptive survey that organizes RCA techniques for microservices by data type (metrics, traces, logs, multimodal) plus a short section on LLM-assisted RCA, gives method tables (graph category, RCA technique), defines common metrics, and lists challenges and trends. The introduction uses a table of public outage events to motivate the topic.

## 2. Problem and motivation
- Problem: rapid and accurate root cause identification in microservices with dense dependencies and propagating faults (p.1).
- Motivation evidence (pp.2-3): Table 1 of 14 public outage events from 2021 to 2024 (durations from 87 minutes to six months, sources are company statements or news pages); the number of OpenAI status incidents in 2024; a statement that about 74.38% of failures are recurring in investigated applications (cited from [49], the DejaVu work). Evidence type: anecdotal (public incident pages) and one cited measurement.
- Real? Outages are real, but Table 1 is a hand-picked list with unverified entries; at least one entry looks wrong (see critique).

## 3. Method (of the survey)
- Scope and selection: no search protocol, databases, queries or inclusion criteria are stated.
- Structure: preliminaries (data for RCA; dependency, topology, Bayesian, knowledge-graph, rule, statistical, time-series, graph-theory and ML-based RCA, pp.6-11); metric-based (Table 3), trace-based (Table 4), log-based (Table 5), multimodal (Table 6) and LLM-based (pp.21-22) techniques; evaluation metrics (Table 7); interpretability and generalizability (pp.23-24); challenges and trends (pp.24-26).
- Each table lists data source, RCA category, RCA method, graph construction and graph category.

## 4. Data and experimental setup
- None. No experiments.
- Benchmarks named: TrainTicket, SockShop, OnlineBoutique, SocialNetwork (p.7).

## 5. Results (copied; no quantitative results)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Methods tabulated | metric-based (Table 3), trace-based (Table 4), log-based (Table 5), multimodal (Table 6: Pdiagnose, [77], MicroCBR, [81], CloudRCA, MMRCA, Eadro, DiagFusion, Nezha, GROOT, MULAN) | n/a | n/a | pp.13, 16, 19, 21 |
| Outage events | 14 events 2021-2024 (Table 1) | n/a | n/a | p.2 |
| Recurring failures | about 74.38% (cited from [49]) | n/a | n/a | p.3 |

- Statistical testing: n/a.
- Notable statements: faults are "destructive, dependency-complex, propagative and recurring" (p.3); an LLM-based RCA tendency to hallucinate and the difficulty of spotting hallucinations (p.25); real-time analysis is a future trend (p.25); declarative RCA that identifies possible cascading failures from logs ([91], p.20); Sage mentioned as proactively restoring QoS (p.17).

## 6. Limitations
- Stated: none explicit.
- **My critique:**
  1. Preprint, not peer reviewed; the ACM DOI is the template placeholder; "Received 2 July 2024; revised xxx; accepted xxx" appears in the file.
  2. No search methodology; no quantitative comparison; evaluation section only defines metrics.
  3. Table 1 contains unverified or questionable entries; for the UniSuper row, the "Transaction impact" cell reads "125 billion dollars", which I could not verify and which looks like a fund size rather than a loss (not verified, do not cite). The OpenAI incident counts quoted on p.3 (11, 14, 34, 17, 24 for January to May) sum to 100, yet the text says "exceeded 112".
  4. Several entries in method tables are unnamed ("-" with a bare reference number), which makes the tables hard to use.
  5. The survey blends the unit "RCA" across incident-level LLM tools (cloud incident triage) and microservice instance localization, so the taxonomy mixes different problems.
  6. No coverage of recent label-free multimodal methods in the text I read (no mention of DeepHunt or BARO; a text search found none) and no discussion of the Pham et al. benchmark.
- Not discussed: cascade forecasting as a task, apart from passing mentions of Sage and [91].

## 7. Reproducibility
- Not applicable. arXiv 2408.00803 exists (checked 2026-10-07; no journal reference or DOI recorded there).

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | survey | label-free | n/a |
| Live / streaming | calls real-time analysis a trend (p.25) | incremental windows | n/a |
| Telemetry used | all three | traces (+ metrics, SSH) | n/a |
| Propagation modelling | surveys graph categories | edge probabilities | n/a |
| Forecasts future failures | no | claimed | n/a |
| Explanation | surveys interpretability (pp.23-24) | templates | n/a |
| Evaluation rigor | none (survey) | synthetic only | n/a |
| Open / reproducible | n/a | yes | n/a |

- **What they have that we do not:** a broad catalogue of methods, including LLM-based RCA.
- **What we have that they do not:** implementation and tests.
- **Could a reviewer say "this already exists"?** No.
- **Position:** cite for taxonomy and outage motivation only with caveats; prefer the peer-reviewed survey (Fu et al.) for claims.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- No. It provides outage motivation (anecdotal) and a statement that faults propagate and recur (p.3). The recurring-failure statistic (74.38%) comes from DejaVu [49]; it supports supervised or case-based methods more than label-free ones, since recurring failures are learnable from history. This is a consideration for us: if most failures recur, historical labels become valuable.
- Evidence that our gap is not a gap: none.

## 10. Citation-ready facts (each with page)
- The survey categorizes RCA methods by data modality (metrics, traces, logs, multimodal) and covers LLM-based RCA (Sec. 3, pp.11-22).
- It reports that about 74.38% of failures were recurring in the investigated applications, citing DejaVu (p.3; second-hand).
- It lists TrainTicket, SockShop, OnlineBoutique and SocialNetwork as common benchmarks (p.7).
- It notes LLM-based RCA assistants are limited by low accuracy and hallucination (p.25).

## 11. Open questions / things to verify
- Source [49] for the 74.38% figure (DejaVu, check in its own paper).
- Table 1 entries; do not cite individual rows without checking the cited pages.
- Publication status of the preprint.
