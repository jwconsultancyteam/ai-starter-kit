# Builder, step 11: Claude Code on the web

Claude Code is Claude working in the files of your project, not in a chat window. On the web it runs in a sandbox that
Anthropic hosts, so there is nothing to install. It works on its own branch, and you read the change before it goes in.

This step picks up where [step 10](../../starter/10-scheduled-tasks/) stopped. There, the Monday report chose its own
"three biggest changes" and left out route NL-BE. Here, Claude Code writes a small script with that rule written down,
so the answer is the same every week.

| | |
|---|---|
| Time to set up | about 15 minutes, including your first repository |
| You need | a Claude account on Pro, Max, Team or Enterprise (not on Free), and a GitHub account (free is enough) |
| Tested | claude.ai/code in a Chromium browser, Team plan, [FILL date of recording] |
| Download | [shipments-export-sample.csv](shipments-export-sample.csv), [task-prompt.txt](task-prompt.txt), [expected-output.md](expected-output.md), [first-repository.md](first-repository.md) |

## Before and after

The same job: "the three biggest changes between last week and the week before".

| | Step 10 (a Cowork task) | Step 11 (Claude Code on the web) |
|---|---|---|
| What Claude does | Does the whole job again every Monday | Writes a script once, with the rule in it |
| The pick | Its own. In our run it left out NL-BE (+24) | The rule decides: biggest change up or down, clients and routes |
| Where the result lives | A chat and three files | A script and a README in your repository |
| Can you check it | You read the result each time | You read the rule once, and the output matches a separate count |

## Where

1. Make a repository with the sample export in it. No GitHub experience? Follow [first-repository.md](first-repository.md).
2. Go to **claude.ai/code** and sign in.
3. Approve the GitHub authorization when it asks.
4. If it offers the **Claude GitHub App**: choose **Only select repositories** and pick your test repository.
   Do not give it all your repositories.
5. Pro and Max get a **Default** environment. On Team and Enterprise you see **Create your first cloud environment**:
   click **Create & finish**. (On Team and Enterprise an Owner must first turn on the GitHub connector in
   Organization settings > Connectors.)
6. Below the message box, pick your repository and the branch **main**.
7. Pick the mode **Plan**. Claude shows its plan before it changes a file.

![Where: repository, branch and mode](images/where.jpg)

## The task

Paste [task-prompt.txt](task-prompt.txt):

> Write a small Python script, changes.py, that reads shipments-export-sample.csv and prints the three biggest changes
> in pallets between the last week in the file and the week before. Count every client and every route, and rank by
> the size of the change, up or down. Use ISO weeks. Add a README that explains the rule and how to run it. Run it
> once on the sample file and show me the output.

[FILL from the recording: what the plan said, what you approved, the files and the diff count.]

![The plan](images/plan.jpg)

## Check the result

The output must match [expected-output.md](expected-output.md), which we counted with a separate script:

```text
route BE-BE: 25 -> 60 (+35)
route NL-BE: 77 -> 101 (+24)
route BE-FR: 71 -> 48 (-23)
```

If your numbers differ, ask Claude why before you accept anything. Do not fix the expected numbers to match.

![The diff and the output](images/result.jpg)

## Keep it or throw it away

- **Keep it:** click **Create PR**, then merge it in GitHub. Now the script is in your main version.
- **Throw it away:** do nothing. Your main version did not change. The work stays on its own branch.

## Good to know

- It uses your normal Claude limits. Several tasks at once use more.
- A session that sits idle for a while is closed. When you reopen it, the conversation is back, but anything that was
  still running in the background is not.
- Never put real client data in a test repository. The sample export is made up.
- Mods, hooks and the terminal come later. Today is only the web.

## Time win and solution win

- **Time win:** no more checking the pick every Monday. Our estimate: 5 minutes a week.
- **Solution win:** the rule for "biggest change" is in a file you can read and change. Same file, same answer.

## Common mistakes

| Mistake | Fix |
|---|---|
| The repository list is empty | Give the Claude GitHub App access to that repository (step 4) |
| You picked Auto or Accept edits | Start in Plan the first time, so you see what it will do |
| Real data in the test repository | Use the made-up sample only |
| The output differs from expected-output.md | Ask Claude to explain the difference before you merge |

## What we call this in our own work

A change on its own branch, read before it goes in. In pharma IT this is change control. Here it is one button.

## Next

Step 12 (Saturday): what Claude Code just did has a name. A goal, tools, a loop and a stop rule. That is an agent.
