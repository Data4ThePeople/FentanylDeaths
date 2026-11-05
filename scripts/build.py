"""Join the cleaned WONDER data and the county geometry into data/build/dashboard.json.

Per place, one value per year (null where WONDER publishes none):
  d  deaths (published counts only, 10 or more)
  r  crude rate per 100,000
  s  status string, one character per year: P published, L 0 to 9 deaths, M missing, N deaths but no rate
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
    shapes = set(geo["counties"])
    unmatched = sorted(set(counties) - shapes)
    D = {"years": YEARS, "us": us, "states": states,
         "counties": counties, "unmatched": unmatched,
         "paths": geo["counties"], "stateLines": geo["states"], "nation": geo["nation"]}
    (ROOT / "data/build/dashboard.json").write_text(json.dumps(D, separators=(",", ":")))
    print(len(D["counties"]), "counties on the map;", len(unmatched), "county codes with no shape:", unmatched)


if __name__ == "__main__":
    main()
