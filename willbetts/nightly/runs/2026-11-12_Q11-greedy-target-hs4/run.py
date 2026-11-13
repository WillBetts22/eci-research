"""Q11 - Does the greedy optimizer's target change under HS4 ECI? (no greedy run)

For each Spring 2026 report country and each industry group, add 5% of the country's total
exports to that group and recompute the country's ECI (z-score units).
  grouped : lab rules on the cleaned CSV (zero filter, strict RCA), sign oriented
  HS4     : the same dollar bump spread over the group's HS4 products in proportion to the
            country's own exports there (world exports if it has none), repo HS4 ECI.
Services (chapter 99) has no HS4 counterpart and is excluded from the HS4 side.
Also: how often the notebook's own compute_eci flips sign between the base matrix and a
perturbed one (proposal 2026-11-11 #1), which would make the greedy compare opposite signs.
Pre-stated metric: agreement of the argmax group, and Spearman between the two gain rankings.
Years: 2022 (the notebook's greedy year, N4) and 2019.
"""
import sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'lib'))
import numpy as np, pandas as pd
import eci, research as R
import warnings; warnings.filterwarnings('ignore')

t0 = time.time()
SHARE = 0.05
GROUPS = [g for g in R.LAB_GROUPS]
res = {}
for year in [2022, 2019]:
    G = eci.notebook_filter(R.lab_groups_iso3(year))
    H = R.repo_hs(year, 4)
    base_g = eci.eci_from_exports(G, strict=True)
    base_h = eci.eci_from_exports(H)
    # notebook sign check uses name-indexed data
    Gn = eci.notebook_filter(eci.load_groups(year))
    iso = eci.group_name_to_iso3(eci.load_groups(year, notebook_names=False).index)
    name_of = {}
    raw_names = eci.load_groups(year, notebook_names=False).index
    for raw, new in zip(raw_names, eci.load_groups(year).index):
        if iso[raw]:
            name_of[iso[raw]] = new
    nb_base = eci.notebook_eci(Gn, apply_filter=False)
    nb_base_sign = np.corrcoef(nb_base, eci.notebook_mcp(Gn).sum(1))[0, 1] > 0
    rows, flips, nflip_total = [], {}, 0
    for c in R.REPORT_COUNTRIES:
        if c not in G.index:
            continue
        for g in GROUPS:
            Gp = G.copy(); Gp.loc[c, g] += SHARE * G.loc[c].sum()
            dg = eci.eci_from_exports(Gp, strict=True)[c] - base_g[c]
            dh = np.nan
            if g != 'Services and Utilities' and c in H.index:
                cols = [p for p in H.columns if int(p[:2]) in R.LAB_GROUPS[g]]
                w = H.loc[c, cols]
                if w.sum() == 0:
                    w = H[cols].sum()
                Hp = H.copy(); Hp.loc[c, cols] += SHARE * H.loc[c].sum() * w / w.sum()
                dh = eci.eci_from_exports(Hp)[c] - base_h[c]
            # notebook sign flip?
            nm = name_of.get(c)
            flip = None
            if nm in Gn.index:
                Gnp = Gn.copy(); Gnp.loc[nm, g] += SHARE * Gn.loc[nm].sum()
                v = eci.notebook_eci(Gnp, apply_filter=False)
                flip = bool((np.corrcoef(v, eci.notebook_mcp(Gnp).sum(1))[0, 1] > 0) != nb_base_sign)
                nflip_total += int(flip)
            rows.append({'iso3': c, 'country': R.REPORT_COUNTRIES[c], 'group': g, 'gain_grouped': dg, 'gain_hs4': dh, 'notebook_sign_flip': flip})
    df = pd.DataFrame(rows)
    df.to_csv(HERE / 'figures' / f'gains_{year}.csv', index=False)
    summ = []
    for c, d in df.groupby('country'):
        dd = d.dropna(subset=['gain_hs4'])
        bg = d.loc[d.gain_grouped.idxmax(), 'group']
        bg_nos = dd.loc[dd.gain_grouped.idxmax(), 'group']
        bh = dd.loc[dd.gain_hs4.idxmax(), 'group']
        summ.append({'country': c, 'best_grouped': bg, 'best_grouped_excl_services': bg_nos, 'best_hs4': bh,
                     'agree_excl_services': bg_nos == bh, 'spearman_gain_rankings': R.spearman(dd.set_index('group').gain_grouped, dd.set_index('group').gain_hs4)[0],
                     'max_gain_grouped': float(d.gain_grouped.max()), 'max_gain_hs4': float(dd.gain_hs4.max()),
                     'hs4_rank_of_grouped_best': int(dd.gain_hs4.rank(ascending=False)[dd.group == bg_nos].iloc[0])})
    summ = pd.DataFrame(summ)
    summ.to_csv(HERE / 'figures' / f'summary_{year}.csv', index=False)
    res[year] = {'summary': summ.to_dict('records'), 'n_agree': int(summ.agree_excl_services.sum()), 'n_countries': int(len(summ)),
                 'mean_spearman': float(summ.spearman_gain_rankings.mean()),
                 'notebook_base_sign_agrees_with_diversity': bool(nb_base_sign),
                 'notebook_sign_flips': int(nflip_total), 'notebook_perturbations': int(df.notebook_sign_flip.notna().sum()),
                 'best_grouped_counts': summ.best_grouped.value_counts().to_dict(), 'best_hs4_counts': summ.best_hs4.value_counts().to_dict()}
    print(year); print(summ.round(3).to_string()); print({k: v for k, v in res[year].items() if k != 'summary'})
res['runtime_s'] = time.time() - t0
R.save_json(res, HERE / 'results.json')
