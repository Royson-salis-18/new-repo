---
key: motter2002
title: "Cascade-based attacks on complex networks"
authors: "Adilson E. Motter; Ying-Cheng Lai"
year: 2002
venue: "Physical Review E 66, 065102(R) (20 Dec 2002; Crossref: 1,572 citations); text read is arXiv cond-mat/0301086v1"
publisher: "American Physical Society (arXiv version read)"
doc_type: journal-article
doi: "10.1103/physreve.66.065102"
issn: "1063-651X; 1095-3787 (Crossref)"
scopus_indexing: "unverified: ISSN 1063-651X not checked in the Scopus preview"
scopus_match: ""
sjr_quartile: "unknown: no list supplied"
peer_reviewed: "yes (Phys. Rev. E rapid communication); arXiv copy read"
cited_by_crossref: "1572 (Crossref, 2026-10-08)"
n_references: "about 32"
license: ""
batch: "13"
read_status: reviewed                  # full text read (4 pages); figures seen only via captions
pages: 4
text_chars: 0
metadata_source: crossref+arxiv
task: "load-redistribution cascade model on complex networks"
supervision: "n/a"
online_or_streaming: "n/a"
telemetry: "none"
propagation_modeling: "overload cascade: load = number of shortest paths through a node; capacity C_j = (1+alpha) L_j; failed nodes redistribute load"
forecasts_future_failures: "no"
llm_used: "no"
systems_evaluated: "scale-free model networks (N about 5000), homogeneous networks, Internet at AS level (N=6474), western US power grid (N=4941)"
datasets: "published network graphs [30, 31]"
dataset_open: "n/a"
code_open: "n/a"
baselines_compared: "random vs degree-based vs load-based trigger"
metrics: "relative size G of largest connected component after cascade"
headline_result: "load-based attack on one node at alpha 0.2 in scale-free networks affects more than 60% of nodes (more than 3000 of 5000) (p.2)"
evidence_quality: "simulation (theory)"
relevance_to_us: "2"
overlap_with_us: "analogy (load-based cascade; our noisy-OR model has no load)"
threat_level_for_novelty: "low"
---

# Motter and Lai: Cascade-based attacks on complex networks

> Notes from the **full text** (4-page rapid communication). Page numbers are PDF pages. Figures seen only via captions.

## 1. Summary
Each node carries a load (number of shortest paths through it) and a capacity proportional to its initial load with tolerance alpha. Removing one high-load node redistributes loads and can overload others, cascading through the network. Heterogeneous networks (scale-free, Internet, US power grid) can lose a large part of their largest connected component after one targeted removal; homogeneous networks resist.

## 2. Problem and motivation
- Static robustness studies ignore flow dynamics; real overloads (for example the 10 August 1996 western US blackout) show cascades (p.1). Cited, not analysed.

## 3. Method (p.1-2)
- Load and capacity definitions; cascades triggered by a single node removed at random, by highest degree, or by highest load; damage G = N'/N (Eq. 3).

## 4. Data and experimental setup (pp.2-3)
- Scale-free networks (gamma 3, N 5000 to 5100, 5 triggers x 10 networks), homogeneous 3-regular, Internet AS level (6474 nodes), western US grid (4941 nodes).

## 5. Results (copied)
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| Scale-free, load-based attack, alpha 0.2 | more than 60% of nodes affected | random trigger: G near 1 | random breakdown | p.2 |
| Scale-free, alpha 1 | largest component shrinks by more than 20% | n/a | n/a | p.2 |
| Homogeneous network, alpha 0.05 | no cascade | n/a | n/a | p.2 |
| Internet AS level | more than 20% of nodes disconnected by one targeted node for alpha up to 0.4 | random: rare cascades for alpha above 0.05 | n/a | p.3 |
| US power grid | largest component under half after one high-load removal even at alpha 1 | n/a | n/a | p.3 |

## 6. Limitations
- Stated: model simplifications (all pairs exchange one unit via shortest paths) (p.1).
- **My critique (for our use):** shortest-path load is a model of flow, not of microservice request traffic; the cascade is overload-driven connectivity loss, not latency or error propagation; averages over 5 triggers per condition; no calibration against real service systems.

## 7. Reproducibility
- Model fully described; networks cited from public sources.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | n/a | none | n/a |
| Live / streaming | n/a | incremental | n/a |
| Telemetry used | none | traces | n/a |
| Propagation modelling | load redistribution | noisy-OR edge probabilities | different class; theirs captures overload |
| Forecasting | no | claimed | n/a |
| Explanation | n/a | templates | n/a |
| Evaluation rigor | simulation | synthetic | n/a |
| Open / reproducible | n/a | yes | n/a |

- **What they have that we do not:** a load-dependent mechanism for cascades (overload).
- **What we have that they do not:** measured microservice traces.
- **Could a reviewer say "this already exists"?** No.
- **Position:** cite as background that cascades depend on load heterogeneity and key nodes; supports a limitation that our noisy-OR model ignores load.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- No; it motivates reporting that our risk score has no load/capacity term.

## 10. Citation-ready facts (each with page)
- "In heterogeneous networks, removing one high-load node can trigger a cascade of overload failures that disconnects more than half of the nodes (p.2)."

## 11. Open questions / things to verify
- Scopus status of ISSN 1063-651X.
