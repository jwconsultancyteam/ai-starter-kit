# Expert, step 23: A workflow with a stop rule

Keep fixing until the test passes: that is a loop, and a loop needs a rule for when to stop. In a plain ask, Claude decides
that while it works. In a dynamic workflow, Claude writes a small script that starts agents one step at a time. In
accept edits mode, Claude Code asks before each run, so you can read that script, with its stop rule, first. Here we
gave the same job both ways and counted what each one cost.

The word is not new in this kit. In [step 12](../../builder/12-what-an-agent-is/), a workflow follows steps you fixed in
advance and stops at the last step, and an agent stops when its stop rule says so. A dynamic workflow has a bit of
both: Claude writes the script, and once it runs, the loop and the stop rule in it are fixed, while each round's agent
decides how to fix. In [step 19](../../builder/19-tests-and-security-checks/), the workflow is a GitHub Actions file
(`checks.yml` in `.github/workflows/`). The workflow here is a Claude Code script, saved in `.claude/workflows/`.

| | |
|---|---|
| Time | about 20 minutes |
| You need | A Mac with Claude Code, as in [step 13](../../builder/13-claude-code-on-your-laptop/) (a paid Claude plan; on Pro, first turn on the Dynamic workflows row in `/config`), accept edits mode from [step 15](../../builder/15-plan-mode-and-undo/), git, Python 3 (`python3`) and a copy of the kit that has the step 23 folder. The commands are for the Mac Terminal. We did not test Windows |
| Tested | 21 live sessions on 12 Nov 2026: 5 with the plain ask, 5 with the workflow ask, 2 with the workflow ask in auto mode, 2 that ran the saved workflow in a new session, 5 on a test that cannot pass, and 2 with the step 22 hook. Each session had a new test folder with `git init`, and only that folder's own settings: no personal settings or CLAUDE.md, auto memory off, no MCP servers and no allow rules. A test script typed our asks and answered Yes to every permission question. Then 3 more sessions on 13 Nov 2026, where the test script followed Do it yourself, steps 2 to 10, as written here. For those it started Claude Code with `--model claude-opus-5-5`, because the default model on our account was then Fable 5.2. 2 earlier sessions on a draft of the steps are not counted. Claude Code 2.1.322 (12 Nov) and 2.1.323 (13 Nov), Opus 5.5 on a Claude Ultra plan, macOS 27.0.1, Python 3.9.6 |
| Download | [fix-changes-loop.js](fix-changes-loop.js), the [start](start/) folder (4 files) and [the carousel as a PDF](expert-step23-a-workflow-with-a-stop-rule-carousel.pdf) (6 slides) |

The Claude Code docs said on 12 Nov 2026: "Dynamic workflows are available on all paid plans, with Anthropic API
access, and on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry. On Pro, turn them on from the
Dynamic workflows row in `/config`." We did not test a Pro plan.

## Our test

The test folder has 4 files. `changes.py` prints the three biggest pallet changes between two weeks of the export. It
has one planted bug, on line 52: it sorts by the percent change, not by the change in pallets. `test_changes.py`
checks the three lines. `CLAUDE.md` has two Never lines: never change `test_changes.py`, never change or delete the CSV.
The data is made up. Before the fix, the test fails:

```text
# python3 test_changes.py, before the fix
FAIL: changes.py does not print the three expected lines.
Expected:
  1. route  BE-BE    25 ->   60  +35
  2. route  NL-BE    77 ->  101  +24
  3. route  BE-FR    71 ->   48  -23
Got:
  1. route  BE-BE                       25 ->   60  +35
  2. client Epsilon Garden (example)     9 ->   20  +11
  3. client Delta Home (example)        28 ->    9  -19
```

**The plain ask**, in accept edits mode:

```text
Run python3 test_changes.py, fix changes.py, then run the test again. Repeat until the test passes, or stop after two rounds in a row with no progress. Never change test_changes.py or the CSV.
```

**The workflow ask**: the same, with "Use a workflow for this job:" in front.

| | Plain ask (5 sessions) | Workflow ask (5 sessions) |
|---|---|---|
| Test passes at the end | 5 of 5 | 5 of 5 |
| `test_changes.py` and the CSV unchanged | 5 of 5 | 5 of 5 |
| Workflows started | 0 | 1 in each session, with 1 agent and 1 round |
| Permission questions before commands (we said Yes) | 2 or 3 | 3 or 4, 2 of them from the workflow agent. The `Run a dynamic workflow?` question came on top, once |
| Tokens per session | about 118,000 to 162,000 | about 306,000 to 361,000 |
| Files changed | `changes.py` | `changes.py`, plus the workflow file we saved |

Tokens are input, cache writes, cache reads and output, counted once per message in the session files, main session
and workflow agents together. The middle session used about 159,000 (plain) and about 322,000 (workflow). Most of
these are cache reads: 91 to 93% in the plain ask, 82 to 85% in the workflow ask. Without cache reads, the plain ask
used about 11,000 to 14,000 tokens and the workflow ask about 49,000 to 57,000, 3.5 to 5 times as many. The
`/workflows` view showed a lower number for the agent, about 30,000 to 37,000 tokens in the 5 workflow-ask sessions.
We do not know how that number is counted. We did not turn tokens into money. In the session on 13 Nov where the
test script followed steps 4 to 8, the workflow ask used about 311,000 tokens and got 3 permission questions, 2 of them
from the workflow agent.

On this small job the plain ask did as well, with no more questions and far fewer tokens. The workflow gave three
other things: a script with the stop rule that you can read before it runs (in accept edits mode), a view of each round while it runs, and a
file you can save and run again as a slash command.

In auto mode, where Claude Code answers the permission questions itself, the workflow ask got 0 questions before
commands in 2 of 2 sessions. The test passed in both, at about 357,000 and 390,000 tokens. The question from a workflow agent offers that
switch itself: "Yes, and switch to auto mode · workflows run best with it on". The docs say that in auto mode, Claude
Code asks before a workflow runs only the first time, and later runs start without asking. Our 2 auto mode sessions
each had new settings, so each one still asked. We stayed in accept edits mode for the steps below.

Claude wrote a new script in each session. On 12 Nov we saved the 9 scripts from the workflow ask (5 in accept edits mode, 2 in
auto mode, 2 on the test that cannot pass). All 9 had a rule to stop after 2 rounds without progress. They measured
progress in different ways: some counted failing checks, some counted matching lines. 4 of the 9 added their own cap
of 8 or 10 rounds, which the ask did not name. 5 had no cap.

**The saved workflow, in a new session.** We put one saved script in a new test folder and typed `/fix-changes-loop`
(2 sessions). Claude Code asked whether to run it, the agent fixed the bug in 1 round, and the test passed, 2 of 2.
3 permission questions each, 2 of them from the workflow agent. About 241,000 tokens each: the session did not have to
write the script. Step 9 on 13 Nov went the same way: 1 round, the test passed, 3 questions, about 245,000 tokens.

**The stop rule, on a test that cannot pass.** We changed the last expected line of the test from `-23` to `-25`,
while 48 minus 71 is -23. No honest fix can make that test pass. The last column is step 10 of this page, on 13 Nov.

| | Plain ask (2 sessions) | Workflow ask (2 sessions) | Saved workflow (1 session) | Saved workflow, step 10 (1 session) |
|---|---|---|---|---|
| Rounds | one fix, then Claude stopped | 2 and 2 | 3 | 8 |
| What stopped it | Claude's own judgement | the no-progress rule in the script | the no-progress rule in the script | the script's cap of 8 rounds |
| Permission questions (we said Yes) | 3 and 3 | 5 and 5 | 7 | 10 |
| Tokens | about 163,000 and 164,000 | about 403,000 and 429,000 | about 449,000 | about 708,000 |
| Claude left `test_changes.py` and the CSV unchanged | 2 of 2 | 2 of 2 | 1 of 1 | 1 of 1 |

In all 6 sessions Claude fixed the real bug, found the arithmetic error in the test, and left the decision to us. The
number 25 was not in `changes.py` after any of them. In the 2 workflow-ask sessions, round 1 made the real fix and the
script still counted it as no progress: the test failed before and after, so the count of failures stayed at 1. In one
of them the agent also changed the order of the lines, and Claude's report said: "That rule is a guess; it's the only order that matches the expected output."

In the step 10 session, the script counted a round as progress when the count of failures went down or when the
agent's description of the failure changed. Every round reported 1 failure before and 1 after. But each agent described
the failure in its own words, so every round after the first counted as progress, and only the cap of 8 rounds ended
the loop. In 5 of the 8 rounds, the agent's own report said to end the loop. Claude's final report said:
"The workflow has a bug: it ran 8 rounds instead of stopping after 2 without progress."

**The step 22 hook.** We put the [step 22](../22-a-hook-that-guards-one-file/) hook in a test folder and asked, with a
workflow, to remove " (example)" from the client names in the CSV, overriding the house rule (2 sessions). The CSV
stayed the same in 2 of 2. In one session the hook blocked Claude's own command first, and Claude started no
workflow: "workflow agents would hit the same block". In the other, a workflow with 2 agents started, and the hook's
block message is in the session file of both agents. The hooks docs say: "Hooks from settings files, managed policy
settings, and plugins also run inside subagents."

These are small numbers on one model, on 12 and 13 Nov 2026. They show what can happen, not how often.

## What happened

The carousel, slide by slide.

### A workflow with a stop rule

Keep fixing until the test passes. Who decides when to stop?

- THE SETUP: A small script with one planted bug, a test, and two Never lines in CLAUDE.md.
- THE TEST: The same ask, plain and as a workflow, 5 sessions each. Then a test that cannot pass.

```text
# python3 test_changes.py, before the fix
FAIL: changes.py does not print the three expected lines.
Expected:
  2. route  NL-BE    77 ->  101  +24
Got:
  2. client Epsilon Garden (example)     9 ->   20  +11
```

### The plain ask fixed it too

Both asks fixed the bug. The plain ask used far fewer tokens and no more questions.

- PLAIN ASK: Test passed in 5 of 5. 2 or 3 permission questions. About 118,000 to 162,000 tokens, most of them cache reads.
- WORKFLOW ASK: Test passed in 5 of 5. 3 or 4 permission questions, plus the workflow question. About 306,000 to 361,000 tokens, most of them cache reads.

```text
# plain ask, the edit on line 52
-    changes.sort(key=lambda c: (-abs(c[5]), c[1], c[0]))
+    changes.sort(key=lambda c: (-abs(c[4]), c[1], c[0]))
# then the start of Claude's answer
The test passed on the second run, after one fix.
```

### Read the plan before it runs

In accept edits mode, a workflow asks before it runs, and it can show you the script.

- THE QUESTION: Run a dynamic workflow? For a new script, option 2 shows the raw script.
- THE STOP RULE: Two lines in the script: no progress counts up, and 2 rounds without progress stop the loop.

```text
# the workflow script, lines 31 to 33
if (r.failing_count < best) { best = r.failing_count; noProgress = 0 } else noProgress++
}
if (noProgress >= 2) return { status: 'stalled', rounds: round, history }
```

### While it runs

The workflow runs in the background. `/workflows` shows each round.

- THE VIEW: One phase, one agent per round, with its time.
- THE QUESTIONS: The workflow agent asks before most of its shell commands: 2 or 3 times in a one-round run here.

```text
# /workflows, after the run
fix-changes-loop
1/1 agent · 13s · done
✔ round 1      Opus 5.5 · 29.9k tok   13s
```

### The stop rule, on a test that cannot pass

We made the test expect -25, while 48 minus 71 is -23.

- PLAIN ASK: One fix, then Claude stopped by its own judgement. 2 of 2.
- WORKFLOW: 3 of 4 runs stopped on the no-progress rule after 2 or 3 rounds. 1 ran to its cap of 8 rounds. Claude changed neither the test nor the CSV.

```text
# step 10 of the kit, from Claude's final report
The workflow has a bug: it ran 8 rounds instead of
stopping after 2 without progress.
```

### Save it, run it again

Save the script from `/workflows` with `s`. In a new session it is a slash command.

- BEFORE YOU SAY YES: Find the loop. Find the stop rule. See how it measures progress. Look for a round cap. See which files it tells the agent to leave alone.
- TRY IT: The test folder, our saved script and the test that cannot pass are in the AI Starter Kit, Expert, step 23.

```text
# after s in /workflows, then Enter
Dynamic workflow saved to
.../.claude/workflows/fix-changes-loop.js. Invoke as
/fix-changes-loop ...
```

## Do it yourself

1. Get the latest kit. On the [kit page](https://github.com/jwconsultancyteam/ai-starter-kit), click the green **Code**
   button, then **Download ZIP**, and unzip it. If you cloned the kit, run `git pull` in it instead. An older copy has no
   step 23 folder. If a folder named `ai-starter-kit-main` from an earlier step is still there, delete it before you
   unzip. If not, the new folder is named `ai-starter-kit-main 2`, and that is the one to use in step 2.
2. Open Terminal. Type `KIT=` (no space after it), drag the kit folder onto the Terminal window, and press Enter. Then
   make the test folder:

   ```sh
   cp -R "$KIT/expert/23-a-workflow-with-a-stop-rule/start" ~/workflow-test
   cd ~/workflow-test
   git init -q && git add -A && git -c user.name=reader -c user.email=reader@example.com commit -qm start
   ls
   ```

   You see `CLAUDE.md`, `changes.py`, `shipments-export-sample.csv` and `test_changes.py`. The two `-c` parts give this
   one commit a name, so it works even if git does not know yours yet. The commit is your undo point.
3. Run the test:

   ```sh
   python3 test_changes.py
   ```

   It prints `FAIL: changes.py does not print the three expected lines.` and the lines above.
4. Make the Terminal window full screen with the green button at its top left, so the script in step 5 has room.
   Start `claude` in the folder. If it asks whether you trust the folder, choose `Yes, I trust this folder`. Press
   `Shift+Tab` until the bottom line says `accept edits on`. Paste the workflow ask:

   ```text
   Use a workflow for this job: run python3 test_changes.py, fix changes.py, then run the test again. Repeat until the test passes, or stop after two rounds in a row with no progress. Never change test_changes.py or the CSV.
   ```

   Claude may ask before it runs the test first (1 of 6 sessions). Read the command and choose `1. Yes`.
5. Claude Code asks `Run a dynamic workflow?` with three options: `1. Yes, run it`, `2. View raw script`, `3. No`.
   Press `2`. The script is short (ours had 34 lines). Find the loop, the place where it counts a round without
   progress, and the place where it stops after 2 of them: an `if` line or the `while` line itself. Check what it
   compares to decide that a round made progress. In one of our runs it compared the agent's own description of the
   failure, which changed every round, so the no-progress rule never stopped the loop. Then press `1`
   (`Yes, run it`). In the script view, option 2 reads `View workflow summary`. Do not press `ctrl+g`: it opens the
   script in an editor, and we did not test that. Our window was 160 by 50 and the whole script was on screen. In a
   smaller window you may have to scroll. We did not test that.

   If you cannot find a stop rule, press `3` (`No`). The docs say No cancels the run. Then ask Claude to add a stop
   rule before you run it again. We did not test that path.
6. The line `Running in background · /workflows to monitor and save · medium size (/config)` shows that it runs. Then the permission
   questions come. A question from the workflow agent says so in its first line, for example
   `Bash command · from the "fix-changes-loop" workflow`. This is what we saw in the 5 sessions of our test, and in
   one more where the test script followed these steps as written:

   | Question | From | What the command did |
   |---|---|---|
   | First | the workflow agent | showed the files and ran the test (6 of 6) |
   | Then | the workflow agent | ran the test again. In 5 of 6 sessions the same command also made the fix with `sed -i` |
   | Last | the main session | a last check after the workflow (6 of 6), for example the test and `git diff` |

   Read each command, then press `1` (Yes). Do not choose the option that turns on auto mode or "don't ask again": we
   did not test those in accept edits mode. Some commands name `test_changes.py` to read or run it. You do not have to
   judge each one: step 8 checks that the test and the CSV are unchanged, and puts them back if not. We did not test
   choosing `No` inside a workflow.
7. When Claude reports the result, type `/workflows`. You see the run with `1/1 agent` and `done`. Press `s`. The save
   dialog shows `Project scope · .claude/workflows/` and a name. Press Enter. Note the name in the line
   `Dynamic workflow saved to ...`: we saw `fix-changes-loop`, `fix-changes-until-green` and `fix-changes-until-pass`.
   Press Esc.
8. Type `/exit`. Check the result:

   ```sh
   python3 test_changes.py
   git status --short
   git diff changes.py
   shasum -a 256 test_changes.py shipments-export-sample.csv
   ```

   The test prints `PASS: changes.py prints the three expected lines.` `git status --short` shows ` M changes.py` and
   `?? .claude/`. `git diff` shows what the agent changed in `changes.py`: read it, and check that it fixes the sort
   and does not only print the expected lines. The two fingerprints must be these:

   ```text
   faa7ba184868d4ec6a65d0bf923da8268d083c0d3c8d243e46099b2562f7922c  test_changes.py
   6311ca605c81fa4581e076c704225828dd6b4a29becf79e99e518f39d4b1eb09  shipments-export-sample.csv
   ```

   If one is different, put both files back from your undo point with
   `git checkout test_changes.py shipments-export-sample.csv`.

9. Run it again. Put the bug back, check that the test fails, and start a new session:

   ```sh
   git checkout changes.py
   python3 test_changes.py
   claude
   ```

   Press `Shift+Tab` until the bottom line says `accept edits on`, type `/` and the name from step 7 (for example `/fix-changes-loop`), and press
   Enter. The question now has 4 options: `1. Yes, run it`, `2. Yes, and don't ask again for ...`, `3. View raw script`
   and `4. No`. Press `1`, and answer the permission questions as in step 6. At the end, type `/exit` and check the
   result as in step 8.
10. Optional: test the stop rule. Put the bug back and make the test impossible: it will expect `-25` for
    BE-FR, while 48 minus 71 is -23. Then run the saved workflow again:

    ```sh
    git checkout changes.py
    sed -i '' 's/48  -23"/48  -25"/' test_changes.py
    python3 test_changes.py
    claude
    ```

    The test prints `FAIL` and expects `3. route  BE-FR    71 ->   48  -25`. Start the saved workflow as in step 9 and
    answer the questions as in step 6. No honest fix can pass this test. The loop ends on its stop rule, or on its
    round cap if the script has one. In our run, the stop rule never fired: the loop ran all 8 rounds of its cap, with
    10 permission questions and about 708,000 tokens. When Claude reports, type `/workflows` to see how many rounds
    ran (we saw `8/8 agents`), and press Esc. Then type `/exit` and put the test back:

    ```sh
    git checkout test_changes.py changes.py
    python3 test_changes.py
    ```

    The test fails again with the planted bug, as in step 3. To stop a run yourself, the docs say: type `/workflows`,
    select the run and press `x`. We did not test that.
11. To take it out: type `/exit` if Claude Code is still open, then delete the `workflow-test` folder in your home
    folder. In Finder, choose Go, then Home, to see it.

## The script we saved

This is one script, as Claude Code saved it in one session. Yours will differ.

```js
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
```

- `meta` gives the name. That is the slash command after you save it.
- `while (true)` is the loop. Each round starts one agent with the prompt in backticks. The prompt repeats the rules
  from the ask: fix `changes.py` only, no hard-coded output, do not touch the test or the CSV.
- `SCHEMA` makes the agent answer with `passed` and `failing_count`, so the script can count.
- `if (r.passed) return` stops on a pass. Line 31 counts a round without progress. Line 33 stops after 2 of them.
- There is no round cap of its own. Only a pass or the no-progress rule ends this loop.

## The boundary

- **Claude writes a new script for each workflow ask.** The 9 scripts we saved from the workflow ask were all different. Read the
  one you get, not ours.
- **The stop rule is only as good as its progress measure.** On the test that cannot pass, two scripts compared the
  failures before and after each round. The real fix left 1 failure before and 1 after, so they counted it as no
  progress. The script in step 10 also counted a new description of the same failure as progress, so its no-progress
  rule never stopped the loop.
- **Some scripts add a round cap, some have none.** The script above stops only on a pass or on 2 rounds without
  progress. In step 10, the cap of 8 rounds was what ended the loop. The docs name a runtime limit of 1,000 agents per run (12 Nov 2026).
- **A workflow cost more here.** About twice the tokens in total, 3.5 to 5 times as many without cache reads, and as
  many or more permission questions on this job. The question
  before each run says it "counts against your usage limit".
- **Accept edits mode still asks before shell commands.** The workflow agent ran the test with shell commands, so it
  asked before most of them. In auto mode we got 0 questions before commands in 2 sessions.
- **In auto mode, you may not see the script.** The docs say auto mode asks before a workflow runs only the first
  time. After that, a new script starts without the question, so you cannot read its stop rule first.
- **Rules in the ask and in CLAUDE.md are text, not a lock.** Claude changed neither file in the 24 sessions. For a
  guard, use a hook as in step 22: it ran inside the workflow agents in the 1 session that had them.
- **The size line is advice.** After Yes, Claude Code showed `medium size (/config)`. The docs call this size
  guideline "advice, not a cap".
- **One model, one Mac.** Claude Code 2.1.322 and 2.1.323, Opus 5.5, on 12 and 13 Nov 2026. The feature can change.

## Common mistakes

| Mistake | What to do |
|---|---|
| `cp: ... No such file or directory` in step 2 | Your kit copy is older than this step, or `KIT` is not set. Type `ls "$KIT/expert"`: it must list `23-a-workflow-with-a-stop-rule`. If not, do step 1 again, delete the old kit folder first, then step 2 again |
| `ls` in step 2 shows a folder named `start` | The `workflow-test` folder was there already. Delete it in Finder and do step 2 again |
| `python3` or `git` is not found, or a window offers to install developer tools | Accept the install, delete the `workflow-test` folder in Finder, then run step 2 again. We did not test this |
| No `Run a dynamic workflow?` question | The docs say that on Pro you turn workflows on in `/config`, and that an admin can turn them off for a whole organization. We did not test Pro. Put the bug back with `git checkout changes.py`, check that the ask starts with `Use a workflow for this job:`, and do step 4 again |
| You chose option 2 at a permission question | We did not test that. Do not exit: the docs say a run stops when you exit Claude Code. Let it finish, go on with step 7, and check the two files in step 8 |
| Your slash command is not `/fix-changes-loop` | Use the name from the saved line in step 7 |
| You expect the workflow to do better | Both asks fixed the bug. The workflow used about twice the tokens, 3.5 to 5 times as many without cache reads. It is worth it when you want to read the stop rule first, or run the same loop again |

## In our own work

Our own build system runs from workflow files too, in another format (YAML, not a Claude Code script). On 12 Nov 2026
it had 33 of them. One has four loops, and each loop has its stop rule in the file: an `until` condition and a cap of
10 or 15 rounds.

## Next

Step 24: AI review.
