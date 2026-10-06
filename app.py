"""Simple viewer for rca-lab.  Run:  .venv\\Scripts\\streamlit run app.py
Read-only: it only shows results computed from telemetry (synthetic demo or live APIs).
"""
import time
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from rcalab import config, evaluate, synthetic
from rcalab.cascade import cascade_risk, edge_probabilities, path_probabilities
from rcalab.detector import detect
from rcalab.explain import explain
from rcalab.rca import rank

st.set_page_config(page_title="rca-lab", layout="wide")
st.title("rca-lab: root cause + cascade risk")

# ---------- sidebar: where does the telemetry come from? ----------
mode = st.sidebar.radio("Telemetry source", ["Synthetic demo", "Live (config.yaml)"])
cfg = config.load("config.yaml" if Path("config.yaml").exists() else "config.example.yaml")
z_thr = st.sidebar.slider("Anomaly threshold (z)", 2.0, 8.0, float(cfg["detector"]["z_threshold"]), 0.5)
play = st.sidebar.toggle("Play (animate graph)", value=False)
method = st.sidebar.selectbox("RCA method", ["full", "anomaly_only", "earliest", "random"])

if mode == "Synthetic demo":
    services = sorted({e for es in synthetic.CALLS.values() for e in es})
    root = st.sidebar.selectbox("Injected fault in", services, index=services.index("cart-db"))
    hard = st.sidebar.checkbox("Hard case (victims louder than the root)", True)
    kw = dict(lag_range=(0, 1), root_mag=3.0, victim_mag=8.0) if hard else {}
    tel, truth = synthetic.make(root, **kw)
    baseline, window = truth["baseline"], (truth["baseline"], len(tel.times))
    st.caption(f"Ground truth (hidden from the algorithm): fault injected in **{root}** at window {truth['onset']}.")
else:
    gaps = config.missing(cfg)
    if gaps:
        st.error("config.yaml is missing required values:\n\n- " + "\n- ".join(gaps)
                 + "\n\nRun `python -m rcalab init` to fill them in.")
        st.stop()
    minutes = st.sidebar.number_input("Look back (minutes)", 10, 240, 30)
    from rcalab.collect import collect
    step = cfg["collection"]["step_seconds"]
    with st.spinner("Reading Prometheus / Jaeger / Loki ..."):
        end = time.time()
        tel = collect(cfg, end - minutes * 60, end)
    baseline = cfg["collection"]["baseline_minutes"] * 60 // step
    window = (baseline, len(tel.times))

det = detect(tel, baseline, z_thr, kind=cfg["detector"]["kind"])
res = rank(tel, det, window, cfg["cascade"]["max_lag_windows"], cfg["cascade"]["max_hops"], method)

def live_graph(tel, det):
    """Weighted call graph at one moment. Edge weight = learned cascade probability
    p(callee failure -> caller failure); node colour = deviation now; thick border = cascade risk."""
    T = len(tel.times)
    if "t" not in st.session_state or st.session_state.t >= T:
        st.session_state.t = T - 1
    if play:  # advance one window per tick, wrap around
        st.session_state.t = (st.session_state.t + 1) % T
    t = st.slider("Time (window)", 0, T - 1, key="t")
    probs = edge_probabilities(tel, det.flags[: t + 1], cfg["cascade"]["max_lag_windows"])
    P = path_probabilities(tel.services, probs, cfg["cascade"]["max_hops"])
    risk = cascade_risk(det.a[t], P)
    lines = ['digraph { rankdir=LR; node [style=filled, shape=ellipse, fontname=Helvetica];']
    for i, name in enumerate(tel.services):
        z = det.z[t, i]
        k = min(z / 10.0, 1.0)                       # white -> red with deviation
        fill = "#%02x%02x%02x" % (255, int(255 * (1 - k)), int(255 * (1 - k)))
        lines.append(f'"{name}" [fillcolor="{fill}", penwidth={1 + 5 * risk[i]:.1f}, '
                     f'label="{name}\\nz={z:.1f}  risk={risk[i]:.0%}"];')
    for (callee, caller), p in probs.items():
        hot = det.flags[t, tel.index(callee)]
        color = "#e5484d" if hot else "#9a9a9a"
        lines.append(f'"{callee}" -> "{caller}" [penwidth={0.5 + 7 * p:.1f}, color="{color}", '
                     f'label="{p:.2f}", fontsize=10];')
    st.graphviz_chart(" ".join(lines) + "}")
    st.caption(f"t = {pd.to_datetime(tel.times[t], unit='s'):%H:%M:%S}  |  arrows show failure spreading "
               "callee -> caller; thickness/label = learned probability; red arrow = callee anomalous now; "
               "node colour = deviation; thick border = cascade risk.")


tab_rca, tab_signals, tab_eval = st.tabs(["Diagnosis", "Signals", "Evaluation"])

# ---------- Diagnosis ----------
with tab_rca:
    if not res.ranking:
        st.success("No service deviated from its baseline.")
    else:
        left, right = st.columns(2)
        with left:
            st.subheader("Likely root causes")
            df = pd.DataFrame(res.ranking, columns=["service", "score"]).set_index("service")
            st.bar_chart(df)
        with right:
            st.subheader("Cascade risk (who gets pulled in next)")
            risk = pd.Series(res.risk, name="risk").sort_values(ascending=False)
            st.bar_chart(risk)
        st.subheader("Explanation")
        st.text(explain(tel, det, res, window))

    st.subheader("Live weighted graph")
    top = res.ranking[0][0] if res.ranking else None
    st.fragment(run_every=1.0 if play else None)(lambda: live_graph(tel, det))()

# ---------- Signals ----------
with tab_signals:
    svc = st.selectbox("Service", tel.services, index=tel.services.index(top) if top else 0)
    i = tel.index(svc)
    st.line_chart(pd.DataFrame({"deviation (z)": det.z[:, i]}, index=pd.to_datetime(tel.times, unit="s")))
    st.write("Per-feature deviation (peak in the incident window):")
    peak = pd.Series(det.feature_z[window[0]:window[1], i].max(axis=0), index=tel.features)
    st.bar_chart(peak)
    st.write("Deviation (z) of every service over time (darker red = more abnormal):")
    heat = pd.DataFrame(det.z, columns=tel.services)
    heat["window"] = range(len(heat))
    heat = heat.melt("window", var_name="service", value_name="z")
    st.altair_chart(alt.Chart(heat).mark_rect().encode(
        x="window:O", y="service:N",
        color=alt.Color("z:Q", scale=alt.Scale(scheme="reds", domain=[0, 10], clamp=True))),
        width="stretch")

# ---------- Evaluation ----------
with tab_eval:
    st.write("Scores every method against known injected faults (10 runs, paired Wilcoxon vs `full`).")
    src = st.radio("Runs from", ["Synthetic", "Saved live runs (runs/)"], horizontal=True)
    if st.button("Run evaluation"):
        if src == "Synthetic":
            out = evaluate.run_synthetic(cfg, runs=10, hard=True)
        else:
            out = evaluate.run_dir(cfg, Path("runs"))
        st.dataframe(pd.DataFrame(out["metrics"]).T)
        st.write("Significance of `full` over each baseline (lower p = stronger evidence):")
        st.dataframe(pd.DataFrame(out["full_vs_baselines"]).T)

if mode != "Synthetic demo":
    every = st.sidebar.number_input("Auto-refresh live data every (s, 0 = off)", 0, 600, 0)
    if every:
        time.sleep(every)
        st.rerun()
