# Builder, step 16: A second brain

In [step 14](../14-claude-md-house-rules/), you wrote the house rules for a folder. In [step 15](../15-plan-mode-and-undo/),
you decided when Claude Code must ask first. But every new session still starts empty. What you told Claude yesterday
is gone, unless it was saved somewhere.

A second brain is that somewhere. Claude Code has one built in, auto memory. For many notes, you can add a wiki that
Claude writes and keeps up to date.

| | |
|---|---|
| Time | about 25 minutes |
| You need | Claude Code, as in [step 13](../13-claude-code-on-your-laptop/) |
| Tested | one fact told in chat, then asked in a new session, in 4 setups. Then a wiki built from 16 made-up client notes, and two questions with and without it, two runs each. Print mode (`claude -p`), no personal settings loaded. Claude Code 2.1.312, Mac, 28 Oct 2026 |
| Download | [notes/](notes/) (16 made-up client notes), [CLAUDE.md.template](CLAUDE.md.template), [wiki-index.template.md](wiki-index.template.md), [wiki-page.template.md](wiki-page.template.md), [memory-and-wiki-cheat-sheet.md](memory-and-wiki-cheat-sheet.md) and [the carousel as a PDF](builder-step16-second-brain-carousel.pdf) (8 slides) |

## Two kinds of memory

| | CLAUDE.md | Auto memory |
|---|---|---|
| Who writes it | You | Claude |
| What is in it | Your rules | What Claude learned: your corrections, your preferences, facts you told it |
| Where | In your folder | `~/.claude/projects/<project>/memory/`, only on your own computer |
| What loads | The whole file, every session | The first 200 lines or 25KB of `MEMORY.md`, every session |

Anthropic's words: auto memory is "notes Claude writes itself based on your corrections and preferences". It "is on by
default in local sessions". `MEMORY.md` is the index: "one line per memory, loaded into every session". The details
go in topic files, which Claude reads "on demand" ([code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)).

## Test 1: tell it once, ask in a new session

Session 1: **"Remember this for later: Sarah at Example Logistics wants every invoice in Dutch, and sent to
finance@example.com, not to her."** Session 2, a new session in the same folder: **"Who gets the Example Logistics
invoice, and in which language?"** The fact was in no file.

| Setup | Session 1 | Session 2 |
|---|---|---|
| Plain folder, auto memory on | "I've saved it to memory." It did not ask | Right: finance@example.com, in Dutch. 6 seconds, USD 0.04 |
| Plain folder, auto memory off | "the note will be gone once the conversation ends" | Did not know |
| Wiki folder, manual mode, nobody said yes | Wanted to write it in the wiki. The edit needed a yes | Did not know |
| Wiki folder, accept edits | Wrote it in the wiki, with the source "told by you in chat" | Right. 8 seconds, USD 0.09 |

Costs are API prices, as shown by Claude Code.

What Claude saved in the first setup: one line in `MEMORY.md`, and a topic file with the fact, "Why" and "How to
apply". Plain markdown. You can read it, change it or delete it.

**Two things we did not expect.**

- **In the wiki folder, auto memory stayed empty.** Our `CLAUDE.md` makes the wiki the knowledge base, so Claude put
  the fact there and not in its own memory. Your house rules decide where it remembers.
- **A "remember this" can be lost in manual mode.** The wiki edit needed a yes ([step 15](../15-plan-mode-and-undo/)).
  Nobody said yes, so nothing was saved, and the next session did not know. Read what Claude says after "remember
  this". If it asks, say yes.

## Test 2: a wiki that Claude writes

The idea is Andrej Karpathy's ["LLM Wiki"](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (4 Apr
2026). Three layers:

- **Raw sources:** your notes. In Karpathy's words, "the LLM reads from them but never modifies them".
- **The wiki:** markdown pages that Claude writes. When it answers a question, it "reads the index first to find
  relevant pages". A `log.md` keeps every change.
- **The schema:** a `CLAUDE.md` with the rules. Ours: [CLAUDE.md.template](CLAUDE.md.template) (19 lines).

We gave Claude Code 16 made-up client notes ([notes/](notes/)). One client's price changed: EUR 1,850 agreed on 3 Sep,
EUR 1,950 from 1 Nov after a call on 8 Oct. There is also a proposal of EUR 1,900 that was not accepted, and a draft of
EUR 1,790 that was never sent.

**The build.** "Build the wiki from all notes in notes/." In accept edits mode: 72 seconds, USD 0.37, one time. It wrote
9 files: a page per client, 3 topic pages, `index.md` and `log.md`. It put EUR 1,850 until 31 Oct and EUR 1,950 from
1 Nov under "Current state", the old pallet limit under "History", and the EUR 1,900 and EUR 1,790 offers under "Not
agreed". The 16 notes did not change.

**The questions.** Two runs each, with and without the wiki:

| Question | Without a wiki | With the wiki |
|---|---|---|
| "What price did we agree with Example Logistics?" | Right both times. 22 and 10 seconds, USD 0.11 | Right both times. 6 and 9 seconds, USD 0.10 |
| "Which fixed-price clients have no October check in our notes?" | Right both times: Alpha Retail. 18 and 16 seconds, USD 0.12 | Right both times. 12 and 10 seconds, USD 0.13 and 0.14 |

**The honest result: with 16 notes, you do not need a wiki yet.** Claude Code searched the notes and found the right
answer every time. The wiki was a few seconds faster. Karpathy says the pattern "works surprisingly well at moderate
scale (~100 sources, ~hundreds of pages)". Start with auto memory. Add the wiki when your notes grow.

## Do it yourself

1. Make a test folder. Copy [notes/](notes/) into it.
2. Start `claude` in the folder. Type `/memory` and check that auto memory is on.
3. Say: "Remember this: Sarah at Example Logistics wants every invoice in Dutch." Read the answer.
4. Type `/clear` for a new session. Ask: "In which language does Example Logistics get its invoice?"
5. Type `/memory` and open the auto memory folder. Read what Claude saved.
6. For the wiki: copy [CLAUDE.md.template](CLAUDE.md.template) into the folder as `CLAUDE.md`. Press `Shift+Tab` to
   accept edits. Say: "Build the wiki from all notes in notes/."
7. Open `wiki/clients/example-logistics.md`. Check the price under "Current state" against the notes.

Your wiki looks different from ours? Claude may choose other topic pages. Check the facts, not the page names.

## Good to know

- **Auto memory is per project and per computer.** All folders in one git repository share one memory. Anthropic: "Files
  are not shared across machines or cloud environments" ([docs](https://code.claude.com/docs/en/memory)).
- **Keep `MEMORY.md` short.** Only the first 200 lines or 25KB load. Ours has 106 lines (17KB). Its folder has 258
  topic files.
- **A date does not retire an old fact.** In our own vault in August, almost every note had a date, but none said which
  older note it replaced. Two versions of one fact loaded into the same session. Hence the rule in the template: one
  "Current state", and the old value moves to "History".
- **Never put passwords, API keys or client data in memory or the wiki.** Both are plain text files.
- **Not a backup.** Memory and the wiki are files on your computer. Git comes in step 17.

## Time win and solution win

- **Time win:** say a fact once. In our test, the next session answered in 6 seconds, without asking again.
- **Solution win:** your knowledge stays in plain files you can read and fix: a memory index for what you tell Claude,
  a wiki for what is in your notes.

## Common mistakes

| Mistake | Fix |
|---|---|
| "Remember this" in manual mode, and you do not read the answer | If Claude asks to write, say yes. Then check with `/memory` |
| A wiki for 10 notes | Not needed yet. Claude can search 16 notes. Start a wiki when your notes grow |
| New facts added next to the old ones | One "Current state" per page. The old value moves to "History" |
| A draft offer read as a deal | Put "not sent" in the note. The template puts it under "Not agreed" |
| You never look at what it saved | Open `/memory` once a week. Delete what is wrong |

## Next

Step 17 (Thursday): GitHub, your real undo button.
