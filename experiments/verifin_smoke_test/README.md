# VeriFin setup and solver sanity check

Experiment date: November 23, 2026

## Environment
- Windows
- Python 3.14.3
- Z3 5.4.1
- VeriFin repository: https://github.com/verifiedfinance/anon
- Commit: 5c49943e8aa43f3dc03c1b2058a73469b22c5c5e

## Setup findings
Windows initially could not find the standalone Z3 executable.
Adding verifin/.venv/bin to the terminal session's PATH resolved
the two initial test failures.

The resulting test run had 398 passed and 1 failed.
The remaining CAGR test timed out at 10 seconds.
Repeating that calculation with a 30-second limit also timed out.

## Solver example
Replayed the bundled FinanceBench example financebench_id_03029:
"What is the FY2018 capital expenditure amount (in USD millions) for 3M?"

The prepared evidence fixes capital expenditures at 1577 million.
The counterexample query asks whether the computed amount can
differ from the claimed answer by more than 0.5 million.

| Claimed amount (USD millions) | Solver result | Interpretation |
|---|---|---|
| 1577 | unsat | No counterexample under the encoded facts |
| 1677 | sat | Altered claim violates the tolerance |

Only the claimed answer was altered; the evidence remained 1577.

The original query also requested a model after returning unsat,
producing "model is not available." This is a separate output error.

## Scope and limitations
This was a replay of prepared solver inputs, plus a deliberately
incorrect answer. We reviewed the bundled evidence text but did
not independently verify the original filing or XBRL.

No live LLM pipeline or FinReflectKG evaluation was performed.
No VeriFin source files were changed.

This entry summarizes terminal results reported during the session;
it is not a saved raw execution log.