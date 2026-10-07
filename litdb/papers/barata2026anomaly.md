---
key: barata2026anomaly
title: "Anomaly detection and root-cause identification in microservices: a survey"
authors: "Barata, Luís M.; Sequeira, Sérgio; Lopes, Eurico; Inácio, Pedro R. M.; Freire, Mário M."
year: 2026
venue: "Cluster Computing 29:309"
publisher: "Springer Nature"
doc_type: journal-article
doi: "10.1007/s10586-026-06095-9"
issn: "1386-7857, 1573-7543"
scopus_indexing: "indexed (manual check of Scopus Sources preview by ISSN, 2026-10-07; CiteScore 2025 = 8.4, 82nd percentile, rank 98/568 Computer Networks and Communications)"
scopus_match: "ISSN 1386-7857, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied (Scopus preview shows SJR 2025 = 1.014, quartile not displayed)"
peer_reviewed: "yes (received 14 Jun 2025, revised 2 Mar 2026, accepted 4 Mar 2026, published online 3 Jun 2026, p.1)"
cited_by_crossref: ""
n_references: "about 250"
license: "CC BY 4.0"
batch: "3"
read_status: reviewed                  # Figs 1-11 not inspected; reference list (about 250 entries) skimmed by search, not read
pages: 42
text_chars: 236859
metadata_source: crossref
task: "survey (PRISMA systematic review of anomaly detection and root-cause identification)"
supervision: "n/a (survey)"
online_or_streaming: "n/a"
telemetry: "logs, traces, monitoring metrics"
propagation_modeling: "n/a (surveys graph-based, statistical and ML RCI)"
forecasting_note: "none"
forecasts_future_failures: "no (not a focus)"
llm_used: "no"
systems_evaluated: "n/a (tabulates testbeds: Train Ticket, Sock Shop, Hipster-Shop, DeathStar etc.)"
datasets: "Table 9 lists datasets (AIOps Challenge 2020/2021, GAIA, TraceRCA, HDFS, etc.)"
dataset_open: "n/a"
code_open: "replication package cited as [54]; not checked"
baselines_compared: "none"
metrics: "tables of reported values copied from studies; averages across studies in Sec. 4.7"
headline_result: "117 studies per abstract (143 per Sec. 4.1.4); 86% published 2020-2024; 70% from Chinese institutions; Sec. 4.7 averages of reported metrics across heterogeneous studies"
evidence_quality: "2"
relevance_to_us: "3"
overlap_with_us: "partial (taxonomy, testbed and dataset tables)"
threat_level_for_novelty: "low"
---

# Anomaly detection and root-cause identification in microservices: a survey

> Reading notes written from the **full text** (`litdb/texts/barata2026anomaly.txt`). Page numbers are PDF pages (article pages 1 to 42).
> Figs 1-11 not inspected. The reference list (about 250 entries, pp.32-41) was searched for key terms but not read entry by entry. The page order in the extracted text is sometimes interleaved (columns); I read the content in extracted order.

## 1. One-paragraph summary
A PRISMA-style survey of anomaly detection and root-cause identification in microservice systems. It describes data collection (logs, traces, monitoring), detection methods (unsupervised, supervised, reinforcement learning, trace comparison, statistical), anomaly types, root-cause methods (ML, graph, statistical), testbeds and datasets, and then averages the reported metrics of selected studies by method category. It ends with future directions including trusted execution environments and "Trusted Distributed AI", and a table of proposed trust indicators.

## 2. Problem and motivation
- Problem: monitoring, detecting anomalies and identifying root causes in dynamic microservice systems (pp.1-3).
- Motivation evidence: Alibaba manages more than 30,000 services (cites [7]); "Amazon lost millions of dollars during outages in 2013 and 2018" (cites [17, 18]); Walmart's monolith collapsed during peaks before moving to microservices (cites [19]) (p.2). These are anecdotal and second-hand; no numbers are given for the Amazon losses in the text.
- Real? Asserted with anecdotes. The survey also states that faults "can propagate rapidly along service call chains" and calls for preventing cascading failures (p.2), without evidence.

## 3. Method (of the survey)
- PRISMA process (pp.8-9): seven libraries (IEEE Xplore, ACM DL, ScienceDirect, Wiley, Springer Link, Scopus, Web of Science); search December 2021 to May 2025; keywords in Table 4 (p.8): "microservice* abnormal*", "microservices fail*", "microservice* fault*", "microservice AND anomalies", "microservice* AND abnormal*", "micro-service* abnormal*", "microservice anomalies", dated 2012 to 2025; 10,485 records found; 9,648 discarded after de-duplication and basic exclusions; 837 screened by title; 306 after abstract screening (531 excluded); 171 read in full; 143 included (141 plus 2 from citations); 63 from initial search plus 80 added via alerts (p.9).
- Classification: data collection (log, trace, monitoring), detection method (UL, SL, RL, trace comparison, statistical), RCI method (ML, graph, statistical), anomaly type (workflow, performance, security) (Tables 5-7).
- Comparison (Sec. 4.7, pp.22-23): "we selected those with more than 80% values in the most frequent metrics", averaged values per category and read off which category "performs better".
- Trust analysis: four dimensions (reliability, explainability, consistency, robustness) and Table 10 of proposed indicators (DSI, RCRV, CIS, NDR, FAR, PSI, DCR) (p.30); T = f(R, Ro, C, E) (p.30).

## 4. Data and experimental setup
- No experiments. The paper tabulates works with the reported metrics (Tables 5 to 7, pp.15-19).
- Testbeds (Table 8, p.21): Train Ticket used by the largest number of studies, then Sock Shop (19 cited), Hipster-Shop, DeathStar, PyMicro and others; proprietary platforms such as Alibaba EagleEye, IBM Bluemix, Meituan.
- Datasets (Table 9, p.22): AIOps Challenge 2020 and 2021 (9 publications), GAIA, TraceRCA dataset, HDFS, BGL, SMD, MicroCU and others; several marked proprietary. Note the table marks GAIA as "Proprietary" although CHASE (batch 2) cites a public GAIA repository.

## 5. Results (copied; survey statistics)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Studies by year | 86% published between 2020 and 2024 | n/a | n/a | p.10 |
| Studies by country | 70% Chinese institutions, Canada 6%, Portugal 3%, USA 3% | n/a | n/a | p.10 |
| Detection method share | machine learning 70% of detection methods | n/a | n/a | p.25 |
| Mean performance by RCI class | ML: precision 94.9%, recall 98.0%, F1 99.0%, accuracy 94.3%; graph-based: precision 92.7%, recall 89.7%; statistical: precision 85.0%, recall 88.0%, F1 85.8%, accuracy 99.0% | n/a | n/a | p.23 |
| Top-5 detection methods named | tree-matching [14], deep variational Bayesian network [78], SVM [95], VGAE+LSTM-AE [11], GAT [83] (by reported values) | n/a | n/a | p.27 |
| Top-5 RCI methods named | MLP [137], metric causality graph [97], RPCA [94], SBFL [81], PageRank value [160] | n/a | n/a | p.28 |

- Statistical testing: none.
- The survey's own caution: "it isn't easy to compare the performances of various methods" because of different datasets and missing metrics (p.28), and "direct performance comparisons should be interpreted with caution" (p.31, limitations).

## 6. Limitations
- Stated (p.31): English only, 2012 to May 2025; possible selection bias; heterogeneity makes direct performance comparison unreliable; new methods after cut-off missed.
- **My critique:**
  1. Internal inconsistency in counts: abstract and Sec. 2 say 117 studies included (1,700 results reviewed); Sec. 4.1.4 reports 10,485 records and 143 included.
  2. Search terms omit "root cause", "RCA", "failure diagnosis", "cascad*" and "propagation": the keyword list centres on anomaly, abnormal, fault, fail (Table 4). The survey therefore likely under-samples RCA-only work and the very literature on propagation and forecasting that matters to us.
  3. The cross-study averaging in Sec. 4.7 filters to values above 80%, mixes datasets and metrics, and then ranks categories (e.g., "log-based is the most accurate data collection method"; "statistical is the top detection method"); this is selection-biased and not a valid comparison, despite the authors' own caveat. Conclusions drawn from it in the discussion (p.27) should not be cited.
  4. "Top five" method lists rank by self-reported numbers from different datasets.
  5. Pham et al. 2024 (ref [176]) is listed in Table 6 as a method row with "n.a" performance, rather than recognised as an evaluation study; DeepHunt, Eadro, Nezha and BARO do not appear in the text (a search found none).
  6. The "trust indicators" in Table 10 are newly named indices (DSI, RCRV, CIS, NDR, FAR, PSI, DCR) with no definition equations and no application to the surveyed studies; Sec. 6.1 and 6.2 on TEEs and trusted distributed AI are loosely connected to the evidence reviewed.
  7. The Table 5 and Table 6 footnotes are scrambled (letters a to e re-used in different orders across tables), making column meanings error-prone.
  8. Motivating claims (Amazon losses, Walmart) are anecdotal.
  9. 70% of included studies are from Chinese institutions (reported), which the authors attribute to large author teams; geographic concentration is noted but not analysed for dataset overlap.
- Not discussed: label requirements of methods as a classification axis (it uses UL, SL, RL), benchmark validity, cascade forecasting.

## 7. Reproducibility
- Replication package referenced as [54] ("documentation and source data"), p.9; I did not look it up (unverified).
- Data availability statement: "No datasets were generated or analysed" (p.32).

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | survey; reports UL as the most used detection class (p.25) | label-free | n/a |
| Live / streaming | calls online detection a future direction (p.31) | incremental windows | n/a |
| Telemetry used | logs, traces, metrics | traces (+ metrics, SSH) | n/a |
| Propagation modelling | surveys graph-based RCI | edge probabilities | n/a |
| Forecasts future failures | no | claimed | n/a |
| Explanation | trust dimensions (explainability) | templates | n/a |
| Evaluation rigor | PRISMA search but flawed cross-study comparison | synthetic only | n/a |
| Open / reproducible | replication package cited | yes | n/a |

- **What they have that we do not:** a large systematic catalogue and tables of testbeds and datasets.
- **What we have that they do not:** implementation and tests.
- **Could a reviewer say "this already exists"?** No.
- **Position:** cite for the testbed and dataset catalogues and for the observation that unsupervised detection is the dominant class; do not cite its averaged performance numbers.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- It reports that unsupervised learning is the most-used detection class and that graph-based methods dominate RCI (pp.23-26), consistent with the label-free graph direction, which also means the space is crowded.
- It mentions that propagation can cause cascading failures and that "forecasting the impact of recovery efforts is challenging" (p.19), citing [188], but offers no forecasting section; cascade forecasting is not covered, probably because of the keyword choice, not because it is absent in the literature.
- It reaffirms that benchmark comparability is poor (p.28).

## 10. Citation-ready facts (each with page)
- A PRISMA review reports 143 included studies in its selection section (p.9) while its abstract says 117 (p.1).
- Reported distribution: 86% of included studies published 2020 to 2024; 70% from Chinese institutions (p.10).
- Train Ticket is the most-used open testbed, followed by Sock Shop and Hipster-Shop (Table 8, p.21, text p.22).
- The AIOps Challenge 2020 and 2021 datasets are the most cited public datasets (9 publications) (Table 9, p.22).
- The authors acknowledge that performance comparisons across the reviewed studies are difficult because of different datasets and missing metrics (p.28).

## 11. Open questions / things to verify
- The replication package [54].
- Which count (117 or 143) the journal version intends.
- Whether the GAIA dataset is public (Table 9 says proprietary; CHASE cites a public repository).
- Figs 1-11.
