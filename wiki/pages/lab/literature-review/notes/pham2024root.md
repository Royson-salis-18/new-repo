---
key: pham2024root
title: "Root Cause Analysis for Microservices based on Causal Inference: How Far Are We?"
authors: "Pham, Luan; Ha, Huong; Zhang, Hongyu"
year: 2024
venue: "39th IEEE/ACM International Conference on Automated Software Engineering (ASE '24), Sacramento, CA"
publisher: "ACM (IEEE/ACM)"
doc_type: proceedings-article
doi: "10.1145/3691620.3695065"
issn: "none in Crossref (ACM ISBN 979-8-4007-1248-7/24/10)"
scopus_indexing: "unverified (no ISSN; the IEEE ASE series ISSN 1527-1366 returned 0 results in the Scopus preview; see litdb/reference/scopus_checks.md)"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (ASE main technical track; reviewers thanked p.11)"
cited_by_crossref: ""
n_references: "about 67"
license: "CC BY 4.0"
batch: "2"
read_status: reviewed                  # Table 5 columns garbled in extraction (mapping inferred, flagged below); Figs 1-4 not inspected; supplementary material (GitHub) not read
pages: 13
text_chars: 86740
metadata_source: crossref
task: "benchmark / evaluation of causal-discovery and RCA methods (service-level localization from metrics)"
supervision: "mixed: causal-discovery methods are unsupervised; compared RCA methods are label-free"
online_or_streaming: "no (offline cases; studies input data length and failure-time misspecification)"
telemetry: "metrics only (Prometheus/Istio/cAdvisor); no logs or traces"
propagation_modeling: "causal discovery (PC, FCI, Granger, LiNGAM, GES, NTLR, PCMCI) + PageRank/random walk; hypothesis-test methods without graph (NSigma, BARO, epsilon-Diagnosis)"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "Sock Shop (two datasets), Online Boutique, Train Ticket on a 4-node AWS Kubernetes cluster; six synthetic datasets"
datasets: "synthetic (CIRCA, RCD, CausIL generators; 10 and 50 nodes) and benchmark systems with 5 fault types injected in 5 services per system (Table 2)"
dataset_open: "yes (Zenodo record 13305663, CC-BY-4.0, verified via API)"
code_open: "yes (github.com/phamquiluan/RCAEval, MIT, verified; Zenodo DOI 10.5281/zenodo.13294049 cited)"
baselines_compared: "21 RCA methods incl. PC/FCI/Granger/LiNGAM/fGES/NTLR + PageRank or random walk, CausalRCA, CausalAI, RUN, MicroCause, epsilon-Diagnosis, RCD, CIRCA, NSigma, BARO, and a random 'Dummy'"
metrics: "AC@k, Avg@5; F1, F1-S, SHD for causal graphs; runtime"
headline_result: "no method best everywhere (abstract p.1); PC/FCI/Granger/LiNGAM/fGES/NTLR-based RCA, CausalAI, RUN, MicroCause mostly near the Dummy random baseline (p.6); CausalRCA, RCD, CIRCA, NSigma, BARO best (p.6); NSigma and BARO fastest, 0.01 s on every dataset (Table 6 p.8)"
evidence_quality: "4"
relevance_to_us: "5"
overlap_with_us: "partial (same task family and baselines to run; no cascade forecasting)"
threat_level_for_novelty: "low (it is the evaluation reference a reviewer will use against us)"
---

# Root Cause Analysis for Microservices based on Causal Inference: How Far Are We?

> Reading notes written from the **full text** (`litdb/texts/pham2024root.txt`). Page numbers are PDF pages (paper pp.706-716 in ACM numbering = PDF pp.1-11; references to p.13).
> Caveats: Table 5 (p.7) extracted with columns scrambled. I copy only rows whose 21 values I could map to the header (4 synthetic + Online Boutique 5 + Sock Shop 1 two + Sock Shop 2 five + Train Ticket five); mapping is inferred and should be checked against the PDF. Figs 1-4 not inspected; the supplementary material on GitHub was not read.

## 1. One-paragraph summary
An empirical study that runs nine causal-discovery methods and twenty-one metric-based RCA methods on six synthetic datasets and four datasets from three benchmark microservice systems, and reports effectiveness, runtime, sensitivity to input length and to a wrong failure time. Main conclusions: no method wins everywhere; most methods that build a full causal graph are barely better than a random-choice baseline; simple methods that compare pre- and post-failure metric distributions (NSigma, BARO) are accurate and fastest but sensitive to the specified failure time (NSigma much more than BARO); and performance on synthetic data does not predict performance on real systems.

## 2. Problem and motivation
- Problem: no comprehensive evaluation of causal-inference RCA exists (pp.1-2).
- Motivation evidence: hours to diagnose without tools (cites [28, 57]) and "up to 100 million USD per hour of downtime" for Amazon.com (cites [19, 22]) (p.1). These are cited second-hand claims (anecdotal / cited).
- Real? The paper's own evidence is that existing RCA methods underperform in realistic settings, which supports the need for better RCA, not the cost claims.

## 3. Method (of the study)
- Causal graph methods: PC, PCMCI, FCI, Granger, DirectLiNGAM, ICA-LiNGAM, GES, fGES, NTLR; scoring by PageRank or random walk, depth-first search, or hypothesis testing (pp.3-4).
- RCA methods (21): the PC/FCI/Granger/ICA-LiNGAM/fGES/NTLR + PageRank or random walk variants, CausalRCA, CausalAI, RUN, MicroCause, epsilon-Diagnosis, RCD, CIRCA, NSigma, BARO, plus Dummy (random node) (p.6).
- NSigma: z-score of post-failure vs pre-failure data; BARO: median and IQR based variant with change-point estimation of failure time; neither builds a causal graph (p.3).
- Settings: default hyper-parameters from the original papers; hyper-parameter tuning by BIC only for causal discovery (Sec. 3.3, 4.1); CIRCA uses PC to build its graph because no call graph is available (p.5). Correctness checked by reproducing published results (p.5).
- Inputs: metrics only; failure time t_F assumed known for RCD, CIRCA, NSigma, epsilon-Diagnosis; BARO estimates it. Study variants with t_F misspecified by 60 s (p.6).

## 4. Data and setup
- Synthetic: CIRCA generator (VAR time series, noise change fault), RCD generator (discrete series, conditional probability change), CausIL generator (no fault injection) at 10 and 50 nodes; 200 faulty cases for CIRCA10/50 and RCD10/50, 10 for CausIL (Table 1, p.4).
- Benchmark systems (Table 2, p.4): Sock Shop 1 (38 metrics, 13 services, 5 target services, 2 fault types, 50 cases), Sock Shop 2 (46 metrics, 15 services, 5 faults, 125 cases), Online Boutique (49 metrics, 12 services, 5 faults, 125 cases), Train Ticket (212 metrics, 64 services, 5 faults, 125 cases).
- Faults (injected): CPU hog, memory leak, disk IO stress, network delay, packet loss, into **five services** per system (p.4); 100 to 200 concurrent users; four-node Kubernetes on AWS, Istio + Prometheus + cAdvisor.
- Repeats: 10 (causal discovery and RCA effectiveness), 5 for the data-length study because it took over 400 hours per repeat (p.8).
- Hardware: 8 CPUs, 16 GB RAM (p.5).
- Leakage: methods are unsupervised; main issue is assumed knowledge of failure time and pre-failure window.

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Causal discovery F1 range | all methods F1 between 0.1 and 0.54 | n/a | PC wins 7 of 18 cases, FCI 9 | p.5, Table 3 p.6 |
| RCA vs random | PC/FCI/Granger/LiNGAM/fGES/NTLR-based, CausalAI, RUN, MicroCause mostly similar to Dummy | n/a | Dummy | p.6 |
| Best RCA methods | CausalRCA, RCD, CIRCA, NSigma, BARO | n/a | n/a | p.6, p.7 |
| Runtime | NSigma and BARO 0.01 s on all eight datasets; RCD 12.44 s and CIRCA 3,792.29 s on Train Ticket; CausalRCA 1,326.34 s TT | n/a | n/a | Table 6, p.8 |
| Scale | most methods handle 38-49 metrics within seconds; Train Ticket (212 metrics) takes minutes to about an hour | n/a | n/a | p.8 |
| Data length | RCD Online Boutique Avg@5 0.13 to 0.79 from 60 to 600 points; CausalRCA Sock Shop 1 0.62 to 0.93 from 120 to 600 | n/a | n/a | p.8 |

- Table 5 (p.7), Avg@5, values I could map (inferred columns; check PDF): Dummy RCD10 0.3, RCD50 0.06, CIRCA10 0.3, CIRCA50 0.06; Online Boutique CPU/MEM/DISK/DELAY/LOSS 0.25/0.24/0.26/0.26/0.25; Train Ticket 0.07/0.08/0.06/0.07/0.07. BARO [t_delta = 0]: RCD10 0.22, RCD50 0.05, CIRCA10 0.92, CIRCA50 0.87; Online Boutique 0.97/1/0.91/0.98/0.67; Train Ticket 0.90/0.96/0.84/0.77/0.66. NSigma [t_delta = 0]: RCD10 0.21, RCD50 0.06; Train Ticket 0.81/0.96/0.85/0.61/0.7. With the failure time shifted by 60 s: BARO Train Ticket 0.81/0.99/0.77/0.82/0.72; NSigma Train Ticket 0.03/0/0.03/0.05/0.12.
- Statistics: average of 10 repeats; no tests or CIs.
- Efficiency: Table 6 p.8; PC with KCI independence test takes over 1 hour per case for 10-node graphs (p.7); PC and FCI ran out of memory on RCD50, and GES, DirectLiNGAM, NTLR were excluded for exceeding 1 hour per case (Table 4 note, p.6); MicroCause, RUN and NTLR-based RCA exceeded 2 hours per case on some datasets (Table 5 note, p.7).

## 6. Limitations
- Stated (Sec. 5.3, p.11): different applications and faults may behave differently; fault set limited to five common faults.
- **My critique:**
  1. Conflict of interest: the first author developed BARO and the RCAEval framework used here, and BARO ends up among the best methods; the paper does not discuss this. Code used for competitors is third-party, with reproduction checks, but tuning effort is not equal (defaults only for RCA methods, p.11).
  2. Faults injected into only five services per system, so a prior on those services can score well (a point later made by other papers, see REVIEW_REPORT 3.3); the paper includes the random Dummy, which picks uniformly over nodes, not a service-frequency prior.
  3. Metrics only: no traces or logs, so propagation-aware methods using call graphs get no real graph (CIRCA is given PC-estimated structure).
  4. Failure time is assumed known for most methods; real pipelines need a detector, and the paper itself shows sensitivity.
  5. Three benchmark systems are small demo apps with synthetic load; injected faults are not production incidents.
  6. No statistical tests; ten repeats average out stochastic methods, not case variation.
  7. Dummy shows the floor but Avg@5 on 12 to 64 services has a high chance floor, especially for Online Boutique and Sock Shop.
- Not discussed: effect of baseline-window contamination, multiple simultaneous faults.

## 7. Reproducibility
- Code: https://github.com/phamquiluan/RCAEval, HTTP 200, MIT license, last push 2026-09-29, 237 stars (checked 2026-10-07).
- Data: https://zenodo.org/records/13305663, CC-BY-4.0, files include online-boutique.zip (31.0 MB), sock-shop-1.zip (3.5 MB), sock-shop-2.zip (79.1 MB), syn_circa.zip, syn_rcd.zip, syn_causil.zip, rca_circa.zip, rca_rcd.zip (sizes from Zenodo API). Not downloaded.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | none for compared methods | label-free | Comparable |
| Live / streaming | offline, studies input length and failure-time error | incremental windows | Theirs measures timing sensitivity; ours does not |
| Telemetry used | metrics only | traces (+ metrics) | Different |
| Propagation modelling | causal discovery, found weak | edge probabilities, mostly prior | Their finding: graph learning gives little over simple tests |
| Forecasts future failures | no | risk score, untested | Neither |
| Explanation | none | template | Ours slightly |
| Evaluation rigor | 21 methods, 4 systems, real injected faults, open data and code | synthetic only | Theirs, clearly |
| Open / reproducible | yes | yes | Comparable |

- **What they have that we do not:** a broad benchmark, ready datasets and a reference implementation of 21 methods.
- **What we have that they do not:** trace-based live adapters; a forecasting idea.
- **Could a reviewer say "this already exists"?** Not for our contribution, but it supplies the strongest evidence against our synthetic results and shows that simple comparison methods (NSigma, BARO) are the bar to beat.
- **Position:** "Following Pham et al., we compare against the lightweight baselines NSigma and BARO and a random Dummy baseline."
- **Must we run it as a baseline?** Yes: RCAEval contains BARO, NSigma, CIRCA, RCD, CausalRCA and the datasets; MIT licensed.

## 9. Does this paper change what problem we should solve?
- It strengthens the point that simple, label-free, graph-free methods are the real competition; any added propagation machinery must beat BARO/NSigma.
- It does not address cascade forecasting at all.
- Evidence the problem is real: hours-to-diagnose and downtime cost statements are second-hand.

## 10. Citation-ready facts (each with page)
- Evaluates 9 causal-discovery and 21 RCA methods on 6 synthetic and 4 benchmark datasets; no method stands out in all situations (abstract, p.1).
- Many causal-graph RCA methods perform close to a random Dummy baseline (p.6).
- NSigma and BARO are consistently the fastest RCA methods (p.7, Table 6 p.8); RCD, CIRCA, NSigma are sensitive to failure time; BARO is more robust (p.6).
- Synthetic-data performance may not reflect real systems (abstract p.1; p.6).
- Data and code are open (p.11).

## 11. Open questions / things to verify
- Table 5 column mapping (check the PDF image); numbers above are labelled inferred.
- Supplementary Table S1 (not read).
- The Amazon.com 100 million USD per hour claim comes from refs [19, 22] and is not verified here.
