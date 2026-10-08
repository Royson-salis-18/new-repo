# Report: Fang et al. (2025), Rethinking the Evaluation of Microservice RCA

Key `fang2025rethinking`. Note: `litdb/papers/` same key. Coverage: full text read (20 pages incl. references); plots (Figs 6-11) not inspected.

## (a) Bibliographic block
Aoyang Fang, Songhan Zhang, Yifan Yang, Haotong Wu, Junjielong Xu, Xuyang Wang, Rui Wang, Manyi Wang, Qisheng Lu, Pinjia He (CUHK Shenzhen). arXiv 2510.04711v2, cs.SE, 23 Dec 2025; ACM template placeholders; literature matrix lists DOI 10.1145/3797100 (unverified). Preprint; not Scopus-indexed. SJR unknown.

## (b) Plain-language summary
A simple rule that counts which service raises the most alerts matches the best RCA models on public datasets. The authors show the datasets are easy, build a harder Train-Ticket dataset, and find 11 recent methods mostly fail on it.

## (c) Problem and motivation
Reported RCA progress may reflect easy benchmarks (pp.1-2).

## (d) Method
Preliminary study with SimpleRCA on 11 datasets (Table 2); dataset diagnostics (Tables 1, 3); benchmark generation pipeline with dynamic workload, 31 fault types, impact-driven validation, hierarchical labels (pp.8-11).

## (e) Datasets, protocol
9,152 injections, 1,430 validated cases, 25 fault types, 4 min normal + 4 min fault, redeploy each time; 11 methods re-implemented; trained methods split 80/20 by fault type (pp.11-12).

## (f) Results (copied)
Existing data: SimpleRCA Top@1 0.93 on Nezha-TT vs Nezha 0.87; 0.83 on RE3-TT and RE3-SS vs BARO 0.50 and 0.00 (Table 2 p.6); 733 of 737 cases lack some telemetry type; 68% of cases have symptoms only in the injected service (Table 3 p.7). New benchmark: mean Top@1 0.21; MicroRCA 0.37, Baro 0.36, MicroDig 0.35, MicroHECL 0.34, SimpleRCA 0.28; SimpleRCA Top@5 0.80 is the highest of all (Table 5 p.14). 84.4% of injections were silent (p.13). Hard cases: modelling bottlenecks 47.4%, scalability 39.8% (Fig 10 p.17).

## (g) Limitations and stern critique
SimpleRCA's Top@5 on the new benchmark exceeds every SOTA method, contradicting the text's reading that simple rules fail; Nezha Top@1 0.04 vs 0.87-0.93 shows re-implementation and tuning sensitivity; two evaluation sets are mixed in one table; one system; SLI-based oracle excludes gray failures; release promised, not shown; template placeholders.

## (h) Reproducibility
Release promised (p.19); not verified.

## (i) Head-to-head with our work
Evaluation guide. Our propagation-aware method must beat SimpleRCA, BARO and MicroRCA on a benchmark where the root cause is not the loudest service.

## (j) Does it change our problem? Could a reviewer say it exists?
It changes our evaluation design: include SimpleRCA, report Top@1 to Top@5 with counts, and use cases with silent or attenuated root symptoms (Type II/III).

## (k) Sentences
Safe: "A rule-based alert counter matched or exceeded state-of-the-art RCA methods on several public benchmarks, which the authors attribute to localized faults and shallow call chains [Fang et al.]." Must NOT write: that the new benchmark proves simple rules fail (its Top@5 says otherwise); any Table 5 value as independently verified.

## (l) Things to verify
Benchmark release; ACM version; whether our baselines reproduce the Table 5 values.
