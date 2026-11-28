# Angola: HS ch. 89 missing from the cleaned *Daily Instruments* cell (2019–2021)

Found by: `runs/2026-11-28_P-2026-11-28-1-dd-plus-f1/notebook.ipynb`, Setup cell 2.

## What we see
| Year | Cleaned *Daily Instruments* (`data/cleaned/<year>clean.csv`) | Raw ch. 89 (`data/raw/<year>_mega.csv`) | Raw ch. 89–95 (the lab mapping rebuilt from raw) |
|---|---|---|---|
| 2019 | $39.1M | $351.5M | $382.7M |
| 2020 | $23.8M | $950.4M | $966.7M |
| 2021 | $25.1M | $1,166.1M | $1,210.2M |

The cleaned cell is roughly the raw total *without* ch. 89 (ships, floating/drilling platforms). In 2022 and 2023 the two sources agree. Angola is the only country where raw ch. 89 exceeds the cleaned cell in any year.

## Why it matters
- It is one more cleaned-vs-raw gap of the Q05 kind. These gaps are why grouped-ECI verdicts differ between the cleaned base and the rebuilt base (11-27, 11-28).
- Ch. 89 is the chapter F1 remaps, and 11-24 found oil-sector vessels and platforms there for Nigeria and Congo. Angola's HS6 breakdown was not checked tonight. Whether ch. 89 should count at all is a mapping question (F1). Whether it is *present* is a data question.

## What's needed (data team / Will)
1. Check `code/data-retrieval/datacleaning2025.ipynb` for why Angola's ch. 89 lines didn't reach the 2019–2021 cleaned files. Was it a different pull, an HS-revision filter, or a dropped reporter-year?
2. No external data needed. This is internal to the repo's pull and cleaning.
