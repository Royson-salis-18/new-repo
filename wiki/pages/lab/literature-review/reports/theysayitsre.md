# Report: Vangapelli (2026), AI-Driven Root Cause Analysis In Real-Time Distributed Systems

Key `theysayitsre`. Note: `litdb/papers/theysayitsre.md`. Page numbers are PDF pages.
Coverage: full text (8 pages) read to the end including references. The queue key was formed from the first words of the abstract.

## (a) Bibliographic block
Santhosh Vangapelli (independent researcher, USA, ORCID in header). International Journal of Artificial Intelligence and Machine Learning (Svedberg Open), Vol. 6, No. 7s, 2026, pp.202-209. DOI printed in the footer: https://doi.org/10.48084/etasr.XXXXX (placeholder, an ETASR-style prefix with XXXXX); no ISSN, no review dates in the PDF. License CC BY 4.0 (footer). Scopus: unverified (no ISSN to search). SJR unknown. Peer review unclear.

## (b) Plain-language summary
An opinion paper saying AI-based incident diagnosis will only work if companies keep a fresh map of their services, a registry of schema and changes, and a searchable memory of past incidents. It sketches a five-layer architecture and quotes other papers' results. It has no experiment.

## (c) Problem and motivation
RCA is expensive because evidence is scattered across logs, events, graphs, deployments and contracts (pp.1-2). Supported by second-hand citations (gray failure, alert storms, troubleshooting guides). No data of its own.

## (d) Method
Conceptual: four requirements (Table II), a five-layer architecture (Table III), four proposed metrics (hypothesis precision, MTTR, novel incident detection rate, time to first actionable hypothesis); a "composite illustrative case" (p.6).

## (e) Datasets, protocol
None. Table IV reuses reported numbers from five other studies without a common protocol.

## (f) Results (relayed, second-hand)
MicroRCA 89% precision and 97% mean average precision; MicroNet 90% mean average precision; RCACopilot 76.6% accuracy across a year of Microsoft incidents; DiagFusion localization improvement 20.9% to 368% over single-modality baselines; alert-storm F1 above 0.9 with more than 98% alert volume reduction (Table IV, pp.5-6). The paper explains the gap between about 90% and 76.6% by stale context, without testing this.

## (g) Limitations and stern critique
Nothing measured; the headline inference compares different metrics and tasks; placeholder DOI, no ISSN or dates; citation [9] (Li 2026, with the author initial wrong) is described as knowledge-graph-assisted fault localization, which it is not; some references are from another journal family and one concerns IoT anomaly detection; single independent author.

## (h) Reproducibility
Nothing to reproduce. "Data available upon request".

## (i) Head-to-head with our work
No overlap in evidence. The conceptual point that RCA quality is bounded by the freshness of topology and context is relevant to our adaptive graph.

## (j) Does it change our problem? Could a reviewer say it exists?
No. It cannot be used as prior art for a method, and it gives no evidence on the problem.

## (k) Sentences
Safe: none recommended. If needed: "Position papers argue that RCA quality depends on fresh topology and change context [theysayitsre]." Must NOT write: any Table IV figure as this paper's result; that the paper demonstrates performance advantages; that it cites Li (2026) correctly.

## (l) Things to verify
Venue and ISSN; DOI validity; the relayed numbers at their sources.
