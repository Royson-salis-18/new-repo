# Report: Wang and Qi (2024), A Comprehensive Survey on Root Cause Analysis in (Micro) Services

Key `tingtingwangguilinqi2024comprehensive`. Note: `litdb/papers/tingtingwangguilinqi2024comprehensive.md`. Page numbers are PDF pages.
Coverage: full text read; references (pp.26-31) skimmed; Figs 1-6 not inspected.

## (a) Bibliographic block
Tingting Wang and Guilin Qi (Southeast University). arXiv:2408.00803v1 [cs.SE], 23 July 2024, 31 pages, ACM template ("Manuscript submitted to ACM", DOI placeholder XXXXXXX). No journal reference or DOI in the arXiv record (checked 2026-10-07). Preprint: not peer reviewed, not Scopus-indexed. SJR n/a. Funding: NSFC U21A20488.

## (b) Plain-language summary
A catalogue of RCA techniques sorted by the kind of telemetry they use, with a short LLM section and a list of open challenges. It opens with a table of well-known outages to show why RCA matters.

## (c) Problem and motivation
Faults in microservice systems are destructive, propagate through dependencies and recur (p.3). Evidence offered: a table of 14 public outages (2021 to 2024; p.2), OpenAI status-page incident counts (p.3), and a cited figure that about 74.38% of failures recur (from [49], DejaVu). The evidence is anecdotal or second-hand.

## (d) Method
No survey protocol: no databases, queries or criteria. Tables 3 to 6 list methods with data source, RCA category, technique, graph construction, graph category; Table 7 defines metrics (A@K, MAR, precision, recall, F1, training and localization time). Interpretability and generalizability discussed qualitatively (pp.23-24).

## (e) Datasets, protocol
None. Benchmarks named: TrainTicket, SockShop, OnlineBoutique, SocialNetwork.

## (f) Results
No quantitative results. Descriptive outputs: method tables, metric definitions, outage table, list of challenges and trends (real-time analysis, multimodal unified models, explainable AI, LLM operations; pp.24-26).

## (g) Limitations and stern critique
Not peer reviewed; DOI is a template placeholder and revision dates are "xxx"; no systematic selection; no quantitative comparison; entries in Table 1 are unverified and the UniSuper row's "125 billion dollars" looks like a fund size, not a loss (unverified); the OpenAI incident counts on p.3 sum to 100 but the text says over 112; many method-table rows are unnamed; the taxonomy mixes cloud-incident LLM triage with microservice instance localization; it does not mention DeepHunt, BARO or the Pham et al. benchmark.

## (h) Reproducibility
Not applicable. The arXiv record exists.

## (i) Head-to-head with our work
Not a competitor. It names Sage (graphical VAE with counterfactuals for QoS) and a declarative log-based approach that finds cascading failures, which confirm our need to cite prior propagation work; neither is analyzed in depth.

## (j) Does it change our problem? Could a reviewer say it exists?
No. One consideration: the cited 74.38% recurrence figure suggests historical labelled data is valuable, which argues for label-light methods rather than label-free only; we should state recurrence as an assumption we do not exploit.

## (k) Sentences
Safe: "Surveys organize RCA methods by telemetry type and graph category [tingtingwang2024]." / "LLM-based RCA assistants are reported to be limited by hallucination [tingtingwang2024]." / "A cited study reports about 74% of failures recur in the investigated applications [DejaVu, via tingtingwang2024]." Must NOT write: any Table 1 impact figure; that the survey is peer reviewed; the 74.38% figure as our own or without the DejaVu source; that the survey proves cascade prediction is under-explored.

## (l) Things to verify
DejaVu's own statement of the recurrence rate; Table 1 rows; whether a journal version exists.
