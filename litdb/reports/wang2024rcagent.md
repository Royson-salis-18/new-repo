# Report: Wang et al. (2024), RCAgent (CIKM '24)

Key `wang2024rcagent`. Note: `litdb/papers/wang2024rcagent.md`. Coverage: full text of arXiv v3 read; figures not inspected.

## (a) Bibliographic block
Zefan Wang, Zichuan Liu, Yingying Zhang, Aoxiao Zhong, Jihong Wang, Fengbin Yin, Lunting Fan, Lingfei Wu, Qingsong Wen. CIKM '24, DOI 10.1145/3627673.3680016; arXiv 2310.16340v3. Peer reviewed. Scopus: unverified. SJR unknown.

## (b) Plain-language summary
A locally hosted language model is given tools to read logs, code and past cases and then writes the root cause, fix, evidence and responsible team for failed Flink jobs at Alibaba.

## (c) Problem and motivation
GPT-based RCA raises privacy issues and workflow-based LLM RCA lacks autonomy (pp.1-2).

## (d) Method
ReAct-style controller plus observation snapshot keys, code and log expert agents, JsonRegen, error handling, trajectory-level self-consistency (pp.2-4).

## (e) Datasets, protocol
161 balanced jobs from about 5,000 non-trivial (15,616 anomalous) Flink jobs; labels from rule outputs summarized by an LLM and proofread by SREs; judge GPT-4; online OoD jobs with SRE ratings (pp.5-7).

## (f) Results (copied)
Root cause METEOR 15.15 vs ReAct 6.44, G-Correctness 5.22 vs 3.06 (Table 1 p.5); solution G-Helpfulness 5.48 vs 3.41 (Table 2); pass rate 99.38% vs 86.33%, invalid rate 7.93% vs 22.82% (Table 4 p.6); online responsibility precision 80.74% (RCAgent), 82.06% (TSC) vs 77.85% (fine-tuned T5); human helpfulness 2.47 / 2.92 vs 1.36 (Table 5 p.7).

## (g) Limitations and stern critique
Flink jobs, not microservices; text metrics and a GPT-4 judge; small offline set; reference answers LLM-written from rules; weak ReAct baseline; proprietary data, system and code; moderate human helpfulness (2.92 of 5).

## (h) Reproducibility
Not reproducible.

## (i) Head-to-head with our work
Different task (log text RCA). Reusable idea: require quoted evidence to match the input.

## (j) Does it change our problem? Could a reviewer say it exists?
No. "LLM agents for RCA" exists; our contribution is not an LLM agent.

## (k) Sentences
Safe: "Tool-augmented LLM agents have been deployed for cloud job-failure RCA with self-consistency and evidence filtering [RCAgent]." Must NOT write: its scores as microservice localization accuracy.

## (l) Things to verify
Online set size; CIKM vs arXiv differences.
