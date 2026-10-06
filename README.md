# rca-lab

Lean research harness for: *unlabeled, live-telemetry root cause analysis with probabilistic cascade-risk prediction.*
Python only, no UI. **Read-only: no SSH and no shell execution** (enforced by a test). Telemetry comes from tool APIs: Prometheus (metrics), Jaeger (traces + call graph), Loki (logs, optional).

## Pipeline

```
Prometheus / Jaeger / Loki ──collect──▶ Telemetry (windows x services x features)
      ──detector (robust-z or IsolationForest, baseline-calibrated, NO labels)──▶ anomaly scores + flags
      ──cascade (edge probabilities learned from flags; noisy-OR risk)──▶ propagation P[u,v], risk
      ──rca (strength x precedence x blast radius, minus explained-by-upstream)──▶ ranking
      ──explain (text only, never alters ranking)
```

Faults are injected outside this app (e.g. the OTel demo's feature-flag UI). You report what you injected with `record`;
the label (`runs/<id>/label.json`) is used **only** by `evaluate`.

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
python -m rcalab --config config.yaml record --service cart --fault flagd:cartFailure \n    --start 2026-10-06T18:00:00 --end 2026-10-06T18:05:00   # reads that window, saves runs/
python -m rcalab --config config.yaml evaluate               # A@k, MRR, delay, Wilcoxon vs baselines
python -m rcalab evaluate --synthetic [--hard]               # no live system needed
```

`record` only reads telemetry from Prometheus/Jaeger/Loki for the window you give it.

## Methods compared

`full` (proposed), `anomaly_only`, `earliest`, `random`. Paired Wilcoxon on per-run reciprocal rank.
"Diagnosis delay" = earliest time after injection from which the top-1 stays correct. It is an automated proxy;
comparing to a human debugging time still needs a separate measurement.

## Not built yet

GPU detector (PyTorch autoencoder, CUDA 12.8+ build needed for the RTX 5050), real-system runs, LLM-written explanations.

## Dashboard

```
.venv\Scripts\python server.py      # then open http://127.0.0.1:8000
```

One HTML file (`static/index.html`, no build step, works offline) + a small FastAPI backend (`server.py`).
Layered call graph with learned cascade probabilities as edge weights, animated failure flow, a scrubbable timeline
(playback re-computes everything using only data up to that moment), live root-cause ranking and explanation.
The **Evaluate** button runs the method comparison. It is read-only like the rest of the app.

## Research

See [RESEARCH.md](RESEARCH.md) for hypotheses, protocol, baselines, statistics and threats to validity.
`python -m rcalab evaluate` writes `results/<run>/{summary.json,per_run.csv,table.tex}`.
