---
key: chen2024automatic
title: "Automatic Root Cause Analysis via Large Language Models for Cloud Incidents (RCACopilot)"
authors: "Yinfang Chen; Huaibing Xie; Minghua Ma; Yu Kang; Xin Gao; Liu Shi; Yunjie Cao; Xuedong Gao; Hao Fan; Ming Wen; Jun Zeng; Supriyo Ghosh; Xuchao Zhang; Chaoyun Zhang; Qingwei Lin; Saravan Rajmohan; Dongmei Zhang; Tianyin Xu"
year: 2024
venue: "EuroSys '24, Athens (ACM); arXiv 2305.15778v4 read"
publisher: "ACM"
doc_type: proceedings-article
doi: "10.1145/3627703.3629553 (printed); the literature matrix key 'ahmed2023llmrca' and DOI 10.48550/arxiv.2305.15778 refer to this same paper"
issn: ""
scopus_indexing: "unverified: EuroSys proceedings not checked in the Scopus preview"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (EuroSys '24; arXiv v4 read)"
cited_by_crossref: ""
n_references: "about 61"
license: ""
batch: "11"
read_status: reviewed                  # text read through Sec 5.4 (page 12); remainder (deployment discussion, references) skimmed only; Figs not inspected
pages: 17
text_chars: 0
metadata_source: arxiv
task: "incident root cause CATEGORY prediction and explanation (not service localization)"
supervision: "few-shot LLM (GPT-4) with nearest-neighbour demonstrations from labelled history; handlers hand-built by on-call engineers"
online_or_streaming: "collection component deployed 4+ years in 30 teams; prediction component in preliminary deployment (claimed)"
telemetry: "logs, exception stacks, socket metrics, probes via per-alert-type handlers"
propagation_modeling: "none"
forecasts_future_failures: "no"
llm_used: "yes (GPT-4 and GPT-3.5-turbo; FastText embeddings trained on incidents)"
systems_evaluated: "Microsoft Transport (email) service, one year: 653 incidents"
datasets: "653 incidents labelled by OCEs; 75% train, 25% test"
dataset_open: "no"
code_open: "no"
baselines_compared: "XGBoost, FastText, fine-tuned GPT-3.5, GPT-4 prompt only, GPT-4 with GPT embeddings"
metrics: "micro-F1, macro-F1, time"
headline_result: "RCACopilot (GPT-4) micro-F1 0.766, macro-F1 0.533 vs fine-tuned GPT 0.103 / 0.144, XGBoost 0.022 / 0.009 (Table 2 p.11)"
evidence_quality: "2"
relevance_to_us: "2"
overlap_with_us: "low (incident classification with LLM; no propagation)"
threat_level_for_novelty: "low"
---

# RCACopilot (Chen et al., EuroSys 2024)

> Notes from the **full text** (arXiv v4). Read in detail through page 12; the deployment lessons and references skimmed only. Page numbers are PDF pages. Figures not inspected. The literature matrix lists this paper under the key `ahmed2023llmrca` (a different first author: Ahmed et al. is a separate ICSE 2023 paper cited here as ref [1]); that attribution is wrong.

## 1. Summary
An on-call system in which engineers build per-alert-type "incident handlers" (decision-tree workflows of data-collection actions); the collected diagnostic text is summarized by an LLM and a GPT-4 few-shot prompt, with nearest historical incidents as demonstrations, predicts the root cause category and writes an explanation. Evaluated on one year of 653 incidents of one Microsoft service.

## 2. Problem and motivation
- Troubleshooting guides are manual, outdated and incomplete (pp.3-4). Insights from the dataset: 93.80% of recurring incidents reappear within 20 days; 24.96% (163 of 653) have a new root cause category (pp.4-6). Single-service statistics.

## 3. Method (pp.6-9)
- Handler actions: scope switching, query, mitigation. Embedding by FastText trained on past incidents; similarity combines Euclidean distance and temporal decay (alpha 0.3, K 5); GPT summary 120-140 words; multiple-choice prompt with option "unseen incident".

## 4. Data and experimental setup (pp.10-11)
- 653 incidents from Transport; root cause categories assigned manually by OCEs; 75/25 train-test split; GPT-4 default; three rounds per experiment.

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Micro-F1 / Macro-F1 | 0.766 / 0.533 (GPT-4); 0.761 / 0.505 (GPT-3.5) | 0.257 / 0.122 | GPT-4 with GPT embeddings | Table 2 p.11 |
| Fine-tuned GPT | n/a | 0.103 / 0.144 | n/a | Table 2 |
| XGBoost / FastText | n/a | 0.022 / 0.009; 0.076 / 0.004 | n/a | Table 2 |
| Diagnostic info alone vs summarized | 0.689 / 0.510 vs 0.766 / 0.533 | n/a | n/a | Table 3 p.12 |
| Inference time | 4.205 s (GPT-4) | 0.524 s (FastText) | n/a | Table 2 |

## 6. Limitations
- Stated: (not read in the tail).
- **My critique:**
  1. The task is classification of incident root-cause category, not localization; accuracy cannot be compared with service-level RCA.
  2. Test set is about 25% of 653, roughly 160 incidents with a long-tailed category distribution (Fig 3); no confidence intervals; macro-F1 0.533.
  3. Baseline scores are extremely low (XGBoost micro-F1 0.022, GPT-4 prompt 0.026), well below what a majority-class or nearest-neighbour rule would reach on a dataset where about 75% of incidents belong to previously seen categories (100% minus 24.96% new, p.6); this suggests the baselines were not configured to exploit history, which inflates the headline gap.
  4. Handlers are hand-built per alert type, so the pipeline carries the manual effort the paper aims to remove.
  5. Single service of one company; data and code not released.
  6. Time-split vs random split of the 75/25 split is not stated in the part I read.
- Not discussed: calibration of the "unseen incident" option; cost of GPT-4 calls at scale.

## 7. Reproducibility
- Not reproducible (proprietary data, no code).

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | labelled history + hand-built handlers | none | ours |
| Live / streaming | deployed (claimed) | incremental | theirs (claimed) |
| Telemetry used | logs, stacks, metrics | traces (+ metrics) | different |
| Propagation modelling | none | edge probabilities | ours |
| Forecasts future failures | no | claimed | n/a |
| Explanation | LLM narrative | templates | theirs |
| Evaluation rigor | one service, no CIs | synthetic | neither |
| Open / reproducible | no | yes | ours |

- **What they have that we do not:** an LLM explanation layer integrated with an on-call workflow.
- **What we have that they do not:** a localization method on service graphs; open artifacts.
- **Could a reviewer say "this already exists"?** For LLM-based incident RCA explanation: yes.
- **Position:** cite as LLM incident-classification prior art (used by Vangapelli as "76.6% accuracy"; the paper's figure is micro-F1 on its own incident categories).
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- No. It supports (single-company) that most incidents recur within weeks and a quarter are new, which bears on label-free methods for novel failures.

## 10. Citation-ready facts (each with page)
- "In a year of 653 incidents of a Microsoft email service, 24.96% belonged to a new root cause category and 93.80% of recurring incidents reappeared within 20 days (pp.5-6)".
- "RCACopilot reports micro-F1 0.766 and macro-F1 0.533 for root cause category prediction on 25% held-out incidents (Table 2 p.11)".

## 11. Open questions / things to verify
- Split protocol; deployment section; why baselines score so low; the DOI/venue match for the arXiv v4.
