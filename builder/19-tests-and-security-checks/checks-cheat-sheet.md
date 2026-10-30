# Checks cheat sheet: test and scan every pull request

## Ask Claude Code

- "Add a test test_changes.py that fails if the three lines of python3 changes.py change. Add a GitHub Actions workflow
  that runs pytest and gitleaks on every pull request. Put it on a branch and open a pull request."
- "Merge this pull request. Then make the two checks required, so nothing can merge to main while a check is red."
- "On a new branch from main, change changes.py to rank by percent, not by pallets. Do not change the test. Open a
  pull request, wait for the checks and tell me the result. Do not merge."

Change the script name to your own.

## Does a red check block, or only warn?

| Repository | Required checks | A red check |
|---|---|---|
| Private, GitHub Free | Refused: "Upgrade to GitHub Pro or make this repository public to enable this feature." | Warns. The merge goes through |
| Public, GitHub Free | Works | Blocks: `Required status check "pytest" is failing.` |

Do not guess. Open a bad pull request and try to merge it.

## A key in a change

| Repository | What happened to our made-up key |
|---|---|
| Public | GitHub stopped the push: "Push cannot contain secrets" |
| Private, GitHub Free | The push went through, and gitleaks went red |

A red scan means the key already reached GitHub. Closing the pull request does not remove it. With a real key: change
the key at the service it belongs to.

## See it yourself

| You want | Command |
|---|---|
| The checks of a pull request | `gh pr checks <number>` |
| Can this pull request merge? | `gh pr view <number> --json mergeStateStatus` |
| Which checks are required | `gh api repos/<you>/<repository>/branches/main/protection` |

On a private repository on GitHub Free, the last command returns the upgrade message.

In our test, `mergeStateStatus` said `UNSTABLE` when a red check did not block, and `BLOCKED` when it did.

## Before you merge

- [ ] Both checks are green.
- [ ] Nobody changed a test just to make it green.
- [ ] You read the whole change, not only the file you asked about.
- [ ] No key, password or token in the change. Only made-up or public data in a public repository.

From step 19 of the AI Starter Kit. We tested this in Claude Code 2.1.314, 30 Oct 2026, on a personal GitHub Free
account. We did not test GitHub Pro.
