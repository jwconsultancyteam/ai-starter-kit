# Builder, step 15: Plan mode and undo

In [step 14](../14-claude-md-house-rules/), Claude Code only read the export. Now it changes a file. Before you let
it, decide two things: when it must ask you first, and how you undo a step.

The mode decides when it asks. Rewind undoes a step.

| | |
|---|---|
| Time | about 20 minutes |
| You need | Claude Code, as in [step 13](../13-claude-code-on-your-laptop/) |
| Tested | one task in three modes (manual, plan, accept edits), with no personal settings loaded, then the ask screens and rewind in a live session. Claude Code 2.1.310, Mac, 26 Oct 2026 |
| Download | [shipments-export-sample.csv](shipments-export-sample.csv), [modes-and-rewind-cheat-sheet.md](modes-and-rewind-cheat-sheet.md) and [the carousel as a PDF](builder-step15-plan-mode-and-undo-carousel.pdf) (8 slides) |

## The three modes to start with

Press `Shift+Tab` to switch the mode. The bottom line of the screen shows the mode you are in.

| Mode | What you see | What it does without asking |
|---|---|---|
| Manual | `⏸ manual mode on` | Reads only. It asks before it edits a file or runs a command |
| Plan | `⏸ plan mode on` | Reads, and writes a plan. It does not change your files |
| Accept edits | `⏵⏵ accept edits on` | Reads and edits files, and runs common file commands. It still asks before other commands |

Anthropic's words: in Manual mode, "Claude Code stops and asks you before most actions that edit files, run shell
commands, or reach the network". Plan mode "tells Claude to research and propose changes without making them"
([code.claude.com/docs/en/permission-modes](https://code.claude.com/docs/en/permission-modes)).

In our clean test, with no personal settings, Claude Code started in manual mode. If your settings start it in
another mode, `Shift+Tab` gets you to these three. More modes exist. Leave them for later.

## Our test

One task, the same in every run: **add a column `checked` with the value `no`** to the made-up export from step 11
(199 lines). One run per mode, in print mode (`claude -p`), with no personal settings loaded.

| | Manual | Plan | Accept edits |
|---|---|---|---|
| The file after | Unchanged | Unchanged | Changed, and right |
| Time | 80 seconds | 26 seconds | 31 seconds |
| Cost (API prices, as shown by Claude Code) | USD 0.44 | USD 0.27 | USD 0.39 |
| Blocked | 3 commands and 1 file write | Nothing | 3 commands |

In print mode there is nobody to answer "yes", so a question counts as a "no".

- **Manual** tried three commands and a file write. Each one needed a yes, so nothing changed: "every way of writing
  to it needs your permission, and none was granted."
- **Plan** read the file and wrote a plan: 199 lines, 7 columns, and Windows line endings on every line. "I've
  written the plan, but I haven't changed the CSV yet." It saved the plan in Claude Code's own folder,
  `~/.claude/plans/`, not in your folder.
- **Accept edits** made the change with two file edits, without asking. Its three shell commands were still blocked.
  New first line: `date,shipment_id,client,route,pallets,weight_kg,status,checked`.

**Plan mode saw the Windows line endings.** That matters. Manual mode offered us a one-line `sed` command to run
ourselves. We ran it on a copy: it put `,no` after the hidden line-end mark, so the status column broke. A plan
shows you the file before anything changes.

## The ask screen

In a live session (manual mode), Claude Code asked before each edit:

```text
Do you want to make this edit to shipments-export-sample.csv?
❯ 1. Yes
  2. Yes, and switch to accept edits (auto-approve file edits and common file commands) for this session (shift+tab)
  3. No

Esc to cancel · Tab to amend
```

- **1** allows this one edit.
- **2** allows this edit and switches the rest of the session to accept edits.
- **3** says no.

Shell commands get their own ask screen. We said no to one that would rewrite the whole file. The screen showed
`Interrupted · What should Claude do instead?`. We typed "Do it with your file edit tool, not a shell command."
It asked twice more, once for each edit, and we said yes.

## Rewind: undo a step

Press `Esc` twice when the input is empty, or type `/rewind`. You get a list of your messages. Pick the one to go
back to. Each entry shows what changed, for example `shipments-export-sample.csv +199 -199`.

Then choose what to restore:

```text
1. Restore code and conversation
2. Restore conversation
3. Restore code
4. Summarize from here
5. Summarize up to here
6. Never mind

⚠ Rewinding does not affect files edited manually or via bash.
```

**Choose 1, Restore code and conversation.** In our test, "Restore code" alone put the file back, but Claude still
remembered its edit. When we then asked for the same column with a `sed` command, it said: "The checked column is already in the file from my last edit". It
was not. Restore both, and Claude and your file agree again.

**Rewind does not undo a shell command.** In a new session we let Claude Code change the file with one `sed` command.
The rewind screen said "The code will be unchanged." and had no "Restore code" option. After the rewind, the file was
still changed. Anthropic: "A file that only Bash commands changed isn't tracked and stays as it is. To revert it, use
version control, such as Git." ([code.claude.com/docs/en/checkpointing](https://code.claude.com/docs/en/checkpointing))

## Do it yourself

1. Make a test folder with only [shipments-export-sample.csv](shipments-export-sample.csv). Keep a copy somewhere
   else.
2. Start `claude` in the folder. Press `Shift+Tab` until it says `plan mode on`.
3. Ask: "Add a column named checked with the value no on every row." Read the plan. Nothing changes yet.
4. Press `Shift+Tab` until it says `manual mode on`. Ask it to make the change. Answer `1. Yes` to each edit.
5. Open the file and check the new last column.
6. Press `Esc` twice, pick your last message and choose `Restore code and conversation`. Check that the file is back.

Your file looks different from ours? Our run took two edits. Yours may take another route. Check the file, not the
steps.

## Good to know

- **Plan first when a change touches a file you care about.** Plan mode cost us 26 seconds and changed nothing.
- **Rewind is a quick undo, not a backup.** Anthropic: checkpoints are "not a replacement for version control". Git
  comes in step 17.
- **Rewind does not track everything.** Not shell commands, not your own edits outside Claude Code, and not edits from
  other sessions ([docs](https://code.claude.com/docs/en/checkpointing)).
- **It keeps file snapshots for the last 100 checkpoints** of a session, and you can still `/rewind` after you resume a session.
- **Claude can make its own files.** In one shell test it left a `shipments-export-sample.csv.bak` backup in the
  folder. Look at the folder after a change, not only at the file.

## Time win and solution win

- **Time win:** in 26 seconds the plan showed the line endings, before anything changed.
- **Solution win:** you decide what runs. One key switches the mode. `Esc` twice opens the undo.

## Common mistakes

| Mistake | Fix |
|---|---|
| Option 2 on the first ask "to save time" | Start with 1. Switch to accept edits when you trust the job |
| "Restore code" only | Choose "Restore code and conversation", so Claude does not remember an edit that is gone |
| You count on rewind after a shell command | Rewind does not undo it. Keep a copy, or use Git (step 17) |
| You run a one-line command Claude suggests | Ask for a plan first. The `sed` line we got broke a column |
| You check only the file | Look at the whole folder. Claude can leave extra files |

## Next

Step 16 (Wednesday): a second brain.
