# Builder, step 20: Other models with Pi

Pi is a coding agent, like Claude Code, that works with models from many companies. So you can try a cheaper model on a
task like your real work, with made-up data. The [step 19](../19-tests-and-security-checks/) test checks the same three
lines, whatever the model is called.

We ran the step 11 task on 4 setups. The same model gave two different answers to the same ask. Then we made the ask
sharper, and all 8 runs matched our count. A bigger model was not the fix here. A clearer ask was.

| | |
|---|---|
| Time | about 20 minutes (our estimate) |
| You need | a Mac or Linux terminal ([step 13](../13-claude-code-on-your-laptop/)), an OpenRouter account with a little credit, and Python. You install pytest below. Windows is not covered in this step |
| Tested | a Mac, Pi 0.86.0 and Claude Code 2.1.316, 31 Oct 2026. Each run started on a new copy of the step 11 repository, with only a README and the made-up CSV. Pi ran with `pi -p`, a new settings folder, no extensions, no skills and no context files, in a macOS sandbox. Claude Code ran with `claude -p`, `--setting-sources project,local`, accept edits mode, and single Python commands allowed. Other shell commands were refused in those runs |
| Download | [sharper-ask.txt](sharper-ask.txt) and [the carousel as a PDF](builder-step20-other-models-with-pi-carousel.pdf) (8 slides). You also use [shipments-export-sample.csv](../11-claude-code-on-the-web/shipments-export-sample.csv) from step 11 and [test_changes.py](../19-tests-and-security-checks/test_changes.py) from step 19 |

## Four words first

| Word | What it is |
|---|---|
| Pi | A coding agent for the terminal, from `earendil-works/pi`. It can use models from many companies |
| OpenRouter | One account and one API key for models from many companies. You pay per use |
| API key | A secret that lets a program spend your credit. Treat it like a password |
| Flash model | A company's cheaper, faster model. Here: DeepSeek V4.1 Flash and Qwen3.8 Flash |

## Read this before you install Pi

Pi's README: "Pi does not include a built-in permission system for restricting filesystem, process, network, or
credential access. By default, it runs with the permissions of the user and process that launched it."

So Pi does not stop to ask, as Claude Code does in [step 15](../15-plan-mode-and-undo/). It can run any command that you
can run. Pi's README: "If you need stronger boundaries, containerize or sandbox Pi."

We ran it in a macOS sandbox, on a copy of the folder. **Your run below has no sandbox.** A new folder does not stop Pi:
it can read and change any file that you can, and it can read the key. In our runs Pi tried to go outside its folder, and
only the sandbox stopped it. So use made-up data, and use a spare user account or a container if that computer holds work
you care about.

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

So 2 of 9 runs matched our count, and the step 19 test went red on all 9. The other 7 runs did not count wrong. They answered another question. "Count every client and every route" can be read
more than one way. Step 11 lists three readings. The 7 runs counted client and route pairs. Opus 5.5 printed:

```text
1. Alpha Retail (example), BE-NL: 33 -> 0 (-33)
2. Alpha Retail (example), NL-BE: 19 -> 49 (+30)
3. Delta Home (example), BE-FR: 24 -> 3 (-21)
```

Both Opus 5.5 runs said which reading they chose, and gave our three numbers as the other reading. On step 11, Opus 5.5
stopped and asked us. In `claude -p` and `pi -p` nobody could answer.

DeepSeek read the same ask both ways: pairs on one run, each client and each route on its own on two. With an Opus plan
in front of it, DeepSeek counted pairs: the plan said pairs.

### The sharper ask

We added two sentences to the same task. [sharper-ask.txt](sharper-ask.txt) is the task plus these:

> Count each client on its own and each route on its own, not client and route pairs. Print one header line, then the
> three changes, each line in exactly this format: 1. route  AA-BB    10 ->   20  +10

| Setup | Matched our count | Step 19 test | Time per run | Cost per run |
|---|---|---|---|---|
| Pi, DeepSeek V4.1 Flash | 2 of 2 | 2 of 2 | 44 and 47 seconds | under 1 cent |
| Pi, Qwen3.8 Flash | 2 of 2 | 1 of 2 | 152 and 172 seconds | under 1 cent |
| Claude Code, Opus 5.5 | 2 of 2 | 2 of 2 | 48 and 67 seconds | 28 and 36 cents, as shown |
| Opus 5.5 plans, then Pi with DeepSeek builds | 2 of 2 | 2 of 2 | 75 and 95 seconds | 25 and 27 cents, as shown |

So 8 of 8 runs matched our count, and 7 of 8 passed the test. The one red test had the right numbers and different
spacing. The test pins the exact format, so it goes red on that too.

**How we measured.** Time is the clock around the run. Cost for Pi is the cost in Pi's own output. Cost "as shown" is
the figure Claude Code reports, plus Pi's cost for the build. We ran Claude Code signed in with a plan, so that figure
is not a bill we paid. In the plan setup, Claude Code stayed in plan mode and changed nothing in the project folder. It
saved its plan in its own plans folder. Its answer went to Pi with "Carry out this plan."

**Runs not in the tables.** One DeepSeek run on the first ask finished, but our script crashed while it saved the result.
We do not have its answer, so we ran it again. One Qwen run on the first ask hit our 4-minute limit, so we stopped it and
ran it again. Two Claude Code runs failed before they started, from a mistake in our command, so we ran them again.

**What this does not show.**

- A few runs of one small task. It does not rank these models.
- Each model ran in one tool only: Opus 5.5 in Claude Code, the Flash models in Pi. So this does not separate the model
  from the tool.
- We wrote the sharper ask after we knew the answer, and its format line says `route`. No run tested the first sentence
  alone. On real work you do not know the answer first.

## Do it yourself

We ran the same models and the same asks, with the extra flags in the Tested row. We did not run the short command in
step 4 in this form, and we did not test the install. We give no clicks for OpenRouter: our account already existed, and
we did not walk them.

1. Install Pi. Its README: "Pi requires Node.js 22.19 or newer. The macOS, Linux, and Windows installers can install it
   if needed."

   ```bash
   curl -fsSL https://pi.dev/install.sh | sh
   ```

   Then open a new terminal and check it:

   ```bash
   pi --version
   ```

2. Make an account on openrouter.ai, add a little credit and create an API key. Set a low credit limit on the key if
   you can. Pi can read this key. Then, in the terminal, paste this line and press Enter:

   ```bash
   read -s OPENROUTER_API_KEY
   ```

   Paste the key and press Enter. It does not show, and it does not go in your shell history. Then paste these two lines.
   The second prints only the length of the key, so it must not print 0:

   ```bash
   export OPENROUTER_API_KEY
   echo ${#OPENROUTER_API_KEY}
   ```

3. Download the three files in the Download row. Make a new folder and move two of them in. Leave `test_changes.py` in
   Downloads for now. Pi can read and change any file in its folder, and in our runs the test was not there.

   ```bash
   mkdir ~/pi-test
   cd ~/pi-test
   mv ~/Downloads/shipments-export-sample.csv ~/Downloads/sharper-ask.txt .
   ```

4. Run the ask. Pi does not ask before it runs a command. In our runs this took under 3 minutes:

   ```bash
   pi -p --model openrouter/deepseek/deepseek-v4.1-flash "$(cat sharper-ask.txt)"
   ```

5. Check it yourself. Do not take the agent's word for it. Now move the test in and install pytest in this folder:

   ```bash
   mv ~/Downloads/test_changes.py .
   python3 -m venv .venv
   .venv/bin/python -m pip install pytest
   python3 changes.py
   .venv/bin/python -m pytest test_changes.py
   ```

   You want one header line, then these three lines, and `1 passed`. We ran the three pytest commands on a Mac with a
   script from our runs:

   ```text
   1. route  BE-BE    25 ->   60  +35
   2. route  NL-BE    77 ->  101  +24
   3. route  BE-FR    71 ->   48  -23
   ```

6. Try the first ask too. Look at which question your model answers, and run it more than once. Models and prices change,
   and yours may read it another way. The test goes red on this one, because the first ask gives no format:

   ```bash
   mkdir ~/pi-test-2
   cd ~/pi-test-2
   cp ~/pi-test/shipments-export-sample.csv .
   pi -p --model openrouter/deepseek/deepseek-v4.1-flash "Write a small Python script, changes.py, that reads shipments-export-sample.csv and prints the three biggest changes in pallets between the last week in the file and the week before. Count every client and every route, and rank by the size of the change, up or down. Use ISO weeks. Add a README that explains the rule and how to run it. Run it once on the sample file and show me the output."
   ```

## Good to know

- **Pi has no plan mode.** Pi's README: "Pi ships with powerful defaults but skips features like sub-agents and plan
  mode." In our test, plan and build were two runs.
- **Use an API key in Pi.** Our Pi runs used an OpenRouter key. We did not test a Claude subscription login. Check
  Anthropic's terms first.
- **What OpenRouter stores.** Its page: "OpenRouter does not store your prompts or responses". There are exceptions on
  that page, and each model provider has its own policy. We did not check those policies, so we used made-up data only.
- **Model names and prices change.** We read them on 31 Oct 2026. Check them on openrouter.ai.
- **A test checks only what it checks.** Ours pins three lines from one sample file. It went red on 3 runs with the right
  numbers, and it cannot tell you which reading you meant. So you need a count you already trust first, as in step 11.

## Time win and solution win

- **Time win:** the runs we timed took 27 to 216 seconds. Our limit was 4 minutes. One more Qwen run hit it, and we ran
  it again.
- **Solution win:** the test checks the same three lines whatever the model, so you do not take its word for it. It
  checks only those lines.

## Common mistakes

| Mistake | What to do |
|---|---|
| You run Pi in a folder with real work | Stop. Pi does not ask first, and a new folder does not limit it. Use made-up data, and a spare account or a container if that computer holds work you care about |
| You paste your key into a file | Use step 2. Pi can read any file, and a file can reach GitHub if the folder becomes a repository |
| You put `test_changes.py` in the folder before Pi runs | Pi can read the answer or change the test. Start again in a new folder |
| The test is red and the numbers are right | Only the format differs. Do not edit the test. Run step 4 again in a new folder. We did not test this |
| The three lines name a client and a route | Your model counted pairs. Use the sharper ask |
| `command not found: pi` after the install | Open a new terminal. Then do step 2 again and `cd ~/pi-test`, because a new terminal loses both. We did not test this |
| Pi prints an error about the key, credit or model, or there is no `changes.py` | Do step 2 again in this terminal, check your credit on openrouter.ai and check the model name there. We did not test this |
| `No module named pytest` | Use `.venv/bin/python`, as in step 5, not plain `python3` |

## In our own work

On step 11, in Plan mode on the web, Opus 5.5 asked us what counts as one item and recommended pairs. We picked clients
and routes pooled, so its script gave the three route lines. On 31 Oct, with `claude -p` and nobody to answer, it chose
pairs on 2 of 2 runs and said so. So the same ask can give another answer when nobody settles the reading. Our step 11
ask stays as it was in this test, and the sharper ask is here.

## Next

The Expert level, steps 21 to 30, starts with guardrails.
