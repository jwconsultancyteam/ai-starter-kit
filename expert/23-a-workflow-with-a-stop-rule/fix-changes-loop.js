export const meta = {
  name: 'fix-changes-loop',
  description: 'Run test_changes.py, fix changes.py, repeat until pass or 2 rounds without progress',
  phases: [{ title: 'Fix loop', detail: 'test → fix → retest' }],
}
const SCHEMA = {
  type: 'object',
  properties: {
    passed: { type: 'boolean' },
    failing_count: { type: 'integer', description: 'number of failing tests/assertions after your fix (0 if passed)' },
    summary: { type: 'string', description: 'what failed before, what you changed in changes.py, and final test output summary' },
  },
  required: ['passed', 'failing_count', 'summary'],
}
phase('Fix loop')
let best = Infinity, noProgress = 0, round = 0
const history = []
while (true) {
  round++
  const r = await agent(
`Round ${round}. In the current directory: run \`python3 test_changes.py\`. If it passes, report passed=true and change nothing.
Otherwise read the failure, read changes.py and test_changes.py, and fix changes.py ONLY so the test passes for real (no special-casing the test, no hardcoding expected outputs). Do NOT modify test_changes.py or shipments-export-sample.csv. Do not commit.
Then run \`python3 test_changes.py\` again and report the result.
Previous rounds:\n${history.join('\n') || '(none)'}`,
    { label: `round ${round}`, schema: SCHEMA })
  if (!r) { log(`round ${round}: agent returned nothing`); noProgress++ }
  else {
    history.push(`Round ${round}: passed=${r.passed}, failing=${r.failing_count}. ${r.summary}`)
    log(`round ${round}: passed=${r.passed}, failing=${r.failing_count}`)
    if (r.passed) return { status: 'passed', rounds: round, history }
    if (r.failing_count < best) { best = r.failing_count; noProgress = 0 } else noProgress++
  }
  if (noProgress >= 2) return { status: 'stalled', rounds: round, history }
}