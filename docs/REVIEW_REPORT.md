# Honest review of the project: RCA + cascading-failure risk for microservices

Prepared 2026-10-07 for Royson Salis and team (Bharath, Dhanush, Anish).
Systems reviewed: **microservice-mapper** (the product) and **rca-lab** (the research harness).
Everything below is tagged with where it comes from, so you can tell evidence from opinion:

- **[T]** a test I ran myself (scripts in `experiments/`, raw results in `docs/experiments/`)
- **[F]** I read the full text of the paper (your local PDFs)
- **[A]** I read only the abstract/metadata, retrieved from OpenAlex/arXiv/Zenodo (verified to exist)
- **[D]** your own documentation (README / wiki) for microservice-mapper. I did **not** audit its source code line by line
- **[J]** my judgement, i.e. an opinion, not a measurement

I did not and cannot claim to have read 50+ papers in full. I verified **65** papers exist (matrix in Appendix A,
`docs/literature/literature_matrix.csv`), read **~21 in full** (your two folders), and read abstracts for the rest.
Nothing here is cited from memory without being flagged. Items I could not verify are listed in Appendix B.

---

## 0. Read this first

1. **The idea is publishable only if you reframe it.** "Predicting cascading-failure risk is under-explored" is **not true**.
   At least eight verified works already predict or model failure propagation (AID 2021, an explainable-GNN fault-forecasting
   paper in IEEE TNSM 2025, a container cascade-fault paper 2023, Li 2026 in your own folder, Seer, Sage, MicroHECL, Groot). [A][F]
2. **"Unlabeled RCA" is also not unique.** BARO (2024), TORAI (2026) and Sage are label-free; DeepHunt is *label-light* (self-supervised pretraining,
   reaches 90+% A@5 with merely 1% labeled failure samples, plus operator feedback labels online). [A][F]
3. **Right now you have zero real evidence that your method works.** Every accuracy number so far is from a synthetic generator that
   encodes the same assumption the method makes. That is circular. Do not put those numbers in a paper as results. [T]
4. **On synthetic data the cascade parts of the method do nothing measurable.** Full method MRR 0.97, without the cascade term 0.97,
   without the "explained-away" term 0.97, simple PageRank 0.95. Only temporal precedence (first to deviate) matters (0.90 without it). [T]
5. **The "learned" propagation probabilities barely learn.** 82% of edges stay exactly at the 0.5 prior at the end of an incident. [T]
6. **The risk score is no better than a trivial rule.** AUROC of cascade risk about 1.00; the prior-only version (no learning) is also
   1.00; the rule "callers of a failing service are at risk" scores 0.90 to 1.00. [T]
7. **The detector, as built, false-alarms heavily on real healthy traffic.** On 119 windows of real OTel-demo traffic with no injected
   fault, 43.5% of service-windows were flagged and about 7 services per window. A simple fix (log-latency only, z=8, persistence 3)
   drops that to 0.4%, but the cost in missed real faults is unmeasured. [T]
8. **Public labelled benchmarks exist and are free** (RCAEval: 735 cases, 3 systems, CC-BY). Use them. Two 2026 papers also say these
   benchmarks are easier than they look and that simple methods match state of the art. You must beat *simple* baselines, not weak ones. [A]
9. **Your reading notes contain two claims that the papers do not support** (Chain-of-Event is *supervised*; Pham et al. does not prove
   an event-based approach is right). Fix before your professors see them (section 6). [F]
10. **Realistic target for "a few days":** an honest empirical paper, "does label-free, propagation-aware modelling help RCA and early
    warning? an open evaluation", with RCAEval + your own OTel fault-injection runs. Section 8 and 10 give the design and a day-by-day plan.
11. **Some of what you want is not doable in days** (human debugging-time study, many architectures, a trained GNN with real cascade
    labels). Section 10 says what to cut.
12. I need three decisions/permissions from you (section 11): dataset downloads, fault injection, and the framing.

---

## 1. What the two systems are

**microservice-mapper** [D]: a Node/TypeScript + React app. It SSHes into EC2 hosts, reads docker-compose + docker stats + `/proc/net/tcp`,
builds a "hybrid" dependency graph (declared edges from compose, observed edges from TCP/log parsing), scores root causes with a
**hand-weighted additive rule** (earliest anomaly +0.30, container exited +0.35, observed edge +0.20, downstream correlation +0.15),
and optionally reads per-service Isolation Forest scores from a Python sidecar. It is a product/engineering tool.

**rca-lab** [T]: the research harness I built with you. Python. Collects from Jaeger (traces), optional Prometheus/Loki, or SSH (allowlisted
read-only docker commands). Unsupervised robust-z detector, edge-probability estimator, noisy-OR "cascade risk", a ranking that combines
anomaly strength, temporal precedence, "blast radius" and an explained-away penalty, plus ablations, baselines, statistics, and a dashboard.

**What "the concept" is, precisely** (use this wording, it is what reviewers will test):

- **Task A, root-cause localization.** Given multivariate telemetry up to time *t* for services *S* and a call graph *G*, output a ranking
  of services by how likely each is the fault origin. Metric: Avg@k / A@k, MRR.
- **Task B, cascade-risk forecasting.** Given the same input and the set of services currently anomalous *A(t)*, output for every currently
  healthy service *v* the probability R_v(t, h) that *v* becomes anomalous within horizon *h*. Metrics: AUROC / average precision,
  Brier score and calibration error, and **lead time** (how many seconds before the real degradation the alarm fires).
- **Event-level variant** (from your Chain-of-Event reading): an *event* is (service, signal, direction), e.g. "latency up on cart".
  Risk is then defined per event, and the graph is over events, not services.
- **Task C, explanation.** Text that states which evidence supports the ranking. It must never change the ranking.

Your paper currently has Task A and a *claim* about Task B but **no evaluation of Task B at all**, so the distinguishing feature is
the least supported part.

---

## 2. Where it is useful, what it can do, where it fails

### 2.1 Useful when [J]
- Small to mid-size Docker-Compose / Kubernetes demo or lab systems where you can export OpenTelemetry traces to Jaeger.
- Teaching, demos, and as an *experiment harness* for studying RCA on live telemetry.
- Quick triage of "which service deviated first and who depends on it", as a hint, not an oracle.

### 2.2 Capabilities (verified working) [T]
Real traces pulled from the OTel demo (about 10k spans, 14 services, correct call graph recovered); SSH sampling of 24 containers (CPU, memory,
network, error-log counts); project management and three data methods; ablations/baselines/statistics export.

### 2.3 Where it fails or is unproven

| Area | Failure / limit | Source |
|---|---|---|
| Detector | 43.5% of service-windows flagged on healthy real traffic; 7 services/window | [T] |
| Cascade learning | 82% of edge probabilities equal the prior | [T] |
| Cascade value | ablations tie; risk == prior-only == structural rule | [T] |
| Real faults | none run yet, so detection sensitivity and RCA accuracy on real faults are **unknown** | [T] |
| Prometheus on OTel host | times out; no CPU/memory features, traces only | [T] |
| SSH mode | each sampling cycle about 40 s on 24 containers; adds load (host load average > 24 on 2 vCPU) so it perturbs what you measure | [T] |
| microservice-mapper TCP view | connections shorter than the 5 s poll are invisible; no real request tracing | [D] |
| microservice-mapper weights | 0.30/0.35/0.20/0.15 are hand-set, never fit or validated | [D] |
| microservice-mapper ML | features are CPU/mem/network only; HTTP latency/errors mostly null; "no labels, so flag-rate is not accuracy" | [D] |
| Both | train-on-incident problem: if the baseline window contains a fault the model learns it as normal | [D][J] |
| Both | assumes failures travel along observed call edges; shared infrastructure faults (node, network, DB) violate this | [J] |
| Both | only call-graph edges seen in sampled traces; rare edges are missing | [T][J] |
| Windows | App Control blocks scikit-learn's OpenMP DLL on this PC, so the Isolation Forest option does not load here | [T] |

**As a research subject on its own, microservice-mapper is a systems/tool contribution, not a research paper.** A tool/demo track could take it,
but only with a usability or overhead evaluation against Jaeger+Grafana. It has no accuracy evaluation.

---

## 3. What the closest published work does (and what that means for you)

### 3.1 The map of the field [A][F]
- **Surveys:** Soldani and Brogi (ACM CSUR 2022); Fu et al. (CSUR 2025, local); Wang and Qi 2024 (local); Pham et al. failure-diagnosis survey (TOSEM 2025); AIOps-in-the-LLM-era (CSUR 2025).
- **Graph/propagation RCA:** MonitorRank (unverified, see App. B), CloudRanger 2018, MicroRCA 2020, AutoMAP 2020, MicroHECL 2021, anomaly-propagation diagnosis 2021.
- **Causal RCA:** MicroCause 2020, CIRCA 2022, RCD 2022, CausalRCA 2023, "limited observability" 2024.
- **Multimodal / label-light RCA:** DiagFusion 2023, Nezha 2023, Eadro 2023, DeepHunt 2024 (self-supervised), BARO 2024, TORAI 2026, DéjàVu 2022 (supervised).
- **Event graphs:** Groot 2021, KGroot 2024, Chain-of-Event 2024 (supervised), MHP-RCA 2025 (Hawkes).
- **Cascade / propagation prediction:** AID 2021, TNSM fault-forecasting GNN 2025, container cascade-fault 2023, Li 2026, latent-diffusion propagation 2025, Seer 2018/19 (anticipates QoS violations), Sage 2021, STMformer 2024 (forecasting).
- **LLM / agents:** Roy et al. 2024, RCAgent 2024, mABC 2024, MicroRCA-Agent 2025 (local), OpenRCA 2.0 2026, AIOpsLab 2025.
- **Evaluation critiques:** Pham et al. 2024 ("How far are we"), "Rethinking evaluation" 2026, "Does graph structure earn its place" 2026.
- **Theory you are re-using without citing yet:** independent-cascade model (Kempe et al. 2003), learning influence probabilities (Goyal et al. 2010), inferring diffusion networks (Gomez-Rodriguez et al. 2010), cascade models (Motter-Lai 2002, Buldyrev et al. 2010).

### 3.2 Comparison with your concept (marks from the abstract or full text only; `?` = I cannot tell)

| Work | Label-free | Online stage | Forecasts future failures | Learns propagation weights | Multimodal | Open data/code | Basis |
|---|---|---|---|---|---|---|---|
| **DeepHunt** (TOSEM 2024) | label-light (self-supervised + 1% labeled failures; operator feedback labels online) | yes (online localization) | no | implicit (graph autoencoder) | yes | dataset D1 public | [F] |
| **Chain-of-Event** (FSE 2024) | **no** (trains on labelled historical incidents) | incident-time inference | no | yes (supervised link weights) | events from metrics/logs/traces | proprietary prod. data | [F] |
| **MicroHECL** (ICSE-SEIP 2021) | ? | yes (dynamic call graph) | no | no (analyzes propagation chains) | ? | ? | [A] |
| **Groot** (2021) | rule-based | yes (real-time event graph) | no | rules, not learned | yes | ? | [A] |
| **AID** (2021) | ? | ? | **predicts cascading impact via dependency intensity** | yes (intensity between services) | traces + series | ? | [A] |
| **Explainable GNN fault forecasting** (TNSM 2025) | no (trained GNN) | ? | **yes: fault probabilities with probabilistic propagation** | via simulation (MDP) | ? | ? | [A] |
| **Li 2026** (Discover AI; your folder) | partly (self-supervised pretraining) | yes (claims real-time) | **yes: cascade prediction with path probabilities** | yes | ? | **no** (proprietary; code/data "will be released") | [F] |
| **Container cascade fault** (2023) | no (historical faults) | yes | detection of cascade | yes (spatial-temporal) | ? | ? | [A] |
| **TORAI** (2026) | **yes** | ? | no | no | yes | ? | [A] |
| **BARO** (2024) | **yes** | yes (online change point) | no | no | metrics | yes (RCAEval) | [A] |
| **Seer** (arXiv 2018) | ? | yes | **anticipates QoS violations** | no | traces | ? | [A] |
| **MicroRCA-Agent** (2025) | Isolation Forest + LLM | challenge pipeline | no | no | yes | code released | [F] |
| **rca-lab (yours)** | yes | partly (incremental windows) | **claimed, untested** | yes, but 82% prior | traces (+SSH metrics) | yes | [T] |

**Honest reading:** the *combination* (label-free + online + forecasting + learned propagation + open) is not in this table as one verified work, but that
is a weak novelty argument, because each ingredient exists and the combination is only as valuable as the evidence that it works. Right now the evidence is absent.
I cannot prove no such combined paper exists. Section 8 lists the searches to repeat before submission.

### 3.3 Two papers that decide how you write the paper
- **Pham et al., ASE 2024 [F].** Evaluates 9 causal-discovery and 21 RCA methods. "No method stands out in all situations"; and
  **performance on synthetic data may not reflect real systems**. This is the citation a reviewer will use against our synthetic results.
- **Rethinking RCA evaluation, PACMSE 2026 [A]:** simple rule-based methods match or beat state of the art on four widely used benchmarks.
  **"Does graph structure earn its place?" (2026 [A]):** in a controlled test on RCAEval, the graph model beat the flat model by 0.003 Avg@5 (p=0.844);
  a ranker reading *no telemetry* reaches Avg@5 = 0.488 because faults are injected into only 5 services per system. So **Avg@5 is a weak metric: report Avg@1/@3/MRR and a no-telemetry prior baseline.**

---

## 4. Our own evidence (every test I ran)

All raw files are in `docs/experiments/`. Synthetic = our generator; live = real OTel-demo traffic on your EC2.

| # | Test | Result | What it means |
|---|---|---|---|
| T1 | 10-run synthetic comparison (hard case; latest run in `results/synthetic_sanity_hard`) | A@1: full=ablations=PageRank=1.00; earliest 0.40 (p_Holm 0.19), random 0.60 (p_Holm 0.63), anomaly-only 0.10 (p_Holm 0.027) | only the weakest baseline is significantly worse; 10 runs cannot separate the rest |
| T2 | Robustness sweep, 36 configs (p_propagate 0.3/0.6/0.9, noise x1/x3, edges 0/30/60% missing, victim louder or not), 20 runs each | MRR: full 0.97, no_cascade 0.97, no_explained 0.97, **no_precedence 0.90**, PageRank 0.95, earliest 0.92, anomaly-only 0.81, random 0.73. Baseline beats full by >0.05 in 0 of 252 comparisons | cascade/explained-away add nothing; precedence is the active ingredient; but the generator was built by us |
| T3 | Cascade-risk predictiveness (who fails next) | AUROC risk 0.99-1.00 = prior-only 0.99-1.00; structural rule 0.90-1.00; random 0.44-0.64 | the model is no better than "callers of a failing service" |
| T4 | Edge probabilities at end of incident | synthetic: 82% of edges exactly at prior 0.5; live healthy: 22% | "learned" probabilities are mostly the prior |
| T5 | **False alarms on real healthy traffic** (119 windows, 16 active services, 30-window baseline) | current detector: flag rate 0.435, any flag in 89% of windows, 7.0 services/window | detector unusable as is |
| T6 | Detector fixes on the same data | no span_rate: 0.204; baseline-quantile log-scale: 0.201; latency-only log z=5/pers3: 0.069; **z=8/pers3: 0.004** | false alarms are fixable; sensitivity cost unmeasured |
| T7 | SSH sampler on 24-container host | about 43 s per cycle; host load average >24 on 2 vCPU | observation perturbs the system under test |
| T8 | OTel host Prometheus via Grafana proxy | 504 on every query | only trace-derived features available live |

**Caveats on T5/T6 (be fair to the system):** the baseline was only 7.5 minutes of a freshly started demo (warm-up transients, bursty load generator);
I have no independent proof that the demo was fault-free, because it is a live system I did not instrument for ground truth. These numbers show the detector
needs calibration, not that the idea is wrong. They are also exactly the kind of number a reviewer will ask for.

---

## 5. The reviewer-2 report (written as a stern, hyper-negative reviewer would)

> **Paper:** "Probabilistic Cascading Failure and Agent Assisted Root Cause Analysis for Microservice Systems"
> **Recommendation: Reject** (would become *major revision* only if M1-M6 are fixed).

**Summary of claims.** The authors propose an unsupervised pipeline that detects anomalies in live telemetry, learns failure-propagation
probabilities between services, ranks root causes, predicts the cascading-failure risk of each service, and uses an LLM agent for explanations.
They claim it reduces debugging time, is accurate, and works on any architecture.

**M1. Novelty is overstated and the stated gap is false.** The related-work section claims early identification of cascading-failure risk "is not
sufficiently understood". AID, a TNSM 2025 GNN fault-forecasting paper, Li 2026, Seer, Sage, MicroHECL and Groot all address prediction or modelling of failure
propagation. Label-free RCA is addressed by BARO, TORAI, Sage and DeepHunt. LLM-agent RCA by RCAgent, mABC, Roy et al., MicroRCA-Agent. The paper cites none of
the propagation-prediction works. The delta over any of them is never stated.

**M2. No empirical evidence.** The results are produced by a synthetic generator written by the authors, whose failure-propagation mechanism is the model's own
assumption. Success on it is tautological. Pham et al. (ASE 2024) explicitly warn that synthetic performance does not transfer.

**M3. Strawman baselines.** The comparisons are against random ordering, "earliest anomaly" and "highest anomaly score", and a self-implemented PageRank.
There is no comparison with BARO, CIRCA, RCD, MicroRCA, MicroCause, DeepHunt, Chain-of-Event, or even the 15 reproducible baselines shipped with RCAEval.

**M4. The proposed components do not contribute.** Removing the cascade term, or the explained-away term, changes nothing; only a decades-old heuristic
(first anomaly wins) matters. The paper's headline mechanism is therefore unsupported by its own ablation.

**M5. "Learned" propagation probabilities are priors.** The estimator is a Beta-style smoother with an arbitrary prior (0.5, strength 2) and typically a handful of
observations per edge; most edges never leave the prior. Correlation of anomaly onsets within a lag window is presented as propagation probability, with no handling
of common causes (load spikes, shared hosts), no identifiability argument, and no sensitivity analysis. Goyal et al. need many observations to fit such probabilities.

**M6. The detector is uncalibrated.** Thresholds are arbitrary. On healthy production-like traffic it flags a large fraction of windows. Taking the maximum z-score over
many features inflates the false-positive rate (a multiple-comparison problem). No detection precision/recall or detection-delay results are reported.

**M7. The distinguishing task, cascade-risk prediction, is never evaluated.** There is no forecasting task definition, no ground truth of which services were actually
affected, no calibration, no lead time. The one internal check shows the risk score equals its prior-only version and a trivial structural rule. Labels, if derived from the
same detector, would be circular.

**M8. "Live/real-time" is asserted, not shown.** No end-to-end latency (fault to correct ranking) is measured. Windows are 15-30 s; trace ingestion adds delay;
evaluation is offline over recorded windows.

**M9. RQ1 is untestable as posed.** "Reduce debugging time compared with conventional approaches" needs a human study or a defined conventional workflow. Neither exists.

**M10. Generality is not tested.** "Architecture independent" is claimed from at most one or two small demo applications with a handful of injected fault types. RCAEval-style
benchmarks inject faults into only five services per system; per-fault repetitions are not independent samples.

**M11. Statistics are thin.** Ten runs, Wilcoxon tests, many comparisons. At n=10 the smallest possible exact two-sided p is 0.002, and Holm correction over seven comparisons raises it to about 0.014, so power is minimal; no confidence intervals on detection delay;
repetitions of the same fault-service pair are treated as independent.

**M12. Benchmark validity is ignored.** Recent work shows simple rules match state of the art on public benchmarks and that Avg@5 has a high no-telemetry floor.
The paper reports none of the controls (no-telemetry prior, simple rules).

**M13. Observation perturbs the system.** The SSH sampling mode adds measurable load on the host under test. Overhead of the monitoring itself is never reported.

**M14. The LLM "agent" is unevaluated.** No evidence that explanations are faithful, no hallucination rate, no determinism, no comparison with a template. "Agent" overclaims if it
only rephrases a ranking.

**M15. Related-work table misdescribes prior art.** DeepHunt is described as static and non-live; its own paper has an online localization stage and an operator-feedback loop, and it is label-light, not label-free. Summaries rely on abstracts.

**M16. Reproducibility.** The closest competitor (Li 2026) is irreproducible (proprietary data, code "will be released"); this paper has an advantage if it releases everything but must then actually do so, with seeds, versions, and raw telemetry.

**Minor.** Inconsistent notation; units missing (seconds vs windows); the LaTeX table has an empty column; claims such as "outperforms" without tests; abstract numbers not traceable to a table.

### How to pre-empt each point (what you do about it)

| Point | Fix | Cost |
|---|---|---|
| M1 | Cite all of section 3; state delta explicitly; reframe as an evaluation-driven study | low |
| M2, M3, M12 | Use RCAEval RE1/RE2 + OTel runs; compare with BARO, CIRCA, RCD, MicroRCA (+ prior baseline, simple rules); report Avg@1/3, MRR | medium (needs downloads) |
| M4, M5 | Keep the ablations, report them honestly; fit or tune propagation estimation properly, or drop the claim | medium |
| M6 | Calibrate the detector on held-out healthy data; report false-alarm rate per hour and detection delay | low-medium |
| M7 | Define Task B formally; get ground-truth impact labels from independent signals (trace error status / SLO breach), report AUROC/AP, Brier, lead time vs structural, persistence, Hawkes | medium-high |
| M8 | Measure fault-to-ranking latency end to end | low |
| M9 | Rewrite RQ1 as algorithmic time-to-localization; mention human study as future work | low |
| M10, M11 | At least 2 systems; at least 30 cases per system; cluster-aware statistics; CIs | medium |
| M13 | Prefer tools mode; measure sampler overhead; report it as a threat | low |
| M14 | Drop "agent" or evaluate faithfulness with automatic checks; be modest | low-medium |

---

## 6. Corrections to your reading notes (`WHAT I GOT.docx`) [F]

| Note | Problem | Corrected statement |
|---|---|---|
| #5 Chain-of-Event gives "the exact probability of one event triggering another" and a way to do this label-free | CoE is **supervised**: it trains the event-causal graph on historical incidents with root-cause labels taken from SRE tickets; its NEG is a uniformly weighted fully connected graph used as the *starting point*; link weights are *learned from labels* and used for ranking, not exact trigger probabilities. The paper lists unsupervised/active learning as future work. | CoE is a *supervised* event-graph ranker; your label-free variant would be new relative to it, but then CoE is a reference, not a foundation, and you must show your weights are meaningful. |
| #11 Pham et al. "proves" PC/Granger fail on real systems and that an event-based approach is the right choice | Pham et al. report: most causal-inference RCA methods handle Sock Shop (38-46 metrics) and Online Boutique (49) within seconds, but take minutes to about an hour on Train Ticket (212 metrics); PC/FCI ran out of memory on a 50-node *synthetic* set and some methods exceeded 1-2 hour per-case limits; **NSigma and BARO (which learn no causal graph) are consistently the fastest**. They conclude no method is best everywhere and synthetic results may not transfer. They did **not** evaluate event-based methods. | "Causal-discovery RCA methods vary widely in cost and accuracy [Pham 2024]; we therefore evaluate lightweight alternatives empirically." Do not claim they prove your approach. |
| #3 "use an LLM instead of deep learning" | An LLM does not replace a detector; it cannot see raw telemetry reliably. The OTel AIOps benchmark (2026 [A]) found density-based deep models (DAGMM, Deep SVDD) detect well while reconstruction autoencoders collapse to predict-all-anomaly on most signals under its engineered features; LLMs were not the detector there. | LLM = explanation layer on top of a detector. Say so. |
| #1 MicroRCA-Agent "proven blueprint" | It is a *competition* pipeline (CCF International AIOps Challenge) with a challenge score (50.71), not a general accuracy result. | Use it as an architectural reference; do not cite it as proof of effectiveness. |
| #6 DeepTraLog and Nezha "contain ready-to-use faults and multimodal data" | I could **not** verify the hosting location or contents of either dataset in this session. | Verify before relying on them; RCAEval RE2 is a verified multi-source alternative. |
| file name | The PDF `Real-Time Observability and Failure Prediction in Kubernetes-Based Microservices.pdf` is actually the observability **survey** by Faseeha et al. (IEEE Access 2025). | Cite it as a survey, not as failure-prediction work. |
| Related-work table | DeepHunt "uses a static dataset instead of live telemetry" is unfair (it has an online stage and feedback loop). | Say DeepHunt is evaluated on recorded benchmark datasets; avoid "static". |

---

## 7. Data you can use (verified on Zenodo, CC-BY-4.0 unless noted) [A]

| Dataset | Content | Size | Notes |
|---|---|---|---|
| RCAEval RE1-OB / RE1-SS / RE1-TT | 375 cases total (125/system), metrics only, 5 fault types (CPU, MEM, DISK, DELAY, LOSS) | 31 / 79 / 280 MB | smallest; metrics only |
| RCAEval RE2-OB / RE2-SS / RE2-TT | 270 cases (90/system), metrics + logs + traces, 6 fault types | **1.2 GB** / 246 MB / **2.8 GB** | multi-source; the useful one for you |
| RCAEval RE3-OB / RE3-SS / RE3-TT | 90 cases, code-level faults | 191 / 102 / 242 MB | optional |
| OTel AIOps Benchmark (2026) | traces+metrics+logs, OpenTelemetry on EKS, Chaos Mesh injection | 63 MB | for detector comparison |
| PetShop (arXiv 2023) | performance-issue dataset | not checked | optional |

Caution (Kintsugi 2026 [A]): schema inconsistencies silently zero telemetry for most RE1 cases; faults only in 5 services per system.
Always run a **no-telemetry prior baseline** and check the data loaders.

---

## 8. What to change in the research design

### 8.1 Recommended framing [J]
**"Does label-free, propagation-aware modelling help root-cause localization and early warning? An open evaluation on live OpenTelemetry telemetry and RCAEval."**
This stays within what you can finish, survives the criticisms above whichever way results fall (a clear negative on the cascade term is still a finding),
and uses what you built (live adapter, ablations, statistics).

### 8.2 Rewritten research questions and falsifiable hypotheses

| RQ | Question | Hypothesis (falsified if...) |
|---|---|---|
| RQ1 | Detection quality of label-free detectors on real traffic | H1: calibrated detector keeps false alarms under X/hour with median detection delay under Y s (falsified if not) |
| RQ2 | Localization accuracy vs strong simple baselines | H2: proposed method has higher MRR/Avg@1 than BARO and a no-telemetry prior on RE2 (falsified if CIs overlap) |
| RQ3 | Does the propagation/graph term help? | H3: removing it lowers MRR on at least two systems (falsified otherwise; report either way) |
| RQ4 | Cascade-risk forecasting | H4: risk predicts future degradation better than the structural rule and persistence (AUROC/AP, Brier, lead time) |
| RQ5 (optional) | Explanation faithfulness | H5: every explained claim maps to a measured feature (automatic checks) |

### 8.3 Experiments
1. **RCAEval RE1/RE2 on Sock Shop and Online Boutique** (smallest sizes first), 5-fold or leave-fault-service-out, baselines via RCAEval's reference implementations
   (BARO, CIRCA, RCD, MicroRCA, etc.; MIT-licensed code) + prior baseline + simple rules + yours.
2. **Own OTel-demo fault-injection runs** (feature-flag faults injected outside the app; `rcalab record`): aim for 30+ runs across 5+ faults and 5+ services; repeat to get variance.
   Flag names must be verified in the demo's feature-flag UI (I have not).
3. **Cascade-risk evaluation (Task B):** ground-truth "affected services" from an *independent* signal (trace error status / SLO breach), not from your detector.
   Report AUROC/AP, Brier + calibration curve, lead time, vs structural, persistence, Hawkes (MHP-style), logistic regression on lagged features.
4. **Detector study:** robust-z, log-space robust-z, BOCPD (BARO), EWMA/CUSUM, STL residual, Isolation Forest, DAGMM/Deep SVDD. Report false alarms per hour and detection delay.
5. **Overhead and latency:** CPU/RAM of the collector, sampling load on the host, fault-to-ranking latency.

### 8.4 Models and approaches worth testing (and which to skip) [J]
| Role | Try | Skip / caution |
|---|---|---|
| Detection | robust-z (log-space), BOCPD, EWMA/CUSUM, STL residual, Isolation Forest | transformers/Mamba: no evidence they help here; the Mamba paper in your folder is a cost-sensitive classification study, not microservice RCA evidence |
| Deep detection | DAGMM / Deep SVDD (best semi-supervised models in the 2026 OTel benchmark); LSTM-AE only as a contrast | reconstruction AEs collapsed on several signals there |
| Localization | NSigma and BARO (simple, fastest), PageRank/random walk (MicroRCA-style), CIRCA, RCD, simple rules, no-telemetry prior | PC/GES/LiNGAM/NTLR on large metric sets (e.g. Train Ticket): minutes to an hour per case, some OOM, per Pham et al. |
| Propagation | learned edge strengths with explicit sensitivity analysis; Hawkes process (MHP-RCA idea) | GNN-based propagation: needs labels and large data; only as a stated upper bound |
| Explanation | structured-JSON LLM prompt over evidence (MicroRCA-Agent style) | free-text agent loops without faithfulness checks |
| Hardware | the RTX 5050 only matters for DAGMM/AE/GNN; keep VRAM capped | scikit-learn is blocked on this PC by App Control; use WSL2 or EC2 for ML runs rather than lowering Windows security (Smart App Control cannot be re-enabled without reinstalling Windows) |

### 8.5 Statistics and reporting
Per-case metrics; 95% bootstrap CIs; Holm-corrected paired tests; Cliff's delta; cluster repetitions by (fault, service); report variance across seeds;
publish per-case CSVs. Never report a metric without its baseline.

### 8.6 Threats to validity to write down
Injected faults are not production incidents; our detector thresholds were tuned by us; demo systems are small; sampled traces miss rare edges; observation overhead (SSH);
circularity if labels come from the detector; baseline implementations are ours or RCAEval's, not the original authors'; one cloud region/instance type.

---

## 9. The paper: structure, safe claims, and how to avoid plagiarism

### 9.1 Structure (target 8-10 pages; adapt to venue)
1. **Introduction** (problem, why RCA + early warning matter, contributions as *testable claims*). 2. **Related work** (section 3.1 grouped; end with the comparison table and an explicit delta paragraph). 3. **Problem formulation** (Tasks A/B/C as in section 1). 4. **Method** (detector, propagation estimator, ranking, risk, explanation; equations and pseudocode; limitations). 5. **Experimental setup** (systems, datasets, fault injection, baselines, metrics, statistics, hardware). 6. **Results** (RQ1-RQ5, with ablations and failure cases). 7. **Discussion** (why precedence works, when graph helps/doesn't, cost). 8. **Threats to validity.** 9. **Conclusion.** Artifact availability statement.

### 9.2 Claims you may and may not make
| May claim (if the data supports it) | Do not claim |
|---|---|
| "On RE2-SS/OB, method X achieves Avg@1 = ... [CI], vs BARO ..." | "outperforms the state of the art" without tests |
| "Removing the propagation term changes MRR by ..." (even if ~0) | "novel cascading-failure prediction" |
| "Label-free; no incident labels are used for training" | "unsupervised" without describing what is calibrated on what |
| "Open, reproducible pipeline and data" | "works on any architecture" |
| "Fault-to-ranking latency of ... s on our testbed" | "reduces debugging time" (needs human study) |
| "LLM explanations passed automatic faithfulness checks in n% of cases" | "agentic" unless the agent acts/reasons with tools and you evaluate it |

### 9.3 Plagiarism and integrity checklist
- Write every paragraph in your own words after you understand the source; cite *every* borrowed idea, method, number and dataset.
- Do not paste or lightly paraphrase abstracts, tables or figure captions from the 20+ papers. Re-derive tables from your own data.
- Cite the theory you reuse (Kempe 2003, Goyal 2010, Isolation Forest, MAD/robust statistics) and the benchmark authors (RCAEval, CC-BY attribution).
- Use your institution's similarity checker (iThenticate/Turnitin) before submission; target a low similarity with properly quoted/cited material only.
- Check the target venue's policy on AI-assisted writing and disclose use as required; you remain responsible for every claim and number.
- I cannot verify Scopus indexing. Check each target journal in the Scopus source list / Scimago and avoid predatory venues.

---

## 10. A realistic plan for the next 7 days [J]

| Day | Do | Output |
|---|---|---|
| 1 | Approve downloads; fix detector (log-latency, calibrated on held-out healthy data); decide framing; set up WSL2 or use EC2 for ML | calibrated detector, false-alarm/hour number |
| 2 | RCAEval loaders for RE1-SS/OB and RE2-SS/OB; run prior baseline, simple rules, BARO, MicroRCA, CIRCA/RCD via RCAEval code | baseline table |
| 3 | Run proposed method + ablations on RCAEval; stats | RQ2/RQ3 results |
| 4 | OTel-demo fault-injection campaign (30+ runs) with `rcalab record`; measure latency and overhead | own-data results, RQ1/RQ4 labels |
| 5 | Cascade-risk (Task B) evaluation vs structural/persistence/Hawkes; calibration | RQ4 results |
| 6 | Write: method, setup, results, threats; figures from `results/*/table.tex` | full draft |
| 7 | Related work, abstract, intro; similarity check; reference check against `references.bib`; supervisor review | submission-ready draft |

**If time runs short, cut in this order:** LLM faithfulness (RQ5), RE3, human study, second detector family, then Task B depth (keep a minimal AUROC vs structural).
**Never cut:** RCAEval baselines, ablations, false-alarm calibration, threats to validity.

---

## 11. Decisions and permissions I need from you
1. **Downloads (Zenodo, CC-BY):** RE1-SS 79 MB, RE1-OB 31 MB, RE2-SS 246 MB, RE2-OB 1.2 GB (optional), OTel AIOps benchmark 63 MB, RCAEval code 1 MB. Say which, and I will fetch them.
2. **Fault injection on the OTel host:** you toggle the demo's feature flags (I recommend you do it, since it is your system), tell me the time window and flag, and I `record` and score.
3. **Framing:** confirm section 8.1 (honest empirical study) vs insisting on "novel cascade prediction" (I advise against the latter without evidence).
4. **ML environment:** WSL2 or EC2 instead of changing Windows App Control.
5. **Venue:** pick candidate venues so I can tailor page limits and check for Scopus indexing with you.

---

## Appendix A. Verified literature (65 papers)
See `docs/literature/literature_matrix.csv` (key, year, title, venue, first author, OpenAlex citation count, DOI, category, read depth, relevance)
and `docs/literature/references.bib` (**metadata from OpenAlex; complete the author lists and venue fields before submission**).

Papers read in full (local PDFs) [F]: DeepHunt; Pham et al. 2024; Chain-of-Event; MicroRCA-Agent; Li 2026; Wang and Qi survey; Fu et al. survey; Barata et al. survey;
CHASE, Few-shot cross-system, Graph-Neural-AI, Hybrid RCA (Erakovic and Pahl), Real-Time Context-Aware (Ortiz 2019), AI for Microservice Monitoring (Podduturi 2025),
Faseeha observability survey, Xie et al. hypergraph RCA (arXiv 2511.17566), Mamba cost-sensitive, MaaS cascading-failure, Maheshkar agentic RCA, "real-time" RCA (Vangapelli 2026).
I extracted full text but only skimmed several of these (CHASE, Few-shot, Graph-Neural-AI, Hybrid RCA, Ortiz, Podduturi, Mamba, MaaS, Maheshkar, Vangapelli): **verify my characterization before citing them.**
`CausalRCA.pdf` is a scanned image with no extractable text; I used its OpenAlex abstract.

Quality note [J]: several local items (independent-researcher or low-visibility venues, e.g. the "real-time" RCA piece, the MaaS cascading-failure piece, the bank-VP agentic RCA manuscript)
are weak evidence; do not lean on them for claims.

## Appendix B. Items I could not verify (do not cite until you do)
- **MonitorRank** (Kim et al., SIGMETRICS 2013): known to me from the literature, not found by title in OpenAlex this session.
- **OpenRCA (ICLR 2025):** not found by title in OpenAlex/arXiv this session (OpenRCA 2.0, 2026, is on arXiv).
- **DeepTraLog, Nezha datasets** (from your notes): hosting and contents not checked.
- **FRL-MFPG, CARE (full), MicroDig/HORW, UniDiag, LogFiT, Cascade-IoT, TraceGra (details), GNN-SDN, MLP-Anomaly, the two log surveys** (from your team sheet): several not matched by title; fill the sheet's Problem/Solution/Gap columns from the actual papers.
- **Chandola et al. "Anomaly detection: a survey"**: OpenAlex returned a 2021 book-chapter reprint; cite the original ACM Computing Surveys 2009 after checking.
- **AIOps survey (Notaro et al. 2021)**: not matched.
- **Whether a single published paper combines all your ingredients**: I found none, but absence in two search engines is not proof. Re-run the searches in `experiments/mine.py` with new keywords, and Google Scholar / Scopus, right before submission.

## Appendix C. Reproducibility
`experiments/README.md` lists every script. Raw numbers: `docs/experiments/*.json`. Real telemetry used for T5/T6: `docs/experiments/otel_healthy_live.npz`.
Code and tests: commit history in this repository; 7 tests pass (including the guard that confines SSH to one allowlisted module).
