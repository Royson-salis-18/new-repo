"""rca_lite: a small, label-free, self-healing root-cause pipeline for DYNAMIC microservice telemetry.

One file, no training, no labels. Works on (a) a CSV/DataFrame of per-service metrics (your ml-dataset-labeled.csv schema) and
(b) live data sampled over SSH from Docker hosts (same schema), optionally enriched with trace-style columns.

The method in five steps (each one fixes a failure we measured):
  1. prepare()    cumulative counters -> per-second rates; the first row after every collector restart is dropped (counter baseline,
                  log backlog); optional container_up signal (a stopped container simply disappears from `docker stats`).
  2. score()      per service and feature, a ONE-SIDED robust z-score on a log scale against a CAUSAL, SELF-HEALING baseline: the last
                  `window` samples, minus a short guard, minus anything that was itself anomalous. A long fault never becomes "normal",
                  and the data is never judged against its own future (the notebook's whole-dataset mean/std did both).
  3. calibrate()  the alarm threshold is picked so healthy-looking data raises at most N false-alarm episodes per hour; a service is
                  flagged only after `persistence` consecutive judged samples above it. Unjudgeable samples neither extend nor break a streak.
  4. attribute()  root cause = largest of (a) OWN evidence (cpu, memory, pids, disk, container_up, self latency) and (b) the part of a
                  service's SYMPTOMS (errors, latency, traffic, logs) that no callee already shows. Victims only echo their callee's
                  symptoms, so they score low; the source has own evidence or symptoms nobody downstream explains. Services with no
                  telemetry at all can be inferred as suspects from their callers' unexplained symptoms (blind-spot inference).
  5. risk()       cascade risk of a healthy service = severity of its flagged callees x the probability that failure crosses that edge
                  (learned across incidents with EdgeLearner; 0.5 prior = plain structure).
No arbitrary commands: the SSH sampler runs only the fixed read-only templates in ALLOWED (a test checks this file).
"""
from __future__ import annotations

import json
import re
import threading
import time
import warnings
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

# name: (direction that means trouble, scale, evidence group)
SPEC = {
    "cpu_percent": (+1, "log", "own"), "memory_usage_mb": (+1, "log", "own"), "pids": (+1, "log", "own"),
    "block_read_bytes": (+1, "log", "own"), "block_write_bytes": (+1, "log", "own"),
    "network_rx_bytes": (+1, "log", "sym"), "network_tx_bytes": (+1, "log", "sym"),
    "log_count": (+1, "log", "sym"), "error_count": (+1, "log", "sym"), "warning_count": (+1, "log", "sym"),
    "trace_count": (+1, "log", "sym"), "avg_trace_duration_ms": (+1, "log", "sym"),
    "latency_p95": (+1, "log", "sym"), "trace_errors": (+1, "lin", "sym"), "span_rate": (-1, "log", "sym"),
    "self_latency": (+1, "log", "own"), "container_up": (-1, "lin", "own"),
}
CUMULATIVE = {"network_rx_bytes", "network_tx_bytes", "block_read_bytes", "block_write_bytes"}
FLOOR = {"log": 0.15, "lin": 0.05}          # smallest scale = a 15% change on the log scale; 0.05 on a 0..1 quantity
DEFAULT_PRESETS = {
    "sock-shop": [("edge-router", "front-end"), ("front-end", "catalogue"), ("front-end", "carts"), ("front-end", "orders"), ("front-end", "user"),
                  ("orders", "carts"), ("orders", "user"), ("orders", "payment"), ("orders", "shipping"), ("orders", "orders-db"),
                  ("carts", "carts-db"), ("catalogue", "catalogue-db"), ("user", "user-db"), ("shipping", "rabbitmq"), ("queue-master", "rabbitmq")],
}


# ------------------------------------------------------------------------------------------------ 1. prepare
@dataclass
class Panel:
    times: np.ndarray                      # (T,) unix seconds of each tick (ticks with no data at all do not exist)
    services: list[str]
    features: list[str]
    X: np.ndarray                          # (T, S, F), NaN = unknown
    edges: list[tuple[str, str]] = field(default_factory=list)   # (caller, callee)
    step: float = 30.0


def match_edges(raw, services):
    """Map generic (caller, callee) names to the service names in the data by substring ('orders' -> 'orders-1')."""
    out = set()
    for a, b in raw:
        ca = [s for s in services if s == a or re.fullmatch(re.escape(a) + r"[-_]?\d*", s)] or [s for s in services if a in s]
        cb = [s for s in services if s == b or re.fullmatch(re.escape(b) + r"[-_]?\d*", s)] or [s for s in services if b in s]
        for x in ca[:1]:
            for y in cb[:1]:
                if x != y:
                    out.add((x, y))
    return sorted(out)


def prepare(df: pd.DataFrame, step: float | None = None, track_presence: bool = False, gap_factor: float = 5.0, drop_first: bool = True,
            edges=None) -> Panel:
    """DataFrame(timestamp, service, <metrics>) -> Panel. See module docstring, step 1."""
    d = df.copy()
    d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
    feats = [c for c in SPEC if c in d.columns and c != "container_up"]
    parts = []
    for svc, g in d.sort_values("timestamp").groupby("service", sort=False):
        t = g["timestamp"].astype("int64").to_numpy() / 1e9
        dt = np.diff(t, prepend=np.nan)
        med = np.nanmedian(dt[1:]) if len(dt) > 2 else 30.0
        new_session = np.isnan(dt) | (dt > gap_factor * med)
        row = pd.DataFrame({"t": t, "service": svc})
        for f in feats:
            v = pd.to_numeric(g[f], errors="coerce").to_numpy(float)
            if f in CUMULATIVE:
                dv = np.diff(v, prepend=np.nan)
                rate = dv / np.where(dt > 0, dt, np.nan)
                rate[new_session | (dv < 0)] = np.nan          # counter reset or collector restart
                v = rate
            row[f] = v
        if drop_first:
            row.loc[new_session, feats] = np.nan               # startup sample: no rate yet, log backlog
        parts.append(row)
    long = pd.concat(parts, ignore_index=True)
    if step is None:
        step = float(max(5, round(np.nanmedian([np.nanmedian(np.diff(p["t"])) for p in parts if len(p) > 2]))))
    long["tick"] = np.floor(long["t"] / step).astype(np.int64)
    ticks = np.sort(long["tick"].unique())
    tmap = {k: i for i, k in enumerate(ticks)}
    services = list(dict.fromkeys(long["service"]))
    smap = {s: i for i, s in enumerate(services)}
    F = feats + (["container_up"] if track_presence else [])
    X = np.full((len(ticks), len(services), len(F)), np.nan)
    present = np.zeros((len(ticks), len(services)), bool)
    for tick, svc, *vals in long[["tick", "service"] + feats].itertuples(index=False, name=None):
        i, j = tmap[tick], smap[svc]
        X[i, j, :len(feats)] = vals
        present[i, j] = True
    if track_presence:
        k = F.index("container_up")
        for j in range(len(services)):
            last_seen = -10 ** 9
            for i in range(len(ticks)):
                if present[i, j]:
                    last_seen = i
                    X[i, j, k] = 1.0
                elif i - last_seen <= 6 and present[i].any():   # others reported, this one vanished shortly after being seen
                    X[i, j, k] = 0.0
    p = Panel(ticks.astype(float) * step, services, F, X, [], step)
    if edges:
        p.edges = match_edges(edges, services)
    return p


# ------------------------------------------------------------------------------------------------ 2. score
@dataclass
class Scores:
    z: np.ndarray            # (T, S, F) one-sided deviation, 0 where not judged
    own: np.ndarray          # (T, S)
    sym: np.ndarray          # (T, S)
    zs: np.ndarray           # (T, S) max(own, sym)
    judged: np.ndarray       # (T, S) bool: at least one feature could be judged


def score(p: Panel, window: int = 80, guard: int = 2, min_base: int = 20, exclude_z: float = 4.0, common_frac: float = 0.5) -> Scores:
    T, S, F = p.X.shape
    X = p.X.copy()
    direction = np.array([SPEC[f][0] for f in p.features], float)
    floor = np.array([FLOOR[SPEC[f][1]] for f in p.features], float)
    for j, f in enumerate(p.features):
        if SPEC[f][1] == "log":
            X[:, :, j] = np.log1p(np.maximum(X[:, :, j], 0))
    Z = np.zeros((T, S, F))
    J = np.zeros((T, S, F), bool)
    usable = ~np.isnan(X)                                      # sample may teach the baseline (valid and not itself anomalous)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for t in range(T):
            lo, hi = max(0, t - window - guard), max(0, t - guard)
            if hi - lo < 5:
                continue
            B = np.where(usable[lo:hi], X[lo:hi], np.nan)
            n = np.sum(~np.isnan(B), axis=0)
            med = np.nanmedian(B, axis=0)
            mad = np.nanmedian(np.abs(B - med), axis=0) * 1.4826
            z = direction * (X[t] - med) / np.maximum(mad, floor)
            ok = (n >= min_base) & ~np.isnan(z)
            Z[t] = np.where(ok, np.clip(z, 0, 50), 0.0)
            J[t] = ok
            usable[t] &= ~(Z[t] >= exclude_z)                  # self-healing: an anomaly never becomes the baseline
    for j, f in enumerate(p.features):                         # common-mode: a feature shifting in most services at once is load, not a fault
        if SPEC[f][2] != "sym":
            continue
        for t in range(T):
            col, ok = Z[t, :, j], J[t, :, j]
            if ok.sum() >= 4 and np.mean(col[ok] > 3.0) > common_frac:
                Z[t, :, j] = np.where(ok, np.maximum(col - np.median(col[ok]), 0.0), 0.0)
    own_idx = [i for i, f in enumerate(p.features) if SPEC[f][2] == "own"]
    sym_idx = [i for i, f in enumerate(p.features) if SPEC[f][2] == "sym"]
    own = Z[:, :, own_idx].max(axis=2) if own_idx else np.zeros((T, S))
    sym = Z[:, :, sym_idx].max(axis=2) if sym_idx else np.zeros((T, S))
    return Scores(Z, own, sym, np.maximum(own, sym), J.any(axis=2))


# ------------------------------------------------------------------------------------------------ 3. calibrate + flag
def _persist(raw: np.ndarray, judged: np.ndarray, k: int) -> np.ndarray:
    if k <= 1:
        return raw.copy()
    run = np.zeros(raw.shape, int)
    for t in range(raw.shape[0]):
        prev = run[t - 1] if t else 0
        run[t] = np.where(raw[t], prev + 1, np.where(judged[t], 0, prev))
    flags = run >= k
    for t in range(raw.shape[0] - 2, -1, -1):
        flags[t] |= raw[t] & flags[t + 1]
    return flags


def flags_for(sc: Scores, tau: float, persistence: int = 2) -> np.ndarray:
    return _persist(sc.zs >= tau, sc.judged, persistence)


def calibrate(sc: Scores, step: float, budget_per_hour: float = 2.0, persistence: int = 2, grid=None) -> float:
    """Smallest threshold whose persistent-flag episodes (whole system) stay within budget. Assumes the data is mostly healthy,
    so any real faults make the threshold slightly conservative, never aggressive."""
    hours = max(sc.zs.shape[0] * step / 3600.0, 1e-9)
    for tau in (grid if grid is not None else np.arange(3.0, 40.0, 0.5)):
        f = flags_for(sc, tau, persistence)
        episodes = int((f[1:] & ~f[:-1]).sum() + f[0].sum())
        if episodes / hours <= budget_per_hour:
            return float(tau)
    return 40.0


def incidents(flags: np.ndarray, gap: int = 3, pad: int = 2) -> list[tuple[int, int]]:
    on = np.flatnonzero(flags.any(axis=1))
    if len(on) == 0:
        return []
    out, a, b = [], on[0], on[0]
    for t in on[1:]:
        if t - b <= gap:
            b = t
        else:
            out.append((max(a - pad, 0), b + 1))
            a = b = t
    out.append((max(a - pad, 0), b + 1))
    return out


# ------------------------------------------------------------------------------------------------ 4. attribute
def attribute(p: Panel, sc: Scores, window: tuple[int, int], gamma: float = 1.0, infer_unobserved: bool = True) -> pd.DataFrame:
    """Rank services for one incident window (tick range). score = max(own evidence, symptoms no callee already shows)."""
    a, b = window
    own = sc.own[a:b].max(axis=0)
    sym = sc.sym[a:b].max(axis=0)
    idx = {s: i for i, s in enumerate(p.services)}
    callees: dict[int, list[int]] = {}
    callers: dict[int, list[int]] = {}
    for c, e in p.edges:
        if c in idx and e in idx:
            callees.setdefault(idx[c], []).append(idx[e])
            callers.setdefault(idx[e], []).append(idx[c])
    # a callee explains its callers' symptoms with ANY of its evidence (a crashed callee has container_up, not symptoms)
    explain = np.maximum(own, sym)
    resid = np.array([max(0.0, sym[i] - gamma * max((explain[w] for w in callees.get(i, [])), default=0.0)) for i in range(len(p.services))])
    score_ = np.maximum(own, resid)
    judged = sc.judged[a:b].any(axis=0)
    note = [""] * len(p.services)
    if "container_up" in p.features:                           # a stopped process is a fact, not a degree: it outranks any symptom
        k = p.features.index("container_up")
        for i in np.flatnonzero(sc.z[a:b, :, k].max(axis=0) >= 5.0):
            score_[i] += 100.0
            note[i] = "container stopped/crashed (hard evidence)"
    if infer_unobserved:                                        # no telemetry at all, but its callers show symptoms nobody else explains
        for i in range(len(p.services)):
            if not judged[i] and callers.get(i):
                inferred = 0.9 * max(resid[c] for c in callers[i])
                if inferred > score_[i]:
                    score_[i], note[i] = inferred, "inferred: no telemetry, callers show unexplained symptoms"
    top = []
    for i in range(len(p.services)):
        zi = sc.z[a:b, i, :].max(axis=0)
        top.append(p.features[int(np.argmax(zi))] if zi.max() > 0 else "")
    df = pd.DataFrame({"service": p.services, "score": score_, "own": own, "symptoms": sym, "unexplained_symptoms": resid, "top_feature": top, "note": note})
    return df.sort_values("score", ascending=False).reset_index(drop=True)


# ------------------------------------------------------------------------------------------------ 5. cascade risk
class EdgeLearner:
    """P(caller degrades | callee degrades) learned across incidents (label-free, uses detector flags only); pooled prior."""

    def __init__(self, max_lag: int = 4, strength: float = 2.0):
        self.max_lag, self.strength, self.n, self.k = max_lag, strength, {}, {}

    def update(self, p: Panel, flags: np.ndarray):
        idx = {s: i for i, s in enumerate(p.services)}
        for c, e in p.edges:
            ci, ei = idx[c], idx[e]
            for t in range(flags.shape[0]):
                if flags[t, ei] and (t == 0 or not flags[t - 1, ei]):
                    self.n[(c, e)] = self.n.get((c, e), 0) + 1
                    self.k[(c, e)] = self.k.get((c, e), 0) + int(flags[t:t + self.max_lag + 1, ci].any())

    def prob(self, c: str, e: str) -> float:
        tn, tk = sum(self.n.values()), sum(self.k.values())
        p0 = (tk + 0.5) / (tn + 1.0) if tn else 0.5
        return (self.k.get((c, e), 0) + self.strength * p0) / (self.n.get((c, e), 0) + self.strength)


def risk(p: Panel, sc: Scores, flags: np.ndarray, t: int, tau: float, learner: EdgeLearner | None = None) -> pd.DataFrame:
    """Risk that each currently-unflagged service is dragged in by a flagged callee."""
    idx = {s: i for i, s in enumerate(p.services)}
    out = {}
    for c, e in p.edges:
        if flags[t, idx[e]] and not flags[t, idx[c]]:
            sev = min(1.0, sc.zs[t, idx[e]] / (2 * tau))
            pr = learner.prob(c, e) if learner else 0.5
            out[c] = 1 - (1 - out.get(c, 0.0)) * (1 - sev * pr)
    return pd.DataFrame({"service": list(out), "risk": list(out.values())}).sort_values("risk", ascending=False).reset_index(drop=True)


# ------------------------------------------------------------------------------------------------ evaluation helpers
def row_flags(p: Panel, df: pd.DataFrame, flags: np.ndarray) -> pd.Series:
    """Map tick-level service flags back onto the rows of the original DataFrame (for precision/recall against row labels)."""
    step = p.step
    tick = {int(round(t / step)): i for i, t in enumerate(p.times)}
    smap = {s: i for i, s in enumerate(p.services)}
    ts = pd.to_datetime(df["timestamp"], utc=True).astype("int64").to_numpy() / 1e9
    vals = [bool(flags[tick[int(np.floor(t / step))], smap[s]]) if int(np.floor(t / step)) in tick else False for t, s in zip(ts, df["service"])]
    return pd.Series(vals, index=df.index)


# ------------------------------------------------------------------------------------------------ live SSH (read-only)
_UNITS = {"b": 1, "kb": 1e3, "mb": 1e6, "gb": 1e9, "tb": 1e12, "kib": 1024, "mib": 1024 ** 2, "gib": 1024 ** 3, "tib": 1024 ** 4}
ALLOWED = {
    "stats": "docker stats --no-stream --format '{{json .}}'",
    "containers": "docker ps --format '{{.Names}}'",
}
_LOGS = ("docker ps --format '{{.Names}}' | xargs -P 8 -I{} sh -c 'L=$(docker logs --since __SEC__s {} 2>&1); "
         "echo \"{} $(printf \"%s\" \"$L\" | grep -c \"\") $(printf \"%s\" \"$L\" | grep -ciE \"error|exception|fatal\") $(printf \"%s\" \"$L\" | grep -ciE \"warn\")\"'")
_PATH_RE = re.compile(r"^/[A-Za-z0-9_./-]{1,200}$")


def _bytes(text: str) -> float:
    m = re.match(r"\s*([\d.]+)\s*([A-Za-z]+)", text or "")
    return float(m.group(1)) * _UNITS.get(m.group(2).lower(), 1) if m else float("nan")


class HostSampler:
    """Polls one Docker host over SSH using ONLY the fixed read-only commands above; rows follow your CSV schema."""

    def __init__(self, host: str, key_path: str, user: str = "ubuntu", name: str | None = None, log_every_s: int = 30):
        self.host, self.key_path, self.user, self.name = host, key_path, user, name or host
        self.log_every_s, self.rows, self.last_error = log_every_s, [], None
        self._client, self._halt, self._thread, self._last_logs = None, threading.Event(), None, time.time()

    def _connect(self):
        import paramiko
        if self._client and self._client.get_transport() and self._client.get_transport().is_active():
            return self._client
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())          # trust on first use (Colab has no known_hosts)
        c.connect(self.host, username=self.user, key_filename=self.key_path, timeout=20, banner_timeout=40, auth_timeout=30,
                  look_for_keys=False, allow_agent=False)
        self._client = c
        return c

    def _run(self, command: str, timeout: int = 60) -> str:
        last = None
        for _ in range(3):
            try:
                _, out, _ = self._connect().exec_command(command, timeout=timeout)
                return out.read().decode("utf-8", "replace")
            except Exception as e:                                       # a busy host can drop the banner: retry
                last, self._client = e, None
                time.sleep(3)
        raise last

    def containers(self) -> list[str]:
        return [n for n in self._run(ALLOWED["containers"], 30).split() if n]

    def compose_edges(self, path: str):
        """(caller, callee) pairs from depends_on / links of a compose file on the host (read-only `cat`)."""
        if not _PATH_RE.match(path) or ".." in path:
            raise ValueError(f"refusing path {path!r}")
        import yaml
        edges = set()
        for svc, spec in ((yaml.safe_load(self._run(f"cat {path}", 30)) or {}).get("services") or {}).items():
            for key in ("depends_on", "links"):
                deps = (spec or {}).get(key) or []
                for d in (deps if isinstance(deps, (list, dict)) else [deps]):
                    edges.add((svc, str(d).split(":")[0]))
        return sorted(edges)

    def sample_once(self) -> list[dict]:
        now = time.time()
        scan = now - self._last_logs >= self.log_every_s
        logs = {}
        if scan:
            for line in self._run(_LOGS.replace("__SEC__", str(int(now - self._last_logs) + 2)), 90).splitlines():
                parts = line.rsplit(" ", 3)
                if len(parts) == 4 and all(x.isdigit() for x in parts[1:]):
                    logs[parts[0]] = tuple(int(x) for x in parts[1:])
            self._last_logs = now
        rows = []
        for line in self._run(ALLOWED["stats"], 90).splitlines():
            try:
                d = json.loads(line)
                rx, tx = (_bytes(x) for x in d["NetIO"].split("/"))
                br, bw = (_bytes(x) for x in d["BlockIO"].split("/"))
                lg = logs.get(d["Name"]) if scan else None
                rows.append({"timestamp": pd.Timestamp(now, unit="s", tz="UTC"), "service": d["Name"], "cpu_percent": float(d["CPUPerc"].strip("%")),
                             "memory_usage_mb": _bytes(d["MemUsage"].split("/")[0]) / 1e6, "memory_percent": float(d["MemPerc"].strip("%")),
                             "network_rx_bytes": rx, "network_tx_bytes": tx, "block_read_bytes": br, "block_write_bytes": bw,
                             "pids": float(d["PIDs"]), "log_count": lg[0] if lg else np.nan, "error_count": lg[1] if lg else np.nan,
                             "warning_count": lg[2] if lg else np.nan})
            except (KeyError, ValueError, json.JSONDecodeError):
                continue
        return rows

    def start(self, every_s: float = 10.0):
        def loop():
            while not self._halt.is_set():
                t0 = time.time()
                try:
                    self.rows.extend(self.sample_once())
                    self.last_error = None
                except Exception as e:
                    self.last_error = f"{type(e).__name__}: {str(e)[:100]}"
                self._halt.wait(max(1.0, every_s - (time.time() - t0)))
        self._halt.clear()
        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()
        return self

    def stop(self):
        self._halt.set()

    def frame(self) -> pd.DataFrame:
        return pd.DataFrame(self.rows)


# ------------------------------------------------------------------------------------------------ actual vs predicted
def evaluate(p: Panel, sc: Scores, flags: np.ndarray, ledger: list[dict], tau: float, slack_s: float = 40.0) -> dict:
    """Compare predictions with the FAULT LEDGER (what we injected, with start/end times we logged ourselves).
    ledger rows: {"service": name-substring, "kind": "...", "start": unix, "end": unix}.
    Everything outside ledger intervals (+slack for recovery) is treated as healthy, so any flag there is a false alarm."""
    svc_idx = {s: i for i, s in enumerate(p.services)}
    rows, covered = [], np.zeros(len(p.times), bool)
    for f in ledger:
        j = next((i for s, i in svc_idx.items() if f["service"] in s), None)
        a = int(np.searchsorted(p.times, f["start"] - p.step)); b = int(np.searchsorted(p.times, f["end"] + slack_s)) + 1
        covered[max(a - 2, 0):b + 2] = True
        if j is None or b <= a:
            rows.append({**f, "detected": False, "note": "service/time not in data"}); continue
        seg = flags[a:b]
        hit = seg[:, j].any()
        first = int(np.argmax(seg.any(axis=1))) if seg.any() else None
        att = attribute(p, sc, (a, b))
        rank = int(att.index[att.service == p.services[j]][0]) + 1
        rows.append({**f, "root_flagged": bool(hit), "any_flag": bool(seg.any()), "delay_s": None if not hit else float((int(np.argmax(seg[:, j])) * p.step)),
                     "true_root_rank": rank, "predicted_top1": att.service.iloc[0], "top1_correct": att.service.iloc[0] == p.services[j]})
    healthy = ~covered
    ep = lambda m: int((m[1:] & ~m[:-1]).sum() + m[0]) if len(m) else 0
    fa = int(ep(flags[healthy].any(axis=1))) if healthy.any() else 0
    hours = healthy.sum() * p.step / 3600.0
    return {"faults": pd.DataFrame(rows), "healthy_minutes": float(healthy.sum() * p.step / 60), "false_alarm_samples": int(flags[healthy].sum()),
            "false_alarms_per_hour": float(fa / hours) if hours else float("nan")}


# ------------------------------------------------------------------------------------------------ guarded fault injection (YOUR lab only)
class Chaos:
    """Injects crash / pause faults on a host you own. Only `docker stop|start|pause|unpause <name>` where <name> is a currently running
    (or ledger-known) container. Every action is appended to the ledger with its time, so the ground truth is never reconstructed afterwards."""

    def __init__(self, host: HostSampler):
        self.host, self.ledger, self._open = host, [], {}

    def _do(self, verb: str, name: str):
        known = set(self.host.containers()) | set(self._open)
        if verb not in ("stop", "start", "pause", "unpause") or name not in known:
            raise ValueError(f"refused: {verb} {name}")
        return self.host._run(f"docker {verb} {name}", 90)

    def inject(self, name: str, kind: str = "stop"):
        t = time.time()
        self._do(kind, name)
        self._open[name] = (kind, t)
        return t

    def recover(self, name: str):
        kind, t0 = self._open.pop(name)
        self._do("start" if kind == "stop" else "unpause", name)
        row = {"service": name, "kind": kind, "start": t0, "end": time.time(), "host": self.host.name}
        self.ledger.append(row)
        return row

    def recover_all(self):
        return [self.recover(n) for n in list(self._open)]
