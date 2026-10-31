# Builder, step 19: Tests and security checks on every pull request

In [step 17](../17-github-undo-button/), `git revert` took a wrong change back, after it was already committed. A
test shows it earlier. A check runs on every pull request, and a red check tells you that something is wrong before
you merge.

But a red check does not always stop the merge. On GitHub Free, in a private repository, it blocks nothing. We saw that
in our own test.

| | |
|---|---|
| Time | about 20 minutes (our estimate) |
| You need | Claude Code ([step 13](../13-claude-code-on-your-laptop/)), the `weekly-shipments` repository and the GitHub CLI ([step 17](../17-github-undo-button/)) |
| Tested | an interactive Claude Code session on a Mac, in a new clone of our private `weekly-shipments`, accept edits mode, no personal Claude Code settings loaded, and pytest and gitleaks were already on our computer. A script answered the yes prompts, so in our run nobody read each one. Claude Code 2.1.314, a personal GitHub Free account, 30 Oct 2026 |
| Download | [test_changes.py](test_changes.py), [checks.yml](checks.yml) (goes in `.github/workflows/`), [checks-cheat-sheet.md](checks-cheat-sheet.md) and [the carousel as a PDF](builder-step19-tests-and-security-checks-carousel.pdf) (8 slides) |

## Six words first

| Word | What it is |
|---|---|
| Pull request | A proposed change on its own branch. You see it and its checks before it goes into `main` |
| Check | A job that GitHub Actions runs on the pull request. It ends green or red |
| Required check | A check that must be green before GitHub allows the merge |
| pytest | A program that runs your tests |
| gitleaks | A program that looks for keys in your files and history. This is the key scan |
| Push protection | A GitHub setting that refuses a push when it finds a key |

## The two ways at a glance

| | Private, GitHub Free | Public, GitHub Free |
|---|---|---|
| Checks run on every pull request | Yes | Yes |
| Make the checks required | Refused, HTTP 403 | Works |
| Merge with a red check | Went through | Refused, HTTP 405 |
| Merge with a red check and admin rights | Not needed: it merges without them | Refused, on a test pull request |
| Push a made-up key, one format | Went through, then gitleaks went red | Push protection was on: GitHub stopped the push |

## Our test

**Ask 1:** "Add a test test_changes.py that fails if the three lines of python3 changes.py change. Add a GitHub
Actions workflow that runs pytest and gitleaks on every pull request. Put it on a branch and open a pull request."

- It asked for a yes 7 times. Under 2 minutes after the ask, the pull request was open and pytest and gitleaks were
  both green.
- Claude said: "I didn't plant a fake secret to confirm gitleaks fails when it finds one, so that path is
  untested."
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

**Ask 4:** "Merge pull request 3 now, with the red check." It merged. So Claude took it back, on our ask,
with `git revert -m 1` on the merge, in a new pull request. Both checks were green. We asked it to merge that one too,
and the three lines were right again.

**The same bad change in a public copy.** We asked Claude to make a new public repository,
[weekly-shipments-public](https://github.com/JWconsultancy1234/weekly-shipments-public), with the same files and the
two checks required, with no exception for admins. The data is made up, so that is fine. Then the same percent change,
and a try to merge it. The GitHub API answered: `Required status check "pytest" is failing.` The `gh pr merge` command
said: "the base branch policy prohibits the merge". On a test pull request that
Claude opened in that copy, a merge with admin rights was refused as well. You can see
[the blocked pull request](https://github.com/JWconsultancy1234/weekly-shipments-public/pull/2).

**The key scan, with a made-up key.** We asked: "On a new branch from main, add a file config.py with one made-up
example API key in the format of a Stripe test key. Make it up, it must not be a real key. Open a pull request, wait
for the checks and tell me the result. Do not merge."

- The session was still working in the public copy, so it tried there first. GitHub stopped the push: "Push cannot
  contain secrets". The key never reached the public repository. Push protection was on for
  that repository, and we tried one key format. We did not check where that setting came from. GitHub offered a link to allow the key. We did
  not use it.
- We sent it to the private repository instead. The push went through, and gitleaks went red, pytest stayed green.
- The red check did not block there either: GitHub's merge status was `UNSTABLE`, not `BLOCKED`. We closed the pull
  request without merging, and deleted the branch.
- Claude said it plainly: "closing PR #5 won't remove the key from the private repo".
- Claude also said: "Other PRs only pick up the key if the branch merges, or if they're built on top of it." Our own
  test says otherwise. In a local test, without GitHub, the same scan went red on a later branch without the key while
  the key branch still existed. It was clean once that branch was deleted. So delete that branch too.

### What we saw on the way

- **The prompt suggested changing the test.** After the red check, the next suggestion in the prompt was: "update the
  test
  to the new output". Nobody sent it, and Claude left the test alone, as we asked. A red test goes green if you change the test. So when a pull request touches a test, read that
  change first.
- **It changed more than we asked.** "I updated the rule and sample output to match, even though you only named
  changes.py." The README was in the pull request too. Read the whole change.
- **Claude tested its own block.** In the public copy, it opened a test pull request with a broken test, and tried
  a normal merge and a merge with admin rights. That pull request stays visible, closed.
- **Our computer is not your computer.** A pre-push hook on our own computer blocks pushes from a local `main`. It
  stopped the first push to the new repository. Claude asked how to go on, and the script that answered our prompts picked the first option: skip the hook once, for
  that first push only. Nobody read that question. Read yours. You will not see
  this unless
  you have the same setting.

## Do it yourself

1. In the terminal, go to `weekly-shipments`. Run `git switch main`, then `git pull`. Start `claude`. Press `Shift+Tab` until it says `accept edits on`.
2. Paste ask 1. Read each command before you choose **1. Yes**. Do not choose the options that say "don't ask again" or "switch to auto mode". Choose **No** at anything you did not ask for: a write to
   another repository, a GitHub setting, a branch delete, a forced push. If you do not understand a prompt, choose
   **No** and paste: "What does this command do, and is it needed?" Expect long commands. In our run, Claude also changed
   `changes.py` and the CSV for a moment, to prove that the test fails, and put them back. If you are not sure, choose **No**
   and ask, then, in a second terminal in `weekly-shipments`, run `git status` before you go on. If Claude has not committed yet, you want to see only the new files it made. If it has, you see nothing to commit, which is fine too. If `changes.py` or the CSV
   shows as modified, paste: "Put changes.py and the CSV back as they are on main." Then check the three lines with
   `python3 changes.py`. We did not test that wording. If pytest or gitleaks is not on your computer, Claude may want to install
   it. Read that prompt too. The check on GitHub installs gitleaks itself, so you can say **No** to a local gitleaks install.
   We did not test this. Wait for two green checks. Then read the change: on GitHub, open the pull request and click **Files changed**.
3. Merge it: paste "Merge this pull request. Go back to main and pull." We did not test that wording. Then make a bad change as in ask 3, and see the check go red. Do not merge it. In a second terminal, go to
   `weekly-shipments` and run `gh pr view 3 --json mergeStateStatus`, with your own pull request number. In our test, `UNSTABLE` did not block and,
   with no exception for admins, `BLOCKED` blocked. `BLOCKED` alone does not tell you if an admin can still merge. Ask Claude to close the pull request and go back to `main`.
4. Optional, the key scan. Only after ask 1 is merged, and only with a made-up key. In a new session in your own folder, paste:
   "On a new branch from main, add a file config.py with one made-up example API key in the format of a Stripe test key. Make it up, it must not be a real key. Open a pull request, wait for the checks and tell me the result. Do not merge."
   Afterwards, paste: "Close that pull request without merging. Delete the branch on GitHub and on this computer. Go back to main." We did not test that wording. We also did not run this ask in a new session in the private
   repository: ours reached it through a follow-up ask.
5. Choose your rule for `main`:
   - **Stay private on GitHub Free.** The check shows red and blocks nothing. Your rule is: never merge on red. Nothing enforces that rule
     but you. Merged on red by accident? Paste, with your own number: "Undo the merge of pull request 3 with git revert, on a branch, in a pull request. Wait for the checks and tell me the result. Do not merge." Read that pull request. When both checks are green, merge it. Main keeps the wrong change until you do. If the red check was the key scan, a revert does not remove the key: change the key at the service first, and ask Claude for the options.
   - **Pay for a plan that has it.** GitHub lists protected branches for private repositories under GitHub Pro. After the
     upgrade, paste: "Make the two checks required, with no exception for admins, so nothing can merge to main while a
     check is red." On your own repository, you are the admin. We did not test this.
   - **Use a public copy,** only if the data is made up. It shows you the block. It does not protect your working
     repository. The email in your git settings shows in the commits you push, so this ask names the noreply address
     GitHub offers. Paste: "Make a new public repository called weekly-shipments-public with only the files committed on main here, in one new commit, with no old history. Never copy a .env file or anything else not committed on main. Use my GitHub noreply address for every commit in that repository. Show me the file list and the address before you push. The data is made up, so that is fine. Keep this repository private. In the new repository, make the two checks
     required, with no exception for admins, so nothing can merge to main while a check is red." Before you say yes, check that the list holds only made-up data and the address ends in users.noreply.github.com. Our ask did not say "one new commit", "noreply" or "committed on main". Claude chose one new commit. It copied the email
     from our git settings, which already held the noreply address. Yours may be your real email, so we added both here
     and did not test this wording. Then paste: "In weekly-shipments-public, on a new branch, with the same noreply address, change changes.py to rank by percent, not by pallets. Do not change the test. Open a pull request, wait for the checks, and then try to merge it. Tell me exactly what GitHub says." Expect a refusal. Claude
     stays in the public copy after this, so type `/exit` and start a new session in your own folder. We left our copy up.

**Looks different from ours?** Wait until the checks have ended, then read the state again. For another word or other
check names, paste what you see into Claude and ask what it means.

## Good to know

- **A check that nobody must obey only shows red.** GitHub's plans page lists protected branches for private
  repositories under GitHub Pro. On its pricing page, repository rules on Free are for public repositories only.
- **GitHub's own secret scanning does not help a private repository on Free, and a personal paid plan does not change that.** For private repositories, GitHub's page lists organization plans with Secret Protection and enterprise plans, not Pro. On public repositories it "runs
  automatically for free". This workflow runs gitleaks, and that worked in our
  private repository.
- **A red key scan means the key already reached GitHub.** Closing the pull request or deleting the branch does not
  remove it: GitHub still showed our commit afterwards. With a real key: change the key at the service it belongs to,
  first. If the key is only on a side branch, delete that branch, so later scans stop going red. Ask Claude which branch. If it
  is in `main`, do not delete `main`. Ask Claude for the options. We did not test that. In our run the log did not name the key or the file, so ask Claude to
  find it. The workflow scans the whole history. Claude warned that if the key merges, "every later PR will fail
  gitleaks, even after config.py is deleted, unless the key is removed from history or allowlisted". We did not test that.
- **This test pins today's output.** Any change to the three lines it checks goes red, wanted or not. If you wanted the new output, updating the test
  is right. Read that the new lines are the ones you wanted.
- **A `.gitignore` only keeps out the files it names.** The step 17 template names `.env` files. Our made-up key was in
  `config.py`.
- **A Claude review does not block by itself.** Anthropic says automated security reviews "should complement, not
  replace, your existing security practices and manual code reviews." `/security-review` is a review you ask for. On its
  Code Review service, Anthropic says a review "never approves or blocks the pull request". In our test, the merge block came
  from a required check, and the push block from push protection.
- **The check runs on pull requests.** A direct push to `main` does not start it. We did not test a direct push.
- **No exception for admins is about the merge.** GitHub says people with admin permissions "can manage branch
  protection rules". So an admin can still change the rule, and on your own repository, that is you. We did not test that.
- **Public means public.** A pull request stays visible, even after you close it. Never put real data in a public
  copy, and never a real key.
- **In an organization, the official gitleaks action needs a license key.** Its page says `GITLEAKS_LICENSE` is
  "required for organizations, not required for user accounts". Claude installed the gitleaks program in the workflow
  itself, so ours does not use that action.

## Time win and solution win

- **Time win:** in our test, every later pull request was checked in under a minute, with no person watching.
- **Solution win:** a pull request that fails the test or the scan shows up red, if you wait for the checks before you
  merge. And you know
  which of
  your repositories really block, and which only show red.

## Common mistakes

| Mistake | Fix |
|---|---|
| You think a red check stops the merge | Check it, without merging: open a red pull request and run `gh pr view <number> --json mergeStateStatus`. On GitHub Free, in a private repository, ours said `UNSTABLE` |
| You make your working repository public to get the block | Keep it private. A public copy with only made-up data shows you the block. It does not protect the working repository |
| A red test goes green because the test changed | Read every change to a test before you merge |
| Green means correct | A test only checks what it checks. Ours checks three lines, not the header. The scan only finds key formats it knows, so green does not prove there is no key |
| The downloaded test fails on your own script | It skips a header line, then expects the three lines of the step 17 `changes.py`. Use ask 1, so Claude writes the test for your script |
| `gitleaks` is red on your first pull request, and you added no key | It scans the whole history, so an old key counts. Ask Claude what it found. With a real key: change the key |
| pytest is not found | It was already on our computer. Ask Claude to install it for this folder. We did not test this |
| `pytest` crashes on your own computer | Ours did, from a plugin in our own Python. Claude used `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest`. The check on GitHub was fine |

## In our own work

Our own main repository runs five security scanners on pull requests: gitleaks, semgrep, bandit, pip-audit and zizmor.
New findings fail, for pip-audit only when a dependency file changed. Findings already in the baseline do not. That repository is private, on a paid GitHub Team plan, so a required check works there: it stops a normal merge. An admin
can still override it.

## Next

Step 20: other models with Pi.
