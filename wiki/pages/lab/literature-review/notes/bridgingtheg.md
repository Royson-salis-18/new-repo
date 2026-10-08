---
key: bridgingtheg
title: "Bridging the Gap: A Systematic Framework for Agentic AI Root Cause Analysis in Hybrid Distributed Systems (AURORA)"
authors: "Maheshkar, Jaykumar Ambadas (U.S. Bancorp, per the PDF header)"
year: 2025
venue: "Acta Sci., 26(1), 2025, pp.228-245 (PDF header, ISSN 2178-7727)"
publisher: "not stated"
doc_type: journal-article
doi: ""
issn: "2178-7727 (printed in the PDF header); Crossref and Scopus both identify this ISSN as 'Acta Scientiae', a Brazilian journal of science and mathematics education (Lutheran University of Brazil)"
scopus_indexing: "the ISSN is indexed (Scopus preview: Acta Scientiae, CiteScore 2025 = 1.0, 37th percentile), but a microservices RCA paper in a science and mathematics education journal is a venue mismatch; I could not find this article under that journal in Crossref (title search returned other works): publication in that venue is unverified"
scopus_match: "ISSN 2178-7727, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied (Scopus preview shows SJR 2025 = 0.243 for Acta Scientiae)"
peer_reviewed: "unverified (a journal name and page numbers are printed; no review dates; venue/article not found in Crossref)"
cited_by_crossref: ""
n_references: "about 38 (numbering skips [36])"
license: "unknown"
batch: "7"
read_status: reviewed                  # Figs 1-4 not inspected; Tables 1-6 read
pages: 18
text_chars: 65961
metadata_source: pdf-header
task: "RCA (localization) via LLM multi-agent framework with hierarchical causal discovery; plus remediation"
supervision: "mixed: causal discovery unsupervised; learned fusion weights use labelled incidents; RL 'learning agent'; claims few-shot adaptation as future work"
online_or_streaming: "claimed (production deployment); no live evaluation shown"
telemetry: "metrics (Prometheus), logs (Elasticsearch), traces (Jaeger) via OpenTelemetry"
propagation_modeling: "causal discovery (hierarchical RCD with PC), neural Granger causality, PageRank with uncertainty; edge voting for multimodal fusion"
forecasts_future_failures: "no (lists proactive failure prediction as future work)"
llm_used: "yes (LangChain ReAct supervisor agent, an OpenAI API in the cost table, temperature 0.0, max 15 iterations)"
systems_evaluated: "Sock-Shop (15 microservices), Train Ticket (41), Online Boutique (11), synthetic systems of 100 to 1000 services, and a 247-microservice production deployment at an unnamed organization"
datasets: "about 500 failure scenarios (60% single root cause, 15% cascading, 10% multi-root, 10% Byzantine, 5% novel); data not released"
dataset_open: "no"
code_open: "repository exists: https://github.com/jay-gatech/agenticai-rca-langchain (MIT, last push 2025-11-04; top-level folders aurora, deployment, scripts; no benchmark data or evaluation scripts seen at top level; README cites the work as an 'arXiv preprint')"
code_open_note: "checked via the GitHub API 2026-10-07"
baselines_compared: "rule-based, PC, RCD, RUN"
metrics: "Top-1, Top-3, Top-5, MRR, time, ECE; MTTR in the deployment"
headline_result: "Sock-Shop top-5 recall 94.3% vs RUN 91.0%, RCD 89.0%, PC 86.2%, rule-based 73.1% (Table 2, p.10); production MTTR 47 min to 4.3 min (91% reduction), 74x ROI (p.13)"
evidence_quality: "1"
relevance_to_us: "2"
overlap_with_us: "low (LLM agent plus causal discovery; supervised pieces; no forecasting)"
threat_level_for_novelty: "low"
---

# Bridging the Gap: A Systematic Framework for Agentic AI Root Cause Analysis in Hybrid Distributed Systems (AURORA)

> Reading notes written from the **full text** (`litdb/texts/bridgingtheg.txt`). Page numbers are PDF pages (18 pages; printed pages 228-245).
> Figs 1-4 (architecture and workflow diagrams) not inspected; Tables 1-6 read as text.

## 1. One-paragraph summary
A paper by a bank vice president presents AURORA, a multi-agent framework in which a LangChain ReAct "supervisor" calls specialist agents (telemetry collection, anomaly detection, causal inference, root cause localization, remediation, learning). Causal inference uses a hierarchical RCD variant, neural Granger causality and edge voting across modalities. The paper states three theorems (sample complexity O(n^2 log n), identifiability, multimodal fusion), reports top-5 recall of 94.3% on Sock-Shop above RUN and RCD, ablations, a failure taxonomy, and a production deployment on 247 microservices with a 91% MTTR reduction and 74x ROI.

## 2. Problem and motivation
- Problem: RCA in hybrid cloud and on-premise microservices; four deficiencies (alert fatigue, dependency complexity, dynamic evolution, knowledge silos) (p.2).
- Evidence offered: "it can take up to three hours to find the cause of a failure without automated tools" attributed to NeurIPS 2022 [5][9] (p.2); resilience-pattern percentages (circuit breaker 58% fewer errors, bulkhead 10% availability, retry 21%, timeout 30%) with no source (p.2). Evidence type: cited second-hand and unsourced.
- Real? Standard claims; the three-hour figure is a second-hand statement in the RCD paper's literature (Pham et al., batch 2, p.1 cite "at least several hours" with sources [28, 57]); the resilience percentages are unsourced.

## 3. Method
- Architecture (pp.6-9): seven agents; supervisor via create_react_agent; telemetry from Prometheus, Elasticsearch, Jaeger; anomaly agent with z-score, isolation forest and pattern rules; causal agent with hierarchical RCD (adaptive partition size starting at sqrt(n), halving when the candidate set is small), neural Granger (LSTM), multimodal fusion by weighted edge voting with weights inversely proportional to estimated error (Theorem 3); localization agent with personalized PageRank, random walk, betweenness and Bayesian posterior; remediation through the Kubernetes API with human approval; learning agent with reinforcement learning.
- Theory (pp.5-6): Theorem 1: with bounded in-degree d and partition size k at most sqrt(n), sample complexity O((d^2/alpha^2) log(nk/delta)) = O(n^2 log n); Corollary 1 contrasts with PC's O(n^3); Theorem 2: root cause identifiability given a path, no hidden confounders and sufficient intervention strength; Lemma 1: intervention detectable when KL divergence exceeds a threshold; Theorem 3: fused error below the weighted average of modality errors. Proofs are sketched in a few sentences with citations to Pearl and Spirtes et al. and are not proved.
- Hyper-parameters (Table 6, p.12): RCD alpha 0.05, subset 20, LLM temperature 0.0, max iterations 15, GNN hidden 64, Granger epochs 100.
- Assumptions: causal Markov and faithfulness, no major hidden confounders, at least 100 historical episodes, 15 to 500 services, single root cause for the strongest guarantees (p.14).

## 4. Data and experimental setup
- Benchmarks: Sock-Shop (15 microservices), Train Ticket (41), Online Boutique (11), synthetic 100, 200, 500, 1000 services; "almost 500" failure scenarios: single root (60%), cascade (15%), multi-root (10%), Byzantine (10%), novel (5%) (p.10). How scenarios were produced and labelled is not described; synthetic data for the large systems.
- Statistics: bootstrap CIs (1000 resamples), paired t-tests with Bonferroni, Cohen's d, ANOVA variance decomposition (p.10). The Sock-Shop paired t-test uses "50 failure situations" (p.10).
- Production case: 247 microservices (payments, authentication, fraud detection) on-premises plus AWS EKS, 6-month phased rollout: shadow mode 156 incidents with 89.1% agreement with a human, human-in-the-loop 94 proposals, full automation; MTTR 47 min to 4.3 min, 5.2% false positive rate, $1.2 million annual savings, 74x ROI (p.13). The organization, incident definitions and baselines are not described.
- Leakage and protocol: not described.

## 5. Results (copied; Tables 2-5)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Sock-Shop Top-1 / Top-3 / Top-5 / MRR | 71.2% / 91.3% / 94.3% / 0.798 | 61.1% / 84.5% / 91.0% / 0.719 | RUN | Table 2, p.10 |
| Sock-Shop Top-5 95% CI | [93.1%, 95.5%] | [89.5%, 92.5%] | RUN | Table 2 |
| Time on Sock-Shop (s) | 156 | 95 (RUN) | RUN | Table 2 |
| Scalability time at 1000 synthetic services | 892 s | 5,812 s (RUN); PC and RCD timeout | RUN | Table 3, p.11 |
| Ablation (top-5): without LLM reasoning | 87.2% (-7.1) | n/a | n/a | Table 4, p.11 |
| ECE | 0.043 vs RUN 0.089, RCD 0.156 | n/a | RUN | p.10, p.12 |
| Failure taxonomy (top-5 by type) | single 97.2%, cascading 83.4%, multi-root 78.1%, Byzantine 71.5%, novel 67.3% | n/a | n/a | Table 5, p.12 |
| Production | MTTR 47 to 4.3 min; false positives 5.2%; ROI 74x | none | none | p.13 |

- Statistical testing: paired t-tests, p less than 0.01 vs RCD and p less than 0.001 vs RUN (p.10); the abstract states p less than 0.01 and the final assessment p less than 0.001 with d = 0.85 (pp.1, 15).

## 6. Limitations
- Stated: novel failures (67.3%), incomplete observability (71.8%), cascades (83.4%), multi-root (78.1%), Byzantine faults (71.5%), LLM hallucination about 3%, temperature sensitivity of 8.4% (pp.12-14).
- **My critique (several checks I could do from the paper alone):**
  1. Internal numerical inconsistencies. (a) Sock-Shop timing: Table 2 gives AURORA 156 s, RUN 95 s, RCD 142 s, PC 1,247 s, while Table 3 gives the same Sock-Shop (15 services) as AURORA 1.8 s, RUN 3.1 s, RCD 4.2 s, PC 28 s. (b) The Table 2 top-5 recall CI [93.1%, 95.5%] is about +/-1.2 points; for a proportion near 94% a 95% binomial interval needs about 1,400 or more cases to be that narrow (with the stated 50 scenarios it would be about +/-6.4 points; with 500 about +/-2.0). (c) A top-5 recall of 94.3% cannot be k/50 (94% or 96%) or k/500 (94.2% or 94.4%). (d) The p-value is reported as less than 0.01 (abstract, p.10) and less than 0.001 (final assessment), with Cohen's d 0.85 against RCD in one place and 0.73 against RUN in another.
  2. The theorems are asserted with sketches, not proofs; Theorem 3's bound (error of the fused graph below the weighted average of modality errors) does not follow in general from edge voting; the O(n^2 log n) claim is accompanied by the remark "practical observations indicate near-quadratic scaling" while Section D states an experimental O(n log^2 n); no derivation connects the sample complexity to the reported runtime tables.
  3. The experimental systems for the large-scale claims (100 to 1000 services) are synthetic; the number of failure scenarios and their generation are not described; no code or data for the evaluation (the repository's top level shows no benchmark folder).
  4. The production case study (247 microservices, 91% MTTR cut, 74x ROI) is unattributed and unverifiable: organization, incident counts per phase beyond a few figures, the definition of MTTR, baselines and the $1.2 million savings are not substantiated; ROI is computed by dividing claimed savings by a cost that includes an API cost of about $150 per month.
  5. Supervised and learned components (fusion weights from "labeled occurrences", RL learning agent, 100 historical episodes needed) contradict a label-free framing; the abstract does not say so.
  6. Venue: the ISSN printed is that of Acta Scientiae, a science and mathematics education journal; I could not find the article in Crossref under that journal; the code repository's README cites the work as an "arXiv preprint". Publication status is unverified.
  7. References include blog posts and vendor pages ([4], [13]-[19], [22]-[25]) and six entries by the same unrelated author on network security and trading connectivity ([34]-[39], with [36] missing) that are not cited in the text I read; this looks like citation padding.
  8. RUN and RCD results "match published" figures but the paper does not report running their code on identical scenarios; RCD's published numbers are on other data.
  9. The theory section's "warning" sentence about identifiability is repeated verbatim four times (pp.6, 14, 16), indicating unedited text.
- Not discussed: labelled test scenarios for the LLM agent's variance across runs (only temperature sensitivity), cost per incident at scale, safety evaluation of remediation actions beyond approval gates.

## 7. Reproducibility
- Code: https://github.com/jay-gatech/agenticai-rca-langchain exists (checked 2026-10-07; MIT license; last push 2025-11-04; folders aurora (agents, api, causal_inference, config, integrations), deployment, scripts; scripts has run_local.py). No dataset or evaluation scripts for the 500 scenarios observed at the top level; I did not run it.
- Data: none released.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | partly supervised/learned | label-free | Ours cleaner; theirs mixed |
| Live / streaming | claims production use | incremental windows | Claim unverified |
| Telemetry used | metrics, logs, traces | traces (+ metrics, SSH) | Theirs broader |
| Propagation modelling | causal discovery + Granger + PageRank | edge probabilities | Theirs richer on paper; evidence unreliable |
| Forecasts future failures | no (future work) | claimed | n/a |
| Explanation | causal graph + LLM text | templates | Their LLM layer exists (3% hallucination reported) |
| Evaluation rigor | inconsistent numbers, synthetic scale tests | synthetic only | Neither; theirs less credible |
| Open / reproducible | code only | yes | Ours (data and tests) |

- **What they have that we do not:** an implemented LLM agent skeleton, causal-discovery ensemble, remediation hooks.
- **What we have that they do not:** consistent, honestly reported negative controls; label-free design.
- **Could a reviewer say "this already exists"?** Weakly: "LLM agents plus causal discovery" exists in several forms. The reliability of this paper's evidence is low.
- **Position:** do not cite as evidence of performance; at most as an example of an agentic RCA design with unverified results.
- **Must we run it as a baseline?** No (unreliable, API-dependent).

## 9. Does this paper change what problem we should solve?
- No. Its listing of its own failure modes (cascading 83.4%, multi-root 78.1%) is itself a statement (unsupported) that cascades are harder.

## 10. Citation-ready facts (each with page)
- None recommended as evidence. If needed: "A single-author preprint-style article proposes an LLM multi-agent framework combining hierarchical causal discovery, neural Granger causality and ReAct reasoning (pp.1-9)."

## 11. Open questions / things to verify
- Where (if anywhere) the paper was published; whether a valid DOI or arXiv entry exists.
- The related SSRN paper by the same author (Crossref lists "Agentic Artificial Intelligence for Root Cause Analysis and Self-Healing in Hybrid Distributed Financial Systems", SSRN 6003914, 2026) may be a version of this work.
- Figs 1-4; repository subfolders.
