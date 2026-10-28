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
| Tested | the step 11 repository in a folder on a Mac: a wrong change, a good change after it, then one ask to undo the wrong one, with and without git. Then the "Do it yourself" steps on GitHub, in a new clone of our private repository. Print mode (`claude -p`), no personal settings loaded. Claude Code 2.1.312, git 2.54, 28 Oct 2026 |
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
  "Commit the change to changes.py.", accept edits mode still needed a yes before `git commit`. In print mode nobody can say yes
  ([step 15](../15-plan-mode-and-undo/)), so nothing was committed until we allowed git commands.
- **Its commits have your name, and a second line.** The commit was made under our own git name. At the end of the
  message, Claude Code added `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **In plan mode, it warned about a conflict before it changed anything.** We asked which git commands it would run.
  It proposed `git revert`, checked with a dry run that changed nothing, and said: "It will conflict." The `--top`
  change had touched the lines next to the percent code. In a new session we asked for the revert. It fixed the two
  places by hand and kept `--top`.
- **It chose `git revert` on its own.** In the last run we allowed every git command and only said "Undo it". It chose
  revert, not `git reset --hard`, which throws work away. That was one run. A public bug report says Claude Code ran
  `git reset --hard` and lost work that was not committed
  ([#34327](https://github.com/anthropics/claude-code/issues/34327)). So say "with git revert" when you ask for an undo.

## Do it yourself

We ran these steps on GitHub, with our own private `weekly-shipments` repository.

1. **Get the step 11 work into main.** On github.com, open `weekly-shipments`, then **Pull requests**. If the step 11
   pull request is still open, open it and click **Merge pull request**. No repository? Make one with
   [first-repository.md](../11-claude-code-on-the-web/first-repository.md) and upload [changes.py](changes.py) too.
2. **Sign in, then clone.** The repository is private, so git needs your GitHub sign-in. Install the
   [GitHub CLI](https://cli.github.com), type `gh auth login` and follow the prompts. When it asks if you want to
   authenticate Git with your GitHub credentials, say yes. Then go to the folder for your projects and type
   `git clone https://github.com/<your-name>/weekly-shipments.git`, then `cd weekly-shipments`. We were already signed
   in, so we did not see the prompts of `gh auth login`.
3. Run `python3 changes.py`. Check the three lines against the output above.
4. Start `claude`. Press `Shift+Tab` until it says `accept edits on`. Paste ask 1 from [our test](#our-test). When it
   wants to run `python3 changes.py`, say yes: that is how it checks its own work. Run `python3 changes.py` again:
   NL-BE is gone.
5. Say: "Commit this change." Say yes to each git command it asks for. Claude may first make a new branch, such as
   `rank-by-percent-change`. That is fine: your main branch stays as it was.
6. Paste ask 2. Commit it the same way.
7. Type `git log --oneline` in the terminal. You see one line per commit.
8. Say: "Ranking by percent was a mistake. Undo only that change with git revert and keep the --top option." Run
   `python3 changes.py`: the three lines are back. Run `python3 changes.py --top 5`: five lines.
9. Type `git push`. On a new branch, git stops and shows the command to use instead:
   `git push --set-upstream origin <your-branch>`. Type that. Your commits, the revert too, are now on GitHub, on that
   branch. To get them into main, open the pull request that GitHub suggests and merge it, as in step 1. We
   stopped before that merge.

### What we saw on GitHub

- **Without a sign-in, git asks for a username and a password.** Your GitHub password does not work there. GitHub:
  "Password-based authentication for Git has been removed"
  ([docs.github.com](https://docs.github.com/en/get-started/git-basics/about-remote-repositories)). With an empty
  sign-in, git said `Repository not found`, for a repository that does exist.
- **Claude made a branch before it committed,** in 2 of 2 runs. After the merge, `main` had a pull request in its
  history, and Claude said: "You were on `main`, so I branched first rather than committing there."
- **When it could not run the script, it committed a bug.** In one run, we did not allow `python3`. Claude said its
  `--top` change was "untested", and it was right: the script then printed 1 line instead of 3. With `python3`
  allowed, Claude ran the script and the change worked.
- **Check the commit code in `git log`.** Claude told us the revert was `fc99b44`. Then it changed that commit, so in
  `git log` it was `ca0e8cb`. In another run it said why: "I also amended the revert commit to add the
  Co-Authored-By line."

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
- **Private stays private.** Keep `weekly-shipments` private. Step 18 puts one page online from a separate repository, so this one stays private.
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
| `git clone` says `Repository not found` for your own repository | Git has no sign-in, so the private repository looks like it does not exist. Type `gh auth login`, then clone again |
| `git push` says the branch has no upstream branch | Type the command git shows: `git push --set-upstream origin <your-branch>` |
| You say no when Claude wants to run the script | Then it cannot check its work. Say yes to `python3 changes.py` |

## In our own work

One of our own repositories has 1,900+ commits on its main branch since 29 March 2026, and 1,900+ merged pull
requests. 4 of those commits are reverts. We counted them in its `git log` on 28 Oct 2026.

## Next

Step 18 (Friday): from an artifact link to a real website.
