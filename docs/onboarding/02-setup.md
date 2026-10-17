# 02 · Setup

You can run the notebook in **Google Colab** (the way the lab has always done it) or **locally** from this repo. Colab is easier for a first run. Local is better if you're using the agent team.

## Option A: Google Colab (recommended for first run)
1. In Google Drive, add a **shortcut** to the shared `ECI Research` folder into your *My Drive* (right-click → *Organize → Add shortcut*). The notebook expects `/content/drive/My Drive/ECI Research/...`.
2. Open `code/current/Spring2026.ipynb` in Colab: *File → Upload notebook*, or open the copy in Drive under `4. Code Files/10. 2026 Spring/`.
3. Run the first cell (`drive.mount`) and authorize.
4. Edit the **config cell** (cell `#1`); see [04-running-the-code.md](04-running-the-code.md).

**Drive ↔ repo path map**, for when Drive paths in old instructions don't match this repo:

| Drive (old) | Repo (new) |
|---|---|
| `1. Instructions - Onboarding/` | `docs/original-instructions/` |
| `2. Templates/` | `templates/` |
| `3. Country Reports/<n>. <Year> - <Term>/` | `reports/<year>-<term>/` |
| `4. Code Files/10. 2026 Spring/` | `code/current/` |
| `4. Code Files/<n>. <sem> - Code/` | `code/archive/<sem>/` |
| `4. Code Files/Data Retrieval/` | `code/data-retrieval/` |
| `5. Datasets/raw data/` | `data/raw/` |
| `5. Datasets/cleaned data/` | `data/cleaned/` |
| `5. Datasets/<sem> - Data/` | `data/archive/<sem>/` |
| `5. Datasets/New_result_update/` | `data/results/greedy-pickles/` + `data/results/sdv-sids/` |
| `6. Results Presentations/` | `presentations/` |
| `7. Literature Review/` | `literature/` |
| `_To-Do & Trackers/` | `admin/` |

Every file's old Drive path is in the `original_drive_path` column of [`catalog/CATALOG.csv`](../../catalog/CATALOG.csv).

## Option B: local Python
```bash
git clone <repo-url> eci-research && cd eci-research
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab code/current/Spring2026.ipynb
```
Then in the config cell, point the paths at the repo instead of Drive:
```python
root_path   = "../../data/archive/"          # instead of "/content/drive/My Drive/ECI Research/5. Datasets/"
folder      = "2024-fall/"
data_folder = "2019-2023 cleaned"
GDP4_path   = root_path + "2024-fall"
AUTO_REPORT_PATH = "../../reports/<semester>/<Country>/auto-report"
```
Skip the `from google.colab import ...` cells, and replace `!pip install` lines with the requirements file.

## Option C: Claude Code + the agent team
1. Install Claude Code: <https://code.claude.com>
2. `cd eci-research && claude`
3. Type `/onboard` or just describe what you need. The `research-pm` agent will route it.

See [08-using-the-agent-team.md](08-using-the-agent-team.md).

## Secrets
Only the **data team** needs a UN Comtrade API key (for the annual pull). Copy `.env.example` to `.env` and set `COMTRADE_API_KEY`. `.env` is gitignored, so **never** paste a key into a notebook you commit.
