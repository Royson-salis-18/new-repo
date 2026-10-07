# Is the problem real? Evidence ledger

Purpose: keep an honest record of what the literature actually shows about the problem we claim to solve, so the paper's motivation rests on cited evidence
and not on assumptions. Add a row for every claim a **reviewed** paper makes. Quote nothing; paraphrase and give the page.

## Our claimed problem (draft wording)
Root-cause localization on live, unlabeled, architecture-varying telemetry is hard; early identification of cascading-failure risk is under-addressed;
this lengthens debugging time for operators.

## A. Evidence the problem is real (pro)
| # | Claim (paraphrased) | Source (key, page) | Evidence type (measured / anecdotal / assumed) | Strength |
|---|---|---|---|---|
| | | | | |

## B. Evidence our specific gap is already addressed (con)
| # | What exists | Source (key, page) | How close to our contribution | Consequence for us |
|---|---|---|---|---|
| 1 | Verified by abstract (not yet in full): AID (2021) predicts cascading impact via dependency intensity | see docs/REVIEW_REPORT.md section 3.2 | high | must be cited and compared |
| 2 | Verified by abstract: IEEE TNSM 2025 GNN fault forecasting with probabilistic propagation | same | high | must be cited and compared |

## C. Open questions about the problem
- Do operators actually lack early warning, or do they lack *trust in* and *actionability of* alerts? (look for incident studies)
- What fraction of incidents propagate along call edges vs shared infrastructure? (our model assumes call edges)
- What debugging-time numbers exist from real incidents, and who measured them?
