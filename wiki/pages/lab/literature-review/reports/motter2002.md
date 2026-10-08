# Report: Motter and Lai (2002), Cascade-based attacks on complex networks

Key `motter2002`. Note: `litdb/papers/motter2002.md`. Coverage: full 4-page text read; figures via captions only.

## (a) Bibliographic block
Adilson E. Motter, Ying-Cheng Lai. Phys. Rev. E 66, 065102(R), 2002, DOI 10.1103/physreve.66.065102 (Crossref: ISSN 1063-651X, 1,572 citations); arXiv cond-mat/0301086. Peer reviewed. Scopus: unverified. SJR unknown.

## (b) Plain-language summary
Each node can carry a limited load; if one heavily loaded node fails, its load shifts to others, which may overload in turn. A single targeted failure can bring down a large part of networks with a few very busy nodes.

## (c) Problem and motivation
Static robustness results miss the dynamics of flow; the 1996 western US blackout is cited (p.1).

## (d) Method
Load = number of shortest paths through a node; capacity (1+alpha) times initial load; cascade after removing one node; damage G = largest component fraction (pp.1-2).

## (e) Datasets, protocol
Scale-free networks (N about 5000, 5 triggers x 10 networks), homogeneous networks, Internet AS graph (6,474 nodes), western US grid (4,941 nodes) (pp.2-3).

## (f) Results (copied)
Load-based attack at alpha 0.2 affects more than 60% of nodes; random breakdown leaves G near 1; homogeneous networks resist at alpha 0.05; Internet: more than 20% disconnected at alpha up to 0.4; US grid: largest component under half at alpha 1 (pp.2-3).

## (g) Limitations and stern critique
Shortest-path flow model; connectivity loss as damage; few triggers per condition; not calibrated to service systems.

## (h) Reproducibility
Model and sources given.

## (i) Head-to-head with our work
Background for load-driven cascades; our model has no load term.

## (j) Does it change our problem? Could a reviewer say it exists?
No.

## (k) Sentences
Safe: "Cascades of overload failures triggered by one high-load node can disconnect large parts of heterogeneous networks [Motter and Lai]." Must NOT write: that it models microservice request propagation.

## (l) Things to verify
Scopus status of ISSN 1063-651X.
