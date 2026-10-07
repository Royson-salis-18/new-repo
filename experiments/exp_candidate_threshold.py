"""Does a stricter CANDIDATE threshold rescue the full method on large noisy apps?
After an alarm, RCA ranks services flagged at `tau_cand`. At 3.5 many healthy-noise services are candidates and the precedence term
rewards whichever noise flagged first. Sweep tau_cand with the same injections for every method."""
import json
import os
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
from rcalab import store  # noqa: E402
from rcalab.detector import calibrate_threshold, detect  # noqa: E402
from rcalab.rca import rank  # noqa: E402
from rcalab.replay import inject, make_edge_probs  # noqa: E402
from rcalab.topology import bootstrap_telemetry, random_dag  # noqa: E402

OUT = ROOT / "docs" / "experiments"
real = store.load(OUT / "otel_healthy_long.npz")
SP = real.features.index("span_rate")
MIN_RATE = 6
METHODS = ["full", "no_cascade", "anomaly_only", "selftime", "earliest", "pagerank", "random"]
TAUS = (3.5, 6.0, 8.0, 12.0)
results = {}


def first_flag(col, a, b):
    i = np.where(col[a:b])[0]
    return int(i[0]) + a if len(i) else None


def run(label, base, edges, fit, cal, onset_lo, onset_hi, runs, seed):
    rg = np.random.default_rng(seed)
    tau_alarm = calibrate_threshold(base, fit, cal, 5.0, persistence=3)
    q = make_edge_probs(edges, rg)
    mon = [s for s in base.services if np.nanmedian(base.X[:, base.index(s), SP]) >= MIN_RATE and any(c == s for _, c in edges)]
    acc = {t: {m: [] for m in METHODS} for t in TAUS}
    used = 0
    Tn = len(base.times)
    for _ in range(runs):
        root = mon[int(rg.integers(len(mon)))]
        onset = int(rg.integers(onset_lo, min(onset_hi, Tn - 30)))
        tel2, truth = inject(base, root, onset, q, rg, m_self=6.0)
        if first_flag(detect(tel2, fit, tau_alarm, persistence=3, kind="calibrated").flags.any(axis=1), onset, onset + 10) is None:
            continue
        used += 1
        w = (max(fit, onset - 4), min(Tn, onset + 12))
        for tc in TAUS:
            det = detect(tel2, fit, tc, persistence=2, kind="calibrated")
            for m in METHODS:
                names = [s for s, _ in rank(tel2, det, w, 4, 3, m).ranking]
                acc[tc][m].append(float(root in names and names.index(root) == 0))
    results[label] = {"alarmed_runs": used, "tau_alarm": tau_alarm, **{str(tc): {m: float(np.mean(v)) if v else None for m, v in acc[tc].items()} for tc in TAUS}}
    print(f"\n[{label}] alarmed {used}/{runs}, alarm threshold {tau_alarm}; A@1 by candidate threshold")
    print(f"  {'tau_cand':>8} " + " ".join(f"{m:>12}" for m in METHODS))
    for tc in TAUS:
        print(f"  {tc:8.1f} " + " ".join(f"{results[label][str(tc)][m]:12.2f}" for m in METHODS))


run("real 17-service topology", real, real.edges, 60, 120, 195, 270, 150, 3)
for n in (50, 100, 200):
    rg = np.random.default_rng(100 + n)
    names, edges = random_dag(n, rg)
    base = bootstrap_telemetry(real, names, edges, 300, rg)
    run(f"{n} services", base, edges, 60, 100, 180, 260, 90, n)
(OUT / "candidate_threshold.json").write_text(json.dumps(results, indent=1))
