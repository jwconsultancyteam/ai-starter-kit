# Builder, step 18: From artifact link to a real website

In [step 17](../17-github-undo-button/), `weekly-shipments` stayed private. Now you want to show one result to
someone else: a client, a colleague, or your own phone. You do not make the repository public for that. You put one
page online.

Claude Code can do that in two ways, each from one sentence:

- **An artifact link.** Claude Code publishes the page on claude.ai. Only you can open it, until you share it.
- **GitHub Pages.** The page gets its own address on `github.io`, from a new public repository that holds only that
  page.

| | |
|---|---|
| Time | about 15 minutes |
| You need | Claude Code on a Pro, Max, Team or Enterprise plan, signed in with `/login` ([step 13](../13-claude-code-on-your-laptop/)), the `weekly-shipments` repository and the GitHub CLI from [step 17](../17-github-undo-button/) |
| Tested | an interactive Claude Code session on a Mac, in our `weekly-shipments` clone, accept edits mode, no personal settings loaded, Claude Max. Claude Code 2.1.312, 28 Oct 2026. Not in print mode: there, artifacts are off |
| Download | [index.html](index.html) (the page we put online), [publish-cheat-sheet.md](publish-cheat-sheet.md) and [the carousel as a PDF](builder-step18-artifact-to-website-carousel.pdf) (8 slides) |

## The two ways at a glance

| | Artifact link | GitHub Pages |
|---|---|---|
| Address | `claude.ai/artifact/...` | `https://<your-name>.github.io/<repository>/` |
| Who can open it | Only you, until you share it | Everyone on the internet |
| What you need | Pro or higher, signed in with `/login` | A GitHub account. On GitHub Free, the repository must be public |
| Our time, from the ask to a page that opens | 47 seconds | Under 3 minutes |
| How often it asked for a yes | Once: to run `python3 changes.py` | 7 times, before each `gh` and git command. One of them came from a git setting on our own computer |
| Limits | One page, 16 MiB at most | Public for everyone. GitHub logs the IP address of each visitor |

## Our test

Two asks, in one session, in the step 17 repository.

**Ask 1:** "Make a web page that shows the output of python3 changes.py, and publish it as an artifact."

- It asked once, before it ran `python3 changes.py`. We chose **1. Yes**.
- 47 seconds later it gave a `claude.ai/artifact/...` link, and said: "the link is private, so only you can open it
  for now. To show it to others, use the page's Share menu."
- The page shows the three lines of step 11, bars for the two weeks, the terminal output, and a note that the data is
  a made-up export of 198 shipments. We counted the rows: 198.

**Ask 2:** "Put this page online with GitHub Pages, in a new public repository called pallet-changes. Only the page
goes in it, not the script or the CSV."

- It asked before each `gh` and git command: 7 times. We chose **1. Yes** each time. One of the 7 came from a git
  setting on our own computer (see below).
- It made the public repository `pallet-changes`, with one file in it: `index.html`. We checked: the script and the
  CSV are not in it.
- Under 3 minutes after the ask, the page opened at `https://jwconsultancy1234.github.io/pallet-changes/`, with no
  sign-in. GitHub says it "can take up to 10 minutes".

### What we saw on the way

- **It typed the numbers into the page.** Claude said: "I copied the figures into the page by hand, so it won't
  update when the CSV changes." New data means: run the script again and publish again.
- **A failed build, and a page that worked.** During our test, GitHub listed two builds: one "Page build failed", one built. Claude
  said that the failed one was a duplicate that GitHub cancelled. The page opened all the same.
- **A new folder asks first.** The first time you start `claude` in a folder, it asks if you trust it. The cursor
  starts on **No, exit**. Choose **Yes, I trust this folder**.
- **Our branch is not your branch.** A git setting on our own computer blocks pushes to `main`. So Claude put the
  page on a branch called `gh-pages` and told us why. Without that setting, Claude can use `main`. Both work.

## Do it yourself

1. In the terminal, go to `weekly-shipments` and start `claude`. Press `Shift+Tab` until it says `accept edits on`.
2. Paste ask 1 from [our test](#our-test). When it wants to run `python3 changes.py`, choose **1. Yes**. Your browser
   opens the new page. Press `Ctrl+]` to open it again later.
3. Check the three lines on the page against step 11.
4. Paste ask 2. Read each command before you choose **1. Yes**. Wait until Claude says the page is live.
5. Open the `github.io` address on your phone.
6. Done showing it? Run `/artifacts` in Claude Code, select the page and press `d` to delete it. For GitHub Pages,
   delete the `pallet-changes` repository on github.com. We did not test the two deletes: our pages are still online.

Your page looks different from ours? Claude designs each page again. Check the numbers, not the look.

## Good to know

- **GitHub Pages is the quick way.** It shows something fast. For a product site, I point my own domain through DNS to
  Cloudflare Pages or my own server. GitHub Pages can use your own domain too: add a DNS record, and enter the domain
  under **Settings** > **Pages** in the repository. GitHub: it "supports using custom domains".
- **GitHub Pages is public.** GitHub: "GitHub Pages sites are publicly available on the internet, even if the
  repository for the site is private." Only put made-up or public data on it.
- **Never make `weekly-shipments` public to share one page.** On GitHub Free, a Pages site needs a public repository.
  Make a new one that holds only the page, as in ask 2.
- **Private is not a safe.** Never push keys, passwords or tokens, not even to a private repository. Keep them in a
  `.env` file: the [`.gitignore` template from step 17](../17-github-undo-button/gitignore.template) keeps `.env` out
  of git.
- **An artifact starts private.** Anthropic: "A new artifact is visible only to you." You share it from the
  **Share** control in the page header. On Team and Enterprise plans, public links are off until an owner turns them
  on.
- **A public artifact link needs no account.** Anthropic: anyone with the link can open it, "with no claude.ai sign-in
  required". That is different from a chat artifact in [step 6](../../starter/06-artifacts/), where everyone needs a
  Claude account. We shared our page this way, but we did not open it from a signed-out browser.
- **No link?** Artifacts need a claude.ai sign-in. Anthropic: "Sessions using an API key, gateway token, or
  cloud-provider credential cannot publish." They are also off when you run `claude -p`.
- **Deleting is for good.** In `/artifacts`, `d` "permanently deletes an artifact you own after you confirm. Its link
  stops working for everyone, including you."
- **GitHub logs visits.** GitHub: "When a GitHub Pages site is visited, the visitor's IP address is logged and stored
  for security purposes."

## Time win and solution win

- **Time win:** from the terminal output to a page on your phone in under 3 minutes, with no website builder.
- **Solution win:** you share one page, and your repository with the script and the data stays private.

## Common mistakes

| Mistake | Fix |
|---|---|
| You make your private repository public to share one page | Make a new repository with only the page in it, as in ask 2 |
| The page shows old numbers | Claude typed them in. Run the script again and ask Claude to publish again |
| Claude writes a local HTML file, but gives no link | Sign in with `/login`. An API key or `claude -p` cannot publish |
| The `github.io` address gives a 404 | Wait. It can take up to 10 minutes |
| You get an email about a failed Pages build | Open the address first. In our test, one build failed and the page still worked |
| Client names or real data on the page | Only made-up or public data on a page anyone can open |

## In our own work

Before this test, I had 24 artifacts in my claude.ai gallery: reports, plans and dashboards. None of my 31
repositories used GitHub Pages. We counted both on 28 Oct 2026. Now 1 of my 32 repositories does: `pallet-changes`, the
one from this test.

My other live websites run elsewhere, like Cloudflare Pages or my own server. I point my own domain to them through DNS.

## Next

Step 19 (Saturday): tests and security checks on every change.
