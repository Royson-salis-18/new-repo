---
key: wang2024fewshot
title: "Few-Shot Cross-System Anomaly Trace Classification for Microservice-based systems (arXiv v2); published as 'Cross-System Categorization of Abnormal Traces in Microservice-Based Systems via Meta-Learning'"
authors: "Wang, Yuqing; Mäntylä, Mika V.; Demeyer, Serge; Beyazit, Mutlu; Kisaakye, Joanna; Nyyssölä, Jesse"
year: 2024
venue: "arXiv:2403.18998v2 (31 Mar 2024); published version: Proceedings of the ACM on Software Engineering (FSE 2025), DOI 10.1145/3715742, 19 June 2025"
publisher: "arXiv (preprint read); ACM (published version)"
doc_type: preprint
doi: "10.1145/3715742 (published version; the local PDF is the preprint)"
issn: "2994-970X (PACMSE, from Crossref)"
scopus_indexing: "published venue (PACMSE, ISSN 2994-970X) not found in the Scopus Sources preview (0 results, 2026-10-07); the preprint is not indexed; status of the published paper: unverified"
scopus_match: "ISSN 2994-970X, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "preprint read here: no; the published version is peer reviewed (arXiv comment: 'Accepted at ACM FSE 2025')"
cited_by_crossref: "5 (published version, Crossref 2026-10-07)"
n_references: "about 40"
license: "arXiv"
batch: "4"
read_status: reviewed                  # the preprint version; published version may differ in title, numbers and details; Figs 1-5 not inspected
pages: 12
text_chars: 65577
metadata_source: arxiv + crossref (published version found by search)
task: "classification of already-abnormal traces into fault categories (few-shot, meta-learning); not localization"
supervision: "supervised few-shot (K labelled traces per class in the target tasks) with labelled base categories for meta-training; autoencoder pre-trained on normal traces"
online_or_streaming: "no"
telemetry: "traces (spans) and logs; BERT embeddings of operations and log events"
propagation_modeling: "none"
forecasts_future_failures: "no"
llm_used: "no (BERT base used as an embedding model)"
systems_evaluated: "TrainTicket (30 fault categories) and OnlineBoutique (32 fault categories), from DeepTraLog and Nezha datasets"
datasets: "DeepTraLog (TrainTicket, 14 fault categories) and Nezha (TrainTicket and OnlineBoutique, fault cases per pod)"
dataset_open: "yes (github.com/FudanSELab/DeepTraLog has TraceLogData and GraphData folders; github.com/IntelligentDDS/Nezha has rca_data folders; listings verified via GitHub API, nothing downloaded)"
code_open: "promised 'upon acceptance' (p.11); not verified for the published version"
baselines_compared: "ablation variants only: OnlySpan, Linear-AE, GLU-AE, Linear/RNN/LSTM/CNN meta-learners, ProtoNet, TE-MatchingNet, NearNeighbor, Decision tree"
metrics: "accuracy with 95% CI over 50 meta-test tasks (best of 5 runs per task)"
headline_result: "E1 TrainTicket->TrainTicket 5-shot 92.91, 10-shot 93.26; E2 OB->OB 82.50 and 85.20; E3 OB->TT 86.35 and 92.19; E4 TT->OB 82.37 and 84.77 (Tables II, III, pp.9)"
evidence_quality: "2"
relevance_to_us: "2"
overlap_with_us: "low (supervised trace classification, not RCA or forecasting)"
threat_level_for_novelty: "low"
---

# Few-Shot Cross-System Anomaly Trace Classification for Microservice-based systems

> Reading notes written from the **full text** of the arXiv v2 preprint (`litdb/texts/yuqingwang...cross.txt`). Page numbers are PDF pages (12 pages).
> The published version (PACMSE 2025, DOI 10.1145/3715742) has a different title and may differ in content; I did not read it. Figs 1-5 not inspected.

## 1. One-paragraph summary
The paper classifies abnormal traces into fault categories with few labelled examples. A multi-head attention autoencoder fuses span attributes and BERT-embedded log events into a trace vector (trained on normal traces of each system); a Transformer-encoder meta-learner trained with MAML on "base" fault categories adapts with 5 or 10 labelled traces per class to 5-way tasks drawn from 10 "novel" categories of the same or another system. Reported 10-shot accuracies are 93.26% (TrainTicket) and 85.2% (OnlineBoutique) within system, and 92.19% and 84.77% across systems.

## 2. Problem and motivation
- Problem: classify abnormal traces by fault category with few examples and across systems (pp.1-2).
- Motivation: trace-based AD and RCA are central to AIOps, labelled abnormal traces are imbalanced across fault categories, and systems are heterogeneous (pp.1-2). No incident data. Evidence type: assumed.
- The task is classification given that a trace is abnormal; it does not localize the faulty service.

## 3. Method
- Span vectors: normalized start time, end time, duration, hierarchical span ID, and a BERT-based embedding of "service operation" (WordPiece, average of word embeddings) (Eq.1, p.4). Log event vectors: BERT embedding of severity, component and message without log parsing (p.4).
- MultiHAttenAE (Eq.2-6, pp.4-5): project spans and logs to a common space, multi-head attention with spans as queries and logs as keys and values to produce the trace representation, decoder reconstructs both; MSE loss; trained per system on 3,960 normal traces (3,360 train, 570 validation) (p.6).
- TE-MAML (pp.5-6): Transformer-encoder meta-learner with MAML (first-order approximation), N-way K-shot with N = 5, K = 5 or 10; four meta-training tasks and 50 meta-testing tasks per experiment drawn from C(10,5) = 252 possible 5-subsets of the 10 novel categories (pp.7).
- Hyper-parameters: AdamW; details "in replication package" (p.7); not in the paper.
- Assumptions: labelled abnormal traces for base categories; K labelled traces per class for each new task; normal traces of the target system to train the autoencoder (so cross-system transfer still needs target normal data and target labelled shots).

## 4. Data and setup
- Datasets built from DeepTraLog (TrainTicket, 14 fault categories from fault branches) and Nezha (TrainTicket and OnlineBoutique, faults injected into pods; four injected fault categories per pod, each pod-case treated as its own category) (p.6). Combined: 30 fault categories for TrainTicket (20 base and 10 novel) and 32 for OnlineBoutique (22 base and 10 novel) (p.7).
- Table I (p.7): TrainTicket base categories average 1,117 unique traces per category (min 26, max 2,309); novel average 1,275; OnlineBoutique base 565, novel 320.
- Experiments (p.7): E1 TrainTicket to TrainTicket; E2 OnlineBoutique to OnlineBoutique; E3 OnlineBoutique to TrainTicket; E4 TrainTicket to OnlineBoutique. (The text then says "E1 and E3 are within system experiments while E2 and E4 are cross-system", which contradicts these definitions.)
- Labels: both datasets were labelled automatically by running normal and faulty versions interchangeably, so some labelled-abnormal traces may be normal (p.8).
- Leakage: base and novel categories are random mixes; because each pod-case is a "category", categories from the same injected fault type on neighbouring pods can appear in both base and novel sets and may be near-duplicates; the paper does not analyze this.
- Hardware: 32-core CPU, A100 40 GB (p.7).

## 5. Results (copied; Tables II and III, p.9)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| E1 TT to TT, 5-shot / 10-shot accuracy | 92.91 +/- 2.10 / 93.26 +/- 1.40 | 92.21 +/- 1.73 / 93.07 +/- 1.64 | GLU-AE + TE-MAML | Table II |
| E3 OB to TT, 5-shot / 10-shot | 86.35 +/- 2.00 / 92.19 +/- 1.99 | 85.07 +/- 2.38 / 94.40 +/- 2.19 | GLU-AE + TE-MAML | Table II |
| E2 OB to OB, 5-shot / 10-shot | 82.50 +/- 2.35 / 85.20 +/- 2.33 | 80.61 +/- 2.96 (GLU-AE) / 83.07 +/- 3.29 (CNN-MAML) | see left | Table III |
| E4 TT to OB, 5-shot / 10-shot | 82.37 +/- 2.07 / 84.77 +/- 2.28 | 79.01 +/- 2.63 (CNN-MAML) / 84.08 +/- 2.76 (CNN-MAML) | see left | Table III |
| Span-only ablation | OnlySpan+TE-MAML 80.64 / 78.77 (E1), 72.83 / 73.15 (E2) | n/a | n/a | Tables II, III |
| Adaptation time per task | 0.0460 s (E1, 5-shot) to 0.0977 s | n/a | n/a | Table IV, p.9 |
| Trace construction time per task | 1.84 s (TrainTicket 5-shot), 5.02 s (OnlineBoutique 10-shot) | n/a | n/a | Table V, p.9 |

- Statistical testing: 95% confidence intervals across 50 meta-test tasks (accuracy +/- values); no significance tests between methods.
- Important protocol detail: "each meta-testing task's accuracy" is the best of 5 runs of that task (p.8).
- Many differences between the proposed model and its AE variants are within the reported intervals (e.g., E1 10-shot 93.26 +/- 1.40 vs GLU-AE 93.07 +/- 1.64; E3 10-shot GLU-AE is higher at 94.40).
- Ablation: replacing the Transformer meta-learner or MAML hurts a lot (e.g., Linear-MAML about 45% on TrainTicket).

## 6. Limitations
- Stated (Sec. V, p.10): baselines are authors' own ablation variants; datasets limited; no trace-level metrics; CPU contention vs network delay confusion in OnlineBoutique; 5-way setup due to limited categories.
- **My critique:**
  1. "Best of 5 runs per task" inflates reported accuracy; the justification (label noise) does not license selecting the maximum; mean and variance across runs should be reported.
  2. Cross-system claim is weaker than it sounds: the autoencoder is trained on normal traces from the target system, and each target task supplies K labelled traces per class, so the method needs target normal data plus labelled examples.
  3. Fault "categories" are per pod-case in Nezha; categories can be very similar across base and novel sets, so "novel" may be easy; no check.
  4. Ground truth labels are noisy by the authors' own account.
  5. No comparison with any published trace classification, anomaly or RCA method: baselines are only internal ablations.
  6. The task assumes abnormality is already detected and a trace-level fault category suffices; it does not localize services; the abstract and index terms mention RCA but there is no RCA evaluation.
  7. Text contradicts itself on which experiments are within- and cross-system (p.7).
  8. Code and data to be released "upon acceptance"; hyper-parameters are not in the paper.
  9. The published version has a different title and is presumably revised; results here may not match it.
- Not discussed: time-split protocol, run-to-run variance beyond the 95% CI across tasks.

## 7. Reproducibility
- Datasets: DeepTraLog repo (github.com/FudanSELab/DeepTraLog, folders TraceLogData and GraphData, last push 2026-01-05, no license file) and Nezha repo (github.com/IntelligentDDS/Nezha, MIT, last push 2025-05-20, rca_data for 2022-08-22, 2022-08-23, 2023-01-29, 2023-01-30); listings verified via the GitHub API on 2026-10-07; nothing downloaded; dataset sizes unknown.
- Code: promised after acceptance (p.11); I did not look for the published artifact.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | labelled base categories and K labelled shots per task | label-free | Ours lighter |
| Live / streaming | no | incremental windows | Ours |
| Telemetry used | spans and logs | traces (+ optional metrics, SSH) | Theirs uses logs too |
| Propagation modelling | none | edge probabilities | Ours |
| Forecasts future failures | no | claimed | n/a |
| Explanation | none | templates | Ours |
| Evaluation rigor | two systems, 50 tasks, CIs, but best-of-5 and internal baselines | synthetic only | Theirs has real injected faults; weaker protocol |
| Open / reproducible | datasets public, code pending | yes | Ours (code) |

- **What they have that we do not:** evaluation on real injected-fault traces of two benchmark systems with fault-type categories; datasets that include logs and traces (Nezha).
- **What we have that they do not:** localization and propagation modelling without labels.
- **Could a reviewer say "this already exists"?** No: a different task.
- **Position:** cite as an example of few-shot fault-type classification; not as RCA prior art.
- **Must we run it as a baseline?** No. The Nezha and DeepTraLog datasets are candidates for our evaluation.

## 9. Does this paper change what problem we should solve?
- It indicates demand for cross-system generalization with few labels, consistent with our motivation, but it is a classification setting.
- The REVIEW_REPORT item that DeepTraLog and Nezha datasets were unverified can now be partly resolved: both GitHub repositories list data folders (see section 7).

## 10. Citation-ready facts (each with page)
- A few-shot meta-learning framework classifies abnormal traces into fault categories on TrainTicket and OnlineBoutique and reports 10-shot accuracies of 93.26% and 85.2% within system (Tables II-III, p.9; preprint).
- It assumes labelled shots per task and normal traces of each system for the autoencoder (pp.5-6).
- The accuracy of each meta-test task is the best of five runs (p.8).
- The published version appears in Proceedings of the ACM on Software Engineering, 2025 (DOI 10.1145/3715742).

## 11. Open questions / things to verify
- Read the published version and check whether the best-of-5 protocol and numbers changed.
- Dataset sizes and licenses for Nezha and DeepTraLog (ask the user before downloading).
- Scopus status of PACMSE (not found in the preview; the journal is new).
