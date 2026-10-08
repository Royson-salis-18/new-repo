# Report: Chen et al. (2024), RCACopilot (EuroSys '24)

Key `chen2024automatic`. Note: `litdb/papers/chen2024automatic.md`. Coverage: arXiv v4 read in detail to page 12; deployment lessons and references skimmed; figures not inspected. Matrix key `ahmed2023llmrca` points to this paper (the first-author attribution in the matrix is wrong).

## (a) Bibliographic block
Yinfang Chen, Huaibing Xie, Minghua Ma, Yu Kang, and 14 others (Microsoft, UIUC and others). EuroSys '24, DOI 10.1145/3627703.3629553; arXiv 2305.15778v4. Peer reviewed. Scopus: unverified. SJR unknown.

## (b) Plain-language summary
Engineers script data-collection workflows per alert type; an LLM summarizes the collected text and, using similar past incidents as examples, names the likely root cause category and explains it.

## (c) Problem and motivation
Troubleshooting guides are manual and stale; 24.96% of 653 incidents had a new root cause category; 93.80% of recurring incidents recurred within 20 days (pp.3-6).

## (d) Method
Handlers (scope switching, query, mitigation), FastText embeddings, time-decayed similarity, GPT summary, multiple-choice few-shot prompt with an "unseen incident" option (pp.6-9).

## (e) Datasets, protocol
653 incidents from a Microsoft email service, manual labels by OCEs, 75/25 split, GPT-4 default (p.10).

## (f) Results (copied)
Micro-F1 0.766, macro-F1 0.533 (GPT-4), 0.761 / 0.505 (GPT-3.5); XGBoost 0.022 / 0.009; FastText 0.076 / 0.004; fine-tuned GPT 0.103 / 0.144; GPT-4 prompt-only 0.026 / 0.004; GPT-4 with GPT embeddings 0.257 / 0.122 (Table 2 p.11). Summarized diagnostic information 0.766 vs raw 0.689 micro-F1 (Table 3 p.12). 4.205 s inference.

## (g) Limitations and stern critique
Category classification, not localization; about 160 test incidents without intervals; baselines near zero, implausibly weak; hand-built handlers; one service of one company; no data or code; split type not stated in the part read.

## (h) Reproducibility
Not reproducible.

## (i) Head-to-head with our work
Different task; LLM explanation layer idea only.

## (j) Does it change our problem? Could a reviewer say it exists?
No. Exists for LLM incident classification; not for propagation-aware localization.

## (k) Sentences
Safe: "RCACopilot predicts incident root cause categories with a few-shot LLM and reports micro-F1 0.766 on one year of one Microsoft service's incidents [RCACopilot]." Must NOT write: "76.6% accuracy of RCA" as a microservice localization result.

## (l) Things to verify
Deployment section; baseline configuration; split protocol.
