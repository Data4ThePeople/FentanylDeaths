"""Join the cleaned WONDER data and the county geometry into data/build/dashboard.json.

Per place, one value per year (null where WONDER publishes none):
  d  deaths (published counts only, 10 or more)
  r  crude rate per 100,000
  s  status string, one character per year: P published, L 0 to 9 deaths, M missing, N deaths but no rate,
     X state total withheld because it would reveal a county count under 10
Nothing is filled or interpolated. Duplicate keys are a hard failure (checked in clean_wonder.py).
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
YEARS = list(range(1999, 2025))
CODE = {"pub": "P", "low": "L", "missing": "M", "na": "N"}


def series(path):
    out = {}
    for r in csv.DictReader(open(ROOT / path)):
        g = out.setdefault(r["code"], {"n": r["name"], "d": [None] * len(YEARS), "r": [None] * len(YEARS),
                                       "s": ["M"] * len(YEARS)})
        i = YEARS.index(int(r["year"]))
        g["d"][i] = int(r["deaths"]) if r["deaths"] else None
        g["r"][i] = float(r["rate"]) if r["rate"] else None
        g["s"][i] = CODE[r["status"]]
    for g in out.values():
        g["s"] = "".join(g["s"])
    return out


def main():
    geo = json.loads((ROOT / "data/build/geo.json").read_text())
    counties = series("data/clean/county.csv")
    states = series("data/clean/state.csv")
    us = series("data/clean/us.csv")["US"]
    # A state total minus its published counties gives the combined deaths of its gray (0 to 9) counties.
    # Where that remainder is under 10, showing the state total or rate would publish a count of 9 or
    # fewer, which WONDER's data use terms bar. Those state-years are withheld (status X).
    withheld = 0
    for sf, g in states.items():
        cs = [counties[c] for c in counties if c[:2] == sf]
        for i in range(len(YEARS)):
            if g["d"][i] is None:
                continue
            gray = [c for c in cs if c["s"][i] == "L"]
            rest = g["d"][i] - sum(c["d"][i] or 0 for c in cs)
            if gray and rest < 10:
                g["d"][i] = g["r"][i] = None
                g["s"] = g["s"][:i] + "X" + g["s"][i + 1:]
                withheld += 1
    print(withheld, "state-years withheld so no county count under 10 can be derived")
    shapes = set(geo["counties"])
    unmatched = sorted(set(counties) - shapes)
    D = {"years": YEARS, "us": us, "states": states,
         "counties": counties, "unmatched": unmatched,
         "paths": geo["counties"], "stateLines": geo["states"], "nation": geo["nation"]}
    (ROOT / "data/build/dashboard.json").write_text(json.dumps(D, separators=(",", ":")))
    print(len(D["counties"]), "counties on the map;", len(unmatched), "county codes with no shape:", unmatched)


if __name__ == "__main__":
    main()
