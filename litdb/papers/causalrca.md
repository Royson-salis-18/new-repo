---
key: causalrca
title: "CausalRCA: Causal inference based precise fine-grained root cause localization for microservice applications"
authors: "Ruyue Xin, Peng Chen, Zhiming Zhao"
year: 2023
venue: "The Journal of Systems & Software, vol. 203, article 111724"
publisher: "Elsevier"
doc_type: journal-article
doi: "10.1016/j.jss.2023.111724 (printed on page 1)"
issn: "0164-1212 (from the printed front matter 'ISSN 0164-1212/' as seen; not yet checked in Scopus)"
scopus_indexing: "unverified: ISSN not yet checked in the Scopus preview"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (journal; received 15 July 2022, accepted 19 April 2023, online 6 May 2023, as printed)"
cited_by_crossref: ""
n_references: ""
license: "CC BY 4.0 (printed)"
batch: "7"
read_status: partial                   # page 1 (abstract, intro start) and page 2 (intro, contributions) read from screenshots; pages 3-13 NOT read
pages: 13
text_chars: 0
metadata_source: pdf-visual
task: "fine-grained root cause metric localization (service plus metric)"
supervision: "likely label-free (anomaly detection then gradient-based causal structure learning); unverified, methods section not read"
online_or_streaming: "claims real-time; unverified"
telemetry: "metrics (service latency and resource metrics)"
propagation_modeling: "weighted causal graph from gradient-based causal structure learning; ranking along the graph (details unread)"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "Sock-Shop (per intro)"
datasets: "unread"
dataset_open: "abstract states code and data are in a GitHub repository (not checked)"
code_open: "stated in abstract; repository not checked"
baselines_compared: "unread (abstract says 'baseline methods')"
metrics: "AC@k / Avg@k"
headline_result: "abstract: average AC@3 of fine-grained root cause metric localization in the faulty service 0.719, average increase 10% vs baselines, Avg@5 improved by 9.43% (p.1); the intro (p.2) words the 9.43% as AC@5"
evidence_quality: "unrated (not fully read)"
relevance_to_us: "3"
overlap_with_us: "partial (causal-graph RCA on metrics)"
threat_level_for_novelty: "low-medium"
---

# CausalRCA (Xin, Chen, Zhao, JSS 2023)

> **Partial read.** The PDF is a scan with no extractable text. I read page 1 and page 2 (abstract, introduction, contributions) from screenshots in the browser pane; the viewer then stopped rendering reliably and pages 3-13 (related work onward, method, experiments, discussion) were NOT read. Nothing below goes beyond pages 1-2. Please treat all unread fields as unknown.

## 1. Summary (from abstract and intro only)
Proposes CausalRCA, a framework that builds a weighted causal graph of monitoring metrics with gradient-based causal structure learning and ranks root cause metrics, targeting fine-grained (service plus metric) localization. Evaluated on the Sock-Shop microservice benchmark per the introduction.

## 2. Problem and motivation (pp.1-2)
Coarse-grained localization only finds the faulty service; fine-grained localization also names the metric (for example memory use), which supports better recovery actions. Existing causal-inference RCA is said to depend on linear causal assumptions and strict data distributions (p.1). Motivation is argued from citations, not data.

## 3. Claims (copied, p.1-2)
AC@3 average 0.719 for fine-grained metric localization in the faulty service, about 10% above baselines; Avg@5 up 9.43% (abstract); intro says 9.43% is AC@5. Contributions: automated real-time framework, gradient-based causal structure learning for linear and non-linear relations, coarse and fine-grained experiments.

## 4. Critique (limited)
- Metric naming is inconsistent between abstract (Avg@5) and intro (AC@5); to check against the experiments.
- "Real-time" is claimed; unverified.
- Everything about data, baselines, injected faults, repetitions and statistics is unread.

## 5. Comparison with our work
Same family as CIRCA/RCD/BARO-type causal metric RCA; label-free in spirit. Our propagation-aware scoring would need to be compared against it only if it is part of RCAEval-style baselines (not confirmed here).

## 6. Does it change our problem?
Not on the evidence read. It adds to "causal-graph RCA on metrics exists"; Pham et al. (batch 2) found such methods often no better than simple baselines, which applies as a caution.

## 7. To verify (needs a legible read of pages 3-13)
Experimental design, baselines, fault types, number of runs, leakage, code repository, whether metric-level labels are used, Scopus status of ISSN 0164-1212.
