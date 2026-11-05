"""Post tie-out: every number in posts/fentanyl-deaths-by-county/POST.md that comes from our data, recomputed here.

Sources, independent of scripts/story_numbers.py and scripts/post_charts.py:
  - U.S. fentanyl (T40.4) and unnamed-drug (T50.9) deaths and rates: data/raw/wonder/*_us_year*.txt
  - county and state values: the data inlined in dist/index.html, which scripts/tieout.py ties to the raw
    WONDER exports value by value (TIEOUT.md)
  - all overdose deaths and deaths by opioid type: SUD_V3's raw WONDER exports (1999-2020 database through 2017,
    2018-2024 database after)

Each check names a passage that must appear in the post word for word, with the recomputed number inside it.
Then every number in the post's text is listed as checked here, or as cited to an outside source, so nothing
is left unaccounted for. Writes the result to TIEOUT.md under "Post numbers".
"""
import csv, io, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST = (ROOT / "posts/fentanyl-deaths-by-county/POST.md").read_text()
RAW = ROOT / "data/raw/wonder"
SUD = ROOT.parent / "SUD_V3/data/raw/wonder"
html = (ROOT / "dist/index.html").read_text()
D = json.loads(re.search(r"const D = (\{.*?\});\n", html, re.S).group(1))
Y = D["years"]; ix = Y.index
C = {f: g for f, g in D["counties"].items() if f in D["paths"]}
WEST = {"AK", "AZ", "CA", "CO", "HI", "ID", "MT", "NM", "NV", "OR", "UT", "WA", "WY"}


def table(p, delim):
    L = Path(p).read_text().split("\n")
    end = next((i for i, l in enumerate(L) if l.startswith('"---"')), len(L))
    return [r for r in csv.DictReader(io.StringIO("\n".join(L[:end])), delimiter=delim) if not r.get("Notes")]


def us_series(stem):
    out = {}
    for p, lo, hi in ((RAW / f"mcd9920_{stem}.txt", 1999, 2017), (RAW / f"mcd1824_{stem}.txt", 2018, 2024)):
        for r in table(p, "\t"):
            y = int(r["Year"])
            if lo <= y <= hi:
                assert y not in out
                out[y] = (int(r["Deaths"]), float(r["Crude Rate"]))
    return out


FEN, UNK = us_series("us_year"), us_series("us_year_t509")
TOT, OPI = {}, {}
for p, lo, hi in ((SUD / "ucd_1999_2020_state_year_drug.csv", 1999, 2017), (SUD / "ucd_2018_2024_state_year_drug.csv", 2018, 2024)):
    for r in table(p, ","):
        y = int(r["Year"])
        if lo <= y <= hi:
            TOT[y] = TOT.get(y, 0) + int(r["Deaths"])
for p, lo, hi in ((SUD / "mcd_1999_2020_year_drugtype.csv", 1999, 2017), (SUD / "mcd_2018_2024_year_drugtype.csv", 2018, 2024)):
    for r in table(p, ","):
        y = int(r["Year"])
        if lo <= y <= hi:
            assert (r["Multiple Cause of death Code"], y) not in OPI
            OPI[(r["Multiple Cause of death Code"], y)] = float(r["Crude Rate"])

checks, bad, covered = [], [], []


def pct(x, d=0):
    """Half-up rounding, as a reader would do it."""
    q = round(x * 10 ** d + 1e-9 * (1 if x >= 0 else -1)) / 10 ** d
    return f"{q:.{d}f}%"


def check(passage, *values):
    """passage must be in the post, and contain each recomputed value."""
    ok = passage in POST
    miss = [v for v in values if v not in passage]
    checks.append(passage)
    if not ok:
        bad.append(f"passage not found in post: {passage!r}")
    if miss:
        bad.append(f"passage {passage!r} lacks recomputed {miss}")
    if ok and not miss:
        covered.append(passage)


f, t = lambda y: FEN[y][0], lambda y: TOT[y]
n = lambda v: f"{v:,}"

# ---- intro and subtitle
check("from 2013 to 2022, yearly overdose deaths in the U.S. went up by 63,959, from 43,982 to 107,941".replace("from 2013", "From 2013"),
      n(t(2022) - t(2013)), n(t(2013)), n(t(2022)))
check("deaths involving fentanyl went up by 70,733, from 3,105 to 73,838", n(f(2022) - f(2013)), n(f(2013)), n(f(2022)))
check("Overdose deaths that did not involve fentanyl went down by 6,774", n(-((t(2022) - f(2022)) - (t(2013) - f(2013)))))
check("deaths involving fentanyl account for 82% of the rise", pct((f(2022) - f(2001)) / (t(2022) - t(2001)) * 100))
check("Fentanyl was involved in 7% of overdose deaths in 2013, 51% in 2019 and 68% in 2022",
      *(pct(f(y) / t(y) * 100) for y in (2013, 2019, 2022)))
check("overdose deaths fell by 25,623, and deaths involving fentanyl fell by 25,041, or 98% of the drop",
      n(t(2023) - t(2024)), n(f(2023) - f(2024)), pct((f(2023) - f(2024)) / (t(2023) - t(2024)) * 100))
check("Deaths involving fentanyl rose from 3,105 in 2013 to 73,838 in 2022, then fell to 47,735 in 2024",
      n(f(2013)), n(f(2022)), n(f(2024)))
check("All overdose deaths rose from 43,982 in 2013 to 107,941 in 2022, then fell to 79,384 in 2024",
      n(t(2013)), n(t(2022)), n(t(2024)))
check("Deaths involving fentanyl rose from 3,105 in 2013 to 73,838 in 2022, then fell to 47,735 in 2024.](images/01",
      n(f(2024)))

# ---- how to read the map
cnt10 = lambda y: [g for g in D["counties"].values() if g["s"][ix(y)] in "PN" and (g["d"][ix(y)] or 0) >= 10]  # N: count but no rate (CT 2022+)
share22 = sum(g["d"][ix(2022)] for g in cnt10(2022)) / f(2022)
check("In 1999, only 6 counties had 10 or more fentanyl deaths. In 2013 there were 55. By 2022 there were 991, and those counties held 94%",
      str(len(cnt10(1999))), str(len(cnt10(2013))), str(len(cnt10(2022))), pct(share22 * 100))

# ---- history
by = {g["n"]: g for g in D["counties"].values()}
cook, wayne, phl = by["Cook County, IL"], by["Wayne County, MI"], by["Philadelphia County, PA"]
check("Cook County, Illinois, had 283 fentanyl deaths and Wayne County, Michigan, had 103",
      str(cook["d"][ix(2006)]), str(wayne["d"][ix(2006)]))
if not all(phl["s"][ix(y)] == "L" for y in (2005, 2006, 2007)):
    bad.append("Philadelphia is not 0-9 in each of 2005-2007")
check("shows fewer than 10 on the map in each of those years")
check("In 2006 Cook County had 283 and Wayne County had 103", str(cook["d"][ix(2006)]), str(wayne["d"][ix(2006)]))
check("the U.S. fentanyl death rate was 1.0 per 100,000 people in 2013 and 22.2 in 2022",
      f"{FEN[2013][1]:.1f}", f"{FEN[2022][1]:.1f}")
yrs01 = range(2001, 2025)
her = max(OPI[("T40.1", y)] for y in yrs01); rx = max(OPI[("T40.2", y)] for y in yrs01)
her_y = [y for y in yrs01 if OPI[("T40.1", y)] == her]; rx_y = [y for y in yrs01 if OPI[("T40.2", y)] == rx]
fpk = max(FEN[y][1] for y in yrs01); fpk_y = [y for y in yrs01 if FEN[y][1] == fpk]
check("neither death rate went above 4.8 per 100,000 people", f"{max(her, rx):.1f}")
check("The fentanyl death rate peaked at 22.2 in 2022", f"{fpk:.1f}", *map(str, fpk_y))
check("That is 363% higher than the highest rate for heroin (4.8 in 2016 and 2017)",
      pct((fpk - her) / her * 100), f"{her:.1f}", " and ".join(map(str, her_y)))
check("393% higher than the highest rate for prescription opioids (4.5 in 2016 and 2017)",
      pct((fpk - rx) / rx * 100), f"{rx:.1f}", " and ".join(map(str, rx_y)))
check("The fentanyl rate rises from 1.0 in 2013 to 22.2 in 2022, then falls in 2023 and 2024",
      f"{FEN[2013][1]:.1f}", f"{FEN[2022][1]:.1f}")
if not FEN[2024][1] < FEN[2023][1] < FEN[2022][1]:
    bad.append("fentanyl rate does not fall in both 2023 and 2024")
check("Prescription opioid and heroin rates stay under 5")
if max(her, rx) >= 5:
    bad.append("prescription opioid or heroin rate reaches 5")


# ---- counties that stand out (20+ deaths)
def pub(g, y, m=20):
    i = ix(y)
    return g["s"][i] == "P" and g["d"][i] is not None and g["d"][i] >= m


peaks = sorted(((max((C[k]["r"][ix(y)], y) for y in Y if pub(C[k], y)), k) for k in C if any(pub(C[k], y) for y in Y)), reverse=True)
(mr, my), mk = peaks[0]
check("McDowell County, West Virginia, had 206.4 fentanyl deaths per 100,000 residents in 2023 (36 deaths)",
      f"{mr:.1f}", str(my), str(C[mk]["d"][ix(my)]))
if C[mk]["n"] != "McDowell County, WV":
    bad.append(f"highest rate on record is {C[mk]['n']}")
top10 = [C[k]["n"] for _, k in peaks[:10]]
wv = [x.replace(" County, WV", "") for x in top10 if x.endswith(", WV")]
check("eight of the top ten are in West Virginia: McDowell, Wyoming, Logan, Mercer, Raleigh, Cabell, Mason and Fayette",
      *wv)
if len(wv) != 8:
    bad.append(f"{len(wv)} WV counties in top ten")
check("The other two are Baltimore city and Scioto County, Ohio")
if sorted(x for x in top10 if not x.endswith(", WV")) != ["Baltimore city, MD", "Scioto County, OH"]:
    bad.append(f"non-WV top ten: {[x for x in top10 if not x.endswith(', WV')]}")
r24 = sorted((k for k in C if pub(C[k], 2024)), key=lambda k: -C[k]["r"][ix(2024)])
bal = next(k for k in C if C[k]["n"] == "Baltimore city, MD")
check("Baltimore city had the highest rate in the country in 2024, 95.2 per 100,000 (541 deaths)",
      f"{C[bal]['r'][ix(2024)]:.1f}", str(C[bal]["d"][ix(2024)]))
if r24[0] != bal:
    bad.append("Baltimore city is not first in 2024")
bw = max((C[bal]["r"][ix(y)], y) for y in Y if pub(C[bal], y))
check("Its worst year was 2021, at 135.6 per 100,000 (782 deaths)", str(bw[1]), f"{bw[0]:.1f}", str(C[bal]["d"][ix(bw[1])]))
top25 = lambda y: set(sorted((k for k in C if pub(C[k], y)), key=lambda k: -C[k]["r"][ix(y)])[:25])
every = [C[k]["n"] for k in set.intersection(*(top25(y) for y in range(2016, 2025)))]
check("Baltimore city, Cabell County, West Virginia (home to Huntington), and St. Louis city were in the country's top 25 by rate every year from 2016 to 2024")
if sorted(every) != sorted(["Baltimore city, MD", "Cabell County, WV", "St. Louis city, MO"]):
    bad.append(f"top 25 every year 2016-2024: {every}")
for name, pos, passage in (("Rio Arriba County, NM", 2, "Rio Arriba County, New Mexico, had the second-highest rate in the country (80.1 per 100,000, 32 deaths)"),
                           ("Anchorage Borough, AK", 7, "Anchorage, Alaska, was seventh (55.9 per 100,000, 162 deaths)")):
    k = next(k for k in C if C[k]["n"] == name)
    check(passage, f"{C[k]['r'][ix(2024)]:.1f}", str(C[k]["d"][ix(2024)]))
    if r24.index(k) + 1 != pos:
        bad.append(f"{name} is #{r24.index(k) + 1} in 2024, post says {pos}")
d24 = sorted((k for k in C if C[k]["s"][ix(2024)] == "P" and C[k]["d"][ix(2024)]), key=lambda k: -C[k]["d"][ix(2024)])[:3]
check("Maricopa County, Arizona, had 1,005 fentanyl deaths (21.5 per 100,000), Cook County, Illinois, had 990 (19.1) and Los Angeles County had 988 (10.1)",
      *(x for k in d24 for x in (n(C[k]["d"][ix(2024)]), f"{C[k]['r'][ix(2024)]:.1f}")))
if [C[k]["n"] for k in d24] != ["Maricopa County, AZ", "Cook County, IL", "Los Angeles County, CA"]:
    bad.append(f"most deaths 2024: {[C[k]['n'] for k in d24]}")
check("Eight of the ten are in West Virginia; the others are Baltimore city (135.6 in 2021) and Scioto County, Ohio (126.4 in 2020)",
      f"{bw[0]:.1f}", *(f"{r:.1f} in {y}" for (r, y), k in peaks[:10] if C[k]["n"] == "Scioto County, OH"))

# ---- 2024
check("Fentanyl deaths fell from 72,776 in 2023 to 47,735 in 2024", n(f(2023)), n(f(2024)))
a, b = ix(2023), ix(2024)
st = sorted(((g["d"][b] - g["d"][a]) / g["d"][a] * 100, g["n"]) for g in D["states"].values() if g["d"][a] and g["d"][b])
hidden = sorted((g["n"], "2024" if g["d"][a] else "2023") for g in D["states"].values() if not (g["d"][a] and g["d"][b]))
check("That is 49 states, counting DC", str(len(st)))
if any(p >= 0 for p, _ in st):
    bad.append("a state rose or held")
check("Hawaii's 2024 total and New Hampshire's 2023 total are not shown")
if hidden != [("Hawaii", "2024"), ("New Hampshire", "2023")]:
    bad.append(f"hidden states: {hidden}")
big = ", ".join(f"{s[1]} ({pct(-s[0], 1)})" for s in st[:5])
small = ", ".join(f"{s[1]} ({pct(-s[0], 1)})" for s in st[::-1][:5])
check("The largest drops were in West Virginia (down 48.4%), Arkansas (46.6%), North Dakota (46.1%), Virginia (45.8%) and Wisconsin (45.7%)",
      *(f"{s[1]}" for s in st[:5]), *(pct(-s[0], 1) for s in st[:5]))
check("The smallest were in the West: Nevada (down 4.9%), Alaska (6.9%), Utah (9.8%), Washington (13.5%) and Arizona (16.5%)",
      *(f"{s[1]}" for s in st[::-1][:5]), *(pct(-s[0], 1) for s in st[::-1][:5]))
check("West Virginia fell most, 48.4%, then Arkansas, North Dakota, Virginia and Wisconsin. Nevada fell least, 4.9%",
      pct(-st[0][0], 1), pct(-st[-1][0], 1))
both = [k for k in C if pub(C[k], 2023) and pub(C[k], 2024)]
fell = [k for k in both if C[k]["d"][b] < C[k]["d"][a]]
same = [k for k in both if C[k]["d"][b] == C[k]["d"][a]]
rose = [k for k in both if C[k]["d"][b] > C[k]["d"][a]]
check("Of 435 counties with 20 or more fentanyl deaths in both 2023 and 2024, 411 (94.5%) had fewer deaths in 2024. Five were unchanged and 19 rose",
      str(len(both)), str(len(fell)), pct(len(fell) / len(both) * 100, 1), str(len(rose)))
if len(same) != 5:
    bad.append(f"{len(same)} unchanged")
both10 = [k for k in C if pub(C[k], 2023, 10) and pub(C[k], 2024, 10)]
fell10 = [k for k in both10 if C[k]["d"][b] < C[k]["d"][a]]
check("639 of 706 counties (90.5%) fell", str(len(fell10)), str(len(both10)), pct(len(fell10) / len(both10) * 100, 1))
check("All overdose deaths fell 26%", pct((t(2023) - t(2024)) / t(2023) * 100))
check("from 39,160 to 29,771", n(UNK[2023][0]), n(UNK[2024][0]))
check("The number of fentanyl deaths fell 34.4%", pct((f(2023) - f(2024)) / f(2023) * 100, 1))
check("Overdose deaths that did not involve fentanyl fell 1.8%, from 32,231 to 31,649",
      pct(((t(2023) - f(2023)) - (t(2024) - f(2024))) / (t(2023) - f(2023)) * 100, 1), n(t(2023) - f(2023)), n(t(2024) - f(2024)))

# ---- counties that went the other way
west = [k for k in rose if C[k]["n"][-2:] in WEST]
check("Nineteen counties had more fentanyl deaths in 2024 than in 2023. Nine are in Western states, and three of those are in Washington")
if (len(rose), len(west), sum(C[k]["n"].endswith(", WA") for k in west)) != (19, 9, 3):
    bad.append(f"rose {len(rose)}, west {len(west)}")
spk = max(rose, key=lambda k: C[k]["d"][b] - C[k]["d"][a])
check("Spokane County, Washington, had the largest increase, from 176 to 249 deaths (31.9 to 44.8 per 100,000)",
      str(C[spk]["d"][a]), str(C[spk]["d"][b]), f"{C[spk]['r'][a]:.1f}", f"{C[spk]['r'][b]:.1f}")
if C[spk]["n"] != "Spokane County, WA" or spk != max(rose, key=lambda k: (C[k]["d"][b] - C[k]["d"][a]) / C[k]["d"][a]):
    bad.append("Spokane is not the largest increase by count and by percent")
clk = max(rose, key=lambda k: C[k]["d"][b])
check("Clark County, Nevada, home to Las Vegas, had the most deaths of the group, 519 in 2024", str(C[clk]["d"][b]))
if C[clk]["n"] != "Clark County, NV":
    bad.append("Clark County is not the most deaths among the 19")
check("Spokane County, Washington, rose most, 41.5% (176 to 249)", pct((C[spk]["d"][b] - C[spk]["d"][a]) / C[spk]["d"][a] * 100, 1))
check("Nine of the 19 are in Western states")

# ---- method
tie = (ROOT / "TIEOUT.md").read_text()
nwith = int(re.search(r"(\d+) state-years are withheld", tie).group(1))
nvals = int(re.search(r"\*\*Result: ([\d,]+) values checked", tie).group(1).replace(",", ""))
check("we leave the state's total out for that year (43 state-years)", str(nwith))
check("about 250,000 values, with no differences")
if round(nvals, -4) != 250000:
    bad.append(f"page tie-out checked {nvals:,} values")

# ---- every number in the post's text, accounted for
body = POST.split("\n---\n", 1)[1] if POST.startswith("---") else POST
sub = re.search(r"^subtitle: (.*)$", POST, re.M).group(1)
text = re.sub(r"\]\([^)]*\)", "]", sub + "\n" + body)            # drop link targets and image paths
text = re.sub(r"<iframe.*?</iframe>", "", text, flags=re.S)
text = re.sub(r"^::: spacer.*$|^#.*$", "", text, flags=re.M)
nums = []
for para in text.split("\n"):
    for m in re.finditer(r"\d[\d,]*(?:\.\d+)?%?", para):
        v = m.group(0).rstrip(",")
        if any(v in c and c in para for c in covered):
            continue
        nums.append((v, para[max(0, m.start() - 70):m.end() + 40].strip()))

out = [f"**Post numbers: {len(checks)} passages checked, {len(bad)} mismatches.**", ""]
out += [f"- MISMATCH: {x}" for x in bad] or ["No mismatches."]
out += ["", "Numbers in the post not recomputed here (cited to an outside source, a year or date, a count of items, or a step in the map instructions):", ""]
out += [f"- `{v}`: ...{ctx}..." for v, ctx in nums]
print("\n".join(out))
section = "## Post numbers\n\nRun `python3 scripts/tieout_post.py`.\n\n" + "\n".join(out) + "\n"
tie = (ROOT / "TIEOUT.md").read_text()
tie = tie.split("\n## Post numbers\n")[0].rstrip("\n") + "\n\n" + section
(ROOT / "TIEOUT.md").write_text(tie)
