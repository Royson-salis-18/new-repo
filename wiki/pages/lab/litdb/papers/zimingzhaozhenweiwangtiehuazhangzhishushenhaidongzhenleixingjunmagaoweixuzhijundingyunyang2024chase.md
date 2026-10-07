---
key: zimingzhaozhenweiwangtiehuazhangzhishushenhaidongzhenleixingjunmagaoweixuzhijundingyunyang2024chase
title: "CHASE: A Causal Hypergraph based Framework for Root Cause Analysis in Multimodal Microservice Systems"
authors: "Zhao, Ziming; Wang, Zhenwei; Zhang, Tiehua; Shen, Zhishu; Dong, Hai; Lei, Zhen; Ma, Xingjun; Xu, Gaowei; Ding, Zhijun; Yang, Yun"
year: 2024
venue: "arXiv:2406.19711v2 [cs.LG] (22 Apr 2025); manuscript in IEEE journal LaTeX template (venue not stated)"
publisher: "arXiv"
doc_type: preprint
doi: ""
issn: ""
scopus_indexing: "not indexed (arXiv preprint; no journal reference or DOI in the arXiv record, checked 2026-10-07)"
scopus_match: ""
sjr_quartile: "n/a"
peer_reviewed: "no (preprint; submission status unknown)"
cited_by_crossref: ""
n_references: "36"
license: "arXiv"
batch: "2"
read_status: reviewed                  # Figs 1-4 not inspected visually
pages: 11
text_chars: 59507
metadata_source: arxiv
task: "localization (instance-level, per trace) with node classification"
supervision: "supervised (cross-entropy on root-cause labels, Eq.15; trained on a labelled training split)"
online_or_streaming: "no (offline per trace)"
telemetry: "traces (topology), logs (FastText template embeddings), metrics (time series transformer embedding)"
propagation_modeling: "GNN (HGT) + hypergraph convolution over hyperedges built from call-graph ancestors/descendants (not learned causal edges)"
forecasting_note: "none"
forecasts_future_failures: "no"
llm_used: "no (LLM encoder mentioned only as future work)"
systems_evaluated: "GAIA / MicroSS (10 service instances, log-injected anomalies) and AIOps 2020 challenge environment (hundreds of instances, 68 injected failures over 3 months)"
datasets: "GAIA: 1099 static traces (160 train); AIOps 2020: 68 failures, dynamic traces"
dataset_open: "yes (GAIA https://github.com/CloudWise-OpenSource/GAIA-DataSet and AIOps 2020 https://github.com/NetManAIOps/AIOps-Challenge-2020-Data, both HTTP 200; not downloaded)"
code_open: "unverified (a Google Drive file link, p.2; not downloaded)"
baselines_compared: "PC, GES, CloudRanger, MicroRCA, TrinityRCL, CausalRCA, DiagFusion (descriptions of MicroRCA and CloudRanger on pp.7-8 are inaccurate)"
metrics: "A@1, A@3, Avg@5 (GAIA); Percentage@1/3/5 of anomalous traces flagged (AIOps 2020)"
headline_result: "GAIA A@1 0.6135, A@3 0.8823, Avg@5 0.8276 vs best baseline (TrinityRCL) 0.4503, 0.8244, 0.7651 (Table II, p.8); AIOps 2020 Percentage@1 0.22 vs 0.17"
evidence_quality: "2"
relevance_to_us: "3"
overlap_with_us: "partial"
threat_level_for_novelty: "low"
---

# CHASE: A Causal Hypergraph based Framework for Root Cause Analysis in Multimodal Microservice Systems

> Reading notes written from the **full text** (`litdb/texts/...chase.txt`). Page numbers are PDF pages (11 pages, references to p.11).
> Figs 1-4 (diagrams and sensitivity plots) not inspected. The code link is a Google Drive file, which I did not open.

## 1. One-paragraph summary
CHASE builds, for each trace, a heterogeneous graph of instance, log and metric nodes. Logs go through FastText on templates, metrics through a time-series transformer, instance types through one-hot plus positional encoding. A heterogeneous graph transformer-style attention layer lets each instance aggregate "anomaly information" from its log and metric nodes. Then it builds hyperedges from the trace's call structure (each hyperedge links a node, one of its parents, and all ancestors of that parent; a further hyperedge links a node and its descendants), applies one hypergraph convolution, and classifies each instance as root cause or not with a cross-entropy loss trained on labels. On the GAIA dataset (10 instances) it reports A@1 of 0.6135 vs 0.4503 for the best baseline; on AIOps 2020 it reports a trace-flagging percentage, not localization accuracy.

## 2. Problem and motivation
- Problem: RCA that jointly uses multimodal data, call topology and multi-hop causal flow (pp.1-2).
- Motivation evidence: general statements that engineers are overwhelmed by data sources; no incident statistics. Evidence type: assumed.
- Real? Argued only by novelty claims about prior methods lacking the three properties together.

## 3. Method
- Graph: G(I, M, L, E) per trace; all logs of an instance collapsed to one log node; metric nodes per metric type (Sec. III-A).
- Encoders (Eq.1-2): FastText on log templates; transformer time-series model, last-timestep embedding for metrics; instance one-hot times learnable matrix plus sinusoidal positional encoding (n = 20000).
- Attention (Eq.3-9): per-head key from log/metric nodes, query from the instance, learnable prior scalars phi per modality initialised to 1, softmax over neighbours, weighted sum of value embeddings, update X~ = (1 - gamma) W sigma(X^) + gamma E(I), gamma = 0.5.
- Hypergraph (Eq.10-14, Algorithm 1): hyperedges from ancestors/descendants in the trace DAG, all weights equal (W_H = I); convolution X~(l) = sigma(Dv^-1/2 H De^-1 H^T Dv^-1/2 X~(l-1) Theta); one layer.
- Loss: cross-entropy over instances with ground-truth root cause label (Eq.15). Training supervised.
- Hyper-parameters (p.8): 3 attention layers, 8 heads, LeakyReLU slope 0.3, hidden size 128, one hypergraph layer, gamma 0.5; baselines use their published hyper-parameters; PageRank damping 0.85, 100 iterations, tolerance 0.01.
- Assumptions: labelled traces, call topology per trace, logs and metrics per instance.

## 4. Data and setup
- GAIA / MicroSS: 10 service instances (mobile, log, web, database, Redis); anomalies injected into **logs** (login failure, memory anomalies, access denied, missing files); 1099 static traces; 160 for training, rest for validation and test, following DiagFusion (p.7).
- AIOps 2020: hundreds of instances, 3 months, 68 injected failures of about 5 minutes; dynamic trace topology (p.7).
- Metrics: A@1, A@3, Avg@5 (GAIA). For AIOps 2020, Percentage@n = share of traces in the n minutes after the labelled start that the method flags as anomalous (Eq.18); this is a trace-level detection rate, not root cause accuracy.
- Leakage: random or unspecified split of traces; traces in a failure are highly correlated, and the paper does not state a failure-level split. GAIA uses 160 training traces from a total of 1099.
- Hardware and runtime: not reported.

## 5. Results (copied; Table II, p.8)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| GAIA A@1 | 0.6135 | 0.4503 | TrinityRCL | Table II |
| GAIA A@3 | 0.8823 | 0.8244 | TrinityRCL | Table II |
| GAIA Avg@5 | 0.8276 | 0.7651 | TrinityRCL | Table II |
| AIOps 2020 Percentage@5 / @3 / @1 | 0.15 / 0.16 / 0.22 | 0.12 / 0.14 / 0.17 | TrinityRCL / TrinityRCL, DiagFusion / MicroRCA | Table II |
| Ablation GAIA A@1 / A@3 / Avg@5 | default 0.6135 / 0.8823 / 0.8276; w/o instance embedding 0.5927 / 0.8554 / 0.7852; w/o heterogeneous message passing 0.3845 / 0.5403 / 0.6581; w/o causal hyperedge 0.4679 / 0.8106 / 0.7598 | n/a | n/a | Table III, p.10 |

- The paper's "36.2%" etc. are relative gains (0.6135 vs 0.4503 is +36.2%); absolute A@1 difference is 0.163.
- Statistics: none; single run per configuration, no variance.
- Other baselines on GAIA (A@1): PC 0.2960, GES 0.3003, CloudRanger 0.3290, MicroRCA 0.3421, CausalRCA 0.3652, DiagFusion 0.4121.
- Efficiency: not reported.

## 6. Limitations
- Stated: none beyond future work (spatiotemporal hypergraph, LLM-based encoders) (p.10).
- **My critique:**
  1. Supervised, but the paper does not say so plainly; labels are needed per trace.
  2. GAIA is 10 instances with log-injected faults; chance A@1 is about 0.10 and chance A@3 about 0.30, so the dataset is easy and the margins matter little for realism.
  3. The only "RCA" number on the harder dataset (AIOps 2020) is not RCA: it is the fraction of traces flagged anomalous after a failure begins, 0.15 to 0.22 for CHASE, which is low in absolute terms.
  4. The "causal" hypergraph is built from call-graph ancestry with equal weights; there is no causal discovery or interventional evidence beyond an informal argument (Eq.13).
  5. Baseline descriptions are partly wrong: the MicroRCA bullet text describes gradient-based causal structure learning (that is CausalRCA's method), and CloudRanger is described as an ML model on logs (it is a causal-graph and random-walk method); PC and GES are run with edge weights equal to node out-degree, an unusual configuration; "GSE" appears in the table for GES.
  6. No variance, no significance tests, no repeats, sensitivity and ablation only on one dataset.
  7. Baselines requiring static topology are marked inapplicable on AIOps 2020, leaving two or three baselines.
  8. Code is a Google Drive link, not a repository; not verified.
  9. Preprint in a journal template, venue unknown.
- Not discussed: label leakage between traces of the same failure; cost and latency; real production data.

## 7. Reproducibility
- Code: https://drive.google.com/file/d/11erha3k8FeA67z-sfKGReqHz66PpO6o4/view (from p.2); not opened. Status: unverified.
- Data: GAIA (github.com/CloudWise-OpenSource/GAIA-DataSet, HTTP 200) and AIOps 2020 (github.com/NetManAIOps/AIOps-Challenge-2020-Data, HTTP 200); not downloaded.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | supervised, labelled traces | label-free | Ours lighter |
| Live / streaming | offline per trace | incremental windows | Ours |
| Telemetry used | traces, logs, metrics | traces (+ optional metrics, SSH) | Theirs broader |
| Propagation modelling | hypergraph from call-graph ancestry, equal weights | edge probabilities | Neither shows learned propagation helps on realistic data |
| Forecasts future failures | no | risk score, untested | Neither |
| Explanation | attention weight heatmap (Fig 4) | template text | Slightly theirs |
| Evaluation rigor | 2 public datasets, 7 baselines, no stats; one dataset has only 10 instances | synthetic only | Theirs marginally, but weak |
| Open / reproducible | public datasets; code on Drive | yes | Ours |

- **What they have that we do not:** an end-to-end learned multimodal model with published numbers on two public datasets.
- **What we have that they do not:** label-free operation, a forecasting hypothesis, honest ablations.
- **Could a reviewer say "this already exists"?** Not for our contribution; it is a supervised localizer.
- **Position:** cite among supervised GNN localizers (with DiagFusion, Eadro, DejaVu) that need labels.
- **Must we run it as a baseline?** No (supervised, code unverified, datasets small).

## 9. Does this paper change what problem we should solve?
- No. It adds nothing on forecasting or label-free methods. Its ablation (removing the hyperedge layer drops A@1 from 0.6135 to 0.4679) is one dataset with 10 instances.
- Evidence the problem is real: none.

## 10. Citation-ready facts (each with page)
- CHASE is a supervised heterogeneous-graph and hypergraph model for per-trace instance-level RCA with multimodal data (pp.4-7).
- On GAIA it reports A@1 0.6135 against 0.4503 for TrinityRCL (Table II, p.8).
- The GAIA dataset in that evaluation has 10 service instances (p.7).
- On AIOps 2020 it reports the share of anomalous traces flagged, 0.22 at the one-minute span versus 0.17 (Table II).

## 11. Open questions / things to verify
- The code link; the venue and publication status; the split protocol for traces within failures; Figs 1-4.
