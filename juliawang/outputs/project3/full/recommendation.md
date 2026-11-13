# Project 3 — recommendation and limits

1. **Use product-level HS4 ECI as a research benchmark, with diversity as a required simpler comparator.** In the original held-out decade, HS4 ECI RMSE is 2.115, diversity 2.133, and baseline 2.164. HS4 ECI improves on baseline in 6 of 7 additional designs. But its primary paired MSE advantage over diversity has a 95% interval [-0.278, 0.456], so a reliable advantage over diversity is not established.

2. **The lab's goods-only grouped ECI is not yet justified as the main growth-forecast score.** Primary test RMSE is 2.171 for 18 groups and 2.156 without the overlapping aggregate. Compare 2.118 for HS4 using the same product coverage as the 17 groups. This points toward information loss from aggregation in this design, while period results and uncertainty prevent a universal conclusion. This is a reconstruction from goods data, not a complete validation of the services-inclusive report index.

3. **Treat overlap and coverage as separate problems.** In 1998 the 18-group sums are 117.8% of goods exports; the 17-group coverage is 84.2%. Merely dropping the overlapping category therefore also changes coverage. Do not silently substitute these variants in production reports.

4. **No universal alternative winner emerges.** Continuous log(1+RCA) ECI has primary RMSE 2.220 and improves on baseline in 5 of 7 additional designs. Fitness at 200 iterations has RMSE 2.293; no annual network reached the specified log-value convergence tolerance at either recorded iteration count. Its finite-iteration comparison cannot settle the merits of converged Fitness.

5. **Error concentration and scoring choices matter.** After removing the five largest baseline misses (diagnostic only), primary HS4 ECI RMSE is 1.804 and baseline 1.784. Inspect the saved paired intervals and contribution tables rather than declaring a winner from average errors alone. Rankings across the alternative designs are exploratory and overlapping periods are not independent evidence.

**Practical recommendation:** retain both product-level ECI and diversity in the lab's validation work; review the grouped mapping before relying on its growth predictions. More out-of-time validation and a resolved Fitness specification would strengthen measure selection. These results do not establish that raising any score causes growth or validates an ECI-maximizing investment budget.
