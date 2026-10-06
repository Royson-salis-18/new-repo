"""Score RCA methods against injected-fault labels and compare them statistically."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import stats

from . import store, synthetic
from .detector import detect
from .rca import rank
from .telemetry import Telemetry

METHODS = ["full", "anomaly_only", "earliest", "random"]


def score_one(tel: Telemetry, truth: str, inject_idx: int, baseline: int, cfg: dict,
              method: str) -> dict:
    d, c = cfg["detector"], cfg["cascade"]
    det = detect(tel, baseline, d["z_threshold"], kind=d["kind"])
    T = len(tel.times)

    def top_at(end: int):
        res = rank(tel, det, (baseline, end), c["max_lag_windows"], c["max_hops"], method)
        return [s for s, _ in res.ranking]

    names = top_at(T)
    r = names.index(truth) + 1 if truth in names else len(tel.services) + 1
    # Diagnosis delay: earliest window (after injection) from which top-1 is correct and stays correct.
    tops = [top_at(e) for e in range(inject_idx + 1, T + 1)]
    ok = [bool(t) and t[0] == truth for t in tops]
    delay = None
    for k in range(len(ok)):
        if all(ok[k:]):
            delay = (k + 1) * (tel.times[1] - tel.times[0])
            break
    return {"rank": r, "rr": 1.0 / r, "delay_s": delay}


def aggregate(rows: list[dict], top_k: list[int]) -> dict:
    ranks = np.array([r["rank"] for r in rows])
    out = {f"A@{k}": float((ranks <= k).mean()) for k in top_k}
    out["MRR"] = float(np.mean([r["rr"] for r in rows]))
    d = [r["delay_s"] for r in rows if r["delay_s"] is not None]
    out["median_delay_s"] = float(np.median(d)) if d else None
    out["resolved"] = len(d) / len(rows)
    return out


def compare(results: dict[str, list[dict]]) -> dict:
    """Paired Wilcoxon on per-run reciprocal rank: full vs each baseline."""
    base = np.array([r["rr"] for r in results["full"]])
    out = {}
    for m, rows in results.items():
        if m == "full":
            continue
        other = np.array([r["rr"] for r in rows])
        try:
            p = float(stats.wilcoxon(base, other).pvalue) if np.any(base != other) else 1.0
        except ValueError:
            p = float("nan")
        out[m] = {"mean_diff_rr": float((base - other).mean()), "wilcoxon_p": p}
    return out


def run_dir(cfg: dict, runs_dir: Path) -> dict:
    results = {m: [] for m in METHODS}
    for d in sorted(p for p in runs_dir.iterdir() if (p / "label.json").exists()):
        label = json.loads((d / "label.json").read_text())
        tel = store.load(d / "telemetry.npz")
        inject_idx = int(np.searchsorted(tel.times, label["t_inject"]))
        for m in METHODS:
            results[m].append(score_one(tel, label["service"], inject_idx,
                                        label["baseline_windows"], cfg, m))
    return _report(results, cfg)


def run_synthetic(cfg: dict, runs: int = 10, seed: int = 0, hard: bool = False) -> dict:
    kw = dict(lag_range=(0, 1), root_mag=3.0, victim_mag=8.0) if hard else {}
    rng = np.random.default_rng(seed)
    roots = sorted({e for es in synthetic.CALLS.values() for e in es})
    results = {m: [] for m in METHODS}
    for i in range(runs):
        root = roots[int(rng.integers(len(roots)))]
        tel, truth = synthetic.make(root, seed=seed * 1000 + i, **kw)
        for m in METHODS:
            results[m].append(score_one(tel, truth["service"], truth["onset"], truth["baseline"],
                                        cfg, m))
    return _report(results, cfg)


def _report(results: dict, cfg: dict) -> dict:
    k = cfg["experiment"]["top_k"]
    return {"n_runs": len(results["full"]),
            "metrics": {m: aggregate(rows, k) for m, rows in results.items()},
            "full_vs_baselines": compare(results)}
