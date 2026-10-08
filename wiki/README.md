# Wiki

One place for all documentation of **microservice-mapper** (the product) and **rca-lab** (the research harness).

| File | Use it to |
|---|---|
| [INDEX.md](INDEX.md) | browse by topic |
| [TIMELINE.md](TIMELINE.md) | see what was written / done when, plus the commit history |
| [TAGS.md](TAGS.md) | find pages by what they talk about (RCA, cascade, SSH, benchmarks, limitations ...) |
| [CATALOG.csv](CATALOG.csv) | filter everything in a spreadsheet |
| `pages/` | copies of every document |

**The copies in `pages/` are refreshed, not edited.** Edit the original (shown in `CATALOG.csv` as `source_path`), then rebuild:

```
.venv\Scripts\python tools\build_wiki.py
```

Last build: 2026-10-08 16:03; 267 pages.
