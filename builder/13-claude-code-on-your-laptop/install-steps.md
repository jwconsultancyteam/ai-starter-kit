# Install Claude Code: the steps per computer

The commands come from Anthropic's setup page:
[code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup) (read on 24 Oct 2026). We tested the Mac command
on 24 Oct 2026. We did not test the Windows commands.

You need a paid Claude plan: Pro, Max, Team or Enterprise. The Free plan does not include Claude Code.

## 1. Open a terminal

| Computer | How |
|---|---|
| Mac (macOS 13 or newer) | Press Cmd + Space, type `Terminal`, press Enter |
| Windows 10 (1809 or newer) or 11 | Open the Start menu, type `PowerShell`, press Enter. You do not need to run it as Administrator |

New to the terminal? Anthropic has a short guide:
[code.claude.com/docs/en/terminal-guide](https://code.claude.com/docs/en/terminal-guide).

## 2. Paste one line and press Enter

**Mac, Linux or WSL:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell** (your prompt starts with `PS C:\`):

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD** (your prompt starts with `C:\`, without `PS`):

```bat
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

The command shows no progress while it downloads. Wait until it says the install is complete. On our Mac that took
10 seconds.

What our Mac showed at the end:

```text
✔ Claude Code successfully installed!

  Version: 2.1.310

  Location: ~/.local/bin/claude
```

## 3. Check it

Open a **new** terminal window, then type:

```bash
claude --version
```

A working install prints a version number. Ours printed:

```text
2.1.310 (Claude Code)
```

Something wrong? `claude doctor` checks the install and changes nothing.

## 4. Start it in one folder

Make a test folder with only the sample file
([shipments-export-sample.csv](shipments-export-sample.csv)). Then:

```bash
cd ~/my-first-folder
claude
```

The first time, Claude Code asks three things:

1. **A text style.** Pick one. You can change it later with `/theme`.
2. **How to sign in.** Pick "Claude account with subscription". Your browser opens. Sign in there.
3. **Do you trust this folder?** Claude Code will be able to read, edit and run files in it. Say yes only for a folder
   you made yourself.

## 5. Switch to Plan mode before you ask

Press **Shift + Tab** until the bottom line says `plan mode on`. In Plan mode, Claude Code reads and answers but does
not change files. Then ask the three questions in [first-three-questions.txt](first-three-questions.txt).

## Updates

The one-line install updates itself in the background. Installs with Homebrew or WinGet do not: run
`brew upgrade claude-code` or `winget upgrade Anthropic.ClaudeCode` from time to time.

## No terminal at all

The Claude desktop app has a **Code** tab with Claude Code inside. You do not need the terminal for it. Download it
from [code.claude.com/docs/en/desktop-quickstart](https://code.claude.com/docs/en/desktop-quickstart), open the
**Code** tab and pick a folder on your computer. The same paid plans apply. We did not test this route today.
