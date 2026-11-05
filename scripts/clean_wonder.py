"""Tidy the CDC WONDER exports into data/clean/{county,state,us}.csv and *_t509.csv.

Years 1999-2017 come from the 1999-2020 database (D77), 2018-2024 from the 2018-2024 Single Race
database (D157). Each file holds one row per place and year:
  deaths      published count, or empty when WONDER shows Suppressed (1-9), 0, Missing
  status      pub (10 or more deaths) | low (0-9: WONDER's Suppressed or 0, shown as one class
              because WONDER's terms bar publishing counts of 9 or fewer) | missing | na (no rate)
  rate        crude rate per 100,000. WONDER's published rate where it shows one. D77 hides
              rates for 10-19 deaths ("Unreliable"); there we compute deaths / population * 100,000
              rounded to 1 decimal, CDC's own crude-rate formula (rate_src = calc)
  small       1 when deaths are 10-19 (hatched on the map in every year)
County codes renamed by Census are mapped to the current code (46113 -> 46102, 02270 -> 02158).
"""
import csv, glob, io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/wonder"
OUT = ROOT / "data/clean"
RENAME = {"46113": "46102", "02270": "02158"}
FIELDS = ["code", "name", "year", "deaths", "population", "rate", "rate_lo", "rate_hi", "rate_src", "status", "small",
          "aa_rate"]


def load(path):
    """Rows of a WONDER export: the data block ends at the first '---' line; footnotes follow."""
    lines = Path(path).read_text().split("\n")
    end = next(i for i, l in enumerate(lines) if l.startswith('"---"'))
    return [r for r in csv.DictReader(io.StringIO("\n".join(lines[:end])), delimiter="\t") if not r["Notes"]]


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def tidy(r, key, name):
    d, pop, cr = r["Deaths"], num(r["Population"]), r["Crude Rate"]
    out = {"code": RENAME.get(r[key], r[key]) if key else "US", "name": r[name] if name else "United States",
           "year": int(r["Year"]), "deaths": "", "population": "" if pop is None else int(pop), "rate": "",
           "rate_lo": "", "rate_hi": "", "rate_src": "", "small": 0, "aa_rate": r.get("Age Adjusted Rate", "")}
    if d in ("Suppressed", "0"):
        out["status"] = "low"
        out["aa_rate"] = ""
        return out
    if d == "Missing":
        out["status"] = "missing"
        out["aa_rate"] = ""
        return out
    n = int(d)
    out["deaths"] = n
    out["small"] = int(10 <= n < 20)
    if num(cr) is not None:
        out.update(rate=num(cr), rate_lo=num(r.get("Crude Rate Lower 95% Confidence Interval")),
                   rate_hi=num(r.get("Crude Rate Upper 95% Confidence Interval")), rate_src="wonder", status="pub")
    elif cr == "Unreliable" and pop:
        out.update(rate=round(n / pop * 1e5, 1), rate_src="calc", status="pub")
    else:  # Connecticut counties 2022 on: deaths but "Not Available" rate
        out["status"] = "na"
    if num(out["aa_rate"]) is None:
        out["aa_rate"] = ""
    return out


def build(level, suffix=""):
    key, name = {"county": ("County Code", "County"), "state": ("State Code", "State"), "us": (None, None)}[level]
    rows = {}
    for db, lo, hi in (("mcd9920", 1999, 2017), ("mcd1824", 2018, 2024)):
        for p in sorted(glob.glob(str(RAW / f"{db}_{level}_year{suffix}.txt")) +
                        glob.glob(str(RAW / f"{db}_{level}_year{suffix}_[12]*.txt"))):
            for r in load(p):
                y = int(r["Year"])
                if lo <= y <= hi:
                    t = tidy(r, key, name)
                    k = (t["code"], y)
                    if k in rows:
                        raise SystemExit(f"duplicate {level}{suffix} key {k} in {p}")
                    rows[k] = t
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{level}{suffix}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        w.writerows(rows[k] for k in sorted(rows))
    return rows


if __name__ == "__main__":
    for s in ("", "_t509"):
        for lvl in ("county", "state", "us"):
            rows = build(lvl, s)
            print(f"{lvl}{s}: {len(rows)} rows, years {min(y for _, y in rows)}-{max(y for _, y in rows)}")
