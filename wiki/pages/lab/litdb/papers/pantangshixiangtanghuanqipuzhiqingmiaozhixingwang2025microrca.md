---
key: pantangshixiangtanghuanqipuzhiqingmiaozhixingwang2025microrca
title: "MicroRCA-Agent: Microservice Root Cause Analysis Method Based on Large Language Model Agents"
authors: "Tang, Pan; Tang, Shixiang; Pu, Huanqi; Miao, Zhiqing; Wang, Zhixing"
year: 2025
venue: "arXiv:2509.15635v1 [cs.AI], 19 Sep 2025 (technical report of a solution at the 2025 CCF International AIOps Challenge)"
publisher: "arXiv"
doc_type: preprint
doi: ""
issn: ""
scopus_indexing: "not indexed (arXiv preprint)"
scopus_match: ""
sjr_quartile: "n/a"
peer_reviewed: "no (preprint; competition technical report)"
cited_by_crossref: ""
n_references: "2"
license: "arXiv"
batch: "2"
read_status: reviewed                  # prompts (Figs 13, 16, 18) and good/bad case figures (19-22) are images, not read
pages: 18
text_chars: 68743
metadata_source: arxiv
task: "localization (component) + cause text; LLM agent pipeline"
supervision: "label-free pre-processing (Drain, Isolation Forest) + zero-shot LLM reasoning; competition phase-one data used to build Drain templates and detectors"
online_or_streaming: "no (offline per-fault time window given in the input)"
telemetry: "logs, traces, metrics (APM 7, infra pod 9 and node 16, TiDB 14)"
propagation_modeling: "none explicit (LLM reasons over summaries; call relations only as parent-child pod pairs in trace anomalies)"
forecasts_future_failures: "no"
llm_used: "yes (summarization of metrics in two stages, and final root cause reasoning; model not named in the paper; the repo README says to configure DeepSeek API keys)"
systems_evaluated: "one competition environment (e-commerce microservices on Kubernetes with TiDB, 2025 CCF AIOps Challenge)"
datasets: "challenge phase-one (training) and phase-two data; no statistics on size given in the paper"
dataset_open: "partly (phase-one URL cited, https://www.aiops.cn/gitlab/aiops-live-benchmark/phaseone/; not checked)"
code_open: "yes (github.com/tangpan360/MicroRCA-Agent, verified, no license file, last push 2026-01-14)"
baselines_compared: "none (ablation over modality combinations only)"
metrics: "challenge score (definition not given in the paper)"
headline_result: "final score 50.71 for log+trace+metric; 51.27 for log+metric; metric-only 42.78 (Table 1, p.16)"
evidence_quality: "1"
relevance_to_us: "3"
overlap_with_us: "partial (the LLM explanation layer idea; not label-free forecasting)"
threat_level_for_novelty: "low (for RCA); medium for the 'LLM-assisted RCA' framing"
---

# MicroRCA-Agent: Microservice Root Cause Analysis Method Based on Large Language Model Agents

> Reading notes written from the **full text** (`litdb/texts/...microrca.txt`). Page numbers are PDF pages.
> Not read: the prompt images (Figs 13, 16, 18, in Chinese per p.11) and the good/bad case figures (Figs 19 to 22, pp.15 and 17).

## 1. One-paragraph summary
A competition solution report. For each fault window (start and end time are given in the input), it (a) compresses error logs into Drain templates with counts, (b) finds trace anomalies with per-call-pattern Isolation Forests trained on normal-looking windows plus a status-code check, (c) filters metrics by a symmetric-ratio change test and asks an LLM to summarize them in two stages, then (d) gives all three summaries to an LLM that outputs the faulty component, a reason and a reasoning trace. It reports a challenge score of 50.71 and a modality ablation.

## 2. Problem and motivation
- Problem: localize the fault component and cause for faults in a microservice system with logs, traces and metrics (p.1).
- Motivation: practical competition task; no incident-cost or labelling-cost evidence. Evidence type: assumed.
- Real? Not argued; it is a competition setup.

## 3. Method
- Preprocessing: regex extraction of fault start and end times from the anomaly description, conversion of all modalities to 19-digit nanosecond timestamps (pp.3-4).
- Logs (pp.4-6): keep logs in the window, keep those containing "error", reduce to node, pod, message; match to 156 Drain templates learned from phase-one error logs; deduplicate by pod and template with counts; map pod to service.
- Traces (pp.6-8): for each (parent pod, child pod, operation) train an Isolation Forest (n_estimators 100, contamination 0.01) on 30-second window averages; training data = 40 minutes after the end of each of 50 randomly selected phase-one faults, assumed normal; plus status check (status.code not 0); report the top 20 duration anomalies and top 20 status anomalies.
- Metrics (pp.8-13): normal period defined as the windows before and after the fault (from 10 minutes after the previous fault ended to the fault start, and from 10 minutes after this fault to the next fault start); the two largest and two smallest values are excluded; symmetric ratio of P50 and P99 (Eq.1) between fault and normal; metrics changing under 5% are dropped (claimed to cut about 50% of tokens); two-stage LLM summarization (APM+TiDB first, then pods and nodes), "phenomenon only, no fault judgment" (p.9).
- Final reasoning (pp.14-16): one prompt with the three summaries, output JSON with component, reason, reasoning trace; regex and JSON validation, retries.
- Hyper-parameters: as above; LLM model, temperature and prompt wording not in the text.
- Assumptions: fault time window known; normal periods exist before and after each fault in the data; faults are rare and separated.

## 4. Data and setup
- 2025 (8th) CCF International AIOps Challenge environment: Online-Boutique-like services (frontend, cartservice, checkout), Kubernetes nodes, TiDB (pp.1, 4 to 10). No counts of faults, services or days in the paper.
- Fault types: not enumerated in the paper.
- Protocol: phase-one data for Drain and Isolation Forest training; evaluation on the competition scoring (phase two) (footnote 2 p.5); the scoring formula is not stated.
- Leakage: the normal baseline for metrics uses periods **after** the fault as well as before it, which a live system does not have; the trace detector is trained on windows after other faults.
- Hardware and runtime: not reported.

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Challenge score, log+trace+metric | 50.71 | none | no baselines | Table 1, p.16 |
| Metric only | 42.78 | n/a | n/a | Table 1 |
| Trace only / log only | 31.09 / 23.59 | n/a | n/a | Table 1 |
| Log+metric | 51.27 | n/a | n/a | Table 1 |
| Trace+metric / log+trace | 48.58 / 35.32 | n/a | n/a | Table 1 |

- Statistical testing: none; single score per configuration.
- Ablations: modality combinations only; no ablation of the LLM, the filters, or the Isolation Forest.
- Efficiency: not reported (claims a multi-processing strategy, p.2).
- The unit of "score" is not defined in the paper (maximum and meaning unknown).

## 6. Limitations
- Stated: LLM hallucination in a bad case (trace chains not given to the model but cited in its reasoning, p.16); plan to add retrieval and jury mechanisms; keyword filter for logs should be improved.
- **My critique:**
  1. It is a competition technical report with no baselines and an undefined score, so it gives no general accuracy evidence.
  2. 50.71 is the full system; the best ablation (log+metric, 51.27) is higher, so the claimed benefit of the trace module is not supported by their own table.
  3. The LLM model is not named; stochastic outputs, no repeated runs or variance.
  4. Baseline periods use data after the fault; Isolation Forest training windows assumed normal because they follow a fault.
  5. No ablation shows that the LLM step beats a simple ranking of the anomaly summaries.
  6. Two references only; no related work section.
  7. The explanation layer is the LLM's own reasoning, with no faithfulness check (the paper itself shows a hallucinated reasoning chain).
- Not discussed: fault-time detection (given as input), cost, reproducibility of LLM outputs.

## 7. Reproducibility
- Code: https://github.com/tangpan360/MicroRCA-Agent exists (checked 2026-10-07; 269 stars; last push 2026-01-14; no license file; contains src, submission, Dockerfile, run.sh, README in English and Chinese). README tells users to supply a DeepSeek API key. Not run.
- Data: the cited phase-one URL (https://www.aiops.cn/gitlab/aiops-live-benchmark/phaseone/) was not checked; the challenge site responds (HTTP 200).

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | no failure labels; uses competition phase-one data to fit templates and detectors | label-free calibration on a baseline window | Similar spirit; ours fits only on a clean window of the same system |
| Live / streaming | offline per fault window | incremental windows | Ours is closer to live |
| Telemetry used | logs, traces, metrics, TiDB | traces (+ metrics) | Theirs broader |
| Propagation modelling | none explicit | edge probabilities | Ours has a model; theirs delegates to the LLM |
| Forecasts future failures | no | risk score, untested | Neither |
| Explanation | LLM reasoning trace (hallucination seen) | templates (LLM layer not built) | Theirs exists but unverified |
| Evaluation rigor | single score, no baselines | synthetic only | Both weak |
| Open / reproducible | code yes | yes | Comparable |

- **What they have that we do not:** an end-to-end multimodal pipeline with LLM explanations, released as code.
- **What we have that they do not:** a propagation model, honest negative controls, an evaluation plan with baselines.
- **Could a reviewer say "this already exists"?** For "LLM on top of anomaly summaries to explain RCA": yes, many such systems exist; this is one example, not strong evidence.
- **Position:** "LLM-based RCA pipelines exist (e.g., MicroRCA-Agent); we use the LLM only to verbalize a ranking produced by a non-LLM scorer."
- **Must we run it as a baseline?** No (competition-specific, API-dependent, undefined score).

## 9. Does this paper change what problem we should solve?
- It does not. It shows the LLM-agent route is popular, but its evidence is a competition score. It supports the REVIEW_REPORT point that an LLM should sit on top of a detector, as here, where Isolation Forest and statistical filters do the detection.
- Evidence the problem is real: none offered.

## 10. Citation-ready facts (each with page)
- MicroRCA-Agent combines Drain log templates, Isolation Forest plus status-code checks on traces, and LLM summarization of filtered metrics, and ends with an LLM that outputs component, reason and reasoning trace (pp.1-2, 14-16).
- It reports a challenge score of 50.71 on a competition dataset; the best modality combination in its ablation was log+metric at 51.27 (Table 1, p.16).
- The authors observed LLM hallucination in a bad case (p.16).
- It is a technical report for the 2025 CCF International AIOps Challenge (footnote p.1).

## 11. Open questions / things to verify
- LLM model and prompts (Figs 13, 16, 18); score definition from the challenge site.
- Whether phase-one data is public (URL not checked).
