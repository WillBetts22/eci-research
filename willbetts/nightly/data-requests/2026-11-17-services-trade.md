# Data request / data issue: the "Services and Utilities" column is not services

Found by `runs/2026-11-17_P-2026-11-17-1-services-column/notebook.ipynb` (nightly 2026-11-17).

## The issue
- In `data/cleaned/<year>clean.csv`, the column `Services and Utilities` is built from HS chapter 99 (`datacleaning2025.ipynb`: `"Services and Utilities":[99]`). In `data/raw/<year>_mega.csv`, chapter 99 has exactly one HS6 code, **999999**: Comtrade's *commodities not specified according to kind*. These are goods reported without a product code, often for confidentiality.
- With 999999 included, the repo's totals match WDI **merchandise** (goods) exports (median |log ratio| 0.0015 in 2019, against 0.0123 without it). So the column is goods, not services.
- `docs/methodology.md` and Table 1 of every report describe it as "Financial, business, legal, communication, travel". That description is wrong for the data we actually use.
- The `get_service()` EB02 services pull in `code/data-retrieval/Data_Retrieval_2025.ipynb` never reaches `data/raw` or the cleaned CSVs.
- The drop-any-zero rule removes 14–25 countries a year only because this column is zero, including Thailand every year and the Philippines in 2019–2021.

## What Will needs to decide
1. Drop the column from the ECI input (recommended; the income fit is unchanged, mean Δ Spearman +0.004 over 2019–2022), **or**
2. Rename it to "Unspecified goods (HS 999999)" and keep it, **or**
3. Replace it with real services exports (below).

## External data (only if option 3)
- **Dataset:** UN Comtrade services (EBOPS 2010, `typeCode='S'`, `clCode='EB'`), total services exports (code `S`/`200`), flow X, partner World. Alternative: WTO–OECD BaTiS or WTO–UNCTAD–ITC annual trade in services.
- **Source:** https://comtradeplus.un.org/ (API: `comtradeapicall.getFinalData(..., typeCode='S', ...)`), https://www.wto.org/english/res_e/statis_e/gstdh_oecd_wto_bal_trade_serv_e.htm
- **Variables:** reporter ISO3, year, total services exports (current US$). Optionally the EBOPS main components (transport, travel, ICT, financial, other business) for a few service "products".
- **Years:** 2019–2023 (2024 with the next data update).
- **Why:** with a services column, the grouped ECI would match its own description, and Singapore, the UK and the UAE could be scored on services.

## Also noted
- Kuwait (2021) and Saudi Arabia (2022) are absent from the cleaned CSVs entirely, which removes UAE peers.
- Saudi Arabia's goods exports are 80.4% HS 999999 in 2019, so any analysis that drops chapter 99 (all HS4 work) treats Saudi Arabia as a much smaller, non-oil exporter.
