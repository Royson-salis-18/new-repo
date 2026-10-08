# What is wrong with our approach, why, and what we can still do

*Written 2026-10-08. Every number below comes from a test we ran (files named in each section) or from a paper we read in full (page cited in `literature-review/`). Nothing is assumed. Where we have one run, it says "one run".*

---

## 0. The verdict in plain words

**What we wanted:** watch a live microservice app with no labels and no training, notice when it breaks, name the service that caused it (root cause), and say which healthy services will break next (cascade risk).

**What we actually have:**

| Claim we wanted to make | Status | One-line reason |
|---|---|---|
| "We detect faults with few false alarms on live traffic" | **Partly true** | 0.1 false alarms/hour on real healthy traffic, but only **42%** of injected faults are caught at that setting |
| "We find the root cause better than existing approaches" | **False on our evidence** (but see the UPDATE section: A@1 0.75 after the silence fix, equal to "most abnormal" with the same signals) | our ranking (A@1 0.44) is slightly below plain "most abnormal service" (0.46) and equal to the original notebook's ranking (0.46); random is 0.04 |
| "Our propagation reasoning (explain-away, precedence, cascade) helps" | **False on our evidence** | switching each term off changes nothing or improves results, in every test since 2026-10-06 |
| "We predict cascading failures" | **Not shown** | cascade risk was never better than the trivial rule "callers of a failing service" |
| "It works on real faults" | **One real fault** | a container stop on DeathStarBench, ranked #1, but only because the container disappeared (easiest possible fault) |
| "Our results compare with the papers" | **Not comparable** | the papers use labelled, pre-recorded benchmarks with the fault time given; we use our own live data and detect the time ourselves |

**Why it feels like "we are fucked":** the parts we hoped would be new (propagation-aware ranking, cascade prediction) do not beat simple baselines, and our data is too thin to detect slow or frozen services.

**Why we are not actually dead:** the parts that *do* work are exactly what the literature lacks (see `literature-review/GAPS.md` G2/G3):
1. a detector with a **measured false-alarm rate on real traffic** (no paper we read reports one);
2. a **ground-truth-first evaluation** (fault ledger, detected vs given time, false alarms per hour);
3. **honest negative results**: we can show *when* propagation reasoning does not help, which matches what Pham et al. (ASE'24) and Fang et al. (2025) found on public data.

A paper framed as "an operating-point-aware evaluation of label-free RCA" (GAPS.md section 4) is publishable with what we have plus about a week of runs. A paper claiming "a new RCA method that beats the state of the art" is not.

---

## UPDATE 2026-10-08 (evening): first LIVE frozen-service test, and what it showed

**What we did.** DeathStarBench social network (27 containers), light user traffic (4 requests/s), 6 healthy minutes, then `docker pause` on `post-storage-service` for 91 s, 4 minutes later `docker pause` on `user-timeline-service` for 91 s, each written to the fault ledger and always unpaused. Users saw **88%** and **43%** failed requests during the two pauses (independent truth). Files: `experiments/run_live_pause.py`, `docs/experiments/live_pause_results.json`, `live_pause_samples.csv`, `live_pause/`.

| | post-storage paused | user-timeline paused | false alarms (9 healthy min) |
|---|---|---|---|
| code before this test | **not flagged**, rank 8 of 27 | **not flagged**, rank 13 | 0 |
| after the fixes below (same data, so not an independent test) | **flagged**, rank 7 | **flagged**, rank 8 | 0 |
| "most abnormal" (before) | rank 9 | rank 16 | |

**Why it failed, found in the data:** during a pause the frozen container's CPU and traffic go to exactly 0, but
1. `docker stats` prints network bytes in kB steps, so healthy traffic already reads 0 in about a third of 10 s ticks: a drop to 0 scored only z = 1.6;
2. my common-mode rule treated "many services went quiet together" as a load drop and erased it;
3. a freeze stalls the whole chain above it (nginx-thrift, home-timeline, user-timeline all went silent too), so the frozen service's silence was "explained" by its silent callers.

**Fixes kept** (bench re-checked on all 6 seeds: unchanged, A@1 0.70 / 0.75, frozen 1.00, false alarms 0.10-0.15/h; real crash: root #1 in **all 8** variants, also without the crash signal and with compose edges only):
* SSH "silence" = a container that usually uses CPU or moves bytes had **neither** in a tick (a paused container shows exactly 0.00% CPU);
* a meaningful unit per feature in the log scale (`log(x + 2000 B/s)` for byte rates), so a one-kB tick on an idle series can no longer score z = 46;
* network activity used only as an input to "alive?", not scored on its own; thread count (`pids`) treated as an inherited symptom (threads pile up in services waiting on a slow callee).

**Tried and reverted:** a "deepest silent service is the cause" rule. It did not fix the live ranking and lowered bench frozen-service A@1 from 1.00 to 0.80.

**Honest conclusion.** With `docker stats` + logs only, a frozen service is now **detected** (flagged, no false alarms) but **not localised**: the whole call chain above it stalls at the same moment and looks identical from the outside. Localising it needs per-request traces (where requests wait), which DeathStar's Jaeger does not have yet (no traced traffic). The bench result (frozen A@1 1.00) does **not** transfer to real SSH data, and is now reported only with this caveat.

---

## UPDATE 2026-10-08 (afternoon): what we fixed in the logic, measured honestly

**Rule used:** every change was tuned on bench seeds 0-2 and then judged on seeds 3-5, which were never used for tuning. Numbers below are from the seeds never used for tuning unless marked.

| Change | Why | Measured effect |
|---|---|---|
| **Silence signal** (a service that usually reports went quiet) | a frozen or crashed service sends nothing, so it had nothing to score (P3) | frozen-service A@1 **0.06 -> 1.00**; overall A@1 **0.52 -> 0.75**, A@3 **0.63 -> 0.85**; false alarms unchanged (0.15/h) |
| **Activity-drop signal** for SSH data (network in+out) | a paused container stays in `docker stats` but stops talking | needed for the rule below; live `pause` still untested |
| **"Quiet is inherited" rule**: a service's silence counts only if its callers did not go quiet/down and none of its callees broke loudly; a stopped container is never explained away | on the real crash, the stopped service's cache (nobody calling it) and the entry point (traffic fell because requests failed) were blamed | real DeathStar crash **without** the crash signal: root rank **21-26 -> 1** (with the call graph), **-> 3** with only compose edges |
| **Real call graph** for DeathStar (hand-written from its source) and a read-only reader for real trace edges (`trace_edges`) | compose `depends_on` is start order, not calls (P7) | see the row above; DeathStar's own Jaeger has no traces yet because the app gets no traffic |
| **Threshold floor live**: tau >= 4 until 30 healthy minutes exist | a per-hour false-alarm budget cannot be calibrated from 2 minutes (tau had fallen to 1.5) | prevents early false alarms; not a measured gain |
| Window evidence (`win_k`), own-only explain-away | aimed at slow faults and noisy callees | +0.03 A@1, within noise, at 0.39 false alarms/h; left as switches, not default |

**Bench after the fixes (6 seeds):**

| Method | seeds 0-2: A@1 / A@3 | seeds 3-5 (judge): A@1 / A@3 | slow A@1 | false alarms/h |
|---|---|---|---|---|
| **ours, new default** | 0.70 / 0.76 | **0.75 / 0.85** | 0.04 / 0.23 | 0.10 / 0.15 |
| ours before the fixes | 0.44 / 0.50 | 0.52 / 0.63 | 0.04 / 0.23 | 0.10 / 0.15 |
| most abnormal (same new signals) | 0.73 / 0.80 | 0.76 / 0.83 | 0.14 / 0.29 | 0.10 / 0.15 |
| original notebook | 0.46 / 0.50 | 0.49 / 0.56 | 0.14 / 0.23 | 78.7 / 79.7 |
| random | 0.04 / 0.11 | 0.06 / 0.20 | | |

**What this does and does not change:**
* P3 (frozen services) is **fixed on the bench**; the live `docker pause` test is still to do (notebook 11d).
* On the bench, the gain comes from the new *signal*, not from the source-vs-victim reasoning: plain "most abnormal" with the same signals scores the same. The reasoning pays off on the **real** crash (root #1 instead of a victim), because real faults have knock-on effects (callees go quiet, callers' traffic drops) that the bench does not simulate. That bench limitation is now a stated threat to validity.
* P2 (slow faults) is **still open**.
* The DeathStar call graph was written by hand **after** seeing this crash (from the DeathStarBench source, not tuned to the answer); confirm it with real traces once the app has load.
* Still one real fault in total (P9).

---

## 1. What we are doing (the pipeline, one line per step)

See the flowchart in section 0 of `ipynb/rca_research.ipynb`.

| Step | What it does | File |
|---|---|---|
| Data | `docker stats` + log-error counts over SSH (10 s), or traces from Jaeger (15 s) | `colab/rca_lite.py` (`HostSampler`), `rcalab/sources/` |
| 1 Prepare | counters to rates, drop rows after collector gaps, `container_up` from presence | notebook section 2 |
| 2 Score | one-sided robust z of each series against its own recent past; anomalies never enter the baseline; heavy-tail and binomial spreads | notebook section 3 |
| 3 Threshold | tau chosen from a false-alarm budget on healthy history; per-series noise normalisation; persistence | notebook section 4 |
| 4 Common-mode | remove a shift that most services share (load, not a fault) | notebook section 5 |
| 5 Attribute | score = max(own evidence, symptoms not explained by a failing callee); crash bonus; blind-spot inference | notebook section 6 |
| 6 Risk | caller risk = severity of failing callee x edge probability (0.5 unless learned) | notebook section 7 |
| Check | fault ledger -> recall, delay, A@1/A@3, false alarms per hour | notebook sections 8, 9, 11 |

---

## 2. The evidence (all of it, good and bad)

### 2.1 Test bench, 2026-10-08 (notebook section 8; 3 seeds x 37-38 labelled faults, 10 h of real healthy OTel traffic per seed)

Averages over seeds 0, 1, 2 (raw file: `docs/experiments/bench_ablation_3seeds.csv`). Fault time given for ranking (like benchmarks); detection measured by our own detector.

| Method | recall | A@1 | A@3 | A@1 slow | A@1 errors | A@1 crash | A@1 hang | false alarms/h |
|---|---|---|---|---|---|---|---|---|
| **ours (default)** | 0.42 | 0.44 | 0.50 | 0.04 | 0.58 | 1.00 | 0.06 | **0.10** |
| ours + 3-tick smoothing | 0.43 | 0.47 | 0.49 | 0.17 | 0.61 | 1.00 | 0.03 | 0.34 |
| most abnormal service | 0.42 | 0.46 | 0.56 | 0.14 | 0.60 | 1.00 | 0.03 | 0.10 |
| earliest flagged | 0.42 | 0.46 | 0.56 | 0.14 | 0.60 | 1.00 | 0.03 | 0.10 |
| original notebook (whole-data z > 3, rank by count) | 0.52 | 0.46 | 0.50 | 0.14 | 0.66 | 0.94 | 0.04 | **78.7** |
| random | 0.42 | 0.04 | 0.11 | 0.04 | 0.06 | 0.00 | 0.06 | 0.10 |

(recall = root flagged during its fault. Recall is the same for ranking-only variants because they share the detector.)

**Read it this way:** every method finds crashes; every method fails slow and hang faults; on ranking, ours is slightly *worse* than "most abnormal" (0.44 vs 0.46 A@1, 0.50 vs 0.56 A@3). Our one clear win is false alarms: 0.1/h vs 78.7/h for the original notebook, about 800x fewer, at equal ranking accuracy.

### 2.2 What each component is worth (same bench, 3 seeds)

| Variant (one thing changed) | recall | A@1 | A@3 | false alarms/h | tau | Verdict |
|---|---|---|---|---|---|---|
| ours (default) | 0.42 | 0.44 | 0.50 | 0.10 | 3.25 | reference |
| no per-series normalisation | **0.28** | **0.38** | 0.50 | **1.37** | 13.0 | **the only component that clearly helps** (errors A@1 0.58 -> 0.23 without it) |
| no tail-aware spread | 0.43 | 0.44 | 0.52 | 0.29 | 3.25 | small false-alarm gain only |
| no binomial errors | 0.42 | 0.44 | 0.50 | 0.10 | 3.25 | no effect once normalisation is on |
| no self-healing baseline | 0.42 | 0.43 | 0.50 | 0.10 | 3.25 | tiny; slow A@1 0.04 -> 0.00 |
| no log scale | 0.42 | 0.43 | 0.52 | 0.05 | 3.25 | no clear effect |
| no common-mode removal | 0.42 | 0.44 | 0.50 | 0.10 | 3.25 | no effect on the bench (needed on the real crash, 2.4) |
| no explain-away (gamma = 0) | 0.42 | **0.46** | **0.56** | 0.10 | 3.25 | **removing it is better** |
| no crash bonus | 0.42 | 0.44 | 0.50 | 0.10 | 3.25 | no effect on the bench (crash roots already score highest); needed on the real crash |
| no blind-spot inference | 0.42 | 0.44 | 0.50 | 0.10 | 3.25 | no effect |
| persistence 1 | 0.43 | 0.44 | 0.50 | 1.56 | 3.25 | 15x more false alarms |
| persistence 3 | 0.39 | 0.44 | 0.50 | 0.78 | 3.00 | less recall |
| "sustained" window ranking | 0.42 | 0.43 | 0.50 | 0.10 | 3.25 | slightly worse |

Before today's changes (tail spread, binomial errors, normalisation) the same bench gave tau 18.5, recall 0.32, A@1 0.39 and error-fault recall 0.0 (seed 0).

### 2.3 Earlier tests (2026-10-06 and 07; `docs/FIXES_AND_TESTS.md`, `docs/REVIEW_REPORT.md` section 4)

| Test | Result |
|---|---|
| False alarms on real healthy OTel traffic, old detector | flags in 89% of windows, 7 services per window (215 per hour) |
| Same, calibrated detector | 0 in 32 held-out minutes (budget not guaranteed) |
| Detection of injected slowdowns, monitorable roots | 17-47% depending on budget |
| Ranking, 17-service topology | "most abnormal" A@1 0.46; full method (precedence + blast radius) 0.31-0.34; random 0.22 |
| Ranking, random 50-200 service topologies | full method near random; simple ranking 0.24-0.36 |
| Cascade risk AUROC | 0.99-1.00, equal to the prior-only model; structural rule 0.90-1.00 |
| Edge probabilities after an incident | 82% exactly at the prior 0.5 (synthetic), 22% (live) |
| SSH sampler cost | 43 s per cycle on a 24-container host; load average > 24 on 2 vCPU |

### 2.4 The one real fault (DeathStarBench, `post-storage-service` stopped for 124 s; notebook section 9)

| Variant | rank of the true root | first-ranked | false flags before the fault |
|---|---|---|---|
| full method | **1** | post-storage-service | 0 |
| without `container_up` | 23 | nginx-thrift (a victim) | 0 |
| without the crash bonus | 12 | nginx-thrift | 0 |
| without wiring edges | 1 | post-storage-service | 0 |
| no crash bonus, no common-mode | 12 | nginx-thrift | 0 |
| no crash bonus, no wiring edges | 13 | nginx-thrift | 0 |

The client saw 95% failed requests during the stop and 0% outside it. The victims' error logs jumped about 30x; the root only vanished. **Without the "container disappeared" fact, every variant blames a victim.**

---

## 3. The problems, one by one

Each problem: **what is wrong -> evidence -> why it happens -> what it means for the paper -> fix (cost) -> status.**

### P1. The ranking is no better than "pick the most abnormal service"
* **Evidence:** 2.1 (0.44 vs 0.46), 2.2 (removing explain-away raises A@1 to 0.46 and A@3 to 0.56), 2.3 (full method 0.31-0.34 vs 0.46).
* **Why:** (a) in most faults the root *is* the most abnormal service (Fang et al. 2025: 68% of 737 public cases are of this easy type), so there is nothing for propagation reasoning to fix; (b) in the hard cases (slow, hang) the root's own evidence is too weak or missing, so explain-away has nothing to work with; (c) the wiring is incomplete (P7), so explain-away is often switched off without anyone noticing.
* **Paper:** cannot claim a better RCA method. Can claim: "propagation reasoning adds nothing on label-free live data at a fixed false-alarm rate; here is where and why". That is gap G1 in `GAPS.md`.
* **Fix:** report results split by difficulty (root loudest vs not), add NSigma/BARO/SimpleRCA baselines (2-3 days with RCAEval data).
* **Status:** open; baselines not run.

### P2. Slow faults are almost invisible in our data
* **Evidence:** bench slow-fault A@1 0.04 (0.14 for "most abnormal", 0.17 with smoothing); earlier 17-47% detection.
* **Why:** p95 latency per 15 s tick computed from 2-30 spans jumps 10x or more when the service is healthy (image-provider: healthy z up to 24). A 2-5x slowdown sits inside that noise. With docker-stats data (DeathStar), there is no latency at all.
* **Paper:** must state the minimum detectable effect: a slowdown under about 5x is not detectable at 15 s windows with this traffic.
* **Fix:** (a) more traffic (a steady load generator: about 20+ requests per service per tick); (b) longer windows for low-traffic services; (c) per-request tests (compare span latency distributions, Mann-Whitney) instead of a p95 per tick; (d) self-time from traces in SSH mode too (needs Jaeger on every bench). Cost 1-3 days each.
* **Status:** open. Smoothing (3-tick median) helped slightly: A@1 slow 0.04 -> 0.17, at 0.34 false alarms/h.

### P3. Frozen ("hang"/pause) services are not found
* **Evidence:** bench hang A@1 0.03-0.06 for every method (random also 0.06); the live pause test has not been run.
* **Why:** a frozen service sends no telemetry, so it has nothing to score; its callers show timeouts and look like the root. Our blind-spot inference only gives the silent service 0.9 x its callers' unexplained symptoms, which is always less than the callers' own score.
* **Paper:** this is the clearest open problem and matches gap G3 ("silence is a symptom"). If we fix it, it is a real contribution.
* **Fix:** a "went silent while callers keep calling it" signal: expected spans (from its callers' outgoing calls or its own history) minus observed spans, scored as own evidence. For SSH data: CPU drops to ~0 with `container_up` = 1 while callers' errors rise. Test on the bench (hang rows) and live (`docker pause`). Cost 1-2 days.
* **Status:** open; it is the best single thing to work on.

### P4. Crashes look solved only because they are trivial
* **Evidence:** crash A@1 = 1.00 for us, for "most abnormal", and 0.94 for the original notebook.
* **Why:** a stopped container disappears from `docker stats`; `container_up = 0` is a fact, not an inference.
* **Paper:** do not let crashes inflate the average. Report per fault type. One real crash (n = 1) is a demonstration, not evidence.
* **Fix:** report per-type tables; run at least 10 real faults per type (stop, pause, CPU limit, network delay, error injection).
* **Status:** open.

### P5. The detector trades recall for silence
* **Evidence:** at 0.1 false alarms per hour, 42% of injected roots are flagged; the original notebook flags 52% but raises 78.7 false alarms per hour.
* **Why:** the threshold is set by the noisiest series; normalisation helps but the data are noisy (P2).
* **Paper:** report the full curve (recall vs false alarms per hour), not one point. This curve is itself new (gap G2).
* **Fix:** the budget sweep in notebook section 8 already produces it; add confidence intervals over seeds. Cost: hours.
* **Status:** partly done.

### P6. The data are thin
* **Evidence:** OTel: only 21-78% of 15 s ticks have any latency per service; Prometheus on the OTel host returned 504 on every query; DeathStar SSH data have CPU, memory, network, log counts, but no latency or traces.
* **Why:** demo apps with a light load generator; SSH sampling every 10-43 s; no metrics pipeline on most hosts.
* **Paper:** the papers we compare with use metrics + logs + traces for every service at 1 s or better.
* **Fix:** on every bench: a steady load generator, Jaeger/OTel collector, cAdvisor or node exporter; collect over hours. Cost: 1 day per bench.
* **Status:** open; needs your benches running.

### P7. The wiring (call graph) is incomplete, which silently disables explain-away
* **Evidence:** DeathStar compose file gives 19 `depends_on` edges for 27 containers; nginx-thrift's real callees are mostly missing, so its symptoms were never explained away.
* **Why:** `depends_on` describes start order, not calls. Real call edges come from traces.
* **Fix:** take edges from traces (Jaeger dependencies API) whenever available; report edge coverage. Cost: half a day.
* **Status:** open.

### P8. The test bench is partly circular
* **Evidence:** the injection model in section 8 assumes, for example, that a slow root shows higher self time and its callers do not; that is exactly what our "own evidence" uses.
* **Why:** any semi-synthetic bench encodes assumptions about propagation.
* **Paper:** bench numbers are an upper bound for our method's propagation logic. Only ledger-scored real faults (sections 9 and 11) are real evidence; say so in threats to validity.
* **Fix:** real fault campaigns (P4), plus RCAEval's public real-fault data. Cost: 2-4 days.
* **Status:** open.

### P9. One real fault in total
* **Evidence:** the DeathStar crash is the only fault we caused and recorded on a real system.
* **Fix:** notebook section 11d runs a fault and scores it automatically; repeat 10+ times per type on 2+ apps, at random times, with 5+ healthy minutes between faults.
* **Status:** tooling ready; runs not done.

### P10. Cascade risk is unproven
* **Evidence:** AUROC equal to the prior-only model; the structural rule ("callers of a failing service") does as well.
* **Why:** with 0.5 edge probabilities, risk is just the structure; learning needs many incidents per edge (40 incidents were not enough for 143 edges).
* **Paper:** drop "cascade prediction" as a headline. Keep it as a second task compared against the structural rule and persistence, with lead time and calibration (gap G4).
* **Status:** open.

### P11. Time resolution hides the order of events
* **Evidence:** calls propagate in milliseconds; our ticks are 10-15 s, so the root and its victims flag in the same tick.
* **Why:** that is why "who flagged first" (precedence) was noise and made rankings worse.
* **Fix:** per-request trace analysis (span timestamps) if order is needed; otherwise drop precedence.
* **Status:** precedence dropped.

### P12. Comparing with the papers is not possible as things stand
* **Why:** they use labelled, pre-recorded benchmarks with the fault time given (RCAEval, AIOps challenge data, proprietary data). Our data are live and our detector must find the time.
* **Fix:** run the same open apps the papers used (Sock Shop, Online Boutique, Train Ticket) on our VPC with the same fault types, and run our method on RCAEval with the fault time given. Then numbers are comparable. Cost: 2-4 days.
* **Status:** open; needs approval for downloads and AWS time.

### P13. The original notebook's approach was misleading
* **Evidence:** 78.7 false alarms per hour; whole-dataset z-scores use the future and the fault itself (leakage); cumulative counters scored as values; the first row of every session has a log backlog (log_count = 100); ranking by counts put `user-1` above the labelled `orders-1`.
* **Status:** fixed in the new notebook (sections 2-4).

### P14. Watching changes what we watch
* **Evidence:** the SSH sampler took 43 s per cycle on a 24-container host; load average above 24 on 2 vCPU.
* **Fix:** sample less often, or use a metrics agent; report the overhead.
* **Status:** open.

### P15. Statistics are thin
* **Evidence:** 38-45 faults per seed, 3 seeds; 1 real fault.
* **Fix:** 30+ cases per fault type, bootstrap confidence intervals clustered by seed or run.
* **Status:** open.

---

## 4. What we can honestly claim today

| Claim | OK? |
|---|---|
| A label-free detector whose threshold is set from a false-alarm budget; 0.1 false alarms/h on 10 h of real healthy traffic | yes (bench) |
| About 800x fewer false alarms than the original approach at the same ranking accuracy | yes (bench, 3 seeds) |
| Presence (`container_up`) turns crash RCA from "victim blamed" into "root first" on a real app | yes, n = 1 |
| Propagation reasoning does not help on our data; here is when it cannot (thin data, incomplete wiring, root not the loudest) | yes (negative result) |
| Slow and frozen services are not detectable with 15 s trace aggregates at this traffic level | yes (negative result) |
| Our method is better than the state of the art | **no** |
| We predict cascading failures | **no** |
| Results comparable with published numbers | **no**, until P12 is done |

---

## 5. What to do next, in order (each with how we will know it worked)

| # | Task | Done when | Days |
|---|---|---|---|
| 1 | Silence signal for frozen services (P3) | bench hang A@1 rises above 0.3 without lowering other rows; a live `pause` ranks the root in the top 3 | 1-2 |
| 2 | Real fault campaign on your benches (P4, P9) | 10+ ledger-scored faults per type (stop, pause, CPU limit, delay) on 2 apps | 2-3 |
| 3 | Trace edges instead of compose edges (P7) | edge coverage reported; DeathStar explain-away active | 0.5 |
| 4 | Recall vs false-alarm curve with confidence intervals (P5) | figure with 3+ seeds | 0.5 |
| 5 | RCAEval + baselines (NSigma, BARO, SimpleRCA, PageRank) with fault time given (P1, P12) | per-difficulty table | 2-3 |
| 6 | More traffic and data on the benches (P2, P6) | 20+ spans per service per tick; slow-fault recall measured again | 1 |
| 7 | Write the paper as an evaluation study (GAPS.md section 4) | draft with the tables above | 2 |

---

## 6. Words used here

| Word | Meaning |
|---|---|
| root cause | the service where the fault was injected (from the ledger) |
| victim | a service that looks broken only because it calls the root |
| recall | share of faults where the root itself was flagged during the fault |
| A@1 / A@3 | share of faults where the root is first / in the top 3 of the ranking |
| false alarms/h | flag episodes per hour outside every fault window |
| tau | the alarm threshold, chosen from the false-alarm budget |
| ledger | the record of faults we caused, written at the moment we caused them |
| semi-synthetic bench | real healthy traffic with faults added by code; useful for comparisons, not proof |
