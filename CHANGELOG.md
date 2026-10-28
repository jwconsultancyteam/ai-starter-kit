# Changelog

What changed in the kit, newest first. Dates are Brussels time.

## 29 Oct 2026

- Builder, step 17: GitHub, your real undo button is live: five git words, commit every change, and undo one wrong
  change with `git revert` while a later change stays. Includes a git cheat sheet, a `.gitignore` template and the
  step 11 script and export. Tested on a Mac, Claude Code 2.1.312 and git 2.54, 28 Oct 2026, with no personal
  settings: a wrong change, a good change after it, then "Undo it", in a plain folder and in a git repository. Both
  undos gave the right output. Without git, Claude rebuilt the file by hand and said it "may not match your original
  exactly"; with git, it made a revert commit. It did not commit on its own, and accept edits mode still asked before
  `git commit`.

## 28 Oct 2026

- The main README now matches what the kit is: steps come at 08:00 (Brussels time) from step 15, the Builder steps
  from step 12 are tested in Claude Code on a Mac, the Starter steps need no GitHub account, and "What every step
  contains" is split into Starter and Builder. Step 17 has one name everywhere: GitHub, your real undo button. The
  step 16 wiki index template says its links are examples.
- Builder, step 16: A second brain is live: auto memory next to CLAUDE.md, and a wiki that Claude Code writes from
  your notes (Andrej Karpathy's LLM Wiki pattern), with a 19-line CLAUDE.md for the wiki, templates for the index and
  a page, 16 made-up client notes and a cheat sheet. Tested on a Mac, Claude Code 2.1.312, 28 Oct 2026, with no
  personal settings: one fact told in chat, then asked in a new session, in 4 setups. With auto memory on, the new
  session knew it (6 seconds); with auto memory off, it did not. In a wiki folder in manual mode, the save needed a yes
  and was lost. The wiki build took 72 seconds; with 16 notes, Claude found the right answers with and without it.

## 27 Oct 2026

- Builder, step 15: Plan mode and undo is live: the three modes to start with (manual, plan, accept edits) and
  Shift+Tab to switch, the ask screen and its three answers, and rewind with "Restore code and conversation". Includes
  a one-page cheat sheet. Tested on a Mac, Claude Code 2.1.310, 26 Oct 2026, with no personal settings: one task (add
  a column) in each mode. Manual and plan left the file unchanged (80 and 26 seconds), accept edits changed it right
  (31 seconds). Rewind put back a file edit, but did not undo a change made only by a shell command.

## 26 Oct 2026

- Builder, step 14: CLAUDE.md, the house rules for one folder is live: what goes in (what the folder is, rules you
  can check, a pointer to a context pack, Never lines), what stays out, a 15-line template, the Monday context pack and
  a blank one, and our /init output. Tested on 24 Oct 2026, Claude Code 2.1.310: the same question without and with a
  CLAUDE.md, two runs each (about 500 words and 65 to 87 seconds without; 111 to 149 words and 25 seconds with). One
  rule ("Start with a table") was ignored in both runs with the file. A concrete rule in a context pack was followed
  in one run.

## 25 Oct 2026

- Builder, step 13: Claude Code on your own laptop is live: the one-line install for Mac, Windows PowerShell and
  Windows CMD from Anthropic's setup page, `claude --version` as the check, the first start (sign-in and the trust
  question), Plan mode before the first question, and three read-only questions on the step 11 sample export with
  the right answers to check. Includes the Desktop app Code tab as the route with no terminal. Tested on a Mac,
  Claude Code 2.1.310, 24 Oct 2026: the install took 10 seconds, and the first answer missed one route because it
  had read only the first 5 lines. Windows: not tested.

## 24 Oct 2026

- Builder, step 12: What an agent is is live: the four parts (a goal, tools, a loop and a stop rule), a chat answer
  vs a workflow vs an agent, step 11 read as an agent, and a one-page agent brief with a fifth line for what the agent
  may never do. Includes the step 11 job as a filled-in brief. Tested in Claude Code on 23 Oct 2026: Plan mode first,
  it asked one question the brief left open, and the output matched step 11's expected output.

## 23 Oct 2026

- Builder, step 11: Claude Code on the web is live: the step 10 Monday report becomes a small script in your own
  repository, written by Claude Code on claude.ai/code in Plan mode, on its own branch, with the rule for "biggest
  change" written down and the output checked against a separate count. Includes how to make your first repository.
  Before any code, Claude Code asked what counts as one item; the kit says which answer gives the
  expected output. Recorded on claude.ai/code in Chrome, Max plan, 23 Oct 2026.

## 22 Oct 2026

- Starter, step 10: Scheduled tasks is live: the step 9 Monday report as a scheduled task in a project with the
  export, Weekly on Monday at 07:00, Automatically approve with "Do not send anything" in the instructions, one test
  run with Run now checked against the expected numbers, how to pause it, and what to check before you let it run.
  Recorded on claude.ai in a Chromium browser, Team plan, 21 Oct 2026.

## 21 Oct 2026

- Starter, step 9: Cowork is live: the same export first in Chat (one Excel file is a Chat job), then a weekly report
  task in Cowork with three outputs (Excel, a one-page PDF, an email draft), Manually approve and Allow once, and the
  expected numbers to check the result against. Recorded on claude.ai in a Chromium browser, Team plan, 19 Oct 2026.

## 20 Oct 2026

- Starter, step 8: Skills is live: upload a free skill (a follow-up email after a client call), what is in a
  SKILL.md, the same call notes before and after, and how to make your own. Recorded on claude.ai in a Chromium
  browser, Team plan, 19 Oct 2026.

## 19 Oct 2026, evening

- Steps 1 to 4: each step folder now has its carousel as a PDF to download, built from the step's tested screenshots
  and README. Steps 5 to 9 already had one, so every step now has a carousel.

## 19 Oct 2026

- Starter, step 7: Connectors is live: connect Google Calendar and test it on a separate calendar with four made-up
  meetings, the same question before and after, the connector's tools (it can also create, update and delete events)
  and how to keep changes on Needs approval, plus a connector safety checklist. Recorded on claude.ai in a Chromium
  browser, Team plan, 19 Oct 2026.
- Steps 5, 6 and 7: the carousel of each step is now in its folder as a PDF to download.

## 18 Oct 2026

- Starter, step 6: Artifacts is live: the same job twice in the Renewals project (an email with a table, then a
  one-page overview as an artifact), the prompt, and how sharing works per plan. Recorded on claude.ai in Chrome,
  Team plan, 16 Oct 2026.
- Starter, step 6: added a diagram, "Three readers: three copies, or one page?", with its Excalidraw source.

## 17 Oct 2026

- Starter, step 5: Chat, Cowork, Code is live: where the switch is, Chat or Cowork under the message box, which plans
  get what, and the one-page "which way for which job" table. Checked on claude.ai in Chrome, Team plan,
  16 Oct 2026.

## 16 Oct 2026

- Starter, step 4: Memory is live: where the switches are, the same question asked three times (memory off, after
  one normal chat, after "Remember this"), how to change or delete what Claude kept. Recorded on claude.ai in
  Chrome, Team plan, 15 Oct 2026.
- The road now follows the 30-day plan: 10 Starter steps, then Builder 11 to 20 and Expert 21 to 30. A new step
  every day, weekends included.

## 15 Oct 2026

- Starter, step 3: Which Claude for which job is live: the four models and the effort levels as the menu shows
  them, one question asked to Haiku 5.5, Sonnet 5.5 and Opus 5.5, screenshots. Recorded on claude.ai in Chrome, Team plan,
  14 Oct 2026.

## 14 Oct 2026

- Starter, step 2: Projects, Claude's own desk is live: project instructions, a sample price list (made-up clients),
  before and after screenshots. Recorded on claude.ai in Chrome, Team plan, 13 Oct 2026.

## 13 Oct 2026

- Starter, step 1: Instructions for Claude is live: template, John Doe example, before and after screenshots.
- The road: Projects ("Claude's own desk") is step 2, so it follows step 1 as the video and post promise. Which
  Claude for which job moves to step 3.
- License: CC BY 4.0.
