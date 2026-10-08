# Report: Buldyrev et al. (2010), Catastrophic cascade of failures in interdependent networks

Key `buldyrev2010cascade`. Note: `litdb/papers/` same key. Coverage: arXiv v1 (8 pages) read to the ER solution; scale-free section skimmed; figures not inspected.

## (a) Bibliographic block
Sergey V. Buldyrev, Roni Parshani, Gerald Paul, H. Eugene Stanley, Shlomo Havlin. Nature 464 (2010), DOI 10.1038/nature08932 (Crossref: ISSN 0028-0836, 3,976 citations); arXiv 0907.1182v1 read. Peer reviewed (Nature). Scopus: unverified. SJR unknown.

## (b) Plain-language summary
When two networks depend on each other node by node, removing a few nodes can trigger back-and-forth failures that collapse both. Such coupled networks are more fragile, especially when some nodes have many connections.

## (c) Problem and motivation
Real systems are interdependent; single-network results may mislead (p.1).

## (d) Method
Percolation cascade with generating functions; recursion for mutual giant component; closed form for ER networks (pp.2-4).

## (e) Datasets, protocol
Model networks only; random node removal; one-to-one dependencies (pp.1-2).

## (f) Results (copied)
Critical mean degree 2.445 for two interdependent ER networks (1 for a single ER network); broader degree distributions increase vulnerability (abstract p.1).

## (g) Limitations and stern critique
Structural, not dynamic, cascade; one-to-one dependency; no real data in this version; not calibrated to microservices.

## (h) Reproducibility
Equations given (analytic).

## (i) Head-to-head with our work
Background theory for cascades; our model is a noisy-OR (independent-cascade style) edge model on measured traces.

## (j) Does it change our problem? Could a reviewer say it exists?
No.

## (k) Sentences
Safe: "In coupled random networks with one-to-one dependencies, a small initial failure can fragment both networks (critical mean degree 2.445 for ER) [Buldyrev et al.]." Must NOT write: that the result describes microservice failure propagation.

## (l) Things to verify
Nature version; Scopus status of ISSN 0028-0836.
