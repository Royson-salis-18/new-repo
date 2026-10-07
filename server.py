"""Dashboard backend.  Run:  python server.py   then open http://localhost:8000
Read-only: serves results computed from telemetry (synthetic demo or the live observability APIs).
"""
import time
from functools import lru_cache
from pathlib import Path

import numpy as np
import uvicorn
import yaml
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from rcalab import collect as collector
from rcalab import config, evaluate, synthetic
from rcalab.sources import ssh as sshsrc
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


_live = {"at": 0.0, "tel": None, "minutes": None}


_sampler = {"obj": None, "key": None}


def _ensure_sampler(c: dict):
    """In ssh/both mode keep one background sampler polling the host; restart it if the target changes."""
    if collector.mode(c) == "tools" or config.missing(c):
        if _sampler["obj"]:
            _sampler["obj"].stop(); _sampler.update(obj=None, key=None)
        return
    key = (c["ssh"]["host"], c["ssh"]["key_path"], c["system"]["name"], c["collection"]["step_seconds"])
    if _sampler["key"] != key:
        if _sampler["obj"]:
            _sampler["obj"].stop()
        s = sshsrc.Sampler(collector.ssh_source(c), collector.sample_path(c), c["collection"]["step_seconds"])
        s.start(); _sampler.update(obj=s, key=key)


def _live_data(minutes: int, z: float, refresh: bool):
    """Live telemetry. First call pulls the whole window; refreshes (only when following the latest
    window) re-read just the new windows (tools) or the sample file (ssh). Scrubbing reuses the cache."""
    c = cfg()
    if config.missing(c):
        raise ValueError("Not connected yet. Missing: " + ", ".join(config.missing(c)) + ". Use the Connect button.")
    _ensure_sampler(c)
    step = c["collection"]["step_seconds"]
    now = time.time()
    incremental = collector.mode(c) != "ssh"
    if _live["tel"] is None or _live["minutes"] != minutes or (refresh and not incremental and now - _live["at"] > 10):
        _live.update(tel=collector.collect(c, now - minutes * 60, now), at=now, minutes=minutes)
    elif refresh and now - _live["at"] > 10:
        new = collector.collect(c, _live["tel"].times[-1] - 2 * step, now, trim_leading=False,
                                services=_live["tel"].services)
        _live.update(tel=collector.merge(_live["tel"], new, keep=minutes * 60 // step), at=now)
    tel = _live["tel"]
    base = min(c["collection"]["baseline_minutes"] * 60 // step, max(len(tel.times) // 2, 1))
    return tel, detect(tel, base, z, kind=c["detector"]["kind"]), base, None


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html", headers={"Cache-Control": "no-store"})


@app.get("/api/meta")
def meta():
    c = cfg()
    return {"demo_services": sorted({e for es in synthetic.CALLS.values() for e in es}),
            "live_missing": config.missing(c), "z": c["detector"]["z_threshold"], "mode": collector.mode(c)}


@app.get("/api/state")
def state(source: str = "demo", root: str = "cart-db", hard: bool = True, z: float = 3.5,
          method: str = "full", t: int = -1, minutes: int = 30):
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
        "heat": [[round(float(v), 2) for v in row] for row in np.nan_to_num(np.minimum(det.z, 20)).T],
        "step_s": float(tel.times[1] - tel.times[0]),
        "series": [float(x) for x in np.nan_to_num(np.minimum(det.z.max(axis=1), 20))],
        "z_threshold": z,
    }


@app.get("/api/eval")
def run_eval(source: str = "demo"):
    c = cfg()
    out = evaluate.run_synthetic(c, runs=10, hard=True) if source == "demo" else evaluate.run_dir(c, ROOT / "runs")
    return out


class ConfigIn(BaseModel):
    mode: str = "tools"
    system_name: str = ""
    jaeger_url: str = ""
    jaeger_entry: str = ""            # comma separated entry services, optional
    prometheus_url: str = ""
    loki_url: str = ""
    ssh_host: str = ""
    ssh_user: str = "ubuntu"
    ssh_port: int = 22
    ssh_key_path: str = ""
    ssh_compose_file: str = ""


@app.get("/api/config")
def get_config():
    c = cfg()
    j, ss = c["sources"]["jaeger"], c.get("ssh", {})
    return {"mode": collector.mode(c), "system_name": c["system"]["name"] if c["system"]["name"] != "REQUIRED" else "",
            "jaeger_url": "" if j["url"] == "REQUIRED" else j["url"], "jaeger_entry": ",".join(j.get("entry_services") or []),
            "prometheus_url": c["sources"]["prometheus"].get("url", ""), "loki_url": c["sources"].get("loki", {}).get("url", ""),
            "ssh_host": "" if ss.get("host") in (None, "REQUIRED") else ss["host"], "ssh_user": ss.get("user", "ubuntu"),
            "ssh_port": ss.get("port", 22), "ssh_key_path": "" if ss.get("key_path") in (None, "REQUIRED") else ss["key_path"],
            "ssh_compose_file": ss.get("compose_file", ""), "missing": config.missing(c),
            "sampler_error": _sampler["obj"].last_error if _sampler["obj"] else None}


@app.post("/api/config")
def set_config(b: ConfigIn):
    if b.mode not in ("tools", "ssh", "both"):
        return {"error": "mode must be tools, ssh or both"}
    c = config.load(ROOT / "config.yaml") if (ROOT / "config.yaml").exists() else config.load(ROOT / "config.example.yaml")
    c.setdefault("source", {})["mode"] = b.mode
    c["system"]["name"] = b.system_name.strip() or "REQUIRED"
    c["sources"]["jaeger"]["url"] = b.jaeger_url.strip() or "REQUIRED"
    c["sources"]["jaeger"]["entry_services"] = [x.strip() for x in b.jaeger_entry.split(",") if x.strip()]
    c["sources"]["prometheus"]["url"] = b.prometheus_url.strip()
    c["sources"].setdefault("loki", {})["url"] = b.loki_url.strip()
    ss = c.setdefault("ssh", {})
    ss.update(host=b.ssh_host.strip() or "REQUIRED", user=b.ssh_user.strip() or "ubuntu", port=b.ssh_port,
              key_path=b.ssh_key_path.strip() or "REQUIRED", compose_file=b.ssh_compose_file.strip())
    (ROOT / "config.yaml").write_text(yaml.safe_dump(c, sort_keys=False), encoding="utf-8")
    _live.update(tel=None, at=0.0, minutes=None)
    return {"ok": True, "missing": config.missing(c)}


@app.post("/api/test")
def test_connection():
    """Check each configured source separately so you can see which one is not reachable."""
    c, out = cfg(), []
    m = collector.mode(c)
    def check(name, fn):
        t = time.time()
        try:
            out.append({"source": name, "ok": True, "detail": fn(), "ms": int((time.time() - t) * 1000)})
        except Exception as e:
            out.append({"source": name, "ok": False, "detail": str(e)[:200], "ms": int((time.time() - t) * 1000)})
    if m in ("tools", "both"):
        from rcalab.sources import jaeger, loki, prometheus
        if c["sources"]["jaeger"]["url"] not in ("", "REQUIRED"):
            check("jaeger", lambda: f"{len(jaeger.services(c['sources']['jaeger']['url']))} services")
        if c["sources"]["prometheus"].get("url"):
            check("prometheus", lambda: f"{len(prometheus.query_range(c['sources']['prometheus']['url'], 'vector(1)', time.time() - 60, time.time(), 15))} points")
        if c["sources"].get("loki", {}).get("url"):
            check("loki", lambda: f"{loki.query_range(c['sources']['loki']['url'], 'vector(1)', time.time() - 60, time.time(), 15).size} points")
    if m in ("ssh", "both"):
        if config.missing(c) and any(k.startswith("ssh.") for k in config.missing(c)):
            out.append({"source": "ssh", "ok": False, "detail": "host / key_path not set", "ms": 0})
        else:
            check("ssh", lambda: f"{len(collector.ssh_source(c).stats())} running containers (read-only docker stats)")
    return {"mode": m, "results": out}


app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
