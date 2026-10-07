---
key: podduturi2025microservice
title: "AI for Microservice Monitoring & Anomaly Detection"
authors: "Podduturi, Santhosh (independent researcher, USA)"
year: 2025
venue: "ICCSAIML'25 conference proceeding, published in International Journal of Emerging Trends in Computer Science and Information Technology (Eureka Vision Publication), pp.192-211"
publisher: "Eureka Vision Publication (ScienceTech Xplore per Crossref)"
doc_type: proceedings-article
doi: "10.56472/ICCSAIML25-125 (PDF header; Crossref lists 10.56472/iccsaiml25-125)"
issn: "3050-9246 (journal ISSN printed on p.1)"
scopus_indexing: "not found: ISSN 3050-9246 returned 0 results in the Scopus Sources preview (2026-10-07); the proceedings volume has no ISSN in Crossref; status of the volume: unverified, likely not indexed"
scopus_match: "ISSN 3050-9246, see litdb/reference/scopus_checks.md"
sjr_quartile: "unknown: no list supplied; venue not found in Scopus preview"
peer_reviewed: "unclear (conference proceeding of a low-visibility publisher; no review dates in the PDF)"
cited_by_crossref: ""
n_references: "15"
license: "unknown (not stated in the text read)"
batch: "5"
read_status: reviewed                  # full text read; no tables or figures of results exist
pages: 21
text_chars: 94365
metadata_source: crossref
task: "overview / narrative review (no method, no experiment)"
supervision: "n/a"
online_or_streaming: "n/a"
telemetry: "metrics, logs, traces, events (described generically)"
propagation_modeling: "none"
forecasts_future_failures: "generic claims only"
llm_used: "no"
systems_evaluated: "none (four unnamed hypothetical-looking 'use cases')"
datasets: "none"
dataset_open: "n/a"
code_open: "n/a"
baselines_compared: "none"
metrics: "none"
headline_result: "none (no numbers); qualitative claims of reduced downtime and fewer false positives in unnamed use cases (pp.12-14)"
evidence_quality: "1"
relevance_to_us: "1"
overlap_with_us: "none"
threat_level_for_novelty: "low"
---

# AI for Microservice Monitoring & Anomaly Detection

> Reading notes written from the **full text** (`litdb/texts/podduturi2025microservice.txt`). Page numbers are PDF pages (journal pages 192 to 212).
> Contains no tables of results or experiments.

## 1. One-paragraph summary
A 21-page narrative overview of why microservice monitoring is hard and how supervised, unsupervised, deep and reinforcement learning could be applied to anomaly detection, followed by four unnamed "use cases" (e-commerce, finance, healthcare, telecom) described without data, numbers or sources, then challenges and future directions. It presents no method, experiment or measurement.

## 2. Problem and motivation
- Problem: monitoring and anomaly detection in microservices (pp.1-3).
- Motivation: generic statements about thresholds producing false positives and delayed detection. Evidence type: assumed.
- Real? Not argued with evidence.

## 3. Method
- None. Sections 3 to 5 describe generic ML techniques (supervised, unsupervised, autoencoders, LSTMs, RL), data collection and preprocessing (normalization, Min-Max or z-score), deployment and feedback loop (pp.5-12). Section 6 describes four use cases (pp.12-14). Sections 7 to 9 discuss challenges (data quality, interpretability, scalability, concept drift) and future directions (predictive anomaly detection, self-healing, federated learning, multi-agent systems) (pp.14-21).

## 4. Data and experimental setup
- None. The "case studies" give no organization names, datasets, model configurations or numbers (pp.12-14).

## 5. Results
| Metric | Theirs | Best baseline | Baseline name | Page |
|---|---|---|---|---|
| none reported | n/a | n/a | n/a | n/a |

- The use cases claim reduced downtime, fewer false positives, proactive alerts and "improved patient outcomes" without any figures (pp.12-14).

## 6. Limitations
- Stated: challenges of deploying AI (data quality, interpretability, scalability, real-time constraints, drift) (Sec. 7-8).
- **My critique:**
  1. No evidence of any kind; the "case studies" are unattributed narratives.
  2. The reference list cannot be matched to real publications. I checked eight of the listed DOIs with Crossref (2026-10-07): six returned "not found" (refs [1], [4], [6], [12], [14], [15]); 10.1145/3359992 (ref [7], stated as an ACM Computing Surveys article) resolves to the proceedings of a CoNEXT workshop; 10.1109/ACCESS.2020.3005439 (ref [11], stated as an IEEE Access paper on microservice monitoring) resolves to a paper titled "Fractional Controller Design of a DC-DC Converter for PEMFC". The arXiv identifier in ref [10] (2101.01642) resolves to a physics paper ("Probing non-affine expansion with light scattering"). Two references share the page range 1234-1245 ([1], [15]). The Vaswani citation lists the first author as "G. S. Vaswani" ([5]). These facts suggest the references may be erroneous or fabricated; I cannot determine intent.
  3. The paper mixes unrelated domains (fraud detection, patient monitoring) under "microservice monitoring".
  4. Single independent author; publisher and venue are low-visibility and the ISSN is not in Scopus.
  5. Claims such as "AI can predict failures before they occur" are made without support.
- Not discussed: any quantitative comparison; label requirements in practice; evaluation protocols.

## 7. Reproducibility
- Nothing to reproduce.

## 8. Comparison with OUR work
| Dimension | This paper | Ours (rca-lab) | Who is stronger, and why |
|---|---|---|---|
| Label requirement | generic discussion | label-free | n/a |
| Live / streaming | claims real-time | incremental windows | Ours implemented |
| Telemetry used | generic | traces (+ metrics) | n/a |
| Propagation modelling | none | edge probabilities | Ours |
| Forecasts future failures | generic claims | claimed, untested | Neither evidenced |
| Explanation | mentions LIME and SHAP | templates | n/a |
| Evaluation rigor | none | synthetic only | Ours |
| Open / reproducible | n/a | yes | Ours |

- **What they have that we do not:** nothing.
- **What we have that they do not:** an implementation and tests.
- **Could a reviewer say "this already exists"?** No.
- **Position:** do not cite.
- **Must we run it as a baseline?** No.

## 9. Does this paper change what problem we should solve?
- No. It must not be used as evidence that the problem is real or solved; its numbers and sources are unverifiable.

## 10. Citation-ready facts (each with page)
- None recommended. If mentioned at all: "The paper is a narrative overview without experiments (pp.1-21)."

## 11. Open questions / things to verify
- None worth the effort; flag the reference list problem to the team and remove this paper from any citation list.
