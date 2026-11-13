"""Build derived/score_panel.csv: complexity variants per country-year (1995-2024) from the
Growth Lab HS4 panel, merged with Growth Lab published ECI, WDI, WGI and PWT.

Sample each year: total goods exports >= $1B and population >= 1M (Atlas ranking rule).
Variants: ECI (binary RCA>=1), ECI log(1+RCA), ECI capped RCA, ECI RCA percentile,
ECI per-capita RCA (RpcA>=1), ECI RCA>=1 & RpcA>=1, log Fitness, diversity, entropy,
resource export share (HS 26/27/71).
"""
import sys
from pathlib import Path
B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B.parent / 'lib'))
import numpy as np, pandas as pd
import eci, research as R
import warnings; warnings.filterwarnings('ignore')

rows = []
for y in range(1995, 2025):
    X = R.atlas_hs4(y)
    pop = R.wdi().query('year == @y').set_index('iso3').population.reindex(X.index)
    rca = eci.rca(X)
    X = X.loc[rca.index]
    M = (rca >= 1).astype(float)
    div = M.sum(axis=1)
    pcx = X.div(pop, axis=0)
    rpca = pcx / (X.sum(axis=0) / pop.sum())
    Mp = (rpca >= 1).astype(float)
    sc = pd.DataFrame(index=X.index)
    sc['eci_binary'] = R.eci_weighted(M)
    for name, W in R.rca_variants(X).items():
        key = {'log(1+RCA)': 'eci_log1p', 'capped RCA (min(RCA,2))': 'eci_capped', 'RCA percentile (within product)': 'eci_pctile'}.get(name)
        if key:
            sc[key] = R.eci_weighted(W.loc[X.index], orient_to=div)
    sc['eci_rpca'] = R.eci_weighted(Mp, orient_to=div)
    sc['eci_rca_and_rpca'] = R.eci_weighted(M * Mp, orient_to=div)
    Mb = M.loc[M.sum(axis=1) > 0, M.sum(axis=0) > 0]
    sc['log_fitness'] = R.fitness(Mb, n_iter=100, tol=0)
    sc['diversity'] = div
    sc['entropy'] = R.entropy(X)
    sc['resource_share'] = R.resource_share(X)
    sc['n_countries_year'] = len(X)
    sc['year'] = y
    rows.append(sc.rename_axis('iso3').reset_index())
    print(y, len(X), flush=True)
P = pd.concat(rows)
P = P.merge(R.atlas_cy()[['iso3', 'year', 'eci', 'coi', 'growth_proj']].rename(columns={'eci': 'eci_atlas_published'}), on=['iso3', 'year'], how='left')
P = P.merge(R.wdi(), on=['iso3', 'year'], how='left').merge(R.wgi(), on=['iso3', 'year'], how='left')
P = P.merge(R.pwt()[['iso3', 'year', 'hc', 'gdppc_pwt', 'rgdpna', 'pop']].rename(columns={'pop': 'pop_pwt'}), on=['iso3', 'year'], how='left')
P.to_csv(B / 'derived' / 'score_panel.csv', index=False)
print(P.shape)
