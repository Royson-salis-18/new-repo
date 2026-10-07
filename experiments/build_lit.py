import json, re, csv, pathlib
ROOT = pathlib.Path(r"C:\Users\MITE\Downloads\final project (short and sweet)"); D = ROOT / "docs/literature"
pool = {}
for f in ("raw_openalex.json", "on_topic.json"):
    for p in json.loads((D / f).read_text(encoding="utf-8")): pool[p["id"]] = p
for p in json.loads((D / "targeted.json").read_text(encoding="utf-8")).values():
    pool.setdefault(p["id"], {**p, "cites": p.get("cites", 0)})
for p in json.loads((D / "team_lookup.json").read_text(encoding="utf-8")):
    if p.get("title"): pool.setdefault("team:" + p["title"], p)
norm = lambda s: re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())

# (key, title-substring, category, read-depth, relevance-to-our-claims)
# depth: FULL = full text read (local PDF); ABS = abstract/metadata only; SEE = known from a verified citing source only
L = [
 # --- surveys
 ("soldani2022", "Anomaly Detection and Failure Root Cause Analysis in (Micro) Service-Based Cloud Applications", "survey", "ABS", "background"),
 ("fu2025rcl", "Intelligent Root Cause Localization in MicroService Systems", "survey", "FULL", "background; local copy"),
 ("wang2024survey", "A Comprehensive Survey on Root Cause Analysis in (Micro) Services", "survey", "FULL", "background; local copy"),
 ("pham2025diag", "Failure Diagnosis in Microservice Systems: A Comprehensive Survey and Analysis", "survey", "ABS", "background"),
 ("zhang2025aiopsllm", "A Survey of AIOps in the Era of Large Language Models", "survey", "ABS", "LLM context"),
 ("notaro2021", "A Survey of AIOps Methods for Failure Management", "survey", "ABS", "background"),
 # --- graph / propagation based RCA
 ("wu2020microrca", "MicroRCA: Root Cause Localization of Performance Issues in Microservices", "graph-RCA", "ABS", "baseline (PageRank family)"),
 ("wang2018cloudranger", "CloudRanger: Root Cause Identification for Cloud Native Systems", "graph-RCA", "ABS", "baseline"),
 ("liu2021microhecl", "MicroHECL: High-Efficient Root Cause Localization in Large-Scale Microservice Systems", "graph-RCA", "ABS", "closest: anomaly propagation chains"),
 ("meng2020microcause", "Localizing Failure Root Causes in a Microservice through Causality Inference", "causal-RCA", "ABS", "baseline"),
 ("ma2020automap", "AutoMAP: Diagnose Your Microservice-based Web Applications Automatically", "graph-RCA", "ABS", "baseline"),
 ("graphbased2019", "Graph-based root cause analysis for service-oriented and microservice architectures", "graph-RCA", "ABS", "background"),
 ("anomprop2021", "Anomaly Propagation Based Fault Diagnosis for Microservices", "graph-RCA", "ABS", "propagation; close"),
 # --- causal / unsupervised multimodal
 ("li2022circa", "Causal Inference-Based Root Cause Analysis for Online Service Systems with Intervention Recognition", "causal-RCA", "ABS", "baseline (CIRCA)"),
 ("ikram2022rcd", "Root Cause Analysis of Failures in Microservices Through Causal Discovery", "causal-RCA", "ABS", "baseline (RCD)"),
 ("xin2023causalrca", "CausalRCA: Causal inference based precise fine-grained root cause localization", "causal-RCA", "ABS", "baseline; local PDF unreadable (scanned)"),
 ("pham2024far", "Root Cause Analysis for Microservice System based on Causal Inference: How Far Are We?", "evaluation-critique", "FULL", "KEY: no method wins; synthetic != real"),
 ("pham2024baro", "BARO: Robust Root Cause Analysis for Microservices via Multivariate Bayesian Online Change Point Detection", "unsup-RCA", "ABS", "baseline; strong simple method"),
 ("sun2024deephunt", "Interpretable Failure Localization for Microservice Systems Based on Graph Autoencoder", "unsup-RCA", "FULL", "closest: self-supervised multimodal; has online stage"),
 ("zhang2023diagfusion", "Robust Failure Diagnosis of Microservice System Through Multimodal Data", "multimodal-RCA", "ABS", "baseline (DiagFusion)"),
 ("yu2023nezha", "Nezha: Interpretable Fine-Grained Root Causes Analysis for Microservices on Multi-modal Observability Data", "multimodal-RCA", "ABS", "baseline; dataset"),
 ("lee2023eadro", "Eadro: An End-to-End Troubleshooting Framework for Microservices on Multi-source Data", "multimodal-RCA", "ABS", "baseline"),
 ("li2022dejavu", "Actionable and interpretable fault localization for recurring failures in online service systems", "multimodal-RCA", "ABS", "supervised baseline"),
 ("yu2021tracerca", "Practical Root Cause Localization for Microservice Systems via Trace Analysis", "trace-RCA", "ABS", "baseline (TraceRCA)"),
 ("hou2021aid", "AID: Efficient Prediction of Aggregated Intensity of Dependency in Large-scale Cloud Systems", "cascade-prediction", "ABS", "CLOSEST: predicts cascading impact via dependency intensity"),
 ("trinity2024", "TrinityRCL: Multi-Granular and Code-Level Root Cause Localization", "multimodal-RCA", "ABS", "background"),
 ("hemirca2024", "HeMiRCA: Fine-Grained Root Cause Analysis for Microservices with Heterogeneous Data Sources", "multimodal-RCA", "ABS", "background"),
 ("microirc2024", "MicroIRC: Instance-level Root Cause Localization for Microservice Systems", "multimodal-RCA", "ABS", "background (team sheet)"),
 ("micronet2024", "MicroNet: Operation Aware Root Cause Identification of Microservice System Anomalies", "multimodal-RCA", "ABS", "background (team sheet)"),
 ("torai2026", "TORAI: Multi-source Root Cause Analysis for Blind Spots in Microservice Service Call Graph", "unsup-RCA", "ABS", "unsupervised, call-graph-free; close"),
 ("mhprca2025", "MHP-RCA: Multivariate Hawkes Process-based Root Cause Analysis in microservice systems", "event-RCA", "ABS", "event/Hawkes alternative; close"),
 ("limited2024", "Microservice Root Cause Analysis With Limited Observability Through Intervention Recognition in the Latent Space", "causal-RCA", "ABS", "background"),
 ("dgercl2024", "DGERCL: A Dynamic Graph Embedding Approach for Root Cause Localization in Microservice Systems", "graph-RCA", "ABS", "background"),
 # --- cascade / failure propagation / forecasting
 ("gnnfault2025", "Explainable GNN-Based Approach to Fault Forecasting in Cloud Service Debugging", "cascade-prediction", "ABS", "CLOSEST: probabilistic failure propagation, GNN forecasting"),
 ("container2023", "Container cascade fault detection based on spatial", "cascade-prediction", "ABS", "CLOSEST: cascade fault model, supervised"),
 ("explcascade2024", "Explaining Microservices' Cascading Failures From Their Logs", "cascade-explain", "ABS", "close: explains cascades (declarative)"),
 ("stmformer2024", "System States Forecasting of Microservices with Dynamic Spatio-Temporal Data", "forecasting", "ABS", "forecasting baseline family"),
 ("diffusion2025", "Latent Diffusion over Dynamic Service Graphs for Uncertainty-Quantified Failure Propagation Prediction", "cascade-prediction", "ABS", "close; venue quality unclear"),
 ("sage2021", "Sage: practical and scalable ML-driven performance debugging in microservices", "perf-debug", "ABS", "unsupervised, counterfactual; close in spirit"),
 ("seer2018", "Seer: Leveraging Big Data to Navigate the Increasing Complexity of Cloud Debugging", "perf-debug", "ABS", "predicts QoS violations ahead of time"),
 ("lin2018node", "Predicting Node failure in cloud service systems", "failure-prediction", "ABS", "failure prediction precedent"),
 ("metastable2021", "Metastable failures in distributed systems", "cascade-theory", "ABS", "why cascades matter"),
 ("gremlin2016", "Gremlin: Systematic Resilience Testing of Microservices", "fault-injection", "ABS", "fault injection method"),
 ("alibaba2021", "Characterizing Microservice Dependency and Performance", "dataset-analysis", "ABS", "real call-graph characteristics"),
 # --- theory behind propagation modelling
 ("kempe2003", "Maximizing the spread of influence through a social network", "cascade-theory", "ABS", "independent cascade model (our noisy-OR/propagation)"),
 ("goyal2010", "Learning influence probabilities in social networks", "cascade-theory", "ABS", "learning edge probabilities from co-occurrence (our estimator)"),
 ("gomez2010", "Inferring networks of diffusion and influence", "cascade-theory", "ABS", "NetInf: inferring diffusion"),
 ("buldyrev2010", "Catastrophic cascade of failures in interdependent networks", "cascade-theory", "ABS", "network cascade theory"),
 ("motter2002", "Cascade-based attacks on complex networks", "cascade-theory", "ABS", "load-redistribution cascade model"),
 # --- anomaly detection
 ("liu2008iforest", "Isolation Forest", "anomaly-detection", "ABS", "detector option"),
 ("chandola", "Anomaly Detection: A Survey", "anomaly-detection", "ABS", "background"),
 ("dbn2020", "Unsupervised Detection of Microservice Trace Anomalies through Service-Level Deep Bayesian Networks", "anomaly-detection", "ABS", "trace anomaly baseline"),
 ("tracegra2023", "TraceGra: A trace-based anomaly detection for microservice using graph deep learning", "anomaly-detection", "ABS", "team sheet"),
 ("tracedae2025", "TraceDAE: Trace-Based Anomaly Detection in Microservice Systems via Dual Autoencoder", "anomaly-detection", "ABS", "background"),
 ("traceabench2025", "A Comprehensive Benchmark and Empirical Study of Trace Anomaly Detection", "evaluation-critique", "ABS", "empirical study"),
 ("amulsys2025", "Anomaly detection for microservice system via augmented multimodal data and hybrid graph representations", "anomaly-detection", "ABS", "team sheet; no abstract in OpenAlex"),
 ("tralog2025", "TraLogAnomaly: A microservice system anomaly detection approach based on hybrid event sequences", "anomaly-detection", "ABS", "team sheet; event sequences"),
 # --- LLM / agents
 ("roy2024agents", "Exploring LLM-based Agents for Root Cause Analysis", "llm-agent", "ABS", "agent RCA"),
 ("mabc2024", "mABC: Multi-Agent Blockchain-inspired Collaboration for root cause analysis in micro-services architecture", "llm-agent", "ABS", "agent RCA"),
 ("rcagent2024", "RCAgent: Cloud Root Cause Analysis by Autonomous Agents with Tool-Augmented Large Language Models", "llm-agent", "ABS", "agent RCA"),
 ("ahmed2023llmrca", "Automatic Root Cause Analysis via Large Language Models for Cloud Incidents", "llm-agent", "ABS", "LLM RCA"),
 # --- benchmarks / evaluation
 ("pham2025rcaeval", "RCAEval: A Benchmark for Root Cause Analysis of Microservice Systems with Telemetry Data", "benchmark", "ABS", "KEY dataset (735 cases)"),
 ("petshop2023", "The PetShop Dataset", "benchmark", "ABS", "dataset"),
 ("pyrca2023", "PyRCA: A Library for Metric-based Root Cause Analysis", "benchmark", "ABS", "tooling"),
 ("bench2022", "Constructing Large-Scale Real-World Benchmark Datasets for AIOps", "benchmark", "ABS", "dataset"),
 ("rethink2026", "Rethinking the Evaluation of Microservice RCA with a Fault Propagation-Aware Benchmark", "evaluation-critique", "ABS", "KEY: simple rules match SOTA on 4 benchmarks"),
]
found, missing = [], []
for key, sub, cat, depth, rel in L:
    s = norm(sub); hit = None
    for p in pool.values():
        if s in norm(p["title"]) and (hit is None or (p.get("cites") or 0) > (hit.get("cites") or 0)): hit = p
    (found if hit else missing).append((key, sub, cat, depth, rel, hit))
print(len(found), "matched,", len(missing), "unmatched")
for m in missing: print("  UNMATCHED:", m[0], "|", m[1][:70])

def bibkey(key, p): return key
rows, bib = [], []
for key, sub, cat, depth, rel, p in found:
    doi = (p.get("doi") or "").replace("https://doi.org/", "")
    rows.append({"key": key, "year": p.get("year") or p.get("publication_year"), "title": p["title"], "venue": p.get("venue") or "", "first_author": p.get("first_author") or "",
                 "cites_openalex": p.get("cites", 0), "doi": doi, "category": cat, "read_depth": depth, "relevance": rel})
    ty = "@article" if (p.get("venue") or "").lower() not in ("", "arxiv (cornell university)") and "conference" not in (p.get("venue") or "").lower() and "symposium" not in (p.get("venue") or "").lower() else "@misc"
    bib.append(f"{ty}{{{key},\n  title={{{{{p['title']}}}}},\n  author={{{p.get('first_author') or 'Unknown'} and others}},\n  year={{{p.get('year') or p.get('publication_year')}}},\n"
               f"  journal={{{p.get('venue') or ''}}},\n" + (f"  doi={{{doi}}},\n" if doi else "") + "  note={metadata via OpenAlex; complete author list and venue details must be verified before submission}\n}\n")
rows.sort(key=lambda r: (r["category"], -(r["cites_openalex"] or 0)))
with open(D / "literature_matrix.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
(D / "references.bib").write_text("\n".join(bib), encoding="utf-8")
print("wrote", len(rows), "rows")
from collections import Counter; print(Counter(r["category"] for r in rows))
