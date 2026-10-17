export const meta = {
  name: 'semester-reports',
  description: 'Produce ECI country reports for many countries in parallel: brief -> analysis -> draft -> double-blind QA -> one revision round -> filing',
  phases: ['Brief', 'Analyze', 'Draft', 'QA', 'Revise', 'File'],
}

// args: ["Poland", "Kenya"]  or  { countries: [...], semester: "2026-fall", sections: "comprehensive" }
const input = Array.isArray(args) ? { countries: args } : (args || {})
const countries = input.countries || []
if (countries.length === 0) {
  return 'No countries given. Example args: {"countries": ["Poland", "Kenya"], "semester": "2026-fall"}'
}
const sections = input.sections || 'comprehensive'
const semesterHint = input.semester
  ? `The semester is ${input.semester}.`
  : 'Take the semester from the "Current semester context" section of CLAUDE.md (format YYYY-spring or YYYY-fall).'

const role = name => `You are acting as the "${name}" agent of the ECI Lab. First read .claude/agents/${name}.md and CLAUDE.md, then follow them exactly.`

phase('Brief')
const briefs = await pipeline(countries, country =>
  agent(`${role('analyst')}
Prepare a run brief for ${country}. ${semesterHint}
- Find its previous report via catalog/COUNTRIES.md and read the text mirror under catalog/text/.
- Extract the 3 comparable (peer) countries, the category (developed/emerging), and the leading/emerging comparison economies, if listed.
- Determine the exact country names as the notebook uses them (see the rename cell in code/current/Spring2026.ipynb, e.g. "Vietnam", "USA").
If there is no previous report, propose 3 sensible peers and set needsConfirmation=true.
Do not run the notebook yet.`, {
    label: `brief: ${country}`,
    schema: {
      type: 'object',
      required: ['country', 'semester', 'peers', 'category', 'needsConfirmation'],
      properties: {
        country: { type: 'string' },
        semester: { type: 'string' },
        peers: { type: 'array', items: { type: 'string' } },
        category: { type: 'string', enum: ['developed', 'emerging'] },
        leading: { type: 'array', items: { type: 'string' } },
        emerging: { type: 'array', items: { type: 'string' } },
        previousReport: { type: 'string' },
        needsConfirmation: { type: 'boolean' },
      },
    },
  }),
)
const ready = briefs.filter(b => b && !b.needsConfirmation)
const toConfirm = briefs.filter(b => b && b.needsConfirmation)
if (toConfirm.length) log(`Needs peer confirmation, skipped: ${toConfirm.map(b => b.country).join(', ')}`)

phase('Analyze')
const analyses = await pipeline(ready, b =>
  agent(`${role('analyst')}
Run the analysis for ${b.country} (semester ${b.semester}).
Command: python3 scripts/run_notebook.py --country "${b.country}" --peers "${b.peers.join(',')}" --category ${b.category} --semester ${b.semester} --sections ${sections}${b.leading && b.leading.length ? ` --leading "${b.leading.join(',')}"` : ''}${b.emerging && b.emerging.length ? ` --emerging "${b.emerging.join(',')}"` : ''}
Then write reports/${b.semester}/${b.country}/analysis-notes.md as your instructions describe. Previous report: ${b.previousReport || 'none'}.`, {
    label: `analyze: ${b.country}`,
    stallMs: 3 * 60 * 60 * 1000,
    schema: {
      type: 'object',
      required: ['country', 'ok', 'folder', 'headline', 'errors'],
      properties: {
        country: { type: 'string' },
        ok: { type: 'boolean' },
        folder: { type: 'string' },
        headline: { type: 'string' },
        errors: { type: 'array', items: { type: 'string' } },
      },
    },
  }),
)
const analyzed = analyses.filter(a => a && a.ok)

phase('Draft')
await pipeline(analyzed, a =>
  agent(`${role('report-writer')}
Draft the country report for ${a.country} from ${a.folder}/analysis-notes.md. Produce the _draft.md, the .docx, and slides.md as your instructions describe.`, { label: `draft: ${a.country}` }),
)

const qaSchema = {
  type: 'object',
  required: ['verdict', 'failures'],
  properties: {
    verdict: { type: 'string', enum: ['PASS', 'FAIL'] },
    failures: { type: 'array', items: { type: 'string' } },
  },
}
const review = (a, tag) =>
  agent(`${role('qa-reviewer')}
Independently review ${a.folder}. You did not write it. Re-verify the numbers against the executed notebook yourself. Write ${a.folder}/qa-report${tag}.md.`, { label: `qa${tag}: ${a.country}`, schema: qaSchema })

phase('QA')
const qa = await pipeline(analyzed, async a => {
  const [r1, r2] = await parallel([review(a, '-A'), review(a, '-B')])
  const failures = [...((r1 && r1.failures) || []), ...((r2 && r2.failures) || [])]
  const pass = r1 && r2 && r1.verdict === 'PASS' && r2.verdict === 'PASS'
  return { a, pass, failures }
})

phase('Revise')
const final = await pipeline(qa.filter(Boolean), async q => {
  if (q.pass) return { country: q.a.country, verdict: 'PASS', open: [] }
  await agent(`${role('report-writer')}
Revise the ${q.a.country} report in ${q.a.folder}. Address every QA item below and reply with item -> change.
${q.failures.map((f, i) => `${i + 1}. ${f}`).join('\n')}`, { label: `revise: ${q.a.country}` })
  const r = await review(q.a, '-final')
  return { country: q.a.country, verdict: r ? r.verdict : 'UNKNOWN', open: r ? r.failures : ['QA did not complete'] }
})

phase('File')
await agent(`${role('archivist')}
File the new outputs under reports/ for: ${analyzed.map(a => a.country).join(', ')}. Regenerate the catalog, remove _work folders, run the safety scan, and propose (do not run) a commit.`, { label: 'file' })

return {
  results: final.filter(Boolean),
  failedAnalysis: analyses.filter(a => a && !a.ok).map(a => ({ country: a.country, errors: a.errors })),
  needsPeerConfirmation: toConfirm.map(b => ({ country: b.country, proposedPeers: b.peers })),
  headlines: analyzed.map(a => ({ country: a.country, headline: a.headline })),
}
