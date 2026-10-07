import sys, json, itertools, pathlib, os, time
import numpy as np
from scipy.stats import rankdata

def roc_auc_score(y, s):
    y = np.asarray(y); s = np.asarray(s, float); n1 = int(y.sum()); n0 = len(y) - n1
    r = rankdata(s); return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
ROOT = pathlib.Path(r"C:\Users\MITE\Downloads\final project (short and sweet)")
sys.path.insert(0, str(ROOT)); os.chdir(ROOT)
from rcalab import synthetic, config
from rcalab.detector import detect
from rcalab.rca import rank
from rcalab.cascade import edge_probabilities, path_probabilities, cascade_risk

cfg = config.load("config.example.yaml"); lag, hops = cfg["cascade"]["max_lag_windows"], cfg["cascade"]["max_hops"]
METHODS = ["full", "no_cascade", "no_precedence", "no_explained", "pagerank", "anomaly_only", "earliest", "random"]
roots = sorted({e for es in synthetic.CALLS.values() for e in es})
OUT = ROOT / "docs/experiments"; OUT.mkdir(parents=True, exist_ok=True)

# ---------- E2: robustness sweep (final-ranking accuracy) ----------
def run_cfg(p_prop, noise, drop, victim_louder, runs=20, seed=0):
    rng = np.random.default_rng(seed); rr = {m: [] for m in METHODS}; a1 = {m: [] for m in METHODS}
    kw = dict(root_mag=3.0, victim_mag=8.0, lag_range=(0, 1)) if victim_louder else dict(root_mag=6.0, victim_mag=4.0, lag_range=(1, 2))
    for i in range(runs):
        root = roots[int(rng.integers(len(roots)))]
        tel, truth = synthetic.make(root, seed=seed * 1000 + i, p_propagate=p_prop, noise=noise, **kw)
        tel.edges = [e for e in tel.edges if rng.random() >= drop]            # the call graph we OBSERVE may be incomplete
        det = detect(tel, truth["baseline"], 3.5); T = len(tel.times)
        for m in METHODS:
            names = [s for s, _ in rank(tel, det, (truth["baseline"], T), lag, hops, m).ranking]
            r = names.index(root) + 1 if root in names else len(tel.services) + 1
            rr[m].append(1 / r); a1[m].append(float(r == 1))
    return {m: {"MRR": float(np.mean(rr[m])), "A@1": float(np.mean(a1[m]))} for m in METHODS}

sweep = []
t0 = time.time()
for p_prop, noise, drop, vl in itertools.product((0.3, 0.6, 0.9), (1.0, 3.0), (0.0, 0.3, 0.6), (False, True)):
    res = run_cfg(p_prop, noise, drop, vl)
    sweep.append({"p_propagate": p_prop, "noise": noise, "edge_dropout": drop, "victim_louder": vl, "results": res})
print(f"E2 done in {time.time()-t0:.0f}s, {len(sweep)} configs")
(OUT / "synthetic_sweep.json").write_text(json.dumps(sweep, indent=1))

# summary: mean MRR per method over all configs / over the hard ones
def agg(filt):
    sel = [s for s in sweep if filt(s)]
    return {m: float(np.mean([s["results"][m]["MRR"] for s in sel])) for m in METHODS}, len(sel)
for name, f in (("all configs", lambda s: True), ("victim louder than root", lambda s: s["victim_louder"]), ("root louder", lambda s: not s["victim_louder"]),
                ("edges 60% missing", lambda s: s["edge_dropout"] == 0.6), ("p_propagate=0.3", lambda s: s["p_propagate"] == 0.3), ("noise x3", lambda s: s["noise"] == 3.0)):
    a, n = agg(f); print(f"{name:26} (n={n:2d}) " + "  ".join(f"{m}={a[m]:.2f}" for m in METHODS))
# where does full lose to a baseline?
losses = [(s["p_propagate"], s["noise"], s["edge_dropout"], s["victim_louder"], m, round(s["results"][m]["MRR"] - s["results"]["full"]["MRR"], 2))
          for s in sweep for m in METHODS if m != "full" and s["results"][m]["MRR"] > s["results"]["full"]["MRR"] + 0.05]
print("configs where a baseline/ablation beats full by >0.05 MRR:", len(losses), "of", len(sweep) * (len(METHODS) - 1)); print(losses[:12])

# ---------- E3: does cascade risk predict who fails next? ----------
def risk_auc(p_prop, victim_louder, runs=30, seed=1):
    rng = np.random.default_rng(seed); ys, scores = [], {"risk": [], "prior_only": [], "structural": [], "random": []}
    kw = dict(root_mag=3.0, victim_mag=8.0, lag_range=(1, 2)) if victim_louder else dict(root_mag=6.0, victim_mag=4.0, lag_range=(1, 2))
    for i in range(runs):
        root = roots[int(rng.integers(len(roots)))]
        tel, truth = synthetic.make(root, seed=seed * 1000 + i, p_propagate=p_prop, **kw)
        det = detect(tel, truth["baseline"], 3.5); t = truth["onset"] + 2                  # shortly after the root fails
        now = det.flags[t]; fut = det.flags[t + 1: t + 9].any(axis=0)
        cand = [j for j in range(len(tel.services)) if not now[j]]
        if len({int(fut[j]) for j in cand}) < 2: continue
        probs = edge_probabilities(tel, det.flags[: t + 1], lag); P = path_probabilities(tel.services, probs, hops)
        risk = cascade_risk(det.a[t], P)
        prior = {k: 0.5 for k in probs}; Pp = path_probabilities(tel.services, prior, hops); risk0 = cascade_risk(det.a[t], Pp)
        parents = {c for c, e in tel.edges if now[tel.index(e)]}                            # callers of a currently failing callee
        for j in cand:
            ys.append(int(fut[j])); scores["risk"].append(risk[j]); scores["prior_only"].append(risk0[j])
            scores["structural"].append(float(tel.services[j] in parents)); scores["random"].append(rng.random())
    return {k: (float(roc_auc_score(ys, v)) if len(set(ys)) > 1 else None) for k, v in scores.items()}, len(ys), float(np.mean(ys)) if ys else None
e3 = []
for p_prop, vl in itertools.product((0.3, 0.6, 0.9), (False, True)):
    auc, n, prev = risk_auc(p_prop, vl); e3.append({"p_propagate": p_prop, "victim_louder": vl, "n_service_windows": n, "prevalence": prev, "auroc": auc})
    print(f"E3 p={p_prop} victim_louder={vl!s:5} n={n:4d} prev={prev if prev is None else round(prev,2)}  " + "  ".join(f"{k}={v:.2f}" if v is not None else f"{k}=NA" for k, v in auc.items()))
(OUT / "cascade_risk_auroc.json").write_text(json.dumps(e3, indent=1))

# ---------- E4: are the 'learned' edge probabilities anything but the prior? ----------
fr = []
for i in range(30):
    root = roots[i % len(roots)]; tel, truth = synthetic.make(root, seed=500 + i, p_propagate=0.85)
    det = detect(tel, truth["baseline"], 3.5); probs = edge_probabilities(tel, det.flags, lag)
    fr.append(np.mean([abs(v - 0.5) < 1e-9 for v in probs.values()]))
print(f"E4 synthetic: mean fraction of edges whose 'learned' p equals the 0.5 prior at end of incident = {np.mean(fr):.2f}")
from rcalab import store
tel = store.load(ROOT / "docs/experiments/otel_healthy_live.npz"); det = detect(tel, 30, 8.0, persistence=3)
probs = edge_probabilities(tel, det.flags, lag); vals = np.array(list(probs.values()))
print(f"E4 live OTel (healthy): {len(vals)} edges; fraction exactly at prior 0.5 = {np.mean(np.abs(vals-0.5)<1e-9):.2f}; p range {vals.min():.2f}-{vals.max():.2f}")
(OUT / "edge_prior_fraction.json").write_text(json.dumps({"synthetic_mean_fraction_at_prior": float(np.mean(fr)), "live_edges": len(vals), "live_fraction_at_prior": float(np.mean(np.abs(vals - 0.5) < 1e-9))}))
