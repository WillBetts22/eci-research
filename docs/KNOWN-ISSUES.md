# Known Issues & Gotchas

Compiled 2026-10-17 from the notebook's own `TO FIX` comments, a test run of `code/current/Spring2026.ipynb` (Vietnam, Section 1) through `scripts/run_notebook.py`, and a scan of the data. Add to this list whenever you hit something.

## Data quality flags (data team, please investigate)
These were observed but their root causes are **not yet verified**.

| # | Observation | Why it matters |
|---|---|---|
| D1 | **2023 total exports sum to about $45T**, vs. about $23–31T for 2019–2022. Real world goods + services exports are about $31T. | Possible double counting in the 2023 pull or cleaning, e.g. HS chapters 28/29/30/38/83/84/87/92/99 count toward both their own group and *High-complexity Products*. That overlap is intentional, but check that 2023 wasn't cleaned differently. |
| D2 | **Country coverage varies by year**: 161 / 155 / 137 / 142 / 155 rows for 2019–2023, and only 106–123 rows have nonzero exports in *every* group. | `df_to_matrix` drops any country with a zero in any group, so peers can vanish for some years. In the test run, the Philippines had no ECI for 2019–2021. |
| D3 | In the test run, **all countries' ECI dropped sharply from 2020 to 2021**, and Singapore came out far below its usual ranking. | It is likely tied to D2: the set of countries in the eigenvector calculation changes each year. Compare ECI only across years with the same country set, or flag this in the report. |
| D4 | The HS-chapter mapping in `datacleaning2025.ipynb` puts chapter **84** (machinery) only in *High-complexity Products*, while *Machinery and Construction* = chapter 83 only, and chapter **85** (electrical machinery) sits in *Transportation*. | It looks unintended. Review it against the Table 1 descriptions before the next data update. |
| D5 | The cleaned CSV header `"Precious Stones\t"` has a trailing **tab**. | The code depends on it. Don't "fix" it in one place only. |
| D6 | Country names differ between files. The notebook's rename cell maps e.g. `Viet Nam`→`Vietnam`, `Republic of Korea`→`South Korea`, `USA, Puerto Rico and US Virgin Islands`→`USA`. | **Always use the notebook's names** (`Vietnam`, `USA`, …) in the config. `run_notebook.py` checks this for you. 27 export-data names have no GDP match (e.g. `Turkey`, `Egypt`, `Slovakia`, `Gambia`). Add renames if your country is one of them. |

## Notebook bugs (`code/current/Spring2026.ipynb`)
| # | Where | Problem | Workaround |
|---|---|---|---|
| N1 | `#20 aagrate()` | Divides the sum of yearly growth rates by `len(nums)` (5 values → 4 intervals), so average growth is **understated by about 20%**. The notebook notes "not CAGR". | Report it as computed (for consistency with past reports) but note the method, or fix it to `/ (len(nums)-1)` for *all* countries in a semester. |
| N2 | Cell after `#29` | `gdp_and_eci_graph()` returns `tags`, but the code defining `tags` is commented out → `NameError`. | The **figure is still saved** before the error, so it's harmless. To silence it, delete `return tags`. |
| N3 | SOI w/ ADI cells | "I made this run without crashing but it's still wrong." In the test run, the SOI regression used `nobs = 5`, and the contrast country was the main country itself. | Treat the SOI quartile and contrast country as **unverified** until fixed. QA should check `[nobs]` (the Thailand 2025 run had 116). |
| N4 | Greedy `#67`–`#71`, Plot `#145`/`#147` | Hardcode `year = 2022` while `end_year = 2023`. | `run_notebook.py` sets them to `--greedy-year` (default: end year). In Colab, edit by hand. |
| N5 | `#65 greedy_stablizer()` | Never called, and it passes `(percentage, part)` in the wrong argument order. | Ignore it. |
| N6 | `#72` | The portfolio table export is marked `TO FIX`. | Use the older "MD 3 Plot Budget Allocation" notebook in `code/archive/2023-fall/`. |
| N7 | Sensitivity `#160` | Reads `5. Datasets/2023 Fall - Data/2019-2023 cleaned/`, which doesn't exist on Drive. | Point it at `2024 Fall - Data/2019-2023 cleaned/`. `run_notebook.py` handles this. |
| N8 | Many cells | `!pip install plotly==5.3.1` / `kaleido==0.2.1` pins | Locally, use `requirements.txt`. kaleido must stay at **0.2.1** for `write_image`. |
| N9 | Default config | `main_country = "Vietnam"` is left over from the last run | Always set your own country. |

## Process gotchas
- **Copy-paste errors** are the #1 QA failure: the wrong country name in a caption after copying a previous report.
- The **greedy optimizer takes 15–30 minutes per budget level**. In Colab, keep the tab open or the runtime disconnects.
- **Auto-report images must be public** in Drive for the Apps Script `replaceImage` call to work.
- Binary files (`.pptx`, `.docx`) **can't be merged** in git. Coordinate edits to the consolidated deck.
- `data/cleaned/` and `data/archive/2024-fall/2019-2023 cleaned/` hold the same 2019–2023 files. The notebook reads the archive path.
