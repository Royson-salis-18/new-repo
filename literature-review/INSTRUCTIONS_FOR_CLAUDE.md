# Instructions for a future Claude session (continue the literature review)

Read this whole file before doing anything. It records how the work was done, the rules the user set, what is finished, what is pending, and the traps already hit.

## 1. Who and what
- User: Royson Salis (roysonsalis2005@gmail.com); team Bharath, Dhanush, Anish. Final-year project + paper: label-free, propagation-aware root-cause analysis (RCA) and cascade-risk prediction for microservices.
- Your role: the **paper-reading session**. Read papers fully, write notes/reports, keep the evidence ledger and gap analysis honest. Do **not** change the project code (`rcalab`) or run experiments on the user's EC2 hosts from this role; propose code or experiment changes in batch documents instead.
- Local project (Windows): `C:\Users\MITE\Downloads\final project (short and sweet)`; the reading database is `litdb/` there. This GitHub folder (`literature-review/`) is a published copy of `litdb/` without PDFs or full texts.

## 2. Rules the user set (follow exactly)
1. Read each paper **completely**, one at a time, in batches of 3. Scanned PDFs: render pages to images and read them visually.
2. Copy numbers with **page references** or do not write them. Mark anything unverified. Paraphrase; quote at most a few words.
3. Flag weak evidence plainly. Record corrections to earlier notes in the batch document's section 7.
4. Scopus: never guess. Check by ISSN in the Scopus preview (`https://www.scopus.com/sources?...` search by ISSN in the browser). SJR quartile stays "unknown: no list supplied" until the user adds a Scopus or Scimago file to `litdb/reference/`; remind the user once per batch.
5. Ask before downloading anything or changing system/security settings. (On 2026-10-08 the user said "you have all permissions"; still ask for anything new or large, and never bypass a block.)
6. Keep chat replies short; put the substance in files.
7. Commit after each batch with author `Royson Salis <roysonsalis2005@gmail.com>`; end the message with the Co-Authored-By line the harness specifies.
8. The user asked that the "go" step be automatic: continue batches without waiting for "go", stopping only for permission questions and the final summary.

## 3. Per-paper workflow (local project)
1. `.venv\Scripts\python.exe litdb\tools\add_paper.py <pdf> --batch N` -> extracts text (`litdb/texts/<key>.txt`, page markers), metadata (Crossref/arXiv), writes a note skeleton.
2. Read the full text (use offsets for long files). Fill `litdb/papers/<key>.md`: YAML header (venue, DOI, ISSN, Scopus status, peer review, supervision, telemetry, propagation modelling, forecasting, datasets, code, baselines, metrics, headline result with page, evidence quality, relevance, overlap, threat) + 11 sections (summary, problem, method, data, results table with pages, limitations + stern critique, reproducibility, comparison with our work, does it change our problem, citation-ready facts, open questions).
3. Write `litdb/reports/<key>.md` with sections (a)-(l).
4. Add rows to `litdb/PROBLEM_EVIDENCE.md` (section A before the "## B." heading; section B before "## C.").
5. After 3 papers: `litdb/batches/batch-NN.md` (side-by-side, what each means for our claims, does the problem change, baselines/datasets to add, claims weakened, safe sentences, corrections, proposals), append to `litdb/reference/scopus_checks.md`, run `.venv\Scripts\python.exe litdb\tools\build_table.py`, commit.
6. Verification habits: check DOIs in Crossref (`https://api.crossref.org/works/<doi>`), code repos via the GitHub API, do sanity arithmetic (CI width vs sample size, k/n feasibility, MAE <= RMSE, table-to-table consistency). These caught several broken papers (AURORA, STMformer, Li 2026).

## 4. Traps already hit (do not repeat)
- **PyMuPDF is blocked** by Windows Application Control on this PC. Use `pypdfium2` (installed in `.venv`) to render scanned pages: `pypdfium2.PdfDocument(p)[i].render(scale=1.6).to_pil().save(...)`, then read the PNGs.
- Do not use poppler (not installed). The browser PDF viewer is unreliable for screenshots.
- Scimago and ScienceDirect show bot checks: do not bypass them.
- A script that searched arXiv by title and downloaded PDFs was **denied by the auto-mode classifier**; do not retry it or route around it. `litdb/tools/fetch_oa.py` (OpenAlex best_oa_location + arXiv DOIs) was allowed and was used once.
- Some PDFs' text extraction mislabels keys (`ahmed2023llmrca` is RCACopilot by Chen et al.; `hou2021aid` is AID by Yang et al.). Check authors against the text.
- `sed`-style bulk edits once mislabelled all notes as batch 2; edit frontmatter per file.
- Windows filenames: avoid zero-width characters (a stray file was created once).
- Bash heredocs with nested quotes broke once; write Python scripts to a temp file and run them.

## 5. State at hand-over (2026-10-08)
- Read in full: 37 papers (batches 1-13). See `PAPERS.md` section A.
- Not read: 44 matrix papers (`PAPERS.md` section B), mostly paywalled.
- Gap analysis: `GAPS.md` v2. Core gaps G1 (accuracy per symptom stratum) and G2 (operating point: false alarms/hour, detected vs given fault time) have high confidence; G3 (root vs victim signals), G4 (cascade early warning vs structural rule) medium; G5, G6 extensions.
- Corrections made so far are listed in each `batches/batch-NN.md` section 7 (e.g., AID is edge strength not forecasting; TNSM 2025 "fault forecasting" is simulation-only; DeepHunt is label-free at cold start; RCACopilot's "76.6%" is micro-F1 on one service's categories).

## 6. What to do next (priority order)
1. Get PDFs for the papers that could close a gap (`GAPS.md` section 5): BARO, RCAEval, TraceRCA, MicroRank, SuanMing, Sage, latent-diffusion propagation (2025), TORAI, LatentScope, yRCA (SPE 2024), Goyal 2010, Gomez-Rodriguez 2010, Alibaba dependency characterization (SoCC 2021), metastable failures (HotOS 2021), "Does graph structure earn its place?" (2026), Kintsugi (2026). Ask the user to drop PDFs into `litdb/incoming/` if they are paywalled.
2. Read them in batches of 3 with the workflow above; update `GAPS.md` section 6 confidence after each batch (a gap that is closed must be moved to section 3, "not gaps").
3. Run the Scopus preview check for the unchecked ISSNs/proceedings listed in `reference/scopus_checks.md` (KDD, FSE, CIKM, EuroSys, TNSM 1932-4537, JSS 0164-1212, Nature 0028-0836, PRE 1063-651X).
4. Fix the literature matrix attribution errors noted in batch 11 section 7.
5. When the user supplies a Scopus/Scimago list, re-run `build_table.py` so the quartile column fills.
6. Keep this GitHub folder in sync: copy `litdb/` content (not `pdfs/`, `texts/`, `incoming/`) to `literature-review/`, regenerate `PAPERS.md`, update this file's section 5, commit, push.

## 7. Claims the project must not make (from the evidence)
"Label-free RCA is new", "early warning is new", "cascade prediction is unexplored", "first to use co-location", "propagation modelling improves localization" (unless shown per symptom stratum against SimpleRCA/NSigma/BARO and a no-telemetry prior), "LLM agent" without a faithfulness check.

## 8. Repository layout note (2026-10-08)
- This GitHub repo (`Royson-salis-18/new-repo`) also holds the whole project at the root (`rcalab/`, `docs/`, `litdb/`, `ipynb/`, ...), pushed separately by the user. `litdb/` at the root is the live reading database with the long auto-generated keys; `literature-review/` is the curated copy with short keys (`KEY_MAP.md`), `PAPERS.md` and these instructions.
- When you update the review, change `litdb/` first, then regenerate `literature-review/` from it (copy, apply `KEY_MAP.md`, regenerate `PAPERS.md`).
- Paper PDFs were removed from the repo on the user's request (2026-10-08); only summaries and source details (titles, authors, DOI/arXiv links) are published. `.gitignore` keeps `litdb/pdfs`, `litdb/texts`, `litdb/incoming` and `*.pdf` out. Never commit PDFs or full texts here.
