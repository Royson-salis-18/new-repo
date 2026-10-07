# Report: Fu et al. (2025), Intelligent Root Cause Localization in MicroService Systems: A Survey

Key `fu2025intelligent`. Note: `litdb/papers/fu2025intelligent.md`. Page numbers are PDF pages.
Coverage: full text read, including the references (scanned for relevant terms, entries not individually read). Figures 1-9 not inspected.

## (a) Bibliographic block
Nan Fu, Guang Cheng, Yue Teng, Guangye Dai (Southeast University), Shui Yu (UTS), Zihan Chen (Southeast University). *ACM Computing Surveys* 57(12), Article 325, July 2025, 37 pages. DOI 10.1145/3736755. ISSN 0360-0300 / 1557-7341. Received 29 Apr 2024, revised 10 Apr 2025, accepted 29 Apr 2025. 147 references. Crossref cited-by: 10. Scopus: venue indexed (manual preview check 2026-10-07; CiteScore 2025 = 65.2, 99th percentile, rank 1 of 241 in General Computer Science; SJR 2025 shown as 5.985; quartile unknown, no list supplied). Peer reviewed: yes. Strong venue; the survey itself has methodological gaps (below).

## (b) Plain-language summary
A map of how root causes are found in microservice systems: how telemetry is collected, how benchmarks inject faults, how methods work (with or without building a dependency or causal graph), where AI helps, and what is missing. It ends with open problems and an unevaluated proposal for an end-to-end system for enterprise networks.

## (c) Problem and motivation
Faults are inevitable and costly, and previous surveys lacked data collection and AI-driven analysis (pp.2-4). No measured evidence is supplied; motivation is cited and asserted (assumed or anecdotal).

## (d) Method
Taxonomy: data collection (observability tools in Table 3, benchmark systems in Table 4, fault simulation in Table 5, collection techniques scored in Table 6, public datasets in Table 7) -> direct analysis (single metrics, trace records, multi-source) -> indirect analysis (causal graphs by PC, fault propagation graphs, inference graphs; dependency and relationship graphs; inference by random walk, BFS, DFS, AI) -> evaluation metrics (AC@k, Avg@k, PR@k, MAP, RankScore; accuracy, precision, recall, FPR, F1, ROC). Attribute comparison of 12 methods (Table 9) and of 17 studies by check marks (Table 10). No search protocol or inclusion and exclusion criteria are stated.

## (e) Datasets, protocol, leakage
No experiments. Benchmarks described: Train Ticket (41 microservices, 86 request types), Sock Shop (13, 10), Hotel Reservation (15), Hipster-Shop (10). Public datasets in Table 7 (Psqueeze, DejaVu A/B/C, RCD, TraceRCA, MEPFL). No leakage question applies.

## (f) Results (copied)
No numbers beyond classification outputs: 12 methods in Table 9 (7 use AI), 17 studies in Table 10 (check marks for closed-world, open-world, effectiveness, time and resource overhead), seven localization levels (Fig 8). Qualitative statements: heuristic unsupervised methods are lighter but less accurate than supervised ones (p.23); supervised methods need engineer-prepared labels (pp.22-23); benchmark fault types differ from production faults (pp.13, 27); most fault injection targets microservice level only (p.10).

## (g) Limitations and stern critique
Authors: future directions only. Mine: no reproducible selection protocol; "performance evaluation" is check marks; no mention of DeepHunt, BARO, Eadro, DiagFusion or Nezha; the reference "Pham et al. [102]" is a 2016 paper, so the 2024 ASE benchmark evidence is absent; the claim that AI-driven methods are "more intelligent" is not backed by controlled comparison; Table 9's "Multi-Source" means multiple root causes, an unusual definition; the proposed framework is not evaluated.

## (h) Reproducibility
Not applicable. The DOI resolves in Crossref. Nothing to run.

## (i) Head-to-head with our work
Not a competitor. It is a taxonomy and a source for statements about labels, benchmark mismatch and tooling. It supports our label-free motivation and our caution about injected faults, and it lists tools we use (Jaeger, Prometheus).

## (j) Does it change our problem? Could a reviewer say it exists?
No change to our problem. It gives no evidence on cascade forecasting; the topic is outside its taxonomy, which shows RCA surveys treat it separately, not that it is unexplored (see REVIEW_REPORT 3.2). We should cite it for taxonomy and for the label-cost remark.

## (k) Sentences
Safe: "Surveys group microservice RCA into direct methods that analyze data without a graph and indirect methods that build a causal or topological graph and infer over it [fu2025intelligent]." / "Supervised RCA methods depend on engineer-prepared labels, which are costly to obtain [fu2025intelligent]." / "Public benchmark fault types such as CPU or memory exhaustion and packet loss or delay differ from the more varied faults in production [fu2025intelligent]." Must NOT write: that the survey evaluated methods quantitatively; that it shows AI methods beat heuristics; that it covers recent label-free methods; that it found cascade forecasting unexplored.

## (l) Things to verify
Seer's classification in the survey; whether later versions add recent methods; Figs 1-9.
