export const meta = {
  name: 'qa-sweep',
  description: 'Double-blind QA of every country report in a folder: two independent reviewers per report, then a merged and deduplicated verdict table',
  phases: ['Find', 'Review', 'Merge'],
}

// args: "reports/2026-spring"  (default: the current semester's folder)
const target = typeof args === 'string' && args ? args : null

phase('Find')
const found = await agent(`List the country report folders or files to QA under ${target || 'reports/<current semester from CLAUDE.md>'}.
A target is either a folder reports/<semester>/<Country>/ or a single report file (.docx/.pdf) directly in the semester folder.
Return one entry per country.`, {
  label: 'find reports',
  schema: {
    type: 'object',
    required: ['targets'],
    properties: { targets: { type: 'array', items: { type: 'object', required: ['country', 'path'], properties: { country: { type: 'string' }, path: { type: 'string' } } } } },
  },
})

const schema = {
  type: 'object',
  required: ['verdict', 'findings'],
  properties: {
    verdict: { type: 'string', enum: ['PASS', 'FAIL'] },
    findings: { type: 'array', items: { type: 'object', required: ['check', 'issue', 'fix'], properties: { check: { type: 'string' }, issue: { type: 'string' }, fix: { type: 'string' } } } },
  },
}
const reviewer = (t, lens) => agent(`You are acting as the "qa-reviewer" agent. Read .claude/agents/qa-reviewer.md and CLAUDE.md first.
Review ${t.path} (${t.country}). Focus extra hard on: ${lens}.
If there is no analysis-notes.md or executed notebook (older reports), check internal consistency, country names, years, numbering, and template fidelity, and say that the numbers could not be traced.
Do not write files. Return findings only.`, { label: `${t.country}: ${lens.split(',')[0]}`, schema })

phase('Review')
const reviews = await pipeline(found.targets, async t => {
  const [a, b] = await parallel([
    reviewer(t, 'numbers, traceability to notebook output, years'),
    reviewer(t, 'country-name copy-paste errors, figure/table numbering, claims and consistency'),
  ])
  return { t, a, b }
})

phase('Merge')
return await agent(`Merge these QA results into one Markdown table: Country | Verdict (FAIL if either reviewer failed) | Top issues (deduplicated) | Fix.
Drop findings that only one reviewer raised AND that are vague. Keep anything concrete.
Then list the 3 most common issue types across all reports.

${JSON.stringify(reviews.filter(Boolean).map(r => ({ country: r.t.country, path: r.t.path, A: r.a, B: r.b })), null, 1)}`, { label: 'merge' })
