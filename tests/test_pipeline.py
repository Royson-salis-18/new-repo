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
    assert again.services == tel.services and np.allclose(again.X, tel.X, equal_nan=True)


def test_missing_config_values_detected():
    gaps = config.missing(CFG)
    assert "sources.jaeger.url" in gaps and "system.name" in gaps


def test_no_process_execution_and_ssh_is_confined_and_allowlisted():
    """No local shell/process execution anywhere. Remote access exists only in sources/ssh.py, through a
    single execution point that is only ever called with allowlisted, read-only commands."""
    import pathlib, re
    proc = re.compile(r"\b(subprocess|os\.system|os\.popen|Popen|pexpect)\b|shell\s*=\s*True")
    # third-party SSH libraries only (our own `from .sources import ssh` is the allowed module itself)
    ssh_libs = re.compile(r"\b(paramiko|asyncssh|fabric)\b|^\s*import\s+ssh2?\b", re.M)
    for f in pathlib.Path("rcalab").rglob("*.py"):
        text = f.read_text(encoding="utf-8")
        assert not proc.search(text), f"{f}: process execution is forbidden"
        if f.as_posix() != "rcalab/sources/ssh.py":
            assert not ssh_libs.search(text), f"{f}: SSH is only allowed in rcalab/sources/ssh.py"

    src = pathlib.Path("rcalab/sources/ssh.py").read_text(encoding="utf-8")
    assert src.count(".exec_command(") == 1, "exactly one remote execution point"
    calls = re.findall(r"self\._run\(([^)]*)\)", src)
    ok = ('ALLOWED["stats"]', 'ALLOWED["containers"]', "_LOG_ERRORS % int(since_s", 'f"cat {path}"')
    assert calls and all(any(c.strip().startswith(a) for a in ok) for c in calls), calls
    assert "_PATH_RE.match(path)" in src                      # file reads are path-validated


def test_calibrated_detector_ignores_drops_and_unjudgeable_windows():
    """Healthy synthetic data with a service that only appears late and one-sided dips must not raise alarms."""
    import numpy as np
    from rcalab.detector import detect
    tel, truth = synthetic.make("cart-db", seed=3)
    X = tel.X.copy()
    j = tel.index("payment")
    X[:, j, tel.features.index("latency_p95")] *= np.where(np.arange(len(tel.times)) % 7 == 0, 0.3, 1.0)   # dips are not faults
    X[:60, tel.index("shipping"), :] = np.nan                                                             # no baseline yet
    tel2 = type(tel)(tel.times, tel.services, X, tel.features, tel.edges)
    det = detect(tel2, 40, 8.0, persistence=3, kind="calibrated")
    assert not det.flags[:truth["onset"]].any()
    assert det.flags[truth["onset"] + 3:, tel2.index(truth["service"])].any()          # the real fault is still caught


def test_edge_learner_learns_shielded_edges_across_incidents():
    import numpy as np
    from rcalab.cascade import EdgeLearner
    from rcalab.telemetry import Telemetry
    services = ["a", "b", "c"]
    tel = Telemetry(np.arange(60.0), services, np.zeros((60, 3, len(__import__('rcalab.telemetry', fromlist=['FEATURES']).FEATURES))), edges=[("a", "c"), ("b", "c")])   # a and b both call c
    learner = EdgeLearner(max_lag=1)
    for k in range(10):
        flags = np.zeros((60, 3), bool)
        flags[10 + k, 2] = True            # c fails
        flags[10 + k + 1, 0] = True        # a (caller) always follows
        learner.update(tel, flags)         # b never does
    p = learner.probs(tel.edges)
    assert p[("c", "a")] > 0.7 > 0.3 > p[("c", "b")]
