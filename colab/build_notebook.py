"""Builds colab/rca_live_colab.ipynb (embeds rca_lite.py so the notebook is self-contained)."""
import json
import pathlib

here = pathlib.Path(__file__).parent
lite = (here / "rca_lite.py").read_text(encoding="utf-8")
cells = []


def md(s):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n").splitlines(True)})


def code(s):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n").splitlines(True)})


md('''
# Live RCA lab: find the broken service, check it against what we really broke
**Two ways to use it.** *Part A* is three buttons. *Part B* has every knob, a fault injector and an *actual vs predicted* scoreboard. *Part C* runs the same method on your labelled CSV.

**How we know a fault is real (and not just the architecture's normal behaviour)**
1. *Healthy* = what the system does before and between faults. The detector learns it on the fly from the last samples (no labels, no training), and the threshold is picked so healthy data raises at most N false alarms per hour.
2. *Actual faults* = the **fault ledger**: the injector writes time and container of every fault *at the moment it is injected*, so the truth never comes from our own detector.
3. *Predicted* = what the detector flagged and which service it ranked first. Part B compares both: detected?, delay, true root ranked #1?, false alarms per healthy hour.
4. A flag with no ledger entry is only *suspicious*; the scoreboard counts it as a false alarm. For a user-facing cross-check, run a small load script against the app and compare its error rate with the flags.
''')
code('''
# 0. setup (about 20 s)
!pip -q install paramiko pyyaml ipywidgets
''')
cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": ["%%writefile rca_lite.py\n"] + lite.splitlines(True)})
code('''
# 1. hosts + SSH key (IPs from a Colab secret; the key stays in this Colab session only; nothing is stored in the notebook)
import os, time, numpy as np, pandas as pd, matplotlib.pyplot as plt
import ipywidgets as W
from IPython.display import display, clear_output
import rca_lite as L

# Lab IPs are NOT stored in this (public) notebook. Put them in a Colab secret named HOSTS (Secrets tab, key icon) as JSON like
#   {"sock-shop": ["1.2.3.4", null], "death-star": ["5.6.7.8", "/home/ubuntu/DeathStarBench/socialNetwork/docker-compose.yml"]}
# (second item = compose file with the service wiring, or null). Or just edit the placeholders below.
import json as _json
HOSTS = {"sock-shop": ("EDIT.ME.IP", None), "death-star": ("EDIT.ME.IP", "/home/ubuntu/DeathStarBench/socialNetwork/docker-compose.yml"),
         "open-telemetry": ("EDIT.ME.IP", None), "shopflowbench": ("EDIT.ME.IP", None)}
try:
    from google.colab import userdata
    HOSTS = {k: tuple(v) for k, v in _json.loads(userdata.get("HOSTS")).items()}
except Exception:
    pass
USER = "ubuntu"
KEY = "/content/key.pem"
if not os.path.exists(KEY):
    try:                                      # preferred: Colab secret SSH_KEY = the full text of your .pem (set once, never in the repo)
        from google.colab import userdata
        open(KEY, "w").write(userdata.get("SSH_KEY").strip() + chr(10)); os.chmod(KEY, 0o600)
    except Exception:
        pass
if not os.path.exists(KEY):
    from google.colab import files
    up = files.upload()                       # choose your .pem
    open(KEY, "wb").write(next(iter(up.values()))); os.chmod(KEY, 0o600)
STATE = {"samplers": {}, "edges": {}, "chaos": {}}
print("key ready; hosts:", ", ".join(HOSTS))
''')
code('''
# 2. shared helpers (used by Part A and B)
def connect(selected, every_s=10):
    for name in selected:
        if name in STATE["samplers"]: continue
        ip, compose = HOSTS[name]
        s = L.HostSampler(ip, KEY, USER, name=name)
        try:
            names = s.containers()
            STATE["edges"][name] = s.compose_edges(compose) if compose else []
        except Exception as e:
            print(f"{name}: cannot connect ({type(e).__name__}: {str(e)[:80]})"); continue
        STATE["samplers"][name] = s.start(every_s)
        STATE["chaos"][name] = L.Chaos(s)
        print(f"{name}: watching {len(names)} containers, {len(STATE['edges'][name])} wiring edges")

def disconnect():
    for s in STATE["samplers"].values(): s.stop()
    STATE["samplers"].clear()

def all_frame(minutes=None):
    fr = [s.frame() for s in STATE["samplers"].values() if s.rows]
    if not fr: return pd.DataFrame()
    df = pd.concat(fr, ignore_index=True)
    if minutes: df = df[df.timestamp >= df.timestamp.max() - pd.Timedelta(minutes=minutes)]
    return df

def analyse(df, window=60, min_base=12, persistence=2, budget=2.0, common_frac=0.5, gamma=1.0, infer=True, use_up=True, step=10):
    p = L.prepare(df, step=step, track_presence=use_up)
    edges = [e for v in STATE["edges"].values() for e in v]
    p.edges = L.match_edges(edges, p.services) if edges else []
    sc = L.score(p, window=window, min_base=min_base, common_frac=common_frac)
    tau = L.calibrate(sc, p.step, budget, persistence)
    flags = L.flags_for(sc, tau, persistence)
    return p, sc, tau, flags

def short(s): return s.replace("socialnetwork-", "").replace("-1", "")
''')
md('''
## How it works (read this once)
**The idea in one sentence:** every service is compared with *its own recent past*; a service that moves far from itself, in the bad direction, and stays there, is flagged; then we work out which flagged service is the *source* and which are only *victims*.

| Step | What happens | Why |
|---|---|---|
| 1. Prepare | Cumulative counters (network, disk) become per-second rates. The first sample after any gap is dropped. A container missing from `docker stats` becomes `container_up = 0`. | Raw cumulative counters only ever go up, and the first row has a log backlog; both fake anomalies in the original notebook. |
| 2. Score | For each service and metric: how many "typical deviations" (robust z-score, log scale) is it above its own last *window* samples? Only the bad direction counts. Samples that were themselves anomalous never enter the baseline. | No labels, no training; the baseline follows slow drift but a long fault never becomes "normal". |
| 3. Threshold | The alarm level **tau** is the smallest value that keeps false alarms on this data under your *false/h* budget. A flag needs *persist* consecutive ticks. | You choose how many false alarms you can live with; the data does the rest. |
| 4. Common-mode | If more than *load share* of the services move together on a metric, the shared part is removed. | A traffic burst moves everything; it is load, not 20 simultaneous faults. |
| 5. Attribute | Score of a service = max(**own evidence**: CPU, memory, pids, disk, container_up; **unexplained symptoms**: errors/latency/traffic that no callee already shows). A stopped container ranks first (hard evidence). A service with no telemetry can be inferred from its callers. | Victims only echo their callee's symptoms, so their unexplained part is small. |
| 6. Risk | A healthy caller of a flagged service gets risk = severity x probability the failure crosses that edge (learned across incidents; starts at 0.5). | Tells you who is likely next. |

**How to read the results**
- **Heatmap:** rows are services, columns are time, bright = unusual. Cyan bands are faults *we injected* (the ledger). A good run lights up inside the cyan band and stays dark elsewhere.
- **Scoreboard:** `root_flagged` = the injected service itself was flagged; `delay_s` = seconds from injection to first flag; `true_root_rank` = where the injected service sits in the ranking (1 is best); `top1_correct` = the first name was right; `false alarms/h` = flags outside every fault window.
- **Ledger:** the only source of "actual" truth. Everything the detector says is a *prediction* until it is matched against a ledger row.

**Honest limits:** pause/slow/partial faults are the hard cases and are not validated yet; with sparse data (few requests) latency cannot be judged; wiring edges from compose files can be incomplete, which weakens the victim-vs-source split; thresholds are calibrated on mostly-healthy data, so give it at least 3 healthy minutes first.
''')
md('''
## Part A: the simple version
Three steps: **1** pick hosts and press *Start watching* (wait ~3 min). **2** press *What's wrong right now?* **3** *Stop* when done.
''')
code('''
CSS = """<style>
.card{border-radius:10px;padding:14px 18px;margin:8px 0;font-family:sans-serif;color:#111}
.ok{background:#d9f7e3;border:1px solid #2e9e5b}.bad{background:#ffe0e0;border:1px solid #d33}.warn{background:#fff3cd;border:1px solid #d9a400}
.card h3{margin:0 0 4px 0}.bar{height:14px;border-radius:4px;background:#d33;display:inline-block;vertical-align:middle}
.rk td{padding:3px 10px;font-family:sans-serif;font-size:13px}.help{background:#eef3ff;border-left:4px solid #4a6cf7;padding:8px 12px;margin:6px 0;font-family:sans-serif;font-size:13px;color:#111}
</style>"""
display(W.HTML(CSS))
def card(kind, title, body=""):
    display(W.HTML(f'<div class="card {kind}"><h3>{title}</h3>{body}</div>'))
def bars(att, n=5):
    mx = max(float(att.score.iloc[0]), 1e-9)
    rows = "".join(f'<tr><td>{i+1}</td><td><b>{short(r.service)}</b></td><td><span class="bar" style="width:{max(4, int(220*min(r.score,mx)/mx))}px"></span></td>'
                   f'<td>{r.score:.1f}</td><td>{r.top_feature}</td><td>{r.note}</td></tr>' for i, r in att.head(n).iterrows())
    return f'<table class="rk">{rows}</table>'
def help_box(t): return W.HTML(f'<div class="help">{t}</div>')

host_pick = W.SelectMultiple(options=list(HOSTS), value=tuple(list(HOSTS)[:1]), description="Hosts", rows=4)
b_start, b_now, b_stop = W.Button(description="1  Start watching", button_style="success", icon="play"), W.Button(description="2  What's wrong right now?", button_style="info", icon="search"), W.Button(description="3  Stop", icon="stop")
out_a = W.Output()
def _start(_):
    with out_a: clear_output(); connect(host_pick.value)
def _now(_):
    with out_a:
        clear_output()
        df = all_frame()
        if df.empty: card("warn", "No data yet", "Press Start watching and wait a minute."); return
        mins = (df.timestamp.max() - df.timestamp.min()).total_seconds() / 60
        if mins < 3: card("warn", "Still learning what normal looks like", f"{mins:.1f} min of data so far; wait until about 3 min of healthy behaviour has been seen."); return
        p, sc, tau, flags = analyse(df)
        if not flags[-6:].any():
            card("ok", "All clear", f"Nothing unusual in the last minute. Watching {len(p.services)} services; alarm level tau = {tau}."); return
        att = L.attribute(p, sc, (len(p.times) - 12, len(p.times))); top = att.iloc[0]
        why = top.note or f"strongest unexplained evidence: {top.top_feature}"
        card("bad", f"Most likely broken: {short(top.service)}", f"{why}.<br>{bars(att)}")
        r = L.risk(p, sc, flags, len(p.times) - 1, tau)
        if len(r): card("warn", "Next at risk", ", ".join(f"<b>{short(s)}</b> ({v:.0%})" for s, v in zip(r.service[:3], r.risk[:3])))
b_start.on_click(_start); b_now.on_click(_now); b_stop.on_click(lambda _: disconnect())
display(W.VBox([help_box("<b>Simple mode.</b> Red = something is wrong and the bars show the ranking (longer bar = more likely the source). Green = nothing unusual. Yellow = not enough data yet."),
                host_pick, W.HBox([b_start, b_now, b_stop]), out_a]))
''')
md('''
## Part B: the detailed version
Four tabs: **Connect** (hosts, containers), **Tune** (every knob), **Inject** (cause a real fault and log it), **Results** (actual vs predicted). *Injection works only on containers listed by `docker ps` on the host you pick, only with `docker stop|start|pause|unpause`, only after you tick the ownership box. Every fault is written to the ledger with its exact time.*
''')
code('''
sl = dict(
    window=W.IntSlider(60, min=20, max=200, description="baseline win", style={"description_width": "100px"}),
    min_base=W.IntSlider(12, min=5, max=40, description="min base", style={"description_width": "100px"}),
    persistence=W.IntSlider(2, min=1, max=6, description="persist", style={"description_width": "100px"}),
    budget=W.FloatSlider(2.0, min=0.2, max=20, step=0.2, description="false alarms/h", style={"description_width": "100px"}),
    common_frac=W.FloatSlider(0.5, min=0.2, max=0.95, step=0.05, description="load share", style={"description_width": "100px"}),
    gamma=W.FloatSlider(1.0, min=0, max=1.5, step=0.1, description="explain g", style={"description_width": "100px"}),
    step=W.IntSlider(10, min=5, max=60, description="tick seconds", style={"description_width": "100px"}))
cb_infer, cb_up = W.Checkbox(True, description="infer services with no telemetry"), W.Checkbox(True, description="use container_up (crash signal)")
minutes = W.IntSlider(20, min=3, max=240, description="last minutes", style={"description_width": "100px"})
hosts_b = W.Dropdown(options=list(HOSTS), description="host")
cont = W.Dropdown(options=[], description="container")
kind = W.Dropdown(options=["stop", "pause"], description="fault")
ok = W.Checkbox(False, description="I own this lab; allow injecting this fault")
b_conn, b_refresh, b_inj, b_rec, b_an = (W.Button(description=d, icon=i) for d, i in (("Connect host", "plug"), ("List containers", "refresh"), ("Inject fault", "bolt"), ("Recover", "heartbeat"), ("Analyse + score", "line-chart")))
b_inj.button_style, b_rec.button_style, b_an.button_style, b_conn.button_style = "danger", "success", "info", "success"
out_b, out_l, out_r = W.Output(), W.Output(), W.Output()
def ledger(): return [r for c in STATE["chaos"].values() for r in c.ledger]
def show_ledger():
    with out_l:
        clear_output()
        act = {n: c._open for n, c in STATE["chaos"].items() if c._open}
        if act: card("bad", "Faults currently active", ", ".join(f"<b>{k}</b>: {list(v)}" for k, v in act.items()))
        display(pd.DataFrame(ledger()) if ledger() else W.HTML("<i>fault ledger is empty</i>"))
def _conn(_):
    with out_b: connect([hosts_b.value])
def _refresh(_):
    s = STATE["samplers"].get(hosts_b.value)
    if s: cont.options = sorted(s.containers())
def _inj(_):
    if not ok.value:
        with out_b: card("warn", "Tick the ownership box first")
        return
    STATE["chaos"][hosts_b.value].inject(cont.value, kind.value)
    with out_b: card("bad", f"INJECTED {kind.value} on {cont.value}", time.strftime("%H:%M:%S") + " : wait ~1 min, then press Recover.")
    show_ledger()
def _rec(_):
    for r in STATE["chaos"][hosts_b.value].recover_all():
        with out_b: card("ok", f"Recovered {r['service']}", f"after {r['end']-r['start']:.0f}s. Wait ~1 min, then Analyse.")
    show_ledger()
def _an(_):
    with out_r:
        clear_output()
        df = all_frame(minutes.value)
        if df.empty: card("warn", "No data yet"); return
        p, sc, tau, flags = analyse(df, **{k: v.value for k, v in sl.items()}, infer=cb_infer.value, use_up=cb_up.value)
        ev = L.evaluate(p, sc, flags, ledger(), tau)
        fa = ev["false_alarms_per_hour"]
        card("ok" if fa <= sl["budget"].value else "warn", "Detector health",
             f"{len(p.times)} ticks x {len(p.services)} services, {len(p.edges)} wiring edges. Alarm level tau = <b>{tau}</b> (picked for at most {sl['budget'].value}/h). "
             f"Healthy time {ev['healthy_minutes']:.1f} min, false alarms <b>{fa:.1f}/h</b> ({ev['false_alarm_samples']} flagged service-ticks).")
        f = ev["faults"]
        if len(f):
            hit = int(f.get("top1_correct", pd.Series(dtype=bool)).sum()); det = int(f.get("root_flagged", pd.Series(dtype=bool)).sum())
            card("ok" if hit == len(f) else "warn", "Actual vs predicted", f"faults injected: <b>{len(f)}</b> | root flagged: <b>{det}</b> | ranked #1: <b>{hit}</b>")
            display(f.assign(service=lambda d: d.service.map(short)))
        else:
            card("warn", "No injected faults yet", "Inject one (tab 3), wait ~1 min, recover, wait ~1 min, press Analyse. Without a ledger entry there is no ground truth.")
        top = np.argsort(-sc.zs.max(axis=0))[:15]
        fig, ax = plt.subplots(figsize=(11, 4.5)); im = ax.imshow(np.minimum(sc.zs[:, top].T, 30), aspect="auto", cmap="magma")
        ax.set_yticks(range(len(top))); ax.set_yticklabels([short(p.services[i]) for i in top], fontsize=7); plt.colorbar(im, label="deviation (z)")
        for fr in ledger():
            ax.axvspan(np.searchsorted(p.times, fr["start"]), np.searchsorted(p.times, fr["end"]), color="cyan", alpha=.25)
        ax.set_title("bright = unusual; cyan = faults WE injected"); plt.show()
        if flags[-6:].any():
            att = L.attribute(p, sc, (max(len(p.times) - 24, 0), len(p.times)), gamma=sl["gamma"].value, infer_unobserved=cb_infer.value)
            card("bad", "Current ranking", bars(att, 8))
for b, fn in ((b_conn, _conn), (b_refresh, _refresh), (b_inj, _inj), (b_rec, _rec), (b_an, _an)): b.on_click(fn)
t1 = W.VBox([help_box("<b>Connect.</b> Pick a host and connect: a background sampler reads <code>docker stats</code> (and a log-error count) every 10 s, read-only. Then list its containers."), W.HBox([hosts_b, b_conn, b_refresh]), out_b])
t2 = W.VBox([help_box("<b>Tune.</b> <b>baseline win</b>: how many past ticks define normal (longer = steadier, slower to adapt). <b>min base</b>: samples needed before judging. <b>persist</b>: consecutive ticks above tau to flag (higher = fewer false alarms, slower). <b>false alarms/h</b>: the budget used to pick tau. <b>load share</b>: when this fraction of services move together it is treated as load. <b>explain g</b>: how much of a caller's symptoms a failing callee explains away (0 = none). <b>tick seconds</b>: window size."),
             W.HBox([W.VBox(list(sl.values())[:4]), W.VBox(list(sl.values())[4:] + [minutes])]), W.HBox([cb_infer, cb_up])])
t3 = W.VBox([help_box("<b>Inject.</b> <b>stop</b> kills the container (easy: it disappears). <b>pause</b> freezes it while Docker still lists it (hard: only its callers show errors). Always press <b>Recover</b>. Leave 5+ min healthy between faults, vary targets and types; each one is logged to the ledger below with its exact time."),
             W.HBox([cont, kind]), ok, W.HBox([b_inj, b_rec]), out_l])
t4 = W.VBox([help_box("<b>Results.</b> Press Analyse after a recovered fault. Green cards = within budget / all roots ranked first. The heatmap should light up in the cyan band only."), b_an, out_r])
tabs = W.Tab(children=[t1, t2, t3, t4]); [tabs.set_title(i, t) for i, t in enumerate(("1 Connect", "2 Tune", "3 Inject", "4 Results"))]
display(tabs)
''')
md('''
**Faults to try (all recorded in the ledger):** `stop` on a leaf (database/cache), `stop` on a mid-tier service, `pause` (process frozen; the container stays "up", so this is the hard case). Repeat each type at different times and on different services, and leave at least 5 min healthy between faults. For degradations (`docker update --cpus`, `tc netem`, `stress-ng`) run them from the host terminal and add the ledger row by hand: `STATE["chaos"]["death-star"].ledger.append({"service":"post-storage","kind":"cpu-limit","start":t0,"end":t1})`.
''')
md('''
## Part C: your labelled CSV (`ml-dataset-labeled.csv`)
Same method, but the truth is the `anomaly_label` column. It reports row-level precision/recall and the top-ranked service per flagged episode. Counters become rates and baselines use only the past, which removes the leakage and cumulative-counter artefacts of the original notebook.
''')
code('''
CSV = "/content/drive/MyDrive/ml-dataset-labeled.csv"   # or upload below
if not os.path.exists(CSV):
    from google.colab import files as _f
    print("Upload ml-dataset-labeled.csv"); _u = _f.upload(); CSV = next(iter(_u))
raw = pd.read_csv(CSV)
pc = L.prepare(raw, track_presence=False, edges=L.DEFAULT_PRESETS["sock-shop"])
scc = L.score(pc, window=80, min_base=20)
bud = W.FloatSlider(2.0, min=0.2, max=20, step=0.2, description="false/h")
def run_csv(_=None):
    tau = L.calibrate(scc, pc.step, bud.value, 2); flags = L.flags_for(scc, tau, 2)
    pred = L.row_flags(pc, raw, flags); y = raw["anomaly_label"].astype(bool)
    tp, fp, fn = int((pred & y).sum()), int((pred & ~y).sum()), int((~pred & y).sum())
    print(f"threshold {tau} | rows flagged {int(pred.sum())} | true anomalies {int(y.sum())} | precision {tp/max(tp+fp,1):.3f} recall {tp/max(tp+fn,1):.3f}")
    for a, b in L.incidents(flags):
        att = L.attribute(pc, scc, (a, b)); print(f"episode ticks {a}-{b}: top-3 = {list(att.service[:3])}")
    print("services that really carry the labelled anomalies:", dict(raw.loc[y, "service"].value_counts()))
run_csv()
display(bud); bud.observe(lambda c: run_csv(), names="value")
''')
nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "name": "python3"}, "language_info": {"name": "python"}, "colab": {"provenance": []}}, "nbformat": 4, "nbformat_minor": 5}
(here / "rca_live_colab.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")
print("cells", len(cells))
