# Report: Yao et al. (2024), Chain-of-Event (CoE)

Key `yao2024chain`. Structured note: `litdb/papers/yao2024chain.md`. Page numbers are PDF pages (ACM cover = p.1).
Reading coverage: full text read to the end including references. Not available: Appendix A (error-bound proof) is cited but absent from this PDF. Figs 1-3 are diagrams and were not inspected visually; Tables 1-6 were readable as text.

## (a) Bibliographic block
- Zhenhe Yao, Changhua Pei, Wenxiao Chen, Hanzhang Wang, Liangfei Su, Huai Jiang, Zhe Xie, Xiaohui Nie, Dan Pei (Tsinghua, UCAS/CNIC, eBay). "Chain-of-Event: Interpretable Root Cause Analysis for Microservices through Automatically Learning Weighted Event Causal Graph". FSE Companion '24, Porto de Galinhas, 15-19 July 2024. ACM, DOI 10.1145/3663529.3663827, ISBN 9798400706585. Open access CC BY 4.0. Received 2024-02-08, accepted 2024-04-18 (p.13). ACM page lists 9 citations as of 3 March 2026 (p.1).
- ISSN: none. Scopus: unverified (a proceedings volume without ISSN; the Scopus preview title search was not usable). SJR quartile: unknown, no list supplied.
- Peer review: conference companion volume with an acceptance process; the PDF does not name the track, so I do not claim more.

## (b) Plain-language summary
CoE converts monitoring data into labelled events and works out which event in an incident is most likely the origin. It starts from a graph linking events in the same or neighboring services, and learns weights from past incidents so the true origin scores highest. The result is a small, readable model (52 KB, p.10) whose weights operators can inspect and edit. It reports 79.3% top-1 on service incidents and 85.3% on business incidents from one large e-commerce company.

## (c) Problem and motivation
Three challenges are stated (pp.3-4): multi-modal data, interpretability aligned with SRE knowledge, automatic causality learning. The motivation that incidents are costly and RCA is hard is asserted with general citations; there are no incident-cost or time-to-diagnose numbers (evidence type: assumed). The industrial scale (over 5,000 services, 10 TB per day, p.5) shows the setting is real but is not evidence of the RCA gap itself.

## (d) Method (re-implementation level)
Events are triples (what, when, where) from metrics, logs, traces and operator actions; how they are produced in the experiments is not specified. For an incident, build a naive graph: all event pairs in the same service get bidirectional edges, pairs in adjacent services get an edge in call direction (pp.6-7). Learnable tables: R_s (same-service event-type pair weights), R_d (cross-service), and S (importance per event type). Inference follows Algorithm 1 (p.8): edge weight E[(a,b)] from R_s or R_d; k = alpha times the mean outgoing weight sum (alpha = 0.2); start scores = normalized S; iterate up to T = 100 steps spreading mass along edges with transition weight E/(sum + k); the leftover k/(sum + k) share is "self-caused" and accumulates into the root cause score, multiplied by a length bonus min(1, 0.01 * 2^(i-1)). Training minimizes the negative score of the labelled root-cause event with Adam plus L2, learning rate 4e-5, about 45 minutes per dataset (pp.8-10). Optional human edits to weights (p.9). Assumptions: labelled historical incidents, known service call graph, pre-extracted events, root cause observable as an event.

## (e) Datasets, protocol, leakage
One proprietary e-commerce system (over 5,000 services, three data centers, 185 million users). Two datasets of real incidents from Jan 2020 to Apr 2021: Service (service-level) with 170 incidents and Business with 782 incidents (p.9; conclusion says 952 total, p.11). Split evenly into train and test with random splitting; labels via keyword search over remediation tickets. The Service-dataset percentages are consistent with a test set of about 82 incidents (my inference), so one case is about 1.2 points. Leakage risk: random rather than temporal splits and per-event-type parameters allow memorizing recurring incident patterns. Results "stay the same in five repeated experiments" (p.10), which points to a fixed setup rather than variance across splits.

## (f) Results (copied)
Table 2 (p.10), top-1 / top-3: Service: CoE 79.3% / 98.8%; Groot with manual graph 74% / 92%; CoE with manual graph 78.1% / 93.9%; GraphSAGE 62.2% / 78.1%; GCN 29.3% / 57.3%; GAT 12.2% / 47.6%; Groot without manual graph 17.1% / 48.8%; PageRank 16.1% / 25.3%. Business: CoE 85.3% / 96.6%; GraphSAGE 81.1% / 93.7%; Groot with manual graph 81% / 96%; CoE with manual graph 78.7% / 95%; GCN 69.2% / 85.3%; GAT 60.5% / 79.2%; Groot without manual graph 23.2% / 45.5%; PageRank 1.2% / 1.8%. Ablation (Tables 3-5, pp.10-11): learning R_s is the largest single factor on the Service dataset (51.2% top-1 without it vs 79.3%); bonus terms add about 3.7 points top-1 on Service. Efficiency (p.10): 4.06 s per Business incident (18.73 events), 2.16 s per Service incident (14.70 events), 52.06 KB model. No statistical tests, no confidence intervals, no variance across splits.

## (g) Limitations and stern critique
Authors: future work toward unsupervised or active learning (p.11). Mine: (1) supervised, yet marketed as needing "no manual configuration" (Table 1, p.4; labelling cost asserted as free, p.6); (2) one proprietary system, small test sets, one split, no statistics; (3) event generation hidden; (4) gains over simple GraphSAGE on Business are 4.2 points top-1 and the top-3 gain over Groot is 0.6 points, which is small relative to likely noise at n of a few hundred; (5) "surpasses human expertise" (p.10) rests on one manual graph built by the authors' rules; with the manual graph CoE scores below Groot and GraphSAGE on Business top-1; (6) random splits invite memorization; (7) weights are normalized transition weights with a self-cause remainder, not calibrated trigger probabilities; (8) appendix proof absent; (9) interpretability shown on one case only, no user study.

## (h) Reproducibility
Code at https://github.com/NetManAIOps/Chain-of-Event: HTTP 200 checked 2026-10-07, last push 2024-05-06, contents graph/, util/, conf/, requirements; README is minimal; no license file; no data. Data is proprietary. I did not run the code.

## (i) Head-to-head with our work
CoE is stronger where we are weakest: it learns weights from real incidents, reports real-incident accuracy and gives a concrete explanation (weights, per-hop contributions). It is weaker on openness of data, on the label requirement, and it does not forecast. Our edge probabilities (mostly the prior) are far less informative than CoE's learned weights, and the Table 4 gains (learning R_s moves Service top-1 from 51.2% to 79.3%) show what a good estimator can add. Our event-level variant idea (service, signal, direction) is close to CoE's event definition, so it cannot be presented as new.

## (j) Does it change our problem? Could a reviewer say it exists?
No change to the forecasting or label-free gap. A reviewer could say "learned event-level propagation weights exist (CoE)". We must state: CoE is supervised; ours estimates propagation without incident labels. We must also show our weights carry information (they currently do not, 82% at the prior on synthetic data).

## (k) Sentences
Safe: "Chain-of-Event (Yao et al. 2024) learns event-pair causal weights from labelled historical incidents and reports 79.3% top-1 on a proprietary service-incident dataset." / "Its authors name unsupervised or active learning as future work." / "Its code is public; its data are not." Must NOT write: that CoE is label-free or unsupervised; that CoE computes the exact probability one event triggers another; that CoE forecasts failures; that CoE beats human experts in general (one manual graph, one dataset); any comparison implying our method outperforms CoE.

## (l) Things to verify
Appendix A / longer version for the proof; event-extraction details; whether the code runs on a public dataset; the FSE Companion track and Scopus status; whether 170/782 are train+test or test only (the text reads as totals).
