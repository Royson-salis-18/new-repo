# Cross-paper gaps we can solve

Basis: 37 of 65 queue papers read in full (batches 1-13); 28 are unread (no open PDF), including SuanMing, Sage, Nezha, BARO, RCD, MicroRCA, Eadro, DiagFusion. A gap below could be partly closed by an unread paper; each is marked with what could overturn it. Evidence IDs refer to `PROBLEM_EVIDENCE.md`.

## Gap 1 (strongest): nobody evaluates propagation-aware RCA on cases where propagation matters
- Pham et al. (A12, A13): most causal-graph RCA is near random on 4 benchmarks; failure-time sensitivity.
- Fang et al. (A44, A45): a rule-based alert counter matches or beats SOTA on public benchmarks; 68% of cases have symptoms only in the injected service; 99% lack some telemetry.
- CIRCA (A42), PetShop (A51), DeepHunt (A9, A10): the winning baseline is NSigma, ranked correlation or reconstruction error.
- Methods papers (CausalRCA, MicroHECL, AURORA) report gains over weak or self-implemented baselines on one system.
- **Gap:** no benchmark or protocol isolates cases where the root cause is quiet and a downstream service is loud, with SimpleRCA/NSigma/BARO baselines, confidence intervals, normal-window false alarms and failure-time error.
- **Solvable:** stratify cases by Fang's Type I/II/III, report each stratum, add the baselines. This is the cheapest and most defensible contribution.
- Could be overturned by: BARO and RCAEval full papers (unread).

## Gap 2: label-free RCA and early warning are separate worlds; nobody has a label-free, calibrated cascade-risk score on real telemetry
- Label-free RCA exists (CIRCA, DeepHunt, BARO-type) but outputs a ranking, not a risk of spread.
- Early warning exists but is supervised (Seer, DéjàVu-style), simulation-only (Unyi), metrics-forecast without failure labels (STMformer), proprietary (Li 2026), or unread (SuanMing).
- Calibration (ECE, Brier) is not reported for any risk output in the read papers (AURORA's ECE claim sits in an inconsistent paper).
- **Gap:** a label-free, trace-based cascade-risk score evaluated against real injected cascades, with calibration and a constant/persistence baseline.
- **Solvable:** this is our Task B; the missing piece is real injected multi-service cascades as ground truth.
- Could be overturned by: SuanMing, AID follow-ups, Sage (unread).

## Gap 3: propagation channels are modelled as call edges only, and channel weights are never learned without labels
- DéjàVu (A47): deployment edges help, supervised. STMformer: same-host attention helps, one run. Xie et al. (A29, A30): group relations help, small. Soldani survey (A53): call-only graphs miss co-hosted services. MicroHECL: direction depends on anomaly type (traffic downstream, latency upstream).
- **Gap:** no label-free method learns separate weights for call, co-location and load-balancing channels, nor respects direction by anomaly type, nor tests on shared-host faults.
- **Solvable:** add channels and direction as ablations; the test needs faults on shared hosts, which our SSH/EC2 setup can produce (do not run experiments without the user's go-ahead).
- Could be overturned by: Xie et al. follow-ups; Sage.

## Gap 4: the value of propagation modelling is never measured against the loudness of the symptom
- DeepHunt: propagation weights are small, no ablation (batch 1). CausalRCA: +6.7% and +9.4% relative Avg@5, own-tuned. DéjàVu: ablation helps, supervised.
- **Gap:** an ablation that holds symptom loudness fixed (same detector, with and without propagation) across fault types.
- **Solvable:** same harness as Gap 1; one table.

## Gap 5: explanations are untested for faithfulness
- LLM RCA (AURORA, MicroRCA-Agent, RCAgent, RCACopilot) is judged by LLM scores, human helpfulness 2.92 of 5 (A48), or hallucinated evidence (A15). Non-LLM methods give graphs or rankings without any faithfulness check.
- **Gap:** no paper measures whether an explanation cites evidence present in the telemetry or whether it changes operator decisions.
- **Solvable (small):** verifiable explanation templates with an evidence-match check (as RCAgent's fuzzy-match filter). Needs a human study to claim operator benefit.

## What I would build around
One paper: **a label-free, propagation-aware RCA and cascade-risk method, evaluated on a stratified, propagation-hard benchmark with strong simple baselines and calibration.** That combines Gaps 1, 2 and 4 (core) and Gap 3 (extension); Gap 5 is optional.

## Claims we must not make
- "Unlabeled RCA is new", "early warning is new", "cascade prediction is unexplored", "propagation modelling improves localization" (without the strata and baselines above).

## Confidence
- High: Gap 1 (several independent papers converge).
- Medium: Gaps 2-3 (depend on unread papers).
- Low-medium: Gap 5 (inference from LLM papers; non-LLM faithfulness literature not surveyed).
