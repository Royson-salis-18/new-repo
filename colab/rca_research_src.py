# %% [markdown]
# # RCA research notebook: every step visible, every change measurable
#
# **What we are building.** A system that watches a running microservice application, notices when something goes wrong *without labels or training*, names the service that is the **source** of the problem (root cause), and says which healthy services are **at risk next** (cascade).
#
# **How to use this notebook.**
# 1. Read the flowchart (section 0). Each later section is one box of it.
# 2. Every box has three cells: **CODE** (the whole method, nothing hidden), **LOOK** (the data before and after this step, plotted), **WHY / WHAT IF** (the problem this step fixes and what to change).
# 3. Section 8 is the **test bench**: hundreds of labelled faults on real healthy traffic, so any change you make prints a before/after accuracy table. Section 9 is the real crash. Section 10 is your CSV. Section 11 is live on your AWS hosts.
#
# **Ground truth, always.** "Actual" faults come only from a **fault ledger** written when the fault is caused (by us), never from the detector. Everything the detector says is a *prediction* until it is matched against the ledger.

# %%
# 0. Setup. Runs on Colab or locally; downloads the real data from the GitHub repo if it is not next to the notebook.
import json, os, time, urllib.request, warnings
from dataclasses import dataclass, field
import numpy as np, pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
try:
    from IPython.display import display, Markdown
except ImportError:                                   # plain python (used for testing)
    display, Markdown = print, str
IN_COLAB = "google.colab" in str(globals().get("get_ipython", lambda: "")())
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
plt.rcParams.update({"figure.figsize": (12, 3.6), "axes.grid": True, "grid.alpha": .3, "font.size": 9})
REPO = "https://raw.githubusercontent.com/Royson-salis-18/new-repo/main/"

def fetch(path):
    """Local copy if we are inside the repo, else download from GitHub."""
    for base in ("", "../"):
        if os.path.exists(base + path):
            return base + path
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    urllib.request.urlretrieve(REPO + path, path)
    return path

# %% [markdown]
# ## 0. The flowchart: what we do, in order
# Data comes in (left), goes through six steps, and comes out as a ranking and an at-risk list (right). The bottom loop is how we *check ourselves*: faults we cause are written to a ledger, and the evaluation compares the ledger with what the pipeline predicted.

# %%
STAGES = [("DATA", "docker stats, logs,\ntraces, or your CSV"), ("1 PREPARE", "counters -> rates\ndrop restart rows\ncrash signal"),
          ("2 SCORE", "robust z vs OWN\nrecent past\n(bad direction only)"), ("3 THRESHOLD", "tau from false-alarm\nbudget + persistence"),
          ("4 COMMON-MODE", "everyone moves =\nload, not a fault"), ("5 ATTRIBUTE", "own evidence vs\ninherited symptoms\n-> root ranking"),
          ("6 RISK", "who is next:\nseverity x edge prob"), ("OUTPUT", "root cause,\nat-risk services")]

def flowchart(highlight=None, ax=None):
    """Pipeline diagram. highlight = index of the stage to emphasise (0..7)."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 3.4))
    ax.set_xlim(0, 16); ax.set_ylim(-1.9, 2.2); ax.axis("off")
    for i, (title, body) in enumerate(STAGES):
        x = 0.1 + i * 2.0
        hot = highlight == i
        col = "#ffd166" if hot else ("#cfe8ff" if 0 < i < 7 else "#e8e8e8")
        ax.add_patch(FancyBboxPatch((x, 0), 1.7, 1.9, boxstyle="round,pad=0.05", fc=col, ec="#d62828" if hot else "#555", lw=2.5 if hot else 1))
        ax.text(x + .85, 1.6, title, ha="center", va="center", weight="bold", fontsize=9)
        ax.text(x + .85, .75, body, ha="center", va="center", fontsize=7.5)
        if i < 7:
            ax.annotate("", (x + 2.0, .95), (x + 1.75, .95), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.add_patch(FancyBboxPatch((3.2, -1.75), 3.6, .9, boxstyle="round,pad=0.05", fc="#d8f3dc", ec="#2d6a4f"))
    ax.text(5.0, -1.3, "FAULT LEDGER (truth)\nwhat WE broke, and when", ha="center", fontsize=8, weight="bold")
    ax.add_patch(FancyBboxPatch((9.2, -1.75), 3.6, .9, boxstyle="round,pad=0.05", fc="#d8f3dc", ec="#2d6a4f"))
    ax.text(11.0, -1.3, "EVALUATE: actual vs predicted\nrecall, delay, A@1, false alarms/h", ha="center", fontsize=8, weight="bold")
    ax.annotate("", (9.2, -1.3), (6.85, -1.3), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2d6a4f"))
    ax.annotate("", (12.0, -.85), (14.9, -.05), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2d6a4f", connectionstyle="arc3,rad=-0.2"))
    ax.set_title("RCA pipeline (yellow = the step this section is about)" if highlight is not None else "RCA pipeline", fontsize=10)
    return ax

flowchart(); plt.show()

# %% [markdown]
# ## 1. The real data we have
# | Dataset | What it is | Truth |
# |---|---|---|
# | **OTel healthy** | OpenTelemetry demo shop, 77 min of *healthy* traffic, 17 services, traces only (p95 latency, error rate, request rate, self time), 15 s ticks | none needed: it is healthy; we inject labelled faults into it in section 8 |
# | **DeathStar crash** | DeathStarBench social network on AWS, 27 containers, docker stats + log error counts every 10 s; we **stopped `post-storage-service` for ~2 min** | ledger written at the moment of the stop; a client measured 95% failed requests during it, 0% before/after |
# | **Your CSV** | `ml-dataset-labeled.csv` (Sock Shop, docker stats, `anomaly_label`) | the label column (section 10) |

# %%
zf = np.load(fetch("docs/experiments/otel_healthy_long.npz"), allow_pickle=True)
meta = json.loads(str(zf["meta"]))
OTEL = dict(times=zf["times"], X=zf["X"], services=meta["services"], features=meta["features"], edges=[tuple(e) for e in meta["edges"]])

ev = json.load(open(fetch("docs/experiments/ssh_crash_events.json")))
DS_EDGES = [tuple(e) for e in json.load(open(fetch("docs/experiments/deathstar_edges.json")))]
rows = []
for line in open(fetch("samples/death-star-crash.jsonl")):
    r = json.loads(line)
    for n, v in r["svc"].items():
        rows.append(dict(timestamp=pd.Timestamp(r["t"], unit="s", tz="UTC"), service=n, cpu_percent=v["cpu"], memory_usage_mb=v["mem"] / 1e6,
                         network_rx_bytes=v["rx"], network_tx_bytes=v["tx"], error_count=np.nan if v["err"] is None else v["err"]))
DS = pd.DataFrame(rows)
DS_LEDGER = [{"service": ev["container"], "kind": "stop", "start": ev["t_stop"], "end": ev["t_start"]}]
print("OTel healthy  :", OTEL["X"].shape, "(ticks, services, features)")
print("DeathStar     :", DS.shape[0], "rows,", DS.service.nunique(), "containers; ledger:", DS_LEDGER[0]["service"], f"stopped {ev['t_start']-ev['t_stop']:.0f}s")
display(DS.head(3))

# %% [markdown]
# ### LOOK at the raw data first (problems are visible before any model runs)

# %%
fig, axs = plt.subplots(1, 3, figsize=(15, 3.4))
for s in ["socialnetwork-nginx-thrift-1", "socialnetwork-text-service-1", ev["container"]]:
    g = DS[DS.service == s]
    axs[0].plot(g.timestamp, g.network_rx_bytes / 1e6, label=s.replace("socialnetwork-", ""))
    axs[1].plot(g.timestamp, g.error_count, ".-", label=s.replace("socialnetwork-", ""))
for ax in axs[:2]:
    ax.axvspan(pd.Timestamp(ev["t_stop"], unit="s", tz="UTC"), pd.Timestamp(ev["t_start"], unit="s", tz="UTC"), color="red", alpha=.12)
axs[0].set_title("PROBLEM 1: network bytes are CUMULATIVE\n(they only go up; a raw z-score just measures time)"); axs[0].legend(fontsize=7)
axs[1].set_title("error log lines per scan (red = real fault)\nPROBLEM 2: the VICTIMS scream, the root goes silent"); axs[1].legend(fontsize=7)
valid = np.mean(~np.isnan(OTEL["X"][:, :, OTEL["features"].index("latency_p95")]), axis=0)
axs[2].barh(OTEL["services"], valid); axs[2].set_xlim(0, 1)
axs[2].set_title("OTel: share of 15 s ticks with any latency\nPROBLEM 3: sparse data, many ticks unjudgeable")
plt.tight_layout(); plt.show()

# %% [markdown]
# ## 2. STEP 1: PREPARE
# **What:** turn raw rows into a clean cube `X[tick, service, feature]`.
# * cumulative counters (network, disk) become **per-second rates**; a counter going down (restart) becomes *unknown*;
# * the **first row after any gap** is dropped (no rate yet, and log scans there contain the whole backlog: the original notebook's `log_count = 100` artefact);
# * `container_up`: a container that **disappears** from `docker stats` while others are still reported becomes `0` (crashed/stopped). Without this, a crash looks like "no data" instead of "broken".
#
# **What if:** turn `track_presence` off and section 9 shows the crash root falling out of first place.

# %%
SPEC = {   # feature: (direction that means trouble, scale, evidence group)
    "cpu_percent": (+1, "log", "own"), "memory_usage_mb": (+1, "log", "own"), "pids": (+1, "log", "own"),
    "block_read_bytes": (+1, "log", "own"), "block_write_bytes": (+1, "log", "own"),
    "network_rx_bytes": (+1, "log", "sym"), "network_tx_bytes": (+1, "log", "sym"),
    "log_count": (+1, "log", "sym"), "error_count": (+1, "log", "sym"), "warning_count": (+1, "log", "sym"),
    "latency_p95": (+1, "log", "sym"), "trace_errors": (+1, "lin", "sym"), "span_rate": (-1, "log", "sym"),
    "self_latency": (+1, "log", "own"), "container_up": (-1, "lin", "own"),
}
# "own"  = evidence about the service ITSELF (its CPU, memory, its own processing time, whether it is running)
# "sym"  = symptoms that can be INHERITED from a broken dependency (errors, end-to-end latency, traffic, log errors)
CUMULATIVE = {"network_rx_bytes", "network_tx_bytes", "block_read_bytes", "block_write_bytes"}
FLOOR = {"log": 0.15, "lin": 0.05}    # smallest allowed spread: a 15% change (log scale) or 0.05 absolute (0..1 quantities)

@dataclass
class Panel:
    times: np.ndarray          # (T,) seconds
    services: list
    features: list
    X: np.ndarray              # (T, S, F); NaN = unknown
    edges: list = field(default_factory=list)   # (caller, callee)
    step: float = 15.0

def match_edges(raw, services):
    """Map wiring names ('orders') onto data names ('orders-1', 'socialnetwork-orders-1')."""
    import re
    out = set()
    pick = lambda a: ([s for s in services if s == a or re.search(r"(^|[-_])" + re.escape(a) + r"([-_]\d+)?$", s)] or [s for s in services if a in s])[:1]
    for a, b in raw:
        for x in pick(a):
            for y in pick(b):
                if x != y:
                    out.add((x, y))
    return sorted(out)

def prepare(df, step=None, track_presence=True, gap_factor=5.0, drop_first=True, edges=None):
    d = df.copy(); d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
    feats = [c for c in SPEC if c in d.columns and c != "container_up"]
    parts = []
    for svc, g in d.sort_values("timestamp").groupby("service", sort=False):
        t = g["timestamp"].astype("int64").to_numpy() / 1e9
        dt = np.diff(t, prepend=np.nan)
        med = np.nanmedian(dt[1:]) if len(dt) > 2 else 30.0
        new_session = np.isnan(dt) | (dt > gap_factor * med)          # first row, or first row after a collector gap
        row = pd.DataFrame({"t": t, "service": svc})
        for f in feats:
            v = pd.to_numeric(g[f], errors="coerce").to_numpy(float)
            if f in CUMULATIVE:                                       # counter -> per-second rate
                dv = np.diff(v, prepend=np.nan)
                v = dv / np.where(dt > 0, dt, np.nan)
                v[new_session | (dv < 0)] = np.nan                    # restart / reset: unknown, not a spike
            row[f] = v
        if drop_first:
            row.loc[new_session, feats] = np.nan
        parts.append(row)
    long = pd.concat(parts, ignore_index=True)
    if step is None:
        step = float(max(5, round(np.nanmedian([np.nanmedian(np.diff(p["t"])) for p in parts if len(p) > 2]))))
    long["tick"] = np.floor(long["t"] / step).astype(np.int64)
    ticks = np.sort(long["tick"].unique()); tmap = {k: i for i, k in enumerate(ticks)}
    services = list(dict.fromkeys(long["service"])); smap = {s: i for i, s in enumerate(services)}
    F = feats + (["container_up"] if track_presence else [])
    X = np.full((len(ticks), len(services), len(F)), np.nan)
    present = np.zeros((len(ticks), len(services)), bool)
    for tick, svc, *vals in long[["tick", "service"] + feats].itertuples(index=False, name=None):
        X[tmap[tick], smap[svc], :len(feats)] = vals; present[tmap[tick], smap[svc]] = True
    if track_presence:                                                # vanished while the others still report = down
        k = F.index("container_up")
        for j in range(len(services)):
            last = -10 ** 9
            for i in range(len(ticks)):
                if present[i, j]:
                    last = i; X[i, j, k] = 1.0
                elif i - last <= 6 and present[i].any():
                    X[i, j, k] = 0.0
    return Panel(ticks.astype(float) * step, services, F, X, match_edges(edges, services) if edges else [], step)

def panel_from_otel(o):
    """The OTel file is already a cube; keep the trace features and add container_up = 1 (all services running)."""
    keep = ["latency_p95", "trace_errors", "span_rate", "self_latency"]
    X = np.stack([o["X"][:, :, o["features"].index(f)] for f in keep] + [np.ones(o["X"].shape[:2])], axis=2)
    return Panel(np.asarray(o["times"], float), list(o["services"]), keep + ["container_up"], X, list(o["edges"]), float(np.median(np.diff(o["times"]))))

P_DS = prepare(DS, step=10, track_presence=True, edges=DS_EDGES)
print("DeathStar cube:", P_DS.X.shape, P_DS.features, "| wiring edges:", len(P_DS.edges))

# %% [markdown]
# ### LOOK: before vs after PREPARE

# %%
flowchart(1); plt.show()
j_root = P_DS.services.index(ev["container"]); j_ng = P_DS.services.index("socialnetwork-nginx-thrift-1")
t_rel = (P_DS.times - P_DS.times[0]) / 60
fault_x = ((ev["t_stop"] - P_DS.times[0]) / 60, (ev["t_start"] - P_DS.times[0]) / 60)
fig, axs = plt.subplots(1, 2, figsize=(14, 3.2))
g = DS[DS.service == "socialnetwork-nginx-thrift-1"]
axs[0].plot((g.timestamp.astype("int64") / 1e9 - P_DS.times[0]) / 60, g.network_rx_bytes / 1e6, label="raw counter (MB)")
ax2 = axs[0].twinx(); ax2.plot(t_rel, P_DS.X[:, j_ng, P_DS.features.index("network_rx_bytes")] / 1e3, color="C1", label="rate (kB/s)")
axs[0].set_title("nginx-thrift network: raw cumulative (blue) vs per-second rate (orange)")
axs[1].step(t_rel, P_DS.X[:, j_root, P_DS.features.index("container_up")], where="mid")
for ax in axs: ax.axvspan(*fault_x, color="red", alpha=.12); ax.set_xlabel("minutes")
axs[1].set_title(f"container_up of {ev['container'].replace('socialnetwork-','')}: drops to 0 while stopped"); plt.show()

# %% [markdown]
# ## 3. STEP 2: SCORE (how unusual is each service, compared with *its own* recent past)
# For every service *s*, feature *f*, tick *t*:
#
# $$ z_{t,s,f} = d_f \cdot \frac{x_{t,s,f} - \text{median}(\text{baseline})}{\max(1.4826\cdot\text{MAD}(\text{baseline}),\ \text{floor}_f)} $$
#
# * **baseline** = the last `window` ticks before *t* (skipping a short `guard`), **only samples that were not themselves anomalous** (`self_heal`): a long fault never becomes "normal".
# * **log scale** for positive quantities (latency 100 to 200 ms is the same jump as 1 to 2 s); **one-sided** ($d_f$ = direction that means trouble, negative values clipped to 0); **median/MAD** instead of mean/std so one spike cannot inflate the spread.
# * only the **past** is used. The original notebook used the mean/std of the *whole* dataset (including the faults and the future): that is leakage and also hides long faults.
#
# * **spread** = the larger of 1.4826 x MAD, the 90% deviation / 1.645 (`tail_q`, for heavy-tailed or mostly-zero series where MAD collapses to 0), and a floor. For the **error rate** we also use the binomial spread sqrt(p(1-p)/n) with n = requests in this tick (`binomial`): one error out of 4 requests is weak evidence, 40 out of 100 is strong.
#
# **What if:** `window` small = adapts fast but forgets normal; large = stable but slow to follow drift. `self_heal=False` lets faults leak into the baseline. `log_scale=False` makes big services dominate. Test each in section 8.

# %%
@dataclass
class Scores:
    z: np.ndarray        # (T,S,F) one-sided deviations (0 = normal or not judged)
    med: np.ndarray      # (T,S,F) baseline median used at each tick (transformed scale)
    scale: np.ndarray    # (T,S,F) baseline spread used at each tick
    own: np.ndarray      # (T,S) max over "own" features
    sym: np.ndarray      # (T,S) max over "symptom" features
    zs: np.ndarray       # (T,S) max(own, sym) = the service's anomaly score
    judged: np.ndarray   # (T,S) at least one feature could be judged
    common: np.ndarray   # (T,F) share of services moving together (before removal)

def sorted_q(A, n, q):
    """q-quantile along axis 0 of an array already sorted along axis 0 (NaN sort last); n = valid count per column."""
    idx = np.clip(np.floor(q * (np.maximum(n, 1) - 1)).astype(int), 0, A.shape[0] - 1)
    out = np.take_along_axis(A, idx[None], axis=0)[0]
    return np.where(n > 0, out, np.nan)

def score(p, window=60, min_base=12, guard=2, exclude_z=4.0, common_frac=0.5, log_scale=True, self_heal=True, tail_q=0.9, binomial=True, smooth=1):
    T, S, F = p.X.shape
    X = p.X.copy()
    direction = np.array([SPEC[f][0] for f in p.features], float)
    floor = np.array([FLOOR[SPEC[f][1]] for f in p.features], float)
    for j, f in enumerate(p.features):
        if log_scale and SPEC[f][1] == "log":
            X[:, :, j] = np.log1p(np.maximum(X[:, :, j], 0))
        elif not log_scale and SPEC[f][1] == "log":
            floor[j] = 1e-6
    if smooth > 1:                                                      # rolling median of the last `smooth` VALID values per series:
        Xs = X.copy()                                                   # a sustained shift survives, a one-tick spike does not
        for j in range(F):
            if p.features[j] == "container_up":
                continue
            df_ = pd.DataFrame(X[:, :, j])
            Xs[:, :, j] = np.where(np.isnan(X[:, :, j]), np.nan, df_.rolling(smooth, min_periods=1).median().to_numpy())
        X = Xs
    k_err = p.features.index("trace_errors") if "trace_errors" in p.features else None
    k_rate = p.features.index("span_rate") if "span_rate" in p.features else None
    Z = np.zeros((T, S, F)); MED = np.full((T, S, F), np.nan); SC = np.full((T, S, F), np.nan)
    J = np.zeros((T, S, F), bool)
    usable = ~np.isnan(X)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for t in range(T):
            lo, hi = max(0, t - window - guard), max(0, t - guard)
            if hi - lo < 5:
                continue
            B = np.where(usable[lo:hi], X[lo:hi], np.nan)              # only past samples that were normal
            n = np.sum(~np.isnan(B), axis=0)
            med = sorted_q(np.sort(B, axis=0), n, 0.5)                  # median of the baseline (NaN-aware, one sort)
            dev = np.sort(np.abs(B - med), axis=0)
            spread = np.maximum(sorted_q(dev, n, 0.5) * 1.4826, floor)  # 1.4826 x MAD = std for normal data
            if tail_q:                                                  # heavy tails / mostly-zero series: MAD collapses, so also
                spread = np.maximum(spread, sorted_q(dev, n, tail_q) / 1.645)   # respect the 90% deviation
            if binomial and k_err is not None and k_rate is not None:  # error RATE: 1 error in 4 requests is weak evidence
                p0 = np.clip(med[:, k_err], 0.01, 0.99); n_now = np.maximum(p.X[t, :, k_rate], 1)
                spread[:, k_err] = np.maximum(spread[:, k_err], np.sqrt(p0 * (1 - p0) / n_now))
            z = direction * (X[t] - med) / spread
            ok = (n >= min_base) & ~np.isnan(z)                         # enough history and a value now
            Z[t] = np.where(ok, np.clip(z, 0, 50), 0.0); J[t] = ok; MED[t] = med; SC[t] = spread
            if self_heal:
                usable[t] &= ~(Z[t] >= exclude_z)                       # an anomaly never becomes the baseline
    common = np.zeros((T, F))
    for j, f in enumerate(p.features):                                  # STEP 4 lives here: common-mode removal
        for t in range(T):
            col, ok = Z[t, :, j], J[t, :, j]
            if ok.sum() >= 4:
                common[t, j] = np.mean(col[ok] > 3.0)
                if common_frac is not None and SPEC[f][2] == "sym" and common[t, j] > common_frac:
                    Z[t, :, j] = np.where(ok, np.maximum(col - np.median(col[ok]), 0.0), 0.0)
    own_i = [i for i, f in enumerate(p.features) if SPEC[f][2] == "own"]
    sym_i = [i for i, f in enumerate(p.features) if SPEC[f][2] == "sym"]
    own = Z[:, :, own_i].max(axis=2) if own_i else np.zeros((T, S))
    sym = Z[:, :, sym_i].max(axis=2) if sym_i else np.zeros((T, S))
    return Scores(Z, MED, SC, own, sym, np.maximum(own, sym), J.any(axis=2), common)

S_DS = score(P_DS, window=30, min_base=8)

# %% [markdown]
# ### LOOK: one service, one feature, the baseline band, and the score

# %%
flowchart(2); plt.show()
k = P_DS.features.index("error_count"); j = P_DS.services.index("socialnetwork-user-timeline-service-1")
x = np.log1p(P_DS.X[:, j, k]); med, sc = S_DS.med[:, j, k], S_DS.scale[:, j, k]
fig, axs = plt.subplots(1, 2, figsize=(14, 3.2))
axs[0].plot(t_rel, x, ".-", label="log(1 + error lines)"); axs[0].plot(t_rel, med, label="baseline median (past only)")
axs[0].fill_between(t_rel, med - 4 * sc, med + 4 * sc, alpha=.2, label="median +- 4 spreads")
axs[0].set_title("user-timeline error logs vs its own past"); axs[0].legend(fontsize=7)
whole = (P_DS.X[:, j, k] - np.nanmean(P_DS.X[:, j, k])) / np.nanstd(P_DS.X[:, j, k])
axs[1].plot(t_rel, S_DS.z[:, j, k], label="OUR z (past only, one-sided, robust)"); axs[1].plot(t_rel, whole, label="original notebook z (whole dataset, mean/std)")
axs[1].axhline(3, ls="--", c="k", lw=.8)
for ax in axs: ax.axvspan(*fault_x, color="red", alpha=.12); ax.set_xlabel("minutes")
axs[1].set_title("same data, two scores: the whole-dataset z is squashed by the fault itself"); axs[1].legend(fontsize=7); plt.show()

# %% [markdown]
# ## 4. STEP 3: THRESHOLD + PERSISTENCE (when is a score an alarm?)
# * A service is **flagged** when its score is above **tau** for `persistence` ticks in a row. Ticks with no data neither extend nor break the streak.
# * **tau is not guessed.** It is the smallest value whose alarms on healthy data stay under your budget (`budget` false alarms per hour). You choose the trade-off; the data sets the number.
#
# **What if:** a lower budget means fewer false alarms but later/fewer detections; a higher persistence means fewer flickers but slower detection. The curve below shows the trade-off on 77 min of real healthy OTel traffic.

# %%
def persist(raw, judged, k):
    if k <= 1:
        return raw.copy()
    run = np.zeros(raw.shape, int)
    for t in range(raw.shape[0]):
        prev = run[t - 1] if t else 0
        run[t] = np.where(raw[t], prev + 1, np.where(judged[t], 0, prev))   # unknown ticks keep the streak
    fl = run >= k
    for t in range(raw.shape[0] - 2, -1, -1):
        fl[t] |= raw[t] & fl[t + 1]                                            # mark the whole streak, not only its end
    return fl

def flags_for(sc, tau, persistence=2):
    return persist(sc.zs >= tau, sc.judged, persistence)

def episodes_per_hour(fl, step):
    starts = (fl[1:] & ~fl[:-1]).sum() + fl[0].sum()
    return starts / max(fl.shape[0] * step / 3600, 1e-9)

def normalise(sc, ref, q=0.995, features=None):
    """Per-series noise normalisation: a series that is jumpy even when HEALTHY (ref = scores on healthy history) is shrunk so its
    healthy extreme sits at z = 3; quiet series are never amplified. Then one global tau is fair to every service."""
    Zr = np.where(ref.z > 0, ref.z, np.nan)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        Q = np.nan_to_num(np.nanquantile(Zr, q, axis=0), nan=0.0)          # (S, F) healthy extreme per series
    Z = sc.z / np.maximum(Q / 3.0, 1.0)
    fs = features
    own_i = [i for i, f in enumerate(fs) if SPEC[f][2] == "own"]; sym_i = [i for i, f in enumerate(fs) if SPEC[f][2] == "sym"]
    own = Z[:, :, own_i].max(axis=2); sym = Z[:, :, sym_i].max(axis=2)
    return Scores(Z, sc.med, sc.scale, own, sym, np.maximum(own, sym), sc.judged, sc.common)

def calibrate(sc, step, budget=2.0, persistence=2, grid=np.arange(1.5, 40.0, 0.25)):
    for tau in grid:
        if episodes_per_hour(flags_for(sc, tau, persistence), step) <= budget:
            return float(tau)
    return 40.0

P_OT = panel_from_otel(OTEL)
S_OT = score(P_OT)
taus = np.arange(3, 30, 1.0)
fig, ax = plt.subplots(figsize=(8, 3.2))
for k_ in (1, 2, 3):
    ax.plot(taus, [episodes_per_hour(flags_for(S_OT, t_, k_), P_OT.step) for t_ in taus], label=f"persistence {k_}")
ax.set_yscale("symlog"); ax.axhline(2, ls="--", c="k", lw=.8); ax.set_xlabel("tau"); ax.set_ylabel("false alarms / hour")
ax.set_title("healthy OTel traffic: false alarms vs threshold (dashed = budget 2/h)"); ax.legend(); plt.show()
print("tau chosen for budget 2/h, persistence 2:", calibrate(S_OT, P_OT.step, 2.0, 2))

# %% [markdown]
# ## 5. STEP 4: COMMON-MODE (a traffic burst is not 20 faults)
# If more than `common_frac` of the services move together on one symptom feature, the shared part (the median score) is subtracted. Real example below: in the DeathStar run, network traffic jumped on almost every container at once.
#
# **What if:** `common_frac=None` switches it off; in section 9 the crash root drops from #1 when we also remove hard evidence. A too-low value can erase a real fault that hits many services at once (e.g. a shared database), so the bench tests it.

# %%
flowchart(4); plt.show()
S_DS_nocm = score(P_DS, window=30, min_base=8, common_frac=None)
kx = P_DS.features.index("network_rx_bytes")
fig, axs = plt.subplots(1, 2, figsize=(14, 3.2))
axs[0].plot(t_rel, S_DS.common[:, kx]); axs[0].axhline(.5, ls="--", c="k"); axs[0].set_title("share of containers whose network-in is unusual (dashed = 0.5)")
axs[1].plot(t_rel, S_DS_nocm.z[:, :, kx].max(axis=1), label="max z without common-mode removal")
axs[1].plot(t_rel, S_DS.z[:, :, kx].max(axis=1), label="max z with removal"); axs[1].legend(fontsize=7)
for ax in axs: ax.axvspan(*fault_x, color="red", alpha=.12)
plt.show()

# %% [markdown]
# ## 6. STEP 5: ATTRIBUTE (source or victim?)
# For the incident window, each service gets:
# * **own** = strongest *own* evidence (CPU, memory, self time, `container_up`);
# * **symptoms** = strongest *inheritable* evidence (errors, latency, traffic, log errors);
# * **explained** = the strongest evidence of any service it **calls** (a broken callee explains its callers' symptoms), times `gamma`;
# * **unexplained = max(0, symptoms - explained)**;
# * **score = max(own, unexplained)**, plus a large bonus for a stopped container (`hard`: a stopped process is a fact, not a degree);
# * a service with **no data at all** whose callers have unexplained symptoms gets 0.9 x that (blind-spot inference).
#
# **Why:** victims only echo their callee, so their unexplained part is small; the source has its own evidence or symptoms that nothing downstream explains. **What if:** `gamma=0` = plain "most abnormal service"; `hard=False` = no crash bonus; missing wiring edges = nothing gets explained away (the method silently becomes "most abnormal").

# %%
def attribute(p, sc, window, gamma=1.0, hard=True, infer=True, agg="max"):
    a, b = window
    if agg == "max":                                    # strongest single tick in the window
        own = sc.own[a:b].max(axis=0); sym = sc.sym[a:b].max(axis=0)
    else:                                               # "sustained": mean of the top half of ticks (one spike cannot win)
        def top_half(M):
            k = max(1, (b - a) // 2)
            return np.sort(M[a:b], axis=0)[-k:].mean(axis=0)
        own = top_half(sc.own); sym = top_half(sc.sym)
    idx = {s: i for i, s in enumerate(p.services)}
    callees, callers = {}, {}
    for c, e in p.edges:
        if c in idx and e in idx:
            callees.setdefault(idx[c], []).append(idx[e]); callers.setdefault(idx[e], []).append(idx[c])
    evidence = np.maximum(own, sym)
    explained = np.array([gamma * max((evidence[w] for w in callees.get(i, [])), default=0.0) for i in range(len(p.services))])
    unexpl = np.maximum(0.0, sym - explained)
    final = np.maximum(own, unexpl)
    note = [""] * len(p.services)
    if hard and "container_up" in p.features:
        k = p.features.index("container_up")
        for i in np.flatnonzero(sc.z[a:b, :, k].max(axis=0) >= 5.0):
            final[i] += 100.0; note[i] = "STOPPED (hard evidence)"
    judged = sc.judged[a:b].any(axis=0)
    if infer:
        for i in range(len(p.services)):
            if not judged[i] and callers.get(i):
                guess = 0.9 * max(unexpl[c] for c in callers[i])
                if guess > final[i]:
                    final[i], note[i] = guess, "inferred: silent, callers have unexplained symptoms"
    top = [p.features[int(np.argmax(sc.z[a:b, i].max(axis=0)))] if sc.z[a:b, i].max() > 0 else "" for i in range(len(p.services))]
    out = pd.DataFrame({"service": p.services, "score": final, "own": own, "symptoms": sym, "explained": explained,
                        "unexplained": unexpl, "top_feature": top, "note": note})
    return out.sort_values("score", ascending=False).reset_index(drop=True)

w0 = int(np.searchsorted(P_DS.times, ev["t_stop"])) - 2; w1 = int(np.searchsorted(P_DS.times, ev["t_start"])) + 1
ATT = attribute(P_DS, S_DS, (w0, w1))
display(ATT.head(8).assign(service=lambda d: d.service.str.replace("socialnetwork-", "")).round(1))

# %% [markdown]
# ### LOOK: the incident as a graph (who is the source, who are the victims, why)

# %%
def layers(services, edges, max_col=7):
    """Layered layout: callers on the left, callees on the right (longest path from entry points).
    Long columns wrap into sub-columns; with no edges at all, a circle."""
    if not edges:
        ang = np.linspace(0, 2 * np.pi, len(services), endpoint=False)
        return {s: (3 * np.cos(a), 3 * np.sin(a)) for s, a in zip(services, ang)}
    lvl = {s: 0 for s in services}
    for _ in range(len(services)):
        changed = False
        for c, e in edges:
            if lvl[e] < lvl[c] + 1 and lvl[c] + 1 < len(services):
                lvl[e] = lvl[c] + 1; changed = True
        if not changed:
            break
    cols = {}
    for s in services:
        cols.setdefault(lvl[s], []).append(s)
    pos, x0 = {}, 0.0
    for L in sorted(cols):
        members = cols[L]; n_sub = (len(members) - 1) // max_col + 1
        for k, s in enumerate(members):
            sub, row = divmod(k, max_col); in_sub = min(max_col, len(members) - sub * max_col)
            pos[s] = (x0 + sub * 0.9, row - (in_sub - 1) / 2)
        x0 += 0.9 * n_sub + 1.2
    return pos

def draw_incident(p, att, truth=None, title="", short=lambda s: s.replace("socialnetwork-", "").replace("-1", "")):
    top = list(att.service[:8]) + ([truth] if truth and truth not in set(att.service[:8]) else [])
    near = [x for c, e in p.edges for x in (c, e) if (c in top or e in top) and x not in top]     # their callers and callees
    names = set(top) | set(list(dict.fromkeys(near))[:10])
    edges = [(c, e) for c, e in p.edges if c in names and e in names]
    pos = layers(sorted(names), edges); sc_ = dict(zip(att.service, att.score)); rank = {s: i + 1 for i, s in enumerate(att.service)}
    fig, axs = plt.subplots(1, 2, figsize=(15, 5), gridspec_kw={"width_ratios": [1.4, 1]})
    ax = axs[0]
    for c, e in edges:
        ax.annotate("", pos[e], pos[c], arrowprops=dict(arrowstyle="->", color="#999", lw=1, shrinkA=12, shrinkB=12))
    mx = max(att.score.max(), 1e-9)
    for s in names:
        v = min(sc_.get(s, 0), mx) / mx
        ax.scatter(*pos[s], s=300 + 1500 * v, c=[plt.cm.Reds(.15 + .85 * v)], edgecolors="k" if s != truth else "lime", linewidths=1 if s != truth else 3, zorder=3)
        ax.text(pos[s][0], pos[s][1] - .32, f"#{rank.get(s,'-')} {short(s)}", ha="center", fontsize=7)
    ax.set_title(title + "  (arrow = calls; red = higher score; green ring = TRUE root from the ledger)"); ax.axis("off")
    top = att.head(8)[::-1]
    axs[1].barh(top.service.map(short), top.own, color="#e63946", label="own evidence")
    axs[1].barh(top.service.map(short), top.unexplained, left=0, color="#457b9d", alpha=.6, label="unexplained symptoms")
    axs[1].barh(top.service.map(short), -top.explained, color="#bbb", label="explained by a broken callee (shown left)")
    axs[1].axvline(0, c="k", lw=.8); axs[1].legend(fontsize=7); axs[1].set_title("why each service got its score")
    plt.tight_layout(); plt.show()

flowchart(5); plt.show()
draw_incident(P_DS, ATT, truth=ev["container"], title="DeathStar real crash")

# %% [markdown]
# ## 7. STEP 6: RISK (who is next?)
# Risk of a healthy caller = 1 - prod(1 - severity(callee) x P(failure crosses the edge)). P starts at 0.5 (structure only) and can be learned across incidents. **Honest status:** in earlier tests learning edge probabilities helped in a 17-service app and was unclear at 100 services; treat risk as a *ranking of who to watch*, not a calibrated probability.

# %%
def risk(p, sc, fl, t, tau, edge_prob=None):
    idx = {s: i for i, s in enumerate(p.services)}; out = {}
    for c, e in p.edges:
        if fl[t, idx[e]] and not fl[t, idx[c]]:
            sev = min(1.0, sc.zs[t, idx[e]] / (2 * tau))
            out[c] = 1 - (1 - out.get(c, 0.0)) * (1 - sev * (edge_prob or {}).get((c, e), 0.5))
    return pd.Series(out, dtype=float).sort_values(ascending=False)

F_DS = flags_for(S_DS, 6.0, 2)
print("at risk 20 s after the stop:"); display(risk(P_DS, S_DS, F_DS, int(np.searchsorted(P_DS.times, ev["t_stop"])) + 2, 6.0).round(2))

# %% [markdown]
# ## 8. THE TEST BENCH: change anything, measure accuracy
# **How the labelled faults are made.** 77 min of *real healthy* OTel traffic is extended to ~10 h by playing it forwards and backwards (no splices, values stay continuous). Then faults are injected at random times on random services with enough data; each injection is written to the ledger. Four fault types, each with the **assumption** it encodes (because a semi-synthetic bench is only as honest as its assumptions):
#
# | type | root | callers (up to 2 hops) | assumption |
# |---|---|---|---|
# | `slow` | latency and self time x2-5 | end-to-end latency up (weaker per hop), self time unchanged | the time is spent *inside* the root |
# | `errors` | error rate 20-60% | error rate up (x0.6 per hop) | errors propagate upward |
# | `crash` | no data, container_up = 0 | errors 30-90%, latency x1.5 | callers see failures |
# | `hang` | no data, container_up stays 1 | latency x3-8 (timeouts), some errors | **hard case**: root is frozen, not gone |
#
# Metrics: **recall** = the root itself got flagged during its fault; **A@1 / A@3** = the root is first / in the top 3 of the ranking for the fault window (time given, like the benchmarks); **delay**; **false alarms/h** on all healthy ticks. Baselines: `most_abnormal`, `earliest`, `random`, and `original` (the original notebook: whole-dataset z > 3, rank by count).

# %%
def callers_of(edges):
    up = {}
    for c, e in edges:
        up.setdefault(e, []).append(c)
    return up

def make_bench(seed=0, tiles=8, gap=(40, 60), dur=(8, 16), kinds=("slow", "errors", "crash", "hang")):
    rng = np.random.default_rng(seed)
    base = panel_from_otel(OTEL)
    X = np.concatenate([base.X if i % 2 == 0 else base.X[::-1] for i in range(tiles)])
    T = X.shape[0]; times = base.times[0] + np.arange(T) * base.step
    clean = Panel(times, base.services, base.features, X.copy(), base.edges, base.step)
    fi = {f: i for i, f in enumerate(base.features)}
    valid = np.mean(~np.isnan(base.X[:, :, fi["latency_p95"]]), axis=0)
    eligible = [i for i in range(len(base.services)) if valid[i] >= 0.4]
    up = callers_of(base.edges); sidx = {s: i for i, s in enumerate(base.services)}
    ledger, t = [], 160
    while t + 20 < T:
        r = int(rng.choice(eligible)); kind = str(rng.choice(kinds)); d = int(rng.integers(*dur)); a, b = t, t + d
        hop1 = [sidx[c] for c in up.get(base.services[r], [])]
        hop2 = [sidx[c2] for c in hop1 for c2 in up.get(base.services[c], [])]
        seg = X[a:b]
        if kind == "slow":
            m = rng.uniform(2, 5)
            seg[:, r, fi["latency_p95"]] *= m; seg[:, r, fi["self_latency"]] *= m
            for hop, hs in ((1, hop1), (2, hop2)):
                for c in hs:
                    if rng.random() < .8: seg[:, c, fi["latency_p95"]] *= 1 + (m - 1) * .7 ** hop
        elif kind == "errors":
            e = rng.uniform(.2, .6)
            seg[:, r, fi["trace_errors"]] = np.where(np.isnan(seg[:, r, fi["trace_errors"]]), np.nan, np.maximum(seg[:, r, fi["trace_errors"]], e))
            for hop, hs in ((1, hop1), (2, hop2)):
                for c in hs:
                    v = seg[:, c, fi["trace_errors"]]; seg[:, c, fi["trace_errors"]] = np.where(np.isnan(v), np.nan, np.maximum(v, e * .6 ** hop))
        elif kind in ("crash", "hang"):
            for f in ("latency_p95", "trace_errors", "span_rate", "self_latency"):
                seg[:, r, fi[f]] = np.nan
            if kind == "crash":
                seg[:, r, fi["container_up"]] = 0.0
            e = rng.uniform(.3, .9) if kind == "crash" else rng.uniform(.1, .4)
            lm = 1.5 if kind == "crash" else rng.uniform(3, 8)
            for hop, hs in ((1, hop1), (2, hop2)):
                for c in hs:
                    v = seg[:, c, fi["trace_errors"]]; seg[:, c, fi["trace_errors"]] = np.where(np.isnan(v), np.nan, np.maximum(v, e * .5 ** (hop - 1)))
                    seg[:, c, fi["latency_p95"]] *= 1 + (lm - 1) * .5 ** (hop - 1)
        ledger.append({"root": base.services[r], "kind": kind, "a": a, "b": b})
        t = b + int(rng.integers(*gap))
    return clean, Panel(times, base.services, base.features, X, base.edges, base.step), ledger

def original_method(p, a=None, b=None):
    """The original notebook: per service/feature z over the WHOLE dataset (mean/std, raw scale), anomaly = |z| > 3."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        Zw = np.abs((p.X - np.nanmean(p.X, axis=0)) / np.nanstd(p.X, axis=0))
    return np.nan_to_num(np.nanmax(np.where(np.isnan(Zw), -1, Zw), axis=2), nan=0) > 3

def rank_window(method, p, sc, fl, a, b, cfg, rng):
    if method == "ours":
        return list(attribute(p, sc, (a, b), cfg["gamma"], cfg["hard"], cfg["infer"], cfg["agg"]).service)
    if method == "most_abnormal":
        return [p.services[i] for i in np.argsort(-sc.zs[a:b].max(axis=0))]
    if method == "earliest":
        first = np.where(fl[a:b].any(axis=0), np.argmax(fl[a:b], axis=0), 10 ** 6)
        return [p.services[i] for i in np.lexsort((-sc.zs[a:b].max(axis=0), first))]
    if method == "random":
        return list(rng.permutation(p.services))
    if method == "original":
        return [p.services[i] for i in np.argsort(-fl[a:b].sum(axis=0), kind="stable")]

DEFAULT = dict(window=60, min_base=12, persistence=2, budget=2.0, common_frac=0.5, gamma=1.0, hard=True, infer=True,
               log_scale=True, self_heal=True, tail_q=0.9, binomial=True, per_series=True, smooth=1, agg="max", method="ours", seed=0)
_BENCH, _SCORES = {}, {}

def run(cfg=None, verbose=False, **over):
    cfg = {**DEFAULT, **(cfg or {}), **over}
    if cfg["seed"] not in _BENCH:
        _BENCH[cfg["seed"]] = make_bench(cfg["seed"])
    clean, p, ledger = _BENCH[cfg["seed"]]
    rng = np.random.default_rng(cfg["seed"])
    kw = dict(window=cfg["window"], min_base=cfg["min_base"], common_frac=cfg["common_frac"], log_scale=cfg["log_scale"], self_heal=cfg["self_heal"], tail_q=cfg["tail_q"], binomial=cfg["binomial"], smooth=cfg["smooth"])
    key = (cfg["seed"], tuple(sorted(kw.items())))
    if key not in _SCORES:
        _SCORES[key] = (score(p, **kw), score(clean, **kw))
    sc, sc_clean = _SCORES[key]
    if cfg["per_series"]:
        sc, sc_clean = normalise(sc, sc_clean, features=p.features), normalise(sc_clean, sc_clean, features=p.features)
    if cfg["method"] == "original":
        fl = original_method(p); tau = float("nan")
    else:
        tau = calibrate(sc_clean, p.step, cfg["budget"], cfg["persistence"])   # threshold from healthy history only
        fl = flags_for(sc, tau, cfg["persistence"])
    rows, healthy = [], np.ones(len(p.times), bool)
    for f in ledger:
        a, b = f["a"], f["b"] + 4; healthy[max(f["a"] - 2, 0):b + 4] = False
        j = p.services.index(f["root"])
        hit = fl[a:b, j].any()
        order = rank_window(cfg["method"], p, sc, fl, f["a"], b, cfg, rng)
        rk = order.index(f["root"]) + 1
        rows.append(dict(kind=f["kind"], root=f["root"], recall=hit, any_flag=fl[a:b].any(), delay_s=(np.argmax(fl[a:b, j]) * p.step) if hit else np.nan,
                         rank=rk, A1=rk == 1, A3=rk <= 3))
    R = pd.DataFrame(rows)
    fa = episodes_per_hour(fl[healthy], p.step)
    summary = dict(tau=tau, faults=len(R), recall=R.recall.mean(), A1=R.A1.mean(), A3=R.A3.mean(), delay_s=R.delay_s.mean(), false_alarms_h=fa,
                   **{f"A1_{k}": g.A1.mean() for k, g in R.groupby("kind")}, **{f"recall_{k}": g.recall.mean() for k, g in R.groupby("kind")})
    if verbose:
        display(R.groupby("kind")[["recall", "A1", "A3", "delay_s"]].mean().round(2))
    return summary, R

t0_ = time.time(); BASE, BASE_R = run(verbose=True); print(f"default run: {time.time()-t0_:.1f}s, {BASE['faults']} faults")
print({k: round(v, 3) if isinstance(v, float) else v for k, v in BASE.items()})

# %% [markdown]
# ### Ablations and baselines: what each step is worth
# Each row turns ONE thing off (or swaps the ranking method). Green = better than our default, red = worse. **This table is the evidence for every design choice above.**

# %%
VARIANTS = {
    "ours (default)": {}, "no self-healing baseline": dict(self_heal=False), "no log scale": dict(log_scale=False),
    "no common-mode": dict(common_frac=None), "no tail-aware spread": dict(tail_q=None), "no binomial errors": dict(binomial=False), "no per-series normalisation": dict(per_series=False), "no explain-away (gamma=0)": dict(gamma=0.0), "no crash bonus": dict(hard=False),
    "no blind-spot inference": dict(infer=False), "persistence 1": dict(persistence=1), "persistence 3": dict(persistence=3),
    "BASELINE most_abnormal": dict(method="most_abnormal"), "BASELINE earliest": dict(method="earliest"),
    "BASELINE random": dict(method="random"), "BASELINE original notebook": dict(method="original"),
}
def compare(variants, cols=("recall", "A1", "A3", "A1_slow", "A1_errors", "A1_crash", "A1_hang", "delay_s", "false_alarms_h", "tau")):
    tab = pd.DataFrame({name: run(v)[0] for name, v in variants.items()}).T[list(cols)].astype(float).round(3)
    ref = tab.iloc[0]
    def colour(col):
        better_low = col.name in ("delay_s", "false_alarms_h")
        return [("background-color:#d8f3dc" if (v < ref[col.name] if better_low else v > ref[col.name]) else
                 "background-color:#ffd6d6" if (v > ref[col.name] if better_low else v < ref[col.name]) else "") for v in col]
    try:
        display(tab.style.apply(colour, axis=0).format("{:.3f}"))
    except Exception:
        display(tab)
    return tab

ABL = compare(VARIANTS)

# %% [markdown]
# ### Sensitivity: sweep one knob, watch accuracy and false alarms move

# %%
def sweep(param, values, **fixed):
    res = [run({**fixed, param: v})[0] for v in values]
    fig, ax = plt.subplots(1, 2, figsize=(13, 3))
    for m in ("recall", "A1", "A3"):
        ax[0].plot(values, [r[m] for r in res], "o-", label=m)
    ax[0].set_ylim(0, 1.02); ax[0].legend(); ax[0].set_xlabel(param); ax[0].set_title(f"accuracy vs {param}")
    ax[1].plot(values, [r["false_alarms_h"] for r in res], "o-", c="C3"); ax[1].set_xlabel(param); ax[1].set_title("false alarms / hour")
    plt.show()
    return pd.DataFrame(res, index=values)[["recall", "A1", "A3", "false_alarms_h", "tau"]].round(3)

display(sweep("budget", [0.5, 1, 2, 5, 10]))
display(sweep("window", [20, 40, 60, 100, 160]))

# %% [markdown]
# ### YOUR experiment
# Change anything in `MY` (or edit any function above and re-run its cell), then run this cell. It prints your numbers next to the default. Ideas worth testing for the paper:
# * the **hang** row is the weak spot: a frozen service has no data, so only *silence* points at it. Idea: add a "went silent while its callers are calling it" feature in `prepare`/`score` and see if `A1_hang` rises without hurting the rest.
# * use `seed=1, 2, 3` to check a gain is not luck (different fault times/targets).
# * try `gamma=0.7` (partial explain-away) or `common_frac=0.7`.

# %%
MY = dict(gamma=0.7, persistence=2, budget=2.0)
mine = compare({"ours (default)": {}, "MY": MY, "MY seed 1": {**MY, "seed": 1}, "default seed 1": {"seed": 1}})

# %% [markdown]
# ### LOOK: one injected fault from the bench, end to end

# %%
clean_, p_, ledger_ = _BENCH[0]
f_ = next(f for f in ledger_ if f["kind"] == "slow")
sc_ = score(p_); tau_ = calibrate(score(clean_), p_.step); fl_ = flags_for(sc_, tau_, 2)
a_, b_ = f_["a"], f_["b"] + 4
fig, ax = plt.subplots(figsize=(13, 3.8))
lo_, hi_ = a_ - 40, b_ + 20
top_ = np.argsort(-sc_.zs[a_:b_].max(axis=0))[:10]
ax.imshow(np.minimum(sc_.zs[lo_:hi_, top_].T, 30), aspect="auto", cmap="magma", extent=[lo_, hi_, len(top_) - .5, -.5])
ax.set_yticks(range(len(top_))); ax.set_yticklabels([p_.services[i] for i in top_])
ax.axvspan(f_["a"], f_["b"], color="cyan", alpha=.25); ax.set_title(f"bench fault: {f_['kind']} on {f_['root']} (cyan = ledger); tau = {tau_}"); plt.show()
draw_incident(p_, attribute(p_, sc_, (a_, b_)), truth=f_["root"], title=f"bench: {f_['kind']} on {f_['root']}", short=lambda s: s)

# %% [markdown]
# ## 9. The REAL fault: DeathStar crash, with every switch
# One real run only, the easy fault type (a crash). It shows what each component does on real data; it is **not** a general accuracy number.

# %%
def ds_case(track_presence=True, edges=True, hard=True, common_frac=0.5, gamma=1.0):
    p = prepare(DS, step=10, track_presence=track_presence, edges=DS_EDGES if edges else None)
    sc = score(p, window=30, min_base=8, common_frac=common_frac)
    a = int(np.searchsorted(p.times, ev["t_stop"])) - 2; b = int(np.searchsorted(p.times, ev["t_start"])) + 1
    att = attribute(p, sc, (a, b), gamma=gamma, hard=hard)
    fl = flags_for(sc, 6.0, 2)
    return dict(rank_of_true_root=int(att.index[att.service == ev["container"]][0]) + 1 if ev["container"] in set(att.service) else None,
                top1=att.service[0].replace("socialnetwork-", ""), false_flags_before_fault=int(fl[:a].sum()))

display(pd.DataFrame({
    "full method": ds_case(), "no crash signal (container_up)": ds_case(track_presence=False), "no crash bonus": ds_case(hard=False),
    "no wiring edges": ds_case(edges=False), "no crash bonus + no common-mode": ds_case(hard=False, common_frac=None),
    "no crash bonus + no edges": ds_case(hard=False, edges=False)}).T)

# %% [markdown]
# ## 10. Your labelled CSV (`ml-dataset-labeled.csv`)
# Same pipeline; truth = `anomaly_label`. Compared with the original notebook's approach on the same rows. Runs only if the file already sits next to the notebook or in `/content/drive/MyDrive/`; otherwise skipped (no upload prompt).

# %%
CSV = next((c for c in ("ml-dataset-labeled.csv", "/content/ml-dataset-labeled.csv", "/content/drive/MyDrive/ml-dataset-labeled.csv") if os.path.exists(c)), None)
SOCK_EDGES = [("front-end", "catalogue"), ("front-end", "carts"), ("front-end", "orders"), ("front-end", "user"), ("orders", "carts"), ("orders", "user"),
              ("orders", "payment"), ("orders", "shipping"), ("orders", "orders-db"), ("carts", "carts-db"), ("catalogue", "catalogue-db"), ("user", "user-db"),
              ("shipping", "rabbitmq"), ("queue-master", "rabbitmq")]
if CSV:
    raw = pd.read_csv(CSV)
    pc = prepare(raw, track_presence=False, edges=SOCK_EDGES)
    scc = score(pc, window=80, min_base=20)
    y = raw["anomaly_label"].astype(bool)
    def rows_flagged(p, fl):
        tick = {int(round(t / p.step)): i for i, t in enumerate(p.times)}; sm = {s: i for i, s in enumerate(p.services)}
        ts = pd.to_datetime(raw["timestamp"], utc=True).astype("int64").to_numpy() / 1e9
        return pd.Series([bool(fl[tick[int(np.floor(t / p.step))], sm[s]]) if int(np.floor(t / p.step)) in tick else False for t, s in zip(ts, raw["service"])], index=raw.index)
    res = {}
    for name, fl in (("ours budget 2/h", flags_for(scc, calibrate(scc, pc.step, 2.0), 2)), ("ours budget 10/h", flags_for(scc, calibrate(scc, pc.step, 10.0), 2)),
                     ("original notebook (|z|>3 whole data)", original_method(pc))):
        pred = rows_flagged(pc, fl); tp = int((pred & y).sum()); fp = int((pred & ~y).sum()); fn = int((~pred & y).sum())
        res[name] = dict(flagged_rows=int(pred.sum()), precision=tp / max(tp + fp, 1), recall=tp / max(tp + fn, 1))
    display(pd.DataFrame(res).T.round(3))
    print("labelled anomalies per service:", dict(raw.loc[y, "service"].value_counts()))
else:
    print("CSV not found: skipped.")

# %% [markdown]
# ## 11. LIVE on your AWS hosts (same pipeline, ledger-scored)
# **Nothing to upload.** The key comes from the Colab secret `SSH_KEY` (key icon on the left, notebook access ON). Host IPs are built in below; a secret `HOSTS` (same JSON shape) overrides them if your IPs change.
# The sampler only runs read-only `docker stats` / `docker ps` / `docker logs --since`. The injector only runs `docker stop|start|pause|unpause` on a container that `docker ps` lists, and writes the ledger.
#
# Cells in order: **11a** check key + hosts -> **11b** start watching -> **11c** collect healthy minutes and analyse -> **11d** (optional) inject a fault, recover, score it against the ledger.

# %%
# 11a. key + host check
HOSTS = {"death-star": ["13.233.8.32", "/home/ubuntu/DeathStarBench/socialNetwork/docker-compose.yml"],
         "sock-shop": ["15.207.109.141", None], "open-telemetry": ["13.201.89.80", None], "shopflowbench": ["13.203.200.52", None]}
KEY = os.environ.get("RCA_KEY", "/content/key.pem")
LIVE = {}

def _secret(name):
    try:
        from google.colab import userdata
        return userdata.get(name)
    except Exception:
        return None

def live_setup():
    """Install deps, load rca_lite (sampler + injector), write the key from the secret, return the module."""
    import importlib, sys, subprocess
    if IN_COLAB:
        subprocess.run([sys.executable, "-m", "pip", "-q", "install", "paramiko", "pyyaml"], check=False)
    sys.path.insert(0, os.path.dirname(os.path.abspath(fetch("colab/rca_lite.py"))))
    import rca_lite; importlib.reload(rca_lite)
    global HOSTS
    h = _secret("HOSTS")
    if h:
        HOSTS = json.loads(h)
    if not os.path.exists(KEY):
        k = _secret("SSH_KEY")
        if not k:
            raise RuntimeError("No SSH key: add a Colab secret named SSH_KEY (full .pem text) and enable notebook access, then re-run.")
        k = k.strip().replace("\\n", chr(10))                     # a key pasted as one line with literal \n also works
        if not k.startswith("-----BEGIN"):
            raise RuntimeError("SSH_KEY does not look like a .pem (it must start with -----BEGIN and end with -----END).")
        open(KEY, "w").write(k + chr(10)); os.chmod(KEY, 0o600)
    return rca_lite

def check_hosts():
    L = live_setup(); ok = {}
    for n, (ip, compose) in HOSTS.items():
        try:
            names = L.HostSampler(ip, KEY, "ubuntu", name=n).containers()
            ok[n] = f"OK: {len(names)} containers"
        except Exception as e:
            ok[n] = f"FAILED: {type(e).__name__}: {str(e)[:90]}"
    display(pd.Series(ok, name="ssh check"))
    return ok

RUN_LIVE = IN_COLAB or bool(os.environ.get("RCA_KEY"))
HOST_OK = check_hosts() if RUN_LIVE else {}
if not RUN_LIVE:
    print("Not on Colab and no RCA_KEY set: live section skipped.")

# %%
# 11b. start watching every host that answered (background threads; data accumulate while you read)
def watch(*names, every_s=10):
    L = live_setup()
    for n in names:
        if n in LIVE:
            continue
        ip, compose = HOSTS[n]
        s = L.HostSampler(ip, KEY, "ubuntu", name=n)
        try:
            edges = s.compose_edges(compose) if compose else []
        except Exception:
            edges = []
        LIVE[n] = dict(sampler=s.start(every_s), chaos=L.Chaos(s), edges=edges)
        print(f"{n}: sampling every {every_s}s, {len(edges)} wiring edges")

def stop_watching():
    for v in LIVE.values():
        v["sampler"].stop()

if RUN_LIVE:
    watch(*[n for n, v in HOST_OK.items() if v.startswith("OK")])

# %%
# 11c. collect, then analyse (re-run any time; the first ~5 min are the healthy baseline).
# The first ticks after the baseline fills often look bright on the heatmap (thin baseline); they only count if they cross tau.
LIVE_MINUTES = float(os.environ.get("RCA_LIVE_MINUTES", 5))

def live_frame(minutes=None):
    fr = [v["sampler"].frame() for v in LIVE.values() if v["sampler"].rows]
    if not fr:
        return pd.DataFrame()
    df = pd.concat(fr, ignore_index=True)
    return df if not minutes else df[df.timestamp >= df.timestamp.max() - pd.Timedelta(minutes=minutes)]

def wait_for(minutes):
    t_end = time.time() + 60 * minutes
    while time.time() < t_end:
        n = sum(len(v["sampler"].rows) for v in LIVE.values())
        errs = {k: v["sampler"].last_error for k, v in LIVE.items() if v["sampler"].last_error}
        print(f"\r{(t_end - time.time()) / 60:4.1f} min left | {n} rows {errs or ''}", end="")
        time.sleep(10)
    print()

def analyse_live(minutes=60, step=10, budget=2.0, persistence=2, show=True):
    df = live_frame(minutes)
    if df.empty:
        print("no live data yet"); return None
    p = prepare(df, step=step, track_presence=True, edges=[e for v in LIVE.values() for e in v["edges"]])
    sc = score(p, window=60, min_base=12)
    led = [r for v in LIVE.values() for r in v["chaos"].ledger]
    healthy = np.ones(len(p.times), bool)
    for r in led:
        healthy[max(int(np.searchsorted(p.times, r["start"])) - 2, 0):int(np.searchsorted(p.times, r["end"])) + 8] = False
    ref = Scores(sc.z[healthy], sc.med[healthy], sc.scale[healthy], sc.own[healthy], sc.sym[healthy], sc.zs[healthy], sc.judged[healthy], sc.common[healthy])
    scn = normalise(sc, ref, features=p.features); refn = normalise(ref, ref, features=p.features)
    tau = calibrate(refn, p.step, budget, persistence); fl = flags_for(scn, tau, persistence)
    print(f"{len(p.times)} ticks ({len(p.times) * step / 60:.0f} min) x {len(p.services)} containers | tau={tau} | "
          f"false alarms on healthy ticks: {episodes_per_hour(fl[healthy], p.step):.1f}/h")
    if show:
        top = np.argsort(-scn.zs.max(axis=0))[:15]
        fig, ax = plt.subplots(figsize=(13, 4.5))
        ax.imshow(np.minimum(scn.zs[:, top].T, 10), aspect="auto", cmap="magma"); ax.set_yticks(range(len(top)))
        ax.set_yticklabels([p.services[i].replace("socialnetwork-", "") for i in top], fontsize=7)
        for r in led:
            ax.axvspan(np.searchsorted(p.times, r["start"]), np.searchsorted(p.times, r["end"]), color="cyan", alpha=.25)
        ax.set_title("LIVE: deviation per container (bright = unusual); cyan = faults in the ledger"); plt.show()
    out = []
    for r in led:
        a = max(int(np.searchsorted(p.times, r["start"])) - 1, 0); b = int(np.searchsorted(p.times, r["end"])) + 4
        att = attribute(p, scn, (a, b)); j = next(i for i, s in enumerate(att.service) if r["service"] in s)
        out.append(dict(kind=r["kind"], service=r["service"], seconds=round(r["end"] - r["start"]),
                        flagged=bool(fl[a:b, p.services.index(att.service[j])].any()), true_root_rank=j + 1, predicted_top1=att.service[0]))
        if show:
            draw_incident(p, att, truth=att.service[j], title=f"LIVE {r['kind']} on {r['service']}")
    if out:
        display(pd.DataFrame(out))
    elif fl[-6:].any():
        display(attribute(p, scn, (len(p.times) - 12, len(p.times))).head(5))
    else:
        print("All clear: no service flagged in the last minute.")
    return p, scn, fl

if RUN_LIVE and LIVE:
    wait_for(LIVE_MINUTES)
    LIVE_RESULT = analyse_live()

# %%
# 11d. OPTIONAL: cause a fault on YOUR lab and score it. Set DO_FAULT = True, pick the container, run the cell.
# "stop" = crash (easy); "pause" = frozen process, Docker still lists it (the hard case, not validated yet).
DO_FAULT, FAULT_HOST, FAULT_CONTAINER, FAULT_KIND, FAULT_SECONDS = False, "death-star", "socialnetwork-post-storage-service-1", "pause", 90
if RUN_LIVE and DO_FAULT:
    ch = LIVE[FAULT_HOST]["chaos"]
    try:
        ch.inject(FAULT_CONTAINER, FAULT_KIND); print(time.strftime("%H:%M:%S"), "INJECTED", FAULT_KIND, FAULT_CONTAINER)
        time.sleep(FAULT_SECONDS)
    finally:
        for r in ch.recover_all():                               # always recover, even if the cell is interrupted
            print(time.strftime("%H:%M:%S"), "RECOVERED", r["service"], f"after {r['end'] - r['start']:.0f}s")
    wait_for(2)
    LIVE_RESULT = analyse_live()
