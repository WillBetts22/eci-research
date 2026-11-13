# Does economic complexity predict growth? Plain-English summary

Maitree Mody, November 2026. This covers Projects 1 and 2 from Will's plan (`willbetts/ECI_growth_prediction.md`).
Full details, code and every number are in `eci_growth_projects_1_2.ipynb`.

## The question
Our lab's country reports tell countries to raise their **Economic Complexity Index (ECI)**, a score for how many
sophisticated products a country exports. That advice only makes sense if a higher ECI actually leads to faster growth.
I tested that in two ways:
1. **Looking back (Project 1):** did countries with higher ECI grow faster over the next 10 years?
2. **Looking forward (Project 2):** when Harvard (and our own model) used ECI to *forecast* growth, did the forecasts
   come true?

## What data I used
- Harvard Growth Lab's official ECI scores, going back to 1962 (not our lab's own ECI, so we test the idea, not our code).
- World Bank GDP, population and natural-resource income, back to 1960.
- Every version of Harvard's published growth forecasts (13 releases, 2019 to 2026).

Everything was downloaded fresh and the code was written separately from Will's nightly runs, so the two can check
each other. Three independent review passes went through the work; every number in the notebook was reproduced from
scratch.

## Project 1: Did high-ECI countries grow faster?
**Yes, quite consistently.**
- Comparing countries at the same income level, a country with a clearly higher ECI (one standard deviation) grew about
  **1.25 percentage points faster per year** over the following decade. Over ten years that adds up to a lot.
- This matches Harvard's famous 2013 result reasonably well: on the same decades they used, I get 1.65 points per
  year, versus their 1.9.
- It holds in **almost every decade since 1974**. The one weak decade is 2004 to 2014, when oil and mineral exporters
  boomed because of high commodity prices, regardless of their ECI.
- It holds in every region, and it is not driven by East Asia.
- It works about **equally for rich and poor countries**. Harvard says it matters more for poor countries; I did not
  find that.
- Countries that were **more complex than their income suggested** grew much faster: the top fifth grew 2.7% a year,
  the bottom fifth 0.1%.

**The catch: this does not prove that raising ECI *causes* growth.** When I compare each country only with itself over
time ("did Brazil grow faster in the decades after *its* ECI rose?"), the effect halves and is no longer clearly
significant. So ECI is a good *sign* of countries that will grow, but the evidence that *pushing up* your ECI makes
you grow is weak. That matters for the lab's "maximize ECI" advice, and it is what Project 4 should dig into.

## Project 2: Did ECI-based forecasts come true?
### Test 1: Harvard's real forecasts
In June 2019 Harvard published growth forecasts for 2017 to 2027. Seven of those ten years have now happened, so I
compared the forecasts with reality for 132 countries, and against simple rules of thumb anyone could use:
"every country grows at the average rate", or "every country repeats its last decade".

- Harvard's forecasts were **somewhat right**: they lined up moderately with what happened (correlation 0.49).
- They had the smallest average error, but **the edge over the simple rules was small and mostly not statistically
  meaningful**. "Repeat last decade's growth" ranked countries just as well.
- Their edge was bigger over 2017 to 2019 and shrank over 2020 to 2024 (Covid years), though big non-Covid crises
  explain the largest misses.
- The **biggest misses** were crises no trade-based model can see coming: Venezuela's economic collapse, Lebanon's
  banking crash, Myanmar's 2021 coup, Sri Lanka's debt default and the war in Ukraine. Tourism economies hit by Covid
  (Tunisia, Thailand) and commodity swings (Oman's oil cuts, DR Congo's mining boom) explain most of the rest of the top 10.
- **An open puzzle:** Harvard never says whether its forecast is for total GDP or GDP per person. The numbers look like
  total GDP, but not conclusively. If it is per person, the forecasts were the least accurate of everything tested.
- Harvard's forecasts are mostly fixed once published, but three years' forecasts were quietly revised later.

### Test 2: Our own "time machine" test (rolling-origin)
I pretended to stand in 1984, 1994, 2004 and 2014. Each time I built the growth model using **only data available at
that moment**, forecast the next decade, and checked the forecast against what happened (511 forecasts in total).

- Adding ECI made the forecasts **a little better in 3 of the 4 decades** (again not in the 2004 commodity boom).
- But the improvement is **small and fragile**: it is mostly not statistically significant, and about 90% of it comes
  from just 8 dramatic cases (for example Iraq after 1994, and Venezuela and Sudan after 2014). Remove the 10 most
  extreme cases and the gain shrinks to about a third.
- ECI did **no better than simply counting how many products a country exports well**. That is a key question for
  Project 3.
- Will's nightly run found ECI made forecasts *worse*. That is because it only looked at 2005 to 2014. When I run my data
  over that same period, I get the same answer. The older decades are where ECI helps.

## The big picture
- **ECI is a real signal:** across 50 years, more complex economies have tended to grow faster than their income level
  would predict.
- **As a forecasting tool it adds only a little:** small gains, driven by a few extreme cases, and not clearly better
  than simple alternatives.
- **There is little evidence that raising ECI causes growth.** The lab should be careful about telling countries to
  "maximize ECI".

## What is left to do
- Optional extra: test whether misses are bigger for oil exporters or countries hit hardest by Covid.
- Re-score Harvard's 2019 forecasts once 2025 to 2027 data come out.
- Hand off to Project 3 (is ECI better than simpler measures?) and Project 4 (does raising ECI cause growth?).
