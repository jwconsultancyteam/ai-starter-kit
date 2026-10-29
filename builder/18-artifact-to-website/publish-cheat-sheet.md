# Publish cheat sheet: one page online

## Which way

| You want | Use | Who can open it |
|---|---|---|
| Show it to yourself, on another screen | Artifact link | Only you |
| Show it to a few people for a short time | Artifact link, shared from the **Share** control | The people you share it with |
| A page with its own address that stays up | GitHub Pages, in a new public repository | Everyone on the internet |

## Ask Claude Code

- "Make a web page that shows the output of python3 changes.py, and publish it as an artifact."
- "Put this page online with GitHub Pages, in a new public repository called pallet-changes. Only the page goes in
  it, not the script or the CSV."

Change the script name and the repository name to your own.

## Before you publish

- [ ] Only made-up or public data on the page. No client names, no prices, no keys.
- [ ] The numbers on the page match the script output.
- [ ] Your working repository stays private. The page goes in a new repository.

## Find it again, or take it down

| Artifact link | GitHub Pages |
|---|---|
| `Ctrl+]` opens the last one of this session | `https://<your-name>.github.io/<repository>/` |
| `/artifacts` lists all of them | The repository on github.com, then **Settings** > **Pages** |
| In `/artifacts`, `d` deletes it for good | Delete the repository on github.com |

From step 18 of the AI Starter Kit. We tested the two asks in Claude Code 2.1.312, 28 Oct 2026. The keys and the
take-down steps come from the Claude Code and GitHub docs. We did not run the deletes.
