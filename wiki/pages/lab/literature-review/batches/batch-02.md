# Batch 02: 2026-10-07

Papers: 1) pham2024root, 2) pantang...microrca (MicroRCA-Agent), 3) zimingzhao...chase (CHASE). All read in full: yes, with exceptions: Pham Table 5 columns scrambled in extraction (values flagged inferred), Figs 1-4 and supplementary material not read; MicroRCA-Agent prompt images (Figs 13, 16, 18) and case figures (19-22) not read; CHASE Figs 1-4 not inspected and its Google Drive code link not opened.
Reports: `litdb/reports/`. Notes: `litdb/papers/`.
Scopus: Pham = unverified (ACM proceedings without ISSN); MicroRCA-Agent and CHASE = arXiv preprints, not indexed, not peer reviewed. SJR unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side
| | Pham 2024 | MicroRCA-Agent 2025 | CHASE 2024/25 | Ours |
|---|---|---|---|---|
| Task | benchmark of 9 causal discovery + 21 RCA methods | LLM-agent localization + explanation (competition) | per-trace instance RCA with hypergraph | RCA + untested cascade risk |
| Labels needed | no (compared methods are label-free) | no failure labels; fits Drain and Isolation Forest on competition phase-one data | yes (supervised cross-entropy) | no |
| Telemetry | metrics only | logs, traces, metrics, TiDB | traces, logs, metrics | traces (+ optional metrics, SSH) |
| Propagation / graph | causal discovery found weak; graph-free NSigma, BARO strong | none explicit; LLM reasons | hypergraph over call-graph ancestry, equal weights | edge probabilities, mostly prior |
| Forecasts failures | no | no | no | claimed, untested |
| Data (open?) | open (Zenodo CC-BY, RCAEval MIT) | code open; data partly (URL unchecked) | public datasets; code on Drive (unverified) | open |
| Baselines | 21 methods + random Dummy | none | 7 baselines (some mis-described) | random, earliest, anomaly-only, own PageRank |
| Headline result | no method best everywhere; many near random; NSigma/BARO fastest, 0.01 s | score 50.71 (log+metric 51.27) | GAIA A@1 0.6135 vs 0.4503; AIOps2020 Percentage@1 0.22 vs 0.17 | none on real faults |
| Evidence quality (1-5) | 4 | 1 | 2 | 1 |
| Scopus status | unverified | not indexed | not indexed | n/a |

## 2. What each means for our claims
- **Pham:** the strongest piece of evidence for how we must evaluate. Simple, graph-free, label-free methods (NSigma, BARO) beat most graph-based ones on real injected faults, and synthetic results do not transfer. Our synthetic-only results are exactly what it warns against. It also makes explicit that a Dummy random baseline and a wrong failure time must be tested.
- **MicroRCA-Agent:** an engineering example of non-LLM detectors feeding an LLM, with no baselines and an undefined score. It is not evidence that LLM agents localize well; its own bad case shows hallucination. Fits our plan to keep the LLM as explanation layer, but we would have to evaluate faithfulness.
- **CHASE:** supervised GNN on a 10-instance dataset; its "causal" hypergraph is call-graph ancestry. No consequence for our claims except as one of many supervised GNN localizers.

## 3. Does this batch change the problem statement?
- Real? Pham gives measured evidence that RCA remains unsolved in the sense that sophisticated causal-graph methods are near random on benchmarks, but the evidence is about method quality, not incident cost. Cost and time statements in Pham (hours to diagnose, Amazon downtime cost) are second-hand.
- Already solved? No. But the bar is lower-complexity than expected: label-free statistical deviation methods already work well on benchmark faults.
- Misframed? Any claim that propagation modelling improves RCA is unsupported by Pham's finding that graph-free methods win. The honest framing remains: does propagation or cascade modelling add anything beyond simple deviation scoring, and can it forecast.

## 4. Baselines and datasets to add because of this batch
- RCAEval (MIT): BARO, NSigma, CIRCA, RCD, CausalRCA plus the Dummy baseline, with Online Boutique, Sock Shop 1 and 2, Train Ticket datasets from Zenodo 13305663 (CC-BY, sizes 3.5 to 79 MB for the smaller ones). Needs the user's permission to download.
- Add a service-frequency prior baseline (faults are injected into five services only).
- Test failure-time misspecification (60 s shift) as Pham does.
- Report Avg@1 and Avg@3 and per-fault-type results.
- CHASE and MicroRCA-Agent: not needed as baselines.

## 5. Claims in our draft that this batch contradicts or weakens
- Any statement that synthetic data results support method superiority: Pham states that synthetic performance may not reflect real systems.
- "Graph-based or causal propagation modelling improves root cause ranking": weakened; causal-discovery methods were mostly near the random baseline (p.6).
- "LLM agent improves RCA": not supported; MicroRCA-Agent has no baseline and shows hallucination.

## 6. Sentences we can safely write (with citation keys)
- "Pham et al. [pham2024root] evaluated nine causal discovery and twenty-one RCA methods and found no method best in all situations; several graph-based methods performed close to a random baseline, while NSigma and BARO were accurate and fastest."
- "Performance on synthetic data did not reliably predict performance on real benchmark systems [pham2024root]."
- "LLM-based RCA pipelines have been reported in an AIOps competition setting, with LLM-hallucinated reasoning observed in failure cases [MicroRCA-Agent key]."
- "Supervised graph-learning localizers such as CHASE need labelled traces [CHASE key]."
- Do NOT write: that Pham et al. evaluated event-based methods or proved any approach correct; that MicroRCA-Agent or CHASE are peer reviewed; that CHASE infers causality; that the competition score is an accuracy.

## 7. Corrections needed to earlier notes or reports
1. REVIEW_REPORT correction table #11 is confirmed in substance: Pham et al. did not evaluate event-based methods; NSigma and BARO are the fastest (0.01 s, Table 6); PC/FCI ran out of memory on the 50-node RCD synthetic set and some methods exceeded 1 to 2 hour limits. One nuance: the paper's Table 6 shows BARO and NSigma at 0.01 s on every dataset, so "consistently the fastest" is accurate.
2. REVIEW_REPORT section 0 point 8 says RCAEval has 735 cases and CC-BY: that is the later RCAEval benchmark; the dataset in this paper (Zenodo 13305663) is a separate CC-BY-4.0 artifact with Sock Shop 1 and 2, Online Boutique and Train Ticket. Both are under CC-BY; do not confuse them (unverified here for the 735-case set).
3. Pham's first author also wrote BARO, which ends up among the best methods: a conflict of interest not stated in the paper. Our notes should mention this when citing BARO's ranking.
4. REVIEW_REPORT row "MicroRCA-Agent: Isolation Forest + LLM; code released": confirmed; but the paper does not name its LLM (the README mentions DeepSeek) and reports no baselines.
5. The REVIEW_REPORT said CHASE was read only skimmed; now read: supervised, GAIA has only 10 instances, AIOps 2020 metric is not localization accuracy, baselines are mis-described. Update any note that says CHASE "outperforms" without these caveats.
