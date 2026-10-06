"""Command line: python -m rcalab <command>"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from . import config, evaluate, store
from .detector import detect
from .explain import explain
from .rca import rank


def main():
    ap = argparse.ArgumentParser(prog="rcalab")
    ap.add_argument("--config", default="config.yaml")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="create config.yaml, prompting for required values")
    sub.add_parser("check", help="list config values still missing")
    p = sub.add_parser("diagnose", help="analyse the last N minutes of live telemetry")
    p.add_argument("--minutes", type=int, default=20)
    p = sub.add_parser("record", help="collect a labelled run for a fault you injected elsewhere")
    p.add_argument("--service", required=True, help="service the fault was injected into")
    p.add_argument("--fault", required=True, help="free-text fault name, e.g. flagd:cartFailure")
    p.add_argument("--start", required=True, help="injection start (ISO time or unix seconds)")
    p.add_argument("--end", required=True, help="injection end (ISO time or unix seconds)")
    p.add_argument("--out", default="runs")
    p = sub.add_parser("evaluate", help="score saved runs (or --synthetic) against labels")
    p.add_argument("--runs-dir", default="runs")
    p.add_argument("--synthetic", action="store_true")
    p.add_argument("--hard", action="store_true", help="synthetic: victims louder than the root")
    a = ap.parse_args()

    if a.cmd == "init":
        cfg = config.init(out=a.config)
        print(f"wrote {a.config}; still missing: {config.missing(cfg) or 'nothing'}")
        return
    if a.cmd == "evaluate" and a.synthetic:
        cfg = config.load(a.config if Path(a.config).exists() else "config.example.yaml")
        print(json.dumps(evaluate.run_synthetic(cfg, hard=a.hard), indent=2))
        return

    cfg = config.load(a.config)
    if a.cmd == "check":
        gaps = config.missing(cfg)
        print("config complete" if not gaps else "missing:\n  " + "\n  ".join(gaps))
        return
    config.require_complete(cfg)

    if a.cmd == "diagnose":
        from .collect import collect
        step = cfg["collection"]["step_seconds"]
        end = time.time()
        tel = collect(cfg, end - a.minutes * 60, end)
        base = cfg["collection"]["baseline_minutes"] * 60 // step
        det = detect(tel, base, cfg["detector"]["z_threshold"], kind=cfg["detector"]["kind"])
        window = (base, len(tel.times))
        res = rank(tel, det, window, cfg["cascade"]["max_lag_windows"], cfg["cascade"]["max_hops"])
        print(explain(tel, det, res, window))
    elif a.cmd == "record":
        from .record import record
        n = len([d for d in Path(a.out).glob("run_*")]) if Path(a.out).exists() else 0
        d = record(cfg, a.service, a.fault, a.start, a.end, Path(a.out) / f"run_{n:02d}_{a.service}")
        print(f"saved {d}")

        print(json.dumps(evaluate.run_dir(cfg, Path(a.runs_dir)), indent=2))


if __name__ == "__main__":
    main()
