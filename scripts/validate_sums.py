"""State-to-national and county-to-state checks on the cleaned WONDER data. Runs on every build.

1. States sum to the U.S. total each year (exact where no state is hidden; otherwise the published states
   must not exceed the U.S. total).
2. Published counties never exceed their state total, and match it exactly where the state has no
   county with 1-9 deaths.
3. The 2018-2020 overlap: D77 and D157 county death counts are identical.
"""
import csv, glob, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from clean_wonder import load, RENAME

ROOT = Path(__file__).resolve().parents[1]
rd = lambda n: list(csv.DictReader(open(ROOT / f"data/clean/{n}.csv")))
fail = []
for s in ("", "_t509"):
    us = {int(r["year"]): r for r in rd("us" + s)}
    st = collections.defaultdict(list)
    for r in rd("state" + s):
        st[int(r["year"])].append(r)
    co = collections.defaultdict(list)
    for r in rd("county" + s):
        co[(int(r["year"]), r["code"][:2])].append(r)
    exact = partial = 0
    for y, rows in st.items():
        pub = sum(int(r["deaths"]) for r in rows if r["deaths"])
        tot = int(us[y]["deaths"])
        if all(r["deaths"] for r in rows):
            exact += 1
            if pub != tot: fail.append(f"{s} {y}: states {pub} != US {tot}")
        elif pub > tot: fail.append(f"{s} {y}: published states {pub} > US {tot}")
        else: partial += 1
        for r in rows:
            if not r["deaths"]: continue
            cs = co[(y, r["code"])]
            cp = sum(int(c["deaths"]) for c in cs if c["deaths"])
            if all(c["status"] != "low" for c in cs) and cp != int(r["deaths"]) and not any(c["status"] == "missing" for c in cs):
                fail.append(f"{s} {y} {r['name']}: counties {cp} != state {r['deaths']}")
            elif cp > int(r["deaths"]):
                fail.append(f"{s} {y} {r['name']}: counties {cp} > state {r['deaths']}")
    print(f"T40.4{s or ''}: {exact} years with every state published (exact match required), {partial} with hidden states")
    # overlap
    a = {}
    for p in glob.glob(str(ROOT / f"data/raw/wonder/mcd9920_county_year{s}_[12]*.txt")):
        for r in load(p):
            if int(r["Year"]) >= 2018: a[(RENAME.get(r["County Code"], r["County Code"]), int(r["Year"]))] = r["Deaths"]
    b = {(r["code"], int(r["year"])): r for r in rd("county" + s) if int(r["year"]) <= 2020}
    diff = [(k, a[k], b[k]["deaths"] or b[k]["status"]) for k in a if k in b and
            not (a[k] == str(b[k]["deaths"]) or (a[k] in ("Suppressed", "0") and b[k]["status"] == "low"))]
    print(f"  2018-2020 overlap: {len(a)} county-years compared, {len(diff)} differ", diff[:5])
    if diff: fail.append(f"{s} overlap differences: {len(diff)}")
print("FAIL\n" + "\n".join(fail) if fail else "all checks pass")
sys.exit(1 if fail else 0)
