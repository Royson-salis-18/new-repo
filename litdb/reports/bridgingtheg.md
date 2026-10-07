# Report: Maheshkar (2025), Bridging the Gap: Agentic AI Root Cause Analysis in Hybrid Distributed Systems (AURORA)

Key `bridgingtheg`. Note: `litdb/papers/bridgingtheg.md`. Page numbers are PDF pages (18 pages; printed pp.228-245).
Coverage: full text read to the end including references. Figs 1-4 not inspected; Tables 1-6 read as text.

## (a) Bibliographic block
Jaykumar Ambadas Maheshkar (U.S. Bancorp per the PDF header). Header venue "Acta Sci., 26(1), 2025, pp.228-245", ISSN 2178-7727. No DOI. Scopus preview: that ISSN is Acta Scientiae (science and mathematics education; CiteScore 1.0, SJR 0.243), not a computing venue; I could not find the article in Crossref under it. Publication in that venue: unverified. SJR quartile unknown (no list supplied). Peer review unverified.

## (b) Plain-language summary
A single-author paper proposing AURORA, a team of AI agents run by a language-model supervisor that collects telemetry, builds causal graphs, ranks root causes and suggests fixes. It claims better top-5 recall than three baselines on a demo shop and a 91% cut in repair time at a 247-service production system.

## (c) Problem and motivation
RCA in hybrid cloud/on-premise systems: alert fatigue, dependency complexity, dynamic change, knowledge silos (p.2). Support: a second-hand "up to three hours" statement and unsourced resilience-pattern percentages. No own measurement.

## (d) Method
Seven agents under a LangChain ReAct supervisor. Causal layer: hierarchical RCD (partition size starting at sqrt(n)), neural Granger causality, weighted edge voting across metrics, logs and traces. Localization: personalized PageRank, random walk, betweenness, Bayesian posterior. Remediation via Kubernetes with human approval; reinforcement-learning "learning agent". Theorems 1-3 (sample complexity O(n^2 log n), identifiability, fusion error bound) are sketched, not proved (pp.5-6).

## (e) Datasets, protocol
Sock-Shop (15), Train Ticket (41), Online Boutique (11), synthetic 100-1000 services; "almost 500" scenarios (60% single, 15% cascading, 10% multi-root, 10% Byzantine, 5% novel). Generation and labelling not described; paired t-test used 50 scenarios (p.10). Production: 247 services, six-month rollout. No data released.

## (f) Results (copied)
Sock-Shop Table 2 (p.10): Top-1/3/5/MRR AURORA 71.2/91.3/94.3/0.798 (CI 93.1-95.5); RUN 61.1/84.5/91.0/0.719; RCD 58.3/81.2/89.0/0.691; PC 52.4/78.1/86.2/0.641; rule-based 34.2/61.3/73.1/0.482. Times (Table 2): AURORA 156 s, RUN 95 s, RCD 142 s, PC 1,247 s, rule-based 1.5 s. Table 3 (p.11): Sock-Shop AURORA 1.8 s, RUN 3.1 s, RCD 4.2 s, PC 28 s; 1000 synthetic services AURORA 892 s vs RUN 5,812 s. Ablation Table 4: no LLM reasoning 87.2% top-5. ECE 0.043 vs RUN 0.089, RCD 0.156. Failure types Table 5 (p.12): single 97.2%, cascading 83.4%, multi-root 78.1%, Byzantine 71.5%, novel 67.3%. Production (p.13): MTTR 47 to 4.3 min, false positives 5.2%, $1.2M savings, ROI 74x.

## (g) Limitations and stern critique
1. Table 2 and Table 3 give incompatible Sock-Shop times (156 s vs 1.8 s for AURORA; PC 1,247 s vs 28 s).
2. The top-5 CI width implies roughly 1,400+ cases; the stated test used 50 scenarios (CI would be about +/-6 points), and 94.3% is not a possible fraction of 50 or 500 (94.2%/94.4% at 500).
3. p-values and effect sizes differ between abstract and final assessment (p<0.01 vs p<0.001; d 0.85 vs 0.73).
4. Theorems unproved; Theorem 3 does not follow from edge voting in general; stated complexity O(n^2 log n) vs an empirical O(n log^2 n) remark.
5. Large-scale evaluation synthetic; scenario generation undocumented; no benchmark data or scripts in the repository's top level.
6. Production case unverifiable (organization, MTTR definition, baselines, savings); ROI divides claimed savings by costs including about $150/month API cost.
7. Learned/supervised parts (fusion weights, RL agent, 100 historical episodes) conflict with any label-free framing.
8. ISSN printed belongs to an education journal; the README of the code repo calls the work an "arXiv preprint".
9. References: blogs and vendor pages; entries [34]-[39] are unrelated trading/network-security items by one other author, [36] missing; repeated verbatim warning sentences show unedited text.
10. Baselines' numbers "match published" values rather than being rerun on identical scenarios.

## (h) Reproducibility
Repo https://github.com/jay-gatech/agenticai-rca-langchain exists (checked via GitHub API 2026-10-07; MIT; last push 2025-11-04; aurora/, deployment/, scripts/, docker-compose.yml). No evaluation data or benchmark scripts seen. Not run (needs an LLM API, and no downloads without permission).

## (i) Head-to-head with our work
Richer on paper (LLM layer, Granger, remediation); our work is label-free, open and honestly evaluated. Neither reports a verified propagation advantage. The paper's own taxonomy shows cascades as harder (83.4% vs 97.2%), but unsupported.

## (j) Does it change our problem? Could a reviewer say it exists?
No change. "LLM agent plus causal discovery RCA" exists in several forms; this paper's evidence is too unreliable to count as prior-art performance.

## (k) Sentences
Safe: none recommended as evidence. If needed: "An LLM multi-agent RCA design combining causal discovery and ReAct reasoning has been proposed [bridgingtheg]" (state that results are unverified). Must NOT write: any figure from Tables 2-5 or the production case as established; that it is published in a Scopus-indexed computing venue; that its theorems are proved.

## (l) Things to verify
Actual publication venue and DOI; relation to SSRN 6003914; Figs 1-4; repository contents beyond the top level.
