# Report: Wang et al. (2024), Few-Shot Cross-System Anomaly Trace Classification (arXiv v2) / PACMSE 2025

Key `yuqingwang...cross`. Note: `litdb/papers/yuqingwang...cross.md`. Page numbers are PDF pages.
Coverage: full text of the arXiv v2 preprint read to the end of the references. The published version (different title) was not read. Figs 1-5 not inspected.

## (a) Bibliographic block
Yuqing Wang, Mika V. Mäntylä, Jesse Nyyssölä (University of Helsinki), Serge Demeyer, Mutlu Beyazit, Joanna Kisaakye (University of Antwerp, Flanders Make). Preprint: arXiv:2403.18998v2, 31 March 2024, title "Few-Shot Cross-System Anomaly Trace Classification for Microservice-based systems". The arXiv record notes "Accepted at ACM FSE 2025" with DOI 10.1145/3715742. Crossref lists the published paper as "Cross-System Categorization of Abnormal Traces in Microservice-Based Systems via Meta-Learning", Proceedings of the ACM on Software Engineering (FSE 2025), ISSN 2994-970X, 19 June 2025, cited by 5. Scopus: the published venue (PACMSE) was not found in the Scopus Sources preview on 2026-10-07 (0 results; the journal is new), so status unverified; the preprint is not indexed. SJR n/a. Peer review: the published version yes; the preprint no. The queue metadata had labelled this an arXiv preprint without DOI; it should be updated to cite the published version after reading it.

## (b) Plain-language summary
Given a trace already known to be abnormal, the system tells which of several fault types caused it, after seeing only five or ten labelled examples of each type. It first learns a compact representation of each system from normal traces, then meta-learns how to adapt quickly to new fault types, including in a different system.

## (c) Problem and motivation
Few-shot classification of abnormal traces across fault categories and systems (pp.1-2), motivated by fault imbalance and heterogeneity. No incident data. Evidence type: assumed. The task is classification, not localization.

## (d) Method
Span vectors (normalized times, hierarchical span ID, BERT embedding of service operation) and log vectors (BERT embedding of log events, no parsing) are fused by a multi-head attention autoencoder trained on normal traces (3,960 traces per system: 3,360 train, 570 validation). A Transformer-encoder classifier is meta-trained with first-order MAML on 5-way tasks from base fault categories (four meta-training tasks) and tested on 50 5-way tasks drawn from 252 possible 5-subsets of 10 novel categories, with 5 or 10 labelled shots per class. Hyper-parameters are deferred to a replication package.

## (e) Datasets, protocol, leakage
DeepTraLog (TrainTicket, 14 fault categories) and Nezha (TrainTicket and OnlineBoutique, faults injected in pods; each pod-case a category) combined into 30 (20 base, 10 novel) and 32 (22 base, 10 novel) categories (p.7). Labels come from automatic labelling by alternating normal and faulty versions, which the authors acknowledge may mislabel some traces (p.8). Base and novel categories are random mixes, so near-duplicate categories (same fault type on neighbouring pods) may cross the base/novel split. The text defines E1 and E2 as within-system and E3 and E4 as cross-system but later states the opposite (p.7).

## (f) Results (copied)
Tables II and III (p.9), accuracy in % with 95% CI over 50 tasks: E1 TrainTicket to TrainTicket 5-shot 92.91 +/- 2.10, 10-shot 93.26 +/- 1.40; E3 OnlineBoutique to TrainTicket 5-shot 86.35 +/- 2.00, 10-shot 92.19 +/- 1.99; E2 OnlineBoutique to OnlineBoutique 5-shot 82.50 +/- 2.35, 10-shot 85.20 +/- 2.33; E4 TrainTicket to OnlineBoutique 5-shot 82.37 +/- 2.07, 10-shot 84.77 +/- 2.28. Span-only variant: 80.64 and 78.77 (E1), 72.83 and 73.15 (E2). Best close competitors: GLU-AE+TE-MAML (E1 10-shot 93.07 +/- 1.64; E3 10-shot 94.40 +/- 2.19, higher than the proposed model), CNN-MAML (E2 10-shot 83.07 +/- 3.29; E4 10-shot 84.08 +/- 2.76). Times (Tables IV, V): adaptation 0.046 to 0.098 s per task; trace construction 1.84 to 5.02 s per task. Each task's reported accuracy is the best of five runs (p.8).

## (g) Limitations and stern critique
Authors: baselines are their own variants; limited datasets; trace-related metrics not used; confusion of CPU contention and network delay (pp.8, 10). Mine: best-of-five per task inflates results; the cross-system claim still requires target-system normal traces and labelled shots; pod-case categories may leak between base and novel sets; labels are noisy; no published competitor; many differences lie within CIs and one close variant is higher in E3 10-shot; the task is classification not RCA; internal contradiction about E1 to E4 labels; code only promised; published version differs.

## (h) Reproducibility
Datasets: github.com/FudanSELab/DeepTraLog (folders TraceLogData, GraphData) and github.com/IntelligentDDS/Nezha (MIT; rca_data folders for four dates) exist; I verified the listings through the GitHub API and downloaded nothing. Code and hyper-parameters: promised, not seen.

## (i) Head-to-head with our work
Different task (fault-type classification with labels). It shows interest in cross-system transfer with few labels, but not label-free localization or forecasting. Its datasets are candidates for our evaluation because they carry logs and traces with injected faults.

## (j) Does it change our problem? Could a reviewer say it exists?
No. A reviewer would not consider it prior art for our contribution. It resolves part of the earlier worry about dataset hosting for DeepTraLog and Nezha.

## (k) Sentences
Safe: "Wang et al. address few-shot classification of abnormal traces by fault category with a meta-learning framework evaluated on TrainTicket and OnlineBoutique [key]." / "Their cross-system setting still uses normal traces and labelled examples from the target system [key]." Must NOT write: that it localizes root-cause services; that it works without labels; the accuracy figures without noting best-of-five and the preprint status; that the preprint equals the published version.

## (l) Things to verify
Read the published PACMSE version; dataset sizes; whether code was released; Scopus status of PACMSE.
