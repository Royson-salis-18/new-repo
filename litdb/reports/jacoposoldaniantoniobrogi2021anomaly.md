# Report: Soldani and Brogi (2022), survey of anomaly detection and RCA

Key `jacoposoldani...2021anomaly`. Note: `litdb/papers/` same key. Coverage: arXiv v1 (36 pages); Sections 1, 2, 3.4, 4.4, 5, 6 read in detail; per-technique text skimmed; Tables 1-2 did not extract.

## (a) Bibliographic block
Jacopo Soldani, Antonio Brogi (University of Pisa). ACM Computing Surveys 55(3), article 59 (2022), DOI 10.1145/3501297 (Crossref: ISSN 0360-0300, 245 citations); text read is arXiv 2105.12378v1. Venue ISSN is Scopus-indexed (earlier check); this article not checked. SJR unknown.

## (b) Plain-language summary
A structured overview of how to detect abnormal behaviour in multi-service applications and find its likely cause, grouped by the data used and the method.

## (c) Problem and motivation
Failures are hard to detect and explain in applications of hundreds of services; solutions are scattered (pp.1-2).

## (d) Method
Taxonomy: log-, trace- and monitoring-based detection; log-, trace- and monitoring-based RCA with direct, topology graph-based and causality graph-based analysis; discussion of setup cost, granularity, accuracy, explainability (pp.3-28).

## (e) Datasets, protocol
None; no quantitative comparison (pp.28, 30).

## (f) Results
Qualitative: RCA techniques usually return a ranked set of candidate causes; false positives/negatives are inherent; correlation-driven methods are prone to spurious correlation; topology-only graphs miss co-hosted services (p.27); explainability by design, continual adaptation, and countermeasure recommendation are open (pp.28, 30-31).

## (g) Limitations and stern critique
No search protocol in the sections read; 2021 cut-off; no quantitative comparison; published version may differ from arXiv v1.

## (h) Reproducibility
Not applicable.

## (i) Head-to-head with our work
Context only. Gives citable statements for our limitations (co-location, explanation, comparison problems).

## (j) Does it change our problem? Could a reviewer say it exists?
It states preemptive prediction of degradations as a future direction (as of 2021); Seer and SuanMing already address part of it; do not cite this survey as proof that forecasting is absent.

## (k) Sentences
Safe: "Surveys note that graphs modelling only service interactions can miss anomalies caused by co-hosted services [Soldani and Brogi, p.27]." Must NOT write: that the survey evaluates accuracy of techniques.

## (l) Things to verify
arXiv v1 vs CSUR text; Tables 1-2.
