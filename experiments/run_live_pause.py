"""LIVE frozen-service test on DeathStarBench (the case the bench says we now solve, never tested live).

Uses the research notebook's own code (colab/rca_research_src.py: sampler, guarded injector + ledger, analysis).
Sequence: 6 min healthy -> `docker pause` service A for 90 s -> unpause -> 4 min -> pause service B for 90 s -> unpause -> 3 min.
Light user traffic (4 req/s) runs throughout; its HTTP results are an independent check of real impact.
Every pause is undone in `finally`, even on error or Ctrl+C.
Run: RCA_KEY=<pem> .venv\\Scripts\\python experiments\\run_live_pause.py      (about 18 minutes)
"""
import json
import os
import pathlib
import threading
import time
import warnings
from concurrent.futures import ThreadPoolExecutor

import matplotlib
import requests

matplotlib.use("Agg")
warnings.filterwarnings("ignore")
ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT / "colab")
src = (ROOT / "colab" / "rca_research_src.py").read_text(encoding="utf-8")
a = src.index("# %% [markdown]\n# ## 8. THE TEST BENCH")
b = src.index("# %% [markdown]\n# ## 11. LIVE")
c = src.index("# 11d. OPTIONAL")
os.environ.setdefault("RCA_LIVE_MINUTES", "0")
src_live = src[b:c].replace("HOST_OK = check_hosts() if RUN_LIVE else {}", "HOST_OK = {}").replace("if RUN_LIVE:\n    watch(", "if False:\n    watch(").replace("if RUN_LIVE and LIVE:", "if False:")
import matplotlib.pyplot as plt  # noqa: E402

FIG = ROOT / "docs" / "experiments" / "live_pause"
FIG.mkdir(parents=True, exist_ok=True)
_n = [0]


def _show(*_a, **_k):
    _n[0] += 1
    plt.savefig(FIG / f"fig{_n[0]:02d}.png", dpi=80, bbox_inches="tight")
    plt.close("all")


plt.show = _show
g = {"__name__": "nb"}
exec(compile(src[:a] + src_live, "nb", "exec"), g)
_n[0] = 0
for old in FIG.glob("fig*.png"):
    old.unlink()

HOST = "death-star"
TARGETS = ["socialnetwork-post-storage-service-1", "socialnetwork-user-timeline-service-1"]
BASE, FAULT, GAP, TAIL = 360, 90, 240, 180
BASEURL = f"http://{g['HOSTS'][HOST][0]}:8080"
PATHS = ["/wrk2-api/home-timeline/read?user_id=1&start=0&stop=10", "/wrk2-api/user-timeline/read?user_id=2&start=0&stop=10",
         "/wrk2-api/home-timeline/read?user_id=3&start=0&stop=10", "/wrk2-api/user-timeline/read?user_id=4&start=0&stop=10"]
client, stop_load = [], threading.Event()


def worker(i):
    k = i
    while not stop_load.is_set():
        t0 = time.time()
        try:
            r = requests.get(BASEURL + PATHS[k % len(PATHS)], timeout=8)
            client.append((t0, r.status_code, time.time() - t0))
        except requests.RequestException:
            client.append((t0, 0, time.time() - t0))
        k += 1
        time.sleep(1.0)


g["watch"](HOST)
chaos = g["LIVE"][HOST]["chaos"]
pool = ThreadPoolExecutor(4)
for i in range(4):
    pool.submit(worker, i)
t_begin = time.time()
try:
    print("healthy baseline", BASE, "s", flush=True)
    time.sleep(BASE)
    for n, tgt in enumerate(TARGETS):
        try:
            chaos.inject(tgt, "pause")
            print(time.strftime("%H:%M:%S"), "PAUSED", tgt, flush=True)
            time.sleep(FAULT)
        finally:
            for r in chaos.recover_all():
                print(time.strftime("%H:%M:%S"), "UNPAUSED", r["service"], f"after {r['end'] - r['start']:.0f}s", flush=True)
        time.sleep(GAP if n < len(TARGETS) - 1 else TAIL)
finally:
    chaos.recover_all()                       # belt and braces
    stop_load.set()
    pool.shutdown(wait=True)
    g["stop_watching"]()

# ---- independent truth: what users saw
led = chaos.ledger
cl = client


def rate(t0, t1):
    xs = [s for t, s, _ in cl if t0 <= t < t1]
    return (sum(s != 200 for s in xs) / len(xs), len(xs)) if xs else (float("nan"), 0)


user = {"healthy_error_rate": rate(t_begin + 60, led[0]["start"])[0]}
for r in led:
    user[r["service"]] = {"error_rate_during": rate(r["start"], r["end"])[0], "requests": rate(r["start"], r["end"])[1]}
print("USER-VISIBLE:", json.dumps(user, default=float), flush=True)

# ---- our pipeline vs the ledger
res = g["analyse_live"](minutes=60, show=True)
p, scn, fl = res
np = g["np"]
out = []
for r in led:
    a_ = max(int(np.searchsorted(p.times, r["start"])) - 1, 0)
    b_ = int(np.searchsorted(p.times, r["end"])) + 4
    ours = list(g["attribute"](p, scn, (a_, b_)).service)
    plain = [p.services[i] for i in np.argsort(-scn.zs[a_:b_].max(axis=0))]
    j = p.services.index(r["service"])
    out.append({"service": r["service"], "seconds": round(r["end"] - r["start"]),
                "root_flagged": bool(fl[a_:b_, j].any()),
                "delay_s": float(np.argmax(fl[a_:b_, j]) * p.step) if fl[a_:b_, j].any() else None,
                "rank_ours": ours.index(r["service"]) + 1, "top3_ours": ours[:3],
                "rank_most_abnormal": plain.index(r["service"]) + 1, "top3_most_abnormal": plain[:3],
                "user_error_rate": user[r["service"]]["error_rate_during"]})
healthy = np.ones(len(p.times), bool)
for r in led:
    healthy[max(int(np.searchsorted(p.times, r["start"])) - 2, 0):int(np.searchsorted(p.times, r["end"])) + 8] = False
summary = {"host": HOST, "faults": out, "user": user, "healthy_minutes": float(healthy.sum() * p.step / 60),
           "false_alarm_episodes_per_h": float(g["episodes_per_hour"](fl[healthy], p.step)), "ledger": led,
           "t_begin": t_begin, "t_end": time.time()}
(ROOT / "docs" / "experiments" / "live_pause_results.json").write_text(json.dumps(summary, indent=1, default=float))
g["live_frame"]().to_csv(ROOT / "docs" / "experiments" / "live_pause_samples.csv", index=False)
print(json.dumps(out, indent=1, default=float))
print("healthy minutes", summary["healthy_minutes"], "false alarms/h", summary["false_alarm_episodes_per_h"])
