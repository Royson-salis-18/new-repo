# Batch 06: 2026-10-07

Papers: 1) realtimeobse (Faseeha et al., IEEE Access 2025, an observability survey), 2) costsensitiv (Liu et al., Cost-Sensitive Mamba, 2024), 3) sheriffadepoju2023cascading (Adepoju, MaaS cascading failures, 2023). All read in full: yes, with exceptions: figures not inspected in any; Faseeha Tables 1-4 and Figs 1-7 did not extract; Liu Figs 1-4 not inspected; Adepoju Fig 1 not inspected.
Scopus: Faseeha = IEEE Access, venue indexed (CiteScore 2025 9.3, 91st percentile); Liu = ISSN 2998-8780 not found; Adepoju = ISSN 2456-6667 not found. SJR quartiles unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side
| | Faseeha et al. | Liu et al. (Mamba) | Adepoju (MaaS) | Ours |
|---|---|---|---|---|
| Type | peer-reviewed survey (observability) | supervised detection method paper | conceptual essay | RCA + untested risk |
| Task | tool and framework taxonomy | window-level anomaly classification | taxonomy of ML-dependency cascades | RCA + cascade risk |
| Labels needed | n/a | yes | n/a | no |
| Telemetry | logs, metrics, traces, eBPF | metrics (RS-Anomic) | none | traces (+ metrics, SSH) |
| Propagation / graph | n/a | none | taxonomy only | edge probabilities |
| Forecasting | mentions SuanMing (100-200 s ahead) and AAD | no | calls for it | claimed, untested |
| Data (open?) | n/a | RS-Anomic repo exists (no license), code not linked | none | open |
| Baselines | none (copied numbers) | 7 cited methods, unverifiable | none | random, earliest, anomaly-only, own PageRank |
| Headline result | RCA 34.2% and performance analysis 30.1% of framework purposes | F1 0.91, AUROC 0.98 (Table 2) | none | none on real faults |
| Evidence quality (1-5) | 2 | 1 | 1 | 1 |
| Scopus status | venue indexed | not found | not found | n/a |

## 2. What each means for our claims
- **Faseeha et al.:** useful background on observability tooling; its Sec. V.A.27 contains speculative descriptions of papers it did not read, and its cross-paper numbers cannot be compared. Its most useful by-product is a pointer to **SuanMing** (ICPE 2021, verified in Crossref): prior art for predicting microservice performance degradation ahead of time (reported 100 s to 200 s ahead, accuracy 90%, F1 0.7, second-hand). Together with AID, Seer and Sage, it is part of the early-warning related work that we must read and cite.
- **Liu et al.:** a detection paper whose comparison table cannot be trusted; "cost-sensitive" is a 5:1 class weight. One reusable idea: report calibration (ECE, Brier) and alarm rate for any risk output.
- **Adepoju:** conceptual only; no evidence; weak venue. It cannot support or contradict a claim about cascade prediction.

## 3. Does this batch change the problem statement?
- Real? No measured evidence in any of the three.
- Already solved? Early warning has at least one explicit published predictor (SuanMing); the claim "predicting degradation is under-explored" is not supportable.
- Misframed? Our Task B must be stated relative to SuanMing, AID, Seer, Sage: label-free, open, evaluated against structural baselines.

## 4. Baselines and datasets to add because of this batch
- Read SuanMing (Grohmann et al., ICPE 2021) in full; check whether code and data are available; candidate baseline for early warning.
- RS-Anomic (github.com/ms-anomaly/rs-anomic; 100,464 normal and 14,112 anomaly instances, ten anomaly types, metrics only; about 12% anomalous) is a small public metrics dataset with labelled anomaly types; needs the user's permission to download; useful only for detector calibration, not RCA.
- Adopt ECE and Brier score (and alarm rate) in the Task B evaluation, as in Liu et al.'s reporting.

## 5. Claims in our draft that this batch contradicts or weakens
- Any claim that early prediction of degradation is unexplored: SuanMing (via Faseeha) predicts degradation ahead of time.
- Any use of Adepoju as evidence that cascading-failure risk is real or measured.

## 6. Sentences we can safely write (with citation keys)
- "Observability for microservices rests on logs, metrics and traces [realtimeobse]."
- "Prior work has predicted microservice performance degradations before they occur, e.g., SuanMing [Grohmann et al., ICPE 2021]" (after reading the original).
- "Conceptual work argues that ML-dependent services add silent decision-quality failure modes [sheriffadepoju2023cascading]" (label it conceptual).
- Do NOT write: Liu et al.'s comparison numbers; Faseeha's overhead figures as comparable; that Adepoju measured anything.

## 7. Corrections needed to earlier notes or reports
1. `docs/REVIEW_REPORT.md` section 6 states the Faseeha PDF is "actually the observability survey by Faseeha et al. (IEEE Access 2025)": confirmed (IEEE Access 13, pp.72011-72039). Additional: its framework descriptions contain speculation.
2. REVIEW_REPORT Appendix A: "Mamba cost-sensitive" is a metrics-only window classifier with unverifiable baselines on a dataset with about 12% anomalies; not evidence for microservice RCA. The REVIEW already said it is not RCA evidence; the new facts are the dataset statistics and the 5:1 weight.
3. REVIEW_REPORT lists the MaaS piece as weak evidence: confirmed; additionally, the venue (a civil-engineering journal) is not found in the Scopus preview.
4. New item for the forecasting related work not in REVIEW_REPORT section 3.2: SuanMing (ICPE 2021). Verified to exist in Crossref (DOI 10.1145/3427921.3450248); contents not yet read.
