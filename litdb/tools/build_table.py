"""Rebuild the survey table and comparison matrix from the notes' front matter.

    python litdb/tools/build_table.py
Writes litdb/papers.csv, litdb/SURVEY_TABLE.md, litdb/COMPARISON_MATRIX.md, litdb/QUEUE.md
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

import yaml

DB = Path(__file__).resolve().parent.parent
rows = []
for f in sorted((DB / "papers").glob("*.md")):
    m = re.match(r"^---\n(.*?)\n---\n", f.read_text(encoding="utf-8"), re.S)
    if not m:
        continue
    try:
        d = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"[skip] {f.name}: bad front matter ({e})")
        continue
    d["file"] = f.name
    rows.append(d)

COLS = ["key", "year", "title", "venue", "doc_type", "doi", "issn", "scopus_indexing", "sjr_quartile", "peer_reviewed", "read_status", "task", "supervision",
        "online_or_streaming", "telemetry", "propagation_modeling", "forecasts_future_failures", "llm_used", "systems_evaluated", "datasets", "dataset_open", "code_open",
        "baselines_compared", "metrics", "headline_result", "evidence_quality", "relevance_to_us", "overlap_with_us", "threat_level_for_novelty", "batch", "cited_by_crossref"]
rows.sort(key=lambda d: (str(d.get("read_status")) != "reviewed", -int(d.get("year") or 0)))
with open(DB / "papers.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)

cell = lambda v, n=60: (str(v) if v not in (None, "") else "-").replace("|", "/").replace("\n", " ")[:n]
with open(DB / "SURVEY_TABLE.md", "w", encoding="utf-8") as fh:
    fh.write(f"# Literature survey table ({len(rows)} papers)\n\nGenerated from `litdb/papers/*.md`. `read_status`: extracted < read-in-full < reviewed. "
             "Scopus status is only as good as the list in `litdb/reference/`.\n\n")
    fh.write("| Key | Year | Title | Venue | Scopus | SJR | Status | Task | Supervision | Open data/code | Evidence | Threat |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    for d in rows:
        fh.write(f"| {cell(d.get('key'), 24)} | {cell(d.get('year'))} | {cell(d.get('title'), 70)} | {cell(d.get('venue'), 34)} | {cell(d.get('scopus_indexing'), 22)} | "
                 f"{cell(d.get('sjr_quartile'))} | {cell(d.get('read_status'))} | {cell(d.get('task'), 20)} | {cell(d.get('supervision'), 14)} | "
                 f"{cell(d.get('dataset_open'), 6)}/{cell(d.get('code_open'), 6)} | {cell(d.get('evidence_quality'))} | {cell(d.get('threat_level_for_novelty'))} |\n")

with open(DB / "COMPARISON_MATRIX.md", "w", encoding="utf-8") as fh:
    fh.write("# Comparison with our work (reviewed papers only)\n\n| Key | Supervision | Online | Telemetry | Propagation | Forecasts failures | LLM | Datasets (open?) | Result | Overlap | Threat |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
    for d in rows:
        if d.get("read_status") == "reviewed":
            fh.write(f"| {cell(d.get('key'), 22)} | {cell(d.get('supervision'), 14)} | {cell(d.get('online_or_streaming'), 8)} | {cell(d.get('telemetry'), 22)} | {cell(d.get('propagation_modeling'), 24)} | "
                     f"{cell(d.get('forecasts_future_failures'), 6)} | {cell(d.get('llm_used'), 8)} | {cell(d.get('datasets'), 24)} ({cell(d.get('dataset_open'), 5)}) | {cell(d.get('headline_result'), 50)} | "
                     f"{cell(d.get('overlap_with_us'), 8)} | {cell(d.get('threat_level_for_novelty'), 8)} |\n")

todo = [d for d in rows if d.get("read_status") != "reviewed"]
with open(DB / "QUEUE.md", "w", encoding="utf-8") as fh:
    fh.write(f"# Reading queue ({len(todo)} not yet reviewed, {len(rows) - len(todo)} reviewed)\n\n")
    for d in todo:
        fh.write(f"- [{d.get('read_status')}] {d.get('key')} ({d.get('year')}): {cell(d.get('title'), 90)}\n")
print(f"{len(rows)} papers; {len(rows) - len(todo)} reviewed; wrote papers.csv, SURVEY_TABLE.md, COMPARISON_MATRIX.md, QUEUE.md")
