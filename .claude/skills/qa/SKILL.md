---
name: qa
description: Independent QA review of one ECI country report folder. Use when a report draft needs checking before it is marked done or published.
argument-hint: "<path to reports/<semester>/<Country>>"
---

Delegate to the `qa-reviewer` agent with the folder `$ARGUMENTS`. It must not be the agent that wrote the draft. Relay its VERDICT and the FAIL items verbatim, and say where `qa-report.md` was written. Don't fix anything yourself unless the user asks. If they do, route the fixes to `report-writer`.
