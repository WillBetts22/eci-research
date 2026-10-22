"""Plot descriptive OLS fits. Requires NumPy, pandas, and Matplotlib."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / 'outputs'

def fit(x, y):
    beta = np.linalg.lstsq(x,y,rcond=None)[0]
    pred = x @ beta
    residual = y - pred
    r2 = 1 - (residual @ residual) / ((y-y.mean()) @ (y-y.mean()))
    # Exact leave-one-country-out OLS error using leverage.
    leverage = np.sum(x * (x @ np.linalg.inv(x.T @ x)), axis=1)
    loo_rmse = np.sqrt(np.mean((residual/(1-leverage))**2))
    assert np.allclose(x.T @ residual, 0, atol=1e-8)
    return beta,pred,r2,loo_rmse

def run():
    r = pd.read_csv(OUT/'2019_common_metrics.csv')
    y = r.eci.to_numpy()
    configs = [('Entropy','entropy'),('RCA diversity','rca_diversity'),('Concentration (HHI)','hhi')]
    rows = []
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig, axes = plt.subplots(1,3,figsize=(15,5.4))
    for ax,(label,col) in zip(axes,configs):
        v = r[col].to_numpy(); grid=np.linspace(v.min(),v.max(),200)
        ax.scatter(v,y,s=25,alpha=.65,color='#237d9b',edgecolor='white',linewidth=.3)
        for degree,color,name in [(1,'#df7541','Linear'),(2,'#7047a3','Quadratic')]:
            x=np.column_stack([v**i for i in range(degree+1)])
            beta,pred,r2,rmse=fit(x,y)
            g=np.column_stack([grid**i for i in range(degree+1)])
            ax.plot(grid,g@beta,color=color,lw=2,label=f'{name}: R²={r2:.2f}')
            row={'predictor':col,'model':name,'n':len(y),'r_squared':r2,'loo_rmse':rmse}
            row.update({f'beta_{i}':b for i,b in enumerate(beta)}); rows.append(row)
        ax.set(xlabel=label,ylabel='Recomputed ECI',title=label)
        ax.legend(loc='upper left',fontsize=9,frameon=False)
        ax.grid(alpha=.15)
    fig.suptitle('Does diversification explain ECI?  |  2019, 119 countries',fontsize=17,y=.99)
    fig.text(.5,.015,'Descriptive fits; grouped local ECI. Overlapping aggregate excluded. ECI sign oriented to RCA diversity.',ha='center',fontsize=10,color='#555555')
    fig.tight_layout(rect=(0,.06,1,.93)); fig.savefig(OUT/'models_2019.png',dpi=180);plt.close(fig)
    scores=pd.DataFrame(rows); scores.to_csv(OUT/'model_comparison.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(12,5.4))
    corr=pd.read_csv(OUT/'correlations.csv'); corr=corr[corr['sample']=='common']
    for label,col in configs:
        part=corr[corr.metric==col]
        axes[0].plot(part.year,part.spearman_rho,marker='o',label=label)
    axes[0].axhline(0,color='gray',lw=.8)
    axes[0].set(title='Rank associations across years',xlabel='Year',ylabel='Spearman rank correlation',ylim=(-.6,.7),xticks=range(2019,2024))
    axes[0].legend(frameon=False,fontsize=9)
    axes[0].grid(alpha=.15)
    axes[1].scatter(r.entropy_rank,r.eci_rank,color='#237d9b',alpha=.65,s=25)
    axes[1].plot([1,119],[1,119],color='#df7541',ls='--',label='Identical rankings')
    axes[1].set(title='Rank disagreements, 2019',xlabel='Diversification rank (entropy)',ylabel='ECI rank',xlim=(122,0),ylim=(122,0))
    axes[1].legend(frameon=False); axes[1].grid(alpha=.15)
    fig.suptitle('Positive association does not mean identical rankings',fontsize=16)
    fig.text(.5,.015,'Fixed country sample; each year standardized separately. 2023 data have a documented quality flag.',ha='center',fontsize=10,color='#555555')
    fig.tight_layout(rect=(0,.06,1,.93));fig.savefig(OUT/'robustness_and_ranks.png',dpi=180);plt.close(fig)
    note='''# Descriptive models

Outcome: recomputed ECI in 2019. Each model uses one diversification measure, with either a linear term or linear and squared terms. Coefficients and scores are in model_comparison.csv.

R² measures fit to the same 119 countries used for estimation. Leave-one-country-out RMSE (LOO RMSE) checks whether curvature improves held-out-country reconstruction, but is not an independent forecast test: ECI itself is computed jointly using the full country network. No models here estimate growth or causality. Do not select a preferred model from in-sample R² alone.

Entropy and HHI describe export shares; RCA diversity counts specialization groups. ECI's sign was oriented positively to RCA diversity, so the direction of that association is partly conventional. All measures share the underlying trade data.

'''
    (OUT/'models.md').write_text(note+scores.to_string(index=False)+'\n')
    print(scores.to_string(index=False))

if __name__=='__main__': run()
