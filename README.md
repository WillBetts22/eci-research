# ECI Research Lab — Columbia University

The Economic Complexity Research Lab (advised by Prof. Soulaymane Kachani, IEOR) writes **country reports** that measure each economy's *Economic Complexity Index (ECI)*, then recommend which industries it should grow next. The recommendations come from opportunity gain, a greedy budget-allocation optimizer, sensitivity analysis, and the Structural Optimality Index (SOI).

This repo holds **everything the lab has produced since 2019**: data, code, templates, and every previous report, presentation, and literature review. Every file is organized and labeled. It also includes **an agentic workflow**: a team of Claude Code agents, led by a Research PM, that can run most of the semester for you.

> **New member?** Start at **[docs/onboarding/00-START-HERE.md](docs/onboarding/00-START-HERE.md)**. It takes about an hour, and afterwards you'll know enough to produce a report.

---

## Quick links

| I want to… | Go to |
|---|---|
| Get onboarded | [docs/onboarding/00-START-HERE.md](docs/onboarding/00-START-HERE.md) |
| Understand ECI, PCI, RID, SDV, SOI | [docs/methodology.md](docs/methodology.md) |
| Write my country report, step by step | [docs/onboarding/03-your-first-country-report.md](docs/onboarding/03-your-first-country-report.md) |
| Run the analysis notebook | [docs/onboarding/04-running-the-code.md](docs/onboarding/04-running-the-code.md) · [code/current/](code/current/) |
| Find a country's previous report | [catalog/COUNTRIES.md](catalog/COUNTRIES.md) |
| Find *any* file (with labels) | [catalog/README.md](catalog/README.md) · [catalog/CATALOG.csv](catalog/CATALOG.csv) |
| Use the data | [data/README.md](data/README.md) |
| Pull a new year of UN Comtrade data | [docs/onboarding/07-annual-data-update.md](docs/onboarding/07-annual-data-update.md) |
| Use the AI agent team | [docs/onboarding/08-using-the-agent-team.md](docs/onboarding/08-using-the-agent-team.md) |
| See the lab's history | [docs/HISTORY.md](docs/HISTORY.md) |
| Fix a known bug or gotcha | [docs/KNOWN-ISSUES.md](docs/KNOWN-ISSUES.md) |

## Repo map

```
eci-research/
├── docs/                    ← START HERE: onboarding, methodology, history, known issues
│   ├── onboarding/          ← numbered guides 00–08, plus the Fall 2025 automation demo video
│   └── original-instructions/  ← the original Word instructions (kept for reference)
├── code/
│   ├── current/             ← the notebook to run this semester (Spring2026.ipynb)
│   ├── data-retrieval/      ← UN Comtrade download + cleaning notebooks
│   ├── report-automation/   ← Google Apps Script that fills the report template from JSON
│   └── archive/<semester>/  ← every past semester's code
├── data/
│   ├── raw/                 ← <year>_mega.csv: raw Comtrade exports by HS code (2019–2023)
│   ├── cleaned/             ← <year>clean.csv: 155 countries × 18 industry groups
│   ├── results/             ← greedy-optimizer pickles, SDV/SIDS outputs
│   └── archive/<semester>/  ← past data snapshots and GDP files
├── reports/<semester>/      ← every country report ever written, by semester
├── templates/               ← Auto Report Template + older templates
├── presentations/           ← Updated Consolidated ECI Presentation + older decks
├── literature/              ← literature review + member submissions
├── admin/                   ← to-dos, meeting notes, trackers, recruiting
├── catalog/                 ← auto-generated index of every file + text copies of all Word docs
├── scripts/                 ← catalog and doc-conversion helpers
└── .claude/                 ← the agent team: agents, skills, workflows
```

Folders marked "current" are what to use. Everything under `archive/` is history. Everything under `archive/` is history.

## The semester in one picture

```
 (once a year)                (every semester, per country)
┌──────────────┐   ┌───────────┐   ┌────────────┐   ┌────────────┐   ┌───────────┐   ┌──────────────┐
│ Pull Comtrade│ → │ Run the   │ → │ Fill the   │ → │ QA review  │ → │ Add 3     │ → │ Publish PDF  │
│ + World Bank │   │ notebook  │   │ report     │   │ (numbers,  │   │ slides to │   │ on lab site, │
│ GDP data     │   │ for your  │   │ template   │   │ figures,   │   │ the deck  │   │ update       │
│              │   │ country   │   │ (auto/JSON)│   │ prose)     │   │           │   │ tracker      │
└──────────────┘   └───────────┘   └────────────┘   └────────────┘   └───────────┘   └──────────────┘
 data-engineer       analyst         report-writer     qa-reviewer     report-writer    archivist
                         ▲                                                             │
                         └──────────────── research-pm coordinates everything ─────────┘
```

## The agent team (Claude Code)

The repo ships with a **Claude Code agent team** in [`.claude/`](.claude/). Open the repo in Claude Code and type:

```
/kickoff                       # PM plans the semester: assignments, deadlines, issues
/country-report Vietnam        # analyst → writer → QA for one country
/onboard                       # interactive tour for a new member
/status                        # PM reports what's done, what's blocked, what's next
```

For many countries at once, use a **workflow**, a saved script that fans out one agent per country and cross-checks the results:

```
/semester-reports  (args: ["Vietnam","Canada","Poland"])
/lit-review        (args: "economic complexity and inequality")
/qa-sweep          (args: "reports/2026-spring")
```

Full guide: [docs/onboarding/08-using-the-agent-team.md](docs/onboarding/08-using-the-agent-team.md).

## Ground rules

1. **Never commit personal data**: no rosters, phone numbers, applicant responses, or resumes. Those stay on the lab's private Google Drive.
2. **Never commit API keys.** The Comtrade key goes in a local `.env` file (see `.env.example`). Every old hardcoded key was replaced with `<COMTRADE_API_KEY>`.
3. **Don't edit `archive/`.** To change old code, copy it into `code/current/` first.
4. **After adding files, run** `python3 scripts/docx_to_md.py && python3 scripts/build_catalog.py` so the catalog stays accurate. The agents do this for you.

## Links

- Published reports: <https://kachanilab.ieor.columbia.edu/research-projects/economic-complexity>
- Harvard Atlas of Economic Complexity: <https://atlas.cid.harvard.edu/>
- UN Comtrade: <https://comtradeplus.un.org/>
- Lab email: ecilab@columbia.edu
