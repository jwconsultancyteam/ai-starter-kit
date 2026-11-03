"""Claude Code PreToolUse hook: block changes to the shipments export.

Claude Code sends the planned tool call as JSON on stdin. Exit 2 blocks the call,
and Claude Code shows the text on stderr to Claude. Exit 0 lets the call go on.
"""

import json
import re
import sys

PROTECTED = "shipments-export-sample.csv"
# Shell forms that can change a file: redirect, in-place edit, move, delete, copy over, tee, truncate.
WRITES = re.compile(r">|\bsed\s+-i|\bperl\s+-[a-z]*i|\bmv\b|\brm\b|\bcp\b|\btee\b|\btruncate\b")

call = json.load(sys.stdin)
tool = call.get("tool_name", "")
args = call.get("tool_input", {})

if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
    target = args.get("file_path") or args.get("notebook_path") or ""
    blocked = target.endswith(PROTECTED)
elif tool == "Bash":
    command = args.get("command", "")
    blocked = PROTECTED in command and bool(WRITES.search(command))
else:
    blocked = False

if blocked:
    print(f"Blocked by a hook: {PROTECTED} is read-only. Write the result to a new file.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
