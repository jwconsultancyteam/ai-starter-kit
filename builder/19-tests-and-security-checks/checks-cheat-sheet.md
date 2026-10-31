# Checks cheat sheet: test and scan every pull request

## Ask Claude Code

- "Add a test test_changes.py that fails if the three lines of python3 changes.py change. Add a GitHub Actions workflow
  that runs pytest and gitleaks on every pull request. Put it on a branch and open a pull request."
- "Merge this pull request. Then make the two checks required, so nothing can merge to main while a check is red."
- "On a new branch from main, change changes.py to rank by percent, not by pallets. Do not change the test. Open a
  pull request, wait for the checks and tell me the result. Do not merge."

- For a public copy, only with made-up data: "Make a new public repository called weekly-shipments-public with only the files committed on main here, in one new commit, with no old history. Never copy a .env file or anything else not committed on main. Use my GitHub noreply address for every commit in that repository. Show me the file list and the address before you push. The data is made up, so that is fine. Keep this repository private. In the new repository, make the
  two checks required, with no exception for admins, so nothing can merge to main while a check is red." Then, there:
  "In weekly-shipments-public, on a new branch, with the same noreply address, change changes.py to rank by percent, not by pallets. Do not change the test. Open a pull request, wait for the checks, and then try to merge it. Tell me exactly what GitHub says."
  Then type `/exit` and start a new session in your own folder. Claude stays in the public copy otherwise.
- For the key scan, only with a made-up key, in a new session in your own folder: "On a new branch from main, add a file config.py with one made-up example API key in the format of a Stripe test key. Make it up, it must not be a real key. Open a pull request, wait for the checks and tell me the result. Do not merge."
  Afterwards: "Close that pull request without merging. Delete the branch on GitHub and on this computer. Go back to main."
- Merged on red by accident? With your own number: "Undo the merge of pull request 3 with git revert, on a branch, in a pull request. Wait for the checks and tell me the result. Do not merge." Read that pull request. When both checks are green, merge it. Main keeps the wrong change until you do. If the red check was the key scan, a revert does not remove the key: change the key at the service first, and ask Claude for the options.

We did not test the "new commit", "committed on main", "noreply" and "Afterwards" wording. We did not run the key scan ask in a new session in
the private repository: ours reached it through a follow-up ask. Change the script name to your own.

## Does a red check block, or only show red?

| Repository | Required checks | A red check |
|---|---|---|
| Private, GitHub Free | Refused: "Upgrade to GitHub Pro or make this repository public to enable this feature." | Blocks nothing. The merge goes through |
| Public, GitHub Free | Works | Blocks. The API: `Required status check "pytest" is failing.` `gh pr merge`: "the base branch policy prohibits the merge" |

Do not guess. Open a bad pull request, do not merge it, and read `mergeStateStatus` below.

## A key in a change

| Repository | What happened to our made-up key |
|---|---|
| Public, push protection on | GitHub stopped the push: "Push cannot contain secrets" |
| Private, GitHub Free | The push went through, and gitleaks went red |

A red scan means the key already reached GitHub. Closing the pull request or deleting the branch does not remove it. With a real
key: change the key at the service it belongs to, first. If the key is only on a side branch, delete that branch, so later scans stop going red. Ask Claude which branch. If it
is in `main`, do not delete `main`. Ask Claude for the options. We did not test that. A `.gitignore` only keeps out the files it names.

## See it yourself

| You want | Command |
|---|---|
| The checks of a pull request | `gh pr checks <number>` |
| Can this pull request merge? | `gh pr view <number> --json mergeStateStatus` |
| Which checks are required | `gh api repos/<you>/<repository>/branches/main/protection` |

On a private repository on GitHub Free, the last command returns the upgrade message.

In our test, `mergeStateStatus` said `UNSTABLE` when a red check did not block, and `BLOCKED` when it did, with no
exception for admins. `BLOCKED` alone does not tell you if an admin can still merge.

## Before you merge

- [ ] Both checks are green.
- [ ] Nobody changed a test just to make it green.
- [ ] You read the whole change under **Files changed** on the pull request, not only the file you asked about.
- [ ] No key, password or token in the change. Only made-up or public data in a public repository.

From step 19 of the AI Starter Kit. We tested this in Claude Code 2.1.314, 30 Oct 2026, on a personal GitHub Free
account. We did not test GitHub Pro.
