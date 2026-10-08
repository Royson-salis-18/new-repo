# What we are, where we help, and why it matters (scope and value)

*Written 2026-10-08. Real-world numbers come from the sources listed in section 9, each with its caveat. Our own numbers come from `docs/WHAT_IS_WRONG.md`. Where something is our judgement and not a measurement, it says "judgement".*

---

## 1. What we are, in one paragraph

We are a **first responder for the first minutes of an incident** in a containerised microservice application. With **no labels, no training and no history**, we watch every service's metrics, logs and traces, say **"something is wrong"** with a known false-alarm rate, and point at **which service to look at first** (root-cause *localisation*). We also list which healthy services are **likely to be dragged in next** (cascade risk).

We are **not**:
* a fixer: we do not restart, roll back or scale anything;
* a "why" engine: we name a *service*, not the bug, config line or deploy that broke it;
* a fortune teller: we see trouble only after it shows up in the telemetry, not before.

---

## 2. What you need to know first (the DevOps/SRE vocabulary)

| Term | Meaning | Why it matters for us |
|---|---|---|
| **Incident lifecycle** | detect -> triage (who owns it) -> diagnose/localise (where is it) -> mitigate (stop the pain) -> postmortem (learn) | we work on **detect** and **localise** only |
| **MTTD / MTTR** | mean time to detect / to resolve (or restore) | our value is cutting the "where is it" part of MTTR |
| **SLI / SLO / error budget** | a measured indicator (e.g. p95 latency), the target for it, and how much failure is allowed | engineers act on SLO breaches; our false-alarm budget is the same idea applied to alerts |
| **Four golden signals** | latency, traffic, errors, saturation (Google SRE book) | these are exactly the features we score |
| **Observability: metrics, logs, traces** | numbers over time; text events; the path of each request through services | traces give the call graph and *self time*; without them we see much less |
| **Alert fatigue / alert storm** | too many alerts, many false or duplicated, so engineers ignore or drown in them | the reason a stated false-alarm rate matters |
| **Root cause vs contributing factors** | modern SRE practice prefers "contributing factors"; "root cause" is contested | we should say "faulty service localisation", not "root cause" in the strict sense |
| **Victim vs source** | a service that looks broken because it calls a broken one, vs the broken one | our main technical problem (`WHAT_IS_WRONG.md` P1, P3) |
| **Cascading failure** | a failure that spreads because one broken part makes others more likely to break; the most common cause is **overload** (Google SRE book, ch. 22) | what "cascade risk" tries to warn about |
| **Retry storm / metastable failure** | the system stays broken after the trigger is gone because retries and backlogs keep it overloaded | the cascade type that lasts hours, and our motivation for early warning |
| **Blast radius** | how many users or services one failure affects | what cascade risk estimates |
| **Gray / partial failure** | a service that is slow or half-working rather than dead | the hard case for every detector, ours included (slow and hang faults) |

---

## 3. How bad the problem is in the real world (evidence, with caveats)

| Fact | Source | Caveat |
|---|---|---|
| **54%** of operators say their most recent serious outage cost more than **$100,000**; about **1 in 5** say more than **$1 million** (Uptime 2025 report, 2024 survey). The newer survey gives **57%** | Uptime Institute, Annual Outage Analysis 2025 | survey of respondents' most recent major outage, not all outages; Uptime itself warns that outage data are uncertain |
| Of 597 public outages of 32 popular Internet services (2009-2015), a large share were rooted in the **failure-recovery chain** (detection, failover, backups), not in a single bug. A secondary summary lists cross-service dependencies at about 8% and traffic load at about 9% of causes | Gunawi et al., SoCC 2016 (and a secondary summary) | built from news and public postmortems; percentages cover only outages with a known cause |
| At AWS, **at least 4 of 15 major outages in a decade** were metastable (self-sustaining overload) failures; retries were the most common sustaining effect (over 50% of cases); such outages most often last **4-10 hours** | Huang et al., "Metastable Failures in the Wild", OSDI 2022 (paper and slides) | public incident reports only |
| **AWS us-east-1, 7 Dec 2021:** an automated capacity-scaling action caused a connection surge that overwhelmed internal network devices; console, Route 53, API Gateway, EC2 and others degraded within minutes, and AWS's **own monitoring and incident tooling was affected**, delaying updates. Netflix, Slack, Disney+, Venmo and others were hit | trade-press summaries of AWS status updates | AWS's own post-event summary is the primary source; not re-read here |
| **Roblox, 28-31 Oct 2021: 73-hour outage.** Causes were contention in a new Consul streaming feature plus a BoltDB performance problem; one Consul cluster served many workloads. **Diagnosis took about two days**: early theories (bad hardware, load) were wrong, and the in-house telemetry itself depended on Consul, so engineers were "flying blind" | Roblox's own postmortem, Jan 2022 | one company, one incident |
| Overload is **the most common cause of cascading failures**: one replica fails, its load moves to the others, and they fail in turn | Google, *Site Reliability Engineering*, ch. 22 | practitioner guidance, not a statistic |
| Microsoft studied hundreds of high-severity incidents of a cloud service with hundreds of millions of users (a review says 152 Microsoft Teams incidents) and concluded that many lasted long because detection and mitigation practices were too slow; it recommends **automation for diagnosis and root-causing** | Ghosh et al., SoCC 2022 (Best Paper) | exact time figures not retrieved here |
| In 20 Microsoft online services, **4.11% to 91.58%** of incident reports were reassigned at least once (wrong team first) | Chen et al., ICSE-SEIP 2019 (incident triage) | reassignment is triage, closely related to "which service is it" |
| Engineers spend on average **36.3% of mitigation time** looking for the right troubleshooting guide (18 Microsoft services) | Jiang et al., ESEC/FSE 2020 industry track | measures guide search, not localisation itself |
| An **alert storm** (many alerts from one failure) makes manual diagnosis slow; summarising it cut the alerts to examine by **more than 98%** at a large bank | Zhao et al., ICSE-SEIP 2020 | one organisation |
| In a large public RCA benchmark study, **84.4% of injected faults produced no user-visible anomaly**, and **68%** of 737 public cases are "easy" (symptoms only in the injected service) | Fang et al. 2025 (read in full, `literature-review/`) | benchmark data, not production |
| All evaluated RCA methods **invent root causes on normal data**; methods' accuracy collapses when the fault time is off by 60 s (0.81 to 0.03-0.12) | PetShop (CLeaR'24) p.12; Pham et al. (ASE'24) Table 5 | benchmarks |

**What these sources say together.** Outages are expensive. A large part of their duration is spent finding *where* the problem is, often with the wrong team or the wrong theory first, and often with the monitoring itself degraded. Cascades through overload and retries turn short faults into hour-long outages. Alert noise is a real cost. That is the space we work in.

**What they do not say.** None of them shows that a tool like ours shortens real incidents. That would need a field study, which we do not have.

---

## 4. Where our approach is useful (scenarios), how well, and our evidence

| Scenario | Real-world example of the type | Can we detect it? | Can we name the source? | Our evidence |
|---|---|---|---|---|
| **Container crash, OOM kill, restart loop** | a pod dies, callers start failing | yes | **yes**: ranked first, and since 2026-10-08 also without the "container vanished" signal (silence + quiet-inheritance rule, with the call graph) | 1 real crash (DeathStar): rank 1, 0 false flags; bench crash A@1 1.00 |
| **Error burst in one service** (bad deploy, bad config, broken dependency client) | errors start right after a release | often (bench recall 0.4-0.6) | **often** (bench A@1 0.58) | semi-synthetic bench only |
| **Overload cascade / retry storm** | Google SRE ch. 22; metastable failures; AWS 2021 | yes: many services light up | **unclear**: everything is loud at once; common-mode removal may even hide it | not tested |
| **Slow service (latency degradation)** | a slow database query, a GC pause | **rarely** with 15 s trace aggregates (bench slow A@1 0.04) | rarely | bench |
| **Frozen / hung service** (deadlock, `docker pause`) | a service stops answering but stays "up" | **yes**: bench, and live on DeathStar after a fix (silence = no CPU and no traffic) | bench **yes** (A@1 1.00); **live no** (rank 7-8 of 27: the stalled chain above it looks the same; needs traces) | bench + 2 live pauses (88% and 43% user errors) |
| **Shared infrastructure failure** (network, DNS, service discovery, cloud region) | AWS 2021 network devices; Roblox Consul | the symptoms, yes | **no**: the culprit is not one of the services we watch | none (out of scope) |
| **Silent data or logic bugs** (wrong results, no errors) | | no | no | out of scope |
| **Slow resource leak** (memory creeping over hours) | | maybe (memory feature), late | maybe | not tested |
| **Cascade risk ("who is next")** | a failing dependency's callers | n/a | ranks callers of flagged services | equal to the structural rule; unproven (`WHAT_IS_WRONG.md` P10) |

**Where it fits best (judgement):**
* small and medium teams running **10-100 containerised services** (Docker/Kubernetes) without a commercial AIOps product or labelled incident history;
* **new or fast-changing systems**, where training data do not exist yet or go stale after each release (label-free is an advantage here);
* **labs, test benches and staging**, to check resilience changes with a fault ledger;
* as a **pre-filter for on-call**: one ranked suspect list instead of an alert storm, with a promised false-alarm rate.

**Where it does not fit:**
* teams that already have rich labelled history: supervised methods are much stronger there (Chain-of-Event 79.3% top-1 with labels vs 17.1% for a label-free graph, proprietary data);
* infrastructure and cloud-provider failures;
* gray failures (slow, frozen) until the silence signal (P3) and better latency data (P2) exist.

---

## 5. The value argument: the reasons, and whether each holds

| # | Reason the solution is useful | Real-world support | Holds for us today? |
|---|---|---|---|
| R1 | Finding *where* a fault is takes a large share of incident time, often with wrong theories first | Roblox (2 days of diagnosis), Microsoft triage reassignments (4-92%), Ghosh et al. | yes as motivation; **we have not measured time saved** |
| R2 | Alert noise is costly, so a detector must state its false-alarm rate | alert storms (Zhao et al.); PetShop: all methods invent root causes on normal data | **yes**: 0.1 false alarms/h vs 78.7/h for the original approach, measured |
| R3 | Labels and history are often missing (new systems, constant change), so label-free matters | judgement plus the literature split: supervised methods need labelled incidents | yes, by design |
| R4 | Victims are louder than the source, so plain "most abnormal" blames the wrong service | our real crash (victims' error logs about 30x); Fang et al. Type III cases | **partly**: crashes (real, n = 1) and frozen services (bench) now handled; slow services not |
| R5 | Cascades turn short faults into long outages, so early warning has value | SRE book ch. 22; metastable failures (4 of 15 major AWS outages) | **not yet**: our risk score equals the structural rule; slow overload cascades are the only kind with time to warn |
| R6 | Monitoring itself fails during big incidents, so a simple, independent watcher is useful | AWS 2021 (incident tooling affected); Roblox (telemetry depended on Consul) | yes as an argument for the SSH mode (independent of the app's own telemetry), but it **adds load** (`WHAT_IS_WRONG.md` P14) |

**Honest summary:** R2 and R3 are fully backed. R1 and R6 are backed as motivation, but we have not shown the benefit. R4 holds only for crashes. R5 does not hold yet.

---

## 6. Where in an incident we help (the timeline)

```
fault starts -> symptoms appear -> DETECT -> TRIAGE / LOCALISE -> mitigate -> recover -> postmortem
                                   ^^^^^^    ^^^^^^^^^^^^^^^^^
                                   we help here (first minutes)
```

* **Detect:** about 0-30 s after the symptoms for crashes (one real case); errors on the bench average about 20 s; slow and frozen services often never.
* **Localise:** one ranked list. Useful only if the true source is in the top 3 often enough (bench A@3 0.50 overall, 1.00 for crashes, 0.6 for errors).
* **We do not help with:** mitigation (rollback, restart, scaling), the actual bug, or the postmortem.

---

## 7. How to say it in the paper (claims that survive review)

* **Problem statement:** "During an incident, engineers must first find which service is at fault. Public postmortems and incident studies show this step is slow and error-prone (Roblox, Microsoft triage, Ghosh et al.), and that automatic methods invent faults on healthy data (PetShop) or depend on labelled history (Chain-of-Event)."
* **What we offer:** "A label-free detector and localiser that runs on live container telemetry, has a stated false-alarm rate, and is evaluated against a fault ledger, together with an analysis of *which fault types* such methods can and cannot handle."
* **Do not say:** "reduces MTTR", "predicts cascading failures", "outperforms the state of the art", "finds the root cause". None is shown.

---

## 8. What to study to defend this (reading list, in order)

1. Google SRE book: ch. 6 (monitoring, golden signals), ch. 22 (cascading failures), ch. 15 (postmortem culture). Free at sre.google.
2. Huang et al., *Metastable Failures in the Wild*, OSDI 2022 (why cascades last hours).
3. Gunawi et al., *Why Does the Cloud Stop Computing?*, SoCC 2016 (what real outages look like).
4. Ghosh et al., *How to Fight Production Incidents?*, SoCC 2022 (where incident time goes at Microsoft).
5. Roblox *Return to Service* postmortem (a real diagnosis going wrong for two days).
6. Pham et al. ASE'24 and Fang et al. 2025 (why RCA benchmarks flatter methods; in `literature-review/`).
7. Our `literature-review/GAPS.md` (which gaps are really open).

---

## 9. Sources

* Uptime Institute, *Annual Outage Analysis 2025*: https://intelligence.uptimeinstitute.com/resource/annual-outage-analysis-2025 ; press release: https://www.businesswire.com/news/home/20250506733553/en/Uptime-Announces-Annual-Outage-Analysis-Report-2025 ; summary: https://www.datacenterknowledge.com/outages/data-center-outages-decline-for-fourth-straight-year-but-issues-persist
* Gunawi et al., SoCC 2016: https://www.ece.iastate.edu/%7Emai/docs/papers/2016_SoCC_COS.pdf ; secondary summary: https://arxiv.org/pdf/1806.03210
* Huang et al., OSDI 2022: https://www.usenix.org/conference/osdi22/presentation/huang-lexiang ; slides: https://www.usenix.net/sites/default/files/conference/protected-files/osdi22_slides_huang_lexiang.pdf
* AWS us-east-1, Dec 2021 (summaries): https://www.pluralsight.com/resources/blog/cloud/what-happened-with-the-aws-outage , https://thestack.technology/aws-down-december-2021/ , https://www.lightreading.com/cloud/aws-outage-cuts-down-swaths-of-the-internet
* Roblox postmortem: https://about.roblox.com/newsroom/2022/01/roblox-return-to-service-10-28-10-31-2021 ; discussion: https://newsletter.pragmaticengineer.com/p/real-world-3
* Google SRE book ch. 22: https://sre.google/sre-book/addressing-cascading-failures/
* Ghosh et al., SoCC 2022: https://www.microsoft.com/en-us/research/?p=881646 ; review: https://systemsdistributed.substack.com/p/how-to-fight-production-incidents
* Incident triage at Microsoft, ICSE-SEIP 2019: https://www.microsoft.com/en-us/research/uploads/prod/2019/03/incidenttriage_cameraReady.pdf
* Troubleshooting-guide recommendation, ESEC/FSE 2020: https://2020.esec-fse.org/details/esecfse-2020-industry-papers/9/How-to-Mitigate-the-Incident-An-Effective-Troubleshooting-Guide-Recommendation-Techn
* Alert storms, ICSE-SEIP 2020: https://2020.icse-conferences.org/details/icse-2020-Software-Engineering-in-Practice/24/Understanding-and-Handling-Alert-Storm-for-Online-Service-Systems
* Fang et al. 2025, PetShop, Pham et al., Chain-of-Event: see `literature-review/PAPERS.md` (read in full, page references there)
