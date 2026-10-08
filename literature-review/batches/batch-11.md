# Batch 11: 2026-10-08

Papers: 1) RCACopilot (Chen et al., EuroSys 2024; the matrix key is `ahmed2023llmrca`), 2) PyRCA (Liu et al., Salesforce 2023), 3) PetShop dataset (Hardt et al., CLeaR 2024).
All read in full: RCACopilot read in detail to p.12 (tail skimmed); PyRCA and PetShop in full; figures not inspected in any.
Scopus: PyRCA is an arXiv technical report (not indexed); RCACopilot (EuroSys) and PetShop (PMLR/CLeaR) not checked in the Scopus preview. SJR quartiles unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side
| | RCACopilot | PyRCA | PetShop | Ours |
|---|---|---|---|---|
| Type | LLM incident classification | toolkit | benchmark | RCA + untested risk |
| Labels | labelled history + hand-built handlers | none | n/a | none |
| Telemetry | logs, stacks, metrics | metrics | metrics 5-min + service map | traces (+ metrics) |
| Propagation | none | PC/GES + walks/tests | graph given | edge probabilities |
| Data (open?) | no | synthetic generator | yes (stated) | open |
| Headline | micro-F1 0.766 (about 160 test incidents) | HT recall 1.00 on its own synthetic | ranked correlation competitive | none on real faults |
| Evidence quality | 2 | 1 | 3 | 1 |

## 2. What each means for our claims
- **RCACopilot:** LLM-based incident classification (not localization) on one service; baselines near zero; useful only as an explanation-layer reference. It is the source of the "76.6%" that Vangapelli relays as "accuracy" (it is micro-F1 on a category prediction task).
- **PyRCA:** tooling; its perfect Recall@1 for hypothesis testing is a property of the synthetic generator. Source of baseline implementations (HT/CIRCA, RCD, epsilon-diagnosis).
- **PetShop:** small public benchmark where ranked correlation beats methods that learn graphs or SCMs from 5-minute data; all methods produce false root causes on normal data. Supports adding a correlation/NSigma baseline and a normal-period false-alarm check.

## 3. Does this batch change the problem statement?
- No change. It reinforces the evaluation lessons: simple baselines are strong on small benchmarks; report specificity on normal periods.

## 4. Baselines and datasets to add because of this batch
- Ranked correlation among anomalous nodes (MAD filter) as a baseline.
- Normal-period false-alarm rate for every method (PetShop shows all methods fail it).
- PetShop (68 issues, service map given): optional public test set; download needs the user's permission (not done). PyRCA as a source of HT/RCD baselines (not installed).

## 5. Claims in our draft that this batch contradicts or weakens
- Any use of RCACopilot's 76.6% as evidence of RCA accuracy.
- Any claim that causal graph learning improves localization without comparing to ranked correlation.

## 6. Sentences we can safely write (with citation keys)
- "LLM-based incident classification with few-shot retrieval has been deployed at Microsoft [RCACopilot]."
- "On the 68-issue PetShop benchmark, a ranked-correlation baseline was competitive with or better than methods that learn graphs or structural models from small samples [PetShop]."
- Do NOT write: RCACopilot's F1 as RCA accuracy; PyRCA's synthetic recall as real performance.

## 7. Corrections needed to earlier notes or reports
1. The literature matrix key `ahmed2023llmrca` (title "Automatic Root Cause Analysis via LLMs for Cloud Incidents", arXiv 2305.15778) is RCACopilot by Chen et al.; Ahmed et al. (ICSE 2023) is a different paper cited inside it. Fix the author attribution in `docs/literature/literature_matrix.csv` and REVIEW_REPORT.
2. `theysayitsre` note (batch 7): "RCACopilot 76.6% accuracy across a year of Microsoft incidents" is micro-F1 for root cause category on about 25% held-out incidents of one service (653 total).
3. PetShop year: arXiv 2023, PMLR CLeaR 2024; the matrix says 2023.

## 8. Proposals (no code changed)
- Add ranked correlation and SimpleRCA baselines; report specificity on normal windows.
- Consider PetShop and RCAEval RE1/RE2 as public test sets after permission to download.
