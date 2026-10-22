# Julia Wang — diversification versus ECI

Research question: **Do more diversified countries always have higher ECI?**

- `exploration.ipynb`: research explanation and interactive exploration.
- `analyze.py`: reproducible calculation; run with Python, NumPy, and pandas installed.
- `outputs/findings.md`: executed results, methods, and limitations.
- `outputs/`: country metrics, correlations, disagreement tables, and an SVG scatterplot.

Uses only existing 2019–2023 cleaned exports. Excludes the overlapping High-complexity Products aggregate. Primary analysis uses 2019 and a fixed 119-country sample. Results concern the lab's grouped-data ECI, not published Harvard rankings. The ECI sign is positively oriented to RCA diversity by convention.

Run `python3 juliawang/analyze.py` from the repository root, or open the notebook and run cells in order. Notebook additionally uses IPython. No external data required.

Model plots: run `python3 juliawang/plot_models.py` after the analysis (requires Matplotlib). See `outputs/models.md` for model interpretation and `outputs/model_comparison.csv` for fit and leave-one-country-out RMSE.
