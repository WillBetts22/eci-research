"""Reproducible full Project 3 comparison. Called by eci_growth_3.ipynb.

Reads the checksum-verified historical source; uses no live downloads.
"""
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
from scipy.linalg import eigh
from scipy.sparse.csgraph import connected_components
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'juliawang/outputs/project3/full'
# Reuse only the documented chapter mapping, not nightly scores or regression results.
sys.path.insert(0, str(ROOT / 'willbetts/nightly/lib'))
from research import LAB_GROUPS

MEASURES = ['diversity', 'entropy', 'hhi', 'eci_hs4', 'eci_hs2',
            'eci_groups18_goods', 'eci_groups17_goods', 'eci_hs4_matched17',
            'eci_continuous', 'log_fitness200', 'log_fitness500', 'eci_harvard']

def spectral(W, reference):
    valid = W.sum(axis=1) > 0
    a = W[valid]
    a = a[:, a.sum(axis=0) > 0]
    kc, kp = a.sum(axis=1), a.sum(axis=0)
    b = a / np.sqrt(kc[:, None] * kp[None, :])
    values, vectors = eigh(b @ b.T)
    components = connected_components((a @ a.T) > 0, directed=False)[0]
    gap = values[-2] - values[-3]
    if components != 1 or gap < 1e-8:
        raise ValueError('Disconnected or spectrally degenerate network')
    v = vectors[:, -2] / np.sqrt(kc)
    if np.corrcoef(v, np.asarray(reference)[valid])[0, 1] < 0:
        v = -v
    result = np.full(len(W), np.nan)
    result[valid] = (v - v.mean()) / v.std()
    return result, {'components': components, 'gap': gap, 'zero_degree_rows': int((~valid).sum())}

def binary_eci(X):
    a = np.asarray(X, float)
    a = a[:, a.sum(axis=0) > 0]
    shares = a / a.sum(axis=1, keepdims=True)
    rca = shares / (a.sum(axis=0) / a.sum())
    m = (rca >= 1).astype(float)
    score, diag = spectral(m, m.sum(axis=1))
    return score, diag, rca, m

def compute_year(d, year, pop):
    X = d.pivot(index='country_iso3_code', columns='product_hs92_code', values='export_value')
    population = pop.reindex(X.index)
    X = X.loc[X.sum(axis=1).ge(1e9) & population.ge(1e6)].fillna(0.)
    X = X.loc[:, X.sum(axis=0).gt(0)]
    score, diag, rca, m = binary_eci(X)
    shares = X.to_numpy() / X.sum(axis=1).to_numpy()[:, None]
    logs = np.zeros_like(shares)
    np.log(shares, out=logs, where=shares > 0)
    scores = pd.DataFrame({'iso3': X.index, 'year': year, 'diversity': m.sum(axis=1),
        'entropy': -(shares*logs).sum(axis=1), 'hhi': (shares**2).sum(axis=1), 'eci_hs4': score})
    diagnostics = [{'year': year, 'measure': 'eci_hs4', **diag}]
    chapter = X.columns.str[:2].astype(int)
    groups = pd.DataFrame({name: X.loc[:, chapter.isin(chapters)].sum(axis=1)
                           for name, chapters in LAB_GROUPS.items()}, index=X.index)
    nonoverlap = groups.drop(columns='High-complexity Products')
    covered = set(c for g, chs in LAB_GROUPS.items() if g != 'High-complexity Products' for c in chs)
    matched = X.loc[:, chapter.isin(covered)]
    matrices = {'eci_hs2': X.T.groupby(X.columns.str[:2]).sum().T,
                'eci_groups18_goods': groups, 'eci_groups17_goods': nonoverlap,
                'eci_hs4_matched17': matched}
    coverage = []
    for name, matrix in matrices.items():
        e, dg, _, _ = binary_eci(matrix)
        scores[name] = e
        diagnostics.append({'year': year, 'measure': name, **dg})
        coverage.append({'year': year, 'measure': name, 'countries': len(X),
                         'nonzero_categories': int(matrix.sum(axis=0).gt(0).sum()),
                         'sum_to_goods_ratio': matrix.to_numpy().sum()/X.to_numpy().sum()})
    # Continuous alternative: identical spectral construction with log(1+RCA) weights.
    scores['eci_continuous'], dg = spectral(np.log1p(rca), m.sum(axis=1))
    diagnostics.append({'year': year, 'measure': 'eci_continuous', **dg})
    # Tacchella simultaneous updates, normalized to mean 1 every iteration.
    # Finite iteration estimates are explicit; do not claim convergence from rank stability.
    valid = m.sum(axis=1) > 0
    a = m[valid]; a = a[:, a.sum(axis=0) > 0]
    F, Q = np.ones(len(a)), np.ones(a.shape[1])
    saved = {}
    delta_log = np.nan
    floor = 1e-250
    for iteration in range(1, 501):
        fn = a @ Q
        qn = 1 / (a.T @ (1 / np.maximum(F, floor)))
        fn, qn = fn/fn.mean(), qn/qn.mean()
        delta_log = float(np.max(np.abs(np.log10(np.maximum(fn, floor)) - np.log10(np.maximum(F, floor)))))
        F, Q = np.maximum(fn, floor), np.maximum(qn, floor)
        if iteration in [200, 500]:
            v = np.full(len(X), np.nan); v[valid] = np.log10(F)
            scores[f'log_fitness{iteration}'] = v
            saved[iteration] = {'year': year, 'iterations': iteration,
                'max_log10_update': delta_log, 'floor_countries': int((F <= floor).sum()),
                'converged_log_tolerance_1e_8': bool(delta_log < 1e-8)}
    fitness_diagnostics = list(saved.values())
    fitness_diagnostics[-1]['rank_correlation_200_500'] = scores.log_fitness200.corr(scores.log_fitness500, method='spearman')
    return scores, diagnostics, coverage, fitness_diagnostics

def window(scores, cy, start, horizon):
    a = cy.loc[cy.year.eq(start)].set_index('iso3')
    b = cy.loc[cy.year.eq(start+horizon)].set_index('iso3')
    s = scores.loc[scores.year.eq(start)].set_index('iso3').copy()
    y0 = a.gdppc_ppp_const.reindex(s.index); y1 = b.gdppc_ppp_const.reindex(s.index)
    s['growth'] = 100*np.log(y1.where(y1.gt(0))/y0.where(y0.gt(0)))/horizon
    s['income'] = np.log(y0.where(y0.gt(0)))
    s['rents'] = a.resource_rents_pct_gdp.reindex(s.index)
    s['eci_harvard'] = a.eci_hs.reindex(s.index)
    s['start'] = start; s['horizon'] = horizon
    return s.reset_index()

def horse_race(train, test, label):
    needed = ['growth', 'income', 'rents'] + MEASURES
    train = train.dropna(subset=needed).copy()
    test = test.dropna(subset=needed).copy()
    results, predictions = [], []
    variants = {'baseline': []} | {m:[m] for m in MEASURES} | {'eci_plus_diversity':['eci_hs4','diversity']}
    for name, extra in variants.items():
        columns = ['income','rents'] + extra
        means, sd = train[columns].mean(), train[columns].std(ddof=0)
        assert sd.gt(0).all()
        xt = sm.add_constant((train[columns]-means)/sd, has_constant='add')
        xv = sm.add_constant((test[columns]-means)/sd, has_constant='add')
        # Center training-period effects: future effect zero means the training-average period effect.
        for year in sorted(train.start.unique())[1:]:
            indicator = (train.start == year).astype(float)
            xt[f'period_{year}'] = indicator - indicator.mean()
            xv[f'period_{year}'] = 0.
        fit = sm.OLS(train.growth, xt).fit(cov_type='cluster', cov_kwds={'groups':train.iso3}) if train.start.nunique()>1 else sm.OLS(train.growth, xt).fit(cov_type='HC1')
        prediction = fit.predict(xv)
        err = test.growth.to_numpy()-prediction.to_numpy()
        results.append({'design':label,'measure':name,'n_train':len(train),'n_test':len(test),
                        'train_r2':fit.rsquared,'rmse':np.sqrt(np.mean(err**2)), 'mae':np.mean(np.abs(err))})
        predictions.append(pd.DataFrame({'iso3':test.iso3.to_numpy(), 'start':test.start.to_numpy(),
            'design':label,'measure':name,'actual':test.growth.to_numpy(), 'prediction':prediction.to_numpy(),'error':err}))
    return pd.DataFrame(results), pd.concat(predictions,ignore_index=True)

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    cy = pd.read_csv(ROOT/'maitreemody/eci_growth/data/derived/country_year.csv')
    parts=[]
    source=ROOT/'juliawang/data/raw/atlas_hs92_country_product_year_4.csv'
    for chunk in pd.read_csv(source, usecols=['country_iso3_code','product_hs92_code','year','export_value'],
                             dtype={'product_hs92_code':str},chunksize=300000):
        parts.append(chunk.loc[chunk.year.between(1995,2019) & chunk.product_hs92_code.str.fullmatch(r'\d{4}')])
    trade = pd.concat(parts,ignore_index=True)
    score_parts=[]; diagnostics=[]; coverage=[]; fitness=[]
    for year,d in trade.groupby('year'):
        pop=cy.loc[cy.year.eq(year)].set_index('iso3').population
        sc,dg,cv,ft=compute_year(d,int(year),pop)
        score_parts.append(sc); diagnostics+=dg; coverage+=cv; fitness+=ft
        print('Computed',year,'countries',len(sc),flush=True)
    scores=pd.concat(score_parts,ignore_index=True)
    scores=scores.merge(cy[['iso3','year','eci_hs']].rename(columns={'eci_hs':'eci_harvard'}),on=['iso3','year'],how='left',validate='one_to_one')
    scores.to_csv(OUT/'all_measures.csv',index=False)
    pd.DataFrame(diagnostics).to_csv(OUT/'spectral_diagnostics.csv',index=False)
    pd.DataFrame(coverage).to_csv(OUT/'aggregation_coverage.csv',index=False)
    pd.DataFrame(fitness).to_csv(OUT/'fitness_diagnostics.csv',index=False)
    windows={(s,h):window(scores,cy,s,h) for h in [5,10] for s in range(1995,2020) if s+h<=2024}
    designs=[('primary_1998_2008',windows[1998,10],windows[2008,10])]
    # Additional origins are specified before inspecting their prediction errors.
    for h,origins in [(10,[2005,2008,2014]),(5,[2005,2010,2015,2019])]:
        for origin in origins:
            historical=[w for (s,k),w in windows.items() if k==h and s+h<=origin]
            train=pd.concat(historical,ignore_index=True)
            assert train.start.max()+h<=origin
            designs.append((f'rolling_h{h}_{origin}',train,windows[origin,h]))
    results=[]; predictions=[]
    for label,tr,te in designs:
        r,p=horse_race(tr,te,label); results.append(r); predictions.append(p)
    results=pd.concat(results,ignore_index=True); predictions=pd.concat(predictions,ignore_index=True)
    base=results.loc[results.measure.eq('baseline'),['design','rmse','train_r2']].rename(columns={'rmse':'baseline_rmse','train_r2':'baseline_r2'})
    results=results.merge(base,on='design',validate='many_to_one')
    results['r2_gain']=results.train_r2-results.baseline_r2
    results['mse_improvement_pct']=100*(1-results.rmse**2/results.baseline_rmse**2)
    results.to_csv(OUT/'horse_race.csv',index=False); predictions.to_csv(OUT/'predictions.csv',index=False)
    stability=[]
    for year in range(1995,2019):
        pair=scores.loc[scores.year.eq(year)].merge(scores.loc[scores.year.eq(year+1)],on='iso3',suffixes=('_a','_b'))
        for m in MEASURES:
            stability.append({'year':year,'measure':m,'paired_countries':int(pair[[m+'_a',m+'_b']].notna().all(axis=1).sum()),
                              'spearman':pair[m+'_a'].corr(pair[m+'_b'],method='spearman')})
    pd.DataFrame(stability).to_csv(OUT/'stability.csv',index=False)
    # Paired-country bootstrap within each design; overlapping origins are never treated as independent.
    intervals=[]; extremes=[]
    rng=np.random.default_rng(20261113)
    for label,g in predictions.groupby('design'):
        wide=g.pivot(index='iso3',columns='measure',values='error')
        draws=rng.integers(0,len(wide),size=(2000,len(wide)))
        for comparator in ['baseline','diversity']:
            for measure in ['eci_hs4','eci_hs2','eci_groups18_goods','eci_groups17_goods','eci_continuous','log_fitness200']:
                difference=wide[comparator].to_numpy()**2-wide[measure].to_numpy()**2
                lo,hi=np.quantile(difference[draws].mean(axis=1),[.025,.975])
                intervals.append({'design':label,'measure':measure,'comparator':comparator,
                    'mse_reduction':difference.mean(),'ci_low':lo,'ci_high':hi})
        # Diagnostic trimming based on baseline errors only: same countries removed for every model.
        remove=wide.baseline.abs().nlargest(min(5,len(wide))).index
        for measure in wide.columns:
            kept=wide.drop(index=remove)
            extremes.append({'design':label,'measure':measure,'remaining':len(kept),
                'trimmed_rmse':np.sqrt(np.mean(kept[measure]**2)),
                'trimmed_mse_gain':np.mean(kept.baseline**2-kept[measure]**2)})
    pd.DataFrame(intervals).to_csv(OUT/'paired_intervals.csv',index=False)
    pd.DataFrame(extremes).to_csv(OUT/'trimmed_error_diagnostic.csv',index=False)
    large=predictions.loc[predictions.design.eq('primary_1998_2008') & predictions.measure.eq('baseline')].copy()
    large['absolute_error']=large.error.abs()
    large.nlargest(10,'absolute_error').to_csv(OUT/'largest_baseline_misses.csv',index=False)
    contributions=[]
    for label,g in predictions.groupby('design'):
        w=g.pivot(index='iso3',columns='measure',values='error')
        for comparator in ['baseline','diversity']:
            delta=w[comparator]**2-w.eci_hs4**2
            for country in delta.abs().nlargest(10).index:
                contributions.append({'design':label,'comparator':comparator,'iso3':country,
                    'mse_gain_contribution':delta[country]/len(w),
                    'total_mean_mse_gain':delta.mean()})
    pd.DataFrame(contributions).to_csv(OUT/'largest_gain_contributions.csv',index=False)
    print('Completed',len(designs),'designs.',flush=True)
    return results

if __name__=='__main__':
    run()
