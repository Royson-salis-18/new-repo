import json, time, requests, pathlib

OUT = pathlib.Path(r"C:\Users\MITE\Downloads\final project (short and sweet)\docs\literature")
OUT.mkdir(parents=True, exist_ok=True)

QUERIES = {
  "rca_core": ["root cause analysis microservices", "root cause localization microservice systems", "root cause analysis distributed tracing anomaly",
               "fault localization microservices graph", "microservice anomaly detection root cause multimodal"],
  "rca_unsupervised": ["unsupervised root cause analysis microservice", "causal inference root cause microservices", "causal discovery microservice root cause",
                       "PageRank root cause microservice", "graph neural network root cause localization microservice", "graph autoencoder failure localization microservice"],
  "cascade": ["cascading failure microservices", "failure propagation microservice dependency", "cascading failure prediction microservice architecture",
              "fault propagation analysis microservices", "failure propagation probability service dependency graph", "cascading failures cloud services prediction",
              "microservice resilience cascading failure circuit breaker", "service dependency graph failure impact prediction"],
  "anomaly": ["anomaly detection microservices metrics logs traces", "multivariate time series anomaly detection microservice", "log anomaly detection deep learning",
              "trace anomaly detection microservice", "isolation forest microservice anomaly"],
  "llm_agent": ["large language model root cause analysis cloud incidents", "LLM agent root cause analysis microservices", "agentic AI root cause analysis",
                "LLM incident management cloud"],
  "benchmarks": ["benchmark root cause analysis microservice dataset", "microservice fault injection dataset benchmark", "RCAEval benchmark", "chaos engineering microservices fault injection"],
  "online_live": ["online root cause analysis streaming telemetry microservice", "real-time root cause analysis microservice"],
  "surveys": ["survey root cause analysis microservices", "survey AIOps anomaly detection incident", "survey failure diagnosis cloud microservice"],
}
FIELDS = "id,title,publication_year,cited_by_count,doi,type,primary_location,abstract_inverted_index,authorships,ids"

def abstract(inv):
    if not inv: return ""
    pos = {}
    for w, idxs in inv.items():
        for i in idxs: pos[i] = w
    return " ".join(pos[i] for i in sorted(pos))

papers = {}
for cat, qs in QUERIES.items():
    for q in qs:
        try:
            r = requests.get("https://api.openalex.org/works", timeout=40,
                             params={"search": q, "per-page": 40, "select": FIELDS, "filter": "from_publication_date:2012-01-01,type:article|preprint|book-chapter|proceedings-article"})
            r.raise_for_status()
        except Exception as e:
            print("ERR", q, e); continue
        for w in r.json().get("results", []):
            if not w.get("title"): continue
            p = papers.setdefault(w["id"], {"id": w["id"], "title": w["title"], "year": w.get("publication_year"),
                "cites": w.get("cited_by_count", 0), "doi": w.get("doi"),
                "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                "venue_type": ((w.get("primary_location") or {}).get("source") or {}).get("type"),
                "first_author": ((w.get("authorships") or [{}])[0].get("author") or {}).get("display_name"),
                "abstract": abstract(w.get("abstract_inverted_index")), "cats": set(), "queries": set(), "arxiv": (w.get("ids") or {}).get("arxiv")})
            p["cats"].add(cat); p["queries"].add(q)
        time.sleep(0.25)
    print(cat, "->", len(papers), "unique so far")

rows = []
for p in papers.values():
    p["cats"] = sorted(p["cats"]); p["queries"] = sorted(p["queries"]); rows.append(p)
rows.sort(key=lambda p: -p["cites"])
(OUT / "raw_openalex.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
print("total", len(rows))
