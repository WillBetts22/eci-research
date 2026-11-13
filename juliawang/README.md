# Julia Wang — diversification versus ECI

Research question: **Do more diversified countries always have higher ECI?**

- `exploration.ipynb`: research explanation and interactive exploration.
- `analyze.py`: reproducible calculation; run with Python, NumPy, and pandas installed.
- `outputs/findings.md`: executed results, methods, and limitations.
- `outputs/`: country metrics, correlations, disagreement tables, and an SVG scatterplot.

Uses only existing 2019–2023 cleaned exports. Excludes the overlapping High-complexity Products aggregate. Primary analysis uses 2019 and a fixed 119-country sample. Results concern the lab's grouped-data ECI, not published Harvard rankings. The ECI sign is positively oriented to RCA diversity by convention.

Run `python3 juliawang/analyze.py` from the repository root, or open the notebook and run cells in order. Notebook additionally uses IPython. No external data required.

Model plots: run `python3 juliawang/plot_models.py` after the analysis (requires Matplotlib). See `outputs/models.md` for model interpretation and `outputs/model_comparison.csv` for fit and leave-one-country-out RMSE.

## Project 3: complexity measures and growth

- `eci_growth_3.ipynb`: executed data audit, initial comparison, aggregation tests, Fitness/continuous-RCA alternatives, rolling-origin robustness, error diagnostics and recommendation.
- `prepare_growth_data.py`: verifies and extracts the historical input; see `data/README.md`.
- `project3_horse_race.py`: reproducible extended comparisons for 1995–2019 starting-year measures; run `.venv/bin/python juliawang/project3_horse_race.py`.
- `outputs/project3/full/recommendation.md`: evidence-based recommendation and limits.
- `outputs/project3/full/`: country-year scores, eight forecast designs, spectral/Fitness diagnostics, paired intervals, error concentration tables and figures.

The grouped scores are goods-only reconstructions; actual services are unavailable. Fitness is evaluated at explicit finite iteration counts and has not passed the stated convergence check. Results use revised historical data and do not establish causality.
