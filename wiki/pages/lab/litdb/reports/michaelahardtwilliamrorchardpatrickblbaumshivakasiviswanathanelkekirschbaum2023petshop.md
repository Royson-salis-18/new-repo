# Report: Hardt et al. (2023/2024), PetShop dataset

Key `michaelahardt...2023petshop`. Note: `litdb/papers/` same key. Coverage: full text read (22 pages); Figs 5-6 and Appendix A not inspected.

## (a) Bibliographic block
Michaela Hardt, William R. Orchard, Patrick Blöbaum, Elke Kirschbaum, Shiva Prasad Kasiviswanathan. PMLR vol. 236 (CLeaR 2024), pp.1-21; arXiv 2311.04806. Peer reviewed per header. Scopus: unverified. SJR unknown.

## (b) Plain-language summary
A public benchmark of 68 injected slowdowns and availability drops in an AWS pet-adoption demo, with the service map and a harness to score root-cause methods.

## (c) Problem and motivation
No standard dataset for microservice RCA, so every group builds its own (p.1).

## (d) Method
Injection of latency, overload, memory-leak, CPU-hog and misconfiguration issues at five nodes under three traffic scenarios; service map from X-Ray; one ground-truth node per issue (pp.5-10).

## (e) Datasets, protocol
68 issues (36 latency, 32 availability), each repeated twice; train/test split by originating microservice; top-1 and top-3 recall at PetSite (pp.5, 10).

## (f) Results (copied)
Top-3 recall (Table 3 p.12): traversal 0.57 to 1.00; CIRCA 0.00 to 1.00 (0.00 on high-traffic availability); counterfactual 0.00 to 0.86; epsilon-diagnosis 0.00 to 0.33; RCD 0.00 to 0.75; correlation 0.57 to 0.92. Top-1: correlation best in most cells, e.g. 0.83 on high-traffic availability vs traversal 0.33 (Table 8 p.22). All methods fabricate root causes on normal data (p.12).

## (g) Limitations and stern critique
Artificial traffic; fault injection tuned to strong effects; single root cause; target is a graph leaf; 8 to 14 issues per cell with no intervals; untuned default methods; authors note feedback loops and cycles are absent.

## (h) Reproducibility
Dataset and code stated at github.com/amazon-science/petshop-root-cause-analysis (not checked, not downloaded).

## (i) Head-to-head with our work
Public benchmark with a supplied service graph, 5-minute metrics; ranked correlation is a strong baseline we must include.

## (j) Does it change our problem? Could a reviewer say it exists?
No. It supports adding NSigma/correlation baselines and reporting false alarms on normal data.

## (k) Sentences
Safe: "On the 68-issue PetShop benchmark, ranked correlation was competitive with or better than methods that learn graphs or structural models from small samples [PetShop]." Must NOT write: that causal methods are generally inferior (the paper's methods were untuned).

## (l) Things to verify
Licence and repo contents; whether to add PetShop to our evaluation set (needs permission to download).
