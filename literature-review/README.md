# Literature review: label-free, propagation-aware RCA and cascade-risk prediction for microservices

Team: Royson Salis, Bharath, Dhanush, Anish. Review carried out with Claude (Anthropic) as the paper-reading session; every number in these files is copied from a paper with a page reference, or it is not written.

**Start here:**
1. [`GAPS.md`](GAPS.md) - the cross-paper research gaps we can solve, with evidence, acceptance criteria, reviewer attacks, and the recommended project framing.
2. [`PAPERS.md`](PAPERS.md) - every paper (names, authors, venue, DOI/arXiv link, evidence quality), with links to the note and report for each one read.
3. [`PROBLEM_EVIDENCE.md`](PROBLEM_EVIDENCE.md) - evidence ledger: what the literature shows about our problem (pro, rows A1-A56) and what already covers our contribution (con, rows B1-B10).
4. [`INSTRUCTIONS_FOR_CLAUDE.md`](INSTRUCTIONS_FOR_CLAUDE.md) - how a future Claude session should continue this work.

## Status (2026-10-08)
- 37 papers read in full (13 batches). 44 papers in the literature matrix are not yet read in full (no open-access PDF found).
- Scopus status checked by ISSN for most journals (`reference/scopus_checks.md`); SJR quartiles are "unknown" until a Scopus or Scimago list file is supplied.

## Layout
| Path | Contents |
|---|---|
| `GAPS.md` | gap analysis v2 (read this first) |
| `PAPERS.md` | full paper index with links |
| `KEY_MAP.md` | short keys used here vs the long keys in the local `litdb/` |
| `PROBLEM_EVIDENCE.md` | evidence ledger with page references |
| `SURVEY_TABLE.md`, `COMPARISON_MATRIX.md`, `papers.csv` | auto-generated survey table and comparison with our system |
| `QUEUE.md` | reading queue (auto-generated) |
| `notes/<key>.md` | per-paper reading notes: YAML header (venue, DOI, Scopus, supervision, data, code, headline result) + 11 sections |
| `reports/<key>.md` | per-paper report, sections (a)-(l): bibliographic block, summary, method, data, copied results, stern critique, reproducibility, head-to-head with our work, safe and unsafe sentences |
| `batches/batch-NN.md` | per-batch side-by-side comparison, consequences for our claims, corrections to earlier notes |
| `reference/scopus_checks.md` | Scopus checks by ISSN, Crossref and GitHub verifications |
| `reference/literature_matrix.csv` | the original 65-paper literature matrix |
| `tools/` | scripts used (`add_paper.py`, `build_table.py`, `scopus_check.py`, `fetch_oa.py`, note template) |
| `project-context/` | copies of the project's own review and test reports (REVIEW_REPORT, FIXES_AND_TESTS, RCA_AND_CASCADE_SIMPLE, RESEARCH) that the gap analysis relies on |
| `LITDB_WORKFLOW.md` | the original workflow description of the reading database |

## Not in this repo (on purpose)
- Paper PDFs and their extracted full texts: copyrighted, and this repository is public. They are in the local project (`litdb/pdfs`, `litdb/texts`).
- The project code (`rcalab`) and raw telemetry.

## Honesty rules used throughout
- Numbers are copied with a page reference or not written. Anything not verified is marked "unverified".
- Scopus status is never guessed. arXiv preprints are not Scopus-indexed and not peer reviewed.
- Weak evidence is flagged as weak (evidence quality 1 = weak/unverifiable, 5 = rigorous, open, multi-system).
