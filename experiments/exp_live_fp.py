import sys, json, time, pathlib
import numpy as np
ROOT = pathlib.Path(r"C:\Users\MITE\Downloads\final project (short and sweet)")
sys.path.insert(0, str(ROOT)); import os; os.chdir(ROOT)
from rcalab import projects, store
from rcalab.collect import collect
from rcalab.detector import detect

OUT = ROOT / "docs" / "experiments"; OUT.mkdir(parents=True, exist_ok=True)
cfg = projects.load("open-telemetry")
end = time.time(); t0 = time.time()
tel = collect(cfg, end - 30 * 60, end)
print(f"collected {len(tel.times)} windows x {len(tel.services)} services in {time.time()-t0:.0f}s")
store.save(OUT / "otel_healthy_live.npz", tel)

active = [s for s in tel.services if np.nansum(tel.X[:, tel.services.index(s), tel.features.index("span_rate")]) > 50]
res = {"windows": len(tel.times), "services_active": active, "settings": []}
for base in (20, 30, 40):
    for z in (3.5, 5.0, 8.0):
        for pers in (2, 3):
            if base + 5 > len(tel.times): continue
            det = detect(tel, base, z, persistence=pers)
            idx = [tel.services.index(s) for s in active]
            f = det.flags[base:][:, idx]
            res["settings"].append({"baseline_windows": base, "z": z, "persistence": pers, "eval_windows": int(f.shape[0]),
                                    "flag_rate": float(f.mean()), "windows_with_any_flag": float(f.any(axis=1).mean()),
                                    "mean_services_flagged_per_window": float(f.sum(axis=1).mean())})
for r in res["settings"]:
    print(f"base={r['baseline_windows']:2d} z={r['z']:<4} pers={r['persistence']}  flag_rate={r['flag_rate']:.2f}  windows_with_any_flag={r['windows_with_any_flag']:.2f}  avg_flagged/window={r['mean_services_flagged_per_window']:.1f}")
# which services / features dominate false alarms at the default setting
det = detect(tel, 30, 3.5, persistence=2)
by = {}
for s in active:
    i = tel.services.index(s); fl = det.flags[30:, i]
    if fl.any():
        fz = det.feature_z[30:, i][fl].mean(axis=0); by[s] = {"flag_rate": float(fl.mean()), "top_feature": tel.features[int(np.argmax(fz))]}
res["default_setting_by_service"] = by
print(json.dumps(by, indent=1))
(OUT / "live_false_alarm.json").write_text(json.dumps(res, indent=1))
