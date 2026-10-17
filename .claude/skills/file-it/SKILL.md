---
name: file-it
description: File new or changed files into the right place, regenerate the catalog and text mirrors, and run the PII/secret/size scan before a commit. Use after any work that created files, or before committing.
---

Delegate to the `archivist` agent: file everything new per its filing rules, run `python3 scripts/docx_to_md.py && python3 scripts/build_catalog.py`, remove `_work/` folders, run the pre-commit safety scan, and propose a commit message. Show the user the scan results and the proposed commit. Commit only if they say so, and push only if they say so.
