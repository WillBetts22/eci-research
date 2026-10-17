<!-- text mirror of admin/todos/archive/2020_2021 Possible Proposals.docx — edit the .docx, not this file -->

Shomik

Here are some possible tasks/projects I thought I could work on over the next few months. I’m sure I’ll come up with more ideas, especially as I continue to get more familiar with the research.

Shifting the matrix of comparative advantage from a binary measure to a scale (i.e. rather than just assigning 1 if a country has a RCA for the product, assign it a number along a scale that reflects exactly how much of a RCA it has)

Trying to reconcile the contradictions in the model for countries such as Brazil, which have a high SOI and a low rate of GDP growth

Anything else that needs to be worked on-I’m open to doing anything the group needs, and don’t have a strong preference on what aspect of the research I’m working on

Ajit

Similarly, please find below some potential areas I think I would want to work on/look into over the next few months

In the Sequential Development Strategy, we could try changing the metric to RCA, and apply this across the top 3 categories, as they are likely to be closely related. This could then be iterated upon using the same greedy algorithm, but is likely more reflective of how a country would prioritize economic development

To account for the aspect of time-value, is there a way to introduce a discount rate to the marginal opportunity gain as we look at the sequential development strategy across iterations. Can we assign a variable of time to each iteration

Explore ways of modeling economic growth within representative samples of countries, i.e. take a country with high, medium, and low ECI and model their investment decisions in conjunction with one another

I also think maybe trying to do my own analysis of a new country could help with deeper understanding all of the material; additionally open to other projects that the team thinks would be best to look into

Haoxian

A few suggestions to improve current greedy algorithm:

Overcome the sparsity. Since the original greedy algorithm will sometimes output some sparse solution. In other words, the solution suggests that the country should allocate its budget to just a few industries, in order to improve the ECI value. So, this might not make so much sense in reality. The reason why this happened might be the hard threshold of the ECI calculation. A similar metric is ECI+, which does not calculate the comparative advantages. Therefore, instead of optimizing ECI, we can try to optimize ECI+.

ECI + Reference: https://arxiv.org/abs/1707.05826

Contravention to the suggested development vector. Another issue that I observed from our previous results is that sometimes the solution is a bit different from the suggested development vector. For example, sometimes it tends to put a great budget on the industry with lower priority in the suggested development vector. One way to solve it is to add a penalty term to the objective so that the solution that we obtain will not be too different from the suggested development vector.
