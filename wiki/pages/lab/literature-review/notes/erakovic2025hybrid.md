---
key: erakovic2025hybrid
title: "Hybrid Root Cause Analysis for Partially Observable Microservices Based on Architecture Profiling"
authors: "Erakovic, Isidora; Pahl, Claus"
year: 2025
venue: "Proceedings of the 15th International Conference on Cloud Computing and Services Science (CLOSER 2025), pp.255-263"
publisher: "SCITEPRESS - Science and Technology Publications"
doc_type: proceedings-article
doi: "10.5220/0013453600003950"
issn: "2184-5042 (proceedings), ISBN 978-989-758-747-4 (from the paper footer, p.1)"
scopus_indexing: "venue series indexed: ISSN 2184-5042 matches Scopus source 'International Conference on Cloud Computing and Services Science, CLOSER - Proceedings' (Scopus preview 2026-10-07; CiteScore 2025 = 2.2, 37th percentile, 130 documents 2022-25); whether the 2025 volume is covered: unverified"
scopus_match: "ISSN 2184-5042, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied (Scopus preview shows SJR 2025 = 0.22, quartile not displayed)"
peer_reviewed: "yes (conference proceedings; review process not described in the PDF)"
cited_by_crossref: ""
n_references: "about 33"
license: "CC BY-NC-ND 4.0"
batch: "4"
read_status: reviewed                  # Tables 1-2 and Figures 1-9 are images; their numeric content was not available
pages: 9
text_chars: 34800
metadata_source: crossref
task: "detection + localization (rule-based RCA on trace latency)"
supervision: "rule-based with thresholds (label-free; thresholds from normal-period maxima)"
online_or_streaming: "no (offline analysis of trace CSV files)"
telemetry: "trace logs only (latency, interactions); no CPU/network/storage metrics by design"
propagation_modeling: "call-graph and architecture mining (shared host/CPU, call dependencies) with latency-pattern rules"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "one ISP microservices system via the TraceRCA public dataset (footnote 1, p.3)"
datasets: "rca_2020_04_22.csv (design) and rca_2020_04_21.csv (validation; only first 40 minutes with trace IDs, one injected fault at docker_007 at 00:17) plus ret_info.csv fault injections"
dataset_open: "yes (https://github.com/NetManAIOps/TraceRCA, cited p.3; not downloaded)"
code_open: "no (no code link)"
baselines_compared: "none"
metrics: "none (qualitative visual confirmation against injected fault)"
headline_result: "claims correct localization of the injected fault in docker_004 (22 Apr 2020) and a container network fault in docker_007 (21 Apr 2020), shown by figures and latency tables; no accuracy numbers (pp.5-8)"
evidence_quality: "1"
relevance_to_us: "3"
overlap_with_us: "partial (trace-only, label-free, architecture-aware)"
threat_level_for_novelty: "low"
---

# Hybrid Root Cause Analysis for Partially Observable Microservices Based on Architecture Profiling

> Reading notes written from the **full text** (`litdb/texts/erakovic2025hybrid.txt`). Page numbers are PDF pages (CLOSER pp.255-263).
> Not available: Tables 1 and 2 (their contents did not extract) and Figures 1-9 (not inspected), so the numeric latency values are unknown to me.

## 1. One-paragraph summary
A short conference paper proposes a rule-based RCA for trace-only (partially observable) microservice systems. It mines the architecture from trace logs (call dependencies, shared hosts), flags anomalies by comparing latencies with pre-fault maxima, classifies the latency pattern (gradual rise, rapid rise, widespread spikes), and maps pattern plus architecture to five fault types (CPU exhaustion, memory exhaustion, host network error, container network error, database failure) by hand-written rules. It illustrates the method on two days of an ISP trace dataset with injected faults and concludes success, without quantitative evaluation.

## 2. Problem and motivation
- Problem: RCA when only trace latency is observable (no CPU, network, storage metrics, as in some clouds) (p.1).
- Motivation: generic statements that RCA is crucial; the claim "current state-of-the-art lacks a deeper interpretation of RCA results within architectural properties" (p.1). No incident data. Evidence type: assumed.

## 3. Method
- Architecture mining (Sec. 4.2.2, p.4): architectural pattern mining (shared resources, shared host, e.g., load balancing across hosts) and call dependency analysis (a call graph from traces); BIRCH clustering used "to validate results" (p.3).
- Anomaly detection (Sec. 5.1, p.7): following Forsberg (2019, a master's thesis), record each component's maximum latency during normal operation and flag interactions that exceed it during the anomaly period.
- Pattern definitions (p.3-4): gradual latency increase (low gradient), rapid increase (high gradient), widespread spikes (irregular). Gradient thresholds are not given.
- Rules (Sec. 4.2.3, p.4): CPU exhaustion = rapid increase and shared CPU; memory exhaustion = gradual increase and affected component; host network error = widespread spikes across all components on the host; container network error = rapid increase in the affected container and connected ones; database failure = rapid increase across all components interacting with the database. The rules are derived from cited literature (Forsberg 2019, Samir and Pahl 2020, Yu et al. 2024, Hadi and Girsang 2023) and the authors' own analysis, not learned.
- Anti-pattern analysis: traces not involving the suspect component should look normal (p.5-6).
- Hyper-parameters: none specified beyond the max-latency threshold.
- Assumptions: only trace latency is visible; faults are of the five listed types and are visible as latency changes.

## 4. Data and setup
- ISP trace log dataset from the TraceRCA repository (footnote 1, p.3): analysis of one day (rca_2020_04_22.csv) and the fault injection file (ret_info.csv), then a second day (rca_2020_04_21.csv) where trace data exist only for the first 40 minutes and one fault is injected in docker_007 at 00:17 (p.7).
- Faults: injected CPU, network and database faults (p.3); in the two examples, container network errors.
- Protocol: the technique was built from the 22 Apr day; "different datasets were used to evaluate the solution" (footnote 2, p.3); validation on 21 Apr is a single fault.
- Leakage: rules are defined using the same dataset family; the same system and fault injection process; validation cases are few.
- Hardware, runtime: not reported.

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Localization of the 22 Apr fault | identified as container network error in docker_004 by visual inspection of latency plots (Figs 1-8) | none | none | pp.5-7 |
| Localization of the 21 Apr fault | docker_007 identified as container network issue (Table 2, Fig 9; one injected fault at 00:17, Table 1) | none | none | pp.7-8 |

- Statistical testing: none. No accuracy, precision, recall, MRR or detection delay.
- Ablations: none.
- Efficiency: not reported.

## 6. Limitations
- Stated: variability of system behaviour and the need for adaptive thresholds (p.8).
- **My critique:**
  1. Evaluation is two worked examples, each with one injected fault, interpreted visually; no numbers.
  2. Rules were handcrafted and checked on the same dataset family; the fault-type rules are generic latency heuristics and the paper does not show that the five fault types are distinguishable in the data.
  3. Thresholds (max normal latency, gradient cutoffs) are undefined or uncalibrated; the baseline is a single day's maximum.
  4. In the second experiment (21 Apr) the text itself notes trace data only for the first 40 minutes and a single fault; db_003 shows no effect "as a consequence of low number of interactions", which shows the method's dependence on data coverage.
  5. Claims to "go beyond" MRCA (Wang et al. 2024) are not tested by comparison.
  6. No baselines (MicroRank, TraceRCA, MicroRCA, DeepHunt).
  7. A companion paper (Erakovic and Pahl, 2025, anomaly detection for partially observable container systems) is cited for details, so this paper is partly incomplete on its own.
  8. Figures carry the evidence, and I could not inspect them.
- Not discussed: false alarm rate under normal operation, multi-fault cases, cascades.

## 7. Reproducibility
- Dataset: TraceRCA repository https://github.com/NetManAIOps/TraceRCA (cited p.3; not opened or downloaded by me). Code: none stated. The rules are described in text and can be reimplemented, but thresholds are missing.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | none (rules and thresholds) | label-free calibration | Similar |
| Live / streaming | offline | incremental windows | Ours |
| Telemetry used | traces only | traces (+ optional metrics, SSH) | Same for the trace-only case |
| Propagation modelling | architecture mining + latency patterns | edge probabilities | Theirs adds fault-type reasoning; unevaluated |
| Forecasts future failures | no | claimed | n/a |
| Explanation | pattern and architecture rules with natural-language reasoning | templates | Theirs shows rule-based explanations |
| Evaluation rigor | two examples | synthetic only | Both weak; theirs uses real injected faults on public data, ours has none |
| Open / reproducible | dataset public, code no | yes | Ours (code), theirs (dataset) |

- **What they have that we do not:** fault-type classification from latency pattern plus architecture; use of a real, public trace dataset with injected faults.
- **What we have that they do not:** a quantified evaluation plan, probabilistic propagation, open code.
- **Could a reviewer say "this already exists"?** Partly for "trace-only, label-free RCA using architecture knowledge", yes, but with minimal evidence.
- **Position:** "Rule-based, trace-only RCA with architecture mining has been proposed (Erakovic and Pahl 2025) and evaluated on two injected-fault cases."
- **Must we run it as a baseline?** No; the rule system is not specified precisely enough, but the ISP TraceRCA dataset is a candidate real-fault dataset for us.

## 9. Does this paper change what problem we should solve?
- It reinforces that trace-only settings (partial observability) are a realistic constraint, the same as ours in Jaeger-only mode.
- It offers no evidence on cascade forecasting.
- Evidence the problem is real: none beyond assertion.

## 10. Citation-ready facts (each with page)
- A rule-based RCA maps latency patterns and architectural knowledge to five fault types using only trace latency (Sec. 4.2, pp.3-4).
- It uses the ISP trace dataset from the TraceRCA repository with injected faults (p.3).
- Its evaluation consists of two worked examples without quantitative metrics (Sec. 5, pp.6-8).
- CLOSER proceedings are indexed in Scopus as a series (checked 2026-10-07); coverage of the 2025 volume unverified.

## 11. Open questions / things to verify
- Table 1 and 2 contents and Figs 1-9.
- Whether the TraceRCA dataset (NetManAIOps/TraceRCA) includes the ISP trace files with injected faults and their size; ask the user before downloading.
- Companion CLOSER 2025 paper by the same authors.
