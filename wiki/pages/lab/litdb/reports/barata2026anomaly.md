# Report: Barata et al. (2026), Anomaly detection and root-cause identification in microservices: a survey

Key `barata2026anomaly`. Note: `litdb/papers/barata2026anomaly.md`. Page numbers are PDF pages (42 pages).
Coverage: full body text read to the end (conclusion and declarations). The reference list (about 250 entries) was searched for key terms, not read in full. Figs 1-11 not inspected.

## (a) Bibliographic block
Luís M. Barata, Sérgio Sequeira, Eurico Lopes, Pedro R. M. Inácio, Mário M. Freire (Universidade da Beira Interior, IPCB, Portugal). *Cluster Computing* 29:309 (2026), Springer Nature, open access CC BY 4.0. DOI 10.1007/s10586-026-06095-9. ISSN 1386-7857 / 1573-7543. Received 14 June 2025, revised 2 March 2026, accepted 4 March 2026, published online 3 June 2026. Scopus: venue indexed (preview check 2026-10-07; CiteScore 2025 = 8.4, 82nd percentile, rank 98 of 568 in Computer Networks and Communications; SJR 2025 shown as 1.014; quartile unknown, no list supplied). Peer reviewed: yes.

## (b) Plain-language summary
A systematic literature review of how researchers detect anomalies and find root causes in microservices, with tables of methods, testbeds and datasets. Its quantitative conclusions about which kind of method works best come from averaging numbers that different papers reported on different data, which cannot support such conclusions.

## (c) Problem and motivation
Microservices create dynamic, interdependent systems where detection and diagnosis are hard (pp.1-3). Evidence offered is anecdotal: Alibaba manages over 30,000 services; Amazon "lost millions" in 2013 and 2018 outages; Walmart's monolith failed at peaks (p.2; second-hand citations). The paper says minor faults can propagate rapidly and cause cascading failures (p.2), unquantified.

## (d) Method (of the review)
PRISMA with seven libraries, search window December 2021 to May 2025, seven keyword combinations (Table 4, p.8), counts: 10,485 identified, 9,648 removed, 837 screened, 306 after abstract screening, 171 read, 143 included (p.9). Studies are tagged by data collection (log, trace, monitoring), detection type, root-cause method and anomaly type; Sec. 4.7 averages reported metrics above 80% per category; Sec. 6 proposes trust dimensions and indicators (Table 10).

## (e) Datasets and protocol
No experiments. Table 8 lists testbeds (Train Ticket most used, then Sock Shop with 19 citing works, Hipster-Shop, DeathStar and others, plus proprietary platforms such as Alibaba EagleEye and IBM Bluemix). Table 9 lists datasets (AIOps Challenge 2020 and 2021 cited by 9 works; GAIA, TraceRCA, HDFS, BGL, SMD, MicroCU and others; several marked proprietary).

## (f) Results (copied)
Distribution: 86% of included studies published 2020 to 2024 (p.10); 70% from Chinese institutions (p.10); machine learning used in 70% of detection methods (p.25). Averages of self-reported metrics (p.23): ML root-cause methods precision 94.9%, recall 98.0%, F1 99.0%, accuracy 94.3%; graph-based precision 92.7%, recall 89.7%; statistical precision 85.0%, recall 88.0%, F1 85.8%, accuracy 99.0%. The text itself says comparison is difficult (p.28) and should be interpreted with caution (p.31).

## (g) Limitations and stern critique
Authors: English only, to May 2025, selection bias possible, heterogeneity limits comparison (p.31). Mine: the abstract and Sec. 2 state 117 studies (1,700 results) but Sec. 4.1.4 reports 143 studies (10,485 records); the search terms contain no "root cause", "cascad*" or "propagation", so RCA-only and propagation work is under-sampled; Sec. 4.7 averages above-80% values across heterogeneous studies and ranks method categories, which is invalid; the "top five" lists rank by self-reported numbers from different data; Pham et al. 2024 is tabulated as a method row; DeepHunt, Eadro, Nezha and BARO are absent; Table 10's seven trust indices are named but not defined by equations or applied; footnotes in Tables 5 and 6 are scrambled; motivation is anecdotal.

## (h) Reproducibility
A replication package is referenced as [54] (p.9); I did not check it. No data were generated (p.32).

## (i) Head-to-head with our work
Not a competitor. It supplies lists of testbeds and datasets (useful for choosing evaluation systems), confirms that unsupervised detection and graph-based RCI are the dominant classes, and highlights the lack of comparability. It offers no support for cascade forecasting, probably because of its search terms.

## (j) Does it change our problem? Could a reviewer say it exists?
No. It reinforces that our evaluation must be on common benchmarks with shared baselines, since the survey admits cross-paper comparison is unreliable.

## (k) Sentences
Safe: "A recent PRISMA-style survey reports that unsupervised learning is the most common detection approach and graph-based methods dominate root-cause identification in microservice studies [barata2026anomaly]." / "Train Ticket and Sock Shop are the most used open testbeds, and the AIOps Challenge 2020 and 2021 datasets the most cited public datasets in that survey [barata2026anomaly]." / "The survey's authors note that performance comparisons across studies are hard because of differing datasets and metrics [barata2026anomaly]." Must NOT write: any of its averaged accuracy figures; its "best method" rankings; that it covers cascade forecasting; the count of included studies without noting the 117 versus 143 discrepancy.

## (l) Things to verify
Replication package [54]; which count is correct; GAIA availability; Figs 1-11.
