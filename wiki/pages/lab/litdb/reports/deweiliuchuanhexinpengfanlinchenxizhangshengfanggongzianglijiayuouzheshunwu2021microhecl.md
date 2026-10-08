# Report: Liu et al. (2021), MicroHECL

Key `deweiliu...2021microhecl`. Note: `litdb/papers/` same key. Coverage: full text read; figures not inspected.

## (a) Bibliographic block
Dewei Liu, Chuan He, Xin Peng (Fudan), Fan Lin, Shengfang Gong, Ziang Li, Jiayu Ou, Zheshun Wu (Alibaba), Chenxi Zhang. arXiv 2103.01782v1, 1 Mar 2021; published as ICSE-SEIP 2021 per CIRCA's reference list (unverified). Preprint; not Scopus-indexed. SJR unknown.

## (b) Plain-language summary
When an order-success metric drops, walk the service call graph from the affected service along calls that look abnormal, in the direction each kind of anomaly travels, and rank the ends of those chains by how closely their metrics track the business metric.

## (c) Problem and motivation
Alibaba e-commerce (over 30,000 services) needs root cause localization in minutes (pp.1-2).

## (d) Method
Dynamic call graph from the last 30 minutes; anomaly detectors per type (OC-SVM for response time, random forest for errors, 3-sigma plus correlation for traffic); propagation direction by type (Table I p.4); Pearson-correlation pruning at 0.7; ranking by correlation (pp.3-7).

## (e) Datasets, protocol
75 issues from 28 Alibaba subsystems (Feb-Jun 2020), engineer-annotated; baselines MonitorRank and Microscope reimplemented by the authors (p.7).

## (f) Results (copied)
HR@1/3/5/MRR 0.48/0.67/0.72/0.58 vs MonitorRank 0.32/0.40/0.43/0.37 and Microscope 0.35/0.49/0.59/0.44 (Table IV p.7); time 22.3% less than Microscope and 31.7% less than MonitorRank (p.8); pruning keeps HR@3 0.67 while time falls 75 s to 46 s (p.8); deployment HR@3 68%, 76 s average, over 600 issues (p.9). Detector F1 0.91 (response time, 600 balanced test cases) and 0.95 (errors, 400 cases) (Tables II-III).

## (g) Limitations and stern critique
Supervised detectors (100,000 + 1,000 labelled cases); 75 private cases, no intervals; self-implemented baselines; no simple baseline; 30-to-5-minute claim without protocol; single-company data; window limits (pp.8-9).

## (h) Reproducibility
No code or data.

## (i) Head-to-head with our work
Call-graph family. We are label-free and open; they have direction-by-anomaly-type logic and deployment evidence.

## (j) Does it change our problem? Could a reviewer say it exists?
No. Borrow the observation that traffic anomalies propagate upstream to downstream and latency/error anomalies the other way.

## (k) Sentences
Safe: "MicroHECL traverses a dynamic call graph along anomalous calls with type-specific propagation directions and correlation pruning [MicroHECL]." Must NOT write: its accuracy figures as reproducible; that it is label-free.

## (l) Things to verify
Published version; availability of any code.
