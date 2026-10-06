# rca-lab

Lean research harness for: *unlabeled, live-telemetry root cause analysis with probabilistic cascade-risk prediction.*
Python only, no UI, no SSH. Telemetry comes from tool APIs: Prometheus (metrics), Jaeger (traces + call graph), Loki (logs, optional).

## Pipeline

```
Prometheus / Jaeger / Loki ──collect──▶ Telemetry (windows x services x features)
      ──detector (robust-z or IsolationForest, baseline-calibrated, NO labels)──▶ anomaly scores + flags
      ──cascade (edge probabilities learned from flags; noisy-OR risk)──▶ propagation P[u,v], risk
      ──rca (strength x precedence x blast radius, minus explained-by-upstream)──▶ ranking
      ──explain (text only, never alters ranking)
```

Fault injection labels (`runs/<id>/label.json`) are used **only** by `evaluate`.

## Setup (Windows)

```
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q
```

## Use

```
python -m rcalab init                    # prompts for every REQUIRED value in config.example.yaml
python -m rcalab --config config.yaml check
python -m rcalab --config config.yaml diagnose --minutes 20
python -m rcalab --config config.yaml experiment --runs 10   # injects faults, saves runs/
python -m rcalab --config config.yaml evaluate               # A@k, MRR, delay, Wilcoxon vs baselines
python -m rcalab evaluate --synthetic [--hard]               # no live system needed
```

`experiment` runs the commands in `fault_injection.faults` on this machine (default: `docker stop/pause/update`),
so the target containers must be local (or change the commands, e.g. to `kubectl`).

## Methods compared

`full` (proposed), `anomaly_only`, `earliest`, `random`. Paired Wilcoxon on per-run reciprocal rank.
"Diagnosis delay" = earliest time after injection from which the top-1 stays correct. It is an automated proxy;
comparing to a human debugging time still needs a separate measurement.

## Not built yet

GPU detector (PyTorch autoencoder, CUDA 12.8+ build needed for the RTX 5050), real-system runs, LLM-written explanations.
