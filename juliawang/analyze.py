"""Reproducible descriptive analysis using only local cleaned exports."""
from pathlib import Path
import numpy as np
import pandas as pd
from numpy.linalg import eigh
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'juliawang' / 'outputs'

def load(year):
    x = pd.read_csv(ROOT / 'data' / 'cleaned' / f'{year}clean.csv')
    x.columns = x.columns.str.strip()
    x = x.set_index('Country').drop(columns=['High-complexity Products'])
    assert x.index.is_unique and not x.isna().any().any()
    assert np.isfinite(x.to_numpy()).all() and (x >= 0).all().all()
    return x.loc[x.sum(axis=1) > 0]

def measure(x):
    shares = x.div(x.sum(axis=1), axis=0)
    m = (shares.div(x.sum(axis=0) / x.to_numpy().sum(), axis=1) > 1).astype(float)
    m = m.loc[m.sum(axis=1) > 0, m.sum(axis=0) > 0]
    d = m.sum(axis=1).to_numpy()
    u = m.sum(axis=0).to_numpy()
    # Symmetric matrix similar to the usual row-normalized ECI operator.
    b = m.to_numpy() / np.sqrt(d[:, None] * u[None, :])
    values, vectors = eigh(b @ b.T)
    assert abs(values[-1] - 1) < 1e-8
    assert values[-2] < 1 - 1e-8, 'Disconnected network: ECI ambiguous'
    k = vectors[:, -2] / np.sqrt(d)
    # Explicit orientation convention, not an empirical finding about the sign.
    if np.corrcoef(k, d)[0, 1] < 0:
        k = -k
    eci = (k - k.mean()) / k.std()
    s = shares.loc[m.index]
    result = pd.DataFrame({'eci': eci, 'rca_diversity': d,
        'entropy': -(s * np.log(s.where(s > 0))).sum(axis=1),
        'hhi': (s ** 2).sum(axis=1), 'top_industry': s.idxmax(axis=1),
        'top_share': s.max(axis=1) }, index=m.index)
    result['eci_rank'] = result.eci.rank(ascending=False, method='average')
    result['entropy_rank'] = result.entropy.rank(ascending=False, method='average')
    result['rank_gap'] = result.entropy_rank - result.eci_rank
    residual = np.linalg.norm((b @ b.T) @ vectors[:, -2] - values[-2] * vectors[:, -2])
    assert residual < 1e-8
    return result, values[-2] - values[-3]

def run():
    OUT.mkdir(exist_ok=True)
    raw = {y: load(y) for y in range(2019, 2024)}
    common = sorted(set.intersection(*(set(x.index) for x in raw.values())))
    summaries = []
    results = {}
    for y, x in raw.items():
        for sample, data in [('available', x), ('common', x.loc[common])]:
            r, gap = measure(data)
            r.to_csv(OUT / f'{y}_{sample}_metrics.csv')
            for metric in ['entropy', 'rca_diversity', 'hhi']:
                rho = r[metric].rank().corr(r.eci.rank())
                summaries.append({'year':y,'sample':sample,'countries':len(r),
                    'metric':metric,'spearman_rho':rho,'eigenvalue_gap':gap})
            if sample == 'common': results[y] = r
    summary = pd.DataFrame(summaries)
    summary.to_csv(OUT / 'correlations.csv', index=False)
    r = results[2019]
    # Count all strict ordering violations, rather than cherry-picking examples.
    pairs = r.reset_index().merge(r.reset_index(), how='cross', suffixes=('_a','_b'))
    pairs = pairs.loc[pairs.Country_a < pairs.Country_b].copy()
    violations = pairs.loc[(pairs.entropy_a-pairs.entropy_b)*(pairs.eci_a-pairs.eci_b) < 0].copy()
    violations['entropy_gap'] = (violations.entropy_a-violations.entropy_b).abs()
    violations['eci_gap'] = (violations.eci_a-violations.eci_b).abs()
    violations.sort_values('entropy_gap', ascending=False).to_csv(OUT/'2019_entropy_ordering_violations.csv',index=False)
    r.sort_values('rank_gap', key=abs, ascending=False).head(12).to_csv(OUT/'2019_largest_rank_disagreements.csv')
    def sx(v): return 80 + (v-r.entropy.min()) / (r.entropy.max()-r.entropy.min())*650
    def sy(v): return 450 - (v-r.eci.min()) / (r.eci.max()-r.eci.min())*370
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="850" height="540" viewBox="0 0 850 540">', '<rect width="850" height="540" fill="white"/>', '<g font-family="sans-serif" fill="#172b4d">', '<text x="65" y="30" font-size="19">Diversification and ECI, 2019 — fixed country sample</text>', '<path d="M80 70V450H750" fill="none" stroke="#333"/>']
    for val in np.linspace(r.entropy.min(),r.entropy.max(),5):
        svg.append(f'<text x="{sx(val):.1f}" y="475" text-anchor="middle" font-size="12">{val:.2f}</text>')
    for val in np.linspace(r.eci.min(),r.eci.max(),5):
        svg.append(f'<text x="70" y="{sy(val):.1f}" text-anchor="end" font-size="12">{val:.2f}</text>')
    for name,row in r.iterrows():
        svg.append(f'<circle cx="{sx(row.entropy):.1f}" cy="{sy(row.eci):.1f}" r="4" fill="#187e9b" opacity="0.7"><title>{escape(name)}: entropy {row.entropy:.3f}, ECI {row.eci:.3f}</title></circle>')
    for name,row in r.loc[r.rank_gap.abs().nlargest(6).index].iterrows():
        svg.append(f'<text x="{sx(row.entropy)+5:.1f}" y="{sy(row.eci)-6:.1f}" font-size="10">{escape(name)}</text>')
    svg.extend(['<text x="400" y="515" text-anchor="middle">Export-share entropy (higher = more diversified)</text>', '<text x="20" y="260" transform="rotate(-90 20 260)" text-anchor="middle">Recomputed ECI</text>', '</g></svg>'])
    (OUT/'2019_diversification_vs_eci.svg').write_text(''.join(svg))
    text = f'''# Diversification versus ECI — results

Question: Do more diversified countries always have higher ECI?

No, in this grouped local dataset, entropy and ECI do not give identical country orderings. In 2019, {len(violations):,} of {len(pairs):,} country pairs have opposite strict orderings (entropy ties are not violations).

Fixed sample: {len(common)} countries with positive recorded exports in every year, 2019–2023. The overlapping High-complexity Products group is excluded, leaving 17 groups. Zero entries are retained. This is a recomputed grouped-data ECI, not published Harvard ECI.

## Rank correlations (fixed country sample)

'''
    text += summary.loc[summary['sample']=='common',['year','metric','spearman_rho']].to_string(index=False)
    text += '''

## Interpretation and limits

Entropy measures how evenly export value is distributed across groups. RCA diversity counts groups with RCA > 1. ECI also uses which groups other countries specialize in, so identical diversity counts need not imply identical ECI. The ECI eigenvector sign is oriented to correlate positively with RCA diversity by convention; the sign of that relationship is therefore not an independent finding.

This is descriptive evidence, not a test of causality, growth prediction, or the accuracy of either measure. Broad and potentially problematic industry mappings remain in the source data. Excluding the overlapping aggregate does not repair those mappings. Nominal prices affect shares. The repository flags 2023 totals as potentially anomalous; treat 2019 as primary and later years as sensitivity checks. Fixed country coverage improves comparability but ECI is still standardized separately each year. Available-sample results are saved separately. No country-name harmonization is applied to the fixed-sample intersection.

See correlations.csv, country metrics, and ordering violations for the underlying numbers. A small gap between the second and third eigenvalues can indicate sensitivity of ECI to perturbations; it is reported in correlations.csv.
'''
    (OUT/'findings.md').write_text(text)
    print(text[:1800])
    return results, summary

if __name__ == '__main__':
    run()
