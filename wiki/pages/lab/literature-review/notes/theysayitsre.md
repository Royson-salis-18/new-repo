---
key: theysayitsre
title: "AI-Driven Root Cause Analysis In Real-Time Distributed Systems"
authors: "Vangapelli, Santhosh (independent researcher, USA)"
year: 2026
venue: "International Journal of Artificial Intelligence and Machine Learning (Svedberg Open), Vol. 6, No. 7s, 2026, pp.202-209"
publisher: "Svedberg Open"
doc_type: journal-article
doi: "placeholder: the footer prints 'https://doi.org/10.48084/etasr.XXXXX' (an ETASR-style DOI with XXXXX); no valid DOI in the PDF"
issn: "not printed in the PDF"
scopus_indexing: "unverified: no ISSN in the PDF, so the Scopus check was not possible; venue appears low-visibility"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "unclear (no review dates printed)"
cited_by_crossref: ""
n_references: "17"
license: "CC BY 4.0 (footer)"
batch: "7"
read_status: reviewed
pages: 8
text_chars: 28588
metadata_source: pdf-header
task: "position/overview article on AI-driven RCA architecture (no method implementation, no experiments)"
supervision: "n/a"
online_or_streaming: "n/a"
telemetry: "logs, traces, metrics, dependency graph, schema registry, deployment history (conceptual)"
propagation_modeling: "none (cites dependency-graph traversal by others)"
forecasts_future_failures: "no"
llm_used: "mentions RCACopilot-style LLM reasoning; none built here"
systems_evaluated: "none (illustrative composite case, not a real system)"
datasets: "none"
dataset_open: "n/a ('data available upon request')"
code_open: "n/a"
baselines_compared: "none (Table IV re-states numbers from other papers)"
metrics: "none measured; reports others' figures"
headline_result: "none of its own; relays MicroRCA 89% precision and 97% MAP, MicroNet 90% MAP, RCACopilot 76.6% accuracy, DiagFusion 20.9% to 368% improvement, alert-storm F1 above 0.9 (Table IV pp.5-6, second-hand)"
evidence_quality: "1"
relevance_to_us: "2"
overlap_with_us: "low (LLM-assisted RCA architecture idea; no evaluation)"
threat_level_for_novelty: "low"
---

# AI-Driven Root Cause Analysis In Real-Time Distributed Systems

> Reading notes written from the **full text** (`litdb/texts/theysayitsre.txt`). Page numbers are PDF pages (journal pp.202-209).
> The queue key `theysayitsre` was created from the first words of the abstract; the paper is by Vangapelli.

## 1. One-paragraph summary
An 8-page position article argues that AI-driven RCA is reliable only with four platform foundations (trustworthy service-state context, governed task-oriented interfaces, machine-readable schema and change awareness, structured operational memory with semantic retrieval), sketches a five-layer architecture (ingestion, context, diagnostic workflow, retrieval and memory, reasoning and response), restates published results of other systems in a table, and walks through a composite illustrative incident. It builds and measures nothing.

## 2. Problem and motivation
- Problem: RCA is operationally expensive because evidence is fragmented across logs, events, dependency graphs, deployments and interface contracts (pp.1-2).
- Motivation evidence: cites gray failure (Huang et al., HotOS 2017) and alert storms (Zhao et al., ICSE-SEIP 2020), and troubleshooting-guide issues (Ghosh et al., SoCC 2022) (pp.2-3). These are second-hand citations.
- Real? Plausible and consistent with known literature; no data here.

## 3. Method
- None implemented. A five-layer architecture is described conceptually (Tables II and III, pp.3-5).
- Four evaluation metrics are proposed (hypothesis precision, MTTR relative to manual, novel incident detection rate, time to first actionable hypothesis) (p.5) but not measured.

## 4. Data and experimental setup
- None. Table IV (pp.5-6) re-states figures from five other studies and states that they are "not aggregated into a unified benchmark". The "illustrative case study" is a composite built from patterns in the reviewed papers (p.6).

## 5. Results
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| none measured | n/a | n/a | n/a | n/a |

- Relayed (second-hand): MicroRCA 89% precision, 97% mean average precision; MicroNet 90% mean average precision; RCACopilot RCA accuracy 76.6% over a year of Microsoft incidents; DiagFusion root-cause localization improved 20.9% to 368% over single-modality baselines; alert-storm F1 above 0.9 with more than 98% alert volume reduction (Table IV, pp.5-6).
- The paper attributes the gap between 89% to 90% (controlled) and 76.6% (production) to schema drift, ownership transitions and deployment recency (p.6-7); this attribution is not tested and compares different metrics (precision, MAP, accuracy) on different tasks.

## 6. Limitations
- Stated: abstraction versus fidelity tradeoff; overconfidence of LLM-based systems after recent changes; novel failures need humans (p.7).
- **My critique:**
  1. No data, experiments or implementation: the abstract's phrase "evaluated against empirically reported results" means numbers copied from other papers.
  2. The headline inference (controlled 89% to 90% vs production 76.6%, "directly attributable" to stale context) mixes metrics and tasks and is unsupported.
  3. The footer carries a placeholder DOI "10.48084/etasr.XXXXX" (an ETASR-style prefix with XXXXX), no ISSN, no review dates; the header names a different journal (Svedberg Open IJAIML, Vol. 6, No. 7s, 2026).
  4. Ref [9] ("L. Li et al., Service dependency modeling and failure propagation prediction ... GNN, Discover Artificial Intelligence, 2026") is cited as support for "knowledge graph-assisted fault localization" and for "dependency graph traversal and fault propagation modeling automate cross-service correlation"; the cited paper (batch 1) is a supervised GNN propagation predictor with unverifiable results, listed with the first author's initial wrong (the author is Linling Li), so the citation neither matches the claim nor the author.
  5. Several references are from a different journal family (ETASR 2025 and 2026) cited as supporting graph-based and hybrid anomaly detection ([16], [17]); one of them is on IoT anomaly detection (El Guemmat et al.).
  6. Single independent author; venue not verifiable.
- Not discussed: how the proposed layers would be evaluated empirically; labels; cost.

## 7. Reproducibility
- Nothing to reproduce; "data available upon request".

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | n/a | label-free | n/a |
| Live / streaming | conceptual | incremental windows | Ours implemented |
| Telemetry used | logs, traces, metrics, schema, history | traces (+ metrics) | n/a |
| Propagation modelling | none | edge probabilities | Ours |
| Forecasts future failures | no | claimed | n/a |
| Explanation | ranked hypotheses, evidence pointers, confidence (concept) | templates | Their concept is richer; not built |
| Evaluation rigor | none | synthetic only | Ours |
| Open / reproducible | no | yes | Ours |

- **What they have that we do not:** a clear articulation of context-freshness and structured incident memory as RCA requirements (an architecture sketch).
- **What we have that they do not:** a working pipeline and tests.
- **Could a reviewer say "this already exists"?** No (no implementation or evaluation).
- **Position:** do not cite as evidence; at most as an opinion piece on LLM-assisted RCA infrastructure.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- No. It raises the useful but unevidenced point that stale topology degrades RCA, relevant to our dynamic edge learning.

## 10. Citation-ready facts (each with page)
- None recommended.

## 11. Open questions / things to verify
- Venue identity and ISSN; whether a valid DOI exists; whether the cited numbers match their sources (MicroRCA, MicroNet, RCACopilot, DiagFusion, Zhao et al.).
