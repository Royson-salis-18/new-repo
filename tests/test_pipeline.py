import numpy as np

from rcalab import config, store, synthetic
from rcalab.cascade import cascade_risk, edge_probabilities, path_probabilities
from rcalab.detector import detect
from rcalab.explain import explain
from rcalab.rca import rank

CFG = config.load("config.example.yaml")


def _run(root, seed=0, method="full"):
    tel, truth = synthetic.make(root, seed=seed)
    det = detect(tel, truth["baseline"], 3.5)
    w = (truth["baseline"], len(tel.times))
    return tel, det, w, rank(tel, det, w, 4, 3, method)


def test_no_false_alarms_in_baseline():
    tel, det, *_ = _run("cart-db")
    assert not det.flags[:40].any()


def test_root_cause_is_top1_for_leaf_faults():
    for root in ["cart-db", "catalogue-db", "orders-db", "queue", "payment"]:
        _, _, _, res = _run(root)
        assert res.ranking[0][0] == root, (root, res.ranking[:3])


def test_full_beats_anomaly_only_on_average():
    def mrr(method):
        rr = []
        for seed in range(8):
            root = ["cart-db", "queue", "orders-db", "catalogue-db"][seed % 4]
            _, _, _, res = _run(root, seed, method)
            names = [s for s, _ in res.ranking]
            rr.append(1 / (names.index(root) + 1) if root in names else 0)
        return np.mean(rr)
    assert mrr("full") >= mrr("anomaly_only")


def test_cascade_risk_flows_callee_to_caller():
    tel, det, w, res = _run("cart-db")
    P = path_probabilities(tel.services, edge_probabilities(tel, det.flags))
    i, j = tel.index("cart-db"), tel.index("frontend")
    assert P[i, j] > P[j, i]
    a = np.zeros(len(tel.services)); a[i] = 1.0
    assert cascade_risk(a, P)[tel.index("cart")] > 0.3


def test_explanation_names_root_cause_and_roundtrip(tmp_path):
    tel, det, w, res = _run("queue")
    assert "queue" in explain(tel, det, res, w).splitlines()[0]
    store.save(tmp_path / "t.npz", tel)
    again = store.load(tmp_path / "t.npz")
    assert again.services == tel.services and np.allclose(again.X, tel.X)


def test_missing_config_values_detected():
    gaps = config.missing(CFG)
    assert "sources.prometheus.url" in gaps and "system.name" in gaps
