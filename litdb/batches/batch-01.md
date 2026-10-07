# Batch 01: 2026-10-07

Papers: 1) li2026service, 2) yao2024chain, 3) sun2025interpretable. All read in full: yes, with exceptions: Li p.12 Algorithm 1 body and Figs 1-4, 8 not read; Yao Appendix A absent from the PDF and Figs 1-3 not inspected; Sun Figs 1-11 not inspected. All tables were read.
Per-paper reports: `litdb/reports/<key>.md`. Notes: `litdb/papers/<key>.md`.

Reminder: Scopus status below is a venue-level check on the public Scopus Sources preview (2026-10-07). No Scopus Source List or Scimago file is in `litdb/reference/`, so SJR quartiles are unknown. Please download one in your browser and drop it there.

## 1. Side-by-side
| | Li 2026 (`li2026service`) | Yao 2024, CoE (`yao2024chain`) | Sun 2025, DeepHunt (`sun2025interpretable`) | Ours (rca-lab) |
|---|---|---|---|---|
| Task | cascade/propagation prediction, path ranking, risk score | event-level root-cause ranking inside an incident | instance-level root-cause ranking given a detected failure | RCA ranking + untested cascade-risk score |
| Labels needed | yes (supervised on labelled failures; a self-supervised add-on is mentioned p.14) | yes (root-cause events from SRE tickets, p.6) | no at cold start; optional operator feedback | no (baseline-window calibration) |
| Telemetry | metrics, logs, API traces, config | events from metrics, logs, traces, ops activities | traces, logs, metrics, deployment topology | traces (+ optional Prometheus/Loki, SSH docker) |
| Propagation / graph | GAT + temporal net + noisy-OR (Eq.21) | learned event-pair weights, chain scoring | GAE + first-order up/downstream max; learned weights tiny (Table 7) | edge probabilities, mostly prior |
| Forecasts failures | yes (claimed, horizons 5 min to 24 h) | no | no | claimed, untested |
| Data (open?) | proprietary; promised, not verified | proprietary; code public | D1 public (GitHub README + MEGA link, not verified), D2 NDA; code public | open, synthetic + one healthy live system |
| Baselines | generic ML/graph, 2 adapted domain methods, industry tools; no propagation-prediction work | PageRank, GCN, GAT, GraphSAGE, Groot | 9 methods incl. DejaVu, Eadro, DiagFusion | random, earliest, anomaly-only, own PageRank |
| Headline result | F1 about 0.93; P 0.94, R 0.92 (Table 7 p.20; internally inconsistent) | Service top-1 79.3%, top-3 98.8%; Business 85.3% / 96.6% (Table 2 p.10) | zero labels: A@5 0.959 (D1), 0.903 (D2); 30% labels A@5 0.966 / 0.946 (Table 3 p.17) | none on real faults |
| Evidence quality (1-5) | 2 | 2 | 3 | 1 |
| Scopus status | venue indexed (CiteScore 2025 6.2, 75th pct); quartile unknown | unverified (ACM proceedings, no ISSN) | venue indexed (CiteScore 2025 11.6, 89th pct); quartile unknown | n/a |

## 2. What each means for our claims
- **Li 2026:** closes the door on "nobody predicts cascades"; its noisy-OR cascade formula (Eq.21 p.10) is the same functional form as our cascade-risk, so that component is not novel. Its evidence is not credible enough to be a performance bar: proprietary data, numbers that disagree (detection-time reduction 63.2% in the abstract vs 38.5% in Table 7; 3, 8 or 93 systems depending on the page), labels built from the same signals used as features.
- **Chain-of-Event:** supervised event-level propagation weights. It shows that learned weights beat uniform and rule-based weights on their data (Table 4), which sets what a good estimator can add. It confirms the earlier correction that CoE is supervised. Our event-level variant is not new.
- **DeepHunt:** the decisive paper for our positioning. Label-free multimodal localization already exists and works (A@5 above 0.9 with zero labels), peer-reviewed in a strong venue, with open code and one open dataset. Its label-free mode is effectively averaged reconstruction-error ranking, and its learned propagation weights are small, with no ablation isolating them.

## 3. Does this batch change the problem statement?
- Real? The problem is real in the sense that labelling is costly (cited: four experienced operators nearly a month for 1,000 cases, DeepHunt p.2) and RCA is hard for SREs (asserted in all three). None of the three measures debugging time or incident cost; the evidence is mostly assumed or anecdotal (see PROBLEM_EVIDENCE.md A1-A10).
- Already solved? Label-free RCA: largely addressed by DeepHunt. Cascade forecasting: claimed by Li (unverifiable), not by the other two. Learned propagation weights: addressed with labels by CoE.
- Misframed? "Unlabeled RCA" and "cascade prediction under-explored" are both misframed. Defensible framing: an open, honest evaluation of whether propagation structure adds value beyond a deviation-ranking baseline in label-free RCA, plus an independently labelled early-warning test. Both DeepHunt (tiny weights) and our own synthetic ablations point to propagation adding little, so that question is genuinely open and testable.

## 4. Baselines and datasets to add because of this batch
- Run DeepHunt (code public) on D1 and on RCAEval or our OTel runs, and a reconstruction-error-only control (its 0%-label mode).
- Add a "mean deviation over window, no graph" baseline; DeepHunt's own cold start suggests it will be strong.
- Use D1 (Aiops-Dataset, README links a MEGA file; ask the user before downloading; 46 instances, 210 failures) as a second public dataset beside RCAEval.
- CoE can be a supervised reference only if we can label events; low priority.
- Li 2026: not runnable (no code or data).

## 5. Claims in our draft that this batch contradicts or weakens
- "Early identification of cascading-failure risk is not sufficiently understood" (draft related work): contradicted by Li 2026 as a claim, whatever its quality.
- "Unsupervised/label-free RCA" as a contribution: contradicted by DeepHunt's zero-label cold start.
- "Learned propagation probabilities" as a contribution: CoE (supervised) and Li (supervised, noisy-OR) both exist.
- "DeepHunt uses a static dataset / is not live": wrong; DeepHunt has an online localization stage (0.17 to 0.26 s per case, p.20) and a feedback loop. It is evaluated on recorded datasets.
- "Propagation-aware modelling improves RCA": not supported by DeepHunt's own parameters (Table 7) and not by our ablations.

## 6. Sentences we can safely write (with citation keys)
- "Label-free localization with graph autoencoders trained on normal data has been shown to rank the true root cause in the top five in over 90% of cases on two datasets without any failure labels [sun2025interpretable]."
- "Supervised event-graph methods learn event-pair propagation weights from labelled incidents [yao2024chain]; unsupervised variants were left as future work by their authors."
- "Supervised GNN approaches to failure-propagation prediction have been proposed, but the reported results rely on proprietary data that was not available at publication [li2026service]."
- "Operator labelling of root causes is costly; one cited estimate is four operators for nearly a month per 1,000 cases [sun2025interpretable, citing RCLIR]."
- Do NOT write: any Li 2026 percentage as established fact; that CoE or DeepHunt forecast failures; that DeepHunt needs labels; that D2 of DeepHunt is open.

## 7. Corrections needed to earlier notes or reports
1. `docs/REVIEW_REPORT.md` section 3.2 and section 0 point 2 call DeepHunt "label-light (self-supervised + 1% labeled failures)". Correction: the paper reports full zero-label results (A@5 0.959 and 0.903, Table 3 p.17; "zero-label cold start", p.13); at 1% labels A@5 is 0.966 and 0.910. DeepHunt is label-free at cold start and label-light for improvement. The "label-free is not unique" conclusion is stronger, not weaker.
2. REVIEW_REPORT states that DeepHunt has an online stage: confirmed (0.169 s and 0.262 s per case, Table 6 p.20), but failure detection is out of its scope (p.6), so "online" means diagnosis after detection.
3. DeepHunt's abstract says "two open source datasets"; only D1 is open (p.15). Our own notes should not say both are open.
4. REVIEW_REPORT lists AID as "predicts cascading impact via dependency intensity" from its abstract. DeepHunt cites it as "prediction of aggregated intensity of dependency" (ref [51], title only). Cascade impact is not evident from that title; verify AID in full before calling it cascade-prediction prior art.
5. Li 2026 ref 22 is DeepHunt, and Li's Table 5 describes it as expert-rule-based; that description is wrong. Our table of prior art should not copy Li's characterisation.
6. REVIEW_REPORT section 3.2 marks Li 2026 "partly label-free (self-supervised pretraining)". Correction: the main model is supervised (Eq.17); the self-supervised element is a single paragraph (p.14) claiming 87% of supervised performance with 70% less labelling, with no table.
7. REVIEW_REPORT lists Chain-of-Event as supervised: confirmed (p.6); the CoE paper itself describes the method as supervised.
8. Our noisy-OR cascade formula equals Li's Eq.21 in form; the draft must not present the formula as new.
