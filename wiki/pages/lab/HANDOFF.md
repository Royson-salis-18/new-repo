# HANDOFF: read this first on a new laptop / new Claude session

Tell Claude: "Read HANDOFF.md, then wiki/INDEX.md, then continue." Everything below is what Claude needs to continue where we left off (state as of 2026-10-08).

## Who / what
- User: Royson (roysonsalis2005@gmail.com). Paper: "Probabilistic Cascading Failure and Agent Assisted Root Cause Analysis for Microservice Systems". Needs a publishable, honest, non-plagiarised paper within days. Wants results that are accurate, "crazy sharp", unique, no false data; hates optimistic claims. Prefers short, simple answers and a simple UI.
- Two codebases: `microservice-mapper` (older product, separate repo, GitHub Royson-salis-18/microservice-mapper) and this repo's `rcalab/` (research lab: label-free live-telemetry RCA + cascade risk).

## Repo map (this repo)
- `rcalab/`: detector (calibrated, causal baseline, one-sided log-scale MAD z, false-alarm-budget threshold), rca methods, cascade, replay/inject, SSH source (read-only allowlist), Jaeger source.
- `colab/rca_lite.py`: the SIMPLE method (rates, self-healing baseline, common-mode removal, hard-evidence `container_up`, own-vs-inherited attribution, EdgeLearner, `evaluate()` vs fault ledger, guarded `Chaos` injector). `colab/build_notebook.py` -> `colab/rca_live_colab.ipynb` (Part A simple UI, Part B detailed UI + injection + actual-vs-predicted, Part C user's labelled CSV). `colab/original.ipynb` = user's original notebook.
- `docs/`: `RCA_AND_CASCADE_SIMPLE.md` (logic, issues, what to change), `REVIEW_REPORT.md`, `FIXES_AND_TESTS.md`, `experiments/` (results JSON/npz). `wiki/` (INDEX/TIMELINE/TAGS/CATALOG; rebuild with `tools/build_wiki.py`), `litdb/` (paper database; PDFs/texts are gitignored and must be re-fetched), `RESEARCH.md`.
- `history/`: copies of the Claude chat transcripts (JSONL). Search them for details not in docs.
- Python env: `.venv\Scripts\python` (Windows). Recreate: `python -m venv .venv`, install numpy pandas scipy paramiko pyyaml pytest matplotlib. `pytest.ini` exists; 10 tests pass.

## Lab hosts (AWS, user `ubuntu`, key `sock-shop-key.pem` kept OUT of git; upload manually)
sock-shop 15.207.109.141 | death-star 13.233.8.32 (DeathStarBench socialNetwork, compose at /home/ubuntu/DeathStarBench/socialNetwork/docker-compose.yml) | open-telemetry 13.201.89.80 (Jaeger http://13.201.89.80:8080/jaeger/ui) | shopflowbench 13.203.200.52 (user's own bench; purpose and port 8081 not yet explained). IPs may change if instances restart.

## Standing rules
- Honest reporting: say when tests fail or were not run. Do not claim novelty for precedence/blast-radius/cascade terms (tests did not support them). Paper numbers cited from litdb are not comparable to ours (their data is labelled/pre-trained; ours is live and dynamic); a fair comparison means running the same services on our VPC.
- Ask before: downloads (RCAEval etc.), fault injection on hosts (user said OK once for a brief stop of one Death Star container; a new fault type needs a fresh OK), pushing to remotes. Never commit `.pem`/keys. Fixed read-only SSH allowlist only; the injector only does docker stop/start/pause/unpause on listed containers.
- Auto-commit hook (user-level, `~/.claude/hooks/auto-commit.sh`, settings.json Stop/SessionEnd) commits but never pushes. It must be reinstalled on the new laptop (copy those two things from `history/claude-config/`).
- Git commit trailer: `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.

## Key results so far (all honest, small)
- False alarms on healthy real OTel traffic: 215/h -> 0 in 32 min with calibrated threshold.
- Semi-synthetic injected slowdowns: detection 17-47% at strict budgets; plain "most abnormal"/self-time ranking (A@1 0.46) beat the full precedence+blast method (0.31-0.34); near random in 50-200 service apps.
- Death Star real crash (one run, easy fault): lite method ranks the stopped container #1, +0 s, 0 false alarms in 7.5 healthy min, after two fixes (hard-evidence `container_up`, common-mode removal). Pause/slow faults untested.
- Original notebook flaws: whole-dataset z-scores (leakage), cumulative counters as features, first-sample log artifact, ranking by anomaly counts (ranked user-1 above orders-1).

## Open tasks (in order)
1. Run the Colab notebook live; inject stop AND pause faults on each bench via Part B; collect ledger-scored results (repeat >=10 times per fault type, random targets/times, >=5 min healthy between).
2. Get `ml-dataset-labeled.csv` (user's Drive) and run Part C; report precision/recall and ranking honestly. Drive connector was not authorized, so Claude could not read/update Drive files; user uploads the notebook via Drive "Manage versions -> Upload new version" to keep the link.
3. Healthy data = self-generated steady traffic on the benches (run a load generator for hours) plus pre-fault periods of RCAEval; organic-ish faults = docker stop/pause, `docker update --cpus/--memory`, `tc netem`, stress-ng, DB/dependency faults, app flags (OTel flagd), randomized campaign with ledger.
4. Baselines to add: NSigma, BARO, MicroRCA-style PageRank, CIRCA, RCD; report A@1/A@3 with given and detected fault times.
5. Paper: reword contribution (calibrated label-free detector with measured false-alarm rate, self-time and hard-evidence signals, honest ledger-based evaluation); update `docs/FIXES_AND_TESTS.md` and rebuild wiki after new results.
6. Pending separate session: litdb batch reading (3 papers per batch); needs user go-ahead for PDF reads.

## Update 2026-10-08 (later the same day)
- Start page for all docs: `wiki/Home.md`. Honest status: `docs/WHAT_IS_WRONG.md` (problems P1-P15, evidence, fixes, allowed claims).
- Research notebook: `colab/rca_research_src.py` (percent format, the source of truth) -> `colab/build_research_nb.py` -> `colab/rca_research.ipynb`, copied to `ipynb/`. Every pipeline step is inline code with LOOK plots and WHY/WHAT-IF text, flowchart in section 0, test bench + ablations + sweeps in section 8, real crash in 9, CSV in 10 (skipped if absent, never prompts), live in 11 (key from Colab secret SSH_KEY, IPs built in, secret HOSTS overrides).
- Local test of the whole notebook incl. live: `RCA_KEY=<path to pem> RCA_LIVE_MINUTES=3` and exec the src with matplotlib Agg.
- Method changes today (all measured on the bench, 3 seeds): tail-aware spread, binomial error spread, per-series noise normalisation (tau 18.5 -> 3.25, false alarms 0.1/h). Ranking = "most abnormal" (A@1 0.45 vs 0.46); original notebook approach 78.7 false alarms/h. Slow and hang faults fail for every method. Best next task: a "silence" signal for frozen services (P3).
- User preferences: wants everything in GitHub `Royson-salis-18/new-repo` (public is OK for them; never commit .pem). Will not upload CSV or pem to Colab; the key is in the Colab secret.
