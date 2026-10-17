export const meta = {
  name: 'lit-review',
  description: 'Literature review in the ECI Lab format: find candidate papers, summarize each in parallel, cross-check claims against the source, and synthesize implications for country reports',
  phases: ['Search', 'Summarize', 'Verify', 'Synthesize'],
}

// args: "economic complexity and inequality"  or  { topic: "...", papers: ["arXiv:2506.18829", "https://..."], max: 6 }
const input = typeof args === 'string' ? { topic: args } : (args || {})
const topic = input.topic || 'recent advances in economic complexity relevant to country reports'
const max = input.max || 6
const role = 'You are acting as the "lit-scout" agent of the ECI Lab. Read .claude/agents/lit-scout.md first and follow its format and rules.'

phase('Search')
let papers = input.papers
if (!papers || papers.length === 0) {
  const found = await agent(`${role}
Find the ${max} most relevant, credible papers on: "${topic}".
First check literature/ and catalog/text/literature/ so you skip papers the lab already reviewed.
Prefer peer-reviewed or well-cited arXiv/NBER papers from the last 10 years, plus foundational ones if missing.`, {
    label: 'search',
    schema: {
      type: 'object',
      required: ['papers'],
      properties: { papers: { type: 'array', items: { type: 'string', description: 'title + URL/DOI' } } },
    },
  })
  papers = found.papers.slice(0, max)
}

phase('Summarize')
const entries = await pipeline(papers, p =>
  agent(`${role}
Open this paper and write ONE entry in the lab's 3-question format: ${p}
Return the Markdown entry only. State "abstract only" if you could not access the full text.`, { label: `summarize: ${String(p).slice(0, 40)}` }),
)

phase('Verify')
const checked = await pipeline(entries.filter(Boolean), e =>
  agent(`You are a skeptical fact-checker. Re-open the source cited in this literature-review entry and check every finding and number against it.
Return the corrected entry (same format). Remove any claim you cannot find in the source, and add "[verified]" after the title if everything checks out.

${e}`, { label: 'verify' }),
)

phase('Synthesize')
return await agent(`${role}
Write literature/reviews/${topic.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60)}.md containing:
1. a 1-paragraph overview of "${topic}"
2. all of the entries below
3. "Implications for our reports": 3-5 bullets the report-writer can use
Return the file path and the implications bullets.

${checked.filter(Boolean).join('\n\n---\n\n')}`, { label: 'synthesize' })
