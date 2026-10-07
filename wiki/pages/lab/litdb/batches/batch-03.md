# Batch 03: 2026-10-07

Papers (all surveys): 1) fu2025intelligent, 2) tingtingwangguilinqi2024comprehensive (Wang and Qi), 3) barata2026anomaly. All read in full: yes, with exceptions: figures not inspected in any of the three; reference lists were searched for key terms, not read entry by entry.
Scopus: Fu = ACM Computing Surveys, venue indexed (CiteScore 2025 65.2, 99th percentile); Barata = Cluster Computing, venue indexed (CiteScore 2025 8.4, 82nd percentile); Wang and Qi = arXiv preprint, not indexed, not peer reviewed. SJR quartiles unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side
| | Fu 2025 | Wang and Qi 2024 | Barata 2026 | Ours |
|---|---|---|---|---|
| Type | peer-reviewed survey (CSUR) | arXiv survey | peer-reviewed PRISMA survey (Cluster Computing) | n/a |
| Scope | RCA in microservices; data collection, direct vs indirect analysis | RCA by data modality + LLM | anomaly detection and root-cause identification | RCA + risk forecasting |
| Selection method | none stated | none stated | PRISMA, 10,485 records to 143 (abstract says 117) | n/a |
| Labels discussed | supervised needs engineer-prepared labels (pp.22-23) | mentions recurring failures | UL most used detection class (p.25) | label-free |
| Propagation / graph | causal and topological graphs, random walk | dependency, topology, causal, KG | graph-based dominates RCI | edge probabilities |
| Forecasting | not covered (Seer and one 2020 reference only) | passing (Sage, [91]) | not covered (search terms exclude it) | claimed |
| Quantitative comparison | none (check marks) | none | averages across studies, invalid | n/a |
| Motivation evidence | cited, unmeasured | outage table (anecdotal) + 74.38% recurrence (cited) | anecdotes (Amazon, Walmart) | n/a |
| Evidence quality (1-5) | 3 | 2 | 2 | n/a |
| Scopus status | indexed venue | not indexed | indexed venue | n/a |

## 2. What each means for our claims
- **Fu:** best peer-reviewed taxonomy to cite. States that supervised RCA needs costly labels and that benchmark fault types differ from production, both supporting our framing. Omits DeepHunt, BARO, Eadro, DiagFusion, Nezha, and its "Pham et al." reference is a 2016 paper, so it does not use the 2024 benchmark evidence.
- **Wang and Qi:** preprint with weak rigor; useful only for its remark that most failures recur in some systems (about 74%, second-hand from DejaVu) and for naming Sage and a log-based cascade explanation work. Table 1 outage entries are unverified.
- **Barata:** useful catalogues of testbeds (Table 8) and datasets (Table 9); its performance averages are invalid and must not be cited; its search strings exclude "root cause", "propagation" and "cascad*", so its silence on cascade forecasting is a sampling artifact, not evidence of a gap.

## 3. Does this batch change the problem statement?
- Real? The surveys agree that RCA is hard and that labels are costly, but none supplies measured incident cost or time-to-diagnose data. The recurrence statistic (about 74%, via DejaVu) raises a point: if most failures recur, historical labels are valuable, so "label-free" must be justified by deployment realities (new systems, drift), not assumed.
- Already solved? No survey claims it is solved; none reviews cascade forecasting as a task.
- Misframed? The surveys do not support the claim that "cascade prediction is under-explored": they do not cover it. That claim must rest on our own literature search (REVIEW_REPORT lists at least eight works), not on these surveys.

## 4. Baselines and datasets to add because of this batch
- Candidate additional public datasets from the catalogues: AIOps Challenge 2020/2021, GAIA (check availability), TraceRCA dataset (Fu Table 7, Barata Table 9). Each needs the user's permission before download.
- Testbeds to consider besides Online Boutique/Sock Shop/Train Ticket: DeathStar Social Network, Hipster-Shop.
- No new baselines beyond those from batches 1 and 2.

## 5. Claims in our draft that this batch contradicts or weakens
- "Cascade prediction is under-explored" cannot be supported by citing these surveys; they do not review it.
- "State of the art is deep, supervised, graph-based" is weakened: surveys themselves note labels are costly and unsupervised methods dominate detection.
- Any claim that survey-averaged performance shows a best method class: invalid (Barata's own caveat).

## 6. Sentences we can safely write (with citation keys)
- "Surveys group microservice RCA into direct methods and indirect, graph-based methods [fu2025intelligent]."
- "Supervised RCA methods require engineer-prepared labels, which are costly to obtain [fu2025intelligent]."
- "Public benchmark faults (CPU or memory exhaustion, packet loss, delay) differ from the more varied faults seen in production [fu2025intelligent]."
- "Train Ticket and Sock Shop are the most-used open testbeds [barata2026anomaly; fu2025intelligent Table 4]."
- "Surveys of RCA report difficulty in comparing methods across studies because datasets and metrics differ [barata2026anomaly]."
- Do NOT write: Barata's category averages; Wang and Qi's Table 1 impact figures; "no survey covers cascade forecasting" as proof it is unexplored; the 117 or 143 study count without noting the discrepancy.

## 7. Corrections needed to earlier notes or reports
1. REVIEW_REPORT section 3.1 lists "Pham et al. failure-diagnosis survey (TOSEM 2025)". Crossref shows DOI 10.1145/3715005 ("Failure Diagnosis in Microservice Systems: A Comprehensive Survey and Analysis", ACM TOSEM, 2025) is by Zhang, Xia, Fan, Shi, Xiong, Zhong, Ma, Sun, Pei (Barata ref [27] agrees). The matrix key `pham2025diag` in `docs/literature/literature_matrix.csv` is a mislabel. Not read by us yet; flagged for a later batch.
2. REVIEW_REPORT lists the Fu survey as read in full [F]; now confirmed read; but note it omits recent label-free multimodal methods and does not cite the 2024 ASE benchmark.
3. REVIEW_REPORT Appendix A treats Wang and Qi as a local survey; it is a preprint (arXiv 2408.00803) with a placeholder DOI.
4. REVIEW_REPORT describes the Barata survey implicitly as a source on RCA; its search strategy excludes RCA keywords; its aggregate performance numbers are not citable.
5. The queue key `barata2026anomaly` indicates 2026; the paper was published online 3 June 2026 (Cluster Computing 29:309), consistent with metadata.
