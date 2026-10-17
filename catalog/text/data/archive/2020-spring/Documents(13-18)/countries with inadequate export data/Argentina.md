<!-- text mirror of data/archive/2020-spring/Documents(13-18)/countries with inadequate export data/Argentina.docx — edit the .docx, not this file -->

Optimal Industry Development Strategy for Argentina

0. Executive Summary

In this report, we aim to uncover the economic path Argentina went through during the period from 2009 to 2014. Specifically, we dive into the topic through a macroeconomic overview of Argentina from the perspective of Gross Domestic Product (GDP) and Economic Complexity Index (ECI), which reflect countries’ production capability and production structure, respectively. We find that during the period of our interest, Argentina demonstrated a low level of economic growth with an annual GDP growth rate of 8.2%, concurrent with a decrease in economic complexity as compared with other major economies in South America.

The level of economic progress during the period, we believe, can be partially explained through analysis of the economic and product complexity structure of Argentina on the industry group level. The product classification system we adopt allows us to measure the realized industry development for various industry groups and to observe that Argentina invested heavily in developing Animals and By-products, Clothing and Accessories and Textiles during the period, while its emerging peers and developed economies around the globe have adopted much more complex and progressive paths.

Based on our analysis of the opportunity gain and a sensitivity analysis of major industry groups, Argentina can further its gains by prioritizing High-complexity Products, Services and Utilities, and Food and Preparations. We further note that Argentina has a slightly mismatched development strategy that indicates a moderate level of structural optimality on the complexity level, having an adjusted R-square of around 4.5%. Since a significant positive correlation exists between five-year GDP growth and the structural optimality index of an economy as we define and calculate, Argentina indeed has a suboptimal growth experience as compared with fast-growing economies both on a regional scale and on a global scale, and has the potential to further its economic gains through industrial structure optimization as suggested in the paper.

2. Macroeconomic Results

2.1 GDP Ranking and Changes

As the 28th largest economy in the world by GDP, Argentina has a GDP of 552 billion USD in 2013 and 519 billion USD in 2018, exhibiting an extraordinary level of economic output. Figure 1 illustrates the time-series GDP results for major emerging economies from 1999-2018, and Argentina demonstrates a high level of consistency in terms of both GDP and GDP growth. However, its growth rate is not as good as compared with many other emerging economies in the world, with an average annual growth of -0.1% during the period from 2013 to 2018. This number is much below the annual growth rates of the other six leading emerging economies, which have a geometric average growth rate of 2.2% and an arithmetic average growth rate of 2.4%. The contrast is particularly significant with China, one of the leading emerging economies in the world, which has an average annual growth rate of 8.2% during the same period. The pace of economic growth in Argentina, we believe, can be reflected through changes in ECI and PCI, and can be further explained by a suboptimal set of production strategies adopted by Brazil from 2013 to 2018, which we will expand at the later stage of the report.

Figure 1: GDP Comparison Among Major Emerging Economies

2.2 ECI Ranking and Changes

The Economic Complexity Index (ECI), as defined by Ricardo Hausmann and Cesar Hidalgo in 2009 to explain the knowledge accumulated in a country's population, exhibits a similar pattern for Brazil. As illustrated in Figure 2 below, Argentina exhibits a stably low production capability from 2013 to 2018, as measured by ECI. This is in direct contrast to countries such as China and South Korea, which demonstrate an advantage in terms of both the ECI and GDP indexes.

Figure 2: ECI Comparison                           Figure 3: GDP and ECI (Argentina)

Figure 3 offers a further comparison of GDP and ECI over the time span from 2013 to 2018 for Argentina. There’s a strong negative correlation between ECI and GDP, indicating the ineffectiveness of the country in developing a competitive product space that helps to accumulate complicated knowledge and technology, and that ECI doesn’t have the predictive power to estimate the potential economic development of Argentina,. In order to provide a more concrete answer to why this has happened, we will dive into an analysis of Argentina’s production structure and its product space designs in the next few chapters.

4.2 Budgeted Industry Development Strategy and Interpretation

The optimal budgeted industry development strategy aims to solve the most efficient allocations under the budgeted constraint of different situations of heuristic total export growth. In order to obtain such an allocation portfolio, we formulate an optimization problem as the following:

where k(x) is the second largest eigenvector of  after adding  to the original export vector, C is the country that we are interested in, P is the product space, B is the heuristic budget.

If we can solve this problem, then we can know what the largest ECI that a country can improve to. Accordingly, the optimal solution  that we obtain here is exactly our optimal allocation. However, the biggest problem is that the objective function is not convex. Therefore, we cannot apply the classical tools for convex optimization on this problem. In order to solve this problem, our idea is to use greedy algorithm. The way that we apply greedy algorithm is that firstly we separate the total budget into k equal parts, and then for the first equal part we try to search for the product that can optimize our objective function by iterating through each . After we find the optimal product p for this equal part, we add the amount back to the export value of this product p and update the ECI for this country. If we observe that ECI does not change after iterating all the products, then we can add up one more equal part to invest. Until we find there is an ECI increment, we add the amount now to that product. The rest equal parts can be done in the same way.

However, as is known to all, greedy algorithm is a kind of local search algorithm, which is pretty possible to run into a local minimum. Therefore, for local search algorithms, one typical way is to keep it away from the local minimum is to enhance the vision of the algorithm by looking more steps forward. In our setting, whenever we obtain an increment of ECI, we mark down the required amount of export growth. Simultaneously, we continue searching for the next ECI increment point, compare the ratios of these two possibilities and pick the largest one. The ratio is defined as the following:

where  is just the ECI of the country after adding some amount of export increment to product , which is exactly the amount that is able to make ECI change. Also, we can express it in the way of .

In this way, we can obtain a further sighted greedy algorithm. Also, the number of parts that we would like to separate the budget into also matters. In order to solve this problem, we added a stabilizer on top of the enhanced greedy algorithm, by running the algorithm for different number of parts and selecting the portfolio with the largest ECI increment and most complex economic structure.

Besides, it is quite common that there is a surplus for the budget. To deal with the surplus, we just add it to the product which needs the least amount of dollar to make  = 1, (i.e., the smallest amount of required export increase).

For further suggestions on Argentina’s development in the future. We also offer the optimization result of Argentina based on export data in 2018. Below is the economic panel for Argentina in 2018. From all the four line graphs, we see that Argentina already obtains some great increment in terms of ECI. Most importantly, the higher the budget is, the greater the ECI will be. This means that in both short term and long term, Colombia still has great room to improve. For the case of 5 percent, the ECI increment is mainly caused by chemical manufacturing and textiles. For 10 and 15 percent growth, ECI increment can be attributed to the development of daily instruments and chemical products. For the case of 20 percent growth, ECI can grow much higher than all the previous cases, mainly because of the introduction of machinery and construction. Therefore, for future strategy, Indonesia should prioritize development of chemical manufacturing, and then chemicals and daily instruments, and eventually machinery and construction, in order to optimize ECI.

4.3  Sensitivity Analysis

In the following section our broad aim is to understand how sensitive Argentina is to changes in export in various industries. While the Economic Complexity Index has been shown to contain valuable information about the economic strength/capacity of a country, little has been said as to the stability of the measure itself. We seek to uncover the main drivers of stability under a country's ECI score and better understand longer-term projections for ECI growth. Additionally, gaining an intuition on the industries that are bolstering an economy and the industries that offer the greatest return per unit of investment is best done through visualization of industry specific sensitivity. To this end, we have developed two categories of sensitivity analysis.

ECI Sensitivity Graph

Firstly, in order to assess the effect particular industries have on each respective country, we developed ECI Sensitivity graphs. We use shocking methodology to increment or decrement an industry’s export level by a certain percentage and recalculate the ECI all else being equal. While freezing the export dynamics of the rest of the world and enacting an instantaneous shock in export for a particular industry and country may not reflect real-life dynamics, what it does offer us is an understanding of a country’s level of dependency on an industry in the context of ECI. The shocking is done in small percentage increments in order to smooth out the resulting curve. Additionally, a recurring theme one will see is that for most industries, a breaking point occurs where the ECI either jumps upwards or downwards, creating a hockey stick shape rather than a linear trend. While the inflection point may not be accurate in context of real life, comparing the various inflection points across industries can give us valuable insight.

The graphs are formulated as follows: There are four ECI Sensitivity graphs. The first two represent data from 2018. The first chart shows positive shocking in which export numbers are shocked upwards per industry. The X-axis is in terms of percentage shock per current dollar value of export. The Y-axis is the recalculated ECI level post-shocking. The second chart follows the same format except the X-axis represents negative shocking. In other words, exports for each industry are decremented and the ECI is accordingly recomputed. The final two sensitivity graphs show the same results using 2013 data. Below is an example of an ECI sensitivity graph.

Example 2018 (Incremental ECI Sensitivity)

4.3 Sensitivity Analysis Results and Interpretation

Below is Argentina’s 2018 ECI Sensitivity Charts. Firstly in the positive chart, we notice that increases in export of High Complexity Products and Transportation lead to large gains in ECI, however expansions of over 150% and 200% in Transportation and High Complexity Products respectively are required to experience the ECI growth.

Next we consider Argentina’s 2018 Negative Shock chart. Interestingly no industries actually cause the ECI to drop when exports are decreased. Instead there are quite a few industries such as Food and Preparations and Services and Utilities that actually improve ECI when exports are decreased by 20-40%.

Argentina 2018 (Incremental ECI Sensitivity)

Argentina 2018 (Decremental  ECI Sensitivity)
