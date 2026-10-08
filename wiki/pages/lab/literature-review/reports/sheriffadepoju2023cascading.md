# Report: Adepoju (2023), Cascading Failure Modes in Model-as-a-Service Architectures

Key `sheriffadepoju2023cascading`. Note: `litdb/papers/sheriffadepoju2023cascading.md`. Page numbers are PDF pages.
Coverage: full text (12 pages) read; Figure 1 not inspected; references checked by Crossref lookup for ten entries.

## (a) Bibliographic block
Sheriff Adepoju (Prairie View A&M University). International Journal of Scientific Research in Civil Engineering, vol. 7, issue 6, pp.109-120, Technoscience Academy, accepted 1 Dec 2023, published 15 Dec 2023. DOI 10.32628/IJSRCE237530. ISSN 2456-6667. License CC BY-NC. Scopus: ISSN not found in the Sources preview on 2026-10-07 (0 results; discontinued status cannot be excluded). SJR unknown. Peer review: not described; two weeks from acceptance to publication.

## (b) Plain-language summary
An essay claiming that services that depend on machine-learning models can fail without errors, by producing worse decisions, and that these failures can cascade. It proposes thinking about circuit breakers and fallbacks in terms of decision quality. It has no data, no experiments and no case studies.

## (c) Problem and motivation
ML models as runtime service dependencies introduce "silent" decision-quality failures that propagate (pp.1-4). Motivation is conceptual, backed by citations to general cascading-failure and IoT literature. No incident data.

## (d) Method
None. A taxonomy (Table 1, p.5) of five cascade types, a discussion of circuit breakers, static and dynamic fallbacks, graceful degradation (pp.5-7), security, privacy and policy cascades (p.8), and a challenges table (Table 2, pp.9-10).

## (e) Datasets, protocol, leakage
None.

## (f) Results
None. The conclusion states that the study "systematically evaluated the dynamics of failure" (p.10), but no evaluation method appears in the paper.

## (g) Limitations and stern critique
No evidence; the claim of systematic evaluation is unsupported; venue is a civil-engineering journal not found in the Scopus preview and the publication took two weeks; ten references checked in Crossref exist, but several are unrelated to the topic (deep learning in computational chemistry [4], circumpolar health congress proceedings [5], naval ship architecture [15], automotive E/E architectures [22], a Greek thesis [3]); some references are from the same publisher family as Podduturi (IJETCSIT, ISSN 3050-9246 [10]); the text contains garbled headings and unusual phrasing consistent with automated paraphrasing (an observation about text quality); one DOI (ref [9], IJRPETM) was not found.

## (h) Reproducibility
Nothing to reproduce.

## (i) Head-to-head with our work
No overlap in method or evidence. Its only relevance is the idea that ML-dependent services can fail through decision-quality degradation, which our telemetry-based detector would not see.

## (j) Does it change our problem? Could a reviewer say it exists?
No. It cannot be used to claim that cascading-failure prediction is under-explored or solved; it provides no data and a weak venue. REVIEW_REPORT's classification of this paper as weak evidence is confirmed.

## (k) Sentences
Safe: "Conceptual work has argued that machine-learning model services add silent decision-quality failure modes to cascading failures in service architectures [sheriffadepoju2023cascading]." (with the word "conceptual".) Must NOT write: that the paper shows or measures cascading failures; that it evaluated resilience mechanisms; that it supports a cascade prediction method.

## (l) Things to verify
Venue status in Scopus (active vs discontinued); Figure 1.
