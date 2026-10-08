---
key: wang2024rcagent
title: "RCAgent: Cloud Root Cause Analysis by Autonomous Agents with Tool-Augmented Large Language Models"
authors: "Zefan Wang; Zichuan Liu; Yingying Zhang; Aoxiao Zhong; Jihong Wang; Fengbin Yin; Lunting Fan; Lingfei Wu; Qingsong Wen"
year: 2024
venue: "CIKM '24, Boise, ID (ACM); arXiv 2310.16340v3 read"
publisher: "ACM"
doc_type: proceedings-article
doi: "10.1145/3627673.3680016"
issn: ""
scopus_indexing: "unverified: CIKM proceedings not checked in the Scopus preview"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (CIKM '24; arXiv v3 read)"
cited_by_crossref: ""
n_references: "about 63"
license: ""
batch: "10"
read_status: reviewed                  # full text read; references skimmed; Figs 1-5 not inspected
pages: 9
text_chars: 57761
metadata_source: crossref+arxiv
task: "LLM-agent RCA for Flink job failures: root cause, solution, evidence, responsibility (text outputs)"
supervision: "zero-shot LLM (Vicuna-13B) with tools; labels (rule-derived and SRE-proofread) only for evaluation"
online_or_streaming: "deployed to analyse out-of-domain job failures (claimed); offline evaluation"
telemetry: "logs (platform, runtime, infrastructure), advisor database, code repositories"
propagation_modeling: "none"
forecasts_future_failures: "no"
llm_used: "yes (Vicuna-13B-v1.5-16k locally deployed; GPT-4-0613 as judge)"
systems_evaluated: "Alibaba Cloud Real-time Compute Platform for Apache Flink (not microservices)"
datasets: "161 jobs (offline, class-balanced from about 5,000 non-trivial of 15,616 anomalous jobs); online out-of-domain jobs labelled by SREs (count not stated)"
dataset_open: "no"
code_open: "no"
baselines_compared: "ReAct, XGBoost on embeddings, fine-tuned T5, LLM summary"
metrics: "METEOR, BLEURT, BARTScore, EmbScore, GPT-4 G-Correctness / G-Helpfulness, human H-Helpfulness, responsibility precision"
headline_result: "root cause METEOR 15.15 vs ReAct 6.44; G-Correctness 5.22 vs 3.06 (Table 1 p.5); online human helpfulness 2.92 of 5 with TSC (Table 5 p.7)"
evidence_quality: "2"
relevance_to_us: "2"
overlap_with_us: "low (LLM agent over logs for Flink jobs; no propagation)"
threat_level_for_novelty: "low"
---

# RCAgent (Wang et al., CIKM 2024)

> Notes from the **full text** (arXiv v3, 9 pages). Page numbers are PDF pages. Figures not inspected.

## 1. Summary
A tool-augmented ReAct-style LLM agent on a locally hosted 13B model answers four questions about failed Flink jobs on Alibaba Cloud: root cause, solution, evidence and responsibility. Additions: observation snapshot keys to handle long logs, LLM-based code and log "expert agents", JSON repair, and trajectory-level self-consistency. Compared with plain ReAct and non-agent baselines using text-similarity metrics, a GPT-4 judge and human ratings.

## 2. Problem and motivation
- Existing LLM RCA uses GPT-family APIs (privacy) or workflows without autonomy (pp.1-2). Motivation is from citations.

## 3. Method (pp.2-4)
- Controller agent with thought-action-observation cycle; semantically minimalist tools; code and log expert agents; JsonRegen; error messages for bad actions; trajectory-level self-consistency (TSC) aggregation by embeddings or an LLM.

## 4. Data and experimental setup (pp.5-6)
- Offline: 161 jobs after class balancing (no more than two jobs with the same root cause) from about 5,000 non-trivial jobs; reference answers first written by an LLM summarizing rule outputs of Flink Advisor and then proofread by SREs (p.5). Data after detection time are hidden from tools.
- Judge: GPT-4-0613 scores 0-10 (G-Correctness, G-Helpfulness). Online: out-of-domain jobs labelled by SREs; human helpfulness 0-5.

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Root cause METEOR / G-Correctness | 15.15 / 5.22 (RCAgent); 16.49 / 5.47 (TSC) | 6.44 / 3.06 | ReAct | Table 1 p.5 |
| Solution METEOR / G-Helpfulness | 12.94 / 5.48; 16.45 / 5.69 (TSC) | 6.42 / 3.41 | ReAct | Table 2 |
| Trajectory pass rate / invalid rate | 99.38% / 7.93% | 86.33% / 22.82% | ReAct | Table 4 p.6 |
| Online responsibility precision | 80.74% (RCAgent); 82.06% (TSC) | 77.85% | Finetune T5 | Table 5 p.7 |
| Online human helpfulness | 2.47 +/- 0.17; 2.92 +/- 0.21 (TSC) | 1.36 +/- 0.03 | ReAct | Table 5 |

## 6. Limitations
- Stated: privacy trades off model strength; context length; action validity (p.2). No limitations section proper.
- **My critique:**
  1. Task is Flink job failures and text answers, not microservice localization; no top-k or localization accuracy.
  2. Evaluation relies on METEOR/BLEURT-type scores, a GPT-4 judge, and a human helpfulness rating of 2.92 out of 5 ("moderate support"); references for the offline set are LLM-summarized rule outputs, which may bias toward rule-style text.
  3. Offline set is 161 jobs; the online set size is not given; no intervals except across SC samples.
  4. ReAct baseline (zero-shot, local 13B) is a weak comparison: its pass rate is 86% and the paper itself notes ReAct scores below classical methods on the online set (p.7).
  5. Proprietary data and system; no code.
- Not discussed: cost per case beyond a scaling plot; hallucination rate on evidence beyond a fuzzy-matching filter.

## 7. Reproducibility
- Not reproducible: proprietary platform, data and code.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | zero-shot LLM | none | tie |
| Live / streaming | deployed (claimed) | incremental | theirs (claimed) |
| Telemetry used | logs, code, advisor DB | traces (+ metrics) | different |
| Propagation modelling | none | edge probabilities | ours |
| Forecasts future failures | no | claimed | n/a |
| Explanation | free-text root cause, solution, evidence | templates | theirs (unverified faithfulness) |
| Evaluation rigor | LLM-judge, small | synthetic | neither |
| Open / reproducible | no | yes | ours |

- **What they have that we do not:** natural-language explanation with evidence and an expert-agent design for long logs.
- **What we have that they do not:** localization on service graphs with propagation and cascade-risk output; open code.
- **Could a reviewer say "this already exists"?** For "LLM agents for RCA explanation": yes. Not for propagation-aware localization.
- **Position:** cite as LLM-agent RCA prior art in industry; do not use its numbers.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- No. It indicates that evidence-grounded LLM explanations are being deployed; our explanation layer (templates) should state its faithfulness checks (cited evidence must appear in the input, as in its fuzzy-match filter).

## 10. Citation-ready facts (each with page)
- "RCAgent runs a ReAct-style agent on a locally hosted 13B model for Flink job RCA and reports human helpfulness of 2.92 out of 5 on online out-of-domain jobs (Table 5 p.7)".
- "It filters hallucinated evidence by fuzzy-matching quoted evidence to the log chunk (p.4)".

## 11. Open questions / things to verify
- Online set size; whether the CIKM version differs from arXiv v3.
