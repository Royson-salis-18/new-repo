# Cross-paper research gaps (v2, thorough)

Purpose: identify gaps that **several papers together** leave open, that **our project can actually close** with what we have built,
and that will **survive a hostile reviewer and the final grading**. Written 2026-10-08. Supersedes v1 (commit 638cc09).

---

## 0. How this was produced, and how far to trust it

| Source | What it is | Weight |
|---|---|---|
| 37 papers read in full (`litdb/papers`, batches 1-13) | numbers copied with page references | primary evidence |
| 28 papers with abstract only (no open PDF), via `docs/literature/raw_openalex.json` | used **only** to check whether a gap is already closed | threat check, marked **[abs]** |
| Our own tests (`docs/FIXES_AND_TESTS.md`, `docs/RCA_AND_CASCADE_SIMPLE.md`, `docs/REVIEW_REPORT.md` section 4) | real OTel traffic with injected faults, Death Star crash test | shows we hit each gap ourselves |
| Papers cited in `REVIEW_REPORT.md` but not in litdb ("Does graph structure earn its place?" 2026, Kintsugi 2026, OTel AIOps benchmark 2026) | abstract level, other session | marked **[rev]**, not verified here |

Rule used: a gap counts only if (a) at least three read papers show it, (b) no read paper closes it, and (c) the abstracts of the unread papers do not obviously close it.
Evidence IDs (A12, B7, ...) refer to `PROBLEM_EVIDENCE.md`.

---

## 1. What the field has already established (do NOT claim these as ours)

| Settled point | Shown by (read in full unless marked) |
|---|---|
| Label-free / unsupervised RCA exists and works on benchmarks | CIRCA (KDD'22), DeepHunt (TOSEM, A@5 0.90-0.96 with zero labels), CausalRCA (JSS'23), TraceRCA [abs], BARO [abs], TORAI [abs], LatentScope [abs] |
| Early warning of QoS violations with culprit naming exists (supervised) | Seer (p.2: 91% / 89%); node-failure prediction (Lin 2018) [abs]; SuanMing (via Faseeha, unread) |
| Learning dependency strength from traces without labels exists | AID (ASE'21; CE 0.327 vs 0.603 on Huawei, Table III p.8) |
| Graph propagation with co-location/deployment edges exists (supervised) | DéjàVu (FDG with deployment edges, pp.3-4), DiagFusion [abs], Xie et al. hypergraph (A29-A30) |
| LLM agents for RCA exist | RCAgent, RCACopilot, MicroRCA-Agent, AURORA, Roy et al. [abs], mABC [abs] |
| Multimodal RCA exists | Eadro [abs], Nezha [abs], DiagFusion [abs], CHASE, DeepHunt |
| RCA under missing traces / blind spots exists | TORAI [abs], LatentScope [abs] |
| Cascade theory exists | Motter-Lai (overload), Buldyrev (interdependent percolation), Kempe (independent cascade) [abs], Goyal (learning influence probabilities) [abs] |

**Consequence:** "label-free", "early warning", "propagation-aware", "multimodal" and "LLM explanation" are each **not** novel on their own.
A project built on any of them as the headline will fail review (this is `REVIEW_REPORT.md` M1).

---

## 2. The gaps, ranked by (strength of evidence) x (fit with what we built) x (chance of a clean result)

### G1. Nobody reports RCA accuracy conditioned on whether the root cause is the loudest service  **[strongest; core]**

**Statement.** Every RCA paper we read reports one pooled accuracy. None splits cases by where the root cause sits in the
symptom ranking. Yet several papers show, independently, that pooled numbers are dominated by easy cases in which the root
cause is simply the most anomalous service, where no propagation reasoning is needed.

**Evidence across papers**
| Paper | What it shows | Page |
|---|---|---|
| Fang et al. 2025 | 68% of 737 public cases are Type I (symptoms only in the injected service); a rule-based alert counter (SimpleRCA) matches or beats SOTA on 10 public datasets | Tables 2-3, pp.6-7 |
| Fang et al. 2025 | on their harder benchmark SimpleRCA still has the **highest Top@5 (0.80)** of 12 methods | Table 5 p.14 |
| Pham et al. ASE'24 | most causal-graph RCA methods no better than random on 4 benchmarks; simple methods better | p.6 |
| CIRCA KDD'22 | strongest baseline on 99 real failures is plain NSigma (AC@1 0.323 vs CIRCA 0.404) | Table 3 p.7 |
| PetShop CLeaR'24 | ranked correlation competitive with or better than graph/SCM learners; target is a graph leaf (no confounding) | Tables 3, 8; p.12 |
| DeepHunt TOSEM | reconstruction error alone puts the root first in about 70% of 63 cases | p.7 |
| CausalRCA JSS'23 | only +6.7% / +9.4% relative Avg@5 over PC/GES/LiNGAM + PageRank; loses AC@1 in several cells | Tables 3-4 pp.8-9 |
| "Graph structure" 2026 [rev] | graph model beat flat model by 0.003 Avg@5 (p=0.844); no-telemetry prior reaches Avg@5 0.488 | REVIEW_REPORT 3.3 |

**Who comes closest, and why it does not close the gap.** Fang et al. define Type I/II/III but use it only to *describe datasets*;
they never report method accuracy per type. Pham et al. vary data scale and fault time, not symptom rank. Nobody tests the
hypothesis "propagation modelling helps only when the root is not the loudest".

**Our own evidence.** Plain "most abnormal service" is our best method (A@1 0.46 vs full 0.31-0.34, random 0.22, 17 services);
the full method is near random at 50-200 services (`FIXES_AND_TESTS.md` 5.1-5.2). Death Star crash: the callers' error logs jumped
30x while the stopped root simply vanished, so ranking by abnormality blamed the victims (`RCA_AND_CASCADE_SIMPLE.md` 5).

**What a solution must show (acceptance criteria).**
1. A stratification rule computed **without** labels for the method but **with** the injected root for evaluation:
   symptom rank of the root among services (rank 1 = Type I; root silent = Type II; another service louder = Type III), using Fang's
   threshold (fault window > 2x pre-fault mean) so it is comparable.
2. Accuracy (A@1, A@3, MRR) **per stratum**, with 95% bootstrap CIs clustered by (fault type, target service).
3. Baselines that must be present: no-telemetry prior, random, SimpleRCA, NSigma, BARO, plus at least one graph method (MicroRCA-style PageRank or CIRCA).
4. Falsifiable hypothesis: *in Type III cases, propagation-aware ranking has higher A@1 than the best non-graph baseline; in Type I it does not.*
   Either outcome is a finding.

**Feasibility.** High. Needs RCAEval RE2 (public, CC-BY, download approval) and/or our OTel/Death Star runs. Stratification is a few lines of analysis code.

**Reviewer attacks and answers.**
| Attack | Answer |
|---|---|
| "Stratification uses ground truth" | It is used only to report results, never by the method; same as reporting per fault type |
| "Type thresholds are arbitrary" | Use Fang's rule for comparability and report a sensitivity sweep (1.5x, 2x, 3x) |
| "Few Type III cases" | Report counts per stratum; RCAEval RE2 has 270 cases, Fang says about 14% Type III across public data (Table 3) - expect about 35; add our own runs |

---

### G2. No RCA pipeline is evaluated at a stated operating point (false alarms per hour, detected vs given fault time)  **[strong; core]**

**Statement.** Benchmarks hand the method the fault time and evaluate only faulty windows. No read paper reports, for an
RCA pipeline, (a) how many root causes it invents on healthy traffic per hour, or (b) its accuracy when the fault time comes
from its own detector rather than from the injection log.

**Evidence across papers**
| Paper | What it shows | Page |
|---|---|---|
| PetShop | **all** evaluated methods fabricate root causes on normal data | p.12 |
| Pham et al. | NSigma on Train Ticket Avg@5 about 0.81 at the exact time vs about 0.03-0.12 when 60 s late | Table 5 p.7 |
| CIRCA | analysis delay is a fixed assumption (t_delay = 5 min) | p.5 |
| Fang et al. | 84.4% of injections produced no user-visible anomaly, so "silent" periods are the norm | p.13 |
| Seer | accuracy given without a false-alarm rate or lead time | p.2 |
| MicroHECL | deployment numbers without a false-alarm rate; failures that show no metric anomaly are missed | p.9 |
| BARO [abs] | the only one that targets robustness to inaccurate detection (end-to-end change-point detection) | abstract |
| Eadro [abs] | integrates detection and localization, but supervised | abstract |

**Who comes closest.** BARO (robust to detection errors) and Eadro (joint) [abs]. Neither, from the abstracts, reports false alarms per hour on
healthy traffic or a detected-vs-given comparison; this must be checked when BARO is read in full.

**Our own evidence.** The old detector raised 215 false-alarm episodes per hour on real healthy OTel traffic; the calibrated one raised
0 in 32 minutes. But it caught only 17-23% of injected root slowdowns at 1 alarm/hour and 38-47% at 5/hour, and the curve is flat in fault size
(`FIXES_AND_TESTS.md` 2, 4). Only 5 of 16 services have enough spans per 15 s window to be monitorable (section 3).

**What a solution must show.**
1. A detection-sensitivity curve: recall of the root vs false alarms per hour (ROC-style "operating curve"), on real healthy traffic held out from calibration.
2. RCA accuracy reported twice: with the fault time **given** (benchmark convention) and **detected** (deployment convention), and the gap between them.
3. A monitorability report: fraction of services with enough data per window, and accuracy restricted to monitorable roots.
4. Falsifiable hypothesis: *at 1 false alarm per hour, end-to-end A@1 of every method drops by at least X relative to given-time A@1.*

**Feasibility.** High; this is mostly our existing calibrated detector and `replay` harness, plus real faults.

**Reviewer attacks and answers.**
| Attack | Answer |
|---|---|
| "32 min of healthy data is too short" | Collect hours; report false alarms with a Poisson CI; calibrate on one slice, test on another |
| "Your detector is weak, so this is about your detector" | Run the same protocol on BARO/NSigma; the point is that nobody reports it |
| "Healthy is assumed" | State it; show no SLO breach during the slice |

---

### G3. Victims are louder than the root, and silence is a symptom: label-free root-vs-victim signals are untested  **[medium-strong; core method piece]**

**Statement.** Methods rank the most anomalous service. In real faults the root can be quieter than its callers (it waits
or disappears), so a ranking needs signals that separate *own* fault from *inherited* fault. Self-time (exclusive latency) and
liveness/absence are cheap, label-free candidates. No read paper evaluates them as root-vs-victim discriminators.

**Evidence across papers**
| Paper | What it shows | Page |
|---|---|---|
| Fang et al. | "signal-loss blind spots" (cessation of telemetry not read as a signal) and modelling assumptions that faults increase event frequency (Nezha) are failure modes of SOTA | p.17 |
| Fang et al. | Type III cases: stronger symptoms in services other than the injected one; "symptom drift" with deeper chains | pp.7, 14 |
| Soldani and Brogi | topology-only graphs miss anomalies caused by co-hosted services | p.27 |
| MicroHECL | some availability issues show no metric anomaly at all | p.9 |
| DeepHunt | needs propagation-aware scoring because reconstruction error alone misranks about 30% | p.7 |
| Chain-of-Event | without learned weights an event graph reaches only 17.1% top-1 (proprietary) | Table 2 p.10 |

**Who comes closest.** TORAI and LatentScope [abs] handle missing traces / unobservable candidates (blind spots), not victim-vs-root
inside visible services. MicroRank/TraceRCA [abs] use trace coverage ("more abnormal, fewer normal traces through it"), which is a
related discriminator and must be a baseline.

**Our own evidence.** `selftime` ranking: A@1 0.39 / 0.21 / 0.29 / 0.36 at 50 / 100 / 200 / 500 services vs `full` 0.13 / 0.05 / 0.06 / 0.00
(`FIXES_AND_TESTS.md` 5.2), but not consistent at 17 services (0.34 vs 0.46). Death Star: with `container_up` the root was ranked first;
without it, the callers were blamed (one run).

**What a solution must show.**
1. Ablation per stratum (G1): ranking by abnormality vs abnormality + self-time vs + liveness, on Type I and Type III separately.
2. A case set that includes "root keeps running but slows/errs" (where liveness does not help) - currently untested.
3. Falsifiable hypothesis: *self-time raises A@1 on Type III cases and does not lower it on Type I.*

**Feasibility.** Medium-high; features exist. Needs real slow/erroring faults (OTel feature flags, `docker pause`, CPU limit) with approval.

**Risk.** Self-time needs traces with span timing; services without traces get no benefit (state as a limitation; TORAI covers that space).

---

### G4. Cascade-risk "forecasting" is never evaluated against the trivial structural rule, with lead time and calibration  **[medium; second task]**

**Statement.** Papers that predict propagation either are supervised (Seer), simulation-only (Unyi), forecast metric values rather than
failures (STMformer), use proprietary data (Li 2026), or estimate edge strength without forecasting (AID). None defines the task as
"at the alarm, which not-yet-affected services will degrade, and how far ahead", and none compares with "callers of a failing service"
(structural rule) and persistence, with calibration (Brier/ECE) and lead time.

**Evidence across papers**
| Paper | What it shows | Page |
|---|---|---|
| Seer | supervised, own apps, no lead time or false-alarm rate | pp.2-4 |
| Unyi et al. TNSM'25 | GNN regresses a model-checker value from its own inputs; real traces left to future work | pp.11-16 |
| STMformer | forecasts metrics; no failure labels; no persistence baseline; inconsistent ablation | Tables 1-3 |
| AID | edge strength, not a forecast; 89% of labels "strong", no constant baseline | Tables II-III |
| Li 2026 | noisy-OR cascade risk identical in form to ours; proprietary, inconsistent numbers | Eq.21 p.10 |
| Liu et al. (Mamba) | the only read paper that reports calibration (ECE/Brier) for a risk output | Table 2 p.7 |
| Soldani and Brogi | lists predicting degradations as a future direction (2021) | p.28 |
| diffusion2025 [abs] | **claims** calibrated uncertainty for failure-propagation prediction from traces (weak venue, abstract only) | abstract |
| container2023 [abs] | cascade fault detection learned from historical faults (supervised) | abstract |

**Who comes closest.** diffusion2025 [abs] (calibrated propagation prediction claim) and SuanMing (unread). Both must be read before we claim this gap.

**Our own evidence.** Learning edges across incidents: AP 0.16 -> 0.51 in a 17-service app (oracle 0.53, structural rule 0.34) but mixed at 100 services;
lead time exists only for **slow** cascades; synthetic check: risk AUROC equals prior-only and the structural rule (`FIXES_AND_TESTS.md` 6; `REVIEW_REPORT.md` T3).

**What a solution must show.**
1. Formal task: at alarm time t0, predict for each not-yet-anomalous service whether it degrades within horizon H; ground truth from an
   **independent** signal (SLO breach or trace error status), never from our own detector (avoid circularity).
2. Baselines: structural rule, persistence, uniform-prior noisy-OR, learned noisy-OR, (optional) Hawkes as in MHP-RCA [abs].
3. Metrics: AP (victims are rare), AUROC, Brier and reliability curve, and lead time; results split by cascade speed (fast vs slow).
4. Falsifiable hypothesis: *learned edge probabilities beat the structural rule on AP for slow cascades; nothing beats it for fast ones.*

**Feasibility.** Medium. Needs real multi-service cascades; the OTel demo's feature flags may give some. Risk: few real victims per incident.

---

### G5. Propagation channels other than calls, and common causes, are unhandled in label-free edge learning  **[medium; extension]**

**Statement.** Label-free edge learning (AID, our EdgeLearner) uses call edges only and treats co-movement as propagation, so a load spike
or a shared host that hits several services at once looks like propagation. Papers that model co-location or sibling channels are supervised.

**Evidence:** DéjàVu deployment edges help (MAR -3% to -31% without graph aggregation, Table 3 p.8, supervised); Xie et al. group relations
(Avg@3 +0.08 to 0.14, Table II p.8, single run); STMformer same-host module (Table 3 p.8, one run, inconsistent); Soldani p.27; MicroHECL:
traffic propagates upstream-to-downstream, latency and errors downstream-to-upstream (Table I p.4); `REVIEW_REPORT.md` M5 (no common-cause handling);
Goyal 2010 [abs] shows influence probabilities need many observations per edge, matching our "40 incidents too few for 143 edges".

**What a solution must show.** An ablation with co-host edges and direction-by-anomaly-type, on faults that hit a shared host (CPU or memory
stress on a node), with ground truth from the injection. Hypothesis: *co-host edges raise A@1 on node-level faults and do not hurt service-level faults.*

**Feasibility.** Medium-low for the deadline: needs node-level faults on our EC2 hosts (approval) and enough incidents per edge.
Keep as "extension / future work" unless time allows.

---

### G6. Explanations are not checked for faithfulness  **[low-medium; optional]**

LLM RCA papers are judged by text similarity, an LLM judge, or human helpfulness (RCAgent 2.92 of 5, Table 5 p.7); MicroRCA-Agent shows a hallucinated
trace in a bad case (p.16); AURORA reports a 3% hallucination figure in a paper with inconsistent numbers. Non-LLM methods give rankings with no explanation
check. yRCA (explcascade2024 [abs]) explains cascades from logs but needs app instrumentation. Gap: a cheap automatic faithfulness check (every claim in an
explanation maps to a measured feature/value present in the input), as RCAgent's evidence fuzzy-match filter does (p.4). Low effort with templates; claim
"faithful by construction", not "helps operators", unless a user study is run.

---

## 3. Things that look like gaps but are NOT (do not build the project on them)

| Tempting claim | Why it fails |
|---|---|
| "No label-free RCA" | CIRCA, DeepHunt, CausalRCA, TraceRCA [abs], BARO [abs], TORAI [abs] |
| "Cascade prediction is unexplored" | Seer, Li 2026, Unyi, container2023 [abs], diffusion2025 [abs], SuanMing |
| "We are the first to use co-location" | DéjàVu, DiagFusion [abs], Xie et al., MicroRCA [abs] (attributed graph with machines) |
| "Blind spots / missing traces are ignored" | TORAI, LatentScope [abs] |
| "LLM agents for RCA are new" | RCAgent, RCACopilot, Roy et al. [abs], mABC [abs] |
| "Benchmarks are too easy" as our contribution | Fang et al. and Pham et al. already said it; our delta must be the *per-stratum* evaluation (G1) and the operating point (G2) |

---

## 4. Recommended project (what survives review and grading)

**Working title.** *When Does Propagation Help? A Label-Free, Operating-Point-Aware Evaluation of Root-Cause Localization and Cascade Early Warning in Microservices*

**One-sentence problem statement.** Public RCA results are pooled over easy cases and measured with the fault time given, so it is unknown when
propagation-aware, label-free methods help in practice; we measure this per symptom stratum and at a fixed false-alarm budget, and test whether
cascade risk adds warning time over a structural rule.

**Contributions (each tied to a gap and falsifiable):**
1. **Evaluation protocol (G1 + G2).** Symptom-rank strata, no-telemetry prior, SimpleRCA/NSigma/BARO/graph baselines, clustered CIs, given vs detected time,
   false alarms per hour on held-out healthy traffic, monitorability. Applied to RCAEval RE2 and our OTel (and Death Star) fault runs.
2. **Root-vs-victim signals (G3).** Label-free self-time and liveness features; ablation per stratum shows where they help.
3. **Cascade early-warning task (G4).** Formal definition with independent ground truth, compared with structural and persistence baselines,
   calibrated, split by cascade speed; learned edge probabilities across incidents with their data requirements stated.

**Research questions**
| RQ | Hypothesis (falsified if) |
|---|---|
| RQ1 Where do propagation-aware methods beat simple ones? | Graph-based A@1 > best non-graph A@1 in Type III; not in Type I (falsified if CIs overlap in Type III) |
| RQ2 What does the operating point cost? | At 1 false alarm/h, detected-time A@1 is lower than given-time A@1 for all methods (falsified if not) |
| RQ3 Do self-time and liveness separate root from victim? | They raise Type III A@1 without lowering Type I A@1 |
| RQ4 Does learned cascade risk give earlier warning than the structural rule? | AP(learned) > AP(structural) for slow cascades with lead time > 0 |

**Minimum to pass vs nice to have**
| Must have (grading-critical) | Nice to have |
|---|---|
| RCAEval RE2 on 2 systems (OB, SS) with the baselines above | Train Ticket (large; cost per Pham) |
| >= 30 real fault runs on the OTel demo, >= 3 fault types, >= 5 target services | Death Star with more fault types |
| Per-stratum tables with clustered bootstrap CIs | Hawkes baseline for RQ4 |
| Healthy-traffic false alarms over >= 2 hours with a CI | Co-host channel (G5) |
| Full related-work section citing section 1 above and stating the delta | Explanation faithfulness check (G6) |
| Threats to validity, artifact release (code, per-case CSVs, seeds) | Human-time study |

**Pre-empting the reviewer (maps to `REVIEW_REPORT.md` section 5).** M1 novelty -> section 3 of this file and the delta paragraph; M2 synthetic -> RCAEval + real runs;
M3 strawman baselines -> BARO, NSigma, SimpleRCA, CIRCA, PageRank, prior; M4 components do not contribute -> RQ1 tests exactly where they do; M6 detector ->
RQ2; M7 Task B undefined -> RQ4 definition with independent labels; M11 statistics -> clustered CIs, >= 30 cases per stratum where possible; M12 benchmark validity -> strata and prior.

---

## 5. Must read before writing (could close or weaken a gap)

| Paper | Why | Gap at risk |
|---|---|---|
| BARO (FSE'24) | robust to detection error; may report operating points | G2 |
| RCAEval (WWW'25 companion) | dataset details, baseline code, case counts | G1 |
| TraceRCA (IWQoS'21) and MicroRank | trace-coverage discriminator, label-free | G3 |
| Latent Diffusion propagation (2025) | claims calibrated propagation prediction | G4 |
| SuanMing (ICPE'21), Sage (ASPLOS'21) | degradation prediction; counterfactual RCA | G4 |
| TORAI (FSE'26), LatentScope (KDD'24) | blind spots / limited observability | G3 boundary |
| Explaining cascading failures from logs (SPE'24, yRCA) | cascade explanation | G6 |
| Goyal 2010, Gomez-Rodriguez 2010 | theory for learning propagation probabilities | G4, G5 |
| Characterizing microservice dependency (SoCC'21, Alibaba traces) | do real call graphs have heterogeneous edges? | G4 assumption |
| Metastable failures (HotOS'21) | cascades that persist after the trigger | G4 framing |
| "Does graph structure earn its place?" 2026, Kintsugi 2026 [rev] | direct competitors to G1's framing | G1 |

All of these need PDFs (paywalled or not yet fetched). Downloads need the user's permission; none were made for this document.

---

## 6. Confidence

| Gap | Confidence it is open | Main risk |
|---|---|---|
| G1 per-stratum evaluation | high | "Graph structure earns its place" [rev] may already stratify; read it first |
| G2 operating point | high | BARO may report false alarms; read it |
| G3 root-vs-victim signals | medium | TraceRCA/MicroRank discriminators are close; must be baselines |
| G4 cascade early warning | medium-low | diffusion2025 and SuanMing unread |
| G5 channels + common causes | medium | supervised work is close; feasibility for us is low |
| G6 faithfulness | low-medium | non-LLM explanation literature not surveyed |
