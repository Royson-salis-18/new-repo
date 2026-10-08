---
key: soldani2022survey
title: "Anomaly Detection and Failure Root Cause Analysis in (Micro)Service-Based Cloud Applications: A Survey"
authors: "Jacopo Soldani; Antonio Brogi"
year: 2022
venue: "ACM Computing Surveys 55(3), article 59 (published 3 Feb 2022 per Crossref); text read is arXiv 2105.12378v1 (26 May 2021)"
publisher: "ACM"
doc_type: journal-article
doi: "10.1145/3501297"
issn: "0360-0300; 1557-7341 (Crossref)"
scopus_indexing: "venue: ACM Computing Surveys ISSN 0360-0300 is Scopus-indexed (confirmed earlier in litdb/reference/scopus_checks.md); this article's own record not checked"
scopus_match: "ISSN 0360-0300, see scopus_checks.md"
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (ACM Computing Surveys); the arXiv v1 read may differ from the published version"
cited_by_crossref: "245 (Crossref, 2026-10-08)"
n_references: "about 96 (arXiv v1)"
license: ""
batch: "12"
read_status: reviewed                  # sections 1-4 read (intro, terminology, detection and RCA discussions, conclusions); per-technique descriptions skimmed; Tables 1-2 not extracted
pages: 36
text_chars: 166507
metadata_source: crossref+arxiv
task: "survey of anomaly detection and RCA for multi-service applications (qualitative taxonomy)"
supervision: "n/a (survey covers unsupervised, supervised, rule-based)"
online_or_streaming: "n/a"
telemetry: "logs, distributed traces, monitoring KPIs"
propagation_modeling: "classified: topology graph-based, causality graph-based, direct analysis, visualization"
forecasts_future_failures: "no (lists preemptive countermeasures and prediction as future directions)"
llm_used: "no (2021)"
systems_evaluated: "n/a"
datasets: "n/a"
dataset_open: "n/a"
code_open: "n/a"
baselines_compared: "none (qualitative; no quantitative comparison by design)"
metrics: "n/a"
headline_result: "no quantitative result; states that accuracy cannot be compared across techniques because each is evaluated on different applications (pp.28, 30)"
evidence_quality: "4 (as a survey; qualitative)"
relevance_to_us: "4"
overlap_with_us: "context (taxonomy and open challenges)"
threat_level_for_novelty: "low"
---

# Soldani and Brogi: Anomaly Detection and Failure RCA in (Micro)Service-Based Cloud Applications (survey)

> Notes from the **full text** of the arXiv v1 (36 pages): read Sections 1, 2, 3.4, 4.4, 5 and 6 in detail; individual technique descriptions (3.1-3.3, 4.1-4.3) skimmed; Tables 1-2 did not extract. Page numbers are PDF pages.

## 1. Summary
A qualitative survey that separates anomaly detection from RCA for multi-service applications, classifies techniques by data used (logs, distributed traces, monitoring KPIs) and by method, and discusses setup cost, type/granularity of identified root causes, accuracy and explainability, ending with open challenges.

## 2. Problem and motivation
- Detection and understanding of failures in multi-service applications is a "pain" for operators; solutions are scattered, and often cover only detection or only RCA (pp.1-2). Cited motivation; no measurements of its own.

## 3. Method
- Literature survey with a taxonomy: anomaly detection (log-based, trace-based, monitoring-based) and RCA (log-based, trace-based, monitoring-based; direct, topology graph-based, causality graph-based analysis); no search protocol is given in the sections read, so coverage is not reproducible.

## 4. Data and experimental setup
- None. Quantitative comparison is explicitly left to future work (pp.28, 30).

## 5. Results
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| none (qualitative) | n/a | n/a | n/a | n/a |

- Statements useful to us:
  - False positives and negatives are inherent to RCA; correlation-driven methods are prone to spurious correlations even when guided by topology (p.27).
  - A topology that only models service interactions can miss performance anomalies caused by co-hosted services consuming a node's resources (p.27).
  - Most surveyed techniques return a ranked set of candidate root causes; explanation of why a candidate is ranked is an open challenge (pp.27-28).
  - Open directions: continual adaptation to changing applications (re-training and manual updates are costly), explainability by design, recommending countermeasures; and training models to predict similar performance degradations to pre-emptively scale and stop propagation (pp.28, 30-31).

## 6. Limitations
- Stated: no quantitative comparison; accuracy not comparable across papers (pp.28, 30).
- **My critique:**
  1. Published in 2021-2022; excludes LLM-agent, benchmark-critique and hypergraph work; the arXiv v1 may predate revisions in the CSUR version.
  2. No stated search protocol or inclusion criteria in the sections I read; counts of surveyed techniques are not reproducible.
  3. Tables 1-2 (classification) did not extract, so I could not verify individual classification entries.
- Not discussed: label requirements as a design axis (it uses "unsupervised/supervised" for detection only), and cascade forecasting as an existing line of work.

## 7. Reproducibility
- Not applicable.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | classified for detection | none | n/a |
| Live / streaming | n/a | incremental | n/a |
| Telemetry used | survey | traces (+ metrics) | n/a |
| Propagation modelling | topology/causality graph classes | edge probabilities | n/a |
| Forecasting | open direction | claimed | n/a |
| Explanation | open challenge | templates | n/a |
| Evaluation rigor | none | synthetic | n/a |
| Open / reproducible | n/a | yes | n/a |

- **What they have that we do not:** a broad 2021 taxonomy and the explicit statement of open challenges.
- **What we have that they do not:** an implemented method.
- **Could a reviewer say "this already exists"?** Not applicable.
- **Position:** cite for taxonomy and for three limitations we can use: topology-only graphs miss co-hosting, explanation is open, comparison across papers is unreliable.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- It supports our limitation (call-edge-only propagation) and our explanation layer motivation. It also records (as of 2021) cascade/degradation prediction as a future direction, which later work (Seer, SuanMing) had already addressed in part; so it cannot be used as evidence that forecasting is absent.

## 10. Citation-ready facts (each with page)
- "A topology that models only service interactions may miss anomalies caused by co-hosted services consuming a node's resources (p.27)."
- "The survey notes that accuracy cannot be compared across techniques because evaluations use different applications and environments (p.28)."

## 11. Open questions / things to verify
- Differences between arXiv v1 and the CSUR version; Tables 1-2.
