from builtins import open
import json
from pathlib import Path

path = Path("data/benchmarks/finreflectkg_multihop/final_master_dataset.json")

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Top-level type:", type(data).__name__)

# Handle either a list or a dict with a "questions" field
if isinstance(data, list):
    questions = data
    metadata = None
else:
    questions = data.get("questions", [])
    metadata = data.get("metadata")

print("Number of questions:", len(questions))

if metadata is not None:
    print("\nMetadata:")
    print(json.dumps(metadata, indent=2))

print("\nFirst 5 questions:\n")

for i, q in enumerate(questions[:5], start=1):
    print(f"--- Question {i} ---")
    print(json.dumps(q, indent=2))
    print()