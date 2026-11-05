"""Exploration (Eric, November 5, 2026): did the counties with the highest fentanyl death rates before 2024
see the largest drops in 2024?

Universe: counties with 20+ published fentanyl deaths in the base year. A county whose next-year count is
suppressed (0 to 9) is reported separately; its change is at least -(base - 9) deaths.

Checks against regression to the mean (high years tend to be followed by lower ones by chance):
  A. level = 2023 rate, change = 2023 -> 2024
  B. level = average of the 2021 and 2022 rates (years not used in the change), change = 2023 -> 2024
  C. the same test one year earlier and two years earlier (level 2021 -> change 2021->2022; level 2022 ->
     change 2022->2023). If high counties also fell more in years without a national drop, the 2024
     pattern is not special to 2024.
"""
import json
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
D = json.loads((ROOT / "data/build/dashboard.json").read_text())
Y = D["years"]; ix = Y.index
C = {f: g for f, g in D["counties"].items() if f in D["paths"]}


def val(g, y):
    i = ix(y)
    return (g["d"][i], g["r"][i]) if g["s"][i] == "P" and g["d"][i] is not None else (None, None)


def rank(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0] * len(xs); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and xs[o[j + 1]] == xs[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = rank(a), rank(b); n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    return cov / (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5


def test(label, level_of, y0, y1, groups=5):
    rows, supp = [], []
    for f, g in C.items():
        d0, _ = val(g, y0)
        lv = level_of(g)
        if d0 is None or d0 < 20 or lv is None:
            continue
        d1, _ = val(g, y1)
        if d1 is None:
            supp.append((g["n"], d0))
            continue
        rows.append((lv, (d1 - d0) / d0 * 100, d0, d1, g["n"]))
    rows.sort()
    rho = spearman([r[0] for r in rows], [r[1] for r in rows])
    print(f"\n== {label}: {len(rows)} counties (plus {len(supp)} with {y1} count suppressed); "
          f"Spearman rank correlation, level vs % change: {rho:+.2f}")
    n = len(rows)
    for q in range(groups):
        part = rows[q * n // groups:(q + 1) * n // groups]
        s0, s1 = sum(r[2] for r in part), sum(r[3] for r in part)
        print(f"  group {q + 1} (level {part[0][0]:.1f} to {part[-1][0]:.1f}): n={len(part)}, "
              f"median change {median(r[1] for r in part):+.1f}%, pooled {s0:,} -> {s1:,} ({(s1 - s0) / s0 * 100:+.1f}%), "
              f"share that fell {sum(r[1] < 0 for r in part) / len(part):.0%}")
    if supp:
        print("  suppressed next year:", supp)
    return rows


def rate(y):
    return lambda g: val(g, y)[1]


def avg_rate(*ys):
    def f(g):
        v = [val(g, y)[1] for y in ys]
        return None if None in v else sum(v) / len(v)
    return f


rows = test("A. 2023 rate vs change 2023->2024", rate(2023), 2023, 2024)
test("B. average 2021-2022 rate vs change 2023->2024", avg_rate(2021, 2022), 2023, 2024)
test("C1. 2021 rate vs change 2021->2022 (placebo, national deaths rose)", rate(2021), 2021, 2022)
test("C2. 2022 rate vs change 2022->2023 (placebo, national deaths about flat)", rate(2022), 2022, 2023)

print("\n== top 20 counties by 2023 rate: change 2023->2024")
for lv, ch, d0, d1, n in rows[-20:][::-1]:
    print(f"  {n}: rate {lv:.1f}, {d0} -> {d1} ({ch:+.1f}%)")

# ---- states
a, b = ix(2023), ix(2024)
st = [(g["r"][a], (g["d"][b] - g["d"][a]) / g["d"][a] * 100, g["n"]) for g in D["states"].values()
      if g["d"][a] and g["d"][b]]
print(f"\n== states: {len(st)}; Spearman, 2023 rate vs % change: {spearman([s[0] for s in st], [s[1] for s in st]):+.2f}")
for s in sorted(st, reverse=True)[:10]:
    print(f"  {s[2]}: 2023 rate {s[0]:.1f}, change {s[1]:+.1f}%")
print("  lowest 2023 rates:")
for s in sorted(st)[:10]:
    print(f"  {s[2]}: 2023 rate {s[0]:.1f}, change {s[1]:+.1f}%")

# ---- is it just the West? (fentanyl reached the West later; Western counties sit in the low groups)
WEST = {"AK", "AZ", "CA", "CO", "HI", "ID", "MT", "NM", "NV", "OR", "UT", "WA", "WY"}
west_share = [sum(r[4][-2:] in WEST for r in rows[q * len(rows) // 5:(q + 1) * len(rows) // 5]) for q in range(5)]
print("\n== Western counties per 2023-rate group (A):", west_share)
C_all = C
C = {f: g for f, g in C_all.items() if g["n"][-2:] not in WEST}
test("A without the West", rate(2023), 2023, 2024)
test("C2 without the West (placebo)", rate(2022), 2022, 2023)
C = C_all
