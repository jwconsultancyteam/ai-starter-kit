# Modes and rewind: cheat sheet

Claude Code 2.1.310, tested on 26 Oct 2026. Details and sources: [README.md](README.md).

## Switch the mode

Press `Shift+Tab`. The bottom line of the screen shows the mode.

| You see | Mode | Use it when |
|---|---|---|
| `⏸ plan mode on` | Plan | You want to see what it would do first. It does not change your files |
| `⏸ manual mode on` | Manual | You want to say yes to each edit and each command |
| `⏵⏵ accept edits on` | Accept edits | You trust the job. File edits run without asking. Other commands still ask |

## The ask screen

| Answer | What happens |
|---|---|
| `1. Yes` | This one edit runs |
| `2. Yes, and switch to accept edits ...` | This edit runs, and the rest of the session is in accept edits |
| `3. No` | It does not run |
| `Esc` | Cancel |

## Undo a step

1. Press `Esc` twice (with an empty input), or type `/rewind`.
2. Pick the message to go back to.
3. Choose `Restore code and conversation`.
4. Open the file and check it.

## Rewind does not undo

- a change made by a shell command (`sed`, `awk`, a script) to a file Claude had not edited with its file edit tool
- your own edits outside Claude Code
- edits from other sessions

For those: keep a copy, or use Git (step 17).
