# Research protocol

Working title: *Probabilistic Cascading Failure and Agent Assisted Root Cause Analysis for Microservice Systems*
Fill the LaTeX sections from this file; `results/<run>/table.tex` drops straight into the paper.

## 1. Research questions and hypotheses

| | Statement | Falsified if |
|---|---|---|
| RQ1 | Can unsupervised RCA on unlabeled live telemetry with cascade-risk modelling localise injected faults accurately? | A@1 CI includes the best baseline's A@1 across systems |
| H1 | The proposed method (`full`) achieves higher MRR than non-cascade baselines (`anomaly_only`, `earliest`, `pagerank`) | Holm-corrected Wilcoxon p >= 0.05 |
| H2 | Each component (cascade blast-radius, temporal precedence, explained-away penalty) contributes: removing it lowers MRR | Ablation MRR not lower, or CIs overlap fully |
| RQ2 | Does it reduce time-to-diagnosis? | Automated delay (below) not lower than baselines |
| H3 | Cascade risk predicts *future* anomalies: services with high risk at t become anomalous within `max_lag` windows more often than low-risk ones | AUROC of risk vs. later-anomalous <= 0.5 (**not yet implemented**) |

Honesty note: the synthetic generator (`rcalab/synthetic.py`) encodes the method's own assumptions. Its output
is a **pipeline sanity check, never evidence**. Today it shows the ablations and PageRank tie with `full`, i.e.
the synthetic data cannot support H2. Only real fault-injection runs can.

## 2. Systems under test (generalisation; addresses the "single architecture" gap)

1. OpenTelemetry Demo (Prometheus + Jaeger + OpenSearch logs) - primary, already running on EC2
2. Sock Shop (needs Prometheus + a tracer added)
3. Death Star (Social Network) - third architecture

Report results **per system** and pooled. Architecture-independence is claimed only if results hold on >= 2 systems.

## 3. Fault taxonomy and run design

Fault types: service crash/stop, pause (hang), CPU throttle, injected latency, error injection (OTel demo
feature flags e.g. `cartFailure`, `productCatalogFailure`). Injected **outside** the app; labelled via
`python -m rcalab record`. Per system x fault type x target service: >= 10 runs (spec: "Number of runs: 10"),
randomised order, 5-minute baseline before each injection, recovery period between runs, fixed seeds,
no load-generator changes mid-experiment. Labels are used only by `evaluate`.

## 4. Metrics

- **A@k** (k = 1, 3, 5) and **MRR** of the true root-cause service. Same metric family as DeepHunt (Sun et al., TOSEM) for comparability.
- **Diagnosis delay (automated proxy)**: seconds after injection until top-1 is correct and stays correct, using only data available at each step (no look-ahead).
- **Human debugging time** (the quantity in the problem statement) is *not* measured by this code; it needs a small
  user study or a documented manual-triage protocol. Until then RQ2 is claimed only for the automated delay.
- Overhead: wall-clock per diagnosis (and GPU use once the learned detector exists).

## 5. Methods compared (same runs, same detector settings)

- **Proposed:** `full`
- **Ablations (H2):** `no_cascade`, `no_precedence`, `no_explained`
- **Baselines:** `pagerank` (MicroRCA-style personalised PageRank; simplified re-implementation, say so in the paper),
  `anomaly_only`, `earliest`, `random`
- **To add from the literature (not yet implemented):** a correlation/causal-discovery baseline (CausalRCA / RCD family),
  and DeepHunt or another published method on a public labelled dataset as a secondary check.

## 6. Statistics

Per-run reciprocal rank, paired across methods. Bootstrap 95% CIs (2000 resamples). Paired Wilcoxon signed-rank,
proposed vs each other method, **Holm-corrected**. Effect size: Cliff's delta. With 10 runs power is low: report
CIs and effect sizes, not p-values alone, and prefer >= 30 runs per system.

## 7. Reproducibility

Every `evaluate` writes `results/<name>/summary.json` (config values, git commit, Python/platform, timestamp),
`per_run.csv`, `table.tex`. Seeds are fixed. Raw telemetry per run is stored in `runs/<id>/telemetry.npz`.

## 8. Threats to validity

- Injected faults are not production incidents; fault set is ours.
- Detector thresholds were set by us; tune on a held-out system, report on the others.
- Demo systems are small and well-instrumented; real systems have missing/inconsistent telemetry.
- Call graph comes from sampled traces; rarely used edges may be missing.
- Possible circularity: edge probabilities are learned from the same incident's anomaly flags (no labels, but same data).
- Baselines are our re-implementations, not the authors' code.

## 9. Status

Done: collection adapters (Prometheus/Jaeger/Loki), unsupervised detector, cascade model, RCA + ablations,
PageRank baseline, evaluation with CIs/Holm/effect sizes/results export, fault labelling (`record`), read-only guard test.
Missing: real runs on any system, H3 cascade-risk prediction test, learned (GPU) detector, causal baseline,
OTel-specific PromQL queries (verify once Prometheus responds), OpenSearch log adapter, human-time study.
