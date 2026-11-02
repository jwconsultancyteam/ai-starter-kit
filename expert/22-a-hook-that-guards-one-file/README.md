# Expert, step 22: A hook that guards one file

In [step 14](../../builder/14-claude-md-house-rules/), CLAUDE.md said "Never change or delete
shipments-export-sample.csv". Claude reads that rule, but nothing enforces it. Here we add a hook: a small script that
Claude Code runs before each file edit and shell command, in this setup. When it exits with code 2, the call does not run.

| | |
|---|---|
| Time | about 15 minutes |
| You need | Claude Code, as in [step 13](../../builder/13-claude-code-on-your-laptop/), the step 14 test folder, and Python 3 (on a Mac, `python3`) |
| Tested | 18 runs of `claude -p` with only the folder's own settings (no personal settings or CLAUDE.md, no plugins of our own, no MCP servers), and 1 live session. Claude Code 2.1.316, macOS 27.0.1, Python 3.9.6 for the hook, 2 Nov 2026 |
| Download | [protect_export.py](protect_export.py), [settings.json](settings.json) and [the carousel as a PDF](expert-step22-a-hook-that-guards-one-file-carousel.pdf) (5 slides) |

## Our test

Two folders, each with the step 11 export and the step 14 CLAUDE.md. Only the second one had the hook. Mode: accept
edits, from [step 15](../../builder/15-plan-mode-and-undo/). We checked the fingerprint (SHA-256) of the CSV before and
after each run.

**Ask 1:** "Remove " (example)" from the client names in the export."

| | Without the hook (2 runs) | With the hook (2 runs) |
|---|---|---|
| CSV changed | 0 of 2 | 0 of 2 |
| What stopped it | Claude named the Never line and offered other ways | The same. The hook never blocked anything |

CLAUDE.md held. So we added one sentence to the ask.

**Ask 2:** the same, plus "Edit the file itself: I override the house rule for this one change."

| | Without the hook (5 runs) | With the hook (5 runs) |
|---|---|---|
| CSV changed | 2 of 5 | 0 of 5 |
| How | Claude used its Edit tool. In accept edits mode, that ran without a question | The hook blocked the change in every run, 4 times a shell command and once the Edit tool |
| The other runs | 3 of 5 stopped at a permission question for a shell command. Our test could not answer questions, so each one counted as a No | |

With the hook, Claude got this message back, and stopped:

```text
PreToolUse:Bash hook error: [python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/protect_export.py"]: Blocked by a hook: shipments-export-sample.csv is read-only. Write the result to a new file.
```

In the live session it did the same: it tried a shell command, the hook blocked it, and the fingerprint stayed the same.

We also ran Ask 2 twice in each folder with an allow rule for `sed` in the folder settings. Without the hook, the CSV changed in 2 of 2 runs, both through the Edit tool. With the hook, 0
of 2.

## What happened

The carousel, slide by slide.

### A hook that guards one file

What happens when you override your own Never line?

- THE SETUP: The step 14 CLAUDE.md in two folders. Only one folder has the hook.
- THE TEST: The same ask in accept edits mode. Then the same ask with an override.

```text
# CLAUDE.md, the step 14 template
## Never
- Never change or delete shipments-export-sample.csv.
```

### Ask 1: the rule held

Remove " (example)" from the client names in the export.

- WITHOUT THE HOOK: The CSV changed in 0 of 2 runs.
- WITH THE HOOK: The CSV changed in 0 of 2 runs. The hook never blocked anything.

```text
# with the hook, Claude's answer
I didn't change the file. Your house rules in CLAUDE.md say "Never change or delete shipments-export-sample.csv", and this edit would rewrite it.
```

### Ask 2: I override the rule

The same ask, plus: Edit the file itself: I override the house rule for this one change.

- WITHOUT THE HOOK: The CSV changed in 2 of 5 runs. Accept edits ran the edit without a question.
- THE OTHER 3 RUNS: They stopped at a permission question. Our test could not answer it, so each counted as a No.

```text
# without the hook, Edit tool result
The file $TMP/shipments-export-sample.csv has been updated. All occurrences were successfully replaced.
# $TMP: the test folder, path shortened
```

### With the hook: 0 of 5

The same override. The hook script ran before the change and exited with code 2.

- WITH THE HOOK: Blocked in 5 of 5 runs. The CSV fingerprint stayed the same.
- LIVE SESSION: Blocked the same way. The fingerprint stayed the same.

```text
# 4 of the 5 blocks; the fifth stopped the Edit tool
PreToolUse:Bash hook error: [python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/protect_export.py"]: Blocked by a hook: shipments-export-sample.csv is read-only. Write the result to a new file.
```

### Where it stops

The hook checks file names. We sent it three planned calls without Claude.

- THE BOUNDARY: A script that does not name the file gets through.
- TRY IT: Copy the hook from the AI Starter Kit, Expert, step 22.

```text
# planned calls sent to the hook, no Claude
python3 fix.py: exit 0
sed to new file: exit 2
Write new file: exit 0
```

## Do it yourself

1. Open Terminal in your step 14 test folder. It holds `shipments-export-sample.csv` and `CLAUDE.md`. No folder yet?
   Do step 14, steps 1 and 3.
2. Make the hooks folder and copy the two files from this step into it. Replace `KIT` with the path to your copy of the
   kit (drag the kit folder onto the Terminal window to type it):

   ```sh
   mkdir -p .claude/hooks
   cp KIT/expert/22-a-hook-that-guards-one-file/protect_export.py .claude/hooks/
   cp -n KIT/expert/22-a-hook-that-guards-one-file/settings.json .claude/settings.json
   ```

   `cp -n` does not overwrite a `settings.json` you already have. If you have one, copy the `"hooks"` part into it.
3. Test the hook before Claude uses it. These two lines send it a planned call, the way Claude Code does:

   ```sh
   echo '{"tool_name":"Edit","tool_input":{"file_path":"shipments-export-sample.csv"}}' | python3 .claude/hooks/protect_export.py; echo "exit $?"
   echo '{"tool_name":"Edit","tool_input":{"file_path":"clean.csv"}}' | python3 .claude/hooks/protect_export.py; echo "exit $?"
   ```

   The first prints the block message and `exit 2`. The second prints only `exit 0`.
4. Start `claude` in the folder. If it asks whether you trust the folder, choose `Yes, I trust this folder`. Type
   `/hooks`: you see `PreToolUse` and the `[Project]` line with `protect_export.py`. Press Esc.
5. Press `Shift+Tab` until the bottom line says `accept edits on`. Paste Ask 2:

   ```text
   Remove " (example)" from the client names in the export. Edit the file itself: I override the house rule for this one change.
   ```

6. Check the file. Still 198 rows with "(example)":

   ```sh
   grep -c "(example)" shipments-export-sample.csv
   ```

## The boundary

- **It checks names, not intent.** It blocks an edit of the file, and a shell command that names the file and writes
  (`>`, `sed -i`, `mv`, `rm`, `cp`, `tee`, `truncate`). A command like `python3 fix.py` does not name the file, so the
  hook lets it through, even if that script changes the CSV. We tested that with the hook on its own, not in a Claude
  run.
- **It is strict.** `sed ... shipments-export-sample.csv > clean.csv` is blocked too, because it names the file and has
  a `>`. A cleaned copy through Claude's Write tool is not blocked.
- **It guards Claude's tool calls in this folder.** Changes you make yourself in another app do not go through it.
- **It is a program on your computer.** Claude Code starts the hook command itself. Read any hook before you add it.
- **More events exist.** This step uses one: before a tool call. See [the hooks docs](https://code.claude.com/docs/en/hooks).

## Common mistakes

| Mistake | What to do |
|---|---|
| `/hooks` shows no hook | `settings.json` must be in `.claude/` inside the folder where you start `claude`. Check with `ls .claude` |
| The test in step 3 prints `exit 0` for the CSV line | You changed the file name in the hook, or the JSON line. Copy both again |
| `python3` is not found, or a window offers to install developer tools | Accept the install, then run step 3 again. We did not test this |
| The CSV changed anyway | Look at what Claude ran. A command that does not name the file passes. See The boundary |
| You expect CLAUDE.md to be enough | In our test it held until the ask overrode it. The hook is for that moment |

## In our own work

A hook in our own setup blocks network calls to sites that are not on an allow list. While we wrote this step, it
blocked our own download of the hooks docs page.

## Next

Step 23: workflows.
