import csv, json, re, time, requests, pathlib
ROOT = pathlib.Path(r"C:\Users\MITE\Downloads\final project (short and sweet)")
rows = list(csv.DictReader(open(ROOT / "docs/literature/team_sheet.csv", encoding="utf-8")))
FIELDS = "id,title,publication_year,cited_by_count,doi,primary_location,abstract_inverted_index,authorships"

def abstract(inv):
    if not inv: return ""
    pos = {}
    for w, idxs in inv.items():
        for i in idxs: pos[i] = w
    return " ".join(pos[i] for i in sorted(pos))
def norm(s): return set(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())

out = []
for r in rows:
    title = r["Title"].split(":", 1)[1].strip() if ":" in r["Title"] else r["Title"]
    short = r["Title"].split(":", 1)[0]
    best, bs = None, 0
    for q in (title, r["Title"]):
        try:
            res = requests.get("https://api.openalex.org/works", params={"search": q, "per-page": 6, "select": FIELDS}, timeout=40).json().get("results", [])
        except Exception as e:
            print("ERR", q[:40], e); continue
        for w in res:
            sc = len(norm(title) & norm(w.get("title") or "")) / max(len(norm(title) | norm(w.get("title") or "")), 1)
            if sc > bs: best, bs = w, sc
        if bs >= 0.8: break
        time.sleep(0.3)
    rec = {"author": r["Author"], "listed": r["Title"], "match": round(bs, 2)}
    if best and bs >= 0.55:
        rec.update(title=best["title"], year=best["publication_year"], cites=best["cited_by_count"], doi=best.get("doi"),
                   venue=((best.get("primary_location") or {}).get("source") or {}).get("display_name"),
                   first_author=((best.get("authorships") or [{}])[0].get("author") or {}).get("display_name"),
                   abstract=abstract(best.get("abstract_inverted_index")))
    out.append(rec)
    print(f"{rec['match']:.2f} {r['Author']:8} {short[:16]:16} -> {(rec.get('title') or 'NOT FOUND')[:70]} | {rec.get('year')} | {(rec.get('venue') or '')[:34]} | abs={len(rec.get('abstract',''))}")
(ROOT / "docs/literature/team_lookup.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
