# Data

| Folder | Contents | Status |
|---|---|---|
| `raw/` | `<year>_mega.csv`: UN Comtrade exports (partner = World). Rows are HS 6-digit commodity codes (`cmdCode`), columns are reporter country codes. 2019–2023. | current |
| `cleaned/` | `<year>clean.csv`: 1 row per country, 19 columns (`Country` + 18 industry groups), current US$. 2019–2023. Identical to `archive/2024-fall/2019-2023 cleaned/`. | current |
| `archive/2024-fall/` | `2019-2023 cleaned/` (what the notebook reads), `GDP_2022.csv`, `GDP_2023.csv` | current |
| `archive/2023-fall/` | 2019–2022 cleaned set, GDP, raw data, sensitivity/contingency outputs | archive |
| `archive/2022-fall/` | 2019–2021 set, `Country_Code.csv` (Comtrade code → name, **still used by the cleaning notebook**), retrieval notebooks, contingency tables | archive |
| `archive/2020-spring/` | 2013–2019 data, raw retrieval zip, the first scripts | archive |
| `results/greedy-pickles/` | `<Country>_<year>_percentage<N>_part[30, 60, 90, 120].p`: greedy optimizer outputs (2022–2023) | reference |
| `results/sdv-sids/` | `sdv_and_sids<Country>.txt`: sequential development strategy logs, about 50 countries | reference |
| `results/misc/` | Loose sensitivity/contingency tables (Japan, Mauritania, Senegal), UK 2023 greedy pickles, SOI CSVs | reference |

## Data dictionary
**`<year>clean.csv`**
| Column | Type | Notes |
|---|---|---|
| `Country` | str | Comtrade name. The notebook renames some (e.g. `Viet Nam`→`Vietnam`). See `docs/KNOWN-ISSUES.md` D6. |
| 18 industry columns | float, US$ | `Animals and By-products`, `Vegetables, Fruits and Plants`, `Food and Preparations`, `Energy Drilling and Mining`, `Chemicals`, `Chemical Manufacturing`, `Raw Manufacturing`, `Wood Products`, `Clothing and Accessories`, `Textile`, `Metals`, `Machinery and Construction`, `Transportation`, `Weapons`, `Daily Instruments`, `Precious Stones\t` (**trailing tab**), `High-complexity Products`, `Services and Utilities` |

HS-chapter → group mapping: `docs/methodology.md#industry-groups`.

**`GDP_<year>.csv`** (World Bank WDI): `Series Name` ("GDP (current US$)"), `Country Name`, `Country Code`, then one column per year from 1990.

**Greedy pickles**: `pickle.load` returns the `two_step_greedy()` result: `[0]` = allocation by industry, `[2]` = ECI increments.

## Quality flags
Read `docs/KNOWN-ISSUES.md` (D1–D6) before relying on cross-year ECI comparisons.

## Sources
- UN Comtrade: <https://comtradeplus.un.org/> (API: `comtradeapicall`, key in `.env`)
- World Bank GDP (current US$): indicator `NY.GDP.MKTP.CD`
