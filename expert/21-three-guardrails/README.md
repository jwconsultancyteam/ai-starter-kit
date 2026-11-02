# Expert, step 21: Three guardrails for one spreadsheet

Step 19 checked a result. Step 20 compared model runs. Here the question is what a tool is allowed to do while producing its result. This is a Mac command exercise, not a model benchmark or a complete agent sandbox.

| | |
|---|---|
| Where | A Mac terminal, from an unzipped or cloned copy of this kit |
| You need | Python 3.8 or newer, /usr/bin/sandbox-exec, sh, awk, cat and curl. Uses the [step 11 sample CSV](../../builder/11-claude-code-on-the-web/shipments-export-sample.csv). No model account needed. |
| Tested | macOS 27.0.1, Python 3.12.3, 2 Nov 2026 |
| Download | [the carousel as a PDF](expert-step21-three-guardrails-carousel.pdf) (5 slides) |

## Do it yourself

From the kit root, run:

```sh
python3 expert/21-three-guardrails/demo.py
```

[Read the script](demo.py) before running it. It copies the CSV into a temporary directory, creates a dummy private note and starts a local HTTP listener. It runs four commands without its policy, resets the CSV and removes the first report, then runs the same commands under the policy. The first command counts lines below the header with awk. This works for this fixture: the script also checks the count with Python's CSV reader. Do not generalise that line-counting shortcut to CSV files with multiline records.

## What happened

### One spreadsheet. Three guardrails.

Can the report still be written if the source stays untouched?

- THE JOB: Count the shipment rows and save a report.
- THE TEST: Run the same four commands with the guardrails off and on.

### Protect the original

The command tried to append a line to a disposable copy of the CSV.

- GUARDRAILS OFF: The append succeeded.
- GUARDRAILS ON: The append failed. The CSV fingerprint stayed the same.

### Give it the exact path

A dummy private note sat outside the output folder. The command knew where it was.

- GUARDRAILS OFF: The command read the note.
- GUARDRAILS ON: The read failed. This rule protected that note, not the whole Mac.

### Test the connection

A harmless endpoint listened on the same Mac. The request carried no shipment data.

- GUARDRAILS OFF: The endpoint answered.
- GUARDRAILS ON: The request failed. No internet upload was tested.

### Keep the useful result

The report still said 198 shipment rows with the guardrails on.

- TRY IT: Run the demo from the AI Starter Kit on a Mac.
- WHAT THIS SHOWS: The commands ran under a policy. No model chose them.

## The boundary

The policy applies to the child commands, not to the Python harness that sets up and checks the exercise. It denies file writes except under the temporary output directory, denies reads of the exact dummy-note path, and denies network operations. The run checks one append, one direct read and one HTTP request to loopback. It does not test another path to the note, protect all the other readable files on the host, or demonstrate an internet upload. Do not use this as a policy for running untrusted code.

Both reports read `Shipment rows: 198`. The append changed the disposable CSV in the control. With restrictions, the append and note read exited 1 and curl exited 7. The SHA-256 of the restricted input copy was unchanged. The original kit file was not the target of any write. Temporary files are removed on normal exit.
