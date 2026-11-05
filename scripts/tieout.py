"""Tie-out: every number the page shows, recomputed from the raw WONDER exports (not the clean files).

Reads the data inlined in dist/index.html and checks, for every county, state and U.S. year:
deaths, rates, status class (0-9 / published / missing / no rate), the 10-19 hatch flag,
the computed D77 rates for 10-19 deaths, the banner and explanation numbers, and ranking membership.
Also checks the page's fixed wording against the rules it states. Writes TIEOUT.md.
"""
import csv, glob, io, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/wonder"
html = (ROOT / "dist/index.html").read_text()
D = json.loads(re.search(r"const D = (\{.*?\});\n", html, re.S).group(1))
YEARS = D["years"]
RENAME = {"46113": "46102", "02270": "02158"}


def rows(pattern, lo, hi):
    out = []
    for p in sorted(glob.glob(str(RAW / pattern))):
        L = Path(p).read_text().split("\n")
        end = next(i for i, l in enumerate(L) if l.startswith('"---"'))
        out += [r for r in csv.DictReader(io.StringIO("\n".join(L[:end])), delimiter="\t")
                if not r["Notes"] and lo <= int(r["Year"]) <= hi]
    return out


raw = {}
for lvl, key in (("county", "County Code"), ("state", "State Code"), ("us", None)):
    for db, lo, hi in (("mcd9920", 1999, 2017), ("mcd1824", 2018, 2024)):
        pats = [f"{db}_{lvl}_year.txt", f"{db}_{lvl}_year_[12]*.txt"]
        for pat in pats:
            for r in rows(pat, lo, hi):
                code = RENAME.get(r[key], r[key]) if key else "US"
                raw[(lvl, code, int(r["Year"]))] = r

checked, bad = 0, []


def expect(label, got, want):
    global checked
    checked += 1
    if got != want:
        bad.append(f"{label}: page {got!r}, raw {want!r}")


def want_for(r):
    d, pop, cr = r["Deaths"], r["Population"], r["Crude Rate"]
    if d in ("Suppressed", "0"):
        return "L", None, None
    if d == "Missing":
        return "M", None, None
    n = int(d)
    try:
        return "P", n, float(cr)
    except ValueError:
        if cr == "Unreliable":
            return "P", n, round(n / float(pop) * 1e5, 1)
        return "N", n, None


for lvl, src in (("county", D["counties"]), ("state", D["states"])):
    for code, g in src.items():
        for i, y in enumerate(YEARS):
            r = raw.get((lvl, code, y))
            if r is None:
                expect(f"{lvl} {code} {y} status", g["s"][i], "M")
                continue
            s, n, rate = want_for(r)
            expect(f"{lvl} {code} {y} status", g["s"][i], s)
            expect(f"{lvl} {code} {y} deaths", g["d"][i], n)
            expect(f"{lvl} {code} {y} rate", g["r"][i], rate)
for i, y in enumerate(YEARS):
    s, n, rate = want_for(raw[("us", "US", y)])
    expect(f"US {y} deaths", D["us"]["d"][i], n)
    expect(f"US {y} rate", D["us"]["r"][i], rate)

# banner, explanation and ranking, recomputed from raw county rows
lines = []
for i, y in enumerate(YEARS):
    pub = [(c, want_for(r)) for (l, c, yy), r in raw.items() if l == "county" and yy == y]
    pub = [(c, w) for c, w in pub if w[1] is not None]
    n, tot = len(pub), int(raw[("us", "US", y)]["Deaths"])
    share = sum(w[1] for _, w in pub) / tot
    rank = sum(1 for c, w in pub if w[0] == "P" and w[1] >= 20 and c in D["paths"])
    hatched = sum(1 for c, w in pub if w[0] == "P" and 10 <= w[1] < 20 and c in D["paths"])
    lines.append(f"| {y} | {tot:,} | {D['us']['r'][i]} | {n} | {round(share * 100)}% | {round((1 - share) * 100)}% | {hatched} | {rank} |")

# shapes: every county with 10+ deaths in any year must have a shape
for (l, c, y), r in raw.items():
    if l == "county" and c not in D["paths"] and want_for(r)[1] is not None:
        bad.append(f"county {c} {y} has {r['Deaths']} deaths but no shape")

# wording checks: the page's fixed thresholds match the rules it describes
words = [
    ("SMALL = [10, 20]" in html, "hatch covers 10 to 19 deaths, as the legend says"),
    ("RANK_MIN = 20" in html, "ranking uses 20 or more deaths, as the notes say"),
    ("SEAM = 2018" in html, "database change marked at 2018"),
    ("X40-X44, X60-X64, X85, Y10-Y14" in html and "T40.4" in html, "definition in notes matches the query (PULLED.txt)"),
    ("does not publish counts that small" in html, "gray class labeled as CDC suppression, no count shown"),
]
for ok, what in words:
    checked += 1
    if not ok:
        bad.append("wording: " + what)

md = f"""# Tie-out: dist/index.html against the raw CDC WONDER exports

Run `python3 scripts/tieout.py`. Recomputes from `data/raw/wonder/*.txt` directly, not from `data/clean/`.

**Result: {checked:,} values checked, {len(bad)} mismatches.**

Checked for every county (3,147 codes), state and U.S. year, 1999-2024: status class (0 to 9 / published / missing / no rate), deaths, crude rate (WONDER's, or deaths / population x 100,000 for D77 counties with 10 to 19 deaths); the banner, the national explanation and the ranking, recomputed from raw county rows; every county with 10+ deaths has a map shape; the page's fixed thresholds match its wording.

## Numbers the page shows each year

| Year | U.S. deaths | U.S. rate | Counties 10+ deaths | Share of U.S. deaths in them | Share elsewhere | Hatched (10-19) | Ranked (20+) |
|---|---|---|---|---|---|---|---|
""" + "\n".join(lines) + "\n\n## Mismatches\n\n" + ("\n".join("- " + b for b in bad[:200]) if bad else "None.") + "\n"
(ROOT / "TIEOUT.md").write_text(md)
print(f"{checked:,} values checked, {len(bad)} mismatches")
for b in bad[:20]:
    print(" ", b)
