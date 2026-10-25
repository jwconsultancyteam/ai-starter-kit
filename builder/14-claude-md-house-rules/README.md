# Builder, step 14: CLAUDE.md, the house rules for one folder

In [step 13](../13-claude-code-on-your-laptop/), Claude Code answered questions in a test folder. Every new session
starts from zero: it does not know what "this week" means to you, or what it may never touch.

CLAUDE.md fixes that. It is a plain text file in the folder. Claude Code reads it at the start of every session.

| | |
|---|---|
| Time | about 15 minutes |
| You need | Claude Code, as in [step 13](../13-claude-code-on-your-laptop/) |
| Tested | the same question in folders without and with a CLAUDE.md, two runs each, and one run with a context pack. Claude Code 2.1.310, 24 Oct 2026 |
| Download | [CLAUDE.md.template](CLAUDE.md.template), [monday-overview.md](monday-overview.md), [context-pack.template.md](context-pack.template.md), [what-not-to-put-in.md](what-not-to-put-in.md), [init-output-example.md](init-output-example.md), [shipments-export-sample.csv](shipments-export-sample.csv) and [the carousel as a PDF](builder-step14-claude-md-house-rules-carousel.pdf) (8 slides) |

The template is called `CLAUDE.md.template` on purpose. A file called `CLAUDE.md` in this kit would load each time you
start Claude Code in it. Rename it to `CLAUDE.md` in your own test folder.

## What goes in

| Part | Example from the template |
|---|---|
| What the folder is, in one or two lines | "A weekly shipments export from our transport planning. The data is made up." |
| Rules you can check | "BE-NL and NL-BE are two separate routes." |
| Where the rules for one job are | "For the Monday overview, follow monday-overview.md." |
| Never | "Never change or delete shipments-export-sample.csv." |

Anthropic says it plainly: Claude treats CLAUDE.md as "context, not enforced configuration". Write rules that are
"concrete enough to verify", and aim for "under 200 lines per CLAUDE.md file"
([code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)).

## Our test

One vague question, the same in every folder: **"Give me the Monday overview of this export."** Each folder had only
the made-up export from step 11, and nothing else that Claude Code loads.

| | Without CLAUDE.md (2 runs) | With a 17-line CLAUDE.md (2 runs) |
|---|---|---|
| Length | 545 and 507 words | 149 and 111 words |
| Time | 65 and 87 seconds | 25 and 25 seconds |
| Cost (API prices, as shown by Claude Code) | USD 0.31 and 0.37 | USD 0.20 and 0.20 |
| What came back | Two different reports: client tables, an 8-week trend, advice on clients and empty trips | A route table both times, with the same numbers and the weeks named |
| Route numbers | Right | Right: BE-BE +35, NL-BE +24, BE-FR -23, BE-NL -5 |

The 17-line test file had the Monday rules inside. In the kit template (15 lines) they moved to the context pack.

Without house rules, Claude Code picked its own answer, and the two runs did not look alike. With house rules, it
answered the question we meant.

**It did not follow every rule.** The rule said "Start with a table". Both runs put a sentence or a title first. That is
what "context, not enforced configuration" means in practice.

**Then we made the rule concrete.** We moved the Monday rules into their own file,
[monday-overview.md](monday-overview.md), with "Your first line is the table. No title or sentence before it." One
run: the table came first, biggest change first, then 3 lines. 98 words. This was one run, not proof.

The sample file did not change in any run. No run made a file.

## `/init` writes a start, not the rules

`/init` reads the folder and writes a CLAUDE.md for you. In our test folder it wrote 26 lines
([init-output-example.md](init-output-example.md)): a good description of the columns. But none of our house rules.
It cannot know that "this week" means the last full ISO week, or what Claude may never touch. Only you know that.

So: run `/init`, keep the two lines that say what the folder is, cut the rest, and add your own rules.

## Do it yourself

1. Make a test folder with only [shipments-export-sample.csv](shipments-export-sample.csv).
2. Ask Claude Code: "Give me the Monday overview of this export." Save the answer.
3. Download [CLAUDE.md.template](CLAUDE.md.template) and [monday-overview.md](monday-overview.md) into the folder.
   Rename the template to `CLAUDE.md`.
4. Start a new session (type `/clear` or start `claude` again). Ask the same question.
5. Compare the two answers. Then change one rule and ask again.

To check that it loaded, type `/context` in Claude Code. Your CLAUDE.md is in the list.

## Good to know

- **It also loads from the folders above.** Claude Code reads CLAUDE.md in your folder and in every folder above it.
  We found this the hard way: our first "without" test sat inside a folder that had a CLAUDE.md, and it loaded.
- **Short wins.** Every line is read in every session. A 2026 study of AGENTS.md and CLAUDE.md files found that
  instructions in them "are well followed", but that repository overviews "are not helpful", and that context files
  raised cost "by over 20% on average" ([arXiv 2602.11988](https://arxiv.org/abs/2602.11988)).
- **One job, one context pack.** Rules for one job go in their own file. CLAUDE.md gets one line that points to it.
  Template: [context-pack.template.md](context-pack.template.md).
- **It works in every folder.** Put a CLAUDE.md in each project folder. A personal one in `~/.claude/CLAUDE.md` applies
  to all your folders.
- **Already have an AGENTS.md?** Claude Code can read a repository's AGENTS.md too. See the
  [docs](https://code.claude.com/docs/en/memory).
- Never put passwords, API keys or client data in CLAUDE.md. More in [what-not-to-put-in.md](what-not-to-put-in.md).

## Time win and solution win

- **Time win:** no more explaining your rules at the start of each session. In our test the answer also came faster:
  about 25 seconds instead of 65 to 87.
- **Solution win:** the same question gives the same kind of answer, every session, for everyone who uses the folder.

## Common mistakes

| Mistake | Fix |
|---|---|
| A long CLAUDE.md "to be safe" | Aim for under 200 lines. Cut what Claude can read from the files itself |
| You keep the whole `/init` output | Keep the two lines that say what the folder is. Add your own rules |
| "Start with a table" | "Your first line is the table." Write it so anyone can check it |
| Rules for every job in one file | One context pack per job. One pointer line in CLAUDE.md |
| A Never line you rely on | CLAUDE.md can be ignored. Keep a Never line, and add a hard block later (Expert, step 21) |
| You test in a folder inside another project | A CLAUDE.md in a folder above also loads. Test in a clean folder |

## Next

Step 15 (Tuesday): Plan mode, permission modes and rewind. Make Claude Code ask before it changes, and undo a step.
