---
key: sheriffadepoju2023cascading
title: "Cascading Failure Modes in Model-as-a-Service Architectures: When Your Dependencies Think"
authors: "Adepoju, Sheriff (Prairie View A&M University, Texas, USA)"
year: 2023
venue: "International Journal of Scientific Research in Civil Engineering (IJSRCSE), Vol. 7, Issue 6, pp.109-120"
publisher: "Technoscience Academy"
doc_type: journal-article
doi: "10.32628/IJSRCE237530"
issn: "2456-6667"
scopus_indexing: "not found (ISSN 2456-6667 returned 0 results in the Scopus Sources preview, 2026-10-07; the preview lists active titles, so discontinued status cannot be excluded)"
scopus_match: "ISSN 2456-6667, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied; venue not found in Scopus preview"
peer_reviewed: "unclear (journal article; accepted 1 Dec 2023, published 15 Dec 2023; review process not described)"
cited_by_crossref: ""
n_references: "23"
license: "CC BY-NC"
batch: "6"
read_status: reviewed                  # Figure 1 (resilience strategies diagram) not inspected; Tables 1-2 read
pages: 12
text_chars: 38344
metadata_source: crossref
task: "conceptual essay on cascading failures in ML-dependent service architectures (no method or evaluation)"
supervision: "n/a"
online_or_streaming: "n/a"
telemetry: "none (conceptual)"
propagation_modeling: "none (taxonomy of cascade types, Table 1)"
forecasts_future_failures: "no (calls for formal probabilistic propagation models as future research)"
llm_used: "no (machine-learning model services)"
systems_evaluated: "none"
datasets: "none"
dataset_open: "n/a"
code_open: "n/a"
baselines_compared: "none"
metrics: "none"
headline_result: "none (taxonomy of five cascade types and resilience patterns: circuit breakers, fallbacks, graceful degradation)"
evidence_quality: "1"
relevance_to_us: "2"
overlap_with_us: "none (concept of silent decision-quality failures only)"
threat_level_for_novelty: "low"
---

# Cascading Failure Modes in Model-as-a-Service Architectures: When Your Dependencies Think

> Reading notes written from the **full text** (`litdb/texts/sheriffadepoju2023cascading.txt`). Page numbers are PDF pages (journal pp.109-120).
> Figure 1 not inspected.

## 1. One-paragraph summary
A conceptual article argues that when machine-learning models are runtime service dependencies (Model-as-a-Service), failures can propagate "silently" as degraded decision quality rather than errors. It lists cascade types (decision, data, infrastructure, orchestration, cross-layer), re-describes circuit breakers, fallbacks and graceful degradation for ML dependencies, and lists research challenges. It reports no data, experiments or measurements.

## 2. Problem and motivation
- Problem: ML-dependent services introduce silent failure modes beyond service unavailability (pp.1-4).
- Motivation: conceptual; supported by general cascading-failure theory and a few citations on microservice and IoT cascades (Kim and Lee 2018, Zuccaro et al. 2018, Xing 2020, Zhou et al. 2018).
- Real? The notion that ML services can fail silently is plausible, but the paper gives no measured evidence, incidents or data.

## 3. Method
- None. Table 1 (p.5) lists five failure types (decision-centric, data-induced, infrastructure, orchestration, cross-layer) with mechanisms and example impacts; Sec. on circuit breakers, fallbacks (static and dynamic) and graceful degradation (pp.5-7); security, privacy and policy cascades (p.8); challenges and research directions (Table 2, pp.9-10).

## 4. Data and experimental setup
- None.

## 5. Results
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| none reported | n/a | n/a | n/a | n/a |

- The conclusion claims the study "systematically evaluated the dynamics of failure" (p.10) although no method of evaluation is described.

## 6. Limitations
- Stated: difficulty of resilience testing for non-deterministic ML systems; lack of metrics for decision quality (pp.9-10).
- **My critique:**
  1. Conceptual article, no evidence, no case study, no data; "systematically evaluated" is unsupported.
  2. Venue mismatch and credibility: the paper appears in the International Journal of Scientific Research in Civil Engineering; the ISSN is not found in the Scopus Sources preview; acceptance to publication took two weeks.
  3. Reference list quality: references exist in Crossref but several are unrelated to the topic (a chapter on deep learning in computational chemistry [4], the proceedings of an international congress on circumpolar health [5], a naval ship architecture paper [15], an automotive E/E architecture paper [22], a Greek thesis [3]); others are from the same publisher family as Podduturi (2025, batch 5), e.g., IJETCSIT ISSN 3050-9246 [10].
  4. Language shows traces of automated paraphrasing in places (e.g., headings "4.3 Cascades 4.3 Infrastructure and Orchestration Cascades", unusual phrases such as "Intelligence-psychic monitoring schemes", "Cascading failure cross- usually interfering simulating"). This is an observation on text quality only.
  5. Key claims (silent decision-quality failures, circuit breakers on output distributions) are asserted, not tested.
- Not discussed: any quantitative measurement of propagation or detection.

## 7. Reproducibility
- Nothing to reproduce. DOI printed on p.1 is 10.32628/IJSRCE237530 (not re-checked in Crossref in this session beyond metadata from the queue).

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | n/a | label-free | n/a |
| Live / streaming | n/a | incremental windows | n/a |
| Telemetry used | none | traces (+ metrics) | n/a |
| Propagation modelling | taxonomy only | edge probabilities | Ours is implemented |
| Forecasts future failures | calls for it | claimed, untested | Neither |
| Explanation | n/a | templates | n/a |
| Evaluation rigor | none | synthetic only | Ours, slightly |
| Open / reproducible | n/a | yes | Ours |

- **What they have that we do not:** a vocabulary for decision-quality ("silent") failures in ML-dependent services.
- **What we have that they do not:** an implementation.
- **Could a reviewer say "this already exists"?** No.
- **Position:** do not cite as evidence for cascading failure prediction; at most to note that ML dependencies add silent failure modes (as a conceptual claim).
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- No. It is not evidence that cascade prediction is real or under-explored: it has no data and a weak publication venue. The earlier REVIEW_REPORT already flagged it as weak evidence.

## 10. Citation-ready facts (each with page)
- A conceptual article classifies cascades in ML-dependent service architectures into decision, data, infrastructure, orchestration and cross-layer types (Table 1, p.5).
- It argues circuit breakers for ML dependencies should consider output distributions and decision fidelity, not only timeouts and errors (pp.5-6).
- (Not recommended for citation as evidence.)

## 11. Open questions / things to verify
- Whether the venue has been discontinued or is indexed under another ISSN; Figure 1.
