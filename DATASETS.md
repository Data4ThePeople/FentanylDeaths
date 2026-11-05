# Datasets

## CDC WONDER Multiple Cause of Death (NCHS, National Vital Statistics System)

**What it is.** Counts of deaths of U.S. residents from death certificates, with population and death rates. One row is one place and year. Our count is deaths whose **underlying cause** was a drug overdose (ICD-10 X40-X44 accidental, X60-X64 suicide, X85 homicide, Y10-Y14 intent undetermined) and that list **T40.4** among the multiple causes. T40.4 is "other synthetic narcotics." CDC uses it as its measure of deaths involving synthetic opioids other than methadone, mostly illegally made fentanyl. It also includes tramadol and other synthetic opioids. On the page this is "deaths involving synthetic opioids, mostly fentanyl."

**Where it comes from.** https://wonder.cdc.gov, two databases:
- Multiple Cause of Death, 1999-2020 (D77). We use it for 1999-2017.
- Multiple Cause of Death, 2018-2024, Single Race (D157). We use it for 2018-2024.

Exports are tab-separated text with CDC's query settings and footnotes at the bottom, kept unchanged in `data/raw/wonder/`. WONDER's API returns national data only, so county exports come from the web form. They are run in Eric's Chrome after he accepts the data use terms. `data/raw/wonder/PULLED.txt` records each query.

**Version and vintage.** 2024 deaths are final. CDC added them to WONDER in February 2026. Final data are not revised after release.

**Coverage.** All U.S. counties and county-equivalents, by county of **residence** (where the person lived, not where they died). 1999-2024. Deaths of non-residents of the U.S. are excluded. Nothing is filled in or modeled: every count is a tally of death certificates.

**Changes over time.**
- **Two databases, 2018 seam.** D77 uses bridged-race population estimates. D157 uses single-race postcensal estimates (July 1 resident population). Death counts should match in the overlap years, 2018-2020; populations, and so rates, can differ slightly. We compare the overlap county by county.
- **County changes (from WONDER's Location Updates):**
  - Alaska: Chugach (02063) and Copper River (02066) census areas were formed from Valdez-Cordova (02261) in January 2019. WONDER's note on how deaths and populations are reported across the split is checked against the exports.
  - Connecticut: for 2022-2024, deaths are reported for the 8 old counties, but there are no county population estimates (Census uses 9 planning regions). WONDER gives no county rates for Connecticut in those years. The state rate is available.
  - Virginia: Bedford city (51515) merged into Bedford County (51019) on July 1, 2013. Clifton Forge city (51560) merged into Alleghany County (51005) on July 1, 2001.
  - Florida: Dade County (12025) became Miami-Dade (12086) in 1997, before our period.
- **Death certificate detail.** Some overdose certificates do not name a drug (T50.9, "other and unspecified drugs"). This was more common in earlier years and varies by state and county, often with the kind of death investigation system. Fentanyl counts are lower where the drug was not named. We pull T50.9 overdoses by county and year to report where this is common. We do not adjust any counts.

**Suppressed, censored or masked values.**
- Counts of 1 to 9 deaths show as "Suppressed," along with their rates, for any place below the national level.
- WONDER's data use terms say not to publish "death counts of 9 or fewer or death rates based on counts of nine or fewer." So zero counts are not shown as zero either.
- **How we handle it:** counties with 0 to 9 deaths get one neutral color labeled "0 to 9 deaths (CDC does not publish counts this small)." We never work out a hidden count by subtracting published counties from a state total. The page's national explanation ("N counties had 10 or more deaths and account for X% of U.S. deaths; the rest were in counties with fewer than 10 each") is computed at the national level only, where it cannot reveal any one county's count.

**Missing data.** Connecticut county rates for 2022-2024 are "Not Available" and shown as no rate (24 county-years). Some Alaska areas show "Missing" in D77 years before they existed or after they were redrawn; they are shown as no data. A county with no row in an export is treated as missing, not zero.

**Revisions.** None expected for final years. We pin the exports by date in `PULLED.txt`.

**Units and rounding.** Rates are per 100,000 residents, published to one decimal.
- **Crude rate:** deaths divided by population.
- **Age-adjusted rate:** uses the 2000 U.S. standard population. D77 provides it for counties; D157 does not allow age-adjusted rates for any county grouping ("Age Adjusted Rates are not available when county level locations ... are selected"). It is kept in the clean files where published but not used on the map.
- **Map value: the crude rate in every year**, so 1999-2017 and 2018-2024 use the same measure. Counties with older populations may show lower crude rates partly because of age; the page says so.

**Known quirks.**
- **Unreliable rates.** D77 marks rates based on fewer than 20 deaths "Unreliable" and does not show them. D157, since February 2026, flags a rate only when its 95% confidence interval is wider than 160% of the rate, which in practice shows rates for every county with 10 or more deaths. To treat all years alike, for D77 counties with 10 to 19 deaths we compute the crude rate ourselves with CDC's formula, deaths / population x 100,000, rounded to one decimal (`rate_src = calc` in `data/clean/county.csv`; 815 county-years). Counties with 10 to 19 deaths are hatched on the map in every year and labeled "rate can swing a lot from year to year." This uses counts of 10 or more only, which the data use terms allow.
- **Rankings** use only counties with 20 or more deaths in that year, so tiny counties with unstable rates do not fill the top of the list.

**Uncertainty.** WONDER gives 95% confidence intervals for each rate, and we show them in the hover. Counts are complete tallies, not samples, but rates in small counties swing from year to year by chance.

**License and attribution.** U.S. government public data. Credit: "Centers for Disease Control and Prevention, National Center for Health Statistics. Multiple Cause of Death on CDC WONDER." Use is bound by the WONDER data use restrictions, which Eric accepted on 2026-11-05.

## us-atlas counties-albers-10m (Mike Bostock, from U.S. Census Bureau cartographic boundaries)

**What it is.** County and state outlines, already projected (Albers USA, Alaska and Hawaii inset), in TopoJSON. 3,142 counties.

**Where it comes from.** `https://cdn.jsdelivr.net/npm/us-atlas@3.0.1/counties-albers-10m.json`, saved to `data/raw/geo/`. ISC license.

**Version and vintage.** us-atlas 3.0.1 uses Census 2017 cartographic boundaries at 1:10 million. Valdez-Cordova (02261) is one shape, so Chugach and Copper River are not drawn separately. Connecticut has its 8 old counties. Oglala Lakota County, SD is 46102.

**Known quirks.** Unmatched codes: WONDER codes 02201, 02232, 02280 (old Alaska areas), 51515 (Bedford city, VA) and 51560 (Clifton Forge city, VA) have no 2017 shape; none had 10 or more deaths in any year. 46113 (Shannon County, SD) and 02270 (Wade Hampton, AK) are mapped to their renamed codes 46102 (Oglala Lakota) and 02158 (Kusilvak). Small counties and Virginia's independent cities are very small at this scale. Every WONDER county code is matched to a shape. Any code without a shape is listed in `TIEOUT.md` and in the page notes.
