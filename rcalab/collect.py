"""Pull metrics + traces + logs from tool APIs into one Telemetry object."""
from __future__ import annotations

import numpy as np

from .sources import jaeger, loki, prometheus
from .telemetry import FEATURES, Telemetry


def collect(cfg: dict, start: float, end: float) -> Telemetry:
    step = cfg["collection"]["step_seconds"]
    src = cfg["sources"]
    names = cfg["system"].get("services") or jaeger.services(src["jaeger"]["url"])
    n = int((end - start) // step) + 1
    times = start + step * np.arange(n)
    X = np.full((n, len(names), len(FEATURES)), np.nan)

    for j, svc in enumerate(names):
        for key in ("cpu", "memory", "net_rx", "net_tx"):
            q = src["prometheus"]["queries"][key].replace("{service}", svc)
            X[:, j, FEATURES.index(key)] = prometheus.query_range(
                src["prometheus"]["url"], q, start, end, step)
        if src.get("loki", {}).get("url"):
            q = src["loki"]["error_query"].replace("{service}", svc)
            X[:, j, FEATURES.index("log_errors")] = loki.query_range(
                src["loki"]["url"], q, start, end, step)

    p95, rate, edges = jaeger.fetch(src["jaeger"]["url"], names, start, end, step)
    X[:, :, FEATURES.index("latency_p95")] = p95
    X[:, :, FEATURES.index("trace_errors")] = rate
    return Telemetry(times, names, X, list(FEATURES), edges)
