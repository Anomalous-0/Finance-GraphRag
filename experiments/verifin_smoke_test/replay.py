import json
import subprocess
from pathlib import Path


###
###Run this in terminal: 
###cd into verifin
###.\.venv\Scripgit -C .. status --shortts\python.exe ..\experiments\verifin_smoke_test\replay.py
###

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
VERIFIN = REPO / "verifin"
Z3 = VERIFIN / ".venv" / "bin" / "z3.exe"
SOURCE = (
    VERIFIN / "examples" / "financebench_first_question_trace"
    / "11_z3_counterexample_check" / "counterexample_query.smt2"
)

original = SOURCE.read_text(encoding="utf-8")

# Remove the model request: an UNSAT result has no model to display.
matching = original.replace("(get-model)", "")

# Change only the claimed answer, leaving the evidence at 1577.
wrong = matching
for old, new in [
    ("computed_capital_expenditures 1577.0",
     "computed_capital_expenditures 1677.0"),
    ("1577.0 computed_capital_expenditures",
     "1677.0 computed_capital_expenditures"),
]:
    if wrong.count(old) != 1:
        raise ValueError(f"Expected exactly one occurrence of: {old}")
    wrong = wrong.replace(old, new)

results = []
for name, query, expected in [
    ("matching_claim", matching, "unsat"),
    ("wrong_claim", wrong, "sat"),
]:
    (HERE / f"{name}.smt2").write_text(query, encoding="utf-8")
    try:
        run = subprocess.run(
            [str(Z3), "-in"],
            input=query,
            capture_output=True,
            text=True,
            timeout=30,
        )
        lines = run.stdout.strip().splitlines()
        status = lines[0] if lines else "NO_OUTPUT"
        result = {
            "case": name,
            "expected": expected,
            "status": status,
            "returncode": run.returncode,
            "stdout": run.stdout,
            "stderr": run.stderr,
            "passed": status == expected and run.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        result = {
            "case": name,
            "expected": expected,
            "status": "TIMEOUT",
            "passed": False,
        }
    results.append(result)
    print(f"{name}: {result['status']} (expected {expected})")

(HERE / "results.json").write_text(
    json.dumps(results, indent=2), encoding="utf-8"
)
print(f"Results saved to {HERE / 'results.json'}")
raise SystemExit(0 if all(r["passed"] for r in results) else 1)