"""Root cause ranking: combine anomaly strength, temporal precedence and cascade explanation."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .cascade import cascade_risk, edge_probabilities, path_probabilities
from .detector import Detection
from .telemetry import Telemetry


@dataclass
class RCAResult:
    ranking: list[tuple[str, float]]       # (service, score), best first
    onset: dict[str, int]                  # window index where each flagged service first deviated
    strength: dict[str, float]
    risk: dict[str, float]                 # cascade risk for every service
    P: np.ndarray                          # propagation probabilities, services x services
    services: list[str]


def rank(tel: Telemetry, det: Detection, window: tuple[int, int], max_lag: int = 4,
         max_hops: int = 3, method: str = "full") -> RCAResult:
    """Rank candidate root causes inside window = (start, stop) of window indices.

    method: full | anomaly_only | earliest | random (the last three are ablations/baselines).
    """
    s0, s1 = window
    flags = det.flags[s0:s1]
    cand = [i for i in range(len(tel.services)) if flags[:, i].any()]
    strength = {i: float(det.a[s0:s1, i].max()) for i in cand}
    onset = {i: int(np.argmax(flags[:, i])) + s0 for i in cand}

    probs = edge_probabilities(tel, det.flags, max_lag)
    P = path_probabilities(tel.services, probs, max_hops)

    scores = {}
    if method == "random":
        rng = np.random.default_rng(0)
        scores = {i: float(rng.random()) for i in cand}
    elif method == "anomaly_only":
        scores = dict(strength)
    elif method == "earliest":
        scores = {i: -onset[i] + 1e-3 * strength[i] for i in cand}
    else:
        total = sum(strength.values()) or 1.0
        t_min, t_max = (min(onset.values()), max(onset.values())) if cand else (0, 0)
        for u in cand:
            prec = 1.0 if t_max == t_min else 1.0 - (onset[u] - t_min) / (t_max - t_min)
            blast = sum(P[u, v] * strength[v] for v in cand if v != u) / total
            # How much of u's own anomaly is already explained by an earlier failing upstream cause?
            explained = max((P[w, u] * strength[w] for w in cand if w != u and onset[w] <= onset[u]),
                            default=0.0)
            scores[u] = strength[u] * (0.4 * prec + 0.6 * blast) * (1.0 - 0.8 * explained)

    ranking = sorted(((tel.services[i], sc) for i, sc in scores.items()), key=lambda x: -x[1])
    a_now = det.a[s1 - 1]
    risk = cascade_risk(a_now, P)
    return RCAResult(ranking=ranking,
                     onset={tel.services[i]: t for i, t in onset.items()},
                     strength={tel.services[i]: v for i, v in strength.items()},
                     risk={s: float(r) for s, r in zip(tel.services, risk)},
                     P=P, services=tel.services)
