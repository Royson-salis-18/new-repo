---
key: buldyrev2010cascade
title: "Catastrophic cascade of failures in interdependent networks"
authors: "Sergey V. Buldyrev; Roni Parshani; Gerald Paul; H. Eugene Stanley; Shlomo Havlin"
year: 2010
venue: "Nature 464, April 2010 (Crossref: DOI 10.1038/nature08932, 3,976 citations); text read is arXiv 0907.1182v1 (7 Jul 2009)"
publisher: "Springer Nature (arXiv version read)"
doc_type: journal-article
doi: "10.1038/nature08932"
issn: "0028-0836; 1476-4687 (Crossref)"
scopus_indexing: "unverified: ISSN 0028-0836 not checked in the Scopus preview"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (Nature); arXiv v1 read"
cited_by_crossref: "3976 (Crossref, 2026-10-08)"
n_references: "about 25"
license: ""
batch: "12"
read_status: reviewed                  # full text read to the ER-network solution; scale-free and simulation sections skimmed; figures not inspected
pages: 8
text_chars: 29224
metadata_source: crossref+arxiv
task: "theory of cascading failure in two interdependent random networks (percolation)"
supervision: "n/a"
online_or_streaming: "n/a"
telemetry: "none"
propagation_modeling: "analytic percolation cascade between two networks with one-to-one dependency; random node removal"
forecasts_future_failures: "no (critical threshold analysis)"
llm_used: "no"
systems_evaluated: "model networks (Erdos-Renyi, scale-free); no real systems in the version read"
datasets: "none"
dataset_open: "n/a"
code_open: "n/a"
baselines_compared: "single-network percolation"
metrics: "critical fraction p_c; mutual giant component size"
headline_result: "two interdependent ER networks collapse below mean degree 2.445 (vs 1 for a single ER network); broader degree distributions make interdependent networks more vulnerable to random failure (abstract p.1)"
evidence_quality: "analytic (theory)"
relevance_to_us: "2"
overlap_with_us: "analogy only (cascade mechanics)"
threat_level_for_novelty: "low"
---

# Buldyrev et al.: Catastrophic cascade of failures in interdependent networks

> Notes from the **full text** of the arXiv v1 (8 pages). Page numbers are PDF pages. Figures not inspected; the scale-free results were read in the abstract and the introduction only.

## 1. Summary
Two networks A and B, each node of A depending on a node of B and vice versa; a fraction of nodes is removed from A, nodes lose function when they leave the giant component of their own network or lose their partner, and the process iterates. Generating-function analysis gives the critical fraction and the size of the mutual giant component. For two ER networks the critical mean degree is 2.445; broad degree distributions raise vulnerability.

## 2. Problem and motivation
- Real systems (power and communication networks) are coupled; single-network robustness results may mislead (p.1). Argued conceptually.

## 3. Method (pp.2-3)
- Percolation cascade with alternating stages A1, B2, A3 ...; recursive relations for p_n (Eq. 13), mutual giant component by the intersection of x = p P_A(p P_B(x)); ER closed form in Section IV.

## 4. Data and experimental setup
- Analytic with random node removal; assumptions: independent random networks, one-to-one dependence, no load redistribution, no time dynamics (pp.1-2).

## 5. Results
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Critical mean degree, two ER networks | 2.445 | 1 (single ER network) | single-network percolation | abstract p.1 |
| Effect of broader degree distribution | more vulnerable (interdependent) | more robust (single) | single network | abstract p.1 |

## 6. Limitations
- Stated: simplifying assumptions (p.2).
- **My critique (for our use):**
  1. Cascade here is structural (loss of connectivity), not dynamic load or latency propagation; it cannot be mapped to microservice anomaly spreading without extra assumptions.
  2. Dependencies are one-to-one and symmetric; microservice dependencies are directed, many-to-many and mediated by retries and timeouts.
  3. No empirical validation against real systems in the version read.
- Not discussed: partial dependency, time delays, recovery, intervention.

## 7. Reproducibility
- Analytic; equations given.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | n/a | none | n/a |
| Live / streaming | n/a | incremental | n/a |
| Telemetry used | none | traces | n/a |
| Propagation modelling | percolation theory | noisy-OR edge probabilities | different model class |
| Forecasting | threshold analysis | claimed | n/a |
| Explanation | n/a | templates | n/a |
| Evaluation rigor | theory | synthetic | n/a |
| Open / reproducible | n/a | yes | n/a |

- **What they have that we do not:** a formal result that interdependence lowers resilience (critical degree 2.445).
- **What we have that they do not:** application to measured traces.
- **Could a reviewer say "this already exists"?** No.
- **Position:** cite only as general background on cascading failures in coupled systems, with the caveat that the model is structural and not calibrated to microservices.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- No.

## 10. Citation-ready facts (each with page)
- "In a model of two interdependent random networks, a cascade triggered by removing a small fraction of nodes can fragment both networks; the critical mean degree is 2.445 for ER networks (abstract p.1)."

## 11. Open questions / things to verify
- Published Nature version differences; Scopus status of ISSN 0028-0836; whether our noisy-OR model should be compared with percolation or independent-cascade (Kempe 2003) as theory.
