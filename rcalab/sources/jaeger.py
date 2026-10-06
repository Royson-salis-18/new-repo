from __future__ import annotations

import numpy as np
import requests


def services(url: str) -> list[str]:
    r = requests.get(f"{url.rstrip('/')}/api/services", timeout=30)
    r.raise_for_status()
    return [s for s in r.json()["data"] if not s.startswith("jaeger")]


def _is_error(span: dict) -> bool:
    for t in span.get("tags", []):
        if t["key"] == "error" and str(t["value"]).lower() == "true":
            return True
        if t["key"] in ("http.status_code", "http.response.status_code") and int(t["value"]) >= 500:
            return True
    return False


def fetch(url: str, service_names: list[str], start: float, end: float, step: int):
    """Return (latency_p95, error_rate, edges) with arrays shaped (n_windows, n_services)."""
    n = int((end - start) // step) + 1
    idx = {s: i for i, s in enumerate(service_names)}
    lat = [[[] for _ in service_names] for _ in range(n)]
    err = np.zeros((n, len(service_names)))
    tot = np.zeros((n, len(service_names)))
    edges: set[tuple[str, str]] = set()

    for svc in service_names:
        r = requests.get(f"{url.rstrip('/')}/api/traces", timeout=60,
                         params={"service": svc, "start": int(start * 1e6), "end": int(end * 1e6),
                                 "limit": 1500})
        r.raise_for_status()
        for trace in r.json().get("data", []):
            procs = {pid: p["serviceName"] for pid, p in trace["processes"].items()}
            by_id = {s["spanID"]: s for s in trace["spans"]}
            for s in trace["spans"]:
                name = procs[s["processID"]]
                if name != svc or name not in idx:
                    continue  # count each span once, under its own service
                w = int((s["startTime"] / 1e6 - start) // step)
                if not 0 <= w < n:
                    continue
                lat[w][idx[name]].append(s["duration"] / 1000.0)  # ms
                tot[w, idx[name]] += 1
                err[w, idx[name]] += _is_error(s)
                for ref in s.get("references", []):
                    parent = by_id.get(ref["spanID"])
                    if parent:
                        pname = procs[parent["processID"]]
                        if pname != name:
                            edges.add((pname, name))

    p95 = np.full((n, len(service_names)), np.nan)
    for w in range(n):
        for j in range(len(service_names)):
            if lat[w][j]:
                p95[w, j] = np.percentile(lat[w][j], 95)
    with np.errstate(invalid="ignore", divide="ignore"):
        rate = np.where(tot > 0, err / tot, np.nan)
    return p95, rate, sorted(edges)
