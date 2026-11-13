# Proposals from the all-questions batch (Q03-Q16), 2026-11-12

Source: `paper/eci_fourteen_tests.pdf` and `runs/2026-11-12_Q03..Q16/`. The queue is now exhausted; these are candidates to promote into `QUEUE.md`. Each fits one night.

1. **Port the reports to oriented HS4 ECI (dry run).** For the 7 Spring 2026 countries, recompute every ECI sentence in the report template with HS4 ECI aggregated to groups for presentation, and list which claims change. Highest-impact follow-up of Q04/Q09/Q13.
2. **Fix the notebook's sign in place (on a copy) and rerun one greedy budget level for one 2022 country.** Q11 shows the 2022 base sign is reversed, so past greedy allocations optimized minus-complexity. Measure how different the allocation is.
3. **Why the ECI-growth slope fell after 2005 (Q12/Q16).** Split by region and by China-exposure (share of a country's export basket in products where China's market share rose most), and test whether the slope decline comes from a few groups.
4. **Human capital vs ECI horse race out of time (Q14 + Q16).** Add PWT `hc` (and Barro-Lee) as a candidate in the rolling-origin test. If it beats every ECI variant, that is the clearest evidence that ECI is a proxy.
5. **Why our ECI predicts worse than the Growth Lab's on the same trade data (Q12: 0.566 vs 0.749).** Replicate their cleaning (3-year averages, product filters, services) step by step and see which step carries the predictive gain.
6. **Mirror data for commodity exporters (Q13).** Saudi Arabia's 2019 pull is $49B vs the Growth Lab's $189B. Compare reporter vs partner-reported (mirror) exports for the 20 largest commodity exporters.
7. **HS6 localization fix (Q04).** Test a minimum-ubiquity product filter or a regularized eigenvector at HS6 to see whether the extra granularity helps once the Gabon/Suriname localization is removed.
8. **EU-28 row and aggregate drop as one cleaning change** (Q02/Q05): rebuild 2019-2022 with HS 84 fixed and EU-28 removed, and recompute the greedy's one-step targets (cheap version of Q11).
