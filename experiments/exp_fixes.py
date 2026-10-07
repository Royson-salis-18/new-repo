"""Tests for the fixes: calibrated detector, self-time ranking, cross-incident cascade learning, and larger applications.

Background telemetry is REAL (docs/experiments/otel_healthy_long.npz: 77 min of the OTel demo, no fault injected). Faults are
injected with rcalab.replay; ground truth (root, onset, who is affected and when) comes from the injection, never from our
detector. Everything here is semi-synthetic and the report says so.   Run: .venv\\Scripts\\python experiments\\exp_fixes.py
"""
import json
import os
import pathlib
import sys
import time

import numpy as np
from scipy.stats import rankdata

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
from rcalab import store  # noqa: E402
from rcalab.cascade import EdgeLearner, cascade_risk, path_probabilities  # noqa: E402
from rcalab.detector import calibrate_threshold, detect  # noqa: E402
from rcalab.rca import rank  # noqa: E402
from rcalab.replay import inject, make_edge_probs  # noqa: E402
from rcalab.topology import bootstrap_telemetry, random_dag  # noqa: E402

OUT = ROOT / "docs" / "experiments"
real = store.load(OUT / "otel_healthy_long.npz")
F = real.features
SP = F.index("span_rate")
T = len(real.times)
FIT, CAL = 60, 120
MIN_RATE = 6                                            # spans/window needed before a window percentile means anything
active = [s for i, s in enumerate(real.services) if np.nansum(real.X[:, i, SP]) > 50]
monitorable = [s for s in active if np.nanmedian(real.X[:, real.services.index(s), SP]) >= MIN_RATE]
print(f"real healthy telemetry: {T} windows ({T * 15 / 60:.0f} min); active services {len(active)}; MONITORABLE at 15 s windows "
      f"(median >= {MIN_RATE} spans/window): {len(monitorable)} -> {monitorable}")
res = {"real_windows": T, "active": active, "monitorable": monitorable, "min_rate": MIN_RATE}


def auc(y, s):
    y, s = np.asarray(y), np.asarray(s, float)
    n1, n0 = int(y.sum()), int(len(y) - y.sum())
    return float("nan") if n1 == 0 or n0 == 0 else float((rankdata(s)[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def ap(y, s):
    y = np.asarray(y)[np.argsort(-np.asarray(s, float), kind="stable")]
    return float("nan") if y.sum() == 0 else float(np.mean([y[:k + 1].sum() / (k + 1) for k in range(len(y)) if y[k]]))


def first_flag(col, start, stop):
    idx = np.where(col[start:stop])[0]
    return int(idx[0]) + start if len(idx) else None


# ------------------------------------------------------------ A: false alarms on real healthy data
print("\n== A. false alarms on REAL healthy traffic (test slice = last 127 windows, never used for fitting or calibration)")
hours = (T - FIT - CAL) * 15 / 3600
A = {}
cols = [real.services.index(s) for s in active]
f = detect(real, FIT, 3.5, persistence=2).flags[FIT + CAL:][:, cols]
A["old robust-z 3.5, persist 2"] = {"flag_rate": float(f.mean()), "episodes_per_hour": float(((f[1:] & ~f[:-1]).sum() + f[0].sum()) / hours)}
TAU = {}
for budget in (1, 2, 5, 10):
    TAU[budget] = calibrate_threshold(real, FIT, CAL, budget, persistence=3)
    f = detect(real, FIT, TAU[budget], persistence=3, kind="calibrated").flags[FIT + CAL:][:, cols]
    ep = int(((f[1:] & ~f[:-1]).sum() + f[0].sum()))
    A[f"calibrated, target {budget}/h"] = {"threshold": TAU[budget], "flag_rate": float(f.mean()), "episodes": ep, "episodes_per_hour": ep / hours}
for k, v in A.items():
    print(f"  {k:30} " + "  ".join(f"{a}={b:.3f}" if isinstance(b, float) else f"{a}={b}" for a, b in v.items()))
res["A_false_alarms"] = {"test_hours": hours, **A}

# ------------------------------------------------------------ B: detection sensitivity vs fault size
print("\n== B. detection of injected slowdowns in REAL telemetry (MONITORABLE roots; detected = root flagged within 10 windows)")
rng = np.random.default_rng(7)
q_real = make_edge_probs(real.edges, rng)
Nb = 60
B = {}
for mag in (2, 4, 8):
    runs = []
    for _ in range(Nb):
        root = monitorable[int(rng.integers(len(monitorable)))]
        onset = int(rng.integers(FIT + CAL + 15, T - 30))
        runs.append(inject(real, root, onset, q_real, rng, m_self=float(mag)) + (root, onset))
    for name, kw in (("old robust-z 3.5/p2", dict(thr=3.5, pers=2, kind="robust_z")), (f"calibrated 1/h (tau={TAU[1]})", dict(thr=TAU[1], pers=3, kind="calibrated")),
                     (f"calibrated 5/h (tau={TAU[5]})", dict(thr=TAU[5], pers=3, kind="calibrated")), ("calibrated 10/h", dict(thr=TAU[10], pers=3, kind="calibrated"))):
        hit, delays = 0, []
        for tel2, truth, root, onset in runs:
            det = detect(tel2, FIT, kw["thr"], persistence=kw["pers"], kind=kw["kind"])
            t = first_flag(det.flags[:, tel2.index(root)], onset, min(onset + 10, T))
            if t is not None:
                hit += 1
                delays.append((t - onset) * 15)
        B.setdefault(f"x{mag}", {})[name] = {"detected": hit / Nb, "median_delay_s": float(np.median(delays)) if delays else None}
    print(f"  slowdown x{mag}: " + "  |  ".join(f"{n.split(' (')[0]}: {v['detected']:.0%}" + (f" (med {v['median_delay_s']:.0f}s)" if v["median_delay_s"] else "") for n, v in B[f"x{mag}"].items()))
res["B_detection_by_size"] = {"n_per_cell": Nb, **B}

# ------------------------------------------------------------ C: RCA with two-stage design
print("\n== C. root-cause ranking on the real 17-service topology: alarm at the strict threshold, then rank candidates at a lower threshold")
METHODS = ["full", "selftime", "anomaly_only", "earliest", "pagerank", "no_cascade", "random"]
C = {}
for mag in (4, 8):
    rr = {m: [] for m in METHODS}
    a1 = {m: [] for m in METHODS}
    a3 = {m: [] for m in METHODS}
    used = 0
    for _ in range(100):
        root = monitorable[int(rng.integers(len(monitorable)))]
        onset = int(rng.integers(FIT + CAL + 15, T - 30))
        tel2, truth = inject(real, root, onset, q_real, rng, m_self=float(mag))
        alarm = detect(tel2, FIT, TAU[5], persistence=3, kind="calibrated")
        if first_flag(alarm.flags.any(axis=1), onset, min(onset + 10, T)) is None:
            continue                                                    # no alarm fired -> RCA never runs (counted in B)
        used += 1
        det = detect(tel2, FIT, 3.5, persistence=2, kind="calibrated")   # lower threshold collects candidates after an alarm
        w = (max(FIT, onset - 4), min(T, onset + 12))
        for m in METHODS:
            names = [s for s, _ in rank(tel2, det, w, 4, 3, m).ranking]
            r_ = names.index(root) + 1 if root in names else len(tel2.services) + 1
            rr[m].append(1 / r_)
            a1[m].append(float(r_ == 1))
            a3[m].append(float(r_ <= 3))
    C[f"x{mag}"] = {"alarmed_runs": used, **{m: {"A@1": float(np.mean(a1[m])), "A@3": float(np.mean(a3[m])), "MRR": float(np.mean(rr[m]))} for m in METHODS}}
    print(f"  slowdown x{mag}, {used}/100 runs alarmed:  " + "  ".join(f"{m} A@1={C[f'x{mag}'][m]['A@1']:.2f}/MRR={C[f'x{mag}'][m]['MRR']:.2f}" for m in METHODS))
res["C_rca_real_topology"] = C

# ------------------------------------------------------------ D: larger applications
print("\n== D. larger applications: random call graphs, REAL bootstrapped background (T=300), monitorable roots, slowdown x6, same two-stage design")
D = {}
for n in (50, 100, 200, 500):
    rg = np.random.default_rng(100 + n)
    names, edges = random_dag(n, rg)
    base = bootstrap_telemetry(real, names, edges, 300, rg)
    tau = calibrate_threshold(base, 60, 100, 5.0, persistence=3)
    q = make_edge_probs(edges, rg)
    mon = [s for s in names if np.nanmedian(base.X[:, base.index(s), SP]) >= MIN_RATE and any(c == s for _, c in edges)]
    meth = ("full", "selftime", "anomaly_only", "earliest", "pagerank", "random")
    rr = {m: [] for m in meth}
    a1 = {m: [] for m in meth}
    t_det = t_rank = 0.0
    used = 0
    for _ in range(60):
        root = mon[int(rg.integers(len(mon)))]
        onset = int(rg.integers(180, 260))
        tel2, truth = inject(base, root, onset, q, rg, m_self=6.0)
        t0 = time.time()
        alarm = detect(tel2, 60, tau, persistence=3, kind="calibrated")
        t_det += time.time() - t0
        if first_flag(alarm.flags.any(axis=1), onset, onset + 10) is None:
            continue
        used += 1
        det = detect(tel2, 60, 3.5, persistence=2, kind="calibrated")
        w = (max(60, onset - 4), onset + 12)
        for m in meth:
            t0 = time.time()
            ranking = rank(tel2, det, w, 4, 3, m).ranking
            t_rank += (time.time() - t0) if m == "full" else 0
            nm = [s for s, _ in ranking]
            r_ = nm.index(root) + 1 if root in nm else n + 1
            rr[m].append(1 / r_)
            a1[m].append(float(r_ == 1))
    D[n] = {"services": n, "edges": len(edges), "monitorable_roots": len(mon), "tau_5h": tau, "alarmed_runs": used, "detect_s": t_det / 60, "rank_full_s": t_rank / max(used, 1),
            "methods": {m: {"A@1": float(np.mean(a1[m])) if a1[m] else None, "MRR": float(np.mean(rr[m])) if rr[m] else None} for m in meth}}
    print(f"  n={n:3d} edges={len(edges):4d} monitorable roots={len(mon):3d} alarmed {used}/60 | detect {t_det / 60:.2f}s rank {D[n]['rank_full_s']:.2f}s | "
          + "  ".join(f"{m} A@1={D[n]['methods'][m]['A@1']:.2f}" if D[n]['methods'][m]['A@1'] is not None else f"{m} n/a" for m in meth))
res["D_larger_apps"] = D

# ------------------------------------------------------------ E: cascade risk, fast vs slow cascades
print("\n== E. cascade-risk forecasting at the moment the ALARM fires; truth = injected onset of each victim; horizon 8 windows")
HOR = 8


def eval_topology(label, base, q, tau, fit, roots, onset_lo, onset_hi, seed, lag):
    rg = np.random.default_rng(seed)
    Tn = len(base.times)

    def incident():
        root = roots[int(rg.integers(len(roots)))]
        onset = int(rg.integers(onset_lo, onset_hi))
        tel2, truth = inject(base, root, onset, q, rg, lag=lag, m_self=8.0, duration=30)
        return tel2, truth, detect(tel2, fit, tau, persistence=3, kind="calibrated")

    hist = [incident() for _ in range(40)]
    test = [incident() for _ in range(100)]
    q_or = {(callee, caller): v for (caller, callee), v in q.items()}
    out = {}
    for K in (0, 2, 8, 20, 40):
        learner = EdgeLearner()
        for tel2, truth, det in hist[:K]:
            learner.update(tel2, det.flags)
        learned = learner.probs(base.edges)
        prior_only = {(callee, caller): 0.5 for caller, callee in base.edges}
        ys, sc, used = [], {"learned": [], "prior-only": [], "structural": [], "oracle": [], "random": []}, 0
        for tel2, truth, det in test:
            t_alarm = first_flag(det.flags[:, tel2.index(truth["root"])], truth["onset"], min(truth["onset"] + 10, Tn - HOR - 1))
            if t_alarm is None:
                continue
            used += 1
            now = det.flags[t_alarm]
            cand = [j for j, s in enumerate(tel2.services) if not now[j] and truth["affected"].get(s, 10**9) > t_alarm]
            if not cand:
                continue
            risks = {name: cascade_risk(det.a[t_alarm], path_probabilities(tel2.services, pr, 3)) for name, pr in (("learned", learned), ("prior-only", prior_only), ("oracle", q_or))}
            parents = {c for c, e in tel2.edges if now[tel2.index(e)]}
            for j in cand:
                ys.append(int(truth["affected"].get(tel2.services[j], 10**9) <= t_alarm + HOR))
                for name in ("learned", "prior-only", "oracle"):
                    sc[name].append(float(risks[name][j]))
                sc["structural"].append(float(tel2.services[j] in parents))
                sc["random"].append(rg.random())
        out[K] = {"alarmed_runs": used, "n": len(ys), "prevalence": float(np.mean(ys)) if ys else None,
                  **{f"AUROC_{k}": auc(ys, v) for k, v in sc.items()}, **{f"AP_{k}": ap(ys, v) for k, v in sc.items()}}
    print(f"  [{label}]  K = past incidents seen by the learner")
    for K, v in out.items():
        print(f"    K={K:2d} alarmed={v['alarmed_runs']:3d} n={v['n']:4d} prev={v['prevalence'] if v['prevalence'] is None else round(v['prevalence'], 2)}  AUROC learned {v['AUROC_learned']:.2f}  prior-only {v['AUROC_prior-only']:.2f}  "
              f"structural {v['AUROC_structural']:.2f}  oracle {v['AUROC_oracle']:.2f}  random {v['AUROC_random']:.2f}   (AP learned {v['AP_learned']:.2f} structural {v['AP_structural']:.2f} oracle {v['AP_oracle']:.2f})")
    return out


E = {}
roots_real = [s for s in monitorable if any(c == s for _, c in real.edges)]
rg1 = np.random.default_rng(55)
names100, edges100 = random_dag(100, rg1)
base100 = bootstrap_telemetry(real, names100, edges100, 300, rg1)
tau100 = calibrate_threshold(base100, 60, 100, 5.0, persistence=3)
q100 = make_edge_probs(edges100, rg1)
mon100 = [s for s in names100 if np.nanmedian(base100.X[:, base100.index(s), SP]) >= MIN_RATE and any(c == s for _, c in edges100)]
for regime, lag in (("fast cascade (lag 0-1 windows)", (0, 1)), ("slow cascade (lag 2-6 windows)", (2, 6))):
    rg0 = np.random.default_rng(31)
    q_r = make_edge_probs(real.edges, rg0)
    E[f"real 17-service | {regime}"] = eval_topology(f"real topology | {regime}", real, q_r, TAU[5], FIT, roots_real, FIT + CAL + 5, T - 40, 41, lag)
    E[f"100 services | {regime}"] = eval_topology(f"100 services | {regime}", base100, q100, tau100, 60, mon100, 180, 250, 42, lag)
res["E_cascade_learning"] = E

(OUT / "fixes_results.json").write_text(json.dumps(res, indent=1, default=float))
print("\nsaved docs/experiments/fixes_results.json")
