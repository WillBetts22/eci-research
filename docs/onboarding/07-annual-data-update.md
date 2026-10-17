# 07 · Annual Data Update (data team)

Do this once a year, when a new year of UN Comtrade data is available. Comtrade data typically lags 1–2 years. **Next due: add 2024 data** (current cleaned data covers 2019–2023).

> `/data-update 2024` runs the `data-engineer` agent through this checklist and validates the output.

## 1 · Retrieve Comtrade exports
Notebook: [`code/data-retrieval/Data_Retrieval_2025.ipynb`](../../code/data-retrieval/)
1. Get a UN Comtrade API subscription key at <https://comtradedeveloper.un.org/>. Put it in `.env` as `COMTRADE_API_KEY=...`. **Never commit it.** Replace the `"<COMTRADE_API_KEY>"` placeholder in `get_export()` with `os.environ["COMTRADE_API_KEY"]`.
2. Run the notebook **locally**, not in Colab: it makes about 150 API calls with 10-second sleeps, so expect about 30+ minutes.
3. Put `Country_Code.csv` (from `data/archive/2022-fall/Country_Code.csv`) next to the notebook.
4. Set `year_list = np.array([<new year>])`
5. Run all → one `<reporter_code>.csv` per country → `merge_all()` → `<year>_mega.csv`
6. Add the services column (`get_service`)
7. Move `<year>_mega.csv` → `data/raw/`

## 2 · Clean into 18 industry groups
Notebook: [`code/data-retrieval/datacleaning2025.ipynb`](../../code/data-retrieval/)
- Reads `<year>_mega.csv`, transposes it to countries × HS codes, maps reporter codes to names with `Country_Code.csv`, and sums **HS 2-digit chapters** into the 18 groups (mapping in [../methodology.md#industry-groups](../methodology.md#industry-groups))
- Output: `<year>clean.csv` → `data/cleaned/` **and** a new semester snapshot `data/archive/<semester>/2019-<year> cleaned/`

## 3 · GDP
Download **GDP (current US$)** for all countries from the World Bank (WDI) → `GDP_<year>.csv` with columns `Series Name, Country Name, Country Code, 1990 … <year>`. Put it in the semester snapshot folder.

## 4 · Validate
- [ ] `<year>clean.csv` has about 150+ rows and exactly the 19 columns (`Country` + 18 groups)
- [ ] No all-zero rows. Check against last year: countries that dropped out?
- [ ] Country names match last year's file (diff the `Country` column). Renames break the notebook silently.
- [ ] Spot-check 3 countries' totals against the Comtrade website
- [ ] GDP file covers every country in the clean file (or document the gaps)

## 5 · Update the notebook for the new year
From [`docs/original-instructions/Semesterly Update Instructions.docx`](../original-instructions/). Let **X** = the new year and **#** = its index (2019 = 1, so 2024 = 6):

| Cell | Change |
|---|---|
| `#1` | `folder`, `data_folder`, `GDP4_path`, `sdv_path`, `end_year = X` |
| `#5` | add `df# = pd.read_csv(path_to_data + data_folder + '/Xclean.csv')` |
| `#6` | add `matrix#` and update the dataframe list |
| `#10` | `gdp_df_filtered` columns and the print statement |
| `#18` | add `eci_X` |
| `#19` | `eci_list` (the variable is still called `eci_19to21_dict`; leave the name) |
| `#49` | GDP file path `GDP_X.csv` |
| Greedy `#67`–`#71`, Plot `#145`/`#147` | `year = X` |

Save the updated notebook as `code/current/<Semester>.ipynb` and move the previous one to `code/archive/<semester>/`.
