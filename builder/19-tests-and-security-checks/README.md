# Builder, step 19: Tests and security checks on every change

In [step 17](../17-github-undo-button/), `git revert` took a wrong change back, after it was already in. A test stops
it earlier. A check runs on every pull request, and a red check tells you that something is wrong before you merge.

But a red check does not always stop the merge. On GitHub Free, in a private repository, it only warns. We saw that
in our own test.

| | |
|---|---|
| Time | about 20 minutes |
| You need | Claude Code ([step 13](../13-claude-code-on-your-laptop/)), the `weekly-shipments` repository and the GitHub CLI ([step 17](../17-github-undo-button/)) |
| Tested | an interactive Claude Code session on a Mac, in a new clone of our private `weekly-shipments`, accept edits mode, no personal settings loaded. Claude Code 2.1.314, a personal GitHub Free account, 30 Oct 2026 |
| Download | [test_changes.py](test_changes.py), [checks.yml](checks.yml) (goes in `.github/workflows/`), [checks-cheat-sheet.md](checks-cheat-sheet.md) and [the carousel as a PDF](builder-step19-tests-and-security-checks-carousel.pdf) (8 slides) |

## Three words first

| Word | What it is |
|---|---|
| Pull request | A proposed change on its own branch. You see it and its checks before it goes into `main` |
| Check | A job that GitHub Actions runs on the pull request. It ends green or red |
| Required check | A check that must be green before GitHub allows the merge |

## The two ways at a glance

| | Private, GitHub Free | Public, GitHub Free |
|---|---|---|
| Checks run on every pull request | Yes | Yes |
| Make the checks required | Refused, HTTP 403 | Works |
| Merge with a red check | Went through | Refused, HTTP 405 |
| Merge with a red check and admin rights | Not needed: it merges without them | Refused, on a test pull request |
| Push a made-up key | Went through, then gitleaks went red | GitHub stopped the push |

## Our test

**Ask 1:** "Add a test test_changes.py that fails if the three lines of python3 changes.py change. Add a GitHub
Actions workflow that runs pytest and gitleaks on every pull request. Put it on a branch and open a pull request."

- It asked for a yes 7 times. Under 2 minutes after the ask, the pull request was open and pytest and gitleaks were
  both green.
- Claude said: "I didn't plant a fake secret to confirm gitleaks finds one, so that path is untested."
- Claude also said that a failing check would not stop a merge until the checks are required.

**Ask 2:** "Merge this pull request. Then make the two checks required, so nothing can merge to main while a check is
red."

- It merged. Then GitHub refused the second part, for branch protection and for rulesets, with the same answer:
  "Upgrade to GitHub Pro or make this repository public to enable this feature."
- Claude did not hide it: "GitHub refused the setting, so main is still unprotected."

**Ask 3:** "On a new branch from main, change changes.py to rank by percent, not by pallets. Do not change the test.
Open a pull request, wait for the checks and tell me the result. Do not merge."

- pytest went red: `'1. route  BE-BE                       25 ->   60  +140.0%' != '1. route  BE-BE    25 ->   60  +35'`.
- gitleaks stayed green.
- Claude said: "Nothing blocks this merge".

**Ask 4:** "Merge pull request 3 now, with the red check." It merged. So we took it back,
as in step 17, with `git revert` in a new pull request. Both checks were green, and the three lines were right again.

**The same bad change in a public copy.** We asked Claude to make a new public repository,
[weekly-shipments-public](https://github.com/JWconsultancy1234/weekly-shipments-public), with the same files and the
two checks required, with no exception for admins. The data is made up, so that is fine. Then the same percent change,
and a try to merge it. GitHub answered: `Required status check "pytest" is failing.` On a test pull request that
Claude opened in that copy, a merge with admin rights was refused as well. You can see
[the blocked pull request](https://github.com/JWconsultancy1234/weekly-shipments-public/pull/2).

**The key scan, with a made-up key.** We asked: "On a new branch from main, add a file config.py with one made-up
example API key in the format of a Stripe test key. Make it up, it must not be a real key. Open a pull request, wait
for the checks and tell me the result. Do not merge."

- The session was still working in the public copy, so it tried there first. GitHub stopped the push: "Push cannot
  contain secrets". The key never reached the public repository. GitHub offered a link to allow the key. We did
  not use it.
- We sent it to the private repository instead. The push went through, and gitleaks went red, pytest stayed green.
- The red check only warned there too: GitHub's merge status was `UNSTABLE`, not `BLOCKED`. We closed the pull request
  without merging.
- Claude said it plainly: "closing PR #5 won't remove the key from the private repo".

### What we saw on the way

- **Claude offered to change the test.** After the red check, the next suggestion in the prompt was: "update the test
  to the new output". A red test goes green if you change the test. So when a pull request touches a test, read that
  change first.
- **It changed more than we asked.** "I updated the rule and sample output to match, even though you only named
  changes.py." The README was in the pull request too. Read the whole change.
- **Claude tested its own block.** In the public copy, it opened a test pull request with a broken test, and tried
  a normal merge and a merge with admin rights. That pull request stays visible, closed. GitHub does not let you
  delete a pull request.
- **Our computer is not your computer.** A git setting on our own computer blocks pushes to `main`. It stopped the
  first push to the new repository. We allowed one exception, for that first push only. You will not see this unless
  you have the same setting.

## Do it yourself

1. In the terminal, go to `weekly-shipments` and start `claude`. Press `Shift+Tab` until it says `accept edits on`.
2. Paste ask 1. Read each command before you choose **1. Yes**. Wait for two green checks.
3. Merge it. Then make a bad change as in ask 3, and see the check go red. Do not merge it. Close it.
4. Choose your rule for `main`:
   - **Stay private on GitHub Free.** The check warns. Your rule is: never merge on red. Nothing enforces that rule
     but you.
   - **Pay for a plan that has it.** GitHub lists protected branches for private repositories under GitHub Pro. We did
     not test this.
   - **Use a public repository,** with only made-up or public data in it. Then make the checks required, as above.

## Good to know

- **A check that nobody must obey is only a warning.** GitHub's plans page lists protected branches for private
  repositories under GitHub Pro. On its pricing page, repository rules on Free are for public repositories only.
- **GitHub's own secret scanning does not help a private repository on Free.** On public repositories it "runs
  automatically for free". That is why this workflow runs gitleaks.
- **A red key scan means the key already reached GitHub.** Closing the pull request does not remove it. With a real
  key: change the key at the service it belongs to.
- **Claude's reviews advise. They do not block.** Anthropic says automated security reviews "should complement, not
  replace, your existing security practices and manual code reviews." `/security-review` is a review you ask for. The
  block comes from a required check.
- **Public means public.** A pull request stays visible, even after you close it. Never put real data in a public
  copy, and never a real key.
- **In an organization, the official gitleaks action needs a license key.** Its page says `GITLEAKS_LICENSE` is
  "required for organizations, not required for user accounts". Claude installed the gitleaks program in the workflow
  itself, so ours does not use that action.

## Time win and solution win

- **Time win:** one ask, and every later change gets checked in under a minute, with no person watching.
- **Solution win:** the wrong change shows up red before it is in, not after. And you know which of your repositories
  really block, and which only warn.

## Common mistakes

| Mistake | Fix |
|---|---|
| You think a red check stops the merge | Check it: try to merge a red pull request. On GitHub Free, in a private repository, it goes through |
| You make your working repository public to get the block | Make a separate public copy with only made-up data, as we did |
| A red test goes green because the test changed | Read every change to a test before you merge |
| Green means correct | A test only checks what it checks. Ours checks three lines, not the header |
| `pytest` crashes on your own computer | Ours did, from a plugin in our own Python. Claude used `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest`. The check on GitHub was fine |

## In our own work

Our own main repository runs five security scanners on pull requests: gitleaks, semgrep, bandit, pip-audit and zizmor.
Only new findings fail. And there, a required check is what stops the merge.

## Next

Step 20 (Sunday): one agent, any model.
