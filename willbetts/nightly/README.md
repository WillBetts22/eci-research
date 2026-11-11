# Nightly ECI Research

An automated research cycle. Every night a cloud Claude agent picks **one** question from `QUEUE.md`, runs a small experiment on the repo's data, writes the result up as an executed notebook, and opens a PR titled `Nightly research YYYY-MM-DD — <QID>: …`. Will reviews it in the morning and merges.

| File / folder | What it is | Who edits |
|---|---|---|
| `PROTOCOL.md` | The exact procedure the agent follows | Will |
| `QUEUE.md` | Prioritized questions. Reorder it to steer the agent | Will |
| `runs/<date>_<QID>-<slug>/notebook.ipynb` | One executed write-up per night | Agent (new files only) |
| `proposals/<date>.md` | New research avenues the agent found | Agent → Will promotes to `QUEUE.md` |
| `data-requests/<date>-<slug>.md` | Data problems found, external data needed | Agent → Will fulfills |
| `lib/eci.py` | Shared ECI helpers (created by Q01) | Agent, when a question calls for it |

**Morning review:** read the PR's TL;DR and the "⚠️ Needs your input" section, skim the notebook, then merge. PRs don't conflict with each other, so merge them in any order. If a night's question needs external data, add the file and note where you put it in `QUEUE.md`.

The routine is managed at https://claude.ai/code/routines. Pause or delete it there.
