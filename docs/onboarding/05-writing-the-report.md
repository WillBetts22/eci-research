# 05 · Writing the Report

Template: [`templates/Auto Report Template.docx`](../../templates/) (text copy: `catalog/text/templates/Auto Report Template.md`).

## How the template works
- `[Square brackets]` are **values**. They're filled automatically from the JSON, or by you from notebook output. Never type a number that didn't come from the notebook.
- `{Curly braces}` are **instructions** for 1–2 sentences of country-specific context. Replace the whole `{...}` with your prose.
- `[increased/decreased]`-style placeholders: pick one.
- Boilerplate methodology paragraphs stay as-is. They're the same in every report.

## Section → source map
| Report section | Values come from | You write |
|---|---|---|
| Title page / author list | Current semester's member list | — |
| **0. Executive Summary** | GDP growth, ECI change, RID counts, SOI quartile, R² adj | Key export sectors / shocks that drove the period |
| **1. Report Overview** | Years | Why this period mattered for the country |
| **2.1 GDP** (Figure 1) | `[GDP growth rate]`, `[Relative GDP growth quality]`, peers | Notable divergence/crossovers in the GDP lines |
| **2.2 ECI** (Figures 2–3) | ECI start/end/change, peer standing | What drove the ECI movement, plus any external shock (optional paragraph) |
| **3.1 Product categorization** (Tables 1–2) | Boilerplate + OLS table | — |
| **3.2 RID** (Table 3) | # of positive/negative RID groups | Which industries moved, and whether that matches the country's known strategy |
| **3.3 Regional comparison** (Tables 4a/4b) | Leading/emerging peers | Brief comparison |
| **4.1 SDV** (Tables 5–6) | Opportunity-gain ranking | — |
| **4.2–4.5 Greedy** (Figure 4, Tables 7–8) | Top industry at 5/10/15/20% | ECI increment pattern across budgets |
| **4.6–4.8 Sensitivity** (Figures 5–6) | `[Industry 4–6]`, `[Pos Trend]`, `[Neg Trend]` | — |
| **5. SOI** (Figures 9–10) | `[SOI quartile]`, `[R^2 adj]`, contrast country | 1–2 sentences on the contrast economy |
| **6. Concluding remarks** | `[Industry 1–3]` (top SDV), `[Industry 4]` (most sensitive) | Policy-relevant summary |

## Style rules (from past reviews)
- Compare with **the country's previous report**: say what changed and why.
- Compare with the **3 peers** throughout. Use the same peers as last time.
- Check **figure and table numbering**: it must be consecutive and match the in-text references.
- Format all tables in the **same style** as the template.
- Use **past tense** for the analysis period and **present tense** for recommendations.
- Don't over-claim causality. ECI is associated with growth, and the [literature review](../../literature/) explains what is and isn't safe to claim.
- File names: `<Country>_<end year>.docx` / `.pdf`.

## QA checklist
Paste this into your PR. The `qa-reviewer` agent checks the same list.
- [ ] Every `[placeholder]` and `{instruction}` is gone (search for `[` and `{`)
- [ ] GDP growth, ECI values, R², SOI, and the allocation percentages match the JSON and notebook output exactly
- [ ] Country names in captions and text are correct everywhere. (Copy-paste from another country's report is the #1 error.)
- [ ] Years in captions match `[Start Year]–[End Year]`
- [ ] Figures 1–10 and Tables 1–8 are numbered consecutively and referenced correctly
- [ ] Peers match the previous report (or the change is explained)
- [ ] Executive summary and conclusion agree with the body
- [ ] Prose that is country-specific is factually accurate (check claims about FDI, policy, and shocks against a source)
- [ ] Both PDF and DOCX are committed
