"""Build the unified wiki: copy every markdown doc from both repos into wiki/pages/ and generate three indexes.

    python tools/build_wiki.py

Sources (everything tracked or untracked-but-not-ignored, so it follows the repos automatically):
    microservice-mapper  (the product)         C:/Users/MITE/Downloads/microservice-mapper
    rca-lab              (the research harness) this folder
Outputs in wiki/:
    README.md     how to use / rebuild
    INDEX.md      by TOPIC (section), each page with title, summary, dates, size, tags
    TIMELINE.md   by TIME: pages by creation date, recent updates, and the commit history of both repos
    TAGS.md       by CONTENT: tag -> pages that talk about it (derived from the text, not from file names)
    CATALOG.csv   everything in one table
    pages/        copies of the docs (originals untouched; re-run to refresh)
Dates come from git history; files git does not know fall back to the file's modified time. This is a development tool (it calls git).
"""
from __future__ import annotations

import csv
import html
import re
import shutil
import subprocess
from urllib.parse import quote
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MAPPER = Path(r"C:\Users\MITE\Downloads\microservice-mapper")
OUT = HERE / "wiki"
PAGES = OUT / "pages"

REPOS = [("mapper", MAPPER), ("lab", HERE)]
EXCLUDE = re.compile(r"(^|/)(node_modules|\.venv|litdb/texts|litdb/pdfs|\.git|dist|build)(/|$)", re.I)

TAGS = {
    "root cause analysis (RCA)": r"root[- ]cause|\bRCA\b",
    "cascading failure / propagation": r"cascad|propagat|blast radius",
    "anomaly detection": r"anomal|isolation forest|z-score|robust-z|false alarm",
    "traces / Jaeger / OpenTelemetry": r"\btrace|jaeger|opentelemetry|\botel\b|span",
    "metrics / Prometheus": r"prometheus|promql|cadvisor|docker stats|\bmetrics?\b",
    "logs": r"\blogs?\b|loki|log parsing|drain",
    "SSH / EC2 / Docker": r"\bssh\b|\bec2\b|docker|compose",
    "dashboard / UI": r"dashboard|frontend|react|canvas|websocket|\bUI\b",
    "machine learning / GNN": r"\bGNN\b|graph neural|autoencoder|isolation forest|machine learning|\bML\b",
    "LLM / agents": r"\bLLM\b|language model|agentic|\bagent\b",
    "benchmark / dataset": r"benchmark|dataset|RCAEval|train.?ticket|sock shop|online boutique|death ?star",
    "evaluation / statistics": r"wilcoxon|confidence interval|holm|cliff|AUROC|A@1|\bMRR\b|ablation",
    "literature / papers": r"\bpaper\b|scopus|literature|citation|survey",
    "limitations / threats": r"limitation|threat|caveat|not (yet )?(proven|supported)|unverified",
    "architecture / data flow": r"architecture|data flow|pipeline|component",
    "configuration / API": r"\bconfig|\bAPI\b|endpoint|\.env|settings",
    "troubleshooting": r"troubleshoot|known issue|failed|timeout|error",
}


def git(repo: Path, *args: str) -> str:
    try:
        return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""


def section_of(repo: str, rel: str) -> tuple[str, int]:
    r = rel.lower()
    if repo == "mapper":
        if r.startswith("wiki/"):
            return "Microservice Mapper: wiki (architecture, data, operations)", 20
        if r in ("wiki.md", "readme.md"):
            return "Microservice Mapper: overview", 10
        return "Microservice Mapper: other components", 25
    if r in ("readme.md", "research.md"):
        return "rca-lab: overview and research protocol", 30
    if r.startswith("docs/"):
        return "Reports and findings", 40
    if r.startswith("experiments/"):
        return "Experiments", 45
    if r.startswith("litdb/batches/"):
        return "Literature: batch comparisons", 54
    if r.startswith("litdb/reports/"):
        return "Literature: per-paper reports", 55
    if r.startswith("litdb/papers/"):
        return "Literature: per-paper structured notes", 56
    if r.startswith("litdb/reference/"):
        return "Literature: venue / Scopus checks", 57
    if r.startswith("litdb/"):
        return "Literature: database, survey table, evidence ledger", 50
    return "rca-lab: other", 60


def clean_md(s: str) -> str:
    s = re.sub(r"^---\n.*?\n---\n", "", s, flags=re.S)          # YAML front matter
    return s


def title_summary(text: str, path: Path) -> tuple[str, str, list[str]]:
    if path.suffix.lower() == ".html":
        t = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
        body = re.sub(r"<(script|style).*?</\1>", " ", text, flags=re.S | re.I)
        plain = html.unescape(re.sub(r"<[^>]+>", " ", body))
        plain = re.sub(r"\s+", " ", plain).strip()
        return (t.group(1).strip() if t else path.stem), plain[:240], []
    body = clean_md(text)
    h1 = re.search(r"^#\s+(.+)$", body, re.M)
    title = h1.group(1).strip() if h1 else path.stem
    heads = [m.group(1).strip() for m in re.finditer(r"^##\s+(.+)$", body, re.M)][:8]
    summary = ""
    in_code = False
    for line in body.splitlines():
        st = line.strip()
        if st.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not st or st.startswith(("#", "|", ">", "---", "<", "![", "- [", "```")):
            continue
        summary = re.sub(r"[*_`]|\[([^\]]+)\]\([^)]*\)", r"\1", st)
        if len(summary) > 40:
            break
    return title, summary[:240], heads


def tags_for(text: str, title: str) -> list[str]:
    out = []
    for tag, rx in TAGS.items():
        n = len(re.findall(rx, text, re.I))
        if n >= 4 or re.search(rx, title, re.I):
            out.append((n, tag))
    return [t for _, t in sorted(out, reverse=True)][:6]


def dates(repo: Path, rel: str, full: Path) -> tuple[datetime, datetime, str]:
    log = git(repo, "log", "--follow", "--format=%aI|%s", "--", rel).strip().splitlines()
    if log:
        last = datetime.fromisoformat(log[0].split("|", 1)[0])
        first = datetime.fromisoformat(log[-1].split("|", 1)[0])
        return first, last, log[-1].split("|", 1)[1]
    m = datetime.fromtimestamp(full.stat().st_mtime).astimezone()
    return m, m, "(not committed yet; file modified time)"


def main() -> None:
    if OUT.exists():
        shutil.rmtree(PAGES, ignore_errors=True)
    PAGES.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, repo in REPOS:
        if not repo.exists():
            continue
        files = git(repo, "ls-files", "-co", "--exclude-standard", "-z").split("\0")
        for rel in files:
            if not rel or EXCLUDE.search(rel) or not rel.lower().endswith((".md", ".html")):
                continue
            if name == "lab" and rel.startswith("wiki/"):      # our own generated output
                continue
            if rel.lower().endswith(".html") and "reference" not in rel.lower():
                continue
            src = repo / rel
            if not src.is_file():
                continue
            try:
                text = src.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            sec, order = section_of(name, rel)
            dst = PAGES / name / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            title, summary, heads = title_summary(text, src)
            created, updated, first_msg = dates(repo, rel, src)
            plain = clean_md(text)
            rows.append({"repo": name, "rel": rel, "page": f"pages/{name}/{rel}".replace("\\", "/"), "section": sec, "order": order, "title": title, "summary": summary,
                         "headings": heads, "words": len(re.findall(r"\w+", plain)), "created": created, "updated": updated, "first_commit": first_msg,
                         "tags": tags_for(plain, title)})
    rows.sort(key=lambda r: (r["order"], r["repo"], r["rel"]))
    now = datetime.now().astimezone()
    fmt = lambda d: d.strftime("%Y-%m-%d %H:%M")
    day = lambda d: d.strftime("%Y-%m-%d")

    # ---------------- INDEX.md (topic) ----------------
    L = [f"# Wiki index by topic\n\n{len(rows)} pages from 2 repositories, generated {fmt(now)}. Use `TIMELINE.md` for time order and `TAGS.md` for what the pages talk about.\n"]
    L.append("**Start here:** [`pages/lab/docs/REVIEW_REPORT.md`](pages/lab/docs/REVIEW_REPORT.md) (honest review) · [`pages/lab/docs/FIXES_AND_TESTS.md`](pages/lab/docs/FIXES_AND_TESTS.md) (latest tests) · "
             "[`pages/lab/RESEARCH.md`](pages/lab/RESEARCH.md) (protocol) · [`pages/mapper/WIKI.md`](pages/mapper/WIKI.md) (the product's own wiki)\n")
    cur = None
    for r in rows:
        if r["section"] != cur:
            cur = r["section"]
            L.append(f"\n## {cur}\n\n| Page | What it says | Created | Updated | Words | Tags |\n|---|---|---|---|---|---|")
        L.append(f"| [{r['title'][:70]}]({quote(r['page'], safe='/')}) | {r['summary'][:130].replace('|', '/')} | {day(r['created'])} | {day(r['updated'])} | {r['words']} | {', '.join(r['tags'][:3])} |")
    # data catalogue (non-markdown files that matter)
    L.append("\n## Data and results files (not copied; open at the original path)\n\n| File | Size | Modified | What it is |\n|---|---|---|---|")
    data = [("docs/experiments", "*.json", "experiment results"), ("docs/experiments", "*.npz", "real telemetry captured from your EC2 hosts"),
            ("docs/literature", "*.csv", "literature tables"), ("docs/literature", "references.bib", "bibliography (metadata verified via Crossref/OpenAlex)"),
            ("litdb", "papers.csv", "survey table as CSV"), ("results", "*/summary.json", "method-comparison runs")]
    for d, pat, what in data:
        for f in sorted((HERE / d).glob(pat)):
            L.append(f"| `{d}/{f.relative_to(HERE / d).as_posix()}` | {f.stat().st_size / 1024:.0f} KB | {day(datetime.fromtimestamp(f.stat().st_mtime))} | {what} |")
    (OUT / "INDEX.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---------------- TIMELINE.md ----------------
    T = [f"# Wiki timeline\n\nGenerated {fmt(now)}. Dates come from git history (created = first commit of the file, updated = latest commit).\n"]
    T.append("\n## 1. When each page was created (oldest first)\n")
    cur = None
    for r in sorted(rows, key=lambda r: r["created"]):
        if day(r["created"]) != cur:
            cur = day(r["created"])
            T.append(f"\n### {cur}\n")
        T.append(f"- {r['created'].strftime('%H:%M')} [{r['title'][:80]}]({quote(r['page'], safe='/')}) ({r['repo']}) · {r['section'].split(':')[0]}")
    T.append("\n## 2. Most recently updated (newest first, top 25)\n")
    for r in sorted(rows, key=lambda r: r["updated"], reverse=True)[:25]:
        T.append(f"- {fmt(r['updated'])} [{r['title'][:80]}]({quote(r['page'], safe='/')}) ({r['repo']})")
    T.append("\n## 3. Work history (commits of both repositories, newest first)\n")
    for name, repo in REPOS:
        T.append(f"\n### {name}\n")
        for line in git(repo, "log", "--format=%aI|%h|%s", "-n", "80").strip().splitlines():
            try:
                d, h, s = line.split("|", 2)
                T.append(f"- {fmt(datetime.fromisoformat(d))} `{h}` {s[:110]}")
            except ValueError:
                continue
    (OUT / "TIMELINE.md").write_text("\n".join(T) + "\n", encoding="utf-8")

    # ---------------- TAGS.md (content) ----------------
    G = [f"# Wiki index by content\n\nTags are derived from what is written inside each page (keyword counts), not from file names. A page appears under a tag when the topic is mentioned at least 4 times or in its title.\n"]
    for tag in TAGS:
        pages = [r for r in rows if tag in r["tags"]]
        if not pages:
            continue
        G.append(f"\n## {tag} ({len(pages)})\n")
        for r in sorted(pages, key=lambda r: r["section"] + r["rel"]):
            G.append(f"- [{r['title'][:80]}]({quote(r['page'], safe='/')}) · {r['section'].split(':')[0]} · {day(r['updated'])}")
    (OUT / "TAGS.md").write_text("\n".join(G) + "\n", encoding="utf-8")

    # ---------------- CATALOG.csv + README ----------------
    with open(OUT / "CATALOG.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["repo", "source_path", "wiki_page", "section", "title", "summary", "words", "created", "updated", "tags"])
        for r in rows:
            w.writerow([r["repo"], r["rel"], r["page"], r["section"], r["title"], r["summary"], r["words"], fmt(r["created"]), fmt(r["updated"]), "; ".join(r["tags"])])
    (OUT / "README.md").write_text(
        "# Wiki\n\nOne place for all documentation of **microservice-mapper** (the product) and **rca-lab** (the research harness).\n\n"
        "| File | Use it to |\n|---|---|\n| [INDEX.md](INDEX.md) | browse by topic |\n| [TIMELINE.md](TIMELINE.md) | see what was written / done when, plus the commit history |\n"
        "| [TAGS.md](TAGS.md) | find pages by what they talk about (RCA, cascade, SSH, benchmarks, limitations ...) |\n| [CATALOG.csv](CATALOG.csv) | filter everything in a spreadsheet |\n| `pages/` | copies of every document |\n\n"
        "**The copies in `pages/` are refreshed, not edited.** Edit the original (shown in `CATALOG.csv` as `source_path`), then rebuild:\n\n```\n.venv\\Scripts\\python tools\\build_wiki.py\n```\n\n"
        f"Last build: {fmt(now)}; {len(rows)} pages.\n", encoding="utf-8")
    print(f"wiki built: {len(rows)} pages -> {OUT}")
    for sec in dict.fromkeys(r["section"] for r in rows):
        print(f"  {sum(r['section'] == sec for r in rows):3d}  {sec}")


if __name__ == "__main__":
    main()
