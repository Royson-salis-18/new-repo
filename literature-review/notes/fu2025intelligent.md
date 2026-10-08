---
key: fu2025intelligent
title: "Intelligent Root Cause Localization in MicroService Systems: A Survey and New Perspectives"
authors: "Fu, Nan; Cheng, Guang; Teng, Yue; Dai, Guangye; Yu, Shui; Chen, Zihan"
year: 2025
venue: "ACM Computing Surveys, Vol. 57, No. 12, Article 325"
publisher: "ACM"
doc_type: journal-article
doi: "10.1145/3736755"
issn: "0360-0300, 1557-7341"
scopus_indexing: "indexed (manual check of Scopus Sources preview by ISSN, 2026-10-07; CiteScore 2025 = 65.2, 99th percentile, rank 1/241 General Computer Science)"
scopus_match: "ISSN 0360-0300, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied (Scopus preview shows SJR 2025 = 5.985, quartile not displayed)"
peer_reviewed: "yes (received 29 Apr 2024, revised 10 Apr 2025, accepted 29 Apr 2025, p.30 end)"
cited_by_crossref: "10 (Crossref, 2026-10-07)"
n_references: "147"
license: "ACM publication rights licensed"
batch: "3"
read_status: reviewed                  # Figs 1-9 not inspected; references skimmed for topic terms, not each read
pages: 37
text_chars: 148447
metadata_source: crossref
task: "survey"
supervision: "n/a (survey)"
online_or_streaming: "n/a"
telemetry: "metrics, logs, traces (observability), collection tools"
propagation_modeling: "n/a (surveys causal and topological graph methods)"
forecasts_future_failures: "no (not a focus; Seer and Mariani et al. appear only in passing)"
llm_used: "no (future-work mentions)"
systems_evaluated: "n/a (surveys Train Ticket, Sock Shop, Hotel Reservation, Hipster-Shop benchmarks)"
datasets: "Table 7 lists five public datasets"
dataset_open: "n/a"
code_open: "n/a"
baselines_compared: "none (qualitative tables only)"
metrics: "n/a"
headline_result: "survey of work published 2013 to 2024; classifies methods as direct vs indirect analysis; Table 10 compares 17 studies by check marks only"
evidence_quality: "3"
relevance_to_us: "4"
overlap_with_us: "partial (taxonomy and gaps)"
threat_level_for_novelty: "low"
---

# Intelligent Root Cause Localization in MicroService Systems: A Survey and New Perspectives

> Reading notes written from the **full text** (`litdb/texts/fu2025intelligent.txt`). Page numbers are PDF pages (article pages 325:1 to 325:37).
> Figures 1-9 not inspected. The reference list (147 entries) was scanned for relevant terms; each entry was not read in detail.

## 1. One-paragraph summary
A survey of root cause localization in microservice systems covering data collection (observability tools, benchmark systems, fault injection, production practice, public datasets), "direct" analysis (from observed data without a graph) and "indirect" analysis (via causal or topological graphs plus inference such as random walk), the role of AI in each, a qualitative attribute comparison of 12 methods and a check-mark evaluation of 17 studies, and a list of challenges with a proposed end-to-end framework for enterprise networks.

## 2. Problem and motivation
- Problem: no survey covers the whole lifecycle (data collection, AI-driven analysis, evaluation) (pp.2-4).
- Motivation evidence: statements that faults are inevitable and cause user dissatisfaction or financial losses (cites [14, 68, 102]); billions of runtime records per day per system (cites [76], pp.2, 12). No numbers measured by the authors.
- Real? Asserted with citations, not measured.

## 3. Method (of the survey)
- Scope: papers published 2013 to 2024 (p.2). **No search protocol, databases, query strings, or inclusion and exclusion criteria are given** (my search of the text for these terms found none).
- Taxonomy (Fig 2, p.6): data collection -> direct analysis (metrics, traces, multi-source) or indirect analysis (causal graphs: PC and variants, fault propagation graphs, inference graphs; topological graphs: dependency and relationship graphs) -> inference (random walk, BFS, DFS, AI) -> evaluation.
- Comparison dimensions: interpretable, adaptive, scalable, practical, multi-source (Table 9, p.24); closed-world vs open-world, effectiveness, time and resource overhead (Table 10, p.27).
- Proposed end-to-end framework with user, network and cloud agents (Fig 9, p.30), not evaluated.

## 4. Data and experimental setup
- None: no experiments or re-evaluation. Table 10 uses check marks taken from the cited papers.
- Benchmarks described: Train Ticket (41 microservices, 86 request types), Sock Shop (13, 10), Hotel Reservation (15), Hipster-Shop (10) (Table 4, p.9).
- Fault simulation tools: Istio, Chaos Mesh, tc, stress-ng, Strace, code modification (Table 5, p.10).
- Collection tools compared: Istio, cAdvisor, Jaeger, Node-exporter, Prometheus, eBPF by intrusiveness, complexity, generality, versatility (Table 6, p.11).
- Public datasets (Table 7, p.14): Psqueeze, DejaVu (A, B, C), RCD, TraceRCA, MEPFL datasets, with sizes and fault levels as cited.

## 5. Results (copied; no quantitative results)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Methods classified | 17 studies in Table 10; 12 in Table 9 (7 AI, 5 non-AI) | n/a | n/a | pp.24, 27 |
| Localization levels | seven levels (Fig 8) | n/a | n/a | p.25 |

- Statistical testing: n/a.
- Notable claims: heuristic unsupervised methods are lighter but less accurate than supervised ones (p.23); supervised methods need labels prepared by engineers, which is costly (pp.22-23); most studies inject faults into microservices only, limiting levels of fault data (p.10); mismatch between benchmark fault types and production faults (pp.13, 27).

## 6. Limitations
- Stated: none explicit; future directions list open problems (Sec. 7).
- **My critique:**
  1. No systematic review protocol: selection of papers is not reproducible.
  2. Table 10's "effectiveness" and "efficiency" are check marks; no numbers are compared, so the "performance evaluation" promised in the abstract is qualitative.
  3. Some characterisations conflate methods (e.g. Seer is listed under topological/supervised RCA; it is a QoS-violation predictor) and Table 9's "Multi-Source" column is defined as multiple root causes, which differs from the usual meaning of multimodal data (p.24, footnote 5).
  4. Coverage of recent multimodal and label-free methods is thin: a text search finds no mention of DeepHunt, BARO, Eadro, DiagFusion or Nezha anywhere in the paper (only CIRCA, inside a list of PC-based methods, p.17). It cites HRLHF, Grace, DejaVu and others.
  5. The reference labelled "Pham et al. [102]" (p.23) is Cuong Pham et al. 2016 (failure diagnosis by targeted fault injection), not the 2024 ASE evaluation by Luan Pham et al., which is not cited; so the survey does not engage with the benchmark evidence that simple methods compete.
  6. The proposed end-to-end framework (Fig 9) has no implementation or data.
  7. The text claims AI methods "have become more intelligent than traditional methods" (p.2) without evidence from controlled comparisons, whereas the later benchmark literature (Pham et al.) finds simple methods competitive.
- Not discussed: label-free vs labelled comparisons on common data; cascade forecasting as a task.

## 7. Reproducibility
- Not applicable (survey). Publisher page: ACM DOI 10.1145/3736755 resolves via Crossref; Crossref cited-by 10.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | surveys; says unlabeled data is scarce for supervised methods (pp.22-23) | label-free | n/a |
| Live / streaming | calls for adaptive, low-overhead collection (p.28) | incremental windows | n/a |
| Telemetry used | metrics, logs, traces | traces (+ metrics, SSH) | n/a |
| Propagation modelling | surveys causal/topological graphs | edge probabilities | n/a |
| Forecasts future failures | not a focus | claimed | n/a |
| Explanation | surveys interpretability as an attribute | templates | n/a |
| Evaluation rigor | no experiments | synthetic only | n/a |
| Open / reproducible | n/a | yes | n/a |

- **What they have that we do not:** a broad taxonomy and tooling overview.
- **What we have that they do not:** an implemented system and tests.
- **Could a reviewer say "this already exists"?** No, but our related-work section must cover this survey and use its taxonomy.
- **Position:** "Following the taxonomy of Fu et al., our approach is an indirect (graph-based) unsupervised method."
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- It documents that supervised methods need hard-to-obtain labels (pp.22-23) and that benchmark fault types differ from production (pp.13, 27), supporting our label-free motivation and our caution about injected faults.
- It does not discuss cascade forecasting as a field; cascade or failure prediction appears only through Seer and one 2020 reference [83] ("Predicting failures in multi-tier distributed systems"), listed in the references, not discussed in the text I read. This suggests RCA surveys treat forecasting as outside their scope; it does not show forecasting is unexplored (other work exists, see REVIEW_REPORT 3.2).

## 10. Citation-ready facts (each with page)
- The survey organizes root cause localization into data collection, direct analysis and indirect analysis (graph-based) (pp.6, 14-22).
- It reports that supervised methods require engineer-prepared labels, which is costly (pp.22-23).
- It notes a mismatch between benchmark fault types (CPU or memory exhaustion, packet loss, delay) and production faults (pp.13, 27).
- Most fault-injection studies inject at microservice level, limiting data granularity (p.10).
- It lists Train Ticket, Sock Shop, Hotel Reservation and Hipster-Shop as widely used benchmark systems (Table 4, p.9).

## 11. Open questions / things to verify
- Whether the survey's classification of Seer is accurate.
- Whether a 2025 revision cycle (revised April 2025) added only the data-collection material; the survey's literature cutoff appears to be 2024 but most cited methods are 2021 to 2023.
- Figs 1-9.
