# Batch 08: 2026-10-08

Papers: 1) AID (Yang et al., arXiv 2021), 2) Unyi et al. (IEEE TNSM 2025, GNN fault forecasting), 3) STMformer (Xu et al., arXiv 2024).
All read in full: yes (figures not inspected; Unyi Table III values and Table I did not extract).
Scopus: AID and STMformer are arXiv preprints (not Scopus-indexed); TNSM ISSN 1932-4537 not yet checked in the Scopus preview. SJR quartiles unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).
Note: these three PDFs came from arXiv and an institutional repository (open access) via `litdb/tools/fetch_oa.py`, with your permission.

## 1. Side-by-side
| | AID | Unyi et al. | STMformer | Ours |
|---|---|---|---|---|
| Type | method (edge strength) | method (simulation) | method (metric forecasting) | RCA + untested risk |
| Task | dependency intensity from traces | graph-level fault probability regression | pod metric forecasting | RCA + cascade risk |
| Labels | none (labels for eval) | simulator labels | none | none |
| Telemetry | traces | none | eBPF metrics + TCP connections | traces (+ metrics, SSH) |
| Propagation | time-warped caller/callee similarity | GNN on retry/MDP model | GAT + attention + host grouping | edge probabilities |
| Forecasting | no | no (aggregate formula) | metric values only | claimed, untested |
| Data (open?) | stated, unchecked | synthetic, stated, unchecked | own, dataset not stated | open |
| Headline | Industry CE 0.327 vs 0.603 | R2 0.99 on synthetic | MAE 0.0166 vs 0.0171 (step 16) | none on real faults |
| Evidence quality | 2 | 1 | 2 | 1 |

## 2. What each means for our claims
- **AID:** closest to our edge-weight learning: label-free, trace-based, evaluated against 94 hand-labelled edges. It does not forecast. Our edge-probability estimator must be compared with its DSW similarity; the 89% strong labels mean a constant predictor is a necessary baseline.
- **Unyi et al.:** "GNN fault forecasting" that is simulation-only and regresses a model-checker output from its own inputs. It cannot be used as evidence that cascade risk is predictable from real telemetry.
- **STMformer:** forecasts metric values; uses host co-location and TCP connection graphs. Supports our limitation that call-edge-only propagation misses co-location. Its abstract gains do not match its tables, and Table 3 has an impossible MAE/RMSE pair.

## 3. Does this batch change the problem statement?
- Real? AID reports five of 13 public AWS outages as dependency-related (Table I p.4) and engineer interviews at one company; thin but consistent.
- Already solved? Less than assumed: none of the three forecasts real failures or cascades from telemetry. Label-free edge strength from traces is covered (AID).
- Misframed? Our claim should be "label-free, trace-based cascade-risk scoring with calibrated evaluation", not "first to learn edge strength".

## 4. Baselines and datasets to add because of this batch
- AID (github.com/OpsPAI/aid): propagation-weight baseline (DSW similarity per call edge), and its released TT dataset with 19 labelled edges.
- A constant "strong" predictor and a persistence baseline for forecasting tasks (reporting hygiene seen missing here).
- Check STMformer repo and dataset availability before citing the dataset.

## 5. Claims in our draft that this batch contradicts or weakens
- Any claim that learning call-edge strength without labels is new (AID).
- Any claim that GNN fault forecasting exists for real telemetry (Unyi is synthetic only).

## 6. Sentences we can safely write (with citation keys)
- "AID estimates continuous dependency intensity from traces without labels [tianyiyang...2021efficient]."
- "Forecasting models that use host co-location and connection graphs exist [yifeixu...2024system]; they forecast metrics, not failures."
- "A GNN has been trained to predict model-checker fault probabilities on synthetic service meshes [unyi2025explainable]; real-trace evaluation is future work (p.16)."
- Do NOT write: AID's 45.8% / 61.1% / 33.2% as general performance; STMformer's 8.6% / 2.2%; Unyi's R2 values as evidence of forecasting.

## 7. Corrections needed to earlier notes or reports
1. `docs/REVIEW_REPORT.md` section 3.2 (checked by abstract only): AID "predicts cascading impact via dependency intensity" is imprecise: it predicts the dependency intensity value (edge strength); it does not forecast failure impact or time.
2. REVIEW_REPORT's IEEE TNSM 2025 entry ("GNN fault forecasting with probabilistic propagation") is a simulation-only paper with synthetic labels; it is weaker prior art than assumed.
3. PROBLEM_EVIDENCE.md section B row 1 (AID: "predicts cascading impact via dependency intensity") and row 2 (TNSM 2025) should be read with these corrections; updated in this batch.

## 8. Proposals (no code changed)
- Add a per-edge AID-style DSW similarity as an alternative edge weight and compare to our learned weights on RCAEval.
- Report a constant-prediction baseline and ECE/Brier for any risk output.
