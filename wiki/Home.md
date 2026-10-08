# Project wiki: label-free RCA and cascade risk for microservices

**Start here.** Every document of the project is linked from this page. Paths are relative to the repository root.

## 1. Read first (in this order)

| # | Document | What it tells you |
|---|---|---|
| 1 | [What is wrong, why, and what we can still do](../docs/WHAT_IS_WRONG.md) | the honest status: every problem, its evidence, cause, fix and cost; what we may and may not claim |
| 2 | [RCA and cascade logic in simple words](../docs/RCA_AND_CASCADE_SIMPLE.md) | how the method works and why it is not on par with the papers |
| 3 | [Cross-paper research gaps](../literature-review/GAPS.md) | six gaps across 37 papers read in full; the recommended paper framing |
| 4 | [Handoff](../HANDOFF.md) | state of everything; how to continue on a new laptop or in a new Claude session |

## 2. Run things

| What | Where | Notes |
|---|---|---|
| **Research notebook** (every step visible, flowchart, test bench, ablations, live) | [`ipynb/rca_research.ipynb`](../ipynb/rca_research.ipynb) | open in Colab: File > Open notebook > GitHub > `Royson-salis-18/new-repo`; needs the Colab secret `SSH_KEY` only for the live section |
| Simple live notebook (buttons, fault injector) | [`ipynb/rca_live_colab.ipynb`](../ipynb/rca_live_colab.ipynb) | older two-part UI; same core |
| Core library used by the notebooks (sampler, injector) | [`colab/rca_lite.py`](../colab/rca_lite.py) | read-only SSH allowlist; injector limited to docker stop/start/pause/unpause |
| Full research harness (CLI + dashboard) | [`rcalab/`](../rcalab), [`README.md`](../README.md) | tools/ssh/both data modes, experiments in `experiments/` |
| microservice-mapper (the product) | separate repo `Royson-salis-18/microservice-mapper` | discovery, graph, traffic |

### How the notebook is organised

| Section | Content |
|---|---|
| 0 | flowchart of the whole pipeline (and the ledger/evaluation loop) |
| 1 | the real data: OTel healthy traffic, DeathStar crash, your CSV |
| 2-7 | one step each (prepare, score, threshold, common-mode, attribute, risk): CODE, LOOK (plots), WHY / WHAT IF |
| 8 | test bench: labelled faults on 10 h of real healthy traffic; ablation table, sweeps, "your experiment" cell |
| 9 | the real crash with every component switched on and off |
| 10 | your labelled CSV (skipped if the file is not present) |
| 11 | live on the AWS hosts: key check, watch, analyse, optional fault + ledger scoring |

## 3. Evidence and results

| Document | Content |
|---|---|
| [Fixes and tests on larger apps](../docs/FIXES_AND_TESTS.md) | false alarms, detection, ranking on 17-200 services, cascade, DeathStar crash |
| [Hostile review report](../docs/REVIEW_REPORT.md) | reviewer-2 critique (M1-M16), how to pre-empt each point, data sources, 7-day plan |
| `docs/experiments/` | raw result files (JSON/NPZ) used by every table |

## 4. Literature

| Document | Content |
|---|---|
| [Literature review start page](../literature-review/README.md) | map of the literature folder |
| [Papers](../literature-review/PAPERS.md), [survey table](../literature-review/SURVEY_TABLE.md), [comparison matrix](../literature-review/COMPARISON_MATRIX.md) | what each paper does, indexed venue, how it compares |
| [Problem evidence](../literature-review/PROBLEM_EVIDENCE.md) | page-cited evidence IDs used by GAPS.md |
| `literature-review/reports/` | one detailed report per paper |

## 5. Older index (auto-built)

[INDEX](INDEX.md) by topic, [TIMELINE](TIMELINE.md) by date, [TAGS](TAGS.md), [CATALOG.csv](CATALOG.csv). Rebuild with `.venv\Scripts\python tools\build_wiki.py`.

## 6. Chat history

`history/transcripts/` holds every Claude chat of this project (JSONL), `history/memory/` the memory files. See [HANDOFF.md](../HANDOFF.md) for how to restore them.
