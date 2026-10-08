"""SSH-mode test on a real 27-container app (DeathStarBench social network): stop one container briefly and see what the SSH data shows.

The fault is injected HERE, outside the app (rcalab never runs arbitrary commands). The container is always restarted in `finally`.
Independent ground truth: a light client load records HTTP status/latency per request, so the real user-visible impact is known
without using our detector.     Run: .venv\\Scripts\\python experiments\\ssh_crash_test.py     (about 11 minutes)
"""
import json
import os
import pathlib
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import paramiko
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
from rcalab.sources.ssh import Sampler, SSHSource  # noqa: E402

HOST, KEY = "13.233.8.32", r"C:\Users\MITE\Downloads\sock-shop-key.pem"
TARGET = "socialnetwork-post-storage-service-1"
BASE, FAULT, RECOVER = 360, 120, 180                  # seconds
STEP = 10
BASEURL = f"http://{HOST}:8080"
PATHS = ["/wrk2-api/home-timeline/read?user_id=1&start=0&stop=10", "/wrk2-api/user-timeline/read?user_id=2&start=0&stop=10",
         "/wrk2-api/home-timeline/read?user_id=3&start=0&stop=10", "/wrk2-api/user-timeline/read?user_id=4&start=0&stop=10"]
sample_file = ROOT / "samples" / "death-star-crash.jsonl"
sample_file.unlink(missing_ok=True)

client_log, stop_load = [], threading.Event()


def load_worker(i):
    k = i
    while not stop_load.is_set():
        t0 = time.time()
        try:
            r = requests.get(BASEURL + PATHS[k % len(PATHS)], timeout=8)
            client_log.append((t0, r.status_code, time.time() - t0))
        except requests.RequestException:
            client_log.append((t0, 0, time.time() - t0))
        k += 1
        time.sleep(1.0)                                # 4 workers -> about 4 requests per second


def ssh_exec(cmd, tries=4):
    """Run one command on the host; retries because a busy host can drop the SSH banner (that crashed the first attempt)."""
    last = None
    for i in range(tries):
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            c.connect(HOST, username="ubuntu", key_filename=KEY, timeout=20, banner_timeout=40, auth_timeout=30, look_for_keys=False, allow_agent=False)
            _, o, _ = c.exec_command(cmd, timeout=60)
            return o.read().decode().strip()
        except Exception as e:
            last = e
            time.sleep(5)
        finally:
            c.close()
    raise last


events = {"host": HOST, "container": TARGET, "baseline_s": BASE, "fault_s": FAULT, "recover_s": RECOVER, "step_s": STEP}
sampler = Sampler(SSHSource(HOST, "ubuntu", KEY, known_hosts=".known_hosts"), sample_file, STEP, log_every_s=30)
pool = ThreadPoolExecutor(4)
t_begin = time.time()
try:
    print("start sampler + light load", flush=True)
    sampler.start()
    for i in range(4):
        pool.submit(load_worker, i)
    time.sleep(BASE)
    events["t_stop"] = time.time()
    print("STOP", TARGET, ssh_exec(f"docker stop -t 2 {TARGET}"), flush=True)
    time.sleep(FAULT)
finally:
    events["t_start"] = time.time()
    print("START", TARGET, ssh_exec(f"docker start {TARGET}"), flush=True)
(ROOT / "docs" / "experiments" / "ssh_crash_events.json").write_text(json.dumps({**events, "partial": True}))   # keep the timing even if something later fails
time.sleep(RECOVER)
stop_load.set()
sampler.stop()
time.sleep(2)
events["t_end"] = time.time()
events["t_begin"] = t_begin
try:
    events["status_after"] = ssh_exec(f"docker ps --filter name={TARGET} --format '{{{{.Names}}}} {{{{.Status}}}}'")
except Exception as e:
    events["status_after"] = f"unknown ({type(e).__name__})"
events["client"] = client_log
(ROOT / "docs" / "experiments" / "ssh_crash_events.json").write_text(json.dumps(events))
n = len(client_log)
print(f"done. sampler rows: {len(sample_file.read_text().splitlines())}; client requests: {n}; container after: {events['status_after']}", flush=True)
