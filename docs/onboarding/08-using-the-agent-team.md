# 08 · Using the Agent Team (Claude Code)

This repo has a built-in team of AI agents that can do most of the mechanical work: run the notebook, pull the numbers, draft the report, QA it, file everything, and keep the catalog current. You stay in charge of judgment calls and of anything published.

## Setup
1. Install Claude Code: <https://code.claude.com>
2. `cd eci-research && claude`

Because of `.claude/settings.json` (`"agent": "research-pm"`), every session starts with the **Research PM** in charge. Describe what you need in plain English, or use a command below.

## How it is organized
Claude Code offers three building blocks, and this repo uses all of them:

| Building block | What it is | In this repo |
|---|---|---|
| **Subagents** (`.claude/agents/`) | Specialist workers with their own instructions and tools. A coordinator delegates to them. | `research-pm` (the coordinator at the top), `analyst`, `report-writer`, `qa-reviewer`, `data-engineer`, `lit-scout`, `archivist`, `onboarding-guide` |
| **Skills** (`.claude/skills/`) | Step-by-step playbooks, invoked as `/name` | `/onboard`, `/kickoff`, `/country-report`, `/qa`, `/data-update`, `/status`, `/file-it` |
| **Workflows** (`.claude/workflows/`) | Scripts that fan work out to many agents in parallel and cross-check the results. They run in the background and can be resumed. | `/semester-reports`, `/qa-sweep`, `/lit-review` |

The difference is who holds the plan. With subagents and skills, the PM decides turn by turn what happens next. A workflow puts the plan in a script, so a 10-country job runs the same way every time, and its intermediate results don't flood the conversation. (Background: <https://code.claude.com/docs/en/workflows>.)

```
                         research-pm  (main session, decides and delegates)
     ┌──────────┬──────────┬────┴─────┬───────────┬──────────┬───────────┐
 onboarding  data-      analyst   report-     qa-        lit-       archivist
 -guide      engineer             writer      reviewer   scout
                                                 ^
                              independent: never reviews its own work

 Workflows (fan-out):  semester-reports = per country: analyst -> writer -> 2x QA -> verdict
                       qa-sweep         = per report: 2 independent reviewers -> merged verdict
                       lit-review       = per paper: lit-scout -> cross-check -> synthesis
```

## Commands
| Command | What happens | Time |
|---|---|---|
| `/onboard` | Interactive tour for a new member | 30–60 min |
| `/kickoff` | PM plans the semester: country list, assignments (from tracker history), GitHub issues, deadlines | 10 min |
| `/country-report Poland` | analyst runs Section 1 → you confirm the numbers → report-writer drafts → qa-reviewer checks → archivist files it | About 20–40 min, plus 1–2 hours if you include greedy |
| `/qa reports/2026-fall/Poland` | Independent QA of one report | 5 min |
| `/data-update 2024` | data-engineer pulls, cleans, and validates a new data year (needs `COMTRADE_API_KEY`) | 1–2 hours |
| `/status` | What's done, what's in progress, and what's blocked this semester | 1 min |
| `/file-it` | archivist files new files, regenerates the catalog, and scans for PII and keys | 2 min |
| `/semester-reports` (workflow) | Same as `/country-report`, but for many countries in parallel | Varies |
| `/qa-sweep` (workflow) | Double-blind QA of every report in a folder | Varies |
| `/lit-review` (workflow) | Reviews many papers in parallel, in the lab's format | Varies |

Pass workflow inputs in plain English, e.g. *"run /semester-reports for Poland, Canada and Kenya, comprehensive only"*.

## Running headless (no chat)
```bash
python3 scripts/run_notebook.py --country Vietnam --peers Singapore,Malaysia,Philippines \
    --category emerging --semester 2026-fall          # the analyst's engine; works without Claude
claude -p "/status"                                   # one-shot status report
```

## What the agents will NOT do
- Commit personal data or API keys (the archivist scans before every commit)
- Push to GitHub, create issues, or touch the lab website without asking you
- Invent numbers. Missing values stay as `[placeholders]` and get flagged.
- Edit anything under `archive/`

## Tips
- Review the analyst's `analysis-notes.md` before letting the writer go. Garbage in, garbage out.
- Read the QA report even when it passes. It's the fastest way to understand your own report.
- The agents follow the docs. When you find a better way to do something, update the relevant `docs/` or `.claude/skills/` file, and the whole team improves.
