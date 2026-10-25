# What not to put in CLAUDE.md

CLAUDE.md is read at the start of every session. Every line costs room, every time. Keep only the rules that apply
to almost every task in the folder.

| Leave it out | Why | Put it here instead |
|---|---|---|
| A long description of the folder or the code | A 2026 study found that repository overviews in context files "are not helpful" ([arXiv 2602.11988](https://arxiv.org/abs/2602.11988)). Claude can read the files itself | One or two lines: what the folder is for |
| Rules for one job only | They load in every session, also when you do another job | A context pack for that job, such as [monday-overview.md](monday-overview.md) |
| Vague rules: "format it properly", "be careful" | You cannot check them, and neither can Claude | A rule you can check: "Your first line is the table" |
| Two rules that disagree | Anthropic: "Claude may pick one arbitrarily" | One rule. Delete the other |
| More than about 200 lines | Anthropic: longer files "consume more context and reduce adherence" | Split by job, or move rules for some files into `.claude/rules/` with `paths:` |
| Passwords, API keys, client data | The file is plain text, and you may share or commit it | Nowhere in the folder |
| A rule that must never be broken | CLAUDE.md is "context, not enforced configuration". It can be ignored | Keep it as a Never line, and add a hard block later (Expert, step 21: hooks) |

Sources: [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) and
[code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices), read on 24 Oct 2026.
