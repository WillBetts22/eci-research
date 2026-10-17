---
name: data-update
description: Add a new year of UN Comtrade export data and World Bank GDP to the lab's datasets, then validate it and update the notebook config. Use once a year or when someone asks to update the data.
argument-hint: "<year to add, e.g. 2024>"
---

Delegate to the `data-engineer` agent to add data year **$ARGUMENTS**, following `docs/onboarding/07-annual-data-update.md`.

1. Preflight: check that `COMTRADE_API_KEY` is set (`test -n "$COMTRADE_API_KEY"` or a `.env` entry). If it's missing, stop and explain how to get a key. Never ask the user to paste the key into chat or a file that gets committed.
2. Warn the user about runtime (about 30+ minutes for the pull) before starting, and run it in the background.
3. When the engineer finishes, show its validation table. Any row/country/total anomaly larger than in `docs/KNOWN-ISSUES.md` D1/D2 needs the user's sign-off.
4. Propose the notebook config changes (the cell table in guide 07) in a **new** notebook `code/current/<Semester>.ipynb`. Don't edit the archived one.
5. Hand off to `archivist`, then update the "Current semester context" in `CLAUDE.md` with the new latest data year.
