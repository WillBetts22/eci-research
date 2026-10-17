# 04 · Running the Code

**Notebook:** [`code/current/Spring2026.ipynb`](../../code/current/Spring2026.ipynb), with 168 cells in 4 sections. Cells carry `#N` comment numbers that match the semesterly update instructions. Search the notebook for `TO DO` to find every line you're expected to edit.

> Read [../KNOWN-ISSUES.md](../KNOWN-ISSUES.md) first. A few cells are flagged `TO FIX` and have known workarounds.

## Section 1 · Comprehensive (cells 0–95)

### Config cell (`#1`): the only cell you must edit
```python
folder      = "2024 Fall - Data/"        # semester data folder
data_folder = "2019-2023 cleaned"         # <year>clean.csv files
main_country = "Vietnam"                  # ← YOUR COUNTRY (exact name as in the CSV)
comparable_countries   = [main_country, 'Singapore', 'Malaysia', 'Philippines']  # ← same peers as last report
sdv_emerging_countries = ["China", "Singapore"]          # emerging economies for RID/SDV table 4b
sdv_leading_countries  = ['France', 'Greece', 'Portugal'] # leading economies for table 4a
sdv_comparable_countries = [main_country, 'Greece', 'Poland', 'Portugal', 'France']
begin_year, end_year = 2019, 2023
AUTO_REPORT_PATH = "/content/drive/My Drive/ECI Auto Report Demo"   # where JSON + img/ are written
category = "developed"                    # or "emerging"
```
**Check the country name:** `grep -c "^<Country>," data/cleaned/2023clean.csv` should print `1`.

### Then run in order
| Cells | Part | Save / record |
|---|---|---|
| `#3`–`#10` | Import packages & data, fix missing GDP | If your country's GDP is missing for a year, patch it in `#10` (see the UAE example) |
| `#11`–`#16` | **Mcp, Mcc, Mpp, ECI, PCI** | — |
| `#17`–`#19` | ECI dictionaries per year | 2019–2023 ECI for the main country and peers |
| `#20`–`#24` | **GDP peer comparison** (Figure 1) + average annual growth | GDP growth % → `[GDP growth rate]` |
| `#25` | **ECI peer comparison** (Figure 2) | — |
| `#26`–`#27` | ECI change table | ECI change for the 4 countries |
| `#29` | **GDP + ECI trend** for the main country (Figure 3) | — |
| `#30`–`#34` | Proximity, distance, **RID** (Table 3) | # of industries with positive RID |
| `#35`–`#37` | RID vs. leading (4a) / emerging (4b) economies | — |
| `#38`–`#40` | **Opportunity gain** → SDV (Tables 5–6) | — |
| SDV & SIDS `main()` | Sequential vectors for each country | Download the sequential-vector `.xls`; combine your 4 countries into one table, add an ECI row at the bottom |
| `#42`–`#46` | **SOI** | Regression R² and adjusted R² (Figure 9) |
| SOI w/ ADI | SOI rank & quartile, contrast country (Figure 10) | `[SOI quartile]`, `[SOI]` |
| **"IMPORTANT. RUN THIS TO SAVE JSON."** | Writes `<Country>.json` | **Don't skip this.** The auto-report needs it. |

The notebook ends Section 1 with `assert(False)` so that "Run all" stops there. That's intentional.

## Section 2 · Greedy budget allocation (cells 97–130)  slow
1. `#53`: set `path` to a `New_result_update/` folder in **your** Drive (or `data/results/greedy-pickles/` locally)
2. Run the metrics cells `#55`–`#63` as-is
3. Run `#67` (5%), `#69` (10%), `#70` (15%), `#71` (20%). **Each takes about 15–30 minutes.** Each one writes `<Country>_<year>_percentage<N>_part[30, 60, 90, 120].p`.
   -  These cells hardcode `year = 2022`. Set it to `end_year` (2023) unless you're intentionally matching an older report. See KNOWN-ISSUES.
   - Run them in the background (Colab: keep the tab open; locally: `jupyter nbconvert --execute` or let the agent run it).

## Section 3 · Plot budget allocation (cells 131–150)
- Set the country in `#72`, then run all
- Save: **pie charts** (Figure 4), **ECI growth/increment chart**, and the **portfolio table** (`tableau <Country> <year>.xls` → Table 8)
- Portfolio table formatting: scientific notation, merged/centered headers, dark-blue border cells, light-blue body

## Section 4 · Sensitivity (cells 151–167)
- Make sure `raw_matrix` is read from the **latest** `<year>clean.csv`
- Save **Positive Shocking** and **Negative Shocking** plots (Figures 6a/6b)
- Run `sensitivity_new(raw_matrix, main_country, "High-complexity Products", root_path)` and `... "Clothing and Accessories" ...` to get the SDV-sensitivity tables. Colour coding: dark blue is positive, white is 0, light blue is negative.
- Run `cont(main_country, raw_matrix, root_path)` → `<Country>_contingency.xlsx`. Center and bold it.
- The "Navia edited automation" cell writes `[Industry 4–6]`, `[Pos Trend]`, `[Neg Trend]` into the JSON

## Auto-report image IDs
The Apps Script swaps template images by alt-text title. The notebook saves each figure under the matching ID:

| File in `img/` | Report figure/table |
|---|---|
| `kix.2h1zoxev3wer.png` | Figure 1: GDP comparison among peers |
| `kix.we5usefgy5tx.png` | Figure 2: ECI comparison among peers |
| `kix.kwwogf42gcjl.png` | Figure 3: GDP growth & ECI trend |
| `kix.fjnsupcfly3m.png` | Table 3: Realized Industry Development |
| `kix.hntjod878mme.png` | Tables 5/6: SDV / opportunity-gain ranking |
| `kix.qkzmpvrz2v9z.png`, `kix.u68suuv7ge1c.png` | Figure 4: greedy pie charts / ECI increments |
| `kix.lg1dve7hm257.png` | Table 8: portfolio |
| `kix.muhorlhdgh4f.png`, `kix.x2pl31md3ani.png` | Figures 6a/6b: sensitivity (positive / negative) |
| `kix.cqwj8nwgoqtv.png` | Figure 9: GDP growth vs. SOI regression |
| `kix.lcc2qvnzl4s3.png` | Figure 10: SOI of the country |

A complete real example is in [`reports/2025-fall/Thailand/(Correct Folder) ECI Auto Report Test/`](../../reports/2025-fall/Thailand/).

## JSON keys the notebook produces
`[Country] [Category] [Start Year] [End Year] [GDP growth rate] [GDP growth quality] [Relative GDP growth quality] [ECI growth quality] [increased/decreased] [Industry development] [SOI] [SOI quartile] [SOI quality] [SOI Contrast Country] [SOI Contrast] [SOI Contrast GDP] [R^2] [R^2 adj] [F-Stat] [Prob] [nobs] [Industry 1–4] [Pos Trend] [Neg Trend] [Overinvested] [Underinvested] [Overall quality] [Strategy quality]`

Placeholders in the template that the notebook does **not** yet fill (e.g. `[Peer 1–3]`, `[ECI start]`, `[ECI end]`, `[POS RID END]`, `[Top industry 5pct]`, `[SDV Leading 1–3]`) must be filled by hand or by the `report-writer` agent from the notebook output.
