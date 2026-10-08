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
# 1. hosts + SSH key (the key stays in this Colab session only; nothing is stored in the notebook)
import os, time, numpy as np, pandas as pd, matplotlib.pyplot as plt
import ipywidgets as W
from IPython.display import display, clear_output
import rca_lite as L

HOSTS = {   # name -> (ip, compose file with the service wiring, or None)
    "sock-shop":      ("15.207.109.141", None),
    "death-star":     ("13.233.8.32",    "/home/ubuntu/DeathStarBench/socialNetwork/docker-compose.yml"),
    "open-telemetry": ("13.201.89.80",   None),
    "shopflowbench":  ("13.203.200.52",  None),
}
USER = "ubuntu"
KEY = "/content/key.pem"
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
## Part A: the simple version
1. pick hosts, press **Start watching** (give it about 3 minutes of healthy data first)
2. **What's wrong right now?** shows green (nothing unusual) or red with the most likely broken service
3. **Stop** when finished
''')
code('''
host_pick = W.SelectMultiple(options=list(HOSTS), value=("death-star",), description="Hosts", rows=4)
b_start, b_now, b_stop = W.Button(description="Start watching", button_style="success"), W.Button(description="What's wrong right now?", button_style="info"), W.Button(description="Stop")
out_a = W.Output()
def _start(_):
    with out_a: clear_output(); connect(host_pick.value)
def _now(_):
    with out_a:
        clear_output()
        df = all_frame()
        if df.empty: print("No data yet; click Start watching and wait a minute."); return
        mins = (df.timestamp.max() - df.timestamp.min()).total_seconds() / 60
        if mins < 3: print(f"Only {mins:.1f} min of data. Wait until about 3 min of healthy behaviour has been seen."); return
        p, sc, tau, flags = analyse(df)
        if not flags[-6:].any():
            print("GREEN: nothing unusual in the last minute (", len(p.services), "services, alarm threshold", tau, ")"); return
        att = L.attribute(p, sc, (len(p.times) - 12, len(p.times)))
        top = att.iloc[0]
        print(f"RED: most likely broken: {short(top.service)}  ({top.note or 'strongest unexplained evidence: ' + top.top_feature})")
        display(att.head(3).assign(service=lambda d: d.service.map(short))[["service", "score", "top_feature", "note"]])
        r = L.risk(p, sc, flags, len(p.times) - 1, tau)
        if len(r): print("Next at risk:", ", ".join(f"{short(s)} ({v:.0%})" for s, v in zip(r.service[:3], r.risk[:3])))
b_start.on_click(_start); b_now.on_click(_now); b_stop.on_click(lambda _: disconnect())
display(W.VBox([host_pick, W.HBox([b_start, b_now, b_stop]), out_a]))
''')
md('''
## Part B: the detailed version (every knob, fault injection, actual vs predicted)
*Injection works only on containers that `docker ps` lists on the host you pick, only with `docker stop|start|pause|unpause`, only after you tick the box. Every fault is written to the ledger with its exact time.*
''')
code('''
sl = dict(
    window=W.IntSlider(60, min=20, max=200, description="baseline win"), min_base=W.IntSlider(12, min=5, max=40, description="min base"),
    persistence=W.IntSlider(2, min=1, max=6, description="persist"), budget=W.FloatSlider(2.0, min=0.2, max=20, step=0.2, description="false/h"),
    common_frac=W.FloatSlider(0.5, min=0.2, max=0.95, step=0.05, description="load share"), gamma=W.FloatSlider(1.0, min=0, max=1.5, step=0.1, description="explain g"),
    step=W.IntSlider(10, min=5, max=60, description="tick s"))
cb_infer, cb_up = W.Checkbox(True, description="infer services with no telemetry"), W.Checkbox(True, description="use container_up")
minutes = W.IntSlider(20, min=3, max=240, description="last min")
hosts_b = W.Dropdown(options=list(HOSTS), description="host")
cont = W.Dropdown(options=[], description="container")
kind = W.Dropdown(options=["stop", "pause"], description="fault")
ok = W.Checkbox(False, description="I own this lab; allow injecting this fault")
b_conn, b_refresh, b_inj, b_rec, b_an = (W.Button(description=d) for d in ("Connect host", "List containers", "Inject fault", "Recover", "Analyse + score"))
b_inj.button_style, b_rec.button_style, b_an.button_style = "danger", "success", "info"
out_b, out_l = W.Output(), W.Output()
def ledger():
    return [r for c in STATE["chaos"].values() for r in c.ledger]
def show_ledger():
    with out_l:
        clear_output()
        act = {n: c._open for n, c in STATE["chaos"].items() if c._open}
        if act: print("ACTIVE faults:", act)
        display(pd.DataFrame(ledger()) if ledger() else "fault ledger is empty")
def _conn(_):
    with out_b: connect([hosts_b.value])
def _refresh(_):
    s = STATE["samplers"].get(hosts_b.value)
    if s: cont.options = sorted(s.containers())
def _inj(_):
    if not ok.value:
        with out_b: print("tick the ownership box first")
        return
    STATE["chaos"][hosts_b.value].inject(cont.value, kind.value)
    with out_b: print(time.strftime("%H:%M:%S"), "INJECTED", kind.value, cont.value, "(remember to Recover)")
    show_ledger()
def _rec(_):
    for r in STATE["chaos"][hosts_b.value].recover_all():
        with out_b: print(time.strftime("%H:%M:%S"), "RECOVERED", r["service"], f"after {r['end']-r['start']:.0f}s")
    show_ledger()
def _an(_):
    with out_b:
        clear_output()
        df = all_frame(minutes.value)
        if df.empty: print("no data"); return
        p, sc, tau, flags = analyse(df, **{k: v.value for k, v in sl.items()}, infer=cb_infer.value, use_up=cb_up.value)
        print(f"{len(p.times)} ticks x {len(p.services)} services | threshold tau={tau} (chosen for <= {sl['budget'].value}/h false alarms) | edges {len(p.edges)}")
        ev = L.evaluate(p, sc, flags, ledger(), tau)
        print(f"healthy time {ev['healthy_minutes']:.1f} min -> false alarms {ev['false_alarms_per_hour']:.1f}/h ({ev['false_alarm_samples']} flagged service-ticks)")
        if len(ev["faults"]):
            display(ev["faults"].assign(service=lambda d: d.service.map(short)))
        else: print("No ledger faults yet: inject one above, wait about 1 minute, recover, wait about 1 minute, press Analyse.")
        top = np.argsort(-sc.zs.max(axis=0))[:15]
        fig, ax = plt.subplots(figsize=(11, 4.5)); ax.imshow(np.minimum(sc.zs[:, top].T, 30), aspect="auto", cmap="magma")
        ax.set_yticks(range(len(top))); ax.set_yticklabels([short(p.services[i]) for i in top], fontsize=7)
        for f in ledger():
            a = np.searchsorted(p.times, f["start"]); b = np.searchsorted(p.times, f["end"]); ax.axvspan(a, b, color="cyan", alpha=.25)
        ax.set_title("deviation per service (bright = unusual); cyan = faults WE injected (the ledger)"); plt.show()
        if flags[-6:].any(): display(L.attribute(p, sc, (max(len(p.times) - 24, 0), len(p.times)), gamma=sl["gamma"].value, infer_unobserved=cb_infer.value).head(8).assign(service=lambda d: d.service.map(short)))
for b, f in ((b_conn, _conn), (b_refresh, _refresh), (b_inj, _inj), (b_rec, _rec), (b_an, _an)): b.on_click(f)
display(W.VBox([W.HBox([W.VBox(list(sl.values())[:4]), W.VBox(list(sl.values())[4:] + [minutes])]), W.HBox([cb_infer, cb_up]),
                W.HBox([hosts_b, b_conn, b_refresh]), W.HBox([cont, kind]), ok, W.HBox([b_inj, b_rec, b_an]), out_b, out_l]))
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
