# litdb: the reading database

One note per paper, read from the **full text**, with a structured header that builds the survey table, the comparison matrix and the reading queue.

## Workflow (batches of 3)

1. **You** give me 3 papers (PDF paths or names from the queue). Or say "next batch" and I take the next three in `QUEUE.md` order.
2. **I run** `python litdb/tools/add_paper.py <pdf> --batch N` for each: full text with page markers, verified metadata (Crossref / arXiv), ISSN, and a Scopus check.
3. **I read each paper completely** (`litdb/texts/<key>.txt`, and I open the PDF pages for tables/figures/scans), then fill `litdb/papers/<key>.md`: problem, method, data, results with page numbers,
   limitations, my critique, reproducibility, and the comparison with our work.
4. **I write** `litdb/batches/batch-NN.md`: the three papers side by side, what each means for our claims, and whether the problem we solve is real.
5. **I rebuild** `SURVEY_TABLE.md`, `COMPARISON_MATRIX.md`, `QUEUE.md`, `papers.csv` and update `PROBLEM_EVIDENCE.md`.

## Files
| file | purpose |
|---|---|
| `papers/<key>.md` | the note (YAML header + reading sections) |
| `texts/<key>.txt` | full extracted text, `=== page N ===` markers |
| `pdfs/<key>.pdf` | copy of the PDF |
| `SURVEY_TABLE.md`, `papers.csv` | the survey table (all papers; Scopus status, quartile, supervision, open data/code, threat level) |
| `COMPARISON_MATRIX.md` | reviewed papers vs our work |
| `QUEUE.md` | what is still to read |
| `PROBLEM_EVIDENCE.md` | evidence (with page refs) that the problem is real, and counter-evidence |
| `batches/batch-NN.md` | per-batch comparison document |
| `reference/` | **you** put the Scopus / Scimago files here (see below) |

## Scopus indexing (needs one file from you)
Scopus has no free API and Scimago blocks scripts, so I cannot look it up myself. Download in your **browser** and drop into `litdb/reference/`:
- the official **Scopus Source List** (Excel) from Elsevier's Scopus "Sources" / "content" page, and/or
- Scimago's **journal ranking CSV** (scimagojr.com → Journal Rankings → Download data).

Then `add_paper.py` matches each paper's ISSN: *indexed* (active), *in list but inactive*, *discontinued for quality reasons*, or *not found*, plus the SJR quartile.
Without a list the field says `unknown`. I never guess. Conference papers are matched by their proceedings ISSN/ISBN; arXiv preprints are not Scopus-indexed.
Remember that "Scopus-indexed" is a property of the **venue**, not of the paper's quality, and a venue can be indexed and still weak.

## Honesty rules
- Numbers are copied from the paper with a page reference or are not written.
- `read_status: reviewed` only after I read the whole text. `extracted` means text exists but I have not reviewed it.
- Anything I could not verify is written as "unverified".
- Scanned PDFs (`chars/page ~ 0`) are read visually page by page.

## Suggested order for the 21 papers already queued (most threatening to our novelty first)
| Batch | Papers |
|---|---|
| 1 | Li 2026 (GNN failure-propagation prediction), Chain-of-Event (FSE 2024), DeepHunt (TOSEM) |
| 2 | Pham et al. (ASE 2024), MicroRCA-Agent (2025), CHASE |
| 3 | Fu et al. survey (CSUR 2025), Wang and Qi survey, Barata et al. survey (these also feed `PROBLEM_EVIDENCE.md`) |
| 4 | Few-shot cross-system anomaly trace classification, Graph Neural AI with temporal dynamics, Hybrid RCA (Erakovic and Pahl) |
| 5 | Xie et al. hypergraph RCA (arXiv 2511.17566), Ortiz et al. real-time context-aware architecture, Podduturi AI monitoring |
| 6 | Faseeha observability survey, Mamba cost-sensitive, MaaS cascading failures |
| 7 | Maheshkar agentic RCA, "real-time" RCA (Vangapelli; placeholder DOI), CausalRCA (scanned) |

Then the 44 abstract-only papers from `docs/literature/literature_matrix.csv`, once you supply the PDFs.
