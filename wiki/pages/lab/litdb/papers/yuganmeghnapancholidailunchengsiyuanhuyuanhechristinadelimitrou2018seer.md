---
key: yuganmeghnapancholidailunchengsiyuanhuyuanhechristinadelimitrou2018seer
title: "Seer: Leveraging Big Data to Navigate The Increasing Complexity of Cloud Debugging"
authors: "Yu Gan; Meghna Pancholi; Dailun Cheng; Siyuan Hu; Yuan He; Christina Delimitrou"
year: 2018
venue: "arXiv preprint 1804.09136v1 (cs.DC, 24 Apr 2018); 7-page short version (the full ASPLOS 2019 Seer paper is a different, longer paper, not read)"
publisher: "arXiv"
doc_type: preprint
doi: "10.48550/arxiv.1804.09136"
issn: ""
scopus_indexing: "arXiv preprints are not Scopus-indexed"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "preprint (the text carries no venue; a workshop origin is likely but unverified)"
cited_by_crossref: ""
n_references: "36"
license: ""
batch: "9"
read_status: reviewed                  # full text (7 pages) read; Figs 1-4 not inspected as plots
pages: 7
text_chars: 0
metadata_source: arxiv
task: "anticipate QoS violations and name the culprit microservice, then adjust resources"
supervision: "supervised (deep network trained offline on traces with manually annotated QoS violations, p.3)"
online_or_streaming: "yes (streaming queue-depth traces every few ms; inference 2-14 ms small cluster, hundreds of ms at 200 instances without TPU)"
telemetry: "RPC-level traces with queue depth per microservice (own Thrift tracing); hardware counters for cause diagnosis"
propagation_modeling: "none explicit: one input and output neuron per microservice; dependencies learned implicitly"
forecasts_future_failures: "yes (QoS violations, horizon not quantified in this version)"
llm_used: "no"
systems_evaluated: "three own end-to-end apps (social network, movie streaming, e-commerce based on Sockshop); 10 x 40-core local cluster and 200 GCE instances"
datasets: "own traces; not released in this text ('plan to open-source' the apps)"
dataset_open: "no (planned)"
code_open: "no"
baselines_compared: "only input-metric variants of the same network (CPU utilization, latency, latency rate, queue depth); no external baseline"
metrics: "QoS-violation detection accuracy, culprit accuracy, inference time"
headline_result: "abstract: anticipates QoS violations 91% of the time and names the culprit in 89% of cases on GCE; local cluster 93% and 91% (p.2)"
evidence_quality: "1"
relevance_to_us: "4"
overlap_with_us: "partial (early warning plus culprit; supervised)"
threat_level_for_novelty: "medium"
---

# Seer (Gan et al., arXiv 2018 short version)

> Notes from the **full text** (7 pages). Page numbers are PDF pages. Plots (Figs 2-4) seen only as axis text; accuracy values come from the prose.

## 1. Summary
A neural network with one input and one output neuron per microservice takes streaming per-microservice queue-depth traces and fires an output when that microservice is about to cause a QoS violation. Once detected, hardware counters identify the contended resource and resources are adjusted (cache partitioning, container resize, bandwidth control). Trained offline on traces with manually annotated QoS violations.

## 2. Problem and motivation
- Detecting QoS violations after the fact is too late; in microservice graphs hiccups propagate quickly (p.1). Argued, no measured incident rate.

## 3. Method
- Queue depth chosen over CPU utilization and latency because the latter gave false positives or the wrong culprit (pp.2-3, Fig 2a plot only).
- Architecture: input neurons = number of active microservices, 5 hidden layers, SGD/ADAGRAD (p.3). Not robust to autoscaling because the network size equals the service count (p.5).
- Inference moved to TPUs for 200-instance scale (p.4).

## 4. Data and experimental setup
- Three own applications of tens of services each; 10 servers of 40 cores and 200 GCE instances (p.3). QoS violation threshold and prediction lead time are not stated here. Train and test traces are described as disjoint "application and system configurations" (p.3).
- Labels: manually supervised annotation of QoS violations (p.3).

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| QoS violation anticipated, local cluster | 93% | n/a | none (internal metric comparison only) | p.2 |
| Culprit correct, local cluster | 91% | n/a | none | p.2 |
| QoS violation anticipated, GCE 200 instances | 91% | n/a | none | abstract, p.2 |
| Culprit correct, GCE | 89% | n/a | none | abstract, p.2 |
| Inference time | 60% of detections within 2 ms; max 14 ms (small cluster) | hundreds of ms without TPU | n/a | p.4 |
- Fig 2a compares input metrics but the values are only in a plot. Fig 4 shows one example of tail latency with and without Seer.

## 6. Limitations
- Stated: not robust to autoscaling; assumes full control of the cluster and instrumented services; some memory-bound violations not predicted early enough (p.5).
- **My critique:**
  1. No external baseline and no definition of how far ahead "anticipates" means; accuracy lacks a false-positive rate or alarm rate.
  2. Supervised with manual labels; the system is bound to a fixed service set and instrumentation.
  3. Apps are the authors' own and unreleased; results are not reproducible.
  4. The headline percentages carry no confidence intervals or counts of violations.
- Not discussed: calibration, cost of false alarms, behaviour on unseen applications.

## 7. Reproducibility
- Apps and code not released in this version. The later ASPLOS 2019 paper was not read.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | manual QoS labels | none | ours |
| Live / streaming | yes | incremental | theirs (deployed in own cluster) |
| Telemetry used | queue depth traces + HW counters | traces (+ metrics) | different |
| Propagation modelling | implicit | explicit edges | ours (explainable) |
| Forecasts future failures | yes (QoS) | claimed, untested | theirs, with caveats |
| Explanation | none | templates | ours |
| Evaluation rigor | none external | synthetic | neither |
| Open / reproducible | no | yes | ours |

- **What they have that we do not:** an end-to-end early warning with culprit naming, evaluated on live clusters.
- **What we have that they do not:** label-free operation, explicit edge model, open code.
- **Could a reviewer say "this already exists"?** Yes for "early warning plus culprit from traces". Our difference is label-free, explicit propagation and calibrated scoring.
- **Position:** cite as the prior art for early QoS-violation prediction with culprit identification (supervised).
- **Must we run it as a baseline?** Not feasible (no code); compare conceptually.

## 9. Does this paper change what problem we should solve?
- Yes in framing: early warning with culprit identification already exists (supervised), so the claim must be about label-free operation and explicit propagation.

## 10. Citation-ready facts (each with page)
- "Seer anticipates QoS violations from per-microservice queue-depth traces and reports 91% detection and 89% culprit accuracy on a 200-instance GCE cluster (authors' own applications)" (p.2).

## 11. Open questions / things to verify
- The ASPLOS 2019 Seer paper (not read); lead time; false-alarm rate.
