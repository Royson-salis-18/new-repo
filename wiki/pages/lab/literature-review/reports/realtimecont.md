# Report: Ortiz et al. (2019), Real-Time Context-Aware Microservice Architecture for Predictive Analytics

Key `realtimecont`. Note: `litdb/papers/realtimecont.md`. Page numbers are PDF pages.
Coverage: body text read to the conclusion and appendix; references read to [41] and skimmed after; figures and appendix tables not inspected.

## (a) Bibliographic block
Guadalupe Ortiz, José Antonio Caravaca, Alfonso García-de-Prado, Juan Boubeta-Puig (University of Cádiz), Francisco Chávez de la O (University of Extremadura). IEEE Access 7, pp.183177-183194, published 18 December 2019 (received 18 Nov 2019, accepted 13 Dec 2019). CC BY 4.0. ISSN 2169-3536. DOI as printed in the PDF header: 10.1109/ACCESS.2019.2960516 (printed with spaces; not verified in Crossref). Scopus: venue indexed (preview 2026-10-07; CiteScore 2025 = 9.3, 91st percentile, 31/351 General Engineering; SJR 2025 = 0.884; quartile unknown, no list supplied). Peer reviewed: yes (a short review time typical of IEEE Access).

## (b) Plain-language summary
An IoT software architecture that forecasts air pollutant levels and sends smartphone alerts before dangerous levels occur. The architecture is built from microservices and uses ARIMA forecasting on a Spark cluster plus a complex-event engine. It has nothing to do with finding the root cause of microservice failures.

## (c) Problem and motivation
Context-aware predictive decision-making for IoT data (pp.1-2). Motivation is generic (IoT growth, disaster prevention). Not relevant.

## (d) Method
Message broker, domain and context services, ARIMA prediction module on Hadoop YARN and Spark Streaming, ESB, Esper CEP engine, context broker, mobile app. ARIMA per pollutant with history windows of 1 to 14 days; stationarity tested with the Augmented Dickey-Fuller test.

## (e) Datasets, protocol, leakage
118,370 air-quality records (2014-01-01 to 2016-03-31) with 10-fold cross-validation and a 70/30 split (p.10); two months of Mazagon data (June and July 2019) for level hit rates (pp.10-11, 16); synthetic IoT messages for throughput tests (pp.11-12). Random cross-validation on time series is not a valid forecasting protocol; "erroneous predictions due to anomalies" were discarded in the two-month check (p.16).

## (f) Results (copied)
Processing time under 0.06 s per message and 0.01 s per event up to 300,000 messages, for the prediction module and the whole architecture (pp.12-13); alert-level hit rate 100% for CO and NO2 and 48.64% to 93.81% for the other four pollutants (p.11 and appendix). No baselines or tests.

## (g) Limitations and stern critique
Out of scope for RCA; random cross-validation on time series; discarding anomalous predictions; no baseline forecasters (stated as not the aim); performance on synthetic messages. The earlier REVIEW_REPORT listed this among microservice RCA papers read; it should not be.

## (h) Reproducibility
Dataset DOI http://dx.doi.org/10.17632/4y586x9bhv.1 (Mendeley Data; not opened). No code.

## (i) Head-to-head with our work
No overlap. Only shared word: "predictive" and "microservice".

## (j) Does it change our problem? Could a reviewer say it exists?
No.

## (k) Sentences
Safe (if at all): "Microservice architectures have also been used to build IoT streaming pipelines that forecast environmental measurements (Ortiz et al. 2019)." Must NOT write: that it predicts microservice failures or provides RCA evidence.

## (l) Things to verify
DOI spelling in Crossref; appendix tables.
