"""Check that changes.py still prints the three right lines.

Run it with: python3 test_changes.py
It prints PASS or FAIL and ends with exit code 0 (pass) or 1 (fail).
It needs nothing installed. pytest can run it too.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXPECTED = [
    "1. route  BE-BE    25 ->   60  +35",
    "2. route  NL-BE    77 ->  101  +24",
    "3. route  BE-FR    71 ->   48  -23",
]


def printed_lines():
    result = subprocess.run(
        [sys.executable, "changes.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return [f"changes.py stopped with an error: {result.stderr.strip()}"]
    # The first line is the header; everything after it must match exactly.
    return result.stdout.splitlines()[1:]


def test_three_lines_unchanged():
    assert printed_lines() == EXPECTED


if __name__ == "__main__":
    got = printed_lines()
    if got == EXPECTED:
        print("PASS: changes.py prints the three expected lines.")
        sys.exit(0)
    print("FAIL: changes.py does not print the three expected lines.")
    print("Expected:")
    for line in EXPECTED:
        print(f"  {line}")
    print("Got:")
    for line in got:
        print(f"  {line}")
    sys.exit(1)
