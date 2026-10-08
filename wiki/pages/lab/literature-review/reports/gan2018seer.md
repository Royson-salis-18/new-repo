# Report: Gan et al. (2018), Seer (arXiv short version)

Key `gan2018seer`. Note: `litdb/papers/` same key. Coverage: full 7-page text read; plots not inspected. This is the short arXiv version, not the ASPLOS 2019 paper.

## (a) Bibliographic block
Yu Gan, Meghna Pancholi, Dailun Cheng, Siyuan Hu, Yuan He, Christina Delimitrou (Cornell). arXiv 1804.09136v1, cs.DC, 24 Apr 2018. Preprint; not Scopus-indexed. SJR unknown.

## (b) Plain-language summary
A neural network watches how many requests are queued at each microservice and warns, before users notice, which microservice is about to cause a latency-target violation; then it adjusts resources.

## (c) Problem and motivation
After-the-fact detection of QoS violations is too late and violations propagate across dependencies (p.1). Argued, no measured rate.

## (d) Method
Per-service queue depth as input (chosen over utilization and latency), 5 hidden layers, outputs one neuron per service; offline training with manual violation labels; TPU inference for scale; hardware counters to find the contended resource (pp.2-5).

## (e) Datasets, protocol
Three own applications (social network, movie streaming, e-commerce from Sockshop); 10-server local cluster and 200-instance GCE; no external baselines; lead time and QoS threshold not stated (pp.3-4).

## (f) Results (copied)
Anticipates QoS violations 91% (GCE) and 93% (local) of the time; names culprit 89% (GCE) and 91% (local) (abstract and p.2). Inference within 2 ms for 60% of detections, up to 14 ms (p.4). Input-metric comparison only in Fig 2a (plot).

## (g) Limitations and stern critique
No external baseline, no lead-time, no false-alarm rate, no counts or intervals; supervised with manual labels; fixed service set (autoscaling breaks the network size); unreleased apps; hardware counters unavailable on public clouds (microbenchmarks as fallback).

## (h) Reproducibility
Not reproducible from this text; apps and code to be released.

## (i) Head-to-head with our work
Prior art for early warning plus culprit naming. Ours: label-free, explicit edges, open code; theirs: live clusters and mitigation.

## (j) Does it change our problem? Could a reviewer say it exists?
Yes: "early warning with culprit identification" exists (supervised). Our claim must be label-free plus explicit propagation plus calibration.

## (k) Sentences
Safe: "Seer anticipates QoS violations and names the culprit microservice from queue-depth traces with a supervised network [Seer]." Must NOT write: its percentages as general accuracy, or that it is label-free.

## (l) Things to verify
The ASPLOS 2019 full paper; prediction lead time; false-alarm rate.
