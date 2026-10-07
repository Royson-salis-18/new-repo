"""Dashboard backend.  Run:  python server.py   then open http://localhost:8000
Serves results computed from telemetry (synthetic demo, or a saved project's live data via tools and/or SSH).
"""
import time
from functools import lru_cache
from pathlib import Path

import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rcalab import collect as collector
from rcalab import config, evaluate, projects, synthetic
from rcalab.cascade import cascade_risk, edge_probabilities, path_probabilities
from rcalab.detector import calibrate_threshold, detect
from rcalab.explain import explain, suspects
from rcalab.rca import rank
from rcalab.sources import ssh as sshsrc

ROOT = Path(__file__).parent
app = FastAPI()
projects.migrate_legacy()

_live: dict[str, dict] = {}          # per project: {"tel", "at", "minutes"}
_samplers: dict[str, dict] = {}      # per project: {"obj", "key"}


def cfg() -> dict:
    """Config of the active project (or the template when there are no projects yet)."""
    a = projects.active()
    return projects.load(a) if a else config.load(projects.TEMPLATE)


def _stop_sampler(name: str):
    s = _samplers.pop(name, None)
    if s and s["obj"]:
        s["obj"].stop()


def _ensure_sampler(name: str, c: dict):
    """ssh/both projects keep a background sampler polling their host; restart it if the target changes."""
    if collector.mode(c) == "tools" or config.missing(c):
        return _stop_sampler(name)
    key = (c["ssh"]["host"], c["ssh"]["key_path"], c["ssh"].get("user"), c["collection"]["step_seconds"])
    if _samplers.get(name, {}).get("key") != key:
        _stop_sampler(name)
        s = sshsrc.Sampler(collector.ssh_source(c), collector.sample_path(c), c["collection"]["step_seconds"])
        s.start()
        _samplers[name] = {"obj": s, "key": key}


def _ensure_all_samplers():
    for n in projects.names():
        try:
            _ensure_sampler(n, projects.load(n))
        except Exception as e:
            print(f"[sampler] {n}: {e}")


@lru_cache(maxsize=32)
def _demo(root: str, hard: bool, z: float):
    kw = dict(lag_range=(0, 1), root_mag=3.0, victim_mag=8.0) if hard else {}
    tel, truth = synthetic.make(root, **kw)
    return tel, detect(tel, truth["baseline"], z), truth["baseline"], truth["onset"]


def _live_data(minutes: int, z: float, refresh: bool):
    """Live telemetry of the active project. First call pulls the whole window; refreshes (only when
    following the latest window) re-read just the new windows (tools) or the sample file (ssh)."""
    name, c = projects.active(), cfg()
    if name is None:
        raise ValueError("No project yet. Click the project menu, then New project.")
    if config.missing(c):
        raise ValueError(f"Project '{name}' is incomplete. Missing: " + ", ".join(config.missing(c)))
    _ensure_sampler(name, c)
    st = _live.setdefault(name, {"tel": None, "at": 0.0, "minutes": None})
    step = c["collection"]["step_seconds"]
    now = time.time()
    incremental = collector.mode(c) != "ssh"
    if st["tel"] is None or st["minutes"] != minutes or (refresh and not incremental and now - st["at"] > 10):
        st.update(tel=collector.collect(c, now - minutes * 60, now), at=now, minutes=minutes)
    elif refresh and now - st["at"] > 10:
        new = collector.collect(c, st["tel"].times[-1] - 2 * step, now, trim_leading=False, services=st["tel"].services)
        st.update(tel=collector.merge(st["tel"], new, keep=minutes * 60 // step), at=now)
    tel = st["tel"]
    base = min(c["collection"]["baseline_minutes"] * 60 // step, max(len(tel.times) // 2, 1))
    d = c["detector"]
    if d.get("kind") == "calibrated":
        cal = int(max(min(d.get("calibration_windows", 100), len(tel.times) - base - 10), 10))
        tau = calibrate_threshold(tel, base, cal, float(d.get("alarm_budget_per_hour", 5)), persistence=int(d.get("persistence", 3)))
        st["tau"] = tau
        return tel, detect(tel, base, tau, persistence=int(d.get("persistence", 3)), kind="calibrated"), base, None
    return tel, detect(tel, base, z, kind=d["kind"]), base, None


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html", headers={"Cache-Control": "no-store"})


@app.get("/api/meta")
def meta():
    c = cfg()
    return {"demo_services": sorted({e for es in synthetic.CALLS.values() for e in es}),
            "z": c["detector"]["z_threshold"], "mode": collector.mode(c), "active": projects.active()}


@app.get("/api/state")
def state(source: str = "demo", root: str = "cart-db", hard: bool = True, z: float = 3.5,
          method: str = "full", t: int = -1, minutes: int = 20):
    try:
        tel, det, base, onset = _demo(root, hard, z) if source == "demo" else _live_data(minutes, z, refresh=(t < 0))
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
    two_stage = source != "demo" and c["detector"].get("kind") == "calibrated"
    if two_stage and t > base and not det.flags[base:t + 1].any():
        text = "No alarm in this window: nothing exceeds the calibrated alarm threshold, so no root-cause ranking is run."
    elif t > base:
        det_rca = det
        if source != "demo" and c["detector"].get("kind") == "calibrated":   # two-stage: strict alarm, lower threshold for candidates
            det_rca = detect(tel, base, float(c["detector"].get("candidate_threshold", 3.5)), persistence=2, kind="calibrated")
        res = rank(tel, det_rca, (base, t + 1), lag, hops, method)
        ranking = [{"service": s, "score": float(v)} for s, v in res.ranking]
        text = explain(tel, det_rca, res, (base, t + 1))
        sus = suspects(tel, det_rca, res, (base, t + 1))
    score = {r["service"]: r["score"] for r in ranking}

    return {
        "T": T, "t": t, "baseline": base, "onset": onset, "time": float(tel.times[t]),
        "nodes": [{"id": s, "z": float(det.z[t, i]), "risk": float(risk[i]), "flag": bool(det.flags[t, i]),
                   "score": score.get(s, 0.0)} for i, s in enumerate(tel.services)],
        "edges": [{"source": callee, "target": caller, "p": float(p),
                   "hot": bool(det.flags[t, tel.index(callee)])} for (callee, caller), p in probs.items()],
        "ranking": ranking, "explanation": text, "suspects": sus, "services": tel.services,
        "heat": [[round(float(v), 2) for v in row] for row in np.nan_to_num(np.minimum(det.z, 20)).T],
        "step_s": float(tel.times[1] - tel.times[0]),
        "series": [float(x) for x in np.nan_to_num(np.minimum(det.z.max(axis=1), 20))],
        "z_threshold": (_live.get(projects.active() or "", {}).get("tau", z) if source != "demo" else z),
    }


@app.get("/api/eval")
def run_eval(source: str = "demo"):
    c = cfg()
    return evaluate.run_synthetic(c, runs=10, hard=True) if source == "demo" else evaluate.run_dir(c, ROOT / "runs")


# ---------------- projects ----------------
class ProjectIn(BaseModel):
    original_name: str = ""            # set when editing/renaming an existing project
    mode: str = "tools"
    system_name: str = ""
    services: str = ""
    jaeger_url: str = ""
    jaeger_entry: str = ""
    prometheus_url: str = ""
    loki_url: str = ""
    ssh_host: str = ""
    ssh_user: str = "ubuntu"
    ssh_port: int = 22
    ssh_key_path: str = ""
    ssh_compose_file: str = ""
    step_seconds: int = 15
    baseline_minutes: int = 10


@app.get("/api/projects")
def list_projects():
    rows = projects.listing()
    for r in rows:
        r["sampler_error"] = (_samplers.get(r["name"], {}).get("obj").last_error if r["name"] in _samplers else None)
    return {"active": projects.active(), "projects": rows}


@app.get("/api/projects/{name}")
def get_project(name: str):
    try:
        c = projects.load(name)
    except Exception:
        return {"error": f"no project named {name}"}
    return {**projects.to_form(c), "missing": config.missing(c)}


@app.post("/api/projects")
def save_project(b: ProjectIn):
    if not b.system_name.strip():
        return {"error": "Give the project a name."}
    try:
        base = projects.load(b.original_name) if b.original_name else None
        c = projects.from_form(b.model_dump(), base)
        new = projects.slug(b.system_name)
        if new != projects.slug(b.original_name) and new in projects.names():
            return {"error": f"A project named '{new}' already exists."}
        name = projects.save(c)
        if b.original_name and projects.slug(b.original_name) != name:
            _stop_sampler(projects.slug(b.original_name)); _live.pop(projects.slug(b.original_name), None)
            projects.delete(b.original_name)
        projects.set_active(name)
        _live.pop(name, None)
        _ensure_sampler(name, c)
    except Exception as e:
        return {"error": str(e)}
    return {"ok": True, "name": name, "missing": config.missing(c)}


@app.post("/api/projects/{name}/select")
def select_project(name: str):
    try:
        projects.set_active(name)
    except KeyError:
        return {"error": f"no project named {name}"}
    return {"ok": True, "active": projects.active()}


@app.delete("/api/projects/{name}")
def delete_project(name: str):
    _stop_sampler(projects.slug(name)); _live.pop(projects.slug(name), None)
    projects.delete(name)
    return {"ok": True, "active": projects.active()}


@app.post("/api/projects/{name}/test")
def test_project(name: str):
    """Check each source of a project separately so you can see which one is not reachable."""
    try:
        c = projects.load(name)
    except Exception:
        return {"error": f"no project named {name}"}
    out, m = [], collector.mode(c)

    def check(source, fn):
        t = time.time()
        try:
            out.append({"source": source, "ok": True, "detail": fn(), "ms": int((time.time() - t) * 1000)})
        except Exception as e:
            out.append({"source": source, "ok": False, "detail": (str(e) or type(e).__name__)[:200], "ms": int((time.time() - t) * 1000)})

    if m in ("tools", "both"):
        from rcalab.sources import jaeger, loki, prometheus
        s = c["sources"]
        if s["jaeger"]["url"] not in ("", "REQUIRED"):
            check("jaeger", lambda: f"{len(jaeger.services(s['jaeger']['url']))} services")
        else:
            out.append({"source": "jaeger", "ok": False, "detail": "URL not set", "ms": 0})
        if s["prometheus"].get("url"):
            check("prometheus", lambda: f"{len(prometheus.query_range(s['prometheus']['url'], 'vector(1)', time.time() - 60, time.time(), 15))} points")
        if s.get("loki", {}).get("url"):
            check("loki", lambda: f"{loki.query_range(s['loki']['url'], 'vector(1)', time.time() - 60, time.time(), 15).size} points")
    if m in ("ssh", "both"):
        if any(k.startswith("ssh.") for k in config.missing(c)):
            out.append({"source": "ssh", "ok": False, "detail": "host / key file not set", "ms": 0})
        else:
            check("ssh", lambda: f"{len(collector.ssh_source(c).containers())} running containers (read-only docker ps)")
    return {"mode": m, "results": out}


app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

if __name__ == "__main__":
    _ensure_all_samplers()
    uvicorn.run(app, host="127.0.0.1", port=8000)
