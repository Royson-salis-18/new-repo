# Report: Tang et al. (2025), MicroRCA-Agent

Key `pantangshixiangtanghuanqipuzhiqingmiaozhixingwang2025microrca`. Note: `litdb/papers/pantang...microrca.md`. Page numbers are PDF pages.
Coverage: full text read to the end (18 pages, 2 references). Not read: prompt images (Figs 13, 16, 18) and good/bad case figures (Figs 19 to 22).

## (a) Bibliographic block
Pan Tang, Shixiang Tang, Huanqi Pu (Shanghai University), Zhiqing Miao (ECNU), Zhixing Wang (BIT). arXiv:2509.15635v1 [cs.AI], 19 September 2025. Footnote: technical report of a solution at the 2025 (8th) CCF International AIOps Challenge. No DOI, no venue, no ISSN. Not peer reviewed, not Scopus-indexed. Code: github.com/tangpan360/MicroRCA-Agent.

## (b) Plain-language summary
The team compresses logs, trace anomalies and metric changes into short text, and lets a large language model read it and name the faulty component and the cause. It scored 50.71 in the competition scoring. The paper says the metrics are the most useful signal and logs alone the least useful.

## (c) Problem and motivation
Competition task: given a fault time window, find the component and reason. No motivation data or incident statistics. Evidence type: assumed. Not a research claim about the problem.

## (d) Method
Logs: keep error logs in the window, Drain templates (156 learned from phase-one error logs), counts per pod and template. Traces: one Isolation Forest per (parent pod, child pod, operation) trained on 30-second average durations from 40-minute windows after 50 random faults (n_estimators 100, contamination 0.01), plus status.code not 0 check; top 20 of each reported. Metrics: normal baseline = windows before and after the fault with extremes trimmed; symmetric ratio of P50 and P99 against a 5% change threshold; two-stage LLM summarization (service and pod, then node). Final LLM call with the three summaries yields JSON (component, reason, reasoning trace) with regex and retries. LLM name, temperature and prompts are not in the text; the README references a DeepSeek API key.

## (e) Datasets, protocol, leakage
Competition environment (Online-Boutique-style services, Kubernetes, TiDB); no counts of faults, fault types or services in the paper. Phase-one data used to build templates and detectors; the scoring phase is separate. Leakage and realism: the metric baseline uses periods after the fault; Isolation Forest windows are assumed normal because they follow a recovery; the fault window is provided as input, not detected.

## (f) Results (copied)
Table 1 (p.16), challenge score: log only 23.59; trace only 31.09; metric only 42.78; log+trace 35.32; trace+metric 48.58; log+metric 51.27; all three 50.71. No baselines, no variance, no statistical tests; score definition not given.

## (g) Limitations and stern critique
Authors: a bad case shows LLM hallucination (trace chains not supplied but cited), planned retrieval or jury mechanisms (p.16). Mine: no baselines; undefined score; the full system is below the best two-modality system; LLM unnamed and stochastic with no repeats; baseline window uses post-fault data; no ablation of the LLM step; no faithfulness evaluation of the reasoning trace (the paper itself reports a hallucinated one); only two references.

## (h) Reproducibility
Code exists (checked 2026-10-07; 269 stars; no license; src, Dockerfile, run.sh, submission folder). It needs an LLM API key. Data: cited phase-one URL not checked. Not run.

## (i) Head-to-head with our work
Same family of ideas (non-LLM detectors feeding an LLM) as our planned explanation layer, but this report has no baselines and no propagation model. We should not claim to beat it (no comparable metric) and should not cite it as evidence that LLM agents work; at most as an architectural example.

## (j) Does it change our problem? Could a reviewer say it exists?
No change. A reviewer can say "LLM-agent RCA exists"; our defense is that the LLM only explains a ranking produced elsewhere and that we evaluate faithfulness. REVIEW_REPORT correction #1 (competition pipeline, not a general result) is confirmed.

## (k) Sentences
Safe: "MicroRCA-Agent (Tang et al. 2025) pairs Drain log templates, Isolation Forest trace detectors and LLM summaries of filtered metrics, and reports a challenge score of 50.71 on the 2025 CCF AIOps Challenge data [key]." / "Its authors report an LLM hallucination in a bad case [key]." Must NOT write: that it proves LLM agents localize root causes accurately; that its score is comparable to accuracy numbers elsewhere; that it is peer reviewed; that it is label-free in a strict sense (it fits templates and detectors on challenge phase-one data).

## (l) Things to verify
Score definition on the challenge site; LLM and prompts; whether phase-one data is publicly downloadable.
