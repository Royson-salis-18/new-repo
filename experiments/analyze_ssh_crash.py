"""Analyse the SSH crash test: what does SSH-only telemetry show when a container is stopped, with and without `container_up`?
Ground truth for impact = client-side HTTP results (independent of our detector). Run after experiments/run_ssh_crash.py."""
import json
import os
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
from rcalab import config  # noqa: E402
from rcalab.collect import collect  # noqa: E402
from rcalab.detector import Detection, _calibrated_fz, _persist  # noqa: E402
from rcalab.rca import rank  # noqa: E402

ev = json.loads((ROOT / "docs/experiments/ssh_crash_events.json").read_text())
STEP = ev["step_s"]
cfg = config.load("config.example.yaml")
cfg["system"]["name"] = "death-star-crash"
cfg["source"]["mode"] = "ssh"
cfg["collection"]["step_seconds"] = STEP
cfg["ssh"].update(host=ev["host"], key_path=r"C:\Users\MITE\Downloads\sock-shop-key.pem", compose_file="/home/ubuntu/DeathStarBench/socialNetwork/docker-compose.yml")
tel = collect(cfg, ev["t_begin"], ev["t_end"], trim_leading=False)
T = len(tel.times)
F = tel.features
up = F.index("container_up")
tgt = ev["container"]
j_t = tel.index(tgt)
w_stop = int((ev["t_stop"] - tel.times[0]) // STEP)
w_start = int((ev["t_start"] - tel.times[0]) // STEP)
print(f"telemetry: {T} windows x {len(tel.services)} containers at {STEP}s; edges from compose: {len(tel.edges)}; stop at window {w_stop}, restart at {w_start}")

# ---- independent ground truth: what clients experienced
cl = np.array(ev["client"])                                  # t, status, latency
bins = ((cl[:, 0] - tel.times[0]) // STEP).astype(int)
err_rate = np.array([np.mean(cl[bins == w, 1] != 200) if (bins == w).any() else np.nan for w in range(T)])
lat = np.array([np.median(cl[bins == w, 2]) * 1000 if (bins == w).any() else np.nan for w in range(T)])
print(f"client-visible error rate: baseline {np.nanmean(err_rate[:w_stop]):.2f} | during fault {np.nanmean(err_rate[w_stop:w_start]):.2f} | after restart {np.nanmean(err_rate[w_start + 2:]):.2f}")
print(f"client median latency ms:  baseline {np.nanmedian(lat[:w_stop]):.0f} | during fault {np.nanmedian(lat[w_stop:w_start]):.0f} | after restart {np.nanmedian(lat[w_start + 2:]):.0f}")

BASE_K, MIN_VALID = 30, 20            # baseline = first 30 valid samples (300 s), judged after 20: all before the fault at window ~36


def detection(tel_, thr, persistence=3):
    fz, e = _calibrated_fz(tel_, None, base_k=BASE_K, min_valid=MIN_VALID, return_evidence=True)
    z = fz.max(axis=2)
    return Detection(z=z, a=1 / (1 + np.exp(-(z - thr))), flags=_persist(z >= thr, e, persistence), feature_z=fz)


tel_noup = type(tel)(tel.times, tel.services, tel.X.copy(), tel.features, tel.edges)
tel_noup.X[:, :, up] = np.nan                                  # what the model saw before the container_up fix
results = {}
for label, t_ in (("SSH metrics only (before fix)", tel_noup), ("SSH metrics + container_up (after fix)", tel)):
    print(f"\n=== {label}")
    for thr in (4.0, 6.0, 8.0):
        d = detection(t_, thr)
        base_fl = int(d.flags[:w_stop].sum())
        during = d.flags[w_stop:w_start + 1]
        flagged = [(tel.services[k].replace("socialnetwork-", "").replace("-1", ""), int(np.argmax(during[:, k])) * STEP) for k in range(len(tel.services)) if during[:, k].any()]
        root_hit = d.flags[w_stop:w_start + 1, j_t]
        delay = (int(np.argmax(root_hit)) * STEP) if root_hit.any() else None
        w = (max(MIN_VALID, w_stop - 4), w_start + 1)
        ranked = [s.replace("socialnetwork-", "").replace("-1", "") for s, _ in rank(t_, d, w, 4, 3, "anomaly_only").ranking[:4]]
        pos = [s for s, _ in rank(t_, d, w, 4, 3, "anomaly_only").ranking].index(tgt) + 1 if any(s == tgt for s, _ in rank(t_, d, w, 4, 3, "anomaly_only").ranking) else None
        print(f"  tau={thr}: false flags in baseline={base_fl}; root flagged={'yes, +%ds' % delay if delay is not None else 'NO'}; "
              f"services flagged during fault={len(flagged)} {[f'{n}(+{t}s)' for n, t in sorted(flagged, key=lambda x: x[1])[:5]]}; top-4 ranking={ranked}; true root rank={pos}")
        results.setdefault(label, {})[str(thr)] = {"baseline_false_flags": base_fl, "root_flagged": delay is not None, "root_delay_s": delay,
                                                   "n_flagged_during_fault": len(flagged), "top4": ranked, "root_rank": pos}
results["client"] = {"error_rate_baseline": float(np.nanmean(err_rate[:w_stop])), "error_rate_fault": float(np.nanmean(err_rate[w_stop:w_start])),
                     "latency_ms_baseline": float(np.nanmedian(lat[:w_stop])), "latency_ms_fault": float(np.nanmedian(lat[w_stop:w_start]))}
results["windows"] = {"T": T, "stop": w_stop, "start": w_start, "step_s": STEP}
(ROOT / "docs/experiments/ssh_crash_results.json").write_text(json.dumps(results, indent=1, default=float))
print("\nwhich features of OTHER containers moved during the fault (max one-sided z in fault window, no container_up):")
fz, _ = _calibrated_fz(tel_noup, None, base_k=BASE_K, min_valid=MIN_VALID, return_evidence=True)
seg = fz[w_stop:w_start + 1]
for f_i, f in enumerate(F):
    if f == "container_up":
        continue
    k = int(np.argmax(seg[:, :, f_i].max(axis=0)))
    print(f"  {f:12} max z={seg[:, k, f_i].max():5.1f}  in {tel.services[k].replace('socialnetwork-', '').replace('-1', '')}")
