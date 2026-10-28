# Builder, step 17: GitHub, your real undo button

In [step 15](../15-plan-mode-and-undo/), rewind undid a file edit, but not a change made by a shell command. Anthropic
says it plainly: checkpoints are "not a replacement for version control". In [step 16](../16-second-brain/), we said
the same of memory: "Not a backup."

Git is that backup. Every commit is a saved version of your folder. GitHub keeps a copy of it online. And `git revert`
takes out one change, even a change from days ago, and keeps everything you did after it.

| | |
|---|---|
| Time | about 20 minutes |
| You need | Claude Code, as in [step 13](../13-claude-code-on-your-laptop/), and the `weekly-shipments` repository from [step 11](../11-claude-code-on-the-web/), or the two files in this folder |
| Tested | the step 11 repository in a folder on a Mac: a wrong change, a good change after it, then one ask to undo the wrong one, with and without git. Print mode (`claude -p`), no personal settings loaded. Claude Code 2.1.312, git 2.54, 28 Oct 2026 |
| Download | [changes.py](changes.py) and [shipments-export-sample.csv](shipments-export-sample.csv) (the step 11 script and export), [git-cheat-sheet.md](git-cheat-sheet.md), [gitignore.template](gitignore.template) and [the carousel as a PDF](builder-step17-github-undo-button-carousel.pdf) (8 slides) |

## Five words first

| Word | What it is |
|---|---|
| Repository | A folder that keeps every saved version of its files. Yours is `weekly-shipments` |
| Commit | One saved version, with a short message that says what changed |
| Clone | A copy of a GitHub repository on your own computer |
| Push | Send your new commits to GitHub |
| Revert | A new commit that takes out the change of one old commit. The old commit stays in the history |

## Our test

The step 11 script prints the three biggest changes in pallets. The right output, from
[expected-output.md](../11-claude-code-on-the-web/expected-output.md):

```text
route BE-BE: 25 -> 60 (+35)
route NL-BE: 77 -> 101 (+24)
route BE-FR: 71 -> 48 (-23)
```

Three asks, each in a new session, in accept edits mode:

1. **A wrong change:** "Change changes.py so it ranks the changes by percent instead of by pallets." Now NL-BE was
   gone from the top 3, and two small clients were in: Epsilon Garden (+122.2%) and Delta Home (-67.9%).
2. **A good change after it:** "Add an option --top N to changes.py so I can print more than three lines."
3. **The undo:** "The percent ranking was a mistake. Undo it."

We ran the three asks twice: once in a git repository, once in a plain folder with the same files. In the git
repository, we also asked Claude to commit after asks 1 and 2.

| | Plain folder | Git repository |
|---|---|---|
| What Claude said | "This folder has no git history or backup, so I couldn't restore the earlier version. I rebuilt it by hand, which means it may not match your original exactly." | "The change is saved as revert commit `e471b48` on `main`, so the percent version is still in the history." |
| The top 3 after the undo | Right | Right |
| `--top 5` after the undo | Works | Works |
| The rest of the folder | The README was 18 lines different from the original. The paragraph about Beta Foods was gone | Only the `--top` lines differ from the step 11 version. We checked with `git diff` |
| Can you see what changed? | No. There is no old version to compare with | Yes. `git log` lists every change, `git diff` shows every line |
| Time and cost (API prices, as shown by Claude Code) | 45 seconds, USD 0.20 | 40 seconds, USD 0.18 |

**Both answers were right.** The difference is what you can prove. In the plain folder, Claude rebuilt the file from
what it understood, and said so. In the git repository, it took the old lines back from the history.

### Four things we saw on the way

- **It did not commit on its own.** After the wrong change, the file was changed but not committed. When we asked
  "Commit the change", accept edits mode still asked before it ran `git commit`. In print mode there is nobody to say
  yes ([step 15](../15-plan-mode-and-undo/)), so nothing was committed until we allowed git commands.
- **Its commits have your name, and a second line.** The commit was made under our own git name. At the end of the
  message, Claude Code added `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **In plan mode, it warned about a conflict before it changed anything.** We asked which git commands it would run.
  It proposed `git revert`, checked with a dry run that changed nothing, and said: "It will conflict." The `--top`
  change had touched the lines next to the percent code. In a new session we asked for the revert. It fixed the two
  places by hand and kept `--top`.
- **It chose `git revert` on its own.** In the last run we allowed every git command and only said "Undo it". It chose
  revert, not `git reset --hard`, which throws work away. That was one run. In public bug reports, Claude Code has run
  `git reset --hard` and lost work that was not committed
  ([#34327](https://github.com/anthropics/claude-code/issues/34327)). So say "with git revert" when you ask for an undo.

## Do it yourself

1. **Get the step 11 work into main.** On github.com, open `weekly-shipments`, then **Pull requests**. If the step 11
   pull request is still open, open it and click **Merge pull request**. No repository? Make one with
   [first-repository.md](../11-claude-code-on-the-web/first-repository.md) and upload [changes.py](changes.py) too.
2. **Clone it.** In the terminal, go to the folder for your projects and type
   `git clone https://github.com/<your-name>/weekly-shipments.git`. Then `cd weekly-shipments`. The repository is
   private, so git needs your GitHub sign-in. We were already signed in with the GitHub CLI (`gh auth login`), so we
   did not test the sign-in screen.
3. Run `python3 changes.py`. Check the three lines against the output above.
4. Start `claude`. Press `Shift+Tab` until it says `accept edits on`. Paste ask 1 from [our test](#our-test). Run
   `python3 changes.py` again: NL-BE is gone.
5. Say: "Commit this change." When it asks before `git commit`, choose **1. Yes**.
6. Paste ask 2. Commit it the same way.
7. Type `git log --oneline` in the terminal. You see one line per commit.
8. Say: "Ranking by percent was a mistake. Undo only that change with git revert and keep the --top option." Run
   `python3 changes.py`: the three lines are back. Run `python3 changes.py --top 5`: five lines.
9. Type `git push`. Open the repository on github.com and click the commit count above the file list: the revert is
   there too.

Your commits look different from ours? Claude may write other messages or take another route. Check the output, not
the steps.

## Good to know

- **Commit before you let Claude make a big change.** Git can only bring back what was committed. A change that was
  never committed has no saved version.
- **Revert, not reset.** `git revert` adds a commit and keeps the history. `git reset --hard` and `git restore`
  "will discard uncommitted changes in your working directory" ([git-scm.com](https://git-scm.com/docs/git-revert)).
- **Rewind is for the last few minutes, git for every day after.** Anthropic: "Checkpoints are designed for quick,
  session-level recovery. For permanent version history and collaboration, continue using version control, such as
  Git" ([docs](https://code.claude.com/docs/en/checkpointing)). By default, Claude Code deletes the file snapshots of a session about 30 days after it last saved one.
- **Keep secrets out before the first commit.** Copy [gitignore.template](gitignore.template) into the folder as
  `.gitignore`, so git never saves your `.env` file. A key that reached GitHub must be replaced at the service it
  belongs to. Deleting the commit is not enough.
- **Private stays private.** Keep `weekly-shipments` private. Step 18 puts a page online without making it public.
- **Auto memory is not in your repository.** It lives in `~/.claude/projects/` on your own computer
  ([step 16](../16-second-brain/)), so git does not save it.
- **No terminal?** GitHub Desktop can clone, commit and revert: **History**, right-click a commit, **Revert Changes in
  Commit** ([docs.github.com](https://docs.github.com/en/desktop/managing-commits/reverting-a-commit-in-github-desktop)).
  We did not test it.

## Time win and solution win

- **Time win:** one sentence undid one change from an earlier session. 40 seconds, and the later change stayed.
- **Solution win:** every change is in the history, with its own line. You can see what Claude did, and take any of it
  back.

## Common mistakes

| Mistake | Fix |
|---|---|
| You ask "undo it" in a folder without git | Claude can only rebuild from what it remembers. Use git from the first day |
| You never commit | Ask "Commit this change" after every change you want to keep |
| You ask for an undo without saying how | Say "with git revert". Never allow `git reset --hard` |
| `git revert` stops with a conflict | That is normal when a later change touched the same lines. Ask Claude to fix the conflict and keep the later change |
| A `.env` file with keys is in your commits | Replace the key at the service first. Then add `.gitignore` |
| You made the repository public to share one page | Keep it private. Step 18 shows another way |

## In our own work

One of our own repositories has 1,900+ commits on its main branch since 29 March 2026, and 1,900+ merged pull
requests. 4 of those commits are reverts. We counted them in its `git log` on 28 Oct 2026.

## Next

Step 18 (Friday): from an artifact link to a real website.
