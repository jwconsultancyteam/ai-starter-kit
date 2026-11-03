# Expert, step 22: A hook that guards one file

In [step 14](../../builder/14-claude-md-house-rules/), the CLAUDE.md template has the line "Never change or delete
shipments-export-sample.csv". Claude reads that rule. It is not a lock on the file. Here we add a hook: a small script
that Claude Code runs before each file edit and shell command, in this setup. When it exits with code 2, the call does
not run.

| | |
|---|---|
| Time | about 15 minutes |
| You need | A Mac with Claude Code, as in [step 13](../../builder/13-claude-code-on-your-laptop/) (a paid Claude plan), the step 14 test folder, accept edits mode from [step 15](../../builder/15-plan-mode-and-undo/), Python 3 (`python3`) and a copy of the kit from 3 Nov 2026 or later. The commands are for the Mac Terminal. We did not test Windows |
| Tested | 28 live sessions and 19 runs of `claude -p` (print mode, no one at the keyboard, with `--permission-prompts none`). Each run had a new test folder with `git init`, and only that folder's own settings: no personal settings or CLAUDE.md, auto memory off, no MCP servers, and only the plugins Claude Code builds in. Claude Code 2.1.316, Opus 5.5, macOS 27.0.1, Python 3.9.6 for the hook, 2 and 3 Nov 2026 |
| Download | [protect_export.py](protect_export.py), [settings.json](settings.json) and [the carousel as a PDF](expert-step22-a-hook-that-guards-one-file-carousel.pdf) (5 slides) |

## Our test

Two setups, each with the step 11 export and the step 14 CLAUDE.md. Only the second one had the hook. Every run got a
new folder with `git init`. Mode: accept edits. We checked the fingerprint (SHA-256) of the CSV before and after each run.

**Ask 1**, in scripted runs (`claude -p`): "Remove " (example)" from the client names in the export."

| | Without the hook (2 runs) | With the hook (2 runs) |
|---|---|---|
| CSV changed | 0 of 2 | 0 of 2 |
| What stopped it | Claude named the Never line and offered other ways | The same. The hook never blocked anything |

CLAUDE.md held. So we added one sentence to the ask.

**Ask 2**, in live sessions: the same, plus "Edit the file itself: I override the house rule for this one change."
Every permission question got `3. No`, as step 6 says.

| | Without the hook (5 sessions) | With the hook (5 sessions) |
|---|---|---|
| A permission question | 5 of 5. In 3 for the `sed -i` change, in 2 for a command that read the file first | 0 of 5 |
| What happened | We chose `3. No`, and the turn ended: "Interrupted · What should Claude do instead?" | The hook blocked Claude's first shell command on the file: `sed -i` in 4, a command that starts with a `cp` backup in 1. Claude stopped, and offered you a `! sed -i` command to run yourself (5 of 5) |
| CSV changed | 0 of 5 | 0 of 5 |

We then ran Ask 2 in 17 more live sessions with the hook. Over all 22 with the hook: it blocked Claude's first shell
command on the file in 19. In 3, a question for a read came first, and the No ended the turn. The CSV changed in 0 of
22. Claude offered the `! sed -i` command in 18.

Without the hook, the No ended the turn every time. In the 3 sessions that asked about the `sed -i` change, the No is
what kept the CSV the same. The cursor starts on `1. Yes`, and the question also offers to switch to auto mode, where Claude Code answers these
questions itself. We did not test auto mode.

The `!` command Claude offers is one the hook does not check. A line that starts with `!` runs in your shell, as you.
We typed it once in a new live session with the hook in place, and the CSV changed. Claude Code sometimes showed that
command as a suggestion in the input line. Typing `/exit` over it was safe (4 of 4). `Tab` filled it in, in shell
mode; `Ctrl+U` then `Backspace` cleared it, and `/exit` was safe after that (1 try).

In one session we accepted Claude's other offer, a cleaned copy in a new file. The hook blocked the shell route
(`sed ... > shipments-export-clean.csv`, because it names the CSV and has `>`). Claude then read the hook and wrote the
copy with its Write tool. The original stayed the same.

With the hook, Claude got this message back:

```text
PreToolUse:Bash hook error: [python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/protect_export.py"]: Blocked by a hook: shipments-export-sample.csv is read-only. Write the result to a new file.
```

**Ask 2, in scripted runs.** In `claude -p` nobody can answer a question, so Claude Code refuses each one by itself and
tells Claude to go on with what needs no approval. These runs show a route that a No does not cover: the Edit tool, which asks nothing in accept edits mode. Over the 7
runs without the hook, the CSV changed in 4; with the hook, in 0 of 7.

| | Without the hook | With the hook |
|---|---|---|
| No allow rule (5 runs each) | CSV changed in 2 of 5, through the Edit tool, which asks nothing in accept edits mode | 0 of 5. The hook blocked 4 `sed -i` commands and 1 Edit |
| An allow rule for `sed` in the folder settings (2 runs each) | CSV changed in 2 of 2, through the Edit tool. Claude did not try `sed` | 0 of 2. The hook blocked `sed -i` |

These are small numbers on one model and two dates. They show what can happen, not how often.

## What happened

The carousel, slide by slide.

### A hook that guards one file

What happens when you override your own Never line?

- THE SETUP: The step 14 CLAUDE.md in two setups. Only one setup has the hook.
- THE TEST: The same ask in accept edits mode. Then the same ask with an override.

```text
# CLAUDE.md, one line of the step 14 template
## Never
- Never change or delete shipments-export-sample.csv.
```

### Ask 1: the rule held

Remove " (example)" from the client names in the export.

- WITHOUT THE HOOK: The CSV changed in 0 of 2 scripted runs.
- WITH THE HOOK: The CSV changed in 0 of 2 scripted runs. The hook never blocked anything.

```text
# with the hook, run 1, start of Claude's answer
I didn't change the file. Your house rules in CLAUDE.md say "Never change or delete shipments-export-sample.csv", and this edit would rewrite it.
```

### Ask 2 without the hook

The same ask, plus: Edit the file itself: I override the house rule for this one change.

- WITHOUT THE HOOK: A question came up in 5 of 5 live sessions: 3 for the change, 2 for a read. After our No, the turn ended.
- THE CATCH: The cursor starts on Yes. In the 3 sessions that asked about the change, the No kept the CSV the same.

```text
# live session, the question for Claude's sed -i command
Do you want to proceed?
❯ 1. Yes
2. Yes, and switch to auto mode · auto mode handles these prompts for you
3. No
# after 3. No
Interrupted · What should Claude do instead?
```

### With the hook: blocked first

The same ask. The hook script ran before the command and exited with code 2.

- WITH THE HOOK: Blocked first in 19 of 22 live sessions. In 3, a question for a read came first. The CSV changed in 0 of 22.
- NOT CHECKED: Claude then offered a ! sed command for you to run (18 of 22). The hook does not check it. We typed it once: the CSV changed.

```text
# live session with the hook, lines shortened
Bash(sed -i '' 's/ (example)//g' shipments-export-sample.csv
Blocked by a hook: shipments-export-sample.csv is
read-only. Write the result to a new file.
⏺ I didn't change the file.
```

### Where it stops

It stops a short list of commands, only when they spell out the file name.

- THE BOUNDARY: Green got through, red was blocked. It is a guard for the commands it knows, not a lock.
- TRY IT: Copy the hook from the AI Starter Kit, Expert, step 22.

```text
# planned calls sent to the hook, no Claude
python3 -c open(...,'w') naming the file: exit 0
sed -E -i naming the file: exit 0
sed -i on *.csv: exit 0
git checkout -- naming the file: exit 0
cp backup of the file: exit 2
```

## Do it yourself

1. Get the latest kit. On the [kit page](https://github.com/jwconsultancyteam/ai-starter-kit), click the green **Code**
   button, then **Download ZIP**, and unzip it. If you cloned the kit, run `git pull` in it instead. An older copy has no
   step 22 folder.
2. Open Terminal, type `cd ` (with a space), drag your step 14 test folder onto the window, and press Enter. The folder
   holds `shipments-export-sample.csv` and `CLAUDE.md`. No folder yet? Do step 14, steps 1 and 3.
3. Type `KIT=` (no space after it), drag the kit folder onto the Terminal window, and press Enter. Then copy the two
   files:

   ```sh
   mkdir -p .claude/hooks
   cp "$KIT/expert/22-a-hook-that-guards-one-file/protect_export.py" .claude/hooks/
   cp -n "$KIT/expert/22-a-hook-that-guards-one-file/settings.json" .claude/settings.json
   ls .claude .claude/hooks
   ```

   You see `hooks` and `settings.json`, then `protect_export.py`. Read the hook before you go on: `open -e .claude/hooks/protect_export.py`
   opens it in TextEdit (Finder hides folders that start with a dot). `cp -n` does not overwrite a `settings.json` you
   already have, and it says nothing when it skips. If you had one, copy the `"hooks"` part into it.
4. Test the hook before Claude uses it. These two lines send it a planned call, the way Claude Code does:

   ```sh
   echo '{"tool_name":"Edit","tool_input":{"file_path":"shipments-export-sample.csv"}}' | python3 .claude/hooks/protect_export.py; echo "exit $?"
   echo '{"tool_name":"Edit","tool_input":{"file_path":"clean.csv"}}' | python3 .claude/hooks/protect_export.py; echo "exit $?"
   ```

   The first prints the block message and `exit 2`. The second prints only `exit 0`. Any other result: stop here, the
   hook does not block anything yet.
5. Start `claude` in the folder. If it asks whether you trust the folder, choose `Yes, I trust this folder`. Type
   `/hooks`: you see `PreToolUse` and a `[Project]` line that starts with `python3`. The file name can be cut off.
   Press Esc.
6. Press `Shift+Tab` until the bottom line says `accept edits on`. Paste Ask 2:

   ```text
   Remove " (example)" from the client names in the export. Edit the file itself: I override the house rule for this one change.
   ```

   You should see `Blocked by a hook: shipments-export-sample.csv is read-only`, at the end of an error line. Usually
   no question comes before it (in 3 of our 22 sessions with the hook, one did, for a read). If a permission question
   comes up, choose `3. No` (the cursor starts on Yes). The turn ends. Then type `/exit`, start
   `claude` again, turn accept edits on again with `Shift+Tab`, and paste Ask 2 once more. The same applies if Claude
   only answers that CLAUDE.md does not allow it: the hook had nothing to block.
   Claude then offers you a command to run yourself, starting with `!`. Do not run it: the hook does not check it,
   and in our test it changed the CSV. Claude Code may show it as a suggestion in the input line. Do not press `Tab`:
   that fills it in, and `Enter` would then run it. If you did press `Tab`, press `Ctrl+U`, then `Backspace`.
   Also say no if Claude offers to change or turn off the hook. Claude may also offer a cleaned copy in a new file.
   That is fine if you want one: the original stays the same. The hook's message says to write a new file, while
   the step 14 CLAUDE.md says to create one only when you ask. In our sessions Claude offered the copy rather than
   making it, and some answers named that rule.
7. Type `/exit` to leave Claude Code. Check the file. Still 198 rows with "(example)":

   ```sh
   grep -c "(example)" shipments-export-sample.csv
   ```

To take the hook out later, remove the settings first, then the script. If you copied our `settings.json` in step 3:

```sh
rm .claude/settings.json
rm .claude/hooks/protect_export.py
```

If you merged the `"hooks"` part into your own `settings.json`, delete that part in a text editor first. Never delete only
the script: see The boundary.

## The boundary

- **It knows a short list of commands, and only when they spell out the file name.** It blocks Claude's Edit and Write
  tools on the file, and a shell command that names the file and has one of `>`, `sed -i`, `perl -i`, `mv`, `rm`, `cp`,
  `tee` or `truncate`. `sed -i` on `*.csv`, on `shipments-*.csv` or on a name kept in a shell variable got `exit 0`.
  Other commands that change the file get through, even when they name it. We sent the hook planned calls without Claude: an inline Python write,
  `sed -E -i`, `git checkout --` and `dd` all got `exit 0`, and so did a script like `python3 fix.py`. It is a guard
  for the commands it knows, not a lock on the file.
- **It matches the name as typed.** The same name with other capital letters got `exit 0`. On a Mac that can be the same
  file. A longer name that ends with it, like `old-shipments-export-sample.csv`, is blocked.
- **It is strict where it does match.** A backup with `cp`, `sed ... > clean.csv` and even a read with `2>/dev/null`
  are blocked, because they name the file and have `cp` or `>`. A cleaned copy like `clean.csv` through Claude's Write tool is not.
- **If the hook breaks, it can fail both ways.** Input it cannot read gave `exit 1`, and only `exit 2` blocks, so then
  nothing is blocked. That is why step 4 tests it. If the script is missing while the settings still point to it,
  `python3` itself exits with 2: in our run, Claude Code then blocked both calls Claude tried, a Write and a shell command,
  and the file was not made.
- **It guards Claude's tool calls in this folder, not yours.** A `!` command you type in Claude Code, or a change you
  make in another app, does not go through it. In our test, the `! sed -i` command Claude offers changed the CSV.
- **It does not guard itself.** An edit to `.claude/settings.json` and `rm` of the hook script both got `exit 0`. If
  Claude offers to change or turn off the hook, say no.
- **It is a program on your computer.** Claude Code starts the hook command itself. Read any hook before you add it.
- **More events exist.** This step uses one: before a tool call. See [the hooks docs](https://code.claude.com/docs/en/hooks).

## Common mistakes

| Mistake | What to do |
|---|---|
| `cp: ... No such file or directory` in step 3 | Your kit copy is older than this step, or `KIT` is not set. Do step 1, then step 3 again |
| `/hooks` shows no hook | `settings.json` must be in `.claude/` inside the folder where you start `claude`. Check with `ls .claude` |
| The test in step 4 prints `exit 0` for the CSV line | You changed the file name in the hook, or the JSON line. Copy both again |
| `python3` is not found, or a window offers to install developer tools | Accept the install, then run step 4 again. We did not test this |
| The CSV changed anyway | Look at what Claude ran. A command outside the hook's list passes. See The boundary. Copy the file again from the kit yourself (the hook only checks Claude): `cp "$KIT/builder/14-claude-md-house-rules/shipments-export-sample.csv" .` In a new Terminal window, set `KIT` again first, as in step 3 |
| Your Never line reads differently | Step 14 asked you to change a rule. The hook does not read CLAUDE.md, so it still guards the file |
| You expect CLAUDE.md to be enough | In our test it held until the ask overrode it. Then only a No at the permission question kept the file the same, unless the hook was there |

## In our own work

A hook in our own setup blocks network calls to sites that are not on an allow list. While we wrote this step, it
blocked our own download of the hooks docs page.

## Next

Step 23: workflows.
