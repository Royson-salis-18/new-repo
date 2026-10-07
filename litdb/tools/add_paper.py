"""Add a paper to the database: extract full text, fetch verified metadata, check Scopus, write a note skeleton.

    python litdb/tools/add_paper.py "C:/path/paper.pdf" [--doi 10.xxxx/yyyy] [--key sun2024deephunt] [--batch 1]

Outputs
    litdb/texts/<key>.txt      full text, page-marked ("=== page N ===")
    litdb/pdfs/<key>.pdf       copy of the PDF
    litdb/papers/<key>.md      note skeleton: metadata filled, reading sections TO BE WRITTEN from the full text
Never overwrites an existing note (prints a warning instead).
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scopus_check import Index  # noqa: E402

DB = Path(__file__).resolve().parent.parent
TEMPLATE = DB / "tools" / "note_template.md"
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>,;]+)", re.I)
ARXIV_RE = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})(v\d+)?", re.I)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def extract(pdf: Path) -> list[str]:
    from pypdf import PdfReader
    pages = []
    for pg in PdfReader(str(pdf)).pages:
        try:
            pages.append(pg.extract_text() or "")
        except Exception:
            pages.append("")
    return pages


def find_doi(text: str) -> str | None:
    for m in DOI_RE.finditer(text):
        d = m.group(1).rstrip(".)")
        if not d.lower().startswith("10.48550"):         # arXiv's own DOI is not the venue DOI
            return d
    return None


def crossref(doi: str) -> dict | None:
    try:
        r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=30)
        if r.status_code != 200:
            return None
        m = r.json()["message"]
    except Exception:
        return None
    authors = "; ".join(f"{a.get('family', '')}, {a.get('given', '')}".strip(", ") for a in m.get("author", []))
    year = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    return {"title": (m.get("title") or [""])[0], "authors": authors, "year": year,
            "venue": (m.get("container-title") or [""])[0], "publisher": m.get("publisher", ""), "type": m.get("type", ""),
            "issn": m.get("ISSN", []), "isbn": m.get("ISBN", []), "doi": m.get("DOI", doi), "cited_by_crossref": m.get("is-referenced-by-count"),
            "n_references": m.get("reference-count"), "license": ((m.get("license") or [{}])[0].get("URL", ""))}


def arxiv_meta(aid: str) -> dict | None:
    import xml.etree.ElementTree as ET
    try:
        t = requests.get("http://export.arxiv.org/api/query", params={"id_list": aid}, timeout=30).text
        e = ET.fromstring(t).find("{http://www.w3.org/2005/Atom}entry")
        ns = "{http://www.w3.org/2005/Atom}"
        return {"title": re.sub(r"\s+", " ", e.find(ns + "title").text), "year": int(e.find(ns + "published").text[:4]),
                "authors": "; ".join(a.find(ns + "name").text for a in e.findall(ns + "author")), "venue": "arXiv preprint", "type": "preprint",
                "publisher": "arXiv", "issn": [], "isbn": [], "doi": "", "arxiv": aid}
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--doi")
    ap.add_argument("--key")
    ap.add_argument("--batch", default="")
    a = ap.parse_args()
    pdf = Path(a.pdf)
    pages = extract(pdf)
    text = "\n".join(f"=== page {i + 1} ===\n{p}" for i, p in enumerate(pages))
    chars = sum(len(p) for p in pages)
    meta, src = None, "none"
    doi = a.doi or find_doi("\n".join(pages[:3]))
    if doi:
        meta = crossref(doi)
        src = "crossref" if meta else "doi-not-resolved"
    if not meta:
        m = ARXIV_RE.search("\n".join(pages[:2]))
        if m:
            meta, src = arxiv_meta(m.group(1)), "arxiv"
    meta = meta or {"title": "", "authors": "", "year": "", "venue": "", "publisher": "", "type": "", "issn": [], "isbn": [], "doi": doi or ""}
    fam = slug(meta["authors"].split(",")[0]) if meta.get("authors") else slug(pdf.stem)[:12]
    first_word = slug(next((w for w in re.split(r"\W+", meta.get("title", "")) if len(w) > 3), ""))
    key = a.key or f"{fam}{meta.get('year') or ''}{first_word}"
    idx = Index()
    sc = idx.lookup(meta.get("issn") or [], meta.get("venue", ""))

    (DB / "texts").mkdir(exist_ok=True)
    (DB / "texts" / f"{key}.txt").write_text(text, encoding="utf-8")
    (DB / "pdfs").mkdir(exist_ok=True)
    if not (DB / "pdfs" / f"{key}.pdf").exists():
        shutil.copy2(pdf, DB / "pdfs" / f"{key}.pdf")
    note = DB / "papers" / f"{key}.md"
    if note.exists():
        print(f"[warn] {note.name} already exists; not overwritten")
    else:
        t = TEMPLATE.read_text(encoding="utf-8")
        fill = {"KEY": key, "TITLE": meta["title"].replace('"', "'"), "AUTHORS": meta.get("authors", ""), "YEAR": meta.get("year", ""), "VENUE": meta.get("venue", ""),
                "PUBLISHER": meta.get("publisher", ""), "DOC_TYPE": meta.get("type", ""), "DOI": meta.get("doi", ""), "ISSN": ",".join(meta.get("issn") or []),
                "SCOPUS": sc["scopus"], "SCOPUS_MATCH": sc["scopus_match"], "SJR_Q": sc["sjr_quartile"], "LISTS": sc["list_files"], "PAGES": len(pages),
                "CHARS": chars, "BATCH": a.batch, "META_SRC": src, "CITED_BY": meta.get("cited_by_crossref", ""), "NREFS": meta.get("n_references", ""),
                "LICENSE": meta.get("license", "")}
        for k, v in fill.items():
            t = t.replace("{{" + k + "}}", str(v))
        note.write_text(t, encoding="utf-8")
    print(f"key={key}\n pages={len(pages)} chars={chars} (chars/page={chars // max(len(pages), 1)}; ~0 means a scanned PDF needing OCR)\n"
          f" metadata={src} | doi={meta.get('doi') or '-'} | venue={meta.get('venue') or '-'} | issn={meta.get('issn')}\n"
          f" scopus={sc['scopus']} {sc['scopus_match']} | sjr={sc['sjr_quartile'] or '-'}\n note={note}\n text={DB / 'texts' / (key + '.txt')}")


if __name__ == "__main__":
    main()
