# Builder, step 20: Other models with Pi

Pi is a coding agent, like Claude Code, that works with models from many companies. So you can try a cheaper model on
real work. The [step 19](../19-tests-and-security-checks/) test tells you if the work is right, whatever the model is
called.

We ran the step 11 task on 4 setups. On our first ask, Opus 5.5 missed our count and a cheap model hit it. Then we made
the ask sharper, and all 8 runs matched the count. The model was not the problem. Our ask was.

| | |
|---|---|
| Time | about 20 minutes (our estimate) |
| You need | a terminal ([step 13](../13-claude-code-on-your-laptop/)), an OpenRouter account with a little credit, and Python with pytest ([step 19](../19-tests-and-security-checks/)) |
| Tested | a Mac, Pi 0.86.0 and Claude Code 2.1.316, 31 Oct 2026, 2 runs per setup, 8 runs per ask. Each run started on a new copy of commit `3aafdba` of `weekly-shipments`: only a README and the made-up CSV. Pi ran with `pi -p`, a new settings folder and no extensions, in a macOS sandbox. Claude Code ran with `claude -p`, no personal settings, accept edits mode, and Python commands allowed. Other shell commands were refused in those runs |
| Download | [sharper-ask.txt](sharper-ask.txt) and [the carousel as a PDF](builder-step20-other-models-with-pi-carousel.pdf) (8 slides). You also use [shipments-export-sample.csv](../11-claude-code-on-the-web/shipments-export-sample.csv) from step 11 and [test_changes.py](../19-tests-and-security-checks/test_changes.py) from step 19 |

## Four words first

| Word | What it is |
|---|---|
| Pi | A coding agent for the terminal, from `earendil-works/pi`. It can use models from many companies |
| OpenRouter | One account and one API key for models from many companies. You pay per use |
| API key | A secret that lets a program spend your credit. Treat it like a password |
| Flash model | A company's cheaper, faster model. Here: DeepSeek V4.1 Flash and Qwen 3.8 Flash |

## Read this before you install Pi

Pi's README: "Pi does not include a built-in permission system for restricting filesystem, process, network, or
credential access. By default, it runs with the permissions of the user and process that launched it."

So Pi does not stop to ask, as Claude Code does in [step 15](../15-plan-mode-and-undo/). It can run any command that you
can run. Pi's README: "If you need stronger boundaries, containerize or sandbox Pi." We ran it in a macOS sandbox, on a
copy of the folder.

Use a new folder and made-up data only. Do not start Pi in a folder with your real work or your keys.

## Our test

The first ask is the step 11 task, word for word:

> Write a small Python script, changes.py, that reads shipments-export-sample.csv and prints the three biggest changes
> in pallets between the last week in the file and the week before. Count every client and every route, and rank by
> the size of the change, up or down. Use ISO weeks. Add a README that explains the rule and how to run it. Run it
> once on the sample file and show me the output.

**Two checks.** The right count is in step 11's [expected-output.md](../11-claude-code-on-the-web/expected-output.md):
route BE-BE +35, route NL-BE +24, route BE-FR -23. The step 19 test is stricter, because it also pins the format of
each line.

### The first ask

| Setup | Matched the count | Step 19 test | Time per run | Cost per run |
|---|---|---|---|---|
| Pi, DeepSeek V4.1 Flash | 2 of 2 | 0 of 2 | 27 and 57 seconds | under 1 cent |
| Pi, Qwen 3.8 Flash | 0 of 2 | 0 of 2 | 113 and 216 seconds | under 2 cents |
| Claude Code, Opus 5.5 | 0 of 2 | 0 of 2 | 64 and 65 seconds | 35 and 36 cents, as shown |
| Opus 5.5 plans, then Pi with DeepSeek builds | 0 of 2 | 0 of 2 | 76 and 84 seconds | 31 cents, as shown |

The other runs did not count wrong. They answered another question. "Count every client and every route" can be read two
ways. Opus 5.5 and Qwen counted client and route pairs:

```text
1. Alpha Retail (example), BE-NL: 33 -> 0 (-33)
2. Alpha Retail (example), NL-BE: 19 -> 49 (+30)
3. Delta Home (example), BE-FR: 24 -> 3 (-21)
```

DeepSeek counted each client and each route on its own, as our count does. With an Opus plan in front of it, DeepSeek
counted pairs too: the plan said pairs.

### The sharper ask

We added two sentences to the same task. This is [sharper-ask.txt](sharper-ask.txt):

> Count each client on its own and each route on its own, not client and route pairs. Print one header line, then the
> three changes, each line in exactly this format: 1. route  AA-BB    10 ->   20  +10

| Setup | Matched the count | Step 19 test | Time per run | Cost per run |
|---|---|---|---|---|
| Pi, DeepSeek V4.1 Flash | 2 of 2 | 2 of 2 | 44 and 47 seconds | under 1 cent |
| Pi, Qwen 3.8 Flash | 2 of 2 | 1 of 2 | 152 and 172 seconds | under 1 cent |
| Claude Code, Opus 5.5 | 2 of 2 | 2 of 2 | 48 and 67 seconds | 28 and 36 cents, as shown |
| Opus 5.5 plans, then Pi with DeepSeek builds | 2 of 2 | 2 of 2 | 75 and 95 seconds | 25 and 27 cents, as shown |

So 8 of 8 runs matched the count, and 7 of 8 passed the test. The one red test had the right numbers and different spacing. The test pins the exact format, so it goes red on that too.

**How we measured.** Time is the clock around the run. Cost for Pi is the cost in Pi's own output. Cost "as shown" is
the figure Claude Code reports, plus Pi's cost for the build. We ran Claude Code signed in with a plan, so that figure
is not a bill we paid. In the plan setup, Claude Code stayed in plan mode and wrote no files. Its answer went to Pi with
"Carry out this plan."

**Runs not in the tables.** One earlier Qwen run on the first ask hit our 4-minute limit, so we stopped it and ran it again. Two Claude Code runs failed before they started, from a mistake in our command, so we ran them again. No other run was left out.

**What this does not show.** Two runs of one small task. It does not rank these models. It shows that a test can judge
any of them, and that our ask mattered here.

## Do it yourself

Mac or Linux. We ran the same model and the same ask, with the extra flags in the Tested row. We did not run the short
command in step 4 in this form, and we did not test the install or the OpenRouter clicks.

1. Install Pi. Its README: "Pi requires Node.js 22.19 or newer. The macOS, Linux, and Windows installers can install it
   if needed."

   ```bash
   curl -fsSL https://pi.dev/install.sh | sh
   ```

2. Make an account on openrouter.ai, add a little credit and create an API key. Set a low credit limit on the key if
   you can. Then, in the terminal, paste the key after the first line. It does not show, and it does not go in your
   shell history:

   ```bash
   read -s OPENROUTER_API_KEY
   export OPENROUTER_API_KEY
   ```

3. Make a new folder and put three files in it: `shipments-export-sample.csv`, `test_changes.py` and `sharper-ask.txt`.

   ```bash
   mkdir ~/pi-test
   cd ~/pi-test
   ```

4. Run the ask. Pi does not ask before it runs a command:

   ```bash
   pi -p --model openrouter/deepseek/deepseek-v4.1-flash "$(cat sharper-ask.txt)"
   ```

5. Check it yourself. Do not take the agent's word for it:

   ```bash
   python3 changes.py
   python3 -m pytest test_changes.py
   ```

   You want these three lines, and `1 passed`:

   ```text
   1. route  BE-BE    25 ->   60  +35
   2. route  NL-BE    77 ->  101  +24
   3. route  BE-FR    71 ->   48  -23
   ```

6. Try the first ask too: use step 11's [task-prompt.txt](../11-claude-code-on-the-web/task-prompt.txt) in a second new
   folder. Look at which question your model answers. Models and prices change, and yours may read it another way.

## Good to know

- **Pi has no plan mode.** Pi's README: "Pi ships with powerful defaults but skips features like sub-agents and plan
  mode." In our test, plan and build were two runs.
- **Use an API key in Pi.** Anthropic's terms are not clear on a Claude subscription login in Pi, so we do not promise
  that it works. Our Pi runs used an OpenRouter key.
- **What OpenRouter stores.** Its page: "OpenRouter does not store your prompts or responses". There are exceptions on
  that page, and each model provider has its own policy. We did not check those policies, so we used made-up data only.
- **Model names and prices change.** We read them on 31 Oct 2026. Check them on openrouter.ai.
- **A pinned test goes red on format too.** That is why the sharper ask gives the exact line. If the numbers are right and
  only the spacing differs, ask for the exact format. Do not change the test to make it green.

## Time win and solution win

- **Time win:** the 16 runs in our tables each took under 4 minutes, on all 4 setups.
- **Solution win:** the test says if the work is right, so you can try a cheaper model without taking its word for it.

## Common mistakes

| Mistake | What to do |
|---|---|
| You run Pi in a folder with real work | Stop. Use a new folder and made-up data. Pi does not ask first |
| You paste your key into a file in the folder | Use step 2. A file in the folder can reach GitHub |
| The test is red and the numbers are right | Only the format differs. Ask for the exact format. Do not edit the test |
| The three lines name a client and a route | Your model counted pairs. Use the sharper ask |
| `pi: command not found` after the install | Open a new terminal. We did not test this |
| `No module named pytest` | Ask your agent to install it for this folder, as in step 19. We did not test this |

## In our own work

Step 11 ran on Claude Code on the web on 23 Oct, and its script gave the three route lines. The same ask gave pairs on
Opus 5.5 in Claude Code on 31 Oct, on 2 of 2 runs. So a task that worked once can read differently on another model. Our
step 11 ask stays as it was in this test, and the sharper ask is here.

## Next

The Expert level, steps 21 to 30, starts with guardrails.
