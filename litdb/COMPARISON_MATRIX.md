# Comparison with our work (reviewed papers only)

| Key | Supervision | Online | Telemetry | Propagation | Forecasts failures | LLM | Datasets (open?) | Result | Overlap | Threat |
|---|---|---|---|---|---|---|---|---|---|---|
| li2026service | supervised (cr | claimed  | service logs, API-call | GNN (GAT + GRU/Transform | yes (h | no | proprietary, anonymized; (no (p) | P 0.94, R 0.92, accuracy 0.93, detection time 3.2  | high (ta | medium ( |
| sun2025interpretable | label-free at  | partly:  | traces, logs (Drain te | GNN (GraphSAGE-style GAE | no | no | D1 (210 failures, 3,714  (partl) | 30% labels: D1 A@1 0.803, A@5 0.966, Avg@5 0.898;  | high (la | high for |
| yao2024chain | supervised (tr | no (inci | events derived from me | learned weighted event-c | no | no (BERT | Service dataset (170 inc (no) | Service: top-1 79.3%, top-3 98.8%; Business: top-1 | partial  | low (for |
