# Experiments behind docs/REVIEW_REPORT.md

Run with the project venv from the project root. Scripts have absolute paths for this machine; edit `ROOT` if you move the folder.

| script | what it does | output |
|---|---|---|
| `mine.py`, `titles.py`, `team.py`, `build_lit.py` | literature mining via the OpenAlex API, verification by title, matrix + bibliography | `docs/literature/*` |
| `exp_live_fp.py` | false-alarm rate of the detector on REAL healthy OTel-demo telemetry | `docs/experiments/live_false_alarm.json`, `otel_healthy_live.npz` |
| `exp_detector_fix.py` | do simple detector changes fix the false alarms? | `docs/experiments/detector_fix_live.json` |
| `exp_synth.py` | E2 robustness sweep, E3 cascade-risk AUROC vs structural baseline, E4 learned-vs-prior edge probabilities | `docs/experiments/synthetic_sweep.json`, `cascade_risk_auroc.json`, `edge_prior_fraction.json` |

`exp_live_fp.py` needs the live OTel host; the saved `.npz` lets you rerun `exp_detector_fix.py` and E4 offline.
All synthetic results are sanity checks, not evidence (see the report, section 4).
