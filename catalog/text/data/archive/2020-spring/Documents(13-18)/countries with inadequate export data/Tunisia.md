<!-- text mirror of data/archive/2020-spring/Documents(13-18)/countries with inadequate export data/Tunisia.docx — edit the .docx, not this file -->

2. Macroeconomic Results

2.1 GDP Ranking and Changes

As the 92nd largest economy in the world by GDP, Tunisia has a GDP of 46 billion USD in 2013 and 39 billion USD in 2018, exhibiting a decreasing trend in economic output. Figure 1 illustrates the time-series GDP results for major emerging economies from 1999-2018. Tunisia has an average annual growth of -2% during the period from 2013 to 2018. This number is clearly below the average annual growth rate of the other four leading emerging economies, which have a geometric average growth rates of 1.8% and an arithmetic average growth rate of 2.1%. The contrast is particularly significant with China, one of the leading emerging economies in the world, which has an average annual growth rate of 8.2% during the same period. The stagnancy of economic growth in Tunisia, we believe, can be reflected through changes in ECI and PCI, and can be further explained by a suboptimal set of production strategies adopted by Tunisia from 2013 to 2018, which we will expand at the later stage of the report.

Figure 1: GDP Comparison Among Major Emerging Economies

2.2 ECI Ranking and Changes

The Economic Complexity Index (ECI), as defined by Ricardo Hausmann and Cesar Hidalgo in 2009 to explain the knowledge accumulated in a country's population, exhibits a similar pattern for Tunisia. As illustrated in Figure 2 below, Tunisia exhibits a slightly increasing level of production capability from 2013 to 2018, as measured by ECI. This is in direct contrast to countries such as China, which demonstrates a steady trend in terms of both the ECI and GDP indexes.

Figure 2: ECI Comparison                            Figure 3: GDP and ECI (Tunisia)

Figure 3 offers a further comparison of GDP and ECI over the entire time span from 2013 to 2018 for Tunisia. From the graph, it can be observed that the stagnancy of GDP during the period from 2013 to 2018 was accompanied by an increasing ECI, indicating little predictive power of ECI in terms of Tunisia’s potential economic development. In order to get a better insight of the relationship between ECI and the country’s economy, we will dive into an analysis of Tunisia’s production structure and its product space designs in the next few chapters.

4. Product Space Design

4.1 Suggested Development Vector

As aforementioned, distance gives us an idea of how far each new product is from a country’s current mix of exports. As defined in Hausmann and Hidalgo (2009), distance is “the weighted proportion of products connected to goods p that country c is not exporting, i.e., MCP=0.”  Based on this definition, the distance between a country and any product that the country is currently exporting (i.e., the country is a significant exporter in the product as compared to global average) is zero. Similarly, opportunity gain quantifies the contribution of a new product in terms of opening up the doors to more and more complex products. Intuitively, a product that a country is currently exporting (i.e., MCP=1) has an opportunity gain of zero. And unreasonable investment on certain product p would lead to a relative decrement in export of more profitable products, and therefore lead to a negative opportunity gain of product p.  The opportunity gain is not the only estimator of a country’s level of economic development. However, among countries with comparable economics strength, those having higher ECI, or in other words, more reasonable economics structures are often in better shape.

Table 5: Opportunity Gain Ranking on a Regional Scale

We define the ranking of opportunity gain for a country c, as the Suggested Development Vector (SDV) of c. Table 5 and 6 summarize how the SDV of Spain compares with a selected group of regional and leading economies in the world, with the industry groups ranked in decreasing order of significance. Dark blue indicates positive opportunity gain, light blue indicates zero opportunity gains, and white indicates negative opportunity gains. The result shows that leading countries barely have any industries with positive opportunity gain. In other words, those countries are already in the most stable and efficient economic structure. Without the necessity of economic transition, those countries merely need to maintain a steady and balanced economic development.  In contrast, less developed countries have nearly half of industries with positive opportunity gain, and share common interests in industrial manufacturing and High-complexity Products industries. It can be concluded that Tunisia shares the characters of a less developed country as compared with the world’s leading economies and other major economies in Europe, with a premature economics structure that leans towards basic to intermediate level industries.

Table 6: Opportunity Gain Ranking on a Global Scale

4.2 Budgeted Industry Development Strategy and Interpretation

The optimal budgeted industry development strategy aims to solve the most efficient allocations under the budgeted constraint of different situations of heuristic total export growth. In order to obtain such an allocation portfolio, we formulate an optimization problem as the following:

where k(x) is the second largest eigenvector of  after adding  to the original export vector, C is the country that we are interested in, P is the product space, B is the heuristic budget.

If we can solve this problem, then we can know what the largest ECI that a country can improve to. Accordingly, the optimal solution  that we obtain here is exactly our optimal allocation. However, the biggest problem is that the objective function is not convex. Therefore, we cannot apply the classical tools for convex optimization on this problem. In order to solve this problem, our idea is to use greedy algorithm. The way that we apply greedy algorithm is that firstly we separate the total budget into k equal parts, and then for the first equal part we try to search for the product that can optimize our objective function by iterating through each . After we find the optimal product p for this equal part, we add the amount back to the export value of this product p and update the ECI for this country. If we observe that ECI does not change after iterating all the products, then we can add up one more equal part to invest. Until we find there is an ECI increment, we add the amount now to that product. The rest equal parts can be done in the same way.

However, as is known to all, greedy algorithm is a kind of local search algorithm, which is pretty possible to run into a local minimum. Therefore, for local search algorithms, one typical way is to keep it away from the local minimum is to enhance the vision of the algorithm by looking more steps forward. In our setting, whenever we obtain an increment of ECI, we mark down the required amount of export growth. Simultaneously, we continue searching for the next ECI increment point, compare the ratios of these two possibilities and pick the largest one. The ratio is defined as the following:

where  is just the ECI of the country after adding some amount of export increment to product , which is exactly the amount that is able to make ECI change. Also, we can express it in the way of .

In this way, we can obtain a further sighted greedy algorithm. Also, the number of parts that we would like to separate the budget into also matters. In order to solve this problem, we added a stabilizer on top of the enhanced greedy algorithm, by running the algorithm for different number of parts and selecting the portfolio with the largest ECI increment and most complex economic structure.

Besides, it is quite common that there is a surplus for the budget. To deal with the surplus, we just add it to the product which needs the least amount of dollar to make  = 1, (i.e., the smallest amount of required export increase).

Below is the economic panel for Tunisia in 2013. We can see that for different percentages of heuristic total export growth, the ECI of Tunisia has different performance. From all the four line graphs, we see that Tunisia already obtains some great increment in terms of ECI. However, increasing the budget for too large an amount would not produce a higher and higher ECI. One thing to notice is that, even though the growth pattern does not change a lot, the eventual ending point is quite high, which is around eight times of the original ECI. This means that in short terms, Tunisia still has great room to improve. For the four export growth budget, the increment primarily attributes to high-complexity products and daily instruments. Therefore, Tunisia should focus on developing high-complexity products and daily instruments.

4.3 Sensitivity Analysis Results and Interpretation

5. Macro-level Predictions

5.1 Structural Optimality Index

Indeed, such choice of prioritization has proven to be a significant factor in deciding the economic outcomes of countries. In order to quantitatively evaluate how effective our development strategies are and how deviations from the suggested developmental path will lead to suboptimal growth results, we define the measure – Structural Optimality Index (SOI) – on a country level as the Adjusted R-Square obtained from regressing the country’s realized industry development over the suggested development strategy. Both strategies are quantified in nature, with the realized development represented by export increase in every major industry group and the suggested development strategy represented by the opportunity gains of developing the corresponding industry groups as calculated in previous sections. The adjusted R-square from the regression thus provides us with a quantified measure of how the development path adopted by the country has fitted with/differed from calculations on a complexity level.

After obtaining this measure for all countries in our database, we further regress countries’ five-year economic growth, which is defined as the percent increase in GDP (USD), over their SOI. Figure 6 illustrates the regression output, which shows a strong positive correlation between countries’ SOI and their five-year GDP growth, significant at the 1% level and achieving an adjusted R2 of 4.5%. In other words, the more a country develops as suggested by calculations on a complexity level, the better economic outcomes it achieves.

Figure 2: Regression of Five-year GDP Growth over SOI

5.2 SOI of Tunisia and Its Implications

Tunisia, for instance, has a relatively low level of structural optimality as compared with its African peers. As the regression in Figure 7 suggests (the orange curve represents export increase and the blue curve stands for opportunity gain of the corresponding industry), Tunisia demonstrates a moderate level of correlation with the suggested developmental path, having an adjusted R-square of around -6.2%. Tunisia ranks in 105th place among all observed countries in terms of SOI and has slow economic progress among its African peers from 2013 to 2018 with an annual growth rate of 26.5%, which is consistent with the regression result in Figure 6. This is in direct contrast to emerging economies such as Turkey, where there is a high SOI of around 21.8% and a corresponding GDP growth of 36.7%, making it one of the fastest developing economies during the period. In sum, Tunisia’s slower economic progress from 2013 to 2018 can be at least partially explained by a mismatched development strategy that demonstrates a considerable level of deviations from our suggested developmental path.

Figure 7: SOI for Tunisia (2013-2018)

**Table 1**

| Table 18: OLS Regression Results | Table 18: OLS Regression Results |
|---|---|
| Dep. Variable: GDP | F-Statistic: 5.963 |
| R2: 0.054 | Prob (F-Stat): 0.0163 |
| Adj R2: 0.045 | No. Observations: 106 |
