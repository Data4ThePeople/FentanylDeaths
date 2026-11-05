# Status

Project: FentanylDeaths (fentanyl deaths by county, 1999-2024)
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: none yet
Step: 1
Since: 2026-11-05

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | | |
| 2a | Draft with brackets resolved | | |
| 2b | Eric's edit, Claude's look-over | | |
| 2c | Slice markup | | |
| 2d | Hero 1680x1080 + alt text | | |
| 2e | SEO | | |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Log

- 2026-11-05 Step 1 opened. Topic: the rise of fentanyl in the US and the matching rise in deaths; an interactive map of the fentanyl death rate by county over time, plus a short history of fentanyl for readers. Fentanyl only. Target: publish 2026-11-06.
- 2026-11-05 Decisions: fentanyl deaths = underlying cause drug overdose (X40-X44, X60-X64, X85, Y10-Y14) with multiple cause T40.4, CDC WONDER Multiple Cause of Death 1999-2020 and 2018-2024 Single Race, by county of residence and year. Suppressed counties (1 to 9 deaths) get their own color outside the rate scale, labeled; zero-death counties labeled separately; no filling.  rankings only for counties with 20+ deaths. Extra export of overdoses with no drug named (T50.9) to report where certification varies. County boundary changes (CT, AK, VA, CO) checked and noted.
- 2026-11-05 Data pulled in Eric's Chrome (38 WONDER exports; county queries split into 2-year batches to stay under WONDER's 2-minute limit). National counts match SUD_V3. Validation: states sum to U.S. in every fully published year; counties never exceed state totals; D77 and D157 county counts identical for 2018-2020 (9,441 county-years).
- 2026-11-05 WONDER's data use terms bar publishing counts of 9 or fewer, including zero, so 0 and 1-9 are one gray class "0 to 9 deaths"; no subtraction to reveal hidden counts.
- 2026-11-05 Eric approved: map uses crude rates in every year (D157 gives no county age-adjusted rates); D77 rates for 10-19 deaths computed as deaths / population x 100,000 so all years match D157's practice; 10-19 deaths hatched in every year; ranking 20+ deaths. Banner shows U.S. deaths each year plus a national explanation of the share of deaths in counties with 10+.
- 2026-11-05 Eric: state selector (zooms to one state) and 1x/2x/5x play added. Disclosure fix: state totals and rates withheld for 43 state-years where the state total minus published counties would reveal under 10 deaths in its gray counties; tie-out checks it. Tie-out 250,501 values, 0 mismatches.
- 2026-11-05 Repo made public with README; GitHub Pages live at https://data4thepeople.github.io/FentanylDeaths/
- 2026-11-05 Independent tie-out: about 263,000 values, 0 differences (incl. WONDER API re-pull of U.S. totals). Its findings fixed: small counts derivable by subtraction (closed by the 43 withheld state-years plus a U.S.-level check), renamed counties now shown under current names (WONDER uses old names), overlap note corrected (rates match), gray-class wording now cites CDC's data rule (WONDER does publish zeros). Eric: play speeds 1x/2x/3x; bar chart shows the selected state.
