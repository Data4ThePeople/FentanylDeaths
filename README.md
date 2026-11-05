# Fentanyl Deaths, County by County, 1999-2024

An interactive map from Data 4 The People of deaths involving synthetic opioids, mostly fentanyl, in every U.S. county from 1999 to 2024. Pick a year, press play (at 1x, 2x or 5x speed), choose one state, or click a county to see its deaths, rate and trend next to its state and the U.S.

**Live map:** https://data4thepeople.github.io/FentanylDeaths/

## What is counted

Deaths of U.S. residents whose underlying cause was a drug overdose (ICD-10 X40-X44, X60-X64, X85, Y10-Y14) and whose death certificate lists T40.4, "other synthetic narcotics," among the causes. CDC uses this group to track fentanyl deaths. Most are illegally made fentanyl, but it also includes tramadol and other synthetic opioids. Deaths are counted in the county where the person lived.

## What's in this repo

| Path | What it is |
|---|---|
| `data/raw/wonder/` | CDC WONDER exports, unchanged, with CDC's query settings and footnotes. `PULLED.txt` describes every query. |
| `data/raw/geo/` | County and state shapes (us-atlas 3.0.1, Census 2017 boundaries). |
| `data/clean/` | One tidy CSV per level (county, state, U.S.), plus the same for overdoses where no drug was named (T50.9). |
| `data/build/dashboard.json` | The data the page reads. |
| `dist/index.html` | The map, one self-contained file. |
| `scripts/` | Everything that builds the above. |
| `DATASETS.md` | The data, its limits, and every method decision. |
| `TIEOUT.md` | Every number on the page checked against the raw exports. |
| `RESEARCH.md` | Sources for a short history of fentanyl. |

## Data sources

| Source | Used for |
|---|---|
| CDC, National Center for Health Statistics. Multiple Cause of Death, 1999-2020, on CDC WONDER | 1999-2017 |
| CDC, National Center for Health Statistics. Multiple Cause of Death, 2018-2024, Single Race, on CDC WONDER (2024 final data released February 2026) | 2018-2024 |
| U.S. Census Bureau cartographic boundaries via us-atlas | Map shapes |

Use of the CDC data is bound by the [CDC WONDER data use restrictions](https://wonder.cdc.gov/datause.html), including not publishing death counts of 9 or fewer.

## Rebuild

WONDER's API does not return county data, so the exports in `data/raw/wonder/` come from the WONDER web form (settings in `PULLED.txt`). From the repo root:

```
python3 scripts/build_geo.py       # county shapes
python3 scripts/clean_wonder.py    # raw exports to data/clean/
python3 scripts/validate_sums.py   # counties vs states vs U.S., and the 2018-2020 overlap
python3 scripts/build.py           # data/build/dashboard.json
python3 scripts/render.py          # dist/index.html
python3 scripts/tieout.py          # TIEOUT.md
```

## Method notes

- **Counties with 0 to 9 deaths are one gray class.** CDC does not publish county counts of 1 to 9, and its terms bar publishing any count of 9 or fewer, including zero.
- **State totals that would reveal a small county count are withheld.** If a state's total minus its published counties would show that its gray counties had fewer than 10 deaths combined, the state's total and rate are left out for that year.
- **Crude rates in every year.** CDC does not provide county age-adjusted rates in its 2018-2024 database.
- **Counties with 10 to 19 deaths are hatched**, because their rates can swing a lot by chance. For 1999-2017 their rates are calculated as deaths divided by population times 100,000, the way CDC calculates crude rates.
- **The ranking lists only counties with 20 or more deaths.**
- **Two CDC databases meet at 2018.** Their county death counts are identical for 2018-2020.
- **Early counts are likely low**, because more overdose death certificates did not name a drug in earlier years.

See `DATASETS.md` for the full method and every known limit.
