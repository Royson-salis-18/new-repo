"""Unsupervised per-service anomaly detection. No labels are used anywhere here.

Calibrate on a baseline slice of *normal* operation, then score every window.
Output `z` is "how many robust standard deviations from normal", `a` maps it to (0, 1).
"""
from __future__ import annotations

from dataclasses import dataclass

import warnings

import numpy as np

from .telemetry import Telemetry

# Absolute scale floors so a flat-zero baseline (e.g. error counts) does not give infinite z.
_ABS_FLOOR = {"cpu": 0.01, "memory": 1e6, "net_rx": 1e3, "net_tx": 1e3,
              "log_errors": 1.0, "latency_p95": 1.0, "trace_errors": 0.05, "span_rate": 2.0}


@dataclass
class Detection:
    z: np.ndarray            # (T, S) service-level deviation score
    a: np.ndarray            # (T, S) anomaly probability-like score in (0, 1)
    flags: np.ndarray        # (T, S) bool, sustained z >= threshold
    feature_z: np.ndarray    # (T, S, F) per-feature deviation, for explanations


def _calibrate(base: np.ndarray, features: list[str]):
    with warnings.catch_warnings():                        # features with no data at all stay NaN -> no evidence
        warnings.simplefilter("ignore", RuntimeWarning)
        med = np.nanmedian(base, axis=0)                   # (S, F)
        mad = np.nanmedian(np.abs(base - med), axis=0) * 1.4826
    floor = np.array([_ABS_FLOOR[f] for f in features])
    med, mad = np.nan_to_num(med), np.nan_to_num(mad)      # no baseline data -> neutral, floor decides
    scale = np.maximum.reduce([mad, 0.1 * np.abs(med), np.broadcast_to(floor, med.shape)])
    return med, scale


def detect(tel: Telemetry, baseline_windows: int, z_threshold: float = 3.5,
           persistence: int = 2, kind: str = "robust_z") -> Detection:
    med, scale = _calibrate(tel.X[:baseline_windows], tel.features)
    fz = np.abs(np.nan_to_num(tel.X, nan=0.0) - med) / scale
    # A missing sample means "no evidence", not "normal value": zero deviation.
    fz = np.where(np.isnan(tel.X), 0.0, fz)
    fz = np.minimum(fz, 50.0)

    if kind == "isolation_forest":
        z = _iforest_z(fz, baseline_windows)
    else:
        z = fz.max(axis=2)
    a = 1.0 / (1.0 + np.exp(-(z - z_threshold)))

    raw = z >= z_threshold
    flags = raw.copy()
    if persistence > 1:  # require `persistence` consecutive windows
        run = np.zeros_like(raw, dtype=int)
        for t in range(raw.shape[0]):
            run[t] = np.where(raw[t], (run[t - 1] if t else 0) + 1, 0)
        flags = run >= persistence
        for t in range(raw.shape[0] - 1, -1, -1):  # back-fill the run's earlier windows
            if t + 1 < raw.shape[0]:
                flags[t] |= raw[t] & flags[t + 1]
    return Detection(z=z, a=a, flags=flags, feature_z=fz)


def _iforest_z(fz: np.ndarray, baseline_windows: int) -> np.ndarray:
    from sklearn.ensemble import IsolationForest
    T, S, _ = fz.shape
    z = np.zeros((T, S))
    for s in range(S):
        m = IsolationForest(n_estimators=200, random_state=0).fit(fz[:baseline_windows, s])
        raw = -m.score_samples(fz[:, s])                   # higher = more anomalous
        ref = -m.score_samples(fz[:baseline_windows, s])
        z[:, s] = np.maximum(0, (raw - np.median(ref)) / (ref.std() + 1e-9))
    return z
