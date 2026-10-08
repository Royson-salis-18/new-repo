# Batch 12: 2026-10-08

Papers: 1) AIOps benchmark datasets (Li et al., arXiv 2022), 2) Soldani and Brogi survey (CSUR 2022; arXiv v1 read), 3) Buldyrev et al. (Nature 2010; arXiv v1 read).
All read: the dataset paper to the conclusion; the survey in detail for Sections 1-2, 3.4, 4.4, 5-6 (technique descriptions and Tables 1-2 not verified); Buldyrev to the ER solution. Figures not inspected.
Scopus: CSUR ISSN 0360-0300 is indexed (earlier check); Nature ISSN 0028-0836 and the datasets paper (arXiv) not indexed/checked. SJR quartiles unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side
| | AIOps datasets | Soldani and Brogi | Buldyrev et al. | Ours |
|---|---|---|---|---|
| Type | dataset description | survey | theory | RCA + untested risk |
| Telemetry | KPIs, traces, metrics | survey of logs/traces/KPIs | none | traces (+ metrics) |
| Propagation | none | taxonomy | percolation, one-to-one | edge probabilities |
| Forecasting | no | open direction | threshold analysis | claimed, untested |
| Data (open?) | yes (stated) | n/a | n/a | open |
| Headline | 169 injected failures, 7 types | no quantitative result | critical degree 2.445 | none on real faults |
| Evidence quality | 2 | 4 (qualitative) | analytic | 1 |

## 2. What each means for our claims
- **AIOps datasets:** source of the 2020 challenge data (traces, KPIs, metrics, ground truth) with call and deployment dependencies. Injected faults of seven types on one system (shares Fang et al.'s concerns).
- **Soldani and Brogi:** gives citable limitations: topology-only graphs miss co-hosted services (p.27), explainability and countermeasures are open, comparison across papers is unreliable (pp.28, 30). It lists predicting degradations as a 2021 future direction.
- **Buldyrev et al.:** general theory of structural cascades in coupled networks; not calibrated to microservices.

## 3. Does this batch change the problem statement?
- No. It supplies citations for limitations and one more public dataset (needs permission to download).

## 4. Baselines and datasets to add because of this batch
- 2020 AIOps challenge dataset C (169 injected failures; traces, KPIs, metrics): optional trace-based test set. Not downloaded.

## 5. Claims in our draft that this batch contradicts or weakens
- Any statement that cascade or degradation prediction is absent from the literature (the 2021 survey lists it as open, but Seer and SuanMing exist).
- Any use of Buldyrev et al. as evidence for microservice cascades.

## 6. Sentences we can safely write (with citation keys)
- "Surveys note that graphs modelling only service interactions can miss anomalies caused by co-hosted services [Soldani and Brogi, p.27]."
- "A public dataset with traces, KPIs and metrics for 169 injected failures was released with the 2020 AIOps challenge [Li et al. 2022]."
- "Cascading failures in coupled networks have been analysed by percolation theory [Buldyrev et al.]" (background only).
- Do NOT write: that survey results are quantitative; that Buldyrev's model describes service dependency cascades.

## 7. Corrections needed to earlier notes or reports
1. The literature matrix lists Buldyrev as 2010 and the arXiv key as 2009 (v1 date); both refer to the Nature 2010 paper (Crossref confirmed).
2. Soldani and Brogi is 2022 (CSUR), arXiv 2021; the matrix key `soldani2022` is correct for the journal year.
3. `docs/REVIEW_REPORT.md` should not cite the survey for forecasting absence.

## 8. Proposals (no code changed)
- Add a co-location (same host) edge ablation to our propagation model, citing Soldani and Brogi p.27 and DéjàVu's deployment edges as motivation.
