# Batch 10: 2026-10-08

Papers: 1) Fang et al. 2025 (Rethinking RCA evaluation, arXiv), 2) DéjàVu (Li et al., FSE 2022), 3) RCAgent (Wang et al., CIKM 2024).
All read in full: yes except DéjàVu's final discussion tail and references; figures not inspected in any.
Scopus: Fang et al. is an arXiv preprint (not indexed; ACM version unchecked); DéjàVu (FSE) and RCAgent (CIKM) proceedings not checked in the Scopus preview. SJR quartiles unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side
| | Fang et al. | DéjàVu | RCAgent | Ours |
|---|---|---|---|---|
| Type | benchmark + re-evaluation | supervised GNN RCA | LLM-agent RCA (zero-shot) | RCA + untested risk |
| Labels | n/a | supervised | none (LLM) | none |
| Telemetry | metrics, logs, traces | metrics (graph from traces + CMDB) | logs, code, advisor DB | traces (+ metrics) |
| Propagation | studies it | GAT on call + deployment edges | none | edge probabilities |
| Forecasting | no | no | no | claimed, untested |
| Data (open?) | promised | stated package | proprietary | open |
| Headline | 11 methods mean Top@1 0.21 | MAR 1.66-5.03; A@5 79-96% | G-Correctness 5.22 vs 3.06 | none on real faults |
| Evidence quality | 3 | 3 | 2 | 1 |

## 2. What each means for our claims
- **Fang et al.:** the strongest external argument for our evaluation design. On public benchmarks a rule-based alert counter matches or beats SOTA; 68% of cases have symptoms only in the injected service; 99% lack some telemetry. Propagation-aware methods cannot show an advantage on such data. On their harder benchmark SimpleRCA still has the highest Top@5 (0.80), so a SimpleRCA baseline is mandatory.
- **DéjàVu:** supervised RCA whose graph includes deployment (co-location) edges; ablation shows graph aggregation helps; Random Forest beats it on A@1 on two datasets.
- **RCAgent:** LLM-agent explanation prior art on Flink jobs; weak evidence; reusable evidence-matching filter.

## 3. Does this batch change the problem statement?
- Real? 74.38% of bank failure tickets recurring and 28.98 min average diagnosis (DéjàVu, single bank); 84.4% of injected faults silent (Fang et al.).
- Already solved? Supervised graph RCA with deployment edges (DéjàVu) exists; label-free RCA (CIRCA) exists.
- Misframed? We must frame propagation value around hard cases (silent or attenuated root symptoms) and compare against SimpleRCA.

## 4. Baselines and datasets to add because of this batch
- SimpleRCA: per-service count of threshold alerts (3-sigma/P95 on metrics, 3x P95 latency on traces, error keywords in logs).
- Evaluate on cases classified by Fang et al.'s Type I / II / III (root symptom only / no symptom / other service louder) and report each separately.
- If their benchmark is released: candidate hard test set (needs the user's permission to download; not downloaded).

## 5. Claims in our draft that this batch contradicts or weakens
- Any claim that propagation modelling improves localization without a SimpleRCA comparison.
- Any claim that unsupervised/learned graph methods are state of the art on public benchmarks.

## 6. Sentences we can safely write (with citation keys)
- "Simple alert-counting rules match state-of-the-art RCA on several public benchmarks, because most faults manifest only in the injected service [Fang et al., Tables 2-3]."
- "DéjàVu models failure propagation over call and deployment relations and is supervised [li2022actionable]."
- "LLM agents have been applied to cloud job-failure RCA [RCAgent]."
- Do NOT write: Table 5 values as verified; that the new benchmark shows simple rules fail.

## 7. Corrections needed to earlier notes or reports
1. `docs/REVIEW_REPORT.md` and the literature matrix list the Fang et al. paper as `rethink2026` with DOI 10.1145/3797100; the arXiv text is v2 (Dec 2025); the DOI/venue is unverified here.
2. REVIEW_REPORT's characterization of DéjàVu as a purely "recurring-failure" method is correct; additional: its graph includes deployment edges (co-location), not only calls.
3. The abstract of Fang et al. says 25 fault types across 6 categories; the text says 31 types across 7 categories before filtering; categories after filtering unstated.

## 8. Proposals (no code changed)
- Add SimpleRCA to the evaluation harness; classify cases by Type I/II/III using the thresholds in Fang et al. (2x pre-fault average).
- Add co-location edges (same host/pod set) as an optional propagation channel and test their effect on cases of Type III.
