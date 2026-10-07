# Fixes attempted and tests on larger apps (2026-10-07)

Scope: the problems found in `REVIEW_REPORT.md`, what we fixed, what we tested on larger applications, and what is still not solved.
Everything in this document is **semi-synthetic**: the background telemetry is **real** (77 minutes of the OpenTelemetry demo on your EC2,
no fault injected, 16 active services, 23 call edges), and the faults are **injected** with ground truth taken from the injection, never from our detector.
The effect of a fault (latency multiplier, error rate, propagation probability and lag) is an assumption. **None of this replaces real fault injection** (the demo's feature flags), which is still missing.

Scripts: `experiments/exp_fixes.py`, `experiments/exp_candidate_threshold.py`, `experiments/collect_long_healthy.py`. Raw results: `docs/experiments/fixes_results.json`, `candidate_threshold.json`.
Code: `rcalab/detector.py` (calibrated detector), `rcalab/replay.py` (fault injection into real telemetry), `rcalab/topology.py` (larger apps), `rcalab/cascade.py` (`EdgeLearner`), `rcalab/sources/jaeger.py` (self time).

## 1. Scorecard

| Problem from the review | What I did | Result | Status |
|---|---|---|---|
| Detector flags 43% of service-windows on healthy real traffic | one-sided, log-scale, causal detector with explicit evidence rules; threshold calibrated to a false-alarm budget | **0 false-alarm episodes in 32 min** at the strict thresholds (old detector: 215 episodes/hour) | fixed, with caveats (section 2) |
| Brand-new / sparse services looked like +30 sigma events | judge a feature only after 20 valid baseline samples and only in windows with at least 3 spans; unknown windows no longer break persistence | removed the main source of false alarms | fixed |
| Detection of real slowdowns | measured | **only 17-23% of root slowdowns caught at 1 alarm/hour, 38-47% at 5/hour** (any size from x2 to x8) | **not solved** |
| Victims look louder than the root cause | added self (exclusive) time from traces as a feature and a `selftime` ranking | best or near-best in some settings (A@1 0.49 vs random 0.08 at 50 services), not consistent | promising, **not proven** |
| "Learned" propagation probabilities are the prior | `EdgeLearner`: learn across incidents, empirical-Bayes prior | small app: average precision of next-victim forecast **0.16 -> 0.51** (oracle 0.53, structure-only 0.34). 100 services: mixed | partly solved |
| Cascade/precedence terms add nothing | tested at 17, 50, 100, 200, 500 services | **full method is never better than simple abnormality ranking; near random at 50-200 services** | **claim not supported** |
| Larger apps | random call graphs with real bootstrapped background, 50-500 services | compute fine (500 services: detect 0.96 s, rank 0.17 s per run); accuracy modest | tested |
| No real faults | not possible without the demo's feature flags | - | **still open** |

## 2. False alarms on real healthy traffic (test slice = last 127 windows = 32 min, never used for fitting or calibration)

| Detector | flagged service-windows | false-alarm episodes per hour |
|---|---|---|
| old robust-z (3.5, persistence 2) | 17.1% | **215** |
| calibrated, target 1/h and 2/h (threshold 8.25) | 0.0% | **0** |
| calibrated, target 5/h (threshold 7.25) | 1.5% | **15** (target missed) |
| calibrated, target 10/h (threshold 4.25) | 3.1% | **28** (target missed) |

Caveats: only 32 minutes of test data, so "0" means "none observed", not "below 1/hour with confidence". The budget is **not guaranteed**: the calibration slice
(windows 60-180) was calmer than the test slice, so looser targets overshoot. A real deployment needs a longer calibration period and periodic recalibration.
A "healthy" label is an assumption: I did not instrument the demo to prove it was fault-free.

## 3. What can and cannot be monitored at 15-second windows

Only **5 of 16 active services** (`cart`, `frontend`, `frontend-proxy`, `load-generator`, `product-catalog`) average at least 6 spans per window. For the rest, a per-window
latency percentile is built from a handful of requests (or none) and is not informative. This is a property of the data at this load, but it is a real limit of any
window-percentile method: **low-traffic services are effectively invisible**. Possible fixes (not built): adaptive windows that wait for enough spans, or per-span sequential tests (CUSUM / likelihood ratio) instead of window percentiles.

## 4. Detection of injected slowdowns (monitorable roots only; detected = root flagged within 10 windows; 60 injections per cell)

| Slowdown | old detector | calibrated 1/h | calibrated 5/h | calibrated 10/h |
|---|---|---|---|---|
| x2 | 45% | 18% | 45% | 57% |
| x4 | 35% | 17% | 47% | 58% |
| x8 | 43% | 23% | 40% | 40% |

Median delay 15-60 s (persistence of 3 windows already costs 30-45 s). The curve is **flat in fault size**, which says the limit is noise and persistence, not effect size.
The old detector looks similar here only because it flags everything all the time (215 false episodes/hour).

## 5. Root-cause ranking

### 5.1 Real 17-service topology (71-74 of 100 runs raised an alarm; rank at candidate threshold 3.5)
| method | A@1 (x4) | A@1 (x8) | MRR (x8) |
|---|---|---|---|
| anomaly_only (most abnormal service) | **0.46** | **0.46** | 0.65 |
| selftime | 0.34 | 0.35 | 0.60 |
| full (precedence + cascade + explained-away) | 0.34 | 0.31 | 0.54 |
| earliest / pagerank / no_cascade | 0.30-0.34 | 0.31-0.34 | 0.53-0.54 |
| random | 0.23 | 0.21 | 0.46 |

With about 70 runs the standard error is about 0.06, so the ordering among the middle methods is **within noise**. What is solid: everything beats random, and nothing beats plain "most abnormal service".

### 5.2 Larger applications (A@1, fault x6, only runs that raised an alarm)
| services | alarmed | full | selftime | anomaly_only | earliest | pagerank | random |
|---|---|---|---|---|---|---|---|
| 50 | 38/60 | 0.13 | **0.39** | 0.37 | 0.11 | 0.11 | 0.08 |
| 100 | 38/60 | 0.05 | 0.21 | **0.26** | 0.05 | 0.11 | 0.05 |
| 200 | 35/60 | 0.06 | **0.29** | 0.26 | 0.06 | 0.14 | 0.03 |
| 500 | 11/60 | 0.00 | 0.36 | **0.91** | 0.00 | 0.09 | 0.00 |

The n=500 row rests on 11 runs, so treat it as an indication only. Candidate-threshold sweep (`candidate_threshold.json`): raising the candidate threshold lifts `full` (for example 0.02 -> 0.18 at 100 services) but it never catches the plain ranking
(0.24-0.36 for `anomaly_only`, 0.25-0.49 for `selftime`). **Precedence and the cascade terms are net negative when many services raise noise flags**: whichever noisy service flagged first wins.

## 6. Cascade-risk forecasting at the moment of the alarm (truth = injected onset of each victim; horizon 8 windows; edges half "shielded" (p=0.1), half "open" (p=0.9))

Average precision (AP) is the informative number because victims are rare (prevalence 0-6%).

| topology / regime | AP learned, K=0 -> K=8 -> K=40 past incidents | AP structure-only ("callers of failing services") | AP oracle (true edge weights) | AUROC learned / structure / oracle |
|---|---|---|---|---|
| 17 services, fast cascade (lag 0-1) | 0.16 -> 0.51 -> 0.54 | 0.34 | 0.53 | 0.94 / 0.88 / 0.96 |
| 17 services, slow cascade (lag 2-6) | 0.37 -> 0.63 -> 0.65 | 0.71 | 0.74 | 0.97 / 0.92 / 0.98 |
| 100 services, fast | 0.50 -> 0.38 -> 0.37 | 0.12 | 1.00 | 0.98-1.00 / 0.99 / 1.00 |
| 100 services, slow | 0.38 -> 0.38 -> 0.40 | 0.25 | 0.93 | 0.95-0.99 / 0.84 / 1.00 |

Readings:
- In the **small** app, learning across incidents is a **real improvement** over learning within one incident (AP 0.16 -> 0.5), reaching the oracle in the fast regime; in the slow regime it matches but does not beat the structure-only rule on AP, while beating it on AUROC.
- In the **100-service** app the learner is far from the oracle (0.4 vs 0.9-1.0) with 40 incidents, and its AUROC is slightly **below** the uniform prior. With 143 edges, 40 incidents give each edge too few trials.
- With 2% to 6% positives and 500 to 2,100 candidates per cell, AP is noisy; no confidence intervals were computed. Do not quote these to three digits.
- Lead time exists only for **slow** cascades. With synchronous propagation (lag under 15 s) the victims are already affected by the time a 3-window alarm fires, so there is nothing left to forecast.
- The heterogeneity of edges (shielded vs open) is **my assumption**. Whether real call graphs have it (retries, timeouts, circuit breakers) is an empirical question the paper must answer or flag.

## 7. Larger-app cost
Per diagnosis run (T=300 windows, 9 features): 50 services detect 0.13 s / rank 0.01 s; 100: 0.29 / 0.02; 200: 0.39 / 0.04; 500: 0.96 / 0.17. The pipeline scales; accuracy is the issue, not compute.

## 8. What changed in the app
- `config.example.yaml`: detector defaults to `calibrated` with `alarm_budget_per_hour: 5`, `persistence: 3`, `candidate_threshold: 3.5`.
- Dashboard live mode: strict alarm first; no alarm means no ranking ("healthy"); after an alarm, candidates are ranked at the lower threshold; default ranking is `selftime`. The synthetic demo is unchanged.
- New feature `self_latency` (exclusive span time) is collected from Jaeger; 9 tests pass.

## 9. What this means for the paper
1. **Drop or demote the claim that precedence + cascade terms improve RCA.** Our own tests say they do not, and recent literature (Kintsugi 2026, "Rethinking RCA evaluation" 2026) says the same about graph structure.
2. **A defensible contribution is the evaluation itself**: a calibrated, label-free detector with a measured false-alarm rate on real traffic; the finding that most services in a typical demo are not monitorable at 15 s windows; self-time as a cheap discriminating signal; and learning propagation across incidents (small app) with its limits.
3. **Cascade forecasting only has value for slow cascades**, and learning needs many incidents per edge: state both limits.
4. **Real fault runs are mandatory**: toggle faults in the OTel demo's feature-flag page; `rcalab record` them; rerun `exp_fixes.py` logic on real labels.

## 10. Still open
- Real faults (not injected): the single most important missing piece.
- Detection sensitivity at strict budgets; low-traffic services (section 3).
- Budget guarantees (section 2), longer healthy data, drift handling.
- Confidence intervals for sections 5-6; more incidents per cell.
- Public benchmarks (RCAEval) and strong baselines (BARO, CIRCA, RCD): pending your download approval.
- microservice-mapper (the product) has not been re-tested on larger apps yet; see the follow-up note.
