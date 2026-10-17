<!-- text mirror of code/archive/2022-fall/New Country Reports/United Kingdom (Updated 2021).docx — edit the .docx, not this file -->

https://atlas.cid.harvard.edu/

# Optimal Industry Development Strategy Using Economic and Product Complexity

# United Kingdom

─

The Economic Complexity Lab - Columbia University

Haoxian Chen, Davepriyan Gunaratnam, Rohan Macherla, Ajit Akole, Shomik Ghose, Alex Wei-Liang Ku, Sannidhya Modi, Xilin Wang, Alexandra Garcia, Kelly Mi, Alex Chung, Margarita Demkina

Optimal Industry Development Strategy for United Kingdom

0. Executive Summary

In this report, we aim to uncover the economic path the UK went through during the period from 2013 to 2018. We include an additional analysis regarding the impact of COVID-19 on the country’s development in 2021. Specifically, we dive into the topic through a macroeconomic overview of the UK from the perspective of Gross Domestic Product (GDP) and Economic Complexity Index (ECI), which reflect countries’ production capability and production structure, respectively. We find that between 2013 and 2018, the UK demonstrated a low level of economic growth with an average annual GDP growth rate of 3.03%, concurrent with an increase in economic complexity as compared with other major developed economies. Average annual GDP growth increased to 3.79% between 2019 to 2021, but economic complexity decreased, again in line with other major developed economies.

The mixed progress during 2013 to 2018, we believe, can be partially explained through analysis of the economic and product complexity structure of the UK on the industry group level. The product classification system we adopt allows us to measure the realized industry development for various industry groups and to observe that the UK consistently relied on developing the Chemicals, Machinery and Construction, and Daily Instruments industries during the period, while some of its developed counterparts and emerging economies around the globe adopted much more complex and progressive paths. Regarding the post-COVID decline in economic complexity coupled with a higher GDP as observed in 2021, we determine that the UK prioritized basic, low complexity industries such as Food and Preparations and Daily Instruments in reaction to the higher global demand for such products in the midst of a pandemic.

Based on our analysis of the opportunity gain and a sensitivity analysis of major industry groups, the UK can further its gains by prioritizing High-Complexity Products and Transportation. We further note that the UK has a heavily mismatched development strategy between 2013 and 2018 that indicates a low level of structural optimality (compared to other developed countries) on the complexity level, having an adjusted R-square of around 1.84%. In 2021, adjusted R-square is 5.07%, which is still low relative to other developed countries. Since a significant positive correlation exists between five-year GDP growth and the structural optimality index of an economy as we define and calculate, the UK indeed has a comparable growth experience with fast-growing economies both on a regional scale and on a global scale, and has the potential to further its economic gains through industrial structure optimization as suggested in the paper.

1. Report Overview

In this report, we aim to uncover the economic path the UK went through during the period from 2013 to 2018, and the impact of COVID-19 on its economic development as observed in 2021. Specifically, we dive into the topic through a macroeconomic overview of the UK from the perspective of Gross Domestic Product (GDP) and Economic Complexity Index (ECI), which reflect countries’ production capability and production structure, respectively. We then analyze the industrial framework and changes of the UK during the period based on quantitative measures such as Product Complexity Index (PCI) and Product Family Complexity Index (PfCI), followed by a detailed analysis of how such changes have matched with development strategies as quantitatively measured by opportunity gains on an industry-level. We conclude our report with macro-level results and predictions of the UK, as deduced from regression models we have established on a global scale, which take into account countries’ stances in their product space.

2. Macroeconomic Results

2.1 GDP Ranking and Changes

Figure 1 illustrates the time-series GDP results for the UK and two of its peer countries (France and Italy) from 2013-2018. Similar to the other countries, the UK displayed upward growth over the period. Furthermore, the UK’s average annual growth rate of 3.03% over the five-year period is comparable to those of its peers, which are 2.59% and 2.46% for France and Italy, respectively.

Figure 1: GDP Comparison Among Leading Economies (2013-2018)

Figure 2 illustrates the time-series GDP results in 2019-2021. Similar to the other countries, the UK displayed upward growth over the period, despite an observed decrease in GDP in 2020 due to the economic implications of COVID-19. Yet, it displayed a greater increase of 0.73% in average annual growth rate, up to 3.79%; whereas France only increased 0.10%, up to 2.69%, and Italy decreased 0.78%, down to 1.68%.

Figure 2: GDP Comparison Among Leading Economies (2019-2021)

2.2 ECI Ranking and Changes

The Economic Complexity Index (ECI), as defined by Ricardo Hausmann and Cesar Hidalgo in 2009 to explain the knowledge accumulated in a country's population is illustrated in Figure 3. As shown, the UK exhibits a significant increase in production capability from 2013 to 2018. The UK (63.22% ECI change) is the country in the peer group with the greatest increase in ECI change, as France  attained a significantly lower ECI change (16.37%) and Italy (-31.46%) saw decreases in production capability over the period.

Figure 3: ECI Comparison (2013-2018)

However, as shown in Figure 4, the UK exhibits a significant decrease in production capability from 2019 to 2021. Its peers also experienced comparable decreases in production capability over the period, as marked by a sharp decline following 2020.

Figure 4: ECI Comparison (2019-2021)

Figure 5 offers a further comparison of GDP Growth and ECI over the time span from 2013 to 2018 for the UK. The steady increase in GDP growth during the period from 2013 to 2018 is accompanied by a volatile eventual increase in ECI. The results show that the economic growth experienced by the UK during the period from 2013 to 2018, though relatively stable, is only partially consistent with the predictions by ECI and that the UK made some progress in effectively developing a competitive product space that helps to accumulate complicated knowledge and technology. In order to provide a more concrete answer to why this has happened, we will dive into an analysis of the UK’s production structure and its product space designs in the next few chapters.

Figure 5: GDP Growth and ECI (2013-2018)

Figure 6 compares GDP Growth and ECI between 2019 and 2021 for the UK. The decrease followed by a sharp increase in GDP growth during the period from 2019 to 2021 is paralleled by opposite changes in ECI. The COVID-19 pandemic in 2020 necessitated a prioritization of low complexity industries as demand for basic, essential products replaced that of higher-complexity, discretionary products. This explains the inconsistency in the relationship between GDP and ECI presented by the UK over this period.

Figure 6: GDP and ECI (2019-2021)

3. Production Analysis

3.1 Product Categorization

Our main data source in this research is the UN Comtrade Website (https://comtrade.un.org), which provides us with valuable information on countries’ export values on an annual basis, including highly specific export data for more than 5000 categories of products. In order to have a holistic vision of the product space of a country, however, a level of categorization is required. Products in our data source are labelled from 010000-999999, with the first two-digits representing a general category to which the product belongs. Based on the 99 categories as extracted from the label, we further group the products into 18 most widely-accepted industries, as summarized in Table 1.

Note that the High-complexity Products industry group is not a distinct industry but rather an aggregated industry that encompasses the most complicated products from the most technologically-advanced industries (as measured by PCI). This industry serves as an indicator for us to quantitatively evaluate how well a country has performed in developing cutting-edge technologies and closing its technical gap with advanced economies, which has become a topic of wide concern today. Indeed, when we rank the 18 categories based on PfCI (an equivalent concept of PCI as calculated based on the 18 categorized product groups), the High-complexity Products industry has the highest PfCI among all industry groups.

Table 1: Categorization of Products

We further observe a positive correlation between the GDP and the export of High-complexity Products. A higher adjusted R-square exists between GDP and High-complexity Products exports, indicating that more successful economics, as measured by GDP, tend to be those that are capable of producing and exporting High-complexity Products as we define them. The Figure 3 and 4 show the OLS results in a universe of 107 and 21 typical countries respectively.

Figure 3: OLS Regression Results of GDP against Percentage Volume of Exports

Figure 4: OLS Regression Results of GDP against Volume of Percentage Exports

3.2 Realized Industry Development

Based on the product categorization aforementioned, we aim to capture the UK’s realized industry production strategy between 2013 and 2018 on a complexity level. In Hausmann and Hidalgo (2009), distance is defined to be a measure of how far a country is from a certain product not in its product space. We extend this concept to all product groups and quantify how technically equipped a country is to develop the corresponding product groups. In other words, the shorter the distance between a country and a product group, the more capable a country is in developing products within that group. Defining this net distance change as the Realized Industry Development (RID), our export data allow us to calculate and compare RID of the UK and the 18 product groups in 2018 and 2021 through subtraction, where a positive RID indicates a shortening of the distance (i.e., advancement of the industry), and a negative RID indicates the reverse.

Table 2: Realized Industry Development (RID) of UK (2013-2018)

Table 3: Realized Industry Development (RID) of UK (2019-2021)

Between 2013 and 2018, the UK shows advancement in around half of the product groups, with negative RIDs pertaining mostly to low-complexity industries. However, the UK demonstrates a regressive trend in ECI between 2019 and 2021, as every previously positive RID industry changes to negative, and most other industries’ RIDs increase in negativity.

3.3 Regional and Global Comparison

Table 3 and 4 below summarize how the production strategy adopted by the UK compares with leading economies and a selected group of emerging economies in the world, as measured in RID.

Table 4a: RID Comparison across Leading Economies (2018)

Table 4b: RID Comparison across Leading Economies (2021)

Table 4c: RID Comparison across Emerging Economies (2018)

Table 4d: RID Comparison across Emerging Economies (2021)

Tables 4c and 4d further examines UK’s development strategy against those of emerging economies on a global scale. Reasonably, emerging economies such as China, South Korea, Singapore, and India have devoted the majority of their efforts into intermediate industry groups while developed economies such as the UK should have relied more on advanced industry groups. This trend holds true in general, regardless of the continent or the time period, and serves as an indicator for which phase of development a country is currently in as evaluated from its production strategy. Based on this standard, UK is indeed adopting a moderate but slightly out-of-phase strategy that seeks development in industry groups with a lower level of complexity than it should.

4. Product Space Design

4.1 Suggested Development Vector

As aforementioned, distance gives us an idea of how far each new product is from a country’s current mix of exports. As defined in Hausmann and Hidalgo (2009), distance is “the weighted proportion of products connected to goods p that country c is not exporting, i.e., MCP=0.”  Based on this definition, the distance between a country and any product that the country is currently exporting (i.e., the country is a significant exporter in the product as compared to global average) is zero. Similarly, opportunity gain quantifies the contribution of a new product in terms of opening up the doors to more and more complex products. Intuitively, a product that a country is currently exporting (i.e., MCP=1) has an opportunity gain of zero. And unreasonable investment on certain product p would lead to a relative decrement in export of more profitable products, and therefore lead to a negative opportunity gain of product p.  The opportunity gain is not the only estimator of a country’s level of economic development. However, among countries with comparable economic strength, those having higher ECI, or in other words, more reasonable economic structures are often in better shape.

Table 5: SDV of High EfCI Countries 2013(up), 2018(down)

We define the ranking of opportunity gain for a country c, as the Suggested Development Vector (SDV) of c. Table 5 shows the SDV of a selected group of leading economies with outstanding economic complexity, with the industry groups ranked in decreasing order of significance. Dark blue indicates positive opportunity gain, light blue indicates zero opportunity gains, and white indicates negative opportunity gains. The result shows that leading countries barely have any industries with positive opportunity gain. In other words, those countries are already in the most stable and efficient economic structure. Without the necessity of economic transition, those countries merely need to maintain a steady and balanced economic development. In contrast, countries listed in Table 6 have nearly half of industries with positive opportunity gain. While the economies with absolute negative ECI, such as South Africas and Colombia, all need to develop High-complexity Products, Machinery and Construction and Daily Instruments, those with median ECI are facing a more complicated and diverse situation, such as Italy and Spain. We focus on SDV results for 2018 because they give the most accurate snapshot of complexity for global comparison in the absence of the irregular effects of the COVID-19 pandemic observed in 2021.

It can be concluded that the United Kingdom is categorized to be a highly complex country as compared with the world’s leading economies and other major economies in Europe.

Table 6: SDV of Other Typical Countries 2013

4.2 Budgeted Industry Development Strategy and Interpretation

The optimal budgeted industry development strategy aims to solve the most efficient allocations under the budgeted constraint of different situations of heuristic total export growth. In order to obtain such an allocation portfolio, we formulate an optimization problem as the following:

where k(x) is the second largest eigenvector of  after adding  to the original export vector, C is the country that we are interested in, P is the product space, B is the heuristic budget.

If we can solve this problem, then we can know what the largest ECI that a country can improve to. Accordingly, the optimal solution  that we obtain here is exactly our optimal allocation. However, the biggest problem is that the objective function is not convex. Therefore, we cannot apply the classical tools for convex optimization on this problem. In order to solve this problem, our idea is to use greedy algorithm. The way that we apply greedy algorithm is that firstly we separate the total budget into k equal parts, and then for the first equal part we try to search for the product that can optimize our objective function by iterating through each . After we find the optimal product p for this equal part, we add the amount back to the export value of this product p and update the ECI for this country. If we observe that ECI does not change after iterating all the products, then we can add up one more equal part to invest. Until we find there is an ECI increment, we add the amount now to that product. The rest equal parts can be done in the same way.

However, as is known to all, greedy algorithm is a kind of local search algorithm, which is pretty possible to run into a local minimum. Therefore, for local search algorithms, one typical way is to keep it away from the local minimum is to enhance the vision of the algorithm by looking more steps forward. In our setting, whenever we obtain an increment of ECI, we mark down the required amount of export growth. Simultaneously, we continue searching for the next ECI increment point, compare the ratios of these two possibilities and pick the largest one. The ratio is defined as the following:

where  is just the ECI of the country after adding some amount of export increment to product , which is exactly the amount that is able to make ECI change. Also, we can express it in the way of .

In this way, we can obtain a further sighted greedy algorithm. Also, the number of parts that we would like to separate the budget into also matters. In order to solve this problem, we added a stabilizer on top of the enhanced greedy algorithm, by running the algorithm for different number of parts and selecting the portfolio with the largest ECI increment and most complex economic structure.

Besides, it is quite common that there is a surplus for the budget. To deal with the surplus, we just add it to the product which needs the least amount of dollar to make  = 1, (i.e., the smallest amount of required export increase).

Interpretation:

For the purpose of a clear explanation of the line charts, we try to label all the products in Table 7. Please refer to this table when trying to understand the investment trajectories in the line charts.

Table 7: Products Labeling

Below is the economic panel for the UK in 2013. We can see that for different percentages of heuristic total export growth, the ECIs of the United Kingdom actually have similar amounts of increments. Overall, 5, 10, 15, and 20 percent export growth result in a similar ECI improvement pattern, which starts from around 0.92 and ends at around 1.09.

Among all four cases (5, 10, 15 and 20 percent export growth), energy drilling and mining, vegetables, daily instruments and chemicals account for the allocation portfolio. Compared with the solution of other countries, it is obvious that there is not so much room for ECI improvement, which can be reasoned by the pretty well-rounded economic structure of the United Kingdom. Therefore, carrying on the current production pattern is sufficient for maintaining the ECI at an advanced level. Additionally, given that there is a pretty developed economic structure, the United Kingdom should focus more on the development of energy drilling and mining, which can be beneficial for the production of other industries.

Figure 5: Greedy Based ECI Improvement Results of the United Kingdom in 2013 with Different Budgets

Table 8: Portfolio of the United Kingdom in 2013

For further suggestions on the United Kingdom’s development in the future. We also offer the optimization result based on export data in 2018. Below is the economic panel for the United Kingdom in 2018. We can see that there is a similar pattern for the ECI improvement trajectories, which is that the improvements in 5, 10, 15 and 20 percent export growth all result in the ECI growth from 1.31 to 1.86. Again, since the United Kingdom is a pretty developed economic entity, the optimization result is very sparse and there are not so many suggestions for future development in terms of ECI improvement. However, one difference between 2013 and 2018 is that energy drilling and mining, which accounts for most of the portfolio in 2013, is now replaced by services and utilities. Additionally, transportations and high-complexity products become more and more important and serve as the second and third largest component in all scenarios. This can be resulted by the growing demand of technology innovation in nowadays society. A more detailed numerical representation of the portfolio is shown in Table 9.

Figure 6: Greedy Based ECI Improvement Results of the United Kingdom in 2018 with Different Budgets

Table 9: Portfolio of the United Kingdom in 2018

Updated export data for 2021 yields the following ECI improvement trajectories for the United Kingdom. A new pattern thus emerges with improvements in 5, 10, 15 and 20 percent export growth, as all result in distinct ECI growth, with maximum growth of 1.21 (up from -0.892) reached at 15% export growth. Given the necessary change in exports as a result of the COVID-19 pandemic, 2021 data presents greater potential for development, or more accurately “recovery” development. As in 2013, Energy Drilling and Mining composes as significant part of the portfolio in all scenarios, but unlike in 2018, Services and Utilities contributes minimally. Interestingly, more rudimentary industries like Vegetables, Fruits, and Plants and Precious Stones are shown to contribute significantly, suggesting that in their export strategy in reaction to COVID-19, the UK regressed in terms of complexity, and the next steps to optimize its ECI growth require moving through less complex businesses as in the case of a less developed country.

Figure 7: Greedy Based ECI Improvement Results of the United Kingdom in 2021 with Different Budgets

Table 10: Portfolio of the United Kingdom in 2021

4.3  Sensitivity Analysis and Contingency Strategy

In the following section our broad aim is to understand how sensitive the UK is to changes in export in various industries. While the Economic Complexity Index has been shown to contain valuable information about the economic strength/capacity of a country, little has been said as to the stability of the measure itself. We seek to uncover the main drivers of stability under a country's ECI score and better understand longer-term projections for ECI growth. Additionally, gaining an intuition on the industries that are bolstering an economy and the industries that offer the greatest return per unit of investment is best done through visualization of industry specific sensitivity. To this end, we have developed two categories of sensitivity analysis.

ECI Sensitivity Graph

Firstly, in order to assess the effect particular industries have on each respective country, we developed ECI Sensitivity graphs. We use shocking methodology to increment or decrement an industry’s export level by a certain percentage and recalculate the ECI all else being equal. While freezing the export dynamics of the rest of the world and enacting an instantaneous shock in export for a particular industry and country may not reflect real-life dynamics, what it does offer us is an understanding of a country’s level of dependency on an industry in the context of ECI. The shocking is done in small percentage increments in order to smooth out the resulting curve. Additionally, a recurring theme one will see is that for most industries, a breaking point occurs where the ECI either jumps upwards or downwards, creating a hockey stick shape rather than a linear trend. While the inflection point may not be accurate in context of real life, comparing the various inflection points across industries can give us valuable insight.

The graphs are formulated as follows: There are four ECI Sensitivity graphs. The first two represent data from 2018. The first chart shows positive shocking in which export numbers are shocked upwards per industry. The X-axis is in terms of percentage shock per current dollar value of export. The Y-axis is the recalculated ECI level post-shocking. The second chart follows the same format except the X-axis represents negative shocking. In other words, exports for each industry are decremented and the ECI is accordingly recomputed. The final two sensitivity graphs show the same results using 2013 data. Below is an example of an ECI sensitivity graph.

Example 2018 (Incremental ECI Sensitivity)

SDV sensitivity

Secondly, we analyze the sensitivity of the SDV to changes in export levels. The goal is to understand how export level changes for a particular industry can affect the marginal opportunity gain for other industries. We will be using specifically High Complexity Products and Food and Preparations as our base industries. We will be increasing or decreasing the absolute export level in both of these industries and observing the effects on the SDV.

When the opportunity gain of an industry is negative, the SDV sensitivity approximates how an over-development of the industry jeopardizes the economic structure of a country. When the opportunity gain of the industry is zero, the SDV sensitivity determines whether the further development of the industry shapes the country with a better economic structure and predicts how the SDV would change accordingly.  Specifically, as we reduce the export of such an industry to 25%-50% of its original value, a few other industries originally with negative opportunity gain could likely become profitable.

Similar to the ECI sensitivity graphs above, we will be shocking export of High Complexity Products and Food and Preparations in small percentage increments. A new SDV, represented by a new column in the charts, is recorded only when a certain level of shock changes the structure of the SDV. In effect we are incrementing or decrementing export levels of two industries until the marginal opportunity gain of any industry changes in category (positive, negative, or neutral).  Below is an example of a SDV Sensitivity chart with Positive Shocking. Industries with positive marginal opportunity gain are colored blue, neutral is colored white and negative is colored red.

Example High-complexity Products 2018 (Incremental SDV Sensitivity)

Contingency Plan

The Contingency Plan aims to present a set of solutions with respect to upheavals in different industries. Instead of compensating for the declining production directly, the best strategy is to develop those incipiently profitable industries. In this manner, we can derive the contingency strategy for countries to deal with possible abrupt declines of crucial industries.  In some cases, the SDV remains unchanged even when a zero-opportunity-gain industry declines to its 20% in terms of export. We can then conclude the industry is not indispensable to the country. As a clarification, the three consecutive N/As means that the country doesn’t even need to respond to a collapse in the industry. Countries tend to have distinct solutions to the up and down of the same industry.  To create the contingency strategy table we decrease  the export level for each industry in the country’s current production space by 60% respectively. The three highest ranking industries in the new SDV are then returned.

Example Contingency Strategy 2018

4.3 Sensitivity Analysis Results and Interpretation

Below is the United Kingdom’s 2018 ECI Sensitivity Charts. Firstly in the positive chart, we notice immediately that an increase in export in the majority of industries actually causes decreases in ECI. Only Transportation seems to give an immediate increase in ECI level. A large increase in High Complexity Products would also lead to an increase in the ECI level.

Next we consider the United Kingdom’s 2018 Negative Shock chart. We see that for the UK decreasing the export of Food and Preparation could drastically increase the overall ECI for the country. Similarly large decreases in Precious Stones could also increase ECI level. The Uk is most sensitive to decreases in export of High Complexity Products and Machinery and Construction.

United Kingdom 2018 (Incremental ECI Sensitivity)

United Kingdom 2018 (Decremental  ECI Sensitivity)

Next we consider the 2013 ECI Sensitivity graphs. We see that in the positive shocking case, even a small increase in High Complexity Products could drastically improve the ECI index. Similarly to 2018, an increase in Transportation would also increase ECI level. Increases in export of most other industries lead to decreasing ECI scores.

In the 2013 negative shocking case, we see that again the UK could benefit from a decrease in Transportation and Precious Stones. In addition, large decreases in Energy, Drilling, and Mining could increase the ECI score. In 2013, the UK was incredibly sensitive to reductions in Machinery and Construction.

United Kingdom 2013 (Incremental ECI Sensitivity)

United Kingdom 2013 (Decremental  ECI Sensitivity)

Below we see the SDV sensitivity charts for High Complexity Products and Food and Preparations in 2018. The UK’s SDV was shown to be quite sensitive to decrements to export level in High Complexity Products in 2018. This helps explain the decrease in the UK’s ECI over the course of the pandemic, as demand for High Complexity Products decreased globally, thus decreasing the UK’s export of these. In 2018, Vegetables, Fruits, and Plants seems to be the leading industry if a drawdown in High Complexity Products is experienced. In fact it becomes the only positive opportunity gain industry after major drawdowns in High Complexity products. Again, this helps explain why the UK’s GDP grew despite a decrease in ECI: it focused on Vegetables, Fruits, and Plants as major exports given the drawdown in High Complexity Products, despite its low contribution to ECI.

The UK’s SDV is fairly insensitive to changes in health of the Food and Preparations industry in 2018, since this is not a major industry for the UK. We need to see very large increases in export to cause any change in the SDV. On the decremental side, we see that the SDV again is fairly stable with respect to decreases in export. Vegetables, Fruits, and Plants again seem to be the highest opportunity gain industries.

United Kingdom High-complexity Products 2018 (Incremental SDV Sensitivity)

United Kingdom High-complexity Products 2018 (Decremental SDV Sensitivity)

United Kingdom Food & Preparations 2018 (Incremental SDV Sensitivity)

United Kingdom Food & Preparations 2018 (Decremental SDV Sensitivity)

4.4 Contingency Strategy

Decreasing export of each industry in UK’s 2018 production space by 60% respectively, we derive the contingency strategy shown below.

United Kingdom Contingency Strategy 2018

Based on the UK’s RID for 2021, we note that the contingency strategy recommended by our algorithm in 2018 is mirrored by the UK’s development strategy over the course of the pandemic. As such, it supports the reasoning behind the UK’s increase in GDP between 2019 and 2021.

5. Macro-level Predictions

5.1 Structural Optimality Index

Indeed, such choice of prioritization has proven to be a significant factor in deciding the economic outcomes of countries. In order to quantitatively evaluate how effective our development strategies are and how deviations from the suggested developmental path will lead to suboptimal growth results, we define the measure – Structural Optimality Index (SOI) – on a country level as the Adjusted R-Square obtained from regressing the country’s realized industry development over the suggested development strategy. Both strategies are quantified in nature, with the realized development represented by export increase in every major industry group and the suggested development strategy represented by the opportunity gains of developing the corresponding industry groups as calculated in previous sections. The adjusted R-square from the regression thus provides us with a quantified measure of how the development path adopted by the country has fitted with/differed from calculations on a complexity level.

After obtaining this measure for all countries in our database, we further regress countries’ five-year economic growth, which is defined as the percent increase in GDP (USD), over their SOI. Figure 6 illustrates the regression output, which shows a strong positive correlation between countries’ SOI and their five-year GDP growth, significant at the 1% level and achieving an adjusted R2 of 4.5%. In other words, the more a country develops as suggested by calculations on a complexity level, the better economic outcomes it achieves.

Figure 2: Regression of Five-year GDP Growth over SOI

5.2 SOI of United Kingdom and Its Implications

The United Kingdom, for instance, has a low level of structural optimality as compared with its developed peers. As the regression in Figure 7 suggests (the orange curve represents export increase and the blue curve stands for opportunity gain of the corresponding industry), UK demonstrates a low level of correlation with the suggested developmental path, having an adjusted R-square of around 1.84% in 2018 and 5.07% in 2021. The U.K. ranks in the 4th quartile among all countries in terms of SOI and makes an average rate of economic progress lower than its  developed peers from 2013 to 2018 with an average 5-year GDP growth rate of 3.03%, which is consistent with the regression result in Figure 6. This is in direct contrast to emerging economies such as Turkey, where there is high SOI of around 21.8% and a corresponding GDP growth of 36.7% from 2013 to 2018, making it one of the fastest developing economies during the period. In sum, the U.K.’s slow economic progress from 2013 to 2018 can be at least partially explained by a development strategy that demonstrates a low level of similarity with our suggested developmental path. In specific, the U.K. invested heavily in the Chemicals and Machinery industry, while it should have focused more on industry groups such as Energy & Drilling, and Precious Stones.

Figure 7: SOI of UK (2013-2018)

In 2021, the UK ranks in the second quartile among all countries in terms of SOI and obtains an average 3-year GDP growth rate of 3.79% between 2019 and 2021. Progress is slow on a global scale during this period, but the UK demonstrates a greater ability to adjust to negative economic shocks by improving SOI and increasing GDP growth.

Figure 8: SOI of UK (2019-2021)

6. Concluding Remarks

In conclusion, the UK demonstrated a low level of economic growth in terms of annual GDP increase during the period from 2013 to 2018, concurrent with an increase in economic complexity as compared with other major developed economies. In 2021, the economic effects of the COVID-19 pandemic can be seen in the UK’s regression in terms of economic complexity despite a considerable increase in GDP.

The mixed progress during the period between 2013 and 2018, we believe, can be partially explained through analysis of the economic and product complexity structure of the UK on the industry group level. The product classification system we adopt allows us to measure the realized industry development for various industry groups and to observe that the UK consistently relied on developing the Chemicals, Machinery and Construction, and Daily Instruments industries during this period, while some of its developed counterparts and emerging economies around the globe adopted much more complex and progressive paths. In 2021, the mixed progress is a result of global demand for basic, low-complexity products, which the UK positions itself to meet. As such, its ECI decreases, but its GDP increases at a faster rate, in average, than its developed counterparts.

Based on our analysis of the opportunity gain and a sensitivity analysis of major industry groups, the UK could further its gains by prioritizing High-Complexity Products and Transportation prior to the pandemic. Given the economic effects of COVID-19, the UK’s regression in terms of complexity leads us to suggest the UK further its gains by focusing on Energy, Drilling, and Mining; Precious Stones; and Vegetables, Fruits, and Plants. We further note that the UK had a heavily mismatched development strategy in 2013-2018 that indicated a low level of structural optimality (compared to other developed countries) on the complexity level, having an adjusted R-square of around 1.84%. In 2021, adjusted R-square is 5.07% and ranks higher in terms of structural optimality amongst other countries. Since a significant positive correlation exists between five-year GDP growth and the structural optimality index of an economy as we define and calculate, the UK indeed has a suboptimal growth experience as compared with fast-growing economies both on a regional scale and on a global scale, and has the potential to further its economic gains through industrial structure optimization as suggested in the paper.

References

Hausmann, R., Hidalgo, C., Bustos, S., Coscia, M., Chung, S., Jimenez, J., Simoes, A. and Yıldırım, M. (2007). The Atlas of Economic Complexity. [online] Atlas.cid.harvard.edu. Available at: http://atlas.cid.harvard.edu/.

Balassa, B., “The Purchasing Power Parity Doctrine - A Reapprais- al,” Journal of Political Economy 72, 584-596 (1964).

Feenstra, R.; Lipsey, R.; Deng, H.; Ma, A. & Mo, H. “World Trade Flows: 1962-2000” NBER working paper 11040. National Bureau of Economic Research, Cambridge MA (2005).

United Nations Commodity Trade Statistics Database (http://comtrade.un.org/db/), accessed in August 2019.

The World Economic Forum, “The global competitiveness report,” (various years).

Barro, R. & Lee, J-W. “A New Data Set of Educational Attainment in the World, 1950-2010,” NBER Working Paper No. 1590 (2010).

Kaufmann, D. & Kraay, A. “Governance Indicators: Where Are We, Where Should We Be Going?” Policy Research Working Paper 4370. Washington, DC: World Bank (2008).

Hanushek, E.A. & Woessmann, L. “The Role of Cognitive Skills in Economic Development,” Journal of Economic Literature 46(3), 607- 668 (2008).

**Table 1**

| Category | Description |
|---|---|
| Animals and By-products | All kinds of meat, livestock and related by-products |
| Vegetables, Fruits and Plants | All kinds of plants, edible vegetables and fruits |
| Food and Preparations | Edible preparations, raw cooking materials and appliances |
| Clothing and Accessories | All kinds of fabrics, filament, clothing and accessories |
| Textiles | All kinds of textile articles and related products |
| Wood Products | Book, paper and other elementary products related to wood |
| Metals | Mining of all sorts of raw Metals |
| Refined and Processed Stones | Refined or processed stone products such as pearl and ceramics |
| Energy Drilling and Mining | Mining industry for energy, minerals, stone materials, etc. |
| Daily Instruments | Basic daily instruments such as sport requisites, timing and measuring tools |
| Raw Manufacturing | Basic products made from plastic, rubber, leather, etc. |
| Chemical Manufacturing | Advanced chemical products and pharmaceutical products |
| Chemicals | Raw chemical materials and by-products |
| Machinery and Construction | Machinery and mechanical appliances, including electrical equipment |
| Transportation | Vehicles and locomotives including aircraft, ship, railway, etc. |
| Weapons | Explosives, arms and ammunition |
| Services and Utilities | Financial, business, legal, communication, travel Services and Utilities, etc. |
| High-complexity Products | Agglomeration of advanced products with highest PCIs |

**Table 2**

|  | High-complexity Products | Food and Preparations | Animals and By-products |
|---|---|---|---|
| Adj.R-squared | 0.075 | 0.006 | 0.002 |
| F-statistic | 9.556 | 1.638 | 1.175 |
| No. Observations | 107 | 107 | 107 |

**Table 3**

|  | High-complexity Products | Food and Preparations | Animals and By-products |
|---|---|---|---|
| Adj.R-squared | 0.149 | 0.003 | -0.012 |
| F-statistic | 4.510 | 1.059 | 0.7542 |
| No. Observations | 21 | 21 | 21 |

**Table 4**

| Ranking | France | the UK | Germany |
|---|---|---|---|
| 1 | High-complexity Products | Services and Utilities | High-complexity Products |
| 2 | Chemical Manufacturing | Weapons | Transportation |
| 3 | Daily Instruments | Raw Manufacturing | Wood Products |
| 4 | Animals and By-products | Precious Stones | Metals |
| 5 | Food and Preparations | Animals and By-products | Food and Preparations |

**Table 5**

| Ranking | France | the UK | Germany |
|---|---|---|---|
| 1 | Services and Utilities | Precious Stones | Daily Instruments |
| 2 | Precious Stones | High-complexity Products | Transportation |
| 3 | High-complexity Products | Services and Utilities | Chemicals |
| 4 | Energy Drilling and Mining | Energy Drilling and Mining | Chemical Manufacturing |
| 5 | Machinery and Construction | Wood Products | Clothing and Accessories |

**Table 6**

| Ranking | China | South Korea | Singapore |
|---|---|---|---|
| 1 | High-complexity Products | Transportation | Transportation |
| 2 | Transportation | Textile | High-complexity Products |
| 3 | Machinery and Construction | High-complexity Products | Precious Stones |
| 4 | Energy Drilling and Mining | Chemical Manufacturing | Daily Instruments |
| 5 | Daily Instruments | Machinery and Construction | Services and Utilities |

**Table 7**

| Ranking | China | South Korea | Singapore |
|---|---|---|---|
| 1 | Chemicals | Chemicals | Weapons |
| 2 | Daily Instruments | Daily Instruments | Energy Drilling and Mining |
| 3 | Transportation | Transportation | Transportation |
| 4 | Raw Manufacturing | Textile | Machinery and Construction |
| 5 | Weapons | Raw Manufacturing | High-complexity Products |

**Table 8**

| Label | Product Names |
|---|---|
| 1 | Animal and By-products |
| 2 | Vegetables, Fruits and Plants |
| 3 | Food and Preparations |
| 4 | Energy Drilling and Mining |
| 5 | Chemicals |
| 6 | Chemical Manufacturing |
| 7 | Raw Manufacturing |
| 8 | Wood Products |
| 9 | Clothing and Accessories |
| 10 | Textile |
| 11 | Metals |
| 12 | Machinery and Construction |
| 13 | Transportation |
| 14 | Weapons |
| 15 | Daily Instruments |
| 16 | Precious Stones |
| 17 | High-complexity Products |
| 18 | Services and Utilities |

**Table 9**

| Table 18: OLS Regression Results | Table 18: OLS Regression Results |
|---|---|
| Dep. Variable: GDP | F-Statistic: 5.963 |
| R2: 0.054 | Prob (F-Stat): 0.0163 |
| Adj R2: 0.045 | No. Observations: 106 |
