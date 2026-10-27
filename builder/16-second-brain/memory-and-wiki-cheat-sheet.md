# Memory and wiki: cheat sheet

Claude Code 2.1.312, tested on 28 Oct 2026. Details and sources: [README.md](README.md).

## Two kinds of memory

| | Auto memory | A wiki in your folder |
|---|---|---|
| Who writes it | Claude, when it learns something | Claude, from your notes, with your rules |
| Where | `~/.claude/projects/<project>/memory/`, on your own computer | A `wiki/` folder next to your notes |
| What loads | The first 200 lines or 25KB of `MEMORY.md`, at the start of every session | `CLAUDE.md`. Claude reads `wiki/index.md` first, then the pages it needs |
| Good for | Things you tell Claude in chat | Facts from many notes: prices, what changed, what was never agreed |

## Auto memory

- On by default. Check it with `/memory`. The toggle is there too.
- Say "Remember this: ...". Claude saves a note and adds one line to `MEMORY.md`.
- Open the folder with `/memory` and read what it saved. You can edit or delete any file.

## The wiki, in 3 jobs

| You say | Claude does |
|---|---|
| "Build the wiki from all notes in notes/." | Writes one page per client and topic, `index.md` and `log.md` |
| "Add notes/<file>." | Updates every page the note touches, the index and the log |
| "Check the wiki." | Lists facts that disagree, pages missing from the index, lines without a source |

## Rules that kept it right in our test

- One "Current state" per page. A new fact replaces the old one. The old one moves to "History".
- A note that was not sent or not agreed goes under "Not agreed".
- Every fact names its source note.
- Never change the raw notes.
