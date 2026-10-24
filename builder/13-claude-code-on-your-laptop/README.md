# Builder, step 13: Claude Code on your own laptop, in one line

In [step 11](../11-claude-code-on-the-web/), Claude Code ran in a sandbox on the web. Today it runs on your own
computer, in your own folders. The install is one line in the terminal.

| | |
|---|---|
| Time | about 10 minutes |
| You need | a paid Claude plan (Pro, Max, Team or Enterprise), and a Mac or a Windows computer |
| Tested | the Mac install and the three questions, Claude Code 2.1.310, 24 Oct 2026. Windows: not tested |
| Download | [install-steps.md](install-steps.md), [first-three-questions.txt](first-three-questions.txt), [shipments-export-sample.csv](shipments-export-sample.csv) and [the carousel as a PDF](builder-step13-claude-code-on-your-laptop-carousel.pdf) (8 slides) |

## The one line

| Computer | Paste this in the terminal |
|---|---|
| Mac, Linux or WSL | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Windows PowerShell | `irm https://claude.ai/install.ps1 \| iex` |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` |

Source: Anthropic's setup page, [code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup).
Then open a new terminal window and type `claude --version`. A version number means it works.

The full steps per computer, with what our screen showed at each step: [install-steps.md](install-steps.md).

## Web or laptop

| | Claude Code on the web (step 11) | Claude Code on your laptop (today) |
|---|---|---|
| Where it runs | A sandbox that Anthropic hosts | Your own computer |
| Which files | A GitHub repository | Any folder you open it in |
| Install | Nothing | One line |
| Good for | A task you start and check later, from any browser | Daily work on your own files |

## Our test

On 24 Oct 2026 we ran the Mac line on a Mac, in a clean home folder with no earlier Claude Code files.

1. **The install took 10 seconds.** It printed `Claude Code successfully installed!` and `Version: 2.1.310`.
2. **The check.** `claude --version` printed `2.1.310 (Claude Code)`.
3. **The first start.** `claude` in a test folder asked for a text style, then how to sign in, then whether we trust
   the folder.
4. **Plan mode.** The new default mode is Auto mode. We pressed Shift + Tab until it said `plan mode on`. In Plan mode
   it reads, but it does not change files.
5. **Three questions** from [first-three-questions.txt](first-three-questions.txt), in a folder with only the sample
   export.

| Question | Answer | Right? |
|---|---|---|
| What is in this folder? | One file, about 198 shipment rows, and routes "out of Belgium (BE-NL, BE-FR, BE-BE)" | Partly. It missed NL-BE, the route with the most rows. It had read only the first 5 lines |
| What does the file contain? | 198 rows, 7 columns, weeks 35 to 42 of 2026, 24 August to 16 October | Yes |
| Which three routes changed most? | BE-BE +35, NL-BE +24, BE-FR -23 | Yes. The same three as in step 11 |

We checked every answer with a separate count. The sample file did not change.

The lesson: a quick question gets a quick look. For the third question it read the whole file, and it was right.
When an answer matters, ask which lines it read.

## Good to know

- **Not on Free.** Claude Code needs Pro, Max, Team or Enterprise. It uses your normal Claude limits.
- **No terminal?** The Claude desktop app has a **Code** tab with Claude Code inside. See the end of
  [install-steps.md](install-steps.md). We did not test that route today.
- **In your editor.** Claude Code has an extension for VS Code (what I use) and Cursor, and other VS Code forks can
  install it from the Open VSX registry. JetBrains IDEs (IntelliJ, PyCharm, Android Studio and more) have a plugin.
  In any other editor, type `claude` in its built-in terminal: the CLI works in any terminal. See
  [VS Code](https://code.claude.com/docs/en/vs-code) and [JetBrains](https://code.claude.com/docs/en/jetbrains).
- **Updates.** The one-line install updates itself. Homebrew and WinGet installs do not.
- **Started on the web?** Anthropic's docs say `claude --teleport` pulls a web session into your terminal. It needs a
  checkout of the same repository, the session's branch pushed, and a sign-in with your claude.ai account. We did not
  test it today. See [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web).
- **Trust only your own folders.** When it asks "Do you trust this folder?", the answer gives it read, edit and run
  rights in that folder.
- Never put real client data in a test folder. The sample export is made up.

## Time win and solution win

- **Time win:** no setup afternoon. The install took us 10 seconds. My estimate from no install to a first answer: 10 minutes.
- **Solution win:** Claude Code works on the files on your own computer, not only on a repository on the web.

## Common mistakes

| Mistake | Fix |
|---|---|
| `command not found: claude` after the install | Open a new terminal window. Still not found? The installer prints a line to add `~/.local/bin` to your PATH. Run that line |
| You start it in your home folder or Downloads | Start it in one test folder with only the sample file |
| You ask in Auto mode and it starts to make files | Press Shift + Tab until it says `plan mode on` before you ask |
| You trust the first answer | Check it, or ask which lines of the file it read |
| You are on the Free plan | Claude Code needs Pro, Max, Team or Enterprise |

## Next

Step 14 (Monday): CLAUDE.md, the house rules for one folder.
