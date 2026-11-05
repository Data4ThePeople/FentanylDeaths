# Tie-out: dist/index.html against the raw CDC WONDER exports

Run `python3 scripts/tieout.py`. Recomputes from `data/raw/wonder/*.txt` directly, not from `data/clean/`.

**Result: 250,501 values checked, 0 mismatches.** 43 state-years are withheld under the disclosure rule (state total minus published counties under 10 with at least one gray county), and the check confirms no shown state total allows a county count under 10 to be derived.

Checked for every county (3,147 codes), state and U.S. year, 1999-2024: status class (0 to 9 / published / missing / no rate), deaths, crude rate (WONDER's, or deaths / population x 100,000 for D77 counties with 10 to 19 deaths); the banner, the national explanation and the ranking, recomputed from raw county rows; every county with 10+ deaths has a map shape; the page's fixed thresholds match its wording.

## Numbers the page shows each year

| Year | U.S. deaths | U.S. rate | Counties 10+ deaths | Share of U.S. deaths in them | Share elsewhere | Hatched (10-19) | Ranked (20+) |
|---|---|---|---|---|---|---|---|
| 1999 | 730 | 0.3 | 6 | 12% | 88% | 6 | 0 |
| 2000 | 782 | 0.3 | 5 | 8% | 92% | 5 | 0 |
| 2001 | 957 | 0.3 | 6 | 10% | 90% | 5 | 1 |
| 2002 | 1,295 | 0.5 | 11 | 15% | 85% | 8 | 3 |
| 2003 | 1,400 | 0.5 | 17 | 18% | 82% | 15 | 2 |
| 2004 | 1,664 | 0.6 | 17 | 16% | 84% | 12 | 5 |
| 2005 | 1,742 | 0.6 | 24 | 21% | 79% | 19 | 5 |
| 2006 | 2,707 | 0.9 | 39 | 37% | 63% | 28 | 11 |
| 2007 | 2,213 | 0.7 | 23 | 17% | 83% | 16 | 7 |
| 2008 | 2,306 | 0.8 | 30 | 19% | 81% | 24 | 6 |
| 2009 | 2,946 | 1.0 | 43 | 25% | 75% | 31 | 12 |
| 2010 | 3,007 | 1.0 | 45 | 25% | 75% | 36 | 9 |
| 2011 | 2,666 | 0.9 | 35 | 21% | 79% | 27 | 8 |
| 2012 | 2,628 | 0.8 | 38 | 22% | 78% | 31 | 7 |
| 2013 | 3,105 | 1.0 | 55 | 30% | 70% | 42 | 13 |
| 2014 | 5,544 | 1.7 | 129 | 54% | 46% | 76 | 53 |
| 2015 | 9,580 | 3.0 | 207 | 69% | 31% | 106 | 101 |
| 2016 | 19,413 | 6.0 | 344 | 83% | 17% | 142 | 202 |
| 2017 | 28,466 | 8.7 | 478 | 88% | 12% | 186 | 292 |
| 2018 | 31,335 | 9.6 | 495 | 89% | 11% | 198 | 297 |
| 2019 | 36,359 | 11.1 | 554 | 89% | 11% | 215 | 339 |
| 2020 | 56,516 | 17.2 | 795 | 92% | 8% | 296 | 499 |
| 2021 | 70,601 | 21.3 | 958 | 93% | 7% | 365 | 593 |
| 2022 | 73,838 | 22.2 | 991 | 94% | 6% | 343 | 640 |
| 2023 | 72,776 | 21.7 | 983 | 93% | 7% | 364 | 611 |
| 2024 | 47,735 | 14.0 | 738 | 90% | 10% | 288 | 442 |

## Mismatches

None.
