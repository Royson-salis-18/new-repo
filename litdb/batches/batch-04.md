# Batch 04: 2026-10-07

Papers: 1) yuqingwang...cross (Few-shot cross-system trace classification; arXiv v2 read, published as PACMSE 2025), 2) graphneurala (Graph Neural AI with temporal dynamics; arXiv 2511.03285), 3) erakovic2025hybrid (Hybrid RCA, CLOSER 2025). All read in full: yes, with exceptions: figures not inspected in all three; Erakovic Tables 1 and 2 did not extract; the published version of paper 1 not read.
Scopus: Erakovic = CLOSER proceedings series indexed (ISSN 2184-5042 match; 2025 volume coverage unverified); Wang et al. = preprint not indexed, published venue PACMSE (ISSN 2994-970X) not found in the preview; Graph Neural AI = arXiv preprint, not indexed. SJR unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side
| | Wang et al. (few-shot) | Graph Neural AI | Erakovic and Pahl | Ours |
|---|---|---|---|---|
| Task | classify abnormal traces by fault category | anomaly detection + "root cause tracing" (not evaluated) | rule-based RCA + fault-type from trace latency | RCA + untested risk |
| Labels needed | yes (base categories and K shots) | unclear | no (rules, thresholds) | no |
| Telemetry | spans + logs | traces | traces only | traces (+ optional metrics, SSH) |
| Propagation / graph | none | GCN + GRU, path score | architecture mining, call graph | edge probabilities |
| Forecasts failures | no | no | no | claimed, untested |
| Data (open?) | DeepTraLog + Nezha repos (verified listing); code pending | DeathStarBench trace data, no link | TraceRCA ISP dataset (cited, unverified) | open |
| Baselines | internal ablations | 1DCNN, LSTM, Transformer, GAT | none | random, earliest, anomaly-only, own PageRank |
| Headline result | 93.26% / 85.2% (10-shot, within-system), 92.19% / 84.77% cross | AUC 0.951, F1 0.896 | two worked examples, no metrics | none on real faults |
| Evidence quality (1-5) | 2 | 1 | 1 | 1 |
| Scopus status | published venue not found; preprint not indexed | not indexed | series indexed, volume unverified | n/a |

## 2. What each means for our claims
- **Wang et al.:** a different task (fault-type classification with labels); its cross-system claim still needs target-system normal data and labelled shots; best-of-five scoring inflates its numbers. It does resolve part of an earlier uncertainty: the DeepTraLog and Nezha GitHub repositories do contain data folders.
- **Graph Neural AI:** no usable evidence; no description of anomalies or labels. Useful only as an example of the unreliability of GNN preprints in this area.
- **Erakovic and Pahl:** the most similar in constraints (trace-only, label-free) but gives two visual examples. It supports the idea that architecture knowledge helps interpret propagation, with no numbers. Its ISP dataset (TraceRCA repository) is a candidate real-fault test set for us.

## 3. Does this batch change the problem statement?
- Real? None of the three measures the problem. Each asserts that RCA is hard and cascades occur.
- Already solved? No; these papers show low-rigor evaluation in the area, which supports our plan to evaluate with common benchmarks and baselines.
- Misframed? No change. One consideration: cross-system generalization is posed by Wang et al. as a need; our label-free claim of "architecture independence" must be tested on at least two systems.

## 4. Baselines and datasets to add because of this batch
- Datasets (all need the user's permission before download): Nezha repo `rca_data` (OnlineBoutique 2022-08-22/23, TrainTicket 2023-01-29/30; includes traces, logs, metrics per the repo README and the Wang et al. use of it), DeepTraLog repo (TraceLogData, GraphData), TraceRCA ISP dataset (via NetManAIOps/TraceRCA).
- No new baselines from these papers.

## 5. Claims in our draft that this batch contradicts or weakens
- None directly. These papers do not address cascade forecasting or label-free forecasting.
- Warning: do not cite the Graph Neural AI or Erakovic and Pahl numbers as evidence for GNN or rule-based methods' accuracy.

## 6. Sentences we can safely write (with citation keys)
- "Few-shot meta-learning has been applied to classify abnormal traces by fault category on TrainTicket and OnlineBoutique, still requiring labelled examples per task [yuqingwang... / PACMSE 2025]."
- "Rule-based RCA that uses only trace latency and architecture mining has been illustrated on injected faults from a public ISP trace dataset [erakovic2025hybrid]."
- Do NOT write: any accuracy number from these papers as established evidence of method quality; that Graph Neural AI localizes root causes; that the cross-system method is label-free.

## 7. Corrections needed to earlier notes or reports
1. `docs/REVIEW_REPORT.md` Appendix B says the hosting and contents of the DeepTraLog and Nezha datasets were not checked. Partly resolved: github.com/IntelligentDDS/Nezha (MIT) lists `rca_data` folders for 2022-08-22, 2022-08-23 (OnlineBoutique) and 2023-01-29, 2023-01-30 (TrainTicket); github.com/FudanSELab/DeepTraLog lists TraceLogData and GraphData. File sizes, formats and licenses (DeepTraLog has no license file) not yet checked.
2. The Few-shot paper was queued as an arXiv preprint without DOI; it has been published as "Cross-System Categorization of Abnormal Traces in Microservice-Based Systems via Meta-Learning", PACMSE 2025, DOI 10.1145/3715742. The note says so; the published version is still to be read.
3. The queue entry `graphneurala` had no metadata; identified as arXiv:2511.03285 (5 Nov 2025).
4. REVIEW_REPORT said these papers were skimmed; now read: the few-shot paper is supervised classification; Graph Neural AI has no anomaly or label description; Hybrid RCA has no quantitative evaluation. Any earlier note characterizing them more favourably should be revised.
