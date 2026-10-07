import sys, json, pathlib, os
import numpy as np
ROOT = pathlib.Path(r"C:\Users\MITE\Downloads\final project (short and sweet)")
sys.path.insert(0, str(ROOT)); os.chdir(ROOT)
from rcalab import store
from rcalab.detector import detect

tel = store.load(ROOT / "docs/experiments/otel_healthy_live.npz")
F = tel.features
span = F.index("span_rate")
active = [i for i, s in enumerate(tel.services) if np.nansum(tel.X[:, i, span]) > 50]
names = [tel.services[i] for i in active]
BASE = 30
print(f"{len(tel.times)} windows, {len(active)} active services, baseline={BASE}")

def rate(flags): f = flags[BASE:][:, active]; return f.mean(), f.any(axis=1).mean(), f.sum(axis=1).mean()

def show(name, flags):
    a, b, c = rate(flags); print(f"{name:58} flag_rate={a:.3f}  windows_with_any={b:.2f}  avg_flagged/window={c:.1f}")
    return {"flag_rate": a, "windows_with_any": b, "avg_flagged": c}

out = {}
# 0) current detector
out["current (all features, robust-z 3.5, persist 2)"] = show("current (all features, robust-z 3.5, persist 2)", detect(tel, BASE, 3.5, persistence=2).flags)

# 1) drop the load-driven feature (span_rate): latency + errors only
t2 = type(tel)(tel.times, tel.services, tel.X.copy(), tel.features, tel.edges); t2.X[:, :, span] = np.nan
out["no span_rate"] = show("no span_rate (latency + errors only)", detect(t2, BASE, 3.5, persistence=2).flags)

# 2) load-normalised throughput: service span rate / total entry span rate
tot = np.nansum(tel.X[:, :, span], axis=1, keepdims=True) + 1e-9
t3 = type(tel)(tel.times, tel.services, tel.X.copy(), tel.features, tel.edges); t3.X[:, :, span] = tel.X[:, :, span] / tot * 100
out["load-normalised span_rate"] = show("load-normalised span_rate share", detect(t3, BASE, 3.5, persistence=2).flags)

# 3) log-latency (multiplicative noise) + quantile threshold from baseline
def quantile_flags(X, base, q=0.999, margin=1.25, persistence=2):
    Z = np.log1p(np.nan_to_num(X, nan=0.0)); hi = np.quantile(Z[:base], q, axis=0) * margin
    raw = (Z > hi).any(axis=2); run = np.zeros_like(raw, dtype=int)
    for t in range(raw.shape[0]): run[t] = np.where(raw[t], (run[t - 1] if t else 0) + 1, 0)
    return run >= persistence
X = tel.X.copy(); X[:, :, span] = np.nan
out["quantile on log features, no span_rate"] = show("baseline-quantile (log scale), no span_rate", quantile_flags(X, BASE))
out["quantile on log features, normalised span"] = show("baseline-quantile (log), normalised span_rate", quantile_flags(t3.X, BASE))

# 4) latency only, robust z in log space, higher persistence
t4 = type(tel)(tel.times, tel.services, np.full_like(tel.X, np.nan), tel.features, tel.edges); t4.X[:, :, F.index("latency_p95")] = np.log1p(tel.X[:, :, F.index("latency_p95")])
for z, pers in ((3.5, 2), (5, 3), (8, 3)):
    out[f"latency only (log) z={z} pers={pers}"] = show(f"latency-only (log-space robust z={z}, persist {pers})", detect(t4, BASE, z, persistence=pers).flags)
(ROOT / "docs/experiments/detector_fix_live.json").write_text(json.dumps(out, indent=1))
