"""Scopus-indexing lookup against a spreadsheet YOU download (Scopus has no free API).

Put one or both files in litdb/reference/:
  * the official "Scopus Source List" (.xlsx) from Elsevier  -> indexed / active / discontinued-for-quality
  * Scimago's journal ranking export (.csv, ';' separated)    -> SJR quartile (based on Scopus data)
Matching is by ISSN (print or electronic); title is only used as a fallback and is flagged as a weaker match.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

REF = Path(__file__).resolve().parent.parent / "reference"


def norm_issn(x) -> str:
    return re.sub(r"[^0-9Xx]", "", str(x or "")).upper()


def norm_title(x) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(x or "").lower()).strip()


def _col(headers, *needles):
    for i, h in enumerate(headers):
        hl = str(h or "").lower()
        if all(n in hl for n in needles):
            return i
    return None


class Index:
    def __init__(self):
        self.scopus_by_issn, self.scopus_by_title = {}, {}
        self.sjr_by_issn, self.sjr_by_title = {}, {}
        self.files = []
        for f in sorted(REF.glob("*")):
            n = f.name.lower()
            try:
                if f.suffix.lower() == ".xlsx" and ("scopus" in n or "source" in n):
                    self._load_scopus(f)
                elif f.suffix.lower() == ".csv":
                    self._load_scimago(f)
            except Exception as e:
                print(f"[scopus_check] could not read {f.name}: {e}")

    def _load_scopus(self, f: Path):
        import openpyxl
        wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
        rows_total = 0
        for ws in wb.worksheets:
            it = ws.iter_rows(values_only=True)
            head = None
            for row in it:                                 # find the header row
                if row and any("source title" in str(c or "").lower() for c in row):
                    head = row
                    break
            if not head:
                continue
            c_title, c_pi, c_ei = _col(head, "source title"), _col(head, "print"), _col(head, "e-issn")
            c_act, c_type, c_pub = _col(head, "active"), _col(head, "source type"), _col(head, "publisher")
            c_disc = _col(head, "discontinued")
            for row in it:
                if not row or c_title is None or not row[c_title]:
                    continue
                rec = {"title": row[c_title], "active": str(row[c_act]) if c_act is not None else "",
                       "type": str(row[c_type]) if c_type is not None else "", "publisher": str(row[c_pub]) if c_pub is not None else "",
                       "discontinued_quality": str(row[c_disc]) if c_disc is not None and row[c_disc] else ""}
                for c in (c_pi, c_ei):
                    if c is not None and norm_issn(row[c]):
                        self.scopus_by_issn[norm_issn(row[c])] = rec
                self.scopus_by_title[norm_title(row[c_title])] = rec
                rows_total += 1
        self.files.append(f"{f.name} ({rows_total} sources)")

    def _load_scimago(self, f: Path):
        with open(f, encoding="utf-8-sig", newline="") as fh:
            rd = csv.reader(fh, delimiter=";")
            head = next(rd)
            c_t, c_i = _col(head, "title"), _col(head, "issn")
            c_q, c_s = _col(head, "quartile"), _col(head, "sjr")
            if c_t is None or c_i is None:
                return
            n = 0
            for row in rd:
                if len(row) <= max(c_t, c_i):
                    continue
                rec = {"title": row[c_t], "quartile": row[c_q] if c_q is not None and len(row) > c_q else "", "sjr": row[c_s] if c_s is not None and len(row) > c_s else ""}
                for i in re.split(r"[,\s]+", row[c_i]):
                    if norm_issn(i):
                        self.sjr_by_issn[norm_issn(i)] = rec
                self.sjr_by_title[norm_title(row[c_t])] = rec
                n += 1
            self.files.append(f"{f.name} ({n} journals)")

    def lookup(self, issns: list[str], title: str = "") -> dict:
        if not (self.scopus_by_issn or self.sjr_by_issn):
            return {"scopus": "unknown (no list in litdb/reference/)", "scopus_match": "", "sjr_quartile": "", "list_files": ""}
        out = {"scopus": "not found in list", "scopus_match": "", "sjr_quartile": "", "list_files": "; ".join(self.files)}
        for i in map(norm_issn, issns or []):
            if i in self.scopus_by_issn:
                r = self.scopus_by_issn[i]
                status = "indexed" if r["active"].lower().startswith("active") else f"in list but {r['active'] or 'status unknown'}"
                if r["discontinued_quality"]:
                    status += " (DISCONTINUED for quality reasons)"
                out.update(scopus=status, scopus_match=f"ISSN {i}: {r['title']}")
                break
        else:
            r = self.scopus_by_title.get(norm_title(title))
            if r:
                out.update(scopus="possible (title match only; verify)", scopus_match=f"title: {r['title']}")
        for i in map(norm_issn, issns or []):
            if i in self.sjr_by_issn:
                out["sjr_quartile"] = self.sjr_by_issn[i]["quartile"]
                if out["scopus"].startswith("not found") or out["scopus"].startswith("unknown"):
                    out["scopus"] = "indexed (via Scimago/Scopus data)"
                break
        return out
