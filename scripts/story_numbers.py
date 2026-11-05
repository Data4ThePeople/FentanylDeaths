"""Numbers for the post's beats, from the built page data (data/build/dashboard.json) and, for beat 1,
the national overdose totals in SUD_V3's raw WONDER exports. Prints everything BEATS.md cites.

Beat 1: all overdose deaths (underlying cause X40-X44, X60-X64, X85, Y10-Y14, summed over states) vs deaths
        involving T40.4. One death can involve several drugs; "involving" is not "caused only by."
Beat 4: counties with 20 or more deaths in a year only (the page's ranking rule).
Beat 5: 2023 to 2024 for counties with 20+ deaths in both years, and for states shown in both years.
"""
import csv, io, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUD = ROOT.parent / "SUD_V3/data/raw/wonder"
D = json.loads((ROOT / "data/build/dashboard.json").read_text())
Y = D["years"]
ix = Y.index


def rows(p):
    L = Path(p).read_text().split("\n")
    end = next((i for i, l in enumerate(L) if l.startswith('"---"')), len(L))
    return [r for r in csv.DictReader(io.StringIO("\n".join(L[:end])), delimiter="\t" if str(p).endswith(".txt") else ",")
            if not r.get("Notes")]


# ---- beat 1
tot = Counter()
for p, lo, hi in ((SUD / "ucd_1999_2020_state_year_drug.csv", 1999, 2017), (SUD / "ucd_2018_2024_state_year_drug.csv", 2018, 2024)):
    for r in rows(p):
        if lo <= int(r["Year"]) <= hi:
            tot[int(r["Year"])] += int(r["Deaths"])
fen = dict(zip(Y, D["us"]["d"]))
print("== beat 1: overdose deaths, T40.4-involved, the rest")
for y in sorted(tot):
    print(y, tot[y], fen[y], tot[y] - fen[y], f"{fen[y] / tot[y]:.0%}")
for a, b in ((2001, 2022), (2013, 2022), (2023, 2024)):
    dt, df = tot[b] - tot[a], fen[b] - fen[a]
    print(f"{a}-{b}: all overdoses {dt:+,}; T40.4-involved {df:+,}; without T40.4 {dt - df:+,}; T40.4 share of change {df / dt:.0%}")

# ---- beat 4
C = {f: g for f, g in D["counties"].items() if f in D["paths"]}


def ok(g, y, m=20):
    i = ix(y)
    return g["s"][i] == "P" and g["d"][i] is not None and g["d"][i] >= m


def top(y, n):
    return sorted((f for f, g in C.items() if ok(g, y)), key=lambda f: -C[f]["r"][ix(y)])[:n]


print("\n== beat 4: highest rates 2024 (20+ deaths)")
for f in top(2024, 10):
    g = C[f]; print(g["n"], g["d"][ix(2024)], g["r"][ix(2024)])
print("\n== beat 4: highest rate in any year (20+ deaths)")
peaks = sorted(((max((C[f]["r"][ix(y)], y) for y in Y if ok(C[f], y)), f) for f in C if any(ok(C[f], y) for y in Y)), reverse=True)
for (r, y), f in peaks[:10]:
    print(C[f]["n"], y, C[f]["d"][ix(y)], r)
print("\n== beat 4: years in the national top 25 by rate, 2016-2024")
cnt = Counter(f for y in range(2016, 2025) for f in top(y, 25))
for f, n in cnt.most_common(10):
    print(C[f]["n"], n)
print("\n== beat 4: most deaths 2024")
for f in sorted((f for f in C if C[f]["d"][ix(2024)]), key=lambda f: -C[f]["d"][ix(2024)])[:10]:
    g = C[f]; print(g["n"], g["d"][ix(2024)], g["r"][ix(2024)], "2023:", g["d"][ix(2023)])

# ---- beat 5
a, b = ix(2023), ix(2024)
both = [f for f in C if ok(C[f], 2023) and ok(C[f], 2024)]
up = sorted((f for f in both if C[f]["d"][b] > C[f]["d"][a]), key=lambda f: C[f]["d"][a] - C[f]["d"][b])
print(f"\n== beat 5: {len(both)} counties with 20+ deaths in 2023 and 2024; {len(up)} had more deaths in 2024")
for f in up:
    g = C[f]; print(g["n"], g["d"][a], "->", g["d"][b], g["r"][a], "->", g["r"][b])
st = sorted(((g["d"][b] - g["d"][a]) / g["d"][a], g["n"], g["d"][a], g["d"][b]) for g in D["states"].values() if g["d"][a] and g["d"][b])
print(f"\n== beat 5: {len(st)} states shown in both years; {sum(1 for s in st if s[0] >= 0)} rose or held")
for s in st[-6:][::-1] + st[:5]:
    print(f"{s[1]} {s[2]} -> {s[3]} ({s[0]:+.1%})")
print("not comparable:", [g["n"] for g in D["states"].values() if not (g["d"][a] and g["d"][b])])
