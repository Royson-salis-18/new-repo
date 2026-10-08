# Batch 07: 2026-10-08

Papers: 1) theysayitsre (Vangapelli 2026, position paper), 2) bridgingtheg (Maheshkar 2025, AURORA), 3) causalrca (Xin, Chen, Zhao, JSS 2023).
Read: all three. 1 and 2 in full (figures not inspected). 3 (scanned PDF) as rendered images, pages 1-12 (page 13 references unread), after you granted permission to install a renderer (pypdfium2; PyMuPDF was blocked by the Windows Application Control policy).
Scopus: bridgingtheg ISSN 2178-7727 = Acta Scientiae (education; mismatch); theysayitsre no ISSN; causalrca ISSN 0164-1212 confirmed by Crossref, Scopus preview not yet checked. SJR quartiles unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side
| | Vangapelli | Maheshkar (AURORA) | Xin et al. (CausalRCA) | Ours |
|---|---|---|---|---|
| Type | position paper | LLM multi-agent framework | causal metric RCA method | RCA + untested risk |
| Labels | n/a | mixed | none | none |
| Propagation | none | causal discovery, Granger, PageRank | weighted causal graph | edge probabilities |
| Forecasting | no | no | no | claimed, untested |
| Open | no | code repo, no data | code + data (no license) | yes |
| Headline | none of its own | top-5 94.3% Sock-Shop (internally inconsistent) | Avg@5 0.6681 vs 0.5738 (+9.43%), one Sock-Shop | none on real faults |
| Evidence quality | 1 | 1 | 2 | 1 |

## 2. What each means for our claims
- Vangapelli: nothing measured; do not cite as evidence. Its stale-context point is an opinion.
- Maheshkar: unreliable (conflicting timing tables, impossible CI/fraction fit, venue mismatch, unverifiable production claims). Not usable as a baseline or as evidence.
- CausalRCA: label-free causal-graph metric RCA exists; modest gains over PC/GES/LiNGAM+PageRank on one Sock-Shop, own-tuned, 10 runs; not citable as a general win. Code and data are open (no license).

## 3. Does this batch change the problem statement?
No. It adds two weak-evidence papers; "LLM agent plus causal discovery RCA" claims exist but are not trustworthy.

## 4. Baselines and datasets to add
CausalRCA repo (github.com/AXinx/CausalRCA_code, data_collected folder) is a candidate extra baseline or dataset; not downloaded or run.

## 5. Claims in our draft this batch weakens
None strongly. Avoid citing AURORA numbers.

## 6. Sentences we can safely write
- "Position papers argue RCA quality depends on fresh topology and change context [theysayitsre]" (label as opinion).
- "Causal-structure-learning methods for fine-grained metric RCA exist [causalrca]."
- Do NOT write AURORA's or Vangapelli's relayed numbers.

## 7. Corrections to earlier notes
None new. The Li (2026) citation in Vangapelli is mismatched to its claim (see its note).

## 8. Proposals (no code changed)
Reuse the sanity checks used here (binomial CI vs sample size, k/n feasibility, table-to-table consistency) as an evaluation-hygiene checklist for our own results.
