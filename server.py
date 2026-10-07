"""Dashboard backend.  Run:  python server.py   then open http://localhost:8000
Read-only: serves results computed from telemetry (synthetic demo or the live observability APIs).
"""
import time
from functools import lru_cache
from pathlib import Path

import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from rcalab import config, evaluate, synthetic
from rcalab.cascade import cascade_risk, edge_probabilities, path_probabilities
from rcalab.detector import detect
from rcalab.explain import explain, suspects
from rcalab.rca import rank

ROOT = Path(__file__).parent
app = FastAPI()


def cfg() -> dict:
    return config.load(ROOT / ("config.yaml" if (ROOT / "config.yaml").exists() else "config.example.yaml"))


@lru_cache(maxsize=32)
def _demo(root: str, hard: bool, z: float):
    kw = dict(lag_range=(0, 1), root_mag=3.0, victim_mag=8.0) if hard else {}
    tel, truth = synthetic.make(root, **kw)
    return tel, detect(tel, truth["baseline"], z), truth["baseline"], truth["onset"]


_live = {"at": 0.0, "key": None, "val": None}


def _live_data(minutes: int, z: float):
    c = cfg()
    if config.missing(c):
        raise ValueError("config.yaml is missing: " + ", ".join(config.missing(c)))
    key = (minutes, z)
    if _live["key"] != key or time.time() - _live["at"] > 10:   # re-read at most every 10 s
        from rcalab.collect import collect
        step = c["collection"]["step_seconds"]
        end = time.time()
        tel = collect(c, end - minutes * 60, end)
        base = c["collection"]["baseline_minutes"] * 60 // step
        _live.update(at=time.time(), key=key, val=(tel, detect(tel, base, z, kind=c["detector"]["kind"]), base, None))
    return _live["val"]


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html", headers={"Cache-Control": "no-store"})


@app.get("/api/meta")
def meta():
    c = cfg()
    return {"demo_services": sorted({e for es in synthetic.CALLS.values() for e in es}),
            "live_missing": config.missing(c), "z": c["detector"]["z_threshold"]}


@app.get("/api/state")
def state(source: str = "demo", root: str = "cart-db", hard: bool = True, z: float = 3.5,
          method: str = "full", t: int = -1, minutes: int = 30):
    try:
        tel, det, base, onset = _demo(root, hard, z) if source == "demo" else _live_data(minutes, z)
    except Exception as e:  # surfaced in the UI
        return {"error": str(e)}
    c = cfg()
    T = len(tel.times)
    t = T - 1 if t < 0 else min(t, T - 1)
    lag, hops = c["cascade"]["max_lag_windows"], c["cascade"]["max_hops"]

    probs = edge_probabilities(tel, det.flags[: t + 1], lag)
    P = path_probabilities(tel.services, probs, hops)
    risk = cascade_risk(det.a[t], P)

    ranking, text, sus = [], "Baseline period: collecting normal behaviour.", []
    if t > base:
        res = rank(tel, det, (base, t + 1), lag, hops, method)
        ranking = [{"service": s, "score": float(v)} for s, v in res.ranking]
        text = explain(tel, det, res, (base, t + 1))
        sus = suspects(tel, det, res, (base, t + 1))
    score = {r["service"]: r["score"] for r in ranking}

    return {
        "T": T, "t": t, "baseline": base, "onset": onset, "time": float(tel.times[t]),
        "nodes": [{"id": s, "z": float(det.z[t, i]), "risk": float(risk[i]), "flag": bool(det.flags[t, i]),
                   "score": score.get(s, 0.0)} for i, s in enumerate(tel.services)],
        "edges": [{"source": callee, "target": caller, "p": float(p),
                   "hot": bool(det.flags[t, tel.index(callee)])} for (callee, caller), p in probs.items()],
        "ranking": ranking, "explanation": text, "suspects": sus, "services": tel.services,
        "heat": [[round(float(v), 2) for v in row] for row in np.minimum(det.z, 20).T],
        "step_s": float(tel.times[1] - tel.times[0]),
        "series": [float(x) for x in np.minimum(det.z.max(axis=1), 20)],
        "z_threshold": z,
    }


@app.get("/api/eval")
def run_eval(source: str = "demo"):
    c = cfg()
    out = evaluate.run_synthetic(c, runs=10, hard=True) if source == "demo" else evaluate.run_dir(c, ROOT / "runs")
    return out


app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
