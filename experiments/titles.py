import json, time, requests, pathlib, re

OUT = pathlib.Path(r"C:\Users\MITE\Downloads\final project (short and sweet)\docs\literature")
TITLES = [
 "MicroRCA: Root Cause Localization of Performance Issues in Microservices",
 "Root Cause Analysis of Failures in Microservices through Causal Discovery",
 "Causal Inference-Based Root Cause Analysis for Online Service Systems with Intervention Recognition",
 "Practical Root Cause Localization for Microservice Systems via Trace Analysis",
 "Localizing failure root causes in a microservice through causality inference",
 "Interpretable Fine-Grained Root Causes Analysis for Microservices on Multi-modal Observability Data",
 "Eadro: An End-to-End Troubleshooting Framework for Microservices on Multi-source Data",
 "Actionable and Interpretable Fault Localization for Recurring Failures in Online Service Systems",
 "RCAEval: A Benchmark for Root Cause Analysis of Microservice Systems with Telemetry Data",
 "OpenRCA: Can Large Language Models Locate the Root Cause of Software Failures?",
 "Root Cause Analysis for Microservices based on Causal Inference: How Far Are We?",
 "Exploring LLM-based Agents for Root Cause Analysis",
 "mABC: multi-Agent Blockchain-Inspired Collaboration for root cause analysis in micro-services architecture",
 "RCAgent: Cloud Root Cause Analysis by Autonomous Agents with Tool-Augmented Large Language Models",
 "MonitorRank: Ranking Anomalous Services for Root Cause Analysis",
 "CloudRanger: Root Cause Identification for Cloud Native Systems",
 "MicroHECL: High-Efficient Root Cause Localization in Large-Scale Microservice Systems",
 "Sage: Practical and Scalable ML-Driven Performance Debugging in Microservices",
 "Seer: Leveraging Big Data to Navigate the Complexity of Performance Debugging in Cloud Microservices",
 "Microservice Root Cause Analysis With Limited Observability Through Intervention Recognition in the Latent Space",
 "Unsupervised Detection of Microservice Trace Anomalies through Service-Level Deep Bayesian Networks",
 "Predicting Node Failure in Cloud Service Systems",
 "Gremlin: Systematic Resilience Testing of Microservices",
 "Maximizing the spread of influence through a social network",
 "Learning influence probabilities in social networks",
 "Inferring networks of diffusion and influence",
 "Catastrophic cascade of failures in interdependent networks",
 "Cascade-based attacks on complex networks",
 "Isolation Forest",
 "Anomaly detection: A survey",
 "Alibaba cluster microservice traces call graph characterization",
 "Characterizing microservice dependency and performance: Alibaba trace analysis",
 "Metastable Failures in Distributed Systems",
 "Automap: Diagnose your microservice-based web applications automatically",
 "Anomaly detection and failure root cause analysis in microservice-based cloud applications multimodal survey",
 "ChaosOrca fault injection containers",
 "TrainTicket: benchmarking microservice systems for software engineering research",
 "Sock Shop microservices demo application observability",
 "PyRCA: A Library for Metric-based Root Cause Analysis",
 "Multimodal causal root cause diagnosis microservices Granger",
 "Fault propagation graph prediction microservice early warning failure forecasting",
 "Predicting failures in microservice systems before they happen metrics forecasting",
 "OpenTelemetry demo microservices dataset anomalies",
 "AIOps incident management large language models survey cloud",
 "Hawkes process root cause analysis alarm propagation topology",
 "Bayesian network fault diagnosis service dependency probabilistic root cause",
 "Probabilistic graphical model failure propagation distributed system root cause",
 "Online change point detection root cause analysis microservices",
 "Counterfactual root cause analysis microservices",
]
FIELDS = "id,title,publication_year,cited_by_count,doi,type,primary_location,abstract_inverted_index,authorships,ids"

def abstract(inv):
    if not inv: return ""
    pos = {}
    for w, idxs in inv.items():
        for i in idxs: pos[i] = w
    return " ".join(pos[i] for i in sorted(pos))

def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower())

found = {}
for t in TITLES:
    try:
        r = requests.get("https://api.openalex.org/works", params={"search": t, "per-page": 5, "select": FIELDS}, timeout=40)
        res = r.json().get("results", [])
    except Exception as e:
        print("ERR", t[:50], e); continue
    best, bscore = None, 0
    tw = set(norm(t).split())
    for w in res:
        ww = set(norm(w.get("title") or "").split())
        sc = len(tw & ww) / max(len(tw | ww), 1)
        if sc > bscore: best, bscore = w, sc
    status = "OK " if bscore >= 0.6 else "?? "
    if best:
        print(f"{status}{bscore:.2f} {best['publication_year']} c={best['cited_by_count']:4d} [{(((best.get('primary_location') or {}).get('source') or {}).get('display_name') or '')[:30]:30}] {best['title'][:90]}")
        found[t] = {"query": t, "match": bscore, "id": best["id"], "title": best["title"], "year": best["publication_year"], "cites": best["cited_by_count"],
                    "doi": best.get("doi"), "venue": ((best.get("primary_location") or {}).get("source") or {}).get("display_name"),
                    "first_author": ((best.get("authorships") or [{}])[0].get("author") or {}).get("display_name"), "abstract": abstract(best.get("abstract_inverted_index"))}
    else:
        print("-- none", t[:70])
    time.sleep(0.25)
(OUT / "targeted.json").write_text(json.dumps(found, indent=1), encoding="utf-8")
