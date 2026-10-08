# Report: Yang et al. (2021), AID: Aggregated Intensity of Dependency

Key `tianyiyang...2021efficient`. Note: `litdb/papers/` same key. Coverage: full text read (13 pages incl. references list start); Figs 1-6 not inspected.

## (a) Bibliographic block
Tianyi Yang, Jiacheng Shen, Yuxin Su, Xiao Ling, Yongqiang Yang, Michael R. Lyu (CUHK, Huawei). arXiv 2109.04893v1, cs.SE, 20 Aug 2021. Not Scopus-indexed (preprint). Published version: unverified. SJR unknown.

## (b) Plain-language summary
Counts calls, errors and latency per service per minute, then measures how closely a callee's series follows its caller's (with time lag). Closer following means a stronger dependency. Checked against engineer labels on two systems.

## (c) Problem and motivation
Binary dependency graphs do not show which dependencies matter in an outage (pp.1-5). Evidence: 5 of 13 AWS outages 2011-2020 "related" to dependency (Table I p.4); Huawei Cloud incident study of over 1000 incidents with no figures; engineer interviews at one company.

## (d) Method
Candidate pairs from spans; three KPIs per 1-minute bin; directed dynamic status warping (Algorithm 1 p.7); min-max normalised similarity averaged over KPIs (Eqs 1-2).

## (e) Datasets, protocol
Train-Ticket (25 services, 17.5M spans, 18 strong and 1 weak label) and Huawei Cloud (192 services, about 1e10 spans, 67 strong and 8 weak labels) (Table II p.7). Labels by PhD students and senior engineers; evaluation CE, MAE, RMSE; baselines Pearson, Spearman, Kendall.

## (f) Results (copied)
Industry: AID CE 0.3270, MAE 0.1751, RMSE 0.3044 vs best baselines 0.6030, 0.4501, 0.4537 (Table III p.8). TT: Pearson MAE 0.3305 better than AID 0.3435; AID better on CE and RMSE. DSW vs DTW on Industry CE 0.3270 vs 0.3584 (Table IV p.9). 155 s per pair of 1440-bin series (p.9). Case study: more than ten unnecessary dependencies optimised (p.10, anecdotal).

## (g) Limitations and stern critique
Tiny, skewed label set (89% to 95% strong); no constant baseline; labels binary vs continuous score; parameters set on evaluated data; no CIs or repeated runs; baselines only correlation coefficients; direct calls only; asynchronous calls weak; case study unquantified; the cascading-failure framing is motivation, not tested.

## (h) Reproducibility
Code and data stated at github.com/OpsPAI/aid (not checked). Industrial data cannot be fully shared.

## (i) Head-to-head with our work
Same family as our edge-weight estimation (label-free, trace-based). They evaluate edge strength against labels; we use weights for RCA and risk. Compare against their DSW similarity.

## (j) Does it change our problem? Could a reviewer say it exists?
Yes for "learn edge strength from traces without labels". No for RCA ranking or calibrated cascade-risk scoring. Corrects REVIEW_REPORT: AID does not predict cascades in time.

## (k) Sentences
Safe: "AID estimates continuous dependency intensity from trace-derived invocation, error and duration series without labels [AID]." Must NOT write: that AID predicts or forecasts failures; its percentage reductions as general results.

## (l) Things to verify
Published venue; repository; effect of using AID weights in RCA.
