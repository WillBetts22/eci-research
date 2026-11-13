# Project 3 — initial horse race

- **Coverage:** 95 common training countries and 129 common test countries; 0 preliminary observations excluded for missing compared measures.
- **ECI validation:** primary-network Pearson correlations with Harvard are 0.920–0.963; rank correlations are 0.968–0.982. Check the disagreement table before treating this as exact replication.
- **Held-out growth errors:** baseline RMSE is 2.164, calculated ECI 2.115, and diversity 2.133 annual percentage points. The smallest observed error belongs to **ECI + diversity** (2.112); this ranking alone does not establish a reliable advantage.
- **ECI versus baseline uncertainty:** mean squared-error reduction is 0.213, with a paired-country 95% bootstrap interval of [-0.272, 0.756]. Positive reductions favor adding ECI. This interval describes these test countries, not uncertainty across future decades.
- **Metric dependence:** calculated ECI's test MAE is 1.643, compared with baseline 1.614. Thus its lower RMSE does not mean lower error under every scoring rule.
- **ECI versus diversity:** the paired mean squared-error reduction is 0.076, with a 95% interval of [-0.285, 0.456]. Positive values favor ECI; an interval spanning zero does not establish that it is better.
- **Network sensitivity:** using all positive-export reporters changes calculated ECI's test RMSE to 2.002. This dependence on network construction warrants further checks; the alternative was not chosen as a new winner after viewing outcomes.
- **What this does not show:** no causal effect, final measure winner, or validation of the lab's grouped ECI has been established. One forecast period, revised data, network choices, and assumed zero exports for absent product cells limit interpretation.
