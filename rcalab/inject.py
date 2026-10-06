"""Fault injection. Writes ground-truth labels that are used ONLY for scoring."""
from __future__ import annotations

import json
import random
import subprocess
import time
from pathlib import Path

from .collect import collect


def _run(cmd: str):
    subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)


def run_once(cfg: dict, service: str, fault: str, out_dir: Path) -> Path:
    """Inject one fault, recover, collect telemetry, save telemetry + label to out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    fi = cfg["fault_injection"]
    spec = fi["faults"][fault]
    base_s = cfg["collection"]["baseline_minutes"] * 60

    time.sleep(fi["settle_seconds"])
    t_inject = time.time()
    _run(spec["inject"].replace("{service}", service))
    try:
        time.sleep(fi["duration_seconds"])
    finally:
        _run(spec["recover"].replace("{service}", service))   # always recover
    t_recover = time.time()
    time.sleep(cfg["collection"]["step_seconds"] * 3)          # let the last window land

    tel = collect(cfg, t_inject - base_s, time.time())
    from .store import save
    save(out_dir / "telemetry.npz", tel)
    (out_dir / "label.json").write_text(json.dumps({
        "service": service, "fault": fault, "t_inject": t_inject, "t_recover": t_recover,
        "baseline_windows": int(base_s // cfg["collection"]["step_seconds"])}, indent=2))
    return out_dir


def pick(cfg: dict, services: list[str], rng: random.Random) -> tuple[str, str]:
    return rng.choice(services), rng.choice(list(cfg["fault_injection"]["faults"]))
