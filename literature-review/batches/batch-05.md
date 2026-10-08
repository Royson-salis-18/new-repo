# Batch 05: 2026-10-07

Papers: 1) shuaiyuxie...root (CCLH, arXiv 2511.17566), 2) realtimecont (Ortiz et al., IEEE Access 2019), 3) podduturi2025microservice (ICCSAIML'25). All read in full: yes, with exceptions: Xie Figs 1-6 not inspected; Ortiz figures and appendix tables not inspected, reference list skimmed after [41].
Scopus: Xie = arXiv preprint, not indexed, not peer reviewed; Ortiz = IEEE Access, venue indexed (ISSN 2169-3536; CiteScore 2025 9.3, 91st percentile); Podduturi = ISSN 3050-9246 not found in Scopus preview. SJR quartiles unknown (no list supplied; please add a Scopus or Scimago file to `litdb/reference/`).

## 1. Side-by-side
| | Xie et al. (CCLH) | Ortiz et al. | Podduturi | Ours |
|---|---|---|---|---|
| Task | supervised RCL + failure-type identification | IoT predictive architecture (not RCA) | narrative overview | RCA + untested risk |
| Labels needed | yes | n/a (ARIMA forecasting) | n/a | no |
| Telemetry | metrics, traces, logs, deployment | air-quality sensors | generic | traces (+ metrics, SSH) |
| Propagation / graph | hypergraph: call, co-location, load-balancing siblings | none | none | call edges only |
| Forecasts failures | no | no (forecasts pollutant levels) | generic claims | claimed, untested |
| Data (open?) | A public (GAIA); B, C self-collected, not stated released; no code | dataset DOI (unopened) | none | open |
| Baselines | 6 incl. DiagFusion, TVDiag, DeepHunt (supervised variant) | none | none | random, earliest, anomaly-only, own PageRank |
| Headline result | HR@1 0.875 / 0.923 / 0.918 (Table I p.8) | under 0.06 s per message; alert-level hit rate 48.64% to 100% | none | none on real faults |
| Evidence quality (1-5) | 2 | 2 (irrelevant) | 1 | 1 |
| Scopus status | not indexed | venue indexed | not found | n/a |

## 2. What each means for our claims
- **Xie et al.:** the only useful paper in this batch. It shows that propagation channels beyond call edges (co-location on a host, sibling instances behind a load balancer) are modelled in recent supervised RCA work, and its ablation without the hypergraph loses about 0.08 to 0.14 Avg@3 and 0.08 to 0.32 F1 on its datasets (Table II p.8). This supports listing shared-infrastructure propagation as a limitation of our call-edge model and a planned extension. It also shows how unstable baseline comparisons are: its supervised DeepHunt variant scores HR@1 0.31 to 0.44, far below DeepHunt's published values.
- **Ortiz et al.:** off-topic. Remove from the RCA literature list.
- **Podduturi:** no evidence; references appear erroneous or fabricated (6 of 8 DOIs not found, 2 unrelated). Remove from any citation list and warn the team.

## 3. Does this batch change the problem statement?
- Real? No measured evidence of incident cost or time-to-diagnose in any of the three. Xie cites a GitHub availability report (about 1.5 hours to resolve a codespace failure) and shows demo-system illustrations of group effects.
- Already solved? No. Group-level propagation in a supervised setting exists; label-free is open in this respect.
- Misframed? Our "propagation along call edges only" assumption is explicitly challenged by Xie's Fig 1 demonstrations (co-location and load balancing); we must state this limitation and, ideally, test it.

## 4. Baselines and datasets to add because of this batch
- GAIA dataset (github.com/CloudWise-OpenSource/GAIA-DataSet, 10 instances, 1,099 cases; used by Xie and CHASE), subject to the user's permission to download.
- A non-call-edge propagation variant of our model (host co-location edges, sibling edges) as an ablation, with data from our EC2 hosts if the SSH or docker metrics expose co-location.
- No new external baselines (CCLH has no code).

## 5. Claims in our draft that this batch contradicts or weakens
- "Failures propagate along observed call edges" (our modelling assumption): contradicted as a general statement by Xie et al.'s demonstrations; we should present it as an assumption with a limitation.
- Any reference to Ortiz et al. or Podduturi as microservice-RCA or prediction literature must be removed.

## 6. Sentences we can safely write (with citation keys)
- "Recent supervised RCA models represent group relationships among instances, such as co-location on a host and load-balancing siblings, as hyperedges [shuaiyuxie...root, arXiv preprint]."
- "Failure propagation in microservices is not limited to call edges: resource contention among co-located instances and load redistribution to siblings have been demonstrated on Online Boutique [same]."
- Do NOT write: that CCLH outperforms DeepHunt in general; that CCLH is peer reviewed; any claim from Podduturi; that Ortiz et al. concerns microservice failure prediction.

## 7. Corrections needed to earlier notes or reports
1. `docs/REVIEW_REPORT.md` Appendix A lists "Real-Time Context-Aware (Ortiz 2019)" and "AI for Microservice Monitoring (Podduturi 2025)" among papers read as relevant. Ortiz et al. is an IoT air-quality architecture, unrelated to microservice RCA; Podduturi is an overview with an unverifiable reference list. Neither should be cited.
2. The REVIEW_REPORT note that the Xie et al. paper is "hypergraph RCA" is correct; it is supervised (cross-entropy on culprit and failure type), not label-free, and has no code link.
3. REVIEW_REPORT Appendix B says OpenRCA (ICLR 2025) was not found; CCLH cites "OpenRCA: Can large language models locate the root cause of software failures?" at ICLR 2025 (p.11). That corroborates the existence of the paper; verify its title and details before citing.
4. Xie et al. cite "Zhang et al., Failure diagnosis in microservice systems: a comprehensive survey and analysis, ACM TOSEM 2024" (ref [2]); this matches the correction in batch 3 (the survey attributed to "Pham" in the matrix is by Zhang et al.).
