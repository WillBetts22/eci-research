#  Start Here: New Member Onboarding

Welcome to the ECI Research Lab. This page is your first-week checklist. Work through it top to bottom; it should take about **2 hours** in total.

> **Shortcut:** if you have [Claude Code](https://code.claude.com) installed, open this repo and type `/onboard`. The `onboarding-guide` agent walks you through these same steps and answers questions as you go.

## What the lab does, in 60 seconds

We measure how **complex** a country's economy is (how sophisticated, diverse, and rare the things it exports are) using the **Economic Complexity Index (ECI)** from Hausmann & Hidalgo. Then we answer a practical question: *which industries should this country invest in next to raise its complexity, and with it its long-run growth?*

For each country we produce a **country report** (~20 pages, same structure every time), published at <https://kachanilab.ieor.columbia.edu/research-projects/economic-complexity>.

## Week 1 checklist

### Day 1: get access (15 min)
- [ ] Get added to the GitHub repo (ask the research lead) and clone it: `git clone <repo-url>`
- [ ] Get added to the lab's Google Drive folder (the Colab notebooks read from it) and the group chat / Slack
- [ ] Get **editor** access on the lab website (see [06-presentation-and-website.md](06-presentation-and-website.md))

### Day 1: see the big picture (45 min)
- [ ] Watch the **automation demo video**: [`media/Fall2025-Automation-Demo.mp4`](media/Fall2025-Automation-Demo.mp4) (download it if GitHub won't preview it)
- [ ] Open [`presentations/Updated Consolidated ECI Presentation.pptx`](../../presentations/) and read the **first ~30 slides**. They introduce the concepts and calculations. Then click through a few country summaries to see what finished output looks like.
- [ ] Read [01-what-is-eci.md](01-what-is-eci.md), the plain-English version of the theory

### Day 2: see a finished report (30 min)
- [ ] Read one recent report end to end, e.g. [`reports/2026-spring/Vietnam.pdf`](../../reports/2026-spring/Vietnam.pdf)
- [ ] Open [`templates/Auto Report Template.docx`](../../templates/) and compare. Every report follows the same section structure, and only the `[bracketed]` values and `{instruction}` paragraphs change.
- [ ] Skim [`catalog/COUNTRIES.md`](../../catalog/COUNTRIES.md) to see which countries we've covered and when

### Day 3: run the code (60 min + waiting)
- [ ] Follow [02-setup.md](02-setup.md) to get Colab or local Python working
- [ ] Follow [04-running-the-code.md](04-running-the-code.md) for **any** country (the notebook defaults to Vietnam), at least through the ECI graphs
- [ ] Note anything confusing and post it in the group chat. Fixing the docs counts as a contribution!

### Then: your assignment
- [ ] Get your country assignment from the research lead (it is tracked in `admin/trackers/Country Reports Tracker.xlsx` and as GitHub issues)
- [ ] Follow [03-your-first-country-report.md](03-your-first-country-report.md)

## The guides

| # | Guide | When you need it |
|---|---|---|
| 00 | **Start here** (this page) | Day 1 |
| 01 | [What is ECI?](01-what-is-eci.md) | Before touching code |
| 02 | [Setup](02-setup.md) | Before running the notebook |
| 03 | [Your first country report](03-your-first-country-report.md) | When you get your assignment |
| 04 | [Running the code](04-running-the-code.md) | While running the notebook |
| 05 | [Writing the report](05-writing-the-report.md) | After the notebook finishes |
| 06 | [Presentation & website](06-presentation-and-website.md) | After the report is approved |
| 07 | [Annual data update](07-annual-data-update.md) | Once a year (data team) |
| 08 | [Using the agent team](08-using-the-agent-team.md) | Anytime: it makes everything above faster |

## Lab norms (from past meeting notes)
- Weekly stand-up is **required**. Give 24 hours' notice if you can't make it.
- Typical commitment is about **2 hours/week** on code and writing, individually or in groups.
- The lab is student-run, so being self-driven is the expectation. Ask questions early in the group chat.
- A typical semester timeline: assignments in week 2–3 → check-in about 2 weeks later → reports due about 3 weeks after that. For example, Spring 2026 assigned countries on 03/29, checked in on 04/05, and had reports due 04/19.

## Who to ask
- **Research lead / PM**: assignments, deadlines, access
- **Data team**: Comtrade/GDP data issues
- **Automation team**: the auto-report JSON and Apps Script
- **Prof. Kachani**: countries list and research direction (via the lead)
