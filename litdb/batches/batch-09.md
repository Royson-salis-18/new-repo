# Batch 09: 2026-10-08

Papers: 1) Seer (Gan et al., arXiv 2018 short version), 2) CIRCA (Li et al., KDD 2022), 3) MicroHECL (Liu et al., arXiv 2021).
All read in full: yes (figures not inspected; CIRCA appendices only skimmed).
Scopus: Seer and MicroHECL are arXiv preprints (not Scopus-indexed); CIRCA is KDD '22 proceedings (not checked in the Scopus preview). SJR quartiles unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side
| | Seer | CIRCA | MicroHECL | Ours |
|---|---|---|---|---|
| Type | early-warning method (supervised) | causal RCA (label-free) | call-graph RCA (supervised detectors) | RCA + untested risk |
| Labels | manual QoS labels | none | trained detectors | none |
| Telemetry | queue-depth traces | metrics | call metrics RT/EC/QPS | traces (+ metrics) |
| Propagation | implicit | CBN from architecture + criterion | type-specific direction + pruning | edge probabilities |
| Forecasting | yes (QoS) | no | no | claimed, untested |
| Data (open?) | own apps, unreleased | proprietary; code stated | proprietary | open |
| Headline | 91% / 89% (own apps) | AC@1 0.404 vs NSigma 0.323 (99 cases) | HR@3 0.67 vs 0.49 (75 cases) | none on real faults |
| Evidence quality | 1 | 3 | 2 | 1 |

## 2. What each means for our claims
- **Seer:** prior art for early QoS-violation warning plus culprit naming (supervised, own apps, no external baseline). Our claim must be label-free, explicit propagation, calibrated, open.
- **CIRCA:** established label-free, architecture-aware metric RCA. A must-run baseline. Its simple NSigma baseline is the runner-up on real data, so NSigma and BARO belong in our comparison. Its gain over NSigma is 8 cases out of 99.
- **MicroHECL:** supervised call-graph RCA; contributes the observation that traffic anomalies propagate upstream to downstream and latency/error anomalies downstream to upstream.

## 3. Does this batch change the problem statement?
- Real? Industrial demand is claimed by Alibaba and by CIRCA's bank case; numbers are proprietary.
- Already solved? Early warning with culprit (Seer) and label-free causal RCA (CIRCA) both exist.
- Misframed? Yes if we say "unlabeled RCA" or "early warning" is new. The defensible space: label-free, trace-based, explicit propagation edges, cascade-risk output with calibration, honest negative controls, open artifacts.

## 4. Baselines and datasets to add because of this batch
- CIRCA (in RCAEval) and NSigma as baselines; BARO if available.
- Report a constant/simple baseline and AC@1 with counts, not only AC@k.
- Direction-by-anomaly-type as an ablation in our propagation model.

## 5. Claims in our draft that this batch contradicts or weakens
- "Label-free RCA is new" and "early warning with culprit identification is new".
- Any claim that propagation modelling beats simple baselines without testing against NSigma.

## 6. Sentences we can safely write (with citation keys)
- "Seer anticipates QoS violations and names the culprit microservice from queue-depth traces with a supervised network [Seer]."
- "CIRCA ranks metrics without labels by testing deviation from regression on causal parents [CIRCA]."
- "MicroHECL traverses a dynamic call graph with type-specific propagation directions [MicroHECL]."
- Do NOT write: Seer's 91% / 89% as general accuracy; CIRCA's 25% as robust; MicroHECL's numbers as reproducible.

## 7. Corrections needed to earlier notes or reports
1. `litdb/papers` AID note (batch 8): CIRCA's reference list cites AID as ASE 2021, pp.653-665 (verified from CIRCA ref [26], second-hand); the AID note said the published venue was unverified. Resolved: ASE 2021 (second-hand).
2. REVIEW_REPORT lists Seer as forecasting prior art: this arXiv version is a short supervised early-warning system; the full ASPLOS 2019 paper was not read.
3. CIRCA's Table 3 shows NSigma is the strongest baseline on real data: relevant for our baseline selection (REVIEW_REPORT).

## 8. Proposals (no code changed)
- Add NSigma and CIRCA to the baseline set; compute AC@1 with n, and add a bootstrap CI.
- Model direction by anomaly type (latency/error downstream to upstream; traffic upstream to downstream) as a propagation ablation.
