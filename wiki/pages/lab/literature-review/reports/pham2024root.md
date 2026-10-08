# Report: Pham, Ha, Zhang (2024), RCA for microservices based on causal inference: how far are we?

Key `pham2024root`. Note: `litdb/papers/pham2024root.md`. Page numbers are PDF pages.
Coverage: full text read to the end of the references. Caveats: Table 5 columns scrambled in extraction (values flagged "inferred"); Figs 1-4 not inspected; the GitHub supplementary material not read.

## (a) Bibliographic block
Luan Pham, Huong Ha (RMIT), Hongyu Zhang (Chongqing University). ASE '24 (39th IEEE/ACM International Conference on Automated Software Engineering), Sacramento, 27 Oct to 1 Nov 2024. ACM DOI 10.1145/3691620.3695065, ISBN 979-8-4007-1248-7/24/10, CC BY 4.0. No ISSN. Scopus: unverified (the ASE ISSN 1527-1366 returned nothing in the preview; ACM proceedings have no ISSN). SJR: unknown, no list supplied. Peer reviewed: yes (main track; reviewers acknowledged p.11). Funded by ARC and AWS cloud credits.

## (b) Plain-language summary
The authors ran nearly every causal-inference method used for microservice RCA through one common test, and found that most are no better than picking a service at random on their benchmarks. The ones that do well are surprisingly simple (NSigma and BARO compare metric values before and after the fault) and run in hundredths of a second, but they depend on knowing when the fault began. Results on synthetic data did not predict results on real benchmark systems.

## (c) Problem and motivation
No comprehensive evaluation of causal-inference RCA existed (pp.1-2). Motivation: hours to find root causes without tools, and a claim that one hour of downtime could cost Amazon.com up to 100 million USD (p.1, citing [19, 22] and [28, 57]); both are second-hand (anecdotal). The study's evidence for "problem is real" is its own: most methods fail against a random baseline.

## (d) Method of the study
Nine causal discovery algorithms (PC, PCMCI, FCI, Granger, DirectLiNGAM, ICA-LiNGAM, GES, fGES, NTLR) and scoring by PageRank, random walk, depth-first search or hypothesis testing; 21 RCA methods listed in the note including CausalRCA, CausalAI, RUN, MicroCause, epsilon-Diagnosis, RCD, CIRCA, NSigma, BARO and a Dummy random pick. Defaults from the original papers; BIC-based tuning only for causal discovery; failure time assumed known except BARO; variant with the failure time off by 60 s. NSigma is a z-score of post- vs pre-failure data per metric; BARO is a median/IQR version with Bayesian change-point estimation (BARO is the authors' own earlier method, ref [42]).

## (e) Datasets and protocol
Six synthetic sets (CIRCA, RCD, CausIL generators, 10 and 50 nodes) and Sock Shop (two datasets), Online Boutique, Train Ticket deployed on a four-node AWS Kubernetes cluster with Istio, Prometheus, cAdvisor, 100 to 200 concurrent users; five faults (CPU hog, memory leak, disk IO stress, network delay, packet loss) injected into five services per system (Table 2, p.4: 50, 125, 125, 125 cases). Metrics only. Ten repeats for effectiveness, five for the data-length study (over 400 hours per repeat). Leakage in the usual sense is absent (unsupervised methods); the main protocol assumption is the known failure time and pre-failure window.

## (f) Results (copied, with caveats)
Causal graphs: F1 between 0.1 and 0.54; PC best in 7 of 18 cases, FCI in 9 (p.5); edge direction estimates poor; all degrade on larger graphs. RCA: causal-graph-based methods "mostly perform similarly to Dummy"; CausalRCA, RCD, CIRCA, NSigma and BARO are the best (p.6). Table 6 (p.8) runtime: NSigma and BARO 0.01 s on all eight datasets; RCD 12.44 s on Train Ticket; CausalRCA 1,326.34 s on Train Ticket; CIRCA 3,792.29 s on Train Ticket; MicroCause, RUN and NTLR-based methods did not finish some datasets within 2 hours per case. Data length: RCD Online Boutique Avg@5 from 0.13 to 0.79 as data grows from 60 to 600 points; CausalRCA Sock Shop 1 from 0.62 to 0.93 (p.8). Table 5 (inferred column mapping): Dummy Avg@5 on Train Ticket about 0.07; BARO with exact failure time on Train Ticket 0.90, 0.96, 0.84, 0.77, 0.66 across the five fault types and with a 60-second shift 0.81, 0.99, 0.77, 0.82, 0.72; NSigma with the shift 0.03, 0, 0.03, 0.05, 0.12. No statistical testing.

## (g) Limitations and stern critique
Authors: representativeness of systems and faults (p.11). Mine: (1) the authors created BARO and RCAEval, and BARO ranks among the best, undisclosed as a conflict; (2) faults are injected into only five services per system, so the chance floor is high and a service-frequency prior could be strong; Dummy is uniform over nodes, not that prior; (3) metrics only, so structure-aware methods are not given real call graphs; (4) known failure time for most methods; (5) tiny demo apps with synthetic load; (6) default hyper-parameters for RCA methods versus tuned causal discovery, so effort differs; (7) no significance tests; (8) cost-of-downtime motivation is second-hand.

## (h) Reproducibility
Code github.com/phamquiluan/RCAEval exists (MIT, last pushed 2026-09-29, 237 stars; checked 2026-10-07). Data Zenodo 13305663 (CC-BY-4.0): files include online-boutique.zip (about 31.0 MB), sock-shop-1.zip (3.5 MB), sock-shop-2.zip (79.1 MB), synthetic and rca_* archives. The paper also cites Zenodo DOI 10.5281/zenodo.13294049 for code. Nothing downloaded or run.

## (i) Head-to-head with our work
Same task family (label-free, service-level localization) but on metrics only, offline. Pham et al. are far stronger on evaluation: 21 methods, real benchmark systems, open data. Their central message supports our own synthetic finding that simple, graph-free scoring is hard to beat, and it makes BARO and NSigma the mandatory baselines. They say nothing about cascade forecasting, live telemetry or traces.

## (j) Does it change our problem? Could a reviewer say it exists?
It does not change the problem; it raises the bar. A reviewer will cite it against any synthetic-only result and against any claim that graph-based RCA methods are strong. They will expect a Dummy baseline and robustness to the failure time.

## (k) Sentences
Safe: "Pham et al. evaluated nine causal discovery and twenty-one RCA methods and found that no method excels in all situations [pham2024root]." / "Several causal-graph RCA methods performed close to a random baseline in their benchmark, while NSigma and BARO were accurate and fastest [pham2024root]." / "Synthetic-data results did not reliably predict real-system results [pham2024root]." Must NOT write: that Pham et al. proved causal discovery fails in general or that they evaluated event-based methods (they did not); that they validated our approach; any cost-of-downtime figure as established fact; that graph-free methods are always better.

## (l) Things to verify
Check Table 5 in the PDF image; read the supplementary material; whether RCAEval datasets contain traces and logs for the RE2 versions (the later datasets, not in this paper); the Amazon cost claim at its source.
