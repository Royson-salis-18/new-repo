# Report: Xu et al. (2024), STMformer

Key `yifeixu...2024system`. Note: `litdb/papers/` same key. Coverage: full text read (11 pages); Figs 1-4 not inspected.

## (a) Bibliographic block
Yifei Xu, Jingguo Ge, Haina Tang, Shuai Ding, Tong Li, Hui Li (Chinese Academy of Sciences). arXiv 2408.07894v1, cs.NI, 15 Aug 2024; ACM template with placeholder DOI and "Conference'24". Not Scopus-indexed (preprint). SJR unknown.

## (b) Plain-language summary
A transformer that predicts the next stretch of pod metrics (CPU, memory, network) using which pods share a host and which pods currently have TCP connections.

## (c) Problem and motivation
System state forecasting supports AIOps; states depend on neighbours on the same host and on call connections, with delayed cascades (pp.1-2). One example plot (Fig 1b).

## (d) Method
Series decomposition, IMM (same-host attention), SMM (GAT on per-step connection adjacency), TMM (TimesNet block plus PatchCrossAttention with linear-attention approximation), ProbSparse attention (pp.4-6).

## (e) Datasets, protocol
Own Train-Ticket data: 41 services, 7 VMs, about 14,000 samples (64 x 56 pods x 80 features), 5 s sampling, 1-2 hours per condition, six Chaos Mesh faults; split 8:1:1; horizons 16, 32, 64, 128 (pp.6-8).

## (f) Results (copied)
Step 16: MAE 0.01663 (FEDformer 0.01709), MSE 0.002102 (PatchTST 0.002126) (Table 1 p.7). Step 32: MAE 0.01623, MSE 0.002084. Step 64: MAE 0.01644 (PatchTST 0.01899), MSE 0.002040 (PatchTST 0.002053). Step 128: MAE 0.01728 (TimesNet 0.01818), MSE 0.002126 (PatchTST 0.002081, better) (Table 2 p.8). Abstract claims 8.6% MAE and 2.2% MSE reduction. Ablation (Table 3 p.8): removing PCA MAE 0.04434; removing IMM MAE 0.5768 with RMSE 0.1300 (impossible pair).

## (g) Limitations and stern critique
Metric forecasting, not failure prediction; abstract gains do not match the tables (about 2.7% MAE and 1.1% MSE at step 16); impossible MAE/RMSE in the ablation; no persistence baseline; split protocol unstated (leakage risk); one deployment, one run; weak spatio-temporal baselines (STSGT non-convergent); random matrix alpha unexplained; dataset release unstated.

## (h) Reproducibility
Code stated at github.com/xuyifeiiie/STMformer (not checked); dataset not stated as public.

## (i) Head-to-head with our work
They use host co-location and dynamic connections as propagation channels for forecasting; we use call edges only. They forecast metrics; we score cascade risk and rank root causes.

## (j) Does it change our problem? Could a reviewer say it exists?
It supports listing co-location as a limitation of our call-edge model. Not prior art for cascade-risk scoring or RCA.

## (k) Sentences
Safe: "Metric forecasting models that exploit host co-location and TCP-connection graphs exist [STMformer]." Must NOT write: its 8.6% / 2.2% gains; that it predicts failures or cascades.

## (l) Things to verify
Split protocol; dataset availability; published version; Table 3 numbers.
