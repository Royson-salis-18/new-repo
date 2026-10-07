"""Collect a long window of REAL telemetry from the saved project 'open-telemetry' (tools mode) and save it.
Run while the system is healthy (no feature-flag faults enabled). Output: docs/experiments/otel_healthy_long.npz"""
import os
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
from rcalab import projects, store  # noqa: E402
from rcalab.collect import collect  # noqa: E402

minutes = int(sys.argv[1]) if len(sys.argv) > 1 else 110
cfg = projects.load("open-telemetry")
end = time.time()
t0 = time.time()
tel = collect(cfg, end - minutes * 60, end)
out = ROOT / "docs" / "experiments" / "otel_healthy_long.npz"
store.save(out, tel)
print(f"saved {out.name}: {len(tel.times)} windows x {len(tel.services)} services, edges={len(tel.edges)}, took {time.time() - t0:.0f}s")
