# Builder, step 20: Other models with Pi

Pi is a coding agent, like Claude Code, that works with models from many companies. We ran the step 11 task on 4 setups,
with Pi and with Claude Code. The same model, DeepSeek V4.1 Flash, gave two different answers to the same ask. Then we
made the ask sharper, and all 8 runs matched our count.

So your task in this step is the sharper ask, in the Claude Code you already have. Then the
[step 19](../19-tests-and-security-checks/) test checks the same three lines. Pi is optional, at the end, because it has
no built-in permission system.

| | |
|---|---|
| Time | about 10 minutes (our estimate). The Pi part is extra |
| You need | Claude Code in a terminal ([step 13](../13-claude-code-on-your-laptop/)) and Python. You install pytest below. Our commands are for a Mac. On Windows, see Good to know |
| Tested | a Mac, Claude Code 2.1.316 and Pi 0.86.0, 31 Oct 2026. Details under How we measured |
| Download | [sharper-ask.txt](sharper-ask.txt) and [the carousel as a PDF](builder-step20-other-models-with-pi-carousel.pdf) (8 slides). You also use [shipments-export-sample.csv](../11-claude-code-on-the-web/shipments-export-sample.csv) from step 11 and [test_changes.py](../19-tests-and-security-checks/test_changes.py) from step 19 |

## Four words first

| Word | What it is |
|---|---|
| Pi | A coding agent for the terminal, from [earendil-works/pi](https://github.com/earendil-works/pi). It can use models from many companies |
| OpenRouter | One account and one API key for models from many companies. You pay per use |
| Flash model | A company's cheaper model. Here: DeepSeek V4.1 Flash and Qwen3.8 Flash |
| Sandbox | A wall around a program, so it can reach less. A container is one kind |

## Our test

The first ask is the step 11 task, word for word:

> Write a small Python script, changes.py, that reads shipments-export-sample.csv and prints the three biggest changes
> in pallets between the last week in the file and the week before. Count every client and every route, and rank by
> the size of the change, up or down. Use ISO weeks. Add a README that explains the rule and how to run it. Run it
> once on the sample file and show me the output.

**Two checks.** Our count is in step 11's [expected-output.md](../11-claude-code-on-the-web/expected-output.md): route
BE-BE +35, route NL-BE +24, route BE-FR -23. It uses the reading we picked on step 11: clients and routes ranked
together. The step 19 test is stricter, because it also pins the format of each line.

### The first ask

| Setup | Matched our count | Step 19 test | Time per run | Cost per run |
|---|---|---|---|---|
| Pi, DeepSeek V4.1 Flash | 2 of 3 | 0 of 3 | 27 and 57 seconds, one run not timed | under 1 cent |
| Pi, Qwen3.8 Flash | 0 of 2 | 0 of 2 | 113 and 216 seconds | under 2 cents |
| Claude Code, Opus 5.5 | 0 of 2 | 0 of 2 | 64 and 65 seconds | 35 and 36 cents, as shown |
| Opus 5.5 plans, then Pi with DeepSeek builds | 0 of 2 | 0 of 2 | 76 and 84 seconds | 31 cents, as shown |

So 2 of 9 runs matched our count, and the step 19 test went red on all 9: 7 runs counted client and route pairs, and the
other 2 had our numbers in another format. The 7 did not count wrong. They answered another question. "Count every client
and every route" can be read more than one way, and step 11 lists three readings. After a header line, one Opus 5.5 run
printed:

```text
1. Alpha Retail (example), BE-NL: 33 -> 0 (-33)
2. Alpha Retail (example), NL-BE: 19 -> 49 (+30)
3. Delta Home (example), BE-FR: 24 -> 3 (-21)
```

Both Opus 5.5 runs said which reading they chose, and gave our three numbers as the other reading. On step 11, Opus 5.5
stopped, asked us and recommended pairs. These runs used print mode (`claude -p`, `pi -p`), with nobody to answer. Step 11
also ran in Plan mode on the web at Extra effort. We did not test which difference was the cause.

DeepSeek read the same ask both ways: pairs on one run, each client and each route on its own on two. With an Opus plan
in front of it, DeepSeek counted pairs: the plan said pairs.

### The sharper ask

We added two sentences to the same task. [sharper-ask.txt](sharper-ask.txt) is the task plus these:

```text
Count each client on its own and each route on its own, not client and route pairs. Print one header line, then the three changes, each line in exactly this format: 1. route  AA-BB    10 ->   20  +10
```

| Setup | Matched our count | Step 19 test | Time per run | Cost per run |
|---|---|---|---|---|
| Pi, DeepSeek V4.1 Flash | 2 of 2 | 2 of 2 | 44 and 47 seconds | under 1 cent |
| Pi, Qwen3.8 Flash | 2 of 2 | 1 of 2 | 152 and 172 seconds | under 1 cent |
| Claude Code, Opus 5.5 | 2 of 2 | 2 of 2 | 48 and 67 seconds | 28 and 36 cents, as shown |
| Opus 5.5 plans, then Pi with DeepSeek builds | 2 of 2 | 2 of 2 | 75 and 95 seconds | 25 and 27 cents, as shown |

So 8 of 8 runs matched our count, and 7 of 8 passed the test. The one red test had the right numbers and different
spacing. The test pins the exact format, so it goes red on that too.

**How we measured.** Each run started on a new copy of the step 11 repository, with only a README and the made-up CSV.

- Pi ran with `pi -p`, a new home and settings folder, no extensions, no skills, no context files and telemetry off, with
  JSON output and its own session folder, in a macOS sandbox. The sandbox blocked writes outside the run folder and
  the system temp folder, and reads of some folders. It did not block the network or most other reads.
- Claude Code ran with `claude -p`, `--setting-sources project,local`, accept edits mode, and single Python commands
  allowed, with no sandbox and our real home folder reachable. Two runs said in their answer that test files were outside the
  repository. Our logs do not show where. A separate run with the same setting sources said no CLAUDE.md or memory contents were loaded. We cannot rule out that
  our machine played a part.
- Time is the clock around the run. Cost for Pi is the cost in Pi's own output. Cost "as shown" is the figure Claude Code
  reports, plus Pi's cost for the build. We ran Claude Code signed in with a plan, so that figure is not a bill we paid.
- In the plan setup, Claude Code stayed in plan mode. It saved its plan in its own plans folder. Its answer went to Pi
  with "Carry out this plan." The sandbox kept Pi from the saved plan file, so Pi had only that answer.

**The third DeepSeek run.** It was an early test of our test script, with the same ask and model, and we did not time it. It
is in the table because it counted.

**Runs not in the tables.** One DeepSeek run on the first ask finished, but our test script crashed while it saved the
result. We do not have its answer, so we ran it again. One Qwen run on the first ask hit our 4-minute limit for Pi, so we
stopped it and ran it again. Two Claude Code runs failed before they started, from a mistake in our command, so we ran
them again.

**What this does not show.**

- A few runs of one small task. It does not rank these models.
- Each model ran in one tool only: Opus 5.5 in Claude Code, the Flash models in Pi. So this does not separate the model
  from the tool.
- We wrote the sharper ask after we knew the answer, and its format line says `route`. No run tested the first sentence
  alone. On real work you do not know the answer first.

## Do it yourself

We ran the ask once on a Mac, in a normal Claude Code session on an Ultra plan with Opus 5.5, in manual mode
([step 15](../15-plan-mode-and-undo/)) with `--setting-sources project,local`. Our own add-ons still ran in that session. The folder held the CSV and the ask,
not under the name below. It asked 5 times: once to trust the folder, then before some commands and each new
file. A script of ours typed yes each time. Then we ran the commands in step C on a copy of that folder, and got the
three lines below and `1 passed`. Your plan and model may differ. The letters A to D are only for this page.

**A. Make a folder.** Download `sharper-ask.txt`, `shipments-export-sample.csv` and `test_changes.py` from the Download
row. Move two of them in. Leave the test in Downloads for now, so Claude does not write to pass it.

```bash
mkdir ~/ask-test
cd ~/ask-test
mv ~/Downloads/shipments-export-sample.csv ~/Downloads/sharper-ask.txt .
cat sharper-ask.txt
```

**B. Run the ask.** Copy the text that `cat` printed. Start Claude Code, paste it and press Enter. Read each question
before you say yes. Type `/exit` when it is done.

```bash
claude
```

**C. Check it yourself.** Do not take the agent's word for it.

```bash
mv ~/Downloads/test_changes.py .
python3 -m venv .venv
.venv/bin/python -m pip install pytest
python3 changes.py
.venv/bin/python -m pytest test_changes.py
```

You want one header line, then these three lines, and `1 passed`:

```text
1. route  BE-BE    25 ->   60  +35
2. route  NL-BE    77 ->  101  +24
3. route  BE-FR    71 ->   48  -23
```

**To start over.** The first line makes a new empty folder with its own name, each time:

```bash
cd "$(mktemp -d ~/ask-try-XXXX)"
cp ~/ask-test/shipments-export-sample.csv ~/ask-test/sharper-ask.txt .
claude
```

Paste the ask. After `/exit`, download a new copy of the test and run all of step C in this folder.

**D. Try the first ask.** Look at which question your model answers. It may stop and ask you, as it did on step 11. If it
does, pick the reading you want. Each try gets a new folder:

```bash
cd "$(mktemp -d ~/ask-try-XXXX)"
cp ~/ask-test/shipments-export-sample.csv .
claude
```

Paste the first ask from Our test above, and type `/exit` when it is done. The step 19 test is not for this try, because
this ask does not pin the format. We ran this ask with `claude -p`, not in this kind of session.

## Pi is optional, and at your own risk

Pi's README: "Pi does not include a built-in permission system for restricting filesystem, process, network, or
credential access. By default, it runs with the permissions of the user and process that launched it."

So Pi has no permission prompt of its own, as Claude Code has in [step 15](../15-plan-mode-and-undo/). In our `pi -p` runs
it ran its commands with no question. It can run any command that you can run. A new folder does not stop it. It can read and change any file that you can, it can reach the network, and it
can read your key. In our runs Pi tried to read a plan file outside its folder and to write in `/tmp`, and only the
sandbox stopped it. Pi's README: "If you need stronger boundaries, containerize or sandbox Pi."

**Run this part only on a spare computer or in a container. If you have neither, skip it.** The results above are the
point of this step. We give no steps for a container here.

We did not test the install, the OpenRouter pages or this short command. Our runs used the flags under How we measured.

1. That computer also needs Python. Install Pi. Its README: "Pi requires Node.js 22.19 or newer. The macOS, Linux, and Windows installers can install it
   if needed." Then open a new terminal and run `pi --version`.

   ```bash
   curl -fsSL https://pi.dev/install.sh | sh
   ```

2. Make an account on openrouter.ai. Add a little credit at openrouter.ai/settings/credits and create a key at
   openrouter.ai/settings/keys. We did not check the smallest amount. Our runs cost cents. Set a low credit limit on the
   key if that page offers one. In the terminal, paste this line and press Enter, then paste the key and press Enter. It
   does not show, and it does not go in your shell history. Then paste the second line. Stay in this window for step 3:

   ```bash
   read -s OPENROUTER_API_KEY
   ```

   ```bash
   export OPENROUTER_API_KEY
   ```

3. Download the three files on that computer, make a folder and run the ask. To stop Pi, press Ctrl+C.

   ```bash
   mkdir ~/pi-test
   cd ~/pi-test
   mv ~/Downloads/shipments-export-sample.csv ~/Downloads/sharper-ask.txt .
   pi -p --model openrouter/deepseek/deepseek-v4.1-flash "$(cat sharper-ask.txt)"
   ```

   Then check it. These are the same commands as step C:

   ```bash
   mv ~/Downloads/test_changes.py .
   python3 -m venv .venv
   .venv/bin/python -m pip install pytest
   python3 changes.py
   .venv/bin/python -m pytest test_changes.py
   ```

4. Delete the key at openrouter.ai/settings/keys when you are done.

## Good to know

- **Windows.** We tested on a Mac only. On Windows, put the CSV and `sharper-ask.txt` in a new folder by hand, start
  Claude Code there and paste the ask. Add the test only after the run. Then ask Claude Code to install pytest in a
  `.venv` as in step 19 and run the test. We did not test this.
- **Pi has no built-in plan mode.** Pi's README: "Pi ships with powerful defaults but skips features like sub-agents and
  plan mode." In our test, plan and build were two runs.
- **Use an API key in Pi.** Our Pi runs used an OpenRouter key. We did not test a Claude subscription login. Check
  Anthropic's terms first.
- **What OpenRouter stores.** Its page: "OpenRouter does not store your prompts or responses". There are exceptions on
  that page, and each model provider has its own policy. We did not check those policies, so we used made-up data only.
- **Model names and prices change.** We read them on 31 Oct 2026. Check them on openrouter.ai.
- **A test checks only what it checks.** Ours pins three lines from one sample file. It went red on 3 runs with the right
  numbers, and it cannot tell you which reading you meant. So you need a count you already trust first, as in step 11.
- **Step 12 has a line for this.** Its [example brief](../12-what-an-agent-is/agent-brief-example-step11.txt) has a "Stop and ask me when" line. No run here used it.
- **New at Claude this week.** The plans now read: Max, USD 100 a month, 5x Pro usage. Ultra, USD 200 a month, 10x Pro
  usage. Ultra has no 5-hour limit on verified accounts. It still has a weekly limit. Fast mode for Opus 4.8 is deprecated, and is removed on 30 Nov. Sources:
  [claude.com/pricing](https://claude.com/pricing), [What is the Ultra plan?](https://support.claude.com/en/articles/17728952)
  and the [Claude Code changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

## Time win and solution win

- **Time win:** a rerun in Claude Code took about a minute on this small task. The first ask took 64 and 65 seconds, the
  sharper ask 48 and 67.
- **Solution win:** the test checks the same three lines whatever the model, so you do not take its word for it. It
  checks only those lines.

## Common mistakes

| Mistake | What to do |
|---|---|
| You put `test_changes.py` in the folder before the run | Claude can read the answer, and could have changed the test. Use To start over above |
| `mv` says `No such file or directory` | Find the file in your browser's downloads list, then move it |
| The test is red and the numbers are right | Only the format differs. Do not edit the test. Ask: "Change only the print format of changes.py to match sharper-ask.txt." We did not test this |
| The test is red and the numbers differ | Do not edit the test. Use To start over above. If it differs again, your model read the task another way |
| The first ask gives lines that name a client and a route | Your model counted pairs. That is a fair reading. The sharper ask is for this |
| `No module named pytest` | Use `.venv/bin/python`, as in step C, not plain `python3` |
| You run Pi on a computer with real work | Press Ctrl+C. Read the Pi part again before you go on |

## In our own work

On step 11, in Plan mode on the web, Opus 5.5 asked us what counts as one item and recommended pairs. We picked clients
and routes pooled, so its script gave the three route lines. On 31 Oct, with `claude -p` and nobody to answer, it chose
pairs on 2 of 2 runs and said so: its own pick was pairs both times. So the same ask can give another answer when nobody
settles the reading. Our step 11 ask stays as it was in this test, and the sharper ask is here. This step shows Pi only in
this test.

## Next

The Expert level, steps 21 to 30, starts with guardrails.
