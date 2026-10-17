"""Run the lab's Colab notebook locally, for one country, against this repo's data.

The notebook in code/current/ was written for Google Colab and reads/writes
"drive/My Drive/ECI Research/...". This script:
  1. builds a throwaway "fake Drive" folder whose data files are symlinks into data/,
  2. patches the config cell (country, peers, category, years),
  3. strips Colab-only lines (drive.mount, !pip),
  4. executes the chosen sections and saves every output
     (executed notebook, <Country>.json, img/, tables) to reports/<semester>/<Country>/.

Usage:
    python3 scripts/run_notebook.py --country Vietnam --peers Singapore,Malaysia,Philippines \
        --category emerging --semester 2026-fall
    # add --sections comprehensive,greedy,plot,sensitivity for everything (greedy is SLOW: 1-2 h)

The repo's data/ is never written to.
"""
import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent.parent
NB = ROOT / "code" / "current" / "Spring2026.ipynb"

# Drive folder name -> repo folder (mirrored file-by-file as symlinks)
DRIVE_DATA = {
    "2024 Fall - Data": "data/archive/2024-fall",
    "2023 Fall - Data": "data/archive/2023-fall",
    "2022 Fall - Data": "data/archive/2022-fall",
    "raw data": "data/raw",
    "cleaned data": "data/cleaned",
}

SECTION_MARKERS = [  # (section name, markdown heading that starts it)
    ("comprehensive", "# Comprehensive"),
    ("greedy", "# 2. Greedy Budget Allocation"),
    ("plot", "# 3. Plot Budget Allocation"),
    ("sensitivity", "# 4. Sensitivity"),
]


def mirror(src: Path, dst: Path):
    """Recreate src's directory tree under dst with every file symlinked (so writes stay in dst)."""
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        t = dst / rel
        if p.is_dir():
            t.mkdir(parents=True, exist_ok=True)
        else:
            t.parent.mkdir(parents=True, exist_ok=True)
            if not t.exists():
                t.symlink_to(p)


def build_shim(work: Path):
    ds = work / "drive" / "My Drive" / "ECI Research" / "5. Datasets"
    for drive_name, repo_rel in DRIVE_DATA.items():
        mirror(ROOT / repo_rel, ds / drive_name)
        # a few cells use the path without "5. Datasets/"
        mirror(ROOT / repo_rel, work / "drive" / "My Drive" / "ECI Research" / drive_name)
    # cell 153 still points at an old Fall-2022 path
    mirror(ROOT / "data/archive/2024-fall/2019-2023 cleaned", work / "drive/My Drive/ECI Research/Fall 2022/Data/2019-2021 cleaned")
    # sensitivity cell (#160) reads "2023 Fall - Data/2019-2023 cleaned", which never existed; point it at the real 2019-2023 set
    mirror(ROOT / "data/archive/2024-fall/2019-2023 cleaned", ds / "2023 Fall - Data" / "2019-2023 cleaned")
    for d in ["ECI Auto Report Demo/img", "ECI Auto Report Test/img", "New_result_update"]:
        (work / "drive" / "My Drive" / d).mkdir(parents=True, exist_ok=True)
    (work / "sdv_and_sids").mkdir()
    (work / "newdrive").symlink_to(work / "drive", target_is_directory=True)


def py_list(xs):
    return "[" + ", ".join(repr(x) for x in xs) + "]"


def patch_config(src: str, a) -> str:
    subs = {
        "main_country": repr(a.country),
        "comparable_countries": "[main_country, " + ", ".join(repr(p) for p in a.peers) + "]",
        "category": repr(a.category),
        "begin_year": str(a.begin_year),
        "end_year": str(a.end_year),
    }
    if a.leading:
        subs["sdv_leading_countries"] = py_list(a.leading)
    if a.emerging:
        subs["sdv_emerging_countries"] = py_list(a.emerging)
    if a.sdv_comparable:
        subs["sdv_comparable_countries"] = "[main_country, " + ", ".join(repr(p) for p in a.sdv_comparable) + "]"
    for var, val in subs.items():
        src, n = re.subn(rf"^(\s*){var}\s*=.*$", rf"\g<1>{var} = {val}", src, count=1, flags=re.M)
        if n == 0 and var in ("main_country", "comparable_countries"):
            sys.exit(f"config cell no longer has `{var} = ...`; update scripts/run_notebook.py")
    return src


def clean_code(src: str, a) -> str:
    src = src.replace("/content/drive/", "drive/")
    src = re.sub(r"(['\"])/content/", r"\1", src)  # other Colab scratch paths, e.g. /content/sdv_and_sids/
    out = []
    for line in src.splitlines():
        s = line.strip()
        if s.startswith(("!", "%pip", "pip install")) or "google.colab" in s or "drive.mount(" in s:
            out.append(re.match(r"\s*", line).group(0) + "pass  # [run_notebook] removed Colab-only line")
            continue
        out.append(line)
    src = "\n".join(out)
    # greedy/plot cells hardcode the data year; align with --greedy-year
    src = re.sub(r"^(\s*)year\s*=\s*20\d\d\b", rf"\g<1>year = {a.greedy_year}", src, flags=re.M)
    return src


def select_cells(nb, sections):
    starts = {}
    for i, c in enumerate(nb.cells):
        if c.cell_type == "markdown":
            for name, marker in SECTION_MARKERS:
                if c.source.strip().startswith(marker):
                    starts.setdefault(name, i)
    order = [n for n, _ in SECTION_MARKERS if n in starts]
    keep = set()
    for k, name in enumerate(order):
        end = starts[order[k + 1]] if k + 1 < len(order) else len(nb.cells)
        if name in sections:
            keep.update(range(starts[name], end))
    keep.update(range(0, starts.get("comprehensive", 0)))  # header cells (cell 2 is the "save JSON" helper; skip it)
    cells = []
    for i in sorted(keep):
        c = nb.cells[i]
        if c.cell_type == "code" and c.source.strip().startswith("# RUN THIS AT END TO SAVE OUTPUT"):
            continue
        if c.cell_type == "code" and c.source.strip() == "assert(False)":
            continue
        cells.append(c)
    return cells


def check_names(nb, a):
    """Validate country names the way the notebook sees them.

    The notebook renames some countries before using them (e.g. 'Viet Nam' -> 'Vietnam',
    'Republic of Korea' -> 'South Korea'), and needs every name in both the export and GDP data.
    """
    import pandas as pd
    renames = {}
    for c in nb.cells:
        if c.cell_type == "code" and "mxlist.append(df_to_matrix" in c.source:
            for conds, new in re.findall(r"if\s+(country_name\s*==.*?):\s*\n\s*data\.loc\[i, \"Country\"\]\s*=\s*(['\"].*?['\"])", c.source):
                for old in re.findall(r"==\s*(['\"].*?['\"])", conds):
                    renames[old[1:-1]] = new[1:-1]
    exports = {renames.get(n, n) for n in pd.read_csv(ROOT / "data/cleaned" / f"{a.end_year}clean.csv")["Country"]}
    gdp = {renames.get(n, n) for n in pd.read_csv(ROOT / "data/archive/2024-fall/GDP_2023.csv")["Country Name"]}
    problems = {}
    for name in dict.fromkeys([a.country, *a.peers, *a.leading, *a.emerging, *a.sdv_comparable]):
        where = [label for label, s in (("export data", exports), ("GDP data", gdp)) if name not in s]
        if where:
            hint = sorted(n for n in exports | gdp if name.lower()[:4] in str(n).lower())[:6]
            problems[name] = f"missing from {' and '.join(where)}; similar: {hint}"
    if problems:
        sys.exit("Country-name problems (use the notebook's names, e.g. 'Vietnam', 'USA', 'South Korea'):\n"
                 + "\n".join(f"  {k}: {v}" for k, v in problems.items()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--country", required=True, help="exact name as in data/cleaned/<year>clean.csv")
    ap.add_argument("--peers", required=True, help="3 comparable countries, comma-separated")
    ap.add_argument("--category", choices=["developed", "emerging"], required=True)
    ap.add_argument("--semester", required=True, help="e.g. 2026-fall")
    ap.add_argument("--leading", default="", help="leading economies for RID/SDV table 4a")
    ap.add_argument("--emerging", default="", help="emerging economies for RID/SDV table 4b")
    ap.add_argument("--sdv-comparable", default="", help="countries for the SDV comparison table")
    ap.add_argument("--begin-year", type=int, default=2019)
    ap.add_argument("--end-year", type=int, default=2023)
    ap.add_argument("--greedy-year", type=int, default=None, help="data year for greedy/plot (default: end year)")
    ap.add_argument("--sections", default="comprehensive", help="comma list: comprehensive,greedy,plot,sensitivity")
    ap.add_argument("--timeout", type=int, default=4 * 3600, help="per-cell timeout, seconds")
    ap.add_argument("--keep-work", action="store_true", help="keep the fake-Drive working folder")
    a = ap.parse_args()
    split = lambda s: [x.strip() for x in s.split(",") if x.strip()]
    a.peers, a.leading, a.emerging, a.sdv_comparable = split(a.peers), split(a.leading), split(a.emerging), split(a.sdv_comparable)
    a.greedy_year = a.greedy_year or a.end_year
    sections = set(split(a.sections))

    nb = nbformat.read(NB, as_version=4)
    check_names(nb, a)

    out = ROOT / "reports" / a.semester / a.country
    work = out / "_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    build_shim(work)

    cells = select_cells(nb, sections)
    config_done = False
    for c in cells:
        if c.cell_type != "code":
            continue
        if not config_done and "main_country =" in c.source and "comparable_countries" in c.source:
            c.source = patch_config(c.source, a)
            config_done = True
        c.source = clean_code(c.source, a)
    if not config_done:
        sys.exit("could not find the config cell")
    nb.cells = cells

    print(f"Running {len(cells)} cells for {a.country} ({', '.join(sorted(sections))}) in {work} …", flush=True)
    t0 = time.time()
    os.environ.setdefault("MPLBACKEND", "Agg")
    client = NotebookClient(nb, timeout=a.timeout, kernel_name="python3", allow_errors=True,
                            resources={"metadata": {"path": str(work)}})
    client.execute()
    print(f"done in {(time.time() - t0) / 60:.1f} min")

    errors = []
    for i, c in enumerate(nb.cells):
        for o in c.get("outputs", []):
            if o.get("output_type") == "error":
                first = next((l for l in c.source.splitlines() if l.strip()), "")
                errors.append(f"cell {i} [{first[:50]}]: {o['ename']}: {o['evalue'][:160]}")
    out.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, out / f"{a.country}_executed.ipynb")

    # collect everything the notebook wrote (real files, not symlinks)
    auto, other = out / "auto-report", out / "output"
    n = 0
    for p in work.rglob("*"):
        if p.is_file() and not p.is_symlink():
            rel = p.relative_to(work / "drive" / "My Drive") if "My Drive" in str(p) else p.relative_to(work)
            parts = rel.parts
            if parts[0] in ("ECI Auto Report Demo", "ECI Auto Report Test"):
                dst = auto / Path(*parts[1:])
                if dst.name == "tags.json":
                    continue
            else:
                dst = other / p.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)
            n += 1
    if not a.keep_work:
        shutil.rmtree(work)

    summary = {"country": a.country, "peers": a.peers, "category": a.category, "sections": sorted(sections),
               "years": [a.begin_year, a.end_year], "greedy_year": a.greedy_year,
               "files_written": n, "errors": errors}
    (out / "run_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"{n} output files → {out.relative_to(ROOT)}/  (auto-report/, output/, {a.country}_executed.ipynb)")
    if errors:
        print(f"\n{len(errors)} cell(s) raised errors (see run_summary.json; many are known — docs/KNOWN-ISSUES.md):")
        for e in errors:
            print("  -", e)


if __name__ == "__main__":
    main()
