---
name: research-paper-context
description: "Research paper (LaTeX) + the lean rca-lab app built for it; paper RQs, where the code lives, and the user's design requirements"
metadata:
  node_type: memory
  type: project
  originSessionId: e8bd673e-8d9b-478b-9c4e-190f06fcfd1d
  modified: 2026-10-07T09:00:54.338Z
---

User (Royson Salis, with Bharath, Dhanush, Anish) is writing a paper: "Probabilistic Cascading Failure and Agent Assisted Root Cause Analysis for Microservice Systems" (Oct 2026). The old app C:\Users\MITE\Downloads\microservice-mapper is the big product-style version; the research version is **rca-lab** at `C:\Users\MITE\Downloads\final project (short and sweet)` (Python: rcalab package, FastAPI server.py, static/index.html dashboard, RESEARCH.md protocol, tests/).

- Knowledge base (grows over time): C:\Users\MITE\Downloads\royson-paper\royson-paper (PDFs; "non-scopus paper" subfolder).
- Research gap: existing RCA relies on static, labeled, single-architecture datasets; early prediction of cascading-failure risk is under-explored.
- RQs: (1) unsupervised RCA on unlabeled live telemetry + cascade-risk reduces debugging time vs conventional; (2) accurate enough. Independent var: metrics, logs, traces; 10 runs. Human debugging time is NOT measured by the code (only an automated delay proxy).
- EC2 hosts (ap-south-1) are recreated often and IPs change; the user pastes the console table when ready. Key file: C:\Users\MITE\Downloads\sock-shop-key.pem. Old 2 vCPU/3.8 GB OTel host died from memory pressure; new ones are c7i-flex.large (8 GB).

**Design requirements the user stated (follow them):**
- Research project, not a product: protocol, real baselines, ablations, stats (RESEARCH.md); no demo-only tuning. Synthetic data is a sanity check, never evidence.
- Must work for ANY project/architecture, with the data method user-selectable: `source.mode` = tools | ssh | both. SSH is allowed but confined to rcalab/sources/ssh.py with a fixed read-only command allowlist (a test enforces it). No local process/shell execution anywhere.
- Faults are injected outside the app (e.g. OTel demo flagd UI); app only records labels via `record`.
- The "agent" part only explains results, never changes ranking.
- UI should look good (dark dashboard, weighted/animated graph); simple code, Python backend, no Node build step.

**Why:** the user pushed back on a demo-like build and on plain Streamlit; wants research rigor and flexible data sources.
**How to apply:** keep results honest (report ties/failures), keep SSH confined, and don't add features beyond what the protocol needs without asking.

## Status 2026-10-07 (evening) — what has been measured, so don't redo it
- Docs: `docs/REVIEW_REPORT.md` (critique, novelty, plan), `docs/FIXES_AND_TESTS.md` (latest tests), unified `wiki/` hub (rebuild: `.venv\Scripts\python tools\build_wiki.py`), literature DB in `litdb/` (a child session "litdb-reader" reads papers in batches; batches 1-6 done).
- Real healthy OTel telemetry saved: `docs/experiments/otel_healthy_long.npz` (77 min, 16 active services, only 5 "monitorable" at 15 s windows).
- Findings: calibrated one-sided log-scale detector cut false alarms 215/h -> 0 (32 min test); detection of injected slowdowns only 17-47% depending on budget; the "full" method (precedence + cascade terms) is NOT better than plain abnormality ranking and is near random at 50-200 services; self-time (exclusive latency) is best/near-best in places; cross-incident EdgeLearner lifts next-victim AP 0.16->0.5 in the small app, mixed at 100 services; cascade forecasting has value only for slow cascades.
- Nothing yet validated with REAL faults (need OTel demo feature flags toggled by the user) or public benchmarks (RCAEval downloads need approval).
- Mapper tested on Death Star host (27 containers): discovered all 27 within ~45 s after updating the target IP via POST /api/config/remote.
