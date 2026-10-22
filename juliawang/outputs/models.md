# Descriptive models

Outcome: recomputed ECI in 2019. Each model uses one diversification measure, with either a linear term or linear and squared terms. Coefficients and scores are in model_comparison.csv.

R² measures fit to the same 119 countries used for estimation. Leave-one-country-out RMSE (LOO RMSE) checks whether curvature improves held-out-country reconstruction, but is not an independent forecast test: ECI itself is computed jointly using the full country network. No models here estimate growth or causality. Do not select a preferred model from in-sample R² alone.

Entropy and HHI describe export shares; RCA diversity counts specialization groups. ECI's sign was oriented positively to RCA diversity, so the direction of that association is partly conventional. All measures share the underlying trade data.

    predictor     model   n  r_squared  loo_rmse    beta_0    beta_1    beta_2
      entropy    Linear 119   0.155912  0.932498 -1.484503  0.790598       NaN
      entropy Quadratic 119   0.157750  0.938388 -1.736683  1.175592 -0.124688
rca_diversity    Linear 119   0.158262  0.933179 -1.066373  0.194928       NaN
rca_diversity Quadratic 119   0.162596  0.938331 -1.389786  0.330008 -0.012189
          hhi    Linear 119   0.109157  0.958437  0.486626 -1.909169       NaN
          hhi Quadratic 119   0.114020  0.963330  0.273478 -0.449290 -1.674733
