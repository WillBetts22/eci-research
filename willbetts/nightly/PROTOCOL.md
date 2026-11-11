# Nightly ECI Research Protocol

This is the procedure the nightly cloud agent follows. Edit it on `main` to change how the agent behaves. The agent reads the version on `main` each night.

**Goal:** answer **one** small, well-scoped question each night about how to improve the lab's ECI. Write the result up as an executed notebook, and open a PR for Will to review in the morning.

Background, which the agent must read every night:
- `willbetts/research-agenda.md`: the full map of questions
- `willbetts/ECI_growth_prediction.md`: the growth-prediction projects
- `docs/methodology.md`: the lab's ECI exactly as implemented
- `docs/KNOWN-ISSUES.md`: data and notebook bugs (D1–D6, N1–N9)
- `maitreemody/outputs/findings.md` and `juliawang/outputs/findings.md`: teammates' results. Build on them; don't redo them.
- Every past run in `willbetts/nightly/runs/` on `main` (read each notebook's summary cell)

---

## 1. Pick tonight's question

1. Run `git fetch origin '+refs/heads/claude/nightly-*:refs/remotes/origin/claude/nightly-*'`. Then list the run folders on `main` and on every open `claude/nightly-*` branch. A question is **taken** if any run folder names its ID.
2. Take the **highest untaken question in `QUEUE.md`** (the order is the priority).
3. If the top question is blocked by missing data (it is marked `needs-data`, or you find it is), skip it and say so in the PR.
4. If the queue is exhausted, pick the most valuable idea from `proposals/` and use ID `P-<date>-<n>`.
5. Scope it so it fits in about **90 minutes of compute and work**. If it is bigger, do a first slice tonight and propose the rest.

## 2. Branch

- Always branch from `origin/main`: `claude/nightly-YYYY-MM-DD` (use America/New_York date of the morning the PR is for).
- Every night writes **only new files** under `willbetts/nightly/` so PRs never conflict with each other:
  - `runs/YYYY-MM-DD_<QID>-<slug>/notebook.ipynb` (required)
  - `runs/YYYY-MM-DD_<QID>-<slug>/figures/*.png` and small `*.csv` outputs (optional, under 2 MB total)
  - `proposals/YYYY-MM-DD.md`: new research avenues found tonight (optional)
  - `data-requests/YYYY-MM-DD-<slug>.md`: data problems or external data needed (optional)
- **Do not edit** `QUEUE.md`, `PROTOCOL.md`, or any existing file. Will owns them. Never touch anything outside `willbetts/nightly/`, any `archive/` folder, or other members' folders.
- Shared helpers: if `willbetts/nightly/lib/eci.py` exists on `main`, import it. Otherwise define helpers inside the notebook. Create or modify `lib/` only when the question is specifically about it (Q01 creates it).

## 3. Do the research

- Data in the repo: `data/raw/<year>_mega.csv` (HS6 by exporter code, 2019–2023), `data/cleaned/<year>clean.csv` (the lab's 18 groups; note the `"Precious Stones\t"` header), `data/archive/2024-fall/GDP_2023.csv` (nominal total GDP), and `maitreemody/outputs/worldbank_gdp_per_capita_2019_2023.csv` (GDP per capita, PPP and USD, with ISO3).
- Set up with `pip install -q -r requirements.txt pycountry tabulate jupyter nbconvert`.
- **No external data downloads.** If a question needs outside data (Atlas ECI, Penn World Table, BACI, WDI controls, population), do what you can without it. Then write a `data-requests/` file with the exact dataset, source URL, variables, years, and why it's needed. Will gets it.
- Always orient the ECI sign so that it correlates positively with diversity (the lab's `compute_eci` can flip; see Maitree's findings).
- Merge on ISO3 where possible, not on names (KNOWN-ISSUES D6).
- Treat 2023 as suspect (D1). Use 2019 as the primary year unless the question is about time.
- Pre-state the metric and the baseline before you try variants (research-agenda section 5). Report **every** variant you tried, not just the winner.
- Don't run the greedy optimizer (15–30 min per budget level). Propose it instead if it's needed.

## 4. Write the notebook

It must be executed in place with outputs saved: `jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 <path>`. Keep it under about 3 MB: no giant tables, and save figures at a modest DPI.

Required structure (markdown cells):
1. **Header**: question ID and text, date, data files and years used, run time.
2. **TL;DR** (3–5 bullets): what we learned, with the key numbers.
3. **Why this matters for the lab**: which link it tests (ECI predicts growth / is causal / the optimizer's target is sound), or which part of our implementation it improves.
4. **Method**: pre-stated metric and baseline, then the variants.
5. **Results**: code, tables, figures. Each one gets a one-line takeaway.
6. **Caveats**: sample size, short windows, nominal values, D1–D6 issues that touch this result.
7. **Helpful to know**: gotchas or facts about the data and code that future work should know.
8. **New research avenues**: concrete follow-ups, each scoped to one night. Copy them into `proposals/YYYY-MM-DD.md` too.
9. **Data issues / data needed**: anything found, linked to the `data-requests/` file.

Every number in prose must come from a cell output in the same notebook. Never estimate or invent values. If something failed, say so plainly.

## 5. Open the PR

- Commit with a message like `Nightly research Q03: fixed country panel vs per-year ECI`, then push the branch.
- Open a PR **into `main`**, titled `Nightly research YYYY-MM-DD — <QID>: <short question>`.
  - Try `gh pr create` first. If `gh` isn't available or authenticated, use the GitHub REST API with whatever token the environment provides. If neither works, push the branch and put the compare URL `https://github.com/WillBetts22/eci-research/compare/main...<branch>?expand=1` in your final message.
- PR body:
  ```
  ## Question
  ## TL;DR
  ## Key numbers (table)
  ## Helpful to know
  ## New avenues proposed
  ## ⚠️ Needs your input — data issues / external data requests   (write "None" if none)
  ## Files
  ```
- Don't merge. Will reviews and merges.

## Hard rules
- No PII, and no secrets or API keys.
- Don't edit `archive/` folders or other members' work.
- One question per night. Being honest about a null result beats overclaiming.
