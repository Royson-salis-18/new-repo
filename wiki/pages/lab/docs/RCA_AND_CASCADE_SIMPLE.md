# RCA and cascade logic: what it does, why it is not on par, what to change

Plain-language summary. Numbers come from our tests (`FIXES_AND_TESTS.md`) and from papers we read in full (`litdb/`). Paper numbers are copied from those papers; we have **not** run our method on their data.

---

## 1. What the current logic does

**Step 1. Detect.** For every service and every 15-second window we compare its numbers with its own normal behaviour (taken from the first minutes). We only count the bad direction: latency up, errors up, traffic dropping, CPU/memory up. A service is flagged when it stays above the threshold for 3 windows in a row. The threshold is picked so that healthy traffic raises about N false alarms per hour.

**Step 2. Rank root causes (the "full" method).** Among flagged services we score each one:

> score = how abnormal it is  x  ( 0.4 x how early it flagged  +  0.6 x how many other flagged services it could have caused )  x  ( 1 - 0.8 x how much an earlier-failing dependency already explains it )

Simpler methods we compare against: **most abnormal service**, **largest self-time anomaly** (self time = latency of the service itself, not waiting for others), **earliest to flag**, **PageRank**, **random**.

**Step 3. Cascade risk.** Each call edge gets a probability "if the callee fails, the caller fails too". Risk of a service = chance that at least one failing service reaches it within 3 hops (noisy-OR). The edge probabilities are either counted inside one incident (almost always just the 0.5 starting guess) or learned across many past incidents.

---

## 2. What we measured

| Question | Result | Where |
|---|---|---|
| False alarms on healthy real traffic | 215 per hour (old) -> 0 in 32 min (new, strict) | real OTel data |
| Do we catch an injected slowdown on the root? | 17-47% depending on the false-alarm budget | injected into real data |
| Best root-cause method | **plain "most abnormal service" (A@1 0.46)**; our full method 0.31-0.34; random 0.22 | 17-service topology |
| Large apps (50-200 services) | full method **near random**; simple ranking 0.24-0.36 | injected into real data |
| Learning edge probabilities across incidents | helps in the small app (precision 0.16 -> 0.51), unclear at 100 services | injected |
| Real fault on a real 27-container app (SSH) | crashed container **vanished from the data** for 12 samples; its callers' error logs jumped from ~0.6 to 19-36 per sample | Death Star, partial (client log lost) |

---

## 3. Why the results are not proper yet

1. **No real faults yet.** Everything above is real background noise plus *simulated* faults. We cannot compare it with a paper's accuracy until we run on real fault data.
2. **Our data is thinner than the papers' data.** Only 5 of 16 services had enough traffic to judge latency per 15 s. Prometheus was unreachable, so we have no per-service CPU/memory in tools mode. The papers use metrics + logs + traces for every service.
3. **We have to detect the fault first; benchmarks hand the method the fault time.** Our detection catches 17-47%, and then ranking runs on a shaky window. Pham et al. show methods collapse when the time is off (NSigma on Train Ticket: 0.81 at the exact time, 0.03-0.12 when 60 s late).
4. **"Who flagged first" is noise-sensitive.** With many small false flags, the earliest flagged service is often just noise. That is why precedence and "blast radius" make the full method *worse* than plain abnormality in big apps. Also, calls propagate faster than our 15 s window, so order is invisible.
5. **Propagation weights are mostly guesses.** Counting inside one incident gives the starting value (0.5) for 82% of edges. Learning across incidents needs many incidents per edge (40 incidents was not enough for 143 edges).
6. **We only follow call edges.** Real failures also spread through shared hosts and sibling replicas (Xie et al.: adding such group relations raised Avg@3 by 0.08-0.14). Our simulation also assumed call edges only.
7. **We use no labels; the strong papers do.** Chain-of-Event gets 79.3% top-1 with labelled history, but a standard event graph without labels gets 17.1% (proprietary data). DeepHunt without labels: A@5 0.90-0.96 but **A@1 only 0.445 on the harder system**; with 25% labels 0.783. Our 0.46 is in that label-free range, but on different data, so it is not a comparison.
8. **Some papers are not a fair bar.** Li 2026 (94% F1) uses proprietary data and inconsistent numbers. Pham et al. found most causal-graph RCA methods **no better than random** on 4 benchmarks and simple methods work better. So "on par" should mean on par with **simple, label-free baselines on public data**, not with those headline numbers.
9. **SSH data shows the victims, not the root.** In the Death Star crash, the callers screamed (error logs x30) while the stopped container simply disappeared. Without a "container is gone" signal the model ranks the victims first. (We added `container_up` for this; it is not yet scored on real data.)

**Honest answer to "why can't we be on par":** we cannot say we are not on par, because we have not run on the same data. What we can say: our method has no advantage over simple baselines in our tests, our detection step is weak, and our data is thinner than the papers'.

---

## 4. What to change (in this order)

1. **Run on real data.** Public benchmark RCAEval (Sock Shop, Online Boutique) and real faults from the OTel demo's feature flags. *Needs your OK for downloads and for toggling faults.*
2. **Simplify the ranking.** Use "most abnormal" or self-time as the main score. Keep precedence only among *strongly* flagged services, and drop blast radius and the explained-away term unless weights are fitted on held-out incidents.
3. **Add the missing signals.** Use `both` mode: traces plus per-service CPU/memory/network from SSH or Prometheus, plus `container_up` and log errors.
4. **Fix time resolution.** Use longer windows for low-traffic services, and per-request change tests instead of a 15 s percentile. Evaluate with the fault time *given* (like benchmarks) and *detected* (real use), and report both.
5. **Learn propagation properly.** Learn across many incidents, add shared-host and sibling relations, and report confidence intervals.
6. **Add the right baselines.** NSigma, BARO, MicroRCA-style PageRank, CIRCA, RCD (RCAEval has code). Report A@1, A@3 and a "no-telemetry prior" baseline.
7. **Calibrate honestly.** More healthy data, a budget check on a separate slice, drift handling.
8. **Reword the paper's claim.** Contribution = a calibrated, label-free detector with a measured false-alarm rate on real traffic, the self-time signal, and an honest evaluation. Drop "novel cascade prediction" and the claim that precedence/cascade terms help.

---

## 5. Notes on the Death Star crash test
- Done on the host you approved: one container (`post-storage-service`) stopped for ~110 s under light load, then restarted (the log confirms the restart). A later error in my script (SSH banner timeout) prevented the events file and client-side log from being saved, and both hosts are unreachable now, so this test is **partial**: only the raw samples survived.
- To redo: bring the host back, rerun `experiments/run_ssh_crash.py` (about 11 minutes), then `experiments/analyze_ssh_crash.py`.
