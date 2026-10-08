# Batch 13: 2026-10-08

Papers: 1) Motter and Lai (Phys. Rev. E 2002). Single paper; it was the last open-access PDF in the queue.
Read in full: yes (figures via captions only). Scopus: ISSN 1063-651X not checked (unverified). SJR quartile unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side (with the other cascade theory paper)
| | Motter and Lai | Buldyrev et al. (batch 12) | Ours |
|---|---|---|---|
| Mechanism | overload from load redistribution | mutual connectivity loss | noisy-OR over edge probabilities |
| Data | model + Internet + US grid | model networks | measured traces |
| Headline | one load-based attack affects more than 60% of nodes at alpha 0.2 | critical degree 2.445 | none on real faults |

## 2. What it means for our claims
- Load heterogeneity and a few key nodes drive cascades (p.2). Our risk model has no load or capacity term, which should be stated as a limitation. It does not evidence anything about microservice anomaly propagation.

## 3. Does this batch change the problem statement?
- No.

## 4. Baselines and datasets to add
- None. Optional: a load-dependent cascade ablation in simulation (propose only).

## 5. Claims in our draft that this batch weakens
- Any claim that independent noisy-OR probabilities capture overload cascades.

## 6. Sentences we can safely write (with citation keys)
- "Cascades of overload failures triggered by one high-load node can disconnect large parts of heterogeneous networks [Motter and Lai]."
- Do NOT write: that it models microservice request propagation.

## 7. Corrections needed to earlier notes or reports
- None.

## 8. Proposals (no code changed)
- Add a limitation sentence: edge probabilities are load-independent.
