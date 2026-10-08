# Report: Faseeha et al. (2025), Observability in Microservices (IEEE Access)

Key `realtimeobse`. Note: `litdb/papers/realtimeobse.md`. Page numbers are PDF pages.
Coverage: all prose sections read to the conclusion; Tables 1-4 and Figs 1-7 did not extract; references skimmed.

## (a) Bibliographic block
Ummay Faseeha, Hassan Jamil Syed, Fahad Samad, Sehar Zehra, Hamza Ahmed (FAST Karachi, Jinnah University for Women, APU Malaysia). IEEE Access 13, pp.72011-72039, published 17 April 2025 (received 17 March, accepted 11 April 2025). CC BY 4.0. ISSN 2169-3536. DOI as printed 10.1109/ACCESS.2025.3562125 (printed with spaces; not re-checked). Scopus: venue indexed (preview 2026-10-07; CiteScore 2025 = 9.3, 91st percentile; SJR 0.884; quartile unknown, no list supplied). Peer reviewed: yes. Note that the queue file name referred to "real-time observability and failure prediction"; the true title is about observability frameworks.

## (b) Plain-language summary
A catalogue of the tools and research frameworks used to watch microservices (logs, metrics, traces, eBPF), arranged in a taxonomy by purpose, scope, deployment environment and architecture, with remarks on open problems.

## (c) Problem and motivation
Observability across system, service and network levels, in cloud, fog and edge settings (pp.1-4). Generic motivation; no measured evidence.

## (d) Method
Searches in IEEE Xplore, ACM DL and Google Scholar with four phrases; inclusion criteria on containerized microservice observability; exclusion of pre-2019 work except foundations (p.5); taxonomy with seven dimensions (Fig 2); review of 25 frameworks in Section V; comparison tables and counts in Section VI. The number of retrieved or included studies is not stated.

## (e) Datasets and protocol
None.

## (f) Results (copied)
Fig 4 text (p.20): root cause analysis 34.2% and performance analysis 30.1% of framework purposes; tool usage counts (p.23-24): OpenTelemetry in 5 studies, Jaeger and Zipkin in 4 each, BPFTrace in 3, eBPF most mentioned. Reported overhead and timing figures are copied from the surveyed papers (e.g., KUNERVA 4.53% CPU, CDoF 2.69%, eBPFM 1.4% at 10,000 packets per second, DESK 90 ms for 50 pods and 130 ms for 110 pods, pp.22-23). SuanMing is described as predicting microservice performance degradation 100 s to 200 s ahead with accuracy 90% and F1 0.7 (p.12).

## (g) Limitations and stern critique
Non-reproducible selection (no counts); the "other solutions" part of Section V is written speculatively ("likely", "in this excerpt"), indicating descriptions written without reading the sources; "quantitative comparison" of incommensurable numbers from different studies; generic textbook descriptions of some techniques; tool-versus-research mixture; Tables and Figures not recoverable here; not an RCA or forecasting survey; queue label mismatch.

## (h) Reproducibility
Not applicable.

## (i) Head-to-head with our work
Not a competitor. Useful as background for our data-collection design (Jaeger, Prometheus, Loki, eBPF alternatives) and for the cost-of-observation remarks (our SSH sampler added host load; see REVIEW_REPORT T7). It points to SuanMing as forecasting prior art.

## (j) Does it change our problem? Could a reviewer say it exists?
It adds one more item to check in the "early warning" literature (SuanMing, ICPE 2021, verified in Crossref as a paper; not read). A reviewer could cite SuanMing against any "no prior work predicts performance degradation" claim.

## (k) Sentences
Safe: "Observability for microservices rests on logs, metrics and traces collected at system, service and network levels [realtimeobse]." / "Prior work has predicted microservice performance degradations ahead of time, e.g., SuanMing [Grohmann et al. 2021], reported by a survey as 100 to 200 s ahead (verify against the original)." Must NOT write: the survey's overhead figures as comparable; that the survey covers failure prediction; its percentage distributions as field statistics without the caveat about unreported selection counts.

## (l) Things to verify
Read SuanMing, AID, Seer, Sage in full; tables and figures; DOI spelling.
