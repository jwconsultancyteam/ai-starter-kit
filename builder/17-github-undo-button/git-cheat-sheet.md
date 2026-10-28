# Git cheat sheet: save, see, undo

Type these in the terminal, inside your repository folder. Or ask Claude Code to run them and read what it asks
before you say yes.

## Every day

| You want to | Type | What happens |
|---|---|---|
| See what changed | `git status` | Lists the files that changed since the last commit |
| See the lines that changed | `git diff` | Shows each changed line: `-` old, `+` new |
| Save a version | `git add changes.py` then `git commit -m "What changed"` | One commit, with your message |
| Send it to GitHub | `git push` | Your new commits are now online too |
| Send a new branch to GitHub, the first time | `git push --set-upstream origin <branch>` | Git shows this command when a plain `git push` stops. After that, `git push` is enough |
| Get the latest from GitHub | `git pull` | Commits made on github.com come to your computer |
| See the history | `git log --oneline` | One line per commit, newest first |

## Undo

| The change is | Type | What happens |
|---|---|---|
| Committed, maybe days ago | `git revert <commit>` | A new commit takes the change out. Everything after it stays |
| Not committed, one file | `git restore changes.py` | The file goes back to the last commit. Your uncommitted change in that file is gone |
| Lost, after a reset | `git reflog` | Lists where your folder was, also commits no longer in `git log`. Ask Claude to help you get one back |

`<commit>` is the short code at the start of a line in `git log --oneline`, for example `a39580d`.

## Ask Claude Code

- "Commit this change."
- "Undo only the change of commit a39580d with git revert. Keep everything after it."
- "Show me the git commands first. Do not run them yet." (plan mode)

## Never

- `git reset --hard`: it throws away every change you did not commit.
- `git push --force`: it can overwrite commits on GitHub.
- A `.env` file or a key in a commit. Use [gitignore.template](gitignore.template).

From step 17 of the AI Starter Kit. Tested with git 2.54 and Claude Code 2.1.312, 28 Oct 2026.
