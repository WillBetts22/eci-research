#!/usr/bin/env bash
# Regenerate every result in paper/eci_fourteen_tests.pdf (queue Q03-Q16, 2026-11-12).
# Usage: bash willbetts/nightly/run_all.sh [--skip-download]
set -euo pipefail
cd "$(dirname "$0")"
pip install -q -r ../../requirements.txt pycountry statsmodels openpyxl >/dev/null
if [[ "${1:-}" != "--skip-download" ]]; then bash external-data/download.sh; fi
python3 external-data/scripts/build_score_panel.py
for d in runs/2026-11-12_Q*/; do
  [[ -f "$d/run.py" ]] || continue
  echo "== $d"; (cd "$d" && python3 run.py > run.log 2>&1) && tail -n 3 "$d/run.log"
done
if command -v tectonic >/dev/null; then (cd paper && tectonic eci_fourteen_tests.tex); else echo "tectonic not found: compile paper/eci_fourteen_tests.tex yourself"; fi
