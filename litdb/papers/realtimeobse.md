---
key: realtimeobse
title: ""
authors: ""
year: 
venue: ""
publisher: ""
doc_type: 
doi: ""
issn: ""
scopus_indexing: "unknown (no list in litdb/reference/)"          # from litdb/reference lists only; "unknown" until a list is added
scopus_match: ""
sjr_quartile: ""
peer_reviewed: ""                      # yes / no / preprint
cited_by_crossref: ""
n_references: ""
license: ""
batch: "2"
read_status: extracted                 # extracted -> read-in-full -> reviewed
pages: 29
text_chars: 156848
metadata_source: none
# ---- classification (fill after reading) ----
task: ""                               # detection | localization | cascade-forecast | explanation | benchmark | survey | ...
supervision: ""                        # label-free | label-light | supervised | rule-based
online_or_streaming: ""                # yes / no / partly
telemetry: ""                          # metrics, logs, traces, events, profiling
propagation_modeling: ""               # none | call-graph walk | causal discovery | learned weights | simulation | GNN
forecasts_future_failures: ""          # yes / no
llm_used: ""                           # yes / no (role)
systems_evaluated: ""
datasets: ""
dataset_open: ""                       # yes / no / partly (link)
code_open: ""                          # yes / no (link)
baselines_compared: ""
metrics: ""
headline_result: ""                    # exact numbers + page
evidence_quality: ""                   # 1-5 (1 = weak/unverifiable, 5 = rigorous, open, multi-system)
relevance_to_us: ""                    # 1-5
overlap_with_us: ""                    # none | partial | high
threat_level_for_novelty: ""           # low | medium | high
---

# 

> Reading notes written from the **full text** (`litdb/texts/realtimeobse.txt`). Page numbers refer to the PDF page markers.
> Numbers must be copied from the paper with a page reference. If I could not verify something, it says so.

## 1. One-paragraph summary
_(what they did, in plain language)_

## 2. Problem and motivation (their words, paraphrased)
- Problem statement:
- Why they say it matters (evidence offered? incident data? industrial numbers?):
- Is the problem **real**? (evidence quality for the motivation, p.)

## 3. Method
- Pipeline step by step (inputs → detection → graph/propagation → ranking/prediction → output):
- Key equations / algorithms (summarized, with page):
- Hyper-parameters and how they were chosen:
- Assumptions the method needs (labels, topology, instrumentation, history length):

## 4. Data and experimental setup
- Systems / applications:
- Fault or failure types and how they were injected / collected:
- Dataset size, number of cases, time span, source (public/proprietary):
- Train / validation / test protocol and any possibility of leakage:
- Hardware and runtime:

## 5. Results (copy numbers exactly, with page and table/figure)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|

- Statistical testing (yes/no, which test, n):
- Ablations and what they show:
- Efficiency / overhead:

## 6. Limitations
- Stated by the authors (p.):
- **My critique** (what a stern reviewer would say):
- Threats to validity they did not discuss:

## 7. Reproducibility
- Code / data availability (links, verified?):
- What is missing to reproduce:

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | | label-free calibration on a baseline window | |
| Live / streaming | | incremental windows; offline-evaluated so far | |
| Telemetry used | | traces (+ optional Prometheus/Loki, SSH docker metrics) | |
| Propagation modelling | | edge probabilities (mostly prior, see report T4) | |
| Forecasts future failures | | risk score, untested vs structural baseline | |
| Explanation | | template text; LLM layer not built | |
| Evaluation rigor | | synthetic only so far | |
| Open / reproducible | | yes | |

- **What they have that we do not:**
- **What we have that they do not:**
- **Could a reviewer say "this already exists" because of this paper?** (yes/no + why):
- **How we must position against it** (one sentence we can safely write):
- **Must we run it as a baseline?** (yes/no; code available?):

## 9. Does this paper change what problem we should solve?
- Evidence this paper gives that the problem is real or already solved:
- Evidence it gives that our assumed gap is not a gap:

## 10. Citation-ready facts (each with page)
-
-

## 11. Open questions / things to verify
-
