# Research: did West Virginia put more money into the overdose crisis than other states?

Compiled 2026-11-05. Research notes only, not post copy. Builds on `RESEARCH-funding.md` (national totals) and does not repeat it. Source files that could be saved are in `data/raw/funding/wv-funding/`.

"Fentanyl deaths" below means our T40.4 counts from `data/clean/state.csv` (CDC WONDER, final 2024 data). Populations are Census Bureau Vintage 2024 state estimates (July 1 of each year), file NST-EST2024-ALLDATA: https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/state/totals/NST-EST2024-ALLDATA.csv

## 1. What we can say

- **Federal SOR money: yes, West Virginia got much more per resident than most states.** In FY2023 its SAMHSA State Opioid Response allocation was $45,855,881, or $25.90 per resident. That is third among the 50 states and DC, behind Delaware ($37.20) and DC ($36.32). The median state got $4.08 per resident. The other two years were nearly the same: $24.99 in FY2022 (3rd) and $25.85 in FY2024 (3rd).
- **This follows from the formula, not a choice by the state.** SOR money is set by a federal formula based on each state's share of overdose deaths and of people with untreated opioid use disorder, plus a 15% set-aside for the states with the highest overdose death rates. West Virginia is listed first among the 10 set-aside states in FY2022 and FY2023. West Virginia also had the highest fentanyl death rate of any state in 2023 (64.2 per 100,000 in our data).
- **Per death, West Virginia did not stand out.** Its FY2023 SOR allocation was $40,331 per 2023 fentanyl death, 11th of 51. The median was $20,906. Small states that get the $4 million minimum (South Dakota, Wyoming, North Dakota) and the other set-aside states (Delaware, New Hampshire, DC) got more per death.
- **CDC OD2A money was small next to SOR.** West Virginia's OD2A state award is $5,339,590 a year, 4th largest in dollars and 7th per resident ($3.02, FY2025 table; median $1.03 with local awards included). That is about one-ninth of its SOR money.
- **Settlement money arrived in 2023, but very little of it was spent before mid-2024.** About $291 million went out of West Virginia's settlement fund by December 2023 ($217.5 million to the West Virginia First Foundation, $73.5 million to local governments). The Foundation paid no grants through December 31, 2024; it spent about $1.46 million on its own costs. It first awarded grants in December 2024. Local governments reported spending about $6.9 million (9.4%) of their share by June 30, 2024, and 52% of that went to law enforcement (West Virginia Watch's reading of the Foundation's report).
- **Higher SOR funding per resident does not line up with bigger drops across states.** The four states with the most SOR money per resident fell by 30.3% (DC) to 48.4% (West Virginia) from 2023 to 2024. The median state fell 35.5%. Across all 51, the rank correlation between FY2023 SOR per resident and the 2023-2024 change in fentanyl deaths is -0.18 (weak), and per death it is -0.05 (about none). This is a simple description, not a test of cause.
- **The question "did West Virginia spend more" can be answered only in part.** For SOR, yes per resident, because of the formula. For other streams we could get only some states, or only one year. No source we found adds up all overdose spending by state.

## 2. Figures with sources

### 2a. SAMHSA State Opioid Response (SOR)

- **How the formula works, FY2022 and FY2023** (SAMHSA NOFO TI-22-005, posted May 19, 2022, modified to add FY2023 as Appendix L; Appendix K and L, pages 74-79): "two elements weighted equally: the state's proportion of drug overdose deaths (CDC) and the state's proportion of people who meet diagnostic criteria for dependence or abuse of heroin or pain relievers who report not having received any treatment (NSDUH)." Each state and DC get at least $4,000,000. "The allocation continues the 15 percent set-aside for states with the highest overdose mortality rates. For the FY 2022 allocation, this set aside is distributed across 10 states (WV, DE, MD, PA, OH, NH, DC, NJ, MA, KY) based on an ordinal ranking." FY2023 uses the same 10 states. https://www.samhsa.gov/sites/default/files/grants/pdf/fy-22-sor-nofo.pdf
- **FY2024 formula change** (NOFO TI-24-008, posted May 2, 2024, Appendix A): the formula "continues to leverage data estimating drug overdose deaths and opioid misuse per state," keeps the $4M state minimum, and spreads the 15% set-aside over 25 states (WV is one). It cites section 1003 of the 21st Century Cures Act, which says the formula must "avoid a significant cliff between States with similar overdose mortality rates." https://www.samhsa.gov/sites/default/files/grants/pdf/fy-2024-sor-nofo-ti-24-008.pdf
- **West Virginia's allocations** (same NOFOs): FY2022 $44,335,111; FY2023 $45,855,881; FY2024 $45,758,863.
- **What these numbers are:** each table gives the "MAXIMUM dollar amount PER YEAR for which a state/territory can apply." They are allocations, not money spent. State totals in our parse match the program totals: $1,439,500,000 (FY2022), $1,488,500,000 (FY2023), $1,480,500,000 (FY2024), including territories.
- **Oversight problems in earlier years:** HHS Office of Inspector General, "West Virginia Lacked Effective Oversight of Its Opioid Response Grants," report A-06-22-01005, April 22, 2024. It covers the 2017-2020 STR grant and the FY2020 SOR grant. It found the state "could not support its annual progress reports," did not adequately monitor subrecipient spending, and approved advance payments while subrecipients were not spending their funds. West Virginia agreed with all five recommendations. https://oig.hhs.gov/reports/all/2024/west-virginia-lacked-effective-oversight-of-its-opioid-response-grants/ . This says nothing directly about 2023-2024 spending.

### 2b. CDC Overdose Data to Action (OD2A)

- **FY2025 award table** (CDC Injury Center, West Virginia funding page, "funding awarded from October 1, 2024, to September 30, 2025," reviewed October 14, 2026; the page lists every state). West Virginia Department of Health and Human Resources, OD2A in States: $5,339,590. West Virginia has no OD2A local award. https://www.cdc.gov/injury/budget-funding/west-virginia.html
- **The same amount in 2023:** USAspending award NU17CE010210 to the West Virginia Department of Health and Human Resources, project period September 1, 2023 to August 31, 2028, total obligated $21,721,062 as of the record's October 20, 2026 update. https://api.usaspending.gov/api/v2/awards/ASST_NON_NU17CE010210_7523/ (HigherGov, a secondary site, shows the first-year award as $5,339,590: https://www.highergov.com/grant/NU17CE010210 .) We did not find a CDC table of FY2023 or FY2024 awards for all states, so the per-state comparison below uses FY2025.
- **Comparison (our arithmetic, FY2025 table, Vintage 2024 populations):** West Virginia $5,339,590 / 1,769,979 = $3.02 per resident, 7th of 51. Higher: DC $5.62, Vermont $5.05, Alaska $3.64, Wyoming $3.32, Delaware $3.16, Rhode Island $3.10. Median $1.03 (state and local awards added together; North Dakota lists none). In dollars, West Virginia's state award is 4th, behind Florida ($5,823,539), Kentucky ($5,407,419) and Tennessee ($5,343,696).

### 2c. Opioid settlements

- **West Virginia's structure** (West Virginia First Memorandum of Understanding, dated February 16, 2022 in the file name): 72.5% of net funds to the West Virginia First Foundation, 24.5% to local governments, 3% to the state for litigation costs. If the 3% is not spent by December 31, 2026, 1% goes to local governments and 2% to the Foundation. https://wvfirst.org/wp-content/uploads/2025/09/2022.2.16-Final-MOU-Exhibits-REVISED-EX-C.pdf
- **Foundation founded and funded in 2023:** incorporated May 2023 (Foundation's 2025 local expenditure report, below). Its December 29, 2023 financial statement shows $217,500,000 from the West Virginia Qualified Settlement Fund, with $52,221 in expenses paid. https://wvfirst.org/wp-content/uploads/2025/08/First-Foundation-Financial-Statement-12-29-23.pdf
- **No grants paid through 2024:** the December 31, 2024 financial report shows the same $217,500,000 source, $12,453,736 in investment income since inception, $1,463,022 in total expenses (legal, accounting, payroll, insurance and similar), and no grant payments. Total funds $228,490,714. https://wvfirst.org/wp-content/uploads/2025/08/WVFF-December-2024-Financial-Report.pdf
- **First grants:** the board approved up to $19.2 million in September 2024 and announced $10.4 million to 38 recipients in December 2024, then $6.21 million more in March 2025. By June 30, 2025, about $8.72 million had been paid out (West Virginia Public Broadcasting, June 30, 2025; news source). https://wvpublic.org/story/health-science/with-8-7m-distributed-inaugural-opioid-settlement-grant-distribution-halfway-done/
- **Local governments:** "$73.5 million was distributed directly to Local Governments from the QSF in December 2023," and $24.5 million more in January 2025 (West Virginia First Foundation, 2025 Annual QSF Expenditure Report, covering July 1, 2023 to June 30, 2024, dated July 15, 2025). https://wvfirst.org/wp-content/uploads/2025/09/2025-Annual-QSF-Expenditure-Report_FINAL-JULY152025.pdf
- **Local spending through June 2024 (news analysis of that report, not checked line by line by us):** $72.8 million to 226 local governments; about 9.4%, roughly $6.9 million, reported spent; about $3.64 million (52%) went to law enforcement; quick response teams about $685,000 and EMS about $643,000; 144 localities reported no spending. Self-reported. West Virginia Watch, July 2025. https://westvirginiawatch.com/?p=11013 and https://westvirginiawatch.com/?p=11064
- **Our arithmetic on the fund total:** $217,500,000 / 0.725 = $300,000,000, and $73,500,000 / 0.245 = $300,000,000. So the December 2023 payout matches a $300 million draw from the settlement fund under the MOU shares. This is an inference from the shares; we did not find a document stating the $300 million total.
- **Expected total:** West Virginia Public Broadcasting (June 30, 2025) says "more than $1 billion" once paid out. The Cicero Institute (a policy group, September 2025) puts the total under the MOU at $683,233,660, with $505,787,265 to the Foundation and $395,387,846 received by the end of 2025. These two do not agree, and neither is a government source. https://ciceroinstitute.org/wp-content/uploads/2025/09/West%20Virginia%20Opioid%20Settlements%20Brief.pdf
- **Other West Virginia settlements:** a $99 million Janssen (Johnson & Johnson) settlement announced in April 2022 and a $10 million McKinsey settlement announced February 3, 2021 were both to flow through the MOU (WV MetroNews, April 19, 2022). https://wvmetronews.com/2022/04/19/west-virginia-has-a-99-million-settlement-in-hand-so-where-does-the-money-go
- **Why there is no cross-state table:** West Virginia settled separately from most of the national settlements, so it is not in the same rows of the National Opioid Settlements payment dashboard (https://nationalopioidsettlement.com/wp-content/uploads/2025/01/Opioid-Payment-Dashboard-1.1.25.pdf). KFF Health News has state-level 2022-2023 data, but the download is behind a sign-up form (https://kffhealthnews.org/download-the-data-opioid-settlement-expenditures), and KFF says reporting differences make comparisons "nearly impossible."
- **A rough national comparison (our arithmetic, treat with care):** KFF Health News says states and localities got "more than $6 billion" in 2022 and 2023. Over about 335 million people, that is roughly $18 per resident. West Virginia's December 2023 payout of $291 million over 1,770,495 residents is about $164 per resident. But KFF's figure is money received, while most of West Virginia's money was held, not spent, through 2024.

### 2d. Peer-reviewed or government studies comparing states

- McBain, Cantor, Kofner, Lindenfeld and Powell, "The Relationship Between Receipt of Opioid Settlement Funds and Reductions in Opioid Overdose Deaths in the U.S.," *AJPM Focus*, August 22, 2025, doi:10.1016/j.focus.2025.100424. State overdose death rates 2017-2023 and KFF settlement receipts 2022-2023. Each extra settlement dollar per resident was associated with a 0.99% larger decline in opioid overdose deaths in 2022 and 2.46% in 2023. States with higher 2017-2021 death rates received more per resident ($0.87 more per extra death per 100,000). It uses money received, not spent, does not cover 2024, and does not name West Virginia. https://pmc.ncbi.nlm.nih.gov/articles/PMC12547889/
- KFF reports that the largest state drops in opioid death rates from 2023 to 2024 were in Virginia, Wisconsin and West Virginia, about 44% to 46%. It does not tie this to funding. https://www.kff.org/mental-health/opioid-overdose-deaths-national-trends-and-variation-by-demographics-and-states/
- We found no peer-reviewed study that tests whether SOR, OD2A or total state spending explains the 2024 drop across states.

### 2e. West Virginia programs, 2022-2024

- **Naloxone, 2024** (WV Office of Drug Control Policy, "Report of Prescriptions and Distribution of Opioid Antagonists 2024," February 1, 2025): the Bureau for Behavioral Health, with the University of Charleston, shipped 98,628 naloxone kits in 2024, paid for from SOR, the substance use block grant and other SAMHSA grants. 15,270 kits went out on Save-a-Life Day (September 26, 2024). Third parties reported 25,831 more kits. Pharmacies dispensed 18,320 doses in 2024, down 8.5% from 20,020 in 2023. https://odcp.wv.gov/media/39688/download?inline
  - Our arithmetic: 98,628 kits / 1,769,979 residents x 100,000 / 12 months = about 464 kits per 100,000 residents per month. The same report cites a model threshold for "naloxone saturation" of 73.4 kits per 100,000 per month. We found no matching count for other states, so we cannot rank this.
- **Naloxone, 2023:** DHHR said it provided $600,000 worth of naloxone and 29,438 doses on Save a Life Day, September 2023 (release October 10, 2023). https://dohs.wv.gov/article/dhhr-announces-successful-distribution-naloxone-2023-appalachian-save-life-day . We did not find a full-year 2023 kit count.
- **Treatment in prisons, first half of 2024** (ODCP semiannual report, January-June 2024): the corrections department "provided 997 buprenorphine (subutex)" from January to June 2024 and gave medication for opioid use disorder to 35 people released in that period. https://odcp.wv.gov/media/39687/download?inline

## 3. Per-capita table: SOR allocations, all 50 states and DC

Sorted by FY2023 SOR per resident. SOR figures are SAMHSA allocations from the NOFOs above. Population is Census Vintage 2024, July 1, 2023. Fentanyl deaths are our T40.4 counts. "Change" is fentanyl deaths, 2023 to 2024.

**Arithmetic for West Virginia:** $45,855,881 / 1,770,495 = $25.90 per resident. $45,855,881 / 1,137 deaths = $40,331 per death. (587 - 1,137) / 1,137 = -48.4%.

For all 51: median FY2023 SOR per resident $4.08; median per death $20,906; national total (50 states and DC) $1,474,425,000 / 336,806,231 = $4.38 per resident, and / 72,776 deaths = $20,260 per death.

| Rank | State | SOR FY2022 | SOR FY2023 | SOR FY2024 | Pop. 2023 | FY2023 per resident | Fentanyl deaths 2023 | FY2023 per 2023 death | Change in deaths 2023 to 2024 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Delaware | $37,282,640 | $38,558,031 | $38,795,579 | 1,036,423 | $37.20 | 431 | $89,462 | -39.2% |
| 2 | District of Columbia | $24,138,227 | $24,964,125 | $25,158,059 | 687,324 | $36.32 | 343 | $72,782 | -30.3% |
| 3 | **West Virginia** | $44,335,111 | $45,855,881 | $45,758,863 | 1,770,495 | $25.90 | 1,137 | $40,331 | -48.4% |
| 4 | New Hampshire | $28,505,671 | $29,482,574 | $29,880,604 | 1,402,199 | $21.03 | 380 | $77,586 | -40.0% |
| 5 | Maryland | $51,378,523 | $53,156,857 | $53,133,365 | 6,217,062 | $8.55 | 2,060 | $25,804 | -35.9% |
| 6 | Ohio | $97,354,086 | $100,750,866 | $100,192,260 | 11,824,034 | $8.52 | 3,590 | $28,064 | -41.7% |
| 7 | Massachusetts | $57,638,812 | $59,645,936 | $59,506,350 | 7,066,568 | $8.44 | 2,012 | $29,645 | -37.8% |
| 8 | Kentucky | $35,912,100 | $37,159,328 | $37,207,506 | 4,550,595 | $8.17 | 1,475 | $25,193 | -39.6% |
| 9 | New Jersey | $66,745,336 | $69,072,536 | $68,764,571 | 9,379,642 | $7.36 | 2,196 | $31,454 | -31.6% |
| 10 | Rhode Island | $7,442,546 | $7,598,692 | $11,359,101 | 1,103,429 | $6.89 | 317 | $23,971 | -38.5% |
| 11 | Wyoming | $4,000,000 | $4,000,000 | $4,000,000 | 585,067 | $6.84 | 57 | $70,175 | -36.8% |
| 12 | Pennsylvania | $80,772,375 | $83,586,343 | $83,123,161 | 13,017,721 | $6.42 | 3,336 | $25,056 | -38.1% |
| 13 | Vermont | $4,000,000 | $4,000,000 | $5,989,474 | 648,708 | $6.17 | 220 | $18,182 | -24.1% |
| 14 | Alaska | $4,000,000 | $4,000,000 | $5,989,474 | 736,510 | $5.43 | 274 | $14,599 | -6.9% |
| 15 | Nevada | $16,719,861 | $17,307,529 | $16,629,170 | 3,214,363 | $5.38 | 710 | $24,377 | -4.9% |
| 16 | North Dakota | $4,000,000 | $4,000,000 | $4,000,000 | 789,047 | $5.07 | 76 | $52,632 | -46.1% |
| 17 | Maine | $6,325,323 | $6,547,645 | $9,790,828 | 1,399,646 | $4.68 | 489 | $13,390 | -28.6% |
| 18 | Florida | $101,280,912 | $104,840,723 | $104,258,643 | 22,904,868 | $4.58 | 4,593 | $22,826 | -37.4% |
| 19 | Arizona | $31,956,846 | $33,080,062 | $34,788,112 | 7,473,027 | $4.43 | 1,774 | $18,647 | -16.5% |
| 20 | Tennessee | $30,451,167 | $31,521,461 | $31,349,498 | 7,148,304 | $4.41 | 2,771 | $11,375 | -39.9% |
| 21 | Indiana | $29,141,538 | $30,165,802 | $30,264,193 | 6,880,131 | $4.38 | 1,587 | $19,008 | -33.1% |
| 22 | South Dakota | $4,000,000 | $4,000,000 | $4,068,870 | 918,305 | $4.36 | 42 | $95,238 | -28.6% |
| 23 | Missouri | $25,295,012 | $26,184,078 | $26,338,560 | 6,208,038 | $4.22 | 1,358 | $19,281 | -39.4% |
| 24 | Idaho | $7,936,034 | $8,214,969 | $7,832,433 | 1,971,122 | $4.17 | 215 | $38,209 | -35.8% |
| 25 | Oklahoma | $16,150,480 | $16,718,135 | $15,795,312 | 4,063,882 | $4.11 | 753 | $22,202 | -31.5% |
| 26 | Connecticut | $14,372,802 | $14,877,975 | $15,021,882 | 3,643,023 | $4.08 | 1,108 | $13,428 | -31.0% |
| 27 | Louisiana | $17,453,830 | $18,067,295 | $17,995,265 | 4,588,071 | $3.94 | 1,026 | $17,609 | -37.4% |
| 28 | Michigan | $36,844,904 | $38,139,924 | $36,363,911 | 10,083,356 | $3.78 | 2,145 | $17,781 | -45.2% |
| 29 | Oregon | $15,470,977 | $16,014,749 | $15,271,666 | 4,253,653 | $3.76 | 1,272 | $12,590 | -23.3% |
| 30 | New Mexico | $7,617,237 | $7,884,967 | $11,786,253 | 2,121,164 | $3.72 | 651 | $12,112 | -35.5% |
| 31 | Colorado | $21,073,833 | $21,814,534 | $20,798,725 | 5,901,339 | $3.70 | 1,146 | $19,035 | -30.5% |
| 32 | Arkansas | $10,880,435 | $11,262,860 | $10,647,596 | 3,069,463 | $3.67 | 268 | $42,026 | -46.6% |
| 33 | Washington | $27,475,037 | $28,440,727 | $27,116,364 | 7,857,320 | $3.62 | 2,655 | $10,712 | -13.5% |
| 34 | Montana | $4,000,000 | $4,000,000 | $4,342,525 | 1,131,302 | $3.54 | 99 | $40,404 | -21.2% |
| 35 | South Carolina | $18,138,356 | $18,775,881 | $18,791,695 | 5,387,830 | $3.48 | 1,563 | $12,013 | -40.5% |
| 36 | North Carolina | $35,539,042 | $36,788,164 | $36,604,318 | 10,881,189 | $3.38 | 2,745 | $13,402 | -28.6% |
| 37 | Virginia | $27,947,054 | $28,929,334 | $27,332,465 | 8,734,685 | $3.31 | 1,954 | $14,805 | -45.8% |
| 38 | Alabama | $16,264,369 | $16,836,028 | $16,176,149 | 5,117,673 | $3.29 | 1,100 | $15,305 | -33.0% |
| 39 | Utah | $10,839,983 | $11,220,985 | $10,698,472 | 3,443,222 | $3.26 | 337 | $33,297 | -9.8% |
| 40 | Illinois | $37,187,828 | $38,494,902 | $36,702,359 | 12,642,259 | $3.04 | 2,651 | $14,521 | -37.0% |
| 41 | New York | $56,858,435 | $58,856,889 | $56,116,176 | 19,737,367 | $2.98 | 4,936 | $11,924 | -38.2% |
| 42 | Wisconsin | $16,913,533 | $17,508,010 | $17,784,023 | 5,930,405 | $2.95 | 1,309 | $13,375 | -45.7% |
| 43 | Kansas | $8,368,788 | $8,662,933 | $8,323,394 | 2,951,500 | $2.94 | 355 | $24,403 | -17.5% |
| 44 | Iowa | $9,081,141 | $9,400,324 | $8,962,591 | 3,218,414 | $2.92 | 208 | $45,194 | -39.9% |
| 45 | California | $107,038,177 | $110,800,343 | $105,640,843 | 39,198,693 | $2.83 | 7,203 | $15,383 | -32.8% |
| 46 | Hawaii | $4,000,000 | $4,068,210 | $4,000,000 | 1,441,387 | $2.82 | 113 | $36,002 | -7.1% |
| 47 | Georgia | $29,600,797 | $30,641,202 | $28,949,840 | 11,064,432 | $2.77 | 1,678 | $18,261 | -34.7% |
| 48 | Mississippi | $7,241,395 | $7,495,915 | $7,097,094 | 2,943,172 | $2.55 | 449 | $16,695 | -41.9% |
| 49 | Nebraska | $4,491,855 | $4,649,735 | $4,588,329 | 1,987,864 | $2.34 | 61 | $76,225 | -19.7% |
| 50 | Minnesota | $11,354,964 | $11,754,067 | $11,293,373 | 5,753,048 | $2.04 | 935 | $12,571 | -35.2% |

## 4. What could not be found or verified

- **Actual SOR spending by state.** The tables above are the most each state could apply for. USAspending's SOR (CFDA 93.788) obligations by state add up to only $144 million for FY2022 and $230 million for FY2023, far below the $1.4 billion program, so that data is incomplete and we did not use it. TAGGS (taggs.hhs.gov) was not checked. How much of each year's SOR money West Virginia spent, and on what, is not known from these sources.
- **Substance use block grant by state.** SAMHSA's FY2023 allotment page could not be found (404). The block grant formula uses population at risk, cost of services and fiscal capacity, not overdose deaths. USAspending's block grant data by state also looked incomplete, so no block grant comparison is given.
- **OD2A by state for FY2023 and FY2024.** Only the FY2025 table for all states was found. West Virginia's own award appears to be the same each year, but we did not confirm that for other states.
- **Settlement money by state, received and spent.** No primary source gives every state's total in a form that includes West Virginia. KFF Health News's state data is behind a sign-up form. The West Virginia First Foundation's 2025 Annual Report is a scanned PDF too large to read here. The $300 million settlement fund total is our inference from the MOU shares. The news figures on local spending ($6.9 million, 52% law enforcement) were not checked line by line against the Foundation's report.
- **Total state overdose spending, all sources.** We found no federal or peer-reviewed source that adds up federal grants, settlements, Medicaid and state money by state. So we cannot say whether West Virginia spent more in total than other states.
- **Medicaid.** West Virginia expanded Medicaid in 2014 (widely reported; not checked against a primary source this session). We did not find state-by-state Medicaid spending on opioid use disorder treatment for 2022-2024. CMS's T-MSIS substance use data book may have counts of treated enrollees by state; not checked.
- **Treatment and naloxone in other states.** We found West Virginia's 2024 naloxone counts but no matching state-by-state counts, so we cannot rank West Virginia. We found no source for buprenorphine or methadone patients per resident by state for 2023-2024.
- **CDC's state funding page** refused a plain download; it was read through a web fetch tool, which summarized it. The OD2A figures were taken from that summary and should be checked on the page before publishing.

## 5. Bottom line for the editor

West Virginia did get much more federal SOR money per resident than nearly every state, before and during 2023-2024, because the federal formula gives more to states with more overdose deaths and higher death rates. Per death, it was above the median but not near the top. Its OD2A award was also high per resident but small in dollars. Its settlement money was mostly held, not spent, until 2025. Other states with similar SOR funding per resident had drops near the national median, so SOR money per resident alone does not set West Virginia apart. These sources cannot say whether funding caused any part of West Virginia's drop.
